# L-Q024 — historical companion protocol: SAS versus simple benchmarks, admitted in-sample history

**INTERNAL / NON_QUOTABLE.** Output label fixed by this protocol: **NOT_ESTIMABLE** (feasibility, §6).
**Status:** PROTOCOL FIXED 2026-09-14, before any computation. **No parquet row was loaded, and no touch rate,
return or arm comparison was computed, to write this file.** Feasibility comes only from existing
Steward/FREEZE reports and manifest metadata.
**Companion of:** `research/questions/Q024_sas_vs_simple_benchmarks/` (PREREG_LOCKED, prereg sha256
`d29193bc…e257`, decision date 2027-05-17). This is a separate learning artefact. It is **not** an
amendment to Q024 and does not use Q024's directory.
**Governing policy:** `research/LEARNING_POLICY.md` §Historical companions; DP-52, DP-55 (principally), DP-56.
Work package: `research/learning/HISTORICAL_COMPANIONS.md` row L-Q024.
**Prepared by:** registrar (desk run 2026-09-14, learning item `LEARN-COMPANIONS`).

---

## Decision paragraph

The admitted history (SAS pick nights up to 2026-05-29) cannot tell the desk anything about whether
**today's** SAS slate beats simple benchmarks. Not one admitted night was produced by the current
engine. The admitted nights do not form one engine: they come from three different engine
configurations. The largest single configuration holds **19 usable nights**, one short of the desk's
20-night cell floor. Two of the six arms also cannot be built legally on most of those nights: the
sector-matched random arm and the equal-weight arm. The companion is therefore
**NOT_ESTIMABLE for the current engine, and for every historical vintage**. That does not support
starting a shadow benchmark comparison **because of history**. Whether to start one has to be
decided on product grounds. The only evidence that can answer the question is prospective: Q024's
locked window, or an internal flag-off shadow panel (§11).

## 0. What this companion can never be

- It can **never** be independent confirmation of Q024, in either direction, and never a replication
  of it. It re-reads history that has already been partly inspected (§4).
- It can **never** open, preview or approximate Q024's outcomes. Q024's population is prospective
  (pick nights ≥ 2026-09-14). Its sealed post-hoc panel (pick nights 2026-07-08..2026-08-12) belongs to
  Q024's own decision pass and is **not admitted here**. No night after 2026-05-29 is loaded as a selection.
- It produces no controller verdict, no p-value, no q-value, no subscriber claim and no scoring or
  publication change (LEARNING_POLICY §Two outputs; DP-52).

## 1. Internal decision it supports

*"Do simple selections deserve an immediate internal shadow comparison against the SAS slate, ahead
of Q024's registered decision?"* The only permitted outputs are: (a) a recommendation about whether
to propose an INTERNAL_TOOL shadow benchmark panel (flag-off, Haci-only, DP-48), and (b) the evidence
card's wording. It cannot license a benchmark row, a "versus alternatives" sentence, or any change
to Q024.

## 2. Inputs — exact whitelist

**Manifests and hashes (read from the manifest JSONs, and from controller state where the file hash is recorded there):**

