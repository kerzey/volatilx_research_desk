# Steward report: Q012 exposure-only count (R1)

Data Steward, 2026-09-13.
Routed request R1, `research/questions/Q012_capital_recycling/DECISIONS.md`
item 19 / `research/questions/Q012_capital_recycling/PREREG.md` Section 5 ("no measured exposure
exists for this population yet"). Frozen data only:
`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`
(`v001_sas_candidates.parquet`, `p001_daily_split.parquet`, `p001_hourly_raw.parquet`) against
`research/data/exclusions_v003.json`. No live query. No `results/` directory exists or was read.

**Protocol observed (binding): counts only.** Every number below is computable from `C_t` (the
pick-night close from `p001_daily_split`), the published ladder in `public_payload_json`, the
trading calendar and daily/hourly bar *presence*. No bar dated after a pick's own session t+1
was used to compute a touch, a return, a plan result, an excursion or a picks-minus-control
difference, and no outcome of any kind is reported. Bar *coverage* on t+1..t+5 and maturity counts
against the 60-session slot budget are coverage facts, not outcomes -- the only forward-looking
items, per the same discipline as `STEWARD_Q011_exposure.md` and `STEWARD_Q009_exposure.md` section R1.
This report **does not block the lock** (item 19) and **decides no endpoint** -- it confirms or
moves the item-5 schedule dates **out, never in**, and confirms item 6's demotion counts.

---

## Method and a note on "matured"

Q012's population (`PREREG.md` section 2) requires a **contributing night** to carry >= 1 eligible pick
**whose slot is gradeable in both plans** -- gradeable means the full **60-session** capital budget
has forward price data, i.e. session **t+60** must fall on or before the last date the pinned freeze
carries (2026-09-10). Because `manifest_v001` was frozen only three months into a window that opened
2026-06-01, **only 11 start nights (2026-06-01..2026-06-15) currently have their full 60-session
window inside the freeze at all** -- this is expected and is exactly why PREREG section 5 routes R2 (the
successor freeze) and why the decision date sits 5.6 months out. It is a freeze-horizon fact, not a
population defect.

Two funnels are therefore reported:

- **Funnel A ("currently gradable")** -- the literal, present-day PREREG section 2 population: published
  picks whose **t+60 window is already inside `manifest_v001`**. Tiny (11 nights) but true today.
- **Funnel B ("eligibility-criteria population")** -- the same six ladder/eligibility tests applied to
  **every published pick since 2026-06-01 that has at least a session t+1 bar in the freeze**
  (67 non-excluded sessions, through the last such night, 2026-09-09), **without** yet requiring the
  full t+60 window to exist. This is the basis for the run-rate and floor-date projections in
  Section 4 -- every one of these picks becomes gradable exactly when the R2 successor freeze
  (`manifest_v002`, price freeze through 60 sessions past 2026-11-20) exists, which is due before the
  decision pass, not before this report.

`C_t` = pick-night close, `prices_daily_split`. `ATR` not needed for counts. `dir` = +1 bullish /
-1 bearish, `dominant_direction`. Bands: **LOW** 80 <= score < 85, **HIGH** 85 <= score < 90, **ELITE**
score >= 90, **REF** score < 80. Exclusions: `exclusions_v003.json` union of `manual_runs`,
`non_session_runs`, `uncorroborated_publication_runs` (in-window: 2026-06-26, 2026-07-02,
2026-07-06).

---

## 1. Funnel A -- currently gradable under manifest_v001 (t+60 fully inside the freeze)

| Stage | Removed | Remaining |
|---|---|---|
| Published (DP-28), >=2026-06-01, non-excluded, t+60 window inside the freeze | -- | 88 (11 nights: 2026-06-01, 06-02, 06-03, 06-04, 06-05, 06-08, 06-09, 06-10, 06-11, 06-12, 06-15) |
| Missing >=1 of the 3 lane plans entirely (day_trading/swing_trading/longterm_trading) | 8 | 80 |
| All 3 lanes present but missing >=1 of the 6 targets (incl. a lane with only its first target) | 0 | 80 |
| Any of the six levels at/through C_t on the wrong side | 6 | 74 |
| outcome_target_invalid non-null | 1 | 73 |
| Symbol with <60 daily bars dated <=t | 0 | 73 |
| No session t+1 bar | 0 | 73 |
| ELIGIBLE / gradeable today | -- | 73 |

Contributing nights (LOW-or-HIGH): 10 of 11. The one matured night that drops to zero eligible
picks is 2026-06-02 -- all 8 published rows that night carry no lane plan at all (the same night
STEWARD_Q011_exposure.md section 1 flagged; not investigated further here, out of scope for a counts-only
report). Both-band nights: 6 (06-01, 06-05, 06-08, 06-10, 06-12, 06-15). ELITE contributing
nights: 4 (06-01, 06-03, 06-10, 06-15). REF contributing nights: 1 (06-11, the single TJX row,
score 79.58 -- see Section 5).

This is far below every floor in PREREG section 5/section 8 (80, 30, 20) -- as expected, since it reflects barely
two weeks of fully-matured slot budgets. It is not the number the decision pass will gate on; the
decision pass runs against manifest_v002 (R2), which will carry forward bars through 2027-02-22.

---

## 2. Funnel B -- eligibility-criteria population (basis for the run-rate)

| Stage | Removed | Remaining |
|---|---|---|
| Published (DP-28), >=2026-06-01, non-excluded | -- | 550 (68 nights) |
| No session t+1 bar inside the current freeze (right-censored at the 2026-09-10 edge) | 9 | 541 (67 nights, last 2026-09-09) |
| Missing >=1 of the 3 lane plans entirely | 8 | 533 |
| All 3 lanes present but missing >=1 of the 6 targets, broken out: | 8 | 525 |
| -- of which: lane present, first target present, second target null/missing | (2) | -- |
| -- of which: lane present with an empty targets list (no first target either) | (6) | -- |
| Any of the six levels at/through C_t on the wrong side | 7 | 518 |
| outcome_target_invalid non-null | 1 | 517 |
| Symbol with <60 daily bars dated <=t | 0 | 517 |
| No session t+1 bar (measurement-failure check, distinct from the calendar-edge row above) | 0 | 517 |
| ELIGIBLE (structurally; not yet t+60-gradeable -- see Funnel A) | -- | 517 |

This answers PREREG section 10 threat 12 directly: the all-six-levels requirement removes only 16 of 541
(3.0%), not materially below Q011's funnel (Q011 removed 8 of 383, 2.1%, on the weaker "swing lane
has a first target" test). The second-target gap is real but small: 8 rows (1.5% of the
541-row base) carry all three lanes but fail the six-target test -- 2 of those are a populated first
target with a null second target (PM 2026-07-08, V 2026-07-28, both day_trading); the other 6
(FICO, FOXA, GDDY, XYZ, CSCO, INTU) carry an empty day_trading.targets list (no first target
either), so they are not "second-target-only" gaps but full day-lane absences on otherwise-complete
payloads. No lane is ever present with a populated first target but a genuinely null (not just
short-list) second target beyond the 2 named above.

