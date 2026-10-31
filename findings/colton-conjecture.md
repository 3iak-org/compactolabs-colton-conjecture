# Colton's conjecture (OEIS A111291): π(n) ≤ 2T(n) for every integer n ≥ 1

*`thm22`, on `lead-colton`'s ticket of 2026-10-31. Branch `agent/thm22`.
Revised 2026-10-31 on `lead-colton` @ `37c3c75` for the finite-range referee
(`referee/colton-range.md`: R1, R2, R5, R6) and the adversary
(`adversary/colton.md`). Revised again on `lead-colton` @ `5509461` for
`check-range2` and the Rosser–Schoenfeld read. Revised 2026-10-31 by `lead-colton` for prior work (OEIS A323326):
prose only, no change to the mathematics or the certificate. Nothing here
was sent outside this repo.*

## The answer

> **For every integer n ≥ 1, π(n) ≤ 2T(n).** Here T(n) = #{1 ≤ k ≤ n : τ(k) | k}
> and τ is the number of divisors.
>
> - It also holds at n = 0, where it reads 0 ≤ 0, so the statement holds
>   for every n ∈ ℕ.
> - **Equality holds exactly for n ∈ {0, 7}** over ℕ, and only at **n = 7**
>   for n ≥ 1. At n = 7, T(7) = 2 and π(7) = 4. So the statement must be ≤,
>   and the strict form π(n) < 2T(n) is false at n = 7, and at n = 0.
> - This is exactly `OeisA111291.colton_conjecture` in formal-conjectures
>   (`∀ n : ℕ, Nat.primeCounting n ≤ 2 * countRefactorableNat n`; §3).
>
> **This settles only the π form, π(n) ≤ 2T(n).** It does not settle
> Colton's second sentence, that the number of refactorables less than x is
> at least x/(2 log x) for all real x. That is a different statement, it is
> not claimed here in any form, and in its ∀-real-x form it is false on
> (1, 2) (`literature/colton.md` §4).

## Prior work: the full statement was already claimed settled in 2019

**This is not the first proof.** OEIS **A323326** (Jud McCranie,
2019-01-11), "a(n) = 2*T(n) - pi(n)", says in its comments that Zelinsky
proved the result for n > 7.42·10¹³, and then:

> "This calculation went to 7.44*10^13, proving the conjecture."

[L, READ 2026-10-31 by `lit-colton-novelty`: `literature/colton-novelty.md`
§1. Verdict there: the full statement is KNOWN as a claim, unrefereed, with
no method, program or output published, resting on Zelinsky's Theorem 22
as a black box.] A111291 does not link to
A323326, which is why the first literature pass (`literature/colton.md`) and
formal-conjectures both missed it. The "n ≤ 500" figure in
`literature/colton.md` §3 is therefore superseded.

So the finite range is **not new**, and nothing in this file is claimed as a
first proof. In one line: **an independent, reproducible, refereed proof
with threshold 10⁷ that removes the dependence on Theorem 22's unpublished
numbers. Not a first proof.** In more detail:

- **(a) An independent, refereed, reproducible verification** of the whole
  statement. McCranie's is a one-sentence OEIS comment with no code, no
  b-file and no paper, and it rests on Zelinsky's Theorem 22 as published.
  Here:
  - the threshold is re-derived and refereed;
  - the finite range is computed by five implementations across two
    methods, with a published checkpoint certificate (§2) and a written
    reduction lemma;
  - an adversary hunted for a counterexample and found none.
- **(b) The threshold lowered from 7.42·10¹³ to 10⁷** (`colton-threshold.md`).
  So the result no longer depends on a 7.4·10¹³ computation that nobody
  can inspect, or on Theorem 22's unpublished numbers: the remaining range
  is checked in seconds. **Status of (b): not found in prior work as of
  2026-10-31 (`literature/colton-novelty.md`); Lauer 2014, SeqFan and CNKI
  not reached.** It is not claimed as new.

**Evidence status:**

- **[T] refereed** for every n ≥ 10⁷: the threshold. Proved in full in
  `colton-threshold.md`; ref-colton returned ACCEPT WITH CORRECTIONS on
  2026-10-30, and the corrections were applied.
