# Binomial Theorem — Lecture 07 (Class Notes) · Twin 1 transcript
Source: `Binomial Theorem 07 Class Notes.pdf` (34 pages, image-only, no text layer). Every page below was read visually from the render in `work/pages/bt07_pNN.png`. Page keys are PDF page numbers; the printed `Page No.` label, when present, is quoted in the header line.

> **Notation note (F-19).** Math is written in ASCII (`nC_r`, `2^10`) rather than stacked Unicode subscripts, and source typos are quoted verbatim (U-26).

<a id="p01"></a>
## p01 · Course title card — Arjun JEE 2027, Lecture 07 · label: — (PW roundel)
**P:** identical card to L04/L05/L06: giant yellow **ARJUN** cracked by a silver arrow, white/silver **2027**, black banner **Lecture –07 | Mathematics**, amber panel **BINOMIAL THEOREM**, maroon capsule **By– Sachin Jakhar Sir**, teacher right in the black "Physics Wallah" polo with the three-finger salute, compass + pencil props bottom-left.
**H:** none. **DIBY:** none. **U:** none.

---
<a id="p02"></a>
## p02 · Topics to be covered — Binomial Series, **Multinomial Theorem**, Question Practice · label: — (chip only)
**P:** yellow **Topics** + white script *to be covered*; red tiles `A` **Binomial Series** (red rectangle), `B` **Multinomial Theorem** (red rectangle), `C` **Question Practice**, `D` tile printed with **no text**; pencil-character leaning on a silver question mark.
**H:** none. **DIBY:** none. **U:** none — the empty `D` tile is the deck-wide template defect (L04 p03 U-16, L05 p02). `Multinomial Theorem` is the new topic of this lecture and the first time it appears in the BT series.

---
<a id="p03"></a>
## p03 · H.W. Discussion — section break · label: — (chip only)
**P:** black slide, white **H.W. Discussion** in a red rectangle.
**H:** none. **DIBY:** none. **U:** none.

---
<a id="p04"></a>
## p04 · Question [JEE Mains–2021] — Sum (2^k + 3k) 10Ck = a.3^10 + b.2^10, find a + b · label: **Page No. 155**
**P:** red chip **Question [JEE Mains–2021]**; **Let** `nC_r` **denote the binomial coefficient of** `x^r` **in the expansion of (1 + x)^n`.** **If** `Sum_{k=0}^{10} (2^k + 3k) 10C_k = a . 3^10 + b . 2^10 , a, b in R`, **then** `a + b` **is equal to** + blank rule (the summand `(2^k + 3k)` yellow, the sum green, `a + b` cyan).
**H:** cyan double arc under `2^k + 3k` (the split into two sums); orange splitting it as `Sum_{r=0}^{10} 10C_r 2^r + 3 Sum_{r=0}^{10} r . 10C_r`, the first sigma ringed in an orange blob, the `r . 10C_r` rewritten below in orange as `10 . 9C_{r-1}`; orange arrow down to `(1+2)^10 + 30 [ Sum_{r=1}^{10} 9C_{r-1} ]` (the second sigma ringed, `2^9` written under it as the check value); orange result `= 1 . 3^10 + 15 x 2^10` with the `1` ringed and labelled `a` and the `15` ringed and labelled `b`; orange arrow from the printed `a + b` to a circled **`16`** with the cursive `fnf` under it (final-answer tag, F-21); far right an orange ring holding **`85%`** double-underlined (the class success rate).
**DIBY:** none. **U:** none — the printed text has no answer key on the slide; `16` is the teacher's written answer only.

---
<a id="p05"></a>
## p05 · Question [JEE Mains–2023] — Type-02 sum = 1023/10, find n · label: — (chip only)
**P:** red chip **Question [JEE Mains–2023]**; **If** `1/(n+1) nC_n + 1/n nC_{n-1} + ... + 1/2 nC_1 + nC_0 = 1023/10`**, then** `n` **is equal to** (the binomials green, `n` cyan); red tiles `A 9`, `B 6`, `C 7`, `D 8`; printed **`Ans: A`** in blue at the right.
**H:** orange curl arrow from the left of the line into the compact form `Sum_{r=0}^{n} nC_r/(r+1)` with an orange tick; a short orange vertical stroke under `nC_0` writing in the missing denominator `1`; right of centre orange **`# Done!!`** double-underlined — the item is L05 p35's Type-02 identity, `(2^(n+1) - 1)/(n+1) = 1023/10` gives n = 9, so no fresh working is written.
**DIBY:** none. **U:** none.

