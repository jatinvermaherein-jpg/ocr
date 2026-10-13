#!/usr/bin/env python3
"""Build the DIBY question-bank DOCX in the requested layout:

    Chapter, Lecture NN                 <- one title per chapter+lecture
    DIBY-02   ·  page 37                <- tag (+ where it comes from)
    <italic question with real typeset equations>          [Ans.: 13]
      options (small, grey)
    (blank line)  ... next DIBY ... then the next title

Equations are converted from the OCR text to LaTeX and rendered as native Word
equations (OMML) through pandoc, so they look typeset instead of "(x^m + 1/x^2)^22".
Section markers (slides with a DIBY mark but no question) are not included.
"""
from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diby_math import (                                       # noqa: E402
    smart_segments, keep_whole, est_lines, latex_fallback, repair_latex,
)

segments = smart_segments                                       # noqa: E402

CPRINT = 88   # characters per line in the compact edition (10.5 pt on ~18 cm)

import pypandoc                                  # noqa: E402
from docx import Document                        # noqa: E402
from docx.enum.section import WD_SECTION                  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT  # noqa: E402
from docx.oxml import OxmlElement                # noqa: E402
from docx.oxml.ns import qn                      # noqa: E402
from docx.shared import Cm, Pt, RGBColor         # noqa: E402
from lxml import etree                           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "deliverables/DIBY_Master.json")
OUT = os.path.join(ROOT, "deliverables/DIBY_Questions.docx")
CSV_OUT = os.path.join(ROOT, "deliverables/DIBY_Questions.csv")

CHAPTER_ORDER = ["Binomial Theorem", "Permutations & Combinations", "Quadratic Equations",
                 "Trigonometric Equation", "Trigonometric Functions", "Sequence and Series"]
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

GREY = RGBColor(0x77, 0x77, 0x77)
ANSWER_BLUE = RGBColor(0x11, 0x55, 0x99)

# ---- page geometry (compact but readable) -----------------------------------
PAGE_W, PAGE_H = Cm(21.0), Cm(29.7)      # A4
MARGIN_SIDE = Cm(1.5)
MARGIN_VERT = Cm(1.3)
TEXT_WIDTH = Cm(18.0)                    # 21.0 - 1.5 - 1.5


def setup_page(sec):
    sec.page_width, sec.page_height = PAGE_W, PAGE_H
    sec.left_margin = sec.right_margin = MARGIN_SIDE
    sec.top_margin = sec.bottom_margin = MARGIN_VERT
    sec.header_distance = Cm(0.7)
    sec.footer_distance = Cm(0.7)
    return sec


def add_footer_page_number(sec):
    """Centred page number in the footer, so odd/even chapter starts are visible."""
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.font.size = Pt(8)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), " PAGE ")
    inner = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "16")
    rpr.append(sz)
    inner.append(rpr)
    t = OxmlElement("w:t")
    t.text = "1"
    inner.append(t)
    fld.append(inner)
    p._p.append(fld)


# --------------------------------------------------------------------- helpers
LABEL_RE = re.compile(r"DIBY\s*[-\u2013]?\s*\(?\s*([0-9]{1,3}|[A-Za-z])\s*\)?(?![A-Za-z0-9])", re.I)


def is_real_label(lbl: str) -> bool:
    """A printed label carries a DIBY number (DIBY-12, #DIBY-7) or a letter (DIBY-X, DIBY-Y)."""
    return bool(LABEL_RE.search(lbl or ""))


def display_label(lbl: str) -> str:
    """Clean printed tag: '# DIBY-36(Challenger)' -> 'DIBY-36', 'DiBY - (X) [handwritten]' -> 'DIBY-X'."""
    m = LABEL_RE.search(lbl or "")
    return f"DIBY-{m.group(1).upper()}" if m else ""


def letter_label(n: int) -> str:
    """0 -> A, 1 -> B, ... 25 -> Z, 26 -> AA (for DIBYs with no printed tag)."""
    n += 1
    out = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out


COMMENTARY = re.compile(r"\b(slide|board|handwrit|cyan|red box|ticked|working|"
                       r"pre-filled|homework|unclear|illegible|on-board|see |on p\d|"
                       r"SOLVED|not on this)\b", re.I)
NO_ANSWER = re.compile(r"\bnone shown\b|\bnot shown\b|four dots|assigned as homework|"
                       r"\bblank in the source\b", re.I)
JUNK_ANSWER = re.compile(r"^[\s.\-_(]*\)?[\s.\-…]*$")


