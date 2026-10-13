"""Split DIBY-book text into prose and already-typeset LaTeX maths.

The class-note pipeline (ocr_math_to_latex.py) turns OCR output like
"(x^m + 1/x^2)^22" into LaTeX. The DIBY-only books need the opposite: their text
is already LaTeX-ish (\\frac{…}{…}, x^{2}, log_{8}), so spans are detected
directly and handed to pandoc as LaTeX — no re-interpretation.
"""
from __future__ import annotations

import re

STRONG = re.compile(r"[\d=+\-*/^_<>()\[\]|≤≥≠∈∉∪∩⊂⊆×÷·∑∏∫πθαβγδλμ∅∞√]")
LATEXY = re.compile(r"\\frac|\\sqrt|\\left|\\right|\^|_|\\[a-zA-Z]{2,}")
FUNCS = {"log", "ln", "sin", "cos", "tan", "cot", "sec", "cosec", "csc", "lim",
         "max", "min", "exp", "mod", "det", "gcd", "lcm", "sqrt"}
# prose words that end a maths run even when the token looks numeric
STOP = set("""is are was were the a an of for then than that this these those find
value values sum sums term terms root roots equation equations solution solutions
satisfying following possible minimum maximum real positive negative integral
integer number numbers number if let so and or but with from which when where all
any also both each be been being do does did can could will would shall should
hence find given suppose consider then respectively equal equals""".split())

UNICODE_TEX = {
    "≤": r"\le ", "≥": r"\ge ", "≠": r"\ne ", "∈": r"\in ", "∉": r"\notin ",
    "∪": r"\cup ", "∩": r"\cap ", "⊂": r"\subset ", "⊆": r"\subseteq ",
    "×": r"\times ", "÷": r"\div ", "·": r"\cdot ", "∑": r"\sum ", "∏": r"\prod ",
    "∫": r"\int ", "π": r"\pi ", "θ": r"\theta ", "α": r"\alpha ", "β": r"\beta ",
    "γ": r"\gamma ", "δ": r"\delta ", "λ": r"\lambda ", "μ": r"\mu ",
    "∅": r"\emptyset ", "∞": r"\infty ", "⋯": r"\cdots ", "⋅": r"\cdot ",
    "→": r"\to ", "±": r"\pm ", "∀": r"\forall ", "𝝅": r"\pi ",
}


