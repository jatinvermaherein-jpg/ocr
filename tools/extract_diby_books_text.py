#!/usr/bin/env python3
"""Extract every DIBY item from the DIBY-only books, straight from their PDF text layer.

These books are digital natives — no OCR needed. Page text is rebuilt from span
geometry first (see diby_layout.py) so subscripts, superscripts and stacked
fractions survive; markers are then located anywhere inside a rebuilt line, since
"# DIBY-47 # DIBY-48" often share a row.

Layouts handled:
  · numbered — "# DIBY-07" comes first, its text follows. Part tags ("#DIBY-27-A",
    "#DIBY-27-B") stay distinct; an "(Answer)" page feeds the item it belongs to.
  · lettered — "DIBY-C" comes last, question and options precede it; the option
    block may straddle the marker, and the final page is the A–M answer key.

Writes deliverables/diby-books/diby_books.json and diby_books_index.csv
"""
from __future__ import annotations

import csv
import glob
import json
import os
import re
import sys
from collections import Counter

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diby_layout import page_line_stream        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "deliverables/diby-books")

NUM_MARK = re.compile(r"#?\s*D\s*[I1l]\s*B\s*Y\s*[-–—_.]?\s*(\d{1,3})(?!\d)"
                      r"(?:\s*[-–]\s*([A-Z])(?![A-Za-z]))?", re.I)
LET_MARK = re.compile(r"#?\s*D\s*[I1l]\s*B\s*Y\s*[-–—_.]\s*\(?\s*([A-Z])\s*\)?(?![A-Za-z0-9])",
                      re.I)
QUALIFIER = re.compile(r"^\s*\(([A-Za-z][A-Za-z ]{1,14})\)")
KEY_LINE = re.compile(r"^\s*DIBY\s*[-–—_.]?\s*([A-M])\s*[:\-]\s*(.*)$", re.I)
BANNER = re.compile(r"^[^a-z\[\](){}<>]*$")
NOISE = re.compile(r"^\s*(MATHEMATICS|DIBY\s*\(DO IT BY YOURSELF\).*|"
                   r"By\s*:\s*Sachin Jakhar.*|JEE MAINS & IIT JEE ADVANCED|Arjuna JEE 2027|"
                   r"Page\s*No\.?.*|\d{1,3}|[A-D]|[A-D]\s*)$", re.I)
META_LINE = re.compile(r"^\s*\(?(Acidic|Challenger|Critical Thinking|Question|CTQ|JEE\s*(Mains|Adv))"
                       r"[^a-z]*\)?\s*(\[[^\]]*\])?\s*$", re.I)
LEAD_META = re.compile(r"^\s*(?:#\s*)?(?:\(?(?:Acidic|Challenger|Critical Thinking|CTQ|Question)\)?"
                       r"\s*|\[(?:JEE[^\]]*|Multiple Correct|Challenger[^\]]*)\]\s*)+", re.I)
QUOTE = re.compile(r"(never about end result|always about Journey|keep believing|self belief)",
                   re.I)
MARK = re.compile(r"\(\s*([A-Da-d])\s*\)")
OPT_LEAD = re.compile(r"^([A-D])(?![a-z])[\s.\-)\]]*(.+)$")
OPT_NOTE = re.compile(r"\[?\s*JEE[^\]]*\]?")


def is_banner(ln: str) -> bool:
    t = ln.strip()
    if not t or not BANNER.match(t):
        return False
    if len(t) > 45 or any(c.isdigit() for c in t):
        return False
    letters = [c for c in t if c.isalpha()]
    return len(letters) >= 3 and len(t.split()) <= 6


def is_noise(ln: str) -> bool:
    t = ln.strip()
    return bool(NOISE.match(t)) or is_banner(t) or t.lower().startswith("www.")


def keep(ln: str) -> bool:
    return bool(ln.strip()) and not is_noise(ln) and not META_LINE.match(ln)


def strip_lead_meta(text: str) -> str:
    prev = None
    while prev != text:
        prev = text
        text = LEAD_META.sub("", text, count=1).strip()
    text = re.sub(r"^\(\s*(Challenger|Answer|JEE[^)]*)\s*\)\s*", "", text, flags=re.I)
    return text.strip(" #")


