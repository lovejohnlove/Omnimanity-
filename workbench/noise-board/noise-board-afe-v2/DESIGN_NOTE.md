# AFE Rev1.1 Idealized Block Model — Design Note

## What this is

A **classical software block model** of the **documented** CUP Rev1.1
analog-front-end signal path, built from the public design-record values
supplied in this task. It is **idealized**: each stage is a first-principles
mathematical block, not a transistor-level or SPICE model.

## What this is NOT (explicit disclaimers)

- **NOT** a simulation of actual quantum noise.
- **NOT** a model of any physical Zener diode's *measured* noise behavior.
  The design records explicitly state that Zener noise behavior is an
  *assumption*; this simulator honors that by making the input-noise
  distribution a user-selectable synthetic knob, not a calibrated Zener model.
- **NOT** a model of a tested or fabricated hardware board.
- **NOT** fabrication-authorized or physically validated.
- **NOT** connected to, derived from, or representative of any Double Alpha
  or 004c experiment.
- **NOT** connected to GitHub or any other repository.
- Uses **only** Python's standard library; no network calls, no installs.
- The input noise source is synthetic (configurable: `white`, `telegraph`,
  `burst`, or `sine` for deterministic probe). The Zener D1 = 1N4732A
  appears only as a labeled block; its avalanche noise statistics are not
  modeled and are explicitly an assumption per the design records.

## Public design-record values used (verbatim from task)

| Symbol | Value | Role |
|---|---|---|
| D1 | 1N4732A Zener | Noise source (behavior assumed, not modeled) |
| R_bias | 100 kΩ | Zener bias resistor |
| C1 | 0.1 µF | AC coupling capacitor (high-pass) |
| U1 | TLV9062 | Op-amp (configured non-inverting) |
| R2 | 1 kΩ | Feedback divider lower leg |
| R3 | 47 kΩ | Feedback divider upper leg |
| V_ref | 1.65 V | Output bias / mid-supply reference |
| R6 | 1 kΩ | Anti-alias series resistor |
| C3 | 750 pF | Anti-alias shunt capacitor |
| ADC | RP2350/Pico 2 GP26 | 12-bit ADC (modeled) |
| f_s | 500 kS/s | ADC sample rate |
| Rails | analog rails | Output clamp to rails (limits below) |

Nominal gain `1 + R3/R2 = 1 + 47/1 = 48` (task wording says "nominal gain 47";
both the strict formula `48` and the documented "47" are surfaced in the
output and the design note. The model uses the strict formula `48` for math
and reports the documentation-vs-formula discrepancy in every CSV header
comment). Anti-alias corner `1/(2π·R6·C3) = 1/(2π·1000·750e-12) ≈ 212.2 kHz`.

## Signal-path blocks (in order)

1. **Synthetic input source.** User-selectable:
   - `white` — Gaussian(`mu`, `sigma`) (default `mu=0`, `sigma=1`), seeded.
   - `telegraph` — two-state Markov over `{+A, −A}`, per-step flip prob.
   - `burst` — quiescent 0 with occasional Gaussian bursts.
   - `sine` — deterministic `A·sin(2π·f·t)` for filter / aliasing probes.
   The "Zener D1 + R_bias" block is represented as a labeled placeholder;
   its output is whatever the chosen synthetic source produces. This is an
   explicit assumption, not a schematic fact.
2. **C1 coupling (high-pass).** First-order discrete high-pass derived from the
   continuous transfer `H_HP(s) = s·R_eff·C1 / (1 + s·R_eff·C1)` using the
   bilinear transform. The effective resistance `R_eff` is **not specified**
   by the schematic; see "Added assumptions" below.
3. **Non-inverting amplifier.** `V_out = V_ref + G·(V_hp − V_ref)` where
   `G = 1 + R3/R2 = 48`. (Documentation says "47"; flagged, not reconciled.)
4. **Anti-alias low-pass.** First-order discrete low-pass from
   `H_LP(s) = 1 / (1 + s·R6·C3)`, bilinear-transformed, corner ≈ 212.2 kHz.
5. **Rail clamp.** Hard limit `V_lo ≤ V ≤ V_hi`. Limits are an assumption
   (see below).
6. **ADC sampling.** 12-bit quantizer with `V_lo` → code 0 and `V_hi` → code
   4095, sampled at `f_s = 500 kS/s`. Continuous-time input is evaluated at
   `t = k / f_s` for `k = 0, 1, …, N−1`.

## Added assumptions (every one; not silently presented as schematic facts)

