# L-Q027 — historical companion protocol: does the score order price paths, admitted in-sample history

**INTERNAL / NON_QUOTABLE.** Output label fixed by this protocol: **NOT_ESTIMABLE** (feasibility, §6).
**Status:** PROTOCOL FIXED 2026-09-14, before any computation. **No parquet row was loaded, and no touch rate,
rank correlation, return or score–outcome relation was computed, to write this file.** Feasibility comes only
from existing Steward/FREEZE reports and manifest metadata.
**Companion of:** `research/questions/Q027_score_ranking_validity/` (PREREG_LOCKED, prereg sha256
`6b76aaf8…26d4`, decision date 2027-04-12). This is a separate learning artefact. It is **not** an amendment to
Q027 and does not use Q027's directory.
**Governing policy:** `research/LEARNING_POLICY.md` §Historical companions; DP-52, DP-55 (principally), DP-56.
Work package: `research/learning/HISTORICAL_COMPANIONS.md` row L-Q027.
**Prepared by:** registrar (desk run 2026-09-14, learning item `LEARN-COMPANIONS`).

---

## Decision paragraph

History up to 2026-05-29 cannot say whether **today's** SAS score ranks stocks by how well their price paths
turn out. The score being ranked was produced by a different formula on every admitted night. Before
2026-05-18, GEX carried 12 points and technical, projection and catalyst carried less. After that date there
are only 9 admitted nights. The catalyst layer was a flat 80 throughout. The largest single-formula group holds
**19 usable nights**, one short of the desk's 20-night cell floor. The companion is
**NOT_ESTIMABLE for the current engine, and for every historical vintage**. It gives no historical support for
or against the ranking hypothesis. The desk should keep treating "the score is a precise ranking" as
**untested**. Q027's prospective window is the only admissible answer.

## 0. What this companion can never be

- It can **never** be independent confirmation of Q027, in either direction, and never a replication of it.
  The admitted history's top band has already been read against outcomes (§4).
- It can **never** open, preview or approximate Q027's outcomes. Q027's verdict window is prospective (pick
  nights ≥ 2026-09-15). Its sealed post-hoc panel (2026-06-01..2026-08-12) belongs to Q027's own decision pass
  and is **not admitted here**. No night after 2026-05-29 is loaded as a selection.
- No controller verdict, no p-value, no q-value, no subscriber claim, no scoring or ranking change (DP-52).
- It never tests H-075's per-layer ICs (that is L-Q029 / Q029), and never Q024's slate contrast.

## 1. Internal decision it supports

*"Does historical score ordering warrant prioritising the ranking hypothesis?"* That is, should the desk keep
presenting the score internally as a meaningful ordering while Q027 runs, or flag it as unsupported? The only
permitted outputs are evidence-card wording for Q027 and a recommendation on whether any instrumentation is
needed (§11). It cannot license a band-level claim, a threshold change or a conviction-label change.

## 2. Inputs — exact whitelist

**Manifests and hashes (read from the manifest JSONs, and from controller state where the file hash is recorded there):**

| artefact | SHA-256 | role |
|---|---|---|
| `research/data/manifest_v001.json` (file) | `b03f355a68373aadd0f2dc56c9154158929642291bf6caacb2f5a9bf15bef374` (as `base_manifest_sha256` in `manifest_prices_v001.json`; controller state, e.g. `Q006_control_cohort_path/state.json`) | selections |
| └ `sas_candidates` → `research/data/v001_sas_candidates.parquet` | `af40ad8a48915f979cf36b0cc4d6526a7e9ecfbd523351ac4d8155b7a0aaa2f2` | |
| └ `sas_runs` → `research/data/v001_sas_runs.parquet` | `888d6f3be279bacd8fa963899cbdb1e4955449861eb9668757f98bf01e9283ea` | |
| `research/data/manifest_prices_universe_v001.json` (file) | not recorded in any desk artefact as of 2026-09-14; Stage 0 computes and prints it before reading any parquet | bars: ≥ 60-session history and forward bars |
| └ `daily_split` → `research/data/pu001_daily_split.parquet` | `2e654281d480c930d312b294a6ab7035e0d59ec7ba757353760aa0d0ce6afa95` | |
| └ `daily_raw` → `research/data/pu001_daily_raw.parquet` | `b6dc92c98a1f4556d9478eee1460ddfb959920fdc575beb61f55f97f1d80d100` | split-factor snapping only |
| `research/data/manifest_prices_v001.json` (file) | `73d2a895da7db724a236ea051d81944799135f0fb5fb3f1d022659f2b0c3b655` (controller state) | cross-check only |
| └ `prices_daily_split` → `research/data/p001_daily_split.parquet` | `7270c61304c7d4ba3e6708f48fe47f21bbfbffe8a91ebf667c97b495651ff175` | agreement check on overlapping symbol-dates; fails loudly on disagreement |
| `research/data/exclusions_v003.json` | not recorded; Stage 0 prints it | night exclusions |