def split_options(text: str) -> tuple[str, str]:
    """Separate an (A)…(B)…(C)…(D) option set wherever it sits in the text."""
    # '(A)' can also be a function argument ('n(Π (A))')) — that one is followed by ')'
    marks = [m for m in MARK.finditer(text)
             if not text[m.end():m.end() + 1].startswith(")")]
    if len(marks) < 3:
        return text, ""
    for start in range(len(marks)):                   # a label may also sit inside the
        seen, keep = set(), []                        # question ('n(Π (A))') — retry later
        for m in marks[start:]:
            l = m.group(1).upper()
            if l not in seen:
                seen.add(l)
                keep.append((l, m))
        order = [l for l, _ in keep]
        if len(seen) < 3 or (len(seen) < 4 and order != sorted(order, key="ABCD".index)):
            continue                                  # a grid may list A C B D
        if len(text[:keep[0][1].start()].strip()) >= 15:
            break
    else:
        return text, ""
    pieces = {l: [] for l in "ABCD"}
    for i, (l, m) in enumerate(keep):
        end = keep[i + 1][1].start() if i + 1 < len(keep) else len(text)
        piece = text[m.end():end].strip(" .,")
        if len(piece) > 200:
            return text, ""
        pieces[l].append(piece)
    head = text[:keep[0][1].start()].strip()
    # NOTE: everything after the (D) marker *is* (D)'s own text (the piece runs to the
    # end of the text), so there is no separate tail to fold back into the question --
    # doing that duplicated the last option into every question.
    if len(head) < 15:
        return text, ""
    for l in "ABCD":                    # (A)/(B)… labels and margin tags inside a cell
        pieces[l] = [re.sub(r"\[[^\]]{0,45}(?:JEE|IIT|Mains|Advanced|NEET)[^\]]{0,45}\]", "", p).strip()
                     for p in pieces[l]]
        pieces[l] = [re.sub(r"^[A-Da-d]\s*\)\s*", "", p) for p in pieces[l]]
    opts = "   ".join(("(%s) " % l) + " / ".join(p for p in pieces[l] if p) for l in "ABCD")
    return head, opts.strip()


def split_answer(text: str) -> tuple[str, str]:
    """Peel the answer off an item: '[Ans. : …]' or a bare trailing 'Ans: …'."""
    m = re.search(r"\[\s*Ans\.?[^\]]*\]", text, re.I)
    if m:
        inner = re.sub(r"^\s*\[\s*Ans\.?\s*[:\-]?\s*", "", m.group(0), flags=re.I)
        inner = re.sub(r"\s*\]\s*$", "", inner)
        return (text[:m.start()] + " " + text[m.end():]).strip(), inner.strip()
    m = re.search(r"\((?<![A-Za-z])Ans\.?\s*[:\-]?\s*([^)]*)\)", text, re.I)
    if m:
        return (text[:m.start()] + " " + text[m.end():]).strip(), m.group(1).strip()
    m = re.search(r"(?<![A-Za-z])Ans\.?\s*[:\-]?\s*(.*)$", text, re.I)
    if m:
        return text[:m.start()].strip(), m.group(1).strip()
    return text, ""


def clean_title(path: str) -> str:
    base = os.path.splitext(os.path.basename(path))[0]
    base = re.sub(r"\s*Maths By Sachin Sir\s*", " ", base, flags=re.I)
    base = base.replace("QUADRATIC EQUATION_PART-01", "Quadratic Equations Part 01")
    base = base.replace("_DIBY", " DIBY")
    base = re.sub(r"_?\(?\d?\)?$", "", base).strip(" _-")
    return re.sub(r"\s{2,}", " ", base).strip()


