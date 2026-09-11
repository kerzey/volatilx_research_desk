# Q005 — Researcher run log (for red-team)

## Part A — written BEFORE the first run of eval.py (no result had been computed)

### Gate check (2026-09-11)
- `controller.py show Q005` -> state `DATASET_PINNED`; prereg_commit c52fa16; prereg_sha256 8347b498…cd7bc
  matches the file on disk; `git diff --quiet HEAD -- PREREG.md` exit 0.
- PREREG last committed c52fa16 (2026-09-10 23:19 -0500); manifests committed earlier
  (manifest_v001 fb33378 18:49, manifest_prices_v001 ab77b9a 21:07). PREREG unchanged since.
- `freeze_dataset.py --verify` OK for all 11 tables (manifest_v001) and 3 tables (manifest_prices_v001);
  manifest file SHA-256s match controller `manifests` record. exclusions_v001.json committed, clean.
- Cosmetic: PREREG header line still reads "Status: DRAFT (lock by committing…)"; the lock is recorded by the
  controller (PREREG_LOCKED by haci), the file bytes are the locked bytes. Not a blocker.

### Structural facts checked before writing eval.py (no elite counts or trends looked at)
- `overall_score` is reproducible from `score_details_json` (per-row effective weights, subscores,
  bonus/penalties, `gex_missing_offset_value`, ATR block, `industry_rotation_bonus`) for 6,462/6,479 rows to
  <0.01. The 17 exceptions are all on 2026-06-26 (P0): recorded `overall_score` is a 1-decimal value that
  differs from the internal pre/post-block score (an override not visible in the scoring arithmetic).
  All P1 rows (Jul–Sep) reconstruct exactly.
- `industry_rotation_bonus` (sector breadth bonus, platform 139f87d 2026-05-02, removed 66cb63d 2026-05-14)
  is added after the ATR block and clamped; present on 309 rows (P0 only).
- Every Apr–May candidate row has `updated_at` = 2026-06-01 (the 69ef05f catalyst fix). The commit message
  says the historical `catalyst_event_score=80` was "left intact for audit" and the backfill wrote the new
  `*_corrected` earnings columns; the frozen Apr–May catalyst scores are indeed a flat 80. eval.py does not
  read any `*_corrected` column. Scoring columns are treated as point-in-time.
- `industry` is populated for ~4% of candidate rows in the frozen table (DATA_NOTES says ~12%).
- `market_regime_snapshot` date field = `effective_for_trading_date` (t+1); the `market_regime_daily` row used
  on night t is the one with `trading_date = asof_close_date = t`. Stratification joins on trading_date = t,
  v1.2, t >= 2026-06-09 only.
- smart_money_confirmation_score is null on every row (weight forced 0 by config).

### Ambiguities and the reading chosen (fixed before any number was produced)
A1  Nights. PREREG says "5 manual-run nights … ≈108 nights". exclusions_v001.json (same commit as the
    PREREG) also lists `non_session_runs` = 2026-04-03 (Good Friday, no SPY bar), and DATA_NOTES' rule is
    "derive trading nights from the price freeze's SPY bars … fail loudly on a run dated on a non-session day".
    Chosen: nights = sas_runs dates ∩ SPY sessions − manual_runs (=> 04-03 dropped as a non-trading night,
    107 nights expected). eval.py raises if a run falls on a non-session day that is not listed. A Gate-0
    sensitivity with 04-03 retained is printed (informational only, not used by the verdict).
A2  Gate 0 p-values. PREREG names a Poisson trend regression and an exact Poisson rate test; CLAUDE.md rule 6
    says p-values come from permutation tests. Chosen: the PREREG statistics (Poisson-GLM slope on calendar
    days; P1−P0 difference in mean nightly count) with null distributions from permuting nights (10,000
    permutations, seed 20260909), two-sided, decline direction required. Model-based Wald, Pearson-scaled
    (quasi-Poisson) and exact conditional-binomial p-values are printed next to them; any disagreement in
    the gate outcome between the permutation and model-based versions is flagged in run_summary.
