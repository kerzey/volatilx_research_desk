# STEWARD_Q032_exposure.md - R1 (counts only), Q032 regime_conditionality

**Request:** research/questions/Q032_regime_conditionality/PREREG.md Section 5.3 R1, DECISIONS.md
"Routed requests - data-steward - R1 (counts only) - BLOCKING FOR LOCK", routed by the
decision-maker 2026-09-14. Counts only, no outcome of any kind: no touch, no first-touch date, no
return, no excursion, no outcome_* column, no sas_selection_excursion, no
uoa_symbol_daily.fwd_return_*, no arm-vs-outcome cross-tab. Forward bars read only to establish
that a bar exists. Frozen data only - research/data/manifest_v001.json plus
research/data/manifest_prices_v001.json against research/data/exclusions_v003.json, plus
read-only git log, git show, merge-base against the pinned, read-only platform repository -
never a live query (DP-50(c)). Both RESEARCH_DB_URL and ALPACA_API_KEY and ALPACA_SECRET_KEY
are unset in this session - not needed for (a)-(f), which use frozen data and the read-only repo
only; their absence is itself the result of limb (g), reported below.

**Population:** pick nights 2026-06-01..2026-09-10 (DP-06 segment; the arm is a 16:05
property with no outcome attached, so the widest legal span is used, per R1 own preamble).
Denominator for every rate = elapsed sessions, exclusions not pre-removed
(Q019/Q022/Q023/Q027/Q031 convention).

**Elapsed sessions in window: N = 71**, reconfirmed against v001_sas_runs.parquet (71 rows) and
the SPY daily-bar calendar in manifest_prices_v001 - both agree exactly, matching
STEWARD_Q027_exposure.md / STEWARD_Q031_exposure.md.

**Nights excluded from the population (3):** 2026-06-26 (uncorroborated_publication_runs),
2026-07-02 (manual_runs), 2026-07-06 (manual_runs). DP-04 late-finished_at check re-run
independently (every in-window sas_runs.finished_at vs. the next session ~09:30 ET open):
**0** incremental nights fail - 2026-07-06 is already excluded via manual_runs. **Non-excluded
nights: 68.** Identical to the Q027/Q031 population (same window, same criteria), reconfirmed here
independently, not copied.

---

## Headline

**Q032 does not lock. Limb (g) fails outright - ALPACA_API_KEY / ALPACA_SECRET_KEY are absent
from this session, so the SPY-from-2025-01-02 feasibility probe cannot even be attempted - and per
PREREG Section 5.3 R1(g) / DECISIONS item 12, a failed probe with no pinned alternative is a
DEFERRED-at-lock ground on its own, independent of limbs (a)-(f).** Q032 goes to
research/questions/DEFERRED.md on that ground; the H-074 credentials trigger is the re-check
condition, exactly as it was for Q030.

**The other three counted limbs are reported in full below because R1 asks for them regardless, and
because they matter for the re-check.** Two headline findings, both load-bearing:

1. **Under the literal Section 2.2 legality rule, the contributing-night rate in this freeze is 0/71
   in every form.** No night in manifest_prices_v001 reaches the required >=250 prior SPY sessions
   for the volatility tercile - the freeze own last date (2026-09-10) carries only **133** prior
   rvol20 observations (see (c)). This is a data-availability fact, not a screening failure, and
   it is exactly what R2(i) SPY-from-2025-01-02 requirement exists to fix for the real study
   window (2026-09-15 onward). It is also exactly why limb (g) - not (a)-(f) - is the ground that
   actually stops this lock: even a perfect (a)-(f) reading cannot substitute for real SPY history.
2. **On the SMA50-only registered bound (Section 5.1, DECISIONS item 12) - explicitly NOT
   Section-2.2-legal, used only because R1(b)/(c) ask for it as a planning proxy - limbs (a)/(b)/(c)
   numerically clear the re-solved lock thresholds**, and the rarer arm (HOSTILE) is measured richer
   than the old placeholder assumed, which **moves the schedule binding floor from B to A** if the
   question is ever re-attempted with real SPY history (see (a) and the Re-check note). This is
   reported for the re-check, not as a basis for locking now.

**Gate limb table (re-solved thresholds; see (a)-(g) for derivations):**

