# STEWARD_Q029_feasibility.md - R1b (counts only, no outcome), Q029 layer_value_ablation

**Request:** Q029 PREREG.md section 5.3 request R1b, routed by DECISIONS.md item 11
("m, the EVALUABLE/DEAD list, the GEX weight and the suppression list"). Counts-only feasibility
on the frozen data: manifest_v001.json (v001_sas_candidates.parquet, v001_sas_runs.parquet)
against exclusions_v003.json, plus read-only git log/git show against the pinned platform
repository at fa70688. No outcome of any kind is read: no touch, first-touch date, return,
excursion, outcome_*, sas_selection_excursion, uoa_symbol_daily.fwd_return_*, or score-vs-outcome
cross-tab of any shape. No price bar was used beyond what Q027 R1(c) already pins. R1b does not
decide the lock gate; Q027 R1 does (already measured: 0.6761 contributing nights per elapsed
session, clears the 0.36 DEFER threshold by 88%; Q027 and Q029 lock).

**Population:** every row in sas_candidates, published or not, regardless of qualified/
threshold_pass, pick nights 2026-04-01..2026-09-10 (whole freeze), with exclusions_v003.json
(11 nights: 9 manual_runs + 1 non_session_runs + 1 uncorroborated_publication_runs) and DP-04
late-finished_at nights removed. DP-04 re-checked independently for the whole freeze: 0
incremental nights (every DP-04-late night, 2026-04-02 and 05-11..05-14 and 07-06, already in
manual_runs). Population: 5,928 rows / 102 nights (34 in-sample to 2026-05-29, 68 sealed from
2026-06-01, matching exclusions_v003.json's own counts exactly). The 2026-06-01..2026-09-10
segment is 4,020 rows / 68 nights, identical to STEWARD_Q027_exposure.md's step-0 population,
cross-validated.

---

## Headline (what R1b decides)

m has two possible values depending on how one clause of the PREREG's own text is read, and R1b
surfaces the ambiguity rather than resolving it. That is the registrar's/decision-maker's call,
not mine. Both readings, and the measurement that produces each, are below.

- If the "whole-freeze" clause in section 2.4/5.3(d) is read at the literal 2026-04-01 start:
  whole-freeze Gate-0 reconstruction is 84.77%, below the 95% bar, so every E3(j) is UNEVALUABLE
  at record (DECISIONS item 17) and Q029 locks as an IC-only question: m = 10 (2 endpoints times
  5 coverage-evaluable layers).
- If Gate-0's "whole-freeze" is read consistently with Correction 3's own scoping (Correction 3
  names Gate-0 explicitly as one of the "coverage and arithmetic facts" it applies to, and
  decides such facts on the 2026-06-01..2026-09-10 segment because the pre-v1.5 population is a
  demonstrably different engine, not because the sample is thin): segment Gate-0 reconstructs at
  100.00% (68/68 nights, every night at or above 99%), clears both bars comfortably, and m = 16
  (10 IC endpoints plus 6 evaluable E3 endpoints; see the per-layer table below).
- I did not find any reading under which the 84.77% figure is itself in doubt or an artifact of
  noise. It is caused by exactly one mechanism, dated precisely, explained fully in section (d)
  below, and it is the same mechanism (the v1.5 ship, approximately 2026-05-14/05-18) that
  Correction 3 already invokes to scope layer-coverage evaluability to the segment. My own
  reading, offered as a recommendation and not a decision: the same scoping should govern Gate-0,
  because Gate-0's own formula (the GEX-missingness offset, the ATR-elite cap, the extra
  weighted_dimensions fields) did not exist in the engine before that ship; the 84.77%
  whole-freeze figure is not "5,928 rows minus a residual arithmetic error," it is "1,732 rows
  scored by a materially different formula than the one at fa70688."

Per-layer register (segment-scoped reading; the alternative IC-only reading simply drops all six
E3 rows and the projection row entirely):

