"""Builds q3_2026_sentinel_alert_summary.csv from the real EIA-930 BALANCE file, applying the three
Sentinel monitor rules in sentinel_monitors_export.json to Q3 2026 (reporting days 1 Jul - 30 Sep)."""
import pandas as pd, numpy as np, os
IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inputs")
b = pd.read_csv(os.path.join(IN, "EIA930_BALANCE_2026_Jul_Dec.csv"), dtype=str)
b = b[b.Region.isin(["CAL", "NW", "SW"]) & ~b["Balancing Authority"].isin({"AVRN", "DEAA", "GRID", "GWA"})].copy()
for c in ["Demand (MW)", "Demand Forecast (MW)"]:
    b[c] = pd.to_numeric(b[c].str.replace(",", ""), errors="coerce")
b["utc"] = pd.to_datetime(b["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p")
b["ldate"] = pd.to_datetime(b["Data Date"], format="%m/%d/%Y")
b = b.sort_values(["Balancing Authority", "utc"])
rows = []
for ba, g in b.groupby("Balancing Authority"):
    d, f = g["Demand (MW)"], g["Demand Forecast (MW)"]
    miss = d.isna()
    run = (miss != miss.shift()).cumsum(); rl = miss.groupby(run).transform("size")
    m009 = miss & (rl > 3)
    prior_max = d.where(d > 0).cummax().shift()
    m014 = d.notna() & ((d <= 0) | (d >= 1.5 * prior_max))
    m021 = d.notna() & f.notna() & (f > 0) & ((d - f).abs() / f > 0.20)
    inq = (g.ldate >= "2026-07-01") & (g.ldate <= "2026-09-30")
    for mid, m in [("MON-009", m009), ("MON-014", m014), ("MON-021", m021)]:
        mm = m[inq]
        starts = (mm & ~mm.shift(fill_value=False)).sum()
        rows.append((ba, mid, int(mm.sum()), int(starts)))
out = pd.DataFrame(rows, columns=["ba", "monitor_id", "alert_hours", "alerts_opened"])
with open(os.path.join(IN, "q3_2026_sentinel_alert_summary.csv"), "w") as fh:
    fh.write("Sentinel alert summary | Q3 2026 (reporting days 2026-07-01 to 2026-09-30) | exported 2026-10-06 from sentinel-alerting | scenario export authored for this exercise, computed from the EIA-930 BALANCE file\n")
    out.to_csv(fh, index=False)
print(out.pivot(index="ba", columns="monitor_id", values="alert_hours").to_string())
