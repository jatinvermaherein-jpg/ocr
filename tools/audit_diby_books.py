"""Audit the DIBY-book extraction for leftovers.

Looks for (a) items whose page clearly printed options but which stored none,
(b) items with no answer, (c) items whose question is suspiciously short or
still carries LaTeX debris.

    python3 tools/audit_diby_books.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diby_layout import page_line_stream          # noqa: E402
import pymupdf                                     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "deliverables/diby-books/diby_books.json")

FILES = {
    "Basic Mathematics Part 01 DIBY": "Basic Mathematics Part 01  DIBY  Maths By Sachin Sir.pdf",
    "Basic Mathematics Part 02 DIBY": "Basic Mathematics Part 02  DIBY  Maths By Sachin Sir.pdf",
    "Permutations and Combinations DIBY": "Permutations and Combinations  DIBY.pdf",
    "Quadratic Equations Part 01 DIBY": "QUADRATIC EQUATION_PART-01_DIBY (1).pdf",
    "Quadratic Equations Part 02 DIBY": "Quadratic Equations Part 02  DIBY.pdf",
    "Sequence and Series DIBY": "Sequence and Series DIBY.pdf",
    "Set Theory DIBY": "Set Theory DIBY.pdf",
    "Trigonometric Equations DIBY": "Trigonometric Equations DIBY.pdf",
    "Trigonometric Functions DIBY": "Trigonometric Functions DIBY.pdf",
}
MARK = re.compile(r"\(\s*[A-Da-d]\s*\)")


def main() -> None:
    items = json.load(open(SRC))
    pages = {}
    for book, fn in FILES.items():
        doc = pymupdf.open(os.path.join(ROOT, fn))
        for pno, line in page_line_stream(doc):
            pages.setdefault((book, pno), []).append(line)

    no_opt, no_ans, short, debris = [], [], [], []
    for r in items:
        key = (r["book"], r["pdf_page"])
        body = " ".join(pages.get(key, []))
        labels = {m.group(0).strip("() ").upper() for m in MARK.finditer(body)}
        if not r["options"].strip() and len(labels) >= 4:
            no_opt.append((r["book"][:20], r["tag"], r["pdf_page"]))
        if not r["answer"].strip():
            no_ans.append((r["book"][:20], r["tag"], r["pdf_page"]))
        if len(r["question"].strip()) < 25:
            short.append((r["book"][:20], r["tag"], r["pdf_page"], r["question"][:60]))
        if re.search(r"\\frac\{,|\\frac\{\}|\\\\[a-z]+\{?$|\{\(\}|\\frac\{\([a-z]{1,4}\)", r["question"]):
            debris.append((r["book"][:20], r["tag"], r["pdf_page"], r["question"][:70]))

    print(f"items {len(items)}")
    print(f"(a) page printed >=4 labels but no options stored: {len(no_opt)}")
    for t in no_opt:
        print("     ", t)
    print(f"(b) no answer stored: {len(no_ans)}")
    by = {}
    for b, t, p in no_ans:
        by.setdefault(b, []).append(t)
    for b in sorted(by):
        print(f"      {b}: {len(by[b])} -> {by[b][:12]}")
    print(f"(c) question shorter than 25 chars: {len(short)}")
    for t in short:
        print("     ", t)
    print(f"(d) residue patterns in question: {len(debris)}")
    for t in debris[:15]:
        print("     ", t)


if __name__ == "__main__":
    main()
