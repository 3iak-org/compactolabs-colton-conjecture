# Adversary: the RS62 threshold, T(n) − π(n)/2 ≥ 917,294 for every n ≥ 10⁹

*`adv-colton-rs62`, opened by `dev`, 2026-10-31. Branch
`agent/adv-colton-rs62`. Target: `findings/colton-threshold-rs62.md` on
`lead-colton-rs62` @ `81ad7d7`. Scripts and outputs are in
`adversary/colton-rs62/`. I did no part of the mathematics. I did not read
`search/rs62/`, `verify/rs62/` or the two checkers before writing my own code,
and my code shares none of theirs. I did compare my outputs against their
committed data files afterwards.*

## Verdict

**Not broken.** I found no counterexample, and no step that fails or is
applied outside its hypotheses. I also found no defect in the file that needs
a correction.

| Attack | Result | Label |
|---|---|---|
| The claim itself, at **every integer n ∈ [10⁹, 10¹⁰]** (piece 1, which sets the 917,294) | min T(n) − π(n)/2 = **7,185,230.5**, at n = 1,000,000,021. That is 7.8 times the claimed constant. | **[C]** 2026-10-31: two implementations of mine, sharing no code and no method (§3) |
| The claim at every integer n ∈ (10¹⁰, 10¹¹] (piece 2) | min = **74,646,250.5**, at n = 10,000,000,069 | one exact implementation; endpoints match A111291 [L] and PARI. **Not [C]** (§3) |
| The proof's pointwise bound R(n) = (n/u)·g_S(u) − β against the truth, at every integer n ∈ [10⁹, 10¹¹] | The truth is always above it. min (T − π/2) − R = 5,306,751.8 on piece 1 and 59,159,011.0 on piece 2. | one implementation, long double (§3) |
| Stage inputs N, max S, β, L₀…L₆ for G(110,000), G(160,000), G(210,000) and G(28,653,696) | **All agree.** The integers match exactly, and every L_k matches to all 30 printed digits. | third implementation (§2) |
| The three Lemma P pieces and the Lemma Q tail, evaluated from my own coefficients | Surpluses 917,294.525, 8,704,925.507, 68,866,565.870 and 3,287,868,063.035. **These are the file's numbers.** | mpmath at 60 digits; not a certificate (§2) |
| RS62 (3.1) at every prime 59 < q ≤ 10¹¹, as a left limit | Holds. The per-decade minima below 10⁹ equal `rs62-lower.txt`'s to the 3 decimals I print. Above 10⁹ the minimum slack is 1.43·10⁶. | one implementation, long double (§4) |
| RS62 (3.2) at every prime q ∈ (10⁹, 10¹¹] | Holds. Minimum slack is 9.0·10⁵. | one implementation, long double (§4) |
| The written reductions: Lemmas 1, 2, A, B, P, Q, M | Re-derived line by line. **No error found.** | not a referee's report (§1) |

### What "not broken" rules out, and what it does not

- **Ruled out [C]: a counterexample in [10⁹, 10¹⁰].** That is where the
  theorem's constant is set. On this range the theorem's *conclusion* is now
  checked directly, with no RS62, no moments and no chain. The truth exceeds
  the claim by a factor of 7.8 at its weakest point.
- **Ruled out, one implementation: a counterexample in (10¹⁰, 10¹¹].** The
  same is true of an n in [10⁹, 10¹¹] where the chain's pointwise bound
  exceeds the truth, which would have exposed an error in (1.1),
  Proposition A or B, or RS62 at the points used.
- **Not ruled out by computation: n > 10¹¹.** There the claim stands on the
  chain and on RS62 alone. My evidence for that range is that the inputs and
  the four inequalities reproduce, and that the reductions read correctly.
  None of that is exhaustive.

**What would have to be true for "not broken" to be wrong:**

1. **RS62 Theorem 1 is false at some x > 10¹¹ where it is used.** That means
   (3.1) at a real x = n/a > 10¹¹, or (3.2) at an integer n > 10¹¹. I tested
   both only up to 10¹¹.
