# AFE Rev1.1 Topology Comparison & R_eff Sweep — Report

## Status

**Classical synthetic software model.** Not physical validation. Not quantum.
Not 004c. Not a determination of which topology is the "real" board. No winner
picked. Not connected to any experiment, prior repository, or external dataset.

## Files (recovered, SHA-256 verified)

| File | SHA-256 | Bytes |
|---|---|---:|
| `DESIGN_NOTE.md` | `5935cea1bcf28e00e682f8387ba6a30682e14e6d424739582be6287abf1f9ecf` | 8,259 |
| `afe_compare.py` | `b3ad822c621dfbddedb533125907afe06c797f55fb006695b8a44630b02b9609` | 15,103 |
| `test_afe_compare.py` | `98e37cb733300542d3b1109ad07128c0ddb59af48512789f175e7bdc0f1de0bc` | 12,233 |
| `README.md` | `74b06cc96aba839883c8f30d0fec68b75533a86c5c70c00bf0deb0a5f3efb0d0` | 3,942 |

## Test results

**11 tests passed** (1.136s), exit code 0.

```
test_corner_frequencies_match_analytical (SweepCornerFrequencies) ... ok
test_10kHz_pp_invariant_across_r_eff (SweepHighFreqInvariant) ... ok
test_100Hz_pp_matches_analytical_attenuation (SweepLowFreqAttenuation) ... ok
test_equation_mean_and_pp (TopologyA) ... ok
test_gain_value (TopologyA) ... ok
test_sign_argmax_coincides (TopologyA) ... ok
test_sign_positive_correlation (TopologyA) ... ok
test_equation_mean_and_pp (TopologyB) ... ok
test_gain_value (TopologyB) ... ok
test_sign_argmax_inverts (TopologyB) ... ok
test_sign_negative_correlation (TopologyB) ... ok

Ran 11 tests in 1.136s
OK
```

## Test criteria (stated before running)

1. **Topology A equation+sign** (`Vout = Vref + 48·Vin`): `G_NON_INV==48`;
   mean ≈ V_REF within 0.01; p-p ≈ 1.92 V within 5%; Pearson(v_hp,v_amp)>0.99;
   argmax(v_amp) coincides with argmax(v_hp) within 5 samples.
2. **Topology B equation+sign** (`Vout = Vref − 47·Vin`): `G_INV==47`;
   mean ≈ V_REF; p-p ≈ 1.88 V within 5%; Pearson(v_hp,v_amp)<−0.99;
   argmax(v_amp) coincides with argmin(v_hp) within 5 samples.
3. **Sweep corner frequencies** match `1/(2π·R_eff·C1)` within 0.1%.
4. **Sweep high-freq invariance** at 10 kHz: p-p varies <1% across R_eff.
5. **Sweep low-freq attenuation** at 100 Hz: measured p-p matches
   `2·amp·|G|·|H_HP(100 Hz)|` within 10% rel.

## Two hypothetical topology alternatives (both labeled as model alternatives, NOT circuit facts)

| Label | Topology hypothesis | Transfer function | Gain | Sign |
|---|---|---|---:|---|
| **A** | non-inverting | `Vout = Vref + 48·Vin` | 48 | positive |
| **B** | inverting (matches `G = R3/R2 = 47`) | `Vout = Vref − 47·Vin` | 47 | negative |

The available schematic record is text-only and does not establish the
complete topology. **No winner is picked.**

## R_eff sweep — measured results

**Corner frequencies** (analytical = `1/(2π·R_eff·C1)`):

| R_eff | f_HP (analytical) | f_HP (reported) |
|---:|---:|---:|
| 10 kΩ | 159.155 Hz | 159.155 Hz |
| 100 kΩ | 15.9155 Hz | 15.915 Hz |
| 1 MΩ | 1.59155 Hz | 1.592 Hz |

**Sweep at 100 Hz** (amp=0.02 V, N=50000, slice [10000:50000]):

| R_eff | f_HP | Topology | v_amp p-p (V) | v_amp mean (V) |
|---:|---:|---|---:|---:|
| 10 kΩ | 159.155 Hz | A (non-inv) | 1.021475 | 1.650000 |
| 10 kΩ | 159.155 Hz | B (inv) | 1.000194 | 1.650000 |
| 100 kΩ | 15.915 Hz | A | 1.905890 | 1.647480 |
| 100 kΩ | 15.915 Hz | B | 1.866184 | 1.652468 |
| 1 MΩ | 1.592 Hz | A | 1.925304 | 1.641391 |
| 1 MΩ | 1.592 Hz | B | 1.885193 | 1.658429 |

