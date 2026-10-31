#!/usr/bin/env python3
"""Constructive enumeration of p-generators (2*tau(a) | a), a <= M.
No sieve over integers.  See README.md for the pruning proofs.
usage: gen.py M out.txt     (writes 'a g pi(g)' lines, ascending)
"""
import sys, itertools
from math import prod
import cypari2
from gmpy2 import iroot
pari = cypari2.Pari(); pari.allocatemem(2*10**9)

M = int(sys.argv[1]); OUT = sys.argv[2]
SP = [int(x) for x in pari('primes(20000)')]      # small primes; SP[i] has pi = i+1
SPSET = {p: i+1 for i, p in enumerate(SP)}
recs = []   # (a, g, pi_g)

def factor_small(n):          # n is tiny (2*tau), trial division
    out = {}; p = 2
    while n > 1:
        while n % p == 0: out[p] = out.get(p, 0) + 1; n //= p
        p += 1
    return out

# ---- step 1: signatures (non-increasing exponent tuples) with minimal value <= M
def signatures():
    out = []
    def rec(prefix, maxe, cost):
        i = len(prefix)
        if prefix: out.append(tuple(prefix))
        for e in range(1, maxe + 1):
            c = cost * SP[i] ** e
            if c > M: break
            rec(prefix + [e], e, c)
    rec([], 60, 1)
    return out

def emit(a, g, pg):
    recs.append((a, g, pg))

def run_signature(sig):
    T = prod(e + 1 for e in sig)
    forced = factor_small(2 * T)                       # D = 2T = prod p^d
    # need distinct slots with exponent >= d for each forced prime (greedy matching)
    need = sorted(forced.values(), reverse=True)
    if len(need) > len(sig) or any(n > s for n, s in zip(need, sig)): return
    fps = sorted(forced)

    def lb_rest(R, idx):          # min product of R (desc) on primes SP[idx], SP[idx+1], ...
        v = 1
        for j, e in enumerate(R): v *= SP[idx + j] ** e
        return v

    def rec(cur, lastidx, R):     # lastidx: index in SP of last used prime (-1 none); R sorted desc tuple
        lastp = SP[lastidx] if lastidx >= 0 else 0
        unmet = [p for p in fps if p > lastp]
        if len(unmet) > len(R): return
        for e in sorted(set(R), reverse=True):
            R2 = list(R); R2.remove(e); R2 = tuple(R2)
            if not R2:                                  # last slot
                if unmet:
                    if len(unmet) > 1: continue
                    q = unmet[0]
                    if e >= forced[q] and cur * q ** e <= M:
                        emit(cur * q ** e, q, SPSET[q])
                    continue
                if e == 1:
                    hi = M // cur
                    if hi <= lastp: continue
                    lst = pari.primes([lastp + 1, hi]) if hi > lastp else []
                    n = len(lst)
                    pil = lastidx + 1                    # pi(lastp)
                    assert int(pari.primepi(hi)) - pil == n    # counts the interval independently
                    for k in range(n):
                        q = int(lst[k]); emit(cur * q, q, pil + k + 1)
                else:
                    r = int(iroot(M // cur, e)[0])
                    for j in range(lastidx + 1, len(SP)):
                        q = SP[j]
                        if q > r: break
                        emit(cur * q ** e, q, j + 1)
                continue
            for j in range(lastidx + 1, len(SP)):
                q = SP[j]
                if unmet:
                    if q > unmet[0]: break
                    if q == unmet[0] and e < forced[q]: continue
                if cur * q ** e * lb_rest(R2, j + 1) > M: break
                rec(cur * q ** e, j, R2)
    rec(1, -1, sig)

sigs = signatures()
print("signatures:", len(sigs), file=sys.stderr)
for n, s in enumerate(sigs):
    run_signature(s)
recs.sort()
assert len({r[0] for r in recs}) == len(recs)
with open(OUT, "w") as f:
    for a, g, pg in recs: f.write(f"{a} {g} {pg}\n")
print("count", len(recs), file=sys.stderr)
