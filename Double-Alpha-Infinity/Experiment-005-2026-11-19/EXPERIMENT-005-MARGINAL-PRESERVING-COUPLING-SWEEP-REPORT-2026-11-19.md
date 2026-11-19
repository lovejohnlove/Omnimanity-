# Experiment 005 — Marginal-Preserving Coupling Sweep

Date: 2026-11-19  
Status: Local exploratory numerical result; not preregistered, peer-reviewed, or a physical claim  
Relationship: Separate arm from the earlier `γ ε²` row-shift run. The earlier row-shift report and correction note remain unchanged.

## Main finding

The marginal-preserving arm is monotone on the sampled grid for all seven tested values of `γ`, but monotonicity is not the same as equality with the single-chain curve. In particular, the largest non-Perron modulus in the 10×10 swap-symmetric block **does exceed** the single-chain `ρ(ε)` for `γ=0.9` and `γ=1`. No such excess above a `10⁻¹²` numerical threshold was found for `γ≤0.75`.

A 50-digit local refinement of the block-excess peaks gives:

| γ | Refined ε | Symmetric-block SLEM | `ρ(ε)` | Excess |
|---:|---:|---:|---:|---:|
| 0.9 | 0.6785502983657621… | 0.7467636724355946… | 0.7161304898787759… | 0.0306331825568187… |
| 1.0 | 0.7012746569121385… | 0.7537344989455635… | 0.6994261418900880… | 0.0543083570554754… |

The refined ε brackets are each about `3.92×10⁻¹¹` wide. These are local numerical maxima of the block excess, not global proofs over the continuous parameter interval. At those two ε values, the full gap is about `0.2532363` and `0.2462655`, respectively, below the corresponding single-chain gaps (`0.2838695` and `0.3005739`).

## What was computed

The pair state order is `[0,1,∞,r]`, with row-major pair index `4a+b`. Starting from `P(ε)⊗P(ε)`, only source row `(∞,∞)` is changed: with `δ=γ ε(1−ε)`, add `δ` to targets `(∞,∞)` and `(r,r)`, and subtract `δ` from `(∞,r)` and `(r,∞)`. The tested values are `γ∈{0,0.1,0.25,0.5,0.75,0.9,1}`.

The grid contains 1,001 uniform ε points from 0 to 1, plus 141 logarithmically spaced values of `p=1−ε` from `10⁻¹` to `10⁻⁸`, with overlaps deduplicated at tolerance `10⁻¹⁴`: 1,139 unique ε values, or 7,973 matrices total. The proposed endpoint anchors were checked: at `γ=0`, the matrix is exactly `P⊗P` and its gap matches the single-chain gap within `3.0×10⁻¹⁵`; at `γ=1`, row `(∞,∞)` is `ε` to `(∞,∞)` and `1−ε` to `(r,r)`, with the computed row agreeing within `1.2×10⁻¹⁶`.

## Structural checks and interpretation

Marginal preservation makes the coordinate-only observable subspaces invariant with action `P(ε)`. This yields the degree-7 coordinate factor: one eigenvalue 1 and two copies of each of the three nontrivial eigenvalues of `P`; the generic complementary factor has degree 9. Separately, swap symmetry yields a 10-dimensional symmetric block and a 6-dimensional antisymmetric block. The antisymmetric eigenvalues are the six products `λᵢλⱼ` for `i<j`.

These structures give two algebraic routes to `SLEM₁₆≥ρ(ε)`: the invariant coordinate-observable action contains the nontrivial roots of `P`, and the antisymmetric products include `1·λᵢ`. Thus the bound is structural for this family, not merely a grid observation. It does **not** imply that the gap is monotone or that the symmetric block stays below `ρ`.

