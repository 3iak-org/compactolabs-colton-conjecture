# Referee report: Colton threshold, π(n) ≤ 2T(n) for every n ≥ 10⁷

*`ref-colton`, opened by `dev`, 2026-10-30. Refereed:
`findings/colton-threshold.md` and its companions at `lead-colton` @
`116e4ff`. I wrote none of the work and took no instruction on the verdict
from its authors.*

## Verdict: **ACCEPT WITH CORRECTIONS**

I found no FATAL and no GAP. Every step of the threshold theorem holds:
the lemmas, the reductions, the cited inequality and its validity range, the
computed inputs and the arithmetic margin. I re-derived the steps rather than
re-reading them, and I recomputed the inputs and the arithmetic with my own
code. The corrections below are MINOR and only touch the text. None of them
changes the theorem, its threshold or its surplus.

On the evidence ladder, the theorem can go from "[T] candidate on [C]
inputs" to **[T] on [C] inputs, refereed 2026-10-30**. That is subject to
the limits in the last section. The main one: Dusart's (6.5) is a cited
[L] input, and this referee re-read it but did not re-prove it.

**Why the drop from 7.42·10¹³ to 10⁷ is real and not an error.** I checked
this first, and three independent facts agree:

1. Zelinsky's own chain with his own numbers crosses at 7.3094·10¹³
   (recomputed, PARI). With the true B it crosses at 2.8276·10¹³. So his
   threshold is set by his *method*, not by the truth.
2. The true quantity is far from tight at 10⁷. By an exact scan (my own
   linear sieve, one program), **T(n) − π(n)/2 ≥ 61,950.5 for every
   n ∈ [10⁷, 10⁸]**, with the minimum at n = 10⁷. The theorem claims only
   ≥ 3,616 there. So the claimed bound sits 17× below reality and is not
   suspiciously close to it.
3. The two things the file changes really do account for the gain:
   - keeping ln(n/a), with the exact Taylor expansion (Proposition A);
   - using small generator sets on finite pieces, where Lemma P needs no
     sign on c₀.

   Each piece's inequality has a margin I recomputed (table below).

## Findings

All are **MINOR**. They are cosmetic or about labelling, and they are listed
so the record is exact.

**M1. `findings/colton-threshold.md:153–166`: "Lemma 19 as printed is
false".**
- The counterexample is correct. I recomputed it: τ(360, 540, 900) =
  24, 24, 27; 180 ∈ G; true count 1 against printed bound 2.
- But the printed ω(n) is almost certainly a typo for ω(k). With ω(k) the
  bound is π(n/k) − ω(k), and that is exactly the file's "corrected Lemma
  19".
- Suggest saying "false as printed, true with ω(k) for ω(n) (presumably a
  typo)". Otherwise a reader may take it for a substantive error in
  Zelinsky. Nothing uses the lemma.

**M2. `findings/colton-threshold-check-rational.py:68`.** The docstring
cites "eq. (4.3)". The coefficients are defined at (3.2) of the findings
file. Stale cross-reference.

**M3. `findings/colton-threshold.md:9–19, 566–581` (§7.1, the shared-Arb
caveat).**
- This caveat is now discharged by this report. I recomputed N, β,
  max G(M) and L₀…L₆ for all three prefixes in **PARI/GP**, which shares no
  code and no library with either implementation, and no Arb:
  - the generators by `forfactored` over every a ≤ 28,653,696, testing
    2τ(a) | a directly;
  - π(g) by PARI's `primepi`;
  - the sums in 60-digit floating point.
- Agreement:
  - N, β and max G agree exactly at all three M;
  - the L_k agree with `colton-threshold-inputs.json` to
    |diff| ≤ 1.9·10⁻³⁰ (k ≤ 6, all M). That is far inside the
    L_abs_err = 10⁻²⁵ the checkers assume.
- Suggest citing this as the Arb-free second sum, and dropping "the referee
  may disagree" (line 579–580).

**M4. `findings/colton-threshold.md:111–112`: "the same pair is in the
abstract on page 1".**
- The arXiv *abstract page* for 1002.0442v1 does not contain (6.5).
- PDF page 1 may. I could not render it as an image here, so I did not
  check that sentence.
- Theorem 6.9, eq. (6.5), with the ranges x ≥ 599 (lower) and x > 1
  (upper) and the "p₂₅₈ = 1627" remark: I confirmed all of it myself in
  the arXiv PDF text (fetched 2026-10-30, extracted with mutool).
- Either fix "abstract" to "PDF p. 1" if that is what was meant, or drop
  the clause.

