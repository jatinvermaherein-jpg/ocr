#!/usr/bin/env python3
"""
Sequence & Series worker — OCR extraction pipeline.

Assignment (Master OCR Allocation Plan, worker "Current assistant"):
  Sequence & Series L01-L12 = 12 PDFs / 496 pages
  plan branch: ocr/current-sequence-series

Source files are chat uploads and are NOT in the repository. This pipeline looks for
each source in, in order:
    <repo root>            /home/user/ocr
    upload drop            /home/user/uploads
    --src DIR              (repeatable)
and verifies the SHA-256 against the value recorded in
project-admin/PDF_Inventory_and_Worker_Assignments.xlsx (expected hashes hard-coded in
EXPECTED_SHA256 below, extracted from that workbook). A mismatch is reported, never
silently accepted; the actual hash is what gets written into the handoff.

Dual-pass PP-OCRv4 (RapidOCR/onnxruntime), every page, no sampling:
  Pass A: native render @200 dpi
  Pass B: background-adapted render @200 dpi (inverted for dark slides, else CLAHE)
  Primary pass = higher summed line confidence; both passes stored; agreement recorded.

Usage:
  python ocr_pipeline.py --work /home/user/ocr_work --workers 2 [--src /path/to/pdfs] [--only "Sequence*01*"]
"""
import argparse
import difflib
import glob
import hashlib
import json
import os
import re
import time
from multiprocessing import Pool

import numpy as np
import pymupdf
import cv2
from rapidocr_onnxruntime import RapidOCR

REPO = "/home/user/ocr"
UPLOADS = "/home/user/uploads"

CHAPTER = "Sequence & Series"

# Expected SHA-256 values taken from the master inventory workbook (PDF Inventory sheet).
EXPECTED_SHA256 = {
    1:  "a51dee620b85f03f10919c816fb4c91f3495b6370bd8ab215a0eb38fdad1c057",
    2:  "d8e6247d9b1b2778a18b6b0a4152784c1575e3fbe8aa3bd962dfc6700731115a",
    3:  "5f902ed3b4e08170d4c62c21c20cf9ab2214fc81cc26567ed3c8ccbc96a31698",
    4:  "308679659e771b063e66e3f8dce3b144951c3f27e7f53bc8b9683c20f7e35893",
    5:  "eda38c942906cd5d1d1e13f926c52c165f9d6fe5fe32a146d0a78d4616ac3649",
    6:  "0f91eaa6dfa9f0b1ba9eaf444c02edeb52c32bf899a6feeb9358728e742e9beb",
    7:  "9bb866865645b932eb9794592ae62ef672e33a0752ae9cf3f3451734d53f30e0",
    8:  "d2268c368a55d422016cb21c5a4a26422fa698b9cea68ba736eb9ebc14e5ee6f",
    9:  "8cb990b488589cc8b64e3c0c62dd6d3eb73019d69a1842ea94b66f09e61f742c",
    10: "74fec4b272e6104563ac0bb4dc9671b100ffe6baf8a60bccda5ccb1dba5e3aef",
    11: "03cf89ca2bfea6ab52e57c72a009a0bfff5b22ffdce91c2225726c169bf37b7a",
    12: "4bb451bd23c890fa40f50948e0621ea9b23d25e6f06124dd587908b487ccf7db",
}

# (lecture, source filename, expected pages) — filenames exactly as recorded in the inventory.
ASSIGNMENT = [
    (1,  "Sequence and Series 01 Class Notes.pdf",                          44),
    (2,  "Sequence and Series 02 Class Notes.pdf",                          39),
    (3,  "Sequence and Series 03 Class Notes.pdf",                          43),
    (4,  "Sequence and Series 04 Class Notes.pdf",                          42),
    (5,  "Sequence and Series 05 Class Notes.pdf",                          40),
    (6,  "Sequence and Series 06 Class Notes.pdf",                          38),
    (7,  "Sequence and Series 07 Class Notes.pdf.pdf",                      41),
    (8,  "Sequence and Series 08 Class Notes Maths By Sachin Sir.pdf",      48),
    (9,  "Sequence and Series 09 Class Notes.pdf.pdf",                      44),
    (10, "Sequence and Series 10 Class Notes.pdf.pdf",                      35),
    (11, "Sequence and Series 11 Class Notes.pdf.pdf",                      42),
    (12, "Sequence and Series 12 Class Notes.pdf.pdf",                      40),
]

