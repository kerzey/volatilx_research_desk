"""SNDK case study — inspect the pickles written by pull_db.py (scratchpad) plus a few extra read-only rows."""
import sys, os, json
sys.path[:0] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib")]
from desk_env import load; load()
import warnings; warnings.filterwarnings("ignore")
import psycopg, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 80); pd.set_option("display.max_colwidth", 200)
OUT = os.environ["CASE_OUT"]


def js(x):
    if isinstance(x, (dict, list)):
        return x
    try:
        return json.loads(x)
    except Exception:
        return x


cand = pd.read_pickle(os.path.join(OUT, "cand.pkl"))
for _, r in cand.iterrows():
    d = str(r.trading_date)
    if d < "2026-09-08":
        continue
    ctx, sd, pp = js(r.context_json) or {}, js(r.score_details_json) or {}, js(r.public_payload_json)
    print(f"\n################ {d}")
    print("major_risk:", r.major_risk)
    print("thesis:", r.thesis_summary)
    for k in ("catalyst_context", "projection_context", "options_flow_context", "gex_context", "technical_snapshot", "fundamentals_context", "smart_money_context", "missing_data_flags"):
        v = ctx.get(k)
        s = json.dumps(v)[:1400] if v is not None else None
        print(f"  ctx.{k}: {s}")
    print("  score_details keys:", list(sd.keys())[:40])
    for k in ("conflict_penalty", "conflicts", "conflict_reasons", "reasons", "direction_evidence", "timeframe_evidence", "cross_layer_bonus", "atr_projection_meta", "earnings_phase", "days_to_earnings"):
        if k in sd:
            print(f"  sd.{k}: {json.dumps(sd[k])[:900]}")
    if isinstance(pp, dict) and pp:
        print("  pp.risk_flags:", pp.get("risk_flags"))
        print("  pp.execution_private:", json.dumps(pp.get("execution_private"))[:500])
        print("  pp.options_context:", json.dumps(pp.get("options_context"))[:400])
        print("  pp.lane_plans:", json.dumps(pp.get("lane_plans"))[:1500])

uoa = pd.read_pickle(os.path.join(OUT, "uoa.pkl"))
for _, r in uoa.iterrows():
    if str(r.trading_date) >= "2026-09-03":
        print(f"\nUOA why {r.trading_date}: {json.dumps(js(r.why_json))[:2500]}")
gex = pd.read_pickle(os.path.join(OUT, "gex.pkl"))
for _, r in gex.iterrows():
    print(f"GEX walls {r.trading_date} spot {r.spot_close}: {json.dumps(js(r.top_walls_json))[:700]}")

conn = psycopg.connect(os.environ["RESEARCH_DB_URL"], options="-c default_transaction_read_only=on")
q = lambda s: pd.read_sql(s, conn)
print("\n=== SNDK excursion, all published picks")
print(q("""SELECT trading_date, selected_rank rk, round(overall_score::numeric,1) s, entry_ref, mae_natural_pct, dipped_before_l1, upside_levels_json, window_sealed
 FROM sas_selection_excursion WHERE symbol='SNDK' ORDER BY trading_date""").to_string(index=False))
print("\n=== uoa_symbol_daily: how often put premium is exactly 0 (last 30 sessions), SNDK vs all symbols")
print(q("""SELECT (symbol='SNDK') is_sndk, count(*) n, sum(case when put_premium_total=0 then 1 else 0 end) zero_put,
 sum(case when call_premium_total=0 then 1 else 0 end) zero_call FROM uoa_symbol_daily WHERE trading_date >= '2026-08-01' GROUP BY 1""").to_string(index=False))
print(q("""SELECT symbol, count(*) n, sum(case when put_premium_total=0 then 1 else 0 end) zero_put, round(avg(total_premium)::numeric,0) avg_prem
 FROM uoa_symbol_daily WHERE trading_date >= '2026-08-01' AND symbol IN ('SNDK','MU','WDC','STX','NVDA','AMD','TSLA','COIN','META','AAPL')
 GROUP BY symbol ORDER BY symbol""").to_string(index=False))
