# Q005 — elite_thinning: why does SAS publish fewer 90+ picks every month?

**Status:** DRAFT (lock by committing this file after Haci review)
**Family:** F2 Calibration (product-intelligence item PI-010)
**Type:** **DIAGNOSTIC / decomposition.** This question does not test an edge and has no MPE in the
usual sense; it apportions a known decline. **Every number it produces is `NON_QUOTABLE`** (rule 12):
it informs a product decision, not a subscriber claim.
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — used only for the universe/liquidity descriptors in Channel 4 and the SPY tape stratum; **no forward bars and no outcome is used anywhere in this question.**
**Exclusions:** research/data/exclusions_v001.json (`manual_runs.trading_dates`, 5 nights)
**Registered by:** registrar · **Approved by:** haci · **Date:** 2026-09-10

---

## 1. Hypothesis (plain English)

**SAS is publishing fewer and fewer elite (90+) picks — 8 in April, 13 in May, 12 in June, 8 in
July, 3 in August, 2 in the first week of September. This question asks which of four things caused
it: fewer candidates, a general slide in scores, one specific scoring layer falling, or a change in
the kind of stocks reaching the engine at all.**

There is no directional claim to confirm. The pre-registered object is a **decomposition with a
fixed arithmetic and a fixed attribution rule**, written before anyone looks at which layer moved.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Nightly counts and nightly score distributions
  are the observations; candidate rows are aggregated within a night first.
- Source tables (manifest_v001):
  - `sas_candidates` — **every candidate, published or not**: `overall_score`,
    `completeness_score`, `qualified`, `threshold_pass`, `qualification_reason`, `selected_rank`,
    `dominant_direction`, `best_timeframe`, `confidence_level`, the seven layer subscores
    (`flow_strength_score`, `technical_structure_score`, `gex_alignment_score`, `projection_score`,
    `fundamental_quality_score`, `catalyst_event_score`, `smart_money_confirmation_score`),
    `cross_layer_bonus`, `conflict_penalty`, `missing_data_penalty`, `source_membership_json`,
    `score_details_json`, `missing_data_json`, `context_json`, `industry`.
  - `sas_runs` — `config_json` per night (the point-in-time configuration: weights, timeframe
    multipliers, thresholds, feature flags) and `stats_json`.
- Source tables (manifest_prices_v001): `prices_daily_split` only, for Channel 4 descriptors
  (price level, dollar volume, trailing 20-session return and realized vol of each candidate at the
  pick night) and for the SPY tape stratum. Trailing bars only.
- **Filters:** trading_date 2026-04-01 .. 2026-09-10; non-excluded nights only (the 5 manual-run
  nights from `exclusions_v001.json` are dropped and counted, because their candidate context is
  mixed-date); all candidate rows kept regardless of `qualified` or `threshold_pass`.
- **Elite is defined twice, and both are reported:**
  - **Elite-candidate:** `overall_score ≥ 90`, published or not. This is the **primary** target of
    the decomposition, because it has thousands of rows behind it and isolates *scoring* from the
    publication cap.
  - **Elite-published:** `overall_score ≥ 90` **and** `selected_rank` not null. This is the number
    Haci sees (8/13/12/8/3/2) and is the secondary target.
- No outcome column is read. `outcome_*`, `sas_excursion.*`, `level_hit_*` and
  `uoa_symbol_daily.fwd_return_*` are **not joined** in this question at all.

## 3. Baseline — what the comparison is against

- **Reference period P0:** non-excluded nights **2026-04-01 .. 2026-06-30** (≈ 57 nights).
- **Comparison period P1:** non-excluded nights **2026-07-01 .. 2026-09-10** (≈ 49 nights).
- The baseline is **P0's own elite rate applied to P1's nights**: the expected elite count in P1 had
  nothing changed. The **shortfall** `S = E[elite | P0 rate] − observed elite in P1` is the quantity
  every channel is scored against.
- A **month-by-month panel** (Apr, May, Jun, Jul, Aug, Sep-to-10th) is reported alongside the
  two-period split, so the attribution is not an artefact of where the cut falls. The cut date
  2026-07-01 is fixed here, before any look.

## 4. Objective metric — the decomposition (this replaces the template's return objective;
rule 5's path objective does not apply because no outcome is measured)

**Gate 0 — is the fall real?** Poisson regression of the nightly elite-candidate count on calendar
time (and, separately, an exact Poisson rate test of P1 vs P0). **If the decline is not
distinguishable from constant-rate noise at p ≤ 0.05, the decomposition is not run and the answer is
"there is nothing to explain"** (see §8). This gate exists because 3 and 2 are small numbers.

