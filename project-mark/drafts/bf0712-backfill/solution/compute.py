"""Golden numbers and per-incident evidence for BF-0712, from the shipped inputs only."""
import json, os
import numpy as np
import pandas as pd
from data import load_balance, load_interchange, neighbour_ti, INPUTS

bal = load_balance(); ich = load_interchange()
job = pd.read_csv(os.path.join(INPUTS, "BF-0712_backfill_job.csv"), skiprows=1)

# Verdicts (expert reading of the evidence computed below)
V = {
 "01": ("leave", "real load", "Hurricane Helene outage: demand, generation and neighbour-confirmed interchange fall together, then recover over days"),
 "02": ("backfill", "demand error", "demand reported at about zero while the BA's own generation and interchange show load being served"),
 "03": ("backfill", "demand error", "demand, generation and interchange all reported as zero for a full day while neighbours report flows into IID"),
 "04": ("backfill", "demand error", "generation reading collapses while interchange (confirmed by neighbours) is unchanged, so demand is understated"),
 "05": ("backfill", "demand error", "demand, generation and interchange all reported as zero while neighbours report flows into IID"),
 "06": ("backfill", "demand error", "demand, generation and interchange all reported as zero while neighbours report flows into IID"),
 "07": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; the day-ahead forecast is the outlier"),
 "08": ("backfill", "demand error", "demand, generation and interchange all reported as zero while neighbours report flows into IID"),
 "09": ("backfill", "demand error", "demand, generation and interchange all reported as zero while neighbours report flows into IID"),
 "10": ("leave", "real load", "demand above its prior week with neighbour-confirmed extra imports; consistent load, forecast too low"),
 "11": ("backfill", "demand error", "demand reported as zero while generation and interchange stay at normal levels"),
 "12": ("leave", "forecast error", "forecast stuck at 692 MW for the whole day; demand in line with its prior week"),
 "13": ("backfill", "demand error", "demand, generation and interchange all reported as zero while neighbours report flows into IID"),
 "14": ("leave", "forecast error", "forecast stuck at 692 MW for the whole day; demand in line with its prior week"),
 "15": ("backfill", "demand error", "demand and generation reported as zero while interchange shows normal imports"),
 "16": ("backfill", "demand error", "generation reading drops to about 2 MW while interchange is unchanged, so demand is understated"),
 "17": ("backfill", "demand error", "demand reported as zero while generation and interchange stay at normal levels"),
 "18": ("backfill", "demand error", "interchange reported as exactly zero for four days while neighbours report about 1,100 MW of imports; generation also collapses"),
 "19": ("leave", "real load", "cold-weather demand above its prior week with generation up and neighbour-confirmed interchange; forecast too low"),
 "20": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "21": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "22": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "23": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "24": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "25": ("leave", "real load", "demand above its prior week with neighbour-confirmed extra imports and steady generation; forecast too low"),
 "26": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "27": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "28": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "29": ("leave", "forecast error", "forecast collapses to a few thousand MW for a day; demand, generation and interchange normal"),
 "30": ("backfill", "demand error", "interchange reported as exactly zero while neighbours report about 430 MW of imports; generation also collapses"),
 "31": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "32": ("backfill", "demand error", "own interchange shows exports about 1,600 MW above what neighbours report, so demand is understated"),
 "33": ("leave", "forecast error", "forecast stuck at 692 MW for the whole day; demand in line with its prior week"),
 "34": ("backfill", "demand error", "demand reported negative or zero with generation at zero while neighbours report flows into IID"),
 "35": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "36": ("leave", "forecast error", "demand in line with its prior week and neighbour-confirmed; forecast running about 30% low"),
 "37": ("leave", "forecast error", "forecast stuck at 692 MW for the whole day; demand in line with its prior week"),
 "38": ("backfill", "demand error", "demand reported as zero while generation and interchange stay at normal levels"),
}
rows = []
for _, r in job.iterrows():
    t0, t1 = pd.Timestamp(r.first_hour_end_utc), pd.Timestamp(r.last_hour_end_utc)
    g = bal[(bal.ba == r.ba) & (bal.utc >= t0) & (bal.utc <= t1)].set_index("utc")
    ref = bal[(bal.ba == r.ba) & (bal.utc >= t0 - pd.Timedelta(days=7)) & (bal.utc < t0)]
    nb = neighbour_ti(ich, r.ba, t0, t1)
    g = g.join(nb)
    k = r.incident_id[-2:]; v, cat, why = V[k]
    rows.append(dict(incident_id=r.incident_id, ba=r.ba, first_hour_end_utc=r.first_hour_end_utc, last_hour_end_utc=r.last_hour_end_utc,
                     hours=int(r.hours), verdict=v, category=cat, reason=why,
                     submitted_change_mwh=int(r.proposed_change_mwh), applied_change_mwh=int(r.proposed_change_mwh) if v == "backfill" else 0,
                     demand_med=g.d.median(), demand_prior_week_med=ref.d.median(), forecast_med=g.dfc.median(),
                     forecast_prior_week_med=ref.dfc.median(), forecast_distinct=int(g.dfc.nunique()),
                     ng_med=g.ng.median(), ng_prior_week_med=ref.ng.median(), ti_own_med=g.ti.median(),
                     ti_neighbours_med=g.ti_nb.median(), ti_prior_week_med=ref.ti.median(), eia_imputed_hours=int(r.eia_imputed_hours)))
ev = pd.DataFrame(rows)
ev.to_csv("evidence.csv", index=False)
a = ev[ev.verdict == "backfill"]; l = ev[ev.verdict == "leave"]
facts = dict(n=len(ev), hours=int(ev.hours.sum()), submitted_mwh=int(ev.submitted_change_mwh.sum()),
             approved_n=len(a), approved_hours=int(a.hours.sum()), applied_mwh=int(a.applied_change_mwh.sum()),
             removed_n=len(l), removed_hours=int(l.hours.sum()), removed_mwh=int(l.submitted_change_mwh.sum()),
             by_category=ev.groupby(["verdict", "category"]).agg(n=("hours", "size"), hours=("hours", "sum"), mwh=("submitted_change_mwh", "sum")).reset_index().to_dict("records"),
             eia_imputed_in_approved=int(a.eia_imputed_hours.sum()))
json.dump(facts, open("facts.json", "w"), indent=1, default=int)
print(json.dumps(facts, indent=1, default=int))
pd.set_option("display.width", 250)
print(ev[["incident_id", "ba", "verdict", "category", "demand_med", "demand_prior_week_med", "forecast_med", "forecast_prior_week_med", "forecast_distinct", "ng_med", "ng_prior_week_med", "ti_own_med", "ti_neighbours_med"]].round(0).to_string(index=False))
