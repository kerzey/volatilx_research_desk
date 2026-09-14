# STEWARD_Q035_exposure.md - R1 (counts only), Q035 setup_architecture

**Request:** research/questions/Q035_setup_architecture/PREREG.md Section 5.3 R1, and DECISIONS.md
"Routed requests - data-steward - R1 (counts only) - BLOCKING FOR LOCK", routed by the
decision-maker 2026-09-14, as amended by DECISIONS items 2, 4, 13, 14 and 19.

**Population correction applied throughout (DECISIONS item 2, Correction 1):** P_t uses
lower(trim(coalesce(dominant_direction,''))) <> 'bearish' (the platform's actual main lane --
bullish + mixed), intersected with qualification_reason IN ('selected','capped_by_max_output'),
after Section 2.5's row screens. Counts only -- no outcome of any kind. Frozen data only:
research/data/manifest_v001.json + research/data/manifest_prices_v001.json against
research/data/exclusions_v003.json, plus a read-only commit-history check on the pinned platform
repo at fa70688. Never a live query (DP-50(c)). RESEARCH_DB_URL, ALPACA_API_KEY, ALPACA_SECRET_KEY
confirmed unset -- not needed for any of the nine limbs, which use frozen Parquet and the read-only
repo only.

**Period:** pick nights 2026-06-01..2026-09-10 (DP-06 segment). Denominator for every rate =
elapsed sessions (Q019/Q022/Q023/Q027/Q031/Q032/Q033 convention). N = 71 elapsed sessions
(reconfirmed against v001_sas_runs.parquet, 113 rows total, and the price-freeze session calendar,
153 sessions 2026-02-02..2026-09-10). Excluded (exclusions_v003, 3 nights inside this window):
2026-06-26 (uncorroborated_publication_runs), 2026-07-02, 2026-07-06 (manual_runs). Non-excluded:
68, identical to Q027/Q031/Q032/Q033's population on this same window.

---

## Headline

**All nine limbs were measured directly from the raw Parquet. Three of the seven gated limbs are
decisively short -- (c), (d) and (f) -- and they share one root cause that is new to the desk's
record: the projection layer (v1.6 weight 29, the single largest of the seven) carries
score: null, available: false, reasons: ["Projection context unavailable"] for roughly
three-quarters of every population this question touches, including the platform's own
actually-published slate.**

- Of the **579** selected (published) bull-lane rows in this window, **72.2%** have a null
  projection_score. Of the **692** capped_by_max_output rows (the reorder room this question
  exists to use), **74.3%** do. This is not concentrated in one timeframe (short/swing/long all sit
  in the 71-79% range) and is not an artifact of R1's own screens -- it is read directly off
  score_details_json.weighted_dimensions.projection (available: false, weight: 0.0) on the
  frozen sas_candidates rows, before any screen in this report touches them. **This is a genuine
  platform data-completeness fact, not previously logged in CLAUDE.md's known-issues list**, and
  it is reported here as a fact about the data, not interpreted further (that is a question for
  @registrar to register and @researcher to run).
