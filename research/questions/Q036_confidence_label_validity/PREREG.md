# Q036 — confidence_label_validity: does the published "high / medium / low" conviction label actually mark a better price path?

**Status:** PREREG_DRAFT (lock by committing this file) — four items stand in §11 "Open decisions
before lock"; nothing else is pending.
**Family:** **F2 Calibration** (hypothesis **H-011**). The primary endpoint's subject is whether a
published confidence label orders outcomes, which is calibration (DP-29).
**Manifest (provenance, R1 exposure counts and the sealed post-hoc panel only):**
research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA
fa70688bc252d14f8d67e371afafc194731c324e). **No night that carries a verdict here exists in it.**
**Manifest (prices, same standing):** research/data/manifest_prices_v001.json (as_of: 2026-09-10;
base_manifest_sha256 b03f355a…bef374).
**Successor freezes — the question itself (built and pinned at the decision date, DP-23; §5.3 R2):**
`manifest_v00N` (selections: `sas_candidates` **for every candidate row, published and unpublished**,
`sas_runs`, `market_regime_daily`) and `manifest_prices_v00N` (daily bars for **every candidate symbol
on every in-window night**, published or not), covering pick nights **2026-09-15 .. 2027-06-11** with
daily bars through **2027-07-12** (session t+20 of the last included pick night, plus margin) and
≥ 60 prior sessions before 2026-09-15; a second pair **only if** the single DP-13 extension fires,
covering pick nights **.. 2027-07-26** with bars through **2027-08-23**. The primary window is
**entirely prospective** — not one contributing night exists in `manifest_v001` — so the population
enters only through those successor freezes. They are deliberately not written as `**Manifest …:**`
header lines, because no such file exists yet and the pin step reads every `**Manifest` line as a path.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates` ∪
`non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, DP-22)
**unioned with the add-only successor exclusions file** issued with the successor selection freeze —
the identical lists built by the identical criteria for nights after 2026-09-10, **plus
`payload_disabled_runs`** (a night on which every published row carries
`public_payload_json.analysis_status = "disabled"` or no `lane_plans` object, i.e. zero screened
`d_L3` survivors), inherited verbatim from Q027 §2.4 because this question uses Q027's `d*_t`
construction and inherits its failure mode. The successor file may only **add** nights. Both paths are
`eval.py` inputs; no hard-coded file name, no hard-coded date. DP-04 applies mechanically on top.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14

---

## 1. Hypothesis (plain English)

**When the platform prints "high conviction" next to a pick, that pick reaches a target the same
distance away — measured in its own daily range — more often and sooner than a pick on the same night
that the platform printed as "medium conviction"; and it does so for a reason the score alone does not
already explain.**

BACKLOG **H-011** reads: *"Confidence label (high/medium/low) vs realized return — baseline: label
shuffled."* It names the variable and the baseline and leaves the entry, the target, the clock, the
population and the decision rule open. This PREREG fixes all of them, and converts "realized return"
to the price path (rule 5, DP-01) — the return is reported and never decides.

### 1.1 What the label actually is (read from the platform, not assumed)

`services/super_agent_select_scoring.py:1166-1171`:

```python
def _confidence_label(overall_score: float, completeness_score: float) -> str:
    if overall_score >= 82.0 and completeness_score >= 65.0:
        return "high"
    if overall_score >= 68.0 and completeness_score >= 45.0:
        return "medium"
    return "low"
```

It is called once per candidate at `:1425`, after the ATR-elite block (`:1407-1423`), and stamped on
the scorecard at `:1451`. `completeness_score` is `available_weight / total_weight × 100` (`:1347`),
where `total_weight` is the sum of the **timeframe-adjusted effective weights** (`:1316-1322`) — so
completeness is a measure of **how much of the scoring stack had data**, and it is lane-dependent.

Three consequences that shape this question and are stated here so nothing downstream is a surprise:

1. **The label is not a band of `overall_score`.** It is a joint step function of `overall_score`
   **and** `completeness_score`. It is therefore **not** Q027's band-level secondary and this question
   does not merge into Q027 (DP-29 checked explicitly; §7 "Overlaps").
2. **Among published picks the label reduces to a completeness cut.** Publication requires
   `overall_score ≥ 80` (`services/super_agent_select_models.py:91`) and `completeness ≥ 35`
   (`:98`). So on the published slate: `high ⇔ score ≥ 82 ∧ completeness ≥ 65`;
   `medium ⇔ ¬high ∧ completeness ≥ 45`; `low ⇔ completeness < 45`. **Above score 82, high-versus-
   medium is exactly "completeness ≥ 65" versus "completeness 45–65".** That is what endpoint **E2**
   tests, and it is the sentence that separates Q036 from Q027.
3. **The label is subscriber-facing.** `services/super_agent_select_public.py:212` writes *"The symbol
   scored X with {confidence_level} conviction"*, and the label ships in the payload at `:278` and
   `:371`. A mis-ordered label is therefore not a harmless internal field; §9 says what follows.

### 1.2 Two primaries (§4), both night-level, both two-sided

- **E1 — does the label order outcomes at all?** The within-night **high minus medium** touch rate at
  a common ATR distance within 20 sessions from the session t+1 open, averaged over nights, against
  H-011's own baseline (the within-night **label shuffle**). **MPE ±5.0 pp (DP-20, DP-44).**
- **E2 — does the label add anything the score does not already carry?** The same contrast computed
  on **adjacent-score-rank discordant pairs** among published rows with `overall_score ≥ 82`, so the
  two members of every compared pair are the closest in score the night allows. **MPE ±5.0 pp
  (DP-20, DP-44).**

