"""Render selected PDF pages to PNG for page-by-page visual transcription/QA.
Scratch images are written OUTSIDE the repo (/home/user/work/pages) so they never bloat the patchset."""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(__file__))
import pymupdf
from twin1_scope import REPO_ROOT, TWIN1_SCOPE

OUT = "/home/user/work/pages"

def key_for(fn):  # short stable key per file
    import re
    ch = "bt" if fn.startswith("Binomial") else "pc"
    n = re.search(r"(\d\d)", fn).group(1)
    return f"{ch}{n}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lecture"); ap.add_argument("--pages"); ap.add_argument("--scale", type=float, default=1.25)
    a = ap.parse_args()
    for ch, lec, fn, _ in TWIN1_SCOPE:
        k = key_for(fn)
        if a.lecture and k != a.lecture:
            continue
        doc = pymupdf.open(os.path.join(REPO_ROOT, fn))
        want = list(range(1, doc.page_count + 1)) if not a.pages else [int(x) for x in a.pages.split(",")]
        m = pymupdf.Matrix(a.scale, a.scale)
        for pno in want:
            out = f"{OUT}/{k}_p{pno:02d}.png"
            if os.path.exists(out):
                print("cached", out); continue
            pix = doc[pno - 1].get_pixmap(matrix=m)
            pix.save(out)
            print("wrote", out, f"{pix.width}x{pix.height}")
        doc.close()

if __name__ == "__main__":
    main()