---
<a id="p06"></a>
## p06 · Acidic Question — L06 p34's unanswered series, solved here · label: — (chip only)
**P:** red chip **Acidic Question**; printed cyan `S = 3 . 10C_0 + 3^2 . 10C_1/2 + 3^3 . 10C_2/3 + ... + 3^11 . 10C_10/11`. No options, no key — the slide L06 p34 left hanging (F-25) is reprinted here in full.
**H:** orange `1` written under the first `10C_0` (the implicit denominator); white arrow down to white `S = Sum_{r=0}^{10} ( 10C_r/(r+1) ) 3^(r+1)` with the fraction ringed in orange; an orange arrow out of that ring into the Property-05 rewrite, orange `1/11 Sum_{r=0}^{10} 11C_{r+1} 3^(r+1)` enclosed in a white blob; green `= 1/11 { (1+3)^11 - 1 }`; green **`(4^11 - 1)/11`** ringed in green with the cursive `fnf` beside it (F-21); below, a red rectangle holding the expansion green/white `11C_0 3^0 + 11C_1 3^1 + 11C_2 3^2 + 11C_3 3^3 + ... + 11C_11 3^11` minus the green underlined `- 11C_0 3^0` (the r = 0 term taken back out).
**DIBY:** none. **U:** none — **cross-lecture chain closed**: L06 p34 → L07 p06, to be recorded next to the L06 row (F-25 now resolved).
<a id="p07"></a>
## p07 · Question [IIT–JEE–2010] — A_r, B_r, C_r coefficients of (1+x)^10/(1+x)^20/(1+x)^30 · label: **Page No. 157**
**P:** red chip **Question [IIT–JEE–2010]**; **For** `r = 0, 1, …, 10`, **let** `A_r, B_r` **and** `C_r` **denote, respectively, the coefficient of** `x^r` **in the expansions** `(1 + x)^10, (1 + x)^20` **and** `(1 + x)^30`**. Then** `Sum_{r=1}^{10} A_r (B_10 B_r - C_10 A_r)` **is equal to**; red tiles `A B_10 - C_10`, `B A_10(B_10^2 - C_10 A_10)`, `C 0`, `D C_10 - B_10` (no printed key line).
**H:** orange along the top, the definitions the slide assumes: `A_r = 10C_r , B_r = 20C_r , C_r = 30C_r`; pink arcs over the two products inside the parenthesis and a pink arrow splitting the sum into pink `Sum_{r=1}^{10} A_r B_10 B_r - Sum_{r=1}^{10} A_r C_10 A_r`, with `A_r` and `B_r` ringed in green and green arrows up to green `20C_10` and `30C_10`; below, the two red boxes `Sum_{r=1}^{10} 10C_r 20C_r` (prefixed by green `20C_10`) and `Sum_{r=1}^{10} 10C_r 10C_r` (prefixed by orange `- 30C_10`); a green tick through option **D**; right, a green ring with **`60%`** double-underlined.
**DIBY:** none. **U:** none — **cross-lecture chain closed**: this is L06 p29's H.W.-flagged item (F-24), re-printed and worked here.

