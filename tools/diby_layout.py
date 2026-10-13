"""Layout-aware text reconstruction for the DIBY books.

These slides carry maths as positioned glyph runs, so the naive text layer turns
S₁ into "S1", a fraction 2/1! into "2 1!" and x² into "x2". Each page is rebuilt
from span geometry:

  · spans are clustered into rows by baseline,
  · a short span that follows body-size text becomes ^{…} or _{…} (never a
    bare "Ans:" run, never a detached chunk),
  · a short segment sitting directly above another — close by, horizontally
    overlapping and centre-aligned — is a stacked fraction → \\frac{…}{…},
  · a maths-only leftover row (fractions of a display sum) is merged into the
    line it belongs to instead of being printed as debris.
"""
from __future__ import annotations

import re

MATH_ALPHANUM = [
    (0x1D400, 0x1D419, ord("A")), (0x1D41A, 0x1D433, ord("a")),
    (0x1D434, 0x1D44D, ord("A")), (0x1D44E, 0x1D467, ord("a")),
    (0x1D468, 0x1D481, ord("A")), (0x1D482, 0x1D49B, ord("a")),
    (0x1D49C, 0x1D4B5, ord("A")), (0x1D4B6, 0x1D4CF, ord("a")),
    (0x1D4D0, 0x1D4E9, ord("A")), (0x1D4EA, 0x1D503, ord("a")),
    (0x1D504, 0x1D51D, ord("A")), (0x1D51E, 0x1D537, ord("a")),
    (0x1D538, 0x1D551, ord("A")), (0x1D552, 0x1D56B, ord("a")),
    (0x1D56C, 0x1D585, ord("A")), (0x1D586, 0x1D59F, ord("a")),
    (0x1D5A0, 0x1D5B9, ord("A")), (0x1D5BA, 0x1D5D3, ord("a")),
    (0x1D5D4, 0x1D5ED, ord("A")), (0x1D5EE, 0x1D607, ord("a")),
    (0x1D608, 0x1D621, ord("A")), (0x1D622, 0x1D63B, ord("a")),
    (0x1D63C, 0x1D655, ord("A")), (0x1D656, 0x1D66F, ord("a")),
    (0x1D670, 0x1D689, ord("A")), (0x1D68A, 0x1D6A3, ord("a")),
    (0x1D7CE, 0x1D7D7, ord("0")), (0x1D7D8, 0x1D7E1, ord("0")),
    (0x1D7E2, 0x1D7EB, ord("0")), (0x1D7EC, 0x1D7F5, ord("0")),
    (0x1D7F6, 0x1D7FF, ord("0")),
]
GREEK_MATH = ("ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡϴΣΤΥΦΧΨΩ∇"
              "αβγδεζηθικλμνξοπρςστυφχψω∂εϑϰϕϱϖ")
GREEK = {"\U0001D6FC": "α", "\U0001D6FD": "β", "\U0001D6FE": "γ", "\U0001D6FF": "δ",
         "\U0001D70B": "π", "\U0001D703": "θ", "\U0001D706": "λ", "\U0001D707": "μ",
         "\U0001D711": "φ"}
CHAR_FIX = {"−": "-", "–": "-", "—": "-", "∶": ":", "′": "'",
            "\u00a0": " ", "\u2009": " ", "\u200a": " "}
# Symbol-font code points (private use area) seen in these books
PUA = {"\uf0a5": "∞", "\uf0ce": "∈", "\uf0cf": "∉", "\uf0c8": "∪", "\uf0c7": "∩",
       "\uf0cc": "⊂", "\uf0cb": "⊆", "\uf0c6": "≠", "\uf0b9": "≠", "\uf0a3": "≤",
       "\uf0b3": "≥", "\uf0d7": "×", "\uf0b1": "±", "\uf066": "∅", "\uf022": "∀",
       "\uf070": "π", "\uf071": "θ", "\uf061": "α", "\uf062": "β", "\uf064": "δ",
       "\uf067": "γ", "\uf06c": "λ", "\uf06d": "μ", "\uf0b0": "°"}

OPT_LABEL = re.compile(r"^\(\s*[a-dA-D]\s*\)$")
WORD = re.compile(r"[A-Za-z]{3,}")


def norm_char(ch: str) -> str:
    o = ord(ch)
    if 0x1D6A8 <= o <= 0x1D7C9:                    # mathematical Greek alphabets
        return GREEK_MATH[(o - 0x1D6A8) % 58]
    for lo, hi, base in MATH_ALPHANUM:
        if lo <= o <= hi:
            return chr(base + (o - lo))
    if ch in GREEK:
        return GREEK[ch]
    if ch in PUA:
        return PUA[ch]
    return CHAR_FIX.get(ch, ch)