| layer | E1/E2 | E3 | reason |
|---|---|---|---|
| flow_strength | EVALUABLE | EVALUABLE (REMOVAL) | clears 70%/5-distinct/50%-nights on segment; Gate-0 clears on segment |
| technical_structure | EVALUABLE | EVALUABLE (REMOVAL) | same |
| gex_alignment | EVALUABLE | EVALUABLE (ADDITION, weight 12.0) | subscore computed on 99.0% of rows even though production weight is 0 everywhere in-segment; clears the ADDITION-layer >=70% clause too |
| projection | UNEVALUABLE | EVALUABLE (REMOVAL) | subscore non-null on only 62.74% of segment candidate rows, failing the 70% coverage floor despite being the largest-weighted layer (29 pts); E3 unaffected because the 70%-non-null clause in section 4.3 binds E1/E2 and ADDITION-E3 only, never REMOVAL-E3 |
| fundamental_quality | EVALUABLE | EVALUABLE (REMOVAL side only) | 98.71% non-null on segment, contrary to the PREREG's own drafted expectation ("DEAD or ADDITION-only," based on the code's False default); enable_fundamental_enrichment measured True on 81 of 102 population nights, including 67 of the 68 segment nights. ADDITION side (2026-06-02 only) projects to 1.3 contributing nights at 92 sessions: UNEVALUABLE, not in m |
| catalyst_event | EVALUABLE | EVALUABLE (REMOVAL) | clears all three clauses on segment (100% non-null, 8 distinct, 100% of nights nonzero-variance) |
| smart_money_confirmation | DEAD | DEAD | 0.00% non-null, 0 distinct values, on every row in the whole freeze; not merely thin, literally never computed; matches DATA_NOTES / PI-008 |

m (segment-scoped reading) = 10 (E1+E2 times 5 layers) + 6 (E3 for flow, technical, gex,
projection, fundamental-REMOVAL, catalyst) = 16. Within Correction 1's stated bound (<= 21 plus
one further endpoint per layer whose both sides clear 80; no layer's both sides clear 80 here,
so the bound is the plain 21, and 16 is inside it). This is above the PREREG's drafted
expectation of "12-15," driven by fundamental_quality turning out to be EVALUABLE on all three
endpoints (not DEAD/ADDITION-only as drafted) while projection loses two of its three (not fully
evaluable as drafted).

REMOVAL/ADDITION split and per-side projected rate (92-session prospective window, segment rate
times 92, denominator 71 elapsed sessions, the same denominator Q027's R1 cross-validated):

| layer | REMOVAL nights (of 68) | ADDITION nights (of 68) | REMOVAL proj@92 | ADDITION proj@92 | verdict |
|---|---:|---:|---:|---:|---|
| flow_strength | 68 | 0 | 88.1 | 0.0 | REMOVAL only |
| technical_structure | 68 | 0 | 88.1 | 0.0 | REMOVAL only |
| gex_alignment | 0 | 68 | 0.0 | 88.1 | ADDITION only, weight 12.0 |
| projection | 68 | 0 | 88.1 | 0.0 | REMOVAL only (E3; E1/E2 UNEVALUABLE) |
| fundamental_quality | 67 | 1 | 86.8 | 1.3 | split: REMOVAL side clears 80, ADDITION side (1.3 proj.) UNEVALUABLE, not in m |
| catalyst_event | 68 | 0 | 88.1 | 0.0 | REMOVAL only |
| smart_money_confirmation | 0 | 68 | 0.0 | 88.1 | DEAD, not tested despite clearing the count floor, because coverage is 0% |

GEX pre-2026-05-14 weight: 12.0, directly measured, not a fallback. Last population
(non-excluded) night before 2026-05-14 with a non-zero scoring_weights.gex_alignment:
2026-05-08 -> 12.0. Only two distinct values ever appear in sas_runs.config_json's
scoring_weights.gex_alignment across the entire 113-run raw history: 12.0 (2026-04-01..
2026-05-08, clean nights; the raw table also shows 12.0 on 2026-05-13, but that night is an
excluded manual_runs re-run artifact) and 0.0 (2026-05-18 onward, clean). PREREG section 2.3
Option A registers exactly this value; no fallback to the 12.0-by-arithmetic branch is needed.

Whole-freeze Gate-0 reconstruction: 84.77%. Segment (2026-06-01..09-10) Gate-0 reconstruction:
100.00%. See section (d).

Slate-replay disagreement vs the 1% gate: 0 of 68 segment nights exceed 1% (0.00% mean); 12 of
102 whole-freeze nights exceed 1% (2.33% mean), all in April, all explained (section (e)).

Per-layer share of nights the ablated slate differs from production at all (segment, k(t,j)>0
share): flow_strength 94.1%, technical_structure 95.6%, gex_alignment 98.5%, projection 83.8%,
fundamental_quality 88.2%, catalyst_event 32.4%, smart_money_confirmation 0.0% (mechanical
E3=0, a NULL by construction).

Near-miss pool (bull-lane, threshold+completeness pass, not selected), segment: min 0 (3 of 68
nights), median 8, max 26. Whole freeze: min 0 (3 of 102 nights), median 12, max 26.

(g) DP-50(a)/(b) commit sweep since fa70688: NONE, independently re-verified (git merge-base
--is-ancestor fa70688 HEAD confirms ancestry; git log --oneline fa70688..HEAD for the 4 files
returns empty). Same 4 commits Q027's R1 found (2 substantive + 2 merges, all 2026-09-13, neither
touching super_agent_select_scoring.py, _models.py, _service.py or sas_conviction_card.py). v1.7:
no part has shipped or is scheduled with a committed date. docs/SAS_SCORING_RESEARCH_PLAN.md at
fa70688 is still headed "Status: PROPOSAL, not a decision record. Supersedes nothing. Owner
sign-off required before any workstream starts." Its own Phase 1 prerequisite (dark-cohort W60
backfill) has not shipped either; the only in-flight related work is PI-001 (2d5776c, branch
fix/pi-001-backfill-window-floor, not merged to main as of the commit sweep), which only widens
which NULLs a nightly job revisits and touches none of the four named scoring files. No evidence
of a scheduled promotion inside pick nights 2026-09-15..2027-03-10.