def tidy(text: str, brackets: bool = True) -> str:
    """Drop fraction-notation debris that leaks in from stacked layouts."""
    lead = r"^[\s}{)(\]]+" if brackets else r"^[\s}{]+"
    text = re.sub(lead, "", text or "")
    text = re.sub(r"A{3,}(?=[a-z])", "", text)
    if text.count("{") != text.count("}"):        # trim an unclosed LaTeX tail
        depth, last_balanced = 0, len(text)
        for i, ch in enumerate(text):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    last_balanced = i + 1
        text = text[:last_balanced]
    if text.count("{") != text.count("}"):        # trim a tail with an unclosed brace
        depth, last = 0, len(text)
        for i, ch in enumerate(text):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    last = i + 1
        text = text[:last]
    text = re.sub(r"\\[a-zA-Z]*$", "", text)
    # stacked sub-part labels read out as a fraction: "(i)" over "(ii)" -> "(i) (ii)"
    text = re.sub(r"\\frac\{\(([A-Za-z]{1,4})\)\}\{\(([A-Za-z]{1,4})\)\}",
                  r"(\1) (\2)", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\)(?=[A-Za-z])", ") ", text)       # '(ii)The' -> '(ii) The'
    return text.strip(" #,;")


def make_item(book: str, tag: str, page: int, lines: list[str]) -> dict | None:
    # motivational slides sit between items — drop those lines, keep the item
    text = " ".join(l for l in lines if keep(l) and not QUOTE.search(l))
    text = re.sub(r"\s{2,}", " ", text).strip()
    if not text:
        return None
    if len(re.findall(r"\[\s*Ans\b", text, re.I)) >= 2:
        answer = ""                    # item with per-part answers — keep them inline
        rest = text
    else:
        rest, answer = split_answer(text)
    rest = strip_lead_meta(rest)
    question, opts = split_options(rest)
    question, opts2 = tidy(strip_lead_meta(question)), tidy(opts, brackets=False)
    if not question and not opts2 and not answer:
        return None
    return {"book": book, "tag": tag, "pdf_page": page, "question": question,
            "options": opts2, "answer": tidy(answer, brackets=False).strip(" .")}

def parse_numbered(book: str, stream) -> tuple[list[dict], list[str]]:
    items, skipped = [], []
    pending = None

    def flush():
        nonlocal pending
        if pending is None:
            return
        item = make_item(book, pending["tag"], pending["page"], pending["lines"])
        target = pending.get("answer_for")
        if target is not None:
            if item and item["question"]:
                extra = (item["question"] + " " + item["options"]).strip()
                cur = items[target]["answer"]
                items[target]["answer"] = (cur + " " + extra).strip()
            pending = None
            return
        if item is None:
            skipped.append(pending["tag"])
        else:
            items.append(item)
        pending = None

    for pno, row in stream:
        pos = 0
        for m in NUM_MARK.finditer(row):
            pre = row[pos:m.start()].strip(" #")
            if pending is not None and pre:
                pending["lines"].append(pre)
            flush()
            base = f"DIBY-{int(m.group(1)):02d}"
            tag = base + (f"-{m.group(2).upper()}" if m.group(2) else "")
            end = m.end()
            qual = QUALIFIER.match(row[end:end + 30])
            kind = qual.group(1).lower() if qual else ""
            if qual:
                end += qual.end()
            if kind.startswith("answer"):
                target = next((i for i, it in enumerate(items)
                               if it["tag"].split("-")[0] == base or it["tag"] == base), None)
                pending = {"tag": base, "page": pno, "lines": [], "answer_for": target}
            else:
                pending = {"tag": tag, "page": pno, "lines": []}
            pos = end
        tail = row[pos:].strip(" #")
        if pending is not None and tail:
            pending["lines"].append(tail)
    flush()
    return items, skipped


def parse_answer_key(path: str) -> tuple[dict[str, str], set[int]]:
    """The lettered book ends with an 'ANSWERS (A TO M)' grid."""
    doc = pymupdf.open(path)
    answers, key_pages = {}, set()
    for pno in range(doc.page_count):
        lines = [l.strip() for l in doc[pno].get_text().splitlines()]
        hits = [l for l in lines if KEY_LINE.match(l)]
        if len(hits) >= 5:
            key_pages.add(pno + 1)
            for i, l in enumerate(lines):
                m = KEY_LINE.match(l)
                if not m:
                    continue
                val = m.group(2).strip()
                j = i + 1
                while not val and j < len(lines) and j <= i + 3:
                    if lines[j] and not KEY_LINE.match(lines[j]):
                        val = lines[j].strip()
                        break
                    j += 1
                answers[f"DIBY-{m.group(1).upper()}"] = val
    doc.close()
    return answers, key_pages


