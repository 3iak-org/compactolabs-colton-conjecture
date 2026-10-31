/* adversary/colton-rs62/fsieve.c - SECOND implementation for the exact T(n), pi(n) blocks.
   Shares no code with xsieve.c and uses a different method:
   - tau(n) MULTIPLICATIVELY, from a segmented factor sieve: rem[i] starts at n; for each
     prime p <= sqrt(hi) and each multiple of p, divide p out completely (exponent e) and
     multiply tau by (e+1); a leftover rem > 1 is one prime and multiplies tau by 2.
   - n > 1 is prime iff no sieving prime divides it (rem == n untouched) - not tau == 2.
   - small primes by trial division, not by a sieve.
   Per block prints: k T_b P_b minloc argmin  (same meaning as xsieve.c columns 1-5). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64;
int main(int argc, char **argv) {
  u64 N = strtoull(argv[1], 0, 10), B = strtoull(argv[2], 0, 10);
  u64 k0 = strtoull(argv[3], 0, 10), k1 = strtoull(argv[4], 0, 10);
  u64 r = 1; while ((r + 1) * (r + 1) <= N) r++;
  u64 *pr = malloc(sizeof(u64) * (r / 2 + 10)); size_t np = 0;
  for (u64 c = 2; c <= r; c++) { int ok = 1;
    for (size_t j = 0; j < np && pr[j] * pr[j] <= c; j++) if (c % pr[j] == 0) { ok = 0; break; }
    if (ok) pr[np++] = c; }
  u64 *rem = malloc(sizeof(u64) * B); uint32_t *tau = malloc(sizeof(uint32_t) * B);
  unsigned char *hit = malloc(B);
  for (u64 k = k0; k <= k1; k++) {
    u64 lo = (k - 1) * B + 1, hi = k * B; if (hi > N) hi = N; u64 len = hi - lo + 1;
    for (u64 i = 0; i < len; i++) { rem[i] = lo + i; tau[i] = 1; hit[i] = 0; }
    for (size_t j = 0; j < np; j++) { u64 p = pr[j]; if (p * p > hi) break;
      u64 s = (lo + p - 1) / p * p;
      for (u64 m = s; m <= hi; m += p) { u64 i = m - lo, x = rem[i] / p; uint32_t e = 1;
        while (x % p == 0) { x /= p; e++; }
        rem[i] = x; tau[i] *= (e + 1); if (m != p) hit[i] = 1; } }
    long long T = 0, P = 0, minloc = (1LL << 60), arg = 0;
    for (u64 i = 0; i < len; i++) { u64 n = lo + i;
      if (rem[i] > 1) tau[i] *= 2;
      if (n % tau[i] == 0) T++;
      if (n > 1 && !hit[i]) P++;
      long long loc = 2 * T - P; if (loc < minloc) { minloc = loc; arg = (long long)n; } }
    printf("%llu %lld %lld %lld %lld\n", (unsigned long long)k, T, P, minloc, arg); fflush(stdout);
  }
  return 0;
}
