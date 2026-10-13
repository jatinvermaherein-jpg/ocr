# DIBY book extraction — notes

## Decisions taken by the extractor

- **Quadratic Equations Part 02 (lettered book):** the A–M key on page 16 is merged into the
  items; the option block that continues *below* a marker belongs to the previous item and is
  consumed there, never into the next item.
- **Matching / column questions** are stored as a single option string — Column-I `(A)…(D)`,
  then `||`, then Column-II `(P)…(S)` (or the matching answer choices) — with the printed
  answer mapping kept as it stands: Basic Mathematics Part 01 DIBY-12, Part 02 DIBY-70,
  Set Theory DIBY-21, Trigonometric Functions DIBY-32.
- **Image-only questions** (Basic Mathematics Part 01 pp. 19–20, Sequence & Series p. 44),
  **graph questions** and the whole lettered book are read from the rendered page — see
  `manual_fixes.json`.
- **Multi-part items** (several `[Ans.]` in one item) keep every answer inline in the question
  text; they are not split.

## Bugs found and fixed while sharpening the text layer

- **Stacked fractions** whose numerator and denominator sit on separate baselines were being
  flattened (`x^{3}+^{1}3`); they are now rebuilt into `\frac{}{}` from the span geometry
  (~500 fractions restored).
- **Option blocks** were merged into the row above, which interleaved the cells and could empty
  one of them; a row carrying its own `(A)…(D)` labels is now never merged.
- **Lower-case option labels** `(c)`/`(d)` were not recognised as labels.
- **Option letters were glued to text** (`…\frac{1}{abc}(c) 0`); labels are now spaced out.
- **Last option duplicated into the question** — the tail after the `(D)` marker is (D)'s own
  text, not a second copy. Fixed for 365 of the 565 items.
- **Option labels inside the question** (the `(A)` of `n(Π (A))`) no longer derail the option
  split — the splitter skips a label followed by `)` and retries past labels inside the stem.
- **A fraction written as `a/b (bracket)`** had the bracket read as its denominator
  (Sequence & Series DIBY-45).
- **A page heading sitting on the option row** no longer lands inside option (D)
  (Sequence & Series DIBY-86).
- **Spacing around equations:** Word renders an inline equation with no space of its own, so
  text→equation junctions now get an explicit space (`then a(a−b)+…`, not `thena(a−b)+…`), and
  `(ii)The` becomes `(ii) The`.
- **Unclosed brace tails** from stacked layouts leaked `}{…}` debris; brace-depth trim added.
- A sub-part label read as a fraction (`(i)/(ii)`) is restored to `(i) (ii)`.

## Still worth knowing

- Extraction is from the PDF text layer, sharpened by span geometry — it is **not** a
  page-by-page visual transcription. **46 items** were repaired against the rendered page
  (`manual_fixes.json`); the rest carry what the text layer holds.
- Complex display layouts (graphs, matching questions, multi-part sums with several stacked
  fractions) come through flattened; their maths is present but the reading order can be
  jumbled. Multi-part questions keep their sub-part answers inline.
- 1,886 of 1,918 maths spans typeset as native Word equations; the remaining 32 fall back to
  readable plain text.
- The 30 items without an answer are "prove that / show that" proofs and fill-in-the-blank
  questions that carry no printed answer — verified one by one against their own lines.

## Audit helpers

- `tools/audit_diby_books.py` — no answer / short question / LaTeX residue per item.
- `tools/audit_diby_books_options.py` — item looks option-bearing but stored none.
- `tools/verify_diby_books_docs.py` — checks the built DOCX files in the OOXML: 9 book
  headings, a tag per item, typeset equations, no raw LaTeX, pure black, odd-page book breaks,
  no header/footer parts.
