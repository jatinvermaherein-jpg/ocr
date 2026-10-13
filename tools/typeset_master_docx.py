#!/usr/bin/env python3
"""Typeset the consolidated master document: DIBY_Master.md -> DIBY_Master.docx.

The master document was exported as flat text, so every question and every option
printed its maths linearly (`2^8 . 3^5 . 5^4`, `1/(2x^3)`, `x^-6`) and not one Word
equation existed in the file. This builder splits each line into prose + maths
(`tools/diby_math.smart_segments`), sends every maths piece through the same
pandoc pipeline the question-bank and book documents use, and writes native Word
equations (OMML) back into the page. Pieces pandoc cannot parse at all fall back to
readable text — never to raw LaTeX.

It also starts every chapter on a fresh page, keeps long items flowing so pages
fill up, and applies the requested type scale (question 16 pt, DIBY number 14 pt,
headings unchanged).

    python3 tools/typeset_master_docx.py
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diby_math import smart_segments, latex_fallback, repair_latex     # noqa: E402
from build_diby_docx_v2 import latex_to_omml                           # noqa: E402

import pypandoc                                                        # noqa: E402
from docx import Document                                              # noqa: E402
from docx.shared import Pt, RGBColor                                   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_MD = os.path.join(ROOT, "deliverables/DIBY_Master.md")
TMP_MD = os.path.join(ROOT, "deliverables/.DIBY_Master_typeset.md")
OUT = os.path.join(ROOT, "deliverables/DIBY_Master.docx")

BLACK = RGBColor(0, 0, 0)
BODY_PT = 16          # question text
TAG_PT = 14           # the DIBY number line
H1_PT, H2_PT, H3_PT = 18, 13.5, 14

MATHY = re.compile(r"[0-9]\s*[\^_/]|\^|\\[a-zA-Z]+|√|±|\b(?:sqrt|log|sin|cos|tan)\b")
LINEAR = re.compile(r"[_^]\s*[\dA-Za-z{(]|<=|>=|\bsqrt\b|\d\s*/\s*\d")
DIBY_LINE = re.compile(r"^\s*\**\s*(?:#\s*)?DIBY[-\s]?[A-Za-z0-9]{1,3}\b")

# maths pieces pandoc refuses, mapped to a repaired copy it accepts (or to "")
RENDER: dict[str, str] = {}


def prepare(md_lines: list[str]) -> None:
    """Work out, in one pandoc batch, which maths spans can be typeset."""
    pieces = set()
    for line in md_lines:
        if line.lstrip().startswith("|") or line.strip().startswith("<a id="):
            continue
        for kind, val in smart_segments(line):
            if kind == "math" or LINEAR.search(val):
                pieces.add(val)
    rendered = latex_to_omml(sorted(pieces))
    retry = {p: repair_latex(p) for p in pieces if p not in rendered}
    fixed = latex_to_omml(sorted(set(retry.values()))) if retry else {}
    for piece in pieces:
        if piece in rendered:
            RENDER[piece] = piece
        elif fixed.get(retry.get(piece, ""), None) is not None:
            RENDER[piece] = retry[piece]
        else:
            RENDER[piece] = ""                      # stays plain text
    print(f"maths spans: {len(pieces)} unique | typeset as equations {sum(1 for v in RENDER.values() if v)}")
    print(f"  repaired for typesetting: {sum(1 for p in pieces if p in retry and RENDER[p] and RENDER[p] != p)}")
    print(f"  printed as text (unparseable): {sum(1 for p in pieces if not RENDER[p])}")


def texify(line: str) -> str:
    """Wrap the maths inside one markdown line as inline TeX (`$…$`)."""
    if not MATHY.search(line):
        return line.replace("$", "")
    out = []
    for kind, val in smart_segments(line):
        maths = kind == "math" or bool(LINEAR.search(val))
        if not maths:
            out.append(val.replace("$", ""))
            continue
        tex = RENDER.get(val, val)
        if tex:
            out.append(f"${tex}$")
        else:                                        # readable text, never raw LaTeX
            out.append(latex_fallback(val).replace("$", ""))
    return "".join(out)


def repair_dollar_paragraphs(doc) -> int:
    """Rebuild any paragraph pandoc left with literal `$…$` maths in its text."""
    fixed = 0
    for p in doc.paragraphs:
        text = p.text or ""
        if "$" not in text:
            continue
        parts = text.split("$")
        for run in list(p.runs):
            run._element.getparent().remove(run._element)
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:                      # prose
                p.add_run(part)
                continue
            tex = RENDER.get(part, part)
            if tex:
                omml = latex_to_omml([tex]).get(tex)
                if omml is not None:
                    p._p.append(omml)
                    continue
            p.add_run(latex_fallback(part))
        fixed += 1
    return fixed


def main() -> None:
    lines = open(SRC_MD, encoding="utf-8").read().splitlines()
    prepare(lines)
    changed = 0
    for i, line in enumerate(lines):
        if line.lstrip().startswith("|") or line.strip().startswith("<a id="):
            continue
        new = texify(line)
        if new != line:
            changed += 1
        lines[i] = new

    # a line that follows an <a id="…"> anchor without a blank line is swallowed into
    # the same paragraph, which turns '# Chapter' into body text — give every heading
    # and anchor the blank line pandoc needs.
    spaced = []
    for i, line in enumerate(lines):
        if line.strip().startswith("<a id=") and spaced and spaced[-1].strip():
            spaced.append("")
        is_head = bool(re.match(r"^#{1,3} ", line))
        if is_head and spaced and spaced[-1].strip():
            spaced.append("")
        spaced.append(line)
        if line.strip().startswith("<a id=") or is_head:
            spaced.append("")
    open(TMP_MD, "w", encoding="utf-8").write("\n".join(spaced))
    print(f"lines rewritten with typeset maths: {changed}")

    pypandoc.convert_file(TMP_MD, "docx", outputfile=OUT, extra_args=["--quiet"])

    # ---- typography, chapter breaks and page-filling paragraphs -------------
    doc = Document(OUT)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(BODY_PT)
    normal.font.color.rgb = BLACK
    for name, size in (("Heading 1", H1_PT), ("Heading 2", H2_PT), ("Heading 3", H3_PT)):
        if name in [s.name for s in doc.styles]:
            st = doc.styles[name]
            st.font.name = "Calibri"
            st.font.size = Pt(size)
            st.font.bold = True
            st.font.color.rgb = BLACK

    # chapters are recognised by their title (pandoc's heading styles vary here)
    chapter_titles = {
        "binomial theorem", "permutations & combinations", "quadratic equations",
        "trigonometric equation", "trigonometric functions", "sequence and series",
    }
    first_chapter = True
    for p in doc.paragraphs:
        text = (p.text or "").strip()
        style = p.style.name if p.style is not None else ""
        p.paragraph_format.keep_together = False
        if style.startswith("Heading"):
            p.paragraph_format.keep_with_next = True
            if style == "Heading 1" and not first_chapter:
                p.paragraph_format.page_break_before = True    # a new chapter starts a page
            if style == "Heading 1":
                first_chapter = False
        elif text.lower().startswith("module: basic maths") or text.lower() in chapter_titles:
            for run in p.runs:                       # a chapter heading
                run.bold = True
                if run.font.size is None or run.font.size < Pt(H1_PT):
                    run.font.size = Pt(H1_PT)
            p.paragraph_format.keep_with_next = True
            if text.lower() in chapter_titles and not first_chapter:
                p.paragraph_format.page_break_before = True   # every chapter starts a page
                first_chapter = False
        elif DIBY_LINE.match(text):
            p.paragraph_format.keep_with_next = True            # number stays with its item
        else:
            # long items may split so the page fills instead of ending half empty
            p.paragraph_format.keep_with_next = False
            p.paragraph_format.keep_together = len(text) <= 500
    repaired = repair_dollar_paragraphs(doc)
    print(f"paragraphs repaired after conversion: {repaired}")
    doc.save(OUT)
    print("wrote", os.path.relpath(OUT, ROOT), os.path.getsize(OUT), "bytes")
    os.remove(TMP_MD)


if __name__ == "__main__":
    main()
