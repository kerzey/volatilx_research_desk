"""Size the UOA trade-truncation defect (PI-020). Read-only counts; no outcome columns are read."""
import sys, os
sys.path[:0] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib")]
from desk_env import load; load()
import warnings; warnings.filterwarnings("ignore")
import psycopg, pandas as pd
pd.set_option("display.width", 200)
conn = psycopg.connect(os.environ["RESEARCH_DB_URL"], options="-c default_transaction_read_only=on")
q = lambda s: pd.read_sql(s, conn)

# A request returns at most 1,000 trades for up to 50 contracts. A symbol-day whose stored trade count reaches
# 1,000 hit the cap on at least one request: "capped". The exact batch split is not stored, so this is a floor.
base = """WITH c AS (SELECT trading_date, underlying_symbol sym, sum(trade_count) trades, count(*) n,
   sum(case when option_type='put' then premium_total else 0 end) put_prem
   FROM uoa_contract_daily GROUP BY 1,2)"""
print("=== by month: symbol-days, capped (stored trades >= 1000), capped with zero put premium")
print(q(base + """ SELECT to_char(trading_date,'YYYY-MM') m, count(*) symbol_days, sum(case when trades>=1000 then 1 else 0 end) capped,
 sum(case when trades>=1000 and put_prem=0 then 1 else 0 end) capped_zero_put, max(trades) max_trades
 FROM c GROUP BY 1 ORDER BY 1""").to_string(index=False))
print("\n=== published SAS picks since 2026-06-01 whose pick-night UOA row was capped")
print(q(base + """ SELECT count(*) picks, sum(case when c.trades>=1000 then 1 else 0 end) capped_flow,
 sum(case when c.trades>=1000 and c.put_prem=0 then 1 else 0 end) capped_zero_put, sum(case when c.sym is null then 1 else 0 end) no_uoa
 FROM super_agent_select_candidates_daily s LEFT JOIN c ON c.trading_date=s.trading_date AND c.sym=s.symbol
 WHERE s.selected_rank IS NOT NULL AND s.trading_date >= '2026-06-01'""").to_string(index=False))
print("\n=== most-affected symbols since 2026-06-01 (capped symbol-days)")
print(q(base + """ SELECT sym, count(*) days, sum(case when trades>=1000 then 1 else 0 end) capped FROM c WHERE trading_date >= '2026-06-01'
 GROUP BY sym HAVING sum(case when trades>=1000 then 1 else 0 end) > 0 ORDER BY capped DESC LIMIT 15""").to_string(index=False))
