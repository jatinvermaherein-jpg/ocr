# Binomial Theorem — Lecture 08 (Class Notes) · Twin 1 transcript
Source: `Binomial Theorem 08 Class Notes.pdf` (46 pages, image-only, no text layer). Every page below was read visually from the render in `work/pages/bt08_pNN.png`. Page keys are PDF page numbers; the printed `Page No.` label, when present, is quoted in the header line.

> **Notation note (F-19).** Math is written in ASCII (`nC_r`, `2^10`) rather than stacked Unicode subscripts, and source typos are quoted verbatim (U-26).

<a id="p01"></a>
## p01 · Course title card — Arjun JEE 2027, Lecture 08 · label: — (PW roundel)
**P:** identical card to L04–L07: giant yellow **ARJUN** cracked by a silver arrow, white/silver **2027**, black banner **Lecture –08 | Mathematics**, amber panel **BINOMIAL THEOREM**, maroon capsule **By– Sachin Jakhar Sir**, teacher right in the black "Physics Wallah" polo with the three-finger salute, compass + pencil props bottom-left.
**H:** none. **DIBY:** none. **U:** none.

---
<a id="p02"></a>
## p02 · Topics to be covered — applications, remainders, integral & fractional parts · label: — (no header, board slide)
**P:** yellow **Topics** with white script `to be covered`; four red tiles down the left — `A` **Application of Binomial Theorem**, `B` **Finding Remainder**, `C` **Integral & Fractional Part**, `D` **Question Practice**; the first three titles are inside red rectangles, D is not; right, an orange pencil mascot with a pink eraser cap leaning thoughtfully on a giant silver question mark.
**H:** none.
**DIBY:** none. **U:** none — this is the first lecture whose three named topics are all *application* blocks (no new theory heading).

---
<a id="p03"></a>
## p03 · H.W. Discussion — the divider · label: — (no header, board slide)
**P:** white **H.W. Discussion** inside a red rectangle, centred on an otherwise empty black board.
**H:** none.
**DIBY:** none. **U:** none — as in L06/L07, the lecture opens by clearing the previous lecture's homework pile (F-29).

---
<a id="p04"></a>
## p04 · Question [JEE Mains-2022] — Sum_{i != j} ^nC_i ^nC_j, resumed from L07 p19 · label: **Page No. 159**
**P:** red chip **Question [JEE Mains-2022]**; the same question as L07 p19 re-printed — blue sum `Sum_{i,j=0, i != j}^{n} ^nC_i ^nC_j` + white **is equal to**; red tiles `A 2^{2n} - ^{2n}C_n`, `B 2^{2n-1} - ^{2n-1}C_{n-1}`, `C 2^n - 1/2 ^{2n}C_n`, `D 2^{n-1} + ^{2n-1}C_n`; no printed key line.
**H:** orange ring at top right enclosing **`73%`** over a double underline; an orange arrow from the printed sum into orange `Sum_{j=0, i != j}^{n} Sum_{i=0}^{n} ^nC_i ^nC_j`; an orange equals sign then cyan `Sum_{0 <= i < j <= n} ^nC_i ^nC_j + Sum_{0 <= j < i <= n} ^nC_i ^nC_j` — the p15 split applied to the pair sum; an orange diagonal stroke across option tile **A** with a short orange tick at its left edge, marking A as the picked answer.
**DIBY:** none. **U:** none — L07 p19's question is thus answered here, one page after the `dev.` ring mark (U-27); the printed label `Page No. 159` is the same label already spanning L07 p15–p19, continuing the F-26 drift.