A3  Gate 0 decision = "fall is real" if (trend slope < 0 and p_trend ≤ 0.05) OR (P1 rate < P0 rate and
    p_rate ≤ 0.05), i.e. NULL only if both fail, as §8 says. The single Gate-0 p entering BH is
    p_gate = min(p_trend, p_rate). F2 has exactly one registered question reporting a formal test, so BH
    runs over m = 1 and q = p. A within-gate BH over the two components is printed as information.
A4  Poisson regression: count on calendar days since 2026-04-01, no exposure offset (the PREREG regresses the
    count, and Channel 1 handles N_t). Elite = overall_score ≥ 90 (primary: all candidates).
A5  Channel 1: CF = Σ_{t∈P1} N̄_P0 × (Elite_t / N_t) (per-night form of the §4 identity).
A6  Quantile mapping ("the deterministic map that sends P1's empirical quantiles to P0's"): period-pooled
    distributions; P1 values ranked with ties broken by a seeded random key; u = (rank+0.5)/n1; mapped value =
    P0 inverted-CDF quantile at u. Random tie-breaking is required so binary/categorical components (GEX
    offset, ATR cap, best_timeframe) and mass points (flat-80 catalyst, zero penalties) can actually take on
    P0's distribution; a pure value→value map cannot change a binary's rate. Point estimates average 25
    tie-break draws (seed 20260911); each bootstrap replicate uses one draw. Layer scores: only non-null P1
    values are mapped, onto P0's non-null values (layer availability is held at P1's observed state).
A7  completeness_score does not enter overall_score (scoring.py:1347-1348 computes it from the weights;
    overall uses base_score). Its restored share is therefore 0 by construction; it is printed in the table
    with that flag, together with its P0/P1 distribution.
A8  best_timeframe mix: ordinal categorical short<swing<long, mapped as in A6; a remapped row's effective
    weights are rescaled by the night's own config multiplier ratio m[new_tf]/m[old_tf] per layer (zeroed
    layers stay zero). Conflict penalty (which also depends on timeframe) is held at its observed value.
A9  +5 GEX-missingness offset: the additive term itself (recorded `gex_missing_offset_value`, 0 where the key
    is absent because the offset did not exist yet) is mapped as a binary. The GEX layer's inclusion in
    base_score is not toggled. Firing rate is also printed by the PREREG's definition (share of rows with null
    gex_alignment_score).
A10 ATR-elite cap: the recorded binding-block indicator (`atr_elite_block_applied`) is mapped as a binary; a
    row mapped to "blocked" is capped at its direction's cap (84.9 bull/mixed, 79.9 bear) if above it; a row
    mapped to "unblocked" gets its uncapped score. For every other component the block rule is recomputed
    from the counterfactual subscores (is_atr_only ∧ night flag ∧ <2 of flow/technical/smart-money/catalyst
    ≥ 65), and the ATR projection cap (35) is re-applied to atr-only rows, i.e. "the same arithmetic".
    The recomputed rule is checked against the recorded flag and the mismatch count printed.
A11 Rows whose recorded score is not reproduced by the arithmetic (17 rows, 2026-06-26) keep their residual:
    CF score = f(CF components) + (observed − f(observed components)).
A12 industry_rotation_bonus is not one of the 14 registered components; it is held at its observed value.
A13 Channel 3a. "Config change": any value difference in the flattened config_json between consecutive
    non-excluded nights, ignoring `audit_output_dir` (a path) and `market_regime` (a runtime input, not a
    setting). Keys added with boolean False are logged but treated as non-behavioural; any other
    added/removed/changed weight, multiplier, numeric threshold/parameter or flag counts.
    "Effective date brackets the fall": with d = first night on the new config, (i) ≥ 20 non-excluded nights
    on each side of d within the window, and (ii) mean nightly elite-candidate count on nights ≥ d is below
    that on nights < d with two-sided night-permutation p ≤ 0.05 (exact Poisson printed alongside). A local
    step (20 nights before vs 20 after d) is printed as a descriptive diagnostic only. If any change
    qualifies, the verdict is HISTORICALLY_CONFIRMED — configuration and the distributional channels are
    reported as secondary (still computed, with their own would-be label).
