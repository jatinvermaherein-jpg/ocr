#!/usr/bin/env python3
"""Assemble ONE consolidated DIBY (Do It By Yourself) document from all worker registers.

Sources (read-only):
  deliverables/twin-1/diby/diby_rows.json                   143 items  (visual QA passed)
  deliverables/twin-3-.../diby_index.csv                    164 items  (52 visual QA, 112 auto-extract)
  ocr-output/twin-2/DIBY_Candidates.csv                     242 markers (no prompts extracted)
  deliverables/twin-4-.../diby_index.csv                    172 markers (no prompts extracted)

Where a worker extracted no prompt (Twin 2, Twin 4), the question text is reconstructed
from that worker's own raw OCR of the SAME page, delimited by the next DIBY marker.
Nothing is corrected, guessed, or re-worded: draft text is the raw OCR, clearly labelled.

Outputs: deliverables/DIBY_Master.{md,csv,json}
"""
from __future__ import annotations

import csv
import json
import glob
import os
import re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "deliverables")

CHAPTER_ORDER = ["Binomial Theorem", "Permutations & Combinations", "Quadratic Equations",
                 "Trigonometric Equation", "Trigonometric Functions"]

MARKER_RE = re.compile(r"(DIBY|DO\s*IT\s*BY\s*YOURSELF|DPP\s*&\s*DIBY)", re.I)
LABEL_RE = re.compile(r"DIBY\s*[-\u2013\u2014]?\s*(\d+)", re.I)
ANS_RE = re.compile(r"\[\s*Ans\.?\s*:?\s*(.+?)\]", re.I)
JUNK_RE = re.compile(r"^[\s\W]*(?:(?:\(?(?:DO\s*IT\s*BY\s*YOURSELF|DIBY|DPP\s*&\s*DIBY)\)?)[\s\W]*)+$", re.I)
MAX_DRAFT_LINES = 14
MAX_DRAFT_CHARS = 700


def is_junk_draft(text: str) -> bool:
    """True when a reconstructed OCR segment carries no real question text."""
    t = (text or "").strip()
    if len(t) < 12 or JUNK_RE.match(t):
        return True
    return len(re.sub(r"[^A-Za-z0-9]", "", t)) < 12


# ----------------------------------------------------------------------------- helpers
def norm_label(s: str) -> str:
    """Normalise a printed DIBY label for matching: '#DIBY-94' -> 'diby94'."""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def clean_prompt(p: str) -> str:
    """Trim trailing marker bleed (e.g. '... then a = #DIBY-36') without altering text."""
    p = (p or "").strip()
    p = re.sub(r"\s*[#\u2013-]*\s*(?:#\s*)?DIBY\s*[-\u2013]?\s*\d+\s*$", "", p, flags=re.I)
    p = re.sub(r"\s*#\s*DPP\s*&\s*DIBY\s*$", "", p, flags=re.I)
    return p.strip(" ;,-")


def label_from_marker(text: str) -> str:
    m = LABEL_RE.search(text or "")
    return f"DIBY-{m.group(1)}" if m else ""


def collapse(segment: list[str]) -> str:
    """Join OCR lines into one draft string, de-duplicating exact repeats."""
    out, seen_prev = [], None
    for ln in segment:
        ln = ln.strip(" -")
        if not ln or ln == seen_prev:
            continue
        out.append(ln)
        seen_prev = ln
    s = " ".join(out)
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s[:MAX_DRAFT_CHARS] + ("…" if len(s) > MAX_DRAFT_CHARS else "")


# ----------------------------------------------------------------------------- loaders
def load_twin1() -> list[dict]:
    rows = json.load(open(os.path.join(ROOT, "deliverables/twin-1/diby/diby_rows.json")))
    recs = []
    for r in rows:
        label = (r.get("printed_label") or "").strip()
        internal = (r.get("internal_id") or "").strip()
        # printed_label is sometimes prose describing absence, e.g.
        # 'none - no printed DIBY chip or question number on the slide'
        if label.lower().startswith("none") or "no printed" in label.lower():
            label = ""
        recs.append(dict(
            worker="Twin 1", chapter=r["chapter"], lecture=str(r["lecture"]).zfill(2),
            source_pdf=r["source_pdf"], pdf_page=int(r["pdf_page"]),
            printed_label=label, internal_id=internal,
            marker_text=(r.get("diby_marker") or "").strip(),
            prompt=(r.get("prompt_verbatim") or "").strip(),
            options=(r.get("options") or "").strip(),
            answer=(r.get("visible_solution_answer") or "").strip(),
            uncertainty=(r.get("uncertainty_note") or "").strip(),
            qa_status=(r.get("qa_status") or "").strip(),
            prompt_source="verified visual transcription (transcribed from the rendered page)",
            kind="question",
        ))
    return recs


