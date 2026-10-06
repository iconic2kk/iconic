"""Compute every golden number for the MON-021 v2 go-live replay from the shipped inputs."""
import json, os
import pandas as pd
from replay import (load_history, in_window, evaluable, pages, mon014_pages, mon014_flags, load_rota,
                    CANDIDATES, FORECAST_NOT_COMPARABLE, INPUTS)

hist = load_history()
df = in_window(hist)
e_all = evaluable(df)
v2 = e_all[~e_all.ba.isin(FORECAST_NOT_COMPARABLE)]
rota = load_rota(); months = list(rota.index); cap = rota["triage_capacity_pages"]

p14 = mon014_pages(hist, FORECAST_NOT_COMPARABLE)
m14 = p14.groupby("month").size().reindex(months, fill_value=0)
imp = v2[v2.imputed]
rows, S = [], {}
for t in CANDIDATES:
    pv = pages(v2, t)
    mv = pv.groupby("month").size().reindex(months, fill_value=0)
    tot = mv + m14
    miss = imp[~(imp.dev > t / 100)]
    mm = miss.groupby("month").size().reindex(months, fill_value=0)
    im = imp.groupby("month").size().reindex(months, fill_value=0)
    for m in months:
        rows.append(dict(threshold_pct=t, month=m, oncall_pages=int(tot[m]), mon021_v2_pages=int(mv[m]),
                         mon014_pages=int(m14[m]), triage_capacity_pages=int(cap[m]),
                         within_capacity="Y" if tot[m] <= cap[m] else "N",
                         eia_imputed_hours_evaluated=int(im[m]), eia_imputed_hours_missed=int(mm[m])))
    over = [m for m in months if tot[m] > cap[m]]
    S[t] = dict(total=int(tot.sum()), v2_total=int(mv.sum()), peak=int(tot.max()), peak_month=tot.idxmax(),
                peak_cap=int(cap[tot.idxmax()]), months_over=len(over), over=over,
                max_excess=int((tot - cap).max()), max_excess_month=(tot - cap).idxmax(),
                v2_alone_months_over=int((mv > cap).sum()), v2_alone_peak=int(mv.max()),
                missed=len(miss), missed_rows=miss[["ba", "utc", "d", "dfc", "d_imp", "dev"]].astype(str).values.tolist(),
                cap_pass=not over, cov_pass=len(miss) == 0)
passing = [t for t in CANDIDATES if S[t]["cap_pass"] and S[t]["cov_pass"]]
decision = min(passing) if passing else None
# smallest rota change that lets a candidate ship: only coverage-passing candidates can ship
extra = {}
for t in CANDIDATES:
    if not S[t]["cov_pass"]: continue
    r = [x for x in rows if x["threshold_pct"] == t]
    extra[t] = {x["month"]: x["oncall_pages"] - x["triage_capacity_pages"] for x in r if x["oncall_pages"] > x["triage_capacity_pages"]}
best = min(extra, key=lambda t: sum(extra[t].values()))
# binding-month breakdown for the best candidate
bm = list(extra[best])[0] if len(extra[best]) == 1 else max(extra[best], key=extra[best].get)
pv = pages(v2, best)
bd_v2 = pv[pv.month == bm].ba.value_counts().to_dict()
bd_14 = p14[p14.month == bm].ba.value_counts().to_dict()
v1 = pd.read_csv(os.path.join(INPUTS, "MON-021_v1_page_history.csv"), skiprows=1)
fl = mon014_flags(hist, FORECAST_NOT_COMPARABLE); fl_w = in_window(fl)
facts = dict(decision=decision, passing=passing, summary=S, extra_needed=extra, best_flip=best,
             best_flip_total=sum(extra[best].values()), binding_month=bm,
             binding_breakdown_v2=bd_v2, binding_breakdown_mon014=bd_14,
             mon014_by_month=m14.to_dict(), mon014_total=int(m14.sum()), mon014_by_ba=p14.ba.value_counts().to_dict(),
             mon014_kinds=p14.kinds.value_counts().to_dict(),
             mon014_ceiling_flags=fl_w[fl_w.kind == "ceiling"][["ba", "utc", "d", "ceiling"]].astype(str).values.tolist(),
             evaluated_bas=int(v2.ba.nunique()), imputed_evaluated=int(len(imp)),
             min_imputed_dev=float(imp.dev.min()),
             v1_total=int(len(v1)), v1_from_nc=int(v1.ba.isin(FORECAST_NOT_COMPARABLE).sum()),
             v1_by_month=v1.page_date_utc.str[:7].value_counts().sort_index().to_dict())
rep = pd.DataFrame(rows)
rep.to_csv("replay_table.csv", index=False)
json.dump(facts, open("facts.json", "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in facts.items() if k != "summary"}, indent=1, default=str))
for t in CANDIDATES:
    s = S[t]; print(t, {k: s[k] for k in ["peak", "peak_month", "peak_cap", "months_over", "over", "missed", "v2_alone_months_over", "v2_alone_peak", "total"]})
