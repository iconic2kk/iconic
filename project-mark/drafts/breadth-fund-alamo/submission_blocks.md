# Breadth Fund 2026 round: submission blocks

Task type: Root-Cause Analysis. Domain: Economics & Econometrics.

## Block 1. Final recommendation

Send one Article 4 notice, to Wilson County, whose 2026 draw falls 11.7% from $117,147 to $103,409, and pay it $6,869 from the transition reserve; do not issue the finance office's model v2 projection, which names Gillespie County and an $8,240 payment.

## Block 2. Supplementary answers

1. 2026 draws (total $4,999,998 after rounding): Atascosa $87,189; Bandera $33,828; Bexar $2,986,255; Comal $653,087; Frio $8,011; Gillespie $132,778; Guadalupe $469,198; Karnes $40,205; Kendall $258,211; Kerr $142,998; McMullen $4,876; Medina $79,953; Wilson $103,409.
2. Article 4 notices: Wilson County only (down 11.73%). Transition reserve payout: $6,869. Gillespie is the closest other county at down 9.12%; no other county falls by more than 10%.
3. Medina's gap: the June 2025 projection showed $144,482 and the board confirmed $77,368, a gap of $67,114. The fund splits each round equally across the four-digit manufacturing industries the region carried in both the counts year and the year before, and splits each industry's part by the counties' shares of its establishments. Medina had the region's only yarn, fiber and thread mill (NAICS 3131) in the 2023 counts and held that industry's whole part, $60,240.96, in the 2024 round (83 qualifying industries). The mill is absent from the 2024 counts, so 3131 left the region and Medina lost the part. The projection moved Medina's 2024 draw of $150,261 by its own establishment count (26 to 25) and could not see this. The confirmed draw was right; the projection method caused the gap.
4. Finance office model v2: it reproduces the 2023, 2024 and 2025 rounds but misses all 13 counties in each of the 2020, 2021 and 2022 rounds. It counts every industry carried in the 2025 counts (84), including pulp, paper and paperboard mills (NAICS 3221, one establishment in Bexar) and household appliances (NAICS 3352, two in Wilson), which are in their first year and take no part in the 2026 round. It overstates Wilson by $57,061 ($160,470 against $103,409), shows Wilson rising 37.0% instead of falling 11.7%, and names Gillespie (down 11.3%) for the notice.
5. Workbook: one sheet of county by industry establishment counts for 2024 and 2025; one sheet listing each four-digit industry with its region totals for both years, a flag for carried in both years (82 flagged) and its part of the fund ($60,975.61 each); one sheet of the 13 counties with the 2026 draw (formula), the 2025 ledger draw, the change, the notice flag and the transition payment; a backtest sheet with all 78 ledger lines from 2020 to 2025 against the rebuilt draws (no differences); a sheet comparing model v2 with the 2026 draws and naming the two first-year industries; and a Medina sheet with its industry parts in the 2024 and 2025 rounds and the projection gap.
6. Note: one to two pages for the directors, opening with the Wilson notice and the $6,869 payment, then why model v2 should not be issued, then the Medina explanation, then a chart and a table of the 13 draws. The chart is a dot plot of each county's change in draw from the 2025 round to the 2026 round, the fund's figure against model v2, with the minus 10% notice line marked; only Wilson's fund figure sits past the line and only Gillespie's model v2 figure does.

## Block 3. Critical numbers and components

1. Allocation basis: the fund is split equally across qualifying four-digit manufacturing industries (82 in the 2026 round, $60,975.61 each), and each industry's part is split by the counties' annual average private establishment counts. This reproduces all 78 confirmed draws in the ledger to the dollar.
2. Qualification: an industry takes part only if the region carried it in both the counts year and the year before. For the 2026 round this excludes NAICS 3221 (Bexar) and 3352 (Wilson).
3. Wilson's 2026 draw of $103,409 against $117,147 in 2025 (down 11.73%) is the only fall of more than 10%; Gillespie is down 9.12%.
4. Transition reserve payout: $6,869.

## Block 4. Path to recommendation

