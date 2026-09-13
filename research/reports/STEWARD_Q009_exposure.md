# Steward report: Q009 exposure-only stop count (R1) and payload-integrity rulings (R3)

Data Steward, 2026-09-13. Routed requests R1 and R3 from
`research/questions/Q009_stop_whipsaw/DECISIONS.md` ("Routed requests"). R2 (successor freezes)
is due at the decision date and was not built in this run.

Frozen data only: `research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`
(`v001_sas_candidates.parquet`, `v001_sas_runs.parquet`, `v001_outcome_corrections.parquet`,
`p001_daily_split.parquet`) + `research/data/exclusions_v002.json`. No live query. No `results/`
directory was read. R1 inputs are exactly as specified: pick-night close, ATR14 through night t,
and `public_payload_json.lane_plans.swing_trading` -- no bar dated after night t, not even the
session t+1 open; no touch, no return, no target outcome. Counts only.

---

## R1 -- exposure-only stop count

**Population and method.** Published picks (`qualified IS TRUE AND selected_rank IS NOT NULL`,
DP-28) on non-excluded nights (`exclusions_v002.json`, `manual_runs.trading_dates` union
`non_session_runs.trading_dates`), pick night >= 2026-06-01, whose **20-session** forward window
(DP-09 clock) has matured against the SPY-implied trading calendar in `prices_daily_split` (153
sessions, 2026-02-02..2026-09-10). `dir` = +1 bullish / -1 bearish from `dominant_direction`;
`S` = `lane_plans.swing_trading.stop`; `T` = L3 = `lane_plans.swing_trading.targets[0]`;
`s_close = dir x (C_t - S) / ATR`; `d_close = dir x (T - C_t) / ATR`. ATR14 = mean true range
over the 14 sessions ending at t (the desk's standard construction,
`research/reports/explore/scripts/03_build_core.py:71-74`). This reproduces Q007's R2 population
exactly (394 published rows / 49 matured nights, last matured night 2026-08-12), confirming the
calendar/maturity logic is consistent across questions.

### (a) Population funnel

**394 published picks / 49 matured nights** (pick night >= 2026-06-01, non-excluded, 20-session
window matured; last matured pick night 2026-08-12):

| Stage | Removed | Remaining |
|---|---|---|
| Published, in-window, non-excluded, matured (20-session) | -- | 394 |
| No lane-plan ladder at all (no `swing_trading` in payload) | 8 | 386 |
| Swing lane present but no L3 | 0 | 386 |
| Swing lane and L3 present but `stop` NULL (**null-stop denominator**) | **0** | 386 |
| Non-bullish/bearish `dominant_direction` | 0 | 386 |
| No `C_t` or no ATR | 0 | 386 |
| `outcome_target_invalid` non-null | 4 | 382 |
| Wrong-side stop (`s_close <= 0`) | 67 | 315 |
| Wrong-side L3 (`d_close <= 0`) | 2 | 313 |
| Symbol with fewer than 60 daily bars dated <= t | 0 | 313 |
| **ELIGIBLE (all filters passed)** | -- | **313** |

**Headline: the null-stop denominator is 0.** Every published pick in the window that carries a
swing lane at all (386 of 394) carries a non-null stop and a non-null L3. This is not a
window-specific artifact: re-run against the **entire published history** (907 published rows,
all dates), 33 have no swing lane at all, and of the remaining 874, **0 have a missing L3 and 0
have a missing stop.** The "unknown headline number" the PREREG flagged is verifiably zero.

**Wrong-side stop is the binding exclusion, not the null-stop.** 67 of 382 (17.5%) eligible-so-far
picks have a stop on the wrong side of `C_t` -- consistent with §10 threat 2 (the stop is
anchored to the lane `entry`, which can stray from spot). The 4 `outcome_target_invalid` removals
are exactly the 4 in-window rows the E9a correction batch touched (2026-06-01 MSFT; 2026-06-03
CRWD, AVGO; 2026-06-04 AMAT -- see R3 below); this funnel step already handles them correctly.

### (b) Eligible picks by bucket (313 total, 48 nights)

| Bucket | Picks | Share |
|---|---|---|
| TIGHT (`0 < s_close < 1.0`) | 291 | 93.0% |
| MID (`1.0 <= s_close < 2.0`) | 22 | 7.0% |
| WIDE (`s_close >= 2.0`) | 0 | 0.0% |

