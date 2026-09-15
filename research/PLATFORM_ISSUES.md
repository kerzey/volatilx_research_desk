# Platform issues register

Defects and hazards in the VolatilX platform that the desk has found while doing its own work.
This is the follow-up list Haci asked for. It is separate from the LEDGER (verdicts on research
questions) and the BACKLOG (hypotheses). Anything here that becomes a *behaviour change* to
scoring or selection still goes through a research question and a full IMPLEMENTATION_BRIEF
(CLAUDE.md rule 11). Plain bug fixes take the short route below.

## How an issue gets fixed

1. Desk finds it, records it here with evidence (`path:line`, dates, a reproducing query).
2. Haci decides: **fix** (bug — short route), **research first** (it might be a feature, not a
   bug), or **accept** (document and move on).
3. Short route: `@brief-writer fix-brief PI-NNN` produces `research/briefs/PI-NNN_slug.md` — a
   self-contained prompt for the coding agent in the platform repo, with the reproducing query,
   the expected behaviour, a test, and a rollback. **No feature flag, shadow mode or inertness
   proof — ever (DP-59, Haci 2026-09-15): fix is fix.** The brief names the before/after check the
   steward runs after deploy, and says which numbers will change if any.
4. Haci runs the brief in the platform repo, records the PR / SHA here, and the steward
   confirms on the next freeze that the data changed as expected. Then status → `VERIFIED`.

Statuses: `OPEN` · `HACI_DECIDED:<fix|research|accept>` · `BRIEF_WRITTEN` · `IMPLEMENTED:<sha>` · `VERIFIED` · `ACCEPTED`