def answer_short(ans: str) -> str:
    """Return a clean short answer; all descriptive commentary is dropped."""
    ans = (ans or "").strip()
    if not ans or ans.lower().startswith("none"):
        return ""
    if NO_ANSWER.search(ans) and "[Ans." not in ans:
        return ""

    def tidy(v: str) -> str:
        v = re.sub(r"\bAns\.?\s*[:.]?\s*", "", v.strip(), flags=re.I)      # inner "Ans.:" too
        v = re.sub(r"\s*\([^)]*(?:printed|red box|cyan|handwrit|ticked|slide|board|"
                   r"pre-filled|homework)[^)]*\)?", "", v, flags=re.I)
        v = re.sub(r"\s{2,}", " ", v).strip(" ;,")          # keep a leading minus!
        v = re.sub(r"[\s;:.]+$", "", v).strip()
        return "" if not v or JUNK_ANSWER.match(v) or not re.search(r"[A-Za-z0-9]", v) else v

    # 1) list-style answer, e.g. "(i) y in (-inf, -2], (ii) ..."
    if re.match(r"^\s*\(\s*i\s*\)", ans) and len(ans) <= 90 and not COMMENTARY.search(ans):
        v = tidy(ans)
        if v:
            return f"[Ans.: {v}]"

    # 2) bracketed answer anywhere
    m = re.search(r"\[\s*Ans\.?\s*:?\s*([^\]]{1,90})\]", ans, re.I)
    if m:
        v = tidy(m.group(1))
        if v:
            return f"[Ans.: {v}]"

    # 3) "Ans.: …" prefix — take the value, cut off commentary that follows
    m = re.match(r"^\s*Ans\.?\s*[:.]?\s*(.+)$", ans, re.I)
    if m:
        v = re.split(r";|\s\(on-board|\bboard\b", m.group(1))[0]
        v = re.split(r"\.\s+(?=[A-Z])", v)[0]          # drop a trailing sentence
        v = tidy(v)
        if v and len(v) <= 60:
            return f"[Ans.: {v}]"

    # 4) option letter at the start
    m = re.match(r"^\s*\(([A-Da-d])\)", ans)
    if m:
        return f"[Ans.: ({m.group(1).upper()})]"

    # 5) already a short, plain answer
    if len(ans) <= 60 and not COMMENTARY.search(ans):
        v = tidy(ans)
        if v:
            return f"[Ans.: {v}]"
    return ""


def norm_tag(label: str, internal: str, marker: str) -> str:
    """Display tag: normalise '#DIBY-36' -> 'DIBY-36'."""
    lab = (label or "").strip().lstrip("#").strip()
    lab = re.sub(r"\s{2,}", " ", lab)
    if re.match(r"(?i)^diby\s*-\s*", lab):
        lab = re.sub(r"(?i)^diby\s*-\s*", "DIBY-", lab)
        lab = re.sub(r"(?i)^DIBY-(\d)\s*\(", r"DIBY-\1 (", lab)
    if not lab or lab.lower().startswith("none"):
        lab = internal.strip() or (marker.strip() if marker.strip() else "DIBY (no tag printed)")
    return lab


def clean_answer(ans: str) -> tuple[str, str]:
    """Return (short_inline_answer, long_note)."""
    ans = (ans or "").strip()
    if not ans:
        return "", ""
    if ans.lower().startswith("none"):
        return "", ""

    def tidy(v: str) -> str:
        v = re.sub(r"^Ans\.?\s*[:.]?\s*", "", v.strip(), flags=re.I).strip()
        if not v or re.fullmatch(r"[\.\-_·…\s]+", v) or len(re.sub(r"[^A-Za-z0-9]", "", v)) == 0:
            return ""
        return v

    m = re.search(r"\[\s*Ans\.?\s*:?\s*([^\]]{1,40})\]", ans)
    if m and tidy(m.group(1)):
        return f"[Ans.: {tidy(m.group(1))}]", ""
    m = re.match(r"^Ans\.?\s*[:.]?\s*([^(\[]+?)\s*[(\[]", ans)
    if m and tidy(m.group(1)):
        return f"[Ans.: {tidy(m.group(1))}]", ans
    m = re.match(r"^Ans\.?\s*[:.]?\s*([^(\[]+)$", ans)
    if m and tidy(m.group(1)):
        return f"[Ans.: {tidy(m.group(1))}]", ""
    if len(ans) <= 24 and tidy(ans):
        return f"[Ans.: {tidy(ans)}]", ""
    return "", ans


