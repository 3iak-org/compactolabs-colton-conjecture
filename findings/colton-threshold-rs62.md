# Colton's conjecture from 10⁹ on, with Rosser–Schoenfeld 1962 as the only cited input

*`rs62-threshold`, opened by `lead-colton-rs62`, 2026-10-31. Branch
`agent/rs62-threshold`. Companions, all in this directory:*

- *`colton-threshold-rs62-inputs-build.py` reads the two moment grids,
  `results/rs62/moments-grid.txt` and `verify/rs62/moments-grid.txt`. It
  asserts that they agree, and writes `colton-threshold-rs62-inputs.json`
  and `colton-threshold-rs62-inputs-verify.json`, one per implementation.*
- *`colton-threshold-rs62-check-rational.py` and
  `colton-threshold-rs62-check-arb.py` are two checkers of the finitely many
  statements in §4. They share no code and no arithmetic method.*

This file stands alone. It re-proves everything it uses from
`colton-threshold.md`, with general constants, and does not cite that file
for any step.

**Status (2026-10-31): [T] on [C] inputs; refereed, ref-colton-rs62 ACCEPT (round 3, 2026-10-31; round 2 REVISE R1 fixed at 96b2919), report `referee/colton-threshold-rs62.md`.** The computed inputs are [C] (two
implementations, below). Both checkers exit 0 on both input files.

Adversary (adv-colton-rs62, 2026-10-31): NOT BROKEN, `adversary/colton-rs62.md`.

## The answer

> **Theorem (RS62 threshold).** For every integer n ≥ 10⁹,
>
> T(n) − π(n)/2 ≥ 917,294.
>
> The proof cites exactly one external result: Rosser–Schoenfeld 1962,
> Theorem 1, (3.1) and (3.2) [L, READ]. It uses no Dusart, no Axler and no
> other explicit prime bound.

Notation:

- T(n) = #{1 ≤ k ≤ n : τ(k) | k}, where τ is the number of divisors.
- π is the prime-counting function.

**Corollary** [T on [C]; refereed with the Theorem, ref-colton-rs62 ACCEPT, round 3, 2026-10-31]. π(n) ≤ 2T(n) for every integer
n ≥ 1.

- For n ≥ 10⁹ this is the Theorem.
- For 1 ≤ n ≤ 10⁹ (inclusive) it is the exact range: [C], refereed in
  `referee/colton-range.md`, written up in `colton-conjecture.md` §2.
- The two ranges overlap at n = 10⁹. That n is covered twice and there is no
  ≤/< hazard: the Theorem is stated with "≥" at n = 10⁹ inclusive, and the
  range is stated "1 ≤ n ≤ 10⁹" inclusive.

So the conjecture in its π form rests on RS62 plus this project's [C]
computations. Dusart (6.5) is not needed for any n. This is Colton's π form,
as in `colton-conjecture.md`. Colton's x/(2 log x) sentence is not claimed
here.

**No novelty claim.** OEIS A323326 (McCranie 2019) already claims the
conjecture, by computation to 7.44·10¹³ on top of Zelinsky's threshold
(`colton-conjecture.md`, "Prior work"). This file is a second proof of the
analytic half. Its one cited input is different from Dusart, and its
statement was READ; its proof was not checked. The method is
Zelinsky's, as refined in `colton-threshold.md`. Nothing here is a new idea.

### What would have to be true for this to be wrong

1. **The lower bound (3.1) fails at some x where it is used.** It is used
   at every real x ≥ 9,090.9 (§5). There are two cases.
   - **On [9,090.9, 10⁹] it rests on this project's [C],** not on RS62. The
     file `rs62-lower.txt` has two implementations that share no code. Both
     evaluate every one of the 50,847,518 prime-gap intervals in rigorous
     arithmetic, and the reduction of §5 turns that into every real x. For
     the Theorem to be wrong here, both programs would have to be wrong in
     the same direction, or the reduction would have to fail.
   - **For x > 10⁹ it rests on RS62 Theorem 1 [L].** The statement was READ
     from the page image (`literature/colton.md`). The theorem has been
     refereed since 1962, and no correction was found.
2. **RS62 (3.2) fails at some integer x ≥ 10⁹.** That is the other half of
   what is cited, and it is also inside RS62's analytic range.
3. **The computed inputs are wrong by more than the margins allow.** The
   inputs are β, max S and L₀…L₆ for four prefixes G(M). The proof survives:
   - β understated by a factor of up to 1.98 (binding: the tail);
   - all L_k overstated together by up to 1.57%, relative (binding: the
     tail, through c₀ = L₀ − ½ ≥ 0);
   - all L_k overstated together by up to 3.2% on the three finite pieces.

   These margins are from float scratch, not from the checkers. The
   enclosures used have width about 10⁻³¹. A *systematic* error, such as the
   wrong set definition, is what the two implementations exist to rule out.
4. **An error in the reductions** of §3: Proposition A, Proposition B,
   Lemma P, Lemma Q, or the monotonicity in the inputs. Each is a few lines,
   written out in full.
5. **An error in the generator lemma or the disjointness** (§1). Each is
   three lines.
