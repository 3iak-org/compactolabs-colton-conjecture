// findings/colton-threshold.md sections 2 and 6: SANITY ONLY, not an input to the Theorem (thm22, 2026-10-30).
// exploration: Z(n) = sum_{a in G, a<=Mg} max(0, pi(floor(n/a)) - pi(g(a)))
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint64_t *bits,*pref; static uint64_t X;
static uint64_t pi(uint64_t x){ if(x<2) return 0; if(x>X){fprintf(stderr,"x too big %llu\n",(unsigned long long)x);exit(1);} 
  // odd-only: bit i represents 2i+1; count odd primes <= x plus 1 for 2
  uint64_t i=(x-1)/2; // index of largest odd <= x
  uint64_t w=i>>6, b=i&63; uint64_t m = (b==63)?~0ull:((1ull<<(b+1))-1);
  return 1 + pref[w] + __builtin_popcountll(bits[w]&m); }
int main(int argc,char**argv){
  X=strtoull(argv[1],0,10); const char*gf=argv[2];
  uint64_t nb=X/2+1, nw=nb/64+1; bits=malloc(8*nw); memset(bits,0xff,8*nw);
  bits[0]&=~1ull; // 1 not prime
  for(uint64_t i=1; ; i++){ uint64_t p=2*i+1; if(p*p>X) break; if(bits[i>>6]>>(i&63)&1){ for(uint64_t j=(p*p-1)/2;j<nb;j+=p) bits[j>>6]&=~(1ull<<(j&63)); } }
  // clear beyond nb
  for(uint64_t j=nb;j<nw*64;j++) bits[j>>6]&=~(1ull<<(j&63));
  pref=malloc(8*(nw+1)); pref[0]=0; for(uint64_t w=0;w<nw;w++) pref[w+1]=pref[w]+__builtin_popcountll(bits[w]);
  FILE*f=fopen(gf,"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET); uint64_t ng=sz/16; uint64_t*G=malloc(sz); fread(G,8,2*ng,f); fclose(f);
  uint64_t *pg=malloc(8*ng); for(uint64_t k=0;k<ng;k++) pg[k]=pi(G[2*k+1]);
  fprintf(stderr,"sieve to %llu done, pi(X)=%llu, ng=%llu\n",(unsigned long long)X,(unsigned long long)pi(X),(unsigned long long)ng);
  uint64_t n; while(scanf("%llu",(unsigned long long*)&n)==1){ uint64_t Z=0; uint64_t cnt=0; uint64_t amax=0;
    for(uint64_t k=0;k<ng;k++){ uint64_t a=G[2*k]; if(a>n) break; uint64_t q=n/a; uint64_t v=pi(q); if(v>pg[k]){Z+=v-pg[k];cnt++; amax=a;} }
    printf("%llu %llu %llu %llu\n",(unsigned long long)n,(unsigned long long)Z,(unsigned long long)cnt,(unsigned long long)amax); fflush(stdout);}
  return 0; }