Max `s_close` among eligible picks in-window is 1.70 ATR -- **no WIDE picks exist in this window
at all.** Nights with >= 1 eligible pick (any bucket): 48. Nights with >= 1 eligible TIGHT pick:
48 (identical set -- every eligible night has at least one TIGHT pick).

### (c) Contributing nights on the three definitions + B1-valid control-pool availability

Per-night non-published control pool (complement of the DP-28 predicate -- qualified-false and
dark-lane rows alike -- with symbol history >= 60 daily bars dated <= t):

| | Value |
|---|---|
| Share of eligible picks with >= 10 same-night non-published controls | 100.0% |
| Share of eligible picks with >= 3 same-night non-published controls | 100.0% |
| Median control-pool size (night-level, weighted by eligible picks) | 54 |
| 10th percentile control-pool size | 41 |

The nearest-10 pool never binds in this window -- every eligible night has a same-night
non-published pool far above the 10-row floor (10th percentile is 41).

| Definition | Contributing nights (of 49 matured nights) |
|---|---|
| **P1 (B1-valid)** -- >= 1 eligible pick with >= 10 same-night non-published controls | 48 |
| **P2** -- >= 1 eligible pick | 48 |
| **P3 (TIGHT)** -- >= 1 eligible TIGHT pick | 48 |

All three collapse to the same 48/49 matured nights (the one non-contributing matured night has
no eligible pick at all -- lost to the wrong-side-stop/L3 filters). The B1-valid condition never
binds separately from P2 in this window because the control pool is never thin.

### (d) Monthly run-rate and projected date to 80 contributing nights

| Month | P1 (B1-valid) | P2 | P3 (TIGHT) |
|---|---|---|---|
| 2026-06 | 20 | 20 | 20 |
| 2026-07 | 20 | 20 | 20 |
| 2026-08 (partial -- matured only through 08-12) | 8 | 8 | 8 |

Rate = contributing nights / elapsed trading sessions from first matured night (2026-06-01) to
last matured night (2026-08-12) inclusive = 51 sessions; projected forward at that constant rate,
sessions converted to calendar days at 365/252 (same method as `STEWARD_Q007_exposure.md` R2).

| Definition | n today | rate/session | sessions needed for 80 | projected date |
|---|---|---|---|---|
| P1 (B1-valid) | 48 | 0.941 | 34.0 more | **2026-09-30** |
| P2 | 48 | 0.941 | 34.0 more | **2026-09-30** |
| P3 (TIGHT) | 48 | 0.941 | 34.0 more | **2026-09-30** |

All three project to 80 contributing nights by **2026-09-30**. This is a mechanical extrapolation
of the June-August run-rate only; no reading of what it means for locking or for P3's status as
primary is offered here -- that is R-3, Haci's, per the routed request.

### (e) Null-stop share and TIGHT/MID/WIDE split, by month and score band

Null-stop count/share (denominator = picks with swing lane **and** L3 present, before the stop
filter) is 0 in every month and every score band:

| Month | n (swing+L3 present) | null-stop | share |
|---|---|---|---|
| 2026-06 | 163 | 0 | 0.0% |
| 2026-07 | 159 | 0 | 0.0% |
| 2026-08 | 64 | 0 | 0.0% |

| Score band | n (swing+L3 present) | null-stop | share |
|---|---|---|---|
| < 80 | 1 | 0 | 0.0% |
| 80-85 | 317 | 0 | 0.0% |
| 85-90 | 51 | 0 | 0.0% |
| 90+ | 17 | 0 | 0.0% |

TIGHT/MID/WIDE split of eligible picks, by month and by score band (counts only):

| Month | MID | TIGHT | WIDE |
|---|---|---|---|
| 2026-06 | 9 | 120 | 0 |
| 2026-07 | 11 | 123 | 0 |
| 2026-08 | 2 | 48 | 0 |

| Score band | MID | TIGHT | WIDE |
|---|---|---|---|
| < 80 | 1 | 0 | 0 |
| 80-85 | 20 | 237 | 0 |
| 85-90 | 1 | 39 | 0 |
| 90+ | 0 | 15 | 0 |

### (f) Fallback-pattern stops (stop exactly 0.5% from lane entry, targets +0.5%/+1%)

