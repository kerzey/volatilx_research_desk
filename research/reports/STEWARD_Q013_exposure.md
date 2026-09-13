# Steward report: Q013 exposure and knowledge-time check (R1)

Data Steward, 2026-09-13. Routed request R1 (both parts, both blocking),
research/questions/Q013_earnings_proximity/DECISIONS.md section "Routed requests -> data-steward -> R1",
binding verbatim, cross-checked against draft PREREG.md Section 2 (population/arm/contributing-night
definitions) and Section 5 (floors, window, decision-date recipe). Frozen data only:
research/data/manifest_v001.json + research/data/manifest_prices_v001.json
(v001_sas_candidates.parquet, v001_sas_runs.parquet, p001_daily_split.parquet) against
research/data/exclusions_v003.json. No results/ directory was read; no parquet was written; no
manifest, exclusions or state file was created or modified; the controller was not advanced.

Protocol observed (binding): counts only. Session t+1 official open/high/low were read for the
passed_at_entry and control-set counts, exactly as licensed. For sessions >= 2 only the existence
of bars (maturity/coverage) was checked, never their values. No touch of any level, no return, no MAE,
no P&L, no picks-minus-control difference and no outcome of any kind was computed. Same discipline as
STEWARD_Q011_exposure.md / STEWARD_Q009_exposure.md Section R1.

The research-side read-only database credential was not present in this session environment
(checked; empty). Part (a) row-level timestamp pattern is therefore read from the frozen parquet
own created_at/updated_at columns, which are the same DB-sourced values a live query would return
for these historical, already-published rows (they predate the 2026-09-10 freeze and are not expected
to mutate further, modulo the known re-run nights already excluded below) -- this is disclosed, not
substituted silently. The platform repository was read read-only, at its checked-out HEAD fa70688b
(which matches the manifest pinned platform_git_sha exactly), via direct file reads and git log,
for the code citations below; nothing was executed there and nothing was written there.

---

## R1(a) -- knowledge-time verification on the arm-label columns

Claim under test (PREREG Section 5 / Section 10 threat 1): for sas_candidates rows with
trading_date >= 2026-06-01, are days_to_earnings_corrected / earnings_phase /
earnings_phase_subtag / earnings_event_risk_corrected live-path writes at scoring time
(services/super_agent_select_service.py:396-402, services/super_agent_select_scoring.py:1436-1444),
or could they be (or include) output from the Phase-0b backfill
(scripts/rescore_sas_earnings_corrected.py, source file data/sp500_earnings_2026-01-05_to_2026-05-30.json,
ending 2026-05-30)?

### (i) Code check (read-only, platform SHA fa70688b, matches manifest)

- services/super_agent_select_service.py:396-402 writes days_to_earnings_corrected,
  days_since_earnings_corrected, earnings_phase, earnings_event_risk_corrected from
  scorecard.days_to_earnings / .days_since_earnings / .earnings_phase / .earnings_event_risk --
  values produced inside the same scoring pass that writes every other subscore on the row, not
  read back from a separate table. earnings_phase_subtag is not assigned anywhere in this write
  block.
- services/super_agent_select_scoring.py:1436-1444 computes those scorecard fields from
  context.catalyst_context at scoring time (Phase 1B, NON-scoring earnings event-risk,
  computed once best_timeframe is known), matching the PREREG citation exactly.
- services/earnings_phase.py is the single shared classifier the module docstring says it is: both
  the Phase-0b backfill script and the live scorer import NO_WINDOW, classify_earnings_phase,
  compute_event_risk, neutral_subtag from this one module. Current phases are PRE_1_3,
  PRE_4_7, PRE_8_14, PRE_15_30, EARNINGS_DAY, POST_1_7, NO_WINDOW -- NO_WINDOW absorbs
  former POST_8_PLUS and NO_UPCOMING (module docstring), which now live only as the non-scoring
  neutral_subtag() output (FAR / POST_8_PLUS / NO_UPCOMING). neutral_subtag() is never called
  in the live write block above, which is exactly why earnings_phase_subtag is null on every sealed
  row (below) -- a code-confirmed non-population, not a knowledge-time hazard, since the PREREG uses
  the field descriptively only.
- The backfill script own docstring lists its output alphabet ending in NO_UPCOMING (the
  pre-refactor name); the live data never carries that value in earnings_phase (only in the null
  earnings_phase_subtag), additional evidence the sealed rows were not re-written by that script
  old code path.

### (ii) earnings_phase distribution by month, trading_date >= 2026-06-01 (row counts)

