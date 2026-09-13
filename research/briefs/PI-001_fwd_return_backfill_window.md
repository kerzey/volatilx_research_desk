# PI-001 — `uoa_symbol_daily.fwd_return_*` maturation is still frozen: floor the nightly backfill window in-process

**Type:** fix brief (platform issue, not a research finding)
**Register row:** `research/PLATFORM_ISSUES.md` PI-001, severity high, `HACI_DECIDED:fix`
**Written:** 2026-09-13 by the Brief Writer, on Haci's `/desk-run prompt PI-001` (DP-48: asking is the decision)
**Platform repo:** `C:\Users\sahin\Projects\volatilx`
**Platform SHA all `path:line` citations are taken at:** `fa70688bc252d14f8d67e371afafc194731c324e` (committed 2026-09-05)
**Research repo SHA:** `2fa3362`
**Feature flag:** none — see §3 for why.
**Related, deliberately NOT folded in:** PI-002 (nothing alerts on this defect). See §7.

You are the coding agent working in the platform repo. This brief is self-contained: do not ask
questions, do not redesign. Implement §3, run §4, add §5, and report the SHA.

---

## 1. Symptom — what is wrong, and the evidence

Forward returns on `uoa_symbol_daily` stopped maturing in May 2026 and have never recovered.
From the desk's frozen dataset (`research/reports/FREEZE_v001.md` §5, manifest_v001, as_of
2026-09-10):

- `fwd_return_30d_pct` coverage falls from ~99% to 0% starting `trading_date` 2026-05-20,
  cliff-clean (2026-05-19: 494/498 non-null; 2026-05-20: 0/498).
- `fwd_return_14d_pct` falls from ~99% to 0% starting 2026-06-12.
- `fwd_return_5d_pct` falls from ~99% to 0% starting 2026-06-26.
- Writes resume 2026-07-06 but recover only to **~5% of baseline** (~23–25 of ~495–500 symbols
  per night for the 5d/14d horizons) and stay at that level through the latest sampled date,
  2026-08-14 — six-plus weeks after the nominal "fix".
- `fwd_return_30d_pct` **relapses to 0%** for `trading_date >= 2026-07-27`. Those dates are more
  than 30 sessions in the past as of 2026-09-10, so this is not right-censoring; it is a live gap.
- Contrast: the `_w60` outcome family on the SAS/projection tables is clean, with normal
  maturation censoring and no cliff. The defect is isolated to the legacy `fwd_return_*` family.

Platform impact: every product surface that reads these columns — the UOA/whale performance
aggregates in `routers/performance.py:64-105`, `:1412-1421`, `:1541-1600`, `:2924-2971` and the
screener payloads in `routers/uoa_screener.py:271-276`, `:593-595`, `:1113-1114` — is computing
its numbers from a ~5% non-random sample of the rows that should be populated. Desk impact: none
today (the desk computes its own forward returns from its own price freeze), so nothing in the
LEDGER depends on this column.

### Reproducing query (read-only, `$RESEARCH_DB_URL`, `research_ro`)

```sql
-- A. The monthly collapse and the ~5% floor.
SELECT date_trunc('month', trading_date)::date            AS month,
       count(*)                                           AS n_rows,
       round(100.0 * count(fwd_return_5d_pct)  / count(*), 1) AS pct_5d,
       round(100.0 * count(fwd_return_14d_pct) / count(*), 1) AS pct_14d,
       round(100.0 * count(fwd_return_30d_pct) / count(*), 1) AS pct_30d
FROM uoa_symbol_daily
WHERE trading_date BETWEEN DATE '2026-04-01' AND DATE '2026-08-14'
GROUP BY 1
ORDER BY 1;
-- Expected today: April/May near 99% for 5d/14d, then a collapse; July and August ~5%
-- for 5d/14d and ~0% for 30d.

-- B. One fully matured date, the fixed date used throughout this brief.
SELECT count(*)                    AS n_rows,
       count(fwd_return_1d_pct)    AS n_1d,
       count(fwd_return_3d_pct)    AS n_3d,
       count(fwd_return_5d_pct)    AS n_5d,
       count(fwd_return_7d_pct)    AS n_7d,
       count(fwd_return_14d_pct)   AS n_14d,
       count(fwd_return_30d_pct)   AS n_30d
FROM uoa_symbol_daily
WHERE trading_date = DATE '2026-07-28';
-- Expected today: n_rows ~500, n_5d/n_14d ~24, n_30d = 0. Every horizon is due:
-- 2026-07-28 is more than 30 sessions before as_of 2026-09-10.
```

