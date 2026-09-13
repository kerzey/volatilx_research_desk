# Steward report: Q007 exposure-only counts (R2) and price-basis verification (R3)

Data Steward, 2026-09-12. Routed requests R2 and R3 from `research/questions/Q007_gap_at_open/DECISIONS.md`.
Frozen data only: `research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`
(`v001_sas_candidates.parquet`, `p001_daily_split.parquet`, `p001_daily_raw.parquet`,
`p001_hourly_raw.parquet`). No live query. No `results/` directory was read. Counts and pass/fail
only -- no touch, return or outcome of any kind below.

Exclusions applied: `research/data/exclusions_v002.json` (`manual_runs.trading_dates` union
`non_session_runs.trading_dates`). Only 2026-07-02 differs from `exclusions_v001.json` inside
Q007's >= 2026-06-01 window, so this matches the PREREG-cited fallback population exactly.

---

## R2 -- exposure-only contributing-night counts

**Population and method.** Published picks (`qualified IS TRUE AND selected_rank IS NOT NULL`,
per DP-28) on non-excluded nights, pick night >= 2026-06-01, whose 20-session forward window has
matured against the trading calendar implied by `prices_daily_split` (SPY bars; last freeze date
2026-09-10, 153 sessions from 2026-02-02). `C_t` = pick-night close, `O_{t+1}` = next-session
official open, both from `prices_daily_split`. `L3` = `lane_plans.swing_trading.targets[0]` from
`public_payload_json` (confirmed against `services/sas_conviction_card.py:183-186`: L3 is the
first swing-lane target). `g = dir x (O_{t+1} - C_t) / C_t x 100`. "Eligible" = published, has an
L3, L3 on the correct side of `C_t`, L3 not at/through `O_{t+1}`, `O_{t+1}` present (per
DECISIONS.md R2's filter list, applied literally -- note this is a *stricter, gap-group-only*
filter for this exposure count and is not the PREREG's own touch rule, which grades a gap-through
at the open as a hit rather than excluding it).

**Population funnel** (394 published picks / 49 matured nights, last matured pick night
2026-08-12; window: June-August 2026 only, since September nights have not yet matured):

| Stage | Rows removed | Rows remaining |
|---|---|---|
| Published, in-window, non-excluded, matured | -- | 394 |
| No lane-plan ladder (no L3 in payload) | 8 | 386 |
| Non-bullish/bearish `dominant_direction` | 0 | 386 |
| No `C_t` | 0 | 386 |
| Has `C_t`, no `O_{t+1}` | 0 | 386 |
| Wrong-side ladder (L3 not beyond `C_t` in pick direction) | 2 | 384 |


**Per-arm pick counts** (of the 384 side-ok picks, classified by `g` regardless of the
passed-at-entry filter):

| Arm | Picks (side-ok) | Passed-at-entry (excluded) | Eligible picks | Nights with >=1 eligible pick |
|---|---|---|---|---|
| AGAINST (g <= -2.0) | 47 | 0 | 47 | 23 |
| FAVOUR (g >= +2.0) | 42 | 7 | 35 | 21 |
| FLAT (\|g\| < 1.0) | 201 | 0 | 201 | 46 |
| MIDDLE (1.0 <= \|g\| < 2.0, descriptive only) | 94 | 2 | 92 | -- |

**Contributing nights** (>=1 eligible arm pick AND >=1 eligible FLAT pick, same night):

| Arm | Contributing nights (of 49 matured nights) |
|---|---|
| AGAINST + FLAT | 22 |
| FAVOUR + FLAT | 20 |
| TOTAL (union of the two) | 35 |


**Monthly run-rate of contributing nights:**

| Month | AGAINST | FAVOUR | TOTAL (union) |
|---|---|---|---|
| 2026-06 | 6 | 10 | 15 |
| 2026-07 | 13 | 6 | 14 |
| 2026-08 (partial -- matured only through 08-12) | 3 | 4 | 6 |

**Projection to 80 contributing nights** (rate = contributing nights / elapsed trading sessions
from first matured night 2026-06-01 to last matured night 2026-08-12 inclusive = 51 sessions;
projected forward at that constant rate, converting sessions to calendar days at 365/252):

| Arm | n today | rate (per session) | sessions needed for 80 | projected date |
|---|---|---|---|---|
| AGAINST | 22 | 0.431 | 134.5 more | **2027-02-22** |
| FAVOUR | 20 | 0.392 | 153.0 more | **2027-03-21** |
| TOTAL (union) | 35 | 0.686 | 65.6 more | **2026-11-14** |

Both arm-specific projections (AGAINST, FAVOUR) fall after the PREREG's hard stop of
**2027-01-25**; the union/total projection does not. These are mechanical extrapolations of the
June-August run-rate only -- no interpretation of what that means for the primaries is offered
here; that reading belongs to the registrar and Haci per DECISIONS.md.


---

## R3 -- price-basis verification

### Part 1 (load-bearing): is `prices_daily_split.o` the official 09:30 ET open, and do `o`/`h`/`l` exclude extended hours?

