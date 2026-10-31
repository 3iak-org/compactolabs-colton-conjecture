# Referee report: Colton finite range [1, 10⁹], and the seam

*`ref-colton`, second pass, opened by ticket from `dev`, 2026-10-31.
Refereed: `results/range/`, `search/range/`, `verify/range/` at
`lead-colton` @ `41adad0`, and the seam with the threshold theorem
(`findings/colton-threshold.md`, refereed in `referee/colton-threshold.md`).
I wrote none of it.*

## Verdict: **ACCEPT WITH CORRECTIONS**

The claim holds: π(n) ≤ 2T(n) for every integer 1 ≤ n ≤ 10⁹, with equality
only at n = 7. I recomputed every n in [1, 10⁹] with a third program by a
different method (divisor-pair counting, no factorisation). Its checkpoint
file is **byte-identical** to both of theirs: sha256 `985f8d87…f1c9`.

There is one **GAP**, and it is about the label, not the mathematics. The two
implementations behind the [C] use the **same method**. I could close the
evidence gap from here, but only the owner can correct the text. Two MINOR
items concern the stated scope (n = 0).

Combined with the refereed threshold, this covers every n ≥ 1, and both
seam edges are right (see "The seam" below). Colton's conjecture in the π form,
`colton_conjecture` in formal-conjectures, then rests on three things:

- the [C] range (with the GAP fixed);
- the threshold theorem, [T] on [C] inputs;
- the cited Dusart (6.5), see R6.

## Findings

**R1 — GAP: the two range implementations share their method.**

Files: `results/range/README.md` "Method", `search/range/rangesieve.c`, and
`verify/range/README.md:9`, "Method (shares nothing with a divisor-count
sieve / sieve of Eratosthenes)".

The dev ticket describes `results/range` as "a divisor-count sieve plus
Eratosthenes". **It is not one.** Reading the code, both programs compute
τ the same way:

- They run a segmented factor-stripping sieve: rem[i] = n.
- For every prime p ≤ √hi, each multiple has p divided out fully, and
  τ is multiplied by (e+1).
- A leftover rem > 1 is taken to be one prime, so τ is multiplied by 2.
- Both declare n prime iff τ(n) = 2.

They differ only in:

- how the small primes are found: Eratosthenes (`rangesieve.c:19`) versus
  trial division (`blocks.c:17`);
- the segment size: 10⁵ versus 10⁶;
- an independent π at the 1000 checkpoints, PARI `primepi`, in `verify`
  only.

`verify/range`'s "shares nothing with a divisor-count sieve" is true but
beside the point: the other program is not a divisor-count sieve either. By
the standing rule (no shared code *and no shared method*), T(n) is backed by
one method and is not [C] from these two alone. π is better off, because
`verify/range` checks it against PARI at every checkpoint.

The risk this rule exists for is real here. Both programs share every
structural assumption:

- the small-prime bound 31,700 ≥ √10⁹;
- the break condition p² > hi;
- "the leftover is a single prime";
- the uint16 τ;
- counting τ | n per segment.

I found no error in any of these. But two programs built on them cannot
check them against each other.

