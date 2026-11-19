#!/usr/bin/env python3
"""
afe_compare.py -- Topology comparison + R_eff sweep for the documented
CUP Rev1.1 AFE.

CLASSICAL SOFTWARE BLOCK MODEL. NOT a determination of which topology is
the real board. NOT a simulation of quantum noise. NOT a model of any
physical Zener's measured behavior. NOT a tested or fabricated hardware
board. NOT fabrication-authorized or physically validated. NOT connected
to Double Alpha, 004c, GitHub, or any other repository/experiment.

Two hypothetical topology alternatives (both labeled as model alternatives,
NOT circuit facts):
  A) non-inverting:  Vout = Vref + 48 * Vin   (G = 1 + R3/R2 = 48, sign +)
  B) inverting:      Vout = Vref - 47 * Vin   (G = R3/R2 = 47, sign -)
                              (matches the project-notes formula G = R3/R2)

The available schematic record is text-only and does not establish the
complete topology. No winner is picked.

Standard library only. No network. No third-party packages. No hardware.

Signal path (unchanged from the prior afe-v2 model except for topology select):
  synthetic source -> C1 high-pass (R_eff-sweepable) -> [topology A or B]
                    -> 1st-order anti-alias low-pass -> rail clamp
                    -> 12-bit ADC at f_s = 500 kS/s

Public design-record values (from task):
  D1 = 1N4732A, R_bias = 100 kOhm, C1 = 0.1 uF,
  TLV9062, R2 = 1 kOhm, R3 = 47 kOhm, V_ref = 1.65 V,
  R6 = 1 kOhm, C3 = 750 pF, RP2350/Pico 2 GP26 ADC at 500 kS/s.

Added assumptions (DO NOT silently treat as schematic facts; see DESIGN_NOTE):
  A1   R_eff for C1 high-pass = 100 kOhm default; SWEEP at 10k/100k/1M (CLI --r-eff).
  A2   Rails: V_lo=0 V, V_hi=3.3 V (RP2350 ADC full-scale; CLI --v-lo, --v-hi).
  A3   Input distribution synthetic, user-selectable.
  A4   ADC = 12 bits.
  A5   Op-amp ideal.
  A6   Source mean becomes C1 input DC; HP removes it.
  A7   Bilinear discretization at dt = 1/f_s.
  A8   Ideal impulse sampling.
  A9   Topology unspecified by text-only record; both A and B modeled.
  A10  Single gain stage only.
"""

import argparse
import csv
import math
import random
import sys
from typing import Dict, List, Tuple


# --------------------------------------------------------------------------- #
# Design-record constants (DO NOT change without explicit task instruction)
# --------------------------------------------------------------------------- #

R_BIAS      = 100_000.0
C1          = 0.1e-6
R2          = 1_000.0
R3          = 47_000.0
V_REF       = 1.65
R6          = 1_000.0
C3          = 750e-12
F_S         = 500_000.0
ADC_BITS    = 12

# Two hypothetical topology gains
G_NON_INV = 1.0 + R3 / R2   # = 48.0  (formula gain for non-inverting)
G_INV     = R3 / R2         # = 47.0  (matches the project-notes formula G = R3/R2)
GAIN_DOC  = 47.0            # documented nominal value

F_LP      = 1.0 / (2.0 * math.pi * R6 * C3)   # ~212.2 kHz
F_NYQUIST = F_S / 2.0                        # 250 kHz


# --------------------------------------------------------------------------- #
# Synthetic sources
# --------------------------------------------------------------------------- #

def src_white(rng, n, mu, sigma): return [rng.gauss(mu, sigma) for _ in range(n)]

def src_telegraph(rng, n, amp, switch_p):
    state = amp if rng.random() < 0.5 else -amp
    out = []
    for _ in range(n):
        if rng.random() < switch_p:
            state = -state
        out.append(state)
    return out

def src_burst(rng, n, p_burst, burst_len, burst_sigma):
    out = [0.0] * n
    i = 0
    while i < n:
        if rng.random() < p_burst:
            end = min(i + burst_len, n)
            for j in range(i, end):
                out[j] = rng.gauss(0.0, burst_sigma)
            i = end
        else:
            i += 1
    return out

