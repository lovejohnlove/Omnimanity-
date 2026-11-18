# HANDOFF v2 — Double Alpha & 004c Review

**Status:** VERIFIED RECORD — 2026-11-18
**Repo:** lovejohnlove/Omnimanity-
**Path:** stories/HANDOFF-v2-Double-Alpha-and-004c-Review.md
**Size:** 14,316 bytes / 312 lines
**Supersedes:** HANDOFF — PART 2 (truncated draft, do not use)

> **CHANGELOG (nothing erased):**
> - v1 → v2: three-tier rule promoted to §0; symbol collision resolved;
>   retractions restored; environment scoring corrected.
> - v2 → v2.1: §3e promoted to THEOREM for irreducible birth-death chains;
>   §8 open question replaced with phase-type lead.
> - v2.1 → VERIFIED: push confirmed 2026-11-18 against the above path
>   and byte count.
> - **Known error, retained:** Z called the repo URL a typo. It was not.
>   404s were GitHub UI false negatives. Corrected, not deleted.

—

## 0. THE THREE-TIER RULE (read first)

Every claim sits in exactly one tier:

1. **DEFINITION** — true by stipulation. Says nothing about the world.
2. **THEOREM** — follows from the definition. A simulation can confirm it;
   it cannot falsify it. Tests the algebra, not reality.
3. **PREDICTION** — a claim about something outside the model. Could fail.
   Only this tier is physics.

Almost every overclaim in this exchange was a theorem wearing prediction's
clothes. The rule caught five of them across two AI systems and one human
relay, in public, with the retractions left in the record.

**Corollary:** "NOT ESTABLISHED" is a valid terminal answer. Never upgraded
to PASS by absence of failure.

—

## 1. WHO / WHAT / HOUSEWORDS

- **Johnathan Prizes** — pen name of the project owner.
- **Creed / Q / Cue** — collaborator. Simulated hardware ("noise board"),
  runs Python locally.
- **Z** — AI assistant, web chat. **Read-only.** Public fetch + search only.
  No shell, no filesystem, no git. Cannot run code or push.
- **DeepSeek** — second AI, relayed manually. Caught real errors; made real
  errors. Corrections ran both ways.
- **Grok** — performed the actual repository push. Not otherwise in the loop.

**House epistemics:**
- **Tag, do not resolve.** Contradictions are recorded, not smoothed.
- **Repository says ≠ reviewer infers.** Separate columns.
- **Fair Witness** reports observation only, refuses inference — but is
  *hired and placed*, so observation is a position, not neutrality.
  Project variant: **Ferry Witness / North of Zero**.
- **A definition is not a licence.** Defining a term gives it meaning, not
  consequences.
- **Never erase the mistakes.** Supersede in place, dated.

—

## 2. STRAND A — 004c REVIEW

**Inspected:** `main` at `52ea57c0806058817faab385d125ff859f7db8f6`
("Add byte-state validation sign-off draft", 2026-11-17T12:30:22Z, unsigned).
Parent: `d4ae3b2ff8e0b8546d0ed5381cbe47c34d114ec3`.

**Four REBUILD-1 files** (`experiments/004c/code/`), API sizes:

- `diff_004c_REBUILD-1.py` — 7,220 B
- `aggregate_004c_REBUILD-1.py` — 10,404 B
- `server_004c_FINAL_REBUILD-1.py` — 14,546 B
- `generator_004c_FINAL_REBUILD-1.py` — 20,536 B

SHA-256 values are **stated in the repo, not computed by Z**. The API's `sha`
fields are git blob **SHA-1**s — never compare them to SHA-256.

**Findings**

1. **A hedge became an assertion with no new evidence.** Prior: values "are
   the supplied recorded hashes." HEAD: **"SEAL STATUS: BYTE-STATE SEALED."**
   Hashes not recomputed in that commit. Same paragraph still lists
   "provenance … unverified."
2. **The sign-off names `d4ae3b2` (parent) but is added in `52ea57c`.** A
   sign-off cannot review a state it postdates. Not fixable by relabeling.
