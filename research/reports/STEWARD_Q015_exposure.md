# Steward report: Q015 band-composition exposure count (R1)

Data Steward, 2026-09-13. Routed request R1, research/questions/Q015_band_85_90_updown/DECISIONS.md
"Routed requests -> data-steward -> R1" (blocking for lock). Frozen data only:
research/data/manifest_v001.json + research/data/manifest_prices_v001.json
(v001_sas_candidates.parquet, p001_daily_split.parquet, p001_hourly_raw.parquet) against
research/data/exclusions_v003.json. No live query. No results/ directory exists and none was
read; no parquet or state file was created or modified.

Protocol observed (binding). Counts only. For sessions t+1..t+20 only the existence of a
daily/hourly bar was checked (maturity and coverage); no bar value in t+1..t+20 was read. C_t,
ATR14 and bars dated <= t were read only for eligibility, distances and same-night control-pool
sizing. No touch of any level, no UPDOWN, no revisit, no return, no plan result, no band
difference and no outcome of any kind was computed. This is the same discipline as
STEWARD_Q011_exposure.md and STEWARD_Q009_exposure.md R1.

Definitions used, exactly as routed. C_t = pick-night regular-session close from
prices_daily_split (never spot_close); ATR14 = mean true range over the 14 sessions ending at
t from prices_daily_split bars <= t (never the platform atr_pct column, PI-003); dir = +1
bullish / -1 bearish from dominant_direction; L3 = lane_plans.swing_trading.targets[0];
S = lane_plans.swing_trading.stop; d_L3 = dir x (L3-C_t)/ATR; d_S = dir x (C_t-S)/ATR.
Bands on published overall_score, half-open, no rounding: A=[85,90), B=[80,85), E=[90,inf),
U=(-inf,80).

Population before the funnel. Published picks (qualified IS TRUE AND selected_rank IS NOT
NULL, DP-28), pick night >= 2026-06-01, non-excluded per exclusions_v003.json
(manual_runs union non_session_runs union uncorroborated_publication_runs -- in-window this
removes 11 rows on 2026-06-26, 9 on 2026-07-02, 9 on 2026-07-06), whose 20-session forward window
has matured against the SPY-implied trading calendar in prices_daily_split (153 sessions,
2026-02-02..2026-09-10). 383 published picks / 48 matured nights, last matured pick night
2026-08-12 -- this reproduces the matured-population base already measured for Q009 and Q011
exactly (same 383/48/2026-08-12), confirming the calendar/maturity/exclusion logic is consistent
across questions. A further 167 published rows / 20 nights in-window are immature (not yet 20
sessions old as of the freeze) and are printed here, never excluded. Pre-funnel band split of the
383 matured rows: A=53, B=311, E=18, U=1.

---

## (1) The funnel, in order, by band

| Step | Removed (A / B / E / U) | Removed (total) | Remaining |
|---|---|---|---|
| Published, in-window, non-excluded, matured (20-session) | -- | -- | 383 |
| No lane plan at all / no swing lane | 4 / 3 / 1 / 0 | 8 | 375 |
| Swing lane present but no targets[0] (L3) | 0 / 0 / 0 / 0 | 0 | 375 |
| L3 present but no stop (S) | 0 / 0 / 0 / 0 | 0 | 375 |
| outcome_target_invalid non-null | 1 / 3 / 0 / 0 | 4 | 371 |
| Wrong-side L3 (d_L3 <= 0) | 1 / 1 / 0 / 0 | 2 | 369 |
| Wrong-side stop (d_S <= 0) | 9 / 55 / 2 / 0 | 66 | 303 |
| Missing C_t or < 60 daily bars <= t | 0 / 0 / 0 / 0 | 0 | 303 |
| Missing forward bar(s) in t+1..t+20 (ungradeable) | 0 / 0 / 0 / 0 | 0 | 303 |
| ELIGIBLE | 38 / 249 / 15 / 1 | -- | 303 |

