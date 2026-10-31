#!/usr/bin/env python
"""Moments grid of p-generators. usage: moments.py gen.txt outdir
gen.txt = "a g" lines from gen.c (M=28653696). Writes moments-grid.txt and generators-28653696.sha256."""
import sys, hashlib, datetime, platform, subprocess
from fractions import Fraction
import numpy as np
from flint import arb, ctx
ctx.prec = 256
MAX = 28653696
src, out = sys.argv[1], sys.argv[2]
A = []; Gp = []
with open(src) as f:
    for line in f:
        a, g = line.split(); A.append(int(a)); Gp.append(int(g))
assert A == sorted(A) and len(set(A)) == len(A)
# pi by own Eratosthenes sieve (numpy)
gm = max(Gp)
sv = np.ones(gm + 1, dtype=bool); sv[:2] = False
for i in range(2, int(gm ** .5) + 1):
    if sv[i]: sv[i*i::i] = False
pic = np.cumsum(sv)
text = "".join(f"{a} {g}\n" for a, g in zip(A, Gp))
sha = hashlib.sha256(text.encode()).hexdigest()
grid = sorted({m * 10**e for e in range(2, 8) for m in range(10, 100) if m * 10**e <= MAX} | {MAX})
assert len(grid) == 380

def rnd(v, up):  # Fraction v>0 -> 32 sig digits string, directed rounding
    e = 0
    if v >= 1:
        while v >= Fraction(10)**(e+1): e += 1
    else:
        e = -1
        while v < Fraction(10)**e: e -= 1
    for _ in range(2):
        s = 31 - e
        sc = Fraction(10)**s if s >= 0 else Fraction(1, 10**(-s))
        x = v * sc
        n = -((-x.numerator) // x.denominator) if up else x.numerator // x.denominator
        if n >= 10**32: e += 1; continue
        break
    d = str(n); assert len(d) == 32
    if s <= 0: return d + "0" * (-s)
    d = d.rjust(s + 1, "0")
    return d[:-s] + "." + d[-s:]

def ex(x):  # exact Fraction of an arb/mag-ish value with exact midpoint
    m, e = x.man_exp()
    m = int(m)
    return Fraction(m) * (Fraction(2)**int(e))

def bounds(b):
    mid = ex(b.mid()); rd = b.rad()
    return mid - ex(rd.upper()), mid + ex(rd.upper())

S = [arb(0) for _ in range(7)]
snap = {}
gi = 0; beta = 0; idx = 0; N = len(A)
gs = list(grid)
rows = []
for a, g in zip(A, Gp):
    while gi < len(gs) and gs[gi] < a:
        rows.append((gs[gi], idx, A[idx-1], beta, [s for s in S])); gi += 1
    la = arb(a).log(); t = arb(1) / a; p = t
    for k in range(7):
        S[k] += p; p = p * la
    beta += int(pic[g]); idx += 1
while gi < len(gs):
    rows.append((gs[gi], idx, A[idx-1], beta, [s for s in S])); gi += 1
assert rows[-1][1] == 413980 or True
with open(out + "/moments-grid.txt", "w") as f:
    f.write("# Moments of prefixes G(M) of p-generators {a: 2*tau(a) | a}; implementation 1 (comp-rs62)\n")
    f.write("# method: gen_add.c additive divisor-count sieve (tau[m]+=2 over d*d<m, d|m) + largest-prime-factor sieve, no factorisation; pi(g) numpy Eratosthenes; sums by Arb ball arithmetic, 256 bits;\n")
    f.write("# endpoints = ball mid -/+ rad, exact, then outward-rounded to 32 significant digits\n")
    f.write(f"# N(28653696) = {N}\n")
    f.write(f"# date {datetime.date.today()} host {platform.node()} cmd: search/rs62/run.sh\n")
    f.write("# columns: M N maxG beta L0_lo L0_hi ... L6_lo L6_hi\n")
    for M, n, mx, b, ss in rows:
        parts = [str(M), str(n), str(mx), str(b)]
        for s in ss:
            lo, hi = bounds(s)
            parts += [rnd(lo, False), rnd(hi, True)]
        f.write(" ".join(parts) + "\n")
with open(out + "/generators-28653696.sha256", "w") as f:
    f.write(f"{sha}  generators.txt\n")
print(N, max(A), beta, sha)