`ai_agents/principal_agent.py:897-911` default_setup: `step = |entry| x 0.005`;
`stop = entry -+ step`; `targets = [entry +- step, entry +- 2*step]`. Matched with a rounding
tolerance (values are written `round(x, 2)`).

| Month | n (swing+L3 present) | fallback-pattern | share |
|---|---|---|---|
| 2026-06 | 163 | 0 | 0.0% |
| 2026-07 | 159 | 0 | 0.0% |
| 2026-08 | 64 | 0 | 0.0% |

**0 of 386 in-window, and 0 of 874 across the entire published history** carry the fallback
pattern (sanity-checked against the full manifest, not just the window, to rule out a detector
bug). Published/qualified picks appear never to fall back to the deterministic default -- plausibly
because reaching `qualified` status already implies the LLM strategist produced a usable setup.

---

## R3 -- two pre-lock rulings on payload integrity

### Ruling 1 -- did the 2026-06-26 mixed-state mutation touch `public_payload_json`?

**PASS/FAIL: POSITIVE -- it did.** `research/data/exclusions_v003.json` is needed before Q009 can
lock (see "What would go in it" below); it is **not issued in this run**.

**Evidence.** All 52 `sas_candidates` rows for trading_date 2026-06-26 share one `created_at`
(2026-06-26 21:17:31.403724 UTC) -- a single-batch write, not a re-run (no KT-audit-style
timestamp-reset signature). The run's own `stats_json` for that night -- the contemporaneous 16:05
ET audit trail -- records `qualified_count: 8`, `qualification_counts.selected: 8`, and
`direction_counts` showing 0 bearish selections that night. The frozen `sas_candidates` table,
however, shows 11 rows with `qualified = TRUE` and a non-null `selected_rank`: the 8 bullish picks
the run's audit corroborates (AXON, GWW, INCY, LLY, PANW, LYV, GNRC, CRWD, ranks 1-8) plus 3
bearish rows the run's audit does not corroborate at all (DPZ, COIN, AAPL -- ranks 1, 2, 3,
duplicating the bullish top-3). Each of the 3 extra rows carries a fully-formed, internally
consistent `public_payload_json` (complete `lane_plans` for all three lanes, with the `rank` field
inside the payload matching the row's outer `selected_rank`) -- the mutation did not just flip a
`qualified` flag, it produced a complete competing payload including the swing-lane stop Q009
studies. 10 of the 11 rows -- including all 3 of the uncorroborated bearish ones -- pass every
filter in R1's funnel and sit in the 313-pick eligible population, all TIGHT bucket.

**This is not the normal bull/bear dual-rank convention.** Across the whole 113-night history,
many nights carry a separate bullish rank-1..N and a separate bearish rank-1..N sharing the same
integer (e.g. 2026-07-10, 07-21, 08-17, 09-10 all show a duplicated rank-1 slot, one bull one
bear) -- and on every one of those nights, `sas_runs.stats_json.qualified_count` matches the frozen
row count exactly. Checked across all 113 nights in the manifest: **2026-06-26 is the only night
in the entire frozen history where the actual qualified-row count (11) disagrees with the run's
own `stats_json.qualified_count` (8).** That isolation -- 1 of 113, and by exactly the 3 bearish
rows the run's own audit never selected -- is the "partial row mutation, not a re-run" the red
team flagged.

**Dates.** Trading date: 2026-06-26. Row creation (all 52 rows, uniform): 2026-06-26
21:17:31.403724 UTC. `updated_at` for the 3 uncorroborated rows (AAPL, DPZ, COIN): 2026-09-10
21:16:18.413734 UTC -- but that exact timestamp is shared with 16 other same-night rows
(including several of the run-audit-corroborated bullish picks) and with 670 of 4,195 rows
window-wide, clustered in the week of the freeze (09-05/08/09/10) -- a routine late
outcome-column backfill, the same pattern STEWARD_Q007_exposure.md documented (about 18% of rows
touched later, consistent with routine outcome-column backfill). The frozen table has no
per-column timestamp, so the exact moment the `qualified`/`selected_rank`/payload mutation itself
happened cannot be pinned more precisely than "after the 2026-06-26 16:05 ET run, before the
2026-09-10 freeze" -- the same limitation already disclosed in the Q007 report.

**What would go into `exclusions_v003.json` (not issued here).** A new block excluding trading_date
2026-06-26 from Q009's population under DP-22 (citing this report), on the grounds that the
publication predicate cannot be trusted for that single night -- specifically that 3 of its 11
"published" rows (AAPL, DPZ, COIN) are not corroborated by the night's own 16:05 ET run audit.
Whether to exclude the whole night or only the 3 uncorroborated rows is a scope choice for
whoever issues v003 (excluding the whole night is the more conservative, KT-audit-consistent
option, since the 8 corroborated bullish rows' payloads have not themselves been shown clean of
the same write path); this report does not decide that.

### Ruling 2 -- did E9a / the wrong-side-target guard / the cross-lane re-sort rewrite historical rows' payloads inside 2026-06-01..2026-09-10?

**PASS/FAIL: NEGATIVE -- no evidence of a historical payload rewrite from any of the three.**

**E9a** (commit `f94e347`, 2026-07-05, platform repo): 114 ledger entries, authorization =
`E9-2026-07-05`, in `v001_outcome_corrections.parquet`. Fields touched, across all 114 rows:
`outcome_target_invalid` (24), `outcome_hit_by_20` (24), `outcome_hit_by_40` (22), `outcome_hit_by_60`
(22), `outcome_days_to_hit_w60` (22) -- never `public_payload_json` and never any `lane_plans` field.
Checked across the entire 795-row correction ledger (every authorization, every cause,
2026-01..2026-09): not one row touches a payload field -- every correction is an `outcome_*` or
`level_hit_dates.*` or `bear_projection_source` column. `trading_date` range for E9a is
2026-04-07..2026-06-04; only 4 rows fall inside Q009's >= 2026-06-01 window (2026-06-01 MSFT;
2026-06-03 CRWD, AVGO; 2026-06-04 AMAT), and those are exactly the 4 rows R1's funnel removes at
the "`outcome_target_invalid` non-null" step -- the existing exclusion already handles them
correctly; no separate action needed.