| month | EARNINGS_DAY | NO_WINDOW | POST_1_7 | PRE_1_3 | PRE_4_7 | PRE_8_14 | PRE_15_30 | rows | NO_WINDOW share |
|---|---|---|---|---|---|---|---|---|---|
| 2026-06 | 5 | 882 | 17 | 7 | 11 | 12 | 127 | 1061 | 83.1% |
| 2026-07 | 40 | 265 | 151 | 77 | 132 | 271 | 439 | 1375 | 19.3% |
| 2026-08 | 25 | 941 | 220 | 31 | 27 | 27 | 59 | 1330 | 70.8% |
| 2026-09 (partial, through 09-10) | 5 | 375 | 24 | 6 | 3 | 1 | 15 | 429 | 87.4% |

The NO_WINDOW share swings 83% to 19% to 71% to 87% across four months -- a live earnings calendar
producing a real seasonal cluster (a July-heavy reporting burst), not a static or collapsing signal.
A re-run of the Phase-0b backfill across this window would write NO_UPCOMING/null uniformly and
would not reproduce this swing.

### (iii) Non-null days_to_earnings_corrected share by month

| month | non-null share |
|---|---|
| 2026-06 | 100.0% |
| 2026-07 | 99.93% |
| 2026-08 | 99.47% |
| 2026-09 (partial) | 98.37% |

Coverage stays at 98-100% throughout the sealed window (only a handful of individual-row nulls, no
monthly collapse). This is the opposite of what a re-run of a backfill whose source file ends
2026-05-30 would produce over this period (it would write null/NO_UPCOMING across the board).
days_since_earnings_corrected is 100% non-null in every month.

### (iv) Row-level created_at / updated_at pattern (4195 sealed rows, trading_date >= 2026-06-01)

- 97.07% of rows have created_at on the same UTC calendar date as trading_date. The only
  two exceptions are 2026-07-02 (created_at 2026-07-03 14:58:20 UTC) and 2026-07-06
  (created_at 2026-07-07 20:57:48 UTC) -- these are exactly the two known manual re-run nights
  already carried in exclusions_v003.json manual_runs.trading_dates (KT_AUDIT finding,
  independently corroborated here, not a new hazard).
- created_at hour-of-day (UTC) for the sealed window: 20:00-20:59 (557 rows), 21:00-21:59 (3532
  rows), 22:00-22:59 (45 rows), 14:00-14:59 (61 rows). The 20-22 UTC cluster (98.5% of rows) is
  16:00-18:00 ET during EDT (in effect for the whole window) -- consistent with the declared 16:05 ET
  write. The 14:00 UTC cluster (61 rows, 10am EDT) is entirely 2026-07-02 -- the same already-known
  re-run night, not a new pattern.
- updated_at exceeds created_at by more than one hour on 741 of 4195 rows (17.7%), spread thinly
  across nearly every night in the window (single-digit-to-teens row counts per night) rather than
  concentrated on the earnings columns write nights -- consistent with later mutation of other
  columns on the same row (e.g. outcome/ladder-hit backfills, which touch updated_at table-wide) and
  not with a rescore of the earnings columns specifically. No sealed-window row shows an updated_at
  pattern isolated to the earnings columns.

### (v) PASS / FAIL

PASS. The sealed-window (trading_date >= 2026-06-01) days_to_earnings_corrected,
earnings_phase and earnings_event_risk_corrected values are live-path writes at scoring time: the
code path matches the PREREG citation exactly, the monthly phase mix shows real seasonal earnings
clustering rather than a flat backfill signature, non-null coverage stays at 98-100% throughout (a
backfill re-run over this window would instead show null/NO_UPCOMING), and row timestamps cluster at
the declared 16:05 ET write with the only two exceptions being nights already flagged and excluded as
manual re-runs. earnings_phase_subtag is 100% null in the sealed window -- code-confirmed as simply
never populated by the live write block, not a knowledge-time defect, and the PREREG uses it
descriptively only, never for arm assignment. No rule-14 exception is needed; DP-41 DEFERRED branch
does not fire.

---

## R1(b) -- exposure, counts only

### Window and population

Pick nights 2026-06-01 through the last night with a matured 20-session forward window against
the SPY-implied trading calendar in p001_daily_split (153 sessions, 2026-02-02 through 2026-09-10;
last matured pick night 2026-08-12), non-excluded per exclusions_v003.json
(manual_runs union non_session_runs union uncorroborated_publication_runs, which in-window
removes 2026-06-26, 2026-07-02, 2026-07-06), published rows under DP-28
(qualified IS TRUE AND selected_rank IS NOT NULL), with a
public_payload_json.lane_plans.swing_trading.targets[0] present.

