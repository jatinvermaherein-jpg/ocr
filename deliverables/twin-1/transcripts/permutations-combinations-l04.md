# Permutations & Combinations — Lecture 04 (Class Notes) · Twin 1 transcript
Source: `Permutations & Combinations 04 Class Notes.pdf` (43 pages, image-only, no text layer). Every page below was read visually from the render in `work/pages/pc04_pNN.png`. Page keys are PDF page numbers; the printed `Page No.` label, when present, is quoted in the header line. Math is written in ASCII (`nC_r`, `7P4`) per F-19.

<a id="p01"></a>
## p01 · Course title card — Arjun JEE 2027, Lecture 04 · label: — (PW roundel)
**P:** poster art, giant yellow **ARJUN** cracked by a silver arrow, white/silver **2027**; black banner **Lecture –04** | **Mathematics**; on the amber panel **PERMUTATIONS AND COMBINATIONS** (three lines, AND small and centred); maroon capsule **By– Sachin Jakhar Sir**. Teacher photographed right in a black "Physics Wallah" polo, three-finger salute; compass + pencil props bottom-left.
**H:** none. **DIBY:** none. **U:** none.

---
<a id="p02"></a>
## p02 · Topics to be covered · label: — (chip only)
**P:** yellow **Topics** + white script *to be covered*; red tiles `A` **Formula for P & C** (red rectangle), `B` **Problems on Combination(Selection)** (red rectangle, no space before the bracket), `C` **Problems on Permutation (Arrangement)** (red rectangle), `D` — tile printed with **no text**; 3-D pencil-character leaning on a silver question mark.
**H:** none. **DIBY:** none. **U:** none — the empty `D` tile is the deck-wide template defect already logged (U-16, seen in L04 p03 and L05 p02).

---
<a id="p03"></a>
## p03 · H.W. Discussion — section break · label: — (chip only)
**P:** black slide, white **H.W. Discussion** inside a red rectangle.
**H:** none. **DIBY:** none. **U:** none.

---
<a id="p04"></a>
## p04 · Question — 4-digit numbers from 1…7, matrix match (C1/C2) · label: — (chip only)
**P:** red chip **Question**; **Using the digits** `1, 2, 3, 4, 5, 6, 7` **(digits printed green) a number of 4 different digits is formed. Find** — two yellow column heads `C1` (left, over the questions) and `C2` (right, over the values); left items `(1) How many number are formed?`, `(2) How many numbers are exactly divisible by 2?`, `(3) How many numbers are exactly divisible by 25?`, `(4) How many of these are exactly divisible by 4?`; right column `(A) 840  (B) 200  (C) 360  (D) 40  (E) 180`.
**H:** the matching is written as single letters at the left edge, pink/cyan: `A` against (1), `C` against (2), `D` against (3) (with a yellow tick on the item number), `B` against (4) (with a pink tick). Working below, numbered in circles: yellow `③ 20 <- _ _ 25` with `5` and `4` written above the two blanks, and `20 <- _ _ 75` (i.e. 2 endings x 5·4·... = 20 each -> 40 = D); pink `④ 20 <- _ _ 12, _ _ 16, _ _ 24, _ _ 32, _ _ 36, _ _ 52, _ _ 56` with a pink column at right `_ _ 64, _ _ 72, _ _ 76`, and `5`, `4` above the blanks (10 admissible endings x 20 = 200 = B). Items (1) and (2) get no working on this slide.
**DIBY:** none. **U:** 1 — the match-the-following layout prints five values for four questions, so `(E) 180` is a decoy; the handwritten letters give 1->A (7P4 = 840), 2->C (360), 3->D (40), 4->B (200), which is arithmetically self-consistent.
<a id="p05"></a>
## p05 · Question [JEE Mains–2023] — five-digit numbers > 40000, divisible by 5 · label: — (chip only)
**P:** red chip **Question [JEE Mains–2023]**; **The number of five-digit numbers, greater than 40000 and divisible by 5, which can be formed using the digits** `0, 1, 3, 5, 7 and 9` **(digits printed green) without repetition, is equal to**; tiles `A 132`, `B 120`, `C 72`, `D 96`.
**H:** cyan slashes struck through the printed `0` and the printed `5` in the digit list; cyan case work — `5 _ _ _ 0` with `4`, `3`, `2` written above the three blanks, brace to `24` + tick; `7 _ _ _ [box]` with `4 x 3 x 2` written small under the blanks and `2 opt.(0/5)` to the right, brace to `48` + tick; `9 _ _ _ [box]`, brace to `48` + tick — 24 + 48 + 48 = **120**, and **B** carries the cyan tick. Top right, cyan: `81%` inside a circle, double-underlined (the success-rate tag habit, F-13).
**DIBY:** none. **U:** none.

