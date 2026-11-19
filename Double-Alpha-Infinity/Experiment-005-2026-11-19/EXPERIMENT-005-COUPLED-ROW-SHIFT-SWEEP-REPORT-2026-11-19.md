# Experiment 005 — Exploratory Sweep of the Proposed Two-Thread Row-Shift Family

Date: 2026-11-19
Status: Local exploratory numerical result; not preregistered, peer-reviewed, or a physical claim
Scope: One specific 16-state matrix family described in the supplied coupling proposal. This does not revise HANDOFF v7 or the 005a measurement contract, and it is not an execution of 004c.

## Question

Does the specified two-thread row-shift family show a grid-resolved interior turning point in the spectral gap `g = 1 − SLEM` as `ε` varies, for `γ ∈ {0.25, 0.5, 0.9}`?

## Matrix family actually evaluated

Use the single-thread transition matrix, in state order `[0, 1, ∞, r]`,

```text
P(ε) = [[0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, ε, 1−ε],
        [1, 0, 0, 0]].
```

For the two-thread state pair `(a,b)`, use row-major index `4a+b` and begin with `M₀(ε)=P(ε)⊗P(ε)`. In the one source row `(∞,∞)`, move mass `γ ε²` from the target `(∞,∞)` to target `(r,r)`. Every other entry is unchanged. This implements the concrete proposal in the supplied `Pasted_content_94.txt`.

The sweep used 1,001 equally spaced `ε` values on `[0,1]` (step `0.001`) for each of the three specified `γ` values. The reported gap is `1 − SLEM`, where SLEM is the largest eigenvalue modulus after removing one eigenvalue nearest to `1`; any additional unit-modulus eigenvalues remain in the SLEM. A separate local refinement used a `0.00005` `ε` grid in a ±0.004 neighborhood around each coarse-grid extremum.

## Numerical result

| γ | Gap at ε=0 | Gap at ε=1 | Result on the 0.001 grid | Local refinement |
|---:|---:|---:|---|---|
| 0.25 | 0 (within roundoff) | 0.33989410 | 1,000 increasing steps; no grid-resolved turning point | Not applicable |
| 0.5 | 0 (within roundoff) | 0.17743998 | 837 increasing and 163 decreasing steps; non-monotone | Maximum near `ε=0.73145`, `g≈0.16413918`; minimum near `ε=0.89355`, `g≈0.15777883` |
| 0.9 | 0 (within roundoff) | 0.02663772 | 570 increasing and 430 decreasing steps; non-monotone | Maximum near `ε=0.55720`, `g≈0.10909851`; minimum near `ε=0.98660`, `g≈0.02626606` |

The local refinement is a denser numerical search, not a proof of exact critical points or a guarantee that no narrower feature exists elsewhere. For `γ=0.25`, “no turning point” means none was resolved on this grid; it is not a continuous-parameter proof.

## Numerical checks and implementation

- Every matrix in the sweep remained row-stochastic to floating-point precision: maximum absolute row-sum error `2.22×10⁻¹⁶`; minimum transition probability `0`.
- At `γ=0`, the computed SLEM of `P⊗P` agreed with the single-chain SLEM over the sampled grid to maximum absolute error `2.998×10⁻¹⁵`.
- The row shift changes the marginal transition distribution of each individual thread in the `(∞,∞)` source row. The maximum single-coordinate marginal drift over `ε∈[0,1]` is `γ` (0.25, 0.5, or 0.9 respectively). Thus this construction changes both the product structure and the component marginals; the observed non-monotonicity cannot be attributed to “coupling as such” or isolated from that row-level marginal change.
- The first exploratory output exposed an off-by-one index in the turning-point locator. I corrected it and reran the full grid before producing the values in this report; the first pass’s turning-point coordinates are superseded and should not be used.
- The script was run locally with Python 3.12.3 and NumPy 2.5.3 on Linux 6.18.38+ x86-64. It passed Python bytecode compilation. No physical data, performance measurement, or hardware was involved.

## Disposition

For the exact proposed row-shift family, the 0.001-grid sweep finds an interior maximum and minimum at `γ=0.5` and `γ=0.9`; it finds no grid-resolved turning point at `γ=0.25`. This answers the narrow numerical question for that family only. Because the construction changes the single-thread marginals, it is not a controlled demonstration that coupling alone creates the turning points. A separate, explicitly specified marginals-preserving coupling would be a different family and would need its own run.

No inference about the Time Loom, Double Alpha as a whole, physical time, gravity, or 005b follows from these matrix results. The proposed `q(r)` candidate and calibration maps for 005a are still absent; this sweep does not supply them.

## Reproduction files

- Script: `coupled_row_shift_sweep.py`
- Full 3,003-row output: `coupled_row_shift_sweep.csv`
- Machine-readable summary: `coupled_row_shift_sweep_summary.json`

This report is local and review-only. Nothing was written to GitHub, Drive, or Dropbox.