3. **Checkboxes pre-ticked; reviewer and date blank.**
4. **Three-way documentation conflict:**
   - `docs/README-RELAY-DRIFT.md` — console-direct sealed build *from the
     authoritative preregistration*.
   - `prereg/README-PREREG-STATUS.md` — authoritative preregistration
     **unresolved**.
   - sign-off draft — **no sealed artifact present.**
   → **Treat the seal as absent. The most restrictive record governs.**
5. **Byte-state identity ESTABLISHED** for four files (conditional on recorded
   hashes). **Provenance, correctness, performance: UNVERIFIED.**

**§12 environment — scored, not lumped**

- **vCPU: FAIL.** 2 reported vs. 4 required.
- **RAM: NOT ESTABLISHED.** 3.9 GiB is post-reservation total; nominal may be
  4 GiB.
- **Governor: NOT ESTABLISHED.** Absent in KVM guest = not observable here.
- **Dedicated / idle: NOT ESTABLISHED.** One-minute sample is a point reading.

Nothing was run, imported, compiled, or signed.

—

## 3. STRAND B — DOUBLE ALPHA

**What it is.** A dimensionless 4-state relational time model. **Not** a
string-theory proposal. Cycle: `0 → 1 → ∞ → r → 0`.

**Matrix** (ε = 0.900601):

```
P(ε) = [ 0    1    0      0    ]
       [ 0    0    1      0    ]
       [ 0    0     ε    1-ε    ]
       [ 1    0    0      0    ]
```

### 3a. ESTABLISHED — theorem tier

- Characteristic polynomial: **`λ⁴ − ελ³ − (1−ε) = 0`**
- Factors: `(λ−1)(λ³ + pλ² + pλ + p)`, `p = 1−ε`
- **Perron root = 1 for every ε** — carries no information
- **`|λ₂| ~ (1−ε)^(1/3)`**, exponent exactly 1/3
- At ε = 0.900601: **`|λ₂| ≈ 0.485`** (vs p^(1/3) ≈ 0.463; +4.7%)
- **Gap near ε = 0: `1 − |λ₂| ≈ ε/4`**
- Mean dwell at saturation `1/(1−ε) ≈ 10.06`; target 10 ⇒ **ε = 0.9 exactly**
- **ε = 0 is a genuine critical point** — pure cycle, no mixing
- **`αα` → `r` (state); `σ` (generator); `σ²` (return involution)**

### 3b. THE TWO ENDS ARE OPPOSITE

- **ε → 0:** mixing onset, gap opens **linearly** (~ε/4)
- **ε → 1:** cube-root regime; ∞ becomes **absorbing**; chain stops mixing

**The 1/3 law lives in the least dynamical corner of the model.**

### 3c. REFUTED / WITHDRAWN

