# Independent OCR cross-check — Permutations & Combinations L05–L11 + Quadratic Equations L01–L08

**What this is:** an *independent second machine pass plus visual QA* over the block that worker
**Twin 2** (`arena/596a30d9-ocr`) already delivered as machine OCR only — P&C L05–L11 + QE L01–L08,
15 PDFs / 536 pages. It is **not** Twin 2's handoff and does not replace it; Twin 2's handoff is
merged in `main` at `ocr-output/twin-2/`.

This layer exists because Twin 2's README states "No manual review performed" and "does not claim
completion of the allocation plan's visual QA or faithful math/diagram transcription standards".
An independent pass with a different render scale gives the coordinator (a) a disagreement signal
for prioritising QA, and (b) verified transcripts where QA has been done.

This session is pinned to `arena/02fffb3f-ocr`. No other worker's folder is touched.

Page counts were verified against the master inventory before work started — **all 15 files match
exactly (536/536)**; SHA-256 per source file is recorded in every transcript header.

## Relationship to Twin 2's merged machine-OCR handoff

A separate session (`arena/596a30d9-ocr`) has pushed a **machine-only** Twin 2 handoff at
`ocr-output/twin-2/` (536/536 pages, "no manual review performed", per its own README). That
handoff explicitly does **not** claim the plan's visual-QA or faithful-transcription standard.

This folder is the complementary layer:

| | `ocr-output/twin-2/` (worker Twin 2, merged) | this folder (cross-check) |
|---|---|---|
| Machine OCR | ✅ single pass, 1.5× render (1920×1080) | ✅ **dual pass** @200 dpi (native + background-adapted), pass-agreement recorded |
| Visual QA | not performed (declared) | ✅ page-by-page visual verification, `visual-full` / `visual-scan` per page |
| DIBY | marker *candidates* only, labels not identified | printed label + verbatim prompt + options + printed answer per item |
| Verified transcripts | none | `transcripts/*.md` (verified text + raw OCR side by side) |
| Uncertainty | candidate list | page + location entries incl. source-vs-work discrepancies |

**Independent cross-check:** because the two sessions used different render scales and passes, the
two machine outputs can be diffed. On the 8 lectures both have processed, normalised text
similarity averages 0.71–0.85, and **42 pages score below 0.50** — i.e. a large fraction of
handwriting-heavy pages are *not* reliably readable by either machine pass alone. That is the
evidence base for the visual-QA layer, and it is how pages are prioritised for review.

## Status (live)

| Lecture | Pages | Machine extraction (dual-pass) | Visual QA |
|---|---:|---|---|
| Permutations & Combinations 05 | 32 | ✅ 32/32 | ✅ **32/32 visual-full** |
| Permutations & Combinations 06 | 43 | ✅ 43/43 | ✅ **43/43 visual-full** |
| Permutations & Combinations 07 | 42 | ✅ 42/42 | pending |
| Permutations & Combinations 08 | 45 | ✅ 45/45 | pending |
| Permutations & Combinations 09 | 34 | ✅ 34/34 | pending |
| Permutations & Combinations 10 | 37 | ✅ 37/37 | pending |
| Permutations & Combinations 11 | 45 | ✅ 45/45 | pending |
| Quadratic Equations 01–08 | 258 | in progress | pending |
| **Total** | **536** | — | **75/536 = 14.0 %** |

## Contents

| File | Purpose |
|---|---|
| `transcripts/<slug>.md` | page-by-page: verified transcript (where reviewed) + verbatim raw OCR of the primary pass, `[LOWCONF]` flags, `[UNCLEAR]` markers, dual-pass disagreement notes |
| `page_audit.csv` | one row per PDF page (template: Chapter, Lecture, Source PDF, page, heading, text, diagram notes, DIBY present, labels, uncertainty/location, visual-QA status, reviewer) |
| `diby_index.csv` | one row per DIBY item (marker, exact printed label, internal ID only if none printed, verbatim prompt, options, printed answer, uncertainty, QA status) |
| `uncertainty_log.md` | every `[UNCLEAR]` / low-confidence / dual-pass-disagreement / source-discrepancy entry with page + location |
| `qa_notes/<slug>.json` | manual visual-QA provenance per page (topic, page type, verified text, diagram notes, DIBY rows, issues) |
| `tools/ocr_pipeline.py` | dual-pass PP-OCRv4 (RapidOCR/onnxruntime) extraction over every page, no sampling |
| `tools/make_qa_sheets.py` | 2-up native-resolution contact sheets used for manual visual QA |
| `tools/build_deliverables.py` | merges raw OCR + QA notes into the handoff files above |

## Method

1. **Extraction** — every page rendered at 200 dpi; **Pass A** native, **Pass B** background-adapted
   (inverted for dark slides, CLAHE otherwise). Primary pass = higher summed line confidence; both
   passes stored; `pass_agreement` (normalised sequence ratio) recorded. Source PDFs are read-only.
2. **Visual QA** — 2-up native-resolution contact sheets, read page by page against the source;
   340–500 dpi zoom crops used whenever handwriting is ambiguous. Findings recorded in
   `qa_notes/<slug>.json` and marked `visual-full` in the audit.
3. **No silent corrections** — source typos and instructor board errors are transcribed verbatim and
   flagged (e.g. P&C L05 p15's `231 - (10+6+21+15) = 183`; P&C L06 p7's `= n²m²`; L06 p35's option
   `5!4!3!2!` for a three-subject split; L06 p38's printed placeholder answer `[Ans. : (......)]`).

## Known discrepancies / flags for the coordinator

- **P&C L05 p24** (IIT-JEE-2005) is marked H.W. on the slide with no in-class answer; the answer `(D) m²n²`
  is ticked on **L06 p7** during the H.W. discussion — the two pages are cross-referenced.
- **P&C L06 p3** prints the recap formula as `nC3 - (n² - 3n)` while **L05 p16** prints `nC3 - (n(n-4) + n)`.
  Both are transcribed as printed; the algebraic forms agree, the printed forms do not.
- **P&C L06 p15** carries an unresolved factor reading (`6C4` vs `5C5` variant lines) — logged, not reconciled.
- **P&C L06 p22** shows `31 x 31` glyphs where `3! x 3!` is meant — transcribed as drawn, arithmetic
  (`216 + 108 = 324`) noted but not applied to the glyph.
- **P&C L06 p23** is a board *rework* page with no stem and no printed label; its association with the
  L05 shoes question is inferred and flagged as such.
- **P&C L06 pp30, 32, 33** are marked H.W. on the slides; answers are not worked in class.

## Re-run

```bash
python3 -m venv /home/user/ocr_work/.venv && . /home/user/ocr_work/.venv/bin/activate
pip install pymupdf pillow numpy rapidocr_onnxruntime
pip uninstall -y opencv-python && pip install --force-reinstall opencv-python-headless
python tools/ocr_pipeline.py --work /home/user/ocr_work --workers 2
python tools/make_qa_sheets.py --slug <slug> --pdf "<source filename>"
python tools/build_deliverables.py
```

Raw page records, contact sheets and scratch live under `/home/user/ocr_work/` **outside the repo**;
only the handoff files above are committed.
