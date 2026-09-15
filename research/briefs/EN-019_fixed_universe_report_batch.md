# EN-019 — multi-agent reports on a fixed, pre-declared universe, with provenance and an append-only archive

**Type:** enhancement brief, **plumbing** kind (fix-brief format; ENHANCEMENTS.md "Two kinds"). It gates nothing
and changes no subscriber-visible number, copy, field or ordering.
**Register row:** `research/ENHANCEMENTS.md` EN-019, Build = `HACI_DECIDED:build (2026-09-15)`
**Written:** 2026-09-15 by the Brief Writer, on Haci's `/desk-run prompt EN-019` (DP-48: asking is the decision)
**Platform repo:** `C:\Users\sahin\Projects\volatilx`
**Platform SHA all `path:line` citations are taken at:** `c311e819dbe492b18ef52d137000c1d8709919db`
(`c311e81`, "SAS ladder nightly: stamp trading-day steps, not only hit dates")
**Research repo SHA:** `df12d3f`
**Feature flags (both default OFF, read from the environment at call time — the convention of
`core/feature_flags.py:11-23` and `services/sas_conviction_card.py:68-69`):**
- `FIXED_UNIVERSE_REPORT_BATCH_ENABLED` — the nightly fixed-universe batch (new WebJob).
- `AI_REPORT_ARCHIVE_ENABLED` — an append-only archive copy, with provenance, of every report
  `store_ai_report` writes (subscriber `/analyze` and the ad-hoc internal batch).

Runtime settings (not gates; meaningful only when the batch flag is on): `FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS`
(default 80, clamped 1..120), `FIXED_UNIVERSE_REPORT_BATCH_START_DEADLINE_ET` (21:00),
`FIXED_UNIVERSE_REPORT_BATCH_STOP_ET` (22:15), `FIXED_UNIVERSE_REPORT_BATCH_POLL_SECONDS` (60),
`FIXED_UNIVERSE_REPORT_BATCH_PAUSE_SECONDS` (5), `AI_REPORT_ARCHIVE_CONTAINER` (`vx-report-archive`).

**PI-019 overlap — stated plainly.** This brief implements PI-019's two asks (an explicit zone offset and a
`trigger` field) **forward-only and in the archive copy, not in the dated report blob.** Every fixed-universe
report carries them always; every subscriber and ad-hoc batch report carries them in its archive copy once
Haci sets `AI_REPORT_ARCHIVE_ENABLED`. The zone-less legacy `timestamp` (`day_trading_agent.py:609`), the
dated `ai-reports-YYYY-MM-DD` blobs, the `_latest` pointers and the `/analyze` response
(`app.py:3579`, `str(datetime.now())`) are deliberately left byte-identical, because Report Center, Action
Center and Omega read them (§0 choice 2). **Recommendation for `/desk-run verify EN-019`** (the Brief Writer
does not change PI-019's status): if §8 V4 and V8 pass with `AI_REPORT_ARCHIVE_ENABLED` on, the Steward records
in PI-019's evidence "fixed forward for the research record by EN-019 at `<sha>` from `<enable date>`; the
dated blob and every subscriber display keep the zone-less field by design", and recommends Haci either close
PI-019 as fixed-forward or narrow it to the display half if he wants that fixed too. If the archive flag stays
off, PI-019 stays OPEN for subscriber and ad-hoc reports (fixed-universe reports are covered regardless).
The probable cause, located while writing this brief: the naive `datetime.now()` at `day_trading_agent.py:609`
takes the App Service process zone, and `WEBSITE_TIME_ZONE = America/New_York`
(`docs/AZURE_WEBJOBS_AUTOMATION.md:12`, `:97`) arrived with the WebJobs automation commits of 2026-04-05/06
(`76580a9`, `52ccbc0`) — the exact switch date PI-019 measured. The setting's own change date lives in the
Azure activity log, not the repo; the Steward may add it to PI-019's evidence.

**DP-50(b) — history and ship timing, done before writing:** see §0. Short form: **no database row is written
or rewritten, no dated report blob changes, no SAS input or output changes; no `DATA_NOTES.md` repair-log row
is required** (`research/data/DATA_NOTES.md:32-33`: forward-only additions take no row). No locked question
is constrained.

You are the coding agent working in the platform repo. This brief is self-contained: do not ask questions, do
not redesign, do not widen the scope. Implement §3 (including the docs in §3.8), run §4, add §5, and report the SHA.

**Nothing in this brief runs against a database or a blob store.** Under DP-49 you get no DB or blob step: your
`DATABASE_URL` is the platform's read-write role on live production (the desk's read-only role and production
are the same Postgres instance). Two specific prohibitions:

- **Do not run `pytest` in this repo.** `conftest.py:31-35` runs `create_tables()` (DDL) and the autouse
  fixture at `conftest.py:38-55` executes `db.query(User).delete()` and `db.query(UserActivityEvent).delete()`
  before and after **every test**, against whatever `DATABASE_URL` points at. Run the §5 test as
  `python tests/test_report_provenance.py` with `DATABASE_URL` unset — it loads no conftest.
- **Do not run `scripts/run_fixed_universe_report_batch.py`**, with or without `--declare-only`, and do not
  start the app. The only execution of the script allowed is the §5 flag-off test, which returns before any
  import that could open a connection.

§8 is the Data Steward's (read-only role and read/list blob token) and Haci's (deploy, settings).

**Indentation:** `app.py`, `azure_storage.py`, `ai_agents/principal_agent.py`, the new files and `tests/` are
4-space indented. (`models.py` is tab-indented; you do not touch it.)

---

## 0. Ship timing, design choices, cost

### 0.1 DP-50(b) — does this touch anything a locked question reads?

**No.** Checked against every locked question on `research/BOARD.md` (Q002–Q037) and `desk_queue.py` on
2026-09-15.

- **Database:** the batch reads `super_agent_select_runs` and `super_agent_select_candidates_daily` and writes
  **no row anywhere** — no report index (it bypasses `store_ai_report`'s `user_report_index` upsert at
  `azure_storage.py:590-627`), no digest ledger, no job table. The archive flag adds blob writes only.
  Nothing in `scripts/run_nightly_pipeline.py`, the SAS engine, the ladder, the outcome backfills or the UOA
  screener changes; §4(c) proves the diff there is empty.
- **Blobs a PREREG could read:** the only blob object a locked PREREG touches is the SAS report's
  `technical_snapshot` / lane targets via `sas_selection_excursion` (Q004 §4, `services/sas_excursion.py:335-354`),
  written by `store_super_agent_select_report` (`azure_storage.py:642-702`) through
  `services/super_agent_select_report_service.py`. Neither changes (§4(c)); the new `PrincipalAgent` keyword
  arguments default to the old behaviour and the SAS caller does not pass them (§4(d) hashes the default path).
- **No F9 question is registered** (`research/questions/DEFERRED.md` H-086..H-094 — all deferred on exactly this
  collection). H-093 (F5, "does the multi-agent technical read agree with SAS", in the registration queue) would
  read this collection; it constrains nothing here.
- **Shared resources on the pick night:** the batch waits for the nightly pipeline to record that it has finished
  before it starts (§0.2 choice 5), so it never competes with `backfill_outcomes` / `backfill_w60_outcomes` for
  Alpaca bars. `indicator_fetcher.py` has no 429 handling (no `429`/`retry`/`rate limit` anywhere in the file),
  so contention would surface as silent fetch failures in the pipeline's outcome maturation — the thing locked
  questions read. The wait is the protection.

**Repair log:** no row. **Data note:** at a §8 PASS the Steward adds a dated note (not a repair-log row) naming
the first declared night, the archive container, `fixed_universe_v1` and the ship SHA, because H-086's re-entry
trigger (1) says the F9 window starts at that date (DEFERRED.md H-086, "What would move it back", item 1).

### 0.2 Open design choices — what I chose, and the conservative option each takes

1. **Fixed-universe reports go to a separate, non-dated archive container only** — never to
   `ai-reports-YYYY-MM-DD`, never a `_latest` pointer, never `user_report_index`. Writing ~230 blobs a night into
   the dated containers would change subscriber surfaces: Omega's report tool lists **all users'** blobs for a
   symbol and date when `access_scope="all"` (`ai_agents/omega_agent.py:2497-2508` →
   `azure_storage.py:1054-1060`, capped at 120 reports, so research blobs would crowd subscriber blobs out of
   Omega's context), and user 1's Report Center / Action Center would switch to research reports
   (`azure_storage.py:582-588`, `:590-627`). The container name does not start with `ai-reports`, so a lifecycle
   rule written for the dated containers cannot match it (`docs/SAS_EXCURSION_BACKFILL.md:50-52` records a
   report blob that "aged out of its dated container").
2. **Provenance is stamped on the archive copy, not on the dated blob.** Subscriber payloads — the dated history
   blob, the `_latest` pointer, the `ai-reports-jobs` result, the `/api/ai-analysis-result` poll and the
   `/analyze` response — stay **byte-identical with both flags in every position.** The cost is that PI-019 is
   fixed for the research record, not for displays (header).
3. **The numeric trigger contract (`trigger_price` / `trigger_direction` / `trigger_basis`) is requested only
   by the fixed-universe batch.** It is a prompt addition (`ai_agents/principal_agent.py:555`, `:585`), and a
   prompt change alters LLM output for whoever receives it; subscribers and SAS reports keep the current prompt.
   Consequence H-094 must name at re-entry: research plans are generated with three extra prompt lines, so they
   are the subscriber plan's closest sibling, not the identical object. The fields are the model's own statement
   of its trigger; nothing parses the sentence (rule 9; DEFERRED.md H-094 (a)).
4. **Universe `fixed_universe_v1`** = a pinned list of 20 large, liquid S&P 500 common stocks (all 20 present in
   `data/sp500_symbols.txt`), then every candidate of the night's SAS run, capped at 80. Order: liquid list as
   written → published picks (`qualified`) by `selected_rank` → unpublished candidates by `overall_score`
   descending; the cap can only drop the lowest-scored unpublished candidates. No crypto, no ETFs (no bar source
   for crypto in any manifest, DEFERRED.md H-086 (3)). The list was fixed without reading any report or outcome;
   a different list is a new universe id, never an edit.
5. **Clock:** WebJob at **18:30 ET** Mon–Fri. It then waits until the scheduler digest records the nightly
   pipeline as `success` or `failed`; if that has not happened by **21:00 ET** the night is **skipped and
   recorded, never run on a different clock or universe**. It stops *starting* new symbols at **22:15 ET**,
   ahead of the in-process UOA slot at 22:30 (`services/uoa_scheduler.py:181`). Why 18:30: since 2026-06-09
   (the point-in-time-legal range), 63 of 65 SAS runs in the pinned freeze finished the same evening between
   17:05 and **17:46 ET** (`research/data/v001_sas_runs.parquet`, manifest_v001; the other two finished the next
   day — 2026-07-02 across the 07-03 market holiday, and the 2026-07-06 manual re-run listed in
   `research/data/DATA_NOTES.md` "Manual / late SAS runs"). 18:30 clears the latest same-day finish by 44 minutes.
6. **Knowledge time:** SAS candidates enter the universe only from a run whose status is `success` and whose
   `finished_at` is at or before the declaration time; the declaration (symbols, order, sha256, SAS run id and
   finish time) is written to the archive **before the first analysis starts**. Every report is therefore
   generated after 16:05 ET and after its universe was fixed, and — with the 22:15 stop — before the next
   session's pre-market. On a night SAS is unavailable the liquid list still runs and the declaration says
   `sas_component: "unavailable"` with the reason, so a PREREG can filter those nights out.
7. **Analysis shape:** principal agent on, all three lanes in one unscoped call (`app.py:339-343`), 7 timeframes
   (15m…1mo, the same set a subscriber asking for all lanes gets), AI summary off, earnings agent off, raw results
   off. One analysis writes up to three lane blobs (`app.py:481-504`); the manifests count **analyses by
   `job_id`**, not blobs.
8. **No writes outside the archive container:** no database row, no email, no scheduler-digest entry.
   Operations visibility is the WebJob log (with a 30-second heartbeat, so the triggered WebJob idle timeout
   cannot kill a silent LLM call) plus the `_declared_` / `_completed_` / `_skipped_` manifests.
9. **`user_id` on fixed-universe payloads stays `1`** (the internal batch identity, `app.py:3966`) for continuity;
   `report_provenance.trigger` is what distinguishes them.

### 0.3 Volume and cost — bounded default

Universe size, from the pinned freeze over the 65 nights 2026-06-09..2026-09-10
(`v001_sas_candidates.parquet`, counting distinct symbols per `trading_date`, union with the 20-name list):
candidates per night median 62 (47–68); overlap with the liquid list median 4 (1–9); **union median 77,
range 65–83**; the cap of 80 binds on 10 of 65 nights.

Per analysis: three LLM calls — technical summary and price-action summary on `gpt-5.4-nano`, principal on
`gpt-5.6-terra`, reasoning low, ≤ 3,200 output tokens (`ai_agents/principal_agent.py:86-114`) — plus ~8 Alpaca
bar fetches and the price-action fetches. At ~77 analyses a night: **~230 LLM calls and ~230 report blobs a
night, ~1,600 analyses and ~4,800 LLM calls a month.** Today's whole corpus is 697 blobs over ~8 months
(`research/reports/STEWARD_F9_blob_inventory.md` §1), so this is **roughly 50× the current multi-agent report
volume.** Token volume is an estimate, not a measurement (desk view: ~25–35k input and ~4–5k output tokens per
analysis → ~2–3M input and ~0.3–0.4M output tokens a night). The completed manifest records the principal
call's `usage.total_tokens` summed per night, so Haci has the real figure after night one; the nano summaries'
tokens are not in that sum.

Rate limits: calls are strictly sequential with a 5-second pause, i.e. a few requests a minute — far below any
OpenAI tier's RPM; TPM depends on Haci's account tier, which the desk cannot see. Runtime estimate 45–120 s per
analysis → 1–2.5 h for 77 symbols; the 22:15 stop bounds the night at 3 h 45 m from an 18:30 start however slow
it is, and symbols not started are recorded. **If the spend is unacceptable, lower
`FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS`; at 40 each night still carries the ≥ 3 same-day controls H-086
names, because the published picks sit ahead of the cut.**

---

## 1. What is missing, and the evidence

The multi-agent technical reports exist but cannot decide any question, historically or going forward
(`research/reports/STEWARD_F9_blob_inventory.md`, counts and metadata only, 2026-09-14):

- **Selection.** 697 history blobs over 120 days; **73.6% (513) come from the internal batch account `user_id = 1`**
  re-running a hand-picked list; seven symbols are 60% of the corpus, TSLA alone 134. The same symbol is re-run
  within 5 trading days on 56.5% of symbol-days. There is no fixed universe, so no night has its own
  distance-matched controls.
- **No provenance.** Neither the blob name nor the payload says whether a report came from `/analyze`
  (`app.py:3286-3287`, the subscriber's `user_id`) or `/api/internal/batch-analyze` (`app.py:3696-3700`,
  `user_id=1` hard-coded at `app.py:3966` and `:3783`) — PI-019.
- **Zone-less clock.** `timestamp` is UTC to 2026-04-05 and US Eastern from 2026-04-07 with no marker — PI-019.
- **Blob counts are not analysis counts.** One analysis writes one blob **per lane** (`app.py:481-504`) and a
  single blob only on the no-lane fallback (`app.py:505-515`), so every F9 floor was counted in the wrong unit
  (DEFERRED.md H-094 (c)).
- **The GPT plan's trigger is free text** (`"trigger": "string"`, `ai_agents/principal_agent.py:569`, `:576`;
  "describe conditional triggers", `:549`) — ungradeable without a parser rule 9 forbids (H-094 (a)).
