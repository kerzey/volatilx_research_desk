"""EXPLORE_001 step 41: earnings-date fields — which are point-in-time, and do they agree?"""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
C = pd.read_parquet(X.WORK / "cands_ok.parquet")
C["ne_dt"] = pd.to_datetime(C.next_earnings_ctx, errors="coerce")
C["cal_days_ctx"] = (C["ne_dt"] - C.trading_date).dt.days
print("context days_to_earnings vs computed:", (C.days_to_earn_ctx - C.cal_days_ctx).abs().describe().round(2).to_dict())
for grp, sub in (("published", C[C.published]), ("unpublished", C[~C.published])):
    print(grp, "calendar days to next earnings (ctx):", sub.cal_days_ctx.describe(percentiles=[.05,.1,.25,.5]).round(1).to_dict())
    print(grp, "days_to_earnings_corrected:", sub.days_to_earnings_corrected.describe(percentiles=[.05,.1,.25,.5]).round(1).to_dict())
    print(grp, "earnings_phase:", sub.earnings_phase.value_counts(dropna=False).head(8).to_dict())
print("ctx vs corrected, |diff|>3 days share:", ((C.days_to_earn_ctx - C.days_to_earnings_corrected).abs() > 3).mean().round(3))
# does the gate exclude near-earnings candidates from publication?
C["near"] = C.cal_days_ctx.between(0, 14)
print("share with earnings in <=14 cal days: published", C[C.published].near.mean().round(3), " unpublished", C[~C.published].near.mean().round(3))
print(C.groupby(["near"]).qualification_reason.value_counts().unstack().to_string())
ex = X.load_excursion_v2()
print("excursion earnings_within_window share (published):", ex.earnings_within_window.mean().round(3))
