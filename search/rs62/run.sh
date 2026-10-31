#!/bin/sh
# usage: search/rs62/run.sh   (from repo root). Generates results/rs62/{moments-grid.txt,generators-28653696.sha256}
set -e
T=${TMPDIR:-/tmp}; D=$(dirname "$0"); PY=~/dev/projects/open-problems/.venv/bin/python
gcc -O2 -o $T/rs62gen $D/gen_add.c
nice -n 19 $T/rs62gen 28653696 $T/rs62g.txt
nice -n 19 $PY $D/moments.py $T/rs62g.txt results/rs62
gcc -O2 -o $T/rs62lower $D/rs62lower.c -lflint -lmpfr -lgmp
S=$(date +%s); nice -n 19 $T/rs62lower > $T/rs62raw.txt; E=$(date +%s)
echo "base-commit $(git rev-parse --short HEAD) wall ${S:+$((E-S))}s" > $T/rs62meta.txt
nice -n 19 $PY $D/rs62_lower.py $T/rs62raw.txt results/rs62/rs62-lower.txt $T/rs62meta.txt
