import pandas as pd, math
from fractions import Fraction as F
R='/tmp/claude-0/-home-user-iconic/118b864e-7445-5af4-819d-cfe4bc0666d5/scratchpad/task15/raw/'
NM={'48013':'Atascosa','48019':'Bandera','48029':'Bexar','48091':'Comal','48163':'Frio','48171':'Gillespie','48187':'Guadalupe','48255':'Karnes','48259':'Kendall','48265':'Kerr','48311':'McMullen','48325':'Medina','48493':'Wilson'}
rows=[]
for c in NM:
    for y in range(2017,2026):
        d=pd.read_csv(f'{R}a{c}_{y}.csv',dtype={'industry_code':str})
        rows.append(d[d.industry_code.str[:2].isin(['31','32','33'])].assign(county=NM[c]))
A=pd.concat(rows)
C=sorted(NM.values()); POT=5_000_000; rnd=lambda x:math.floor(x+F(1,2))
def counts(own=5,lvl=76,col='annual_avg_estabs'):
    d=A[(A.own_code==own)&(A.agglvl_code==lvl)&(A[col]>0)]
    return {y:d[d.year==y].groupby(['industry_code','county'])[col].sum() for y in range(2017,2026)}
E=counts()
def H(E,y): return set(E[y].index.get_level_values(0))
def alloc(E,y,qual,split='share',weight='equal'):
    inds=[i for i in sorted(H(E,y)) if qual(E,y,i)]
    o={c:F(0) for c in C}
    if weight=='invhost':
        w={c:F(0) for c in C}
        for i in inds:
            s=E[y].loc[i]
            for c,v in s.items(): w[c]+=F(int(v),len(s))
        t=sum(w.values()); return {c:F(POT)*w[c]/t for c in C}
    for i in inds:
        s=E[y].loc[i]; t=int(s.sum())
        for c,v in s.items(): o[c]+=F(POT)/len(inds)*(F(int(v),t) if split=='share' else F(1,len(s)))
    return o
q_none=lambda E,y,i:True
q_two=lambda E,y,i:i in H(E,y-1)
q_three=lambda E,y,i:i in H(E,y-1) and i in H(E,y-2)
q_two_of_three=lambda E,y,i:(i in H(E,y-1)) or (i in H(E,y-2))
q_min2=lambda E,y,i:int(E[y].loc[i].sum())>=2
gold={R_:{c:rnd(v) for c,v in alloc(E,R_-1,q_two).items()} for R_ in range(2020,2026)}
def miss(fn):
    n=0
    for R_ in range(2020,2026):
        o=fn(R_-1)
        n+=sum(1 for c in C if abs(rnd(o[c])-gold[R_][c])>1)
    return n
def county_qual(y):
    o={c:F(0) for c in C}; prev=E[y-1]
    keep=E[y][[ (i,c) in prev.index for i,c in E[y].index]]
    inds=sorted(set(keep.index.get_level_values(0)))
    for i in inds:
        s=keep.loc[i]; t=int(s.sum())
        for c,v in s.items(): o[c]+=F(POT)/len(inds)*F(int(v),t)
    return o
def half_entry(y):
    inds=sorted(H(E,y)); wt={i:(F(1) if i in H(E,y-1) else F(1,2)) for i in inds}; T=sum(wt.values())
    o={c:F(0) for c in C}
    for i in inds:
        s=E[y].loc[i]; t=int(s.sum())
        for c,v in s.items(): o[c]+=F(POT)*wt[i]/T*F(int(v),t)
    return o
def prop(y):
    s=E[y].groupby(level=1).sum(); t=int(s.sum()); return {c:F(POT)*F(int(s.get(c,0)),t) for c in C}
E0=counts(own=0); E3=counts(lvl=75)
tests={
 'H1 + H2 (golden)':lambda y:alloc(E,y,q_two),
 'H1, no qualification':lambda y:alloc(E,y,q_none),
 'H1, hosted three years running':lambda y:alloc(E,y,q_three),
 'H1, hosted in either of two prior years':lambda y:alloc(E,y,q_two_of_three),
 'H1, industry needs 2+ establishments':lambda y:alloc(E,y,q_min2),
 'H1, entry-year industries at half weight':half_entry,
 'H1, county-level qualification':county_qual,
 'equal per industry split equally among hosts, H2':lambda y:alloc(E,y,q_two,split='equal'),
 'establishments / hosting counties, H2':lambda y:alloc(E,y,q_two,weight='invhost'),
 'own share of mfg establishments':prop,
 'H1 + H2 on all ownerships':lambda y:alloc(E0,y,q_two),
 'H1 + H2 on 3-digit industries':lambda y:alloc(E3,y,q_two),
 'H1 + H2 with data year = round year':lambda y:alloc(E,y+1,q_two) if y+1<=2025 else {c:F(0) for c in C},
}
for k,f in tests.items(): print(f'{miss(f):3d} of 78 ledger lines missed  {k}')