---

## 2. Cause

The nightly outcome backfill only re-visits a signal for as many nights as the **backfill window**
is wide. That window is supplied from **outside** the repo, by the Azure WebJob wrapper argument,
and production is executing a stale wrapper that passes `4`.

The causal chain, already established inside the platform repo by the 2026-07-02 repair and
confirmed unchanged at this SHA:

1. **The window comes from the wrapper.** `scripts/run_nightly_pipeline.py:104-109` defines
   `--backfill-trading-days` (repo default 70). `scripts/run_nightly_pipeline.py:139-148` turns it
   into `backfill_start`/`backfill_end`, which `:183-191` forwards to
   `scripts/backfill_outcomes.py` and `:237-238` executes. Whatever the caller passes wins; the
   script asserts nothing about it.
2. **The deployed wrapper passes 4.** `reports/pipeline_repair.md:12-42` documents it: the wrapper
   `app_data/jobs/triggered/nightly_pipeline/run.py` passed `4` from its creation (2026-04-05,
   commit `76580a9`); a signal was therefore visited only on its first ~4 nights — long enough for
   `fwd_return_1d/3d` plus 1-day MFE/MAE, never long enough for 5/7/14/30 — then aged out of the
   window forever. The masking manual full-range sweeps stopped on 2026-05-18, which is exactly
   where the desk's cliff sits.
3. **The committed fix never reached production.** `app_data/jobs/triggered/nightly_pipeline/run.py:98-105`
   at this SHA passes `65`, with the correct explanatory comment (commit `2229780`, 2026-05-31).
   `reports/pipeline_repair.md:27-42` proves production still ran the old 4-day wrapper through
   2026-07-01 and names the mechanism: WebJobs uploaded via Kudu/portal are not replaced by zip
   deploys of `wwwroot`. **Source is correct; the deployed copy is not.** The desk's post-07-06
   ~5% floor is the same defect still running.
4. **The asymmetry that proves it.** The W60 maintainer's window is computed *inside*
   `scripts/run_nightly_pipeline.py:192-209` (`w60_start = subtract_trading_days(backfill_end, 65)`,
   hardcoded) and W60 coverage is healthy. Same pipeline, same night, same DB — the only
   difference is where the number comes from. This is also why the fix belongs in the script and
   not in the wrapper: the stale wrapper still invokes `wwwroot/scripts/run_nightly_pipeline.py`
   (`app_data/jobs/triggered/nightly_pipeline/run.py:83-107` resolves the repo root and executes
   the *deployed* script), so a floor placed in the script takes effect on the next deploy with no
   WebJob re-sync.
5. **What the residual ~5% actually is.** With the wide backfill effectively dead, the only writer
   left is the bulletin trickle inside the screener: `services/uoa_screener.py:1882-1888` fills the
   prior date, and `:1892-1910` visits exactly five older dates (T−3, T−5, T−7, T−14, T−30
   weekdays). Both go through `backfill_uoa_outcomes_from_bulletin`
   (`services/uoa_screener.py:346-353`), which takes symbols **only from that night's bulletin
   lists** (`:361-378`) and caps them at `max_symbols: int = 40` — ~23–25 unique symbols after
   de-duplication across the day/swing/long buckets. ~24 of ~500 is the observed 5%.
