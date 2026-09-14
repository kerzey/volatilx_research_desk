# STEWARD_Q033_exposure.md — R1 (counts only), Q033 direction_vs_magnitude

**Request:** `research/questions/Q033_direction_vs_magnitude/PREREG.md` Section 5.3 R1, and
`DECISIONS.md` "Routed requests - data-steward - R1 (counts only) - BLOCKING FOR LOCK", routed by
the decision-maker 2026-09-14. Counts only, no outcome of any kind: no touch, no first-touch date,
no return, no excursion, no `outcome_*` column, no `sas_selection_excursion`, no
`uoa_symbol_daily.fwd_return_*`, no arm-vs-outcome cross-tab. Forward bars read only to establish
that a bar exists (gradeability/maturity accounting), never for a value. Frozen data only -
`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json` against
`research/data/exclusions_v003.json`, plus read-only git log/git show/merge-base against the
pinned platform repository - never a live query (DP-50(c)).

**Session facts, confirmed directly:** `RESEARCH_DB_URL`, `ALPACA_API_KEY` and `ALPACA_SECRET_KEY`
are all unset in this session (checked, all empty) - not needed for (a)-(e), which use frozen
Parquet only; their absence is limb (f)'s own result.

**Population:** pick nights 2026-06-01..2026-09-10 (DP-06 segment). Denominator for every rate
= elapsed sessions (calendar sessions minus holidays), exclusions not pre-removed. **Elapsed
sessions: N = 71**, reconfirmed against v001_sas_runs.parquet (71 rows) and the SPY daily-bar
calendar in manifest_prices_v001 (71 rows 2026-06-01..2026-09-10) - both agree exactly, matching
STEWARD_Q027/Q031/Q032_exposure.md.

**Nights excluded (3):** 2026-06-26 (uncorroborated_publication_runs), 2026-07-02
(manual_runs), 2026-07-06 (manual_runs) - read directly from exclusions_v003.json.
**Non-excluded nights: 68.** Identical to the Q027/Q031/Q032 population (same window, same file).

---

## Headline

**Every limb R1 asks for was independently recomputed from the raw Parquet tables (not copied),
including (b) and (c), which STEWARD_Q032_exposure.md already answered under a definition that
turns out - checked, not assumed - to be identical on this population for (b)'s arm split and (c)'s
composition.** Section 2.2's arm label is a pure function of SPY bars, so it cannot differ between
questions; Section 2.5's >=5-valid-controls clause never binds anywhere in this freeze (min pool
depth 37 at every maturity horizon tested), so Q033's stricter >=3-picks/>=5-controls funnel
collapses to the same "does the night have >=1 valid published pick" criterion Q032 used -
confirmed by independent recomputation below, not inherited.

**Limb (f) fails outright, exactly as it did for Q032 on the same day: ALPACA_API_KEY /
ALPACA_SECRET_KEY are absent from this session, so the SPY-from-2025-01-02 feasibility probe
cannot be attempted.** Per DECISIONS item 16, a failed probe with no pinned alternative defers
**P2 only** - P1 does not depend on the arm.

**All three exposure-rate floor limbs (a, b, d) clear**, on the reading consistent with DECISIONS
item 6's own registered method (remove freeze-horizon censoring by restricting numerator and
denominator to the maximal sub-period that can mature to t+40 inside this freeze; do not invent a
cap where no independently-measured slower number exists). **One raw reading of limb (d)
(rarer-arm gate-counting episodes) is SHORT if computed on the full 71-session denominator with
strict t+40 maturity enforced** - this is flagged explicitly below because it is the one place a
different, defensible reading of the same counts changes the branch, and it is the coordinator's
call, not mine, to fix which reading governs. My own recommendation, and the reading I use for the
headline branch, is stated with its reasoning below.

**Branch fired (recommended reading): P2 deferred (H-074 credentials re-check trigger); P1 locks
alone.** Window end recomputes to a materially shorter provisional figure than the draft's 158
sessions - see "Window-end consequence" below - because the measured HOSTILE-arm richness is far
above the old 0.20 placeholder, the same finding STEWARD_Q032_exposure.md's re-check note flagged
for its sibling question.

**Gate limb table** (re-solved thresholds, 205 admissible elapsed sessions, DECISIONS Correction 3):

