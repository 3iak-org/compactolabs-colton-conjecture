#!/bin/bash
# usage: run_all.sh <binary> <outdir>   (6 parallel workers over blocks 1..1000)
B=$1; O=$2; mkdir -p $O
for w in 0 1 2 3 4 5; do
  # interleave-free contiguous ranges, sized by uniform cost
  a=$((1+w*167)); b=$((a+166)); [ $b -gt 1000 ] && b=1000
  nice -n 19 $B $a $b > $O/w$w.txt &
done; wait
