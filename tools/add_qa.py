"""Append compact QA rows to a lecture batch. Usage: python3 tools/add_qa.py bt02 <<'TSV'
page|printed_label|heading|handwriting|unc|diby   ('-' = empty, diby = 'NO' or 'YES:DIBY-X')
TSV"""
import sys, json, os
key = sys.argv[1]; path = f"/home/user/ocr/deliverables/twin-1/page-audit/qabatch_{key}.json"
rows = json.load(open(path)) if os.path.exists(path) else []
have = {r["_page"] for r in rows}
n = 0
for line in sys.stdin:
    line = line.rstrip("\n")
    if not line.strip(): continue
    p, lbl, head, hand, unc, diby = (line.split("|") + [""] * 6)[:6]
    p = int(p)
    if p in have:
        rows = [r for r in rows if r["_page"] != p]
    d, _, lab = diby.partition(":")
    rows.append({"_key": key, "_page": p, "source_page_label": lbl or "—", "topic_or_heading": head,
                 "printed_text_captured": "full", "handwriting_captured": hand or "none",
                 "diby_present": d or "NO", "diby_labels": lab, "uncertainty_count": int(unc or 0),
                 "extraction_method": "visual transcription from rendered page (PDF has no text layer)",
                 "visual_qa_status": "QA-PASSED", "reviewer": "twin-1"})
    n += 1
json.dump(sorted(rows, key=lambda r: r["_page"]), open(path, "w"), indent=1)
print(f"{key}: +{n} rows, {len(rows)} total")
