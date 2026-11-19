#!/usr/bin/env python3
"""
afe_model.py -- Idealized block model of the documented CUP Rev1.1 AFE.

CLASSICAL SOFTWARE BLOCK MODEL. NOT a transistor-level / SPICE model.
NOT a simulation of quantum noise. NOT a model of any physical Zener's
measured behavior. NOT a tested or fabricated hardware board. NOT
fabrication-authorized or physically validated. NOT connected to Double
Alpha, 004c, GitHub, or any other repository/experiment.

The input-noise distribution is synthetic and user-selectable
(white / telegraph / burst / sine). The Zener D1=1N4732A appears only as a
labeled block; its avalanche-noise statistics are NOT modeled (an explicit
assumption per the public design records).

Standard library only. No network. No third-party packages. No hardware.

Signal path:
  synthetic source -> C1 high-pass -> non-inverting amp (TLV9062)
                   -> 1st-order anti-alias low-pass -> rail clamp
                   -> 12-bit ADC sampling at f_s = 500 kS/s

Public design-record values (from task):
  D1 = 1N4732A, R_bias = 100 kOhm, C1 = 0.1 uF,
  TLV9062, R2 = 1 kOhm, R3 = 47 kOhm (nominal gain: doc says 47; formula = 48),
  V_ref = 1.65 V,
  R6 = 1 kOhm, C3 = 750 pF (anti-alias corner ~= 212.2 kHz),
  RP2350/Pico 2 GP26 ADC at 500 kS/s, clamp to analog rails.

Added assumptions (DO NOT silently treat as schematic facts; see DESIGN_NOTE):
  A1  R_eff for C1 high-pass = 100 kOhm (CLI --r-eff). Schematic does not specify.
  A2  Analog rails: V_lo=0 V, V_hi=3.3 V (CLI --v-lo, --v-hi). RP2350 ADC full-scale.
  A3  Input-noise distribution is synthetic, user-selectable. Default white sigma=1 V (arbitrary).
  A4  ADC bit depth = 12 bits (codes 0..4095).
  A5  Op-amp ideal (infinite GBW, zero noise, zero bias).
  A6  Synthetic source mean becomes C1 input DC; high-pass removes it; output referenced to V_ref.
  A7  Bilinear transform discretization at dt = 1/f_s = 2 us.
  A8  Ideal impulse sampling at t = k/f_s (no aperture jitter, no S/H droop).
"""

import argparse
import csv
import math
import random
import sys
from typing import List, Tuple


# --------------------------------------------------------------------------- #
# Design-record constants (DO NOT change without explicit task instruction)
# --------------------------------------------------------------------------- #

R_BIAS      = 100_000.0       # Ohm (documented; Zener bias)
C1          = 0.1e-6          # F   (documented; coupling cap)
R2          = 1_000.0         # Ohm (documented; feedback lower leg)
R3          = 47_000.0        # Ohm (documented; feedback upper leg)
V_REF       = 1.65            # V   (documented; output bias / mid-supply ref)
R6          = 1_000.0         # Ohm (documented; anti-alias series R)
C3          = 750e-12         # F   (documented; anti-alias shunt C)
F_S         = 500_000.0       # S/s (documented; ADC sample rate)
ADC_BITS    = 12

# Derived (formula)
GAIN_FORMULA = 1.0 + R3 / R2          # = 48.0
GAIN_DOC     = 47.0                   # documented nominal value (flagged)
F_HP         = 1.0 / (2 * math.pi * R_BIAS * C1)   # high-pass corner IF R_eff=R_bias ~= 15.9 Hz
F_LP         = 1.0 / (2 * math.pi * R6 * C3)       # anti-alias corner ~= 212.2 kHz
F_NYQUIST    = F_S / 2.0              # 250 kHz


# --------------------------------------------------------------------------- #
# Synthetic sources
# --------------------------------------------------------------------------- #

def src_white(rng: random.Random, n: int, mu: float, sigma: float) -> List[float]:
    return [rng.gauss(mu, sigma) for _ in range(n)]

def src_telegraph(rng: random.Random, n: int, amp: float, switch_p: float) -> List[float]:
    state = amp if rng.random() < 0.5 else -amp
    out = []
    for _ in range(n):
        if rng.random() < switch_p:
            state = -state
        out.append(state)
    return out

def src_burst(rng: random.Random, n: int, p_burst: float, burst_len: int,
              burst_sigma: float) -> List[float]:
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

def src_sine(n: int, amp: float, freq: float, fs: float,
             phase: float = 0.0) -> List[float]:
    """Deterministic sine sampled at t = k/fs."""
    return [amp * math.sin(2.0 * math.pi * freq * (k / fs) + phase)
            for k in range(n)]


# --------------------------------------------------------------------------- #
# First-order filter implementations (bilinear transform)
# --------------------------------------------------------------------------- #

