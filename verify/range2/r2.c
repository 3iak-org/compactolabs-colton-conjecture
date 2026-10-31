// Second implementation (range2): tau by additive divisor sieve, primality by segmented Eratosthenes.
// Two passes over blocks of 1e6: pass1 block totals, pass2 running T/pi with offsets.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>
#define B 1000000u
#define NB 1000
static uint32_t sp[4000]; static int nsp;
static void fill(uint32_t lo, uint32_t hi, uint16_t*tau, uint8_t*comp){ // block lo..hi inclusive
  uint32_t len=hi-lo+1; memset(tau,0,len*2); memset(comp,0,len);
  for(uint64_t d=1;d*d<=hi;d++){
    uint64_t s=((lo+d-1)/d)*d; if(s<d*d)s=d*d;
    for(uint64_t m=s;m<=hi;m+=d) tau[m-lo]+=2;
    if(d*d>=lo) tau[d*d-lo]-=1;
  }
  for(int i=0;i<nsp;i++){ uint64_t p=sp[i]; if(p*p>hi)break;
    uint64_t s=((lo+p-1)/p)*p; if(s<p*p)s=p*p;
    for(uint64_t m=s;m<=hi;m+=p) comp[m-lo]=1; }
  if(lo==1) comp[0]=1; // 1 not prime
}
typedef struct{int nz; int64_t minv; uint32_t minpos; int64_t negmin; int neq; uint32_t eq[4096]; int64_t mk; } Res;
int main(){
  { static uint8_t c[40000]; for(int i=2;i<40000;i++){ if(!c[i]){ sp[nsp++]=i; for(long j=(long)i*i;j<40000;j+=i)c[j]=1;} } }
  static int64_t bT[NB],bP[NB],oT[NB+1],oP[NB+1]; static Res R[NB];
  #pragma omp parallel
  { uint16_t*tau=malloc(B*2); uint8_t*comp=malloc(B);
    #pragma omp for schedule(dynamic,1)
    for(int b=0;b<NB;b++){ uint32_t lo=b*B+1,hi=(b+1)*B; fill(lo,hi,tau,comp);
      int64_t t=0,p=0; for(uint32_t n=lo;n<=hi;n++){ if(n%tau[n-lo]==0)t++; if(!comp[n-lo])p++; } bT[b]=t;bP[b]=p; } }
  for(int b=0;b<NB;b++){ oT[b+1]=oT[b]+bT[b]; oP[b+1]=oP[b]+bP[b]; }
  #pragma omp parallel
  { uint16_t*tau=malloc(B*2); uint8_t*comp=malloc(B);
    #pragma omp for schedule(dynamic,1)
    for(int b=0;b<NB;b++){ uint32_t lo=b*B+1,hi=(b+1)*B; fill(lo,hi,tau,comp);
      Res*r=&R[b]; r->minv=INT64_MAX; r->negmin=INT64_MAX; r->mk=INT64_MAX; r->neq=0;
      int64_t T=oT[b],P=oP[b];
      for(uint32_t n=lo;n<=hi;n++){ if(n%tau[n-lo]==0)T++; int pr=!comp[n-lo]; if(pr)P++;
        int64_t v=2*T-P; if(v<r->negmin) r->negmin=v;
        if(v==0){ if(r->neq<4096) r->eq[r->neq]=n; r->neq++; }
        if(n>=1000000 && v<r->minv){ r->minv=v; r->minpos=n; }
        if(pr && v<r->mk) r->mk=v; } } }
  FILE*f=fopen("checkpoints.txt","w");
  int64_t gmin=INT64_MAX; uint32_t gpos=0, neg=INT64_MAX; int64_t allmin=INT64_MAX;
  FILE*e=fopen("equality.txt","w"); long ne=0;
  for(int b=0;b<NB;b++){ Res*r=&R[b];
    fprintf(f,"%u %lld %lld %lld\n",(b+1)*B,(long long)oT[b+1],(long long)oP[b+1],(long long)r->mk);
    if(r->minv<gmin){gmin=r->minv;gpos=r->minpos;}
    if(r->negmin<allmin)allmin=r->negmin;
    if(r->neq>4096){fprintf(stderr,"eq overflow\n");return 1;}
    for(int i=0;i<r->neq;i++){fprintf(e,"%u\n",r->eq[i]);ne++;} }
  fclose(f);fclose(e);
  printf("min over all n of 2T-pi = %lld (>=0 means verdict holds)\n",(long long)allmin);
  printf("equality cases: %ld (equality.txt)\nmin over [1e6,1e9] = %lld first at n=%u\n",ne,(long long)gmin,gpos);
  printf("T(1e9)=%lld pi(1e9)=%lld\n",(long long)oT[NB],(long long)oP[NB]);
  return 0; }