**Why the universe price freeze.** `manifest_prices_v001` begins 2026-01-31: 41 bars before 2026-04-01, so Q027
§2.4's ≥ 60-bar row screen first clears on 2026-04-28 and would delete most of April by construction.
`manifest_prices_universe_v001` starts 2025-01-02 and covers 431 candidate symbols. Fixed before any outcome;
not a variant.

**Columns:** `sas_candidates` (every row, published or not): `trading_date`, `symbol`, `overall_score`,
`dominant_direction`, `qualified`, `selected_rank`, `conflict_penalty`, `best_timeframe`, `confidence_level`,
`public_payload_json.lane_plans` and `.analysis_status` (published rows, for `d*_t` and the zero-lane-plan
signature), `score_details_json` (**key presence only**, for the schema class), `created_at`. `sas_runs`:
`trading_date`, `finished_at`, `config_json`. Bars: `symbol`, `date`, `o`, `h`, `l`, `c`.

**Never inputs:** `market_regime_daily` (not point-in-time before 2026-06-09); `sas_selection_excursion`;
`outcome_*`; `level_hit_*`; `uoa_symbol_daily.fwd_return_*`; the platform's `atr_pct` / `spot_close`; hourly
bars; the seven layer subscores (L-Q029's subject, not this one's); any selection row dated after 2026-05-29.

## 3. Admitted selection dates and loading

- **Admitted selections:** `trading_date <= 2026-05-29` (`in_sample_end`, `manifest_v001.json`). They are loaded
  **only** through `research/lib/eval_utils.py::load_split(manifest, "in_sample", name=<table>,
  date_col="trading_date")` for `sas_candidates` and `sas_runs`, before any join.
- **Night exclusions:** `exclusions_v003.json` (`manual_runs` ∪ `non_session_runs` ∪
  `uncorroborated_publication_runs`), DP-04, and Q027's **zero-lane-plan criterion** (every published row
  `analysis_status = "disabled"` or without `lane_plans`; Q027 §2.4 `payload_disabled_runs`), applied here as a
  criterion, since no successor exclusions file covers the admitted window.
- **Forward bars:** admitted only as (symbol, date) pairs inside `[t−60 sessions, t+20 sessions]` of an admitted
  candidate row, for that row's symbol, plus SPY for `tape_t`. Nothing beyond t+20 is loaded. The last admitted t+20
  is 2026-06-29. No bar is joined to a selection dated after 2026-05-29 (EXPLORE_001 precedent, tighter bound).

## 4. Prior exposure to this history (frozen does not mean untouched)

| source | what it read on the admitted window | consequence |
|---|---|---|
| `research/reports/weekly/2026-09-10.md`, `2026-09-12.md` | W60/W20 returns of published picks from 2026-04-01 **by score band** and regime × band. Q027 §1/§6 record that they showed the 90+ band's lead as an April–May effect | the top of the score distribution in exactly this window has been read against outcomes; E2's top tercile and any band output live there |
| `research/reports/explore/EXPLORE_001.md` §F | elite 90+ in-sample (21 picks / 17 nights; analysis sample 15 / 13), on the path lens | same |
| CLAUDE.md standing findings | "88–90 band underperforms 90+"; "champion symbols graded below base rate" | same |
| `research/questions/Q005_elite_thinning/` (LEDGERED, INCONCLUSIVE) | 90+ publication history 2026-04-01..2026-09-10 | score-distribution composition studied |
| `research/reports/STEWARD_Q027_exposure.md` | counts only on 2026-06-01..09-10. R1(c) notes 40 nights of direct `d*_t` back to 2026-04-01 (a payload distance, not an outcome) | none for outcomes; establishes the `d*_t` level shift |

The candidate-level IC over **all** candidates has not been computed on the admitted window by any desk output.
Published-only band reads have been, and they are range-restricted (HISTORICAL_COMPANIONS boundary).

## 5. Engine versions in the admitted window, and the vintage rule

