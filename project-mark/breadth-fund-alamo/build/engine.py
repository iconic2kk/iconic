"""Shared fund engine used only by the pack builder (the golden solution is separate and reads the zip)."""
import pandas as pd, math
from fractions import Fraction as F
POT = 5_000_000
NM = {'48013':'Atascosa','48019':'Bandera','48029':'Bexar','48091':'Comal','48163':'Frio','48171':'Gillespie','48187':'Guadalupe',
      '48255':'Karnes','48259':'Kendall','48265':'Kerr','48311':'McMullen','48325':'Medina','48493':'Wilson'}
C = sorted(NM.values())
rnd = lambda x: math.floor(F(x) + F(1, 2))
def load(raw):
    rows = []
    for c in NM:
        for y in range(2017, 2026):
            d = pd.read_csv(f'{raw}/a{c}_{y}.csv', dtype={'industry_code': str})
            d = d[(d.own_code == 5) & (d.agglvl_code == 76) & d.industry_code.str[:2].isin(['31', '32', '33']) & (d.annual_avg_estabs > 0)]
            rows.append(d.assign(county=NM[c]))
    a = pd.concat(rows)
    return {y: a[a.year == y].groupby(['industry_code', 'county']).annual_avg_estabs.sum() for y in range(2017, 2026)}
def hosted(E, y): return set(E[y].index.get_level_values(0))
def alloc(E, y, qualify=True):
    inds = sorted(hosted(E, y) & hosted(E, y - 1)) if qualify else sorted(hosted(E, y))
    o = {c: F(0) for c in C}
    for i in inds:
        s = E[y].loc[i]; t = int(s.sum())
        for c, v in s.items(): o[c] += F(POT) / len(inds) * F(int(v), t)
    return {c: rnd(v) for c, v in o.items()}, len(inds)
def estabs(E, y): return {c: int(E[y].groupby(level=1).sum().get(c, 0)) for c in C}
def transition(prev, new):
    return {c: (rnd(F(prev[c] - new[c], 2)) if F(new[c]) < F(prev[c]) * F(9, 10) else 0) for c in C}
