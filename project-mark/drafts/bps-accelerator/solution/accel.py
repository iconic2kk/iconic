"""Accelerator evaluation (golden). Units authorized by the same permit offices in every year (Census's place-level records),
because the county files hold offices out of the county totals until the annual universe update (BPS methodology and 2023 FAQ):
Bastrop County's unincorporated area reported all of 2021 and 2022 but entered the county totals only from January 2023."""
import io, os
import pandas as pd
IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inputs")
AUS = {"48021": "Bastrop", "48055": "Caldwell", "48209": "Hays", "48453": "Travis", "48491": "Williamson"}
Y = [2021, 2022, 2023, 2024]
def county(y):
    t = open(os.path.join(IN, f"co{y}a.txt"), encoding="latin-1").read().splitlines()
    d = pd.read_csv(io.StringIO("\n".join(t[3:])), header=None, dtype=str)
    d["fips"] = d[1].str.zfill(2) + d[2].str.zfill(3)
    d["units"] = d[[7, 10, 13, 16]].apply(pd.to_numeric).sum(axis=1)
    return d.set_index("fips").units
t = open(os.path.join(IN, "bps_place_annual_south_2021_2024.csv"), encoding="latin-1").read().splitlines()
p = pd.read_csv(io.StringIO("\n".join(t[3:])), header=None, dtype=str)
p["year"] = p[0].astype(int); p["key"] = p[1].str.strip() + "-" + p[2].str.strip()
p["fips"] = p[1].str.strip().str.zfill(2) + p[3].str.strip().str.zfill(3)
p["units"] = p[[18, 21, 24, 27]].apply(pd.to_numeric).sum(axis=1)
p = p[p.fips.isin(AUS)]
same = set.intersection(*[set(p[p.year == y].key) for y in Y])
rows = []
for f, nm in AUS.items():
    for y in Y:
        rows.append(dict(county=nm, year=y, county_file=int(county(y)[f]),
                         same_offices=int(p[(p.fips == f) & (p.year == y) & p.key.isin(same)].units.sum())))
T = pd.DataFrame(rows).pivot(index="county", columns="year")
def calc(col):
    B = T[col].loc["Bastrop"]; C = T[col].drop("Bastrop").sum()
    g = lambda s: ((s[2023] + s[2024]) / 2 - (s[2021] + s[2022]) / 2) / ((s[2021] + s[2022]) / 2) * 100
    ch = lambda s: (s[2022] - s[2021]) / s[2021] * 100
    return dict(bastrop_growth=g(B), comparison_growth=g(C), effect=g(B) - g(C), check=ch(B) - ch(C),
                county_growth={c: g(T[col].loc[c]) for c in AUS.values()})
if __name__ == "__main__":
    print(T.to_string())
    for col in ["same_offices", "county_file"]:
        r = calc(col); dec = "SECOND TERM" if abs(r["check"]) <= 40 and r["effect"] >= 20 else "ENDS"
        print(col, {k: (round(v, 3) if not isinstance(v, dict) else {a: round(b, 2) for a, b in v.items()}) for k, v in r.items()}, dec)
