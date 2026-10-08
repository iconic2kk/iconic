# Breadth Fund 2026 round (Root-Cause Analysis, Economics & Econometrics)

Built to the handoff playbook and the 8 October 2026 rules: two large files, one distractor named only in the form, no dashes, prompt silent on method.

## Mechanism
- History with a tie-out: the round ledger (2020 to 2025, 78 county draws) reproduces exactly from the BLS counts.
- Two rules written nowhere, both recoverable from the ledger: (H1) the fund is split equally across qualifying four-digit manufacturing industries and each part follows the counties' establishment shares (concentration-shaped); (H2) an industry qualifies only if the region carried it in the counts year and the year before.
- The 2022 to 2024 counts have no first-year industries, so a rule fitted to the three most recent rounds (H1 alone) ties them exactly. The 2025 counts have two first-year industries (3221 in Bexar, 3352 in Wilson). Nothing in the pack checks the 2026 round.
- The distractor (finance office model v2) is H1 alone, with its perfect three-round backtest on show.
- RCA element: Medina's 2025 drop is the loss of the region's only NAICS 3131 establishment, a whole industry part.

## Uniqueness (design/unique.py)
Golden misses 0 of 78 ledger lines. H1 alone 39; three years running 39; either of two prior years 26; half weight for entry year 39; county-level qualification 72; 2+ establishments 78; equal split among hosts 78; establishments over hosting counties 78; own share of manufacturing establishments 78; 3-digit industries 78; data year equal to round year 78.

## Wrong-path map (2026 round)
| Path | Wilson | Gillespie | Notices | Reserve |
|---|---|---|---|---|
| Golden | 103,409 | 132,778 | Wilson | 6,869 |
| Model v2 (distractor) | 160,470 | 129,617 | Gillespie | 8,240 |
| Golden method on 2026 Q1 counts | 162,659 | 144,425 | none | 0 |
| Share of region's manufacturing establishments | 125,409 | 234,460 | Comal, Guadalupe, Medina | 75,997 |
| Old projection (own count change) | 131,433 | 141,172 | none | 0 |
| 2025 shares carried forward | 117,147 | 146,097 | none | 0 |
(Three years running gives the golden 2026 figures but fails 39 ledger lines.)

## Robustness
- No 2026 county draw has an exact fractional part within 0.03 of a half dollar; Excel ROUND and exact half-up agree (workbook recalculated in LibreOffice matches).
- Margins: Wilson down 11.73% (1.73 points past the line); Gillespie down 9.12% (0.88 points short).
- Second implementation (solution/check_independent.py, csv module and integer arithmetic) matches all 78 ledger lines and every 2026 figure.

## Rebuilding
`python3 solution/golden.py inputs.zip` (figures.json), `python3 solution/make_golden.py inputs.zip` (workbook, note, chart; needs LibreOffice), `python3 solution/wrong_paths.py inputs.zip out.json`.
