# Twin 2 OCR handoff

**OCR finished: 15 / 15 PDFs, 536 / 536 pages.**

**No manual review performed**, as requested by the user. This handoff completes the automated OCR stage only; it does not claim completion of the allocation plan's visual QA or faithful math/diagram transcription standards.

## Files

- [All transcripts — Markdown](Twin_2_OCR.md)
- [All transcripts — plain text](Twin_2_OCR.txt)
- [Page audit / coverage](Page_Audit.csv): one row for every source page; not a visual review.
- [DIBY marker candidates](DIBY_Candidates.md) ([CSV](DIBY_Candidates.csv)): automatic hits, not verified questions.
- [Uncertainty log](Uncertainty_Log.csv): every page marked unreviewed, plus low-score lines with locations.
- [Completion summary](completion_summary.json)
- [Run manifest and source SHA-256 fingerprints](run_manifest.json)
- `records/`: machine-readable JSONL containing text, scores, render size, and bounding boxes for each page.
- `transcripts/`: one Markdown and one plain-text transcript for each of the 15 lectures.
- `Twin_2_OCR.zip`: downloadable bundle; generated archive is not tracked in Git.

## Lecture coverage

| Chapter | Lecture | Source PDF | OCR pages | Transcript |
|---|---:|---|---:|---|
| Permutations & Combinations | 05 | [Permutations and Combinations 05 Class Notes.pdf](../../Permutations%20and%20Combinations%2005%20Class%20Notes.pdf) | 32/32 | [pc05](transcripts/pc05.md) |
| Permutations & Combinations | 06 | [Permutations and Combinations 06 Class Notes.pdf](../../Permutations%20and%20Combinations%2006%20Class%20Notes.pdf) | 43/43 | [pc06](transcripts/pc06.md) |
| Permutations & Combinations | 07 | [Permutations and Combinations 07 Class Notes.pdf](../../Permutations%20and%20Combinations%2007%20Class%20Notes.pdf) | 42/42 | [pc07](transcripts/pc07.md) |
| Permutations & Combinations | 08 | [Permutations and Combinations 08 Class Notes.pdf](../../Permutations%20and%20Combinations%2008%20Class%20Notes.pdf) | 45/45 | [pc08](transcripts/pc08.md) |
| Permutations & Combinations | 09 | [Permutations and Combinations 09 Class Notes.pdf](../../Permutations%20and%20Combinations%2009%20Class%20Notes.pdf) | 34/34 | [pc09](transcripts/pc09.md) |
| Permutations & Combinations | 10 | [Permutations and Combinations 10 Class Notes.pdf](../../Permutations%20and%20Combinations%2010%20Class%20Notes.pdf) | 37/37 | [pc10](transcripts/pc10.md) |
| Permutations & Combinations | 11 | [Permutations and Combinations 11 Class Notes.pdf](../../Permutations%20and%20Combinations%2011%20Class%20Notes.pdf) | 45/45 | [pc11](transcripts/pc11.md) |
| Quadratic Equations | 01 | [Quadratic Equations 01 Class Notes.pdf](../../Quadratic%20Equations%2001%20Class%20Notes.pdf) | 34/34 | [qe01](transcripts/qe01.md) |
| Quadratic Equations | 02 | [Quadratic Equations 02  Class Notes  Maths By Sachin Sir.pdf](../../Quadratic%20Equations%2002%20%20Class%20Notes%20%20Maths%20By%20Sachin%20Sir.pdf) | 38/38 | [qe02](transcripts/qe02.md) |
| Quadratic Equations | 03 | [Quadratic Equations 03  Class Notes  Maths By Sachin Sir.pdf](../../Quadratic%20Equations%2003%20%20Class%20Notes%20%20Maths%20By%20Sachin%20Sir.pdf) | 29/29 | [qe03](transcripts/qe03.md) |
| Quadratic Equations | 04 | [Quadratic Equations 04 Class Notes.pdf](../../Quadratic%20Equations%2004%20Class%20Notes.pdf) | 33/33 | [qe04](transcripts/qe04.md) |
| Quadratic Equations | 05 | [Quadratic Equations 05 Class Notes.pdf](../../Quadratic%20Equations%2005%20Class%20Notes.pdf) | 32/32 | [qe05](transcripts/qe05.md) |
| Quadratic Equations | 06 | [Quadratic Equations 06 Class Notes.pdf](../../Quadratic%20Equations%2006%20Class%20Notes.pdf) | 29/29 | [qe06](transcripts/qe06.md) |
| Quadratic Equations | 07 | [Quadratic Equations 07 Class Notes.pdf](../../Quadratic%20Equations%2007%20Class%20Notes.pdf) | 32/32 | [qe07](transcripts/qe07.md) |
| Quadratic Equations | 08 | [Quadratic Equations 08 Class Notes.pdf](../../Quadratic%20Equations%2008%20Class%20Notes.pdf) | 31/31 | [qe08](transcripts/qe08.md) |

## Recognition limits

- Engine: RapidOCR ONNX Runtime 1.4.4, bundled PP-OCRv4 detection/recognition models, CPU.
- Every PDF page was rendered at 1.5× (normally 1920 × 1080 pixels) and OCR-processed. Existing PDF text, if present, is saved separately.
- All recognized lines are retained, including low-confidence text. No manual corrections, math normalization, answer inference, or invented diagram descriptions.
- The general text recognizer is not a mathematical handwriting transcription system. Fractions, powers, roots, symbols, multi-column layout, and handwriting may be garbled or omitted.
- High engine scores do not certify accurate transcription. Pages with no detected text are not certified blank.
- Original diagrams and annotations remain in the source PDFs; the text outputs do not reproduce those graphics.

Recognized lines: **10713** · Low-score lines (<0.80): **2807** · No-text detections: **0** · DIBY candidates: **242**.

## Re-run / resume

From the repository root, install the pinned packages in an isolated environment. The headless OpenCV wheel is required on this server.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tools/requirements-ocr.txt
.venv/bin/python -m pip uninstall -y opencv-python
.venv/bin/python -m pip install --force-reinstall opencv-python-headless==4.11.0.86
.venv/bin/python tools/ocr_twin2.py --workers 2
.venv/bin/python tools/package_twin2_ocr.py
```

Checkpoints are kept under ignored `.work/` and are reused only for identical source fingerprints and engine settings. Source PDFs and the master allocation documents are unchanged.
