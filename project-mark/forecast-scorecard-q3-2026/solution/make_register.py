"""Write the desk's forecast-change notice register (scenario data)."""
import os
import pandas as pd
from scorecard import INPUTS

N = [  # ba, received (UTC), effective (BA reporting day), description, status
 ("PACW", "2024-08-01 16:12", "2024-08-06", "Day-ahead load forecast moved from vendor service to in-house model", "active"),
 ("BANC", "2024-10-09 14:40", "2024-10-15", "Forecast model retrained on 2019-2024 load history", "active"),
 ("IPCO", "2024-11-26 20:05", "2024-12-03", "Weather inputs switched to new station set", "active"),
 ("AZPS", "2025-01-08 17:31", "2025-01-14", "Behind-the-meter solar adjustment added to day-ahead forecast", "active"),
 ("PSCO", "2025-02-25 15:22", "2025-03-04", "New day-ahead forecasting vendor", "active"),
 ("GCPD", "2025-03-31 18:47", "2025-04-08", "Forecast model upgrade", "withdrawn by BA 2025-04-02"),
 ("SRP", "2025-05-14 13:09", "2025-05-20", "Forecast model retrained ahead of summer", "active"),
 ("NWMT", "2025-06-17 21:56", "2025-06-24", "Day-ahead forecast now produced hourly rather than in blocks", "active"),
 ("BPAT", "2025-08-05 16:30", "2025-08-12", "Load forecast system replacement", "active"),
 ("PACE", "2025-09-02 19:14", "2025-09-09", "Forecast vendor contract change", "withdrawn by BA 2025-09-05"),
 ("TIDC", "2025-09-30 15:48", "2025-10-07", "Forecast model retrained", "active"),
 ("PGE", "2025-11-11 17:02", "2025-11-18", "Electric vehicle load added to day-ahead forecast", "active"),
 ("EPE", "2026-01-06 14:26", "2026-01-13", "Forecast model upgrade", "active"),
 ("SWPW", "2026-04-14 18:55", "2026-04-21", "Forecast process moved to SPP RTO West market timeline", "active"),
 ("CISO", "2026-04-28 16:17", "2026-05-05", "Day-ahead forecast now includes demand-response dispatch", "active"),
 ("CISO", "2026-08-04 20:41", "2026-08-12", "Forecast model retrained", "withdrawn by BA 2026-08-10"),
 ("LDWP", "2026-09-04 15:33", "2026-09-12", "New load forecasting model in production", "active"),
]
r = pd.DataFrame(N, columns=["ba", "received_utc", "effective_reporting_day", "change_notified", "status"])
r.insert(0, "notice_id", [f"FCN-{i:03d}" for i in range(101, 101 + len(r))])
r["desk_action"] = r.status.map(lambda s: "noted; bedding-in applies to scorecard" if s == "active" else "closed; no bedding-in")
path = os.path.join(INPUTS, "forecast_change_notices.csv")
with open(path, "w", newline="") as fh:
    fh.write("grid-data-ops forecast change notice register | notices BAs sent to the desk about changes to their day-ahead forecasting | "
             "exported 2026-10-05 | scenario data authored for this exercise\n")
    r.to_csv(fh, index=False)
print(r.to_string(index=False))
