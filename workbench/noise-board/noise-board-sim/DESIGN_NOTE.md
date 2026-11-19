# Noise Board Simulator — Design Note

## What this is

A standalone **classical pseudorandom software simulation** of a configurable
"noise board." It produces synthetic numeric samples that resemble three
well-known noise phenomenologies. It is a teaching / sanity-check tool for
streaming-data and statistics work.

## What this is NOT (explicit disclaimers)

- **Not a hardware noise generator.** No DAC, no analog frontend, no physical
  source is modeled. Outputs are floating-point numbers in a CSV file.
- **Not a quantum-entropy source.** All randomness comes from Python's
  `random.Random`, which is the Mersenne Twister PRNG. Its outputs are fully
  deterministic given the seed. It is unsuitable for cryptographic use and is
  not a substitute for a hardware random-number generator or a quantum RNG.
- **Not a calibrated model of any specific device.** The parameters (sigma,
  switch-prob, burst probability, etc.) are user knobs, not measured
  constants of any physical noise process.
- **Not connected to any experiment, prior repository, or external dataset.**
  The simulator is self-contained in `/tmp/noise-board-sim` and makes no
  reference to 004c, Time Loom, CUP, GitHub, or any other artifact.

## Sources

All three sources turn a seeded `random.Random` instance into a stream of
floats. There is no I/O, no threading, no network.

1. **`white`** — iid Gaussian samples, `N(mu, sigma^2)`. Implemented via
   `random.Random.gauss(mu, sigma)` per sample.
2. **`telegraph`** — random-telegraph noise: a two-state Markov chain over
   `+amplitude` and `-amplitude`. At each step the state flips with
   probability `switch_prob`. The initial state is drawn uniformly. The
   autocorrelation decays as `(1 - 2*switch_prob)^k`.
3. **`burst`** — occasional burst noise: quiescent (0) by default. At each
   quiescent step a burst is triggered with probability `p_burst`; a triggered
   burst emits `burst_len` consecutive samples drawn from `N(0, burst_sigma^2)`.
   Bursts do not stack (a new burst cannot start inside an ongoing one in this
   implementation); bursts that would overrun the requested length are
   truncated at the end.

## Two-channel mode

Given a target Pearson correlation `rho in [-1, 1]`:

- Channel 1 = `X` (a draw from the selected source).
- An independent draw `Z` from the same source and same parameters is taken
  from the same seeded RNG, immediately after `X` (so the pair `(X, Z)` is
  reproducible from a single seed).
- Channel 2 = `rho * X + sqrt(1 - rho^2) * Z`.

**Mathematical property.** If `X` and `Z` are independent with the same
finite variance, then `Pearson(X, Y) = rho` in expectation. This holds for
*all three* source types, not just Gaussian.

**Limitation.** Linear mixing preserves the *marginal distribution* of the
second channel only when the source is Gaussian. For `telegraph` and `burst`,
the second channel's marginal is a linear mixture of two source-shaped
variables and is **not** identical to the source marginal. The first channel
is always a clean draw from the source. The Pearson correlation still moves
monotonically with `rho`; only the second channel's histogram is distorted.
This is documented as a limitation and verified in the tests (direction only,
not exact magnitude).

A copula-based alternative that preserves both marginals exactly was
considered and rejected: it complicates the code, requires a normal-inverse-CDF
approximation, and does not change the test conclusion (correlation still
moves with `rho`). Linear mixing keeps the simulator small and the math
auditable.

## Reproducibility

- Every run is reproducible from `(--seed, --source, --samples, --two-channel,
  --correlation, <source params>)`.
- The same parameter set always produces byte-identical CSV output.
- The PRNG state advances deterministically; there is no wall-clock or
  entropy input.

## What the tests check

(Stated up-front, before any test is run. See `test_noise_board.py` for the
exact tolerances.)

1. **Same-seed repeatability** — for each source, two independent
   `random.Random(seed)` instances must produce identical sample sequences.
   Strict equality, no tolerance.
2. **Basic mean/variance behavior** —
   - White: `|mean - mu| <= 0.05`, `|std - sigma| <= 0.10` (N=20,000).
   - Telegraph: every sample in `{-A, +A}`; `|mean| <= 0.05`; variance in
     `[0.9*A^2, 1.1*A^2]` (N=20,000, switch_prob=0.5).
   - Burst: `>= 40%` strictly-zero samples; at least one non-zero sample;
     mean of the non-zero samples within `[-0.5, 0.5]` of 0.
3. **Two-channel correlation direction** — for each source, generate
   two-channel pairs at `rho = -0.5, 0.0, +0.5`. Assert
   `corr(-0.5) < corr(0.0) < corr(+0.5)`. Direction only; exact magnitude is
   not asserted. A loose band is also checked (`|corr(0)| <= 0.10`,
   `|corr(+0.5) - 0.5| <= 0.10`, `|corr(-0.5) - (-0.5)| <= 0.15`).

## Out of scope (limitations, plainly stated)

- No spectral shaping (no 1/f, no band-pass). "White" here means iid
  Gaussian, not band-limited white noise.
- No sample-rate or time-unit modeling. The CSV index is a sample index,
  not a timestamp.
- No GUI, no real-time streaming. Output is a complete CSV written to stdout.
- The PRNG is Mersenne Twister. It is statistically good for simulation but
  **not cryptographically secure** and **not quantum**.
- `telegraph` uses iid per-step flip probability, not a continuous-time
  two-state Markov with exponential dwell. This is a discrete-time
  approximation.
- `burst` overlaps and stacking rules are simplified (no stacking; truncated
  at the end of the requested length).
- Two-channel `telegraph`/`burst` second-channel marginals are distorted as
  noted above. Use `white` if you need both marginals to match the source.
- The simulator has not been calibrated against any physical device and
  produces no claim of physical fidelity.
