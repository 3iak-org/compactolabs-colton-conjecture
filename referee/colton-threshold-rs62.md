# Referee report: Colton threshold from 10⁹, Rosser–Schoenfeld 1962 only

*`ref-colton-rs62`, opened by `dev` (PI), 2026-10-31. Refereed:
`findings/colton-threshold-rs62.md` and its companions on `lead-colton-rs62`
@ `81ad7d7869ba055863cbd116cec069b80ec2813a`, plus the inputs it rests on
(`results/rs62/`, `verify/rs62/`). I did no part of this mathematics. My own
code and outputs are in `referee/colton-threshold-rs62/`. Rounds 2 and 3 re-read later heads; the latest round is first.*

## Round 3 (2026-10-31): verdict **ACCEPT**

*Reviewed at `lead-colton-rs62` @ `0050dc3`. The changes since round 2
(`618cf34`):*

- *`search/rs62/rs62lower.c` (new) and `rs62_lower.py`, with
  `results/rs62/rs62-lower.txt`;*
- *`verify/rs62/rs62.c`, its README and `verify/rs62/rs62-lower.txt`;*
- *§0 item 1, §5 and §8 of `findings/colton-threshold-rs62.md`;*
- *the status paragraph in `findings/colton-conjecture.md`;*
- *the master plan, plus a merge of dev. In that merge, `referee/` and
  `literature/` are byte-identical to dev.*

*§§1–4 of the proof and the input JSONs are unchanged, so rounds 1 and 2
stand for them.*

**R1 is closed.** (3.1) on [59, 10⁹] is now the team's own [C], and every
interval is rigorous.

- **Implementation 1: `search/rs62/rs62lower.c`.** A segmented
  Eratosthenes sieve, then every prime-gap interval in FLINT Arb at 128
  bits.
  - An interval passes only if the lower endpoint of the ball
    π(q) − f(q′) is > 0.
  - The block minima are minima of those lower endpoints, printed by exact
    `fmpz` floor to 6 places.
  - There is no floating-point step, and the long-double prefilter is gone.
- **Implementation 2: `verify/rs62/rs62.c`.** A sieve of Atkin, then every
  interval in MPFR at 128 bits with directed rounding, and no prefilter.
  - The rounding chain is: ln q′ down; q′/L up; 2L·L down; q′/(2L²) up; the
    sum up; π(q) − f down. Every operand is positive, so each step is
    monotone, and the result is a lower bound on the true slack.
  - FAIL is reported if any computed slack is ≤ 0.
- **Independence.** The two share no code. Their prime generation
  (Eratosthenes against Atkin) and their arithmetic (Arb balls against
  MPFR directed rounding) are both different methods. The formula for f is
  necessarily the same.
  - Side remark: `rs62lower.c` is structurally close to my own
    `rs62every.c` (Eratosthenes + Arb at 128 bits). So my check is not
    independent of implementation 1 in method. It does not need to be:
    the team's [C] is the pair 1/2.
- **Re-run from the committed code** at `0050dc3`, by me, in scratch, with
  `nice -n 19`:
  - both programs print π(10⁹) = 50,847,534, last prime 999,999,937,
    `INTERVALS 50847518` and `PASS`;
  - their data lines are identical to the committed `rs62-lower.txt` files
    (`r3-comp-rerun.out`, `r3-check-rerun.out`);
  - the block minima and argmins equal my `rs62every.out` in every block.
- **Interval count.** 50,847,518 = π(10⁹) − π(58) = 50,847,534 − 16 ✓.
- **Fault injection,** my own test (`r3-fault-injection.out`). I lowered π
  by 1:
  - implementation 1 through its `bias` argument;
  - implementation 2 by editing a scratch copy, with nothing committed.

  Both report FAIL at q = 59. So both FAIL paths are live.
- **The §5 reduction** from finitely many checks to every real x [T]. I
  re-derived it.
  - f′ = (2L² − L − 2)/(2L³), which is > 0 exactly when
    L > (1 + √17)/4 = 1.2807…, and ln 59 = 4.077….
  - The sets I_q = [q, min(q′, 10⁹)) partition [59, 10⁹), with 10⁹ added
    to the last one. This works because 59 is prime.
  - π = π(q) on I_q, and f(x) < f(q′) (or ≤ f(10⁹) at the end). Hence
    π(x) > f(x).
  - This is correct and complete.
  - The comment in `rs62.c` says "f′ > 0 once L > 1.5". That is weaker than
    (1 + √17)/4 but also true, and the findings file carries the sharp
    threshold.