**Repair (evidence done here; text is the owner's).**

- `referee/colton-range/dpair.c` computes τ(n) as the number of divisor
  pairs: for each d ≤ √hi, every multiple m ≥ d² of d gets +2 (+1 if
  m = d²). There is no factorisation, no prime list and no remainder.
- Primes are n > 1 with τ = 2.
- It ran all 1000 blocks: 2 processes under nice 19, under a minute.
- Its checkpoint file, built in the same format by
  `referee/colton-range/combine_ref.py`, has **sha256
  985f8d879d07621722caa482a10599d8fce1f1c05ce894cd3da39b310ef9f1c9**. That
  is identical to `results/range/checkpoints.txt` and
  `verify/range/checkpoint.txt`.
- So the [C] can rest on a different method (`dpair.c`) plus either theirs.

The owner should:

- relabel accordingly, citing this report and `dpair.c` as the
  different-method implementation;
- correct the "divisor-count sieve" description wherever it appears
  (ticket, master plan, findings);
- remove or qualify the "shares nothing" sentence in `verify/range/README.md`.

One fair caveat: `dpair.c` was written by the referee. If the project wants
the [C] implementations kept apart from the refereeing, the owner can commission
an independent divisor-count or linear-sieve implementation instead. I judge
that unnecessary, but it is the owner's call.

**R2 — MINOR: n = 0.**

- `colton_conjecture` in formal-conjectures (the Lean target named in
  `literature/colton.md`) quantifies over **all n : ℕ, including 0**.
- There π(0) = 0 and T(0) = 0, since `Icc 1 0` is empty. So it holds, **with
  equality**.
- Neither strand mentions n = 0. And "equality only at n = 7" is false over
  ℕ: it is {0, 7}.
- Fix: state the range as n ≥ 1 and add the line "n = 0: 0 ≤ 0, equality,
  trivially". Or state the equality set over ℕ as {0, 7}.

**R3 — MINOR: the format of `checkpoints.txt`.** It has no header, and the
meaning of m_k is documented only in the README. The annotated file carries
a header, but it has a different sha. It would be easy to make the plain file
self-describing. That is not a correctness problem.

## The reduce-to-primes lemma (question 1): sound

Statement (`results/range/README.md`, "Lemma"): if π(1) ≤ 2T(1) and
2T(p) ≥ π(p) for every prime p ≤ N, then π(n) ≤ 2T(n) for every
1 ≤ n ≤ N. I re-derived it:

- For n ≥ 2, let p be the largest prime ≤ n. Then π(n) = π(p), and
  T(n) ≥ T(p) because T counts a growing set.
- So 2T(n) − π(n) ≥ 2T(p) − π(p) ≥ 0.

The margin is nondecreasing between consecutive primes and drops only at
primes. So the minimum over (a, b] is attained at a prime in (a, b] or at a.

Block assembly also checks out. The global margin at a prime in block k is
2T((k−1)10⁶) − π((k−1)10⁶) + (local margin counted from the block start),
because T and π are additive over disjoint blocks. In `rangesieve.c` the
local counters Tb and pib are reset per 10⁶ block, not per 10⁵ sub-segment
(lines 24–33), which is correct.

So m_k ≥ 0 for every k, together with n = 1, covers every n ≤ 10⁹:

- m₁ = 0, at p = 7;
- m_k ≥ 10,910 for k ≥ 2.

The equality claim needs one more step, which the README states only
implicitly. A non-prime n has margin ≥ the margin at the largest prime
p ≤ n. So equality at a non-prime needs margin(p) = 0, which happens only
for p = 7. And 8 is refactorable, so the margin at n = 8 is 2. Hence
equality on [1, 10⁹] holds only at 7.

`verify/range` does not rely on the lemma: it takes block minima over all
n. My `dpair.c` does the same. Over all n, block 1 has minimum 0 (only at
n = 7, by a separate numpy check of every n ≤ 10⁶), and blocks 2–1000 have
minimum 10,910.

## Recomputed (question 3)

- **The full range.** All 1000 checkpoint lines (n, T, π, m_k) are
  reproduced exactly by `dpair.c` (R1).
- **Known values, π(10^k) and T(10^k):**
  - π(10⁶…10⁹) = 78,498; 664,579; 5,761,455; 50,847,534. These are the
    standard published values.
  - T(10⁶…10⁹) = 44,705; 394,240; 3,558,181; 32,608,999.
  - My exact scan in the threshold pass, a third method (a linear sieve),
    gave the same T(10⁷) and T(10⁸).
- **PARI `primepi` at 123, 457, 500, 777 and 999 × 10⁶.** All agree with
  the checkpoint π column.
- **Every n ≤ 10⁶** (numpy, divisor-count by multiples):
  - the only n with margin ≤ 0 is n = 7;
  - the n ≤ 1000 with margin ≤ 2 are exactly the twelve both READMEs list:
    1, 3, 4, 5, 6, 7, 8, 53, 54, 55, 71, 79, with the same margins;
  - the margin at 10⁶ is 10,912.
- **The global minimum over [10⁶, 10⁹]** is 10,910, in block 2. I did not
  locate its argmin; both teams say n = 1,000,697.

## Independence and the checkpoint format (question 2)

- Code: no shared code. The two are different files and the authors say
  neither read the other's; that is plausible.
- Method: shared (R1).
- π: independent at the checkpoints in `verify/range` only (PARI).
- Format: four integers per 10⁶ block. A third party can recheck any block
  in about 0.1 s from the line before it, as `search/range/verify_segment.py`
  and my `dpair.c` both do, and the lemma makes a block check complete for
  that block. This is enough for a quick, piecewise third-party recheck.
  It is not a certificate cheaper than recomputation, and none is possible
  for this quantity at this cost.

## The seam (question 4): sound

- **Threshold side.** Every integer n ≥ 10⁷, inclusive, has
  T(n) − π(n)/2 ≥ 3,616, so 2T(n) − π(n) ≥ 7,232 > 0. That is strict, so
  there is no equality case there.
- **Range side.** Every integer 1 ≤ n ≤ 10⁹, inclusive.
- **Overlap.** [10⁷, 10⁹], two orders of magnitude, with no ≤/< hazard at
  either end. In the overlap the exact minimum of 2T − π is 123,901 (at
  n = 10⁷, from the checkpoints and `dpair.c`). That is consistent with the
  threshold's 7,232 and 17× above it.
- **Definitions match** `colton_conjecture`:
  - T counts k ∈ [1, n] with τ(k) | k, which is `countRefactorableNat`;
  - π counts primes ≤ n, which is `Nat.primeCounting`;
  - τ(1) = 1 divides 1, so 1 is counted. Both programs and mine count it:
    T(1) = 1, margin 2.
- **Small n:** n = 1…8 are checked per n (margins 2, 2, 2, 2, 1, 1, 0, 2).
  n = 0: R2.

## What the combined statement needs that neither strand proves (question 5)

- **R4. A combined finding.** There is no `findings/` file that states
  "π(n) ≤ 2T(n) for all n ≥ 0 (equality exactly at n ∈ {0, 7})" and cites
  both strands with their labels. It must be written before the claim is
  made anywhere.
  - The novelty verdict in `literature/colton.md` covers the finite range.
  - "Colton's conjecture is proved" is a new combined claim, and needs its
    own sentence there.
- **R5. Form of the conjecture.** Only the π form is covered. Colton's
  original sentence ("refactorables less than x is at least x/(2 log x)")
  is a different pointwise statement, for real x. Neither strand addresses
  it, and the combined finding should say so rather than call "Colton's
  conjecture" settled in every form.
- **R6. Dusart (6.5).** The threshold, and so the combination, still rests
  on this cited input. `lit-colton-dusart` was opened for the refereed
  version, and PR #25 is merged into dev; I have not read its result. The
  combined finding should cite that read.

## Also checked at 41adad0 (threshold strand, unchanged mathematics)

- The inputs JSON changed format: it now carries L with an enclosure
  radius L_rad.
- My PARI values from the first pass lie inside every enclosure, with slack
  ≥ 5·10⁻³⁶.
- Both checkers at 41adad0 pass on it.
- The theorem's statement and surplus are unchanged.
- I did not re-referee the text changes.

## Limits: what I could NOT check

1. **My implementation is the referee's own.** It shares no code and no
   method with either team program. But a referee-written second
   implementation is a judgement call (R1).
2. **The argmin 1,000,697** of the [10⁶, 10⁹] minimum was not located by
   me; only the value 10,910 was confirmed.
3. **`search/range/verify_segment.py`** was not run, and
   `crosscheck.py`'s trial-division run was not re-run.
4. **The A111291 data.** I did not re-read the OEIS values against the
   source. They are reproduced by computation here.
5. **No [F].** formal-conjectures' `colton_conjecture_le_500` is by
   `native_decide`, which this project does not count as [F].
6. **Dusart.** See R6.

## Reproduce

```
cd referee/colton-range
gcc -O2 -o dpair dpair.c
nice -n 19 ./dpair 1 600 > p1.txt & nice -n 19 ./dpair 601 1000 > p2.txt; wait   # < 1 min, 2 cores
~/dev/projects/open-problems/.venv/bin/python -I combine_ref.py p1.txt p2.txt   # writes mine_ckpt.txt, prints sha256
# committed outputs: blocks-dpair.txt (= p1+p2, "k Tb pib minlocal_primes minlocal_all"), checkpoints-dpair.txt
```