6. **Both checkers wrong in the same direction.** They use exact rationals
   with series-certified logarithms on one side, and Arb balls with Arb's
   logarithm on the other. I wrote both, so a misreading of the statements by
   me would be shared. The statements are in §4 with their intermediate
   values, so a referee can check them by hand.

## 0. Notation and the cited input

- For a ≥ 2, g(a) is the largest prime factor of a.
- π(x) = #{p ≤ x : p prime}, for real x. ln is the natural logarithm.
- **G = {a ≥ 1 : 2τ(a) | a}**, and **G(M) = G ∩ [1, M]**.
  - Every a ∈ G is even, since 2 | 2τ(a) | a. Hence 1 ∉ G, g(a) is defined,
    and a ≥ 2.
  - In fact min G = 8. The candidates 2, 4 and 6 fail: 2τ = 4, 6 and 8
    respectively, and none of these divides its a.
- For finite S ⊂ G and k ≥ 0:
  - **L_k(S) = Σ_{a∈S} (ln a)^k / a**, with L_{−1} := 0;
  - **β(S) = Σ_{a∈S} π(g(a))**.

**Cited: Rosser & Schoenfeld 1962**, *Approximate formulas for some
functions of prime numbers*, Illinois J. Math. 6 (1962) 64–94, **Theorem 1**,
p. 69. Verbatim, as READ by `lit-colton-rs62` from the page image
(`literature/colton.md`, "Rosser–Schoenfeld 1962, Theorem 1: READ"):

> (3.1)  (x / log x)(1 + 1/(2 log x)) < π(x)   for 59 ≤ x,
>
> (3.2)  π(x) < (x / log x)(1 + 3/(2 log x))   for 1 < x.

Here log = ln. The paper's (3.4) has e^{3/2} = 4.48169, which confirms it.
Status: [L, READ 2026-10-31 by `lit-colton-rs62`; I have not read the PDF
myself]. No later correction was found (RS75, Schoenfeld 1976 and its
corrigendum, zbMATH, Crossref). The proof of Theorem 1 was not checked by
anyone here.

Only the weak forms are used below: "≥" for (3.1), and "≤" for (3.2).

## 1. Tau numbers from generators

**Lemma 1** [T, 2026-10-31]. If a ∈ G and p is a prime with p ∤ a, then ap
is a tau number.

*Proof.* gcd(a, p) = 1 and τ is multiplicative, so τ(ap) = τ(a)τ(p) =
2τ(a). Since a ∈ G, 2τ(a) | a, and a | ap. ∎

(This is one direction of Zelinsky 2002, Lemma 18, which is the only
direction used. `colton-threshold.md` §1 proves both.)

**Lemma 2** [T]. For a ∈ G let E_a = {ap : p prime, p > g(a)}.

- (a) Every element of E_a is a tau number.
- (b) E_a ∩ E_b = ∅ for distinct a, b ∈ G.
- (c) For every integer n ≥ 1 and every finite S ⊂ G,

  **T(n) ≥ Σ_{a∈S} (π(n/a) − π(g(a))) = Σ_{a∈S} π(n/a) − β(S).**   (1.1)

*Proof.*

- **(a)** Every prime factor of a is ≤ g(a) < p, so p ∤ a. Apply Lemma 1.
- **(b)** Suppose m = ap = bq, with p > g(a) and q > g(b) prime.
  - Every prime factor of a is < p, so p is the largest prime factor of m.
  - In the same way, q is the largest prime factor of m.
  - So p = q, and then a = b.
- **(c)** The sets E_a ∩ [1, n], for a ∈ S, are pairwise disjoint by (b).
  By (a) they consist of tau numbers in [1, n]. So T(n) ≥ Σ_a |E_a ∩ [1, n]|.
  - Now |E_a ∩ [1, n]| = #{p prime : g(a) < p ≤ n/a}.
  - If n/a ≥ g(a), this equals π(n/a) − π(g(a)).
  - If n/a < g(a), it is 0 ≥ π(n/a) − π(g(a)), because π is nondecreasing.
  - Summing over a ∈ S gives (1.1). ∎

## 2. Where this sits

`colton-threshold.md` proves T(n) − π(n)/2 ≥ 3616 for n ≥ 10⁷. It is
refereed, and it cites Dusart 2010 (6.5) [L, READ in the arXiv preprint
only; the published 2018 version is unread]. This file replaces that one
input by RS62 Theorem 1, at the cost of starting at 10⁹ instead of 10⁷. The
exact range already reaches 10⁹, so nothing is lost. RS62's constants are
weaker than Dusart's (α = ½ against 1, γ = 3/2 against 1.2762). The longer
moment expansion (J = 6 against 4) and the later start pay for that.

## 3. The chain, with general constants

**Hypotheses on π.** Fix constants α, γ, X₀, Y₀ such that:

- **(H↓)** π(x) ≥ (x/ln x)(1 + α/ln x) for every real x ≥ X₀, where
  **α ≥ 0** and **X₀ > 1**;
- **(H↑)** π(x) ≤ (x/ln x)(1 + γ/ln x) for every real x ≥ Y₀, where Y₀ > 1.

RS62 Theorem 1 gives (H↓) with α = ½, X₀ = 59, and (H↑) with γ = 3/2 for every
Y₀ > 1. The sign α ≥ 0 is used in Proposition A and in the monotonicity
lemma, and nowhere else. It holds for α = ½.

