# Project Mark task: MON-021 v2 forecast-deviation threshold

**Task type:** Data Quality Monitoring & Alerting · **Domain:** Energy Systems & Utilities
**Shape:** Setting one dial (lowest candidate that clears a fixed bar), with a month-by-month capacity grid

## What to upload where

| Platform step | File |
|---|---|
| Prompt | `prompt.md` (paste the text) |
| Input files (ZIP) | `inputs.zip`: 10 files, 4 formats, largest table 267,218 rows |
| File record / provenance | `provenance.md` / `provenance.csv` |
| Golden deliverables | `golden/MON-021_v2_threshold_memo.docx`, `golden/MON-021_v2_replay_by_month.csv`, `golden/MON-021_v2_monthly_pages.png` |

`solution/` holds the scripts that produce every golden number from the shipped files only. Running `compute.py` against a fresh unzip of `inputs.zip` reproduces the golden CSV byte for byte.

## The answer

**Ship MON-021 v2 at 75%.** Peak month: May 2026, 26 pages against a capacity of 30. All 91 evaluated EIA-imputed hours raised an alert.

| Threshold | Busiest month | Months over capacity | Imputed hours missed (of 91) | Pages/year |
|---|---|---|---|---|
| 25% | May 2026: 226 / 30 | 12 (first Oct 2025, 149 vs 30) | 0 | 2,037 |
| 50% | May 2026: 106 / 30 | 9 (first Jan 2026, 38 vs 30) | 0 | 629 |
| **75%** | **May 2026: 26 / 30** | **0** | **0** | **187** |
| 100% | May 2026: 17 / 30 | 0 | 1 (WACM, hour ending 2026-01-26 13:00 UTC, 99.92%) | 100 |
| 150% | Mar 2026: 13 / 30 | 0 | 34 | 73 |

- Out of scope (stay on MON-014): AVA, FPC, GVL, LGEE, PSEI, SEC, SPA, TEPC. 47 BAs are evaluated.
- v1 sent 4,424 pages over the year. 1,581 of them (35.7%) came from those 8 BAs: FPC 365, PSEI 365, SPA 364, SEC 245, GVL 218, TEPC 12, LGEE 9, AVA 3.

## Where the difficulty comes from (all honest data)

1. **Main trap: forecast comparability.** v2's config limits scope to BAs whose forecast and reported demand "describe the same load". The only place that names those BAs is buried in the middle of the 13-page EIA About PDF ("Impact of pseudo-ties and dynamic scheduling on demand forecast"). Their data is correct; their forecast just measures a different load. Replaying all BAs makes **every** candidate fail: 75% is over capacity in all 12 months (peak 85), and 150% is over in 6 months and misses 71 hours. A model that misses this concludes "nothing ships" or picks the wrong setting.
2. **Capacity is not flat.** The rota sets 24 in Dec 2025 and 26 in Jul/Aug 2026; the ticket comment warns about this.
3. **Window edges.** The live Jul–Dec 2026 file includes rows from 1–5 Oct 2026, which must be dropped. Months are keyed on the UTC date of the hour-end timestamp.
4. **Recall universe.** Two imputed FMPP hours have no forecast, so v2 can't evaluate them and they fall outside AC3. Counting them as misses fails every candidate.
5. **Raw vs adjusted.** The replay has to use the reported `Demand (MW)` column, not `Demand (MW) (Adjusted)`.
6. **Red herring.** Dropping noisy-but-valid BAs (WALC, FMPP) is explicitly ruled out in the ticket.
7. **Texture.** Schema drift across files, DST hour 25, generation-only BAs with blank demand, and the April 2026 BA roster change (WACM and WAUW retire, SWPW appears).

## Still to do on your side

- Run the models against the task and check they score under 50%. I could not run the platform's models from here.
