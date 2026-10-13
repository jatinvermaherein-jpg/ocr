#!/usr/bin/env python3
"""Estimate how much of every page a DIBY document actually fills.

There is no Word / LibreOffice in this repo, so page breaks cannot be measured
directly. This simulator computes each paragraph's height from its font size and
character count and then replays Word's page-break rules:

* a paragraph with `keepNext` must share a page with the paragraph after it,
* a paragraph with `keepLines` may not be split across pages,
* a paragraph without `keepLines` splits and wraps onto the next page,
* a paragraph that ends a section closes the page; when that section is
  `oddPage` (every chapter in these documents), a blank page is inserted when
  needed so the next chapter opens on an odd page.

Only the blanks that are *not* followed by a chapter start are real problems —
those are the "half a page empty in the middle of a chapter" ones.

    python3 tools/simulate_page_fill.py deliverables/DIBY_Books_Print.docx ...
"""
from __future__ import annotations

import sys
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
CM_PT = 28.3465                 # points per cm
TW = 566.93                     # twips per cm


def _val(el, attr=W + "val", default=None):
    return el.get(attr) if el is not None else default


def style_sizes(zpath):
    """({style id: half-point size}, {style id: basedOn}, default half-point size)."""
    try:
        st = ET.fromstring(zipfile.ZipFile(zpath).read("word/styles.xml"))
    except KeyError:
        return {}, {}, 22
    sizes, based = {}, {}
    for style in st.iter(W + "style"):
        sid = _val(style, W + "styleId")
        sz = style.find(W + "rPr/" + W + "sz")
        if sz is not None and _val(sz):
            sizes[sid] = int(_val(sz))
        bo = _val(style.find(W + "basedOn"))
        if bo:
            based[sid] = bo
    default = st.find(W + "docDefaults/" + W + "rPrDefault/" + W + "rPr/" + W + "sz")
    return sizes, based, int(_val(default) or 22)


def resolve_size(styles, based, doc_default, sid):
    """Font size of a paragraph style, following basedOn up to Normal."""
    seen = set()
    while sid and sid not in seen:
        seen.add(sid)
        if sid in styles:
            return styles[sid] / 2
        sid = based.get(sid)
    for fallback in ("Normal", "a"):
        if fallback in styles:
            return styles[fallback] / 2
    return doc_default


def sect_layout(sec):
    pg = sec.find(W + "pgSz")
    mar = sec.find(W + "pgMar")
    w = int(_val(pg, W + "w", "11906")) if pg is not None else 11906
    h = int(_val(pg, W + "h", "16838")) if pg is not None else 16838
    ml = int(_val(mar, W + "left", "1134")) if mar is not None else 1134
    mr = int(_val(mar, W + "right", "1134")) if mar is not None else 1134
    mt = int(_val(mar, W + "top", "1134")) if mar is not None else 1134
    mb = int(_val(mar, W + "bottom", "1134")) if mar is not None else 1134
    typ = _val(sec.find(W + "type"), default="nextPage") or "nextPage"
    return dict(text_w=(w - ml - mr) / TW, text_h=(h - mt - mb) / TW,
                ml=ml / TW, kind=typ)


def para_height(p, size_default=11.0, width_cm=16.0, styles=None, doc_default=11.0,
                based=None):
    styles = styles or {}
    based = based or {}
    pr = p.find(W + "pPr")
    kn_el = pr.find(W + "keepNext") if pr is not None else None
    kl_el = pr.find(W + "keepLines") if pr is not None else None
    keep_next = kn_el is not None and (_val(kn_el, default="1") not in ("0", "false"))
    keep_lines = kl_el is not None and (_val(kl_el, default="1") not in ("0", "false"))
    sizes = [int(_val(r.find(W + "rPr/" + W + "sz"), default="0") or 0) / 2
             for r in p.findall(W + "r") if r.find(W + "rPr/" + W + "sz") is not None]
    mark = pr.find(W + "rPr/" + W + "sz") if pr is not None else None
    if mark is not None:
        sizes.append(int(_val(mark, default="0") or 0) / 2)
    if not sizes:
        sid = _val(pr.find(W + "pStyle")) if pr is not None else None
        sizes.append(resolve_size(styles, based, doc_default, sid))
    size = max(sizes) if sizes else size_default
    if size <= 0:
        size = size_default
    text = "".join(t.text or "" for t in p.iter(W + "t"))
    chars = len(text) + 6 * len(p.findall(".//" + W + "tab"))
    if p.find(".//" + M + "oMath") is not None:      # an equation is one wide glyph run
        chars = int(chars * 1.1) + 4
    cpl = max(8.0, width_cm / (0.0177 * size))
    lines = max(1, int(chars / cpl) + (1 if chars % cpl else 0))
    sp = pr.find(W + "spacing") if pr is not None else None
    before = int(_val(sp, W + "before", "0") or 0) / 20 / CM_PT if sp is not None else 0
    after = int(_val(sp, W + "after", "0") or 0) / 20 / CM_PT if sp is not None else 0
    line_h = size * 1.2 / CM_PT
    return lines * line_h + before + after, keep_next, keep_lines, size


