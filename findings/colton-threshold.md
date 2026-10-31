# Colton's conjecture: π(n) ≤ 2T(n) for every n ≥ 10⁷

*`thm22`, opened by `lead-colton`, 2026-10-30/31. Branch `agent/thm22`.
Companions: `colton-threshold-inputs.json` and
`colton-threshold-inputs-verify.json` (the named computed inputs, one file per
[C] implementation, built by `colton-threshold-inputs-build.py`),
`colton-threshold-check-rational.py` and `colton-threshold-check-arb.py`
(two independent checkers of the finitely many inequalities the proof
reduces to).*

**Referee (2026-10-30, `ref-colton`): ACCEPT WITH CORRECTIONS.** No FATAL
and no GAP. The report is `referee/colton-threshold.md` (PR #24 into `dev`).
Corrections M1–M5 were applied on 2026-10-31. They are text only: the
theorem, its threshold and its surplus are unchanged.

**Status (2026-10-31): [T] on [C] inputs, refereed.** Every "[T]" label in
§§1–4 is a step the referee re-derived. The one external input, Dusart
(6.5), is [L] and was not re-proved (§7.3).

The computed inputs come from two implementations that agree on every value:

- `comp-generators` @ `4074e69`: a segmented τ-sieve in C;
- `check-generators` @ `b961da4`: constructive enumeration by exponent
  signature, in Python/PARI, written without reading the first.

Their generator lists have identical sha256 at every checkpoint. They agree
on N, β, max G and max a·g exactly, and on L₀…L₆ to every printed digit (30).
Both sum the L_k with the same ball-arithmetic library, Arb. That shared
component is discharged by the referee's own recomputation in PARI/GP (§7.1),
which uses no Arb and no shared code.

## The answer

> **Theorem (threshold), [T], refereed (ref-colton, 2026-10-30).** For every integer
> n ≥ 10⁷,
>
> T(n) − π(n)/2 ≥ 3616.
>
> In particular π(n) ≤ 2T(n) for every n ≥ 10⁷.

Notation:

- T(n) = #{k ≤ n : τ(k) | k}, where τ is the number of divisors.
- π is the prime-counting function.

Plain consequence: **N\* = 10⁷.** Zelinsky's published threshold is
7.42·10¹³ (2002, Theorem 22). Colton's conjecture therefore reduces to an
exact check of every n < 10⁷. That check is seconds of computation, and it
belongs to `comp-range` / `check-range`, not to this file.

The proof uses five things:

- **Zelinsky's p-generator construction.** Lemmas 18 and 20 are proved here
  in full. His Lemma 19 is false as printed; it is corrected and proved
  here, but it is not used.
- **One cited inequality pair:** Dusart 2010, eq. (6.5).
- **Named computed inputs for three prefixes G(M) of the generator list.**
  For each prefix: the sums L₀…L₄, where L_k = Σ (ln a)^k / a; β = Σ π(g(a));
  and max G(M).
- **Two elementary monotonicity lemmas** (P and Q, §3).
- **Five explicit numerical inequalities.** Each is checked by two
  checkers that share no code and no method.

### What would have to be true for this to be wrong

1. **Dusart (6.5) fails somewhere.** It would have to fail at some real
   x ≥ 599 for the lower bound, or at some x > 1 for the upper bound. I READ
   it in arXiv:1002.0442v1, an unrefereed preprint (§0). I did not read the
   published version (Ramanujan J., 2018). As a sanity check, I tested (6.5)
   at every jump of π on [599, 2·10⁹] with one program. It holds, with
   minimum slack 0.0145 (lower) and 0.0029 (upper). This is observed, not
   proved.
2. **The computed inputs are wrong by more than the margins allow.** The
   proof survives:
   - β understated by up to 23%;
   - all L_k overstated together by up to 0.38%, relative.

   The binding piece for β is [10⁸, 10⁹]; for the L_k it is
   [3·10⁷, 10⁸]. For comparison:
   - the checkers use the lower endpoints of rigorous enclosures, whose
     radii are below 10⁻²⁵;
   - three programs agree to every printed digit (≥ 29): the two [C]
     implementations and my scratch.

   A *systematic* error would get past this. Examples: the wrong set
   definition, ≤ M versus < M, or log₁₀ instead of ln. A second independent
   implementation is what rules that out. It has now reported
   (`check-generators` @ `b961da4`), and it agrees.
3. **An error in the reductions** (Proposition A, Proposition B, Lemma P or
   Lemma Q, §3). Each is a few lines, written out below.
4. **An error in Lemma 20's disjointness.** That is three lines (§1).
5. **Both checkers wrong in the same direction.** They share no code: one
   uses exact rationals with Taylor-certified log bounds, the other Arb ball
   arithmetic. The five inequalities are also given with all their
   intermediate values in §4, so they can be checked with a calculator.

## 0. Notation and cited input

- τ(k) is the number of divisors of k, and ω(k) the number of distinct prime
  factors. For a ≥ 2, g(a) is the largest prime factor.
- π(x) = #{p ≤ x prime}, for real x.
- T(n) = #{1 ≤ k ≤ n : τ(k) | k}. Elements of this set are **tau numbers**
  (refactorable numbers).
- **G = {a ≥ 1 : 2τ(a) | a}**, and **G(M) = G ∩ [1, M]**.
  - Every a ∈ G is even, since 2 | 2τ(a) | a. So 1 ∉ G and g(a) is defined.
  - The smallest elements (with g) are 8 (2), 12 (3), 36 (3), 72 (3),
    80 (5), 96 (3), 128 (2), 180 (5), 240 (5), 252 (7), …
- For finite S ⊂ G and k ≥ 0:
  - **L_k(S) = Σ_{a∈S} (ln a)^k / a**, with L_{−1} := 0. L₀ is Zelinsky's
    "A".
  - **β(S) = Σ_{a∈S} π(g(a))**. Zelinsky's B is β(S) + |S|.

**Cited: Dusart 2010.** Pierre Dusart, *Estimates of some functions over
primes without R.H.*, arXiv:1002.0442v1 (2010), **Theorem 6.9, eq. (6.5)**:

  (x/ln x)(1 + 1/ln x) ≤ π(x)  for real x ≥ 599,
  π(x) ≤ (x/ln x)(1 + 1.2762/ln x)  for real x > 1.

Status:

- [L, READ 2026-10-30: Theorem 6.9, eq. (6.5), page 9 of the arXiv PDF.
  The referee independently confirmed the statement and both validity
  ranges in the same PDF.]
- The same pair is also attributed to the published version, Ramanujan
  J. 45 (2018) 227–251. That version was not read, and no published theorem
  number is cited (§7.3).
- Dusart notes that 1.2762 "is chosen for x = p₂₅₈ = 1627". My sanity run
  finds the minimum upper slack at that prime.
- Nothing else from the prime-number literature is used. The sharper (6.7)
  of the same theorem is not used: I did not need it, and its lower-bound
  range (88,783) may differ in the published version.

## 1. Zelinsky's lemmas (published numbering), proved

Source: Zelinsky, *Tau numbers: a partial proof of a conjecture and other
results*, J. Integer Seq. 5 (2002), Art. 02.2.8, §2. [L, READ 2026-10-30:
TeX source and published PDF from cs.uwaterloo.ca/journals/JIS/VOL5/Zelinsky/.
I checked that the PDF numbers these Lemma 18–21 and Theorem 22.]

**Lemma 18** [T, 2026-10-31]. Zelinsky's statement:
"2 | n/τ(n) iff for any prime p ∤ n, np is a tau number". Proof "left to the
reader". For a ≥ 1 the following are equivalent:

- (i) 2τ(a) | a;
- (ii) for every prime p ∤ a, the number ap is a tau number;
- (iii) a is a tau number and (ii) holds. This is Zelinsky's definition of a
  *p-generator*.

*Proof.*

- **(i) ⇒ (ii).** Let p ∤ a. Since gcd(a, p) = 1 and τ is multiplicative,
  τ(ap) = τ(a)τ(p) = 2τ(a). By (i), 2τ(a) | a | ap.
- **(ii) ⇒ (i).** Take a prime p > 2a; infinitely many exist. Then p ∤ a.
  By (ii), τ(ap) = 2τ(a) divides ap.
  - τ(a) ≤ a, because every divisor of a lies in [1, a]. So
    0 < 2τ(a) ≤ 2a < p.
  - Hence the prime p does not divide 2τ(a), so gcd(2τ(a), p) = 1.
  - Then 2τ(a) | ap gives 2τ(a) | a.
- **(i) ⇒ (iii).** τ(a) | 2τ(a) | a, so a is a tau number. Together with
  (i) ⇒ (ii), this gives (iii).
- **(iii) ⇒ (ii)** is trivial. ∎

So "p-generator" = element of G. Sanity check, not proof: brute force over
a ≤ 3000 and primes p < 5000 finds no disagreement between (i) and (ii)
(observed, 2026-10-30).

**Lemma 19 is false as printed, and true with ω(k) in place of ω(n)** [T].
Zelinsky prints: "Let k be a p-generator. The number of tau numbers ≤ n of
the form kp is at least π(n/k) − ω(n)". Proof "left to the reader".

- The ω(n) is presumably a typo for ω(k).
- With ω(k), the statement is the corrected Lemma 19 below, and that is
  the statement proved here.
- So this is a misprint, not a substantive error in Zelinsky. Nothing in
  this file uses the lemma either way.

The counterexample below is to the statement as printed.

Counterexample: k = 180, n = 1024.

- 180 = 2²·3²·5, so τ(180) = 18 and 36 | 180. Hence 180 ∈ G.
- 1024 = 2¹⁰, so ω(1024) = 1. Also π(1024/180) = π(5.69…) = 3.
- So the printed bound is 3 − 1 = 2.
- The candidates kp ≤ 1024 are 360, 540 and 900:
  - τ(360) = 24, and 24 | 360;
  - τ(540) = 24, and 540/24 = 22.5;
  - τ(900) = 27, and 900/27 = 33.3….
- Only 360 is a tau number, so the true count is 1 < 2.

**Corrected Lemma 19** (ω(k) for ω(n)) [T]. For a ∈ G and n ≥ 1, the number of
tau numbers ap ≤ n with p prime, p ∤ a, is exactly #{p ≤ n/a : p ∤ a}. This
is ≥ π(n/a) − ω(a).

*Proof.*

- Each such p gives a tau number ap ≤ n, by Lemma 18.
- Distinct p give distinct ap.
- At most ω(a) primes divide a. ∎

This lemma is not used below. Zelinsky's Theorem 22 does not use it either:
it uses Lemma 20.

**Lemma 20** [T]. For a ∈ G let E_a = {ap : p prime, p > g(a)}.

- (a) Every element of E_a is a tau number.
- (b) E_a ∩ E_b = ∅ for distinct a, b ∈ G.
- (c) For every n ≥ 1 and every finite S ⊂ G,

  **T(n) ≥ Σ_{a∈S} max(0, π(n/a) − π(g(a))) ≥ Σ_{a∈S} (π(n/a) − π(g(a))).**   (1.1)

*Proof.*

- **(a)** p > g(a) gives p ∤ a. Apply Lemma 18.
- **(b)** Suppose m = ap = bq, with p > g(a) and q > g(b) prime.
  - Every prime factor of a is ≤ g(a) < p. So p is the largest prime factor
    of m: p = g(m).
  - In the same way, q = g(m).
  - So p = q, and then a = m/p = b.
- **(c)** The sets E_a ∩ [1, n], for a ∈ S, are pairwise disjoint sets of
  tau numbers in [1, n]. So T(n) ≥ Σ_a |E_a ∩ [1, n]|.
  - Now |E_a ∩ [1, n]| = #{p prime : g(a) < p ≤ n/a}.
  - If n/a ≥ g(a), this is π(n/a) − π(g(a)) ≥ 0.
  - If n/a < g(a), it is 0, and π(n/a) − π(g(a)) ≤ 0.
  - Either way it equals max(0, π(n/a) − π(g(a))) ≥ π(n/a) − π(g(a)). ∎

Zelinsky's own proof of (b) is the same argument, phrased through the index
k = π(g(aᵢ)) + 1 of the first admissible prime.

**Lemma 21** (count ≥ Aπ(n) − B). The one-line proof, "each summand in A
introduces an error of at most 1", would need π(n/a) ≥ π(n)/a − 1 for all
a ∈ G and all n. Zelinsky does not prove that. **I neither proved nor refuted
it.** Nothing here uses it, and Theorem 22's proof does not use it either.

## 2. Zelinsky's Theorem 22, reproduced from his own inputs

**Statement** (published Theorem 22): for all n > 7.42·10¹³, T(n) > π(n)/2.

**The argument, written out correctly** [T]. Let
M_Z = 28,653,696 and S = G(M_Z), and let n ≥ 599·M_Z.

- Every a ∈ S then has x = n/a ≥ 599. Dusart's lower bound gives
  π(n/a) ≥ (n/a)·h(ln(n/a)), where h(v) = 1/v + 1/v².
- h is decreasing on v > 0, and ln(n/a) ≤ ln n. So
  π(n/a) ≥ (1/a)·(n/ln n)(1 + 1/ln n).
- Summing, and applying (1.1):
  T(n) ≥ L₀(S)·(n/ln n)(1 + 1/ln n) − β(S).
- With L₀ > .508, β < B, and 1 > 0.992, this is Zelinsky's
  "T(n) > .508(n/log n)(1+.992/log n) − 8694520815".
- Dusart's upper bound then turns it into the comparison with π(n)/2.

**His inputs, recomputed** [C, 2026-10-31]. These are the values of
`comp-generators` @ `4fff65a`/`4074e69` and `check-generators`
@ `6faa10e`/`b961da4`, which agree exactly. My scratch program agrees too.

| Zelinsky says | Recomputed | Verdict |
|---|---|---|
| "exactly 413980 p-generators" ≤ 28,653,696 | \|G(28,653,696)\| = **413,980**. M_Z itself is a generator (2⁷·3³·8291) and is counted. | Agrees, reading "≤" (his text says both "≤" and "less than"). |
| "Their A value … is over .508" | L₀ = **0.50800004723884173345…** | True, with margin 4.7·10⁻⁸. A first exceeds .508 at the generator 28,653,680; his M_Z is the next generator. |
| "B < 8694520815" | B = Σ(π(g)+1) = **3,348,920,075**; β = 3,348,506,095 | True; his bound is 2.6× loose. |
| B formula: G(π(413980/36)) + G(π(413980/80)) + G(π(413980/96)) + (413980 − π(413980/36) − π(413980/80) − π(413980/96)) − π(413980/128), with G(m) = m(m+1)/2 | As printed it evaluates to **1,785,485**, which is far *below* the true B. So the printed inequality is **false**. | The formula is garbled; see below. |
| "for all n > 598·28653696" | Dusart's lower bound is stated for x ≥ 599, so the chain is justified for n ≥ 599·M_Z = 1.716·10¹⁰ | A slip, harmless at 7.42·10¹³. |
| crossing "10^13.87" | With A = .508 and B = 8,694,520,815, the final inequality holds exactly for n > **7.30936·10¹³** (log₁₀ = 13.86388). Margin at 7.42·10¹³: 1.32·10⁸. | Agrees: 10^13.87 = 7.41·10¹³ < 7.42·10¹³. |

**Reading the B formula.**

- Replace 413980 by M_Z in the π arguments, and read the last "−" as "×".
  The expression then becomes R = Σ_{c∈{36,80,96}} G(π(M_Z/c)) +
  (413980 − Σ_c π(M_Z/c))·π(M_Z/128).
- R evaluates to **8,685,500,885**. That is within 0.1% of his
  8,694,520,815 but not equal. **I could not reproduce his number exactly.**
- The argument behind this reading proves β ≤ R + 6·π(M_Z/128) =
  8,685,620,465, not β ≤ R. Each family c·q excludes the two primes q | c,
  so 6 more generators fall into the "others" term.
- Both R and his number are far above the true B, so nothing turns on
  this.
- The structure behind this reading is right. If a ∈ G(M_Z) has
  g(a) > M_Z/128:
  - then g(a)² ∤ a, and the cofactor c = a/g(a) is < 128;
  - c satisfies 4τ(c) | c, because τ(a) = 2τ(c) and gcd(g(a), 4τ(c)) = 1;
  - a hand check of c < 128 leaves exactly {36, 80, 96};
  - `comp-generators` counts these as 43,723 / 10,683 / 5,952.
- Since the true B is computed directly, the formula does not matter for
  anything below.

**Verdict on Theorem 22** [T, on the [C] inputs above]: **correct as stated.** His chain is right once written as
above, and his three inputs are right. The defects are presentational:

- Lemma 19 is false as printed (presumably ω(n) for ω(k));
- Lemma 21 is unproved;
- the B formula is garbled;
- "598" should be "599".

With the true B, his own chain already gives 2.83·10¹³ in place of
7.42·10¹³.

## 3. The improved argument

Zelinsky's threshold is high for two separate reasons, and the argument
below removes both.

1. **He replaces ln(n/a) by ln n in every term.** That loses a factor of
   about 1 + ln a / ln(n/a) per term. The L₀-weighted mean of ln a over
   G(M_Z) is L₁/L₀ ≈ 6.2, so the loss is large.
   - Proposition A keeps ln(n/a).
   - This alone, with his own set and Lemma Q, brings the threshold to about
     4.3·10¹¹. That is observed in scratch, J = 4, and is not used.
2. **He uses one generator set for all n.** So the set must have L₀ > 1/2,
   which forces β ≈ 3.3·10⁹, and β is what sets the threshold.
   - Lemma P works on a finite piece of n whatever the sign of L₀ − 1/2.
   - So small n can use small sets with small β: 7,453 for G(16,694).
   - This is what takes the threshold from about 4·10¹¹ to 10⁷.

Throughout this section:

- S ⊂ G is finite, J ≥ 0, n ≥ 599·max S, and u = ln n;
- L_k = L_k(S) and β = β(S).

**Proposition A** (moment lower bound) [T].

  Σ_{a∈S} π(n/a) ≥ (n/u) · Σ_{m=0}^{J} (L_m + m L_{m−1}) u^{−m}.   (3.1)

*Proof.* Fix a ∈ S and put ℓ = ln a.

- Since a ≥ 8, ℓ > 0.
- Since n/a ≥ 599, u − ℓ = ln(n/a) ≥ ln 599 > 0. So t := ℓ/u ∈ (0, 1).
- Dusart's lower bound at x = n/a ≥ 599 gives
  π(n/a) ≥ (n/a)·[(u−ℓ)⁻¹ + (u−ℓ)⁻²].
- For 0 ≤ t < 1 we have the geometric series and its derivative:
  - (u−ℓ)⁻¹ = u⁻¹ Σ_{k≥0} tᵏ;
  - (u−ℓ)⁻² = u⁻² Σ_{k≥0} (k+1) tᵏ.

  Both are absolutely convergent with nonnegative terms, so every partial
  sum is a lower bound:
  - (u−ℓ)⁻¹ ≥ Σ_{k=0}^{J} ℓᵏ u^{−k−1};
  - (u−ℓ)⁻² ≥ Σ_{k=0}^{J−1} (k+1) ℓᵏ u^{−k−2}.
- Add the two, and write the second sum with m = k + 1:
  (u−ℓ)⁻¹ + (u−ℓ)⁻² ≥ Σ_{m=0}^{J} (ℓᵐ + m ℓ^{m−1}) u^{−m−1}.
- Multiply by n/a and sum over a ∈ S. ∎

**Proposition B** (master inequality) [T]. Define

  g_S(u) = Σ_{m=0}^{J} c_m u^{−m},
  c₀ = L₀ − 1/2,  c₁ = L₁ + L₀ − 0.6381,  c_m = L_m + m L_{m−1} for 2 ≤ m ≤ J.   (3.2)

Then, with J ≥ 1 and n ≥ 2,

  **T(n) − π(n)/2 ≥ (n/u)·g_S(u) − β.**   (3.3)

*Proof.*

- By (1.1), T(n) ≥ Σ_S π(n/a) − β.
- Apply (3.1) to the sum.
- By Dusart's upper bound, π(n)/2 ≤ (n/u)(1/2 + 0.6381/u).
- Subtract. ∎

**Lemma P** (one finite piece) [T]. Suppose:

- e ≤ p ≤ q and p ≥ 599·max S;
- c_m > 0 for every 1 ≤ m ≤ J (c₀ may be negative);
- g_S(ln q) ≥ 0;
- (p/ln p)·g_S(ln q) ≥ β.

Then every integer n ∈ [p, q] satisfies
T(n) − π(n)/2 ≥ (p/ln p)·g_S(ln q) − β ≥ 0.

*Proof.* Let n ∈ [p, q], so u ∈ [ln p, ln q] and n ≥ 599·max S.

- g_S is nonincreasing on (0, ∞), because its u^{−m} coefficients are
  positive for m ≥ 1. So g_S(u) ≥ g_S(ln q) ≥ 0.
- x/ln x is increasing for x ≥ e, so n/u ≥ p/ln p > 0.
- Hence (n/u)·g_S(u) ≥ (p/ln p)·g_S(ln q).
- Apply (3.3). ∎

**Lemma Q** (the infinite tail) [T]. Suppose:

- n_f ≥ 599·max S and n_f ≥ e^{J+1};
- c_m ≥ 0 for **every** 0 ≤ m ≤ J. In particular L₀ ≥ 1/2;
- Σ_{m=0}^{J} c_m · n_f/(ln n_f)^{m+1} ≥ β.

Then every n ≥ n_f satisfies T(n) − π(n)/2 ≥ Σ_m c_m n_f/(ln n_f)^{m+1} − β ≥ 0.

*Proof.*

- (n/u)·g_S(u) = Σ_m c_m e^u u^{−m−1}.
- d/du (e^u u^{−m−1}) = e^u u^{−m−2} (u − m − 1). This is ≥ 0 for
  u ≥ m + 1, and here u ≥ ln n_f ≥ J + 1 ≥ m + 1.
- With every c_m ≥ 0, each term is at least its value at u = ln n_f.
- Apply (3.3). ∎

This is the only place where L₀ > 1/2 is needed. An infinite range has to
be anchored in a set whose reciprocal sum beats ½, and Zelinsky's G(M_Z) is
exactly such a set. Sets with L₀ < 1/2 are used only on finite pieces, and
Lemma P does not care about the sign of c₀.

## 4. The theorem with N\* = 10⁷: stages, inputs, inequalities

J = 4 throughout. Three stage sets, all prefixes of the generator list:

| Stage | S | \|S\| | max S | 599·max S | β(S) | used on |
|---|---|---|---|---|---|---|
| 0 | G(16,694) | 352 | 16,668 | 9,984,132 | 7,453 | [10⁷, 10⁸] (two pieces) |
| 1 | G(166,944) | 3,055 | 166,944 | 99,999,456 | 346,644 | [10⁸, 10¹²] (two pieces) |
| F | G(28,653,696) | 413,980 | 28,653,696 | 17,163,563,904 | 3,348,506,095 | [10¹², ∞) (Lemma Q) |

The cut-offs 16,694 = ⌊10⁷/599⌋ and 166,944 = ⌊10⁸/599⌋ are the largest that
satisfy the validity condition at the stage's left end.

**Inputs** [C], 2026-10-31. They come from two files, both on `lead-colton`
@ `1b20e41`:

- **`results/generators/moments.txt`**: `comp-generators` @ `4074e69`.
  Segmented τ-sieve in C; Arb balls at 300 bits; radius ≤ 2·10⁻⁷⁹;
  35 printed digits.
- **`verify/generators/moments.txt`**: `check-generators` @ `b961da4`.
  DFS over exponent signatures with PARI primepi; Arb balls at 256 bits;
  radius ≤ 4·10⁻⁶⁶; 30 printed digits.

They agree exactly on N, β, B, max G and max a·g, and to every printed digit
on L₀…L₆. `colton-threshold-inputs-build.py` reads both files and writes
`colton-threshold-inputs.json` and `colton-threshold-inputs-verify.json`. It
asserts that the integers are equal and that the L_k enclosures overlap.

Each L_k is stored with an **enclosure radius**: that implementation's ball
radius plus one unit in the last printed decimal place. The printed decimals
are rounded midpoints, not outward-rounded endpoints, so the extra ulp is
what makes the enclosure rigorous. Every coefficient c_m in (3.2) is
increasing in every L_k, so the checkers use only the **lower endpoint** of
each enclosure. The table below shows comp-generators' values to 30 significant
digits.

| | L₀ | L₁ | L₂ | L₃ | L₄ |
|---|---|---|---|---|---|
| G(16,694) | 0.386074887965281178944791795969 | 1.53627961512778615391493344608 | 8.11946784452291563279657610895 | 52.8953783969192316944440248372 | 389.060352878419933242328278568 |
| G(166,944) | 0.428513592799916556237796773157 | 1.99663715511024391410144463416 | 13.1319934471026123471372160392 | 107.676778420112115635048941290 | 989.963966379148191497140599898 |
| G(28,653,696) | 0.508000047238841733452073262988 | 3.14950355230516058989272826632 | 30.0282903033822207339992138297 | 357.841623549235450947560606454 | 4730.46992866496347919355857011 |

**Coefficients (3.2)**, to 12 digits:

| S | c₀ | c₁ | c₂ | c₃ | c₄ |
|---|---|---|---|---|---|
| G(16,694) | −0.113925112035 | 1.28425450309 | 11.1920270748 | 77.2537819305 | 600.641866466 |
| G(166,944) | −0.0714864072001 | 1.78705074791 | 17.1252677573 | 147.072758761 | 1420.67108006 |
| G(28,653,696) | +0.00800004723884 | 3.01940359954 | 36.327297408 | 447.926494459 | 6161.83642286 |

c₁, …, c₄ > 0 in every row, so the hypothesis of Lemma P holds. Every
c₀, …, c₄ ≥ 0 for G(28,653,696), so the hypothesis of Lemma Q holds.

**The five inequalities.** Each row is one application of Lemma P. The
surplus column is a lower bound for T(n) − π(n)/2 on the whole piece.

| S | piece [p, q] | ln p | ln q | g_S(ln q) | (p/ln p)·g_S(ln q) | β | surplus |
|---|---|---|---|---|---|---|---|
| G(16,694) | [10⁷, 3·10⁷] | 16.11809565 | 17.21670794 | 0.020400586 | 12,656.946 | 7,453 | **5,203.9** |
| G(16,694) | [3·10⁷, 10⁸] | 17.21670794 | 18.42068074 | 0.006352735 | 11,069.599 | 7,453 | **3,616.6** |
| G(166,944) | [10⁸, 10⁹] | 18.42068074 | 20.72326584 | 0.078853116 | 428,068.42 | 346,644 | **81,424** |
| G(166,944) | [10⁹, 10¹²] | 20.72326584 | 27.63102112 | 0.025028877 | 1,207,767.0 | 346,644 | **861,123** |

The tail, by Lemma Q, with S = G(28,653,696) and n_f = 10¹²:

- ln n_f = 27.63102112. Also n_f ≥ 3⁵ > e⁵ and n_f ≥ 599·max S.
- The five terms c_m n_f/(ln n_f)^{m+1} are:

  | m | 0 | 1 | 2 | 3 | 4 |
  |---|---|---|---|---|---|
  | term | 2.8953·10⁸ | 3.9548·10⁹ | 1.7220·10⁹ | 7.6846·10⁸ | 3.8258·10⁸ |

- Their sum is 7,117,431,709 ≥ β = 3,348,506,095, so the surplus is
  **3.769·10⁹**.

Coverage:

- Stage 0 covers [10⁷, 10⁸] and stage 1 covers [10⁸, 10¹²]. The pieces are
  closed and share endpoints.
- The tail covers [10¹², ∞).
- So every integer n ≥ 10⁷ is covered, and the smallest surplus is 3,616.

**Proof of the Theorem.** Apply Lemma P to the four rows and Lemma Q to the
tail. Every hypothesis is listed above. ∎

**Two independent checks of the arithmetic** (2026-10-31; both scripts are
in this directory and both exit 0):

- **`colton-threshold-check-rational.py`.**
  - Every number is an exact `Fraction`. Each L_k is replaced by the lower
    endpoint of its enclosure.
  - Each ln of an endpoint is replaced by a rational r. The script proves
    r ≥ ln n by showing that a partial Taylor sum of e^r, which is a lower
    bound for e^r, already reaches n.
  - The inequalities are then exact rational comparisons.
- **`colton-threshold-check-arb.py`.**
  - python-flint Arb balls at 256 bits, using Arb's logarithm.
  - An inequality is accepted only if the whole ball lies in [0, ∞).
  - Different code, different arithmetic, same statements.

Both report the same five surpluses: 5203.9458, 3616.5988, 81424.416,
861123.02 and 3.7689256·10⁹.

- I wrote both checkers. "Independent" here means no shared code and a
  different arithmetic method. It does not mean a different author: a
  misreading of the statements by me would be shared.
- The statements they check are the ones in this section, so the referee
  can check those directly.

**Alternatives.** These are not claimed; each is reported as observed with
the same scratch tools.

- **Two-stage version, N\* = 10⁸.** Drop stage 0 and keep G(166,944) and
  G(28,653,696).
- **The method's floor.** It is about 4·10⁶ with Dusart (6.5) alone. At
  4·10⁶ the best set I tried still starts with surplus/β ≈ 1.33.
- **Why I did not go lower.** The finite range below 10⁷ is already
  trivial to compute, so a lower N\* buys nothing and costs another stage.
  10⁷ was chosen for round endpoints and a 23% margin on β.

## 5. The hard step

**What the argument needs.** It must replace the sum over generators by
finitely many numbers, uniformly in n, without throwing away the gain from
ln(n/a) < ln n.

**How Zelinsky did it.** He used the crude bound ln(n/a) ≤ ln n and one set
for every n. That is uniform in n, but the whole margin then has to come from
L₀ − 1/2 = 0.008, against β ≈ 3.3·10⁹. Between them, those two choices
account for the factor of about 10⁷ between his 7.42·10¹³ and 10⁷ (§3).

**How it is done here.** Two steps:

- **Proposition A** expands 1/ln(n/a) in powers of ln a / ln n. All terms
  are nonnegative, so truncating gives a lower bound valid for every n
  above the validity point. Four moments L₁…L₄ capture almost all of the
  gain: at n = 10⁷ the truncation loses about 2% against the exact
  per-term sum (observed in scratch).
- **Lemmas P and Q** convert "for all n in [p, q]" and "for all n ≥ n_f"
  into one inequality each. They use only three monotonicity facts:
  - x/ln x increases for x ≥ e;
  - g_S decreases;
  - e^u u^{−m−1} increases for u ≥ m + 1.

**The sign conditions are the place to check.**

- Lemma P needs c₁, …, c₄ > 0. c₂, c₃, c₄ are sums of positive terms. The
  only one that could fail is c₁ = L₁ + L₀ − 0.6381, and L₁ ≥ 1.53 in every
  stage, so it is comfortably positive.
- Lemma Q needs every c_m ≥ 0, i.e. L₀(G(M_Z)) ≥ 1/2.

**Status: done** [T]. It was refereed (ACCEPT WITH CORRECTIONS,
2026-10-30). No step in it is left to the reader.

**What remains open is not mathematics.** It is the provenance of the one
cited input, Dusart (6.5) (§7.3). The theorem is only as good as β
and L₀…L₄ at three cut-offs. They are the one place where a wrong number
would silently give a wrong theorem, which is why they are named and
tabulated rather than folded into the proof.

## 6. Sanity checks (observed, one program each; not part of the proof)

All of these were run in the scratch directory on 2026-10-30. They are
recorded so the referee can see that the bounds are not vacuous.

**1. The p-generated count against the true count.** Let
Z(n) = Σ_{a∈G} max(0, π(n/a) − π(g(a))), the exact count in (1.1) with
S = all of G (truncated at a ≤ 10⁹). T(n) is the OEIS A111291 value, READ
by `lit-colton`.

| n | Z(n) | T(n) | π(n)/2 |
|---|---|---|---|
| 10⁷ | 391,972 | 394,240 | 332,289.5 |
| 10⁸ | 3,549,887 | 3,558,181 | 2,880,727.5 |
| 10⁹ | 32,576,671 | 32,608,999 | 25,423,767 |

- So 99.4–99.9% of tau numbers are p-generated.
- Z(n) ≥ π(n)/2 already at n = 10⁵ (5,035 against 4,796), and fails at 10⁴
  (588 against 614.5).

**2. The analytic lower bound (3.1) − β against exact counts.** It sits
below Z(n) and above π(n)/2 at every sampled point:

| n | S | analytic bound | Z(n) | π(n)/2 |
|---|---|---|---|---|
| 10⁷ | G(16,694) | 349,767 | 391,972 | 332,289.5 |
| 10⁹ | G(166,944) | 29,071,721 | 32,576,671 | 25,423,767 |
| 10¹⁰ | G(166,944) | 252,950,371 | 302,038,273 | 227,526,255.5 |

With the same set, the exact count in (1.1) at n = 10⁷ is
Σ_{a∈G(16,694)} max(0, π(n/a) − π(g(a))) = 361,490. That is above the
analytic 349,767, as it must be. So the moment truncation plus Dusart cost
3.2% there.

**3. Dusart (6.5) at every jump of π on [599, 2·10⁹].** Long double, one
program. Minimum slack:

- lower bound: 0.0145, just below the prime 1423;
- upper bound: 0.0029, at the prime 1627.

This is not a proof of (6.5) beyond what Dusart proves.

**4. Lemma 18** by brute force, a ≤ 3000 and p < 5000. The counterexample
to printed Lemma 19 was confirmed by script.

## 7. What was not established

1. **One shared component in the inputs, now discharged.** The inputs are [C] in the
   project's sense for the generator lists, N, β and the maxima:
   - two methods, a τ-sieve and a constructive signature enumeration;
   - no shared code;
   - identical sha256 lists;
   - β uses an independent π in each, a bit sieve and PARI.

   The moment sums L_k are a straight sum over that common list. **Both
   implementations do that sum with python-flint Arb.**
   - That is a shared library, though in different code.
   - **Discharged by the referee** (`referee/colton-threshold.md` M3, with
     scripts in `referee/colton-threshold/`).
     - The referee recomputed N, β, max G(M) and L₀…L₆ at all three M in
       PARI/GP. That shares no code and no library with either
       implementation, and uses no Arb:
       - generators by `forfactored` over every a ≤ 28,653,696, testing
         2τ(a) | a directly;
       - π(g) by PARI `primepi`;
       - sums in 60-digit floating point.
     - N, β and max G agree exactly. The L_k agree with
       `colton-threshold-inputs.json` to |difference| ≤ 1.9·10⁻³⁰.
     - Checked here on 2026-10-31: every one of the referee's 21 L_k values
       lies inside the enclosure carried by both input files. The integers
       are equal in both.
   - My scratch mpmath 40-digit sum over my own list (C sieve) is a further
     Arb-free computation. It agrees to 30 digits.

   The quantities used are, for M ∈ {16694, 166944, 28653696}: N(M),
   L₀…L₄ (L₅ and L₆ are slack), β(M) and max G(M).
2. **Refereed, with limits.** `ref-colton` accepted with corrections on
   2026-10-30. The limits are stated in its report:
   - Dusart (6.5) was re-read, but not re-proved;
   - the pruning proofs of `verify/generators/gen.py` were not refereed.
     They do not matter here: two other methods enumerate every integer and
     agree;
   - the scratch claims in §3, §4 "Alternatives" and §6 were not checked,
     and none of them is used.
3. **Dusart (6.5) was read in the arXiv preprint only** (M5).
   - **The published statement (Ramanujan J. 45 (2018) 227–251) has not
     been read**, by me or by the referee. Neither has Zelinsky's own
     source, Dusart 1999, Math. Comp. 68 (HTTP 403 for `lit-colton`).
   - The [T] stands on this one cited inequality pair.
   - **Outcome of the lit pass** (`lit-colton-dusart`, 2026-10-31;
     `literature/colton.md`, PR #25 into `dev`):
     - The published Ramanujan J. 2018 version is paywalled, and was NOT
       READ.
     - No erratum touches π(x). The author's correctif fixes typos in
       Theorem 3.5 only.
     - A secondary source attributes the identical pair (x ≥ 599 lower,
       x > 1 upper, 1.2762) to the published paper, with no theorem number.
       That source is arXiv:2404.17165, p. 8, READ.
     - The published numbering is not established. It is probably §5, by
       inference from Axler, INTEGERS 18 (2018) #A61.
   - So the citation stays arXiv:1002.0442v1 Theorem 6.9, eq. (6.5),
     READ. **The published statement remains unread.** Buying it is
     Aaron's call.
4. **Zelinsky's B = 8,694,520,815 was not reproduced exactly.** My best
   reading of his formula gives 8,685,500,885. This does not matter: the
   true B is computed directly.
5. **Zelinsky's Lemma 21 was neither proved nor refuted.** It is not used.
6. **The finite range n < 10⁷ is not in this file.** The Theorem covers
   n ≥ 10⁷ *inclusive*, so the finite check must cover 1 ≤ n ≤ 10⁷ − 1,
   or any superset of it. The Theorem's surplus is ≥ 3616, so there is no
   equality case at the seam. Colton's statement is sharp only at n = 7.
7. **No novelty claim.**
   - Zelinsky's method is his.
   - The ln(n/a) refinement is the obvious one; `lit-colton` §7 suggests it.
   - Whether anyone has published a lower threshold was searched by
     `lit-colton` ("none found"). I did no literature search of my own.
   - **Added 2026-10-31 (lead-colton).** OEIS A323326 (McCranie 2019) claims
     the full conjecture, by computation to 7.44·10¹³ on top of Zelinsky's
     threshold (`colton-conjecture.md`, "Prior work"). A lower threshold
     than 7.42·10¹³ is "not found in prior work as of 2026-10-31
     (`literature/colton-novelty.md`); Lauer 2014, SeqFan and CNKI not
     reached". It is not claimed as new.

## 8. Reproduce

Machine: PC2 (8 cores, WSL2), the box all of this project's chats run on.
Date: 2026-10-30/31. Branch `agent/thm22`.

```
# rebuild the two input files from the two [C] moment files (asserts they agree)
~/dev/projects/open-problems/.venv/bin/python findings/colton-threshold-inputs-build.py
# the five inequalities, two checkers x two input files (each < 1 s); all four exit 0
for f in findings/colton-threshold-inputs.json findings/colton-threshold-inputs-verify.json; do
  ~/dev/projects/open-problems/.venv/bin/python findings/colton-threshold-check-rational.py $f
  ~/dev/projects/open-problems/.venv/bin/python findings/colton-threshold-check-arb.py $f
done
```

**Sanity scripts** (§2 and §6). They are not inputs to the Theorem and were
kept so that the claims in §2 and §6 can be re-run:

- `colton-threshold-sanity-zelinsky.py` covers:
  - Zelinsky's crossing point: 7.30936·10¹³ with his A and B, and
    2.82759·10¹³ with the true B. This is mpmath `findroot` at 40 digits;
  - his B formula, printed and corrected readings;
  - the Lemma 19 counterexample;
  - Lemma 18 by brute force;
  - the generator at which A first passes .508.
- `colton-threshold-sanity-gen.c` lists the generators ≤ M as binary (a, g)
  pairs. Single-threaded segmented trial division, 2 min to 10⁹.
- `colton-threshold-sanity-z.c` computes Z(n) from that list.
- `colton-threshold-sanity-dusart.c` checks (6.5) at every jump of π up to X.

```
gcc -O2 -o gen findings/colton-threshold-sanity-gen.c -lm && ./gen 1000000000 g1e9.bin
gcc -O2 -o z findings/colton-threshold-sanity-z.c && echo 10000000 | ./z 1250000000 g1e9.bin
gcc -O2 -o du findings/colton-threshold-sanity-dusart.c -lm && ./du 2000000000
~/dev/projects/open-problems/.venv/bin/python findings/colton-threshold-sanity-zelinsky.py g286.bin   # g286.bin = ./gen 28653696 g286.bin
```
