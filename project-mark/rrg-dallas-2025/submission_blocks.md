# Submission blocks: RRG extension decision (Dallas County, Vintage 2025)

**Task type:** Experiment & Causal Analysis · **Domain:** Urban & Regional Science · **Shape:** Before and after with a control (difference-in-differences with a parallel-movement gate)

## Block 1: Final deterministic recommendation

Extend the Relocation and Retention Grant for a second term, 1 July 2027 to 30 June 2030. On the Census Bureau's Vintage 2025 county estimates, Dallas County's domestically sourced growth (natural change plus net domestic migration, per 1,000 residents at the start of each estimate year) improved by 1.886 points per 1,000 more than the rest of Texas between the base year (2023-24) and the program year (2024-25). That is 0.086 above the 1.80 bar. The parallel-movement check (base year against check year) is -1.404, inside the 1.50 limit by 0.096, so the program can be credited.

## Block 2: Supplementary answers

1. Domestically sourced growth per 1,000 residents at the start of the estimate year, check / base / program year: Dallas County -6.237 / -11.147 / -10.178; rest of Texas +13.222 / +9.716 / +8.799.
2. The effect is (-10.178 - (-11.147)) - (8.799 - 9.716) = +0.969 - (-0.917) = +1.886. The parallel-movement check is (-11.147 - (-6.237)) - (9.716 - 13.222) = -4.910 - (-3.506) = -1.404.
3. Where the change from the base year to the program year came from:
   - Dallas County +0.969: natural change -0.058, domestic migration +1.027.
   - Rest of Texas -0.917: natural change -0.088, domestic migration -0.829.
   - The 1.886 effect splits into domestic migration +1.856 and natural change +0.030.
4. The denominator is the 1 July population that opens each estimate year (POPESTIMATE2022, 2023 and 2024). It is the only basis that reproduces Annex A (Dallas -6.2, rest of Texas +13.2, gap 19.5; unrounded -6.237, +13.222, 19.458). The Census Bureau's published rate columns divide by the average of the opening and closing July populations; that basis gives 13.1 and 19.3 for Annex A and an effect of 1.787, which would wrongly let the program lapse.
5. The numerator is NATURALCHG + DOMESTICMIG. International migration is outside the measure, and the Census residual is not a component of change (methodology statement). Taking total change less international migration keeps the residual and gives an effect of 1.709, below the bar.
6. The rest of Texas is the 253 Texas counties other than Dallas County, with counts and populations summed before the rate is formed (it equals the Texas state row less Dallas County). Averaging the county rates instead gives a check of -1.651, which fails the 1.50 limit.
7. Dallas County's total population change fell from +26,620 (2023-24) to -2,616 (2024-25), almost entirely because net international migration fell from 55,809 to 24,912. On total growth the comparison reads -4.426, but the agreement leaves international migration out, so the "collapse" is not the board's question.
8. Counts behind the rates: Dallas County natural change plus domestic migration -16,302 / -29,398 / -27,113 on start-of-year populations 2,613,911 / 2,637,393 / 2,664,013; rest of Texas +363,652 / +272,831 / +252,123 on 27,504,091 / 28,081,854 / 28,654,565.
9. Census's release notes say the 2024-25 domestic migration estimates used incomplete source data (a 26-week IRS file; ages 65 and over carried forward). The agreement fixes Vintage 2025 as published, so the decision stands, but the 0.086 margin could move when Vintage 2026 revises the year.
10. The workbook sets out both areas for the three years with counts, start-of-year bases, natural change and domestic migration in rate points, the effect, the check, the margins and the decision, plus the Annex A reproduction. The note leads with the recommendation, gives the breakdown and carries a chart of both areas' rates across the three years.

## Block 3: Critical numbers

Effect +1.886 points per 1,000, 0.086 above the 1.80 bar (extend)
Parallel-movement check -1.404, inside the 1.50 limit by 0.096
Program year: Dallas County -10.18, rest of Texas +8.80 per 1,000 (base year -11.15 and +9.72)
Annex A reproduced only on the start-of-year base (-6.24, +13.22, gap 19.46); the Census mid-year rate basis gives 1.787 and a lapse

## Block 4: Path from raw data to recommendation

1. Read the evaluation agreement: measure (births, deaths and domestic moves per 1,000 residents, international migration out), comparison (rest of Texas as one area), years, effect, the parallel-movement check (1.50) and the bar (1.80), and Annex A's worked check-year figures.
2. Load co-est2025-alldata.csv (Latin-1), keep Texas county rows (STATE 48, SUMLEV 50), take Dallas County (COUNTY 113) and pool the other 253 counties.
3. Map the years from the file layout: check year = 2023 columns (7/1/2022 to 7/1/2023), base year = 2024, program year = 2025.
4. Build the numerator from NATURALCHG + DOMESTICMIG, not from NPOPCHG or NPOPCHG less INTERNATIONALMIG.
5. Test the candidate denominators against Annex A. Only the start-of-year population returns -6.2, +13.2 and 19.5; the mid-year average behind Census's published rates returns 13.1 and 19.3, so it is rejected.
6. Compute both areas' rates for the three years on the start-of-year base.
7. Take the effect (program vs base) and the check (base vs check) and compare them, unrounded, with 1.80 and 1.50.
8. Split each area's change into natural change and domestic migration in rate points on the same base.
9. Answer the "collapse" question from the components (international migration) and note the release-notes caveat.
10. Write the workbook, the note and the chart.
