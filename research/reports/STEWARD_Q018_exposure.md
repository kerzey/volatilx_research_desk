# Steward report: Q018 exposure-only count (R1) + DP-50(a) commit sweep

Data Steward, 2026-09-13.
Routed request R1, research/questions/Q018_lane_choice_by_band/DECISIONS.md "Routed requests"
(data-steward -- R1), also PREREG.md Section 5 R1. Coordinator's addition: report the
contributing-night counts per arm/endpoint exactly as PREREG Section 2/Section 5 define them, the
measured run-rate, and the projected floor dates. Frozen data only:
research/data/manifest_v001.json + research/data/manifest_prices_v001.json
(v001_sas_candidates.parquet, p001_daily_split.parquet) against research/data/exclusions_v003.json.
No live query. No new manifest, exclusions file or results/ directory was written; two temporary
analysis scripts were run from the scratchpad and are not part of this repo. Two dated entries
were added to research/data/DATA_NOTES.md (new findings surfaced while answering item (2) and the
DP-50(a) sweep, both counts/facts, no outcome). The controller was not advanced -- R1 is not a
blocker for lock and this report builds no new freeze.

Protocol observed (binding): counts only. Every number below is computable from C_t (the
pick-night close, p001_daily_split), ATR14 desk-computed from p001_daily_split bars dated <= t,
the published ladder in public_payload_json, the trading calendar, and the session t+1 official
open (used only per DECISIONS item 3's explicit carve-out, to test whether a target was already
at/through the open -- never to grade a touch, a return or a plan result). No bar dated after a
pick's own session t+1 was used for anything else. No outcome of any kind is reported; no lane
comparison is made.

---

## Headline

- Population: published picks (qualified IS TRUE AND selected_rank IS NOT NULL, DP-28), pick
  nights 2026-06-01..2026-09-09, exclusions_v003.json (manual_runs union non_session_runs union
  uncorroborated_publication_runs) removed -- 541 published rows on 67 non-excluded nights of 70
  elapsed sessions (3 nights excluded in-window: 2026-06-26, 07-02, 07-06; DP-04 is already folded
  into manual_runs per the KT audit, so no separate removal was needed). The identical six-level
  test STEWARD_Q012_exposure.md Section 2 defines removes 24 of 541 (4.4%) -- 16 on the
  ladder/six-target test (8 no lane plan at all, all 2026-06-02; 8 missing >=1 of 6 targets), 8
  further on wrong-side-of-C_t (7) and outcome_target_invalid non-null (1) -- leaving 517
  eligible, of which 495 are LOW-or-HIGH (80 <= score < 90), 21 ELITE, 1 REF (TJX, 2026-06-11,
  79.58). Independently re-derived from the frozen parquet; matches STEWARD_Q012_exposure.md
  Section 2 exactly, row for row.
- Item (4) reconciliation -- rates confirmed, no discrepancy, no recomputation triggered. On
  Q018's own contributing-night definitions (Section 2: a contributing night carries >= 1
  eligible 80-90 pick already gradeable in all three lanes by construction of the six-level test;
  a both-band night carries >= 1 such pick in each of LOW and HIGH):

  | Rate | Measured | / 70 elapsed sessions | STEWARD_Q012_exposure.md Section 4 | Match |
  |---|---|---|---|---|
  | Contributing nights | 66 | 0.9429 | 0.9429 | exact |
  | Both-band nights | 42 | 0.6000 | 0.6000 | exact |
  | ELITE nights | 20 | 0.2857 | 0.2857 | exact |

  Per-month breakdown (LOW nights / HIGH nights / both-band nights / ELITE nights) also matches
  exactly: Jun 19/14/14/10, Jul 20/8/8/6, Aug 21/14/14/3, Sep(partial) 6/6/6/1. No difference
  found -- the Section 5 schedule dates do not move. Window 2026-09-14..2027-03-31, decision date
  Monday 2027-07-12, extension window ..2027-05-12 / decision Monday 2027-08-16, projected raw
  80th both-band pick night approximately 2027-03-25 (session 134 of 137), projected 80th P1/P3
  contributing night approximately 2027-01-22 (not binding), projected 30th post-lock
  contributing night approximately mid-November 2026 (not binding) -- all as already computed in
  DECISIONS.md's Schedule section, restated here as confirmed, not re-derived from different
  inputs.
