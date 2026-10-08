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
| `swpw-forecast-hold/` | Forecasting | Provisional filing at 4,866 MW (hour ending 2026-08-03 00:00 UTC); first committed filing 2027-10-31 | Matched exactly |

None of these designs reaches the under-50% bar against strong agentic models; kept for reference.
