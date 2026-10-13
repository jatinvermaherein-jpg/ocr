# DIBY-only books — extraction

The nine uploaded books ("Arjuna JEE 2027 · By: Sachin Jakhar") are **digital natives**: each page
carries a real text layer, so nothing here was OCR'd. What the plain text layer loses — subscripts,
superscripts, stacked fractions, option grids — is restored from span geometry instead
(`tools/diby_layout.py`), then the items are read out with `tools/extract_diby_books_text.py`.

## Result

| | |
|---|---:|
| Books | 9 |
| Pages | 241 |
| Items | **565** (552 numbered + 13 lettered) |
| With an answer | 535 |
| With options | 312 |
| Duplicate tags | 0 |
| Markers not turned into items | 7 (motivational slides, not questions) |

Per book: Basic Mathematics Part 01 60 · Part 02 62 · Set Theory 31 · Permutations & Combinations 80 ·
Quadratic Equations Part 01 85 · Part 02 13 · Sequence & Series 114 · Trigonometric Equations 61 ·
Trigonometric Functions 59.

## Files

| File | What it is |
|---|---|
| `diby_books.json` | the extraction — book, tag, PDF page, question, options, answer |
| `diby_books_index.csv` | the same rows as a spreadsheet |
| `manual_fixes.json` | the few items whose content sits in an image or a merged text-layer cell; each entry names the page it was read from |
| `qa_notes.md` | anything that needed a decision (merged answer keys, wordless items) |

Documents built from this: `deliverables/DIBY_Books.docx` (compact) and
`deliverables/DIBY_Books_Print.docx` (print, pure black, no cover/contents/header/footer).

## How to reproduce

```bash
python3 tools/extract_diby_books_text.py      # writes diby_books.json + CSV into this folder
python3 tools/build_diby_books_docs.py        # writes the two .docx files
```

Two layouts are handled: **marker-first** (`# DIBY-07` then its question, as in the eight numbered
books) and **marker-last** (`DIBY-C` after the question, as in Quadratic Equations Part 02, whose
option block can straddle the marker and whose final page is the A–M answer key).

## Caveats

* Extraction is from the PDF text layer — it is **not** a page-by-page visual transcription. Six
  items were repaired against the rendered page (see `manual_fixes.json`); the rest carry whatever
  the text layer holds.
* Complex display layouts (graphs, matching/column questions, multi-part sums with several stacked
  fractions) come through flattened; their maths is present but the reading order can be jumbled.
* 1,924 of 1,977 maths spans typeset as native Word equations; the remaining 53 fall back to
  readable plain text (`tools/diby_math.py`).