- DP-50(a) commit sweep: not none. Several commits land inside 2026-06-01..2026-09-10 (the freeze
  as_of) touching the named files. The one that matters most for R1 item (2) is empirically
  confirmed to split the population it measures -- see Section 2 and Section 5 below. Full list
  in Section 5.

---

## 1. R1(1) -- best_timeframe distribution among eligible 80-90 picks, by band and month; B3 non-degeneracy

n = 495 (LOW 422, HIGH 73).

Overall: short 343 (69.3%) - swing 97 (19.6%) - long 55 (11.1%).

By band:

| band | short | swing | long |
|---|---|---|---|
| LOW (n=422) | 287 | 87 | 48 |
| HIGH (n=73) | 56 | 10 | 7 |

By month:

| month | short | swing | long |
|---|---|---|---|
| 2026-06 | 91 | 23 | 19 |
| 2026-07 | 101 | 33 | 14 |
| 2026-08 | 116 | 32 | 15 |
| 2026-09 (partial) | 35 | 9 | 7 |

By band and month:

| month | band | short | swing | long |
|---|---|---|---|---|
| 06 | HIGH | 22 | 7 | 3 |
| 06 | LOW | 69 | 16 | 16 |
| 07 | HIGH | 9 | 1 | 0 |
| 07 | LOW | 92 | 32 | 14 |
| 08 | HIGH | 17 | 2 | 4 |
| 08 | LOW | 99 | 30 | 11 |
| 09 | HIGH | 8 | 0 | 0 |
| 09 | LOW | 27 | 9 | 7 |

Share whose B3 fixed lane (short to day, swing to swing, long to long) differs from each fixed
lane (denominator 495): differs from day: 152/495 = 0.3071; differs from swing: 398/495 = 0.8040;
differs from long: 440/495 = 0.8889. Non-degenerate -- all three lanes appear every month and in
both bands -- but skewed short, consistent with the weekly 2026-09-12 Section 4 counts (474 short
/ 160 swing / 65 long); that count is a different population (the W20 population, not this
six-level-eligible 80-90 cohort), so the two are not directly comparable as a ratio, only as a
shared "skewed short" shape. Decides nothing (B3 descriptive).

## 2. R1(2) -- per-lane ATR distance distribution; ladder monotonicity share

ATR14 desk-computed from p001_daily_split bars dated <= t (platform atr_pct not used, PI-003).
d = dir * (T - C_t) / ATR.

17 of 495 picks (3.4%) carry a price-scale mismatch between the payload's lane-plan levels and
C_t -- see the new finding below -- and are excluded from the quartile table (included, they
only stretch the max; medians are unaffected either way). n = 478 clean:

| Lane | Level | Q1 | Median | Q3 | Min | Max |
|---|---|---|---|---|---|---|
| Day | t1 | 0.237 | 0.367 | 0.526 | 0.023 | 3.325 |
| Day | t2 | 0.410 | 0.593 | 0.859 | 0.114 | 7.903 |
| Swing | t1 | 1.139 | 1.788 | 2.707 | 0.125 | 6.328 |
| Swing | t2 | 2.449 | 3.334 | 4.369 | 0.372 | 10.395 |
| Long | t1 | 3.071 | 4.120 | 5.526 | 0.945 | 11.731 |
| Long | t2 | 5.151 | 6.367 | 8.071 | 1.906 | 16.163 |

Overlap share (does one lane's far target sit beyond the next lane's near target, in ATR
distance): day t2 >= swing t1: 12.55%; swing t2 >= long t1: 59.62%; day t2 >= long t1: 1.67%. Day
and long are cleanly separated by distance; swing and long overlap on more than half of picks --
consistent with PREREG threat 2's "lane is partly distance" framing, most acutely between swing
and long.