| limb | measure | floor | measured (SMA50-only proxy) | measured (strict Section 2.2 legality) | pass/short |
|---|---|---:|---:|---:|---|
| (a) total contributing nights/session | scheduling rate, min(r40, 0.6620) | >= 0.39 (re-solved; DECISIONS states 0.40) | **0.6620** | **0.0000** | proxy: PASS - strict: SHORT |
| (b) rarer-arm (HOSTILE) contributing nights/session | | >= 0.10 (re-solved 0.097) | **0.3099** | **0.0000** | proxy: PASS - strict: SHORT |
| (b) rarer-arm gate-counting episodes/session | | >= 0.025 (re-solved 0.0243) | **0.0563** (unmatured basis) / **0.0141** (t+40-matured basis) | **0.0000** | proxy: PASS (unmatured) / SHORT (t+40-matured) - strict: SHORT |
| (g) SPY-history feasibility probe | credential presence + retrieval | must succeed | -- | -- | **FAIL - credentials absent, probe not attempted** |

**Branch fired: DEFERRED (limb (g)), per PREREG Section 5.3 R1 / DECISIONS item 12 / item 15.**
Re-check trigger: ALPACA_API_KEY / ALPACA_SECRET_KEY present in a future desk session AND SPY
split-adjusted daily bars from 2025-01-02 retrievable (the H-074 trigger, shared with Q030). A
second, narrower trigger from (a)/(b) is recorded for that re-check below.


---

## (a) The Section 2.5/2.6 funnel and the contributing-night rate, three ways

**Strict Section 2.2 legality (the literal registered rule): 0/71 in all three forms.** A legal
Section 2.2 arm label requires >=250 prior SPY sessions in the pinned freeze for the volatility
tercile (Section 2.2). manifest_prices_v001 SPY series runs 2026-02-02..2026-09-10 (153 rows);
the expanding count of computable rvol20 observations reaches only **133** by the freeze last
date (see (c)). No night in the 2026-06-01..2026-09-10 window - nor any night that could exist in
this freeze - clears 250. So under the rule as written, the contributing-night rate is 0 in every
sub-form below, for a data-availability reason stated at lock (Section 5.1, Section 10 threat 11),
not a screening failure.

**SMA50-only proxy (Section 5.1 registered one-sided bound; NOT Section-2.2-legal; substitutes
SMA50-only trend and an expanding-window volatility tercile computed on whatever history the freeze
holds, explicitly short of 250 sessions everywhere) - used only because R1(b)/(c) ask for it, and
reused here for comparability:**

The published-pick funnel underneath (direction screen, >=60-prior-bar screen, null-ladder,
wrong-side, split-scale-payload, d_L3 bound) was **independently recomputed** from
v001_sas_candidates.parquet and p001_daily_split.parquet (own ATR14, C_t, never atr_pct /
spot_close - PI-003), not copied from STEWARD_Q027_exposure.md / STEWARD_Q031_exposure.md.
Published rows on the 68 non-excluded nights: **550** (reconciles exactly with the Q027 figure of
550). Reason breakdown: valid 514, split-scale-screen 19, no-lane_plans 8 (all on 2026-06-02, the
analysis_status="disabled" signature), d_L3 bound 7, wrong-side 2. **Only one non-excluded night
has zero valid picks: 2026-06-02** - reconfirms the identical Q027/Q031 finding independently.
Control pool depth never binds (>=37 every night, see (e)), so "at least 1 eligible pick with at
least 3 valid controls" is satisfied whenever the night has >=1 valid pick.

| form | definition | numerator | denominator | rate |
|---|---|---:|---:|---:|
| **(i) t+40-evaluable sub-period** | num and denom both over the maximal stretch whose nights grade to t+40 on this freeze - **last pick night 2026-07-15** (calendar-derived: session index + 40 <= last freeze date 2026-09-10) | 27 (of 28 non-excluded nights in that stretch; only 2026-06-02 fails) | 31 elapsed sessions (2026-06-01..2026-07-15) | **0.8710** |
| **(ii) t+20-comparable** | numerator = nights maturing to t+20 with >=1 valid pick (last matured night 2026-08-12), denominator = full 71-session window - **the Q031-comparable construction** | 47 | 71 | **0.6620** - bit-for-bit the same as the Q031 report 47/71, confirmed not corrected |
| **(iii) full-denominator t+40** | numerator = (i) 27, denominator = full 71-session window | 27 | 71 | **0.3803** |

