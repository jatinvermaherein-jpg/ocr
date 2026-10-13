#!/usr/bin/env python3
"""Detect maths inside OCR question text and turn it into LaTeX.

OCR of these class notes writes maths in a linear, ASCII form:
    (x^m + 1/x^2)^22      ->  \\left(x^{m}+\\frac{1}{x^{2}}\\right)^{22}
    x^-6                  ->  x^{-6}
    sinx + cosx           ->  \\sin x+\\cos x
    sqrt(a)x^2            ->  \\sqrt{a}x^{2}

The converter is deliberately conservative: anything it is not sure about is
returned as plain text, so a question can never be mangled by it.
"""
from __future__ import annotations

import re

# ----------------------------------------------------------------- symbol tables
SYMBOLS = {
    "≤": r"\le ", "≥": r"\ge ", "≠": r"\ne ", "∞": r"\infty ", "∈": r"\in ",
    "→": r"\to ", "⇒": r"\Rightarrow ", "⇔": r"\Leftrightarrow ", "±": r"\pm ",
    "∓": r"\mp ", "·": r"\cdot ", "×": r"\times ", "÷": r"\div ", "−": "-",
    "∑": r"\sum ", "Σ": r"\sum ", "∫": r"\int ", "∏": r"\prod ", "√": r"\sqrt ",
    "∴": r"\therefore ", "≈": r"\approx ", "≡": r"\equiv ", "⊥": r"\perp ",
    "∥": r"\parallel ", "∠": r"\angle ", "°": r"^{\circ}", "′": "'",
    "α": r"\alpha ", "β": r"\beta ", "γ": r"\gamma ", "δ": r"\delta ",
    "ε": r"\epsilon ", "ζ": r"\zeta ", "η": r"\eta ", "θ": r"\theta ",
    "ι": r"\iota ", "κ": r"\kappa ", "λ": r"\lambda ", "μ": r"\mu ",
    "ν": r"\nu ", "ξ": r"\xi ", "π": r"\pi ", "ρ": r"\rho ", "σ": r"\sigma ",
    "τ": r"\tau ", "υ": r"\upsilon ", "φ": r"\phi ", "χ": r"\chi ",
    "ψ": r"\psi ", "ω": r"\omega ", "Γ": r"\Gamma ", "Δ": r"\Delta ",
    "Θ": r"\Theta ", "Λ": r"\Lambda ", "Π": r"\Pi ", "Φ": r"\Phi ",
    "Ψ": r"\Psi ", "Ω": r"\Omega ", "∂": r"\partial ", "∇": r"\nabla ",
    "ℓ": r"\ell ", "ℝ": r"\mathbb{R} ",
}
SUPERS = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6",
          "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+", "ⁿ": "n"}
SUBS = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6",
        "₇": "7", "₈": "8", "₉": "9", "₊": "+", "₋": "-", "ₙ": "n", "ᵢ": "i", "ⱼ": "j"}

FUNCS = ("cosec", "csc", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh",
         "sin", "cos", "tan", "cot", "sec", "log", "ln", "lim", "max", "min",
         "det", "adj", "deg", "sqrt")

STOPWORDS = {"of", "if", "is", "in", "to", "at", "by", "on", "or", "an", "as",
             "be", "do", "it", "no", "so", "we", "he", "me", "my", "up", "us",
             "am", "the", "and", "for", "are", "its", "has", "was", "not", "but",
             "all", "any", "can", "get", "let", "find", "then", "than", "from",
             "with", "when", "which", "value", "sum", "number", "total"}

GREEK = set("αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΠΦΨΩ")
STRONG_CHARS = set("^_√∑∫∏≤≥≠∞∈→⇒·×÷±°") | GREEK | set("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺₀₁₂₃₄₅₆₇₈₉")
MATH_CHARS = (set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
              | set("+-*/^_=()[]{}|<>.,;:'\"!?%$&~@")
              | set(SYMBOLS) | set(SUPERS) | set(SUBS) | set("≈≡⊥∥∠′"))


# ----------------------------------------------------------------- span finding
def _balanced(s: str) -> bool:
    return s.count("(") == s.count(")") and s.count("[") == s.count("]")


def _is_func_word(word: str) -> bool:
    w = word.lower()
    return any(w.startswith(f) for f in FUNCS)


def _token_is_mathy(tok: str) -> bool:
    core = tok.strip(".,;:!?()[]{}\"'")
    if not core:
        return True                                   # pure punctuation, may join
    if not all(c in MATH_CHARS for c in core):
        return False
    letters = re.sub(r"[^A-Za-z]", "", core)
    if letters.lower() in STOPWORDS:
        return False
    if len(letters) <= 2:                             # x, ax, pq, m
        return True
    if _is_func_word(letters) and len(letters) <= 8:  # sin, cosx, sqrt
        return True
    return False