| artefact | SHA-256 | role |
|---|---|---|
| `research/data/manifest_v001.json` (file) | `b03f355a68373aadd0f2dc56c9154158929642291bf6caacb2f5a9bf15bef374` (as `base_manifest_sha256` in `manifest_prices_v001.json`; the controller pins the same value, e.g. `Q006_control_cohort_path/state.json`) | selections |
| └ table `sas_candidates` → `research/data/v001_sas_candidates.parquet` | `af40ad8a48915f979cf36b0cc4d6526a7e9ecfbd523351ac4d8155b7a0aaa2f2` | |
| └ table `sas_runs` → `research/data/v001_sas_runs.parquet` | `888d6f3be279bacd8fa963899cbdb1e4955449861eb9668757f98bf01e9283ea` | |
| `research/data/manifest_prices_universe_v001.json` (file) | not recorded in any desk artefact as of 2026-09-14; Stage 0 computes and prints it before reading any parquet | bars: history ≥ 60 sessions and forward bars |
| └ table `daily_split` → `research/data/pu001_daily_split.parquet` | `2e654281d480c930d312b294a6ab7035e0d59ec7ba757353760aa0d0ce6afa95` | |
| └ table `daily_raw` → `research/data/pu001_daily_raw.parquet` | `b6dc92c98a1f4556d9478eee1460ddfb959920fdc575beb61f55f97f1d80d100` | split-basis assertions only |
| `research/data/manifest_prices_v001.json` (file) | `73d2a895da7db724a236ea051d81944799135f0fb5fb3f1d022659f2b0c3b655` (controller state, e.g. `Q006_control_cohort_path/state.json`) | cross-check only |
| └ table `prices_daily_split` → `research/data/p001_daily_split.parquet` | `7270c61304c7d4ba3e6708f48fe47f21bbfbffe8a91ebf667c97b495651ff175` | agreement check on overlapping symbol-dates; fails loudly on disagreement |
| `research/data/exclusions_v003.json` | not recorded; Stage 0 prints it | night exclusions |
| `volatilx:data/sp500_sectors.json` at commit `4171b1a` | `c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201` (hash the committed bytes, never the CRLF working tree — DATA_NOTES) | B3 only, and only where knowledge-time legal (§5) |

**Why the universe price freeze is the bar source.** `manifest_prices_v001` starts 2026-01-31. That gives
41 daily bars before 2026-04-01, so Q024 §2.4's "≥ 60 daily bars dated ≤ t" screen (and MOM60, SMA50)
first clears on **2026-04-28**. `manifest_prices_universe_v001` starts 2025-01-02 and carries 431
candidate symbols plus 5 benchmarks (manifest `symbol_counts`). This choice is fixed before any outcome.
It is a data-coverage choice, not a variant.

**Columns:** `sas_candidates`: `trading_date`, `symbol`, `qualified`, `selected_rank`, `overall_score`,
`dominant_direction`, `best_timeframe`, `confidence_level`, `outcome_target_invalid` (exclusion audit
only, as Q024 §2.4), `public_payload_json.lane_plans`, `created_at`. `sas_runs`: `trading_date`,
`finished_at`, `config_json`. Bars: `symbol`, `date`, `o`, `h`, `l`, `c`.

**Never inputs:** `market_regime_daily` (no point-in-time row before 2026-06-09, FREEZE_v001 §7);
`sas_selection_excursion`; every other `outcome_*` column; `level_hit_*`; `uoa_symbol_daily.fwd_return_*`
(degraded from 2026-05-20, FREEZE_v001 §5); the platform's `atr_pct` and `spot_close` (DATA_NOTES, PI-003);
hourly bars; any row of any table dated after 2026-05-29 **as a selection**.

## 3. Admitted selection dates and loading

- **Admitted selections:** `trading_date <= 2026-05-29` (`in_sample_end` in `manifest_v001.json`). They are loaded
  **only** through the existing in-sample helper
  `research/lib/eval_utils.py::load_split(manifest, "in_sample", name=<table>, date_col="trading_date")`,
  for `sas_candidates` and `sas_runs`, before any join.
- **Night exclusions:** `exclusions_v003.json` `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`
  ∪ `uncorroborated_publication_runs.trading_dates`, plus DP-04. Read from the JSON, never hard-coded.
- **Forward bars.** The helper filters selections and has no forward-bar parameter. Bars are therefore admitted
  **only** as (symbol, date) pairs inside `[t−60 sessions, t+20 sessions]` of an admitted selection row, for
  an admitted row's own symbol or a benchmark instrument. Nothing beyond t+20 is loaded, and no bar is
  joined to any selection dated after 2026-05-29. The last admitted night's t+20 is **2026-06-29**. The
  precedent is EXPLORE_001 ("forward paths of in-sample rows only"), applied here with a tighter 20-session bound.

## 4. Prior exposure to this history (frozen does not mean untouched)

