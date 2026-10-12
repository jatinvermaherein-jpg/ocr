"""Pre-register one audit row per expected page for all 13 Twin 1 PDFs (no sampling, no gaps).
Verifies actual page count vs the master inventory and records SHA-256 of each source file."""
import os, sys, csv, hashlib, json
sys.path.insert(0, os.path.dirname(__file__))
import pymupdf
from twin1_scope import REPO_ROOT, TWIN1_SCOPE, slug

AUD = "/home/user/ocr/deliverables/twin-1/page-audit/page_audit_twin1.csv"
COLS = ["chapter","lecture","source_pdf","pdf_page","source_page_label","topic_or_heading",
        "transcript_ref","printed_text_captured","handwriting_captured","diby_present","diby_labels",
        "uncertainty_count","extraction_method","visual_qa_status","reviewer","qa_timestamp"]

def main():
    os.makedirs(os.path.dirname(AUD), exist_ok=True)
    rows, report = [], []
    total = 0
    for ch, lec, fn, exp in TWIN1_SCOPE:
        path = os.path.join(REPO_ROOT, fn)
        doc = pymupdf.open(path)
        n = doc.page_count
        sha = hashlib.sha256(open(path,'rb').read()).hexdigest()
        report.append(dict(chapter=ch, lecture=lec, file=fn, expected=exp, actual=n,
                           match=(exp == n), sha256=sha,
                           transcript=f"transcripts/{slug(ch,lec)}.md"))
        for p in range(1, n + 1):
            rows.append({"chapter": ch, "lecture": lec, "source_pdf": fn, "pdf_page": p,
                         "source_page_label": "", "topic_or_heading": "", "transcript_ref": f"{slug(ch,lec)}#p{p:02d}",
                         "printed_text_captured": "", "handwriting_captured": "", "diby_present": "",
                         "diby_labels": "", "uncertainty_count": "", "extraction_method": "",
                         "visual_qa_status": "PENDING", "reviewer": "", "qa_timestamp": ""})
        total += n
        doc.close()
    # non-destructive: keep any page already QA'd (match on source_pdf + pdf_page)
    prev = {}
    if os.path.exists(AUD):
        for r in csv.DictReader(open(AUD)):
            prev[(r["source_pdf"], int(r["pdf_page"]))] = r
    kept = 0
    for r in rows:
        o = prev.get((r["source_pdf"], r["pdf_page"]))
        if o and o.get("visual_qa_status") not in (None, "", "PENDING"):
            r.update({k: v for k, v in o.items() if v})
            kept += 1
    with open(AUD, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    print(f"preserved {kept} already-QA'd rows" if kept else "no prior QA data to preserve")
    json.dump({"worker":"twin-1","pdfs":len(report),"total_pages":total,"inventory_mismatches":[r for r in report if not r["match"]],"files":report},
              open("/home/user/ocr/deliverables/twin-1/page-audit/scope_manifest.json","w"), indent=1)
    print(f"registered {len(rows)} audit rows across {len(report)} PDFs ({total} pages)")
    mism = [r for r in report if not r['match']]
    print("inventory mismatches:", mism if mism else "none - all 13 files match master inventory page counts")

if __name__ == "__main__":
    main()
