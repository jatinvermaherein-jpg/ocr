# Twin 1 deliverables — OCR of Binomial Theorem L01–L09 + Permutations & Combinations L01–L04

**Assigned scope (master plan):** 13 PDFs / 508 pages · plan branch `ocr/twin-1-binomial-pc01-04` · this session commits to `arena/5aed984f-ocr` (see uncertainty log "Branch note").
All 13 files were verified against the master inventory before work started: page counts **match exactly (508/508)**, and SHA-256 of every source file is stored in `page-audit/scope_manifest.json`. Source PDFs were never modified.

## Layout
| Path | Contents |
|---|---|
| `transcripts/<chapter>-l<nn>.md` | Page-by-page transcript, one file per lecture, anchors `p01…pNN`. Records printed text, handwriting (colour-tagged), diagrams, DIBY marks, per-page uncertainty. |
| `page-audit/page_audit_twin1.csv` | 508 rows — one per expected page, pre-registered before transcription so gaps are impossible. Columns: chapter, lecture, source_pdf, pdf_page, source_page_label, topic/heading, transcript ref, printed/handwriting captured, DIBY present + labels, uncertainty count, extraction method, visual-QA status, reviewer, timestamp. |
| `page-audit/scope_manifest.json` | Per-file expected vs actual page counts + SHA-256. |
| `page-audit/progress.json` | Machine-readable completion ledger (per lecture: reviewed/total). |
| `diby/diby_index_twin1.csv` | DIBY register: marker, exact printed label, internal ID (only when the source has none), verbatim prompt, options, visible answer, uncertainty, QA status. |
| `uncertainty/uncertainty_log_twin1.md` | Open uncertainties (page + location cited) and structural findings for the coordinator. |

## Progress
| Lecture | Pages | Transcribed + QA'd |
|---|---|---|
| Binomial Theorem L01 | 33 | **33 ✅** |
| Binomial Theorem L02 | 40 | **40 ✅** (incl. printed DIBY-01…DIBY-06) |
| Binomial Theorem L03–L09 | 271 | pending |
| Permutations & Combinations L01–L04 | 164 | pending |
| **Total** | **508** | **36 (7.1%)** |

## How work is produced (reproducible pipeline)
```bash
pip install --break-system-packages pymupdf            # renderer (no tesseract available in sandbox)
python3 tools/render_pages.py --lecture bt02 --scale 1.25   # writes PNGs to /home/user/work/pages (outside repo)
# ...transcribe each page image, append to transcripts/*.md, add one qabatch_<key>.json entry per page...
python3 tools/merge_qa.py                              # merges QA into the 508-row audit + DIBY index + progress
python3 tools/init_audit.py                            # (re)register all 508 rows; prints inventory mismatches
```
Page keys: `bt01…bt09`, `pc01…pc04` (`tools/twin1_scope.py` is the single source of truth for the assignment).

## Standards actually applied (from the plan)
- Every page processed in order — no sampling, no omission, no skipped cover/blank-looking slides.
- Printed **and** handwritten content captured, including Hinglish annotations, colour coding, arrow/box marks, and printed option letters/numbers exactly as printed.
- Nothing mathematically "corrected"; source errors and clipped glyphs are transcribed as drawn and logged with page + location.
- Visual comparison is intrinsic: each page is transcribed from the rendered source image, so `visual_qa_status = QA-PASSED` means "read off the source at 1600×900, cross-checked against the printed label scheme", not "OCR confidence was high".
