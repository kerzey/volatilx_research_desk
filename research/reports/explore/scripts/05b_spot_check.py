"""EXPLORE_001 step 5b: find which session's close spot_close matches on 05-13/05-14; run timestamps."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
C = pd.read_parquet(X.WORK / "cands.parquet")
book = X.PathBook(X.load_prices())
runs = X.eu.load_split(X.M, "in_sample", name="sas_runs")
print(runs.columns.tolist())
cols = [c for c in runs.columns if any(k in c for k in ("date","start","finish","status","created"))]
print(runs[runs.trading_date.between("2026-05-11","2026-05-16")][cols].to_string())
for dd in ["2026-05-13", "2026-05-14"]:
    d = pd.Timestamp(dd); i = book.pos[d]
    sub = C[C.trading_date == d]
    for off in range(-3, 4):
        dx = book.cal[i + off]
        cl = np.array([book.by_sym[s].loc[dx, "c"] if dx in book.by_sym[s].index else np.nan for s in sub.symbol])
        print(dd, "offset", off, dx.date(), "matches(<0.1%)", int((np.abs(sub.spot.values / cl - 1) < 0.001).sum()), "of", len(sub))
# candidate created_at for those dates
cand = X.load_candidates()
print(cand[cand.trading_date.isin(pd.to_datetime(["2026-05-12","2026-05-13","2026-05-14","2026-05-15"]))].groupby("trading_date")[["created_at","updated_at"]].agg(["min","max"]).to_string())