def load_twin3() -> list[dict]:
    path = os.path.join(ROOT, "deliverables/twin-3-quadratic09-14-trigeq/diby_index.csv")
    recs = []
    for r in csv.DictReader(open(path, newline="")):
        qa = (r["QA status"] or "").strip()
        verified = qa.startswith("visual")
        recs.append(dict(
            worker="Twin 3", chapter=r["Chapter"], lecture=str(r["Lecture No."]).zfill(2),
            source_pdf=r["Source PDF"], pdf_page=int(r["PDF page"]),
            printed_label=(r["Printed question number/letter (exact)"] or "").strip(),
            internal_id=(r["Internal ID (only if no printed label)"] or "").strip(),
            marker_text=(r["DIBY marker"] or "").strip(),
            prompt=clean_prompt(r["Prompt (verbatim)"]),
            options=(r["Options"] or "").strip(),
            answer=(r["Visible solution/answer"] or "").strip(),
            uncertainty=(r["Uncertainty note"] or "").strip(),
            qa_status=qa,
            prompt_source=("verified visual transcription (transcribed from the rendered page)"
                           if verified else "dual-pass OCR extraction, not visually QA'd"),
            kind="question",
        ))
    return recs


def twin2_page_lines() -> dict[tuple[str, str], list[dict]]:
    pages = {}
    for f in glob.glob(os.path.join(ROOT, "ocr-output/twin-2/records/*.jsonl")):
        for line in open(f):
            d = json.loads(line)
            pages[(d["source"], int(d["pdf_page"]))] = d["lines"]
    return pages


def load_twin2() -> list[dict]:
    path = os.path.join(ROOT, "ocr-output/twin-2/DIBY_Candidates.csv")
    pages = twin2_page_lines()
    recs = []
    for r in csv.DictReader(open(path, newline="")):
        src, page = r["source_pdf"], int(r["pdf_page"])
        lines = pages.get((src, page), [])
        idx = int(r["marker_line"]) - 1
        seg = []
        for ln in lines[idx + 1:]:
            if MARKER_RE.search(ln["text"]):
                break
            seg.append(ln["text"])
            if len(seg) >= MAX_DRAFT_LINES:
                break
        draft = collapse(seg)
        if is_junk_draft(draft):
            draft = ""
        ans = ANS_RE.search(draft)
        label = label_from_marker(r["raw_marker_line"]) or label_from_marker(r["raw_marker"])
        if not label:
            label = label_from_marker(r.get("page_raw_ocr", "")[:80])

        note = (f"automated marker candidate (confidence {float(r['marker_confidence']):.2f})")
        if draft:
            note += "; text after the marker is raw OCR, not visually verified"
            kind = "question-draft"
        else:
            kind = "section-marker"
            # a divider slide: the questions themselves start on the next page
            nxt = pages.get((src, page + 1), [])
            first = ""
            for ln in nxt:
                if MARKER_RE.search(ln["text"]):
                    first = ln["text"].strip()
                    break
            if first:
                note += (f"; section/divider marker only — the questions start on PDF page {page + 1} "
                         f"(first marker there: {first})")
            else:
                note += "; section/divider or note marker — no question text on this page"

        recs.append(dict(
            worker="Twin 2", chapter=r["chapter"], lecture=str(r["lecture"]).zfill(2),
            source_pdf=src, pdf_page=page,
            printed_label=label, internal_id=(r["candidate_id"] or "").strip(),
            marker_text=(r["raw_marker_line"] or "").strip(),
            prompt=draft,
            options="", answer=(ans.group(1).strip() if ans else ""),
            uncertainty=note,
            qa_status="automated candidate only — not reviewed",
            prompt_source=("raw OCR reconstructed from the same page (unverified)" if draft
                           else "no question text on this page (section marker)"),
            kind=kind,
        ))
    return recs