| source | what it read on the admitted window | consequence |
|---|---|---|
| `research/reports/explore/EXPLORE_001.md` (2026-09-10) | 328 published in-sample picks / 41 nights, and a 2,282-row unpublished candidate pool; distance-matched touch paths of picks against matched same-night controls (§A "Skill or distance?"), entry timing, path shape, elite 90+ | the SAS arm's in-sample path and the unpublished-pool comparison are already explored; reanalysis adds no independent evidence |
| `research/reports/weekly/2026-09-10.md`, `2026-09-12.md` | absolute W60/W20 direction-adjusted returns and L1/L2 touches for published picks from 2026-04-01, by band, regime × band, lane, source membership and confidence | the SAS arm's absolute in-sample outcome is known. Combined with public knowledge of the April–May tape, that is a partial read on the SPY arm |
| `research/reports/STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md` | counts only, sealed panel 2026-07-08..09-10; no in-sample night | none for outcomes; supplies the arm-computability definitions |
| `research/questions/Q005_elite_thinning/` (LEDGERED, INCONCLUSIVE) | 90+ band publication history 2026-04-01..2026-09-10, April–May included | score-distribution composition over the admitted window has been studied |
| CLAUDE.md standing findings | "directional_pct ≈ base rate", "88–90 underperforms 90+", among others | treated as already-read history |

No desk output has computed a market-relative or momentum-rank-relative number on the admitted window. The
benchmark contrast itself is unread, but its inputs are not.

## 5. Engine versions in the admitted window, and the vintage rule

**Vintage rule (fixed):** a vintage cell is a set of admitted nights sharing one `sas_runs.config_json` tuple:
`scoring_weights`, `timeframe_weight_multipliers`, `enable_fundamental_enrichment`,
`enable_smart_money_enrichment`, presence/values of `atr_elite_*`, `publication_floor` and
`bear_publish_threshold`. It also shares one `score_details_json` schema class (8-key partial or full).
Cells are **never pooled**, and no estimate is ever labelled as describing a vintage other than its own.
`engine_versions_present` in `manifest_v001.json` is empty, so the vintage comes from `config_json` and schema,
as measured in `STEWARD_Q029_feasibility.md` §(b), (c), (d), (f).

| boundary (source) | effect inside the admitted window |
|---|---|
| fundamental enrichment flag False → True from 2026-05-01, reverting on 2026-05-04 (Q029 R1b §(b), §(f)) | splits pre-v1.5 nights into flag-off and flag-on cells |
| v1.5 weight reallocation (technical 20→27, projection 26→29, catalyst 8→10, GEX 12→0) plus ATR-elite cap 84.9/79.9 and full score schema, first clean night 2026-05-18 (R1b §(c), §(d), §(f)) | separates 2026-05-18..05-29 from everything earlier; the transition nights 05-11..05-15 are all `manual_runs` exclusions, so the switch itself is never observed |
| catalyst layer: earnings resolver wrong before 2026-06-01, catalyst a flat 80 (DATA_NOTES, `69ef05f`; exclusions_v003 `catalyst_layer_regime_change`) | every admitted night; no admitted night carries the current catalyst feature |
| single combined bull/bear 8-cap counter before the 2026-07-02 bear-lane split; replay disagrees on 12 April nights (R1b §(e)) | the April published bullish slate is formed by a different publication mechanism |
| `bear_publish_threshold` absent until 2026-06-29; `publication_floor` absent until 2026-07-08 (R1b §(f); STEWARD_Q027 §(g)) | the publication predicate differs from today's on every admitted night; the published cohort's printed L3 distance roughly doubles across the floor ship (STEWARD_Q027 §(c): 1.06 → 2.10 ATR median, sealed segment) |
| `_enforce_ladder_monotonic` shipped 2026-07-06 (DATA_NOTES) | admitted ladders are pre-fix; L3 is the printed swing target, whose monotonicity is not guaranteed |
| `market_regime_daily` backfilled for every date ≤ 2026-06-08 (FREEZE_v001 §7) | no legal regime label on any admitted night; only the SPY `tape_t` proxy is available |
| bear projection library `v20260517-221435` constant (FREEZE_v001 §6) | no split |
| `uoa_symbol_daily.fwd_return_*` freeze from 2026-05-20 (FREEZE_v001 §5) | not an input; no split |
| sector blob `4171b1a` committed 2026-05-17 | B3 (sector-adjusted random) is **knowledge-time legal only on nights ≥ 2026-05-18**; earlier use would need a rule-14 exception, which a companion may not grant |
| RSP absent from both price manifests (STEWARD_Q024 §(d); `manifest_prices_universe_v001` benchmarks = 5) | B2 (equal-weight) is a **missing arm**; no proxy (HISTORICAL_COMPANIONS boundary) |

