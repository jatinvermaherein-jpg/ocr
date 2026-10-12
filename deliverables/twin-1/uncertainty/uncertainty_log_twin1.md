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

## Added while transcribing L02 / L03

| # | Chapter / Lecture | PDF page | Location | What is uncertain | Status / action |
|---|---|---|---|---|---|
| U-08 | Binomial Theorem L03 | p06 | left column | The **printed** slide numbers two consecutive items "6." and has no item 7 (recap questions 4, 5, 6, 6). | **OPEN (source defect)** — transcribed as printed; coordinator may want the real numbering from the module PDF. |
| U-09 | Binomial Theorem L02 | p31 | upper right orange sequence | Last subscript drawn as `a₄` where the row is labelled `T.T. = 7` (so it should be a₇). | **OPEN** — teacher's 4/7 hand, see also U-06. |
| U-10 | Binomial Theorem L02 | p19 | third working line | Writes `⁵C₀` where the line above writes `⁵Cᵣ`. | **OPEN** — not harmonised. |

**F-06 · DIBY chain spans files.** L02 p22 sets a question with a handwritten `90% DIBY` + `H.W.`; L02 p38 prints the same item as **DIBY-06** (different option order); L03 p08 contains the worked solution. The DIBY register entry for DIBY-06 now points to L03 p08. Any worker de-duplicating by question text across files must not drop either copy.
**F-07 · Printed DIBY blocks exist.** L02 p36–p38 carry `# DIBY-01`…`# DIBY-06` with printed `[Ans.: …]`, including one answer field printed as `....` (DIBY-05). Expect the same block shape in later lectures; L01 had only a handwritten `DIBY-X`.

