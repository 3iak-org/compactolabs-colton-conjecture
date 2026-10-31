# range2 - pi(n) <= 2T(n) for 1 <= n <= 10^9, second implementation

Written blind (did not read search/, results/range/, verify/range/ or the findings before committing).

Method: no factorisation anywhere.
- tau(n): additive divisor sieve per block of 10^6; for each d with d^2 <= hi add 2 at every multiple m >= d^2, subtract 1 at d^2.
  T counts n with n % tau(n) == 0.
- primality: segmented sieve of Eratosthenes (tau is never consulted for pi).
- independent pi: PARI primepi at all 1000 checkpoints and at 10^1..10^9 (crosscheck.py).
- two passes: block totals, then a running T, pi with offsets, checking 2T-pi at every n.

Command: `gcc -O2 -fopenmp -o r2 r2.c && OMP_NUM_THREADS=6 nice -n 19 ./r2`  then `crosscheck.py` (venv python).
Runtime: 10.6 s wall, 53 s CPU (6 threads). Date 2026-10-31.

## Results
1. 2T(n) - pi(n) >= 0 for every 1 <= n <= 10^9. Equality exactly once: n = 7 (equality.txt).
2. checkpoints.txt: 1000 lines "n T(n) pi(n) m_k", n = k*10^6, m_k = min over primes p in ((k-1)e6, k e6] of 2T(p)-pi(p).
   sha256 985f8d879d07621722caa482a10599d8fce1f1c05ce894cd3da39b310ef9f1c9
3. min of 2T(n)-pi(n) over [10^6, 10^9] = 10910, first attained at n = 1000697.
4. Cross-checks, all agree: pi(10^k) k=1..9 = 4, 25, 168, 1229, 9592, 78498, 664579, 5761455, 50847534 (sieve and PARI);
   T(10^k) k=0..9 = 1, 4, 16, 92, 665, 5257, 44705, 394240, 3558181, 32608999
   (k<=5 by a separate tiny Python divisor sieve; k=6..9 from the checkpoint file). PARI primepi agrees with the sieve at all 1000 checkpoints (0 mismatches).

Limit: PARI independently checks pi only at the 1000 checkpoints; pi at other n comes from the sieve alone (consistent via block totals).