6. **Why 30d is 0% and not 5%.** Each horizon has exactly one scheduled chance in that trickle: a
   date's 30d value can only be written on the single night that is 30 weekdays later
   (`services/uoa_screener.py:1897-1903`). The lookback counts **weekdays**, not trading days
   (`_previous_weekday`), so a market holiday in the interval, or one skipped nightly run, means
   the date is never visited again by the 30-day arm. Dates from 2026-07-27 onward fell through
   that single hole.

The computation itself is fine: `services/uoa_screener.py:54-146`
(`_compute_forward_outcomes_from_daily_df`) and the full-universe writer
`scripts/backfill_outcomes.py:147-208` (`_backfill_uoa_symbol_daily`, iterating **all** rows for a
date, NULL-only unless `--force`) are correct and are not the defect. Nothing about *how* a
forward return is computed changes in this brief.

---

## 3. Change — the minimal fix

Two steps. **Step A is the code fix and is unconditional. Step B is a one-off data catch-up; run
it in `--dry-run` only and hand the live command to Haci.**

### Why no feature flag

This restores intended behaviour. `app_data/jobs/triggered/nightly_pipeline/run.py:98-105` already
declares 65 sessions as the intended window, in a comment written when the bug was diagnosed;
`scripts/run_nightly_pipeline.py:104-109` already defaults to 70; the W60 sibling at `:192-209`
already hardcodes 65 in-process. The fix makes the legacy family behave the way the repo already
says it should. A flag would only give the defect a place to keep living, and CLAUDE.md rule 11
governs *new behaviour*, not the repair of a maturation job that is failing to write columns it
was written to write.

### Restatement check (read this before running Step B)

Step A changes no stored value: it only widens which rows a NULL-only job revisits.

Step B fills NULL cells and **never overwrites a non-null cell** (`force=False` is the default;
`scripts/backfill_outcomes.py:167-170` and `:801` — do not pass `--force`). `fwd_return_*` are
point-in-time close-to-close returns, so a late fill is bit-identical to what an on-time fill
would have produced; the platform already ruled this a non-restatement at
`reports/pipeline_repair.md:90-95`. **No published row-level number changes.**

What *does* move: the UOA/whale performance **aggregates** in `routers/performance.py` are means
and hit rates over whatever is currently non-null, i.e. over a biased ~5% minority of due rows.
Raising coverage to ~99% will move those aggregates. That is the repair, not a restatement — the
displayed aggregates today are a sampling artefact of the defect. The brief therefore stops short:
you run Step B **dry** and report the row counts; Haci runs the live sweep himself, or returns the
sweep to the desk as `research` if he wants the aggregate movement studied first. Step A ships
regardless.

### Step A — floor the backfill window inside the pipeline script

**File: `scripts/run_nightly_pipeline.py`.**

A1. Add module-level constants after the imports (currently `:30`, above `_run_command` at `:32`):

```python
# Legacy outcome backfill window. The backfill must keep re-visiting a signal until
# its longest horizon has elapsed (fwd_return_30d_pct on uoa_symbol_daily; the
# 60-session legacy running-max columns on the projection/SAS tables). The window
# used to come from the WebJob wrapper argument alone, and a stale deployed wrapper
# passing 4 froze maturation for months while the W60 maintainer -- whose window is
# computed HERE, in-process -- stayed healthy (reports/pipeline_repair.md:12-46).
# The floor lives in-process so no caller, stale or otherwise, can shorten it.
MIN_BACKFILL_TRADING_DAYS = 65
# Ceiling: the backfill's price frames come from
# ComprehensiveMultiTimeframeAnalyzer.get_stock_data, whose period string is resolved
# by indicator_fetcher._convert_period_to_dates (indicator_fetcher.py:2767-2782) --
# any unrecognised value, including backfill_outcomes.py's own "180d" default
# (scripts/backfill_outcomes.py:804), silently resolves to 180 CALENDAR days
# (~124 sessions). A window wider than that yields no bar for the base date and the
# row is skipped without an error. Cap so the window can never outrun the price frame.
MAX_BACKFILL_TRADING_DAYS = 100
```

