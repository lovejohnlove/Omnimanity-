# Noise Board Workbench — Report

## Status

This workbench collects three **classical synthetic software models** of
noise-board-related signal paths. All are **classical synthetic models**,
**not physical validation**, **not quantum**, and **not 004c**. They are
unrelated to any Double Alpha, Time Loom, or CUP experimental data.

## Recovery summary

All 12 source files across the three projects were recovered from actual
source text in the conversation history that produced them, and verified by
SHA-256 hash. **No file was reconstructed from a hash alone.** Every
recovered file's SHA-256 matches the expected value recorded in the
conversation.

| Project | Files | All hashes match? |
|---|---:|---|
| `noise-board-sim/` | 4 | yes |
| `noise-board-afe-v2/` | 4 | yes |
| `noise-board-afe-v2-comparison/` | 4 | yes |
| **Total** | **12** | **yes** |

**Missing files:** None.

## Test results — all 31 synthetic tests passed

| Project | Tests | Result | Duration |
|---|---:|---|---|
| `noise-board-sim` | 10 | OK | 0.201s |
| `noise-board-afe-v2` | 10 | OK | 0.101s |
| `noise-board-afe-v2-comparison` | 11 | OK | 1.136s |
| **Total** | **31** | **All pass** | — |

Tests were re-run in isolated copies of the recovered source files. No test
code was modified. Test criteria were stated before running in each project's
test module docstring.

## Recovered file hashes

### `noise-board-sim/`

| File | SHA-256 |
|---|---|
| `DESIGN_NOTE.md` | `ace608ab334f4566a075d26c8f606c86c9cc630e345a5d54f9e1c7f7525f22e7` |
| `noise_board.py` | `0d8e67a05cc074b66e7474da0097a3314fb64260fe9837d82bde936b5b4c0ff7` |
| `test_noise_board.py` | `27e84f9c163e3d7123d2288680e8e7d7563518c39f504289124af8c8a7d16c9d` |
| `README.md` | `755a8bea95ec4eb0735cfbfddc5b7ed92d9068012478a5aefa49b4769ca924b5` |

### `noise-board-afe-v2/`

| File | SHA-256 |
|---|---|
| `DESIGN_NOTE.md` | `4da0cd4e5ce1364cc8e563a65f418c336049f547c301c7c0db2c1dd474f6f3ff` |
| `afe_model.py` | `5e96f17f885de69cdc6a2a1a021b93b621475b4c78967171a31945f8787e31d7` |
| `test_afe_model.py` | `a6233085402c15f3ac1226037e5c3713d48c17367c2efe79a2c0a159de107f06` |
| `README.md` | `4e3db83305c7fca8c19999736792649c53ef3a8efa2b9a4782fba4c96b3e9756` |

### `noise-board-afe-v2-comparison/`

| File | SHA-256 |
|---|---|
| `DESIGN_NOTE.md` | `5935cea1bcf28e00e682f8387ba6a30682e14e6d424739582be6287abf1f9ecf` |
| `afe_compare.py` | `b3ad822c621dfbddedb533125907afe06c797f55fb006695b8a44630b02b9609` |
| `test_afe_compare.py` | `98e37cb733300542d3b1109ad07128c0ddb59af48512789f175e7bdc0f1de0bc` |
| `README.md` | `74b06cc96aba839883c8f30d0fec68b75533a86c5c70c00bf0deb0a5f3efb0d0` |

## Model descriptions

### `noise-board-sim/`
Classical pseudorandom noise board with three synthetic sources (white,
telegraph, burst) and optional two-channel mode with configurable Pearson
correlation. Linear mixing: `Y = rho·X + sqrt(1−rho²)·Z`. All randomness is
Mersenne Twister PRNG; **not quantum entropy**.

### `noise-board-afe-v2/`
Idealized block model of the documented CUP Rev1.1 AFE signal path.
Non-inverting topology (`G = 1 + R3/R2 = 48`; documentation says 47 — flagged,
not reconciled). Signal path: source → C1 high-pass → non-inverting amp →
1st-order anti-alias low-pass → rail clamp → 12-bit ADC at 500 kS/s. Synthetic
input only; Zener D1=1N4732A is a labeled placeholder, not a modeled noise
source.

### `noise-board-afe-v2-comparison/`
Comparison of two **hypothetical** topology alternatives (no winner picked):
- **A** non-inverting: `Vout = Vref + 48·Vin`
- **B** inverting: `Vout = Vref − 47·Vin` (matches project-notes `G = R3/R2`)

Plus an R_eff sweep at 10 kΩ / 100 kΩ / 1 MΩ showing corner-frequency
sensitivity (159 Hz / 15.9 Hz / 1.59 Hz).

## Assumptions (summary; full lists in each project's DESIGN_NOTE.md)

- **Classical pseudorandom** — Mersenne Twister PRNG, deterministic given seed.
- **Not quantum entropy** — no quantum RNG modeled or claimed.
- **Synthetic input** — input noise is user-selectable (white/telegraph/burst/sine);
  Zener noise behavior is an assumption, not a calibrated model.
- **Ideal op-amp** — infinite GBW, zero noise, zero bias.
- **R_eff for C1** — schematic does not specify; 100 kΩ default (= R_bias);
  comparison project sweeps 10 kΩ / 100 kΩ / 1 MΩ.
- **Rails** — V_lo=0 V, V_hi=3.3 V (RP2350 ADC full-scale assumption).
- **12-bit ADC** — ideal mid-tread quantization; no INL/DNL.
- **Bilinear discretization** at dt = 2 µs.
- **Topology unspecified** (comparison project only) — both A and B are
  hypothetical; no winner picked.

## Limitations (summary; full lists in each project's DESIGN_NOTE.md)

- **Not physical validation** — no model has been calibrated against or
  validated on any physical hardware board.
- **Not quantum** — all randomness is classical PRNG.
- **Not 004c** — no connection to any 004c experiment, repository, or result.
- No transistor-level or SPICE modeling.
- No Zener avalanche breakdown statistics modeled.
- No PCB layout, parasitics, supply noise, EMI.
- No calibration (records say calibration is unresolved).
- Not cryptographically secure.
- Not fabrication-authorized or physically validated.

## Model-vs-hardware caveat

These are idealized math-of-the-schematic exercises on documented design-record
values plus explicitly documented assumptions. They are **not physical
validation** of any board. The Zener D1=1N4732A appears only as a labeled
block; its avalanche noise statistics are not modeled. The input sources are
synthetic. No result here is a quantum-noise result, a measured-Zener result,
a tested-board result, or a Double Alpha / 004c experimental result.

## License

**No license has been assigned to this workbench.** The presence of this
workbench in the `lovejohnlove/Omnimanity-` repository does **not** imply
that the repository's story license (if any) applies to these software
models. No rights are granted or claimed.

## Sandbox recycling note

The original `/tmp/noise-board-sim/`, `/tmp/noise-board-afe-v2/`, and
`/tmp/noise-board-afe-v2-comparison/` directories were lost when the sandbox
recycled `/tmp` between messages. The files in this workbench were recovered
from actual source text in the conversation history and verified by SHA-256
hash. No file was reconstructed from a hash alone, and no rebuilt file is
labeled as the original if its hash differs.

## Push status

The local commit containing this workbench has **not reached GitHub** as of
this report. The sandbox has no authenticated push route (HTTPS remote, no
SSH keys, no credential helper, no `gh` CLI). The commit exists locally only.
No credentials or tokens were placed in chat or stored in the sandbox.
