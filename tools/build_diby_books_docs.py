#!/usr/bin/env python3
"""Build the DIBY-book question documents (compact + print) from diby_books.json.

Layout per item:  DIBY tag  ·  question (typeset equations)  ·  options  ·  answer.
Style rules carried over from the class-note editions:
  · print edition: black & white only, no cover, no contents, no header/footer,
    12 pt body, each book starts on an odd page, questions flow.
  · compact edition: 10.5 pt body, tighter margins.
Writes deliverables/DIBY_Books_Print.docx and deliverables/DIBY_Books.docx
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_diby_docx_v2 import (                       # noqa: E402
    answer_short, latex_to_omml, letter_label,
)
from diby_math import latex_fallback, segments_latex as segments   # noqa: E402

from docx import Document                              # noqa: E402
from docx.enum.section import WD_SECTION               # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT  # noqa: E402
from docx.oxml import OxmlElement                       # noqa: E402
from docx.oxml.ns import qn                             # noqa: E402
from docx.shared import Cm, Pt, RGBColor                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "deliverables/diby-books/diby_books.json")
BLACK = RGBColor(0, 0, 0)

STYLES = {
    "print": dict(out="deliverables/DIBY_Books_Print.docx", body=12, opt=11, tag=11.5,
                  h1=18, h2=13.5, side=2.0, vert=1.8, spacing=1.15, gap=11, rule=True),
    "compact": dict(out="deliverables/DIBY_Books.docx", body=10.5, opt=10, tag=10,
                    h1=15, h2=12, side=1.5, vert=1.3, spacing=0.95, gap=7, rule=False),
}


def rule(doc, space_after=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    borders.append(bottom)
    pPr.append(borders)
    return p


def build(style_name: str, items: list[dict], omml: dict, latex_ok: set):
    st = STYLES[style_name]
    out = os.path.join(ROOT, st["out"])
    doc = Document()

    n = doc.styles["Normal"]
    n.font.name = "Calibri"
    n.font.size = Pt(st["body"])
    n.font.color.rgb = BLACK
    n.paragraph_format.space_after = Pt(0)
    n.paragraph_format.line_spacing = st["spacing"]

    for name, size in (("Heading 1", st["h1"]), ("Heading 2", st["h2"])):
        s = doc.styles[name]
        s.font.name = "Calibri"
        s.font.size = Pt(size)
        s.font.bold = True
        s.font.italic = name == "Heading 2"
        s.font.color.rgb = BLACK
        s.paragraph_format.keep_with_next = True
        s.paragraph_format.space_before = Pt(0 if name == "Heading 1" else 14)
        s.paragraph_format.space_after = Pt(5)

    text_width = Cm(21.0 - st["side"] * 2)
    first_book = True
    prev_book = prev_section = None
    n_q = 0

    for it in items:
        if it["book"] != prev_book:
            sec = doc.sections[0] if first_book else doc.add_section(WD_SECTION.ODD_PAGE)
            sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
            sec.left_margin = sec.right_margin = Cm(st["side"])
            sec.top_margin = sec.bottom_margin = Cm(st["vert"])
            first_book = False
            prev_book = it["book"]
            prev_section = None
            doc.add_heading(it["book"].upper(), level=1)
            if st["rule"]:
                rule(doc)

        if it.get("section") and it["section"] != prev_section and it["section"].lower() != it["book"].lower():
            doc.add_heading(it["section"], level=2)
            prev_section = it["section"]

        n_q += 1
        tag = doc.add_paragraph()
        tag.paragraph_format.space_before = Pt(st["gap"])
        tag.paragraph_format.space_after = Pt(2)
        tag.paragraph_format.keep_with_next = True
        tr = tag.add_run(it["tag"].strip() or f"DIBY [{letter_label(n_q)}]")
        tr.bold = True
        tr.font.size = Pt(st["tag"])
        tr.font.color.rgb = BLACK

        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.tab_stops.add_tab_stop(text_width, WD_TAB_ALIGNMENT.RIGHT)
        q.paragraph_format.keep_with_next = True
        for kind, val in segments(it["question"]):
            if kind == "math" and val in omml:
                q._p.append(copy.deepcopy(omml[val]))
            elif kind == "math":
                q.add_run(latex_fallback(val))
            else:
                r = q.add_run(val)
                r.italic = True
        ans = answer_short(it.get("answer", ""))
        if ans:
            r = q.add_run("\t")
            for kind, val in segments(ans):
                if kind == "math" and val in omml:
                    q._p.append(copy.deepcopy(omml[val]))
                else:
                    r2 = q.add_run(latex_fallback(val) if kind == "math" else val)
                    r2.bold = True

        if it.get("options"):
            op = doc.add_paragraph()
            op.paragraph_format.space_after = Pt(2)
            op.paragraph_format.left_indent = Cm(0.6)
            for kind, val in segments(it["options"]):
                if kind == "math" and val in omml:
                    op._p.append(copy.deepcopy(omml[val]))
                else:
                    r = op.add_run(latex_fallback(val) if kind == "math" else val)
                    r.font.size = Pt(st["opt"])

    doc.save(out)
    return out, n_q


def main():
    items = json.load(open(SRC))
    if not items:
        print("no items")
        return
    items.sort(key=lambda r: (r["book"], r["pdf_page"], int(re.sub(r"\D", "", r["tag"]) or 0)))

    all_latex = []
    for it in items:
        all_latex += [v for k, v in segments(it["question"]) if k == "math"]
        all_latex += [v for k, v in segments(it.get("options", "")) if k == "math"]
    omml = latex_to_omml(all_latex)
    print(f"equations rendered: {len(omml)} of {len(set(all_latex))} unique maths spans")

    for style in ("compact", "print"):
        path, n = build(style, items, omml, set())
        print(f"{style:8s}: {n} questions -> {os.path.relpath(path, ROOT)}")

    print("\nper book:")
    for book, cnt in Counter(i["book"] for i in items).most_common():
        print(f"   {cnt:4d}  {book}")


if __name__ == "__main__":
    main()
