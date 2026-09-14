# STEWARD_Q019_exposure - R1 (counts only), Q019 conviction_monitor_exit

Request: DECISIONS.md data-steward R1 (counts only) BLOCKING FOR LOCK section (Q019_conviction_monitor_exit/DECISIONS.md lines 156-222), amended by Corrections 1-3.
Data: research/data/manifest_v001.json (table key conviction_monitor, sha256 68752794...9c7c, 3339 rows) plus research/data/manifest_prices_v001.json (base_manifest_sha256 b03f355a...bef374) plus research/data/v001_sas_candidates.parquet, v001_sas_runs.parquet, p001_daily_split.parquet. No live query was made (DP-50(c)). Platform history read read-only from the platform repo (git log/show, DP-50(a)/(b)).
No outcome of any kind is reported below - no touch, no plus-or-minus-1-ATR race, no return, no plan result, no avoided move, no tier-vs-outcome cross-tab. Bars dated after session s were read only to confirm existence (maturity/gradeability), never a value.
Method note (temporary, counts-only tool, not the locked eval.py): ATR14 equals a simple 14-bar mean of True Range on prices_daily_split, bars dated on or before t. The trading calendar is SPYs own date list in the freeze. Scripts live in the scratchpad, not under research/questions/.

## Headline

- A (accrued matched-contributing nights, corrected NOFLAG-at-s definition, through 2026-08-26) = 42.
- Elapsed sessions 2026-06-01..2026-08-26 (calendar minus holidays, exclusions not pre-removed) = 61.
- r = 42/61 = 0.6885 matched-contributing nights per elapsed session - nearly 2x the 0.35 planning rate and well above the r-at-least-0.26 ceiling-test threshold.
- Tier-logic history (item 7): the only commits ever to touch services/conviction_monitor_service.py are three, all same-day, 2026-05-16 (13234cc 14:10 ET creation, baf17b8 15:13 ET, 2cb7a7e 15:33 ET) - all before the window start. No change after 2026-06-01. Result: window start does not move; stays 2026-06-01.
- Lock-or-DEFER call: Q019 LOCKS, on the drafted (unmodified) schedule - window 2026-06-01..2027-05-03, decision Monday 2027-05-24, one automatic extension to 2026-06-01..2027-06-15 / decision 2027-07-12 if a gate is short then. Per DECISIONS item 4, third branch, a rate faster than 0.35 changes nothing - it cannot pull a date in.
- Sub-cells already visible as likely-suppressed at record (section 8 / DP-43, projected at the current mix, not a determination): bearish direction (3/42 nights, about 7 percent), score band 90+ (2/42), score band under 80 (1/42, a single anomalous row, see below). Score band 85-90 (12/42, about 29 percent) and all three dam terciles (19/22/24) project comfortably past 20 by decision date.
- Structural (not accrual) zeros, expected to stay zero for the life of this window: the polarity firing-arm (polarity_only, both) is empty - 0/284 primary-trigger FLAG picks fired via polarity in the entire window - because polarity_unavailable_coverage_low is present on 100 percent of in-scope monitor rows dated 2026-06-01 through 2026-09-10 (0 exceptions), and polarity_tier has been WATCH on every single row since 2026-06-01 (the only HOLD/EXIT polarity rows in the whole freeze are in May 2026, pre-window). The age 3-5 sub-cell is likewise permanently empty for the primary trigger by the age-decay design (every primary FLAG fires at day 1 or day 2); it is populated only under the registered undecayed secondary.
- DP-50(a), item 10: zero commits since manifest SHA fa70688 touch the monitor write path or tier logic. The only commit since fa70688 is 2d5776c (PI-001, uoa_symbol_daily backfill-window fix), unrelated.

---

## (1) Section 2 funnel, matured window (pick nights 2026-06-01..2026-08-26)