| ID | Severity | Status | Issue |
|---|---|---|---|
| PI-001 | high | FAILED:merged to main but no date recovered (still ~5%, 21–25/498 through 2026-09-02) — deployed nightly likely not running d19c9a9 | `uoa_symbol_daily.fwd_return_*` still ~95% degraded; 30d relapsed to 0% from 07-27 — brief: `research/briefs/PI-001_fwd_return_backfill_window.md` |
| PI-002 | high | HACI_DECIDED:fix | No coverage watchdog fires on PI-001 (none found in the codebase by that name) |
| PI-003 | med | HACI_DECIDED:fix | `atr_pct` corrupted around splits (ATR computed on raw bars) |
| PI-004 | med | HACI_DECIDED:fix | Manual re-runs indistinguishable from nightly runs in `super_agent_select_runs` |
| PI-005 | med | HACI_DECIDED:accept | `market_regime_daily` not point-in-time before 06-09 (backfilled) |
| PI-006 | low | HACI_DECIDED:fix | 16 published picks have no target ladder |
| PI-007 | low | HACI_DECIDED:fix | `industry` populated for only 12% of candidates |
| PI-008 | low | HACI_DECIDED:accept | Smart-money layer weight forced to 0; CLAUDE.md weights text says 5 |
| PI-009 | research | HACI_DECIDED:research | L1/L2 targets sit inside one day's range (median 0.31 / 0.55 ATR) — targets are not ATR-scaled |
| PI-010 | research | HACI_DECIDED:research | Elite (90+) count falling: Apr 8 · May 13 · Jun 12 · Jul 8 · Aug 3 · Sep 2 |
| PI-011 | high | HACI_DECIDED:fix | Printed swing stop on the wrong side of the pick-night close for 67 of 382 published picks (17.5%) |
| PI-012 | med | HACI_DECIDED:research | 2026-06-26: three qualified, ranked picks the night's own run audit does not record; no run-history table |
| PI-013 | med | OPEN | `uoa_symbol_daily.score_swing` / `score_long` overwritten in place by the next-morning OI-confirmation pass; no point-in-time copy |
| PI-014 | high | BRIEF_WRITTEN | Conviction Monitor's polarity arm silent since 2026-06-01: `polarity_unavailable_coverage_low` on 100% of in-scope rows, 0 polarity HOLD/EXIT rows — the EXIT tier is the technical arm alone — brief: `research/briefs/PI-014_conviction_monitor_polarity_ordering.md` (2026-09-15; monitor becomes a nightly-pipeline step after `uoa_oi_gex`, 16:02 WebJob removed, no flag per DP-59; Q019 window-start move per its DECISIONS #12(a), Q038 re-entry restarts at the ship date). **⚠ Ship EN-020 Phase A first (2026-09-15).** This fix wakes the polarity arm, which computes polarity from `uoa_contract_daily.buy_premium / sell_premium` (`conviction_monitor_service.py:892-899` → SAS's `_compute_flow_polarity`) — the exact field PI-023 shows is a record of the day's price drift. Shipped first, the monitor's EXIT signals inherit the artefact, and Q019's re-measured rate and Q038's re-entry are set on contaminated nights. After EN-020, uncovered premium is `unknown`, so the arm's own 0.5 coverage gate (`:184`) abstains honestly instead of firing on drift. |
| PI-015 | high | OPEN | Projection layer (v1.6 weight 29, the largest) unscored — `available: false` — on 72.2% of published and 74.3% of capped main-lane rows; `overall_score` is a six-layer blend on ~3 of 4 picks |
| PI-016 | med | OPEN | Conviction label degenerate on the published slate: `completeness_score` never below 65.37 (min 65.3686 of 4,195 scored rows), so `_confidence_label`'s completeness arm is inert — 401 high / 141 medium / **0 low** on 542 published rows, every `medium` the `[80,82)` score sliver; the subscriber sentence at `services/super_agent_select_public.py:212` re-prints "is the score ≥ 82" |
| PI-017 | high | IMPLEMENTED:bccfa67 (code verified 2026-09-14; deploy unconfirmed -- V3 re-check after the next nightly that runs bccfa67; see reports/VERIFY_PI-017.md) | A forced UOA re-run deletes the **whole trading date** from `uoa_contract_daily`, `uoa_symbol_daily` and `uoa_bulletins`, then rebuilds only the symbols it was given — so the single-symbol range runner with `--force` wipes ~498 other symbols and the night's bulletins (a SAS candidate-universe source); the run still records `success`. Signature seen once, 2026-01-09 (23 of ~499 symbols), before every study window. Brief: `research/briefs/PI-017_forced_uoa_rerun_delete_scope.md` (2026-09-14) |
| PI-018 | high | OPEN | Multi-agent technical report: the per-timeframe BUY/SELL call is not a faithful read of the technicals. A ≥ 70-strength signal with "medium" confidence is dropped (neither counted nor held), then "within 2% of a Fibonacci support" turns it into **BUY** — in the SNDK 2026-09-11 sample a 71% **bearish** 15m signal printed as BUY. Support is checked before resistance, so ties go to BUY; and `hold_count` is decremented without having been incremented, so the consensus tally is wrong (sample shows 2/2/2 across 7 timeframes). `day_trading_agent.py:749-804`. **At scale (697 reports): 12.6% of directional calls oppose their own timeframe's bias; 76.1% cite "Near Fibonacci"; 50.1% of reports print a wrong tally** |
| PI-019 | med | OPEN | Multi-agent technical reports: the zone-less `timestamp` switched from **UTC** (to 2026-04-05) to **US Eastern** (from 2026-04-07; both on 04-06) with no marker; and no report records whether it came from a subscriber (`/analyze`) or the internal batch (`user_id=1`, 73.6% of reports). Anything reading report times or treating reports as subscriber demand is silently wrong for part of the history |
| PI-020 | high | VERIFIED:3f1d3e6 (PR #32 merged e513d44, 2026-09-15; **D0 = 2026-09-15**; repo PASS, W5 history unchanged to the row, W1 PASS on all 15 capped names (SNDK dir_ratio 1.00 -> -0.0575, 0 -> 7,222 put prints), W2 PASS (0 ceiling hits, 0 failures), W3 PASS on a substitute (put zero-print share 74.0% -> 17.5%; the brief's literal W3 is void — `snapshot_volume` is NULL on every row), W6 0/78 on D0 and confirms ~2026-09-29; research/reports/VERIFY_PI-020.md) — BRIEF_WRITTEN | **UOA scanner truncates option trades: the flow layer is blind to puts on the most liquid names.** `AlpacaOptionsClient.get_option_trades` (`ai_agents/options_client.py:985-1018`) requests up to 50 contracts with `limit=1000` (`services/uoa_screener.py:1505-1510`, `trades_limit` at `:806`) and never follows `next_page_token`. Alpaca sorts by contract symbol, so calls fill the page and puts get nothing. SNDK 2026-09-08: stored 2,000 trades, all calls, `dir_ratio` 1.00; paginated, the same contracts traded 14,441 calls ($200.7M) and 11,154 puts ($82.5M). **~15–16% of symbol-days hit the cap every month since 2026-01; 317 of 604 published SAS picks since 2026-06-01 were scored on capped flow** (GOOG, MSFT, AMZN, SNDK, ORCL… capped every day). Biases `call/put_premium_total`, `dir_ratio`, flow scores and the flow direction votes bullish. Evidence: `research/reports/case_SNDK_2026-09-15/` — brief: `research/briefs/PI-020_uoa_trades_pagination.md` (2026-09-15, rewritten 2026-09-15 under DP-59: ships directly, no flag, no shadow — from the ship date `put_premium_total`, `dir_ratio`, flow scores and SAS flow votes change for liquid names; no historical row rewritten; the desk logs the ship SHA/date in DATA_NOTES so Q014/Q019/Q029/Q030 split there under DP-50) |
| PI-021 | high | OPEN | **Running the platform test suite deletes every user.** `conftest.py:37-55` (platform `c311e81`) has an autouse fixture that deletes all rows of `UserActivityEvent` and `User` before and after *every* test, and `conftest.py:31-35` runs `create_tables()`, against whatever database the test environment's connection URL names (`conftest.py:9-21` refuses only SQLite). Pointed at production, `pytest` empties `users` and `user_activity_events`. The PI-017 fix brief (§4(c)) told the coding agent to run `python -m pytest tests/ -q` on the base commit and after; PI-017 merged as `575df11`. **Not verified whether that run touched production** — first check: row count and newest signup in `users` against what you expect. Found 2026-09-15 by the Brief Writer while writing EN-019. |
| PI-023 | high | OPEN | **Option buy/sell side is judged against the closing quote, so the label follows the day's price drift.** `services/uoa_screener.py:1114-1116` keeps the closing snapshot's bid/ask and `:1246-1256` classifies every print of the session against it. Over 170 sessions the daily call buy-share runs *against* the tape (Spearman −0.57 with SPY open-to-close) and the put buy-share *with* it (+0.53): up days show 43% of call premium "bought" and 60% of put premium "bought", down days 62% / 41%. **Placebo (Red Team):** for prints in the last 30 minutes, where the closing quote *is* the quote at trade time, the correlation is zero (−0.03 / −0.02); for prints > 3 h before the close in the same contracts on the same days it is −0.58 / +0.46 — the artefact, not trader behaviour. Feeds `dir_ratio`, `call/put_buy_premium`, the SAS flow vote (`super_agent_select_scoring.py:555-560`), Whale Watch qualification (ask-share ≥ 0.65, `whale_watch_tracking.py:114-116`) and the UOA "conviction" column. Alpaca keeps no historical option quotes, so this cannot be repaired after the fact: the quote must be captured during the session → **EN-020** (intraday sampler). Evidence: `research/reports/uoa_side_2026-09-15/REPORT.md` §2, `drift_test.py`. Blocks H-092 alongside PI-020. |
| PI-022 | med | OPEN | **Conviction Monitor wrote nothing on 2026-07-06** — `conviction_monitor_daily` has 0 rows for that session while every other in-window session carries 31–56 (frozen `manifest_v001`; `research/reports/STEWARD_Q038_exposure.md` item 3). A complete one-day outage of the monitor job, not a holiday (07-06 was a normal session; 07-03 was the holiday, and holidays still get off-calendar rows). No watchdog fired; the 24 picks of 06-29/06-30/07-01 lost their day-3/day-4 row and are excluded as `monitor_coverage_outage` in `exclusions_v004.json` (Q019 and Q038 read this table). Same watchdog gap as PI-002 — the PI-002 fix brief should add this table to the coverage check |

## Detail

### PI-001 — fwd_return freeze not fixed
**Evidence:** FREEZE_v001 §5. `fwd_return_30d_pct` coverage 99% → 0% from 2026-05-20;
14d from 06-12; 5d from 06-26; writes resume 07-06 at ~5% of baseline; 30d back to 0% for
`trading_date ≥ 07-27`, well past maturation. CLAUDE.md said "fixed" — corrected 09-10.
**Desk impact:** none now — the desk computes forward returns from its own price freeze.
**Platform impact:** anything on the product that reads these columns (UOA performance surfaces)
is showing mostly nulls. **Recommend: fix.**
**Implemented 2026-09-13, `2d5776c`** — `resolve_backfill_window()` clamps any caller's window into
[65, 100] sessions in-process, so the stale Azure WebJob wrapper can no longer shorten it; the
effective window is now printed on every run. Two files, no scoring path touched.
**MERGED, DEPLOY UNKNOWN (corrected 2026-09-14).** `2d5776c` is on `main` via merge commit `4775e49` (PR #26, "Merge pull request #26 from kerzey/fix/pi-001-backfill-window-floor", 2026-09-13 18:02:57 -0500); `git show --stat 4775e49` confirms exactly the two files the brief named (`scripts/run_nightly_pipeline.py`, `tests/test_nightly_pipeline_backfill_window.py`) and nothing else. Whether this has reached the production WebJob (brief §3 Step A') and whether a nightly has run it are unknown to the desk from a read-only git+DB check. See `research/reports/VERIFY_PI-001.md` §8 for the 2026-09-14 pass -- verdict PENDING, not VERIFIED.

**Second 2026-09-14 pass, verdict FAILED (verification-blocked, not a code finding).** Merge to `main` re-confirmed (git-only); the deployed WebJob wrapper source already requests 65 trading days. But the brief's actual proof -- the §8 coverage-recovery DB check -- could not run: no desk credential (`RESEARCH_DB_URL` or otherwise) was present in that session, and Azure WebJob logs are not visible to the desk at all. FAILED here means "not verified as recovered," not "the fix is broken." See `research/reports/VERIFY_PI-001.md` §9.

**Residual hole — one reconciled statement (2026-09-13, after two verify passes disagreed).**
Both passes counted correctly; they counted different sets, and both summaries were imprecise.
Recomputed once more from `research/data/v001_uoa_symbol.parquet`, counting only dates whose
30-session window had closed by the freeze `as_of` 2026-09-10:

| set | dates | missing cells | range |
|---|---|---|---|
| due and **zero** 30d coverage | **35** | **17,402** | 2026-04-15 .. 2026-07-29 |
| due and partially filled, under 95% | 15 | 7,098 | the ~24-symbol bulletin trickle |
| **all** due dates under 95% | **50** | **24,500** | 2026-04-15 .. 2026-07-29 |
| of the zero set, **cannot** be reached by any nightly window | 15 | 7,460 | 2026-04-15 .. 2026-06-08 |

The second pass's headline "36 dates / 17,896 cells" double-counts: its own date list enumerates
35 dates including the 2026-04-15 / 04-17 pair, then adds that pair again in the caption. Its list
is right and matches this recount exactly. The first pass's "15 dates / 7,460 cells" is the subset
no nightly can ever reach, and was stated as though a deploy had already landed. It had not.

**Sweep range: `--start-date 2026-04-15 --end-date 2026-07-29`.** Wider is free here — the backfill
is NULL-only, so dates that would have self-healed are simply skipped — and it makes the result
independent of when the deploy lands. Use this range, not either narrower one. Still Haci's call,
still never `--force`.

**Not `VERIFIED`:** merge, deploy, one nightly, then the read-only coverage check, in that order.
Full working in `research/reports/VERIFY_PI-001.md` §6 and §7.

**On the `patch7.py` flag raised by the second pass:** staging an enforcement-file edit as a script
under `docs/admin_pass/` for Haci to run is the desk's documented mechanism for rule-15 files —
patch4, patch5 and patch6 all do it, and `docs/HOW_THE_DESK_WORKS.md` names it. The desk did not
run it. Haci applied it himself on 2026-09-13, before establishing that the research URL and
production are one database; patch7 has since been corrected and now replaces its own superseded
section on the next `--apply`.

### PI-002 — no watchdog caught PI-001
**Evidence:** a ~95% shortfall persisted for 3+ months. `grep` for a fwd_return coverage
watchdog finds only `scripts/phase2_signals/feasibility.py:7`, a one-off feasibility note.
**Recommend: fix** — a nightly coverage check with a threshold (the desk's own
`research/lib/daily_check.py` shows the shape: trailing median, floor, RED on a drop).

### PI-003 — ATR corrupted around splits
**Evidence:** EXPLORE_001 §9. BKNG `atr_pct` up to 0.49 (true ≈ 0.04–0.06), CVNA up to 0.55.
Cause: ATR over raw bars spanning a split. The W60 grader already de-splits bars
(`scripts/backfill_w60_outcomes.py:185-193`); the ATR path does not.
**Platform impact:** any ATR-based target or sizing on a recently split name is wrong for ~14
sessions. **Recommend: fix**, reusing the grader's de-split.

### PI-004 — manual runs look like nightly runs
**Evidence:** runs for 05-11, 05-12, 05-13, 05-14, 07-06 finished after the next session had
opened (`finished_at`), with mixed-date `spot_close` (TER 07-06: −9.6%). Haci confirms these
were manual development re-runs. Nothing in `super_agent_select_runs` marks them as such.
**Desk impact:** handled by `research/data/exclusions_v001.json`.
**Recommend: fix (small)** — a `run_kind` column (`nightly` / `manual` / `backfill`) written by
the entry point, so the next manual run is self-declaring. Also lets the product hide manual
runs from subscriber-facing history.

### PI-005 — regime history backfilled
**Evidence:** FREEZE_v001 §7. Three `regime_version` rows per date for 01-02..06-08, all
written 06-02 / 06-08. Live same-night writes only from 06-09.
**Recommend: accept**, with the desk rule "regime-stratify from 06-09 only". Nothing to fix
going forward; the label is now written on the night.

### PI-006 — picks without a ladder
16 published picks lack lane targets in `public_payload_json`. A subscriber saw a pick with no
plan. **Recommend: fix** — publication should require all three lanes' targets, or mark the
pick as plan-pending.

### PI-007 — `industry` mostly empty
12% populated. Blocks sector-cluster questions (H-034) and any sector-aware product feature.
**Recommend: fix** — populate from the fundamentals source already used for `fundamental_quality`.

### PI-008 — smart-money weight is zero
`services/super_agent_select_scoring.py:709-710` forces the weight to 0 when
`enable_smart_money_enrichment` is off; the column has been null since April. Not a bug — a
disabled feature — but CLAUDE.md's "smart-money 5" and any marketing of a seven-layer score
overstate it. **Recommend: accept + docs**, or decide whether to enable.

### PI-009 — targets are distance, not forecast *(research first)*
EXPLORE_001: L1/L2 median 0.31 / 0.55 ATR from the close. The strategist prompt asks for two
targets per lane with no volatility scaling (`ai_agents/principal_agent.py:530-575`). If the
sealed period confirms H-053, the change is ATR-scaled target placement — a scoring/plan
behaviour change, so: PREREG → verdict → HUMAN_APPROVED → full brief with a shadow ladder.
**Haci's view (2026-09-10):** near targets being reachable by other stocks is expected; the
differentiator is *how fast* SAS picks reach them. Product direction if that holds: quick
L1/L2 exits and capital recycling on sub-elite picks, deeper holds on elite picks, and
strategies built on speed. Registered as H-065 / H-066; the research question tests speed
against a distance-matched control, unconditionally, before any target redesign.

### PI-010 — elite is thinning *(research first)*
Published 90+ picks per month fell from 12–13 (May–Jun) to 3 (Aug) and 2 (Sep to the 10th);
the candidate median score fell 67.3 → 62.7 on 09-10 (daily check). Haci wants to know why.
Candidates: score-distribution drift after the 06-01 catalyst fix, weaker tape, GEX nulls
(+5 completeness offset), or universe changes. This is a Registrar question (calibration
family F2), not a fix.

### PI-011 — printed stop on the wrong side of the entry
**Evidence:** STEWARD_Q009_exposure §R1(a). 67 of 382 published picks with a swing lane and an L3
(pick nights 2026-06-01..08-12, matured) carry a printed swing `stop` on the **wrong side of the
pick-night close** — for a bullish pick, a stop above the close, i.e. already breached at publication.
**Cause (read-only):** the stop is written by the Principal Strategist off the lane `entry`, which may
stray more than 5% from spot (`services/super_agent_select_service.py:101-111`), and is passed into
`public_payload_json` **unvalidated** (`:94-95`, `:158`), while targets *are* checked against spot and
entry (`:113-152`). It is shown to subscribers on the report card
(`report_center_frontend/components/ReportCard.tsx:254-255`).
**Desk impact:** these picks are excluded from Q009, which therefore speaks for 303 of 383 published
picks (79%).
**Recommend: fix** — a side-and-distance guard on the written stop, mirroring the existing target
guard. **Timing note:** rule 11 applies with unusual force here — a stop-side guard must not go
flag-on before Q010's decision date, or Q010 would be replicating Q009 on a different population
(Q010 §10.6).

### PI-012 — 2026-06-26: ranked picks the run audit does not record
**Evidence:** STEWARD_Q009_exposure §R3 ruling 1. The frozen `sas_candidates` table holds 11 qualified
rows with a `selected_rank` for that trading date; the run's contemporaneous `stats_json` records 8,
all bullish. The three extra bearish rows (DPZ, COIN, AAPL) carry complete lane plans, including swing
stops, with the payload `rank` matching the outer `selected_rank`. It is the only night in 113 with
this mismatch.
**Desk impact:** the whole night is excluded (`exclusions_v003.json`, `uncorroborated_publication_runs`);
usable nights 103 → 102. Q006 and Q007 are locked citing earlier exclusions files and include that
night — flagged to the Red Team for their reviews, never edited.
**Recommend: research first** — the write path cannot be reconstructed from the desk side, because
`super_agent_select_runs` is updated in place with no run-history table. Two questions for the platform:
what wrote those rows, and should there be an append-only run-history/audit table — its absence is what
makes this and the KT-audit re-run nights unrecoverable rather than merely detectable.

### PI-013 — UOA scores rewritten next morning with no audit trail
**Evidence:** Registrar draft of Q014 (H-040), 2026-09-13. volatilx `services/uoa_screener.py:2236-2239`
multiplies `score_swing` and `score_long` in place by `oi_mult` (0.90 / 1.00 / 1.05 / 1.10, stored in
`oi_confirm_mult`, `:2223-2232`) during the next-morning open-interest confirmation pass, and the
bulletin's lists are re-ranked from the mutated scores (`:2245-2303`). `label_*` is written once,
pre-multiplier (`:1728-1734`). The row therefore carries the *morning* score under a column that
every downstream reader treats as the 16:05 ET screener output. FREEZE_v001 §7 flagged the OI lag
for older rows only.
**Desk impact:** any study conditioning on `score_swing` / `score_long` must divide out
`oi_confirm_mult` to recover the pick-night value (Q014 PREREG §2.1 does exactly that; no rule-14
exception needed because the multiplier is stored). Rows where `oi_confirm_mult` is null cannot be
told apart from unconfirmed ones.
**Recommend: fix** — keep the 16:05 score in its own column (`score_swing_pt`, `score_long_pt`) or write
the confirmed score to a new column and leave the original untouched; either way the point-in-time
value must survive. Fix, not research: no behaviour changes, only where a value is stored.

### PI-014 — the Conviction Monitor's polarity arm has been dark since 2026-06-01
**Diagnosis (steward, 2026-09-15):** `research/reports/STEWARD_PI-014_diagnosis.md` — cause is job ordering (the 16:02 ET monitor WebJob reads same-day `uoa_contract_daily` before the 16:05 pipeline's `uoa_oi_gex` step writes it), onset **2026-05-19** (first live run, not 2026-06-01), decomposition healthy, not PI-020; fix brief `research/briefs/PI-014_conviction_monitor_polarity_ordering.md`.
**Evidence:** `research/reports/STEWARD_Q019_exposure.md` §6 and §8, counts only, on the pinned
freeze (`manifest_v001`, table key `conviction_monitor`, 3,339 rows; no live query, DP-50(c)).
`polarity_unavailable_coverage_low` appears in `reason_codes_json` on **100% of in-scope monitor rows
in every month 2026-06 through 2026-09**, with **0 exceptions**; `polarity_tier` is `WATCH` on
**every** row dated ≥ 2026-06-01 (0 HOLD, 0 EXIT); the only 35 polarity-EXIT and 53 polarity-HOLD rows
in the whole freeze are in **May 2026**, when the arm still worked (80.3% unavailable then, so it was
already degrading). Consequence: **284 of 284** primary EXIT flags on pick nights
2026-06-01..2026-08-26 fired via the technical arm alone, on a tier that prints EXIT for **61%** of
published picks within five sessions.
**This is not the 2026-05-16 polarity rollback.** `docs/POLARITY_ROLLBACK_2026_05_16.md` disabled
v1.6 polarity **in SAS scoring** by flipping `SuperAgentSelectConfig.flow_polarity_enabled` to
`False`. The monitor does not read that flag — it recomputes polarity locally
(`services/conviction_monitor_service.py:906-937`, `:1177-1186`) — and it kept writing polarity
HOLD/EXIT rows for two weeks *after* the rollback shipped, dying at the 2026-05-31 / 06-01 boundary.
A "working as intended" reading of the silence is wrong.
**Cause (read-only, and not in the monitor):** the monitor's tier code has not changed since
**2026-05-16** — `git log --follow services/conviction_monitor_service.py` returns exactly three
commits, all that day (13234cc / baf17b8 / 2cb7a7e), and nothing since; `scripts/run_conviction_monitor.py`
and `routers/conviction_monitor.py` show no commits since the manifest SHA `fa70688`. So this is an
**input** failure, not a logic change. The gate is `services/conviction_monitor_service.py:184-185` —
`coverage is None or coverage < config.polarity_coverage_threshold → ("WATCH", ["polarity_unavailable_coverage_low"])`
— where `coverage_ratio = decomp_premium_total / contract_premium_total` (`:928-937`) is built by
`services/symbol_context_builder.py:136-175` from **`uoa_contract_daily.buy_premium` /
`sell_premium` / `premium_total`**. A 100% failure means the **aggressor decomposition** is empty or
near-empty for the monitored symbols on every date since 2026-06-01, or `premium_total` has been
inflated relative to it. Same table family as **PI-001** (`uoa_symbol_daily` write degradation from
2026-05-20, still ~5% of baseline) and still uncovered by any watchdog (**PI-002**) — the third silent
UOA-side degradation, and the first to reach a paid surface's logic.
**Reproducing check — for the Data Steward on `$RESEARCH_DB_URL`, read-only.** `uoa_contract_daily` is
**not** in `manifest_v001`, so this is an operational diagnosis, not a study input and not a brief's
before-snapshot; it is addressed to the Steward and never to the coding agent (DP-49). By month from
2026-04-01, over the SAS published-pick symbols: the share of `uoa_contract_daily` rows with
`buy_premium + sell_premium > 0`, the median `(buy_premium + sell_premium) / premium_total`, the row
count per date, and the date the median first falls below `polarity_coverage_threshold`. Plus, from
the read-only platform repo, `git log --follow services/symbol_context_builder.py` and any change to
`ConvictionMonitorConfig`'s polarity thresholds between 2026-05-20 and 2026-06-10 — R1 item (7) dated
the monitor service only, so the builder and the config are the two unexamined code paths. If a fix is
briefed, pin that coverage aggregate in the successor freeze so the before/after is reproducible
(DP-50(c)).
**Desk impact:** Q019 (locked 2026-09-13, decision 2027-05-24) tests "the Conviction Monitor's EXIT
tier" and therefore tests **the technical arm alone** for the life of its window; the restriction is
written into its §1/§8/§9 and travels with the verdict (Q019 DECISIONS #10). No other locked question
reads this table.
**Recommend: fix — and fix the input, not the gate.** The coverage threshold is doing its job;
lowering it would publish a polarity tier computed from a fraction of the premium. **DP-50(b) timing
constraint, named here as the policy requires:** restoring polarity changes which picks receive
`EXIT` — a column a locked PREREG reads — so the PI-011 / Q010 pattern applies and the choice is
Haci's. **Either** the restoration is held **flag-off until Q019's decision date, 2027-05-24**; **or**
it ships with a dated `DATA_NOTES.md` entry (column, date range, ship SHA), Q019's window start moves
to the first pick night after the ship and its schedule is recomputed at the measured 0.6885
nights/session — ≈ 8 months to refill the floor — and if that pushes the decision date past
**2027-09-13**, Q019 goes to DEFERRED (Q019 DECISIONS #12(a), DP-43's ceiling). On the arithmetic, a
ship before ≈ **2027-03-08** is survivable and one after it is not. **The desk does not ask for the
fix to be held**: a live surface with one of its two arms silent is worse than a research question
that may have to restart. The cost is written here so the choice is made with it in view.

**Addendum 2026-09-15 (census, `research/reports/monitor_counts_2026-09-15/REPORT.md`).** Two consequences
the original entry did not spell out:
- **HOLD is unreachable.** `overall_tier = _worst_tier([polarity_tier, technical_overall_tier])`
  (`services/conviction_monitor_service.py:792-805`); with `polarity_tier` fixed at WATCH the floor is WATCH,
  so the tier that means "conviction intact" cannot be printed. **0 HOLD `overall_tier` rows since 2026-06-01**
  (2,921 rows; the 1,221 HOLD values in `age_adjusted_severity` are decayed WATCHes). The subscriber sees a
  two-state monitor that rates 67% of picks EXIT within five sessions.
- **Possible input cause shared with PI-020.** `coverage_ratio = decomp_premium_total / contract_premium_total`
  is built from `uoa_contract_daily.buy_premium / sell_premium / premium_total`
  (`services/symbol_context_builder.py:136-175`). PI-020 stores zero-trade rows (`buy_premium` 0) for every
  contract the truncated trades page did not reach, which empties the decomposition on the most liquid names.
  PI-020 predates June, so it is not the whole cause; the fix brief for PI-014 should check the two together.

### PI-015 — the projection layer, v1.6's largest weight, is unscored on three of every four picks
**Filed 2026-09-14 by the registrar (autonomous run, DP-40..48), on the decision-maker's
recommendation at `research/questions/Q035_setup_architecture/DECISIONS.md`, "Platform issue
recommended to the Registrar" (DP-48). Severity high, status OPEN. Recommendation only — the decision
is Haci's, and `HACI_DECIDED` stays unset until `/desk-run prompt PI-015`.**

**Measured numbers, and where the desk read them.** `research/reports/STEWARD_Q035_exposure.md`
(Headline and limbs (a), (c), (f)), on the pinned `manifest_v001`, pick nights 2026-06-01..2026-09-10:
**72.2% of 579** `selected` bull-lane rows and **74.3% of 692** `capped_by_max_output` rows carry
`score: null, available: false, reasons: ["Projection context unavailable"], weight: 0.0` in
`score_details_json.weighted_dimensions.projection`; **not** concentrated in one timeframe (short,
swing and long all 71–79%); read directly off the frozen rows before any Q035 screen touched them.
**Second, independent desk measurement of the same hole:**
`research/questions/Q029_layer_value_ablation/PREREG.md` records `projection_score` non-null on
**62.74%** of its segment rows, clearing 70% in **no month measured** (49.44% → 65.11% peak,
plateauing below the floor from July) — which is why Q029 registered `projection` as **UNEVALUABLE**
on its E1 and E2 endpoints. Two questions, two populations, one gap. *(Related but not new:
`smart_money_confirmation_score` is null on 100% of all 6,479 frozen rows — that is PI-008's weight-0
layer, recorded here only because it is what made Q035's completeness screen reading-dependent.)*

**Why it is high, and the one thing the check must settle.** The published ranking is produced by a
seven-layer v1.6 blend in which projection carries 29 of 100 points. On roughly three of every four
published picks that layer is absent with `weight: 0.0`. **The desk cannot tell from the frozen
payload alone whether the remaining six weights are renormalized or the layer simply contributes
zero**, and the two have opposite consequences: renormalization means the published ranking is, most
nights, a **six-layer score** that is not the documented v1.6 blend; a plain zero means every affected
row is silently docked up to 29 points relative to the rows that do have projection, so a pick's rank
depends on whether its projection context happened to load. Either way the ranking every
subscriber-facing surface rests on is not the one the weights table describes, and no watchdog fires
(PI-002's family).

**Desk impact.** Q035 (H-083, setup architecture) is **DEFERRED** — `research/questions/DEFERRED.md`,
"Q035 / H-083" — because the night's publishable choice set cannot be reconstructed under a
completeness screen when three-quarters of it fails that screen: median `|P_t|` **5** against a floor
of 11, reorder rate **0.2683** against 0.50, and the reconstruction limb's registered population
**empty (0 of 41 nights)**. Q029 carries `projection` as UNEVALUABLE on two endpoints for the life of
its window.

**The platform check — repo-only, no database step (DP-49).** Everything below is satisfiable from the
read-only platform repo by the coding agent: (i) trace the writer of `available: false` /
`"Projection context unavailable"` in `services/super_agent_select_scoring.py` (the projection
subscore path around `:925` and the no-projection-origin / no-projection-context branch at
`:711-712`) back to the projection context builder and the `ai_agents/projection_expert` path, and
state in the brief which of three it is — a missing upstream projection row, a config flag or coverage
threshold, or an exception swallowed into the unavailable branch; (ii) `git log --follow` on the
projection scoring path, the projection context builder and the projection agent from 2026-04-01, to
date the step-up (the desk's own two measurements suggest it predates 2026-06-01 and worsens through
July); (iii) resolve the renormalize-vs-zero question **from the code**, and state the answer
explicitly; (iv) a pure-function unit test that feeds a synthetic projection context to the scorer and
asserts `available: true` with a non-null score, plus `git show --stat` proving no other scorer file
changed. **The coverage before/after is the Data Steward's, on the pinned parquet (`manifest_v001`)
and the successor freeze (DP-50(c))** — the brief names that parquet as the before-snapshot and never
asks anyone to capture one.

**DP-50(b) ship timing — named, decision left to Haci.** A repair rewrites `projection_score`
historically, and with it every setup label and `overall_score` derived from it. In-flight **locked**
questions that read the projection subscore: **Q029** layer value ablation — `projection_score` is a
Tier-1 layer with its own `E3_projection` endpoint and a **fixed and closed** EVALUABLE / DEAD /
UNEVALUABLE register that its schedule note says is "never revised", decision **2027-04-12**, hard
stop **2027-05-24**; **Q028** layer signal independence — `projection_score` is a Tier-1 column and
part of the object of the test, decision **2026-09-28**, hard stop **2026-10-12**; **Q026**
point-in-time integrity — `projection_score` read in its committed `eval.py`, decision **2026-09-21**,
hard stop **2026-10-05**. Every question that reads `overall_score` or the published slate is touched
as well (Q027 and Q031 share Q029's 2027-05-24 hard stop), because an unavailable layer changes the
blend that produces both. **The constraint the brief should carry: flag-off until 2027-05-24**, the
latest in-flight hard stop — or, if Haci wants it sooner, the repair ships and Q026, Q028, Q029, Q027
and Q031 each split at the ship date under DP-06 / DP-50(a), which **Q029 cannot absorb** (its
register is closed at `record` and would have to be re-derived, i.e. Q029 defers). The two nearest
dates are cheap: **Q026 2026-10-05 and Q028 2026-10-12** pass within a month, after which only the
2027-05-24 cohort binds. This is the trade-off, stated; the decision is Haci's under DP-48, and the
desk files nothing further until `/desk-run prompt PI-015`.

**Recommend: fix — the input, and then the documentation.** Restore projection coverage; and state in
the same change which of renormalize-or-zero the scorer does today, because that is what decides
whether the shipped ranking ever matched the documented v1.6 blend. If the answer turns out to be
"renormalize, deliberately", the second half is a weights-table and docs correction (the PI-008
pattern), not a scoring repair. Either way, **the behaviour change that would follow from Q035's
hypothesis is not what is asked for here** — this is a completeness fix, and any change to how the
slate is *ordered* still needs a research question and a full brief (rule 11).

### PI-016 — the conviction label is degenerate: "high" is a re-print of "the score is ≥ 82"
**Filed 2026-09-14 by the registrar (autonomous run, DP-40..48), on the decision-maker's
recommendation at `research/questions/Q036_confidence_label_validity/DECISIONS.md`, "Corrections and
filings added at record" → "Routed requests → registrar" (DP-07, DP-48). Severity med, status OPEN.
Recommendation only — the decision is Haci's, and `HACI_DECIDED` stays unset until
`/desk-run prompt PI-016`.**

**The defect, in one line.** `completeness_score` never falls below **65.3686** anywhere in the
window, so `_confidence_label`'s completeness arm is **inert**: the published label is decided by the
score alone, and the sentence *"scored X with {confidence_level} conviction"*
(`services/super_agent_select_public.py:212`) re-prints *"is the score ≥ 82"*.

**Measured numbers, and where the desk read them.** `research/reports/STEWARD_Q036_exposure.md`
§(a) / §(c) / §(e), counts only and **no outcome of any kind read**, on the pinned `manifest_v001` +
`manifest_prices_v001` against `exclusions_v003.json`, pick nights 2026-06-01..2026-09-10, 67
non-excluded nights:

- **Published label composition: 401 `high` (74.0%) / 141 `medium` (26.0%) / 0 `low` (0.0%)** on
  542 eligible published rows. **25 of 67 nights are single-label, and every one of them is
  all-HIGH.**
- **Minimum `completeness_score` = 65.3686** over **all 4,195 scored `sas_candidates` rows** in the
  window — published, unpublished, any qualification status, any date. **Every cell of both §(e)
  grids sits in the `[65,100]` completeness column**: zero rows in `[35,45)`, zero in `[45,65)`, on
  the published slate (542 rows) and on the unpublished `threshold_pass` cohort (646 rows; 564
  medium / 82 high / 0 low) alike. `Q014 §2` independently records the same floor (65.4) on its own
  control-pool screen.
- **Every `medium` row is the `[80, 82)` score sliver** — MED scores cluster in **`[80.05, 81.99]`**
  on all 26 of the both-labels nights measured.
- **The label column itself is written correctly.** Recomputing
  `_confidence_label(overall_score, completeness_score)` from the stored columns with the literal
  constants at `services/super_agent_select_scoring.py:1167-1170` gives **0 mismatches of 542
  (0.000%), 0 rounding-boundary cases** (§(g)). **This is not a mis-written column**; it is a
  classifier whose second input does not vary.
- **Why the second input does not vary — an observed correlation, not a mechanism claim.** The
  runtime `sas_runs.config_json` on **all 67** non-excluded nights carries
  `enable_catalyst_enrichment = True` and **`enable_fundamental_enrichment = True`**, with only
  `enable_smart_money_enrichment` at its coded default `False`
  (`services/super_agent_select_models.py:109-111`) — i.e. **two of three enrichment layers populate
  `completeness_score`'s numerator on every row**, and the deployment overrides the ORM default that
  several PREREGs cite. `Q029 §2` records the same flag state independently (67 of 68 segment
  nights). The tuple is constant across the window; the DP-50(a)/(b) commit sweep since `fa70688`
  returns **NONE** at HEAD `d19c9a9`, and no v1.7 promotion is scheduled.

**The arithmetic that makes it degenerate.** `_confidence_label`
(`services/super_agent_select_scoring.py:1166-1171`, called at `:1425` after the ATR-elite cap block
at `:1407-1423`, stamped at `:1451`) sets `high` ⇔ `overall_score ≥ 82 ∧ completeness_score ≥ 65`,
`medium` ⇔ ¬`high` ∧ `overall_score ≥ 68 ∧ completeness_score ≥ 45`, else `low`. On a published slate
floored at `publication_floor = 80` and `min_completeness = 35`
(`services/super_agent_select_models.py:91`, `:98`), with completeness never below 65.37, the three
tiers collapse to a single cut at 82: **`low` is unreachable and `medium` means "80.0 ≤ score <
82.0"**. A subscriber reading "high conviction" is reading a two-point score band described in the
language of confidence.

**Desk impact.** **Q036 (H-011, confidence label validity) is DEFERRED** —
`research/questions/DEFERRED.md`, "Q036 / H-011" — because its second primary's population
(`medium ∧ overall_score ≥ 82`) is an **empty cell by arithmetic**: E2's contributing-night rate
measures **0.0000 on every form** (0/47 matured, 0/71 elapsed, 0/67 non-excluded) against a gate of
0.43, while E1 clears at 0.5532. **This row is emphatically *not* a finding that the label fails to
predict the price path** — that question is Q036's, it is deferred, and **no brief and no successor
question may cite this row as evidence for it.** Elsewhere, `Q032 (:368)`, `Q033 (:476)` and
`Q034 (:498)` register `confidence_level` **terciles** as descriptive strata; on this data the column
takes two values on the published slate, so those terciles collapse to at most two cells and will sit
under the 20-contributing-night floor. Their own §4 floors already mark a thin cell descriptive, so
**nothing is owed and no locked file is edited** — it is recorded here so the collapse is expected at
their decision passes rather than discovered.

**The platform check — repo-only, no database step (DP-49).** Everything below is satisfiable from
the read-only platform repo: (i) read `_confidence_label` at `:1166-1171` and the `completeness_score
= clamp(available_weight / total_weight × 100)` computation at `:1347` over the timeframe-adjusted
effective weights at `:1316-1322`, and state **which layers can be absent at all** under the
deployed enrichment flags — i.e. what the reachable range of `completeness_score` actually is;
(ii) state whether the 65 / 45 constants were ever calibrated against an observed completeness
distribution, or were chosen against a configuration in which more layers could be missing;
(iii) confirm from the code whether any deployed path can produce `completeness_score < 65` on a row
that also clears 82; (iv) a pure-function unit test over `_confidence_label` asserting the tier
boundaries, plus `git show --stat` proving no other scorer file changed. **The before/after
distribution is the Data Steward's**, on the pinned parquet (`manifest_v001`) and the successor
freeze (DP-50(c)); the brief names that parquet as the before-snapshot and asks no one to capture one.

**DP-50(b) ship timing — named, decision left to Haci.** Changing `_confidence_label`'s constants, or
any enrichment flag, weight or timeframe multiplier, moves `completeness_score` and the label
together and makes the label **two different features at the ship date** (DP-06 / DP-50(a)).
In-flight questions that read the label or the score: **Q023** (`confidence_level` as a column),
**Q024**, **Q027** and **Q031** (the `overall_score` blend and its published slate; Q027 and Q031
share Q029's **2027-05-24** hard stop), **Q029** (a closed EVALUABLE / DEAD / UNEVALUABLE register
that a mid-window ship would force it to re-derive), and **Q032 / Q033 / Q034**, whose descriptive
`confidence_level` terciles would change definition mid-window. **Q036 itself asserts no
constraint** — it is deferred, and a change to these settings is precisely what could make it
testable again. The trade-off is stated; the decision is Haci's under DP-48, and the desk files
nothing further until `/desk-run prompt PI-016`.

**Recommend: fix — or accept, and stop calling it conviction.** Two honest options, and the desk
takes no third. **`fix`** = re-derive the `:1167-1170` constants against the observed completeness
distribution so the tiers separate something, **or** rename the field to the coverage measure it
actually is and let the card say what it means. **`accept`** = leave the computation alone and stop
describing the output as conviction on subscriber-facing surfaces, since on the running
configuration it carries no information the printed score does not already carry. Either way, any
change to how the slate is *scored or ordered* still needs a research question and a full brief
(rule 11) — and the question of whether the label predicts anything remains **Q036, DEFERRED**.

### PI-017 — a forced UOA re-run for one symbol deletes every symbol's rows for that date

**Found 2026-09-14** by the Registrar while triaging H-021; confirmed by the coordinator in the code
and in the database (read-only, counts only).

**The code.** `services/uoa_screener.py:1282-1287` — when `force` is set, the screener deletes rows
filtered on **`trading_date` only**, from three tables, before recomputing:

```python
if force:
    # Clear existing rows for that date to avoid duplication.
    db.query(UoaContractDaily).filter(UoaContractDaily.trading_date == trade_date).delete(...)
    db.query(UoaSymbolDaily).filter(UoaSymbolDaily.trading_date == trade_date).delete(...)
    db.query(UoaBulletin).filter(UoaBulletin.trading_date == trade_date).delete(...)
```

It then recomputes only `_resolve_universe(db, cfg, universe)` (`:1289`). The range runner in the
platform's `scripts/` directory (`run_uoa_range`) makes `--symbol` **required** (`:34`), passes
`universe=[sym]` (`:79`), and offers `--force` as "Recompute and overwrite rows for each date"
(`:43`). So the documented way to repair one symbol's UOA history deletes every other symbol's
contracts and symbol rows, and the night's bulletin, for each date in the range — and restores one.

**Why it matters beyond UOA.** `uoa_bulletins` feed the SAS candidate universe
(`services/candidate_universe_builder.py`), and `uoa_symbol_daily` carries the flow features and the
`fwd_return_*` columns PI-001 is about. One mistaken repair silently shrinks a night's candidate pool
and flow layer, and the run is still recorded `status = success`.

**Evidence of the signature in history — an inference, not proof.** Counts only:
- The only trading date with fewer than 200 `uoa_symbol_daily` rows is **2026-01-09: 23 rows, 23
  symbols**, between 2026-01-08 (498) and 2026-01-12 (499).
- Its `uoa_runs` row (id 5, `nightly`) carries `config_json = {"force": true}` and
  `symbols_considered = 23`; it started 2026-01-12 19:09:46 UTC and **finished 22 seconds later with
  `status = success`**. Neighbouring nightlies consider 503 symbols and take about six minutes.
- Whether that date held ~499 rows before the forced run cannot be established from current rows.

2026-01-09 is before every registered study window (the frozen candidate history starts 2026-04-01),
so **no locked question is affected**. The hazard is forward-looking: the next single-symbol repair.

**Expected behaviour.** A forced re-run replaces exactly what it recomputes: contract and symbol rows
deleted on `trading_date` **and** `symbol IN (<resolved universe>)`; the bulletin rebuilt from the
full date's symbol rows, not the partial universe. Or: refuse `--force` when the universe is narrower
than what is stored for the date.

**Reproducing check (Data Steward, read-only).** Per trading date, `count(DISTINCT symbol)` in
`uoa_symbol_daily` beside `uoa_runs.config_json->>'force'` and `stats_json->>'symbols_considered'`;
flag any date where a forced run considered fewer symbols than its neighbours.

**Suggested route.** Plain bug fix that restores intended behaviour → `fix-brief` once Haci decides
`fix`. Under DP-49 the brief changes the delete predicate only; it never hands the coding agent a
database step, and it does not repair 2026-01-09.

### PI-018 — the technical report's BUY/SELL call can contradict its own technicals

**Found 2026-09-14** while filing Haci's F9 idea, from the SNDK report he pasted (ai_job `7e78c055…`,
2026-09-11 10:01:49) and a read of the decision code. Read-only; no database or blob was touched.

**What the sample shows.** On the 15m timeframe the indicator layer says `overall_bias: "bearish"`,
`strength: 71.43`, `confidence: "medium"`. The printed decision for the same timeframe is
**`recommendation: "BUY"`**, with the reasoning "Near Fibonacci support at $1624.55". The 4h call is
also BUY for the same reason, on a bullish bias of only 65%. The consensus reads BUY 2 / SELL 2 /
HOLD 2 — six calls for seven timeframes.

**The code that produces it** — `day_trading_agent.py`, thresholds at `:591-593` (`buy_threshold = 70`,
`sell_threshold = 70`, `high_confidence_only = True`):

1. **A strong medium-confidence signal is silently dropped (`:749-771`).** A bearish bias with strength
   ≥ 70 enters the SELL branch, but `if not self.high_confidence_only or confidence == 'high'` fails for
   "medium". Nothing is recorded: not SELL, and — because the `else` that counts a HOLD is never reached
   — not a counted HOLD either. The recommendation stays at its default HOLD.
2. **A nearby Fibonacci level then decides the call (`:776-804`).** Any HOLD with price within 2% of the
   nearest support becomes BUY. The 71% bearish 15m signal becomes a BUY this way.
3. **Ties go to BUY.** Support is tested before resistance, and only a still-HOLD call can flip. On short
   timeframes the Fibonacci grid is tight — the sample's 15m support and resistance sit 0.5% below and
   0.4% above price, both inside the 2% band — so the call becomes BUY and never SELL.
4. **The tally is wrong.** Step 2 runs `hold_count -= 1` for a HOLD that step 1 never counted. Replaying
   the sample through the code gives exactly the printed 2 / 2 / 2: 15m −1, 4h +1−1, 1d/1wk/1mo +3.
   `overall_recommendation` uses `buy_pct` / `sell_pct` over all timeframes, so the headline is not
   changed by this, but the distribution shown to users is.

**Why it matters.** A subscriber reading "BUY, near Fibonacci support" on a timeframe whose technicals are
71% bearish is being given the opposite of the analysis. It also means any research on these reports
must treat the raw indicator bias and the printed call as different variables (BACKLOG F9 preamble).

**Expected behaviour — Haci's call, because part of it is design, not bug:**
- *Bug:* a signal that passes strength but fails the confidence gate must land somewhere explicit (a
  counted HOLD with its reason), and the tally must never decrement what it did not count.
- *Design:* whether proximity to a Fibonacci level may override the indicator bias at all, and if so
  whether it may override an *opposing* strong bias, and how a price inside both bands is resolved
  (today: always BUY).

**Suggested route.** Split it: the counting fix is a plain bug fix (`fix-brief`); the override rule is a
behaviour change to what subscribers are told and should go through research first — H-086/H-089 can
measure whether Fibonacci-flipped calls behave like signal-driven ones before anyone changes the rule.

**At scale (Data Steward blob inventory, 2026-09-14, `research/reports/STEWARD_F9_blob_inventory.md` §8).**
Over all 697 history reports: **495 of 3,933 (12.6%)** BUY/SELL decisions oppose their own timeframe's
`overall_bias` (378 BUY on bearish, 117 SELL on bullish); **"Near Fibonacci" appears in the reasoning of
2,992 of 3,933 (76.1%)**; the consensus tally does not equal the number of timeframes on **349 of 697
reports (50.1%)**. PI-018 is systematic, not a sample artefact.

### PI-019 — report timestamps changed zone silently; report trigger not recorded

**Found 2026-09-14** by the Data Steward's F9 blob inventory (`research/reports/STEWARD_F9_blob_inventory.md`
§3, §6), counts and metadata only.

- **Zone switch.** The report `timestamp` (and every `price_timestamp`, which equals it) carries no zone.
  Against the UTC `stored_at`, reports from 2026-01-22 to 2026-04-05 (201) differ by ≈ 0 minutes — UTC —
  and reports from 2026-04-07 (494) by 240–241 minutes — US Eastern (EDT). 2026-04-06 carries both. No
  `day_trading_agent.py` commit in that window explains it; the cause is platform-side and unlocated.
- **No provenance.** Reports come from `POST /analyze` (`app.py:3286-3287`, the subscriber's `user_id`) or
  `POST /api/internal/batch-analyze` (`app.py:3696-3700`, which hard-codes `user_id = 1` at `app.py:3966`).
  Neither the blob name nor the payload says which. `user_id = 1` is 513 of 697 reports (73.6%).
- **Legacy shape.** 28 reports without `strategy_scope` carry `5m` instead of `15m`.

**Why it matters.** Any display, alert or analysis that reads report times across April 2026 is off by four
hours for part of the history, and any usage or popularity metric built on reports counts an internal job
as subscriber demand three times out of four.

**Expected behaviour.** Timestamps written as ISO-8601 with an explicit offset (or UTC with `Z`); a
`trigger` field (`subscriber` / `internal_batch` / other) on every report. Plain bug fix + additive field;
no historical rewrite needed — the desk can normalise history by date (DP-49: no database or blob step in
the brief).


### PI-020 — UOA option trades truncated at one page; puts dropped on liquid names

**Found 2026-09-15** while tracing why SNDK's three rank-1 picks (09-08, 09-10, 09-11) failed
(`research/reports/case_SNDK_2026-09-15/REPORT.md`). Read-only queries and Alpaca market data only.

**Mechanism, read from code.**
- `services/uoa_screener.py:1505-1510` calls `options_client.get_option_trades(contract_symbols, start, end,
  limit=cfg.trades_limit)` for the up-to-60 selected contracts; `trades_limit = 1000` (`:806`).
- `ai_agents/options_client.py:1007-1017` splits the list into batches of 50 (`_SNAPSHOT_BATCH`, `:17`),
  sends one `/trades` request per batch with `limit=1000`, and **never reads `next_page_token`** (the chain
  and snapshot fetches in the same file do paginate, `:584`, `:914`).
- Alpaca's multi-symbol trades response is ordered by contract symbol. `…C…` sorts before `…P…`, so when a
  batch holds more than 1,000 trades the page fills with calls and the puts return empty.
- `:1522-1535` then stores a zero-trade row for every contract without trades, and `:1601-1605` builds
  `dir_ratio` from the truncated call and put totals.

**Reproduction (`verify_trades.py` in the case folder).** SNDK 2026-09-08: `uoa_contract_daily` holds 60
contracts, 2,000 trades in total, trades on 10 calls and 0 puts. The platform's request shape returns 1,000
trades over 8 call contracts with a `next_page_token`. Paginated, the first 50 contracts hold 14,441 call
trades ($200.7M) and 11,154 put trades ($82.5M). Stored `dir_ratio`: 1.00.

**Scale (`truncation_scale.py`; a symbol-day is "capped" when its stored trades reach 1,000, a floor).**

| month | symbol-days | capped | capped with zero put premium |
|---|---:|---:|---:|
| 2026-01 | 7,992 | 1,311 | 164 |
| 2026-04 | 10,499 | 1,741 | 165 |
| 2026-07 | 10,927 | 1,601 | 194 |
| 2026-08 | 10,461 | 1,483 | 164 |

Every month from January to September is in the same range. Since 2026-06-01, 317 of 604 published SAS picks
had a capped UOA row on their pick night (64 with zero put premium). The most liquid names are capped every
session (GOOG, GOOGL, MSFT, AMZN, NFLX, ORCL, CRM, NOW, KO, WMT, BAC, BA, PFE, GLW, SNDK).

**Why it matters.**
- The flow layer (weight 24) and two direction votes read a premium mix biased toward calls on exactly the
  names with the most options activity. Scores, the cross-layer agreement bonus and "bullish flow" labels
  are inflated for them; bearish flow on liquid names is systematically under-seen.
- **Desk data.** Frozen `uoa_symbol` in `manifest_v001` carries the defect for its whole range. Questions
  that read flow — Q014 (UOA persistence), Q029's flow layer, H-092 (flow label vs premium mix) — measure the
  platform *as it behaved*, which is legitimate for a "does the published score work" question but not for
  "does options flow carry information". No locked question is edited; the Red Team is told at review.
- **Possibly related, unverified:** `gex_symbol_daily.quality_json` shows 39–50 of 2,000 contracts used and
  `flip_quality = missing_iv` for SNDK; 755 of 1,972 GEX rows since 2026-08-01 have no put wall; SNDK reads
  POS_GAMMA every night. The steward should check whether GEX shares a truncation before any GEX finding
  (Q021, Q029, H-091) is trusted.

**Expected behaviour.** Follow `next_page_token` until exhausted (or request per contract) with a sane
per-symbol ceiling that is *recorded* when hit (`trades_truncated` flag and count), so no side is silently
dropped. Plain bug fix, restores intended behaviour. Historical rows are not rewritten by the fix; if Haci
later backfills, the repair is logged in `research/data/DATA_NOTES.md` with its range and ship SHA and any
question spanning it splits at that date (DP-50). DP-49: no database step in the brief.

### PI-021 — platform test fixtures delete all users in whatever database the tests connect to

**Found 2026-09-15** by the Brief Writer while writing the EN-019 brief; lines re-read by the coordinator at
platform `c311e81`.

- `conftest.py:9-21` requires a Postgres connection URL and rejects only SQLite; nothing refuses a
  production host.
- `conftest.py:31-35`: session-scoped autouse fixture runs `create_tables()` (DDL).
- `conftest.py:38-55`: autouse fixture deletes **all** rows of `UserActivityEvent` and `User` before and
  after every test, and commits.
- **Exposure.** `research/briefs/PI-017_forced_uoa_rerun_delete_scope.md` §4(c) (lines 516-525) instructed
  `python -m pytest tests/ -q` on the base commit and after. PI-017 merged as `575df11`. If the coding
  agent's connection URL was the production read-write one (DP-49 says the coding agent's credential is),
  both tables were emptied — twice. **The desk has not verified this**: the research connection was not set
  in the coordinator's shell on 2026-09-15, and the desk does not go looking for credentials (rule 1).

**Expected behaviour.** Tests refuse to run unless the connection names a disposable test database (a
required dedicated test URL, or a hard stop when the host or database name matches production), and cleanup
deletes only rows the tests created. Plain bug fix. **Desk rule until PI-021 is fixed:** no brief tells a
coding agent to run `pytest` in the platform repo (the EN-019 brief already forbids it and uses a standalone
runner).

### PI-023 — the option buy/sell label is judged against the closing quote and follows the day's drift

**Found 2026-09-15** from Haci's question about Omega's option-trades tool (it cannot tell a buy from a sell;
platform `d112d37`). Read-only queries and Alpaca market data only. Full report and the enhancement that fixes
it: `research/reports/uoa_side_2026-09-15/REPORT.md` (EN-020).

**Mechanism, read from code.**
- `services/uoa_screener.py:1114-1116`: the bid/ask kept for a selected contract is the `latestQuote` of the
  snapshot taken when the nightly runs (16:43–17:04 ET in September, `uoa_runs.started_at`), i.e. the closing
  quote.
- `:1246-1256` (`_aggregate_trades_for_contract`): every print of the 09:30–16:00 session is compared with
  that one quote: `≥ ask − 0.1·spread` → `buy_premium`, `≤ bid + 0.1·spread` → `sell_premium`, else
  `unknown_premium`. The MVP spec called this a proxy and asked that counts be stored "so you can replace it
  later" (`docs/UOA_SCREENER_MVP.md` §4.3).
- `:1663-1668`: `dir_ratio` is built from the two buy totals. `symbol_context_builder.py:136-205` hands the
  four-way split to SAS; `super_agent_select_scoring.py:555-560` votes direction from `dir_ratio` when
  polarity is off (it is, PI-014). `whale_watch_tracking.py:114-116` and `routers/whale_watch.py:153-159`
  qualify contracts on the same split. `routers/uoa_screener.py:465-474` shows `buy/total` as conviction.

**Evidence (`drift_test.py`, 170 sessions 2026-01-07..2026-09-14).** Buy-share = buy / (buy + sell) over all
of a day's classified premium, by side, against SPY's open-to-close move (Alpaca daily bars):

| SPY tercile | call buy-share | put buy-share |
|---|---:|---:|
| down day | 0.624 | 0.412 |
| flat | 0.542 | 0.498 |
| up day | 0.429 | 0.598 |

Spearman −0.566 (calls) / +0.533 (puts). On an up day the call's closing quote sits above most of the day's
prints, so they read as sold; the put's sits below, so they read as bought. 23–35% of premium is already
`unknown` under the rule.

**Placebo that rules out trader behaviour (Red Team, `ttc_test.py` / `ttc_test2.py`, 73 sessions
2026-06-01..09-14, the 10 largest prints per contract, 457,135 prints).** If the label were real, its tape
correlation would not depend on how many minutes remained in the session; if it is the closing-quote
artefact it must vanish near the close, where the closing quote is the quote at trade time:

| minutes to close | call ρ | put ρ |
|---|---:|---:|
| < 10 | +0.03 | +0.10 |
| 10–30 | −0.01 | −0.13 |
| 1–3 h | −0.24 | +0.18 |
| > 3 h | −0.55 | +0.47 |

Same contract-days, both legs present (114,619 prints): early (> 3 h) −0.58 / +0.46; late (< 30 min)
−0.03 / −0.02. The < 10-minute row is also the residual bias a 10-minute sampler would carry.

**Why it matters.** The flow direction vote in SAS carries tape-correlated noise on the very variable rule 7
calls dominant; Whale Watch admits contracts by afternoon drift; the UI's conviction number is not what it
says. For the desk: `manifest_v001`'s `uoa_symbol` / `uoa_contract` carry the artefact throughout; Q014, Q029
and Q030 measure the platform as it behaved (still legitimate); **H-092 must not be registered** until a
forward window with quote-at-trade labels exists.

**Expected behaviour.** Each print is labelled against the quote prevailing when it traded. Alpaca offers no
historical option quotes, so the quote must be sampled during the session: EN-020 (every 10 minutes: chain
snapshot → contracts that traded → bracketing quotes stored → prints fetched with a lag and classified against
the brackets → 10-minute buckets; the nightly sums the buckets and marks uncovered premium **unknown** —
no closing-quote fallback — and `dir_ratio` is NULL when a symbol's classified share is below 0.50, so the
SAS legacy vote abstains instead of re-reading the artefact). Historical rows are not rewritten; the ship date is logged in `DATA_NOTES.md` and locked questions split there
(DP-50). A delta-adjusted backfill of history is Phase 2, only after the sampler provides a truth set.