- **Fallback plans are indistinguishable from LLM plans.** `_fallback_strategies_from_experts`
  (`ai_agents/principal_agent.py:878-933`) writes a symmetric ±0.5% / ±1.0% template, identical for all three
  lanes, and no field says which path ran (H-094 (b)).
- **Retention is unproven.** Dated containers are the only store, and a sibling blob is documented as having
  aged out of one (`docs/SAS_EXCURSION_BACKFILL.md:50-52`); the desk's data-plane token cannot see a lifecycle
  policy (inventory §9).

### Reproducing check — **Data Steward only**, read/list blob token, counts only

Not for the coding agent (DP-49). Re-run inventory §3's count over the last 20 dated containers: history blobs
(exclude `_latest.json` and `SAS_` names) grouped by the `_<user_id>_` token in the blob name. Expected today:
`user_id = 1` is the largest single contributor, and no blob payload has a `report_provenance` key or any
`trigger` field.

---

## 2. Cause — the code paths

- **No schedule, no universe.** The only multi-symbol path is the HTTP endpoint `app.py:3696-4011`: a caller
  POSTs ≤ 25 symbols (`app.py:3705-3706`), the work runs as a web-process background task over an in-memory job
  store (`app.py:246-248`, `:4003`). Nothing calls it on a clock; `docs/AZURE_WEBJOBS_AUTOMATION.md:14-22` lists
  no report job. What gets analysed is whatever the operator typed.
- **Provenance is dropped at the write.** `_run_and_persist_expert_analysis` (`app.py:276-518`) knows its caller
  only through `user_id` and passes nothing else to `store_ai_report` (`app.py:493-504`, `:507-515`);
  `store_ai_report` (`azure_storage.py:523-639`) enriches with `symbol`, `user_id`, `stored_at`,
  `strategy_scope` only (`azure_storage.py:551-557`).
- **The zone.** `analysis_output["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')`
  (`day_trading_agent.py:609`), exported unchanged (`day_trading_agent.py:1427-1429`); every per-timeframe
  `price_timestamp` is written beside it (`day_trading_agent.py:726-728`).
- **Plan provenance.** `_summarise_node` (`ai_agents/principal_agent.py:354-444`) replaces missing lanes with the
  template (`:390-409`) and builds `plan` (`:414-428`) without recording which lanes were replaced.
- **Retention.** Only dated containers exist (`azure_storage.py:148-151`), written by UTC day of the write
  (`azure_storage.py:527`).

---

## 3. Change

### Why two feature flags, not none

This is new behaviour, not the restoration of intended behaviour: a scheduled job with real LLM spend, and a
second write on every report. CLAUDE.md rule 11 applies: ship dark, prove the old path byte-identical (§4), flip
last (§8, Haci). Both flags default OFF; with both off, the only runtime differences are a few Python lines that
evaluate `False`.

### 3.1 New file — `services/report_provenance.py` (pure: standard library only; no `db`, `models`, Azure or app import)

```python
"""Report provenance for multi-agent technical reports (EN-019, PI-019).

Pure: standard library only. No database, no Azure, no network, no app import.

The provenance block is written ONLY to the append-only archive copy of a report
(azure_storage.store_ai_report with AI_REPORT_ARCHIVE_ENABLED) and to fixed-universe
research reports. The dated ai-reports-YYYY-MM-DD blob, the _latest pointer, the job
result and every HTTP response stay byte-identical.
"""

from __future__ import annotations

import math
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

REPORT_PROVENANCE_SCHEMA = "report_provenance_v1"

TRIGGER_SUBSCRIBER = "subscriber"
TRIGGER_INTERNAL_BATCH = "internal_batch"
TRIGGER_SCHEDULED_FIXED_UNIVERSE = "scheduled_fixed_universe"
TRIGGERS = (TRIGGER_SUBSCRIBER, TRIGGER_INTERNAL_BATCH, TRIGGER_SCHEDULED_FIXED_UNIVERSE)

PLAN_SOURCE_LLM = "llm"
PLAN_SOURCE_FALLBACK = "fallback_template"

LANE_KEYS = ("day_trading", "swing_trading", "longterm_trading")
SETUP_SIDES = ("buy_setup", "sell_setup")
TRIGGER_DIRECTIONS = ("above", "below")
TRIGGER_BASES = ("close", "touch")

ARCHIVE_CONTAINER_DEFAULT = "vx-report-archive"

_PROVENANCE_EXTRA_KEYS = frozenset(
    {"universe_id", "universe_run_id", "trading_date", "universe_sources", "numeric_trigger_contract"}
)
_TRUE = {"1", "true", "yes", "on"}


def report_archive_enabled() -> bool:
    """AI_REPORT_ARCHIVE_ENABLED, default OFF. Read per call (core/feature_flags.py convention)."""
    return (os.getenv("AI_REPORT_ARCHIVE_ENABLED", "") or "").strip().lower() in _TRUE


def archive_container_setting() -> str:
    return (os.getenv("AI_REPORT_ARCHIVE_CONTAINER", "") or "").strip() or ARCHIVE_CONTAINER_DEFAULT


def utc_iso_z(moment: datetime) -> str:
    if not isinstance(moment, datetime) or moment.tzinfo is None:
        raise ValueError("utc_iso_z needs an aware datetime")
    return moment.astimezone(timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds") + "Z"


def format_utc_offset(offset: Optional[timedelta]) -> Optional[str]:
    if offset is None:
        return None
    total = int(offset.total_seconds())
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    return f"{sign}{total // 3600:02d}:{(total % 3600) // 60:02d}"


def localize_naive_timestamp(text: Any, offset: Optional[timedelta]) -> Optional[str]:
    """'2026-09-11 18:31:02' written in a process at UTC-4 -> '2026-09-11T18:31:02-04:00'.

    The multi-agent engine writes a zone-less local clock read (day_trading_agent.py:609).
    The offset passed here is the writing process's own offset at stamp time, seconds later.
    An already-aware string is returned with its own offset. Unparseable -> None.
    """
    if offset is None or not isinstance(text, str) or not text.strip():
        return None
    try:
        parsed = datetime.fromisoformat(text.strip())
    except ValueError:
        return None
    if parsed.tzinfo is not None:
        return parsed.isoformat(timespec="seconds")
    return parsed.replace(tzinfo=timezone(offset)).isoformat(timespec="seconds")


def find_technical_timestamp(snapshot: Any, symbol: Any) -> Optional[str]:
    if not isinstance(snapshot, Mapping) or not isinstance(symbol, str):
        return None
    for key in (symbol, symbol.upper(), symbol.lower()):
        entry = snapshot.get(key)
        if isinstance(entry, Mapping):
            value = entry.get("timestamp")
            return value if isinstance(value, str) and value.strip() else None
    return None


def lane_blob_keys(strategies: Any) -> List[str]:
    """The lanes app._run_and_persist_expert_analysis writes one blob for, in write order
    (same filter as app.py:481-488). Empty list -> the single-blob fallback path."""
    if not isinstance(strategies, Mapping) or not strategies:
        return []
    keys: List[str] = []
    for lane_key in strategies.keys():
        if not isinstance(lane_key, str):
            continue
        normalized = lane_key.strip().lower()
        if normalized in LANE_KEYS:
            keys.append(normalized)
    return keys


def classify_plan_sources(llm_lane_keys: Iterable[str], final_strategies: Any) -> Dict[str, str]:
    """Per lane: 'llm' if the lane came from the model's structured output, else 'fallback_template'."""
    if not isinstance(final_strategies, Mapping):
        return {}
    llm = {key for key in (llm_lane_keys or []) if isinstance(key, str)}
    return {
        key: (PLAN_SOURCE_LLM if key in llm else PLAN_SOURCE_FALLBACK)
        for key in final_strategies.keys()
        if isinstance(key, str)
    }


def _finite_positive(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number


def _choice(value: Any, allowed: Sequence[str]) -> Optional[str]:
    if not isinstance(value, str):
        return None
    token = value.strip().lower()
    return token if token in allowed else None


def normalise_numeric_trigger(setup: Any) -> Any:
    """COPY of a model-written setup with the three numeric trigger fields coerced.
    Never reads the trigger sentence (rule 9): an invalid or absent field becomes None."""
    if not isinstance(setup, Mapping):
        return setup
    out = dict(setup)
    out["trigger_price"] = _finite_positive(setup.get("trigger_price"))
    out["trigger_direction"] = _choice(setup.get("trigger_direction"), TRIGGER_DIRECTIONS)
    out["trigger_basis"] = _choice(setup.get("trigger_basis"), TRIGGER_BASES)
    out["trigger_fields_complete"] = all(
        out[key] is not None for key in ("trigger_price", "trigger_direction", "trigger_basis")
    )
    return out


def fallback_numeric_trigger(setup: Any, side: str) -> Any:
    """The template's trigger is 'Only act if price confirms beyond the entry level.'
    (ai_agents/principal_agent.py default_setup): level = entry, direction from the side.
    The sentence does not say close or touch, so the basis stays None."""
    if not isinstance(setup, Mapping):
        return setup
    out = dict(setup)
    out["trigger_price"] = _finite_positive(setup.get("entry"))
    out["trigger_direction"] = "above" if side == "buy_setup" else "below"
    out["trigger_basis"] = None
    out["trigger_fields_complete"] = False
    return out


def apply_numeric_trigger_contract(strategies: Any, llm_lane_keys: Iterable[str]) -> Any:
    """New lane dicts (inputs never mutated; the shared fallback template is copied per lane)."""
    if not isinstance(strategies, Mapping):
        return strategies
    llm = {key for key in (llm_lane_keys or []) if isinstance(key, str)}
    result: Dict[str, Any] = {}
    for lane_key, lane in strategies.items():
        if not isinstance(lane, Mapping):
            result[lane_key] = lane
            continue
        lane_copy = dict(lane)
        for side in SETUP_SIDES:
            if side in lane_copy:
                if lane_key in llm:
                    lane_copy[side] = normalise_numeric_trigger(lane_copy[side])
                else:
                    lane_copy[side] = fallback_numeric_trigger(lane_copy[side], side)
        result[lane_key] = lane_copy
    return result


def build_report_provenance(
    *,
    trigger: str,
    job_id: Optional[str],
    strategy_scope: Optional[str],
    lane_keys_in_job: Optional[Sequence[str]],
    plan_sources: Optional[Mapping[str, str]],
    technical_timestamp: Optional[str],
    utc_offset: Optional[timedelta],
    analysis_completed_at_utc: datetime,
    report_status: str = "done",
    extra: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    if trigger not in TRIGGERS:
        raise ValueError(f"unknown trigger {trigger!r}; expected one of {TRIGGERS}")
    extra_items = dict(extra or {})
    unknown = set(extra_items) - _PROVENANCE_EXTRA_KEYS
    if unknown:
        raise ValueError(f"unknown provenance keys {sorted(unknown)}")
    lanes = list(lane_keys_in_job or [])
    scope = strategy_scope if strategy_scope in LANE_KEYS else None
    sources = dict(plan_sources) if isinstance(plan_sources, Mapping) else None
    provenance: Dict[str, Any] = {
        "schema": REPORT_PROVENANCE_SCHEMA,
        "trigger": trigger,
        "job_id": job_id or None,
        "report_status": report_status,
        "strategy_scope": scope,
        "blobs_in_job": len(lanes) if lanes else 1,
        "lane_keys_in_job": lanes,
        "plan_source": (sources or {}).get(scope) if scope else None,
        "plan_sources": sources,
        "technical_timestamp_raw": technical_timestamp if isinstance(technical_timestamp, str) else None,
        "technical_timestamp_iso": localize_naive_timestamp(technical_timestamp, utc_offset),
        "process_utc_offset": format_utc_offset(utc_offset),
        "analysis_completed_at_utc": utc_iso_z(analysis_completed_at_utc),
    }
    provenance.update(extra_items)
    return provenance


def archive_blob_name(*, trigger: Optional[str], stored_at_utc: datetime, history_blob_name: str) -> str:
    token = trigger if trigger in TRIGGERS else "unstamped"
    day = stored_at_utc.astimezone(timezone.utc).date().isoformat()
    return f"reports/{day}/{token}/{history_blob_name}"
```

### 3.2 New file — `services/fixed_universe_batch.py` (pure: standard library plus 3.1)