def _fix_sqrt(text: str) -> str:
    """√(x^2+5) -> \\sqrt{x^2+5}, matching the closing parenthesis."""
    out, i = "", 0
    while i < len(text):
        if text[i] == "√" and i + 1 < len(text) and text[i + 1] == "(":
            depth, j = 0, i + 1
            while j < len(text):
                if text[j] == "(":
                    depth += 1
                elif text[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            inner = text[i + 2:j]
            out += "\\sqrt{" + _fix_sqrt(inner) + "}"
            i = j + 1
            continue
        out += text[i]
        i += 1
    return out


def _texify(span: str) -> str:
    span = _fix_sqrt(span)
    return "".join(UNICODE_TEX.get(c, c) for c in span).strip()


OPT_MARK = re.compile(r"^\(?\s*[A-D]\s*\)$")


def _token_kind(tok: str) -> bool | None:
    """True = maths, False = prose, None = neutral (keeps the run alive)."""
    t = tok.strip()
    if OPT_MARK.match(t):
        return False                                    # end the run at (A)…(D)
    core = t.strip(".,;:!?'’\"()[]")
    if not core:
        return None
    if LATEXY.search(core):
        return True
    if core.lower() in STOP:
        return False
    if core.lower() in FUNCS:
        return True
    if STRONG.search(core):
        return True
    if re.fullmatch(r"[A-Za-z]", core):                 # single-letter variable
        return True
    if re.fullmatch(r"[A-Za-z]{1,4}", core) and core.islower() and len(core) <= 2:
        return True                                     # e, xi, dy …
    return False


def segments_latex(text: str) -> list[tuple[str, str]]:
    """[(kind, value)] where kind is 'text' or 'math' (value is LaTeX)."""
    text = text or ""
    tokens = re.findall(r"\S+", text)
    if not tokens:
        return [("text", text)]
    kinds = [_token_kind(t) for t in tokens]
    out: list[tuple[str, str]] = []
    i = 0
    while i < len(tokens):
        if kinds[i] is not True:
            j = i
            while j < len(tokens) and kinds[j] is not True:
                j += 1
            out.append(("text", " ".join(tokens[i:j])))
            i = j
            continue
        j = i
        last_math = i
        while j < len(tokens) and kinds[j] is not False:
            if kinds[j] is True:
                last_math = j
            j += 1
        run = tokens[i:last_math + 1]
        span = " ".join(run)
        strong = bool(re.search(r"[0-9\\^_=+\-*/≤≥≠∈∪∩×∑√∞πθαβγ∅]", span))
        if strong and len(span) >= 2:
            out.append(("math", _texify(span)))
        else:
            out.append(("text", span))
        i = last_math + 1
    merged: list[tuple[str, str]] = []
    for kind, val in out:
        if merged and merged[-1][0] == kind and kind == "text":
            merged[-1] = (kind, merged[-1][1] + " " + val)
        else:
            merged.append((kind, val))
    return merged or [("text", text)]


SYMBOL_TEX = {v.strip(): k for k, v in UNICODE_TEX.items()}
TEXT_TEX = {"cdot": "·", "times": "×", "ge": "≥", "le": "≤", "ne": "≠", "in": "∈",
            "notin": "∉", "infty": "∞", "pi": "π", "theta": "θ", "alpha": "α",
            "beta": "β", "gamma": "γ", "delta": "δ", "lambda": "λ", "mu": "μ",
            "cup": "∪", "cap": "∩", "emptyset": "∅", "cdots": "⋯", "ldots": "…",
            "to": "→", "pm": "±", "subset": "⊂", "subseteq": "⊆", "sum": "∑",
            "prod": "∏", "int": "∫", "div": "÷", "forall": "∀", "qquad": " ",
            "quad": " ", "left": "", "right": "", ",": "", ";": "", "!": ""}


ILLEGAL_TEX = str.maketrans({'"': "", "%": "", "#": "", "&": "", "$": "", "~": "", "`": ""})


def repair_latex(tex: str) -> str:
    r"""Mechanically repair OCR breakage so pandoc can typeset the span.

    Only characters that cannot appear in LaTeX maths are touched, plus unbalanced
    braces and dangling \left / \right — nothing is invented.
    """
    out = tex.translate(ILLEGAL_TEX)
    out = out.replace("<=", "\\le ").replace(">=", "\\ge ")
    out = re.sub(r'\\cdot\s*"', r"\\cdots ", out)
    # dangling \left / \right (no partner) break the parser -> plain brackets
    for cmd, plain in (("\\left", "("), ("\\right", ")")):
        opens = len(re.findall(re.escape(cmd) + r"[.([{|]", out))
        closes = len(re.findall(re.escape(cmd) + r"[.\])|}]", out))
        while opens > closes:
            out = re.sub(re.escape(cmd) + r"([.([{|])", plain, out, count=1)
            opens -= 1
        while closes > opens:
            out = re.sub(re.escape(cmd) + r"([.\])|}])", plain, out, count=1)
            closes -= 1
    # a dangling superscript / subscript ('x^' or 'x_') cannot be parsed
    out = re.sub(r"[\^_](?=\s*[)} \],]|\s*$)", "", out)
    depth = out.count("{") - out.count("}")
    if depth > 0:
        out += "}" * depth
    elif depth < 0:                      # drop surplus closers from the end
        for _ in range(-depth):
            i = out.rfind("}")
            if i < 0:
                break
            out = out[:i] + out[i + 1:]
    return re.sub(r"\s{2,}", " ", out).strip()


def latex_fallback(tex: str) -> str:
    """Readable plain text for maths pandoc cannot typeset (unbalanced spans)."""
    out = tex
    for _ in range(6):                                 # unwind nested \frac
        new = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", out)
        if new == out:
            break
        out = new
    out = re.sub(r"\\sqrt\{([^{}]*)\}", r"√(\1)", out)
    for cmd in sorted(TEXT_TEX, key=len, reverse=True):     # \\infty before \\in
        out = re.sub(r"\\" + cmd + r"(?![A-Za-z])", lambda m, ch=TEXT_TEX[cmd]: ch, out)
    out = re.sub(r"\\[A-Za-z]+", "", out)
    out = out.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s{2,}", " ", out).strip()


if __name__ == "__main__":
    tests = [
        "2log_{8}2x+ log_{8}x^{2}-2x+ 1=\\frac{4}{3} is.",
        "(A) \\frac{n}{3}16n^{2}+ 12n-1   (B) \\frac{n}{3}16n^{2}-12n+ 1",
        "Find the sum of the first n terms of the series 3^{2}+ 7^{2}+ 11^{2}+ ⋯up to nterms",
        "If S_{1}, S_{2}, S_{3}, … . S_{p} are the sums of infinite G.P.",
        "log_{7}\\frac{2x-6}{2x-1}≥0",
        "Number of real solution of: log_{5}[2 + log_{3}(x + 3)] = 0 is",
        "If the equations x^{3}+ x^{2}-4x= 4and x^{2}+ px+ 2p= 0 (p∈R) have two roots common",
    ]
    for t in tests:
        print("IN :", t)
        for k, v in segments_latex(t):
            print(f"   [{k:4s}] {v!r}")
        print()

def smart_segments(text: str) -> list[tuple[str, str]]:
    """[(kind, value)] for text that may hold *either* OCR-style or LaTeX-style maths.

    The class-note register and the DIBY-book register were written by different
    pipelines: one holds linear OCR maths ('(5rt3/x + 2x/rt3(5))^12'), the other holds
    LaTeX ('\\frac{a}{b}'). Running the OCR splitter alone left the LaTeX half inside
    'text' pieces, which printed as raw LaTeX in the document.

    Here the OCR splitter runs first (it turns linear maths into LaTeX), then every
    remaining *text* piece is re-split with the LaTeX splitter when it still carries a
    backslash command — so no text piece can ever leak raw LaTeX to the page.
    """
    from ocr_math_to_latex import segments as ocr_segments      # local import: optional dep

    out: list[tuple[str, str]] = []
    # a text piece is re-split when it still carries LaTeX or unmistakable maths
    latex_hint = re.compile(
        r"\\"                                        # any backslash command
        r"|[_^]\s*[\dA-Za-z{(]"                       # x^2, a_1
        r"|\d\s*[a-zA-Z]\s*[=+\-/]"                     # 56x= , 9y+
        r"|[a-zA-Z]\s*[=]\s*[-\d]"                       # x= 5
        r"|[≤≥≠∈∪∩√∞∑∏∫]"                                 # unicode maths
        r"|\d+\s*/\s*\d"                              # 5/2
    )
    for kind, val in ocr_segments(text or ""):
        if kind == "math" or not val or not latex_hint.search(val):
            out.append((kind, val))
            continue
        for k2, v2 in segments_latex(val):
            out.append((k2, v2))
    merged: list[tuple[str, str]] = []
    for kind, val in out:
        if merged and merged[-1][0] == kind:
            merged[-1] = (kind, merged[-1][1] + " " + val)
        else:
            merged.append((kind, val))
    return merged or [("text", text or "")]


def est_lines(text: str, chars_per_line: int) -> int:
    """Rough height of a paragraph in lines (used to decide keep-together)."""
    if not text:
        return 0
    return max(1, -(-len(text) // max(10, chars_per_line)))


def keep_whole(chars: int, chars_per_line: int, max_lines: int = 8) -> bool:
    """Should this item be kept on one page, or allowed to flow and fill the page?

    Keeping every item whole is what leaves half-empty pages: an item that does not fit
    in what is left of a page is pushed to the next one in full. Items that are short
    enough to fit comfortably are still kept together; taller ones may split.
    """
    return -(-chars // max(10, chars_per_line)) <= max_lines
