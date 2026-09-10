---
name: daily-check
description: Morning operational check of last night's VolatilX pipeline output against trailing baselines. Run by the data-steward after the 16:05 ET nightly completes.
---
Run the daily operational check for the most recent trading date. Use only $RESEARCH_DB_URL via `python research/lib/db.py "<SELECT ...>"` (no psql needed).

For each item compute today's value and the trailing 20-trading-day median and MAD; flag RED
if |today − median| > 2 MAD, else OK. Output one line per item, RED lines first, then a
final line `ALL CLEAR` if nothing is RED.

1. Stage freshness: max(trading_date) in super_agent_select_runs, projection_pick_bullish_daily,
   uoa_symbol_daily, gex_symbol_daily, market_regime_daily equals the last trading date.
2. Row counts per table above.
3. SAS: number of candidates, number qualified (≥70 & completeness ≥35), number published.
4. Layer null rates in the SAS audit table: projection, technical, flow, catalyst,
   fundamental, smart_money, gex. (A GEX-null spike triggers the +5 offset — call it out.)
5. Source-membership mix of published picks (projection / uoa / whale / multi).
6. Score distribution: median, share ≥90, share with completeness <60.
7. Direction mix (bull/bear) and timeframe mix (short/swing/long).
8. Published-vs-audit consistency: every published symbol exists in the audit table with
   the same score and direction.
9. Outcome maturation: count of picks whose W60 window closed yesterday that still lack
   outcome columns (should be 0).
10. Any row in outcome_correction_ledger dated today.

Write the report to research/reports/daily/<date>.md. Do not interpret; do not suggest fixes
beyond naming the table and column.