| step | count |
|---|---|
| Calendar sessions in window | 61 |
| minus exclusions_v003.json nights in range (manual_runs plus non_session_runs plus uncorroborated_publication_runs) | 2026-06-26, 2026-07-02, 2026-07-06 (3 nights) |
| minus additional DP-04 late-finished_at nights | 0 further - the one DP-04-late night in range (2026-07-06, finished_at 2026-07-07 vs a 13:30 UTC next-open threshold) is already in the exclusions file; all other 60 nights runs finish about 21:0x-21:14 UTC same day, far ahead of the next sessions 13:30 UTC open |
| Matured, non-excluded pick nights | 58 |
| Published picks (qualified true and selected_rank not null) on those 58 nights | 465 (raw published across all 61 sessions before night exclusion equals 494; the 3 excluded nights carry 29 published rows) |
| published picks with zero in-scope monitor rows (t+1..t+5) | 0 of 465 - full monitor coverage in this window (contrast with the historical 915-published-vs-907-qualified gap noted in FREEZE_v001 section 1, not reproduced in this sub-window) |
| picks with no C_t | 0 |
| symbols with fewer than 60 daily bars dated on or before t | 0 |
| FLAG picks (primary trigger) with missing forward bars t+1..t+10 or no next-session open | 0 of 284 |
| caliper-matched candidate controls found ungradeable on the FLAG own window (spot-checked on all 194 post-caliper candidate pairs) | 0 |
| nights dropped for more than 25 percent ungradeable eligible picks | 0 (no gradeability failures were found anywhere in the matured population) |
| Immature nights (pick night after 2026-08-26, t+10 not yet matured on the freeze) | 10: 2026-08-27, 08-28, 08-31, 09-01, 09-02, 09-03, 09-04, 09-08, 09-09, 09-10 |

Pick-night-only quantities through 2026-09-10 (population only, no grading, per R1): the 10 immature nights carry 85 further published picks (8-9 per night). 9 of 85 show zero in-scope monitor rows so far - all 9 are the 2026-09-10 pick night itself, which structurally cannot have a t+1 row yet inside this freeze (not a data gap). Under the primary trigger, 48 picks across 9 of the 10 immature nights already carry an EXIT row despite the incomplete window - informational only, not gradeable, not counted toward A.

## (2) FLAG picks / FLAG nights

| trigger | FLAG picks (of 465) | FLAG nights (of 58) | age at first flag (days_since_qualified) |
|---|---|---|---|
| Primary: age_adjusted_severity equals EXIT | 284 (61.1 pct) | 57 | day 1: 223, day 2: 61 - zero at day 3-5 (age decay confines the primary to days 1-2, as designed) |
| Secondary, undecayed: overall_tier equals EXIT | 316 (68.0 pct) | 58 (every matured night) | day 1: 223, day 2: 61, day 3: 14, day 4: 11, day 5: 7 |

Session-distance-from-t matches days_since_qualified almost exactly for both triggers (small divergences at days 2-4 on the secondary, from holiday-adjacent nights, exactly the hazard section-2/threat-6 names - trading_date was used as authoritative throughout, never days_since_qualified).

By month (pick night t), primary FLAG picks: June 87, July 104, August 93.

## (3) Matched-contributing nights, rate per elapsed session, by month - the number that decides lock-or-DEFER

Under the corrected NOFLAG-at-s definition (Correction 1: a candidate control must carry an in-scope row dated exactly s, and none of its own in-scope rows dated on or before s may be EXIT; rows dated after s are never read) and Correction 2 (the control own pick night must be inside the same 58-night population):

| month | elapsed sessions | matched-contributing nights | rate |
|---|---|---|---|
| 2026-06 | 21 | 12 | 0.571 |
| 2026-07 | 22 | 12 | 0.545 |
| 2026-08 (03-26) | 18 | 18 | 1.000 (every non-excluded August night contributed) |
| Total 06-01..08-26 | 61 | 42 | 0.6885 |

A = 42. r = 0.6885 per session. The candidate-control pool at a given session s draws (as section 3 B2 specifies) from every non-excluded pick night with an in-scope row on s, not just the FLAG own night - measured pool size at s averages 14.5 candidates from about 4.2 distinct originating pick nights (min 2, max 23), which is why the match rate is materially higher than the eight-picks-per-night framing in PREREG threat 7 would suggest on its own.

Ceiling test (re-run): using the measured A equals 42 directly (Correction 3 form): needed nights equals 80 minus 42 equals 38; sessions equals 38 divided by 0.6885 equals 55.2; calendar days about 55.2 times 1.4484 equals 79.9, so the 80th contributing night would land near 2026-11-14 if the current rate held, decision-date-equivalent about 2026-12-05 - both dates are informational only. Per DECISIONS item 4, third branch: a rate faster than 0.35 changes nothing; the drafted schedule (window end 2027-05-03, decision 2027-05-24) stands unmodified; a fast rate is never used to pull a date in.

