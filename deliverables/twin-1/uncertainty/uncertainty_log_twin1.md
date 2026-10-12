# Twin 1 — Uncertainty & Issue Log

Scope: Binomial Theorem L01–L09, Permutations & Combinations L01–L04 (13 PDFs / 508 pages).
Rule followed: nothing guessed, nothing silently corrected; every open item cites PDF page + location.

## Open items

| # | Chapter / Lecture | PDF page | Location | What is uncertain | Candidate readings | Status / action |
|---|---|---|---|---|---|---|
| U-01 | Binomial Theorem L01 | p05 | bottom-right pink line | First token of the final answer line is a cursive group transcribed as `fnf`; its meaning is not defined anywhere on the slide. | "f (no. of)", "finf", "Ans", "∴" | **OPEN** — mathematical content around it is clear: `= ¹⁴C₂ – (21+1) ✓`. Needs teacher's shorthand convention (same token on p13, p16, p17). |
| U-02 | Binomial Theorem L01 | p07 | right column | Small closed circles written low after/inside `6!` and `5!` (`6!₀`, `5!₀`). Purpose not stated (decoration vs. cancellation vs. subscript zero). | pen flourish / deliberate mark | **OPEN** — transcribed exactly as drawn, not interpreted. |
| U-03 | Binomial Theorem L01 | p08 | 4×9 derangement grid | Rows 5 and 6 read `C D A B` and `C D B A`. Transcribed verbatim; a canonical derangement list would differ, but the slide is not corrected. | as printed | **CLOSED (as printed)** — flagged only so the coordinator knows the grid is faithful, not tidied. |
| U-04 | Binomial Theorem L01 | p13 | red vertical list under E₂ | First two entries both read `L₁`; subscripts on `L₄/L₅/L₆` are clipped by the box border. | L₁,L₁ / L₁,L₂ | **OPEN** — needs a higher-resolution re-render (scale 2.0) if the exact list matters downstream. |
| U-05 | Binomial Theorem L01 | p19 | pink cloud `1,3,5,7,9` | Diagonal stroke through the `7`: deletion or flourish? The identical cloud on p20 has no stroke. | flourish | **OPEN (low impact)** |
| U-06 | Binomial Theorem L01 | p27, p28 | example lines | Teacher's open-top `7` is easily misread as `4` in `(a+b)⁷ = ⁷C₀a⁷b⁰ + …`. Adopted `n = 7` because exponent pairs sum to 7; `n = 4` rejected. | 7 (adopted) / 4 | **RESOLVED with rationale** — flagged because the printed chip on p29 legitimately uses `⁴`. |
| U-07 | Binomial Theorem L01 | p29 | lower-left green line | Teacher writes `(2 – 3)⁴` for the x = y = 1 substitution of `(2x–3y)⁴`; recorded as drawn (no "correction" to (2·1–3·1)⁴). | as drawn | **CLOSED (as printed)** |

## Structural findings for the coordinator (not uncertainties, but plan-relevant)

- **F-01 · No text layer anywhere.** All 508 Twin 1 pages are single full-page images (1920×1080 JPEG/JPX on a 1280×720 pt page). `get_text()` returns 0 characters for every page, and no fonts are embedded. Machine OCR is impossible in this sandbox (no tesseract binary, no network outside the allow-list), so transcription is being done visually from rendered page images and every page is therefore also its own visual QA pass.
- **F-02 · "Binomial Theorem 01" is not 100% Binomial content.** p02 announces the lecture plan, p03 opens an "H.W. Discussion", and p04–p22 are Permutations & Combinations material (DIBY-X, de-arrangement, derangements, PIE, sum-of-numbers). Binomial teaching proper starts at p23 (chapter cover). This is *not* a mis-scanned file; it is the recorded lecture including homework recap. Consequence: **do not** treat these P&C slides as duplicates of Twin 2's P&C L05+ files — they come from the module's printed pages 138–145.
- **F-03 · Printed "Page No." watermark is the module page, not the PDF page.** Observed range in BT L01: 138→149 across PDF pages 7→32, with pure-board slides carrying no label. Both numbers are kept in the audit (`pdf_page` + `source_page_label`).
- **F-04 · Two H.W. slides** (BT L01 p21, p22) carry a handwritten `H.W.` mark rather than a printed DIBY marker; they are recorded in the audit but not in the DIBY index, since the DIBY rule keys off the printed `DIBY-*` marker.
- **F-05 · 55th repo PDF still missing.** `git ls-remote origin` shows only `main` (4723bb3) and `admin/ocr-work-plan` (4767582); `main` contains exactly 54 PDFs / 2,128 pages, so nothing new has been pushed for rebalancing. No Sequence & Series uploads are present in this checkout either (those belong to the Current assistant).

## Branch note

The plan assigns Twin 1 the branch `ocr/twin-1-binomial-pc01-04`, but this Arena session is pinned to `arena/5aed984f-ocr` and may not create or push other branches. All Twin 1 output is therefore committed to `arena/5aed984f-ocr` under `deliverables/twin-1/`, ready for the coordinator to merge or cherry-pick onto the Twin 1 branch. Folder layout is exactly the handoff layout from the plan, so the merge is a file move, not a rewrite.
