#!/bin/bash
# Reproduces moments-grid.txt, generators-28653696.sha256, rs62-lower.txt in this directory.
set -e
cd "$(dirname "$0")"
T=${TMPDIR:-/tmp}
PY=~/dev/projects/open-problems/.venv/bin/python
gcc -O2 -o $T/gen gen.c
gcc -O2 -o $T/rs62 rs62.c -lmpfr -lgmp -lm
nice -n 19 $T/gen 28653696 > $T/generators.txt
nice -n 19 $PY -W ignore moments.py $T/generators.txt .
nice -n 19 $T/rs62 > rs62-lower.txt