Contributing nights: 66 of 67 (same single zero-eligible night, 2026-06-02). Both-band nights:
42 of 67. ELITE contributing nights: 20 of 67. REF contributing nights: 1 of 67 (unchanged from
Funnel A -- TJX 2026-06-11 is the only sub-80 published row in the whole window: 1 of 579 published
rows, 0.17%, structurally near-absent because publication itself sits at a ~80 floor).

### Per-month breakdown (contributing nights / eligible picks, LOW-or-HIGH primary population)

| Month | Sessions (non-excl.) | LOW nights | HIGH nights | ELITE nights | REF nights | Both-band nights | LOW picks | HIGH picks | ELITE picks |
|---|---|---|---|---|---|---|---|---|---|
| 2026-06 | 20 | 19 | 14 | 10 | 1 | 14 | 101 | 32 | 11 |
| 2026-07 | 20 | 20 | 8 | 6 | 0 | 8 | 138 | 10 | 6 |
| 2026-08 | 21 | 21 | 14 | 3 | 0 | 14 | 140 | 23 | 3 |
| 2026-09 (partial, through 09-09) | 6 | 6 | 6 | 1 | 0 | 6 | 43 | 8 | 1 |
| Total | 67 | 66 | 42 | 20 | 1 | 42 | 422 | 73 | 21 |

