# Colton A111291, finite range: pi(n) <= 2T(n) for every 1 <= n <= 10^9

Status [C]-candidate (one implementation, `search/range/rangesieve.c`; the second implementation is `check-range`'s and is not read here). Not [C] until the two agree.

**Lead note, 2026-10-31.** This program and `verify/range/blocks.c` agree byte for byte but share a METHOD (factorisation of the remainder, primes = tau==2), so together they are not [C] (ref-colton GAP R1, referee/colton-range.md). The different-method evidence is `referee/colton-range/dpair.c` (divisor-pair counting), adv-colton's range implementation (adversary/colton.md), and `verify/range2/` when it lands. See findings/colton-conjecture.md for the label.
Date 2026-10-30. Base commit 116e4ff (code and results are in the commit that adds this file). Machine: WSL2, 8 cores, gcc -O2.

T(n) = #{1<=k<=n : tau(k) | k}, tau = divisor count.

## Result
pi(n) <= 2T(n) for every integer 1 <= n <= 10^9.
- Equality holds **only at n = 7** (T=2, pi=4). Complete list of equality cases: {7}. Every n <= 10^6 is checked per n (`raw/verbose-block1.txt`: no `EQ` lines, one `margin=0` line, n=7); beyond 10^6 the margin is >= 10910.
- min of 2T(n)-pi(n) over n in [10^6, 10^9]: **10910, first attained at the prime p = 1000697** (T=85803 and pi=148933 at n=2*10^6 are in checkpoint 2). The margin at n = 10^6 itself is 10912. Margin at n = 10^9: 2T - pi = 14370464. (Corrected 2026-10-31 by lead-colton, per adv-colton: the earlier figure 14355343 is m_1000, the minimum over primes in the last block, not the margin at n = 10^9.)
- Every n <= 1000 with margin <= 2 (n, T, pi, margin): (1,1,0,2) (3,2,2,2) (4,2,2,2) (5,2,3,1) (6,2,3,1) (7,2,4,0) (8,3,4,2) (53,9,16,2) (54,9,16,2) (55,9,16,2) (71,11,20,2) (79,12,22,2). All others n<=1000 have margin >= 3. Both the C run and the independent trial-division script `crosscheck.py` print this list; they are identical.
- T(10^9) = 32608999, pi(10^9) = 50847534.

## Lemma (reduction to primes)
Claim: if 2T(p) >= pi(p) for n=1 and for every prime p <= N, then 2T(n) >= pi(n) for every 1 <= n <= N.
Proof. n=1: pi(1)=0 <= 2T(1)=2. For 2 <= n <= N let p be the largest prime <= n (exists, p<=N). Then pi(n)=pi(p) since no prime lies in (p,n], and T(n) >= T(p) since T counts a set that only grows with n. So 2T(n) >= 2T(p) >= pi(p) = pi(n). QED.
Tail: with N = 10^9 the largest prime is 999999937 and every n in [999999937, 10^9] is covered by the same argument (the check at p = 999999937). The margin reported above is the minimum of the margin over the primes; the minimum over all n in a range [a,b] equals the minimum over {a} and the primes in (a,b], by the same monotonicity.

## Method
`search/range/rangesieve.c`: blocks ((k-1)10^6, k10^6], sub-segments of 10^5. For each sub-segment, trial-free factor sieve: for every prime p <= 31700 with p^2 <= segment top, for each multiple strip all factors of p from a remainder array and multiply tau by (e+1); afterwards a remainder > 1 is one prime >31623 (a composite <= 10^9 has a prime factor <= 31622), so tau *= 2. n is prime iff tau = 2. T counts tau | n. Per block it reports T_b, pi_b, and the minimum over primes of the local margin 2T_l - pi_l (counted from block start); `combine.py` adds the offset 2T_0 - pi_0 from the preceding blocks.
Run: `systemd-run --user --scope nice -n 19 search/range/run_all.sh <binary> results/range/raw` (6 workers), then `python search/range/combine.py`. Wall 8.7 s, CPU 47 s.
Block 1 is run separately with `-v` for per-n output (`raw/verbose-block1.txt`).

## Checkpoints
`checkpoints.txt`, sha256 `985f8d879d07621722caa482a10599d8fce1f1c05ce894cd3da39b310ef9f1c9`. No header, deliberately: that sha256 is reproduced byte for byte by four implementations and is cited in the findings, so the file stays headerless (ref-colton R3 declined for that reason; this paragraph is the format's documentation); 1000 lines `n T(n) pi(n) m_k`, n = k*10^6, m_k = min over primes p in ((k-1)10^6, k10^6] of 2T(p)-pi(p). Line 1's minimum 0 is at p = 7. `checkpoints-annotated.txt` (sha256 8b6cbd11...29cdf) is the older form with a header, a k column and the smallest argmin prime; same numbers.

## Cross-checks (`crosscheck.py`, output `crosscheck.txt`)
- pi(10^k), k=1..9 equal 4, 25, 168, 1229, 9592, 78498, 664579, 5761455, 50847534: match.
- T(10^k), k=0..9 equal 1, 4, 16, 92, 665, 5257, 44705, 394240, 3558181, 32608999 (A111291 data as supplied in the brief): match.
- Brute force with tau by trial division, every n <= 10^5: only equality n=7; margin list for n <= 1000 identical to the C run.

## Standalone verifier
`search/range/verify_segment.py checkpoints.txt K` (about 33 lines, numpy, different structure from the C code: vectorised exponent stripping) recomputes block K from the T,pi of line K-1 and compares line K (argmin not compared: not in the file). Spot-checked K = 1, 2, 500, 1000: OK; a deliberately corrupted T on line 500 gives MISMATCH, exit 1.

## Not established
Only one implementation so far. The A111291 values quoted are those in the brief, not re-read from OEIS here. Nothing here depends on the threshold finding; it only overlaps it (n >= 10^7).
