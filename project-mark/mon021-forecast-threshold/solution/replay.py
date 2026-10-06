"""MON-021 v2 go-live paging replay engine. Reads only the shipped input files."""
import glob
import os
from collections import deque

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "..", "inputs")

WINDOW_START = pd.Timestamp("2025-10-01")  # first UTC date in the replay
WINDOW_END = pd.Timestamp("2026-09-30")    # last UTC date in the replay
CANDIDATES = [25, 50, 75, 100, 150]

# About the EIA-930 data, "Impact of pseudo-ties and dynamic scheduling on demand
# forecast": systems for which the actual vs forecast comparison is not meaningful,
# i.e. the forecast is not prepared on the same physical basis as reported demand.
FORECAST_NOT_COMPARABLE = ["AVA", "FPC", "GVL", "LGEE", "PSEI", "SEC", "SPA", "TEPC"]

COLS = {
    "Balancing Authority": "ba",
    "UTC Time at End of Hour": "utc",
    "Demand Forecast (MW)": "dfc",
    "Demand (MW)": "d",
    "Demand (MW) (Imputed)": "d_imp",
}


def load_history():
    """All shipped BALANCE rows (Jul 2024 onward), one row per BA-hour."""
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
    df["month"] = df["date"].dt.strftime("%Y-%m")
    return df.sort_values(["ba", "utc"]).reset_index(drop=True)


def in_window(df):
    return df[(df["date"] >= WINDOW_START) & (df["date"] <= WINDOW_END)].copy()


def load_balance():
    return in_window(load_history())


def evaluable(df):
    e = df[df["d"].notna() & (df["dfc"] > 0)].copy()
    e["dev"] = (e["d"] - e["dfc"]).abs() / e["dfc"]
    e["imputed"] = e["d_imp"].notna()
    return e


def pages(e, thr_pct):
    """MON-021 pages: one per BA per UTC date with any breach above the threshold."""
    hits = e[e["dev"] > thr_pct / 100.0]
    g = hits.sort_values("utc").groupby(["ba", "date"])
    p = g.agg(first_breach=("utc", "first"), breach_hours=("utc", "size"),
              max_dev=("dev", "max"), month=("month", "first")).reset_index()
    return p


def mon014_flags(hist, bas):
    """MON-014 v3: demand <= 0, or >= 1.5x the highest unflagged demand in the prior 365 days."""
    out = []
    win = pd.Timedelta(days=365)
    for ba, g in hist[hist["ba"].isin(bas)].groupby("ba"):
        dq = deque()  # monotonic deque of (time, value) for accepted hours
        for t, d in zip(g["utc"], g["d"]):
            while dq and dq[0][0] <= t - win:
                dq.popleft()
            if np.isnan(d):
                continue
            ceiling = dq[0][1] if dq else None
            kind = "floor" if d <= 0 else ("ceiling" if ceiling is not None and d >= 1.5 * ceiling else None)
            if kind:
                out.append((ba, t, d, ceiling, kind))
            else:
                while dq and dq[-1][1] <= d:
                    dq.pop()
                dq.append((t, d))
    f = pd.DataFrame(out, columns=["ba", "utc", "d", "ceiling", "kind"])
    f["date"] = f["utc"].dt.floor("D")
    f["month"] = f["date"].dt.strftime("%Y-%m")
    return f


def mon014_pages(hist, bas):
    f = in_window(mon014_flags(hist, bas))
    return f.sort_values("utc").groupby(["ba", "date"]).agg(
        first_flag=("utc", "first"), month=("month", "first"), kinds=("kind", lambda s: ",".join(sorted(set(s))))
    ).reset_index()


def load_rota():
    r = pd.read_csv(os.path.join(INPUTS, "oncall_rota_2025-10_to_2026-09.csv"), skiprows=1)
    return r.set_index("rota_month")
