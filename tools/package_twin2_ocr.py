#!/usr/bin/env python3
"""Package raw Twin 2 OCR and machine-generated coverage/confidence logs.

This is not visual or mathematical review. Candidate DIBY hits are not certified
question transcriptions, and no printed question labels are guessed.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "ocr-output/twin-2"
DIBY_RE = re.compile(r"\bD[\W_]*I[\W_]*B[\W_]*Y\b|\bDO\s+IT\s+BY\s+YOURSELF\b", re.IGNORECASE)


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def csv_text(rows, fields):
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def literal_block(text):
    fence = "`" * max(3, max((len(s) for s in re.findall(r"`+", text)), default=0) + 1)
    return f"{fence}text\n{text}\n{fence}\n\n"


def load_records(manifest):
    documents = []
    for document in manifest["documents"]:
        path = OUTPUT / "records" / f"{document['id']}.jsonl"
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        pages = [record["pdf_page"] for record in records]
        expected = list(range(1, document["expected_pages"] + 1))
        if pages != expected:
            raise ValueError(f"Incomplete or duplicate OCR page coverage: {document['id']}")
        for record in records:
            if record["source_sha256"] != document["sha256"]:
                raise ValueError(f"Source fingerprint mismatch: {document['id']}, page {record['pdf_page']}")
            if record["status"] == "error":
                raise ValueError(f"Failed OCR page: {document['id']}, page {record['pdf_page']}: {record['error']}")
            if record["visual_qa_status"] != "not_performed":
                raise ValueError("Raw OCR must not claim a visual review")
        documents.append((document, records))
    return documents


def main():
    manifest = json.loads((OUTPUT / "run_manifest.json").read_text(encoding="utf-8"))
    documents = load_records(manifest)
    all_records = [record for _, records in documents for record in records]
    if len(documents) != 15 or len(all_records) != 536:
        raise ValueError("Twin 2 must contain exactly 15 PDFs and 536 OCR-processed pages")

    audit, uncertainties, candidates = [], [], []
    for document, records in documents:
        for record in records:
            base = {
                "chapter": record["chapter"], "lecture": record["lecture"],
                "source_pdf": record["source"], "pdf_page": record["pdf_page"],
            }
            audit.append({
                **base, "ocr_status": record["status"],
                "ocr_lines": len(record["lines"]),
                "ocr_characters": len(record["raw_text"]),
                "mean_line_confidence": record.get("mean_confidence"),
                "low_confidence_lines": record.get("low_confidence_lines", 0),
                "existing_pdf_text_characters": len(record["embedded_text"]),
                "visual_qa_status": "not_performed_user_requested_ocr_only",
                "diagram_transcription_status": "not_performed",
                "source_sha256": record["source_sha256"],
            })
            uncertainties.append({
                **base, "type": "UNREVIEWED_OCR", "line": "", "confidence": "",
                "location_pdf_points": "", "raw_ocr_text": "",
                "note": "Automated OCR only. Equations, handwriting, layout, and diagram labels may be inaccurate or omitted; no visual comparison or mathematical correction performed.",
            })
            if not record["lines"]:
                uncertainties.append({
                    **base, "type": "NO_TEXT_DETECTED", "line": "", "confidence": "",
                    "location_pdf_points": "whole page", "raw_ocr_text": "",
                    "note": "The OCR engine detected no text. This does not establish that the source page is blank.",
                })
            for line in record["lines"]:
                if line["low_confidence"]:
                    uncertainties.append({
                        **base, "type": "LOW_ENGINE_CONFIDENCE", "line": line["line"],
                        "confidence": line["confidence"],
                        "location_pdf_points": json.dumps(line["bbox_pdf_points"]),
                        "raw_ocr_text": line["text"],
                        "note": "Recognition score below 0.80; text retained unchanged. A confidence score is not an accuracy guarantee.",
                    })
                match = DIBY_RE.search(line["text"])
                if match:
                    candidates.append({
                        **base,
                        "candidate_id": f"T2-{document['id'].upper()}-P{record['pdf_page']:03d}-L{line['line']:03d}",
                        "raw_marker": match.group(0), "raw_marker_line": line["text"],
                        "marker_line": line["line"], "marker_confidence": line["confidence"],
                        "marker_location_pdf_points": json.dumps(line["bbox_pdf_points"]),
                        "printed_question_label": "", "question_label_status": "not_identified_automatically",
                        "page_raw_ocr": record["raw_text"],
                        "prompt_options_answer_status": "not_separated; see unmodified page OCR",
                        "qa_status": "automated_candidate_only_not_reviewed",
                    })

    write_text(OUTPUT / "Page_Audit.csv", csv_text(audit, [
        "chapter", "lecture", "source_pdf", "pdf_page", "ocr_status", "ocr_lines", "ocr_characters",
        "mean_line_confidence", "low_confidence_lines", "existing_pdf_text_characters", "visual_qa_status",
        "diagram_transcription_status", "source_sha256",
    ]))
    write_text(OUTPUT / "Uncertainty_Log.csv", csv_text(uncertainties, [
        "chapter", "lecture", "source_pdf", "pdf_page", "type", "line", "confidence",
        "location_pdf_points", "raw_ocr_text", "note",
    ]))
    write_text(OUTPUT / "DIBY_Candidates.csv", csv_text(candidates, [
        "chapter", "lecture", "source_pdf", "pdf_page", "candidate_id", "raw_marker", "raw_marker_line",
        "marker_line", "marker_confidence", "marker_location_pdf_points", "printed_question_label",
        "question_label_status", "page_raw_ocr", "prompt_options_answer_status", "qa_status",
    ]))

    combined_md = ["# Twin 2 — Raw OCR transcripts\n\n",
        "**15 PDFs · 536 pages · Automated OCR only · No manual review**\n\n",
        "Scope: Permutations & Combinations lectures 05–11 and Quadratic Equations lectures 01–08.\n\n",
        "Text is reproduced directly from the OCR engine, without corrections or guessed missing content. "
        "Equations, handwriting, diagrams, and reading order are not verified. Source PDFs remain the originals in the repository. "
        "All pages, including cover and graphics-only pages, were sent through OCR.\n\n", "## Contents\n\n"]
    combined_txt = ["TWIN 2 — RAW OCR", "15 PDFs / 536 pages", "AUTOMATED OCR ONLY — NO MANUAL REVIEW", ""]
    for document, _ in documents:
        combined_md.append(f"- [{document['chapter']} — Lecture {document['lecture']}](transcripts/{document['id']}.md)\n")
    combined_md.append("\n---\n\n")
    for document, _ in documents:
        combined_md.append((OUTPUT / "transcripts" / f"{document['id']}.md").read_text(encoding="utf-8") + "\n---\n\n")
        combined_txt.append((OUTPUT / "transcripts" / f"{document['id']}.txt").read_text(encoding="utf-8"))
    write_text(OUTPUT / "Twin_2_OCR.md", "".join(combined_md))
    write_text(OUTPUT / "Twin_2_OCR.txt", "\n\n".join(combined_txt))

    diby_md = ["# Twin 2 — Automated DIBY marker candidates\n\n",
        f"Detected marker candidates: **{len(candidates)}**.\n\n",
        "These are raw OCR marker hits, not a reviewed question index. Internal candidate IDs are not printed question numbers. "
        "Prompts, options, solutions, and printed question labels have not been separately verified. "
        "Undetected markers may exist. Each hit includes the full uncorrected OCR from its source page.\n\n"]
    for candidate in candidates:
        diby_md += [f"## {candidate['candidate_id']}\n\n",
            f"Chapter: {candidate['chapter']} · Lecture: {candidate['lecture']} · PDF page: {candidate['pdf_page']}  \n",
            f"Source: `{candidate['source_pdf']}`  \n",
            f"Marker line: {candidate['marker_line']} · Confidence: {candidate['marker_confidence']}\n\n",
            literal_block(candidate["page_raw_ocr"])]
    write_text(OUTPUT / "DIBY_Candidates.md", "".join(diby_md))

    summary = {
        "worker": "Twin 2", "status": "automated_ocr_complete_unreviewed",
        "files_ocr_processed": len(documents), "pages_ocr_processed": len(all_records),
        "manual_pages_reviewed": 0, "failed_ocr_pages": 0,
        "pages_with_no_text_detected": sum(not r["lines"] for r in all_records),
        "recognized_lines": sum(len(r["lines"]) for r in all_records),
        "recognized_characters": sum(len(r["raw_text"]) for r in all_records),
        "low_confidence_lines": sum(r["low_confidence_lines"] for r in all_records),
        "diby_marker_candidates": len(candidates),
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "limits": "No manual review, math correction, diagram description, or verified DIBY question/answer extraction. Raw recognition can contain errors and omissions.",
    }
    write_text(OUTPUT / "completion_summary.json", json.dumps(summary, ensure_ascii=False, indent=2) + "\n")

    overview = ["# Twin 2 OCR handoff\n\n",
        "**OCR finished: 15 / 15 PDFs, 536 / 536 pages.**\n\n",
        "**No manual review performed**, as requested by the user. This handoff completes the automated OCR stage only; "
        "it does not claim completion of the allocation plan's visual QA or faithful math/diagram transcription standards.\n\n",
        "## Files\n\n",
        "- [All transcripts — Markdown](Twin_2_OCR.md)\n",
        "- [All transcripts — plain text](Twin_2_OCR.txt)\n",
        "- [Page audit / coverage](Page_Audit.csv): one row for every source page; not a visual review.\n",
        "- [DIBY marker candidates](DIBY_Candidates.md) ([CSV](DIBY_Candidates.csv)): automatic hits, not verified questions.\n",
        "- [Uncertainty log](Uncertainty_Log.csv): every page marked unreviewed, plus low-score lines with locations.\n",
        "- [Completion summary](completion_summary.json)\n",
        "- [Run manifest and source SHA-256 fingerprints](run_manifest.json)\n",
        "- `records/`: machine-readable JSONL containing text, scores, render size, and bounding boxes for each page.\n",
        "- `transcripts/`: one Markdown and one plain-text transcript for each of the 15 lectures.\n",
        "- `Twin_2_OCR.zip`: downloadable bundle; generated archive is not tracked in Git.\n\n",
        "## Lecture coverage\n\n",
        "| Chapter | Lecture | Source PDF | OCR pages | Transcript |\n",
        "|---|---:|---|---:|---|\n"]
    for document, records in documents:
        link = "../../" + quote(document["source"])
        overview.append(f"| {document['chapter']} | {document['lecture']} | [{document['source']}]({link}) | {len(records)}/{document['expected_pages']} | [{document['id']}](transcripts/{document['id']}.md) |\n")
    overview += ["\n## Recognition limits\n\n",
        "- Engine: RapidOCR ONNX Runtime 1.4.4, bundled PP-OCRv4 detection/recognition models, CPU.\n",
        "- Every PDF page was rendered at 1.5× (normally 1920 × 1080 pixels) and OCR-processed. Existing PDF text, if present, is saved separately.\n",
        "- All recognized lines are retained, including low-confidence text. No manual corrections, math normalization, answer inference, or invented diagram descriptions.\n",
        "- The general text recognizer is not a mathematical handwriting transcription system. Fractions, powers, roots, symbols, multi-column layout, and handwriting may be garbled or omitted.\n",
        "- High engine scores do not certify accurate transcription. Pages with no detected text are not certified blank.\n",
        "- Original diagrams and annotations remain in the source PDFs; the text outputs do not reproduce those graphics.\n\n",
        f"Recognized lines: **{summary['recognized_lines']}** · Low-score lines (<0.80): **{summary['low_confidence_lines']}** · No-text detections: **{summary['pages_with_no_text_detected']}** · DIBY candidates: **{len(candidates)}**.\n\n",
        "## Re-run / resume\n\n",
        "From the repository root, install the pinned packages in an isolated environment. The headless OpenCV wheel is required on this server.\n\n",
        "```sh\npython3 -m venv .venv\n.venv/bin/python -m pip install -r tools/requirements-ocr.txt\n.venv/bin/python -m pip uninstall -y opencv-python\n.venv/bin/python -m pip install --force-reinstall opencv-python-headless==4.11.0.86\n.venv/bin/python tools/ocr_twin2.py --workers 2\n.venv/bin/python tools/package_twin2_ocr.py\n```\n\n",
        "Checkpoints are kept under ignored `.work/` and are reused only for identical source fingerprints and engine settings. "
        "Source PDFs and the master allocation documents are unchanged.\n"]
    write_text(OUTPUT / "README.md", "".join(overview))

    archive = OUTPUT / "Twin_2_OCR.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        for path in sorted(OUTPUT.rglob("*")):
            if path.is_file() and ".work" not in path.relative_to(OUTPUT).parts and path.suffix not in (".zip", ".tmp"):
                zipped.write(path, arcname=str(Path("Twin_2_OCR") / path.relative_to(OUTPUT)))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"BUNDLE: {archive.relative_to(ROOT)} ({archive.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
