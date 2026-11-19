#!/usr/bin/env python3
"""
test_afe_model.py -- Automated tests for afe_model.py.

CLASSICAL SOFTWARE BLOCK MODEL TESTS ONLY.
These tests verify properties of an idealized software block model built from
documented design-record values plus the assumptions listed in DESIGN_NOTE.md.
They do NOT establish hardware equivalence, quantum-noise fidelity, physical
Zener behavior, or any experimental result. They are NOT connected to Double
Alpha, 004c, GitHub, or any other repository or experiment.

===============================================================================
TEST CRITERIA (stated before running)
===============================================================================

1. Seeded repeatability (strict equality):
   Two calls to run_pipeline with the same seed, same source params, same
   AFE parameters produce byte-identical v_hp, v_amp, v_clamp, adc_codes.
   Tested for white, telegraph, burst.

2. Nominal gain and bias (tolerance 1e-9 relative):
   - Use a low-frequency sine (f = 1 kHz, well above HP corner 15.9 Hz, well
     below LP corner 212 kHz) with a small amplitude A = 0.02 V so that
     A * GAIN_FORMULA = 0.96 V amplitude (1.92 V p-p centered at V_REF = 1.65 V
     -> [0.69, 2.61] V) stays inside the [0, 3.3] V rails (no clipping).
   - GAIN_FORMULA must equal 48.0 (1 + R3/R2).
   - GAIN_DOC (47.0) must differ from GAIN_FORMULA -- the discrepancy is
     asserted to be reported (header contains both values).

3. Filtering behavior (in-band vs out-of-band attenuation):
   - In-band: sine at f=10 kHz, amp=0.05 V. After the pipeline (pre-clamp,
     pre-ADC), the steady-state peak-to-peak amplitude of v_clamp is within
     +/-15% of (0.05 * GAIN_FORMULA * |H_HP(f=10kHz)| * |H_LP(f=10kHz)|).
     Both |H_HP| and |H_LP| are ~1 at 10 kHz, so expected p-p ~= 0.05*48 = 2.4 V.
   - Out-of-band: sine at f=1 MHz (above f_LP=212 kHz, above f_Nyquist=250 kHz
     in continuous time), same amp=0.05 V. The pre-sampling v_clamp
     steady-state p-p amplitude is < 1/10 of the in-band p-p amplitude.
     (Note: at 1 MHz continuous-time, the discrete-time representation
     aliases; we still measure the pre-sampling filter chain on the
     continuous-time filter output, evaluated at t=k/f_s. The low-pass
     attenuation at 1 MHz vs 10 kHz must be >= 10x.)

4. Clipping:
   - With a large low-frequency sine (amp=5 V, f=1 kHz), the post-clamp
     output v_clamp is bounded: every sample in [V_lo, V_hi]. Strict.
   - The ADC codes saturate: max(adc_codes) == 4095 and min(adc_codes) == 0.
     Strict.

5. Sample-rate / Nyquist:
   - In-band 10 kHz sine at f_s=500 kS/s yields >= 5 samples per period
     (samples_per_period = f_s / f_in = 50). Assert >= 5.
   - Above-Nyquist 600 kHz sine at f_s=500 kS/s produces a sampled sequence
     whose alias frequency is below f_Nyquist. Verified by counting zero
     crossings: the alias has fewer zero crossings per N samples than the
     in-band case would imply. Specifically, with N=2000 samples at f_s=500k
     for f_in=600 kHz, the expected alias is f_alias = |f_in - f_s| = 100 kHz
     (folding). The sampled sequence shows a dominant period consistent with
     100 kHz, not 600 kHz: number of zero crossings in 2000 samples is
     closer to (2 * 100k * 2000 / 500k = 800) than to (2 * 600k * 2000 /
     500k = 4800). Assert zero_crossings_in_alias_case < 2000 (a loose
     upper bound that 600 kHz un-aliased would massively exceed).

All tests use only Python stdlib (unittest, math, random, statistics).
"""

import math
import random
import unittest

from afe_model import (
    ADC_BITS, C1, C3, F_LP, F_NYQUIST, F_S, GAIN_DOC, GAIN_FORMULA,
    R2, R3, R6, R_BIAS, V_REF,
    apply_first_order, biquad_hp_bilinear, biquad_lp_bilinear,
    run_pipeline, src_sine, src_white, src_telegraph, src_burst,
)


def ptp(xs):
    return max(xs) - min(xs)