def simulate(path, verbose=True):
    styles, based, doc_default_hp = style_sizes(path)
    doc_default = doc_default_hp / 2
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find(W + "body")
    children = [c for c in body if c.tag in (W + "p", W + "tbl", W + "sectPr")]

    first_sec = None
    for c in children:
        sec = c.find(W + "pPr/" + W + "sectPr") if c.tag == W + "p" else (c if c.tag == W + "sectPr" else None)
        if sec is not None:
            first_sec = sec
            break
    lay = sect_layout(first_sec)

    pages = []                       # (used_cm, label)
    used = 0.0
    label = "body"

    def flush(kind="body"):
        nonlocal used, label
        if used > 0 or pages:
            pages.append([used, label])
        used = 0.0
        label = kind

    # group paragraphs glued together by keepNext
    groups = []
    i = 0
    while i < len(children):
        c = children[i]
        if c.tag == W + "sectPr":
            groups.append(("sect", c))
            i += 1
            continue
        if c.tag == W + "tbl":
            h = 0.5 * len(c.findall(W + "tr"))
            groups.append(("tbl", [(h, False, True)]))
            i += 1
            continue
        h, kn, kl, size = para_height(c, doc_default, lay["text_w"], styles, doc_default,
                                      based)
        grp = [(h, kn, kl)]
        j = i + 1
        while kn and j < len(children) and children[j].tag == W + "p":
            nh, nkn, nkl, _ = para_height(children[j], doc_default, lay["text_w"],
                                          styles, doc_default, based)
            grp.append((nh, nkn, nkl))
            kn = nkn
            j += 1
        groups.append(("p", grp, c))
        i = j

    for g in groups:
        if g[0] == "sect":
            lay = sect_layout(g[1])
            continue
        if g[0] == "tbl":
            grp = g[1]
        else:
            grp = g[1]
        total = sum(x[0] for x in grp)
        if total > lay["text_h"]:                 # Word cannot honour this chain
            grp = [(h, False, kl) for h, kn, kl in grp]
            total = sum(x[0] for x in grp)
        split_ok = not any(x[2] for x in grp) and len(grp) == 1
        if not split_ok and used > 0 and used + total > lay["text_h"]:
            flush()
        if split_ok:
            remaining = total
            while remaining > 0.01:
                space = lay["text_h"] - used
                if space <= 0.01:
                    flush()
                    continue
                take = min(space, remaining)
                used += take
                remaining -= take
                if remaining > 0.01:
                    flush()
        else:
            used += total
            if used > lay["text_h"]:
                used = lay["text_h"]          # group taller than a page
        # a section that ends on this paragraph closes the page
        if g[0] == "p":
            sec = g[2].find(W + "pPr/" + W + "sectPr")
            if sec is not None:
                lay2 = sect_layout(sec)
                flush()
                if lay2["kind"] == "oddPage" and (len(pages) + 1) % 2 == 0:
                    pages.append([0.0, "blank (chapter opens on an odd page)"])
                label = "chapter"
                lay = lay2
    if used > 0:
        flush()

    text_h = lay["text_h"]
    wasted = [max(0.0, text_h - p[0]) for p in pages]
    # a gap is fine when the next page starts a chapter
    real = []
    for i, w in enumerate(wasted):
        nxt = pages[i + 1][1] if i + 1 < len(pages) else "end"
        this = pages[i][1]
        if nxt in ("chapter", "blank (chapter opens on an odd page)") or nxt == "end":
            continue                      # a chapter boundary may leave a page short
        if this == "blank (chapter opens on an odd page)":
            continue
        if w > 0.25 * text_h:
            real.append((w, i + 1))
    content = sum(p[0] for p in pages) / text_h
    if verbose:
        print(f"--- {path}")
        print(f"    estimated pages: {len(pages)} | text = {content:.1f} page-heights | "
              f"average fill {100 * content / max(1, len(pages)):.0f}%")
        print(f"    mid-chapter pages more than a quarter empty: {len(real)}")
        for w, n in sorted(real, reverse=True)[:8]:
            print(f"      page {n}: {w:.1f} cm of {text_h:.1f} cm empty "
                  f"({100 * w / text_h:.0f}%)")
    return len(pages), len(real), wasted, pages


def dump_page(path, target):
    """Print the paragraphs the simulator puts on one estimated page."""
    styles, based, dh = style_sizes(path)
    dd = dh / 2
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find(W + "body")
    children = [c for c in body if c.tag == W + "p"]
    sec = [c for c in children if c.find(W + "pPr/" + W + "sectPr") is not None][0] \
        .find(W + "pPr/" + W + "sectPr")
    lay = sect_layout(sec)
    used, page, keep = 0.0, 1, 0
    for i, p in enumerate(children):
        h, kn, kl, size = para_height(p, dd, lay["text_w"], styles, dd, based)
        if keep:
            keep -= 1
        elif used > 0 and used + h > lay["text_h"]:
            page += 1
            used = 0.0
        used += h
        if kn:
            keep += 1
        if page == target:
            text = "".join(t.text or "" for t in p.iter(W + "t"))[:95]
            print(f"  i={i:5d} h={h:5.2f} used={used:5.1f} kn={int(kn)} kl={int(kl)} "
                  f"sz={size:4.1f} :: {text!r}")
    print(f"  page {target} of {page}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--page":
        dump_page(args[2], int(args[1]))
        sys.exit(0)
    for f in args:
        try:
            simulate(f)
        except Exception as e:                     # noqa: BLE001
            import traceback
            print(f"--- {f}\n    FAILED: {e}")
            traceback.print_exc()
