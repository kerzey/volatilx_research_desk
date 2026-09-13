# VERIFY PI-001 — `2d5776c` (floor the legacy outcome backfill window in-process)

**Status: IMPLEMENTED, verification PENDING DEPLOY.** Not `VERIFIED`, and not `FAILED`.
**Written:** 2026-09-13 by the desk, after Haci implemented the brief with a coding agent that
reported it could not run the two DB-touching steps (§4(b), Step B) because the only database
configured in the platform repo is production.
**Brief:** `research/briefs/PI-001_fwd_return_backfill_window.md`
**Platform commit:** `2d5776c` — `scripts/run_nightly_pipeline.py` (+53/−3) and
`tests/test_nightly_pipeline_backfill_window.py` (new, 74 lines). Two files, nothing else.

---

## 1. What is discharged, and how

**Step A — the code fix: LANDED as specified.** Read at `2d5776c`:
`MIN_BACKFILL_TRADING_DAYS = 65` (:39), `MAX_BACKFILL_TRADING_DAYS = 100` (:47),
`resolve_backfill_window()` (:78), the clamp-with-WARNING in the `else` arm (:178-186), and the
four observability additions — `status=starting` (:255), `status=success` (:335),
`digest_details` (:342) and `failure_details` (:374). The explicit `--backfill-start-date` path is
still honoured verbatim.

**§4(b) — "the backfill dry-run must be byte-identical": DISCHARGED WITHOUT A DATABASE.**
That check exists to prove the change did not touch `scripts/backfill_outcomes.py`. The commit
touches exactly two files and that is not one of them, so the file is byte-identical at
`2d5776c` and its dry-run output cannot differ. `git show --stat 2d5776c` is a stronger proof
than running the script twice, and it needs no DB. **The brief should not have asked for it.**

**The coding agent's DDL concern: correct to raise, but moot in fact.**
`scripts/backfill_outcomes.py:816` calls `create_tables()`, which is
`Base.metadata.create_all(bind=engine)` plus add-missing-column migrations (`db.py:47-52`). That
is real DDL. But `scripts/run_nightly_pipeline.py:223` invokes `scripts/backfill_outcomes.py` as a
subprocess on **every nightly run** (`current_step = "backfill_outcomes"`, :278), so that exact
DDL already executes against production every night. Running the script by hand adds no DDL
exposure the platform does not already take nightly. On a current schema both halves are no-ops.

**§4(a), §4(c) — the coding agent's own report covers these.** They need no DB.

---

## 2. What is NOT discharged

**§8 (V1/V2/V3) cannot run until the fix is deployed and one nightly has executed.** The commit
exists in the platform repo; the Azure WebJob runs the **deployed** copy under `wwwroot`. Until a
deploy ships `scripts/run_nightly_pipeline.py` at `2d5776c`, production still runs the stale
4-session window and coverage will not move. Nothing about `2d5776c` reaches the database by
itself.

**The desk has no database in this session** (`RESEARCH_DB_URL` is not set and sourcing
`.env.research` is denied here), so V1/V2/V3 will be run by the Data Steward in a session that has
the read-only role, after the deploy.

---

## 3. The "before" snapshot already exists, frozen and checksummed

§8 asked for a before-CSV taken prior to the deploy. That is unnecessary, and if the deploy has
already happened it would be impossible. **The desk already owns a better one:**
`research/data/v001_uoa_symbol.parquet`, pinned by sha256 in `manifest_v001.json` (as_of
2026-09-10), covering `trading_date` 2026-01-07 .. 2026-09-10 with all eleven columns V2 names.

Verified today on the brief's fixed date **2026-07-28**, and it matches the brief's predictions:

| column | non-null | of rows |
|---|---|---|
| `fwd_return_1d_pct` | 493 | 496 |
| `fwd_return_3d_pct` | 493 | 496 |
| `fwd_return_5d_pct` | **24** | 496 |
| `fwd_return_7d_pct` | **24** | 496 |
| `fwd_return_14d_pct` | **24** | 496 |
| `fwd_return_30d_pct` | **0** | 496 |
| `score_day` / `score_swing` / `score_long` / `label_swing` | 496 | 496 |
| `oi_confirm_mult` | 28 | 496 |

