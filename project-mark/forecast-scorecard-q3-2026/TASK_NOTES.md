# Project Mark task: Q3 2026 forecast reliability scorecard

**Task type:** Data Quality Monitoring & Alerting · **Domain:** Energy Systems & Utilities
**Trap family:** reproduction gate. This is the platform's top-ranked trap family: "Reports a failed back-test, ships anyway" and "Stops at a close but inexact match".

## What to upload where

| Platform step | File |
|---|---|
| Prompt | `prompt.md` (paste the text) |
| Input files (ZIP) | `inputs.zip`: 41 MB, 13 files, 6 formats |
| File record / provenance | `provenance.md` |
| Golden deliverables | `golden/scorecard_q3_2026.csv`, `golden/scorecard_q3_2026_note.docx` |
| Submission blocks 1-4 | `submission_blocks.md` |

The scripts in `solution/` reproduce every golden number from the shipped files only.

## How it is built

- **Published controls.** 799 published figures: monthly and quarterly forecast error per Western BA, Q3 2024 to Q2 2026. They were computed from the real EIA-930 data by a method the folder never spells out.
- **The gate.** FCS-STD-2 section 5 only allows a compilation that reproduces every published figure exactly.
- **Five hidden rules.** Only all five together return 799 of 799, and none of the 799 figures sits on a rounding boundary:
  1. reporting-day months;
  2. leave out EIA-imputed hours;
  3. leave out forecast-flatline days;
  4. leave out 14-day bedding-in windows after active notices;
  5. leave out DST changeover days.
- **The decision depends on the hidden rules.** A model that stops short puts CISO on Watch instead of LDWP. A model that skips the imputed-hours rule sends the letter to WALC.

## Blind tests

Four independent runs on a strong model, with full code tools and unlimited time: two on the 3-rule version and two on this 5-rule version. All four reproduced every control and reached the golden answer, after 50 to 87 tool calls and 15 to 25 minutes each. The platform's own trap data says its model failed tasks built this way (averages of 0.13 to 0.21). Only a platform run shows which way it goes here.
