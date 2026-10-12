# Twin 3 OCR Deliverables — Quadratic Equations L09–L14 + Trigonometric Equation L01–L07

Worker: **Twin 3** (Master OCR Allocation Plan, `project-admin/`).
Assignment: 13 PDFs / 544 pages — Quadratic Equations Lectures 09–14 (6 PDFs / 235 pp),
Trigonometric Equation Lectures 01–07 (7 PDFs / 309 pp).

> **Branch note:** the allocation plan names branch `ocr/twin-3-quadratic09-14-trigeq`, but this
> Arena session is pinned to `arena/052fa64f-ocr`; all Twin-3 work is committed here and this
> folder is the Twin-3 handoff. No other worker's folder is touched.

## Contents

| File | Purpose |
|---|---|
| `transcripts/<slug>.md` | Page-by-page transcript per lecture: verified transcript (where visual QA done) + verbatim raw OCR of the primary pass, `[LOWCONF]` flags, diagram notes, `[UNCLEAR]` markers |
| `page_audit.csv` | One row per PDF page (all 544), template fields from `PDF_Inventory_and_Worker_Assignments.xlsx` → *Page Audit Template* |
| `diby_index.csv` | One row per DIBY item, template fields from *DIBY Index Template* |
| `uncertainty_log.md` | Every `[UNCLEAR]` / low-confidence (<0.65) / dual-pass-disagreement entry with page + location; nothing silently corrected |
| `qa_notes/<slug>.json` | Manual visual-QA record per page (provenance for verified transcripts) |
| `tools/ocr_pipeline.py` | Dual-pass PP-OCRv4 (RapidOCR/onnxruntime) extraction over every page, no sampling |
| `tools/make_qa_sheets.py` | 2-up native-resolution contact sheets used for manual visual QA |
| `tools/build_deliverables.py` | Merges raw OCR + QA notes into the handoff files above |

## Method

1. **Extraction** — every page rendered at 200 dpi; **Pass A** native, **Pass B**
   background-adapted (inverted for dark slides, CLAHE otherwise). Primary pass = higher
   confidence score; both passes stored; `pass_agreement` (normalised sequence ratio) recorded.
   Source PDFs are read-only; SHA-256 per file recorded in each transcript header.
2. **Manual visual QA** — agent reviews 2-up native-res contact sheets page by page against the
   OCR, writes `qa_notes/<slug>.json` (topic, page type, verified text, diagram notes, DIBY
   items, `[UNCLEAR]` issues). Pages with QA notes are marked `visual-full` in the audit;
   pages not yet reviewed are marked `auto-QA (dual-pass)` — **the audit always tells you which**.
3. **No silent corrections** — source typos (e.g. `y = ax² + bc + c` on QE-L09 p29/p31) are
   transcribed verbatim with `[sic]`; ambiguous glyphs get `[UNCLEAR]` + candidate readings.

## Coverage / reconciliation (live — rebuilt by `tools/build_deliverables.py`)

| Lecture | Pages expected | Pages extracted | Visual QA |
|---|---|---|---|
| Quadratic Equations 09 | 34 | 34 | ✅ all 34 pages |
| Quadratic Equations 10 | 44 | 44 | in progress |
| Quadratic Equations 11 | 39 | 39 | pending |
| Quadratic Equations 12 | 40 | 40 | pending |
| Quadratic Equations 13 | 36 | 36 | pending |
| Quadratic Equations 14 | 42 | 42 | pending |
| Trigonometric Equation 01 | 53 | — | pending |
| Trigonometric Equation 02 | 41 | — | pending |
| Trigonometric Equation 03 | 38 | — | pending |
| Trigonometric Equation 04 | 41 | — | pending |
| Trigonometric Equation 05 | 46 | — | pending |
| Trigonometric Equation 06 | 40 | — | pending |
| Trigonometric Equation 07 | 50 | — | pending |

## Re-run

```bash
python3 -m venv /home/user/ocr_work/venv && . /home/user/ocr_work/venv/bin/activate
pip install pymupdf pillow numpy rapidocr_onnxruntime opencv-python-headless
python tools/ocr_pipeline.py --work /home/user/ocr_work --workers 2
python tools/make_qa_sheets.py --slug <slug> --pdf "<source filename>"
python tools/build_deliverables.py
```
