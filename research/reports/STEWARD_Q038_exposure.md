# STEWARD_Q038_exposure — R1 (counts only), Q038 monitor_tier_calibration

Request: PREREG.md §5.7 R1 (research/questions/Q038_monitor_tier_calibration/PREREG.md) and DECISIONS.md
"Routed requests — data-steward R1" (research/questions/Q038_monitor_tier_calibration/DECISIONS.md).
Data: `research/data/manifest_v001.json` (table keys `sas_candidates`, `sas_runs`, `conviction_monitor`),
`research/data/manifest_prices_v001.json` (`p001_daily_split.parquet`, `p001_hourly_raw.parquet`),
`research/data/manifest_prices_universe_v001.json` (not needed — the candidate pool is entirely inside
the 436-symbol `manifest_prices_v001` universe, verified below), `research/data/exclusions_v003.json`.
No live query was made (DP-50(c)); the 2026-09-15 census's live counts are design sizing only and are
not used to settle anything here. Platform history read read-only from the pinned platform repo
(`git log`/`show`, DP-50(a)/(b)). **No outcome of any kind is reported** — no touch, no race,
no rate, no return, no excursion, no tier-versus-outcome cross-tab of any shape; forward bars (t+6..t+15)
were read only to confirm existence for gradeability/maturity accounting, never a value from that range.
`dam5` (a matching covariate fixed before any t+6-or-later bar is read, per §2.4) is computed and reported
per R1 item (4)'s own instruction. Method note (temporary counts-only tool, not the locked `eval.py`):
ATR14 = a simple 14-bar mean of True Range on `prices_daily_split`, bars dated <= t (same convention as
`STEWARD_Q019_exposure.md`). Trading calendar = SPY's own date list in `p001_daily_split` (153 sessions,
2026-02-02..2026-09-10). Scripts live in the session scratchpad, not under `research/questions/`.

## Decision paragraph

