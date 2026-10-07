# Project Mark: draft designs (not submitted)

Both drafts use real EIA-930 data. The six-month BALANCE, INTERCHANGE and SUBREGION files are too large to commit; download them
from https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/ (same file names) and place them in each draft's `inputs/`
folder, together with the EIA reference tables and the two EIA PDFs used in `../mon021-forecast-threshold/`.

| Draft | Task type | Golden answer | Blind test (strong model, full tools) |
|---|---|---|---|
| `bf0712-backfill/` | Data Quality Monitoring | Run BF-0712 with incidents removed: 16 incidents / 471 BA-hours / +489.5 GWh once incident 16 (WAUW) is corrected to "leave as reported" (`solution/compute.py` still has it as backfill) | Matched on all 38 incidents |
| `swpw-forecast-hold/` | Forecasting | Provisional filing at 4,866 MW (hour ending 2026-08-03 00:00 UTC); first committed filing 2027-10-31 | Matched exactly |

Neither design reaches the under-50% bar against strong agentic models; kept for reference.
