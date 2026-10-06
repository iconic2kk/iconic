# Input package provenance (Project Mark task: MON-021 v2 threshold)

Pulled 2026-10-06. 10 files, 4 formats (CSV, PDF, XLSX, JSON). Largest table: EIA930_BALANCE_2025_Jul_Dec.csv.

| File | Format | Rows | Source | License | Nature | Role |
|---|---|---|---|---|---|---|
| EIA930_BALANCE_2025_Jul_Dec.csv | CSV | 267218 | U.S. Energy Information Administration, Form EIA-930 Hourly Electric Grid Monitor, six-month BALANCE file (www.eia.gov/electricity/gridmonitor) | Public domain (U.S. Government work; EIA copyright and reuse policy) | Real, unmodified | Replay data, Oct-Dec 2025 |
| EIA930_BALANCE_2026_Jan_Jun.csv | CSV | 260590 | Same as above | Public domain (U.S. Government work) | Real, unmodified | Replay data, Jan-Jun 2026 |
| EIA930_BALANCE_2026_Jul_Dec.csv | CSV | 139512 | Same as above (live file, data through 5 Oct 2026 at pull time) | Public domain (U.S. Government work) | Real, unmodified | Replay data, Jul-Sep 2026; Oct 2026 rows fall outside the window |
| About_the_EIA-930_data.pdf | PDF |  | EIA, 'About the EIA-930 data' page content (www.eia.gov/electricity/930-content/about.html), printed to PDF with headless Chromium, no added headers/footers | Public domain (U.S. Government work) | Real content, format conversion only | Defines generation-only BAs, imputation rules, and the 8 BAs whose actual-vs-forecast comparison is not meaningful |
| Form_EIA-930_Instructions.pdf | PDF |  | EIA, Form EIA-930 instructions (www.eia.gov/survey/form/eia_930/instructions.pdf) | Public domain (U.S. Government work) | Real, unmodified | Defines demand forecast, anomaly suppression (blanks), DST reporting |
| EIA930_Reference_Tables.xlsx | XLSX |  | EIA, EIA-930 data reference tables (www.eia.gov/electricity/930-content/EIA930_Reference_Tables.xlsx) | Public domain (U.S. Government work) | Real, unmodified | BA roster: generation-only flag, active/retired, activation dates (SWPW 1 Apr 2026; WACM/WAUW retired) |
| sentinel_monitors_export.json | JSON |  | Authored by task author as scenario configuration (fictional alerting system export) | Task author's own work | Authored scenario document; says so in export.record_note | MON-021 v2 definition: metric, evaluable hours, candidate thresholds, scope, paging dedupe |
| CHG-2291.json | JSON |  | Authored by task author as scenario ticket (fictional ticketing export) | Task author's own work | Authored scenario document; says so in export_meta.record_note | Acceptance criteria AC1-AC4 (decision rule) |
| oncall_rota_2025-10_to_2026-09.csv | CSV | 12 | Authored by task author as scenario data (fictional rota export) | Task author's own work | Authored scenario data; title row says so | Monthly triage capacity (24 Dec, 26 Jul/Aug, 30 otherwise) |
| MON-021_v1_page_history.csv | CSV | 4424 | Derived by task author: replay of the MON-021 v1 rule (20%, all BAs) over the three EIA BALANCE files above (solution/make_v1_history.py) | Derived from public-domain EIA data | Derived file; title row states how it was produced | v1 page volume for comparison; pages from the 8 out-of-scope BAs |
