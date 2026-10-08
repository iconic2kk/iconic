import io, zipfile, json, math, sys
from fractions import Fraction as F
import pandas as pd
Z = zipfile.ZipFile(sys.argv[1]); POT = 5_000_000; rnd = lambda x: math.floor(F(x) + F(1, 2))
q = pd.read_csv(io.BytesIO(Z.read('qcew_aacog_counties_annual_2018_2025.csv')), dtype={'industry_code': str, 'area_fips': str})
q1 = pd.read_csv(io.BytesIO(Z.read('qcew_aacog_counties_2026_q1.csv')), dtype={'industry_code': str, 'area_fips': str})
ro = pd.read_csv(io.BytesIO(Z.read('member_counties.csv')), dtype=str); nm = dict(zip(ro.county_fips, ro.county)); C = sorted(nm.values())
led = pd.read_excel(io.BytesIO(Z.read('breadth_fund_ledger_2020_2025.xlsx')), sheet_name='Draws', header=3)
d25 = {r[2]: int(r[5]) for r in led.itertuples(index=False) if int(r[0]) == 2025}
d24 = {r[2]: int(r[5]) for r in led.itertuples(index=False) if int(r[0]) == 2024}
sel = lambda d, col: d[(d.own_code == 5) & (d.agglvl_code == 76) & d.industry_code.str[:2].isin(['31', '32', '33']) & (d[col] > 0)].assign(county=lambda x: x.area_fips.map(nm))
m = sel(q, 'annual_avg_estabs'); E = {y: m[m.year == y].groupby(['industry_code', 'county']).annual_avg_estabs.sum() for y in range(2018, 2026)}
mq = sel(q1, 'qtrly_estabs'); EQ = mq.groupby(['industry_code', 'county']).qtrly_estabs.sum()
H = lambda s: set(s.index.get_level_values(0))
def eq(s, inds):
    o = {c: F(0) for c in C}
    for i in inds:
        x = s.loc[i]; t = int(x.sum())
        for c, v in x.items(): o[c] += F(POT) / len(inds) * F(int(v), t)
    return {c: rnd(v) for c, v in o.items()}
def verdict(new):
    tp = {c: rnd(F(d25[c] - new[c], 2)) for c in C if F(new[c]) < F(d25[c]) * F(9, 10)}
    return tp, sum(tp.values())
own = lambda y: E[y].groupby(level=1).sum()
paths = {
 'Golden: equal part per industry carried two years running, split by establishment share': eq(E[2025], sorted(H(E[2025]) & H(E[2024]))),
 'Distractor (finance model v2): every industry carried in 2025': eq(E[2025], sorted(H(E[2025]))),
 'Industry carried three years running': eq(E[2025], sorted(H(E[2025]) & H(E[2024]) & H(E[2023]))),
 'Golden method on the newest counts (2026 Q1 file)': eq(EQ, sorted(H(EQ) & H(E[2025]))),
 'Share of the region\'s manufacturing establishments': {c: rnd(F(POT) * F(int(own(2025).get(c, 0)), int(own(2025).sum()))) for c in C},
 'Old projection method: 2025 draw moved with own establishment count': {c: rnd(F(d25[c]) * F(int(own(2025)[c]), int(own(2024)[c]))) for c in C},
 '2025 ledger shares carried forward unchanged': dict(d25),
}
rows = []
for k, v in paths.items():
    tp, tot = verdict(v)
    rows.append({'path': k, 'Wilson': v['Wilson'], 'Gillespie': v['Gillespie'], 'notices': ', '.join(tp) or 'none', 'reserve payout': tot})
print(pd.DataFrame(rows).to_string(index=False))
json.dump(rows, open(sys.argv[2], 'w'), indent=1)