```python
"""EN-019: the fixed, pre-declared universe for the nightly multi-agent report batch.

Pure: standard library plus services.report_provenance. No database, no Azure, no network,
no app import. scripts/run_fixed_universe_report_batch.py does the I/O around these functions.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from collections import Counter
from datetime import date, datetime, time, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence

from services.report_provenance import LANE_KEYS, SETUP_SIDES, utc_iso_z

FIXED_UNIVERSE_ID = "fixed_universe_v1"

# The stable half of the universe: twenty large, liquid S&P 500 common stocks, fixed by the
# research desk on 2026-09-15 without reference to any report or outcome (EN-019).
# NEVER edit this tuple. A different list is a new FIXED_UNIVERSE_ID ("fixed_universe_v2").
LIQUID_LIST_V1 = (
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "TSLA", "JPM", "V",
    "LLY", "UNH", "XOM", "WMT", "MA", "COST", "HD", "PG", "JNJ", "BAC",
)

SOURCE_LIQUID = "liquid_v1"
SOURCE_SAS_PUBLISHED = "sas_published"
SOURCE_SAS_CANDIDATE = "sas_candidate"

DEFAULT_MAX_SYMBOLS = 80
MAX_SYMBOLS_CEILING = 120
DEFAULT_START_DEADLINE_ET = time(21, 0)
DEFAULT_STOP_ET = time(22, 15)
DEFAULT_POLL_SECONDS = 60
DEFAULT_PAUSE_SECONDS = 5

PIPELINE_DIGEST_JOB_KEY = "nightly_pipeline"  # services.job_notifications._job_key("Nightly Pipeline")
MANIFEST_KINDS = ("declared", "completed", "skipped")
DONE_STATUSES = ("done", "done_baseline_only")

_TRUE = {"1", "true", "yes", "on"}
_SAFE_TOKEN = re.compile(r"[^a-zA-Z0-9_-]")
_HHMM = re.compile(r"(\d{1,2}):(\d{2})")


def batch_enabled() -> bool:
    """FIXED_UNIVERSE_REPORT_BATCH_ENABLED, default OFF. Must be an App Service setting."""
    return (os.getenv("FIXED_UNIVERSE_REPORT_BATCH_ENABLED", "") or "").strip().lower() in _TRUE


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


def settings_for_manifest(settings: Mapping[str, Any]) -> Dict[str, Any]:
    return {key: (value.strftime("%H:%M") if isinstance(value, time) else value) for key, value in settings.items()}


def _norm_symbol(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    token = value.strip().upper()
    return token or None


def _score(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _rank(row: Mapping[str, Any]) -> Optional[int]:
    rank = row.get("selected_rank")
    return rank if isinstance(rank, int) and not isinstance(rank, bool) else None


def universe_sha256(symbols: Sequence[str]) -> str:
    return hashlib.sha256(json.dumps(list(symbols), separators=(",", ":")).encode("utf-8")).hexdigest()


def declare_universe(
    *,
    trading_date: date,
    declared_at_utc: datetime,
    sas_run: Optional[Mapping[str, Any]],
    sas_candidates: Sequence[Mapping[str, Any]],
    liquid: Sequence[str] = LIQUID_LIST_V1,
    max_symbols: int = DEFAULT_MAX_SYMBOLS,
) -> Dict[str, Any]:
    """Tonight's universe, from data that exists at declared_at_utc. Deterministic.

    Order: the liquid list as written; then published SAS picks (qualified) by selected_rank,
    unranked last, ties by symbol; then the other candidates by overall_score descending,
    missing scores last, ties by symbol. A symbol appears once and carries every source that
    named it. The cap truncates the tail, so only the lowest-scored unpublished candidates can
    be dropped. SAS candidates enter only from a run that finished successfully at or before
    declared_at_utc (knowledge time); otherwise the liquid list runs alone and the reason is kept.
    """
    if not isinstance(declared_at_utc, datetime) or declared_at_utc.tzinfo is None:
        raise ValueError("declared_at_utc must be an aware datetime")
    cap = max(1, int(max_symbols))

    finished = sas_run.get("finished_at_utc") if isinstance(sas_run, Mapping) else None
    reason: Optional[str] = None
    if not isinstance(sas_run, Mapping):
        reason = "no_sas_run_for_trading_date"
    elif str(sas_run.get("status") or "").strip().lower() != "success":
        reason = f"sas_run_status_{str(sas_run.get('status') or 'missing').strip().lower()}"
    elif not isinstance(finished, datetime) or finished.tzinfo is None:
        reason = "sas_run_not_finished"
    elif finished > declared_at_utc:
        reason = "sas_run_finished_after_declaration"
    sas_ok = reason is None

    entries: List[Dict[str, Any]] = []
    position: Dict[str, int] = {}

    def _add(symbol: str, source: str, row: Optional[Mapping[str, Any]] = None) -> None:
        if symbol not in position:
            position[symbol] = len(entries)
            entries.append(
                {
                    "symbol": symbol,
                    "sources": [],
                    "sas_overall_score": None,
                    "sas_qualified": None,
                    "sas_selected_rank": None,
                }
            )
        entry = entries[position[symbol]]
        if source not in entry["sources"]:
            entry["sources"].append(source)
        if row is not None:
            entry["sas_overall_score"] = _score(row.get("overall_score"))
            entry["sas_qualified"] = row.get("qualified") is True
            entry["sas_selected_rank"] = _rank(row)

    for raw in liquid:
        symbol = _norm_symbol(raw)
        if symbol:
            _add(symbol, SOURCE_LIQUID)

    rows = (
        [r for r in (sas_candidates or []) if isinstance(r, Mapping) and _norm_symbol(r.get("symbol"))]
        if sas_ok
        else []
    )
    published = sorted(
        (r for r in rows if r.get("qualified") is True),
        key=lambda r: (_rank(r) is None, _rank(r) or 0, _norm_symbol(r.get("symbol"))),
    )
    others = sorted(
        (r for r in rows if r.get("qualified") is not True),
        key=lambda r: (
            _score(r.get("overall_score")) is None,
            -(_score(r.get("overall_score")) or 0.0),
            _norm_symbol(r.get("symbol")),
        ),
    )
    for row in published:
        _add(_norm_symbol(row.get("symbol")), SOURCE_SAS_PUBLISHED, row)
    for row in others:
        _add(_norm_symbol(row.get("symbol")), SOURCE_SAS_CANDIDATE, row)

    kept = entries[:cap]
    symbols = [entry["symbol"] for entry in kept]
    return {
        "universe_id": FIXED_UNIVERSE_ID,
        "trading_date": trading_date.isoformat(),
        "declared_at_utc": utc_iso_z(declared_at_utc),
        "sas_component": "ok" if sas_ok else "unavailable",
        "sas_unavailable_reason": reason,
        "sas_run_id": sas_run.get("id") if isinstance(sas_run, Mapping) else None,
        "sas_run_finished_at_utc": (
            utc_iso_z(finished) if isinstance(finished, datetime) and finished.tzinfo is not None else None
        ),
        "n_sas_candidates": len(rows),
        "liquid_list": [s for s in (_norm_symbol(x) for x in liquid) if s],
        "max_symbols": cap,
        "entries": kept,
        "symbols": symbols,
        "symbols_sha256": universe_sha256(symbols),
        "dropped_by_cap": [entry["symbol"] for entry in entries[cap:]],
    }


def pipeline_status(digest_payload: Any, job_key: str = PIPELINE_DIGEST_JOB_KEY) -> Optional[str]:
    runs = digest_payload.get("runs") if isinstance(digest_payload, Mapping) else None
    entry = runs.get(job_key) if isinstance(runs, Mapping) else None
    status = entry.get("status") if isinstance(entry, Mapping) else None
    return status.strip().lower() if isinstance(status, str) and status.strip() else None


def pipeline_finished(digest_payload: Any, job_key: str = PIPELINE_DIGEST_JOB_KEY) -> bool:
    return pipeline_status(digest_payload, job_key) in ("success", "failed")


def is_past(now_et: datetime, limit: time) -> bool:
    return (now_et.hour, now_et.minute) >= (limit.hour, limit.minute)


def fixed_universe_prefix(trading_date: date) -> str:
    return f"fixed_universe/{trading_date.isoformat()}/"


def fixed_universe_report_blob_name(
    *, trading_date: date, symbol: str, strategy_scope: Optional[str], stored_at_utc: datetime, job_id: Optional[str]
) -> str:
    safe_symbol = (symbol or "UNKNOWN").upper().replace("/", "-").replace(" ", "_")
    scope = strategy_scope if strategy_scope in LANE_KEYS else "noscope"
    token = stored_at_utc.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    job = _SAFE_TOKEN.sub("_", str(job_id)) if job_id else "nojob"
    return f"{fixed_universe_prefix(trading_date)}{safe_symbol}_{scope}_{token}_{job}.json"


def fixed_universe_manifest_blob_name(*, trading_date: date, kind: str, run_id: str) -> str:
    if kind not in MANIFEST_KINDS:
        raise ValueError(f"unknown manifest kind {kind!r}")
    return f"{fixed_universe_prefix(trading_date)}_{kind}_{_SAFE_TOKEN.sub('_', str(run_id))}.json"


def jobs_entry_from_result(
    *, symbol: str, outcome: Mapping[str, Any], started_at_utc: datetime, finished_at_utc: datetime
) -> Dict[str, Any]:
    job_id = outcome.get("ai_job_id") if isinstance(outcome, Mapping) else None
    job_result = outcome.get("job_result") if isinstance(outcome, Mapping) else None
    entry: Dict[str, Any] = {
        "symbol": symbol,
        "job_id": job_id,
        "started_at_utc": utc_iso_z(started_at_utc),
        "finished_at_utc": utc_iso_z(finished_at_utc),
        "duration_seconds": round((finished_at_utc - started_at_utc).total_seconds(), 1),
        "error": None,
    }
    if not job_id or not isinstance(job_result, Mapping):
        entry.update(
            {
                "status": "done_baseline_only",
                "principal_status": None,
                "lanes_written": [],
                "plan_sources": None,
                "numeric_trigger_setups": 0,
                "numeric_trigger_complete": 0,
                "principal_total_tokens": None,
            }
        )
        return entry
    wrapper = job_result.get("principal_plan")
    plan = wrapper.get("data") if isinstance(wrapper, Mapping) and wrapper.get("success") else None
    strategies = plan.get("strategies") if isinstance(plan, Mapping) else None
    summary = job_result.get("report_provenance_summary")
    summary = summary if isinstance(summary, Mapping) else {}
    setups = complete = 0
    if isinstance(strategies, Mapping):
        for lane in strategies.values():
            if not isinstance(lane, Mapping):
                continue
            for side in SETUP_SIDES:
                setup = lane.get(side)
                if isinstance(setup, Mapping):
                    setups += 1
                    if setup.get("trigger_fields_complete") is True:
                        complete += 1
    usage = plan.get("usage") if isinstance(plan, Mapping) else None
    tokens = usage.get("total_tokens") if isinstance(usage, Mapping) else None
    entry.update(
        {
            "status": "done",
            "principal_status": "ok" if plan is not None else "failed",
            "lanes_written": list(summary.get("lane_keys_in_job") or []),
            "plan_sources": summary.get("plan_sources"),
            "numeric_trigger_setups": setups,
            "numeric_trigger_complete": complete,
            "principal_total_tokens": tokens if isinstance(tokens, int) and not isinstance(tokens, bool) else None,
        }
    )
    return entry


def summarise_completed_run(
    *,
    declaration: Mapping[str, Any],
    jobs: Sequence[Mapping[str, Any]],
    started_at_utc: datetime,
    finished_at_utc: datetime,
    stop_reason: str,
) -> Dict[str, Any]:
    statuses = Counter(str(job.get("status")) for job in jobs)
    done = [job for job in jobs if job.get("status") in DONE_STATUSES]
    job_ids = sorted({str(job["job_id"]) for job in done if job.get("job_id")})
    lanes_hist = Counter(str(len(job.get("lanes_written") or [])) for job in done)
    plan_counts: Counter = Counter()
    for job in done:
        for source in (job.get("plan_sources") or {}).values():
            plan_counts[str(source)] += 1
    tokens = [job["principal_total_tokens"] for job in done if isinstance(job.get("principal_total_tokens"), int)]
    return {
        "universe_id": declaration.get("universe_id"),
        "run_id": declaration.get("run_id"),
        "trading_date": declaration.get("trading_date"),
        "symbols_sha256": declaration.get("symbols_sha256"),
        "started_at_utc": utc_iso_z(started_at_utc),
        "finished_at_utc": utc_iso_z(finished_at_utc),
        "stop_reason": stop_reason,
        "n_declared": len(declaration.get("symbols") or []),
        "n_jobs_listed": len(jobs),
        "status_counts": dict(sorted(statuses.items())),
        "n_analyses": len(job_ids),
        "n_report_blobs_expected": sum((len(job.get("lanes_written") or []) or 1) for job in done),
        "lanes_per_analysis": dict(sorted(lanes_hist.items())),
        "plan_source_counts": dict(sorted(plan_counts.items())),
        "numeric_trigger_setups": sum(int(job.get("numeric_trigger_setups") or 0) for job in done),
        "numeric_trigger_complete": sum(int(job.get("numeric_trigger_complete") or 0) for job in done),
        "principal_tokens_total": sum(tokens) if tokens else None,
        "jobs": [dict(job) for job in jobs],
    }
```

### 3.3 `azure_storage.py`

**(a) Imports.** After the Azure imports ending at `azure_storage.py:13`, add:

```python
from services.fixed_universe_batch import fixed_universe_report_blob_name
from services.report_provenance import (
    REPORT_PROVENANCE_SCHEMA,
    TRIGGER_SCHEDULED_FIXED_UNIVERSE,
    archive_blob_name,
    archive_container_setting,
    report_archive_enabled,
)
```

**(b) Signature** — `azure_storage.py:523` becomes:

```python
def store_ai_report(
    symbol: str,
    user_id: Any,
    payload: Dict[str, Any],
    *,
    archive_provenance: Optional[Dict[str, Any]] = None,
) -> bool:
```

**(c) The archive copy.** Insert between the end of the history-blob `try/except` at `azure_storage.py:580` and the
`# Latest pointer blob` comment at `:582`. Do not change `:551-580` or `:582-639` in any other way:

```python
        # EN-019: append-only archive copy carrying report provenance. Flag-gated, default OFF.
        # The dated history blob above and the latest pointer / report index below are unchanged.
        if report_archive_enabled():
            _write_report_archive_copy(
                enriched_payload=enriched_payload,
                archive_provenance=archive_provenance,
                history_blob_name=history_blob_name,
            )
```

**(d) New module-level functions.** Add `_write_report_archive_copy` immediately **above** `def store_ai_report(`
(`azure_storage.py:523`), and the four others immediately **after** `store_ai_report` ends (`:639`), before
`def store_super_agent_select_report(` (`:642`):

```python
def _write_report_archive_copy(
    *,
    enriched_payload: Dict[str, Any],
    archive_provenance: Optional[Dict[str, Any]],
    history_blob_name: str,
) -> Optional[str]:
    """Archive copy = the dated history payload plus one trailing key. Never raises."""
    try:
        provenance = archive_provenance if isinstance(archive_provenance, dict) else None
        trigger = provenance.get("trigger") if provenance else None
        archive_payload = {
            **enriched_payload,
            "report_provenance": provenance
            or {"schema": REPORT_PROVENANCE_SCHEMA, "trigger": None, "unstamped": True},
        }
        name = archive_blob_name(
            trigger=trigger,
            stored_at_utc=datetime.now(timezone.utc),
            history_blob_name=history_blob_name,
        )
        data = json.dumps(archive_payload, separators=(",", ":"), default=_json_fallback).encode("utf-8")
        return store_report_archive_blob(name, data)
    except Exception:  # noqa: BLE001 - the archive must never break the report write
        logger.exception("EN-019 archive copy failed for %s", history_blob_name)
        return None
```

```python
def _build_archive_container_name() -> str:
    return _ensure_valid_container_name(archive_container_setting())


def store_report_archive_blob(blob_name: str, data: bytes) -> Optional[str]:
    """Append-only write into the EN-019 archive container. Never overwrites, never raises.
    No latest pointer, no report index, no Report Center cache invalidation."""
    try:
        container_client = _get_container_client(_build_archive_container_name())
    except AzureStorageUnavailable as exc:
        logger.warning("Azure storage disabled: %s", exc)
        return None
    except Exception:  # noqa: BLE001
        logger.exception("Failed to initialise Azure storage client for the report archive")
        return None

    content_settings = ContentSettings(content_type="application/json")
    try:
        try:
            container_client.upload_blob(
                name=blob_name, data=data, overwrite=False, content_settings=content_settings
            )
            return blob_name
        except ResourceExistsError:
            collision = uuid.uuid4().hex[:8]
            fallback_name = (
                blob_name[: -len(".json")] + f"_{collision}.json"
                if blob_name.endswith(".json")
                else f"{blob_name}_{collision}"
            )
            container_client.upload_blob(
                name=fallback_name, data=data, overwrite=False, content_settings=content_settings
            )
            return fallback_name
    except Exception:  # noqa: BLE001
        logger.exception("Failed to write report archive blob %s", blob_name)
        return None


def list_report_archive_blob_names(prefix: str) -> Optional[List[str]]:
    """Names under a prefix in the archive container; None if the store is unavailable."""
    try:
        container_client = _get_container_client(_build_archive_container_name())
        return [str(blob.name) for blob in container_client.list_blobs(name_starts_with=prefix)]
    except Exception:  # noqa: BLE001
        logger.exception("Failed to list report archive blobs under %s", prefix)
        return None


def store_fixed_universe_report(
    symbol: str,
    user_id: Any,
    payload: Dict[str, Any],
    *,
    archive_provenance: Optional[Dict[str, Any]] = None,
) -> bool:
    """EN-019 report sink: archive container only. Same call shape as store_ai_report so
    app.run_batch_analysis_for_symbol can take it as report_sink. Refuses anything that is not
    a scheduled fixed-universe report."""
    provenance = archive_provenance if isinstance(archive_provenance, dict) else None
    if (
        not provenance
        or provenance.get("trigger") != TRIGGER_SCHEDULED_FIXED_UNIVERSE
        or not provenance.get("trading_date")
    ):
        logger.error("Fixed-universe report refused for %s: no scheduled_fixed_universe provenance", symbol)
        return False
    try:
        trading_date = date.fromisoformat(str(provenance["trading_date"]))
    except ValueError:
        logger.error("Fixed-universe report refused for %s: bad trading_date", symbol)
        return False

    safe_symbol = (symbol or "UNKNOWN").upper().replace("/", "-").replace(" ", "_")
    strategy_scope = _normalize_strategy_scope(payload.get("strategy_scope"))
    now_utc = datetime.now(timezone.utc)
    enriched = {
        **payload,
        "symbol": safe_symbol,
        "user_id": str(user_id),
        "stored_at": now_utc.replace(tzinfo=None).isoformat(timespec="seconds") + "Z",
        **({"strategy_scope": strategy_scope} if strategy_scope else {}),
        "report_provenance": provenance,
    }
    name = fixed_universe_report_blob_name(
        trading_date=trading_date,
        symbol=safe_symbol,
        strategy_scope=strategy_scope,
        stored_at_utc=now_utc,
        job_id=payload.get("ai_job_id"),
    )
    try:
        data = json.dumps(enriched, separators=(",", ":"), default=_json_fallback).encode("utf-8")
    except Exception:  # noqa: BLE001
        logger.exception("Fixed-universe report for %s could not be serialised", symbol)
        return False
    return store_report_archive_blob(name, data) is not None
```

