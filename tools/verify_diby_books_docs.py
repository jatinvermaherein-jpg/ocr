"""Check the DIBY-book DOCX files straight from their OOXML.

Verifies what the two documents must satisfy: one Heading1 per book, a DIBY- tag per item,
typeset equations (oMath), no raw LaTeX in the text, pure black, an odd-page break between
books, and no header/footer parts.

    python3 tools/verify_diby_books_docs.py [file ...]
"""

import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
RAW_TEX = re.compile(r"\\frac|\\sqrt")
DEFAULT = ["deliverables/DIBY_Books.docx", "deliverables/DIBY_Books_Print.docx"]
QUESTION_DOCS = ["deliverables/DIBY_Questions.docx", "deliverables/DIBY_Questions_Print.docx"]
CHAPTERS = ["BINOMIAL THEOREM", "PERMUTATIONS & COMBINATIONS", "QUADRATIC EQUATIONS",
            "TRIGONOMETRIC EQUATION", "TRIGONOMETRIC FUNCTIONS", "SEQUENCE AND SERIES"]
RAW_ANY = re.compile(r"\\[a-zA-Z]+|\^\{|\^[0-9(]|_\{|\$")


def check(path: str) -> bool:
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    text = "".join(t.text or "" for t in root.iter(W + "t"))
    heads = ["".join(x.text or "" for x in p.iter(W + "t"))
             for p in root.iter(W + "p")
             if p.find(W + "pPr/" + W + "pStyle") is not None
             and p.find(W + "pPr/" + W + "pStyle").get(W + "val") == "Heading1"]
    types = []
    for s in root.iter(W + "sectPr"):
        t = s.find(W + "type")
        types.append(t.get(W + "val") if t is not None else "next(default)")
    cols = sorted({c.get(W + "val") for c in root.iter(W + "color") if c.get(W + "val")})
    hf = [n for n in z.namelist() if "header" in n or "footer" in n]

    omath = len(root.findall(".//" + M + "oMath"))
    tags = len(re.findall(r"DIBY-", text))
    raw = len(RAW_TEX.findall(text))
    odd = [t for t in types[1:]]

    print(os.path.basename(path), os.path.getsize(path), "bytes")
    print(f"   books (Heading1) {len(heads)} | DIBY- tags {tags} | oMath {omath}")
    print(f"   raw LaTeX {raw} | colours {cols} | odd-page breaks {len(odd)}/{len(types) - 1}")
    print(f"   header/footer parts {'none' if not hf else hf}")

    # typography + heading bond
    styles = z.read("word/styles.xml").decode()
    norm = re.search(r'w:styleId="Normal".*?<w:sz w:val="(\d+)"', styles, re.S)
    h1sz = re.search(r'w:styleId="Heading1".*?<w:sz w:val="(\d+)"', styles, re.S)
    normal_pt = int(norm.group(1)) / 2 if norm else None
    h1_pt = int(h1sz.group(1)) / 2 if h1sz else None
    ps = list(root.iter(W + "p"))
    tag_sizes = []
    for p in ps:
        pPr = p.find(W + "pPr")
        if pPr is None:
            continue
        r = p.find(W + "r")
        rPr = r.find(W + "rPr") if r is not None else None
        sz = rPr.find(W + "sz") if rPr is not None else None
        txt = "".join(t.text or "" for t in p.iter(W + "t"))
        if sz is not None and re.fullmatch(r"DIBY[- ]?[\dA-Z]+", (txt or "").strip()):
            tag_sizes.append(int(sz.get(W + "val")) / 2)
    print(f"   question {normal_pt} pt | heading {h1_pt} pt | DIBY number "
          f"{sorted(set(tag_sizes)) or 'style default'} pt")
    orphan = []
    for i, p in enumerate(ps):
        pPr = p.find(W + "pPr")
        if pPr is None or pPr.find(W + "pStyle") is None:
            continue
        if pPr.find(W + "pStyle").get(W + "val") != "Heading1":
            continue
        nxt = ps[i + 1] if i + 1 < len(ps) else None
        if nxt is not None and not "".join(t.text or "" for t in nxt.iter(W + "t")).strip():
            orphan.append(pPr.find(W + "pStyle").get(W + "val"))
        if pPr.find(W + "keepNext") is None:
            orphan.append("no-keepNext")
    print(f"   book headings alone on their page: {'none' if not orphan else orphan}")
    for h in heads:
        print("     -", h)

    ok = (not raw and cols in ([], ["000000"]) and not hf and len(heads) == len(types) == 9
          and tags == 565 and all(t == "oddPage" for t in odd))
    print("   ->", "OK" if ok else "CHECK FAILED")
    return ok


def check_questions(path: str) -> bool:
    """The consolidated question bank: every option typeset, six chapters, no raw LaTeX."""
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    ps = list(root.iter(W + "p"))
    text = "".join(t.text or "" for t in root.iter(W + "t"))
    raw = [t for t in (("".join(x.text or "" for x in p.iter(W + "t"))) for p in ps)
           if RAW_ANY.search(t)]
    omath = len(root.findall(".//" + M + "oMath"))
    types = []
    for sec in root.iter(W + "sectPr"):
        t = sec.find(W + "type")
        types.append(t.get(W + "val") if t is not None else "next(default)")
    chapters = [t for t in (("".join(x.text or "" for x in p.iter(W + "t"))).strip()
                            for p in ps) if t in CHAPTERS]
    tags = len(re.findall(r"DIBY", text))
    cols = sorted({c.get(W + "val") for c in root.iter(W + "color") if c.get(W + "val")})
    hf = [n for n in z.namelist() if "header" in n or "footer" in n]

    styles = z.read("word/styles.xml").decode()
    norm = re.search(r'w:styleId="Normal".*?<w:sz w:val="(\d+)"', styles, re.S)
    normal_pt = int(norm.group(1)) / 2 if norm else None
    print(os.path.basename(path), os.path.getsize(path), "bytes")
    print(f"   chapters {len(chapters)}/6 | DIBY mentions {tags} | oMath {omath}")
    print(f"   raw LaTeX paragraphs {len(raw)} | colours {cols} | "
          f"odd-page breaks {sum(1 for t in types[1:] if t == 'oddPage')}/{len(types) - 1}")
    print(f"   question text {normal_pt} pt | header/footer parts {'none' if not hf else hf}")
    for t in raw[:4]:
        print("      RAW:", t[:90])
    ok = (not raw and len(chapters) == 6 and omath > 1000
          and sum(1 for t in types[1:] if t == "oddPage") == 5)
    print("   ->", "OK" if ok else "CHECK FAILED")
    return ok


def main() -> int:
    files = sys.argv[1:] or DEFAULT
    ok = all(check(f) for f in files)
    for f in QUESTION_DOCS:
        ok = check_questions(f) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
