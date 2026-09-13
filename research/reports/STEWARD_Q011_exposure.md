# Steward report: Q011 exposure-only fill count (R1)

Data Steward, 2026-09-13. Routed request R1, `research/questions/Q011_day1_dip_limit/PREREG.md`
Section 5 ("No measured exposure count exists for this question yet -- it is routed"). Frozen data
only: `research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`
(`v001_sas_candidates.parquet`, `p001_daily_split.parquet`, `p001_hourly_raw.parquet`) against
`research/data/exclusions_v003.json`. No live query. No `results/` directory was read.

Protocol observed (binding, per PREREG Section 5 and the routing request): counts only. Every
number below is computable from C_t, ATR14 (from p001_daily_split, never the platform's
atr_pct -- PI-003), the printed L3, and session t+1's open/high/low plus hourly bars. No bar
dated after session t+1 was read, no touch of any level after session t+1, no race outcome
(WIN/LOSS/NEITHER), no return, no P&L, and no picks-minus-control difference was computed. The
mechanical fill test (low_1 <= LIM_k / high_1 >= LIM_k) uses only the t+1 low/high -- this is
exposure, not outcome, per the PREREG's own framing (Sections 1, 4). Nothing below decides P1, P2,
or the k=0.5 demotion rule; those are eval.py's calls at the decision pass, on the frozen data,
per PREREG Sections 5/8.

---

## Population and method

