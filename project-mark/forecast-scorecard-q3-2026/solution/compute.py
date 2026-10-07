import json, os
import pandas as pd
from scorecard import load, scored, error_pct, flags, INPUTS

b = flags(load())
reg = pd.read_csv(os.path.join(INPUTS, "forecast_change_notices.csv"), skiprows=1)
hist = pd.read_csv(os.path.join(INPUTS, "forecast_scorecard_published_2024Q3_2026Q2.csv"), skiprows=1)
ctrl = hist.set_index(["period_type", "period", "ba"])["forecast_error_pct"]

def bed(days, anchor="effective_reporting_day", withdrawn=False):
    r = reg if withdrawn else reg[reg.status == "active"]; m = pd.Series(False, index=b.index)
    for x in r.itertuples():
        e = pd.Timestamp(str(getattr(x, anchor))[:10])
        m |= (b.ba == x.ba) & (b.ldate >= e) & (b.ldate <= e + pd.Timedelta(days=days - 1))
    return m
def rest_of_month():
    m = pd.Series(False, index=b.index)
    for x in reg[reg.status == "active"].itertuples():
        e = pd.Timestamp(x.effective_reporting_day)
        m |= (b.ba == x.ba) & (b.ldate >= e) & (b.ldate.dt.to_period("M") == e.to_period("M"))
    return m
def evaluate(mask, mkey="month"):
    x = b[mask]; m = error_pct(x, mkey); q = error_pct(x, "quarter")
    ok = sum(int(((m if pt == "month" else q).round(1).get((ba, p))) == v) for (pt, p, ba), v in ctrl.items())
    r = q[[i for i in q.index if i[1] == "2026Q3"]].droplevel(1)
    r = r[~r.index.isin(["WACM", "WAUW"])].sort_values(ascending=False)
    return ok, [(k, round(v, 2)) for k, v in r.head(7).items()]
ev = b.evaluable; base = ev & ~b.imputed & ~b.flatline & ~b.dst_day
V = {
 "golden": base & ~b.bedding_in,
 "bedding-in counting withdrawn notices": base & ~bed(14, withdrawn=True),
 "no flatline screen": ev & ~b.imputed & ~b.dst_day & ~b.bedding_in,
 "bedding-in 13 days": base & ~bed(13),
 "bedding-in to end of month": base & ~rest_of_month(),
 "bedding-in from received date": base & ~bed(14, anchor="received_utc"),
 "no bedding-in": base,
 "no DST-day exclusion": ev & ~b.imputed & ~b.flatline & ~b.bedding_in,
 "keep EIA-imputed hours": ev & ~b.flatline & ~b.dst_day & ~b.bedding_in,
 "no screens, local reporting month": ev,
}
res = {k: dict(zip(["match", "top7"], evaluate(m))) for k, m in V.items()}
res["no screens, UTC month"] = dict(zip(["match", "top7"], evaluate(ev, "m_utc")))
for k, v in res.items(): print(f"{k:40s} {v['match']}/{len(ctrl)} {v['top7']}")
json.dump({k: dict(v, of=len(ctrl)) for k, v in res.items()}, open("variants.json", "w"), indent=1)
s = scored(b); m = error_pct(s, "month"); q = error_pct(s, "quarter")
g = pd.DataFrame({"q3_raw": q[[i for i in q.index if i[1] == "2026Q3"]].droplevel(1)})
for mm in ["2026-07", "2026-08", "2026-09"]:
    g[mm] = m[[i for i in m.index if i[1] == mm]].droplevel(1)
g = g[~g.index.isin(["WACM", "WAUW"])].sort_values("q3_raw", ascending=False)
g["rank"] = range(1, len(g) + 1); g["watch"] = g["rank"] <= 5
g.to_csv("golden_q3.csv"); print(g.head(8).round(3).to_string())
