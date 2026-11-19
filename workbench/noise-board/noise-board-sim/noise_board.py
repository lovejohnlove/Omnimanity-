#!/usr/bin/env python3
"""
noise_board.py -- Classical pseudorandom noise board simulator.

DISCLAIMER: This is a pseudorandom software simulation only.
- It is NOT a hardware noise generator.
- It is NOT a source of quantum entropy.
- It is NOT a calibrated model of any physical device.
- It is NOT cryptographically secure.
- It has no connection to any experiment, prior repository, or external
  dataset. Outputs are synthetic floating-point samples.

All randomness comes from Python's `random.Random` (Mersenne Twister PRNG)
seeded with a user-supplied integer. Two runs with the same seed and the same
parameters produce byte-identical output.

Sources:
  white      -- iid Gaussian samples, mean=mu, sigma=sigma
  telegraph  -- random-telegraph noise: two-state Markov over +/-amplitude,
                per-step flip probability switch_prob
  burst      -- mostly quiescent (0); with prob p_burst per quiescent step,
                emits burst_len Gaussian(0, burst_sigma) samples

Two-channel mode (--two-channel):
  Y1 = X
  Y2 = rho * X + sqrt(1 - rho^2) * Z   (Z is an independent draw from the
                                        same source, drawn from the same RNG)
  Pearson(Y1, Y2) = rho in expectation.
  For `white`, Y2 has the same Gaussian marginal as X.
  For `telegraph` and `burst`, Y2's marginal is a linear mixture and is NOT
  identical to the source marginal. See DESIGN_NOTE.md.

Standard library only. No network. No third-party packages. No hardware.
"""

import argparse
import csv
import math
import random
import sys
from typing import Dict, List, Optional, Tuple


# --------------------------------------------------------------------------- #
# Source generators
# --------------------------------------------------------------------------- #

def generate_white(rng: random.Random, n: int, mu: float, sigma: float) -> List[float]:
    """White noise: n iid Gaussian(mu, sigma) samples."""
    if n < 0:
        raise ValueError(f"n must be >= 0; got {n}")
    if sigma < 0:
        raise ValueError(f"sigma must be >= 0; got {sigma}")
    return [rng.gauss(mu, sigma) for _ in range(n)]


def generate_telegraph(rng: random.Random, n: int, amplitude: float,
                       switch_prob: float) -> List[float]:
    """Random-telegraph noise: two-state Markov over {+amplitude, -amplitude}.

    At each step the state flips with probability `switch_prob`; otherwise it
    persists. The initial state is drawn uniformly from the two states.
    """
    if n < 0:
        raise ValueError(f"n must be >= 0; got {n}")
    if not (0.0 <= switch_prob <= 1.0):
        raise ValueError(f"switch_prob must be in [0,1]; got {switch_prob}")
    if n == 0:
        return []
    state = amplitude if rng.random() < 0.5 else -amplitude
    out: List[float] = []
    for _ in range(n):
        if rng.random() < switch_prob:
            state = -state
        out.append(state)
    return out


def generate_burst(rng: random.Random, n: int, p_burst: float, burst_len: int,
                   burst_sigma: float, quiescent_value: float = 0.0) -> List[float]:
    """Occasional burst noise.

    Output starts quiescent (quiescent_value). At each quiescent step a burst
    is triggered with probability `p_burst`. A triggered burst emits
    `burst_len` consecutive Gaussian(0, burst_sigma) samples (overwriting any
    quiescent values), then advances past the burst. Bursts do not stack; the
    last burst is truncated at index n-1 if it would overrun.
    """
    if n < 0:
        raise ValueError(f"n must be >= 0; got {n}")
    if not (0.0 <= p_burst <= 1.0):
        raise ValueError(f"p_burst must be in [0,1]; got {p_burst}")
    if burst_len < 1:
        raise ValueError(f"burst_len must be >= 1; got {burst_len}")
    if burst_sigma < 0:
        raise ValueError(f"burst_sigma must be >= 0; got {burst_sigma}")
    out = [quiescent_value] * n
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


# --------------------------------------------------------------------------- #
# Two-channel mixing
# --------------------------------------------------------------------------- #

def mix_two_channel(x: List[float], z: List[float], rho: float) -> List[float]:
    """Linear mixing: Y = rho*X + sqrt(1 - rho^2)*Z.

    Preserves Pearson(X, Y) = rho in expectation for any source distribution
    with finite variance. Marginal of Y matches X only for Gaussian X.
    """
    if not (-1.0 <= rho <= 1.0):
        raise ValueError(f"rho must be in [-1,1]; got {rho}")
    if len(x) != len(z):
        raise ValueError(f"x and z must have equal length; got {len(x)} vs {len(z)}")
    factor = math.sqrt(1.0 - rho * rho)
    return [rho * xi + factor * zi for xi, zi in zip(x, z)]