Throughout this section:

- S ⊂ G is finite and nonempty, and J ≥ 1 is an integer;
- L_k = L_k(S), β = β(S), and max S is the largest element of S;
- n is an integer, and u = ln n.

**Proposition A** (moment lower bound) [T]. If n ≥ X₀·max S, then

  Σ_{a∈S} π(n/a) ≥ (n/u) · Σ_{m=0}^{J} (L_m + α m L_{m−1}) u^{−m}.   (3.1)

*Proof.* Fix a ∈ S and put ℓ = ln a.

- **ℓ > 0**, since a ≥ 8.
- **ℓ < u.** n/a ≥ n/max S ≥ X₀ > 1, so u − ℓ = ln(n/a) > 0. Put
  t = ℓ/u. Since u > ℓ > 0, t ∈ (0, 1).
- **(H↓) applies at x = n/a**, because n/a ≥ X₀. With ln x = u − ℓ:

  π(n/a) ≥ (n/a)·[(u − ℓ)⁻¹ + α(u − ℓ)⁻²].

- **Two power series.** For 0 ≤ t < 1:
  - (u − ℓ)⁻¹ = u⁻¹(1 − t)⁻¹ = Σ_{k≥0} ℓᵏ u^{−k−1};
  - (u − ℓ)⁻² = u⁻²(1 − t)⁻² = Σ_{k≥0} (k+1) ℓᵏ u^{−k−2}.

  Both converge, and every term is ≥ 0 because ℓ, u > 0. So every partial
  sum is a lower bound:
  - (u − ℓ)⁻¹ ≥ Σ_{k=0}^{J} ℓᵏ u^{−k−1};
  - (u − ℓ)⁻² ≥ Σ_{k=0}^{J−1} (k+1) ℓᵏ u^{−k−2}.
- **This is where α ≥ 0 enters.** Multiply the second inequality by α ≥ 0;
  the direction is kept. (With α < 0 the truncated α-term would be an upper
  bound, and (3.1) would not follow.)
- **Combine.** Write the second sum with m = k + 1. Its terms become
  m ℓ^{m−1} u^{−m−1} for 1 ≤ m ≤ J. The m = 0 term is 0, consistent with
  L_{−1} = 0. So

  (u − ℓ)⁻¹ + α(u − ℓ)⁻² ≥ Σ_{m=0}^{J} (ℓᵐ + α m ℓ^{m−1}) u^{−m−1}.

- **Sum.** Multiply by n/a > 0 and sum over a ∈ S, using
  Σ_a ℓᵐ/a = L_m and Σ_a m ℓ^{m−1}/a = m L_{m−1}. ∎

**Proposition B** (master inequality) [T]. Define

  g_S(u) = Σ_{m=0}^{J} c_m u^{−m}, where   (3.3)
  - c₀ = L₀ − ½;
  - c₁ = L₁ + αL₀ − γ/2;
  - c_m = L_m + α m L_{m−1} for 2 ≤ m ≤ J.

If n ≥ X₀·max S and n ≥ Y₀, then

  **T(n) − π(n)/2 ≥ (n/u)·g_S(u) − β.**   (3.4)

*Proof.*

- By (1.1), T(n) ≥ Σ_S π(n/a) − β.
- Apply (3.1).
- By (H↑) at x = n ≥ Y₀, π(n)/2 ≤ (n/u)(½ + (γ/2)u⁻¹).
- Subtract. The m = 0 coefficient in (3.1) is L₀ + α·0·L₋₁ = L₀, which
  becomes c₀ = L₀ − ½. The m = 1 coefficient is L₁ + αL₀, which becomes
  c₁ = L₁ + αL₀ − γ/2. This needs J ≥ 1. The others are unchanged. ∎

So the general coefficients are exactly as the brief expected:
c₀ = L₀ − ½, c₁ = L₁ + αL₀ − γ/2, c_m = L_m + αmL_{m−1}, with validity
n ≥ X₀·max S. For RS62:

- **c₀ = L₀ − ½**;
- **c₁ = L₁ + L₀/2 − 3/4**;
- **c_m = L_m + (m/2)L_{m−1}** for 2 ≤ m ≤ 6.

**Lemma P** (one finite piece) [T]. Suppose:

- e ≤ p < q are integers, p ≥ X₀·max S and p ≥ Y₀;
- c_m ≥ 0 for every 1 ≤ m ≤ J (c₀ may have either sign);
- g_S(ln q) ≥ 0.

Then every integer n ∈ [p, q] satisfies

  T(n) − π(n)/2 ≥ (p/ln p)·g_S(ln q) − β.

*Proof.* Let n ∈ [p, q] be an integer. Then n ≥ p ≥ X₀·max S and n ≥ Y₀, so
(3.4) holds. Also u ∈ [ln p, ln q].

- **g_S is nonincreasing on (0, ∞).** Each u^{−m} with m ≥ 1 is decreasing
  there, and its coefficient c_m is ≥ 0. So g_S(u) ≥ g_S(ln q) ≥ 0.
- **x/ln x is nondecreasing for x ≥ e.** Its derivative is
  (ln x − 1)/(ln x)² ≥ 0. So n/u ≥ p/ln p > 0.