## (4) Flagged picks dropped for no valid control

195 of 284 primary FLAG picks (68.7 pct) dropped - DP-12 cost, paid in full, not softened.

| | dam mean | dam median | dam min/max |
|---|---|---|---|
| Dropped (n=195) | -0.940 | -0.763 | -5.978 / +1.175 |
| Matched/retained (n=89) | -0.167 | -0.206 | -1.288 / +1.652 |

The dropped population is systematically the more-damaged tail (mean -0.94 ATR vs -0.17 ATR) - the dam caliper empties for the largest drawdowns because too few NOFLAG published picks land at the same extreme dam on the same session. The retained (matched) primary FLAG picks speak only for ordinary-damage EXIT flags, not for the worst ones - stated per threat 7, this is exactly the shape predicted. By month: dropped June 66/87, July 77/104, August 52/93 (dropped share falling: 75.9 pct, 74.0 pct, 55.9 pct - consistent with a richer control pool as the monitor history accumulates).

## (5) Point-in-time guard failures (section 2)

Zero failures inside the window. All 160 guard failures in the full 3339-row table are in May 2026 (the launch/late-write outage window, KT_AUDIT section 2), specifically created_at-date not equal to trading_date. June/July/August/September 2026: 0 of 838 / 881 / 821 / 311 rows fail either guard clause. No pick in the matured window loses its only flag row to this guard.

## (6) technical_overall_tier UNKNOWN and polarity-unavailable shares

- technical_overall_tier equals UNKNOWN share of in-scope rows: June 0.75 pct (5/664), July/August/September 0 pct. Negligible.
- polarity_unavailable_coverage_low in reason_codes_json: 100 percent of in-scope rows in every month June through September 2026 (May 2026 pre-window was 80.3 pct). This is a structural finding, not a monthly hazard to watch - polarity coverage has not returned even once since 2026-06-01 through the freeze date. Corroborated independently: polarity_tier is WATCH on every row dated on or after 2026-06-01 (0 HOLD, 0 EXIT); all 35 polarity-EXIT and 53 polarity-HOLD rows in the whole freeze are in May 2026.
- WATCH rows whose only reason code is an availability code: June 1.06 pct (3/282), July 0.69 pct (2/291), August/September 0 pct. Low - most WATCH rows also carry genuine technical reason codes alongside the (universal) polarity-unavailable code.
- Consequence for item 8: every one of the 284 primary FLAG picks fired via the technical arm alone; polarity_only and both are empty by construction in this window, not by insufficient accrual.

## (7) Platform git history of the tier logic

git log --follow on services/conviction_monitor_service.py (read-only, platform repo) returns exactly three commits, all on 2026-05-16:

| SHA | timestamp (ET) | change |
|---|---|---|
| 13234cc | 2026-05-16 14:10:01 | initial creation (1039 lines) - the monitor, models, migration, job settings all land together |
| baf17b8 | 2026-05-16 15:13:06 | debug script to run bug fix (plus 263 / minus 57 lines) |
| 2cb7a7e | 2026-05-16 15:33:47 | debug script to run bug fix-2 (plus 51 / minus 6 lines) |

All Fix-1-through-6 work and the age decay are bundled into these three same-day commits (there is no separate commit per named fix - the registrar speculation in section 5 that they might be separately dated is not borne out). The last change to the tier logic is 2026-05-16, 15 calendar days before the window start (2026-06-01). Per DECISIONS item 3: the window start does not move. scripts/run_conviction_monitor.py and routers/conviction_monitor.py show no commits at all since manifest SHA fa70688.

## (8) FLAG-pick splits (matched-contributing nights, DP-43 demotion inputs)

Terciles computed on the full 42-night matched sample (not yet the expanding-window convention the locked eval.py will use - informational for the demotion projection only):

