# Submission blocks: MON-021 v2 go-live

## Block 1: Final deterministic recommendation

Hold: MON-021 v2 cannot ship at any of the five candidate thresholds (25%, 50%, 75%, 100%, 150%). MON-021 stays off when v1 retires, and CHG-2291 goes back to staffing review. The binding month is May 2026. At 75%, the primary on-call would receive 40 pages against a triage capacity of 30: 26 from MON-021 v2 and 14 from MON-014, which pages on-call for the eight BAs outside v2's scope from go-live. The smallest rota change that lets a candidate ship is +10 triage pages in May 2026 (30 to 40), which would let 75% ship.

## Block 2: Supplementary answers

1. The memo opens with the decision: hold, no candidate ships. It names May 2026 as the binding month (75%: 40 on-call pages vs capacity 30).
2. 25%: busiest month is May 2026 at 240 on-call pages vs 30 capacity. Over capacity in 12 of 12 months. 0 EIA-imputed hours missed. Blocked by capacity in every month.
3. 50%: busiest month is May 2026 at 120 vs 30. Over capacity in 10 of 12 months, December 2025 to September 2026 (first breach Dec 2025: 25 vs a reduced capacity of 24). 0 imputed hours missed. Blocked by capacity.
4. 75%: busiest month is May 2026 at 40 vs 30. Over capacity in 1 month (May 2026 only). 0 imputed hours missed. Blocked by capacity in May 2026 only.
5. 100%: busiest month is May 2026 at 31 vs 30. Over capacity in 1 month (May 2026). 1 imputed hour missed: WACM, hour ending 2026-01-26 13:00 UTC, reported 7,463 MW vs a 3,733 MW forecast, deviation 99.92%. Blocked by both capacity and coverage.
6. 150%: busiest month is May 2026 at 26 vs 30. Over capacity in 0 months. 34 imputed hours missed (IID 24, WACM 8, NWMT 1, PSCO 1). Blocked by coverage.
7. The smallest rota capacity change that lets a candidate ship is +10 triage pages in May 2026 (30 to 40). The candidate that would then ship is 75%. No capacity change can rescue 100% or 150%, because they fail coverage. 50% would need extra capacity in 10 months.
8. May 2026 on-call pages at 75%, by BA (40 total):
   - MON-021 v2 (26): WALC 10, BANC 5, TIDC 4, IID 2, NEVP 2, AZPS 1, NWMT 1, PACE 1.
   - MON-014 (14): SPA 8, SEC 6.
9. The CSV has 60 rows: 5 candidates × 12 months (2025-10 to 2026-09). Each row gives the candidate threshold, the month, the pages reaching the primary on-call (v2 + MON-014), that month's rota capacity (30, except 24 in Dec 2025 and 26 in Jul and Aug 2026), a fits/doesn't-fit flag, and the EIA-imputed hours evaluated (91 across the year for every candidate) and missed that month.
   - Monthly on-call pages at 75%: Oct 16, Nov 9, Dec 15, Jan 17, Feb 25, Mar 27, Apr 26, May 40, Jun 19, Jul 17, Aug 12, Sep 18. Only May fails.
   - Missed imputed hours: 0 for 25%, 50% and 75%; 1 for 100% (Jan 2026); 34 for 150% (Nov 1, Dec 1, Jan 5, Feb 2, May 25).
10. The PNG chart shows monthly on-call pages for each of the five candidates against the rota capacity line. The capacity line steps down to 24 in December 2025 and 26 in July and August 2026. Months over capacity are clearly marked, and each candidate's blockers are visible. The title states the hold decision and May 2026 as the binding month (75%: 40 vs 30).

## Block 3: Critical numbers

8 BAs outside v2 scope (AVA, FPC, GVL, LGEE, PSEI, SEC, SPA, TEPC); v2 evaluates the other 47
MON-014 sends 54 on-call pages for those 8 BAs over the year, 14 of them in May 2026
75% in May 2026: 40 on-call pages (26 v2 + 14 MON-014) vs capacity 30, the only month over
100% misses 1 of 91 evaluated EIA-imputed hours (WACM, hour ending 2026-01-26 13:00 UTC, 99.92% deviation)
50% is over capacity in 10 of 12 months (first breach Dec 2025: 25 vs 24)

## Block 4: Path from raw data to recommendation

1. Stack the five EIA-930 BALANCE six-month files (Jul 2024 to Oct 2026) on BA and UTC end-of-hour time, keeping reported demand, the day-ahead forecast and imputed demand. Set the replay window to UTC dates 1 Oct 2025 to 30 Sep 2026, which drops the October 2026 rows from the live file. That gives 12 months matching the rota.
2. Apply v2's scope rule using EIA's About document. Exclude the 8 BAs whose forecast is not on the same physical basis as their demand (pseudo-ties and dynamic scheduling). Generation-only BAs report no demand. Result: 47 BAs evaluated.
3. Replay MON-021 v2 at each candidate. An hour is evaluated when demand is reported and the forecast is above 0. It alerts when |demand − forecast| / forecast exceeds the threshold. Group alerts into one page per BA per UTC date. Result: v2 pages per month, e.g. 75% peaks at 26 in May 2026.
4. Read the go-live paging set-up in the Sentinel export. At v1's retirement, MON-014 starts paging oncall-primary for the BAs outside v2's scope. Replay MON-014 for the 8 BAs: demand ≤ 0, or ≥ 1.5× the highest unflagged demand in the previous 365 days (the 2024–25 files supply the history), one page per BA per UTC date. Result: 54 pages, 14 in May 2026.
5. Add v2 and MON-014 pages per month and compare them with the rota's triage capacity, which covers all on-call pages (30; 24 in Dec, 26 in Jul and Aug). Result: months over capacity are 12, 10, 1, 1 and 0 for 25%, 50%, 75%, 100% and 150%.
6. Test coverage (AC3) on the 91 hours v2 evaluates where EIA imputed demand despite a reported value. Two FMPP imputed hours have no forecast, so they are outside AC3. Result: missed hours are 0, 0, 0, 1 and 34.
7. Apply AC4. No candidate passes both capacity and coverage, so the decision is hold. The binding month is May 2026: 75% has 40 vs 30.
8. Find the smallest capacity change among candidates that pass coverage. 75% needs +10 in May 2026 only; 25% and 50% need extra capacity across many months. Result: +10 in May lets 75% ship.
9. Break down May 2026 at 75% by BA and monitor. Result: 26 v2 pages (WALC 10 …) plus 14 MON-014 pages (SPA 8, SEC 6).
10. Validate the engine by replaying the v1 rule (20%, all BAs). It reproduces the attached v1 page history exactly (4,424 pages). Then write the memo, the 60-row CSV and the chart from the same results.