LOW-or-HIGH eligible picks: 495. LOW-or-HIGH contributing nights: 66. LOW alone covers virtually
every session (66/67 = 98.5%, average 6.4 LOW picks per contributing night); HIGH is materially
scarcer (42/67 = 62.7%, average 1.7 HIGH picks per contributing night) and its monthly share is
uneven (70% to 40% to 67% to 100%-of-a-6-session-month) rather than trending -- see Section 4(c) for
what this means for HIGH-side refill.

---

## 3. Both-band nights (P2's own floor unit)

42 of 67 eligible-population sessions (62.7%) carry at least 1 gradeable LOW pick and at least 1
gradeable HIGH pick the same night -- by month: June 14, July 8, August 14, September 6 (partial).
Because LOW is present on almost every session, a both-band night is, in this data, functionally
equivalent to a HIGH-contributing night (the two counts coincide exactly, month for month) --
HIGH presence, not LOW presence, is what limits P2. Under Funnel A's stricter (currently-gradeable)
reading, both-band nights are only 6 of 10 LOW-or-HIGH contributing nights.

---

## 4. Run-rate and floor-date projections

Rate = 66 contributing (LOW-or-HIGH) nights / 70 elapsed sessions (2026-06-01..2026-09-09
inclusive) = 0.9429 contributing nights per session. Both-band rate = 42/70 = 0.6000 both-band
nights per session. ELITE rate = 20/70 = 0.2857/session. These are Funnel B rates (the larger,
non-maturity-gated base); Funnel A's 10-night sample is too thin to rate-project responsibly and is
not used for projection. All projected dates below are mechanical extrapolations only -- they gate
nothing; every PREREG section 8 gate is decided on eval.py's measured counts from the frozen data at the
decision pass. Construction: (i) raw pick-night date at the measured rate (365/252 session-to-
calendar conversion, matching STEWARD_Q007/Q009/Q011_exposure.md); (ii) plus 60-session maturity
(this question's own budget, not Q011's 20); (iii) plus 7-day freeze-build margin, rounded to the
next Monday on or after -- the same construction PREREG section 5's own decision date uses.

### (a) 80 contributing start nights (P1, P3 -- DP-21)

- 66 measured; need 14 more at 0.9429/session, about 14.8 sessions.
- Raw 80th pick night: 2026-10-01. Plus 60-session maturity: 2026-12-27. Plus 1-week margin, next
  Monday: 2027-01-04.
- This is well before the PREREG's own decision date (2027-03-01) -- not binding, matching
  section 5's projection that P1/P3's 80-night floor is not the binding uncertainty.

### (b) 80 both-band nights (P2 -- DP-21, the binding uncertainty per PREREG section 5)

- 42 measured; need 38 more at 0.6000/session, about 63.3 sessions.
- Raw 80th both-band pick night: 2026-12-10. Plus 60-session maturity: 2027-03-07. Plus 1-week
  margin, next Monday: 2027-03-15.
- This lands 2 weeks after the PREREG's own decision date (Monday 2027-03-01). At the measured
  June-September both-band rate, P2 is on track to miss its own 80-night floor at the decision
  date and would be reported INCONCLUSIVE (floor) per section 8, exactly the outcome PREREG section 5
  already flagged as the "binding uncertainty" -- this measurement confirms rather than resolves it.
  It does not move the decision date itself (P2's shortfall does not sink P1/P3, and no floor is
  lowered to hit a date -- section 5, item 5 of DECISIONS.md); it is reported here as the measured
  input the schedule note says R1 should supply.

