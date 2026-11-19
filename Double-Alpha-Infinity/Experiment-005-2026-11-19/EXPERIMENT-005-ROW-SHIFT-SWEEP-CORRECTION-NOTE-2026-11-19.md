# Experiment 005 — Correction Note for the Earlier Row-Shift Sweep

Date: 2026-11-19
Status: Local correction/addendum; it does not replace or edit the original run report.
Preserved report: `EXPERIMENT-005-COUPLED-ROW-SHIFT-SWEEP-REPORT-2026-11-19.md`

## Branch identity

The saved run evaluated the earlier row-shift family

```text
Mγ(ε) = P(ε) ⊗ P(ε),
then move γ ε² from source row (∞,∞), target (∞,∞),
to source row (∞,∞), target (r,r).
```

It did **not** evaluate the later marginal-preserving family with `δ = γ ε(1−ε)` distributed across four entries in row `(∞,∞)`. Results from these two families are separate and must not be merged.

The row-shift changes each coordinate's transition marginal in the `(∞,∞)` source row by `γ ε²`. It is therefore retained as a distinct “coupling plus marginal drift” arm, not as the marginal-preserving control and not as a result about coupling in general.

## Checks retained from the saved run

These checks remain useful; “exploratory run” does not mean every check is discarded.

1. **Endpoint identity, three sampled γ values:** At `ε=1`, the computed `gap₁₆(1,γ)` agrees with `g_single(1−γ)` for `γ=0.25, 0.5, 0.9`; the observed absolute differences were `0`, `0`, and about `1.33×10⁻¹⁵`, respectively.
2. **Six pinned eigenvalues:** Swap symmetry leaves the antisymmetric subspace invariant under the row update. Its six eigenvalues are the pairwise products `λᵢλⱼ` of the single-chain eigenvalues for `i<j`; they do not depend on `γ`. Comparing these against the full 16×16 spectrum at nine interior parameter points (`ε∈{0.2,0.5,0.8}`, `γ∈{0.25,0.5,0.9}`) gave maximum nearest-eigenvalue distance about `2.00×10⁻¹⁵` in double precision.
3. **Sampled SLEM bound:** Because the pinned set includes the single-chain non-Perron eigenvalues (`λ₁=1`), it implies `SLEM₁₆(ε,γ) ≥ ρ(ε)` and hence `gap₁₆ ≤ g_single(ε)` for this swap-symmetric row-shift family. On the saved 3,003-point grid, no numerical violation was found; the minimum sampled margin was zero at the periodic endpoint `ε=0`.
4. **Stochasticity and Kronecker baseline:** The saved run checked row sums and nonnegative entries across its grid; maximum absolute row-sum error was `2.22×10⁻¹⁶`. At `γ=0`, the `P⊗P` SLEM matched the single-chain SLEM to maximum absolute error about `3.00×10⁻¹⁵`.

These are algebraic structure checks with numerical verification on the stated points. The grid checks alone do not prove a property at every parameter value; the stated subspace argument supplies the general SLEM bound for this exact family.

## Downgrade of the extrema

The original report’s four extrema (two each at `γ=0.5` and `γ=0.9`) remain **exploratory numerical features**, not confirmed turning points. The original run used a 0.001 grid and a local 0.00005 grid refinement around the coarse extrema. It did not use the later package’s 50-digit refinement to `10⁻¹⁰` in `ε`, track eigenvalue branches, or measure the proposed permutation-based noise floor. Thus it does not meet that package’s confirmation criterion. No continuous-parameter claim is made.

The extrema concern only the `γ ε²` row-shift family. They do not answer the question posed by the later `δ = γ ε(1−ε)` marginal-preserving family.

## Artifact identity

The preserved files and hashes from the original local run are:

- Report: `EXPERIMENT-005-COUPLED-ROW-SHIFT-SWEEP-REPORT-2026-11-19.md` — SHA-256 `3c12cc9e0fc32b4c55cb63afbab5f497744bcdc2f2b678dec0488b83f2cbc4fc`
- Script: `coupled_row_shift_sweep.py` — SHA-256 `11f2a8d1cf636f61e80d776b49f0f9b5ac96c05898234e01b2c2b53b906fc2b3`
- CSV: `coupled_row_shift_sweep.csv` — SHA-256 `691a5ee0eb3548619ab90481386438427e86f38f1692cdb4faff53578448fcbd`
- JSON summary: `coupled_row_shift_sweep_summary.json` — SHA-256 `e074226f34fd43c1ff6990a144418994aa475987ba9cf9d2e6caca8b8a60f525`

Nothing was changed in the original report or sent to Drive, Dropbox, or GitHub. The marginal-preserving seven-γ run, if performed, belongs in a separate run record.