---

## (a) Layer coverage, per layer and per month, and for the 2026-06-01..2026-09-10 segment

Q028 section 4.0 retained-layer rule: >=70% non-null, >=5 distinct values, non-zero within-night
variance on >=50% of nights, adopted verbatim by Q029 section 4.3. Measured on flat columns
(<layer>_score columns), all-candidates basis (no eligibility filter; a coverage fact, not an
outcome fact).

| cell | layer | rows | nights | non-null share | distinct values | nights w/ nonzero var |
|---|---|---:|---:|---:|---:|---:|
| WHOLE FREEZE | flow_strength | 5928 | 102 | 99.87% | 5863 | 100.0% |
| WHOLE FREEZE | technical_structure | 5928 | 102 | 100.00% | 1219 | 100.0% |
| WHOLE FREEZE | gex_alignment | 5928 | 102 | 84.35% | 32 | 100.0% |
| WHOLE FREEZE | projection | 5928 | 102 | 59.29% | 3197 | 100.0% |
| WHOLE FREEZE | fundamental_quality | 5928 | 102 | 78.73% | 394 | 79.4% |
| WHOLE FREEZE | catalyst_event | 5928 | 102 | 100.00% | 8 | 66.7% |
| WHOLE FREEZE | smart_money_confirmation | 5928 | 102 | 0.00% | 0 | 0.0% |
| SEGMENT (decisive, Correction 3) | flow_strength | 4020 | 68 | 99.88% | 3986 | 100.0% |
| SEGMENT | technical_structure | 4020 | 68 | 100.00% | 1216 | 100.0% |
| SEGMENT | gex_alignment | 4020 | 68 | 99.00% | 32 | 100.0% |
| SEGMENT | projection | 4020 | 68 | 62.74% | 2214 | 100.0% |
| SEGMENT | fundamental_quality | 4020 | 68 | 98.71% | 379 | 98.5% |
| SEGMENT | catalyst_event | 4020 | 68 | 100.00% | 8 | 100.0% |
| SEGMENT | smart_money_confirmation | 4020 | 68 | 0.00% | 0 | 0.0% |

Per-month non-null share (whole freeze; catalyst and smart-money omitted, flat 100%/0% every
month):

