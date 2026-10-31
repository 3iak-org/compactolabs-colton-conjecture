# usage: moments.py list.txt.gz pi.txt.gz > moments.txt   (list = a g per line, a<=1e8)
import sys,gzip
from flint import arb,ctx
from collections import Counter
ctx.prec=300
Ms=[16694,166944,28653696]
A=[];G=[];P=[]
for l,p in zip(gzip.open(sys.argv[1],'rt'),gzip.open(sys.argv[2],'rt')):
    a,g=map(int,l.split()); 
    if a>Ms[-1]: break
    A.append(a);G.append(g);P.append(int(p))
def show(x):  # enclosure + midpoint, 35 digits
    lo=x.mid()-x.rad(); hi=x.mid()+x.rad()
    return "[%s, %s] mid=%s rad<=%s"%(lo.str(35,radius=False),hi.str(35,radius=False),x.mid().str(35,radius=False),x.rad().str(3,radius=False))
print("# arb ball arithmetic, prec=300 bits; every a, ln a is an arb enclosure; sums are balls. Enclosure printed = mid -/+ rad, rounded outward only to 35 digits display (display rounding is NOT outward; rad shown separately).")
for M in Ms:
    idx=[i for i,a in enumerate(A) if a<=M]
    n=len(idx); beta=sum(P[i] for i in idx)
    print("\nM=%d\nN=%d\nbeta=%d\nB=%d\nmax_G=%d\nmax_a_times_g=%d (a=%d)"%(M,n,beta,beta+n,A[idx[-1]],max(A[i]*G[i] for i in idx),max(idx,key=lambda i:A[i]*G[i]) and A[max(idx,key=lambda i:A[i]*G[i])]))
    L=[arb(0)]*7
    for i in idx:
        a=A[i]; ln=arb(a).log(); t=arb(1)/a; 
        for k in range(7): L[k]+=t; t*=ln
    for k in range(7): print("L_%d = %s"%(k,show(L[k])))
    if M==Ms[-1]:
        c=Counter(A[i]//G[i] for i in idx if G[i]*128>M)
        print("cofactors a/g(a) for g>M/128 (M/128=%s): %d distinct, %d elements"%(M/128,len(c),sum(c.values())))
        print(" ".join("%d:%d"%kv for kv in sorted(c.items())))
