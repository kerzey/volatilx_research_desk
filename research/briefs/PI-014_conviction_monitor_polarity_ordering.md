# PI-014: run the Conviction Monitor inside the nightly pipeline, after UOA has written the day's flow

**Type:** fix brief (a platform issue, not a research finding)
**Register row:** `research/PLATFORM_ISSUES.md` PI-014, severity high, `HACI_DECIDED:fix`
**Written:** 2026-09-15 by the Brief Writer. Haci asked with `/desk-run prompt PI-014`, and under DP-48 asking is the decision.
**Diagnosis it rests on:** `research/reports/STEWARD_PI-014_diagnosis.md` (research commit `d99aa4f`)
**Platform repo:** `C:\Users\sahin\Projects\volatilx`
**Platform SHA for every `path:line` citation:** `d9c052ab27651340ca0b844eec2a943e05085aea`
(`d9c052a`, "EN-019: archive always on, batch keeps only a kill switch", 2026-09-15). The working tree was clean at that SHA.
**Research repo SHA:** `d99aa4f`

**DP-59 governs this brief (Haci, 2026-09-15).** It adds no feature flag, no shadow mode, no flag-off/flag-on test pair,
no byte-identical inertness proof and no flip step. DP-59 also overrides the charter clause that would send a
number-changing fix back to Haci as `research`. The fix ships directly. Its parts are the change (§3), one standalone test
(§5), the Data Steward's read-only check after deploy (§8), and `git revert` as rollback (§6). A flag is also unnecessary
on the merits, because the change restores intended behaviour:
- `scripts/run_conviction_monitor.py:4-5` describes the monitor as "post-SAS nightly".
- `services/conviction_monitor_service.py:6-7` says polarity is computed "from today's `uoa_contract_daily` rows".
- Nobody chose to read that table before it was written.

**Published numbers that change from the ship date (named, as DP-59 requires).** From the first trading date whose nightly
runs the fix (called `D0` below), the Elite Conviction Monitor panel (`routers/conviction_monitor.py:171-200`) and the
`conviction_monitor_daily` rows behind it change as follows:
- **Polarity columns:** `polarity_today`, `polarity_coverage_today` and `polarity_tier` are computed from real flow.
- **Tiers:** `overall_tier` and `age_adjusted_severity` change, and with them the panel's exit/watch/hold counts and sort order. HOLD becomes reachable again (§3.0, point 7).
- **`reason_codes_json` and `notes`:** a symbol with no flow rows now carries `polarity_unavailable_inputs_missing` and its own sentence.
- **`polarity_details_json`:** premiums are populated, and `fallback_reason` takes the new value `no_flow_rows`.
- **`created_at` / `updated_at`:** rows are stamped the same evening after the SAS run finishes, no longer at about 16:02 ET.
- **Holidays and re-runs:** no rows are written on NYSE holidays, or when the pipeline is re-run for an earlier date.
- **Technical arm:** its tiers may move slightly, because its bars are fetched later the same evening.

No historical row is rewritten. SAS scoring, selection, publication time, UOA, and every other table are untouched.