The degree-7 factor was not treated as `χ_P²`. Across the sweep, the coordinate-space invariance residual was at most `1.0×10⁻¹⁵`, the characteristic-coefficient factor check error at most `1.8×10⁻¹⁵`, and the degree-7 roots’ maximum distance to the full spectrum at most `7.8×10⁻¹⁵`. Direct 16×16 eigenvalues matched the union of the 10×10 and 6×6 block spectra to at most `8.2×10⁻¹⁵`; the direct and block-route SLEM values differed by at most `5.7×10⁻¹⁵`. Row-sum and marginal errors were each at most `2.3×10⁻¹⁶`; swap commutation was exact in the computed matrices, with off-block residual at most `2.8×10⁻¹⁷`. All sampled transition probabilities were nonnegative.

State-label permutation checks covered 175 sampled matrices, with eight random simultaneous row/column relabelings each (1,400 comparisons total). The largest matched-spectrum and SLEM change was `8.6×10⁻¹⁵`, far below the refined `γ=0.9` and `γ=1` excesses.

## Gap behavior and endpoint

For each γ, all 1,138 adjacent sampled gap steps increased; the sampled endpoint gaps were 0 (within roundoff) at `ε=0` and 1 at `ε=1`. No grid-resolved gap turning point was found, so there was no gap extremum to refine. This remains a statement about the specified finite grid, not a proof of continuous monotonicity. The separate symmetric-block excess peaks above were refined because they directly address whether the block exceeds `ρ`.

Near `ε=1`, a 50-digit eigensolve over `p=10⁻²…10⁻⁸` gives finite-range log–log SLEM slopes from about 0.3352 to 0.3380 across the seven γ values. This is consistent with a `p^(1/3)`-like approach over the tested range, but it is empirical and does not establish an asymptotic law or smoothness. Sampling was logarithmic near the endpoint rather than assuming a smooth extremum there.

One numerical caveat was diagnosed: at `ε=1`, the degree-7 factor is `(λ−1)λ⁶`, so ordinary double-precision root matching is ill-conditioned for the sixfold zero cluster (a root-only diagnostic showed an apparent error near `10⁻⁷`). The more stable characteristic-coefficient and invariant-space checks passed, and a separate 50-digit check gave zero invariant-subspace residual with the six computed zero-root moduli no larger than `7.6×10⁻²⁶`. This is an eigensolver-conditioning issue, not a mismatch between the full matrix and the swap-block route.

Eigenvalue branches were tracked across the ordered grid by minimum-distance spectral matching. The 127,568-row branch file uses path-dependent labels; exact/repeated eigenvalues make labels ambiguous at collisions. No exceptional-point label is assigned: branch proximity or a crossing is not enough without a high-precision coalescence and geometric-multiplicity check.

## Disposition and records

This arm answers a different question from the earlier row-shift family: it preserves one-coordinate marginals, whereas the `γ ε²` row shift adds marginal drift. Keep both as separately named arms; do not merge their extrema or interpretations. This run is local and review-only. Nothing was published or uploaded, and it does not revise HANDOFF v7, the 005a contract, or the earlier report/correction note.

The earlier row-shift files were hash-checked before and after this run and are unchanged:

- Earlier report: `EXPERIMENT-005-COUPLED-ROW-SHIFT-SWEEP-REPORT-2026-11-19.md` — SHA-256 `3c12cc9e0fc32b4c55cb63afbab5f497744bcdc2f2b678dec0488b83f2cbc4fc`
- Earlier correction note: `EXPERIMENT-005-ROW-SHIFT-SWEEP-CORRECTION-NOTE-2026-11-19.md` — SHA-256 `e5f13ada7ab5793add7705fdde3303277270d28f9392c7091f4031f6d688c910`
- Earlier script, CSV, and JSON hashes also match their pre-run values.

The new run artifacts are `marginal_preserving_coupling_sweep.py`, `marginal_preserving_coupling_sweep.csv`, `marginal_preserving_coupling_sweep_summary.json`, and `marginal_preserving_coupling_branch_tracking.csv` in `/workspace`. The CSV contains all 7,973 matrix results; the branch CSV contains eigenvalue values and path-dependent labels. The summary records validation maxima, permutation noise checks, block-excess refinements, and endpoint tests.

The calculations used Python 3.12, NumPy 2.5.3, and mpmath 50-digit arithmetic on Linux x86-64. No physical data, performance measurement, or hardware was involved.
