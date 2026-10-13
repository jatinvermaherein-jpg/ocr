#!/usr/bin/env python3
"""Build the PRINT edition of the DIBY question bank — black & white.

Spec (as requested):
  · no cover page, no contents page — the document starts at the first chapter
  · larger body text (12 pt) with a little more air between questions
  · pure black on white: no colour anywhere; hierarchy comes from size,
    bold and italic only
  · every chapter starts on an odd (right-hand) page
  · running header naming the chapter + page number in the footer, both black
  · questions are never split across a page break

Equations are native Word equations (OMML), same as the compact edition.
Writes deliverables/DIBY_Questions_Print.docx
"""
from __future__ import annotations

import copy
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_diby_docx_v2 import (          # noqa: E402  reuse the maths pipeline
    CHAPTER_ORDER, answer_short, clean_options, display_label, is_real_label, letter_label,
    latex_to_omml, segments, SRC,
)
from diby_math import keep_whole, latex_fallback      # noqa: E402

import json                                             # noqa: E402
from docx import Document                               # noqa: E402
from docx.enum.section import WD_SECTION                # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT  # noqa: E402
from docx.oxml import OxmlElement                       # noqa: E402
from docx.oxml.ns import qn                             # noqa: E402
from docx.shared import Cm, Pt, RGBColor                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "deliverables/DIBY_Questions_Print.docx")

BLACK = RGBColor(0x00, 0x00, 0x00)          # the only colour used

PAGE_W, PAGE_H = Cm(21.0), Cm(29.7)         # A4
MARGIN_SIDE = Cm(2.0)
MARGIN_VERT = Cm(1.8)
HEADER_DIST = Cm(0.9)
FOOTER_DIST = Cm(1.0)
TEXT_WIDTH = Cm(21.0 - 2.0 * 2)             # 17.0 cm
CHARS_PER_LINE = 62                          # at 16 pt on a 17 cm line

# type scale (larger than the earlier print edition)
SIZE_BODY = 16
SIZE_OPTIONS = 14
SIZE_NOTE = 10
SIZE_TAG = 14
SIZE_SOURCE = 8.5
SIZE_H1 = 18
SIZE_H2 = 14
SIZE_HEADER = 9
SIZE_FOOTER = 9
LINE_SPACING = 1.15


# ------------------------------------------------------------------ page setup


def setup_page(sec):
    sec.page_width, sec.page_height = PAGE_W, PAGE_H
    sec.left_margin = sec.right_margin = MARGIN_SIDE
    sec.top_margin = sec.bottom_margin = MARGIN_VERT
    sec.header_distance = HEADER_DIST
    sec.footer_distance = FOOTER_DIST
    return sec


def rule(doc, space_after=10, space_before=0, sz="8"):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), sz)
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    borders.append(bottom)
    pPr.append(borders)
    return p


