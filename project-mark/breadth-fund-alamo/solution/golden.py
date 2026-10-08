"""Golden solution: Breadth Fund 2026 round. Reads only inputs.zip (or an unzipped folder) and writes figures.json."""
import sys, io, zipfile, json, math, os
from fractions import Fraction as F
import pandas as pd
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'inputs.zip')
def read(name, **kw):
    if src.endswith('.zip'):
        with zipfile.ZipFile(src) as z: return z.read(name)
    return open(os.path.join(src, name), 'rb').read()
q = pd.read_csv(io.BytesIO(read('qcew_aacog_counties_annual_2018_2025.csv')), dtype={'industry_code': str, 'area_fips': str})
roster = pd.read_csv(io.BytesIO(read('member_counties.csv')), dtype=str)
name = dict(zip(roster.county_fips, roster.county)); C = sorted(name.values())
led = pd.read_excel(io.BytesIO(read('breadth_fund_ledger_2020_2025.xlsx')), sheet_name='Draws', header=3)
POT = 5_000_000
rnd = lambda x: math.floor(F(x) + F(1, 2))
# charter 3.4: private (own_code 5), four-digit manufacturing industries (agglvl 76, NAICS 31-33), annual average establishments
m = q[(q.own_code == 5) & (q.agglvl_code == 76) & q.industry_code.str[:2].isin(['31', '32', '33']) & (q.annual_avg_estabs > 0)].copy()
m['county'] = m.area_fips.map(name)
E = {y: m[m.year == y].groupby(['industry_code', 'county']).annual_avg_estabs.sum() for y in range(2018, 2026)}
hosted = lambda y: set(E[y].index.get_level_values(0))
def round_draws(R):
    y = R - 1
    inds = sorted(hosted(y) & hosted(y - 1))          # an industry counts once the region has carried it two years running
    out = {c: F(0) for c in C}; detail = []
    for i in inds:
        s = E[y].loc[i]; tot = int(s.sum())
        for c, v in s.items():
            part = F(POT) / len(inds) * F(int(v), tot)   # equal part per industry, split by the counties' establishment shares
            out[c] += part; detail.append((R, i, c, int(v), tot, float(part)))
    return {c: rnd(v) for c, v in out.items()}, inds, detail
draws, inds, details = {}, {}, []
for R in range(2020, 2027):
    draws[R], inds[R], d = round_draws(R); details += d
# backtest against every ledger line
bt = []
for _, r in led.iterrows():
    bt.append((int(r['Round']), r['County'], int(r['Draw ($)']), draws[int(r['Round'])][r['County']]))
assert all(a == b for _, _, a, b in bt), 'backtest failed'
prev, new = draws[2025], draws[2026]
notice = {c: (rnd(F(prev[c] - new[c], 2)) if F(new[c]) < F(prev[c]) * F(9, 10) else 0) for c in C}
# the finance office's two projections, rebuilt
est = lambda y: m[m.year == y].groupby('county').annual_avg_estabs.sum()
proj25 = {c: rnd(F(int(draws[2024][c])) * F(int(est(2024)[c]), int(est(2023)[c]))) for c in C}
def all_hosted(y):
    ii = sorted(hosted(y)); o = {c: F(0) for c in C}
    for i in ii:
        s = E[y].loc[i]; t = int(s.sum())
        for c, v in s.items(): o[c] += F(POT) / len(ii) * F(int(v), t)
    return {c: rnd(v) for c, v in o.items()}, ii
v2, v2_inds = all_hosted(2025)
first_year = sorted(set(v2_inds) - set(inds[2026]))
v2_notice = {c: (rnd(F(prev[c] - v2[c], 2)) if F(v2[c]) < F(prev[c]) * F(9, 10) else 0) for c in C}
v2_back = {R: all_hosted(R - 1)[0] for R in range(2020, 2026)}
v2_miss = {R: sum(1 for c in C if v2_back[R][c] != draws[R][c]) for R in v2_back}
# Medina's 2025 drop
med = {R: dict((i, (cnt, tot, round(p, 2))) for (RR, i, c, cnt, tot, p) in details if RR == R and c == 'Medina') for R in (2024, 2025)}
lost = sorted(set(med[2024]) - set(med[2025]))
out = {
 'draws': {str(R): draws[R] for R in draws}, 'qualifying_industries': {str(R): len(inds[R]) for R in inds},
 'backtest_lines': len(bt), 'backtest_mismatches': sum(1 for _, _, a, b in bt if a != b),
 'draws_2026': new, 'change_2026_pct': {c: round((new[c] - prev[c]) / prev[c] * 100, 2) for c in C},
 'notices_2026': {c: v for c, v in notice.items() if v}, 'reserve_call_2026': sum(notice.values()),
 'model_v2_2026': v2, 'model_v2_notices': {c: v for c, v in v2_notice.items() if v}, 'model_v2_reserve_call': sum(v2_notice.values()),
 'model_v2_backtest_mismatched_counties_by_round': v2_miss, 'first_year_industries_2025': first_year,
 'first_year_detail': {i: E[2025].loc[i].to_dict() for i in first_year},
 'projection_2025': proj25, 'projection_2025_medina_miss': draws[2025]['Medina'] - proj25['Medina'],
 'medina_industries_lost_2025_round': {i: med[2024][i] for i in lost},
 'medina_2024_parts': med[2024], 'medina_2025_parts': med[2025],
 'part_per_industry': {str(R): round(POT / len(inds[R]), 2) for R in inds},
}
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'figures.json'), 'w'), indent=1)
print('backtest', out['backtest_lines'], 'lines,', out['backtest_mismatches'], 'mismatches')
print('2026 draws', new); print('notices', out['notices_2026'], 'reserve', out['reserve_call_2026'])
print('model v2 notices', out['model_v2_notices'], out['model_v2_reserve_call'], 'v2 backtest mismatched counties', v2_miss)
print('first-year industries', first_year, out['first_year_detail'])
print('Medina lost', out['medina_industries_lost_2025_round'], 'proj miss', out['projection_2025_medina_miss'])
print('qualifying', out['qualifying_industries'], 'part', out['part_per_industry'])
