# Q027 — score_ranking_validity: does a higher SAS score actually mean a better price path?

**Status:** PREREG_DRAFT (lock by committing this file) — every decision is applied from
`DECISIONS.md` (decide + record passes, 2026-09-14). No item is pending and nothing blocks the lock;
the one routed item still open, R2 (successor freezes), is due **before** the decision pass and is not
a blocker (DP-23).
**Decisions:** DECISIONS.md (2026-09-14) · exposure basis:
`research/reports/STEWARD_Q027_exposure.md` (R1, counts only, measured on the pinned freeze — no live
query stands behind any number in this file, DP-50(c))
**Family:** **F2 Calibration** (hypothesis **H-073**, with **H-010** folded in as the band-level
secondary and **H-012** as a stratum — both marked *merged into Q027* in `research/BACKLOG.md`,
DP-29). The primary endpoint's subject is whether the published score orders outcomes, which is
calibration.
**Manifest (selections, sealed post-hoc panel and R1 counts only):** research/data/manifest_v001.json
(as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e) — **for provenance, the
sealed post-hoc panel (§6) and R1's counts-only exposure measurement (§5.1) only.** No night that
carries a verdict here exists in it.
**Manifest (prices, sealed post-hoc panel and R1 counts only):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — same standing.
**Successor freezes — the question itself (built and pinned at the decision date, DP-23; §5.3 R2):**
`manifest_v00N` (selections: `sas_candidates` **for every candidate row, published and unpublished**,
`sas_runs`, `market_regime_daily`) and `manifest_prices_v00N` (daily bars for **every candidate symbol
on every in-window night**, published or not), covering pick nights **2026-09-15 .. 2027-03-05** with
daily bars through **2027-04-05** (session t+20 of the last included pick night) and ≥ 60 prior
sessions before 2026-09-15; a second pair **only if** the single DP-13 extension fires, covering pick
nights **.. 2027-04-19** with bars through **2027-05-17**. **The primary window is entirely
prospective: not one night that carries a verdict here exists in `manifest_v001`**, so the population
enters *only* through those successor freezes, which the desk pins at the decision date
(`pin_at_decision`, DP-23 — the Q024 pattern). They are named here and deliberately **not** written as
`**Manifest …:**` header lines, because no such file exists yet and the pin step reads every
`**Manifest` line as a path.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates` ∪
`non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, DP-22)
**unioned with the add-only successor exclusions file** issued with the successor selection freeze —
the identical three lists, built by the identical criteria, covering nights after 2026-09-10, **plus a
fourth list, `payload_disabled_runs`** (DECISIONS item 11: a night on which *every* published row
carries `public_payload_json.analysis_status = "disabled"` or no `lane_plans` object at all, i.e. zero
screened `d_L3` survivors — §2.4). The successor file may only **add** nights; no night is ever
removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be.
Both paths are `eval.py` inputs; no hard-coded file name, no hard-coded date. DP-04 applies
mechanically on top.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14

---

## 1. Hypothesis (plain English)

**Among all the stocks SAS scores on a night, the higher-scored ones actually reach a target the same
distance away — measured in each stock's own daily range — more often and sooner than the
lower-scored ones; and the score orders them smoothly, not just at the top.**

BACKLOG **H-073** (Haci's H3, *Ranking validity*) reads: *"does a higher SAS score mean a better
expected outcome — PASS mean per-night Spearman IC ≥ 0.05, positive in ≥ 60% of out-of-sample
windows, and the top tier materially beats the bottom tier; FAIL IC ≈ 0, unstable, or materially
non-monotonic → stop presenting the score as a precise conviction ranking."* It names a population
(**all 16:05 candidates**, published or not) and a statistic, and leaves the entry, the target
distance, the clock, the tie handling and the decision rule open. This PREREG fixes all of them.

**Two primaries** (§4), both night-level, both two-sided:

- **E1 — the information coefficient.** The mean per-night Spearman rank correlation between
  `overall_score` and the **path outcome** — *whether and when* a target placed at the night's
  common ATR distance is first touched within 20 sessions from the session t+1 open — across every
  eligible candidate that night. **MPE `|ρ̄| ≥ 0.05`.**
- **E2 — the tercile contrast.** The within-night top-tercile minus bottom-tercile touch rate at the
  same distance and the same clock, averaged over nights. **MPE ±5.0 pp (DP-20).**

**Folded in, and where they sit.** **H-010** (score-band monotonicity) becomes the **band-level
secondary** (§4.3): per-band night-demeaned touch rates with a pre-registered monotonicity statistic
and adjacent-band contrasts. It is not a third primary — but a **material band inversion is a
blocker** on the question-level verdict (§8), because "materially non-monotonic" is half of H-073's
own FAIL condition and a secondary with no teeth would quietly drop it. **H-012** (conflict-penalty
validity) rides as a **stratum** (§4.3): E1 and E2 recomputed on penalized and unpenalized rows, plus
a base-score-matched penalized-minus-unpenalized touch contrast, all descriptive.

**What is not in this question.** Per-**layer** ICs belong to **H-075** and are not computed here
(§7). Q027 tests the composite `overall_score` and nothing else.

**Why the window starts after the lock.** The desk's weekly snapshots of 2026-09-10 and 2026-09-12
already printed band-level *returns* on sealed nights — the 90+ lead as an April–May effect, the
70–80 band's disappearance, the 88–90 versus 90+ finding in CLAUDE.md's standing list. The top of the
score distribution has therefore been read against outcomes on those nights, and both the band
secondary and the top tercile of E2 live there. Those nights are contaminated for this question and
are **not used for any verdict**: the window is **prospective-only, pick nights ≥ 2026-09-15** (§6),
and the sealed stretch is printed once as a labelled post-hoc panel that enters no verdict, no half,
no stratum test, no CI comparison and no q. This is the Q023 / Q018 pattern, applied for the same
reason.

**Direction of the claim.** H-073 predicts `E1 > 0` and `E2 > 0`. Both are registered **two-sided**:
a confirmed *negative* IC — the score ordering outcomes backwards — would be a more consequential
finding than a null, and §9 says what it licenses.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Candidate rows are reduced to one statistic per
  night first; nights are the observations. Control rows never add to n.
- **Source tables (the successor selection freeze, §5.3):**
  `sas_candidates` — **every row, published or not, regardless of `qualified` / `threshold_pass`**:
  `trading_date`, `symbol`, `overall_score`, `qualified`, `threshold_pass`, `qualification_reason`,
  `selected_rank`, `dominant_direction`, `best_timeframe`, `confidence_level`, `completeness_score`,
  the seven layer subscores, `cross_layer_bonus`, **`conflict_penalty`**, `missing_data_penalty`,
  `score_details_json`, `source_membership_json`, `context_json`,
  `public_payload_json` → `lane_plans.swing_trading.targets` (published rows only, for §2.2's
  distance), `outcome_target_invalid` (exclusion audit only);
  `sas_runs` — `finished_at` (DP-04), `config_json` (the weights / multiplier / threshold audit,
  §10 threat 9);
  `market_regime_daily` — `trading_date`, `regime_version`, `market_regime`, `data_quality`,
  `created_at` (rule-7 stratum only; never a filter, never an arm).
- **Source tables (the successor price freeze, §5.3):** `prices_daily_split` (pick-night close,
  ATR14, beta60, runup20, mom20, forward bars to t+20, SPY tape), `prices_daily_raw` (split-factor
  snapping only). **No hourly bar is used and no primary depends on one.**
- **No outcome column is ever an input.** `outcome_*`, `sas_selection_excursion.*`, `level_hit_*` are
  not joined; `uoa_symbol_daily.fwd_return_*` is banned outright (FREEZE_v001 §5). Unpublished
  candidates are essentially **ungraded** in the platform's own outcome columns (FREEZE_v001 §4:
  0 of 5,572 non-qualified rows sealed, 2.4% with any return), which is exactly why every outcome
  here is computed from pinned bars.

### 2.1 Eligible rows — exact filter

**The two dates below are illustrative of values `eval.py` receives as inputs.** §5.3 R2 requires the
script to take the window start, the window end, the manifest paths, the exclusions-file paths and
the output directory as arguments, with **no hard-coded date, manifest name or path**, so that the
byte-identical script serves the primary run and the single DP-13 extension run alike.

```sql
SELECT c.*
FROM   sas_candidates c
JOIN   sas_runs run ON run.trading_date = c.trading_date
WHERE  c.trading_date >= DATE '2026-09-15'        -- §6 window start   (input, illustrative)
  AND  c.trading_date <= DATE '2027-03-05'        -- §5.2 window end   (input, illustrative)
  AND  c.trading_date NOT IN (<exclusions_v003 ∪ the add-only successor exclusions file:
                               manual_runs ∪ non_session_runs
                               ∪ uncorroborated_publication_runs
                               ∪ payload_disabled_runs, read from the JSONs>)
  AND  c.overall_score IS NOT NULL
  AND  c.dominant_direction IN ('bullish','bearish')   -- §2.4: 'mixed' excluded and counted
-- and, applied in eval.py from the pinned price freeze, not in SQL:
--   ≥ 60 split-adjusted daily bars dated ≤ t (ATR14, beta60, runup20, mom20 defined)
--   a session t+1 open exists, and daily bars cover t+1..t+20 without a gap
```

