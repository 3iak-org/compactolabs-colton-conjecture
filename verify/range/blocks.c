/* Independent check of pi(n) <= 2T(n).  tau via segmented factorisation
   (divide out each small prime, multiply (e+1)); primes = (tau==2).
   usage: blocks k0 k1                -> lines "k t q minprimelocal minalllocal"
          blocks k0 k1 T0 P0 thr      -> (single block k0..k1 with offsets) lists n with 2T-pi<=thr
   block k = n in ((k-1)e6, k e6]; t = #{tau|n} in block, q = #primes in block;
   minprimelocal = min over primes of (2t_run - q_run) with running counts through that prime. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define S 1000000
int main(int argc,char**argv){
  int k0=atoi(argv[1]),k1=atoi(argv[2]);
  int list=argc>=6; long long T0=0,P0=0,thr=0;
  if(list){T0=atoll(argv[3]);P0=atoll(argv[4]);thr=atoll(argv[5]);}
  /* small primes by trial division (independent of any sieve of Eratosthenes) */
  int sp[4000],ns=0;
  for(int n=2;n<=31700;n++){int ok=1;for(int i=0;i<ns&&(long)sp[i]*sp[i]<=n;i++)if(n%sp[i]==0){ok=0;break;} if(ok)sp[ns++]=n;}
  uint32_t*rem=malloc(S*4); uint16_t*tau=malloc(S*2);
  for(int k=k0;k<k1;k++){
    uint64_t lo=(uint64_t)(k-1)*S+1, hi=(uint64_t)k*S;
    for(int i=0;i<S;i++){rem[i]=lo+i;tau[i]=1;}
    for(int j=0;j<ns&&(uint64_t)sp[j]*sp[j]<=hi;j++){
      uint32_t p=sp[j]; uint64_t f=((lo+p-1)/p)*p;
      for(uint64_t m=f;m<=hi;m+=p){
        uint32_t*r=&rem[m-lo]; int e=0; do{*r/=p;e++;}while(*r%p==0); tau[m-lo]*=e+1;}
    }
    long long t=0,q=0,mp=1LL<<60,ma=1LL<<60;
    for(int i=0;i<S;i++){
      if(rem[i]>1)tau[i]*=2;
      uint64_t n=lo+i;
      if(n%tau[i]==0)t++;
      if(tau[i]==2&&n>1){q++; long long v=2*t-q; if(v<mp)mp=v;}
      long long v=2*t-q; if(v<ma)ma=v;
      if(list){long long mg=2*(T0+t)-(P0+q); if(mg<=thr)printf("n=%llu T=%lld pi=%lld margin=%lld prime=%d\n",(unsigned long long)n,T0+t,P0+q,mg,tau[i]==2&&n>1);}
    }
    if(!list)printf("%d %lld %lld %lld %lld\n",k,t,q,mp,ma);
  }
}