303 eligible picks -- this matches the STEWARD_Q009_exposure.md v003-addendum eligible count
(303) exactly, even though the two questions filter order differs (Q009 filters on the stop
first; Q015 uses the funnel order R1 specifies) -- the AND-combination of filters lands on the same
population, a second cross-question consistency check. The 8 no-lane-plan removals are, as PREREG
Section 2 states, all on the single night 2026-06-02 (ON/A, WDC/A, MU/E, SMCI/A, MPC/B, AMT/A,
CAT/B, MSFT/B) -- this is the entire "no swing lane" removal and the reason 2026-06-02 is the one
matured night with zero eligible picks in any band (below). No "swing lane present but no L3" and
no "L3 but no stop" case exists anywhere in the window, matching the null-ladder/null-stop findings
already measured for Q009 and Q011 on the analogous fields.

---

## (2) Eligible picks and contributing nights, by band

| Band | Eligible picks | Nights with >= 1 eligible pick (of 48 matured) |
|---|---|---|
| A = [85,90) | 38 | 21 |
| B = [80,85) | 249 | 47 |
| E = [90,inf) | 15 | 14 |
| U = (-inf,80) | 1 | 1 |

Band E (14 nights) and band U (1 night) are both below the 20-contributing-night SUPPRESSION
floor (DECISIONS.md items 1, 15, 16) -- SUPPRESSED, counts only, per (4) below.

---

## (3) Paired nights (P1/P2) and band-A nights (P3)

Every one of band A 21 eligible-carrying nights is also a band-B eligible-carrying night
(nights_A is a strict subset of nights_B in this window) -- so the P1/P2 paired definition and the
P3 band-A-only definition collapse to the same 21 nights here, the same pattern already measured
for Q009, whose three definitions collapsed to one count in its window.

| Definition | Contributing nights (of 48 matured) |
|---|---|
| P1/P2 -- paired (>= 1 eligible A and >= 1 eligible B, same night) | 21 |
| P3 -- band-A-only (>= 1 eligible A) | 21 |

Of the 48 matured nights: 21 are paired-contributing, 26 carry band B only (no eligible A
pick that night -- non-contributing for P1/P2, printed, never added to any exclusions file), 1
(2026-06-02) carries zero eligible picks in any band (non-contributing, not an exclusion), and
0 nights carry band A with no band B. 21+26+1 = 48.

---

## (4) Band-E and band-U contributing nights

| Band | Contributing nights | vs. 20-night SUPPRESSION floor |
|---|---|---|
| E = [90,inf) | 14 | below floor -- SUPPRESSED |
| U = (-inf,80) | 1 | below floor -- SUPPRESSED |

Both descriptive arms print as counts only at the decision pass; neither can produce a verdict
(DECISIONS.md item 1; PREREG Section 3 B1-prime). Band U is the single pre-publication-floor
row that survives the eligibility funnel (2026-06-02 MPC); no band-U row appears after 2026-06-02
in this window, consistent with publication_floor = 80.0 (2026-07-07) having already closed this
baseline by the time it took effect, and with the near-zero pre-existing supply the PREREG cites.

---

## (5) The 85-88 / 88-90 split of band A

| Sub-band | Eligible picks | Nights with >= 1 eligible pick |
|---|---|---|
| 85-88 | 26 | 18 |
| 88-90 | 12 | 9 |

Both sub-bands are below the 20-contributing-night floor as measured today; both would print
SUPPRESSED if reported at the decision pass on today counts (subject to eval.py own measured
counts at that time, per DECISIONS.md item 16 -- not decided here).

---

## (6) Null-ladder / null-stop / wrong-side counts by band, standalone

| Band | No swing lane | Swing but no L3 | L3 but no stop | outcome_target_invalid | Wrong-side L3 | Wrong-side stop |
|---|---|---|---|---|---|---|
| A | 4 | 0 | 0 | 1 | 1 | 9 |
| B | 3 | 0 | 0 | 3 | 1 | 55 |
| E | 1 | 0 | 0 | 0 | 0 | 2 |
| U | 0 | 0 | 0 | 0 | 0 | 0 |
| Total | 8 | 0 | 0 | 4 | 2 | 66 |

Wrong-side stop is the binding exclusion in every band, as already measured for Q009 and Q011
(the stop is anchored to the lane entry, which can stray from C_t -- PREREG Section 10 threat 3).

