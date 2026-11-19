# Report File Hash Baseline

This file records the SHA-256 hashes of the five report files in this
workbench. The 12 recovered source files have their hashes recorded in
`WORKBENCH_REPORT.md` and in the conversation history; this file provides the
analogous baseline for the report files themselves, so that any future
modification can be detected.

**These are classical synthetic software model reports.** Not physical
validation. Not quantum. Not 004c. No license has been assigned to this
workbench; the story license (if any) does not apply.

## Report hashes

| File | SHA-256 | Bytes |
|---|---|---:|
| `noise-board-sim/REPORT.md` | `4c985ae9368abe255fa6b6bd4b0d0e9f1b9af53a8b02ab88bd3fe81f83fbaaee` | 4,001 |
| `noise-board-afe-v2/REPORT.md` | `b46f2048b0f28b96a0605d9aff6af406130a3d2b18843ada2f9b4aa1d5a42df4` | 5,955 |
| `noise-board-afe-v2-comparison/REPORT.md` | `2f0ea6eaa0a351ab471f4bfdb91b38a2b0e1423ccd7f3b5ca917e174221dca2d` | 6,910 |
| `WORKBENCH_REPORT.md` | `2e1a7416c4aff5f6794feef3d6c7f61c32bc2528dc31d516c97610456ff7c132` | 6,724 |
| `ENVIRONMENT_REPORT.md` | `0e3dc6beb37616485a03a58f5675f7c3680d45ebfc74fbe9b152f9ea1203016a` | 2,770 |

## Verification command

```sh
cd workbench/noise-board
sha256sum noise-board-sim/REPORT.md \
         noise-board-afe-v2/REPORT.md \
         noise-board-afe-v2-comparison/REPORT.md \
         WORKBENCH_REPORT.md \
         ENVIRONMENT_REPORT.md
```

Compare the output to the values listed above. A mismatch means the report
has been modified since this baseline was written.