- **The rewritten text.** §0 item 1, §5 and §8 now say what is true:
  - (3.1) on [9,090.9, 10⁹] rests on [C], not on RS62;
  - RS62 below 10⁸ is qualified as an unread tabulation;
  - RS62 [L] is relied on only for (3.1) at real x > 10⁹ and (3.2) at
    integer x ≥ 10⁹, both in its analytic range.

  My referee checks are described as non-team, not as [C], which is right.

**Labels after round 3.**

- The Theorem, T(n) − π(n)/2 ≥ 917,294 for every n ≥ 10⁹: **[T] on [C],
  refereed (ACCEPT, round 3, 2026-10-31).**
- (3.1) on [59, 10⁹]: **[C]**.
- RS62 Theorem 1, for (3.1) at real x > 10⁹ and (3.2) at integer x ≥ 10⁹:
  **[L], READ as a statement, proof not checked.**
- The Corollary, π(n) ≤ 2T(n) for all n ≥ 1, needs the same [L] plus the
  refereed [C] range.

**Remaining, MINOR (N3).** The status lines read "awaiting round 3":

- `findings/colton-threshold-rs62.md` line 18, §6 and §8 item 1;
- `findings/colton-conjecture.md` §1.

They should now cite this round-3 ACCEPT. Nothing else is open.

**Still not checked by anyone here** (unchanged from round 1):

- RS62's proof of (3.1) above 10⁹ and of (3.2) from 10⁹;
- MathSciNet errata;
- a line-by-line audit of the rational checker's logarithm. Its numbers
  agree with two Arb computations.

## Round 2 (2026-10-31, dev ticket `tmvwgrbmer3ks`): verdict **REVISE** (superseded by round 3)

*Reviewed at `lead-colton-rs62` @ `618cf34`. Since `81ad7d7` that head
changes only `master-plan/colton-rs62.md`. It records reruns that are under
way and have not landed.*

