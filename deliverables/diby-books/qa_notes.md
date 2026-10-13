# DIBY book extraction — notes

## Decisions taken by the extractor

- **Quadratic Equations Part 02 (lettered book):** the A–M key on page 16 is merged into the
  items; the option block that continues *below* a marker belongs to the previous item and is
  consumed there, never into the next item.
- **Matching/column questions:** Basic Mathematics Part 01 DIBY-12, Part 02 DIBY-70 and Set
  Theory DIBY-21 keep both columns in the option text (separated by `||` for the two-column
  ones) with the printed answer mapping.
- **Image-only questions** (Basic Mathematics Part 01 pp. 19–20, Sequence & Series p. 44) and
  **graph/matching slides** are read from the rendered page — see `manual_fixes.json`.

## Bugs found and fixed while sharpening the text layer

- **Stacked fractions** whose numerator and denominator sit on separate baselines were being
  flattened (`a + 1_{a}`); they are now rebuilt into `\frac{}{}` from the span geometry.
- **Option blocks** were merged into the row above, which interleaved the cells and could empty
  one of them; a row carrying its own `(A)…(D)` labels is now never merged.
- **Lower-case option labels** `(c)`/`(d)` were not recognised as labels.
- **Option letters were glued to text** (`…\frac{1}{abc}(c) 0`); labels are now spaced out.
- **Last option duplicated into the question** — the tail after the `(D)` marker is (D)'s own
  text, not a second copy. Fixed for 365 of the 565 items.
- **Unclosed brace tails** from stacked layouts leaked `}{…}` debris; brace-depth trim added.
- A sub-part label read as a fraction (`(i)/(ii)`) is restored to `(i) (ii)`.

## Still worth knowing

- Extraction is from the PDF text layer, sharpened by span geometry — it is **not** a
  page-by-page visual transcription. **41 items** were repaired against the rendered page
  (`manual_fixes.json`); the rest carry what the text layer holds.
- Complex display layouts (graphs, matching/column questions, multi-part sums with several
  stacked fractions) come through flattened; their maths is present but the reading order can
  be jumbled. Sequence & Series DIBY-86 keeps a "WRITING T_n FOR SERIES…" heading inside the
  item text.
- 1,882 of 1,914 maths spans typeset as native Word equations; the remaining 32 fall back to
  readable plain text.