---
<a id="p08"></a>
## p08 · p07 finished — Vandermonde convolutions give C_10 − B_10 · label: — (no header, board slide)
**P:** none — pure board page.
**H:** green at top the two boxed sums carried from p07: `20C_10 [Sum_{r=1}^{10} 10C_r 20C_r] - 30C_10 [Sum_{r=1}^{10} 10C_r 10C_r]` (both sigmas still inside red rectangles, the minus in orange); a yellow arrow out of the first box into a big yellow bracket `10C_10 20C_0 + 10C_9 20C_1 + 10C_8 20C_2 + ... + 10C_0 20C_10 - 10C_10 20C_0` over a white wavy rule, with white arrows down to white `30C_10 - 1`; at right a third red box `Sum_{r=1}^{10} 10C_r 10C_{10-r}` with an orange arrow into orange `10C_0 10C_10 + 10C_1 10C_9 + 10C_2 10C_8 + ... + 10C_10 10C_0` over an orange wavy rule, corrected below by orange `- 10C_0 10C_10`; centre white the substituted line `20C_10 ( 30C_10 - 1 ) - 30C_10 ( 20C_10 - 1 )` with an orange arc over the first factor pair; below it the expansion `20C_10 30C_10 - 20C_10 - 30C_10 20C_10 + 30C_10` with both `20C_10 30C_10` products struck out in green, = green `30C_10 - 20C_10` = green **`C_10 - B_10`** (option D).
**DIBY:** none. **U:** none.

---
<a id="p09"></a>
## p09 · SERIES — Type 05: Replacement (the two standard substitutions) · label: **Page No. 158**
**P:** clipboard icon + red banner **SERIES**; yellow `# Type-05:` then green italic **Replacement** inside a red rectangle (the heading prints a **double colon** `Type-05::`); two further red rectangles, both yellow: `ax^2 + bx + a => x -> 1/x` and `ax^2 + bx + c => x -> c/(ax) ≡`.
**H:** green completing the second rule: `Product of Root / x` (i.e. x -> (product of roots)/x, the fraction bar drawn under *Product of Root*); a tall green brace joining both printed rules to green `Hint (Quad.)^n` with `Hint` double-underlined — the replacement idea applies to any power of a quadratic.
**DIBY:** none. **U:** none — the printed `Type-05::` double colon and the singular `Root` (for *Roots*) are transcribed as printed.