- **[C] 2026-10-31** for every 1 ≤ n ≤ 10⁹: the finite range (§2).
  - **Team side:** `rangesieve.c` and `blocks.c` (factorisation) against
    `verify/range2/r2.c` (an additive divisor-pair sieve, no factorisation).
    These are different methods, by blind authors.
  - **Outside the team:** `referee/colton-range/dpair.c` (divisor-pair
    counting) and `adv-colton`'s `dsieve.c`.
  - All give the same checkpoint file, byte for byte or line for line.
- **Finite range refereed.** `ref-colton` returned ACCEPT WITH CORRECTIONS
  on 2026-10-31 (`referee/colton-range.md`). Its one GAP, R1, was the
  shared method; it is closed by `dpair.c` and recorded in §2.
- **Adversary: NO COUNTEREXAMPLE** (`adv-colton`, 2026-10-31,
  `adversary/colton.md`).
  - It recomputed the range by a further method, which agrees at all 1000
    checkpoints.
  - It tested the threshold's bound (3.3) against the exact count at every
    integer in [10⁷, 10⁹].
  - It found nothing wrong.

### What would have to be true for this to be wrong

1. **Dusart's bound (6.5) is false somewhere.** This is the threshold's one
   external input:
   - π(x) ≥ (x/ln x)(1 + 1/ln x) for x ≥ 599;
   - π(x) ≤ (x/ln x)(1 + 1.2762/ln x) for x > 1.

   It is cited as arXiv:1002.0442v1, Theorem 6.9, eq. (6.5), READ. The
   same pair is also attributed to Ramanujan J. 45 (2018) 227–251, which
   was NOT READ (`colton-threshold.md` §7.3; `lit-colton-dusart`,
   `literature/colton.md`).
2. **An error in the threshold proof** that its referee missed, or in its
   computed inputs. The inputs are [C], and the referee recomputed them
   again, without the shared component, in PARI.
3. **A common error in every finite-range computation.** Six have
   finished (§2). Between them they use:
   - two ways of computing τ: factorisation, and divisor-pair counting;
   - two ways of finding primes: τ = 2, and a separate Eratosthenes.

   To be wrong, they would have to err identically at all 1000 checkpoints
   and in every block minimum.
4. **A mismatch between what was computed and the formal statement.** I
   checked this in §3: the computations count 1 ≤ k ≤ n with τ(k) | k,
   which is `countRefactorableNat n`, and π(n) counts primes ≤ n, which is
   `Nat.primeCounting n`.

## 1. The threshold: every n ≥ 10⁷ — [T], refereed

See `findings/colton-threshold.md`, which is not repeated here.

- **Its statement:** for every integer n ≥ 10⁷, T(n) − π(n)/2 ≥ 3616.
  Equivalently, 2T(n) − π(n) ≥ 7232.
