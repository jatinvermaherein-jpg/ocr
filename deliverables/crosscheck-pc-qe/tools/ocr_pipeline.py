#!/usr/bin/env python3
"""
Twin 2 OCR extraction pipeline.
Assignment: Permutations & Combinations L05-L11 (7 PDFs / 278 pp)
          + Quadratic Equations L01-L08 (8 PDFs / 258 pp) = 15 PDFs / 536 pages.

Renders every page of every assigned PDF (no sampling), runs a DUAL-PASS PP-OCRv4
(RapidOCR/onnxruntime) extraction, and writes per-page raw records to
<work>/raw/<slug>/page_NNN.json plus per-PDF meta.json / summary.json.

Pass A: native render @200 dpi.
Pass B: background-adapted render @200 dpi (inverted when the slide background is
        dark, CLAHE otherwise).
Primary pass = higher score (sum of line confidences). Both passes are stored so a
reviewer can audit disagreements; the agreement ratio is recorded for the audit.

Nothing is silently corrected: text is stored verbatim per pass. Downstream builder
(build_deliverables.py) merges these records with agent QA notes.

Usage:
  python ocr_pipeline.py --work /home/user/ocr_work [--only "Permutations*05*"] [--workers 2]
"""
import argparse
import difflib
import glob
import hashlib
import json
import os
import re
import sys
import time
from multiprocessing import Pool

import numpy as np
import pymupdf
import cv2
from rapidocr_onnxruntime import RapidOCR

REPO = "/home/user/ocr"

# Twin 2 assignment (Master OCR Allocation Plan -> Worker Summary / PDF Inventory)
ASSIGNMENT = [
    ("Permutations & Combinations", 5,  "Permutations and Combinations 05 Class Notes.pdf"),
    ("Permutations & Combinations", 6,  "Permutations and Combinations 06 Class Notes.pdf"),
    ("Permutations & Combinations", 7,  "Permutations and Combinations 07 Class Notes.pdf"),
    ("Permutations & Combinations", 8,  "Permutations and Combinations 08 Class Notes.pdf"),
    ("Permutations & Combinations", 9,  "Permutations and Combinations 09 Class Notes.pdf"),
    ("Permutations & Combinations", 10, "Permutations and Combinations 10 Class Notes.pdf"),
    ("Permutations & Combinations", 11, "Permutations and Combinations 11 Class Notes.pdf"),
    ("Quadratic Equations", 1,  "Quadratic Equations 01 Class Notes.pdf"),
    ("Quadratic Equations", 2,  "Quadratic Equations 02  Class Notes  Maths By Sachin Sir.pdf"),
    ("Quadratic Equations", 3,  "Quadratic Equations 03  Class Notes  Maths By Sachin Sir.pdf"),
    ("Quadratic Equations", 4,  "Quadratic Equations 04 Class Notes.pdf"),
    ("Quadratic Equations", 5,  "Quadratic Equations 05 Class Notes.pdf"),
    ("Quadratic Equations", 6,  "Quadratic Equations 06 Class Notes.pdf"),
    ("Quadratic Equations", 7,  "Quadratic Equations 07 Class Notes.pdf"),
    ("Quadratic Equations", 8,  "Quadratic Equations 08 Class Notes.pdf"),
]

DPI = 200
_engine = None


def engine():
    global _engine
    if _engine is None:
        _engine = RapidOCR()
    return _engine


def slug(chapter, lecture):
    return f"{re.sub(r'[^a-z0-9]+', '-', chapter.lower()).strip('-')}-L{lecture:02d}"


def render(page, dpi=DPI):
    pix = page.get_pixmap(dpi=dpi)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    return img[:, :, :3]


def adapt(img):
    """Background-adapted variant: invert dark slides, CLAHE-contrast the rest."""
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if gray.mean() < 110:
        return 255 - img
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    lab[:, :, 0] = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)


def ahash(img):
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    g = cv2.resize(g, (16, 16), interpolation=cv2.INTER_AREA)
    bits = (g > g.mean()).astype(np.uint8)
    return format(int("".join(map(str, bits.flatten())), 2), "032x")


def lines_in_order(res):
    """Sort OCR boxes into reading order (row bands by y, then x)."""
    if not res:
        return []
    items = []
    for box, txt, conf in res:
        ys = [p[1] for p in box]
        xs = [p[0] for p in box]
        items.append({"y": sum(ys) / 4, "x": sum(xs) / 4,
                      "h": max(ys) - min(ys), "w": max(xs) - min(xs),
                      "text": txt, "conf": round(float(conf), 4)})
    items.sort(key=lambda d: d["y"])
    rows, cur = [], []
    for it in items:
        if cur and abs(it["y"] - cur[-1]["y"]) > max(28, 0.8 * min(it["h"], cur[-1]["h"])):
            rows.append(cur)
            cur = []
        cur.append(it)
    if cur:
        rows.append(cur)
    out = []
    for r in rows:
        r.sort(key=lambda d: d["x"])
        out.extend(r)
    return out


def run_pass(img):
    res, _ = engine()(img)
    lines = lines_in_order(res)
    return {
        "lines": lines,
        "text": "\n".join(l["text"] for l in lines),
        "n_lines": len(lines),
        "mean_conf": round(float(np.mean([l["conf"] for l in lines])), 4) if lines else 0.0,
        "min_conf": round(float(np.min([l["conf"] for l in lines])), 4) if lines else 0.0,
        "score": round(sum(l["conf"] for l in lines), 2),
    }