- **Multiply.** Both factors are nonnegative and each is at least the
  corresponding factor on the right. So
  (n/u)·g_S(u) ≥ (p/ln p)·g_S(ln q). Apply (3.4). ∎

**Lemma Q** (the infinite tail) [T]. Suppose:

- n_f is an integer with n_f ≥ X₀·max S and n_f ≥ Y₀;
- ln n_f ≥ J + 1;
- c_m ≥ 0 for **every** 0 ≤ m ≤ J. In particular L₀ ≥ ½.

Then every integer n ≥ n_f satisfies

  T(n) − π(n)/2 ≥ Σ_{m=0}^{J} c_m · n_f/(ln n_f)^{m+1} − β.

*Proof.* For n ≥ n_f, (3.4) holds, and (n/u)·g_S(u) = Σ_m c_m e^u u^{−m−1}.

- d/du (e^u u^{−m−1}) = e^u u^{−m−2}(u − m − 1). This is ≥ 0 for
  u ≥ m + 1.
- For n ≥ n_f we have u ≥ ln n_f ≥ J + 1 ≥ m + 1 for every m ≤ J.
- So each e^u u^{−m−1} is at least its value at u = ln n_f. Since each
  c_m ≥ 0, the same holds for each term. ∎

**Lemma M** (monotonicity in the inputs; what the checkers may substitute)
[T]. In Lemmas P and Q, each of the following may be replaced by a bound on
the safe side, and the hypotheses and conclusion stay true:

- each L_k by any lower bound L_k^lo ≤ L_k;
- each ln q, ln p and ln n_f in a denominator by any upper bound;
- ln n_f in "ln n_f ≥ J + 1" by any lower bound.

The integers β and max S are used exactly.

Precisely, write c_m^lo for (3.3) evaluated at the L_k^lo, and let
r_p ≥ ln p, r_q ≥ ln q, r_f ≥ ln n_f and λ_f ≤ ln n_f. Suppose:

- for Lemma P: c_m^lo ≥ 0 for 1 ≤ m ≤ J,
  G := Σ_m c_m^lo r_q^{−m} ≥ 0, and (p/r_p)·G − β ≥ s;
- for Lemma Q: c_m^lo ≥ 0 for 0 ≤ m ≤ J, λ_f ≥ J + 1, and
  Σ_m c_m^lo n_f r_f^{−m−1} − β ≥ s.

Then the hypotheses of the respective lemma hold, and its bound is ≥ s.

*Proof.*

- **c_m ≥ c_m^lo for every m.** Each c_m is a constant plus a combination of
  the L_k with coefficients in {1, α, mα}. Since α ≥ 0, all of these are
  ≥ 0. So the sign hypotheses transfer.
- **Lemma P.** g_S(ln q) = Σ_m c_m (ln q)^{−m} ≥ Σ_m c_m^lo (ln q)^{−m}, since
  every weight (ln q)^{−m} is positive. For m ≥ 1 the coefficient c_m^lo is
  ≥ 0 and (ln q)^{−m} ≥ r_q^{−m}, so the sum is ≥ G ≥ 0. Then
  p/ln p ≥ p/r_p > 0 and g_S(ln q) ≥ G ≥ 0. Multiplying,
  (p/ln p)·g_S(ln q) ≥ (p/r_p)·G.
- **Lemma Q.** ln n_f ≥ λ_f ≥ J + 1. Each term satisfies
  c_m n_f (ln n_f)^{−m−1} ≥ c_m^lo n_f r_f^{−m−1}, because c_m ≥ c_m^lo ≥ 0
  and 0 < ln n_f ≤ r_f. ∎

The rational checker uses exactly this substitution. The Arb checker does
not need it: it carries each L_k as the ball spanning its whole enclosure
[L_lo, L_hi], and each ln as an Arb ball.

## 4. The theorem: stages, inputs, inequalities

**Choices.**

- α = ½, X₀ = 59, γ = 3/2, Y₀ = 10⁹ (any Y₀ in (1, 10⁹] would do, since
  every n used is ≥ 10⁹), and J = 6 throughout.
- Four stage sets, all prefixes G(M) with M on the [C] grid:

| Stage | S | \|S\| | max S | 59·max S | β(S) | used on |
|---|---|---|---|---|---|---|
| 1 | G(110,000) | 2,063 | 110,000 | 6,490,000 | 170,282 | [10⁹, 10¹⁰] (Lemma P) |
| 2 | G(160,000) | 2,938 | 159,936 | 9,436,224 | 322,537 | [10¹⁰, 10¹¹] (Lemma P) |
| 3 | G(210,000) | 3,795 | 210,000 | 12,390,000 | 514,970 | [10¹¹, 10¹²] (Lemma P) |
| F | G(28,653,696) | 413,980 | 28,653,696 | 1,690,568,064 | 3,348,506,095 | [10¹², ∞) (Lemma Q) |

How these were chosen (float scratch; not evidence):

- Pieces are decades, for round endpoints.
- For each piece, the set is the grid M that maximises (p/ln p)g_S(ln q)/β.
- The tail starts at 10¹², the first power of ten at which Lemma Q closes
  with a margin: the ratio to β is 1.98 at 10¹², and 0.25 at 10¹¹.