**Every score is in scope.** No qualification threshold (70.0, volatilx
`services/super_agent_select_models.py:85`) and no publication floor (80.0, `:91`) filters this
population: the ranking claim is about the score, and the unpublished rows are the counterfactual
(CLAUDE.md; Q005 §2's "all candidate rows kept regardless of `qualified` or `threshold_pass`").
**Published rows are not an arm here** — publication is recorded per row and used only for descriptive
splits and for §2.2's distance. **"Published" is DP-28's predicate and nothing looser:
`qualified IS TRUE AND selected_rank IS NOT NULL`** (DECISIONS Correction 4). **Dark-lane rows**
(`qualified` true, `selected_rank` null) are therefore **not** published: they are excluded from
§2.2's `d*_t` median and from the published sub-cell, and — because this population is every scored
row — they **remain in the population**, carrying a score and a synthetic target like any other
candidate. DP-28's predicate governs which rows are *called* published; Q027 has no published arm.

### 2.2 The target: one ATR distance per night, identical for every candidate

Every candidate on night t is asked to travel **the same number of its own ATRs**, in its own
direction. That single choice is what makes the within-night rank correlation a test of the *score*
rather than of the *targets the engine drew*.

- `dir` = +1 for `bullish`, −1 for `bearish` from `dominant_direction`. Every distance and every
  touch is direction-adjusted.
- `C_t` = the row's actual regular-session close on night t from `prices_daily_split` (never the
  platform's `spot_close`, stale on re-run nights — EXPLORE_001 §9).
- `ATR` = ATR14 from `prices_daily_split` bars dated ≤ t (never the platform's `atr_pct`, corrupted
  around splits — DATA_NOTES / PI-003).
- **`d*_t`, the night's common distance** = the median over that night's **published** picks —
  **published = `qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28; DECISIONS Correction 4),
  dark-lane rows excluded from the median** — of `d_L3 = dir × (L3 − C_t) / ATR`, where
  `L3 = lane_plans.swing_trading.targets[0]` (volatilx `services/sas_conviction_card.py:182-187`) —
  i.e. the distance the platform itself printed as the swing first target that night, in ATR units.
  Published rows failing the §2.4 split-scale screen are excluded from the median **before** it is
  taken (DATA_NOTES, the APH / KLAC / CRWD / MNST finding: a raw-scale target inflates a printed
  distance without failing any wrong-side test).
  **Thin slate versus absent slate — two different nights, two different rules (DECISIONS item 11,
  Correction 7):**
  - **1 or 2 screened published survivors → thin slate.** `d*_t` is the **median of `d*` over the
    prior 20 contributing nights** (trailing, knowledge-time legal); if that too is unavailable the
    night is **excluded and counted**.
  - **Zero screened published survivors → the slate is structurally absent, and the night is excluded
    whole**, under the successor exclusions file's fourth list `payload_disabled_runs` (§2.4). The
    trailing-median fallback **never** fires here. R1 found this signature on 2026-06-02 (all 8
    published rows carrying `public_payload_json.analysis_status = "disabled"`, no `lane_plans`,
    two enrichment enable-flags off in that night's own `sas_runs.config_json`), recurring on
    2026-04-01, 2026-05-01 and 2026-07-02 — every one the first published night of a calendar month.
    The reason it is an exclusion and not a fallback is measured, not stylistic: on a zero-survivor
    night the common distance would be imported wholesale from a different cohort, and R1(c) measures
    that cohort's median moving from ≈ 1.06 to ≈ 2.10 ATR across a single config ship, so an imported
    `d*_t` would be a different experiment on that night, not a rounding error.

  The distribution of `d*_t` is printed, whole and split by direction, and `eval.py` **fails loudly**
  if any night's `d*_t` falls outside `[0.25, 10]` ATR. *Measured on the sealed stretch (R1(c), counts
  only): `d*_t` is defined on all 68 non-excluded nights (67 direct, 1 fallback), median 1.849 ATR,
  zero nights outside the fail-loud bound.*
- **The synthetic target** for row i on night t:
  `T_i = C_i × (1 + dir_i × d*_t × atr_pct_i)` with `atr_pct_i = ATR_i / C_i` — the same ATR distance
  and the same direction for every row on the night, published or not.

**This is where rule 5's distance-matched control lives.** The comparison is not picks against an
outside cohort; it is candidates against each other on the same night at an identical ATR distance,
which is the matched control construction of Q006 §3 taken to its limit (the match is exact on
distance and direction by construction, and §4.3 prints the post-hoc balance of `beta60`,
`atr_pct`, `runup20` and `log10 adv20` across score terciles so the reader can see what is *not*
matched). A touch rate here is never quoted without that construction attached.

### 2.3 Entry, clock and the two outcome variables

- **Entry `X_i` = the session t+1 regular-session open** (DP-03(b), DP-42), for every row alike — the
  basis Haci actually trades and the only basis that exists for unpublished candidates. The `C_t`
  basis (DP-03(a) / DP-11) is computed and printed for both primaries as a named sensitivity and
  **never decides**.
- **A target already through `X_i` at the t+1 open is not a hit** (rule 5, DP-26): `hit_i = 0`,
  `s_i = ∞` (see below), the row stays in the denominator, and the not-takeable count is printed per
  score tercile and per band.
- **Clock: 20 sessions, t+1..t+20**, uniform for every row, so nothing is right-censored by its own
  timing (DP-42's day/spread horizon; the platform's own 40-session swing window is printed for
  published rows as a descriptive companion only).
- **`hit_i` ∈ {0,1}** = 1 if the regular-session high (bullish) / low (bearish) touches `T_i` on some
  session in t+1..t+20. A gap through `T_i` at a session open is a touch.
- **`s_i`** = the number of sessions from `X_i` to that first touch (1..20), and `s_i = ∞` for a row
  that does not touch. **The path-outcome rank `u_i`** is the within-night rank of `−s_i`: touchers
  are ordered fastest-first, and every non-toucher is tied below every toucher. This is *whether and
  when* (rule 5, DP-08) in one variable, and it is the variable E1 correlates with.
- **No stop, ever** (rule 5, DP-02). Maximum adverse excursion and counter-direction touches at
  `−d*_t` ATR are reported per tercile and per band, never used as exits.

### 2.4 Exclusions — each counted, printed in the results header, never silently dropped

Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or a
measurement failure. None can move a row between score terciles or bands.

- **Nights** in the union of `exclusions_v003.json` and the add-only successor file — `manual_runs` ∪
  `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ **`payload_disabled_runs`** — and any night
  whose `finished_at` is later than the next session's open, or dated on a non-session day (DP-04).
- **`payload_disabled_runs` — a night whose published slate carries no lane plans at all** (DECISIONS
  item 11; the fourth criterion, fixed at this lock): every published row (DP-28:
  `qualified IS TRUE AND selected_rank IS NOT NULL`) carries
  `public_payload_json.analysis_status = "disabled"` or no `lane_plans` object, i.e. **zero rows
  survive the split-scale `d_L3` screen** → the **whole night is excluded and counted**. The criterion
  is a **payload signature: outcome-blind, measurable at freeze time**, and it is add-only — it may
  add nights after 2026-09-10 and may never remove a night from any v003 list. `exclusions_v003.json`
  itself is not edited; the list lives in the successor file (§5.3 R2).
- **`dominant_direction = 'mixed'`** (the scorer's default when direction evidence does not resolve —
  volatilx `services/super_agent_select_scoring.py:1180`) → **row excluded and counted**. The share
  of mixed rows **per score decile** is printed every night, because mixed is plausibly commoner at
  the bottom of the distribution and dropping it truncates the very tail the IC is about (§10 threat
  3). The **"mixed graded long" sensitivity** — the same primaries with mixed rows kept and graded
  bullish — is mandatory and **blocking** (§8 clause 7). A night is excluded in whole if more than
  **25%** of its scored rows are mixed. (DECISIONS item 6: excluded and counted, never graded long in
  the primary — a synthetic target needs a direction, and inventing one for exactly the rows the
  scorer could not resolve would feed the IC a fabricated outcome; the blocking companion is what
  stops the exclusion quietly deleting the tail the IC is about. *Measured, R1(b): mixed is 10.75% of
  scored rows overall, 58.7% in decile 0 and 0.0% from decile 4 up — threat 3 is real and sits exactly
  where it was expected; 0 of 68 nights cross the 25% threshold and 0 of 48 cross the 10% ungradeable
  threshold.*)
- **Fewer than 60 split-adjusted daily bars dated ≤ t** (ATR / beta60 / runup20 / mom20 undefined) →
  row excluded and counted. This is the screen that removes the **CTRA truncated-history signature**
  (last daily bar 2026-05-06 while still appearing as a candidate — `STEWARD_Q023_exposure.md` §6,
  reproduced in `STEWARD_Q024_…` (b)); the per-night count of rows dropped for it is printed and the
  successor freeze repeats the scan (§5.3 R2).
- **Missing forward bars** inside t+1..t+20 (halt, delisting) → ungradeable, excluded and counted;
  a measurement failure, never a classifier. A night is dropped if > 10% of its eligible rows are
  ungradeable.
- **Split-scale payload screen, published rows only (DP-28), for the `d*_t` median** (DATA_NOTES): a
  published row is excluded from the median if `lane_plans.day_trading.entry / C_t` is outside
  `[0.85, 1.15]` or any flattened level implies `|dir × (level − C_t) / ATR| > 20`. It is **not**
  excluded from the population — it still carries a score and a synthetic target like every other
  row; only its printed ladder is distrusted.
- **Immature nights** — session t+20 after the last trading date of the pinned price freeze →
  excluded and counted. Maturity comes from the trading calendar, never from whether a price exists;
  right-censoring is never graded as a non-touch.
- **A night with fewer than 30 eligible rows** → **non-contributing** (§2.5), counted, not an
  exclusion (DECISIONS item 5, the stricter of the two floors on offer; DP-21). Below 30 rows the
  terciles are under 10 wide and a per-night ρ is mostly tie structure. **Measured on this question's
  own funnel** (R1(a), `STEWARD_Q027_exposure.md`): eligible rows per night min **39** / median **51** /
  max **64**, so the floor clears on every measured night with margin — but it is a per-night gate on
  `eval.py`'s own counts, never a projection.

### 2.5 Contributing night, and the episode (DP-51)

- **Contributing night (the floor unit, DP-21; identical for E1 and E2):** a non-excluded night in
  the window, matured to t+20, carrying **≥ 30 eligible rows** with both terciles non-empty **and a
  defined `d*_t`** (directly, or by §2.2's trailing-20-night fallback on a 1–2-survivor night; a
  zero-survivor night is not a non-contributing night, it is **excluded whole** under
  `payload_disabled_runs`). A night that survives the night-level filters but carries fewer than 30
  eligible rows is a **non-contributing night, not an exclusion** — printed in the funnel.
  **This complete definition is the one R1 measured** (`STEWARD_Q027_exposure.md`), and it is the rate
  §5.2's schedule is built on: **0.6761 contributing nights per elapsed session (48/71)**.
- **Episode (DP-51, the H-070 unit):** one **symbol's** run of appearances as an eligible candidate
  row with gaps of **≤ 10 sessions** between successive appearances; a gap of 11 or more sessions
  starts a new episode. Every eligible row belongs to exactly one symbol-episode. Episodes are the
  second resampling unit in §4.4, beside the night.
  *Why it is needed here specifically:* the same ~60 symbols recur night after night and their
  t+1..t+20 windows overlap almost completely, so a night-clustered CI treats one symbol's single
  20-session path as up to twenty independent observations of "did a high score work". The
  night-clustered CI absorbs same-night correlation; the episode-clustered CI absorbs the other axis.
  *Measured on the sealed stretch (R1(e), counts only): 400 distinct symbols, 811 episodes, **70% of
  symbols recurring across more than one episode**, longest episode 44 appearances over 71 sessions —
  §10 threat 5 is confirmed structurally, before any outcome is read, and DP-51's second CI earns its
  place as a decision clause rather than a footnote.*

## 3. Baselines — what this must beat

- **B1 (primary, the null the IC is measured against): the same statistic with `overall_score`
  shuffled within night.** For each night, permute the scores across that night's eligible rows,
  recompute the night statistic, average over nights; 10,000 permutations, seed 20260914. This is
  H-073's own named baseline and it is the exact counterfactual "the score carries no ordering
  information, the outcomes are what they are". Under it `E[E1] = 0` and `E[E2] = 0` by construction,
  and the permutation distribution supplies the p-values BH corrects (§7).
- **B2 (rule-5 distance-matched control, inside both primaries by construction, §2.2):** every row on
  the night carries a target at the **identical ATR distance in its own ATR units and its own
  direction**. A high-score row is therefore never compared against a low-score row asked to travel a
  different distance. A touch rate from this question is never reported without this sentence
  attached (§8's language clause).
- **B3 (the "is 0.05 impressive?" comparator, descriptive, never decides):** the same per-night
  Spearman ρ computed with **`mom20`** — the trailing 20-session return rank from pinned bars — in
  place of `overall_score`, on the identical rows, targets and clock, plus the same tercile contrast.
  It is a free benchmark that costs no new data and no new freeze, and it tells the reader whether a
  confirmed SAS IC is a large number or a small one. **It is not a test of Q024** (§7): Q024 contrasts
  the published *slate* against momentum-ranked *slates* at slate level, with a money gate; B3 is a
  rank correlation over candidates. Neither may be read as a second confirmation of the other.
- **B4 (H-010's own baseline, band level, secondary): the adjacent band.** The band contrast is
  always band `b` against band `b−1` on the same nights, night-demeaned, never against a pooled
  remainder — H-010 as written (DP-25).
- **B5 (H-012's baseline, stratum, descriptive): unpenalized rows at the same base score.** For each
  penalized row (`conflict_penalty > 0`), the same-night unpenalized rows whose **pre-penalty base
  score** is within ±2.0 points, with `base = overall_score + conflict_penalty` re-derived from
  `score_details_json` where present; touch rates contrasted within night. H-012's claim as written.
  *Measured, R1(f): penalized share 32.3%, and the matched pool is feasible on 48 of 48 nights.*

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Nothing in this question is decided by a fixed-horizon return.** Close-to-close returns at T+5 and
T+20 from `X` are printed and are **descriptive by rule 5 and DP-01** — and the per-night return IC
(the Spearman ρ of `overall_score` with the T+20 return) is printed beside E1 as the number H-073
explicitly says "prints and decides nothing". That matters here more than usual: the sealed reads
that motivated H-010 *were* returns.

### 4.1 Per night

Let `N_t` be night t's eligible rows (§2.1, `|N_t| ≥ 30`).

- **`IC_t` = Spearman ρ over `N_t` between `overall_score` and the path-outcome rank `u_i`** (§2.3),
  with the standard mid-rank tie correction on both variables. Non-touchers form one large tied block
  by construction, so `IC_t` is bounded well below 1; §4.3 prints the **maximum attainable |ρ|** given
  each night's tie structure as a scaling reference (descriptive — it never rescales `IC_t`, which
  would silently change the MPE).
- **`G_t` = mean `hit_i` over the top score tercile of `N_t` − mean `hit_i` over the bottom tercile**,
  in percentage points. Terciles are cut on `overall_score` within the night, ties broken by
  (score, symbol ascending) so the cut is deterministic; the boundary scores and tercile sizes are
  printed per night, and the middle tercile's touch rate is printed beside them (it is what makes the
  band secondary readable).

### 4.2 Primary endpoints

- **E1 = mean over contributing nights of `IC_t`**, in Spearman-ρ units. **MPE `|ρ̄| ≥ 0.05`.**
- **E2 = mean over contributing nights of `G_t`**, in percentage points. **MPE ±5.0 pp (DP-20 — E2 is
  a single difference of two touch rates measured at the identical ATR distance within the same
  night, the Q006 E1 shape, not a difference of differences, so the doubling clause does not apply).**

**On the E1 MPE.** `ρ̄ ≥ 0.05` is **Haci's own number**, from the Master Hypothesis Program's H3 PASS
line (`research/reports/INBOX_2026-09-14_master_hypothesis_program.md` §1, H3: *"Mean daily Spearman
IC ≥ 0.05"*). **DP-44 carries no MPE unit for a rank-correlation endpoint** and this autonomous run
writes no new DP entry (DP-40), so the number is applied here **as registered, with its source
stated** (DECISIONS item 3, decided on DP-25: units and cuts come from the hypothesis as written, and
the Registrar does not re-unit a number that is the hypothesis's own). The *general* form — "the MPE
for any per-night rank-correlation endpoint is 0.05 in Spearman-ρ units" — is filed in `DECISIONS.md`
under **Standing rules proposed**, for Haci to confirm before H-075's per-layer ICs and H-082's decay
series need it; it is **not** a DP entry today and nothing in this file depends on it becoming one.
The MPE is **not lowered at the decision pass in any branch**, including one where the CI excludes
zero and the point estimate sits at 0.04 — that is what an MPE is for (rule 6).

### 4.3 Secondary, stratum and sensitivity output

Everything here prints raw p only and is labelled *"descriptive, does not decide"* — **except the
named blockers**, which carry no verdict of their own but **block** a CONFIRMED verdict when they run
the other way (§8 clauses 6–9). Suppression restricts affirmative reporting only: it never removes a
blocker, and a suppressed cell never by itself makes an endpoint INCONCLUSIVE.

**The band-level secondary (H-010, merged).** Bands, fixed at lock, half-open, no rounding:
`< 70` / `70–80` / `80–85` / `85–90` / `≥ 90` — the qualification threshold (`:85`), the publication
floor (`:91`) and the elite line, which are the platform's own boundaries, not cuts chosen by the
desk (DP-26).

- Per band, per night: the **night-demeaned** touch rate `hit_i − mean(hit on night t)`, averaged
  over the band's rows, then over nights. Night-demeaning is what stops a band contrast being a
  calendar contrast — the failure mode H-010's own weekly snapshot ran into (the 70–80 band all but
  vanished after May, so a raw 70–80 vs 80–90 comparison compares April with August).
- **Monotonicity statistic `M`** = Spearman ρ between the band index (1..5) and the band's
  night-demeaned mean, computed per night over the bands present that night and averaged over nights,
  with the within-night score permutation as its null.
- **Adjacent-band contrasts** (B4): band `b` minus band `b−1`, night-demeaned, each with its
  contributing-night count. A band cell on the suppression list, or one with fewer than 20 **measured**
  contributing nights at the decision pass, is **SUPPRESSED** — counts only, no point estimate, not
  "directionally". **The list is fixed at this lock and closed** (DECISIONS item 10, Correction 3): it
  was revised once at `record` from R1(d)'s **measured candidate-level band composition** and is not
  reopened; a cell suppressed here stays suppressed even if it clears 20 measured nights at the
  decision pass, and a cell cleared here still needs ≥ 20 measured contributing nights to print.
  **All five bands, `≥ 90` included, are on the affirmative-reporting list** (Correction 8): the draft
  expected `≥ 90` to be suppressed from the *published*-elite monthly counts (8 / 13 / 12 / 8 / 3 / 2,
  DATA_NOTES / PI-010), but this question counts elite **candidates**, and R1(d) measures them present
  on 17 of 48 nights (35%), projecting **28.5** contributing nights at session 119. The registered rule
  is and always was a **measured count on this question's own population**, not an expectation, and a
  rate measured on a narrower population does not transfer.
- **Blocking (§8 clause 9):** a **material band inversion** — any adjacent-band contrast with ≥ 20
  **measured** contributing nights whose point estimate is **below −5.0 pp** with its own 95%
  night-clustered CI excluding 0 — blocks a question-level CONFIRMED, whatever E1 and E2 do.
  **Suppression restricts affirmative reporting only and never removes this blocker** (DECISIONS
  item 4, Correction 2; Q023 DECISIONS #9 in the same words): the inversion test is computed for
  **every** adjacent pair that has ≥ 20 measured contributing nights, **whether or not that band is on
  the lock-fixed suppression list**. Letting suppression delete the blocker would mean the one boundary
  most likely to be thin — the 90 line, where H-010's whole claim lives — could run backwards with no
  consequence.

**The conflict-penalty stratum (H-012, merged).** All descriptive:
E1 and E2 recomputed on `conflict_penalty > 0` rows and on `conflict_penalty = 0` rows separately;
the B5 base-score-matched penalized-minus-unpenalized touch contrast; the penalized share per score
decile; the penalty's own magnitude distribution. **No verdict rests on this stratum and no platform
change follows from it alone** (§9) — H-012 keeps its own line in the BACKLOG for a question that
makes it primary.

**Computed, and blocking (§8):**

- the **binary-outcome IC** — the same per-night Spearman ρ with `hit_i` in place of `u_i`
  (**E1's** clause-6 blocker);
- the **touch-within-5-sessions tercile contrast** — `G_t` recomputed with the clock cut to t+1..t+5,
  in percentage points (**E2's** clause-6 blocker, Correction 1). This is the companion in a unit that
  **has** an MPE: DP-44 gives sessions-to-touch differences no MPE, so the blocker is stated in DP-20
  touch-rate units (±5.0 pp) and the sessions-to-first-touch distributions stay purely descriptive;
- the **"mixed graded long" sensitivity** of both primaries (§2.4, clause 7);
- the **bull-only** version of both primaries, with the per-night direction mix (clause 8);
- **Half A / Half B** (§6) — the stability clause. It blocks at whatever count it has; it is not a
  reported stratum and is not on the suppression list;
- the **monthly-block stability panel**: `IC_t` and `G_t` averaged within calendar month, each month
  with ≥ 10 contributing nights. H-073's *"positive in ≥ 60% of out-of-sample windows"* is
  implemented here as clause 10, on the months, not as a third primary.

**Computed, mandatory, purely descriptive:**

- **B3**, the `mom20` comparator IC and tercile contrast;
- the **`C_t` entry basis** (DP-03(a) / DP-11) for both primaries, with not-takeable counts;
- the **40-session** companion of both primaries (the platform's own swing window, descriptive —
  DP-09, DP-42);
- **sessions-to-first-touch** distributions (median, p75) by tercile and by band, among touchers —
  **descriptive, with no MPE anywhere in session units** (DP-44); the speed claim is carried by the
  touch-within-5-sessions form above, which is where the blocker lives;
- **maximum favourable and maximum adverse excursion in ATR** from `X`, and counter-direction touches
  at `−d*_t` (reported, never an exit — DP-02);
- the **post-hoc balance table**: `beta60`, `atr_pct`, `runup20`, `log10 adv20` and price level by
  score tercile, with standardized mean differences — what the identical-ATR-distance construction
  does *not* match (§10 threat 4);
- the **tie-structure reference**: per night, the touch base rate, the size of the non-toucher tied
  block, and the maximum attainable |ρ| given that structure;
- the **score-distribution panel**: per night, the share of rows at exactly 84.9 / 79.9 (the ATR-elite
  cap — volatilx `services/super_agent_select_scoring.py:1401-1423`), the share with a null
  `gex_alignment_score` (the +5 offset, `:1379-1399`), and the score IQR — the direct read on
  whether the ranking has resolution at all (§10 threat 2). *Measured on the sealed stretch (R1(d),
  counts only): score IQR median **25.04** with **no night at IQR 0**, the ATR-elite caps firing on
  **2 of 4,020 rows**, null GEX at **0.99%** — threat 2 was measured and is not observed. The panel
  still prints every night of the prospective window; the threat is disclosed as not-yet-seen, not
  retired.*;
- the **per-night return IC** and close-to-close returns at T+5 / T+20 — **descriptive by rule 5 and
  DP-01; they never decide**, and no verdict sentence may lead with them.

**Sub-cells — the list is FIXED at this lock and CLOSED.** It was revised once at `record` from R1's
measured counts (DECISIONS item 10) and is not reopened at the decision pass, in either direction.
Every listed cell additionally needs ≥ 20 **measured** contributing nights to print; clearing the
projection is permission to print, not a guarantee.

- **SUPPRESSED (8 cells, counts only, no point estimate, not "directionally"):** five of the six
  `tape_t` cells — `up_low` (projecting 16.8 contributing nights at session 119), `down_high` (13.4),
  `up_high` (8.4), `down_mid` (6.7), `down_low` (5.0) — and the three `market_regime` labels **absent
  from the measurement**, `bearish` / `neutral` / `risk_off` (0 of 48 nights: structurally absent, not
  merely thin).
- **On the affirmative-reporting list:** `tape_t` `up_mid` (30.2); **all five score bands, `≥ 90`
  included** (28.5; `85–90` at 55.3); `market_regime` `strongly_bullish` (48.6) and `bullish` (23.5);
  all three `best_timeframe` cells; **bull-only and bear-only** (80.4 each); published versus
  unpublished rows (DP-28's predicate); penalized versus unpenalized.
- **Two cells came *off* the draft's expected-suppression list at `record`, and the reason is the rule
  itself** (Correction 8): `≥ 90` and **bear-only** were expected to be suppressed on published-elite
  monthly counts and on H-062's 0.157/session *published*-bear rate. R1(d)/(a) measure the
  all-candidates population this question actually uses — elite **candidates** on 17 of 48 nights, and
  candidate-level **bearish rows on 48 of 48 nights** — so both print. The registered rule is a
  **measured count**, never an expectation.
- `market_regime` **`unlabelled` is not a cell**: the pre-2026-06-09 backfill cannot occur inside a
  window starting 2026-09-15 (rule 14; `exclusions_v003.regime_label_point_in_time_from`).
- **Suppression restricts affirmative reporting only.** It never removes clauses 5–10's blockers, and
  it never by itself makes an endpoint INCONCLUSIVE. The halves, the bull-only version, the "mixed
  graded long" version, the binary-outcome IC, the 5-session companion and the monthly blocks are
  **not** on this list and block at whatever count they have.

**Quotability:** 20-session basis, W20 research window → **every number in this question is
`NON_QUOTABLE`** (rule 12).

### 4.4 Inference — two CIs per primary (DP-51)

Night-level throughout. Control rows never add to n (rule 6).

- **CI 1 — date-clustered (the registered bootstrap):** resample **contributing nights** with
  replacement, 2,000 resamples, recomputing the mean of `IC_t` / `G_t`. A **stationary block
  bootstrap** over the ordered nights (expected block length **10 sessions** — the Q004 / Q007 /
  Q009 / Q011 / Q015 / Q023 value, fixed at lock, not chosen after seeing anything) is printed
  beside it.
- **CI 2 — episode-clustered (DP-51):** resample **symbol-episodes** (§2.5) with replacement **and**
  nights with replacement, jointly: draw a bootstrap set of episodes and a bootstrap set of nights,
  keep the rows in the intersection, recompute each retained night's `IC_t` / `G_t` from the rows
  that survive (a night is retained only if ≥ 30 rows survive and both terciles are non-empty), and
  average. 2,000 resamples, same seed. This is the CI that absorbs one symbol's overlapping
  20-session paths being counted on twenty consecutive nights.
- **DP-51's rule is a decision rule here, not a footnote: a primary that clears MPE with CI 1
  excluding 0 but CI 2 including 0 is INCONCLUSIVE, never CONFIRMED** (§8 clause 5).
- **p-value (decides, feeds BH):** the within-night score permutation of B1, 10,000 permutations,
  seed 20260914, two-sided. The permutation holds each night's outcome structure fixed and destroys
  only the score ordering, which is precisely H-073's null.
- **Every estimate prints:** contributing nights; eligible rows per night (min / median / max);
  distinct symbols and **episodes**, with the episode-length distribution; contributing nights dated
  after the lock commit; `d*_t` distribution; not-takeable counts; rows excluded by reason;
  per-tercile and per-band row counts; and the §4.3 balance table.

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** and ≥ **20
  contributing nights per reported sub-cell**. The weaker "80 eligible with ≥ 20 contributing"
  reading is not used. **No floor is ever lowered to reach a date.**
- **DP-24:** ≥ 30 contributing nights dated after the lock commit. **Every** contributing night here
  is post-lock by construction (§6), so DP-24 binds at 30 of the 80 and is not the gate.
  **PROSPECTIVELY_CONFIRMED is reachable from this run by design; DP-31 does not apply and no
  successor replication question is needed.**
- **Binding maturity: 20 sessions**, uniform across every eligible row (§2.3).
- **Neither primary is demotable** (DECISIONS item 10, fixed at lock — demotion is decided here or not
  at all, DP-43). E1 and E2 share the same contributing nights and each *is* a primary, so a night
  shortfall leaves no endpoint standing: it is a floor failure — the single DP-13 extension, then
  DEFERRED — **never a demotion to descriptive and never an INCONCLUSIVE verdict**.

### 5.1 Exposure basis — measured on this question's own funnel

**No exposure report had ever been run on an all-candidates funnel** — every prior Steward report
counts *published* picks — so R1 was made **blocking for the lock** and measured it. It is delivered
and closed: `research/reports/STEWARD_Q027_exposure.md`, counts only, on the pinned freeze, no live
query (DP-50(c)).

| quantity | measured | source |
|---|---|---|
| **contributing nights per elapsed session, §2.5's complete definition** | **0.6761** (48/71) | **`STEWARD_Q027_exposure.md` (a) — the rate §5.2 is built on** |
| eligible nights per elapsed session (before the freeze's own maturity truncation) | 0.9577, with 100% (48/48) of matured nights converting | `STEWARD_Q027_exposure.md` (a) |
| funnel | 4,020 scored → 3,588 directed → 2,459 eligible on 48 matured nights | `STEWARD_Q027_exposure.md` (a) |
| eligible rows per night | min **39**, median **51**, max **64** | `STEWARD_Q027_exposure.md` (a) |
| contributing nights per elapsed session, published-pick funnel (Q023, superseded here) | 0.9538 (62/65) | `STEWARD_Q023_exposure.md` §5 |
| non-qualified candidate rows in `manifest_v001` | 5,572 over 102 nights | FREEZE_v001 §4 |

**Why the schedule uses 0.6761 and not 0.9577, in one line:** the 0.6761 is bound by the price
freeze's own forward-bar horizon — only 48 of the 68 non-excluded nights could mature to t+20 by
2026-09-10 — while 0.9577 is an **upper bound obtained by extrapolating past that horizon**, and
DP-45 takes the directly measured number because the extrapolation is the one that would pull the
decision date **in** (it would decide around 2027-02-22, seven weeks earlier). The draft's borrowed
0.9538 and its 8-session cushion are **superseded, not defended** (Correction 6): a cushion on a
borrowed number is not evidence, and the measured rate moved every date **out** (DP-43, DP-45).

**Lock-or-DEFER gate: CLEARED.** The floor requires ≥ **0.36** contributing nights per elapsed session
— 80 nights over the ≈ 225 elapsed sessions still admissible under DP-43's 12-month ceiling, solved at
the actual lock date of 2026-09-14 and rounded up (Correction 5). Measured **0.6761**, clear by 88%.
Below that line Q027 would have gone to `research/questions/DEFERRED.md` unregistered, with the
measured rate and the implied date named.

### 5.2 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13; no outcome is looked at)

**Window: pick nights 2026-09-15 .. 2027-03-05 inclusive = 119 elapsed sessions.**
**Decision date: Monday 2027-04-12.** Single DP-13 extension to pick nights **.. 2027-04-19**
(149 sessions), decided **Monday 2027-05-24**, which is also the **hard stop**: still short there,
Q027 goes to DEFERRED. Every date below is computed from R1's **measured** 0.6761 contributing nights
per elapsed session and moved **out** from the drafted schedule (2027-03-08 → 2027-04-12;
2027-04-19 → 2027-05-24). **Out is the only direction a correction may ever move them** (DP-43,
DP-45).

| floor | measured rate | sessions needed | date | binding? |
|---|---|---|---|---|
| **A:** ≥ 80 contributing nights, per primary endpoint (DP-21) | 0.6761/session | ceil(80/0.6761) = **119** | **2027-03-05** | **yes — window end** |
| **B:** ≥ 30 contributing nights dated after the lock commit (DP-24) | 0.6761/session | 45 | 2026-11-16 | no; satisfied by construction (every night is post-lock) |
| **C:** ≥ 20 contributing nights per *reported* sub-cell | 0.6761/session | — | — | checked cell by cell on measured counts at the decision pass; the closed list is §4.3 |

**Arithmetic, session by session** (holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18,
2027-02-15, 2027-03-26; and 2027-05-31 for the extension path):

- **Window.** 2026-09-15 is session 1; session **92 = 2027-01-26** and session **84 = 2027-01-13**
  (the drafted arithmetic, cross-checked by the Steward and unchanged), and session **119 =
  2027-03-05** (Friday). Floor A binds exactly there, so the window end **is** the floor date: there
  is no cushion, by design — a cushion on a measured rate would be a second, unregistered floor, and
  DP-13's single extension is the registered fallback for a measured shortfall.
- **Decision date.** 2027-03-05 **+ 20 sessions** maturity = **2027-04-05**; **+ one calendar week**
  freeze margin = 2027-04-12; first Monday on or after = **Monday 2027-04-12** (not a market holiday;
  a date landing on one moves **out** to the next Monday, never in). That is **6.9 months from the
  lock**, inside DP-43's 12-month ceiling (2027-09-14). `eval.py` is written once (rule 9) and run
  **once**, then. **No interim looks.**
- **Extension (DP-13; DP-43's +30 sessions).** If either floor is short at 2027-04-12 on `eval.py`'s
  **own measured counts** (never on a projection or a run-rate), the window extends **once**,
  automatically and with no new question, to pick nights **2026-09-15 .. 2027-04-19** (session 149),
  decision **Monday 2027-05-24** (2027-04-19 + 20 sessions = 2027-05-17; + one week = 2027-05-24;
  first Monday on or after — 2027-05-31 Memorial Day falls after it, so no further move). The extended
  run uses the **byte-identical, unmodified `eval.py`** and the same floors. 8.3 months from lock,
  inside the ceiling.
- **DEFERRED fallback (the hard stop).** If a floor is still short after that single extension, Q027
  goes to `research/questions/DEFERRED.md` with the measured counts rather than running
  under-powered. **No second extension, no reduced floor, and a floor shortfall is never an
  INCONCLUSIVE verdict** (§8).
- **Pin at the decision date.** The population enters only through §5.3 R2's successor freezes, so the
  DATASET_PINNED step runs at the decision date on those manifests (`pin_at_decision: true` in
  `schedule.json`, the Q024 pattern). The two v001 manifests pinned today cover the sealed post-hoc
  panel and R1 only.
- **Fixed at lock and not reopened at the decision pass:** both MPEs (§4.2, §8); the band cuts and the
  band-inversion blocker (§4.3); the ≥ 30-eligible-rows contributing-night rule; the 10-session block
  length; the seed 20260914; `m = 2` (§7); the four exclusion criteria (§2.4); and the **sub-cell
  suppression list** (§4.3), revised once at `record` from R1's measured counts and then **closed** —
  a suppressed cell stays suppressed even if it clears 20 measured nights, and a cleared cell still
  needs 20 measured nights to print.
- **If a weights, timeframe-multiplier, `qualification_threshold`, ATR-elite-cap, GEX-offset or
  scoring enable-flag change ships mid-window**, `overall_score` is **two different features** and the
  window is **cut at the ship date**: the post-ship segment becomes the question's window with this
  whole schedule recomputed from it — **out, never in**, subject to the same single extension and the
  same 12-month ceiling measured from the original lock — the pre-ship segment becomes a labelled
  descriptive panel entering no verdict, and if neither segment reaches the floors inside the ceiling
  the question is **DEFERRED** (DP-06's pattern, DP-50(a)). `eval.py` **fails loudly** on any
  cross-freeze disagreement in `overall_score`, `conflict_penalty` or `dominant_direction`, and on any
  row whose `score_details_json` re-derivation differs from `overall_score` by more than 0.05.
- **No such split exists at the lock, and it was checked rather than assumed** (DECISIONS item 12, on
  R1(g)): the code sweep since `fa70688` over the three SAS files returns **NONE** (4 commits, none
  touching them), every scoring field — weights, timeframe multipliers, `qualification_threshold`,
  both ATR-elite caps, the GEX offset, the enable-flags — is **constant across all 71 in-window runs**
  in `sas_runs.config_json`, and `outcome_corrections` touch `overall_score` / `conflict_penalty` /
  `dominant_direction` on **0 of 125** rows across the entire frozen history. The two `config_json`
  changes R1 found are **publication gates, not scoring**: `bear_publish_threshold` null→80.0 effective
  2026-06-29, and `publication_floor` null→80.0 effective 2026-07-08 (ship `1765a6f` 2026-07-07,
  already dated in `DATA_NOTES.md`). Both were live **more than two months before this window starts**,
  so neither falls inside it and neither splits it.
- **A `publication_floor` or `bear_publish_threshold` change is not a scoring split — and that clause
  is load-bearing, not ceremonial.** It changes which rows are *published*, not which are scored, so
  the window is not cut; but it changes `d*_t`'s **source cohort**, and R1(c) measures that cohort's
  median distance moving from **1.06 to 2.10 ATR** across the 2026-07-08 ship with no scoring field
  moving at all. So if either gate moves inside the prospective window: the per-night gate values are
  read from `sas_runs.config_json`, the `d*_t` series is printed pre/post, and **both primaries are
  printed split at the ship date as a labelled descriptive panel** — no verdict split, no new blocker,
  and no reopening of the suppression list.

### 5.3 Routed requests

- **R1 → data-steward (counts only; was blocking for the schedule and for the lock-or-DEFER gate).
  DELIVERED and CLOSED, 2026-09-14 — `research/reports/STEWARD_Q027_exposure.md`.** Nothing further is
  asked of it; its numbers are applied in §2.2, §2.4, §2.5, §3, §4.3, §5.1, §5.2 and §10. The request
  as issued, for the record:
  Measured on `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, over pick
  nights **2026-06-01..2026-09-10**, denominators in **elapsed sessions** with exclusions not
  pre-removed (the Q019 / Q022 / Q023 convention). No outcome of any kind is read; no live query
  (DP-50(c)). Required:
  (a) the §2.4 funnel re-derived under *this* population — eligible rows per night after the
  direction, 60-prior-bar and gradeability screens, and **contributing nights per elapsed session**
  under the ≥ 30-eligible-rows rule;
  (b) the **`mixed`** share of scored rows, overall and **per score decile**, and the count of nights
  above the 25% mixed threshold;
  (c) the `d*_t` series: nights with ≥ 3 screened published picks, the median `d_L3` distribution
  whole and by direction, and the count of nights that would fall back to the trailing median or be
  excluded — **including** the split-scale screen's removals (DATA_NOTES);
  (d) the **score-resolution panel**: per night, score IQR, the share of rows at exactly 84.9 / 79.9,
  the share with null `gex_alignment_score`, and the **band composition** (`< 70` / `70–80` /
  `80–85` / `85–90` / `≥ 90`) **at candidate level**, so §4.3's suppression expectations are measured
  rather than assumed;
  (e) the **episode** structure (DP-51): distinct symbols per night, symbol-episodes at the ≤ 10
  session gap rule, and the episode-length distribution;
  (f) the `conflict_penalty > 0` share and the B5 matched-pool feasibility (nights with ≥ 1 penalized
  row having ≥ 1 unpenalized row within ±2.0 base-score points);
  (g) the **DP-50(a)/(b) commit sweep** since manifest SHA `fa70688` over
  `services/super_agent_select_scoring.py`, `services/super_agent_select_models.py` and
  `services/sas_conviction_card.py` — weights, timeframe multipliers, `qualification_threshold`, the
  ATR-elite caps, the GEX offset, the scale-out fractions — with an explicit answer **even when it is
  "none"**, and a dated `DATA_NOTES.md` entry for any repair that rewrote historical rows.
  **The lock-or-DEFER gate R1 decided:** the DP-43 ceiling solved at this lock date leaves ≈ **225**
  admissible elapsed sessions, so the floor required **≥ 0.36 contributing nights per elapsed
  session** — an inequality, re-solved at `record` at the actual lock date and unchanged
  (Correction 5), not a constant. **Measured 0.6761 → Q027 locks**, and §5.2's dates are recomputed on
  the measured rate, **moving out only** (a faster rate would have changed nothing; DP-43, DP-45).
  Below the line Q027 would have gone to `research/questions/DEFERRED.md` unregistered.
- **R2 → data-steward (due before the decision date; not a blocker for lock; DP-23). Re-issued at
  `record` with final dates.** Successor freezes `manifest_v00N` (selections: same SQL, same exclusion
  criteria, **every candidate row published and unpublished**, plus `sas_runs` and
  `market_regime_daily`) and `manifest_prices_v00N`, covering pick nights **2026-09-15..2027-03-05**
  with **20 forward sessions** beyond the last included pick night (daily bars through
  **2027-04-05**) and **≥ 60 prior sessions** before 2026-09-15, delivered before
  **Monday 2027-04-12**; a second pair **only if** the DP-13 extension fires, covering
  **.. 2027-04-19** with forward bars through **2027-05-17**, delivered before **Monday 2027-05-24**,
  built then and not before. Four scope requirements, none optional:
  **(i)** the daily symbol list covers **every candidate symbol on every in-window night, published
  and unpublished** — this is the whole population, not a control cohort, and it is never assumed
  from v001's symbol list; **(ii)** no hourly bars are required (no primary or secondary uses one),
  so the Steward says so explicitly rather than building them; **(iii)** an **add-only successor
  exclusions file** applying the identical criteria to post-lock nights — now **four** lists,
  `manual_runs`, `non_session_runs`, `uncorroborated_publication_runs` and **`payload_disabled_runs`**
  (§2.4; the 2026-06-02 `analysis_status = "disabled"` / no-`lane_plans` signature, recurring
  2026-04-01, 2026-05-01, 2026-07-02), with the file's header note stating **whether the signature is
  still present after 2026-09-10** and whether it is still a first-published-night-of-the-month
  pattern — if it has stopped, said explicitly rather than returned as a silent empty list;
  **(iv)** rows whose bars are missing are **excluded and counted, never
  back-filled or imputed**. Where a successor freeze overlaps an earlier one on `sas_candidates`,
  the rows are compared and `eval.py` **fails loudly** on any disagreement in `overall_score`,
  `conflict_penalty` or `dominant_direction` — a repair that rewrote a score would silently re-run
  the experiment (DP-50(a)). R1(g)'s commit sweep is **repeated for the period between the freezes**.
  Every §5.2 date is re-confirmed session by session from the trading calendar when the freeze is
  built; a correction may move a date **out, never in**.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights 2026-09-15 .. 2027-03-05** (119 elapsed sessions,
  §5.2; .. **2027-04-19** if the single DP-13 extension fires), opening on the first
  session after the lock commit dated 2026-09-14 (the window starts on 09-15 rather than 09-14 so
  that no night whose 16:05 ET run may precede the lock commit can enter), through §5.2's end.
  *Justification, and it is not optional here.* The sealed period **has already been read for this
  hypothesis**: the weekly snapshots of 2026-09-10 and 2026-09-12 printed band-level returns for
  published picks (H-010's BACKLOG line: the 90+ lead as an April–May effect, with pooled 12-week W20
  figures per window), and CLAUDE.md's standing findings already carry "the 88–90 band underperforms
  90+" and "champion symbols graded below base rate". The top of the score distribution has been read
  against outcomes, and both the band secondary and E2's top tercile live there. Those nights are
  **not used for any verdict**.
- **The sealed post-hoc panel** (`manifest_v001` + `manifest_prices_v001`, pick nights
  **2026-06-01 .. 2026-08-12** — after the DP-06 catalyst split, and 08-12 is the 20-session maturity
  cutoff of the pinned price freeze) prints every §4 endpoint **once**, labelled, and enters **no
  verdict, no CI comparison, no half, no stratum test, no q and no §9 rule**. It is split at
  **2026-07-06** into sub-panels **A = 2026-06-01..2026-07-03** and **B = 2026-07-07..2026-08-12**
  and the halves are never blended: `_enforce_ladder_monotonic` shipped on 2026-07-06 (25.71%
  non-monotonic ladders before, 0.00% after — DATA_NOTES, Q018 R1), and the ladders are what `d*_t`
  is computed from. 2026-07-06 is itself excluded in `exclusions_v003`, so the boundary needs no
  tie-break. Each sub-panel is SUPPRESSED below 20 contributing nights.
  **The same boundary now brackets a second ship, and R1(c)'s measurement is reproduced inside the
  panel** (DECISIONS items 7 and 12): `publication_floor` null→80.0 took effect 2026-07-08 (ship
  `1765a6f`, 2026-07-07), with only 2026-07-07 between the two ships, and the night's common distance
  `d*_t` moved from a median of **1.06 to 2.10 ATR** across it. R1(c)'s three-segment `d*_t` table is
  printed in the panel. It remains a **description and enters no verdict**; it sits entirely in the
  sealed stretch, months before the prospective window opens.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date (re-derived from the final window at the decision pass); Half B = after.
  Both primaries must carry the same sign in both halves (§8 clause 8). The halves are a **stability
  clause, not a reported stratum**, and block at whatever count they have.
- **Monthly blocks (H-073's "≥ 60% of out-of-sample windows"):** calendar months of the window with
  ≥ 10 contributing nights; the share with the same sign as the full-sample estimate is §8 clause 10.
  At the registered length and the measured 0.6761/session, the qualifying blocks project as
  **October through February — five of them** (September is a part-month of 12 sessions ≈ 8
  contributing nights and March a stub of 5 ≈ 3, both short of 10), so the clause reads as "at least
  3 of 5"; if six qualify it reads "at least 4 of 6". The count is **stated numerically at the
  decision pass from the measured block count**, with the rule (≥ 60%, rounded up) fixed here and not
  reopened.
- **Regime stratification (rule 7).** Two stratifiers, both reported, both subject to §4.3's
  ≥ 20-night rule:
  - `market_regime_daily.market_regime`, **v1.2 only**, the row with `trading_date = t`, legal only
    where `created_at` falls on that `trading_date` **and at or before that night's own
    `sas_runs.finished_at`** (the Q023 §2.2 timestamp test). A night with no legal label keeps its
    place in the primary — the label is a **stratifier here, not a filter and not an arm** — and is
    reported in an `unlabelled` **count**, which is **not a reportable cell** (§4.3): the
    pre-2026-06-09 backfill cannot occur inside a window starting 2026-09-15
    (`exclusions_v003.regime_label_point_in_time_from`; FREEZE_v001 §7), so the backfill hazard cannot
    reach this window. On the closed list, `strongly_bullish` (projecting 48.6 nights) and `bullish`
    (23.5) print; `bearish`, `neutral` and `risk_off` are **SUPPRESSED as structurally absent** —
    0 of 48 measured nights, not merely thin.
  - **`tape_t`**, the SPY proxy, trailing and legal at 16:05 ET: sign of SPY's trailing 20-session
    return × tercile of its trailing 20-session realized volatility, from `prices_daily_split` bars
    dated ≤ t, with **expanding-window** tercile cut points (for night t, from every session
    2026-03-02..t), so no later night's data sets an earlier night's stratum. **Five of the six cells
    are SUPPRESSED on the closed list** (§4.3) — `up_low` 16.8, `down_high` 13.4, `up_high` 8.4,
    `down_mid` 6.7, `down_low` 5.0 projected contributing nights at session 119 — and print as counts
    only; **`up_mid` (30.2) prints**, subject to its own ≥ 20 measured nights.
- **Knowledge time (rule 14) — every input declared. Q027 needs no rule-14 exception and requests
  none** (DP-05 untouched, DP-41 respected).

  | input | source | available | use |
  |---|---|---|---|
  | `overall_score`, `dominant_direction`, `conflict_penalty`, subscores, `qualified`, `selected_rank`, `confidence_level`, `best_timeframe` | `sas_candidates` (all rows) | pick night, 16:05 ET | ranking variable, eligibility, strata |
  | `public_payload_json.lane_plans.swing_trading.targets[0]` (published rows) | `sas_candidates` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | `d*_t` only |
  | `C_t`, ATR14, beta60, runup20, mom20, adv20, SPY tape | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | distances, balance table, `tape_t` |
  | `market_regime` (v1.2, `trading_date = t`) | `market_regime_daily` | declared 16:05 ET / lag 0, verified FREEZE_v001 §7 for nights ≥ 2026-06-09, enforced per night by the timestamp test | rule-7 stratum only |
  | `finished_at`, `config_json` | `sas_runs` | publication time | DP-04 exclusion; config audit |
  | session t+1 open `X`; daily bars t+1..t+20 | `prices_daily_split` | after the pick night | **entry and outcome measurement only** |

  **What `eval.py` must enforce:** the eligible-row set, `d*_t`, every synthetic target, the tercile
  and band assignments, the episode ids and every stratum label are computed and written to a frozen
  per-row and per-night table **before any post-pick-night bar other than the t+1 open is loaded**,
  and the t+1 open is used **only** as the entry price `X` — never to filter, classify, rank or
  stratify. The run fails if any t+1-or-later field is referenced in eligibility, ranking, tercile
  assignment or stratification.

## 7. Multiple testing

- **Within the question: BH across m = 2** — E1 and E2 — at q ≤ 0.10; the verdict uses q. **`m = 2`
  is fixed at lock**: both endpoints carry a verdict in every branch, an endpoint short of floor still
  has its p computed, and no primary is dropped afterwards (dropping one would lower the bar for the
  survivor). Every secondary and every stratum in §4.3 prints raw p only, marked *"descriptive, does
  not decide"* — including all four adjacent-band contrasts and the whole conflict-penalty stratum.
- **Across the family: F2 Calibration.** F2 holds H-010, H-011, H-012, H-013, H-014, **H-073**,
  H-079, H-080, H-082 — with H-010 and H-012 **merged into Q027** (DP-29) and therefore counted once,
  here. The F2 correction set is computed at the decision pass over the F2 questions locked by then
  and **never shrinks below the 4 primaries registered at this lock and at Q023's**: Q023 (2) +
  Q027 (2) = **4**. **Q005 is excluded**, for the stated reason and not by assumption — a diagnostic
  decomposition with no MPE, no directional primary and no outcome column read at all, so it
  contributes no testable primary. If H-011, H-014, H-079, H-080 or H-082 lock before the decision
  date **2027-04-12**, their primaries join the set and the q's are recomputed on the larger m. The
  set **never shrinks** (DECISIONS item 13, rule 8, DP-29).
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q006 (F1)** contrasts *published picks* against distance-matched *unpublished* controls. Q027
    contrasts candidates against each other by score. A positive E1 is **not** a second confirmation
    of a selection edge, and a Q006 confirmation does not imply the score orders anything: SAS could
    pick well and rank badly, or rank well and publish a cut that throws the ordering away. Neither
    may be quoted as support for the other.
  - **Q024 (F1)** benchmarks the published slate against SPY, equal-weight, sector-matched random and
    momentum ranks, at slate level with a money gate. Q027's **B3** `mom20` comparator is a
    descriptive rank correlation over candidates and **confirms nothing about Q024**, in either
    direction.
  - **Q023 (F2)** tests the 80–90 band × the `strongly_bullish` label. Q027's population contains
    Q023's, and the band secondary shares ingredients with it; the regime stratum here is a reported
    cell, not an arm, and the two questions may not be read as one.
  - **Q015 (F7)** grades the 85–90 sub-band's path shape on the same level and clock with no ranking
    claim. The band touch rate is a shared ingredient, not a shared test.
  - **Q005 (F2)** decomposes the score distribution and reads no outcome column, so it cannot
    contaminate this question; it is also where the score-compression facts in §10 threat 2 come from.
  - **H-075 (F1, unregistered)** owns the **per-layer** ICs and the leave-one-layer-out re-ranking.
    Q027 computes **no layer-level IC**, precisely so that H-075's primaries stay its own and the
    forking paths stay closed.
  - **H-080 (F2, unregistered)** owns the walk-forward threshold-stability test. A monotone band
    profile here does **not** confirm that 90 is a real boundary, and a band inversion here does not
    refute it.
- Threshold: **q ≤ 0.10**, alongside raw p (rule 8).

## 8. Decision rule (numeric, written before unsealing)

`E1` is in **Spearman-ρ units**, the mean per-night rank correlation of `overall_score` with the
path-outcome rank `u_i` over 20 sessions from the t+1 open. `E2` is in **percentage points of
top-minus-bottom tercile touch rate** at the night's common ATR distance. Both over §2.5's
contributing nights. Both two-sided. H-073 predicts `E1 > 0` and `E2 > 0`.

**MPE — E1 `|ρ̄| ≥ 0.05`** (Haci's number, Master Hypothesis Program H3; §4.2 states the source, and
the *general* IC-unit rule is a proposal in `DECISIONS.md`, not a DP entry and not a dependency of
this file). **MPE — E2 ±5.0 pp** (DP-20 — a single within-night difference of two touch rates at an
identical ATR distance, the Q006 E1 shape, so the doubling clause does not apply). **Neither MPE is
lowered at the decision pass in any branch**, including one where it turns a CI-excludes-zero result
into INCONCLUSIVE. That is what an MPE is for (rule 6).

Per endpoint, **HISTORICALLY_CONFIRMED** requires **all** of:

1. **contributing nights ≥ 80** and **≥ 30 dated after the lock commit** (DP-21, DP-24), with ≥ 20
   **measured** contributing nights for any sub-cell that is *reported*. A sub-cell below 20, or one
   on §4.3's lock-fixed closed suppression list, is **SUPPRESSED** (counts only) and does not by
   itself make the endpoint INCONCLUSIVE; **suppression restricts affirmative reporting only and never
   removes clauses 5–10's blockers** — clause 9 in particular runs on measured counts for suppressed
   and unsuppressed bands alike;
2. **≥ 30 eligible rows on every contributing night** and both terciles non-empty (§2.4) — a
   mechanical gate on the statistic's meaning, checked per night, with violating nights
   non-contributing;
3. `|E| > MPE` — `|E1| > 0.05`; `|E2| > 5.0 pp`;
4. the **date-clustered bootstrap 95% CI excludes 0**, and the within-night score permutation p
   (B1) supports it;
5. **the episode-clustered 95% CI (DP-51, §4.4) also excludes 0.** A primary that clears MPE on the
   date-clustered CI and not on the episode-clustered one is **INCONCLUSIVE, never CONFIRMED**;
6. the endpoint's **blocking companion** is not beyond MPE in the opposite sign. For **E1** that is
   the **binary-outcome IC** (§4.3), which must not run beyond `|ρ| = 0.05` the other way. For **E2**
   it is the **touch-within-5-sessions tercile contrast**, which must not run beyond **5.0 pp** in the
   opposite sign. The companion is stated in a unit that **has** an MPE: DP-44 gives
   sessions-to-first-touch differences no MPE, so those distributions are descriptive and **no blocker
   anywhere in this question is expressed in session units**;
7. the **"mixed graded long"** version of the endpoint is not beyond MPE in the opposite sign
   (§2.4) — the guard on excluding the unresolved-direction rows;
8. the **bull-only** version is not beyond MPE in the opposite sign, and the point estimate has the
   **same sign in both halves** (§6) with neither half beyond MPE in the opposite sign;
9. **no material band inversion** (§4.3): no adjacent-band contrast with ≥ 20 **measured**
   contributing nights sits below −5.0 pp with its own 95% night-clustered CI excluding 0. The test is
   computed for **every** adjacent pair meeting that count, **whether or not the band is on the
   lock-fixed suppression list** — suppression restricts affirmative reporting and never removes a
   blocker (Correction 2). This clause implements H-073's own *"materially non-monotonic → FAIL"* and
   blocks the **question-level** verdict even where both primaries clear everything else;
10. the **monthly-block stability clause** (§6): the share of qualifying monthly blocks carrying the
    same sign as the full-sample estimate is **≥ 60%** (rounded up on the measured block count) —
    H-073's *"positive in ≥ 60% of out-of-sample windows"*, registered as a blocking clause rather
    than a reported statistic;
11. **BH `q ≤ 0.10`** within the question (m = 2) **and** within F2 (§7).

- **NULL (per endpoint):** floors and clause 2 met, **both** CIs include 0, **and** `|E| < MPE`.
  *"The SAS score does not order outcomes"* is a real finding — it is H-073's own FAIL branch, it has
  direct product consequences (§9), and it is ledgered with the same care as a positive.
- **INCONCLUSIVE (per endpoint):** anything else — a date-clustered CI that excludes 0 while the
  episode-clustered CI does not (clause 5), halves disagreeing in sign, a blocking companion beyond
  MPE in the opposite sign, fewer than 60% of monthly blocks agreeing, `0 < |E| ≤ MPE` with a CI
  excluding 0 ("real but below MPE", rule 6), or a CI including 0 with `|E| ≥ MPE`.
  **A floor shortfall is never INCONCLUSIVE** — it fires the single DP-13 extension, then DEFERRED
  (§5.2).
- **Question level.** CONFIRMED only if **both** primaries are CONFIRMED with the same sign **and**
  clause 9 holds. E1 confirmed with E2 NULL is reported as *"the ordering carries information that the
  tercile cut does not convert into a touch-rate gap"* and licenses no ranking claim; E2 confirmed
  with E1 NULL is reported as *"the extremes differ but the score does not order the middle"* and
  licenses a **tier** statement only, never a ranking one (§9). Confirmed-with-opposite-signs is
  INCONCLUSIVE and is reported as a contradiction, loudly.
- **What a confirmed E1 does and does not mean (binding on the report).** A CONFIRMED-positive E1
  means *"within a night, SAS's score ranks candidates such that higher-scored names reach a target
  at the same ATR distance sooner, with a mean rank correlation of ρ"*. It does **not** mean the picks
  made money, it does **not** mean the published slate beats anything (Q006, Q024), and it does
  **not** license quoting the score as a probability. The tie structure, the touch base rate and the
  maximum attainable |ρ| must be printed beside any quoted ρ.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — it requires ≥ 30 contributing
  nights dated after this file's lock commit (DP-24, DP-21), which every contributing night here is,
  frozen in the successor manifests and never inspected earlier, reproducing the sign under the
  unmodified `eval.py`. The clause does not weaken. No subscriber-facing statement before that
  (rule 10); even then the basis is `NON_QUOTABLE` until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform presents `overall_score` as a precise number — a 0–100 conviction score with a
qualification threshold at 70 (`services/super_agent_select_models.py:85`), a publication floor at 80
(`:91`), an elite line at 90, a confidence label derived from it
(`services/super_agent_select_scoring.py:1425`) and a rank order on the card. **Nothing on the
platform tests whether that ordering holds**, and this question is the test. Rules below fire **only**
where §8 licenses them, and nothing subscriber-facing ships before PROSPECTIVELY_CONFIRMED (rule 10):

- **Both primaries CONFIRMED positive, clause 9 clean:** (a) a Manual Trading Guide line stating the
  measured IC and the measured tercile gap, with the tie structure, the base rate and the
  identical-ATR-distance construction printed beside them; (b) a **lane rule** — within a night,
  prefer the higher-scored name when two candidates are otherwise comparable, with the measured gap
  as its size; (c) an `INTERNAL_TOOL`, flag-off card field showing the night's within-slate score
  spread. No claim that the score is a probability, and no claim about the published slate versus any
  outside benchmark (that is Q006 and Q024).
- **Both NULL:** this is H-073's own FAIL branch and it has a concrete consequence — **stop presenting
  the score as a precise conviction ranking.** A brief is written to replace the numeric score on
  subscriber surfaces with a coarse tier or a categorical setup label (ENHANCEMENTS **EN-018**, which
  is already the gated home for setup labels), shipped flag-off with a byte-identical checksum on the
  old path and shadowed ≥ 20 trading days before any flip (rule 11). Rank order within a night stops
  being quoted. The weekly stops printing score-band panels as a signal. **This is a result, not a
  non-result.**
- **Either CONFIRMED negative** (the score orders outcomes backwards): the finding is published with
  that sign, the standing presentation is suspended immediately on the internal surface, and a brief
  is written to re-examine the aggregation (`_effective_dimension_weights`,
  `services/super_agent_select_scoring.py:682`) — a sign inversion at composite level is a scoring
  defect, and DP-07 sends the defect half to `PLATFORM_ISSUES.md` while the measurement stays here.
- **E2 CONFIRMED, E1 NULL:** a **tier** statement only — "the top third beats the bottom third by N
  pp" — and explicitly **no** ranking claim, no rank-order display change, no per-rank sizing.
- **E1 CONFIRMED, E2 NULL:** a calibration note only; no lane rule and no display change, because a
  ranking that does not survive a tercile cut is not tradeable as written.
- **A material band inversion (clause 9), whatever the primaries do:** the inverted adjacent pair is
  filed to `PLATFORM_ISSUES.md` with its measured contrast (DP-07), and no guide line, flag or quoted
  number may describe the score as monotone. If the inversion sits at the 90 line it is routed to
  **H-080** (threshold stability) as evidence, never treated as having answered it.
- **The conflict-penalty stratum licenses nothing on its own** (§4.3). A striking split there is a
  reason to register H-012 as its own question, not a reason to change the penalty.
- **The suppressed cells license nothing**, whatever they show — the five suppressed `tape_t` cells
  and the three structurally absent `market_regime` labels (§4.3's closed list). The `≥ 90` band is
  **not** suppressed on the measurement and is reported like any other band, but it is a **secondary**:
  a band result licenses no guide line on its own, and an inversion at the 90 line routes to **H-080**
  as evidence rather than being treated as having answered it.
- **Q027 is in flight from this lock until its decision date, and DP-50(b) applies to the platform in
  the meantime.** There is one database, and a repair or a config change rewrites what this question
  reads. Any platform change to the SAS weights, the timeframe multipliers,
  `qualification_threshold`, the ATR-elite caps, the GEX-missingness offset or the scoring
  enable-flags is **flag-off until Q027's decision date, 2027-04-12** (2027-05-24 if the single DP-13
  extension fires) — the PI-011 / Q010 pattern, checked before any fix brief is written. If such a
  change ships anyway it takes a dated `DATA_NOTES.md` entry naming the column, the date range and the
  ship SHA, and §5.2's window split applies (DP-06, DP-50(a)).
- **DP-49 binds every brief this question produces:** each check handed to the **coding agent** must
  be satisfiable from the platform repo alone — the test suite, a pure-function import,
  `git show --stat`, a file diff. Anything that reads or writes a table belongs in the brief's
  verification section, addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where a write
  is required. Where a frozen manifest covers the affected table, the brief names that parquet as the
  before-snapshot (DP-50(c)).
- Owner: implementer. Shadow period before any flip: ≥ 20 trading days.

## 10. Known threats to validity (registrar's own list)

1. **The outcome is mostly ties, and ties cap the statistic.** Most candidates on most nights will not
   touch, so `u_i` has one large tied block and `|IC_t|` is bounded well below 1. An MPE of 0.05 is
   therefore a bar on a *compressed* scale, and whether 0.05 is demanding depends on the touch base
   rate. The mitigation is disclosure, not adjustment: the per-night touch rate, the tied-block size
   and the **maximum attainable |ρ|** are printed beside every ρ, and `IC_t` is never rescaled by them
   (rescaling would silently move the MPE).
2. **Score resolution may be too coarse for a rank correlation.** The ATR-elite block pins scores at
   exactly 84.9 / 79.9 (`super_agent_select_scoring.py:1401-1423`), the +5 GEX-missingness offset
   fires on a large share of rows (`:1379-1399`), and Q005 measured the elite-candidate rate halving
   over the frozen window. If a night's scores cluster on a handful of values, the ranking being
   tested barely exists. §4.3's score-distribution panel and R1(d) measure it; a night whose score IQR
   is 0 cannot produce a defined ρ and is non-contributing. **Measured and not observed on the sealed
   stretch** (R1(d), counts only): score IQR median 25.04 with no night at IQR 0, the ATR-elite caps
   firing on 2 of 4,020 rows, null GEX at 0.99%. The panel still prints every night of the prospective
   window — the threat is recorded as not-yet-seen, not retired.
3. **Excluding `mixed`-direction rows truncates the bottom of the ranking.** `dominant_direction`
   defaults to `mixed` when the evidence does not resolve (`:1180`), which plausibly correlates with a
   conflict penalty and a low score — exactly the rows the IC needs at the bottom. The per-decile
   mixed share is printed and the "mixed graded long" version is a **blocking** companion (§8
   clause 7), but there is no version of this question in which an unresolved direction has a
   well-defined target, and that limit is stated wherever the IC is quoted.
4. **Identical ATR distance matches distance, not everything.** Rows still differ in price level,
   liquidity, beta and run-up, and `overall_score` is correlated with several of them, so a positive
   IC could be a volatility-structure artefact rather than ranking information. The balance table
   (§4.3) prints the standardized differences across terciles; **H-068 / Q025 is the question that
   would strip exposures properly, and it is DEFERRED** because the exposure-matched control does not
   exist on any night. So this threat is disclosed, not removed, and §9's lane rule is written as a
   within-night preference — the only form the evidence supports.
5. **Overlapping 20-session windows and recurring symbols.** The same names recur nightly and their
   forward windows overlap almost entirely; a night-clustered CI would treat one symbol's path as many
   observations. DP-51's episode-clustered CI is the answer and it is a **decision** clause (§8
   clause 5), not a footnote. It is expected to be materially wider than the date-clustered CI; if it
   is not, that itself is worth reporting. **Confirmed structurally by R1(e)** before any outcome is
   read: 400 symbols, 811 episodes, 70% of symbols recurring across more than one episode, longest
   episode 44 appearances over 71 sessions.
6. **The band secondary inherits H-010's calendar problem.** Bands drift with the tape and with the
   score distribution (the 70–80 band all but vanished after May), so a raw band comparison is a
   calendar comparison. Night-demeaning is the fix registered here, and it is why the band profile is
   a secondary with one blocking clause rather than a primary.
7. **Published rows are a non-random 13% of the population and they set `d*_t`.** The night's common
   distance is the median of the *published* picks' printed L3 distances, so the target distance is
   chosen by the engine for the top of the distribution and then applied to the bottom. That is
   deliberate — it is the distance Haci actually trades — but it means a systematic relationship
   between score and printed distance shows up as a level effect on the whole night, not as a bias
   between terciles. The `d*_t` series is printed, and the **published-only** and **unpublished-only**
   versions of both primaries are reported sub-cells.
8. **A score that has been rewritten.** The in-sample catalyst rescore and the E9a correction batch
   show `sas_candidates` rows are not immutable. `eval.py` re-derives each row's score from
   `score_details_json` where the layer subscores are present and **fails loudly** on a disagreement
   with `overall_score` beyond 0.05; the cross-freeze comparison (§5.3 R2) fails loudly on any
   overlap disagreement.
9. **Config drift inside the window.** A change to the weights, the timeframe multipliers, the
   ATR-elite caps, the GEX offset, `qualification_threshold` or a scoring enable-flag changes what
   `overall_score` *is*, mid-experiment. R1(g) swept to the lock and returned **NONE** — no commit
   touching the three SAS files, every scoring field constant across all 71 in-window runs, and
   `outcome_corrections` on 0 of 125 rows — and R2 sweeps between freezes; §5.2's split rule fires on
   any such ship, moving the window out, never in. The residual risk is the one the sweep cannot see:
   a **publication-gate** change moves no code and no scoring field but doubled `d*_t` across the
   2026-07-08 ship, so §5.2 records those gates per night from `config_json` and prints the `d*_t`
   series across any such date.
10. **One database (DP-50).** A platform repair between freezes can rewrite the scores this question
    ranks on. Rule 4's pinned manifests are what stands between that and a locked question, and §5.3
    R2's loud comparison is what detects it.
11. **The prospective window may not be representative.** Not quite six months is one stretch of tape,
    and rule 7's regime cells are thin at this length: **five of six `tape_t` cells are suppressed**
    on the measured projection, and three of the five `market_regime` labels were **absent from every
    measured night** — so the question may well produce a verdict with only `strongly_bullish`,
    `bullish` and `up_mid` printable beside it. A confirmed IC over **119 sessions** of one tape is a
    real but narrow finding, and §9's language is written to keep it that way; **H-082** (edge decay)
    is where the series is watched over time.
12. **A NULL here is consequential and will be argued with.** "The score does not order outcomes" is a
    product-level statement, and the temptation at the decision pass will be to find a sub-cell where
    it does. The suppression list is fixed at lock, `m = 2` is fixed at lock, and the monthly-block
    and half clauses are blockers rather than reported strata, precisely so that a null cannot be
    rescued by a cell chosen afterwards.

---

## Decisions before lock

Recorded in DECISIONS.md (2026-09-14, decide + record passes). Routed items still open: **R2 only**
(successor freezes and the add-only exclusions file, due before the decision date, not a blocker —
DP-23). R1 is delivered and closed (`research/reports/STEWARD_Q027_exposure.md`).

| # | Decision | Status | Outcome as applied |
|---|---|---|---|
| 1 | Target distance for the IC and the tercile contrast | DECIDED | **A** — one common ATR distance per night `d*_t`, applied to every candidate in its own ATR and direction (§2.2, §3 B2, §4.1) |
| 2 | The outcome variable the IC is computed against | DECIDED | **A** — the path rank `u_i`, with the binary-touch IC as a blocking companion (§2.3, §4.1, §8 clause 6) |
| 3 | The IC MPE and the standing rule behind it | DECIDED | `\|ρ̄\| ≥ 0.05` applied as registered from Haci's H3 line; the *general* IC-unit rule is a **proposal** in DECISIONS.md, not a DP entry (§4.2, §8) |
| 4 | The band-inversion clause | DECIDED | **A** — blocking on the question-level verdict, computed on **measured** counts for suppressed and unsuppressed bands alike (§4.3, §8 clause 9, §9) |
| 5 | The contributing-night row floor | DECIDED | **A** — ≥ 30 eligible rows per night; a shortfall is non-contributing and counted, not an exclusion (§2.4, §2.5, §5.2, §8 clause 2) |
| 6 | Unresolved-direction (`mixed`) rows | DECIDED | **A** — excluded and counted, per-decile share printed, "mixed graded long" blocking (§2.1, §2.4, §8 clause 7, §10 threat 3) |
| 7 | The window start (prospective-only) | **DEFAULTED** | Pick nights **≥ 2026-09-15**; the sealed stretch prints once as a labelled post-hoc panel split at 2026-07-06, entering no verdict (§1, §6). Cost: Q027 decides 2027-04-12, not now |
| 8 | Window end, decision date, extension, lock-or-DEFER | **DEFAULTED** (settled at `record` on R1) | **LOCKS.** Measured 0.6761/elapsed session ≥ the 0.36 gate. Window **2026-09-15..2027-03-05** (119 sessions), decision **Monday 2027-04-12**, single extension to 2027-04-19 decided **Monday 2027-05-24** = hard stop, then DEFERRED (§5.1, §5.2). Every date moved **out** |
| 9 | Successor freezes | ROUTED → data-steward (**R2, open**) | Dates final; four scope requirements; the exclusions file now carries four lists (§5.3 R2) |
| 10 | Demotion, and the sub-cell suppression list | DECIDED | **Neither primary is demotable.** Suppression list **fixed at lock and closed**: 8 cells suppressed (five `tape_t`, three absent `market_regime` labels); `≥ 90` and bear-only **print** — the rule is a measured count, not an expectation (§4.3, §5.2, §6, §8 clause 1) |
| 11 | Exclusions inside an entirely post-freeze window | DECIDED | v003 ∪ the add-only successor file, **four** criteria — the fourth is `payload_disabled_runs` (header, §2.2, §2.4, §5.3 R2) |
| 12 | A mid-window change to what `overall_score` *is* | DECIDED | Window cut at the ship date, out never in; **no split exists at the lock** — R1(g) returned NONE and both `config_json` changes are publication gates predating the window (§5.2) |
| 13 | The F2 correction set, and `m = 2` | DECIDED | `m = 2` fixed in every branch; F2 never shrinks below Q023 (2) + Q027 (2) = 4; H-010 and H-012 counted once, here (§7) |

**Nine corrections from `decide` and `record` are applied**, each one tightening a clause and none
weakening one: the E2 blocking companion restated in touch-rate units (§8 clause 6); suppression
stripped of any power to remove the inversion blocker (§4.3, §8 clause 9); every sub-cell's status
fixed at lock and closed (§4.3); "published" named as DP-28's predicate wherever it is used (§2.1,
§2.2, §2.4, §4.3); the lock-or-DEFER test stated as an inequality measured under §2.5's complete
definition (§5.1, §5.3); the borrowed rate and its cushion replaced by the measurement (§5.1, §5.2);
zero-survivor nights excluded whole rather than fallback-filled (§2.2, §2.4); the two
"expected to be SUPPRESSED" sentences struck as wrong on the measurement (§4.3, §6); and the schedule
rebuilt on the maturity-truncated 0.6761 rather than the 0.9577 extrapolation (§5.1, §5.2).
