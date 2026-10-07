"""Derive the desk's published scorecard history (controls) from the shipped EIA files with the golden method."""
import os
import pandas as pd
from scorecard import load, scored, error_pct, INPUTS

b = load(); s = scored(b)
m = error_pct(s, "month").round(1).rename("forecast_error_pct").reset_index().rename(columns={"month": "period"})
m = m[(m.period >= "2024-07") & (m.period <= "2026-06")].assign(period_type="month")
q = error_pct(s, "quarter").rename("raw").reset_index().rename(columns={"quarter": "period"})
q = q[(q.period >= "2024Q3") & (q.period <= "2026Q2")]
q["rank"] = q.groupby("period")["raw"].rank(ascending=False, method="first").astype(int)
cut = q.period.map(lambda p: 3 if p in ("2024Q3", "2024Q4") else 5)  # Watch widened to five on 2025-04-07 (FCS-STD-2 v8)
q["forecast_watch"] = (q["rank"] <= cut).map({True: "Y", False: ""})
q["forecast_error_pct"] = q["raw"].round(1)
q = q.drop(columns="raw").assign(period_type="quarter")
pub = {"2024Q3": "2024-10-14", "2024Q4": "2025-01-13", "2025Q1": "2025-04-14", "2025Q2": "2025-07-14",
       "2025Q3": "2025-10-13", "2025Q4": "2026-01-12", "2026Q1": "2026-04-13", "2026Q2": "2026-07-13"}
qpub = lambda p: pub[p] if "Q" in p else pub[f"{p[:4]}Q{(int(p[5:]) - 1) // 3 + 1}"]
h = pd.concat([m, q], ignore_index=True)
h["published_on"] = h.period.map(qpub)
h = h[["period_type", "period", "ba", "forecast_error_pct", "rank", "forecast_watch", "published_on"]]
h["rank"] = h["rank"].astype("Int64")
h = h.sort_values(["period_type", "period", "ba"])
path = os.path.join(INPUTS, "forecast_scorecard_published_2024Q3_2026Q2.csv")
with open(path, "w", newline="") as fh:
    fh.write("grid-data-ops forecast reliability scorecard | published figures as issued, Q3 2024 to Q2 2026 | "
             "exported 2026-10-05 from the scorecard archive (figures only; compilation programs not retained)\n")
    h.to_csv(fh, index=False)
print(h.period_type.value_counts().to_dict(), h.ba.nunique())
print(h[(h.period_type == "quarter") & (h.forecast_watch == "Y")].groupby("period").ba.apply(list).to_string())
