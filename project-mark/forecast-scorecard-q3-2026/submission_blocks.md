# Submission blocks: Q3 2026 forecast reliability scorecard

**Task type:** Data Quality Monitoring & Alerting · **Domain:** Energy Systems & Utilities · **Shape:** Ranked list under a cap (top five), gated by reproduction of published controls

## Block 1: Final deterministic recommendation

Put PSCO, WALC, SWPW, SRP and LDWP on Forecast Watch for Q4 2026, and send the formal letter to PSCO. PSCO's Q3 2026 forecast error is 26.9% (26.95 unrounded), 4.97 points above WALC at 22.0%. LDWP takes the fifth Watch place at 8.65%, 0.24 points ahead of CISO at 8.40%, which stays off Watch. This rests on the only compilation that reproduces all 799 published figures: reporting-day months, with EIA-imputed hours, forecast-flatline days, 14-day bedding-in windows after active notices and daylight-saving changeover days left out.

## Block 2: Supplementary answers

1. scorecard_q3_2026.csv has one row per Q3 scorecard BA: 25 rows (the 27 published BAs less WACM and WAUW, retired 1 April 2026). Each row gives the Q3 forecast error and the July, August and September figures to one decimal, the Q3 rank and the Watch flag.
2. The top six, Q3 / Jul / Aug / Sep %: PSCO 26.9 / 29.3 / 26.1 / 24.9; WALC 22.0 / 12.8 / 30.4 / 23.4; SWPW 10.0 / 3.3 / 15.6 / 15.1; SRP 9.2 / 6.9 / 9.2 / 12.0; LDWP 8.6 / 7.8 / 7.5 / 12.8; CISO 8.4 / 8.3 / 8.4 / 8.5. The first five are on Watch.
3. Letter margin: PSCO over WALC by 4.97 points (26.95 against 21.98 unrounded).
4. Watch-cut margin: fifth-placed LDWP (8.65) over sixth-placed CISO (8.40) by 0.24 points. PACE is seventh at 8.22.
5. The compilation:
   - Periods use the BA's reporting day (EIA-930 "Data Date"), not UTC.
   - Scored hours need reported demand and a day-ahead forecast above zero.
   - Four exclusions apply:
     - hours where EIA imputed demand;
     - forecast-flatline days (every forecast for the reporting day the same value);
     - the effective reporting day of each active forecast-change notice and the next 13 days (withdrawn notices do not count);
     - reporting days with 23 or 25 hours.
   - Forecast error is the sum of |demand − forecast| over the sum of demand, times 100. Quarters are computed directly and ranked before rounding.
6. The note's annex sets all 799 published figures (599 monthly, 200 quarterly, Q3 2024 to Q2 2026) beside the compiled figure. The difference is 0.0 on every one.
7. Closest reading that does not stand: counting withdrawn notices as bedding-in. It reproduces 795 of 799, missing GCPD Apr 2025 and Q2 2025 and PACE Sep 2025 and Q3 2025. It gives the same Watch list, but CISO falls to 8.24% and the cut margin reads 0.40.
8. Closest reading that changes the call: no bedding-in (775 of 799), or bedding-in to the end of the effective month as the migration note remembers (779 of 799). LDWP falls to 8.20% or 7.67%, and CISO goes on Watch in its place. Bedding-in lengths of 13 and 15 days reproduce 789 and 783.
9. Other rejected readings:
   - keeping EIA-imputed hours (723 of 799) sends the letter to WALC at 46.4%;
   - UTC months with no screens (495 of 799) puts WALC first and NEVP fifth.
10. The note includes a ranked bar chart of Q3 2026 forecast error for all 25 scorecard BAs, with the five Watch BAs highlighted and the cut marked between LDWP and CISO.

## Block 3: Critical numbers

799 of 799 published figures reproduced, and only by the five-rule compilation (14-day bedding-in pinned: 13 days gives 789, 15 days gives 783)
PSCO 26.95% (letter), 4.97 points above WALC at 21.98%
LDWP 8.65% in fifth place, 0.24 points above CISO at 8.40% (LDWP's bedding-in covers 12 to 25 September 2026)
NEVP 2 July 2026 flatline day excluded (NEVP 7.78% rather than 8.56%)

## Block 4: Path from raw data to recommendation

1. Read FCS-STD-2. The measure, the Watch rule and the section 5 gate are fixed; "valid" hours, the period key and the bedding-in length are not.
2. Stack the five EIA-930 BALANCE files and scope the Western scorecard BAs (CAL, NW, SW; not generation-only; not AVA, PSEI or TEPC). This gives 27 published BAs, 25 active in Q3.
3. Compile the obvious reading (UTC months, every hour with demand and a forecast above zero). It matches only 495 of 799, so it cannot be used.
4. Switch periods to the BA reporting day (Data Date): 664 of 799.
5. Drop hours where EIA imputed demand: the remaining misses cluster in March and November months for DST-observing BAs, in NEVP months, and in BA-months with forecast-change notices.
6. Drop reporting days with 23 or 25 hours (the DST changeovers).
7. Drop days on which the BA's forecast is one value all day (NEVP 692 MW).
8. Join the notice register. Excluding bedding-in from the effective reporting day, active notices only, and searching the length against the archive gives 14 days as the only length returning all 799.
9. Compile Q3 2026 on that method, rank before rounding, and take the top five and the letter. The result is PSCO, WALC, SWPW, SRP, LDWP, with the letter to PSCO.
10. Compute the margins (4.97 and 0.24), compile the near-miss readings to show where they part, and write the CSV and the note with the annex and the chart.
