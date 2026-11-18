# HANDOFF v3 — Double Alpha & 004c Review

**Record status:** Reported execution log; consequences independently recalculated from the displayed matrix — 2026-11-18. The source, command, and environment for the reported run were not supplied, so its provenance is not independently verified.

**Document repository:** `lovejohnlove/Omnimanity-`  
**Path:** `Double-Alpha-Infinity/HANDOFF-v3-Double-Alpha-and-004c-Review.md`  
**004c source repository:** `lovejohnlove/-M-004`  
**Supersedes:** Earlier HANDOFF v2 records, retained unchanged; see the repository observations below.

## Change record

- **v1 → v2:** the three-tier rule was promoted to §0; the symbol collision was resolved; retractions were restored; environment scoring was corrected.
- **v2 → v2.1:** §3e was promoted to a theorem for irreducible birth-death chains; the §8 open question was replaced with a phase-type lead.
- **v2.1 → v3:** the numerical results were recalculated from the displayed matrix; the dwell discrepancy was corrected; the spectral-gap monotonicity was derived rather than inferred from six samples; the rank evidence for `J₃(0)` was retained. These checks do not verify the provenance of the relayed execution log.
- **Final v3 review pass:** the physics conclusion was narrowed to this object; ε=0.900601 was labeled unknown-origin; and numerical correctness was distinguished from execution authenticity, with a term added for that distinction.
- **Known error, retained:** Z called the repository URL a typo after three 404s. It was not a typo; the 404s were GitHub UI false negatives. Z also stated the correct principle (“404 is not proof of absence”) and then failed to apply it.
- **Known error, retained:** an earlier relayed message said “Committed and confirmed.” That claim was withdrawn; it was not supported by commit evidence available in that relay.
- **Known error, retained:** the 0.94 ratio was asserted as a constant. It depends on ε and was retracted by Z.

## 0. The three-tier rule

1. **DEFINITION** — true by stipulation. It says nothing by itself about the world.
2. **THEOREM** — follows from the definition and assumptions. A calculation can check its algebraic consequences; it cannot test whether the assumptions describe reality.
3. **PREDICTION** — a claim about something outside the model that could fail. Only this tier is physics.

Almost every overclaim in this exchange was a theorem wearing prediction’s clothes. The rule caught five of them across two AI systems and one human relay, with the retractions left in the record.

**Corollary:** “NOT ESTABLISHED” is a valid terminal answer. Do not upgrade a claim to PASS merely because no failure was observed.

**A useful distinction for this record:** an independent calculation can corroborate consequences of the supplied matrix. It cannot establish the provenance of somebody else’s run, the truth of the premises, or a physical prediction.

## 0a. Public v2 path and size observations

