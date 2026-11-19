# Noise Board Simulator — Report

## Status

**Classical synthetic software model.** Not physical validation. Not quantum.
Not 004c. Not connected to any experiment, prior repository, or external
dataset.

## Files (recovered, SHA-256 verified)

| File | SHA-256 | Bytes |
|---|---|---:|
| `DESIGN_NOTE.md` | `ace608ab334f4566a075d26c8f606c86c9cc630e345a5d54f9e1c7f7525f22e7` | 5,889 |
| `noise_board.py` | `0d8e67a05cc074b66e7474da0097a3314fb64260fe9837d82bde936b5b4c0ff7` | 11,005 |
| `test_noise_board.py` | `27e84f9c163e3d7123d2288680e8e7d7563518c39f504289124af8c8a7d16c9d` | 9,479 |
| `README.md` | `755a8bea95ec4eb0735cfbfddc5b7ed92d9068012478a5aefa49b4769ca924b5` | 1,951 |

## Test results

**10 tests passed** (0.201s), exit code 0.

```
test_burst_sparsity_and_nonzero (BurstBasic) ... ok
test_burst (SameSeedRepeatability) ... ok
test_telegraph (SameSeedRepeatability) ... ok
test_two_channel_pair_repeatability (SameSeedRepeatability) ... ok
test_white (SameSeedRepeatability) ... ok
test_telegraph_states_mean_variance (TelegraphBasic) ... ok
test_burst (TwoChannelCorrelationDirection) ... ok
test_telegraph (TwoChannelCorrelationDirection) ... ok
test_white (TwoChannelCorrelationDirection) ... ok
test_white_mean_and_std (WhiteMeanVariance) ... ok

Ran 10 tests in 0.201s
OK
```

## Test criteria (stated before running)

1. **Same-seed repeatability** (strict equality): two `random.Random(seed)`
   instances with same params produce identical length-500 sequences.
2. **Mean/variance** (N=20,000, seed=42):
   - white (mu=1, sigma=2): `|mean−1| ≤ 0.05`, `|std−2| ≤ 0.10`
   - telegraph (A=1, switch_prob=0.5): all samples ∈ {−1,+1}; `|mean| ≤ 0.05`;
     `0.9 ≤ var ≤ 1.1`
   - burst (p_burst=0.05, len=10, sigma=2): ≥40% zeros; ≥1 non-zero;
     non-zero `|mean| ≤ 0.5`
3. **Two-channel correlation direction** (N=20,000, seed=42):
   `c(−0.5) < c(0.0) < c(+0.5)` strict; loose band `|c(0)|≤0.10`,
   `|c(+0.5)−0.5|≤0.10`, `|c(−0.5)−(−0.5)|≤0.15`.

## Measured numbers

**CLI repeatability:** two identical `python3 noise_board.py --seed 42 --source
white --samples 5` invocations produced byte-identical CSV output.

**Two-channel correlation** (N=20,000, seed=42):

| source | c(−0.5) | c(0.0) | c(+0.5) | monotonic? |
|---|---:|---:|---:|---|
| white | −0.4957 | 0.0051 | 0.5024 | yes |
| telegraph | −0.5094 | −0.0146 | 0.4905 | yes |
| burst | −0.4902 | 0.0070 | 0.4994 | yes |

All three sources satisfy `c(−0.5) < c(0.0) < c(+0.5)` and fall inside the
loose magnitude band.

## Model description

Three selectable synthetic sources:
- **white** — iid Gaussian(mu, sigma) via `random.Random.gauss`
- **telegraph** — two-state Markov over {+A, −A}, per-step flip prob
- **burst** — quiescent 0; with prob p_burst per step emits burst_len
  Gaussian(0, burst_sigma) samples

Two-channel mode: `Y = rho·X + sqrt(1−rho²)·Z` where X and Z are independent
draws from the same source. Pearson(X, Y) = rho in expectation for all
sources. For non-Gaussian sources, Y's marginal is a linear mixture (not the
source marginal) — documented limitation.

## Assumptions

- PRNG is Mersenne Twister (`random.Random`), deterministic given seed.
- All randomness is classical pseudorandom; **not quantum entropy**.
- Not cryptographically secure.
- Not calibrated against any physical device.

## Limitations

- No spectral shaping (no 1/f, no band-pass); "white" = iid Gaussian.
- No sample-rate or time-unit modeling; CSV index is a sample index.
- No GUI, no real-time streaming; output is a complete CSV to stdout.
- telegraph uses iid per-step flip probability (discrete-time approximation,
  not continuous-time Markov with exponential dwell).
- burst: no stacking; truncated at end of requested length.
- Two-channel telegraph/burst: second-channel marginal distorted by linear
  mixing. Use `white` if both marginals must match the source.
- Not validated against any physical board; no claim of physical fidelity.