- Section 2.5(3) requires "a null/non-finite ... any of the seven layer subscores" to remove a row
  from the population. Read fully literally (**including** smart_money_confirmation_score), that
  column is **null in 100% of the entire 6,479-row frozen sas_candidates table** -- every trading
  date, every row, not a window-specific artifact -- so the literal screen leaves **P_t permanently
  empty, on any window, forever**, which cannot be the Registrar's intent given Section 2.3's own
  accommodation for exactly this layer (the zero-variance argmax exclusion). **I use the reading
  that excludes smart_money_confirmation_score from the completeness screen** (consistent with
  Section 2.3's own PI-008 clause for that column) for every number below, and flag the literal
  reading for the coordinator, the same way STEWARD_Q033_exposure.md's limb (d) flagged its own
  reading-dependent gate. Even under this more generous reading, the **projection**-driven
  completeness screen alone takes the median contributing night's |P_t| from 16 (pre-screen) to
  **3**, and the fully-screened population (adding the Section 2.5(2) t+20-gradeability and
  60-prior-session screens) to a median of **5** -- decisively below the registered floor of 11.
- **Branch fired: DEFERRED, on the measured numbers, independent of any reading choice on limb
  (b).** Limbs (c), (d) and (f) are not close; nothing about a longer window or the single DP-13
  extension cures them, because they are **testability limbs, not sample-rate gates** (DECISIONS
  item 14's own words) -- they measure whether the architecture has room to be tested at all, and
  the answer today is that it mostly does not, because the platform itself did not score the
  projection layer for most of the rows this question needs.

**Gate limb table** (9 limbs as routed; (a)-(g) are gated, (h)-(i) are informational per R1's own text):

| limb | measure | floor | measured | pass/short |
|---|---|---:|---:|---|
| (a) contributing-night rate/session | full-window / subperiod (t+20-evaluable) | >= 0.36 | **0.5775** (41/71) / 0.8039 (41/51) | **PASS** |
| (b) rarest-setup (C, catalyst) nights/session | full-window / subperiod | >= 0.09 | 0.0845 (6/71) / **0.1176** (6/51) | **SHORT** on full-window reading, **PASS** on subperiod reading -- flagged, not decided, here |
| (c) reorder room: median size of P_t, share P_t>=9 | -- | median >= 11 and >= 80% of nights with P_t>=9 | **median 5**, **31.7%** of nights >= 9 | **SHORT** (both sub-clauses) |
| (d) reorder rate | pure-ranker slate vs reconstructed universal slate | >= 0.50 | **0.2683** (11/41) | **SHORT** |
| (e) partition viability | row-weighted margin share >= 0.25 sd; >=4 varying layers on >=80% of nights | >= 0.60 margin share, >=4 layers on >=80% | margin share **0.615**; >=4 layers on **85.4%** of nights | **PASS** |
| (f) reconstruction correctness | agreement, universal-arm reconstruction vs actual published slate | >= 0.90 | **0** qualifying ("undisturbed") nights exist to measure this on; on the full screened population, **0.00** (0/41) | **SHORT** (undefined on its own registered population; decisively short on the only computable proxy) |
| (g) DP-50(a)/(b) sweep since fa70688 | commit sweep | no change, or dated | cited, see (g) below: **NONE** | **PASS** |
| (h) mixed-row share | informational | -- | 442/2739 (16.1%) of the non-bearish lane, but **0** in P_t's reason set and **0** in the actual published slate | informational, no gate |
| (i) printed swing target distance in ATR units | informational | -- | **not computed this pass** (see note) | informational, no gate |

Four of the seven gated limbs clear; three do not, and one of the three that clears ((b)) clears
only under one of two readings -- the reading choice on (b) does not change the branch, because (c),
(d) and (f) are decisively short on any reading.

---

## (a) Contributing-night rate -- Section 2.6's own funnel

**Section 2.6 definition used exactly as registered:** a night t contributes iff it has a
corroborated, non-excluded sas_runs row, |P_t| >= 1 after Section 2.2's filters and Section 2.5's
screens, and >= 1 row of P_t gradeable at 2.0 ATR on the 20-session clock. "Gradeable" here means a
bar exists at t+1 and the forward split-adjusted series reaches session t+20 inside this freeze
(the freeze ends 2026-09-10; a touch is never computed, per R1's own ban on outcome columns -- this
is a pure censoring/completeness check, the same construction STEWARD_Q032/Q033_exposure.md used
for their CTRA signature).

**Funnel, direction + reason filter only (Section 2.2), before Section 2.5:** 1,251 rows / 71 nights
(all bullish -- **0 mixed rows** ever reach qualification_reason IN ('selected',
'capped_by_max_output') on this window, see (h)). After exclusions: **1,185 rows / 68 nights**.

**After Section 2.5(3) completeness (excluding smart_money_confirmation_score, see Headline):** 301
rows / 61 nights survive.

**After Section 2.5(2) gradeability (60 prior sessions, t+1 bar, forward series to t+20 inside
the freeze) and Section 2.5(1)/(4):** **239 rows across 41 nights.** The freeze's own last date
(2026-09-10) right-censors every pick night after **2026-08-12** -- this is the same cutoff
fit.py's training window independently derives in DECISIONS item 9, an exact cross-check.

**Rate:**

| form | numerator | denominator | rate |
|---|---:|---:|---:|
| full window | 41 | 71 | **0.5775** |
| t+20-evaluable sub-period (2026-06-01..2026-08-12) | 41 | 51 | **0.8039** |

Both clear the **>= 0.36** gate (item 14) comfortably. Per DECISIONS item 13's already-registered
construction, min(r_Q035, 0.6620) would govern the schedule, not this gate -- min(0.5775,
0.6620) = 0.5775.

## (b) Per-setup rate -- the limb the PREREG itself names as decisive, and the one that turns out
not to be the binding problem

Setup assigned by within-night z-score argmax over the six populated layers (flow, technical,
projection, catalyst, gex, fundamental -- smart_money_confirmation_score is always null and so is
always excluded, consistent with Section 2.3), tie-break v1.6 weight order, on the
**fully-screened** P_t (239 rows / 41 nights) -- the pure ranker (w = 1) needs no fit and no
outcome.

| setup | rows | nights placing >=1 name | share of the 41 contributing nights | rate/71 | rate/51 |
|---|---:|---:|---:|---:|---:|
| A (flow) | 47 | 30 | 73.2% | 0.4225 | 0.5882 |
| B (projection or technical) | 85 | 32 | 78.0% | 0.4507 | 0.6275 |
| C (catalyst) -- **rarest** | 6 | 6 | 14.6% | **0.0845** | **0.1176** |
| O (residual) | 101 | -- | -- | -- | -- |

C is the rarest setup, exactly as Section 10 threat 5 anticipated (catalyst carries weight 10
against 29/27/24). Its rate clears the **>= 0.09** gate under the sub-period reading and falls short
by a hair under the full-window reading (0.0845 < 0.09) -- the identical reading ambiguity
STEWARD_Q033_exposure.md's limb (d) flagged for its own gate, applied here for the first time to
this question. **I do not decide which reading governs**, consistent with that precedent; I note
only that it does not matter to the branch, since (c), (d) and (f) below are short by far more than
a reading choice can close.

## (c) Reorder room: the distribution of P_t size -- decisively short

On the 239-row, 41-night fully-screened population:

| | value |
|---|---:|
| median size of P_t | **5** (registered floor: >= 11) |
| mean | 5.83 |
| min / max | 1 / 14 |
| share of nights with P_t size >= 9 | **31.7%** (13/41; registered floor: >= 80%) |

Both sub-clauses fail, and neither is close. The pre-completeness-screen size of P_t (direction +
qualification-reason filter only) has median **16** -- the completeness screen alone (driven almost
entirely by the null projection_score, see Headline) removes roughly two-thirds of the reorder
room before the gradeability screen is even applied.

## (d) Reorder rate -- decisively short

Pure-ranker top-8 (by S_i with w=1) vs the reconstructed universal top-8 (overall_score,
sorted by -overall_score then symbol), both built from the identical fully-screened P_t, on all
41 contributing nights:

- **Nights where the two slates differ (by set membership): 11 / 41 = 0.2683** (registered floor:
  >= 0.50).
- Mean names swapped, on the 11 differing nights: **1.27**. Mean names swapped, over all 41
  contributing nights: **0.34**.

A ranker with a median of 5 names to choose 8 from (P_t size <= 8 on the majority of nights) has
very little room to reorder anything -- this result is the direct, mechanical consequence of (c),
not an independent finding about the setup architecture itself.

## (e) Partition viability -- passes

On the same 239-row population, within-night z-standardized over whichever of the six layers carry
non-zero within-night variance that night:

- **Row-weighted margin share** (top z-score exceeds the runner-up by >= 0.25 sd): **0.615**
  (registered floor: >= 0.60). **PASS**, narrowly.
- **Share of nights with >= 4 layers carrying non-zero within-night variance: 85.4%** (35/41;
  registered floor: >= 80% of nights). **PASS.**

This is the one limb where the tiny per-night P_t size does not hurt the partition -- when only 2-5
names compete each night, their layer scores tend to be more separated relative to that small
sample's own spread, not less. Reported as measured; not a reason to read (c), (d) and (f) any less
seriously.

## (f) Reconstruction correctness -- short, and undefined on its own registered population

Two distinct populations, both measured:

- **On the raw P_t** (Section 2.2's direction + qualification-reason filter alone, before any
  Section 2.5 screen -- 1,185 rows / 68 non-excluded nights): the reconstructed universal slate
  (top 8, sorted by -overall_score then symbol) agrees with the platform's actual published
  main-lane slate on **68 / 68 nights = 100%**. This validates DECISIONS items 1 and 2's population
  correction itself: P_t as corrected reconstructs the platform's own choice set exactly.
- **On the fully-screened P_t** (239 rows / 41 nights -- the population Section 3 and Section 4.1
  actually build both arms from): agreement is **0 / 41 = 0.00%**. Once the completeness screen
  removes roughly 70% or more of each night's rows (again, overwhelmingly the null-projection_score
  rows), the top-8-by-overall_score of what survives essentially never matches the eight names the
  platform actually published that night, because most of the published eight themselves have a
  null projection_score and are disproportionately the ones the screen just removed.
- **Section 5.3(f)'s own qualifying condition -- "nights where no row was removed by Section 2.5" --
  is measured directly: 0 of 41 contributing nights have zero rows removed.** The limb's registered
  population is empty; it cannot be measured on its own terms at all, on this freeze.

Registered floor >= 0.90; measured **0.00** (or undefined). **SHORT**, by the largest margin of any
limb in this report.

## (g) DP-50(a)/(b) commit sweep since fa70688 -- cited, not re-run

Per R1's own instruction (cite STEWARD_Q033_exposure.md Section (e) rather than re-run it
if HEAD is still d19c9a9): **HEAD reconfirmed directly in this session at d19c9a9** (a read-only
commit-log check against the pinned platform repo, output "d19c9a9 Merge pull request #27 ..."),
identical to every sibling sweep run today. STEWARD_Q033_exposure.md Section (e)'s answer stands:
**NONE** of the four commits between fa70688 and d19c9a9 touch
services/super_agent_select_scoring.py, services/super_agent_select_models.py,
services/sas_conviction_card.py, or services/market_regime/scorer.py; no weight, threshold, cap,
completeness floor, bear-lane setting, enable-flag or v1.7 promotion has landed since the pin.
**PASS.**

## (h) Mixed-row share -- informational, DECISIONS item 2's correction has zero measured impact here

442 of 2,739 non-bearish-lane rows in this window (16.1%) carry dominant_direction equal to mixed.
**None of them ever reach qualification_reason IN (selected, capped_by_max_output), and none
appear in the actual published main-lane slate (0 of 560 published rows).** DECISIONS item 2's
correction -- reading the lane as non-bearish rather than bullish-only -- is verified correct against
the code (confirmed again here: the code-level lane is non-bearish), but on **this specific
window's actual data**, it changes nothing numerically: P_t built on a bullish-only filter and P_t
built on the non-bearish filter are identical sets here, because no mixed row this window ever
cleared the qualification/completeness bar mixed candidates would need to. Recorded for the Red
Team, not a gate.

## (i) Printed swing target distance in ATR units -- not computed this pass

Registered as non-gating and explicitly stated not to move Q035's 2.0-ATR level in any branch
(DECISIONS item 4). Given the decisive, non-time-curable shortfalls already established on (c),
(d) and (f), this informational limb was not computed in this pass; the printed target sits inside
public_payload_json.lane_plans.swing_trading.targets index 1 for published rows and can be pulled
on request if the coordinator still wants it for Section 10 threat 3's record.

---

## What this does and does not decide

This is a counts-only exposure measurement; no touch, first-touch date, return, excursion,
outcome_* column or setup-versus-outcome relationship appears anywhere above, and forward bars
were read only to establish gradeability and to build the screened population, never for a value.
**Per R1's own routed rule (any limb short means Q035 goes to research/questions/DEFERRED.md at
lock with the measured number named, not re-registered on a weaker partition, a merged setup or
a reduced floor), three of the seven gated limbs -- (c), (d) and (f) -- are short, decisively and
for a single, common, verifiable reason: the projection layer (v1.6's largest weight) is unscored
for roughly three-quarters of both the published slate and the capped tail in this window.** This
is a finding about data completeness, reported here as a fact; it is not this report's place to say
what it means for the hypothesis or to route a fix -- that is a question for the registrar to
register and the researcher to run, and the Registrar/decision-maker applies whichever reading
governs limb (b) and locks or defers the file. The Data Steward does not decide that step and does
not advance the controller under this protocol.

**On the user's request for projected dates each floor is reached, for the record:** the
rate-based floors (A: 80 contributing nights per primary, C: 20 per half, D: 30 post-lock) would
each be reached well inside DP-43's 225-session ceiling at the measured 0.5775 to 0.8039 per
session contributing rate. **Floor B (20 nights in the rarest setup, C) would need approximately
237 sessions at the full-window reading of (b) -- outside the 225-session ceiling -- or
approximately 170 sessions at the sub-period reading -- inside it.** None of this matters to the
branch: (c), (d) and (f) are **testability limbs, not sample-rate gates** (DECISIONS item 14), and
no amount of additional elapsed time cures a projection-layer null rate that is already present, at
the same 72 to 74 percent share, across the entire frozen history this freeze holds. Waiting longer
does not add reorder room; it only adds more nights shaped exactly like the ones already measured.