**Current engine** (the definition this companion would need): the 2026-05-18 weight vector, post-06-01 catalyst,
split bull/bear lanes, `bear_publish_threshold` = 80, `publication_floor` = 80, monotonic ladders. That is,
nights ≥ 2026-07-08.

## 6. Feasibility — counts and metadata only (no outcomes)

**Funnel over admitted sessions (from exclusions_v003, STEWARD_Q029 §(b)/(c)/(f), STEWARD_Q027 Headline):**

| step | nights |
|---|---:|
| trading sessions 2026-04-01..2026-05-29 (April 21, Good Friday 04-03 closed; May 20) | 41 |
| minus `manual_runs` in window (04-02, 04-24, 05-11, 05-12, 05-13, 05-14, 05-15) | **34** (matches `night_counts_after_exclusions.in_sample_to_2026-05-29`) |
| **V-A** pre-v1.5 weights, GEX 12, partial schema, fundamental flag off: the 19 April nights + 05-04 | 20 |
| **V-B** pre-v1.5 weights, GEX 12, partial schema, fundamental flag on: 05-01, 05-05..05-08 | 5 |
| **V-C** 2026-05-18 weight vector, ATR-elite cap, full schema: 05-18..05-29 | 9 |
| minus nights whose published slate carries no `lane_plans` at all, so no swing target and `k_t = 0` (04-01 in V-A, 05-01 in V-B; STEWARD_Q027 Headline) | V-A **19**, V-B **4**, V-C **9** |
| nights produced by the **current engine** | **0** |
| nights where B3 is knowledge-time legal | V-C only (9) |
| nights where B2 (EW) exists | 0 |
| maturity: session t+20 ≤ price horizon (last admitted t+20 = 2026-06-29 ≤ 2026-09-10) | all — maturity costs nothing |
| post-lock nights | not applicable (history) |

Not measured, and not needed for the verdict: per-night bullish `k_t` in-sample, and rank-pool size. Both could
only lower the counts above.

**Estimability threshold (fixed):** a vintage cell is estimable only with **≥ 20 contributing nights**, the rule-6
per-cell floor below which the desk suppresses any cell to counts only. A companion may not report a cell a
registered question would suppress. No pooling across cells.

**Verdict: NOT_ESTIMABLE — for the current engine (0 admitted nights) and for every historical vintage (largest
cell V-A = 19 < 20).** Two further limits bind even on V-A: B3 is illegal there by knowledge time, and B2 does
not exist anywhere. So at most four of Q024's six arms could ever be built on that cell. V-C, the closest vintage
to today, has 9 nights.

**Stage 0 (optional confirmation, counts only).** An `eval.py` for this companion may re-derive the table above
from the whitelisted metadata columns, with no bar loaded. It prints the file hashes it computes. If its
census differs from this table, it stops, and the difference is recorded in `REPORT.md`; this protocol is not
edited. **Stage 1 (outcomes) runs only if Stage 0 finds a cell with ≥ 20 contributing-eligible nights on which
every built arm is knowledge-time legal.** On the reports above, Stage 1 is not expected to run.

## 7. Comparison, endpoint, entry and target distance (fixed; applies only if Stage 1 runs)

Adopted from Q024 PREREG §2.2–§4, **restricted to one vintage cell**:

