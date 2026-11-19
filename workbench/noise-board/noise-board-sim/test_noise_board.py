#!/usr/bin/env python3
"""
test_noise_board.py -- Automated tests for noise_board.py.

CLASSICAL SIMULATION ONLY.
These tests verify properties of a pseudorandom software simulation. They do
not establish hardware equivalence, quantum entropy, physical fidelity, or any
experimental result. They are not connected to 004c or any other repository.

===============================================================================
TEST CRITERIA (stated before running)
===============================================================================

1. Same-seed repeatability (strict equality, no tolerance):
   For each source {white, telegraph, burst}, two independent
   `random.Random(seed)` instances must produce byte-identical sample
   sequences of length 500 when given the same parameters.

2. Basic mean/variance behavior (N = 20,000, seed = 42):
   - white (mu=1.0, sigma=2.0):
       |sample_mean - 1.0| <= 0.05
       |sample_std  - 2.0| <= 0.10
   - telegraph (amplitude=1.0, switch_prob=0.5):
       every sample is exactly in {-1.0, +1.0}
       |sample_mean| <= 0.05
       0.9 <= sample_variance <= 1.1     # Var(+/-A) = A^2 = 1
   - burst (p_burst=0.05, burst_len=10, burst_sigma=2.0):
       fraction of strictly-zero samples >= 0.40
       at least one strictly-non-zero sample
       mean of the non-zero samples within [-0.5, 0.5]

3. Two-channel correlation direction (N = 20,000, seed = 42):
   For each source {white, telegraph, burst}, generate two-channel pairs at
   rho in {-0.5, 0.0, +0.5}. Let c(r) = sample Pearson(X, Y) at parameter r.
   Direction assertion (strict):
       c(-0.5) < c(0.0) < c(+0.5)
   Loose magnitude band (sanity, not required for direction pass):
       |c(0.0)|              <= 0.10
       |c(+0.5) - 0.5|       <= 0.10
       |c(-0.5) - (-0.5)|    <= 0.15
   The negative side is slightly looser because finite-sample variance is
   asymmetric for extreme rho on bounded/long-tailed sources.

===============================================================================
"""

import math
import random
import statistics
import unittest

from noise_board import (
    generate_burst,
    generate_channel_pair,
    generate_telegraph,
    generate_white,
    mix_two_channel,
    _generate_source,
)


def pearson(xs, ys):
    n = len(xs)
    if n != len(ys) or n < 2:
        raise ValueError("need equal-length sequences of length >= 2")
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    sxy = 0.0
    sx = 0.0
    sy = 0.0
    for x, y in zip(xs, ys):
        dx = x - mx
        dy = y - my
        sxy += dx * dy
        sx += dx * dx
        sy += dy * dy
    denom = math.sqrt(sx * sy)
    if denom == 0.0:
        raise ValueError("zero variance in one channel; Pearson undefined")
    return sxy / denom


# --------------------------------------------------------------------------- #
# 1. Same-seed repeatability
# --------------------------------------------------------------------------- #

class SameSeedRepeatability(unittest.TestCase):
    """Two RNGs with the same seed and same source params must match exactly."""

    def _check_pair(self, source, params, n=500, seed=12345):
        rng_a = random.Random(seed)
        a = _generate_source(rng_a, source, n, params)
        rng_b = random.Random(seed)
        b = _generate_source(rng_b, source, n, params)
        self.assertEqual(a, b,
                         f"same-seed {source}: sequences differ (lengths "
                         f"{len(a)} vs {len(b)})")

    def test_white(self):
        self._check_pair("white", {"mu": 0.5, "sigma": 1.5})

    def test_telegraph(self):
        self._check_pair("telegraph", {"amplitude": 2.0, "switch_prob": 0.1})

    def test_burst(self):
        self._check_pair("burst",
                         {"p_burst": 0.05, "burst_len": 8,
                          "burst_sigma": 1.5, "quiescent": 0.0})

    def test_two_channel_pair_repeatability(self):
        """The (X, Y) pair from generate_channel_pair must be reproducible."""
        params = {"mu": 0.0, "sigma": 1.0}
        x1, y1 = generate_channel_pair(seed=7, source="white", n=300,
                                       params=params, rho=0.3)
        x2, y2 = generate_channel_pair(seed=7, source="white", n=300,
                                       params=params, rho=0.3)
        self.assertEqual(x1, x2, "channel X not reproducible")
        self.assertEqual(y1, y2, "channel Y not reproducible")


# --------------------------------------------------------------------------- #
# 2. Basic mean/variance behavior
# --------------------------------------------------------------------------- #