- G(28,653,696) is the [C] grid set the earlier proof also used. Grid sets
  with L₀ > ½ start at M = 1.7·10⁷.
- With these choices the theorem's surplus is set by piece 1. The lead's
  one-piece scout ([10⁹, 10¹²] with G(290,000)) reaches about 4.4·10⁵; this
  split gives 9.2·10⁵ and far larger relative margins on pieces 2 and 3.

**Hypotheses that are pure integer facts** (checked by both checkers, and
checkable by eye):

- **Validity of (3.1), "p ≥ 59·max S".** Each left end is at least 59·max S:
  10⁹ ≥ 6,490,000; 10¹⁰ ≥ 9,436,224; 10¹¹ ≥ 12,390,000;
  10¹² ≥ 1,690,568,064. So (H↓) is applied only at x = n/a ≥ 59, and in fact
  only at x ≥ p/max S. The smallest such value is 10⁹/110,000 = 9,090.9…
  (§5).
- **p ≥ e and p ≥ Y₀**: every p ≥ 10⁹.
- **ln n_f ≥ J + 1 = 7**: n_f = 10¹² > 3⁷ = 2,187 > e⁷.
- **Coverage.** [10⁹, 10¹⁰], [10¹⁰, 10¹¹], [10¹¹, 10¹²] and [10¹², ∞) are
  closed, share their endpoints, and cover every integer n ≥ 10⁹.

**Inputs** [C], 2026-10-31. N, max S, β and enclosures [L_lo, L_hi] of
L₀…L₆, for the four sets. They come from:

- **`results/rs62/moments-grid.txt`**, from `comp-rs62` @ `2712e14`,
  sha256 `f0bc09ad…53a0a5a6`. Its method:
  - τ by an additive divisor-count sieve;
  - largest prime factors by a separate sieve;
  - π(g) by numpy Eratosthenes;
  - sums in Arb balls at 256 bits, outward-rounded to 32 digits.
- **`verify/rs62/moments-grid.txt`**, from `check-rs62` @ `67a10cd`,
  sha256 `ffed2c34…787793f3`. Its method:
  - τ by factorisation over its own linear-sieve spf table;
  - π(g) by PARI `primepi`;
  - sums in gmpy2/MPFR at 200 bits, with every operation, including log,
    rounded toward −∞ for lo and toward +∞ for hi.
- The 380 data lines are byte-identical; the files differ only in their
  comments.
- Both generator lists hash to `0be671d9…c6edaed18f`. That is the sha256 of
  the refereed [C] list of `colton-threshold.md`.
- The [C] label is `lead-colton-rs62`'s (ticket, 2026-10-31). The lead read
  both core loops, and re-ran every program from committed code.

`colton-threshold-rs62-inputs-build.py` reads both and refuses unless:

- the 380 grid values of M are present, in order;
- the integers agree exactly;
- every pair of L_k enclosures overlaps;
- every endpoint is a 32-significant-digit outward-rounded decimal.

As a further cross-check, M = 28,653,696 is compared with the earlier
refereed computation, `colton-threshold-inputs.json`. The build script copies
the endpoint strings verbatim into the two JSON files.

The lower endpoints, truncated to 30 significant digits, so they are still lower
bounds. The tables below are printed by
`colton-threshold-rs62-check-rational.py --tables`. Lower bounds are truncated
and upper bounds are rounded up.

| S | L₀ | L₁ | L₂ | L₃ | L₄ | L₅ | L₆ |
|---|---|---|---|---|---|---|---|
| G(110,000) | 0.421246729295455220483591562119 | 1.91076476728556712067241467064 | 12.1171366799006452511253777796 | 95.6817680716118684879166892892 | 848.175421652057824273572783032 | 7999.34662283919440461229463068 | 78320.2674167894092763899709717 |
| G(160,000) | 0.427797769197507463586618867266 | 1.98804428125013867653653696503 | 13.0288429564390556805988726520 | 106.438539077470045734553099182 | 975.099875964109460503724609955 | 9497.11643439547286583183055707 | 95996.1540283438660086795733745 |
| G(210,000) | 0.432454092753326788549854204240 | 2.04447824772965164111567330638 | 13.7128434594135030297579544276 | 114.729229184053861206494548977 | 1075.59462132896457613490755876 | 10715.3047534513348997410919601 | 110763.549496499938306218252385 |
| G(28,653,696) | 0.508000047238841733452073262987 | 3.14950355230516058989272826631 | 30.0282903033822207339992138297 | 357.841623549235450947560606454 | 4730.46992866496347919355857011 | 66131.6237995009360562091529310 | 957831.456465890104236918584216 |

**Coefficients (3.3)** at the lower endpoints, to 10 significant digits:

| S | c₀ | c₁ | c₂ | c₃ | c₄ | c₅ | c₆ |
|---|---|---|---|---|---|---|---|
| G(110,000) | −0.07875327070 | 1.371388131 | 14.02790144 | 113.8574730 | 1039.538957 | 10119.78517 | 102318.3072 |
| G(160,000) | −0.07220223080 | 1.451943165 | 15.01688723 | 125.9818035 | 1187.976954 | 11934.86612 | 124487.5033 |
| G(210,000) | −0.06754590724 | 1.510705294 | 15.75732170 | 135.2984943 | 1305.053079 | 13404.29130 | 142909.4637 |
| G(28,653,696) | 0.008000047238 | 2.653503575 | 33.17779385 | 402.8840590 | 5446.153175 | 77957.79862 | 1156226.327 |

