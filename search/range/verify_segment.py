#!/usr/bin/env python3
"""Usage: verify_segment.py checkpoints.txt K   (1<=K<=1000)
Recomputes block ((K-1)e6, K*e6] from scratch with numpy and checks line K against line K-1."""
import sys, numpy as np
cp = {}
for k, l in enumerate(open(sys.argv[1]), 1):
    n, T, pi, mm = map(int, l.split()); cp[k] = (T, pi, mm, 0)
cp[0] = (0, 0, 0, 0)  # argmin is not in the file
K = int(sys.argv[2]); lo = (K-1)*10**6+1; hi = K*10**6
n = np.arange(lo, hi+1, dtype=np.int64)
rem = n.copy(); tau = np.ones(len(n), dtype=np.int64)
sieve = np.ones(int(hi**0.5)+2, dtype=bool); sieve[:2] = False
for i in range(2, int(len(sieve)**0.5)+1):
    if sieve[i]: sieve[i*i::i] = False
for p in np.nonzero(sieve)[0]:
    if p*p > hi: break
    idx = np.arange((-lo) % p, len(n), p)          # positions of multiples of p
    e = np.zeros(len(idx), dtype=np.int64)
    while True:                                     # strip p's, counting exponent
        m = rem[idx] % p == 0
        if not m.any(): break
        rem[idx[m]] //= p; e[m] += 1
    tau[idx] *= e + 1
tau[rem > 1] *= 2
isp = tau == 2; div = (n % tau == 0)
T0, P0 = cp[K-1][:2]
Tl = np.cumsum(div); Pl = np.cumsum(isp)
margin = 2*(T0+Tl) - (P0+Pl)
mn = margin[isp].min(); am = n[isp][margin[isp] == mn][0]
got = (T0+int(Tl[-1]), P0+int(Pl[-1]), int(mn), 0)
ok = got == cp[K]
print("block", K, "recomputed", got, "file", cp[K], "OK" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