def norm(t):
    return re.sub(r"\s+", " ", t).strip().lower()


def process_page(args):
    pdf_path, pno, out_dir = args
    out_f = os.path.join(out_dir, f"page_{pno + 1:03d}.json")
    if os.path.exists(out_f):
        return ("skip", os.path.basename(pdf_path), pno + 1)
    doc = pymupdf.open(pdf_path)
    page = doc[pno]
    t0 = time.time()
    img = render(page)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    pa = run_pass(img)
    pb = run_pass(adapt(img))
    primary, pname = (pa, "A") if pa["score"] >= pb["score"] else (pb, "B")
    ratio = difflib.SequenceMatcher(None, norm(pa["text"]), norm(pb["text"])).ratio()
    rec = {
        "pdf": os.path.basename(pdf_path),
        "page": pno + 1,
        "page_size_pts": [round(page.rect.width, 1), round(page.rect.height, 1)],
        "dark_background": bool(gray.mean() < 110),
        "mean_luma": round(float(gray.mean()), 1),
        "ahash": ahash(img),
        "pass_A_native": pa,
        "pass_B_adapted": pb,
        "primary_pass": pname,
        "pass_agreement": round(ratio, 4),
        "text": primary["text"],
        "n_lines": primary["n_lines"],
        "mean_conf": primary["mean_conf"],
        "min_conf": primary["min_conf"],
        "seconds": round(time.time() - t0, 1),
    }
    doc.close()
    tmp = out_f + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, out_f)
    return ("done", os.path.basename(pdf_path), pno + 1)


def write_meta(chapter, lecture, fname, pdf_path, work):
    sd = os.path.join(work, "raw", slug(chapter, lecture))
    os.makedirs(sd, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    n = doc.page_count
    doc.close()
    sha = hashlib.sha256(open(pdf_path, "rb").read()).hexdigest()
    meta = {"chapter": chapter, "lecture": lecture, "source_pdf": fname,
            "pages": n, "sha256": sha, "slug": slug(chapter, lecture)}
    with open(os.path.join(sd, "meta.json"), "w") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    return meta


def write_summary(meta, work):
    """Per-PDF roll-up written once every page record exists."""
    sd = os.path.join(work, "raw", meta["slug"])
    recs = []
    for f in sorted(glob.glob(os.path.join(sd, "page_*.json"))):
        recs.append(json.load(open(f)))
    if len(recs) != meta["pages"]:
        return None
    low = [r["page"] for r in recs if r["mean_conf"] < 0.85]
    dis = [r["page"] for r in recs if r["pass_agreement"] < 0.60]
    empty = [r["page"] for r in recs if r["n_lines"] == 0]
    diby = [r["page"] for r in recs if "DIBY" in r["text"].upper()]
    summ = {
        "slug": meta["slug"], "pages": meta["pages"],
        "mean_conf": round(float(np.mean([r["mean_conf"] for r in recs])), 4),
        "pages_low_conf_lt_0.85": low,
        "pages_pass_disagreement_lt_0.60": dis,
        "pages_no_text": empty,
        "pages_with_DIBY_marker": diby,
        "total_minutes": round(sum(r["seconds"] for r in recs) / 60, 1),
    }
    with open(os.path.join(sd, "summary.json"), "w") as fh:
        json.dump(summ, fh, ensure_ascii=False, indent=1)
    return summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/home/user/ocr_work")
    ap.add_argument("--only", default=None, help="glob on source filename")
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()

    metas, jobs = [], []
    for chapter, lecture, fname in ASSIGNMENT:
        if a.only and not glob.fnmatch.fnmatch(fname, a.only):
            continue
        p = os.path.join(REPO, fname)
        if not os.path.exists(p):
            print(f"MISSING {fname}", flush=True)
            continue
        meta = write_meta(chapter, lecture, fname, p, a.work)
        metas.append((meta, p))
        sd = os.path.join(a.work, "raw", meta["slug"])
        for i in range(meta["pages"]):
            jobs.append((p, i, sd))

    print(f"[twin2] {len(metas)} PDFs, {len(jobs)} page jobs, {a.workers} workers", flush=True)
    os.makedirs(os.path.join(a.work, "raw"), exist_ok=True)

    done = 0
    t0 = time.time()
    with Pool(a.workers) as pool:
        for st, pdf, pg in pool.imap_unordered(process_page, jobs, chunksize=1):
            done += 1
            if done % 5 == 0 or done == len(jobs):
                el = time.time() - t0
                eta = el / done * (len(jobs) - done)
                print(f"[twin2] {done}/{len(jobs)} pages ({st} {pdf} p{pg}) "
                      f"elapsed {el/60:.1f}m eta {eta/60:.1f}m", flush=True)

    for meta, _ in metas:
        s = write_summary(meta, a.work)
        if s:
            print(f"FINISHED {s['slug']}: {s['pages']}p mean_conf {s['mean_conf']} "
                  f"low={len(s['pages_low_conf_lt_0.85'])} dis={len(s['pages_pass_disagreement_lt_0.60'])} "
                  f"notext={len(s['pages_no_text'])} diby={len(s['pages_with_DIBY_marker'])}", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
