# Second implementation: p-generators (2*tau(a) | a), OEIS A111291 / Zelinsky Thm 22

Author: open-problems/check-generators, 2026-10-30. Written from the problem statement only (never read `search/`
or `results/generators/`). Python = project venv, PARI via cypari2. Method: constructive enumeration, no sieve of tau.

## Results (all M, one run to 1e9, lists for smaller M are prefixes of the canonical list)
Evidence label: pending referee; computed exactly here by one method + cross-checks below ([C] needs agreement with the other implementation).

| M | count | A = sum 1/a (rigorous bounds, 30 digits) | sum pi(g) | B = sum(pi(g)+1) | sha256 of "a g\n" list |
|---|---|---|---|---|---|
| 1e6 | 16717 | 0.458200261130726223049408353832 .. ...833 | 7884795 | 7901512 | b4c39f15...40dfd |
| 1e7 | 150788 | 0.493095317810104210206092860160 .. ...161 | 491083595 | 491234383 | e5bd85a5...4d4 |
| 28653696 | 413980 | 0.508000047238841733452073262987 .. ...988 | 3348506095 | 3348920075 | 0be67198...d18f |
| 1e8 | 1377071 | 0.524950206194584139618713115440 .. ...441 | 33372518093 | 33373895164 | 7a957a85...53c8 |
| 1e9 | 12702327 | 0.554320785055140975830815237974 .. ...975 | 2415172104191 | 2415184806518 | b67be982...f457 |

Full hashes and bounds: `results.txt` (verbatim output of `summarize.py`).
Full sha256: 1e6 `b4c39f150a491025225d4f4bea0c3dce55f5cc87fd528ded620ecbb554f40dfd`;
1e7 `e5bd85a50c8277b9c586359d08eb0aea020785c4a88c68b4792b743d5a51d4d4`;
28653696 `0be671d98fb91d71e976103c0c69d30284504489073aef8c8171bac6edaed18f`;
1e8 `7a957a85e676316b9e2e102a769631e76696cebce30c02aa19f3a92e2a0553c8`;
1e9 `b67be982e3b0231f30712af5df2985285ad56b3af4878469e1050662cafcf457`.

Lists: `list_<M>.txt.gz` for M = 1e6, 1e7, 28653696, 1e8 (re-hashing the decompressed file reproduces the sha above;
checked for 28653696 and 1e8). For 1e9 regenerate: `python gen.py 1000000000 out.txt` (38 s, one core) then
`cut -d' ' -f1,2 out.txt | sha256sum` (out.txt has a third column, pi(g)).