---
<a id="p05"></a>
## p05 · board — Total = 2^2n and the diagonal sum = ^2nC_n, so the answer is A · label: — (no header, board slide)
**P:** none — pure board page.
**H:** cyan at top `Total = Sum_{j=0}^{n} ( Sum_{i=0}^{n} ^nC_i ^nC_j )` (the inner product in yellow) `= Sum_{j=0}^{n} ( ^nC_j Sum_{i=0}^{n} ^nC_i ) = 2^n Sum_{j=0}^{n} ^nC_j = 2^{2n}` — each of the two inner sums is blobbed in cyan and labelled `2^n` above it; second line, cyan `Total` inside a white ring with a white `2^n` written under the ring, then `= Sum Sum_{i=j} + Sum Sum_{i<j} + Sum Sum_{i>j}` with a cyan **cloud** drawn over each sum (the p15 three-way split, with the clouds standing for the term sets); an orange arrow from the `i = j` cloud down into a **red rectangle** holding orange `Sum_{j=0}^{n} Sum_{i=0}^{n} ^nC_i ^nC_j , (i = j)`; a white arrow out of that box labelled white `j -> i` to white `Sum_{i=0}^{n} (^nC_i)^2 = ^{2n}C_n` (a small down arrow under the sigma) with the expansion beneath it `(^nC_0)^2 + (^nC_1)^2 + (^nC_2)^2 + ... + (^nC_n)^2` and a white curved arrow back up to `^{2n}C_n`.
**DIBY:** none. **U:** none — the ring round `Total` with `2^n` below it is the teacher's shorthand for the two-factor split (`2^n . 2^n`); read literally as written.
<a id="p06"></a>
## p06 · Question [JEE Mains–2021] — coefficient of a^7 b^8 in (a + 2b + 4ab)^10 = K.2^16 · label: — (chip only)
**P:** red chip **Question [JEE Mains–2021]**; **If the coefficient of** `a^7 b^8` **in the expansion of** `(a + 2b + 4ab)^10` **is** `K.2^16`**, then** `K` **is equal to ________.** (`a^7 b^8` orange, trinomial green, `K` cyan). A white circle with **`88%`** and a double underline sits top-right (success-rate tag, F-13).
**H:** cyan arc from the trinomial to the cyan multinomial term `10!/(a! b! g!) a^a (2b)^b (4ab)^g`; a pink cloud restating it as `10!/(a!b!g!) 2^b 4^g a^(a+g) b^(b+g)` with the two exponents ringed in orange and labelled `7` and `8`; right, cyan `a + b + g = 10` over orange `a + g = 7`, `b + g = 8`, an orange brace giving `a = 2`, `b = 3`, `g = 5`; a **red rectangle** holding pink `10!/(2!3!5!) . 2^3 . 4^5 a^7 b^8`; beside it a white circle `315` with the cursive `fnf` mark after it — the ringed number is K itself (10!/(2!3!5!) = 2520, x 2^3 2^10 / 2^16 = 2520/8 = 315 ✓).
**DIBY:** none. **U:** none. The `fnf`-after-a-ring is the pattern F-21 identified (teacher's "final" tag).

---
<a id="p07"></a>
## p07 · Question [JEE Mains–2020] — (2x^2+3x+4)^10 = SUM a_r x^r, find a_7/a_13 · label: **Page No. 160**
**P:** red chip **Question [JEE Mains–2020]** with a cluster of gold star stickers to its right; **Let** `(2x^2 + 3x + 4)^10 = SUM_{r=0}^{20} a_r x^r`**. Then** `a_7/a_13` **is equal to ________.** (the trinomial yellow, the ratio cyan).
**H:** the blank filled in yellow with `8` inside a ring, a yellow arrow out to the cursive `fnf`-family mark at the right edge; pink circle `M-1` (double-underlined); cyan `10!/(a!b!g!) (2x^2)^a (3x)^b 4^g = 10!/(a!b!g!) 2^a 3^b 4^g x^(2a+b)`; orange `a_7 = coeff of x^7 => 2a + b = 7 & a + b + g = 10` and `a_13 = coeff of x^13 => 2a + b = 13 & a + b + g = 10`; at left a long pink bracket down to pink cursive **`lengthy~~~`** (the same comment as L05 p05, where it was ambiguous — here the word is unambiguous).
**DIBY:** none. **U:** none — Method 1 is set up and abandoned; the replacement method (p08) is used instead.

---
<a id="p08"></a>
## p08 · p07 solved by Method 2 — "Replacement" x -> 4/(2x) · label: — (no header, board slide)
**P:** none — pure board page.
**H:** green ring `M-2` and green **`Replacement`** double-underlined; the red box `(2x^2+3x+4)^10 = a_0 + a_1 x + a_2 x^2 + … … + a_19 x^19 + a_20 x^20` with `a_0` ringed green and `a_19`, `a_20` ringed orange; at left orange `x -> 4/(2x)` **OR** `x -> 2/x`; orange arrow to `x^10 (4+3x+2x^2)^10` (an orange strike through a stray `x^20` written under it) = white/cyan `a_0 x^20 + a_1 2^1 x^19 + a_2 2^2 x^18 + … … + a_19 2^19 x^1 + a_20 2^20`, the trailing `x^20` underlined and struck in orange; a red box `(4+3x+2x^2)^10` with every term divided by `2^10` (`a_0 x^20/2^10` ringed orange, `a_20 2^20/2^10` ringed green); down the page three red boxes with the paired coefficients — green `a_0 = a_20 2^20/2^10`, orange `a_19 = a_1 2^1/2^10`, orange `a_20 = a_0 2^0/2^10` — a dashed arrow to a fourth red box `a_13 = a_7 . 2^7/2^10`; at left the conclusion in orange `a_7 = a_13 2^13/2^10`, hence `a_7/a_13 = 2^3 = 8`; bottom-right white `8 (ringed) = 2^3 = 2^10/2^7 = a_7/a_13`.
**DIBY:** none. **U:** 1 — in that last fraction the numerator is drawn like `a_0`/`a_7`; the identity two lines above requires `a_7`, transcribed as `a_7`.

---
<a id="p09"></a>
## p09 · APPLICATION OF BINOMIAL THEOREM — 1. Finding Remainder (new section) · label: **Page No. 161**
**P:** clipboard icon + red banner **APPLICATION OF BINOMIAL THEOREM**, thickly decorated with gold star stickers (three clusters); everything else is board work.
**H:** cyan ringed `1` then cyan **`Finding Remainder :`** underlined; two orange short-division sketches of 13 by 7 — `7 sqrt(13)` with `14` under it and the remainder ringed cyan `-1`, then the same with `7` under it and the remainder ringed cyan `6` plus a white tick; cyan below `fnl = -1 + 7 = 6`; right, pink `13 x 23 x 65 x 101` with green remainders `1, 2, 2, 2` written above the four factors, green arcs pairing them over a pink `3`, a pink arrow to pink `Remainder => 2` with a green tick, and a green `8/3` joined by a long green arrow into that `2`; in a red cloud at the right edge, red **`100% Ques^n`** over a red Devanagari word read as **आएगा** ("will come") — the same claim L06 p14 records as "100% Ques aaega".
**DIBY:** none. **U:** 1 — the Devanagari is written cursively; `आएगा` is the reading that matches the English elsewhere in the series. **Also:** the mark before `= -1 + 7 = 6` is spelled **`fnl`**, a cleaner form of the `fnf` scribble (see F-30 below) and further support for "final".

---
<a id="p10"></a>
## p10 · p09 continued — remainders mod 3, and (13)^76/3 · label: — (no header, board slide)
**P:** none — board page split by a wavy white vertical line.
**H:** left, green `R = 2 <=` green `8/3` `==` pink `13 x 23 x 65 x 101` with green remainders `-2, 2, -1, 2` above the factors and a pink `3` under the join; below it green `R = (-1)` ringed `<=` `-16/3` `==` the same pink product with remainders `-2, 2, 2, 2` and a pink `3`, then a green arrow from the ringed `(-1)` labelled `+3` to a ringed `2` with a green tick. Right, white `(13)^76 / 3 ==` a ringed `R = 1`, with white arcs down to `13 x 13 x 13 x … 13` carrying a small `1` above every factor and a `3` under the product line (13 == 1 mod 3).
**DIBY:** none. **U:** none.
<a id="p11"></a>
## p11 · p10 continued — (14)^76/3 solved two ways, named after students · label: — (no header, board slide)
**P:** none.
**H:** white at top `(14)^76 / 3 => R = (1)` with the answer ringed; two orange arrows down to two orange methods, each headed by a name with a wavy underline: **`Sumit`** — `14 x 14 x … 14` (76 factors) over `3` with `-1` written above every 14, collapsing to orange `(-1)^76/3 => (R = 1)` ringed; **`Santosh`** — the same product with `2` above every factor over `3`, then `=> 2^76/3 = (2 x 2 x … x 2)/3` with `-1` above each 2 over `3`, an orange arrow to a large ringed **`R = 1`**.
**DIBY:** none. **U:** none. (Both routes give the same remainder; the naming is the teacher's habit of crediting a classroom solution.)

---
<a id="p12"></a>
## p12 · RAPID FIRE ROUND — remainder items (i)–(iv), (i) solved twice · label: **Page No. 161 / 162**
**P:** red chip **RAPID FIRE ROUND**; printed list `(i)` **Find Remainder of** `2^136 ÷ 7`, `(ii)` **Find Fractional part of** `5^99/13`, `(iii)` `7^2022 + 3^2022` **divided by 5**, `(iv)` **[JEE MAINS–2022] Remainder when (11)^1011 + (1011)^11 divided by 9** (the year-tag yellow). The printed label is the compound **`Page No. 161 / 162`**, i.e. one slide spanning two module pages (kept in the audit as one row, first of four such slides).
**H:** orange, top-right, the remainder-of-products route: `2^136/7 = 2¹.(8)^45/7 = 2¹ · 8.8.8…8/7` with `-1` above every 8, an arc marked `7` under the run, giving orange `R = 2`. Below the printed list, the same (i) by expansion: orange `2^136 = 2¹.(2^135) = 2¹.(2³)^45 = 2¹.(7+1)^45` (the `2³` ringed and double-underlined); cyan `2^136/7 = ( ⁴⁵C₀ 7^45·2 + ⁴⁵C₁ 7^44·2 + … … + ⁴⁵C₄₄ 7¹·2 + ⁴⁵C₄₅ 1·2 )` with everything but the last term inside a **red rectangle** (those are multiples of 7), the final `⁴⁵C₄₅ 1·2` ringed cyan with a `2` above it; then cyan `2^136/7 = (integer)/7 + (2/7)` with the `2/7` ringed, and cyan `R = 2` under a white tick. Item `(i)` carries an orange tick; item `(iii)` an orange stroke through the numeral.
**DIBY:** none. **U:** 1 — the compound printed page label `161 / 162` (F-08's non-monotonic labelling, new form).

---
<a id="p13"></a>
## p13 · RAPID FIRE ROUND — item (ii) fractional part of 5^99/13 · label: **Page No. 161 / 162**
**P:** the same printed four-item list; `(i)` and `(ii)` now ticked in magenta.
**H:** cyan at top right `5¹.5^98/13 = 5¹.25^49/13 = 5¹.25.25.25…25/13` — a green brace over the run labelled `49`, a `5` then `-1` written above the factors, and cyan `≡ -5/13`; yellow `R = -5 +13 = (8)` with 8 ringed. Item `(ii)` re-opened in cyan: `{ 5^99/13 } = Remainder/13 = 8/13`; a green generic division sketch `y sqrt(x)` with `Q` above and `R` below, in braces, `-> x = yQ + R`; below, pink `13 sqrt(5^99)` with `8` under the bar, then `{5^99/13} = { (13(Q) + 8)/13 } = { Q + 8/13 } = {8/13} = 8/13 - [8/13 (struck, `0` beneath) } = 8/13`, with a magenta arc linking the pink working to the green sketch.
**DIBY:** none. **U:** none.

---
<a id="p14"></a>
## p14 · rule card — fractional-part function · label: — (no header, board slide)
**P:** none.
**H:** a cyan cloud enclosing a **red rectangle** with cyan `{ a^n / b } = Remainder/b`; a cyan line from the cloud to a small pink oval labelled **`FPF`** (the curly braces are the fractional-part function); at right a pink cloud with pink `{ Integer + a } = { a }`.
**DIBY:** none. **U:** 1 — this is the one place the writer spells **`FPF`** in clear capitals; it must not be conflated with the cursive `fnf`/`fnl` mark that follows ringed answers on p06 and in L05 (F-30) — different glyph, different meaning, both appearing in the same lecture.

---
<a id="p15"></a>
## p15 · RAPID FIRE ROUND — item (iii): 7^2022 + 3^2022 mod 5 · label: **Page No. 161 / 162**
**P:** the same printed list.
**H:** a green arrow from `(iii)` to cyan `(iii)` then green `7^2022/5 + 3^2022/5`; the `7^2022` term ringed in orange with an orange arrow down to `(49)^1011/5 => (-1) or (4)` (both ringed); an orange arrow from the second fraction to `(-1) or (4)`; orange at right `(3²)^1011/5 = (9.9.9…9)/5` with `-1` above each 9, over `5`, giving `=> (-1)` ringed; the item's answer written at top-right in a yellow ring fed by an orange arc: **`R = 3`** (4 + 4 = 8 ≡ 3).
**DIBY:** none. **U:** none.

---
<a id="p16"></a>
## p16 · RAPID FIRE ROUND — item (iv), JEE MAINS–2022 · label: **Page No. 161 / 162**
**P:** the same printed list, item `(iv)` unchanged.
**H:** green working in two halves, each headed by a green `9` (the divisor) under the printed bases. Left: `11.11.11…11` (1011 factors) with a `2` above each, over `9`, `≡ 2^1011/9 = (2³)^337/9 = 8^337/9 = (8.8.8…8)/9` with `-1` above each 8, `=> R = -1 + 9 = (8)`. Right: `1011.1011…1011` (11 factors) with a `3` above each, over `9`, `=> 3^11/9` with a green arrow to `R = 0`. The two halves are joined by green arcs up to the green conclusion `8 + 0 = (8)` with the 8 ringed.
**DIBY:** none. **U:** none. (The same JEE MAINS–2022 pair sum reappears as L07 p04's H.W. answer — cross-lecture chain already logged there.)
<a id="p17"></a>
## p17 · JEE MAINS–2024: remainder of 428^2024 ÷ 21 · label: **Page No. 162**
**P:** red chip `Question [JEE Mains–2024]`; question **The remainder when 428^2024 is divided by 21 is** (428 cyan).
**H:** green chain `(428)^2024/21 ≡ (8)^2024/21 = (8²)^1012/21 = (64)(64)(64)…(64)` over `21` — each 64 ringed with a `1` above it — `⇒` ringed **1**.
**DIBY:** none. **U:** none.

---
<a id="p18"></a>
## p18 · JEE MAINS–2023: 19^200 + 23^200 ÷ 49 (H.W.) · label: **Page No. 161**
**P:** red chip `Question [JEE Mains–2023]`; **The remainder, when 19^200 + 23^200 is divided by 49, is ________.** (bases cyan).
**H:** green ring round **`H.W.`**, double-underlined, to the right of the blank.
**DIBY:** none (H.W. ring alone is not a register row). **U:** 1 — label back to `161` after `162` (F-08).

---
<a id="p19"></a>
## p19 · JEE MAINS–2024: remainder of 64^32^32 ÷ 9 · label: — (no printed label)
**P:** red chip `Question [JEE Mains–2024]`; **Remainder when 64^32^32 is divided by 9 is equal to** (64 cyan, tower exponent).
**H:** green ring round the exponent `32^32` with an arrow to a green `k`; below, green `k Time` brace over `64.64.64…64` divided by `9`, `⇒` a large green ring **`R = 1`**.
**DIBY:** none. **U:** none.

---
<a id="p20"></a>
## p20 · Acidic Question (NCERT): 6^(n+2) + 7^(2n+1) divisible by 43 · label: **Page No. 161**
**P:** red chip **Acidic Question** with a pink ring round **NCERT**; **Show that 6^(n+2) + 7^(2n+1) is divisible by 43 for all n ∈ N**, the `n ∈ N` inside a red rectangle.
**H:** cyan re-writing `7^(2n).7¹ = 49ⁿ.7¹` with orange arrows down to `(43+6)^n`; pink/cyan/orange `6^(n+2) + 7.(43+6)^n = 6^(n+2) + 7.( ⁿC₀43ⁿ + ⁿC₁43^(n-1)6¹ + … … + ⁿC_(n-1)43¹6^(n-1) + ⁿCₙ6ⁿ )` with the bracketed expansion inside a **red rectangle**; orange `= 6ⁿ.6² + 7.(43(I) + 6ⁿ)`; orange `= 6ⁿ.36 + 7×43×I + 7×6ⁿ` (double-underlined on the first and last terms); orange `= 43(7I) + 6ⁿ(36+7)` with cyan `43` under `(36+7)`, a cyan tick and a cyan cursive annotation in parentheses at the right (unresolved).
**DIBY:** none. **U:** 1 — the trailing cyan parenthesised cursive is illegible at render resolution.

---
<a id="p21"></a>
## p21 · IMPORTANT NOTE — x^n − y^n and x^n + y^n divisibility, with proof · label: — (no printed label)
**P:** red chip **IMPORTANT NOTE**; **(a)** `(x^n − y^n) n ∈ N is always divisible by (x − y).`; **(b)** `(x^n + y^n) n ∈ odd natural number is always divisible by (x + y).` (green powers, cyan divisors).
**H:** cyan arc from (b) to the proof `((x+y) − y)^n + yⁿ`, the inner `(x+y−y)` double-underlined in orange; the expansion `ⁿC₀(x+y)ⁿ − ⁿC₁(x+y)^(n-1)y¹ + ⁿC₂(x+y)^(n-2)y² − … … + ⁿC_(n-1)(x+y)¹(−y)^(n-1) + ⁿCₙ(−y)ⁿ + yⁿ` written across the slide with the leading part inside a **red rectangle** and a pink arrow to `(x+y)×I`; a long cyan arc carries the left-hand `+ yⁿ` to the far right; pink bottom-right `(-1)ⁿyⁿ + yⁿ` with an arrow labelled `n∈odd` to `-yⁿ + yⁿ = 0`.
**DIBY:** none. **U:** none.

---
<a id="p22"></a>
## p22 · board — two applications of the rule · label: — (no printed label)
**P:** none.
**H:** green `xⁿ − y is always div. by` with `(x−y)` ringed; an orange arc down to orange `25³⁴ − 9³⁴ is div. by` a cyan ring **16** (orange wavy line under it, cyan arrow up from `25 − 9`); below, pink `21³³ + 12³³ is div. by` a pink ring **33** with a pink arrow up from `(21+12)`.
**DIBY:** none. **U:** none.

---
<a id="p23"></a>
## p23 · JEE MAINS–2023 MCQ: 25^190 − 19^190 − 8^190 + 2^190 · label: — (no printed label)
**P:** red chip `Question [JEE Mains–2023]`; **25^190 − 19^190 − 8^190 + 2^190 is divisible by**; options **A 34 but not by 14**, **B Both 14 and 34**, **C Neither 14 nor 34**, **D 14 but not by 34** — a yellow/orange tick across box A.
**H:** a pink arc links the first two powers and another the last two; yellow parity chain at the right: `odd — odd` above, `(odd − even)` in a yellow ring feeding from the two brackets, a yellow arrow to `even`; the pink grouping `(25^190 − 8^190) − (19^190 − 2^190)` inside a **red rectangle**, with pink `div. by (25−8)` and `↧ 17`, and `19 − 2 = 17`.
**DIBY:** none. **U:** none. (The working proves divisibility by 17; the tick is on A — recorded as drawn.)
<a id="p24"></a>
## p24 · JEE MAINS–2023 MCQ: two divisibility statements (H.W.) · label: **Page No. 162**
**P:** red chip `Question [JEE Mains–2023]`; **Among the statements:** `(S1): 2023^2022 − 1999^2022 is divisible by 8`, `(S2): 13(13)^n − 11n − 13 is divisible by 144 for infinite many n ∈ N.`; options **A Both (S1) and (S2) are incorrect**, **B Only (S1) is correct**, **C Only (S2) is correct**, **D Both (S1) and (S2) are correct** (no tick).
**H:** yellow ring round **`H.W.`**, double-underlined, right of S2.
**DIBY:** none. **U:** none.

---
<a id="p25"></a>
## p25 · JEE MAINS–2023: remainder of (2023)^2023 ÷ 35 (H.W.) · label: — (no printed label)
**P:** red chip `Question [JEE Mains–2023]`; **The remainder when (2023)^2023 is divided by 35 is ________.**
**H:** yellow ring round **`H.W.`**, double-underlined, under the blank.
**DIBY:** none. **U:** none.

---
<a id="p26"></a>
## p26 · FINDING LAST DIGIT(S) — last digit of 3^104 · label: **Page No. 162**
**P:** section banner chip **FINDING LAST DIGIT(S)** (white rounded card with a clipboard-and-pencil emoji) + smaller red chip **Question**; **Find last digit of 3^104.** (cyan).
**H:** a pink arrow from the banner to pink `create (10)` (10 ringed); pink `3^104 = (3²)^52 = (10−1)^52 = ⁵²C₀10^52 − C₁10^51 + ⁵²C₂10^50 − … + ⁵²C₅₀10² − ⁵²C₅₁10¹ + ⁵²C₅₂` with the long leading run inside a **red rectangle** and a cyan blob ring round the penultimate term `⁵²C₅₁10¹`; cyan `= 100(I) − 520 + 1` and `= 100(I) − 519` (orange wavy underline on 100(I)); at right orange `100(I) = ~~~ 00` over `− 519` and a wavy rule with a ringed **`81`** — the last two digits, so the last digit is 1.
**DIBY:** none. **U:** none. (New sub-section marker in the deck; the emoji card is decorative, no register row.)

---
<a id="p27"></a>
## p27 · JEE MAINS–2024: product of last two digits of 1919^1919 (H.W.) · label: — (no printed label)
**P:** red chip `Question [JEE Mains–2024]`; **Product of last two digits of 1919^1919 is ________.**
**H:** yellow ring round **`H.W.`**; an orange arrow from the printed power down to the opened method orange `(1920 − 1)^1919 = ~~~` and nothing further (the class only sets up the "nearest multiple of 100" trick).
**DIBY:** none. **U:** none.

---
<a id="p28"></a>
## p28 · INTEGRAL & FRACTIONAL PART — (√2+1)^6 = I + f · label: **Page No. 162**
**P:** section banner **INTEGRAL & FRACTIONAL PART** (white card + clipboard emoji) and chip **Question**; **If (√2 + 1)^6 = I + f where I is integral part & f is fractional part). Then find:** `(i)` **I** `(ii)` **f² + 196f** (cyan) — both item numerals crossed in magenta.
**H:** magenta `= 197.` after (i); white `= 196.` after (ii); pink expansion `(√2+1)^6 = ⁶C₀(√2)⁶ + C₁(√2) + ⁶C₂(√2)⁴ + C₃(√2)³ + ⁶C₄(√2)² + ⁶C₅√2 + ⁶C₆`; cyan `(√2 − 1)^6 =` left open.
**DIBY:** none. **U:** none.

---
<a id="p29"></a>
## p29 · add the conjugates — 2(⁶C₀2³ + …) = 198 · label: — (no printed label)
**P:** none.
**H:** the two expansions repeated, pink `(√2+1)^6 = …` and cyan `(√2−1)^6 = ⁶C₀(√2)⁶ − C₁(√2)⁵ + … `, each with the odd terms `⁶C₁(√2)⁵`, `⁶C₃(√2)³`, `⁶C₅√2` struck through in orange; cyan `add` double-underlined with a long cyan rule; the sum `= 2( ⁶C₀(√2)⁶ + ⁶C₂(√2)⁴ + ⁶C₄(√2)² + ⁶C₆ )` in pink/yellow, an orange arrow down to yellow `= 2( ⁶C₀2³ + ⁶C₂2² + ⁶C₄2 + ⁶C₆ )`, then yellow `= 198` (underlined).
**DIBY:** none. **U:** none.

---
<a id="p30"></a>
## p30 · I + f + G = 198 ⇒ f + G = 1, I = 197 and f² + 196f = 196 · label: — (no printed label)
**P:** none.
**H:** green `(√2+1)^6 + (√2−1)^6 = 198`; orange arrows to `I + f + G = 198` with a pink arc over the whole left side feeding a ring labelled **Integer** and magenta `Int.` under 198; right, white `0 ≤ f < 1`, `0 < G < 1`, a rule, `0 < f + G < 2`; pink arcs from both to the central pink `# f + G = 1`; left, orange `I + (f + G)` — the bracket ringed pink with a `1` above — `= 198`, and magenta `I = 197` double-underlined; right, green `(√2+1)^6 × (√2−1)^6 = 1` down to `(I+f)(G) = 1` (G ringed) then `(197 + f)(1 − f) = 1`; centre-bottom white `197 + f − 197f − f² = 1` and a ringed **`196 = f² + 196f`** (the exponent on the first f is faint).
**DIBY:** none. **U:** 1 — `f²` vs `f` in that last line; the algebra forces the square, and the superscript is present but light.

---
<a id="p31"></a>
## p31 · the subtraction variant: f − G = 0 · label: — (no printed label)
**P:** none.
**H:** orange `I` (ringed cyan) `+ f − G = 198` (green) with a pink arc over `+ f − G` to a pink **Integer** ring and magenta `Int.`; right white `0 ≤ f < 1`, `0 < G < 1` over a rule; a cyan arc labelled cyan `×(−1)` down to `0 ≤ f < 1`, `−1 < −G < 0`, cyan `add`, rule, `−1 < f − G < 1`; white arcs from the Integer ring and from that last line to white **`# f − G = 0`**.
**DIBY:** none. **U:** none.

---
<a id="p32"></a>
## p32 · method card — add or subtract, then multiply · label: — (no printed label)
**P:** none.
**H:** red `# S⁴` at top-left; pink `(a+√b)^n = I + f` and `(a−√b)^n = G` with green arrows into a green ring **add** `or` ring **sub.**; orange arcs up from both rings to orange `as acc. to irr. terms get cancelled.`; orange arcs down to `f + G = 1` (from add) and `f − G = 0` (from sub); below, cyan `# final step: multiplication` beside a **red rectangle** round pink `(a+√b)^n (a−√b)^n`. The cursive word **final** here is written out in full — it is the same token as the abbreviated `fnf`/`fnl` mark seen before a boxed answer on p06 (and in L05), confirming F-30 rather than clashing with the printed `FPF` of p14.
**DIBY:** none. **U:** none.

---
<a id="p33"></a>
## p33 · prove I = 1/(1−f) − f for (5+2√6)^n · label: **Page No. 163**
**P:** red chip **Question**; **If (5 + 2√6)^n = I + f, where I ∈ N, n ∈ N and 0 ≤ f < 1, then prove that I = 1/(1−f) − f.** (the fraction printed cyan).
**H:** white `(5+2√6)^n = ⁿC₀5ⁿ + ⁿC₁5^(n-1)(2√6)¹ + ⁿC₂5^(n-2)(2√6)² + …` and `(5−2√6)^n = ⁿC₀5ⁿ − ⁿC₁5^(n-1)(2√6)¹ + ⁿC₂5^(n-2)(2√6)² − …`, each with the `ⁿC₁` term struck through in orange; orange `add` with a long orange rule; orange `(5+2√6)^n + (5−2√6)^n = 2( ⁿC₀5ⁿ + ⁿC₂5^(n-2)2².6¹ + … … )` with a green wavy underline; cyan `I + f` + green `G` = green `I₁`, with a white rule under `f + G` dropping to `1`; white `# f + G = 1`.
**DIBY:** none. **U:** none.

---
<a id="p34"></a>
## p34 · multiplication step closes p33 · label: — (no printed label)
**P:** none.
**H:** white `(5+2√6)^n · (5−2√6)^n = 1`; orange arcs down to orange `(I+f) G = 1`, an arrow to `(I+f)(1−f) = 1`, an arc to `I = 1/(1−f) − f`; at the right an orange cursive closing annotation that reads as **`hence`** under a small rule (same glyph style as the cyan mark at the foot of p20) — the teacher's proof-completion tag, not a number.
**DIBY:** none. **U:** 1 — that cursive tag is legible only as `hence`; recorded as a tag, no value.