1. From qcew_aacog_counties_annual_2018_2025.csv keep rows with own_code 5, agglvl_code 76, industry_code starting 31, 32 or 33 and annual_avg_estabs above 0; map area_fips to county with member_counties.csv.
2. For each round R, take the counts year Y = R minus 1. A four-digit industry qualifies if the 13 counties together have establishments in it in year Y and in year Y minus 1.
3. Each qualifying industry's part is 5,000,000 divided by the number of qualifying industries. A county receives the part times its annual_avg_estabs in the industry divided by the 13 counties' total in the industry. Sum over industries and round half up to the dollar.
4. Rebuild the 2020 to 2025 rounds and compare with the Draws sheet of breadth_fund_ledger_2020_2025.xlsx: all 78 lines match. Counting every industry carried in year Y instead fails 39 lines (every county in 2020, 2021 and 2022).
5. 2026 round on the 2025 counts: 84 industries carried, 82 qualifying (3221 and 3352 are first-year), part $60,975.61. Draws: Atascosa $87,189; Bandera $33,828; Bexar $2,986,255; Comal $653,087; Frio $8,011; Gillespie $132,778; Guadalupe $469,198; Karnes $40,205; Kendall $258,211; Kerr $142,998; McMullen $4,876; Medina $79,953; Wilson $103,409.
6. Compare each 2026 draw with the 2025 ledger draw. Only Wilson is below 90% ($103,409 against a 90% mark of $105,432.30). Transition payment: ($117,147 minus $103,409) divided by 2 = $6,869.
7. Medina: in the 2024 round (2023 counts, 83 qualifying industries) Medina held 1 of 1 establishment in NAICS 3131, a part of $60,240.96. NAICS 3131 has no establishments in the 2024 counts. The June projection was $150,261 times 25/26 = $144,482.
8. Model v2 is step 3 using all 84 carried industries: Wilson $160,470, Gillespie $129,617 (down 11.3%), payout $8,240. Reject it because it fails the 2020 to 2022 rounds.

## File-type justification

The auditor needs to follow every draw from the BLS counts, so the workbook is an Excel file with live formulas from the establishment counts through the industry parts to each county's draw, plus the full ledger backtest. The directors need a short readable paper, so the note is a Word document of one to two pages. The chart is embedded in the note because the decision is visual: which county's change crosses the minus 10% line under the fund's method and under the finance office's model.

## Stumping strategy

1. Unwritten, concentration-shaped allocation rule. A county's draw depends on how many establishments the other counties hold in each industry and on how many industries qualify, not on its own counts. The charter describes the purpose only. Models tend to assume own-figure weights. Expected wrong output: Medina explained by its own counts or regional shares, with notices to Comal, Guadalupe and Medina and a $75,997 payout, or no notices at all under the old projection method.
2. Unwritten qualification rule, learned only from the older rounds and needed in the forward round. The 2022 to 2024 counts have no first-year industries, so any rule fitted to the three most recent rounds misses it; the 2025 counts contain two. Expected wrong output: Gillespie notice and $8,240.
3. Distractor equal to the shortcut. The finance office's deck shows exactly the figures of the rule fitted to recent rounds, with a perfect 2023 to 2025 backtest, so a solver on that path sees confirmation and stops.
4. Newer data in the pack. The 2026 first-quarter file is the latest BLS release but not the counts the charter names; using it gives no notices.
5. The decision flips by county: Wilson under the right method, Gillespie under the distractor, three other counties under regional shares, none under the old projection.

## Distractor

File: finance_projection_2026_round.pptx (slides 3 to 5). It shows the finance office's rebuilt model v2 reproducing every county's confirmed draw in the 2023, 2024 and 2025 rounds to the dollar, a full table of projected 2026 draws, and a notice to Gillespie County with an $8,240 transition payment. It looks right because it is the office's official revision made at the board's request, it uses the same BLS counts and four-digit industries, and its backtest ties exactly. It is wrong because it counts every industry carried in the latest counts year. The ledger's 2020 to 2022 rounds show that an industry in its first year in the region takes no part, which model v2 fails on all 39 lines of those rounds. In the 2026 round that wrongly adds NAICS 3221 (Bexar) and 3352 (Wilson), handing Wilson a whole industry's part and moving the notice from Wilson to Gillespie.
