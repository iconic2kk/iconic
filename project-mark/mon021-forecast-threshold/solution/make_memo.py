import json
import pandas as pd
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

f = json.load(open("facts.json")); S = {int(k): v for k, v in f["summary"].items()}; F = {int(k): v for k, v in f["fleet"].items()}
rep = pd.read_csv("replay_table.csv")
c = f["chosen"]; sc = S[c]
mon = lambda m: pd.Period(m).strftime("%B %Y")
cap_peak = sc["peak"] + sc["min_headroom"]
miss100 = S[100]["missed_rows"][0]

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2.0); s.top_margin = s.bottom_margin = Cm(1.8)

def para(text="", bold=False, size=None, space=4, italic=False):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(space); return p

def mixed(parts, space=4):
    p = doc.add_paragraph()
    for t, b in parts:
        r = p.add_run(t); r.bold = b
    p.paragraph_format.space_after = Pt(space); return p

def head(text):
    p = para(text, bold=True, size=11.5, space=2); p.paragraph_format.space_before = Pt(8)

para("MON-021 v2 threshold decision (CHG-2291)", bold=True, size=15, space=2)
para("To: grid-data-ops on-call leads    From: grid-data-ops    Date: 6 October 2026", size=9.5, space=8)

head("Decision")
mixed([("Ship MON-021 v2 at 75%. ", True),
       (f"It is the lowest candidate that stays within the rota's triage capacity in all twelve months of the replay "
        f"(October 2025 to September 2026) and that alerted on all {f['imputed_evaluated']} evaluated hours in which EIA "
        f"later imputed demand. The month closest to capacity is {mon(sc['peak_month'])}: {sc['peak']} pages against "
        f"{cap_peak}, {sc['min_headroom']} pages of headroom. ", False),
       (f"We reject 50% and 25%, which breach capacity in {S[50]['months_over']} and {S[25]['months_over']} of 12 months, "
        f"and 100% and 150%, which fit the rota but miss {S[100]['missed']} and {S[150]['missed']} hours that EIA had to impute.", False)])

head("How each candidate performed")
t = doc.add_table(rows=1, cols=6); t.style = "Light Grid Accent 1"
hdr = ["Threshold", "Busiest month (pages / capacity)", "Months over capacity", "First month over capacity",
       f"EIA-imputed hours missed (of {f['imputed_evaluated']})", "Pages in year"]
for i, h in enumerate(hdr):
    t.rows[0].cells[i].text = h
for th in [25, 50, 75, 100, 150]:
    s = S[th]
    pk_cap = int(rep[(rep.threshold_pct == th) & (rep.month == s["peak_month"])].triage_capacity_pages.iloc[0])
    first = f"{mon(s['first_over'])} ({s['first_over_pages']} vs {s['first_over_cap']})" if s["first_over"] else "none"
    vals = [f"{th}%" + ("  (ship)" if th == c else ""), f"{mon(s['peak_month'])}: {s['peak']} / {pk_cap}",
            str(s["months_over"]), first, str(s["missed"]), f"{s['total']:,}"]
    row = t.add_row().cells
    for i, v in enumerate(vals):
        row[i].text = v
        if th == c:
            for r in row[i].paragraphs[0].runs: r.bold = True
for row in t.rows:
    for cell in row.cells:
        for p in cell.paragraphs:
            for r in p.runs: r.font.size = Pt(9)
para("", space=2)
mixed([("The setting just below the pick, 50%, first breaks in January 2026 ", True),
       (f"({S[50]['first_over_pages']} pages against a capacity of {S[50]['first_over_cap']}) and stays over capacity in every "
        f"month from January to September 2026, peaking at {S[50]['peak']} pages in {mon(S[50]['peak_month'])}. ", False),
       ("The setting just above, 100%, ", True),
       (f"misses one imputed hour: {miss100[0]}, hour ending {miss100[1][:16]} UTC, reported {float(miss100[2]):,.0f} MW against a "
        f"day-ahead forecast of {float(miss100[3]):,.0f} MW. EIA imputed {float(miss100[4]):,.0f} MW; the deviation is "
        f"{float(miss100[5])*100:.2f}%, just under the 100% line, so v2 at 100% would have stayed silent on a doubled demand value.", False)])

