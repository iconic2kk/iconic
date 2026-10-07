"""Forecast reliability scorecard engine (golden method). Reads only the shipped inputs.

Golden method (FCS-STD-2 as the desk compiled it), five rules on top of coverage:
  * scorecard BAs: Western (EIA regions CAL, NW, SW) BAs reporting demand and a day-ahead forecast, excluding
    the BAs EIA lists as having forecasts not comparable with demand (AVA, PSEI, TEPC in the West)
  * scored hour: reported demand present, day-ahead forecast > 0, EIA did not impute demand for the hour,
    the BA's reporting day is not a forecast-flatline day (every forecast for the day identical, 2+ values),
    the day is not in a 14-day bedding-in window after an active forecast-change notice (effective day + 13),
    and the day is not a DST changeover day (a reporting day with 23 or 25 hours)
  * month / quarter: by the BA's reporting day ("Data Date"), not UTC
  * forecast error % = sum |D - DF| / sum D over scored hours x 100, published to one decimal
"""
import glob
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "..", "inputs")
WEST = {"CAL", "NW", "SW"}
NOT_COMPARABLE = {"AVA", "FPC", "GVL", "LGEE", "PSEI", "SEC", "SPA", "TEPC"}
COLS = {"Balancing Authority": "ba", "Data Date": "date", "UTC Time at End of Hour": "utc",
        "Demand Forecast (MW)": "dfc", "Demand (MW)": "d", "Demand (MW) (Imputed)": "d_imp",
        "Demand (MW) (Adjusted)": "d_adj", "Region": "region"}


def load():
    fr = [pd.read_csv(f, usecols=list(COLS), dtype=str).rename(columns=COLS)
          for f in sorted(glob.glob(os.path.join(INPUTS, "EIA930_BALANCE_*.csv")))]
    b = pd.concat(fr, ignore_index=True)
    for c in ["dfc", "d", "d_imp", "d_adj"]:
        b[c] = pd.to_numeric(b[c], errors="coerce")
    b["utc"] = pd.to_datetime(b["utc"], format="%m/%d/%Y %I:%M:%S %p")
    b["ldate"] = pd.to_datetime(b["date"], format="%m/%d/%Y")
    assert not b.duplicated(["ba", "utc"]).any()
    b = b[b["region"].isin(WEST) & ~b["ba"].isin(NOT_COMPARABLE)].copy()
    # MON-031 forecast flatline: every hourly day-ahead forecast reported for the BA's reporting day has the same value
    f = b[b["dfc"].notna()].groupby(["ba", "ldate"])["dfc"].agg(["nunique", "size"])
    flat = f[(f["nunique"] == 1) & (f["size"] >= 2)].reset_index()[["ba", "ldate"]].assign(flatline=True)
    b = b.merge(flat, on=["ba", "ldate"], how="left")
    b["flatline"] = b["flatline"].fillna(False).astype(bool)
    b["imputed"] = b["d_imp"].notna()
    b["evaluable"] = b["d"].notna() & (b["dfc"] > 0)
    b["month"] = b["ldate"].dt.strftime("%Y-%m")
    b["quarter"] = b["ldate"].dt.year.astype(str) + "Q" + b["ldate"].dt.quarter.astype(str)
    b["m_utc"] = b["utc"].dt.strftime("%Y-%m")
    return b


def scored(b):
    """Golden scored hours: all five rules."""
    if "bedding_in" not in b:
        b = flags(b)
    return b[b["evaluable"] & ~b["imputed"] & ~b["flatline"] & ~b["bedding_in"] & ~b["dst_day"]]


def error_pct(x, key):
    g = x.assign(ae=(x["d"] - x["dfc"]).abs()).groupby(["ba", key])
    return (g["ae"].sum() / g["d"].sum() * 100)


BEDDING_DAYS = 14  # effective reporting day plus the next 13


def flags(b):
    """Add the bedding-in and DST-transition-day flags used by the golden method."""
    reg = pd.read_csv(os.path.join(INPUTS, "forecast_change_notices.csv"), skiprows=1)
    reg = reg[reg["status"] == "active"]
    b = b.copy(); b["bedding_in"] = False
    for r in reg.itertuples():
        e = pd.Timestamp(r.effective_reporting_day)
        b.loc[(b["ba"] == r.ba) & (b["ldate"] >= e) & (b["ldate"] <= e + pd.Timedelta(days=BEDDING_DAYS - 1)), "bedding_in"] = True
    n = b.groupby(["ba", "ldate"])["utc"].transform("size")
    b["dst_day"] = n != 24
    return b

