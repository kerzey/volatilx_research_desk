"""SNDK case study, 2026-09-15 — read-only operational pull (not a study result; rule 4 applies to
studies). Session opened read-only. Raw pickles stay in the scratchpad directory, never committed."""
import sys, os
sys.path[:0] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib")]
from desk_env import load; load()
import psycopg, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 80); pd.set_option("display.max_colwidth", 70)
OUT = os.environ.get("CASE_OUT") or os.path.dirname(os.path.abspath(__file__))
SYM = "SNDK"
conn = psycopg.connect(os.environ["RESEARCH_DB_URL"], options="-c default_transaction_read_only=on")


def q(sql):
    return pd.read_sql(sql, conn)


def show(title, fn):
    print("\n=== " + title)
    try:
        df = fn()
        print(df.to_string(index=False))
        return df
    except Exception as e:  # keep going on a bad column name
        print("ERR", e)
        conn.rollback()


show("SNDK candidates", lambda: q(f"""SELECT trading_date, round(overall_score::numeric,1) s, dominant_direction d, best_timeframe tf, confidence_level conf,
 qualified, selected_rank rk, qualification_reason reason, round(flow_strength_score::numeric,0) f, round(technical_structure_score::numeric,0) t,
 round(gex_alignment_score::numeric,0) g, round(projection_score::numeric,0) p, round(fundamental_quality_score::numeric,0) fu,
 round(catalyst_event_score::numeric,0) ca, cross_layer_bonus xb, conflict_penalty cp, synthesis_status
 FROM super_agent_select_candidates_daily WHERE symbol='{SYM}' AND trading_date >= '2026-08-17' ORDER BY trading_date"""))
full = show("SNDK payload row count", lambda: q(f"""SELECT trading_date, public_payload_json, context_json, score_details_json, major_risk, thesis_summary
 FROM super_agent_select_candidates_daily WHERE symbol='{SYM}' AND trading_date >= '2026-08-24' ORDER BY trading_date""").assign(n=1)[["trading_date", "n"]])
q(f"""SELECT trading_date, public_payload_json, context_json, score_details_json, major_risk, thesis_summary
 FROM super_agent_select_candidates_daily WHERE symbol='{SYM}' AND trading_date >= '2026-08-24' ORDER BY trading_date""").to_pickle(os.path.join(OUT, "cand.pkl"))
show("published picks since 09-02", lambda: q("""SELECT trading_date, symbol, selected_rank rk, round(overall_score::numeric,1) s, dominant_direction d, best_timeframe tf
 FROM super_agent_select_candidates_daily WHERE trading_date >= '2026-09-02' AND selected_rank IS NOT NULL ORDER BY trading_date, selected_rank"""))
u = q(f"""SELECT * FROM uoa_symbol_daily WHERE symbol='{SYM}' AND trading_date >= '2026-08-24' ORDER BY trading_date""")
u.to_pickle(os.path.join(OUT, "uoa.pkl"))
print("\n=== SNDK UOA")
print(u[["trading_date", "spot_close", "call_premium_total", "put_premium_total", "call_buy_premium", "put_buy_premium",
         "net_directional_premium", "dir_ratio", "score_day", "bias_day", "score_swing", "bias_swing", "score_long", "bias_long", "oi_confirm_ratio"]].to_string(index=False))
g = q(f"SELECT * FROM gex_symbol_daily WHERE underlying='{SYM}' AND trading_date >= '2026-08-31' ORDER BY trading_date")
g.to_pickle(os.path.join(OUT, "gex.pkl"))
print("\n=== SNDK GEX")
print(g[["trading_date", "spot_close", "net_gex", "regime", "gamma_flip", "pin_risk"]].to_string(index=False))
show("regime", lambda: q("""SELECT trading_date, market_regime, score_band, regime_phase, regime_confidence FROM market_regime_daily
 WHERE trading_date >= '2026-08-31' ORDER BY trading_date"""))
show("conviction monitor", lambda: q(f"""SELECT trading_date, original_pick_date, days_since_qualified dsq, original_score, polarity_today, polarity_tier,
 technical_overall_tier, overall_tier, age_adjusted_severity sev, reason_codes_json FROM conviction_monitor_daily
 WHERE symbol='{SYM}' AND trading_date >= '2026-09-01' ORDER BY trading_date, original_pick_date"""))
show("excursion", lambda: q(f"""SELECT trading_date, selected_rank rk, overall_score, direction, timeframe, entry_ref, signal_date_close, mae_natural_pct,
 dipped_before_l1, upside_levels_json, counter_levels_json, window_sealed FROM sas_selection_excursion
 WHERE symbol='{SYM}' AND trading_date >= '2026-08-01' ORDER BY trading_date"""))
show("SNDK prior SAS history (all time, published)", lambda: q(f"""SELECT trading_date, selected_rank rk, round(overall_score::numeric,1) s, dominant_direction d, best_timeframe tf
 FROM super_agent_select_candidates_daily WHERE symbol='{SYM}' AND selected_rank IS NOT NULL ORDER BY trading_date"""))