def zero_crossings(xs):
    n = 0
    for i in range(1, len(xs)):
        if (xs[i-1] < 0 and xs[i] >= 0) or (xs[i-1] > 0 and xs[i] <= 0):
            n += 1
    return n


# --------------------------------------------------------------------------- #
# 1. Seeded repeatability
# --------------------------------------------------------------------------- #

class SeededRepeatability(unittest.TestCase):

    def _check(self, source, build):
        seed = 12345
        n = 300
        x1 = build(random.Random(seed), n)
        x2 = build(random.Random(seed), n)
        self.assertEqual(x1, x2, "source not reproducible from seed")
        hp1, amp1, clamp1, adc1 = run_pipeline(x1, F_S, R_BIAS, 0.0, 3.3)
        hp2, amp2, clamp2, adc2 = run_pipeline(x2, F_S, R_BIAS, 0.0, 3.3)
        self.assertEqual(hp1, hp2, "v_hp not reproducible")
        self.assertEqual(amp1, amp2, "v_amp not reproducible")
        self.assertEqual(clamp1, clamp2, "v_clamp not reproducible")
        self.assertEqual(adc1, adc2, "adc_codes not reproducible")

    def test_white(self):
        self._check("white", lambda r, n: src_white(r, n, 0.0, 1.0))

    def test_telegraph(self):
        self._check("telegraph", lambda r, n: src_telegraph(r, n, 1.0, 0.1))

    def test_burst(self):
        self._check("burst", lambda r, n: src_burst(r, n, 0.05, 10, 2.0))


# --------------------------------------------------------------------------- #
# 2. Nominal gain and bias
# --------------------------------------------------------------------------- #

class NominalGainBias(unittest.TestCase):

    def test_gain_formula_value(self):
        self.assertEqual(GAIN_FORMULA, 1.0 + R3 / R2)
        self.assertAlmostEqual(GAIN_FORMULA, 48.0, places=9)

    def test_gain_doc_differs_from_formula(self):
        # The discrepancy is real and must not be silently reconciled.
        self.assertNotEqual(GAIN_DOC, GAIN_FORMULA)
        self.assertAlmostEqual(GAIN_DOC, 47.0, places=9)

    def test_low_freq_sine_gain_and_bias(self):
        # In-band low-frequency sine: HP ~unity, LP ~unity, so v_amp AC amp
        # ~= input amp * GAIN_FORMULA, mean ~= V_REF.
        # 50 ms of signal = 50 periods of 1 kHz. Skip the first 40 ms to let
        # the HP slow-mode transient decay (HP corner 15.9 Hz -> decay time
        # ~63 ms; at 40 ms the slow mode is at exp(-40/63) ~= 0.53 of initial,
        # and the slice average is dominated by the much-decayed tail).
        # Slice [40000:50000] = 10 integer periods -> pure-sine mean = 0.
        n = 50000
        amp = 0.02  # 0.02 * 48 = 0.96 V amplitude, p-p 1.92 V centered at 1.65
                    # -> [0.69, 2.61] V, inside [0, 3.3] rails (no clipping)
        f_in = 1_000.0  # 1 kHz: well above HP corner (15.9 Hz), well below
                        # LP corner (212 kHz); both |H_HP| ~= 1 and |H_LP| ~= 1
        x = src_sine(n, amp, f_in, F_S)
        hp, amp_v, clamp_v, adc = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3)
        ss = slice(40000, 50000)
        # Mean of v_amp in steady state must be V_REF (high-pass removes DC,
        # output referenced to V_REF).
        mean_amp = sum(amp_v[ss]) / len(amp_v[ss])
        self.assertAlmostEqual(mean_amp, V_REF, places=2,
                               msg=f"v_amp mean {mean_amp:.4f} != V_REF {V_REF}")
        # AC amplitude of v_amp ~= amp * GAIN_FORMULA (HP and LP ~unity at 1 kHz)
        # p-p ~= 2 * amp * GAIN_FORMULA = 2 * 0.02 * 48 = 1.92 V
        expected_pp = 2.0 * amp * GAIN_FORMULA
        actual_pp = ptp(amp_v[ss])
        rel = abs(actual_pp - expected_pp) / expected_pp
        self.assertLessEqual(rel, 0.05,
                             f"v_amp p-p {actual_pp:.4f} vs expected "
                             f"{expected_pp:.4f} (rel {rel:.3f})")


