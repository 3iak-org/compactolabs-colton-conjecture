/* ref-colton: tau(n) = #{(d, n/d)} by counting divisor pairs d <= sqrt(n): no factorisation.
   For each d, every multiple m of d with m >= d*d gets +2 (+1 if m == d*d).
   Primes: n > 1 with tau == 2. Block k = ((k-1)e6, k e6].
   Output per block: k Tb pib minlocal_over_primes minlocal_over_all_n */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define B 1000000ULL
int main(int c,char**v){
  int k0=atoi(v[1]),k1=atoi(v[2]); uint16_t *t=malloc(2*B);
  for(int k=k0;k<=k1;k++){
    uint64_t lo=(k-1)*B+1, hi=k*B;
    for(uint64_t i=0;i<B;i++)t[i]=0;
    for(uint64_t d=1;d*d<=hi;d++){
      uint64_t m=d*d; if(m<lo) m=((lo+d-1)/d)*d;
      if(m==d*d){ t[m-lo]+=1; m+=d; }
      for(;m<=hi;m+=d) t[m-lo]+=2;
    }
    long long Tb=0,pb=0,mp=1LL<<60,ma=1LL<<60;
    for(uint64_t i=0;i<B;i++){ uint64_t n=lo+i;
      if(n%t[i]==0)Tb++;
      if(n>1&&t[i]==2){pb++; long long x=2*Tb-pb; if(x<mp)mp=x;}
      long long x=2*Tb-pb; if(x<ma)ma=x; }
    printf("%d %lld %lld %lld %lld\n",k,Tb,pb,mp,ma); fflush(stdout);
  }}