def biquad_hp_bilinear(dt: float, f_c: float) -> Tuple[float, float, float, float]:
    """First-order high-pass via bilinear transform of H(s) = sRC/(1+sRC).

    Returns (b0, b1, a1) for y[n] = b0*x[n] + b1*x[n-1] - a1*y[n-1].
    The fourth tuple element is a placeholder for API symmetry (set to 0.0).
    """
    wc = 2.0 * math.pi * f_c
    # Pre-warp
    K = 2.0 / dt
    # H(z) = (K - (2/dt) * (1-z^-1)) / (K + wc) ... actually the standard form:
    # bilinear: s = (2/dt) * (1 - z^-1) / (1 + z^-1)
    # H_HP(s) = sRC/(1+sRC) = s/(s + wc)  where wc = 1/(RC)
    # Substitute and simplify:
    a0 = K + wc
    b0 =  K / a0
    b1 = -K / a0
    a1 = (wc - K) / a0
    return (b0, b1, a1, 0.0)

def biquad_lp_bilinear(dt: float, f_c: float) -> Tuple[float, float, float, float]:
    """First-order low-pass via bilinear transform of H(s) = 1/(1+sRC) = wc/(s+wc)."""
    wc = 2.0 * math.pi * f_c
    K = 2.0 / dt
    a0 = K + wc
    b0 =  wc / a0
    b1 =  wc / a0
    a1 = (wc - K) / a0
    return (b0, b1, a1, 0.0)

def apply_first_order(x: List[float], b0: float, b1: float,
                      a1: float) -> List[float]:
    """y[n] = b0*x[n] + b1*x[n-1] - a1*y[n-1]. Zero initial conditions."""
    y: List[float] = [0.0] * len(x)
    y_prev = 0.0
    x_prev = 0.0
    for i, xi in enumerate(x):
        yi = b0 * xi + b1 * x_prev - a1 * y_prev
        y[i] = yi
        x_prev = xi
        y_prev = yi
    return y


# --------------------------------------------------------------------------- #
# Full signal path
# --------------------------------------------------------------------------- #

def run_pipeline(x: List[float], fs: float, r_eff: float,
                 v_lo: float, v_hi: float,
                 gain: float = GAIN_FORMULA) -> Tuple[List[float], List[float],
                                                      List[float], List[int]]:
    """Run the full AFE pipeline.

    Returns (v_hp, v_amp, v_clamp, adc_codes).
    """
    n = len(x)
    dt = 1.0 / fs
    # Stage 2: C1 high-pass
    f_hp = 1.0 / (2.0 * math.pi * r_eff * C1)
    b0, b1, a1, _ = biquad_hp_bilinear(dt, f_hp)
    v_hp = apply_first_order(x, b0, b1, a1)
    # Stage 3: non-inverting amp (single-supply, biased at V_REF).
    # After AC coupling through C1, v_hp is the AC component centered at 0.
    # The op-amp v+ sits at V_REF + v_hp (V_REF from the bias network plus
    # the AC-coupled signal), and v- follows v+, so:
    #   v_amp = V_REF + gain * v_hp
    # (NOT V_REF + gain*(v_hp - V_REF); that would be correct only if v_hp
    # were centered at V_REF, which it is not after C1.)
    v_amp = [V_REF + gain * v for v in v_hp]
    # Stage 4: anti-alias low-pass
    b0l, b1l, a1l, _ = biquad_lp_bilinear(dt, F_LP)
    v_lp = apply_first_order(v_amp, b0l, b1l, a1l)
    # Stage 5: rail clamp
    v_clamp = [min(max(v, v_lo), v_hi) for v in v_lp]
    # Stage 6: 12-bit ADC
    span = v_hi - v_lo
    if span <= 0:
        raise ValueError(f"v_hi ({v_hi}) must be > v_lo ({v_lo})")
    codes_max = (1 << ADC_BITS) - 1
    adc_codes = [int(round((v - v_lo) / span * codes_max)) for v in v_clamp]
    adc_codes = [min(max(c, 0), codes_max) for c in adc_codes]
    return v_hp, v_amp, v_clamp, adc_codes


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="afe_model",
        description=("Idealized block model of the documented CUP Rev1.1 AFE. "
                     "NOT hardware. NOT quantum. NOT validated. "
                     "Synthetic input only."),
        epilog=("Every added assumption is documented in DESIGN_NOTE.md and in "
                "the module docstring. Do not treat assumptions as schematic facts."),
    )
    p.add_argument("--seed", type=int, default=0,
                   help="Seed for synthetic noise sources (default 0).")
    p.add_argument("--source", choices=["white", "telegraph", "burst", "sine"],
                   default="white", help="Synthetic input source (default white).")
    p.add_argument("--samples", type=int, default=1000,
                   help="Number of output samples (default 1000).")
    p.add_argument("--r-eff", type=float, default=R_BIAS,
                   help=("Effective resistance for C1 high-pass in Ohm "
                         f"(default {R_BIAS} = R_bias; ASSUMPTION A1)."))
    p.add_argument("--v-lo", type=float, default=0.0,
                   help="Lower analog rail V_lo in V (default 0.0; ASSUMPTION A2).")
    p.add_argument("--v-hi", type=float, default=3.3,
                   help="Upper analog rail V_hi in V (default 3.3; ASSUMPTION A2).")
    # Source params
    p.add_argument("--mu", type=float, default=0.0, help="white: mean V (default 0).")
    p.add_argument("--sigma", type=float, default=1.0,
                   help="white: std dev V (default 1; arbitrary, not a measured Zener value).")
    p.add_argument("--amplitude", type=float, default=1.0,
                   help="telegraph/sine: amplitude (default 1).")
    p.add_argument("--switch-prob", type=float, default=0.05,
                   help="telegraph: per-step flip probability (default 0.05).")
    p.add_argument("--p-burst", type=float, default=0.02,
                   help="burst: per-step trigger probability (default 0.02).")
    p.add_argument("--burst-len", type=int, default=10,
                   help="burst: samples per burst (default 10).")
    p.add_argument("--burst-sigma", type=float, default=2.0,
                   help="burst: Gaussian std dev of burst samples (default 2.0).")
    p.add_argument("--freq", type=float, default=10_000.0,
                   help="sine: frequency in Hz (default 10000).")
    p.add_argument("--phase", type=float, default=0.0,
                   help="sine: phase in rad (default 0).")
    p.add_argument("--stage", choices=["adc", "clamp", "amp", "hp", "all"],
                   default="adc",
                   help=("Output stage: adc (default), clamp, amp, hp, or all "
                         "(all = index,source,hp,amp,clamp,adc)."))
    return p.parse_args(argv)


