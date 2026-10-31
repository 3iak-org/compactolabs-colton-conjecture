// p-generators: a >= 1 with 2*tau(a) | a.  Segmented tau sieve over [1,M].
// usage: gen M out_prefix   -> writes <prefix>.txt ("a g" lines) and <prefix>.pi ("pi(g)" lines, aligned)
// Method: per segment, divide out every prime p <= sqrt(hi) from a residue array, accumulating
// tau and the largest prime factor; leftover residue >1 is a prime > sqrt(hi).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#define SEG (1u<<20)
typedef struct { uint32_t *a,*g; size_t n,cap; } vec;
static void push(vec*v,uint32_t a,uint32_t g){ if(v->n==v->cap){v->cap=v->cap?v->cap*2:1024;v->a=realloc(v->a,v->cap*4);v->g=realloc(v->g,v->cap*4);} v->a[v->n]=a;v->g[v->n]=g;v->n++; }
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage\n");return 1;}
  uint64_t M=strtoull(argv[1],0,10);
  uint32_t R=(uint32_t)sqrtl((long double)M); while((uint64_t)(R+1)*(R+1)<=M)R++; while((uint64_t)R*R>M)R--;
  // small primes <= R
  char*cs=calloc(R+2,1); uint32_t*pr=malloc(sizeof(uint32_t)*(R+2)); size_t np=0;
  for(uint32_t i=2;i<=R;i++){ if(!cs[i]){pr[np++]=i; for(uint64_t j=(uint64_t)i*i;j<=R;j+=i)cs[j]=1;} }
  size_t nseg=(M+SEG-1)/SEG; // segment s covers (s*SEG, (s+1)*SEG]
  vec*res=calloc(nseg,sizeof(vec));
  #pragma omp parallel
  {
    uint32_t*rem=malloc(SEG*4),*gp=malloc(SEG*4); uint16_t*tau=malloc(SEG*2);
    #pragma omp for schedule(dynamic,1)
    for(size_t s=0;s<nseg;s++){
      uint64_t lo=(uint64_t)s*SEG+1, hi=(uint64_t)(s+1)*SEG; if(hi>M)hi=M; uint32_t len=hi-lo+1;
      for(uint32_t i=0;i<len;i++){rem[i]=lo+i;tau[i]=1;gp[i]=1;}
      for(size_t k=0;k<np;k++){ uint32_t p=pr[k]; if((uint64_t)p*p>hi)break;
        uint64_t f=((lo+p-1)/p)*p;
        for(uint64_t m=f;m<=hi;m+=p){ uint32_t i=m-lo,r=rem[i]; int e=0; do{r/=p;e++;}while(r%p==0); rem[i]=r; tau[i]*=(e+1); gp[i]=p; }
      }
      for(uint32_t i=0;i<len;i++){ uint32_t a=lo+i,t=tau[i],g=gp[i]; if(rem[i]>1){t*=2;g=rem[i];}
        if(a%(2u*t)==0) push(&res[s],a,g); }
    }
    free(rem);free(gp);free(tau);
  }
  // pi table up to G = max g
  uint32_t G=2; for(size_t s=0;s<nseg;s++)for(size_t i=0;i<res[s].n;i++)if(res[s].g[i]>G)G=res[s].g[i];
  uint64_t nb=(G/2)+1, nw=(nb+63)/64;
  uint64_t*bits=calloc(nw,8); bits[0]|=1; // number 1 not prime
  for(uint64_t i=1;(2*i+1)*(2*i+1)<=G;i++) if(!((bits[i>>6]>>(i&63))&1)) for(uint64_t j=((2*i+1)*(2*i+1)-1)/2;j<nb;j+=2*i+1) bits[j>>6]|=1ULL<<(j&63);
  // bits beyond nb-1 : mark as composite so zero-count is exact
  for(uint64_t j=nb;j<nw*64;j++) bits[j>>6]|=1ULL<<(j&63);
  uint32_t*cnt=malloc((nw+1)*4); cnt[0]=0; for(uint64_t w=0;w<nw;w++)cnt[w+1]=cnt[w]+(64-__builtin_popcountll(bits[w]));
  char fn[1024]; snprintf(fn,sizeof fn,"%s.txt",argv[2]); FILE*fa=fopen(fn,"w");
  snprintf(fn,sizeof fn,"%s.pi",argv[2]); FILE*fp=fopen(fn,"w");
  size_t tot=0;
  for(size_t s=0;s<nseg;s++){ for(size_t i=0;i<res[s].n;i++){ uint32_t a=res[s].a[i],g=res[s].g[i];
      uint64_t idx=(g%2)?(g-1)/2:g/2-1; uint64_t w=idx>>6; unsigned b=idx&63;
      uint64_t mask=(b==63)?~0ULL:((1ULL<<(b+1))-1);
      uint64_t zeros=cnt[w]+(b+1-__builtin_popcountll(bits[w]&mask));
      uint64_t pi=(g<2)?0:1+zeros;
      fprintf(fa,"%u %u\n",a,g); fprintf(fp,"%llu\n",(unsigned long long)pi); tot++; } }
  fclose(fa);fclose(fp); fprintf(stderr,"M=%llu count=%zu maxg=%u\n",(unsigned long long)M,tot,G);
  return 0; }