---
<a id="p10"></a>
## p10 · Bumper Question — (1 + x + x^2)^n = Sum a_r x^r, six things to show · label: **Page No. 158**
**P:** red chip **Bumper Question**; **If** `n` **is a positive integer and** `(1 + x + x^2)^n = Sum_{r=0}^{2n} a_r x^r` **(green). Then show that :** six lines in cyan — `(i) a_r = a_2n-r ; 0 <= r <= 2n`, `(ii) a_0 + a_1 + a_2 + .... + a_2n = 3^n`, `(iii) a_0 - a_1 + a_2 - a_3 + .... + a_2n = 1`, `(iv) a_0 + a_1 + a_2 + .... + a_{n-1} = 1/2 (3^n - a_n)`, `(v)` **in a red rectangle** `a_0 + a_2 + a_4 + .... + a_2n = 1/2 (3^n + 1)`, `(vi)` a second red rectangle round the tag **`[IIT-JEE 1994]`** and the statement `a_0^2 - a_1^2 + a_2^2 - a_3^2 + ... + a_2n^2 = a_n`.
**H:** the whole slide is board work. Orange restatement `(1+x+x^2)^n = a_0 + a_1 x + a_2 x^2 + ... + a_2n x^2n`; an orange arc labelled `a = 1` pointing at (ii) with a white `) x = 1` bracket at right; a cyan arrow labelled `x = -1` into (iii); ticks in blue/orange/cyan/cyan/cyan down the left of (i)–(v) marking them as done; cyan at right the mirrored row `3^n = a_0 + a_1 + a_2 + ... ... a_2n-2 + a_2n-1 + a_2n` with orange annotation marks above it (`↓ * #` over the first three terms, `# * ↓` over the last three), orange underlines on `a_0` and `a_2n`, a cyan double-headed arrow through the middle and a down arrow onto `a_2n`; cyan `a_{n-1} + a_n + a_{n+1}` with up-arrows under the outer terms and a double underline under `a_n` (the middle of the row, used in (iv)/(v)); the abbreviation **`HHPP.`** with a wavy underline; cyan `3^n = 2(a_0 + a_1 + a_2 + ... + a_{n-1}) + a_n` (the (iv) rearrangement); yellow, under (vi), arrows from each squared coefficient down to the convolution `a_0 a_2n - a_1 a_2n-1 + a_2 a_2n-2 - a_3 a_2n-3 ... ... a_2n a_0` (its last factor in green).
**DIBY:** none. **U:** 1 — `HHPP.` is an unexplained abbreviation (candidates: *half-partnership*, a Hindi-English shorthand); recorded, not interpreted, like `fnf`.
<a id="p11"></a>
## p11 · board — proof of (i): the x -> 1/x replacement makes the row palindromic · label: — (no header, board slide)
**P:** none — pure board page.
**H:** orange the expansion again `(1+x+x^2)^n = a_0 + a_1 x + a_2 x^2 + ... + a_2n x^2n`, ringed in **magenta** round `a_0` and `a_2n` and in **blue** round `a_1`, tagged orange circled `A`; pink `x -> 1/x` at left with a pink arc into yellow `(x^2+x+1)^n / x^2n = a_0 x^2n + a_1 x^2n-1 + a_2 x^2n-2 + a_3 x^2n-3 + ... + a_2n` over a yellow wavy rule, both `x^2n` divisors struck through in green; a blue arc at the right margin joining A to the next line, annotated blue **`same`** double-underlined; orange circled `B` on `B = (x^2+x+1)^n = a_0 x^2n + a_1 x^2n-1 + a_2 x^2n-2 + a_3 x^2n-3 + ... + a_2n-1 x + a_2n`, with `a_0 x^2n` ringed magenta, `a_2n-1` ringed blue and `a_2n` ringed magenta — the same three coefficients seen from the other end; bottom, magenta `a_0 = a_2n`, blue `a_1 = a_2n-1`, `- ... =>` and a **red rectangle** round blue **`a_r = a_2n-r`** (statement (i) proved).
**DIBY:** none. **U:** none.

---
<a id="p12"></a>
## p12 · board — (vi) opened: multiply by the x -> -x copy and take the x^2n coefficient · label: — (no header, board slide)
**P:** none — pure board page.
**H:** orange `(1+x+x^2)^n = a_0 + a_1 x + a_2 x^2 + ... + a_2n x^2n`; cyan `x -> -x` with a cyan arrow into cyan `(1-x+x^2)^n = a_0 - a_1 x + a_2 x^2 - ... + a_2n x^2n`; then the product written out `(1+x+x^2)^n (1-x+x^2)^n = ( a_0 + a_1 x + a_2 x^2 + ... + a_2n x^2n )( a_0 - a_1 x + a_2 x^2 - ... - a_2n-1 x^2n-1 + a_2n x^2n )` with small white ticks and arrows pairing the first and last factors of each bracket; green under the left-hand product a down arrow to green **`coeff. of x^2n`**; white the convolution actually picked out `( a_0 a_2n - a_1 a_2n-1 + a_2 a_2n-2 - ... ) x^2n`; bottom, green `coeff. of x^2n in (1+x+x^2)^n (1-x+x^2)^n` restating the target.
**DIBY:** none. **U:** none.

---
<a id="p13"></a>
## p13 · board — (vi) closed: that same coefficient is a_n · label: — (no header, board slide)
**P:** none — pure board page.
**H:** orange the expansion line once more; green `coeff. of x^2n in (1+x+x^2)^n (1-x+x^2)^n`; below it green `coeff. of x^2n in (1+x^2+x^4)^n` = white **`a_n`** (the substitution `x -> x^2` inside the same expansion, `+ a_n x^2n` underlined in orange with a white arrow pointing up at it); a blue **cloud** at right containing white `(1+x+x^2)(1-x+x^2) = 1+x^2+x^4` — the identity that makes the two products equal; lower half orange `(1+x+x^2)^n = a_0 + a_1 x + a_2 x^2 + ... + a_n x^n + ... + a_2n x^2n`, orange `x -> x^2`, then `(1+x^2+x^4)^n = a_0 + a_1 x^2 + a_2 x^4 + ... + a_n x^2n + ... + a_2n x^4n`.
**DIBY:** none. **U:** none.

