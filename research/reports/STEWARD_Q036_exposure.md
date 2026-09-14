# STEWARD_Q036_exposure.md - R1 (counts only), Q036 confidence_label_validity

**Request:** research/questions/Q036_confidence_label_validity/PREREG.md S5.1/S5.3 R1, as amended
by DECISIONS.md items 6, 7, 10, 12. **Counts only, BLOCKING FOR LOCK.** No outcome of any kind: no
touch, no first-touch date, no return, no excursion, no outcome_* column, no
sas_selection_excursion, no uoa_symbol_daily.fwd_return_*, no label-versus-outcome cross-tab.
Forward bars read only to establish that a bar exists (maturity accounting), never for a value.
Frozen data only -- research/data/manifest_v001.json + research/data/manifest_prices_v001.json
against research/data/exclusions_v003.json, plus read-only git show/git log/git diff --stat/
git merge-base against the pinned platform repository at fa70688 -- never a live query
(DP-50(c)). RESEARCH_DB_URL, ALPACA_API_KEY, ALPACA_SECRET_KEY are unset in this session; none
is needed -- every limb below reads frozen parquet and the read-only platform repo only.

**Population:** pick nights **2026-06-01..2026-09-10** (DP-06's segment, the widest legal span for a
16:05 ET property with no outcome attached). Denominator for every rate = **elapsed sessions**
(exclusions not pre-removed, the Q019/Q022/Q023/Q027/Q031/Q032/Q034 convention).

**Elapsed sessions in window: N = 71**, reconfirmed against v001_sas_runs.parquet (71 rows) and
the SPY daily-bar calendar in manifest_prices_v001 (153 bars, 2026-02-02..2026-09-10) -- matches
every prior Steward report on this freeze.

**Nights excluded (base, exclusions_v003, 3):** 2026-06-26 (uncorroborated_publication_runs),
2026-07-02 (manual_runs), 2026-07-06 (manual_runs). DP-04 late-finished_at re-check: **1**
night fails (2026-07-06), already excluded -- **0** incremental. **Base non-excluded: 68**, matching
Q027/Q031/Q034.

**payload_disabled_runs -- the criterion new to Q036 (S2.4, inherited verbatim from Q027 S2.4 but
applied here as a whole-night exclusion, not a fallback): 1 additional night, 2026-06-02.** All 8
published rows that night carry analysis_status = "disabled" and no lane_plans object -- the same
signature STEWARD_Q027_exposure.md Headline flags, but where Q027's own construction rescues that
night via its trailing-median fallback (so it still counts as contributing for Q027), Q036's S2.4
excludes it whole. **This is the one place Q036's population differs mechanically from Q027's/Q031's
on this freeze.**

**FINAL non-excluded nights for Q036: 67** (68 minus 1). No other night in-window carries the
analysis_status = "disabled" / no-lane_plans signature on **any** published row, let alone all of
them -- checked directly, not inferred from Q027's report.

---

## Headline

**Q036 does not lock. Limb (c) -- E2's r_join, the overall_score >= 82 restriction -- measures
exactly 0.0000, on every form, over the whole sealed window, with zero contributing nights of any
kind. This is not a small-sample or maturity artifact: completeness_score never once falls below
65.37 anywhere in the 4,195 scored sas_candidates rows in this window -- published, unpublished,
any qualification status, any date -- so a medium-labelled row with overall_score >= 82 cannot
occur under _confidence_label's own arithmetic (completeness >= 65 would make it high, not
medium, the instant overall_score clears 82). E2's contributing series is empty by construction
on this data, not by chance.**

