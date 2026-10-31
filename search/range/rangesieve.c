/* Segmented factor sieve: for each 1e6-block k in [k0,k1], count
 *   Tb  = #{n in block : tau(n) | n},  pib = #{primes in block},
 * and, over primes p in block, min of local margin 2*Tl(p)-pil(p)
 * where Tl,pil count only from the start of the block (global margin =
 * 2*T0 - pi0 + local).  Block k = ((k-1)*1e6, k*1e6].
 * With -v (only valid for k0==1) also prints every n with global margin <= 2
 * for n<=1000 and every n with margin<=0 (equality/violation) anywhere.
 * Usage: rangesieve k0 k1 [-v]     Output: "k Tb pib minlocal argminp" lines. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define BLK 1000000ULL
#define SUB 100000ULL
int main(int argc,char**argv){
  if(argc<3) return 2;
  int k0=atoi(argv[1]),k1=atoi(argv[2]); int verbose=argc>3&&!strcmp(argv[3],"-v");
  if(verbose&&k0!=1) return 2;
  uint32_t L=31700; char *cs=calloc(L+1,1); uint32_t *pr=malloc(4*4000); int np=0;
  for(uint32_t i=2;i<=L;i++){ if(!cs[i]){pr[np++]=i; for(uint64_t j=(uint64_t)i*i;j<=L;j+=i)cs[j]=1;} }
  uint32_t *rem=malloc(4*SUB); uint16_t *tau=malloc(2*SUB);
  int64_t Tg=0,pig=0; /* global running (used for -v only, k0==1) */
  for(int k=k0;k<=k1;k++){
    int64_t Tb=0,pib=0,minl=INT64_MAX; uint64_t argp=0;
    for(uint64_t lo=(uint64_t)(k-1)*BLK+1; lo<=(uint64_t)k*BLK; lo+=SUB){
      uint64_t hi=lo+SUB-1; uint32_t len=SUB;
      for(uint32_t i=0;i<len;i++){rem[i]=lo+i;tau[i]=1;}
      for(int j=0;j<np;j++){ uint64_t p=pr[j]; if(p*p>hi) break;
        uint64_t s=((lo+p-1)/p)*p;
        for(uint64_t m=s;m<=hi;m+=p){ uint32_t i=m-lo,r=rem[i]/p; int e=1;
          while(r%p==0){r/=p;e++;} rem[i]=r; tau[i]*=e+1; } }
      for(uint32_t i=0;i<len;i++){ if(rem[i]>1) tau[i]*=2; }
      /* primes p with p*p>hi were not sieved: a composite n<=hi has a prime factor
         <= sqrt(hi), all divided out, so any leftover rem>1 is a single prime. */
      for(uint32_t i=0;i<len;i++){ uint64_t n=lo+i; int pm=(tau[i]==2);
        if(n%tau[i]==0){Tb++;Tg++;}
        if(pm){pib++;pig++; int64_t ml=2*Tb-pib; if(ml<minl){minl=ml;argp=n;}}
        if(verbose){ int64_t mg=2*Tg-pig;
          if(n<=1000 && mg<=2) printf("LOW n=%llu T=%lld pi=%lld margin=%lld\n",(unsigned long long)n,(long long)Tg,(long long)pig,(long long)mg);
          if(mg<=0 && n>1000) printf("EQ n=%llu T=%lld pi=%lld margin=%lld\n",(unsigned long long)n,(long long)Tg,(long long)pig,(long long)mg);}
      }
    }
    printf("%d %lld %lld %lld %llu\n",k,(long long)Tb,(long long)pib,(long long)minl,(unsigned long long)argp);
    fflush(stdout);
  }
  return 0; }
