# STEWARD_Q027_exposure.md — R1 (counts only), Q027 score_ranking_validity

**Request:** Q027 (`research/questions/Q027_score_ranking_validity/`) DECISIONS.md, "data-steward — R1
(counts only) — BLOCKING for lock", plus the Decision-maker's routing note. Counts only, no outcome of
any kind: no touch, no first-touch date, no return, no excursion, no `outcome_*` column, no
`sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`, no score-vs-outcome cross-tab. Forward
bars read only to prove a bar exists (gradeability accounting), never for a value. Frozen data only —
`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json` against
`research/data/exclusions_v003.json`, plus read-only `git log`/`git show` against the pinned platform
repository — never a live query (DP-50(c)).

**Population:** every row in `sas_candidates`, published or not, regardless of `qualified` /
`threshold_pass`, pick nights **2026-06-01..2026-09-10**, with `exclusions_v003.json` nights and DP-04
late-`finished_at` nights removed. **Denominator for every rate = elapsed sessions**, exclusions **not**
pre-removed (Q019/Q022/Q023 convention).

**Elapsed sessions in window:** N = **71** (2026-06-01..2026-09-10), cross-validated between `sas_runs`
(71 rows) and the SPY daily-bar calendar in `manifest_prices_v001` (71 dates) — they agree exactly.

**Nights excluded from the population (3):** `2026-06-26` (`uncorroborated_publication_runs`),
`2026-07-02` (`manual_runs`), `2026-07-06` (`manual_runs`). DP-04 late-`finished_at` check (every
`sas_runs.finished_at` in-window vs. the next session's 09:30 ET / 13:30 UTC open): exactly one night
fails, `2026-07-06` — already excluded via `manual_runs`, so DP-04 adds **0** incremental nights.
Non-excluded nights: **68**.

---

## Headline

- **Measured contributing-night rate (§2.5's complete definition — matured to t+20, ≥ 30 eligible rows,
  a defined `d*_t`): 48 / 71 elapsed sessions = 0.6761/session.** This clears the **0.36** DEFERRED gate
  by **88%**. **Q027 LOCKS**, not DEFERRED, on this measurement.
- This 0.6761 is **bound to the price freeze's own forward-bar horizon** (last date 2026-09-10), which
  lets only 48 of the window's 68 non-excluded nights mature to t+20 at all (2026-06-01..2026-08-12
  matured; 2026-08-13..2026-09-10, 20 nights, immature — a freeze-horizon artifact, not a screening
  failure). The informative upper bound — eligible nights before the maturity cut (direction + ≥ 60-bar
  screens only, no gradeability/maturity check) — is **68/71 = 0.9577/session**, with **100% (48/48)** of
  the nights old enough to test converting to contributing. I report the stricter, directly-measured
  0.6761 as the schedule basis, not the extrapolation (DP-50(c); dates move out only).
