/* referee: RS62 (3.1) weak form, pi(x) >= f(x) = (x/ln x)(1+1/(2 ln x)), for every real x in [59, 1e9].
   Every prime gap [q, q') with q >= 59 is evaluated in FLINT/Arb (128 bits), no floating-point step:
   pi = pi(q) on [q, q'), f increasing on [59, inf), so the condition is pi(q) - f(q') >= 0, with q' -> 1e9
   for the last interval (closed at 1e9). Primes by a byte-per-odd Eratosthenes sieve.
   Prints per decade block the exact Arb lower endpoint of the minimum slack (to 6 places, rounded down),
   the argmin q, the interval count, and PASS iff every ball lies strictly in (0, inf). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <flint/arb.h>
#define N 1000000000L
static const long BL[9]={59,100,1000,10000,100000,1000000,10000000,100000000,N+1};
int main(void){
  long h=N/2+1; char*c=malloc(h); memset(c,1,h); c[0]=0;
  for(long i=1;(2*i+1)*(2*i+1)<=N;i++) if(c[i]){long p=2*i+1; for(long j=p*p/2;j<h;j+=p)c[j]=0;}
  slong prec=128; arb_t L,f,t,s,best[8]; arb_init(L);arb_init(f);arb_init(t);arb_init(s);
  long bq[8],cnt[8]; int have[8]={0}; for(int b=0;b<8;b++){arb_init(best[b]);cnt[b]=0;}
  long fails=0, nint=0, pi=1 /* the prime 2 */, q=0, qpi=0;
  for(long n=3;;n+=2){
    int isp = (n<=N) && c[n/2];
    if(!isp && n<=N) continue;
    long right = (n<=N)? n : N;            /* next prime, or 1e9 for the last interval */
    if(q>=59){
      arb_log_ui(L,right,prec);              /* L = ln right */
      arb_set_ui(t,right); arb_div(f,t,L,prec);            /* x/L */
      arb_mul_2exp_si(t,L,1); arb_inv(t,t,prec); arb_add_ui(t,t,1,prec); /* 1 + 1/(2L) */
      arb_mul(f,f,t,prec);
      arb_set_ui(s,qpi); arb_sub(s,s,f,prec);
      if(!arb_is_positive(s)) {fails++; fprintf(stderr,"FAIL q=%ld\n",q);}
      int b=0; while(q>=BL[b+1])b++;
      cnt[b]++; nint++;
      arf_t lo; arf_init(lo); arb_get_lbound_arf(lo,s,prec);
      if(!have[b]){arb_set(best[b],s);bq[b]=q;have[b]=1;}
      else { arf_t lb; arf_init(lb); arb_get_lbound_arf(lb,best[b],prec); if(arf_cmp(lo,lb)<0){arb_set(best[b],s);bq[b]=q;} arf_clear(lb);}
      arf_clear(lo);
    }
    if(n>N) break;
    pi++; q=n; qpi=pi;
  }
  printf("# referee rs62every.c: every prime-gap interval in Arb, 128 bits; columns block_lo block_hi intervals min_slack_lbound argmin_q\n");
  for(int b=0;b<8;b++){ arf_t lo; arf_init(lo); arb_get_lbound_arf(lo,best[b],prec);
    /* floor to 6 decimals: print with arf, conservatively subtract 1e-6 is unnecessary since we print lbound truncated */
    double d = arf_get_d(lo, ARF_RND_FLOOR);
    printf("%ld %ld %ld %.6f %ld\n",BL[b],(b==7?N:BL[b+1]),cnt[b],d-0.0000005,bq[b]); arf_clear(lo);}
  printf("intervals %ld pi(1e9) %ld\n", nint, pi);
  printf(fails? "FAIL %ld\n":"PASS\n", fails);
  return 0;
}
