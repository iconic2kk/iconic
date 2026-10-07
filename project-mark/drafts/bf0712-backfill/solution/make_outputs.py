import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ev = pd.read_csv("evidence.csv"); f = json.load(open("facts.json"))
out = ev[["incident_id", "ba", "first_hour_end_utc", "last_hour_end_utc", "hours", "verdict", "category",
          "submitted_change_mwh", "applied_change_mwh", "reason"]].copy()
out["verdict"] = out.verdict.map({"backfill": "backfill", "leave": "leave as reported"})
out.to_csv("../golden/BF-0712_amended_job.csv", index=False)

fig, ax = plt.subplots(figsize=(12, 13.6))
y = list(range(len(ev)))[::-1]
gwh_s = ev.submitted_change_mwh / 1000; gwh_a = ev.applied_change_mwh / 1000
col = {"demand error": "#1f6fb2", "forecast error": "#c0392b", "real load": "#e08e0b"}
ax.barh([v + 0.2 for v in y], gwh_s, height=0.38, color="#b9bec6", label="submitted job")
ax.barh([v - 0.2 for v in y], gwh_a, height=0.38, color=[col[c] if v == "backfill" else "#1f6fb2" for c, v in zip(ev.category, ev.verdict)],
        label="applied after review")
for i, r in ev.iterrows():
    yy = y[i]
    if r.verdict == "leave":
        ax.text(0.6, yy - 0.2, "removed", va="center", fontsize=7.5, color=col[r.category])
ax.set_xscale("symlog", linthresh=10)
ax.set_xticks([-500, -100, -10, 0, 10, 100, 500]); ax.set_xticklabels(["-500", "-100", "-10", "0", "10", "100", "500"])
ax.axvline(0, color="black", linewidth=0.8)
ax.set_yticks(y)
ax.set_yticklabels([f"{r.incident_id[-2:]} {r.ba:<4} {r.first_hour_end_utc[:10]}  {r.hours}h" for _, r in ev.iterrows()], fontsize=8, family="monospace")
for lab, c in zip(ax.get_yticklabels(), ev.verdict):
    lab.set_color("#1f6fb2" if c == "backfill" else "#555")
ax.set_xlabel("Change to published demand, GWh (symmetric log scale)")
ax.legend(handles=[Patch(color="#b9bec6", label="change in the job as submitted"),
                   Patch(color="#1f6fb2", label="change applied (incident backfilled: demand error)"),
                   Patch(color="white", label="removed incidents:"),
                   Patch(color="#c0392b", label="  forecast error (demand correct)"),
                   Patch(color="#e08e0b", label="  real load change (demand correct)")],
          loc="upper center", bbox_to_anchor=(0.45, -0.05), ncol=3, fontsize=8.5, frameon=False)
ax.set_title(f"BF-0712: run with {f['removed_n']} incidents removed. Backfill {f['approved_n']} incidents / {f['approved_hours']} BA-hours, "
             f"{f['applied_mwh'] / 1000:+,.1f} GWh\nversus {f['submitted_mwh'] / 1000:+,.1f} GWh if run as submitted "
             f"({f['n']} incidents / {f['hours']:,} BA-hours)", fontsize=12, fontweight="bold", loc="left")
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("../golden/BF-0712_submitted_vs_applied.png", dpi=150)
print("ok")