def normalise(s: str) -> str:
    return "".join(norm_char(c) for c in s)


class Span:
    __slots__ = ("text", "size", "x0", "x1", "top", "base")

    def __init__(self, s: dict):
        self.text = normalise(s["text"])
        self.size = float(s["size"])
        self.x0, _, self.x1, _ = s["bbox"]
        self.top = float(s["bbox"][1])
        self.base = float(s["origin"][1])

    @property
    def w(self) -> float:
        return self.x1 - self.x0


def _collect(page) -> list[Span]:
    out = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for s in line["spans"]:
                if s["text"].strip():
                    out.append(Span(s))
    return out


def _cluster_rows(spans: list[Span], tol: float) -> list[list[Span]]:
    """Group spans into rows by baseline, against the row's running mean.

    Comparing with the mean (not the first span) stops long chains of slightly
    offset glyphs — the usual shape of a display fraction — from splitting.
    """
    rows: list[list[Span]] = []
    sums: list[float] = []
    for sp in sorted(spans, key=lambda s: s.base):
        if rows and abs(sp.base - sums[-1] / len(rows[-1])) <= tol:
            rows[-1].append(sp)
            sums[-1] += sp.base
        else:
            rows.append([sp])
            sums.append(sp.base)
    for r in rows:
        r.sort(key=lambda s: s.x0)
    return rows


def _segments(row: list[Span], gap: float = 26.0) -> list[list[Span]]:
    segs: list[list[Span]] = []
    for sp in row:
        if segs and sp.x0 - segs[-1][-1].x1 <= gap:
            segs[-1].append(sp)
        else:
            segs.append([sp])
    return segs


def _row_body_base(row: list[Span], body: float) -> float:
    """Baseline of the row's body-size text (scripts ignored), width weighted."""
    big = [s for s in row if s.size >= body * 0.88] or row
    tot = sum(s.w for s in big) or 1.0
    return sum(s.base * s.w for s in big) / tot


def _render_seg(seg: list[Span], body: float, base: float) -> str:
    """One segment's text, marking scripts that attach to body-size glyphs."""
    out = ""
    last_body = False
    for sp in seg:
        txt = sp.text
        is_body = sp.size >= body * 0.88
        small = sp.size < body * 0.88 and len(txt.strip()) <= 5
        dy = sp.base - base
        if last_body and small and dy < -9:
            out += "^{" + txt.strip() + "}"
        elif last_body and small and dy > 9:
            out += "_{" + txt.strip() + "}"
        else:
            out += txt
        last_body = is_body
    return out


def _join(a: str, b: str) -> str:
    if a and b and a[-1].isalnum() and b[0].isalnum():
        return a + " " + b
    return a + b


def _good_frac_part(txt: str) -> bool:
    t = txt.strip()
    if not t or OPT_LABEL.match(t):
        return False
    if not re.search(r"[0-9A-Za-zα-ωΑ-Ω]", t):
        return False
    if "Ans" in t or t.startswith("["):
        return False
    if len(re.findall(r"[A-Za-z]{3,}", t)) >= 2:
        return False
    if t.endswith((",", "(A)", "(B)", "(C)", "(D)")):
        return False
    if re.search(r",\s*-?\d", t):
        return False
    return True


def _column_cuts(segs_per_row) -> list[float]:
    """x positions where an (A)/(B)/(C)/(D) option cell starts — column separators."""
    xs = []
    for segs in segs_per_row:
        for seg in segs:
            if re.match(r"^\(\s*[A-D]\s*\)", seg[0].text):
                xs.append(seg[0].x0)
    xs.sort()
    cuts = []
    for x in xs:
        if not cuts or x - cuts[-1] > 100:
            cuts.append(x)
    return cuts


def _column(cuts: list[float], x: float) -> int:
    i = 0
    while i < len(cuts) and cuts[i] <= x:
        i += 1
    return i                      # 0 = before the first option cell


