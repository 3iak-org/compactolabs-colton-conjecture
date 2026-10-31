#!/usr/bin/env python3
"""Colton threshold from 10^9 via Rosser-Schoenfeld 1962 - checker 1 of 2: EXACT RATIONALS.

Checks every finite hypothesis and inequality that findings/colton-threshold-rs62.md, section 4,
reduces "T(n) - pi(n)/2 >= s for every n >= 10^9" to, on one inputs file
(colton-threshold-rs62-inputs.json or -inputs-verify.json).

Method. Every number is a Python Fraction; no float enters any decision.
  - Each L_k enters as its outward-rounded LOWER endpoint L_lo[k], read as an exact decimal.
    That suffices because every coefficient c_m (eq. (3.3) of the findings file) is a
    nonnegative combination of the L_k plus a constant, and every quantity tested below is
    nondecreasing in every c_m (section 3, "Monotonicity in the inputs").
  - ln n (n a positive integer) is enclosed in a rational interval [lo, hi] by
        ln n = e ln 2 + ln y,   n = 2^e y,  1 <= y < 2,
        ln y = 2 atanh(z) = 2 sum_{j>=0} z^(2j+1)/(2j+1),   z = (y-1)/(y+1) in [0, 1/3),
    the partial sum to j < K being a lower bound and the partial sum plus
        2 z^(2K+1) / ((2K+1)(1 - z^2))
    an upper bound (the tail is dominated termwise by a geometric series of ratio z^2).
    ln 2 is the case y = 2, z = 1/3. Endpoints are then rounded outward to denominator 10^45.
  - Where ln enters with a positive power in a denominator, the UPPER end is used (it makes
    the quantity smaller, given the sign conditions checked first); where a lower bound on
    ln is needed (ln n_f >= J+1) the LOWER end is used.
Shares no code with checker 2 (colton-threshold-rs62-check-arb.py: Arb balls, Arb's log).

Run: ~/dev/projects/open-problems/.venv/bin/python \
         findings/colton-threshold-rs62-check-rational.py [inputs.json] [--tables]
Exit status 0 iff every hypothesis and every inequality holds. --tables also prints the
markdown tables of findings section 4 (every printed value truncated toward zero, so a printed
lower bound is still a lower bound when it is positive).
"""
import json
import os
import sys
from fractions import Fraction as Q

# ---- the cited inequality pair: Rosser-Schoenfeld 1962, Theorem 1 ----------------------------
# (3.1)  pi(x) > (x/ln x)(1 + ALPHA/ln x)  for real x >= X0
# (3.2)  pi(x) < (x/ln x)(1 + GAMMA/ln x)  for real x > 1
ALPHA = Q(1, 2)
X0 = 59
GAMMA = Q(3, 2)

J = 6                                   # moments L_0..L_6
START = 10 ** 9                         # the theorem is for n >= START
# Lemma P pieces: (generator set M, p, q); Lemma Q tail: (M, n_f)
PIECES = [
    (110000, 10 ** 9, 10 ** 10),
    (160000, 10 ** 10, 10 ** 11),
    (210000, 10 ** 11, 10 ** 12),
]
TAIL = (28653696, 10 ** 12)

DEN = 10 ** 45


def _atanh2(z, terms):
    """(lower, upper) for 2*atanh(z), 0 <= z < 1 rational."""
    s = Q(0)
    zz = z * z
    pw = z
    for j in range(terms):
        s += pw / (2 * j + 1)
        pw *= zz
    rem = 2 * pw / ((2 * terms + 1) * (1 - zz))     # pw = z^(2*terms+1) here
    return 2 * s, 2 * s + rem