def src_sine(n, amp, freq, fs, phase=0.0):
    return [amp * math.sin(2.0 * math.pi * freq * (k / fs) + phase) for k in range(n)]


# --------------------------------------------------------------------------- #
# Bilinear first-order filters
# --------------------------------------------------------------------------- #

def biquad_hp_bilinear(dt, f_c):
    wc = 2.0 * math.pi * f_c
    K = 2.0 / dt
    a0 = K + wc
    b0 =  K / a0
    b1 = -K / a0
    a1 = (wc - K) / a0
    return (b0, b1, a1)

def biquad_lp_bilinear(dt, f_c):
    wc = 2.0 * math.pi * f_c
    K = 2.0 / dt
    a0 = K + wc
    b0 =  wc / a0
    b1 =  wc / a0
    a1 = (wc - K) / a0
    return (b0, b1, a1)

def apply_first_order(x, b0, b1, a1):
    y = [0.0] * len(x)
    y_prev = 0.0
    x_prev = 0.0
    for i, xi in enumerate(x):
        yi = b0 * xi + b1 * x_prev - a1 * y_prev
        y[i] = yi
        x_prev = xi
        y_prev = yi
    return y


# --------------------------------------------------------------------------- #
# Topology-selectable amplifier
# --------------------------------------------------------------------------- #

def apply_amp(v_hp: List[float], topology: str) -> List[float]:
    """Apply the topology-selectable amplifier stage.

    Both formulas are HYPOTHETICAL model alternatives, NOT circuit facts.
    The available schematic record is text-only and does not establish
    the complete topology.

      A) non-inverting:  Vout = Vref + 48 * v_hp   (gain +48)
      B) inverting:      Vout = Vref - 47 * v_hp   (gain -47, matches G=R3/R2)
    """
    if topology == "non-inverting":
        g = G_NON_INV
        return [V_REF + g * v for v in v_hp]
    if topology == "inverting":
        g = G_INV
        return [V_REF - g * v for v in v_hp]
    raise ValueError(f"unknown topology: {topology!r}")


# --------------------------------------------------------------------------- #
# Full pipeline (topology-aware)
# --------------------------------------------------------------------------- #

def run_pipeline(x, fs, r_eff, v_lo, v_hi, topology):
    n = len(x)
    dt = 1.0 / fs
    # C1 high-pass
    f_hp = 1.0 / (2.0 * math.pi * r_eff * C1)
    b0, b1, a1 = biquad_hp_bilinear(dt, f_hp)
    v_hp = apply_first_order(x, b0, b1, a1)
    # Topology-selectable amplifier
    v_amp = apply_amp(v_hp, topology)
    # Anti-alias low-pass
    b0l, b1l, a1l = biquad_lp_bilinear(dt, F_LP)
    v_lp = apply_first_order(v_amp, b0l, b1l, a1l)
    # Rail clamp
    v_clamp = [min(max(v, v_lo), v_hi) for v in v_lp]
    # 12-bit ADC
    span = v_hi - v_lo
    if span <= 0:
        raise ValueError(f"v_hi ({v_hi}) must be > v_lo ({v_lo})")
    codes_max = (1 << ADC_BITS) - 1
    adc = [int(round((v - v_lo) / span * codes_max)) for v in v_clamp]
    adc = [min(max(c, 0), codes_max) for c in adc]
    return {
        "v_hp": v_hp,
        "v_amp": v_amp,
        "v_clamp": v_clamp,
        "adc": adc,
        "f_hp": f_hp,
        "topology": topology,
        "r_eff": r_eff,
    }


# --------------------------------------------------------------------------- #
# R_eff sweep
# --------------------------------------------------------------------------- #

DEFAULT_SWEEP_R_EFF = (10_000.0, 100_000.0, 1_000_000.0)