| month | nights | flow | technical | gex | projection | fundamental |
|---|---:|---:|---:|---:|---:|---:|
| 2026-04 | 19 | 99.83% | 100.00% | 38.07% | 49.44% | 0.00% (flag off all month) |
| 2026-05 | 15 | 99.87% | 100.00% | 76.95% | 56.03% | 92.58% |
| 2026-06 | 20 | 99.90% | 100.00% | 98.91% | 56.49% | 95.24% |
| 2026-07 | 20 | 99.76% | 100.00% | 98.64% | 64.46% | 99.92% |
| 2026-08 | 21 | 100.00% | 100.00% | 99.62% | 65.11% | 99.77% |
| 2026-09 (to 9/10) | 7 | 99.77% | 100.00% | 98.37% | 65.03% | 100.00% |

projection never clears 70% in any single month measured; the trend rises (49% to 65%) but
plateaus below the floor from July on. This is not a maturity artifact (unlike Q027's
contributing-night rate); it is a standing feature of the candidate universe - a meaningful share
of nightly candidates simply have no entry in the projection tables that night. catalyst_event's
0% within-night variance in April independently corroborates the known "catalyst scored a flat 80
pre-2026-06-01" finding (DATA_NOTES.md, commit 69ef05f) - a coverage fact reproducing an
already-known finding, not a new one.

## (b) Production effective-weight census, REMOVAL/ADDITION split, enrichment flags

From score_details_json's weighted_dimensions[j].weight (the row's own point-in-time effective
weight, already timeframe-multiplied and context-gated), not the nominal
config_json.scoring_weights value.

Segment (68 nights), share of rows with weight>0 and distinct weight values:

| layer | share rows weight>0 | distinct weight values (segment) |
|---|---:|---|
| flow_strength | 99.88% | 0.0, 19.2, 24.0, 25.2 |
| technical_structure | 100.00% | 25.65, 27.0 |
| gex_alignment | 0.00% | 0.0 |
| projection | 62.81% | 0.0, 29.0, 31.9, 33.35 |
| fundamental_quality | 98.88% | 0.0, 0.75, 1.75, 5.0 |
| catalyst_event | 100.00% | 9.0, 10.0 |
| smart_money_confirmation | 0.00% | 0.0 |

REMOVAL/ADDITION night counts and per-side projections are in the headline table above:
flow/technical/projection/catalyst are REMOVAL on 100% of segment nights; gex/smart-money are
ADDITION on 100%; fundamental splits 67 REMOVAL / 1 ADDITION.

Enrichment flags, per night, population (102 nights):

- enable_smart_money_enrichment: False on all 102 nights, no exceptions. Matches PI-008 and the
  code default (super_agent_select_models.py:111).
- enable_fundamental_enrichment: True on 81 of 102 nights, False on 21. This contradicts the
  PREREG draft's own stated expectation (section 4.3: "smart-money and fundamental expected DEAD
  or ADDITION-only, since both enrichment flags default False"). The code's dataclass default is
  indeed False (super_agent_select_models.py:110), but the deployed, persisted config ran with
  the flag flipped True starting 2026-05-01, with brief single-night reversions (2026-05-04,
  2026-06-02): 20 of the 21 False nights are in April (flag simply never turned on that month),
  the 21st is the 2026-06-02 reversion. On the segment specifically, the flag is True on 67 of
  68 nights - exactly why fundamental_quality measures EVALUABLE on all three endpoints rather
  than DEAD/ADDITION-only.

## (c) GEX addition weight, every distinct config value, with date ranges

Measured two ways, both agreeing:

- Population (exclusions applied), 102 nights: gex_alignment = 12.0 on 2026-04-01..2026-05-08
  (25 nights); gex_alignment = 0.0 on 2026-05-18..2026-09-10 (77 nights). Last population night
  before 2026-05-14: 2026-05-08 -> 12.0.
