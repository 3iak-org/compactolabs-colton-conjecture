"""moments-grid.txt and generators sha256 from the generator list "a g" (gen.c).
Usage: moments.py generators.txt outdir
Directed-rounding MPFR (gmpy2), 200 bits; pi(g) from PARI primepi (cypari2)."""
import sys, hashlib, datetime
import gmpy2
from gmpy2 import mpfr, mpq, mpz, RoundDown, RoundUp
import cypari2
PREC = 200
MMAX = 28653696
K = 7
grid = sorted({m * 10**e for m in range(10, 100) for e in range(2, 9) if m * 10**e <= MMAX} | {MMAX})
assert len(grid) == 380

def render(x, up):
    q = mpq(x)
    k = len(str(int(q))) - 1 if q >= 1 else -1
    if q < 1:
        k = 0
        while q * mpz(10)**(-k) < 1 if k <= 0 else False:
            k -= 1
    # normalise so that 10^k <= q < 10^(k+1)
    p10 = lambda n: mpq(10)**n
    while q < p10(k): k -= 1
    while q >= p10(k + 1): k += 1
    def scaled(kk):
        s = q * p10(31 - kk)
        n = int(gmpy2.f_div(s.numerator, s.denominator)) if not up else int(-gmpy2.f_div(-s.numerator, s.denominator))
        return n
    n = scaled(k)
    if n >= 10**32:
        k += 1; n = scaled(k)
    assert 10**31 <= n < 10**32
    d = str(n); sh = k - 31          # value = n * 10^sh
    if sh >= 0: return d + '0' * sh
    if -sh >= 32: return '0.' + '0' * (-sh - 32) + d
    return d[:sh] + '.' + d[sh:]

def main(gfile, outdir):
    pari = cypari2.Pari(); pari.allocatemem(10**9)
    lo = [mpfr(0, PREC) for _ in range(K)]
    hi = [mpfr(0, PREC) for _ in range(K)]
    beta = 0; N = 0; maxG = 0; gi = 0
    h = hashlib.sha256()
    rows = []
    pic = {}
    with open(gfile) as f:
        pending = [tuple(map(int, l.split())) for l in f]
    ctxd = gmpy2.context(precision=PREC, round=RoundDown)
    ctxu = gmpy2.context(precision=PREC, round=RoundUp)
    idx = 0
    for M in grid:
        while idx < len(pending) and pending[idx][0] <= M:
            a, g = pending[idx]; idx += 1
            h.update(f"{a} {g}\n".encode())
            if g not in pic: pic[g] = int(pari.primepi(g))
            beta += pic[g]; N += 1; maxG = a
            with gmpy2.local_context(ctxd):
                l = gmpy2.log(mpfr(a)); p = mpfr(1); A = mpfr(a)
                for k in range(K):
                    lo[k] = lo[k] + p / A
                    p = p * l
            with gmpy2.local_context(ctxu):
                l = gmpy2.log(mpfr(a)); p = mpfr(1); A = mpfr(a)
                for k in range(K):
                    hi[k] = hi[k] + p / A
                    p = p * l
        row = [M, N, maxG, beta]
        for k in range(K):
            row += [render(lo[k], False), render(hi[k], True)]
        rows.append(' '.join(map(str, row)))
    assert idx == len(pending)
    Nfin = N
    with open(outdir + '/moments-grid.txt', 'w') as o:
        o.write(f"# check-rs62 second implementation, {datetime.date.today()}\n")
        o.write("# generators: C, own linear-sieve smallest-prime-factor table, factorise each even a, tau from exponents, test a % (2 tau) == 0\n")
        o.write("# pi(g): PARI primepi via cypari2. Sums: gmpy2/MPFR, 200 bits, log and every op rounded toward -inf (lo) or +inf (hi);\n")
        o.write("# endpoints converted exactly to rationals then floor/ceil at 32 significant digits.\n")
        o.write(f"# N(28653696) = {Nfin}\n")
        o.write("# columns: M N maxG beta L0_lo L0_hi ... L6_lo L6_hi\n")
        o.write('\n'.join(rows) + '\n')
    with open(outdir + '/generators-28653696.sha256', 'w') as o:
        o.write(h.hexdigest() + "  generators\n" if False else h.hexdigest() + "  generators.txt\n")
main(*sys.argv[1:3])
