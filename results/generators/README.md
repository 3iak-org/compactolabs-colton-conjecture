# p-generators up to 1e9 (Colton / Zelinsky Thm 22 inputs)

A p-generator is a with 2*tau(a) | a. g(a) = largest prime factor (g(1)=1; 1 is not a generator).
Computed 2026-10-30 on PC2 (8 cores, WSL2), commit c4ec96d + this directory's files.

    gcc -O2 -fopenmp -o gen search/generators/gen.c -lm
    OMP_NUM_THREADS=6 systemd-run --user --scope -q nice -n 19 ./gen 1000000000 full     # 21.6 s wall, 1m51 CPU
    python search/generators/stats.py full.txt full.pi results/generators
    python search/generators/selftest.py ./gen          # brute-force tau/g/pi for a <= 1e5: OK (1887 generators)

Method: segmented sieve (2^20 per segment); each prime p <= sqrt(hi) is divided out of a residue array,
accumulating tau and the largest prime factor; leftover residue > 1 is a prime. pi(g) from an odd-only bit sieve
up to max g (27,777,769) with popcount prefix. [C]-candidate only: ONE implementation. It becomes [C] when the
independent `check-` implementation reproduces the sha256 values below.

## Results (summary.txt has the full-precision lines)

| M | count | A = sum 1/a (30 digits) | sum pi(g) | B = sum(pi(g)+1) | sha256 of canonical list |
|---|---|---|---|---|---|
| 1e6 | 16717 | 0.458200261130726223049408353832 | 7884795 | 7901512 | b4c39f150a491025225d4f4bea0c3dce55f5cc87fd528ded620ecbb554f40dfd |
| 1e7 | 150788 | 0.493095317810104210206092860160 | 491083595 | 491234383 | e5bd85a50c8277b9c586359d08eb0aea020785c4a88c68b4792b743d5a51d4d4 |
| 28653696 | 413980 | 0.508000047238841733452073262987 | 3348506095 | 3348920075 | 0be671d98fb91d71e976103c0c69d30284504489073aef8c8171bac6edaed18f |
| 1e8 | 1377071 | 0.524950206194584139618713115440 | 33372518093 | 33373895164 | 7a957a85e676316b9e2e102a769631e76696cebce30c02aa19f3a92e2a0553c8 |
| 1e9 | 12702327 | 0.554320785055140975830815237974 | 2415172104191 | 2415184806518 | b67be982e3b0231f30712af5df2985285ad56b3af4878469e1050662cafcf457 |

A is not an exact rational here (the lcm of the denominators is astronomically large). Each term is
floor(10^60/a); lower bound = their sum, upper bound = lower + count (each floor loses < 1 unit).
The bounds in summary.txt agree to >= 40 digits, so the 30 printed digits are rigorous (truncated, not rounded).
B and the pi sums are exact integers.

## Zelinsky's three numbers (Thm 22, M = 28,653,696)

CONFIRMED: count 413,980 exactly; A = 0.5080000472... > .508 (margin only 4.7e-8, so "over .508" is true but tight);
B true value is 3,348,920,075, which is < 8,694,520,815 (Zelinsky's bound is valid and about 2.6x loose).

## Files

- `generators-le-1e8.txt.gz`: canonical list, "a g\n" per generator ascending (zcat sha256 = the 1e8 row).
  Prefixes a <= M give the other rows (`awk '$1<=M'`).
- `pi-g-le-1e8.txt.gz`: pi(g(a)) per line, aligned with the list (derived; not hashed).
- The 1e9 list is 210 MB / 70 MB gzipped, over the cap, so it is not committed: regenerate with the command
  above (deterministic; `full.txt` hashes to the 1e9 row, `full.pi` is the aligned pi column).
- `summary.txt`: the numbers above at full precision.

## moments.txt (ticket tmvvueavuaamy, 2026-10-31)

N(M), beta, B, max G, max a*g, L_k = sum (ln a)^k / a for k=0..6, and the cofactor table, for M in {16694, 166944, 28653696}.
Command: `python search/generators/moments.py results/generators/generators-le-1e8.txt.gz results/generators/pi-g-le-1e8.txt.gz > results/generators/moments.txt`.
Method: python-flint arb balls at 300 bits; ln a and 1/a are enclosures, sums are balls. The printed value is the ball midpoint
to 35 digits; the ball radius (<= 2e-79 in every case, i.e. > 70 correct digits) is printed beside it. Cofactors use g > M/128 strictly
(M/128 = 223857 exactly): a/g in {36: 43723, 80: 10683, 96: 5952}, 60358 elements. L_0 agrees with A above.