`date`, `timezone`, `List`, `Optional`, `uuid`, `ContentSettings`, `ResourceExistsError` are already imported at
`azure_storage.py:1-13`; `_json_fallback` (`:1002`) and `AzureStorageUnavailable` (`:89`) are module-level.

### 3.4 `ai_agents/principal_agent.py`

**(a) Imports and prompt constants.** After `from .projection_expert import ProjectionExpertAgent`
(`ai_agents/principal_agent.py:30`) add `from services.report_provenance import apply_numeric_trigger_contract, classify_plan_sources`.
After `logger = logging.getLogger(__name__)` (`:33`) add:

```python
# EN-019: numeric trigger contract. Requested only by the fixed-universe research batch
# (scripts/run_fixed_universe_report_batch.py). Every other caller's prompt is unchanged.
NUMERIC_TRIGGER_SYSTEM_RULE = (
    "- For every buy_setup and sell_setup, also restate its trigger as numbers: trigger_price "
    "(the single price level the trigger sentence waits for), trigger_direction ('above' or "
    "'below' that level), and trigger_basis ('close' if the trigger waits for a bar to close "
    "beyond the level, 'touch' if trading through it is enough). Use null for any of the three "
    "the trigger sentence does not state.\n"
)
NUMERIC_TRIGGER_TEMPLATE_RULE = (
    "Inside every buy_setup and sell_setup ALSO include these three keys:\n"
    " \"trigger_price\": number | null,\n"
    " \"trigger_direction\": \"above\" | \"below\" | null,\n"
    " \"trigger_basis\": \"close\" | \"touch\" | null\n"
)
```

**(b) State** — `PrincipalAgentState` (`:36-44`): add `record_plan_sources: bool` and `numeric_trigger_contract: bool`.

**(c) `generate_trading_plan`** — signature `:140-149`: after `strategy_scope: Optional[str] = None,` add
`record_plan_sources: bool = False,` and `numeric_trigger_contract: bool = False,`. In `initial_state`
(`:169-174`), after `"raw_inputs": raw_inputs,` add:

```python
            **({"record_plan_sources": True} if record_plan_sources else {}),
            **({"numeric_trigger_contract": True} if numeric_trigger_contract else {}),
```

**(d) `_initialise_state`** — in the returned dict (`:213-218`), after `"raw_inputs": ...,` add:

```python
            **{key: True for key in ("record_plan_sources", "numeric_trigger_contract") if state.get(key)},
```

**(e) `_summarise_node`** (`:354-444`):
- After `model_raw_inputs = raw_inputs if include_raw else {}` (`:371`) add
  `record_plan_sources = bool(state.get("record_plan_sources"))` and
  `numeric_trigger_contract = bool(state.get("numeric_trigger_contract"))`.
- In the `_summarise_for_client(...)` call (`:373-378`), after `strategy_scope=strategy_scope,` add
  `numeric_trigger_contract=numeric_trigger_contract,`.
- After the scope filter (`:388-389`) and **before** `if not strategies:` (`:390`) add
  `llm_lane_keys = list(strategies.keys()) if isinstance(strategies, dict) else []`.
- After the supplement loop ends (`:409`) and before `generated_time = datetime.utcnow()` (`:411`) add:

```python
        if numeric_trigger_contract:
            strategies = apply_numeric_trigger_contract(strategies, llm_lane_keys)
```

- After `plan["usage"] = usage if usage else {}` (`:428`) add:

```python
        if record_plan_sources:
            plan["plan_sources"] = classify_plan_sources(llm_lane_keys, strategies)
```

**(f) `_summarise_for_client`** — signature `:501-508`: after `strategy_scope: Optional[str] = None,` add
`numeric_trigger_contract: bool = False,`. After the `system_prompt = (...)` expression closes (`:555`) add
`if numeric_trigger_contract: system_prompt += NUMERIC_TRIGGER_SYSTEM_RULE` (two lines). After the
`template_instruction = (...)` expression closes (`:585`) add
`if numeric_trigger_contract: template_instruction += NUMERIC_TRIGGER_TEMPLATE_RULE` (two lines).

Nothing else in this file changes. With both keywords at their defaults every byte of the prompt and the plan is
what it is today (§4(d)).

### 3.5 `app.py`

**(a) Import.** After the `from azure_storage import (...)` block (`app.py:117-126`) add:

```python
from services.report_provenance import (
    TRIGGER_INTERNAL_BATCH,
    TRIGGER_SCHEDULED_FIXED_UNIVERSE,
    TRIGGER_SUBSCRIBER,
    build_report_provenance,
    find_technical_timestamp,
    lane_blob_keys,
    report_archive_enabled,
)
```

**(b) `_run_and_persist_expert_analysis`** (`app.py:276-518`).

Signature: after `principal_strategy_scopes: Optional[List[str]] = None,` (`:289`) add:

```python
    trigger: str = TRIGGER_SUBSCRIBER,
    report_sink: Optional[Callable[..., Any]] = None,
    numeric_trigger_contract: bool = False,
    provenance_extra: Optional[Dict[str, Any]] = None,
```

After the `logger.info("Expert analysis started ...")` line (`:291`) add:

```python
    sink = report_sink if report_sink is not None else store_ai_report
    # EN-019: provenance is recorded for the archive copy (flag) and always for fixed-universe
    # research reports. It never enters job_result, the dated blob or any HTTP response.
    record_provenance = report_archive_enabled() or trigger == TRIGGER_SCHEDULED_FIXED_UNIVERSE
    plan_sources: Optional[Dict[str, str]] = None
```

Both `principal.generate_trading_plan(...)` calls (`:354-361` and `:388-395`): after the `strategy_scope=...,`
argument add `record_plan_sources=record_provenance,` and `numeric_trigger_contract=numeric_trigger_contract,`.

In the multi-scope loop, after the `if not isinstance(lane_plan, dict): ... continue` block (`:366-368`) and
**before** `if merged_plan is None:` (`:370`), add:

```python
                    lane_sources = lane_plan.pop("plan_sources", None)
                    if isinstance(lane_sources, dict):
                        plan_sources = {**(plan_sources or {}), **lane_sources}
```

In the single-call branch, immediately after the call closes (`:395`), still inside `else:`, add:

```python
                if isinstance(plan, dict):
                    popped_sources = plan.pop("plan_sources", None)
                    if isinstance(popped_sources, dict):
                        plan_sources = popped_sources
```

After `strategies = plan_data.get("strategies")` (`:479`) and before `if isinstance(strategies, dict) and strategies:`
(`:481`) add:

```python
    lane_keys_in_job = lane_blob_keys(strategies)

    def _provenance(strategy_scope: Optional[str]) -> Optional[Dict[str, Any]]:
        if not record_provenance:
            return None
        return build_report_provenance(
            trigger=trigger,
            job_id=job_id,
            strategy_scope=strategy_scope,
            lane_keys_in_job=lane_keys_in_job,
            plan_sources=plan_sources,
            technical_timestamp=find_technical_timestamp(technical_snapshot, symbol),
            utc_offset=datetime.now().astimezone().utcoffset(),
            analysis_completed_at_utc=datetime.now(timezone.utc),
            extra=provenance_extra,
        )
```

At `:493` replace `store_ai_report(` with `sink(` and add `archive_provenance=_provenance(lane_key_norm),` after the
payload dict (after `:503`). At `:507` replace `store_ai_report(` with `sink(` and add
`archive_provenance=_provenance(principal_strategy_scope),` after the payload dict (after `:514`). **The payload
dicts themselves (`:496-503`, `:510-514`) do not change.**

Before `logger.info("Expert analysis finished ...")` (`:517`) add:

```python
    if trigger == TRIGGER_SCHEDULED_FIXED_UNIVERSE:
        job_result["report_provenance_summary"] = {
            "plan_sources": plan_sources,
            "lane_keys_in_job": lane_keys_in_job,
        }
```

**(c) `_run_async_analysis_job`** (`app.py:521-617`, the `/analyze` background path). Signature: after
`price_action_period_overrides: Optional[Dict[str, str]] = None,` (`:537`) add `trigger: str = TRIGGER_SUBSCRIBER,`.
The `/analyze` call site (`app.py:3551-3568`) passes positional arguments and is **not edited**; the default
applies. In the `_run_and_persist_expert_analysis(...)` call (`:560-573`) add `trigger=trigger,`. In the error-path
`store_ai_report(...)` (`:606-616`), after the payload dict add:

```python
            archive_provenance=(
                build_report_provenance(
                    trigger=trigger,
                    job_id=job_id,
                    strategy_scope=None,
                    lane_keys_in_job=[],
                    plan_sources=None,
                    technical_timestamp=find_technical_timestamp(technical_snapshot, symbol),
                    utc_offset=datetime.now().astimezone().utcoffset(),
                    analysis_completed_at_utc=datetime.now(timezone.utc),
                    report_status="error",
                )
                if report_archive_enabled()
                else None
            ),
```

**(d) Extract the per-symbol batch body.** Add this function immediately **above**
`@app.post("/api/internal/batch-analyze")` (`app.py:3696`), i.e. after `class InternalGexRunRequest` (`:3688-3693`).
Its body is `app.py:3856-3988` moved, with only the substitutions the parameters imply
(`normalized` → `normalized_symbol`, `payload.price_action_*` → the `*_raw` parameters, `user_id=1` / `1` →
`user_id`, `item["ai_job_id"] = ai_job_id` → `on_job_id`, `store_ai_report` → the sink):

```python
def run_batch_analysis_for_symbol(
    *,
    normalized_symbol: str,
    market: str,
    use_ai: bool,
    use_principal: bool,
    use_earnings: bool,
    include_principal_raw: bool,
    principal_strategy_scope: Optional[str],
    principal_strategy_scopes: Optional[List[str]],
    price_action_timeframes_raw: Any,
    price_action_period_overrides_raw: Any,
    api_key: str,
    secret_key: str,
    base_url: str,
    user_id: int = 1,
    trigger: str = TRIGGER_INTERNAL_BATCH,
    report_sink: Optional[Callable[..., Any]] = None,
    numeric_trigger_contract: bool = False,
    provenance_extra: Optional[Dict[str, Any]] = None,
    on_job_id: Optional[Callable[[Optional[str]], None]] = None,
) -> Dict[str, Any]:
    """One symbol of the internal batch (moved from _run_batch, EN-019). Raises on failure."""
    allowed_scopes = {"day_trading", "swing_trading", "longterm_trading"}
    lane_timeframes = {
        "day_trading": ['15m', '30m', '1h', '4h'],
        "swing_trading": ['1h', '4h', '1d'],
        "longterm_trading": ['1d', '1wk', '1mo'],
    }

    requested_timeframes: List[str] = ['5m', '15m', '30m', '1h', '4h', '1d', '1wk', '1mo']
    selected_scopes: List[str] = []
    if isinstance(principal_strategy_scopes, list) and principal_strategy_scopes:
        selected_scopes = list(principal_strategy_scopes)
    elif isinstance(principal_strategy_scope, str) and principal_strategy_scope in allowed_scopes:
        selected_scopes = [principal_strategy_scope]

    if selected_scopes:
        union_timeframes: List[str] = []
        for scope in selected_scopes:
            for tf in lane_timeframes.get(scope, []):
                if tf not in union_timeframes:
                    union_timeframes.append(tf)
        if union_timeframes:
            requested_timeframes = union_timeframes

    base_period = "5y"
    if "1mo" in requested_timeframes:
        base_period = "10y"

    agent = MultiSymbolDayTraderAgent(
        symbols=normalized_symbol,
        timeframes=requested_timeframes,
        base_period=base_period,
        market=market,
    )
    agent.set_credentials(api_key=api_key, secret_key=secret_key, base_url=base_url)
    try:
        indicator_fetcher.set_credentials(api_key, secret_key, base_url=base_url)
    except Exception as cred_error:  # noqa: BLE001
        logger.warning("Failed to configure shared indicator credentials: %s", cred_error)

    agent.set_trading_parameters(
        buy_threshold=70,
        sell_threshold=70,
        high_confidence_only=True,
    )

    results = agent.run_sequential()
    result_data = None
    technical_snapshot: Dict[str, Any] = {}
    if results:
        result_data = agent.export_results(results)
        if isinstance(result_data, (list, tuple)) and len(result_data) > 1:
            if isinstance(result_data[1], str):
                technical_snapshot = json.loads(result_data[1])
            elif isinstance(result_data[1], dict):
                technical_snapshot = result_data[1]

    price_action_timeframes: Optional[List[str]] = None
    if isinstance(price_action_timeframes_raw, str):
        parts = [
            tf.strip()
            for tf in price_action_timeframes_raw.split(',')
            if tf and tf.strip()
        ]
        price_action_timeframes = parts or None
    elif isinstance(price_action_timeframes_raw, (list, tuple, set)):
        converted = [str(tf).strip() for tf in price_action_timeframes_raw if str(tf).strip()]
        price_action_timeframes = converted or None

    # If the caller did not specify timeframes, default to the strategy lane subset.
    if price_action_timeframes is None and selected_scopes:
        price_action_timeframes = list(requested_timeframes)

    price_action_period_overrides: Optional[Dict[str, str]] = None
    if isinstance(price_action_period_overrides_raw, dict):
        cleaned_overrides = {
            str(key): str(value)
            for key, value in price_action_period_overrides_raw.items()
            if value is not None and str(value).strip()
        }
        price_action_period_overrides = cleaned_overrides or None

    price_action_snapshot: Optional[Dict[str, Any]] = None
    try:
        price_action_snapshot = price_action_analyzer.analyze(
            normalized_symbol,
            timeframes=price_action_timeframes,
            period_overrides=price_action_period_overrides,
            market=market,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Price action analysis failed for %s", normalized_symbol)
        price_action_snapshot = {
            "success": False,
            "symbol": normalized_symbol,
            "error": str(exc),
        }

    background_requested = (use_ai or use_principal or use_earnings) and result_data is not None
    ai_job_id = str(uuid.uuid4()) if background_requested else None
    if on_job_id is not None:
        on_job_id(ai_job_id)

    if ai_job_id:
        job_result = _run_and_persist_expert_analysis(
            job_id=ai_job_id,
            technical_data=result_data,
            technical_snapshot=technical_snapshot,
            price_action_snapshot=price_action_snapshot,
            symbol=normalized_symbol,
            user_id=user_id,
            include_ai=use_ai,
            include_principal=use_principal,
            include_earnings=use_earnings,
            include_principal_raw=include_principal_raw,
            principal_strategy_scope=principal_strategy_scope,
            principal_strategy_scopes=principal_strategy_scopes,
            trigger=trigger,
            report_sink=report_sink,
            numeric_trigger_contract=numeric_trigger_contract,
            provenance_extra=provenance_extra,
        )
        return {"ai_job_id": ai_job_id, "job_result": job_result}

    # Persist the baseline (technical + price action) report so it shows in Report Center
    sink = report_sink if report_sink is not None else store_ai_report
    record_provenance = report_archive_enabled() or trigger == TRIGGER_SCHEDULED_FIXED_UNIVERSE
    sink(
        normalized_symbol,
        user_id,
        {
            "ai_job_id": None,
            "status": "done",
            "ai_analysis": None,
            "principal_plan": None,
            "earnings_analysis": None,
            "technical_snapshot": technical_snapshot,
            "price_action_snapshot": price_action_snapshot,
        },
        archive_provenance=(
            build_report_provenance(
                trigger=trigger,
                job_id=None,
                strategy_scope=None,
                lane_keys_in_job=[],
                plan_sources=None,
                technical_timestamp=find_technical_timestamp(technical_snapshot, normalized_symbol),
                utc_offset=datetime.now().astimezone().utcoffset(),
                analysis_completed_at_utc=datetime.now(timezone.utc),
                extra=provenance_extra,
            )
            if record_provenance
            else None
        ),
    )
    return {"ai_job_id": None, "job_result": None}
```