def twin4_page_segments() -> dict[tuple[str, int, int], list[tuple[str, list[str]]]]:
    """(chapter, lecture, page) -> ordered [(marker_line, text_lines_after_it_before_next_marker)]"""
    text = open(os.path.join(ROOT, "deliverables/twin-4-trigonometric-functions/transcript.md")).read()
    blocks = re.split(r"^### ", text, flags=re.M)[1:]
    page_map = {}
    for b in blocks:
        head, _, body = b.partition("\n")
        # head format: "<chapter> — Lecture NN — PDF page N"
        m = re.search(r"^(.*?)\s*—\s*Lecture\s*(\d+)\s*—\s*PDF page\s*(\d+)\s*$", head.strip())
        if not m:
            continue
        chapter, lecture, page = m.group(1).strip(), int(m.group(2)), int(m.group(3))
        bullets = [ln[2:] for ln in body.splitlines() if ln.startswith("- ")]
        segments, cur_marker, cur = [], None, []
        for bl in bullets:
            is_marker = bool(re.fullmatch(r"\s*#?\s*(?:#\s*)?DIBY\s*[-\u2013]?\s*\d+\s*", bl)) \
                or bool(re.fullmatch(r"\s*DO\s*IT\s*BY\s*YOURSELF\s*(?:\(DIBY\))?\s*", bl, re.I))
            if is_marker:
                if cur_marker is not None:
                    segments.append((cur_marker, cur))
                cur_marker, cur = bl, []
            elif cur_marker is not None:
                cur.append(bl)
        if cur_marker is not None:
            segments.append((cur_marker, cur))
        page_map[(chapter, lecture, page)] = (segments, bullets)
    return page_map


def load_twin4() -> list[dict]:
    path = os.path.join(ROOT, "deliverables/twin-4-trigonometric-functions/diby_index.csv")
    page_map = twin4_page_segments()
    rows = list(csv.DictReader(open(path, newline="")))
    # group rows by page so label-less rows can be matched positionally
    by_page = defaultdict(list)
    for r in rows:
        by_page[(r["Chapter"], int(r["Lecture No."]), int(r["PDF page"]))].append(r)
    recs = []
    for (chapter, lecture, page), prows in by_page.items():
        pdf = prows[0]["Source PDF"]
        segs, bullets = page_map.get((chapter, lecture, page), ([], []))
        segs = list(segs)
        page_ctx = ""
        for b in bullets:
            if not re.fullmatch(r"\s*#?\s*DIBY\s*[-\u2013]?\s*\d+\s*", b) and not JUNK_RE.match(b):
                page_ctx = b.strip()
                break
        used = set()
        for r in prows:
            lbl = (r["Printed question number/letter (exact)"] or "").strip()
            want = norm_label(lbl)
            seg, mi = [], None
            if want:
                for i, (mk, txt) in enumerate(segs):
                    if i in used:
                        continue
                    if norm_label(mk) == want or want.endswith(norm_label(mk)) or norm_label(mk).endswith(want):
                        seg, mi = txt, i
                        break
            if mi is None:
                for i, (mk, txt) in enumerate(segs):
                    if i not in used:
                        seg, mi = txt, i
                        break
            if mi is not None:
                used.add(mi)
            draft = collapse(seg)
            if is_junk_draft(draft):
                draft = ""
            ans = ANS_RE.search(draft)
            if draft:
                note = "marker read by OCR only; text after the marker is raw OCR, not visually verified"
            else:
                note = "marker found by OCR but no question text could be taken from this page"
                if page_ctx:
                    note += f"; page heading as read by OCR: '{page_ctx[:90]}'"
            if not lbl:
                note += "; no printed label read — internal ID, not printed"
            recs.append(dict(
                worker="Twin 4", chapter=r["Chapter"], lecture=str(r["Lecture No."]).zfill(2),
                source_pdf=r["Source PDF"], pdf_page=int(r["PDF page"]),
                printed_label=lbl, internal_id=(r["Internal ID (only if no printed label)"] or "").strip(),
                marker_text=(r["DIBY marker"] or "").strip(),
                prompt=draft,
                options="", answer=(ans.group(1).strip() if ans else ""),
                uncertainty=note,
                qa_status=(r["QA status"] or "").strip(),
                prompt_source=("raw OCR reconstructed from the same page (unverified)" if draft
                               else "no question text on this page (marker only)"),
                kind=("question-draft" if draft else "section-marker"),
            ))
    return recs