## Batch 6 (Binomial Theorem L03 p25–p35)
- **U-11 | Binomial Theorem L03 | p27 | low→med | open-top digit** — power list for `(2+x^3)^5` written `x^0, x^3, x^5, x^9, x^12`; the third entry should be `x^6` (open-top ⁶ vs ⁵ hazard). Transcribed as drawn; page 27 top-right.
- **U-12 | Binomial Theorem L03 | p25 | low | unfinished board** — two coefficient blanks (`___ x^7 × ___ x^30`, `~~~ x^0 × ~~~ x^0`) are left unfilled on the slide; nothing to disambiguate, recorded as-is.
- **U-13 | Binomial Theorem L03 | p16 | low | printed defect** — red chip prints `IVRTTATIONAL` where `IRRATIONAL` is meant (transcribed as printed; not a handwriting ambiguity).
- **U-14 | Binomial Theorem L03 | p15 | low | handwriting** — single unreadable token before "is multiple of 4" in the yellow line; every other word on the page is legible.
- **U-15 | Binomial Theorem L03 | p34 | low | printed defect** — hashtag printed `#futurellTians` (double l) on the closing card.
## Findings (batch 6)
- **F-08 | printed page labels are not monotonic** — L03 shows Page No. 149 (p12), 151 (p09, p13, p16), 152 (p21, p22, p23, p24, p25, p26), 153 (p28): module pages repeat and drift, so the transcript key is always the PDF page and the label is quoted per page.
- **F-09 | DIBY numbering restarts inside one lecture** — L03 has `DIBY-01…DIBY-05` (p11, p14) *and* a second `DIBY-01…DIBY-12` (p31–p35). Same label, different question. The register therefore carries internal IDs (`BT-L03-P11-DIBY-01` vs `BT-L03-P31-DIBY-01`).
- **F-10 | cross-file duplicate set, different answer keys** — L03 p31–p32 reproduces the six printed DIBY questions of L02 p37–p38 in a different order; L02's DIBY-05 answer line is blank (`....`) and L03 p32's DIBY-05 supplies `Ans.: 8` for that same question. Both rows kept; the L02 row now cross-references L03.
- **F-11 | deck order anomaly** — the Thank-You card is PDF p34 while printed DIBY-10/11/12 sit on p35 after it; transcribed in PDF order with a note.
## Batch 7 (Binomial Theorem L04 p01–p16)
- **U-16 | Binomial Theorem L04 | p03 | low | printed defect** — the "Topics to be covered" slide has a **D** tile with no text; kept as printed.
- **U-17 | Binomial Theorem L04 | p15 vs p04 | medium | duplicate printed label** — two different questions in this lecture both print `# DIBY-05` under the same `RAPID FIRE DIBY'S` chip (p04: greatest value of the term independent of x, Ans. (A) 63/8; p15: term independent of x in (1+x+2x^3)(3x^2/2-1/(3x))^9, Ans. 17/54). The deck clearly stitches two rapid-fire sets. Both are in the register with internal IDs; no de-duplication.
- **F-12 | L03 → L04 hand-off is a homework loop** — L03 p28 (H.W.), L03 p29 (H.W. + `90%. DIBY`) and L03 p18 (`# DIBY-(A)`) are discussed as L04 p06, p07 and p05 respectively; L04 p05 carries only a pink `Done!!` because the item was already solved in L03 p18's follow-up. Any cross-file summary must keep these three chains.
- **F-13 | percentage tags** — the teacher writes success-rate tags on solved MCQs (`84%.` on L04 p06 next to the ticked option, `90%. DIBY` on L03 p29). They are annotation, not part of the question; transcribed in the H: field only.
## Batch 8 (Binomial Theorem L04 p33–p46, lecture closed)
- **U-18 | Binomial Theorem L04 | p33, p36 | medium | handwriting legibility (7 vs 4)** — the teacher's `7` is drawn as a crossed stroke that reads as `4` at slide resolution. On p33 all six subscripts of the pink hockey-stick row, and on p36 the two subscripts of the yellow answer, are this glyph; they can only be `7` (Σ_{n=7}^{12} ⁿC₇ = ¹³C₈ = ¹³C₅, and option C `⁵¹C − ³⁰C`). Both readings transcribed as `7` with the glyph noted; these are two further rows for the U-06 7-vs-4 ledger.
- **U-19 | Binomial Theorem L04 | p44 | high | printed defect** — DIBY-26's four options are printed **byte-identically** (`a/11 = b/11 = c/42`), confirmed on a 1.8× zoom crop; the key is `(C)`. The relation that actually holds for the greatest coefficients (a = ¹⁹C₉ = 92378, b = ²⁰C₁₀ = 184756, c = ²¹C₁₀ = 352716) is `a/11 = b/22 = c/42 = 8398`, so one denominator per option was presumably lost in typesetting. Transcribed as printed; **no** repair applied — this is the only page in the assignment where the printed options are unusable for answer verification.
- **U-20 | Binomial Theorem L04 | p40 vs p42 | low | duplicate printed item** — DIBY-19 repeats DIBY-15's question text verbatim with the option list permuted (and the same key `(A)`). Both kept as separate register rows (BT-L04-P40-DIBY-15, BT-L04-P42-DIBY-19); no de-duplication, matching the treatment of L02 p37-38 vs L03 p31-32.
- **U-21 | Binomial Theorem L04 | p38/p39 | low | unfinished working + faint glyph** — DIBY-09's middle exponent prints very faintly on p38 (reads as `x`); p39's board line `ⁿC₄ , ⁿC₅ , ⁿC₆ → AP` fixes it as `x⁵`. p39 stops at `2/(5(n−5)) = 1/((n−4)(n−5)) + 1/20` with no value of n written; the printed key `(D) 14` is the only source for the answer.
- **F-14 | L04's printed DIBY labels are three overlapping sequences** — `RAPID FIRE DIBY'S` items `DIBY-01…08` (p13–p19), a second block `DIBY-07…09` under the **DO IT BY YOURSELF (DIBY)** pill (p38, colliding with p19's 07/08), then `DIBY-13…27` (p40–p44) in which **10, 11 and 12 are never printed** (L03 owns those numbers, see F-11). Register internal IDs therefore carry the PDF page (`BT-L04-P38-DIBY-07` vs `BT-L04-P19-DIBY-07`), and dedup across the series must key on the prompt text, never on the label. Extends U-17.
- **F-15 | header wording for rapid-fire slides is not stable** — L04 p33 prints the chip as **RAPID FIRE ROUND** (no DIBY wording, no `# DIBY-nn` tags) while p13–p19 print **RAPID FIRE DIBY'S** with numbered tags; L03 uses **RAPID FIRE DIBY'S** throughout. Only the tagged slides contribute register rows, so p33's five items are deliberately *not* in the DIBY index (they are in the transcript).