**Vintage rule (fixed):** a cell is a set of admitted nights sharing one `sas_runs.config_json` tuple
(`scoring_weights`, `timeframe_weight_multipliers`, enrichment flags, presence/values of `atr_elite_*`,
`publication_floor`, `bear_publish_threshold`) and one `score_details_json` schema class. **The ranking variable
is the stored `overall_score`, so a formula change is a change of the thing being tested.** Cells are never
pooled. `engine_versions_present` in `manifest_v001.json` is empty, so the vintage comes from config and
schema (`STEWARD_Q029_feasibility.md` §(b)–(f)).

| boundary (source) | effect on the ranking variable inside the admitted window |
|---|---|
| fundamental enrichment off → on from 2026-05-01, off again on 2026-05-04 (R1b §(b), §(f)) | the fundamental layer's weight enters or leaves the blend |
| v1.5 reallocation 20/26/8/12 → 27/29/10/0 (technical/projection/catalyst/GEX), ATR-elite cap 84.9/79.9, GEX-missingness +5 offset, full score schema; first clean night 2026-05-18 (R1b §(c), §(d)) | a different weighting of the same subscores, a cap at the top, and a +5 shift for GEX-missing rows. Rank order changes at every level. Transition nights 05-11..05-15 are excluded |
| catalyst flat 80 before 2026-06-01 (DATA_NOTES `69ef05f`; R1b §(a): catalyst has zero within-night variance on 34 of 102 whole-freeze nights, all segment nights non-zero, i.e. **every admitted night is flat**) | the catalyst layer adds no within-night ordering on any admitted night; today it does |
| `publication_floor` absent until 2026-07-08; `bear_publish_threshold` absent until 2026-06-29 (STEWARD_Q027 §(g)) | `d*_t` is taken from a differently gated published cohort. Across the floor ship the median `d*_t` doubles, 1.06 → 2.10 ATR (§(c), sealed segment), so an admitted-night target distance is a different experiment |
| combined bull/bear lane counter before 2026-07-02 (R1b §(e)) | changes which rows are "published", and so `d*_t`'s cohort |
| ladders non-monotonic before 2026-07-06 (DATA_NOTES) | `L3` feeds `d*_t` |
| regime labels backfilled ≤ 2026-06-08 (FREEZE_v001 §7) | no legal regime stratum; `tape_t` only |
| `uoa_symbol_daily.fwd_return_*` freeze from 2026-05-20 | not an input; no split |
| earnings dates wrong before 2026-06-01 (DATA_NOTES) | no earnings-phase stratum is computable |

**Current engine** for this question: the 2026-05-18 weight vector with the post-06-01 catalyst, and `d*_t` from
the post-2026-07-08 published cohort. That is, nights ≥ 2026-07-08.

## 6. Feasibility — counts and metadata only (no outcomes)

| step | nights |
|---|---:|
| trading sessions 2026-04-01..2026-05-29 | 41 |
| minus `manual_runs` in window (04-02, 04-24, 05-11..05-15) | **34** (matches exclusions_v003 `in_sample_to_2026-05-29`) |
| **V-A** pre-v1.5 formula, GEX 12, fundamental off, partial schema: the 19 April nights + 05-04 | 20 |
| **V-B** pre-v1.5 formula, GEX 12, fundamental on: 05-01, 05-05..05-08 | 5 |
| **V-C** 2026-05-18 formula, ATR-elite cap, GEX offset, full schema: 05-18..05-29 | 9 |
| minus zero-lane-plan nights (04-01 → V-A; 05-01 → V-B; STEWARD_Q027 Headline) | V-A **19**, V-B **4**, V-C **9** |
| nights produced by the **current engine** (formula + catalyst + `d*_t` cohort) | **0** |
| nights with the current formula but flat catalyst and pre-floor `d*_t` (closest vintage) | 9 |
| maturity (last t+20 = 2026-06-29 ≤ 2026-09-10) | all mature |
| rows per night: `sas_candidates` averages about 55 rows per in-sample night (EXPLORE_001 Samples: 2,282 rows / 41 nights). The ≥ 30-eligible-row gate is not expected to bind, but it is unmeasured per night | — |

**Estimability threshold (fixed):** ≥ 20 contributing nights in one vintage cell (rule-6 per-cell floor). No pooling.

**Verdict: NOT_ESTIMABLE — for the current engine (0 admitted nights) and for every historical vintage (largest
cell V-A = 19 < 20).** Even if V-A had reached 20, its result would describe a retired formula with GEX at 12,
no fundamental layer and a flat catalyst, measured at a distance drawn from a pre-floor cohort. HISTORICAL_COMPANIONS
forbids implying validity for today's engine from that.

