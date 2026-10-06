import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rep = pd.read_csv("replay_table.csv")
f = json.load(open("facts.json"))
chosen = f["chosen"]; s = f["summary"][str(chosen)]
months = list(dict.fromkeys(rep.month))
labels = [pd.Period(m).strftime("%b\n%y") for m in months]
cands = [25, 50, 75, 100, 150]
fig, axes = plt.subplots(1, 5, figsize=(17, 5.2), sharey=True)
for ax, t in zip(axes, cands):
    r = rep[rep.threshold_pct == t].set_index("month").loc[months]
    x = range(len(months))
    colors = ["#c0392b" if p > c else ("#1f6fb2" if t == chosen else "#8a9bb0") for p, c in zip(r.pages, r.triage_capacity_pages)]
    ax.bar(x, r.pages.clip(upper=60), color=colors, width=0.75)
    ax.step([i - 0.5 for i in x] + [len(months) - 0.5], list(r.triage_capacity_pages) + [r.triage_capacity_pages.iloc[-1]],
            where="post", color="black", linestyle="--", linewidth=1.3, label="rota triage capacity")
    for i, p in enumerate(r.pages):
        ax.text(i, min(p, 60) + 0.8, str(p), ha="center", va="bottom", fontsize=7, rotation=90 if p > 60 else 0)
    miss = int(r.eia_imputed_hours_missed.sum()); over = int((r.within_capacity == "N").sum())
    ttl = f"{t}%" + ("  ◀ SHIP" if t == chosen else "")
    ax.set_title(f"{ttl}\n{over} of 12 months over capacity\n{miss} EIA-imputed hour{"" if miss == 1 else "s"} missed", fontsize=10,
                 fontweight="bold" if t == chosen else "normal", color="#1f6fb2" if t == chosen else "black")
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylim(0, 66)
    if t == chosen:
        for sp in ax.spines.values(): sp.set_edgecolor("#1f6fb2"); sp.set_linewidth(2.2)
axes[0].set_ylabel("Pages per month (bars above 60 clipped, value labelled)")
h, l = axes[0].get_legend_handles_labels(); fig.legend(h, l, loc="upper right", fontsize=9, frameon=False, bbox_to_anchor=(0.995, 0.955))
fig.suptitle(f"MON-021 v2 replay, Oct 2025 - Sep 2026: ship {chosen}% — peak {s['peak']} pages in "
             f"{pd.Period(s['peak_month']).strftime('%b %Y')} vs capacity {s['peak'] + s['min_headroom']}, all "
             f"{f['imputed_evaluated']} EIA-imputed hours alerted", fontsize=12.5, fontweight="bold")
fig.text(0.5, 0.005, "Red bars breach that month's rota capacity. Scope: 47 BAs whose day-ahead forecast is a valid reference for "
         "reported demand (AVA, FPC, GVL, LGEE, PSEI, SEC, SPA, TEPC stay on MON-014). One page per BA per UTC date.",
         ha="center", fontsize=8.5, color="#333")
plt.tight_layout(rect=[0, 0.03, 1, 0.92])
plt.savefig("../golden/MON-021_v2_monthly_pages.png", dpi=150)
rep.to_csv("../golden/MON-021_v2_replay_by_month.csv", index=False)
print("ok")
