// RS62 (3.1) check on [59,1e9], implementation 1. Segmented sieve of Eratosthenes for the primes; for EVERY
// consecutive prime pair q<q' (q>=59; last interval ends at 1e9) Arb ball arithmetic (128 bits) evaluates
// s = pi(q) - f(q'), f(x)=x/ln x*(1+1/(2 ln x)). pi(q)-f(x) > s_lower for all x in [q,q') because f is increasing
// for x>e. An interval passes iff the ball's lower endpoint is > 0 (i.e. f's upper endpoint < pi(q)).
// Prints, per decade block, the minimum LOWER endpoint (rounded down to 6 places) and its argmin, then INTERVALS n.
// usage: rs62lower [bias]   bias (default 0) is subtracted from pi: a corruption knob for testing that FAIL happens.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <flint/arb.h>
#include <flint/arf.h>
#include <flint/fmpz.h>
#define LIM 1000000000ULL
#define SEG (1u<<24)
#define PREC 128
static const uint64_t B[9]={59,100,1000,10000,100000,1000000,10000000,100000000,1000000001ULL};
static arf_t mn[8]; static uint64_t aq[8],aqn[8]; static int have_mn[8];
static arb_t x,l,t,s,fx; static arf_t lb;
static uint64_t cnt_iv=0, bias=0, firstfail=0; static int fail=0;
static void rec(uint64_t q,uint64_t qn,uint64_t pi){
  uint64_t X=qn?qn:LIM;
  arb_set_ui(x,X); arb_log(l,x,PREC);
  arb_div(fx,x,l,PREC);                 // x/ln x
  arb_mul_ui(t,l,2,PREC); arb_inv(t,t,PREC); arb_add_ui(t,t,1,PREC);   // 1+1/(2 ln x)
  arb_mul(fx,fx,t,PREC);
  arb_set_ui(s,pi-bias); arb_sub(s,s,fx,PREC);
  arb_get_lbound_arf(lb,s,PREC);
  cnt_iv++;
  if(arf_sgn(lb)<=0 && !fail){fail=1;firstfail=q;}
  int b=0; while(q>=B[b+1])b++;
  if(!have_mn[b]||arf_cmp(lb,mn[b])<0){arf_set(mn[b],lb);have_mn[b]=1;aq[b]=q;aqn[b]=qn;}
}
int main(int argc,char**argv){
  if(argc>1)bias=strtoull(argv[1],0,10);
  arb_init(x);arb_init(l);arb_init(t);arb_init(s);arb_init(fx);arf_init(lb);
  for(int i=0;i<8;i++){arf_init(mn[i]);have_mn[i]=0;}
  uint32_t R=31623; char*c=calloc(R+1,1); uint32_t*pr=malloc(4*5000);size_t np=0;
  for(uint32_t i=2;i<=R;i++)if(!c[i]){pr[np++]=i;for(uint64_t j=(uint64_t)i*i;j<=R;j+=i)c[j]=1;}
  char*seg=malloc(SEG); uint64_t pi=0,q=0; int have=0; uint64_t cnt=0;
  for(uint64_t lo=0;lo<=LIM;lo+=SEG){
    uint64_t hi=lo+SEG-1; if(hi>LIM)hi=LIM; uint32_t len=hi-lo+1; memset(seg,1,len);
    if(lo==0){seg[0]=0;if(len>1)seg[1]=0;}
    for(size_t k=0;k<np;k++){uint64_t p=pr[k]; if(p*p>hi)break; uint64_t s0=((lo+p-1)/p)*p; if(s0<p*p)s0=p*p; for(uint64_t m=s0;m<=hi;m+=p)seg[m-lo]=0;}
    for(uint32_t i=0;i<len;i++)if(seg[i]){uint64_t p=lo+i; cnt++;
      if(have) rec(q,p,pi);
      q=p;pi=cnt; have=(q>=59);}
  }
  rec(q,0,pi);
  fprintf(stderr,"pi(1e9)=%llu last prime %llu\n",(unsigned long long)cnt,(unsigned long long)q);
  for(int b=0;b<8;b++){
    fmpz_t z; fmpz_init(z); arf_t e; arf_init(e);
    arf_mul_ui(e,mn[b],1000000,ARF_PREC_EXACT,ARF_RND_DOWN); arf_get_fmpz(z,e,ARF_RND_FLOOR);  // exact; floor => rounded down
    int neg=fmpz_sgn(z)<0; if(neg)fmpz_abs(z,z);
    unsigned long long a=fmpz_fdiv_ui(z,1000000ULL); fmpz_t w; fmpz_init(w); fmpz_fdiv_q_ui(w,z,1000000ULL);
    char*str=fmpz_get_str(NULL,10,w);
    printf("%llu %llu %s%s.%06llu %llu %llu\n",(unsigned long long)B[b],(unsigned long long)(b<7?B[b+1]:1000000000ULL),neg?"-":"",str,a,
      (unsigned long long)aq[b],(unsigned long long)aqn[b]);
    free(str);
  }
  printf("INTERVALS %llu\n",(unsigned long long)cnt_iv);
  printf(fail?"FAIL %llu\n":"PASS\n",(unsigned long long)firstfail);
  return 0;}
