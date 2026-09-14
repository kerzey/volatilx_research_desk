# L-Q029 — historical companion protocol: which scoring layers earn their weight, admitted in-sample history

**INTERNAL / NON_QUOTABLE.** Output label fixed by this protocol: **NOT_ESTIMABLE** (feasibility, §6).
**Status:** PROTOCOL FIXED 2026-09-14, before any computation. **No parquet row was loaded, and no layer IC,
ablation contrast, touch rate or return was computed, to write this file.** Feasibility comes only from existing
Steward/FREEZE reports and manifest metadata.
**Companion of:** `research/questions/Q029_layer_value_ablation/` (PREREG_LOCKED, prereg sha256
`76f2f937…3f02`, decision date shared with Q027). This is a separate learning artefact. It is **not** an amendment
to Q029 and does not use Q029's directory.
**Governing policy:** `research/LEARNING_POLICY.md` §Historical companions; DP-52, DP-55 (principally), DP-56.
Work package: `research/learning/HISTORICAL_COMPANIONS.md` row L-Q029.
**Prepared by:** registrar (desk run 2026-09-14, learning item `LEARN-COMPANIONS`).

---

## Decision paragraph

History up to 2026-05-29 cannot rank the layers for shadow-development effort. Three reasons:

- **The engine cannot be replayed.** On the 25 pre-2026-05-18 admitted nights, the registered replay formula
  fails the ≥ 99% per-night reconstruction gate on every night. The slate replay also fails on 12 of the April
  nights.
- **The rebuildable window is too short.** The 9 nights the formula does rebuild (05-18..05-29) are far below
  the 20-night cell floor.
- **Several layers are not measurable.** The catalyst layer was a flat 80 on every admitted night. The
  fundamental layer was switched off for all of April. GEX changed from a 12-point weight to zero at the very
  boundary.

The companion is **NOT_ESTIMABLE for the current engine, and for every historical vintage**. Architecture
triage should rest on the **mechanical** facts R1b already established: smart-money is never computed, GEX
carries zero weight, and projection misses the coverage floor. It should not rest on a historical outcome
replay, and it should not rest on the earlier layer/outcome audit, which is already-explored evidence (§4). An
internal flag-off shadow ablation log is the instrument that would answer it (§11).

## 0. What this companion can never be

- It can **never** be independent confirmation of Q029, in either direction, and never a replication. The
  platform's own layer/outcome audit already covered this history (§4).
- It can **never** open, preview or approximate Q029's outcomes. Q029's verdict window is prospective (pick
  nights ≥ 2026-09-15). Its sealed post-hoc panel (2026-06-01..2026-08-12) belongs to Q029's decision pass and is
  **not admitted here**. No night after 2026-05-29 is loaded as a selection.
- No controller verdict, no p-value, no q-value, no CARRIES / HARMFUL / DECORATIVE label, no weight brief, no
  scoring change (DP-52).
- It never computes the composite IC (L-Q027) or layer redundancy (Q028).

## 1. Internal decision it supports

*"Which architectural experiments deserve shadow-development effort?"* That is, whether any layer's history
justifies prioritising a flag-off shadow ablation or re-weighting experiment ahead of Q029's decision. The only
permitted outputs are evidence-card wording for Q029 and a recommendation on shadow instrumentation (§11). Any
learned weight, cutoff or ranking rule would require a new version and a future test, never a change to Q029.

## 2. Inputs — exact whitelist

**Manifests and hashes (read from the manifest JSONs, and from controller state where the file hash is recorded there):**