**(e) `_run_batch` now calls it.** Replace the body of the `try:` at `app.py:3855` — lines `:3856-3989` — with the
call below. Lines `:3990-3998` (`item["status"] = "done"` … the `except` block) stay exactly as they are:

```python
                run_batch_analysis_for_symbol(
                    normalized_symbol=normalized,
                    market=market,
                    use_ai=use_ai,
                    use_principal=use_principal,
                    use_earnings=use_earnings,
                    include_principal_raw=include_principal_raw,
                    principal_strategy_scope=principal_strategy_scope,
                    principal_strategy_scopes=principal_strategy_scopes,
                    price_action_timeframes_raw=payload.price_action_timeframes,
                    price_action_period_overrides_raw=payload.price_action_period_overrides,
                    api_key=api_key,
                    secret_key=secret_key,
                    base_url=base_url,
                    user_id=1,
                    trigger=TRIGGER_INTERNAL_BATCH,
                    on_job_id=lambda job_id, _item=item: _item.__setitem__("ai_job_id", job_id),
                )

```

The ad-hoc endpoint's behaviour is unchanged: same analyses, same payloads, same dated blobs, and `item["ai_job_id"]`
is still set before the analysis runs, so a poll mid-analysis sees it exactly as today. The HTTP handlers
`/analyze` (`app.py:3286-3629`) and `/api/ai-analysis-result/{job_id}` (`:3630-3673`) are **not edited**
(§4(b) hashes them).

### 3.6 New file — `scripts/run_fixed_universe_report_batch.py`

```python
"""EN-019: nightly multi-agent report batch on a fixed, pre-declared universe.

Flag-gated: FIXED_UNIVERSE_REPORT_BATCH_ENABLED (default OFF), read BEFORE any heavy import.
With the flag off this script imports only the standard library and the pure
services.fixed_universe_batch module, opens no database connection and touches no blob.

Writes: blobs in the EN-019 archive container only (AI_REPORT_ARCHIVE_CONTAINER).
Never writes a database row, never writes an ai-reports-YYYY-MM-DD container, never sends email.
Reads: super_agent_select_runs / super_agent_select_candidates_daily for the trading date, and the
scheduler digest blob that says whether tonight's nightly pipeline has finished.
"""

from __future__ import annotations

import sys
import threading
import time as _time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from services.fixed_universe_batch import batch_enabled  # noqa: E402  (pure)

LANES_ALL = ["day_trading", "swing_trading", "longterm_trading"]


def _log(message: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"{stamp} fixed_universe_batch {message}", flush=True)


def _start_heartbeat(interval_seconds: int = 30) -> threading.Event:
    """Triggered WebJobs are stopped after a silent idle period; an LLM call can be silent."""
    stop = threading.Event()

    def _beat() -> None:
        while not stop.wait(interval_seconds):
            _log("heartbeat")

    threading.Thread(target=_beat, name="fixed-universe-heartbeat", daemon=True).start()
    return stop


def main(argv: Optional[List[str]] = None) -> int:
    if not batch_enabled():
        print("fixed universe report batch disabled (FIXED_UNIVERSE_REPORT_BATCH_ENABLED off)")
        return 0
    return _run(list(sys.argv[1:] if argv is None else argv))


def _dumps(body: Dict[str, Any]) -> bytes:
    import json

    return json.dumps(body, separators=(",", ":"), default=str).encode("utf-8")


def _run(argv: List[str]) -> int:
    import argparse
    import os

    parser = argparse.ArgumentParser(description="EN-019 fixed-universe multi-agent report batch")
    parser.add_argument(
        "--declare-only",
        action="store_true",
        help="Resolve and print tonight's universe from the database; analyse nothing, write nothing.",
    )
    args = parser.parse_args(argv)

    try:
        from dotenv import load_dotenv

        load_dotenv(_REPO_ROOT / ".env")
    except Exception:  # noqa: BLE001
        pass

    from core.market_sessions import ET, get_market_session_state
    from services.fixed_universe_batch import (
        FIXED_UNIVERSE_ID,
        batch_settings,
        declare_universe,
        fixed_universe_manifest_blob_name,
        fixed_universe_prefix,
        is_past,
        jobs_entry_from_result,
        pipeline_status,
        settings_for_manifest,
        summarise_completed_run,
    )
    from services.report_provenance import TRIGGER_SCHEDULED_FIXED_UNIVERSE

    state = get_market_session_state()
    if not state.nightly_eligible or state.nightly_trading_date is None:
        _log(f"status=skipped reason={state.nightly_reason}")
        return 0
    trading_date = state.nightly_trading_date
    settings = batch_settings()
    run_id = uuid.uuid4().hex[:12]
    heartbeat = _start_heartbeat()
    try:
        from azure_storage import (
            fetch_ai_job_result,
            list_report_archive_blob_names,
            store_fixed_universe_report,
            store_report_archive_blob,
        )
        from services.job_notifications import JOB_STATUS_DIGEST_USER, _digest_job_id, _job_key

        def _manifest(kind: str, body: Dict[str, Any]) -> Optional[str]:
            name = fixed_universe_manifest_blob_name(trading_date=trading_date, kind=kind, run_id=run_id)
            return store_report_archive_blob(name, _dumps(body))

        existing = list_report_archive_blob_names(fixed_universe_prefix(trading_date) + "_")
        if existing is None:
            _log("status=aborted reason=archive_unavailable")
            return 0
        if not args.declare_only and any(("_declared_" in n or "_skipped_" in n) for n in existing):
            _log(f"status=skipped reason=already_declared trading_date={trading_date.isoformat()}")
            return 0

        # 1. Wait for tonight's nightly pipeline to finish: it shares Alpaca and CPU with this job.
        status: Optional[str] = None
        if not args.declare_only:
            digest_id = _digest_job_id(state.calendar_date)
            job_key = _job_key("Nightly Pipeline")
            while True:
                status = pipeline_status(fetch_ai_job_result(digest_id, JOB_STATUS_DIGEST_USER), job_key)
                if status in ("success", "failed"):
                    break
                if is_past(datetime.now(ET), settings["start_deadline_et"]):
                    _manifest(
                        "skipped",
                        {
                            "universe_id": FIXED_UNIVERSE_ID,
                            "run_id": run_id,
                            "trading_date": trading_date.isoformat(),
                            "reason": "pipeline_not_finished_by_deadline",
                            "pipeline_status": status,
                            "at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            "settings": settings_for_manifest(settings),
                        },
                    )
                    _log(f"status=skipped reason=pipeline_not_finished_by_deadline pipeline_status={status}")
                    return 0
                _log(f"waiting for nightly pipeline status={status}")
                _time.sleep(settings["poll_seconds"])

        # 2. Declare the universe from data that exists now. Read-only session; nothing is written.
        import app  # noqa: F401 - production import order (scripts/snapshot_insider_watch.py:32)
        from app import run_batch_analysis_for_symbol
        from db import SessionLocal
        from models import SuperAgentSelectCandidateDaily, SuperAgentSelectRun
        from symbol_map import SymbolNotFound, normalize_symbol

        declared_at = datetime.now(timezone.utc)
        sas_run: Optional[Dict[str, Any]] = None
        candidates: List[Dict[str, Any]] = []
        with SessionLocal() as session:
            run_row = (
                session.query(SuperAgentSelectRun)
                .filter(SuperAgentSelectRun.trading_date == trading_date)
                .one_or_none()
            )
            if run_row is not None:
                finished = run_row.finished_at
                if finished is not None and finished.tzinfo is None:
                    finished = finished.replace(tzinfo=timezone.utc)
                sas_run = {"id": run_row.id, "status": run_row.status, "finished_at_utc": finished}
                rows = (
                    session.query(
                        SuperAgentSelectCandidateDaily.symbol,
                        SuperAgentSelectCandidateDaily.overall_score,
                        SuperAgentSelectCandidateDaily.qualified,
                        SuperAgentSelectCandidateDaily.selected_rank,
                    )
                    .filter(
                        SuperAgentSelectCandidateDaily.trading_date == trading_date,
                        SuperAgentSelectCandidateDaily.run_id == run_row.id,
                    )
                    .all()
                )
                candidates = [
                    {
                        "symbol": row.symbol,
                        "overall_score": row.overall_score,
                        "qualified": bool(row.qualified),
                        "selected_rank": row.selected_rank,
                    }
                    for row in rows
                ]
            session.rollback()

        declaration = declare_universe(
            trading_date=trading_date,
            declared_at_utc=declared_at,
            sas_run=sas_run,
            sas_candidates=candidates,
            max_symbols=settings["max_symbols"],
        )
        declaration.update(
            {
                "run_id": run_id,
                "trigger": TRIGGER_SCHEDULED_FIXED_UNIVERSE,
                "pipeline_status_at_declaration": status,
                "numeric_trigger_contract": True,
                "analysis": {
                    "use_ai_analysis": False,
                    "use_principal_agent": True,
                    "use_earnings_agent": False,
                    "include_principal_raw_results": False,
                    "principal_strategy_scopes": LANES_ALL,
                    "market": "equity",
                    "user_id": 1,
                },
                "settings": settings_for_manifest(settings),
            }
        )
        if args.declare_only:
            import json

            print(json.dumps(declaration, indent=2, default=str))
            return 0
        if _manifest("declared", declaration) is None:
            _log("status=aborted reason=declaration_not_written")
            return 0
        _log(
            f"declared trading_date={trading_date.isoformat()} n={len(declaration['symbols'])} "
            f"sas_component={declaration['sas_component']} sha256={declaration['symbols_sha256']}"
        )

        # 3. Analyse in declared order. Symbols not started before the stop time are recorded.
        api_key = os.getenv("ALPACA_API_KEY")
        secret_key = os.getenv("ALPACA_SECRET_KEY")
        base_url = os.getenv("ALPACA_BASE_URL", "https://api.alpaca.markets")
        started_at = datetime.now(timezone.utc)
        jobs: List[Dict[str, Any]] = []
        stop_reason = "universe_exhausted"
        if not api_key or not secret_key:
            stop_reason = "alpaca_credentials_missing"
        for entry in declaration["entries"]:
            symbol = entry["symbol"]
            if stop_reason == "alpaca_credentials_missing":
                jobs.append({"symbol": symbol, "status": "not_started_credentials", "job_id": None})
                continue
            if is_past(datetime.now(ET), settings["stop_et"]):
                stop_reason = "stop_time_reached"
                jobs.append({"symbol": symbol, "status": "not_started_stop_time", "job_id": None})
                continue
            t0 = datetime.now(timezone.utc)
            try:
                normalized, _message = normalize_symbol(symbol, market="equity")
            except SymbolNotFound as exc:
                jobs.append({"symbol": symbol, "status": "symbol_not_found", "job_id": None, "error": str(exc)[:300]})
                continue
            try:
                outcome = run_batch_analysis_for_symbol(
                    normalized_symbol=normalized,
                    market="equity",
                    use_ai=False,
                    use_principal=True,
                    use_earnings=False,
                    include_principal_raw=False,
                    principal_strategy_scope=None,
                    principal_strategy_scopes=list(LANES_ALL),
                    price_action_timeframes_raw=None,
                    price_action_period_overrides_raw=None,
                    api_key=api_key,
                    secret_key=secret_key,
                    base_url=base_url,
                    user_id=1,
                    trigger=TRIGGER_SCHEDULED_FIXED_UNIVERSE,
                    report_sink=store_fixed_universe_report,
                    numeric_trigger_contract=True,
                    provenance_extra={
                        "universe_id": FIXED_UNIVERSE_ID,
                        "universe_run_id": run_id,
                        "trading_date": trading_date.isoformat(),
                        "universe_sources": list(entry["sources"]),
                        "numeric_trigger_contract": True,
                    },
                )
                jobs.append(
                    jobs_entry_from_result(
                        symbol=symbol,
                        outcome=outcome,
                        started_at_utc=t0,
                        finished_at_utc=datetime.now(timezone.utc),
                    )
                )
            except Exception as exc:  # noqa: BLE001 - one symbol never stops the night
                jobs.append({"symbol": symbol, "status": "error", "job_id": None, "error": str(exc)[:500]})
            _log(f"symbol={symbol} status={jobs[-1]['status']}")
            _time.sleep(settings["pause_seconds"])

        completed = summarise_completed_run(
            declaration=declaration,
            jobs=jobs,
            started_at_utc=started_at,
            finished_at_utc=datetime.now(timezone.utc),
            stop_reason=stop_reason,
        )
        _manifest("completed", completed)
        _log(
            f"status=completed trading_date={trading_date.isoformat()} "
            f"analyses={completed['n_analyses']} statuses={completed['status_counts']} stop_reason={stop_reason}"
        )
        return 0
    finally:
        heartbeat.set()


if __name__ == "__main__":
    raise SystemExit(main())
```

### 3.7 New WebJob — `app_data/jobs/triggered/fixed_universe_report_batch/`

`settings.job`:

```json
{
  "schedule": "0 30 18 * * 1-5",
  "is_singleton": true,
  "stopping_wait_time": 60,
  "shutdownGraceTimeLimit": 1800
}
```

`run.py`: copy `app_data/jobs/triggered/nightly_pipeline/run.py` byte-for-byte, then replace only `main()`
(`app_data/jobs/triggered/nightly_pipeline/run.py:83-107`) with:

```python
def main() -> int:
    script_name = "run_fixed_universe_report_batch.py"
    repo_root = _resolve_repo_root(script_name)
    script_path = repo_root / "scripts" / script_name
    python_executable = _resolve_python_executable(repo_root)
    cmd = [str(python_executable), str(script_path)]
    return subprocess.run(cmd, cwd=str(repo_root), check=False).returncode
```

Cron is interpreted in `WEBSITE_TIME_ZONE = America/New_York` (`docs/AZURE_WEBJOBS_AUTOMATION.md:12`), so 18:30 is
Eastern in both EDT and EST. The existing wrapper is not edited.


### 3.8 Docs

**(a) `docs/AZURE_WEBJOBS_AUTOMATION.md`** — add one row after `blacklist_check` (`:22`):

```markdown
| `fixed_universe_report_batch` | `0 30 18 * * 1-5` | 18:30 | `scripts/run_fixed_universe_report_batch.py` | **Flag-gated** `FIXED_UNIVERSE_REPORT_BATCH_ENABLED` (default OFF). EN-019 research batch: multi-agent reports on a fixed, pre-declared universe, archive container only; waits for the nightly pipeline, writes no DB row. See `docs/FIXED_UNIVERSE_REPORT_BATCH.md` |
```

**(b) New `docs/FIXED_UNIVERSE_REPORT_BATCH.md`:**