**Scheduling rate per DECISIONS item 3: min(r40, 0.6620) = min(0.8710, 0.6620) = 0.6620.** The cap
binds - the desk own measured published-pick number is the slower of the two, so no date is ever
computed from the faster sub-period rate.


---

## (b) SMA50-only arm split, rarer arm, gate-counting tape-episodes

UP iff close_t > SMA50_t (SMA50 first computable 2026-04-14, well before the window - no
in-window night lacks a trend read). vol_t by expanding-window terciles of 20-session annualised
rvol over every SPY session dated <= t **in this freeze** (first rvol20 computable 2026-03-03) -
**this is the proxy, not the registered >=250-session rule** (see (a)/(c)). BENIGN = UP AND vol IN
{LOW, MID}; HOSTILE otherwise.

**Nights per arm (68 non-excluded):**

| arm | nights | share |
|---|---:|---:|
| BENIGN | 46 | 67.6% |
| **HOSTILE (rarer arm)** | **22** | 32.4% |

Bound direction, as Section 5.1 registers it: SMA50-only HOSTILE is a **lower bound** on true
HOSTILE exposure (adding SMA50 > SMA200 can only move UP-classified nights into HOSTILE, never the
reverse); SMA50-only BENIGN is an **upper bound** on true BENIGN. HOSTILE is the rarer arm and it is
the lower-bounded one - the conservative direction for the floor that binds on it.

**Gate-counting tape-episodes** (maximal run of consecutive *sessions* sharing an arm label; an
excluded night does not break a run, only a session carrying the opposite label does; counts if it
contains >=1 contributing night):

Full 71-session sequence resolves into **8 episodes** total:

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


---

## (c) Nine-cell trend x vol composition; first session with >=250 prior SPY sessions

**First session with >=250 prior SPY sessions in manifest_prices_v001: NEVER.** The freeze holds
153 total SPY daily bars (2026-02-02..2026-09-10); the expanding count of valid rvol20
observations reaches only **133** by the last date. The freeze would need to extend roughly another
117 trading sessions further back (to about mid-2025) before the tercile calibration own floor is
satisfiable anywhere - which is exactly the span R2(i) 2025-01-02 start is sized to cover. This is
the single loudest, most concrete confirmation that the registered Section 2.2 arm cannot be legally
assigned on any data the desk holds today.

**Composition, non-excluded 68 nights, SMA50-only proxy** (only two trend states are observable -
UP/NOTUP - because SMA200 does not exist anywhere in this freeze; a true nine-cell read needs
SMA50 > SMA200, unavailable, so this is necessarily a six-cell proxy table, not the registered
nine-cell one):

| trend | vol | nights |
|---|---|---:|
| UP | LOW | 16 |
| UP | MID | 30 |
| UP | HIGH | 13 |
| NOTUP | LOW | 8 |
| NOTUP | MID | 1 |
| NOTUP | HIGH | 0 |

No cell clears the eventual >=20-contributing-night suppression floor except UP/MID (30) and, close
behind, UP/LOW (16) - informational only; Section 4.3 suppression list is fixed at lock and not
reopened by this reading (DECISIONS item 7).

## (d) SMA50-only arm vs platform-label (C1) agreement; Section 2.3 legality failures

**Section 2.3 legality test** (v1.2 row, trading_date = t, market_regime not unknown,
data_quality not insufficient, created_at date = trading_date, created_at <= that night own
sas_runs.finished_at), run against v001_market_regime.parquet:

| reason | nights (of 68 non-excluded) |
|---|---:|
| legal | 63 |
| created_at on wrong date (fails the timestamp test) | 5 |

Zero nights fail on unknown/insufficient grounds or a missing v1.2 row in this window - the same
C1-is-nearly-always-legal pattern STEWARD_Q023_exposure.md reports.

**Agreement, on the 63 nights carrying both a proxy arm label and a legal C1 label** (STRONG iff
market_regime equals strongly_bullish, else NOTSTRONG):

| | C1 = NOTSTRONG | C1 = STRONG |
|---|---:|---:|
| **arm = BENIGN** | 3 | 38 |
| **arm = HOSTILE** | 11 | 11 |

