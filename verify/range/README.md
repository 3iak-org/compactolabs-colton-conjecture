# verify/range: second implementation, pi(n) <= 2T(n), 1 <= n <= 10^9

Date 2026-10-30, base commit 116e4ff (code in this directory's commit). Written from the problem statement only; `search/` and `results/range/` not read.

## Verdict
**pi(n) <= 2T(n) holds for every 1 <= n <= 10^9.** The check is on EVERY n (no prime-only reduction used).
Equality pi(n) = 2T(n) occurs for **n = 7 only** (T(7)=2, pi(7)=4); no n up to 10^9 has margin 0 other than 7.
Margin 2T-pi: n=1:2; n<=1000 with margin<=2: see below. Over [10^6,10^9] min margin = **10910**, first at **n = 1000697** (n=10^6 itself has 10912). In every block k>=2 the block minimum is positive; the 10910 occurs only in block k=2 (next smallest block min is 22672, block 3).
Status: [C] pending agreement of the other implementation (diff the checkpoint).

## Method (factorisation: trial-division small primes, tau from exponents; primes taken from tau == 2)
2026-10-31: referee/colton-range.md GAP R1 found that this program and search/range/rangesieve.c share a method (both factorise; both take primes from tau==2), so they are not independent. The different method (additive divisor sieve, no factorisation, segmented Eratosthenes for primes) is verify/range2/; its checkpoints.txt is cmp-identical to checkpoint.txt here.
`blocks.c`: for each block of 10^6 integers, start from rem[n]=n, tau=1; for each small prime p<=sqrt(hi) (small primes by trial division) divide p out of every multiple fully, count exponent e, multiply tau by (e+1); a leftover rem>1 is one prime >sqrt(hi), multiply by 2. T counts tau(n) | n; n is prime iff tau(n)=2 (n>1). Per block it emits T-count, prime count, local minima of 2T-pi (over primes; over all n). `merge.py` stitches blocks with prefix sums and asserts at all 1000 checkpoints that the cumulative prime count equals **PARI primepi(k*10^6)** (independent counter): all 1000 agree. `brute.py`: separate brute force for n<=10^5 (tau by trial-division divisor counting): no violations, equality only at 7, and (T,pi) at 10,100,...,10^5 = (4,4),(16,25),(92,168),(665,1229),(5257,9592).
Block-min over all n is used for the verdict (so no reduction to primes is needed); the checkpoint column m_k is min over primes, as specified.

Reference values reproduced: pi(10^k), k=1..9 = 4,25,168,1229,9592,78498,664579,5761455,50847534 (k<=5 brute force; k>=6 from checkpoint = PARI); T(10^k), k=0..9 = 1,4,16,92,665,5257,44705,394240,3558181,32608999 (T(10^7..10^9) read from checkpoint rows, T(10^6)=44705, smaller from brute force; T(1)=1).

## Reproduce
```
gcc -O2 -o blocks blocks.c
for c in 0..5: ./blocks a b > partC   # k ranges [1,168),[168,335)... jointly 1..1000 (6 procs, nice 19); ~10 s wall, 57 s CPU
cat parts | sort -n > blocks.raw
python merge.py blocks.raw   # needs cypari2; ~3-4 min (primepi calls) -> checkpoint.txt
./blocks 1 2 0 0 0           # eq_block1.txt: n with margin<=0 in block 1 (only n=7)
./blocks 2 3 44705 78498 10910   # min_block2.txt (first lines: n=1000697 margin 10910)
python brute.py
```
## Outputs
- `checkpoint.txt`: 1000 lines "n T(n) pi(n) m_k", n=k*10^6, m_k = min over primes in ((k-1)e6,k e6] of 2T(p)-pi(p). **sha256 985f8d879d07621722caa482a10599d8fce1f1c05ce894cd3da39b310ef9f1c9**. Rows: 10^6: 44705 78498 0 (m_1=0 from p=7); 10^7: 394240 664579 110641; 10^8: 3558181 5761455 1341048; 10^9: 32608999 50847534 14355343.
- `blocks.raw`, `merge.out`, `brute.out`, `eq_block1.txt`, `min_block2.txt`.

## n <= 1000 with 2T(n)-pi(n) <= 2 (all n, from brute.py)
(n:margin) 1:2, 3:2, 4:2, 5:1, 6:1, 7:0, 8:2, 53:2, 54:2, 55:2, 71:2, 79:2.

## Not established
Only that the two programs agree is evidence of [C]; I have not seen the other one. Both T and pi in `blocks.c` share the PARI-checked prime count only at checkpoints, not at intermediate n (intermediate pi comes from tau==2). Trial-division small primes up to 31700 assumed complete (sqrt(10^9)=31622.8).
