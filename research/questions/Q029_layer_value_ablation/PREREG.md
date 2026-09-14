# Q029 — layer_value_ablation: which of the seven scoring layers actually earns its weight?

**Status:** PREREG_DRAFT (lock by committing this file; `--by desk`, DP-46). Every decision is applied
from `DECISIONS.md` (decide + record passes, 2026-09-14); **no item is pending and nothing blocks the
lock.** Of the three routed items, R1 was never re-routed (it is Q027's, borrowed — §5.2), **R1b is
CLOSED** (delivered 2026-09-14; it fixed `m` = 16 and it was the one blocker), and R2 (the shared
successor freezes) is due **before** the decision pass and is not a blocker (DP-23).
**Decisions:** DECISIONS.md (2026-09-14) · exposure basis (borrowed, §5.2):
`research/reports/STEWARD_Q027_exposure.md` (R1, item (a)) · feasibility basis (fixes `m`, §5.3):
`research/reports/STEWARD_Q029_feasibility.md` (R1b, counts only) — both measured on the pinned
freeze; **no live query stands behind any number in this file** (DP-50(c)).
**Family:** **F1 Selection edge** (hypothesis **H-075**, Haci's H5 *Ingredient value*, with **H-003**
(layer ablation) and **H-020** (GEX, the weight-0 layer) folded in and marked *merged into Q029* in
`research/BACKLOG.md`, DP-29). The deciding subject is which candidates reach the published slate, so
the family is selection (DP-29); the two rank-correlation endpoints additionally carry a **required
companion BH correction across F2** (§7), because they are computed on Q027's machinery.
**Manifest (selections — sealed panel, R1b counts, Gate-0 rehearsal only):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA
fa70688bc252d14f8d67e371afafc194731c324e) — **for provenance, the sealed post-hoc panel (§6) and R1b's
counts-only feasibility measurement (§5.3) only.** No night that carries a verdict here exists in it.
**Manifest (prices — same standing):** research/data/manifest_prices_v001.json (as_of: 2026-09-10;
base_manifest_sha256 b03f355a…bef374).
**Successor freezes — the question itself (built and pinned at the decision date, DP-23; §5.4 R2):**
`manifest_v00N` (selections: `sas_candidates` **for every candidate row, published and unpublished**,
including `score_details_json` and `missing_data_json`; `sas_runs` including **per-night**
`config_json`; `market_regime_daily`) and `manifest_prices_v00N` (daily bars for **every candidate
symbol on every in-window night**, published or not, plus DP-23's hourly bars for published symbols),
covering pick nights **2026-09-15 .. 2027-03-05** with daily bars through **2027-04-05** (session t+20
of the last included pick night) and ≥ 60 prior sessions before 2026-09-15; a second pair **only if**
the single DP-13 extension fires, covering pick nights **.. 2027-04-19** with bars through
**2027-05-17**. **The primary window is entirely prospective: not one night that carries a verdict
here exists in `manifest_v001`**, so the population enters *only* through those successor freezes,
which the desk pins at the decision date (`pin_at_decision`, DP-23 — the Q024 / Q027 pattern). They are
named here and deliberately **not** written as `**Manifest …:**` header lines, because no such file
exists yet and the pin step reads every `**Manifest` line as a path.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates` ∪
`non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, DP-22)
**unioned with the add-only successor exclusions file** issued with the successor selection freeze —
the identical three lists, built by the identical criteria, covering nights after 2026-09-10, **plus a
fourth list, `payload_disabled_runs`**, adopted with Q027's machinery (§2.0; Q027 DECISIONS item 11: a
night on which *every* published row carries `public_payload_json.analysis_status = "disabled"` or no
`lane_plans` object at all, i.e. zero screened `d_L3` survivors, is excluded whole). The successor file
may only **add** nights; no night is ever removed from a v003 list; the **criteria** are fixed at this
lock even though the **dates** cannot be. Both paths are `eval.py` inputs; no hard-coded file name, no
hard-coded date. DP-04 applies mechanically on top.
**Code read for definitions:** the read-only platform repo at the frozen SHA
`fa70688bc252d14f8d67e371afafc194731c324e` (`git show fa70688:<path>`), never HEAD.
**Shared machinery:** the population screens, the night's common ATR distance `d*_t`, the entry, the
clock, the grading rules and the contributing-night definition are **adopted from
`research/questions/Q027_score_ranking_validity/PREREG.md` §2.1–§2.5 by reference, exactly as Q027
registers them after `research/questions/Q027_score_ranking_validity/DECISIONS.md` (2026-09-14) is
applied** (§2.0). One machinery, two questions.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14

---

## 1. Hypothesis (plain English)

**Of the seven ingredient scores SAS blends into its 0–100 number, only some carry information that is
not already in the others: for a layer that does, ranking candidates by that ingredient alone predicts
which ones reach a target the same distance away, the prediction survives being told what the other
six ingredients say, and taking the ingredient's weight out of the recipe makes the published slate
measurably worse.**

BACKLOG **H-075** (Haci's H5) reads: *"which layers carry independent predictive information — PASS a
layer has stable OOS IC and/or its removal materially hurts the slate's net expectancy; FAIL a layer
adds no incremental OOS value → remove or demote it."* **H-003** reads: *"drop each weighted layer,
re-rank, out-of-sample return — baseline: full v1.6 — mechanism: dead layers add noise."* **H-020**
reads: *"GEX alignment (weight 0) vs day-lane outcome — baseline: GEX-missing picks."* All three are
the same experiment run over a different subset of the same seven columns, and running them as one
question is what keeps the multiple-testing denominator honest (§7).

**Three endpoints per evaluable layer** (§4), all night-level, all two-sided. **The evaluable register
is closed at `record` from R1b's counts and `m` = 16** (§4.3, DECISIONS items 6 / 22): three endpoints
each for `flow_strength`, `technical_structure`, `gex_alignment` (an ADDITION test at the **measured**
weight 12.0), `fundamental_quality` (a REMOVAL layer, as measured) and `catalyst_event`; **`projection`
carries E3 only** (its subscore clears the 70% coverage floor in no month measured, so its two IC
endpoints are UNEVALUABLE); **`smart_money_confirmation` is DEAD on all three** (0.00% non-null
everywhere, so adding weight to it changes nothing by construction).

- **E1ⱼ — the marginal IC.** The mean per-night Spearman rank correlation between layer `j`'s subscore
  and the **path outcome** — *whether and when* a target placed at the night's common ATR distance
  `d*_t` is first touched within 20 sessions from the session t+1 open — across every eligible
  candidate that night. **MPE `|ρ̄| ≥ 0.05`** (§4.3).
- **E2ⱼ — the partial IC.** The same statistic **given the other retained layers**: the per-night
  partial rank correlation of layer `j` with the path outcome, controlling for the other layers'
  ranks. This is H-076's **contribution limb**, which Q028 explicitly does not test. **MPE
  `|ρ̄_partial| ≥ 0.05`.**
- **E3ⱼ — the leave-one-layer-out re-ranking.** Recompute `overall_score` from the frozen subscores
  with layer `j`'s effective weight set to 0 (or, for a layer that already carries weight 0 in
  production, **set to its nominal weight** — §4.2), replay the platform's own selection
  (`_qualify_lane`, volatilx `services/super_agent_select_scoring.py:1489-1550`), and measure the
  change in the slate's **within-night control-adjusted L3-touch rate** (`E_t`, Q006 §3 construction).
  **MPE ±5.0 pp (DP-20).**

**Direction of the claim, written out because the sign is easy to misread.** `E3ⱼ` is always
**ablated minus production**. For a layer that carries weight in production (a *removal* layer), the
layer earns its weight when `E3ⱼ < −5.0 pp` — taking it out makes the slate worse. For a layer at
weight 0 in production (an *addition* layer), the layer would earn a weight when `E3ⱼ > +5.0 pp` —
putting it in makes the slate better. **As measured on the sealed segment (R1b(b), §2.3): REMOVAL for
`flow_strength`, `technical_structure`, `projection`, `catalyst_event` and `fundamental_quality`;
ADDITION for `gex_alignment`** — and the draft's expectation that `fundamental_quality` would be
weight-0 (`services/super_agent_select_models.py:110-111`) is **contradicted by the measurement**:
`enable_fundamental_enrichment` was True on 67 of 68 segment nights. **Every endpoint is registered
two-sided**: a removal layer whose deletion *improves* the slate is the most consequential outcome
this question can produce, and §9 says exactly what follows from it.

**What is not in this question.** The composite `overall_score` IC is **Q027's E1 and is not
recomputed here** (§7). The **structure** limb of H-076 — correlation, factor count, conditional
redundancy among the layers — is **Q028's and is not recomputed here**; Q029 computes each layer's
in-window `R²` on the others only as the partial IC's own identification check (§4.3), from its own
window, never from Q028's register. Leave-**two**-layers-out and any refitted weight vector are out of
scope and are named as successors (§10 threat 3).

## 2. Population

### 2.0 What is adopted from Q027, and why the two questions share one machinery

