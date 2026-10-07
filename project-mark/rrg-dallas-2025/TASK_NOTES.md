# Project Mark task: RRG extension decision (rework of the returned Census task)

**Task type:** Experiment & Causal Analysis · **Domain:** Urban & Regional Science

## What changed from the returned task (reviewer's fixes)

- The deciding step is no longer a vintage choice: every year comes from Vintage 2025, as the agreement says.
- No office-habit line or other stakeholder bait.
- The answer is computed from a different measure: natural change plus domestic migration per 1,000 residents at the start of each estimate year, with international migration and the residual left out (reviewer option 1). The age-sex file and the 25 to 44 growth are not part of it.
- Hardening applied: the margin to the bar is 0.086 (under 0.5); the pre-period check is part of the rule with its own 0.096 margin; the components are asked for in rate points on the start-of-year base; the governing basis sits in the agreement's Annex A, not in the press release.

## The trap

Census's published rate columns (and its layout's stated rule) divide by the average of the opening and closing July
populations. On that basis the effect is 1.787 and the program lapses. Only the start-of-year base reproduces the board's own
worked figures in Annex A (-6.2, +13.2, 19.5), and on it the effect is 1.886 and the program is extended. Other wrong turns
(total growth, total less international, averaged county rates) also lead to a lapse.

## Blind tests (strong model, full code tools, prompt and inputs only)

| Run | Version | Result |
|---|---|---|
| A | v1 (Annex A to two decimals) | Missed: lapse at 1.787 (Census mid-year base; called Annex A "an illustration, not a rule") |
| B | v1 | Solved: extend at 1.886 |
| C | v2 (Annex A to one decimal, term dates fixed) | Missed: lapse at 1.787 (same reasoning) |
| D | v2 | Solved: extend at 1.886 |

Two of four strong runs missed. If each platform response misses about half the time, both miss roughly one time in four, so
run the platform evaluation before submitting.

## Rebuilding

Unzip `inputs.zip` into `inputs/` beside `solution/`, then run `python3 solution/rrg.py` (numbers) and
`python3 solution/make_golden.py` (workbook, note, chart; needs LibreOffice for the formula recalculation).