**Wrong-side-target guard (E9b, same commit).** Read from the platform source
(`services/super_agent_select_service.py`, Phase 0.5e diff) -- it runs inside the nightly
candidate-creation loop, setting `row.outcome_target_invalid` only on the row being newly written
that night. It has no backfill path and touches no existing row; it cannot retroactively touch a
historical payload by construction.

**Cross-lane monotonic re-sort (W3, commit `5fa3db4`, deployed 2026-07-06 19:13:42 UTC).** The
commit's own docstring states "Historical rows are untouched" -- it runs inside
`_extract_lane_plans`, called only at row-creation time. Checked against the data: of the 4,195
`sas_candidates` rows in Q009's window (2026-06-01..2026-09-10), 750 (17.9%) show
`updated_at > created_at` -- but zero of those late touches land on 2026-07-05, 2026-07-06 or
2026-07-07 (the E9a/W3 deployment dates); all 750 cluster on 2026-09-05, 09-08, 09-09 and
2026-09-10 (freeze week), matching the routine backfill pattern, not a mid-window rewrite tied to
either commit. No row created before the W3 deployment shows an `updated_at` landing in the
deployment window.

**Dates.** E9a correction batch: 2026-07-05 (all 114 rows, `correction_date` and
`created_at`/`updated_at` identical to the second). W3 deployment: 2026-07-06 19:13:42 UTC (commit
timestamp; first nightly run it could affect is trading_date 2026-07-06 or later). No row-level
evidence of a rewrite on or after either date for rows with `trading_date` before it.

**Net:** §10 threats 6 and 11 are not both negative -- threat 6 (E9a/guard/re-sort) is verified
negative and can be marked so with this report cited; **threat 11 (2026-06-26) is positive** and
blocks the lock under DP-22 until an `exclusions_v003.json` is issued (scope choice above) and the
PREREG is updated to cite it.

---

## Files

- This report: `research/reports/STEWARD_Q009_exposure.md`.
- No new data files were written; all counts were re-derived from
  `research/data/v001_sas_candidates.parquet`, `research/data/v001_sas_runs.parquet`,
  `research/data/v001_outcome_corrections.parquet` and `research/data/p001_daily_split.parquet`
  against `research/data/exclusions_v002.json`. No manifest, exclusions or state file was created
  or modified.

---

## Addendum, 2026-09-13 -- Q009 population under `exclusions_v003.json` (R4)

