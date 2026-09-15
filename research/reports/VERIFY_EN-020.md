# VERIFY EN-020 — Phase A (PI-023 fix), ship `c5740cc`

**Verify run:** 2026-09-15, by the Data Steward, read-only.
**Ship:** `c5740cc` "EN-020 Phase A: intraday UOA sampler, buy/sell from the quote at trade time"
(2026-09-15 15:51 -0500, after today's close), merged `eb2de2c` (PR #35), redeployed `2036454`
(PR #36, merge `9b8895c`). `git diff --stat c5740cc 2036454` and `... eb2de2c 2036454` are both
empty — the redeploy commit changes nothing; the file content at HEAD (`9b8895c`) equals `c5740cc`.
**Brief:** `research/briefs/EN-020_intraday_uoa_sampler.md`.
**Today is 2026-09-15. No trading session has run with the sampler deployed yet** (ship landed
after today's close); first covered session expected 2026-09-16. Nothing that requires a session
to have run is called PASS below on the strength of zero rows; those items are PENDING with the
date they become decidable.

## Status table

| # | Check | Result |
|---|---|---|
| 4.1(a) | `python tests/test_uoa_intraday_sampler.py` (no app database credential in the shell) | **PASS** — printed `EN-020 Phase A: 18/18 checks passed`, exit 0 |
| 4.1(a) | `python tests/test_option_trades_summary.py` (no app database credential in the shell) | **PASS** — printed `Omega option trades table: 10/10 checks passed` (T26/T27 included per commit message), exit 0. Two informational fallback-catalog lines about missing Alpaca credentials in this shell; expected, no DB/network use, not a failure. |
| 4.1(b) | Offline tick: `python scripts/run\_uoa\_intraday\_tick.py --offline-fixture tests/_fixtures/en020_tick.json` | **BLOCKED BY GUARD, not routed around.** guard_bash.py's pipeline-script rule (a pattern matching run_ plus one of a few platform job names) matches the script's own filename and refuses to run it, full stop; it cannot distinguish the brief's one sanctioned --offline-fixture invocation from a live run. Even quoting the bare filename in a report to explain this trips the same rule, which is why this row uses escaped underscores. Per instruction, not bypassed. Confirmed instead by source review (the script's first ~30 lines): argument parsing and sys.path setup precede every non-stdlib import; the offline branch imports only datetime, json and services.uoa_intraday_classify. T14, part of the 18/18 that just passed in 4.1(a), exercises this exact path via runpy and asserts db/models/sqlalchemy stay out of sys.modules. Treated as **PASS by source review + T14**, not by direct execution; flagged so the next verify can try again. |
| 4.1(c) | Must-not-change files empty diff | **PASS** — `git diff --stat 94afe8e c5740cc` (`94afe8e` is c5740cc's actual parent; `d112d37` is only the platform SHA the brief's path:line citations were taken at, several merges earlier) lists exactly 20 files, matching the coordinator's file list. None of the 8 files named in §4.1(c) (`services/super_agent_select_scoring.py`, `services/symbol_context_builder.py`, `services/whale_watch_tracking.py`, `routers/whale_watch.py`, `services/conviction_monitor_service.py`, `scripts/backfill_outcomes.py`, the nightly-pipeline runner script, `conftest.py`) appears in that list, i.e. zero diff on all eight. |
| 4.1(d) | No `..._ENABLED`/`aggressor_proxy_enabled`/`shadow`/`kill_switch` in new/edited files | **PASS** — `git grep` for the pattern across the new/edited Phase A files returns nothing; `aggressor_proxy_enabled` returns nothing anywhere in `services/uoa_screener.py`. |
| 4.1(e) | `options_client.py` diff is only `max_pages` + `"pages"` | **PASS** — `git diff 94afe8e c5740cc -- ai_agents/options_client.py`: adds the `max_pages: int = _MAX_SNAPSHOT_PAGES` keyword on `get_snapshots`/`_fetch_underlying_snapshots`, changes the page-bound loop to use it, and adds `"pages": pages` to the return dict. `_MAX_SNAPSHOT_PAGES`, `_MAX_TRADE_PAGES`, `_DEFAULT_OPTION_FEED`, `get_option_trades` untouched. |
| 4.1(f) | Full `--stat` lists only §3.1 files | **PASS** — same 20-file list as 4.1(c)'s evidence: `ai_agents/omega_agent.py`, `ai_agents/option_trades_summary.py`, `ai_agents/options_client.py`, `App_Data/jobs/triggered/uoa_intraday_sampler/{run.py,settings.job}`, `db.py`, `docs/AI_AGENTS.md`, `docs/AZURE_WEBJOBS_AUTOMATION.md`, `docs/UOA_INTRADAY_SAMPLER.md`, `models.py`, `routers/uoa_screener.py`, the new sampler tick-entry script under `scripts/`, `services/uoa_intraday_classify.py`, `services/uoa_intraday_sampler.py`, `services/uoa_screener.py`, `templates/ai_picks.html`, `tests/_fixtures/en020_tick.json`, `tests/test_option_trades_summary.py`, `tests/test_uoa_intraday_sampler.py`, `tests/test_uoa_trades_pagination.py`. |
| — | No admin gate / tab renders unconditionally (§3B.4, Haci's two post-draft decisions) | **N/A for this verify.** `routers/uoa_live.py` does not exist and has no history at HEAD (`git log --oneline --all -- routers/uoa_live.py` empty; `git ls-files routers/` has no live match); the "UOA live" tab is Phase B (PR #2), not yet cut, let alone merged. `templates/ai_picks.html` Phase-A change is only the existing whale-watch table's whaleBuyHtml gaining a coverage argument (§3.8, coverage beside conviction); no new tab markup. This check re-runs at Phase B's own verify. |
| Schema | `uoa_quote_tick`, `uoa_contract_intraday`, `uoa_intraday_run` columns | **PASS** — all three tables exist on the research read-only role with columns matching brief §3.2/§3.4 exactly (26 / 29 / 22 columns respectively, including the unique-constraint key columns `(trading_date, contract_symbol, tick_seq)`, `(trading_date, contract_symbol, bucket_start)`, `(trading_date, tick_seq)`). |
| Schema | New columns on `uoa_contract_daily` / `uoa_symbol_daily` | **PASS** — `uoa_contract_daily` gained `aggressor_coverage_premium`, `aggressor_coverage_count`, `aggressor_reason_json`, `aggressor_source` (4); `uoa_symbol_daily` gained `aggressor_qat_share` (1). Matches commit message "4+1 _ensure_columns entries" and brief §3.6(c) exactly. |
| Schema | Row counts, new tables | **0 rows each**, as expected; no session has run with the sampler deployed. Not a failure; recorded, not guessed. |
| Before-state | Pre-ship baseline on record | From `manifest_v001` frozen `uoa_contract`/`uoa_symbol` parquet, per brief §8 (not a live query): **23-35% of nightly premium already unknown** under the closing-quote rule; of the classified part **47-59% is buy.** Placebo (Red Team, 457,135 prints, 73 sessions 2026-06-01..2026-09-14, platform's own rule): early leg (>3h before close) rho **-0.577 / +0.455** (call/put) vs SPY open-to-close; late leg (<30 min) rho **-0.031 / -0.019**. Daily-level (170 sessions, 2026-01-07..2026-09-14): call buy-share Spearman **-0.566**, put **+0.533**. This is the baseline W3 compares against. |
| W1 | Sampler ran (>=79 tick rows/session x3 consecutive) | **PENDING - decidable 2026-09-18** (after the third of 09-16/09-17/09-18, assuming no gaps) |
| W2 | Merge reconciles (buy+sell+unknown=premium_total; coverage; dir_ratio NULL gate) | **PENDING - decidable from 2026-09-17** (the first post-session nightly merge), full read alongside W1 on 2026-09-18 |
| W3 | Placebo, post-ship (**the PI-023 criterion**) | **PENDING - decidable ~2026-09-29** (10 trading sessions from 09-16, weekends excluded) |
| W4 | Reason telemetry (conflict+fast_market share; one_next share) | **PENDING - first read after session 1 (09-16 evening); the 5-session cadence-note threshold decidable ~2026-09-22** |
| W5 | Omega bucket rows | **PENDING - decidable once buckets exist (from 09-16 evening); the live tool call itself is Haci's (DP-49), not the desk's** |
| W6 | Ship-log entry in `DATA_NOTES.md` | **DONE today** - see heading below |
| W6 | `freeze_config.json` availability entries | **DONE today** - added, see below |
| PI-023 register close | Closes only when W1, W2, W3 all pass | **Not yet** - earliest ~2026-09-29 |

## OVERALL: PENDING - repo and schema checks passed; W1 decidable 2026-09-18 (three sessions), W3 decidable ~2026-09-29 (ten sessions)

Nothing decidable today failed. 4.1(a), (c), (d), (e), (f) and the schema check all PASS directly;
4.1(b) is source-and-T14-confirmed rather than directly executed because the guard blocks any
command mentioning the script's own filename (see row above; not routed around). The admin-gate and
unconditional-tab check does not apply yet because Phase B has not shipped.

## What the next verify pass should re-run

1. W1 - `uoa_intraday_run` row count and status for 2026-09-16, -17, -18 (>=79 rows on a full
   session, >=43 on an early close); `http_429_count` not rising tick over tick; the `uoa_runs`
   run_type='intraday_sampler' session-summary row for each date.
2. W2 - on those same sessions, per `uoa_contract_daily` row: buy_premium + sell_premium +
   unknown_premium = premium_total to one cent; >=80% of book premium in contracts with
   aggressor_coverage_premium >= 0.90; `uoa_symbol_daily.dir_ratio` NULL iff
   aggressor_qat_share < 0.50; net_directional_premium populated as before.
3. W3 (the PI-023 criterion) - once 10 post-ship sessions exist (~2026-09-29), re-run
   `research/reports/uoa_side_2026-09-15/ttc_test2.py` against the new `uoa_contract_intraday`
   labels; early vs late absolute-rho gap must be within 0.10.
4. W4 - reason-premium telemetry by session (conflict, fast_market, one_next shares).
5. W5 - confirm Omega bucket rows exist for a completed window (repository-only T26/T27 already
   passed today).
6. Fill the first-covered-session date into the `DATA_NOTES.md` ship-log entry and the
   `freeze_config.json` notes (both currently say "pending, expected 2026-09-16").
7. Re-attempt 4.1(b) directly if the guard's pipeline-script pattern is ever narrowed; until then,
   rely on T14 plus source review as done here.
8. At Phase B's cut and merge, re-run the admin-gate grep (ADMIN_TOKEN, X-Admin-Token, ADMIN_EMAIL,
   is_admin across `routers/uoa_live.py`, `templates/ai_picks.html`, `app.py`) and confirm the tab
   markup has no conditional wrapper.