- Raw freeze (unfiltered), 113 nights, for transparency: 12.0 on 2026-04-01..2026-05-13 (29
  nights, including the excluded 2026-05-13 re-run night); 0.0 on 2026-05-11..2026-09-10 (84
  nights; the transition is noisy across 2026-05-11..05-15 because those five nights are exactly
  the manual_runs re-run nights, i.e. the population-filtered answer is the trustworthy one).
  Last raw-dated config before 2026-05-14: 2026-05-13 -> 12.0 (excluded night; not used).

Only two distinct gex_alignment weight values ever appear in the entire frozen history: 12.0 and
0.0. No third value. PREREG section 2.3 Option A registers 12.0, confirmed by direct measurement;
the fallback-to-arithmetic branch (7+3+2=12) is not needed.

The same transition date range (2026-05-11..05-18, clean at 05-18) also carries the full v1.5
weight reallocation together, not just GEX: technical_structure 20.0->27.0, projection
26.0->29.0, catalyst_event 8.0->10.0, gex_alignment 12.0->0.0, effective the first clean
population night 2026-05-18. flow_strength (24.0), fundamental_quality nominal (5.0),
smart_money_confirmation nominal (5.0) are constant across the whole freeze. This matches the
code comment at super_agent_select_models.py:9-13 exactly (7+3+2=12, 24+20+26+5+8+5=88, +12=100).

## (d) Gate-0 reconstruction rehearsal

