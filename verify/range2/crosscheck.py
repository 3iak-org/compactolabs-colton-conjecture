import cypari2
pari=cypari2.Pari(); pari.allocatemem(2*10**9)
bad=0
for l in open("checkpoints.txt"):
    n,T,p,m=map(int,l.split())
    if int(pari.primepi(n))!=p: bad+=1; print("pi mismatch",n)
print("primepi mismatches over 1000 checkpoints:",bad)
rows={int(l.split()[0]):l.split() for l in open("checkpoints.txt")}
print([int(pari.primepi(10**k)) for k in range(1,10)])