Ladder monotonicity -- the historical ~28% figure does not hold uniformly across this window; it
is two regimes, not one, and the split falls squarely inside the population R1 measures. On the
495 eligible picks, flattened-ladder non-monotonicity (day t1,t2 -> swing t1,t2 -> long t1,t2,
checked against the pick's own direction) is:

| Slice | n | Non-monotonic | Share |
|---|---|---|---|
| Whole window (as published) | 495 | 36 | 7.27% |
| Before _enforce_ladder_monotonic shipped (< 2026-07-06) | 140 | 36 | 25.71% |
| On/after _enforce_ladder_monotonic shipped (>= 2026-07-06) | 355 | 0 | 0.00% |

This is not a projection -- every eligible pre-ship pick and every eligible post-ship pick is
counted directly from the frozen payloads. See Section 5 for the commit and DATA_NOTES.md for the
standing note. A blended "approximately 28%" or "7.27%" figure would misstate both halves of this
window; report the two regimes, not one number, wherever this share is cited for Q018's threat-2
discussion.

New finding, not previously in DATA_NOTES: a public_payload_json.lane_plans price-scale mismatch,
distinct from PI-003. PI-003 is about the platform's own atr_pct column being computed on raw
(non-split-adjusted) bars. This is different: for 4 symbols, the lane plan's own printed price
levels (entry, stop, targets, invalidation) are on a different price scale than C_t from
prices_daily_split for the identical symbol/date -- i.e., the levels appear to have been built
from the raw (non-split-adjusted) reference price rather than the split-adjusted one:

| Symbol | Eligible LOW/HIGH picks affected | Ratio (day t1 / C_t) | Pattern |
|---|---|---|---|
| APH | 14 of 14 (100% of its picks in-window) | 2.00-2.05x | Systematic across the entire window, 2026-06-05 to 2026-08-12 |
| KLAC | 1 of 1 | 10.18x | Single night, 2026-06-05 |
| CRWD | 1 of 1 | 4.07x | Single night, 2026-06-29 |
| MNST | 1 of 1 | 2.02x | Single night, 2026-07-13 |

APH's mismatch is not episodic -- it is present on every APH pick this window carries, at a
constant ~2.0x ratio, consistent with a stock split whose adjustment the lane-plan writer's price
reference never picked up while prices_daily_split (correctly) applies it retroactively to every
historical date. This contaminates any ATR-distance or price-level computation for these symbols
(handled above by exclusion) and is invisible to the six-level eligibility test's
wrong-side-of-C_t check, because a 2x-10x larger raw-scale bullish target still sits "above" a
much smaller split-adjusted close -- it passes eligibility while not being a real, tradable
distance. Logged to DATA_NOTES.md under today's date; not investigated further here (counts-only
scope) but flagged for the Red Team / a future PI filing given it recurs identically across APH's
full history in this window, not as a one-off.

## 3. R1(3) -- share of eligible picks with >=1 lane target at/through the session t+1 official open, by lane

Per DECISIONS item 3: a counts-only fact, never entering eligibility. n = 495.

| Lane | Count | Share |
|---|---|---|
| Day | 70 | 14.14% |
| Swing | 10 | 2.02% |
| Long | 0 | 0.00% |

