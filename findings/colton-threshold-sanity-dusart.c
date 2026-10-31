// findings/colton-threshold.md sections 2 and 6: SANITY ONLY, not an input to the Theorem (thm22, 2026-10-30).
// sanity (not proof): check Dusart (6.5) at every prime jump for 599 <= x <= X
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
int main(int argc,char**argv){ uint64_t X=strtoull(argv[1],0,10);
  uint8_t*s=calloc(X+1,1); for(uint64_t i=2;i*i<=X;i++) if(!s[i]) for(uint64_t j=i*i;j<=X;j+=i) s[j]=1;
  uint64_t k=0; long double minL=1e9, minU=1e9; uint64_t argL=0,argU=0; uint64_t prev=0;
  for(uint64_t p=2;p<=X;p++){ if(s[p]) continue;
    // interval [prev, p): pi = k ; lower bound worst at x -> p^-
    if(p>599 && prev>0){ long double L=logl((long double)p); long double fl=(p/L)*(1+1/L); long double m=(long double)k-fl; if(m<minL){minL=m;argL=p;} }
    k++; // now pi(p)=k
    if(p>=2){ long double L=logl((long double)p); long double fu=(p/L)*(1+1.2762L/L); long double m=fu-(long double)k; if(m<minU){minU=m;argU=p;} }
    prev=p; }
  printf("X=%llu pi(X)=%llu  min(pi(x)-lower) over x in [599,X] = %.6Lf near p=%llu ; min(upper-pi) at primes = %.6Lf at p=%llu\n",(unsigned long long)X,(unsigned long long)k,minL,(unsigned long long)argL,minU,(unsigned long long)argU);
}
