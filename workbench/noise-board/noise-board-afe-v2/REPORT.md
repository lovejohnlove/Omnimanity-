# AFE Rev1.1 Idealized Block Model — Report

## Status

**Classical synthetic software model.** Not physical validation. Not quantum.
Not 004c. Not connected to any experiment, prior repository, or external
dataset. Not a model of any physical Zener's measured noise behavior. Not a
tested or fabricated hardware board. Not fabrication-authorized or physically
validated.

## Files (recovered, SHA-256 verified)

| File | SHA-256 | Bytes |
|---|---|---:|
| `DESIGN_NOTE.md` | `4da0cd4e5ce1364cc8e563a65f418c336049f547c301c7c0db2c1dd474f6f3ff` | 9,432 |
| `afe_model.py` | `5e96f17f885de69cdc6a2a1a021b93b621475b4c78967171a31945f8787e31d7` | 13,686 |
| `test_afe_model.py` | `a6233085402c15f3ac1226037e5c3713d48c17367c2efe79a2c0a159de107f06` | 12,155 |
| `README.md` | `4e3db83305c7fca8c19999736792649c53ef3a8efa2b9a4782fba4c96b3e9756` | 2,950 |

## Test results

**10 tests passed** (0.101s), exit code 0.

```
test_clamp_bounds_and_saturation (Clipping) ... ok
test_in_band_vs_out_of_band_attenuation (FilteringBehavior) ... ok
test_gain_doc_differs_from_formula (NominalGainBias) ... ok
test_gain_formula_value (NominalGainBias) ... ok
test_low_freq_sine_gain_and_bias (NominalGainBias) ... ok
test_above_nyquist_aliases (SampleRateNyquist) ... ok
test_in_band_samples_per_period (SampleRateNyquist) ... ok
test_burst (SeededRepeatability) ... ok
test_telegraph (SeededRepeatability) ... ok
test_white (SeededRepeatability) ... ok

Ran 10 tests in 0.101s
OK
```

## Test criteria (stated before running)

1. **Seeded repeatability** (strict): same seed+params → byte-identical
   `v_hp`, `v_amp`, `v_clamp`, `adc_codes`.
2. **Nominal gain/bias**: `GAIN_FORMULA == 48.0`; `GAIN_DOC == 47.0`
   (discrepancy asserted); 1 kHz sine amp=0.02 V, N=50000, slice
   [40000:50000]: `|mean(v_amp)−V_REF| ≤ 0.01`; `|p-p − 1.92 V|/1.92 ≤ 0.05`.
3. **Filtering**: in-band 10 kHz vs out-of-band 240 kHz (above 212 kHz LP
   corner): `p-p_in / p-p_out ≥ 10`.
4. **Clipping**: 5 V sine; `v_clamp ∈ [0, 3.3]` strict; `max(adc)==4095`,
   `min(adc)==0` strict.
5. **Nyquist**: 10 kHz @ 500 kS/s → ≥5 samples/period; 600 kHz @ 500 kS/s
   aliases to ~100 kHz; zero-crossings < 2000.

## Measured numbers

| Quantity | Measured | Expected |
|---|---:|---|
| `v_amp` mean (1 kHz, amp=0.02 V, slice [40000:50000]) | 1.649998 V | 1.65 V |
| `v_amp` p-p | 1.919750 V | 1.9200 V |
| In-band 10 kHz `v_clamp` p-p | 1.918282 V | — |
| Out-of-band 240 kHz `v_clamp` p-p | 0.160149 V | — |
| Attenuation ratio (in/out) | 11.98× | ≥ 10 |
| 10 kHz samples/period | 50.0 | ≥ 5 |
| 600 kHz alias zero-crossings (N=4000) | 1599 | < 2000 |

## Public design-record values used

D1=1N4732A, R_bias=100 kΩ, C1=0.1 µF, TLV9062, R2=1 kΩ, R3=47 kΩ,
V_ref=1.65 V, R6=1 kΩ, C3=750 pF, RP2350/Pico 2 GP26 ADC at 500 kS/s,
clamp to analog rails.

Derived: `G = 1 + R3/R2 = 48` (documentation says 47 — flagged, not
reconciled). Anti-alias corner `1/(2π·R6·C3) ≈ 212.2 kHz`. Nyquist = 250 kHz.

## Signal path

`synthetic source → C1 high-pass (bilinear) → non-inverting amp (V_REF + G·v_hp)
→ 1st-order anti-alias low-pass (bilinear, ≈212 kHz) → rail clamp [V_lo, V_hi]
→ 12-bit ADC at f_s = 500 kS/s`

## Assumptions (every one; not schematic facts)

| # | Assumption | Value |
|---|---|---|
| A1 | R_eff for C1 high-pass | 100 kΩ (= R_bias; CLI `--r-eff`). f_HP ≈ 15.9 Hz. |
| A2 | Analog rails | V_lo=0 V, V_hi=3.3 V (RP2350 ADC full-scale; CLI overridable) |
| A3 | Input-noise distribution | Synthetic, user-selectable (white/telegraph/burst/sine) |
| A4 | ADC bit depth | 12-bit, codes 0…4095 |
| A5 | Op-amp ideal | Infinite GBW, zero noise, zero bias |
| A6 | C1 input DC | Source mean becomes C1 input DC; HP removes it |
| A7 | Time discretization | Bilinear transform at dt = 1/f_s = 2 µs |
| A8 | Sampling instant | Ideal impulse sampling at t = k/f_s |

## Bug found and fixed during build

Initial formula `v_amp = V_REF + G·(v_hp − V_REF)` was wrong: after AC
coupling, `v_hp` is centered at 0, not at V_REF. Corrected to
`v_amp = V_REF + G·v_hp` (single-supply non-inverting amp biased at V_REF).
Documented in code comments and DESIGN_NOTE.md.

## Limitations

- No transistor-level or SPICE modeling of TLV9062.
- No modeling of 1N4732A avalanche breakdown statistics, temperature
  dependence, or excess noise. Zener noise behavior is an explicit assumption.
- No PCB layout, parasitics, supply noise, ground bounce, EMI.
- No calibration (records say calibration is unresolved).
- Anti-alias filter is single first-order RC.
- No ADC INL/DNL, missing codes, or temperature drift.
- Bilinear discretization at dt = 2 µs is acceptable but not exact near
  Nyquist.
- Not validated against any physical board.

## Model-vs-hardware caveat

This is an idealized math-of-the-schematic exercise on documented values plus
the assumptions above. It is **not a physical validation** of the CUP Rev1.1
board. The Zener D1=1N4732A appears only as a labeled block; its avalanche
noise statistics are not modeled. The input source is synthetic. No result
here is a quantum-noise result, a measured-Zener result, a tested-board
result, or a Double Alpha / 004c experimental result.

## Known source-file discrepancy (not corrected — source file is hash-locked)

The recovered `DESIGN_NOTE.md` (a hash-locked source file that cannot be
modified without breaking the SHA-256 baseline) states in its test-criteria
section that the out-of-band filtering probe is "~1 MHz." The actual test
code (`test_afe_model.py` line 191) uses **240 kHz**, not 1 MHz. The test
comments explain the change: 1 MHz would alias above Nyquist (250 kHz), so
240 kHz was chosen as the cleanest below-Nyquist, above-corner probe. This
report (REPORT.md) correctly states 240 kHz throughout. The `DESIGN_NOTE.md`
text is a stale pre-edit description that was not updated when the test was
changed; it is preserved as-is to maintain the hash baseline.
