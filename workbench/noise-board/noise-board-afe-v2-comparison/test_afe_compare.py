#!/usr/bin/env python3
"""
test_afe_compare.py -- Automated tests for afe_compare.py.

CLASSICAL SOFTWARE BLOCK MODEL TESTS ONLY.
These tests verify properties of an idealized software block model built from
documented design-record values plus the assumptions listed in DESIGN_NOTE.md.
They do NOT establish hardware equivalence, quantum-noise fidelity, physical
Zener behavior, or any experimental result. They are NOT connected to Double
Alpha, 004c, GitHub, or any other repository or experiment.

The two topology alternatives (A: non-inverting, B: inverting) are both
HYPOTHETICAL model alternatives. The tests verify each equation and sign
independently. No winner is picked.

===============================================================================
TEST CRITERIA (stated before running)
===============================================================================

1. Topology A equation and sign (non-inverting, Vout = Vref + 48*Vin):
   - 1 kHz sine, amp=0.02 V, n=50000, slice [40000:50000] (10 integer periods).
   - G_NON_INV == 48.0 (formula: 1 + R3/R2).
   - |mean(v_amp) - V_REF| <= 0.01 V.
   - |v_amp p-p - 1.92 V| / 1.92 <= 0.05 (rel).
   - Sign: sample Pearson(v_hp, v_amp) > 0.99 (positive correlation).
   - Sign-index: argmax(v_amp) coincides with argmax(v_hp) (modulo period).

2. Topology B equation and sign (inverting, Vout = Vref - 47*Vin):
   - Same input as (1).
   - G_INV == 47.0 (formula: R3/R2, matches project-notes G = R3/R2).
   - |mean(v_amp) - V_REF| <= 0.01 V.
   - |v_amp p-p - 1.88 V| / 1.88 <= 0.05 (rel).
   - Sign: sample Pearson(v_hp, v_amp) < -0.99 (negative correlation).
   - Sign-index: argmax(v_amp) coincides with argmin(v_hp) (modulo period).

3. R_eff sweep -- corner frequencies match analytical:
   - For R_eff in {10 kOhm, 100 kOhm, 1 MOhm}, f_HP reported by the pipeline
     matches 1/(2*pi*R_eff*C1) within 0.1% relative.
     Expected: 159.155 Hz, 15.9155 Hz, 1.59155 Hz.

4. R_eff sweep -- high-frequency reference is sweep-invariant:
   - At 10 kHz (well above all three corners: 10 kHz is 63x above the
     highest corner 159 Hz, 630x above 15.9 Hz, 6300x above 1.59 Hz),
     |H_HP(10 kHz)| > 0.9998 for all three R_eff, so v_amp p-p for both
     topologies varies by less than 1% relative across the three R_eff values.
     Expected: ~1.92 V (A) and ~1.88 V (B) at all three R_eff.

5. R_eff sweep -- low-frequency probe shows corner attenuation:
   - At 100 Hz, the measured v_amp p-p matches the analytical expectation
        2 * amp * |G| * |H_HP(100 Hz)|
     within 10% relative, for each R_eff and each topology.
     |H_HP(100 Hz)| = 100 / sqrt(100^2 + f_HP^2).
     Expected (amp=0.02 V):
       R_eff=10k (f_HP=159.155 Hz): |H_HP|=0.532
         Case A p-p ~= 2 * 0.02 * 48 * 0.532 = 1.021 V
         Case B p-p ~= 2 * 0.02 * 47 * 0.532 = 1.000 V
       R_eff=100k (f_HP=15.9155 Hz): |H_HP|=0.988
         Case A p-p ~= 2 * 0.02 * 48 * 0.988 = 1.897 V
         Case B p-p ~= 2 * 0.02 * 47 * 0.988 = 1.857 V
       R_eff=1M (f_HP=1.59155 Hz): |H_HP|=0.99987
         Case A p-p ~= 2 * 0.02 * 48 * 0.99987 = 1.920 V
         Case B p-p ~= 2 * 0.02 * 47 * 0.99987 = 1.880 V

All tests use only Python stdlib (unittest, math, random).
"""

import math
import unittest

from afe_compare import (
    C1, F_LP, F_NYQUIST, F_S, G_NON_INV, G_INV, GAIN_DOC, R2, R3, R6, R_BIAS,
    V_REF, apply_amp, biquad_hp_bilinear, biquad_lp_bilinear,
    run_pipeline, src_sine, sweep_r_eff, DEFAULT_SWEEP_R_EFF,
)


