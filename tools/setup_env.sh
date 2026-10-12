#!/bin/sh
# Run at the START of every Twin 1 session: the sandbox resets everything except the repo.
# Installs the renderer + document libs, then renders the page PNGs this worker needs.
set -e
pip install --quiet --break-system-packages pymupdf openpyxl python-docx
mkdir -p /home/user/work/pages
if [ $# -gt 0 ]; then
  for k in "$@"; do python3 tools/render_pages.py --lecture "$k" --scale 1.25 >/dev/null; done
fi
echo "env ready; pages in /home/user/work/pages"