A2. Extract the window resolution into a module-level, importable, side-effect-free helper — same
pattern and same reason as `build_regime_args` at `scripts/run_nightly_pipeline.py:38-57` (pinned
by a test). Place it next to `build_regime_args`:

```python
def resolve_backfill_window(backfill_end: date, requested_trading_days: int) -> tuple[date, int, bool]:
    """Return (backfill_start, effective_trading_days, was_clamped).

    The effective window is the caller's request clamped into
    [MIN_BACKFILL_TRADING_DAYS, MAX_BACKFILL_TRADING_DAYS]. Clamping is reported, never silent.
    """
    requested = max(int(requested_trading_days), 1)
    effective = min(max(requested, MIN_BACKFILL_TRADING_DAYS), MAX_BACKFILL_TRADING_DAYS)
    return subtract_trading_days(backfill_end, effective - 1), effective, effective != requested
```

A3. Replace the `else` arm at `scripts/run_nightly_pipeline.py:144-148` so it calls the helper and
prints a WARNING when it clamps. An explicit `--backfill-start-date` must still be honoured
verbatim — manual repair runs need arbitrary ranges, and the wrapper never passes it, so the floor
still binds in production:

```python
        backfill_window_days: int | None = None
        backfill_window_clamped = False
        if args.backfill_start_date:
            backfill_start = date.fromisoformat(args.backfill_start_date)
        else:
            backfill_start, backfill_window_days, backfill_window_clamped = resolve_backfill_window(
                backfill_end, args.backfill_trading_days
            )
            if backfill_window_clamped:
                print(
                    "WARNING backfill window clamped "
                    f"requested={max(int(args.backfill_trading_days), 1)} "
                    f"effective={backfill_window_days} "
                    f"min={MIN_BACKFILL_TRADING_DAYS} max={MAX_BACKFILL_TRADING_DAYS}"
                )
```

A4. Make the effective window observable, so a stale wrapper is visible on night one instead of in
three months. Add `backfill_window_trading_days={backfill_window_days}` and
`backfill_window_clamped={backfill_window_clamped}` to the `status=starting` print at
`scripts/run_nightly_pipeline.py:211-217` and to the `status=success` print at `:289-294`, and add
the same two keys to the `digest_details` dict at `:295-301` and to `failure_details` at `:325-333`.

That is the whole code change: one file, one new helper, two constants, four print/dict additions.
Do not touch `scripts/backfill_outcomes.py`, `services/uoa_screener.py`, the wrapper, or any
scoring path.

### Step A' — ops action for Haci (not code; state it in the PR description)

The floor makes the deployed *script* self-defending, so the next deploy fixes production even if
the WebJob copy stays stale. Independently, the stale wrapper should still be re-synced:
in Kudu, compare the wrapper the WebJob dashboard executes against
`wwwroot/app_data/jobs/triggered/nightly_pipeline/run.py`, delete/re-sync the stale job, restart
the app, and confirm the next nightly log prints `backfill_window_trading_days=65` (or 70) and
`backfill_window_clamped=False`. Copy the launch line into the PR.

### Step B — historical catch-up (dry-run only in this PR)

Once Step A ships, every date within 65 sessions of tonight self-heals on the next nightly run.
Dates older than that never will. As of 2026-09-11, 65 sessions back is ~2026-06-11, so the
residual hole is roughly **2026-05-11 .. 2026-06-10** plus any date the 2026-07-02 repair missed.

Run, and paste the totals block into the PR:

```
python scripts/backfill_outcomes.py --tables uoa --start-date 2026-05-11 --end-date 2026-06-10 --dry-run --verbose
```

Do **not** run it live and do **not** pass `--force`. The live command, for Haci alone, is the
same line without `--dry-run`.

---

## 4. Before / after check — fixed trading date 2026-07-28 (Tuesday)

Run all four in the platform repo, before and after the change, and paste both outputs in the PR.

**(a) The window resolution — this is what changes.**