| artefact | SHA-256 | role |
|---|---|---|
| `research/data/manifest_v001.json` (file) | `b03f355a68373aadd0f2dc56c9154158929642291bf6caacb2f5a9bf15bef374` (as `base_manifest_sha256` in `manifest_prices_v001.json`; controller state, e.g. `Q006_control_cohort_path/state.json`) | selections, config, score details |
| └ `sas_candidates` → `research/data/v001_sas_candidates.parquet` | `af40ad8a48915f979cf36b0cc4d6526a7e9ecfbd523351ac4d8155b7a0aaa2f2` | |
| └ `sas_runs` → `research/data/v001_sas_runs.parquet` | `888d6f3be279bacd8fa963899cbdb1e4955449861eb9668757f98bf01e9283ea` | |
| `research/data/manifest_prices_universe_v001.json` (file) | not recorded in any desk artefact as of 2026-09-14; Stage 0 computes and prints it before reading any parquet | bars: ≥ 60-session history and forward bars |
| └ `daily_split` → `research/data/pu001_daily_split.parquet` | `2e654281d480c930d312b294a6ab7035e0d59ec7ba757353760aa0d0ce6afa95` | |
| └ `daily_raw` → `research/data/pu001_daily_raw.parquet` | `b6dc92c98a1f4556d9478eee1460ddfb959920fdc575beb61f55f97f1d80d100` | split-factor snapping only |
| `research/data/manifest_prices_v001.json` (file) | `73d2a895da7db724a236ea051d81944799135f0fb5fb3f1d022659f2b0c3b655` (controller state) | cross-check only |
| └ `prices_daily_split` → `research/data/p001_daily_split.parquet` | `7270c61304c7d4ba3e6708f48fe47f21bbfbffe8a91ebf667c97b495651ff175` | agreement check on overlapping symbol-dates; fails loudly on disagreement |
| `research/data/exclusions_v003.json` | not recorded; Stage 0 prints it | night exclusions |
| platform code definitions | read-only, `git show fa70688:<path>` (Q029 header), never HEAD | formula references only |

**Why the universe price freeze.** `manifest_prices_v001` begins 2026-01-31 (41 bars before 2026-04-01), so the
≥ 60-bar row screen and `beta60` / `runup20` for the B4 match first clear on 2026-04-28.
`manifest_prices_universe_v001` starts 2025-01-02. Fixed before any outcome; not a variant.

**Columns:** `sas_candidates` (every row): `trading_date`, `symbol`, the seven `<layer>_score` columns,
`overall_score`, `completeness_score`, `cross_layer_bonus`, `conflict_penalty`, `missing_data_penalty`,
`score_details_json.weighted_dimensions` (and key presence for the schema class), `missing_data_json`,
`dominant_direction`, `best_timeframe`, `qualified`, `threshold_pass`, `selected_rank`, `qualification_reason`,
`public_payload_json.lane_plans` / `.analysis_status` (published rows, `d*_t` and the zero-lane-plan signature),
`created_at`. `sas_runs`: `trading_date`, `finished_at`, `config_json`. Bars: `symbol`, `date`, `o`, `h`, `l`, `c`.

**Never inputs:** `market_regime_daily` (not point-in-time before 2026-06-09); `sas_selection_excursion`;
`outcome_*`; `level_hit_*`; `uoa_symbol_daily.fwd_return_*`; the platform's `atr_pct` / `spot_close`; hourly bars;
the August layer audit's numbers (prior art only, §4); any selection row dated after 2026-05-29.

## 3. Admitted selection dates and loading

- **Admitted selections:** `trading_date <= 2026-05-29` (`in_sample_end`, `manifest_v001.json`). They are loaded
  **only** through `research/lib/eval_utils.py::load_split(manifest, "in_sample", name=<table>,
  date_col="trading_date")` for `sas_candidates` and `sas_runs`, before any join.
- **Night exclusions:** `exclusions_v003.json` (`manual_runs` ∪ `non_session_runs` ∪
  `uncorroborated_publication_runs`), DP-04, and the zero-lane-plan criterion (Q027 §2.4, adopted by Q029 §2.0).
- **Forward bars:** admitted only as (symbol, date) pairs inside `[t−60, t+20]` sessions of an admitted candidate
  row, for that row's symbol, plus SPY for `tape_t`. Nothing beyond t+20 (the last admitted t+20 is 2026-06-29), and
  no bar joined to a later selection.
- **Metadata before bars:** the vintage census, Gate 0, slate replay and layer coverage (Stage 0) use no bar at all.

## 4. Prior exposure to this history (frozen does not mean untouched)

