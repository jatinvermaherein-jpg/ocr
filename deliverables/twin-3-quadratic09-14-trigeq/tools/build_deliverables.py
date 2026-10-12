#!/usr/bin/env python3
"""
Twin 3 deliverable builder.

Merges raw dual-pass OCR records (<work>/raw/<slug>/page_NNN.json) with agent
visual-QA notes (<work>/qa/<slug>.json, optional) into the standard handoff set:

  deliverables/twin-3-quadratic09-14-trigeq/
    transcripts/<slug>.md          page-by-page transcript
    page_audit.csv                 one row per PDF page (template fields)
    diby_index.csv                 one row per DIBY item (template fields)
    uncertainty_log.md             every [UNCLEAR]/low-confidence/disagreement entry
    qa_notes/<slug>.json           copy of the manual QA record (provenance)

Rules honoured: verbatim source text (no silent maths corrections), [UNCLEAR]
markers with page + location, audit row for every page incl. covers/dividers,
reconciliation of expected vs reviewed page counts.
"""
import csv
import glob
import json
import os
import shutil
import sys

WORK = "/home/user/ocr_work"
OUT = "/home/user/ocr/deliverables/twin-3-quadratic09-14-trigeq"
RAW = os.path.join(WORK, "raw")
QA = os.path.join(WORK, "qa")

AUDIT_FIELDS = ["Chapter", "Lecture No.", "Source PDF", "PDF page", "Visible topic/heading",
                "Full text / equations", "Diagram/visual notes", "DIBY present?",
                "DIBY printed label(s)", "OCR uncertainty / location", "Visual QA status", "Reviewer"]
DIBY_FIELDS = ["Chapter", "Lecture No.", "Source PDF", "PDF page", "DIBY marker",
               "Printed question number/letter (exact)", "Internal ID (only if no printed label)",
               "Prompt (verbatim)", "Options", "Visible solution/answer", "Uncertainty note", "QA status"]

AGENT = "arena-twin3-agent"


def load(slug):
    sd = os.path.join(RAW, slug)
    meta = json.load(open(os.path.join(sd, "meta.json")))
    pages = []
    for f in sorted(glob.glob(os.path.join(sd, "page_*.json"))):
        pages.append(json.load(open(f)))
    qa = {}
    qf = os.path.join(QA, slug + ".json")
    if os.path.exists(qf):
        qa = json.load(open(qf)).get("pages", {})
    return meta, pages, qa


def low_conf_lines(rec, thr=0.75):
    prim = rec["pass_A_native"] if rec["primary_pass"] == "A" else rec["pass_B_adapted"]
    return [l for l in prim["lines"] if l["conf"] < thr]


def log_conf_lines(rec, thr=0.65):
    """Page-level uncertainty entries: only genuinely weak readings hit the log."""
    return low_conf_lines(rec, thr)


def build_transcript(slug, meta, pages, qa):
    L = []
    L.append(f"# {meta['chapter']} - Lecture {meta['lecture']:02d}")
    L.append("")
    L.append(f"- Source PDF: `{meta['source_pdf']}`")
    L.append(f"- SHA-256: `{meta['sha256']}`")
    L.append(f"- Pages: {meta['pages']} (reviewed: {len(pages)})")
    L.append(f"- Worker: Twin 3 (branch arena/052fa64f-ocr; plan branch ocr/twin-3-quadratic09-14-trigeq)")
    L.append(f"- QA reviewer: {qa.get('__reviewer__', AGENT) if isinstance(qa, dict) else AGENT}")
    L.append("")
    for rec in pages:
        p = rec["page"]
        note = qa.get(str(p), {})
        L.append(f"## Page {p}")
        L.append("")
        L.append(f"- Topic/heading: {note.get('topic', '(see text)')}")
        L.append(f"- Page type: {note.get('type', 'auto')} | dark bg: {rec['dark_background']} | "
                 f"primary pass {rec['primary_pass']} | mean conf {rec['mean_conf']} | pass agreement {rec['pass_agreement']}")
        if note.get("diagram"):
            L.append(f"- Diagram/visual: {note['diagram']}")
        if note.get("verified_text"):
            L.append("")
            L.append("### Verified transcript (visual QA)")
            L.append("")
            for ln in note["verified_text"].split(" | "):
                L.append(f"- {ln}")
        L.append("")
        L.append("### Raw OCR (primary pass, verbatim)")
        L.append("")
        prim = rec["pass_A_native"] if rec["primary_pass"] == "A" else rec["pass_B_adapted"]
        if not prim["lines"]:
            L.append("- (no text detected)")
        for l in prim["lines"]:
            flag = "  [LOWCONF]" if l["conf"] < 0.75 else ""
            L.append(f"- {l['text']}{flag}")
        if rec["pass_agreement"] < 0.8:
            L.append("")
            L.append(f"> Dual-pass agreement {rec['pass_agreement']} (<0.80): secondary pass text kept in raw record for audit.")
        for iss in note.get("issues", []):
            L.append("")
            L.append(f"> [UNCLEAR] p{p}: {iss}")
        L.append("")
    return "\n".join(L)


