import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

rep = pd.read_csv("replay_table.csv")
f = json.load(open("facts.json")); S = {int(k): v for k, v in f["summary"].items()}
flip = f["best_flip"]; bm = f["binding_month"]
months = list(dict.fromkeys(rep.month))
labels = [pd.Period(m).strftime("%b\n%y") for m in months]
cands = [25, 50, 75, 100, 150]
CLIP = 60
fig, axes = plt.subplots(1, 5, figsize=(17, 5.6), sharey=True)
for ax, t in zip(axes, cands):
    r = rep[rep.threshold_pct == t].set_index("month").loc[months]
    x = list(range(len(months)))
    over = r.oncall_pages > r.triage_capacity_pages
    v2 = r.mon021_v2_pages.clip(upper=CLIP)
    m14 = (r.oncall_pages.clip(upper=CLIP) - v2).clip(lower=0)
    ax.bar(x, v2, color=["#c0392b" if o else "#1f6fb2" for o in over], width=0.75)
    ax.bar(x, m14, bottom=v2, color=["#e8a49c" if o else "#9ec5e8" for o in over], width=0.75,
           hatch="///", edgecolor="white", linewidth=0)
    ax.step([i - 0.5 for i in x] + [len(x) - 0.5], list(r.triage_capacity_pages) + [r.triage_capacity_pages.iloc[-1]],
            where="post", color="black", linestyle="--", linewidth=1.3)
    for i, p in enumerate(r.oncall_pages):
        ax.text(i, min(p, CLIP) + 0.8, str(p), ha="center", va="bottom", fontsize=7, rotation=90 if p > CLIP else 0)
    s = S[t]
    blocks = []
    if s["months_over"]:
        blocks.append(f"{s['months_over']} of 12 months over capacity")
    if s["missed"]:
        blocks.append(f"misses {s['missed']} EIA-imputed hour{'s' if s['missed'] != 1 else ''}")
    head = f"{t}%" + (f"  (+{f['best_flip_total']} in {pd.Period(bm).strftime('%b')} would ship it)" if t == flip else "")
    ax.set_title(head + "\n" + "\n".join(blocks or ["passes"]), fontsize=9.5,
                 fontweight="bold" if t == flip else "normal", color="#1f6fb2" if t == flip else "black")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7); ax.set_ylim(0, CLIP + 7)
    if t == flip:
        i = months.index(bm)
        ax.annotate("binding month", (i, min(r.oncall_pages[bm], CLIP) + 4), xytext=(i - 5, 55),
                    fontsize=8, arrowprops=dict(arrowstyle="->", color="#333"))
        for sp in ax.spines.values():
            sp.set_edgecolor("#1f6fb2"); sp.set_linewidth(2.2)
axes[0].set_ylabel(f"On-call pages per month (bars above {CLIP} clipped, value labelled)")
fig.legend(handles=[Patch(color="#1f6fb2", label="MON-021 v2 pages"),
                    Patch(facecolor="#9ec5e8", hatch="///", edgecolor="white", label="MON-014 pages (BAs outside v2 scope)"),
                    Patch(color="#c0392b", label="month over capacity"),
                    Line2D([0], [0], color="black", linestyle="--", label="rota triage capacity")],
           loc="upper center", ncol=4, fontsize=8.5, frameon=False, bbox_to_anchor=(0.5, 0.925))
b = S[flip]
fig.suptitle(f"MON-021 v2 go-live replay, Oct 2025 - Sep 2026: HOLD, no candidate ships. Binding month "
             f"{pd.Period(bm).strftime('%B %Y')} ({flip}%: {b['peak']} on-call pages vs capacity {b['peak_cap']})",
             fontsize=12.5, fontweight="bold")
fig.text(0.5, 0.008, "On-call pages = MON-021 v2 pages for in-scope BAs + MON-014 pages for AVA, FPC, GVL, LGEE, PSEI, SEC, SPA, TEPC "
         "(routed to oncall-primary from v2 go-live). One page per BA per UTC date.", ha="center", fontsize=8.5, color="#333")
plt.tight_layout(rect=[0, 0.03, 1, 0.88])
plt.savefig("../golden/MON-021_v2_go-live_replay.png", dpi=150)
rep.to_csv("../golden/MON-021_v2_go-live_replay_by_month.csv", index=False)
print("ok")
