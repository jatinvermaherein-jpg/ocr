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