### (c) 30 contributing start nights dated after the lock commit 2026-09-13 (DP-24)

- 0 measured today (no pick night after 2026-09-13 exists yet in the frozen data; the lock postdates
  the freeze).
- At 0.9429/session, 30 post-lock nights need about 31.8 sessions from 2026-09-13.
- Raw 30th post-lock pick night: 2026-10-29. Plus 60-session maturity: 2027-01-24. Plus 1-week
  margin, next Monday: 2027-02-01.
- Before the decision date (2027-03-01) -- not binding, with margin, matching section 5.

Summary:

| Floor | Status | Projected date |
|---|---|---|
| 80 contributing nights, P1/P3 (DP-21) | projected | 2027-01-04 -- not binding |
| 80 both-band nights, P2 (DP-21) | projected | 2027-03-15 -- after the 2027-03-01 decision date; P2 heading for INCONCLUSIVE (floor) at that date on current rate |
| 30 post-lock contributing nights (DP-24) | projected | 2027-02-01 -- not binding |
| 20 per sub-cell, ELITE | see Section 5 | already at 20 (Funnel B), declining monthly |
| 20 per sub-cell, REF | see Section 5 | 1 -- will not clear 20 |

---

## 5. ELITE and REF demotion -- confirmation of DECISIONS.md item 6 / item 3

REF is confirmed far below the 20-night suppression floor and will not approach it. REF (score <
80) is structurally near-absent from publication: 1 of 579 published rows in the whole
2026-06-01..2026-09-10 window score below 80 (TJX, 2026-06-11, score 79.58 -- just under the 80
cutoff), and it is the only REF-band contributing night measured (Funnel A and B agree). Publication
sits at an effective ~80 floor by construction; REF picks are not a thin cohort that might grow,
they are a near-zero one. Item 3's demotion (descriptive, labelled 80-85 stand-in) and item 6's
SUPPRESSED-below-20 treatment are both confirmed with high confidence.

ELITE is thinner than PREREG section 5's own projection assumed, but not "far below 20" as
measured today -- it is a declining trend that has already touched the floor. Funnel B measures
20 contributing ELITE nights through 2026-09-09 (67 sessions), against a sharply declining monthly
count: 10, 6, 3, 1 (June/July/August/September-partial) -- consistent with DATA_NOTES's "12 / 8
/ 3 / 2 elite picks per month" finding (picks, not nights, but the same shape). Two things are true
at once: (i) the cumulative count has already reached the 20-night suppression line, so ELITE is
not guaranteed SUPPRESSED at the decision pass purely on a "far below 20" basis; (ii) the
within-window trend is toward zero, so whether cumulative ELITE nights stay at or above 20
through 2027-03-01 depends on whether September's near-zero rate (1 night in 6 sessions) persists --
a flat extrapolation of the full-window average (0.2857/session) would add roughly 14 more nights by
the 2026-11-20 window end (total about 34), but a flat extrapolation of the September rate alone
would add close to zero. This is a measured fact, not a ruling: DECISIONS.md item 6's demotion to
descriptive at lock is a DP-43 default independent of the night count and is unaffected either
way (ELITE carries no verdict in this question regardless); what R1 confirms is only that the
SUPPRESSED-below-20 print-or-not question is genuinely live and should be re-measured at the
decision pass on eval.py's own count, not assumed from the June-based section 5 projection.

---

## 6. Hourly-bar coverage on the first five sessions after each start night (ordering rule 1)

p001_hourly_raw covers exactly the 227 published-pick symbols in the freeze. All 167 distinct
symbols carried by the 495 LOW/HIGH eligible picks (Funnel B) are inside that hourly universe --
0 missing. Of those 495 picks, 461 have their full first-five-forward-session window inside the
current freeze (the other 34 sit near the 2026-09-10 freeze edge and simply do not have 5 forward
calendar sessions yet, a freeze-horizon artifact, not a coverage gap). Of the 461 with a complete
5-session window, all 461 (100.0%) have at least 1 hourly bar on every one of their first five
forward sessions -- 2,391 of 2,391 available pick-session pairs covered. Ordering rule 1 (L1 vs L2
same-session, Plan R) will resolve from hourly bars for the entire published-pick population
measured here; no fallback-to-L1 case is expected among published symbols. This also confirms the
successor freeze's hourly symbol scope is sufficient, provided manifest_prices_v002 again scopes
hourly bars to published symbols only (control-chain symbols will still fall to ordering rule 1's
stated conservative reading, as PREREG section 2/section 10 threat 11 already anticipates).