| # | Assumption | Reason | Value used |
|---|---|---|---|
| A1 | Effective resistance for C1's high-pass | The schematic shows C1 in series between Zener/R_bias node and the op-amp input; the high-pass corner depends on the *effective* resistance seen by C1, which is not specified (it would be the parallel combination of bias-path output impedance, op-amp input impedance, and any bias-network divider — none of which are documented). | `R_eff = 100 kΩ` (set equal to the documented R_bias, as an *assumption*, with a CLI flag `--r-eff` to override). This places the high-pass corner at `1/(2π·R_eff·C1) ≈ 15.9 Hz`. |
| A2 | Analog rails for clamp/ADC | The Pico 2 ADC reference and analog supply range are not pinned down in the supplied design-record values. The model needs hard limits. | `V_lo = 0 V`, `V_hi = 3.3 V` (RP2350 ADC full-scale assumption). Both are CLI-overridable (`--v-lo`, `--v-hi`). |
| A3 | Input-noise distribution | The records explicitly say Zener noise behavior is an assumption. We must pick something to drive the model. | User-selectable synthetic source (white/telegraph/burst/sine). Defaults: `white, mu=0, sigma=1 V`. The 1 V σ is arbitrary and not a measured Zener value. |
| A4 | ADC bit depth | RP2350/Pico 2 GP26 is documented as 12-bit in the RP2350 datasheet; this is a reasonable assumption but the *effective* resolution after noise/INL is not modeled. | 12-bit, codes 0…4095. |
| A5 | Op-amp ideal behavior | TLV9062 is a real op-amp with finite GBW (1 MHz typical), slew rate, input bias current, voltage noise, etc. None are modeled. | Ideal infinite-GHz, zero-noise, zero-bias op-amp. |
| A6 | DC operating point of C1's input | With a real Zener, the C1 input side sits at the Zener breakdown voltage (~4.7 V for 1N4732A). With a synthetic source, there is no fixed DC level. | The synthetic source's own mean becomes the C1 input DC level; the high-pass removes it before the op-amp. The output is referenced to `V_ref = 1.65 V`. |
| A7 | Time-discretization | Continuous-time filters must be discretized for a software model. | Bilinear transform with the simulator's internal time step `dt = 1/f_s = 2 µs`. Frequencies near `f_s/2 = 250 kHz` are pre-warped; the anti-alias corner (212 kHz) is below Nyquist but close, so the bilinear approximation is acceptable but not exact. |
| A8 | Sampling instant | The ADC samples the continuous-time filter output at `t = k/f_s`. No aperture jitter, no sample-and-hold droop. | Ideal impulse sampling at `t = k/f_s`. |

## Nominal-gain discrepancy (flagged, not reconciled)

- Documentation in this task says "nominal gain 47".
- The strict formula for a non-inverting amplifier with `R2 = 1 kΩ` (lower
  feedback leg, to ground) and `R3 = 47 kΩ` (upper leg, output to inverting
  input) is `1 + R3/R2 = 1 + 47 = 48`.
- Possible interpretations of the documented "47":
  (a) `R3/R2 = 47` (i.e., gain of the feedback divider alone, omitting the
      "+1"); or
  (b) typo / informal rounding.
- The model **uses the strict formula `G = 48`** for math, and every CSV
  header carries the line `# documented_gain=47, formula_gain=48` so the
  discrepancy is visible in every output. The test for nominal gain checks
  `48` (formula); a separate test asserts the discrepancy is reported.

## Out of scope (limitations, plainly stated)

- No transistor-level or SPICE modeling of the TLV9062.
- No modeling of the 1N4732A's avalanche breakdown statistics, temperature
  dependence, or excess noise.
- No PCB layout, no parasitic capacitance / inductance, no supply noise,
  no ground bounce, no EMI.
- No calibration; the records say calibration is unresolved.
- No mechanical / enclosure / shielding modeling.
- The anti-alias filter is a single first-order RC; higher-order anti-alias
  filtering is not modeled.
- No simulation of ADC INL/DNL, missing codes, or temperature drift.
- No quantization-noise dithering model; quantization is ideal mid-tread.
- The model has not been validated against any physical board; it is a
  math-of-the-schematic exercise on documented values plus the assumptions
  above.

## What the tests check (stated before running)

(Exact tolerances are in `test_afe_model.py`'s module docstring.)

1. **Seeded repeatability** — same `--seed` and parameters produce
   byte-identical output. Strict.
2. **Nominal gain and bias** — with a DC input, output = `V_ref + G·(V_in − V_ref)` exactly (within float tolerance). Also: the gain-formula-vs-docs
   discrepancy is reported in the output header.
3. **Filtering behavior** — for a deterministic sine input well below the
   anti-alias corner (~10 kHz), the output amplitude matches the input
   amplitude times the cascade gain (high-pass ~unity, low-pass ~unity)
   within tolerance. For a sine well above the corner (~1 MHz), the output
   amplitude is attenuated by at least 10× relative to the in-band case.
4. **Clipping** — with an input large enough to exceed `V_hi`, the clamped
   output never exceeds `V_hi` and never goes below `V_lo`; ADC codes saturate
   at 4095 / 0.
5. **Sample-rate / Nyquist** — for an in-band sine (10 kHz @ 500 kS/s),
   `>5` samples per period are produced (Nyquist margin). For an above-Nyquist
   sine (600 kHz @ 500 kS/s), the *sampled* sequence shows aliasing: its
   discrete-time dominant frequency is below `f_s/2 = 250 kHz`, verified by
   a zero-crossing count that is lower than the in-band case.
