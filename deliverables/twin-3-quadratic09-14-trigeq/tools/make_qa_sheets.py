#!/usr/bin/env python3
"""Render 2-up visual-QA contact sheets (native 1280x720 per page) for agent review.

Sheets are scratch artifacts (kept OUT of git) under <work>/sheets/<slug>/.
Each half is labelled with its 1-based PDF page number.

Usage: python make_qa_sheets.py --slug quadratic-equations-L09 --pdf "Quadratic Equations 09 Class Notes.pdf"
"""
import argparse
import os

import numpy as np
import pymupdf
from PIL import Image, ImageDraw

REPO = "/home/user/ocr"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--work", default="/home/user/ocr_work")
    ap.add_argument("--per-sheet", type=int, default=2)
    ap.add_argument("--tag", default="", help="sheet set suffix, e.g. scan")
    ap.add_argument("--page-width", type=int, default=1280)
    a = ap.parse_args()

    name = a.slug + ("-" + a.tag if a.tag else "")
    out = os.path.join(a.work, "sheets", name)
    os.makedirs(out, exist_ok=True)
    doc = pymupdf.open(os.path.join(REPO, a.pdf))
    n = doc.page_count
    pw, ph = a.page_width, int(a.page_width * 720 / 1280)
    label_h = 34
    per = a.per_sheet
    sheet_i = 0
    for start in range(0, n, per):
        sheet_i += 1
        canv = Image.new("RGB", (pw * per, ph + label_h), (24, 24, 28))
        dr = ImageDraw.Draw(canv)
        for k in range(per):
            pno = start + k
            if pno >= n:
                break
            pix = doc[pno].get_pixmap(dpi=int(pw / 1280 * 72))
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).resize((pw, ph))
            x = k * pw
            canv.paste(img, (x, label_h))
            dr.rectangle([x, 0, x + pw - 1, label_h], fill=(24, 24, 28))
            dr.text((x + 10, 9), f"PDF page {pno + 1} / {n}   [{name}]", fill=(255, 220, 0))
            dr.rectangle([x, label_h, x + pw - 1, label_h + ph - 1], outline=(90, 90, 96))
        canv.save(os.path.join(out, f"sheet_{sheet_i:02d}.png"), optimize=True)
    doc.close()
    print(f"wrote {sheet_i} sheets -> {out}")


if __name__ == "__main__":
    main()