**Method.** Random sample of 40 symbol-dates drawn from the 227-symbol set covered by
`prices_hourly_raw`, seed fixed for reproducibility. For each symbol-date: (a) confirmed the
raw-to-split scaling factor is identical across `o`, `h`, `l`, `c` (validates that a raw-basis test
carries over to the split-adjusted series); (b) located the hourly bar containing 09:30 ET,
computed DST-aware per date (America/New_York, `zoneinfo`) rather than a fixed UTC offset; (c)
checked `daily_raw.o` falls within that bar's low/high; (d) checked `daily_raw.h`/`l` do not
exceed the min-low/max-high envelope of the hourly bars spanning the official 09:30-16:00 ET
regular session.

**Result: PASS, 40/40 (sample size 40).**

| Check | Pass | Sample |
|---|---|---|
| Raw-to-split factor consistent across o/h/l/c | 40 | 40 |
| Daily open falls inside the hourly bar containing 09:30 ET | 40 | 40 |
| Daily high/low do not exceed the regular-session (09:30-16:00 ET) hourly envelope | 40 | 40 |

**Caveat, stated plainly.** The frozen data is hourly, not tick/minute-level, so this cannot
confirm `o` is the exact 09:30:00 print to the second -- only that it falls inside the single
hourly bar that contains the official open and not in a bar that is purely pre- or post-market,
and that the daily high/low are never more extreme than what the regular-session hourly bars
show. A first pass (before correcting for DST) mis-flagged 2 of 40 symbol-dates (2026-02-20,
2026-03-05) as inconsistent; both were pre-DST (EST) dates where a fixed UTC-hour assumption was
off by one hour. After computing the 09:30/16:00 ET boundary per-date with proper DST handling,
all 40 pass. This is disclosed so the same DST hazard is not silently reintroduced in `eval.py`.


### Part 2 (optional): was the report date behind `days_to_earnings_corrected` available by 16:05 ET on the pick night?