def _leading_option_run(lines: list[str], start: str = "A") -> int:
    """How many leading lines continue an option run of the previous item."""
    expect = list("ABCD"[max(0, "ABCD".index(start)):])
    n = 0
    for ln in lines:
        m = OPT_LEAD.match(ln.strip())
        if not m or m.group(1).upper() != expect[n]:
            break
        n += 1
        if n == len(expect):
            break
    return n


def parse_lettered(book: str, stream, key_pages: set[int],
                   key: dict[str, str]) -> tuple[list[dict], list[str]]:
    regions: list[dict] = []
    buf: list[str] = []
    for pno, row in stream:
        pos = 0
        for m in LET_MARK.finditer(row):
            pre = row[pos:m.start()].strip(" #")
            if pre:
                buf.append(pre)
            regions.append({"tag": f"DIBY-{m.group(1).upper()}", "page": pno,
                            "head": list(buf), "tail": []})
            buf = []
            pos = m.end()
        tail = row[pos:].strip(" #")
        if tail:
            buf.append(tail)
            if regions:
                regions[-1]["tail"].append(tail)

    items, skipped = [], []
    prev_last = None
    for i, reg in enumerate(regions):
        head = [l for l in reg["head"] if keep(l)]
        tail = [l for l in reg["tail"] if keep(l)]
        if prev_last and prev_last != "D":            # (B)(C)(D) of the previous item
            expect = "ABCD"["ABCD".index(prev_last) + 1:]
            while head and expect:
                m = OPT_LEAD.match(head[0].strip())
                if m and m.group(1).upper() == expect[0]:
                    head.pop(0)
                    expect = expect[1:]
                else:
                    break
        if not head and not tail:
            skipped.append(reg["tag"])
            continue
        # option run: trailing lines of the head, continued into the tail
        opts, letters = {}, []
        run = []
        for ln in reversed(head):
            m = OPT_LEAD.match(ln.strip())
            if m:
                run.insert(0, (m.group(1).upper(), m.group(2).strip()))
            else:
                break
        if run:
            head = head[:len(head) - len(run)]
            letters = [l for l, _ in run]
            opts.update(dict(run))
            nxt = "ABCD"[len(letters) - 1] if letters else "A"
            for ln in tail:
                m = OPT_LEAD.match(ln.strip())
                if not m or m.group(1).upper() != nxt:
                    break
                opts[m.group(1).upper()] = m.group(2).strip()
                letters.append(m.group(1).upper())
                nxt = "ABCD"[min(3, "ABCD".index(nxt) + 1)]
        prev_last = letters[-1] if letters else None
        if reg["page"] in key_pages:
            continue                                  # the A–M key grid, not an item
        text = re.sub(r"\s{2,}", " ", " ".join(l for l in head if not QUOTE.search(l))).strip()
        text, answer = split_answer(text)
        text = strip_lead_meta(text)
        if not opts:
            text, jo = split_options(text)
            if jo:
                opts = {l: v.strip() for l, v in
                        re.findall(r"\(([A-D])\)\s*([^()]*?)(?=\s*\([A-D]\)|$)", jo)}
        answer = answer or key.get(reg["tag"], "")
        if not text and not opts and not answer:
            skipped.append(reg["tag"])
            continue
        opt_txt = "   ".join(f"({l}) {opts[l]}".strip() for l in "ABCD" if l in opts)
        items.append({"book": book, "tag": reg["tag"], "pdf_page": reg["page"],
                      "question": text.strip(" #"), "options": opt_txt,
                      "answer": answer.strip(" .")})
    return items, skipped


def parse_book(path: str) -> tuple[list[dict], list[str], set[int], dict[str, str]]:
    doc = pymupdf.open(path)
    book = clean_title(path)
    stream = page_line_stream(doc)
    doc.close()
    key, key_pages = parse_answer_key(path)
    n_let = sum(1 for _, l in stream if LET_MARK.search(l) and not KEY_LINE.match(l))
    n_num = sum(1 for _, l in stream if NUM_MARK.search(l))
    if n_let >= 3 and n_let >= n_num:
        items, skipped = parse_lettered(book, stream, key_pages, key)
        return items, skipped, key_pages, key
    items, skipped = parse_numbered(book, stream)
    return items, skipped, key_pages, key


