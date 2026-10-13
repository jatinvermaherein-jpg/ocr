# Coverage — independent cross-check over the Twin 2 block (P&C L05–L11 + QE L01–L08, 536 pp)

Built from this session's own dual-pass records (`/home/user/ocr_work/raw/…`). Every one of the
15 lectures reconciled at **expected == reviewed** (536/536); there are no gaps.

## Machine extraction (complete)

| | |
|---|---:|
| Pages extracted (dual pass @200 dpi) | **536 / 536** |
| PDFs | 15 / 15 |
| Pages with no text detected | 0 |
| DIBY rows in `diby_index.csv` | 204 (23 visually verified, 181 auto-extract) |
| Uncertainty entries | 341 |

## Visual QA (in progress — tiers are recorded per page)

| Tier | Pages | Meaning |
|---|---:|---|
| `visual-full` | **75** | read page-by-page off contact sheets at native resolution; verified text recorded |
| `visual-scan` | 0 | (reserved: page read at reduced detail only) |
| `auto-QA (dual-pass)` | **461** | machine output only — **not** human-verified |

So: **75 / 536 pages (14.0 %) carry a verified transcript.** The remaining 461 pages have machine
text with `[LOWCONF]` flags and per-page uncertainty entries, and must not be treated as verified.

| Lecture | Pages | Verified (`visual-full`) |
|---|---:|---:|
| Permutations & Combinations 05 | 32 | **32** |
| Permutations & Combinations 06 | 43 | **43** |
| Permutations & Combinations 07 | 42 | 0 |
| Permutations & Combinations 08 | 45 | 0 |
| Permutations & Combinations 09 | 34 | 0 |
| Permutations & Combinations 10 | 37 | 0 |
| Permutations & Combinations 11 | 45 | 0 |
| Quadratic Equations 01–08 | 258 | 0 |
| **Total** | **536** | **75** |

## Why this layer exists (evidence)

The block owner's handoff (`ocr-output/twin-2/`, merged) is machine-only and declares no manual
review. This session ran an independent pass with a different render scale. Comparing the two
machine outputs on the 8 lectures both have processed:

- mean normalised text similarity **0.71–0.85** per lecture
- **42 pages below 0.50 similarity** — i.e. neither machine pass is reliable on those pages

Against this session's 32 visually-verified L05 pages, the two passes split 18 / 7 / 7
(this layer ahead / block owner ahead / tie). Two machine passes agreeing is **not** evidence of
correctness — the 340 dpi zoom crops were what actually resolved the ambiguities (see
`uncertainty_log.md`, e.g. L05 p4 digit set, L05 p5 leading-factor product, L06 p10 gap-method chain).

## Next actions (in priority order)

1. Finish visual QA for P&C L07–L11 (245 pp) — all machine-extracted, none verified yet.
2. Then QE L01–L08 (258 pp).
3. Promote `diby_index.csv` rows from `auto-extract` to verified as their pages are reviewed
   (181 of 204 rows are still auto-extract).