**Agreement rate (BENIGN-STRONG, HOSTILE-NOTSTRONG paired): 49/63 = 77.8%.** This is meaningfully
below the two-definitions-are-the-same-variable reading: the platform label splits the HOSTILE-arm
nights exactly 50/50 (11 STRONG, 11 NOTSTRONG), so C1 is carrying real, non-redundant information
relative to the bar-only partition on this population - Section 10 threat 2 concern is not fully
borne out, though the two are still correlated (BENIGN nights are heavily STRONG, 38/46).


---

## (e) Matched-control pool depth; CTRA scan - confirmed, not corrected

**Control pool depth** (unpublished sas_candidates rows, >=60 prior split-adjusted daily bars,
same-night, no direction filter - Q006 Section 3 B1 construction), independently recomputed across
all 68 non-excluded nights: **min 37, median 53, max 60, mean 50.8.** Nights with pool depth <10:
**0**; <5: **0**; <3: **0**. This **confirms** the STEWARD_Q031_exposure.md figures (min 37, median
54, max 60, mean 49.8) to within the expected rounding from a slightly broader population (all 68
non-excluded nights here vs the 48 t+20-matured nights there) - no disagreement, no DP-50(a)
finding.

**CTRA truncated-history scan**, reproduced independently: last daily bar in
manifest_prices_v001 **2026-05-06**; the symbol keeps appearing as a sas_candidates row (never
qualified) through the end of the window. It clears the >=60-prior-bar screen at every appearance
but fails gradeability the moment a matured night needs its forward bar. Appearances in-window: 19
dates (2026-06-04, 06-05, 06-11, 06-17, 06-25, 08-20, 08-21, 08-25, 08-26, 08-27, 08-28, 08-31,
09-01, 09-02, 09-03, 09-04, 09-08, 09-09, 09-10). The 5 pre-2026-08-12 (t+20-matured) appearances
match the STEWARD_Q027_exposure.md 5 dropped CTRA rows exactly - **confirmed**, not corrected. No
other symbol shows this signature in-window.

## (f) DP-50(a)/(b) commit sweep since fa70688; v1.7 schedule

fa70688bc252d14f8d67e371afafc194731c324e reconfirmed an ancestor of HEAD
(d19c9a945418b09773baffac37f8d723c8a90a9a, via git merge-base --is-ancestor, read-only). **HEAD
is unchanged at d19c9a9** - the same commit STEWARD_Q027_exposure.md and
STEWARD_Q031_exposure.md measured on 2026-09-14. **No new commits exist since those sweeps.** The 4
commits between fa70688 and HEAD (2d5776c, 4775e49, 22a2e1b, d19c9a9) touch none of
services/super_agent_select_scoring.py, services/super_agent_select_models.py,
services/sas_conviction_card.py, or services/market_regime/scorer.py - reconfirmed with
git log --oneline -1 -- path on each of the four named files:

| file | last commit touching it | date | before/after fa70688 (2026-09-05) |
|---|---|---|---|
| services/super_agent_select_scoring.py | 1765a6f (SAS conviction card + 80 publication floor) | 2026-07-07 | before |
| services/sas_conviction_card.py | fa70688 itself | 2026-09-05 | at the pin |
| services/market_regime/scorer.py (C1 only) | bae77e7 (Regime v1.2: weekly_trend graduated scaling) | 2026-06-08 | before |
| docs/SAS_SCORING_RESEARCH_PLAN.md | f06134a | 2026-09-03 | before |

**Answer: NONE.** No weight, timeframe multiplier, qualification_threshold, publication_floor,
bear_publish_threshold, max_output_cap, min_completeness, ATR-elite cap, GEX offset, scoring
enable-flag, lane-plan writer, or market_regime/scorer.py change has landed since fa70688.

**Data-level config_json cross-check** (independently recomputed, not copied): publication_floor
null to 80.0 effective the 2026-07-08 run (46 of 71 in-window runs at 80.0); bear_publish_threshold
null to 80.0 effective the 2026-06-29 run (52 of 71 at 80.0). Both already logged in DATA_NOTES.md
(ladder-monotonicity entry, 2026-09-13); per DECISIONS item 9 these gate publication, not scoring,
and do not trigger a window split. No new DATA_NOTES.md entry needed.