**The identity being decomposed.** Nightly elite-candidate count
`Elite_t = N_t × P(score ≥ 90 | candidate, night t)`, where `N_t` is the candidate count.
Scores themselves come from
`overall_score = clamp(base_score + cross_layer_bonus − conflict_penalty − missing_penalty +
gex_missing_offset)`, then a possible ATR-elite cap, per volatilx
`services/super_agent_select_scoring.py:1347-1348` (base/completeness), `:1364-1368` (missing
penalty), `:1379-1399` (the +5 GEX-missingness offset and the clamp), `:1401-1423` (the ATR-only
Elite block: bull cap 84.9 / bear cap 79.9 — a mechanical way to make 90+ impossible),
`:1316-1322` and `:682-722` (effective weights = base weights × timeframe multipliers, with a layer
zeroed when its context is absent).

**Four channels, each scored by the same counterfactual rule.** For each channel, recompute P1's
elite count after substituting **only that channel's P1 distribution with P0's**, holding everything
else at P1's observed values; then
`restored_share = (counterfactual elite count in P1 − observed elite count in P1) / S`.

- **Channel 1 — candidate count.** Hold P1's per-candidate score distribution fixed; set `N_t` to
  P0's mean. Answers "is the engine simply seeing fewer names?" Also reported: `N_t` by source
  (`source_membership_json` — UOA day/swing/long, whale, projection bull/bear).
- **Channel 2 — score-distribution shift.** Hold `N_t` at P1's value; replace P1's `overall_score`
  distribution with P0's, by **quantile mapping** (the deterministic map that sends P1's empirical
  quantiles to P0's). Reports the shift at the 50th / 90th / 95th / 99th percentile and the fraction
  of the shortfall it carries. Channels 1 and 2 are exhaustive by construction; Channels 3 and 4
  explain *inside* Channel 2.
- **Channel 3 — layer-level shift (the main event).** For each score component in turn —
  `projection_score`, `technical_structure_score`, `flow_strength_score`, `catalyst_event_score`,
  `fundamental_quality_score`, `gex_alignment_score`, `smart_money_confirmation_score`,
  `cross_layer_bonus`, `conflict_penalty`, `missing_data_penalty`, the **+5 GEX-missingness offset**
  (firing rate = share of rows with a null `gex_alignment_score`), `completeness_score`, the
  **best_timeframe mix** (which changes effective weights), and the **ATR-elite cap** (share of rows
  at exactly 84.9 / 79.9) — quantile-map that component's P1 distribution back to P0's, recompute
  `overall_score` with the same arithmetic and the same night's `config_json` weights, and report
  the restored share. Components are scored **one at a time** (marginal) **and** in a greedy
  cumulative order (largest first), and both tables are printed; the gap between them is the
  interaction term.
  - The **catalyst layer must be reported separately from every other layer** and with a standing
    caveat: it is a *different feature* before and after 2026-06-01 (bogus market-wide earnings
    resolver; platform commit 69ef05f; `exclusions_v001.json.catalyst_layer_regime_change`;
    DATA_NOTES). P0 straddles that boundary, so Channel 3's catalyst row is additionally computed
    with P0 restricted to 2026-06-01..06-30 and both versions printed. A catalyst result that only
    appears in the straddling version is an artefact of the fix, not a finding.
  - **Config changes are checked first, not modelled:** the distinct `config_json` hashes per night
    are listed with their date ranges. If weights, timeframe multipliers, `min_completeness`,
    thresholds or the ATR-elite-block flag changed mid-sample, that is a **discrete cause** and is
    reported as Channel 3a ahead of any distributional story.
- **Channel 4 — universe / composition change.** Symbol turnover between P0 and P1 (share of P1
  candidate-nights whose symbol never appeared in P0); the distribution of candidate price level,
  dollar volume, trailing 20-session return and trailing realized vol (from `prices_daily_split`);
  direction mix (bull/bear); `best_timeframe` mix; and sector, **with the standing caveat that
  `industry` is populated for ~12% of candidates (DATA_NOTES), so the sector cut is reported as
  "populated subset only" and never as a sector explanation of the whole**. Counterfactual: reweight
  P1 candidates to P0's joint distribution of (price-level tercile × dollar-volume tercile ×
  direction), by raking, and recompute the elite count.

**Everything in this question is descriptive.** No touch rate, no return, no excursion.

**Inference.** Night-level. CIs for every rate and every restored share: date-clustered bootstrap
over nights, 2,000 resamples, resampling **nights** (not candidate rows). The elite counts are small,
so every restored share is printed **with its CI**, and a share whose CI spans the whole
0–100% range is reported as uninformative rather than as a number.

## 5. Sample floors and expected n