So:

- in every row, c₁ … c₆ > 0, which is the hypothesis of Lemma P;
- in the last row, every c₀ … c₆ ≥ 0, which is the hypothesis of Lemma Q.

**c₁ is the only coefficient that could fail.** c₂ … c₆ are sums of positive
terms. c₁ = L₁ + L₀/2 − 3/4 subtracts a constant. But every term
(ln a)^k/a is ≥ 0, so L₀ and L₁ are nondecreasing in M. Hence in every stage
L₁ ≥ L₁(G(110,000)) ≥ 1.91, and so c₁ ≥ 1.37.

**c₀ in the tail.** c₀ = L₀ − ½ = 0.0080000472… is positive by 1.6% of L₀.
That is a real margin, not a hair. The "4.7·10⁻⁸" in this chat's brief is the
margin of L₀ over Zelinsky's 0.508, not over ½. Even so, the tail's
tolerance to an across-the-board overstatement of the L_k is exactly that
1.57%, because c₀ ≥ 0 is the first hypothesis to break.

**The four inequalities.** In each row, ln p and ln q are upper bounds and
g_S, the left side and the surplus are lower bounds, as in Lemma M. All
values are from the rational checker.

| S | piece [p, q] | ln p ≤ | ln q ≤ | g_S(ln q) ≥ | (p/ln p)·g_S(ln q) ≥ | β | surplus ≥ | ratio ≥ |
|---|---|---|---|---|---|---|---|---|
| G(110,000) | [10^9, 10^10] | 20.7232658370 | 23.0258509300 | 0.02253813745 | 1087576.52530 | 170,282 | **917294.5253** | 6.386 |
| G(160,000) | [10^10, 10^11] | 23.0258509300 | 25.3284360230 | 0.02078650059 | 9027462.50714 | 322,537 | **8704925.507** | 27.98 |
| G(210,000) | [10^11, 10^12] | 25.3284360230 | 27.6310211160 | 0.01757325792 | 69381535.8700 | 514,970 | **68866565.87** | 134.7 |

The tail, by Lemma Q, with S = G(28,653,696), n_f = 10¹²,
ln n_f ≤ 27.6310211159285482082158974563:

| m | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| term ≥ | 289531360 | 3475568100 | 1572739100 | 691181880 | 338146710 | 175177350 | 94029539 |

The sum is ≥ 6636374158.03 ≥ β = 3,348,506,095. So the surplus on [10¹², ∞) is **≥ 3287868063.03**, and the ratio to β is ≥ 1.981.

**Proof of the Theorem.** Apply Lemma P to the three pieces, and Lemma Q to
the tail, with the substitutions of Lemma M. Every hypothesis is listed
above, and both checkers verify each one. The smallest surplus is piece 1's,
917,294.5… ≥ 917,294. ∎

**The two checkers** (2026-10-31). Both exit 0 on both input files, and both
print the same four surpluses.

- **`colton-threshold-rs62-check-rational.py`.**
  - Every number is a Python `Fraction`. Each L_k enters as its lower
    endpoint, read as an exact decimal.
  - ln n is enclosed by writing n = 2^e·y with 1 ≤ y < 2. Then
    ln y = 2 atanh((y−1)/(y+1)) is summed to 50 terms. The tail is bounded by
    a geometric series of ratio z² ≤ 1/9, so the remainder is < 10⁻⁴⁷.
  - The upper ends of the ln enclosures go into the denominators, and the
    lower end into "ln n_f ≥ 7" (Lemma M).
  - It also checks coverage, the validity conditions, and the sign
    conditions.
- **`colton-threshold-rs62-check-arb.py`.**
  - python-flint Arb balls at 256 bits, with Arb's own logarithm.
  - Each L_k is the ball spanning [L_lo, L_hi], so this checker does not use
    Lemma M's monotonicity.
  - It evaluates g_S by Horner's rule in 1/u, which is a different
    evaluation order from the rational checker.
  - A statement X ≥ 0 is accepted only if the whole ball lies in [0, ∞).
- Both were tested on a scratch grid computed from my own generator list
  (C sieve, Arb sums). They reproduce the float scout's surpluses to every
  printed digit.
- They were also tested by fault injection. With L₀(G(28,653,696)) set to
  ½, both report FAIL on c₀ ≥ 0. With β(G(110,000)) set to 2·10⁶, both
  report FAIL on piece 1.

## 5. Exactly which part of RS62 is leaned on

**(3.2), the upper bound.** It is applied only in Proposition B, at x = n,
for integers n ≥ 10⁹. `literature/colton.md` reports that RS62 prove (3.2)
for 10⁸ ≤ x ≤ e³⁷⁵ by Lemma 2 with Theorem 29, and beyond e³⁷⁵ by Lemma 3
with Theorem 31. That is RS62's analytic range [L, READ by `lit-colton-rs62`
as a proof outline only].

**(3.1), the lower bound.** It is applied in Proposition A at x = n/a, for
every stage, every n in the stage's range, and every a ∈ S. So x runs over
[p/max S, ∞) for each stage. The lower ends are:

