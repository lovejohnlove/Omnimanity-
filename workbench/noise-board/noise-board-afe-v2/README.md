# AFE Rev1.1 Idealized Block Model

A **classical software block model** of the *documented* CUP Rev1.1
analog-front-end signal path, built only from the public design-record values
supplied in the task description, plus the explicitly documented assumptions
in `DESIGN_NOTE.md`. Python standard library only.

## What this is and is NOT

- **IS** an idealized block model (source → C1 high-pass → non-inverting amp →
  1st-order anti-alias low-pass → rail clamp → 12-bit ADC at 500 kS/s).
- **IS NOT** a simulation of actual quantum noise.
- **IS NOT** a model of any physical Zener diode's *measured* noise behavior
  (the records say Zener noise behavior is an assumption; the input source is
  a synthetic, user-selectable knob).
- **IS NOT** a tested or fabricated hardware board.
- **IS NOT** fabrication-authorized or physically validated.
- **IS NOT** connected to, derived from, or representative of any Double Alpha
  or 004c experiment, and is NOT published to or connected with GitHub.

## Files

| File | Purpose |
|---|---|
| `DESIGN_NOTE.md` | Design note, blocks, design-record values, every assumption, limitations. |
| `afe_model.py` | Runnable simulator (CLI). |
| `test_afe_model.py` | Automated tests (criteria stated up-front in the module docstring). |
| `README.md` | This file. |

## Requirements

- Python 3.8+ (uses `statistics.fmean`).
- No third-party packages. No network.

## Quick start

```sh
cd /tmp/noise-board-afe-v2

# White synthetic input, default params, 12-bit ADC codes
python3 afe_model.py --seed 42 --source white --samples 50

# Deterministic sine probe at 10 kHz (in-band)
python3 afe_model.py --source sine --freq 10000 --samples 100 --stage all

# Deterministic sine probe at 600 kHz (above Nyquist; aliasing demo)
python3 afe_model.py --source sine --freq 600000 --samples 200 --stage adc

# Telegraph input
python3 afe_model.py --seed 7 --source telegraph --samples 30 \
    --amplitude 0.1 --switch-prob 0.2

# Burst input
python3 afe_model.py --seed 7 --source burst --samples 200 \
    --p-burst 0.05 --burst-len 10 --burst-sigma 0.2
```

## Running the tests

```sh
cd /tmp/noise-board-afe-v2
python3 -m unittest test_afe_model -v
```

Or directly:

```sh
python3 test_afe_model.py
```

The test module docstring states every criterion before any test runs.

## Key assumptions (full list in `DESIGN_NOTE.md`)

- `R_eff = 100 kΩ` for the C1 high-pass (schematic does not specify; set equal
  to R_bias as an assumption; overridable via `--r-eff`).
- `V_lo = 0 V`, `V_hi = 3.3 V` (RP2350 ADC full-scale; overridable).
- Input noise is synthetic and user-selectable.
- 12-bit ADC, ideal op-amp, ideal impulse sampling, bilinear discretization.

## Flagged discrepancy (not reconciled)

- Documentation says "nominal gain 47".
- Formula `1 + R3/R2 = 1 + 47/1 = 48`.
- Model uses `48` for math; every CSV header carries
  `# documented_gain=47 formula_gain=48 (FLAGGED: see DESIGN_NOTE)`.
