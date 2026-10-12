#!/usr/bin/env python3
"""
Twin 3 OCR extraction pipeline (Quadratic Equations L09-L14, Trigonometric Equation L01-L07).

Renders every page of every assigned PDF (no sampling), runs a DUAL-PASS PP-OCRv4
(RapidOCR/onnxruntime) extraction, and writes per-page raw records to
<work>/raw/<slug>/page_NNN.json plus a per-PDF summary.

Pass A: native render @200 dpi.
Pass B: background-adapted render @200 dpi (inverted when the slide background is
        dark, auto-contrast otherwise).
Primary pass = higher score (sum of line confidences). Both passes are stored so a
reviewer can audit disagreements; the agreement ratio is recorded for the audit.

Nothing is silently corrected: text is stored verbatim per pass. Downstream
builder (build_deliverables.py) merges these records with human/agent QA notes.

Usage:
  python ocr_pipeline.py --work /home/user/ocr_work [--only "Quadratic Equations 09*"] [--workers 2]
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

# Twin 3 assignment (Master OCR Allocation Plan)
ASSIGNMENT = [
    ("Quadratic Equations", 9,  "Quadratic Equations 09 Class Notes.pdf"),
    ("Quadratic Equations", 10, "Quadratic Equations 10 Class Notes.pdf"),
    ("Quadratic Equations", 11, "Quadratic Equations 11 Class Notes.pdf"),
    ("Quadratic Equations", 12, "Quadratic Equations 12 Class Notes.pdf"),
    ("Quadratic Equations", 13, "Quadratic Equations 13 Class Notes.pdf"),
    ("Quadratic Equations", 14, "Quadratic Equations 14 Class Notes.pdf"),
    ("Trigonometric Equation", 1, "Trigonometric Equation 01 Class Notes.pdf"),
    ("Trigonometric Equation", 2, "Trigonometric Equation 02 Class Notes.pdf.pdf"),
    ("Trigonometric Equation", 3, "Trigonometric Equation 03 Class Notes.pdf"),
    ("Trigonometric Equation", 4, "Trigonometric Equation 04 Class Notes.pdf.pdf"),
    ("Trigonometric Equation", 5, "Trigonometric Equation 05 Class Notes.pdf"),
    ("Trigonometric Equation", 6, "Trigonometric Equation 06 Class Notes.pdf"),
    ("Trigonometric Equation", 7, "Trigonometric Equation 07 Class Notes.pdf"),
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
        return ("skip", pdf_path, pno + 1)
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


def process_pdf(job):
    chapter, lecture, fname, work, pdf_path = job
    sd = os.path.join(work, "raw", slug(chapter, lecture))
    os.makedirs(sd, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    n = doc.page_count
    doc.close()
    sha = hashlib.sha256(open(pdf_path, "rb").read()).hexdigest()
    jobs = [(pdf_path, i, sd) for i in range(n)]
    done = 0
    for a in jobs:  # sequential inside pdf; pdfs run in pool
        st, _, pg = process_page(a)
        done += 1
        print(f"[{slug(chapter, lecture)}] page {pg}/{n} {st}", flush=True)
    meta = {"chapter": chapter, "lecture": lecture, "source_pdf": fname,
            "pages": n, "sha256": sha, "slug": slug(chapter, lecture)}
    with open(os.path.join(sd, "meta.json"), "w") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/home/user/ocr_work")
    ap.add_argument("--only", default=None, help="glob on source filename")
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    jobs = []
    for chapter, lecture, fname in ASSIGNMENT:
        if a.only and not glob.fnmatch.fnmatch(fname, a.only):
            continue
        p = os.path.join(REPO, fname)
        if not os.path.exists(p):
            print(f"MISSING {fname}", flush=True)
            continue
        jobs.append((chapter, lecture, fname, a.work, p))
    os.makedirs(os.path.join(a.work, "raw"), exist_ok=True)
    with Pool(a.workers) as pool:
        for meta in pool.imap_unordered(process_pdf, jobs):
            print(f"FINISHED {meta['slug']} ({meta['pages']} pages)", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
