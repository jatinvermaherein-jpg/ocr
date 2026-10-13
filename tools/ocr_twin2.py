#!/usr/bin/env python3
"""Resumable, CPU-only OCR of every PDF page assigned to Twin 2.

No visual review, mathematical correction, or missing-text reconstruction is
performed. Raw engine output, confidence, and page coordinates are retained.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "project-admin/Twin_2_OCR_Assignment.json"
OUTPUT = ROOT / "ocr-output/twin-2"
ENGINE_CONFIG = {
    "engine": "rapidocr-onnxruntime", "version": "1.4.4",
    "detector": "ch_PP-OCRv4_det_infer.onnx",
    "recognizer": "ch_PP-OCRv4_rec_infer.onnx",
    "render_scale": 1.5, "text_score": 0.0,
    "det_limit_side_len": 1600, "det_limit_type": "max",
    "det_thresh": 0.25, "det_box_thresh": 0.35,
    "low_confidence_threshold": 0.80,
    "preprocessing": "RGB PDF render converted to BGR; no text correction",
}
ENGINE = None
PDF_CACHE = {}


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def init_worker():
    global ENGINE
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    import cv2
    from rapidocr_onnxruntime import RapidOCR
    cv2.setNumThreads(1)
    ENGINE = RapidOCR(
        intra_op_num_threads=1, inter_op_num_threads=1,
        text_score=ENGINE_CONFIG["text_score"],
        det_limit_side_len=ENGINE_CONFIG["det_limit_side_len"],
        det_limit_type=ENGINE_CONFIG["det_limit_type"],
        det_thresh=ENGINE_CONFIG["det_thresh"],
        det_box_thresh=ENGINE_CONFIG["det_box_thresh"],
        max_side_len=2200,
    )


def ocr_page(document, page_number):
    import fitz
    import numpy as np
    import cv2
    started = time.monotonic()
    record = {
        "document_id": document["id"], "chapter": document["chapter"],
        "lecture": document["lecture"], "source": document["source"],
        "source_sha256": document["sha256"], "pdf_page": page_number,
        "engine_config": ENGINE_CONFIG, "visual_qa_status": "not_performed",
        "status": "error", "error": None, "lines": [],
        "embedded_text": "", "raw_text": "",
    }
    for attempt in range(2):
        try:
            source = str(ROOT / document["source"])
            if source not in PDF_CACHE:
                for old in PDF_CACHE.values():
                    old.close()
                PDF_CACHE.clear()
                PDF_CACHE[source] = fitz.open(source)
            page = PDF_CACHE[source][page_number - 1]
            scale = ENGINE_CONFIG["render_scale"]
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), colorspace=fitz.csRGB, alpha=False)
            image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            result, timing = ENGINE(image)
            lines = []
            for index, item in enumerate(result or [], 1):
                box, text, confidence = item[:3]
                bbox = [[round(float(x), 2), round(float(y), 2)] for x, y in box]
                lines.append({
                    "line": index, "text": str(text),
                    "confidence": round(float(confidence), 6),
                    "bbox_pixels": bbox,
                    "bbox_pdf_points": [[round(x / scale, 2), round(y / scale, 2)] for x, y in bbox],
                    "low_confidence": float(confidence) < ENGINE_CONFIG["low_confidence_threshold"],
                })
            record.update({
                "status": "ocr_complete" if lines else "ocr_no_text_detected",
                "error": None, "lines": lines,
                "raw_text": "\n".join(line["text"] for line in lines),
                "embedded_text": page.get_text(sort=True),
                "page_size_pdf_points": [page.rect.width, page.rect.height],
                "render_size_pixels": [pix.width, pix.height],
                "ocr_timing_seconds": timing,
                "mean_confidence": round(sum(line["confidence"] for line in lines) / len(lines), 6) if lines else None,
                "low_confidence_lines": sum(line["low_confidence"] for line in lines),
                "attempts": attempt + 1,
            })
            break
        except Exception as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"
            record["attempts"] = attempt + 1
    record["completed_at"] = utc_now()
    record["elapsed_seconds"] = round(time.monotonic() - started, 3)
    return record


def write_document(document, records):
    ordered = sorted(records.values(), key=lambda rec: rec["pdf_page"])
    atomic_text(OUTPUT / "records" / f"{document['id']}.jsonl", "".join(
        json.dumps(record, ensure_ascii=False) + "\n" for record in ordered
    ))
    heading = f"{document['chapter']} — Lecture {document['lecture']}"
    parts = [f"# {heading}\n\n",
             f"Source: `{document['source']}`  \n",
             f"Pages expected: {document['expected_pages']}  \n",
             f"OCR pages saved: {len(ordered)}  \n",
             "Status: **Automated OCR only — not manually reviewed.**\n\n",
             "Raw machine text follows without mathematical corrections. Reading order, "
             "handwriting, equations, fractions, and diagram labels may be inaccurate or missing. "
             "A page with no detected text is not certified blank.\n\n"]
    text_parts = [heading, f"Source: {document['source']}", "AUTOMATED OCR — NOT MANUALLY REVIEWED", ""]
    for record in ordered:
        page = record["pdf_page"]
        parts += [f"## PDF page {page}\n\n", f"OCR status: `{record['status']}`\n\n"]
        raw = record["raw_text"]
        if record["status"] == "error":
            raw = f"[OCR ERROR: {record['error']}]"
        elif not raw:
            raw = "[NO TEXT DETECTED BY OCR — not confirmed blank]"
        # Keep raw OCR in a literal block, not interpreted as Markdown/formulas.
        fence = "`" * max(3, max((len(s) for s in __import__('re').findall(r'`+', raw)), default=0) + 1)
        parts += [f"{fence}text\n{raw}\n{fence}\n\n"]
        if record.get("embedded_text", "").strip():
            parts += ["### Existing PDF text layer (separate, uncorrected)\n\n", f"{fence}text\n{record['embedded_text']}\n{fence}\n\n"]
        text_parts += [f"=== PDF PAGE {page} ===", raw, ""]
    atomic_text(OUTPUT / "transcripts" / f"{document['id']}.md", "".join(parts))
    atomic_text(OUTPUT / "transcripts" / f"{document['id']}.txt", "\n".join(text_parts) + "\n")


def write_progress(documents, records, started_at):
    per_doc = []
    for document in documents:
        saved = records[document["id"]]
        successful = sum(rec["status"] != "error" for rec in saved.values())
        per_doc.append({
            "id": document["id"], "source": document["source"],
            "expected_pages": document["expected_pages"], "pages_saved": len(saved),
            "pages_ocr_processed": successful,
            "complete": successful == document["expected_pages"],
        })
    count = sum(doc["pages_ocr_processed"] for doc in per_doc)
    expected = sum(doc["expected_pages"] for doc in per_doc)
    atomic_json(OUTPUT / "progress.json", {
        "worker": "Twin 2", "mode": "OCR only; no manual review",
        "started_at": started_at, "updated_at": utc_now(),
        "expected_files": len(documents), "expected_pages": expected,
        "pages_ocr_processed": count, "files_complete": sum(doc["complete"] for doc in per_doc),
        "complete": count == expected, "manual_pages_reviewed": 0,
        "documents": per_doc,
    })
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    import fitz
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    documents = manifest["documents"]
    if len(documents) != manifest["expected_files"] or sum(d["expected_pages"] for d in documents) != manifest["expected_pages"]:
        raise ValueError("Assignment totals do not reconcile")
    records = {doc["id"]: {} for doc in documents}
    tasks = []
    for document in documents:
        source = ROOT / document["source"]
        document["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        with fitz.open(source) as pdf:
            if len(pdf) != document["expected_pages"]:
                raise ValueError(f"Page count mismatch: {source.name}: {len(pdf)} vs {document['expected_pages']}")
        for page_number in range(1, document["expected_pages"] + 1):
            checkpoint = OUTPUT / ".work" / document["id"] / f"page-{page_number:03d}.json"
            if checkpoint.exists():
                cached = json.loads(checkpoint.read_text(encoding="utf-8"))
                if cached.get("source_sha256") == document["sha256"] and cached.get("engine_config") == ENGINE_CONFIG and cached.get("status") != "error":
                    records[document["id"]][page_number] = cached
                    continue
            tasks.append((document, page_number, checkpoint))
        write_document(document, records[document["id"]])
    started_at = utc_now()
    atomic_json(OUTPUT / "run_manifest.json", {
        **manifest, "documents": documents, "engine_config": ENGINE_CONFIG,
        "started_at": started_at,
    })
    processed = write_progress(documents, records, started_at)
    print(f"START Twin 2: {len(documents)} PDFs / {manifest['expected_pages']} pages; {processed} already saved; {len(tasks)} pending", flush=True)
    with ProcessPoolExecutor(max_workers=args.workers, initializer=init_worker) as pool:
        futures = {pool.submit(ocr_page, doc, page): (doc, page, checkpoint) for doc, page, checkpoint in tasks}
        for future in as_completed(futures):
            document, page_number, checkpoint = futures[future]
            record = future.result()
            atomic_json(checkpoint, record)
            records[document["id"]][page_number] = record
            write_document(document, records[document["id"]])
            processed = write_progress(documents, records, started_at)
            print(f"OCR {processed}/{manifest['expected_pages']} | {document['id']} PDF page {page_number}/{document['expected_pages']} | {len(record['lines'])} lines | {record['status']} | {record['elapsed_seconds']}s", flush=True)
    errors = [rec for docs in records.values() for rec in docs.values() if rec["status"] == "error"]
    print(f"FINISHED: {processed}/{manifest['expected_pages']} pages OCR processed; {len(errors)} errors; manual review: NOT PERFORMED", flush=True)
    return 1 if errors or processed != manifest["expected_pages"] else 0


if __name__ == "__main__":
    sys.exit(main())
