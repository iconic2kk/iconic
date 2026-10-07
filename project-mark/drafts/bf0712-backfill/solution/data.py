"""Loaders for the BF-0712 task. Read only the shipped input files."""
import glob
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "..", "inputs")

# BAs outside the deviation monitor's scope (EIA: actual vs forecast comparison not meaningful)
NOT_COMPARABLE = ["AVA", "FPC", "GVL", "LGEE", "PSEI", "SEC", "SPA", "TEPC"]
JOB_START, JOB_END = pd.Timestamp("2024-09-01"), pd.Timestamp("2026-07-01")
DEV, MIN_HOURS = 0.40, 24

BAL = {
    "Balancing Authority": "ba",
    "UTC Time at End of Hour": "utc",
    "Demand Forecast (MW)": "dfc",
    "Demand (MW)": "d",
    "Net Generation (MW)": "ng",
    "Total Interchange (MW)": "ti",
    "Demand (MW) (Imputed)": "d_imp",
}


def load_balance():
    frames = []
    for f in sorted(glob.glob(os.path.join(INPUTS, "EIA930_BALANCE_*.csv"))):
        frames.append(pd.read_csv(f, usecols=list(BAL), dtype=str).rename(columns=BAL))
    df = pd.concat(frames, ignore_index=True)
    for c in ["dfc", "d", "ng", "ti", "d_imp"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["utc"] = pd.to_datetime(df["utc"], format="%m/%d/%Y %I:%M:%S %p")
    assert not df.duplicated(["ba", "utc"]).any()
    return df.sort_values(["ba", "utc"]).reset_index(drop=True)


def load_interchange():
    frames = []
    for f in sorted(glob.glob(os.path.join(INPUTS, "EIA930_INTERCHANGE_*.csv"))):
        names = {"Balancing Authority": "ba", "Directly Interconnected Balancing Authority": "diba",
                 "UTC Time at End of Hour": "utc", "Interchange (MW)": "mw"}
        x = pd.read_csv(f, usecols=list(names), dtype=str).rename(columns=names)
        frames.append(x[["ba", "diba", "utc", "mw"]])
    i = pd.concat(frames, ignore_index=True)
    i["mw"] = pd.to_numeric(i["mw"], errors="coerce")
    i["utc"] = pd.to_datetime(i["utc"], format="%m/%d/%Y %I:%M:%S %p")
    return i.drop_duplicates(["ba", "diba", "utc"])


def incidents(bal):
    """Runs of 24+ consecutive evaluated hours with |D - DF| / DF > 40%."""
    e = bal[bal["d"].notna() & (bal["dfc"] > 0) & ~bal["ba"].isin(NOT_COMPARABLE)].copy()
    e["dev"] = (e["d"] - e["dfc"]) / e["dfc"]
    e["flag"] = e["dev"].abs() > DEV
    out = []
    for ba, g in e.groupby("ba"):
        t = g["utc"].values; f = g["flag"].values
        i = 0
        while i < len(g):
            if not f[i]:
                i += 1; continue
            j = i
            while j + 1 < len(g) and f[j + 1] and (t[j + 1] - t[j]) == np.timedelta64(1, "h"):
                j += 1
            if j - i + 1 >= MIN_HOURS:
                out.append((ba, pd.Timestamp(t[i]), pd.Timestamp(t[j])))
            i = j + 1
    inc = pd.DataFrame(out, columns=["ba", "first", "last"])
    inc = inc[(inc["first"] >= JOB_START) & (inc["first"] < JOB_END)]
    return inc.sort_values(["first", "ba"]).reset_index(drop=True)


def neighbour_ti(ich, ba, t0, t1):
    """BA's total interchange as its neighbours report it (own report where a neighbour is silent)."""
    own = ich[(ich["ba"] == ba) & (ich["utc"] >= t0) & (ich["utc"] <= t1)]
    rev = ich[(ich["diba"] == ba) & (ich["utc"] >= t0) & (ich["utc"] <= t1)].rename(
        columns={"ba": "diba", "diba": "ba", "mw": "nb"})
    p = own.merge(rev, on=["ba", "diba", "utc"], how="left")
    p["view"] = np.where(p["nb"].notna(), -p["nb"], p["mw"])
    return p.groupby("utc").agg(ti_nb=("view", "sum"), pairs=("view", "size"), silent=("nb", lambda s: int(s.isna().sum())))