| limb | measure | floor | measured | pass/short |
|---|---|---:|---:|---|
| (a) total contributing nights/session | min(r40 over t+40-evaluable sub-period, 0.6620) | >= 0.40 | **0.6620** (cap binds; r40 = 0.8710) | **PASS** |
| (b) rarer-arm (HOSTILE) contributing nights/session | subperiod-restricted, item-6 method | >= 0.10 | **0.4194** (13/31 sub-period) | **PASS** |
| (b) same, full-window/eligible-pick basis (no maturity check) | -- | -- | 0.3099 (22/71) | PASS |
| (b) same, full-window/strict-t+40-maturity basis | -- | -- | 0.1831 (13/71) | PASS |
| (d) rarer-arm gate-counting episodes/session | subperiod-restricted, item-6 method | >= 0.025 | **0.0323** (1/31 sub-period) | **PASS** |
| (d) same, full-window/eligible-pick basis | -- | -- | 0.0563 (4/71) | PASS |
| (d) same, full-window/strict-t+40-maturity basis | -- | -- | **0.0141 (1/71)** | **SHORT** (needs 355 sessions - exceeds the 205-session ceiling outright) |
| (f) SPY-history feasibility probe | credential presence + retrieval | must succeed | -- | **FAIL - credentials absent, probe not attempted** |

Every "PASS" row above except the flagged strict-full-window row for (d) agrees; only that one
literal, freeze-horizon-artifact reading disagrees, and it disagrees by enough to matter (see
"Which reading governs" below).

---

## (a) The Section 2.4 funnel and the contributing-night rate, three ways - independently recomputed

**Funnel, whole window, non-excluded nights (550 published rows on 68 nights):**

| reason | rows |
|---|---:|
| valid | 514 |
| split-scale-screen | 19 |
| no-lane_plans (all on 2026-06-02, analysis_status="disabled") | 8 |
| d_L3 bound [0.25,10] | 7 |
| wrong-side (d_L3 <= 0) | 2 |
| **total** | **550** |

**Reconciles bit-for-bit with STEWARD_Q032_exposure.md's independent count** (550 / 514 / 19 / 8
/ 7 / 2), computed here from v001_sas_candidates.parquet and p001_daily_split.parquet with the
desk's own ATR14 and C_t (never atr_pct/spot_close - PI-003), not copied. By month:

| month | valid | d_L3 bound | no lane_plans | split-scale | wrong-side |
|---|---:|---:|---:|---:|---:|
| 2026-06 | 134 | 6 | 8 | 11 | 1 |
| 2026-07 | 155 | 0 | 0 | 3 | 1 |
| 2026-08 | 164 | 1 | 0 | 5 | 0 |
| 2026-09 (partial, through 09-10) | 61 | 0 | 0 | 0 | 0 |

**Only one non-excluded night has zero valid picks: 2026-06-02** (all 8 published rows lack
lane_plans). Every other non-excluded night has >=4 valid picks (distribution: 4x3, 5x1, 6x1,
7x17, 8x34, 9x10, 10x1 - no night sits between 1 and 3), so the >=3-picks floor and the
>=1-pick floor Q006/Q032 use are the same test on this population.

**Control-pool depth, independently recomputed at both the t+20 and t+40 gradeability requirement:
min 37, never below 5 or even 10, at every night tested** (28 subperiod nights checked at t+40
gradeability: min 37, median 43.0, max 60; a further spot-check of 40 post-subperiod nights at
the >=60-prior-bar screen: min 49, median 55, max 60). **The >=5-controls clause costs zero nights
everywhere in this freeze** - confirming, not assuming, the STEWARD_Q031_exposure.md finding under
Q033's own stricter rule and at the t+40 horizon Q031 did not test.