```markdown
# Fixed-universe multi-agent report batch and report archive (EN-019)

Research plumbing. No subscriber-visible surface reads anything described here.

## What runs
WebJob `fixed_universe_report_batch`, 18:30 ET Mon–Fri, only when `FIXED_UNIVERSE_REPORT_BATCH_ENABLED` is on.
1. Skips non-trading days (`core/market_sessions.py`) and nights already declared.
2. Waits (poll `FIXED_UNIVERSE_REPORT_BATCH_POLL_SECONDS`, default 60) until the scheduler digest records the
   nightly pipeline as success or failed. Not finished by `..._START_DEADLINE_ET` (21:00) → writes `_skipped_`, stops.
3. Declares `fixed_universe_v1`: `LIQUID_LIST_V1` (20 names, never edited) + the night's SAS candidates from a run
   that finished before the declaration; order liquid → published by rank → others by score; cap
   `..._MAX_SYMBOLS` (80). Writes `_declared_<run_id>.json` before the first analysis.
4. Analyses each symbol in order (principal agent, all lanes, 7 timeframes, no AI summary, no earnings), with the
   numeric trigger contract. Stops starting symbols at `..._STOP_ET` (22:15). Writes `_completed_<run_id>.json`.

## Where it writes
Container `AI_REPORT_ARCHIVE_CONTAINER` (default `vx-report-archive`), append-only (`overwrite=False`):
- `fixed_universe/<trading_date>/_declared_|_completed_|_skipped_<run_id>.json`
- `fixed_universe/<trading_date>/<SYMBOL>_<lane>_<UTC stamp>_<job_id>.json`
Never a dated `ai-reports-YYYY-MM-DD` container, a `_latest` pointer, `user_report_index`, email or digest.

## The archive copy of ordinary reports
With `AI_REPORT_ARCHIVE_ENABLED`, every report `store_ai_report` writes also gets
`reports/<UTC date>/<trigger>/<history blob name>` in the archive: the dated payload plus one trailing key,
`report_provenance`. The dated blob, `_latest` pointer, report index and HTTP responses are unchanged.

## `report_provenance` (schema `report_provenance_v1`)
`trigger` (`subscriber` | `internal_batch` | `scheduled_fixed_universe`), `job_id`, `report_status`,
`strategy_scope`, `blobs_in_job`, `lane_keys_in_job`, `plan_source` / `plan_sources` (`llm` | `fallback_template`),
`technical_timestamp_raw` (the zone-less engine clock), `technical_timestamp_iso` (same instant, explicit offset),
`process_utc_offset`, `analysis_completed_at_utc`; fixed-universe reports add `universe_id`, `universe_run_id`,
`trading_date`, `universe_sources`, `numeric_trigger_contract`.
Fixed-universe plans also carry `trigger_price`, `trigger_direction` (`above`|`below`), `trigger_basis`
(`close`|`touch`) and `trigger_fields_complete` on every setup — the model's own statement, never parsed from text.
```

---

## 4. Before / after check — repository only, no database, no blob store

Run all of these and paste the outputs into the PR. None opens a connection: §4(d) stubs `db` and replaces the
Azure container client with an in-memory fake before anything is called. Importing `ai_agents.principal_agent`
pulls `indicator_fetcher` → `symbol_map`, which may try the Alpaca asset catalogue and fall back offline — slow,
not a DB call. **`DATABASE_URL` must be unset in the shell for every command in this section**
(PowerShell: `Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue`).

**(a) The touched-file list is exactly the allowed list.**

```
git diff --stat c311e81..HEAD
```

Must list exactly these 11 paths and nothing else: `app.py`, `azure_storage.py`, `ai_agents/principal_agent.py`,
`services/report_provenance.py`, `services/fixed_universe_batch.py`, `scripts/run_fixed_universe_report_batch.py`,
`app_data/jobs/triggered/fixed_universe_report_batch/run.py`,
`app_data/jobs/triggered/fixed_universe_report_batch/settings.job`, `tests/test_report_provenance.py`,
`docs/AZURE_WEBJOBS_AUTOMATION.md`, `docs/FIXED_UNIVERSE_REPORT_BATCH.md`.

**(b) + (d) Rule-11 inertness hashes — the old path, byte for byte, at the base commit and at HEAD.**

Create a detached checkout of the base commit beside the repo, and save the script below **outside both trees**
(for example `%TEMP%\en019_inertness.py`):

```
git worktree add --detach ..\volatilx-en019-base c311e81
```

```python
"""EN-019 inertness hashes. Run from a platform checkout root, DATABASE_URL unset.
Base (c311e81) and HEAD must print identical lines."""
import hashlib, json, os, sys, types
from datetime import datetime, timezone

os.environ.pop("DATABASE_URL", None)
os.environ.pop("AZURE_STORAGE_CONTAINER", None)
for key in [k for k in os.environ if k.startswith(("AI_REPORT_", "FIXED_UNIVERSE_REPORT_BATCH_"))]:
    os.environ.pop(key)
sys.path.insert(0, os.getcwd())
sys.modules["db"] = types.ModuleType("db")  # any `from db import SessionLocal` fails: no connection possible


class Frozen(datetime):
    @classmethod
    def utcnow(cls):
        return datetime(2026, 9, 11, 22, 31, 2)

    @classmethod
    def now(cls, tz=None):
        aware = datetime(2026, 9, 11, 22, 31, 2, tzinfo=timezone.utc)
        return aware.astimezone(tz) if tz is not None else datetime(2026, 9, 11, 18, 31, 2)


def sha(obj):
    return hashlib.sha256(json.dumps(obj, default=str).encode("utf-8")).hexdigest()


# 1. Subscriber HTTP handlers: /analyze and /api/ai-analysis-result, source text.
text = open("app.py", encoding="utf-8").read().replace("\r\n", "\n")
start = text.index('@app.post("/analyze")\n')
end = text.index("class InternalBatchAnalyzeRequest(BaseModel):")
print("handlers_source", hashlib.sha256(text[start:end].encode("utf-8")).hexdigest())

# 2. Principal prompt on the default path.
import ai_agents.principal_agent as pa
pa.datetime = Frozen
agent = object.__new__(pa.PrincipalAgent)
agent.model, agent.reasoning_effort, agent.text_verbosity, agent.max_output_tokens = "gpt-5.6-terra", "low", "medium", 3200
captured = {}
def capture(body):
    captured["body"] = body
    raise RuntimeError("captured")
agent._create_responses_call = capture
try:
    agent._summarise_for_client("SNDK", {"technical": {"summary": "x"}}, {}, strategy_scope=None)
except RuntimeError:
    pass
print("principal_prompt", sha(captured["body"]))

# 3. Principal plan on the default path (day + swing from the model, long-term from the template).
LLM = {
    "day_trading": {
        "summary": "Day plan", "time_expectation": "hours",
        "buy_setup": {"trigger": "If price closes above 1638.36", "entry": 1638.36, "stop": 1624.55, "targets": [1650.0, 1662.5], "invalidation": 1620.0},
        "sell_setup": {"trigger": "If price closes below 1624.55", "entry": 1624.55, "stop": 1638.36, "targets": [1610.0, 1598.0], "invalidation": 1642.0},
        "no_trade_zone": {"min": 1624.55, "max": 1638.36, "reason": "range"},
    },
    "swing_trading": {
        "summary": "Swing plan", "time_expectation": "days",
        "buy_setup": {"trigger": "If price closes above 1700", "entry": 1700.0, "stop": 1600.0, "targets": [1800.0, 1900.0], "invalidation": 1590.0},
        "sell_setup": {"trigger": "If price trades below 1550", "entry": 1550.0, "stop": 1650.0, "targets": [1450.0, 1400.0], "invalidation": 1660.0},
    },
}
agent._summarise_for_client = lambda *a, **k: (json.loads(json.dumps(LLM)), {"total_tokens": 10}, "raw")
state = {"symbol": "SNDK", "strategy_scope": None, "include_raw_results": False, "raw_inputs": {}, "expert_outputs": {}}
print("principal_plan", sha(agent._summarise_node(state)))

# 4. The dated history blob and latest pointer, as bytes.
import azure_storage as az
az.datetime = Frozen
uploads = []
class FakeContainer:
    def __init__(self, name):
        self.container_name = name
    def upload_blob(self, name, data, overwrite, content_settings):
        uploads.append([self.container_name, name, bytes(data).decode("utf-8"), overwrite])
az._get_container_client = lambda name: FakeContainer(name)
payload = {"ai_job_id": "job-en019", "status": "done", "strategy_scope": "day_trading",
           "technical_snapshot": {"SNDK": {"timestamp": "2026-09-11 18:31:02"}},
           "principal_plan": {"success": True, "data": {"strategies": {"day_trading": {"summary": "x"}}}}}
az.store_ai_report("SNDK", 1, payload)
print("dated_blobs", sha(uploads))
print("overwrite_true_count", open("azure_storage.py", encoding="utf-8").read().count("overwrite=True"))
```

```
cd ..\volatilx-en019-base && python %TEMP%\en019_inertness.py
cd <platform repo> && python %TEMP%\en019_inertness.py
git worktree remove ..\volatilx-en019-base
```

Use the platform repo's own interpreter for both runs. **All five lines must be identical between the two runs.**
`handlers_source` proves the subscriber handlers were not edited; `principal_prompt` and `principal_plan` prove
the default-argument path (every existing caller, including the SAS report service) produces the same prompt and
the same plan bytes; `dated_blobs` proves `store_ai_report` with the flag off writes the same two blobs with the
same names, bytes and overwrite modes; `overwrite_true_count` proves no new overwriting write exists. If any line
differs, the change is not inert — fix the code, not the check.

**(c) Files the nightly pipeline, SAS and subscriber surfaces run on are untouched.**

```
git diff --quiet c311e81..HEAD -- scripts/run_nightly_pipeline.py app_data/jobs/triggered/nightly_pipeline day_trading_agent.py indicator_fetcher.py symbol_map.py services/super_agent_select_report_service.py services/super_agent_select_service.py services/job_notifications.py services/uoa_scheduler.py ai_agents/omega_agent.py ai_agents/expert_agent.py routers templates static models.py db.py conftest.py core && echo UNCHANGED
```

Must print `UNCHANGED`.

**(e) The flags are off by default and the new modules are import-pure.**

```
python -c "import os,sys; [os.environ.pop(k) for k in list(os.environ) if k.startswith(('AI_REPORT_','FIXED_UNIVERSE_REPORT_BATCH_','DATABASE_URL'))]; import services.report_provenance as p, services.fixed_universe_batch as f; assert p.report_archive_enabled() is False and f.batch_enabled() is False; assert not {'db','models','app','azure_storage','sqlalchemy'} & set(sys.modules), sorted({'db','models','app','azure_storage','sqlalchemy'} & set(sys.modules)); print('EN-019 flags default OFF; pure modules import nothing heavy: OK')"
```

**(f) The test file:** `python tests/test_report_provenance.py` → `EN-019: 11/11 checks passed`. Do **not** run
`python -m pytest` (header). If you have a disposable scratch `DATABASE_URL` you may run the full suite against it
and say so in the PR; otherwise state that you skipped it.

---

## 5. Test — `tests/test_report_provenance.py`

Synthetic fixture by design: no report, candidate row or outcome from the desk's frozen data is used (plumbing,
nothing to seed). The SNDK levels 1638.36 / 1624.55 are the illustrative sample quoted in `research/BACKLOG.md` F9.
`T2` must run first (it checks what the flag-off script imports).