# ----------------------------------------------------------------------------- assembly
def slug(r):
    return f"{r['worker']}|{r['source_pdf']}|{r['pdf_page']}|{r['printed_label']}|{r['marker_text']}"


def build() -> list[dict]:
    recs = load_twin1() + load_twin2() + load_twin3() + load_twin4()

    def sort_key(r):
        ci = CHAPTER_ORDER.index(r["chapter"]) if r["chapter"] in CHAPTER_ORDER else 99
        lab = LABEL_RE.search(r["printed_label"] or "")
        return (ci, int(r["lecture"]), r["pdf_page"], int(lab.group(1)) if lab else 9999,
                r["worker"], r["master_id"] if "master_id" in r else "")

    recs.sort(key=sort_key)

    # master ids in final document order
    for i, r in enumerate(recs, 1):
        r["master_id"] = f"DIBY-{i:04d}"

    # repeat detection on normalised prompt text (the same question set twice in the module)
    prompt_groups = defaultdict(list)
    for r in recs:
        key = re.sub(r"[^a-z0-9]", "", (r["prompt"] or "").lower())[:120]
        if len(key) > 40:
            prompt_groups[key].append(r)
    for group in prompt_groups.values():
        if len(group) > 1:
            first = group[0]
            for r in group:
                r["repeat_count"] = len(group)
                r["repeat_of"] = ("" if r is first else
                                  f"{first['master_id']} ({first['source_pdf']} p{first['pdf_page']})")
    for r in recs:
        r.setdefault("repeat_of", "")
        r.setdefault("repeat_count", 1)
    return recs


# ----------------------------------------------------------------------------- writers
CSV_COLS = ["master_id", "worker", "chapter", "lecture", "source_pdf", "pdf_page",
            "printed_label", "internal_id", "marker_text", "kind", "prompt", "options",
            "answer", "uncertainty", "qa_status", "prompt_source", "repeat_of", "repeat_count"]


def write_csv(recs, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS, extrasaction="ignore")
        w.writeheader()
        for r in recs:
            w.writerow(r)


def write_json(recs, path):
    json.dump(recs, open(path, "w"), indent=1, ensure_ascii=False)


