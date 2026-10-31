# merge block output, cross-check against PARI primepi, write checkpoint
import cypari2, hashlib, sys
pari = cypari2.Pari()
rows=[tuple(map(int,l.split())) for l in open(sys.argv[1])]
assert [r[0] for r in rows]==list(range(1,1001))
T=P=0; out=[]; gmin_prime=1<<60; gmin_all=[]; offs={}
for k,t,q,mp,ma in rows:
    offs[k]=(T,P)
    mk=2*T-P+mp; gmin_prime=min(gmin_prime,mk)
    gmin_all.append((2*T-P+ma,k))
    T+=t;P+=q
    if k==1000: pass
    pp=int(pari(f'primepi({k*10**6})'))
    assert pp==P,(k,pp,P)   # independent counter agrees at every checkpoint
    out.append(f"{k*10**6} {T} {P} {mk}\n")
open('checkpoint.txt','w').write(''.join(out))
print(hashlib.sha256(''.join(out).encode()).hexdigest())
print('min over primes up to 1e9 (global running):',gmin_prime)
print('min over all n by block (from block 2 on):',min(gmin_all[1:]))
print('block1 min all n:',gmin_all[0])