At 100 Hz the corner-frequency effect is clear: R_eff=10 kΩ (corner 159 Hz,
above the probe) gives strong attenuation (~53% of unity); R_eff=1 MΩ (corner
1.59 Hz, well below the probe) gives essentially unity.

**Sweep at 10 kHz** (sweep-invariance sanity check):

| R_eff | Topology | v_amp p-p (V) |
|---:|---|---:|
| 10 kΩ | A | 1.917643 |
| 10 kΩ | B | 1.877692 |
| 100 kΩ | A | 1.916603 |
| 100 kΩ | B | 1.876674 |
| 1 MΩ | A | 1.916299 |
| 1 MΩ | B | 1.876376 |

At 10 kHz (63× above the highest corner) all three R_eff values give the same
p-p to within 0.07%.

## Assumptions (A1–A10)

| # | Assumption | Value |
|---|---|---|
| A1 | R_eff for C1 high-pass | Swept at 10 kΩ / 100 kΩ / 1 MΩ (default 100 kΩ) |
| A2 | Analog rails | V_lo=0 V, V_hi=3.3 V |
| A3 | Input distribution | Synthetic, user-selectable |
| A4 | ADC bit depth | 12-bit |
| A5 | Op-amp ideal | Infinite GBW, zero noise |
| A6 | C1 input DC | Source mean; HP removes it |
| A7 | Time discretization | Bilinear at dt = 2 µs |
| A8 | Sampling instant | Ideal impulse at t = k/f_s |
| A9 | **Topology unspecified** | Both A and B are hypothetical; **no winner** |
| A10 | Single-stage model | No multiple gain/buffer stages |

## Bug found and fixed during build

Initial high-frequency invariance test used a 1 kHz probe and 1% threshold.
At 1 kHz with R_eff=10 kΩ (corner 159 Hz), `|H_HP(1 kHz)| ≈ 0.9876` — 1.3%
attenuation, slightly above 1%. Switched to 10 kHz (63× above highest corner)
where `|H_HP| > 0.9998` for all three R_eff. Measured invariance: <0.07%.

## Limitations

- **No topology determination.** Both A and B are hypothetical; no winner.
- No transistor-level or SPICE modeling of TLV9062.
- No modeling of 1N4732A avalanche breakdown statistics.
- No PCB layout, parasitics, supply noise, ground bounce, EMI.
- No calibration (records say calibration is unresolved).
- Single first-order RC anti-alias filter.
- HP slow-mode transient at very low corners (f_HP=1.59 Hz for R_eff=1 MΩ)
  takes ~100 ms to settle; small DC drift remains in the mean. p-p unaffected.
- Single-stage model; real boards may have multiple gain/buffer stages.
- Not validated against any physical board.

## Model-vs-hardware caveat

This is a sensitivity study of an idealized block model, not a measurement of
any physical board. The two topologies are model alternatives, not circuit
facts. The R_eff sweep shows how the model output changes when the assumed
effective resistance changes; it does not establish what the actual
effective resistance on any physical board is. No result here is a
quantum-noise result, a measured-Zener result, a tested-board result, or a
Double Alpha / 004c experimental result.

## Known source-file discrepancy (not corrected — source file is hash-locked)

The recovered `README.md` (a hash-locked source file that cannot be modified
without breaking the SHA-256 baseline) gives a sweep-invariance example using
`--sweep-freq 1000` (1 kHz). The actual test
(`test_afe_compare.py.test_10kHz_pp_invariant_across_r_eff`) uses **10 kHz**
(10,000 Hz), not 1 kHz. The test was changed from 1 kHz to 10 kHz during
development because 1 kHz is only 6× above the highest HP corner (159 Hz for
R_eff=10 kΩ), giving ~1.3% attenuation — above the 1% threshold. At 10 kHz
(63× above the highest corner) the attenuation is <0.02%. This report
(REPORT.md) correctly states 10 kHz throughout. The `README.md` example is a
stale pre-edit value; it is preserved as-is to maintain the hash baseline.
