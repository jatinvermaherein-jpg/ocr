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
from diby_math import (                                # noqa: E402
    latex_fallback, keep_whole, smart_segments as segments, repair_latex,
)

from docx import Document                              # noqa: E402
from docx.enum.section import WD_SECTION               # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT  # noqa: E402
from docx.oxml import OxmlElement                       # noqa: E402
from docx.oxml.ns import qn                             # noqa: E402
from docx.shared import Cm, Pt, RGBColor                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "deliverables/diby-books/diby_books.json")
BLACK = RGBColor(0, 0, 0)

# Type scale: question 16 pt, DIBY number 14 pt; the book heading keeps its old size.
STYLES = {
    "print": dict(out="deliverables/DIBY_Books_Print.docx", body=16, opt=14, tag=14,
                  h1=18, h2=13.5, side=2.0, vert=1.8, spacing=1.15, gap=11, rule=True, cpl=62),
    "compact": dict(out="deliverables/DIBY_Books.docx", body=16, opt=13, tag=14,
                    h1=15, h2=12, side=1.5, vert=1.3, spacing=0.95, gap=7, rule=False, cpl=74),
}


def _space_needed(prev: str, nxt: str) -> bool:
    """Should a space go between two runs of different kinds (text <-> maths)?"""
    if not prev or not nxt:
        return False
    if prev[-1].isspace() or nxt[0].isspace():
        return False
    if prev[-1] in "(\u2013-":
        return False
    if nxt[0] in ",;.)]}=":
        return False
    return True


def emit_spans(par, pieces, omml, *, size=None, bold=False, italic=False, colour=None):
    """Add [(kind, value)] pieces to a paragraph, keeping spaces around equations.

    Word renders an inline OMML equation without any space of its own, so a text run
    ending in a letter followed by an equation (or the other way round) would read
    'thena(a-b)+...'. Insert a plain space run at those junctions.
    """
    prev_kind = prev_val = None
    for kind, val in pieces:
        if not val:
            continue
        if prev_kind is not None and kind != prev_kind and _space_needed(prev_val, val):
            par.add_run(" ")
        if kind == "math" and val in omml:
            par._p.append(copy.deepcopy(omml[val]))
        else:
            r = par.add_run(latex_fallback(val) if kind == "math" else val)
            if size:
                r.font.size = Pt(size)
            r.bold = bold
            r.italic = italic
            if colour:
                r.font.color.rgb = colour
        prev_kind, prev_val = kind, val
    return par


def underline_rule(par, space="1"):
    """Draw the horizontal rule as the paragraph's own bottom border.

    It used to be a separate empty paragraph. That empty paragraph was the only thing
    between a book heading and its first item, and it carried no `keepNext`, so a
    reader (or any viewer that lays the section break out differently) could leave the
    heading sitting alone at the bottom of a page with the first DIBY overleaf.
    Attaching the border to the heading means nothing can come between the two.
    """
    pPr = par._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), space)
    bottom.set(qn("w:color"), "000000")
    borders.append(bottom)
    pPr.append(borders)
    return par


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
            head = doc.add_heading(it["book"].upper(), level=1)
            head.paragraph_format.keep_with_next = True      # never orphan the heading
            head.paragraph_format.space_after = Pt(8)
            if st["rule"]:
                underline_rule(head)

        if it.get("section") and it["section"] != prev_section and it["section"].lower() != it["book"].lower():
            doc.add_heading(it["section"], level=2)
            prev_section = it["section"]

        n_q += 1
        # A tall item cannot be kept whole without leaving half a page empty, so only
        # items short enough to fit comfortably are glued together; longer ones may
        # split across the page break and let the page fill up.
        tally = "\t".join(filter(None, (
            it["tag"].strip(),
            it["question"] or "",
            it.get("options") or "",
            answer_short(it.get("answer", "")),
        )))
        whole = keep_whole(len(tally), st["cpl"])

        tag = doc.add_paragraph()
        tag.paragraph_format.space_before = Pt(st["gap"])
        tag.paragraph_format.space_after = Pt(2)
        tag.paragraph_format.keep_with_next = True          # never orphan a DIBY number
        tr = tag.add_run(it["tag"].strip() or f"DIBY [{letter_label(n_q)}]")
        tr.bold = True
        tr.font.size = Pt(st["tag"])
        tr.font.color.rgb = BLACK

        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.tab_stops.add_tab_stop(text_width, WD_TAB_ALIGNMENT.RIGHT)
        # keepNext is NOT set here on purpose: it would glue this item's question to
        # the next item's tag, and a chain of keepNext paragraphs is what makes Word
        # push whole blocks over and leave half a page empty.
        q.paragraph_format.keep_together = whole
        q.paragraph_format.keep_with_next = bool(it.get("options")) and whole
        emit_spans(q, segments(it["question"]), omml, italic=True, colour=BLACK)
        ans = answer_short(it.get("answer", ""))
        if ans:
            q.add_run("\t")
            emit_spans(q, segments(ans), omml, bold=True, colour=BLACK)

        if it.get("options"):
            op = doc.add_paragraph()
            op.paragraph_format.space_after = Pt(2)
            op.paragraph_format.left_indent = Cm(0.6)
            op.paragraph_format.keep_together = whole
            op.paragraph_format.keep_with_next = False
            emit_spans(op, segments(it["options"]), omml, size=st["opt"], colour=BLACK)

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
        all_latex += [v for k, v in segments(answer_short(it.get("answer", ""))) if k == "math"]
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
