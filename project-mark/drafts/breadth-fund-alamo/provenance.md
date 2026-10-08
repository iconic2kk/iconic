# Provenance: inputs.zip (12 files, 5 formats: CSV, PDF, XLSX, PPTX, DOCX)

Large files: qcew_aacog_counties_annual_2018_2025.csv (110,540 rows) and BLS_Handbook_of_Methods_QCEW.pdf (19 pages).

## Real public files (U.S. Bureau of Labor Statistics and U.S. Census Bureau)

| File | Source |
|---|---|
| qcew_aacog_counties_annual_2018_2025.csv | https://data.bls.gov/cew/data/api/{2018..2025}/a/area/{fips}.csv for the 13 AACOG counties, stacked as published |
| qcew_aacog_counties_2026_q1.csv | https://data.bls.gov/cew/data/api/2026/1/area/{fips}.csv for the same counties, stacked |
| qcew_industry_titles.csv | https://data.bls.gov/cew/doc/titles/industry/industry_titles.csv |
| QCEW_annual_file_layout.pdf | https://www.bls.gov/cew/about-data/downloadable-file-layouts/annual/naics-based-annual-layout.htm (printed) |
| BLS_Handbook_of_Methods_QCEW.pdf | https://www.bls.gov/opub/hom/cew/ (home, data, concepts, design, calculation, presentation pages printed and joined) |
| 2017_to_2022_NAICS.xlsx | https://www.census.gov/naics/concordances/2017_to_2022_NAICS.xlsx |

## Authored scenario files (each labelled "authored for this exercise")

| File | Role |
|---|---|
| compact_charter.pdf | Terms document: purpose, members, fund size, data basis (Article 3.4), notices and transition reserve (Article 4). Says what the fund does, not how draws are computed. Source HTML in `src/`. |
| board_minutes_2025_11_20.docx | 2025 round confirmed "in the same way as every round since the first in 2020"; Medina's complaint; finance office told to rebuild and test its model. |
| member_counties.csv | Roster with county FIPS codes. |

## Files derived from the BLS counts by script (`build/build_pack.py`)

| File | Role |
|---|---|
| breadth_fund_ledger_2020_2025.xlsx | Confirmed draws for the 2020 to 2025 rounds (78 lines), notices, transition payments, reserve. Computed with the fund's method from the real counts. |
| finance_projection_2025_round.pdf | June 2025 projection that moved each 2024 draw with the county's own establishment count (Medina $144,482). |
| finance_projection_2026_round.pptx | The distractor: model v2, which counts every industry carried in the latest year. Ties the 2023 to 2025 rounds exactly; names Gillespie and $8,240. |