```python
"""EN-019 / PI-019 — report provenance, archive copy and the fixed-universe batch: offline tests.

No database, no network writes, no app import. Run as
    python tests/test_report_provenance.py
with DATABASE_URL unset. Do NOT run under pytest in an environment whose DATABASE_URL points at a
real database: conftest.py:31-55 runs create_tables() and deletes every users row around each test.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import types
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

os.environ.pop("DATABASE_URL", None)
_DB_STUB = types.ModuleType("db")
sys.modules.setdefault("db", _DB_STUB)  # any `from db import SessionLocal` raises ImportError

_ENV_PREFIXES = ("AI_REPORT_", "FIXED_UNIVERSE_REPORT_BATCH_")


def _clear_flags():
    for key in [k for k in os.environ if k.startswith(_ENV_PREFIXES)]:
        os.environ.pop(key)
    os.environ.pop("AZURE_STORAGE_CONTAINER", None)


class _Frozen(datetime):
    @classmethod
    def utcnow(cls):
        return datetime(2026, 9, 11, 22, 31, 2)

    @classmethod
    def now(cls, tz=None):
        aware = datetime(2026, 9, 11, 22, 31, 2, tzinfo=timezone.utc)
        return aware.astimezone(tz) if tz is not None else datetime(2026, 9, 11, 18, 31, 2)


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------
_LIQUID = (
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "TSLA", "JPM", "V",
    "LLY", "UNH", "XOM", "WMT", "MA", "COST", "HD", "PG", "JNJ", "BAC",
)
TD = date(2026, 9, 11)
SAS_RUN = {"id": 4242, "status": "success", "finished_at_utc": datetime(2026, 9, 11, 21, 12, 36, tzinfo=timezone.utc)}
DECLARED = datetime(2026, 9, 11, 22, 30, 0, tzinfo=timezone.utc)
SAS_ROWS = [
    {"symbol": "SNDK", "overall_score": 91.2, "qualified": True, "selected_rank": 1},
    {"symbol": "NVDA", "overall_score": 90.4, "qualified": True, "selected_rank": 2},
    {"symbol": "wdc ", "overall_score": 88.0, "qualified": True, "selected_rank": None},
    {"symbol": "MU", "overall_score": 79.5, "qualified": False, "selected_rank": None},
    {"symbol": "QCOM", "overall_score": None, "qualified": False, "selected_rank": None},
    {"symbol": "AMD", "overall_score": 84.1, "qualified": False, "selected_rank": None},
    {"symbol": "AAPL", "overall_score": 70.0, "qualified": False, "selected_rank": None},
    {"symbol": "", "overall_score": 99.0, "qualified": True, "selected_rank": 3},
]
_PAYLOAD = {
    "ai_job_id": "job-en019",
    "status": "done",
    "strategy_scope": "day_trading",
    "technical_snapshot": {"SNDK": {"timestamp": "2026-09-11 18:31:02"}},
    "principal_plan": {"success": True, "data": {"strategies": {"day_trading": {"summary": "x"}}}},
}
_LLM_SUMMARY = {
    "day_trading": {
        "summary": "Day plan", "time_expectation": "hours",
        "buy_setup": {"trigger": "If price closes above 1638.36", "entry": 1638.36, "stop": 1624.55,
                      "targets": [1650.0, 1662.5], "invalidation": 1620.0},
        "sell_setup": {"trigger": "If price closes below 1624.55", "entry": 1624.55, "stop": 1638.36,
                       "targets": [1610.0, 1598.0], "invalidation": 1642.0},
        "no_trade_zone": {"min": 1624.55, "max": 1638.36, "reason": "range"},
    },
    "swing_trading": {
        "summary": "Swing plan", "time_expectation": "days",
        "buy_setup": {"trigger": "If price closes above 1700", "entry": 1700.0, "stop": 1600.0,
                      "targets": [1800.0, 1900.0], "invalidation": 1590.0,
                      "trigger_price": "1700", "trigger_direction": " Above ", "trigger_basis": "close"},
        "sell_setup": {"trigger": "If price trades below 1550", "entry": 1550.0, "stop": 1650.0,
                       "targets": [1450.0, 1400.0], "invalidation": 1660.0,
                       "trigger_price": -5, "trigger_direction": "sideways", "trigger_basis": "TOUCH"},
    },
}


def _fake_storage(az, uploads):
    class _Container:
        def __init__(self, name):
            self.container_name = name

        def upload_blob(self, name, data, overwrite, content_settings):
            uploads.append({"container": self.container_name, "name": name, "data": bytes(data), "overwrite": overwrite})

        def list_blobs(self, name_starts_with=None):
            return [types.SimpleNamespace(name=u["name"]) for u in uploads
                    if u["container"] == self.container_name and u["name"].startswith(name_starts_with or "")]

    az._get_container_client = lambda name: _Container(name)
    az.datetime = _Frozen


def _expect_value_error(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("expected ValueError")


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
def test_t1_flags_default_off_and_settings_bounded():
    _clear_flags()
    from services.fixed_universe_batch import batch_enabled, batch_settings
    from services.report_provenance import archive_container_setting, report_archive_enabled

    assert report_archive_enabled() is False
    assert batch_enabled() is False
    assert archive_container_setting() == "vx-report-archive"
    assert not archive_container_setting().startswith("ai-reports")
    assert batch_settings() == {
        "max_symbols": 80, "start_deadline_et": time(21, 0), "stop_et": time(22, 15),
        "poll_seconds": 60, "pause_seconds": 5,
    }
    os.environ["FIXED_UNIVERSE_REPORT_BATCH_MAX_SYMBOLS"] = "999"
    os.environ["FIXED_UNIVERSE_REPORT_BATCH_STOP_ET"] = "25:00"
    settings = batch_settings()
    assert settings["max_symbols"] == 120 and settings["stop_et"] == time(22, 15)
    _clear_flags()


def test_t2_batch_script_flag_off_imports_nothing_heavy():
    _clear_flags()
    spec = importlib.util.spec_from_file_location(
        "en019_batch_script", _REPO_ROOT / "scripts" / "run_fixed_universe_report_batch.py"
    )
    module = importlib.util.module_from_spec(spec)
    before = set(sys.modules)
    spec.loader.exec_module(module)
    assert module.main([]) == 0
    forbidden = {"app", "models", "azure_storage", "dotenv", "ai_agents.principal_agent",
                 "core.market_sessions", "sqlalchemy"}
    newly = set(sys.modules) - before
    assert not (newly & forbidden), sorted(newly & forbidden)
    assert sys.modules["db"] is _DB_STUB


def test_t3_explicit_offset_timestamps():
    from services.report_provenance import (
        find_technical_timestamp, format_utc_offset, localize_naive_timestamp, utc_iso_z,
    )

    assert format_utc_offset(timedelta(hours=-4)) == "-04:00"
    assert format_utc_offset(timedelta(0)) == "+00:00"
    assert format_utc_offset(timedelta(hours=5, minutes=30)) == "+05:30"
    assert localize_naive_timestamp("2026-09-11 18:31:02", timedelta(hours=-4)) == "2026-09-11T18:31:02-04:00"
    assert localize_naive_timestamp("2026-04-03 14:00:00", timedelta(0)) == "2026-04-03T14:00:00+00:00"
    assert localize_naive_timestamp("2026-09-11T18:31:02-04:00", timedelta(0)) == "2026-09-11T18:31:02-04:00"
    assert localize_naive_timestamp("not a time", timedelta(0)) is None
    assert localize_naive_timestamp("2026-09-11 18:31:02", None) is None
    assert utc_iso_z(datetime(2026, 9, 11, 18, 31, 2, tzinfo=timezone(timedelta(hours=-4)))) == "2026-09-11T22:31:02Z"
    assert find_technical_timestamp({"SNDK": {"timestamp": "2026-09-11 18:31:02"}}, "sndk") == "2026-09-11 18:31:02"
    assert find_technical_timestamp({"SNDK": {}}, "SNDK") is None
    assert find_technical_timestamp(None, "SNDK") is None


def test_t4_lane_keys_and_provenance_block():
    from services.report_provenance import build_report_provenance, lane_blob_keys

    assert lane_blob_keys({"day_trading": {}, " Swing_Trading ": {}, "scalping": {}, 7: {}, "longterm_trading": {}}) == [
        "day_trading", "swing_trading", "longterm_trading"]
    assert lane_blob_keys({}) == [] and lane_blob_keys(None) == []
    sources = {"day_trading": "llm", "swing_trading": "llm", "longterm_trading": "fallback_template"}
    prov = build_report_provenance(
        trigger="internal_batch", job_id="job-1", strategy_scope="swing_trading",
        lane_keys_in_job=["day_trading", "swing_trading", "longterm_trading"], plan_sources=sources,
        technical_timestamp="2026-09-11 18:31:02", utc_offset=timedelta(hours=-4),
        analysis_completed_at_utc=datetime(2026, 9, 11, 22, 33, 10, tzinfo=timezone.utc),
    )
    assert prov == {
        "schema": "report_provenance_v1",
        "trigger": "internal_batch",
        "job_id": "job-1",
        "report_status": "done",
        "strategy_scope": "swing_trading",
        "blobs_in_job": 3,
        "lane_keys_in_job": ["day_trading", "swing_trading", "longterm_trading"],
        "plan_source": "llm",
        "plan_sources": sources,
        "technical_timestamp_raw": "2026-09-11 18:31:02",
        "technical_timestamp_iso": "2026-09-11T18:31:02-04:00",
        "process_utc_offset": "-04:00",
        "analysis_completed_at_utc": "2026-09-11T22:33:10Z",
    }
    single = build_report_provenance(
        trigger="subscriber", job_id=None, strategy_scope=None, lane_keys_in_job=[], plan_sources=None,
        technical_timestamp=None, utc_offset=timedelta(0),
        analysis_completed_at_utc=datetime(2026, 9, 11, 22, 33, 10, tzinfo=timezone.utc), report_status="error",
    )
    assert single["blobs_in_job"] == 1 and single["plan_source"] is None
    assert single["technical_timestamp_iso"] is None and single["report_status"] == "error"
    common = dict(job_id=None, strategy_scope=None, lane_keys_in_job=[], plan_sources=None, technical_timestamp=None,
                  utc_offset=timedelta(0), analysis_completed_at_utc=datetime(2026, 9, 11, tzinfo=timezone.utc))
    _expect_value_error(lambda: build_report_provenance(trigger="cron", **common))
    _expect_value_error(lambda: build_report_provenance(trigger="subscriber", extra={"user_email": "x"}, **common))


def test_t5_plan_sources_and_numeric_trigger_contract():
    from services.report_provenance import apply_numeric_trigger_contract, classify_plan_sources

    template = {"trigger": "Only act if price confirms beyond the entry level.", "entry": 101.5, "stop": 100.99,
                "targets": [102.01, 102.52], "invalidation": 100.99}
    fallback_lane = {"buy_setup": template, "sell_setup": dict(template, entry=0.0)}
    llm_day = json.loads(json.dumps(_LLM_SUMMARY["swing_trading"]))
    strategies = {"day_trading": llm_day, "swing_trading": fallback_lane, "longterm_trading": fallback_lane}
    assert classify_plan_sources(["day_trading"], strategies) == {
        "day_trading": "llm", "swing_trading": "fallback_template", "longterm_trading": "fallback_template"}
    assert classify_plan_sources([], {}) == {}
    out = apply_numeric_trigger_contract(strategies, ["day_trading"])
    buy, sell = out["day_trading"]["buy_setup"], out["day_trading"]["sell_setup"]
    assert (buy["trigger_price"], buy["trigger_direction"], buy["trigger_basis"], buy["trigger_fields_complete"]) == (
        1700.0, "above", "close", True)
    assert (sell["trigger_price"], sell["trigger_direction"], sell["trigger_basis"], sell["trigger_fields_complete"]) == (
        None, None, "touch", False)
    fb_buy, fb_sell = out["swing_trading"]["buy_setup"], out["swing_trading"]["sell_setup"]
    assert (fb_buy["trigger_price"], fb_buy["trigger_direction"], fb_buy["trigger_basis"]) == (101.5, "above", None)
    assert (fb_sell["trigger_price"], fb_sell["trigger_direction"], fb_sell["trigger_fields_complete"]) == (None, "below", False)
    assert "trigger_price" not in template
    assert "trigger_fields_complete" not in llm_day["buy_setup"]
    assert out["swing_trading"]["buy_setup"] is not out["longterm_trading"]["buy_setup"]


def test_t6_declared_universe_is_fixed_ordered_and_knowledge_time_safe():
    from services.fixed_universe_batch import LIQUID_LIST_V1, declare_universe

    assert LIQUID_LIST_V1 == _LIQUID
    d = declare_universe(trading_date=TD, declared_at_utc=DECLARED, sas_run=SAS_RUN, sas_candidates=SAS_ROWS)
    assert d["symbols"] == list(_LIQUID) + ["SNDK", "WDC", "AMD", "MU", "QCOM"]
    assert d["symbols_sha256"] == "ae6f22bab4a5d9d08a3718d321ba88c8c2ad7f0d1dbb8afff6058860204440d1"
    assert d["sas_component"] == "ok" and d["sas_run_id"] == 4242 and d["n_sas_candidates"] == 7
    assert d["dropped_by_cap"] == [] and d["max_symbols"] == 80
    assert d["declared_at_utc"] == "2026-09-11T22:30:00Z" and d["sas_run_finished_at_utc"] == "2026-09-11T21:12:36Z"
    by = {e["symbol"]: e for e in d["entries"]}
    assert by["NVDA"]["sources"] == ["liquid_v1", "sas_published"] and by["NVDA"]["sas_selected_rank"] == 2
    assert by["AAPL"]["sources"] == ["liquid_v1", "sas_candidate"] and by["AAPL"]["sas_qualified"] is False
    assert by["MSFT"]["sources"] == ["liquid_v1"] and by["MSFT"]["sas_overall_score"] is None
    assert by["WDC"]["sources"] == ["sas_published"] and by["QCOM"]["sas_overall_score"] is None
    assert declare_universe(trading_date=TD, declared_at_utc=DECLARED, sas_run=SAS_RUN, sas_candidates=SAS_ROWS) == d

    capped = declare_universe(trading_date=TD, declared_at_utc=DECLARED, sas_run=SAS_RUN, sas_candidates=SAS_ROWS,
                              max_symbols=23)
    assert capped["symbols"][-3:] == ["SNDK", "WDC", "AMD"] and capped["dropped_by_cap"] == ["MU", "QCOM"]
    assert capped["symbols_sha256"] == "2f7317b1a6a3dd06645b9e80ee0bf8c16830dedd7e659fa1f7d81829f5ab7917"

    late_run = dict(SAS_RUN, finished_at_utc=datetime(2026, 9, 11, 23, 0, tzinfo=timezone.utc))
    late = declare_universe(trading_date=TD, declared_at_utc=DECLARED, sas_run=late_run, sas_candidates=SAS_ROWS)
    assert late["sas_component"] == "unavailable"
    assert late["sas_unavailable_reason"] == "sas_run_finished_after_declaration"
    assert late["symbols"] == list(_LIQUID)
    assert late["symbols_sha256"] == "57675ac10a9ec3aff313eebb49a4909ec02f3647cc13f3030d730c3f6e2b88a1"
    failed = declare_universe(trading_date=TD, declared_at_utc=DECLARED, sas_run=dict(SAS_RUN, status="failed"),
                              sas_candidates=SAS_ROWS)
    assert failed["sas_unavailable_reason"] == "sas_run_status_failed"
    none = declare_universe(trading_date=TD, declared_at_utc=DECLARED, sas_run=None, sas_candidates=[])
    assert none["sas_unavailable_reason"] == "no_sas_run_for_trading_date"
    _expect_value_error(lambda: declare_universe(trading_date=TD, declared_at_utc=datetime(2026, 9, 11, 22, 30),
                                                 sas_run=SAS_RUN, sas_candidates=SAS_ROWS))


def test_t7_pipeline_gate_clock_and_names():
    from services.fixed_universe_batch import (
        batch_settings, fixed_universe_manifest_blob_name, fixed_universe_report_blob_name, is_past,
        pipeline_finished, pipeline_status, settings_for_manifest,
    )

    digest = {"run_date": "2026-09-11", "runs": {"nightly_pipeline": {"job_name": "Nightly Pipeline", "status": "success"}}}
    assert pipeline_status(digest) == "success" and pipeline_finished(digest) is True
    assert pipeline_finished({"runs": {"nightly_pipeline": {"status": "failed"}}}) is True
    assert pipeline_finished({"runs": {"blacklist_check": {"status": "success"}}}) is False
    assert pipeline_finished(None) is False
    et = timezone(timedelta(hours=-4))
    assert is_past(datetime(2026, 9, 11, 21, 0, tzinfo=et), time(21, 0)) is True
    assert is_past(datetime(2026, 9, 11, 20, 59, tzinfo=et), time(21, 0)) is False
    assert fixed_universe_manifest_blob_name(trading_date=TD, kind="declared", run_id="ab12cd34ef56") == \
        "fixed_universe/2026-09-11/_declared_ab12cd34ef56.json"
    _expect_value_error(lambda: fixed_universe_manifest_blob_name(trading_date=TD, kind="final", run_id="x"))
    assert fixed_universe_report_blob_name(
        trading_date=TD, symbol="brk/b", strategy_scope=None,
        stored_at_utc=datetime(2026, 9, 12, 0, 5, 9, tzinfo=timezone.utc), job_id="job:1",
    ) == "fixed_universe/2026-09-11/BRK-B_noscope_20260912T000509Z_job_1.json"
    _clear_flags()
    assert settings_for_manifest(batch_settings()) == {
        "max_symbols": 80, "start_deadline_et": "21:00", "stop_et": "22:15", "poll_seconds": 60, "pause_seconds": 5}


def test_t8_job_entries_and_completed_manifest_count_analyses_not_blobs():
    from services.fixed_universe_batch import jobs_entry_from_result, summarise_completed_run

    t0 = datetime(2026, 9, 11, 22, 31, 0, tzinfo=timezone.utc)
    t1 = t0 + timedelta(seconds=84)
    three_lane = {"ai_job_id": "job-a", "job_result": {
        "principal_plan": {"success": True, "data": {"usage": {"total_tokens": 9000}, "strategies": {
            "day_trading": {"buy_setup": {"trigger_fields_complete": True}, "sell_setup": {"trigger_fields_complete": False}},
            "swing_trading": {"buy_setup": {"trigger_fields_complete": True}, "sell_setup": {"trigger_fields_complete": True}},
            "longterm_trading": {"buy_setup": {"trigger_fields_complete": False}, "sell_setup": {"trigger_fields_complete": False}},
        }}},
        "report_provenance_summary": {"lane_keys_in_job": ["day_trading", "swing_trading", "longterm_trading"],
                                      "plan_sources": {"day_trading": "llm", "swing_trading": "llm",
                                                       "longterm_trading": "fallback_template"}}}}
    failed_plan = {"ai_job_id": "job-b", "job_result": {"principal_plan": {"success": False, "error": "boom"},
                                                        "report_provenance_summary": {"lane_keys_in_job": [], "plan_sources": None}}}
    baseline = {"ai_job_id": None, "job_result": None}
    a = jobs_entry_from_result(symbol="SNDK", outcome=three_lane, started_at_utc=t0, finished_at_utc=t1)
    assert (a["status"], a["numeric_trigger_setups"], a["numeric_trigger_complete"], a["principal_total_tokens"],
            a["duration_seconds"]) == ("done", 6, 3, 9000, 84.0)
    b = jobs_entry_from_result(symbol="WDC", outcome=failed_plan, started_at_utc=t0, finished_at_utc=t1)
    assert (b["status"], b["principal_status"], b["lanes_written"]) == ("done", "failed", [])
    c = jobs_entry_from_result(symbol="MU", outcome=baseline, started_at_utc=t0, finished_at_utc=t1)
    assert c["status"] == "done_baseline_only"
    jobs = [a, b, c, {"symbol": "AMD", "status": "error", "job_id": None, "error": "429"},
            {"symbol": "QCOM", "status": "not_started_stop_time", "job_id": None}]
    declaration = {"universe_id": "fixed_universe_v1", "run_id": "ab12cd34ef56", "trading_date": "2026-09-11",
                   "symbols": ["SNDK", "WDC", "MU", "AMD", "QCOM"], "symbols_sha256": "x"}
    s = summarise_completed_run(declaration=declaration, jobs=jobs, started_at_utc=t0, finished_at_utc=t1,
                                stop_reason="stop_time_reached")
    assert (s["n_declared"], s["n_analyses"], s["n_report_blobs_expected"]) == (5, 2, 5)
    assert s["status_counts"] == {"done": 2, "done_baseline_only": 1, "error": 1, "not_started_stop_time": 1}
    assert s["lanes_per_analysis"] == {"0": 2, "3": 1}
    assert s["plan_source_counts"] == {"fallback_template": 1, "llm": 2}
    assert (s["numeric_trigger_setups"], s["numeric_trigger_complete"], s["principal_tokens_total"]) == (6, 3, 9000)


def test_t9_dated_blob_unchanged_and_archive_copy_is_additive():
    import azure_storage as az

    original_client, original_dt = az._get_container_client, az.datetime
    try:
        _clear_flags()
        expected = json.dumps({**_PAYLOAD, "symbol": "SNDK", "user_id": "1", "stored_at": "2026-09-11T22:31:02Z",
                               "strategy_scope": "day_trading"}, separators=(",", ":")).encode("utf-8")
        history = "SNDK_1_day_trading_20260911T223102Z_job-en019.json"

        off = []
        _fake_storage(az, off)
        assert az.store_ai_report("SNDK", 1, dict(_PAYLOAD)) is True
        assert [(u["container"], u["name"], u["overwrite"]) for u in off] == [
            ("ai-reports-2026-09-11", history, False), ("ai-reports-2026-09-11", "SNDK_1_day_trading_latest.json", True)]
        assert off[0]["data"] == expected and off[1]["data"] == expected

        os.environ["AI_REPORT_ARCHIVE_ENABLED"] = "1"
        on = []
        _fake_storage(az, on)
        prov = {"schema": "report_provenance_v1", "trigger": "internal_batch", "job_id": "job-en019"}
        assert az.store_ai_report("SNDK", 1, dict(_PAYLOAD), archive_provenance=prov) is True
        assert [(u["container"], u["name"], u["overwrite"]) for u in on] == [
            ("ai-reports-2026-09-11", history, False),
            ("vx-report-archive", f"reports/2026-09-11/internal_batch/{history}", False),
            ("ai-reports-2026-09-11", "SNDK_1_day_trading_latest.json", True)]
        assert on[0]["data"] == expected and on[2]["data"] == expected
        archived = json.loads(on[1]["data"])
        assert archived["report_provenance"] == prov
        stripped = {k: v for k, v in archived.items() if k != "report_provenance"}
        assert json.dumps(stripped, separators=(",", ":")).encode("utf-8") == expected

        unstamped = []
        _fake_storage(az, unstamped)
        assert az.store_ai_report("SNDK", 1, dict(_PAYLOAD)) is True
        assert unstamped[1]["name"] == f"reports/2026-09-11/unstamped/{history}"
        assert json.loads(unstamped[1]["data"])["report_provenance"] == {
            "schema": "report_provenance_v1", "trigger": None, "unstamped": True}
    finally:
        az._get_container_client, az.datetime = original_client, original_dt
        _clear_flags()


def test_t10_fixed_universe_reports_go_only_to_the_archive():
    import azure_storage as az

    original_client, original_dt = az._get_container_client, az.datetime
    try:
        _clear_flags()
        uploads = []
        _fake_storage(az, uploads)
        wrong = {"schema": "report_provenance_v1", "trigger": "internal_batch", "trading_date": "2026-09-11"}
        assert az.store_fixed_universe_report("SNDK", 1, dict(_PAYLOAD), archive_provenance=wrong) is False
        assert az.store_fixed_universe_report("SNDK", 1, dict(_PAYLOAD), archive_provenance=None) is False
        assert uploads == []
        prov = {"schema": "report_provenance_v1", "trigger": "scheduled_fixed_universe", "trading_date": "2026-09-11",
                "universe_run_id": "run123"}
        assert az.store_fixed_universe_report("SNDK", 1, dict(_PAYLOAD), archive_provenance=prov) is True
        name = "fixed_universe/2026-09-11/SNDK_day_trading_20260911T223102Z_job-en019.json"
        assert [(u["container"], u["name"], u["overwrite"]) for u in uploads] == [("vx-report-archive", name, False)]
        body = json.loads(uploads[0]["data"])
        assert body["report_provenance"] == prov and body["stored_at"] == "2026-09-11T22:31:02Z" and body["user_id"] == "1"
        assert az.list_report_archive_blob_names("fixed_universe/2026-09-11/") == [name]
    finally:
        az._get_container_client, az.datetime = original_client, original_dt
        _clear_flags()


def test_t11_principal_default_path_unchanged_research_path_additive():
    import ai_agents.principal_agent as pa

    agent = object.__new__(pa.PrincipalAgent)
    agent.model, agent.reasoning_effort, agent.text_verbosity, agent.max_output_tokens = "gpt-5.6-terra", "low", "medium", 3200
    original_dt = pa.datetime
    pa.datetime = _Frozen
    try:
        agent._summarise_for_client = lambda *a, **k: (json.loads(json.dumps(_LLM_SUMMARY)), {"total_tokens": 10}, "raw")
        base_state = {"symbol": "SNDK", "strategy_scope": None, "include_raw_results": False, "raw_inputs": {},
                      "expert_outputs": {}}
        off = agent._summarise_node(dict(base_state))["principal_result"]
        assert "plan_sources" not in off
        assert "trigger_fields_complete" not in off["strategies"]["day_trading"]["buy_setup"]
        on = agent._summarise_node(dict(base_state, record_plan_sources=True, numeric_trigger_contract=True))["principal_result"]
        assert on["plan_sources"] == {"day_trading": "llm", "swing_trading": "llm", "longterm_trading": "fallback_template"}
        assert on["strategies"]["swing_trading"]["buy_setup"]["trigger_fields_complete"] is True
        assert on["strategies"]["longterm_trading"]["buy_setup"]["trigger_direction"] == "above"
        assert {k: v for k, v in on.items() if k not in ("plan_sources", "strategies")} == \
            {k: v for k, v in off.items() if k != "strategies"}

        assert "record_plan_sources" not in agent._initialise_state({"symbol": "SNDK"})
        assert agent._initialise_state({"symbol": "SNDK", "numeric_trigger_contract": True})["numeric_trigger_contract"] is True

        del agent._summarise_for_client
        captured = []

        def _capture(body):
            captured.append(body)
            raise RuntimeError("captured")

        agent._create_responses_call = _capture
        for contract in (False, True):
            try:
                agent._summarise_for_client("SNDK", {}, {}, strategy_scope=None, numeric_trigger_contract=contract)
            except RuntimeError:
                pass
        assert "trigger_price" not in json.dumps(captured[0])
        assert "trigger_price" in json.dumps(captured[1]) and "trigger_basis" in json.dumps(captured[1])
    finally:
        pa.datetime = original_dt


_CHECKS = [
    test_t2_batch_script_flag_off_imports_nothing_heavy,
    test_t1_flags_default_off_and_settings_bounded,
    test_t3_explicit_offset_timestamps,
    test_t4_lane_keys_and_provenance_block,
    test_t5_plan_sources_and_numeric_trigger_contract,
    test_t6_declared_universe_is_fixed_ordered_and_knowledge_time_safe,
    test_t7_pipeline_gate_clock_and_names,
    test_t8_job_entries_and_completed_manifest_count_analyses_not_blobs,
    test_t9_dated_blob_unchanged_and_archive_copy_is_additive,
    test_t10_fixed_universe_reports_go_only_to_the_archive,
    test_t11_principal_default_path_unchanged_research_path_additive,
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
    print(f"EN-019: {passed}/{len(_CHECKS)} checks passed")
```