---
<a id="p06"></a>
## p06 · Question [JEE Mains–2022] — 4-digit numbers between 1000 and 3000 divisible by 4 · label: — (chip only)
**P:** red chip **Question [JEE Mains–2022]**; **Numbers are to be formed between 1000 and 3000, which are divisible by 4, using the digits** `1, 2, 3, 4, 5 and 6` **(green) without repetition of digits. Then the total number of such numbers is** `_____`.
**H:** pink `30` written into the blank and ringed in pink; the printed digit `1` in the list struck through in pink; pink partial enumeration in a column — `1 _ 24`, `1 _ 32`, `1 _ 36` (the leading `1` underlined each time); at right pink `Done!` with a double underline and a small tail stroke after it.
**DIBY:** none. **U:** 1 — only the `1 _ _ _` family is written out; the `2 _ _ _` half of the count (and hence the route to 30) is not on the slide, so the ringed `30` is the sole evidence for the answer.

---
<a id="p07"></a>
## p07 · Question — MIRACLE with vowels only in odd positions · label: — (chip only)
**P:** red chip **Question**; **Find the number of words that can be formed using all the letters of the word 'MIRACLE' such that the vowels occupy only the odd positions.** (`MIRACLE` yellow-highlighted, `odd positions` green); tiles `A 576`, `B 144`, `C 288`, `D 720`.
**H:** white curve from `MIRACLE` to the split `A, I, E` (vowels) and `M, R, C, L` (consonants); cyan position numbers `1 2 3 4 5 6 7` over a row of seven pink slots with cyan `*` on the odd positions 1, 3, 5, 7. Four pink patterns ringed in magenta and numbered: ① `V _ V _ V _ _`, ② `V _ _ _ V _ V`, ③ `V _ V _ _ _ V`, ④ `_ _ V _ V _ V`; on row ① the per-slot choice counts are written under the letters (`3 4 2 3 1 2 1`, the V's circled, the consonant slots ringed) and a white brace leads to `3! x 4! = 144`, with a ditto mark `"` repeated against rows ②③④. Below a white rule: the cursive marker `fnf = 144 x 4` and `= 576`. **A** carries a white tick and a strike across the tile.
**DIBY:** none. **U:** 1 — the cursive `fnf` before `= 144 x 4` is the same unresolved mark seen in the Binomial series (U-02; re-read in F-34). Here it behaves as a "total" sign; still not decoded, so it is transcribed rather than translated.

---
<a id="p08"></a>
## p08 · FORMULA's FOR P & C — Theorems 01–03 · label: **Page No.128**
**P:** clipboard icon + red banner **FORMULA's FOR P & C**; three yellow headings with white italic statements: **Theorem-01 :** *Number of ways of arranging n different things in a line =*; **Theorem-02 :** *Number of ways of arranging r things taken out of n-different things in a line =*; **Theorem-03 :** *Number of ways of selecting r things out of n-different things =*. The three right-hand sides are left blank in print.
**H:** white `n!` after Theorem 01; orange after Theorem 02 `nP_r = n!/(n-r)!`; orange after Theorem 03 `nC_r = n!/(r!(n-r)!)`; white `Permut.` with a hook from the word *arranging* in Theorem 02, orange `Comb.` with a hook under *selecting* in Theorem 03 (the wavy underline there is printed orange).
**DIBY:** none. **U:** none — the label prints `Page No.128` with no space after `No.`, unlike the Binomial module's `Page No. 154`.
<a id="p09"></a>
## p09 · RAPID FIRE ROUND — four fill-ins on nCr / nPr · label: — (chip only)
**P:** red chip **RAPID FIRE ROUND**; **Answer the following Questions:** then `1. Value of 10C3 = ____`, `2. If 12Cx = 12C7 then possible value(s) of x = ____` (item 2 enclosed in a printed **red rectangle**), `3. Value of 7P3 = ____`, `4. (True/False) : nC0 = nCn = 1` (the identity printed cyan).
**H:** pink `120` in blank 1 with a white tick and a pink slash through the printed number `1.`; pink `7, 5` in blank 2 with an orange comma between them; cyan `210` in blank 3; a cyan tick under the printed word *True* in item 4. Working: green `(i) 10C3 = 10!/(7! 3!) = (10.9.8.7 ... 1)/(7!.3!...) = 120` with `3 4` written above the cancelled run and a pink circle-and-slash over the struck `7 ... 1`; blue `7P3 = 7!/4! = (7.6.5.4!)/4! = 210` (the cancelled factorials struck in blue); orange, right half: `② 12Cx = 12C7` with `x` and `7` each ringed, an arrow out to a ringed `x = 7`, and below `x + 7 = 12` in an orange oval around `x = 5`.
**DIBY:** none. **U:** none.

---
<a id="p10"></a>
## p10 · board note — the nCx = nCy rule · label: — (no header, board slide)
**P:** none — pure board page.
**H:** pink `Notes.` inside a hand-drawn circle, a curved pink arrow out of it to `Note:-` (single-underlined); then `If.` and a **red rectangle** round `nC_x = nC_y`, a white/pink `=>`, a second red rectangle round `x = y` (the `y` with a long descender), printed-style pink `OR`, and a third red rectangle round `x + y = n`.
**DIBY:** none. **U:** none. (This is the P&C twin of the Binomial module's Property 01(ii) rule card, L05 p12.)

---
<a id="p11"></a>
## p11 · Question — if 2nP4 = 396 x nP2 (tagged H.W. / DIBY) · label: — (chip only)
**P:** red chip **Question**; **If** `2nP4 = 396 x nP2`**, then the value of** `n`**, is** (the binomials green, `n` cyan); tiles `A 4`, `B 5`, `C 6`, `D 7`. No printed answer key.
**H:** blue, upper right: `H.W.` double-underlined, and under it `(80% DIBY)` inside blue brackets.
**DIBY:** YES — handwritten tag only (no printed `# DIBY-nn`), internal ID `BT`-style key is `PC-L04-P11-DIBY(HW)`. **U:** 1 — the item is assigned and never solved in this file (same pattern as L05 p23's `90% DIBY` + `H.W.`, F-18); no answer is recoverable from these pages.

---
<a id="p12"></a>
## p12 · RAPID FIRE QUESTION — 6 boys & 5 girls, four selection counts · label: — (chip only)
**P:** red chip **RAPID FIRE QUESTION**; **In a class there are** `six boys` **&** `five girls`**, then:** — the two phrases green and each inside a printed **red rectangle**; four cyan sub-questions, each with a handwritten tick: `(i) Number of ways of selecting 5 students.` (yellow tick), `(ii) Number of ways of selecting 3 girls & 2 boys.` (pink tick), `(iii) Number of ways of selecting 5 students with atleast 2 boys.` (green tick), `(iv) Number of ways of selecting 5 students with atmost 2 girls.` (green tick).
**H:** yellow at top right `Total = 11 stds.` with `11` ringed; a yellow arrow from (i) to yellow `11C5` + a yellow tick; pink `(ii)` with `5G & 6B` and two arcs down into a red rectangle holding pink `5C3 x 6C2`; cyan `(iii)` with yellow case labels over four red rectangles — `2B,3G` -> `6C2 x 5C3`, `3B,2G` -> `6C3 x 5C2`, `4B 1G` -> `6C4 x 5C1`, `5B` -> `6C5`; green `(iv)` under the row with arrows pointing up at the same boxes, labelled `3B 2G + 4B 1G + 5B 0G`; at the left of the (iii) row, green the cursive marker `fnf.` before the first `=` (the same unexplained mark as U-02/F-34, here plainly used as a "therefore/total" sign).
**DIBY:** none (RAPID FIRE QUESTION carries no numbered tags, per F-17). **U:** 1 — no numeric evaluation is written for (ii)–(iv); only the expressions are set up.
<a id="p13"></a>
## p13 · RAPID FIRE QUESTION — arranging 3 boys & 2 girls with end-position and alternation rules · label: — (chip only)
**P:** red chip **RAPID FIRE QUESTION**; **In a class there are** `six Boys` **&** `five Girls`**, then:** (both green); `(i) Number of ways of arranging 3 Boys & 2 Girls in a line such that end positions occupied by girls.`, `(ii) ... end positions occupied by boys.`, `(iii) ... boys and girls are alternate.` — each item carrying a hand tick (pink on (i), cyan on (ii), cyan on (iii)).
**H:** pink arrow from (i) down to pink `(i)` `selectn` above `6C3 × 5C2 ×`, then yellow `Arrang.` above a slot row `( ) _ _ _ ( )` with `2 × 3 × 2 × 1 × 1` written beneath and, under that, cyan `B1B2B3 G1G2` with a yellow hook grouping the girls; the result in a **red rectangle**, yellow `= 6C3 × 5C2 × 12`. Right half, pink `(ii) 6C3 × 5C2 × 36` with pink `selectn` (wavy) over the first factor and cyan `arrg.` over `36`, and a cyan slot row `(−)_ _ _(−)` with cyan `3 × 3 × 2 × 1 × 2` under it. Cyan `(iii) 6C3 × 5C2` with a large cyan loop carrying the pattern `B G B G B` over slots `3 × 2 × 2 × 1 × 1` and `×12` inside the loop; the alternating string `B G B G B` boxed in red with a green tick, and the rejected `G B G B B` below it in green with a green cross.
**DIBY:** none. **U:** none.

---
<a id="p14"></a>
## p14 · board — the unrestricted case, and why 11P5 is wrong · label: — (no header, board slide)
**P:** none — pure board page.
**H:** orange `11 stds.` above an orange oval holding green `6B, 5G`; a long orange arc from that oval down-left into a large orange circle containing `11P5 = 11!/6!`, and an orange `×` written under the circle (the route marked wrong). Centre, green `# no. of ways of arranging 3B, 2G in a line:` with `arranging` ringed in pink and a green wavy rule beneath; below it pink `selectn × arrang.` over a **red rectangle** holding pink `6C3 × 5C2 × 5!` with a pink tick at the right.
**DIBY:** none. **U:** none.

---
<a id="p15"></a>
## p15 · RESRTICTED SELECTION EXAMPLE — particular / specific boys · label: **Page No.129**
**P:** red chip **RESRTICTED SELECTION EXAMPLE** — the word is printed with the letters transposed, `RESRTICTED` for RESTRICTED; yellow **5 boys** white **are selected out of** green **9 boys** white **such that :**; cyan `(i)` **Two** `particular` **(inside a printed red rectangle) boys will not serves together.** and cyan `(ii)` **Two specific boys will only serves together.** (both print the ungrammatical "serves"; (ii) has a double space before it).
**H:** pink arrow from `(ii)` into a red rectangle holding pink `already fixed`; centre, a red rectangle `9 Boys` with two green branch arrows to green `A, B` and yellow `7 Boys.`; right, white `(i) 9C5 − (7C3)` with green ticks/crosses above `A B` and the phrase `OR` under it, then three case trees in green (`A✓ B✕` -> `7C4`, `A✕ B✓` -> `7C4`, `A✕ B✕` -> `7C5`) feeding cyan `(i) = (7C4 + 7C4 + 7C5)`, and below cyan `(ii) = (7C3 + 7C5)` with its own two trees (`AB` both ticked -> `7C3`; both crossed -> `7C5`); a long white arrow from the `9C5 − (7C3)` line down into the cyan (i) line, labelled `equal` with a double underline.
**DIBY:** none. **U:** 2 — (a) printed chip typo `RESRTICTED`, transcribed as printed (same family as `IVRTTATIONAL`, `ever`); (b) the printed grammar errors `will not serves` / `will only serves together` are kept verbatim.

---
<a id="p16"></a>
## p16 · FORMATION OF TEAM / COMMITTEE — JEE (Adv.)–2016 Paper-1 debate club · label: **Page No.129**
**P:** clipboard icon + red banner **FORMATION OF TEAM / COMMITTEE**; second red chip **Question [JEE (Adv.)–2016, Paper–1]**; **A debate club consists of 6 girls and 4 boys. A team of 4 members is to be selected from this club including the selection of a captain (from among these 4 members) for the team. If the team has to included at most one boy, then the number of ways of selecting the them is ________.** (the slide prints "has to included" and "selecting the them"); eight printed underscores for the answer.
**H:** cyan `D.C.` over a cyan circle containing `6G / 4B`; green arrow to green `4 members`; orange arrow to the two orange case labels `1B, 3G` and `4G` above orange `4C1 × 6C3 + 6C4`; cyan `(4 x 20 + 15) x 4 = ` with **`380` ringed in cyan**; the captain factor written cyan as `× 4C1` with an empty cyan **cloud** outline above it and a cyan arrow down from the cloud into that factor.
**DIBY:** none. **U:** 1 — the empty cloud is an unfinished doodle/label, not a value; nothing is written inside it on any later page.

---
<a id="p17"></a>
## p17 · Question [JEE Mains–2019] — committee of 11, m and n · label: — (chip only)
**P:** red chip **Question [JEE Mains–2019]**; **A committee of 11 members is to be formed from 8 males and 5 females. If** `m` **(cyan) is the number of ways the committee is formed with at least 6 males and** `n` **is the number of ways the committee is formed with at least 3 females, then**; tiles `A m = n = 68`, `B m + n = 68`, `C m = n = 78`, `D n = m − 8`.
**H:** cyan, right of the question: `H.W.` written inside a cyan oval with a double underline and a small ring at each side — assigned as homework; nothing else is written on the slide and no answer key is printed.
**DIBY:** none (this item is tagged only `H.W.`, without the DIBY wording, so no register row). **U:** 1 — unresolved in this file; check the next lecture's H.W. discussion before treating it as answered.

---
<a id="p18"></a>
## p18 · Question [JEE (Adv.)–2018, Paper–2] — α1 for 3 boys & 2 girls · label: **Page No.129**
**P:** red chip **Question [JEE (Adv.)–2018, Paper–2]**; **In a high school, a committee has to be formed from a group of 6 boys** `M1, M2, M3, M4, M5, M6` **and 5 girls** `G1, G2, G3, G4, G5` **(both lists green);** cyan `(i)` **Let** `α1` **be the total number of ways in which the committee can be formed such that the committee has 5 members, having exactly 3 boys and 2 girls.**
**H:** a cyan tick against `(i)`; centre, cyan `(3B 2G)` above a **red rectangle** holding cyan `α1 = 6C3 × 5C2` — only part (i) is on this slide.
**DIBY:** none. **U:** none.