---

## (7) Hourly-bar coverage, sessions t+1..t+20, published pick symbols

p001_hourly_raw is scoped to the 227 published-pick symbols in the freeze (per
manifest_prices_v001.json).

| Scope | Symbol-sessions with >= 1 hourly bar |
|---|---|
| Overall (all 303 eligible picks x 20 forward sessions) | 6,060 / 6,060 = 100.0% |
| Band A | 760 / 760 = 100.0% |
| Band B | 4,980 / 4,980 = 100.0% |
| Band E | 300 / 300 = 100.0% |
| Band U | 20 / 20 = 100.0% |
| By month: 2026-06 | 2,380 / 2,380 = 100.0% |
| By month: 2026-07 | 2,680 / 2,680 = 100.0% |
| By month: 2026-08 | 1,000 / 1,000 = 100.0% |
| Session t+1 only (all 303 eligible picks) | 303 / 303 = 100.0% |

No fallback to DP-27 conservative default is forced by missing hourly bars anywhere in this
population -- every eligible pick t+1..t+20 window can, as far as bar existence goes, be
ordered from prices_hourly_raw.

B2 pool (unpublished candidates). prices_hourly_raw covers 227 of 428 distinct symbols that
ever appear as a non-published sas_candidates row across the whole manifest (54.3%) -- but that
227 is exactly the published-symbol set (222 of the 227 hourly-covered symbols are also
non-published on some other night; the remaining 5 hourly-covered symbols are published on
every night they appear as candidates at all). 206 of 428 non-published-row symbols (48.1%) have
zero hourly bars anywhere in the freeze. A B2 control drawn from one of those 206 symbols cannot
be ordered by hourly bars at all and falls to the DP-27 counter-first reading by construction,
not by a thin sample -- flagged per the R1 request, decided nowhere here.

---

## (8) B2 control-set size distribution

Per-night non-published sas_candidates pool (complement of the DP-28 predicate: qualified-false
and dark-lane rows alike), restricted to symbols with >= 60 daily bars <= t (the same floor applied
to published picks, needed for beta60/atr_pct/runup20 to be computable) -- measured on the
47 nights that carry >= 1 eligible pick in any band:

| | Value |
|---|---|
| Median pool size | 54 |
| 10th percentile pool size | 42 |
| Minimum pool size (any contributing night) | 37 |
| Maximum pool size | 60 |

| Band | Eligible picks | Share with < 3 valid same-night controls | Share with < 10 valid same-night controls |
|---|---|---|---|
| A | 38 | 0.0% | 0.0% |
| B | 249 | 0.0% | 0.0% |
| E | 15 | 0.0% | 0.0% |
| U | 1 | 0.0% | 0.0% |
| Overall | 303 | 0.0% | 0.0% |

The nearest-10 pool never binds in this window -- every contributing night non-published
pool is far above the 10-row floor (minimum measured: 37). This matches the equivalent B1-valid
control-pool finding already measured for Q009.

---

## (9) Contributing nights per month and per-session rate, both definitions

Since P1/P2 (paired) and P3 (band-A) collapse to the identical 21-night set here, one table serves
both.

| Month | Elapsed sessions | Contributing nights (paired = band-A) | Eligible picks: A / B / E / U |
|---|---|---|---|
| 2026-06 | 21 | 10 | 25 / 82 / 11 / 1 |
| 2026-07 | 22 | 9 | 11 / 119 / 4 / 0 |
| 2026-08 (partial -- matured only through 08-12) | 8 | 2 | 2 / 48 / 0 / 0 |
| Total | 51 | 21 | 38 / 249 / 15 / 1 |

The rate is declining month over month, not flat: 10/21 = 0.476/session in June, 9/22 =
0.409/session in July, 2/8 = 0.250/session in August (partial). Band-E contributing nights show
the same shrinkage the PREREG already names (10 in June, 4 in July, 0 in the matured part of
August). This is a measured seasonal pattern, printed per the R1 request so it is visible rather
than averaged away; no reading of what it means for the family or for H-060 mechanism is offered
here.

---

## Run-rate and floor-date projections

