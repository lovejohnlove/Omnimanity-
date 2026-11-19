# AFE Rev1.1 — Topology Comparison & R_eff Sweep

A **standalone classical software comparison** of two **hypothetical** block-model
topologies for the documented CUP Rev1.1 AFE, plus a sweep of the assumed
effective resistance `R_eff` seen by the coupling capacitor `C1`. Python
standard library only.

## What this is and is NOT

- **IS** a comparison of two hypothetical topology alternatives:
  - **A** non-inverting: `Vout = Vref + 48·Vin`
  - **B** inverting: `Vout = Vref − 47·Vin` (matches the project-notes formula `G = R3/R2 = 47`)
- **IS NOT** a determination of which topology is the "real" board. No winner is picked.
- **IS NOT** a circuit-fact statement about the CUP Rev1.1 hardware.
- **IS NOT** a simulation of actual quantum noise.
- **IS NOT** a model of any physical Zener's measured behavior.
- **IS NOT** a tested or fabricated hardware board.
- **IS NOT** fabrication-authorized or physically validated.
- **IS NOT** connected to, derived from, or representative of any Double Alpha
  or 004c experiment.
- **IS NOT** published to or connected with GitHub.

## Why two topologies?

The project notes give `R2 = 1 kΩ`, `R3 = 47 kΩ`, and `G = R3/R2 = 47`. This
formula `G = R3/R2` is the inverting-amplifier gain magnitude. The available
schematic record is text-only and does not establish the complete topology, so
both the non-inverting interpretation (`G = 1 + R3/R2 = 48`) and the inverting
interpretation (`G = R3/R2 = 47`) are modeled as alternatives.

## Files

| File | Purpose |
|---|---|
| `DESIGN_NOTE.md` | Design note, both topologies, R_eff sweep plan, every assumption, limitations. |
| `afe_compare.py` | Runnable simulator (CLI) with `--topology` and `--mode sweep`. |
| `test_afe_compare.py` | Automated tests (criteria stated up-front in the module docstring). |
| `README.md` | This file. |

## Requirements

- Python 3.8+.
- No third-party packages. No network.

## Quick start

```sh
cd /tmp/noise-board-afe-v2-comparison

# Both topologies, per-sample CSV (sine 1 kHz, 5 samples)
python3 afe_compare.py --source sine --freq 1000 --samples 5 --topology both

# Topology A only
python3 afe_compare.py --source sine --freq 1000 --samples 100 \
    --topology non-inverting

# Topology B only
python3 afe_compare.py --source sine --freq 1000 --samples 100 \
    --topology inverting

# R_eff sweep at 100 Hz (shows corner attenuation)
python3 afe_compare.py --mode sweep --sweep-freq 100 --sweep-amp 0.02 \
    --sweep-n 50000 --topology both

# R_eff sweep at 1 kHz (shows sweep-invariance at high freq)
python3 afe_compare.py --mode sweep --sweep-freq 1000 --sweep-amp 0.02 \
    --sweep-n 50000 --topology both
```

## Running the tests

```sh
cd /tmp/noise-board-afe-v2-comparison
python3 -m unittest test_afe_compare -v
```

The test module docstring states every criterion before any test runs.

## Topology selection

- `--topology non-inverting` → Case A only (`Vout = Vref + 48·Vin`).
- `--topology inverting` → Case B only (`Vout = Vref − 47·Vin`).
- `--topology both` → both in one CSV for direct comparison.

## R_eff sweep

`--mode sweep` runs the pipeline at `R_eff ∈ {10 kΩ, 100 kΩ, 1 MΩ}` for the
selected topology (or both). At `--sweep-freq 100` the corner-frequency effect
is visible (the 10 kΩ case shows strong attenuation, the 1 MΩ case shows
near-unity). At `--sweep-freq 1000` all three corners are well below the probe,
so the output p-p is essentially invariant across the sweep.

## Key assumptions (full list in `DESIGN_NOTE.md`)

- A1 `R_eff` for C1 high-pass: schematic does not specify; sweep covers 10 kΩ,
  100 kΩ, 1 MΩ (default 100 kΩ = R_bias as a single-point assumption).
- A2 Rails `V_lo=0 V`, `V_hi=3.3 V` (RP2350 ADC full-scale).
- A3 Synthetic, user-selectable input.
- A4 12-bit ADC.
- A5 Ideal op-amp.
- A9 **Topology unspecified** by the text-only schematic; both A and B are
  hypothetical alternatives; **no winner picked**.