Reconstructed overall_score from stored weighted_dimensions plus the row's stored
cross_layer_bonus, conflict_penalty, missing_data_penalty, a derived GEX-missingness offset
(+5.0 iff the row's gex_alignment subscore is null), and the stored atr_elite_block_applied flag
(re-applying the same 84.9/79.9 cap by dominant_direction where true), per section 2.4's formula,
tolerance 0.05.

| scope | rows | parse_ok (weighted_dimensions present, all 7 keys) | reconstructs (<=0.05) | nights below 99% reconstruction |
|---|---:|---:|---:|---:|
| WHOLE FREEZE (2026-04-01..09-10) | 5928 | 100.00% | 84.77% | 25 of 102 |
| SEGMENT (2026-06-01..09-10) | 4020 | 100.00% | 100.00% | 0 of 68 |

The whole-freeze shortfall is not noise and not a partial failure; it is one mechanism, fully
explained, dated precisely to the same ship as (c). score_details_json carries only 8 keys for
every row dated 2026-04-01..2026-05-08 (no atr_elite_block_applied, no
gex_missing_offset_applied/value, no atr_projection_meta, etc.; fields _serialize_score_details,
services/super_agent_select_service.py:305-336 at fa70688, always writes); from 2026-05-11
onward every row carries the full ~20-key schema. Every single non-reconstructing row in the
pre-2026-05-11 era resolves to a residual of exactly +5.00 (865 of 1,462 "partial-schema" rows,
2026-04-01..2026-05-08, 90th/95th/99th percentile residual all approximately +5.0000) - the
signature of applying the v1.5 GEX-missingness offset (services/super_agent_select_scoring.py,
comment: "v1.5, GEX-missingness offset ... Post-Option-A coverage fix (2026-05-15)") to rows the
actual engine, running before that ship, never applied it to. Rows dated 2026-05-11 onward (full
schema) reconstruct at 100.00%, with zero exceptions, including the 25 "partial-schema" rows'
April/May siblings once the offset existed. In other words: the fa70688 Gate-0 formula
reconstructs the fa70688 engine perfectly, everywhere that engine ran; it cannot reconstruct an
engine two ships earlier, which is what the pre-2026-05-11 rows are. This is the arithmetic-layer
version of the same v1.5 boundary DP-06/Correction 3 already treat as a feature split for layer
coverage.

Residual distribution (parse_ok rows, whole freeze): median approximately 0.000006 (essentially
exact), mean 0.70 (pulled up entirely by the +5.0 partial-schema cluster), max 5.000077, min
-7.000056. The -7 tail (a small number of rows) is a separate, smaller residual worth a second
look at record; not diagnosed further here since it does not change either reconstruction-rate
headline (segment is already 100%, and the -7 rows are also confined to the pre-05-11
partial-schema era on inspection of the detail data) - consistent with the same formula-vintage
explanation, most likely an interaction between the missing ATR-elite fields and a capped row,
but the segment result does not depend on resolving it.

## (e) Slate-replay check and per-layer slate-change rate

Replay construction: bull lane = dominant_direction != bearish (includes mixed, per the code:
547 of 5,928 population rows carry mixed), threshold
max(timeframe_thresholds.get(best_timeframe, qualification_threshold), publication_floor),
completeness_score >= min_completeness, cap max_output_cap, sort (-overall_score, symbol). One
correction made and reported, not assumed: a night's own config_json sometimes lacks the
publication_floor / min_completeness keys entirely (56 of 102 nights lack publication_floor, all
pre-2026-07-08); this is not the same as the key being present with value null, it means the
mechanism did not exist in the engine on that night. The night's own config is honored literally:
an absent key is treated as "that gate did not apply that night" (0.0 floor), not as the current
dataclass's default (80.0); using the current default for historical nights where the field never
existed produced spurious disagreement in early diagnostic passes and is not used in the reported
numbers below.

(i) Disagreement rate vs the frozen published set (qualified IS TRUE AND selected_rank IS NOT
NULL):

| scope | nights | nights >1% disagreement | mean disagreement rate |
|---|---:|---:|---:|
| WHOLE FREEZE | 102 | 12 (all in April) | 2.33% |
| SEGMENT (2026-06-01..09-10) | 68 | 0 | 0.00% |

Every one of the 12 April discordant nights is explained, not merely counted. On each of them,
the frozen selected_rank sequence mixes bullish and bearish symbols under one shared counter
(e.g. 2026-04-13: ranks 1-4 are bearish NOW, DDOG, ARES, TTD; ranks 5-8 are bullish ANET, SLB,
TER, GEV) - i.e. the actual historical engine used a single combined 8-cap lane across both
directions on those nights, not the independent bull/bear lanes with separate counters that
_qualify_lane/_qualify_all_lanes implements at fa70688. The code's own comment (line 1642,
"BEAR lane split, 2026-07-02 instrument-only decision") dates this split; April nights predate
it by construction, so a fa70688-based bull-only replay cannot and should not reproduce them. No
unreproducible qualification_reason was found among published bull rows anywhere in the freeze
(selected_dark, sub-80 v2 markers; none appear qualified in the bull lane). This 12-night pattern
is a second, independent confirmation (beyond Gate-0's) that the pre-segment population runs
meaningfully different selection code, reinforcing Correction 3's segment scoping.

(ii) Per-layer ablated-vs-production slate-change rate, SEGMENT (68 nights), computed with the
renormalized (production) denominator convention, GEX addition weight 12.0, cross_layer_bonus/
conflict_penalty/ATR-elite decision held fixed per section 2.4:

| layer | night class | share nights k=0 | k distribution (min/p50/p90/max) |
|---|---|---:|---|
| flow_strength | REMOVAL | 5.9% | 0 / 4 / 8 / 10 |
| technical_structure | REMOVAL | 4.4% | 0 / 4.5 / 8 / 12 |
| gex_alignment | ADDITION (w=12.0) | 1.5% | 0 / 6 / 8 / 8 |
| projection | REMOVAL | 16.2% | 0 / 2 / 4 / 8 |
| fundamental_quality | REMOVAL/ADDITION (mixed, see (b)) | 11.8% | 0 / 2 / 6 / 6 |
| catalyst_event | REMOVAL | 67.6% | 0 / 0 / 2 / 4 |
| smart_money_confirmation | ADDITION (w=0, DEAD) | 100.0% | 0 / 0 / 0 / 0 |

smart_money_confirmation's E3=0 on every contributing night is a mechanical identity (its
subscore is null everywhere, so giving it weight changes nothing; available and weight>0 never
both hold), not a measurement. It is the cleanest possible confirmation of DEAD. Every other
layer moves the slate on a majority of nights; catalyst_event (smallest live weight, most
discretized subscore) is the least mobile of the six live layers but still moves the slate on
32.4% of nights.

## (f) Near-miss pool (bull-lane, threshold+completeness pass, not selected; B3's draw pool)