Delivered as part of R4 (`research/questions/Q009_stop_whipsaw/DECISIONS.md`, "Routed requests"):
`research/data/exclusions_v003.json` re-derived `night_counts_after_exclusions` and, per R4's
request, this addendum re-derives Q009's R1 population under the new file so the Registrar can
quote measured figures rather than the decision-maker's arithmetic. Same method, same inputs,
same frozen tables as R1 above (`manifest_v001.json` + `manifest_prices_v001.json`, no bar dated
after night t, counts only) -- the only change is the exclusion set: `exclusions_v002.json`'s
`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`, now also excluding
`exclusions_v003.json`'s new `uncorroborated_publication_runs.trading_dates` (2026-06-26, whole
night).

### Population funnel, re-derived (v003)

| Stage | Removed | Remaining |
|---|---|---|
| Published, in-window, non-excluded, matured (20-session) | -- | 383 |
| No lane-plan ladder at all | 8 | 375 |
| Swing lane present but no L3 | 0 | 375 |
| Swing lane and L3 present but `stop` NULL | 0 | 375 |
| Non-bullish/bearish direction | 0 | 375 |
| No `C_t` or no ATR | 0 | 375 |
| `outcome_target_invalid` non-null | 4 | 371 |
| Wrong-side stop (`s_close <= 0`) | 66 | 305 |
| Wrong-side L3 (`d_close <= 0`) | 2 | 303 |
| Symbol with fewer than 60 daily bars dated <= t | 0 | 303 |
| **ELIGIBLE (all filters passed)** | -- | **303** |

Matured nights fall from 49 to **48** (2026-06-26 was itself a matured night; removing it removes
one whole night from the denominator, not a partial-night count). Published picks fall from 394
to **383** -- exactly the 11 rows the night carried. Of those 11, one had already been removed by
R1's wrong-side-stop filter (67 -> 66 at that step here), so eligible picks fall by exactly 10:
**313 -> 303**, matching R3 ruling 1's count that 10 of the night's 11 rows sat in the eligible
population.

### Eligible picks by bucket (v003: 303 total, 47 nights)

| Bucket | Picks | Share |
|---|---|---|
| TIGHT (`0 < s_close < 1.0`) | 282 | 93.1% |
| MID (`1.0 <= s_close < 2.0`) | 21 | 6.9% |
| WIDE (`s_close >= 2.0`) | 0 | 0.0% |

Bucket composition is essentially unchanged from v002 (TIGHT 93.0% -> 93.1%, MID 7.0% -> 6.9%,
WIDE still empty) -- the excluded night's picks were removed roughly in proportion, not
concentrated in one bucket (9 TIGHT + 1 MID of the 10 eligible dropped rows).

### Contributing nights (v003)

All three definitions (P1 B1-valid, P2, P3 TIGHT) again collapse to the same count: **47 of 48**
matured nights carry >= 1 eligible pick. The B1 control-pool condition still never binds
separately in this window (every published pick has a large same-night non-published pool; the
2026-06-26 exclusion removes the night's rows from both sides of that comparison, so it does not
change which nights clear the >= 10-control floor).

### Net effect of v003 on Q009's registered population

| | v002 | v003 | Change |
|---|---|---|---|
| Matured nights | 49 | 48 | -1 |
| Published picks (in-window, non-excluded, matured) | 394 | 383 | -11 |
| Eligible picks | 313 | 303 | -10 |
| Contributing nights (all 3 definitions) | 48 | 47 | -1 |
| TIGHT / MID / WIDE | 291 / 22 / 0 | 282 / 21 / 0 | -9 / -1 / 0 |

No gate changes: `eval.py` reads these measured counts directly, never a projection. The
80-contributing-night floor (DP-21) and the 30-contributing-night-after-lock floor (DP-24) move
by one fewer starting night; DECISIONS.md item 20 already priced this in ("cost is one night: 48
-> 47 contributing nights and ~= 10 eligible picks, which changes no gate").

**Files.** No new data files were written for this addendum; counts re-derived from the same
frozen parquet as R1 (`v001_sas_candidates.parquet`, `v001_sas_runs.parquet`,
`v001_outcome_corrections.parquet`, `p001_daily_split.parquet`) against
`research/data/exclusions_v003.json`. No manifest, exclusions or state file was modified by this
addendum; `exclusions_v003.json` itself was written separately as R4's deliverable.
