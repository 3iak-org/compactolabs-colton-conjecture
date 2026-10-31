// p-generators {a : 2*tau(a) | a}, a <= M, by additive sieves (no factorisation of any a):
//  tau: for each d <= sqrt(M), for each multiple m = d*d, d*d+d, ...: tau[m] += (m==d*d ? 1 : 2)
//       (counts divisor pairs {d, m/d} with d*d <= m).
//  lpf: primes from own Eratosthenes; for p ascending, lpf[multiples of p] = p (last write = largest prime factor).
// usage: gen_add M out.txt  -> "a g" lines
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
int main(int argc,char**argv){
  uint64_t M=strtoull(argv[1],0,10);
  uint16_t*tau=calloc(M+1,2); uint32_t*lpf=calloc(M+1,4); char*comp=calloc(M+1,1);
  for(uint64_t d=1;d*d<=M;d++) for(uint64_t m=d*d;m<=M;m+=d) tau[m]+=(m==d*d)?1:2;
  for(uint64_t p=2;p<=M;p++){ if(comp[p])continue;
    if(p*p<=M) for(uint64_t j=p*p;j<=M;j+=p)comp[j]=1;
    for(uint64_t j=p;j<=M;j+=p)lpf[j]=p; }
  FILE*f=fopen(argv[2],"w"); size_t n=0;
  for(uint64_t a=2;a<=M;a++) if(a%(2u*tau[a])==0){fprintf(f,"%llu %u\n",(unsigned long long)a,lpf[a]);n++;}
  fclose(f); fprintf(stderr,"M=%llu count=%zu\n",(unsigned long long)M,n); return 0;}