**PUSH DATES — do not lock on the drafted schedule, do not DEFER on the primary criterion alone — and
flag one fragile, decision-critical number for the coordinator.** The measured primary contributing-night
rate is **19/53 = 0.3585 per eligible session** (95% CI 0.243–0.493), which lands inside DP-43's
0.29–0.55 band: window end, interim date and both decision dates move out (§5.6 middle branch), they do
not lock as drafted (2027-03-01) and the rate is not low enough to DEFER on that number by itself. At this
rate the **80-contributing-night floor projects to window end ~2027-04-26, decision ~2027-05-24** and the
**>=20 three-group-night gate (§8 clause 6) is already effectively met** (18/53 measured, clears by ~60
sessions). But **item (6) — the B3 (`S2`) two-way gate DECISIONS.md decided (item 3, DEFAULTED R-5) — is
the binding constraint, not the primary.** Measured B3: only **4 of 129** matured, gradeable `G_C` picks
obtain a 1:1 same-night, same-direction, +/-0.25 ATR `dam5`-matched `G_A` pick (3.1%); the B3-contributing-
night rate is **4/53 = 0.0755/session**, and at the primary's own implied decision date (2027-05-24) B3
projects to only **~17 of the 20 nights** clause 7 requires. Pushing the decision date further, to
**~2027-07-26** (B3's own central rate reaching 20), clears B3 **and** stays inside the 2027-09-15 ceiling
— so on the **measured/central rate**, DP-43's push-branch (not DECISIONS item 8's DEFER branch) is what
textually fires, with the new decision date set by B3, not by the primary. **The number is fragile: B3
rests on 4 successes in 53 nights (95% CI 0.030–0.179).** At the CI's lower bound B3 would need ~590
total eligible sessions — unreachable inside the ceiling — which is exactly the condition DECISIONS item 8
names for DEFERRED ("CONFIRMED is unreachable from the run by design... Q038 is DEFERRED rather than
locked"). §5.4 already establishes NULL is unreachable on any window this size, so if B3 cannot clear, the
design can only return INCONCLUSIVE and item 8's DEFER branch is the one that fires. **I do not resolve
this call — the coordinator does, per the routing protocol — but I report it as the single number that
decides between "push to ~2027-07-26" and "DEFER now," and recommend re-measuring B3 specifically (not
just the primary rate) at R2, before the interim freeze, rather than trusting a 4-success estimate through
to the decision pass.** No other gate is close: three-group nights clear early (18/53), the 90+ score band
clears easily (10 distinct nights of 53, rate 0.189/session — **not** suppressed, unlike Q019's precedent),
and bearish stays suppressed (1/53). Two data-quality notes, neither blocking: (a) 74 of 491 eligible
picks are genuinely holiday-shortened (4 in-scope rows, not 5), exactly as §10.7 anticipates; (b)
**2026-07-06 carries zero `conviction_monitor` rows for the entire day** — a complete one-day outage,
distinct from and additional to the four holiday off-calendar dates — worth a defect filing on its own
(see item 3).

---

## (1) §2.5 funnel, night by night, both cohorts (DP-53: maturity added once, cohorts reported separately)

**Trading calendar:** 153 sessions 2026-02-02..2026-09-10 (SPY bars, `p001_daily_split`). **Maturity
boundary — the exact t+15 session, fixed here for R1** (§5.2's "the Steward fixes the exact session"):
the last pick night `t` whose full session t+6..t+15 window is inside the freeze (last date 2026-09-10)
is **2026-08-19** (index 137 of 153; t+15 for 2026-08-19 = 2026-09-10, the freeze's last date; t+15 for
2026-08-20 would be 2026-09-11, not in the freeze). This is one session later than the PREREG's own rough
"~2026-08-18" estimate.

| step | value |
|---|---|
| Elapsed calendar sessions 2026-06-01..2026-09-10 | 71 |
| minus exclusions_v003.json in-window nights | 2026-06-26, 2026-07-02, 2026-07-06 (3 nights) |
| minus additional DP-04 late-finished_at nights | 0 further |
| Eligible sessions | 68 |
| Matured eligible pick nights (2026-06-01..2026-08-19) | 53 |
| Immature eligible pick nights (2026-08-20..2026-09-10) | 15 |
| Published picks, 68 eligible nights | 550 (raw pre-exclusion, 71 nights: 579) |
| matured cohort (53 nights) published picks | 424 |
| immature cohort (15 nights) published picks | 126 |
| Matured picks with zero in-scope monitor rows | 0 of 424 |
| Immature picks with zero in-scope rows | 9 of 126, all the 2026-09-10 pick night |
| Point-in-time guard failures in-window | 0 (all 160 in the full freeze are May 2026, pre-window) |
| Matured picks with no C_t / no Close_t5 / no Open_t6 / fewer than 60 prior daily bars | 0 / 0 / 0 / 0 |
| Matured picks ungradeable (missing any daily bar t+6..t+15) | 0 of 424 |
| Nights with more than 25 pct of eligible picks ungradeable | 0 |
| Matured picks failing the row-count/last_i eligibility rule | 24 of 424, see item 3 |
| Matured eligible classifiable picks | 400 |
| Immature picks failing the same rule (informational only) | 35 of 126 |

## (2) Terminal-state split G_A/G_B/G_C, both fields, plus the day-5 cross-tab (bijection, measured)

Under overall_tier (the classifier, decision 1), all 491 eligible picks (matured + immature):

| group | n | matured only (of 400) |
|---|---:|---:|
| G_A (never EXIT) | 159 | 130 |
| G_B (softened) | 170 | 141 |
| G_C (persisting EXIT) | 162 | 129 |

By month (all eligible, incl. immature): 2026-06 G_A 55 / G_B 49 / G_C 40; 2026-07 43 / 53 / 55;
2026-08 54 / 61 / 55; 2026-09 (immature only, partial) 7 / 7 / 12.

Under age_adjusted_severity (the displayed secondary field), same 491 picks:
G_A 320, G_B 171, G_C 0 -- structurally empty at the pick level, confirming the PREREG's own Decision-1
rationale (day 3-5 decay makes an undecayed-EXIT terminal row impossible under this field) as a measured
fact, not an assumption.

Pick-level agreement between the two classifiers (n=491): G_A-G_A 159, G_B-G_A 10, G_C-G_A 26,
G_B-G_B 160, G_C-G_B 136 (G_A-G_B combination = 0). Overall raw agreement 65.0 pct -- not higher, because
the age field collapses the softened and persisting groups into a single non-EXIT bucket by construction.

Day-5 cross-tab, measured directly on the row dated exactly t+5 (n = 417 published picks with such a row,
guard-passed):

| overall_tier vs age_adjusted_severity | HOLD | WATCH |
|---|---:|---:|
| EXIT | 0 | 142 |
| WATCH | 275 | 0 |

Bijection holds on 417 of 417 rows (100 pct, 0 exceptions): EXIT maps to WATCH, WATCH maps to HOLD, no
other cell populated -- exactly as section 2.3 states, now measured rather than assumed.

Monthly claim-scope shares (total in-scope, guard-passed rows across all 550 published picks: 2,505 rows):

| month | polarity_unavailable_coverage_low share | polarity_tier dist | overall_tier HOLD rows | technical_overall_tier UNKNOWN share |
|---|---:|---|---:|---:|
| 2026-06 | 100.0 pct | WATCH 664 (100 pct) | 0 | 0.75 pct (5/664) |
| 2026-07 | 100.0 pct | WATCH 752 (100 pct) | 0 | 0.00 pct |
| 2026-08 | 100.0 pct | WATCH 821 (100 pct) | 0 | 0.00 pct |
| 2026-09 partial | 100.0 pct | WATCH 268 (100 pct) | 0 | 0.00 pct |

Structural, not accrual: the polarity arm has not returned once in this window. Reproduces Q019's item 6.

## (3) In-scope-row-count distribution and the eligibility-rule failure count

| in-scope rows | count (of 550) | note |
|---:|---:|---|
| 0 | 9 | all immature -- the 2026-09-10 pick night |
| 1 | 9 | all immature |
| 2 | 8 | all immature |
| 3 | 33 | 24 matured (excluded) + 9 immature |
| 4 | 74 | eligible -- holiday-shortened cohort |
| 5 | 417 | eligible -- full watch |

Failing the eligibility rule: 59 of 550 total (24 matured, permanently excluded and counted; 35 immature,
not yet gradable). In the matured cohort the failure rate is 24/424 = 5.7 pct, entirely concentrated on
three consecutive pick nights: 2026-06-29, 2026-06-30 and 2026-07-01 (24 picks, every one of them). Root
cause, traced directly: for these nights, session t+3 or t+4 lands on 2026-07-06, and conviction_monitor
carries zero rows for the entire day 2026-07-06 -- a complete one-day outage, confirmed system-wide (row
count by trading_date in-window: every other session carries 31 to 56 rows; 2026-07-06 carries exactly
0). This compounds with the adjacent 2026-07-03 holiday (a market-closed weekday on which the job still
wrote about 44 off-calendar rows dated 07-03 -- see below -- so those rows exist but don't match any
t-plus-k session) to drop these three nights' picks to 3 in-scope rows each, one short of the 4-row floor.
This 2026-07-06 outage is a new finding, distinct from ordinary holiday shortening, and is not itself in
exclusions_v003.json (that file excludes 2026-07-06 as a pick night for an unrelated SAS re-run reason;
the conviction_monitor outage that day is a separate, previously unfiled fact worth a defect entry).
Holiday-shortened 4-row picks (74, genuinely by design, not excluded): cluster at pick nights 2026-06-12,
06-15 through 06-18 (Juneteenth, 2026-06-19, still received about 40 off-calendar monitor rows that day)
and 2026-08-31 through 09-03 (Labor Day, 2026-09-07, ahead of them -- these four nights are also in the
immature cohort, so this bucket is informational there).

Off-calendar monitor rows (dated on a non-trading weekday), full in-window count: 107, on exactly the four
weekday market holidays inside or adjacent to the window: 2026-05-25 (Memorial Day, 40 rows, pre-window
spillover), 2026-06-19 (Juneteenth, 40), 2026-07-03 (Independence Day observed, 44), 2026-09-07 (Labor
Day, 43). These confirm the "five weekdays, not five sessions" mechanism directly: the monitor's cron runs
Monday through Friday regardless of market holidays, writing a row dated on the holiday that matches no
t-plus-k session and is correctly excluded by the session-membership filter (never included by a
date-range filter, which would silently ingest it -- verified this distinction mattered in code).

## (4) B2 pool depth -- unpublished sas_candidates after the dam5 caliper and direction constraint

Pool size: about 44 unpublished (dark-lane-inclusive) candidate rows per night with a computable dam5
(2,927 valid rows over 66 of 68 eligible nights; the 2 missing nights are late-window nights lacking a
Close-t-plus-5 inside the freeze) -- matches the PREREG's own "about 42 a night" estimate.

Share of eligible picks obtaining 3-or-more / 10-or-more caliper-matched controls, by group (all 491
eligible picks, 482 with a computable own dam5):

| group | n eligible | share 3-or-more controls | share full 10 controls | share zero controls |
|---|---:|---:|---:|---:|
| G_A | 159 | 56.0 pct (89) | 1.3 pct (2) | 17.6 pct (28) |
| G_B | 170 | 56.5 pct (96) | 1.2 pct (2) | 10.0 pct (17) |
| G_C | 162 | 37.7 pct (61) | 0.0 pct (0) | 28.4 pct (46) |
| overall | 491 | 50.1 pct (246) | 0.8 pct (4) | 18.5 pct (91) |

G_C (the most-damaged group by construction) has the thinnest control pool -- the DP-12-predicted shape,
reproducing Q019's finding that the caliper empties fastest for the extreme tail.

dam5 distribution, dropped (fewer than 3 controls) vs retained (3 or more), by group (dam5 present, n=482):

| group | dropped n / mean / median | retained n / mean / median |
|---|---|---|
| G_A | 68 / plus 1.646 / plus 1.417 | 89 / plus 0.472 / plus 0.407 |
| G_B | 70 / plus 0.734 / plus 0.613 | 96 / minus 0.003 / minus 0.066 |
| G_C | 98 / minus 2.259 / minus 2.053 | 61 / minus 1.268 / minus 1.202 |
| overall | 236 / minus 0.246 / minus 0.432 | 246 / minus 0.145 / minus 0.173 |

In every group the dropped tail sits further from zero than the retained tail (more favorable in G_A,
more adverse in G_C) -- the caliper systematically loses the extremes, as designed and as disclosed,
never softened.

## (5) Contributing-night and three-group-night rate per eligible session, by month

Computed on the matured cohort only (53 eligible sessions; gradeable, control-matched [3 or more
controls] picks per section 2.6):

| month | eligible sessions | contributing nights | three-group nights | contrib rate | 3-group rate |
|---|---:|---:|---:|---:|---:|
| 2026-06 | 20 | 5 | 4 | 0.250 | 0.200 |
| 2026-07 | 20 | 7 | 7 | 0.350 | 0.350 |
| 2026-08 | 13 | 7 | 7 | 0.538 | 0.538 |
| total | 53 | 19 | 18 | 0.3585 | 0.3396 |

95 pct Wilson CI on the primary rate: 0.243 to 0.493 (n=53). This is the number that decides section
5.6's lock-or-DEFER call, per DECISIONS item 5: 0.3585 falls inside the 0.29-0.55 band, so the window
end, the interim date and both decision dates move out; nothing locks as drafted, and nothing DEFERs on
this number alone. Month-over-month the rate is rising (0.25, then 0.35, then 0.54), consistent with a
richer control pool as the monitor history accumulates (the same pattern Q019 measured). Group presence
per matured night: 77 G_A / 83 G_B / 48 G_C matched-and-gradeable picks across the 53 nights. 34 of 53
matured nights are non-contributing (carry a matched pick in at most one extreme group), not excluded --
listed in the scratch output, available on request.

## (6) B3 (S2) feasibility -- the two-way gate DECISIONS item 3 (DEFAULTED, R-5) made material

Of the 129 matured, gradeable G_C picks with a computable own dam5, only 4 obtain a 1-to-1, same-night,
same-direction, 0.25-ATR-caliper dam5-matched G_A pick (greedy nearest, without replacement, ties by
symbol ascending) -- a 3.1 pct match rate, thinner than Q019's 31.3 pct published-to-published match
rate, because the pool here is restricted to G_A picks specifically (not all published picks) within the
same night. B3-contributing nights (1 or more matched pair): 4 of 53 (7.5 pct), 95 pct Wilson CI 0.030 to
0.179 -- a very wide interval on a 4-success numerator.

Projected B3 count at the decision date the primary rate alone would imply (window end about 2027-04-26,
decision about 2027-05-24, about 224 total eligible sessions): about 16.9 -- below the 20-night floor
clause 7 (as amended by Decision 3) requires. Pushing further, to where B3's own central rate reaches 20
(window end about 2027-06-24, decision about 2027-07-26, about 265 total eligible sessions), clears the
floor and stays inside the 2027-09-15 ceiling. At the CI's lower bound (0.030), reaching 20 would need
about 590 total eligible sessions -- unreachable inside the ceiling. This is the fragile number described
in the decision paragraph: on the measured or central rate, DP-43's push branch fires (new date about
2027-07-26, driven by B3); on the CI's pessimistic tail, DECISIONS item 8's DEFER branch fires instead.
Recommend re-measuring B3 specifically at R2 (not only the primary rate) before treating either
resolution as settled.

## (7) 90+ and bearish counts per night (section 4(d) suppression test)

On the matured, matched (3 or more controls), gradeable sample (n=208 picks, the same population item
(5)'s contributing/non-contributing nights are built from):

| band | n picks | distinct nights (of 53) | rate per session |
|---|---:|---:|---:|
| score under 80 | 1 | 1 | 0.019 |
| score 80 to 85 | 169 | -- | -- |
| score 85 to 90 | 28 | -- | -- |
| score 90 or above | 10 | 10 | 0.189 |
| bearish | 1 | 1 | 0.019 |

By group: 90-plus picks split G_A 4 / G_B 3 / G_C 3 (no concentration in one group). Bearish: the single
matched-sample occurrence is in G_C. Score band under 80 and bearish stay suppressed at any projected
schedule (both project to only 4 to 5 nights even at the farthest, 2027-07-26, horizon, far under the
20-night floor -- matching the already-decided suppressions and STEWARD_Q017_exposure.md item 1's
platform-wide bearish scarcity). Score band 90-plus projects to about 42 nights by the 2027-05-24 horizon
(0.189 per session times about 224 sessions) and higher at any pushed-out date -- clears the 20-night
floor comfortably and should NOT be suppressed at lock, unlike Q019's precedent (where 90-plus was thin,
2 of 42). The full published (pre-match) window population shows the same pattern less filtered: 23 of
550 published rows (4.2 pct) are 90-plus, 14 of 550 (2.5 pct) bearish -- both consistent with
STEWARD_Q017_exposure.md.

## (8) Hourly-bar coverage of in-window unpublished candidate symbols

391 distinct unpublished-candidate symbols appear in the B2 pool across the 68 eligible nights (rows with
a computable dam5). Of these, 215 (55.0 pct) are covered by manifest_prices_v001's 227-symbol hourly
freeze -- not because unpublished symbols were hourly-frozen directly, but because those 215 symbols were
also published on some other night in the window (the hourly freeze is published-symbols-only). Row-level
coverage (weighted by how often a symbol actually appears as an unpublished candidate) is higher: 72.3
pct (2,116 of 2,927 valid B2-pool rows) -- materially above the naive 227-of-436 equals 52.1 pct
symbol-count reading the PREREG's ordering-rule-1 discussion cites, because frequently-selected symbols
dominate candidate-row volume and cycle between published and unpublished across nights. Consequence for
DP-27 (ordering rule 1): on the sealed portion, the adverse-first tie-resolution rule binds on about 27.7
pct of unpublished-control same-session ties, not the about 48 pct a symbol-count-only reading would
suggest. This is a genuinely better number than the PREREG's conservative framing, worth carrying into
eval.py's own printed tie-rate accounting; R2's ask for full hourly coverage on successor nights remains
necessary regardless, since the sealed-portion asymmetry (even at 72.3 pct) is real and non-zero.

## (9) Platform git history -- tier-logic ship / polarity-restoration check (re-run of Q019 R1 item 7)

git log --follow on services/conviction_monitor_service.py in the pinned, read-only platform repo
returns exactly the same three commits Q019's R1 found, all 2026-05-16: 13234cc (14:10:01 ET, initial
creation), baf17b8 (15:13:06 ET, bug-fix debug script), 2cb7a7e (15:33:47 ET, bug-fix-2 debug script). A
parallel check on scripts/run_conviction_monitor.py and routers/conviction_monitor.py (not part of
Q019's original check, added here for completeness) returns one additional commit, f4f4e1494 (2026-05-16
17:41:02 ET, "Conviction monitor UI implementation" -- the router/UI layer, not the tier logic), also
pre-window. A git log from the manifest's pinned platform SHA (fa70688) to HEAD, filtered to these three
files, returns zero commits. No tier-logic ship, no polarity-restoration commit, dated or undated, exists
inside or after the window. Section 5.6's window-start rule does not fire; the window start stays
2026-06-01.

---

## Answering the coordinator's specific asks

Contributing nights per arm/endpoint, exactly as sections 2 and 5 define them: P1 and P2 share the
section 2.6 definition and are identical by construction -- 19 matured contributing nights (of 53
matured eligible sessions; 400 matured eligible/classifiable picks; 208 matched-and-gradeable picks
across G_A/G_B/G_C 77/83/48). Three-group nights: 18. B3-contributing nights: 4.

Measured run-rate: primary r = 0.3585 per eligible session (95 pct CI 0.243 to 0.493, n=53); three-group
r = 0.3396; B3 r = 0.0755 (95 pct CI 0.030 to 0.179, n=53, only 4 successes).

Projected dates each floor is reached, at the measured/central rate (uncertainty scenarios below; DP-53:
matured-cohort rate applied to future eligible sessions, maturity leg added once):

| floor | needed beyond accrued | central projection | optimistic (rate CI high) | pessimistic (rate CI low) |
|---|---|---|---|---|
| 80 contributing nights (primary, DP-21) | plus 61 beyond 19 accrued | window end about 2027-04-26, decision about 2027-05-24 | window end about 2027-02-17, decision about 2027-03-22 | window end about 2027-08-20, decision about 2027-09-20 -- past the ceiling |
| 20 three-group nights (clause 6) | plus 2 beyond 18 accrued | clears almost immediately, about 2026-09 | -- | -- |
| 20 B3 nights (clause 7, Decision 3) | plus 16 beyond 4 accrued | window end about 2027-06-24, decision about 2027-07-26 | (rate CI high 0.179) about 2027-01, well inside | (rate CI low 0.030) needs about 590 sessions -- unreachable inside the 2027-09-15 ceiling |
| 60 contributing nights (DP-58 interim) | plus 41 beyond 19 accrued | window end about 2027-02-03, look about 2027-03-08 | -- | -- |
| 30 post-lock contributing nights (DP-24) | 30, none accrued (lock is today) | pick night about 2027-01-14 (matures about 2027-02-05) -- clears well before any decision date above; not binding | -- | -- |

Trading calendar for projected (future, post-2026-09-10) dates was constructed from the standard NYSE
holiday schedule (fixed and observed dates through 2028), independently reproduced and cross-checked
against three dates the PREREG itself states (interim window end 2026-12-01, t-plus-15 2026-12-22,
Monday 2027-01-04; fixed-look window end 2027-01-29, t-plus-15 2027-02-22; extension window end
2027-03-15, t-plus-15 2027-04-06) -- all three reproduce exactly, so the future-calendar construction is
trustworthy for the projections above.

Uncertainty scenarios: shown in the table above via each rate's 95 pct Wilson CI (small-n binomial,
appropriate given 53 matured nights). The primary rate's own pessimistic CI bound (0.243) sits below the
0.29 DEFER threshold -- so even the primary criterion alone is not fully settled at 95 pct confidence,
though the point estimate is comfortably inside the push band. B3's CI is the wider and more
decision-relevant uncertainty -- see item (6) and the decision paragraph.

DP-53 cohort separation: the fully observable (matured) cohort is 53 nights and 19 contributing, reported
and used for every rate above; the immature tail (15 nights, 2026-08-20 through 2026-09-10, 126 published
picks, of which 35 also fail the row-count rule but are not yet classifiable and are not counted toward
any floor) is reported separately in item (1) and never mixed into the rate.

## Files

Scratch scripts and intermediate parquet/json (temporary, not committed under research/questions/):
build.py through build11.py, futcal.py, calendar.json, future_calendar.json, per_pick parquet files,
unpub_candidates.parquet, per_night_summary.parquet, b3_summary.json, all under the session scratchpad
directory. This report: research/reports/STEWARD_Q038_exposure.md.

No controller state transition was made by this report. R1 informs the desk's record-time
lock/push/DEFER decision on Q038; it does not execute it. readiness.json written alongside per
research/templates/READINESS_TEMPLATE.json, counts only.