- Floors (rule 6): **≥ 20 nights per cell, ≥ 80 nights total.** No maturity requirement — nothing
  forward-looking is measured — so **the floors are met today**.
- Expected n: **≈ 108 non-excluded nights** total (113 raw, 5 manual-run exclusions);
  **P0 ≈ 57 nights, P1 ≈ 49 nights**; both clear the 20-night cell floor. Candidate rows: 6,479 in
  the frozen table across all nights, of which the elite-candidate subset is the small one.
- **Elite counts are the small numbers here**: 33 published elite in P0 and 13 in P1 (from
  DATA_NOTES' monthly series, before the manual-run exclusion, which removes 4 in-sample elites on
  2026-05-11..14 — so the corrected P0 count is lower and `eval.py` must print its own derivation).
  This is why the **elite-candidate** definition is primary and why Gate 0 exists.
- **Decision date: 2026-09-15** (as soon as the file is locked and the Researcher has written
  `eval.py`). No waiting period: the data is already mature. One pass, no interim looks (rule 9).
- No successor freeze is needed. This question is answered entirely from `manifest_v001`.

## 6. Test window, split and stratification

- **Test window: all 108 non-excluded nights (2026-04-01 .. 2026-09-10), April–May included.**
  *Justification (one sentence):* EXPLORE_001 examined price paths, entry timing and volatility — it
  did not analyse score composition, candidate counts or layer distributions, so no threshold or cut
  in this question is data-derived from the exploration; the only figures that shaped it are the
  monthly elite counts, which were already in DATA_NOTES before the exploration ran.
