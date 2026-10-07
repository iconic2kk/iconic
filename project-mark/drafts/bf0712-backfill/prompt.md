I own the cleaned hourly demand series we republish from EIA-930, and backfill job BF-0712 is waiting on my sign-off. It would overwrite reported demand with the day-ahead forecast for every hour of the 38 incidents in the job file. Under DQ-STD-007, tell me whether we run it as submitted, run it with incidents removed, or reject it, and what that decision does to published demand.

Write it up as a short memo, a DOCX, for the data governance board. Lead with the call, the number of incidents and BA-hours we would backfill, and the net change to published demand in GWh next to what the job as submitted would have done. Then go through every incident: the verdict and the evidence in the data that settles it.

Give me the job back as a CSV the pipeline can run: one row per incident with the incident ID, BA, hours, the verdict, and the MWh change it applies.

And chart it as a PNG: for every incident, the MWh change the submitted job would apply against the change we actually apply, so the board can see the difference at a glance.
