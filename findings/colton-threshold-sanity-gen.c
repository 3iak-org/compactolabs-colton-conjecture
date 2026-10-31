// findings/colton-threshold.md sections 2 and 6: SANITY ONLY, not an input to the Theorem (thm22, 2026-10-30).
// exploration only: enumerate p-generators a <= M (2*tau(a) | a) with g(a)=gpf(a)
// segmented: for each segment compute tau and gpf by trial division by primes <= sqrt(M)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
int main(int argc,char**argv){
  uint64_t M=strtoull(argv[1],0,10); const char*out=argv[2];
  uint64_t r=(uint64_t)sqrtl((long double)M)+2;
  char*isc=calloc(r+1,1); uint32_t*pr=malloc(sizeof(uint32_t)*(r+1)); int np=0;
  for(uint64_t i=2;i<=r;i++){ if(!isc[i]){pr[np++]=i; for(uint64_t j=i*i;j<=r;j+=i)isc[j]=1;} }
  const uint64_t SEG=1<<22;
  uint64_t*rem=malloc(8*SEG); uint32_t*tau=malloc(4*SEG); uint64_t*gp=malloc(8*SEG);
  FILE*f=fopen(out,"wb"); uint64_t cnt=0;
  for(uint64_t lo=1;lo<=M;lo+=SEG){
    uint64_t hi=lo+SEG; if(hi>M+1)hi=M+1; uint64_t L=hi-lo;
    for(uint64_t i=0;i<L;i++){rem[i]=lo+i;tau[i]=1;gp[i]=1;}
    for(int k=0;k<np;k++){ uint64_t p=pr[k]; if(p*p>=hi && p>hi) break;
      uint64_t s=((lo+p-1)/p)*p;
      for(uint64_t m=s;m<hi;m+=p){ uint64_t i=m-lo; int e=0; while(rem[i]%p==0){rem[i]/=p;e++;} tau[i]*=(e+1); gp[i]=p; }
    }
    for(uint64_t i=0;i<L;i++){ if(rem[i]>1){tau[i]*=2; gp[i]=rem[i];}
      uint64_t a=lo+i; if(a%(2ull*tau[i])==0){ uint64_t rec[2]={a,gp[i]}; fwrite(rec,8,2,f); cnt++; } }
  }
  fclose(f); fprintf(stderr,"M=%llu generators=%llu\n",(unsigned long long)M,(unsigned long long)cnt); return 0;
}