def sweep_r_eff(source_fn, n, fs, v_lo, v_hi, topologies, r_effs=DEFAULT_SWEEP_R_EFF):
    """Run the pipeline across the cartesian product of (r_eff, topology).

    source_fn is a callable returning the input list (so each sweep point
    uses the same input). Returns a list of dicts, each augmented with
    measurements.
    """
    x = source_fn()
    rows = []
    for r_eff in r_effs:
        for topo in topologies:
            res = run_pipeline(x, fs, r_eff, v_lo, v_hi, topo)
            v_amp = res["v_amp"][n // 5:]  # skip first 20% for transients
            v_clamp_ss = res["v_clamp"][n // 5:]
            res["v_amp_pp"]   = max(v_amp) - min(v_amp)
            res["v_amp_mean"] = sum(v_amp) / len(v_amp)
            res["v_clamp_pp"] = max(v_clamp_ss) - min(v_clamp_ss)
            res["v_clamp_mean"] = sum(v_clamp_ss) / len(v_clamp_ss)
            rows.append(res)
    return rows


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="afe_compare",
        description=("Topology comparison + R_eff sweep for the documented "
                     "CUP Rev1.1 AFE. Two HYPOTHETICAL topology alternatives; "
                     "no winner picked. NOT hardware. NOT quantum."),
        epilog=("All assumptions are documented in DESIGN_NOTE.md and in the "
                "module docstring. Do not treat assumptions as schematic facts."),
    )
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--source", choices=["white", "telegraph", "burst", "sine"],
                   default="sine",
                   help="Synthetic source (default sine, for clean comparison).")
    p.add_argument("--samples", type=int, default=1000)
    p.add_argument("--topology",
                   choices=["non-inverting", "inverting", "both"],
                   default="both",
                   help="Topology alternative(s) to run (default both).")
    p.add_argument("--r-eff", type=float, default=R_BIAS,
                   help=("Effective resistance for C1 HP in Ohm "
                         f"(default {R_BIAS}; ASSUMPTION A1)."))
    p.add_argument("--v-lo", type=float, default=0.0)
    p.add_argument("--v-hi", type=float, default=3.3)
    # Source params
    p.add_argument("--mu", type=float, default=0.0)
    p.add_argument("--sigma", type=float, default=1.0)
    p.add_argument("--amplitude", type=float, default=0.02,
                   help="sine/telegraph amplitude (default 0.02 V).")
    p.add_argument("--switch-prob", type=float, default=0.05)
    p.add_argument("--p-burst", type=float, default=0.02)
    p.add_argument("--burst-len", type=int, default=10)
    p.add_argument("--burst-sigma", type=float, default=2.0)
    p.add_argument("--freq", type=float, default=1000.0,
                   help="sine frequency in Hz (default 1000).")
    p.add_argument("--phase", type=float, default=0.0)
    # Mode
    p.add_argument("--mode", choices=["samples", "sweep"], default="samples",
                   help=("samples = emit per-sample CSV (default); "
                         "sweep = emit R_eff sweep summary."))
    p.add_argument("--sweep-freq", type=float, default=100.0,
                   help=("sine frequency for R_eff sweep probe (default 100 Hz; "
                         "shows the corner-frequency effect)."))
    p.add_argument("--sweep-amp", type=float, default=0.02,
                   help="sine amplitude for R_eff sweep probe (default 0.02 V).")
    p.add_argument("--sweep-n", type=int, default=50000,
                   help="sample count for sweep probe (default 50000).")
    return p.parse_args(argv)


def build_source(args, n=None, freq_override=None, amp_override=None):
    n = n if n is not None else args.samples
    freq = freq_override if freq_override is not None else args.freq
    amp = amp_override if amp_override is not None else args.amplitude
    if args.source == "sine":
        return src_sine(n, amp, freq, F_S, args.phase)
    rng = random.Random(args.seed)
    if args.source == "white":
        return src_white(rng, n, args.mu, args.sigma)
    if args.source == "telegraph":
        return src_telegraph(rng, n, amp, args.switch_prob)
    if args.source == "burst":
        return src_burst(rng, n, args.p_burst, args.burst_len, args.burst_sigma)
    raise SystemExit(f"unknown source: {args.source}")