```
python -c "import importlib.util,sys; from datetime import date; spec=importlib.util.spec_from_file_location('p','scripts/run_nightly_pipeline.py'); m=importlib.util.module_from_spec(spec); sys.modules['p']=m; spec.loader.exec_module(m); print(m.resolve_backfill_window(date(2026,7,28), 4)); print(m.resolve_backfill_window(date(2026,7,28), 70))"
```

- Before: `AttributeError: module 'p' has no attribute 'resolve_backfill_window'`.
- After: the first call returns a start date equal to `subtract_trading_days(date(2026,7,28), 64)`
  with `65, True`; the second returns `70, False`.

**(b) The outcome computation — this must NOT change.** The fix does not touch the backfill script,
so its dry-run report for the fixed date must be byte-identical before and after:

```
python scripts/backfill_outcomes.py --tables uoa --start-date 2026-07-28 --end-date 2026-07-28 --dry-run
```

The `2026-07-28: uoa X/Y updated (pop=… fut=… noP=…)` line and the COMPLETE totals block must
match exactly. If they differ, you changed something you were told not to change — stop.

**(c) The test suite:**

```
python -m pytest tests/test_nightly_pipeline_backfill_window.py tests/test_nightly_pipeline_regime_pin.py -q
```

Before: the first file does not exist. After: all pass.

**(d) The existing coverage watchdog, as narrative evidence (running it against prod is Haci's
step, not yours — run it only if you have a DB):**

```
python scripts/check_outcome_coverage.py
```

`services/outcome_coverage_monitor.py:32-46` and `:118-136` compute per-horizon coverage over due
rows with a 95% threshold; `data/outcome_coverage_report.json` is the artefact. Before: the
`uoa_symbol_daily` horizons appear in `alerts`. After the sweep and a few nights: they clear.
Whether that alert reaches anyone is PI-002 and is out of scope here.

---

## 5. Test — the test that would have caught this

New file `tests/test_nightly_pipeline_backfill_window.py`, modelled directly on
`tests/test_nightly_pipeline_regime_pin.py:24-42` (same `_load_pipeline_module` helper, same
`from user import User` mapper-registration line before the pipeline import, same `_REPO_ROOT`
bootstrap; import `subtract_trading_days` from `core.trading_days`).

```python
"""Pin test: the nightly legacy-outcome backfill window is floored IN-PROCESS.

The window used to come only from the Azure WebJob wrapper argument. A stale deployed
wrapper passing 4 froze fwd_return_5/7/14/30d maturation on uoa_symbol_daily from
2026-05-20 to at least 2026-09-10 (research PI-001; reports/pipeline_repair.md:12-46),
while the W60 maintainer -- window computed in-process -- stayed healthy. No caller may
shorten the window below the longest horizon the backfill has to reach.
"""

def test_floor_exceeds_longest_outcome_horizon():
    mod = _load_pipeline_module()
    # 60-session legacy running-max is the longest horizon the backfill must reach;
    # fwd_return_30d_pct is the shortest binding one. The floor must clear both.
    assert mod.MIN_BACKFILL_TRADING_DAYS >= 65
    assert mod.MAX_BACKFILL_TRADING_DAYS >= mod.MIN_BACKFILL_TRADING_DAYS


def test_stale_wrapper_argument_is_clamped_up():
    mod = _load_pipeline_module()
    end = date(2026, 7, 28)
    start, effective, clamped = mod.resolve_backfill_window(end, 4)   # the 2026-04-05 wrapper value
    assert effective == mod.MIN_BACKFILL_TRADING_DAYS
    assert clamped is True
    assert start == subtract_trading_days(end, mod.MIN_BACKFILL_TRADING_DAYS - 1)


def test_healthy_argument_is_passed_through():
    mod = _load_pipeline_module()
    end = date(2026, 7, 28)
    start, effective, clamped = mod.resolve_backfill_window(end, 70)
    assert (effective, clamped) == (70, False)
    assert start == subtract_trading_days(end, 69)


def test_window_cannot_outrun_the_180_calendar_day_price_frame():
    mod = _load_pipeline_module()
    _start, effective, clamped = mod.resolve_backfill_window(date(2026, 7, 28), 400)
    assert (effective, clamped) == (mod.MAX_BACKFILL_TRADING_DAYS, True)


def test_deployed_wrapper_still_requests_at_least_the_floor():
    """Contract test on the WebJob wrapper source -- the original defect, at source."""
    import ast
    src = (_REPO_ROOT / "app_data" / "jobs" / "triggered" / "nightly_pipeline" / "run.py").read_text()
    literals = [n.value for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Constant)]
    i = literals.index("--backfill-trading-days")
    requested = int(literals[i + 1])
    mod = _load_pipeline_module()
    assert requested >= mod.MIN_BACKFILL_TRADING_DAYS
```