| split | cell | matched-contributing nights (of 42) |
|---|---|---|
| direction | bullish | 42 |
| direction | bearish | 3 - structurally rare (14/550 published rows are bearish per STEWARD_Q017_exposure.md); projected SUPPRESSED at record |
| score band | 80-85 | 39 |
| score band | 85-90 | 12 |
| score band | 90+ | 2 - projected SUPPRESSED at record |
| score band | under 80 | 1 - a single anomalous published row (TJX, 2026-06-11, overall_score 79.58, just under the nominal 80 qualification cut); noted, not investigated further here |
| dam tercile | T1 most adverse | 19 |
| dam tercile | T2 | 22 |
| dam tercile | T3 least adverse/favorable | 24 |
| age, primary trigger only | 1-2 | 42 (100 pct) |
| age, primary trigger only | 3-5 | 0, permanently, by the age-decay design, not an accrual gap (populated only under the registered undecayed secondary: 14/11/7 picks at days 3/4/5 respectively) |
| firing arm | technical-only | 42 (100 pct) |
| firing arm | polarity-only / both | 0 / 0, structural, see item (6) |

Projected at decision date (linear extrapolation from the current mix to 80 total matched-contributing nights - informational, the actual call is made on the full accrued sample at record): bearish to about 5.7, score-band-90-plus to about 3.8, score-band-under-80 to about 1.9, all three remain below the 20-night floor. Score band 85-90 to about 22.9 (crosses). All three dam terciles already exceed, or are within one night of, 20 and will clear comfortably. The polarity-firing-arm cells will not clear 20 under current data conditions no matter how long the window runs, because the underlying signal (polarity_unavailable_coverage_low) has not recovered since launch.

## (9) Hourly-bar coverage, sessions after s through t+10, both arms

100 percent symbol-level coverage, both arms. All 61 distinct FLAG-arm symbols and all 67 distinct control-arm symbols used in the matched set appear in the 227-symbol p001_hourly_raw universe - 0 missing. Confirms the PREREG expectation (section 3 B2, item 9): both arms are published picks, so the DP-27 adverse-first tie rule stays rare and symmetric here, matching the 100-percent-coverage precedent measured for Q015 (STEWARD_Q015_exposure.md section 7).

## (10) DP-50(a): commits since manifest SHA fa70688 touching the monitor

Zero. The only commit in the platform repo since fa70688 (the manifest pinned platform SHA) is 2d5776c - PI-001: floor the legacy outcome backfill window in-process - which touches uoa_symbol_daily backfill window resolution only; it does not touch conviction_monitor_service.py, scripts/run_conviction_monitor.py, routers/conviction_monitor.py, or any conviction-monitor table. The pinned conviction_monitor rows are unaffected.

---

## Answering the coordinator specific asks

- Contributing nights per arm/endpoint, exactly as section 2 / section 5 define them: P1 and P2 share the section 2 definition - A equals 42 matched-contributing nights (of 58 matured, non-excluded pick nights; 465 published picks; 284 primary FLAG picks; 89 matched FLAG picks). There is one arm pair (FLAG vs damage-matched NOFLAG), not two.
- Measured run-rate: r equals 0.6885 matched-contributing nights per elapsed session (elapsed equals calendar sessions minus holidays, 61; exclusions not pre-removed, per Correction 3).
- Projected date each floor is reached (informational; does not move the schedule per DP-43/DP-45): 80-contributing-nights floor about 2026-11-14 at the measured rate; 30-post-lock-nights floor about 2026-11-15 from a 2026-09-13 lock. Both land roughly 6 months ahead of the drafted 2027-05-24 decision date - DP-24 is confirmed not binding, exactly as the PREREG anticipated at the (much slower) 0.35 planning rate.
- Lock-or-DEFER call: LOCK, on the unmodified drafted schedule - window 2026-06-01..2027-05-03, decision Monday 2027-05-24, single automatic extension to 2027-06-15 / decision 2027-07-12 available under DP-13 if a gate is still short then. The measured rate (0.6885) exceeds both the r-at-least-0.26 ceiling threshold and the 0.35 planning rate, so per DECISIONS item 4, third branch, nothing moves the date in.
- Sub-cells projected below 20 nights at decision date: direction equals bearish, score band 90+, score band under 80 (accrual-based projections, see item 8) - plus two structural (non-accrual) zeros that will not be fixed by waiting: the polarity-only and both firing-arm cells, and the primary trigger age 3-5 cell.

## Files

- Scratchpad scripts (temporary, not committed under research/questions/): q019_r1.py through q019_r12_0910.py, intermediate parquet/json, all under the session scratchpad directory.
- This report: research/reports/STEWARD_Q019_exposure.md.

No controller state transition was made by this report - R1 informs the desk record-time lock-or-DEFER decision on Q019; it does not execute it.
