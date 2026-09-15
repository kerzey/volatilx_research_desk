"""Read-only counts for the EN (buy/sell side) design: how big is the nightly UOA book, and how much
premium is already classified 'unknown' by the closing-quote proxy. Operational check, not a study result."""
import json
import os
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[3] / "research" / "lib")]
import desk_env  # noqa: E402

desk_env.load()
from sqlalchemy import create_engine, text  # noqa: E402

engine = create_engine(os.environ["RESEARCH_DB_URL"])
Q = {
    "per_day": """
        select trading_date, count(distinct underlying_symbol) syms, count(*) contracts,
               sum(trade_count) trades,
               round((sum(buy_premium)/nullif(sum(premium_total),0))::numeric,3) buy_share,
               round((sum(sell_premium)/nullif(sum(premium_total),0))::numeric,3) sell_share,
               round((sum(unknown_premium)/nullif(sum(premium_total),0))::numeric,3) unknown_share
        from uoa_contract_daily where trading_date >= '2026-09-01' group by 1 order by 1""",
    "unknown_by_month": """
        select date_trunc('month', trading_date)::date m,
               round((sum(unknown_premium)/nullif(sum(premium_total),0))::numeric,3) unknown_share,
               round((sum(buy_premium)/nullif(sum(buy_premium)+sum(sell_premium),0))::numeric,3) buy_of_classified
        from uoa_contract_daily where trading_date >= '2026-01-01' group by 1 order by 1""",
    "span_vs_spread": """
        -- contracts whose day's traded price range is wider than the closing spread: the closing quote
        -- cannot classify them consistently
        select count(*) n,
               sum(case when (ask - bid) > 0 and premium_max is not null then 1 else 0 end) with_spread
        from uoa_contract_daily where trading_date >= '2026-09-01' and trade_count > 0""",
    "latest_run": "select run_type, trading_date, status, stats_json from uoa_runs order by id desc limit 3",
}
with engine.connect() as c:
    for k, q in Q.items():
        print("==", k)
        for r in c.execute(text(q)):
            row = list(r)
            if k == "latest_run" and row[3]:
                try:
                    s = json.loads(row[3])
                    row[3] = {kk: s.get(kk) for kk in ("symbols_considered", "symbols_passing_gates", "contracts_selected", "contracts_with_trades", "trades_fetch")}
                except Exception:
                    pass
            print(row)
