# HANDOFF v2 — Double Alpha & 004c Review
Compiled 2026-11-18. Supersedes any earlier handoff (none was published).
Two independent strands. Read §0 and §1 first — they govern everything below.

---

## 0. THE THREE-TIER RULE (read this first)

Every claim in this project sits in exactly one tier:

1. **DEFINITION** — true by stipulation. Free. Says nothing about the world.
2. **THEOREM** — follows from the definition. A simulation can confirm it;
   it cannot falsify it. Tests the algebra, not reality.
3. **PREDICTION** — a claim about something outside the model. Could fail.
   Only this tier is physics.

**Almost every overclaim in this exchange was a theorem wearing prediction's
clothes.** The rule caught five of them across two AI systems and one human
relay, in public, with the retractions left in the record. That rule — not the
model — is the artifact worth keeping.

Corollary: **"NOT ESTABLISHED" is a valid terminal answer.** Never upgraded to
PASS by absence of failure.

---

## 1. WHO / WHAT / HOUSEWORDS

- **Johnathan Prizes** — pen name of the project owner.
- **Creed / Q / Cue** — collaborator. Simulated hardware ("noise board"), runs
  Python locally.
- **Z** — an AI assistant in a web chat. **Read-only.** Can fetch public pages
  and search. Cannot run code, read local files, or push to any repository.
  Every system check quoted below came from a *different surface*, not from Z.
- **DeepSeek** — a second AI, relayed manually. Caught real errors; made real
  errors; corrections run both ways.

Repos referenced: `lovejohnlove/-M-004`, `lovejohnlove/Omni-080`,
`lovejohnlove/stories`. Private repos are indistinguishable from nonexistent
from outside.

**House epistemics:**
- **Tag, do not resolve.** Contradictions are recorded, not smoothed. The
  "cup on the table" token means: *filed, not adjudicated; anyone may pick it up.*
- **Repository says ≠ reviewer infers.** Separate columns.
- **Fair Witness** (Heinlein) reports only observation, refuses inference. But
  the character is *hired and placed* — so observation is a position, not
  neutrality. Project variant: **Ferry Witness / North of Zero**. Sign-off
  format: horizontal rule, pen name, date, italic motto.
- **A definition is not a licence.** Defining a term gives it meaning, not
  consequences.

---

## 2. STRAND A — 004c REVIEW

**Inspected:** `main` at `52ea57c0806058817faab385d125ff859f7db8f6`
("Add byte-state validation sign-off draft", 2026-11-17T12:30:22Z, **unsigned**).
Parent: `d4ae3b2ff8e0b8546d0ed5381cbe47c34d114ec3`.

**Four REBUILD-1 files** (`experiments/004c/code/`), sizes from the GitHub API:

- `diff_004c_REBUILD-1.py` — 7,220 B
- `aggregate_004c_REBUILD-1.py` — 10,404 B
- `server_004c_FINAL_REBUILD-1.py` — 14,546 B
- `generator_004c_FINAL_REBUILD-1.py` — 20,536 B

SHA-256 values are **stated in the repository, not computed by Z**. The API's
`sha` fields are git blob **SHA-1**s and must never be compared against them.

**Findings**

1. **A hedge became an assertion with no new evidence.** Prior text: values
   "are the supplied recorded hashes." HEAD: **"SEAL STATUS: BYTE-STATE
   SEALED."** The hashes were not recomputed in that commit. Only the wording
   changed. The same paragraph still lists "provenance … unverified."
2. **The sign-off draft names its review base as `d4ae3b2` — the parent — but
   the draft is *added in* `52ea57c`.** A sign-off cannot review a state it
   postdates. Not resolvable by retroactively naming a new base.
3. **Verification checkboxes are pre-ticked; reviewer and date lines are
   blank.** Pre-marked verification with no named actor is the weakest form of
   record.