| source | what it read on the admitted window | consequence |
|---|---|---|
| platform August layer audit, `volatilx:docs/SAS_SCORING_RESEARCH_PLAN.md:53-67` (read by the registrar when drafting Q029, quoted in Q029 §6) | per-layer "corr vs hit" / "corr vs favorable" with a verdict per layer, on n = 635 decidable published picks (5,868 candidate rows for the smart-money line). Its population spans the platform's historical cohort, which includes the admitted April–May nights | **H-075's own statistic has already been computed on this history.** Any companion estimate is a re-read, never evidence independent of it. Its range-restriction caveat applies |
| `research/reports/STEWARD_Q029_feasibility.md` (R1b) | counts only on the whole freeze from 2026-04-01: layer coverage per month, weight census, Gate-0 reconstruction, slate replay, near-miss pool | mechanical facts about the admitted window are known (§5, §6); no outcomes |
| `research/reports/weekly/2026-09-10.md`, `2026-09-12.md` | published-pick returns from 2026-04-01 by **source membership** and band | layer-adjacent outcome reads exist |
| `research/reports/explore/EXPLORE_001.md` | in-sample published picks and a matched unpublished pool on the path lens | the E3 control construction's in-sample paths are explored |
| `research/questions/Q028_layer_signal_independence/` (pinned, outcome-free, not yet run) | none yet | no exposure; L-Q029 does not compute redundancy |

## 5. Engine versions in the admitted window, and the vintage rule

**Vintage rule (fixed):** a cell is a set of admitted nights sharing one `sas_runs.config_json` tuple
(`scoring_weights`, `timeframe_weight_multipliers`, enrichment flags, presence/values of `atr_elite_*`,
`publication_floor`, `bear_publish_threshold`, `max_output_cap`, `min_completeness`) and one `score_details_json`
schema class. Cells are never pooled. **The reconstruction formula is Q029 §2.4's, at `fa70688`, unchanged.** A
vintage-specific formula (for example, dropping the GEX offset for partial-schema rows) would be a new formula
written after the Steward inspected residuals. It is **not admitted** (HISTORICAL_COMPANIONS: an unreconstructible
engine gives NOT_ESTIMABLE, not a favourable subset). It is recorded here as a rejected design, not a variant,
because nothing was computed.