DPI = 200
_engine = None
_extra_src = []


def engine():
    global _engine
    if _engine is None:
        _engine = RapidOCR()
    return _engine


def slug(lecture):
    return f"sequence-series-L{lecture:02d}"


def find_source(fname):
    """Locate a source PDF across repo root, the upload drop, and --src directories."""
    for d in [REPO, UPLOADS] + _extra_src:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            return p
    return None


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


def write_meta(lecture, fname, pdf_path, work, expected_pages):
    sd = os.path.join(work, "raw", slug(lecture))
    os.makedirs(sd, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    n = doc.page_count
    doc.close()
    sha = hashlib.sha256(open(pdf_path, "rb").read()).hexdigest()
    exp = EXPECTED_SHA256.get(lecture, "")
    meta = {
        "chapter": CHAPTER, "lecture": lecture, "source_pdf": fname,
        "pages": n, "pages_expected_from_plan": expected_pages,
        "page_count_matches_plan": n == expected_pages,
        "sha256": sha, "sha256_expected": exp,
        "sha256_matches_inventory": (sha == exp) if exp else None,
        "slug": slug(lecture),
    }
    with open(os.path.join(sd, "meta.json"), "w") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    return meta


def write_summary(meta, work):
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
    global _extra_src
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/home/user/ocr_work")
    ap.add_argument("--only", default=None, help="glob on source filename")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--src", action="append", default=[], help="extra directory to look for sources")
    a = ap.parse_args()
    _extra_src = a.src

    metas, jobs, missing = [], [], []
    for lecture, fname, expected_pages in ASSIGNMENT:
        if a.only and not glob.fnmatch.fnmatch(fname, a.only):
            continue
        p = find_source(fname)
        if not p:
            missing.append(fname)
            continue
        meta = write_meta(lecture, fname, p, a.work, expected_pages)
        if not meta["page_count_matches_plan"]:
            print(f"PAGE COUNT MISMATCH L{lecture:02d}: plan {expected_pages} vs file {meta['pages']}", flush=True)
        if meta["sha256_matches_inventory"] is False:
            print(f"SHA-256 MISMATCH L{lecture:02d} ({fname}) - continuing, actual hash recorded", flush=True)
        metas.append((meta, p))
        sd = os.path.join(a.work, "raw", meta["slug"])
        for i in range(meta["pages"]):
            jobs.append((p, i, sd))

    if missing:
        print(f"MISSING {len(missing)} source file(s):", flush=True)
        for m in missing:
            print(f"   - {m}", flush=True)
        print("Searched: repo root, /home/user/uploads, and any --src directories.", flush=True)
    if not jobs:
        print("Nothing to do: no source PDFs found.", flush=True)
        return

    print(f"[seq] {len(metas)} PDFs, {len(jobs)} page jobs, {a.workers} workers", flush=True)
    os.makedirs(os.path.join(a.work, "raw"), exist_ok=True)
    done = 0
    t0 = time.time()
    with Pool(a.workers) as pool:
        for st, pdf, pg in pool.imap_unordered(process_page, jobs, chunksize=1):
            done += 1
            if done % 5 == 0 or done == len(jobs):
                el = time.time() - t0
                eta = el / done * (len(jobs) - done)
                print(f"[seq] {done}/{len(jobs)} pages ({st} {pdf} p{pg}) elapsed {el/60:.1f}m eta {eta/60:.1f}m", flush=True)

    for meta, _ in metas:
        s = write_summary(meta, a.work)
        if s:
            print(f"FINISHED {s['slug']}: {s['pages']}p mean_conf {s['mean_conf']} "
                  f"low={len(s['pages_low_conf_lt_0.85'])} dis={len(s['pages_pass_disagreement_lt_0.60'])} "
                  f"notext={len(s['pages_no_text'])} diby={len(s['pages_with_DIBY_marker'])}", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
