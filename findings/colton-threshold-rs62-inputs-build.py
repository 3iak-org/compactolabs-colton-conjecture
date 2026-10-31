#!/usr/bin/env python3
"""Build the inputs of findings/colton-threshold-rs62.md from the two [C] moment grids.

Reads
    results/rs62/moments-grid.txt   (implementation 1, comp-rs62)
    verify/rs62/moments-grid.txt    (implementation 2, check-rs62)
in the shared format (lines 'M N maxG beta L0_lo L0_hi ... L6_lo L6_hi', '#' comments ignored)
and writes, one file per implementation,
    findings/colton-threshold-rs62-inputs.json         (from implementation 1)
    findings/colton-threshold-rs62-inputs-verify.json  (from implementation 2)
holding the four stage sets the proof uses, with the lo/hi strings copied VERBATIM.

It refuses (exit 1) unless:
  - each file has exactly the 380 grid values of M, ascending, as defined in the brief;
  - every lo/hi is a plain decimal with exactly 32 significant digits and lo <= hi;
  - the two files agree exactly on M, N, maxG, beta, and their [lo, hi] enclosures overlap
    for every M and k (two rigorous enclosures of one number must intersect);
  - within each file N, beta and every L_k are nondecreasing in M (they are sums of
    nonnegative terms over nested sets; a decrease would mean a broken file);
  - for M = 28653696, N, maxG and beta equal the refereed [C] values in
    findings/colton-threshold-inputs.json, and each L_k enclosure overlaps that file's
    enclosure [L - L_rad, L + L_rad] (a cross-check against the earlier, independently
    refereed computation; not an input to the proof).

Run from the repo root:
    ~/dev/projects/open-problems/.venv/bin/python findings/colton-threshold-rs62-inputs-build.py \
        [grid1] [grid2]
"""
import hashlib
import json
import os
import re
import sys
from fractions import Fraction

USED = [110000, 160000, 210000, 28653696]   # the stage sets of findings/colton-threshold-rs62.md section 4
K = 7                                        # L_0..L_6
DEC = re.compile(r"^[0-9]+\.[0-9]+$|^[0-9]+$")


def grid_values():
    vals = {m * 10 ** e for e in range(2, 9) for m in range(10, 100) if m * 10 ** e <= 28653696}
    vals.add(28653696)
    return sorted(vals)


def sig_digits(s):
    d = s.replace(".", "").lstrip("0")
    return len(d)


def parse(path):
    rows = {}
    order = []
    with open(path) as fh:
        text = fh.read()
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split(" ")
        if len(f) != 4 + 2 * K:
            sys.exit(f"{path}: bad field count in line: {line[:60]}")
        M, N, maxG, beta = (int(x) for x in f[:4])
        lo = f[4::2]
        hi = f[5::2]
        for s in lo + hi:
            if not DEC.match(s) or sig_digits(s) != 32:
                sys.exit(f"{path}: M={M}: not a 32-significant-digit plain decimal: {s}")
        for a, b in zip(lo, hi):
            if Fraction(a) > Fraction(b):
                sys.exit(f"{path}: M={M}: lo > hi")
        rows[M] = dict(N=N, maxG=maxG, beta=beta, L_lo=lo, L_hi=hi)
        order.append(M)
    if order != grid_values():
        sys.exit(f"{path}: the M column is not exactly the 380 grid values in ascending order")
    prev = None
    for M in order:
        r = rows[M]
        if not (1 <= r["maxG"] <= M):
            sys.exit(f"{path}: M={M}: maxG out of range")
        if prev is not None:
            if r["N"] < prev["N"] or r["beta"] < prev["beta"]:
                sys.exit(f"{path}: M={M}: N or beta decreases")
            for k in range(K):
                if Fraction(r["L_hi"][k]) < Fraction(prev["L_lo"][k]):
                    sys.exit(f"{path}: M={M}: L_{k} decreases")
        prev = r
    return rows, hashlib.sha256(text.encode()).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    p1 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "results/rs62/moments-grid.txt")
    p2 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(root, "verify/rs62/moments-grid.txt")
    r1, h1 = parse(p1)
    r2, h2 = parse(p2)
    for M in grid_values():
        a, b = r1[M], r2[M]
        for key in ("N", "maxG", "beta"):
            if a[key] != b[key]:
                sys.exit(f"M={M}: {key} differs: {a[key]} vs {b[key]}")
        for k in range(K):
            if Fraction(a["L_hi"][k]) < Fraction(b["L_lo"][k]) or Fraction(b["L_hi"][k]) < Fraction(a["L_lo"][k]):
                sys.exit(f"M={M}: L_{k} enclosures do not overlap")
    print(f"grids agree: 380 values of M, integers equal, every L_k enclosure overlaps")

    # cross-check against the earlier refereed [C] computation at M = 28653696
    old = json.load(open(os.path.join(here, "colton-threshold-inputs.json")))["sets"]["28653696"]
    for r, name in ((r1, p1), (r2, p2)):
        x = r[28653696]
        assert (x["N"], x["maxG"], x["beta"]) == (old["N"], old["maxa"], old["beta"]), name
        for k in range(K):
            olo = Fraction(old["L"][k]) - Fraction(old["L_rad"][k])
            ohi = Fraction(old["L"][k]) + Fraction(old["L_rad"][k])
            assert not (Fraction(x["L_hi"][k]) < olo or ohi < Fraction(x["L_lo"][k])), (name, k)
    print("M = 28653696 agrees with findings/colton-threshold-inputs.json (N, maxG, beta; L_k overlap)")

    for r, src, h, out, impl in (
        (r1, p1, h1, "colton-threshold-rs62-inputs.json", "implementation 1 (comp-rs62, results/rs62/)"),
        (r2, p2, h2, "colton-threshold-rs62-inputs-verify.json", "implementation 2 (check-rs62, verify/rs62/)"),
    ):
        doc = {
            "_status": f"[C] inputs, {impl}",
            "_source": os.path.relpath(src, root),
            "_source_sha256": h,
            "_definitions": {
                "G(M)": "{1 <= a <= M : 2*tau(a) | a}",
                "g(a)": "largest prime factor of a",
                "L_k(M)": "sum_{a in G(M)} (ln a)^k / a, k = 0..6",
                "beta(M)": "sum_{a in G(M)} pi(g(a))",
                "L_lo, L_hi": "outward-rounded decimal endpoints: L_lo[k] <= L_k(M) <= L_hi[k] rigorously",
            },
            "sets": {str(M): r[M] for M in USED},
        }
        with open(os.path.join(here, out), "w") as fh:
            json.dump(doc, fh, indent=1)
            fh.write("\n")
        print(f"wrote findings/{out} from {os.path.relpath(src, root)} (sha256 {h[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