def _has_signal(txt: str) -> bool:
    if any(c in STRONG_CHARS for c in txt):
        return True
    if re.search(r"\d\s*/\s*\d", txt):
        return True
    if re.search(r"[A-Za-z0-9)\]}]\s*/\s*[A-Za-z0-9(\\{]", txt):
        return True
    if re.search(r"[A-Za-z0-9]{1,4}\s*=\s*[A-Za-z0-9(\\{-]", txt):
        return True
    return False


def find_math_spans(text: str) -> list[tuple[int, int, str]]:
    """Return [(start, end, raw_span)] for the maths-looking pieces of `text`."""
    spans = []
    tokens = [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", text)]
    i = 0
    while i < len(tokens):
        if not _token_is_mathy(tokens[i][2]):
            i += 1
            continue
        j = i
        group = []
        while j < len(tokens) and _token_is_mathy(tokens[j][2]):
            group.append(tokens[j])
            j += 1
        while group and not _balanced(text[group[0][0]:group[-1][1]]):
            group = group[:-1]                        # keep a balanced prefix
        if group:
            raw = text[group[0][0]:group[-1][1]]
            if _has_signal(raw):
                trimmed = raw.rstrip(".,;:!?")
                if trimmed:
                    spans.append((group[0][0], group[0][0] + len(trimmed), trimmed))
        i = j
    return spans


# ------------------------------------------------------------------ conversion
def _unicode_powers(s: str) -> str:
    s = re.sub("[" + "".join(SUPERS) + "]+",
               lambda m: "^{" + "".join(SUPERS[c] for c in m.group(0)) + "}", s)
    s = re.sub("[" + "".join(SUBS) + "]+",
               lambda m: "_{" + "".join(SUBS[c] for c in m.group(0)) + "}", s)
    return s


def _symbols(s: str) -> str:
    return "".join(SYMBOLS.get(c, c) for c in s)


def _balanced_arg(s: str, i: int) -> int | None:
    """Index just past the group starting at s[i] == '(' (balanced), or None."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "(":
            depth += 1
        elif s[j] == ")":
            depth -= 1
            if depth == 0:
                return j + 1
    return None


def _roots(s: str) -> str:
    """sqrt(…) or \\sqrt (…) -> \\sqrt{…}."""
    while True:
        m = re.search(r"(?<![A-Za-z\\])sqrt\s*\(", s)
        if not m:
            break
        end = _balanced_arg(s, m.end() - 1)
        if end is None:
            break
        s = s[:m.start()] + r"\sqrt{" + s[m.end():end - 1] + "}" + s[end:]
    while True:
        m = re.search(r"\\sqrt\s*\(", s)
        if not m:
            break
        end = _balanced_arg(s, m.end() - 1)
        if end is None:
            break
        s = s[:m.start()] + r"\sqrt{" + s[m.end():end - 1] + "}" + s[end:]
    return re.sub(r"\\sqrt\s*([A-Za-z0-9])", r"\\sqrt{\1}", s)


def _funcs(s: str) -> str:
    s = _roots(s)
    # funzione names, whole word (cosec before cos) or glued to its argument (sinx)
    for f in ("cosec", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh",
              "sin", "cos", "tan", "cot", "sec", "csc", "log", "ln", "lim",
              "max", "min"):
        s = re.sub(rf"(?<![A-Za-z\\]){f}(?=[\sA-Za-z0-9(]|$)",
                   lambda m, f=f: "\\" + f + " ", s, flags=re.I)
    return s


PLACE = "ZQP{}\x00"
def _protect(s: str):
    """Hide already-braced groups so fractions cannot eat across them."""
    store = []

    def repl(m):
        store.append(m.group(0))
        return f"ZQP{len(store) - 1}QZ"
    return re.sub(r"\{[^{}]*\}", repl, s), store


def _restore(s: str, store: list[str]) -> str:
    for i, val in enumerate(store):
        s = s.replace(f"ZQP{i}QZ", val)
    return s


def _fractions(s: str) -> str:
    """a/b -> \\frac{a}{b} (innermost first)."""
    atom = r"(?:\([^()]*\)|[A-Za-z0-9\.\^_\\]+)"
    pat = re.compile(rf"({atom})\s*/\s*({atom})")
    prev = None
    while prev != s:
        prev = s

        def repl(m):
            num, den = m.group(1), m.group(2)
            num = num[1:-1] if num.startswith("(") and num.endswith(")") else num
            den = den[1:-1] if den.startswith("(") and den.endswith(")") else den
            return r"\frac{" + num + "}{" + den + "}"
        s = pat.sub(repl, s)
    return s


def _exp_parens(s: str) -> str:
    """x^(1/5) -> x^{1/5} ; x_(n) -> x_{n}."""
    return re.sub(r"([\\A-Za-z0-9)\]\}])\s*([\^_])\s*\(([^()]*)\)",
                  lambda m: f"{m.group(1)}{m.group(2)}{{{m.group(3)}}}", s)


def _braces(s: str) -> str:
    """x^2 -> x^{2}, x^-6 -> x^{-6}, f_n -> f_{n}."""
    pat = re.compile(r"(\\[A-Za-z]+|[A-Za-z0-9)\]\}])([\^_])(?!\{)([+\-]?\d+|[A-Za-z])")
    prev = None
    while prev != s:
        prev = s
        s = pat.sub(lambda m: f"{m.group(1)}{m.group(2)}{{{m.group(3)}}}", s)
    return s


def _frac_in_braces(s: str) -> str:
    """{1/5} -> {\\frac{1}{5}} for simple cases."""
    return re.sub(r"\{([^{}/]{1,20})/([^{}/]{1,20})\}",
                  lambda m: r"{\frac{" + m.group(1).strip() + "}{" + m.group(2).strip() + "}}", s)


def _delims(s: str) -> str:
    if (r"\frac" in s or r"\sqrt" in s or "^{" in s) and _balanced(s) and "(" in s:
        s = s.replace("(", r"\left(").replace(")", r"\right)")
    return s


def _cleanup(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\{\s*\}", "", s)
    s = s.replace(" . ", r"\,\cdot\, ")
    s = re.sub(r"[\+\-\*/=_·]+$", "", s).strip()
    s = re.sub(r"^[\*/^_·]+", "", s).strip()
    return s.strip()


def to_latex(raw: str) -> str | None:
    """Convert an OCR maths span to LaTeX; None when not confident."""
    s = raw.strip()
    if not s or not _has_signal(s):
        return None
    s = _unicode_powers(s)
    s = _symbols(s)
    s = _funcs(s)
    s, store = _protect(s)          # hide {..} groups from the fraction pass
    s = _fractions(s)
    s = _restore(s, store)
    s = _exp_parens(s)
    s = _braces(s)
    s = _frac_in_braces(s)
    s = _delims(s)
    s = _cleanup(s)

    # ---- rejection / sanitising -----------------------------------------
    if not s or s == raw:
        return None
    s = s.replace(r"\cosec", r"\operatorname{cosec}")
    s = re.sub(r"\s*&\s*", " ", s)                       # OCR column marks
    if s.count(r"\left(") != s.count(r"\right)"):        # unbalanced \left … \right
        s = s.replace(r"\left(", "(").replace(r"\right)", ")")
    for w in re.findall(r"[A-Za-z]{3,}", re.sub(r"\\[A-Za-z]+", " ", s)):
        if w.lower() not in FUNCS:
            return None
    if s.count("{") != s.count("}") or s.count(r"\left(") != s.count(r"\right)"):
        return None
    if len(s) > 400:
        return None
    return s


def segments(text: str) -> list[tuple[str, str]]:
    """Split text into [('text', s) | ('math', latex)] preserving order."""
    out, pos = [], 0
    for start, end, raw in find_math_spans(text):
        latex = to_latex(raw)
        if latex is None:
            continue
        if start > pos:
            out.append(("text", text[pos:start]))
        out.append(("math", latex))
        pos = end
    if pos < len(text):
        out.append(("text", text[pos:]))
    return out or [("text", text)]


if __name__ == "__main__":
    tests = [
        "(x^m + 1/x^2)^22",
        "(4x/5 + 5/(2x^2))^9",
        "x^-6",
        "(sqrt(a)x^2 + 1/(2x^3))^10",
        "sinx + cosx = 1",
        "cosec x - cosec 2x = cosec 4x",
        "x² - 5x + 6 = 0",
        "√(1-sinx+√(1+sinx))",
        "(2x^(1/5) - 1/(x^(1/5)))^15",
        "xyz = 2^8 . 3^5 . 5^4",
        "The natural number m, for which the coefficient of x in the binomial expansion of (x^m + 1/x^2)^22 is 1540, is ______",
    ]
    for t in tests:
        print("IN :", t)
        for kind, val in segments(t):
            print(f"   [{kind}] {val}")
        print()