def clean_options(opts: str) -> str:
    o = (opts or "").strip()
    if not o or o.lower().startswith("none") or "no options" in o.lower():
        return ""
    if o.lower().startswith("not extracted"):
        return ""
    return o


# ------------------------------------------------------- batch LaTeX -> OMML
def _pandoc_batch(pairs: list[tuple[str, str]], key: str) -> dict[str, etree._Element]:
    """pairs: [(id, latex)] -> {id: oMath} for those pandoc could typeset."""
    if not pairs:
        return {}
    lines = []
    for ident, tex in pairs:
        lines.append(f"{key}{ident} ${tex}$")   # marker + maths in ONE paragraph
        lines.append("")
    with tempfile.TemporaryDirectory() as td:
        md = os.path.join(td, "m.md")
        dx = os.path.join(td, "m.docx")
        open(md, "w").write("\n".join(lines))
        pypandoc.convert_file(md, "docx", outputfile=dx,
                              extra_args=["--standalone", "--quiet"])
        with zipfile.ZipFile(dx) as z:
            root = etree.fromstring(z.read("word/document.xml"))
    out: dict[str, etree._Element] = {}
    for p in root.iter(f"{{{W_NS}}}p"):
        text = "".join(t.text or "" for t in p.iter(f"{{{W_NS}}}t"))
        m = re.search(key + r"(\d{5})", text)
        if not m:
            continue
        omml = p.find(f"{{{M_NS}}}oMath")
        if omml is not None:
            out[m.group(1)] = omml
    return out


def latex_to_omml(latex_list: list[str]) -> dict[str, etree._Element]:
    """Convert many LaTeX strings to OMML.

    Two pandoc passes: the raw spans first, then a mechanically repaired copy of
    whatever failed (OCR leftovers such as `\frac{6}{x^}` or a dangling `\left`).
    Anything still unparseable is printed as readable text by `latex_fallback`.
    """
    uniq = sorted(set(latex_list))
    if not uniq:
        return {}
    ids = {tex: f"{i:05d}" for i, tex in enumerate(uniq)}
    by_id = {v: k for k, v in ids.items()}
    got = _pandoc_batch([(ids[t], t) for t in uniq], "ZQ")
    retry = [(ident, repair_latex(by_id[ident])) for ident in sorted(by_id)
             if ident not in got]
    if retry:
        got.update(_pandoc_batch(retry, "ZR"))
    return {by_id[ident]: omml for ident, omml in got.items()}


# ------------------------------------------------------------------ docx bits
def add_math(par, omml):
    par._p.append(copy.deepcopy(omml))


