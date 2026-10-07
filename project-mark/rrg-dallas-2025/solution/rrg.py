"""RRG evaluation (golden method). Reads only the shipped inputs.
Rate = (NATURALCHG + DOMESTICMIG) / POPESTIMATE at the start of the estimate year x 1,000 (residual and international
migration left out); rest of Texas pooled (counts summed). Annex A check year reproduces exactly (-6.24 / +13.22 / 19.46)."""
import os
import pandas as pd
IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inputs")
d = pd.read_csv(os.path.join(IN, "co-est2025-alldata.csv"), encoding="latin-1")
tx = d[(d.STATE == 48) & (d.SUMLEV == 50)]
AREAS = {"Dallas County": tx[tx.CTYNAME == "Dallas County"], "Rest of Texas": tx[tx.CTYNAME != "Dallas County"]}
YEARS = {"check": 2023, "base": 2024, "program": 2025}
rows = []
for a, g in AREAS.items():
    s = g.sum(numeric_only=True)
    for lab, y in YEARS.items():
        b = s[f"POPESTIMATE{y-1}"]
        rows.append(dict(area=a, year=lab, period=f"7/1/{y-1} to 7/1/{y}", start_pop=b, natural=s[f"NATURALCHG{y}"], domestic=s[f"DOMESTICMIG{y}"],
                         nat_rate=s[f"NATURALCHG{y}"] / b * 1000, dom_rate=s[f"DOMESTICMIG{y}"] / b * 1000,
                         rate=(s[f"NATURALCHG{y}"] + s[f"DOMESTICMIG{y}"]) / b * 1000))
t = pd.DataFrame(rows).set_index(["area", "year"])
r = t["rate"]
eff = (r["Dallas County", "program"] - r["Dallas County", "base"]) - (r["Rest of Texas", "program"] - r["Rest of Texas", "base"])
chk = (r["Dallas County", "base"] - r["Dallas County", "check"]) - (r["Rest of Texas", "base"] - r["Rest of Texas", "check"])
if __name__ == "__main__":
    pd.set_option("display.width", 200)
    print(t.round(3).to_string())
    print("effect", round(eff, 4), "margin over 1.80", round(eff - 1.80, 4))
    print("check", round(chk, 4), "inside 1.50 by", round(1.50 - abs(chk), 4))
    for a in AREAS:
        dn = t.loc[(a, "program"), "nat_rate"] - t.loc[(a, "base"), "nat_rate"]; dd = t.loc[(a, "program"), "dom_rate"] - t.loc[(a, "base"), "dom_rate"]
        print(a, "change natural", round(dn, 3), "domestic", round(dd, 3), "total", round(dn + dd, 3))
    print("decision:", "EXTEND" if abs(chk) <= 1.5 and eff >= 1.8 else "LAPSE")