def pearson(xs, ys):
    n = len(xs)
    if n != len(ys) or n < 2:
        raise ValueError("need equal-length sequences of length >= 2")
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = sum((x - mx) ** 2 for x in xs)
    sy = sum((y - my) ** 2 for y in ys)
    denom = math.sqrt(sx * sy)
    if denom == 0:
        raise ValueError("zero variance")
    return sxy / denom

def ptp(xs): return max(xs) - min(xs)
def mean(xs): return sum(xs) / len(xs)


# --------------------------------------------------------------------------- #
# 1. Topology A equation and sign
# --------------------------------------------------------------------------- #

class TopologyA(unittest.TestCase):
    """Case A: Vout = Vref + 48 * Vin (non-inverting, sign +)."""

    N = 50000
    AMP = 0.02
    F_IN = 1000.0
    SLICE = slice(40000, 50000)

    def test_gain_value(self):
        self.assertAlmostEqual(G_NON_INV, 1.0 + R3 / R2, places=9)
        self.assertAlmostEqual(G_NON_INV, 48.0, places=9)

    def test_equation_mean_and_pp(self):
        x = src_sine(self.N, self.AMP, self.F_IN, F_S)
        res = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3, "non-inverting")
        amp_v = res["v_amp"]
        ss = self.SLICE
        self.assertAlmostEqual(mean(amp_v[ss]), V_REF, places=2,
                               msg=f"A mean {mean(amp_v[ss]):.4f} != V_REF {V_REF}")
        expected_pp = 2.0 * self.AMP * G_NON_INV  # 1.92
        rel = abs(ptp(amp_v[ss]) - expected_pp) / expected_pp
        self.assertLessEqual(rel, 0.05,
                             f"A p-p {ptp(amp_v[ss]):.4f} vs {expected_pp:.4f}")

    def test_sign_positive_correlation(self):
        x = src_sine(self.N, self.AMP, self.F_IN, F_S)
        res = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3, "non-inverting")
        ss = self.SLICE
        corr = pearson(res["v_hp"][ss], res["v_amp"][ss])
        self.assertGreater(corr, 0.99,
                           f"A Pearson(v_hp, v_amp) = {corr:.4f} not > 0.99")

    def test_sign_argmax_coincides(self):
        # argmax(v_amp) and argmax(v_hp) should be at the same index (modulo LP
        # phase shift). The LP at 1 kHz has near-zero phase shift, so they
        # coincide within a few samples.
        x = src_sine(self.N, self.AMP, self.F_IN, F_S)
        res = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3, "non-inverting")
        ss_start = self.SLICE.start
        ss_stop = self.SLICE.stop
        i_hp_max = max(range(ss_start, ss_stop),
                       key=lambda i: res["v_hp"][i])
        i_amp_max = max(range(ss_start, ss_stop),
                        key=lambda i: res["v_amp"][i])
        # 1 kHz @ 500 kS/s = 500 samples/period; LP phase shift < 1 sample.
        self.assertLessEqual(abs(i_hp_max - i_amp_max), 5,
                             f"A argmax mismatch: v_hp@{i_hp_max}, v_amp@{i_amp_max}")


# --------------------------------------------------------------------------- #
# 2. Topology B equation and sign
# --------------------------------------------------------------------------- #

class TopologyB(unittest.TestCase):
    """Case B: Vout = Vref - 47 * Vin (inverting, sign -)."""

    N = 50000
    AMP = 0.02
    F_IN = 1000.0
    SLICE = slice(40000, 50000)

    def test_gain_value(self):
        self.assertAlmostEqual(G_INV, R3 / R2, places=9)
        self.assertAlmostEqual(G_INV, 47.0, places=9)
        # Matches the project-notes formula G = R3/R2
        self.assertAlmostEqual(G_INV, GAIN_DOC, places=9)

    def test_equation_mean_and_pp(self):
        x = src_sine(self.N, self.AMP, self.F_IN, F_S)
        res = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3, "inverting")
        amp_v = res["v_amp"]
        ss = self.SLICE
        self.assertAlmostEqual(mean(amp_v[ss]), V_REF, places=2,
                               msg=f"B mean {mean(amp_v[ss]):.4f} != V_REF {V_REF}")
        expected_pp = 2.0 * self.AMP * G_INV  # 1.88
        rel = abs(ptp(amp_v[ss]) - expected_pp) / expected_pp
        self.assertLessEqual(rel, 0.05,
                             f"B p-p {ptp(amp_v[ss]):.4f} vs {expected_pp:.4f}")

    def test_sign_negative_correlation(self):
        x = src_sine(self.N, self.AMP, self.F_IN, F_S)
        res = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3, "inverting")
        ss = self.SLICE
        corr = pearson(res["v_hp"][ss], res["v_amp"][ss])
        self.assertLess(corr, -0.99,
                        f"B Pearson(v_hp, v_amp) = {corr:.4f} not < -0.99")

    def test_sign_argmax_inverts(self):
        # argmax(v_amp) and argmin(v_hp) should be at the same index (modulo LP
        # phase shift).
        x = src_sine(self.N, self.AMP, self.F_IN, F_S)
        res = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3, "inverting")
        ss_start = self.SLICE.start
        ss_stop = self.SLICE.stop
        i_hp_min = min(range(ss_start, ss_stop),
                       key=lambda i: res["v_hp"][i])
        i_amp_max = max(range(ss_start, ss_stop),
                        key=lambda i: res["v_amp"][i])
        self.assertLessEqual(abs(i_hp_min - i_amp_max), 5,
                             f"B argmax(v_amp)={i_amp_max} != argmin(v_hp)={i_hp_min}")


