/* Generators: a<=M with 2*tau(a) | a.  Own smallest-prime-factor table (linear sieve),
   factorise each even a, tau from exponents.  No divisor-count sieve.
   Output: lines "a g" ascending. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char**argv){
  uint32_t M = argc>1? (uint32_t)strtoul(argv[1],0,10):28653696u;
  uint32_t *spf = calloc(M+1,4), *pr = malloc(4*2000000); uint32_t np=0;
  for(uint32_t i=2;i<=M;i++){
    if(!spf[i]){spf[i]=i;pr[np++]=i;}
    for(uint32_t j=0;j<np;j++){uint64_t v=(uint64_t)pr[j]*i; if(pr[j]>spf[i]||v>M)break; spf[v]=pr[j];}
  }
  for(uint32_t a=2;a<=M;a+=2){
    uint32_t n=a; uint64_t tau=1; uint32_t g=0;
    while(n>1){uint32_t p=spf[n],e=0; while(n%p==0){n/=p;e++;} tau*=e+1; if(p>g)g=p;}
    if(a % (2*tau)==0) printf("%u %u\n",a,g);
  }
  return 0;
}