- **By month, the 0.6761 figure is entirely a maturity artifact:** June 20/21 = 0.952, July 20/22 =
  0.909, August 8/21 = 0.381 (only 8 of August's nights had matured by the 2026-09-10 freeze date),
  September 0/7 (entirely immature). The eligible-night proxy is ≥ 0.91/session in every month measured.
- **Schedule at the measured rate (moves OUT from the PREREG's provisional schedule, which borrowed
  Q023's 0.9538 — DP-43, DP-45):** window 2026-09-15..**2027-03-05** (119 elapsed sessions, Floor A
  binds), decision date **Monday 2027-04-12** (was provisionally 2027-03-08); single DP-13 extension if
  needed, window end **2027-04-19** (149 sessions), decision date **Monday 2027-05-24** (was
  provisionally 2027-04-19). Both **inside DP-43's 12-month ceiling** (2026-09-14 + 12mo = 2027-09-14):
  6.9 months and 8.3 months from lock respectively.
- **Sub-cell suppression list, measured from R1(d)/(e) at the window-end projection (119 sessions):**
  contrary to the PREREG's own stated expectations, the **≥ 90 candidate-level band clears 20**
  (projects to 28.5, because R1(d) measures the larger all-candidates population Q027 actually uses, not
  the published-elite rate the PREREG's expectation cited), and **bear-only clears 20** (projects to
  80.4, because candidate-level bearish rows appear on every one of the 48 measured nights — the 0.157
  BACKLOG/H-062 figure the PREREG cites is a *published*-bear rate from a different, narrower population
  and does not transfer). **5 of the 6 `tape_t` cells project below 20** (only `up_mid` clears, at 30.2);
  the `market_regime` `bearish`/`neutral`/`risk_off` labels are **structurally absent** — 0 of 48 nights,
  not merely thin (echoes `STEWARD_Q023_exposure.md` §1/§8). Full table in the Sub-cell section below.
- **DP-50(a)/(b) commit sweep since `fa70688`, over the three named SAS scoring/models/conviction-card
  files: NONE.** 4 commits exist between `fa70688` and HEAD (`d19c9a9`), none touching those three files
  (detail in (g)). **But** `sas_runs.config_json` itself shows two in-window changes the code sweep alone
  would miss: `publication_floor` (null → 80.0, effective the 2026-07-08 run) and `bear_publish_threshold`
  (null → 80.0, effective the 2026-06-29 run) — both already logged in `DATA_NOTES.md` (the
  ladder-monotonicity entry, 2026-09-13). Per DECISIONS item 12 neither is a window-split trigger (they
  gate *publication*, not *scoring*) — but the measured `d*_t` series **does** show a real level shift
  coincident with the `publication_floor` ship: median ≈ 1.05–1.09 ATR on the 21 pre-2026-07-08 nights
  vs. ≈ 2.10 ATR on the 46 nights from 2026-07-08 on — see (c).
- **New finding, flagged and not resolved here:** `2026-06-02`'s entire published slate (8/8 rows) has
  **no `lane_plans` at all** in `public_payload_json` (`analysis_status="disabled"`); that night's own
  `sas_runs.config_json` independently shows two enrichment enable-flags off. The identical signature
  recurs on `2026-04-01`, `2026-05-01`, and `2026-07-02` (the last already excluded via `manual_runs`) —
  all four are the first published night of a calendar month. `2026-06-02` is **not** currently in
  `exclusions_v003.json`. This does not change the lock-or-DEFER call (the night still has 42 eligible
  candidate rows and a fallback-derived `d*_t`, so it counts as contributing either way) — flagging for
  the registrar/red-team, not adjudicating it here.
- No `outcome_corrections` row in-window touches `overall_score`, `conflict_penalty` or
  `dominant_direction` (0 of 125 `sas_candidates`-table corrections) — confirmed zero across the *entire*
  frozen history, not just this window. No repair rewrote the column Q027 ranks on. §10 threat 8 is
  clean on this manifest.

---

## (a) The §2.1/§2.4 funnel

### Step-by-step, whole period (68 non-excluded nights)

| step | rule | rows surviving | dropped |
|---|---|---:|---:|
| 0 | scored (`overall_score IS NOT NULL`) | 4,020 | — |
| 1 | `dominant_direction IN ('bullish','bearish')` | 3,588 | 432 (mixed, 10.75%) |
| 2 | ≥ 60 split-adjusted daily bars dated ≤ t | 3,588 | 0 |
| 3a | matured to t+20 (session t+20 ≤ 2026-09-10, the freeze's own last date) | 2,464 rows / 48 nights | 1,124 rows / 20 nights (immature — freeze-horizon artifact) |
| 3b | gradeable (bars cover t+1..t+20 with no gap), matured rows only | **2,459** | 5 (all CTRA — see CTRA scan below) |

**Eligible rows = 2,459**, all on the 48 matured nights. Every one of the 68 non-excluded nights already
clears ≥ 30 rows at step 2 (min 39, median 55, max 64) — the maturity screen (step 3a), not the row-count
floor, is what actually removes nights from the contributing set.

By month (step 0 → step 1 → step 2, identical after step 1):

| month | step 0 | step 1 (dir screen) | dropped mixed |
|---|---:|---:|---:|
| 2026-06 | 1,009 | 878 | 131 |
| 2026-07 | 1,252 | 1,116 | 136 |
| 2026-08 | 1,330 | 1,202 | 128 |
| 2026-09 (partial, 1-10) | 429 | 392 | 37 |

**Eligible rows per night (min/median/max), among the 48 matured nights: 39 / 51 / 64** (mean 51.2). By
month: June (20 nights) 39/43.5/49; July (20 nights) 47/57.5/63; August (8 nights) 54/58/64.

**CTRA truncated-history scan** (repeated per `STEWARD_Q023_exposure.md` §6 / `STEWARD_Q024_…` (b)):
reproduced exactly. CTRA's last daily bar in `manifest_prices_v001` is **2026-05-06**; it keeps appearing
as a `sas_candidates` row (bullish, never qualified) through **2026-09-10**. It carries ≥ 60 *prior* bars
at every appearance (so it survives step 2), but fails **gradeability** the moment a matured night needs
its t+1 bar: exactly the 5 rows dropped at step 3b (2026-06-04, 06-05, 06-11, 06-17, 06-25 — the CTRA
appearances on matured nights; its later appearances, 2026-08-20 onward, sit on immature nights not yet
testable). No other symbol shows this signature in-window.

**Contributing nights (§2.5, the arm-independent floor): 48 of 71 elapsed sessions = 0.6761/session.**
Every one of the 48 matured nights clears both the ≥ 30-eligible-row floor and has a defined `d*_t`
(47 directly, 1 via the trailing-median fallback — see (c)); no night is dropped for either reason.

**Eligible-night rate before the maturity cut** (screens 0-2 only, informative upper bound, not the
schedule basis): 68/71 = **0.9577/session**.

---

## (b) `mixed`-direction share

**Overall: 432/4,020 = 10.75%** of scored rows.

**Per score decile** (deciles of `overall_score` over all 4,020 scored rows, decile 0 = lowest):

| decile | score range | n | mixed | share |
|---|---|---:|---:|---:|
| 0 | 26.77–45.02 | 402 | 236 | **58.7%** |
| 1 | 45.03–51.42 | 402 | 130 | **32.3%** |
| 2 | 51.43–57.07 | 402 | 52 | **12.9%** |
| 3 | 57.08–62.16 | 402 | 14 | 3.5% |
| 4–9 | 62.17–93.31 | 2,412 | 0 | 0.0% |

Confirms §10 threat 3's concern directly: `mixed` is concentrated entirely in the bottom 3-4 deciles and
is literally zero from decile 4 up.

**Nights above the 25% mixed threshold (whole-night exclusion rule): 0 of 68.** Per-night mixed share:
min 3.2%, median 9.7%, max **23.5%** — no night crosses the line, so this exclusion rule fires **zero**
times over the measured window.

**Nights above the 10% ungradeable threshold: 0 of 48 matured nights.** The only gradeability failures
are the 5 CTRA rows (one per night, across 5 distinct matured nights), each ≤ 1/39 = 2.6% of that night's
eligible pool — far under 10%.

---

## (c) The `d*_t` series

**Published rows (`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28) in-window: 550, across all
68 non-excluded nights** (every night publishes at least 1).

Split-scale payload screen (`lane_plans.day_trading.entry / C_t` outside [0.85, 1.15], or any flattened
lane level implying > 20 ATR from `C_t`, dir-adjusted; ATR = desk-computed ATR14, `C_t` from
`prices_daily_split`, never `atr_pct`/`spot_close` — PI-003):

| reason | rows |
|---|---:|
| survives (used for `d_L3`) | 522 |
| fails split-scale screen (entry ratio **and** a flattened level > 20 ATR, jointly, every time) | 20 |
| no `lane_plans` at all in `public_payload_json` | 8 (all on 2026-06-02 — see Headline) |

**Nights with ≥ 3 screened survivors: 67 of 68.** The one exception is **2026-06-02** (0 survivors, all
8 published picks lack `lane_plans`). A trailing-20-night fallback **is** available for it: the 40 nights
with direct, screened `d*_t` going back to 2026-04-01 in this same manifest give a well-defined trailing
median (2026-05-04..2026-06-01 alone supplies 20). **0 nights would be excluded outright** for lacking
both a direct measurement and a fallback.

**`d*_t` distribution (median `d_L3` per night, 67 direct-measurement nights):** min 0.679, p25 1.266,
median 1.849, p75 2.174, max 3.701 (all ATR units). **0 nights fall outside the eval script's [0.25, 10]
ATR fail-loud bound.**

**By direction** (per-night median among screened survivors): bullish (67 nights) mean 1.80, median
1.86; bearish (12 nights with ≥ 1 screened bearish published pick) mean 2.02, median 2.09.

**Level shift coincident with the `publication_floor` ship (see (g)):**

| segment | nights | median `d*_t` (ATR) | mean |
|---|---:|---:|---:|
| < 2026-06-29 (no `bear_publish_threshold`, no `publication_floor`) | 17 | 1.063 | 1.088 |
| 2026-06-29..2026-07-07 (`bear_publish_threshold` live, `publication_floor` not yet) | 4 | 0.983 | 1.114 |
| ≥ 2026-07-08 (both live) | 46 | **2.100** | **2.107** |

The night's common ATR distance roughly **doubles** the same week `publication_floor` goes live. This is
recorded per DECISIONS item 12 ("it changes `d*_t`'s source cohort... the `d*_t` series is printed across
the ship date") and is a fact about the measured cohort, not a scoring change — no verdict follows from
it here.

---

## (d) Score-resolution panel

**Score IQR per night** (all 68 non-excluded nights): min 13.48, p25 22.28, median 25.04, p75 26.88, max
34.14. No night has IQR = 0; every night's ranking has some resolution.

**ATR-elite cap (exactly 84.9 bullish / 79.9 bearish):** **2 of 4,020 population rows (0.05%)**, both at
79.9, both in-window. Across the **entire** frozen manifest (all 6,479 rows, any date, published or not):
still only 2 rows at 79.9, **0** at 84.9, and **0 of the 907 published rows in the whole manifest
history** sit at either cap. §10 threat 2's stated concern is **not observed as a candidate-level
clustering signature** in this manifest — measured directly, not assumed.

**Null `gex_alignment_score` share: 0.99% (40 of 4,020)** overall; per-night share min 0%, median 0%, max
5.0%. Not the "large share of rows" §10 threat 2 anticipates for the +5 GEX-missingness offset — again,
measured, not assumed.

**Band composition, candidate level, full population (4,020 scored rows, all 68 nights):**

| band | rows | share |
|---|---:|---:|
| < 70 | 2,206 | 54.88% |
| 70-80 | 825 | 20.52% |
| 80-85 | 880 | 21.89% |
| 85-90 | 86 | 2.14% |
| ≥ 90 | 23 | 0.57% |

**Band composition, eligible-row basis (the 48 contributing nights, 2,459 rows) — nights-with-≥-1-row
presence, the basis used for the §5.2 sub-cell projection below:**

| band | rows | nights present (of 48) |
|---|---:|---:|
| < 70 | 1,182 | 48 |
| 70-80 | 575 | 48 |
| 80-85 | 627 | 48 |
| 85-90 | 57 | 33 |
| ≥ 90 | 18 | 17 |

The `≥ 90` band appears in **17 of 48 (35%)** contributing nights at the candidate level — far denser
than the published-elite rate (8/13/12/8/3/2 picks per month, DATA_NOTES/PI-010) the PREREG's own §4.3
text cites as its suppression expectation, because this population is every scored candidate, not the
published slate. See the Sub-cell section for the projected count.

---

## (e) Episode structure (DP-51)

Basis: the direction + ≥60-prior-bar-screened population (step 1/2, all 68 non-excluded nights, 3,588
rows) — not truncated by the price freeze's forward-bar horizon the way the eligible-row set is, since
episode structure needs no forward bar.

**Distinct symbols per night:** min 39, median 55, max 64. **Distinct symbols across the whole window:
400.**

**Symbol-episodes** (a symbol's run of appearances with gaps ≤ 10 sessions; 11+ sessions starts a new
episode): **811 episodes total**, mean **2.03 episodes/symbol**, **280 of 400 symbols (70%)** recur across
more than one episode.

**Episode length, in appearances (rows):** min 1, p25 1, median 2, mean 4.42, p75 5, max 44.

**Episode length, in session span (first to last appearance, inclusive):** min 1, p25 1, median 4, mean
10.3, p75 13, max 71.

This corroborates §10 threat 5 directly: a majority of symbols recur across multiple episodes, and the
longest single episode spans 71 sessions with 44 recorded appearances — a night-clustered CI alone would
treat that one name's overlapping 20-session paths as up to 44 quasi-independent observations.

---

## (f) `conflict_penalty` and B5 matched-pool feasibility

**Penalized share (`conflict_penalty > 0`):** eligible rows (the 48 contributing nights) 32.3%
(794/2,459); full step-2 population (all 68 nights) 32.2% — stable across the maturity cut.

**B5 matched-pool feasibility** (nights with ≥ 1 penalized row having ≥ 1 same-night unpenalized row
whose `overall_score` is within ±2.0 of the penalized row's re-derived pre-penalty base score,
`base = overall_score + conflict_penalty`): **48 of 48 contributing nights are feasible** — every
contributing night has ≥ 1 penalized row and ≥ 1 matched unpenalized comparison row.

---

## (g) DP-50(a)/(b) commit sweep since `fa70688`

`fa70688bc252d14f8d67e371afafc194731c324e` confirmed as an ancestor of HEAD
(`d19c9a945418b09773baffac37f8d723c8a90a9a`, verified via `git merge-base --is-ancestor` against the
pinned platform repository). **4 commits total (2 substantive + 2 merges) between them, all dated
2026-09-13:**

| commit | date (ET) | summary | touches the three named SAS files? |
|---|---|---|---|
| `2d5776c` | 2026-09-13 18:37 | PI-001: floor the legacy outcome backfill window in-process | **No** -- touches only the platform's nightly-pipeline entrypoint script (backfill-window clamp) and a new test file; the affected table is `uoa_symbol_daily`, already a banned Q027 input |
| `4775e49` | 2026-09-13 19:02 | merge PR #26 (PI-001) | -- |
| `22a2e1b` | 2026-09-13 21:55 | EN-002: speed-to-target internal card (Haci-only, flag off) | **No** -- new files only (a new speed-to-target service, a new admin router, `app.py` +2 lines, docs, tests); confirmed via `git diff --stat` that neither the scoring file nor the conviction-card file is in the changed-file list, despite the commit message referencing the conviction-card file in prose |
| `d19c9a9` | 2026-09-13 22:01 | merge PR #27 (EN-002) | -- |

**Answer: NONE.** No weight, timeframe multiplier, `qualification_threshold`, ATR-elite cap,
GEX-missingness offset, or scoring enable-flag changed in the platform code since `fa70688`.

**`sas_runs.config_json` cross-check (data-level, complements the code sweep):** 6 distinct `config_json`
blobs appear across the 71 in-window runs. Field-by-field:

| field | in-window behavior |
|---|---|
| `qualification_threshold`, `scoring_weights`, `timeframe_weight_multipliers`, `atr_elite_bull_max_score` (84.9), `atr_elite_bear_max_score` (79.9), `atr_sas_component_cap`, `max_conflict_penalty`, `max_cross_layer_bonus`, `missing_data_penalties`, `projection_score_ceiling` | constant across the whole window |
| `publication_floor` | null (25 nights, 2026-06-01..07-07) -> 80.0 (46 nights, 2026-07-08..09-10) |
| `bear_publish_threshold` | null (19 nights, 2026-06-01..06-26) -> 80.0 (52 nights, 2026-06-29..09-10) |
| two enrichment enable-flags | false on 2 nights only: 2026-06-02, 2026-07-02 (latter already excluded) |
| synthesis enable-flag | false on 1 night only: 2026-07-02 (already excluded) |
| two regime/earnings-bonus flags | null on 2026-06-01/06-02 only (transitional), false thereafter |

The `publication_floor` / `bear_publish_threshold` changes are already logged in `DATA_NOTES.md`
(the ladder-monotonicity entry, 2026-09-13: `publication_floor = 80.0` ships via commit `1765a6f`,
2026-07-07, effective the next run). Per DECISIONS item 12 these do not trigger a window split (they
gate publication, not scoring) but are recorded here as instructed, with the `d*_t` level shift
printed in (c). No new `DATA_NOTES.md` entry is needed -- the underlying fact is already dated there;
this report adds the `d*_t` consequence.

No `DATA_NOTES.md` entry is needed for a rewrite of historical `sas_candidates` or price rows: the
`outcome_corrections` ledger has 125 rows touching the SAS candidates table in-window, and 0 of them
touch `overall_score`, `conflict_penalty`, or `dominant_direction` (checked across the entire frozen
history, not just this window -- 0 of all rows in the ledger touch those three fields). Every in-window
correction is to an `outcome_*` / `level_hit_dates.*` / `bear_projection_source` field, none of which
Q027 reads.

---

## Sub-cell suppression flags, projected to the recommended window end (119 elapsed sessions, 2027-03-05)

Linear projection from the 48 measured contributing nights (their sub-cell presence rate x
0.6761/session x 119 sessions = x 80.45). Small-sample, indicative only (n = 48); a projection, not a
future measurement, reported as such.

| sub-cell | nights present (of 48) | projected at 119 sessions | flag |
|---|---:|---:|---|
| score band < 70 | 48 | 80.4 | ok |
| score band 70-80 | 48 | 80.4 | ok |
| score band 80-85 | 48 | 80.4 | ok |
| score band 85-90 | 33 | 55.3 | ok |
| score band >= 90 | 17 | 28.5 | ok -- clears (PREREG's own text expected suppression, based on the published-elite rate; R1(d)'s candidate-level measurement says otherwise) |
| `market_regime`: strongly_bullish | 29 | 48.6 | ok |
| `market_regime`: bullish | 14 | 23.5 | ok |
| `market_regime`: unlabelled (pre-2026-06-09 backfill / illegal) | 5 | 8.4 | not a tested cell -- informational |
| `market_regime`: bearish / neutral / risk_off | 0 | -- | none observed at all -- structurally absent, not thin |
| `tape_t`: up_mid | 18 | 30.2 | ok |
| `tape_t`: up_low | 10 | 16.8 | SUPPRESS |
| `tape_t`: down_high | 8 | 13.4 | SUPPRESS |
| `tape_t`: up_high | 5 | 8.4 | SUPPRESS |
| `tape_t`: down_mid | 4 | 6.7 | SUPPRESS |
| `tape_t`: down_low | 3 | 5.0 | SUPPRESS |
| `best_timeframe`: short | 48 | 80.4 | ok |
| `best_timeframe`: swing | 48 | 80.4 | ok |
| `best_timeframe`: long | 48 | 80.4 | ok |
| bull-only | 48 | 80.4 | ok -- PREREG's cited 0.157/session expectation is a published-bear rate (H-062/Q023), a different population; candidate-level bearish rows appear every measured night |
| bear-only | 48 | 80.4 | ok -- same caveat |
| published | 48 | 80.4 | ok |
| unpublished | 48 | 80.4 | ok |
| penalized (`conflict_penalty > 0`) | 48 | 80.4 | ok |
| unpenalized | 48 | 80.4 | ok |

Net: 5 of the 6 `tape_t` cells project below 20 at the recommended decision window; every other listed
sub-cell clears, including two the PREREG's own text expected to be suppressed (>= 90 band, bear-only)
-- both corrected here by measurement, per DECISIONS Correction 3 / item 10 ("fixed at lock, revised once
at `record` from R1(d)'s measured candidate-level band composition and R1(e)'s episode structure, then
closed").

---

## Projected schedule at the measured rate (0.6761/elapsed session)

Calendar: weekdays minus {2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26,
2027-05-31, 2027-06-18, 2027-09-06}, verified against the PREREG's own arithmetic (session 92 from
2026-09-15 lands on 2027-01-26, session 84 on 2027-01-13 -- both match section 5.2 exactly).

| floor | measured rate | sessions needed | projected date |
|---|---|---:|---|
| A: >= 80 contributing nights per primary endpoint (DP-21) | 0.6761/session | ceil(80/0.6761) = 119 | 2027-03-05 |
| B: >= 30 contributing nights post-lock (DP-24, satisfied by construction) | 0.6761/session | ceil(30/0.6761) = 45 | 2026-11-16 |
| C: >= 20 contributing nights per reported sub-cell | -- | -- | see Sub-cell table above |

Window end = later of A and B = A, session 119 = 2027-03-05. Window: pick nights
2026-09-15..2027-03-05 = 119 elapsed sessions (moved OUT from the PREREG's provisional 92-session /
2027-01-26 window, per DP-43/DP-45 -- the measured 0.6761 rate is slower than the borrowed 0.9538).

Decision date: window end + 20 sessions maturity (2027-04-05) + 1 calendar week (2027-04-12) + first
Monday on/after = Monday 2027-04-12 (was provisionally 2027-03-08). 6.9 months from the
2026-09-14 lock -- inside DP-43's 12-month ceiling (2027-09-14).

Single DP-13 extension (+30 sessions, if either floor is short on the eval script's own measured
counts at the decision pass): window end session 149 = 2027-04-19; decision date = maturity
2027-05-17 + 1 week 2027-05-24 + first Monday on/after = Monday 2027-05-24 (was provisionally
2027-04-19). 8.3 months from lock -- inside the ceiling.

Hard stop unchanged in kind: still short at the extended decision date -> `research/questions/DEFERRED.md`.

---

## What this does and does not decide

This is a counts-only exposure measurement. No touch rate, return, excursion, plan result, or
score-vs-outcome relationship appears anywhere above. The lock-or-DEFER call is mechanical: the
measured contributing-night rate (0.6761/elapsed session) clears the 0.36 floor implied by DP-43's
12-month ceiling at this lock date by a wide margin, so Q027 locks. The Registrar/Decision-maker
applies DP-43/DP-45's move-out-only rule to fold this report's schedule into `record`, fixes the sub-cell
suppression list from the table above (revised once, then closed per DECISIONS item 10), and files the
2026-06-02 no-`lane_plans` finding for whoever owns `exclusions_v003.json`'s next revision. I do not
decide any of that.
