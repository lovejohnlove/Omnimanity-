# Noise Board Workbench

This workbench collects three **classical synthetic software models** of
noise-board-related signal paths, recovered from prior conversation history
and verified by SHA-256 hash against the values recorded in that history.

## What these are

- **Classical pseudorandom software simulations** built with Python's
  standard library only.
- **Synthetic numeric models** of noise sources and analog front-end signal
  paths.
- Each project is self-contained in its own subfolder with its own design
  note, runnable script, automated tests, and README.

## What these are NOT

- **NOT quantum-noise results.** All randomness is Mersenne Twister PRNG,
  deterministic given the seed. No quantum entropy is modeled or claimed.
- **NOT physically validated board behavior.** No model here has been
  calibrated against, or validated on, any physical hardware board.
- **Unrelated to 004c.** These models have no connection to any 004c
  experiment, repository, or result.
- **NOT connected to any other repository or experiment** including Double
  Alpha, Time Loom, or CUP experimental data.
- **NOT published to or connected with GitHub** beyond this workbench
  location.

## License

**No license has been assigned to this workbench.** The presence of this
workbench in the `lovejohnlove/Omnimanity-` repository does **not** imply
that the repository's story license (if any) applies to these software
models. No rights are granted or claimed. Do not copy, modify, or
redistribute these files without first obtaining explicit authorization
from the repository owner.

## Recovered projects

All files below were recovered from actual source text in the conversation
history that produced them, and verified by SHA-256 hash. No file was
reconstructed from a hash alone. If a file's hash did not match, it was
left out (see "Missing files" below).

### `noise-board-sim/` — Noise Board Simulator

A standalone classical pseudorandom noise board with three selectable
sources (white, random-telegraph, occasional burst) and an optional
two-channel mode with a configurable correlation parameter.

| File | SHA-256 | Bytes |
|---|---|---:|
| `DESIGN_NOTE.md` | `ace608ab334f4566a075d26c8f606c86c9cc630e345a5d54f9e1c7f7525f22e7` | 5,889 |
| `noise_board.py` | `0d8e67a05cc074b66e7474da0097a3314fb64260fe9837d82bde936b5b4c0ff7` | 11,005 |
| `test_noise_board.py` | `27e84f9c163e3d7123d2288680e8e7d7563518c39f504289124af8c8a7d16c9d` | 9,479 |
| `README.md` | `755a8bea95ec4eb0735cfbfddc5b7ed92d9068012478a5aefa49b4769ca924b5` | 1,951 |

Tests: 10 passed (seeded repeatability, mean/variance, two-channel
correlation direction).

### `noise-board-afe-v2/` — AFE Rev1.1 Idealized Block Model

A classical software block model of the documented CUP Rev1.1
analog-front-end signal path, using only public design-record values plus
explicitly documented assumptions. Single non-inverting topology
(`G = 1 + R3/R2 = 48`; documentation says 47 — flagged, not reconciled).

| File | SHA-256 | Bytes |
|---|---|---:|
| `DESIGN_NOTE.md` | `4da0cd4e5ce1364cc8e563a65f418c336049f547c301c7c0db2c1dd474f6f3ff` | 9,432 |
| `afe_model.py` | `5e96f17f885de69cdc6a2a1a021b93b621475b4c78967171a31945f8787e31d7` | 13,686 |
| `test_afe_model.py` | `a6233085402c15f3ac1226037e5c3713d48c17367c2efe79a2c0a159de107f06` | 12,155 |
| `README.md` | `4e3db83305c7fca8c19999736792649c53ef3a8efa2b9a4782fba4c96b3e9756` | 2,950 |

Tests: 10 passed (seeded repeatability, nominal gain/bias, filtering,
clipping, Nyquist).

### `noise-board-afe-v2-comparison/` — Topology Comparison & R_eff Sweep

A standalone comparison of two **hypothetical** block-model topologies for
the documented CUP Rev1.1 AFE, plus a sweep of the assumed effective
resistance `R_eff`. No topology winner is picked. The two alternatives:

- **A** non-inverting: `Vout = Vref + 48·Vin`
- **B** inverting: `Vout = Vref − 47·Vin` (matches the project-notes formula `G = R3/R2`)

| File | SHA-256 | Bytes |
|---|---|---:|
| `DESIGN_NOTE.md` | `5935cea1bcf28e00e682f8387ba6a30682e14e6d424739582be6287abf1f9ecf` | 8,259 |
| `afe_compare.py` | `b3ad822c621dfbddedb533125907afe06c797f55fb006695b8a44630b02b9609` | 15,103 |
| `test_afe_compare.py` | `98e37cb733300542d3b1109ad07128c0ddb59af48512789f175e7bdc0f1de0bc` | 12,233 |
| `README.md` | `74b06cc96aba839883c8f30d0fec68b75533a86c5c70c00bf0deb0a5f3efb0d0` | 3,942 |

Tests: 11 passed (topology A equation+sign, topology B equation+sign,
sweep corner frequencies, sweep high-freq invariance, sweep low-freq
attenuation).

## Missing files

None. All 12 files across the three projects were recovered with matching
SHA-256 hashes.

## How to run

Each project subfolder is independent. `cd` into a subfolder and run:

```sh
python3 -m unittest test_<module> -v
```

See each project's own `README.md` for CLI usage.

## Sandbox recycling note

The original `/tmp/noise-board-sim/`, `/tmp/noise-board-afe-v2/`, and
`/tmp/noise-board-afe-v2-comparison/` directories were lost when the
sandbox recycled `/tmp` between messages. The files in this workbench were
recovered from actual source text in the conversation history and verified
by SHA-256 hash. No file was reconstructed from a hash alone, and no
rebuilt file is labeled as the original if its hash differs.
