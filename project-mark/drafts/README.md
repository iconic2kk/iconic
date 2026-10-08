# Project Mark: draft designs (not submitted)

All drafts use real EIA-930 data. The six-month BALANCE, INTERCHANGE and SUBREGION files are too large to commit; download them
from https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/ (same file names) and place them in each draft's `inputs/`
folder, together with the EIA reference tables and the two EIA PDFs used in `../mon021-forecast-threshold/`.

| Draft | Task type | Golden answer | Blind test (strong model, full tools) |
|---|---|---|---|
| `bf0712-backfill/` | Data Quality Monitoring | Run BF-0712 with incidents removed: 16 incidents / 471 BA-hours / +489.5 GWh once incident 16 (WAUW) is corrected to "leave as reported" (`solution/compute.py` still has it as backfill) | Matched on all 38 incidents |
| `clean-feed-reduced-monitoring/` | Data Quality Monitoring & Alerting | SCL to reduced monitoring at 99.819% clean-hour share, 5.480 points over TPWR (94.339%). Decoys: CISO via the 18-way tie at 100%, DOPD without the neighbour-tie check, TPWR under the withdrawn 5 MW allowance | Both runs matched exactly |
| `gv-unit-tiers/` | Descriptive & Distribution Analysis | 2027 verification tiers from EIA-860M (Aug 2026): Tier 1 >= 199.8 MW (179 units), Tier 2 >= 49.0 MW (634), 783 tests, fits the 800 crew-day budget. Trap: generator rows instead of EIA-860 units (954 tests, over budget). EIA-860/860M files are public and must be downloaded from eia.gov | First run matched exactly (second stopped) |
| `rrg-v3-template/` | Experiment & Causal Analysis | v3 of `../rrg-dallas-2025/`: worked example removed, start-of-year base defined in a definitions annex, analysts' template wired to Census mid-year rates (gives 1.787, lapse). Golden unchanged: extend at 1.886 | Both runs solved (overrode the template). v2 on the platform: 100% / 100% |
| `rrg-v4-residual/` | Experiment & Causal Analysis | v4: measure worded as components of change other than international migration; template takes total less international (keeps the residual, gives 1.709, lapse). Golden: extend at 1.886 | First run solved (spotted the residual from the methodology statement); second stopped |
| `bps-accelerator/` | Experiment & Causal Analysis | Census Building Permits Survey held-out office: Bastrop County unincorporated area reported 2021-22 but entered county totals only in Jan 2023. Same-office basis: effect +17.7 vs 20 bar, program ends; county files: +144.8, second term. Census BPS files from www2.census.gov/econ/bps | First run solved (reconciled place file to county totals); with a requester-practice line added (`prompt_with_practice_line.md`) a fresh run still solved it |
| `naics519-travis/` | Root Cause Analysis (Economics & Econometrics) | Board tracker's NAICS 519 line in Travis County falls 6,883 to 480 in 2022Q1 because QCEW moved to NAICS 2022 (519130's 6,608 jobs recoded to 513/516/519290), not tech layoffs. End-2021 to end-2023 on unchanged codes (518+5415): +2,583; real losses came in 2023 (-4,999 Dec 2022 to Dec 2023). `solution/rca.py` uses the wider 511+515+519 group (+2,493); both agents preferred the narrower unchanged-code basis, which is the more defensible golden | Both runs solved with the same figures (+2,583, -4,999) and also caught a second break (about 1,000 jobs entering new 519 in Jan 2023) |
| `swpw-forecast-hold/` | Forecasting | Provisional filing at 4,866 MW (hour ending 2026-08-03 00:00 UTC); first committed filing 2027-10-31 | Matched exactly |

None of these designs reaches the under-50% bar against strong agentic models; kept for reference.

## Scouted, not built

- **Hidden Simpson's flip, Census school finances (F-33), Texas FY2019 to FY2023.** Real composition gaps exist: across Texas
  counties with four or more districts, pooled per-pupil instruction growth differs from the within-district (base-enrollment
  weighted) growth by up to about 10 points (Harrison County +57.8 pooled vs +47.7 within, driven by a district hosting a
  statewide virtual program; Karnes County +14.9 vs +21.1). Not built because nothing in the real F-33 documentation makes the
  within-district figure the determinate one: only an explicit rule (which strong models follow) or a requester-practice line
  (flagged as bait on review) would, and the enrollment jumps behind the gaps are visible enough that agents investigate them.
  Files: www2.census.gov/programs-surveys/school-finances/tables/YYYY/secondary-education-finance/ (elsec22.txt on the server is
  truncated; use elsec22.xlsx).
