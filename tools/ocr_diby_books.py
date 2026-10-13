#!/usr/bin/env python3
"""Resumable OCR for the DIBY-only books (Basic Mathematics, Set Theory, P&C, Quadratic,
Sequence & Series, Trig Equations, Trig Functions ...).

Reads every *.pdf found in the source folders, renders each page and runs RapidOCR
(PP-OCRv4, same engine as the rest of the project), keeping line text, confidence and
bounding boxes. Re-running continues where it stopped.

Sources (first one that exists is used):
    <repo>/diby-books/*.pdf        <- recommended upload folder
    <repo>/*DIBY*.pdf              <- anything hanging in the repo root
    $DIBY_BOOKS_DIR                <- override

Output:
    ocr-output/diby-books/records/<id>.jsonl   one JSON object per page
    ocr-output/diby-books/progress.json
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "ocr-output/diby-books")
REC_DIR = os.path.join(OUT_DIR, "records")
PROGRESS = os.path.join(OUT_DIR, "progress.json")

ENGINE_CONFIG = {
    "engine": "rapidocr-onnxruntime",
    "version": "1.4.4",
    "detector": "ch_PP-OCRv4_det_infer.onnx",
    "recognizer": "ch_PP-OCRv4_rec_infer.onnx",
    "render_scale": 1.7,
    "text_score": 0.0,
    "low_confidence_threshold": 0.8,
    "preprocessing": "RGB PDF render converted to BGR; no text correction",
}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_files() -> list[str]:
    env = os.environ.get("DIBY_BOOKS_DIR")
    candidates: list[str] = []
    if env:
        candidates += glob.glob(os.path.join(env, "*.pdf"))
    candidates += glob.glob(os.path.join(ROOT, "diby-books/*.pdf"))
    candidates += glob.glob(os.path.join(ROOT, "*DIBY*.pdf"))
    seen, out = set(), []
    for c in sorted(candidates):
        rp = os.path.realpath(c)
        if rp not in seen and os.path.isfile(c):
            seen.add(rp)
            out.append(c)
    return out


def clean_title(path: str) -> str:
    base = os.path.splitext(os.path.basename(path))[0]
    base = re.sub(r"\s*Maths By Sachin Sir\s*", " ", base, flags=re.I)
    base = re.sub(r"_?\(?\d\)?$", "", base.strip())
    base = re.sub(r"\s{2,}", " ", base).strip(" -_")
    return base


def scope() -> list[dict]:
    docs = []
    for i, path in enumerate(source_files(), 1):
        doc = pymupdf.open(path)
        docs.append({
            "id": f"db{i:02d}",
            "book": clean_title(path),
            "source": os.path.basename(path),
            "path": path,
            "expected_pages": doc.page_count,
            "sha256": sha256(path),
        })
        doc.close()
    return docs


_ENGINE = None
_DOCS: dict[str, "pymupdf.Document"] = {}


def get_engine():
    global _ENGINE
    if _ENGINE is None:
        from rapidocr_onnxruntime import RapidOCR
        _ENGINE = RapidOCR()
    return _ENGINE


def get_doc(path: str):
    d = _DOCS.get(path)
    if d is None:
        d = pymupdf.open(path)
        _DOCS[path] = d
    return d


def ocr_page(path: str, page_no: int) -> dict:
    import cv2
    import numpy as np

    scale = ENGINE_CONFIG["render_scale"]
    doc = get_doc(path)
    page = doc[page_no - 1]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    t0 = time.time()
    res, _ = get_engine()(img)
    elapsed = time.time() - t0

    lines = []
    for i, item in enumerate(res or [], 1):
        box, text, score = item[0], item[1], float(item[2])
        ys = [p[1] for p in box]
        xs = [p[0] for p in box]
        lines.append({
            "line": i,
            "text": text,
            "confidence": round(score, 6),
            "bbox": [[round(float(x), 1), round(float(y), 1)] for x, y in zip(xs, ys)],
            "top": round(float(min(ys)), 1),
            "left": round(float(min(xs)), 1),
            "low_confidence": score < ENGINE_CONFIG["low_confidence_threshold"],
        })
    return {
        "pdf_page": page_no,
        "engine_config": ENGINE_CONFIG,
        "lines": lines,
        "raw_text": "\n".join(l["text"] for l in lines),
        "render_size_pixels": [pix.width, pix.height],
        "page_size_pdf_points": [round(page.rect.width, 2), round(page.rect.height, 2)],
        "mean_confidence": round(sum(l["confidence"] for l in lines) / len(lines), 6) if lines else 0.0,
        "low_confidence_lines": sum(1 for l in lines if l["low_confidence"]),
        "status": "ocr_complete",
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def worker(job):
    doc, page_no = job
    out = os.path.join(REC_DIR, f"{doc['id']}.jsonl")
    try:
        rec = ocr_page(doc["path"], page_no)
        rec.update({"document_id": doc["id"], "book": doc["book"],
                    "source": doc["source"], "source_sha256": doc["sha256"]})
    except Exception as exc:
        rec = {"document_id": doc["id"], "book": doc["book"], "source": doc["source"],
               "source_sha256": doc["sha256"], "pdf_page": page_no, "status": "error",
               "error": repr(exc), "lines": [], "raw_text": "",
               "mean_confidence": 0.0, "low_confidence_lines": 0}
    with open(out, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return doc["id"], page_no, rec["status"]


def done_pages() -> dict[str, set[int]]:
    have: dict[str, set[int]] = {}
    for f in glob.glob(os.path.join(REC_DIR, "*.jsonl")):
        doc_id = os.path.basename(f)[:-6]
        ok = set()
        for line in open(f):
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("status") == "ocr_complete":
                ok.add(d["pdf_page"])
        have[doc_id] = ok
    return have


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()

    os.makedirs(REC_DIR, exist_ok=True)
    docs = scope()
    if not docs:
        print("No DIBY book PDFs found. Put them in <repo>/diby-books/ "
              "or set DIBY_BOOKS_DIR.", flush=True)
        return
    have = done_pages()

    jobs = []
    for d in docs:
        for p in range(1, d["expected_pages"] + 1):
            if p not in have.get(d["id"], set()):
                jobs.append((d, p))
    jobs.sort(key=lambda j: j[0]["id"])

    total_pages = sum(d["expected_pages"] for d in docs)
    print(f"diby books: {len(docs)} files / {total_pages} pages | {len(jobs)} left to do", flush=True)
    for d in docs:
        print(f"   {d['id']}  {d['expected_pages']:4d} pp  {d['source']}", flush=True)

    t_start = time.time()
    if jobs:
        with ProcessPoolExecutor(max_workers=args.workers) as ex:
            futs = [ex.submit(worker, j) for j in jobs]
            done = 0
            for fu in as_completed(futs):
                fu.result()
                done += 1
                if done % 20 == 0 or done == len(jobs):
                    el = time.time() - t_start
                    rate = done / el if el else 0
                    left = (len(jobs) - done) / rate / 60 if rate else 0
                    print(f"  {done}/{len(jobs)} pages ({rate:.2f} p/s, ~{left:.0f} min left)", flush=True)

    progress = {"worker": "DIBY books OCR", "expected_files": len(docs),
                "expected_pages": total_pages, "documents": []}
    for d in docs:
        recs = {}
        f = os.path.join(REC_DIR, f"{d['id']}.jsonl")
        if os.path.exists(f):
            for line in open(f):
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("status") == "ocr_complete" or r["pdf_page"] not in recs:
                    recs[r["pdf_page"]] = r
        with open(f, "w") as out:
            for p in sorted(recs):
                out.write(json.dumps(recs[p], ensure_ascii=False) + "\n")
        progress["documents"].append({
            "id": d["id"], "book": d["book"], "source": d["source"],
            "expected_pages": d["expected_pages"], "pages_ocr_processed": len(recs),
            "complete": len(recs) == d["expected_pages"], "sha256": d["sha256"]})
    progress["pages_ocr_processed"] = sum(x["pages_ocr_processed"] for x in progress["documents"])
    progress["complete"] = progress["pages_ocr_processed"] == total_pages
    progress["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    json.dump(progress, open(PROGRESS, "w"), indent=2)
    print(f"done: {progress['pages_ocr_processed']}/{total_pages} pages | complete={progress['complete']}",
          flush=True)


if __name__ == "__main__":
    main()