Overall flat rate = 21 contributing nights / 51 elapsed sessions (2026-06-01..2026-08-12
inclusive) = 0.4118 paired-contributing nights per session. Because the rate is visibly
declining (above), two more conservative rates are also projected, using the same mechanical
method STEWARD_Q007/Q009/Q011_exposure.md use: sessions-to-calendar-days at 365/252, then +20
sessions own maturity (365/252) +7 calendar days freeze margin, rounded to the next Monday on or
after. All dates below are mechanical extrapolations of a measured rate; they gate nothing and
decide nothing -- every PREREG Section 8 gate is evaluated on eval.py measured counts at the
decision pass, never on this projection (DECISIONS.md item 4; PREREG Section 5).

### Floor 1 -- 80 contributing nights per primary endpoint (DP-21; binds both P1/P2 and P3 identically here)

Need 59 more contributing nights beyond the 21 measured.

| Rate used | Sessions needed | Raw 80th-night date | +20-session maturity | +1-week margin, next Monday |
|---|---|---|---|---|
| Flat overall (0.4118/session) | 143.3 | 2027-03-08 | 2027-04-06 | 2027-04-19 |
| Jul+Aug only (0.3667/session) | 160.9 | 2027-04-02 | 2027-05-01 | 2027-05-10 |
| Aug only, partial month (0.2500/session) | 236.0 | 2027-07-20 | 2027-08-18 | 2027-08-30 |

### Floor 3 -- 30 contributing nights dated after the lock commit (DP-24), projected from 2026-09-13

| Rate used | Sessions needed | Raw 30th-post-lock-night date | +20-session maturity | +1-week margin, next Monday |
|---|---|---|---|---|
| Flat overall (0.4118/session) | 72.9 | 2026-12-28 | 2027-01-26 | 2027-02-08 |
| Jul+Aug only (0.3667/session) | 81.8 | 2027-01-10 | 2027-02-08 | 2027-02-15 |
| Aug only, partial month (0.2500/session) | 120.0 | 2027-03-06 | 2027-04-04 | 2027-04-12 |

Floor 1 (the 80-night total) is the binding gate under every rate tested -- its projected date
is later than Floor 3 under all three rates, so by the time Floor 1 clears, Floor 3 has already
cleared with margin (e.g. at the flat rate, 2027-04-19 for Floor 1 versus 2027-02-08 for Floor 3).

### Whether the 12-month ceiling (2027-09-13) is cleared

| Rate used | Floor-1 projected date | vs. ceiling 2027-09-13 |
|---|---|---|
| Flat overall | 2027-04-19 | clears by about 5 months |
| Jul+Aug | 2027-05-10 | clears by about 4 months |
| Aug only (partial, most pessimistic) | 2027-08-30 | clears by only about 2 weeks |

Yes -- 80 paired contributing nights (P1/P2) and 80 band-A contributing nights (P3), each with
>= 30 dated after the lock commit, are projected to be reachable by 2027-09-13 under all three
rates measured, including the most pessimistic (the partial-August-only rate). The margin under
that pessimistic rate is thin (about two weeks), and the rate is measured to be declining
month-over-month, not flat, so a further slowdown in band-A/band-B pairing beyond what
August (partial) already shows would be the scenario to watch. This is a measured-rate report, not
a recommendation; the registrar DP-43 ceiling test and the conditional
research/questions/DEFERRED.md branch apply per DECISIONS.md "Routed requests -> registrar
(conditional)" note, not here.

All three rate scenarios project Floor 1 date later than the PREREG drafted floor decision
date (Monday 2027-01-18) -- R1 pushes the date out, never in, per DP-43/DP-45, exactly as the
PREREG anticipates.

---

## Files

- This report: research/reports/STEWARD_Q015_exposure.md.
- No new data files were written; all counts were re-derived from
  research/data/v001_sas_candidates.parquet, research/data/p001_daily_split.parquet and
  research/data/p001_hourly_raw.parquet against research/data/exclusions_v003.json. No
  manifest, exclusions or state file was created or modified. The controller was not advanced;
  Q015 remains PREREG_DRAFT pending @registrar apply Q015.