**M5. `findings/colton-threshold.md:586–589` (Dusart provenance).**
- The theorem's one external input is read only in an unrefereed preprint.
  That is honestly stated.
- The same two inequalities are widely attributed to Dusart 1999
  (Math. Comp. 68) and to the 2018 Ramanujan J. version. **I did not read
  either** (§ Limits).
- Not a gap in the proof. But a `lit-` chat should read the refereed
  statement before anything leaves the repo, because the [T] stands on it.

## What I checked and found sound (do not re-check)

**Mathematics, re-derived from the first line:**

- **Lemma 18, all four directions.** The (ii)⇒(i) step uses p > 2a ≥ 2τ(a),
  so gcd(p, 2τ(a)) = 1. Sound.
- **Lemma 20.**
  - (a) p > g(a) ⇒ p ∤ a, then Lemma 18.
  - (b) Disjointness: g(ap) = p, because every prime factor of a is < p.
  - (c) The count |E_a ∩ [1, n]| = max(0, π(n/a) − π(g(a))).

  Sound. (1.1) follows.
- **Proposition A.** Valid because:
  - min G = 8, so ℓ > 0;
  - n/a ≥ 599 gives t = ℓ/u < 1.

  Both series have nonnegative terms, so partial sums are lower bounds. The
  reindexing m = k+1 gives coefficient ℓᵐ + mℓ^{m−1} at u^{−m−1} for
  m = 0…J; the second series is truncated at k = J−1, consistently. Summing
  over S gives (n/u) Σ (L_m + m L_{m−1}) u^{−m}. Sound.
- **Proposition B.**
  - Dusart's upper bound at x = n > 1 gives π(n)/2 ≤ (n/u)(½ + 0.6381/u),
    and 1.2762/2 = 0.6381 exactly.
  - So c₀ = L₀ − ½ and c₁ = L₁ + L₀ − 0.6381.

  Sound.
- **Lemma P.**
  - g_S is nonincreasing because c₁…c_J > 0.
  - x/ln x is increasing for x ≥ e.
  - The product step needs g_S(u) ≥ 0, which follows from
    g_S(u) ≥ g_S(ln q) ≥ 0.
  - The validity condition is needed for every n ∈ [p, q], and it follows
    from p ≥ 599·max S.

  Sound.
- **Lemma Q.** d/du(e^u u^{−m−1}) ≥ 0 for u ≥ m+1. Needs c_m ≥ 0 for all
  m, i.e. L₀ ≥ ½, and ln n_f ≥ J+1 = 5. Sound.
- **Coverage.** Closed pieces [10⁷, 3·10⁷], [3·10⁷, 10⁸], [10⁸, 10⁹],
  [10⁹, 10¹²] and [10¹², ∞) cover every n ≥ 10⁷, inclusive of 10⁷.
- **Validity points** (599·max S):
  - 9,984,132 ≤ 10⁷;
  - 99,999,456 ≤ 10⁸;
  - 17,163,563,904 ≤ 10¹².
- **max G(M).** 16,668 = 2²·3²·463, with τ = 18. The other two maxima are
  confirmed by PARI.
- **Cut-offs.** ⌊10⁷/599⌋ = 16,694 and ⌊10⁸/599⌋ = 166,944.
- **Boundary.** The theorem covers n ≥ 10⁷ inclusive. The finite check
  must cover n ≤ 10⁷ − 1, as §7.6 says.

**Inputs and arithmetic, recomputed with my own code**
(`referee/colton-threshold/`):

| piece | S | g_S(ln q) | (p/ln p)·g_S(ln q) | β | surplus | margin on β | uniform L_k overstatement survivable |
|---|---|---|---|---|---|---|---|
| [10⁷, 3·10⁷] | G(16,694) | 0.0204005864 | 12,656.946 | 7,453 | 5,203.946 | ×1.698 | 1.50% |
| [3·10⁷, 10⁸] | G(16,694) | 0.0063527350 | 11,069.599 | 7,453 | **3,616.599** | ×1.485 | **0.384%** |
| [10⁸, 10⁹] | G(166,944) | 0.0788531163 | 428,068.416 | 346,644 | 81,424.416 | **×1.235** | 2.46% |
| [10⁹, 10¹²] | G(166,944) | 0.0250288770 | 1,207,767.019 | 346,644 | 861,123.019 | ×3.484 | 3.26% |
| [10¹², ∞) | G(28,653,696) | — (Lemma Q) | 7,117,431,709.2 | 3,348,506,095 | 3.7689·10⁹ | ×2.126 | c₀ ≥ 0 survives 1.57% |

