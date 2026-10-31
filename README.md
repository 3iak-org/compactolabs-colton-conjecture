# Colton's conjecture (OEIS A111291): π(n) ≤ 2T(n) for every n

This repository holds a complete, checkable proof that

    π(n) ≤ 2T(n)   for every integer n ≥ 0,

where T(n) counts the k ≤ n with τ(k) | k (refactorable numbers) and τ is the number of divisors.
Equality holds exactly at n = 0 and n = 7.

**The full story, with the proof written out in KaTeX, is the lab-notebook entry:
https://labs.compacto.land/results/colton-conjecture/**

## Prior work: this is not a first proof

- **Zelinsky** (J. Integer Seq. 5 (2002), Theorem 22) proved the inequality for n > 7.42·10¹³,
  using numbers from an unpublished program.
- **McCranie**, in a comment on OEIS **A323326** (2019), says a computation to 7.44·10¹³ completes
  the proof. That claim has not been refereed, and no code for it is published.

What is here is an independent version that anyone can rerun, and that does not depend on Theorem
22's unpublished numbers:

- **Zelinsky's argument, re-derived with explicit constants.** Two routes lower its threshold:
  - **from 10⁹, using only Rosser–Schoenfeld 1962**: T(n) − π(n)/2 ≥ 917,294 for every n ≥ 10⁹
    (`findings/colton-threshold-rs62.md`);
  - **from 10⁷, using Dusart's (6.5)**, as read in arXiv:1002.0442v1:
    T(n) − π(n)/2 ≥ 3616 for every n ≥ 10⁷ (`findings/colton-threshold.md`).
- **An exact check of every 1 ≤ n ≤ 10⁹.** Several implementations, using different methods, give
  a byte-identical 1000-line checkpoint file. Its sha256 is
  `985f8d879d07621722caa482a10599d8fce1f1c05ce894cd3da39b310ef9f1c9`.

An AI referee chat that the team could not brief accepted each part, and an AI adversary chat found
no counterexample. Neither is human peer review. Nothing here is formalised in Lean.

Neither lowered threshold was found in prior work as of 2026-10-31. The search was incomplete, so
they are not claimed as new. Only the π form is claimed; Colton's x/(2 log x) sentence is a
different statement.

## What is in each folder

| Folder | What it holds |
|---|---|
| `findings/` | `colton-conjecture.md` is the whole statement, the finite range and the seam. `colton-threshold-rs62.md` and `colton-threshold.md` are the two threshold proofs. Alongside them are, for each route: the input builder, the computed inputs (`*-inputs.json`, `*-inputs-verify.json`), and two checkers that share no code (exact rationals, and Arb balls). The `sanity` programs are not part of the proof. |
| `search/rs62/`, `results/rs62/` | RS62 route, implementation 1. An additive divisor-count sieve with Arb sums gives the 380-point moment grid. A segmented Eratosthenes with Arb checks RS62 (3.1) on all 50,847,518 prime-gap intervals in [59, 10⁹]. |
| `verify/rs62/` | RS62 route, implementation 2, written blind. Factorisation, PARI `primepi` and MPFR directed rounding for the grid; a sieve of Atkin with MPFR for (3.1). Its data lines match implementation 1 exactly. |
| `search/generators/`, `results/generators/`, `verify/generators/` | Dusart route: generator moments from a τ-sieve in C, and a blind exponent-signature enumeration in Python/PARI. |
| `search/range/`, `results/range/`, `verify/range/`, `verify/range2/` | The finite range 1 ≤ n ≤ 10⁹: three team implementations. Two use factorisation and were written blind to each other. The third is a blind additive divisor sieve. All produce the same checkpoint file. |
| `referee/` | The referee reports (threshold, range, RS62 threshold in three rounds), with the referee's own every-n and every-interval programs. |
| `adversary/` | The adversary reports, with their sieves. The RS62 report computes T(n) − π(n)/2 exactly at every n ∈ [10⁹, 10¹⁰]: the minimum is 7,185,230.5, at n = 1,000,000,021. |
| `literature/` | What was read, at what status, including the discovery of A323326. |

`PROVENANCE.md` lists every file with its path and sha256 in the source repository, at the pinned
commit.

## How to run the checks

You need Python 3, `python-flint` (0.9.0 was used) and a C compiler:

```sh
python -m venv .venv && .venv/bin/pip install python-flint==0.9.0

# Rebuild the inputs from the two implementations' files. Each builder asserts that they agree.
.venv/bin/python findings/colton-threshold-rs62-inputs-build.py
.venv/bin/python findings/colton-threshold-inputs-build.py

# The final inequalities: two checkers x two input files, for each route. All eight must exit 0.
for p in colton-threshold-rs62 colton-threshold; do
  for f in findings/$p-inputs.json findings/$p-inputs-verify.json; do
    .venv/bin/python findings/$p-check-rational.py $f
    .venv/bin/python findings/$p-check-arb.py $f
  done
done

# The finite range from scratch, by divisor enumeration (about 16 s on one core).
awk '/^```c$/{f=1;next} /^```$/{if(f)exit} f' findings/colton-conjecture.md > divenum.c
gcc -O2 -o divenum divenum.c && ./divenum 1000 > cp.txt
sha256sum cp.txt    # 985f8d879d07621722caa482a10599d8fce1f1c05ce894cd3da39b310ef9f1c9
```

Rerunning the heavier computations needs more:

- the RS62 implementations need FLINT, MPFR, GMP, PARI (cypari2) and gmpy2. See `search/rs62/run.sh`
  and `verify/rs62/README.md`.
- `verify/range2/r2.c` needs OpenMP: `gcc -O2 -fopenmp -o r2 r2.c`.

Each of them runs in minutes.

## What this does not claim

- It is not a first proof (see the prior work above), and neither lowered threshold is claimed as
  new.
- The cited prime bounds are not re-proved:
  - **Rosser–Schoenfeld 1962 Theorem 1** was read as a statement. Its proof was not checked. It is
    relied on only for (3.1) at x > 10⁹ and (3.2) at x ≥ 10⁹; below 10⁹, (3.1) is checked here.
  - **Dusart's (6.5)** was read in the arXiv preprint only. The published version (Ramanujan J.,
    2018) was not read.
- In each route, the two final-inequality checkers share no code, but the same author wrote both.
- Nothing above 10¹¹ was checked exhaustively.

The notebook entry has the complete list.
