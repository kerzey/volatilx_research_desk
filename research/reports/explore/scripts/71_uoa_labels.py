"""EXPLORE_001 step 71: UOA label vocabulary and score distribution (to define 'active' properly)."""
import sys
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
U = X.eu.load_split(X.M, "in_sample", name="uoa_symbol")
for c in ("label_day", "label_swing", "label_long"):
    print(c, U[c].value_counts(dropna=False).head(12).to_dict())
print(U[["score_day", "score_swing", "score_long"]].describe().round(1).to_string())
print("rows per date:", U.groupby("trading_date").size().describe().round(0).to_dict())
