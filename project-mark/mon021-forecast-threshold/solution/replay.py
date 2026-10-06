"""MON-021 replay engine. Reads only the shipped input files."""
import glob
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "..", "inputs")

WINDOW_START = pd.Timestamp("2025-10-01")  # first UTC date in the replay
WINDOW_END = pd.Timestamp("2026-09-30")    # last UTC date in the replay
CANDIDATES = [25, 50, 75, 100, 150]

# About the EIA-930 data, "Impact of pseudo-ties and dynamic scheduling on demand
# forecast": systems for which the actual vs forecast comparison is not meaningful.
FORECAST_NOT_COMPARABLE = ["AVA", "FPC", "GVL", "LGEE", "PSEI", "SEC", "SPA", "TEPC"]

COLS = {
    "Balancing Authority": "ba",
    "UTC Time at End of Hour": "utc",
    "Demand Forecast (MW)": "dfc",
    "Demand (MW)": "d",
    "Demand (MW) (Imputed)": "d_imp",
}


def load_balance():
    frames = []
    for f in sorted(glob.glob(os.path.join(INPUTS, "EIA930_BALANCE_*.csv"))):
        x = pd.read_csv(f, usecols=list(COLS), dtype=str).rename(columns=COLS)
        frames.append(x)
    df = pd.concat(frames, ignore_index=True)
    for c in ["dfc", "d", "d_imp"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["utc"] = pd.to_datetime(df["utc"], format="%m/%d/%Y %I:%M:%S %p")
    assert not df.duplicated(["ba", "utc"]).any(), "duplicate BA-hour across files"
    df["date"] = df["utc"].dt.floor("D")
    df = df[(df["date"] >= WINDOW_START) & (df["date"] <= WINDOW_END)].copy()
    df["month"] = df["date"].dt.strftime("%Y-%m")
    return df


def evaluable(df):
    e = df[df["d"].notna() & (df["dfc"] > 0)].copy()
    e["dev"] = (e["d"] - e["dfc"]).abs() / e["dfc"]
    e["imputed"] = e["d_imp"].notna()
    return e


def pages(e, thr_pct):
    hits = e[e["dev"] > thr_pct / 100.0]
    g = hits.sort_values("utc").groupby(["ba", "date"])
    p = g.agg(first_breach=("utc", "first"), breach_hours=("utc", "size"),
              max_dev=("dev", "max"), month=("month", "first")).reset_index()
    return p


def load_rota():
    r = pd.read_csv(os.path.join(INPUTS, "oncall_rota_2025-10_to_2026-09.csv"), skiprows=1)
    return r.set_index("rota_month")
