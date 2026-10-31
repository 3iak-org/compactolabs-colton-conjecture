# verify/rs62 - blind second implementation (check-rs62)

Written from the definitions in the brief only; `search/`, `results/` and the other
side's files were not read.

## Reproduce (one command, ~3 min)

    cd verify/rs62 && ./run.sh

(`run.sh` builds `gen.c`, `rs62.c`, runs `moments.py` with the venv python, writes the three outputs.)

## Method

* **Generators** (`gen.c`): own linear-sieve smallest-prime-factor table up to 28653696; every
  even a is factorised from the table, tau(a) = prod(e_i+1), test `a % (2*tau) == 0`.
  No divisor-count sieve. N(28653696) = 413980; sha256 is over the text "a g\n" per generator.
* **pi(g)**: PARI `primepi` through cypari2.
* **Moments** (`moments.py`): gmpy2/MPFR, 200 bits. For the lower sum every operation
  (ln a, each multiplication building (ln a)^k, each division by a, each addition) is performed
  with rounding toward -inf; for the upper sum toward +inf. All operands are positive
  (a >= 2 so ln a > 0), so each operation is monotone and the directed result is a rigorous
  bound on the exact value, by induction. MPFR's log is correctly rounded in each mode.
  Endpoints are converted to exact rationals and floored/ceiled at 32 significant digits
  (no float formatting). Width of [lo,hi] before output rounding is ~1e-55 relative.
* **rs62-lower** (`rs62.c`): sieve of Atkin to 1e9 (flat bit array, quadratic-form toggles 4x^2+y^2, 3x^2+y^2, 3x^2-y^2 by residue mod 12, then removal of multiples of squares of the Atkin primes themselves; no Eratosthenes; pi(1e9) = 50847534 printed to stderr,
  matches the known value). EVERY interval [q,q') (q prime, 59 <= q <= 1e9, last one ending at 1e9) is evaluated in
  MPFR at 128 bits with directed rounding, no prefilter: L = ln q' rounded down, q'/L and q'/(2L^2) rounded up, sum rounded up,
  slack = pi(q) - that, rounded down. All operands positive so each directed operation is monotone and the computed slack is a
  lower bound of the exact pi(q) - f(q'). Since f is increasing on x >= 59, slack > 0 gives pi(x) > f(x) on all of [q,q').
  Block minima are the minima of those lower bounds (strict <, first minimiser kept); printed `%.6R*f` with RNDD.
  The last interval uses f(1e9), printed `nextprime` = 1000000000 (not a prime, a marker). The file carries
  `INTERVALS 50847518` (= pi(1e9) - pi(58)) just before PASS/FAIL; FAIL names the first q with computed slack <= 0.
  (Earlier version cleared non-minimal intervals by a long-double test; that is gone. The eight block lines are unchanged.)
  Wall time ~2m20s single core.

## Self-test against findings/colton-threshold.md section 4 (run after commit)

Compared (no code changed afterwards) on M = 28653696: N = 413980, maxG = 28653696,
beta = 3348506095 all agree; L0..L4 agree with the table to every digit printed there
(30-33 significant digits), and each of my [lo,hi] enclosures contains the printed values.