| boundary (source) | effect inside the admitted window |
|---|---|
| partial 8-key `score_details_json` (no `atr_elite_block_applied`, no GEX-offset fields) for rows ≤ 2026-05-08; full schema from 2026-05-11 (R1b §(d)) | the registered Gate-0 formula leaves a +5.00 residual on non-reconstructing partial-schema rows; an undiagnosed −7.00 tail sits in the same era; **every one of the 25 pre-v1.5 admitted nights is below 99% reconstruction** (25 of 102 whole-freeze nights below 99% = the 20 + 5 nights of V-A + V-B) |
| v1.5 weight reallocation 20/26/8/12 → 27/29/10/0 plus ATR-elite cap, first clean night 2026-05-18 (R1b §(c), §(f)) | GEX is a **REMOVAL** layer at weight 12 before, and an **ADDITION** layer after: two different tests (Q029 §2.3's direction rule), never pooled |
| fundamental enrichment off all April and on 2026-05-04; on 05-01 and 05-05 onward (R1b §(b)) | fundamental non-null share 0.00% in April (R1b §(a)): no fundamental endpoint in V-A |
| catalyst flat 80 before 2026-06-01 (DATA_NOTES `69ef05f`); zero within-night variance on 34 of 102 whole-freeze nights while every segment night varies, i.e. **every admitted night** (R1b §(a)) | catalyst fails the non-zero-variance clause on every admitted night: no catalyst endpoint anywhere in the window |
| layer coverage by month (R1b §(a)): April GEX 38.07%, projection 49.44%; May GEX 76.95%, projection 56.03%, fundamental 92.58% | projection fails the 70% rule in every month; GEX fails in April |
| smart-money 0.00% non-null, flag False on all nights (R1b) | DEAD everywhere |
| single combined bull/bear counter before 2026-07-02; replay disagrees > 1% on **12 April nights** (R1b §(e)) | E3's slate replay is not the platform's selection on those nights |
| `publication_floor` absent until 2026-07-08; `bear_publish_threshold` absent until 2026-06-29 | a replay honouring the night's own config (Q029 §2.5) replays a different publication gate from today's |
| ladders non-monotonic before 2026-07-06; `d*_t` cohort shift at 2026-07-08 (1.06 → 2.10 ATR median, STEWARD_Q027 §(c)) | the target distance comes from a different cohort |
| regime labels backfilled ≤ 2026-06-08 | `tape_t` only |
| `uoa_symbol_daily.fwd_return_*` freeze from 2026-05-20 | not an input; no split |

**Current engine** for this question: the `fa70688` formula, the 2026-05-18 weight vector with GEX as an addition
test, post-06-01 catalyst, fundamental enrichment on, split lanes, `publication_floor` = 80. That is, nights
≥ 2026-07-08.

## 6. Feasibility — counts and metadata only (no outcomes)

| step | nights |
|---|---:|
| trading sessions 2026-04-01..2026-05-29 | 41 |
| minus `manual_runs` in window (04-02, 04-24, 05-11..05-15) | **34** |
| **V-A** pre-v1.5, GEX 12 (REMOVAL), fundamental off, partial schema: the 19 April nights + 05-04 | 20 |
| **V-B** pre-v1.5, GEX 12, fundamental on, partial schema: 05-01, 05-05..05-08 | 5 |
| **V-C** 2026-05-18 formula (GEX ADDITION), ATR-elite cap, full schema: 05-18..05-29 | 9 |
| minus zero-lane-plan nights (04-01 → V-A; 05-01 → V-B) | V-A **19**, V-B **4**, V-C **9** |
| **E3 (ablation):** nights passing Gate 0 (≥ 99% per night under the registered formula) | V-A 0, V-B 0, V-C 9 |
| **E3:** of those, slate replay within 1% | V-C 9 (the replay failures are April) |
| **E1 (marginal IC):** layers meeting the coverage rule in the cell's month | V-A: flow, technical only (19 nights); V-C: at most flow, technical, GEX, fundamental (9 nights; May-level coverage, not cell-level) |
| **E2 (partial IC):** needs ≥ 3 other retained layers | V-A: 2 retained layers, so **undefined by construction**; V-C: at most 4 retained (9 nights) |
| catalyst endpoints | none on any admitted night (zero within-night variance) |
| nights produced by the **current engine** | **0** |
| maturity (last t+20 = 2026-06-29) | all mature |

**Estimability threshold (fixed):** ≥ 20 contributing nights in one vintage cell, per endpoint (rule-6 per-cell
floor). No pooling across cells, and no pooling of GEX's REMOVAL and ADDITION sides.

**Verdict: NOT_ESTIMABLE — for the current engine (0 admitted nights) and for every historical vintage.** E3
reaches 9 nights at most (V-C), because the registered replay does not reconstruct the pre-v1.5 engine. E1 reaches
19 nights at most, for two layers only, on a retired formula. E2 is undefined on V-A and 9 nights at most on V-C.
Catalyst is flat everywhere.

**Stage 0 (optional, counts only):** re-derive the vintage census, per-night Gate-0 rate, replay disagreement and
per-cell layer coverage from whitelisted metadata, with no bar loaded, printing the computed hashes. If it
disagrees with this table, it stops and the disagreement is recorded in `REPORT.md`; this protocol is not edited.
**Stage 1 runs only if Stage 0 finds, for some endpoint and layer, a cell with ≥ 20 contributing-eligible nights**,
and is not expected to run.

## 7. Comparison, endpoint, entry and target distance (fixed; applies only if Stage 1 runs)

Adopted from Q029 PREREG §2.3–§4.1 (itself adopting Q027 §2.1–§2.5), **restricted to one vintage cell and to the
layer/endpoint pairs Stage 0 finds evaluable there**:

- **Population and publication predicate:** every scored candidate; published = `qualified IS TRUE AND
  selected_rank IS NOT NULL` (DP-28); `d*_t` and the split-scale screen as in Q027 §2.2 / §2.4, with the
  trailing fallback taken within the same cell.
- **Entry:** t+1 open; synthetic target at `d*_t` ATR; 20-session clock; already through at entry = not a hit; no stop.
- **E1ⱼ:** per-night Spearman ρ(subscoreⱼ, path rank). **E2ⱼ:** partial rank correlation given the other retained
  layers. **E3ⱼ:** `ΔE*_{t,j}`, the ablated minus production within-night control-adjusted L3-touch rate. Controls are
  the 10 nearest same-night candidates on `beta60` / `atr_pct` / `runup20` in neither slate. The B3 near-miss placebo
  is subtracted. The replay uses the night's own config literally, with an absent key meaning an absent gate.
- **Scale reference:** `mom20` IC on identical rows (Q029 §3 B6).
- **Missingness:** Gate-0 failures, replay failures, coverage failures, ungradeable rows and thin control pools are
  counted by reason, never back-filled, never imputed.
- **Feature knowledge time:** subscores, weights, config and payload come from 16:05 ET rows; distances, matches and
  `tape_t` from bars ≤ t. Every ablated slate and match is frozen before any forward bar is read.
- **Not computed:** the fuller "layer removed everywhere" sensitivity, the GEX weight curve, and added-minus-dropped
  decomposition beyond its count. Adding any of them is a variant (§10).

## 8. Uncertainty and dependence (fixed)

Descriptive 95% intervals only. (i) Date-clustered bootstrap over contributing nights, with a stationary block
bootstrap (expected block length 10) beside it. (ii) Episode × night bootstrap (DP-51; for E3, episodes on the union
of the two slates). Both use 2,000 resamples, seed `20260909` (`eval_utils.SEED`); B3 placebo uses 2,000 draws per
night per layer, never adding to n. Dependence assumed: overlapping 20-session windows on consecutive nights, a
shared market factor within night, symbol recurrence, and near-identical production and ablated slates within a night
(the E3 contrast rests on discordant picks only). **No p-value, no q-value, no verdict language**, and no reading of
the audit's correlations as a prior or a comparison.

## 9. Output label, report form, permitted use, review

- **Label:** `NOT_ESTIMABLE` (current engine and all vintages). A card citing it uses MECHANICAL, because the
  finding is a reconstruction/coverage fact. Any hypothetical Stage-1 output would be labelled
  `EXPLORATORY — RETIRED ENGINE VINTAGE <cell>`.
- **Report:** `research/learning/L-Q029/REPORT.md`, due by 2026-09-28. It leads with the decision paragraph, and
  never uses `research/questions/Q029_*/results/`.
- **Permitted internal use:** Q029 evidence-card wording; architecture triage from the mechanical R1b facts only; the
  shadow-instrumentation recommendation in §11.
- **Review of interpretation:** the Red Team reads `REPORT.md` before any card cites it.

## 10. Variants register

Every analysis variant examined is recorded here with date, change, reason and whether it was chosen before or
after any outcome was seen. **Empty as of 2026-09-14.** (The rejected vintage-specific reconstruction formula in §5
is a design decision taken without computation, not a variant.)

| id | date | variant | reason | before/after outcomes | where reported |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 11. What would resolve the question instead

- **Q029's prospective window** (pick nights 2026-09-15..2027-03-05, shared with Q027), unchanged.
- **An internal flag-off shadow ablation log** is the instrument that answers "which experiment deserves effort"
  without history. Scope: each night, persist the production bull slate and the per-layer leave-one-out slates
  computed by the platform's own `_qualify_lane` on the stored `weighted_dimensions`. Metrics: the slate-change share
  `k_{t,j}` per layer (mechanical, outcome-free, useful immediately) and, only after maturity, path outcomes under a
  separately registered protocol. It must be versioned against the scoring SHA, with a rollback of "disable the
  flag". It may be proposed through the enhancement channel. It cannot feed Q029's verdict or change its population.
- **Mechanical triage available now, without outcomes** (R1b): smart-money is never computed; GEX is computed but
  carries zero weight; projection, the largest weight, fails the 70% coverage floor in every month; catalyst moves
  the segment slate on 32.4% of nights. These are coverage facts, not evidence that any layer helps or hurts.