---

## 7. Eligible same-cohort refill availability per session (LOW / HIGH separately)

Refill availability = the same contributing-night counts read as "does this session offer at
least 1 eligible pick of this cohort." Over the 67-session eligibility-criteria window:

| Cohort | Sessions with >=1 eligible pick | Sessions with 0 (idle-refill risk) | Avg picks per non-idle session |
|---|---|---|---|
| LOW | 66 / 67 (98.5%) | 1 (1.5%) | 6.4 |
| HIGH | 42 / 67 (62.7%) | 25 (37.3%) | 1.7 |

A LOW slot almost never lacks a refill candidate on any given session. A HIGH slot's refill
supply is materially thinner -- over a third of sessions in this window published no HIGH-band pick
at all, and the monthly HIGH-contributing-night share swings from 70% to 40% to 67% to 100% (n=6)
rather than holding steady, so a HIGH slot's idle risk inside a 60-session Plan R budget is not a
small-print detail -- it is likely to bind on some HIGH chains. This is a counts-only fact for
eval.py's idle-session accounting (PREREG section 4, "if no eligible same-cohort pick exists ...
the slot is idle") and decides nothing.

---

## 8. Data caveats

1. The t+60 maturity gate is the whole story of why Funnel A is thin. manifest_v001 (as_of
   2026-09-10) simply has not existed long enough for most of the 2026-06-01..2026-11-20 window to
   complete a 60-session forward budget. This is not a data defect and needs no correction -- it is
   the reason PREREG section 5 names a 2027-03-01 decision date and routes R2.
2. The single zero-eligible night (2026-06-02) recurs from Q011. All 8 published rows that night
   carry no lane plan at all -- the same finding STEWARD_Q011_exposure.md section 1/section 4
   flagged. Not re-investigated here (counts-only scope); still worth the registrar's/red-team's
   attention if it recurs on later nights once R2 is built.
3. REF's near-absence is a publication-threshold fact, not a sampling artifact -- the platform's
   own qualification gate sits within a hair of 80, so a "descriptive REF cohort" is really a
   1-row cohort for the life of this window; the labelled 80-85 stand-in in PREREG section 2/section
   3 will have essentially nothing to describe.
4. ELITE's SUPPRESSED-or-not status is genuinely undetermined by this report and should be
   re-measured at the decision pass rather than assumed from either the section 5 projection (which
   assumed "far below 20") or a flat extrapolation of the June-September average (which would put
   it well above 20) -- the within-window trend is toward zero and neither extrapolation is
   reliable on 4 months of a 6-month primary window.
5. Hourly coverage is complete for every published symbol measured, consistent with
   manifest_prices_v001's hourly scope (227 published-pick symbols) and with
   STEWARD_Q011_exposure.md's identical finding for its own population.
6. Both-band nights track HIGH-band nights almost exactly in this data (LOW is present on 98.5%
   of sessions), so P2's floor is really gated by HIGH-band publication frequency, not by any
   LOW-HIGH interaction.

---

## Files

- This report: research/reports/STEWARD_Q012_exposure.md.
- No new data files were written; no manifest, exclusions or state file was created or modified.
  All counts were re-derived from research/data/v001_sas_candidates.parquet,
  research/data/p001_daily_split.parquet and research/data/p001_hourly_raw.parquet against
  research/data/exclusions_v003.json. The controller was not advanced (R1 does not block the lock
  and this report builds no new freeze -- R2 is a separate, later routed request due at the
  decision date).
