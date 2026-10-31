#!/usr/bin/env python3
"""Colton threshold, checker 2 of 2: ARB BALL ARITHMETIC (python-flint).

Independent of colton-threshold-check-rational.py: no shared code, and a
different method - every real number is an Arb ball (midpoint + rigorous
radius), logarithms come from Arb, and an inequality X >= Y is accepted only
if the ball X - Y lies entirely in [0, inf). The rational checker instead
uses exact Fractions and Taylor-certified upper bounds for ln.

What is checked (findings/colton-threshold.md, section 4): for each stage set
S = G(M), the lower bound

    T(n) - pi(n)/2 >= (n / ln n) * gS(ln n) - beta(S),
    gS(u) = (L0 - 1/2) + (L1 + L0 - 0.6381)/u + sum_{m=2..4} (Lm + m L(m-1))/u^m,

and Lemma P on each piece [p, q], Lemma Q on [n_f, inf).

Run: ~/dev/projects/open-problems/.venv/bin/python \
         findings/colton-threshold-check-arb.py [inputs.json]
Each L_k enters as the ball  printed value +/- L_rad_k  (the implementation's
own enclosure, widened by one ulp of the printed decimal).
"""
import json
import os
import sys

from flint import arb, ctx

ctx.prec = 256  # bits

PIECES = {
    "16694": [10**7, 3 * 10**7, 10**8],
    "166944": [10**8, 10**9, 10**12],
}
TAIL = ("28653696", 10**12)


def ball(decimal_string, radius_string):
    return arb(decimal_string) + arb(0, arb(radius_string))  # mid +/- rad


def nonneg(x):
    """True iff the ball x is certainly >= 0."""
    return x >= 0  # flint: comparison is True only if it holds for every point of the ball


def poly_g(Ls, u):
    L0, L1, L2, L3, L4 = Ls
    half = arb(1) / 2
    dus = arb("1.2762") / 2
    return ((L0 - half)
            + (L1 + L0 - dus) / u
            + (L2 + 2 * L1) / u**2
            + (L3 + 3 * L2) / u**3
            + (L4 + 4 * L3) / u**4)


def run(path):
    data = json.load(open(path))["sets"]
    verdicts = []
    for M, ends in PIECES.items():
        S = data[M]
        Ls = [ball(s, r) for s, r in zip(S["L"][:5], S["L_rad"][:5])]
        beta = arb(S["beta"])
        # coefficient positivity (g decreasing in u)
        dec = all(nonneg(c) for c in [Ls[1] + Ls[0] - arb("0.6381"), Ls[2] + 2 * Ls[1],
                                      Ls[3] + 3 * Ls[2], Ls[4] + 4 * Ls[3]])
        valid = ends[0] >= 599 * S["maxa"]
        verdicts += [dec, valid]
        print(f"G({M}): coefficients>0 {dec}; n0={ends[0]} >= 599*{S['maxa']} {valid}")
        for p, q in zip(ends[:-1], ends[1:]):
            gq = poly_g(Ls, arb(q).log())
            lhs = arb(p) / arb(p).log() * gq
            ok = nonneg(gq) and nonneg(lhs - beta)
            verdicts.append(ok)
            print(f"   [{p}, {q}]  (p/ln p) g(ln q) - beta = {(lhs - beta).str(8)}   {'OK' if ok else 'FAIL'}")
    M, nf = TAIL
    S = data[M]
    Ls = [ball(s, r) for s, r in zip(S["L"][:5], S["L_rad"][:5])]
    beta = arb(S["beta"])
    cs = [Ls[0] - arb(1) / 2, Ls[1] + Ls[0] - arb("0.6381"), Ls[2] + 2 * Ls[1],
          Ls[3] + 3 * Ls[2], Ls[4] + 4 * Ls[3]]
    allpos = all(nonneg(c) for c in cs)
    u = arb(nf).log()
    big = nonneg(u - 5)
    total = sum((c * arb(nf) / u ** (m + 1) for m, c in enumerate(cs)), arb(0))
    ok = allpos and big and nf >= 599 * S["maxa"] and nonneg(total - beta)
    verdicts.append(ok)
    print(f"G({M}) tail from {nf}: coefficients>=0 {allpos}; ln n_f >= 5 {big}; "
          f"sum c_m n/(ln n)^(m+1) - beta = {(total - beta).str(8)}   {'OK' if ok else 'FAIL'}")
    print("ALL HOLD" if all(verdicts) else "FAILURE")
    return 0 if all(verdicts) else 1


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "colton-threshold-inputs.json")))
