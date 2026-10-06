I run grid data ops, and MON-021 v2 can't go live until we know what it does to the on-call. Replay the go-live paging set-up over the last twelve complete months of the published EIA-930 hourly data in the folder and tell me which candidate threshold we ship under CHG-2291. If none of them can ship, say so plainly, say what blocks each candidate, and tell me the smallest rota capacity change that would let one of them ship and which candidate that would be.

Put the call in a short decision memo, a DOCX, for the on-call leads. Open with the decision and the month that binds it. Then for every candidate give its busiest month with on-call pages against capacity, how many months it breaks capacity, and how many of the hours EIA later imputed it would have stayed silent on. For the binding month, break the on-call pages down by BA for the candidate that ships, or that a capacity change would let ship.

I also need the replay as a CSV for the ops dashboard: one row per candidate per month, with the pages that reach the primary on-call, that month's rota capacity, whether it fits, and how many EIA-imputed hours the candidate evaluated and missed that month.

Last, chart it as a PNG: monthly on-call pages for each candidate against the capacity line, with the decision and the binding month in the title.
