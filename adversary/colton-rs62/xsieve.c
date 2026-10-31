/* adversary/colton-rs62/xsieve.c - exact T(n), pi(n) past 1e9, against the RS62 claim.
   Method (as adversary/colton/dsieve.c, not the team's):
   - tau(n) by DIVISOR-PAIR counting: for each d<=sqrt(hi), each m=d*e in the segment
     with e>=d adds 2 (1 if e==d). No factorisation.
   - primes by a separate segmented Eratosthenes bitmap; asserts tau==2 <=> prime.
   Block k covers ((k-1)B, kB]. Per block prints, with T_l,P_l counted from block start:
     k T_b P_b  minloc argmin   lb lbarg   lowmin upmin
   minloc = min_n (2T_l(n)-P_l(n));
   lb     = min_n (2T_l(n)-P_l(n) - 2R(n)), R(n) = (n/u) g_S(u) - beta for the stage set
            the RS62 theorem assigns to n (pieces [1e9,1e10],(1e10,1e11],(1e11,1e12], tail);
   lowmin = min over primes q>59 in block of P_l(q) - f(q), f(x)=(x/ln x)(1+1/(2 ln x))
            [global (3.1) slack at x->q^- is P_off + lowmin - 1];
   upmin  = min over primes q in block of F(q) - P_l(q), F(x)=(x/ln x)(1+3/(2 ln x))
            [global (3.2) slack at x=q is upmin - P_off].
   long double throughout for R, f, F: an attack, not a certificate. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef long long ll; typedef long double ld;
static ld C[4][7], BETA[4];
static ld R(ll n){
  if(n<1000000000LL) return -1e300L;
  int s = n<=10000000000LL?0 : n<=100000000000LL?1 : n<=1000000000000LL?2 : 3;
  ld u=logl((ld)n), g=0, up=1; for(int m=0;m<7;m++){g+=C[s][m]/up; up*=u;}
  return (ld)n/u*g-BETA[s];
}
int main(int argc,char**argv){
  ll N=atoll(argv[1]), B=atoll(argv[2]); ll k0=atoll(argv[3]), k1=atoll(argv[4]);
  FILE*cf=fopen(argv[5],"r"); if(!cf) return 9;
  for(int s=0;s<4;s++){ for(int i=0;i<7;i++) if(fscanf(cf,"%Lf",&C[s][i])!=1) return 9;
    if(fscanf(cf,"%Lf",&BETA[s])!=1) return 9; }
  fclose(cf);
  ll sq=(ll)sqrtl((ld)N)+2; while(sq*sq>N) sq--;
  char*sm=calloc(sq+2,1); int*pr=malloc(sizeof(int)*(sq+2)); int np=0;
  for(ll i=2;i<=sq+1;i++){ if(!sm[i]){pr[np++]=i; for(ll j=i*i;j<=sq+1;j+=i) sm[j]=1;} }
  unsigned short*tau=malloc(sizeof(unsigned short)*B); unsigned char*comp=malloc(B);
  for(ll k=k0;k<=k1;k++){
    ll lo=(k-1)*B+1, hi=k*B; if(hi>N) hi=N;
    ll len=hi-lo+1; memset(tau,0,sizeof(unsigned short)*len); memset(comp,0,len);
    for(ll d=1; d*d<=hi; d++){
      ll e=(lo+d-1)/d; if(e<d) e=d;
      ll m=d*e; if(m>hi) continue;
      if(e==d){ tau[m-lo]+=1; m+=d; }
      for(; m<=hi; m+=d) tau[m-lo]+=2;
    }
    for(int i=0;i<np;i++){ ll p=pr[i]; if(p*p>hi) break;
      ll s=((lo+p-1)/p)*p; if(s<p*p) s=p*p; for(ll m=s;m<=hi;m+=p) comp[m-lo]=1; }
    if(lo==1) comp[0]=1;
    ll T=0,P=0,minloc=1LL<<60,arg=0,lbarg=0; ld lb=1e300L, lowmin=1e300L, upmin=1e300L;
    for(ll i=0;i<len;i++){ ll n=lo+i; int t=tau[i]; int isp=!comp[i];
      if((t==2)!=isp){fprintf(stderr,"tau/prime disagree at %lld\n",n);return 3;}
      if(n%t==0) T++;
      if(isp){ P++; ld v=logl((ld)n), x=(ld)n/v;
        if(n>59){ ld s=(ld)P - x*(1+0.5L/v); if(s<lowmin) lowmin=s; }
        { ld s=x*(1+1.5L/v)-(ld)P; if(s<upmin) upmin=s; } }
      ll loc=2*T-P; if(loc<minloc){minloc=loc;arg=n;}
      if(n>=1000000000LL){ ld v=(ld)loc-2.0L*R(n); if(v<lb){lb=v;lbarg=n;} }
    }
    printf("%lld %lld %lld %lld %lld %.6Lf %lld %.6Lf %.6Lf\n",k,T,P,minloc,arg,lb>1e299L?0.0L:lb,lbarg,
           lowmin>1e299L?0.0L:lowmin, upmin>1e299L?0.0L:upmin);
    fflush(stdout);
  }
  return 0;
}