sas_runs carries 51 nights in the raw window; 48 nights remain after the three exclusion
dates. This reproduces STEWARD_Q011_exposure.md and STEWARD_Q009_exposure.md matured
population base exactly (383 published rows / 48 matured nights / last matured night 2026-08-12,
same 8 no-ladder / 4 outcome_target_invalid / 0 mixed-direction / 0 missing-bar removals), confirming
the calendar, maturity and exclusion machinery is consistent across all three questions Steward
reports.

### 1. Population funnel

| Stage | Removed | Remaining |
|---|---|---|
| Published, in-window, non-excluded, matured (20-session) | -- | 383 |
| No swing-lane ladder at all (no L3) | 8 | 375 |
| outcome_target_invalid non-null | 4 | 371 |
| Mixed-direction dominant_direction | 0 | 371 |
| Missing C_t, missing O_1, or fewer than 14 prior ATR bars | 0 | 371 |
| Immature (fewer than 20 forward sessions with any bar) | 0 | 371 |
| ELIGIBLE (all filters passed) | -- | 371 |

One matured night (2026-06-02) drops to zero eligible published picks -- all 8 published rows
that night carry no swing_trading lane at all, the same night and the same root cause
STEWARD_Q011_exposure.md Section 1 flags.

### 2. Arm split (371 eligible picks)

k_p = trading sessions from t to the first session on/after trading_date + days_to_earnings_corrected
calendar days, on the SPY calendar (p001_daily_split).

| Arm | Definition | Eligible picks | Contributing-night status |
|---|---|---|---|
| A | 0 to 3 sessions to report | 44 | primary |
| B | 4 to 20 sessions to report | 137 | primary (baseline) |
| C | more than 20 sessions, or dtn null / unresolvable | 190 | descriptive only (B4) |

days_to_earnings_corrected is non-null on all 371 eligible rows (consistent with R1(a)(iii)); no row
fell into Arm C for the null/unresolvable reason inside this window -- every Arm-C row has a
computable, finite or beyond-freeze-horizon k greater than 20.

Per-k cells inside Arm A, and 4-way bands inside Arm B (picks / distinct contributing-eligible
nights carrying that cell):

| Cell | Picks | Distinct nights |
|---|---|---|
| A, k=0 | 14 | 11 |
| A, k=1 | 12 | 10 |
| A, k=2 | 8 | 8 |
| A, k=3 | 10 | 8 |
| B, k=4-7 | 42 | 23 |
| B, k=8-13 | 49 | 20 |
| B, k=14-20 | 46 | 27 |

All three Arm-B bands already clear the 20-contributing-night SUPPRESSION floor inside the sealed
window alone; all four Arm-A cells (8-11 nights) do not yet.

### 3. Contributing nights (PREREG Section 2 definition)

A contributing night requires at least 1 eligible Arm-A pick and at least 1 eligible Arm-B pick, each
with at least 3 valid B2 matched controls.

- B2 control-set size: every night in the window has an eligible control pool (per-night eligible
  count: min 37, median 54, max 60 -- eligibility requires at least 60 prior bars for beta60, at
  least 21 for runup20, a t+1 open, and full 20-forward-session bar coverage). Every one of the 181
  Arm-A/B eligible picks matched its full 10 nearest controls (min = max = 10 across both arms); 0 of
  181 (0.0%) fall below the 3-control floor. The B2 gate never binds in this window.
- Contributing nights: 23 of 48 matured, non-excluded window nights.
- B3 (arm-matched, descriptive) pool is materially thinner, as PREREG Section 3 and Section 10
  threat 14 anticipate: available same-arm control rows per pick average 8.2 (Arm A) and 26.9
  (Arm B), and 24 of 181 picks (13.3%) would carry fewer than 3 valid controls under B3 (Arm A: 12
  of 44, 27.3%; Arm B: 12 of 137, 8.8%) -- confirming B3 could not itself carry the primaries floor.

### 4. Contributing nights per month (the seasonal-clustering figure the routing request asks for)

| Month | Window nights | Contributing nights | Rate/session | Arm-A picks | Arm-B picks | Arm-C picks |
|---|---|---|---|---|---|---|
| 2026-06 | 20 | 2 | 10.0% | 3 | 20 | 125 |
| 2026-07 | 20 | 14 | 70.0% | 30 | 101 | 28 |
| 2026-08 (partial, through 08-12) | 8 | 7 | 87.5% | 11 | 16 | 37 |
| Total | 48 | 23 | 47.9% | 44 | 137 | 190 |

