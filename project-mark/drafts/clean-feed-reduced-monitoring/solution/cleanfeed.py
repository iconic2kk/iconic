"""DQ-STD-7 clean-hour engine (golden method). Reads only the shipped inputs.

Golden reading of DQ-STD-7 section 3, for each covered Western BA and each hour of its Q3 2026 reporting days:
  present as filed  : demand, day-ahead forecast, net generation and total interchange present, every subregion the BA
                      reports in the quarter present (subregion BAs), and no EIA-imputed value (Demand/NG/TI Imputed
                      columns and the by-source Imputed columns all empty)
  same quantity     : NG = sum of NG by energy source; TI = sum of the BA's own INTERCHANGE rows; demand = sum of subregion
                      demand (BAs that report subregions); each tie value = minus the interconnected BA's own filing of the
                      same tie for the same UTC hour, where that BA files on Form EIA-930
  balance           : demand + total interchange = net generation
  all comparisons exact (whole MW). Share = clean hours / hours in quarter x 100. Highest share wins; tie -> higher mean demand.
"""
import os
import numpy as np
import pandas as pd

IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inputs")
D, DF, NG, TI = "Demand (MW)", "Demand Forecast (MW)", "Net Generation (MW)", "Total Interchange (MW)"
IMP = ["Demand (MW) (Imputed)", "Net Generation (MW) (Imputed)", "Total Interchange (MW) (Imputed)"]
GENONLY = {"AVRN", "DEAA", "GRID", "GWA"}
Q0, Q1 = "2026-07-01", "2026-09-30"


def _rd(name):
    x = pd.read_csv(os.path.join(IN, name), dtype=str)
    for c in x.columns:
        if "(MW)" in c:
            x[c] = pd.to_numeric(x[c].str.replace(",", ""), errors="coerce")
    x["utc"] = pd.to_datetime(x["UTC Time at End of Hour"], format="%m/%d/%Y %I:%M:%S %p")
    x["ldate"] = pd.to_datetime(x["Data Date"], format="%m/%d/%Y")
    return x


def build(tol=0, tol_cp=None, onesided_fails=False):
    tol_cp = tol if tol_cp is None else tol_cp
    b = _rd("EIA930_BALANCE_2026_Jul_Dec.csv")
    b = b[b.Region.isin(["CAL", "NW", "SW"]) & ~b["Balancing Authority"].isin(GENONLY)].rename(columns={"Balancing Authority": "ba"})
    i = _rd("EIA930_INTERCHANGE_2026_Jul_Dec.csv").rename(columns={"Balancing Authority": "ba", "Directly Interconnected Balancing Authority": "diba", "Interchange (MW)": "mw"})
    s = _rd("EIA930_SUBREGION_2026_Jul_Dec.csv").rename(columns={"Balancing Authority": "ba", "Demand (MW)": "mw", "Sub-Region": "sub"})
    q = b[(b.ldate >= Q0) & (b.ldate <= Q1)].copy()
    F = [c for c in b.columns if c.startswith("Net Generation (MW) from") and not c.endswith(")")]
    FI = [c for c in b.columns if c.startswith("Net Generation (MW) from") and c.endswith("(Imputed)")]
    # present as filed
    used = q.groupby("ba")[F].transform(lambda c: c.notna().any())
    q["p_core"] = q[[D, DF, NG, TI]].notna().all(axis=1)
    q["p_source"] = ~(used & q[F].isna()).any(axis=1)
    q["p_notimp"] = q[IMP].isna().all(axis=1) & q[FI].isna().all(axis=1)
    iq = i[i.ba.isin(q.ba.unique())]
    iq = iq.merge(q[["ba", "utc"]], on=["ba", "utc"])            # the BA's own tie rows for its Q3 hours
    ties = iq.groupby("ba").diba.unique()
    full = q[["ba", "utc"]].merge(pd.DataFrame([(a, d) for a, ds in ties.items() for d in ds], columns=["ba", "diba"]), on="ba")
    full = full.merge(iq[["ba", "diba", "utc", "mw"]], on=["ba", "diba", "utc"], how="left")
    q = q.merge(full.groupby(["ba", "utc"]).mw.apply(lambda v: v.notna().all()).rename("p_ties").reset_index(), on=["ba", "utc"], how="left")
    q["p_ties"] = q.p_ties.fillna(True)
    sq = s.merge(q[["ba", "utc"]], on=["ba", "utc"])
    subs = sq.groupby("ba")["sub"].nunique()
    sg = sq.groupby(["ba", "utc"]).agg(ssum=("mw", "sum"), sn=("mw", "count")).reset_index()
    q = q.merge(sg, on=["ba", "utc"], how="left")
    q["nsub"] = q.ba.map(subs)
    q["p_subs"] = q.nsub.isna() | (q.sn == q.nsub)
    q["present"] = q.p_core & q.p_notimp & q.p_subs
    # same quantity
    q["a_ng_sources"] = (q[NG] - q[F].sum(axis=1, min_count=1)).abs() <= tol
    ts = iq.groupby(["ba", "utc"]).mw.sum().rename("tsum").reset_index()
    q = q.merge(ts, on=["ba", "utc"], how="left")
    q["a_ti_ties"] = (q[TI] - q.tsum).abs() <= tol
    q["a_ti_sumvalid"] = (q[TI] - q["Sum(Valid DIBAs) (MW)"]).abs() <= tol
    q["a_d_subs"] = q.nsub.isna() | ((q[D] - q.ssum).abs() <= tol)
    filers = set(i.ba.unique())
    cp = i[["ba", "diba", "utc", "mw"]].rename(columns={"ba": "diba", "diba": "ba", "mw": "cp"})
    full = full.merge(cp, on=["ba", "diba", "utc"], how="left")
    full["ok"] = ~full.diba.isin(filers) | full.mw.isna() | (full.cp.isna() & (not onesided_fails)) | ((full.mw + full.cp).abs() <= tol_cp)
    # a tie the interconnected BA files but this BA leaves blank is already caught by p_ties; a tie only the other end files
    # counts against that other end's presence, not this BA's
    q = q.merge(full.groupby(["ba", "utc"]).ok.all().rename("a_tie_counterpart").reset_index(), on=["ba", "utc"], how="left")
    q["a_tie_counterpart"] = q.a_tie_counterpart.fillna(True)
    q["a_balance"] = (q[D] + q[TI] - q[NG]).abs() <= tol
    q["clean"] = q.present & q.a_ng_sources & q.a_ti_ties & q.a_d_subs & q.a_tie_counterpart & q.a_balance
    return q


CHECKS = ["present", "a_ng_sources", "a_ti_ties", "a_d_subs", "a_tie_counterpart", "a_balance"]


def table(q, mask=None):
    m = q.clean if mask is None else mask
    g = q.assign(m=m).groupby("ba").agg(hours=("m", "size"), clean_hours=("m", "sum"), mean_demand=(D, "mean"))
    g["unclean_hours"] = g.hours - g.clean_hours
    g["share"] = g.clean_hours / g.hours * 100
    for c in CHECKS:
        g["fail_" + c] = q.assign(f=~q[c]).groupby("ba").f.sum()
    g = g.sort_values(["share", "mean_demand"], ascending=[False, False])
    g["rank"] = range(1, len(g) + 1)
    return g


if __name__ == "__main__":
    q = build()
    t = table(q)
    pd.set_option("display.width", 250)
    print(t.round(3).to_string())