The following are **adopted verbatim** from `research/questions/Q027_score_ranking_validity/PREREG.md`
as that file stands once its `DECISIONS.md` (2026-09-14, six items decided and six corrections) is
applied by `@registrar apply Q027`: **§2.1** the eligible-row SQL and the "every score is in scope"
rule; **§2.2** the night's common ATR distance `d*_t` and the synthetic target `T_i`; **§2.3** the
entry `X_i`, the 20-session clock, `hit_i`, `s_i` and the path-outcome rank `u_i`; **§2.4** every
exclusion with its counted reason, including the `mixed`-direction rule, the 60-prior-bar screen, the
gradeability screen, the split-scale payload screen and the 25% / 10% night thresholds; **§2.5** the
contributing-night rule (≥ 30 eligible rows, a defined `d*_t`, matured to t+20) and the **episode**
(one symbol's run of eligible candidate appearances with gaps ≤ 10 sessions).

Three reasons this is a reference and not a copy. **(a)** The two questions must not disagree about
which rows exist: Q027 asks whether the composite orders outcomes and Q029 asks which ingredient does,
on the same nights with the same targets, and a difference in either answer must come from the
ranking variable and nothing else. **(b)** One `d*_t` means one distance-matched control (rule 5) for
both, so no touch rate from either question is quoted against a distance the other did not use.
**(c)** It is what lets the Steward's single Q027 exposure count serve both (§5.2), rather than
routing a second count for an identical funnel.

**The shared lock gate is CLEARED, on Q027's measurement and not on a second one.** Q027's R1 measured
**0.6761 contributing nights per elapsed session (48/71)** against the **≥ 0.36** inequality (80 nights
over the elapsed sessions still admissible under DP-43's 12-month ceiling at a 2026-09-14 lock,
re-solved at the actual lock date and unchanged) — clear by 88%, so **both questions lock**. Had it
been below, **Q029 would have gone to `research/questions/DEFERRED.md` with Q027**, on the same
measurement and without a second request. The funnel is the same funnel, so Q029 also adopts Q027's
**window, decision date, extension date and hard stop whole** (§5.5) and computes no date of its own
that could land earlier.

### 2.1 Units

- **Unit of inference: the trading night** (rule 6), for every endpoint. Candidate rows are reduced to
  one statistic per night first; nights are the observations. Control rows and Monte-Carlo placebo
  draws never add to n.
- **The row inside a night** is a scored candidate (`sas_candidates`), published or not, for E1 and
  E2; and a slate member or its matched control for E3.

### 2.2 Source tables and the columns this question adds to Q027's list

Everything in Q027 §2, plus — and these are the columns that make the ablation computable at all:

- `sas_candidates.score_details_json` → **`weighted_dimensions[<layer>].{available, weight,
  base_weight, score}`**, written by `_serialize_score_details` (volatilx
  `services/super_agent_select_service.py:306-336`) from the scorer's own loop
  (`services/super_agent_select_scoring.py:1329-1340`). **`weighted_dimensions[j].weight` is the row's
  own point-in-time effective weight for layer `j`** — the output of `_effective_dimension_weights`
  (`:682-722`) after the timeframe multiplier, the enrichment flags and the source-origin tests have
  been applied. It is stored, so the ablation needs no reconstruction of the run's context packet.
- `sas_candidates.missing_data_json` — the missing-data flags `_compute_missing_penalty`
  (`:725-748`) reads. This matters: the missing-data penalty **is a function of the weight vector**
  (`:745` skips a flag whose dimension carries zero weight), so an ablation changes it mechanically.
- `sas_candidates` seven subscore columns, `completeness_score`, `cross_layer_bonus`,
  `conflict_penalty`, `missing_data_penalty`, `best_timeframe`, `dominant_direction`, `qualified`,
  `threshold_pass`, `selected_rank`, `qualification_reason`, `source_membership_json`.
- `sas_runs.config_json` — **per night**: `scoring_weights`, `timeframe_weight_multipliers`,
  `qualification_threshold`, `publication_floor`, `max_output_cap`, `min_completeness`,
  `bear_publish_threshold`, `bear_max_output_cap`, `timeframe_thresholds`,
  `enable_fundamental_enrichment`, `enable_smart_money_enrichment`, `atr_elite_block_enabled`,
  `atr_elite_bull_max_score`, `atr_elite_bear_max_score`, `missing_data_penalties`. The replay uses
  **the night's own config**, never a constant written into `eval.py`.
- `prices_daily_split` — `C_t`, ATR14, `beta60`, `atr_pct`, `runup20`, `mom20`, `adv20`, forward bars
  t+1..t+20, SPY tape. `prices_daily_raw` — split-factor snapping only. **No hourly bar is used and no
  endpoint depends on one.**

**No outcome column is ever an input** (Q027 §2): `outcome_*`, `level_hit_*`,
`sas_selection_excursion.*` and `uoa_symbol_daily.fwd_return_*` are never joined. Every outcome here
is computed from pinned bars.

### 2.3 The seven layers, and which of them is a removal test and which an addition test

| layer | subscore column | scorer | base weight v1.6 | production effective weight |
|---|---|---|---|---|
| projection | `projection_score` | `:925` | 29.0 | live (0 where no projection origin and no projection context — `:711-712`) |
| technical_structure | `technical_structure_score` | `:831` | 27.0 | live |
| flow_strength | `flow_strength_score` | `:751` | 24.0 | live (0 where no flow origin and no flow context — `:713-714`) |
| catalyst_event | `catalyst_event_score` | `:1014` | 10.0 | live where catalyst context present (`:717-718`) |
| fundamental_quality | `fundamental_quality_score` | `:979` | 5.0 | 0 whenever `enable_fundamental_enrichment` is false (`:707-708`; default `False`, `services/super_agent_select_models.py:110`) — but **measured True on 67 of 68 segment nights**, so this is a **REMOVAL** layer (R1b(b)) |
| smart_money_confirmation | `smart_money_confirmation_score` | `:1051` | 5.0 | **0 whenever `enable_smart_money_enrichment` is false** (`:709-710`; default `False`, `:111`; PI-008) — measured False on **all 102** nights and the subscore null on every row: **DEAD** (§4.3) |
| gex_alignment | `gex_alignment_score` | `:882` | **0.0** | **0 always** (`services/super_agent_select_models.py:9-17`: kept in the dict at 0.0 so the subscore is still computed for audit visibility) — measured 0.0 on 100% of segment rows: an **ADDITION** test at the measured weight **12.0** |

Base weights: `_default_scoring_weights`, `services/super_agent_select_models.py:8-22`. Timeframe
multipliers: `_default_timeframe_weight_multipliers`, `:37-66` (`fundamental_quality` runs
0.15 / 0.35 / 1.00 and `smart_money_confirmation` 0.2 / 0.3 / 0.7 across short / swing / long, so the
two flag-gated layers would be small even with their flags on).

**The direction rule, deterministic and per night per layer (fixed at lock):** layer `j` is a
**REMOVAL** test on night `t` if its production effective weight is `> 0` on at least one eligible row
that night, and an **ADDITION** test if it is `0` on every eligible row. **The rule governs `E3ⱼ`
only** (DECISIONS Correction 1): `E1ⱼ` and `E2ⱼ` are rank correlations of a **subscore**, whose
ordering information does not depend on the weight that subscore carries, so they are computed over
**all** of the layer's contributing nights regardless of its effective weight, with the REMOVAL /
ADDITION split reported as a **descriptive stratum** subject to the ≥ 20-night rule. For `E3ⱼ`, a layer
whose nights split between the two is **two different tests and is never pooled** — the REMOVAL nights
and the ADDITION nights are separate endpoints, each with its own floor (the DP-06 "two different
features" pattern applied to a weight vector) — **except that a side R1b projects below 80 contributing
nights inside the window is declared UNEVALUABLE at `record`, counts only, no verdict, not in `m`**,
and the other side is that layer's E3 endpoint (§4.3, DECISIONS item 16).

**As measured by R1b(b) on the 2026-06-01..2026-09-10 segment, and now closed (DECISIONS item 23): no
split survives, and the assignment is per layer.** REMOVAL on **68 of 68** segment nights:
`flow_strength`, `technical_structure`, `projection`, `catalyst_event`. ADDITION on 68 of 68:
`gex_alignment` (production weight 0.0 on 100% of segment rows) and `smart_money_confirmation` (DEAD,
not tested). **`fundamental_quality` is a REMOVAL layer** — `enable_fundamental_enrichment` measures
True on **67 of the 68** segment nights (81 of 102 population nights), contrary to the draft's own
expectation from the dataclass default; its **single ADDITION night, 2026-06-02**, projects to **1.2
contributing nights** at 119 sessions and is therefore **UNEVALUABLE, not in `m`** — and that night
also carries the `payload_disabled_runs` signature the §2.0 machinery excludes whole, so it is out on
two independent grounds.

**The addition weight** for an ADDITION test is `base_weight × that night's timeframe multiplier for
the row's `best_timeframe``, taken from the night's own `config_json` — i.e. the weight the layer
*would* carry if its gate were open. For smart-money and fundamental that is 5.0 × the multiplier,
already in the config. **For GEX the config value is 0.0 and there is no nominal in v1.6**, so the
addition weight is the value of `scoring_weights.gex_alignment` in the **last `sas_runs.config_json`
dated before the v1.5 ship of 2026-05-14**, read from the pinned `manifest_v001` freeze by R1b — a
measurement, not an assumption (DP-50(c): never a live query).

**Measured, and registered: the GEX addition weight is `12.0`** (R1b(c); DECISIONS item 2 / item 23 /
Correction 9). The last population config dated before 2026-05-14 is **2026-05-08 → 12.0**, and only
**two** distinct values appear anywhere in the frozen history (12.0 through 2026-05-08, 0.0 from
2026-05-18). The registrar's arithmetic on the code comment
(`services/super_agent_select_models.py:9-13`: *"technical_structure 20→27, projection 26→29,
catalyst_event 8→10 absorb the reallocation"*, i.e. +7 +3 +2 = 12, and 24+20+26+5+8+5 = 88 with 12
making 100) agrees, and is kept here as a **corroborating remark only, never as the registered basis**;
**the draft's "if no night carries a non-zero value" fallback branch did not fire and is struck.** A
weight-sensitivity curve at `w ∈ {5, 12, 24}` is printed beside every ADDITION E3 as a descriptive
companion that **never decides** (§4.4).

### 2.4 The ablated score — exact arithmetic, and what is held fixed

For row `i` on night `t` and layer `j`, from that row's stored `weighted_dimensions` and the night's
`config_json`:

```
production (reconstruction, Gate 0):
  W        = { w_k = weighted_dimensions[k].weight }                     for the 7 layers
  A        = { k : weighted_dimensions[k].available AND w_k > 0 }
  avail_w  = Σ_{k∈A} w_k ;  total_w = Σ_k w_k  (or 1.0 if 0)            (:1322-1347)
  base     = ( Σ_{k∈A} score_k · w_k ) / avail_w                         (:1348)
  compl    = clamp( avail_w / total_w × 100 )                            (:1347)
  miss     = Σ_{flags f set in missing_data_json, dim(f) has w>0} penalty_f   (:740-747)
  gex_off  = 5.0 if score_gex is null else 0.0                           (:1390)
  overall  = clamp( base + cross_layer_bonus − conflict_penalty − miss + gex_off )   (:1393-1399)
  then the ATR-elite cap, re-applied exactly as stored (below)           (:1401-1423)

ablation of layer j:   W' = W with w_j := 0      (REMOVAL)
                       W' = W with w_j := base_weight_j × multiplier(best_timeframe)  (ADDITION)
                       everything else recomputed from W' by the identical formulas.
```

**Held fixed at their production values, never recomputed:** `cross_layer_bonus` (`:1078`),
`conflict_penalty` (`:1116`), every subscore (including the ATR projection cap at
`atr_sas_component_cap`, which is already baked into the stored `projection_score` — `:1300-1314`),
and the **ATR-elite block decision**: if the row's stored `score_details_json.atr_elite_block_applied`
is true, the same cap (`atr_elite_bull_max_score` / `atr_elite_bear_max_score` per
`dominant_direction`) is re-applied to the ablated score; if false, no cap is applied. The block's own
confirmation count (`_count_strong_non_projection_layers`, `:97-119`) is a function of subscores, not
of weights, so holding it fixed is exact for a weight-only ablation. **This is the weight-only
ablation** — the counterfactual "the same engine with this layer's weight set to zero", which is the
change a brief would actually ship. The fuller "layer removed everywhere" variant (also struck from
the elite-block confirmation set and from the cross-layer bonus's evidence) is a **descriptive
sensitivity** printed beside it and never decides (DECISIONS item 3).

**Gate 0 — the reconstruction positive control, run first and read first.** `eval.py` recomputes
`overall_score` at the **production** weight vector by the arithmetic above and compares it to the
stored `overall_score`. A row agreeing within **0.05** is *reconstructable*. A night is
**non-contributing for E3** (counted, not excluded) unless **≥ 99% of its eligible rows are
reconstructable** and `weighted_dimensions` parses on **≥ 95%** of them. `eval.py` **fails loudly** if
the whole-**window** reconstruction rate is below **95%**, or on any single in-window night below 99%,
because below that the ablation is not measuring the platform's arithmetic. The rate, the per-night
distribution and the residual distribution are printed. **No Gate 0 target is ever relaxed to make a
pass succeed, and none was.**

**The rehearsal ran before the lock (R1b(d)), and the E3 limb exists** (DECISIONS items 17 / 21,
Correction 7). **The evaluability determination is made on the 2026-06-01..2026-09-10 segment** — the
engine vintage this question's window belongs to (DP-06 / DP-50(a), Correction 3's own scoping) — where
reconstruction measures **100.00%: 68 of 68 nights, every night at or above 99%, zero exceptions**, and
the slate replay (§2.5) disagrees on **0.00%** of segment nights. **The whole-freeze figure from
2026-04-01 is 84.77% and is printed here with its mechanism, deciding nothing**: rows before
~2026-05-11 carry an **8-key** `score_details_json` with no `atr_elite_block_applied` and no
GEX-missingness offset, and every non-reconstructing row resolves to a residual of exactly **+5.00** —
the `fa70688` formula applied to an engine two ships older; the **−7.00** residual tail is confined to
the same partial-schema era. That is a **different feature**, not a residual error, and it is
structurally absent from a window that is post-v1.5 by construction. **No PI is filed** (DP-07 not
engaged): the artefact is in the desk's rehearsal of a superseded engine, not in the engine that ran.
The two figures are **never quoted interchangeably**, and the in-window gates above are unchanged. Had
the segment rate fallen below 95%, or the replay disagreed on more than 1% of slate rows, **every
`E3ⱼ` would have been UNEVALUABLE at `record` and Q029 would have locked as an IC-only question**
(`m = 2L`, no weight brief, no CARRIES / HARMFUL / DECORATIVE label, a PI under DP-07 and H-003's
mechanism to DEFERRED). **That branch was not taken, and the measured rates are named rather than the
branch struck.**

### 2.5 The slate replay

For night `t` and layer `j`:

- **Lane.** The replay runs the **bull lane only** — `main = [c for c in scorecards if
  dominant_direction != 'bearish']` (`:1642-1649`), threshold
  `max(timeframe_thresholds.get(best_timeframe, qualification_threshold), publication_floor)`,
  `completeness_score ≥ min_completeness`, cap `max_output_cap`, sort key
  `(−overall_score, symbol)` — the platform's own `_qualify_lane` (`:1509-1548`), replayed with the
  night's own config. **The bear lane is held at its production membership and enters neither slate**
  (`bear_publish_threshold`, `bear_max_output_cap`, `:1659-1671`); bearish picks are excluded and
  counted. The reason is that the two lanes have independent caps, so a bull ablation cannot move a
  bear slot, and pooling them would put a second, differently-gated population inside one endpoint. It
  is also forced by rule 6: bear-contributing nights ran at 0.157 per session (BACKLOG H-062), so a
  bear E3 endpoint could not reach 80 nights in any window inside DP-43's ceiling. **Binding on the
  report: every E3 verdict sentence says "the published *bull* slate", never "the slate"** (DECISIONS
  item 18).
- **Each night's own config is honoured literally, and the dataclass default is never substituted**
  (DECISIONS Correction 15). An **absent** key means that gate **did not exist that night** — an absent
  `publication_floor` is a floor of **0.0**, not today's 80.0 — and the same rule applies to
  `bear_publish_threshold`, `bear_max_output_cap` and the ATR-elite caps. R1b(e) found **56 of 102
  nights' `config_json` lack `publication_floor` entirely** (all pre-2026-07-08), where substituting the
  current default produced **spurious** disagreement. Inside Q029's own window the point is moot
  (`publication_floor` = 80.0 has been live since 2026-07-08); the rule governs the sealed descriptive
  panel and makes `eval.py` deterministic rather than version-dependent.
- **`S^prod_t`** = the replayed production slate; **`S^abl_t,j`** = the slate the ablated score
  selects. `eval.py` **fails loudly** if `S^prod_t` differs from the frozen published set
  (`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28) on more than **1%** of in-window
  slate rows — that disagreement would mean the replay is not the platform's selection. Rows the
  platform published under a `qualification_reason` the replay cannot reproduce (`selected_dark`, the
  sub-80 v2 bear markers, `:1553-1565`) are listed and counted. **Rehearsed before the lock (R1b(e)):
  the replay disagrees on 0.00% of the 68 segment nights, none above the 1% gate**; the 12 discordant
  nights in the freeze are all April, all pre-dating the 2026-07-02 bear-lane split, and are the
  single-lane counter rather than a replay failure (§6).
- **Overlap is printed, always**: per night per layer, `|S^prod ∩ S^abl|`, the discordant count
  `k_{t,j} = |S^abl \ S^prod|`, and the share of nights with `k_{t,j} = 0`. A layer whose ablation
  changes no slate on any night has `E3ⱼ ≡ 0` by mechanical identity, and that is a **finding, not a
  measurement failure** (§8).

### 2.6 Contributing nights (DP-21's floor unit), per endpoint

- **E1ⱼ / E2ⱼ:** a **Q027 §2.5 contributing night** (≥ 30 eligible rows, defined `d*_t`, matured,
  non-excluded) that additionally carries **≥ 30 eligible rows with a non-null `subscore_j` and
  non-zero within-night variance in it**; for **E2ⱼ**, additionally every one of the night's
  **retained** layers (the Q028 §4.0 coverage rule, restated in §4.3) non-null on those rows.
- **E3ⱼ:** a Q027 §2.5 contributing night that additionally (i) passes §2.4's Gate-0 night rule,
  (ii) has `|S^prod_t| ≥ 1`, and (iii) has **≥ 10 distinct same-night candidates in that night's §3 B4
  distance-matched control pool** — the night's eligible rows in **neither** slate — **for every pick
  in `S^prod_t ∪ S^abl_t,j`**. Ten is the number B4 actually draws; drawing 10 controls with
  replacement from a pool of 3 gives three distinct names replicated, which is not the distance-matched
  control rule 5 requires (DECISIONS Correction 2). A night failing (iii) is non-contributing and
  counted, **never back-filled by widening the match**. The cost is nil as measured:
  `STEWARD_Q023_exposure.md` §6 gives a mean of **51.8** same-night non-published rows passing the Q006
  match screens (median 54, **min 39**).
  **This floor is on B4's control pool and on nothing else** (Correction 12). It imposes **no floor on
  B3's near-miss placebo pool**, which R1b(f) measures at **min 0 (3 of 68 nights), median 8, max 26**;
  read onto that pool it would strike roughly half the nights and defer the question on a bookkeeping
  artefact. `k_{t,j} ≤ |near-miss pool|` by construction, so B3's draw is always feasible, an empty pool
  forces `k_{t,j} = 0`, and such a night still contributes with `ΔE* = 0` (§3 B3, DECISIONS item 7).
- **Episode (DP-51):** Q027 §2.5's definition for E1/E2 (one symbol's run of eligible **candidate
  appearances**, gaps ≤ 10 sessions); for E3, one symbol's run of appearances **in the union of the
  two slates**, same gap rule. Every row belongs to exactly one symbol-episode per endpoint.

## 3. Baselines — what each endpoint must beat

There is a baseline for every endpoint and none of them is a pooled remainder.

- **B1 — the within-night subscore permutation (E1ⱼ's null).** For each night, permute
  `subscore_j` across that night's eligible rows, recompute `IC_{t,j}`, average over nights; 10,000
  permutations, seed 20260914, two-sided. Under it `E[E1ⱼ] = 0` by construction. This is the exact
  counterfactual "this ingredient carries no ordering information, the outcomes are what they are".
- **B2 — the residual permutation (E2ⱼ's null).** For each night, regress the mid-ranks of
  `subscore_j` on the mid-ranks of the other retained layers, permute the **residual** across rows,
  re-add the fit, and recompute the partial IC. This destroys layer `j`'s own contribution while
  preserving both its relationship to the other layers and their relationship to the outcome — the
  null H-076's contribution limb names and the one a plain permutation would get wrong.
- **B3 — the placebo swap (E3ⱼ's null), and the baseline H-003 does not have.** For each
  E3-contributing night, draw `k_{t,j}` symbols uniformly from the **near-miss pool** — bull-lane
  candidates that pass the night's threshold and completeness gates but were not selected — replace
  `k_{t,j}` uniformly chosen members of `S^prod_t`, and recompute `E_t`. 2,000 draws per night per
  layer, seed 20260914. This is "what a swap of this size and this provenance is worth when it carries
  no information", and it is what stops a confirmed E3 being a statement about swap size. **B3 draws
  are Monte Carlo and never add to n** (rule 6). `E3ⱼ` is reported **raw and placebo-adjusted**
  (minus the night's placebo mean), and **the placebo-adjusted value is the one that must clear the
  MPE** (§8 clause 5).
  **The draw is always feasible, and a thin pool is flagged rather than dropped** (DECISIONS item 24 /
  Correction 12). `k_{t,j} ≤ |near-miss pool|` by construction — the ablated slate is the top-`|S|` of
  the same passing set, so a swap needs an entrant from that pool — therefore a draw of `k_{t,j}`
  symbols always exists; an **empty** pool forces `k_{t,j} = 0` and the night contributes `ΔE* = 0`
  (item 7's diluting choice). A night whose near-miss pool holds **fewer than 10 distinct names** prints
  a **`DEGENERATE_PLACEBO`** flag with its pool size — the 2,000 draws are then near-exhaustive and the
  placebo mean close to determinate — and **still contributes**. **No night is ever back-filled by
  widening a pool or a match.** Measured: min 0 on 3 of 68 segment nights, median 8, max 26.
- **B4 — the rule-5 distance-matched control, inside `E_t` by construction.** For every pick in either
  slate, the **10 nearest** same-night candidates from the control pool by Q006 §3's Euclidean
  distance on night-median/MAD-standardized `beta60`, `atr_pct`, `runup20`, matched with replacement,
  ties by symbol ascending, each carrying a synthetic target at **the identical ATR distance `d*_t` in
  its own ATR units and the pick's direction**, graded by exactly the pick's rule. **Control pool** =
  that night's eligible rows in neither `S^prod_t` nor `S^abl_t,j` (so a pick is never its own
  control, in either arm). A touch rate from this question is never reported without this sentence
  attached.
- **B5 — the full v1.6 slate (H-003's own baseline).** `E3ⱼ` is always the ablated slate against **the
  production slate on the same night**, paired, never against a pooled or a historical rate.
- **B6 — the scale reference (descriptive, never decides).** The same per-night IC computed with
  `mom20` — the trailing 20-session return rank from pinned bars — in place of a subscore, on the
  identical rows, targets and clock (Q027 §3 B3's definition verbatim). It answers "is 0.05 a big
  number here" without a new freeze. **It is not a test of Q024 and confirms nothing about it** (§7).

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Nothing in this question is decided by a fixed-horizon return.** Close-to-close returns at T+5 and
T+20 from the entry, and the per-night return IC of every layer, are printed and are **descriptive by
rule 5 and DP-01**. That matters more than usual here: the prior art on this exact hypothesis — the
platform's own August layer audit (`docs/SAS_SCORING_RESEARCH_PLAN.md:53-67`) — is a table of
correlations against *hit and favourable excursion*, and §6/§10 threat 1 record what follows from the
registrar having read it.

### 4.1 Per night, per layer

Let `N_t` be night `t`'s eligible rows (Q027 §2.1), `u_i` the path-outcome rank (Q027 §2.3),
`d*_t` the night's common ATR distance (Q027 §2.2).

- **`IC_{t,j}` = Spearman ρ over `N_t` between `subscore_j` and `u_i`**, mid-rank tie correction on
  both variables.
- **`PIC_{t,j}` = the partial rank correlation** between `subscore_j` and `u_i` given the other
  retained layers: rank-transform `subscore_j`, `u_i` and each other retained layer within the night;
  OLS-residualize the first two on the rest; take the Pearson correlation of the residuals. The
  night's **variance-inflation diagnostic** `R²_{t,j}` (layer `j`'s `R²` on the other retained layers)
  is printed with it.
  **The retained set is named, and it is five: `flow_strength`, `technical_structure`, `gex_alignment`,
  `fundamental_quality`, `catalyst_event`** (§4.3's coverage rule applied to R1b(a); DECISIONS item 22 /
  Correction 10). So every evaluable `E2ⱼ` controls for **four** other layers — clearing §4.3's "≥ 3
  other retained layers" — and **`projection`, the largest-weighted layer in the engine at 29 points, is
  not among the controls**, because its subscore fails the 70% coverage floor. That is an interpretation
  constraint on every E2 result and it is **not optional**: the `R²_{t,j}` panel is printed on that set
  and §8's E2 verdict sentence names it.
- **`E_t(S)` = mean over `p ∈ S` of `hit_p` − mean over `p ∈ S` of the mean `hit` of `p`'s 10 matched
  controls** (§3 B4), in percentage points — Q006 §3's `E_t`, computed at `d*_t` so that both slates
  and both control sets are asked to travel the same distance.
- **`ΔE_{t,j} = E_t(S^abl_t,j) − E_t(S^prod_t)`**, and its placebo-adjusted form
  `ΔE*_{t,j} = ΔE_{t,j} − mean_B3(ΔE_{t,j})`.

### 4.2 Primary endpoints, per evaluable layer `j`

- **E1ⱼ = mean over E1-contributing nights of `IC_{t,j}`**, in Spearman-ρ units. **MPE `|ρ̄| ≥ 0.05`.**
- **E2ⱼ = mean over E2-contributing nights of `PIC_{t,j}`**, same units. **MPE `|ρ̄_partial| ≥ 0.05`.**
- **E3ⱼ = mean over E3-contributing nights of `ΔE*_{t,j}`**, in percentage points, sign convention
  **ablated minus production** (§1). **MPE ±5.0 pp (DP-20).**

**On the IC MPE.** `0.05` is **Haci's own number**, from the Master Hypothesis Program's H3 PASS line
(`research/reports/INBOX_2026-09-14_master_hypothesis_program.md` §1, H3: *"Mean daily Spearman IC
≥ 0.05"*), and it is **the same number and the same source Q027 registers** for the composite. DP-44
carries no MPE unit for a rank-correlation endpoint, and an autonomous run writes no DP entry from a
DEFAULTED item (DP-40), so the number is stated here with its source and applied as registered;
**Q027's own `DECISIONS.md` (2026-09-14) already carries the general rule** ("the MPE for any per-night
rank-correlation endpoint is 0.05 in Spearman-ρ units") as a **proposed standing entry** for Haci, and
Q029's `DECISIONS.md` restates it as the second question to need it — proposed, never assumed: until he
confirms it, the number stands here on its own source. Neither IC MPE is lowered at the decision pass in any branch,
including one where a CI excludes zero at 0.04 — that is what an MPE is for (rule 6).

**On the E3 MPE, and why DP-20's doubling clause is considered and not applied.** `ΔE_{t,j}` is
arithmetically a difference of differences, the shape that carried ±10.0 pp in Q022 E1, Q018 P4 and
Q012 P2 — but in those questions the two components were means over **different nights or different
picks**, independently estimated. Here the two `E_t`'s are computed **on the same night, from slates
that overlap on most members, against control sets drawn from the same pool at the same distance**, so
the pairing removes the night effect and almost all of the composition; the residual variance is the
variance of the discordant picks alone. A 10.0 pp bar on a quantity whose structural maximum is set by
the discordant share would return INCONCLUSIVE by construction rather than by evidence — the mirror of
the objection Q022 §8 raised in the other direction. ±5.0 pp is also the number **H-075 is written
with** (DP-25: units and cuts come from the hypothesis as written). DP-20's own larger-MPE licence is
scoped to *"an endpoint with **no control** (a raw arm contrast)"*, and `ΔE*_{t,j}` carries rule 5's
distance-matched control inside it by construction (§3 B4), so the licence does not reach it; the six
precedents that used 10.0 pp (Q007 P1, Q008 K1, Q012 P2, Q014 E1, Q022 E1, Q023 E1) each raised it for
**independently estimated components or small independent cells**, a premise that fails here
(DECISIONS item 1).

**The strict half of the alternative is kept as a blocking companion rather than as the MPE**
(DECISIONS item 1 / Correction 6). §4.4's **added-minus-dropped decomposition** — the undiluted
control-adjusted contrast of the picks the ablation adds against those it drops — is **computed and
blocking**: on a layer with **≥ 20 discordant contributing nights** it must carry the **same sign as
`E3ⱼ`**, and a contrast beyond **10.0 pp in the opposite sign blocks a CONFIRMED** (§8 clause 11).
Below 20 discordant nights it prints counts only and blocks nothing, and §8 clause 9's lead-with-the-
`k=0`-share rule carries the narrowness there.

### 4.3 Evaluability, and how `m` is fixed at lock

A layer-endpoint pair is **EVALUABLE** only if R1b (§5.3) measures, **on the 2026-06-01..2026-09-10
segment of the sealed freeze** and with no outcome in view:

> **Why the segment and not the whole freeze** (DECISIONS Correction 3 / item 21, decided before any
> count existed). The catalyst layer is a different feature before 2026-06-01 (DP-06), the enrichment
> flags and the weight vector both changed inside April–May, and the pre-v1.5 rows carry a partial
> `score_details_json` schema — so whole-freeze coverage would let sealed rows written by an engine two
> ships older mis-declare a layer that is alive in the prospective window, or alive one that is dead.
> The per-month series is printed beside every count so a coverage trend is visible; the April–May
> counts serve R1b(b)'s flag census and R1b(c)'s GEX weight **only** and decide no layer's
> evaluability. Item 6(iii)'s `UNREGISTERED_LIVE` clause below covers the residual risk in the
> direction that cannot inflate a claim.

- **for E1ⱼ:** `subscore_j` non-null on **≥ 70%** of candidate rows, **≥ 5 distinct values**, and
  non-zero within-night variance on **≥ 50%** of nights — the **Q028 §4.0 retained-layer coverage
  rule**, adopted verbatim so the two questions agree about which layers exist;
- **for E2ⱼ:** E1ⱼ evaluable, and at least **three other** layers retained on the same rows (a partial
  correlation controlling for one other layer is not the statistic H-076 names);
- **for E3ⱼ:** §2.4's Gate-0 rehearsal passes on the segment, and — **for an ADDITION layer only** — the
  layer's subscore is non-null on ≥ 70% of rows, since adding weight to a null subscore changes
  nothing by construction (`:1341` counts a dimension only when `available and weight > 0`). **The 70%
  clause binds E1ⱼ, E2ⱼ and ADDITION-E3ⱼ and never REMOVAL-E3ⱼ** (DECISIONS item 22): a layer already
  carrying weight in production is ablated out of an arithmetic that is running, whatever its coverage,
  and that is why `projection` keeps its E3 endpoint while losing its two IC endpoints. Its coverage is
  reported beside every `E3_projection` number so no reader takes the endpoint for a full-coverage one.

A pair that fails is **DEAD** (for a layer whose subscore is not computed in production) or
**UNEVALUABLE** (for a mechanical failure), is reported with its measured coverage, enters **no BH
set**, and carries **no verdict** — "the platform does not compute this ingredient" is a counted fact,
not a test result. **An E3 side (REMOVAL or ADDITION) that R1b projects below 80 contributing nights
inside the window is UNEVALUABLE at `record` on the same terms** — counts only, not in `m` — and the
other side is that layer's E3 endpoint (§2.3, DECISIONS item 16). **`m` = the number of EVALUABLE
layer-endpoint pairs, fixed at `record` from R1b's counts and never revised at the decision pass.** An
evaluable pair short of its floor at the decision pass still has its p computed and stays in `m`;
dropping it would lower the bar for the survivors (Q027 §7's rule). **A pair declared DEAD or
UNEVALUABLE at `record` is never added to `m` later**: if the successor freeze's own coverage counts
show a layer that was dead on the sealed freeze carrying usable variation inside the window, it is
reported as **`UNREGISTERED_LIVE`** — counts only, no verdict, no q — and named as a successor
question.

**The register, measured by R1b and closed at `record` (DECISIONS item 22; `m` = 16):**

| layer | E1 | E2 | E3 | measured basis (segment) |
|---|---|---|---|---|
| `flow_strength` | EVALUABLE | EVALUABLE | EVALUABLE (REMOVAL) | 99.88% non-null, 3,986 distinct, variance on 100% of nights |
| `technical_structure` | EVALUABLE | EVALUABLE | EVALUABLE (REMOVAL) | 100.00%, 1,216 distinct, 100% of nights |
| `gex_alignment` | EVALUABLE | EVALUABLE | EVALUABLE (**ADDITION**, w = 12.0) | 99.00%, 32 distinct, 100% of nights; production weight 0.0 on 100% of rows |
| `fundamental_quality` | EVALUABLE | EVALUABLE | EVALUABLE (**REMOVAL**) | 98.71%, 379 distinct, 98.5% of nights; flag True on 67/68 nights. Its **ADDITION side is UNEVALUABLE** (1 night → 1.2 projected) |
| `catalyst_event` | EVALUABLE | EVALUABLE | EVALUABLE (REMOVAL) | 100.00%, **8 distinct** (tie-structure reference mandatory, §4.4) |
| `projection` | **UNEVALUABLE** | **UNEVALUABLE** | EVALUABLE (REMOVAL) | subscore non-null on **62.74%** of segment rows, clearing 70% in **no month measured** (49.44% → peak 65.11%, plateauing below the floor from July). §4.3's 70% clause binds E1/E2 and ADDITION-E3 only, **never REMOVAL-E3** |
| `smart_money_confirmation` | **DEAD** | **DEAD** | **DEAD** | 0.00% non-null, 0 distinct values, flag False on all 102 nights; E3 ≡ 0 by mechanical identity (`:1341`) |

**`m` = 5 × 3 + 1 = 16**, fixed and never revised. **The draft's expectation is struck and kept in one
line so the contradiction is visible:** *"flow, technical, projection and catalyst evaluable on all
three; GEX evaluable on E1/E2 and an ADDITION test on E3; smart-money and fundamental expected DEAD or
ADDITION-only; `m` expected 12–15, bounded above by 21."* The measurement contradicted it twice —
**`projection` lost two of its three endpoints** and **`fundamental_quality` gained all three on its
REMOVAL side** — and 16 is inside Correction 1's bound (no layer has both E3 sides clearing 80, so the
bound is the plain 21). The larger `m` is the **stricter** BH denominator for every endpoint here (§7).

**The partial IC's identification clause, fixed at lock.** If layer `j`'s in-window mean `R²_{t,j}` on
the other retained layers exceeds **0.90**, `E2ⱼ` is declared **UNIDENTIFIED**: it is reported with its
`R²` and its CI as counts only, carries no verdict, and is removed from **nothing** — it was never in
`m`, because `m` is fixed at lock and the clause is evaluated on `eval.py`'s measured `R²`, which is
not an outcome. This is Q029's own check on its own window; **Q028's register is not consulted** for
it, so no post-lock path runs through another question's output.

### 4.4 Secondary, stratum and sensitivity output

Everything here prints raw p only and is labelled *"descriptive, does not decide"* — **except the
named blockers** (§8 clauses 6–11), which carry no verdict of their own but block a CONFIRMED when they
run the other way. Suppression restricts affirmative reporting only; it never removes a blocker, and a
suppressed cell never by itself makes an endpoint INCONCLUSIVE (Q027 DECISIONS Correction 2's rule,
adopted).

**Computed, and blocking:**

- the **binary-outcome** versions of E1ⱼ and E2ⱼ (Spearman ρ with `hit_i` in place of `u_i`) — clause 6;
- the **touch-within-5-sessions** version of E3ⱼ (DP-20 units; **not** a sessions-to-touch difference,
  which DP-44 leaves descriptive and gives no MPE — Q027 DECISIONS Correction 1's rule, adopted) —
  clause 6;
- the **"mixed graded long"** version of all three endpoints (Q027 §2.4) — clause 7;
- the **bull-only** version of E1ⱼ and E2ⱼ — clause 8 (E3 is bull-lane by construction, §2.5);
- **Half A / Half B** (§6) — the stability clause; it blocks at whatever count it has and is not a
  reported stratum;
- the **monthly-block panel** (calendar months with ≥ 10 contributing nights): H-075's *"stable OOS
  IC"* is implemented as clause 10 on the months, at ≥ 60% sign agreement, for E1ⱼ and E2ⱼ;
- the **placebo-adjustment** of E3ⱼ (§3 B3) — clause 5, which is where the adjusted value binds;
- the **added-minus-dropped decomposition** of E3ⱼ: the control-adjusted touch rate of the picks the
  ablation *adds* minus that of the picks it *drops*, on discordant nights, with its own night count —
  the undiluted form of the same contrast, reported because `E3ⱼ ≈ P(discordant) × (that contrast) ×
  k/|S|` and a reader is owed the factorization. **It is a blocker, not merely descriptive** (DECISIONS
  item 1 / Correction 6): on a layer with **≥ 20 discordant contributing nights** it must carry the same
  sign as `E3ⱼ`, and a contrast beyond **10.0 pp in the opposite sign blocks a CONFIRMED** — clause 11.
  Below 20 discordant nights it prints counts only and blocks nothing.

**Computed, mandatory, purely descriptive:**

- the **slate-overlap panel**: per layer, the share of nights with `k_{t,j} = 0`, the distribution of
  `k_{t,j}`, and the identity of the layers whose ablation never moves a slate. **R1b(e) measured the
  `k = 0` share per layer on the sealed segment** — flow 5.9%, technical 4.4%, gex 1.5%, projection
  16.2%, fundamental 11.8%, **catalyst 67.6%**, smart-money 100% — so on present evidence catalyst's
  share is above §8 clause 9's 50% line and **will lead its verdict sentence**; the in-window shares are
  what the clause actually runs on;
- the **fixed-denominator sensitivity** of E3ⱼ: the ablated `base` computed with `w_j` removed from the
  numerator but **not** from `avail_w`, isolating "losing layer `j`" from "up-weighting the others"
  (§10 threat 4);
- the **"layer removed everywhere" sensitivity** of E3ⱼ (§2.4);
- the **weight-sensitivity curve** for every ADDITION layer at `w ∈ {5, 12, 24}` (§2.3);
- the **two modifiers, descriptive only**: the same replay with `cross_layer_bonus` set to 0
  (`:1078`) and with `conflict_penalty` set to 0 (`:1116`), reported with `ΔE` and slate overlap,
  **no MPE, no q, no verdict** — H-012 owns the conflict penalty as its own open BACKLOG line and
  nothing here licenses a change to it (§9);
- the **agent-level cut, descriptive only**: `score_details_json` fields that resolve to a single
  agent, at Q028 §4.5's **90% parse-coverage floor per month**, with the same IC treatment. Haci's
  "10 agents" (`ai_agents/`: principal, projection_expert, expert, omega, earnings,
  option_flow_monitor, price_action, …) feed the layers rather than scoring separately, so no
  agent-level endpoint is a primary;
- the **tie-structure reference, mandatory and named in the verdict sentence for `gex_alignment` and
  `catalyst_event`** (DECISIONS Correction 11). R1b(a) measures **32** distinct `gex_alignment` values
  and **8** distinct `catalyst_event` values on 4,020 segment rows; an IC on an 8-level variable against
  a mostly-tied outcome rank is bounded well below 1. The per-night touch base rate, the tied-block size
  and the **maximum attainable `|ρ|`** print **beside every quoted `E1ⱼ` / `E2ⱼ`** and are named in
  those two layers' verdict sentences. **`IC_t` is never rescaled by them and the 0.05 MPE is never
  adjusted for them** — rescaling would silently move the MPE;
- `mom20` (B6), the `C_t` entry basis (DP-03(a) / DP-11) for all three endpoints with not-takeable
  counts, the 40-session companion, sessions-to-first-touch distributions, **maximum favourable and
  adverse excursion in ATR** and counter-direction touches at `−d*_t` (reported, never an exit —
  DP-02), the tie-structure reference (per night: touch base rate, non-toucher tied-block size,
  maximum attainable `|ρ|`), and the T+5 / T+20 return ICs.

**Sub-cells — the list is FIXED at lock, was revised once at `record` from Q027's R1 counts, and is now
CLOSED** (DECISIONS item 13 / item 25). A cell suppressed here **stays suppressed even if it clears 20
measured nights** at the decision pass, and a cell cleared here still needs **≥ 20 measured**
contributing nights to print. The cells are `best_timeframe` (short / swing / long — **for E1 and E2
only**, because the timeframe multipliers change exactly what is being ablated; for E3 the slate's
timeframe composition is printed instead); bull-only / bear-only; published versus unpublished rows;
`market_regime_daily.market_regime` (rule 7, §6); and the SPY `tape_t` stratum (§6).

**The list is Q027's, transferred whole** — the two questions share the funnel, the population, the
contributing-night rule and now the window (119 sessions), so Q027's per-cell projections at session 119
*are* this question's counts, and re-measuring the same cells on the same nights would be a second
number for one quantity.

- **SUPPRESSED (8 cells), counts only:** `tape_t` `up_low` (16.8 nights projected), `down_high` (13.4),
  `up_high` (8.4), `down_mid` (6.7), `down_low` (5.0); and the three `market_regime` labels
  **structurally absent** from the measurement — `bearish`, `neutral`, `risk_off` (0 of 48 nights).
- **NOT suppressed:** `tape_t` `up_mid` (30.2); `market_regime` `strongly_bullish` (48.6) and `bullish`
  (23.5); all three `best_timeframe` cells (E1/E2 only); **bull-only and bear-only** (80.4 each on the
  candidate-level population); published versus unpublished.
- **`market_regime` `unlabelled` is not a cell here** — the pre-2026-06-09 backfill cannot occur in a
  window starting 2026-09-15 (rule 7, FREEZE_v001 §7).
- **The draft's expectations are struck** (Correction 13): it read *"bear-only is expected to be
  SUPPRESSED"* and *"the six `tape_t` cells are expected to be SUPPRESSED"*. Those rested on rates from
  the **narrower published** population (PI-010's published-elite counts, H-062's 0.157/session bear
  rate) and **do not transfer** to a candidate-level funnel. The registered rule is a measured count,
  not an expectation.
- **Suppression restricts affirmative reporting only.** It never removes a blocker, never by itself
  makes an endpoint INCONCLUSIVE, and §8's blockers run on **measured** counts for suppressed and
  unsuppressed cells alike. Not on the list, and blocking at whatever count they have: the halves, the
  monthly blocks, the bull-only version, the "mixed graded long" version, the binary-outcome IC, the
  5-session companion, the placebo adjustment, and the added-minus-dropped blocker at its own ≥ 20
  discordant-night floor.

**Quotability:** 20-session basis, W20 research window → **every number in this question is
`NON_QUOTABLE`** (rule 12).

### 4.5 Inference — two CIs per primary (DP-51)

Night-level throughout; control rows and placebo draws never add to n (rule 6).

- **CI 1 — date-clustered:** resample **contributing nights** with replacement, 2,000 resamples,
  recomputing the endpoint's mean. A **stationary block bootstrap** over the ordered nights (expected
  block length **10 sessions**, the Q004 / Q007 / Q009 / Q011 / Q015 / Q023 / Q027 value, fixed at
  lock) is printed beside it.
- **CI 2 — episode-clustered (DP-51):** resample **symbol-episodes** (§2.6) and **nights** jointly —
  draw a bootstrap set of episodes and a bootstrap set of nights, keep the rows in the intersection,
  recompute each retained night's statistic from the surviving rows (a night is retained for E1/E2
  only if ≥ 30 rows survive; for E3 only if `S^prod` and `S^abl` are both non-empty after the draw),
  and average. 2,000 resamples, same seed.
- **DP-51's rule is a decision rule here, not a footnote: a primary that clears MPE with CI 1
  excluding 0 but CI 2 including 0 is INCONCLUSIVE, never CONFIRMED** (§8 clause 4). The threat is
  acute in this question for the same reason as in Q027 — the same ~60 symbols recur nightly with
  almost fully overlapping 20-session windows — and worse for E3, where the discordant picks are often
  the *same borderline names* night after night.
- **p-values (decide, feed BH):** E1ⱼ from B1, E2ⱼ from B2, E3ⱼ from a night-level paired sign-flip
  permutation on `ΔE*_{t,j}`; 10,000 draws each, seed 20260914, all two-sided.
- **Every estimate prints:** contributing nights per endpoint per layer; eligible rows per night
  (min / median / max); distinct symbols and **episodes** with the episode-length distribution;
  contributing nights dated after the lock commit; `d*_t` distribution; slate sizes and overlap;
  reconstruction rates; not-takeable counts; rows excluded by reason; and the `R²_{t,j}` panel.

## 5. Sample floors, expected n, window and schedule

### 5.1 Floors

- **Rule 6 as read by DP-21:** ≥ **80 contributing nights per primary endpoint** and ≥ **20** per
  reported sub-cell. The weaker "80 eligible with ≥ 20 contributing" reading is not used. **No floor
  is ever lowered to reach a date.**
- **DP-24:** ≥ 30 contributing nights dated after the lock commit. **Every** contributing night here is
  post-lock by construction (§6), so DP-24 binds at 30 of the 80 and is not the gate.
  **PROSPECTIVELY_CONFIRMED is reachable from this run by design; DP-31 does not apply and no
  successor replication question is owed.**
- **Binding maturity: 20 sessions**, uniform across every eligible row.
- **No primary is demotable after lock.** Demotion and the EVALUABLE / DEAD / UNEVALUABLE
  determination happen **once, at `record`, from R1b's counts** (§4.3, DP-43); a shortfall afterwards
  is a floor failure — the single DP-13 extension, then DEFERRED — never a demotion and never an
  INCONCLUSIVE verdict.

### 5.2 Exposure basis — R1 is **borrowed from Q027**, not re-routed; measured, and the gate is CLEARED

Q029's E1 and E2 run on **exactly Q027's funnel** (§2.0), so the contributing-night rate that sizes
this question is the one the Steward measured for Q027:
**`research/reports/STEWARD_Q027_exposure.md`, request R1, item (a) — contributing nights per elapsed
session under Q027 §2.5's complete definition.** No second exposure count was requested and none should
ever be run; the two questions share the number, the gate and the arithmetic:

- **the lock-or-DEFER inequality is Q027's** — ≥ **0.36** contributing nights per elapsed session
  (80 nights over the elapsed sessions still admissible under DP-43's 12-month ceiling at a 2026-09-14
  lock, rounded up, re-solved at `record` at the actual lock date and unchanged). Above it, Q029 locks
  and §5.5's dates are recomputed on the measured rate, **moving out only** (DP-43, DP-45). Below it,
  **both** questions would have gone to `research/questions/DEFERRED.md` on the same measurement;
- **measured: 0.6761 contributing nights per elapsed session (48/71) — the gate is CLEARED by 88% and
  both questions lock.** **The drafted planning rate of 0.9538/elapsed session (borrowed from Q023's
  published-pick funnel), its 8-session cushion and every date built on them are struck** (DECISIONS
  Correction 5 / Correction 14). The measured rate is **slower** than the borrowed one, so §5.5's
  window end and both dates moved **out**; a faster rate would have changed nothing and never could.
  **Q027's 0.9577 eligible-night proxy is not used for any date** — it extrapolates past the price
  freeze's own forward-bar horizon and would have pulled the decision in to ~2027-02-22 (DP-45).

**What the borrowed count does not cover, and what R1b adds.** Q027's R1 measures a funnel; it does
not measure whether a *layer* has usable variation, whether the ablation reconstructs the platform's
arithmetic, or whether an ablated slate ever differs from the published one. Those three things fix
`m`, fix the EVALUABLE / DEAD list and decide whether E3 can move at all — and all three must be fixed
**at lock**, from counts, with no outcome in view. They are **R1b**, a feasibility request, explicitly
not a second exposure count (§5.3).

**E3's own rate is bounded, not projected — and as measured it binds at the same session as E1's.** An
E3-contributing night is a Q027-contributing night that also passes Gate 0, has `|S^prod_t| ≥ 1` and has
≥ 10 distinct B4 controls per slate member, so its rate is **at most** the E1 rate. **Every one of those
limbs measures at 100% on the sealed segment** (DECISIONS item 24): Gate 0 passes on **68/68** nights,
the replay disagrees on **0.00%**, `|S^prod_t| ≥ 1` on every night, and the B4 control pool measures
**mean 51.8, median 54, min 39** (`STEWARD_Q023_exposure.md` §6) against the floor of 10. The min-0
**near-miss** nights cost nothing (`k ≤ pool` by construction; a `k = 0` night contributes `ΔE* = 0`).
So **Floor B binds where Floor A binds, at session 119**, and §5.5's window end — always the **later**
of the two floor projections, moving **out** only — does not move beyond Q027's.

### 5.3 Routed request — R1b → data-steward (counts only; was **blocking for `m` and for the lock**) — **CLOSED, delivered 2026-09-14**

**Answered in full at `research/reports/STEWARD_Q029_feasibility.md`** and settled in DECISIONS items
21–27 with Corrections 7–15. Nothing further is asked of the Steward on R1b, and **`m` = 16 is fixed and
closed** (§4.3). What it fixed, each recorded in the section that uses it: the EVALUABLE / DEAD /
UNEVALUABLE register and `m` (§4.3); the REMOVAL / ADDITION assignment and the **measured** GEX addition
weight 12.0 (§2.3); Gate 0's segment reading, 100.00% on 68/68 nights against 84.77% whole-freeze with
its dated mechanism (§2.4); the replay's 0.00% disagreement and the literal-config rule (§2.5); the
near-miss pool and the pool a control floor governs (§2.6, §3 B3); the per-layer `k = 0` share (§4.4);
and the DP-50 commit sweep returning **NONE**, with v1.7 unshipped and unscheduled (§5.5). **The request
text below is kept exactly as issued, before any count existed, so what was asked stays legible.**

Measured on `manifest_v001` (selections) against `exclusions_v003.json`, over pick nights
**2026-04-01..2026-09-10** — the **whole** freeze, because §2.3's addition weight and the enrichment
flags change inside it — plus read-only `git log` / `git show` in the platform repo at `fa70688`.
**No live query** (DP-50(c)). **No outcome of any kind is read**: no touch, no first-touch date, no
return, no excursion, no `outcome_*`, no `sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`,
and no score-versus-outcome cross-tab of any shape. **No price bar is needed for any part of R1b**
except the daily bars already pinned for Q027's R1(c). Required:

(a) **Layer coverage, per layer and per month** — non-null share of each of the seven subscore
columns over all candidate rows, distinct-value count, and the share of nights with non-zero
within-night variance, against §4.3's 70% / 5-value / 50%-of-nights rule. This fixes the EVALUABLE /
DEAD list and therefore `m`.

(b) **The production effective-weight census, per layer and per night** — from
`score_details_json.weighted_dimensions[j].weight`: the share of rows with weight > 0, the distinct
weight values, and **the REMOVAL / ADDITION split of nights** under §2.3's rule, plus the per-night
values of `enable_fundamental_enrichment` and `enable_smart_money_enrichment` from `config_json`.

(c) **The GEX addition weight** — the value of `scoring_weights.gex_alignment` in every distinct
`sas_runs.config_json` in the freeze, with the date range of each, and in particular **the last
config dated before 2026-05-14**. If no such night carries a non-zero value, please say so
explicitly; §2.3 then registers 12.0 with its derivation printed.

(d) **The Gate-0 reconstruction rehearsal** (§2.4) — the share of rows whose `overall_score`
reconstructs from stored `weighted_dimensions` + `config_json` + the stored bonus / penalties / GEX
offset / ATR-elite flag to within 0.05, per night and overall; the `weighted_dimensions` parse-coverage
per night; and the residual distribution. This is a pure arithmetic check on frozen columns.

(e) **The slate-replay check and the slate-change rate** — replay `_qualify_lane` on the bull lane with
each night's own config and report (i) the disagreement rate against the frozen published set
(`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28), listing every night above 1% and every
unreproducible `qualification_reason`; and (ii) **for each of the seven layers, the share of nights on
which the ablated slate differs from the production slate at all, and the distribution of the
discordant count `k_{t,j}`**. This is a function of 16:05 columns only and reads no outcome; it is
what tells the desk, before lock, which E3 endpoints can move.

(f) **The near-miss pool** (B3's draw pool) — per night, the number of bull-lane candidates passing
the threshold and completeness gates but not selected, with the min / median / max.

(g) **The DP-50(a)/(b) commit sweep** since manifest SHA `fa70688` over
`services/super_agent_select_scoring.py`, `services/super_agent_select_models.py`,
`services/super_agent_select_service.py` and `services/sas_conviction_card.py` — the weights, the
timeframe multipliers, the enrichment flags, `qualification_threshold`, `publication_floor`,
`max_output_cap`, `min_completeness`, the ATR-elite caps, the GEX-missingness offset and the lane-plan
writer — each with SHA and date in ET, with an explicit answer **even when it is "none"**, plus a dated
`research/data/DATA_NOTES.md` entry for any repair that rewrote historical rows. **Please state
separately whether any part of the "v1.7" scoring workstream
(`docs/SAS_SCORING_RESEARCH_PLAN.md` §7, Phase 5: *"v1.7 assembled → shadow-parallel nightly (dark)
≥ 4 weeks"*) has shipped or is scheduled to ship inside Q029's window** — a promotion of a new weight
vector is precisely the event §5.5 splits the window on.

**What R1b decides:** `m`, the EVALUABLE / DEAD / ADDITION-vs-REMOVAL list, the GEX addition weight and
the sub-cell suppression list — all fixed at `record` and then closed. **It does not decide the lock
gate; Q027's R1 does** (§5.2). Report to `research/reports/STEWARD_Q029_feasibility.md`.

*(End of the request as issued. It was answered in full on 2026-09-14 and every answer is folded into
the section that uses it — §2.3, §2.4, §2.5, §2.6, §3, §4.3, §4.4 and §5.5 — with the counts named
there. R1b is closed; the request is not re-issued and no part of it is re-run.)*

### 5.4 Routed request — R2 → data-steward (successor freezes; due before the decision date; **not** a blocker for lock, DP-23)

**Q029 and Q027 need the same successor freezes.** Please build **one** pair and pin it for both:
`manifest_v00N` (selections: the same SQL and exclusion criteria as v001, over `sas_candidates` for
**every candidate row, published and unpublished**, plus `sas_runs` and `market_regime_daily`) and
`manifest_prices_v00N` (daily bars for **every candidate symbol on every in-window night**), covering
pick nights **2026-09-15 .. 2027-03-05** with **20 forward sessions** beyond the last included pick
night (daily bars through **2027-04-05**) and **≥ 60 prior sessions** before 2026-09-15, delivered
before **Monday 2027-04-12**; a second pair **only if** the DP-13 extension fires, covering
**.. 2027-04-19** with forward bars through **2027-05-17**, delivered before **Monday 2027-05-24**,
built then and not before. (Every date here moved **out** from the drafted 2027-01-26 / 2027-03-08 with
§5.5's schedule, on Q027's measured rate — DECISIONS Correction 14.) Q027's scope requirements apply
unchanged — every candidate symbol published and unpublished; an **add-only** successor exclusions file
carrying **four** criteria (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs` and
**`payload_disabled_runs`**, adopted with the machinery at §2.0), which may add nights and may never
remove one from a v003 list; missing bars excluded and counted, never back-filled — **plus three that
are Q029's and are not optional**:
**(v)** `sas_candidates.score_details_json` and `sas_candidates.missing_data_json` are in the frozen
column set (without `weighted_dimensions` there is no ablation);
**(vi)** `sas_runs.config_json` is frozen **per night**, not once;
**(vii)** **hourly bars for published symbols are included, per DP-23** (DECISIONS Correction 4). Q029
uses none and no endpoint depends on one — DP-27 stays unreachable and no intra-session ordering is
needed anywhere — but DP-23's clause is unconditional, so this is a build requirement from the standing
policy, added to the shared pair rather than argued with. The general question, *"is DP-23's hourly-bar
clause waivable where no endpoint uses one?"*, is filed for Haci as a proposed standing rule and is not
decided by this question.
Where a successor freeze overlaps an earlier one, the rows are compared and `eval.py` **fails loudly**
on any disagreement in `overall_score`, any layer subscore, `conflict_penalty`, `cross_layer_bonus`,
`dominant_direction` or `weighted_dimensions[*].weight` — a repair that rewrote a weight would
silently re-run the experiment (DP-50(a)). R1b(g)'s commit sweep is **repeated for the period between
the freezes**. Every §5.5 date is re-confirmed session by session from the trading calendar when the
freeze is built; a correction may move a date **out, never in**.

### 5.5 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13; no outcome is looked at)

**Window: pick nights 2026-09-15 .. 2027-03-05 inclusive = 119 elapsed sessions** — **Q027's window,
adopted whole** (§2.0, §5.2), so one freeze, one exposure count, one maturity horizon and one decision
date serve both. **Decision date: Monday 2027-04-12.** Single DP-13 extension to window end
**2027-04-19** (session 149), decided **Monday 2027-05-24**, which is also the **hard stop**: still
short there, Q029 goes to DEFERRED.

**The drafted schedule is struck** (DECISIONS Correction 5 / Correction 14): the 92-session window, the
0.9538 borrowed planning rate, the "floor A met at session 84" line, the 8-session cushion and the
2027-03-08 / 2027-04-19 dates were a drafting projection on a borrowed number. Q027's R1 measured
**0.6761 contributing nights per elapsed session (48/71)**, which is slower, so every date moved **out**
and may only ever move out again (DP-43, DP-45).

| floor | measured rate | sessions needed | window end at session 119 |
|---|---|---|---|
| **A:** ≥ 80 contributing nights, per E1ⱼ / E2ⱼ endpoint (DP-21) | **0.6761**/session (R1(a), measured) | **ceil(80/0.6761) = 119** | **2027-03-05** |
| **B:** ≥ 80 contributing nights, per E3ⱼ endpoint | ≤ A's rate; every additional limb of §2.6's E3 rule measures at **100%** on the segment (Gate 0 68/68; replay 0.00%; `\|S^prod_t\| ≥ 1` on every night; B4 pool min 39 ≥ 10) | **binds at the same session 119** (item 24) | **2027-03-05** |
| **C:** ≥ 30 contributing nights dated after the lock commit (DP-24) | 0.6761/session | 45 = **2026-11-16** | **non-binding**, satisfied by construction |
| **D:** ≥ 20 contributing nights per *reported* sub-cell | Q027's per-cell projections at session 119 | — | the closed suppression list, §4.4 |

**Window end = the later of A and B = session 119.** **Arithmetic** (holidays 2026-11-26, 2026-12-25,
2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31): 2026-09-15 is session 1; session 119 =
**2027-03-05**. Decision date: 2027-03-05 **+ 20 sessions** maturity = **2027-04-05**; **+ one calendar
week** freeze margin = 2027-04-12; first Monday on or after, not a market holiday = **Monday
2027-04-12** — **6.9 months from the lock**, inside DP-43's 12-month ceiling (2027-09-14). `eval.py` is
written once (rule 9) and run **once**, then. **No interim looks.**

- **Extension (DP-13; DP-43's +30 sessions).** If any floor is short at 2027-04-12 on `eval.py`'s
  **own measured counts** (never on a projection or a run-rate), the window extends **once**,
  automatically and with no new question, to window end **2027-04-19** (session 149), decision
  **Monday 2027-05-24** (2027-04-19 + 20 sessions = 2027-05-17; + one week; first Monday on or after).
  The extended run uses the **byte-identical, unmodified `eval.py`** and the same floors. 8.3 months
  from lock, inside the ceiling.
- **DEFERRED fallback (the hard stop).** A floor still short after that single extension sends Q029 to
  `research/questions/DEFERRED.md` with the measured counts rather than running under-powered. **No
  second extension, no reduced floor, and a floor shortfall is never an INCONCLUSIVE verdict** (§8).
- **No primary is demotable after lock**, and no floor is ever lowered to reach a date. The
  EVALUABLE / DEAD / UNEVALUABLE determination and every demotion happened **once, at `record`, from
  R1b's counts** (§4.3, DP-43); a shortfall measured afterwards is a floor failure — the single
  extension, then DEFERRED — never a demotion and never an INCONCLUSIVE verdict.
- **Fixed at lock and not reopened at the decision pass:** all three MPEs (§4.2) and the
  added-minus-dropped blocker's 10.0 pp / 20-discordant-night terms; the REMOVAL / ADDITION direction
  rule, its per-layer assignment and the addition weights including **GEX at 12.0** (§2.3); the
  weight-only ablation scope and the renormalized denominator (§2.4); Gate 0's thresholds, its segment
  scope and the 1% replay gate (§2.4); **`m` = 16 and the closed EVALUABLE / DEAD / UNEVALUABLE
  register** (§4.3); the 0.90 identification threshold (§4.3); the **closed** sub-cell suppression list
  (§4.4); and the conventions of DECISIONS item 19 — **seed 20260914**; **10,000** permutation draws for
  B1, B2 and the E3 sign-flip; **2,000** for B3 and for each bootstrap; the **10-session** expected block
  length; the 0.05 Gate-0 tolerance; the expanding-window `tape_t` tercile cuts and the `market_regime`
  v1.2 timestamp test. Seed, draw counts and library versions print in the results header. **The
  Researcher writes `eval.py` once (rule 9) and runs the 2027-04-12 pass and, if it fires, the
  2027-05-24 extension pass on the byte-identical, unmodified script; the Data Steward owns R1b, R2,
  the pins and the cross-freeze comparison.**
- **If a weights, timeframe-multiplier, enrichment-flag, `qualification_threshold`,
  `publication_floor`, `bear_publish_threshold`, `max_output_cap`, `min_completeness`, ATR-elite-cap or
  GEX-offset change ships mid-window — including any promotion of the v1.7 score** — `overall_score` and
  the weight vector are **two different features** and the window is **cut at the ship date**: the
  post-ship segment becomes the question's window with this whole schedule recomputed from it — **out,
  never in**, subject to the same single extension and the same 12-month ceiling measured from the
  **original** lock — the pre-ship segment becomes a labelled descriptive panel entering no verdict, and
  if neither segment reaches the floors inside the ceiling the question is **DEFERRED** (DP-06's
  pattern, DP-50(a)). **`publication_floor`, `bear_publish_threshold`, `max_output_cap` and
  `min_completeness` are split triggers here although Q027 correctly treats them as non-splits there**
  (DECISIONS item 15): they change *which rows are published*, which is precisely the object `E3ⱼ`
  measures, as well as `d*_t`'s source cohort. **The window is cut whole, not per endpoint** — Q029 has
  one window, one freeze and one decision date shared with Q027, and splitting E3 from E1/E2 would give
  the question two schedules.
- **No split trigger is in view at lock** (DECISIONS item 27, from R1b(g)): the commit sweep since
  `fa70688` over the four named SAS files returns **NONE** (independently re-verified; `git log
  fa70688..HEAD` over those paths is empty); **v1.7 has not shipped and is not scheduled** — the plan
  document is still headed *"Status: PROPOSAL, not a decision record"* and its own Phase 1 prerequisite
  has not shipped; **no repair rewrote a historical row** in R1b's census, so no new `DATA_NOTES.md`
  entry is owed from it, and every config change the sweep found (the v1.5 weight reallocation effective
  2026-05-18, the ATR-elite caps from 2026-05-18, `publication_floor` from 2026-07-08,
  `bear_publish_threshold` from 2026-06-29, the enrichment-flag history) is a **per-night contemporaneous
  fact, not a mutation**, and predates the window by more than two months. The forward constraint is
  unchanged and is stated in §9: any such change is **flag-off until 2027-04-12 (2027-05-24 if the
  extension fires)**, checked before any fix brief is written.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights 2026-09-15 .. 2027-03-05** (119 elapsed sessions;
  .. 2027-04-19 if the single DP-13 extension fires), opening on the first session after the lock commit
  dated 2026-09-14 (09-15 rather than 09-14 so that no night whose 16:05 ET run may precede the lock
  commit can enter).
- **Why the sealed period cannot decide this question, and it is not a close call.** The platform's own
  **August layer audit is a per-layer table of correlations against outcomes on the sealed cohort**,
  committed in the read-only repo at `docs/SAS_SCORING_RESEARCH_PLAN.md:53-67` and read by the
  registrar while drafting: seven rows, one per layer, "corr vs hit" and "corr vs favorable" on n = 635
  decidable published picks, each with a verdict in the table's own last column
  (*"Largest weight, no signal"*, *"Only weighted layer that works"*, *"Mildly anti-predictive"*,
  *"Best magnitude predictor"*, *"Dead — NULL on all 5,868 rows"*, *"negative corr predates zeroing"*).
  That is **H-075's own statistic, already computed on the sealed period**. Add the desk's own reads —
  the 2026-09-10 / 09-12 weeklies' band-level returns and CLAUDE.md's standing "88–90 underperforms
  90+" — and the sealed stretch is contaminated for every endpoint here. The sealed nights are
  therefore **not used for any verdict**: the window is prospective-only (DP-43, the Q018 / Q023 /
  Q027 pattern).
- **Binding consequences of having read that table, stated so they can be checked.** (i) **No
  threshold, cut, MPE, layer list, direction or suppression rule in this PREREG is derived from it**:
  the MPEs are Haci's 0.05 and DP-20's 5.0 pp, the coverage rule is Q028's, the layer list is the
  seven columns the code defines, and the evaluability determination rests on R1b's counts, which are
  coverage facts and not outcome facts. (ii) **Every endpoint is registered two-sided**, so nothing in
  that table can act as a prior. (iii) The audit's own caveat — *"Correlations on the published cohort
  (n=635 decidable) — range-restricted"* (`:66-67`) — is one of the reasons Q029's population is **all
  16:05 candidates** rather than published picks. (iv) The audit is printed **once** in the report as a
  labelled prior-art panel, alongside Q029's measured numbers, and **enters no verdict, no CI
  comparison, no half, no stratum and no q**. (v) The prior-art panel also notes that the **12 April
  replay discordances** R1b(e) found are the pre-2026-07-02 **single-lane counter**, not a replay
  failure, and that they pre-date the 2026-07-02 bear-lane split (DECISIONS Correction 15); the
  in-window 1% replay gate is untouched by them.
- **The sealed post-hoc panel** (`manifest_v001` + `manifest_prices_v001`, pick nights
  **2026-06-01 .. 2026-08-12** — after the DP-06 catalyst split, and 08-12 is the 20-session maturity
  cutoff of the pinned price freeze) prints every §4 endpoint **once**, labelled, entering **no
  verdict**. It is split at **2026-07-06** into **A = 2026-06-01..2026-07-03** and
  **B = 2026-07-07..2026-08-12** and the halves are never blended (`_enforce_ladder_monotonic` shipped
  2026-07-06 and the ladders are what `d*_t` is computed from — DATA_NOTES, Q018 R1; 2026-07-06 is
  itself excluded in `exclusions_v003`). Each sub-panel is SUPPRESSED below 20 contributing nights.
  **The catalyst layer's own DP-06 boundary (2026-06-01, `69ef05f`) is why the panel starts there**: a
  catalyst IC computed across it would be two features averaged.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date (re-derived from the final window at the decision pass); Half B = after. Every
  primary must carry the same sign in both halves (§8 clause 8). The halves are a **stability clause,
  not a reported stratum**, and block at whatever count they have.
- **Monthly blocks (H-075's "stable OOS IC"):** calendar months with ≥ 10 contributing nights; the
  share with the same sign as the full-sample estimate is §8 clause 10, at ≥ 60% rounded up on the
  measured block count.
- **Regime stratification (rule 7).** Both of Q027 §6's stratifiers, adopted verbatim and subject to
  the ≥ 20-night rule: `market_regime_daily.market_regime` (**v1.2 only**, the row with
  `trading_date = t`, legal only where `created_at` falls on that trading date and at or before that
  night's own `sas_runs.finished_at` — the Q023 §2.2 timestamp test; a night with no legal label keeps
  its place in the primary and is reported in an `unlabelled` cell, since the label is a **stratifier,
  never a filter and never an arm**); and **`tape_t`**, the SPY proxy (sign of the trailing 20-session
  return × tercile of trailing 20-session realized volatility, from bars ≤ t, **expanding-window**
  tercile cut points). The window starts long after the 2026-06-09 point-in-time boundary
  (FREEZE_v001 §7), so the backfill hazard cannot reach it.
- **Knowledge time (rule 14) — every input declared. Q029 needs no rule-14 exception and requests
  none** (DP-05 untouched, DP-41 respected).

  | input | source | available | use |
  |---|---|---|---|
  | seven layer subscores, `overall_score`, `completeness_score`, `cross_layer_bonus`, `conflict_penalty`, `missing_data_penalty`, `dominant_direction`, `best_timeframe`, `qualified`, `selected_rank`, `qualification_reason`, `threshold_pass` | `sas_candidates` (all rows) | pick night, 16:05 ET | ranking variables, replay inputs, eligibility, strata |
  | `score_details_json.weighted_dimensions[*]`, `missing_data_json`, `source_membership_json` | `sas_candidates` | written with the candidate at 16:05 ET (`super_agent_select_service.py:306-336`) | the ablation arithmetic (§2.4) |
  | `config_json` (weights, multipliers, flags, thresholds, caps) | `sas_runs`, per night | written by the night's own run | the replay's gates (§2.5) |
  | `public_payload_json.lane_plans.swing_trading.targets[0]` (published rows) | `sas_candidates` | written during the run before `finished_at` (`services/super_agent_select_service.py:155-161`) | `d*_t` only |
  | `C_t`, ATR14, `beta60`, `runup20`, `mom20`, `adv20`, SPY tape | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | distances, matching, `tape_t` |
  | `market_regime` (v1.2, `trading_date = t`) | `market_regime_daily` | lag 0, verified FREEZE_v001 §7 for nights ≥ 2026-06-09, enforced per night by the timestamp test | rule-7 stratum only |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion |
  | session t+1 open; daily bars t+1..t+20 | `prices_daily_split` | after the pick night | **entry and outcome measurement only** |

  **What `eval.py` must enforce:** every ablated score, every replayed slate, every tercile, band,
  episode id and stratum label is computed and written to a frozen per-row and per-night table
  **before any post-pick-night bar other than the t+1 open is loaded**, and the t+1 open is used
  **only** as the entry price. The run fails if any t+1-or-later field is referenced in eligibility,
  scoring, selection, layer evaluability or stratification.

## 7. Multiple testing

- **Within the question: BH across `m` = 16** — the EVALUABLE layer-endpoint pairs fixed at `record`
  from R1b and **never revised** (§4.3): three endpoints (E1ⱼ, E2ⱼ, E3ⱼ) each for `flow_strength`,
  `technical_structure`, `gex_alignment`, `fundamental_quality` and `catalyst_event`, plus
  **E3_projection**. The drafted "expected 12–15, bounded above by 21" is **replaced by the measured
  16**, which is the **stricter** denominator for every endpoint here. `m` is **fixed in every
  branch**: an endpoint short of floor still has its p computed and stays in `m`, a DEAD or UNEVALUABLE
  pair was never in it, and **no pair is dropped afterwards** — dropping one would lower the bar for the
  survivors. Threshold **q ≤ 0.10** alongside raw p (rule 8).
- **Across the family: F1 Selection edge.** F1's correction set at this lock is **Q006 (2) +
  Q024 (6) + Q025 (2, which never shrinks despite Q025's deferral) + Q029 (16) = 26**, computed
  at the decision pass over the F1 questions locked by then and **never falling below 26**. If another
  F1 question locks before 2027-04-12 its primaries join the set and the q's are recomputed on the
  larger denominator. **This is the reason H-003, H-020 and H-075 are one question and not three:**
  three PREREGs asking the same thing of the same seven columns would have produced three separate
  corrections over overlapping endpoints, and rule 8 would have been satisfied on paper only.
- **Required companion correction across F2**, on **E1ⱼ and E2ⱼ only.** The two rank-correlation
  endpoints are computed on Q027's population, distance and clock, and Q027's primaries sit in F2; a
  layer IC and the composite IC are not independent tests. So E1ⱼ and E2ⱼ must clear **q ≤ 0.10 in F1
  and in F2**, where F2's set at that pass is **Q023 (2) + Q027 (2) + these `2L` = 10 endpoints, i.e.
  14 in all**, with **L = 5** — the IC-evaluable layers (`projection` contributes no IC endpoint and
  `smart_money_confirmation` none) — and **the larger of the two q's is the one quoted and the one that
  decides** (the Q015 / Q020 companion-correction pattern). E3ⱼ is corrected in F1 only.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q027 (F2)** owns the **composite** `overall_score` IC. Q029 recomputes it nowhere. A confirmed
    layer IC here does **not** confirm Q027's E1 and a null there does not refute one here — a
    composite can order outcomes while no single ingredient does, and one ingredient can order them
    while the blend does not. The two verdicts are compared only by the **Reporter**, from ledgered
    verdicts, after both are closed.
  - **Q028 (F8)** owns H-076's **structure** limb (correlation, factor count, conditional redundancy)
    and reads no outcome at all. Q029 owns the **contribution** limb (E2ⱼ). **Neither alone answers
    H6** — Q028 §8 says so in its own verdict sentence, and §8 here repeats it. The joint H6 answer is
    assembled by the Reporter from the two ledgered verdicts (the H-077 pattern). Q029 does **not**
    read Q028's register to choose which partial ICs to report (§4.3).
  - **Q006 (F1)** contrasts published picks against distance-matched unpublished controls. Q029's
    `E_t` is Q006's `E_t`, so a confirmed E3ⱼ is **not** a second confirmation of a selection edge:
    E3 is a *difference between two slates*, and it can be large while `E_t` itself is zero, or zero
    while `E_t` is large. §9's rules are written accordingly.
  - **Q024 (F1)** benchmarks the published slate against SPY, equal-weight, sector-matched random and
    momentum ranks, with a money gate. Q029's B6 `mom20` comparator is a descriptive rank correlation
    over candidates and **confirms nothing about Q024**, in either direction.
  - **Q005 (F2)** decomposes the score distribution and reads no outcome column, so it cannot
    contaminate this question; it is where §10 threat 6's score-compression facts come from.
  - **H-012 (F2, open)** owns the conflict penalty. Q029's modifier ablations are descriptive and
    license nothing about it (§4.4, §9).
  - **H-080 (F2, unregistered)** owns threshold stability; **H-082 (F2)** owns edge decay and names
    "H-075's per-layer ICs" as one of its series. A layer IC confirmed here is an input to H-082's
    series, never an answer to it.

## 8. Decision rule (numeric, written before unsealing)

`E1ⱼ` and `E2ⱼ` are in **Spearman-ρ units** (marginal and partial per-night rank correlation of layer
`j` with the path-outcome rank `u_i` over 20 sessions from the t+1 open). `E3ⱼ` is in **percentage
points of the slate's within-night control-adjusted L3-touch rate**, **ablated minus production**,
placebo-adjusted (§3 B3). All over §2.6's contributing nights. All **two-sided**.

**MPEs — `|E1ⱼ| ≥ 0.05`, `|E2ⱼ| ≥ 0.05`** (Haci's number, Master Hypothesis Program H3; §4.2 states
the source and both questions' DECISIONS files propose the unit as a standing entry) —
**`|E3ⱼ| > 5.0 pp`** (DP-20; §4.2 gives the reason the doubling clause is not applied and keeps its
strict half as clause 11's blocker). **No MPE is lowered at the decision pass in any
branch**, including one where it turns a CI-excludes-zero result into INCONCLUSIVE (rule 6).

**Per endpoint, HISTORICALLY_CONFIRMED requires all of:**

1. **contributing nights ≥ 80** and **≥ 30 dated after the lock commit** (DP-21, DP-24), with ≥ 20 for
   any sub-cell that is *reported*. A sub-cell below 20 is **SUPPRESSED** (counts only), does not by
   itself make the endpoint INCONCLUSIVE, and its suppression never removes clauses 5–11's blockers;
2. the **mechanical gates**: ≥ 30 eligible rows on every contributing night for E1ⱼ / E2ⱼ; Gate 0's
   ≥ 99% per-night reconstruction and ≥ 95% `weighted_dimensions` parse for E3ⱼ, with the **in-window**
   reconstruction ≥ 95% and the 1% replay gate (§2.4 — the gates run on the window's own nights; the
   sealed freeze's 84.77% whole-freeze figure is a pre-v1.5 artefact and decides nothing); for E2ⱼ,
   `R²_{t,j} ≤ 0.90` (§4.3 — above it the endpoint is UNIDENTIFIED and carries no verdict);
3. `|E| > MPE`;
4. the **date-clustered bootstrap 95% CI excludes 0** **and** the **episode-clustered 95% CI excludes
   0** (DP-51, §4.5). Clearing MPE on the first and not the second is **INCONCLUSIVE, never
   CONFIRMED**;
5. **for E3ⱼ only:** the **placebo-adjusted** value (§3 B3) is the one measured in clauses 3 and 4, and
   the **raw** value must agree in sign;
6. the **blocking companion** is not beyond MPE in the opposite sign: the **binary-outcome** IC for
   E1ⱼ / E2ⱼ; the **touch-within-5-sessions** version for E3ⱼ (DP-20 units — a sessions-to-touch
   difference has no MPE under DP-44 and cannot serve as a blocker);
7. the **"mixed graded long"** version of the endpoint is not beyond MPE in the opposite sign;
8. the **bull-only** version (E1ⱼ / E2ⱼ; E3 is bull-lane by construction) is not beyond MPE in the
   opposite sign, and the point estimate has the **same sign in both halves** (§6) with neither half
   beyond MPE in the opposite sign;
9. **the layer's own arithmetic is not degenerate:** for E3ⱼ, the share of contributing nights with
   `k_{t,j} = 0` is printed and, where it exceeds **50%**, the verdict sentence must lead with it —
   a confirmed E3 driven by a minority of nights is a real but narrow finding and is reported as one;
10. the **monthly-block stability clause** (§6): the share of qualifying monthly blocks carrying the
    same sign as the full-sample estimate is **≥ 60%** (rounded up on the measured block count) —
    H-075's *"stable OOS"*, registered as a blocking clause rather than a reported statistic;
11. **for E3ⱼ only, the added-minus-dropped blocker** (§4.2, §4.4; DECISIONS item 1 / Correction 6): on
    a layer with **≥ 20 discordant contributing nights**, the undiluted control-adjusted contrast of the
    picks the ablation *adds* against those it *drops* must carry the **same sign as `E3ⱼ`**, and a
    contrast beyond **10.0 pp in the opposite sign blocks a CONFIRMED**. Below 20 discordant nights it
    prints counts only and blocks nothing, and clause 9 carries the narrowness there;
12. **BH `q ≤ 0.10`** within the question (over **`m` = 16**) **and** within F1 (26) — and, for
    E1ⱼ / E2ⱼ, **also within F2** (14), with the larger q quoted and deciding (§7).

- **NULL (per endpoint):** floors and clause 2 met, **both** CIs include 0, **and** `|E| < MPE`.
  A mechanical `E3ⱼ ≡ 0` — the ablated slate never differs from the production slate on any
  contributing night — is a **NULL with its own sentence**: *"removing this layer's weight changes the
  published slate on 0 of N nights"*. That is a result, and it is H-003's own mechanism answered in the
  cleanest possible way.
- **INCONCLUSIVE (per endpoint):** anything else — CI 1 excluding 0 while CI 2 does not (clause 4),
  halves disagreeing in sign, a blocking companion beyond MPE the other way, **an added-minus-dropped
  decomposition beyond 10.0 pp in the sign opposite `E3ⱼ` on a layer with ≥ 20 discordant nights
  (clause 11)**, fewer than 60% of monthly blocks agreeing, `0 < |E| ≤ MPE` with a CI excluding 0
  ("real but below MPE", rule 6), a CI including 0 with `|E| ≥ MPE`, or (E2ⱼ) UNIDENTIFIED. **A floor
  shortfall is never INCONCLUSIVE** — it fires the single DP-13 extension, then DEFERRED (§5.5).

**Binding on every verdict sentence, fixed at lock:**

- **E2ⱼ** is described as *"partial on the four other **retained** layers — flow, technical, gex,
  fundamental, catalyst minus `j` — with `projection` excluded for coverage"* (§4.1, Correction 10). A
  partial IC quoted without that list reads as controlling for the whole engine, and it does not.
- **E3ⱼ** says *"the published **bull** slate"*, never *"the slate"* (§2.5, item 18).
- **`gex_alignment` and `catalyst_event`** name the tie structure — the per-night touch base rate, the
  tied-block size and the **maximum attainable `|ρ|`** — in the sentence that quotes their `E1ⱼ` /
  `E2ⱼ` (§4.4, Correction 11); no ρ is ever rescaled and the MPE is never adjusted.
- **Where clause 9's `k = 0` share exceeds 50%**, the E3 verdict sentence **leads** with it.

**Per layer — the label that goes in the register.** Fixed here; one row per layer, printed whatever it
says. **`projection` prints `E1 UNEVALUABLE` / `E2 UNEVALUABLE` with its measured 62.74% coverage and
carries only its E3 row; `smart_money_confirmation` prints DEAD in all three** (§4.3):

| label | condition |
|---|---|
| **CARRIES** | `E2ⱼ` CONFIRMED beyond MPE **and** `E3ⱼ` CONFIRMED in the consistent sign (REMOVAL layer: `E3ⱼ < −5.0 pp`; ADDITION layer: `E3ⱼ > +5.0 pp`) |
| **HARMFUL** | `E3ⱼ` CONFIRMED in the inconsistent sign (REMOVAL layer: `E3ⱼ > +5.0 pp` — deleting it improves the slate; ADDITION layer: `E3ⱼ < −5.0 pp`) |
| **MARGINAL_ONLY** | `E1ⱼ` CONFIRMED, `E2ⱼ` NULL — the layer predicts, but everything it knows is already in the others |
| **DECORATIVE** | `E1ⱼ`, `E2ⱼ` and `E3ⱼ` all NULL with floors met |
| **DEAD** | declared at `record` from R1b: the layer is not computed (or not weighted) in production; counts only, no verdict, not in `m` — **`smart_money_confirmation`** |
| **UNDECIDED** | anything else, including any endpoint INCONCLUSIVE or UNIDENTIFIED |

**For a layer whose only evaluable endpoint is E3 (`projection`, §4.3), the labels read on E3 alone:**
CARRIES iff `E3ⱼ` is CONFIRMED in the consistent sign, HARMFUL iff CONFIRMED in the inconsistent sign,
DECORATIVE iff `E3ⱼ` is NULL with its floor met, UNDECIDED otherwise; MARGINAL_ONLY is unreachable for
it and its two IC cells print **UNEVALUABLE (62.74% coverage)**, never a verdict. The layer's row still
prints in every branch.

**Question level.** **CONFIRMED** iff **at least one layer** is **CARRIES** or **HARMFUL** — H-075's
PASS as written (*"a layer has stable OOS IC and/or its removal materially hurts the slate"*).
**NULL** iff **every evaluable layer is DECORATIVE** — H-075's FAIL as written (*"a layer adds no
incremental OOS value → remove or demote it"*), and it is the more consequential branch (§9).
**INCONCLUSIVE** otherwise. The register prints all seven rows in every branch, DEAD and UNDECIDED
included; no layer may be omitted, and no subset chosen afterwards (the Q005 / Q028 anti-cherry-pick
rule).

**What a confirmed layer does and does not mean (binding on the report).** A CARRIES layer means
*"within a night, this ingredient orders candidates toward a target at the same ATR distance, over and
above what the other ingredients say, and its weight measurably changes which names get published"*.
It does **not** mean the picks made money, it does **not** mean the published slate beats anything
(Q006, Q024), it does **not** license quoting any layer as a probability, and — because Q028 owns the
structure limb — it does **not** by itself justify any change to the architecture (§7).

**PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5.1) — it requires ≥ 30 contributing
nights dated after this file's lock commit (DP-24, DP-21), which every contributing night here is,
frozen in the successor manifests and never inspected earlier, reproducing the sign under the
unmodified `eval.py`. The clause does not weaken. No subscriber-facing statement before that (rule 10);
even then the basis is `NON_QUOTABLE` until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform blends seven named layers into one 0–100 number at fixed weights (projection 29 /
technical 27 / flow 24 / catalyst 10 / fundamental 5 / smart-money 5 / GEX 0 —
`services/super_agent_select_models.py:8-22`), describes itself as a seven-layer score, and **two of
the seven are switched off by default flags while a third carries zero weight** (`:110-111`, `:17`).
**Nothing on the platform measures whether any individual layer earns its weight**, and this question
is that measurement. Rules below fire **only** where §8 licenses them, and nothing subscriber-facing
ships before PROSPECTIVELY_CONFIRMED (rule 10):

- **A DECORATIVE layer:** a brief proposing `scoring_weights[j] = 0` with the freed weight
  **explicitly not redistributed by hand** (a redistribution is a new weight vector and needs its own
  question), shipped **flag-off with a byte-identical checksum on the old path** and shadowed ≥ 20
  trading days before any flip (rule 11); and a **PI against the product description** — "seven-layer
  score" overstates what is measured, with the counted version attached. PI-008 is the existing entry
  of exactly this shape for smart-money and the new PI cites it.
- **A HARMFUL layer** (removing it improves the slate): the same brief at priority, plus a
  `PLATFORM_ISSUES.md` entry under DP-07, and the layer's contribution is suspended on the internal
  surface immediately. A sign inversion at layer level is a scoring defect as much as a research
  finding, and the two halves are routed separately.
- **An ADDITION layer confirmed positive** (GEX, smart-money or fundamental improves the slate at its
  nominal weight): an **ENHANCEMENTS** entry proposing the weight and, where the layer is gated by an
  enrichment flag, the cost of turning that flag on — filed with a recommendation, the decision Haci's
  (DP-48), gated on PROSPECTIVELY_CONFIRMED, and shipped by rule 11's inert-then-dark-then-flip
  sequence. **H-020's own claim** — GEX carries day-lane information at weight 0 — is answered here by
  E1_gex / E2_gex / E3_gex and nowhere else.
- **A CARRIES layer:** no product change. It is the sentence the score's description may rest on, and
  it becomes an input to **H-083** (setup-specific architecture) and **H-082** (decay), both of which
  own their own PREREGs.
- **Every layer DECORATIVE (the question-level NULL):** this is H-075's FAIL branch and it is a result,
  not a non-result — *"no single ingredient adds incremental value at its current weight"*. It routes
  to **EN-018** (categorical setups) and to **H-083** as the successor architecture question, and it
  means the weight vector is not where the improvement is. **It does not license "the score is
  useless"** — that is Q027's question, not this one.
- **The modifier ablations and the agent-level cut license nothing on their own** (§4.4). A striking
  conflict-penalty split is a reason to register H-012 as its own primary question.
- **The suppressed cells license nothing**, whatever they show.
- **The register is offered to the platform's own weight workstream.** `docs/SAS_SCORING_RESEARCH_PLAN.md`
  plans a walk-forward weight search and a v1.7 promotion on an **in-sample** layer audit (§2.1 of that
  document, on the sealed cohort). An **EN** is filed under DP-48 proposing that the promotion criteria
  consume Q029's prospective register instead — and, either way, **DP-50(b) binds: any change to the
  weights, the timeframe multipliers, the enrichment flags, `qualification_threshold`,
  `publication_floor`, `max_output_cap`, `min_completeness`, the ATR-elite caps or the GEX-missingness
  offset — including a v1.7 promotion — is flag-off until Q029's decision date, 2027-04-12
  (2027-05-24 if the single DP-13 extension fires)**, the PI-011 / Q010 pattern, checked before any fix
  brief is written. `publication_floor`, `bear_publish_threshold`, `max_output_cap` and
  `min_completeness` are inside that list here, because they change which rows are published — the very
  object `E3ⱼ` measures (§5.5, DECISIONS item 15). As of the lock the sweep is clean: **no such change
  has shipped since `fa70688` and v1.7 is unshipped and unscheduled** (item 27). If such a change ships anyway it takes a dated `DATA_NOTES.md` entry naming the
  column, the date range and the ship SHA, and §5.5's window split applies (DP-06, DP-50(a)). **Q027 is
  in flight on the same clause and the same dates (2027-04-12 / 2027-05-24)**, so the constraint is one
  constraint, not two.
- **DP-49 binds every brief this question produces:** each check handed to the **coding agent** must be
  satisfiable from the platform repo alone — the test suite, a pure-function import, `git show --stat`,
  a file diff. A weight change is ideal for this: the proof of inertness is a unit test on
  `_effective_dimension_weights` and a byte-identical checksum on the old path, with **no database step
  anywhere**. Anything that reads or writes a table belongs in the brief's verification section,
  addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where a write is required; where a
  frozen manifest covers the affected table, the brief names that parquet as the before-snapshot
  (DP-50(c)).
- Owner: implementer. Shadow period before any flip: ≥ 20 trading days.

## 10. Known threats to validity (registrar's own list)

1. **The hypothesis has already been tested on the sealed period, by the platform.**
   `docs/SAS_SCORING_RESEARCH_PLAN.md:53-67` is a per-layer outcome-correlation table with verdicts,
   and the registrar read it while drafting. §6 states the four binding consequences; the mitigation is
   a prospective-only window, two-sided registration, and a design whose every threshold comes from
   Haci's H3, DP-20, Q028's coverage rule or the code. It cannot be mitigated further, and a reader who
   wants to check the blindness should check §6's list against §4's numbers.
2. **The ablation renormalizes.** `base_score = weighted_sum / available_weight` (`:1348`), so removing
   a layer does not merely delete information — it **up-weights the survivors**. That is exactly what
   setting the weight to 0 would do in production, so it is the right counterfactual for a brief; but
   `E3ⱼ` therefore measures "lose `j` and re-weight the rest", not "lose `j`". The fixed-denominator
   sensitivity (§4.4) separates the two and is printed with every E3.
3. **Leave-one-out understates a shared factor.** If two layers carry the same signal, removing either
   alone changes little and both look decorative. Q028 measures that redundancy (its `S3`); Q029
   answers it inside its own window with the partial IC and the 0.90 identification clause, and
   **leave-two-out is out of scope and is a successor question**, named here so it cannot be added at
   the decision pass.
4. **Slate overlap dilutes E3 toward zero.** With a cap of 8 and a small nightly candidate pool, most
   ablations will move one or two names. The registered answers are the overlap panel, the
   added-minus-dropped decomposition, R1b(e)'s pre-lock measurement of the slate-change rate per layer,
   and §8 clause 9's requirement that a high `k = 0` share lead the verdict sentence. A structurally
   immovable E3 is reported as a mechanical NULL, not as a failed measurement.
5. **The two flag-gated layers may be untestable rather than worthless.** `enable_fundamental_enrichment`
   and `enable_smart_money_enrichment` default `False` (`:110-111`), so their contexts may never be
   built and their subscores may be null throughout — in which case adding weight changes nothing by
   construction (`:1341`) and the honest label is **DEAD, not DECORATIVE**. R1b(a)(b) decided which,
   from coverage counts, before the lock, and it split them: **`smart_money_confirmation` is DEAD**
   (0.00% non-null, flag False on all 102 nights) while **`fundamental_quality` is a live REMOVAL
   layer** (flag True on 67 of 68 segment nights, 98.71% non-null) — the draft expected both to be
   dead or addition-only. The platform's own audit calls smart-money *"Dead — NULL on all 5,868 rows"*,
   which is a coverage fact; the desk measured it rather than inheriting it, and got the same answer.
   **The third surprise runs the other way:** `projection`, the largest-weighted layer, fails the
   coverage floor for its two IC endpoints (62.74%), so the engine's biggest ingredient is neither
   IC-testable nor available as a control for anyone else's partial IC (§4.1).
6. **Score resolution and ties cap every IC.** Most candidates will not touch, so `u_i` carries one
   large tied block and `|IC|` is bounded well below 1; and the ATR-elite block pins scores at 84.9 /
   79.9 (`:1401-1423`) while the +5 GEX-missingness offset fires on a share of rows (`:1379-1399`).
   An MPE of 0.05 is a bar on a compressed scale. The mitigation is disclosure, not adjustment: the
   touch base rate, the tied-block size and the **maximum attainable `|ρ|`** print beside every ρ, and
   no IC is ever rescaled by them (rescaling would silently move the MPE). Q027 §10 threats 1–2 apply
   here verbatim and are inherited, not re-derived.
7. **Overlapping 20-session windows and recurring symbols.** DP-51's episode-clustered CI is the answer
   and it is a **decision** clause (§8 clause 4). It bites hardest on E3, whose discordant picks are
   often the same borderline names on consecutive nights.
8. **A replay that is not the platform's selection.** If `_qualify_lane`'s inputs are not fully frozen —
   a `timeframe_thresholds` override, a dark-bear symbol list, a mid-run config change — the production
   slate will not reproduce. §2.5's 1% loud-failure gate and R1b(e) tested this **before** the lock, on
   the sealed freeze, where it cost nothing to discover: **0.00% disagreement on 68 of 68 segment
   nights**, with the 12 April discordances explained as the pre-2026-07-02 single-lane counter and the
   absent-config-key trap registered rather than left to the dataclass (§2.5, Correction 15).
9. **A score, or a weight, that has been rewritten.** `sas_candidates` rows are not immutable (the
   in-sample catalyst rescore, the E9a batch). Gate 0 re-derives every score from stored components,
   and §5.4's cross-freeze comparison fails loudly on any disagreement in `overall_score`, a subscore
   or a stored weight.
10. **Config drift inside the window, and a live weight workstream.** A v1.7 promotion or any weight /
    multiplier / flag change makes `overall_score` and the ablation two different experiments
    mid-flight. R1b(g) sweeps to the lock, R2 sweeps between freezes, §5.5 splits the window at any
    such ship, and §9 states the DP-50(b) flag-off constraint that is supposed to prevent it.
11. **One database (DP-50).** A repair between freezes can rewrite the very weights this question
    ablates. Rule 4's pinned manifests are what stands between that and a locked question, and §5.4's
    loud comparison is what detects it.
12. **`m` is large and the family is larger.** **Sixteen** primaries inside one question — more than the
    12–15 the draft expected — on top of F1's existing ten and F2's four, is a demanding correction:
    F1 = 26, the F2 companion set = 14, and the larger q decides for the ICs. By design. The alternative, three
    PREREGs over the same seven columns, would have been worse (§7). The cost is real and is stated:
    a genuine but modest layer effect may not survive BH at this denominator, and that outcome is
    INCONCLUSIVE, reported as such, not re-cut on a smaller family.
13. **A question-level NULL will be argued with.** "No ingredient earns its weight" is a statement
    about the product's architecture, and the temptation at the decision pass will be to find the
    sub-cell, the timeframe or the month where one does. The suppression list is fixed at lock, `m` is
    fixed at `record`, the halves and monthly blocks are blockers rather than reported strata, and
    every one of the seven rows prints whatever it says. **`m`, the suppression list, the register and
    the schedule are all closed as of this lock** (§4.3, §4.4, §5.5), so the only thing the decision
    pass produces is numbers.

---

## Decisions before lock

Recorded in DECISIONS.md (2026-09-14, `decide` + `record` passes). **Routed items still open: none** —
R1 was never re-routed (Q027's, borrowed, §5.2), **R1b is CLOSED** (delivered 2026-09-14; it fixed
`m` = 16), and R2 (the shared successor freezes) is due before the decision pass and is not a blocker
(DP-23). Twenty-seven items and fifteen corrections are applied above; **nothing is pending**.

| # | Decision | Bucket | What is registered |
|---|---|---|---|
| 1 | E3's MPE | DECIDED | ±5.0 pp (DP-20), doubling clause declined with its reason; its strict half kept as the **added-minus-dropped blocker** at 10.0 pp / ≥ 20 discordant nights — §4.2, §4.4, §8 clause 11 |
| 2 | The GEX addition weight | DECIDED | the **measured** value from the last pre-2026-05-14 config (2026-05-08) — §2.3 |
| 3 | Ablation scope | DECIDED | **weight-only**; "layer removed everywhere" a printed sensitivity — §2.4, §4.4 |
| 4 | The partial IC's status | DECIDED | **`E2ⱼ` is a primary**; three endpoints per evaluable layer — §4.2, §7 |
| 5 | E3's denominator convention | DECIDED | **renormalized** (the platform's own arithmetic); fixed-denominator a printed sensitivity — §2.4, §4.4 |
| 6 | Evaluability, and how `m` is fixed | DECIDED | declared once at `record` from counts, then **closed**; four clauses incl. `UNREGISTERED_LIVE` — §4.3 |
| 7 | E3's night set | DECIDED | **every** E3-contributing night, `ΔE = 0` included — §2.6, §4.1, §8 clause 9 |
| 8 | The two modifiers | DECIDED | ablated, **descriptive only**; H-012 keeps the conflict penalty — §4.4, §9 |
| 9 | The window start | **DEFAULTED** | prospective-only, pick nights ≥ 2026-09-15; not taken: read the sealed nights (DP-43) — §6 |
| 10 | Exposure basis, gate, window end, decision date | **DEFAULTED (R-3)** | **LOCK** on Q027's measured 0.6761 ≥ 0.36; window .. 2027-03-05 (119 sessions), decision 2027-04-12, single extension decided 2027-05-24 = hard stop; not taken: the 0.9577 proxy — §5.2, §5.5 |
| 11 | `m`, the register, the GEX weight, the suppression list | ROUTED → **CLOSED** | R1b delivered 2026-09-14; settled in items 21–26 — §2.3, §4.3, §4.4 |
| 12 | Successor freezes | ROUTED → open, **not a blocker** | R2, dates fixed at `record` and moved out — §5.4 |
| 13 | Demotion, and the sub-cell suppression list | DECIDED | **no primary demotable after lock**; the cell list fixed, revised once, now **closed** — §4.4, §5.5 |
| 14 | Exclusions inside a post-freeze window | DECIDED | v003 ∪ the add-only successor file, **four** criteria, criteria fixed at lock — header, §5.4 |
| 15 | A mid-window config or publication-gate change | DECIDED | the window is **cut whole** at the ship date, out and never in; the trigger list is wider than Q027's — §5.5, §9 |
| 16 | The REMOVAL / ADDITION split's scope and floors | DECIDED | governs `E3ⱼ` only; a side below 80 is **UNEVALUABLE at `record`**, not in `m` — §2.3, §4.3 |
| 17 | If Gate 0 or the replay had failed | DECIDED | the IC-only branch is registered and **recorded as not taken, with the measured rates named** — §2.4 |
| 18 | The lane for the slate replay | DECIDED | **bull lane only**; every E3 sentence says "the published **bull** slate" — §2.5, §8 |
| 19 | Who writes and runs `eval.py`, and the fixed conventions | DECIDED | Researcher writes once, runs 2027-04-12 (and the extension) unmodified; seed 20260914, 10,000 / 2,000 draws, 10-session blocks — §5.5 |
| 20 | The BH sets | DECIDED | within-question `m`, F1, and the **required** F2 companion on E1ⱼ/E2ⱼ with the larger q deciding — §7 |
| 21 | Gate 0's scope; does the E3 limb exist | DECIDED | **the segment reading**; 100.00% on 68/68 in-window-vintage nights, 84.77% whole-freeze printed with its mechanism; **no PI** — §2.4 |
| 22 | `m`, and the closed register | DECIDED | **`m` = 16**; `projection` E3-only, `smart_money` DEAD ×3, retained set of five — §4.3 |
| 23 | The REMOVAL / ADDITION assignment; the GEX weight | DECIDED | no split survives; `fundamental_quality` is REMOVAL; **GEX = 12.0**, fallback branch struck — §2.3 |
| 24 | E3's rate, the near-miss pool, which floor Correction 2 governs | DECIDED | Floor B binds at session 119; the ≥ 10 floor is **B4's control pool, not B3's**; `DEGENERATE_PLACEBO` flag — §2.6, §3 B3, §5.2 |
| 25 | The suppression list, closed | DECIDED | Q027's measured list transferred whole: **8 cells suppressed**, the draft's expectations struck — §4.4 |
| 26 | The BH sets, with `m` final | DECIDED | **within 16 · F1 26 · F2 companion 14 (L = 5)** — §7, §8 clause 12 |
| 27 | DP-50's sweep and the v1.7 trigger | DECIDED | sweep **NONE**; v1.7 unshipped and unscheduled; flag-off to 2027-04-12 / 2027-05-24 — §5.5, §9 |

**Two items were DEFAULTED on Haci's behalf** (#9 and #10, both under DP-43, which adds no DP entry).
Overturning either is a successor question, not an edit to this file. Every other item met a DECIDE
ground; **no floor, arm, MPE, gate, denominator or clause was weakened anywhere** — `m` rose from an
expected 12–15 to 16, which raises the BH bar; the control-pool floor moved from 3 to 10; every date
moved **out**; and the suppression list came from measurement rather than from the draft's
expectations. Five standing-rule proposals are listed in DECISIONS.md for Haci to confirm or drop; none
of them is assumed here.