- **Publication predicate:** `qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28), `dominant_direction =
  'bullish'`; `k_t` as published.
- **Entry:** session t+1 regular-session open (DP-03(b)). **Target:** `L3 = lane_plans.swing_trading.targets[0]`;
  `d_p = (L3 − C_t)/ATR14` from split bars ≤ t; arm target `C_{t,m} × (1 + d_p × atr_pct_m)`.
- **Endpoint:** first touch within t+1..t+20 (`high ≥ target`); a target already through the t+1 open is not a hit.
  No stop.
- **Comparison:** `D_{a,t} = mean_p HIT_p − mean_p rate_a(d_p)` for arms SPY, MOM20, MOM60, TECH (Q024 §3 B1, B4–B6),
  plus SECRAND on knowledge-time-legal nights only. EW is printed as a **missing arm**.
- **Screens and missingness (each counted, never imputed):** Q024 §2.4 (no swing target; target invalid or wrong
  side; price-scale screen `[0.5, 2.0]` / 12 ATR; < 60 bars; missing t+1 open; ungradeable).
- **Feature knowledge time:** every selection, rank and distance input comes from rows and bars dated ≤ t. Bars
  after t are used only for entry and touch.
- **Stratification:** SPY `tape_t` (Q024 §6 definition). Every cell below 20 nights is SUPPRESSED, and "holds across
  regimes" is stated as untestable on a single tape.
- **Not computed:** the clause-7 money gate, fixed-horizon panels, and 40/60-session windows. Adding any of them is a variant (§10).

## 8. Uncertainty and dependence (fixed)

Stationary block bootstrap over the ordered contributing nights: expected block length 10 sessions, 2,000
resamples, seed `20260909` (`eval_utils.SEED`), 95% percentile interval, **descriptive only**. Dependence assumed:
consecutive nights share overlapping 20-session windows (serial dependence, which the block bootstrap addresses);
same-night picks share the market factor (absorbed by the night aggregation); symbols recur across nights (**not**
absorbed, stated as a limitation). With < 80 nights from one tape, the interval is not a precision statement.
**No p-value, no q-value, no verdict language.**

## 9. Output label, report form, permitted use, review

- **Label:** `NOT_ESTIMABLE` (current engine and all vintages). A card citing it carries the MECHANICAL label,
  because the finding is a lineage/coverage fact. If Stage 1 ever ran on a qualifying cell, its output would be
  `EXPLORATORY — RETIRED ENGINE VINTAGE <cell>`, never a statement about the current engine.
- **Report:** `research/learning/L-Q024/REPORT.md`, due by 2026-09-28 (two weeks, LEARNING_POLICY). It leads
  with the internal decision and this feasibility answer, with every limitation above. It never uses
  `research/questions/Q024_*/results/`.
- **Permitted internal use:** evidence-card wording for Q024, and the shadow-panel recommendation in §11.
  Nothing else.
- **Review of interpretation:** the Red Team reads `REPORT.md` before any card cites it. The Reporter's card keeps
  `as_of` at the report's observation date.

## 10. Variants register

Every analysis variant examined is recorded here with its date, what changed, why, and whether it was chosen
before or after any outcome was seen. **Empty as of 2026-09-14.**

| id | date | variant | reason | before/after outcomes | where reported |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 11. What would resolve the question instead

- **Q024's own prospective window** (pick nights 2026-09-14..2027-04-07; decision 2027-05-17), unchanged.
- **An internal flag-off shadow benchmark panel** (Q024 §9's INTERNAL_TOOL candidate). Scope: nightly SAS
  bullish slate against SPY, MOM20, MOM60 and TECH at the slate's own ATR distances, logged prospectively, with
  version stated and a rollback of "turn it off". It may be proposed through the enhancement channel. It cannot
  feed Q024's verdict, and it cannot be read before Q024's decision date in any way that changes Q024.
- **RSP pinnability** (Q024 R2's first action) settles the EW arm prospectively. History cannot.