Do not add a DB-touching test. `scripts/backfill_outcomes.py` is unchanged and is already covered
by the before/after in §4(b).

---

## 6. Rollback

```
git revert --no-edit <sha> && git push
```

One commit, one script plus one new test file. Reverting restores the wrapper-supplied window.
No data rollback exists or is needed: Step A writes nothing, and Step B (if Haci runs it) writes
only NULL cells with values that are point-in-time by construction.

---

## 7. Out of scope — do not touch

- **PI-002** — why nothing alerted. `services/outcome_coverage_monitor.py` exists and *is* wired
  into the nightly at `scripts/run_nightly_pipeline.py:249-256` via
  `scripts/check_outcome_coverage.py`, with a 95% threshold. Whether it fired and was ignored, or
  never ran, is a separate register row. Do not change the monitor, its threshold, or its routing.
- The bulletin trickle: `services/uoa_screener.py:346-353` (`max_symbols=40`), `:361-378`,
  `:1882-1910` (weekday-counted lookback arms). It is a symptom, not the defect, and changing it
  changes what the screener writes.
- `indicator_fetcher._convert_period_to_dates` (`indicator_fetcher.py:2508-2523`, `:2767-2782`)
  silently mapping unknown period strings such as `"180d"`, `"120d"`, `"90d"` to 180 calendar days.
  Real hazard, separate ticket; §3 A1 handles it defensively with `MAX_BACKFILL_TRADING_DAYS`.
- `adjustment='raw'` forward returns mis-measuring across splits
  (`indicator_fetcher.py:2857-2867`, `reports/pipeline_repair.md:85-88`). That is PI-003's family.
- `uoa_contract_daily` forward returns, and the projection/SAS legacy running-max restatement list
  (`reports/pipeline_repair.md:96-100`). Same root cause, different populations, owner decision.
- Anything in `services/super_agent_select_scoring.py`, and any selection, ranking, target, or
  published payload. No subscriber-visible copy or field changes in this PR.
- `--force`, anywhere. No non-null cell is overwritten by this work.

---

## 8. What the Data Steward runs at `/desk-run verify PI-001 <sha>`

Read-only, `$RESEARCH_DB_URL`, fixed date **2026-07-28**. Snapshot **before** Haci deploys, compare
**after** at least one post-deploy nightly run.

```sql
-- V1. Coverage on the fixed date. This is the number that must move.
SELECT count(*) AS n_rows,
       count(fwd_return_5d_pct)  AS n_5d,
       count(fwd_return_14d_pct) AS n_14d,
       count(fwd_return_30d_pct) AS n_30d
FROM uoa_symbol_daily
WHERE trading_date = DATE '2026-07-28';

-- V2. Row-level immutability. Save to CSV before and after.
SELECT symbol,
       fwd_return_1d_pct, fwd_return_3d_pct, fwd_return_5d_pct,
       fwd_return_7d_pct, fwd_return_14d_pct, fwd_return_30d_pct,
       score_day, score_swing, score_long, label_swing, oi_confirm_mult
FROM uoa_symbol_daily
WHERE trading_date = DATE '2026-07-28'
ORDER BY symbol;
-- research/reports/PI-001_before_20260728.csv / PI-001_after_20260728.csv

-- V3. The trailing frontier, to confirm it keeps moving rather than freezing again.
SELECT trading_date,
       count(*) AS n_rows,
       round(100.0 * count(fwd_return_5d_pct)  / count(*), 1) AS pct_5d,
       round(100.0 * count(fwd_return_30d_pct) / count(*), 1) AS pct_30d
FROM uoa_symbol_daily
WHERE trading_date BETWEEN DATE '2026-06-11' AND DATE '2026-08-14'
GROUP BY 1 ORDER BY 1;
```