head("Scope: which BAs v2 evaluates")
mixed([(f"v2 evaluates {f['evaluated_bas']} BAs. Eight BAs stay on MON-014 only: AVA, FPC, GVL, LGEE, PSEI, SEC, SPA and TEPC. ", True),
       ("EIA's documentation for the EIA-930 data states that for these systems a significant share of demand sits outside "
        "their system or is controlled by other BAs through pseudo-ties and dynamic scheduling, so the comparison between "
        "actual and forecast demand is not very meaningful. Their forecasts describe a different load from the demand they "
        "report, which fails v2's scope test. Their reported numbers are not wrong; the forecast is simply not a valid "
        "reference for them. Generation-only BAs report neither demand nor a demand forecast, so v2 never evaluates them. "
        "WALC and FMPP stay in scope despite being noisy, as CHG-2291 requires: WALC is the largest source of pages at 75% "
        f"({f['v2_by_ba_chosen']['WALC']} of {sc['total']}).", False)])
mixed([(f"Of v1's {f['v1_total']:,} pages over the same twelve months, {f['v1_from_nc']:,} ({f['v1_from_nc']/f['v1_total']*100:.1f}%) came from those eight BAs ", True),
       ("(" + ", ".join(f"{k} {v}" for k, v in f["v1_nc_by_ba"].items()) + "). "
        f"FPC and PSEI paged on every day of the year. v2 at 75% would have sent {sc['total']} pages in the same period, "
        f"{f['v1_total'] - sc['total']:,} fewer than v1.", False)])

head("How the replay was built")
for b in [
    "Data: the three published EIA-930 BALANCE six-month files covering July 2025 to October 2026, stacked and keyed on BA "
    "and 'UTC Time at End of Hour' (no duplicate BA-hours across files). Only hours whose UTC end-timestamp date falls between "
    "1 October 2025 and 30 September 2026 are replayed; the October 2026 rows in the live July-December 2026 file are outside the window.",
    "Values: the reported 'Demand (MW)' column, not the adjusted series, because v2 alerts on what BAs report. An hour is "
    "evaluated only when demand is reported and the day-ahead forecast is above zero; deviation = |demand - forecast| / forecast, "
    "and an alert fires when it exceeds the threshold.",
    "Paging: one page per BA per UTC date of the hour-end timestamp, counted in that date's month and compared with that "
    "month's triage capacity on the rota export (24 in December 2025, 26 in July and August 2026, 30 otherwise).",
    f"Recall: {f['imputed_evaluated']} evaluated hours have a populated 'Demand (MW) (Imputed)' value although the BA reported "
    f"demand. Two further imputed FMPP hours had no day-ahead forecast, so v2 cannot evaluate them and they are outside AC3.",
]:
    p = doc.add_paragraph(b, style="List Bullet"); p.paragraph_format.space_after = Pt(2)

head("Why no other answer survives")
para(f"Running v2 across every BA in the feed, as v1 does, including the eight whose forecasts are not comparable, "
     f"would fail every candidate: 75% would breach capacity in all 12 months (peak {F[75]['peak']} pages), 100% in "
     f"{F[100]['months_over']} months, and 150% in {F[150]['months_over']} months while missing {F[150]['missed']} imputed hours. "
     "That 'nothing ships' result comes from forecasts that measure a different load, not from bad data, so it is not a valid "
     "reading of the change. Inside the configured scope the ranking is unambiguous: below 75% capacity binds, above 75% "
     "recall breaks, and 75% clears both. The call would flip only if May 2026's capacity fell below 26 pages, or if an "
     f"imputed hour had deviated by 75% or less; the closest imputed hour in the replay deviated by {f['min_imputed_dev']*100:.2f}%.", space=4)
doc.save("../golden/MON-021_v2_threshold_memo.docx")
print("saved")