**Zelinsky Theorem 22 at M = 28,653,696: all three confirmed.** count = 413,980 exactly; A = 0.5080000472... > .508
(margin 4.7e-8, so the claim is true but razor-thin; the rigorous interval is far inside it); B = 3,348,920,075 < 8,694,520,815
(true, but the stated bound is 2.6x the actual value, so B is not Zelinsky's exact figure - his is an upper bound).
Note g(a) here is the largest prime factor; the B convention is exactly the brief's sum(pi(g)+1).

## Commands
    python gen.py 1000000000 g1e9.txt        # 'a g pi(g)' ascending; ~38 s, 1 core
    python summarize.py g1e9.txt             # results.txt; 200000 random primepi spot checks (use --full for all: ~ms each, hours)
    python brute.py 100000 g1e9.txt          # independent brute force a<=1e5 (trial division)
    gcc -O2 -o sieve_check sieve_check.c; ./sieve_check 100000000 | cmp - <(cut -d' ' -f1 g1e9.txt | awk '$1<=1e8')

## Method
Every a>1 has a signature: the non-increasing tuple f of its prime exponents; tau(a)=prod(f_i+1)=:T depends on f only.
So 2*tau(a)|a iff D:=2T divides a. D is tiny (T<=~10^4) and its prime factors are <= 31.
1. Enumerate signatures f with minimal value prod p_i^{f_i} (p_i = i-th prime, largest exponent on smallest prime)
   <= M. Valid: any a with signature f is >= that minimum (rearrangement inequality). 1273 signatures for M=1e9.
2. For a signature, enumerate exponent sequences over primes in increasing order: each prime used gets one remaining
   exponent from the multiset (each distinct value tried once, so each a is produced exactly once, as its factorisation
   is unique), all other primes get 0. The a produced has signature f exactly, so tau=T; we force D|a so the generator
   condition holds by construction. a is built as a product, never factored.
3. Prunes, each with its proof:
   - (P1) Forced primes: each prime p|D, with v_p(D)=d, must be used with exponent >= d. So at a step that jumps past an
     unmet forced prime p (chooses q>p) the branch is dead, hence q<=p; if q=p then e>=d. Also #unmet forced primes <= #remaining
     exponents, and the sorted required d's must be dominated by sorted f (greedy matching): necessary since distinct primes need
     distinct slots. All are necessary conditions of D|a, so no generator is lost.
   - (P2) Size: cur*q^e*(min product of remaining exponents R2 on the primes after q) <= M, break the loop on the first failure.
     The bound is the rearrangement minimum on the primes following q (all later primes are larger), and it is increasing in q,
     so breaking is valid.
   - (P3) Last slot, exponent 1: all primes q in (last used, M/cur], listed by PARI `primes([lo,hi])`; the count is asserted
     equal to primepi(hi)-primepi(lo) (so no prime is skipped or invented). Last slot exponent e>1: q<=floor((M/cur)^(1/e)),
     integer root by gmpy2, primes from a PARI table of the first 20000 primes (enough: q<=31623).
   - (P4) The non-last primes are always < sqrt(M) <= 31623, inside the 20000-prime table (largest 224737).
pi(g): for a last-slot prime q at position k in the list, pi(q)=pi(lo)+k+1; pi(lo) is a table index of PARI's prime list.
This is cross-checked by (i) the primepi(hi) count assertion for every range, (ii) 200000 random records vs `primepi(g)`
(0 mismatches), (iii) primepi(10^k)=known values k=1..9.
A: exact integers: lo = sum floor(10^40/a), hi = lo+count (each floor loses <1); printed truncated/rounded outward to 30 digits.
The width of every interval is <1e-30 after the outward rounding, as shown by the one-ulp gaps in the table.

## Cross-checks done
- `brute.py`: trial-division tau for all a<=1e5: same 1887 (a,g) pairs. (`brute_out.txt`)
- `sieve_check.c`: plain divisor-count sieve to 1e8 (a different method, written by me, NOT the main method): its 1,377,071 generators
  equal the list for 1e8 exactly (`cmp` clean).
- Rerun with M=1e8 (different prunes active) is byte-identical to the 1e9 list restricted to a<=1e8.

## Not established
- pi(g) was checked against primepi on a 200000-record random sample plus the per-range count assertions, not on every one of the
  12.7M records (primepi costs ~ms per call at these sizes).
- 1e9 completeness rests on the pruning proofs and on agreement at <=1e8 with two other methods; there is no independent sieve at 1e9 from me.
- No claim of agreement with the other implementation: that comparison is the lead's.

## Extra sums (ticket tmvvueaws0gs9, 2026-10-30): `moments.txt`, `moments.py`
`python moments.py g1e9.txt > moments.txt` (uses the list produced by gen.py; M = 16694, 166944, 28653696, inclusive).
L_k = sum (ln a)^k / a for k=0..6 by python-flint `arb` at 256 bits: every term is a ball (ln and division enclosed), the sum is a ball
sum, so the printed radius (~1e-66..1e-75, in `moments.txt`) is a rigorous error bound; the 30-digit mid/enclosure print is
identical at both ends because the radius is far below the 30th digit. L_0 agrees with the A in the table above. Also in the file: N, beta, B = beta+N,
max G, max a*g(a), and for M=28653696 the cofactors a/g for g > M/128 (g*128 > M): {36: 43723, 80: 10683, 96: 5952}, total 60358.
beta and B are exact integers, with the same pi(g) caveats as above (the pi values come from the same records).
