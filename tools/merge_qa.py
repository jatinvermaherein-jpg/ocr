"""Merge per-batch QA JSON into the master page audit + DIBY index.
Batches live in deliverables/twin-1/page-audit/qabatch_<key>.json (list of row dicts)."""
import os, csv, json, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))

D = "/home/user/ocr/deliverables/twin-1"
AUD = f"{D}/page-audit/page_audit_twin1.csv"
DIBY = f"{D}/diby/diby_index_twin1.csv"
PROG = f"{D}/page-audit/progress.json"

def main():
    files = [f for f in sorted(os.listdir(f"{D}/page-audit")) if f.startswith("qabatch_")]
    rows = list(csv.DictReader(open(AUD)))
    idx = {(r["source_pdf"], int(r["pdf_page"])): r for r in rows}
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ")
    applied = 0
    from twin1_scope import TWIN1_SCOPE
    key_by_prefix = {}
    for ch, lec, fn, _ in TWIN1_SCOPE:
        pref = ("bt" if ch.startswith("Binomial") else "pc") + lec
        key_by_prefix[pref] = fn
    for fn in files:
        batch = json.load(open(f"{D}/page-audit/{fn}"))
        for rec in batch:
            key = rec.pop("_key")                      # e.g. "bt01"
            pdf = key_by_prefix[key]
            r = idx[(pdf, rec.pop("_page"))]
            for k, v in rec.items():
                r[k] = str(v)
            r["qa_timestamp"] = now
            applied += 1
    with open(AUD, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    # DIBY index
    djf = f"{D}/diby/diby_rows.json"
    if os.path.exists(djf):
        drows = json.load(open(djf))
        cols = ["chapter","lecture","source_pdf","pdf_page","diby_marker","printed_label","internal_id",
                "prompt_verbatim","options","visible_solution_answer","uncertainty_note","qa_status"]
        with open(DIBY, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(drows)
        print(f"DIBY index: {len(drows)} rows")
    done = sum(1 for r in rows if r["visual_qa_status"] and r["visual_qa_status"] != "PENDING")
    per = {}
    for r in rows:
        k = (r["chapter"], r["lecture"])
        s = per.setdefault(k, [0, 0]); s[1] += 1
        if r["visual_qa_status"] and r["visual_qa_status"] != "PENDING": s[0] += 1
    json.dump({"worker":"twin-1","qa_rows_applied":applied,"pages_reviewed":done,"pages_total":len(rows),
               "per_lecture":{f"{c} L{l}": {"reviewed": v[0], "total": v[1]} for (c,l),v in per.items()},
               "updated": now}, open(PROG,"w"), indent=1)
    print(f"applied {applied} QA rows | pages reviewed {done}/{len(rows)}")
    for (c,l),v in sorted(per.items()):
        if v[0]: print(f"   {c} L{l}: {v[0]}/{v[1]}")

if __name__ == "__main__":
    main()
