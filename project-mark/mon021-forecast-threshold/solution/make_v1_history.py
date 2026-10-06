"""Derive MON-021 v1 page history (20%, whole feed) from the shipped EIA-930 files."""
import os
import pandas as pd
from replay import load_balance, evaluable, pages, load_rota, INPUTS

df = load_balance()
e = evaluable(df)
p = pages(e, 20).sort_values(["first_breach", "ba"]).reset_index(drop=True)
rota = load_rota()
out = pd.DataFrame({
    "page_id": [f"PG-21-{i:05d}" for i in range(1, len(p) + 1)],
    "monitor_id": "MON-021",
    "monitor_version": 1,
    "threshold_pct": 20,
    "ba": p["ba"],
    "page_date_utc": p["date"].dt.strftime("%Y-%m-%d"),
    "first_breach_hour_end_utc": p["first_breach"].dt.strftime("%Y-%m-%d %H:%M"),
    "breach_hours": p["breach_hours"],
    "max_deviation_pct": (p["max_dev"] * 100).round(1),
    "routed_to": p["month"].map(rota["primary_oncall"]),
})
path = os.path.join(INPUTS, "MON-021_v1_page_history.csv")
with open(path, "w", newline="") as fh:
    fh.write("sentinel page history export | MON-021 v1 (threshold 20%, scope: every BA in FD-EIA930-BAL) | "
             "page dates 2025-10-01 to 2026-09-30 UTC | regenerated 2026-10-05 by replaying the v1 rule "
             "over the published EIA-930 BALANCE six-month files\n")
    out.to_csv(fh, index=False)
print(len(out), out.ba.nunique(), out.head(3).to_string())
