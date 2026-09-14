INTERNAL_TOOL — flag-off, visible to Haci only, no subscriber-facing copy or number; gate: Q002 (2026-10-12)

# EN-002 — speed-to-target (sessions to first touch of L1/L2/L3), built as a Haci-only internal card

**Type:** enhancement brief, **behaviour** kind, **gate not met** → INTERNAL_TOOL (ENHANCEMENTS.md
"Two kinds"; DP-48)
**Register row:** `research/ENHANCEMENTS.md` EN-002, Build = `HACI_DECIDED:build`
**Written:** 2026-09-13 by the Brief Writer, on Haci's `/desk-run prompt EN-002` (DP-48: asking is
the decision)
**Gate:** Q002 `speed_to_target`, state `DATASET_PINNED`, decision date **2026-10-12**. Not
HISTORICALLY_CONFIRMED, not `HUMAN_APPROVED`. Therefore **no subscriber surface changes in this
brief** and no number produced by this tool may be quoted, shown to a subscriber, or pasted into
marketing copy until Q002 reaches PROSPECTIVELY_CONFIRMED (CLAUDE.md rules 10 and 12).
**Platform repo:** `C:\Users\sahin\Projects\volatilx`
**Platform SHA all `path:line` citations are taken at:** `2d5776c373896d150f1865b681e9bc99fda058b1`
(committed 2026-09-13)
**Research repo SHA:** `f8c18cf`
**Feature flag:** `SAS_SPEED_TO_TARGET_INTERNAL`, **default OFF**, read from the environment at call
time (the repo's existing convention — `services/sas_conviction_card.py:68-69` and
`core/feature_flags.py:1-23`).
**DP-49:** this brief hands the coding agent **no database step**. Every check in §4 and §5 is
satisfiable from the repository alone. DB reads are in §8, addressed to the Data Steward on the
read-only role. Env-var flips are in §8, addressed to Haci.
**DP-50(b) ship-timing check:** performed, answer in §0.

You are the coding agent working in the platform repo. This brief is self-contained: do not ask
questions, do not redesign, do not widen the scope. Implement §3, run §4, add §5, update §6, and
report the SHA. **Do not connect to a database, do not run `pytest` against the production
`DATABASE_URL`, and do not start the app** — see the warning at the end of §4.

---

## 0. DP-50(b) — does building this touch anything a locked question reads?

**No.** Checked against every locked question on `research/BOARD.md` (Q002–Q023) on 2026-09-13.

- The change is **additive only**: five new files, plus two lines in `app.py` and one line in
  `docs/README.md`. It adds **no column**, runs **no migration**, and performs **no write** of any
  kind. Nothing in the scoring, selection, qualification or publication path is opened —
  `services/super_agent_select_scoring.py`, `services/super_agent_select_service.py`,
  `services/super_agent_select_public.py` and `scripts/run_sas_ladder_nightly.py` are untouched — so
  **which picks get published does not change**, and no historical row is rewritten (DP-50(a) does
  not fire; no `DATA_NOTES.md` repair-log row is due).
- The only persisted values the tool **reads** are `level_hit_steps_json` and
  `level_hit_dates_json` (`models.py:603`, `models.py:610`). Three locked PREREGs mention those
  columns and all three **ban them as inputs**: Q008 §"knowledge time" (`PREREG.md:458-460`), Q013
  (`PREREG.md:469-471`), Q022 (`PREREG.md:174`). Q002 itself computes first-touch from its own
  pinned price freeze (`Q002/PREREG.md` §2), never from these columns. So no locked PREREG's inputs
  move.
- **The one live constraint is rule 9 (no judgment in the inner loop), and it is in §3.4.** Q002's
  three primaries are all *control-differenced*. This tool ships with the control arm **stubbed**
  (`"control_status": "AWAITING_Q002"`), so it can never show Haci a Q002 primary before the
  decision date. Keeping it stubbed until 2026-10-12 is an acceptance criterion (§7, AC-9), not a
  preference.

---

## 1. What is missing, and the evidence

The performance surface tells a reader **whether** a committed target was reached and **how far
away** it was. It does not tell them **how fast**, and it never shows a comparator.

- `services/sas_conviction_card.py:406-427` emits per level `hit` (rate), `tgt` (median distance),
  `n`, `window` and `exit`. The one speed field, `avg_hit_day`
  (`services/sas_conviction_card.py:423`), is the **mean sessions-to-hit among in-window touchers
  only** (`services/sas_conviction_card.py:404`) — survivor-biased by construction, measured from
  the pick night rather than from a tradeable entry, and printed with no control beside it.
