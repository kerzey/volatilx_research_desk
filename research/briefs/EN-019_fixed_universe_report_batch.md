# EN-019 — multi-agent reports on a fixed, pre-declared universe, with provenance and an append-only archive

**Type:** enhancement brief, **plumbing** kind. **Ships directly under DP-59** (`research/DECISION_POLICY.md:37`):
no feature flag, no kill switch, no shadow mode, no inertness proof, no flip step returned to Haci. The build is
**always-on once deployed**; it is checked *here*, in the registers, by the Data Steward after deploy (§4.2, §8).
**Register row:** `research/ENHANCEMENTS.md` EN-019, Build = `HACI_DECIDED:build (2026-09-15)`
**Rewritten:** 2026-09-15 by the Brief Writer under DP-59, replacing the two-flag version of this brief
(research SHA `b8c1747`; the pre-DP-59 text, with every file body reproduced in full, is
`git show b8c1747:research/briefs/EN-019_fixed_universe_report_batch.md`).
**Platform repo:** `C:\Users\sahin\Projects\volatilx`, branch `feat/en-019-fixed-universe-report-batch`
**Platform SHA all `path:line` citations are taken at:** `380336725f3d8e69f977ee0e6bd11898f13bed23`
(`3803367`, merge of `main` into `feat/en-019-fixed-universe-report-batch`; the EN-019 implementation commit
already on that branch is `1463fb0`)
**Research repo SHA:** `b8c1747`
**Runtime settings — sizing only, never gates** (read from the environment at call time, clamped; every one of
them leaves a runnable job): `FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS` (80, clamped 1..120),
`FIXED_UNIVERSE_REPORT_BATCH_START_DEADLINE_ET` (21:00), `FIXED_UNIVERSE_REPORT_BATCH_STOP_ET` (22:15),
`FIXED_UNIVERSE_REPORT_BATCH_POLL_SECONDS` (60), `FIXED_UNIVERSE_REPORT_BATCH_PAUSE_SECONDS` (5).
There is **no** `FIXED_UNIVERSE_REPORT_BATCH_ENABLED` and **no** `AI_REPORT_ARCHIVE_ENABLED`; §4.1(c) greps for
both names and must find nothing. The archive container is the constant `vx-report-archive`
(`services/report_provenance.py:32`).

