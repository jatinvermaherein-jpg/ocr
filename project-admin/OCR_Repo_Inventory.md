# OCR Repository Inventory — what exists, where it is, and what state it's in

**Audited:** 2026-10-13 · **Repo:** `jatinvermaherein-jpg/ocr` @ `main` / `arena/4e1fafa6`-series working branch
**Method:** full file-tree walk + re-computed counts from the source artifacts themselves (CSV/JSON parsed, not copied from READMEs). PDF page counts re-verified with PyMuPDF at audit time.

---

## 1. Headline numbers

| Item | Value | Verified how |
|---|---|---|
| Source PDFs in repo root | **66** | `ls *.pdf` |
| Total source pages | **2,624** | PyMuPDF `page_count` on all 66 files |
| OCR workstreams | **5** (Current-assistant S&S + Twin 1–4) | master allocation plan |
| Pages with a page-audit row | **2,128 / 2,128** of the twin-scope pages | 508 + 536 + 544 + 540 CSV rows |
| Pages visually verified | **767** (508 Twin 1 + 259 Twin 3) | audit `visual_qa_status` / `qa_notes` |
| Pages machine-OCR'd only | **1,361** (536 Twin 2 + 540 Twin 4 + 285 Twin 3) | audit status columns |
| DIBY items captured | **721** rows across 4 registers (143 + 242 + 164 + 172) | CSV row counts |
| Uncertainty entries logged | **3,950** across all logs | CSV/MD entry counts |
| JSON/JSONL machine reports | **27 JSON + 536 JSONL page records** | `find` + parse |