def ln_interval(n):
    """Rational lo <= ln n <= hi for an integer n >= 1, width < 1e-40."""
    assert isinstance(n, int) and n >= 1
    e = n.bit_length() - 1
    y = Q(n, 2 ** e)
    assert 1 <= y < 2
    l2lo, l2hi = _atanh2(Q(1, 3), 50)               # (1/9)^50 < 1e-47
    ylo, yhi = _atanh2((y - 1) / (y + 1), 50)
    lo = e * l2lo + ylo
    hi = e * l2hi + yhi
    lo = Q((lo.numerator * DEN) // lo.denominator, DEN)
    hi = Q(-((-hi.numerator * DEN) // hi.denominator), DEN)
    assert hi - lo < Q(1, 10 ** 40)
    return lo, hi


def coefficients(L):
    """c_0..c_J of g_S(u) = sum_m c_m u^-m  (findings file, eq. (3.3))."""
    c = [L[0] - Q(1, 2), L[1] + ALPHA * L[0] - GAMMA / 2]
    for m in range(2, J + 1):
        c.append(L[m] + ALPHA * m * L[m - 1])
    return c


def g_S(c, u):
    return sum(cm / u ** m for m, cm in enumerate(c))


def show(x, d=6):
    """Decimal rendering for the log only (rounded toward zero); not used in any decision."""
    sign = "-" if x < 0 else ""
    x = abs(x)
    ip = x.numerator // x.denominator
    fp = ((x - ip) * 10 ** d).numerator // ((x - ip) * 10 ** d).denominator
    return f"{sign}{ip}.{fp:0{d}d}"


def sig(x, n, up=False):
    """x >= 0 truncated (toward zero) to n significant digits, as a plain decimal string;
    with up=True rounded UP instead (for printing upper bounds)."""
    assert x >= 0
    if x == 0:
        return "0"
    e = 0
    while x >= 10 ** (e + 1):
        e += 1
    while x < 10 ** e:
        e -= 1
    d = n - 1 - e                      # decimal places
    if d >= 0:
        y = x * 10 ** d
        v = -((-y.numerator) // y.denominator) if up else y.numerator // y.denominator
        t = str(v).rjust(d + 1, "0")
        return (t[:-d] + "." + t[-d:]) if d > 0 else t
    y = x / 10 ** (-d)
    v = -((-y.numerator) // y.denominator) if up else y.numerator // y.denominator
    return str(v * 10 ** (-d))


def tables(sets):
    rows_L, rows_c, rows_p = [], [], []
    for M, p, q in PIECES + [(TAIL[0], None, None)]:
        S = sets[str(M)]
        L = [Q(s) for s in S["L_lo"][: J + 1]]
        c = coefficients(L)
        rows_L.append(f"| G({M:,}) | " + " | ".join(sig(x, 30) for x in L) + " |")
        rows_c.append(f"| G({M:,}) | " + " | ".join(("−" + sig(-x, 10)) if x < 0 else sig(x, 10) for x in c) + " |")
        if p is not None:
            lp, lq = ln_interval(p)[1], ln_interval(q)[1]
            gq = g_S(c, lq)
            lhs = Q(p) / lp * gq
            rows_p.append(f"| G({M:,}) | [10^{len(str(p)) - 1}, 10^{len(str(q)) - 1}] | {sig(lp, 12, True)} | {sig(lq, 12, True)} | "
                          f"{sig(gq, 10)} | {sig(lhs, 12)} | {S['beta']:,} | **{sig(lhs - S['beta'], 10)}** | {sig(lhs / S['beta'], 4)} |")
    M, nf = TAIL
    S = sets[str(M)]
    c = coefficients([Q(s) for s in S["L_lo"][: J + 1]])
    hi = ln_interval(nf)[1]
    terms = [cm * nf / hi ** (m + 1) for m, cm in enumerate(c)]
    print("\nTABLE L (lower endpoints, 30 significant digits, truncated)")
    print("| S | L₀ | L₁ | L₂ | L₃ | L₄ | L₅ | L₆ |\n|---|---|---|---|---|---|---|---|")
    print("\n".join(rows_L))
    print("\nTABLE C (coefficients at the lower endpoints, 10 significant digits, truncated toward zero)")
    print("\n".join(rows_c))
    print("\nTABLE P")
    print("\n".join(rows_p))
    print("\nTABLE Q (terms c_m n_f/(ln n_f)^(m+1), ln n_f replaced by its upper bound)")
    print(f"ln n_f <= {sig(hi, 30, True)}")
    print("| term ≥ | " + " | ".join(sig(t, 8) for t in terms) + " |")
    print(f"sum >= {sig(sum(terms), 12)} ; beta = {S['beta']:,} ; surplus >= {sig(sum(terms) - S['beta'], 12)} ; "
          f"ratio >= {sig(sum(terms) / S['beta'], 4)}")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    args = [a for a in sys.argv[1:] if a != "--tables"]
    path = args[0] if args else os.path.join(here, "colton-threshold-rs62-inputs.json")
    inp = json.load(open(path))
    print("inputs:", path)
    print("status:", inp.get("_status", "?"), "| source sha256:", inp.get("_source_sha256", "?"))
    sets = inp["sets"]
    ok = True
    surpluses = []
    lowest_x = None

    def check(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  [{'ok' if cond else 'FAIL'}] {msg}")

    assert ALPHA >= 0   # needed by Proposition A (truncation is a lower bound) and by monotonicity

    # coverage: [START, p_1], [p_1, p_2], ..., [p_k, n_f], [n_f, inf)
    print("\nCoverage")
    ends = [p for _, p, _ in PIECES] + [TAIL[1]]
    check(PIECES[0][1] == START, f"first piece starts at {START}")
    check(all(PIECES[i][2] == ends[i + 1] for i in range(len(PIECES))), "pieces are contiguous and end at n_f")

    for M, p, q in PIECES:
        S = sets[str(M)]
        L = [Q(s) for s in S["L_lo"][: J + 1]]
        beta = Q(S["beta"])
        c = coefficients(L)
        print(f"\nLemma P, piece [{p}, {q}], S = G({M}): N = {S['N']}, max S = {S['maxG']}, beta = {S['beta']}")
        check(p < q, "p < q")
        check(p >= X0 * S["maxG"], f"(V) p >= 59 max S = {X0 * S['maxG']}")
        lnp_lo, lnp_hi = ln_interval(p)
        lnq_lo, lnq_hi = ln_interval(q)
        check(lnp_lo >= 1, "(E) ln p >= 1, i.e. p >= e")
        check(all(cm > 0 for cm in c[1:]), f"(D) c_1..c_{J} > 0   (c_0 = {show(c[0])}, c_1 >= {show(c[1])})")
        gq = g_S(c, lnq_hi)                 # <= g_S(ln q) since g_S is nonincreasing
        check(gq >= 0, f"(G) g_S(ln q) >= {show(gq, 9)} >= 0")
        lhs = Q(p) / lnp_hi * gq            # <= (p/ln p) g_S(ln q)
        s = lhs - beta
        check(s >= 0, f"(I) (p/ln p) g_S(ln q) - beta >= {show(s, 3)}   (ratio to beta >= {show(lhs / beta, 4)})")
        surpluses.append(s)
        x = Q(p, S["maxG"])
        lowest_x = x if lowest_x is None else min(lowest_x, x)

    M, nf = TAIL
    S = sets[str(M)]
    L = [Q(s) for s in S["L_lo"][: J + 1]]
    beta = Q(S["beta"])
    c = coefficients(L)
    print(f"\nLemma Q, tail [{nf}, inf), S = G({M}): N = {S['N']}, max S = {S['maxG']}, beta = {S['beta']}")
    check(nf >= X0 * S["maxG"], f"(V) n_f >= 59 max S = {X0 * S['maxG']}")
    lo, hi = ln_interval(nf)
    check(lo >= J + 1, f"(E) ln n_f >= J + 1 = {J + 1}   (ln n_f >= {show(lo)})")
    check(all(cm >= 0 for cm in c), f"(N) c_0..c_{J} >= 0   (c_0 = L_0 - 1/2 >= {show(c[0], 12)})")
    terms = [cm * nf / hi ** (m + 1) for m, cm in enumerate(c)]
    s = sum(terms) - beta
    check(s >= 0, f"(I) sum_m c_m n_f/(ln n_f)^(m+1) - beta >= {show(s, 1)}   (ratio >= {show(sum(terms) / beta, 4)})")
    surpluses.append(s)
    lowest_x = min(lowest_x, Q(nf, S["maxG"]))

    smin = min(surpluses)
    print(f"\nminimum surplus over all pieces and the tail >= {show(smin, 3)}")
    print(f"(3.1) is applied at x = n/a >= {show(lowest_x, 3)} (min over stages of p / max S); "
          f"(3.2) at x = n >= {START}")
    if "--tables" in sys.argv:
        tables(sets)
    print("\nALL HYPOTHESES AND INEQUALITIES HOLD" if ok else "\nSOMETHING FAILS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