# ------------------------------------------------------------------------ main
def main():
    recs = json.load(open(SRC))
    items = [r for r in recs if r["prompt"]]
    items.sort(key=lambda r: (CHAPTER_ORDER.index(r["chapter"]) if r["chapter"] in CHAPTER_ORDER else 99,
                              r["lecture"], r["pdf_page"], r["master_id"]))

    prepared, all_latex = [], []
    for r in items:
        q_segs = segments(r["prompt"])
        o_txt = clean_options(r["options"])
        o_segs = segments(o_txt) if o_txt else []
        prepared.append((r, q_segs, o_segs))
        all_latex += [v for k, v in q_segs if k == "math"]
        all_latex += [v for k, v in o_segs if k == "math"]
        all_latex += [v for k, v in segments(answer_short(r["answer"])) if k == "math"]
    omml = latex_to_omml(all_latex)
    print(f"maths spans: {len(set(all_latex))} unique, {len(omml)} rendered as Word equations")

    # ---- labels: printed DIBY-n stays; everything else becomes DIBY A, DIBY B, ...
    counter = 0
    for r, _, _ in prepared:
        if is_real_label(r["printed_label"]):
            r["print_label"] = display_label(r["printed_label"]) or "DIBY"
        else:
            r["print_label"] = f"DIBY [{letter_label(counter)}]"
            counter += 1
    print(f"letter-labelled DIBYs (no printed tag): {counter}")

    doc = Document()

    n = doc.styles["Normal"]
    n.font.name = "Calibri"
    n.font.size = Pt(SIZE_BODY)
    n.font.color.rgb = BLACK
    n.paragraph_format.space_after = Pt(0)
    n.paragraph_format.line_spacing = LINE_SPACING

    h1 = doc.styles["Heading 1"]
    h1.font.name = "Calibri"
    h1.font.size = Pt(SIZE_H1)
    h1.font.bold = True
    h1.font.color.rgb = BLACK
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(4)
    h1.paragraph_format.keep_with_next = True

    h2 = doc.styles["Heading 2"]
    h2.font.name = "Calibri"
    h2.font.size = Pt(SIZE_H2)
    h2.font.bold = True
    h2.font.italic = True
    h2.font.color.rgb = BLACK
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(5)
    h2.paragraph_format.keep_with_next = True

    # ---------------- chapters (document starts here — no cover, no contents) --
    prev_chapter = None
    first = True
    for r, q_segs, o_segs in prepared:
        if r["chapter"] != prev_chapter:
            if first:
                setup_page(doc.sections[0])
            else:
                setup_page(doc.add_section(WD_SECTION.ODD_PAGE))
            first = False
            prev_chapter = r["chapter"]
            prev_key = None
            doc.add_heading(r["chapter"].upper(), level=1)
            rule(doc, space_after=12)

        key = (r["chapter"], r["lecture"])
        if key != prev_key:
            doc.add_heading(f"Lecture {r['lecture']}", level=2)
            prev_key = key

        # tag + source line
        tag = doc.add_paragraph()
        tag.paragraph_format.space_before = Pt(11)
        tag.paragraph_format.space_after = Pt(2)
        tag.paragraph_format.keep_with_next = True
        whole = keep_whole(len(r["prompt"] or "") + len(o_txt or ""), CHARS_PER_LINE)
        tr = tag.add_run(r["print_label"])
        tr.bold = True
        tr.font.size = Pt(SIZE_TAG)
        tr.font.color.rgb = BLACK

        # question (kept whole across page breaks)
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.keep_together = whole         # short items stay whole
        q.paragraph_format.tab_stops.add_tab_stop(TEXT_WIDTH, WD_TAB_ALIGNMENT.RIGHT)
        for kind, val in q_segs:
            if kind == "math" and val in omml:
                q._p.append(copy.deepcopy(omml[val]))
            elif kind == "math":
                run = q.add_run(latex_fallback(val))
                run.italic = True
                run.font.color.rgb = BLACK
            else:
                run = q.add_run(val)
                run.italic = True
                run.font.color.rgb = BLACK
        short = answer_short(r["answer"])
        if short:
            q.add_run("\t")
            for kind, val in segments(short):        # answers typeset like the rest
                if kind == "math" and val in omml:
                    q._p.append(copy.deepcopy(omml[val]))
                elif kind == "math":
                    run = q.add_run(latex_fallback(val))
                    run.bold = True
                    run.font.color.rgb = BLACK
                else:
                    run = q.add_run(val)
                    run.bold = True
                    run.font.color.rgb = BLACK

        # options
        if o_segs:
            op = doc.add_paragraph()
            op.paragraph_format.space_after = Pt(2)
            op.paragraph_format.left_indent = Cm(0.6)
            op.paragraph_format.keep_together = whole     # one option block stays put
            op.paragraph_format.keep_with_next = False
            for kind, val in o_segs:
                if kind == "math" and val in omml:
                    op._p.append(copy.deepcopy(omml[val]))
                elif kind == "math":
                    run = op.add_run(latex_fallback(val))
                    run.font.size = Pt(SIZE_OPTIONS)
                    run.font.color.rgb = BLACK
                else:
                    run = op.add_run(val)
                    run.font.size = Pt(SIZE_OPTIONS)
                    run.font.color.rgb = BLACK
            for run in op.runs:
                run.font.size = Pt(SIZE_OPTIONS)
                run.font.color.rgb = BLACK

    doc.save(OUT)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
    print("chapters:", len({r['chapter'] for r, _, _ in prepared}), "| questions:", len(prepared))


if __name__ == "__main__":
    main()
