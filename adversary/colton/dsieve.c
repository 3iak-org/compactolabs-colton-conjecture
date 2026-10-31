/* adversary/colton/dsieve.c - independent recount of T(n), pi(n) for 1<=n<=N.
   Method (deliberately unlike search/range and verify/range):
   - tau(n) by DIVISOR-PAIR counting: for each d<=sqrt(hi), each multiple m=d*e
     in the segment with e>=d contributes 2 (1 if e==d). No factorisation.
   - primes by a separate segmented Eratosthenes bitmap (not tau==2).
   - asserts tau(n)==2 <=> prime as an internal cross-check.
   Per block of B integers it prints: block T_b pi_b minloc argmin lmin_bound
   minp (last column) = same min over primes only;
   where minloc = min over n in block of (2T_l(n)-pi_l(n)) with T_l,pi_l counted
   from block start, and lmin_bound = min over n of 2T_l(n)-pi_l(n) - 2*R(n),
   R(n) = analytic RHS of (3.3) for the stage set the theorem assigns to n
   (only for n>=1e7; coefficients read from argv file). Combine adds offsets.
   Also prints every n with global margin <=2 for n<=B (first block, verbose). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef long long ll;
static double C0[5], C1[5]; static double B0, B1; /* stage 0 / stage1 coefs, beta */
static double R(ll n){
  if(n<10000000LL) return -1e300;
  double u=log((double)n), *c; double b;
  if(n<=100000000LL){c=C0;b=B0;} else {c=C1;b=B1;}
  double g=0,up=1; for(int m=0;m<5;m++){g+=c[m]/up; up*=u;}
  return (double)n/u*g-b;
}
int main(int argc,char**argv){
  ll N=atoll(argv[1]), B=atoll(argv[2]); int k0=atoi(argv[3]), k1=atoi(argv[4]);
  FILE*cf=fopen(argv[5],"r"); for(int i=0;i<5;i++) if(fscanf(cf,"%lf",&C0[i])!=1) return 9;
  if(fscanf(cf,"%lf",&B0)!=1) return 9; for(int i=0;i<5;i++) if(fscanf(cf,"%lf",&C1[i])!=1) return 9;
  if(fscanf(cf,"%lf",&B1)!=1) return 9; fclose(cf);
  int verbose = argc>6;
  ll sq=(ll)sqrtl((long double)N)+2; while(sq*sq>N) sq--; 
  /* small primes up to sq by plain trial-free sieve */
  char*sm=calloc(sq+2,1); int*pr=malloc(sizeof(int)*(sq+2)); int np=0;
  for(ll i=2;i<=sq+1;i++){ if(!sm[i]){pr[np++]=i; for(ll j=i*i;j<=sq+1;j+=i) sm[j]=1;} }
  unsigned short*tau=malloc(sizeof(unsigned short)*B); unsigned char*comp=malloc(B);
  for(int k=k0;k<=k1;k++){
    ll lo=(ll)(k-1)*B+1, hi=(ll)k*B; if(hi>N) hi=N;
    ll len=hi-lo+1; memset(tau,0,sizeof(unsigned short)*len); memset(comp,0,len);
    for(ll d=1; d*d<=hi; d++){
      ll e = (lo+d-1)/d; if(e<d) e=d;
      for(ll m=d*e; m<=hi; m+=d, e++) tau[m-lo] += (e==d)?1:2;
    }
    for(int i=0;i<np;i++){ ll p=pr[i]; if(p*p>hi) break;
      ll s=((lo+p-1)/p)*p; if(s<p*p) s=p*p; for(ll m=s;m<=hi;m+=p) comp[m-lo]=1; }
    if(lo==1) comp[0]=1;
    ll T=0,P=0,minloc=1LL<<60,arg=0,minp=1LL<<60; double lb=1e300; ll lbarg=0;
    for(ll i=0;i<len;i++){ ll n=lo+i; int t=tau[i];
      if((t==2)!=(!comp[i])){fprintf(stderr,"tau/prime disagree at %lld\n",n);return 3;}
      if(n%t==0) T++; if(!comp[i]) P++;
      ll loc=2*T-P; if(loc<minloc){minloc=loc;arg=n;}
      if(!comp[i] && loc<minp) minp=loc;
      if(verbose && loc<=2) printf("V %lld %lld %lld %lld\n",n,T,P,loc);
      if(n>=10000000LL){ double v=(double)loc-2.0*R(n); if(v<lb){lb=v;lbarg=n;} }
    }
    printf("%d %lld %lld %lld %lld %.6f %lld %lld\n",k,T,P,minloc,arg,lb>1e299?0.0:lb,lbarg,minp);
    fflush(stdout);
  }
  return 0;
}
