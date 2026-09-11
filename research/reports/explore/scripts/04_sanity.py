"""EXPLORE_001 step 4: sanity checks on spot_close, atr_pct, lane plans."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 40)
C = pd.read_parquet(X.WORK / "cands.parquet")
bad = C[C.spot_vs_close.abs() > 0.005]
print("spot mismatch by date:\n", bad.groupby("trading_date").size().sort_values(ascending=False).head(15))
print(bad[["trading_date","symbol","spot","raw_close_d","spot_vs_close","published"]].sort_values("spot_vs_close").head(12).to_string())
print(bad[["trading_date","symbol","spot","raw_close_d","spot_vs_close","published"]].sort_values("spot_vs_close").tail(8).to_string())
print("published mismatches:", bad.published.sum())
# ATR
C["atr_ratio"] = C.atr_pct / C.atr14_px_pct
print(C.atr_ratio.describe(percentiles=[.01,.05,.25,.5,.75,.95,.99]))
w = C[(C.atr_ratio > 1.5) | (C.atr_ratio < 0.67)]
print("atr ratio outliers", len(w)); print(w[["trading_date","symbol","atr_pct","atr14_px_pct","spot","raw_close_d"]].head(15).to_string())
print(C[["atr_pct","atr14_px_pct"]].corr(method="spearman"))
# lane plans for published
P = C[C.published]
print("published has_lane_plans:", P.has_lane_plans.value_counts().to_dict())
print("ladder coverage:", {l: P[l].notna().sum() for l in X.LADDER})
print("counter coverage:", {k: P[k].notna().sum() for k in X.COUNTER_KEYS})
print(P[~P.has_lane_plans][["trading_date","symbol","overall_score","downside_source"]].to_string())
# excursion entry_ref vs spot
print("ex_entry_ref vs spot |diff|>0.1%:", ((P.ex_entry_ref / P.spot - 1).abs() > 0.001).sum())
