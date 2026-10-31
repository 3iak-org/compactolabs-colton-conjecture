# Adversary: Colton's conjecture, π(n) ≤ 2T(n) for every n ≥ 1

*`adv-colton`, opened by `dev`, 2026-10-31. Branch `agent/adv-colton`.
Target: the claim on `lead-colton` @ `bfebd85` (the brief's `41adad0` plus one
master-plan commit). That is `findings/colton-threshold.md` (n ≥ 10⁷), plus
`results/range/` and `verify/range/` (1 ≤ n ≤ 10⁹). The combined
`findings/colton-conjecture.md` did not exist on that branch when I looked, so
I attacked the two halves and the seam between them. Scripts and outputs are in
`adversary/colton/`. I did not read `search/range/`, `verify/range/` or the
team's generator code before writing mine; my code shares none of it.*

## Verdict

**No counterexample. I could not break the claim.** Every attack below came
back clean. The claim survives the attacks I knew how to make.

- **Statement:** it is the right one.
- **Low range:** recomputed exactly by a third method.
- **Proof inputs:** recomputed.
- **The five inequalities:** re-evaluated.
- **The analytic bound:** tested against the exact count at every n where
  both are available.

I found one wrong number and one robustness fact:

- **Wrong number (text only, does not affect the claim).**
  `results/range/README.md` line 11 says "Margin at n = 10^9: 14355343". The
  margin 2T − π at n = 10⁹ is **14,370,464** (= 2·32,608,999 − 50,847,534).
  The 14,355,343 is m₁₀₀₀, the *minimum over primes* in the last block
  (999·10⁶, 10⁹], which is a different quantity. The checkpoint files label
  their columns correctly; only the README sentence is wrong. The owner is
  `lead-colton`.
- **Robustness: the claim does not need Dusart.** Dusart (6.5) is the one
  input nobody has read in its refereed form. Replace it by Rosser–Schoenfeld
  1962 Theorem 1 and start at 10⁹, where the exact range ends, and the same
  chain still closes, with margin (§5). This has two limits:
  - it is a float exploration, not a certificate;
  - I could not read RS62 itself.

  But it means a defect in the published Dusart pair would not, on present
  evidence, sink the conjecture. It would only move work around.

**What would have to be true for "no counterexample" to be wrong:**

1. **A wrong analytic input.** Beyond 10⁹ nothing here is exhaustive. There
   the claim rests on the threshold theorem's chain and its cited π bounds.
   My checks of that chain are re-derivation and recomputation, not a second
   proof.
2. **A shared misreading of the definition.** My code, the team's two range
   implementations and the referee's PARI script would all have to share it.
   §1 compares the definition against the formal statement verbatim, which is
   the defence against that.

## 1. Is the statement Colton's conjecture? Yes. [checked 2026-10-31]

`formal-conjectures` @ `b6939a3`, `FormalConjectures/OEIS/111291.lean`, READ:

```
def countRefactorableNat (m : ℕ) : ℕ := (Icc 1 m).filter (fun k => k.divisors.card ∣ k) |>.card
theorem colton_conjecture : ∀ n : ℕ, Nat.primeCounting n ≤ 2 * countRefactorableNat n
```

| Question from the brief | Answer |
|---|---|
| Does k = 1 count? | **Yes.** It is in `Icc 1 m`, and τ(1) = 1 divides 1. The team's T(n) = #{1 ≤ k ≤ n : τ(k) \| k} also includes it (T(1) = 1, A111291 a(0) = 1). k = 0 is excluded by `Icc 1`. That matters, since in Mathlib `(0).divisors.card = 0` and `0 ∣ 0`. |
| ≤ or <? | **≤** throughout: in π, in T and in the inequality. Strict is false at n = 7: T(7) = 2 (namely 1, 2) and π(7) = 4. Both range implementations report equality at n = 7 only, and so does mine (§2). |
| n real or integer? | **ℕ**, including n = 0, where π(0) = 0 ≤ 0. Neither range file starts at 0, but the case is trivial. A real-x version, π(x) ≤ 2T(⌊x⌋) for real x ≥ 0, is equivalent, because both sides are step functions that jump only at integers. |
| `Nat.primeCounting n` | π(n), the number of primes ≤ n (Mathlib defines it as `primeCounting' (n+1)`). That matches the team's π. |

The OEIS %C form "T(x) ≥ x/(2 log x)" is a **different** statement. In the
∀-real form it is false on (1, 2), as `literature/colton.md` §4 says.
formal-conjectures marks its eventual form as solved. The team's claim is
about the π form only, and should say so in the combined file.

## 2. The low range, recomputed by a third method [C-supporting, 2026-10-31]

`adversary/colton/dsieve.c`, compiled with gcc -O2 and run with
`nice -n 19` as 2 processes (blocks 1–500 and 501–1000 of 10⁶ each); all
1000 blocks took seconds of wall time. The method was chosen to be unlike
both team implementations:

- **τ(n) by divisor-pair counting.** For each d ≤ √hi, every m = d·e in the
  segment with e ≥ d adds 2, or 1 if e = d. It never factorises anything.
- **Primes by a separate segmented Eratosthenes bitmap,** not by τ = 2. The
  program asserts τ(n) = 2 ⇔ n prime at every n ≤ 10⁹. The assertion never
  fired.
- **The margin 2T − π is tracked at every n,** with the minimum both over all
  n and over primes only.

Results (`adversary/colton/blocks.txt`, sha256 `0b5b29c7…be838f7`;
`combine.out`; `v1.txt`):

- **Equality π(n) = 2T(n) occurs only at n = 7.** Every n ≤ 10⁶ was checked
  one at a time. The 12 values of n ≤ 1000 with margin ≤ 2 are identical to
  the team's list: 1, 3, 4, 5, 6, 7, 8, 53, 54, 55, 71 and 79.
- **On (10⁶, 10⁹] the minimum margin is 10,910,** at n = 1,000,697. The next
  smallest block minimum is 22,672, at 2,000,003.
- **T(10⁶), T(10⁷), T(10⁸), T(10⁹)** = 44,705, 394,240, 3,558,181,
  32,608,999. **π** at the same points = 78,498, 664,579, 5,761,455,
  50,847,534. π(10⁹) also agrees with PARI `primepi`.
- **All 1000 lines of `results/range/checkpoints.txt` match mine exactly** in
  (n, T(n), π(n), m_k), with m_k the block minimum over primes. That file's
  sha256 equals `verify/range/checkpoint.txt`, so this is agreement with both.
  - My first comparison found 84 lines differing by 1–7 in the last column.
    The cause was that I had taken the minimum over *all* n and they over
    primes. In a block that opens with a refactorable non-prime, the minimum
    over all n can sit at the block's first n, below every prime's margin.
  - Once both sides compute the same quantity there are 0 differences.
  - The difference does not touch the claim: the global minimum is the same
    either way.
- **The margin at n = 10⁹ is 14,370,464,** not the README's 14,355,343 (see
  Verdict).

So the [C] for 1 ≤ n ≤ 10⁹ is now backed by three implementations, with no
shared code and three different ways of computing τ.

## 3. The proof's computed inputs, recomputed [2026-10-31]

Script: `adversary/colton/gen.py`, output in `gen.out` and `coefs.txt`.

- G(M) = {a ≤ M : 2τ(a) | a}. τ is computed with numpy divisor-pair slicing,
  with no factoring.
- g(a) comes from `sympy.factorint`, and π(g) from a numpy Eratosthenes
  cumulative sum.
- L_k is computed in gmpy2 mpfr at 320 bits. That is neither Arb nor PARI, so
  it is a third arithmetic.

For M = 16,694, 166,944 and 28,653,696 I get:

| M | N | max G | β |
|---|---|---|---|
| 16,694 | 352 | 16,668 | 7,453 |
| 166,944 | 3,055 | 166,944 | 346,644 |
| 28,653,696 | 413,980 | 28,653,696 | 3,348,506,095 |

L₀…L₄ agree with the table in `colton-threshold.md` §4 to all 30 printed
digits, and so do c₀…c₄ to 12. One point carries Zelinsky's whole margin:
L₀(G(M_Z)) = 0.50800004723884…, above ½ by 0.008. I reproduce it.

## 4. The five inequalities, and the analytic bound against the truth [2026-10-31]

**The inequalities.** `adversary/colton/ineq.py` evaluates them in mpmath
(60 digits) from my own coefficients. The hypotheses hold:

- c₁…c₄ > 0 in both finite stages;
- every c ≥ 0 for the tail set;
- 599·max S ≤ the left end of every piece: 9,984,132 ≤ 10⁷,
  99,999,456 ≤ 10⁸, and 1.716·10¹⁰ ≤ 10¹²;
- ln 10¹² ≥ 5.

Surpluses: **5203.946, 3616.599, 81424.42, 861123.0 and 3.7689·10⁹**. These
are the team's numbers.

**The Dusart ranges.** The brief asked whether the analytic inputs are used
outside their stated ranges. They are not:

- the lower bound is used only at x = n/a ≥ 599, by the condition just
  listed;
- the upper bound is used only at x = n ≥ 10⁷ > 1.

**The analytic bound against the exact count.** This is the attack on "a bound
that holds at checkpoints but fails between them". At **every integer** n in
[10⁷, 10⁹], dsieve computes the right-hand side R(n) of (3.3),
(n/u)·g_S(u) − β, with the stage set the theorem assigns to n. It then
compares 2R(n) with the exact 2T(n) − π(n).