The monthly rate swings 10% to 87.5% -- June is a trough, July is the peak of a Q2-earnings
reporting burst, and August (partial) is still inside it. This is the seasonal clustering the PREREG
own Section 5 names (S&P reporting comes in roughly six-week bursts each quarter); any single blended
rate below averages it away and is presented with that caveat.

### 5. Composition counts (per arm, counts only, no outcome)

|  | Arm A (n=44) | Arm B (n=137) |
|---|---|---|
| Bearish share | 2 (4.5%) | 4 (2.9%) |
| passed_at_entry count (share) | 2 (4.5%) | 1 (0.7%) |

Bear-share gap A minus B = 1.6 pp (PREREG Section 10 threat 2 mandatory-diagnostic trigger is
20 pp -- not tripped). passed_at_entry-share gap A minus B = 3.8 pp (Section 10 threat 3 trigger
is 10 pp -- not tripped). Both are printed as counts only; neither is interpreted here.

### 6. Run-rate and floor-date projections (mechanical extrapolation only; decides nothing)

Rate = 23 contributing nights divided by 51 elapsed sessions (2026-06-01 through 2026-08-12
inclusive) = 0.4510 contributing nights per session, blended across one trough month and 1.5 peak
months. Projected dates below follow the same two-step construction STEWARD_Q011_exposure.md and
STEWARD_Q009_exposure.md use: first, the raw pick-night date the rate implies (sessions-to-calendar
at 365 over 252), then plus 20 trading sessions own maturity (also 365/252-converted) plus a 7-day
freeze-build margin, rounded up to the next Monday. Every gate is still evaluated on eval.py measured
counts at the decision pass, never on this projection (PREREG Section 8).

| Floor | Measured | Rate basis | Projected date (maturity and margin adjusted) |
|---|---|---|---|
| 80 contributing nights total (DP-21) | 23 | 0.4510/session, blended | 2027-03-22 |
| 30 contributing nights after lock commit (DP-24), lock approx 2026-09-13 | 0 (none post-lock yet) | 0.4510/session, blended | 2027-01-25 |
| Arm-A per-k cells to 20 nights (k=0/1/2/3) | 11 / 10 / 8 / 8 | own per-cell rate | 2026-11-16 / 2026-11-30 / 2027-01-11 / 2027-01-11 |
| Arm-B bands to 20 nights (4-7 / 8-13 / 14-20) | 23 / 20 / 27 | -- | already met |

The 80-contributing-night floor is the binding gate at the blended rate: its projected date
(2027-03-22) is later than both the 30-post-lock floor projected date (2027-01-25) and the PREREG
drafted floor of Monday 2027-03-01 (DP-43: a projection pushes the decision date out, never pulls it
in). All projected dates fall well inside the 12-month ceiling of 2027-09-13 -- on this measured
rate, R1(b) does not trigger the DP-43 DEFERRED branch; 80 contributing nights and 30 post-lock
contributing nights both project to be reachable before the ceiling.

Seasonal caveat (load-bearing, not decorative): the blended rate mixes a 10%/session trough month
with two months at 70-88%/session. At the pure July-August rate (21 contributing divided by 28
sessions = 75.0%/session) the 80-night floor would project to roughly 2026-12-14 (maturity and
margin adjusted) instead of 2027-03-22 -- earlier than the drafted 2027-03-01 floor, which would then
bind instead of the rate. At a rate no better than the June trough (10%/session) sustained
indefinitely, the 80-night floor would not project inside the 12-month ceiling at all. The true date
depends on where the Q3 and Q4 2026 earnings seasons fall relative to the remaining window, which
this counts-only report does not forecast. The blended 0.4510/session figure is reported as the
single mechanical number the routing request asks for; the range above is reported so the seasonal
clustering is visible rather than averaged away, per the request own instruction.

---

## Files

- This report: research/reports/STEWARD_Q013_exposure.md.
- No new data files were written; all counts were re-derived from
  research/data/v001_sas_candidates.parquet, research/data/v001_sas_runs.parquet and
  research/data/p001_daily_split.parquet against research/data/exclusions_v003.json. No manifest,
  exclusions or state file was created or modified. The controller was not advanced -- lock is the
  registrar apply-Q013 step per DECISIONS.md, not this report.