| stage | p / max S |
|---|---|
| 1 | 10⁹/110,000 = 9,090.9… |
| 2 | 10¹⁰/159,936 = 62,525.0… |
| 3 | 10¹¹/210,000 = 476,190.4… |
| F | 10¹²/28,653,696 = 34,899.5… |

So **(3.1) is used at every real x ≥ 9,090.9**, and that includes all of
[9,090.9, 10⁸). That is RS62's table-dependent range: they derive (3.1) from
(3.3), and prove (3.3) for x ≤ 10⁸ by Lemma 4 with Theorem 16, which rests on
tables (`literature/colton.md`).

`literature/colton.md` originally said that "the table-dependent range below
10⁸ is not used". That is true for (3.2) and false for (3.1). It was
corrected on 2026-10-31 (PR #38).

This cannot be engineered away. Using (3.1) only on x ≥ 10⁸ would force
max S ≤ p/10⁸. At p = 10⁹ that is max S ≤ 10, i.e. S ⊆ G(10) = {8}, with
L₀ = 1/8. No piece starting at 10⁹ closes with that.

**What RS62 itself rests on below 10⁸.** `literature/colton.md` (correction
of 2026-10-31) records how RS62 prove (3.1) there:

- below 10⁸, through Theorem 16 and the Appel–Rosser 1961 tabulation;
- below 16,000, through the Rosser–Walker tabulation.

The Appel–Rosser report is NOT READ and could not be obtained. RS62 do not
say how finitely many tabulated points cover every real x. So below 10⁸ the
[L] citation is qualified: it points to a computation nobody here can
inspect. **The Theorem therefore does not use RS62 for (3.1) below 10⁹.** It
uses the project's own [C] check, below.

**(3.1) on [59, 10⁹] is [C] here** (2026-10-31). The two files have
identical data lines:

- `results/rs62/rs62-lower.txt`, from `comp-rs62-lower` @ `5beace1`:
  segmented Eratosthenes, and every interval evaluated in FLINT Arb balls at
  128 bits;
- `verify/rs62/rs62-lower.txt`, from `check-rs62-lower` @ `acfa694`: sieve
  of Atkin, and every interval evaluated in MPFR at 128 bits with directed
  rounding.

No step in either is in floating point. Both report INTERVALS 50,847,518,
which is π(10⁹) − π(58) = 50,847,534 − 16, and PASS. The lead read both and
re-ran both from committed code.

| block | min slack π(q) − f(q′) ≥ | at q |
|---|---|---|
| [59, 100) | 0.170566 | 61 |
| [10², 10³) | 1.076985 | 113 |
| [10³, 10⁴) | 12.051857 | 1009 |
| [10⁴, 10⁵) | 82.139136 | 10039 |
| [10⁵, 10⁶) | 524.880187 | 100237 |
| [10⁶, 10⁷) | 3493.861600 | 1000099 |
| [10⁷, 10⁸) | 24903.718139 | 10000609 |
| [10⁸, 10⁹] | 185418.872767 | 100000193 |

**From finitely many checks to every real x** [T]. Let
f(x) = (x/ln x)(1 + 1/(2 ln x)), and write L = ln x.

- **f is increasing on [59, ∞).** f(x) = x/L + x/(2L²), so

  f′(x) = 1/L − 1/L² + 1/(2L²) − 1/L³ = 1/L − 1/(2L²) − 1/L³ = (2L² − L − 2)/(2L³).

  The numerator is positive exactly when L > (1 + √17)/4 = 1.2807…. At
  x = 59, L = ln 59 = 4.077… > 1.29, and L only increases. So f′ > 0 on
  [59, ∞).
- **The intervals.** Let q < q′ be consecutive primes with 59 ≤ q ≤ 10⁹.
  The last such q is 999,999,937, whose successor exceeds 10⁹. Each real
  x ∈ [59, 10⁹] lies in exactly one set I_q = [q, min(q′, 10⁹)), except
  x = 10⁹, which belongs to the last interval taken closed. This works
  because 59 is prime and is the smallest q used.
- **π is constant on I_q**, equal to π(q), since no prime lies strictly
  between q and q′.
- **The check.** The files assert slack(q) = π(q) − f(q′) > 0 for every
  q < 999,999,937, and π(q) − f(10⁹) > 0 for the last q.
- **Every real x.** For x ∈ I_q we have x < q′ (or x ≤ 10⁹ for the last
  interval), and f is increasing. So f(x) < f(q′), or f(x) ≤ f(10⁹). Hence
  π(x) = π(q) > f(x).

So π(x) > f(x) for every real x ∈ [59, 10⁹], which is (3.1) on that range. ∎

**A third, non-team confirmation** (referee, not [C]). The referee's own
programs give the same block minima to all six printed digits:

- `referee/colton-threshold-rs62/rs62every.c`: every interval, in Arb at
  128 bits;
- `referee/colton-threshold-rs62/rs62low.py`: Arb, with a different
  decomposition of the range.

Both are referee-side checks, not team [C].

**So RS62 Theorem 1 [L] is relied on only for:**

- (3.1) at real x > 10⁹;
- (3.2) at integer x ≥ 10⁹.

Both are inside RS62's analytic range x ≥ 10⁸.

## 6. The hard step

**What has to be done.** Infinitely many n must be reduced to finitely many
checked numbers. The gain from ln(n/a) < ln n must survive the reduction,
because without it RS62's weaker constants do not close at 10⁹. That is the
whole of §3. It rests on three things.

1. **Proposition A's truncation is a lower bound.** That needs every
   discarded term to be ≥ 0:
   - ℓ > 0 (a ≥ 8);
   - ℓ < u (n/a ≥ X₀ > 1);
   - α ≥ 0.

   Dusart's α = 1 and RS62's α = ½ both satisfy this. The α = ½ only scales
   the second series.
2. **The sign conditions.**
   - Lemma P needs c₁ … c₆ ≥ 0. Only c₁ = L₁ + L₀/2 − 3/4 could fail, and it
     is ≥ 1.37.
   - Lemma Q needs c₀ ≥ 0, i.e. L₀(G(28,653,696)) ≥ ½. It holds by 0.008.
3. **Validity of (3.1) at every x = n/a it is applied to.** That is
   p ≥ 59·max S for every stage, which is integer arithmetic. It also
   includes the range point of §5: (3.1) is used down to x ≈ 9,091.

**Status: done** [T, 2026-10-31; refereed, ref-colton-rs62 ACCEPT (round 3, 2026-10-31; round 2 REVISE R1 fixed at 96b2919), report `referee/colton-threshold-rs62.md`]. No step is left to the
reader. Where this file differs from `colton-threshold.md` §3:

- the constants are general;
- J = 6;
- Lemma M states the substitution that the checkers make, which the earlier
  file left implicit in its checker docstrings.

**What I did not find hard, and a referee should still check:**

- the m-reindexing in Proposition A;
- the m = 1 bookkeeping in Proposition B (c₁ absorbs −γ/2);
- the direction of every substitution in Lemma M.

## 7. Sanity checks (observed, one program each; not part of the proof)

- **Float scout** (numpy float64 cumulative moments over my own generator
  list, in scratch) gives the same four surpluses as the checkers to 9
  digits.
- **Tolerances**, by bisection in float:
  - L_k scaled down by a common factor 1 − ε: the pieces fail at
    ε = 3.42%, 3.64% and 3.20%, and the tail at 1.57% (through c₀);
  - β: the pieces tolerate a factor 6.4, 28 and 135, and the tail 1.98.
- **The analytic bound against the truth at n = 10⁹.** With G(110,000), the
  pointwise (n/u)g_S(u) − β at n = 10⁹ is about 1.88·10⁶. The true value is
  T(10⁹) − π(10⁹)/2 = 32,608,999 − 25,423,767 = 7,185,232 (exact range,
  `referee/colton-range.md`). So the bound sits below the truth, as it must.
- **The exact value over piece 1, from the adversary** (adversary-side
  evidence, not team [C], and not used by the Theorem).
  `adversary/colton-rs62.md` computes T(n) − π(n)/2 at every integer
  n ∈ [10⁹, 10¹⁰], with two implementations of its own. The minimum is
  7,185,230.5, at n = 1,000,000,021. That is 7.8 times the Theorem's
  constant of 917,294.
- **My generator list** (`colton-threshold-sanity-gen.c`, run in scratch to
  28,653,696) has 413,980 elements. Its Arb moment sums agree with
  `colton-threshold-inputs.json` at M = 28,653,696 to all 32 digits.

## 8. What was not established

1. **Referee status:** refereed, ref-colton-rs62 ACCEPT (round 3, 2026-10-31; round 2 REVISE R1 fixed at 96b2919), report `referee/colton-threshold-rs62.md`.
2. **RS62 Theorem 1 is [L], READ as a statement, not checked as a proof.**
   - It is relied on only for (3.1) at x > 10⁹ and (3.2) at x ≥ 10⁹ (§5).
   - Below 10⁹, (3.1) is this project's [C] (`rs62-lower.txt`, two
     implementations, every interval rigorous).
   - RS62's own proof below 10⁸ rests on an unread tabulation
     (`literature/colton.md`, correction of 2026-10-31). That is why the
     Theorem does not use it there.
3. **Independence of the two checkers is of code and method, not of author.**
   I wrote both.
4. **No attempt to lower 10⁹.** The exact range reaches 10⁹, so a lower start
   buys nothing.
   - Float scout, not evidence: from 10⁷ with RS62, small sets have c₁ near
     zero or negative, and the chain is much tighter.
   - I did not establish where the RS62 chain's floor is.
5. **No novelty claim** (see "The answer").

## 9. Reproduce

Machine: PC2 (8 cores, WSL2). Date: 2026-10-31. Each command takes under a
second.

```
PY=~/dev/projects/open-problems/.venv/bin/python
# rebuild the two input files from the two [C] grids (asserts they agree)
$PY findings/colton-threshold-rs62-inputs-build.py
# two checkers x two input files; all four must exit 0
for f in findings/colton-threshold-rs62-inputs.json findings/colton-threshold-rs62-inputs-verify.json; do
  $PY findings/colton-threshold-rs62-check-rational.py $f
  $PY findings/colton-threshold-rs62-check-arb.py $f
done
```
