"""Per-item audit: does an item's own lines carry option labels it didn't store?

Runs the same marker scan the extractor uses, so the option labels counted belong
to the item itself and not to a neighbour on the same page.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymupdf                                   # noqa: E402
import diby_layout                               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
NUM = re.compile(r"#?\s*D\s*[I1l]\s*B\s*Y\s*[-–—_.]?\s*(\d{1,3})(?!\d)", re.I)
LET = re.compile(r"DIBY\s*-\s*([A-M])\b")
MARK = re.compile(r"\(\s*[A-Da-d]\s*\)")

items = {(r["book"], r["tag"]): r for r in json.load(open(
    os.path.join(ROOT, "deliverables/diby-books/diby_books.json")))}

for book, fn in FILES.items():
    doc = pymupdf.open(os.path.join(ROOT, fn))
    stream = diby_layout.page_line_stream(doc)
    lettered = "Part 02" in book
    pat = LET if lettered else NUM
    regions, cur = [], None
    for pno, line in stream:
        for m in pat.finditer(line):
            tag = "DIBY-" + (m.group(1).upper() if lettered else m.group(1))
            if cur and cur["tag"] == tag:
                continue
            if cur:
                regions.append(cur)
            cur = {"tag": tag, "page": pno, "lines": [line[m.end():]]}
            break
        else:
            if cur:
                cur["lines"].append(line)
    if cur:
        regions.append(cur)

    missing = []
    for reg in regions:
        it = items.get((book, reg["tag"]))
        if it is None or it["options"].strip():
            continue
        body = " ".join(reg["lines"])
        labels = {m.group(0).strip("() ").upper() for m in MARK.finditer(body)}
        if len(labels) == 4:
            missing.append((reg["tag"], reg["page"], body[:80]))
    if missing:
        print(f"== {book}: {len(missing)} item(s) look option-bearing but stored none")
        for t, p, s in missing[:10]:
            print(f"     {t} p{p} :: {s}")
