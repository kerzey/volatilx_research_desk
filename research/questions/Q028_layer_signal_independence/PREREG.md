# Q028 — layer_signal_independence: are the seven scoring layers seven signals, or three or four?

**Status:** PREREG_DRAFT (lock by committing this file; `--by desk`, DP-46). **All decisions are
settled** — nine items (five drafted, four raised at decide), no routed request, nothing pending;
recorded in `DECISIONS.md` (decision-maker, 2026-09-14) and applied to this file the same day by
`@registrar apply Q028`. The former §11 is now "Decisions before lock" at the end.
**Family:** **F8 System validity** (Haci's Master Hypothesis Program, H6 → BACKLOG **H-076**, the
**structure half**). The contribution half — each layer's incremental predictive information given the
others (partial IC) — is **H-075's and is not tested here**; §8 states what follows from that split.
**Type:** **DIAGNOSTIC / structure. PASS / FAIL, no primary endpoint, no MPE, no BH.** This question
tests no edge, measures no price path and reads **no outcome column**. It produces a **layer-structure
register**: the correlation and factor structure of the score's own inputs, with thresholds fixed
before the run. **Every number it produces is `NON_QUOTABLE`** (rule 12) and none is ever a subscriber
claim.
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; frozen_at
2026-09-10T22:31:32Z; platform SHA fa70688bc252d14f8d67e371afafc194731c324e).
**Manifest (prices):** **none — not used.** No price bar, raw or split-adjusted, is read anywhere in
this question.
**Exclusions:** research/data/exclusions_v003.json (newest, DP-22) — `manual_runs.trading_dates` ∪
`non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, derived in
`eval.py` from the file, never hard-coded (§2.3).
**Code read for definitions:** the read-only platform repo at the frozen SHA
`fa70688bc252d14f8d67e371afafc194731c324e` (`git show fa70688:<path>`), never HEAD.
**Script by:** Researcher (rule 9, written once from §4 as amended by `DECISIONS.md`) ·
**First pass run by:** Researcher, 2026-09-28, on the pinned parquet (DP-50(c): **no live query of any
kind produces any number here**) · **Standing per-freeze re-run:** Data Steward, byte-identical
script, published as `research/reports/LAYER_STRUCTURE_vNNN.md` (§9; decision 7).
**Determinism (rule 9, decision 8):** fixed RNG seed **`20260914`**, used for B2's permutation
reference (2,000 draws) and for both bootstraps of §4.6 (2,000 resamples each); `eval.py` prints the
seed, the draw counts and its library versions in the register header. A bounded Gate 0 re-run pass
reuses the same seed; a pass that changes the seed is a new pass and is recorded as one.
**DP-50 sweep at lock (2026-09-14, decision 9):** no repair shipping after the 2026-09-10 freeze can
reach a row here, the parquet being sha256-pinned — including `2d5776c` (PI-001), which touches
`uoa_symbol_daily.fwd_return_*`, **a table this question does not read at all** (§2.4). DP-50(b) runs
forward, not backward: a weights, multiplier, flag or scoring change shipped after this lock
constrains no brief — this verdict is about the engine **at `fa70688` on 2026-04-01..2026-09-10** —
it fires §9's standing re-run instead. Any repair rewriting historical `sas_candidates` rows still
gets its dated `DATA_NOTES.md` entry.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14 (decisions applied 2026-09-14) · **Decisions:** DECISIONS.md

---

## 1. Hypothesis (plain English, one sentence)

**The seven layer scores SAS prints are not seven independent signals: within a single night's
candidate slate they collapse onto three or four underlying factors, and most of any one layer can be
predicted from the others.**

H-076 is Haci's H6, filed with his own PASS / FAIL wording: *"are the agents ten signals or repeated
versions of three or four factors — PASS low-to-moderate conditional redundancy plus incremental
contribution; FAIL highly correlated layers and no incremental information → collapse the architecture
into fewer factors."* His PASS has two limbs. **This question decides the structure limb only**
(correlation, factor count, conditional redundancy); the incremental-contribution limb is H-075's.

**Label mapping, fixed here so the verdict cannot drift:**

| this question's label | Haci's H6 structure limb | controller verdict |
|---|---|---|
| **REDUNDANT** | FAIL (structure) | HISTORICALLY_CONFIRMED (`HISTORICAL_ONLY`) |
| **DISTINCT** | PASS (structure) | NULL (`HISTORICAL_ONLY`) |
| **MIXED** | neither | INCONCLUSIVE |

There is no directional edge to confirm and no effect size. The pre-registered object is **a fixed set
of structural statistics and a fixed threshold rule**, written before anyone looks at what they are.

## 2. Population

### 2.1 Units

- **The estimation unit is the within-night cross-section**: on each night, the candidates SAS scored
  at 16:05 and the layer scores it gave them. Selection is a within-night ranking problem, so the
  structure that matters for the architecture is the structure *within* a night's slate, not across
  the whole sample.
- **The unit of inference, and the unit every bootstrap resamples, is the trading night** (rule 6).
  Candidate rows are aggregated (centred and scaled) within a night before anything is pooled.
- The candidate row is the observation inside a night. Row counts never substitute for night counts
  in any floor (§5.1).

### 2.2 Exact filters on the frozen manifest

- **Source table:** `sas_candidates` (`super_agent_select_candidates_daily`), 6,479 rows,
  frozen SQL `WHERE trading_date <= '2026-09-10'`, sha256 `af40ad8a…aaa2f2`.
- **Nights:** `trading_date` 2026-04-01 .. 2026-09-10 (113 nights in `v001_sas_runs.parquet`), minus
  the exclusions of §2.3 → **102 nights**.
- **Rows:** **every candidate row on an included night, published or not** — H-076's population is
  "all 16:05 candidates". No filter on `qualified`, `threshold_pass`, `selected_rank`,
  `overall_score`, `completeness_score`, `dominant_direction` or `confidence_level`.
  **DP-28 is considered and does not apply as a filter:** it excludes dark-lane rows *from an arm of
  published picks*, and this question has no published arm. `qualified IS TRUE AND selected_rank IS
  NOT NULL` appears once, as a **descriptive stratum** (§4.4(v)), never as a population filter.
- **Tier-1 columns (the seven layers, the object of the test):** `flow_strength_score`,
  `technical_structure_score`, `gex_alignment_score`, `projection_score`,
  `fundamental_quality_score`, `catalyst_event_score`, `smart_money_confirmation_score`.
- **Supporting columns:** `overall_score`, `completeness_score`, `cross_layer_bonus`,
  `conflict_penalty`, `missing_data_penalty`, `best_timeframe`, `dominant_direction`,
  `confidence_level`, `qualified`, `selected_rank`, `source_membership_json`, `missing_data_json`,
  `market_regime_snapshot`, `score_details_json`, `created_at`, `updated_at`, `symbol`, `run_id`.
- **`sas_runs`:** `config_json` per night (point-in-time weights, timeframe multipliers, feature
  flags) and `trading_date` — used to recompute effective weights (§3 B3, §4.1) and to list the
  distinct configuration hashes with their date ranges (§10 threat 5).

### 2.3 Exclusions

The **11** nights in `exclusions_v003.json` (`manual_runs.trading_dates` 9 ∪ `non_session_runs` 1 ∪
`uncorroborated_publication_runs` 1) are **dropped and counted**, leaving **102 nights (34 in-sample
to 2026-05-29, 68 sealed from 2026-06-01)** — the file's own `night_counts_after_exclusions`, which
`eval.py` re-derives from `v001_sas_runs.parquet` rather than reading. The reason is the Q005 reason
and it is substantive here: on a re-run night the frozen row is a re-run's output 19–51 h after the
16:05 decision, not the decision's (`sas_candidates_availability_note_correction`), and on 2026-06-26
the frozen row set does not match the night's own run audit — in both cases the night's cross-section
is not the 16:05 cross-section this question is about. **A sensitivity including all 113 nights is
printed; it never decides, never promotes and never demotes a verdict line** (decision 5). A
disagreement between the 102-night verdict and the 113-night sensitivity is reported as evidence
**about the excluded nights**, not about the architecture.
`manual_runs.late_but_clean` nights are **kept** (that list exists precisely to say they are clean).

### 2.4 What is not read

No outcome column of any table is read anywhere: `outcome_*`, `level_hit_*`, `outcome_sealed_w60`,
`sas_excursion.*`, `uoa_symbol.fwd_return_*`. No price bar, no touch, no return, no excursion, no
`manifest_prices_v001`. **There is nothing in this question that could unseal anything**, which is why
it runs on the sealed freeze today (§5.3, the Q005 argument, DP-31).

### 2.5 Tier 1 and Tier 2 — and a column correction

- **Tier 1 (decides):** the seven layer subscore columns above. They are the stored form of
  `subscores` in volatilx `services/super_agent_select_scoring.py:1329-1332`, computed by
  `_score_flow_strength` (`:751`), `_score_technical_structure` (`:831`), `_score_gex_alignment`
  (`:882`), `_score_projection_strength` (`:925`), `_score_fundamentals` (`:979`), `_score_catalyst`
  (`:1014`) and `_score_smart_money` (`:1051`), and assembled at `:1220-1233`.
- **Tier 2 (secondary, descriptive, never decides):** the agent-level fields inside
  **`sas_candidates.score_details_json`**, written by `_serialize_score_details`
  (volatilx `services/super_agent_select_service.py:306-336`): `subscores`,
  `weighted_dimensions[*].{available, weight, base_weight, score}`, `direction_evidence`,
  `timeframe_evidence`, `cross_layer_bonus`, `conflict_penalty`, `missing_data_penalty`,
  `atr_projection_meta`, `projection_method_meta`, `gex_missing_offset_*`, `dir_ratio_polarity`,
  `flow_polarity_*`, `polarity_diagnostic`.
- **Correction to H-076's wording, recorded rather than silently applied (decision 1).** The BACKLOG
  entry names "the agent-level fields in `component_scores_json`". That column does not exist on
  `sas_candidates`: `component_scores_json` is a column of **`market_regime_daily`**
  (volatilx `models.py:1912`), holding the regime scorer's four components — `weekly_trend`,
  `daily_secular_structure`, `volatility`, `fib_phase` (`services/market_regime/scorer.py:506`) — one
  row per night, market-wide. It is a **night-level** object and therefore cannot enter a within-night
  cross-section of candidates at all. The candidate-level agent detail H-076 is reaching for is
  `score_details_json`, and that is what Tier 2 reads. **`market_regime_daily.component_scores_json`
  is not read anywhere in this question**, and the register prints that sentence once, in full — a
  night-level, market-wide object with four regime components — so the BACKLOG's wording cannot be
  re-borrowed by **H-083**, which cites the same phrase for its setup definitions (§9.1). The
  correction is a mis-named column, not a re-unit: the hypothesis's units, population and cuts are
  unchanged (DP-25 is not offended), and Tier 2 never decides (§4.5), so this cannot move a verdict
  in either direction.

### 2.6 Knowledge time (rule 14)

Every column read is written with the candidate at 16:05 ET on its own `trading_date`
(`manifest_v001.availability.sas_candidates`, as amended by
`exclusions_v003.sas_candidates_availability_note_correction`), or is the night's own `config_json`.
`market_regime_snapshot` is the point-in-time snapshot stored on the candidate row and is a different
object from `market_regime_daily` (§6). Nothing post-dates the pick night. **No new rule-14 exception
is requested** (DP-41): none is needed.

## 3. Baselines — what the structure is measured against

A diagnostic's baseline is the claim it audits, plus a reference for what "no association" actually
looks like in this data. There are three, and all three are computed and printed.

- **B1 — the architecture's own claim (the null).** Seven layers are seven signals: the retained-layer
  correlation matrix is the identity, the effective number of factors equals the number of retained
  layers `K`, and every layer's conditional R² on the others is 0. **DISTINCT means B1 survives.**
  B1 is also what the product copy asserts — a seven-layer score with weights projection 29 /
  technical 27 / flow 24 / catalyst 10 / fundamental 5 / smart-money 5 / GEX 0
  (`services/super_agent_select_models.py:8-22`).
- **B2 — the independence reference under this data's own arithmetic (the control that answers "is
  this just clamping and sparsity?").** Within each night, each layer's values are permuted
  **independently across candidates**, 2,000 draws under the fixed seed **`20260914`** (decision 8),
  preserving every layer's marginal distribution,
  its clamping to 0–100 (`_clamp`, `:18`), its discreteness and ties (the technical layer is a
  three-point mixture, `:852-877`), and its per-night missingness pattern. This gives the sampling
  distribution of every statistic in §4.3 under **exactly zero** cross-layer association at the same
  n. Each statistic is reported both raw and as an **excess over B2's median**, because with lumpy
  three-valued layers the independent value of the effective-factor count is not exactly `K`.
  **B2 draws are Monte Carlo and never add to n** (rule 6); B2 produces a reference, not a verdict.
- **B3 — the known-redundant positive control (the upper reference, and Gate 0's target).** Two
  relationships that are redundant *by construction* and must show up as such or the script is wrong:
  (i) `overall_score` against the weighted average of the layers recomputed with that night's own
  effective weights (`_effective_dimension_weights`, `:682-722`, applied at `:1316-1348`, with
  `cross_layer_bonus` `:1078`, `conflict_penalty` `:1116`, the missing penalty `:1364-1368`, the +5
  GEX-missingness offset and clamp `:1379-1399` and the ATR-elite block `:1401-1423`); and
  (ii) `completeness_score` against the effective-weight share of available layers (`:1347`).
  Both must reach R² ≥ 0.90 on their defined domain.

**Descriptive reference, not a baseline:** the effective-weight vector itself. Whatever redundancy is
found is reported next to *how much of the score the redundant layers actually carry* — base weights
(`:8-22`) × timeframe multipliers (`:37-66`), per `best_timeframe`. A redundancy between two layers
carrying 0 and 5 weight is a different product fact from one between the 29- and 27-weight layers.

## 4. Objective metric — the layer-structure register

**Rule 5's price-path objective does not apply**, and the reason is that no outcome exists in this
question: no entry basis, no ladder target, no touch, no control cohort, no fixed-horizon return.
DP-01, DP-03, DP-08, DP-09, DP-11 and DP-12 are inapplicable and are cited here only to record that
they were considered. **DP-10, DP-20 and DP-44 (MPEs) are inapplicable**: there is no effect size in
ATR or in percentage points to clear. The thresholds in §8 serve the MPE's role — they are fixed here,
before the run, and are never adjusted afterwards (the Q005 pattern).

### 4.0 Definitions, fixed before the run

- **Within-night standardisation (DP-26 convention, not derived from any outcome).** For night `t`
  and layer `j`, `Z_ijt = (x_ijt − mean_t(x_·jt)) / sd_t(x_·jt)` over the candidates of that night
  with a non-null value. A (night, layer) with zero within-night variance contributes no pair for
  that layer and is counted. Both the **within-night** matrices (primary) and the **pooled raw**
  matrices (descriptive) are printed; their difference is the across-night / tape component and is
  named as such (§10 threat 4).
- **Association measure:** **Spearman** rank correlation with mid-ranks, primary, because several
  layers are heavily discretised and clamped. **Pearson** is printed as a sensitivity and never
  decides.
- **Retained layer set `K` (coverage rule, fixed at draft).** Within a cell, a layer is **retained**
  if it is non-null on **≥ 70%** of the cell's candidate rows **and** has **≥ 5 distinct values**
  **and** has non-zero within-night variance on **≥ 50%** of the cell's nights. Layers failing any
  clause are **dropped from the matrix, named, and reported with their coverage, distinct-value count
  and null share**. A dropped layer is recorded as *not an independent signal in that cell* — it is
  never read as evidence of distinctness (§8 criterion (d)). **The 50% and 90% coverage-floor
  sensitivities are computed and they bind (decision 3):** a criterion that turns on `K` must survive
  the floor that works against it, so §8's criterion (d) requires `K ≤ 4` at **70%** *and* at **50%**,
  and DISTINCT's `K ≥ 5` requires `K ≥ 5` at **70%** *and* at **90%**; otherwise that line is MIXED.
  Criteria (a)–(c) keep the two CIs of §4.6 as their guard and print the 50% / 90% sensitivities
  beside them — the asymmetry is deliberate, not an omission.
- **Complete-case rows.** Within a cell, rows used for the matrix are those with a non-null value on
  **every retained layer**; the retained rows and the dropped rows are counted per night, and the
  **missingness-indicator** correlation matrix (one 0/1 column per layer) is printed beside the score
  matrix, **always**, because missingness is itself informative (§10 threat 2). **The
  pairwise-complete matrix is a binding companion, not a footnote (decision 2):** where it is positive
  semi-definite and its §8 criterion crossing **disagrees** with the complete-case primary on the same
  criterion in the same cell, **that criterion's line is INCONCLUSIVE (MIXED)**, never the favourable
  half; where it is **not** PSD, that fact and the smallest eigenvalue are printed and the sensitivity
  is reported as **uncomputable for S1/S2** — which is the arithmetic reason complete-case is primary:
  S1 and `N_eff` are eigenvalues, and a pairwise matrix need not be PSD.

### 4.1 Gate 0 — positive control (run first, read first)

The script must independently re-find five things that are already known — four from the frozen
parquet and the code at `fa70688` alone, the fifth a check on its own construction:

**Every item below is a pre-stated, binary, row-level condition** (decision 6 — "arithmetically
verified" without a tolerance is not a pre-registered rule, the Q026 item-2 lesson; a share threshold
invented at draft would be a number with no source, DP-25 / DP-26). Where the expected fact is
distributional, the gate is an **identity against that night's own `sas_runs.config_json` and the code
at `fa70688`**, and the distribution itself is **printed, not gated**.

(a) `score_details_json.subscores` equals the seven stored subscore columns row by row to relative
tolerance **1e-6** on every row where both exist (`:1329-1332` writes one from the other);
(b) **B3(i)** — `overall_score` reconstructed from the night's effective weights reaches **R² ≥ 0.90**,
and **B3(ii)** — `completeness_score` likewise. Both are computed on **every included row, with no
domain carve-out**; the registered arithmetic is the full chain §3 B3 names (effective weights
`:682-722`, `cross_layer_bonus` `:1078`, `conflict_penalty` `:1116`, the missing penalty `:1364-1368`,
the +5 GEX-missingness offset and clamp `:1379-1399`, the ATR-elite block `:1401-1423`). A row class
the script cannot reconstruct is **named, counted and left in the denominator** — the domain is not
chosen at run time — and the target stays **R² ≥ 0.90**;
(c) **identity, row by row at relative tolerance 1e-6:** on every night whose `config_json` has
`enable_smart_money_enrichment` **false**, or lacks the key (the code default `False` at
`services/super_agent_select_models.py:111` governs, and those nights are **counted**), the
re-implemented `_effective_dimension_weights` (`:709-710`) gives `smart_money_confirmation` an
effective weight of **exactly 0** on **every** row. `smart_money_confirmation_score`'s null share,
constant share and distinct-value count — the **PI-008** picture — are **printed, not gated**;
(d) **identity:** `gex_alignment`'s base weight parsed from **every** night's `config_json` is
**exactly 0.0** (`services/super_agent_select_models.py:9-17` — computed for audit visibility, zeroed
out of the weighted average). Its null share and distinct-value count are **printed, not gated**;
(e) **script-correctness gate:** Gate 0 **fails if the catalyst layer is pooled across 2026-06-01
anywhere in a verdict-carrying cell** (DP-06, platform commit `69ef05f`; the split is mandatory
whether or not a difference is visible). The per-month catalyst panel either side of that date is
**printed, not gated**.

**If Gate 0 does not re-find every one of these, the verdict is INCONCLUSIVE and no other section of
the register is interpreted** (§8). The fix-and-re-run loop is bounded at **two passes inside the hard
stop of 2026-10-12**, each recorded with its diff and date, each reusing the seed of §4.6; **no Gate 0
target is ever relaxed to make a pass succeed.**

### 4.2 What is computed, per cell

Every statistic below is computed per cell (§4.4) on the within-night standardised, complete-case,
retained-layer data, and every one carries **both** confidence intervals of §4.6.

### 4.3 The structural statistics

- **S1 — top-two variance share.** The share of total variance carried by the first two principal
  components of the retained-layer Spearman matrix, `(λ₁ + λ₂) / Σλ`. This is H-076's own named
  statistic.
- **S2 — effective number of factors.** The participation ratio `N_eff = (Σλ)² / Σλ²`, reported with
  `N_eff / K` and with `N_eff − median(N_eff under B2)`.
- **S3 — conditional redundancy.** For each retained layer `j`, `R²_j` from an OLS regression of `Z_j`
  on the other `K − 1` retained layers, pooled within the cell. Reported for **every** layer, always,
  and summarised by `max R²`, `median R²`, and the **count of layers with `R²_j ≥ 0.50`**. The
  precision-matrix form `R²_j = 1 − 1/(R⁻¹)_jj` is printed as a cross-check; if the matrix's condition
  number exceeds `1e6` the OLS form governs and the condition number is printed.
- **S4 — the full pairwise matrix (descriptive, printed in full, always).** Every pair's Spearman
  correlation with both CIs, plus Pearson, plus each layer's null share, distinct-value count and
  within-night variance share. **No pair and no layer may be omitted from this table** — this is the
  guard against reporting only the flattering half (the Q005 rule).
- **S5 — weight-carried redundancy (descriptive).** The effective-weight-weighted share of
  `overall_score` variance attributable to PC1 and to PC1+PC2, per `best_timeframe`: how much of the
  *score* actually rides on the redundant directions.

### 4.4 Cells

1. **Pooled, all included nights** — the cell the verdict is stated on.
2. **Period split (required, DP-06 and rule 7):** **P0 = 2026-04-01 .. 2026-05-29** (34 nights) and
   **P1 = 2026-06-01 .. 2026-09-10** (68 nights). The catalyst layer is a different feature across
   this boundary, and the in-sample / sealed boundary (`in_sample_end = 2026-05-29`) is the same cut.
   **A structural claim counts only if it holds in both** (§8).
3. **`best_timeframe` strata:** short / swing / long, separately — H-076's named stratification, and
   the reason it matters is in the code: the timeframe multipliers change the effective weights and
   zero some layers entirely (`_effective_dimension_weights`, `:682-722`;
   `_default_timeframe_weight_multipliers`, `services/super_agent_select_models.py:37-66`, where
   `fundamental_quality` runs 0.15 / 0.35 / 1.00 and `gex_alignment` 1.0 / 0.9 / 0.6 across
   short / swing / long).
4. **Monthly panel:** `N_eff` per calendar month (2026-04 .. 2026-09), with both CIs — H-076's
   "effective number of factors per month".
5. **Descriptive strata, no verdict line:** published (`qualified IS TRUE AND selected_rank IS NOT
   NULL`, DP-28's predicate) vs the rest; `dominant_direction` bullish / bearish / mixed; and, for
   nights ≥ 2026-06-09 only, `market_regime_daily` regime (§6).

### 4.5 Tier 2 (secondary, descriptive, never decides)

Tier 2 is **`sas_candidates.score_details_json`** and nothing else (decision 1);
**`market_regime_daily.component_scores_json` is not read anywhere in this question**.
Parse `score_details_json` on every included row and report **parse coverage per field per month**
first. Fields clearing a **90%** parse-coverage floor in a cell get the same S1–S3 treatment,
reported beside Tier 1. Nothing in Tier 2 enters §8. The reason for the floor and the per-month
reporting is schema drift inside this JSON over the sample — fields were added and removed during the
window (volatilx `docs/POLARITY_ROLLBACK_2026_05_16.md`; `docs/STALE_SETUP_GATE_FINDINGS.md:183`
removes the `stale_setup_*` fields from `_serialize_score_details`) — so a field whose schema changes
mid-sample is reported per period and never pooled across the change.

### 4.6 Inference — two confidence intervals on every statistic (DP-51)

Every statistic in §4.3 is reported with **both**:

- the **night-clustered bootstrap CI**: 2,000 resamples of **nights** with replacement (never of
  candidate rows), percentile 95%; and
- the **episode-clustered CI (DP-51)**: an **episode** is one symbol's run of *candidate appearances*
  with gaps of ≤ 10 sessions between successive appearances (the TI-003 / Q003 window); the bootstrap
  resamples **episodes and nights jointly**, 2,000 resamples, percentile 95%.

**Determinism (decision 8, rule 9).** Both bootstraps and B2's permutation reference run under the
single fixed RNG seed **`20260914`**, named here at lock and derived from no outcome (DP-26; the Q027
convention): 2,000 draws for B2 and 2,000 resamples for each bootstrap. `eval.py` prints the seed, the
three draw counts and its library versions in the register's header, so every number is re-derivable
to the digit at any later freeze (§9's standing re-run depends on that). A bounded Gate 0 re-run pass
reuses the same seed; a pass that changes it is a new pass, recorded with its diff and date.

**DP-51 applies here and is not waived.** It bites harder in this question than in most: the same
symbols recur in the candidate universe night after night, so a pooled correlation matrix is driven by
a much smaller number of independent symbol-episodes than its row count suggests. Per DP-51's clause,
translated to a threshold question: **a threshold crossing that holds on the night-clustered CI and
not on the episode-clustered CI makes that line INCONCLUSIVE, never a verdict** (§8). Both CIs are
printed for every statistic in every cell, including the ones that do not cross a threshold.

No other inference is performed. There is no estimate of an effect, no standard error on a return, no
permutation test that decides: B2's permutation reference is printed as a comparison column and is
explicitly **not** a decision rule (§7).

## 5. Sample floors, expected n, window and schedule

### 5.1 Floors (rule 6, DP-21)

This question has **no primary endpoint in the effect-size sense**, so rule 6's floors do not bind in
their usual form — and **none is waived**. They are applied in the strictest available reading:

- **Every cell that carries a verdict line needs ≥ 20 contributing nights** (DP-21's cell floor) **and
  a median of ≥ 10 complete-case rows per contributing night.** A cell below either is **demoted to
  descriptive at lock and printed, never dropped** (DP-43's demote-not-drop).
- **The pooled cell and both period cells clear DP-21's 80-night reading** for the pooled cell and the
  20-night reading for each period cell: **102 / 34 / 68 nights**.
- The `best_timeframe` strata are the cells most at risk: their per-night row counts are unknown at
  drafting (no desk report measures the `best_timeframe` mix). The rule above is applied by `eval.py`
  from the **measured** counts, and any stratum below it prints as descriptive. No stratum's floor is
  reduced to let it carry a verdict.

### 5.2 Expected n

From the pinned freeze (`research/reports/FREEZE_v001.md` §1, sha256-pinned — **no live query**):
**6,479 candidate rows over 113 nights**, ≈ 57 candidates per night; **102 nights after exclusions**
(34 in-sample, 68 sealed, `exclusions_v003.night_counts_after_exclusions`). `eval.py` derives its own
included-row count and prints it; the figure is not hard-coded here.
**No Steward exposure report is required and R1 is not a lock condition**: nothing accrues, the data
is already mature, so there is no run-rate to measure and no projection to make (the Q026 reading).

### 5.3 Window — the sealed freeze, now (DP-31 applies, on its own terms)

The test window **is** the frozen period, **2026-04-01 .. 2026-09-10**, and the question runs on the
sealed `manifest_v001` **immediately**. This is not a shortcut to a date, and it rests on two facts
that are checkable in §2.4: **no outcome column of any table is read**, and **no price bar is read at
all**, so no verdict about any edge can move as a result of running this file and the sealed period
stays sealed for every question that measures a price path (rule 3; the Q005 argument, cited in
H-076's own BACKLOG entry). What the question is *about* — the factor structure of the scoring engine
at SHA `fa70688` — is a property of that engine on that period, and a later freeze under a different
config is a different object.

### 5.4 Schedule (final; `schedule.json`, written from `DECISIONS.md` "## Schedule", 2026-09-14)

**decision_date: Monday 2026-09-28 · extension_date: none · hard_stop: Monday 2026-10-12 ·
rule: fixed** (not exposure-driven; the population closed 2026-09-10 and the measured post-lock
projection is **0 contributing nights, exactly**).

- **2026-09-14/15** — lock (`--by desk`, DP-46), the decisions having been applied. Population pinned
  at `manifest_v001`; **no price manifest**; no freeze work is required for the lock (DP-23
  inapplicable — this question's population is complete at v001).
- **by Friday 2026-09-25** — the **Researcher** commits `eval.py`, written once from §4 as amended by
  the decisions (rule 9), with the exclusion set derived from `exclusions_v003.json` at run time
  (decision 5) and the seed, draw counts and library versions printed in the register header
  (decision 8).
- **Monday 2026-09-28** — the **Researcher** runs it on the pinned parquet, **Gate 0 first and read
  first** (§4.1). One pass, no interim look (rule 9). Output:
  `research/reports/LAYER_STRUCTURE_manifest_v001.md`.
- **hard stop Monday 2026-10-12** — the outer bound on §4.1 / §8's bounded Gate 0 fix-and-re-run loop
  (at most two passes, each with its diff and date). Gate 0 still failing there ⇒ **INCONCLUSIVE**,
  ledgered as such, register filed incomplete, script defect to the Researcher.
- **after the verdict, standing** — the **Data Steward** re-runs the byte-identical script at every
  subsequent freeze **and** whenever `sas_runs.config_json`'s hash changes, publishing
  `LAYER_STRUCTURE_vNNN.md` (decision 7; DP-50(a)).
- **gates:** none of the rule 6 effect-size form — there is no primary endpoint. The floors that do
  bind are §5.1's, in their strictest reading and **none waived**: ≥ 20 contributing nights **and** a
  median ≥ 10 complete-case rows per contributing night for every verdict-carrying cell, met by the
  pooled (**102**), P0 (**34**) and P1 (**68**) cells; a `best_timeframe` stratum or a month below
  either is **demoted to descriptive at lock and printed, never dropped**. **DP-24 is unreachable by
  design and §8 says so** (DP-31); **`HISTORICAL_ONLY`** labels the verdict in every branch, beside
  "structure limb only — contribution untested (H-075)" (decision 4).
- **ceiling:** DP-43's 12 months is not engaged — the decision date is 14 days after the lock.

**No extension exists.** DP-13's automatic extension and DEFERRED fallback answer "the floors came up
short at the decision date", and no floor can come up short on already-mature frozen data; nothing
accrues, so DP-43's exposure-driven schedule has no input (`rule: fixed`) and its 12-month ceiling is
not engaged.

## 6. Split and stratification

- **Calendar split = the DP-06 split.** P0 (to 2026-05-29, in-sample) and P1 (from 2026-06-01,
  sealed) as in §4.4(2); the two boundaries coincide to the session, so one cut serves both rule 7's
  "must hold in both halves" and DP-06's catalyst split. A structural finding that appears in only one
  period is **not a finding** and is labelled unstable (§8).
- **Monthly panel** (§4.4(4)) sits underneath the two-period split so no conclusion is an artefact of
  where the cut falls (the Q005 pattern). Any month with fewer than 20 contributing nights is labelled
  as such and no trend is read from it.
- **Regime (rule 7).** `market_regime_daily` is knowledge-time-legal only from **2026-06-09**
  (`regime_version='v1.2'`; the whole 2026-01-02..2026-06-08 range was backfilled 06-02/06-08 —
  manifest_v001 `availability.market_regime`, `exclusions_v003.regime_label_point_in_time_from`). It
  is therefore used as a **descriptive stratum for nights ≥ 2026-06-09 only** and never for the whole
  sample. `sas_candidates.market_regime_snapshot` **is** point-in-time (written with the candidate at
  16:05) and is the whole-sample regime descriptor; the two are different objects and are never
  conflated (the Q005 §6 distinction).
- **Nothing in this question's design is data-derived from a sealed look.** EXPLORE_001 examined
  price paths, entry timing and volatility; it contains **no correlation, PCA or subscore-structure
  analysis at all** (verified 2026-09-14: no match for `correlat|PCA|subscore` in
  `research/reports/explore/EXPLORE_001.md`). The 0.80 threshold is H-076's own text; the remaining
  thresholds, the coverage floor, the Spearman choice and the within-night standardisation are
  Registrar conventions fixed at draft under **DP-26**.

## 7. Multiple testing

**No correction, because nothing here is a hypothesis test.** The register reports **no p-value and no
q-value**: Gate 0 is a reproduction check, the statistics are descriptions of a frozen matrix, and B2's
permutation reference is a comparison column, not a decision rule. Q028 is filed in **F8** and, per
that family's header in `research/BACKLOG.md`, **enters no BH correction set** — F8's correction runs
across the members that carry primaries (H-074, H-081, H-083), and Q028 neither joins that set nor
changes any other family's denominator.

The guard against selective reporting is structural rather than a q-threshold, and it is fixed here:
**S4's full pairwise table, every layer's `R²_j`, every cell and every dropped layer's coverage are
printed in full, always**, and §8's rule is applied to whatever appears, never to a subset chosen
afterwards.

## 8. Decision rule (numeric, written before unsealing)

Let `K` = retained layers in the cell (§4.0), and `S1`, `S2 = N_eff`, `S3 = {R²_j}` as in §4.3, each
with its **night-clustered** and **episode-clustered** 95% CI (§4.6). "Both CIs" below means the
stated bound holds on **each** of the two.

**Gate 0 first.** If §4.1's positive control — as restated there in binary, row-level form (decision
6) — does not re-find all five items, the verdict is **INCONCLUSIVE** and nothing else in the register
is interpreted. At most **two** fix-and-re-run passes, each recorded with its diff and date, each
under the same seed, all inside the hard stop **2026-10-12**; still failing there ⇒ **INCONCLUSIVE**,
filed incomplete. **No Gate 0 target is ever relaxed to make a pass succeed.**

**REDUNDANT ⇒ HISTORICALLY_CONFIRMED (label `HISTORICAL_ONLY`)** — in the pooled cell **and** in both
P0 and P1, at least one of:

- **(a)** `S1 ≥ 0.80`, with both CIs' **lower** bounds ≥ 0.80 *(H-076's own threshold)*;
- **(b)** `N_eff ≤ 3.0`, with both CIs' **upper** bounds ≤ 3.0;
- **(c)** at least **3** retained layers with `R²_j ≥ 0.50`, each with both CIs' **lower** bounds
  ≥ 0.50;
- **(d)** `K ≤ 4` at the **70%** coverage floor **and** at the **50%** floor (decision 3 — a criterion
  that turns on `K` must survive the floor that works against it; `K ≤ 4` at 70% but not at 50% is
  **MIXED**) — fewer than five of the seven layers carry usable within-night variation under §4.0's
  coverage rule. A layer that is null, constant, or without within-night variance is not an
  independent signal, and if four or fewer survive, the seven-layer architecture is already at most
  four signals **as measured**, whatever the correlations among the survivors are.

**The route is named in the verdict (decision 3(i)).** A REDUNDANT verdict is written
`REDUNDANT (correlation route)` when it is reached through (a)/(b)/(c), `REDUNDANT (dead-layer route)`
when reached through (d), and both labels where both fire. Both map to HISTORICALLY_CONFIRMED /
`HISTORICAL_ONLY` and neither changes §9.

**A dead-layer finding prints its cause (decision 3(iii)).** The verdict sentence names **each dropped
layer** with its null share, its distinct-value count, **its cause at `fa70688`**
(`enable_smart_money_enrichment` / `enable_fundamental_enrichment` default `False`,
`services/super_agent_select_models.py:110-111`; `gex_alignment` base weight `0.0`, `:9-17`; or absent
context) and **the summed effective weight the dropped layers carry**. A `K ≤ 4` verdict is a true
statement about *this freeze's configuration*, not an architecture indictment — §9 already forbids
acting on it either way.

**DISTINCT ⇒ NULL (label `HISTORICAL_ONLY`)** — in the pooled cell **and** in both P0 and P1, **all**
of:

- `K ≥ 5` at the **70%** coverage floor **and** at the **90%** floor (decision 3; `K ≥ 5` at 70% but
  not at 90% is **MIXED**); **and**
- `S1 ≤ 0.60`, with both CIs' **upper** bounds ≤ 0.60; **and**
- `N_eff ≥ 0.70 × K`, with both CIs' **lower** bounds ≥ `0.70 × K`; **and**
- **no** retained layer has `R²_j ≥ 0.50` on the point estimate.

**MIXED ⇒ INCONCLUSIVE** — anything else. Specifically and non-exhaustively: the statistics fall
between the two bands; the REDUNDANT and DISTINCT criteria disagree between P0 and P1 (rule 7 — a
structure that holds in one period is not a result); a criterion is met on the night-clustered CI and
not on the episode-clustered CI (**DP-51**); a criterion's crossing on the **pairwise-complete**
matrix (where that matrix is PSD) disagrees with the complete-case primary on the same criterion in
the same cell — **that criterion's line is INCONCLUSIVE, never the favourable half** (decision 2; a
non-PSD pairwise matrix prints its smallest eigenvalue and is uncomputable for S1/S2, which cannot
resolve a disagreement in either direction); criterion **(d)** or DISTINCT's `K ≥ 5` holds at the 70%
floor but not at the sensitivity floor that works against it (decision 3); or Gate 0 passes but the
OLS and precision-matrix forms of `S3` disagree about which layers clear 0.50. In every MIXED branch
the register prints the full numbers and states plainly that the structure limb is undecided.

**What this verdict does *not* settle, stated in the verdict sentence itself.** H6's PASS needs *low
redundancy* **and** *incremental contribution*. This question decides only the first. A **DISTINCT**
verdict here does **not** mean the layers carry independent predictive information — uncorrelated
layers can all be uninformative — and a **REDUNDANT** verdict does **not** by itself justify collapsing
the architecture: correlated layers can each still add. The joint H6 answer is assembled from this
question and **H-075**'s partial IC by the Reporter (the H-077 pattern), from ledgered verdicts only.

**The scope travels with the verdict as a fixed label (decision 4).** Whatever the branch, the verdict
is restated — in §9, in the register, in `research/LEDGER.md` and anywhere else it is quoted — as
**"structure limb only — contribution untested (H-075)"**, beside **`HISTORICAL_ONLY`** (DP-31) and
`NON_QUOTABLE` (rule 12). Q028 is **ledgered on its own** and does not wait for H-075: H-083's setup
rule and H-075's estimability scoping both take this register as an input (§9.1, §9.2), Q028 carries
no primary and joins no correction set (DP-29, §7), and no architecture change follows from this
question in either branch (§9).

**PROSPECTIVELY_CONFIRMED is unreachable from this run by design** (DP-31). The measured post-lock
projection is **0 contributing nights, exactly**: the population is a freeze taken 2026-09-10, four
days before this lock, and closed; nothing accrues and no waiting changes it. **DP-31's
successor-prospective-question clause resolves, here as in Q026 and for the same reason, to §9's
standing re-run rather than to a successor PREREG** — DP-31 exists to keep a *tradeable* verdict
reachable without an interim look, and **no branch of this question can ever produce a tradeable
verdict**, because it reads no outcome. That reasoning is stated so it cannot be borrowed by a
question that does read one.

**No MPE applies** (DP-10 / DP-20 / DP-44 inapplicable, §4). The thresholds 0.80 / 3.0 / 0.50 / 0.60 /
0.70×K / K ≤ 4 / K ≥ 5 serve the MPE's role and are fixed here, before the run.

## 9. If REDUNDANT (and if DISTINCT), what changes

**Opening, per DP-31 and rule 10: no guide line, no lane rule, no playbook entry, no product change,
no marketing claim and no quotable number follows from either verdict of this question.** Its verdict
carries the labels **`HISTORICAL_ONLY`** and **"structure limb only — contribution untested (H-075)"**
(decision 4) wherever it is restated, ledgered or quoted, and every number it produces is
`NON_QUOTABLE` (rule 12). Two further reasons make this stricter than usual here: the
verdict is one limb of H6 (§8), and an architecture change needs H-075 as well.

**What it does change, all internal:**

1. **It supplies H-083's setup definitions.** H-083 (A/B/C architecture) assigns setups from 16:05
   columns; whether "flow-led" and "projection-led" are even separable is exactly `S3` and `S4`. The
   register is the input to that PREREG's setup rule, which is then frozen there.
2. **It scopes H-075.** A partial-IC design cannot separate two layers whose `R²` on each other is
   near 1; the retained set, the coverage rule's casualties and the pairwise table tell H-075 which
   per-layer contrasts are estimable at all.
3. **A dead-layer finding goes to the existing issues, with measurement attached.** `smart_money`
   already sits as **PI-008** (`HACI_DECIDED:accept` — "CLAUDE.md's 'smart-money 5' and any marketing
   of a seven-layer score overstate it"); this question supplies the counted version. If
   `fundamental_quality` is also dead in the sample (`enable_fundamental_enrichment` defaults `False`,
   `services/super_agent_select_models.py:110`), or if `gex_alignment`'s coverage is as thin as
   H-076 expects at weight 0, a **new PI** is filed against the seven-layer description with the
   measured coverage — filed with a recommendation, the decision Haci's (**DP-48**), and any brief
   that follows hands the coding agent **no database step** (**DP-49**).
4. **An internal `EN`** is filed proposing that the nightly check print the effective-factor count and
   the live-layer count, so architecture drift is visible without a study. `INTERNAL_TOOL`, flag-off,
   never subscriber-facing (DP-48, rule 11).
5. **On DISTINCT:** the seven-layer description survives its structure test at census strength on this
   freeze, and that sentence — with its `HISTORICAL_ONLY` label and the fixed qualifier **"structure
   limb only — contribution untested (H-075)"** — is what may be said internally. Nothing becomes
   quotable.

**In both branches — the standing re-run (registered here as a Data Steward step; the Steward owns the
re-run only, the Researcher writes `eval.py` once and runs the first pass — decision 7, rule 9).** The
register is written to `research/reports/LAYER_STRUCTURE_manifest_v001.md`, ledgered with this
question under the label of decision 4, and the
**byte-identical script runs at every subsequent freeze**, published as `LAYER_STRUCTURE_vNNN.md`, and
**additionally whenever `sas_runs.config_json`'s hash changes** — a weights or flag change is a change
to the architecture under test, which is why the re-run trigger is the config and not only the
calendar. This is what DP-31's successor clause resolves to in §8, and it is also what DP-50(a)
requires, because a successor freeze can disagree with its predecessor about the past.

## 10. Known threats to validity (registrar's own list)

1. **Discreteness, clamping and ties.** The technical layer is a three-point mixture weighted 0.45 /
   0.35 / 0.20 (`:852-877`), several layers are clamped to 0–100 (`:18`), and `_component_average`
   (`:439`) produces heavy ties. Rank correlations on such variables are attenuated in ways a naive
   reading would call "independence". **B2** — permutation with identical marginals, ties and
   missingness — is the defence, and every statistic prints its excess over B2's median.
2. **Missingness is informative, and complete-case rows are a selected subset.** A layer is null
   because its *context* is absent (`_effective_dimension_weights` zeroes the weight in exactly that
   case, `:707-718`), which correlates with `missing_data_penalty` and `completeness_score`. The
   missingness-indicator matrix is printed beside the score matrix, complete-case retention is counted
   per night, and the pairwise-complete sensitivity is printed **and binds** — a PSD pairwise matrix
   that crosses a criterion the other way makes that criterion INCONCLUSIVE (§4.0, §8; decision 2).
   This is a real limit on how far a DISTINCT verdict generalises to the rows that were dropped.
3. **Repeated symbols.** The candidate universe re-selects the same names night after night, so the
   pooled matrix has far fewer independent units than rows. This is exactly H-070's hazard; **DP-51's
   episode-clustered CI** is registered as a *gate*, not a footnote (§4.6, §8).
4. **Within-night standardisation removes the tape.** Two layers that co-move only *across* nights —
   both rising when the market rises — will look independent within night. That is the right frame for
   a within-night ranking engine, but it is a choice: the **pooled raw** matrices are printed beside
   the within-night ones and the difference is reported as the across-night component, not hidden.
5. **A configuration change mid-sample mixes two architectures.** Weights, multipliers and feature
   flags are point-in-time in `sas_runs.config_json`; the register lists the distinct config hashes
   with their date ranges first, and reports a cut at any change date (the Q005 Channel 3a discipline).
   The known one is the v1.5 reallocation that moved `gex_alignment` to 0.0 and lifted technical
   20→27, projection 26→29, catalyst 8→10 (`services/super_agent_select_models.py:9-13`, dated
   2026-05-14 in the code comment) — inside this window.
6. **`K` depends on the coverage floor.** 70% is a Registrar convention (DP-26); at 50% a
   half-populated layer survives and at 90% it does not, and criterion (d) turns on it. **Decision 3
   makes the sensitivity binding rather than decorative:** criterion (d) must hold at 70% **and** 50%,
   DISTINCT's `K ≥ 5` at 70% **and** 90% — each criterion is checked at the floor that works against
   it — otherwise the line is MIXED. Both sensitivities are printed for every criterion, and the
   verdict sentence names the floors it used.
7. **Eigenvalue sampling error at small `K`.** With four to seven variables, `S1` and `N_eff` have
   material sampling error even at thousands of rows; the two CIs and B2 are the guard, and a
   threshold crossing inside either CI is INCONCLUSIVE by §8, not a near-miss to be argued.
8. **This is about the score's inputs, not its information.** Two uncorrelated layers can both be
   worthless; two correlated layers can both add. §8 says so in the verdict sentence, and H-075 is
   the other half.
9. **The catalyst layer is two different features across 2026-06-01** (DP-06, `69ef05f`). A pooled
   matrix straddling that date is printed and never decides; the P0/P1 requirement in §8 is what makes
   that binding rather than advisory.
10. **Tier 2's schema drifts.** `_serialize_score_details`'s field set changed inside the window
    (polarity rollback 2026-05-16; `stale_setup_*` removed). Parse coverage per field per month is
    printed first, the 90% floor governs, and no field is pooled across its own schema change. Tier 2
    never decides, which bounds this threat.
11. **One freeze, one SHA.** The structure reported is the structure of the engine at
    `fa70688` on 2026-04-01..2026-09-10. §9's standing re-run — triggered by a new freeze **or** a
    config-hash change — is what keeps that claim from being quietly generalised forward.
12. **The re-run and uncorroborated nights are excluded, not repaired.** 11 nights' cross-sections are
    not the 16:05 cross-sections and cannot be reconstructed (no append-only run history, EN-001); the
    all-113-night sensitivity is printed so the cost of the exclusion is visible rather than assumed,
    and it **never promotes and never demotes** a verdict line (decision 5) — a disagreement is
    evidence about those 11 nights, not about the architecture.

## 11. Decisions before lock

Recorded in DECISIONS.md (2026-09-14). Routed items still open: **none**. All nine items are DECIDED —
five drafted here plus four raised by the Decision-maker; **no item was defaulted on Haci's behalf and
none reached the ASK class** (no rule-14 exception, nothing that encodes how he trades, no trade-off
between waiting and sample — the population closed 2026-09-10 — and no MPE in any unit). The
Registrar's recommended option was taken on all five drafted items, **four of them tightened**; no
floor, threshold, gate, CI clause or cell was weakened. Sections above are as amended by these
decisions, and the seven corrections listed in DECISIONS.md "## Corrections to silent choices" are
applied in full.

| # | Decision | Choice | Where it lives |
|---|---|---|---|
| 1 | Which column carries the "agent-level fields" H-076 names | **A** — Tier 2 reads `sas_candidates.score_details_json` (`_serialize_score_details`, `services/super_agent_select_service.py:306-336`); **`market_regime_daily.component_scores_json` is read nowhere here** and the register prints, once, that it is a night-level market-wide object with four regime components, so H-083 cannot re-borrow the BACKLOG's wording | §2.5, §4.5 |
| 2 | Missingness handling for the matrices | **A, made binding** — complete-case rows on the retained set are primary (S1 and `N_eff` are eigenvalues; a pairwise matrix need not be PSD); where the pairwise-complete matrix **is** PSD and crosses a criterion the other way, **that criterion's line is INCONCLUSIVE (MIXED)**, never the favourable half; where it is not PSD, the smallest eigenvalue prints and S1/S2 are uncomputable on it | §4.0, §8, §10.2 |
| 3 | A layer that is null, constant or without within-night variance | **A, with three tightenings** — dropped, named, counted, read as *not an independent signal* (criterion (d)); **(i)** the route is labelled `REDUNDANT (correlation route)` / `REDUNDANT (dead-layer route)`; **(ii)** criterion (d) must hold at the **70%** *and* **50%** floors, DISTINCT's `K ≥ 5` at **70%** *and* **90%**, else MIXED; **(iii)** the verdict sentence names each dropped layer with its null share, distinct-value count, **cause at `fa70688`** and the **summed effective weight** dropped | §4.0, §8, §10.6 |
| 4 | Ledger the structure verdict alone, or hold it for H-075 | **A** — ledgered on its own with the fixed label **"structure limb only — contribution untested (H-075)"** beside `HISTORICAL_ONLY` (DP-31) and `NON_QUOTABLE` (rule 12), used verbatim wherever the verdict is restated; the joint H6 answer is the Reporter's, from ledgered verdicts only; **no architecture change follows in either branch** | §8, §9 |
| 5 | The 11 `exclusions_v003` nights | **A** — excluded from every verdict-carrying cell (DP-22, DP-04); the all-113-night version is printed and **never decides, never promotes, never demotes**; `eval.py` derives the set from the JSON at run time, `late_but_clean` nights kept | header, §2.3, §10.12 |
| 6 | Gate 0's targets, made enforceable *(raised at decide)* | **(b)** every included row, **no domain carve-out**, target **R² ≥ 0.90**, unreconstructible rows named, counted and kept in the denominator; **(c)**/**(d)** become **row-by-row identities against each night's `config_json` and the code at `fa70688` at relative tolerance 1e-6** (smart-money effective weight exactly 0 where the flag is off or absent; `gex_alignment` base weight exactly 0.0); **(e)** becomes a **script-correctness gate** on the mandatory 2026-06-01 catalyst split. Shares, distinct-value counts and the catalyst panel are **printed, not gated**. No target is ever relaxed | §4.1, §8 |
| 7 | Who writes `eval.py`, and who owns the standing re-run *(raised at decide)* | The **Researcher** writes it once from §4 (rule 9) **and runs the 2026-09-28 pass**; the **Data Steward** owns the **standing re-run only** — byte-identical script at every subsequent freeze and at every `sas_runs.config_json` hash change, published as `LAYER_STRUCTURE_vNNN.md` | header, §5.4, §9 |
| 8 | Determinism: seed, draw counts, environment *(raised at decide)* | Fixed RNG seed **`20260914`** for B2 (2,000 draws) and both bootstraps (2,000 resamples each); `eval.py` prints seed, draw counts and library versions in the register header; a Gate 0 re-run pass reuses the seed, and a seed change is a new pass | header, §3 B2, §4.6, §4.1 |
| 9 | DP-50 sweep at lock, and which SHA the code is read at *(raised at decide)* | **Immaterial to the population by construction** — sha256-pinned parquet frozen 2026-09-10; `2d5776c` (PI-001) touches `uoa_symbol_daily.fwd_return_*`, a table this question never reads. **Not** immaterial to the definitions: every code reference is read at **`fa70688…c324e`**, never HEAD, and the register prints that SHA beside the manifest SHA; DP-50(b) runs forward and fires §9's standing re-run, not a constraint on any brief | header, §2.4, §9, §10.11 |

**Standing rules proposed from this question** (DECISIONS.md; Haci's to confirm later, none added as a
DP here): a Gate 0 item states a number and a failure branch or it is not a gate — where the fact is
distributional, gate an identity against the point-in-time config and the frozen SHA and print the
distribution; a printed sensitivity that contradicts the primary on the same criterion makes that
criterion INCONCLUSIVE; a verdict criterion that turns on a Registrar convention must hold at the
convention **and** at the sensitivity value that works against it; a deterministic script names its
seed at lock; a diagnostic's verdict carries its scope in its own label.
