# PI-017 — a forced UOA re-run deletes the whole trading date: scope the delete to what the run recomputes

**Type:** fix brief (platform issue, not a research finding)
**Register row:** `research/PLATFORM_ISSUES.md` PI-017, severity high, `HACI_DECIDED:fix`
**Written:** 2026-09-14 by the Brief Writer, on Haci's `/desk-run prompt PI-017` (DP-48: asking is the decision)
**Platform repo:** `C:\Users\sahin\Projects\volatilx`
**Platform SHA all `path:line` citations are taken at:** `d19c9a945418b09773baffac37f8d723c8a90a9a` (`d19c9a9`, 2026-09-13, merge of PR #27)
**Research repo SHA:** `e864827`
**Feature flag:** none — see §3 for why.
**Ship-timing check (DP-50(b)), done before writing:** this change rewrites **no historical row**. It
only changes what a *future* forced run is allowed to delete, and the nightly path never sets
`force` (`services/uoa_scheduler.py:103` passes `force=False`). Therefore: no locked question's data
moves, and **no `research/data/DATA_NOTES.md` repair-log row is required at ship** (that log takes
rows for repairs that rewrite history; a guard on future writes does not — `DATA_NOTES.md:32-33`).
Two locked questions are nevertheless exposed to the *defect*, and are the reason this ships now:

- **Q014** (`uoa_persistence`, DATASET_PINNED, decision **2027-04-05**) reads `uoa_symbol_daily`
  `score_day / score_swing / score_long / label_day / label_swing / label_long` from manifest_v001
  **and its successor freeze** (`research/questions/Q014_uoa_persistence/PREREG.md:46-51`). A forced
  re-run on any date in that window rewrites exactly those columns.
- **Q030** (`universe_discovery_recall`, PREREG_LOCKED, decision **2027-04-12**, prospective window)
  reconstructs the candidate universe from the night's UOA bulletin lists and names any change to
  those lists as a threat (`research/questions/Q030_universe_discovery_recall/PREREG.md:400`,
  `:654-655`, `:953`).

**Constraint, from the register and repeated here:** until this fix is deployed, no forced UOA re-run
may be executed on any trading date from **2026-06-01** onward. After it is deployed, a *partial*
forced run still rewrites `unusual_*` / `score_*` / `label_*` for the symbols it touches (§7, first
bullet), so any such run on a date ≥ 2026-06-01 gets a dated `DATA_NOTES.md` repair-log row and is
checked against Q014 and Q030 first. That is Haci's step, not the coding agent's.

You are the coding agent working in the platform repo. This brief is self-contained: do not ask
questions, do not redesign. Implement §3, run §4, add §5, report the SHA.

**Nothing in this brief runs against a database.** Under DP-49 you get no DB step at all: your
credential on that Postgres is the platform's read-write role and it points at live production.
Every check in §4 is satisfiable from the repository alone. §8 is the Data Steward's, on the
read-only role.

**Indentation:** `services/uoa_screener.py` and `scripts/run_uoa_*.py` are **tab-indented**. The
snippets below are shown with spaces; convert to tabs to match the surrounding file. `tests/` is
space-indented (4).

---

## 1. Symptom — what is wrong, and the evidence

`run_uoa_nightly(..., force=True)` deletes every row for the trading date from three tables and then
recomputes only the symbols it was given. The documented way to repair one symbol's UOA history —
`scripts/run_uoa_range.py`, which makes `--symbol` **required** (`scripts/run_uoa_range.py:34`),
passes `universe=[sym]` (`:79`) and advertises `--force` as "Recompute and overwrite rows for each
date" (`:43`) — therefore deletes ~498 other symbols' contract and symbol rows **and the night's
bulletin**, for every date in the range, and restores one symbol. The run still finishes
`status = "success"`.

It reaches past UOA. `uoa_bulletins` is the day/swing/long feed of the SAS candidate universe
(`services/candidate_universe_builder.py:38-48`, `_load_bulletin_lists`), and `uoa_symbol_daily`
carries the flow features and the `fwd_return_*` family PI-001 is about. One mistaken repair
silently shrinks a night's candidate pool and its flow layer.

**The signature in history, from the frozen freeze — not from a live query (DP-50(c)).**
`research/data/v001_uoa_symbol.parquet` (manifest_v001, as_of 2026-09-10, 83,747 rows, sha256
`1b959ef809fe925d4f1794e1ae347d385879823fa133cb1f051dd983fae34ac4`) covers 169 trading dates,
2026-01-07..2026-09-10. Exactly one of them has fewer than 200 rows:

| trading_date | rows | distinct symbols |
|---|---|---|
| 2026-01-07 | 499 | 499 |
| 2026-01-08 | 498 | 498 |
| **2026-01-09** | **23** | **23** |
| 2026-01-12 | 499 | 499 |
| 2026-01-13 | 499 | 499 |

Its `uoa_runs` row (id 5, `nightly`) carries `config_json = {"force": true}` and
`symbols_considered = 23`; it started 2026-01-12 19:09:46 UTC and finished 22 seconds later with
`status = "success"`. Neighbouring nightlies consider 503 symbols and take about six minutes.
Whether 2026-01-09 held ~499 rows before that run cannot be established from stored rows, so this is
a signature, not a proof — but it is the exact signature the code produces. 2026-01-09 is before
every registered study window (frozen candidate history starts 2026-04-01), so **no locked question
is affected today**. The hazard is the next single-symbol repair.

### Reproducing query — **Data Steward only**, read-only role on `$RESEARCH_DB_URL`

Not for the coding agent (DP-49). Counts only; no row bodies.

```sql
-- Any date whose forced run considered far fewer symbols than its neighbours.
SELECT s.trading_date,
       count(DISTINCT s.symbol)                     AS n_symbols,
       r.status,
       (r.config_json::jsonb)->>'force'             AS forced,
       (r.stats_json::jsonb)->>'symbols_considered' AS symbols_considered,
       r.started_at, r.finished_at
FROM uoa_symbol_daily s
LEFT JOIN uoa_runs r
       ON r.trading_date = s.trading_date AND r.run_type = 'nightly'
GROUP BY s.trading_date, r.status, r.config_json, r.stats_json, r.started_at, r.finished_at
HAVING count(DISTINCT s.symbol) < 200
ORDER BY s.trading_date;
-- Expected today: exactly one row, 2026-01-09, 23 symbols, forced = true, status = success.
```

---

## 2. Cause

**`services/uoa_screener.py:1282-1287`** — the forced-delete block filters on `trading_date` alone:

```python
    if force:
        # Clear existing rows for that date to avoid duplication.
        db.query(UoaContractDaily).filter(UoaContractDaily.trading_date == trade_date).delete(synchronize_session=False)
        db.query(UoaSymbolDaily).filter(UoaSymbolDaily.trading_date == trade_date).delete(synchronize_session=False)
        db.query(UoaBulletin).filter(UoaBulletin.trading_date == trade_date).delete(synchronize_session=False)
        db.commit()
```

**`services/uoa_screener.py:1289`** — only *then* is the universe resolved,
`universe_syms = _resolve_universe(db, cfg, universe)`, and `_resolve_universe`
(`services/uoa_screener.py:964-987`) returns the caller's explicit list when one is given
(`:965-967`). The recompute loop at `:1314` walks that list only. So the delete is unconditionally
date-wide while the rebuild is universe-wide: whenever the two differ, the difference is destroyed.
The ordering is the whole bug — the code deletes before it knows what it is going to write.

Callers that can reach the block with a narrow universe, all at this SHA:

| caller | universe passed | force |
|---|---|---|
| `scripts/run_uoa_range.py:76-82` | `[sym]`, `--symbol` **required** at `:34` | `--force` at `:43` |
| `scripts/run_uoa_nightly.py:49` | `--symbols` CSV or `None` (`:44`) | `--force` at `:38` |
| `scripts/run_uoa_sample_100.py:74-80` | first 100 S&P symbols (`:69`) | `--force` at `:61` |
| `scripts/run_uoa_oi_gex_for_day.py:161` | `--symbols` CSV or `None` (`:150`) | `--force` / `--force-uoa` at `:121-136` |
| `services/uoa_scheduler.py:103` | `None` (full universe) | **`force=False`** — the nightly never enters the block |

No HTTP route reaches `run_uoa_nightly` with `force=True`; the only router reference to these runs is
the read-only diagnostic at `routers/uoa_screener.py:840-900`.

Two consequences of the same ordering that the fix also has to answer:

1. **The bulletin.** `UoaBulletin` has `UNIQUE (trading_date)` (`models.py:1189`), and the rebuild at
   `services/uoa_screener.py:1864-1875` always `db.add()`s a new one. Today that is safe only because
   the whole-date delete removed the old row first. Whatever the fix does about the bulletin must
   keep that constraint satisfiable.
2. **The run record.** `services/uoa_screener.py:1877` sets `status = "success"` for a re-run that
   rebuilt 23 of 499 symbols, and `:1279` records `{"model_version", "force"}` without recording the
   universe. The audit trail cannot tell a full re-run from a one-symbol repair — which is why the
   desk needed three joined queries to identify 2026-01-09.

---

## 3. Change — the minimal fix

Resolve the universe **before** the delete; delete only what is about to be rewritten; never let a
partial run touch the night's bulletin; and say in `uoa_runs` that the run was partial.

### Why no feature flag

This restores intended behaviour. `--force` is documented as "recompute and overwrite rows"
(`scripts/run_uoa_range.py:43`) for a run whose declared unit is one symbol
(`scripts/run_uoa_range.py:34`, `:79`); deleting 498 other symbols is not a behaviour anyone chose,
and no caller wants it. CLAUDE.md rule 11 gates *new behaviour* shipping dark; a flag here would only
give the destructive path a switch to keep living behind, and the flag-off branch would be the branch
that loses data. The old whole-date behaviour stays reachable, but only by asking for it in words:
`force_scope="date"`.

The one deliberate change on the nightly (`force=False`) path is that `uoa_runs.config_json` gains
descriptive keys (§3.5). That column is internal audit state: read by the passthrough diagnostic at
`routers/uoa_screener.py:869-879` and by the desk, by no scoring input and by no subscriber surface.
`status` for a full run stays exactly `"success"`.

### 3.1 New module-level helpers — `services/uoa_screener.py`

Add immediately **above** `def _resolve_universe(` at `services/uoa_screener.py:964`:

```python
# --- Forced re-run delete scope (PI-017) -------------------------------------
# A forced re-run used to delete rows filtered on trading_date alone and then rebuild
# only the universe it was handed, so `run_uoa_range.py --symbol INTC --force` wiped
# every other symbol's contract and symbol rows and the night's bulletin for each date.
# A forced re-run may now delete only what it is about to recompute.
FORCE_SCOPE_AUTO = "auto"          # explicit universe -> that universe; no universe -> whole date
FORCE_SCOPE_UNIVERSE = "universe"  # always only the resolved universe
FORCE_SCOPE_DATE = "date"          # always the whole trading date (the pre-PI-017 behaviour)
_FORCE_SCOPES = (FORCE_SCOPE_AUTO, FORCE_SCOPE_UNIVERSE, FORCE_SCOPE_DATE)


def resolve_force_delete_scope(
    *,
    explicit_universe: Optional[Sequence[str]],
    resolved_universe: Sequence[str],
    force_scope: str = FORCE_SCOPE_AUTO,
) -> Optional[List[str]]:
    """Which symbols a forced re-run is allowed to delete.

    Returns None for "the whole trading date" (full-universe re-run, historical behaviour),
    or the explicit list of symbols the run is about to recompute. Pure: no DB, no I/O.
    """
    scope = (force_scope or FORCE_SCOPE_AUTO).strip().lower()
    if scope not in _FORCE_SCOPES:
        raise ValueError(f"unknown force_scope {force_scope!r}; expected one of {_FORCE_SCOPES}")
    if scope == FORCE_SCOPE_DATE:
        return None
    if scope == FORCE_SCOPE_UNIVERSE or explicit_universe:
        return [s.strip().upper() for s in resolved_universe if s and s.strip()]
    return None


def delete_rows_for_forced_rerun(
    db: Session,
    *,
    trade_date: date,
    symbols: Optional[Sequence[str]],
) -> Dict[str, int]:
    """Delete exactly what a forced re-run is about to rewrite. Returns the row counts.

    symbols is None   -> the whole trading date, bulletin included (full-universe re-run).
    symbols is a list -> only those symbols' contract and symbol rows. The bulletin is a
    cross-sectional artefact of the WHOLE date -- a partial re-run cannot reproduce it and
    must not delete it. It also feeds the SAS candidate universe
    (services/candidate_universe_builder.py:38-48).
    """
    if symbols is None:
        n_contracts = (
            db.query(UoaContractDaily)
            .filter(UoaContractDaily.trading_date == trade_date)
            .delete(synchronize_session=False)
        )
        n_symbols = (
            db.query(UoaSymbolDaily)
            .filter(UoaSymbolDaily.trading_date == trade_date)
            .delete(synchronize_session=False)
        )
        n_bulletins = (
            db.query(UoaBulletin)
            .filter(UoaBulletin.trading_date == trade_date)
            .delete(synchronize_session=False)
        )
    else:
        syms = [s.strip().upper() for s in symbols if s and s.strip()]
        if not syms:
            return {"contract_rows": 0, "symbol_rows": 0, "bulletins": 0}
        n_contracts = (
            db.query(UoaContractDaily)
            .filter(
                UoaContractDaily.trading_date == trade_date,
                UoaContractDaily.underlying_symbol.in_(syms),
            )
            .delete(synchronize_session=False)
        )
        n_symbols = (
            db.query(UoaSymbolDaily)
            .filter(
                UoaSymbolDaily.trading_date == trade_date,
                UoaSymbolDaily.symbol.in_(syms),
            )
            .delete(synchronize_session=False)
        )
        n_bulletins = 0
    db.commit()
    return {
        "contract_rows": int(n_contracts or 0),
        "symbol_rows": int(n_symbols or 0),
        "bulletins": int(n_bulletins or 0),
    }
```

Note the column name: contract rows are keyed by `UoaContractDaily.underlying_symbol`
(`models.py:834`), not `symbol`.

Add both public names to `__all__` beside `"run_uoa_nightly"` at `services/uoa_screener.py:2337`.

### 3.2 Signature — `services/uoa_screener.py:1210-1217`

One keyword-only parameter, defaulted to the safe-and-unchanged `auto`:

```python
def run_uoa_nightly(
    db: Session,
    *,
    trading_date: Optional[date] = None,
    universe: Optional[Sequence[str]] = None,
    config: Optional[UoaConfig] = None,
    force: bool = False,
    force_scope: str = FORCE_SCOPE_AUTO,
) -> Dict[str, Any]:
```

### 3.3 Resolve the universe before anything is deleted

Insert immediately **after** the idempotency early-return block that ends at
`services/uoa_screener.py:1248` and **before** the `run = (` lookup at `:1249`:

```python
    # PI-017: resolve the universe BEFORE anything is deleted. A forced re-run may only
    # delete what it is about to recompute.
    universe_syms = _resolve_universe(db, cfg, universe)
    force_delete_symbols = resolve_force_delete_scope(
        explicit_universe=universe,
        resolved_universe=universe_syms,
        force_scope=force_scope,
    )
    partial_force = bool(force and force_delete_symbols is not None)
    preserve_bulletin = bool(partial_force and existing_bulletin is not None)
    run_config = {
        "model_version": cfg.model_version,
        "force": bool(force),
        "force_scope": FORCE_SCOPE_DATE if force_delete_symbols is None else FORCE_SCOPE_UNIVERSE,
        "universe_explicit": bool(universe),
        "universe_size": len(universe_syms),
        "universe_symbols": list(universe_syms[:50]) if universe else None,
    }
```

`existing_bulletin` is already in scope from `:1231-1236`. Then **delete the now-duplicate line**
`services/uoa_screener.py:1289` (`universe_syms = _resolve_universe(db, cfg, universe)`).

Moving the call is behaviour-preserving: `_resolve_universe` reads env, the S&P file and (last
resort) `user_favorite_symbols` (`services/uoa_screener.py:969-987`); it writes nothing and depends
on nothing the delete block touches. It now runs after the early return at `:1237-1248`, so the
"bulletin already exists, not forced" path still does no extra work of consequence.

### 3.4 The scoped delete — replace `services/uoa_screener.py:1282-1287`

```python
    deleted = {"contract_rows": 0, "symbol_rows": 0, "bulletins": 0}
    if force:
        deleted = delete_rows_for_forced_rerun(
            db, trade_date=trade_date, symbols=force_delete_symbols
        )
        if partial_force:
            logger.warning(
                "UOA forced PARTIAL re-run trading_date=%s symbols=%d deleted_symbol_rows=%d "
                "deleted_contract_rows=%d -- other symbols and the night's bulletin are left "
                "untouched; the recomputed rows carry cross-sectional percentiles computed over "
                "this subset only and are not comparable with the rest of the date",
                trade_date.isoformat(),
                len(force_delete_symbols or []),
                deleted["symbol_rows"],
                deleted["contract_rows"],
            )
```

### 3.5 The run record

- `services/uoa_screener.py:1260` (new-run branch): `run.set_config(run_config)`.
- `services/uoa_screener.py:1279` (existing-run branch): `run.set_config(run_config)`.
- After the `stats = {...}` literal closes at `services/uoa_screener.py:1312`, add:

```python
    stats["force_scope"] = FORCE_SCOPE_DATE if force_delete_symbols is None else FORCE_SCOPE_UNIVERSE
    stats["force_partial"] = partial_force
    stats["force_deleted"] = deleted
```

- `services/uoa_screener.py:1877`: `run.status = "success_partial" if partial_force else "success"`.

`"success"` is not the right status for a run that rebuilt 23 of 499 symbols; `"success_partial"`
says so without inventing a failure. The only equality test against this column anywhere in the repo
is `services/uoa_screener.py:1254`, inside a `not force` branch whose body is `pass` — inert; the
sibling at `:2018` is the `oi_confirm` run type. `routers/uoa_screener.py:875` (inside `_fmt_run`, `:869-880`) passes the string
through to a diagnostic JSON payload and compares nothing. Do not add any other status value.

### 3.6 The bulletin on a partial run

A partial re-run must not rewrite the night's bulletin: it cannot reproduce a cross-sectional
artefact of the whole date, and the bulletin feeds the SAS candidate universe. Since §3.4 no longer
deletes it, the unconditional `db.add(bulletin)` at `services/uoa_screener.py:1875` would now violate
`UNIQUE (trading_date)` (`models.py:1189`) — so the build has to be skipped, not just the delete.

Replace `services/uoa_screener.py:1842-1875` (from `lists = {"day": top_day, ...}` through
`db.add(bulletin)`) so the whole build, `md_lines` included, sits in an `else`, and one
`bulletin_payload` is produced either way. Leave `top_day` / `top_swing` / `top_long` at
`:1838-1840` where they are — `_top_list` (`:1773-1837`) already queries the **whole** trading date,
so when a bulletin does have to be built after a partial run it is built from the full date's
surviving rows, which is the behaviour the register asked for:

```python
    if preserve_bulletin:
        bulletin_payload = {
            "model_version": existing_bulletin.model_version,
            "lists": existing_bulletin.get_lists(),
            "markdown": existing_bulletin.markdown,
            "html": existing_bulletin.html,
        }
        stats["bulletin_action"] = "preserved"
    else:
        lists = {"day": top_day, "swing": top_swing, "long": top_long}
        # ... md_lines + UoaBulletin(...) + db.add(bulletin) exactly as today ...
        bulletin_payload = {
            "model_version": bulletin.model_version,
            "lists": lists,
            "markdown": bulletin.markdown,
            "html": bulletin.html,
        }
        stats["bulletin_action"] = "rebuilt_from_full_date"
```

Finally, the return at `services/uoa_screener.py:1912-1922` uses the payload instead of the local
`bulletin` / `lists`:

```python
    return {
        "trading_date": trade_date.isoformat(),
        "status": "success_partial" if partial_force else "success",
        "stats": stats,
        "bulletin": bulletin_payload,
    }
```

Keys, order and values of that dict are otherwise unchanged; on every non-partial run
`bulletin_payload` is built from exactly the four expressions inlined there today.

### 3.7 Callers

- **`scripts/run_uoa_range.py:76-82`** — pass `force_scope="universe"` explicitly. This script exists
  only to re-run one symbol (`:34`, `:79`), so it must never be able to wipe a date even if the
  meaning of `auto` is ever loosened:

```python
            res = run_uoa_nightly(
                db,
                trading_date=d,
                universe=[sym],
                config=cfg,
                force=bool(args.force),
                force_scope="universe",
            )
```

  and change the `--force` help at `scripts/run_uoa_range.py:43` to:
  `"Recompute and overwrite rows for THIS SYMBOL on each date. Other symbols' rows and the night's bulletin are never deleted (PI-017)."`

- **`scripts/run_uoa_nightly.py`** — the general-purpose runner keeps `auto` and gains the escape
  hatch. Add after the `--force` argument at `:38`:

```python
    parser.add_argument(
        "--force-scope",
        choices=["auto", "universe", "date"],
        default="auto",
        help=(
            "What --force may delete. auto (default): only the symbols given by --symbols, "
            "or the whole date when no --symbols is given. universe: only the resolved "
            "symbols. date: the whole trading date including the bulletin (destructive)."
        ),
    )
```

  and pass it through at `:49`: `force_scope=str(args.force_scope)`.

- **`scripts/run_uoa_sample_100.py:74-80`** and **`scripts/run_uoa_oi_gex_for_day.py:161`** — leave
  the call sites alone. Both pass an explicit universe, so `auto` scopes them correctly; that is the
  fix working. Do not add flags to them.

### 3.8 Docs — `docs/UOA_SCREENER_MVP.md`

Add a subsection at the end of `### 1.3 Universe build (MVP)` — its last bullet is `docs/UOA_SCREENER_MVP.md:66`; insert before the `---` at `:68`:

```markdown
### 1.4 Re-running a date (`--force` scope)

`--force` deletes before it recomputes. What it may delete is set by `force_scope`
(`services/uoa_screener.py`, `resolve_force_delete_scope`): **auto** (default) — with an explicit
universe, only those symbols' `uoa_contract_daily` / `uoa_symbol_daily` rows; with no universe, the
whole trading date including `uoa_bulletins`. **universe** — always only the resolved symbols
(`scripts/run_uoa_range.py` hardcodes this). **date** — the whole trading date, the pre-PI-017
behaviour, now only on request. A partial forced run never deletes or rewrites the night's bulletin:
the bulletin is cross-sectional over the whole date and feeds the SAS candidate universe. Its
`uoa_runs` row records `status = 'success_partial'`, plus `force_scope`, `universe_size` and
`force_deleted` in config/stats.
```

And one line under `### 7.1 uoa_runs`, after the DDL block that ends at `docs/UOA_SCREENER_MVP.md:353` and before `### 7.2` at `:356`:

```markdown
`status` is `running` | `success` | `success_partial` (forced re-run over a subset universe) | `failed`.
```

That is the whole change: one service file, two scripts, one doc, one new test file. Do not touch
scoring, selection, ranking, targets, or any published payload.

---

## 4. Before / after check — repository only, no database

Run all four in the platform repo and paste the outputs into the PR. None of them opens a connection:
`services/uoa_screener.py:19-30` imports `models` only, and `models.py:76` declares its own `Base` —
the module never imports `db.py`, so importing it constructs no engine. (The import does pull
`indicator_fetcher` → `symbol_map`, whose module-level `refresh_symbol_catalog` at `symbol_map.py:243`
tries the Alpaca asset catalog and falls back to a bundled map offline. Slow, not a DB call.)

**(a) The delete scope — this is what changes.**

```
python -c "from services.uoa_screener import resolve_force_delete_scope as r; print(r(explicit_universe=None, resolved_universe=['AAPL','MSFT'], force_scope='auto')); print(r(explicit_universe=['intc'], resolved_universe=['INTC'], force_scope='auto')); print(r(explicit_universe=['INTC'], resolved_universe=['INTC'], force_scope='date')); print(r(explicit_universe=None, resolved_universe=['AAPL','MSFT'], force_scope='universe'))"
```

- Before: `ImportError: cannot import name 'resolve_force_delete_scope'`.
- After, exactly: `None` / `['INTC']` / `None` / `['AAPL', 'MSFT']`.

**(b) The nightly path is untouched — proved by diff, not by running anything.**

```
git show --stat HEAD
git diff d19c9a9..HEAD -- services/uoa_scheduler.py scripts/run_nightly_pipeline.py services/super_agent_select_scoring.py services/candidate_universe_builder.py routers/uoa_screener.py
```

`git show --stat` must list exactly five paths: `services/uoa_screener.py`,
`scripts/run_uoa_range.py`, `scripts/run_uoa_nightly.py`, `docs/UOA_SCREENER_MVP.md`,
`tests/test_uoa_force_scope.py`. The `git diff` must print **nothing**. The scheduler is the nightly
caller and it passes `force=False` (`services/uoa_scheduler.py:103`), so an empty diff there plus
check (a)'s first line — `auto` with no explicit universe → `None`, the whole-date branch — is the
complete argument that production's nightly behaviour is unchanged. Do not try to demonstrate this by
running the screener.

**(c) The test suite:**

```
python -m pytest tests/test_uoa_force_scope.py -q
python -m pytest tests/ -q
```

Before: the first file does not exist. After: it passes, and the full suite's pass/fail set is
unchanged from the base commit (run it on the base commit first and diff the summary lines).

**(d) The diff reads as described:**

```
git diff d19c9a9..HEAD -- services/uoa_screener.py
git grep -n "UoaBulletin.trading_date == trade_date).delete" -- services/
```

After: the `git grep` returns exactly one hit, inside `delete_rows_for_forced_rerun`. No
`.filter(UoaSymbolDaily.trading_date == trade_date).delete(` or
`.filter(UoaContractDaily.trading_date == trade_date).delete(` survives outside that function.

---

## 5. Test — the test that would have caught it

New file `tests/test_uoa_force_scope.py`. Two halves: pure-function assertions on the scope rule, and
an in-memory SQLite contract test on the delete itself — same pattern and fixture shape as
`tests/test_market_regime_repository.py:35-46` (`create_engine("sqlite:///:memory:")`, `StaticPool`,
`Base.metadata.create_all(engine, tables=[...])`, `from user import User` to register mappers).
SQLite in memory; **no production database is involved.**

The fixture is the 2026-01-09 signature in miniature: one symbol under repair, two collateral
symbols, one bulletin that names the collateral, and a neighbouring date that must never move.

```python
"""PI-017: a forced UOA re-run may delete only what it is about to recompute.

A single-symbol forced re-run used to delete every symbol's uoa_contract_daily and
uoa_symbol_daily rows for the date, plus the night's uoa_bulletins row, and then rebuild
one symbol -- the 2026-01-09 signature: 23 of ~499 symbols left, status 'success'
(research PI-017). uoa_bulletins feeds the SAS candidate universe
(services/candidate_universe_builder.py:38-48), so the blast radius is not confined to UOA.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from models import Base, UoaBulletin, UoaContractDaily, UoaSymbolDaily
from user import User  # noqa: F401 -- registers the User mapper
from services.uoa_screener import (
    FORCE_SCOPE_AUTO,
    FORCE_SCOPE_DATE,
    FORCE_SCOPE_UNIVERSE,
    delete_rows_for_forced_rerun,
    resolve_force_delete_scope,
)

TD = date(2026, 1, 9)        # the date the desk found wiped
TD_NEXT = date(2026, 1, 12)  # the neighbouring nightly, must never be touched


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(
        engine,
        tables=[UoaSymbolDaily.__table__, UoaContractDaily.__table__, UoaBulletin.__table__],
    )
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()


def _seed(session):
    for td in (TD, TD_NEXT):
        for sym in ("INTC", "AAPL", "MSFT"):
            session.add(UoaSymbolDaily(trading_date=td, symbol=sym, score_day=50.0))
            session.add(
                UoaContractDaily(
                    trading_date=td,
                    underlying_symbol=sym,
                    contract_symbol=f"{sym}260116C00100000_{td:%m%d}",
                    option_type="call",
                    expiration_date=date(2026, 1, 16),
                    strike_price=100.0,
                    dte=7,
                )
            )
        session.add(
            UoaBulletin(
                trading_date=td,
                model_version="uoa-1.0",
                lists_json=json.dumps({"day": [{"symbol": "AAPL"}, {"symbol": "MSFT"}]}),
                markdown=f"# UOA Bulletin - {td.isoformat()}",
            )
        )
    session.commit()


# --- the scope rule (pure, no DB) --------------------------------------------

def test_no_explicit_universe_still_means_the_whole_date():
    assert resolve_force_delete_scope(
        explicit_universe=None, resolved_universe=["AAPL", "MSFT"], force_scope=FORCE_SCOPE_AUTO
    ) is None


def test_explicit_universe_scopes_the_delete_and_is_normalised():
    assert resolve_force_delete_scope(
        explicit_universe=[" intc "], resolved_universe=[" intc "], force_scope=FORCE_SCOPE_AUTO
    ) == ["INTC"]


def test_universe_scope_never_returns_whole_date():
    assert resolve_force_delete_scope(
        explicit_universe=None, resolved_universe=["AAPL"], force_scope=FORCE_SCOPE_UNIVERSE
    ) == ["AAPL"]


def test_whole_date_is_reachable_only_by_asking_for_it():
    assert resolve_force_delete_scope(
        explicit_universe=["INTC"], resolved_universe=["INTC"], force_scope=FORCE_SCOPE_DATE
    ) is None


def test_unknown_scope_is_refused():
    with pytest.raises(ValueError):
        resolve_force_delete_scope(
            explicit_universe=None, resolved_universe=["AAPL"], force_scope="everything"
        )


# --- the delete itself (in-memory SQLite) ------------------------------------

def test_single_symbol_force_cannot_touch_other_symbols_or_the_bulletin(db):
    _seed(db)
    deleted = delete_rows_for_forced_rerun(db, trade_date=TD, symbols=["INTC"])

    assert deleted == {"contract_rows": 1, "symbol_rows": 1, "bulletins": 0}
    surviving = {r.symbol for r in db.query(UoaSymbolDaily).filter(UoaSymbolDaily.trading_date == TD)}
    assert surviving == {"AAPL", "MSFT"}
    assert db.query(UoaContractDaily).filter(
        UoaContractDaily.trading_date == TD, UoaContractDaily.underlying_symbol == "INTC"
    ).count() == 0
    assert db.query(UoaContractDaily).filter(UoaContractDaily.trading_date == TD).count() == 2
    # the night's bulletin -- a SAS candidate-universe source -- survives intact
    bulletin = db.query(UoaBulletin).filter(UoaBulletin.trading_date == TD).one()
    assert json.loads(bulletin.lists_json)["day"] == [{"symbol": "AAPL"}, {"symbol": "MSFT"}]
    # the neighbouring date is untouched
    assert db.query(UoaSymbolDaily).filter(UoaSymbolDaily.trading_date == TD_NEXT).count() == 3


def test_full_universe_force_still_replaces_the_whole_date(db):
    _seed(db)
    deleted = delete_rows_for_forced_rerun(db, trade_date=TD, symbols=None)

    assert deleted == {"contract_rows": 3, "symbol_rows": 3, "bulletins": 1}
    assert db.query(UoaSymbolDaily).filter(UoaSymbolDaily.trading_date == TD).count() == 0
    assert db.query(UoaBulletin).filter(UoaBulletin.trading_date == TD).count() == 0
    assert db.query(UoaSymbolDaily).filter(UoaSymbolDaily.trading_date == TD_NEXT).count() == 3
    assert db.query(UoaBulletin).filter(UoaBulletin.trading_date == TD_NEXT).count() == 1


def test_empty_symbol_list_deletes_nothing(db):
    _seed(db)
    assert delete_rows_for_forced_rerun(db, trade_date=TD, symbols=[]) == {
        "contract_rows": 0, "symbol_rows": 0, "bulletins": 0
    }
    assert db.query(UoaSymbolDaily).filter(UoaSymbolDaily.trading_date == TD).count() == 3
```

Add no test that touches Postgres, and do not import `db.py` anywhere in this file.

---

## 6. Rollback

```
git revert --no-edit <sha> && git push
```

One commit, five files, no data migration — the change writes nothing and deletes nothing by itself.
Reverting restores the whole-date delete, after which the header constraint applies again and no
forced UOA run may be executed on any date from 2026-06-01 onward.

---

## 7. Out of scope — do not touch

- **Cross-sectional percentiles on a subset run.** `_pct_rank`
  (`services/uoa_screener.py:870-895`) is applied at `:1592-1594` to the symbols the run recomputed,
  so a one-symbol re-run writes `unusual_day/swing/long = 0.0` and therefore deflated `score_*` /
  `label_*` for that symbol — values not comparable with the rest of the date. That is a second,
  pre-existing defect of subset runs, unchanged by this brief (§3.4 only logs a warning about it).
  Do not "fix" it here: any change to how a score is computed is a scoring change and needs its own
  research question. The desk will file it as its own register row.
- **Repairing 2026-01-09.** This brief repairs code, not data. Whether that hole is backfilled is
  Haci's decision (§8), it is a write, and it would need a `DATA_NOTES.md` repair-log row.
- **`run_uoa_oi_confirm`'s force path** (`services/uoa_screener.py:2018-2029`) and
  `run_gex_nightly`'s (`app.py:4042`, `scripts/run_gex_nightly.py:40-59`). Different functions,
  different tables, not audited here.
- **A run-history table.** PI-012 (three ranked picks on 2026-06-26 that no run audit records; no
  run-history table) is a separate register row. `uoa_runs` keeps `UNIQUE (run_type, trading_date)`
  (`models.py:390`) — one row per date, overwritten by re-runs. Do not add a table or change that
  constraint.
- **PI-001** (`fwd_return_*` maturation, branch `fix/pi-001-backfill-window-floor`) and **PI-013**
  (`score_swing` / `score_long` overwritten by the morning OI pass). Same tables, different defects.
- `services/uoa_scheduler.py`, `scripts/run_nightly_pipeline.py`,
  `services/candidate_universe_builder.py`, `services/super_agent_select_scoring.py`, and every
  router. §4(b) requires their diff to be empty.
- Any subscriber-visible copy, field, ordering or number. There are none in this change.

---

## 8. Verification at `/desk-run verify PI-017 <sha>`

**Whose step is whose.** The coding agent's work ends at §4 — repo checks only. Deployment is Haci's.
The queries below are the **Data Steward's**, on `$RESEARCH_DB_URL` under the read-only role
(`sas_research_ro`), counts only.

**Step 1 — Haci (deploy).** Merge and deploy. Nothing else is required for the fix to take effect:
the nightly path is unchanged, and the next forced run — whenever one happens — is scoped.

**Step 2 — Data Steward, read-only.** The before-state is the pinned freeze, not a live capture
(DP-50(c)): `research/data/v001_uoa_symbol.parquet`, sha256
`1b959ef809fe925d4f1794e1ae347d385879823fa133cb1f051dd983fae34ac4`, which records 2026-01-09 at 23
rows / 23 symbols and its neighbours at 498 and 499 (§1).

```sql
-- V1. Nothing in history moved. Must return exactly one row, unchanged: 2026-01-09, 23.
SELECT trading_date, count(DISTINCT symbol) AS n_symbols
FROM uoa_symbol_daily
GROUP BY trading_date
HAVING count(DISTINCT symbol) < 200
ORDER BY trading_date;

-- V2. Per-date row counts across the freeze window, to compare against the parquet.
SELECT trading_date, count(*) AS n_rows, count(DISTINCT symbol) AS n_symbols
FROM uoa_symbol_daily
WHERE trading_date BETWEEN DATE '2026-01-07' AND DATE '2026-09-10'
GROUP BY trading_date ORDER BY trading_date;

-- V3. The new audit fields appear on runs that happen after the deploy.
SELECT trading_date, status,
       (config_json::jsonb)->>'force'          AS forced,
       (config_json::jsonb)->>'force_scope'    AS force_scope,
       (config_json::jsonb)->>'universe_size'  AS universe_size,
       (stats_json::jsonb)->>'bulletin_action' AS bulletin_action
FROM uoa_runs
WHERE run_type = 'nightly'
ORDER BY trading_date DESC
LIMIT 10;

-- V4. One bulletin per date, still.
SELECT trading_date, count(*) AS n_bulletins
FROM uoa_bulletins
WHERE trading_date >= DATE '2026-09-01'
GROUP BY trading_date HAVING count(*) <> 1;
```

**PASS requires all four:**

1. **V1 is still the single 2026-01-09 row at 23 symbols.** A second short date appearing after the
   deploy means a forced run wiped one anyway — FAIL, revert per §6.
2. **V2 matches the frozen parquet row-for-row** over 2026-01-07..2026-09-10. Any per-date count that
   differs from the freeze is a historical rewrite this fix was not supposed to cause — FAIL.
3. **V3 shows the post-deploy nightlies at `status = 'success'`** with `force = false`,
   `force_scope = 'date'`, `universe_size` near 500 and `bulletin_action = 'rebuilt_from_full_date'`.
   Any nightly at `success_partial` means the scheduler is somehow passing a universe — FAIL.
4. **V4 returns no rows.**

**Step 3 — only if Haci later runs a forced repair (a write, his alone).** The command, the date
list, the symbol list and the row counts it will touch go in the register entry *before* it runs;
afterwards it gets a dated row in `research/data/DATA_NOTES.md` (table.column, date range, ship SHA),
and Q014 (decision 2027-04-05) and Q030 (decision 2027-04-12) are checked first per the header. The
desk does not run it, and neither does the coding agent.