**t+40-evaluable sub-period, calendar-derived:** last pick night whose t+40 <= 2026-09-10 (the
freeze's own last date) is **2026-07-15** - 31 elapsed sessions (2026-06-01..2026-07-15), reproduced
independently and agreeing with STEWARD_Q032_exposure.md's figure.

| form | numerator | denominator | rate |
|---|---:|---:|---:|
| **(i) t+40-evaluable sub-period** (both num & denom over 2026-06-01..2026-07-15) | **27** (28 non-excluded sub-period nights; only 2026-06-02 fails) | 31 | **0.8710** |
| **(ii) t+20-comparable** (Q031's series-B construction, full window) | **47** | 71 | **0.6620** - reconfirmed bit-for-bit against STEWARD_Q031_exposure.md, under Q033's own Section 2.5 rule (verified identical to Q031's rule, not borrowed) |
| **(iii) full-denominator t+40** | 27 | 71 | **0.3803** |

**Scheduling rate per DECISIONS item 6: min(0.8710, 0.6620) = 0.6620.** The cap binds - no date is
ever computed from the faster sub-period rate.

## (b) The Section 2.2 arm split under the SMA50-only trend variant - independently recomputed

UP iff close_t > SMA50_t; vol_t by expanding-window terciles of 20-session annualised SPY
rvol over every SPY session dated <= t in this freeze (no >=250-session floor - the proxy, not
the registered rule; see (c)). BENIGN = UP and vol in {LOW,MID}; HOSTILE otherwise. **Computed
directly from p001_daily_split.parquet SPY rows, not copied from STEWARD_Q032_exposure.md.**

**Nights per arm (68 non-excluded): BENIGN 46 (67.6%), HOSTILE 22 (32.4%) - bit-for-bit identical
to STEWARD_Q032_exposure.md**, confirming (b) transfers to Q033 as R1 permitted. HOSTILE is the
rarer arm and, per Section 5.1's registered bound, the SMA50-only HOSTILE count is a **lower bound**
on true HOSTILE exposure (adding SMA50 > SMA200 can only move UP-classified nights out of UP,
never back in).

**Gate-counting tape-episodes** (71-session full sequence resolves into 8 episodes, identical
boundaries to STEWARD_Q032_exposure.md, independently reproduced from the SPY series alone):

| arm | start | end | length (sessions) | contributing nights (eligible-pick basis) | contributing nights (t+40-matured basis) |
|---|---|---|---:|---:|---:|
| BENIGN | 2026-06-01 | 2026-06-10 | 8 | 7 | 7 |
| HOSTILE | 2026-06-11 | 2026-07-06 | 16 | 13 | 13 |
| BENIGN | 2026-07-07 | 2026-07-16 | 8 | 8 | 7 |
| HOSTILE | 2026-07-17 | 2026-07-20 | 2 | 2 | 0 |
| BENIGN | 2026-07-21 | 2026-07-22 | 2 | 2 | 0 |
| HOSTILE | 2026-07-23 | 2026-07-30 | 6 | 6 | 0 |
| BENIGN | 2026-07-31 | 2026-09-09 | 28 | 28 | 0 |
| HOSTILE | 2026-09-10 | 2026-09-10 | 1 | 1 | 0 |

**"Contributing nights" recomputed under Q033's own Section 2.5 rule (>=3 valid picks, each >=5
controls, matured to t+40) - reconciles exactly with the counts above, verified pick-by-pick, not
assumed transferable.** HOSTILE rarer-arm contributing nights, t+40-matured basis: **13** (episode 2
only - the only HOSTILE episode whose sessions fall inside the 2026-06-01..2026-07-15 maturity
sub-period). HOSTILE rarer-arm contributing nights, eligible-pick basis (no maturity check - the
reading that removes freeze-horizon censoring the same way Section 5.1's r40 does): **22** - all
non-excluded HOSTILE nights bar none (the single zero-valid-pick night, 2026-06-02, is a BENIGN
night).

**Rarer-arm gate-counting episodes** (an episode counts if it contains >=1 contributing night):
t+40-matured basis -> **1 of 4 HOSTILE episodes** (only episode 2); eligible-pick basis -> **4 of 4**.

## (c) Nine-cell composition; first session with >=250 prior SPY sessions - independently recomputed

**First session with >=250 prior SPY sessions in manifest_prices_v001: NEVER.** The freeze holds
153 total SPY daily bars (2026-02-02..2026-09-10); the expanding count of valid 20-session rvol
observations reaches only **133** by the last date (independently recomputed - matches
STEWARD_Q032_exposure.md's 133 exactly). Roughly another 117 sessions of prior SPY history (to
about mid-2025) are needed before the registered tercile calibration is satisfiable anywhere - this
is exactly what R2(i)'s SPY-from-2025-01-02 requirement is sized to fix, and exactly why the
**strict Section 2.2 legality rate on this freeze is 0/71 in every form**, a data-availability fact
stated at lock (Section 10 threat 11), not a screening failure, and not evidence against the
partition.

**Composition, non-excluded 68 nights, SMA50-only proxy (six-cell - no SMA200 exists in this
freeze, so only UP/NOTUP is observable):**

| trend | vol | nights |
|---|---|---:|
| UP | LOW | 16 |
| UP | MID | 30 |
| UP | HIGH | 13 |
| NOTUP | LOW | 8 |
| NOTUP | MID | 1 |
| NOTUP | HIGH | 0 |

**Bit-for-bit identical to STEWARD_Q032_exposure.md**, independently reproduced here from the raw
SPY series. Only UP/MID (30) clears the eventual >=20-contributing-night suppression floor;
informational only - Section 4.3's suppression list is fixed at lock (DECISIONS item 10).

## (d) d_L3 in [0.25,10] exclusions, and the d_L3 < 0.5 share - this question's own

**Picks excluded by the d_L3 in [0.25,10] validity bound: 7** (of 550 published rows on
non-excluded nights) - see (a)'s funnel table.

**Of the 514 valid picks (i.e. those that already clear every other screen, including the
[0.25,10] bound itself), the number with d_L3 < 0.5: 20 (3.89%).** This is the direct read on
Section 10 threat 6 / DECISIONS item 21 / Correction 5: how often the printed swing target sits
inside Q033's registered +/-0.5 ATR direction band, i.e. how often a_p and m_p are structurally
close to the same indicator. **A small, non-trivial share (roughly 1 in 26 valid picks) - reported
as a fact about the ladder (PI-009/H-053), never a licence to move the band** (DECISIONS item 21
already forecloses that).

## (e) DP-50(a)/(b) commit sweep since fa70688; v1.7 schedule - reconfirmed independently

fa70688bc252d14f8d67e371afafc194731c324e reconfirmed as an ancestor of HEAD
(git merge-base --is-ancestor, read-only). **HEAD is unchanged at d19c9a9** - the same commit
STEWARD_Q027/Q031/Q032_exposure.md measured, all on 2026-09-14; **no new commits exist since any
of those sweeps.** The 4 commits between fa70688 and HEAD (2d5776c, 4775e49, 22a2e1b,
d19c9a9) touch none of services/super_agent_select_scoring.py,
services/super_agent_select_models.py, services/sas_conviction_card.py, or
services/market_regime/scorer.py - reconfirmed with git log --oneline -1 -- path on each:

| file | last commit touching it | date | before/after fa70688 (2026-09-05) |
|---|---|---|---|
| services/super_agent_select_scoring.py | 1765a6f | 2026-07-07 | before |
| services/sas_conviction_card.py | fa70688 itself | 2026-09-05 | at the pin |
| services/market_regime/scorer.py | bae77e7 | 2026-06-08 | before |
| docs/SAS_SCORING_RESEARCH_PLAN.md | f06134a | 2026-09-03 | before |

**Answer: NONE.** No weight, timeframe multiplier, qualification_threshold, publication_floor,
bear_publish_threshold, max_output_cap, min_completeness, ATR-elite cap, GEX offset, scoring
enable-flag, or lane-plan-writer change has landed since fa70688.

**v1.7 schedule check, extended to Q033's own admissible window (2026-09-15..2027-08-23):**
docs/SAS_SCORING_RESEARCH_PLAN.md unchanged since 2026-09-03 (before fa70688), still headed
"Status: PROPOSAL... Owner sign-off required before any workstream starts," phases in relative
weeks with no calendar anchor, no commit anywhere showing the workstream has started. **No v1.7
promotion is scheduled inside 2026-09-15..2027-08-23, or anywhere else**, because no start date
exists to count weeks from. Stated as an absence of a schedule, to be rechecked at every future
freeze (Section 5.3 R2(vii), DECISIONS item 8's eval.py deadline of 2027-04-05).

## (f) SPY-history feasibility probe - the lock-gate limb

**Result: FAIL.** ALPACA_API_KEY and ALPACA_SECRET_KEY are both unset in this desk session -
confirmed directly (both empty). RESEARCH_DB_URL is also unset, not needed for this limb. **No
SPY bar retrieval was attempted** - nothing to attempt without credentials, and per Rule 1 the desk
does not look for or request any credential beyond the named research ones. Identical finding, same
day, to STEWARD_Q032_exposure.md's limb (g) and to Q030/H-074.

---

## Which reading governs limb (d) - flagged for the coordinator, not decided here

Two of the three exposure-rate floor limbs (a, b) clear under every reading tested; **limb (d)
(rarer-arm gate-counting episodes) clears under two of three readings and is short under the
third**:

1. **Subperiod-restricted (numerator and denominator both over the 31-session t+40-evaluable
   sub-period)** - the literal method DECISIONS item 6 already registers for limb (a)'s own rate,
   applied here to the arm-specific count for the first time: **1 qualifying episode / 31 sessions =
   0.0323 - PASS.**
2. **Eligible-pick basis (full 71-session denominator, maturity not checked)** - the reading
   STEWARD_Q032_exposure.md reported for the same limb on its own question: **4/71 = 0.0563 -
   PASS.**
3. **Strict (full 71-session denominator, t+40 maturity enforced literally)** - the only reading
   under which an episode must have already matured inside this short historical freeze to count
   at all: **1/71 = 0.0141 - SHORT**, and by enough that it matters: at this rate, floor D would need
   **355 sessions**, which exceeds even the DP-13-extended ceiling (188 sessions) and the 205-session
   admissible ceiling outright (projected roughly 2028-02-07, versus the latest admissible window
   end of roughly 2027-07-09).

**Reading 3 is not a measurement of a slower true rate; it is a ceiling effect of this freeze's own
horizon** - no freeze shorter than roughly 40 plus (5 times a typical HOSTILE-episode gap) sessions
can ever show 5 matured rarer-arm episodes, no matter how rich the true HOSTILE rate is, because
maturity alone consumes the first 40 of this freeze's 71 sessions and only one HOSTILE episode is
old enough to have cleared that bar yet. That is exactly the freeze-horizon-censoring artifact
DECISIONS item 6 names and removes for limb (a)'s own rate ("only freeze-horizon censoring is
removed, and only because it cannot occur inside the registered window - R2 delivers t+40 bars for
every in-window night"); the same reasoning applies unchanged to limb (d), and reading 3 is not
what item 6's method implies if extended consistently. **I use reading 1 for the headline branch
below because it is the already-registered method applied without alteration, not a new
invention** - but I am reporting, not deciding, and the coordinator's ruling on whether item 6's
method extends to limb (d) is what actually fixes the branch.

## Window-end consequence (informational - not this report's decision to make)

If the measured HOSTILE-arm rate replaces Section 5.1's 0.20 placeholder, floor B (>=20 rarer-arm
contributing nights) projects to bind far earlier than the draft assumed - at the subperiod rate
(0.4194/session), session 48 (~2026-11-19); even at the most conservative full-window/strict
reading (0.1831/session), session 110 (~2027-02-22) - both well before floor A (>=80 total
contributing nights, 0.6620/session) binds at session 121 (~2027-03-09). **Floor A becomes the
binding floor, not floor B**, the same reversal STEWARD_Q032_exposure.md's re-check note flagged
for its sibling question. Under every reading of limb (d) except the strict one, floor D
(session ~65-89) also clears before floor A. **Recomputed window end (all readings but the strict
one): 121 sessions (2026-09-15..2027-03-09), decision date roughly 2027-05-17 - about five to six
weeks earlier than the draft's provisional 2027-07-12**, moving out relative to nothing locked
(Section 5.2's 158 was always provisional) and not a violation of "out only, never in" (DP-45),
since no window has been locked yet. This is stated for the registrar's `record` step; this report
does not recompute or apply Section 5.2's schedule.

---

## What this does and does not decide

This is a counts-only exposure measurement. No touch rate, return, excursion, plan result, or
arm-versus-outcome relationship appears anywhere above. Limbs (a)-(e) were independently
recomputed from v001_sas_candidates.parquet, p001_daily_split.parquet, v001_sas_runs.parquet
and the read-only platform repository - (b) and (c) reconcile bit-for-bit with
STEWARD_Q032_exposure.md's independent count, confirming rather than assuming they transfer to
Q033's stricter funnel; (a), (d) and (e) are measured fresh under Q033's own rule. **Limb (f) is
short - credentials absent, probe not attempted, no pinned alternative exists - and per DECISIONS
item 16 that defers P2 alone, with the H-074 re-check trigger, while P1 does not depend on the
arm.** On the floor-rate limbs, reading 1 (subperiod-restricted, DECISIONS item 6's own registered
method) clears all three; the coordinator's ruling on whether that method extends to limb (d) is
what fixes whether the branch is **P2 deferred / P1 locks alone** (my recommended reading) or
**Q033 DEFERRED in full** (the strict literal reading). The Registrar/Decision-maker applies
whichever ruling holds and locks or defers the file; the Data Steward does not decide that step and
does not advance the controller under this protocol.
