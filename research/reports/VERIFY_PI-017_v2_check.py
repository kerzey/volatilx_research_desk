# PI-017 brief section 8, check V2: per-date counts in uoa_symbol_daily vs the frozen v001 parquet.
# Counts only. Read-only session. Never prints the connection string.
# Run from the desk root: python research/reports/VERIFY_PI-017_v2_check.py
import sys, os
sys.path.insert(0, "research/lib")
import desk_env; desk_env.load()
import psycopg, pandas as pd

url = os.environ["RESEARCH_DB_URL"]
sql = """SELECT trading_date, count(*) AS n_rows, count(DISTINCT symbol) AS n_symbols
FROM uoa_symbol_daily
WHERE trading_date BETWEEN '2026-01-07' AND '2026-09-10'
GROUP BY trading_date ORDER BY trading_date"""
with psycopg.connect(url, options="-c default_transaction_read_only=on") as conn:
    live = pd.read_sql(sql, conn)
live["trading_date"] = pd.to_datetime(live["trading_date"]).dt.date

pq = pd.read_parquet("research/data/v001_uoa_symbol.parquet", columns=["trading_date", "symbol"])
pq["trading_date"] = pd.to_datetime(pq["trading_date"]).dt.date
frz = pq.groupby("trading_date").agg(n_rows=("symbol", "size"), n_symbols=("symbol", "nunique")).reset_index()
lo, hi = pd.Timestamp("2026-01-07").date(), pd.Timestamp("2026-09-10").date()
frz = frz[(frz.trading_date >= lo) & (frz.trading_date <= hi)]

m = frz.merge(live, on="trading_date", how="outer", suffixes=("_freeze", "_live"), indicator=True)
diff = m[(m._merge != "both") | (m.n_rows_freeze != m.n_rows_live) | (m.n_symbols_freeze != m.n_symbols_live)]
print(f"freeze dates: {len(frz)}  live dates: {len(live)}  freeze rows: {int(frz.n_rows.sum())}  live rows: {int(live.n_rows.sum())}")
print(f"dates differing or missing on one side: {len(diff)}")
if len(diff):
    print(diff.to_string(index=False))
print("V2:", "PASS -- live matches freeze row-for-row on every date" if len(diff) == 0 else "FAIL -- see differences above")
