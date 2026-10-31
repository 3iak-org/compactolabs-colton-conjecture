# brute force, written separately: tau by counting divisors with trial division (n<=1e5), primes by trial division
import math, sys
N=100000
def tau(n):
    c=0; r=math.isqrt(n)
    for d in range(1,r+1):
        if n%d==0: c+=2 if d*d!=n else 1
    return c
T=0;P=0;bad=[];small=[];minm=None;checks={}
for n in range(1,N+1):
    t=tau(n)
    if n%t==0: T+=1
    if t==2: P+=1
    m=2*T-P
    if m<0: bad.append(n)
    if n<=1000 and m<=2: small.append((n,m))
    if n in (10,100,1000,10000,100000): checks[n]=(T,P)
print('violations n<=1e5:',bad)
print('checks (n:(T,pi)):',checks)
print('n<=1000 with 2T-pi<=2:',small)
print('equality n<=1e5:',[n for n,_ in small if _==0])
