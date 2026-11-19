# AFE Rev1.1 — Topology Comparison & R_eff Sweep

## What this is

A **standalone classical software comparison** of two explicitly **hypothetical**
block-model topologies for the documented CUP Rev1.1 AFE, plus a sweep of the
**assumed** effective resistance `R_eff` seen by the coupling capacitor `C1`.

## What this is NOT (explicit disclaimers)

- **NOT** a determination of which topology is the "real" board.
- **NOT** a circuit-fact statement about the CUP Rev1.1 hardware.
- **NOT** a simulation of actual quantum noise.
- **NOT** a model of any physical Zener diode's measured noise behavior.
- **NOT** a tested or fabricated hardware board.
- **NOT** fabrication-authorized or physically validated.
- **NOT** connected to, derived from, or representative of any Double Alpha
  or 004c experiment.
- **NOT** published to or connected with GitHub.
- Uses **only** Python's standard library; no network calls, no installs.

## Why two topologies?

The project notes give `R2 = 1 kΩ`, `R3 = 47 kΩ`, and `G = R3/R2 = 47`.
This formula `G = R3/R2` is the **inverting** amplifier gain magnitude
(`Vout = Vref − (R3/R2)·Vin` for a single-supply inverting stage biased at
`Vref`).

However, the **available schematic record is text-only** and does not establish
the complete topology. The previous model (in the now-recycled
`/tmp/noise-board-afe-v2/`) assumed a **non-inverting** stage, which would give
`G = 1 + R3/R2 = 48` and `Vout = Vref + 48·Vin`.

Neither interpretation can be ruled out from the text-only record. Both are
plausible; both are hypothetical; **this project treats them as two model
alternatives, not circuit facts. No winner is picked.**

## The two hypothetical cases (both labeled as alternatives)

| Label | Topology hypothesis | Transfer function | Gain magnitude | Sign |
|---|---|---|---:|---|
| **A** | non-inverting | `Vout = Vref + 48·Vin` | 48 | positive |
| **B** | inverting (matches the stated `G = R3/R2 = 47`) | `Vout = Vref − 47·Vin` | 47 | negative |

`Vin` here is the AC-coupled signal `v_hp` after the C1 high-pass (centered at 0).
`Vref = 1.65 V` is the output bias.

## Public design-record values (unchanged from prior task)

| Symbol | Value |
|---|---|
| D1 | 1N4732A (Zener; noise behavior assumed, not modeled) |
| R_bias | 100 kΩ |
| C1 | 0.1 µF |
| U1 | TLV9062 (ideal op-amp; see assumption A5) |
| R2 | 1 kΩ |
| R3 | 47 kΩ |
| V_ref | 1.65 V |
| R6 | 1 kΩ |
| C3 | 750 pF |
| ADC | RP2350/Pico 2 GP26 (12-bit, modeled) |
| f_s | 500 kS/s |
| Rails | analog rails (clamped; limits are an assumption, see A2) |

## Added assumptions (carried over from prior work + sweep additions)

Every assumption is explicit. **Do not silently treat any of these as schematic facts.**

| # | Assumption | Reason | Value |
|---|---|---|---|
| A1 | Effective resistance for C1's high-pass | The schematic does not specify the resistance seen by C1 (parallel combination of bias-path output impedance, op-amp input impedance, any bias divider — none documented). The previous model used `R_eff = 100 kΩ` as a single assumption; this project **sweeps** `R_eff ∈ {10 kΩ, 100 kΩ, 1 MΩ}` to show sensitivity. | CLI `--r-eff`; sweep values 10 kΩ, 100 kΩ, 1 MΩ. |
| A2 | Analog rails for clamp/ADC | Pico 2 ADC reference and analog supply range not pinned down in the supplied values. | `V_lo = 0 V`, `V_hi = 3.3 V` (RP2350 ADC full-scale). CLI-overridable. |
| A3 | Input-noise distribution | Records explicitly say Zener noise behavior is an assumption. | Synthetic, user-selectable: `white`, `telegraph`, `burst`, `sine`. Defaults arbitrary. |
| A4 | ADC bit depth | RP2350 GP26 documented as 12-bit; effective resolution after noise/INL not modeled. | 12-bit, codes 0…4095. |
| A5 | Op-amp ideal behavior | TLV9062 has finite GBW, slew, bias, noise — none modeled. | Ideal infinite-GBW, zero-noise, zero-bias op-amp. |
| A6 | C1 input DC operating point | Synthetic source has no fixed DC level. | Source mean becomes C1 input DC; high-pass removes it; output referenced to V_ref. |
| A7 | Time discretization | Continuous filters must be discretized. | Bilinear transform at `dt = 1/f_s = 2 µs`. |
| A8 | Sampling instant | ADC aperture / S/H not modeled. | Ideal impulse sampling at `t = k/f_s`. |
| A9 | Topology is unspecified | Text-only schematic does not establish whether the stage is non-inverting or inverting. | Both topologies modeled as alternatives; user-selectable. |
| A10 | Single-stage model | Real boards may have multiple gain stages or buffer stages. | Single gain stage only. |

