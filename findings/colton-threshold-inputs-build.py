#!/usr/bin/env python3
"""Build the checkers' input files from the two [C] implementations' moment files.

  results/generators/moments.txt  (comp-generators: tau sieve in C + Arb 300-bit sums)
      -> findings/colton-threshold-inputs.json
  verify/generators/moments.txt   (check-generators: signature DFS + PARI + Arb 256-bit sums)
      -> findings/colton-threshold-inputs-verify.json

Each L_k is stored as the printed decimal string together with an enclosure
radius `L_rad[k]` = (ball radius printed by that implementation) + (one unit
in the last printed decimal place). The printed decimal is a rounded or
truncated midpoint, not an outward-rounded endpoint, so the extra ulp is what
makes  [L_k - L_rad[k], L_k + L_rad[k]]  a rigorous enclosure of the true
value. The checkers use only the LOWER endpoint of that enclosure; every
coefficient of the bound is increasing in every L_k. N, beta, max G and
max a*g are exact integers, and must agree exactly between the two files.

Run from the repo root:
  ~/dev/projects/open-problems/.venv/bin/python findings/colton-threshold-inputs-build.py
"""
import json
import re
from decimal import Decimal

SETS = ("16694", "166944", "28653696")


def ulp(s):
    return Decimal(1).scaleb(-len(s.split(".")[1])) if "." in s else Decimal(1)


def parse_comp(path):
    txt = open(path).read()
    out = {}
    for blk in txt.split("\nM=")[1:]:
        M = blk.split("\n")[0].strip()
        geti = lambda key: int(re.search(r"^" + key + r"=(\d+)", blk, re.M).group(1))
        L, R = [], []
        for k in range(7):
            m = re.search(r"^L_%d = .*mid=([0-9.]+) rad<=([0-9.e+-]+)" % k, blk, re.M)
            L.append(m.group(1))
            R.append(str(Decimal(m.group(2)) + ulp(m.group(1))))
        out[M] = {"N": geti("N"), "L": L, "L_rad": R, "beta": geti("beta"), "B": geti("B"),
                  "maxa": geti("max_G"), "max_ag": geti("max_a_times_g")}
    return out


def parse_verify(path):
    txt = open(path).read()
    out = {}
    for blk in txt.split("== M=")[1:]:
        M = blk.split("\n")[0].strip()
        L, R = [], []
        for k in range(7):
            m = re.search(r"^L_%d mid=([0-9.]+) .*rad=\[([0-9.e+-]+) \+/- ([0-9.e+-]+)\]" % k, blk, re.M)
            L.append(m.group(1))
            R.append(str(Decimal(m.group(2)) + Decimal(m.group(3)) + ulp(m.group(1))))
        mb = re.search(r"beta = (\d+)\s+B = (\d+)", blk)
        mg = re.search(r"max G = (\d+)\s+max a\*g\(a\) = (\d+)", blk)
        out[M] = {"N": int(re.search(r"^N = (\d+)", blk, re.M).group(1)), "L": L, "L_rad": R,
                  "beta": int(mb.group(1)), "B": int(mb.group(2)),
                  "maxa": int(mg.group(1)), "max_ag": int(mg.group(2))}
    return out


DEFS = {
    "G(M)": "{a <= M : 2*tau(a) | a}",
    "g(a)": "largest prime factor of a",
    "L_k(M)": "sum_{a in G(M)} (ln a)^k / a",
    "beta(M)": "sum_{a in G(M)} pi(g(a))",
    "L_rad": "rigorous enclosure radius: true L_k lies in [L_k - L_rad_k, L_k + L_rad_k] (printed ball radius + one ulp of the printed decimal)",
}


def main():
    comp = parse_comp("results/generators/moments.txt")
    ver = parse_verify("verify/generators/moments.txt")
    for M in SETS:
        a, b = comp[M], ver[M]
        for key in ("N", "beta", "B", "maxa", "max_ag"):
            assert a[key] == b[key], (M, key, a[key], b[key])
        for k in range(7):
            lo_a, hi_a = Decimal(a["L"][k]) - Decimal(a["L_rad"][k]), Decimal(a["L"][k]) + Decimal(a["L_rad"][k])
            lo_b, hi_b = Decimal(b["L"][k]) - Decimal(b["L_rad"][k]), Decimal(b["L"][k]) + Decimal(b["L_rad"][k])
            assert max(lo_a, lo_b) <= min(hi_a, hi_b), ("enclosures disjoint", M, k)
        print(f"G({M}): integers agree exactly; L_0..L_6 enclosures overlap")
    json.dump({"_status": "[C] 2026-10-31: comp-generators, results/generators/moments.txt (lead-colton @ 1b20e41)",
               "_definitions": DEFS, "sets": {M: comp[M] for M in SETS}},
              open("findings/colton-threshold-inputs.json", "w"), indent=1)
    json.dump({"_status": "[C] 2026-10-31: check-generators, verify/generators/moments.txt (lead-colton @ 1b20e41)",
               "_definitions": DEFS, "sets": {M: ver[M] for M in SETS}},
              open("findings/colton-threshold-inputs-verify.json", "w"), indent=1)
    print("wrote findings/colton-threshold-inputs.json and findings/colton-threshold-inputs-verify.json")


if __name__ == "__main__":
    main()
