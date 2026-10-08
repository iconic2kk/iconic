"""Golden numbers for the Travis County tracker-drop root cause task (QCEW, NAICS 2022 conversion)."""
import pandas as pd, sys, os
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'inputs')
q = pd.read_csv(os.path.join(D, 'qcew_travis_county_quarterly_2021_2023.csv'), dtype=str)
a = pd.read_csv(os.path.join(D, 'qcew_travis_county_annual_2021_2023.csv'), dtype=str)
q = q[q.own_code == '5']; a = a[a.own_code == '5']
q['m3'] = q.month3_emplvl.astype(int); a['emp'] = a.annual_avg_emplvl.astype(int)
def Q(code, yq):
    y, k = yq.split('Q'); r = q[(q.industry_code == code) & (q.year == y) & (q.qtr == k)]
    return int(r.m3.iloc[0]) if len(r) else 0
def A(code, y):
    r = a[(a.industry_code == code) & (a.year == str(y))]
    return int(r.emp.iloc[0]) if len(r) else 0
OLD, NEW = ['511', '515', '519'], ['513', '516', '519']   # closed under the Census 2017->2022 concordance
qs = [f'{y}Q{k}' for y in (2021, 2022, 2023) for k in (1, 2, 3, 4)]
print('quarter   519  closed_group  tracker(518+519+5415)  like-for-like(518+5415+group)  sector51')
for t in qs:
    grp = sum(Q(c, t) for c in (OLD if t < '2022' else NEW))
    trk = Q('518', t) + Q('519', t) + Q('5415', t)
    lfl = Q('518', t) + Q('5415', t) + grp
    print(f'{t}  {Q("519", t):5d}  {grp:6d}  {trk:6d}  {lfl:6d}  {Q("51", t):6d}')
print('\n2021 annual 519 detail:', {c: A(c, 2021) for c in ['519110', '519120', '519130', '519190']})
print('2021Q4 519 detail (m3):', {c: Q(c, '2021Q4') for c in ['519110', '519120', '519130', '519190']})
print('2022Q1 new-code detail (m3):', {c: Q(c, '2022Q1') for c in ['513', '516', '519', '516210', '519210', '519290', '513210']})
for lbl, s, e in [('tracker 2021Q4->2023Q4', '2021Q4', '2023Q4'), ('2021Q4->2022Q1', '2021Q4', '2022Q1'), ('2022Q4->2023Q4', '2022Q4', '2023Q4')]:
    g = lambda t: sum(Q(c, t) for c in (OLD if t < '2022' else NEW))
    trk = lambda t: Q('518', t) + Q('519', t) + Q('5415', t)
    lfl = lambda t: Q('518', t) + Q('5415', t) + g(t)
    print(f'{lbl}: tracker {trk(e)-trk(s):+d}, like-for-like {lfl(e)-lfl(s):+d}, group {g(e)-g(s):+d}, 519 {Q("519",e)-Q("519",s):+d}, 5415 {Q("5415",e)-Q("5415",s):+d}, 518 {Q("518",e)-Q("518",s):+d}')