## Signal-path blocks (same as prior model, with selectable topology)

`synthetic source → C1 high-pass (bilinear, R_eff-sweepable) → [topology A or B] → 1st-order anti-alias low-pass (bilinear, ≈212 kHz) → rail clamp [V_lo, V_hi] → 12-bit ADC at f_s = 500 kS/s`

The only difference from the prior model is the topology selection at the
amplifier stage. Everything else (C1, anti-alias, clamp, ADC) is identical.

## R_eff sweep plan

For each `R_eff ∈ {10 kΩ, 100 kΩ, 1 MΩ}`:
- Analytical HP corner: `f_HP = 1 / (2π · R_eff · C1)`
  - 10 kΩ → 159.15 Hz
  - 100 kΩ → 15.92 Hz
  - 1 MΩ → 1.59 Hz
- Drive a deterministic sine probe (default: `f = 100 Hz, amp = 0.02 V`).
- Measure steady-state `v_amp` peak-to-peak and mean for both topologies.
- Also drive a high-frequency reference (default: `f = 1 kHz, amp = 0.02 V`)
  to confirm the HP corner has no observable effect well above all three
  corners.

Expected behavior:
- At 1 kHz (well above all three corners): `|H_HP| ≈ 1` for all three `R_eff`,
  so `v_amp` p-p is essentially unchanged across the sweep.
- At 100 Hz:
  - `R_eff = 10 kΩ` (`f_c = 159 Hz`): `|H_HP(100 Hz)| = 100/sqrt(100² + 159²) ≈ 0.532`
    → strong attenuation, `v_amp` p-p ≈ `1.92 · 0.532 ≈ 1.02 V` (Case A) or
    `1.88 · 0.532 ≈ 1.00 V` (Case B).
  - `R_eff = 100 kΩ` (`f_c = 15.9 Hz`): `|H_HP(100 Hz)| ≈ 0.988`
    → minimal attenuation.
  - `R_eff = 1 MΩ` (`f_c = 1.59 Hz`): `|H_HP(100 Hz)| ≈ 0.9999`
    → essentially unity.

The sweep is **a model-output sensitivity study**, not a measurement of any
physical board.

## Out of scope (limitations, plainly stated)

- No determination of the actual CUP Rev1.1 topology (no winner).
- No transistor-level or SPICE modeling of TLV9062.
- No modeling of the 1N4732A's avalanche breakdown statistics.
- No PCB layout, parasitics, supply noise, ground bounce, EMI.
- No calibration (records say calibration is unresolved).
- The model has not been validated against any physical board.
- This is not a hardware-performance or quantum-noise claim of any kind.

## What the tests check (stated before running)

(Exact tolerances in `test_afe_compare.py` module docstring.)

1. **Topology A equation and sign** — `Vout = Vref + 48·Vin`:
   - For a 1 kHz sine (amp = 0.02 V), steady-state `v_amp` p-p = `2 · 0.02 · 48 = 1.92 V`
     within 5% relative.
   - Mean = `V_ref = 1.65 V` within 0.01.
   - Sign: at the index where `v_hp` is maximum, `v_amp` is also maximum
     (positive correlation, sample correlation > 0.99).
2. **Topology B equation and sign** — `Vout = Vref − 47·Vin`:
   - For the same 1 kHz sine, steady-state `v_amp` p-p = `2 · 0.02 · 47 = 1.88 V`
     within 5% relative.
   - Mean = `V_ref = 1.65 V` within 0.01.
   - Sign: at the index where `v_hp` is maximum, `v_amp` is minimum
     (negative correlation, sample correlation < −0.99).
3. **R_eff sweep — corner frequencies match analytical**:
   - For each `R_eff ∈ {10 kΩ, 100 kΩ, 1 MΩ}`, the reported `f_HP` matches
     `1/(2π·R_eff·C1)` to within 0.1% relative.
4. **R_eff sweep — high-frequency reference is sweep-invariant**:
   - At 1 kHz, `v_amp` p-p for both topologies varies by less than 1% relative
     across the three `R_eff` values (because `|H_HP(1 kHz)| ≈ 1` for all three).
5. **R_eff sweep — low-frequency probe shows attenuation**:
   - At 100 Hz, the measured `v_amp` p-p matches the analytical expectation
     `2 · amp · |G| · |H_HP(100 Hz)|` within 10% relative for each `R_eff` and
     each topology. The Case B gain magnitude `|G| = 47`; Case A `|G| = 48`.

All tests use only Python stdlib (`unittest`, `math`, `random`).
