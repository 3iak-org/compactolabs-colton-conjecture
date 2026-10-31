#!/usr/bin/env python3
"""Colton threshold from 10^9 via Rosser-Schoenfeld 1962 - checker 2 of 2: ARB BALL ARITHMETIC.

Independent of colton-threshold-rs62-check-rational.py: no shared code and a different method.
Every real is an Arb ball (python-flint, 256 bits); logarithms are Arb's; a statement X >= 0 is
accepted only if the whole ball X lies in [0, inf) (flint's comparison is True only when it holds
for every point of the balls). Each L_k enters as the ball spanning its WHOLE enclosure
[L_lo, L_hi] (union of the two decimal endpoints, each itself converted to a ball), so this
checker does not lean on the monotonicity-in-L_k argument the rational checker uses.

Statements checked (findings/colton-threshold-rs62.md, section 4), J = 6,
    c_0 = L_0 - 1/2,  c_1 = L_1 + L_0/2 - 3/4,  c_m = L_m + (m/2) L_{m-1}  (2 <= m <= 6):
  Lemma P on each piece [p, q] with set S:  p >= 59 max S,  c_1..c_6 > 0,  g_S(ln q) >= 0,
      (p / ln p) g_S(ln q) - beta(S) >= 0;
  Lemma Q on [n_f, inf):  n_f >= 59 max S,  ln n_f >= 7,  c_0..c_6 >= 0,
      sum_m c_m n_f / (ln n_f)^(m+1) - beta(S) >= 0;
  and that the pieces tile [10^9, n_f].

Run: ~/dev/projects/open-problems/.venv/bin/python \
         findings/colton-threshold-rs62-check-arb.py [inputs.json]
"""
import json
import os
import sys

from flint import arb, ctx

ctx.prec = 256

STAGES = {          # set M -> piece endpoints for Lemma P
    "110000": (10 ** 9, 10 ** 10),
    "160000": (10 ** 10, 10 ** 11),
    "210000": (10 ** 11, 10 ** 12),
}
FINAL_SET, NF = "28653696", 10 ** 12
FROM = 10 ** 9
RS_A, RS_G, RS_X0 = arb(1) / 2, arb(3) / 2, 59     # RS62 (3.1) constant, (3.2) constant, (3.1) range
ORDER = 6


def enclosure(lo, hi):
    return arb(lo).union(arb(hi))


def cs(Ls):
    out = [Ls[0] - arb("0.5"), Ls[1] + RS_A * Ls[0] - RS_G / 2]
    out += [Ls[m] + RS_A * m * Ls[m - 1] for m in range(2, ORDER + 1)]
    return out


def evaluate(coef, u):
    acc = arb(0)
    for m in range(ORDER, -1, -1):      # Horner in 1/u
        acc = acc / u + coef[m]
    return acc


def run(path):
    data = json.load(open(path))
    sets = data["sets"]
    verdicts = []
    surplus = []

    def v(flag, text):
        verdicts.append(bool(flag))
        print(("   OK   " if flag else "   FAIL ") + text)

    pieces = sorted(STAGES.items(), key=lambda kv: kv[1][0])
    v(pieces[0][1][0] == FROM and pieces[-1][1][1] == NF
      and all(pieces[i][1][1] == pieces[i + 1][1][0] for i in range(len(pieces) - 1)),
      f"pieces tile [{FROM}, {NF}]")
    for M, (p, q) in pieces:
        S = sets[M]
        Ls = [enclosure(a, b) for a, b in zip(S["L_lo"][: ORDER + 1], S["L_hi"][: ORDER + 1])]
        coef = cs(Ls)
        print(f"G({M}) on [{p}, {q}]  beta={S['beta']}  maxS={S['maxG']}")
        v(p >= RS_X0 * S["maxG"], "p >= 59 maxS")
        v(arb(p).log() >= 1, "p >= e")
        v(all(x > 0 for x in coef[1:]), "c_1..c_6 > 0  (c_1 = %s)" % coef[1].str(10))
        gq = evaluate(coef, arb(q).log())
        v(gq >= 0, "g_S(ln q) = %s >= 0" % gq.str(10))
        d = arb(p) / arb(p).log() * gq - S["beta"]
        v(d >= 0, "(p/ln p) g_S(ln q) - beta = %s" % d.str(12))
        surplus.append(d)
    S = sets[FINAL_SET]
    Ls = [enclosure(a, b) for a, b in zip(S["L_lo"][: ORDER + 1], S["L_hi"][: ORDER + 1])]
    coef = cs(Ls)
    u = arb(NF).log()
    print(f"G({FINAL_SET}) on [{NF}, inf)  beta={S['beta']}  maxS={S['maxG']}")
    v(NF >= RS_X0 * S["maxG"], "n_f >= 59 maxS")
    v(u >= ORDER + 1, "ln n_f >= 7  (ln n_f = %s)" % u.str(10))
    v(all(x >= 0 for x in coef), "c_0..c_6 >= 0  (c_0 = %s)" % coef[0].str(12))
    tot = arb(0)
    for m in range(ORDER + 1):
        tot += coef[m] * arb(NF) / u ** (m + 1)
    d = tot - S["beta"]
    v(d >= 0, "sum c_m n_f/(ln n_f)^(m+1) - beta = %s" % d.str(12))
    surplus.append(d)
    low = min(s.lower() for s in surplus)
    print("smallest surplus lower bound: %s" % low.str(12))
    print("ALL HOLD" if all(verdicts) else "FAILURE")
    return 0 if all(verdicts) else 1


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "colton-threshold-rs62-inputs.json")))