**Ship-timing check (DP-50(b)), done before writing.** The Registrar sweeps the questions below on `D0`. The desk
writes the DATA_NOTES entry (§8, Step 3).
- **Q019** `conviction_monitor_exit` (state `DATASET_PINNED`, decision **2027-05-24**) tests the monitor's EXIT tier. Its
  DECISIONS #10 restricts the claim to the technical arm, because polarity was dead. This ship is exactly the dated
  "restoration of a structurally-unavailable input" that **DECISIONS #12(a) and Correction 11** anticipate. It is a
  **restart, not a split** (#3: "no split, no second pair of primaries"):
  - The window start moves to the first pick night after the ship.
  - The Registrar recomputes §5 at the measured rate. Dates can only move out. Q019 goes to `DEFERRED.md` only if the recomputed decision date lands after **2027-09-13**.
  - PI-014's own arithmetic puts a ship before about **2027-03-08** as survivable, so a September–October 2026 ship is well inside that.
  - The Registrar should note two things. First, `r = 0.6885` was measured while every EXIT came from the technical arm alone, and polarity-fired EXITs and reachable HOLD rows change which picks flag. The rate should therefore be re-measured on post-`D0` nights before it sets any date. Second, pick night `D0 − 1` is the first whose five in-scope rows are all post-fix, while #12(a) as written starts at the first pick night *after* the ship. The later of the two is the conservative reading.
- **Q038** `monitor_tier_calibration` (state `DEFERRED`, 2026-09-15) has no dates to move. Everything its record pass measured describes the pre-`D0` feature:
  - the terminal-state split;
  - B3's 4 of 53;
  - decision 1's "HOLD unreachable → bijection" argument;
  - the structural suppression of the polarity cell.

  **Re-entry by either route is therefore a restart at `D0`.** Route 1's trailing-quarter re-measurement must use only
  post-`D0` nights. Route 2's precomputed schedule (window from 2026-06-01, decision 2027-05-24) spans `D0` and cannot be
  used as written. The Registrar adds that sentence to Q038's `DEFERRED.md` entry.
- **Q026** `point_in_time_integrity` reads `conviction_monitor` from `manifest_v001` only, as a census of rows dated on or before 2026-09-10, so it is unaffected. **Q008** mentions the monitor's 16:02 clock in its §9 prose only. It still runs after the close on the same evening, and no data read changes. No other PREREG or DECISIONS file reads this table.
- **Onset date correction.** The PI-014 register row says "since 2026-06-01". The diagnosis dates the failure to **2026-05-19**, the monitor's first live scheduled run, and the pinned freeze agrees (§1). The June boundary came from month-level aggregation: May mixed four backfilled dates, which worked, with 15 live ones, which did not.
- **Knowledge time.** `research/lib/freeze_config.json` declares `conviction_monitor.available_time_et = "16:02"`, `lag_sessions: 1`. From `D0` the row appears the same evening after `sas_ladder_nightly`, still well before the next open, so `lag_sessions: 1` and Q019's §2 point-in-time guard still hold. The DATA_NOTES entry records the new time.
- **PI-020** (trade pagination, `BRIEF_WRITTEN`, not implemented at `d9c052a`: no `get_option_trades_paged` in the repo) is a different defect (diagnosis §3). If its pagination is later switched on, it changes the buy/sell decomposition for capped names, and with it polarity values for those symbols. That takes its own DATA_NOTES date.

You are the coding agent in the platform repo. This brief is self-contained: do not ask questions, do not redesign, and do not
widen the scope. Implement §3, run §4, add §5, and report the SHA.

**Nothing in this brief runs against a database.** Under DP-49 you get no DB step at all, because your `DATABASE_URL` is the
platform's read-write role on live production. Two specific prohibitions:
- **Do not run `pytest` in this repo** (research PI-021). `conftest.py` runs `create_tables()` and deletes every `User`
  row around each test, in whatever database `DATABASE_URL` names. Run the §5 test as
  `python tests/test_conviction_monitor_ordering.py` with `DATABASE_URL` unset; it loads no conftest.
- **Do not run `scripts/run_nightly_pipeline.py`, `scripts/run_conviction_monitor.py`, any other `scripts/run_*.py`, or the
  app.** The monitor's first action is a `DELETE` of the date's rows (`services/conviction_monitor_service.py:1097-1101`).

**Whose step is whose.** The coding agent's work ends at §4 and §5, which need only the repo. **Haci** merges, deploys,
confirms in Kudu that the `conviction_monitor` WebJob is gone, and records the SHA and `D0`. The **Data Steward** runs §8
on the read-only role. The **desk** writes the DATA_NOTES entry and the Registrar sweep on `D0`. There is no data repair step.

**Indentation:** `services/conviction_monitor_service.py` uses **tabs**, and its snippets below are shown with tabs; keep them.
`scripts/run_nightly_pipeline.py`, `scripts/run_conviction_monitor.py` and `tests/` use 4 spaces.

---

## 1. Symptom: what is wrong, and the evidence

The Conviction Monitor's polarity arm has not read one options-flow row on any live run since it shipped. Every row
since **2026-05-19** has `polarity_tier = WATCH` and carries `polarity_unavailable_coverage_low`. Because
`overall_tier = worst(polarity, technical)` (`services/conviction_monitor_service.py:1223`, `:792-804`), the panel
cannot print HOLD. The input is not actually thin: the Steward measured settled symbol-day coverage at a median of
0.70–0.89 in every month from April to September, never below the 0.5 gate on any sampled date (diagnosis §1a–§1d).
The monitor reads the table about 50–60 minutes before that day's rows exist (diagnosis §1f).

**Before-state, from the pinned freeze (DP-50(c); no live query).** `research/data/v001_conviction_monitor.parquet`
(`manifest_v001`, 3,339 rows, trading dates 2026-05-12..2026-09-10, sha256
`687527943e8b887254d1bdd54e937c8eb2ac071156c1a63bf5690779e77e9c7c`), counted by the Brief Writer on 2026-09-15:

| rows | dates | carry `polarity_unavailable_coverage_low` | `polarity_details.contract_premium_total` null | `polarity_tier` | `overall_tier` | `technical_overall_tier` |
|---|---:|---:|---:|---|---|---|
| live runs, 2026-05-19..2026-09-10: **3,179** | 82 | **3,179** | **3,179** | WATCH 3,179 | WATCH 2,060 · EXIT 1,119 · **HOLD 0** | HOLD 624 · WATCH 1,427 · EXIT 1,119 · UNKNOWN 9 |
| backfilled 2026-05-12..05-15 (written 2026-05-16): **160** | 4 | 107 | **0** | HOLD 53 · WATCH 72 · EXIT 35 | HOLD 18 · WATCH 69 · EXIT 73 | — |

- The **null `contract_premium_total` on 3,179 of 3,179 live rows** is the signature of absent rows, not thin ones.
  `prefetch_flow_polarity` creates an entry, with a float `contract_premium_total`, for every symbol that has at least one
  contract row (`services/symbol_context_builder.py:176-197`). The row stores `aggregate.get("contract_premium_total")`
  (`services/conviction_monitor_service.py:1259`). A null therefore means the query returned nothing for that symbol.
  On the four backfilled dates, which were read after contracts existed, it is null on 0 of 160 rows.
- `created_at` is **16:02 ET on every one of the 3,179 live rows**. `created_at` is `server_default=func.now()`
  (`models.py:68`), which is the start of the insert transaction. That transaction begins right after the delete commit at
  `services/conviction_monitor_service.py:1101`, so the timestamp marks the moment the monitor loaded its inputs.
- **624 live rows had a technical arm of HOLD and printed WATCH** only because the polarity arm was stuck at WATCH.
- 167 rows are dated on NYSE holidays (2026-05-25, 06-19, 07-03, 09-07), because the monitor's cron checks weekdays only.

### Reproducing query (**Data Steward only**, read-only role on `$RESEARCH_DB_URL`)

Not for the coding agent (DP-49). Counts and timestamps only.

```sql
-- R1. Every live run read its inputs before that day's UOA run had finished.
WITH cm AS (
  SELECT trading_date, count(*) AS rows, min(created_at) AS cm_first,
         sum(CASE WHEN reason_codes_json LIKE '%"polarity_unavailable_coverage_low"%' THEN 1 ELSE 0 END) AS coverage_low,
         sum(CASE WHEN (polarity_details_json::jsonb)->>'contract_premium_total' IS NULL THEN 1 ELSE 0 END) AS no_aggregate
  FROM conviction_monitor_daily
  WHERE trading_date >= DATE '2026-05-19'
  GROUP BY 1)
SELECT cm.trading_date, cm.rows, cm.coverage_low, cm.no_aggregate,
       cm.cm_first AT TIME ZONE 'America/New_York'  AS cm_first_et,
       u.finished_at AT TIME ZONE 'America/New_York' AS uoa_finished_et,
       cm.cm_first < u.finished_at                   AS monitor_read_first
FROM cm LEFT JOIN uoa_runs u ON u.trading_date = cm.trading_date AND u.run_type = 'nightly'
ORDER BY 1;
-- Expected today, on every non-holiday date: coverage_low = rows = no_aggregate, cm_first_et about 16:02, monitor_read_first = true.
-- (A later forced UOA re-run moves uoa_runs.finished_at. Diagnosis §1f used uoa_contract_daily.created_at for that reason.)
```

---

## 2. Cause

Two WebJobs are scheduled independently, and the consumer fires first.

- `app_data/jobs/triggered/conviction_monitor/settings.job:2` schedules the monitor at `"0 02 16 * * 1-5"`, i.e. 16:02 ET, weekdays.
  Its `run.py:83-92` shells out to `scripts/run_conviction_monitor.py`. That script takes the trading date from the ET clock
  (`:38-41`) and skips weekends only (`:60`), which is why holidays get rows.
- `app_data/jobs/triggered/nightly_pipeline/settings.job:2` starts the pipeline at `"0 05 16 * * 1-5"`, i.e. 16:05 ET.
  Step order: `market_regime` (`scripts/run_nightly_pipeline.py:264-268`), `projection_picks` (`:270-271`), `uoa_oi_gex`
  (`:272-273`), `super_agent_select` (`:274-275`), `sas_ladder_nightly` (`:276-277`), `backfill_outcomes` (`:278-279`), and so on.
  `uoa_oi_gex` runs the UOA nightly (`scripts/run_uoa_oi_gex_for_day.py:158-161`), which writes the date's
  `uoa_contract_daily` and `uoa_symbol_daily` rows. It marks `uoa_runs.status = success` / `finished_at` only at the end
  (`services/uoa_screener.py:2004-2007`). Measured: its contract rows land at 16:49–17:04 ET (diagnosis §1f).
- At 16:02 the monitor calls `prefetch_flow_polarity(db, symbols=..., trading_date=trading_date)`
  (`services/conviction_monitor_service.py:1113-1120`), which filters `trading_date == trading_date` exactly
  (`services/symbol_context_builder.py:168-171`) and returns `{}`. The same-day `dollar_volume_20d` lookup
  (`services/conviction_monitor_service.py:1122`, `:856-888`) returns `{}` as well.
- For each pick, `aggregate = polarity_aggregates.get(symbol) or {}` (`:1178`) yields all-zero inputs
  (`:891-903`). Because the contract total is 0, `coverage_ratio` stays `None` (`:928-929`), and the decomposition total of 0
  returns `fallback_reason = "no_decomp"` (`:931-933`). The gate `polarity is None or coverage is None or coverage < threshold`
  then returns `("WATCH", ["polarity_unavailable_coverage_low"])` (`:184-185`). The label says coverage was low, but no
  input had been read.
- With `polarity_tier` stuck at WATCH, `_worst_tier` (`:792-804`) floors `overall_tier` at WATCH (`:1223`).

The monitor never re-reads later that evening. The gate itself is correct: fed real rows, it behaves as designed (diagnosis §1).

---

## 3. Change

### 3.0 Design choices, justified from the code

1. **The monitor becomes a pipeline step, and its separate cron is removed.** The dependency ("after `uoa_oi_gex` has
   written the date") is then made explicit by step order, not approximated by a time gap. Two alternatives were rejected:
   - **Rescheduling the cron** (say to 18:00) is a bigger gap, not a dependency. The UOA write already drifted from 49
     to 62 minutes after 16:02 within four weeks (diagnosis §1f). SAS runs finished as late as 17:46 ET (EN-019 §0.2 point 5, from
     `v001_sas_runs.parquet`). A slow or failed pipeline night would quietly bring PI-014 back. The cron would also keep
     resolving its own trading date, ignoring holidays (`scripts/run_conviction_monitor.py:38-41`, `:60`).
   - **A readiness check** (poll `uoa_runs` until `success`) is explicit but worse in three ways:
     - It would wake exactly when UOA finishes, which is when SAS starts (`scripts/run_nightly_pipeline.py:272-275`). The
       monitor's technical arm would then fetch Alpaca bars concurrently with the publication path, and
       `indicator_fetcher.py` has no 429 or retry handling (0 matches for `429|Retry-After|rate limit`).
     - A forced UOA re-run resets the run row to `running` (`services/uoa_screener.py:1375-1379`) and then deletes the
       date's rows (`:1382-1385`). A poller can read in that window.
     - It needs its own timeout policy inside a triggered WebJob.

   A pipeline step instead inherits the pipeline's holiday-aware trading date (`core/market_sessions.py:97-98`), its
   `is_singleton` (`app_data/jobs/triggered/nightly_pipeline/settings.job:3`), and its failure email.
2. **Placement: after `sas_ladder_nightly`, before `backfill_outcomes`.** This placement moves nothing on the publication path.
   `super_agent_select_runs.finished_at`, the actionable time (`research/data/DATA_NOTES.md:156-165`), is unchanged, and
   the monitor fetches no bars while SAS runs. It depends on nothing SAS produces that night: it loads only picks with
   `trading_date < today` (`services/conviction_monitor_service.py:1043-1050`), and their qualifying-day blobs are prior
   nights' (`:960-991`). It runs after the UOA step, so the date's `uoa_contract_daily` and `uoa_symbol_daily` rows exist.
   Subscribers see the day's rows after SAS finishes plus the monitor's runtime, not at about 16:03. Until then
   `/latest` serves the previous date (`routers/conviction_monitor.py:92-98`).
3. **Non-fatal, and still attempted when a fatal step fails.** A monitor failure is printed and recorded in the digest; it
   never fails the pipeline (the `outcome_coverage_check` pattern, `scripts/run_nightly_pipeline.py:293-297`). Tonight's picks
   are not the monitor's input; the previous five nights' picks are. So the pipeline's `except` block also runs the step if it
   has not run yet (for example after a SAS failure). If the UOA step itself failed, rows are still written with honest
   labels (point 6) and the technical arm is kept.
4. **Same-evening guard.** The technical arm has no as-of date. `_fetch_today_price_action` and
   `_fetch_today_technical_snapshot` (`services/conviction_monitor_service.py:998-1022`) fetch bars through today
   (`indicator_fetcher.py:2858-2867`). A pipeline re-run for an earlier date (for example `--trading-date`) must not
   overwrite that date's rows with later bars. The step is therefore skipped, with the reason printed and recorded, whenever
   the pipeline's `trading_date` differs from its ET calendar date. On the scheduled path the two are always equal
   (`core/market_sessions.py:97-98`).
5. **The WebJob folder is deleted** (`app_data/jobs/triggered/conviction_monitor/`). App Service can keep running a stale
   wrapper after a deploy (`docs/AZURE_WEBJOBS_AUTOMATION.md:60-66`), so Haci confirms in Kudu that the job is gone (§8
   Step 1). If one lingered, it would write rows at 16:02 that the pipeline step later replaces. The replacement is harmless
   but leaves a window of stale rows. §8 V4 would show that window as a 16:02 `created_at` on any date the step did not reach.
6. **Honest label; gate unchanged.** When `prefetch_flow_polarity` returns no entry for a symbol, whether because the whole
   date is missing or because that symbol has no contract rows, the row gets `polarity_unavailable_inputs_missing` with
   `fallback_reason = "no_flow_rows"`:
   - The tier stays WATCH, as before.
   - `_polarity_tier_for_direction` (`:172-196`), `_compute_polarity_for_monitor` (`:906-953`) and the thresholds (`:72-77`) are not edited.
   - The code keeps the `polarity_unavailable` prefix that `_summarize_notes` (`:1060`) keys on, and gets its own sentence.
   - A run in which no monitored symbol has flow rows logs a WARNING, and every run adds three counts to its logged stats (`:1083`).
   - The panel shows `fallback_reason` to the subscriber (`templates/ai_picks.html:4025-4028`), so the reason printed there becomes true too.
7. **HOLD becomes reachable again.** `overall_tier = worst(polarity_tier, technical_overall_tier)` (`:1223`, `:792-804`).
   With polarity live, the expected mix changes only in these directions:
   - `overall_tier` HOLD appears where both arms say HOLD. In the freeze, 624 live rows had a technical arm of HOLD.
   - `overall_tier` EXIT can only rise for the same technical reads, because a polarity EXIT adds EXITs.
   - WATCH shrinks from both sides.
   - Symbols whose inputs are thin or missing stay WATCH.
   - The only freeze evidence of the working arm is the four backfilled dates, where polarity was available on most rows and HOLD, WATCH and EXIT all occurred.

   The megacap premium floor also starts to apply. Same-day `dollar_volume_20d` now exists
   (`:856-888`), so names above $500M need at least $1M of classified premium (`:939-947`).
8. **Watchdog overlap is noted, not folded in.** This change does not add the `conviction_monitor_daily` rows-per-session
   check that PI-002 / PI-022 need. It does make the monitor's outcome visible in the pipeline's digest ledger entry
   (`conviction_monitor`, `conviction_monitor_seconds`). If the pipeline never starts (a PI-022-style host outage), the
   night still has no rows. Only PI-002's watchdog catches that.

### 3.1 `services/conviction_monitor_service.py` (tabs)

**(a) Constants.** Insert immediately **after** `_TECHNICAL_TIMEFRAMES: Tuple[str, ...] = ("30m", "1h", "4h", "1d", "1wk")` (`:60`):

```python

# Polarity-arm "no read today" codes all start with "polarity_unavailable" (_summarize_notes relies on it).
# research PI-014: a symbol with no uoa_contract_daily rows for the date is labelled inputs-missing,
# never coverage-low. From 2026-05-19 until this fix every live row was that case, mislabelled.
POLARITY_CODE_INPUTS_MISSING = "polarity_unavailable_inputs_missing"
POLARITY_FALLBACK_INPUTS_MISSING = "no_flow_rows"
```

**(b) Pure helper.** Insert immediately **after** `_compute_polarity_for_monitor` ends (`return result` at `:953`) and
**before** the `# Qualifying-day blob fetch (with cache)` banner (`:956-958`):

```python
def _evaluate_polarity_arm(
	symbol: str,
	direction: str,
	polarity_aggregates: Dict[str, Dict[str, Any]],
	dollar_volume_20d: Optional[float],
	config: ConvictionMonitorConfig,
) -> Tuple[Dict[str, Any], Dict[str, Any], str, List[str]]:
	"""Polarity arm for one pick -> (aggregate, polarity_result, tier, reason_codes). Pure.

	A symbol absent from ``polarity_aggregates`` has no uoa_contract_daily rows for the date
	(prefetch_flow_polarity only creates entries for symbols with rows). It is labelled
	POLARITY_CODE_INPUTS_MISSING; its tier stays WATCH. Symbols with rows go through the
	unchanged _compute_polarity_for_monitor and _polarity_tier_for_direction gate (research PI-014).
	"""
	aggregate = polarity_aggregates.get(symbol) or {}
	if not aggregate:
		result: Dict[str, Any] = {
			"polarity": None,
			"coverage_ratio": None,
			"available": False,
			"fallback_reason": POLARITY_FALLBACK_INPUTS_MISSING,
		}
		return aggregate, result, "WATCH", [POLARITY_CODE_INPUTS_MISSING]
	symbol_daily = _assemble_symbol_daily(aggregate, dollar_volume_20d)
	result = _compute_polarity_for_monitor(symbol_daily, config)
	tier, codes = _polarity_tier_for_direction(
		result.get("polarity"),
		result.get("coverage_ratio"),
		direction,
		config,
	)
	return aggregate, result, tier, codes

```

**(c) Notes.** In `_summarize_notes`, insert two lines immediately **after** `parts.append(f"Polarity flipped against {direction} thesis.")`
(`:1059`) and **before** `elif polarity_tier == "WATCH" and any(c.startswith("polarity_unavailable") for c in codes):` (`:1060`):

```python
	elif polarity_tier == "WATCH" and POLARITY_CODE_INPUTS_MISSING in codes:
		parts.append("Polarity unavailable today (no options-flow rows for this symbol on this date).")
```

**(d) Run stats.** In `run_conviction_monitor`'s `stats` dict, insert after `"unknown_polarity": 0,` (`:1094`):

```python
		"polarity_inputs_missing": 0,
		"polarity_symbols_requested": 0,
		"polarity_symbols_with_flow_rows": 0,
```

**(e) Dark-night warning.** Insert immediately **after** the `except` block that ends `polarity_aggregates = {}` (`:1120`) and
**before** `dollar_volume_map = _fetch_dollar_volume_map(db, unique_symbols, trading_date)` (`:1122`):

```python

	stats["polarity_symbols_requested"] = len(unique_symbols)
	stats["polarity_symbols_with_flow_rows"] = sum(1 for s in unique_symbols if polarity_aggregates.get(s))
	if unique_symbols and stats["polarity_symbols_with_flow_rows"] == 0:
		logger.warning(
			"Conviction monitor %s: no uoa_contract_daily rows for any of %d monitored symbols -- "
			"polarity arm is dark tonight; rows are labelled %s (research PI-014)",
			trading_date,
			len(unique_symbols),
			POLARITY_CODE_INPUTS_MISSING,
		)
```

**(f) Use the helper.** In `_evaluate_one_pick`, replace **exactly** these nine lines (`:1178-1186`), keeping the
`# Polarity arm.` comment at `:1177` and the two `unknown_polarity` lines at `:1187-1188`:

```python
	aggregate = polarity_aggregates.get(symbol) or {}
	symbol_daily = _assemble_symbol_daily(aggregate, dollar_volume_map.get(symbol))
	polarity_result = _compute_polarity_for_monitor(symbol_daily, config)
	polarity_tier, polarity_codes = _polarity_tier_for_direction(
		polarity_result.get("polarity"),
		polarity_result.get("coverage_ratio"),
		direction,
		config,
	)
```

with:

```python
	aggregate, polarity_result, polarity_tier, polarity_codes = _evaluate_polarity_arm(
		symbol,
		direction,
		polarity_aggregates,
		dollar_volume_map.get(symbol),
		config,
	)
	if POLARITY_CODE_INPUTS_MISSING in polarity_codes:
		stats["polarity_inputs_missing"] += 1
```

`aggregate` is still a dict, so the `aggregate.get(...)` reads at `:1255-1259` are unchanged.

**(g) `__all__`.** Insert after `"_dedupe_preserve_order",` (`:1289`):

```python
	"_evaluate_polarity_arm",
	"_summarize_notes",
	"POLARITY_CODE_INPUTS_MISSING",
	"POLARITY_FALLBACK_INPUTS_MISSING",
```

No other line in the file changes.

### 3.2 `scripts/run_nightly_pipeline.py` (4 spaces)

**(a)** Insert `import time` between `import sys` (`:6`) and `import traceback` (`:7`).

**(b) Step helpers.** Insert immediately **after** `resolve_backfill_window` ends (`:86`) and **before** `def main() -> int:` (`:89`):

```python


# Conviction Monitor (research PI-014). It used to be its own 16:02 ET WebJob and read tonight's
# uoa_contract_daily before this pipeline had started, so every live run from 2026-05-19 found no
# flow rows. It now runs as a pipeline step after uoa_oi_gex has written them.
CONVICTION_MONITOR_SCRIPT = "scripts/run_conviction_monitor.py"


def conviction_monitor_skip_reason(trading_date: date, calendar_date: date) -> str | None:
    """Why the monitor step must not run for this invocation, or None. Pure.

    The monitor's technical arm fetches bars through *today* and has no as-of date, so it may only
    evaluate the session that closed on this ET calendar day. A pipeline re-run for an earlier
    trading date must not overwrite that date's monitor rows with later bars.
    """
    if trading_date != calendar_date:
        return "trading_date_not_today"
    return None


def build_conviction_monitor_args(trading_date: date) -> List[str]:
    return [CONVICTION_MONITOR_SCRIPT, "--trading-date", trading_date.isoformat()]


def execute_conviction_monitor_step(trading_date: date, calendar_date: date) -> dict:
    """Run the Conviction Monitor for tonight. Never raises.

    Returns {"status": "success" | "failed" | "skipped:<reason>", "seconds": float | None}.
    """
    reason = conviction_monitor_skip_reason(trading_date, calendar_date)
    if reason is not None:
        print(
            "conviction monitor step skipped "
            f"reason={reason} trading_date={trading_date.isoformat()} calendar_date={calendar_date.isoformat()}"
        )
        return {"status": f"skipped:{reason}", "seconds": None}
    started = time.monotonic()
    try:
        _run_command(build_conviction_monitor_args(trading_date))
        status = "success"
    except Exception as exc:
        print(f"WARNING conviction monitor step failed (non-fatal): {exc}")
        status = "failed"
    seconds = round(time.monotonic() - started, 1)
    print(f"conviction monitor step status={status} seconds={seconds}")
    return {"status": status, "seconds": seconds}
```

**(c)** Insert `    conviction_monitor: dict | None = None` immediately after `backfill_window_clamped = False` (`:151`).

**(d) The step.** Insert immediately **after** `_run_command(sas_ladder_args)` (`:277`) and **before** `current_step = "backfill_outcomes"` (`:278`):

```python
        # Conviction Monitor (research PI-014): after uoa_oi_gex, because its polarity arm reads
        # tonight's uoa_contract_daily / uoa_symbol_daily; after SAS and the ladder, so publication
        # time does not move. Non-fatal.
        current_step = "conviction_monitor"
        conviction_monitor = execute_conviction_monitor_step(trading_date, state.calendar_date)
```

**(e) Digest.** In `digest_details`, insert after `"completed_step": current_step,` (`:344`):

```python
            "conviction_monitor": (conviction_monitor or {}).get("status"),
            "conviction_monitor_seconds": (conviction_monitor or {}).get("seconds"),
```

**(f) Failure path.** Insert immediately **after** the `failure_details = {...}` dict closes (`:380`) and **before**
`record_scheduled_job_run(` (`:381`):

```python
        if trading_date is not None and conviction_monitor is None:
            # The monitor evaluates the previous five nights' picks, not tonight's SAS run, so a fatal
            # failure elsewhere must not cost those picks their evening read (research PI-014).
            conviction_monitor = execute_conviction_monitor_step(trading_date, state.calendar_date)
        failure_details["conviction_monitor"] = (conviction_monitor or {}).get("status")
        failure_details["conviction_monitor_seconds"] = (conviction_monitor or {}).get("seconds")
```

`failure_details` (with its `traceback`) is built before the step runs, so the recorded traceback is the pipeline's own. No
existing line in this file is deleted.

### 3.3 `app_data/jobs/triggered/conviction_monitor/`: delete the WebJob

```
git rm app_data/jobs/triggered/conviction_monitor/run.py app_data/jobs/triggered/conviction_monitor/settings.job
```

Leave `app_data/jobs/triggered/nightly_pipeline/` untouched. Its schedule stays `"0 05 16 * * 1-5"`.

### 3.4 `scripts/run_conviction_monitor.py`: docstring only

Replace lines `:4-5`:

```
``conviction_monitor_daily``. Invoked by the Azure WebJobs cron at
``app_data/jobs/triggered/conviction_monitor/settings.job`` (post-SAS nightly).
```

with:

```
``conviction_monitor_daily``. Invoked by ``scripts/run_nightly_pipeline.py`` as its
``conviction_monitor`` step, after ``uoa_oi_gex`` has written the day's options flow (research PI-014).
The technical arm reads today's bars, so a manual run for an earlier date does not reproduce that date.
```

No code line in the script changes.

### 3.5 Docs

- `docs/AZURE_WEBJOBS_AUTOMATION.md`:
  - Delete the `conviction_monitor` WebJob row (`:20`).
  - In the stage table, insert after the `sas_ladder_nightly` row (`:42`):
    `| 5a | \`conviction_monitor\` | \`run_conviction_monitor.py --trading-date <date>\` | non-fatal | Conviction Monitor rows for recent Elite picks. Runs after \`uoa_oi_gex\` because its polarity arm reads that day's \`uoa_contract_daily\`; skipped when the pipeline is re-run for an earlier date; also attempted after a fatal step fails. Was a separate 16:02 ET WebJob until PI-014 |`
  - After `:66` add: `> After the PI-014 deploy, confirm in Kudu that the \`conviction_monitor\` WebJob is no longer listed, and delete it in the portal if it is.`
- `docs/AI_AGENTS.md`:
  - `:234`: `(13 stages` becomes `(14 stages`.
  - `:240` becomes: `- **Same evening, inside the nightly pipeline after SAS** — Conviction Monitor exit signals over open SAS picks.`
- `docs/AI_PICKS_USER_GUIDE.md:56-57`: replace `Monitor re-evaluates open Elite picks daily around the close (16:02 ET).` with
  `Monitor re-evaluates open Elite picks every trading evening, after the nightly SAS run finishes.`
- `docs/PLATFORM_OVERVIEW.md:108`: replace `16:02 ET WebJob).` with `nightly-pipeline step after \`uoa_oi_gex\`).`
- `docs/SUPER_AGENT_FEATURES.md:91`: replace `16:02 ET re-evaluation of open picks for exit signals` with
  `evening re-evaluation of open picks for exit signals, run inside the nightly pipeline after the UOA step`.

That is the whole change: 11 paths (§4(c)).

---

## 4. Before / after check (repository only: no database, no network)

Unset `DATABASE_URL` in the shell first (PowerShell: `Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue`; Git Bash:
`unset DATABASE_URL`). Importing `services.conviction_monitor_service` pulls in only `sqlalchemy` and `models`
(`services/conviction_monitor_service.py:22-32`), and `models.py:1-7` imports only SQLAlchemy. Azure and the symbol-context
builder are imported lazily inside functions the commands below never call. The fixed trading date is **2026-09-08** (the §5 fixtures).

**(a) What must NOT differ: the coverage gate, fed the 16:02 state.** Run on the base commit and again after:

```
python -c "from services.conviction_monitor_service import ConvictionMonitorConfig as C, _assemble_symbol_daily as a, _compute_polarity_for_monitor as p, _polarity_tier_for_direction as t; r = p(a({}, None), C()); print(r['fallback_reason'], t(r['polarity'], r['coverage_ratio'], 'bullish', C()))"
```

Before and after, exactly: `no_decomp ('WATCH', ['polarity_unavailable_coverage_low'])`.

**(b) What differs: the label a pick gets when its symbol has no flow rows.**

```
python -c "from services.conviction_monitor_service import ConvictionMonitorConfig as C, _evaluate_polarity_arm as e; _, r, tier, codes = e('NVDA', 'bullish', {}, None, C()); print(r['fallback_reason'], tier, codes)"
```

Before: `ImportError: cannot import name '_evaluate_polarity_arm'`. After, exactly: `no_flow_rows WATCH ['polarity_unavailable_inputs_missing']`.

**(c) Scope, proved by diff.** Commit PI-014 as **one commit** containing only the §3 paths, then:

```
git show --stat HEAD
git show --numstat HEAD -- services/conviction_monitor_service.py scripts/run_nightly_pipeline.py scripts/run_conviction_monitor.py
git diff HEAD~1 HEAD -- services/conviction_monitor_service.py | grep '^-[^-]'
git diff --quiet HEAD~1 HEAD -- services/symbol_context_builder.py services/uoa_screener.py services/super_agent_select_scoring.py services/super_agent_select_service.py services/super_agent_select_report_service.py services/job_notifications.py core indicator_fetcher.py models.py db.py conftest.py routers templates app_data/jobs/triggered/nightly_pipeline app_data/jobs/triggered/fixed_universe_report_batch scripts/run_uoa_oi_gex_for_day.py && echo UNCHANGED
```

- `--stat` lists exactly these 11 paths:
  - `services/conviction_monitor_service.py`
  - `scripts/run_nightly_pipeline.py`
  - `scripts/run_conviction_monitor.py`
  - `app_data/jobs/triggered/conviction_monitor/run.py` (deleted)
  - `app_data/jobs/triggered/conviction_monitor/settings.job` (deleted)
  - `tests/test_conviction_monitor_ordering.py` (new)
  - `docs/AZURE_WEBJOBS_AUTOMATION.md`
  - `docs/AI_AGENTS.md`
  - `docs/AI_PICKS_USER_GUIDE.md`
  - `docs/PLATFORM_OVERVIEW.md`
  - `docs/SUPER_AGENT_FEATURES.md`
- `numstat` deletions are exactly **9** for `services/conviction_monitor_service.py`, **0** for `scripts/run_nightly_pipeline.py`
  and **2** for `scripts/run_conviction_monitor.py`.
- The `grep` prints exactly the nine lines quoted in §3.1(f). In particular, no line from `:172-196` (the gate), `:906-953`
  or `:792-811` appears.
- The last command prints `UNCHANGED`.

Do not try to demonstrate the fix by running the monitor or the pipeline. §5 exercises both against in-memory fakes, and §8 is the live check.

---

## 5. Test: `tests/test_conviction_monitor_ordering.py`

This is a standalone runner, following the EN-019 / PI-020 pattern: no pytest, no conftest, no database, no network, no Azure.
Run it as `python tests/test_conviction_monitor_ordering.py` with `DATABASE_URL` unset. Expected output: `PI-014: 12/12 checks passed`.

**Checks that would have caught PI-014:**
- **T5** runs the monitor in the 16:02 state (no flow rows for the date). At the base commit it fails: every row is
  labelled `polarity_unavailable_coverage_low` and nothing is logged.
- **T8** asserts the monitor runs inside the pipeline after `uoa_oi_gex`. At the base commit it fails because the monitor is not a pipeline step.

**Fixture provenance:** `uoa_contract_daily` is not in any desk manifest, and the desk ships no market data into the platform
repo, so the aggregates are synthetic. Their coverage (0.8) sits in the Steward's measured settled symbol-day median band,
0.70–0.89 (diagnosis §1b). The tiers follow from the formulas at `:906-953` and `:172-196`, and the arithmetic is written next to each fixture.

```python
"""PI-014: the Conviction Monitor must read tonight's options flow after the nightly pipeline writes it.

It ran as its own WebJob at 16:02 ET and read same-day uoa_contract_daily three minutes before the 16:05
nightly pipeline started, about 50-60 minutes before the pipeline's uoa_oi_gex step wrote that day's
rows. Every live run from 2026-05-19 found no rows and labelled every pick
polarity_unavailable_coverage_low (research PI-014; reports/STEWARD_PI-014_diagnosis.md).

Offline: no database, no network, no Azure. Run as
    python tests/test_conviction_monitor_ordering.py
with DATABASE_URL unset. Do NOT run under pytest in an environment whose DATABASE_URL points at a
real database: conftest.py runs create_tables() and deletes every users row around each test.
"""

from __future__ import annotations

import importlib.util
import json
import logging
import os
import subprocess
import sys
import types
from datetime import date, datetime
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

os.environ.pop("DATABASE_URL", None)
sys.modules.setdefault("db", types.ModuleType("db"))  # any `from db import ...` raises ImportError

import services.conviction_monitor_service as svc  # noqa: E402

TRADING_DATE = date(2026, 9, 8)   # Tuesday session
PICK_NIGHT = date(2026, 9, 4)     # Friday; weekdays to 2026-09-08 = 2 -> days_since_qualified 2
ET = ZoneInfo("America/New_York")
MONITOR_SCRIPT = "scripts/run_conviction_monitor.py"
_TFS = ("30m", "1h", "4h", "1d", "1wk")


# --- fixtures: prefetch_flow_polarity's per-symbol shape ---------------------------------------

def _agg(cb, cs, pb, ps, total):
    return {
        "call_buy_premium": float(cb),
        "call_sell_premium": float(cs),
        "put_buy_premium": float(pb),
        "put_sell_premium": float(ps),
        "contract_premium_total": float(total),
        "decomp_premium_total": float(cb + cs + pb + ps),
    }


# decomp 1.2M / total 1.5M = coverage 0.8; polarity (0.9 - 0.1 - 0.05 + 0.15) / 1.2 = +0.75
AGG_HOLD_BULL = _agg(900_000, 100_000, 50_000, 150_000, 1_500_000)
# coverage 0.8; polarity (0.1 - 0.5 - 0.5 + 0.1) / 1.2 = -0.666667
AGG_EXIT_BULL = _agg(100_000, 500_000, 500_000, 100_000, 1_500_000)
# coverage 0.8; polarity (0.4 - 0.3 - 0.3 + 0.2) / 1.2 = 0.0
AGG_NEUTRAL = _agg(400_000, 300_000, 300_000, 200_000, 1_500_000)
# decomp 0.6M / total 1.5M = coverage 0.4 < 0.5
AGG_LOW_COVERAGE = _agg(300_000, 100_000, 100_000, 100_000, 1_500_000)
# coverage 0.8, decomp 0.8M < the $1M megacap floor (dollar_volume_20d 600M > 500M)
AGG_BELOW_MIN_MEGACAP = _agg(500_000, 100_000, 100_000, 100_000, 1_000_000)
# rows exist, nothing classified: coverage 0.0
AGG_ROWS_NO_DECOMP = _agg(0, 0, 0, 0, 500_000)


# --- service: pure checks ----------------------------------------------------------------------

def test_t1_symbol_with_no_flow_rows_is_inputs_missing_not_coverage_low():
    cfg = svc.ConvictionMonitorConfig()
    aggregate, result, tier, codes = svc._evaluate_polarity_arm("NVDA", "bullish", {}, None, cfg)
    assert aggregate == {}
    assert tier == "WATCH"
    assert codes == [svc.POLARITY_CODE_INPUTS_MISSING] == ["polarity_unavailable_inputs_missing"], codes
    assert result == {"polarity": None, "coverage_ratio": None, "available": False, "fallback_reason": "no_flow_rows"}
    # The gate is unchanged: fed the same empty inputs directly it still says coverage-low.
    old = svc._compute_polarity_for_monitor(svc._assemble_symbol_daily({}, None), cfg)
    assert old["fallback_reason"] == "no_decomp"
    assert svc._polarity_tier_for_direction(old["polarity"], old["coverage_ratio"], "bullish", cfg) == (
        "WATCH", ["polarity_unavailable_coverage_low"])


def test_t2_symbols_with_flow_rows_go_through_the_unchanged_gate():
    cfg = svc.ConvictionMonitorConfig()
    cases = [
        # label, aggregate, direction, dollar_volume_20d, tier, codes, fallback, coverage, polarity
        ("hold_bull", AGG_HOLD_BULL, "bullish", None, "HOLD", [], None, 0.8, 0.75),
        ("exit_bull", AGG_EXIT_BULL, "bullish", None, "EXIT", ["polarity_flipped_bearish"], None, 0.8, -0.666667),
        ("exit_bear", AGG_HOLD_BULL, "bearish", None, "EXIT", ["polarity_flipped_bullish"], None, 0.8, 0.75),
        ("neutral", AGG_NEUTRAL, "bullish", None, "WATCH", ["polarity_neutralized"], None, 0.8, 0.0),
        ("low_coverage", AGG_LOW_COVERAGE, "bullish", None, "WATCH",
         ["polarity_unavailable_coverage_low"], "low_coverage", 0.4, None),
        ("below_min_megacap", AGG_BELOW_MIN_MEGACAP, "bullish", 600_000_000.0, "WATCH",
         ["polarity_unavailable_coverage_low"], "below_min_premium", 0.8, None),
        ("rows_no_decomp", AGG_ROWS_NO_DECOMP, "bullish", None, "WATCH",
         ["polarity_unavailable_coverage_low"], "no_decomp", 0.0, None),
    ]
    for label, agg, direction, dv, tier, codes, fallback, coverage, polarity in cases:
        aggregate, result, got_tier, got_codes = svc._evaluate_polarity_arm("SYM", direction, {"SYM": agg}, dv, cfg)
        assert aggregate is agg, label
        assert (got_tier, got_codes) == (tier, codes), (label, got_tier, got_codes)
        assert result["fallback_reason"] == fallback, (label, result)
        assert result["coverage_ratio"] == coverage, (label, result)
        assert result["polarity"] == polarity, (label, result)
        assert result["available"] is (polarity is not None), (label, result)


def test_t3_hold_is_reachable_only_when_polarity_is_live():
    assert svc._worst_tier(["WATCH", "HOLD"]) == "WATCH"  # every live row 2026-05-19.. had polarity WATCH
    assert svc._worst_tier(["HOLD", "HOLD"]) == "HOLD"
    assert svc._worst_tier(["EXIT", "HOLD"]) == "EXIT"
    assert svc._worst_tier(["HOLD", "EXIT"]) == "EXIT"
    assert svc._decay("WATCH", 4) == "HOLD" and svc._decay("HOLD", 4) == "HOLD"


def test_t4_notes_name_the_missing_input():
    missing = svc._summarize_notes("bullish", "WATCH", "HOLD", [svc.POLARITY_CODE_INPUTS_MISSING])
    assert missing == "Polarity unavailable today (no options-flow rows for this symbol on this date).", missing
    low = svc._summarize_notes("bullish", "WATCH", "HOLD", ["polarity_unavailable_coverage_low"])
    assert low == "Polarity unavailable today (data coverage low).", low
    assert svc._summarize_notes("bullish", "HOLD", "HOLD", []) == "Conviction intact."
    assert svc._summarize_notes("bullish", "EXIT", "HOLD", ["polarity_flipped_bearish"]) == (
        "Polarity flipped against bullish thesis.")


# --- service: run_conviction_monitor against in-memory fakes -----------------------------------

class _FakeRow:
    trading_date = None  # ConvictionMonitorDaily.trading_date == date -> False; the fake query ignores it

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def set_reason_codes(self, payload):
        self.reason_codes = list(payload or [])

    def set_polarity_details(self, payload):
        self.polarity_details = dict(payload or {})

    def set_technical_signal_count(self, payload):
        self.technical_signal_count = dict(payload or {})


class _FakeQuery:
    def __init__(self, log):
        self.log = log

    def filter(self, *args, **kwargs):
        return self

    def delete(self, synchronize_session=False):
        self.log.append("delete")
        return 0


class _FakeDb:
    def __init__(self):
        self.log, self.added = [], []

    def query(self, *args, **kwargs):
        self.log.append("query")
        return _FakeQuery(self.log)

    def commit(self):
        self.log.append("commit")

    def add_all(self, rows):
        self.added.extend(rows)


class _Capture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


def _identical_snapshot():
    # Qualifying day and today identical -> no weak/break code on any timeframe -> technical HOLD.
    return {"per_timeframe": {tf: {"price": {"close": 100.0}} for tf in _TFS}}


def _run_monitor(aggregates):
    scorecards = [
        SimpleNamespace(symbol=s, dominant_direction="bullish", trading_date=PICK_NIGHT,
                        overall_score=86.0, analysis_report_path=None)
        for s in ("MSFT", "NVDA", "TJX")
    ]
    seen = {}

    def prefetch_flow_polarity(db, *, symbols, trading_date):
        seen["symbols"], seen["trading_date"] = list(symbols), trading_date
        return dict(aggregates)

    stub = types.ModuleType("services.symbol_context_builder")
    stub.prefetch_flow_polarity = prefetch_flow_polarity
    names = ("ConvictionMonitorDaily", "_load_recent_qualifieds", "_fetch_dollar_volume_map",
             "_fetch_qualifying_blob", "_fetch_today_price_action", "_fetch_today_technical_snapshot")
    saved = {name: getattr(svc, name) for name in names}
    saved_module = sys.modules.get("services.symbol_context_builder")
    sys.modules["services.symbol_context_builder"] = stub
    svc.ConvictionMonitorDaily = _FakeRow
    svc._load_recent_qualifieds = lambda db, td, n: list(scorecards)
    svc._fetch_dollar_volume_map = lambda db, symbols, td: {}
    svc._fetch_qualifying_blob = lambda **kw: {"price_action_snapshot": _identical_snapshot(), "technical_snapshot": {}}
    svc._fetch_today_price_action = lambda symbol, timeframes: _identical_snapshot()
    svc._fetch_today_technical_snapshot = lambda symbol: {}
    capture = _Capture()
    svc.logger.addHandler(capture)
    propagate, svc.logger.propagate = svc.logger.propagate, False
    db = _FakeDb()
    try:
        stats = svc.run_conviction_monitor(db, trading_date=TRADING_DATE)
    finally:
        svc.logger.removeHandler(capture)
        svc.logger.propagate = propagate
        for name, value in saved.items():
            setattr(svc, name, value)
        if saved_module is None:
            sys.modules.pop("services.symbol_context_builder", None)
        else:
            sys.modules["services.symbol_context_builder"] = saved_module
    return stats, {r.symbol: r for r in db.added}, capture.records, seen


def test_t5_the_1602_state_is_labelled_inputs_missing_and_logged():
    stats, rows, records, seen = _run_monitor({})
    assert seen == {"symbols": ["MSFT", "NVDA", "TJX"], "trading_date": TRADING_DATE}, seen
    assert stats["errors"] == 0 and stats["rows_written"] == 3, stats
    assert (stats["polarity_symbols_requested"], stats["polarity_symbols_with_flow_rows"],
            stats["polarity_inputs_missing"], stats["unknown_polarity"]) == (3, 0, 3, 3), stats
    for sym, row in rows.items():
        assert row.technical_overall_tier == "HOLD", (sym, row.technical_overall_tier)
        assert (row.polarity_tier, row.overall_tier) == ("WATCH", "WATCH"), sym  # HOLD cannot print
        assert "polarity_unavailable_coverage_low" not in row.reason_codes, (sym, row.reason_codes)
        assert row.reason_codes[0] == "polarity_unavailable_inputs_missing", (sym, row.reason_codes)
        assert row.polarity_details["fallback_reason"] == "no_flow_rows", sym
        assert row.polarity_details["contract_premium_total"] is None, sym  # the freeze's signature
    dark = [r for r in records if r.levelno == logging.WARNING and "polarity arm is dark" in r.getMessage()]
    assert len(dark) == 1, [r.getMessage() for r in records]


def test_t6_after_uoa_oi_gex_polarity_is_live_and_hold_is_reachable():
    stats, rows, records, _ = _run_monitor({"MSFT": AGG_EXIT_BULL, "NVDA": AGG_HOLD_BULL})
    assert stats["errors"] == 0 and stats["rows_written"] == 3, stats
    assert (stats["polarity_symbols_requested"], stats["polarity_symbols_with_flow_rows"],
            stats["polarity_inputs_missing"], stats["unknown_polarity"]) == (3, 2, 1, 1), stats
    nvda, msft, tjx = rows["NVDA"], rows["MSFT"], rows["TJX"]
    assert (nvda.polarity_tier, nvda.overall_tier, nvda.age_adjusted_severity) == ("HOLD", "HOLD", "HOLD")
    assert nvda.notes == "Conviction intact.", nvda.notes
    assert (msft.polarity_tier, msft.overall_tier) == ("EXIT", "EXIT")
    assert msft.reason_codes[0] == "polarity_flipped_bearish", msft.reason_codes
    assert (msft.polarity_coverage_today, msft.polarity_today) == (0.8, -0.666667)
    assert (tjx.polarity_tier, tjx.overall_tier) == ("WATCH", "WATCH")
    assert tjx.reason_codes[0] == "polarity_unavailable_inputs_missing", tjx.reason_codes
    assert not [r for r in records if "polarity arm is dark" in r.getMessage()]


# --- pipeline: orchestration with every side effect replaced -----------------------------------

def _load_pipeline():
    spec = importlib.util.spec_from_file_location(
        "_pi014_nightly_pipeline", _REPO_ROOT / "scripts" / "run_nightly_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    os.environ.pop("DATABASE_URL", None)  # the module loads .env; nothing here connects
    for key in ("MARKET_BRIEF_NIGHTLY_ENABLED", "SAS_EXCURSION_NIGHTLY_ENABLED", "DARK_COHORT_DIGEST_ENABLED"):
        os.environ.pop(key, None)
    return mod


def _run_pipeline(argv, fail_script=None):
    mod = _load_pipeline()
    calls, records = [], []

    def fake_run_command(args):
        calls.append(list(args))
        if fail_script is not None and args[0] == fail_script:
            raise subprocess.CalledProcessError(1, args)

    state = SimpleNamespace(
        now_et=datetime(2026, 9, 8, 16, 5, tzinfo=ET),
        calendar_date=TRADING_DATE,
        latest_closed_trading_date=TRADING_DATE,
        nightly_eligible=True,
        nightly_trading_date=TRADING_DATE,
        nightly_reason="eligible",
    )
    mod._run_command = fake_run_command
    mod.get_market_session_state = lambda: state
    mod.record_scheduled_job_run = lambda **kw: records.append(kw) or True
    mod.send_daily_success_digest_email = lambda **kw: True
    mod.send_job_status_email = lambda **kw: True
    saved_argv, sys.argv = sys.argv, ["run_nightly_pipeline.py", *argv]
    raised, rc = None, None
    try:
        rc = mod.main()
    except Exception as exc:  # noqa: BLE001
        raised = exc
    finally:
        sys.argv = saved_argv
    return rc, raised, calls, records


def test_t7_pure_step_helpers():
    mod = _load_pipeline()
    assert mod.conviction_monitor_skip_reason(TRADING_DATE, TRADING_DATE) is None
    assert mod.conviction_monitor_skip_reason(date(2026, 9, 4), TRADING_DATE) == "trading_date_not_today"
    assert mod.build_conviction_monitor_args(TRADING_DATE) == [MONITOR_SCRIPT, "--trading-date", "2026-09-08"]


def test_t8_monitor_runs_inside_the_pipeline_after_uoa_and_sas():
    rc, raised, calls, records = _run_pipeline([])
    assert raised is None and rc == 0, raised
    scripts = [c[0] for c in calls]
    assert scripts.count(MONITOR_SCRIPT) == 1, scripts
    order = [scripts.index(s) for s in (
        "scripts/run_uoa_oi_gex_for_day.py", "scripts/run_super_agent_select_nightly.py",
        "scripts/run_sas_ladder_nightly.py", MONITOR_SCRIPT, "scripts/backfill_outcomes.py")]
    assert order == sorted(order), scripts
    assert calls[scripts.index(MONITOR_SCRIPT)] == [MONITOR_SCRIPT, "--trading-date", "2026-09-08"]
    (success,) = [r for r in records if r["status"] == "success"]
    assert success["details"]["conviction_monitor"] == "success", success["details"]
    assert isinstance(success["details"]["conviction_monitor_seconds"], float)


def test_t9_a_monitor_failure_does_not_fail_the_pipeline():
    rc, raised, calls, records = _run_pipeline([], fail_script=MONITOR_SCRIPT)
    assert raised is None and rc == 0, raised
    scripts = [c[0] for c in calls]
    assert scripts.index("scripts/backfill_outcomes.py") > scripts.index(MONITOR_SCRIPT), scripts
    (success,) = [r for r in records if r["status"] == "success"]
    assert success["details"]["conviction_monitor"] == "failed", success["details"]


def test_t10_monitor_still_runs_when_a_fatal_step_fails():
    rc, raised, calls, records = _run_pipeline([], fail_script="scripts/run_super_agent_select_nightly.py")
    assert isinstance(raised, subprocess.CalledProcessError), raised
    scripts = [c[0] for c in calls]
    assert scripts.count(MONITOR_SCRIPT) == 1 and scripts[-1] == MONITOR_SCRIPT, scripts
    assert "scripts/backfill_outcomes.py" not in scripts
    (failed,) = [r for r in records if r["status"] == "failed"]
    assert failed["details"]["failed_step"] == "super_agent_select", failed["details"]
    assert failed["details"]["conviction_monitor"] == "success", failed["details"]


def test_t11_a_rerun_for_an_earlier_date_leaves_that_dates_monitor_rows_alone():
    rc, raised, calls, records = _run_pipeline(["--trading-date", "2026-09-04"])
    assert raised is None and rc == 0, raised
    assert MONITOR_SCRIPT not in [c[0] for c in calls]
    (success,) = [r for r in records if r["status"] == "success"]
    assert success["details"]["conviction_monitor"] == "skipped:trading_date_not_today", success["details"]


def test_t12_the_1602_webjob_is_gone_and_the_pipeline_schedule_is_unchanged():
    job = _REPO_ROOT / "app_data" / "jobs" / "triggered" / "conviction_monitor"
    assert not (job / "settings.job").exists() and not (job / "run.py").exists()
    settings = json.loads(
        (_REPO_ROOT / "app_data" / "jobs" / "triggered" / "nightly_pipeline" / "settings.job").read_text())
    assert settings["schedule"] == "0 05 16 * * 1-5", settings


_CHECKS = [
    test_t1_symbol_with_no_flow_rows_is_inputs_missing_not_coverage_low,
    test_t2_symbols_with_flow_rows_go_through_the_unchanged_gate,
    test_t3_hold_is_reachable_only_when_polarity_is_live,
    test_t4_notes_name_the_missing_input,
    test_t5_the_1602_state_is_labelled_inputs_missing_and_logged,
    test_t6_after_uoa_oi_gex_polarity_is_live_and_hold_is_reachable,
    test_t7_pure_step_helpers,
    test_t8_monitor_runs_inside_the_pipeline_after_uoa_and_sas,
    test_t9_a_monitor_failure_does_not_fail_the_pipeline,
    test_t10_monitor_still_runs_when_a_fatal_step_fails,
    test_t11_a_rerun_for_an_earlier_date_leaves_that_dates_monitor_rows_alone,
    test_t12_the_1602_webjob_is_gone_and_the_pipeline_schedule_is_unchanged,
]


if __name__ == "__main__":
    passed = 0
    for check in _CHECKS:
        try:
            check()
        except Exception as exc:  # noqa: BLE001 - a runner, not a library
            print(f"FAIL {check.__name__}: {exc.__class__.__name__}: {exc}")
            raise SystemExit(1)
        passed += 1
    print(f"PI-014: {passed}/{len(_CHECKS)} checks passed")
```

**The arithmetic the assertions rest on**, so that a failure points at code rather than at the test:
- **T5/T6 technical arm:** the qualifying-day and today snapshots are identical (close 100.0 on every timeframe, no structure,
  levels, indicators or bias), so no weak or break code fires. 30m is aged-capped at `days_since_qualified = 2`
  (`:98-104`), which is HOLD by construction. The concurrence rollup returns HOLD (`:784-785`).
- **T6 NVDA:** polarity HOLD and technical HOLD give an overall HOLD, with no decay at day 2 (`:807-811`).
- **T6 MSFT:** EXIT is the worst of EXIT and HOLD.
- **T6 TJX:** absent from the aggregates, so WATCH with the inputs-missing code.

If a check fails, fix the code, not the numbers.

**Loader notes:**
- Loading `scripts/run_nightly_pipeline.py` imports `core.market_sessions`, `core.trading_days` and `services.job_notifications`.
  Its Azure imports are optional and lazy (`services/job_notifications.py:12-17`, `:213-215`). `build_regime_args` imports
  `services/market_regime/repository.py`, which imports only `models`.
- Every function that writes (`_run_command`, the digest recorder, the two email senders) is replaced before `main()` runs.

### Acceptance (what the PR must report)

1. §4(a) prints the identical line before and after, and §4(b) prints the two lines given there.
2. `python tests/test_conviction_monitor_ordering.py` prints `PI-014: 12/12 checks passed`, and the PR states that `pytest` was not run.
3. §4(c) shows the 11-path stat list, deletions of 9 / 0 / 2, the nine `grep` lines, and `UNCHANGED`.
4. No migration was added, and no file under `models.py`, `db.py`, `conftest.py`, `routers/` or `templates/` is in the diff.
5. The platform SHA of the merge.

---

## 6. Rollback

```
git revert --no-edit <sha> && git push
```

This is one commit, with no schema and no data step. It restores the 16:02 WebJob folder, the old labels and the old step list.
After a revert, Haci confirms in Kudu that the `conviction_monitor` WebJob is listed again (the same stale-wrapper caveat as
§8 Step 1). Rows written between `D0` and the revert stay as written. The DATA_NOTES entry (§8 Step 3) gets a closing date.

---

## 7. Out of scope: do not touch

- **Re-running the monitor for past dates.** Rows for 2026-05-19 .. `D0 − 1` stay as written. A historical rebuild would read
  today's bars for the technical arm, and it would be a separate Haci decision with its own DATA_NOTES entry.
- **The coverage gate and polarity formula:** `services/conviction_monitor_service.py:172-196`, `:906-953`, and the thresholds `:72-77`.
  One residual mislabel is recorded here, not fixed. When `fallback_reason = below_min_premium` (coverage is fine, but the premium
  is under the floor), the gate still writes `polarity_unavailable_coverage_low`. On the four frozen dates when inputs existed, that was
  44 of 160 rows (`v001_conviction_monitor.parquet`, 2026-05-12..15). The tier is WATCH either way. If Haci wants the label
  split, it is a separate register entry.
- **The technical arm, tier rules, concurrence rollup, age decay, `_load_recent_qualifieds` and weekday counting**
  (`:328-811`, `:818-849`, `:1029-1052`).
- **`services/symbol_context_builder.py`, `services/uoa_screener.py` (PI-020), and the UOA step's growing runtime** (diagnosis, "What is NOT determined").
- **PI-002 / PI-022**: the coverage watchdog, including a `conviction_monitor_daily` rows-per-session check. **PI-004**: run provenance.
- **`scripts/run_conviction_monitor.py` behaviour** beyond its docstring. Its manual `--trading-date` override remains.
- **Panel copy, routers, templates, models, migrations**, the in-process UOA scheduler, the EN-019 batch, and `.worktrees/`.

---

## 8. Verification at `/desk-run verify PI-014 <sha>`

**Whose step is whose.** **Haci:** merge, deploy, the Kudu check, and noting `D0`. **Data Steward:** the repo half and V1–V5
below, on `$RESEARCH_DB_URL` under `sas_research_ro`: counts and timestamps only, no outcome column, no touch rate.
**Desk:** Step 3 on `D0`. **Registrar:** the Q019 / Q038 sweep named in the header.

**Repo half (Steward, read-only on the platform repo):** at `<sha>`, run the four `git` commands of §4(c). They must reproduce
the 11-path list, deletions of 9 / 0 / 2, the nine `grep` lines, and `UNCHANGED`. Record the output.

**Step 1 (Haci).**
1. Merge and deploy.
2. In Kudu, confirm that the `conviction_monitor` WebJob is **not** listed. If it is, delete it in the portal. This is not a database step.
3. Note `D0`, the first trading date whose nightly pipeline ran `<sha>`.
4. Record `IMPLEMENTED:<sha>` on the PI-014 row.

**Step 2 (Steward), after at least 10 sessions from `D0`.** Replace `D0` in the queries below with the date.

```sql
-- V1. Every session has monitor rows; no rows on a date without a SAS run (holidays).
WITH s AS (SELECT trading_date FROM super_agent_select_runs
           WHERE trading_date BETWEEN DATE 'D0' AND DATE 'D0' + 16),
     cm AS (SELECT trading_date, count(*) AS rows FROM conviction_monitor_daily
            WHERE trading_date BETWEEN DATE 'D0' AND DATE 'D0' + 16 GROUP BY 1)
SELECT coalesce(s.trading_date, cm.trading_date) AS trading_date,
       s.trading_date IS NOT NULL AS sas_run, coalesce(cm.rows, 0) AS monitor_rows
FROM s FULL JOIN cm ON cm.trading_date = s.trading_date
ORDER BY 1;

-- V2. Labels and tiers per date, the 10 dates before D0 (the live before-state) and after.
SELECT trading_date,
       count(*) AS rows,
       sum(CASE WHEN reason_codes_json LIKE '%"polarity_unavailable_coverage_low"%'   THEN 1 ELSE 0 END) AS coverage_low,
       sum(CASE WHEN reason_codes_json LIKE '%"polarity_unavailable_inputs_missing"%' THEN 1 ELSE 0 END) AS inputs_missing,
       sum(CASE WHEN polarity_coverage_today IS NOT NULL THEN 1 ELSE 0 END) AS coverage_present,
       sum(CASE WHEN polarity_today IS NOT NULL THEN 1 ELSE 0 END)          AS polarity_present,
       sum(CASE WHEN polarity_tier = 'HOLD'  THEN 1 ELSE 0 END) AS pol_hold,
       sum(CASE WHEN polarity_tier = 'WATCH' THEN 1 ELSE 0 END) AS pol_watch,
       sum(CASE WHEN polarity_tier = 'EXIT'  THEN 1 ELSE 0 END) AS pol_exit,
       sum(CASE WHEN overall_tier  = 'HOLD'  THEN 1 ELSE 0 END) AS overall_hold,
       sum(CASE WHEN overall_tier  = 'WATCH' THEN 1 ELSE 0 END) AS overall_watch,
       sum(CASE WHEN overall_tier  = 'EXIT'  THEN 1 ELSE 0 END) AS overall_exit,
       sum(CASE WHEN technical_overall_tier = 'UNKNOWN' THEN 1 ELSE 0 END) AS technical_unknown
FROM conviction_monitor_daily
WHERE trading_date BETWEEN DATE 'D0' - 14 AND DATE 'D0' + 16
GROUP BY 1 ORDER BY 1;

-- V3. Why polarity was missing, before vs after (NULL fallback_reason = polarity available).
SELECT CASE WHEN trading_date < DATE 'D0' THEN 'before' ELSE 'after' END AS period,
       (polarity_details_json::jsonb)->>'fallback_reason' AS fallback_reason,
       count(*) AS rows
FROM conviction_monitor_daily
WHERE trading_date BETWEEN DATE 'D0' - 14 AND DATE 'D0' + 16
GROUP BY 1, 2 ORDER BY 1, 2;

-- V4. Write order: the monitor loads its inputs after the day's UOA run and SAS run finished.
--     created_at is the insert transaction's start, just after the monitor's delete: its read time.
WITH cm AS (SELECT trading_date, min(created_at) AS cm_first FROM conviction_monitor_daily
            WHERE trading_date BETWEEN DATE 'D0' - 3 AND DATE 'D0' + 16 GROUP BY 1)
SELECT cm.trading_date,
       cm.cm_first    AT TIME ZONE 'America/New_York' AS cm_first_et,
       u.status                                          AS uoa_status,
       u.finished_at  AT TIME ZONE 'America/New_York' AS uoa_finished_et,
       s.finished_at  AT TIME ZONE 'America/New_York' AS sas_finished_et,
       round((extract(epoch FROM cm.cm_first - u.finished_at) / 60.0)::numeric, 1) AS cm_minus_uoa_min,
       round((extract(epoch FROM cm.cm_first - s.finished_at) / 60.0)::numeric, 1) AS cm_minus_sas_min
FROM cm
LEFT JOIN uoa_runs u ON u.trading_date = cm.trading_date AND u.run_type = 'nightly'
LEFT JOIN super_agent_select_runs s ON s.trading_date = cm.trading_date
ORDER BY 1;

-- V5. History untouched: rows dated on or before the freeze must match manifest_v001 exactly.
SELECT count(*) AS rows,
       sum(CASE WHEN reason_codes_json LIKE '%"polarity_unavailable_coverage_low"%'   THEN 1 ELSE 0 END) AS coverage_low,
       sum(CASE WHEN reason_codes_json LIKE '%"polarity_unavailable_inputs_missing"%' THEN 1 ELSE 0 END) AS inputs_missing,
       sum(CASE WHEN polarity_tier = 'HOLD' THEN 1 ELSE 0 END) AS pol_hold,
       sum(CASE WHEN polarity_tier = 'EXIT' THEN 1 ELSE 0 END) AS pol_exit,
       sum(CASE WHEN overall_tier  = 'HOLD' THEN 1 ELSE 0 END) AS overall_hold
FROM conviction_monitor_daily
WHERE trading_date <= DATE '2026-09-10';
-- Must equal v001_conviction_monitor.parquet (sha256 687527943e8b...9c7c): 3339 | 3243 | 0 | 53 | 35 | 18
```

**PASS requires all of the following:**
1. **V5** equals the freeze exactly. Any difference is a historical rewrite this fix does not make, so the check FAILS: stop and find what wrote it.
2. **V1:** every session `D0 .. D0+9` with a SAS run has `monitor_rows ≥ 1` (the freeze carries 25–44 per date since 2026-06-01).
   No date without a SAS run has monitor rows. A holiday row from `D0` onward means a lingering 16:02 WebJob, so Step 1's Kudu check failed.
3. **V4:** on every session from `D0`, `cm_minus_uoa_min > 0` and `cm_minus_sas_min > 0`. A `cm_first_et` of about 16:02 on any date
   from `D0` FAILS: the old WebJob fired and the pipeline step did not replace its rows.
4. **V2, after `D0`:**
   - On every session, `coverage_present ≥ 0.8 × rows` and `coverage_low < rows`.
   - Across `D0 .. D0+9`, at least one `pol_hold` row and at least one `overall_hold` row.
   - `pol_exit` and the `inputs_missing` share are reported but are not a bar.

   Basis: on the four frozen dates whose inputs existed (2026-05-12..15), coverage was present on 160 of 160 rows and all three
   polarity tiers occurred. **Before `D0`**, V2 should show `coverage_low = rows` and `overall_hold = 0` on every date. Those
   rows were not rewritten, so the before/after contrast is visible in one query.
5. **V3:** after `D0`, `no_decomp` is no longer the only reason, and a NULL (available) reason is present. `no_flow_rows` appears only on
   rows V2 counts as `inputs_missing`.
6. If any session from `D0` has `inputs_missing = rows`, read that date's `uoa_status` in V4:
   - If it is `success`, the ordering is broken, and the check FAILS.
   - Otherwise the night's UOA step failed. The rows are honestly labelled, which is the intended behaviour. Record the date as an operational note, not a PI-014 failure.

On PASS the Steward sets the PI-014 row to `VERIFIED`, and pins V2's monthly aggregate into the next successor freeze notes so the
before/after is reproducible (DP-50(c), the PI-014 entry's own request).

**Step 3 (desk, on `D0`): the `research/data/DATA_NOTES.md` entry.** This is a dated forward-only note, not a repair-log row: no historical row is rewritten.

> ## Conviction Monitor runs inside the nightly pipeline from `D0` (PI-014, code `<sha>`)
> From trading date `D0`, `conviction_monitor_daily` rows are written by the nightly pipeline's `conviction_monitor` step. That step runs after
> `uoa_oi_gex`, `super_agent_select` and `sas_ladder_nightly`, and replaces the 16:02 ET WebJob, which is removed. The
> polarity arm therefore reads that date's `uoa_contract_daily` and `uoa_symbol_daily` rows.
>
> **What differs between the two sides of `D0`:**
> - `polarity_today`, `polarity_coverage_today`, `polarity_tier`, `overall_tier`, `age_adjusted_severity` and `notes` change meaning.
> - `reason_codes_json` gains a new code, `polarity_unavailable_inputs_missing`.
> - `polarity_details_json` gets populated premiums and a new `fallback_reason`, `no_flow_rows`.
> - `created_at` / `updated_at` fall the same evening after the SAS run, no longer at about 16:02 ET.
> - The `technical_*` tiers may move slightly, because bars are fetched later the same evening.
> - No rows are written on NYSE holidays, or when the pipeline is re-run for an earlier date.
>
> **Before `D0`:** from 2026-05-19 to `D0 − 1` every row was written before that day's flow existed. `polarity_tier` is WATCH,
> `polarity_unavailable_coverage_low` is on every row, `polarity_details.contract_premium_total` is null, and `overall_tier` HOLD cannot
> occur. The exception is 2026-05-12..05-15, which was backfilled on 2026-05-16 after contracts existed. PI-014's register row dated
> the onset 2026-06-01; the diagnosis and the freeze date it to 2026-05-19.
>
> **For questions and freezes:**
> - A question whose window spans `D0` treats these columns as two features (DP-50(a)). For Q019 this fires DECISIONS #12(a), a
>   window-start move. Q038's re-entry restarts at `D0`.
> - The `conviction_monitor` availability in `research/lib/freeze_config.json` reads `16:02` for rows before `D0`, and "same evening,
>   after `sas_ladder_nightly`" from `D0`. `lag_sessions` stays 1.