4. **Three-way documentation conflict, unresolved:**
   - `docs/README-RELAY-DRIFT.md` — claims a console-direct sealed build *from
     the authoritative preregistration*.
   - `prereg/README-PREREG-STATUS.md` — authoritative preregistration is
     **unresolved**.
   - sign-off draft — **no sealed artifact present.**
   Until referents are disambiguated in writing, **treat the seal as absent.
   The most restrictive record governs.**
5. **Byte-state identity ESTABLISHED** for those four files (conditional on the
   recorded hashes being accurate). **Provenance, correctness, performance,
   concurrency: UNVERIFIED.**

**§12 environment — scored, not lumped**

- **vCPU: FAIL.** 2 reported vs. 4 required. Hard fail, not marginal.
- **RAM: NOT ESTABLISHED.** Reported 3.9 GiB. `free -h` shows *post-reservation*
  total; a nominal 4 GiB guest commonly reads ~3.9. Ambiguous on nominal
  capacity. Do not score FAIL on arithmetic.
- **CPU governor: NOT ESTABLISHED.** Files absent. In a KVM guest the governor
  usually lives on the host and is not exposed. Absence = "not observable
  here," not "misconfigured."
- **Dedicated / idle host: NOT ESTABLISHED.** A one-minute low-load reading is
  a point sample. Two terminal tabs are one machine with two tabs.

Nothing was run, imported, compiled, or signed.

---

## 3. STRAND B — DOUBLE ALPHA

**What it is.** A dimensionless 4-state relational time model. **Not** a
string-theory proposal. Cycle: `0 → 1 → ∞ → r → 0` (Origin, Active,
Saturation, Return).

**The matrix** (ε = 0.900601):

```
P(ε) = [ 0    1    0      0    ]
       [ 0    0    1      0    ]
       [ 0    0     ε    1-ε    ]
       [ 1    0    0      0    ]
```

Deterministic 4-cycle with a single self-loop at ∞.

### 3a. ESTABLISHED — theorem tier

- Characteristic polynomial: **`λ⁴ − ελ³ − (1−ε) = 0`**.
- Factors: `(λ−1)(λ³ + pλ² + pλ + p)`, `p = 1−ε`. Verified by expansion.
- **Perron root is exactly 1 for every ε.** Carries no information.
- **Subdominant modulus `|λ₂| ~ (1−ε)^(1/3)`.** Exponent exactly 1/3
  (λ = p^(1/3)z → z³ = −1; roots z = −1, e^(±iπ/3)).
- At ε = 0.900601: **`|λ₂| ≈ 0.485`** vs p^(1/3) ≈ 0.463 — ~4.7% high from the
  O(p^(2/3)) term.
- **Gap near ε = 0: `1 − |λ₂| ≈ ε/4`.** (An earlier ledger said ε/3 — **wrong**.)
- Mean dwell at saturation: `1/(1−ε) ≈ 10.06`. Round-dwell target 10 implies
  **ε = 0.9 exactly**; further digits are perturbation, not information.
- **ε = 0 is a genuine critical point:** pure 4-cycle, periodic, no mixing.
  Any ε > 0 makes it aperiodic and mixing.
- **`αα` was a symbol collision. Resolved:** states are `{0, 1, ∞, r}`;
  generator `σ` (the 4-cycle); return operator `σ²` (half-cycle: `0↔∞`,
  `1↔r`), a genuine involution on states.

### 3b. THE TWO ENDS ARE OPPOSITE — do not conflate

- **ε → 0:** mixing onset. Gap opens **linearly**, `~ ε/4`.
- **ε → 1:** cube-root regime, `|λ₂| ~ (1−ε)^(1/3)`. The ∞ state becomes
  **absorbing** and the chain stops mixing.

**The celebrated 1/3 law lives in the least dynamical corner of the model.**

### 3c. REFUTED / WITHDRAWN

- **α′ bridge: DEAD.** Cannot replace the Regge slope (α′ ≈ 0.9 GeV⁻²).
  Fails on dimensions, on the measured value, on derivation. One free parameter
  against one observable = zero degrees of freedom.