- **Refereed** by `ref-colton`, 2026-10-30: ACCEPT WITH CORRECTIONS, no
  FATAL and no GAP (`referee/colton-threshold.md`, PR #24 into `dev`).
  Corrections M1–M5 were applied (PR #23); the literature verdict on Dusart
  was recorded (PR #26).
- **What it rests on:**
  - Zelinsky's p-generator construction, proved there;
  - Dusart (6.5) [L, READ in the arXiv preprint];
  - three [C] generator sets.

**A second, Dusart-free proof from 10⁹** (added 2026-10-31,
`rs62-threshold`): `findings/colton-threshold-rs62.md` proves
T(n) − π(n)/2 ≥ 917,294 for every n ≥ 10⁹. Its only cited input is
Rosser–Schoenfeld 1962 Theorem 1 [L, READ], and only for (3.1) at
x > 10⁹ and (3.2) at x ≥ 10⁹. Below 10⁹, (3.1) is the project's own [C]
(`rs62-lower.txt`). Its inputs are [C] (`results/rs62/`, `verify/rs62/`),
and two checkers each exit 0. Together with the [C] range of §2 it gives
π(n) ≤ 2T(n) for all n with no Dusart. Status: [T] on [C]; refereed, ref-colton-rs62 ACCEPT (round 3, 2026-10-31; round 2 REVISE R1 fixed at 96b2919), report `referee/colton-threshold-rs62.md`. It is not a novelty claim.

## 2. The finite range: every 1 ≤ n ≤ 10⁹ — [C], 2026-10-31

### The reduction lemma [T, proved here]

**Lemma.** Suppose 2T(1) ≥ π(1) and 2T(p) ≥ π(p) for every prime p ≤ N.
Then 2T(n) ≥ π(n) for every 1 ≤ n ≤ N. More precisely, for every
2 ≤ n ≤ N,

  2T(n) − π(n) ≥ 2T(p) − π(p),  where p = the largest prime ≤ n.

*Proof.*

- **n = 1.** π(1) = 0 ≤ 2 = 2T(1), since τ(1) = 1 divides 1.
- **2 ≤ n ≤ N.** Let p be the largest prime ≤ n. It exists, since 2 ≤ n,
  and p ≤ N.
  - No prime lies in (p, n], so π(n) = π(p). That is, π is constant on
    [p, p_next − 1].
  - T is nondecreasing, because it counts a set that only grows with n.
    So T(n) ≥ T(p).
  - Hence 2T(n) − π(n) ≥ 2T(p) − π(p). ∎

**What the lemma gives.**

- Over any interval [a, b], the minimum of 2T − π is attained at a or at a
  prime in (a, b].
- That is why a certificate of block minima over primes covers every
  integer.
- `comp-range` uses the lemma. The other computations evaluate every n
  directly and do not need it.
- **Equality.** On [1, 10⁹], equality π(n) = 2T(n) holds only at 7. At a
  non-prime n the margin is at least the margin at the largest prime ≤ n,
  and that is 0 only for p = 7. The next integer, 8, is refactorable, so
  its margin is 2. This is the referee's step, `referee/colton-range.md`.

### The computations

| | Who | τ(n) by | primes by | π cross-check | n evaluated |
|---|---|---|---|---|---|
| 1 | `comp-range`: `search/range/rangesieve.c`, `results/range/` @ `2856e54`/`8fe609f` | segmented factorisation: strip each prime ≤ 31,700 from a remainder array, multiply (e+1); a leftover > 1 is one prime | τ = 2; small primes by Eratosthenes | none beyond the cross-checks below | primes, then the lemma |
| 2 | `check-range`: `verify/range/blocks.c` + `merge.py` @ `c30dfee`. Written from the statement only, without reading 1 | the same factorisation idea, in independent code | τ = 2; small primes by trial division | **PARI `primepi(k·10⁶)` at all 1000 checkpoints: all agree** | every n |
| 3 | `ref-colton`: `referee/colton-range/dpair.c` + `combine_ref.py` (2026-10-31). Written outside the team. **The different-method implementation of the [C]** | **divisor-pair counting**: each d ≤ √hi adds +2 to every multiple m ≥ d², or +1 if m = d². No factorisation, no prime list, no remainder | τ = 2 | PARI `primepi` at 123, 457, 500, 777 and 999 × 10⁶ | every n |
| 4 | `adv-colton`: `adversary/colton/dsieve.c` (2026-10-31). It did not read `search/range/` or `verify/range/` | divisor-pair counting | **a separate segmented Eratosthenes bitmap**, asserting τ = 2 ⇔ prime at every n ≤ 10⁹ (never fired) | PARI at 10⁹ | every n |
| 5 | `thm22`, this file (code below), 2026-10-31. Not blind: written after reading 1 and 2 | divisor enumeration, the same method as 3 | τ = 2 | — | every n |
| 6 | `check-range2`: `verify/range2/r2.c` @ `cf911da` (2026-10-31). Blind: it did not read `search/`, `results/range/`, `verify/range/` or the findings | **additive divisor sieve**: τ(m) = 2·#{d ≤ √m : d \| m} − [m is a square]. No factorisation | **segmented Eratosthenes**; τ is never consulted for π | **PARI `primepi` at all 1000 checkpoints: 0 mismatches** | every n |

**Results.**

- **Identical checkpoint files.** Computations 1, 2, 3, 5 and 6 produce
  exactly the same 1000-line checkpoint file. Each line is "n T(n) π(n) m_k", for
  n = k·10⁶ with k = 1…1000, where m_k is the minimum of 2T(p) − π(p) over
  primes p in ((k−1)·10⁶, k·10⁶]. The sha256 is
  **`985f8d879d07621722caa482a10599d8fce1f1c05ce894cd3da39b310ef9f1c9`**:
  - `results/range/checkpoints.txt` and `verify/range/checkpoint.txt` are
    byte-identical; I checked with `cmp`;
  - `referee/colton-range/checkpoints-dpair.txt` has the same sha256; I
    re-hashed it on 2026-10-31;
  - the output of computation 5 is byte-identical to all of them;
  - `verify/range2/checkpoints.txt` (computation 6) is `cmp`-identical to
    `results/range/checkpoints.txt`; I checked on 2026-10-31.
- **Computation 4 agrees on all 1000 lines** (n, T(n), π(n), m_k).
  - Its first comparison differed on 84 lines in m_k, because it had taken
    the minimum over all n instead of over primes. With the same quantity
    there are 0 differences (`adversary/colton.md` §2).
  - Its block file is `adversary/colton/blocks.txt`, sha256 `0b5b29c7…be838f7`.
  - It also evaluated the threshold's right-hand side (3.3) at **every
    integer n ∈ [10⁷, 10⁹]**, in double precision, against the exact
    2T(n) − π(n). The bound is below the truth everywhere, with minimum
    slack +93,911 at n = 10,000,007.
- **Every m_k ≥ 0.** m₁ = 0, attained at p = 7. Every other m_k ≥ 10,910.
  By the lemma, 2T(n) − π(n) ≥ 0 for every 1 ≤ n ≤ 10⁹.
- **Equality only at n = 7.** Computations 2–6 evaluate every n and
  report no n in [1, 10⁹] with 2T(n) − π(n) ≤ 0 other than n = 7.
- **Margin at n = 10⁹:** 2·32,608,999 − 50,847,534 = **14,370,464**. The
  14,355,343 in the last checkpoint line is m₁₀₀₀, the minimum over primes
  in the last block; it is not the margin at 10⁹.
- **Smallest margin beyond 10⁶.** The minimum of 2T(n) − π(n) over
  10⁶ < n ≤ 10⁹ is **10,910**, first at **n = 1,000,697**, a prime. It is
  It is reported by 1, 2, 4, 5 and 6. The referee (3) confirmed the value
  10,910 but did not locate its argmin.
- **Small n.** Every n ≤ 1000 with 2T − π ≤ 2: (n : margin) 1:2, 3:2, 4:2,
  5:1, 6:1, 7:0, 8:2, 53:2, 54:2, 55:2, 71:2, 79:2. This comes from 1 and
  from `verify/range/brute.py`, which counts divisors by trial division.

**The label, and the gap that was caught.**

- **[C] 2026-10-31.** This now meets the project rule in full on the team
  side.
  - **Team side:** `rangesieve.c` and `blocks.c` (factorisation, two codes
    blind to each other) against `verify/range2/r2.c` (an additive divisor
    sieve plus Eratosthenes, blind). No code and no method is shared.
  - **Outside the team:** `dpair.c` (the referee) and `dsieve.c`
    (`adv-colton`).
- **The gap.** As first delivered, the [C] rested on 1 and 2 alone, and
  **they share their method.** Both compute τ by remainder-stripping
  factorisation: strip every prime ≤ √hi from a remainder array, multiply
  by (e + 1), and treat a leftover > 1 as one prime. They also share every
  structural assumption that goes with it:
  - the small-prime bound;
  - p² > hi;
  - "the leftover is one prime";
  - uint16 τ.

  The project rule (no shared code *and no shared method*) is not met by
  that pair.
- **It was caught twice, independently:**
  - by `thm22` in the first version of this file, which added computation
    5, a non-blind check;
  - by the referee as **R1 (GAP)**. The referee closed it with `dpair.c`.
- **A dispatch error came first.** The finite-range dispatch had described
  1 as "a divisor-count sieve plus Eratosthenes". It is not one.
  `results/range/README.md` now records the shared method.
- **One caveat, the referee's own, now discharged.** `dpair.c` was written
  by the referee, who had read 1 and 2 in order to referee them. Two checks
  answer that caveat:
  - computation 4 (`adv-colton`) uses a different method, by a chat that
    did not read the team's range code;
  - computation 6 (`check-range2`) is a blind team-side divisor-sieve
    check. It landed on 2026-10-31 with an identical checkpoint file.

**Cross-checks against outside values.**

- **π(10^k), k = 1…9:** 4, 25, 168, 1229, 9592, 78498, 664579, 5761455,
  50847534.
  - Computation 2 checks all 1000 checkpoints against PARI `primepi`.
  - The k = 6…9 values are rows of the checkpoint file.
  - These are the standard values.
- **T(10^k), k = 0…9:** 1, 4, 16, 92, 665, 5257, 44705, 394240, 3558181,
  32608999.
  - These agree with OEIS A111291's data a(0..9). The OEIS entry was READ
    by `lit-colton` (`literature/colton.md` §1, 2026-10-30), not re-read
    by me.
  - The k = 6…9 values are rows of the checkpoint file. The k ≤ 5 values
    come from the brute force in `verify/range/brute.py` and
    `search/range/crosscheck.py`.
- **Consistency with the threshold on the overlap.**
  - At n = 10⁷ the checkpoint gives 2T − π = 2·394,240 − 664,579 =
    123,901. That is ≥ 7232, as the threshold requires.
  - The referee's own scan, a linear sieve with one program
    (`referee/colton-threshold.md`), gives min (T − π/2) = 61,950.5 on
    [10⁷, 10⁸], at n = 10⁷. That is the same 123,901.

### Rechecking a segment

- **One block.**
  `~/dev/projects/open-problems/.venv/bin/python search/range/verify_segment.py results/range/checkpoints.txt K`
  recomputes block ((K−1)·10⁶, K·10⁶] from scratch with numpy, starting
  from line K−1's T and π. It compares the result with line K.
  - It exits 1 on a mismatch.
  - `comp-range` spot-checked K = 1, 2, 500, 1000, and showed that a
    corrupted line is caught.
  - It uses the factorisation method. The method-disjoint rechecks are
    `referee/colton-range/dpair.c` (under a minute on 2 cores) and
    computation 5 below (16 s).
- **Whole range, by the method-disjoint route.** Compile the program
  below, then compare:
  ```
  gcc -O2 -o divenum divenum.c
  ./divenum 1000 > cp.txt
  sha256sum cp.txt   # expect 985f8d87...9f1c9
  ```

Computation 5 was run on 2026-10-31 on PC2 (WSL2) at nice 19: 16.2 s wall,
one core. The output's sha256 is 985f8d87…9f1c9. stderr reported exactly one
n with 2T − π ≤ 0, namely n = 7, and the minimum over n > 10⁶ as 10,910 at
n = 1,000,697.

```c
/* divenum.c: tau(n) by divisor enumeration only: for d <= sqrt(n), d | n adds 2 (1 if d*d = n).
   No factorisation, no prime list; n is prime iff tau(n) = 2.
   Prints "n T(n) pi(n) m_k" for n = k*10^6, k = 1..K, with
   m_k = min over primes p in ((k-1)10^6, k 10^6] of 2T(p) - pi(p).
   Also prints to stderr every n with 2T(n) - pi(n) <= 0, and the global min over n > 10^6. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define B 1000000ULL
int main(int argc, char **argv) {
  int K = atoi(argv[1]);
  uint16_t *tau = malloc(2 * B);
  long long T = 0, P = 0, gmin = 1LL << 60; uint64_t gargmin = 0;
  for (int k = 1; k <= K; k++) {
    uint64_t lo = (uint64_t)(k - 1) * B + 1, hi = (uint64_t)k * B;
    for (uint64_t i = 0; i < B; i++) tau[i] = 0;
    for (uint64_t d = 1; d * d <= hi; d++) {
      uint64_t m = ((lo + d - 1) / d) * d;
      if (m < d * d) m = d * d;
      if (m == d * d) { tau[m - lo] += 1; m += d; }
      for (; m <= hi; m += d) tau[m - lo] += 2;
    }
    long long mk = 1LL << 60;
    for (uint64_t i = 0; i < B; i++) {
      uint64_t n = lo + i;
      if (n % tau[i] == 0) T++;
      if (tau[i] == 2) { P++; long long v = 2 * T - P; if (v < mk) mk = v; }
      long long v = 2 * T - P;
      if (v <= 0) fprintf(stderr, "EQ_OR_FAIL n=%llu T=%lld pi=%lld margin=%lld\n", (unsigned long long)n, T, P, v);
      if (n > B && v < gmin) { gmin = v; gargmin = n; }
    }
    printf("%llu %lld %lld %lld\n", (unsigned long long)hi, T, P, mk);
  }
  fprintf(stderr, "min over 10^6 < n <= %d*10^6 of 2T-pi = %lld at n=%llu\n", K, gmin, (unsigned long long)gargmin);
  return 0;
}
```

The inner loop counts each divisor pair (d, m/d) with d < m/d twice, and
d = m/d once. It visits only m ≥ d², so each d ≤ √m that divides m is
counted exactly once. The counter cannot overflow `uint16_t`: divisors come
in pairs (d, n/d) with d ≤ √n, so τ(n) ≤ 2√n ≤ 63,246 < 65,536 for
n ≤ 10⁹.

## 3. The seam, against the exact statements

**Coverage.**

- The threshold covers **every integer n ≥ 10⁷, inclusive**, with ≤, and
  in fact with 2T − π ≥ 7232.
- The finite range covers **every integer 1 ≤ n ≤ 10⁹**, with ≤.
- Their union is every n ≥ 1, and they **overlap on [10⁷, 10⁹]**.
- Neither half needs the other's endpoint conventions, because the overlap
  is two orders of magnitude wide. On the overlap the two agree: §2,
  consistency with the threshold.

**n = 0.** The formal statement quantifies over n : ℕ, so it includes
n = 0. formal-conjectures `FormalConjectures/OEIS/111291.lean`, clone at
`b6939a3`, READ 2026-10-31:

- `countRefactorableNat m := ((Icc 1 m).filter (fun k => k.divisors.card ∣ k)).card`.
  For m = 0 the interval Icc 1 0 is empty, so T(0) = 0.
- `Nat.primeCounting 0` = #{primes < 1} = 0.
- So the statement at 0 reads 0 ≤ 2·0. It is true, **with equality**.
  Neither computation needs to cover it, but "equality only at n = 7" is
  false over ℕ: **over ℕ the equality set is {0, 7}**, and for n ≥ 1 it is
  {7}. This is R2 in `referee/colton-range.md`.
- The same definitions show that the computed T(n) equals
  `countRefactorableNat n` for n ≥ 1. Both count k ∈ [1, n] with
  τ(k) | k, where τ(k) = `k.divisors.card`. The computed π(n) counts
  primes ≤ n, which is `Nat.primeCounting n`.

**≤ versus <.**

- **The strict form fails at n = 7**: 2T(7) = 4 = π(7). T(7) counts 1 and
  2; π(7) counts 2, 3, 5 and 7. This is checkable by hand.
- n = 7 is the only equality case for 1 ≤ n ≤ 10⁹ (§2).
- For n ≥ 10⁷ the threshold's surplus is ≥ 7232, so there is no equality
  case beyond 10⁹ either.
- So the equality set is {0, 7} over ℕ, and {7} for n ≥ 1. The strict
  inequality holds for every n ∈ ℕ outside {0, 7}. That is a corollary,
  not a separate claim.

**Which statement is claimed.**

- **Only the π form**, π(n) ≤ 2T(n) for all n ∈ ℕ: Zelinsky's form and
  `colton_conjecture` (`literature/colton.md` §1).
- **Colton's second sentence is not claimed in any form** (R5). It says the
  number of refactorables less than x is at least x/(2 log x).
  - In its ∀-real-x form it is false on (1, 2).
  - An integer version for n ≥ 17 would follow from the π form via
    π(n) > n/ln n. That needs Rosser–Schoenfeld [L, CITED, not read here],
    so it is not claimed either.

## 4. Zelinsky 2002: findings

All are from `colton-threshold.md` §§1–2 and were refereed there. They are
listed because they are findings in their own right. **None says his
Theorem 22 is wrong: it reproduces.** With his own inputs, the crossing is at
7.30936·10¹³ < 7.42·10¹³.

- **Lemma 19 is false as printed.** It says π(n/k) − ω(n). The
  counterexample is k = 180, n = 1024: the true count is 1 and the printed
  bound is 2.
  - ω(n) is presumably a misprint for ω(k). With ω(k) the lemma is true
    and proved.
  - It is unused by Theorem 22.
- **The B formula is garbled.**
  - As printed it evaluates to 1,785,485, which is below the true B. So
    the printed inequality is false.
  - The best reading (M_Z for 413980 in the π arguments, × for the last −)
    gives 8,685,500,885.
  - His stated 8,694,520,815 was not reproduced exactly.
- **His B is loose.** The true B = Σ(π(g(a)) + 1) = 3,348,920,075 is 2.6×
  below his bound, which is still valid. With the true B, his own chain
  crosses at 2.83·10¹³.
- **Minor points:**
  - "n > 598·M" should be n ≥ 599·M, since Dusart's lower bound is for
    x ≥ 599;
  - Lemma 21 (Aπ(n) − B) is unproved and unused;
  - A = 0.508000047 is over .508 by only 4.7·10⁻⁸.

## 5. What was not established

1. **The finite range: refereed, and no item is open.** `ref-colton`
   returned ACCEPT WITH CORRECTIONS on 2026-10-31, and `adv-colton` found
   NO COUNTEREXAMPLE.
   - The referee's caveat about its own `dpair.c` is discharged by the
     blind `check-range2` (§2).
   - `check-range2` was not refereed separately. Its agreement is a
     byte-identical checkpoint file.
   - Computation 5 here is one program, written by a chat that had read 1
     and 2.
2. **Dusart's published statement is unread** (R6).
   - The citation is arXiv:1002.0442v1, Theorem 6.9, eq. (6.5), READ.
   - The same pair is also attributed to Ramanujan J. 45 (2018) 227–251:
     NOT READ, and no published theorem number is cited. That version is
     paywalled.
   - `lit-colton-dusart` found that no erratum touches π(x), and that a
     READ secondary source (arXiv:2404.17165, p. 8) attributes the
     identical pair to the published paper. Buying it is Aaron's call.
   - The [T] for n ≥ 10⁷ stands on the preprint statement.
   - **A possible follow-up, not done here.** `adversary/colton.md` §5
     suggests closing from 10⁹ with Rosser–Schoenfeld 1962, Theorem 1,
     instead of Dusart.
     - **RS62 Theorem 1 is now READ** (`lit-colton-rs62`, 2026-10-31,
       `literature/colton.md`, PR #30), p. 69:
       - (3.1) (x/log x)(1 + 1/(2 log x)) < π(x) for x ≥ 59;
       - (3.2) π(x) < (x/log x)(1 + 3/(2 log x)) for x > 1.

       No correction to it was found.
     - The adversary's chain on these constants is a float exploration. A
       rigorous version would need the moments of its stage set as [C],
       plus one rational check. It would remove the Dusart dependency. It
       is deferred, and out of scope for this file.
3. **No Lean.** Nothing here is [F]. `colton_conjecture` remains `sorry`
   in formal-conjectures. Formalising it would need both of these:
   - the threshold argument, including Dusart (6.5) as an axiom or a
     proof;
   - a kernel-checkable certificate for n < 10⁷.
4. **No novelty is claimed for the statement or the finite range.** Both
   were claimed settled in OEIS A323326 (McCranie 2019; see "Prior work"
   above). The superseded basis was `lit-colton`'s "n ≤ 500" search
   (`literature/colton.md` §§3, 6).
   - The lowered threshold (10⁷ against 7.42·10¹³) is "not found in prior
     work as of 2026-10-31 (`literature/colton-novelty.md`); Lauer 2014,
     SeqFan and CNKI not reached". It is not claimed as new.
   - The threshold improvement uses Zelinsky's method, and no claim is
     made that his threshold is wrong.
   - McCranie's computation to 7.44·10¹³ was not reproduced or inspected
     here. It is not needed: our own range plus the 10⁷ threshold covers
     every n.
   - Nothing may leave the repo without Aaron.
5. **T(10^k) against OEIS.** The comparison uses the OEIS data as READ by
   `lit-colton`. OEIS was not re-read for this file.
6. **The x/(2 log x) form** is not claimed (§3).