At the inspected public `lovejohnlove/Omnimanity-` `main` commit [`d809370ac2b1495992f19d84ff43cd60f49ca05e`](https://github.com/lovejohnlove/Omnimanity-/commit/d809370ac2b1495992f19d84ff43cd60f49ca05e), GitHub exposes two non-identical v2 files:

| Public path | GitHub API size / lines | Relevant file text | Raw-byte SHA-256 observed in this review |
|---|---:|---|---|
| [`stories/HANDOFF-v2-Double-Alpha-and-004c-Review.md`](https://github.com/lovejohnlove/Omnimanity-/blob/main/stories/HANDOFF-v2-Double-Alpha-and-004c-Review.md) | 14,627 bytes / 312 lines | No overall `VERIFIED RECORD` status line in its opening metadata | `2fc7860720fe1f8a4c45be64264b59ccb1636ad1d9478723b443e8507f5451eb` |
| [`Double-Alpha-Infinity/HANDOFF-v2-Double-Alpha-and-004c-Review.md`](https://github.com/lovejohnlove/Omnimanity-/blob/main/Double-Alpha-Infinity/HANDOFF-v2-Double-Alpha-and-004c-Review.md) | 11,111 bytes / 261 lines | Says `VERIFIED RECORD`, but its header claims the stories path and 14,316 bytes / 312 lines | `9e207bd26b9aa86b6e90b6c18a2ebe37c8deba5325a4406e910801ead9318565` |

These are **repository observations**, not a decision about which copy is canonical or how the copies came to differ. This draft does not edit or reconcile either v2 file. The new v3 path above was absent when checked.

## 1. Who / what / housewords

- **Johnathan Prizes** — pen name of the project owner.
- **Creed / Q / Cue** — collaborator. Simulated hardware (“noise board”), runs Python locally.
- **Z** — AI assistant in the referenced relay/session. In that session Z reported public fetch/search access but no shell, local filesystem, Git, or write route. This is a statement about that session only; other surfaces may differ.
- **DeepSeek** — second AI, relayed manually. It caught real errors and made real errors; corrections ran both ways.
- **Grok** — identified in the earlier record as the person who performed the earlier repository push; that attribution is retained as reported history.
- **Vibe** — attempted verification; was throttled at capacity. No result was produced.

**House epistemics:**

- **Tag, do not resolve.** Contradictions are recorded, not smoothed.
- **Repository says ≠ reviewer infers.** Keep those separate.
- **Fair Witness** reports observation only and refuses inference — but is *hired and placed*, so observation is a position, not neutrality. Project variant: **Ferry Witness / North of Zero**.
- **A definition is not a licence.** Defining a term gives it meaning, not consequences.
- **Never erase the mistakes.** Supersede in place, dated.

## 2. Strand A — 004c review

**Source inspected:** `lovejohnlove/-M-004`, `main` at commit [`52ea57c0806058817faab385d125ff859f7db8f6`](https://github.com/lovejohnlove/-M-004/commit/52ea57c0806058817faab385d125ff859f7db8f6), “Add byte-state validation sign-off draft,” 2026-11-17T12:30:22Z. GitHub marks the commit unsigned. Its parent is `d4ae3b2ff8e0b8546d0ed5381cbe47c34d114ec3`. The current `main` branch matched this commit when checked.

The four REBUILD-1 files in `experiments/004c/code/` have these GitHub API sizes:

- `diff_004c_REBUILD-1.py` — 7,220 B
- `aggregate_004c_REBUILD-1.py` — 10,404 B
- `server_004c_FINAL_REBUILD-1.py` — 14,546 B
- `generator_004c_FINAL_REBUILD-1.py` — 20,536 B

The repository records SHA-256 values for these files. The GitHub API `sha` fields are Git blob SHA-1 values and must not be compared with SHA-256. This review did not independently recompute the four SHA-256 values.

### Findings at the cited commit

1. The parent README called the code artifacts “sealed and hash-verified” and described the SHA-256 values as supplied recorded hashes. The cited commit changes this to **“SEAL STATUS: BYTE-STATE SEALED”**, scoped to four hash-identified local byte-states. The added sign-off draft reports local `cmp` checks and says the owner approved this limited wording, while explicitly disclaiming reviewer approval and a claim of provenance. These are repository statements; the draft has no named reviewer, date, signature, or raw command output. The narrow byte-state status is retained below, but this review does not independently verify its hashes or provenance.
2. The sign-off draft names `d4ae3b2`—the parent—as its review base and was added in `52ea57c`. That timing alone does not prove a review of the parent was impossible. Because the reviewer and date fields are blank, the reviewer identity and review timing are not established.
3. The sign-off draft has pre-ticked `[x]` checks and blank reviewer, date, approval, and signature fields. They remain statements in an unsigned draft, not an attributable sign-off.
4. The sign-off draft says no syntax, functional, synthetic, runtime, performance, concurrency, or reproducibility tests were performed for that sign-off, and no experiment was executed. This review did not run 004c code.
5. The repository’s broader §12 environment scoring is reported as follows; these values were not remeasured here:
   - **vCPU: FAIL** — 2 reported vs. 4 required.
   - **RAM: NOT ESTABLISHED** — 3.9 GiB is a post-reservation total; nominal capacity may be 4 GiB.
   - **Governor: NOT ESTABLISHED** — absent in the KVM guest is not observable here.
   - **Dedicated / idle: NOT ESTABLISHED** — a one-minute sample is a point reading.

## 3. Strand B — Double Alpha

**What it is:** a dimensionless, four-state relational time model, not a string-theory proposal. The cycle is `0 → 1 → ∞ → r → 0`.

For `0 ≤ ε ≤ 1`, the displayed row-stochastic matrix is:

```text
P(ε) = [ 0    1    0      0    ]
       [ 0    0    1      0    ]
       [ 0    0     ε    1-ε    ]
       [ 1    0    0      0    ]
```

Let `p = 1−ε`. Direct expansion gives

```text
χ(λ) = λ⁴ − ελ³ − (1−ε)
     = (λ−1)(λ³ + pλ² + pλ + p).
```

The Perron root is 1 for every ε, so it carries no information about the scale or physical meaning of this model.

### 3a. Matrix consequences and independent numerical checks

The non-Perron roots are roots of `q(λ)=λ³+pλ²+pλ+p`. As `p→0`, set `λ=p^(1/3)z`; after division by `p`, the equation tends to `z³+1=0`. Thus the nonzero roots scale as `p^(1/3)` near ε=1: the exponent is an algebraic asymptotic consequence of the supplied matrix. The reported local log-log slopes—0.3380, 0.3345, 0.3336—are consistent with that limit, but the slope method and source script were not supplied, so those exact slope values are not independently reproducible from the log alone.

Independent numerical calculations from the displayed matrix give:

- At ε = 0.900601: `|λ₂| = 0.485324705`; `p^(1/3) = 0.463227149`; relative excess = 4.770350% (rounds to +4.8%).
- At ε = 0.9: eigenvalue moduli `[1, 0.48631461, 0.48631461, 0.42282959]`.
- Near ε = 0, the calculated gaps `1−|λ₂|` are 0.026637722 at ε=0.1, 0.002515696 at ε=0.01, and 0.000250156 at ε=0.001. These agree with the reported values to their shown precision.
- At ε = 1, the matrix has rank 3; the characteristic polynomial is `λ³(λ−1)`, so zero has algebraic multiplicity 3 and geometric multiplicity 1. The exact ranks are `rank(A²)=2` and `rank(A³)=1`, establishing a single `J₃(0)` block.

For ε = 0.9, in state order `[0, 1, ∞, r]`, the stationary distribution is

```text
π = [1/13, 1/13, 10/13, 1/13]
  ≈ [0.07692, 0.07692, 0.76923, 0.07692].
```

The mean dwell at ∞ is `1/(1−ε)=10`; the mean return time to state 0 is `1/π₀ = 3 + 1/(1−ε) = 13`.

**Parameter origin:** at ε = 0.900601, `1/(1−ε) ≈ 10.06046` and the corresponding mean return time is about 13.06046—not a dwell of 10. By contrast, ε=0.9 gives dwell 10 and return time 13 exactly. **ε = 0.900601 has no established derivation. It is not fitted to dwell=10, not measured, and not derived. It is a number of unknown origin.**

### 3b. The two endpoints

- **ε = 0:** the matrix is a pure four-cycle. It is periodic and has spectral gap 0; it does not mix in the usual Markov-chain sense.
- **0 < ε < 1:** the chain is irreducible and aperiodic.
- **ε → 1:** state ∞ becomes absorbing and the chain becomes reducible. The non-Perron spectral radius tends to 0 and the spectral gap tends to 1; the chain converges to the absorbing state. “The chain stops mixing” is avoided here because it confuses loss of ongoing stochastic motion with convergence rate.

The cube-root regime is approached at the absorption endpoint, not at an interior setting. The gap statement below concerns the absolute spectral gap of this matrix; it is not a physical mixing measurement.

### 3c. The spectral gap is monotone on `[0,1]`

The reported numerical gap values are:

| ε | Reported gap `1−|λ₂|` |
|---:|---:|
| 0.0 | 0.0000 |
| 0.5 | 0.1774 |
| 0.9 | 0.5137 |
| 0.99 | 0.7781 |
| 0.999 | 0.8985 |
| 1.0 | 1.0000 |

Those samples alone would not establish monotonicity over a continuum. For this matrix, however, the monotonicity follows analytically. For `0<p<1`, the cubic `q(λ)=λ³+pλ²+pλ+p` has discriminant

```text
Δ = −p²(3p² − 14p + 27) < 0,
```

so it has one real root `−s` and a complex-conjugate pair. Here `0<s<1` and

```text
s³ = p(s²−s+1),       D = s²−s+1,       p = s³/D.
```

The complex pair has modulus `ρ = √(p/s) = s/√D`. Since `D<1` for `0<s<1`, this pair has larger modulus than the real root `−s`; therefore `|λ₂|=ρ`. Differentiation gives

```text
dp/ds = s²(s²−2s+3)/D² > 0,
dρ/ds = (2−s)/(2D^(3/2)) > 0.
```

Thus `ρ` increases with `p`; because `p=1−ε`, the gap `g=1−ρ` increases with ε. At the endpoints, `g(0)=0` and `g(1)=1`. Hence the gap is monotone on the full interval and has no interior turning point. Expanding near ε=0 gives `s=1−ε/2+O(ε²)`, `ρ=1−ε/4+O(ε²)`, and therefore `g=ε/4+O(ε²)`.

The numerical sweep may have prompted this finding; the monotonic result is visible from the algebra once the cubic is analyzed.

For the Loom, this means the matrix offers no distinguished interior regime: a qualitatively distinct middle setting cannot be obtained from this matrix alone. That conclusion is about this matrix, not the broader project; a different object or mechanism would need to be specified.

### 3d. Refuted / withdrawn

- **α′ bridge: DEAD** — it fails on dimensions, measured value, and derivation.
- **Lattice bridge:** dimensionally valid, but **predictively empty** while `a` is free.
- **Spectral radius as a physics bridge: VOID** — the Perron root is 1 identically.
- **0.94 ratio as a constant: RETRACTED (Z’s error)** — it depends on ε, approximately 0.90→1.07.
- **“Exponent dictates the ratio”: RETRACTED (DeepSeek’s mirror error)** — an exponent dictates scaling, not a fixed ratio value.
- **`αα · ∞ = 0` as algebra: indeterminate** in `ℂ∪{∞}`; valid only as a graph edge.
- **ε = 0.900601:** no established derivation; not fitted to dwell=10, not measured, and not derived. It is a number of unknown origin.
- **Double copy: unmapped.** Amplitude factorization (gravity = gauge²) is not an additive conjugate pair.
- **Prefactor route: WITHDRAWN** — in truncated models the perturbation overlap is basis-dependent.

### 3e. External-class finding — one cited experiment

A cube-root response is a generic perturbative signature associated with a third-order exceptional point; it is not unique evidence for this model. Hodaei et al. report an experimental observation of higher-order exceptional points in a ternary parity–time-symmetric photonic laser molecule and a cube-root frequency response to refractive-index perturbations: [“Enhanced sensitivity at higher-order exceptional points,” *Nature* 548, 187–191 (2017), DOI 10.1038/nature23280](https://www.nature.com/articles/nature23280); [PubMed record](https://pubmed.ncbi.nlm.nih.gov/28796201/).

This is evidence for a related optical experiment, not validation of the Double Alpha matrix or a physical bridge from it. Cold-atom and magnonics examples from earlier wording are omitted because no verified citations for them are carried into this draft.

### 3f. Structural blocker

**Theorem for irreducible birth-death chains:** an irreducible birth-death chain is reversible (detailed balance solves by construction), and its generator is similar to a symmetric matrix. Its spectrum is real, so it cannot have an exceptional point. This is a result within that class, not a gap in searching for examples.

**NOT PROVEN in general.** A residual lead is phase-type queues (Coxian / phase-type chains with feedback): directed cycle plus absorption, non-reversible, with a defective generator possible. **LEAD, NOT TEST.** No EP3 has been shown there, and four phases have not been shown to be forced.

### 3g. The four-states problem

**N = 4 is free and unforced.** Matching four-state systems elsewhere (cell cycle, seasons, cardiac phases) is **numerology** unless N is derived from the system. Deriving N removes one free parameter, not the important one.

**Named analogue, not a test:** cell cycle with G2/M checkpoint arrest. The four is the cell’s, not the model’s.

### 3h. Final disposition

> **TOY MODEL / THEOREM — EP3-adjacent defective Markov chain.**
> Matrix consequences were independently recalculated from the displayed matrix. The reported execution log’s provenance is not established. No external test, physical scale, α′ bridge, or physics claim is established here.
> **Surviving math:** `λ⁴−ελ³−(1−ε)=0`; `|λ₂|~(1−ε)^(1/3)`; gap `ε/4+O(ε²)` near ε=0; `J₃(0)` by rank; gap monotone on `[0,1]`.
> **No physics claim is established for this object.**

## 4. 004c seal status — scoped claim and unresolved wider conflict

The narrow **BYTE-STATE SEALED** status is retained for the four hash-identified local byte-states, as stated in the 004c sign-off draft. This does **not** mean that provenance, preregistration compliance, runtime correctness, performance, concurrency, or §12 compliance is established. This review did not recompute the four SHA-256 values.

For clarity, three meanings remain separate:

- **Byte-state sealed:** the record claims byte identity to recorded hashes for four local byte-states; this review did not independently recompute SHA-256.
- **Environment sealed:** built on a §12-compliant machine; **NOT ESTABLISHED** (2 reported vCPU vs. 4 required, with other environment measures also unresolved).
- **Provenance sealed:** who built it, when, and from what source; **UNVERIFIED**.

The public records at the cited `-M-004` commit use “sealed” with different scopes and are preserved here without choosing a winner:

| Record | Repository statement |
|---|---|
| [`experiments/004c/docs/README-RELAY-DRIFT.md`](https://github.com/lovejohnlove/-M-004/blob/52ea57c0806058817faab385d125ff859f7db8f6/experiments/004c/docs/README-RELAY-DRIFT.md) | Says the earlier relayed files are not the sealed pipeline and records their mismatch; also says the four REBUILD-1 files are a fresh build against the authoritative v1.6.2 prereg and v1.0.8 design-spec, “sealed by console-direct four-command read.” |
| [`experiments/004c/prereg/README-PREREG-STATUS.md`](https://github.com/lovejohnlove/-M-004/blob/52ea57c0806058817faab385d125ff859f7db8f6/experiments/004c/prereg/README-PREREG-STATUS.md) | Says §1 is unresolved and the full authoritative preregistration base is not present in available files. |
| [`experiments/004c/unsealed/REBUILD-1/README-PRESERVATION-ONLY.md`](https://github.com/lovejohnlove/-M-004/blob/52ea57c0806058817faab385d125ff859f7db8f6/experiments/004c/unsealed/REBUILD-1/README-PRESERVATION-ONLY.md) | Says “HASHES RECORDED, PRESERVATION ONLY — NOT SEALED; NOT VERIFIED BY CONSOLE-DIRECT READ”; describes a local copy/hash match only. |
| [`experiments/004c/sealed/README-STATUS-PROPOSED.md`](https://github.com/lovejohnlove/-M-004/blob/52ea57c0806058817faab385d125ff859f7db8f6/experiments/004c/sealed/README-STATUS-PROPOSED.md) | Says no sealed code artifact is present in that designated directory; the note itself is not a seal. |
| [`experiments/004c/docs/VALIDATION_AUTHORIZATION_ONE_PAGE_SIGNOFF_DRAFT.md`](https://github.com/lovejohnlove/-M-004/blob/52ea57c0806058817faab385d125ff859f7db8f6/experiments/004c/docs/VALIDATION_AUTHORIZATION_ONE_PAGE_SIGNOFF_DRAFT.md) | Says “SEAL STATUS: BYTE-STATE SEALED,” scoped only to the four hash-identified local byte-states; it says provenance and tests remain unverified and has blank reviewer/date/signature fields. |

These statements may refer to different objects or meanings of “sealed”; the relationship is **UNRESOLVED**. Retain the scoped byte-state claim; do not turn it into a broader pipeline, provenance, environment, or experimental seal, and do not erase the other records.

**Three status corrections carried forward:**

- Do not treat the sign-off’s parent commit as invalid merely because the draft was added in its child; the missing reviewer/date leave timing and attribution unestablished.
- **Provenance ≠ commit identity.** “Executed using commit X” can support reproducibility; provenance also requires who built it, when, and from what source.
- Do not fold the reported 3.9 GiB into the vCPU failure. vCPU is reported FAIL; RAM remains NOT ESTABLISHED.

## 5. Next actions

1. If a separate 004c status page is prepared, preserve **BYTE-STATE SEALED** at its narrow scope and tag the wider document conflict without resolving it.
2. Add a concise description at the top of each public repository; links and plain text help readers find the material.
3. Correct any remaining `ε/3` gap statement to `ε/4` where it refers to this matrix near ε=0.
4. If the ε-sieve runs, label it: it tests the simulator.
5. `α + α′ = 0` remains an unmapped representation of `σ²`. Derive or drop it.
6. Treat the phase-type direction as a lead, not a test; investigate EP3 with derived N only if the project chooses to pursue it.

## 6. Terminology

- **TL / Time Loom** — the project. “TL” survives speech-to-text.
- **Omnimanity** — coined term. Verified unused elsewhere as of 2026-11-18, as reported in the prior record.
- **CUP** — umbrella project; relation to the Loom is NOT ESTABLISHED.
- **hold** — framework-level claim. It must specify what would fail it, or it is vocabulary.
- **Loom as mirror, not gate** — reflects a user’s time-model rather than admitting or refusing. It requires disclosing the mirror’s curvature: *we show what we received, what we did to it, and what we threw away.*
- **Cup on the table** — filed, not adjudicated.
- **Correct-but-unauthenticated** — a record whose mathematical consequences have been independently verified against a supplied premise, but whose provenance (who ran it, where, and when) is unverified. Example: the reported §9 execution log.

## 7. What Z could do in the referenced session

For the specific Z session described in this relay, the stated limits were no shell, local filesystem, Git, execution, or write route; public pages could be fetched/searched. This is not a product-wide statement. The Part 2 output is described as having been run on another surface and relayed. Claims that Z itself ran system checks, hashed files, or pushed commits would be misattributed to that session.

## 8. Standing open questions

- Does the Loom constitute an authority by filtering? *Open.*
- Is CUP one project or a set? *Open.*
- Can phase-type queues with derived N produce an EP3? *Lead, not test.*
- Why four states? *Unforced.*
- Does `α + α′ = 0` derive from `σ²`, or is it decoration? *Unmapped.*
- Does the Loom require an interior regime? If yes, this matrix is the wrong object.

## 9. Reported execution log

The following block is transcribed from the supplied Part 2. It is a **reported log**, not an authenticated run: the script, exact command, Python/library versions, input file, and raw execution environment were not supplied.

```text
char poly: -e*lam**3 + e + lam**4 - 1 | matches claim: True
factorisation (lam-1)(lam^3+p lam^2+p lam+p) matches: True

eps=0.900601 eigenvalue moduli: [1.0, 0.4853, 0.4853, 0.422]
|l2|=0.4853  p^(1/3)=0.4632  excess=4.8%   (doc: 0.485, 0.463, +4.7%)
eps=0.9 moduli: [1.0, 0.4863, 0.4863, 0.4228]   (taxonomy doc quoted 0.4863, 0.4863, 0.4228)

gap 1-|l2| vs eps/4 near 0:
  eps=0.1    gap=0.026638   eps/4=0.025000
  eps=0.01   gap=0.002516   eps/4=0.002500
  eps=0.001  gap=0.000250   eps/4=0.000250

local log-log slope of |l2| vs p=1-eps:
  p=0.001: |l2|=0.10154  slope=0.3380
  p=1e-05: |l2|=0.02162  slope=0.3345
  p=1e-07: |l2|=0.00465  slope=0.3336

spectral gap 1-|l2| across eps:
  eps=0.0    gap=0.0000
  eps=0.5    gap=0.1774
  eps=0.9    gap=0.5137
  eps=0.99   gap=0.7781
  eps=0.999  gap=0.8985
  eps=1.0    gap=1.0000

eps=1: rank = 3 | alg mult of 0 = 3 | geom mult = 1
rank(A^2)= 2  rank(A^3)= 1  (single J3(0) block iff ranks 2,1)

eps=0.9: pi=[0.07692 0.07692 0.76923 0.07692]  return time to state0=13.0000  (3+1/(1-eps)=13.0000)  dwell 1/(1-eps)=10.0000

eps=0.900601: pi=[0.07657 0.07657 0.7703  0.07657]  return time to state0=13.0605  (3+1/(1-eps)=13.0605)  dwell 1/(1-eps)=10.0605
```

### 9a. What is independently supported

The characteristic polynomial, factorization, Perron root, eigenvalue magnitudes, listed gap samples, ε=1 rank pattern, stationary distribution, and dwell/return formulas were independently recalculated from the displayed matrix. The exact numerical values above agree to the precision shown, with the ε=0.900601 dwell correction stated in §3a.

The reported log’s `|λ₂| = 0.4853` and the independent calculation’s `0.485324705` agree to four decimal places. The number in the log is correct to its displayed precision. Correctness does not imply authenticity: matching the matrix’s consequences does not prove that the log was generated by a real run in the claimed, but undocumented, environment.

The global monotonicity of the spectral gap is supported by the derivation in §3c, not by the finite sample table alone. The asymptotic exponent 1/3 follows from the cubic scaling in §3a; the reported finite log-log slopes are not independently reproducible without their calculation method.

### 9b. What this record does not establish

- **Not a prediction.** It checks consequences of a supplied theorem/model; it does not test an external physical claim.
- **Not a physics claim.** The matrix is dimensionless; no physical scale or α′ bridge is established.
- **Not a derivation of N = 4.** The state count was chosen.
- **Not independent of the model.** The matrix was supplied as input; these checks verify consequences, not premises.
- **Not proof of the original run’s provenance.** No source script, command, environment, or raw execution capture was supplied. Reproduction of the calculation from the matrix does not prove where the relayed log came from.
- **Not 004c runtime verification.** No 004c code was run or tested in this review.
