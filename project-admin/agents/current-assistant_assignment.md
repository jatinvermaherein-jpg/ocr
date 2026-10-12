# Work Assignment — Current assistant

**Assigned load:** 12 PDFs • 496 pages  
**Branch:** `ocr/current-sequence-series`  
**Output folder:** `deliverables/current-assistant/`  
**Repository:** `git@github.com:jatinvermaherein-jpg/ocr.git`

## Exact assigned files

- **Sequence & Series — Lecture 01** — `Sequence and Series 01 Class Notes.pdf` — 44 pages — Current chat uploads
- **Sequence & Series — Lecture 02** — `Sequence and Series 02 Class Notes.pdf` — 39 pages — Current chat uploads
- **Sequence & Series — Lecture 03** — `Sequence and Series 03 Class Notes.pdf` — 43 pages — Current chat uploads
- **Sequence & Series — Lecture 04** — `Sequence and Series 04 Class Notes.pdf` — 42 pages — Current chat uploads
- **Sequence & Series — Lecture 05** — `Sequence and Series 05 Class Notes.pdf` — 40 pages — Current chat uploads
- **Sequence & Series — Lecture 06** — `Sequence and Series 06 Class Notes.pdf` — 38 pages — Current chat uploads
- **Sequence & Series — Lecture 07** — `Sequence and Series 07 Class Notes.pdf.pdf` — 41 pages — Current chat uploads
- **Sequence & Series — Lecture 08** — `Sequence and Series 08 Class Notes Maths By Sachin Sir.pdf` — 48 pages — Current chat uploads
- **Sequence & Series — Lecture 09** — `Sequence and Series 09 Class Notes.pdf.pdf` — 44 pages — Current chat uploads
- **Sequence & Series — Lecture 10** — `Sequence and Series 10 Class Notes.pdf.pdf` — 35 pages — Current chat uploads
- **Sequence & Series — Lecture 11** — `Sequence and Series 11 Class Notes.pdf.pdf` — 42 pages — Current chat uploads
- **Sequence & Series — Lecture 12** — `Sequence and Series 12 Class Notes.pdf.pdf` — 40 pages — Current chat uploads

## Shared instructions
- Process every page in order. **Do not summarize, sample, or skip anything.** The master inventory gives the expected page count for each PDF.
- On every page record exact chapter, lecture number, source filename, and 1-based PDF page number. Verify chapter and lecture against the title slide; log any mismatch with the filename.
- Transcribe all printed and handwritten content: prose, equations and every derivation step, examples, prompts, answers, options, tables, diagram/graph labels, arrows, marginal notes, and meaningful color annotations.
- Preserve mathematical signs, superscripts/subscripts, Greek letters, brackets, interval endpoints, inequality direction, and question/option labels. Do not silently “correct” a suspected source error.
- Visually compare the transcript with **every original page** after OCR. OCR alone is not final QA. If unclear, mark `[UNCLEAR]`, cite page and approximate location, and retain alternative readings rather than guessing.
- Maintain one audit row for every source page, including covers, topic lists, graphics-only, and blank-looking pages. A no-text OCR page must still be inspected and explicitly categorized.
- Create a separate DIBY (“Do It By Yourself”) index. Capture every marker, full prompt, options, and any visible answer/solution.
- Preserve the exact printed DIBY question label. Numbers and alphabets both count (e.g. `Q. 4`, `2(b)`, `(A)`, `I`); preserve punctuation/case. If no label is printed, create an internal ID such as `L03-P14-DIBY-01` and mark it as internal, not printed.
- Hand off four files under `deliverables/<your-slug>/`: page-by-page transcript (DOCX/Markdown), page audit (XLSX/CSV), DIBY index (CSV), and uncertainty/issue log (CSV).
- Use only your assigned branch and folder; do not edit another worker’s files. Push when every assigned page and DIBY item has passed visual QA. Include reviewed page and DIBY counts in the handoff.
- Assignment/inventory docs are on branch `admin/ocr-work-plan`. Start your branch from that branch. The shared SSH setup file is provided outside the repository; never commit it or any private key.

## Coverage note
The current checkout contains 54 PDFs in the repository (2,128 pages); the user expected 55. The 12 attached Sequence & Series PDFs make the currently indexed total 66 PDFs / 2,624 pages. One expected repo PDF is not yet visible. Do not silently add it; coordinator will inventory and assign it when located.
