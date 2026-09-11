"""EXPLORE_001 step 5: what price is spot_close on 2026-05-13/14? Compare with d-1 close and intraday hourly."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
C = pd.read_parquet(X.WORK / "cands.parquet")
prices = X.load_prices()
book = X.PathBook(prices)
runs = X.eu.load_split(X.M, "in_sample", name="sas_runs")
print(runs[runs.trading_date.isin(pd.to_datetime(["2026-05-12","2026-05-13","2026-05-14","2026-05-15"]))].T.to_string()[:3000])
H = X.load_hourly()
for dd in ["2026-05-13", "2026-05-14"]:
    d = pd.Timestamp(dd); prev = book.cal[book.pos[d]-1]
    sub = C[C.trading_date == d].copy()
    sub["prev_close"] = [book.by_sym[s].loc[prev, "c"] if s in book.by_sym else np.nan for s in sub.symbol]
    sub["vs_prev"] = sub.spot / sub.prev_close - 1
    print(dd, "n", len(sub), "|spot-close|<0.1%:", (sub.spot_vs_close.abs() < 0.001).sum(),
          " |spot-prevclose|<0.1%:", (sub.vs_prev.abs() < 0.001).sum())
    # match against hourly closes of the day
    hh = H[(H.d == d)]
    best = []
    for r in sub.itertuples():
        x = hh[hh.symbol == r.symbol]
        if len(x) == 0: continue
        dif = (x.c / r.spot - 1).abs()
        best.append((r.symbol, int(x.hr.iloc[dif.argmin()]), float(dif.min())))
    b = pd.DataFrame(best, columns=["sym","hr","dif"])
    print(" best-matching hourly bar (UTC hour) for spot:", b[b.dif < 0.002].hr.value_counts().to_dict())