**Stage 0 (optional, counts only):** re-derive the table from whitelisted metadata with no bar loaded, printing the
computed hashes. If it disagrees with this table, it stops and the disagreement is recorded in `REPORT.md`; this
protocol is not edited. **Stage 1 runs only if Stage 0 finds a cell with ≥ 20 contributing-eligible nights**, and
is not expected to run.

## 7. Comparison, endpoint, entry and target distance (fixed; applies only if Stage 1 runs)

Adopted from Q027 PREREG §2.1–§2.5 and §4.1, **restricted to one vintage cell**:

- **Population:** every scored `sas_candidates` row, published or not; `dominant_direction IN ('bullish','bearish')`
  (mixed excluded and counted, with share per score decile); ≥ 60 split bars ≤ t; gradeable t+1..t+20.
- **Publication predicate** (for `d*_t` only): `qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28);
  split-scale screen `[0.85, 1.15]` / 20 ATR; 1–2 survivors → trailing-20-night median **within the same cell**
  (not available → night excluded and counted).
- **Entry:** t+1 open. **Target:** `T_i = C_i × (1 + dir_i × d*_t × ATR_i/C_i)`. **Clock:** 20 sessions. Already
  through at entry = not a hit. No stop.
- **Endpoints (descriptive):** `IC_t` = Spearman ρ(`overall_score`, path rank `u_i`), and `G_t` = top − bottom
  score-tercile touch rate. Each is averaged over contributing nights (≥ 30 eligible rows, both terciles non-empty).
- **Comparison / scale reference:** the same statistics with `mom20` in place of the score (Q027 §3 B3). No
  within-night shuffle p-value is produced.
- **Missingness:** every row and night excluded is counted by reason; nothing is imputed.
- **Feature knowledge time:** score, direction, publication and payload come from 16:05 ET rows; ATR, `mom20` and
  `tape_t` from bars ≤ t. Bars after t are for entry and touch only. Terciles and episodes are frozen before any
  forward bar is read.
- **Strata:** SPY `tape_t` (Q027 §6, expanding cut points from 2026-03-02); cells < 20 SUPPRESSED; regime
  untestable on a single tape.
- **Not computed:** band secondary, conflict-penalty stratum, C_t basis, 40-session companion. Adding any of them is a variant (§10).

## 8. Uncertainty and dependence (fixed)

Two descriptive 95% intervals, both printed, neither called significance. (i) **Date-clustered bootstrap** over
contributing nights, with a stationary block bootstrap (expected block length 10) beside it. (ii) **Episode × night
bootstrap** (DP-51; episode = one symbol's run of appearances with gaps ≤ 10 sessions). Both use 2,000 resamples,
seed `20260909` (`eval_utils.SEED`). Dependence assumed: overlapping 20-session windows on consecutive nights
(serial), a shared market factor within night (absorbed by per-night statistics), and heavy symbol recurrence
(STEWARD_Q027 §(e): 70% of symbols recur across episodes on the sealed stretch; assumed similar in-sample). With
< 80 nights from one strong tape, neither interval is a precision statement. **No p-value, no q-value, no verdict language.**

## 9. Output label, report form, permitted use, review

- **Label:** `NOT_ESTIMABLE` (current engine and all vintages). A card citing it uses MECHANICAL, because the
  finding is a lineage fact. Any hypothetical Stage-1 output would be labelled
  `EXPLORATORY — RETIRED ENGINE VINTAGE <cell>` and could not mention the current engine.
- **Report:** `research/learning/L-Q027/REPORT.md`, due by 2026-09-28. It leads with the decision paragraph and
  every limitation, and never uses `research/questions/Q027_*/results/`.
- **Permitted internal use:** Q027 evidence-card wording; the instrumentation note in §11.
- **Review of interpretation:** the Red Team reads `REPORT.md` before any card cites it.

## 10. Variants register

Every analysis variant examined is recorded here with date, change, reason and whether it was chosen before or
after any outcome was seen. **Empty as of 2026-09-14.**

| id | date | variant | reason | before/after outcomes | where reported |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 11. What would resolve the question instead

- **Q027's prospective window** (pick nights 2026-09-15..2027-03-05; decision 2027-04-12), unchanged. It is the
  first data on which the current formula, catalyst and publication floor all coexist without prior reads.
- **No new historical admission can help.** The only nights produced by today's engine (≥ 2026-07-08) are
  sealed and have already been read against band-level outcomes (Q027 §6).
- **Instrumentation worth noting (not proposed here):** `super_agent_select_runs` is updated in place with no
  append-only run history (DATA_NOTES), which is why re-run nights are unrecoverable rather than merely
  excluded. An append-only run/candidate history would protect future vintage splits. It is a brief-writer
  item if Haci wants it.
