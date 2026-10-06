"""Compute every golden number for MON-021 v2 from the shipped inputs."""
import json, os
import pandas as pd
from replay import load_balance, evaluable, pages, load_rota, CANDIDATES, FORECAST_NOT_COMPARABLE, INPUTS

df = load_balance()
e_all = evaluable(df)
v2 = e_all[~e_all.ba.isin(FORECAST_NOT_COMPARABLE)]
rota = load_rota()
months = list(rota.index)
cap = rota["triage_capacity_pages"]

rows, summary = [], {}
imp = v2[v2.imputed]
for t in CANDIDATES:
    p = pages(v2, t)
    pm = p.groupby("month").size().reindex(months, fill_value=0)
    miss = imp[~(imp.dev > t / 100)]
    mm = miss.groupby("month").size().reindex(months, fill_value=0)
    im = imp.groupby("month").size().reindex(months, fill_value=0)
    for m in months:
        rows.append(dict(threshold_pct=t, month=m, pages=int(pm[m]), triage_capacity_pages=int(cap[m]),
                         within_capacity="Y" if pm[m] <= cap[m] else "N",
                         eia_imputed_hours_evaluated=int(im[m]), eia_imputed_hours_missed=int(mm[m])))
    over = [m for m in months if pm[m] > cap[m]]
    head = (cap - pm)
    summary[t] = dict(total=int(pm.sum()), peak=int(pm.max()), peak_month=pm.idxmax(), months_over=len(over),
                      first_over=over[0] if over else None, first_over_pages=int(pm[over[0]]) if over else None,
                      first_over_cap=int(cap[over[0]]) if over else None,
                      min_headroom_month=head.idxmin(), min_headroom=int(head.min()),
                      missed=len(miss), missed_rows=miss[["ba","utc","d","dfc","d_imp","dev"]].astype(str).values.tolist()[:3],
                      passes=(not over) and len(miss) == 0)
rep = pd.DataFrame(rows)
chosen = min(t for t in CANDIDATES if summary[t]["passes"])
# fleet-wide (wrong-scope) contrast
imp_all = e_all[e_all.imputed]
fleet = {}
for t in CANDIDATES:
    pm = pages(e_all, t).groupby("month").size().reindex(months, fill_value=0)
    fleet[t] = dict(peak=int(pm.max()), months_over=int((pm > cap).sum()), missed=int((~(imp_all.dev > t/100)).sum()))
v1 = pd.read_csv(os.path.join(INPUTS, "MON-021_v1_page_history.csv"), skiprows=1)
v1_nc = v1[v1.ba.isin(FORECAST_NOT_COMPARABLE)]
facts = dict(chosen=chosen, min_imputed_dev=float(imp.dev.min()), summary=summary, fleet=fleet,
             evaluated_bas=int(v2.ba.nunique()), evaluated_hours=int(len(v2)), imputed_evaluated=int(len(imp)),
             imputed_not_evaluable=int(df[df.d.notna() & df.d_imp.notna() & ~(df.dfc > 0) & ~df.ba.isin(FORECAST_NOT_COMPARABLE)].shape[0]),
             v1_total=int(len(v1)), v1_from_nc=int(len(v1_nc)), v1_nc_by_ba=v1_nc.ba.value_counts().to_dict(),
             v1_bas=int(v1.ba.nunique()),
             window_rows_excluded_after=str(df.utc.max()),
             v2_by_ba_chosen=pages(v2, chosen).ba.value_counts().head(5).to_dict())
os.makedirs("../golden", exist_ok=True)
rep.to_csv("replay_table.csv", index=False)
json.dump(facts, open("facts.json", "w"), indent=1, default=str)
print(json.dumps(facts, indent=1, default=str))