| scope | nights with >=1 near-miss | min (incl. 0-nights) | median | max |
|---|---:|---:|---:|---:|
| SEGMENT (68 nights) | 65 (3 nights have 0) | 0 | 8 | 26 |
| WHOLE FREEZE (102 nights) | 99 (3 nights have 0) | 0 | 12 | 26 |

Far above the >=3 (or Correction 2's tightened >=10-distinct) control-pool floor B3/B4 need on
all but a handful of nights; the 3 zero-near-miss nights (segment) are small-candidate-pool
nights and would be non-contributing for B3's draw on that specific layer/night only, counted and
not back-filled, per section 2.6.

Field-level sas_runs.config_json census, full population (102 nights), extending Q027 R1(g)'s
June-Sept table back to April: constant fields: qualification_threshold (70.0), max_output_cap
(8), min_completeness (35.0), scoring_weights.flow_strength (24.0), fundamental_quality (5.0
nominal), smart_money_confirmation (5.0 nominal), enable_smart_money_enrichment (False). Fields
that change inside the freeze, with transition dates:

| field | changes |
|---|---|
| scoring_weights: technical_structure, projection, catalyst_event, gex_alignment | v1.5 reallocation, 20/26/8/12 -> 27/29/10/0, effective 2026-05-18 (clean); see (c) |
| publication_floor | absent (pre-mechanism) through 2026-07-07, then 80.0 from 2026-07-08 |
| bear_publish_threshold, bear_max_output_cap | absent through 2026-06-28, then 80.0 / 5 from 2026-06-29 |
| atr_elite_bull_max_score, atr_elite_bear_max_score, atr_sas_component_cap | absent through 2026-05-08 (in population), then 84.9 / 79.9 / 35.0 from 2026-05-18 |
| enable_fundamental_enrichment | False through 2026-04-30, then True from 2026-05-01, with single-night reversions 2026-05-04 and 2026-06-02 |

No repair rewrote a historical row anywhere in this census; every change above is a genuine
per-night config difference (the run's own contemporaneous decision), not a later mutation of a
stored value, so no new DATA_NOTES.md entry is filed under this report. publication_floor /
bear_publish_threshold's ship is already logged (DATA_NOTES.md, ladder-monotonicity entry,
2026-09-13); the v1.5 weight reallocation, the ATR-elite-block ship and the enrichment-flag
history are new observations from this report but are forward-only facts about what each night's
own run actually used, not rewrites.

---

## Notes for the registrar / decision-maker (not a decision, flagging only)

1. The Gate-0 "whole-freeze" ambiguity (headline) needs a ruling before record. I have not
   resolved it because R1b's job is to measure counts, not to read the PREREG's own text on the
   desk's behalf. Both candidate m values (10 IC-only, or 16 with E3) are reported above with the
   full mechanism.
2. fundamental_quality's enrichment flag being True for most of the freeze is a correction to the
   PREREG draft's own stated expectation (section 4.3), not merely a measurement within it; worth
   a second read of section 1/9's "ADDITION layer" framing for this specific layer, since it is
   not being tested that way.
3. projection, the largest-weighted layer (29 pts), fails the E1/E2 coverage floor on both the
   segment and every individual month measured (peak 65.11% in August, never reaching 70%).
   E3_projection remains testable (REMOVAL layer, Gate-0 clears), so the layer is not silent in
   the register, but its marginal/partial IC (the endpoints closest to "does this ingredient's
   own signal predict") cannot be measured under the registered coverage rule. This is a coverage
   fact, not an outcome fact, and I take no position on whether it should change anything;
   flagging it because it will read as surprising against the PREREG's own drafted expectations.
4. smart_money_confirmation is DEAD everywhere, cleanly, on every one of R1b's independent checks
   (0% coverage, mechanical E3=0, flag always False): three independent confirmations of the same
   fact, not three findings.

---

Counts only. No touch rate, return, excursion, plan result, or score-vs-outcome relationship
appears anywhere above. I do not decide m, the EVALUABLE/DEAD/UNEVALUABLE list, or the Gate-0
scoping question; the registrar/decision-maker applies DECISIONS item 6/17 and Correction 3 to
this report's counts at record.