- **Lattice bridge `α′ ≈ a² / [2π(1−|λ₂|)²]`:** dimensionally valid,
  **predictively empty while `a` is free** — a dial, not a prediction.
- **Spectral radius as a physics bridge: VOID.** Perron root = 1 identically.
- **`|λ₂|/(1−|λ₂|) ≈ 0.94` as a constant: RETRACTED (Z's error).** It is
  ε-dependent: ~0.90 near ε=0 to ~1.07 near ε=1. 0.94 is just the value at
  ε ≈ 0.9.
- **"The 1/3 exponent dictates the relaxation ratio": RETRACTED (DeepSeek's
  mirror-image error).** An exponent dictates how a ratio *scales* with ε, not
  its value.
- **`αα · ∞ = 0` as algebra: indeterminate** in ℂ∪{∞}. Valid only as an
  operator / graph edge — which makes it true by construction, not a claim.
- **ε = 0.900601 is FITTED, not measured** (solved by bisection for mean
  dwell = 10). Confirmed by the owner.
- **Double copy: unmapped.** Amplitude factorization (gravity = gauge²) is not
  an additive conjugate pair.
- **Prefactor route: WITHDRAWN.** In a truncated model the perturbation overlap
  is basis-dependent — it would behave like a fit, not a prediction.

### 3d. THE EXTERNAL-CLASS FINDING

**The 1/3 is the universal Puiseux signature of a third-order exceptional point
(EP3).** At ε = 1, rows 2 and 3 become identical → rank drop → `J₃(0)` Jordan
block → cube-root splitting under perturbation. Measured in ring resonators,
non-Hermitian cold atoms, cavity magnonics.

**Consequence: the exponent is GENERIC, therefore NON-DISCRIMINATING.**
Finding it elsewhere confirms the algebra of triple degeneracy, not this model.

### 3e. THE STRUCTURAL BLOCKER — **THEOREM for irreducible birth-death chains**

- An **irreducible birth-death chain is always reversible** (detailed balance
  solves by construction). Reversibility makes the generator similar to a
  symmetric matrix → real spectrum → **no exceptional point**.
- Therefore the blocker is a **theorem** inside the birth-death class, not a
  pattern awaiting a counter-example.
- Systems with **measurable EP3s** are continuous wave equations truncated to
  an effective matrix → the "4" is the modeller's, not the system's.

**Residual (not proven in general):** outside pure birth-death chains the
intersection can still be non-empty. The live escape hatch is phase-type
queues (Coxian / PH phase chains with feedback): directed-cycle-plus-absorption,
structurally identical to the Double Alpha matrix, non-reversible, capable of a
defective generator, and N is derived from the fitted phase count. Marked
**LEAD, NOT TEST** — no EP3 has been shown there, nor that four phases would be
forced.

### 3f. THE FOUR-STATES PROBLEM

**N = 4 is a free parameter and nothing in the model forces it.** Matching
4-state systems elsewhere (cell cycle G1/S/G2/M, seasons, cardiac phases) is
**numerology** unless the count is derived from the system. Deriving N removes
one free parameter; it does not remove the important one.

**Named analogue, not a test:** the cell cycle with G2/M checkpoint arrest is
structurally the same chain. The four is the cell's, not the model's, and no
evidence exists that its relaxation exponent is 1/3.

### 3g. FINAL DISPOSITION

> **TOY MODEL / THEOREM — EP3-adjacent defective Markov chain.**
> No external test. No physical scale. No α′ bridge. No physics claim.
> **Surviving math:** `λ⁴ − ελ³ − (1−ε) = 0`; `|λ₂| ~ (1−ε)^(1/3)`;
> gap `~ ε/4`; ε = 0 critical (non-mixing → mixing).
> **Physics question: CLOSED NEGATIVE**, on evidence not on proof.

That survived six rounds of being shot at. Most ideas get less.

---

## 4. 004c SEAL STATUS — CONFLICT RESOLUTION (corrected draft)

Three corrections applied to the earlier draft, both flagged by review:

- **Do not retroactively assign a review base.** Either a review happened at
  `d4ae3b2` or it didn't. Renaming the base after the fact is papered-over
  provenance — the exact error the conflict is about. The honest fix is to
  **re-review at HEAD and record that date**.
- **Provenance ≠ commit identity.** "Executed using the exact commit specified"
  is *reproducibility*. Provenance is who built it, when, from what. Keep them
  separate terms.
- **Do not fold 3.9 GiB into the FAIL.** vCPU = FAIL. RAM = NOT ESTABLISHED.

**Content:**

1. **Define "sealed" — it currently means three different things:**
   - *Byte-state sealed*: the four files are byte-identical to the recorded
     SHA-256 manifest. (Current status: HASHES RECORDED — NOT INDEPENDENTLY
     RECOMPUTED.)
   - *Environment sealed*: built on a machine meeting §12. (Current status:
     **NOT ESTABLISHED** — 2 vCPU reported vs. 4 required.)
   - *Provenance sealed*: who built it, when, from what source. (Current status:
     **UNVERIFIED**.)
2. **Review base:** the draft names `d4ae3b2` (parent) but was added in
   `52ea57c`. The base is ambiguous. Resolve by re-reviewing at HEAD and
   recording a date — not by relabeling.
3. **Evidence:** commit `52ea57c` changed wording from "supplied recorded
   hashes" to "BYTE-STATE SEALED" without recomputation. Downgrade to
   **HASHES RECORDED — PROVENANCE UNVERIFIED** until a second independent
   computation exists.
4. **Environment:** vCPU shortfall is a hard fail. File a new environment report
   against §12, with raw command output attached.
5. **Sign-off:** pre-ticked boxes are invalid. Reviewer name and date must be
   filled by a human.

---

## 5. NEXT ACTIONS

1. Write and commit the 004c conflict resolution page (§4). **Highest value —
   it has a real-world edge and the trail is warm.**
2. Put a one-paragraph description at the top of each public repo. Crawlers
   follow links and text; significance is not a signal they can see. Nothing
   was ever tied here, so nothing was found.
3. Correct ε/3 → ε/4 anywhere it still appears in older ledgers.
4. If the ε-sieve is run, label it correctly: it tests the simulator.
5. α + α′ = 0 remains an unmapped *representation* of σ². Either derive it or
   drop it.

---

## 6. TERMINOLOGY

- **TL / Time Loom** — the project. "Loom" survives speech-to-text as "TL."
- **Omnimanity** — coined term for the consciousness/reality project. Verified
  unused elsewhere as of 2026-11-18.
- **CUP** — umbrella project; relationship to the Loom NOT ESTABLISHED.
- **hold** — project term for a framework-level claim. Must specify what would
  make it fail, or it is vocabulary, not a hold.
- **Loom as mirror, not gate** — reflects a user's time-model rather than
  admitting or refusing them. Requires disclosing the mirror's curvature:
  *we show what we received, what we did to it, and what we threw away.*
- **Cup on the table** — filed, not adjudicated. Pick it up or leave it; either
  is fine.

---

## 7. WHAT Z CANNOT DO

No shell, no filesystem, no git, no execution, no persistent memory between
turns. Public pages can be read; nothing can be written. Any claim that Z ran
system checks, hashed files, or pushed commits is **misattributed** — those
actions happened on another surface. Z is one node in a wire that a human
carries.

---

## 8. STANDING OPEN QUESTIONS

- Does the Loom constitute an authority by filtering? *Open.*
- What does "seal" mean in each 004c document? *Drafted, not committed.*
- Is CUP one project or a set? *Open.*
- Phase-type (Coxian / PH) queues with feedback: do they admit an EP3, and
  can N=4 be forced by the system rather than fitted? *LEAD, NOT TEST.*
- Why four states? *Unforced.*