The 12 Sequence & Series PDFs (496 pp) that the master plan listed as "current chat uploads" are **now present in the repo root** — the corpus is complete at 66/66, 2,624/2,624 pages. (Twin 1's log item F-05 tracking the "missing 55th PDF" is therefore superseded: nothing is missing from the tree; only the *Sequence & Series* workstream has no committed output here — see §3.)

---

## 2. Source corpus (verified page counts)

| Chapter | PDFs | Pages | Assigned to |
|---|---:|---:|---|
| Binomial Theorem (L01–L09) | 9 | 344 | Twin 1 |
| Permutations & Combinations (L01–L11) | 11 | 442 | Twin 1 (L01–04), Twin 2 (L05–11) |
| Quadratic Equations (L01–L14) | 14 | 493 | Twin 2 (L01–08), Twin 3 (L09–14) |
| Trigonometric Equation (L01–L07) | 7 | 309 | Twin 3 |
| Trigonometric Functions (L01–L13) | 13 | 540 | Twin 4 |
| Sequence and Series (L01–L12) | 12 | 496 | Current assistant (no output in repo) |
| **Total** | **66** | **2,624** | |

---

## 3. Workstream status

### Twin 1 — Binomial Theorem L01–09 + P&C L01–04 · **COMPLETE (highest fidelity)**
13 PDFs / 508 pp · folder `deliverables/twin-1/`
- 508/508 audit rows marked **QA-PASSED** (visual transcription from rendered pages; source PDFs have no text layer — log item F-01).
- 13 Markdown transcripts **+ 13 matching DOCX exports**.
- DIBY register: **143** physical-item rows with verbatim prompts, options, printed labels.
- Uncertainty log: **11** numbered open/resolved items (U-01…U-11) + 5 structural findings (F-01…F-05).
- Machine ledger: `page-audit/progress.json` (per-lecture reviewed/total), `page-audit/scope_manifest.json` (13 files, expected vs actual page counts, SHA-256 each), 13 `qabatch_*.json` per-page QA batches, `diby/diby_rows.json`.

### Twin 2 — P&C L05–11 + Quadratic L01–08 · **AUTOMATED OCR ONLY (no review)**
15 PDFs / 536 pp · folder `ocr-output/twin-2/`
- 536/536 pages OCR'd; **0** manually reviewed, by explicit user instruction.
- 10,713 recognised lines · 130,609 characters · 2,807 low-confidence lines (< 0.80) · 0 pages with no text.
- 242 DIBY **candidate** hits on 30 distinct pages — markers only, prompts/options/answers **not** extracted (`prompt_options_answer_status` = `not_identified_automatically`).
- Engine: RapidOCR ONNX Runtime 1.4.4, PP-OCRv4 det+rec, 1.5× render (~1920×1080), CPU.
- `completion_summary.json` self-declares status `automated_ocr_complete_unreviewed`.

### Twin 3 — Quadratic L09–14 + Trigonometric Equation L01–07 · **IN PROGRESS (extraction done, QA 48%)**
13 PDFs / 544 pp · folder `deliverables/twin-3-quadratic09-14-trigeq/`
- 544/544 pages extracted (dual-pass PP-OCRv4, pass-agreement recorded) and 544/544 audit rows populated.
- Visual QA: **259 / 544 pages** documented in `qa_notes/` → audit shows `visual-full` 162 + `visual-scan` 97 + `auto-QA (dual-pass)` 285.
- Per-lecture QA coverage: QE L09 34/34, L10 44/44, L11 39/39, L12 40/40, L13 36/36, L14 42/42, **TrEq L01 24/53** — TrEq L02–L07 extraction present, QA pending.
- DIBY index: 164 rows · uncertainty log: **393** cited entries (incl. source typos transcribed verbatim with `[sic]`).
- 13 transcripts written; header notes this session is pinned to `arena/052fa64f-ocr` rather than the plan's branch name.

### Twin 4 — Trigonometric Functions L01–13 · **EXTRACTION ONLY (0 pages verified)**
13 PDFs / 540 pp · folder `deliverables/twin-4-trigonometric-functions/`
- 540/540 audit rows; all 540 carry status `NOT VISUALLY VERIFIED — machine OCR draft only`.
- DIBY index: 172 rows (markers found by OCR; prompts/answers not yet extracted) · uncertainty log: 203 rows (mostly "low mean OCR confidence" page-level flags).
- 1 transcript for all 13 lectures.
- **Known discrepancy:** OCR headings in `Trigonometric Functions 01` pp. 2–33 & 41–49 look like Exponential/Logarithmic Series and inequality material; trig headings only on pp. 34–40. Flagged, not corrected (see its `uncertainty_log.csv`).

### Current assistant — Sequence & Series L01–12 · **NO OUTPUT IN THIS CHECKOUT**
12 PDFs / 496 pp are present at the repo root, but there is no `deliverables/` or `ocr-output/` folder for them. The plan assigns them to `ocr/current-sequence-series`; nothing has landed on this branch/main yet.

---

## 4. Directory map (where everything lives)

```
ocr/
├── *.pdf                                  66 source PDFs / 2,624 pp  (read-only, never modified)
├── project-admin/                         coordinator layer
│   ├── Master_OCR_Allocation_Plan.md/.docx   scope, worker split, shared standard
│   ├── PDF_Inventory_and_Worker_Assignments.xlsx   inventory + audit/DIBY templates
│   ├── Twin_2_OCR_Assignment.json         Twin 2 scope handed to that worker
│   ├── OCR_Repo_Inventory.md / .json      ← THIS AUDIT
├── tools/                                 shared pipeline scripts (9 files + requirements)
├── deliverables/
│   ├── DIBY_Master.md/.csv/.json/.docx   ← consolidated DIBY register (all 721 items, all workers)
│   ├── twin-1/            transcripts(.md+.docx) · page-audit/ · diby/ · uncertainty/
│   ├── twin-3-.../        transcripts/ · page_audit.csv · diby_index.csv · qa_notes/ · uncertainty_log.md · tools/
│   └── twin-4-.../        transcript.md · page_audit.csv · diby_index.csv · uncertainty_log.csv
└── ocr-output/twin-2/     Twin_2_OCR.md/.txt · Page_Audit.csv · DIBY_Candidates.* ·
                           Uncertainty_Log.csv · records/*.jsonl · transcripts/*.md+.txt ·
                           progress.json · completion_summary.json · run_manifest.json
```

---

## 5. Every JSON / machine-readable report (the "summary JSON" layer)

| File | What it holds | Key numbers |
|---|---|---|
| `ocr-output/twin-2/completion_summary.json` | Twin 2 completion certificate | 15 files, 536 pages, 10,713 lines, 130,609 chars, 2,807 low-conf, 242 DIBY candidates, status `automated_ocr_complete_unreviewed` |
| `ocr-output/twin-2/run_manifest.json` | Frozen run provenance | 15 docs × SHA-256 + full engine config (model names, render scale, detector thresholds) + start time |
| `ocr-output/twin-2/progress.json` | Resumable ledger | per-document expected/saved/processed pages, `complete: true` |
| `ocr-output/twin-2/records/*.jsonl` | **536 page records** — text, per-line scores, bounding boxes, render size, timing, embedded-text chars | one JSON object per PDF page |
| `project-admin/Twin_2_OCR_Assignment.json` | Twin 2 scope as handed over | 15 docs / 536 pp |
| `deliverables/twin-1/page-audit/scope_manifest.json` | Twin 1 scope + integrity | 13 files, 508 pp, `inventory_mismatches: []`, SHA-256 each, transcript path each |
| `deliverables/twin-1/page-audit/progress.json` | Twin 1 completion ledger | `pages_reviewed 508 / pages_total 508`, per-lecture split |
| `deliverables/twin-1/page-audit/qabatch_bt01…bt09, pc01…pc04.json` | **13 per-lecture QA batches** — one dict per page (heading, printed/handwriting capture, DIBY flags, uncertainty count, QA status, reviewer) | 508 page dicts total |
| `deliverables/twin-1/diby/diby_rows.json` | Twin 1 DIBY register as JSON | 143 items |
| `deliverables/twin-3-.../qa_notes/*.json` | **7 per-lecture visual-QA records** (slug, chapter, lecture, source, reviewer, per-page verified text / diagram notes / DIBY / `[UNCLEAR]`) | 259 page records: QE L09–L14 (34, 44, 39, 40, 36, 42) + TrEq L01 (24) |

CSV companions (not JSON but part of the same reporting layer): `Page_Audit.csv` (536 rows), `DIBY_Candidates.csv` (242 rows), `Uncertainty_Log.csv` (3,343 rows = 536 unreviewed + 2,807 low-confidence lines), `page_audit_twin1.csv` (508), `diby_index_twin1.csv` (143), `page_audit.csv` twin-3 (544) / twin-4 (540), `diby_index.csv` twin-3 (164) / twin-4 (172), `uncertainty_log.csv` twin-4 (203).

---

## 5b. Consolidated outputs

| File | What it holds |
|---|---|
| `deliverables/DIBY_Master.md` | **One document with every DIBY item in the repository** (721 items, chapter → lecture → page order), each badged by transcription quality, with lecture index and appendices for unverified / unnumbered items |
| `deliverables/DIBY_Master.csv` / `.json` | The same 721 records in machine-readable form (one row/object per item) |
| `deliverables/DIBY_Master.docx` | Word export of the master document |
| `deliverables/DIBY_Questions.docx` | **Question bank in the requested layout** — 655 questions (section markers excluded), one title per chapter+lecture, DIBY tag, italic question with **typeset Word equations**, options, right-aligned answer. Compact density (A4, 1.5 cm side / 1.3 cm vertical margins, 0.95 line spacing, no spacer paragraphs) — ≈42 pages by model estimate vs ≈65 for the earlier spacing, same content. **Each chapter starts on an odd page** (Word `oddPage` section breaks); page numbers in the footer |
| `deliverables/DIBY_Questions.csv` | The same 655 questions in document order, machine-readable |
| `tools/build_diby_master.py` | Builds all four from the four worker registers; for Twin 2/Twin 4 (no prompts extracted) it reconstructs draft question text from those workers' own raw page OCR, delimited by the next marker, and labels it unverified |
| `tools/build_diby_docx_v2.py` | Builds the question-bank DOCX (current layout). Maths is converted to LaTeX and rendered as native Word equations (OMML) through pandoc |
| `tools/ocr_math_to_latex.py` | OCR maths → LaTeX converter (superscripts, subscripts, fractions, roots, Greek/operators). Conservative: anything it is unsure of stays plain text |
| `tools/build_diby_docx.py` | Earlier question-bank DOCX builder (Question/Options/Answer/Tag/Source block layout with marker appendix) — superseded by `build_diby_docx_v2.py` |

Coverage of the master document: 195 verified · 112 ocr-extract · 348 ocr-draft · 66 marker-only (655 items carry question text).

## 6. Shared tooling

| Script | Role |
|---|---|
| `tools/ocr_twin2.py` | Resumable CPU OCR of all Twin-2 pages (checkpoints under gitignored `.work/`) |
| `tools/package_twin2_ocr.py` | Builds the Twin-2 audit/DIBY/uncertainty/summary bundle from JSONL records |
| `tools/render_pages.py` | Renders PDF pages to PNG (outside the repo) for visual transcription |
| `tools/twin1_scope.py` | Twin 1 scope as code — single source of truth |
| `tools/init_audit.py` | Pre-registers one audit row per expected page + SHA-256; verifies page counts |
| `tools/add_qa.py` / `tools/merge_qa.py` | Append per-page QA rows; merge batches into master audit + DIBY index + progress |
| `tools/md_to_docx.py` | Markdown transcript → DOCX export |
| `deliverables/twin-3-.../tools/` | `ocr_pipeline.py` (dual-pass OCR), `make_qa_sheets.py` (2-up contact sheets), `build_deliverables.py` |
| `tools/requirements-ocr.txt` | PyMuPDF 1.26.6 · rapidocr-onnxruntime 1.4.4 · opencv-python-headless 4.11.0.86 |

---

## 7. Open items / gaps worth acting on

1. **Sequence & Series (12 PDFs / 496 pp) has zero output in the repo** — the only untouched slice of the 66-PDF corpus.
2. **Twin 4: 0/540 pages visually verified** — audit, DIBY and uncertainty files exist but every row is explicitly machine-draft.
3. **Twin 3: 285/544 pages still `auto-QA (dual-pass)`**, concentrated in Trigonometric Equation L02–L07.
4. **Twin 2: no manual review at all** (user-requested) — 2,807 low-confidence lines stay unverified and its 242 DIBY entries are candidates, not extracted questions.
5. **Content discrepancy unresolved:** `Trigonometric Functions 01` pp. 2–33/41–49 carry Exponential–Logarithmic Series and inequality headings (Twin 4 log). Needs a coordinator decision — either a mis-scanned module or the correct file is mis-titled.
6. **Branch notes:** each twin's README records that its Arena session branch differs from the branch named in the master plan (`ocr/twin-1-binomial-pc01-04`, `ocr/twin-2-…`, `ocr/twin-3-…`, `ocr/twin-4-…`); handoff folders are laid out so the merge is a file move.
7. **Reporting fidelity is uneven across twins** — Twin 1 reports at item level (per-page QA batches + per-DIBY prompts), Twin 2 at line level (JSONL with boxes), Twin 3 at page level, Twin 4 at page level with a single combined transcript. A unified handoff schema would make the four slices comparable.
