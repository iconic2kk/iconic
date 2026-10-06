I run grid data ops, and MON-021 v2 can't go live until we settle its threshold. Replay it over the last twelve complete months of the published EIA-930 hourly data in the folder and tell me which candidate threshold we ship under the acceptance criteria on CHG-2291, or, if none of them can ship, say so and say what blocks each one.

Put the call in a short decision memo, a DOCX, for the on-call leads. Open with the threshold and the month that runs closest to the rota's capacity at that setting. Then give every candidate its busiest month and page count, how many months it breaks capacity, and how many of the hours EIA later imputed it would have stayed silent on, and for the candidates on either side of the one you pick, show exactly what rules them out. Tell me which BAs v2 leaves on MON-014 and why, and how many of v1's pages over the same year came from them.

I also need the replay itself as a CSV for the ops dashboard: one row per candidate per month, with that month's pages, the rota capacity, whether it fits, and how many EIA-imputed hours the candidate evaluated and missed that month.

Last, chart it as a PNG: monthly pages for each candidate against the capacity line, with the shipped threshold marked and the threshold and its peak month in the title.
