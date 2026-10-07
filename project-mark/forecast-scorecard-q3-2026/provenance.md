# Input package provenance (Project Mark task: Q3 2026 forecast reliability scorecard)

Pulled 2026-10-06. 13 files, 6 formats (CSV, PDF, XLSX, HTML, JSON, TXT). Largest table: EIA930_BALANCE_2024_Jul_Dec.csv (269,426 rows).

| File | Format | Rows | Source | License | Nature | Role |
|---|---|---|---|---|---|---|
| EIA930_BALANCE_2024_Jul_Dec.csv | CSV | 269,426 | U.S. EIA, Form EIA-930 Hourly Electric Grid Monitor, six-month BALANCE file (www.eia.gov/electricity/gridmonitor); pre-July-2024 column schema | Public domain (U.S. Government work) | Real, unmodified | Hourly demand and day-ahead forecast, Jul-Dec 2024 |
| EIA930_BALANCE_2025_Jan_Jun.csv | CSV | 264,934 | Same | Public domain | Real, unmodified | Jan-Jun 2025 |
| EIA930_BALANCE_2025_Jul_Dec.csv | CSV | 267,218 | Same | Public domain | Real, unmodified | Jul-Dec 2025 |
| EIA930_BALANCE_2026_Jan_Jun.csv | CSV | 260,590 | Same | Public domain | Real, unmodified | Jan-Jun 2026 |
| EIA930_BALANCE_2026_Jul_Dec.csv | CSV | 139,512 | Same; live file, data through 5 Oct 2026 at pull time | Public domain | Real, unmodified | Q3 2026 (the period decided); Oct rows outside it |
| About_the_EIA-930_data.pdf | PDF | - | EIA "About the EIA-930 data" page (www.eia.gov/electricity/930-content/about.html), printed to PDF with headless Chromium, no added headers/footers | Public domain | Real content, format conversion only | Data Date meaning, imputation, DST reporting, BAs with non-comparable forecasts, retirements |
| Form_EIA-930_Instructions.pdf | PDF | - | EIA Form EIA-930 instructions (www.eia.gov/survey/form/eia_930/instructions.pdf) | Public domain | Real, unmodified | Definitions of demand and day-ahead forecast, DST reporting |
| EIA930_Reference_Tables.xlsx | XLSX | - | EIA-930 reference tables (www.eia.gov/electricity/930-content/EIA930_Reference_Tables.xlsx) | Public domain | Real, unmodified | BA regions, generation-only flags, activation and retirement dates |
| FCS-STD-2_forecast_reliability_scorecard.html | HTML | - | Authored by task author (fictional desk wiki export) | Task author's own work | Authored scenario document; says so in an HTML comment | Coverage, measure, Watch rule, reproduction gate (section 5) |
| forecast_scorecard_published_2024Q3_2026Q2.csv | CSV | 799 | Derived by task author: the desk's published figures, computed from the shipped EIA files with the golden method (solution/make_history.py) | Derived from public-domain EIA data | Derived file; title row says so | The 799 controls the compilation must reproduce |
| forecast_change_notices.csv | CSV | 17 | Authored by task author (fictional notice register) | Task author's own work | Authored scenario data; title row says so | Bedding-in notices, including three withdrawn |
| sentinel_monitors_export.json | JSON | - | Authored by task author (fictional alerting export) | Task author's own work | Authored scenario document; record_note says so | Desk monitors (texture; no scorecard rule) |
| bi_server_migration_note.txt | TXT | - | Authored by task author (fictional migration note) | Task author's own work | Authored scenario document; header says so | Why the method must be rebuilt; staff recollections (unverified, partly wrong) |