---
<a id="p14"></a>
## p14 · board — differentiating the same expansion: two weighted sums · label: — (no header, board slide)
**P:** none — pure board page.
**H:** orange `(1+x+x^2)^n = a_0 + a_1 x + a_2 x^2 + a_3 x^3 ... + a_2n x^2n`; a green curl arrow into green quoted **`"diff. both side"`** with a wavy underline; white circled `1` then `a_1 + 2a_2 + 3a_3 + ... + 2n a_2n = n.3^n`; green the derivative itself `n (1+x+x^2)^(n-1) x (1+2x) = 1a_1 + 2a_2 x + 3a_3 x^2 + 4a_4 x^3 + ... + 2n a_2n x^(2n-1)`; white circled `2` then `a_1 - 2a_2 + 3a_3 - ... - 2n a_2n` left hanging; a white circle `x = 1` with an arrow into a **red rectangle** `n x 3^(n-1) x 3 = a_1 + 2a_2 + 3a_3 + ... + 2n a_2n`; a long yellow arrow curving down from the same derivative line, labelled yellow `x = -1`, into a second **red rectangle** yellow `-n = a_1 - 2a_2 + 3a_3 - ... - 2n a_2n`.
**DIBY:** none. **U:** none.

---
<a id="p15"></a>
## p15 · DOUBLE SIGMA PROBLEMS — the symmetric-function split · label: **Page No. 159**
**P:** clipboard icon + red banner **DOUBLE SIGMA PROBLEMS**; blue **Important Formula :** followed by yellow `Sum_{j=0}^{n} Sum_{i=0}^{n} f(i,j) = Sum_{i<j} Sum f(i,j) + Sum_{j<i} Sum f(i,j) + Sum_{i=j} Sum f(i,j)`.
**H:** pink beside the heading `# If f(i,j) -> Symmetric func^n of i & j.` with a green arrow across to a green worked column of admissible `f`'s, each ticked: `i^2 + j^2 ✓`, `nC_i + nC_j ✓`, `nC_i nC_j ✓`; pink hand-drawn **blobs** round the double sum on the left (labelled pink `Total`) and round the `i = j` sum on the right; two pink arrows from the `i<j` and `j<i` sums down to pink `equal`; from the `i = j` blob a pink arrow to pink `j -> i` then `= Sum_{i=m}^{n} f(i,i)`; bottom-left a **red rectangle** containing cyan `( Total - (i=j) ) / 2 = Sum_{i<j} = Sum_{j<i}` over a wavy rule.
**DIBY:** none. **U:** none.

---
<a id="p16"></a>
## p16 · IMPORTANT NOTE — the 4x4 grid behind the double sigma · label: — (chip only)
**P:** red chip **IMPORTANT NOTE**; green `# Dhyaan se Dekho`; yellow `Sum_{j=0}^{3} Sum_{i=0}^{3} (i^2 + j^2) =` followed by the full 16-term expansion printed as a 4 x 4 grid in white — rows j = 0..3, columns i = 0..3: `(0^2+0^2) (1^2+0^2) (2^2+0^2) (3^2+0^2)` / `(0^2+1^2) (1^2+1^2) (2^2+1^2) (3^2+1^2)` / `(0^2+2^2) (1^2+2^2) (2^2+2^2) (3^2+2^2)` / `(0^2+3^2) (1^2+3^2) (2^2+3^2) (3^2+3^2)`.
**H:** none — nothing written on the slide; the grid itself is the point (the diagonal `i = j` and the mirror symmetry across it).
**DIBY:** none. **U:** none.