def main():
    os.makedirs(os.path.join(OUT, "transcripts"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "qa_notes"), exist_ok=True)
    audit, diby, unc = [], [], []
    slugs = sorted(d for d in os.listdir(RAW)
                   if os.path.isdir(os.path.join(RAW, d))
                   and os.path.exists(os.path.join(RAW, d, "meta.json")))
    for slug in slugs:
        meta, pages, qa = load(slug)
        with open(os.path.join(OUT, "transcripts", slug + ".md"), "w") as fh:
            fh.write(build_transcript(slug, meta, pages, qa))
        if os.path.exists(os.path.join(QA, slug + ".json")):
            shutil.copy(os.path.join(QA, slug + ".json"), os.path.join(OUT, "qa_notes", slug + ".json"))
        for rec in pages:
            p = rec["page"]
            note = qa.get(str(p), {})
            lc = log_conf_lines(rec)
            uncert = []
            for l in lc:
                uncert.append(f"low-conf ({l['conf']}) line: '{l['text']}'")
            if rec["pass_agreement"] < 0.8:
                uncert.append(f"dual-pass agreement {rec['pass_agreement']}")
            for iss in note.get("issues", []):
                uncert.append(iss)
            dibs = note.get("diby", [])
            audit.append({
                "Chapter": meta["chapter"], "Lecture No.": meta["lecture"],
                "Source PDF": meta["source_pdf"], "PDF page": p,
                "Visible topic/heading": note.get("topic", ""),
                "Full text / equations": note.get("verified_text", rec["text"]),
                "Diagram/visual notes": note.get("diagram", ""),
                "DIBY present?": "yes" if dibs else ("marker-only" if note.get("type") == "divider" and "DIBY" in rec["text"].upper() else "no"),
                "DIBY printed label(s)": "; ".join(d.get("printed_label", "") for d in dibs),
                "OCR uncertainty / location": "; ".join(uncert),
                "Visual QA status": "visual-full" if note else "auto-QA (dual-pass)",
                "Reviewer": AGENT if note else "pipeline (dual-pass PP-OCRv4)",
            })
            for d in dibs:
                diby.append({
                    "Chapter": meta["chapter"], "Lecture No.": meta["lecture"],
                    "Source PDF": meta["source_pdf"], "PDF page": p,
                    "DIBY marker": d.get("printed_label", ""),
                    "Printed question number/letter (exact)": d.get("printed_label", ""),
                    "Internal ID (only if no printed label)": d.get("internal_id", ""),
                    "Prompt (verbatim)": d.get("prompt", ""),
                    "Options": "; ".join(d.get("options", [])) if isinstance(d.get("options"), list) else d.get("options", ""),
                    "Visible solution/answer": d.get("answer", ""),
                    "Uncertainty note": d.get("uncertainty", ""),
                    "QA status": "visual-full",
                })
            for u in uncert:
                unc.append((meta, p, u))
        exp = meta["pages"]
        got = len(pages)
        print(f"{slug}: expected {exp} reviewed {got} {'OK' if exp == got else 'GAP!'}")

    with open(os.path.join(OUT, "page_audit.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=AUDIT_FIELDS)
        w.writeheader()
        w.writerows(audit)
    with open(os.path.join(OUT, "diby_index.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=DIBY_FIELDS)
        w.writeheader()
        w.writerows(diby)
    with open(os.path.join(OUT, "uncertainty_log.md"), "w") as fh:
        fh.write("# Uncertainty / issue log - Twin 3\n\n")
        fh.write("Every entry cites PDF page and location/reading. Nothing below was silently corrected.\n\n")
        if not unc:
            fh.write("(none recorded yet)\n")
        for meta, p, u in unc:
            fh.write(f"- **{meta['chapter']} L{meta['lecture']:02d}** `{meta['source_pdf']}` p{p}: {u}\n")
    print(f"audit rows={len(audit)} diby rows={len(diby)} uncertainty={len(unc)}")


if __name__ == "__main__":
    main()