class WhiteMeanVariance(unittest.TestCase):
    """white: mean ~ mu, std ~ sigma."""

    def test_white_mean_and_std(self):
        n = 20000
        seed = 42
        mu, sigma = 1.0, 2.0
        rng = random.Random(seed)
        samples = generate_white(rng, n, mu, sigma)
        m = statistics.fmean(samples)
        s = statistics.pstdev(samples)  # population std
        self.assertLessEqual(abs(m - mu), 0.05,
                             f"white mean {m:.4f} outside |delta|<=0.05 of {mu}")
        self.assertLessEqual(abs(s - sigma), 0.10,
                             f"white std {s:.4f} outside |delta|<=0.10 of {sigma}")


class TelegraphBasic(unittest.TestCase):
    """telegraph: samples in {-A, +A}, mean ~ 0, variance ~ A^2."""

    def test_telegraph_states_mean_variance(self):
        n = 20000
        seed = 42
        amp = 1.0
        rng = random.Random(seed)
        samples = generate_telegraph(rng, n, amplitude=amp, switch_prob=0.5)
        # Every sample must be exactly +amp or -amp
        for v in samples:
            self.assertIn(v, (amp, -amp),
                          f"telegraph produced value {v!r} not in {{-A, +A}}")
        m = statistics.fmean(samples)
        var = statistics.pvariance(samples)
        self.assertLessEqual(abs(m), 0.05,
                             f"telegraph mean {m:.4f} outside |mean|<=0.05")
        self.assertGreaterEqual(var, 0.9 * amp * amp,
                                f"telegraph variance {var:.4f} below 0.9*A^2")
        self.assertLessEqual(var, 1.1 * amp * amp,
                             f"telegraph variance {var:.4f} above 1.1*A^2")


class BurstBasic(unittest.TestCase):
    """burst: mostly quiescent, some non-zero bursts centered near 0."""

    def test_burst_sparsity_and_nonzero(self):
        n = 20000
        seed = 42
        rng = random.Random(seed)
        samples = generate_burst(rng, n, p_burst=0.05, burst_len=10,
                                 burst_sigma=2.0)
        zeros = sum(1 for v in samples if v == 0.0)
        nonzeros = [v for v in samples if v != 0.0]
        frac_zero = zeros / n
        self.assertGreaterEqual(frac_zero, 0.40,
                                f"burst zero-fraction {frac_zero:.3f} below 0.40")
        self.assertGreater(len(nonzeros), 0,
                           "burst produced no non-zero samples")
        nz_mean = statistics.fmean(nonzeros)
        self.assertLessEqual(abs(nz_mean), 0.5,
                             f"burst non-zero mean {nz_mean:.4f} outside "
                             f"|mean|<=0.5")


# --------------------------------------------------------------------------- #
# 3. Two-channel correlation direction
# --------------------------------------------------------------------------- #

class TwoChannelCorrelationDirection(unittest.TestCase):
    """For each source, c(-0.5) < c(0.0) < c(+0.5). Direction only."""

    N = 20000
    SEED = 42
    RHOS = (-0.5, 0.0, 0.5)
    # Loose magnitude bands (sanity, not required for direction pass)
    BAND = {0.0: 0.10, 0.5: 0.10, -0.5: 0.15}

    def _corrs(self, source, params):
        out = {}
        for r in self.RHOS:
            x, y = generate_channel_pair(seed=self.SEED, source=source,
                                         n=self.N, params=params, rho=r)
            out[r] = pearson(x, y)
        return out

    def _assert_direction(self, source, c):
        self.assertLess(c[-0.5], c[0.0],
                        f"{source}: c(-0.5)={c[-0.5]:.4f} not < c(0.0)={c[0.0]:.4f}")
        self.assertLess(c[0.0], c[0.5],
                        f"{source}: c(0.0)={c[0.0]:.4f} not < c(+0.5)={c[0.5]:.4f}")

    def _assert_band(self, source, c):
        for r in self.RHOS:
            delta = abs(c[r] - r)
            self.assertLessEqual(delta, self.BAND[r],
                                 f"{source}: |c({r}) - {r}| = {delta:.4f} "
                                 f"exceeds band {self.BAND[r]}")

    def test_white(self):
        params = {"mu": 0.0, "sigma": 1.0}
        c = self._corrs("white", params)
        self._assert_direction("white", c)
        self._assert_band("white", c)

    def test_telegraph(self):
        params = {"amplitude": 1.0, "switch_prob": 0.1}
        c = self._corrs("telegraph", params)
        self._assert_direction("telegraph", c)
        # Telegraph marginals are distorted by linear mixing, so the band
        # check is informational here too; direction is the hard requirement.
        self._assert_band("telegraph", c)

    def test_burst(self):
        params = {"p_burst": 0.05, "burst_len": 10, "burst_sigma": 2.0,
                  "quiescent": 0.0}
        c = self._corrs("burst", params)
        self._assert_direction("burst", c)
        self._assert_band("burst", c)


if __name__ == "__main__":
    unittest.main(verbosity=2)
