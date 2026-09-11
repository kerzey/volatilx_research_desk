"""EXPLORE_001 step 6: audit SAS run finish time vs pick night (knowledge-time hazard)."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
runs = X.eu.load_split(X.M, "in_sample", name="sas_runs")
cand = X.load_candidates()
runs["finished_at"] = pd.to_datetime(runs.finished_at, utc=True)
runs["started_at"] = pd.to_datetime(runs.started_at, utc=True)
runs["night_end_utc"] = runs.trading_date.dt.tz_localize("UTC") + pd.Timedelta(hours=23, minutes=59)
runs["late_hours"] = (runs.finished_at - (runs.trading_date.dt.tz_localize("UTC") + pd.Timedelta(hours=21))).dt.total_seconds() / 3600
cc = cand.groupby("trading_date").created_at.min().rename("cand_created_min")
runs = runs.merge(cc, left_on="trading_date", right_index=True, how="left")
out = runs[["trading_date", "started_at", "finished_at", "late_hours", "cand_created_min"]].sort_values("trading_date")
print(out.to_string())
late = out[out.late_hours > 3]
print("\nruns finishing >3h after 21:00 UTC on pick night:", len(late), "of", len(out))
print(late.trading_date.dt.date.tolist())
pd.Series(late.trading_date.dt.date.astype(str).tolist()).to_csv(X.WORK / "late_nights.csv", index=False, header=["trading_date"])