**Why the verdict changed.** I accepted in round 1 because the Theorem cites
RS62 (3.1) on its whole stated range x ≥ 59. `literature/colton.md` now
carries a correction (PR #38, merged): below 10⁸, RS62's own proof of (3.1)
is the Appel–Rosser 1961 tabulation, with the Rosser–Walker tabulation below
16,000. That report is NOT READ and cannot be obtained, and the paper does
not say how finitely many points certify every real x.

The PI has ruled that the [L] citation alone is not enough on
[9,090.9, 10⁸), and I agree. On that range the citation is a pointer to a
computation nobody here can inspect. So the Theorem needs (3.1) on
[9,090.9, 10⁸) as this project's own [C].

**R1 — GAP (blocking). The team's `rs62-lower.txt` is not yet a [C]
certificate for (3.1) on [59, 10⁹].** I judged it directly, from
`search/rs62/lowcand.c`, `search/rs62/rs62_lower.py` and `verify/rs62/rs62.c`
at `618cf34`.

- **Directed rounding covers the block minima only.** Both programs evaluate
  the slack π(q) − f(q′) of all 50,847,518 intervals in `long double`, with
  glibc `logl`. Only the candidates within 0.01 (comp) or 10⁻⁶ (check) of
  each block's float minimum are re-evaluated rigorously, in Arb or in MPFR
  with directed rounding.
- **The rest rests on an accuracy estimate.** For every other interval,
  positivity follows from "long-double error ≈ 10⁻¹¹ ≪ 0.17". That needs
  `logl` to be accurate to roughly 10⁻⁸ relative. glibc documents this, but
  it is not proved, and neither program checks it. The margin is enormous, so
  this is a gap in rigour, not a suspected falsehood. It is still a gap.
- **This half shares code and method.** For those ~50.8 million intervals
  the two implementations call the same library function, glibc `logl`, on
  the same formula at the same precision. Only the prime generation differs:
  segmented Eratosthenes against Atkin. The project rule for [C] is "sharing
  no code and no method". On these intervals the rule is not met: a defect in
  `logl` would hit both programs identically.
- **What is sound in them.** I read both prime generators, including the
  Atkin 3x² − y² loop bounds, and both print π(10⁹) = 50,847,534. The
  interval semantics are right: π = π(q) on [q, q′), the first interval is
  [59, 61), and the last is [999,999,937, 10⁹] against f(10⁹). The
  running-minimum candidate filter cannot drop the true minimiser. The MPFR
  directed chain in `rs62.c` (L rounded down, quotients and sum rounded up,
  slack rounded down) is a correct upper bound on f.
- **Fix.** The lead has already opened it (`master-plan`, 618cf34): rerun
  both programs with every interval in rigorous arithmetic, Arb on one side
  and MPFR directed on the other. Then rewrite §5 so that [9,090.9, 10⁸)
  rests on that [C], with RS62 [L] below 10⁸ qualified as tabular.
- **Expected output, for the re-review.** My own every-interval Arb program
  (item 7 below) gives these values. Both reruns should reproduce them.

| block | intervals | min slack ≥ | at q |
|---|---|---|---|
| [59, 100) | 9 | 0.170566 | 61 |
| [10², 10³) | 143 | 1.076985 | 113 |
| [10³, 10⁴) | 1,061 | 12.051857 | 1009 |
| [10⁴, 10⁵) | 8,363 | 82.139136 | 10039 |
| [10⁵, 10⁶) | 68,906 | 524.880187 | 100237 |
| [10⁶, 10⁷) | 586,081 | 3493.861600 | 1000099 |
| [10⁷, 10⁸) | 5,096,876 | 24903.718139 | 10000609 |
| [10⁸, 10⁹] | 45,086,079 | 185418.872767 | 100000193 |
| total | **50,847,518** | | |

- **What the rewrite must also state.** It must say that f is increasing,
  since that reduces "every real x in a prime gap" to the gap's right end.
  - f′(x) = (1/L)(1 − 1/(2L) − 1/L²), with L = ln x.
  - f′ > 0 exactly when L² − L/2 − 1 > 0, that is L > (1 + √17)/4 ≈ 1.28.
  - At x = 59, L ≈ 4.08, so f′ > 0 on the whole range used.
  - The lead's planned wording in `master-plan` has the right threshold; I
    checked it.

**7. Referee recomputation of (3.1), every interval** (`rs62every.c`,
`rs62every.out`, new in round 2).

- *Method:* a byte-per-odd Eratosthenes sieve to 10⁹. Every prime-gap
  interval with q ≥ 59 is evaluated in FLINT Arb at 128 bits, with no
  floating-point step. Each one must satisfy `arb_is_positive`.
- *Result:* **PASS** in 39 s, over 50,847,518 intervals. The block minima
  and argmins equal both team files to all six printed digits.
- *Two checks of my own:* this and round 1's grid check (`rs62low.py`) are
  both rigorous. They decompose the range differently, but I wrote both and
  both use Arb. They settle the fact for me as referee. They are not the
  team's [C], and they are not two independent implementations.

**What I now believe, and why it is still REVISE.**

- RS62 (3.1) holds on [59, 10⁹]. My two directed checks and the team's two
  near-certificates leave no realistic doubt.
- The Theorem's evidentiary chain, however, must be the team's: two
  implementations, every interval rigorous, no shared code. That is not in
  the branch yet.
- When the reruns land with PASS, 50,847,518 intervals and the minima
  above, and §5 is rewritten accordingly, R1 closes. I expect to move to
  ACCEPT on that alone. Nothing else in round 1 changes.

**Round-1 items.**

- N1 is fixed by PR #38.
- N2 is superseded by R1.
- N3 stands.

## Round 1 verdict (superseded): **ACCEPT**

I checked every step and none fails. The claim is:

> T(n) − π(n)/2 ≥ 917,294 for every integer n ≥ 10⁹,

using only Rosser–Schoenfeld 1962 Theorem 1, (3.1) and (3.2). Together with
the refereed [C] range 1 ≤ n ≤ 10⁹ (`referee/colton-range.md`, with its R1
gap since closed), it gives π(n) ≤ 2T(n) for every n ≥ 1 without Dusart.

- I re-derived the reduction (§§1, 3) from the first line, and it holds as
  written.
- I recomputed every input from scratch with my own programs: the generator
  set, β and L₀…L₆ for all four stage sets. All of them agree, and my
  generator list hashes byte-for-byte to the refereed list.
- I recomputed all four final inequalities in Arb directly, without Lemma M's
  substitution. I got the same surpluses to every digit the file prints.
- I checked RS62 (3.1) on all of [59, 10⁹] with a fully directed-rounding
  program that is not one of the team's. It passes.

There are three items, all MINOR (N1–N3). None blocks acceptance, and none
needs a change to the proof. One of them (N1) is in a file the team does not
own.

The theorem's labels after this report:

- the theorem is **[T] on [C], refereed 2026-10-31**;
- RS62 Theorem 1 stays **[L, READ as a statement; proof not checked]**, and
  the theorem rests on it for (3.1) at real x > 10⁹ and (3.2) at integer
  x ≥ 10⁹.

## The hard step, and whether it is done

The file names the reduction (§6) as the hard step. Having re-derived it, I
think it is elementary, and it is correct: every truncation is a lower bound,
and every sign condition is checked. The steps that actually carry weight
are these three.

1. **The computed inputs, above all c₀ = L₀(G(28,653,696)) − ½ ≥ 0 in the
   tail.** The whole tail rests on L₀ exceeding ½. The margin is
   0.0080000472…, which is 1.57% of L₀. **Done.** I recomputed L₀ from my own
   generator enumeration as 0.50800004723884173345… (Arb, 300 bits). The
   generator set is identical to theirs, by sha256.
2. **RS62 (3.1) at every x = n/a it is applied to,** which is every real
   x ≥ 9,090.9 (stage 1: 10⁹/110,000). That is below 10⁸, so it is inside the
   part of RS62 that rests on tables. **Done, and better than RS62 needs:**
   - (3.1) on [59, 10⁹] is verified here in Arb (§"Recomputed", item 4);
   - above 10⁹ it rests on RS62 [L].
3. **RS62 itself for x ≥ 10⁹.** **Not done, by anyone here.** It is a cited
   [L], and its proof was not checked (§"Could not check").

## Issues

**N1 — MINOR, in `literature/colton.md` (owner: literature scout, not the
team).**

- *Where:* `literature/colton.md`, §"Rosser–Schoenfeld 1962, Theorem 1:
  READ", the paragraph "For the Colton chain, starting at 10⁹".
- *What it says:* "The table-dependent range below 10⁸ is not used".
- *Why it is wrong:* that is false for (3.1). Proposition A applies (3.1) at
  x = n/a, and with stage 1 (n ≥ 10⁹, a ≤ 110,000) x reaches down to
  9,090.9. The findings file already says so (§5, "`literature/colton.md` is
  wrong on this point"), and that is correct.
- *Effect on the proof:* none. The theorem cites (3.1) on its full stated
  range x ≥ 59. On [59, 10⁹] that range is also [C] (team) and verified here
  in Arb.
- *Fix:* the literature scout should correct the sentence. That needs a
  `lit-` chat, not the lead.

**N2 — MINOR, `findings/colton-threshold-rs62.md` §5 and §8 item 2: the
caveat on `rs62-lower.txt`.**

- *What it says:* both team programs clear non-minimal intervals with a
  long-double test, so for those intervals the evidence is "an error
  estimate, not a directed-rounding certificate".
- *Assessment:* that disclosure is accurate. I read
  `verify/rs62/README.md`: the prefilter is long double, and only the
  candidates near each block minimum go to MPFR. The two programs also share
  this filter-then-certify method, though not their prime generation.
- *What closes it:* my check (item 4 below) uses Arb for every evaluation,
  with no float step. It covers every real x ∈ [59, 10⁹] by a different
  decomposition (prime gaps below 10⁵, then a 1,000-step grid with π at the
  grid points). It PASSes, and below 10⁵ its block minima equal theirs to all
  six printed digits.
- *Fix (optional):* the file may cite `referee/colton-threshold-rs62/rs62low.py`
  as the directed-rounding certificate for [59, 10⁹]. Its label would be a
  referee-side check, not team [C]. The theorem does not depend on this
  either way.

**N3 — MINOR, housekeeping.**

- The status lines still read "NOT YET REFEREED": the findings file, line 18,
  and the paragraph added to `findings/colton-conjecture.md` §1.
- On merge they should cite this report.
- §8 item 1 ("Not refereed") should go.

## Recomputed independently (my code, `referee/colton-threshold-rs62/`)

All of this was run with `nice -n 19` on one core, 2026-10-31.

**1. Generator set G(28,653,696)** (`gen.c`).

- *Method:* a smallest-prime-factor table by plain Eratosthenes, with
  factorisation of every a ≥ 2, odd ones included; then the test
  a mod 2τ(a) = 0. π(g) comes from a prefix count of the same table.
- *Output:* 413,980 generators, and 2,063 / 2,938 / 3,795 of them are
  ≤ 110,000 / 160,000 / 210,000.
- *Hash:* the "a g" listing has sha256 `0be671d9…c6edaed18f`. That is
  identical to `results/rs62/` and to the refereed list of
  `colton-threshold.md`.
- *A difference from both team methods:* every a was tested, not only even
  a. No odd a appeared, which is consistent with §0.

**2. N, max S, β and L₀…L₆ for the four sets** (`stages.py`).

- *Method:* sums in Arb at 300 bits.
- *Integers:* they match both team input files exactly. The values are
  - N: 2063, 2938, 3795, 413980;
  - max S: 110000, 159936, 210000, 28653696;
  - β: 170282, 322537, 514970, 3348506095.
- *Moments:* each of my 35-digit midpoints lies inside both teams'
  32-digit enclosures, to within 10⁻³³ (`contain.py`, `contain.out`).

**3. The four inequalities, directly** (`stages.py`, `stages.out`).

These are evaluated in Arb on my own L_k balls, with no Lemma M
substitution and my own coefficient code. c₁…c₆ > 0 in every stage, and
c₀…c₆ > 0 in the tail.

| piece | g_S(ln q) | surplus |
|---|---|---|
| [10⁹, 10¹⁰], G(110,000) | 0.0225381374519 ± 4·10⁻¹⁴ | 917294.525306 ± 4·10⁻¹⁰ |
| [10¹⁰, 10¹¹], G(160,000) | 0.0207865005965 | 8704925.5071466 |
| [10¹¹, 10¹²], G(210,000) | 0.0175732579246 | 68866565.8700035 |
| [10¹², ∞), G(28,653,696), Lemma Q | — | 3287868063.03499 ± 9·10⁻⁷ |

- My tail terms, m = 0…6, are 289531364.2, 3.475568142·10⁹,
  1.572739159·10⁹, 691181881.2, 338146719.2, 175177352.5 and 94029539.90.
  Every one is ≥ the corresponding lower bound in the file's table.
- The minimum surplus is 917,294.525… ≥ 917,294, as claimed.

**4. RS62 (3.1), weak form, for every real x ∈ [59, 10⁹]** (`pigrid.c`,
`rs62low.py`, `rs62low.out`).

The argument:

- *f is increasing.* f(x) = (x/L)(1 + 1/(2L)) with L = ln x has
  f′ = (1/L)(1 − 1/(2L) − 1/L²) > 0 for L ≥ 2. So on any interval where π is
  constant or bounded below, it is enough to compare against f at the right
  end.
- *Below 10⁵,* on every prime gap [p_k, p_{k+1}): π = k ≥ f(p_{k+1}).
- *From 10⁵,* on every [X, X + 1000], X = 10⁵ + 1000j, up to 10⁹:
  π(X) ≥ f(X + 1000).

The data and the check:

- π comes from a byte-per-odd Eratosthenes sieve to 10⁹. Spot values:
  π(10⁶), π(10⁷), π(10⁸), π(10⁹) = 78498, 664579, 5761455, 50847534.
- Every comparison is an Arb ball at 128 bits, and is accepted only if the
  whole ball is > 0.
- **PASS.** Block minima: 0.170566 at 61, 1.076985 at 113, 12.051857 at
  1009 and 82.139136 at 10039. These equal the team's table. Above 10⁵ my
  coarser grid gives smaller slacks than theirs, as it must, and the
  smallest is 445.16.

**5. The file's float margins (§0 "what would have to be true", §4, §7)**
(`margins.py`, mpmath, 30 digits; not a proof).

| quantity | recomputed |
|---|---|
| ratio to β | 6.387, 27.99, 134.7, 1.982 ✓ |
| common L_k scale-down tolerance | 3.42%, 3.64%, 3.20%; tail 1.575% ✓ |
| Lemma Q from 10¹¹: ratio | 0.253 ✓ (claimed 0.25) |
| first grid M with L₀ > ½ | 1.7·10⁷ ✓ |
| pointwise bound at n = 10⁹ with G(110,000) | 1.878·10⁶ ✓ |
| one-piece scout G(290,000) on [10⁹, 10¹²] | 4.43·10⁵ ✓ |
| argmax of the ratio on the grid, per piece | M = 110,000, 160,000, 210,000 ✓ |

Also checked:

- T(10⁹) − π(10⁹)/2 = 32,608,999 − 25,423,767 = 7,185,232 ✓.
- The integers: 59·159,936 = 9,436,224 and 59·28,653,696 = 1,690,568,064 ✓.
- The rounded-up logs: ln 10⁹, 10¹⁰, 10¹¹, 10¹² = 20.72326583694…,
  23.02585092994…, 25.32843602293… and 27.63102111592854820821589745621…
  Each printed value is an upper bound ✓.

**6. The team's own pipeline**, run from a clean `git archive` of
`81ad7d7` in scratch.

- `inputs-build.py` regenerates both JSON files byte-identically.
- Both checkers exit 0 on both input files, and both print a smallest
  surplus of 917294.525306.

## Checked by re-derivation and found sound

- **§0.** Every element of G is even, and min G = 8: τ(2), τ(4), τ(6) = 2, 3, 4
  give 4 ∤ 2, 6 ∤ 4 and 8 ∤ 6. So g(a) is defined and ln a > 0.
- **Lemma 1.** τ(ap) = 2τ(a) when p ∤ a, and 2τ(a) | a | ap.
- **Lemma 2.** p is the largest prime factor of ap when p > g(a), which
  gives disjointness. The count is π(n/a) − π(g(a)), or 0 when n/a < g(a);
  (1.1) holds in both cases because π is nondecreasing.
- **Proposition A.** It needs n/a ≥ X₀ for every a ∈ S, which follows from
  n ≥ X₀·max S. Then 0 < ℓ < u, and both series have nonnegative terms, so
  the truncations at J and J − 1 are lower bounds.
  - Multiplying by α ≥ 0 keeps the direction.
  - The reindex m = k + 1 gives the coefficient α·m·L_{m−1}. I recomputed
    the coefficient of u^{−m−1}: ℓᵐ + α m ℓ^{m−1}.
- **Proposition B.** (3.2) is applied at x = n > 1, its stated range.
  Subtracting (n/u)(½ + (γ/2)/u) changes only c₀ and c₁, and needs J ≥ 1.
- **Lemma P.**
  - g_S is nonincreasing because c_m ≥ 0 for m ≥ 1.
  - x/ln x is nondecreasing for x ≥ e.
  - Both factors are nonnegative, given g_S(ln q) ≥ 0, so the product
    inequality is valid.
- **Lemma Q.** e^u u^{−m−1} is nondecreasing for u ≥ m + 1, and
  ln 10¹² ≈ 27.6 ≥ 7. With every c_m ≥ 0 the termwise bound holds.
- **Lemma M.** Every c_m is affine in the L_k with nonnegative coefficients
  (1, α, mα).
  - Replacing ln q by an upper bound only shrinks the m ≥ 1 terms, whose
    coefficients are ≥ 0.
  - c₀^lo carries no logarithm, so its sign is irrelevant there.
  - The m = 0 term in the tail is c₀ n_f/ln n_f, which needs c₀ ≥ 0. That is
    a hypothesis.
- **Coverage and seam.**
  - The four closed ranges [10⁹, 10¹⁰], [10¹⁰, 10¹¹], [10¹¹, 10¹²] and
    [10¹², ∞) cover every integer n ≥ 10⁹.
  - The range [C] covers 1 ≤ n ≤ 10⁹ inclusive, so n = 10⁹ is covered twice.
    There is no gap.
  - The corollary's strictness: 917,294 > 0 gives π(n) < 2T(n) for n ≥ 10⁹.
- **Where RS62 is applied.**
  - (3.1) is used for real x ≥ 9,090.9 ≥ 59. That is inside its stated
    range, and the theorem asserts it for real x.
  - (3.2) is used for integer x ≥ 10⁹ > 1.
  - Only the weak inequalities are used.
  - **No bound is applied outside its stated range.**
- **The RS62 quotation.** The findings file (§0) quotes (3.1) and (3.2)
  exactly as `literature/colton.md` gives them verbatim from the p. 69 scan:
  "for 59 ≤ x" and "for 1 < x". That agrees with zbMATH's independent
  transcription, as recorded there.
  - The same page's (3.4) has e^{3/2} = 4.48169, which fixes log = ln.
  - α = ½, X₀ = 59 and γ = 3/2 are used exactly as stated.
- **The [C] label on the inputs.** The two team implementations differ in
  method:
  - τ: an additive divisor-count sieve against a linear-sieve factorisation;
  - π(g): numpy Eratosthenes against PARI `primepi`;
  - sums: Arb against MPFR with directed rounding.

  My third implementation agrees with both.

## What I could NOT check

1. **RS62 Theorem 1's proof.** No one on this project has checked it. The
   theorem rests on (3.1) for real x > 10⁹ and (3.2) for integer x ≥ 10⁹ as
   [L]: the statement READ, the proof not checked.
   - I did not read the RS62 scan myself. I relied on `literature/colton.md`
     for the verbatim statement.
   - My Arb check removes the dependence on RS62 below 10⁹ only.
2. **No correction to RS62 in MathSciNet.** The literature pass could not
   reach MathSciNet, and neither can I.
3. **The rational checker's internals.** I did not audit its atanh-series
   logarithm line by line. Its numbers agree with my Arb computation and with
   the team's Arb checker, so an error there would have had to coincide
   with two other implementations.
4. **The team programs' code.** I read `verify/rs62/gen.c` and its README.
   I did not audit `search/rs62/*` or `verify/rs62/rs62.c` line by line.
   Instead I reproduced their outputs with my own code: generators, β, L_k
   and the (3.1) block minima below 10⁵.
5. **The float scout and the sanity programs of §7.** They ran in the
   author's scratch and are not part of the proof. I recomputed the margins
   they report from the committed grid instead (item 5).
6. **The exact range [1, 10⁹].** I did not re-referee it. I relied on
   `referee/colton-range.md`, whose R1 gap is closed in
   `colton-conjecture.md` §2.
7. **My Arb check of (3.1) is one program.** It is a referee's
   directed-rounding check of something the theorem does not need. It is not
   a team [C].

## Reproduce

Round 2: `gcc -O2 -o rs62every $R/rs62every.c -lflint -lmpfr -lgmp && ./rs62every` (39 s, 0.5 GB RAM).

Round 1:

```
PY=~/dev/projects/open-problems/.venv/bin/python
R=referee/colton-threshold-rs62
gcc -O2 -o gen $R/gen.c && ./gen 28653696 > gen.txt              # 3.5 s
$PY $R/stages.py gen.txt                                          # 2 s
gcc -O2 -o pigrid $R/pigrid.c && ./pigrid > pigrid.txt            # 5 s, 0.5 GB RAM
$PY $R/rs62low.py pigrid.txt                                      # 3 s
# against a checkout of lead-colton-rs62 @ 81ad7d7:
$PY $R/contain.py <lead>/findings/colton-threshold-rs62-inputs.json <lead>/findings/colton-threshold-rs62-inputs-verify.json
$PY $R/margins.py <lead>/results/rs62/moments-grid.txt
```

`generators-28653696.sha256` records the sha256 of the "a g" listing of
`gen.txt`, and of `pigrid.txt`.