A14 Nesting. Channels 3 and 4 explain inside Channel 2 (§4). For the "exactly one EXPLAINS" count, Channel 2
    counts as a separate cause only if no nested item (a Channel-3 component or Channel 4) is labelled
    EXPLAINS; otherwise the nested item is the named cause. Count set = {Ch1, Ch4, each Ch3 component}
    + Ch2 if nothing nested explains.
A15 "Sum of all CONTRIBUTES/EXPLAINS shares reconstructs < 50% of S" is evaluated on the two exhaustive
    top-level channels {Ch1, Ch2} (summing nested items with their container would double count).
A16 Month panel stability: P1 months are Jul, Aug, Sep(1–10). A month with < 20 nights is SUPPRESSED (rule 6)
    and cannot count as "holding"; a month with S_m ≤ 0 cannot count either. "Holds" = restored share ≥ 20%.
A17 In-sample/sealed cut: re-run the decomposition with reference = nights ≤ 2026-05-29 and comparison =
    nights ≥ 2026-06-01; "holds across the cut" = restored share ≥ 20% there as well.
A18 Catalyst: the label used in the verdict is the weaker of the full-P0 and June-only-P0 versions. The
    greedy table uses the full-P0 version (same basis as every other component); the June-only row is
    printed separately.
A19 Greedy cumulative: order = Channel-3 marginal restored share, largest first (point estimate, ties by
    PREREG list order), applied cumulatively; "top component" of the greedy table = largest incremental
    share. The order is held fixed inside the bootstrap.
