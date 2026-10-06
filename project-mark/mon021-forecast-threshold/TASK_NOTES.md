# Project Mark task: MON-021 v2 go-live

**Task type:** Data Quality Monitoring & Alerting · **Domain:** Energy Systems & Utilities
**Shape:** Setting one dial (lowest candidate threshold that clears a fixed bar), with a month-by-month capacity grid. The correct outcome is a **justified hold**.

## What to upload where

| Platform step | File |
|---|---|
| Prompt | `prompt.md` (paste the text) |
| Input files (ZIP) | `inputs.zip`: 12 files, 4 formats, five EIA tables of 139k-269k rows each |
| File record / provenance | `provenance.md` / `provenance.csv` |
| Golden deliverables | `golden/MON-021_v2_go-live_decision_memo.docx`, `golden/MON-021_v2_go-live_replay_by_month.csv`, `golden/MON-021_v2_go-live_replay.png` |

`solution/` holds the scripts that produce every golden number from the shipped files only. Running `compute.py` against a fresh unzip of `inputs.zip` reproduces the golden CSV byte for byte.

## The answer

**Hold. No candidate threshold can ship.** The binding month is **May 2026**. At 75%, the primary on-call gets **40 pages against a capacity of 30**: 26 from MON-021 v2 and 14 from MON-014, which starts paging on-call for the 8 out-of-scope BAs when v1 retires. Adding **+10 triage pages in May 2026** would let 75% ship.

| Threshold | Busiest month: on-call / capacity (v2 + MON-014) | Months over | Imputed hours missed (of 91) | Blocked by |
|---|---|---|---|---|
| 25% | May 2026: 240 / 30 (226 + 14) | 12 | 0 | capacity |
| 50% | May 2026: 120 / 30 (106 + 14) | 10 (Dec 2025-Sep 2026; Dec is 25 vs 24) | 0 | capacity |
| 75% | May 2026: 40 / 30 (26 + 14) | 1 (May 2026) | 0 | capacity in May only |
| 100% | May 2026: 31 / 30 (17 + 14) | 1 | 1 (WACM, hour ending 2026-01-26 13:00 UTC, 99.92%) | capacity and coverage |
| 150% | May 2026: 26 / 30 (12 + 14) | 0 | 34 (IID 24, WACM 8, NWMT 1, PSCO 1) | coverage |

- **May 2026 by BA at 75%.** v2: WALC 10, BANC 5, TIDC 4, IID 2, NEVP 2, AZPS 1, NWMT 1, PACE 1. MON-014: SPA 8, SEC 6.
- **MON-014 for the year: 54 on-call pages.** SEC 34, SPA 17, LGEE 2, AVA 1.

## Where the difficulty comes from (all honest data)

1. **Forecast comparability (scope).** v2's scope covers only BAs whose forecast is prepared "on the same physical basis" as their reported demand. The only place that names the 8 that fail this (AVA, FPC, GVL, LGEE, PSEI, SEC, SPA, TEPC) is the middle of the 13-page EIA About PDF.
2. **Shared capacity (the binding constraint).** The trap is spread across three files:
   - CHG-2291 AC1 asks for the paging set-up that takes effect *at go-live*.
   - The Sentinel export's `scheduled_changes` routes MON-014 to on-call for out-of-scope BAs.
   - The rota's title row says capacity covers every monitor.

   A model that checks v2's pages alone answers **"ship 75%"**, which is wrong. A ticket comment repeats that tempting figure; it is correct about v2 alone and incomplete as a decision.
3. **MON-014 replay.** It needs the 365-day look-back (two extra EIA files, including the 2024 schema) and the accepted-only ceiling. Letting flagged spikes into the history drops 2 pages, in Feb and Mar 2026.
4. **Smaller traps.**
   - Rota capacity is uneven (24 in Dec, 26 in Jul and Aug).
   - The live file includes October 2026 rows, which fall outside the window.
   - Two FMPP imputed hours have no forecast, so they are outside AC3.
   - The replay must use reported demand, not adjusted.
   - Generation-only BAs report no demand or forecast.
   - The roster changes in April 2026 (WACM and WAUW retire, SWPW appears).
5. **Wrong path that still says hold.** A model that misses the scope carve-out also says "hold", but for the wrong reason: every candidate up to 100% breaks capacity in most months. It gets the decision line right and almost every number wrong.

## Blind-test history

- **v1 of this task** (no shared capacity, heavy hints): a fresh agent with only the prompt and ZIP matched the golden exactly (about 90-100%). It was too easy, so the task was hardened.
- **v2 (this version):** see below.