2. **An error in the reductions that I missed while reading.** The pointwise
   comparison in §3 would catch any such error that shows up below 10¹¹, but
   not one that only bites in the tail. For example, a wrong sign hypothesis
   on c₀, which matters only in Lemma Q.
3. **A shared misreading of G or β by me and both team implementations.** §2
   computes G from the definition by a third route. The definition of T is
   the one checked against `formal-conjectures` in `adversary/colton.md` §1.

## 1. The reductions, re-derived [2026-10-31]

I attacked the places where the case split lumps things together, and the
places where a hypothesis could be applied out of range. Nothing failed.

- **Lemma 1 / Lemma 2 (disjointness).** If m = ap = bq with p > g(a) and
  q > g(b), then p is the largest prime factor of m, and so is q. So p = q
  and a = b.
  - The count |E_a ∩ [1, n]| = π(n/a) − π(g(a)) is correct when
    n/a ≥ g(a), and the inequality is correct when n/a < g(a).
  - (H↓) is applied at real x = n/a. RS62 states (3.1) for real x ≥ 59.
- **Proposition A.** It needs 0 < ℓ < u and α ≥ 0. ℓ > 0 because min G = 8,
  which I confirmed by computation. ℓ < u because n/a ≥ n/max S ≥ 59.
  Truncating the two positive series is a lower bound, and the
  re-indexing m = k + 1 is right.
- **Proposition B.** (H↑) is used only at x = n ≥ 10⁹. The bookkeeping
  c₁ = L₁ + αL₀ − γ/2 is right.
- **Lemma P.** Each piece needs four things, and I checked all four for
  every piece:
  - p ≥ 59·max S;
  - c_m ≥ 0 for every m ≥ 1, so that g_S is nonincreasing;
  - g_S(ln q) ≥ 0;
  - x/ln x nondecreasing for x ≥ e.

  The bound (p/ln p)·g_S(ln q) − β is the worst corner. My pointwise R(n)
  is at least it, and so is the truth (§3).
- **Lemma Q.** It needs ln n_f ≥ 7 for e^u·u^{−m−1} to increase, which
  10¹² gives (ln 10¹² = 27.6). It also needs **every** c_m ≥ 0, including
  c₀ = L₀ − ½ = 0.0080000472. My own L₀ is 0.508000047238841733452…, as in
  the file.
- **Lemma M.** The direction of every substitution is right. The m = 0 term
  carries no logarithm, and every m ≥ 1 term has c_m^lo ≥ 0.
- **Coverage and seam.** The pieces are closed decades that share endpoints,
  and the tail is [10¹², ∞). The exact range is 1 ≤ n ≤ 10⁹ inclusive, so no
  integer is missed.
- **Where (3.1) is used.** I recomputed p/max S: 9,090.909…, 62,525.010…,
  476,190.476… and 34,899.512…, which are the file's §5 values. So (3.1) is
  used from x ≈ 9,091, as the file says. That makes `literature/colton.md`'s
  "the table-dependent range below 10⁸ is not used" false for (3.1); the
  file already flags this.
- **Text claims spot-checked.** All are correct:
  - R(10⁹) = 1,878,478.68, against the file's "about 1.88·10⁶";
  - L₀(G(a)) first exceeds ½ at a = 16,197,216, so the first *grid* M with
    L₀ > ½ is 1.7·10⁷, as the file says;
  - the L_k failure scale is 3.424%, 3.642% and 3.202% on the three pieces,
    and 0.008/0.508 = 1.575% on the tail, against the file's 3.42, 3.64,
    3.20 and 1.57%;
  - the β ratios are 6.387, 27.99, 134.7 and 1.982.

## 2. The stage inputs, recomputed [2026-10-31]

`inputs.py`, output `inputs.out`, coefficients `coefs-rs62.txt`.

- **τ** by numpy divisor-pair slicing, with no factorisation.
- **g(a)** by `sympy.factorint`.
- **π(g)** from a numpy Eratosthenes cumulative sum.
- **L_k** summed in mpmath at 60 digits. That is a third arithmetic, after
  the team's Arb and MPFR.

