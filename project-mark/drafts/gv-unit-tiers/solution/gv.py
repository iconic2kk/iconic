"""GV-STD-3 tier engine (golden method). Reads only the shipped inputs."""
import math, os
import numpy as np
import pandas as pd

IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inputs")
IBR_PM = {"PV", "WT", "WS", "BA", "FW"}


def western_bas():
    ref = pd.read_excel(os.path.join(IN, "EIA930_Reference_Tables.xlsx"), "BAs")
    return set(ref[ref["Region/Country Code"].isin(["CAL", "NW", "SW"])]["BA Code"])


def inventory(month="august", statuses=("OP", "SB"), cap="Net Summer Capacity (MW)"):
    o = pd.read_excel(os.path.join(IN, f"EIA860M_{month}_generator2026.xlsx"), "Operating", skiprows=2, dtype=str)
    o = o[o["Plant ID"].notna() & o["Generator ID"].notna()].copy()
    o["mw"] = pd.to_numeric(o[cap], errors="coerce")
    o["st"] = o["Status"].str[1:3]
    w = o[o["Balancing Authority Code"].isin(western_bas()) & o.st.isin(statuses) & ~o["Prime Mover Code"].isin(IBR_PM) & (o.mw > 0)].copy()
    return w


def units(w, grain="unit"):
    if grain == "unit":
        w = w.assign(ukey=np.where(w["Unit Code"].notna(), w["Plant ID"] + "|" + w["Unit Code"].fillna(""), w["Plant ID"] + "|gen|" + w["Generator ID"]))
    else:
        w = w.assign(ukey=w["Plant ID"] + "|gen|" + w["Generator ID"])
    return (w.groupby("ukey").agg(plant_id=("Plant ID", "first"), plant=("Plant Name", "first"), ba=("Balancing Authority Code", "first"),
                                  generators=("Generator ID", lambda s: ",".join(sorted(s))), n_gen=("Generator ID", "size"),
                                  technology=("Technology", lambda s: "/".join(sorted(set(s)))), mw=("mw", "sum"))
              .reset_index().sort_values(["mw", "ukey"], ascending=[False, True]).reset_index(drop=True))


def tiers(u):
    tot = u.mw.sum(); cum = u.mw.cumsum() / tot * 100
    b1 = u.mw[cum >= 50].iloc[0]; b2 = u.mw[cum >= 85].iloc[0]
    u = u.assign(tier=np.where(u.mw >= b1, 1, np.where(u.mw >= b2, 2, 3)))
    n = u.tier.value_counts().to_dict(); n = {k: n.get(k, 0) for k in (1, 2, 3)}
    load = n[1] + math.ceil(n[2] / 3) + math.ceil(n[3] / 6)
    cap = u.groupby("tier").mw.sum().to_dict()
    return u, dict(b1=b1, b2=b2, n=n, units=len(u), mw=round(tot, 1), cap={k: round(v, 1) for k, v in cap.items()}, load=load,
                   share1=round(cap[1] / tot * 100, 3), share12=round((cap[1] + cap[2]) / tot * 100, 3))


if __name__ == "__main__":
    u, r = tiers(units(inventory()))
    print("GOLDEN", r)
    for lab, kw, g in [("generator rows", {}, "gen"), ("july inventory", dict(month="july"), "unit"), ("OP only", dict(statuses=("OP",)), "unit"),
                       ("nameplate", dict(cap="Nameplate Capacity (MW)"), "unit"), ("generator rows + nameplate", dict(cap="Nameplate Capacity (MW)"), "gen")]:
        print(f"{lab:28s}", tiers(units(inventory(**kw), g))[1])