**Established via platform code read-through (not a live query), for trading_date >= 2026-06-01
(all of Q007's window):** `days_to_earnings_corrected` is written on the **live scoring path**
(`services/super_agent_select_service.py:396-403`), sourced from `scorecard.days_to_earnings`,
which `services/super_agent_select_scoring.py:1438,1482` populates from
`context.catalyst_context["days_to_earnings"]` -- a same-run, forward-looking earnings-calendar
lookup anchored at `trading_date` (`services/symbol_context_builder.py`, calling
`services/projection_picks.py:_fetch_earnings_dates_bulk`). This runs inside the same nightly
scoring pass that produces the `sas_candidates` row, not a later backfill. The one backfill script
that touches these columns, `scripts/rescore_sas_earnings_corrected.py`, is explicitly scoped by
its own docstring to the pre-fix historical window (rows already scored under the old, wrong
resolver) -- i.e. it targets trading_date < 2026-06-01, not Q007's window.

Row-timestamp check (frozen `sas_candidates`, trading_date >= 2026-06-01, n = 4,195 rows):
`updated_at` is within 30 minutes of `created_at` for 3,454 rows (82%); the remaining 741 (18%)
are touched later, spread across nearly every sealed night rather than concentrated on any
earnings-specific pattern -- consistent with routine outcome-column backfill (`outcome_*`,
`level_hit_dates_json`, which are known to mature over weeks) rather than a later change to the
earnings field itself. The frozen table has no per-column timestamp, so this cannot fully
separate the two effects at the row level.

**Verdict: PASS (code-path evidence) for trading_date >= 2026-06-01 -- Q007's whole window.** Not
established, and not needed, for trading_date < 2026-06-01 (outside Q007's window; already known
wrong per `CLAUDE.md`/`DATA_NOTES.md`).

---

## Files

- `research/data/exclusions_v002.json` -- issued this session (R1).
- `research/data/DATA_NOTES.md` -- paragraph added this session (R1).
- This report: `research/reports/STEWARD_Q007_exposure.md`.

---

## R5 -- variant-B (B3 gap-matched control) feasibility, counts only

Data Steward, 2026-09-13. Routed request R5 from `research/questions/Q007_gap_at_open/DECISIONS.md`
("Routed requests" section). Frozen data only: `research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json` (`v001_sas_candidates.parquet`,
`p001_daily_split.parquet`). No live query. No `results/` directory was read (none exists for
Q007). Counts and dates only -- no price level beyond `C_t`/`O_{t+1}`, no forward bar beyond the
t+1 open, no touch, no return, no target, no outcome of any kind below.

**Population (identical to R2, re-derived from the frozen parquet, not from a cached result):**
published picks (`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28) on non-excluded nights
(`research/data/exclusions_v002.json`), pick night >= 2026-06-01, 20-session forward window
matured against the SPY-implied trading calendar in `prices_daily_split` (153 sessions,
2026-02-02..2026-09-10; last matured pick night 2026-08-12) -- **394 published rows / 49 matured
nights**, reproduced exactly. Applying the R2 funnel (8 no-ladder, 2 wrong-side, then per-arm
passed-at-entry: 0 AGAINST / 7 FAVOUR / 0 FLAT / 2 MIDDLE excluded) gives the same eligible-pick
counts as R2: **AGAINST 47, FAVOUR 35, FLAT 201** (MIDDLE's 92 excluded from R5 -- the request
covers AGAINST/FAVOUR/FLAT only). Total eligible picks in scope: 283.

**Method.** For each eligible pick p (night t, direction `dir_p`, arm), the B3 restricted pool is
every same-night `sas_candidates` row that is **not** published (complement of the §2 predicate --
includes qualified-false rows and dark-lane rows alike, per PREREG §3 B3 / §2), whose symbol has
>= 60 daily bars dated <= t in `prices_daily_split` (2,437 non-published rows on the 49 matured
nights; 2,432 have both a `c_t` and a session-t+1 open and >=60 bars -- 5 rows drop for a missing
forward-open/close, per the same "missing forward bar" bookkeeping as R2). Each pool row's own gap
is computed **direction-adjusted with p's direction**: `g_c = dir_p x (O_{t+1,c} - C_{t,c}) /
C_{t,c} x 100`, and classified with p's own arm cuts (AGAINST <= -2.0, FLAT |g| < 1.0, FAVOUR >=
+2.0). The count reported is the size of that restricted pool in p's own group -- this is the
**pool size before the nearest-10 feature match** (PREREG §3: B3 is missing if this pool has fewer
than 3 rows), so the nearest-neighbour selection on `beta60`/`atr_pct`/`runup20` was not run; it is
irrelevant to whether B3 is reachable at all. Because the restricted-pool count for a given pick
depends only on (night, `dir_p`, arm-cut), not on the individual pick, picks sharing a night and a
direction share the same pool count by construction.

### (a) Picks per arm with >= 3 same-group non-published controls

| Arm | Eligible picks | Picks with >= 3 controls | Share |
|---|---|---|---|
| AGAINST | 47 | 40 | 85.1% |
| FAVOUR | 35 | 30 | 85.7% |
| FLAT | 201 | 201 | 100.0% |

### (b) Control-count distribution per arm

| Arm | Median | 10th percentile | Min | Max |
|---|---|---|---|---|
| AGAINST | 7 | 1.6 | 0 | 26 |
| FAVOUR | 10 | 1.4 | 0 | 20 |
| FLAT | 28 | 19.0 | 11 | 45 |

Two AGAINST picks and one FAVOUR pick have **zero** same-group non-published candidates on their
night (i.e. no stock in the entire non-published pool gapped the same way, direction-adjusted, that
night); a further 5 AGAINST and 4 FAVOUR picks have 1-2, still short of the 3-row PREREG floor.
FLAT's minimum (11) is well clear of the floor at every eligible pick, because the FLAT band (|g| <
1.0) is the densest part of the gap distribution.

### (c) Variant-B contributing nights per arm

A variant-B contributing night requires >= 1 eligible pick in that arm **with a valid B3 set (>= 3
controls)** and >= 1 eligible FLAT pick **with a valid B3 set**, same night. All 46 of R2's
FLAT-eligible nights clear the FLAT-side B3 floor (FLAT's minimum control count is 11), so the
reduction below is driven entirely by the arm side.

| Arm | Variant-B contributing nights | (for comparison: R2's exposure-only contributing nights) |
|---|---|---|
| AGAINST | 18 | 22 |
| FAVOUR | 15 | 20 |
| TOTAL (union) | 29 | 35 |

### (d) Monthly run-rate and projected date to 80 variant-B contributing nights

| Month | AGAINST | FAVOUR | TOTAL (union) |
|---|---|---|---|
| 2026-06 | 6 | 9 | 14 |
| 2026-07 | 11 | 3 | 11 |
| 2026-08 (partial -- matured only through 08-12) | 1 | 3 | 4 |

Projection method identical to R2: rate = contributing nights / elapsed trading sessions from the
first matured night (2026-06-01) to the last matured night (2026-08-12) inclusive = 51 sessions;
projected forward at that constant rate, sessions converted to calendar days at 365/252.

| Arm | n today | rate (per session) | sessions needed for 80 | projected date |
|---|---|---|---|---|
| AGAINST | 18 | 0.353 | 175.8 more | **2027-04-23** |
| FAVOUR | 15 | 0.294 | 220.9 more | **2027-06-28** |
| TOTAL (union) | 29 | 0.569 | 89.6 more | **2026-12-19** |

Both arm-specific variant-B projections (AGAINST, FAVOUR) fall **after** the current hard stop of
**2027-03-31** (DECISIONS.md item 10) -- AGAINST by about 3.5 weeks, FAVOUR by about 3 months. The
union projection does not. These are mechanical extrapolations of the June-August run-rate only, on
the same method R2 used; no reading of what this means for variant B vs. variant A is offered here
-- per the routed request, that waiting-vs-sample trade-off is R-3, back to Haci with these numbers
attached.

---

## Files (R5 addendum)

- This report: `research/reports/STEWARD_Q007_exposure.md` (§R5 appended 2026-09-13).
- No new data files were written; all counts were re-derived from `research/data/v001_sas_candidates.parquet`
  and `research/data/p001_daily_split.parquet` against `research/data/exclusions_v002.json`.
