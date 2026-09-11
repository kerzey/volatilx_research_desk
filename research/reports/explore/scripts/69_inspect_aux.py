"""EXPLORE_001 step 69: inspect auxiliary in-sample tables (uoa_symbol, conviction_monitor, gex_symbol)."""
import sys
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
for name in ("uoa_symbol", "conviction_monitor", "gex_symbol"):
    df = X.eu.load_split(X.M, "in_sample", name=name)
    print(f"\n=== {name}: {df.shape}, {df.trading_date.min().date()}..{df.trading_date.max().date()}")
    print(df.columns.tolist())
    print(df.head(2).T.to_string()[:2500])
C = pd.read_parquet(X.WORK / "cands_ok.parquet")
print("\nindustry coverage published:", C[C.published].industry.notna().mean().round(3), C[C.published].industry.value_counts().head(8).to_dict())
