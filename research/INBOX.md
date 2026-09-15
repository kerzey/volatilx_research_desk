# Inbox — Haci's ideas, in plain words

Write one idea per line, starting with `- [ ] `. No format beyond that: "I think picks that gap
up and close red on day 1 are dead money" is enough. On the next `/desk-run` (or overnight) the desk
turns each line into a backlog hypothesis with an id, a family, a baseline and a mechanism line,
ticks the box here with the H-number, and registers it ahead of everything else (DP-47). If the
idea is a question about the platform rather than an edge ("why did X happen on date Y"), the desk
files it as a platform issue or answers it in `research/reports/` and says which.

Ideas here jump the queue; nothing else does. To research something *right now* instead of
waiting for the cycle: `/desk-run idea "…"`.

_(nothing waiting — add a `- [ ] ` line below)_

- [x] Does SAS actually have an edge? H0: SAS ranking contains no predictive information beyond simple benchmarks. Compare SAS Top 10 not only against random stocks but against embarrassingly simple alternatives — SPY / equal-weight S&P 500 / sector-adjusted random / 20-day momentum / 60-day momentum / analyst revisions / simple technical rank — on forward 1d / 3d / 7d / 14d / 30d returns after risk adjustment. → H-067 (F1), 2026-09-13
- [x] Master Hypothesis Program (H0, H0B, H1–H14; Haci's own Claude + ChatGPT analysis, pasted in session) → H-069..H-084 — H-071 / H-072 merged into Q024 / H-068, H-075 in F1, H-073 / H-079 / H-080 / H-082 in F2, H-078 in F6 (founder arm: new data needed), the rest in the new F8; DP-51 added for H0B; verbatim text and mapping in `research/reports/INBOX_2026-09-14_master_hypothesis_program.md`, 2026-09-14
- [x] Near-miss at the line that actually decides publication now: candidates scoring 75–80 vs 80–85 around the 80.0 publication floor (services/super_agent_select_models.py:91). The old 70 line (H-002) has decided nothing since 2026-07-08, so H-002 merged into Q027; this is its live-line successor. Source: registrar triage of H-002, desk run 2026-09-14. → H-085 (F1)
- [x] Multi-agent technical analysis reports in blob storage (stocks and crypto): do the per-timeframe setups work — entry, stop and targets for day, swing and long trades? Does price move the way the technical findings and action items say? Example: all timeframes bullish, price action uptrend on every timeframe except daily — does it reach the target, and when? Any strong correlation between OBV, volume, Supertrend, Kalman, price action and the move? Does timeframe disagreement (15m/30m/1h/4h bullish, 1d bearish) mean up first then down — day and swing targets hit, long target or entry not? Sample report: ai_job 7e78c055, SNDK, 2026-09-11 10:01:49. → new family F9, H-086..H-090; PI-018 filed from reading the decision code; Data Steward blob inventory is the first step. 2026-09-14
- [x] SAS and multi-agent report usefulness (Haci, 2026-09-14, after sharing docs/sample_sas_report.json and docs/sample_multi_ai_report.json): do the SAS report's risk warnings, its flow label vs premium mix, and its embedded technical consensus predict the pick's path; and does the multi-agent report's own trading plan (trigger, entry, stop, targets) work as a trader reads it → H-091 (F3), H-092 (F5), H-093 (F5), H-094 (F9)
- [x] SNDK was picked 2–3 times last week at 92–93 with big bullish call flow expiring Friday and still fell; why, and will it do better this week (Haci, 2026-09-15) → answered in research/reports/case_SNDK_2026-09-15/REPORT.md; PI-020 filed (UOA trade truncation); H-095 (F1), H-096 (F2)
- [x] Is the Conviction Monitor working? I ignore it in my trading. Is the overall evaluation correct, which data has significant impact, and if it is useless we can remove it from the platform (Haci, 2026-09-15) → census research/reports/monitor_counts_2026-09-15/REPORT.md; Q019 already registered (EXIT vs hold, 2027-05-24); H-097 (F6, calibration + reversal, register with DP-58 look), H-098 (F6, Explorer first); PI-014 addendum (HOLD unreachable)
- [x] FMP API key granted to the desk (Haci, 2026-09-15) → `FMP_API_KEY` loads via desk_env; Haci added it to CLAUDE.md rule 1 himself (guarded file); scope and knowledge-time rules in research/data/DATA_NOTES.md 'External source: FMP'; steward check on H-022's insider-history blocker noted in DEFERRED.md
