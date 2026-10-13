#!/usr/bin/env python3
"""Build a PRINT-READY, professional DIBY question bank DOCX.

Differences from the compact edition (deliverables/DIBY_Questions.docx):
  · cover page + contents page, chapters start on odd (right-hand) pages
  · comfortable print margins (2.2 cm sides / 2.0 cm vertical)
  · body text 11 pt with 1.15 line spacing and clear space between questions
  · real Word Heading styles for chapter/lecture, so the contents field,
    the navigation pane and the outline all work
  · running header naming the current chapter (thin rule), page number centred
    in the footer; cover page carries no number
  · questions are kept whole — a question never splits across a page break
  · answers bold and right-aligned; options and notes indented, print-legible
  · ink-friendly: navy headings, black body text

Equations are the same native Word equations (OMML) as the compact edition.

Writes deliverables/DIBY_Questions_Print.docx
"""
from __future__ import annotations

import copy
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_diby_docx_v2 import (          # noqa: E402  reuse the maths pipeline
    CHAPTER_ORDER, GREY, clean_answer, clean_options, latex_to_omml, norm_tag, segments, SRC,
)

from docx import Document                              # noqa: E402
from docx.enum.section import WD_SECTION               # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER  # noqa: E402
from docx.oxml import OxmlElement                       # noqa: E402
from docx.oxml.ns import qn                             # noqa: E402
from docx.shared import Cm, Pt, RGBColor                # noqa: E402
from lxml import etree                                  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "deliverables/DIBY_Questions_Print.docx")

NAVY = RGBColor(0x1B, 0x2F, 0x5C)
INK = RGBColor(0x11, 0x11, 0x11)

PAGE_W, PAGE_H = Cm(21.0), Cm(29.7)          # A4
MARGIN_SIDE = Cm(2.2)
MARGIN_VERT = Cm(2.0)
FOOTER_DIST = Cm(1.1)
HEADER_DIST = Cm(1.0)
TEXT_WIDTH = Cm(21.0 - 2.2 * 2)              # 16.6 cm


# ------------------------------------------------------------------ page setup
def setup_page(sec, number_pages=True):
    sec.page_width, sec.page_height = PAGE_W, PAGE_H
    sec.left_margin = sec.right_margin = MARGIN_SIDE
    sec.top_margin = sec.bottom_margin = MARGIN_VERT
    sec.header_distance = HEADER_DIST
    sec.footer_distance = FOOTER_DIST
    if number_pages:
        add_page_number(sec)
    return sec


def _field(par, instr: str, cached: str = "1", size=9, italic=False):
    r1 = par.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    r1._r.append(begin)

    r2 = par.add_run()
    ins = OxmlElement("w:instrText")
    ins.set(qn("xml:space"), "preserve")
    ins.text = instr
    r2._r.append(ins)

    r3 = par.add_run()
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    r3._r.append(sep)

    r4 = par.add_run(cached)
    r4.font.size = Pt(size)
    r4.italic = italic

    r5 = par.add_run()
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    r5._r.append(end)
    return par


def add_page_number(sec):
    sec.footer.is_linked_to_previous = False
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _field(p, " PAGE ", cached="1", size=9)


def add_header(sec, chapter: str):
    sec.header.is_linked_to_previous = False
    p = sec.header.paragraphs[0]
    p.paragraph_format.tab_stops.add_tab_stop(TEXT_WIDTH, WD_TAB_ALIGNMENT.RIGHT)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(chapter.upper())
    r.font.size = Pt(8.5)
    r.bold = True
    r.font.color.rgb = NAVY
    r2 = p.add_run("\tDIBY — Question Bank")
    r2.font.size = Pt(8.5)
    r2.italic = True
    r2.font.color.rgb = GREY
    # thin rule under the header
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), "9AA7BD")
    borders.append(bottom)
    pPr.append(borders)


def blank_header_footer(sec):
    sec.header.is_linked_to_previous = False
    sec.footer.is_linked_to_previous = False


def keep_whole(par):
    par.paragraph_format.keep_together = True
    return par