def _emit_header(w, args, r_eff=None):
    w.writerow(["# afe_compare.py output"])
    w.writerow([f"# source={args.source} seed={args.seed} samples={args.samples}"])
    w.writerow([f"# D1=1N4732A R_bias={R_BIAS} C1={C1} TLV9062 R2={R2} R3={R3} V_ref={V_REF}"])
    w.writerow([f"# R6={R6} C3={C3} f_s={F_S} ADC_bits={ADC_BITS}"])
    w.writerow([f"# G_non-inv(A)={G_NON_INV} G_inv(B)={G_INV} GAIN_DOC={GAIN_DOC} (FLAGGED: see DESIGN_NOTE)"])
    w.writerow([f"# f_lp(anti-alias)={F_LP:.3f} f_nyquist={F_NYQUIST:.3f}"])
    if r_eff is not None:
        w.writerow([f"# r_eff={r_eff} f_hp={1/(2*math.pi*r_eff*C1):.3f}"])
    w.writerow([f"# v_lo(A2)={args.v_lo} v_hi(A2)={args.v_hi}"])
    w.writerow([f"# topology_select={args.topology} (A=non-inv, B=inv; both HYPOTHETICAL)"])


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.samples < 1:
        raise SystemExit("--samples must be >= 1")
    if args.v_hi <= args.v_lo:
        raise SystemExit("--v-hi must be > --v-lo")

    w = csv.writer(sys.stdout)

    if args.mode == "sweep":
        n = args.sweep_n
        topologies = (["non-inverting", "inverting"]
                      if args.topology == "both" else [args.topology])
        r_effs = DEFAULT_SWEEP_R_EFF
        def source_fn():
            return src_sine(n, args.sweep_amp, args.sweep_freq, F_S, 0.0)
        rows = sweep_r_eff(source_fn, n, F_S, args.v_lo, args.v_hi, topologies, r_effs)
        # Header
        w.writerow(["# afe_compare.py SWEEP output"])
        w.writerow([f"# sweep_freq={args.sweep_freq} Hz sweep_amp={args.sweep_amp} V"])
        w.writerow([f"# sweep_n={n} samples (skip first {n//5} for transients)"])
        w.writerow([f"# D1=1N4732A R_bias={R_BIAS} C1={C1} TLV9062 R2={R2} R3={R3} V_ref={V_REF}"])
        w.writerow([f"# G_non-inv(A)={G_NON_INV} G_inv(B)={G_INV} GAIN_DOC={GAIN_DOC}"])
        w.writerow([f"# f_lp={F_LP:.3f} f_nyquist={F_NYQUIST:.3f}"])
        w.writerow([f"# v_lo(A2)={args.v_lo} v_hi(A2)={args.v_hi}"])
        w.writerow([f"# ALL topos HYPOTHETICAL; no winner picked (A9)"])
        w.writerow(["r_eff_ohm", "f_hp_hz", "topology",
                    "v_amp_pp_V", "v_amp_mean_V",
                    "v_clamp_pp_V", "v_clamp_mean_V"])
        for r in rows:
            w.writerow([f"{r['r_eff']:.0f}", f"{r['f_hp']:.3f}", r["topology"],
                        f"{r['v_amp_pp']:.6f}", f"{r['v_amp_mean']:.6f}",
                        f"{r['v_clamp_pp']:.6f}", f"{r['v_clamp_mean']:.6f}"])
        return 0

    # Per-sample mode
    _emit_header(w, args, r_eff=args.r_eff)
    x = build_source(args)

    if args.topology == "both":
        res_a = run_pipeline(x, F_S, args.r_eff, args.v_lo, args.v_hi, "non-inverting")
        res_b = run_pipeline(x, F_S, args.r_eff, args.v_lo, args.v_hi, "inverting")
        w.writerow(["index", "source", "v_hp",
                    "v_amp_A", "v_clamp_A", "adc_A",
                    "v_amp_B", "v_clamp_B", "adc_B"])
        for i in range(args.samples):
            w.writerow([i, x[i], res_a["v_hp"][i],
                        res_a["v_amp"][i], res_a["v_clamp"][i], res_a["adc"][i],
                        res_b["v_amp"][i], res_b["v_clamp"][i], res_b["adc"][i]])
    else:
        res = run_pipeline(x, F_S, args.r_eff, args.v_lo, args.v_hi, args.topology)
        w.writerow(["index", "source", "v_hp", "v_amp", "v_clamp", "adc_code"])
        for i in range(args.samples):
            w.writerow([i, x[i], res["v_hp"][i], res["v_amp"][i],
                        res["v_clamp"][i], res["adc"][i]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