**What ships, in one paragraph.** The 18:30 ET WebJob runs every trading night on the fixed universe (the 20-name
stable liquid list plus that night's SAS candidates, cap 80). Every report written by any path — subscriber
`/analyze`, the ad-hoc internal batch, the fixed-universe batch — carries a `report_provenance` block
(schema `report_provenance_v1`) naming its `trigger` (`subscriber` | `internal_batch` | `fixed_universe_batch`)
and explicit ISO-8601 timestamps with an offset. The append-only archive copy is written unconditionally.

**PI-019 — fixed by this build, say so.** PI-019 raised two defects: reports do not say what triggered them, and
the report clock (`day_trading_agent.py:609`, `datetime.now().strftime('%Y-%m-%d %H:%M:%S')`) is UTC to
2026-04-05 and US Eastern from 2026-04-07 with **no zone marker**. Both are fixed forward from the deploy date by
`report_provenance`: `trigger` is the provenance defect; `technical_timestamp_iso` (the same instant with an
explicit offset), `process_utc_offset` and `analysis_completed_at_utc` are the zone defect. The fix is
**forward-only and in the archive copy**: the dated `ai-reports-YYYY-MM-DD` blob, the `_latest` pointer and the
`/analyze` response keep their zone-less `timestamp` field because Report Center, Action Center and Omega render
it (§0.2 choice 2). At a §8 PASS the Steward records PI-019 as **fixed forward at `<sha>` from `<deploy date>`**
for the research record, and asks Haci whether he also wants the display half fixed (a separate, smaller brief).
Probable cause of the switch date, located while writing this brief: the naive `datetime.now()` takes the App
Service process zone, and `WEBSITE_TIME_ZONE = America/New_York` (`docs/AZURE_WEBJOBS_AUTOMATION.md:12`, `:97`)
arrived with the WebJobs automation commits of 2026-04-05/06 (`76580a9`, `52ccbc0`) — the exact date PI-019
measured.

**DP-50(b) — ship timing, checked before writing:** see §0.1. Short form: **no database row is written or
rewritten, no dated report blob changes, no SAS input or output changes, no published number moves; no
`DATA_NOTES.md` repair-log row is required** (`research/data/DATA_NOTES.md:32-33`: forward-only additions take no
row). No locked question is constrained, so nothing delays the ship.

You are the coding agent working in the platform repo. This brief is self-contained: do not ask questions, do not
redesign, do not widen the scope. Implement §3, run §4.1, update §5, and report the SHA.

**Nothing in this brief runs against a database or a blob store (DP-49).** Your `DATABASE_URL` is the platform's
read-write role on live production (the desk's read-only role and production are the same Postgres instance).
Two specific prohibitions:

- **Do not run `pytest` in this repo.** `conftest.py:31-35` runs `create_tables()` (DDL) and the autouse fixture
  at `conftest.py:38-55` executes `db.query(User).delete()` and `db.query(UserActivityEvent).delete()` before and
  after **every test**, against whatever `DATABASE_URL` points at. Run the §5 tests as
  `python tests/test_report_provenance.py` with `DATABASE_URL` unset — that file loads no conftest.
- **Do not run `scripts/run_fixed_universe_report_batch.py` in its normal mode**, and do not start the app. The
  only execution of that script you may perform is the offline dry-run of §3.4,
  `--universe-from-json tests/fixtures/en019_universe_input.json`, which imports only the standard library and
  the pure `services.fixed_universe_batch` module, opens no connection, calls no analyzer and writes nothing.

§4.2 and §8 are the Data Steward's (read-only role, read/list blob token) and Haci's (deploy).

**Indentation:** `app.py`, `azure_storage.py`, `services/`, `scripts/` and `tests/` are 4-space indented.
(`models.py` is tab-indented; you do not touch it.)

---

## 0. Ship timing, design choices, cost

### 0.1 DP-50(b) — does this touch anything a locked question reads?

**No.** Checked against every locked question on `research/BOARD.md` (Q002–Q037) and `desk_queue.py` on 2026-09-15.

- **Database:** the batch reads `super_agent_select_runs` and `super_agent_select_candidates_daily` and writes
  **no row anywhere** — no report index (it bypasses `store_ai_report`'s `user_report_index` upsert), no digest
  ledger, no job table. Nothing in `scripts/run_nightly_pipeline.py`, the SAS engine, the ladder, the outcome
  backfills or the UOA screener changes; §4.1(b) proves the diff there is empty.
- **Blobs a PREREG could read:** the only blob object a locked PREREG touches is the SAS report's
  `technical_snapshot` / lane targets via `sas_selection_excursion` (Q004 §4, `services/sas_excursion.py:335-354`),
  written by `store_super_agent_select_report` (`azure_storage.py:790`). It is untouched, and the SAS caller
  passes none of the new keyword arguments (`record_plan_sources`, `numeric_trigger_contract`), which default to
  the old behaviour.
- **No F9 question is registered** (`research/questions/DEFERRED.md` H-086..H-094, all deferred on exactly this
  collection). H-093 would read this collection; it constrains nothing here.
- **Shared resources on the pick night:** the batch waits for the nightly pipeline to record that it has finished
  before it starts (§0.2 choice 5), so it never competes with `backfill_outcomes` / `backfill_w60_outcomes` for
  Alpaca bars. `indicator_fetcher.py` has no 429 handling, so contention would surface as silent fetch failures
  in outcome maturation — the thing locked questions read. The wait is the protection, and it is not optional.

**Repair log:** no row. **Data note:** at a §8 PASS the Steward adds a dated note (not a repair-log row) naming
the first declared night, the archive container, `fixed_universe_v1` and the ship SHA, because H-086's re-entry
trigger (1) starts the F9 window at that date.

### 0.2 Design choices — what was chosen, and why

1. **Fixed-universe reports go to a separate, non-dated archive container only** — never to
   `ai-reports-YYYY-MM-DD`, never a `_latest` pointer, never `user_report_index`. Writing ~230 blobs a night into
   the dated containers would change subscriber surfaces: Omega's report tool lists **all users'** blobs for a
   symbol and date when `access_scope="all"` (`ai_agents/omega_agent.py` → `azure_storage.py`, capped at 120
   reports, so research blobs would crowd subscriber blobs out of Omega's context), and user 1's Report Center /
   Action Center would switch to research reports. The container name does not start with `ai-reports`, so a
   lifecycle rule written for the dated containers cannot match it (`docs/SAS_EXCURSION_BACKFILL.md:50-52`
   records a report blob that "aged out of its dated container").
2. **Provenance is stamped on the archive copy, not on the dated blob.** The dated history blob, the `_latest`
   pointer, the `ai-reports-jobs` result, the `/api/ai-analysis-result` poll and the `/analyze` response
   (`app.py:3644`) keep their exact current shape. This is a design choice, not a flag: the archive is the
   research record, the dated blob is the product surface. The cost is that PI-019 is fixed for the record and
   not for displays (header).
3. **The numeric trigger contract (`trigger_price` / `trigger_direction` / `trigger_basis`) is requested only by
   the fixed-universe batch**, through the per-call keyword `numeric_trigger_contract=True`. It is a prompt
   addition (`ai_agents/principal_agent.py`), and a prompt change alters LLM output for whoever receives it;
   subscribers and SAS reports keep today's prompt. This keyword is a **parameter of one caller**, not a config
   gate — no environment variable reads it, and no deployment step sets it. Consequence H-094 must name at
   re-entry: research plans are generated with three extra prompt lines, so they are the subscriber plan's
   closest sibling, not the identical object. Nothing parses the trigger sentence (rule 9).
4. **Universe `fixed_universe_v1`** = a pinned list of 20 large, liquid S&P 500 common stocks, then every
   candidate of the night's SAS run, capped at `max_symbols`. Order: liquid list as written → published picks
   (`qualified`) by `selected_rank` → unpublished candidates by `overall_score` descending; the cap can only drop
   the lowest-scored unpublished candidates. No crypto, no ETFs. The list was fixed without reading any report or
   outcome; a different list is a new universe id (`fixed_universe_v2`), never an edit
   (`services/fixed_universe_batch.py:22-28`).
5. **Clock:** WebJob at **18:30 ET** Mon–Fri. It then waits until the scheduler digest records the nightly
   pipeline as `success` or `failed`; if that has not happened by the start deadline (**21:00 ET**) the night is
   **skipped and recorded**, never run on a different clock or universe. It stops *starting* new symbols at
   **22:15 ET**, ahead of the in-process UOA slot at 22:30 (`services/uoa_scheduler.py:181`). Why 18:30: since
   2026-06-09, 63 of 65 SAS runs in the pinned freeze finished the same evening between 17:05 and **17:46 ET**
   (`research/data/v001_sas_runs.parquet`, manifest_v001; the other two finished the next day). 18:30 clears the
   latest same-day finish by 44 minutes.
6. **Knowledge time:** SAS candidates enter the universe only from a run whose status is `success` and whose
   `finished_at` is at or before the declaration time; the declaration (symbols, order, sha256, SAS run id and
   finish time) is written to the archive **before the first analysis starts**. On a night SAS is unavailable the
   liquid list still runs and the declaration says `sas_component: "unavailable"` with the reason, so a PREREG
   can filter those nights out.
7. **Analysis shape:** principal agent on, all three lanes in one unscoped call, 7 timeframes (15m…1mo), AI
   summary off, earnings agent off, raw results off. One analysis writes up to three lane blobs, so manifests
   count **analyses by `job_id`**, not blobs.
8. **No writes outside the archive container:** no database row, no email, no scheduler-digest entry. Operations
   visibility is the WebJob log (30-second heartbeat, so the triggered WebJob idle timeout cannot kill a silent
   LLM call) plus the `_declared_` / `_completed_` / `_skipped_` manifests.
9. **`user_id` on fixed-universe payloads stays `1`** (the internal batch identity) for continuity;
   `report_provenance.trigger` is what distinguishes them.

### 0.3 Volume and cost

Universe size, from the pinned freeze over the 65 nights 2026-06-09..2026-09-10 (`v001_sas_candidates.parquet`,
distinct symbols per `trading_date`, union with the 20-name list): candidates per night median 62 (47–68);
overlap with the liquid list median 4 (1–9); **union median 77, range 65–83**; the cap of 80 binds on 10 of 65
nights.

Per analysis: three LLM calls — technical and price-action summaries on `gpt-5.4-nano`, principal on
`gpt-5.6-terra`, reasoning low, ≤ 3,200 output tokens — plus ~8 Alpaca bar fetches. At ~77 analyses a night:
**~230 LLM calls and ~230 report blobs a night, ~1,600 analyses and ~4,800 LLM calls a month**, roughly 50× the
current multi-agent report volume (697 blobs over ~8 months,
`research/reports/STEWARD_F9_blob_inventory.md` §1). Token volume is an estimate (~25–35k input and ~4–5k output
tokens per analysis); the completed manifest records the principal call's `usage.total_tokens` summed per night,
so Haci has the real figure after night one.

Calls are strictly sequential with a 5-second pause — a few requests a minute, far below any tier's RPM. Runtime
45–120 s per analysis → 1–2.5 h for 77 symbols; the 22:15 stop bounds the night at 3 h 45 m from an 18:30 start,
and symbols not started are recorded. **This is where the sizing settings earn their place: if the spend is more
than he wants, set `FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS=40` and each night still carries the ≥ 3 same-day
controls H-086 names, because the published picks sit ahead of the cut.** Sizing it down is not switching it off;
there is no off.

---

## 1. What is missing, and the evidence

The multi-agent technical reports exist but cannot decide any question, historically or going forward
(`research/reports/STEWARD_F9_blob_inventory.md`, counts and metadata only, 2026-09-14):

- **Selection.** 697 history blobs over 120 days; **73.6% (513) come from the internal batch account
  `user_id = 1`** re-running a hand-picked list; seven symbols are 60% of the corpus, TSLA alone 134. The same
  symbol is re-run within 5 trading days on 56.5% of symbol-days. There is no fixed universe, so no night has its
  own distance-matched controls.
- **No provenance.** Neither the blob name nor the payload says whether a report came from `/analyze`
  (`app.py:3351`, the subscriber's `user_id`) or `/api/internal/batch-analyze` (`app.py:3938`, `user_id=1`
  hard-coded) — PI-019.
- **Zone-less clock.** `timestamp` is UTC to 2026-04-05 and US Eastern from 2026-04-07 with no marker — PI-019.
- **Blob counts are not analysis counts.** One analysis writes one blob **per lane**, a single blob only on the
  no-lane fallback, so every F9 floor was counted in the wrong unit (DEFERRED.md H-094 (c)).
- **The GPT plan's trigger is free text** (`"trigger": "string"`, `ai_agents/principal_agent.py`) — ungradeable
  without a parser rule 9 forbids (H-094 (a)).
- **Fallback plans are indistinguishable from LLM plans.** `_fallback_strategies_from_experts` writes a symmetric
  ±0.5% / ±1.0% template, identical for all three lanes, and no field says which path ran (H-094 (b)).
- **Retention is unproven.** Dated containers are the only store, and a sibling blob is documented as having aged
  out of one (`docs/SAS_EXCURSION_BACKFILL.md:50-52`); the desk's data-plane token cannot see a lifecycle policy.

### Reproducing check — **Data Steward only**, read/list blob token, counts only

Not for the coding agent (DP-49). Re-run inventory §3's count over the last 20 dated containers: history blobs
(exclude `_latest.json` and `SAS_` names) grouped by the `_<user_id>_` token in the blob name. Expected before
deploy: `user_id = 1` is the largest single contributor, and no blob payload has a `report_provenance` key or any
`trigger` field.

---

## 2. Cause — the code paths

- **No schedule, no universe (before this build).** The only multi-symbol path was the HTTP endpoint
  `app.py:3938`: a caller POSTs ≤ 25 symbols, the work runs as a web-process background task over an in-memory
  job store. Nothing called it on a clock; `docs/AZURE_WEBJOBS_AUTOMATION.md` listed no report job. What got
  analysed was whatever the operator typed.
- **Provenance was dropped at the write.** `_run_and_persist_expert_analysis` (`app.py:284`) knew its caller only
  through `user_id` and passed nothing else to `store_ai_report` (`azure_storage.py:558`), which enriched with
  `symbol`, `user_id`, `stored_at`, `strategy_scope` only.
- **The zone.** `analysis_output["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')`
  (`day_trading_agent.py:609`), exported unchanged; the `/analyze` response repeats a naive clock
  (`app.py:3644`, `str(datetime.now())`).
- **Plan provenance.** `_summarise_node` (`ai_agents/principal_agent.py`) replaces missing lanes with the
  template and builds `plan` without recording which lanes were replaced.
- **Retention.** Only dated containers existed, written by UTC day of the write.

---

## 3. Change — always-on

### 3.0 Starting point: what already exists at `3803367`

Commit `1463fb0` on `feat/en-019-fixed-universe-report-batch` already implements most of this build, and the
archive copy is **already unconditional** (`azure_storage.py:623-629` calls `_write_report_archive_copy` with no
condition; `AI_REPORT_ARCHIVE_ENABLED` no longer exists anywhere in the tree). These files exist and their
contracts are correct as written — do not redesign them:

| file | what it holds | status |
|---|---|---|
| `services/report_provenance.py` | schema `report_provenance_v1`, trigger constants, ISO/offset helpers, `build_report_provenance`, the numeric trigger contract, `archive_blob_name` | keep; **§3.2 only** |
| `services/fixed_universe_batch.py` | `LIQUID_LIST_V1` (`:24-28`), `declare_universe`, blob names, pipeline gate, manifest summaries | keep; **§3.1 and §3.3 only** |
| `azure_storage.py:531-556`, `:558-563`, `:623-629`, `:691-788` | archive copy, `store_ai_report(..., archive_provenance=...)`, `store_report_archive_blob`, `list_report_archive_blob_names`, `store_fixed_universe_report` | keep; **§3.2 only** |
| `app.py:284-300`, `:509-520`, `:546`, `:558`, `:561-565`, `:571-588`, `:3761-3936` | the `trigger` / `report_sink` / `numeric_trigger_contract` parameters, `_provenance()` (already unconditional), `report_provenance_summary`, `run_batch_analysis_for_symbol` | keep; **§3.2 only** |
| `scripts/run_fixed_universe_report_batch.py` | the nightly job | **§3.1 and §3.4** |
| `app_data/jobs/triggered/fixed_universe_report_batch/` | `settings.job` + `run.py` | keep as is (§3.7) |
| `tests/test_report_provenance.py` | 11 offline checks | **§5** |
| `docs/AZURE_WEBJOBS_AUTOMATION.md:23`, `docs/FIXED_UNIVERSE_REPORT_BATCH.md` | the two doc entries | **§3.8** |

What remains is the DP-59 delta, §3.1–§3.8. If the branch is ever discarded and you are starting from `c311e81`,
the full file bodies are in the desk's git history —
`git show b8c1747:research/briefs/EN-019_fixed_universe_report_batch.md` — apply them with §3.1–§3.4 folded in,
and ignore every flag and inertness section there.

### 3.1 Delete the kill switch — there is no gate

**(a) `services/fixed_universe_batch.py`.** Delete `_OFF` (`:44`) and the whole `batch_enabled()` function
(`:48-51`). Keep `import os` — §3.3 uses it.

**(b) `scripts/run_fixed_universe_report_batch.py`.** Delete the module-level import
`from services.fixed_universe_batch import batch_enabled` (`:27`) and replace `main()` (`:49-53`) with §3.4's
version. In the module docstring (`:1-11`) replace lines 3–5 with:

```
Always on (DP-59): there is no enable flag and no kill switch. Size the night with
FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS / _PAUSE_SECONDS; never switch it off.
The offline dry-run --universe-from-json PATH resolves and prints a universe from a JSON file:
standard library plus services.fixed_universe_batch only, no database, no Azure, no analyzer.
```

After this, `git grep -n FIXED_UNIVERSE_REPORT_BATCH_ENABLED` must return nothing (§4.1(c)).

### 3.2 Rename the trigger value to `fixed_universe_batch`

The three trigger values are exactly `subscriber`, `internal_batch`, `fixed_universe_batch`. Rename the constant
and its value everywhere; nothing else about the schema changes (`report_provenance_v1` stays, no key is added or
removed). No stored data is affected: nothing has yet been written with the old value.

- `services/report_provenance.py:21-22`:
  `TRIGGER_FIXED_UNIVERSE_BATCH = "fixed_universe_batch"` and
  `TRIGGERS = (TRIGGER_SUBSCRIBER, TRIGGER_INTERNAL_BATCH, TRIGGER_FIXED_UNIVERSE_BATCH)`.
- `azure_storage.py:19` (import), `:753` (the sink's guard), `:756` (the log line — say
  `no fixed_universe_batch provenance`).
- `app.py:129` (import), `:561` (`if trigger == TRIGGER_FIXED_UNIVERSE_BATCH:`).
- `scripts/run_fixed_universe_report_batch.py:94` (import), `:207` (`"trigger": ...` in the declaration),
  `:275` (`trigger=...` passed to `run_batch_analysis_for_symbol`).
- `tests/test_report_provenance.py:394`, and anywhere else the literal appears (§5).
- `docs/FIXED_UNIVERSE_REPORT_BATCH.md:29` (§3.8).

`git grep -n scheduled_fixed_universe` must return nothing afterwards (§4.1(c)).

### 3.3 Sizing settings stay settings

Replace `batch_settings()` (`services/fixed_universe_batch.py:53-61`) with an environment-read, clamped version.
These size the job; none of them can stop it — every value is clamped into a runnable range, and an unparseable
or hostile value falls back to the default.

```python
_HHMM = re.compile(r"(\d{1,2}):(\d{2})")
MAX_SYMBOLS_CEILING = 120


def _int_env(name: str, default: int, lo: int, hi: int) -> int:
    raw = (os.getenv(name, "") or "").strip()
    try:
        value = int(raw) if raw else default
    except ValueError:
        value = default
    return max(lo, min(hi, value))


def _time_env(name: str, default: time) -> time:
    match = _HHMM.fullmatch((os.getenv(name, "") or "").strip())
    if not match:
        return default
    hour, minute = int(match.group(1)), int(match.group(2))
    if 0 <= hour <= 23 and 0 <= minute <= 59:
        return time(hour, minute)
    return default


def batch_settings() -> Dict[str, Any]:
    """Sizing knobs, read per call. None of these is a gate: max_symbols clamps to >= 1, so no
    setting can stop the batch (DP-59 - the job is always on; size it, never switch it off)."""
    return {
        "max_symbols": _int_env(
            "FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS", DEFAULT_MAX_SYMBOLS, 1, MAX_SYMBOLS_CEILING
        ),
        "start_deadline_et": _time_env(
            "FIXED_UNIVERSE_REPORT_BATCH_START_DEADLINE_ET", DEFAULT_START_DEADLINE_ET
        ),
        "stop_et": _time_env("FIXED_UNIVERSE_REPORT_BATCH_STOP_ET", DEFAULT_STOP_ET),
        "poll_seconds": _int_env("FIXED_UNIVERSE_REPORT_BATCH_POLL_SECONDS", DEFAULT_POLL_SECONDS, 15, 900),
        "pause_seconds": _int_env("FIXED_UNIVERSE_REPORT_BATCH_PAUSE_SECONDS", DEFAULT_PAUSE_SECONDS, 0, 120),
    }
```

`settings_for_manifest` (`:64-65`) is unchanged, so every night's `_declared_` manifest records the sizes it ran
with. `re`, `os`, `time`, `Dict` and `Any` are already imported at `:9-16`.

### 3.4 The batch runs unconditionally; the only dry-run is offline

Replace `main()` (`scripts/run_fixed_universe_report_batch.py:49-53`) and add `_print_universe_from_json`
directly below it. Add `date` to the module's datetime import (`:19` becomes
`from datetime import date, datetime, timezone`). `_run()` is otherwise unchanged — including its existing
`--declare-only` flag, which stays as the **Steward's / Haci's** tool (it reads the database) and is never run by
the coding agent.

```python
def main(argv: Optional[List[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--universe-from-json" in args:
        return _print_universe_from_json(args)
    return _run(args)


def _print_universe_from_json(argv: List[str]) -> int:
    """Offline dry-run: resolve and print a universe from a JSON file, then exit.

    No database, no Azure, no analyzer, no LLM call, no write. Imports only the standard library
    and the pure services.fixed_universe_batch module. This is the one execution of this script a
    coding agent may run (DP-49); every other mode reads production.
    """
    import argparse
    import json

    from services.fixed_universe_batch import declare_universe

    parser = argparse.ArgumentParser(description="EN-019 offline universe dry-run")
    parser.add_argument("--universe-from-json", required=True, metavar="PATH")
    args = parser.parse_args(argv)
    with open(args.universe_from_json, encoding="utf-8") as handle:
        body = json.load(handle)

    def _aware(text: Any) -> datetime:
        return datetime.fromisoformat(str(text).replace("Z", "+00:00"))

    sas_run = body.get("sas_run")
    if isinstance(sas_run, dict) and sas_run.get("finished_at_utc"):
        sas_run = {**sas_run, "finished_at_utc": _aware(sas_run["finished_at_utc"])}
    declaration = declare_universe(
        trading_date=date.fromisoformat(str(body["trading_date"])),
        declared_at_utc=_aware(body["declared_at_utc"]),
        sas_run=sas_run,
        sas_candidates=body.get("candidates") or [],
        max_symbols=int(body.get("max_symbols") or 80),
    )
    print(json.dumps(declaration, indent=2, default=str))
    return 0
```

**New file `tests/fixtures/en019_universe_input.json`** — the same rows unit test T6 already uses, so the dry-run
and the test assert the same universe and the same sha256:

```json
{
  "trading_date": "2026-09-11",
  "declared_at_utc": "2026-09-11T22:30:00Z",
  "max_symbols": 80,
  "sas_run": {"id": 4242, "status": "success", "finished_at_utc": "2026-09-11T21:12:36Z"},
  "candidates": [
    {"symbol": "SNDK", "overall_score": 91.2, "qualified": true, "selected_rank": 1},
    {"symbol": "NVDA", "overall_score": 90.4, "qualified": true, "selected_rank": 2},
    {"symbol": "wdc ", "overall_score": 88.0, "qualified": true, "selected_rank": null},
    {"symbol": "MU", "overall_score": 79.5, "qualified": false, "selected_rank": null},
    {"symbol": "QCOM", "overall_score": null, "qualified": false, "selected_rank": null},
    {"symbol": "AMD", "overall_score": 84.1, "qualified": false, "selected_rank": null},
    {"symbol": "AAPL", "overall_score": 70.0, "qualified": false, "selected_rank": null},
    {"symbol": "", "overall_score": 99.0, "qualified": true, "selected_rank": 3}
  ]
}
```

Expected output: 25 symbols — the 20 liquid names in list order, then `SNDK`, `WDC`, `AMD`, `MU`, `QCOM` — with
`"sas_component": "ok"` and
`"symbols_sha256": "ae6f22bab4a5d9d08a3718d321ba88c8c2ad7f0d1dbb8afff6058860204440d1"`. If the hash differs, the
ordering rule was implemented differently from `declare_universe` — fix the code, not the fixture.

### 3.5 Provenance on every report — restated, because it is now unconditional

No code change beyond §3.2; this is the contract the Steward checks and the docs describe.

- `store_ai_report` (`azure_storage.py:558`) writes the dated history blob exactly as before, then **always**
  writes the archive copy (`:623-629` → `_write_report_archive_copy`, `:531-556`) at
  `reports/<UTC date>/<trigger>/<history blob name>` in `vx-report-archive`. The archive body is the dated
  payload **plus one trailing key**, `report_provenance`; the archive write is wrapped so it can never break the
  report write (`:553-556`).
- A caller that passes no `archive_provenance` still gets an archive copy, stamped
  `{"schema": "report_provenance_v1", "trigger": null, "unstamped": true}`. That marker is how the Steward finds
  any report path this build missed (§8 V8).
- `app.py:509-520` builds the provenance block for every report path with no condition on it, and both principal
  calls pass `record_plan_sources=True` (`app.py:375`, `:415`), so `plan_source` / `plan_sources` are present on
  every lane blob. The SAS report service passes neither keyword and is unaffected.
- `report_provenance` fields: `schema`, `trigger`, `job_id`, `report_status`, `strategy_scope`, `blobs_in_job`,
  `lane_keys_in_job`, `plan_source`, `plan_sources`, `technical_timestamp_raw` (the zone-less engine clock, kept
  verbatim), `technical_timestamp_iso` (**explicit ISO-8601 with offset**), `process_utc_offset`,
  `analysis_completed_at_utc` (ISO-8601 `Z`). Fixed-universe reports add `universe_id`, `universe_run_id`,
  `trading_date`, `universe_sources`, `numeric_trigger_contract`. `build_report_provenance` raises `ValueError`
  on an unknown trigger or an unknown extra key — the schema cannot drift silently.

### 3.6 The fixed-universe sink — restated

`store_fixed_universe_report` (`azure_storage.py:740-788`) writes to `vx-report-archive` under
`fixed_universe/<trading_date>/<SYMBOL>_<lane>_<UTC stamp>_<job_id>.json`, append-only (`overwrite=False`, with a
collision suffix), and **refuses** any payload whose provenance is not `trigger = "fixed_universe_batch"` with a
`trading_date`. It writes no dated container, no `_latest` pointer and no `user_report_index` row.

### 3.7 WebJob / cron entry — unchanged

`app_data/jobs/triggered/fixed_universe_report_batch/settings.job`, as it already is at `3803367`:

```json
{
  "schedule": "0 30 18 * * 1-5",
  "is_singleton": true,
  "stopping_wait_time": 60,
  "shutdownGraceTimeLimit": 1800
}
```

Cron is interpreted in `WEBSITE_TIME_ZONE = America/New_York` (`docs/AZURE_WEBJOBS_AUTOMATION.md:12`), so 18:30 is
Eastern in both EDT and EST. `run.py` (a copy of the `nightly_pipeline` wrapper pointing at
`scripts/run_fixed_universe_report_batch.py`) is unchanged.

### 3.8 Docs

**(a) `docs/AZURE_WEBJOBS_AUTOMATION.md:23`** — replace the row with:

```markdown
| `fixed_universe_report_batch` | `0 30 18 * * 1-5` | 18:30 | `scripts/run_fixed_universe_report_batch.py` | Always on; no flag, no kill switch (DP-59). Size it with `FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS` (80, clamped 1..120) and `..._PAUSE_SECONDS`. EN-019 research batch: multi-agent reports on a fixed, pre-declared universe, archive container `vx-report-archive` only; waits for the nightly pipeline, writes no DB row. See `docs/FIXED_UNIVERSE_REPORT_BATCH.md` |
```

**(b) `docs/FIXED_UNIVERSE_REPORT_BATCH.md`** — three edits:

- Replace lines 5–7 (`## What runs` and the kill-switch sentence) with:

```markdown
## What runs
WebJob `fixed_universe_report_batch`, 18:30 ET Mon–Fri. **Always on: no enable flag, no kill switch.** The
settings below size the night; none of them can stop it (`FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS` clamps to
1..120, default 80; `..._START_DEADLINE_ET` 21:00; `..._STOP_ET` 22:15; `..._POLL_SECONDS` 60;
`..._PAUSE_SECONDS` 5). Offline dry-run: `python scripts/run_fixed_universe_report_batch.py
--universe-from-json tests/fixtures/en019_universe_input.json` prints a universe and exits, touching no database.
```

- Line 29: `` `trigger` (`subscriber` | `internal_batch` | `fixed_universe_batch`) ``.
- Append at the end of the `report_provenance` section:

```markdown
This block is what closes PI-019 forward from the deploy date: `trigger` says which path wrote the report, and
`technical_timestamp_iso` / `process_utc_offset` / `analysis_completed_at_utc` are explicit ISO-8601 with an
offset. The legacy zone-less `timestamp` stays in the dated blob and in the `/analyze` response because Report
Center, Action Center and Omega render it; the archive copy is the unambiguous record.
```

---

## 4. Before / after check

### 4.1 Repository check — the coding agent runs this, from the repository alone

`DATABASE_URL` must be unset in the shell for every command
(PowerShell: `Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue`). Paste all outputs into the PR.

**(a) The touched-file list is exactly the allowed list.**

```
git diff --stat 3803367..HEAD
```

Exactly these 9 paths and nothing else: `services/fixed_universe_batch.py`, `services/report_provenance.py`,
`scripts/run_fixed_universe_report_batch.py`, `app.py`, `azure_storage.py`, `tests/test_report_provenance.py`,
`tests/fixtures/en019_universe_input.json`, `docs/AZURE_WEBJOBS_AUTOMATION.md`,
`docs/FIXED_UNIVERSE_REPORT_BATCH.md`.

**(b) The nightly pipeline, SAS and subscriber surfaces are untouched** — the diff proves it directly, needs no
database, and cannot be fooled by a flaky fetch:

```
git diff --quiet 3803367..HEAD -- scripts/run_nightly_pipeline.py app_data/jobs day_trading_agent.py indicator_fetcher.py symbol_map.py services/super_agent_select_report_service.py services/super_agent_select_service.py services/job_notifications.py services/uoa_scheduler.py ai_agents routers templates static models.py db.py conftest.py core && echo UNCHANGED
```

Must print `UNCHANGED`. (`ai_agents/principal_agent.py` was changed by `1463fb0`, which is already in the base of
this diff; this step changes it no further.)

**(c) No flag name and no old trigger value survives.**

```
git grep -n "FIXED_UNIVERSE_REPORT_BATCH_ENABLED\|AI_REPORT_ARCHIVE_ENABLED\|batch_enabled\|scheduled_fixed_universe" -- . ; echo "exit=$?"
```

Must print nothing but `exit=1` (git grep exits 1 when it finds no match). Any hit is a leftover gate or a stale
trigger string.

**(d) The pure modules import nothing heavy, and the triggers are the three named values.**

```
python -c "import os,sys; [os.environ.pop(k) for k in list(os.environ) if k.startswith(('FIXED_UNIVERSE_REPORT_BATCH_','DATABASE_URL'))]; import services.report_provenance as p, services.fixed_universe_batch as f; assert p.TRIGGERS == ('subscriber','internal_batch','fixed_universe_batch'), p.TRIGGERS; assert f.batch_settings()['max_symbols'] == 80; assert not {'db','models','app','azure_storage','sqlalchemy'} & set(sys.modules), sorted({'db','models','app','azure_storage','sqlalchemy'} & set(sys.modules)); print('EN-019 pure modules OK; triggers', p.TRIGGERS)"
```

**(e) Offline universe dry-run — lists the universe, calls no analyzer, opens no connection.**

```
python scripts/run_fixed_universe_report_batch.py --universe-from-json tests/fixtures/en019_universe_input.json
```

Must print a JSON declaration with 25 symbols (the 20 liquid names in order, then `SNDK`, `WDC`, `AMD`, `MU`,
`QCOM`), `"sas_component": "ok"` and
`"symbols_sha256": "ae6f22bab4a5d9d08a3718d321ba88c8c2ad7f0d1dbb8afff6058860204440d1"`. Test T2 (§5) asserts that
the same run imports none of `app`, `models`, `azure_storage`, `dotenv`, `ai_agents.principal_agent`,
`core.market_sessions`, `sqlalchemy`.

**(f) The unit tests.**

```
python tests/test_report_provenance.py
```

Must print `EN-019: 11/11 checks passed`. Do **not** run `python -m pytest` (header). If you have a disposable
scratch `DATABASE_URL` you may run the full suite against it and say so in the PR; otherwise state that you
skipped it and why.

### 4.2 After deploy — the Data Steward's check, read-only

Run at `/desk-run verify EN-019 <sha>`, on the read-only role and the read/list blob token, after the first
trading night following the deploy. Three headline checks; §8 is the full protocol.

1. **The first night's archive container lists ≥ N provenance-stamped fixed-universe reports.** N is that night's
   `n_declared` from `vx-report-archive/fixed_universe/<N>/_declared_<run_id>.json` — **20 on a night SAS was
   unavailable, 65–80 otherwise**. Report blobs under `fixed_universe/<N>/` (names not starting with `_`) equal
   the `_completed_` manifest's `n_report_blobs_expected`; distinct `job_id` equals `n_analyses`; every blob's
   `report_provenance.trigger` is `"fixed_universe_batch"`. Floor for PASS: distinct symbols with at least one
   report blob ≥ 0.8 × N, with every shortfall explained by the completed manifest's `status_counts`.
2. **`/analyze` reports also carry provenance.** For the subscriber and ad-hoc reports written that night, an
   archive copy exists at `reports/<UTC date>/<trigger>/<history blob name>`, its `report_provenance.trigger` is
   `subscriber` or `internal_batch` (never `null`, never `unstamped`), and stripping `report_provenance` from the
   archive body reproduces the dated blob's bytes exactly.
3. **The timestamp offset is present.** Every report's `technical_timestamp_iso` matches
   `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$`, and `process_utc_offset` is `-04:00` in EDT (`-05:00`
   in EST) on 100% of reports. That is PI-019's zone defect, closed forward.

---

## 5. Tests — `tests/test_report_provenance.py`

The file already holds 11 offline checks and must keep holding 11. Three edits; every other check stays as it is,
including T9 (the dated history blob's exact bytes, and that the archive copy is those bytes plus one key) and
T11 (the principal agent's default call versus the fixed-universe call that asks for the numeric trigger
contract — two argument values of one function, not a flag pair).

**(a) Header.** Add `import contextlib` and `import io`. Rename `_clear_flags` to `_clear_settings` (same body —
it clears the `FIXED_UNIVERSE_REPORT_BATCH_` sizing settings) and update its call sites. Drop the `AI_REPORT_`
prefix from `_ENV_PREFIXES`; nothing reads it any more.

**(b) Replace T1** (`:122-142`) — settings are settings, not gates:

```python
def test_t1_sizing_settings_are_settings_not_gates():
    _clear_settings()
    from services.fixed_universe_batch import batch_settings
    from services.report_provenance import ARCHIVE_CONTAINER, TRIGGERS

    assert TRIGGERS == ("subscriber", "internal_batch", "fixed_universe_batch")
    assert ARCHIVE_CONTAINER == "vx-report-archive"
    assert not ARCHIVE_CONTAINER.startswith("ai-reports")
    defaults = {"max_symbols": 80, "start_deadline_et": time(21, 0), "stop_et": time(22, 15),
                "poll_seconds": 60, "pause_seconds": 5}
    assert batch_settings() == defaults

    os.environ["FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS"] = "40"
    os.environ["FIXED_UNIVERSE_REPORT_BATCH_PAUSE_SECONDS"] = "12"
    os.environ["FIXED_UNIVERSE_REPORT_BATCH_STOP_ET"] = "21:45"
    sized = batch_settings()
    assert (sized["max_symbols"], sized["pause_seconds"], sized["stop_et"]) == (40, 12, time(21, 45))

    # No setting can stop the batch: junk falls back, extremes clamp, max_symbols never reaches 0.
    for raw in ("0", "-5", "999", "off", "", "  "):
        os.environ["FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS"] = raw
        assert 1 <= batch_settings()["max_symbols"] <= 120, raw
    os.environ["FIXED_UNIVERSE_REPORT_BATCH_STOP_ET"] = "25:00"
    assert batch_settings()["stop_et"] == time(22, 15)
    _clear_settings()
```

**(c) Replace T2** (`:144-159`) — the offline dry-run is database-free, analyzer-free, and reproduces the
universe:

```python
def test_t2_offline_universe_dry_run_opens_no_database():
    _clear_settings()
    spec = importlib.util.spec_from_file_location(
        "en019_batch_script", _REPO_ROOT / "scripts" / "run_fixed_universe_report_batch.py"
    )
    module = importlib.util.module_from_spec(spec)
    before = set(sys.modules)
    spec.loader.exec_module(module)
    fixture = _REPO_ROOT / "tests" / "fixtures" / "en019_universe_input.json"
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        assert module.main(["--universe-from-json", str(fixture)]) == 0
    printed = json.loads(buffer.getvalue())
    assert printed["symbols"] == list(_LIQUID) + ["SNDK", "WDC", "AMD", "MU", "QCOM"]
    assert printed["symbols_sha256"] == "ae6f22bab4a5d9d08a3718d321ba88c8c2ad7f0d1dbb8afff6058860204440d1"
    assert printed["sas_component"] == "ok" and printed["universe_id"] == "fixed_universe_v1"
    forbidden = {"app", "models", "azure_storage", "dotenv", "ai_agents.principal_agent",
                 "core.market_sessions", "sqlalchemy"}
    newly = set(sys.modules) - before
    assert not (newly & forbidden), sorted(newly & forbidden)
    assert sys.modules["db"] is _DB_STUB
```

Keep T2 first in `_CHECKS` (`:450-462`) — it must run before anything else has imported the heavy modules — and
rename both entries there to match.

**(d) Trigger string.** In T10 (`:382-405`, literal at `:394`) and anywhere else,
`"scheduled_fixed_universe"` becomes `"fixed_universe_batch"`. T10 keeps asserting that the sink **refuses** a
payload stamped `internal_batch` and one with no provenance at all, and writes only to `vx-report-archive`.

The universe fixture rows are the synthetic set already in T6 (plumbing: no report, candidate row or outcome from
the desk's frozen data is used). The SNDK levels 1638.36 / 1624.55 in T5 and T11 are the illustrative sample
quoted in `research/BACKLOG.md` F9.

### Acceptance criteria — numbered and verifiable; what the PR must report

1. `git grep` for `FIXED_UNIVERSE_REPORT_BATCH_ENABLED`, `AI_REPORT_ARCHIVE_ENABLED`, `batch_enabled` and
   `scheduled_fixed_universe` returns **no hits** (§4.1(c) output pasted). There is no flag, no kill switch and
   no environment variable that can prevent the batch from running or the archive from being written.
2. `services.report_provenance.TRIGGERS == ("subscriber", "internal_batch", "fixed_universe_batch")`
   (§4.1(d) output pasted).
3. `batch_settings()` returns the documented defaults with no environment set, honours
   `FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS=40`, and clamps `0`, `-5`, `999` and `off` into `1..120` (T1 passes).
4. The offline dry-run of §4.1(e) prints 25 symbols and
   `symbols_sha256 = ae6f22bab4a5d9d08a3718d321ba88c8c2ad7f0d1dbb8afff6058860204440d1`, having imported none of
   `app`, `models`, `azure_storage`, `dotenv`, `ai_agents.principal_agent`, `core.market_sessions`, `sqlalchemy`
   (T2 passes). Output pasted.
5. `python tests/test_report_provenance.py` prints `EN-019: 11/11 checks passed`, and the PR states that
   `pytest` was not run against a real database.
6. §4.1(a) lists exactly the 9 paths; §4.1(b) prints `UNCHANGED`.
7. `docs/AZURE_WEBJOBS_AUTOMATION.md` and `docs/FIXED_UNIVERSE_REPORT_BATCH.md` say the job is always on, list
   the sizing settings, name the three trigger values, and state that this closes PI-019 forward.
8. The PR body names the merge SHA and the deploy date, so the Steward's §4.2 and §8 window starts from a date
   the register can record.

---

## 6. Rollback

```
git revert --no-edit <merge sha> && git push
```

One command, one commit, no data migration, no setting to unwind. Reverting stops the nightly batch at the next
18:30 (the WebJob directory disappears with the revert) and stops the archive copy at the next report write.

**Archive blobs already written stay.** The container is append-only by design and nothing but the desk reads it,
so leaving them is harmless — and they are the record of what ran. If a container ever has to go away entirely,
that is a portal action of Haci's on `vx-report-archive`, never part of a code rollback.

---

## 7. Out of scope — do not touch

- **The legacy zone-less `timestamp`** (`day_trading_agent.py:609`), the per-timeframe `price_timestamp` fields
  and the `/analyze` response `timestamp` (`app.py:3644`). Changing them changes subscriber payloads and displays
  (§0.2 choice 2); PI-019's display half is a separate decision of Haci's.
- **History.** No backfill, re-stamp or copy of existing blobs into the archive. The 697 historical reports stay
  exploratory; the desk normalises their zone by date (PI-019).
- **The SAS report engine** (`services/super_agent_select_report_service.py`, `store_super_agent_select_report`,
  `azure_storage.py:790`) and every nightly pipeline step. Do not pass `record_plan_sources` or
  `numeric_trigger_contract` from any SAS path.
- **The principal prompt for any caller other than the fixed-universe batch**, the legacy 5m report shape, and
  PI-018's decision-layer overrides.
- **The Omega agent, Report Center, Action Center, templates, static assets, routers.**
- **Any Azure management-plane change** (lifecycle rules, immutability policies, container ACLs). §8 asks Haci to
  *look*; nobody changes one in this brief.
- **A database table, migration or model change.** The batch writes no row.
- **Crypto, ETFs, a second universe, or editing `LIQUID_LIST_V1`.**
- **Adding a flag.** If something here looks as though it needs a gate, that is a design error: say so in the PR
  and stop; do not add one (DP-59).
- Any subscriber-visible copy, field, ordering or number. There are none in this change.

---

## 8. Verification at `/desk-run verify EN-019 <sha>` — full protocol

**Whose step is whose.** The coding agent's work ends at §3–§5 and §4.1 (repository only). Every step below is
either **Haci's** (deploy) or the **Data Steward's** (read-only role `sas_research_ro` on `$RESEARCH_DB_URL`;
blob reads with `PROD_SAS_TOKEN`, read/list). Counts and metadata only: **no price, touch, return or outcome is
read in any step.**

### Haci

1. **Deploy** the merge. In Kudu, confirm the WebJobs dashboard lists `fixed_universe_report_batch` with schedule
   `0 30 18 * * 1-5` and that it executes the wwwroot copy (`docs/AZURE_WEBJOBS_AUTOMATION.md:59-66`, the stale
   wrapper warning). There is nothing to switch on: the first 18:30 ET after the deploy, it runs.
2. **Look, do not change:** Storage account → Data management → Lifecycle management. Record in the register
   whether any rule matches container `vx-report-archive`, and whether any rule matches `ai-reports` (the latter
   answers the F9 inventory's §9 question and `SAS_EXCURSION_BACKFILL.md:50-52`'s "aged out"). If a rule matches
   the archive container, tell the desk — the research record would expire.
3. Optionally set `FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS` if §0.3's spend is more than he wants. Record the
   date and the value; the night's `_declared_` manifest records it too.
4. After **three** trading sessions, run `/desk-run verify EN-019 <sha>`. What moves on the product: nothing a
   subscriber sees; spend rises by ~230 LLM calls a night (§0.3).

### Data Steward — before-state

Structural, not a snapshot: at `c311e81` no archive container existed, and no dated report blob carries
`report_provenance` or `trigger` (`research/reports/STEWARD_F9_blob_inventory.md` §3–§4, measured 2026-09-14 over
all 697 history blobs). No manifest pins a blob store, so there is no parquet to cite; the inventory's counts are
the reference.

### Data Steward — repo half

At `<sha>`, re-run §4.1(a), (b), (c), (d), (e) and (f) with `DATABASE_URL` unset, and record the output.

### Data Steward — database, read-only

```sql
-- S1. The SAS run each declared night was allowed to read.
SELECT trading_date, id, status, finished_at
FROM super_agent_select_runs
WHERE trading_date IN (:n1, :n2, :n3)
ORDER BY trading_date;

-- S2. The candidate rows the declaration must reproduce.
SELECT c.trading_date, c.symbol, c.overall_score, c.qualified, c.selected_rank
FROM super_agent_select_candidates_daily c
JOIN super_agent_select_runs r ON r.id = c.run_id AND r.trading_date = c.trading_date
WHERE c.trading_date IN (:n1, :n2, :n3)
ORDER BY c.trading_date, c.symbol;

-- S3. The batch wrote no report index row (it bypasses store_ai_report).
SELECT count(*) AS rows_in_batch_window
FROM user_report_index
WHERE user_id = 1
  AND stored_at >= :deployed_at
  AND (stored_at AT TIME ZONE 'America/New_York')::time >= TIME '18:30';
```

### Data Steward — blobs, read/list

Container `vx-report-archive`, prefixes `fixed_universe/<N>/` and `reports/`; containers `ai-reports-<N>` and
`ai-reports-<N+1>` (the batch window crosses UTC midnight); `ai-reports-jobs` blob `scheduler-digest-<N>.json`.

- **V1 — dated containers untouched.** No history blob written on or after the deploy date in any `ai-reports-*`
  container has a `report_provenance`, `plan_sources`, `trigger_price` or `report_provenance_summary` key; no
  blob name there starts with `fixed_universe/` or `reports/`. The count of `_1_` history blobs per day is within
  the pre-deploy range (inventory: 513 over 120 active days), not ~230 higher. S3 returns only rows explainable
  by ad-hoc internal-batch use in that window — normally 0.
- **V2 — one declaration, knowledge-time clean.** Exactly one `_declared_*.json` and one `_completed_*.json`,
  **or** exactly one `_skipped_*.json` and no declaration. `declared_at_utc` is later than 18:30 ET on N, later
  than S1's `finished_at` when `sas_component = "ok"`, and later than the digest's
  `runs.nightly_pipeline.updated_at_utc`. Recompute with the shipped pure function —
  `services.fixed_universe_batch.declare_universe(trading_date=N, declared_at_utc=<manifest value>, sas_run=<S1 row>, sas_candidates=<S2 rows>, max_symbols=<manifest settings.max_symbols>)`,
  imported read-only from `$CODEBASE_DIR` at `<sha>` — and its `symbols_sha256` equals the manifest's. (If S1's
  `finished_at` is later than `declared_at_utc`, SAS was re-run after the declaration: record it, not a FAIL.)
- **V3 — reports match the manifest, counted by analysis.** §4.2 check 1, on each of the three nights; plus every
  blob's symbol is in the declared list, no symbol has two `job_id`s, and every blob's provenance carries
  `universe_run_id = run_id` and `trading_date = N`.
- **V4 — PI-019, the zone.** §4.2 check 3, plus: `technical_timestamp_iso` converted to UTC precedes `stored_at`
  by 0–15 minutes; report the counts of `process_utc_offset` values.
- **V5 — timing.** Every report's `stored_at` is before 04:00 ET the next calendar day, and so before the next
  session's pre-market.
- **V6 — plan provenance and numeric trigger fields (counts only).** `plan_source` present on 100% of lane blobs;
  all four `trigger_*` keys present on 100% of setups (values may be null). Report per night:
  `plan_source_counts`, `numeric_trigger_complete / numeric_trigger_setups`, `lanes_per_analysis`,
  `principal_tokens_total`, `status_counts`, `stop_reason`, and the `settings` block. Descriptive; no threshold.
- **V7 — the nightly pipeline was not disturbed.** For each N, S1 shows `status = success` finished the same
  evening, and the digest shows `nightly_pipeline` = `success`, as on the five sessions before the deploy.
- **V8 — every report path is stamped.** §4.2 check 2 over all reports of one night (sample if more than 200).
  **No archive body anywhere carries `"unstamped": true`**; an unstamped copy names a report path this build
  missed, and is filed as a `research/PLATFORM_ISSUES.md` row.

**PASS requires V1–V8 on all three sessions.** On failure: V1 or V7 → tell Haci immediately, revert per §6, file
a PI row; V2–V6 or V8 → record `FAILED` with the failing count and file a PI row. Nothing a subscriber sees is
affected either way, so nothing has to be switched off in a hurry — and there is nothing to switch.

**On PASS** the Steward (i) writes the dated data note of §0.1 (first declared night, container, universe id,
ship SHA — not a repair-log row); (ii) records PI-019 as **fixed forward at `<sha>` from `<deploy date>`** for the
research record, with the display half left open as a separate question for Haci; (iii) notes for H-086..H-094
that re-entry trigger (1) is met from that night and trigger (2a)'s freeze should pin
`vx-report-archive/fixed_universe/` (and `reports/` for the subscriber companion), not the dated containers.