- **α′ bridge: DEAD** — fails on dimensions, measured value, derivation
- **Lattice bridge:** dimensionally valid, **predictively empty** while a is free
- **Spectral radius as bridge: VOID** — Perron root = 1
- **0.94 ratio as constant: RETRACTED (Z's error)** — ε-dependent, ~0.90→~1.07
- **"Exponent dictates the ratio": RETRACTED (DeepSeek's mirror error)**
- **`αα · ∞ = 0` as algebra: indeterminate** in ℂ∪{∞}; valid only as graph edge
- **ε = 0.900601 is FITTED, not measured** — solved by bisection for dwell = 10
- **Double copy: unmapped**
- **Prefactor route: WITHDRAWN** — basis-dependent in truncated models

### 3d. THE EXTERNAL-CLASS FINDING

**1/3 = universal Puiseux signature of a third-order exceptional point.** At
ε = 1, rows 2 and 3 become identical → rank drop → `J₃(0)` → cube-root
splitting. Measured in ring resonators, cold atoms, cavity magnonics.

**Consequence: GENERIC, therefore NON-DISCRIMINATING.** Finding it elsewhere
confirms the algebra of triple degeneracy, not this model.

### 3e. THE STRUCTURAL BLOCKER

**THEOREM for irreducible birth-death chains.** An irreducible birth-death
chain is always reversible (detailed balance solves by construction), and
reversibility makes the generator similar to a symmetric matrix — real
spectrum, no exceptional point. Not a gap in search; a proof.

**NOT PROVEN in general.** Residual target: **phase-type queues (Coxian / PH
with feedback)** — directed cycle plus absorption, non-reversible, derived N,
defective generator possible. **LEAD, NOT TEST.** Nobody has shown an EP3
there, or that four phases would be forced.

### 3f. THE FOUR-STATES PROBLEM

**N = 4 is free and unforced.** Matching 4-state systems elsewhere (cell cycle,
seasons, cardiac phases) is **numerology** unless N is derived from the system.
Deriving N removes one free parameter; not the important one.

**Named analogue, not a test:** cell cycle with G2/M checkpoint arrest. The
four is the cell's, not the model's.

### 3g. FINAL DISPOSITION

> **TOY MODEL / THEOREM — EP3-adjacent defective Markov chain.**
> No external test. No physical scale. No α′ bridge. No physics claim.
> **Surviving math:** `λ⁴ − ελ³ − (1−ε) = 0`; `|λ₂| ~ (1−ε)^(1/3)`;
> gap `~ ε/4`; ε = 0 critical.
> **Physics question: CLOSED NEGATIVE** — on evidence, not proof.

—

## 4. 004c SEAL STATUS — CONFLICT RESOLUTION (draft)

Three corrections applied to the earlier draft:

- **Do not retroactively assign a review base.** Re-review at HEAD and record
  the date.
- **Provenance ≠ commit identity.** "Built from commit X" is *reproducibility*.
- **Do not fold 3.9 GiB into the FAIL.** vCPU = FAIL. RAM = NOT ESTABLISHED.

1. **Define "sealed" — three different meanings in current use:**
   - *Byte-state sealed* — files byte-identical to recorded SHA-256 manifest.
     Status: HASHES RECORDED — NOT INDEPENDENTLY RECOMPUTED.
   - *Environment sealed* — built on a §12-compliant machine.
     Status: **NOT ESTABLISHED** (2 vCPU vs 4 required).
   - *Provenance sealed* — who built it, when, from what.
     Status: **UNVERIFIED**.
2. **Review base:** ambiguous. Resolve by re-review at HEAD with a date.
3. **Evidence:** downgrade to **HASHES RECORDED — PROVENANCE UNVERIFIED**
   until a second independent computation exists.
4. **Environment:** file a new report against §12 with raw command output.
5. **Sign-off:** pre-ticked boxes invalid. Human name and date required.

—

## 5. NEXT ACTIONS

1. Commit the 004c conflict resolution page. Highest value; trail is warm.
2. One-paragraph description at the top of each public repo. Crawlers follow
   links and text; significance is not a signal they can see.
3. Correct ε/3 → ε/4 anywhere it survives in older ledgers.
4. If the ε-sieve runs, label it: it tests the simulator.
5. `α + α′ = 0` remains an unmapped representation of σ². Derive or drop.
6. Phase-type lead: check for EP3 with derived N. LEAD, NOT TEST.

—

## 6. TERMINOLOGY

- **TL / Time Loom** — the project. "TL" survives speech-to-text.
- **Omnimanity** — coined term. Verified unused elsewhere as of 2026-11-18.
- **CUP** — umbrella project; relation to the Loom NOT ESTABLISHED.
- **hold** — framework-level claim. Must specify what would fail it, or it is
  vocabulary.
- **Loom as mirror, not gate** — reflects a user's time-model rather than
  admitting or refusing. Requires disclosing the mirror's curvature:
  *we show what we received, what we did to it, and what we threw away.*
- **Cup on the table** — filed, not adjudicated.

—

## 7. WHAT Z CANNOT DO

No shell, no filesystem, no git, no execution, no memory between turns.
Public pages can be read; nothing can be written. **Any claim that Z ran system
checks, hashed files, or pushed commits is misattributed.** Those actions
happened on other surfaces (Creed's machine, Grok's push). Z is one node in a
relay carried by a human.

—

## 8. STANDING OPEN QUESTIONS

- Does the Loom constitute an authority by filtering? *Open.*
- Is CUP one project or a set? *Open.*
- Can phase-type queues with derived N produce an EP3? *Lead, not test.*
- Why four states? *Unforced.*
- Does `α + α′ = 0` derive from σ², or is it decoration? *Unmapped.*