Results:

| M | N | max S | β | L₀ |
|---|---|---|---|---|
| 110,000 | 2,063 | 110,000 | 170,282 | 0.42124672929545522048359156211906 |
| 160,000 | 2,938 | 159,936 | 322,537 | 0.42779776919750746358661886726646 |
| 210,000 | 3,795 | 210,000 | 514,970 | 0.43245409275332678854985420424042 |
| 28,653,696 | 413,980 | 28,653,696 | 3,348,506,095 | 0.50800004723884173345207326298772 |

- Every L₀…L₆ lies inside the team's [L_lo, L_hi] to all 30 digits printed
  in the file's table. Mine are printed to 32 digits in `inputs.out`.
- c₀…c₆ agree with the file's coefficient table to its 10 digits.
- The four inequalities give the surpluses in the Verdict table. The
  gS(ln q) values 0.0225381374519, 0.0207865005965 and 0.0175732579246 match
  the file. The tail terms match it too.
- This is a non-rigorous 60-digit evaluation, a check on the team's
  certificates rather than a certificate. Rounding error is about
  N·10⁻⁶⁰, against margins of at least 1.5%.

## 3. The truth on [10⁹, 10¹¹], exactly [2026-10-31]

**Implementation 1: `xsieve.c`.**

- τ(n) by divisor-pair counting.
- Primes from a separate segmented Eratosthenes bitmap. It asserts
  τ(n) = 2 ⇔ n prime at every n ≤ 10¹¹, and the assertion never fired.
- Blocks of 10⁶ from n = 1, so the offsets are computed and not assumed.
- 3 processes at `nice -n 19`, 10:00–10:26.
- Output: `blocks-1e11.txt.gz`, uncompressed sha256 `a98ff7ff…944d5b94`.
- For every n ≥ 10⁹, the program also evaluates the proof's pointwise bound
  R(n) = (n/u)·g_S(u) − β, in long double, using the stage set the theorem
  assigns to n.

**Implementation 2: `fsieve.c`, on [1, 10¹⁰].**

- τ(n) multiplicatively, from a segmented factor sieve that divides each
  prime out completely.
- n is prime iff no sieving prime divides it, rather than τ = 2.
- Sieving primes by trial division.
- Unsigned 64-bit arithmetic throughout, and no code shared with
  implementation 1.

Its per-block (T_b, π_b, min local margin, argmin) agree with implementation 1
on every one of the 10,000 blocks: `diff` of columns 1–5 is empty, and it sums to T(10¹⁰) = 302,172,507 and π(10¹⁰) = 455,052,511 independently. Output: `fblocks-1e10.txt.gz`, uncompressed sha256 `5d178290…f3409ad1`. 3 processes, 10:27–10:32.

`combine.py` stitches the blocks. Its output is `combine.out`.

| n | T(n) | π(n) | T − π/2 | cross-check |
|---|---|---|---|---|
| 10⁹ | 32,608,999 | 50,847,534 | 7,185,232 | T = A111291 a(9) [L]; π = PARI `primepi` |
| 10¹⁰ | 302,172,507 | 455,052,511 | 74,646,251.5 | T = A111291 a(10) [L]; π = PARI |
| 10¹¹ | 2,823,898,245 | 4,118,054,813 | 764,870,838.5 | T = A111291 a(11) [L]; π = PARI |

The A111291 values are from `literature/colton.md`, which READ the OEIS
data.

| range | min_n T(n) − π(n)/2 | at n | min_n (T − π/2) − R(n) | at n |
|---|---|---|---|---|
| [10⁹, 10¹⁰] | **7,185,230.5** | 1,000,000,021 | 5,306,751.8 | 1,000,000,023 |
| (10¹⁰, 10¹¹] | **74,646,250.5** | 10,000,000,069 | 59,159,011.0 | 10,000,000,079 |

So:

- **The claim holds at every n ∈ [10⁹, 10¹¹].** This is [C] on [10⁹, 10¹⁰]
  and one implementation beyond. The weakest point is just above 10⁹, where
  the truth is 7.8 times the claimed constant.
- **The analytic bound is a lower bound everywhere it was compared.** The
  proof's own slack is large: its corner value 917,294 sits far below its
  pointwise value of about 1.88·10⁶, which sits below the truth of about
  7.19·10⁶.
- Being the adversary, I note that the *worst point for the truth* and the
  *worst point for the bound* coincide at the left end of piece 1. That is
  exactly where the file says its surplus is set. The seam at 10⁹ is the
  weakest place in the claim, and it holds there with the most room.

## 4. RS62 Theorem 1 where it is used [2026-10-31]

`xsieve.c` evaluates both bounds at every prime, in long double. Both bound
functions increase on the range used and π is a step function, so primes
are the worst points:

- for (3.1), the left limit at each prime q > 59, with slack
  π(q) − 1 − f(q);
- for (3.2), the value at each prime q, with slack F(q) − π(q).

| range of q | min (3.1) slack | min (3.2) slack |
|---|---|---|
| (59, 10⁶] | 0.171 (x → 67⁻) | not used below 10⁹ |
| (10⁶, 10⁷] | 3,493.862 | |
| (10⁷, 10⁸] | 24,903.718 | |
| (10⁸, 10⁹] | 185,418.873 | |
| (10⁹, 10¹⁰] | 1,428,314.340 | 900,212.166 |
| (10¹⁰, 10¹¹] | 11,327,416.468 | 7,533,714.557 |

- The minima up to 10⁹ equal `results/rs62/rs62-lower.txt`'s block minima to
  three decimals: 0.170566, 3493.861600, 24903.718139 and 185418.872767. That
  is agreement from a third program on the file's narrowing in §5.
- My figures are long double, and the minima were not re-evaluated in Arb.
  At slacks this size, that does not matter for an attack.
- Above 10¹¹, RS62 is the only support. Its proof was not checked here, as
  the file says.

## 5. What I did not establish

- **Nothing exhaustive above 10¹¹.** Running implementation 1 to 10¹² would
  cost about 5.5 h on 3 cores. I judged it not worth it: the claim's margin
  over the truth grows by roughly 10× per decade.
- **The exact count on (10¹⁰, 10¹¹] has one implementation.** Its endpoints
  agree with A111291 [L] and PARI.
- **I did not audit the team's checkers** (`-check-rational.py`,
  `-check-arb.py`). I evaluated the same four statements independently,
  without directed rounding.
- **I did not read RS62 itself.** The statement is as READ by
  `lit-colton-rs62`. It agrees with my memory of it, and with the numbers
  above.
- **This is not a referee's report.** The referee owns the proof.

## Reproduce

Python is `~/dev/projects/open-problems/.venv/bin/python`. Run
from `adversary/colton-rs62/`.

```
python inputs.py coefs-rs62.txt > inputs.out          # ~1 min
gcc -O2 -march=native -o $TMPDIR/xsieve xsieve.c -lm
gcc -O2 -march=native -o $TMPDIR/fsieve fsieve.c
# implementation 1, [1,1e11], 3 shards (~26 min wall at nice 19)
$TMPDIR/xsieve 100000000000 1000000 1 33334 coefs-rs62.txt > a.txt &
$TMPDIR/xsieve 100000000000 1000000 33335 66667 coefs-rs62.txt > b.txt &
$TMPDIR/xsieve 100000000000 1000000 66668 100000 coefs-rs62.txt > c.txt; wait
cat a.txt b.txt c.txt > blocks-1e11.txt; python combine.py blocks-1e11.txt   # committed as blocks-1e11.txt.gz
# implementation 2, [1,1e10]; compare columns 1-5
$TMPDIR/fsieve 10000000000 1000000 1 10000 > f.txt
diff <(head -10000 blocks-1e11.txt | cut -d' ' -f1-5) f.txt   # committed as fblocks-1e10.txt.gz
```
