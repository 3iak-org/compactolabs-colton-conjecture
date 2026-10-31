#!/usr/bin/env python3
"""Colton threshold, checker 1 of 2: EXACT RATIONAL ARITHMETIC.

Verifies the finitely many inequalities that findings/colton-threshold.md
reduces "pi(n) <= 2 T(n) for every n >= 10^7" to, given the named computed
inputs in colton-threshold-inputs.json.

Method: every quantity is a Python Fraction. The only transcendental
quantity is ln n at the piece endpoints n; for each one we choose a rational
r and PROVE r >= ln n by showing that a Taylor partial sum of e^r (all terms
positive, so a lower bound for e^r) is already >= n. No floating point enters
any decision. Shares no code with checker 2 (colton-threshold-check-arb.py,
which uses Arb ball arithmetic and Arb's own logarithm).

Run: ~/dev/projects/open-problems/.venv/bin/python \
         findings/colton-threshold-check-rational.py [inputs.json]
(default inputs: colton-threshold-inputs.json = comp-generators; also run it on
colton-threshold-inputs-verify.json = check-generators.)
Exit status 0 iff every inequality holds.
"""
import json
import sys
from fractions import Fraction as F
from decimal import Decimal, getcontext
import os

J = 4                     # moment order used in the theorem (L_0..L_4)
DUSART_LOWER_X0 = 599     # Dusart 2010 (6.5): pi(x) >= x/ln x (1 + 1/ln x), x >= 599
DUSART_UPPER_C = F(12762, 10000)   # pi(x) <= x/ln x (1 + 1.2762/ln x), x > 1

# Stages: (generator set G(M), list of piece endpoints n_0 < n_1 < ... ).
# Piece [n_i, n_{i+1}] is certified by Lemma P (findings file, section 4).
STAGES = [
    ("16694",  [10**7, 3 * 10**7, 10**8]),
    ("166944", [10**8, 10**9, 10**12]),
]
FINAL = ("28653696", 10**12)   # Lemma Q: certifies [n_f, infinity)


def dec_to_frac(s):
    getcontext().prec = 100
    return F(Decimal(s))


def exp_lower(x, need):
    """Return True iff a Taylor partial sum of e^x (x > 0 rational) reaches `need`.
    Every partial sum is a lower bound for e^x, so True proves e^x >= need."""
    assert x > 0
    term = F(1)
    s = F(1)
    for k in range(1, 2000):
        term = term * x / k
        s += term
        if s >= need:
            return True
    return False


def ln_upper(n):
    """Rational r with r >= ln n, certified by exp_lower(r, n)."""
    getcontext().prec = 60
    guess = Decimal(n).ln()
    r = F(guess) + F(1, 10**30)
    r = F(int(r * 10**30) + 1, 10**30)
    assert exp_lower(r, n), "could not certify ln upper bound"
    return r


def coeffs(L):
    """c_0..c_J of g_S(u) = sum_m c_m u^-m (findings/colton-threshold.md, eq. (3.2))."""
    c = [L[0] - F(1, 2), L[1] + L[0] - DUSART_UPPER_C / 2]
    for m in range(2, J + 1):
        c.append(L[m] + m * L[m - 1])
    return c


def g_at(c, u):
    return sum(cm / u**m for m, cm in enumerate(c))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "colton-threshold-inputs.json")
    inp = json.load(open(path))
    print("inputs:", path)
    print("status:", inp.get("_status", "?"))
    ok_all = True

    def lower_L(S):
        # lower endpoint of the rigorous enclosure [L_k - L_rad_k, L_k + L_rad_k];
        # every coefficient c_m is increasing in every L_k, so the lower endpoint is what is needed
        return [dec_to_frac(x) - dec_to_frac(r) for x, r in zip(S["L"][: J + 1], S["L_rad"][: J + 1])]

    for M, pts in STAGES:
        S = inp["sets"][M]
        L = lower_L(S)
        beta = F(S["beta"])
        c = coeffs(L)
        print(f"\nStage G({M}): N={S['N']} beta={S['beta']} max a={S['maxa']}")
        # (V) validity of Dusart's lower bound at x = n/a for every a in S, n >= n_0
        v = pts[0] >= DUSART_LOWER_X0 * S["maxa"]
        print(f"  (V) n_0 = {pts[0]} >= 599 * max a = {DUSART_LOWER_X0 * S['maxa']}: {v}")
        # (D) g_S decreasing: c_m >= 0 for m >= 1
        d = all(cm > 0 for cm in c[1:])
        print(f"  (D) c_1..c_{J} > 0: {d}   (c_0 = {float(c[0]):.6f})")
        ok_all &= v and d
        for p, q in zip(pts, pts[1:]):
            lp, lq = ln_upper(p), ln_upper(q)
            gq = g_at(c, lq)
            lhs = F(p) / lp * gq
            good = gq >= 0 and lhs >= beta
            ok_all &= good
            print(f"  piece [{p:.3e}, {q:.3e}]: g_S(ln q) >= {float(gq):.6e} ; "
                  f"(p/ln p) g_S(ln q) >= {float(lhs):.6e} vs beta = {S['beta']} ; "
                  f"ratio {float(lhs / beta):.4f} ; {'OK' if good else 'FAIL'}")

    M, nf = FINAL
    S = inp["sets"][M]
    L = lower_L(S)
    beta = F(S["beta"])
    c = coeffs(L)
    print(f"\nFinal stage G({M}): N={S['N']} beta={S['beta']} max a={S['maxa']}")
    v = nf >= DUSART_LOWER_X0 * S["maxa"]
    nonneg = all(cm >= 0 for cm in c)
    lf = ln_upper(nf)
    big = nf >= 3 ** (J + 1)   # e < 3, so e^(J+1) < 3^(J+1) <= n_f, i.e. ln n_f >= J+1
    lhs = sum(cm * F(nf) / lf ** (m + 1) for m, cm in enumerate(c))
    good = v and nonneg and big and lhs >= beta
    ok_all &= good
    print(f"  (V) n_f = {nf} >= 599 * max a = {DUSART_LOWER_X0 * S['maxa']}: {v}")
    print(f"  (N) c_0..c_{J} >= 0: {nonneg}   (c_0 = L_0 - 1/2 >= {float(c[0]):.10f})")
    print(f"  (I) sum_m c_m n_f/(ln n_f)^(m+1) >= {float(lhs):.6e} vs beta = {S['beta']} ; "
          f"ratio {float(lhs / beta):.4f} ; {'OK' if good else 'FAIL'}")

    print("\nALL INEQUALITIES HOLD" if ok_all else "\nSOME INEQUALITY FAILS")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