# --------------------------------------------------------------------------- #
# 3. R_eff sweep -- corner frequencies match analytical
# --------------------------------------------------------------------------- #

class SweepCornerFrequencies(unittest.TestCase):

    def test_corner_frequencies_match_analytical(self):
        x = src_sine(5000, 0.02, 100.0, F_S)
        for r_eff in DEFAULT_SWEEP_R_EFF:
            expected = 1.0 / (2.0 * math.pi * r_eff * C1)
            for topo in ("non-inverting", "inverting"):
                res = run_pipeline(x, F_S, r_eff, 0.0, 3.3, topo)
                rel = abs(res["f_hp"] - expected) / expected
                self.assertLessEqual(rel, 1e-3,
                                     f"r_eff={r_eff} topo={topo}: "
                                     f"f_hp={res['f_hp']:.4f} vs expected "
                                     f"{expected:.4f} (rel {rel:.4e})")


# --------------------------------------------------------------------------- #
# 4. R_eff sweep -- high-frequency reference is sweep-invariant
# --------------------------------------------------------------------------- #

class SweepHighFreqInvariant(unittest.TestCase):

    def test_10kHz_pp_invariant_across_r_eff(self):
        # 10 kHz is 63x above the highest corner (159 Hz); |H_HP| > 0.9998 for
        # all three R_eff, so the output p-p should be essentially identical.
        N = 50000
        x = src_sine(N, 0.02, 10_000.0, F_S)
        ss = slice(N // 5, None)
        results = {}
        for r_eff in DEFAULT_SWEEP_R_EFF:
            for topo in ("non-inverting", "inverting"):
                res = run_pipeline(x, F_S, r_eff, 0.0, 3.3, topo)
                results[(r_eff, topo)] = ptp(res["v_amp"][ss])
        # Compare each topology across the three R_eff values.
        for topo in ("non-inverting", "inverting"):
            pps = [results[(r, topo)] for r in DEFAULT_SWEEP_R_EFF]
            ref = pps[1]  # use the middle (100k) as reference
            for pp in pps:
                rel = abs(pp - ref) / ref
                self.assertLessEqual(rel, 0.01,
                                     f"topo={topo}: p-p {pp:.6f} deviates from "
                                     f"ref {ref:.6f} by rel {rel:.4e}")


# --------------------------------------------------------------------------- #
# 5. R_eff sweep -- low-frequency probe shows corner attenuation
# --------------------------------------------------------------------------- #

class SweepLowFreqAttenuation(unittest.TestCase):

    def test_100Hz_pp_matches_analytical_attenuation(self):
        N = 50000
        amp = 0.02
        f_probe = 100.0
        x = src_sine(N, amp, f_probe, F_S)
        ss = slice(N // 5, None)
        for r_eff in DEFAULT_SWEEP_R_EFF:
            f_hp = 1.0 / (2.0 * math.pi * r_eff * C1)
            h_hp_mag = f_probe / math.sqrt(f_probe * f_probe + f_hp * f_hp)
            for topo, g in (("non-inverting", G_NON_INV),
                            ("inverting", G_INV)):
                res = run_pipeline(x, F_S, r_eff, 0.0, 3.3, topo)
                measured = ptp(res["v_amp"][ss])
                expected = 2.0 * amp * g * h_hp_mag
                rel = abs(measured - expected) / expected
                self.assertLessEqual(rel, 0.10,
                                     f"r_eff={r_eff} topo={topo}: measured "
                                     f"{measured:.4f} vs expected {expected:.4f} "
                                     f"(rel {rel:.4e})")


if __name__ == "__main__":
    unittest.main(verbosity=2)
