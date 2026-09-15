"""When does the UOA nightly start, and does it see trades up to 16:00 ET? (Alpaca Basic plan withholds the
latest 15 minutes of historical data.) Read-only operational check."""
import os
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[3] / "research" / "lib")]
import desk_env  # noqa: E402

desk_env.load()
from sqlalchemy import create_engine, text  # noqa: E402

engine = create_engine(os.environ["RESEARCH_DB_URL"])
Q = {
    "nightly_start_et": """
        select trading_date, run_type, (started_at at time zone 'America/New_York')::time start_et,
               (finished_at at time zone 'America/New_York')::time end_et, status
        from uoa_runs where run_type = 'nightly' and trading_date >= '2026-09-01' order by trading_date""",
    "last_print_seen_et": """
        select trading_date, (max(last_trade_ts) at time zone 'America/New_York')::time last_print_et,
               sum(case when last_trade_ts at time zone 'America/New_York' > (trading_date + time '15:50') then 1 else 0 end) contracts_after_1550
        from uoa_contract_daily where trading_date >= '2026-09-01' and trade_count > 0 group by 1 order by 1""",
    "prints_after_1545_share": """
        -- top_trades_json holds the 10 largest prints per contract; use their timestamps as a sample
        select trading_date, count(*) sampled_prints,
               sum(case when (p->>'t')::timestamptz at time zone 'America/New_York' > (trading_date + time '15:45') then 1 else 0 end) after_1545
        from uoa_contract_daily c, jsonb_array_elements(c.top_trades_json::jsonb) p
        where trading_date >= '2026-09-08' and trade_count > 0 group by 1 order by 1""",
}
with engine.connect() as c:
    for k, q in Q.items():
        print("==", k)
        try:
            for r in c.execute(text(q)):
                print(list(r))
        except Exception as e:  # noqa: BLE001
            print("query failed:", str(e).splitlines()[0])