**PASS requires all four:**

1. **V1 moves.** `n_5d`, `n_14d` and `n_30d` each rise from ~24 / ~24 / 0 to `>= 0.95 * n_rows`.
2. **V1 `n_rows` is unchanged.** The repair adds no rows and deletes none.
3. **V2 is monotone.** Every cell that was non-null in `before` is **exactly equal** in `after`;
   only null → non-null transitions are permitted, and only in the six `fwd_return_*` columns.
   `score_day`, `score_swing`, `score_long`, `label_swing`, `oi_confirm_mult` must be identical.
   Any changed non-null value is a FAIL and the PR is reverted per §6.
4. **V3 shows no cliff.** For every date in the window, `pct_5d >= 95` and — for dates at least 30
   sessions before the verify date — `pct_30d >= 95`.

Dates before 2026-06-11 only reach PASS if Haci ran the Step B live sweep; if he did not, note that
in the verify record and leave PI-001 at `IMPLEMENTED:<sha>` with a residual-hole note rather than
`VERIFIED`.

---

## 9. Addendum, 2026-09-13 — corrections after implementation (`2d5776c`)

Three corrections to this brief, established from the frozen dataset after the coding agent
reported it could not run §4(b) or Step B. Full working: `research/reports/VERIFY_PI-001.md`.

**(a) §4(b) should never have been asked of the coding agent.** Its purpose is to prove
`scripts/backfill_outcomes.py` was not modified. The commit touches two files and that is not one
of them, so `git show --stat 2d5776c` proves it without a database. A fix brief must not hand the
coding agent a DB step at all: there is one database, `$RESEARCH_DB_URL` is production separated
only by a read-only role, and the coding agent's credential on it is read-write. Recorded as DP-49
and DP-50.

**(a2) `2d5776c` is on branch `fix/pi-001-backfill-window-floor`, not on `main`.** Production still
runs `fa70688`. Nothing in §8 can be checked until the branch is merged, deployed, and one nightly
has run.

**(b) Step B's date range is wrong.** Corrected twice, then settled. `fwd_return_30d_pct` is the
only column affected, and among dates whose 30-session window had closed by the freeze `as_of`:
**35 dates and 17,402 cells sit at zero coverage** across 2026-04-15..2026-07-29, a further 15
dates are partially filled by the bulletin trickle, and **15 of the zero dates, before 2026-06-08,
can never be reached by any nightly window**. An earlier version of this addendum quoted that last
figure as the sweep scope; it is the right answer to a different question and too narrow for the
sweep, because it assumed a deploy that has not happened. Settled range, wider on purpose so the
result does not depend on deploy timing, and free because the backfill writes only NULLs:

```
python scripts/backfill_outcomes.py --tables uoa --start-date 2026-04-15 --end-date 2026-07-29 --dry-run --verbose
```

Full reconciliation in `research/reports/VERIFY_PI-001.md` §7.

**(c) The §8 before-snapshot already exists.** `research/data/v001_uoa_symbol.parquet`, sha256-pinned
in `manifest_v001.json`, holds all eleven V2 columns for 2026-01-07..2026-09-10 and shows the
predicted 24/24/24/0 on 2026-07-28. Compare V2 against it rather than taking a live CSV: immutable,
checksummed, and it predates the commit by construction.

**Also noted:** the `create_tables()` DDL at `scripts/backfill_outcomes.py:816` already runs against
production on every nightly, because `scripts/run_nightly_pipeline.py:223` invokes that script as a
subprocess each night. Running the sweep by hand adds no DDL exposure.