A20 Channel 4: direction has three values in the data (bullish/bearish/mixed), all kept. Terciles are pooled
    over P0∪P1 candidate rows. Primary counterfactual = reweight P1 rows to P0's joint (price tercile ×
    dollar-volume tercile × direction) cell shares (post-stratification, i.e. raking with the joint table as
    the margin); IPF raking on the three one-way margins is printed as a secondary line. Rows without price
    stats keep weight 1. Price level uses prices_daily_split (the PREREG's named table), so a symbol that
    split later is shown at its split-adjusted level. Dollar volume = 20-session mean of c×v; trailing
    return = c_t / c_{t−20} − 1; realized vol = stdev of 20 daily log returns × √252; bars dated ≤ t.
A21 Bootstrap: 2,000 replicates resampling nights with replacement within P0 and within P1 separately
    (seed 20260909). eval_utils.cluster_bootstrap_ci is used for every nightly rate; the restored shares
    are ratios of whole-pipeline statistics that eval_utils does not cover, so a stratified night bootstrap
    is implemented in eval.py with the same seed convention. Replicates with S ≤ 0 are dropped from share
    CIs and counted. A share whose CI has lo ≤ 0 and hi ≥ 100% is flagged UNINFORMATIVE.
A22 SPY tape stratum: sign of SPY's trailing 20-session return on the night (up/down); no data-derived cut.
A23 Elite-published (secondary target): monthly counts, Gate-0 statistics, its own shortfall, the DATA_NOTES
    raw series, and the publication conversion (elite candidates → published) per period. The channel
    decomposition is run on elite-candidate only (primary per §2).
A24 run_summary.json keys required by the desk: mean_oos := P1 − P0 difference in mean nightly
    elite-candidate count (the fall per night, NON_QUOTABLE); ci := its stratified bootstrap 95% CI;
    p_perm := p_gate; mpe := null (PREREG §8: no MPE applies).

## Part B — run log (appended after running)

### Run
- Single run 2026-09-11T05:19:36Z: `python research/questions/Q005_elite_thinning/eval.py`
  -> exit 0, 88 s, stderr empty. stdout saved as results/run_20260911T051936Z.json (identical to
  run_summary.json). No re-run, no post-run code change.
- Before that single run (nothing had executed yet) five defects found on review were fixed in eval.py:
  snapshot-label NaN fallback; groupby created before columns were added (price stats); datetime
  resolution alignment for merge_asof; one JSON object on stdout instead of two; a component with an empty
  reference set returns NaN instead of 0 (affects only the catalyst June-only row under the in-sample cut).
  None changes the specification.
- Night count 107 (P0 58, P1 49; in-sample 37, sealed 70). Excluded 6: 5 manual-run + 2026-04-03
  (non-session). No SPY session in the window lacks a run. Candidate rows 6,211.
- Gate 0 sensitivity keeping 04-03 (A1): fall_is_real = True (p_trend 0.0245, p_rate 0.0197); same outcome.
- Permutation and model-based gate outcomes agree (both "fall is real").

### Flags for red-team (observed in the output; the specification was NOT changed)
F1  Channel 3a decided the verdict. The four changes flagged as "bracketing the fall" under reading A13 are:
    06-29 `bear_publish_threshold` 80 / `bear_max_output_cap` 5 added (publication gates, cannot move
    overall_score); 07-02 `enable_fundamental_enrichment`/`enable_synthesis`/`enable_multi_agent_reports`
    true->false for ONE night (07-03 holiday, 07-06 excluded), reverted 07-07 (the revert also "brackets");
    07-08 `publication_floor` 80 added (publication gate). The one change that does move scores for many
    nights — 05-15 (weights projection 26->29, technical 20->27, GEX 12->0, catalyst 8->10; ATR block and
    projection cap added) — did NOT qualify (0.556 -> 0.325 elite/night, p_perm 0.062). With dates close to the
    07-01 cut, A13's global before/after test is nearly the same as Gate 0's rate test, so it tends to fire
    on any change dated near the cut. Red-team must decide whether A13 is an acceptable reading of
    "brackets the fall". If it is not, the verdict falls back to the distributional reading eval.py already
    printed: INCONCLUSIVE (marginal top = projection_score, greedy top = flow_strength_score). Logged as
    BACKLOG H-014; no re-specification was run.
F2  GEX offset (A9): the recorded offset fired on 0.5% of P0 rows and 1.2% of P1 rows. By the PREREG's stated
    definition (null gex_alignment_score) the rates are 31.1% (P0) and 1.2% (P1): the offset code did not
    exist in April, so April's null-GEX rows never received +5. eval.py used the recorded offset (the real
    arithmetic). Under the PREREG definition this component would be mapped differently. Both rates are in
    channel3_component_distributions.csv.
F3  On 2026-06-26 (P0), 17 rows have a `technical_structure_score` column value that differs from the
    `score_details_json` subscore. These are the same 17 rows whose recorded overall_score is not
    reproduced; none is elite. eval.py used the JSON subscores (A11 residual add-back), so the P0 technical
    reference distribution includes JSON values for these 17 of 3,139 rows, where the PREREG names the
    column.
F4  Every elite candidate in both periods was published (29/29 in P0, 12/12 in P1), so the secondary target
    (elite-published) is numerically identical to the primary.
F5  The ATR-elite block never bound in the frozen data (0 rows at 84.9/79.9; rule recompute agrees, 0
    mismatches), so the atr_elite_cap component is inert (0%).
F6  Greedy-top reading (A19). If "top of the greedy table" were read as its first row (by construction the
    same as the marginal top), the disagreement check could never fire. The distributional reading would then
    rest on the remaining rules: Channel 2 is the only EXPLAINS item (128%, CI 118.9%–195.2%; Jul 143%,
    Aug 120%; in-sample/sealed cut 122.5%). This is stated for completeness only; eval.py applied A19.
F7  Channel 2 restores more than 100% because P1 has more candidates per night than P0 (62.7 vs 54.1), so
    Channel 1's share is negative (−10.8%). Channels 1 and 2 are not additive shares of S.