def rule(doc, color="BFBFBF", space_after=10, space_before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    pPr.append(borders)
    return p


def toc_field(doc, entries):
    """Real TOC field whose cached result is a always-readable contents list."""
    p0 = doc.add_paragraph()
    p0.paragraph_format.space_after = Pt(6)
    _field(p0, r'TOC \o "1-2" \h \z \u', cached="", size=10)
    # cached result: everything between 'separate' and 'end'
    last = None
    for text, level, count in entries:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        if level == 1:
            p.paragraph_format.space_before = Pt(8)
            r = p.add_run(text)
            r.bold = True
            r.font.size = Pt(11)
            r.font.color.rgb = NAVY
        else:
            p.paragraph_format.left_indent = Cm(0.8)
            r = p.add_run(text)
            r.font.size = Pt(10)
        r2 = p.add_run(f"   ({count})")
        r2.font.size = Pt(8.5)
        r2.italic = True
        r2.font.color.rgb = GREY
        last = p
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    last.add_run()._r.append(end)
    return p0


def update_fields_on_open(doc):
    """Make Word/LibreOffice refresh the TOC when the file is opened."""
    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)


# ------------------------------------------------------------------------ main
def main():
    import json
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
    omml = latex_to_omml(all_latex)
    print(f"maths spans: {len(set(all_latex))} unique, {len(omml)} rendered as Word equations")

    doc = Document()

    # ---- named styles so the TOC/outline/navigation pane work -----------------
    n = doc.styles["Normal"]
    n.font.name = "Calibri"
    n.font.size = Pt(11)
    n.font.color.rgb = INK
    n.paragraph_format.space_after = Pt(0)
    n.paragraph_format.line_spacing = 1.15

    h1 = doc.styles["Heading 1"]
    h1.font.name = "Calibri"
    h1.font.size = Pt(17)
    h1.font.bold = True
    h1.font.color.rgb = NAVY
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(4)
    h1.paragraph_format.keep_with_next = True

    h2 = doc.styles["Heading 2"]
    h2.font.name = "Calibri"
    h2.font.size = Pt(13)
    h2.font.bold = True
    h2.font.italic = True
    h2.font.color.rgb = NAVY
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.keep_with_next = True

    # ---------------- cover ----------------
    sec1 = setup_page(doc.sections[0], number_pages=False)
    blank_header_footer(sec1)

    for _ in range(5):
        doc.add_paragraph()
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("DIBY")
    r.bold = True
    r.font.size = Pt(54)
    r.font.color.rgb = NAVY
    t2 = doc.add_paragraph()
    t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t2.add_run("Do It By Yourself — Question Bank")
    r.font.size = Pt(18)
    r.font.color.rgb = INK
    t3 = doc.add_paragraph()
    t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t3.add_run("Consolidated from the ARJUNA JEE 2027 mathematics class notes")
    r.font.size = Pt(12)
    r.italic = True
    r.font.color.rgb = GREY
    doc.add_paragraph()
    rule(doc, color="1B2F5C", space_after=10)
    qc = Counter(r["prompt_source"].split("(")[0].strip() for r, _, _ in prepared)
    n_ver = qc.get("verified visual transcription", 0)
    n_ext = qc.get("dual-pass OCR extraction, not visually QA'd", 0)
    n_drf = qc.get("raw OCR reconstructed from the same page", 0)
    st = doc.add_paragraph()
    st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = st.add_run(f"{len(prepared)} questions  ·  {len(CHAPTER_ORDER)} chapters  ·  "
                   f"{n_ver} verified, {n_ext} ocr-extract, {n_drf} ocr-draft")
    r.font.size = Pt(11)
    for line in ["Text taken from the class-note slides exactly as printed — no mathematical "
                 "corrections or rewording.",
                 "Equations are typeset. Items marked ocr-draft are raw OCR and should be checked "
                 "against the source PDF page shown with each question.",
                 "Section/divider slides that carry a DIBY mark but no question of their own are "
                 "listed in the repository registers, not here."]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rr = p.add_run(line)
        rr.font.size = Pt(9)
        rr.italic = True
        rr.font.color.rgb = GREY

    # ---------------- contents ----------------
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_page(sec2)
    blank_header_footer(sec2)
    h = doc.add_heading("Contents", level=1)
    h.paragraph_format.space_after = Pt(8)
    entries = []
    for ch in CHAPTER_ORDER:
        ch_q = [x for x in prepared if x[0]["chapter"] == ch]
        if not ch_q:
            continue
        entries.append((ch, 1, len(ch_q)))
        for lect in sorted({x[0]["lecture"] for x in ch_q}):
            l_q = [x for x in ch_q if x[0]["lecture"] == lect]
            entries.append((f"Lecture {lect}", 2, len(l_q)))
    toc_field(doc, entries)
    update_fields_on_open(doc)

    # ---------------- chapters ----------------
    prev_chapter = None
    for r, q_segs, o_segs in prepared:
        if r["chapter"] != prev_chapter:
            if prev_chapter is None:
                sec = doc.add_section(WD_SECTION.ODD_PAGE)
            else:
                sec = doc.add_section(WD_SECTION.ODD_PAGE)
            setup_page(sec)
            add_header(sec, r["chapter"])
            prev_chapter = r["chapter"]
            prev_key = None
            doc.add_heading(r["chapter"].upper(), level=1)
            rule(doc, color="C9D2E0", space_after=12)
            n_ch = sum(1 for x in prepared if x[0]["chapter"] == r["chapter"])
            meta = doc.add_paragraph()
            meta.paragraph_format.space_after = Pt(2)
            mr = meta.add_run(f"{n_ch} questions in this chapter · questions are grouped by lecture "
                              "and shown in source order")
            mr.font.size = Pt(9)
            mr.italic = True
            mr.font.color.rgb = GREY

        key = (r["chapter"], r["lecture"])
        if key != prev_key:
            doc.add_heading(f"Lecture {r['lecture']} — {r['source_pdf']}", level=2)
            prev_key = key

        # tag + source line
        tag = doc.add_paragraph()
        tag.paragraph_format.space_before = Pt(10)
        tag.paragraph_format.space_after = Pt(2)
        tag.paragraph_format.keep_with_next = True
        tr = tag.add_run(norm_tag(r["printed_label"], r["internal_id"], r["marker_text"]))
        tr.bold = True
        tr.font.size = Pt(10.5)
        tr.font.color.rgb = NAVY
        pg = tag.add_run(f"   ·   {r['source_pdf']} — PDF page {r['pdf_page']}")
        pg.font.size = Pt(8)
        pg.italic = True
        pg.font.color.rgb = GREY

        # question (kept whole across page breaks)
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.tab_stops.add_tab_stop(TEXT_WIDTH, WD_TAB_ALIGNMENT.RIGHT)
        keep_whole(q)
        for kind, val in q_segs:
            if kind == "math" and val in omml:
                q._p.append(copy.deepcopy(omml[val]))
            else:
                run = q.add_run(val)
                run.italic = True
        short, long_note = clean_answer(r["answer"])
        if short:
            tab = q.add_run("\t" + short)
            tab.bold = True
            tab.font.color.rgb = INK

        # options
        if o_segs:
            op = doc.add_paragraph()
            op.paragraph_format.space_after = Pt(2)
            op.paragraph_format.left_indent = Cm(0.6)
            keep_whole(op)
            for kind, val in o_segs:
                if kind == "math" and val in omml:
                    op._p.append(copy.deepcopy(omml[val]))
                else:
                    run = op.add_run(val)
                    run.font.size = Pt(10)
            for run in op.runs:
                run.font.size = Pt(10)

        # long answer note
        if long_note:
            an = doc.add_paragraph()
            an.paragraph_format.space_after = Pt(2)
            an.paragraph_format.left_indent = Cm(0.6)
            ar = an.add_run(long_note)
            ar.italic = True
            ar.font.size = Pt(9)
            ar.font.color.rgb = GREY

    doc.save(OUT)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
    print("chapters:", len({r['chapter'] for r, _, _ in prepared}), "| questions:", len(prepared))


if __name__ == "__main__":
    main()
