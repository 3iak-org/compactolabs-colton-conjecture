/* Check pi(x) > f(x) = (x/ln x)(1 + 1/(2 ln x)) on [59,1e9] via interval slacks
   slack(q) = pi(q) - f(q'), q' next prime (1e9 for the last interval).
   f is increasing for x >= 59 (f' = 1/L - 1/(2L^2) - 1/L^3 > 0 once L > 1.5), so on [q,q') pi(x)=pi(q) and
   pi(q) - f(q') > 0 implies pi(x) > f(x) for all x in [q,q'), 59 <= x <= 1e9.
   Sieve of Atkin (no Eratosthenes).  EVERY interval is evaluated in MPFR (PREC bits) with directed
   rounding, no prefilter: L = ln q' rounded DOWN, q'/L and q'/(2L^2) rounded UP, sum rounded UP,
   slack = pi(q) - f_hi rounded DOWN, so the computed slack is a lower bound of the exact one
   (all operands positive, so each directed operation is monotone).  FAIL if any computed slack <= 0. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <mpfr.h>
#define LIM 1000000000ULL
#define NB 8
#define PREC 128
static const uint64_t BL[NB+1]={59,100,1000,10000,100000,1000000,10000000,100000000,LIM};
static int blk(uint64_t q){int b=0;while(b<NB-1&&q>=BL[b+1])b++;return b;}
static mpfr_t x,L,t,u,f,s,best[NB];
static int have[NB]; static uint64_t bq[NB],bp[NB];
static uint64_t pq=0,ppi=0,pcount=0,nint=0,nfail=0,ffq=0;
static void interval(uint64_t q,uint64_t qpi,uint64_t p){
  if(q<59)return;
  mpfr_set_ui(x,p,MPFR_RNDN);           /* exact, p <= 1e9 */
  mpfr_log(L,x,MPFR_RNDD);              /* L <= ln x */
  mpfr_div(t,x,L,MPFR_RNDU);            /* >= x/ln x */
  mpfr_mul_ui(u,L,2,MPFR_RNDD);         /* 2L */
  mpfr_mul(u,u,L,MPFR_RNDD);            /* <= 2 ln^2 x */
  mpfr_div(u,x,u,MPFR_RNDU);            /* >= x/(2 ln^2 x) */
  mpfr_add(f,t,u,MPFR_RNDU);            /* >= f(x) */
  mpfr_ui_sub(s,qpi,f,MPFR_RNDD);       /* <= pi(q)-f(x) */
  nint++;
  if(mpfr_sgn(s)<=0){ if(!nfail)ffq=q; nfail++; }
  int b=blk(q);
  if(!have[b]||mpfr_cmp(s,best[b])<0){mpfr_set(best[b],s,MPFR_RNDD);have[b]=1;bq[b]=q;bp[b]=p;}
}
static void feed(uint64_t p){ pcount++; if(pq)interval(pq,ppi,p); pq=p; ppi=pcount; }
int main(void){
  mpfr_inits2(PREC,x,L,t,u,f,s,(mpfr_ptr)0);
  for(int i=0;i<NB;i++)mpfr_init2(best[i],PREC);
  /* Sieve of Atkin to LIM: bit array, quadratic-form toggles, then square-free pass. */
  uint8_t*bits=calloc(LIM/8+1,1);
#define TOG(n) (bits[(n)>>3]^=(uint8_t)(1u<<((n)&7)))
#define GET(n) ((bits[(n)>>3]>>((n)&7))&1)
  for(uint64_t x=1;4*x*x+1<=LIM;x++) for(uint64_t y=1;;y++){uint64_t n=4*x*x+y*y; if(n>LIM)break; uint64_t r=n%12; if(r==1||r==5)TOG(n);}
  for(uint64_t x=1;3*x*x+1<=LIM;x++) for(uint64_t y=1;;y++){uint64_t n=3*x*x+y*y; if(n>LIM)break; if(n%12==7)TOG(n);}
  for(uint64_t x=2;;x++){ if(3*x*x-(x-1)*(x-1)>LIM)break;
    for(uint64_t y=x-1;y>=1;y--){uint64_t n=3*x*x-y*y; if(n>LIM)break; if(n%12==11)TOG(n);} }
  /* remove multiples of squares of the (already settled, increasing) Atkin primes */
  for(uint64_t r=5;r*r<=LIM;r++) if(GET(r)) for(uint64_t m=r*r;m<=LIM;m+=r*r) if(m<=LIM) bits[m>>3]&=(uint8_t)~(1u<<(m&7));
  feed(2);feed(3);
  for(uint64_t n=5;n<=LIM;n++) if(GET(n)) feed(n);
  /* last interval: [pq, 1e9], f(1e9) */
  interval(pq,ppi,LIM);
  fprintf(stderr,"pi(1e9)=%llu last prime %llu\n",(unsigned long long)pcount,(unsigned long long)pq);
  printf("# check-rs62: pi(x) > (x/ln x)(1+1/(2 ln x)) on [59,1e9]; columns block_lo block_hi min_slack argmin_q nextprime\n");
  printf("# slack(q)=pi(q)-f(q'); last interval uses f(1e9), so its 'nextprime' is printed as 1000000000 (not prime). Blocks [lo,hi), last closed.\n");
  for(int b=0;b<NB;b++){
    if(!have[b]){fprintf(stderr,"empty block %d\n",b);return 1;}
    printf("%llu %llu ",(unsigned long long)BL[b],(unsigned long long)BL[b+1]);
    mpfr_printf("%.6R*f",MPFR_RNDD,best[b]);
    printf(" %llu %llu\n",(unsigned long long)bq[b],(unsigned long long)bp[b]);
  }
  printf("INTERVALS %llu\n",(unsigned long long)nint);
  if(!nfail) printf("PASS\n"); else printf("FAIL %llu (%llu intervals)\n",(unsigned long long)ffq,(unsigned long long)nfail);
  return 0;
}