**Both are registered two-sided, and the negative direction is the live one.** The desk's own weekly
of 2026-09-12 recorded, on sealed nights, *"Medium beat high on next-open L1 touch (78% vs 65%)"* —
i.e. the standing suspicion is that the label is **mis-ordered**. A CONFIRMED negative is a more
consequential finding than a null and §9 says what it licenses. Because that read exists, the sealed
stretch is contaminated for this question and carries **no verdict** (§6).

**Why E1 without E2 would not be a result.** If E1 confirms and E2 nulls, the label is a repackaging
of the score and the finding belongs to Q027, not here; §8 says so numerically.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Rows are reduced to one statistic per night
  first; nights are the observations. Control rows never add to n.
- **Source tables (successor selection freeze, §5.3):**
  `sas_candidates` — **every row, published and unpublished** (the unpublished rows serve §3's B3
  control and §4.3's dark-set panel only): `trading_date`, `symbol`, `overall_score`,
  **`confidence_level`**, **`completeness_score`**, `qualified`, `threshold_pass`,
  `qualification_reason`, `selected_rank`, `dominant_direction`, `best_timeframe`, the seven layer
  subscores, `cross_layer_bonus`, `conflict_penalty`, `missing_data_penalty`, `score_details_json`,
  `context_json`, `public_payload_json` → `lane_plans.swing_trading.targets` (published rows only,
  for §2.2's distance), `outcome_target_invalid` (exclusion audit only);
  `sas_runs` — `finished_at` (DP-04) and **`config_json`** (the enrichment-flag / weight /
  `min_completeness` audit, §2.6 — load-bearing here in a way it is not in other questions);
  `market_regime_daily` — `trading_date`, `regime_version`, `market_regime`, `data_quality`,
  `created_at` (rule-7 stratum only; never a filter, never an arm).
- **Source tables (successor price freeze):** `prices_daily_split` (pick-night close, ATR14, beta60,
  runup20, mom20, adv20, forward bars to t+20, SPY tape), `prices_daily_raw` (split-factor snapping
  only). **No hourly bar is used and no primary depends on one.**
- **No outcome column is ever an input.** `outcome_*`, `sas_selection_excursion.*`, `level_hit_*` are
  not joined. `uoa_symbol_daily.fwd_return_*` is banned outright (FREEZE_v001 §5). Every outcome here
  is computed from pinned bars.

### 2.1 Eligible rows — exact filter

The two dates below are **illustrative of values `eval.py` receives as arguments**. §5.3 R2 requires
the script to take the window start, the window end, the manifest paths, the exclusions-file paths
and the output directory as arguments, with **no hard-coded date, manifest name or path**, so that the
byte-identical script serves the primary run and the single DP-13 extension run alike.

```sql
-- primary population: the published slate (DP-28)
SELECT c.*
FROM   sas_candidates c
JOIN   sas_runs run ON run.trading_date = c.trading_date
WHERE  c.trading_date >= DATE '2026-09-15'        -- §6 window start  (input, illustrative)
  AND  c.trading_date <= DATE '2027-06-11'        -- §5.2 window end  (input, illustrative)
  AND  c.qualified IS TRUE
  AND  c.selected_rank IS NOT NULL                -- DP-28: dark-lane rows excluded from every arm
  AND  c.dominant_direction IN ('bullish','bearish')
  AND  c.confidence_level IN ('high','medium','low')
  AND  c.trading_date NOT IN (SELECT d FROM exclusions_union)   -- §2.4
```

```sql
-- B3 control cohort and the §4.3 dark-set panel only; never in a primary denominator
SELECT c.* FROM sas_candidates c
WHERE  c.threshold_pass IS TRUE
  AND (c.qualified IS NOT TRUE OR c.selected_rank IS NULL)
  AND  c.dominant_direction IN ('bullish','bearish')
```

### 2.2 Arms

Read from the stored `confidence_level` column — the label the subscriber actually saw — never
recomputed into existence:

| arm | filter | what it reduces to on the published slate (§1.1) |
|---|---|---|
| **HIGH** | `confidence_level = 'high'` | `score ≥ 82 ∧ completeness ≥ 65` |
| **MED** | `confidence_level = 'medium'` | `¬high ∧ completeness ≥ 45` |
| **LOW** | `confidence_level = 'low'` | `completeness < 45` |

**LOW is a descriptive arm only** (§4.3) and is never a primary: it is structurally rare on a slate
that already screens at `min_completeness = 35` (`super_agent_select_models.py:98`), and registering
it as a primary would put an endpoint in the correction set that is expected to sit under the 20-night
cell floor. If R1 (§5.1) measures LOW at ≥ 20 contributing nights per calendar half it is still
reported descriptively, with the reason printed.

**Integrity screen, blocking.** `eval.py` recomputes `_confidence_label(overall_score,
completeness_score)` from the stored `overall_score` and `completeness_score` using the literal
constants at `super_agent_select_scoring.py:1167-1170` and compares it with the stored
`confidence_level`. Mismatched rows are **excluded and counted**, and the per-night mismatch share is
printed in the results header. **If more than 2% of eligible rows across the window mismatch, the
question is INCONCLUSIVE on both primaries** — the thresholds are hard-coded constants, not config, so
a material mismatch means something other than `_confidence_label` is writing the column and the arms
are not what this file registered.

### 2.3 The target, the entry and the clock — inherited from Q027, unchanged

This question deliberately reuses **Q027 §2.2 and §2.3 verbatim**, so that a Q036 result and a Q027
result are measured on the same ruler and are directly comparable within F2.

- `dir` = +1 for `bullish`, −1 for `bearish` from `dominant_direction`; every distance and touch is
  direction-adjusted.
- `C_t` = the row's actual regular-session close on night t from `prices_daily_split` (never
  `spot_close`, stale on re-run nights — EXPLORE_001 §9).
- `ATR` = ATR14 from `prices_daily_split` bars dated ≤ t (never `atr_pct`, corrupted around splits —
  DATA_NOTES / PI-003).
- **`d*_t`, the night's common distance** = the median over that night's **screened published** picks
  of `d_L3 = dir × (L3 − C_t) / ATR`, with `L3 = lane_plans.swing_trading.targets[0]` (volatilx
  `services/sas_conviction_card.py:182-187`) — the distance the platform itself printed as the swing
  first target that night, in ATR units. Q027 §2.2's split-scale screen, its 1–2-survivor trailing-
  20-night fallback, its zero-survivor whole-night exclusion and its `[0.25, 10]` fail-loud bound are
  inherited word for word.
- **The synthetic target** for row i on night t: `T_i = C_i × (1 + dir_i × d*_t × atr_pct_i)` with
  `atr_pct_i = ATR_i / C_i` — **the same ATR distance and the same direction for every row on the
  night**. This is where rule 5's distance matching lives for the primaries: HIGH and MED are compared
  at an identical ATR distance by construction, not by a post-hoc adjustment.
- **Entry `X_i` = the session t+1 regular-session open** (DP-03(b), DP-42), identical for every row.
  The `C_t` basis (DP-03(a) / DP-11) is computed and printed for both primaries as a named
  sensitivity and **never decides**.
- **A target already through `X_i` at the t+1 open is not a hit** (rule 5, DP-26): `hit_i = 0`,
  `s_i = ∞`, the row stays in the denominator, and the not-takeable count is printed per arm. This
  matters here: if HIGH picks gap through their target more often, that is a *cost* of the label, and
  it is measured rather than hidden.
- **Clock: 20 sessions, t+1..t+20** for every row (DP-09, DP-42 — the swing lane's L3 on the spread
  horizon). The platform's own 40-session swing window is printed as a descriptive companion.
- **`hit_i` ∈ {0,1}** = 1 if the regular-session high (bullish) / low (bearish) touches `T_i` on some
  session in t+1..t+20; a gap through `T_i` at a session open is a touch.
- **`s_i`** = sessions from `X_i` to that first touch (1..20), `∞` otherwise (DP-08: *when*, not only
  *whether*). Sessions-to-touch differences are **descriptive, no MPE** (DP-44); the unconditional
  touch-within-20 form decides.
- **No stop, ever** (rule 5, DP-02). Maximum adverse excursion and counter-direction touches at
  `−d*_t` ATR are reported per arm, never used as exits.

### 2.4 Exclusions — each counted, printed in the results header, never silently dropped

Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or a
measurement failure. **None can move a row between arms**, which is the property that matters here:
no exclusion reads `confidence_level`, `completeness_score` or any outcome.

- **Nights** in the union of `exclusions_v003.json` and the add-only successor file — `manual_runs` ∪
  `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ `payload_disabled_runs` — and any night
  whose `finished_at` is later than the next session's open, or dated on a non-session day (DP-04).
- **`dominant_direction = 'mixed'`** (`super_agent_select_scoring.py:1180`) → row excluded and
  counted; a synthetic target needs a direction. The mixed share **per arm** is printed, and a night
  is excluded whole if more than 25% of its published rows are mixed. (Q027 R1(b) measured mixed at
  0.0% from score decile 4 up, so on a published slate floored at 80 this screen is expected to be
  near-empty; it is registered anyway.)
- **Fewer than 60 split-adjusted daily bars dated ≤ t** (ATR / beta60 / runup20 / adv20 undefined) →
  row excluded and counted (the CTRA truncated-history signature, `STEWARD_Q023_exposure.md` §6).
- **Missing forward bars** inside t+1..t+20 (halt, delisting) → ungradeable, excluded and counted; a
  measurement failure, never a classifier. A night is dropped if > 20% of its published rows are
  ungradeable.
- **Immature nights** — session t+20 after the last trading date of the pinned price freeze →
  excluded and counted. Maturity comes from the trading calendar, never from whether a price exists;
  right-censoring is never graded as a non-touch.
- **Split-scale payload screen** on the `d*_t` median only (Q027 §2.4, DATA_NOTES): a published row is
  dropped from the **median** if `lane_plans.day_trading.entry / C_t` is outside `[0.85, 1.15]` or any
  flattened level implies `|dir × (level − C_t) / ATR| > 20`. It is **not** dropped from the
  population — it still carries a label and a synthetic target.
- **Label-integrity mismatches** (§2.2) → excluded and counted, with the 2% blocking clause.

### 2.5 Contributing night, and the episode (DP-51)

- **Contributing night for E1** (the floor unit, DP-21): a non-excluded, matured night in the window
  with a defined `d*_t` and **at least one HIGH row and at least one MED row** among its eligible
  published rows. A night whose slate is all-HIGH (or all-MED) is **non-contributing, counted, and
  printed** — the per-night label composition table is part of the results header, because the rate at
  which the slate is single-label is the single biggest determinant of this question's power.
- **Contributing night for E2:** the same, restricted to rows with `overall_score ≥ 82`, so that both
  arms are on the same side of the label's score threshold and the contrast is a completeness
  contrast (§1.1). E2's contributing nights are a subset of E1's; the difference is nights on which
  every MED row sits in `[80, 82)`. That count is printed.
- **Episode (DP-51):** an *episode* is one symbol's run of published selections with gaps of ≤ 10
  sessions between successive selections (the TI-003 / Q003 window). Every primary is reported
  **twice** in §8 — the registered date-clustered block-bootstrap CI, and an **episode-clustered** CI
  resampling episodes and nights jointly. **A primary that clears MPE on the first and not on the
  second is INCONCLUSIVE, never CONFIRMED** (DP-51). This matters more than usual here: a
  high-completeness name is a name with options-flow, catalyst and GEX coverage, and such names
  re-appear on consecutive nights more than thin-coverage names do.

### 2.6 The feature can change under the desk's feet — the enrichment-flag split

`completeness_score` is `available_weight / total_weight` over the **effective** dimension weights
(`super_agent_select_scoring.py:1316-1322, :1347`). Three platform settings move it without moving a
single price: the scoring weights, the timeframe multipliers, and the enrichment enable-flags
(`enable_catalyst_enrichment`, `enable_fundamental_enrichment`, `enable_smart_money_enrichment` —
`super_agent_select_models.py:109-111`, the last two defaulting **False**). If any of them ships
mid-window, the 65 and 45 lines fall in a different place and **the label is a different feature
before and after**, exactly the DP-06 / DP-50(a) pattern.

So: `eval.py` reads every in-window night's `sas_runs.config_json`, prints the per-night panel of
scoring weights, timeframe multipliers, `min_completeness`, `publication_floor` and the three
enrichment flags, and **splits the window at any date on which that tuple changes**, reporting each
side separately and the pooled result only when both sides agree in sign. A split that leaves either
side below 20 contributing nights makes that side descriptive; a split that leaves the **larger** side
below 80 makes both primaries INCONCLUSIVE (§8 clause 6). Any such ship date is also checked against
`research/data/DATA_NOTES.md` (DP-50(a)).

## 3. Baselines — what this must beat

There is always a baseline; here there are four, and the first is the one H-011 names.

- **B0 — the thing the claim is against: the MED arm.** "High conviction picks reach target more
  often" has as its baseline the **same night's medium-label published picks, at the same ATR
  distance, from the same entry, on the same clock**. Both primaries are differences against B0.
- **B1 — H-011's own baseline, the label shuffle (E1's null).** Within each contributing night,
  permute `confidence_level` across that night's eligible published rows, preserving the night's label
  counts exactly; recompute E1; 10,000 draws; the p-value is the two-sided permutation p on the
  night-averaged statistic (rule 6: p-values from permutation tests). Nights are permuted
  independently and the night structure is preserved, so the shuffle destroys only the
  label-to-outcome link.
- **B2 — the matched-pair randomization (E2's null).** For each adjacent-score-rank discordant pair
  (§4.2), flip which member is treated as HIGH with probability ½, independently across pairs;
  recompute E2; 10,000 draws. This is the conditional null — it holds the score-to-label association
  fixed, which a plain label shuffle does not, and is therefore the correct baseline for a
  score-matched endpoint.
- **B3 — the distance-matched control cohort (rule 5), descriptive.** The same night's **unpublished**
  `threshold_pass` candidates, with targets at the identical `d*_t` ATR distance and the identical
  entry and clock. B3 does not enter either primary — the primaries are already distance-matched
  arm-to-arm by §2.3 — but **no absolute touch rate for any arm may be quoted anywhere without B3
  printed beside it**. A hit rate without that control is descriptive (rule 5).

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

### 4.1 Per night

For contributing night t, over eligible published rows:

- `p_HIGH(t)` = share of HIGH rows with `hit_i = 1`; `p_MED(t)` likewise.
- `e1(t) = p_HIGH(t) − p_MED(t)` — in percentage points.
- `Δs(t) = mean(s_i | HIGH, hit) − mean(s_i | MED, hit)` — sessions, **descriptive** (DP-44).

### 4.2 Primary endpoints

- **E1 = mean over contributing nights of `e1(t)`.** Two-sided. **MPE ±5.0 pp (DP-20, DP-44).**
  p from B1. CI: date-clustered block bootstrap over nights (block length 5 sessions) **and**
  episode-clustered (DP-51), both printed.

- **E2 = mean over contributing nights of `e2(t)`**, where `e2(t)` is built as follows and nowhere
  else:
  1. Take the night's eligible published rows with `confidence_level ∈ {high, medium}` **and
     `overall_score ≥ 82`**.
  2. Sort them by `overall_score` ascending; ties broken by `symbol` ascending (deterministic).
  3. Form every **adjacent** pair `(i, i+1)` in that order whose labels **differ**. In any ordering
     containing both labels at least one such pair exists, so every night with both arms present above
     82 contributes — and each pair is the closest-in-score comparison that night admits.
  4. `e2(t)` = the mean over those pairs of `100 × (hit_HIGH − hit_MED)` percentage points.

  Two-sided. **MPE ±5.0 pp (DP-20, DP-44).** p from B2. CIs as for E1, both forms (DP-51).
  The distribution of the within-pair `|Δoverall_score|` is printed. **Blocking sensitivity:** E2
  recomputed with pairs of `|Δoverall_score| > 2.0` dropped; if that version's point estimate changes
  sign or falls outside the primary's 95% CI, the verdict is **INCONCLUSIVE** (§8 clause 5).

### 4.3 Reported, never deciding (no MPE, raw p only, marked *"descriptive, does not decide"*)

- **The fixed-horizon return H-011 literally names:** direction-adjusted t+1-open-to-t+20-close return
  per arm and the HIGH−MED difference, with medians and a trimmed mean beside the mean. Rule 5 /
  DP-01: **it never decides**, and §9 forbids quoting it alone.
- **B3 panel:** absolute touch rate for HIGH, MED and the distance-matched unpublished control.
- **LOW arm:** e1-style contrasts LOW vs MED and LOW vs HIGH, with counts.
- **Dark-set panel:** the same E1 statistic computed on unpublished `threshold_pass` rows, where all
  three labels have mass. This is the "does the label work where it is not shown" panel; a
  disagreement between it and E1 is reported loudly and licenses nothing.
- **Completeness as a continuous variable:** per-night Spearman correlation between
  `completeness_score` and the path-outcome rank `u_i` (Q027 §2.3's variable), on published rows with
  `overall_score ≥ 82`. This is E2's continuous shadow and is the diagnostic that says whether a
  confirmed E2 is a threshold effect at 65 or a smooth completeness gradient.
- **Balance table across arms** (the confounders the label is not matched on): `beta60`, `atr_pct`,
  `runup20`, `mom20`, `log10 adv20`, `best_timeframe` mix, `dominant_direction` mix, `selected_rank`
  distribution, `conflict_penalty`, `missing_data_penalty`, and the share with each layer subscore
  null. **`missing_data_penalty` is the one to watch**: it is driven by the same missing layers that
  drive completeness, so it is a mediator, not a confounder, and it is printed rather than adjusted.
- **Not-takeable counts per arm** (targets already through the t+1 open), **MAE** and
  counter-direction touch rate per arm, and `Δs(t)`.
- **40-session companion** on the platform's own swing window, published rows only.
- **Strata (rule 7):** every stratum below prints E1 and E2 with counts; a cell under **20
  contributing nights** is printed and marked descriptive.
  - `market_regime_daily.market_regime` (point-in-time; see §10 threat 8).
  - Calendar halves (§6).
  - `best_timeframe` (day / swing / long) — required, because `total_weight` and therefore
    completeness is lane-dependent (`:1316-1322`).
  - `dominant_direction` (bullish / bearish).
  - Score stratum `[80,82) / [82,85) / [85,88) / [88,90) / [90,100]` — E1 only; `[80,82)` can contain
    no HIGH row by construction and is printed as a structural zero, not a finding.

## 5. Sample floors and expected n

Floors (rule 6, DP-21): **≥ 80 contributing nights per primary endpoint**, **≥ 20 per stratum cell**.
DP-24: **≥ 30 contributing nights dated after the lock commit** — satisfied trivially, since the
entire window is post-lock. Monte Carlo draws (B1, B2) never add to n.

### 5.1 Expected n, the assumption it rests on, and the gate that replaces guessing

Measured run-rate, from `STEWARD_Q034_exposure.md` on the pinned freeze (counts only, DP-50(c)):
**71 elapsed sessions in 2026-06-01..2026-09-10 (≈ 21.3 per month), 3 excluded (4.2%), 68 non-excluded
nights, 550 published rows → 8.09 published rows per night.**

Window 2026-09-15..2027-06-11 ≈ 8.9 months → ≈ **190 elapsed sessions**, ≈ **182 non-excluded**.
Contributing nights depend on one unmeasured quantity: **`ρ_co`, the share of nights whose published
slate carries at least one HIGH row and at least one MED row.** With ~8 published rows a night it is
not obviously near 1 and it is not obviously small; the desk does not know it, and this file does not
guess it.

**Required:** `80 / 182 = 0.44` contributing nights per non-excluded night. So the question is
feasible iff **`ρ_co ≥ 0.44`** (E1) and the E2 restriction to `overall_score ≥ 82` does not push it
below that.

**R1 — Steward exposure request, counts only, due before the lock is pinned.** On the 68 non-excluded
sealed nights of `manifest_v001`, measure and report: (a) the per-night count of published rows by
`confidence_level`; (b) `ρ_co` = share of nights with ≥ 1 HIGH **and** ≥ 1 MED published row;
(c) the same restricted to `overall_score ≥ 82` (E2's `ρ_co`); (d) the count of nights with any LOW
published row; (e) the joint distribution of `overall_score × completeness_score` on published rows,
as counts in the `[80,82)/[82,85)/[85,88)/[88,90)/[90,100] × [35,45)/[45,65)/[65,100]` grid; (f) the
per-night `sas_runs.config_json` tuple of §2.6 across the sealed window, so the desk knows whether
that tuple has ever moved; (g) the label-integrity mismatch rate of §2.2. **No outcome of any kind**
— no touch, no first-touch date, no return, no excursion, no `outcome_*`, no
`uoa_symbol_daily.fwd_return_*`. All seven limbs are population counts and none reads a price.

**Gate, fixed at this lock and not negotiable afterwards (DP-43's 12-month ceiling, DP-45):**

| R1 measures | consequence |
|---|---|
| `ρ_co ≥ 0.44` **and** E2's `ρ_co ≥ 0.44` | lock as written; window and dates below stand |
| either in `[0.36, 0.44)` | lock as written; the DP-13 extension (§5.2) is expected to be needed and is already registered |
| either `< 0.36` | **the question does not lock — it goes to `research/questions/DEFERRED.md`** with `ρ_co` named, because 80 contributing nights would then need a window past 2027-09, which is more than 12 months after lock (DP-43) |
| E1's gate passes but E2's fails | **DEFERRED**, not "lock E1 alone" — E1 without E2 cannot be distinguished from Q027 (§1.2) and would add a primary to F2 that can only restate another question |

### 5.2 Window, decision date, extension, hard stop

- **Window:** pick nights **2026-09-15 .. 2027-06-11**.
- **Maturity:** t+20 of 2027-06-11 ≈ **2027-07-12**; the successor price freeze carries bars through
  that date plus margin, and ≥ 60 prior sessions before 2026-09-15.
- **Decision date: 2027-07-19** (the first Monday on or after maturity plus a one-week freeze margin,
  DP-43). **≈ 10.1 months after lock — inside DP-43's 12-month ceiling.**
- **DP-13, registered here and firing on `eval.py`'s measured counts, never on a projection or a
  run-rate:** if at the decision date **either** primary is short of 80 contributing nights, or the
  DP-24 post-lock clause is short, the window extends **once, automatically, with no new question**,
  to pick nights through **2027-07-26** (+30 sessions), bars through **2027-08-23**, and the
  **extension decision date 2027-08-30**. No gate is ever reduced.
- **Hard stop: 2027-08-30.** If a gate is still short after that single extension, the question goes
  to **DEFERRED** rather than running under-powered (DP-13).

### 5.3 Routed requests

- **R1 — data-steward, before the lock is pinned:** §5.1, counts only, on the pinned freeze. Its
  result decides lock-versus-DEFERRED by the §5.1 gate table, and nothing else in this file moves.
- **R2 — data-steward, at the decision date (DP-23):** build and pin `manifest_v00N` /
  `manifest_prices_v00N` per the header, **including every candidate symbol, published and
  unpublished** (B3 needs the unpublished cohort), plus the add-only successor exclusions file built
  by the four criteria fixed at this lock. `eval.py` takes every path and date as an argument.
- **R3 — researcher:** `eval.py` is written **once**, before any successor freeze exists, against the
  §2 schema, and is byte-identical across the primary and extension runs (rule 9).

## 6. Split and stratification

- **The sealed stretch carries no verdict.** The weekly of **2026-09-12** printed, on sealed nights,
  the medium-versus-high next-open L1 touch rate (78% vs 65%) and a Jun–Aug return comparison by
  label; the weekly of **2026-09-10** printed a projection-confidence version. This question's exact
  contrast has therefore been read on those nights. They are contaminated and are **not used for any
  verdict, half, stratum, CI comparison or q**. They are printed **once**, as a clearly labelled
  post-hoc panel, with the contamination note attached (the Q027 / Q023 pattern). The panel exists so
  that the weekly's uncontrolled line is replaced by the same number computed properly, and it
  licenses nothing.
- **In-sample / out-of-sample by calendar date:** **H1 = pick nights 2026-09-15 .. 2027-01-29**,
  **H2 = 2027-02-01 .. 2027-06-11**. Both primaries are computed and reported in each half separately
  as well as pooled. Halves are fixed here and are never re-cut after the numbers are seen.
- **A result counts only if the sign agrees in both halves** (rule 7, §8 clause 3).
- **Regime stratification (rule 7):** `market_regime_daily.market_regime`, joined on `trading_date`,
  with `regime_version` and `data_quality` printed. The whole window is after **2026-06-09**, so every
  regime label used here is point-in-time legal (CLAUDE.md; FREEZE_v001 §7) — the backfill hazard does
  not touch this question, and that is a property of the window, not an assumption.
- **DP-06 does not bite** — the window is entirely after 2026-06-01 — but **§2.6's enrichment-flag
  split is the same hazard in this question's own variable** and does bite if a config ships.

## 7. Multiple testing

- **Primaries registered here: 2** (E1, E2). `m = 2` is **fixed at this lock**: both carry a verdict in
  every branch, an endpoint short of floor still has its p computed, and neither is dropped afterwards
  (dropping one would lower the bar for the survivor). Every §4.3 panel, every stratum and the LOW arm
  print **raw p only**, marked *"descriptive, does not decide"*, and enter no correction set.
- **Across the family: F2 Calibration.** F2 holds H-010, H-011, H-012, H-013, H-014, H-073, H-079,
  H-080, H-082, with H-010 and H-012 merged into Q027 (DP-29). The F2 correction set is computed at
  the decision pass over the F2 questions locked by then and **never shrinks below the 18 primaries
  standing at this lock**: Q023 (2) + Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) +
  **Q036 (2) = 18**. Q005 is excluded for the stated reason — a diagnostic decomposition with no MPE
  and no outcome column read at all. If H-014, H-079, H-080 or H-082 lock before **2027-07-19**, their
  primaries join the set and the q's are recomputed on the larger m; the set never shrinks.
- **Threshold: q ≤ 0.10** (Benjamini–Hochberg), reported alongside raw p (rule 8).
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q027 (F2)** asks whether `overall_score` orders outcomes. **Q036 shares Q027's `d*_t`, entry,
    clock and outcome variable, and on prospective nights it shares many of the same nights.** E1 is
    partly a restatement of Q027's ranking result on a coarser variable; **E2 is the part that is
    not**, and §8 clause 4 refuses a Q036 verdict that rests on E1 alone. A Q027 confirmation and a
    Q036 E1 confirmation are **one finding stated twice** unless E2 confirms too; neither may be
    quoted as corroborating the other.
  - **Q005 (F2, PI-010)** decomposes why the elite band thinned and reads `completeness_score` as one
    channel component. It reads **no outcome column at all** and says nothing about whether
    completeness predicts a path; there is no overlap of endpoints.
  - **Q029 (F1/F2)** owns the per-layer ICs. A layer that carries information there is a candidate
    *explanation* for a confirmed E2 (completeness is presence-of-layer), never corroboration of it.
  - **The projection-target confidence label** (`services/projection_picks_scoring.py:218-264`) is a
    **different field on a different object** and is **out of scope**; the 2026-09-10 weekly's
    proposal to extend H-011 to it is a separate hypothesis and is not tested here (DP-25).

## 8. Decision rule (numeric, written before unsealing)

Clauses 5, 6, 7 and the §2.2 integrity screen are **blockers**: they can only move a verdict toward
INCONCLUSIVE, never toward CONFIRMED.

1. **CONFIRMED (positive) — requires both primaries.** `E1 ≥ +5.0 pp` **and** `E2 ≥ +5.0 pp`, each
   with a 95% **date-clustered** CI excluding 0 **and** a 95% **episode-clustered** CI excluding 0
   (DP-51), each with `q ≤ 0.10` on the F2 set, each with ≥ 80 contributing nights, and clause 3 clean.
2. **CONFIRMED (negative) — the live direction.** The mirror of clause 1 with both `≤ −5.0 pp`. This
   is a result, not a failure, and §9 gives it the larger consequence.
3. **Half agreement (rule 7).** Both halves must carry the same sign on the endpoint concerned. Signs
   disagreeing on either primary → **INCONCLUSIVE**, reported with both halves printed.
4. **E1 and E2 disagreeing — the Q027 boundary.** `E1` clears MPE and `E2` does not (CI including 0,
   or `|E2| < 5.0 pp`): the verdict is **NULL for Q036**, stated as *"the label carries no path
   information beyond `overall_score`; whatever E1 shows belongs to Q027's ranking result."* No
   label-specific guide line, brief, flag or quotable number follows. The converse — `E2` clears and
   `E1` does not — is **INCONCLUSIVE** and reported as a contradiction, loudly: a completeness effect
   that vanishes unconditionally means the label's own composition is working against it.
5. **Pair-caliper blocker.** If E2 restricted to `|Δoverall_score| ≤ 2.0` (§4.2) changes sign or falls
   outside the primary E2's 95% CI → **INCONCLUSIVE**.
6. **Config-split blocker (§2.6).** If the §2.6 tuple changes in-window and the larger side has < 80
   contributing nights, or the two sides disagree in sign on either primary → **INCONCLUSIVE**, with
   the split date and the ship SHA printed.
7. **Episode blocker (DP-51).** A primary clearing MPE on the date-clustered CI but not the
   episode-clustered CI is **INCONCLUSIVE**, never CONFIRMED.
8. **NULL.** Both primaries at ≥ 80 contributing nights with 95% CIs including 0, or with point
   estimates inside ±5.0 pp. "Positive but below MPE" is **INCONCLUSIVE**, never CONFIRMED (rule 6).
9. **INCONCLUSIVE.** Any primary below 80 contributing nights after the single DP-13 extension (which
   sends the question to DEFERRED instead, §5.2), any blocker firing, the §2.2 mismatch rate above 2%,
   or a q above 0.10 on an otherwise-passing primary.
10. **What a confirmed E2 does and does not mean (binding on the report).** A CONFIRMED-positive E2
    means *"among published picks scoring 82 or better on the same night, the ones with more of the
    scoring stack populated reached a target at the same ATR distance more often within 20 sessions,
    by X pp."* It does **not** mean the picks made money, it does **not** mean the published slate
    beats anything (Q006, Q024), and it does **not** license quoting the word "conviction" as a
    probability. The B3 control rate, the not-takeable share and the arm counts must be printed beside
    any quoted number.
11. **PROSPECTIVELY_CONFIRMED:** reachable from this run by design — every contributing night is dated
    after this file's lock commit and is frozen in successor manifests never inspected earlier
    (DP-24, DP-21), reproducing the sign under the unmodified `eval.py`. No subscriber-facing
    statement before that (rule 10); even then the basis is `NON_QUOTABLE` until restated on W60
    (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform prints the label in plain words to subscribers — *"The symbol scored X with
{confidence_level} conviction"* (`services/super_agent_select_public.py:212`) — and ships it in the
payload (`:278`, `:371`). **Nothing on the platform has ever tested whether that word is ordered
correctly**, and this question is that test. Nothing subscriber-facing ships before
PROSPECTIVELY_CONFIRMED (rule 10); everything below ships flag-off with a byte-identical checksum on
the old path and shadows ≥ 20 trading days before any flip (rule 11).

- **Both primaries CONFIRMED positive (clause 1):** (a) a **Manual Trading Guide line** stating the
  measured HIGH−MED gap with the B3 control rate, the not-takeable share and the arm counts printed
  beside it; (b) a **lane rule** — on a night where two published picks score within 2 points, prefer
  the "high" one, sized by the measured E2 gap; (c) an `INTERNAL_TOOL`, flag-off card field surfacing
  `completeness_score` itself, since E2 says the completeness line is where the information is.
- **Both primaries CONFIRMED negative (clause 2) — the larger consequence.** The card is telling
  subscribers the opposite of what the data says. (a) A brief is written to **suspend the conviction
  wording at `super_agent_select_public.py:212`** on the internal surface immediately and to gate the
  subscriber surface behind the flag; (b) a brief to **re-derive or retire `_confidence_label`**
  (`:1166-1171`) — the honest reading of a confirmed negative is that a *data-availability* measure
  has been given a *conviction* word, and the enhancement is either to re-fit the thresholds against
  the measured path or to rename the field to what it measures; filed against ENHANCEMENTS **EN-018**,
  the gated home for setup and tier labels; (c) the weekly stops printing label panels as a signal.
- **E1 CONFIRMED, E2 NULL (clause 4):** **no label-specific change at all.** A brief is written to
  **replace the label on the card with the score tier it is standing in for**, because a second
  presentation of the same information invites double-counting by the reader. Every consequence in
  that branch belongs to Q027, and the Q036 line in the ledger says so.
- **Both NULL (clause 8):** the label is uninformative about the path. A brief is written to drop the
  word "conviction" from `:212` in favour of a neutral coverage statement, or to remove the field —
  **this is a result, not a non-result**, and it retires a standing subscriber-facing claim.
- **INCONCLUSIVE:** nothing ships, and the reason (which blocker fired) is ledgered.
- **Nothing in any branch may be supported by the §4.3 fixed-horizon return**, alone or in
  combination (rule 5, DP-01).

Owner: implementer, via `IMPLEMENTATION_BRIEF.md` run by Haci in the platform repo (rule 2). Shadow
period before any flip: ≥ 20 trading days. No brief written from this question hands the coding agent
a database step (DP-49).

## 10. Known threats to validity (registrar's own list)

1. **Score confounding — the central threat.** The label contains `overall_score ≥ 82`, so an
   unconditional HIGH−MED gap is partly Q027's ranking result. **E2 exists solely for this**, and §8
   clause 4 makes E1-alone a NULL rather than a finding. Residual within-pair score difference is
   printed and clause 5 blocks on it.
2. **Completeness is a liquidity/coverage proxy.** A high-completeness name is one with flow,
   catalyst and GEX data — larger, more optionable, more covered. A confirmed E2 could be a size or
   liquidity effect wearing a label. The §4.3 balance table prints `beta60`, `atr_pct`, `runup20`,
   `log10 adv20` and the layer-null shares across arms; §9 forbids a mechanism claim, and §8 clause 10
   binds the wording. This is disclosed, not adjusted away.
3. **`missing_data_penalty` is a mediator, not a confounder.** The same missing layers that lower
   completeness also subtract from `overall_score` (`:1364-1368` per Q005). Adjusting for it would
   remove part of the effect being measured. It is printed per arm and never adjusted.
4. **Lane-dependence of completeness.** `total_weight` uses timeframe-adjusted effective weights
   (`:1316-1322`), so the identical missing layer produces a different completeness in day, swing and
   long. The lane stratum in §4.3 is required for this reason, and a label effect that lives in one
   lane only is reported as such.
5. **Config drift inside the window** — §2.6, with the blocking clause at §8 clause 6. The two
   enrichment flags default False (`super_agent_select_models.py:110-111`); flipping either one moves
   every completeness score in the window.
6. **Arm imbalance and single-label nights.** If most slates are all-HIGH, `ρ_co` collapses and the
   question is not answerable. §5.1's gate decides that **before** lock, on measured counts, and sends
   the question to DEFERRED rather than to a thin run.
7. **Sealed contamination.** The 2026-09-12 weekly read this exact contrast. §6 removes the sealed
   stretch from every verdict; the residual exposure is that a registrar who has seen "78 vs 65" may
   have chosen a design that flatters the negative direction. Mitigations: both primaries are
   **two-sided** with a symmetric MPE, the arms and estimator are inherited from Q027's already-locked
   machinery rather than invented here, and the window is prospective-only.
8. **Regime label.** Point-in-time labels are legal only from 2026-06-09 (FREEZE_v001 §7); the entire
   window is after that date, so the hazard does not apply — stated as a checked property, not an
   assumption. `regime_version` and `data_quality` are printed per night.
9. **Episode dependence (DP-51).** High-completeness names recur on consecutive nights more than
   thin-coverage names, so the same forward path can enter many nights' statistics. The
   episode-clustered CI is registered as a blocker (§8 clause 7), not a footnote.
10. **`d*_t` imported from a different cohort.** Q027 R1(c) measured the published median distance
    moving from ≈ 1.06 to ≈ 2.10 ATR across a single config ship. The inherited zero-survivor
    whole-night exclusion and the 1–2-survivor trailing-median fallback are why; the `d*_t`
    distribution is printed and `eval.py` fails loudly outside `[0.25, 10]` ATR.
11. **Gap-through asymmetry.** If HIGH picks are the ones that run after hours, they will show more
    not-takeable targets at the t+1 open, which *lowers* E1 by construction. That is a real cost of
    the label and is measured (§4.3), but it means a NULL E1 may coexist with a genuine but
    un-takeable edge; the `C_t` sensitivity (DP-11) is printed for exactly this reason and never
    decides.
12. **One database (DP-50).** Every number in this file that is not computed by `eval.py` comes from
    the pinned freeze or the read-only platform repo, never a live query. A repair shipped between
    `manifest_v001` and the successor freezes is checked against `research/data/DATA_NOTES.md` at the
    decision pass and, if it touches `overall_score`, `completeness_score` or publication, splits the
    window at its ship date (DP-50(a), §2.6).
13. **`uoa_symbol_daily.fwd_return_*` is never read** (FREEZE_v001 §5: coverage ≈ 5% of baseline and
    0% for `trading_date ≥ 2026-07-27`). Every outcome here is computed from pinned daily bars.

## 11. Open decisions before lock

1. **Primary population: published slate, or every `threshold_pass` candidate.** — Options: A the
   published slate only (DP-28), with the all-candidate dark-set panel descriptive (§4.3) / B every
   `threshold_pass` row, where all three labels have mass and power is far higher.
   Recommendation: **A**, because the label is only *shown* on the published card
   (`super_agent_select_public.py:212`) and B would test a field no subscriber ever sees while
   duplicating Q027's population exactly. Changes: §2.1, §2.5, §4.3, §5.1.
2. **E2's estimator.** — Options: A adjacent-score-rank discordant pairs as drafted (§4.2) / B a
   Mantel–Haenszel contrast over coarse score strata `[82,88)/[88,100]`.
   Recommendation: **A**, because it needs no caliper chosen by the registrar, contributes on every
   night where both arms exist above 82, and matches each HIGH to the closest-scoring MED the night
   admits; B leaves more residual score inside each stratum. Changes: §4.2, §3 (B2), §8 clause 5.
3. **Lock now behind §5.1's gate, or defer until R1 reports.** — Options: A lock now, with the gate
   table deciding lock-versus-DEFERRED on R1's measured `ρ_co` before the dataset is pinned / B hold
   the draft uncommitted until R1 reports, then lock with the real projection written in.
   Recommendation: **A**, because R1 reads only population counts and no outcome, so nothing it
   returns can shape a hypothesis that is already fixed in writing, and the gate is numeric and
   pre-committed. Changes: §5.1, §5.3, header Status.
4. **The sealed post-hoc panel (§6).** — Options: A print it once, clearly labelled, entering no
   verdict / B omit the sealed stretch entirely.
   Recommendation: **A**, because the 2026-09-12 weekly already published an uncontrolled version of
   this number; replacing it with the same statistic computed on the registered construction, marked
   as carrying no verdict, is better than leaving the loose line as the desk's only record.
   Changes: §6, §4.3.