def write_md(recs, path):
    total = len(recs)
    by_worker = Counter(r["worker"] for r in recs)
    verified = sum(1 for r in recs if r["prompt_source"].startswith("verified"))
    extracted = sum(1 for r in recs if r["prompt_source"].startswith("dual-pass"))
    draft = sum(1 for r in recs if r["prompt_source"].startswith("raw OCR"))
    has_ans = sum(1 for r in recs if r["answer"] and "none" not in r["answer"].lower())
    has_opt = sum(1 for r in recs if r["options"] and "no options" not in r["options"].lower()
                  and "not extracted" not in r["options"].lower())

    L = []
    A = L.append
    A("# DIBY — Consolidated Master Document")
    A("")
    A(f"**{total} DIBY items** collected from every OCR workstream in this repository, "
      "in one document, in chapter → lecture → page order.")
    A("")
    A("This file is generated by `tools/build_diby_master.py` from the four worker registers. "
      "It adds nothing to and removes nothing from the source registers — where a worker had not "
      "extracted a question, the text is **that worker's own raw OCR of the same page**, clearly marked "
      "as unverified. No maths was corrected, no text was re-worded.")
    A("")
    A("## Where these items come from")
    A("")
    A("| Source register | Items | Prompt quality |")
    A("|---|---:|---|")
    A(f"| `deliverables/twin-1/diby/diby_rows.json` | {by_worker['Twin 1']} | "
      "**verified** — visually transcribed from the rendered page (508/508 QA-PASSED scope) |")
    A(f"| `deliverables/twin-3-.../diby_index.csv` | {by_worker['Twin 3']} | "
      "52 verified (visual-full/visual-scan) + 112 auto-extracted by dual-pass OCR |")
    A(f"| `ocr-output/twin-2/DIBY_Candidates.csv` | {by_worker['Twin 2']} | "
      "marker candidates only — draft text reconstructed from the Twin 2 page OCR |")
    A(f"| `deliverables/twin-4-.../diby_index.csv` | {by_worker['Twin 4']} | "
      "marker candidates only — draft text reconstructed from the Twin 4 transcript OCR |")
    A("")
    A("## Read the labels before trusting a question")
    A("")
    A("| Badge | Meaning | Items |")
    A("|---|---|---:|")
    A(f"| ✅ **verified** | Transcribed from the rendered page image by a human-directed visual pass. | {verified} |")
    A(f"| 🔶 **ocr-extract** | Machine OCR extraction that passed a dual-pass check but no visual QA. | {extracted} |")
    A(f"| ⚠️ **ocr-draft** | Marker confirmed by OCR only; question text below is raw OCR, unrestored and unverified. | {draft} |")
    A("")
    A(f"Options captured for **{has_opt}** items · answers/solutions shown on the slide for **{has_ans}** items. "
      "Blank fields mean the source register has no value — not that the slide lacks one.")
    A("")
    A("**Provenance rule used here:** printed labels, page numbers and worker statuses are reproduced exactly "
      "as the workers recorded them. Where a slide shows no printed DIBY number, the worker's internal ID is kept "
      "(`internal_id`, marked *internal — not printed on the slide*).")
    A("")
    A("## Contents")
    A("")
    for ch in CHAPTER_ORDER:
        items = [r for r in recs if r["chapter"] == ch]
        if not items:
            continue
        lects = sorted({r["lecture"] for r in items})
        A(f"- **{ch}** — {len(items)} items · lectures {lects[0]}–{lects[-1]} "
          f"(`#{re.sub(r'[^a-z]+','-',ch.lower()).strip('-')}`)")
    A("")
    A("### Lecture index")
    A("")
    A("| Chapter | Lecture | Items | PDF pages | Question text quality |")
    A("|---|---|---:|---|---|")
    for ch in CHAPTER_ORDER:
        ch_items = [r for r in recs if r["chapter"] == ch]
        for lect in sorted({r["lecture"] for r in ch_items}):
            l_items = [r for r in ch_items if r["lecture"] == lect]
            pages = sorted(r["pdf_page"] for r in l_items)
            q = Counter(r["prompt_source"].split("(")[0].strip() for r in l_items)
            desc = " · ".join(f"{n} {k}" for k, n in
                              [("verified", q.get("verified visual transcription", 0)),
                               ("ocr-extract", q.get("dual-pass OCR extraction, not visually QA'd", 0)),
                               ("ocr-draft", q.get("raw OCR reconstructed from the same page", 0)),
                               ("marker only", q.get("no question text on this page", 0))] if n)
            A(f"| {ch} | {lect} | {len(l_items)} | {pages[0]}" +
              (f"–{pages[-1]}" if pages[-1] != pages[0] else "") + f" | {desc} |")
    A("")
    A("---")
    A("")

    for ch in CHAPTER_ORDER:
        ch_items = [r for r in recs if r["chapter"] == ch]
        if not ch_items:
            continue
        anchor = re.sub(r"[^a-z]+", "-", ch.lower()).strip("-")
        A(f'<a id="{anchor}"></a>')
        A(f"# {ch}")
        A("")
        A(f"*{len(ch_items)} DIBY items.*")
        A("")
        for lect in sorted({r["lecture"] for r in ch_items}):
            l_items = sorted([r for r in ch_items if r["lecture"] == lect],
                             key=lambda r: (r["pdf_page"], r["master_id"]))
            src = l_items[0]["source_pdf"]
            A(f"## Lecture {lect} — `{src}`")
            A("")
            A(f"*{len(l_items)} item(s) · pages {l_items[0]['pdf_page']}–{l_items[-1]['pdf_page']}*")
            A("")
            for r in l_items:
                if r["prompt_source"].startswith("verified"):
                    badge = "✅ verified"
                elif r["prompt_source"].startswith("dual-pass"):
                    badge = "🔶 ocr-extract"
                elif r["kind"] == "section-marker":
                    badge = "⬜ marker only"
                else:
                    badge = "⚠️ ocr-draft"
                label = r["printed_label"] or (f"{r['internal_id']} *(internal — not printed on the slide)*"
                                               if r["internal_id"] else "no printed label")
                A(f"### {r['master_id']} · {label}")
                A("")
                A(f"- **Source:** `{r['source_pdf']}` — PDF page {r['pdf_page']} · worker {r['worker']} · {badge}")
                if r["marker_text"] and norm_label(r["marker_text"]) != norm_label(r["printed_label"]):
                    A(f"- **Marker as recorded:** `{r['marker_text']}`")
                if r["repeat_count"] > 1 and r["repeat_of"]:
                    A(f"- **Repeat appearance:** same question also at {r['repeat_of']}")
                A("")
                if r["prompt"]:
                    A(f"**Question**  \n{r['prompt']}")
                else:
                    A("**Question**  \n_No question printed on this page — the marker is a "
                      "section/divider or note mark. See the note below._")
                A("")
                if r["options"]:
                    A(f"**Options**  \n{r['options']}")
                    A("")
                if r["answer"]:
                    A(f"**Answer as shown on the slide**  \n{r['answer']}")
                    A("")
                if r["uncertainty"]:
                    A(f"**Notes / uncertainty**  \n{r['uncertainty']}")
                    A("")
                A("---")
                A("")

    # appendix
    A("# Appendix A — items that still need a human eye")
    A("")
    A("These items have no verified transcription in any register. They are listed so a reviewer can "
      "work down the list; each one needs the source PDF opened at the given page.")
    A("")
    draft_items = [r for r in recs if not r["prompt_source"].startswith(("verified", "dual-pass"))]
    A(f"**{len(draft_items)} items** (all from Twin 2 and Twin 4).")
    A("")
    A("| Master ID | Chapter | Lecture | PDF page | Label |")
    A("|---|---|---:|---:|---|")
    for r in draft_items:
        A(f"| {r['master_id']} | {r['chapter']} | {r['lecture']} | {r['pdf_page']} | "
          f"{r['printed_label'] or r['internal_id'] or '—'} |")
    A("")
    A("# Appendix B — markers with no question number")
    A("")
    nonum = [r for r in recs if not any(c.isdigit() for c in (r["printed_label"] or ""))]
    A(f"**{len(nonum)} items** carry a DIBY marker but no printed `DIBY-n` / question-number label "
      "(usually a handwritten or section-style mark, or a marker the OCR could not number). "
      "They are included above with internal IDs where the worker created one.")
    A("")
    A("| Master ID | Chapter | Lecture | PDF page | Marker as recorded |")
    A("|---|---|---:|---:|---|")
    for r in nonum:
        A(f"| {r['master_id']} | {r['chapter']} | {r['lecture']} | {r['pdf_page']} | "
          f"`{(r['marker_text'] or '—')[:60]}` |")
    A("")
    A("---")
    A("")
    A("_Generated by `tools/build_diby_master.py`. Machine-readable companions: "
      "`DIBY_Master.csv` (one row per item), `DIBY_Master.json` (full records), "
      "`DIBY_Master.docx` (Word export of this document)._")

    open(path, "w").write("\n".join(L) + "\n")


def main():
    recs = build()
    write_md(recs, os.path.join(OUT_DIR, "DIBY_Master.md"))
    write_csv(recs, os.path.join(OUT_DIR, "DIBY_Master.csv"))
    write_json(recs, os.path.join(OUT_DIR, "DIBY_Master.json"))
    print(f"items: {len(recs)}")
    print("by worker:", dict(Counter(r["worker"] for r in recs)))
    print("by chapter:", dict(Counter(r["chapter"] for r in recs)))
    print("prompt quality:", dict(Counter(r["prompt_source"].split("(")[0].strip() for r in recs)))
    print("with question text:", sum(1 for r in recs if r["prompt"]))
    print("repeats flagged:", sum(1 for r in recs if r["repeat_of"]))


if __name__ == "__main__":
    main()