The three sha256 values in T6 were computed by the desk from `json.dumps(symbols, separators=(",", ":"))` of the
lists written beside them; if T6 fails on a hash, the ordering rule was implemented differently from §3.2 — fix
the code.

### Acceptance (what the PR must report)

1. §4(a): exactly the 11 paths.
2. §4(b)/(d): the five inertness lines, base and HEAD, identical — pasted.
3. §4(c): `UNCHANGED`.
4. §4(e): the OK line.
5. §4(f): `EN-019: 11/11 checks passed`, and a statement that `pytest` was not run against a real database.
6. The platform SHA of the merge.

---

## 6. Rollback

```
FIXED_UNIVERSE_REPORT_BATCH_ENABLED=0   and   AI_REPORT_ARCHIVE_ENABLED=0   (App Service settings)
```

Either flag off stops its behaviour at the next call; nothing already written is deleted (append-only by design,
and the desk wants it kept). Code rollback, if ever needed: `git revert --no-edit <sha> && git push` — one commit,
no data migration.

---

## 7. Out of scope — do not touch

- **The legacy zone-less `timestamp`** (`day_trading_agent.py:609`), per-timeframe `price_timestamp`
  (`:726-728`) and the `/analyze` response `timestamp` (`app.py:3579`). Changing them changes subscriber payloads
  and displays (§0.2 choice 2).
- **History.** No backfill, re-stamp or copy of existing blobs into the archive. The 697 historical reports stay
  exploratory; the desk normalises their zone by date (PI-019).
- **The SAS report engine** (`services/super_agent_select_report_service.py`, `store_super_agent_select_report`)
  and every nightly pipeline step. Do not pass the new keyword arguments from any SAS path.
- **The legacy 5m report shape**, PI-018's decision-layer overrides, and the principal prompt for any caller other
  than the fixed-universe script.
- **The Omega agent, Report Center, Action Center, templates, static assets, routers.**
- **Any Azure management-plane change** (lifecycle rules, immutability policies, container ACLs). §8 asks Haci to
  *look*; nobody changes one in this brief.
- **A database table, migration or model change.** The batch writes no row.
- **Crypto, ETFs, a second universe, or editing `LIQUID_LIST_V1`.**
- Any subscriber-visible copy, field, ordering or number. There are none in this change.

---

## 8. Verification at `/desk-run verify EN-019 <sha>`

**Whose step is whose.** The coding agent's work ends at §3–§5 (repository only). Every step below is either
**Haci's** (deploy, portal, settings — writes to production configuration) or the **Data Steward's** (read-only
database role `sas_research_ro` on `$RESEARCH_DB_URL`; blob reads with `PROD_SAS_TOKEN`, read/list). Counts and
metadata only: **no price, touch, return or outcome is read in any step.**

### Haci

1. **Deploy** the merge. In Kudu, confirm the WebJobs dashboard lists `fixed_universe_report_batch` with schedule
   `0 30 18 * * 1-5` and that it executes the wwwroot copy (`docs/AZURE_WEBJOBS_AUTOMATION.md:59-66`, the stale
   wrapper warning).
2. **Look, do not change:** Storage account → Data management → Lifecycle management. Record in the register whether
   any rule matches container `vx-report-archive`, and whether any rule matches `ai-reports` (the latter answers the
   inventory's §9 question and `SAS_EXCURSION_BACKFILL.md:50-52`'s "aged out"). If a rule matches the archive
   container, stop and tell the desk before step 3.
3. **Set** `FIXED_UNIVERSE_REPORT_BATCH_ENABLED=1` and, recommended for PI-019, `AI_REPORT_ARCHIVE_ENABLED=1`.
   (App settings restart the app.) Leave the other settings at their defaults. Record the date each was set.
4. After **three** trading sessions, run `/desk-run verify EN-019 <sha>`. What moves on the product: nothing a
   subscriber sees; spend rises by ~230 LLM calls a night (§0.3).

### Data Steward — before-state

The before-state is structural, not a snapshot: no archive container exists at `c311e81`, and no dated report blob
carries `report_provenance` or `trigger` (`research/reports/STEWARD_F9_blob_inventory.md` §3–§4, measured
2026-09-14 over all 697 history blobs). No manifest pins a blob store, so there is no parquet to cite; the
inventory's counts are the reference.

### Data Steward — checks, for each of the first three sessions N after the batch flag was set

**Repo half:** at `<sha>`, re-run §4(a), (c), (e) and §4(f) (standalone, `DATABASE_URL` unset) and record the output.

**Database (read-only):**

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
  AND stored_at >= :flag_set_at
  AND (stored_at AT TIME ZONE 'America/New_York')::time >= TIME '18:30';
```

**Blobs (read/list):** container `vx-report-archive`, prefixes `fixed_universe/<N>/` and `reports/`; containers
`ai-reports-<N>` and `ai-reports-<N+1>` (the batch window crosses UTC midnight); `ai-reports-jobs` blob
`scheduler-digest-<N>.json`.

- **V1 — dated containers untouched.** No history blob written on or after the deploy date in any `ai-reports-*`
  container has a `report_provenance`, `plan_sources`, `trigger_price` or `report_provenance_summary` key; no blob
  name there starts with `fixed_universe/` or `reports/`. The count of `_1_` history blobs per day is within the
  pre-deploy range (inventory: 513 over 120 active days), not ~230 higher. S3 returns only rows explainable by
  ad-hoc internal-batch use in that window (each must match a dated `_1_` history blob) — normally 0.
- **V2 — one declaration, knowledge-time clean.** Exactly one `_declared_*.json` and one `_completed_*.json`, **or**
  exactly one `_skipped_*.json` and no declaration. `declared_at_utc` is later than 18:30 ET on N, later than S1's
  `finished_at` when `sas_component = "ok"`, and later than the digest's `runs.nightly_pipeline.updated_at_utc`.
  Recompute with the shipped pure function —
  `services.fixed_universe_batch.declare_universe(trading_date=N, declared_at_utc=<manifest value>, sas_run=<S1 row>, sas_candidates=<S2 rows>, max_symbols=<manifest settings.max_symbols>)`,
  imported read-only from `$CODEBASE_DIR` at `<sha>` — and its `symbols_sha256` equals the manifest's. (If S1's
  `finished_at` is later than `declared_at_utc`, SAS was re-run after the declaration: record it, not a FAIL.)
- **V3 — reports match the manifest, counted by analysis.** Report blobs under `fixed_universe/<N>/` (names not
  starting with `_`) = `n_report_blobs_expected`; distinct `job_id` in those names = `n_analyses`; every blob's
  symbol is in the declared list; no symbol has two `job_id`s; every blob's `report_provenance` has
  `trigger = "scheduled_fixed_universe"`, `universe_run_id = run_id`, `trading_date = N`. A shortfall in blobs
  with matching manifest counts means a write failed — record the count.
- **V4 — PI-019, the zone.** Every report's `technical_timestamp_iso` matches
  `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$`; converted to UTC it precedes `stored_at` by 0–15 minutes;
  report the counts of `process_utc_offset` values (expected all `-04:00` in EDT or all `-05:00` in EST).
- **V5 — timing.** Every report's `stored_at` is before 04:00 ET on the next calendar day (and so before the next
  session's pre-market).
- **V6 — plan provenance and numeric trigger fields (counts only).** `plan_source` present on 100% of lane blobs;
  all four `trigger_*` keys present on 100% of setups (values may be null). Report per night: `plan_source_counts`,
  `numeric_trigger_complete / numeric_trigger_setups`, `lanes_per_analysis`, `principal_tokens_total`,
  `status_counts`, `stop_reason`. These are descriptive; no threshold.
- **V7 — the nightly pipeline was not disturbed.** For each N, S1 shows `status = success` finished the same
  evening, and the digest shows `nightly_pipeline` = `success`, as on the five sessions before the flag was set.
- **V8 — only if `AI_REPORT_ARCHIVE_ENABLED` was set.** For every dated history blob with `stored_at` after the flag
  was set (sample all of one night if more than 200), an archive copy exists at
  `reports/<UTC date of stored_at, or the next UTC date>/<trigger>/<same name>`, and
  `json.dumps({k: v for k, v in archive.items() if k != "report_provenance"}, separators=(",", ":")).encode()`
  equals the dated blob's bytes exactly. Every archive copy whose `user_id` is not `"1"` has
  `trigger = "subscriber"`; none has `trigger = null`.

**PASS requires V1–V7 on all three sessions, and V8 if the archive flag was set.** Actions on failure: V1 or V7
fails → Haci sets both flags to 0 immediately (§6) and the desk files a PLATFORM_ISSUES row; V2–V6 or V8 fails →
record `FAILED` with the failing count, flags may stay on (nothing a subscriber sees is affected).

**On PASS** the Steward (i) writes the dated data note of §0.1 (first declared night, container, universe id,
SHA — not a repair-log row); (ii) records the PI-019 recommendation from this brief's header; (iii) notes for
H-086..H-094 that re-entry trigger (1) is met from that night and trigger (2a)'s freeze should pin
`vx-report-archive/fixed_universe/` (and `reports/` for the subscriber companion), not the dated containers.