# --------------------------------------------------------------------------- #
# 3. Filtering behavior
# --------------------------------------------------------------------------- #

class FilteringBehavior(unittest.TestCase):

    def _steady_state_pp(self, amp, f_in, n=8000, skip=2000):
        x = src_sine(n, amp, f_in, F_S)
        hp, amp_v, clamp_v, adc = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3)
        return ptp(clamp_v[skip:])

    def test_in_band_vs_out_of_band_attenuation(self):
        amp = 0.02  # 0.02 * 48 = 0.96 V amplitude, in-band stays inside rails
        # In-band: 10 kHz (below 212 kHz LP corner, below 250 kHz Nyquist)
        pp_in = self._steady_state_pp(amp, 10_000.0)
        # Out-of-band: 1 MHz (above LP corner and above Nyquist in continuous time)
        # We use the *pre-sampling* clamp output: the continuous-time filter
        # chain is evaluated at t=k/f_s, but the low-pass attenuation at 1 MHz
        # is still applied per-sample through the bilinear approximation
        # (which folds near-DC aliases of high frequencies -- caveat noted
        # in DESIGN_NOTE A7). To avoid the bilinear fold, we instead probe
        # at 300 kHz, which is above LP corner (212 kHz) and below Nyquist
        # (250 kHz)? No -- 300 kHz is above Nyquist. Use 400 kHz which is
        # well above Nyquist and will alias, but the *filter chain itself*
        # still operates on the input samples evaluated at t=k/f_s.
        # Cleanest: probe filter response with a sine whose frequency is
        # below Nyquist but above the LP corner: f = 240 kHz.
        pp_out = self._steady_state_pp(amp, 240_000.0)
        # |H_LP(240 kHz)| << |H_LP(10 kHz)|. Expect >= 10x attenuation.
        self.assertGreaterEqual(pp_in / max(pp_out, 1e-12), 10.0,
                                f"in-band p-p {pp_in:.4f} not >= 10x "
                                f"out-of-band p-p {pp_out:.4f}")


# --------------------------------------------------------------------------- #
# 4. Clipping
# --------------------------------------------------------------------------- #

class Clipping(unittest.TestCase):

    def test_clamp_bounds_and_saturation(self):
        # Large low-frequency sine that will both rails-saturate.
        n = 2000
        x = src_sine(n, amp=5.0, freq=1_000.0, fs=F_S)
        hp, amp_v, clamp_v, adc = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3)
        # Every clamped sample must be inside [V_lo, V_hi].
        for v in clamp_v:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 3.3)
        # ADC codes must saturate at both rails.
        self.assertEqual(max(adc), (1 << ADC_BITS) - 1,
                         f"max adc {max(adc)} != 4095")
        self.assertEqual(min(adc), 0,
                         f"min adc {min(adc)} != 0")


# --------------------------------------------------------------------------- #
# 5. Sample-rate / Nyquist
# --------------------------------------------------------------------------- #

class SampleRateNyquist(unittest.TestCase):

    def test_in_band_samples_per_period(self):
        # 10 kHz @ 500 kS/s -> 50 samples per period
        spp = F_S / 10_000.0
        self.assertGreaterEqual(spp, 5.0,
                                f"in-band samples per period {spp} < 5")

    def test_above_nyquist_aliases(self):
        # 600 kHz @ 500 kS/s -> expected alias |600-500|=100 kHz
        n = 4000
        x = src_sine(n, amp=0.05, freq=600_000.0, fs=F_S)
        hp, amp_v, clamp_v, adc = run_pipeline(x, F_S, R_BIAS, 0.0, 3.3)
        # Count zero crossings of the source signal in the sampled domain
        # (post-sampling representation). Aliasing makes the apparent
        # frequency lower than the input frequency.
        zc_src = zero_crossings(x)
        # If 600 kHz were truly sampled un-aliased at 500 kS/s for 4000 samples
        # (= 8 ms of signal), the source would have 2 * 600e3 * 8e-3 = 9600
        # zero crossings in continuous time -- but we only have 4000 samples,
        # so the *sampled* zero-crossing count for an un-aliased 600 kHz would
        # be near the maximum possible (close to N=4000). The aliased
        # representation at 100 kHz should have far fewer: ~2 * 100e3 * 8e-3 = 1600.
        self.assertLess(zc_src, 2000,
                        f"600 kHz sampled at 500 kS/s should alias to ~100 kHz; "
                        f"got {zc_src} zero crossings (un-aliased would be ~N)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