- If (1.1), Proposition A or Dusart were wrong, this is where it would show.
- The minimum of 2(T − π/2) − 2R over the range is **+93,911**, at
  n = 10,000,007. That is double precision, against a margin of thousands.
- The bound is below the truth everywhere: as tested, it is never violated.
- Above 10⁹ the pieces are continuous in n. Lemma P's monotonicity argument
  covers them, and I re-derived it: g_S is nonincreasing because
  c_{m≥1} > 0, and x/ln x is increasing.

**The seam.** The theorem covers n ≥ 10⁷ inclusive, and the exact range
covers 1 ≤ n ≤ 10⁹. They overlap on [10⁷, 10⁹]. No n is missed, and n = 0
is trivial.

## 5. Does the claim depend on Dusart (6.5)? Apparently not. [exploration, 2026-10-31]

The theorem's one unread input is the refereed form of Dusart's pair
(`literature/colton.md`, lit-colton-dusart: the published version is
paywalled and unread). Since the exact range already runs to 10⁹, the
analytic part only has to start at 10⁹. I re-ran the team's chain with
general constants:

- lower bound π(x) ≥ (x/v)(1 + α/v) for x ≥ X₀;
- upper bound π(x) ≤ (x/v)(1 + γ/v);
- hence c₁ = L₁ + αL₀ − γ/2 and c_m = L_m + αmL_{m−1}.

The constants are Rosser–Schoenfeld 1962, Theorem 1: α = ½ with X₀ = 59, and
γ = 3/2 for x > 1. Script `adversary/colton/robust.py` (J = 6), output
`robust-rs62.out`. A greedy search over prefix sets G(M) finds:

- **piece [10⁹, 5.62·10¹²], S = G(287,050), β = 885,114: surplus 57,719;**
- **tail n ≥ 5.62·10¹², S = G(28,653,696): surplus 2.8·10¹⁰.**

Limits on this:

- **Float64 moments.** The surplus is 6.5% of β, which float64 error cannot
  close, but the result is still not certified.
- **RS62 is [L, CITED, not read].** Project Euclid refused scripted download
  (bot wall, 2026-10-31). The constants are from memory, consistent with the
  corpus's own citation of RS62 in `09-number-theory.md`.
  - `adversary/colton/bounds.py` checks both pairs at every prime ≤ 10⁹
    (left limits for the lower bounds). This is a sanity check, not a proof.
  - RS62 holds there with minimum slack 0.17 (lower, at 67) and 1.49 (upper,
    at 113).
  - Dusart (6.5) holds with 0.0145 (lower, at 1423) and 0.0029 (upper, at
    1627). Those are the team's figures.
- **Proposal for `lead-colton`, not a correction.** A rigorous version of
  this backup would take the theorem off Dusart altogether, with RS62 as its
  only input: refereed since 1962, open access, and widely re-used. Buying
  Dusart 2018 then stops mattering. It needs:
  - the moments of G(287,050) as [C];
  - one rational check;
  - someone to read RS62 Theorem 1.

## 6. What I did not establish

- **No exhaustive check beyond 10⁹.** Above 10⁹ the claim is only as good as
  the threshold chain and its π bounds. My work there is recomputation and
  re-derivation:
  - Proposition A, Proposition B, Lemma P, Lemma Q and Lemma 20 (b), checked
    line by line. I found nothing wrong.
  - This is **not a referee's report.** I did not audit the team's rational
    or Arb checkers. My own evaluation is in non-rigorous 60-digit floats.
- **Zelinsky's Theorem 22 was not attacked separately.** The new threshold
  supersedes it, and nothing here uses it.
- **My tail spot-checks lean on literature values.** The OEIS a(10) and
  a(11), against π(10¹⁰) and π(10¹¹), give margins of about 1.5·10⁸ and
  1.5·10⁹. Those are [L] (A111291 data), not recomputed.
- **RS62 not read** (§5). **Dusart 2018 not read** (the team's own open item).

## Reproduce

Python is `~/dev/projects/open-problems/.venv/bin/python`; run from
`adversary/colton/`.

```
gcc -O2 -o $TMPDIR/dsieve dsieve.c -lm
python gen.py coefs.txt > gen.out                      # inputs, ~1 min
python ineq.py coefs.txt                               # five inequalities
$TMPDIR/dsieve 1000000000 1000000 1 1 coefs.txt v > v1.txt
$TMPDIR/dsieve 1000000000 1000000 1 500 coefs.txt > a.txt &
$TMPDIR/dsieve 1000000000 1000000 501 1000 coefs.txt > b.txt; wait
cat a.txt b.txt > blocks.txt; python combine.py blocks.txt
python bounds.py 1e9; python robust.py 1000000000
```

Machine PC2 (WSL2, 8 cores, 2 used, nice 19), 2026-10-31.