- **Calendar split:** the in-sample / sealed boundary `in_sample_end = 2026-05-29` (both manifests)
  is reported as a third cut alongside P0/P1 and the month panel. A channel that explains the fall
  only on one side of one cut is labelled unstable and cannot reach CONFIRMED (§8).
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` is knowledge-time-legal only from **2026-06-09**, `regime_version = 'v1.2'`
    (manifest_v001 `availability.market_regime`; the whole 2026-01-02..2026-06-08 range was
    backfilled 06-02/06-08). It is used as a stratifier only for nights ≥ 06-09.
    - Separately and explicitly: `market_regime_snapshot` on `sas_candidates` **is** point-in-time
      (written with the candidate at 16:05 ET) and may be used for the whole sample as a *scoring
      input* descriptor — it is one of the plausible causes of a score shift and is reported under
      Channel 3a. The two must not be conflated in the report.
  - For the whole sample the tape is described from SPY's own trailing path in `prices_daily_split`
    (trailing 20-session return and realized vol), in words, not with a regime label.
- **Knowledge time (rule 14):** every field used was written at 16:05 ET with the candidate, or is a
  trailing price statistic. Nothing post-dates the pick night.

## 7. Multiple testing

- **Channels are not competing hypotheses with p-values**; the decomposition is an accounting
  identity plus counterfactuals, and its uncertainty is carried by bootstrap CIs on restored shares.
  The only formal test is **Gate 0** (one test, p ≤ 0.05).
- BH is nevertheless applied within Family **F2 Calibration** (H-010, H-011, H-012, PI-010/Q005 —
  4 items, 1 registered question) across any formal test that F2 questions report, so Q005's Gate 0
  p-value enters the family correction and is printed with its q (threshold q ≤ 0.10).
- **Channel 3 examines 14 components.** To stop component-shopping, the restored-share table is
  printed **in full, for every component, always** — no component may be omitted from the report,
  and the attribution rule in §8 is applied to whichever component tops the table, not to a
  component chosen afterwards.

## 8. Decision rule (numeric, written before unsealing)

Let `S` be the shortfall defined in §3 and `restored_share` be as defined in §4.

- **Gate 0 — NULL ("no fall to explain"):** if the nightly elite-candidate count shows no decline at
  p ≤ 0.05 (Poisson trend test) **and** the P1-vs-P0 exact Poisson rate test is not significant at
  p ≤ 0.05, the verdict is **NULL**: the monthly series is consistent with small-number noise, no
  product change follows, and DATA_NOTES' framing of a "shrinking" elite must be softened.
- **Attribution labels** (applied to each channel and to each Channel-3 component):
  - **EXPLAINS** — `restored_share ≥ 50%` and the bootstrap 95% CI lower bound ≥ 25%.
  - **CONTRIBUTES** — `restored_share ≥ 20%` and CI lower bound ≥ 0%.
  - **NOT A DRIVER** — `restored_share < 20%` or CI spanning 0.
- **HISTORICALLY_CONFIRMED (a cause is identified):** exactly one channel (or one Channel-3
  component) is labelled **EXPLAINS**, *and* it holds in the same direction in the month-by-month
  panel (its restored share ≥ 20% in at least 2 of the 3 months of P1), *and* it holds across the
  in-sample/sealed cut. The report then names that cause in its first sentence.
- **INCONCLUSIVE:** two or more components are labelled EXPLAINS (the decomposition cannot separate
  them); or the greedy-cumulative and marginal tables disagree about the top component; or the sum
  of all CONTRIBUTES/EXPLAINS shares reconstructs less than 50% of `S`, in which case the report
  states plainly that **the fall is unexplained by the registered channels** and names what data
  would separate them.
- **A discrete configuration change (Channel 3a) short-circuits the rest:** if `config_json` shows a
  weight, multiplier, threshold or flag change (including the ATR-elite-block cap or the
  `min_completeness` rule) whose effective date brackets the fall, the verdict is
  **HISTORICALLY_CONFIRMED — configuration**, the distributional channels are reported as secondary,
  and the brief is a config review rather than a data story.
- **PROSPECTIVELY_CONFIRMED is not available for this question.** It is a diagnostic of the past;
  the four-verdict controller record ends at HISTORICALLY_CONFIRMED / NULL / INCONCLUSIVE.
- **No MPE applies** (§Type). The 20%/50% attribution thresholds serve the same role as an MPE and
  are fixed here, before any look.

## 9. If a cause is identified, what changes on the platform

- **Score distribution / layer fell (Channel 2 or 3):** an `IMPLEMENTATION_BRIEF` to re-examine that
  layer's scaling — e.g. if the catalyst layer fell after 69ef05f, the fix moved a 10-weight layer
  off a flat 80 and the 90+ band was calibrated against the *broken* layer; if the **+5
  GEX-missingness offset** stopped firing after the coverage fix, the platform quietly removed a
  structural +5 that elite scores were leaning on (the code itself schedules that offset for a v1.6
  cleanup and a re-validation, `services/super_agent_select_scoring.py:1379-1391`); if the
  **ATR-elite block** is capping rows at 84.9/79.9 more often, that is a deliberate gate working as
  designed and the elite *definition*, not the engine, needs revisiting.
- **Candidate count fell (Channel 1):** the problem is upstream in the source engines (UOA/whale/
  projection feeds), not in scoring; the brief goes there.
- **Universe changed (Channel 4):** elite is a market-condition badge, not a quality badge, and the
  product must stop implying a constant standard.
- **In every branch, one product decision follows:** whether 90+ remains an absolute threshold or
  becomes a **relative** (per-night top-percentile) badge. That decision is Haci's; this question
  supplies the evidence. Until it is made, **every elite claim anywhere on the platform carries the
  DATA_NOTES caveat that it rests on ~45 picks and a handful of repeated names.**
- Any code change ships flag-off with a byte-identical checksum on the old path and a ≥ 20-day shadow
  (rule 11). Nothing here is subscriber-facing (NON_QUOTABLE).

## 10. Known threats to validity (registrar's own list)

1. **Small numbers.** 3 and 2 elite picks in August and September are Poisson noise territory; Gate 0
   is the guard, and the elite-candidate definition (not the published one) is primary for exactly
   this reason.
2. **The channels are not orthogonal.** Candidate count, score distribution and universe composition
   move together; marginal and cumulative attributions will differ, and §8 treats that disagreement
   as INCONCLUSIVE rather than picking the flattering table.
3. **Quantile mapping assumes the component's rank order is meaningful across periods.** For a layer
   that changed definition (catalyst, 06-01) this is false — handled by the separate post-fix
   restriction in §4.
4. **`config_json` may not capture every behavioural change.** Prompt or model changes in the
   upstream LLM agents (`ai_agents/principal_agent.py`) would not appear in config. The report must
   list the platform commits between 2026-04-01 and 2026-09-10 that touch scoring or the agents, from
   the read-only platform repo, as context — and say plainly that a prompt change is a cause this
   decomposition cannot see.
5. **`industry` at ~12% coverage** cannot support a sector conclusion; §4 restricts it and the
   report must not round that caveat away.
6. **Manual-run nights** distort candidate context (mixed-date `spot_close`) and contain 4 in-sample
   elites; they are excluded by the shared exclusions file and the corrected monthly series is
   printed next to DATA_NOTES' raw series. The two will not match, and that is expected.
7. **`market_regime_snapshot` (candidate column, point-in-time) vs `market_regime_daily`
   (backfilled before 06-09)** are different objects; conflating them would silently import a
   look-ahead. §6 separates them explicitly.
8. **This question is a decomposition, not a cause.** Even a clean EXPLAINS label identifies *where*
   the arithmetic moved, not *why* the market or the engine changed. The brief that follows must say
   so.
