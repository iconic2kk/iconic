"""Derive the BF-0712 backfill job export from the shipped EIA-930 BALANCE files."""
import os
import pandas as pd
from data import load_balance, incidents, INPUTS

bal = load_balance()
inc = incidents(bal)
rows = []
for k, r in inc.iterrows():
    g = bal[(bal.ba == r.ba) & (bal.utc >= r["first"]) & (bal.utc <= r["last"])]
    dev = ((g.d - g.dfc) / g.dfc).abs()
    rows.append({
        "incident_id": f"BF-0712-{k + 1:02d}",
        "ba": r.ba,
        "first_hour_end_utc": r["first"].strftime("%Y-%m-%d %H:%M"),
        "last_hour_end_utc": r["last"].strftime("%Y-%m-%d %H:%M"),
        "hours": len(g),
        "max_abs_deviation_pct": round(dev.max() * 100, 1),
        "reported_demand_mwh": int(g.d.sum()),
        "forecast_mwh": int(g.dfc.sum()),
        "proposed_change_mwh": int((g.dfc - g.d).sum()),
        "eia_imputed_hours": int(g.d_imp.notna().sum()),
        "proposed_action": "replace Demand (MW) with Demand Forecast (MW) for every hour",
    })
job = pd.DataFrame(rows)
path = os.path.join(INPUTS, "BF-0712_backfill_job.csv")
with open(path, "w", newline="") as fh:
    fh.write("sentinel backfill job export | BF-0712 | status: awaiting data-owner sign-off | source: MON-021 deviation incidents "
             "(|reported demand - day-ahead forecast| / forecast > 40% for 24+ consecutive hours, hour-end UTC 2024-09-01 to "
             "2026-06-30, monitored BAs) | regenerated 2026-10-05 from the published EIA-930 BALANCE six-month files\n")
    job.to_csv(fh, index=False)
print(len(job), job.hours.sum(), job.proposed_change_mwh.sum())
print(job[["incident_id", "ba", "first_hour_end_utc", "hours", "proposed_change_mwh", "eia_imputed_hours"]].to_string(index=False))