def styled_heading(doc, text, size=13.5, space_before=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.line_spacing = 0.95
    r = p.add_run(text)
    r.bold = True
    r.italic = True
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    return p


def main():
    recs = json.load(open(SRC))
    items = [r for r in recs if r["prompt"]]
    items.sort(key=lambda r: (CHAPTER_ORDER.index(r["chapter"]) if r["chapter"] in CHAPTER_ORDER else 99,
                              r["lecture"], r["pdf_page"], r["master_id"]))

    # 1) work out math spans for question + options text
    prepared = []
    all_latex = []
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

    # labels: a printed DIBY number stays; anything else becomes DIBY A, DIBY B, ...
    counter = 0
    for r, _, _ in prepared:
        if is_real_label(r["printed_label"]):
            r["print_label"] = norm_tag(r["printed_label"], "", r["marker_text"])
        else:
            r["print_label"] = f"DIBY [{letter_label(counter)}]"
            counter += 1
    print(f"letter-labelled DIBYs (no printed tag): {counter}")

    # 2) build the document
    doc = Document()
    setup_page(doc.sections[0])
    text_width = TEXT_WIDTH

    n = doc.styles["Normal"]
    n.font.name = "Calibri"
    n.font.size = Pt(10.5)
    n.paragraph_format.space_after = Pt(0)
    n.paragraph_format.line_spacing = 0.95

    # compact title block (page 1, so chapter 1 still starts on an odd page)
    t = doc.add_paragraph()
    t.paragraph_format.space_before = Pt(0)
    t.paragraph_format.space_after = Pt(0)
    tr = t.add_run("DIBY — Question Bank")
    tr.bold = True
    tr.italic = True
    tr.font.size = Pt(14)
    tr.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    sub = doc.add_paragraph()
    sub.paragraph_format.space_after = Pt(8)
    qc = Counter(r["prompt_source"].split("(")[0].strip() for r, _, _ in prepared)
    n_ver = qc.get("verified visual transcription", 0)
    n_ext = qc.get("dual-pass OCR extraction, not visually QA'd", 0)
    n_drf = qc.get("raw OCR reconstructed from the same page", 0)
    sr = sub.add_run(f"{len(items)} questions · {n_ver} verified, {n_ext} ocr-extract, "
                     f"{n_drf} ocr-draft (unverified) · equations typeset; "
                     "OCR text not corrected — check ocr-draft items against the source page")
    sr.italic = True
    sr.font.size = Pt(8)
    sr.font.color.rgb = GREY

    add_footer_page_number(doc.sections[0])

    prev_chapter = None
    first_chapter = True
    for r, q_segs, o_segs in prepared:
        # every new chapter starts on an odd page
        if r["chapter"] != prev_chapter:
            if not first_chapter:
                sec = doc.add_section(WD_SECTION.ODD_PAGE)
                setup_page(sec)
            first_chapter = False
            prev_chapter = r["chapter"]
            prev_key = None
            ch = doc.add_paragraph()
            ch.paragraph_format.space_before = Pt(2)
            ch.paragraph_format.space_after = Pt(6)
            ch.paragraph_format.keep_with_next = True
            cr = ch.add_run(r["chapter"].upper())
            cr.bold = True
            cr.font.size = Pt(15)
            cr.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

        key = (r["chapter"], r["lecture"])
        if key != prev_key:
            styled_heading(doc, f"{r['chapter']}, Lecture {r['lecture']}")
            prev_key = key

        # short items stay on one page; tall ones may split so the page fills up
        whole = keep_whole(len(r["prompt"] or "") + len(o_txt or ""), CPRINT)

        # tag line
        tag = doc.add_paragraph()
        tag.paragraph_format.space_before = Pt(5)
        tag.paragraph_format.space_after = Pt(1)
        tag.paragraph_format.keep_with_next = True          # never orphan a DIBY number
        tr = tag.add_run(r["print_label"])
        tr.bold = True
        tr.font.size = Pt(10)

        # question paragraph (italic, maths inline, answer right-aligned)
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(1)
        q.paragraph_format.line_spacing = 0.95
        q.paragraph_format.keep_together = whole
        q.paragraph_format.tab_stops.add_tab_stop(text_width, WD_TAB_ALIGNMENT.RIGHT)
        for kind, val in q_segs:
            if kind == "math" and val in omml:
                add_math(q, omml[val])
            elif kind == "math":                      # pandoc could not typeset it
                run = q.add_run(latex_fallback(val))
                run.italic = True
            else:
                run = q.add_run(val)
                run.italic = True
        short = answer_short(r["answer"])
        if short:
            q.add_run("\t")
            for kind, val in segments(short):        # answers typeset like the rest
                if kind == "math" and val in omml:
                    add_math(q, omml[val])
                elif kind == "math":
                    run = q.add_run(latex_fallback(val))
                    run.italic = True
                    run.font.color.rgb = ANSWER_BLUE
                else:
                    run = q.add_run(val)
                    run.italic = True
                    run.font.color.rgb = ANSWER_BLUE

        # options line
        if o_segs:
            op = doc.add_paragraph()
            op.paragraph_format.space_after = Pt(1)
            op.paragraph_format.left_indent = Cm(0.35)
            op.paragraph_format.line_spacing = 0.92
            op.paragraph_format.keep_together = whole     # one option block stays put
            op.paragraph_format.keep_with_next = False
            for kind, val in o_segs:
                if kind == "math" and val in omml:
                    add_math(op, omml[val])
                elif kind == "math":                      # pandoc could not typeset it
                    run = op.add_run(latex_fallback(val))
                    run.font.size = Pt(9)
                    run.font.color.rgb = GREY
                else:
                    run = op.add_run(val)
                    run.italic = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = GREY

    doc.save(OUT)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")

    # 3) machine-readable side-car of exactly what is in the document
    import csv
    with open(CSV_OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["document_order", "tag", "chapter", "lecture", "source_pdf", "pdf_page",
                    "question_text", "options", "answer_shown", "text_quality", "master_id"])
        for i, (r, _, _) in enumerate(prepared, 1):
            w.writerow([i, norm_tag(r["printed_label"], r["internal_id"], r["marker_text"]),
                        r["chapter"], r["lecture"], r["source_pdf"], r["pdf_page"],
                        r["prompt"], clean_options(r["options"]), r["answer"],
                        r["prompt_source"], r["master_id"]])
    print("wrote", CSV_OUT)


if __name__ == "__main__":
    main()
