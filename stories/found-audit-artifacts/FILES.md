# File list and provenance

**Proposed destination:** `lovejohnlove/Omnimanity-/stories/found-audit-artifacts/`

The first proposed public bundle contains the README, this file list, and these two raw Drive V5 script snapshots. Archive paths use clean `.py` filenames; the original Drive titles are preserved below.

| Proposed archive path | Original Drive title | Size | Raw SHA-256 | What it does / evidence status |
|---|---|---:|---|---|
| `code/drive-v5/dual_anchor_audit_harness.py` | `dual_anchor_audit_harness.py - PLAIN - V5 EDITED` | 1,744 bytes | `2b81993342e2b6c4fefdef59f9dbb89c7d5e23f768822a4bc651cb521cc3ab89` | Compares two supplied series point by point within a tolerance and optionally checks range equality. The included example compares identical synthetic lists. The hash matches the Drive V5 expected value; its `VERIFIED` output is only the function’s result for the supplied inputs, not an empirical claim. |
| `code/drive-v5/prereg_harness_s3_verbatim_FIXED.py` | `prereg_harness_s3_verbatim_FIXED.py - PLAIN - V5` | 1,271 bytes | `a14f1c5fe0b373370925c760ccde4c4aff7313ab5a42d295e6c185c0abf14e7f` | Applies a three-boolean `SUPPORTED`/`FALSIFIED`/`PARTIAL` decision rule and demonstrates it with generated regression data. The hash matches the Drive V5 expected value; this is a later, smaller V5 snapshot, not the missing 7,895-byte original. |

Both files are byte-for-byte copies of the raw Drive “PLAIN” files. The hashes were computed from the downloaded bytes and checked against the Drive V5 expected-hash record. They establish byte identity only—not authorship, canonical status, or scientific validity.

The review draft also contains `README.md` (the explanatory note) and this `FILES.md`. Neither is a source artifact. No other code, manifests, closure reports, or data files are proposed for this first public bundle.