FIX_PATH = os.path.join(OUT_DIR, "manual_fixes.json")


def apply_fixes(items: list[dict]) -> int:
    """Overrides for items whose content lives in an image — read from the page.

    Each entry records the page it was read from, so nothing is invented.
    """
    if not os.path.exists(FIX_PATH):
        return 0
    fixes = json.load(open(FIX_PATH))
    by_key = {(r["book"], r["tag"]): r for r in items}
    applied = 0
    for fx in fixes:
        key = (fx["book"], fx["tag"])
        if key in by_key:
            row = by_key[key]
        else:
            row = {"book": fx["book"], "tag": fx["tag"], "pdf_page": fx.get("pdf_page", 0),
                   "question": "", "options": "", "answer": ""}
            items.append(row)
            by_key[key] = row
        for field in ("question", "options", "answer"):
            if fx.get(field) is not None:
                row[field] = fx[field]
        row["note"] = fx.get("note", "read from the page image")
        applied += 1
    return applied


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    files = [f for f in sorted(glob.glob(os.path.join(ROOT, "*DIBY*.pdf")))
             if "Synthetic" not in f]
    all_items, all_skipped, notes = [], [], []
    for f in files:
        got, skipped, key_pages, key = parse_book(f)
        all_items += got
        all_skipped += [(s, clean_title(f)) for s in skipped]
        n_ans = sum(1 for g in got if g["answer"])
        n_opt = sum(1 for g in got if g["options"])
        extra = f" keys:{len(key)}" if key else ""
        print(f"{clean_title(f)[:42]:44s} {len(got):4d} items  "
              f"(answers {n_ans:3d}, options {n_opt:3d}){extra}")
        if key_pages:
            notes.append(f"{clean_title(f)}: A–M answer key on page(s) "
                         f"{sorted(key_pages)} merged into items")
        got = [g for g in got]
        gq = [g for g in got if len(re.findall(r"[A-Za-z]{3,}", g["question"])) == 0]
        if gq:
            notes.append(f"{clean_title(f)}: {len(gq)} items whose text has no words "
                         f"(probably graph/statement page): "
                         + ", ".join(g['tag'] for g in gq[:8]))

    n_fix = apply_fixes(all_items)
    if n_fix:
        print(f"\n   applied {n_fix} visual-read fix(es) from manual_fixes.json")
        all_items.sort(key=lambda r: (r["book"], r["pdf_page"]))
        have = {(r["book"], r["tag"]) for r in all_items}
        all_skipped = [(tag, bk) for tag, bk in all_skipped if (bk, tag) not in have]
    json.dump(all_items, open(os.path.join(OUT_DIR, "diby_books.json"), "w"),
              indent=1, ensure_ascii=False)
    with open(os.path.join(OUT_DIR, "diby_books_index.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Book", "DIBY tag", "PDF page", "Question", "Options", "Answer", "QA status"])
        for r in all_items:
            w.writerow([r["book"], r["tag"], r["pdf_page"], r["question"], r["options"],
                        r["answer"], "text-layer extraction — not visually verified"])
    if notes:
        open(os.path.join(OUT_DIR, "qa_notes.md"), "w").write(
            "# DIBY book extraction — notes\n\n" + "\n".join(f"- {n}" for n in notes) + "\n")
    print(f"\nTOTAL: {len(all_items)} DIBY items from {len(files)} books")
    print("   with a question:", sum(1 for r in all_items if r["question"]),
          "| with an answer:", sum(1 for r in all_items if r["answer"]),
          "| with options:", sum(1 for r in all_items if r["options"]))
    if all_skipped:
        shown = ", ".join(f"{t} ({b[:22]})" for t, b in all_skipped[:10])
        print(f"   skipped markers (image/quote pages): {len(all_skipped)} → {shown}"
              + (" …" if len(all_skipped) > 10 else ""))
    print("   duplicate tags inside a book:",
          sum(1 for k, v in Counter((r["book"], r["tag"]) for r in all_items).items() if v > 1))


if __name__ == "__main__":
    main()
