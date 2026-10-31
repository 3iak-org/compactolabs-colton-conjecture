#!/usr/bin/env python
"""usage: rs62_lower.py raw.txt out.txt. Wraps the output of rs62lower.c (every interval evaluated in Arb) into results/rs62/rs62-lower.txt."""
import sys, datetime, platform, subprocess
raw = open(sys.argv[1]).read().split("\n")
raw = [l for l in raw if l]
meta = open(sys.argv[3]).read().strip() if len(sys.argv) > 3 else ""
with open(sys.argv[2], "w") as fh:
    fh.write("# RS62 (3.1) pi(x) > f(x) on [59,1e9]; slack(q)=pi(q)-f(q'), last interval f(1e9). Implementation 1 (comp-rs62)\n")
    fh.write("# method: segmented Eratosthenes; EVERY interval [q,q') evaluated with Arb 128-bit balls (rs62lower.c), lower endpoint of pi(q)-f(q') must be >0;\n")
    fh.write("# min slack = block minimum of that lower endpoint, rounded down to 6 places\n")
    fh.write(f"# date {datetime.date.today()} host {platform.node()} cmd: search/rs62/run.sh\n")
    if meta: fh.write(f"# {meta}\n")
    fh.write("# columns: block_lo block_hi min_slack argmin_q nextprime\n")
    for l in raw:
        p = l.split()
        if len(p) == 5 and p[4] == "1000000000": p[4] = "(1e9)"
        if len(p) == 5 and p[4] == "0": p[4] = "(1e9)"
        fh.write(" ".join(p) + "\n")
