# DIBY book extraction — notes

- Quadratic Equations Part 02 DIBY: A–M answer key on page(s) [16] merged into items
- Option labels sitting inside the question text (the `(A)` of `n(Π (A))`) no longer
  derail the option split — the splitter retries past them.
- Option labels sitting inside the question text (the `(A)` of `n(Π (A))`) no longer derail
  the option split — the splitter retries past them.
- Audit helpers: `tools/audit_diby_books.py` (no answer / short question / residue) and
  `tools/audit_diby_books_options.py` (item looks option-bearing but stored none). After the
  fixes both report nothing structural: the only remaining no-answer items are "prove that /
  show that" proofs and fill-in-the-blank questions that carry no printed answer.
