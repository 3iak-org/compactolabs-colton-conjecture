#!/usr/bin/env python3
"""moments.py g1e9.txt : extra sums over G(M) for the threshold proof. Ball arithmetic (python-flint arb, 256 bits)."""
import sys
from collections import Counter
from flint import arb, ctx
ctx.prec = 256
rows = []
for l in open(sys.argv[1]):
    a, g, p = map(int, l.split())
    if a > 28653696: break
    rows.append((a, g, p))
def show(x):    # enclosure [lo, hi] and midpoint, 30 sig digits
    m, r = x.mid(), x.rad()
    lo, hi = m - r, m + r
    return f"mid={m.str(30, radius=False)} enclosure=[{lo.str(30, radius=False)}, {hi.str(30, radius=False)}] rad={r.str(3)}"
for M in (16694, 166944, 28653696):
    S = [r for r in rows if r[0] <= M]
    print(f"== M={M}")
    print("N =", len(S))
    L = [arb(0)] * 7
    for a, g, p in S:
        la = arb(a).log(); inv = arb(1) / arb(a); t = inv
        for k in range(7):
            L[k] += t; t = t * la
    for k in range(7): print(f"L_{k} {show(L[k])}")
    beta = sum(p for _, _, p in S)
    print("beta =", beta, " B =", beta + len(S))
    print("max G =", max(r[0] for r in S), " max a*g(a) =", max(r[0] * r[1] for r in S))
    if M == 28653696:
        C = Counter(a // g for a, g, p in S if 128 * g > M)
        print("cofactors a/g for g > M/128 (cofactor: count):", dict(sorted(C.items())), " total", sum(C.values()))