- Every coefficient c₀…c₄ agrees with the file's table to its 12 digits.
- The file's own margin claims are confirmed exactly:
  - "β understated by up to 23%", binding on [10⁸, 10⁹];
  - "L_k overstated by up to 0.38%", binding on [3·10⁷, 10⁸].
- The minimum surplus is 3,616.599 ≥ 3,616, so the stated constant holds.

**The checkers** (read, not just run):

- Both lower the L_k by the error bound (rational) or carry it as a ball
  (Arb). That is the conservative direction, since every c_m is
  increasing in every L_k.
- Both use an *upper* bound on ln p and ln q, which is also conservative:
  p/ln p falls and g_S(ln q) falls.
- The rational checker certifies r ≥ ln n by an exact Taylor partial sum
  of e^r reaching n. That is valid, since all terms are positive.
- They are genuinely different arithmetic. They share the transcription of
  the statements, and I checked those statements independently above.

**Independence of the generator lists:**

- `search/generators/gen.c` is a segmented trial-division τ-sieve in C,
  with π from a bit sieve.
- `verify/generators/gen.py` is a signature-enumeration construction in
  Python/PARI, with π from PARI.
- These are different methods with no shared code.
- Mine (PARI `forfactored`) is a third method. All three agree on N and β.

**Zelinsky §2 numbers, recomputed:**

- R = 8,685,500,885, and R + 6π(M_Z/128) = 8,685,620,465.
- The printed formula as written gives 1,785,485.
- Crossing 7.30936·10¹³ with his A and B, and 2.82759·10¹³ with the true
  B = 3,348,920,075.
- Margin at 7.42·10¹³: 1.3205·10⁸.
- Cofactors c < 128 with 4τ(c) | c are exactly {36, 80, 96}.

All match the file.

**Sanity values:**

- T(10⁷) = 394,240, π(10⁷) = 664,579, and T(10⁸) = 3,558,181. These match
  §6.
- Dusart (6.5) at every jump of π on [599, 10⁸] (PARI, 50 digits): minimum
  slack 0.014481 (lower) and 0.002878 (upper). These match §6.3. They are
  observed, not proof.

## Limits: what I could NOT check

1. **Dusart (6.5) itself.**
   - I confirmed the statement and validity ranges in the arXiv preprint.
     I did not check its proof, and I read neither refereed version (1999
     Math. Comp.; 2018 Ramanujan J.).
   - My numerical check reaches 10⁸. The proof uses the lower bound at
     x = n/a up to 1.25·10¹¹ on the finite pieces, and at every x ≥ 599
     in the tail, and the upper bound at all n ≥ 10⁷. For those it rests
     entirely on Dusart.
   - This is the one external dependency of the theorem.
2. **The exact scan on [10⁷, 10⁸] is one program** (my linear sieve). It
   is a sanity check of the conclusion, not part of the proof, and not [C].
   I did not extend it past 10⁸.
3. **Completeness of `verify/generators/gen.py`'s pruning** (its README
   proofs) was not refereed. It does not matter for the theorem: two other
   methods (the τ-sieve and my `forfactored`) enumerate every integer
   ≤ 28,653,696 and agree with it. But the pruning proofs themselves are
   unchecked.
4. **Not checked:**
   - the scratch claims in §3 (≈4.3·10¹¹ with Proposition A alone) and in
     §4 "Alternatives" (floor ≈4·10⁶);
   - the Z(n) and analytic-bound tables in §6.1–6.2, apart from the
     T and π values;
   - Lemma 18's brute-force sanity run.

   None is used by the theorem.
5. **Zelinsky's paper** was not read by me. The quotations of his lemmas
   and numbers are taken from the file and from `literature/colton.md`.
6. **The finite range n < 10⁷** is outside this report, as briefed.
   Colton's conjecture for all n is **not** established until that strand
   is done and refereed.
7. **No Lean.** This is a refereed written proof, not [F].

## Reproduce

All scripts are in `referee/colton-threshold/`. Run them with the system
`gp` (PARI) and `gcc`.

```
cd referee/colton-threshold
gp -q -s 2G gen.gp > gen-out.txt     # 22 s: N, beta, max G, L0..L6 at the three M (forfactored)
# Ls.gp is gen-out.txt reformatted as gp vectors (committed)
gp -q ineq.gp                        # coefficients, the five inequalities, margins
gcc -O2 -o scan scan.c && ./scan 100000000 10000000   # 2 s: exact min of T(n)-pi(n)/2 on [1e7,1e8]
gp -q -s 1G misc.gp                  # 1 min: cofactors, Lemma 19 numbers, Dusart sanity to 1e8
gp -q z.gp                           # Zelinsky section 2 numbers
```