def generate_channel_pair(seed: int, source: str, n: int, params: dict,
                          rho: float) -> Tuple[List[float], List[float]]:
    """Generate (X, Y) with target Pearson correlation rho.

    Both X and Z are drawn from a single `random.Random(seed)` in fixed order
    (X first, then Z), so the pair is reproducible from one seed. Y is then
    formed by linear mixing.
    """
    rng = random.Random(seed)
    x = _generate_source(rng, source, n, params)
    z = _generate_source(rng, source, n, params)
    y = mix_two_channel(x, z, rho)
    return x, y


# --------------------------------------------------------------------------- #
# Dispatch
# --------------------------------------------------------------------------- #

def _generate_source(rng: random.Random, source: str, n: int,
                     params: dict) -> List[float]:
    if source == "white":
        return generate_white(rng, n, params["mu"], params["sigma"])
    if source == "telegraph":
        return generate_telegraph(rng, n, params["amplitude"],
                                  params["switch_prob"])
    if source == "burst":
        return generate_burst(rng, n, params["p_burst"], params["burst_len"],
                              params["burst_sigma"],
                              params.get("quiescent", 0.0))
    raise ValueError(f"unknown source: {source!r}")


def _source_params_from_args(args) -> Dict[str, float]:
    if args.source == "white":
        if args.sigma < 0:
            raise SystemExit(f"--sigma must be >= 0; got {args.sigma}")
        return {"mu": args.mu, "sigma": args.sigma}
    if args.source == "telegraph":
        if not (0.0 <= args.switch_prob <= 1.0):
            raise SystemExit(f"--switch-prob must be in [0,1]; got {args.switch_prob}")
        return {"amplitude": args.amplitude, "switch_prob": args.switch_prob}
    if args.source == "burst":
        if not (0.0 <= args.p_burst <= 1.0):
            raise SystemExit(f"--p-burst must be in [0,1]; got {args.p_burst}")
        if args.burst_len < 1:
            raise SystemExit(f"--burst-len must be >= 1; got {args.burst_len}")
        if args.burst_sigma < 0:
            raise SystemExit(f"--burst-sigma must be >= 0; got {args.burst_sigma}")
        return {"p_burst": args.p_burst, "burst_len": args.burst_len,
                "burst_sigma": args.burst_sigma, "quiescent": 0.0}
    raise SystemExit(f"unknown --source: {args.source!r}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="noise_board",
        description=("Classical pseudorandom noise board simulator "
                     "(Python stdlib only). WARNING: pseudorandom simulation; "
                     "NOT hardware, NOT quantum, NOT cryptographically secure."),
        epilog=("This simulator produces synthetic samples only. It is not a "
                "hardware noise generator, not a quantum-entropy source, and "
                "not a calibrated model of any physical device."),
    )
    p.add_argument("--seed", type=int, required=True,
                   help="Integer seed for random.Random (reproducible).")
    p.add_argument("--source", choices=["white", "telegraph", "burst"],
                   required=True, help="Noise source type.")
    p.add_argument("--samples", type=int, default=1000,
                   help="Samples per channel (default 1000).")
    p.add_argument("--two-channel", action="store_true",
                   help="Emit two channels with target correlation --correlation.")
    p.add_argument("--correlation", type=float, default=0.0,
                   help="Target Pearson correlation in [-1,1] (default 0.0).")
    # Source params
    p.add_argument("--mu", type=float, default=0.0, help="white: mean (default 0).")
    p.add_argument("--sigma", type=float, default=1.0, help="white: std dev (default 1).")
    p.add_argument("--amplitude", type=float, default=1.0,
                   help="telegraph: amplitude A (default 1; state is +/-A).")
    p.add_argument("--switch-prob", type=float, default=0.05,
                   help="telegraph: per-step flip probability in [0,1] (default 0.05).")
    p.add_argument("--p-burst", type=float, default=0.02,
                   help="burst: per-step trigger probability (default 0.02).")
    p.add_argument("--burst-len", type=int, default=10,
                   help="burst: samples per burst (default 10).")
    p.add_argument("--burst-sigma", type=float, default=2.0,
                   help="burst: Gaussian std dev of burst samples (default 2.0).")
    p.add_argument("--format", choices=["csv", "plain"], default="csv",
                   help="Output format (default csv).")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.samples < 0:
        raise SystemExit(f"--samples must be >= 0; got {args.samples}")
    params = _source_params_from_args(args)

    if args.two_channel:
        if not (-1.0 <= args.correlation <= 1.0):
            raise SystemExit(f"--correlation must be in [-1,1]; got {args.correlation}")
        x, y = generate_channel_pair(args.seed, args.source, args.samples,
                                    params, args.correlation)
        rows = [(i, x_i, y_i) for i, (x_i, y_i) in enumerate(zip(x, y))]
        header = ("index", "channel_1", "channel_2")
    else:
        rng = random.Random(args.seed)
        x = _generate_source(rng, args.source, args.samples, params)
        rows = [(i, x_i) for i, x_i in enumerate(x)]
        header = ("index", "sample")

    if args.format == "csv":
        w = csv.writer(sys.stdout)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    else:
        sys.stdout.write("# " + " ".join(header) + "\n")
        for r in rows:
            sys.stdout.write(" ".join(repr(v) for v in r) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
