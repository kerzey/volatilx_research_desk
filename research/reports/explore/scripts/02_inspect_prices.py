"""EXPLORE_001 step 2: price table sanity — sessions, hourly stamps, split factors."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "research/lib")
import eval_utils as eu
P = "research/data/manifest_prices_v001.json"
dr = eu.load_table(P, "prices_daily_raw"); ds = eu.load_table(P, "prices_daily_split"); hr = eu.load_table(P, "prices_hourly_raw")
print(dr.head(3)); print(dr.dtypes); print(hr.head(3)); print(hr.dtypes)
dr["date"] = pd.to_datetime(dr["date"]); ds["date"] = pd.to_datetime(ds["date"])
print("daily date range", dr.date.min(), dr.date.max(), dr.symbol.nunique())
m = dr.merge(ds, on=["symbol","date"], suffixes=("_r","_s"))
m["f"] = m.c_r / m.c_s
spl = m.groupby("symbol").f.agg(["min","max"])
print(spl[(spl["max"]/spl["min"]) > 1.01])
# hourly
hr["t"] = pd.to_datetime(hr["t"], utc=True)
print("hourly range", hr.t.min(), hr.t.max())
print(hr.t.dt.hour.value_counts().sort_index())
# is daily open equal to regular session open (13:30 UTC)? compare with hourly 13:00 bar open for AAPL-like names
x = hr[hr.symbol == hr.symbol.iloc[0]].copy(); x["d"] = x.t.dt.tz_convert("America/New_York").dt.date
d0 = dr[dr.symbol == hr.symbol.iloc[0]].set_index(dr[dr.symbol == hr.symbol.iloc[0]].date.dt.date)
for d in list(x.d.unique())[40:44]:
    xx = x[x.d == d][["t","o","h","l","c","v"]]
    print(d, "daily:", d0.loc[d, ["o","h","l","c"]].to_dict() if d in d0.index else None)
    print(xx.to_string())
