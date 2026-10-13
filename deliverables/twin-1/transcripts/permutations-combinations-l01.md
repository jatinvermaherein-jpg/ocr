# Permutations & Combinations — Lecture 01 (Class Notes) · Twin 1 transcript
Source: `Permutations & Combinations 01 Class Notes.pdf` (46 pages, image-only, no text layer). Renders: `work/pages/pc01_pNN.png`. Page keys are PDF page numbers; the printed `Page No.` label, when present, is quoted in the header line. Math in ASCII per F-19.

> Note on order: this lecture was transcribed back-to-front (p46 down to p01) to avoid colliding with the parallel twin working forward through the deck; the sections have now been re-sorted into ascending PDF page order (p01 → p46).

---

---

<a id="p01"></a>
## p01 · course cover · label: Cover

- **P:** printed course artwork — huge gold block letters `ARJUNA` with a fletched arrow piercing the final letter, white block `JEE 2027` below; a black band `Lecture – 01` | `Mathematics`; a yellow banner `PERMUTATIONS` / `AND` / `COMBINATIONS`; a dark red band `By- Sachin Jakhar Sir`. Right: the instructor in a black `Physics Wallah` polo with a three-finger salute, wrist watch and beads; bottom-left a printed protractor, set-square and pencil; background circuit-board graphics and candles. `PW` shield logo top-right.
- **H:** none.
- **DIBY:** —
- **U:** 0
- **Note:** cover slides carry no teaching content; recorded for completeness (same treatment as the other four decks' p01).

---

<a id="p02"></a>
## p02 · Topics to be covered · label: Agenda

- **P:** printed title `Topics` [yellow block] `to be covered` [white script]. Four rows, each a red rounded tile with a white letter: `A` + printed white `Graphical Transformation` inside a printed red rectangle; `B` + `Fundamental Principle of Counting` inside a printed red rectangle; `C` + `Question Practice`; `D` + (no text). Right half: printed 3-D cartoon pencil with a face, an eraser-cap and a moustache, leaning on a giant silver question mark.
- **H:** none — pure print. The two boxed items A and B are the deck's two topics, and they match the order in which the lecture runs (transformations p04–p29, counting p30 onward); row `D` is left blank by the design.
- **DIBY:** —
- **U:** 0

---

<a id="p03"></a>
## p03 · H.W. Discussion · label: Divider

- **P:** black slide, printed white title `H.W. Discussion` boxed by a printed red rectangle at centre.
- **H:** none.
- **DIBY:** —
- **U:** 0
- **Note:** marks the boundary where the lecture switches from the new topic to homework being read back — the pages above it (p01–p02) are the closing homework slides.

---

<a id="p04"></a>
## p04 · Proof that cosθ + cos(120°+θ) + cos(240°+θ) = 0 · label: board

- **P:** `Acidic Question` chip (no page-number band). Printed stem identical to p05: `If cos³θ + cos³(120° + θ) + cos³(240° + θ) = (a/b)cos3θ, where 'a' and 'b' are relative prime, then the value a + b is`.
- **H:** pink first line `M = cosθ + cos(120° + θ) + cos(240° + θ) = 0`, with two cyan arc marks and cyan letters `A` and `B` above it (labelling the two compound angles). Two curved orange arrows drop from `cosθ` and `cos(120° + θ)` into the orange expansion `M = cosθ - (1/2)cosθ - (√3/2)sinθ - (1/2)cosθ + (√3/2)sinθ` — every one of the five terms struck through with a white diagonal line — and below that, white `= 0.` Right column, cyan, the four values used: `cos120° = -1/2`, `sin120° = +√3/2`, `cos240° = -1/2`, `sin240° = -√3/2`.
- **DIBY:** —
- **U:** 0

---

<a id="p05"></a>
## p05 · Acidic Question: cos³ sum = (a/b)cos3θ · label: Question

- **P:** `Acidic Question` chip (no page-number band). Stem: `If` [white] `cos³θ + cos³(120° + θ) + cos³(240° + θ) = (a/b)cos3θ` [green, `a` over `b` as a stacked fraction] `, where 'a' and 'b' are relative prime, then the value` [white] `a + b` [cyan] `is` [white].
- **H:** white throughout. Above `(120° + θ)` the annotation `180° + θ - 60°` with a wavy underline beneath the annotation; above `(240° + θ)` the annotation `180° + 60° + θ`, likewise wavy-underlined. A white arrow runs from the stem to a white **circle enclosing a crossed digit** at mid-page, read as `7` (= a + b = 3 + 4); next to the circle the cursive `fnf`. A long curved white arrow drops from `relative prime, then` to the identity line `x³ + y³ + z³ = 3xyz`; right of it `x + y + z = 0`; between them the small annotation `60° - θ` with an up-arrow into the next line. The application line reads `= 3cosθ (cos(θ - 60°)) (cos(60° + θ))` — each bracket preceded by a small tick mark rather than a sign — and the last line `= (3/4)cos3θ`.
- **DIBY:** —
- **U:** 2 — (i) the circled digit is crossed in the same way the hand writes `4` elsewhere (F-08), so it could be re-read as `4`; the arithmetic of the printed question (`a = 3, b = 4`) points to `7`, so `7` is transcribed; (ii) the cursive `fnf` gloss ("total/therefore", U-02) appears a ninth time and stays unexpanded.
- **Note:** this is the same printed question as p04 — p04 proves the cosine sum is `0` (so `x + y + z = 0` holds) and p05 finishes with `3xyz = (3/4)cos3θ`.

---

<a id="p06"></a>
## p06 · Q: (a + b)^100 + (a - b)^100 · label: Question

- **P:** `Question` chip (no page-number band). Stem: `The sum of the coefficients of the` [white] `x` [pink] `-free and` [white] `x` [pink] `-dependent terms in the expansion of` [white] `(a + b)^100 + (a - b)^100` [green] `, (where` [white] `a = √x` [green] `and` [white] `b = 1` [green] `), are` [white] `k1` [cyan] `and` [white] `k2` [cyan] `respectively, then:`. Four printed options: `(A)` [white] `k1 = 2^99 , k2 = 2^99` [green], `(B)` `k1 = 2^100 , k2 = 2^99`, `(C)` `k1 = 2^100 , k2 = 0`, `(D)` `k1 = 0 , k2 = 2^100`.
- **H:** cyan marks on the right, made before the options were settled — a large opening curly brace spanning three lines, then three stacked `≡` symbols with a horizontal stroke under them (the writer's shorthand for the odd/even cancellation: adding the two binomial expansions keeps only the even-`b` terms, i.e. `2 · Σ C(100,2r) a^(100-2r) b^(2r)`), and below that a second cyan `≡` with a wavy double stroke. A cyan tick is struck through the option `(A)` label — **A** is the chosen answer, `k1 = 2^99, k2 = 2^99`.
- **DIBY:** —
- **U:** 1 — the cyan marks are equivalence glyphs rather than letters; read as the cancellation shorthand, not as text.

---

<a id="p07"></a>
## p07 · Acidic Question: trig sum at α = π/5 · label: Question

- **P:** `Acidic Question` chip (no page-number band). Stem: `The value of the expression` [white] followed by the printed green fraction `(sin7α + 6sin5α + 17sin3α + 12sinα) / (sin6α + 5sin4α + 12sin2α)`, then `, where` [white] `α = π/5` [cyan] `is equal to` [white]. Four option tiles down the left, each a red rounded square with a white letter beside a printed white fraction: `A` `(√5 - 1)/4`, `B` `(√5 + 1)/4`, `C` `(√5 + 1)/2`, `D` `(√5 - 1)/2`.
- **H:** a white curved arrow from the fraction down-left to a white line `N =` [sin7α + sin5α] `+` [5 sin5α + 5 sin3α] `+` [12 sin3α + 12 sinα] — the three groups each boxed in red, cyan arcs drawn over `5 sin5α` and `5 sin3α` to mark the pairing; a yellow curved arrow from the first box down to a yellow line `2 sin6α cosα + 5(2 sin4α cosα) + 12(2 sin2α cosα)` with a yellow arc linking `sin6α` and `sin4α`; the bracketed factor `(sin6α + 5sin4α + 12sin2α)` boxed in red with a cyan arrow to a cyan `D`, i.e. `N = 2cosα (sin6α + 5sin4α + 12sin2α)`; below, cyan `N/D = 2cosα`; and top right, cyan `2cos36° = 2( (√5 + 1)/4 )`. A cyan tick is struck through the option `C` tile — **C** is the chosen answer, `(√5 + 1)/2`.
- **DIBY:** —
- **U:** 0
- **Note:** the writer splits the coefficients `6 = 1 + 5`, `17 = 1 + 5 + 12` so each pair reduces by sum-to-product and reproduces the denominator; the hand values `2cos36° = (√5+1)/2` agrees with the printed option C.

---

<a id="p08"></a>
## p08 · Q (JEE Adv. 2011): 1/sin(π/n) = 1/sin(2π/n) + 1/sin(3π/n) · label: Question

- **P:** pink `Page No.60` top-right. `Question [JEE (Adv.)-2011]` chip. Stem: `The positive integer value of` [white] `n > 3` [white/italic] `satisfying the equation` [white], then the printed display equation `1/sin(π/n) = 1/sin(2π/n) + 1/sin(3π/n)` (numerators `1` in green; each `sin(...)` in green with the `n` in red) and `is` [white].
- **H:** a cyan hand-drawn circle enclosing a cursive `H.W.` with a double underline and a dot — the question is **assigned as homework**; no working is written on this page.
- **DIBY:** —
- **U:** 1 — the tag is cursive and could be re-read as another abbreviation; bracketed as homework on the strength of the circle + underline convention seen throughout (F-18, F-20).

---

<a id="p09"></a>
## p09 · Graphical transformation toolkit · label: Rule

- **P:** `GRAPHICAL TRANSFORMATION` banner (clip-board tile). Body: `# If graph of` [green] `y = f(x)` [yellow] `is known then :` [green]. `We can draw graph of` [white] `⇒` then three right-hand lines — `|f(x)|, f(|x|), -f(x), f(-x)` [yellow], `f(x) ± k, f(x ± k), kf(x), f(kx)` [cyan], `|y| = f(x)` [cyan].
- **H:** none — pure print.
- **DIBY:** —
- **U:** 0
- **Note:** the nine transformations listed here are the table of contents for the rest of the lecture: T-VI (p14), the `f(-x ± k)` rule (p17), `y = f(kx)` (p21), `y = f(|x|)` (p28), `|y| = f(x)` (p26 Example 4 and p25 board).

---

<a id="p10"></a>
## p10 · RAPID FIRE ROUND: five graphs of f · label: Exercise

- **P:** `RAPID FIRE ROUND` chip. Left column: `Draw the graphs of:` [white] then five items, labels white and expressions green — `(i) y = |f(x)|`, `(ii) y = f(|x|)`, `(iii) y = |f(|x|)|`, `(iv) y = -f(x)`, `(v) y = f(-|x|)`. Right: printed white graph of `f(x)` on labelled axes — `y` at top, `f(x)` beside it, `x` at right; `O` at the origin, `x` ticks `0` (below `O`), `1`, `2`, `4`, `-1` on the left; `y` ticks `2`, `1`, `-1` with dashed guide lines. The printed curve: rises from `(-1, -1)` to the origin, arches up to a maximum of `1` between `0` and `1`, drops to `0` at `1`, climbs in a concave-up sweep to the corner `(2, 2)`, then falls in a quarter-arc to `4` on the axis.
- **H:** cyan ticks struck through `(i)`, `(ii)`, `(iii)`, `(iv)` and an orange tick through `(v)` — all five assigned; a cyan brace from `(ii)` and `(iii)` to a cyan `"same"` (double-underlined) — those two graphs coincide because `f(|x|)` is already non-negative here; a curved orange arrow from `(v)` down to a small orange sketch — axes with `x` ticks `-1`, `O`, `1`, a curve that peaks at the origin and falls away to the left and right, and a dashed horizontal line below the axis.
- **DIBY:** —
- **U:** 0

---

<a id="p11"></a>
## p11 · Note: f(x) → f(-x) → f(-|x|) · label: Note

- **P:** a panel ringed by a chain of printed gold stars. Inside, top-left: `Note :` [orange, underlined]. Centred inside a printed red rectangle, an orange vertical chain of three lines joined by two printed down-arrows: `y = f(x)` → `y = f(-x)` → `y = f(-|x|)`.
- **H:** none — the whole chain is printed.
- **DIBY:** —
- **U:** 0
- **Note:** this is the printed rule that the questions on p12–p13 test; the star ring is a decoration (cf. F-35 on the `RAR` badge).

---

<a id="p12"></a>
## p12 · Q: which function matches the graph · label: Question

- **P:** `Question` chip (no page-number band). Stem: `Which function corresponds to the given graph?`. Options in one row: `(A)` [white] `y = |sinx|` [cyan], `(B)` `y = sin|x|`, `(C)` `y = -|sinx|`, `(D)` `y = -sin|x|`. Printed yellow curve on white axes below-left: hump above the axis on `[-2π, -π]`, trough on `[-π, 0]`, trough on `[0, π]`, hump on `[π, 2π]`; `x`-axis ticks `-2π`, `-π`, `O`, `π`, `2π`, `y`-axis ticks `1`, `-1`.
- **H:** a pink tick struck through the `(D)` label — option **D** marked (the graph is even and negative just right of the origin, i.e. `y = -sin|x|`).
- **DIBY:** —
- **U:** 0

---

<a id="p13"></a>
## p13 · Q: graph of y = f(-|x|) · label: Question

- **P:** `Question` chip (no page-number band). Stem: `The graph of` [white] `y = f(x)` [green] `is shown in figure : Which of the following best represent the graph of` [white] `y = f(-|x|)` [cyan] `?`. Printed cyan figure top-right: a straight line rising from the lower left to a cusp on the positive `y`-axis, then a parabolic dip below the axis to the right, rising again past `x`; axes marked `O`, `x`, `y`. Options — `(A)` line rising to a cusp then a dip with a small arch above the axis; `(B)` two mirror-image dips with a cusp at the origin; `(C)` two outer dips and two small arches, symmetric about the `y`-axis; `(D)` a single triangular peak at the positive `y`-axis with straight lines falling away on both sides.
- **H:** a pink tick struck through the `(D)` option label — the option **D** is the one marked; a short pink dash floats at mid-height left of the figure (start of a stroke, not a glyph).
- **DIBY:** —
- **U:** 0
- **Note:** consistent with the rule on p11: `f(-|x|)` keeps the *left* branch and mirrors it, which is the triangular figure (D).

---

<a id="p14"></a>
## p14 · T-VI · label: Rule

- **P:** `GRAPHICAL TRANSFORMATION` banner (clip-board tile). Body: `# T-VI :` [green] `To Draw` [yellow] `y = f(x ± k)` [cyan] — i.e. `y = f(x ± k)`. `For` [white] `f(x + k)` [yellow] `: Shift whole graph by 'k' units in left direction (along X-axis)` [white], with a long printed red arrow above pointing **left**; `For` [white] `f(x - k)` [yellow] `: Shift whole graph by 'k' units in right direction (along X-axis)` [white], with a long printed red arrow below pointing **right**.
- **H:** none — pure print.
- **DIBY:** —
- **U:** 0

---

<a id="p15"></a>
## p15 · sin shifted by ±π/2 · label: board

- **P:** — (no header, board slide)
- **H:** left — pink `# y = sin(x)` above a yellow sine wave drawn on red axes. Top right — yellow `y = sin(x + π/2) = cos x` above a yellow wave on red axes (peaking at the y-axis); bottom right — yellow `y = sin(x - π/2) = -sin(π/2 - x) = -cos x` above a yellow wave on red axes (trough at the y-axis). Each shifted wave is linked to its own red vertical axis arrow.
- **DIBY:** —
- **U:** 0

---

<a id="p16"></a>
## p16 · y = x² shifted by 1 and by −2 · label: board

- **P:** — (no header, board slide)
- **H:** centre — yellow `y = x^2` above a yellow upward parabola drawn on yellow axes through the origin. To its right a yellow `y = (x-1)^2` above a magenta parabola tangent to the axis on the right, its vertex marked with a cyan tick labelled `1`; to the left a yellow `y = (x+2)^2` above a yellow parabola whose vertex is marked with a cyan tick labelled `-2`. Two cyan curved arrows run out of the central parabola to each shifted copy.
- **DIBY:** —
- **U:** 0

---

<a id="p17"></a>
## p17 · horizontal shift of the reflected graph · label: Rule

- **P:** `GRAPHICAL TRANSFORMATION` banner (clip-board tile). Body: `# To Draw` [white] `y = f(-x ± k)` [yellow] — i.e. `y = f(-x ± k)`. `For` [white] `f(-x + k)` [yellow] `: Shift whole graph by 'k' units in right direction (along X-axis)` [white], with a long printed red arrow above pointing **right**; `For` [white] `f(-x - k)` [yellow] `: Shift whole graph by 'k' units in left direction (along X-axis)` [white], with a long printed red arrow below pointing **left**.
- **H:** none — this page is pure print.
- **DIBY:** —
- **U:** 0
- **Note:** the two rules are stated as the *reflected* graph shifted the opposite way from the usual `f(x ± k)` rule on p14 (here `+k` → right, `−k` → left), because the reflection in `f(-x)` reverses the axis.

---

<a id="p18"></a>
## p18 · board — sin(-x), sin(-x + pi/2), sin(-x - pi/2) · label: — (no header, board slide)
**P:** none — board page.
**H:** three hand plots on red axes with arrowheads and yellow sine-type curves: at the left pink `# y = sin(-x)` over the reversed sine; at the upper right yellow `y = sin(-x + pi/2) = cos x` over a curve that is at its maximum at x = 0; at the lower centre yellow `y = sin(-x - pi/2) = -cos x` over the curve that is at its minimum at x = 0. No x or y labels are written on any of the three axes.
**DIBY:** none. **U:** none — the identities are correct as written (sin(−x + π/2) = cos x, sin(−x − π/2) = −cos x).

---

<a id="p19"></a>
## p19 · GRAPHICAL TRANSFORMATION — T-VII: y = k f(x) · label: — (no label)
**P:** clipboard icon + red banner **GRAPHICAL TRANSFORMATION**; green `# T-VII :` yellow **To Draw** cyan `y = kf(x)` yellow `, (k > 0)`; white **Multiply every number on Y-axis by 'k'.**; yellow **As a result :** white `If k > 1, graph will stretch along Y-axis.` and `If 0 < k < 1, graph will compress along Y-axis.`
**H:** none. **DIBY:** none. **U:** none.

---

<a id="p20"></a>
## p20 · Example — 2 sin x, sin x, (1/2) sin x on one grid (amplitude change) · label: — (no label)
**P:** red chip **Example**; a white graph-paper strip (Desmos-style) with printed axes, no printed formula.
**H:** three curves — blue `y = 2 sin x` (label in blue at the upper right with a blue arrow), red `y = sin x` (red label with a red arrow) and green `y = 1/2 sin x` (green label below the axis with a curly green arrow); hand-coloured y-ticks `1` in red and `1/2` in green on the y-axis, printed ticks `2` and `-2`, x-ticks `-6, -4, -2, 0, 2, 4, 6`.
**DIBY:** none. **U:** none — this is the illustration for T-VII (p19), the amplitude rule.

---

<a id="p21"></a>
## p21 · GRAPHICAL TRANSFORMATION — T-VIII: y = f(kx) · label: — (no label)
**P:** clipboard icon + red banner **GRAPHICAL TRANSFORMATION**; green `# T-VIII :` yellow **To Draw** cyan `y = f(kx)` yellow `, (k > 0)`; white **Divide every number on X-axis by 'k'.**; yellow **As a result :** white `If k > 1, graph will compress along X-axis.` and `If 0 < k < 1, graph will stretch along X-axis.`
**H:** none. **DIBY:** none. **U:** none — the worked example for this rule is p22 (same slide family), and the printed page carries no label here although p20/p24 of this deck do.

---

<a id="p22"></a>
## p22 · Example — sin(2x), sin x, sin(x/2) on one grid (period change) · label: — (no label)
**P:** red chip **Example**; the body of the slide is a white graph-paper strip (a Desmos-style export) with a plain x-axis, no printed formula.
**H:** three curves on the strip — blue `y = sin(2x)`, red `y = sin x`, green `y = sin(x/2)` — with hand arrows from each coloured label to its curve (the green label written at the top right as `y = sin(1/2 x)` with a green arrow, the blue label below the axis with a blue arrow, the red label at the right with a red curl); printed x-ticks `−6, −4, −2, 0, 2, 4, 6` and a heavy vertical rule at the origin.
**DIBY:** none. **U:** none.

---

<a id="p23"></a>
## p23 · Example — draw y = sin(pi x) · label: — (no label)
**P:** red chip **Example**; **Draw :** cyan `y = sin(pi x)`.
**H:** a hand-drawn plot filling the slide: red axes with arrowheads and a green dot at the origin, an orange sine curve of period 2 crossing the axis at every integer (small orange crosses at `−2`, `−1`, `1`, `2`), orange x-labels `−2, −3/2, −1, −1/2, 0, 1/2, 1, 3/2, 2` (the half-integers written as stacked fractions).
**DIBY:** none. **U:** none — the printed rule this illustrates is T-VIII (p21); the curve is drawn from scratch rather than by dividing the axis.

---

<a id="p24"></a>
## p24 · GRAPHICAL TRANSFORMATION — T-IX: to draw |y| = f(x) · label: — (no label)
**P:** clipboard icon + red banner **GRAPHICAL TRANSFORMATION**; `# T-IX : To Draw |y| = f(x)` (green `T-IX`, yellow `To Draw`, cyan formula); white rule **Remove part of the graph below X-axis, now take image of portion above X-axis in X-axis & keep both.**
**H:** two green sketches — at the left `y = f(x)` drawn as an upward parabola cutting the axis twice with a hand-drawn arrow up the y-axis; at the right `|y| = f(x)`, the same curve keeping only the parts at or above the axis together with their mirror images below it (the two lower branches).
**DIBY:** none. **U:** 1 — the rule as printed is loose ("remove the part below the X-axis" then "keep both"): it describes reflecting the *upper* part downward while retaining it, which is what the sketch shows, but the wording could be read as deleting the lower part of f(x) first; kept verbatim.

---

<a id="p25"></a>
## p25 · board — |y| = sin x, the lens construction · label: — (no header, board slide)
**P:** none — board page (illustration of the rule on p24).
**H:** pink `# |y| = sin x`; red axes with arrowheads; orange curve drawn as two closed "lens" shapes sitting symmetrically about the x-axis — one between `0` and `pi`, one between `-2pi` and `-pi` (the only intervals where sin x is non-negative), with orange dots at `0`, `pi`, `-pi`, `-2pi` and those labels written in orange below the axis.
**DIBY:** none. **U:** none — no `pi`-labelled hump is drawn between `-pi` and `0`, consistent with |y| requiring sin x >= 0.

---

<a id="p26"></a>
## p26 · Example — six graphs by multiple transformation (H.W.) · label: — (no label)
**P:** red chip **Example**; **Draw following graphs using multiple transformation:** cyan `(i) y = |ln|x||`, `(ii) y = |||x| - 2| - 3|`, `(iii) y = e^(-|x|) + 2`, `(iv) y = -{-x}`, `(v) |y| = 3 + sqrt(2 - x)`, `(vi) y = |x^2 - 5|x| + 6|`.
**H:** an orange cursive `H.W.` with dots and a double underline at the lower right of the list; nothing drawn on this page.
**DIBY:** none (H.W. only, F-18). **U:** none — all six graphs are worked through on P&C L02 p06-p10, which carries the same printed slide with the sketches.

---

<a id="p27"></a>
## p27 · Question — number of solutions of |f(|x|)| = 2 from a printed graph (H.W.) · label: — (no label)
**P:** red chip **Question**; **If graph of a function f(x) is shown as following then number of solutions of equation |f(|x|)| = 2 is equal to**; red tiles **A** 3, **B** 6, **C** 10, **D** Infinite. The printed white figure at the right: a curve rising linearly from `x = -1` (dashed drop to the axis) to a peak `3` on the y-axis, falling to `0` at `x = 1`, curling up to a sharp spike just before `2`, plunging through `3` down to `-3` near `3.5` and returning up towards the axis; dotted rules at the levels `3` and `-3`, axis ticks `-1, 0, 1, 2, 3, 4`, y-ticks `3, 2, -3`.
**H:** an orange cursive `H.W.` with two dots and a double dash to the left of the figure — the question is assigned, no construction drawn on this slide.
**DIBY:** none (H.W. only). **U:** none — the same question is fully graphed and answered (C, 10) two lectures later at P&C L02 p11; cross-referenced there.

---

<a id="p28"></a>
## p28 · Question — number of solutions of |x^2 - |x|| = ln|x| (H.W.) · label: — (no label)
**P:** red chip **Question**; **Number of solutions of equation |x^2 - |x|| = ln|x| is equal to** (the equation in cyan).
**H:** an orange circle enclosing the cursive `H.W.` over a double underline with two small rings — the item is assigned, nothing solved on this slide.
**DIBY:** none (H.W. only, F-18). **U:** none — this is the same question that P&C L02 p12 works through graphically (with the ringed `2` and a `fnf` mark), so the two decks cross-reference: assigned in L01, solved in L02.

---

<a id="p29"></a>
## p29 · # P&C # PERMUTATIONS & COMBINATIONS (topic header, star-framed) · label: — (no label)
**P:** centred white bold **PERMUTATIONS & COMBINATIONS** inside a thin red rectangle, with an orange handwritten `# P&C #` above it and the whole block ringed by roughly ninety gold star stickers.
**H:** pink arrow from the box's left edge down to pink `1 Ques.` branching into `Mains` and `Adv.`; a red rectangle holding pink `Probability` with a pink bracket down to `XII`; green arrows from the box's right edge to green `Sochne wala (Case Making)` and green `Independent`.
**DIBY:** none. **U:** none — the star frame is used here as emphasis for the chapter title, the same device as the boxed coefficient rules in BT L09 p18.

---

<a id="p30"></a>
## p30 · FUNDAMENTAL PRINCIPLE OF COUNTING — multiplication (AND) and addition (OR) · label: **Page No.125**
**P:** clipboard icon + red banner **FUNDAMENTAL PRINCIPLE OF COUNTING**; cyan `# Multiplication Principle: (AND)` over white Hinglish **Jab tak process complete na ho tab tk number of ways ko multiply kte rho.**; cyan `# Addition Principle: (OR)` over white **Agr given process 'm' tarike se complete ho gya hai & ussi process ko complete krne ke 'n' aur tarike hain, to total ways =**.
**H:** a cyan `Process` label with a two-headed arrow above a red rectangle of four cells `m | n | p | t` separated by orange strokes, an orange arrow to orange `Total = m x n x p x t` (the letters coloured per cell); orange `OR options` at the right; in the addition half, two red rectangles `n-ways` and `m-ways` with a cyan `OR` at their left and a cyan brace whose arrow curves up to the cyan handwriting `(m+n) ways` that completes the printed sentence.
**DIBY:** none. **U:** none — the Hinglish is transcribed verbatim, including `kte`, `krne`, `gya`.

---

<a id="p31"></a>
## p31 · Question (same slide, earlier reveal) — the three lists before the table · label: **Page No.125**
**P:** identical printed question to p32.
**H:** green lists only — `Shirt -> S1  S2  S3`, `Jeans -> J1  J2`, `Belt -> B1  B2  B3  B4` — the same yellow flexing-boy cartoon, and the same cyan summary `Shirt -> 3 / Jeans -> 2 / Belt -> 4` over a rule with the cursive `fnf = 3 x 2 x 4 = 24 ways`. The product table of p32 is not yet drawn, so this page is transcribed as the earlier state of that slide rather than as new content (F-16 handling).
**DIBY:** none. **U:** none.

---

<a id="p32"></a>
## p32 · Question — Golu's shirts/jeans/belts: the full product table · label: **Page No.125**
**P:** red chip **Question**; **Let a person "Little Golu" has 3 different shirts, 2 different Jeans & 4 different belts. Then find number of ways of getting ready.** (`3 different shirts`, `2 different Jeans`, `4 different belts` in yellow, `Little Golu` green).
**H:** a cyan three-column table headed `Shirt | Jean | Belt` filled in pink with `S1 S1 S1 S1 S1 S1 S1 S2` against `J1 J1 J1 J1 J2 J2 J2 J2` against `B1 B2 B3 B4 B1 B2 B3 B4`, the columns trailing into vertical dots; at the right a yellow cartoon of a flexing boy; cyan `Shirt -> 3`, `Jeans -> 2`, `Belt -> 4` over a cyan rule, then the cursive `fnf` in cyan `= 3 x 2 x 4` and `= 24 ways`.
**DIBY:** none. **U:** none — p31 and p32 are the same printed slide at successive reveals (see the delta note on p31).

---

<a id="p33"></a>
## p33 · Question — Golu's kurta/pajama vs T-shirt/jeans outfit count · label: — (no label)
**P:** red chip **Question**; **Consider 3 different Kurtas, 2 different Pajamas, 4 different T-Shirts & 3 different Jeans.** (all counts in yellow) **In how many ways can little Golu dress up for an event either fully ethnic or fully casual.** (`little Golu` green).
**H:** pink `Ethnic.` beside an orange `3 x 2` inside a red rectangle, with `K` and `P` written above the two factors and dashes into them, then an orange arrow to orange `6 ways`; below, pink `Casual.` beside an orange `4 x 3` in a second red rectangle with `T` and `J` written under the factors and arrows up into them, arrow to orange `12 ways`; two long orange arcs carry both results to the right, where an orange circle reads `add` and the cursive `fnf` mark opens `= 12 + 6 = 18 ways`.
**DIBY:** none. **U:** none — another sighting of the cursive `fnf` glyph (here standing where "total" would go), consistent with F-34/U-02.

---

<a id="p34"></a>
## p34 · Question — 7 flags, signals with 2 flags one above the other · label: **Page No.125**
**P:** red chip **Question**; **There are 7 flags of different colour. Find the number of different signals that can be transmitted by the use of 2 flags one above the other.** (`7 flags` yellow).
**H:** a cyan two-row box `P-1 | 7 optn` over `P-2 | 6 optn` with cyan `Total = 7 x 6 = 42` below; at the right an orange enumeration grid, two blocks of six columns — the first headed `G G G G G G` over `B  BL.  W  Y  O  P`, the second headed `B B B B B B` over `G  BL.  W  Y.  O  P` — the colours abbreviated green, blue, black, white, yellow, orange, pink.
**DIBY:** none. **U:** none — only twelve of the 42 ordered pairs are written out; the rest are implied by the pattern.

---

<a id="p35"></a>
## p35 · Question — JEE-Adv Section-B, six multiple-correct questions · label: **Page No.125**
**P:** red chip **Question**; **Section-B of JEE-Adv. contains six multiple choice questions in which one or more than one options can be correct. Find total number of ways to attempt these 6 questions:** cyan `(i) Each question should be answered.`, `(ii) One can leave the question unattempted.`
**H:** yellow arc from (i) to the row `Q1. Q2 Q3 Q4 Q5 Q6`, each with a `15` under a smiley arc, then an arrow to yellow `Total = (15)^6`; a second yellow arc from (ii) to yellow `(16)^6`.
**DIBY:** none. **U:** none — 15 = the non-empty subsets of four options, 16 = the same plus "not attempted" (p36).

---

<a id="p36"></a>
## p36 · board — one multiple-correct question has 16 ways to answer · label: — (no header, board slide)
**P:** none — board page.
**H:** orange at the top `1 Ques.` over `Multiple Correct`; pink `Q1.` with four option bubbles `O A  O B  O C  O D`; under each bubble a cyan `2 opt.` and cyan `2 opt. x 2 opt. x 2 opt. x 2 opt. = (16) ways` with `16` ringed in cyan; a fan of yellow arrows on the right listing all sixteen possibilities in yellow: `not-attempted`, `A`, `B`, `C`, `D`, `AB, AC, AD`, `BC, BD, CD`, `ABC, ACD, ABD, BCD`, `ABCD`.
**DIBY:** none. **U:** none.

---

<a id="p37"></a>
## p37 · board — Section-B, one question at a time: 16 ways each, cases drawn out · label: — (no header, board slide)
**P:** none — board page continuing p35/p36.
**H:** yellow heading `Sec-B`; a yellow row `Q1 Q2 Q3` with a `16` written under each and an arrow to yellow `(16)^3`; below it the pink case enumeration — `A A` with a long pink brace listing the per-question options (`A B C D AB ...`) and pink `16 ways`; `A B` with a second brace and pink `16 ways`; to the right two further cases, `A C` and `A —` (unattempted), each with its own brace and pink `16 ways`.
**DIBY:** none. **U:** 1 — the four case heads are written as pairs of letters (`A A`, `A B`, `A C`, `A —`) with no label saying what they condition on; read as "the answer to Q1 fixed, then to Q2", which the printed deck never states.

---

<a id="p38"></a>
## p38 · Question — 10 True/False questions, attempt counts · label: — (no label)
**P:** red chip **Question**; **Question Paper containing 10 True/False Questions, number of ways to attempt question paper such that:** cyan `(i) No Restriction`, `(ii) All Questions should be answered.` (`10 True/False` yellow).
**H:** a yellow tick through `(i)`; yellow `=> 3^10` after (i) and yellow `=> 2^10` after (ii) (both handwritten, not printed); below, the yellow row `Q1 Q2 . . . Q10` with a smiley arc under `Q1` and an arrow down to a yellow `3` branching into `T  f  UA` (true / false / unattempted).
**DIBY:** none. **U:** none — the slide counts "attempt" as choosing T, F or leaving blank, hence 3^10 in (i).

---

<a id="p39"></a>
## p39 · Question — letter lock, 3 rings, unsuccessful attempts · label: — (no label)
**P:** red chip **Question**; **A letter lock consists of 3 rings each marked with 10 different letters. In how many ways, its is possible to make an unsuccessful attempt to open the lock?** (`3 rings` yellow; "its is" printed as it stands).
**H:** a yellow sketch of the three nested rings numbered `1`, `2`, `3` with a yellow arrow into them and three arrows down to yellow `10 x 10 x 10`; then yellow `Total = 10^3` splitting into two branches, upper `1 correct` and lower a red rectangle holding `999 incorrect` with a yellow tick beside it.
**DIBY:** none. **U:** none.

---

<a id="p40"></a>
## p40 · Question [hand-made MCQ] — 6 marbles into 3 pockets · label: **Page No.125**
**P:** red chip **Question**; **A boy has 6 marbles, number of ways in which he can put these marbles in 3 pockets.** (`6 marbles` yellow, `3 pockets` green).
**H:** green `6 x 5 x 4` above three pink pocket sketches `P1 P2 P3`, each with green marble ovals below (`M3 M5`, `M4`, `M1 M2 M6`) and green `1 way` arrows, plus a second grouping row (`M1 M2 M3` / `M4 M5 M6`) also labelled `1 way` — the wrong product is illustrated and then rejected; at the right five cyan circled bubbles with letters beneath, `E (120)` struck through, `D (42)` struck through, `A (3^6)` ticked yellow, `B (6^3)` struck through with a green arrow down to an empty green cloud, `C (7^3)` crossed green; below, six cyan marble circles labelled `M1 ... M6`, each with a yellow arrow to a `3`, giving yellow `3 x 3 x 3 ... = (3^6)` ringed.
**DIBY:** none. **U:** 1 — the option bubbles A–E are hand-drawn, not printed: the deck's question is free-response and the MCQ was made on the slide, so the option list is recorded as instructor-added.

---

<a id="p41"></a>
## p41 · Question — 4 letters, 3 post-boxes, two conditions · label: — (no label)
**P:** red chip **Question**; **Number of ways of posting 4 letters in 3 letters boxes such that:** cyan `(i) No box has more than one letter`, `(ii) No box should contain all letters` (`4 letters` yellow, `3 letters` green).
**H:** green sketch of three post-boxes labelled `P.B. 1`, `P.B. 2`, `P.B. 3`; a yellow row of four letter boxes `L1 L2 L3 L4`, each with an arrow down to `3 x 3 x 3 x 3 = 3^4 = (81)` (81 ringed); pink `(i) zero.`; pink `(ii)` with yellow `81 - 3 = (78) ways.` and a yellow arc under the subtracted `3`.
**DIBY:** none. **U:** none — (i) is dismissed in one word because four letters cannot sit one-per-box in three boxes.

---

<a id="p42"></a>
## p42 · Question — 7 people, number of hand-shakes · label: **Page No.125**
**P:** red chip **Question**; **Total 7 person gathered in conference hall for Annual meet, find total number of Hand-shakes.** (`7 person` in green).
**H:** the seven people in yellow as `A B C D E F G` in a row with hand-shake arcs drawn above and below them (cyan arcs fanning from `A`, green from `C`, red from `E`/`F`); below, the count in colours `6 + 5 + 4 + 3 + 2 + 1 = (21)` with the `21` ringed in red.
**DIBY:** none. **U:** none — this is the question whose working appears two lectures later as the unlabelled board pages P&C L04 p27-p28 (same `6+5+...+1 = 21` plus a K7 diagram); cross-referenced there.

---

<a id="p43"></a>
## p43 · Question — DIBY proof: sums of sin and cos 120° apart · label: — (no label)
**P:** red chip **Question**; **Prove that** cyan `(i) sin(theta) + sin(120 + theta) + sin(240 + theta) = 0` and `(ii) cos(theta) + cos(120 + theta) + cos(240 + theta) = 0` (degrees printed as `120°`, `240°`).
**H:** a red curly brace gathering both lines, a red arrow down to red `DIBY - (X)` with the crossed glyph ringed — the counterpart of p44's tick; no working.
**DIBY:** register row PC-L01-P43-DIBY(cross). **U:** none.

---

<a id="p44"></a>
## p44 · Question — DIBY proof: cos^2x + cos^2(x+pi/3) + cos^2(x-pi/3) = 3/2 · label: — (no label)
**P:** red chip **Question**; **Prove that** cyan `cos^2 x + cos^2 (x + pi/3) + cos^2 (x - pi/3) = 3/2`.
**H:** red handwriting at mid-right `DIBY - (tick)`: the word `DIBY`, a dash, and a ringed stroke that reads as a tick (it could also be a capital `Y`); nothing else on the slide — the identity is never worked.
**DIBY:** register row PC-L01-P44-DIBY(tick) — a hand-written DIBY tag with no printed `# DIBY-nn` label, the same pattern as L04 p11. **U:** 1 — p44's ringed stroke and p43's are one shape family (tick vs cross), so they are read as done/attempted marks rather than letters.

---

<a id="p45"></a>
## p45 · Homework · label: — (no label)
**P:** clipboard icon + red banner **Homework**; white `# Re-attempt all Class Examples`; white `# DPP & DIBY`.
**H:** none. **DIBY:** none — instruction slide with no `# DIBY-nn` item on it (F-18). **U:** none.

---

<a id="p46"></a>
## p46 · closing slide — Thank You · label: — (no label)
**P:** white script `It is never about` + red script `end result`; white script `It's always about` + cyan script `Journey`; large `Thank` (yellow) `You` (white script); cyan hashtag `#futurellTians`.
**H:** none. **DIBY:** none. **U:** none — the same closing card as the other three decks' endings.
