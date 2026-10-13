# Sequence & Series worker — L01–L12 (12 PDFs / 496 pages)

**Assignment (Master OCR Allocation Plan):** the *"Current assistant"* block —
**Sequence & Series, Lectures 01–12, 12 PDFs / 496 pages**, plan branch `ocr/current-sequence-series`.
This session is pinned to `arena/02fffb3f-ocr`, so all work is committed here.

## ⛔ Status: BLOCKED — source PDFs not delivered

The 12 Sequence & Series PDFs are recorded in the master inventory as **"Current chat uploads"**.
Attachment metadata for all 12 files arrived in-session (twice), but **no file bytes reached the
sandbox**: `/home/user/uploads` does not exist and a full filesystem scan returns only the
**54 PDFs already in the repository**. Nothing Sequence & Series exists in any branch or in any
commit in repository history.

**No OCR has been run and no page content has been written.** Nothing in this folder is invented —
every content field is blank or explicitly marked pending.

## What *is* done (all of it real, none of it dependent on the missing files)

| Deliverable | State |
|---|---|
| **Source reconciliation** | ✅ all 12 files matched to the master inventory: filename, lecture, page count, expected SHA-256 |
| **`preregistration_manifest.json`** | ✅ 12 files / **496 pages** expected; per-file page counts + expected fingerprints + verification rules |
| **`page_audit.csv`** | ✅ **496 rows pre-registered** — one per *expected* page, so a gap is impossible once extraction starts (same practice Twin 1 documents) |
| **`tools/ocr_pipeline.py`** | ✅ written and **dry-run verified** — reports the 12 missing sources cleanly and exits; dual-pass PP-OCRv4 (200 dpi native + background-adapted); multi-location source lookup (repo root → `/home/user/uploads` → `--src`); automatic page-count and SHA-256 verification against the inventory |
| **`tools/make_qa_sheets.py`** | ✅ ready (2-up native-resolution contact sheets for visual QA, supports `--first/--last` for partial passes) |
| **`tools/build_deliverables.py`** | ✅ ready (merges raw OCR + QA notes into the standard handoff set, master-workbook column templates) |

## Expected scope (from the inventory, unverified until the files arrive)

| Lecture | Pages | Source filename |
|---|---:|---|
| Sequence & Series 01 | 44 | `Sequence and Series 01 Class Notes.pdf` |
| Sequence & Series 02 | 39 | `Sequence and Series 02 Class Notes.pdf` |
| Sequence & Series 03 | 43 | `Sequence and Series 03 Class Notes.pdf` |
| Sequence & Series 04 | 42 | `Sequence and Series 04 Class Notes.pdf` |
| Sequence & Series 05 | 40 | `Sequence and Series 05 Class Notes.pdf` |
| Sequence & Series 06 | 38 | `Sequence and Series 06 Class Notes.pdf` |
| Sequence & Series 07 | 41 | `Sequence and Series 07 Class Notes.pdf.pdf` |
| Sequence & Series 08 | 48 | `Sequence and Series 08 Class Notes Maths By Sachin Sir.pdf` |
| Sequence & Series 09 | 44 | `Sequence and Series 09 Class Notes.pdf.pdf` |
| Sequence & Series 10 | 35 | `Sequence and Series 10 Class Notes.pdf.pdf` |
| Sequence & Series 11 | 42 | `Sequence and Series 11 Class Notes.pdf.pdf` |
| Sequence & Series 12 | 40 | `Sequence and Series 12 Class Notes.pdf.pdf` |
| **Total** | **496** | |

## To unblock — any one of these

1. **Re-attach the PDFs** to the chat (a fresh attachment attempt).
2. **Commit them to the repository** (repo root, same as the other 54), then tell me — I pull and start.
3. **Give me a reachable URL** for the files (my network access is limited to GitHub/npm/PyPI hosts).

The moment a source appears, verification and extraction start with **zero setup cost**:

```bash
# verifies page count + SHA-256 against the inventory, then runs dual pass over every page
python tools/ocr_pipeline.py --work /home/user/ocr_work --workers 2 --src /path/to/pdfs
python tools/make_qa_sheets.py --slug sequence-series-L01 --pdf "Sequence and Series 01 Class Notes.pdf"
python tools/build_deliverables.py
```

## Method (as specified by the plan, applied unchanged)

1. **Extraction** — every page, no sampling. Pass A native @200 dpi; Pass B background-adapted
   (inverted for dark slides, CLAHE otherwise). Primary pass = higher summed line confidence; both
   passes retained; `pass_agreement` recorded per page.
2. **Verification before extraction** — page count and SHA-256 of each delivered file are checked
   against `preregistration_manifest.json`. A mismatch is printed and recorded, never silently accepted.
3. **Visual QA** — 2-up native-resolution contact sheets read page by page; high-dpi zoom crops used
   for handwriting ambiguities; results written per page and tiered (`visual-full` / `visual-scan` /
   `auto-QA (dual-pass)`), so coverage is always explicit.
4. **No silent corrections** — source typos and instructor board errors are transcribed verbatim with
   `[sic]`/`[UNCLEAR]` + page and location.
5. **DIBY** — exact printed label, verbatim prompt, options, visible answer; internal ID **only** where
   the source prints no label.

Raw records, contact sheets and scratch stay under `/home/user/ocr_work/` (outside the repo); only the
handoff files are committed.
