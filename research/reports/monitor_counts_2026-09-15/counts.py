"""Conviction Monitor — counts only (no outcome or price column is read). Operational check for filing
hypotheses, 2026-09-15. Live read-only session; NON_QUOTABLE."""
import sys, os, json
sys.path[:0] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib")]
from desk_env import load; load()
import warnings; warnings.filterwarnings("ignore")
import psycopg, pandas as pd
from collections import Counter
pd.set_option("display.width", 220); pd.set_option("display.max_rows", 200)
conn = psycopg.connect(os.environ["RESEARCH_DB_URL"], options="-c default_transaction_read_only=on")
q = lambda s: pd.read_sql(s, conn)

print("=== rows, picks covered, date range")
print(q("""SELECT count(*) rows, count(distinct (symbol, original_pick_date)) picks, min(trading_date) d0, max(trading_date) d1,
 min(days_since_qualified) dsq_min, max(days_since_qualified) dsq_max FROM conviction_monitor_daily""").to_string(index=False))
print("\n=== overall_tier by days_since_qualified (rows), 2026-06-01 onward")
print(q("""SELECT days_since_qualified dsq, overall_tier, count(*) n FROM conviction_monitor_daily
 WHERE trading_date >= '2026-06-01' GROUP BY 1,2 ORDER BY 1,2""").pivot(index="dsq", columns="overall_tier", values="n").fillna(0).astype(int).to_string())
print("\n=== per pick: first EXIT day, ever-EXIT share, tier reversals (EXIT then back to WATCH/HOLD), since 2026-06-01")
per = q("""SELECT symbol, original_pick_date, days_since_qualified dsq, overall_tier FROM conviction_monitor_daily
 WHERE original_pick_date >= '2026-06-01' ORDER BY symbol, original_pick_date, days_since_qualified""")
g = per.groupby(["symbol", "original_pick_date"])
first_exit = g.apply(lambda d: d.loc[d.overall_tier == "EXIT", "dsq"].min())
n = len(first_exit)
print(f"picks tracked {n}; ever EXIT {first_exit.notna().sum()} ({first_exit.notna().mean():.1%})")
print("first EXIT day distribution:", first_exit.dropna().astype(int).value_counts().sort_index().to_dict())
rev = g.apply(lambda d: ((d.overall_tier.shift() == "EXIT") & (d.overall_tier != "EXIT")).any())
print(f"picks with EXIT followed later by a non-EXIT tier: {int(rev.sum())} ({rev.mean():.1%})")
lens = g.size()
print("rows per pick (tracking length):", lens.describe()[["min", "25%", "50%", "75%", "max"]].to_dict())
print("\n=== age_adjusted_severity vs overall_tier (rows since 06-01)")
print(q("""SELECT overall_tier, age_adjusted_severity, count(*) n FROM conviction_monitor_daily WHERE trading_date >= '2026-06-01'
 GROUP BY 1,2 ORDER BY 1,2""").to_string(index=False))
print("\n=== per-timeframe tiers on EXIT rows (which arm carries the EXIT)")
print(q("""SELECT technical_flip_30m_tier t30, technical_flip_1h_tier t1h, technical_flip_4h_tier t4h, technical_flip_1d_tier t1d, technical_flip_1wk_tier t1w, count(*) n
 FROM conviction_monitor_daily WHERE trading_date >= '2026-06-01' AND overall_tier='EXIT' GROUP BY 1,2,3,4,5 ORDER BY n DESC LIMIT 12""").to_string(index=False))
print("\n=== reason code frequency on EXIT rows vs non-EXIT rows (since 06-01)")
rc = q("""SELECT overall_tier, reason_codes_json FROM conviction_monitor_daily WHERE trading_date >= '2026-06-01'""")
cnt = {"EXIT": Counter(), "other": Counter()}
tot = {"EXIT": 0, "other": 0}
for _, r in rc.iterrows():
    k = "EXIT" if r.overall_tier == "EXIT" else "other"
    tot[k] += 1
    codes = r.reason_codes_json if isinstance(r.reason_codes_json, list) else json.loads(r.reason_codes_json or "[]")
    for c in set(codes):
        cnt[k][c] += 1
rows = []
for c in set(cnt["EXIT"]) | set(cnt["other"]):
    rows.append((c, cnt["EXIT"][c] / max(tot["EXIT"], 1), cnt["other"][c] / max(tot["other"], 1)))
df = pd.DataFrame(rows, columns=["code", "share_on_EXIT", "share_on_other"]).sort_values("share_on_EXIT", ascending=False)
df["lift"] = (df.share_on_EXIT / df.share_on_other.replace(0, float("nan"))).round(2)
print(f"EXIT rows {tot['EXIT']}, other rows {tot['other']}; distinct codes {len(df)}")
print(df.head(40).round(3).to_string(index=False))
print("\n=== the SAS card: does anything downstream read the monitor? (rows joined to published picks, since 06-01)")
print(q("""SELECT count(distinct (s.symbol, s.trading_date)) published, count(distinct (m.symbol, m.original_pick_date)) monitored
 FROM super_agent_select_candidates_daily s LEFT JOIN conviction_monitor_daily m ON m.symbol=s.symbol AND m.original_pick_date=s.trading_date
 WHERE s.selected_rank IS NOT NULL AND s.trading_date >= '2026-06-01'""").to_string(index=False))