Published picks (`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28) on non-excluded nights
(`exclusions_v003.json`: `manual_runs.trading_dates` union `non_session_runs.trading_dates` union
`uncorroborated_publication_runs.trading_dates` -- in-window this excludes **2026-06-26**,
**2026-07-02**, **2026-07-06**), pick night >= 2026-06-01, whose 20-session forward window has
matured against the SPY-implied trading calendar in `prices_daily_split` (153 sessions,
2026-02-02..2026-09-10; last matured pick night **2026-08-12**).

`dir` = +1 bullish / -1 bearish from `dominant_direction`. `C_t` = the pick's close on
`prices_daily_split` at t. `ATR` = ATR14 computed from `p001_daily_split` bars dated <= t (mean
true range over the 14 sessions ending at t, desk-standard construction,
`research/reports/explore/scripts/03_build_core.py:71-74` -- never the platform's `atr_pct`,
corrupted around splits per PI-003 / DATA_NOTES). `L3` = `public_payload_json.lane_plans
.swing_trading.targets[0]`. `d_close = dir x (L3 - C_t) / ATR`, required > 0. `O_1`/`H_1`/`L_1`/`C_1`
= session t+1 official regular-session open/high/low/close from `prices_daily_split`.
`LIM_k = C_t - dir x k x ATR` for k in {0.25, 0.5}. Fill (mechanical, PREREG Section 2): bullish
`FILLED_k = 1` iff `low_1 <= LIM_k`; bearish iff `high_1 >= LIM_k`. Fill-at-open: bullish
`O_1 <= LIM_k`; bearish `O_1 >= LIM_k`. Not-takeable, Plan M (open arm): `dir x (L3 - O_1) <= 0`.

This reproduces Q009's and Q007's matured-population base exactly at the pre-filter stage (383
published rows / 48 matured nights, last matured night 2026-08-12), confirming the
calendar/maturity/exclusion logic is consistent across questions. Q011's funnel then diverges from
Q009's (which filters on a printed stop; Q011 needs no stop at all -- the level tested is L3, the
swing lane's first target, and the entry is either the next-open or the resting limit, never the
printed lane entry price).

---

## 1. Population funnel

| Stage | Removed | Remaining |
|---|---|---|
| Published, in-window, non-excluded, matured (20-session) | -- | 383 |
| No lane-plan ladder at all (no `swing_trading` in payload) | 8 | 375 |
| Swing lane present but no L3 (`targets[0]` null/empty) | 0 | 375 |
| `outcome_target_invalid` non-null | 4 | 371 |
| Non-bullish/bearish `dominant_direction` | 0 | 371 |
| No `C_t` (no bar at t) | 0 | 371 |
| Symbol with fewer than 60 daily bars dated <= t (ATR undefined) | 0 | 371 |
| Wrong-side L3 (`d_close <= 0`) | 2 | 369 |
| No session t+1 bar / missing forward bar | 0 | 369 |
| **ELIGIBLE (all filters passed)** | -- | **369** |

**Matured nights: 48. Contributing nights (>= 1 eligible pick, PREREG Section 2 shared definition
for all four primaries): 47.** The one matured night that drops to zero eligible picks is
**2026-06-02** -- all 8 published rows that night carry no `swing_trading` lane at all (see
caveats, Section 4); this is the entirety of the "no lane-plan ladder" removal (8 of 8 on one
night, not spread across the window).

**The 4 `outcome_target_invalid` removals** are 2026-06-01 MSFT, 2026-06-03 AVGO/CRWD, 2026-06-04
AMAT -- the same 4 rows the E9a correction batch touched inside this window (identified in
`STEWARD_Q009_exposure.md` R1). **The 2 wrong-side-L3 removals** are 2026-06-05 LLY (bullish,
`d_close = -0.25`) and 2026-07-28 APH (bearish, `d_close = -17.7`).

**No null-ladder-but-has-L3 case exists** (the "swing lane present but no L3" row is 0) -- same
finding as Q009's null-stop headline: once a lane plan exists at all, its L3 is always populated.

---

## 2. Per-arm, per-k exposure counts (369 eligible picks, 47 contributing nights)

### (a) Totals

| | Plan M (open) | Plan L(0.25) | Plan L(0.5) |
|---|---|---|---|
| Not takeable | **9** (2.4%) | 0 (impossible by construction -- Section 2; verified) | 0 (impossible by construction -- Section 2; verified) |
| Filled | n/a | **232** (62.9%) | **157** (42.5%) |
| Not filled | n/a | **137** (37.1%) | **212** (57.5%) |
| -- of filled, at the open (gap through `LIM_k`) | n/a | 89 (38.4% of filled) | 43 (27.4% of filled) |
| -- of filled, intraday | n/a | 143 (61.6% of filled) | 114 (72.6% of filled) |

`232 + 137 = 369` and `157 + 212 = 369` -- every eligible pick is classified in both k arms (ITT,
PREREG Sections 1/4: no pick is dropped for a non-fill). Plan L(k)'s not-takeable count is verified
0 for both k, confirming the PREREG Section 2 construction argument (L3 lies beyond `C_t` in the
trade direction by the `d_close > 0` eligibility filter; `FILL_k` lies on the opposite side of
`C_t` from L3 by construction, so a filled limit pick is always takeable).

### (b) Contributing nights carrying >= 1 fill, per k (the Section 5 demotion-rule input)

| k | Contributing nights with >= 1 fill | of 47 |
|---|---|---|
| 0.25 | **46** | 97.9% |
| 0.5 | **44** | 93.6% |

Both clear the PREREG Section 5 demotion floor (fewer than 20 nights with >= 1 fill at k=0.5
demotes P1-B/P2-B to descriptive) by a wide margin as measured today. This is not a demotion
ruling -- that is `eval.py`'s call at the decision pass on the then-current frozen data -- but
nothing in the present count points toward it.

### (c) Hourly-bar coverage on session t+1 (ordering rule 2 input)

`p001_hourly_raw` covers exactly the 227 published-pick symbols in the freeze (per
`manifest_prices_v001.json`). **369 of 369 eligible picks (100.0%)** have >= 1 regular-session
(13:00-19:00 UTC, i.e. 09:00-15:00 ET during EDT -- the whole window is EDT, no DST boundary
inside it) hourly bar on session t+1. Every eligible pick can be resolved by ordering rule 2
without falling back to its conservative default reading.

### (d) Monthly breakdown

| Month | Contributing nights | Eligible picks | Filled @0.25 | Filled @0.5 |
|---|---|---|---|---|
| 2026-06 | 19 | 147 | 83 (56.5%) | 57 (38.8%) |
| 2026-07 | 20 | 158 | 106 (67.1%) | 76 (48.1%) |
| 2026-08 (partial -- matured only through 08-12) | 8 | 64 | 43 (67.2%) | 24 (37.5%) |
| **Total** | **47** | **369** | **232 (62.9%)** | **157 (42.5%)** |

### (e) Per-night detail (47 contributing nights)

| Night | Eligible | M not-takeable | Filled @0.25 | Not filled @0.25 | Filled @0.5 | Not filled @0.5 |
|---|---|---|---|---|---|---|
| 2026-06-01 | 7 | 1 | 3 | 4 | 2 | 5 |
| 2026-06-03 | 6 | 0 | 6 | 0 | 6 | 0 |
| 2026-06-04 | 7 | 0 | 6 | 1 | 6 | 1 |
| 2026-06-05 | 7 | 1 | 3 | 4 | 2 | 5 |
| 2026-06-08 | 8 | 0 | 6 | 2 | 3 | 5 |
| 2026-06-09 | 8 | 0 | 7 | 1 | 4 | 4 |
| 2026-06-10 | 8 | 0 | 3 | 5 | 3 | 5 |
| 2026-06-11 | 8 | 0 | 5 | 3 | 3 | 5 |
| 2026-06-12 | 8 | 2 | 1 | 7 | 1 | 7 |
| 2026-06-15 | 8 | 0 | 5 | 3 | 2 | 6 |
| 2026-06-16 | 8 | 1 | 4 | 4 | 1 | 7 |
| 2026-06-17 | 8 | 0 | 2 | 6 | 0 | 8 |
| 2026-06-18 | 8 | 3 | 0 | 8 | 0 | 8 |
| 2026-06-22 | 8 | 0 | 7 | 1 | 6 | 2 |
| 2026-06-23 | 8 | 0 | 6 | 2 | 4 | 4 |
| 2026-06-24 | 8 | 0 | 3 | 5 | 2 | 6 |
| 2026-06-25 | 8 | 0 | 5 | 3 | 5 | 3 |
| 2026-06-29 | 8 | 0 | 4 | 4 | 0 | 8 |
| 2026-06-30 | 8 | 0 | 7 | 1 | 7 | 1 |
| 2026-07-01 | 8 | 0 | 7 | 1 | 6 | 2 |
| 2026-07-07 | 8 | 0 | 8 | 0 | 8 | 0 |
| 2026-07-08 | 8 | 0 | 5 | 3 | 4 | 4 |
| 2026-07-09 | 8 | 0 | 4 | 4 | 3 | 5 |
| 2026-07-10 | 10 | 0 | 7 | 3 | 6 | 4 |
| 2026-07-13 | 8 | 1 | 6 | 2 | 4 | 4 |
| 2026-07-14 | 8 | 0 | 4 | 4 | 3 | 5 |
| 2026-07-15 | 8 | 0 | 4 | 4 | 2 | 6 |
| 2026-07-16 | 8 | 0 | 4 | 4 | 1 | 7 |
| 2026-07-17 | 8 | 0 | 8 | 0 | 3 | 5 |
| 2026-07-20 | 8 | 0 | 4 | 4 | 4 | 4 |
| 2026-07-21 | 9 | 0 | 7 | 2 | 3 | 6 |
| 2026-07-22 | 9 | 0 | 5 | 4 | 4 | 5 |
| 2026-07-23 | 8 | 0 | 5 | 3 | 3 | 5 |
| 2026-07-24 | 9 | 0 | 8 | 1 | 7 | 2 |
| 2026-07-27 | 8 | 0 | 3 | 5 | 2 | 6 |
| 2026-07-28 | 8 | 0 | 3 | 5 | 2 | 6 |
| 2026-07-29 | 8 | 0 | 7 | 1 | 6 | 2 |
| 2026-07-30 | 4 | 0 | 4 | 0 | 2 | 2 |
| 2026-07-31 | 5 | 0 | 3 | 2 | 3 | 2 |
| 2026-08-03 | 8 | 0 | 6 | 2 | 3 | 5 |
| 2026-08-04 | 8 | 0 | 4 | 4 | 4 | 4 |
| 2026-08-05 | 8 | 0 | 8 | 0 | 3 | 5 |
| 2026-08-06 | 8 | 0 | 6 | 2 | 3 | 5 |
| 2026-08-07 | 8 | 0 | 3 | 5 | 1 | 7 |
| 2026-08-10 | 8 | 0 | 5 | 3 | 3 | 5 |
| 2026-08-11 | 8 | 0 | 6 | 2 | 4 | 4 |
| 2026-08-12 | 8 | 0 | 5 | 3 | 3 | 5 |

Sums check: eligible column totals 369; `filled + not_filled` reconciles to `eligible` on every
row for both k.

---

## 3. Run-rate and floor-date projections

**Rate = 47 contributing nights / 51 sessions (2026-06-01..2026-08-12 inclusive, the elapsed
sessions from the first possible pick night through the last matured one) = 0.9216 contributing
nights per session** -- this is the same population/window Q009's R1 used (also 51 sessions, also
47 contributing nights under `exclusions_v003.json`), so the two questions' run-rates coincide in
this snapshot; that is a coincidence of the current freeze, not a structural link between the two
questions' populations.

All three projected dates below are **mechanical extrapolations of the June-August run-rate only**
-- they gate nothing and decide nothing; every gate in PREREG Section 8 is evaluated on `eval.py`'s
measured counts from the frozen data at the decision pass, never on this projection. Per the
routing request, each projected date is built in two steps: (i) the raw pick-night date -- the
calendar date on which the rate-implied Nth qualifying pick night occurs (sessions-to-calendar via
365/252, the same conversion `STEWARD_Q007_exposure.md`/`STEWARD_Q009_exposure.md` use); then (ii)
plus 20 trading sessions (that pick night's own 20-session maturity window, also converted at
365/252) plus 7 calendar days (freeze-build margin), rounded to the next Monday on or after -- the
same construction the PREREG's own Section 5 uses for its decision date. Step (i) alone is a "when
does the pick night happen" date; step (ii) is "when can a freeze actually confirm it as a
contributing night" -- the two are different questions, and only (ii) is a usable floor date.

### Floor 1 -- 80 contributing nights per primary endpoint (DP-21)

- Need 33 more contributing nights beyond the 47 measured; at 0.9216/session that is 35.8 more
  sessions.
- Raw pick-night date (the 80th qualifying pick night): **2026-10-02**.
- Plus 20-session maturity: 2026-10-30.
- Plus 1-week freeze margin, next Monday: **2026-11-09**.

### Floor 2 -- 20 contributing nights per stratum cell (regime label legal only from 2026-06-09; calendar halves)

**Already met, as measured, with no projection needed.**
- Regime-legal (trading_date >= 2026-06-09) contributing nights: **42 of 47** -- cleared 20 on
  **2026-07-13** (the date of the 20th such night). The 5 contributing nights 2026-06-01..06-08
  carry no legal regime label (FREEZE_v001 Section 7 / `exclusions_v003.json`
  `regime_label_point_in_time_from`) and are excluded from regime stratification, never dropped
  from the population.
- Calendar halves (median-split of the 47 contributing nights, `in_sample_end` marks only what is
  excluded): Half A (<= 2026-07-10, the median contributing-night date) = **24 nights**; Half B
  (> 2026-07-10) = **23 nights**. Both already clear 20 (20th Half-A night: 2026-07-01; 20th
  Half-B night: 2026-08-07). **Caveat:** the halves split point is the median of the final
  window's contributing nights, so it will shift later as more nights accrue; this is a snapshot
  on today's 47 matured nights, not a fixed partition -- it is reported because both sides already
  clear 20 nights on the data measured today, not because the partition is final.

### Floor 3 -- 30 contributing nights dated after the lock commit 2026-09-13 (DP-24)

- 0 measured today (the last matured pick night, 2026-08-12, predates the lock date; no pick night
  after 2026-09-13 has had time to mature yet).
- At 0.9216/session, 30 post-lock contributing nights need 32.6 sessions from 2026-09-13.
- Raw pick-night date (the 30th post-lock qualifying pick night): **2026-10-30** -- matching the
  PREREG Section 5 text's own "around 2026-10-30" figure (computed there from a roughly 2026-09-15
  lock date at the same roughly 0.92/session rate; this is the same raw pick-night date, not yet
  maturity-adjusted).
- Plus 20-session maturity: 2026-11-27.
- Plus 1-week freeze margin, next Monday: **2026-12-07**.

**Summary -- the three projected floor dates, maturity- and margin-adjusted:**

| Floor | Status | Projected date |
|---|---|---|
| 80 contributing nights (DP-21) | projected | **2026-11-09** |
| 20 per stratum cell (regime; calendar halves) | already met | 2026-07-13 (regime); 2026-08-07 (later half) |
| 30 contributing nights after lock 2026-09-13 (DP-24) | projected | **2026-12-07** |

Floor 3 (post-lock) remains the binding gate, as the PREREG itself states (Section 5: "This is the
binding gate, not the 80-night floor") -- its maturity-adjusted date (2026-12-07) is earlier than
the PREREG's own decision-date target of Monday 2026-12-14 (built from the primary window's last
pick night, 2026-11-06, not from this rate projection -- the two are independent constructions and
are not expected to coincide exactly; the PREREG's decision date carries margin for the whole
primary window, not just the 30th post-lock night).

---

## 4. Data caveats bearing on the fill definition

1. **No missing t+1 bars in this window.** All 371 candidates surviving the pre-t+1 filters had a
   complete session t+1 daily bar (`o`, `h`, `l`, `c` all present) -- the "no session t+1 bar"
   funnel step removed 0. No halt/delisting gap inside the matured window.
2. **Split-corrupted ATR (PI-003 / DATA_NOTES) does not appear to affect this population.** ATR
   was computed from `p001_daily_split` (split-adjusted), never the platform's `atr_pct` (which is
   computed on raw bars and is known corrupted around splits -- up to 10x true ATR% on BKNG,
   CVNA). Neither BKNG nor CVNA appears in the matured published set at all, and the eligible-pick
   ATR-as-percent-of-`C_t` distribution tops out at 14.9% (median 3.6%) -- no outlier consistent
   with an unadjusted-split artifact. PI-003 itself is still open (`HACI_DECIDED:fix`, not yet
   `IMPLEMENTED`/`VERIFIED`); this is a check on the current window's data, not a statement that
   the underlying platform bug is fixed.
3. **Picks without an L3.** 8 of 383 matured published picks (2.1%) carry no `swing_trading` lane
   at all and therefore no L3 -- but **all 8 fall on a single night, 2026-06-02** (ON, WDC, MU,
   SMCI, MPC, AMT, CAT, MSFT), not spread across the window. This is the only matured night that
   drops to zero eligible picks. No other matured night in the window has a no-ladder pick. This
   concentration is flagged for the registrar's and Red Team's attention -- it was not
   investigated further here (out of scope for a counts-only exposure report; no payload or
   run-log root-cause read was performed for this night, unlike the R3 rulings issued for
   2026-06-26 under Q009). Separately, 0 picks have a `swing_trading` lane present but a
   null/empty `targets[0]` -- once a lane exists at all, L3 is always populated, matching Q009's
   "null-stop denominator is 0" finding for the analogous stop field.
4. **Hourly-bar scope.** `p001_hourly_raw` is scoped to the 227 published-pick symbols only (not
   the full 436-symbol daily universe), so it fully covers this question's population (every
   eligible pick is, by construction, a published pick) but would not cover a B2 control-pool
   symbol without its own published history -- not a hazard for this exposure count (B2 is out of
   scope for R1), but relevant if a future R1-style request extends to B2 fill rates.

---

## Files

- This report: `research/reports/STEWARD_Q011_exposure.md`.
- No new data files were written; all counts were re-derived from
  `research/data/v001_sas_candidates.parquet`, `research/data/p001_daily_split.parquet` and
  `research/data/p001_hourly_raw.parquet` against `research/data/exclusions_v003.json`. No
  manifest, exclusions or state file was created or modified. The controller was not advanced.