By band: HIGH (n=73) day 10/73 = 13.70%, swing 1/73 = 1.37%, long 0; LOW (n=422) day 60/422 =
14.22%, swing 9/422 = 2.13%, long 0. Excluding the 17 scale-mismatch rows moves day to
70/478 = 14.64% (they contribute 0 hits either way, since a doubled/10x'd target is never "at or
through" a normal-scale open) -- the finding is not an artifact of Section 2's scale issue.
Concentrated in the day lane by construction (Section 10 threat 14), essentially absent in the
long lane. 70 of 495 picks (14.1%) have their day-lane t1 or t2 already passed at the open on at
least one side.

## 4. R1(4) -- reconciliation (see Headline)

Confirmed exact match to STEWARD_Q012_exposure.md Section 4: 0.9429 / 0.6000 / 0.2857
contributing / both-band / ELITE nights per elapsed session, month-by-month identical. No
discrepancy; the 80th both-band night projection, the window end (2027-03-31), the decision date
(Monday 2027-07-12), and the DP-13 extension date (Monday 2027-08-16) all stand as DECISIONS.md
already computed them. This is expected, not a coincidence: Q018's eligible-pick test is Q012's
Funnel B test (DECISIONS.md, "Does record need a fresh exposure count? No."), so an independent
re-derivation from the same frozen parquet against the same exclusions file has no room to differ
absent a bug in one of the two computations. None found.

## 5. DP-50(a) -- platform commits, 2026-06-01..2026-09-10 (freeze as_of), touching the named areas

Git history access in this session is restricted to git log (bounded --since/--until, optionally
with a pathspec) -- git show/git diff/git diff-tree/git cat-file are blocked by this desk's own
sandbox guard for the platform repo, so no diff content was inspected, only commit metadata (SHA,
timestamp, subject). Findings below are corroborated wherever possible by direct Read of the
current file (which shows the present state, not the historical diff) and by empirical checks
against the frozen parquet (Section 2, Section 1). Timestamps are git commit timestamps
(committer-local, shown here as recorded, -05:00/CDT); they are not production write times and
are not asserted to be.

Not none. Seven commits land in-window touching the four named surveillance targets, plus
adjacent scoring/service-layer work:

| SHA | Date (local) | File(s) touched (of the named set) | Subject | Relevance |
|---|---|---|---|---|
| 5fa3db4 | 2026-07-06 14:13 | services/super_agent_select_service.py | W3: publication-time cross-lane ladder monotonicity (H4 family) | Ships _enforce_ladder_monotonic (current location :195-215). Empirically confirmed to split the population R1 measures -- 25.71% non-monotonic before, 0.00% after (Section 2). This is the single most load-bearing DP-50(a) finding for Q018: the mechanism named in threat 2 did not exist for the first 5 weeks of the very window whose "historical ~28%" figure the desk carries. |
| f718b34 | 2026-07-06 15:44 | services/super_agent_select_service.py | X4: unresolvable ladders feed the G3 degraded-batch assertion | Same-day follow-on; adds the "unresolvable, left as published, WARNING" branch the current docstring at :210-214 describes. No unresolvable case survived into the 495-pick eligible population measured here (0% non-monotonic post-ship). |
| 1765a6f | 2026-07-07 20:43 | services/sas_conviction_card.py, services/super_agent_select_models.py, services/super_agent_select_scoring.py | SAS conviction card + 80 publication floor | Introduces SuperAgentSelectConfig.publication_floor = 80.0 at super_agent_select_models.py:86-91 (current comment dates it 2026-07-07, cites docs/SAS_CONVICTION_TIER_DECISION.md, and states "only sub-80 bulls are affected -- they fall to the dark set"). Empirically checked: bullish published-row minimum score is 79.58 pre-ship (1 row, TJX, dated before this ship) and 80.14 post-ship -- i.e., the one sub-80 published row in the whole window predates the formal floor, and no sub-80 bull was published afterward either. The floor's codification lands mid-window; its effect on what got published is not measurably different before vs. after in this frozen data. Flagged per DP-50(a) regardless, since it touches the publication-predicate area named in the request. |
| a67ee72, a676e98, c619732 | 2026-07-08 12:52 / 20:49 / 23:41 | services/sas_conviction_card.py | Ladder/performance-page display commits | Display-layer only by subject line; not independently confirmed against a diff (git show/diff blocked this session). |
| a475f2b | 2026-09-05 11:08 | services/sas_conviction_card.py | Conviction card: windowed max moves + 20/40/60td lane windows | This is the commit PREREG itself already cites as "the 2026-09-05 lane-window ruling" (PREREG.md line 30, sas_conviction_card.py:194) -- already disclosed, not a new finding. Lands 5 days before the freeze as_of; fa70688 (same day, 12:04) is the exact SHA manifest_v001.platform_git_sha is pinned to, so the freeze reflects only the post-ruling state -- there is no before/after split visible inside manifest_v001 for this one (unlike ladder monotonicity, which has picks on both sides of its ship date). |
| fa70688 | 2026-09-05 12:04 | services/sas_conviction_card.py | Conviction card: resolve post-backfill display contradictions | = manifest_v001.platform_git_sha. The freeze's pinned code state. |

Also in-window, touching services/super_agent_select_service.py and/or
services/super_agent_select_scoring.py (adjacent to the publication predicate, not among the four
literally named, included for completeness): a multi-day bear/dark-lane build-out --
56d86a3/5f94594/cd68573 (2026-06-02, secular regime gates, OFF by default), a9234b8 (2026-06-28,
bear MTF technical + bull/bear/both routing), 49e050a/aa4108f/d2788b8/9be2a14/31d6418
(2026-07-02/07-03, "Bear Phase 1: dark-grade the sub-80 v2 bearish cohort" / "instrument-only dark
lane for v1-only bears"), and f94e347/d3d49bc/a3e6674/3f36900 (2026-07-05, "Phase 0.5e-h: ladder
integrity audit", precursor to 5fa3db4). No discontinuity attributable to this build-out was found
in the measured contributing/both-band/ELITE rates (Section 4 matches exactly), but
"wrong-side-target exclusion" and "cluster integrity" are exactly the mechanisms the six-level
eligibility test leans on, and this is when they were built -- named here so a future freeze that
disagrees with v001 about a bear-candidate row has a first place to look.

ai_agents/principal_agent.py (the lane-plan writer): one commit in-window -- 83b571d, 2026-07-09
18:36, "upgrading agents to gpt 5.6." This is the file containing the lines PREREG cites (:546-554
the "three meaningfully different strategies" instruction, :897-911 the deterministic fallback).
Current Read of both ranges shows text consistent with PREREG's citation. Cannot confirm from git
log alone whether the prompt text at those specific lines changed on this commit, or only a
model-version constant elsewhere in the same file -- full diff inspection (git show/git diff) is
blocked in this session for this repo. A GPT-model upgrade changes lane-plan generation behavior
even against an identical prompt, so this is flagged for the Red Team / a session with fuller repo
access to confirm one way or the other before it is treated as settled.

routers/super_agent_select.py / scripts/generate_sas_trading_guide.py (not literally named by R1,
checked for adjacency to the publication predicate): a645cb9 (2026-07-07, "Pro SAS gating: open
80-89 to Pro, lock 90+ in place" -- subscription/UI tier access, not the DB
qualified/selected_rank predicate), eb743bf/8c75eff/b24954c/15af742 (2026-07-06 to 07-09,
guide-generator versioning and the L4-trim ruling -- 8c75eff is the commit behind the 2026-07-08
ruling PREREG already cites via docs/SAS_EXIT_SCHEDULE_L4TRIM_RULING.md), ecb29c8 (2026-07-06,
"dirty-tree guard + median-with-label amendment," file not independently confirmed). None of these
appear, by subject line, to touch the qualified/selected_rank write path itself.

Action per DP-50(a): the ladder-monotonicity finding (Section 2, 5fa3db4) is the one item here
that materially changes what a column means mid-window for Q018's own population; it is now in
DATA_NOTES.md (dated entry below) ahead of the successor freeze. The publication-floor commit
(1765a6f) and the bear/dark-lane build-out are logged in the same entry for completeness even
though no measurable population effect was found. The principal_agent.py GPT-upgrade commit is
flagged as unconfirmed, needs a fuller-access follow-up -- not asserted as a feature split,
because I cannot show it touched the cited lines.

---

## Files

- This report: research/reports/STEWARD_Q018_exposure.md.
- Two dated entries added to research/data/DATA_NOTES.md (2026-09-13): (1) the
  _enforce_ladder_monotonic mid-window ship date and the measured pre/post non-monotonic share;
  (2) the public_payload_json.lane_plans price-scale mismatch (APH systematic, KLAC/CRWD/MNST
  episodic).
- No new manifest, exclusions file, or results/ directory. No controller advance -- R1 does not
  block Q018's lock (already committed) and this report builds no new freeze; R2 (successor
  freezes) remains due at the 2027-07-12 decision date.
- Analysis scripts were run from the session scratchpad, not committed to this repo.