| gate limb | measure | threshold | measured | pass/short |
|---|---|---|---:|---|
| E1 r_join, Form (i) (schedule basis, DECISIONS item 6) | matured-sub-period joint rate | >= 0.43 | **0.5532** (26/47) | **PASS** |
| E1 r_join, Form (ii) (full-denominator, for the record) | 71-session denominator | -- | 0.3662 (26/71) | descriptive |
| E1 rho_co (diagnostic only, item 6) | both-labels-present marginal | -- | 0.5915 (/71) / 0.6269 (/67) | diagnostic |
| **E2 r_join, Form (i) (the limb that decides, per item 7's "E1 clears / E2 fails" clause)** | matured-sub-period joint rate, overall_score >= 82 | **>= 0.43** | **0.0000 (0/47)** | **SHORT -- by the whole 0.43, not a margin** |
| E2 r_join, Form (ii) | full-denominator | -- | 0.0000 (0/71) | SHORT |
| (g) label-integrity mismatch | recomputed vs stored confidence_level | <= 2% | **0.000%** (0/542, boundary cases 0) | PASS |
| (d) LOW arm | nights with any eligible published LOW row | descriptive | **0** | descriptive (structurally absent, not thin) |

**Gate branch fired: research/questions/DEFERRED.md.** Two of the gate's independent triggers fire
simultaneously: **E2's r_join < 0.37** (item 7's DEFERRED clause on its own), and **E1 clears while
E2 fails** (item 7's explicit "DEFERRED, not lock E1 alone" clause, because E1 without E2 cannot be
distinguished from Q027's ranking result -- S1.2). Neither the DP-13 extension nor any window
lengthening changes this call: the extension mechanism moves a slow rate to a later decision date,
but it cannot manufacture the [45,65) completeness band this freeze shows zero rows in. **No amount
of waiting fixes a rate of exactly zero rooted in a value the scoring stack has not produced once in
five months of frozen history** (the Q034 pattern, recurring here in a different variable).

**Re-check trigger, as specified in the routed request:** "the Steward measures >= 0.43 joint
contributing nights per elapsed session, on both the unrestricted and the overall_score >= 82
series, over a trailing quarter." Stated plainly: that re-check can only pass if
completeness_score starts landing in [45,65) on nights where overall_score also clears 82 --
i.e., if the scoring stack starts leaving a partial layer gap on a high-scoring name, which nothing
in the five-month frozen history shows it doing even once.

**A second, load-bearing data fact, flagged not resolved (limb (f)):** the PREREG's own S2.6 states
"the last two [enrichment flags] defaulting False" for enable_fundamental_enrichment and
enable_smart_money_enrichment, citing the platform's declared code default
(services/super_agent_select_models.py:110-111, confirmed read-only at fa70688:
enable_fundamental_enrichment: bool = False). **The observed runtime sas_runs.config_json for
every one of the 67 non-excluded nights in this window shows enable_fundamental_enrichment = True**
-- only enable_smart_money_enrichment sits at its coded default (False); catalyst enrichment is
also True throughout. The deployment overrides the code default for the fundamental flag on every
night measured. This is very likely why completeness_score never leaves the high-90s/100 band in
this window (two of three enrichment layers, not one, are actively populating the completeness
denominator's numerator) -- stated as an observed correlation between two measured facts, not a
mechanism claim (that is for the registrar/researcher, not this report).

---

## (a) Per-night label composition and single-label-night share

**Eligible published rows** (qualified IS TRUE AND selected_rank IS NOT NULL, dominant_direction
IN ('bullish','bearish') -- 0 mixed rows found on the 67 non-excluded nights -- confidence_level IN
('high','medium','low')) **on the 67 non-excluded nights: 542.**

| label | rows | share |
|---|---:|---:|
| high | 401 | 74.0% |
| medium | 141 | 26.0% |
| low | 0 | 0.0% |

**Single-label nights (all-HIGH or all-MED; LOW never appears in the non-excluded population): 25 of
67 (37.3%).** Every single-label night in this window is all-HIGH (never all-MED) -- checked directly.

By month:

| month | elapsed | non-excluded | LOW rows | single-label nights |
|---|---:|---:|---:|---:|
| 2026-06 | 21 | 19 | 0 | 12 |
| 2026-07 | 22 | 20 | 0 | 5 |
| 2026-08 | 21 | 21 | 0 | 7 |
| 2026-09 (partial, 1-10) | 7 | 7 | 0 | 1 |

**The 3 LOW-labelled published rows anywhere in the raw window (AAPL/DPZ/COIN, 2026-06-26, score
81.0/85.1/81.3, completeness 100.0) sit entirely on the excluded uncorroborated_publication_runs
night.** Recomputing _confidence_label on their own stored overall_score/completeness_score
gives medium/high/medium -- none recomputes to low -- consistent with exclusions_v003.json's
own finding that this night's frozen row set does not match its 16:05 ET run audit. This is additional,
independent evidence for that exclusion, not a new one.

---

## (b) r_join -- the limb that decides -- three forms

d*_t defined per Q027 S2.2 (dominant_direction known, split-scale screen, d_L3 in [0.25, 10], the
1-2-survivor trailing-20-night fallback, the zero-survivor whole-night exclusion), independently
recomputed from v001_sas_candidates.parquet and p001_daily_split.parquet (own ATR14 -- 14-session
SMA of true range -- and C_t, never atr_pct/spot_close, PI-003):

- **Every one of the 67 non-excluded nights has a direct d_L3 median from >= 3 screened survivors**
  (min 4, median 8, max 10). **0 nights need the 1-2-survivor fallback; 0 nights have zero survivors**
  (the one night that would have -- 2026-06-02 -- is already excluded via payload_disabled_runs).
  **d*_t is defined for all 67 non-excluded nights.**
- **d*_t distribution** (per-night median d_L3, ATR units, 67 nights): min 0.679, p25 1.266,
  median **1.858**, p75 2.195, max 3.701 -- this reproduces STEWARD_Q027_exposure.md S(c)'s own
  distribution (median 1.849, p25 1.266, max 3.701) to within rounding on an independently-built ATR
  series, which is strong cross-validation that this report's construction matches the registered one.

**Maturity** (session t+20 <= 2026-09-10, the freeze's own last date): **47 of 67 non-excluded nights
matured** (last matured night **2026-08-12**, first immature **2026-08-13** -- identical cutoff to
STEWARD_Q027/Q031_exposure.md). 20 immature (freeze-horizon artifact, not a screening failure).

**Nights with >= 1 HIGH and >= 1 MED eligible published row (both conditions already satisfied -- d*_t
defined on all 67):**

| form | numerator | denominator | rate |
|---|---:|---:|---:|
| **(i) matured sub-period, both num/denom restricted (the schedule basis, DECISIONS item 6)** | **26** | **47** | **0.5532** |
| (ii) full-denominator, for the record | 26 | 71 | 0.3662 |
| (iii) rho_co marginal, no maturity restriction, diagnostic only | 42 | 67 (non-excl.) / 71 (elapsed) | 0.6269 / 0.5915 |

Scheduling rate (DECISIONS item 6): **min(0.5532, 0.6620) = 0.5532** -- clears the 0.43 gate limb with
room to spare.

By month (matured nights only, numerator = both-labels-present):

| month | matured nights | E1 contributing |
|---|---:|---:|
| 2026-06 | 19 | 7 |
| 2026-07 | 20 | 15 |
| 2026-08 | 8 | 4 |
| 2026-09 | 0 | 0 |

---

## (c) The same r_join, restricted to overall_score >= 82 -- E2's series

**Exactly 0 rows in the entire 67-night, 542-row eligible population carry confidence_level =
'medium' AND overall_score >= 82.** Confirmed at the widest possible scope, not just the eligible
population: **0 of all 4,195 scored sas_candidates rows in 2026-06-01..2026-09-10** -- any
qualified/threshold_pass status, any direction -- satisfy medium AND score >= 82. The reason is
arithmetic, not sampling: medium requires NOT high AND completeness >= 45; high requires score
>= 82 AND completeness >= 65; and **completeness_score never falls below 65.37 anywhere in this
window** (min over all 4,195 rows: 65.3686). So the instant score >= 82 and completeness >= 65
(which is every row, given the observed floor), the row is high by construction -- medium AND
score >= 82 is an empty cell on this data, not a rare one.

| form | numerator | denominator | rate |
|---|---:|---:|---:|
| (i) matured sub-period | 0 | 47 | **0.0000** |
| (ii) full-denominator | 0 | 71 | **0.0000** |
| (iii) marginal, diagnostic | 0 | 67 / 71 | 0.0000 |

**Nights that fall out of E1's 26-night contributing set into E2 non-contribution, solely because
every MED row that night sits below 82: 26 of 26 -- all of them.** MED scores on those 26 nights
cluster tightly in **[80.05, 81.99]**, i.e. the [80,82) sliver the PREREG's own S2.5 anticipated as
a possible zero-mass gap -- "E2's contributing nights are a subset of E1's; the difference is
nights on which every MED row sits in [80, 82). That count is printed" -- measured here at its
maximum possible value: **100% of E1's contributing nights**, not a subset.

---

## (d) LOW arm

**0 nights carry any eligible published LOW row** in the 67-night non-excluded population. Item 12's
descriptive-arm demotion is moot here -- there is no LOW mass to demote; the arm is **structurally
absent from the non-excluded population, not merely thin**, matching the pattern
STEWARD_Q027_exposure.md found for market_regime bearish/neutral/risk_off labels. The only 3 LOW
rows in the raw (pre-exclusion) window sit on the already-excluded 2026-06-26 night and do not
themselves recompute to low under _confidence_label (see (a)).

---

## (e) overall_score x completeness_score grid

**Published rows (67 non-excluded nights, 542 rows):**

| score band | [35,45) | [45,65) | [65,100] |
|---|---:|---:|---:|
| <80 | 0 | 0 | 1 |
| [80,82) | 0 | 0 | 140 |
| [82,85) | 0 | 0 | 302 |
| [85,88) | 0 | 0 | 56 |
| [88,90) | 0 | 0 | 21 |
| [90,100] | 0 | 0 | 22 |

**Unpublished threshold_pass rows (the B3/dark-set cohort, same 67 nights, 646 rows):**

| score band | [35,45) | [45,65) | [65,100] |
|---|---:|---:|---:|
| <80 (see note) | 0 | 0 | 212 |
| [80,82) | 0 | 0 | 352 |
| [82,85) | 0 | 0 | 77 |
| [85,88) | 0 | 0 | 5 |
| [88,90) / [90,100] | 0 | 0 | 0 |

Note: threshold_pass rows below 80 exist because the lane threshold can sit below publication_floor
before its 2026-07-08 ship (per (f)); threshold_pass itself only requires score >=
max(lane_threshold, publication_floor), so this is not an anomaly.

**Every single cell in both grids -- published and dark -- sits in the [65,100] completeness column.
Zero rows, on either cohort, anywhere in the sealed window, carry completeness_score in [35,45)
or [45,65).** Dark-cohort label composition confirms the same asymmetry: 564 medium / 82 high / **0
low** -- the dark cohort (DECISIONS item 16 / Correction 5, already established to share the published
slate's two floors) shows the identical completeness ceiling.

---

## (f) sas_runs.config_json tuple across the 67 non-excluded nights, and the DP-50(a)/(b) sweep

| field | behavior across the 67 nights |
|---|---|
| min_completeness | constant, 35.0 |
| max_output_cap | constant, 8 |
| qualification_threshold | constant, 70.0 |
| atr_elite_bull_max_score / atr_elite_bear_max_score | constant, 84.9 / 79.9 |
| scoring_weights, timeframe_weight_multipliers | constant (byte-identical JSON every night) |
| enable_catalyst_enrichment | constant, **True** |
| **enable_fundamental_enrichment** | constant, **True** -- see Headline; contradicts PREREG S2.6's cited code default of False |
| enable_smart_money_enrichment | constant, **False** (matches its coded default) |
| publication_floor | **moves**: null (17 nights, through 2026-07-07) to 80.0 (50 nights, from 2026-07-08) |
| bear_publish_threshold | **moves**: null (16 nights, through 2026-06-26/28 window) to 80.0 (51 nights, from 2026-06-29) -- exact split date reconfirmed here as **2026-06-29** |

**No field that feeds completeness_score's numerator/denominator (:1316-1322, :1347) or the
_confidence_label thresholds themselves (:1167-1170) moves in-window.** publication_floor and
bear_publish_threshold gate publication, not the score or completeness computation -- already
logged in DATA_NOTES.md (the ladder-monotonicity entry, 2026-09-13, per
STEWARD_Q027_exposure.md S(g)) and reconfirmed here on Q036's own 67-night population, not copied.
Per DECISIONS item 11's own list these two fields are named S2.6 triggers regardless of mechanism;
flagged here for the registrar's ruling on whether that clause is read as applying to R1's sealed
diagnostic count (it is not, on its plain reading -- item 11 splits eval.py's prospective window at
a ship date, and neither field's sealed-window movement changes a completeness or label value on any
row in this population, verified directly above) rather than resolved unilaterally by this report.

**DP-50(a)/(b) commit sweep since fa70688, reconfirmed independently in this session (not copied):**
fa70688bc252d14f8d67e371afafc194731c324e is an ancestor of HEAD
(d19c9a945418b09773baffac37f8d723c8a90a9a, git merge-base --is-ancestor). **4 commits, all dated
2026-09-13** (2d5776c PI-001 backfill-window floor, 4775e49 merge, 22a2e1b EN-002
speed-to-target internal card flag-off, d19c9a9 merge) -- **git diff --stat fa70688 HEAD --
services/super_agent_select_scoring.py services/super_agent_select_models.py
services/sas_conviction_card.py returns empty.** **Answer: NONE** -- no weight, timeframe multiplier,
qualification_threshold, publication_floor, bear_publish_threshold, ATR-elite cap, GEX offset,
or scoring/enrichment enable-flag has changed in the platform code since fa70688. _confidence_label
itself (:1166-1171) verified byte-identical to the PREREG's S1.1 citation, called at :1425
**after** the ATR-elite cap block (:1407-1423), so the stored overall_score the label was computed
from is the post-cap value -- the S2.2 integrity screen (limb (g)) is well-posed. overall_score and
completeness_score are rounded to 4 dp at return (matching DECISIONS item 10's description).

**v1.7 schedule check (docs/SAS_SCORING_RESEARCH_PLAN.md):** unchanged since its 2026-08-26 draft,
still headed "Status: PROPOSAL -- not a decision record... Owner sign-off required before any
workstream starts," phases in relative weeks with no calendar anchor, no commit anywhere shows the
workstream has started. **No v1.7 promotion is scheduled inside this window or the prospective one**
-- same finding as STEWARD_Q027/Q031/Q034_exposure.md, to be rechecked at every future sweep.

---

## (g) Label-integrity mismatch rate

Recomputed _confidence_label(overall_score, completeness_score) from the stored columns using the
literal constants (high iff overall >= 82.0 AND completeness >= 65.0; medium iff overall >=
68.0 AND completeness >= 45.0; else low), compared against the stored confidence_level, on the
542 eligible published rows (67 non-excluded nights):

**Mismatches: 0 of 542 (0.000%).** **Boundary-tolerance cases (within 0.01 of 82.0/68.0/65.0/45.0,
counted separately per DECISIONS item 10): 0.** Well under the 2% blocking threshold -- **this limb
does not itself contribute to the DEFERRED call.** sas_candidates.confidence_level on this
population is exactly what _confidence_label at the pinned SHA would write from the stored
overall_score/completeness_score -- no PLATFORM_ISSUES.md entry is warranted from this limb.

---

## (h) d*_t funnel (behind (b))

Published rows, dominant_direction known, 67 non-excluded nights: **542**.

| category | rows |
|---|---:|
| valid (survives all screens, used for d_L3) | 514 |
| split-scale payload screen (entry ratio outside [0.85,1.15] AND a flattened level >20 ATR, jointly) | 20 |
| d_L3 outside [0.25,10] ATR bound | 7 |
| wrong side (d_L3 <= 0) | 1 |
| no lane_plans at all | 0 (the one night with this signature, 2026-06-02, is already excluded whole) |
| **total** | **542** |

**Zero-survivor nights: 0. 1-2-survivor fallback nights: 0. Nights outside the [0.25,10] bound at
the night level: 0.** dominant_direction = 'mixed' share: **0.0%** on all three arms (HIGH/MED/LOW)
-- no mixed-direction row survives into the eligible published population on any non-excluded night in
this window. d*_t distribution already given in (b); no movement comparable to Q027 R1(c)'s
1.06 to 2.10 ATR shift is visible inside Q036's 67-night population (the publication_floor ship at
2026-07-08 falls inside this window and the same level shift Q027 found is present here too --
median d*_t 1.06 ATR pre-ship vs approx 2.10 post-ship -- but as established in (f), this field does
not touch completeness_score or the confidence label, so it is reported and not adjudicated).

---

## The lock-or-DEFER call

**Both of item 7's independent DEFERRED triggers fire:**

1. **E2's r_join (0.0000) < 0.37** -- the "either < 0.37 -> DEFERRED" clause fires on its own.
2. **E1 clears (0.5532 >= 0.43) while E2 fails** -- the "E1's limb clearing while E2's fails is
   DEFERRED, not 'lock E1 alone'" clause fires independently, for the reason S1.2 gives: E1 without
   E2 cannot be distinguished from Q027's ranking result.

**Q036 goes to research/questions/DEFERRED.md**, with:
- the measured rates named: **E1 r_join = 0.5532 (Form i, schedule basis) / 0.3662 (Form ii);
  E2 r_join = 0.0000 (every form)**;
- the re-check trigger, verbatim from the routed request: "the Steward measures >= 0.43 joint
  contributing nights per elapsed session, on both the unrestricted and the overall_score >= 82
  series, over a trailing quarter" -- stated plainly above: this requires completeness_score to
  start landing in [45,65) on score >= 82 nights, which has not happened once in five months of
  frozen history;
- **no (g) PLATFORM_ISSUES.md entry** -- the label-integrity screen clears at 0.000%, so this
  DEFERRED is not a data-quality defect, it is a population that does not exist on the current
  scoring configuration;
- the enable_fundamental_enrichment code-default-vs-runtime-config discrepancy (Headline, (f))
  flagged for whoever next revises the PREREG or investigates why completeness_score behaves this
  way -- not adjudicated here.

**Projected date the 80-night floor would be reached, for the record only (moot -- the gate call does
not depend on it):** E1 alone, at the Form-(i) scheduling rate (0.5532/elapsed session, capped at
0.6620), would clear 80 contributing nights in **approx 145 elapsed sessions** -- well inside any
window this desk has ever set. **E2 has no such date: at a measured rate of exactly zero, the
projection is undefined**, not merely far out (contrast STEWARD_Q034_exposure.md's literal-reading
projection of "session approx 880," which is at least a finite number).

---

## What this does and does not decide

This is a counts-only exposure measurement. No touch rate, return, excursion, plan result, or
label-versus-outcome relationship appears anywhere above. The lock-or-DEFER call is mechanical and
follows directly from PREREG S5.1's gate table as re-solved in DECISIONS.md items 6/7: E2's
measured r_join is 0.0000, which is below every threshold in the gate table by construction, not by
a close call. I report the measured population and the branch it implies; the registrar/
decision-maker files the DEFERRED.md entry and updates the board. The Data Steward does not
advance the controller under this protocol and takes no position on whether the label carries price
information -- that remains "a question for @registrar to register and @researcher to run" if and
when completeness_score is ever observed to vary the way the PREREG's design requires.
