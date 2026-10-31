#!/usr/bin/env python3
"""findings/colton-threshold.md sections 1-2: SANITY ONLY, not an input to the Theorem.
(thm22, 2026-10-30.) Usage: python colton-threshold-sanity-zelinsky.py g286.bin
where g286.bin is the output of `colton-threshold-sanity-gen 28653696 g286.bin`."""
import sys
import numpy as np
import mpmath as mp
from sympy import primepi, primerange, primenu, divisor_count as tau

M, N = 28653696, 413980
G = lambda m: m * (m + 1) // 2
P = {c: int(primepi(M // c)) for c in (36, 80, 96, 128)}
Pn = {c: int(primepi(N // c)) for c in (36, 80, 96, 128)}
print("B formula as printed (413980 in the pi arguments):",
      G(Pn[36]) + G(Pn[80]) + G(Pn[96]) + (N - Pn[36] - Pn[80] - Pn[96]) - Pn[128])
print("reading: M in the pi arguments, last '-' as 'x':",
      G(P[36]) + G(P[80]) + G(P[96]) + (N - P[36] - P[80] - P[96]) * P[128], " (Zelinsky states 8694520815)")
print("c < 128 with 4 tau(c) | c:", [c for c in range(1, 128) if c % (4 * tau(c)) == 0])

mp.mp.dps = 40
def F(n, A, B):
    L = mp.log(n)
    return A * (n / L) * (1 + mp.mpf('0.992') / L) - B - mp.mpf('0.5') * (n / L) * (1 + mp.mpf('1.2762') / L)
for B in (8694520815, 3348920075):
    r = mp.findroot(lambda x: F(mp.e ** x, mp.mpf('0.508'), B), 31.5)
    print(f"A=.508 B={B}: crossing n = {mp.nstr(mp.e ** r, 10)}; F(7.42e13) = {mp.nstr(F(mp.mpf('7.42e13'), mp.mpf('0.508'), B), 8)}")

k, n = 180, 1024
c = [k * p for p in primerange(2, n // k + 1) if (k * p) % tau(k * p) == 0]
print(f"Lemma 19 printed: k=180 in G {k % (2 * tau(k)) == 0}; tau numbers 180p <= 1024: {c}; "
      f"printed bound pi(n/k)-omega(n) = {int(primepi(n // k)) - int(primenu(n))}")

bad = 0
for a in range(1, 3001):
    gen = a % (2 * tau(a)) == 0
    allp = all((a * p) % tau(a * p) == 0 for p in primerange(2, 5000) if a % p)
    bad += gen != allp
print("Lemma 18 brute force a <= 3000, p < 5000: mismatches", bad)

d = np.fromfile(sys.argv[1], dtype=np.uint64).reshape(-1, 2)
acc, first = mp.mpf(0), None
for a in d[:, 0]:
    acc += mp.mpf(1) / int(a)
    if first is None and acc > mp.mpf('0.508'):
        first = int(a)
print("count", len(d), "; A first exceeds .508 at generator", first, "; A(G(M)) =", mp.nstr(acc, 25))