def build_source(args) -> List[float]:
    n = args.samples
    if args.source == "sine":
        return src_sine(n, args.amplitude, args.freq, F_S, args.phase)
    rng = random.Random(args.seed)
    if args.source == "white":
        return src_white(rng, n, args.mu, args.sigma)
    if args.source == "telegraph":
        if not (0.0 <= args.switch_prob <= 1.0):
            raise SystemExit("--switch-prob must be in [0,1]")
        return src_telegraph(rng, n, args.amplitude, args.switch_prob)
    if args.source == "burst":
        if not (0.0 <= args.p_burst <= 1.0):
            raise SystemExit("--p-burst must be in [0,1]")
        if args.burst_len < 1:
            raise SystemExit("--burst-len must be >= 1")
        return src_burst(rng, n, args.p_burst, args.burst_len, args.burst_sigma)
    raise SystemExit(f"unknown source: {args.source}")


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.samples < 1:
        raise SystemExit("--samples must be >= 1")
    if args.v_hi <= args.v_lo:
        raise SystemExit("--v-hi must be > --v-lo")

    x = build_source(args)
    v_hp, v_amp, v_clamp, adc = run_pipeline(
        x, F_S, args.r_eff, args.v_lo, args.v_hi)

    w = csv.writer(sys.stdout)
    # Header comment carries all design values and flagged discrepancies.
    w.writerow([f"# afe_model.py output"])
    w.writerow([f"# source={args.source} seed={args.seed} samples={args.samples}"])
    w.writerow([f"# D1=1N4732A R_bias={R_BIAS} C1={C1} TLV9062 R2={R2} R3={R3} V_ref={V_REF}"])
    w.writerow([f"# R6={R6} C3={C3} f_s={F_S} ADC_bits={ADC_BITS}"])
    w.writerow([f"# documented_gain={GAIN_DOC} formula_gain={GAIN_FORMULA} (FLAGGED: see DESIGN_NOTE)"])
    w.writerow([f"# r_eff(assumption A1)={args.r_eff} f_hp={1/(2*math.pi*args.r_eff*C1):.3f}"])
    w.writerow([f"# f_lp(anti-alias)={F_LP:.3f} f_nyquist={F_NYQUIST:.3f}"])
    w.writerow([f"# v_lo(assumption A2)={args.v_lo} v_hi(assumption A2)={args.v_hi}"])

    if args.stage == "all":
        w.writerow(["index", "source", "v_hp", "v_amp", "v_clamp", "adc_code"])
        for i in range(args.samples):
            w.writerow([i, x[i], v_hp[i], v_amp[i], v_clamp[i], adc[i]])
    elif args.stage == "hp":
        w.writerow(["index", "v_hp"]); 
        for i in range(args.samples): w.writerow([i, v_hp[i]])
    elif args.stage == "amp":
        w.writerow(["index", "v_amp"])
        for i in range(args.samples): w.writerow([i, v_amp[i]])
    elif args.stage == "clamp":
        w.writerow(["index", "v_clamp"])
        for i in range(args.samples): w.writerow([i, v_clamp[i]])
    else:  # adc
        w.writerow(["index", "adc_code"])
        for i in range(args.samples): w.writerow([i, adc[i]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