- There is **no distance-matched control anywhere in the platform**. The only matched-control code
  in the repo is an offline research script, `scripts/phase2_signals/track_a_stats.py:52-93`; the
  live surfaces have none. `services/super_agent_grounding.py:172` already *describes* a
  distance-matched comparison in prose that no live surface computes.
- The desk's exploratory evidence that speed is where the edge sits (in-sample, exploratory, **not a
  finding**): `research/reports/explore/EXPLORE_001.md` §E — "Speed vs matched control: L3 median 3
  sessions vs 5, L4 7 vs 11, L2 2 vs 2. Touch rates within 40 are similar at L3 (0.82 vs 0.81)."
  n = 280 picks / 35 nights. Registered as H-065 → **Q002**, decision date 2026-10-12.
- The raw material already exists and is persisted: `level_hit_steps_json` holds the **trading-day
  step** of each first touch, 1 = the first bar after the signal, stamped by
  `scripts/run_sas_ladder_nightly.py:307` over a uniform 60-trading-day scan
  (`scripts/run_sas_ladder_nightly.py:52-56`; `models.py:604-610`). Nothing reads it as a speed
  distribution.

Coverage of that raw material, from the pinned freeze (`research/data/manifest_v001.json`,
`v001_sas_candidates.parquet`, sha256 `af40ad8a…a2f2`, as_of 2026-09-10; predicate
`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28):

| month | published rows | with `level_hit_steps_json` | nights |
|---|---:|---:|---:|
| 2026-04 | 168 | 160 | 21 |
| 2026-05 | 160 | 152 | 20 |
| 2026-06 | 171 | 163 | 21 |
| 2026-07 | 177 | 168 | 22 |
| 2026-08 | 170 | 170 | 21 |
| 2026-09 (to 09-10) | 61 | 43 | 7 |
| **total** | **907** | **856** | **112** |

In the tool's window (`trading_date >= 2026-06-01`): **579 published rows over 71 nights**.
Of those, **578 are tier-eligible** under §3.1's existing score >= 80 gate; one published row
(TJX, 2026-06-11, score 79.5802) is below that gate. The output expectation is therefore
**578 tier-eligible picks over 71 nights**, with the one-row difference explicitly reconciled.
This is a specification correction dated 2026-09-14, supported by VERIFY_EN-002.md; it changes
neither the shipped tier gate nor its payload. The original failed verification is preserved.
These before-counts come from the freeze, not a live query (DP-50(c)).

---

## 2. Cause — why it is not there today

Not a defect; a surface that was never built. The ladder card computes what it can from one ORM
fetch (`services/sas_conviction_card.py:305-312`) and stops at hit rates. The two structural
reasons speed-with-a-control was never added:

1. **No control cohort at read time.** A distance-matched control needs the same-night *unpublished*
   candidates matched on `beta60` / `atr_pct` / `runup20` and graded against synthetic targets at
   the same ATR distance (Q002 §3 B1). Unpublished candidate rows carry no lane plan and therefore
   no ladder, and the platform holds no forward price panel to grade one — the ladder job fetches
   bars per symbol from the vendor (`scripts/run_sas_ladder_nightly.py:34`,
   `services/sas_excursion.py`). Building that cohort live is a research pipeline, not a card.
2. **No entry-basis correction.** Q002 measures from the **next session's open** and records a level
   already at or through that open as `passed_at_entry`, **not** a hit (Q002 §4). The nightly scan
   has no next-open price and grades an open-gap-through as a step-1 hit. In-sample that is 9% of
   L2s and 5% of L3s (EXPLORE_001 §E), so it is not a rounding difference.

Both are handled explicitly in §3 rather than papered over.

---

## 3. Change — the minimal internal tool

Ship a **read-only, derived-only, flag-off** internal card. **No shadow column, no migration, no
write, no nightly job.** Reasons, stated so they are not re-litigated: (a) every input the tool needs
is already persisted in `level_hit_steps_json`, so a shadow column would duplicate it; (b) a shadow
column would require a nightly write to production, which under DP-49 is not the coding agent's to
run and under DP-50(a) would put new historical values into the desk's shared instance between
freezes; (c) Q002 grades the hypothesis from its own pinned freeze and does not need a platform
sidecar.

### 3.1 New file — `services/sas_speed_to_target.py` (pure; **no** SQLAlchemy, **no** `db`, **no** `models` import)

The whole computation lives in pure functions over plain dicts, so §4 and §5 can exercise it with a
bare `python` interpreter and no environment.

Module constants:

```python
TOOL_VERSION = "v1"
GATE = {"question": "Q002", "decision_date": "2026-10-12",
        "required_state": "PROSPECTIVELY_CONFIRMED"}
SPEED_LEVELS = ("L1", "L2", "L3")
SPEED_CUTS = (1, 2, 3, 5, 10)          # sessions from entry; all reported
PRIMARY_CUT = {"L1": 2, "L2": 2, "L3": 5}   # Q002 §4 endpoints S1 / S2 / S3
WINDOW_START = date(2026, 6, 1)        # Q002 §6 test window; also clears DP-06 and the
                                       # 2026-04-01 manual overrides at routers/performance.py:934-946
MIN_COHORT_FLOOR = 20                  # same floor as services/sas_conviction_card.py:44
QUOTABILITY = "NON_QUOTABLE"           # CLAUDE.md rule 12: 2/5/10-session windows are research-basis
```

Functions, exactly these signatures:

1. `def tool_enabled() -> bool` — mirrors `services/sas_conviction_card.py:68-69`:
   `return (os.getenv("SAS_SPEED_TO_TARGET_INTERNAL", "") or "").strip().lower() in ("1","true","yes","on")`.
   Put it here rather than in `core/feature_flags.py` so that `core/feature_flags.py` stays
   byte-identical and the §4 diff stays as short as possible.

2. `def sessions_from_next_open(step: Optional[int]) -> Optional[int]` — the definitional bridge.
   `level_hit_steps_json` stores step 1 = the first bar after the signal, i.e. **the entry session**
   under Q002's next-open entry, so the mapping is the identity for `step >= 1` and `None`
   otherwise. Docstring must say exactly that, and must say that a level touched at step `s` counts
   as "within `s` sessions of the entry".

3. `def sessions_elapsed(trading_date: date, as_of: date) -> int` — trading days in
   `(trading_date, as_of]`, i.e. `trading_days_between(trading_date, as_of)` from
   `core/trading_days.py:126` (holiday-aware; `core/trading_days.py:45-56` carries the 2026 holiday
   set). Import `core.trading_days` only — it is pure stdlib (`core/trading_days.py:1-21`).

4. `def classify(step, sessions_matured, cut, *, void=False, has_target=True, passed_at_entry=None) -> str`
   returning exactly one of:
   - `"no_target"` — the lane plan has no price for this level;
   - `"void"` — wrong side of entry (reuse `services.sas_reference.ladder_level_is_void`, imported
     **inside the router**, not here — keep this module import-pure; the router passes the boolean);
   - `"passed_at_entry"` — `passed_at_entry is True`;
   - `"hit"` — `step is not None and 1 <= step <= cut`;
   - `"no_hit"` — `sessions_matured >= cut`;
   - `"pending"` — otherwise.
   Precedence is that order, top to bottom. `"no_target"`, `"void"`, `"passed_at_entry"` and
   `"pending"` are **excluded from both numerator and denominator** and counted separately —
   `passed_at_entry` because Q002 §4 says a target already passed at entry is not a hit, `pending`
   because an immature window is not a miss.

5. `def summarize_speed(rows, *, control_reference=None) -> dict` — the payload builder. `rows` is a
   list of plain dicts, one per published pick:

   ```python
   {"trading_date": date, "symbol": str, "overall_score": float,
    "tier": "select" | "apex",              # 80–89 / 90+, same cut as sas_conviction_card.py:314-321
    "levels": {"L1": {"step": int|None, "void": bool, "has_target": bool,
                      "passed_at_entry": bool|None}, ...},
    "sessions_matured": int}
   ```

   For each tier × level it emits:

   ```python
   {"level": "L1", "n": <graded denominator>,
    "hit_within": {"1": 0.42, "2": 0.61, "3": ..., "5": ..., "10": ...},   # None if n < 20
    "primary_cut": 2,
    "median_sessions_to_touch": <float|None>, "p75_sessions_to_touch": <float|None>,
    "survivor_biased": True,          # Q002 §4: days-to-touch among touchers is descriptive only
    "excluded": {"pending": int, "passed_at_entry": int, "void": int, "no_target": int},
    "passed_at_entry_known": <bool>,  # False whenever any row's passed_at_entry is None
    "building": n < MIN_COHORT_FLOOR,
    "control": None, "control_status": "AWAITING_Q002"}
   ```

   Top level of the returned dict: `{"enabled": True, "tool_version": TOOL_VERSION,
   "quotability": "NON_QUOTABLE", "internal_only": True, "gate": GATE,
   "entry_basis": <see 3.3>, "window_start": "2026-06-01", "as_of": ..., "nights": int,
   "picks": int, "min_cohort_floor": 20, "tiers": [...], "caveats": [...]}`.
   `nights` = distinct `trading_date` count (CLAUDE.md rule 6: the night is the unit; the tool does
   not claim inference, but it prints the night count next to every pick count so the reader can see
   which one they are looking at).

6. `def load_control_reference(path: Optional[str] = None) -> dict` — reads
   `data/sas_speed_control_reference.json`; on missing file, unreadable file, or
   `status != "PUBLISHED"`, returns `{"status": "AWAITING_Q002"}` and the control cells stay `None`.
   Never raises.

### 3.2 New file — `data/sas_speed_control_reference.json` (ships stubbed)

```json
{
  "status": "AWAITING_Q002",
  "gate": "Q002",
  "decision_date": "2026-10-12",
  "note": "Distance-matched control speed cannot be computed in the platform (no unpublished-candidate forward-price panel). This file is populated by the research desk only after Q002 reaches PROSPECTIVELY_CONFIRMED. Until then the internal card shows control: null.",
  "levels": {}
}
```

Same shape and location convention as the existing read-only report JSONs the admin surfaces load
(`routers/admin_outcome_coverage.py:23`, `data/outcome_coverage_report.json`).

### 3.3 New file — `routers/admin_sas_speed.py`

Admin-token security model copied verbatim from `routers/admin_outcome_coverage.py:26-29`
(`ADMIN_TOKEN` env var + matching `X-Admin-Token` header). Do **not** put this on
`routers/performance.py`, which is public and unauthenticated by design
(`routers/performance.py:1-4`).

```
router = APIRouter(prefix="/api/admin/sas-speed-to-target", tags=["admin"])

GET ""  ->  _require_admin(x_admin_token)          # 401 first, always
            if not tool_enabled(): return {"enabled": False, "gate": GATE}
            rows = <one read-only ORM SELECT, mirroring services/sas_conviction_card.py:305-312,
                    with the extra filter SuperAgentSelectCandidateDaily.trading_date >= WINDOW_START>
            build the plain-dict rows (payload -> lane-plan level prices via the same extraction as
            services/sas_conviction_card.py:246-258; void via services.sas_reference.ladder_level_is_void,
            imported inside the function like services/sas_conviction_card.py:301-302;
            steps via r.get_level_hit_steps(), models.py:732)
            return summarize_speed(rows, control_reference=load_control_reference())
```

`passed_at_entry` is passed as `None` for every row (the platform has no next-session open), so
`passed_at_entry_known` is `False` and the payload's `entry_basis` reads
`"signal_close_step_proxy (NOT Q002's next-open entry; passed_at_entry not applied)"`. Put that same
sentence in `caveats`. Do **not** invent a next-open price and do **not** add a vendor fetch.

Wrap the whole body in the same `try/except` + `logger.exception` shape the conviction endpoint uses
(`routers/performance.py:2441-2445`) so a failure returns `{"enabled": true, "error": "..."}` rather
than a 500.

### 3.4 The control arm stays stubbed until 2026-10-12

`control` is `None` and `control_status` is `"AWAITING_Q002"` in every cell shipped by this brief.
Populating it is a **separate** change, after Q002 decides, driven by editing
`data/sas_speed_control_reference.json` — no code change. This is the rule-9 guard from §0: with no
control arm, the card cannot be an interim look at any Q002 primary.

### 3.5 New file — `tests/test_sas_speed_to_target.py`

See §5. It must be runnable **both** as `python tests/test_sas_speed_to_target.py` and under pytest.

### 3.6 New file — `docs/SAS_SPEED_TO_TARGET_INTERNAL.md`

Reference doc: what the card shows, the flag and its default, the four exclusion states, the
entry-basis divergence from Q002 §4, the `NON_QUOTABLE` marking, and the sentence: *"No number on
this card may reach a subscriber surface, a chat answer, or marketing copy until research question
Q002 reaches PROSPECTIVELY_CONFIRMED (gate date 2026-10-12)."*

### 3.7 Edits to existing files — exactly three lines, in two files

- `app.py`: one import beside `routers/admin_outcome_coverage` at **`app.py:7041`**, and one
  `app.include_router(admin_sas_speed_router)` beside **`app.py:7056`**.
- `docs/README.md`: one table row inserted after **`docs/README.md:47`** in the "Super Agent Select
  (SAS)" section:

  `| [SAS_SPEED_TO_TARGET_INTERNAL.md](SAS_SPEED_TO_TARGET_INTERNAL.md) | Reference (internal tool) | Haci-only speed-to-target card; flag SAS_SPEED_TO_TARGET_INTERNAL, default off; gated on research Q002 (2026-10-12) |`

**No other existing file is edited.** In particular `templates/performance.html:1069` (the
subscriber fetch of the conviction card) and `services/sas_conviction_card.py` are not touched — the
merge of a speed row into the subscriber card is out of scope (§9).

### 3.8 Why no feature flag would be wrong here, and why this one is right

A flag *is* needed: this is behaviour, not a repair. Default OFF, env-read at call time so Azure app
settings flip it without a deploy (`core/feature_flags.py:1-5`). With the flag off the endpoint
returns `{"enabled": false}` and does not touch the database at all — the same shape as
`routers/performance.py:2430-2431`.

---

## 4. Before/after check — the inertness proof, from the repo alone (DP-49)

Let `BASE = 2d5776c373896d150f1865b681e9bc99fda058b1` and `HEAD` = your commit.

**(a) The touched-file list is exactly the allowed list.**

```bash
git -C . diff --name-only 2d5776c HEAD
```

Must print exactly, and nothing else:

```
app.py
data/sas_speed_control_reference.json
docs/README.md
docs/SAS_SPEED_TO_TARGET_INTERNAL.md
routers/admin_sas_speed.py
services/sas_speed_to_target.py
tests/test_sas_speed_to_target.py
```

**(b) The subscriber path is byte-identical.** This is the rule-11 inertness proof, and it is a
diff — not "run it twice and compare", which a flaky fetch could fake:

```bash
git -C . diff --stat 2d5776c HEAD -- \
  services/sas_conviction_card.py services/super_agent_select_public.py \
  services/super_agent_select_report_service.py services/super_agent_select_scoring.py \
  services/super_agent_select_service.py routers/performance.py routers/super_agent_select.py \
  templates/performance.html models.py db.py core/feature_flags.py \
  scripts/run_sas_ladder_nightly.py
```

Must print **nothing at all** (empty diff). Belt and braces, the same set by hash:

```bash
for f in services/sas_conviction_card.py routers/performance.py templates/performance.html \
         models.py scripts/run_sas_ladder_nightly.py core/feature_flags.py; do
  a=$(git show 2d5776c:$f | sha256sum | cut -d' ' -f1)
  b=$(sha256sum $f | cut -d' ' -f1)
  echo "$f before=$a after=$b $([ "$a" = "$b" ] && echo MATCH || echo DIFFER)"
done
```

All six must read `MATCH`. Paste the six lines into the PR description under the heading
`EN-002 inertness`.

**(c) `app.py` changed by exactly two added lines.**

```bash
git -C . diff --numstat 2d5776c HEAD -- app.py
```

Must read `2	0	app.py`.

**(d) The flag is off by default and the module is import-pure.**

```bash
python -c "
import os, sys
os.environ.pop('SAS_SPEED_TO_TARGET_INTERNAL', None)
for m in ('sqlalchemy','db','models'):
    sys.modules.pop(m, None)
import services.sas_speed_to_target as m
assert m.tool_enabled() is False, 'flag must default OFF'
assert 'db' not in sys.modules and 'models' not in sys.modules, 'module must not import db/models'
os.environ['SAS_SPEED_TO_TARGET_INTERNAL'] = 'true'
assert m.tool_enabled() is True
print('EN-002 flag default OFF: OK; import-pure: OK')
"
```

This must succeed **with `DATABASE_URL` unset**. If it fails because something in the import chain
wants `DATABASE_URL`, the module is not pure — fix the module, not the check.

> **Warning, and it is not optional.** `conftest.py:32-35` runs `create_tables()` in a
> session-scoped autouse fixture, and `db.py:14-22` builds the engine from `DATABASE_URL` at import.
> `python -m pytest` therefore issues **DDL against whatever database `DATABASE_URL` points at**,
> and in this repo that credential is read-write on **live production** (DP-50: the desk's
> read-only role and production are the same Postgres instance). Run the §5 test with
> `python tests/test_sas_speed_to_target.py`, which loads no conftest and opens no connection. Run
> the wider suite only if you have a scratch `DATABASE_URL`; if you do not, say so in the PR and
> skip it. Do not point it at production to "just check".

---

## 5. Test — `tests/test_sas_speed_to_target.py`

Pure, offline, fixture-driven. No DB, no network, no app. Written so
`python tests/test_sas_speed_to_target.py` runs every assertion and exits non-zero on failure, and
so pytest collects the same functions.

**Fixture (use these rows verbatim).** Synthetic by design — the desk does not seed a platform
fixture from Q002's sealed outcome data (CLAUDE.md rule 3). Six published picks, `as_of` fixed:

| # | trading_date | symbol | score | tier | L1 step | L2 step | L3 step | sessions_matured | notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-15 | AAA | 92.0 | apex | 1 | 2 | 4 | 40 | all three inside their primary cuts |
| 2 | 2026-06-15 | BBB | 84.0 | select | 3 | 6 | None | 40 | L1/L2 late, L3 matured miss |
| 3 | 2026-06-16 | CCC | 88.0 | select | 2 | None | None | 40 | L2/L3 matured misses |
| 4 | 2026-06-17 | DDD | 91.0 | apex | None | None | None | 40 | all matured misses |
| 5 | 2026-08-31 | EEE | 86.0 | select | None | None | None | 3 | **pending** at L3 (cut 5 > 3), matured miss at L1/L2 (cut 2 ≤ 3) |
| 6 | 2026-06-18 | FFF | 83.0 | select | 1 | 1 | 1 | 40 | L2 `void=True`, L3 `has_target=False` |

Required assertions:

1. **T1 — the step→session bridge.** `sessions_from_next_open(1) == 1`,
   `sessions_from_next_open(None) is None`, `sessions_from_next_open(0) is None`.
2. **T2 — `classify` precedence, one assertion per branch.** Notably
   `classify(step=1, sessions_matured=40, cut=2, passed_at_entry=True) == "passed_at_entry"` (a
   step-1 hit that was already through the entry is **not** a hit — Q002 §4), and
   `classify(step=None, sessions_matured=3, cut=5) == "pending"` while
   `classify(step=None, sessions_matured=3, cut=2) == "no_hit"`.
3. **T3 — denominators on the fixture.** apex/L1 `n == 2` with `hit_within["2"]` numerator 1 (row 1
   hits at step 1; row 4 is a matured miss). select/L3 `n == 2` (rows 2 and 3; row 5 is `pending`,
   row 6 is `no_target`), `excluded == {"pending": 1, "passed_at_entry": 0, "void": 0,
   "no_target": 1}`. select/L2 `excluded["void"] == 1` (row 6).
4. **T4 — the floor.** Every cell on this 6-row fixture has `building is True` and
   `hit_within` is `None`, because `n < 20` (`MIN_COHORT_FLOOR`). Then build a padded fixture of 24
   apex/L1 rows (20 hits at step 1, 4 matured misses) and assert `building is False` and
   `hit_within["2"] == 0.8333` to 4 dp — the floor releases at exactly 20, matching
   `services/sas_conviction_card.py:44` and `:143`.
5. **T5 — the gate is inert.** `summarize_speed(rows)` with no `control_reference` gives every cell
   `control is None` and `control_status == "AWAITING_Q002"`; the top level carries
   `quotability == "NON_QUOTABLE"`, `internal_only is True`, and
   `gate["decision_date"] == "2026-10-12"`.
6. **T6 — the shipped reference file is still stubbed.**
   `load_control_reference()["status"] == "AWAITING_Q002"`. This is the test that fails loudly if
   anyone populates the control before Q002 decides (AC-9).
7. **T7 — the entry-basis caveat is present.** `payload["passed_at_entry_known"]` is `False` for
   every cell built from rows whose `passed_at_entry` is `None`, and the string
   `"NOT Q002's next-open entry"` appears in `payload["entry_basis"]`.
8. **T8 — holiday-aware session count.** `sessions_elapsed(date(2026,7,1), date(2026,7,8)) == 4`
   (2026-07-03 is the observed Independence Day holiday, `core/trading_days.py:52`) and
   `sessions_elapsed(date(2026,8,3), date(2026,8,10)) == 5`. This is the test that would have caught
   a weekday-count shortcut of the kind `services/sas_conviction_card.py:232-243` has to live with.
9. **T9 — flag default.** `tool_enabled()` is `False` with the env var unset, absent, `""`, `"0"`,
   `"off"`; `True` for `"1"`, `"true"`, `"yes"`, `"on"` (case-insensitive).

Run it:

```bash
python tests/test_sas_speed_to_target.py
```

Expected last line: `EN-002: 9/9 checks passed`.

---

## 6. Docs

- New: `docs/SAS_SPEED_TO_TARGET_INTERNAL.md` (§3.6).
- One line added to `docs/README.md` after line 47 (§3.7).
- Nothing in `docs/SUPER_AGENT_EXPOSURE_POLICY.md` changes — this tool quotes nothing, and saying so
  is the doc's job, not an amendment to the policy.

---

## 7. Acceptance criteria (numbered, verifiable)

1. `git diff --name-only 2d5776c HEAD` prints exactly the seven paths in §4(a).
2. §4(b) prints an empty diff and six `MATCH` lines; the six lines are pasted in the PR under
   `EN-002 inertness`.
3. `git diff --numstat 2d5776c HEAD -- app.py` reads `2	0	app.py`.
4. §4(d) succeeds with `DATABASE_URL` unset: the flag defaults OFF and
   `services/sas_speed_to_target.py` imports neither `db` nor `models`.
5. `python tests/test_sas_speed_to_target.py` prints `EN-002: 9/9 checks passed`.
6. With the flag off, `GET /api/admin/sas-speed-to-target` returns `{"enabled": false, ...}` and the
   handler reaches **no** database call — verifiable by reading the handler: the `tool_enabled()`
   guard precedes the first `db` use, as at `routers/performance.py:2430-2431`. (Do not start the
   app to check this.)
7. Without a valid `X-Admin-Token` the endpoint returns 401 **regardless of the flag** — the
   `_require_admin` call is the first statement in the handler, as at
   `routers/admin_outcome_coverage.py:38`.
8. No migration, no `Column(...)` added to `models.py`, no `INSERT`/`UPDATE`/`DELETE` anywhere in
   the diff. `git diff 2d5776c HEAD | grep -iE "INSERT INTO|UPDATE |DELETE FROM|add_column|create_all"`
   returns nothing.
9. `data/sas_speed_control_reference.json` ships with `"status": "AWAITING_Q002"` and T6 enforces it.
   No control number appears anywhere in the diff.
10. **Subscriber payload byte-identical (rule 11 inertness).** No subscriber-facing template,
    router or service is in the diff (criteria 1 and 2 establish this directly);
    `/api/performance/sas/conviction-card` is served by unchanged code and therefore returns the
    same bytes as at `2d5776c` for identical database state.
11. The strings `NON_QUOTABLE`, `internal_only` and the gate date `2026-10-12` appear in the payload
    and in `docs/SAS_SPEED_TO_TARGET_INTERNAL.md`.

---

## 8. Verification — who runs what, after the PR lands

**These steps are not the coding agent's.** They are listed here so nobody is left deciding whether
they may touch production.

### 8a. Data Steward, on `$RESEARCH_DB_URL` (read-only role) — `/desk-run verify EN-002 <sha>`

**Repo half (no database):** at the platform SHA `<sha>`, re-run §4(a), §4(b) and §4(d) and record
the seven paths, the six `MATCH` lines and the flag-default result.

**Frozen half (the before-state is the freeze, DP-50(c)):** import the shipped pure function and
replay it over the pinned parquet — no live query is needed and none is authorised here.

```python
import sys, json, hashlib, pandas as pd
sys.path.insert(0, r"C:\Users\sahin\Projects\volatilx")   # read-only
from services.sas_speed_to_target import summarize_speed, load_control_reference

df = pd.read_parquet(r"research/data/v001_sas_candidates.parquet")   # sha256 af40ad8a…a2f2
pub = df[(df.qualified == True) & (df.selected_rank.notna()) &
         (pd.to_datetime(df.trading_date) >= "2026-06-01")]
# expected: 579 DP-28 published rows; 578 tier-eligible after the existing score >=80 gate (§1)
rows = [...]   # build the §3.1 row dicts from level_hit_steps_json / public_payload_json,
               # as_of = 2026-09-10, passed_at_entry=None
out = summarize_speed(rows, control_reference=load_control_reference())
print(out["picks"], out["nights"])
print(hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest())
```

Record in a **new dated verification report**: published input rows == 579, tier-eligible
`picks == 578`, `nights == 71`, the one excluded sub-80 row identified above, the payload sha256,
and every cell's `control_status == "AWAITING_Q002"`. Preserve `VERIFY_EN-002.md` as the failed
original-specification receipt. Any discrepancy from these reconciled counts is a FAIL, not a
rounding note. This correction does not assert a new replay passed or that the tool was deployed.

**One read-only SQL, and only this one** (the live coverage the endpoint will see today, against the
frozen baseline above):

```sql
SELECT date_trunc('month', trading_date)::date AS m,
       count(*) AS published_rows,
       count(level_hit_steps_json) AS with_steps,
       count(DISTINCT trading_date) AS nights
FROM super_agent_select_candidates_daily
WHERE qualified IS TRUE AND selected_rank IS NOT NULL
  AND trading_date >= DATE '2026-06-01'
GROUP BY 1 ORDER BY 1;
```

**Must match** the June/July/August rows of the §1 table (171/163/21, 177/168/22, 170/170/21) —
those months are fully sealed in `manifest_v001`. September and later will be larger; that is
maturation, not a defect. **Must not change:** nothing in this table may differ for `trading_date <=
2026-09-10` other than the normal maturation of September rows. Any change to a sealed June–August
count means something other than EN-002 wrote to the table and is a PI, filed immediately.

Set EN-002's Status to `VERIFIED` or `FAILED` on the strength of those two halves.

### 8b. Haci only — the flag

Flipping `SAS_SPEED_TO_TARGET_INTERNAL` (and setting `ADMIN_TOKEN` if it is not already set) in
Azure app settings is **his**, and it is the only production-side action this brief creates. It
writes **zero rows** and moves **nothing** on the product: with the flag on, one new
admin-token-protected JSON endpoint answers; no subscriber surface, no scoring input, no scheduled
job changes. Turning it on before 2026-10-12 is fine — the control arm is stubbed, so it cannot leak
a Q002 primary.

---

## 9. Out of scope — do not touch

- **Any subscriber surface.** `templates/performance.html`, `routers/performance.py`,
  `services/sas_conviction_card.py`, `services/super_agent_select_public.py`,
  `services/super_agent_select_report_service.py`. Merging a speed row into the conviction card is a
  **separate brief**, written only after Q002 reaches PROSPECTIVELY_CONFIRMED and Haci approves it.
- **Any scoring, selection, qualification or publication code.**
  `services/super_agent_select_scoring.py`, `services/super_agent_select_service.py`,
  `services/candidate_universe_builder.py`, `scripts/generate_sas_trading_guide.py`.
- **The ladder pipeline.** `scripts/run_sas_ladder_nightly.py`, `scripts/backfill_sas_ladder.py`,
  `services/sas_excursion.py`. Do not change how `level_hit_steps_json` is computed, do not widen
  the 60-trading-day scan (`scripts/run_sas_ladder_nightly.py:52-56`), do not backfill anything.
- **The database.** No migration, no new column, no write, no `create_tables()`, no ad-hoc query, no
  running the app against `DATABASE_URL`. See the warning in §4.
- **Computing a real distance-matched control.** It needs an unpublished-candidate forward-price
  panel the platform does not have (§2.1). Stub only.
- **Deriving `passed_at_entry`.** No next-open fetch, no vendor call. Report it as unknown (§3.3).
- **Chat/grounding surfaces.** `services/super_agent_grounding.py`, `routers/omega_chat.py`,
  `routers/concierge_chat.py` — the tool's numbers must not become answerable by any assistant.
- **`core/feature_flags.py`** — deliberately left byte-identical so the §4(b) hash set is clean.

---

## 10. Rollback

One flag:

```
SAS_SPEED_TO_TARGET_INTERNAL=false      # Azure app settings; endpoint returns {"enabled": false}
```

One command, if the code itself must go:

```bash
git revert --no-edit <HEAD>
```

Nothing to undo in the database — the change never wrote to it.
