# Combine raw per-block output into the checkpoint file and summary.
import sys,glob,hashlib
rows={}
for f in glob.glob('results/range/raw/w*.txt'):
    for l in open(f):
        k,Tb,pib,ml,ap=map(int,l.split()); rows[k]=(Tb,pib,ml,ap)
assert sorted(rows)==list(range(1,1001))
T=pi=0; out=["# k n=k*10^6 T(n) pi(n) minmargin argmin_p",
 "# minmargin = min over primes p in ((k-1)*10^6, k*10^6] of 2T(p)-pi(p); argmin_p = smallest such p attaining it"]
best=None
for k in range(1,1001):
    Tb,pib,ml,ap=rows[k]
    mm=2*T-pi+ml          # offset + local margin
    T+=Tb; pi+=pib
    out.append(f"{k} {k*10**6} {T} {pi} {mm} {ap}")
    if k>=2 and (best is None or mm<best[0]): best=(mm,ap,k)
    if k==1: m1=(T,pi)
txt="\n".join(out)+"\n"
open('results/range/checkpoints-annotated.txt','w').write(txt)
plain="".join(" ".join(l.split()[1:5])+"\n" for l in out if l[0]!="#")
open('results/range/checkpoints.txt','w').write(plain)
txt=txt
print("sha256",hashlib.sha256(plain.encode()).hexdigest())
print("margin at n=1e6:",2*m1[0]-m1[1],"min over primes in (1e6,1e9]:",best,"final",T,pi)