def _find_fractions(segs_per_row, bodies, bases):
    """Stacked fractions: a short segment directly over another, close and aligned.

    The two halves must sit in the same column, so fractions inside side-by-side
    option cells never get crossed with each other.
    """
    used, pairs = set(), []
    cuts = _column_cuts(segs_per_row)
    for di, dsegs in enumerate(segs_per_row):
        bd = bases[di]
        for si, dseg in enumerate(dsegs):
            if (di, si) in used:
                continue
            dx0, dx1 = dseg[0].x0, dseg[-1].x1
            dw = dx1 - dx0
            if dw > 320 or len(dseg) > 6:
                continue
            dc = (dx0 + dx1) / 2
            best = None
            for ui in range(len(segs_per_row)):
                if not ui or ui == di:
                    continue
                bu = bases[ui]
                if not (22 <= bd - bu <= 150):
                    continue
                for sj, useg in enumerate(segs_per_row[ui]):
                    if (ui, sj) in used:
                        continue
                    ux0, ux1 = useg[0].x0, useg[-1].x1
                    uw = ux1 - ux0
                    if uw > 320 or len(useg) > 8:
                        continue
                    if _column(cuts, ux0) != _column(cuts, dx0):
                        continue
                    if min(ux1, dx1) - max(ux0, dx0) < 0.55 * min(uw, dw):
                        continue
                    if abs((ux0 + ux1) / 2 - dc) > 0.30 * max(uw, dw) + 12:
                        continue
                    if best is None or bu > bases[best[0]]:
                        best = (ui, sj, useg)
            if best is None:
                continue
            ui, sj, useg = best
            num = _render_seg(useg, bodies[ui], bases[ui]).strip()
            den = _render_seg(dseg, bodies[di], bd).strip()
            if not (_good_frac_part(num) and _good_frac_part(den)):
                continue
            used.add((ui, sj))
            used.add((di, si))
            pairs.append({"ub": bases[ui], "db": bd, "cx": dc,
                          "text": "\\frac{" + num + "}{" + den + "}",
                          "u": (ui, sj), "d": (di, si)})
    return pairs


def _is_math_only_row(items: list[tuple[float, str]]) -> bool:
    txt = " ".join(t for _, t in items)
    return bool(txt.strip()) and not WORD.search(txt)


def page_rows(page) -> list[str]:
    """Reconstructed text rows for one page, top to bottom, fractions folded in."""
    spans = _collect(page)
    if not spans:
        return []
    body = max((s.size for s in spans if len(s.text) > 25), default=max(s.size for s in spans))
    rows = _cluster_rows(spans, min(max(30.0, 0.50 * body), 60.0))
    if not rows:
        return []
    segs_per_row = [_segments(r) for r in rows]
    bodies = [max(s.size for s in r) for r in rows]
    bases = [_row_body_base(r, bodies[i]) for i, r in enumerate(rows)]

    pairs = _find_fractions(segs_per_row, bodies, bases)
    folded_u = {p["u"] for p in pairs}
    folded_d = {p["d"] for p in pairs}

    lines = []                                     # (base, [(x, text), …])
    for i, row in enumerate(rows):
        items = []
        for si, seg in enumerate(segs_per_row[i]):
            if (i, si) in folded_u or (i, si) in folded_d:
                continue
            txt = _render_seg(seg, bodies[i], bases[i])
            if txt.strip():
                items.append((seg[0].x0, txt))
        lines.append({"base": bases[i], "items": items, "used": False})

    for p in pairs:                                # a fraction joins its own line
        carrier = min(lines, key=lambda L: abs(L["base"] - (p["ub"] + p["db"]) / 2))
        carrier["items"].append((p["cx"], p["text"]))
        carrier["used"] = True

    # maths-only debris rows (stacked parts of a display sum) rejoin that line
    merged = [False] * len(lines)
    for i, L in enumerate(lines):
        if merged[i] or not L["items"] or L["used"]:
            continue
        if not _is_math_only_row(L["items"]):
            continue
        near = [j for j, M in enumerate(lines)
                if j != i and not merged[j] and M["items"] and abs(M["base"] - L["base"]) <= 165]
        if not near:
            continue
        host = min(near, key=lambda j: abs(lines[j]["base"] - L["base"]))
        lines[host]["items"].extend(L["items"])
        merged[i] = True

    out = []
    for i, L in enumerate(lines):
        if merged[i]:
            continue
        text = ""
        for _, piece in sorted(L["items"], key=lambda t: t[0]):
            text = _join(text, piece)
        text = " ".join(text.split())
        if not text:
            continue
        cells = [c.strip() for c in re.split(r"(?=\(\s*[A-D]\s*\))", text) if c.strip()]
        out.extend(cells)
    return out


def page_line_stream(doc) -> list[tuple[int, str]]:
    out = []
    for pno in range(doc.page_count):
        for txt in page_rows(doc[pno]):
            out.append((pno + 1, txt))
    return out