**v1.7 schedule check:** docs/SAS_SCORING_RESEARCH_PLAN.md is unchanged since 2026-09-03 (before
fa70688), still headed Status PROPOSAL, not a decision record, Owner sign-off required before
any workstream starts, phases in relative weeks with no calendar anchor, and no commit anywhere in
the repo shows the workstream has started. **No v1.7 promotion is scheduled inside
2026-09-15..2027-07-09** (this question own re-solved admissible span) **or anywhere else**,
because no start date exists to count weeks from. Stated as an absence of a schedule, to be
rechecked at every future freeze, not assumed clear permanently (same caveat the
STEWARD_Q031_exposure.md sweep records).

## (g) SPY-history feasibility probe - the lock-gate limb

**Result: FAIL. ALPACA_API_KEY and ALPACA_SECRET_KEY are both unset in this desk session** -
confirmed directly (both empty). RESEARCH_DB_URL is also unset, though it is not needed for this
limb (the probe is a market-data call, not a database read). **No SPY bar retrieval was attempted**
- there is nothing to attempt without credentials, and per Rule 1 and the guard-hook policy the desk
does not look for or request any credential beyond the named research ones.

**What the probe would need, stated for whoever runs it next:** both Alpaca market-data environment
variables populated in the desk session (market-data endpoints only - the trading endpoints are
blocked outright by policy regardless of credential validity), then a single daily-bars call for
SPY, split-adjusted, start 2025-01-02 through the freeze end, feed sip, checked only for **coverage
and first/last bar date**, no values beyond that (per R1(g) own scope: coverage and first/last
bar date only, no values needed beyond that). This is exactly the H-074 / Q030 blocker
(research/questions/DEFERRED.md, Q030, 2026-09-14): the same absent pair stopped that question
freeze attempt, and it stops this lock-gate limb the same way, before eight months are spent finding
out at the 2027 decision pass.


---

## Re-check note (for whoever revisits this after credentials are restored)

If ALPACA_API_KEY and ALPACA_SECRET_KEY become available and R2(i) delivers true SPY history from
2025-01-02, two things from this report change the provisional schedule that the PREREG/DECISIONS
carry today, worth flagging now rather than re-discovering later:

- **The measured HOSTILE-arm rate (0.3099/session, proxy) is far above the Section 5.1 placeholder
  (0.20 x 0.6620 = 0.132/session) it replaces.** At the measured rate, floor B (20 rarer-arm
  contributing nights) projects to bind at only **~65 sessions** (~2026-12-15) and floor D (5
  rarer-arm gate-counting episodes) at **~89 sessions** (~2027-01-21) - both far earlier than floor A
  (80 total contributing nights, ~121 sessions, ~2027-03-09 at the capped 0.6620 rate). **Floor A
  would become the binding floor**, not floor B as the provisional schedule in DECISIONS.md
  assumes - a materially earlier window end than the ~151-session provisional figure now on the
  board, if the true SMA50/SMA200, >=250-session arm split turns out close to this proxy. This
  is a proxy reading on a lower/upper-bounded arm, not a substitute for R1(b) run again on real SPY
  history, and it does not change today DEFERRED call.
- **The strict-legality 0/71 finding is not evidence against the hypothesis or the partition** - it
  is purely that this freeze SPY series starts too late. It disappears entirely once R2(i)
  extended SPY history is pinned; no re-specification of the arm is implied or needed (DECISIONS
  item 12, PREREG Section 5.3 R2(i)).

## What this does and does not decide

This is a counts-only exposure measurement. No touch rate, return, excursion, plan result, or
arm-versus-outcome relationship appears anywhere above. Limbs (a)-(f) are reported in full because
R1 asks for them unconditionally; limb (g) is the one that actually decides today, and it is short -
credentials absent, probe not attempted, no pinned alternative exists. Per PREREG Section 5.3 R1 and
DECISIONS items 12 and 15, **Q032 goes to research/questions/DEFERRED.md** with this report
measured counts and the H-074 credentials re-check trigger; it is not re-registered on a weaker
partition. The Registrar/Decision-maker files the DEFERRED entry and updates the board; the Data
Steward does not decide that step, and does not advance the controller under this protocol.
