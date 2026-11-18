# CUP Rev1.1 — documentation-only hardware packet

**Review status: documentation only. These are Drive-rendered text/design records—not native KiCad CAD, not complete fabrication files, not fabrication-authorized, and not verified physical-board results.**

This folder contains four read-only text exports from the Google Drive folder `Omnimanity CUP - Hybrid p-bit Coprocessor Module`, plus an export-hash manifest. The exports are not the original Drive file bytes. The `Drive-export payload` SHA-256 values below identify the exact bytes returned by Google Drive's export operation (`text/csv` or `text/plain`); they do not hash the underlying native Google Sheet or Doc. The separate packaged-file hashes in [`drive-text-exports/EXPORT_HASHES.md`](drive-text-exports/EXPORT_HASHES.md) include the review warning headers. Neither hash type validates the design.

The exports were retrieved on `2026-11-18`. Source dates below are only those visible in the exported content; absence of a visible source date does not establish when a record was created or last modified. Google Docs styling, comments, suggestions, revision history, and Google Sheets styling/metadata are not represented in these text exports.

## Design recorded here

The intended signal path is a Zener-noise source (`D1`, 1N4732A) coupled through `C1` into a `TLV9062` gain stage (`R2=1 kΩ`, `R3=47 kΩ`, nominal gain 47), with a 1.65 V buffered reference (`R4/R5=10 kΩ`, `R7=0 Ω`), then a `1 kΩ`/`750 pF` anti-alias network and clamp into Pico 2 / RP2350 `GP26` ADC input. The notes specify 500 kS/s sampling. The baseline also records a ferrite bead between `3V3_RAW` and `3V3_A`, 10 µF bulk and 100 nF high-frequency decoupling on the analog island, and a four-layer, 1.6 mm FR4 stackup with solid L2 ground, HASL default, and 0.5 oz inner / 1 oz outer copper.

These are **design intentions from the records**, not verified board behavior. The BOM labels white/pink Zener-noise behavior as an assumption. The requested FB1 attenuation is greater than 40 dB over 500 kHz–2 MHz, but the bead's `600 Ω @ 100 MHz` rating alone does not establish that result. The notes require measurement at `3V3_RAW` and `3V3_A`; those physical bench results are pending.

## Source records, provenance, and status

| Exact Google Drive source title | Drive source ID | Source date shown in text | Export and payload SHA-256 | Source status / caveat |
|---|---|---|---|---|
| `CUP_BOM_Rev1.1_Frozen_Corrected.csv - FINAL BUILD BOM` | `1HwCC6zO-CYaqh6RSbl47pdXCVpQ2X-tNiHxeYf4953I` | No date visible in the exported sheet data | One-tab Google Sheet exported as `text/csv`; `6ecb7ab088fbbfd0df64682787e8f047e3a4c2faed4ecee637c6bff9cb4f241a` | The title says “FINAL BUILD BOM” and many rows say “Frozen,” but D1's noise-source behavior is explicitly an assumption and the build notes leave its bias decision pending. FB1's >40 dB attenuation remains physically unvalidated. Do not treat the title as fabrication approval. |
| `CUP_Rev1.1_Frozen.kicad_sch - KiCad Schematic Skeleton - TEXT` | `1zJIWFsJ9EIOX4zT_Whp7R8KhMnvVYzYWizsXvJay7EA` | No date visible in the exported text | Google Doc exported as `text/plain`; `18d8da7183aee555510b0666f019680ed41a8f73b326252276d75748a271b724` | A text skeleton with schematic-like declarations; it is not a native `.kicad_sch` file and is not verified as a complete schematic. |
| `CUP_Rev1.1_Fabrication_Build_Notes.md - DESIGN-COMMITTED FAB BLOCKED with review observations` | `1ohGJf1kDnaYcFCQ0XqMcjhPAUdpgTgrbtHJjed9A-Es` | `2026-10-28` | Google Doc exported as `text/plain`; `80c5ceac6639bcc8671e5f8153ce42211329fbc1c79ef2b34a612efcbe0c9b68` | Source status: **DESIGN-COMMITTED / FABRICATION RELEASE BLOCKED**. It says the document does not close the four gates or authorize fabrication. D1 bias, FB1 attenuation, KiCad layout/clearance/return paths, firmware integration, LUT contents, and physical bench validation remain open or pending. |
| `CUP_Rev1.1_Component_Reconciliation_Note.md` | `1Ur6W-kqjmjKL4mgm_daFhpKUhQj440RhNvxy96pkey4` | `2026-10-28` | Google Doc exported as `text/plain`; `91e267d1a6fc0fda75faa3c95a275864737c4f4abb83beac7d183e500cbe29cd` | Reconciles the concept image against the design baseline and says the image is non-authoritative. White/pink noise controls are unmeasured assumptions; LUT-dependent validation remains pending. |

The BOM export contains one sheet, and its CSV export does not preserve styling, comments, or other spreadsheet metadata. Plain-text Doc exports do not preserve the original Google Docs styling, comments, suggestions, or revision history. The hashes identify export output bytes, not the original Drive-stored documents.

## Release boundary and missing files

The Drive folder search found no native `.kicad_pcb` or `.kicad_pro` project, Gerber or drill files, or complete native KiCad design package. The `.kicad_sch`-named record is a Google Doc text export, not a native CAD source. The source notes also leave the Zener bias choice, measured FB1 attenuation over 500 kHz–2 MHz, layout and return-path review, firmware compile/flash/integration, calibration LUT contents, and physical bench validation unresolved. A documented or simulated result must not be represented as a verified result from a physical board.

## License and attribution

The documentation-only CUP Rev1.1 packet in this directory—including these Drive-derived text exports, this README, and its metadata—is offered under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. See [`LICENSE.md`](LICENSE.md) and <https://creativecommons.org/licenses/by/4.0/>. Suggested attribution: `lovejohnlove, CUP Rev1.1 documentation-only packet`.

This license applies **only** to `hardware/CUP-Rev1.1/`. It does not relicense `stories/`, the repository's existing stories, or any other pre-existing project materials. No claim is made here that this packet is a native or buildable hardware design. The repository root README is intentionally unchanged and does not advertise this packet.