**Revised V2 procedure:** compare the post-deploy live rows against this parquet, not against a
CSV. Same test — every cell non-null in the freeze must be exactly equal afterwards; only
null → non-null transitions are permitted, and only in the six `fwd_return_*` columns. It is
strictly better evidence: immutable, sha256-pinned, and it predates the commit by construction.

---

## 4. Step B is one column and 15 dates — and the brief's date range is wrong

The brief estimated the residual hole as "roughly 2026-05-11 .. 2026-06-10" across horizons and
the coding agent read that as ~11,000 live price fetches. Measured from the frozen data instead of
estimated, the hole that will **not** self-heal is much narrower:

**`fwd_return_30d_pct` only, 15 trading dates, 7,460 row-cells, all at 0% coverage:**

```
2026-04-15, 2026-04-17,
2026-05-20, 2026-05-21, 2026-05-22, 2026-05-26, 2026-05-27, 2026-05-28, 2026-05-29,
2026-06-01, 2026-06-02, 2026-06-03, 2026-06-04, 2026-06-05, 2026-06-08
```

Everything else self-heals. A nightly run dated 2026-09-10 carries a 65-session window back to
**2026-06-09**, and the other cliffs all sit later than that: 14d at 2026-06-12, 7d at 2026-06-24,
5d at 2026-06-26. Those columns refill on the first post-deploy run with no sweep at all.

**The brief's Step B command misses two dates.** `--start-date 2026-05-11` excludes
**2026-04-15 and 2026-04-17**, which are holed (0 of ~501 on both). Corrected range:

```
python scripts/backfill_outcomes.py --tables uoa --start-date 2026-04-15 --end-date 2026-06-10 --dry-run --verbose
```

and the same line without `--dry-run` to write. Never `--force`.

### The hole grows one date per session until the fix is deployed

The 65-session window slides forward with the run date. Each session that passes before the first
post-deploy nightly moves the trailing edge forward one session and strands one more date:

| first post-deploy nightly | window reaches back to | consequence |
|---|---|---|
| 2026-09-11 (Fri) | 2026-06-10 | 30d hole stays at 15 dates |
| 2026-09-14 (Mon) | 2026-06-11 | 30d hole stays at 15 dates; 14d still fully saved |
| **2026-09-15 (Tue)** | **2026-06-12** | **the 14d column starts going permanently dark, ~497 cells per session** |
| 2026-09-24 or later | 2026-06-24 onward | 7d, then 5d (2026-06-26), begin the same |

So the deploy is the urgent half, not the sweep. Deploying in time for Monday's nightly keeps the
permanent damage at one column and 15 dates. Every session after that adds a column-date the
sweep would then also have to cover.

---

## 5. Research impact: none

`uoa_symbol_daily.fwd_return_*` is banned as an outcome for desk studies
(`research/data/DATA_NOTES.md`; `FREEZE_v001.md` §5) — the desk computes forward returns from its
own pinned price freeze. No locked PREREG reads these columns, no LEDGER row depends on them, and
filling them changes no research result. The frozen parquet is immutable regardless of what
happens in production. Nothing here touches rule 3 or rule 4.

---

## 6. Disposition

`PI-001` stays at **`IMPLEMENTED:2d5776c`** with this residual-hole note, exactly as the brief's §8
directs when the sweep has not been run. It reaches `VERIFIED` only when all four PASS conditions
hold, which requires, in order:

1. Haci deploys `2d5776c` to Azure (`wwwroot`), ideally before the 2026-09-14 nightly.
2. Haci confirms the next nightly log prints `backfill_window_trading_days=65` (or 70) and
   `backfill_window_clamped=False` — the brief's §3 Step A' also asks him to re-sync the stale
   WebJob wrapper in Kudu, which is independent of the deploy.
3. Haci decides on the 30d sweep (§4 above) — his call, because it moves the UOA/whale performance
   aggregates in `routers/performance.py` off a biased ~5% sample and onto a full one.
4. The Data Steward runs V1/V2/V3 against the read-only role and compares V2 to the frozen parquet.

**A note on leaving the sweep undone.** The unhealed stretch is not neutral. After the deploy,
30d coverage will read ~0% for 2026-04-15..2026-06-08 and ~99% from 2026-06-09 onward, so any
trailing-window aggregate that spans that boundary mixes two sampling regimes. Either run the
sweep, or have the performance surfaces exclude the unhealed dates from the 30d aggregate. The
worst option is to leave it half-filled and keep quoting the blended number.
