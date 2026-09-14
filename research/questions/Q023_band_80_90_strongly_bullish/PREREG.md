# Q023 — band_80_90_strongly_bullish: do the platform's 80–90 picks do worse on nights its own regime engine calls `strongly_bullish`?

**Status:** DRAFT (lock by committing this file) — every decision is applied from `DECISIONS.md` (decide + record passes, 2026-09-13). No item is pending and nothing blocks the lock; the one routed item still open, R2 (successor freezes), is due **before** the decision pass and is not a blocker (DP-23).
**Decisions:** DECISIONS.md (2026-09-13) · exposure basis: `research/reports/STEWARD_Q023_exposure.md` (R1, counts only, measured on the pinned freeze — no live query stands behind any number in this file, DP-50(c))
**Family:** **F2 Calibration** (hypothesis **H-013**, filed in F2 in `research/BACKLOG.md`; DP-29 — the primary endpoint's subject is whether the score band is calibrated conditional on a published regime label, which is calibration).
**Manifest (selections, sealed post-hoc panel and R1 counts only):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices, sealed post-hoc panel and R1 counts only):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374)
**Manifest (the question itself):** the **successor selection and price freezes** named in §5 (DP-23) — `manifest_v00N` (selections, **plus `market_regime_daily` and `projection_pick_bullish_daily`**) and `manifest_prices_v00N`, covering pick nights **2026-09-14 .. 2027-02-25** with **60 forward sessions** beyond the last included pick night; a second pair **only if** the single DP-13 extension fires, covering **.. 2027-04-09**. **The primary window is entirely prospective: not one night that carries a verdict here exists in `manifest_v001`**, so the population enters *only* through those successor freezes, which the desk pins at the decision date (`pin_at_decision`, DP-23). The two v001 manifests are pinned now and are used for exactly two things, neither of which decides anything: the labelled sealed post-hoc panel (§6) and R1's counts-only exposure measurement (§5.1).
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, DP-22) **unioned with the add-only successor exclusions file issued with the successor selection freeze** — the identical three lists, built by the identical criteria, covering nights after 2026-09-10. The successor file may only **add** nights; no night is ever removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be (DECISIONS item 8). Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. DP-04 applies mechanically on top.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) · **Date:** 2026-09-13

---

## 1. Hypothesis (plain English)

**On the nights the platform's own market-regime engine calls the tape `strongly_bullish`, its 80–90
scored picks do worse than on other nights — they reach the swing target less often relative to
look-alike stocks that night, and the committed scale-out returns less per trade — so the score is
over-reading a tape that has already run.**

BACKLOG H-013 reads: *"The 80–90 band underperforms on nights the point-in-time regime label is
`strongly_bullish` — baseline: the same band on `bullish` / other point-in-time nights; and the
projection-bullish list on the same nights, to separate a SAS effect from a tape effect."* It names
no entry, no level, no clock, no plan and no decision. This PREREG fixes all of them (§2–§4) and
keeps both named baselines (§3).

**Two primaries** (§4), both night-level arm contrasts, both two-sided:

- **E1 — the edge.** The *within-night, control-adjusted* rate at which an 80–90 pick touches its
  printed swing target within 20 sessions, averaged per night, on `strongly_bullish` nights minus the
  same on other nights. This is the calibration claim: does the band's edge over same-night
  look-alikes shrink when the label says the tape is strongest?
- **E2 — the money.** The realized ATR per published pick of the platform's own committed SELECT
  scale-out, on `strongly_bullish` nights minus other nights. This is the claim a skip or sizing rule
  would need: does the band actually *pay* less on those nights, in absolute terms?

**Why both, and why neither alone is enough.** E1 with the within-night control strips the tape out
by construction — a night on which everything ran gives `E_t ≈ 0` exactly like a night on which
nothing did — so E1 can only say the *selection* is worse calibrated on those nights, never that the
band is unprofitable there. E2 keeps the tape in, which is what a trader feels, but a raw arm
contrast on a night-type defined by the tape is *partly* the tape — it is the **total effect** in
DP-12's sense, and DP-12 says a total effect is descriptive and licenses no rule on its own (§4.2,
§8 clause 9, §9). The two together are the finding; each alone licenses much less, and §9 says
exactly what each licenses.

**H-013 predicts both negative. Both are registered two-sided**: a result beyond MPE in the opposite
sign is a confirmed finding with the opposite sign, and would be at least as useful (it would say the
band is *best* on strongly-bullish nights).

**What was already seen, and why the window starts after the lock.** The desk's weekly snapshots of
2026-09-10 and 2026-09-12 already printed this contrast on sealed nights — fixed-horizon T+20 returns
for the 80–90 band by point-in-time regime label, on both entry bases, plus the projection-bullish
comparator (the figures are in the BACKLOG H-013 line). Those nights are contaminated for this
question. They are **not used**: the window is **prospective-only, pick nights ≥ 2026-09-14** (§6),
and the sealed stretch is printed once as a labelled post-hoc panel that enters no verdict. H-013's
own BACKLOG line reached the same conclusion ("probably needs prospective nights before a PREREG is
viable"); this file agrees with it and registers the prospective test rather than deferring.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first;
  the arm is a property of the *night*, so the night is also the unit the arm is assigned to.
- **Source tables (the successor selection freeze, §5):**
  `sas_candidates` — `trading_date`, `qualified`, `selected_rank`, `overall_score`,
  `dominant_direction`, `best_timeframe`, `confidence_level`,
  `public_payload_json` → `lane_plans.{day_trading, swing_trading, longterm_trading}.{entry, stop, targets}`,
  `outcome_target_invalid` (exclusion audit only), `score_details_json` (band-integrity check,
  §10 threat 8), `context_json`;
  `sas_runs` — `finished_at` (DP-04), `config_json` (the `publication_floor` / weights audit,
  §10 threat 11);
  `market_regime_daily` — `trading_date`, `regime_version`, `market_regime`, `raw_parent_regime`,
  `score_band`, `regime_phase`, `regime_confidence`, `data_quality`, `asof_close_date`,
  `effective_for_trading_date`, `secular_risk_score`, `created_at`;
  `projection_pick_bullish_daily` — the B3 panel only (§3), never a primary.
- **Source tables (the successor price freeze, §5):** `prices_daily_split` (pick-night close, ATR14,
  beta60, runup20, forward bars to t+60, SPY tape), `prices_daily_raw` (split-factor snapping only),
  `prices_hourly_raw` (published symbols; the intraday audit of the entry and the not-takeable count —
  **no primary depends on an hourly bar**, see §4).

### 2.1 Treatment rows — exact filter

**The two dates below are illustrative of values `eval.py` receives as inputs.** §5.3 R2 requires the
script to take the window start, the window end, the manifest paths and the exclusions-file paths as
arguments, with **no hard-coded date, manifest name or path**, so that the byte-identical script
serves the primary run and the DP-13 extension run alike (DECISIONS Correction 10(d)).

```sql
SELECT c.*
FROM   sas_candidates c
JOIN   market_regime_daily r
       ON  r.trading_date  = c.trading_date          -- DECISIONS item 1: the row the platform's own
                                                     -- consumer reads to gate a pick scored on t's close
       AND r.regime_version = 'v1.2'
JOIN   sas_runs run
       ON  run.trading_date = c.trading_date          -- for the §2.2 legality timestamp test
WHERE  c.qualified IS TRUE
  AND  c.selected_rank IS NOT NULL                   -- publication predicate, DP-28
  AND  c.overall_score >= 80.0
  AND  c.overall_score <  90.0                       -- half-open, no rounding; H-013's own cut (DP-25)
  AND  c.trading_date  >= DATE '2026-09-14'          -- §6 window start        (input, illustrative)
  AND  c.trading_date  <= DATE '2027-02-25'          -- §5 window end          (input, illustrative)
  AND  c.trading_date NOT IN (<exclusions_v003 ∪ the add-only successor exclusions file:
                               manual_runs ∪ non_session_runs
                               ∪ uncorroborated_publication_runs, read from the JSONs>)
  AND  r.market_regime <> 'unknown'
  AND  COALESCE(r.data_quality, '') <> 'insufficient'
  AND  r.created_at::date = r.trading_date           -- §2.2 legality, limb 1 (same-evening write)
  AND  r.created_at <= run.finished_at               -- §2.2 legality, limb 2 (written before the run
                                                     -- that published the picks) — DECISIONS item 1
```

Dark-lane rows (`qualified` false or `selected_rank` NULL) are **never** in any arm (DP-28); they are
counted in the §2.4 funnel and are available to the B2 control pool. `90+` is outside the population
by construction — it is the band H-013 is *not* about — and is **SUPPRESSED at lock**: structural,
because `publication_floor = 80.0` since 2026-07-07 and the elite trend is 12 / 8 / 3 / 2 picks per
month since June (DATA_NOTES). It can return no verdict and license no sentence (§4.3's lock-time
suppression list, §9).

### 2.2 Arm assignment — a property of the night, fixed at 16:05 ET

- **STRONG** iff `market_regime = 'strongly_bullish'`.
- **NOTSTRONG** iff `market_regime ∈ ('bullish','neutral','bearish','risk_off')` — H-013's
  "`bullish` / other" pooled (DECISIONS item 2, DP-25; the pooled form is the hypothesis as written,
  is the *noisier* and therefore harder comparator, and is the only one that still reaches the
  20-night arm floor if the tape turns). **§8 clause 8's 60% composition guard is fixed at lock** and
  may not be moved in either direction at the decision pass: if fewer than 60% of NOTSTRONG
  contributing nights carry `bullish`, the verdict is taken on the STRONG vs `bullish`-only contrast
  instead. On the sealed panel the guard is met trivially — R1 §3 measures the NOTSTRONG arm at
  **100% `bullish`** (0 `neutral`, 0 `bearish`, 0 `risk_off` in 65 sessions) — and it is still
  measured on the prospective window, where the tape may differ.
- **Legality of the night's regime row — a timestamp test, not a date test** (DECISIONS item 1). A
  night's row is legal only where **all** of: `regime_version = 'v1.2'`; `market_regime <> 'unknown'`;
  `COALESCE(data_quality,'') <> 'insufficient'`; **`created_at` falls on the row's own
  `trading_date`**; and **`created_at` is at or before that night's own `sas_runs.finished_at`**.
  Anything else — including a same-day row posted *after* the run that published the picks — is
  treated as **missing**, and the **night is excluded and counted**, in whole, under its own reason
  code. A late-written label is never a label. (A date-only test would pass a row written at 19:00 ET;
  the honest test is against the consumer that actually used it. R1 §4 measures **1 failure in 65
  in-window sessions** — 2026-07-06, written 2026-07-07 14:23 UTC, the FREEZE_v001 §7 exception, a
  night already excluded by `exclusions_v003.manual_runs` — and **0** nights carrying `unknown`,
  `insufficient` or no v1.2 row.)
- `market_regime` is the **smoothed** column the platform's own consumers read (volatilx
  `models.py:1854-1855`, `services/market_regime/scorer.py:500`); `raw_parent_regime` and
  `score_band` are **descriptive sub-cells only** and never assign an arm.
- **Arm composition is printed, per arm:** the night counts by label, by `regime_phase`
  (`impulse_up` / `pullback_in_bull` / …), the `secular_risk_score` distribution, and the number of
  **episodes** (§2.4).

### 2.3 Levels, entry, clock

- **Direction** `dir` = +1 bullish / −1 bearish from `dominant_direction`. Every distance and every
  touch is direction-adjusted.
- **`C_t`** = the pick's actual regular-session close on pick night t from `prices_daily_split`
  (never the platform's `spot_close`, stale on re-run nights — EXPLORE_001 §9).
  **`ATR`** = ATR14 from `prices_daily_split` bars dated ≤ t (never the platform's `atr_pct`,
  corrupted around splits — DATA_NOTES / PI-003).
- **Entry `X` = the session t+1 regular-session open** (DP-03(b), DP-42) — Haci's option-spread
  entry, and the basis on which this band is actually traded; it exists for picks and for
  distance-matched controls alike, which is what rule 5 requires. The **`C_t` basis (DP-03(a) /
  DP-11) is computed and printed for every endpoint as a named sensitivity** and never decides.
  **A level already through `X` at the open is not a hit** (rule 5) and is not a fillable exit
  fraction (§4); the count is printed per arm.
- **`L3`** = `lane_plans.swing_trading.targets[0]` — the printed swing first target (volatilx
  `services/sas_conviction_card.py:182-187`). `d_L3 = dir × (L3 − C_t) / ATR`.
- **The six-level ladder** `L1…L6` = the platform's own flattening, `day_trading[0], day_trading[1],
  swing_trading[0], swing_trading[1], longterm_trading[0], longterm_trading[1]`
  (`services/sas_conviction_card.py:182-187`), each graded on **its own lane window** —
  L1/L2 20, L3/L4 40, L5/L6 60 sessions (`_LADDER_LEVEL_WINDOW`, `:194`).
- **Clocks.** **E1: L3 within 20 sessions from `X`** (DP-09 — L3 is the primary level, so the primary
  clock is the 20-session spread horizon; the platform's own 40-session swing window is printed
  alongside, descriptively). **E2: the committed plan's own lane windows on a 60-session budget**
  (L1/L2 20, L3/L4 40, L5/L6 60 sessions from `X`), remainder closed at the session **t+60** close —
  DECISIONS item 3, DEFAULTED under DP-43: 40% of the SELECT scale-out sits in L5/L6, whose own
  windows are 60 sessions, so truncating the plan at 20 sessions would price the plan's deep half at a
  t+20 close and report a plan nobody trades. The cost is ~2 months of waiting, which DP-43 says is
  not a reason.
  **Binding maturity: 60 sessions, uniform across every eligible pick**, so nothing is right-censored
  by its own timing.

### 2.4 Exclusions — each counted, per arm, printed in the results header, never silently dropped

Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or a
measurement failure. None can move a pick or a night between arms.

- **Nights** in **the union of `exclusions_v003.json` and the add-only successor exclusions file**
  (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs` from both, DECISIONS item 8
  — every night of this window postdates the v003 freeze, so v003 alone would silently drop the
  `uncorroborated_publication_runs` and `non_session_runs` protections the sealed period gets), and
  any prospective night whose `finished_at` is later than the next session's open (DP-04),
  mechanically.
- **Nights with no legal regime label** by §2.2's **timestamp** test — excluded in whole, counted,
  listed by reason code (`unknown` / `insufficient` / no v1.2 row / written on a later date / written
  after that night's own `finished_at`).
- **Null-ladder denominator:** no lane plan, a missing lane, or fewer than six flattened levels →
  pick excluded and counted. (Scale: the Steward measured **495 six-level-eligible 80–90 published
  picks over 2026-06-01..2026-09-09** — DATA_NOTES, `STEWARD_Q018_exposure.md` §2 — ≈ 7 per night, so
  six-level eligibility is not a thin filter.)
- **Wrong-side or non-monotone ladder at the close:** any level at or through `C_t` in the pick's
  direction, or the six levels not strictly monotone in the direction, or `outcome_target_invalid`
  non-null → excluded and counted. The whole window sits after platform commit `5fa3db4`
  (2026-07-06), which ships `_enforce_ladder_monotonic`, so non-monotonicity is expected at ≈ 0%
  (DATA_NOTES: 25.71% before that commit, 0.00% after); a non-zero rate is a loud flag, not a silent
  drop.
- **Split-scale payload screen** (DATA_NOTES, the APH / KLAC / CRWD / MNST finding): a pick is
  excluded and counted if `lane_plans.day_trading.entry / C_t` is outside `[0.85, 1.15]` or any
  flattened level implies `|dir × (level − C_t) / ATR| > 20`. Decided from pick-night data only,
  applied identically in both arms.
- **Missing forward bars** inside t+1..t+60 (halt, delisting) → ungradeable, excluded and counted;
  this is a measurement failure, never a classifier. A night is dropped if > 25% of its eligible picks
  are ungradeable.
- **Fewer than 60 daily bars dated ≤ t** (ATR / beta60 / runup20 undefined) → excluded, counted.
- **Immature nights** — session t+60 after the last trading date of the pinned price freeze →
  excluded and counted. Maturity comes from the trading calendar, never from whether a price exists;
  right-censoring is never graded as a non-touch.

### 2.5 Contributing night, and the episode

- **Contributing night (the floor unit, DP-21; identical for E1 and E2):** a non-excluded night in the
  window carrying a legal regime label **and ≥ 1 eligible 80–90 published pick**, matured to t+60.
  A night that survives the night-level filters but carries no eligible pick is a **non-contributing
  night, not an exclusion** — printed in the funnel.
- **Episode — defined on the arm-label series, not on the contributing sample** (DECISIONS item 4):
  **a maximal run of consecutive *sessions* carrying the same legal arm label; a session with no legal
  arm label (unknown / insufficient / late write / missing v1.2 row / excluded night) does *not* break
  a run, and only a session carrying the *other* arm's legal label ends one.** An episode counts
  toward the §8 clause 2 gate **only if it contains ≥ 1 contributing night**, and it is resampled
  carrying its contributing nights (§4.4).
  *Why on the label series.* The regime label is smoothed by hysteresis (`promote_n` 3 of 5,
  `enter_bearish` 2, `exit_bearish` 3 — volatilx `services/market_regime/scorer.py:60`, `:386-420`),
  so nights arrive in runs, not independently; an episode is one draw of the tape. Defining it on
  *contributing* nights would let a single excluded night inside a ten-night stretch split one draw
  into two — the direction that makes the gate easier, which is the direction the desk does not take
  (DP-45).
  Episodes are the resampling and permutation unit (§4.4) and carry their own gate (§8 clause 2).
  **Measured, for scale only** (R1 §3, sealed panel, 65 sessions): STRONG 5 episodes of lengths
  [6, 4, 8, 2, 30]; NOTSTRONG 4 episodes of lengths [3, 4, 2, 5] carrying 13 contributing nights —
  **3.25 contributing nights per episode**, the number §5.2 sizes the window on.

## 3. Baseline(s) — what this must beat

- **B1 (primary, the arm baseline): the same band on NOTSTRONG nights** — "Y's rate when X did not
  happen", same window, same population, same plans, same grading, same control construction. This
  *is* E1's and E2's second term. There is no version of this question without it.
- **B2 (rule-5 distance-matched control, inside E1 by construction):** for each eligible pick, the
  **10 nearest same-night non-published `sas_candidates` rows** (the complement of the DP-28
  predicate) on `beta60` / `atr_pct` / `runup20` computed from `prices_daily_split` bars dated ≤ t,
  standardized by the night's cross-sectional median and MAD, Euclidean distance, with replacement
  across picks, ties broken by symbol ascending — **the Q006 §3 construction verbatim**. Each control
  carries a **synthetic target at the same ATR distance and direction** as the pick it matches,
  `L3_c = C_c × (1 + dir_p × d_L3,p × atr_pct_c)`, graded from the control's own session t+1 open with
  exactly the §4 rules, same direction, same 20-session window, and for E2's control panel a full
  synthetic six-level ladder at the pick's own ATR distances. Controls **never add to inferential n**
  (rule 6). A pick with fewer than **3** valid controls is dropped from E1 and counted, **never
  imputed**; the pool has been measured on this exact population and is not thin — R1 §6: mean 51.8,
  median 54, min 39, max 60 valid same-night non-published rows, **100% of nights ≥ 3 and ≥ 10**
  (consistent with `STEWARD_Q015_exposure.md` §8's median 54 / p10 42 / min 37). R1 §6 also confirms
  the **CTRA truncated-history signature** (last daily bar 2026-05-06, still appearing as a candidate
  to 2026-09-10): a control whose daily bars stop before the pick night fails the ≥ 60-prior-bars
  screen and is not a control; `eval.py` prints the count of candidates dropped for this reason per
  night, and the successor freeze repeats the scan (§5.3 R2).
- **B3 (H-013's second named baseline, descriptive, EVALUABLE-gated): the projection-bullish list on
  the same nights.** For each night, the same night statistic computed on
  `projection_pick_bullish_daily`'s published bullish list — synthetic target at the night's **median
  SAS `d_L3`** ATR distance from each projection pick's own `C_t`, graded from its own session t+1
  open over 20 sessions, against its own 10 nearest same-night non-published look-alikes — and the
  same STRONG − NOTSTRONG arm contrast. This is the "SAS effect or tape effect" separator H-013 asks
  for, and the successor price freeze is **extended to every `projection_pick_bullish_daily` symbol on
  every in-window night** so that it is computable (DECISIONS item 5, §5.3 R2; DP-25 names the
  comparator, DP-23 makes the freeze's symbol scope a build-cost question and not a trade-off about
  this question). **The ≥ 80% symbol-night coverage gate is fixed at lock** and is evaluated on the
  successor freeze's own coverage at the decision pass: below it `eval.py` prints
  `B3 = NOT COMPUTABLE` with the coverage figure and §9's SAS-specific language is barred. On the
  present freeze the gate is projected clear with a wide margin — R1 §7 measures **98.17%
  (913/930)** of projection-bullish symbol-nights already carrying ≥ 60 prior daily bars in
  `manifest_prices_v001`, *before* the successor freeze adds the explicit scope. **B3 never decides in
  any branch** — the within-night control in B2 is what removes the tape for validity purposes; B3
  governs only what the report is allowed to *call* the finding (§8's language clause, §9). With no
  B3, no sentence of the form "this is a SAS problem, not a market problem" may be written, and the
  result is reported as a property of model-selected momentum names on those nights.
- **B4 (the money baseline, inside E2 by construction): the band's own committed plan on NOTSTRONG
  nights.** One plan, two night-types, no plan contrast anywhere in this question — Q023 does not test
  an exit rule (that is F6's subject; §7).

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Nothing in this question is decided by a fixed-horizon return.** Close-to-close returns at T+5,
T+20 and T+60 from `X` are printed and are **descriptive by rule 5 and DP-01**; they are the basis of
the sealed panel that has already been seen (§6), which is exactly why they decide nothing here.

### 4.1 Per pick

- **`hit_p` (E1's raw ingredient)** = 1 if the regular-session high (bullish) / low (bearish) touches
  `L3` on some session in **t+1..t+20**, else 0. A gap through `L3` at a session open is a touch. A
  pick whose `L3` is at or through `X` at the t+1 open is **not-takeable**: `hit_p = 0`, it stays in
  the denominator, and the not-takeable count is printed per arm (rule 5).
- **`ctrl_p`** = the mean of `hit` over that pick's ≥ 3 matched controls, graded identically from each
  control's own t+1 open at the identical ATR distance.
- **`e_p = hit_p − ctrl_p`** — the pick's control-adjusted touch indicator, in rate units.
- **`r_p` (E2)** = the realized ATR per trade of **Plan S, the committed SELECT scale-out**: the
  platform's own published schedule for SCORE 80–89, fractions `[0, 15, 30, 15, 25, 15]` on
  `L1…L6` (volatilx `services/sas_conviction_card.py:203-218`; the guide's `BAND_EXITS` 85–88 row is
  the source of truth, `scripts/generate_sas_trading_guide.py:89-95`). Entry `X` for the whole
  position. Each fraction exits at **its own level's first touch inside that level's lane window**
  (L1/L2 20, L3/L4 40, L5/L6 60 sessions from `X`), at the level price, or at the session open where
  the session opens through it. A fraction whose level is at or through `X` at the open is recorded
  **unfillable** and is **not** reallocated — it rides to the end. Everything unexited at session
  **t+60** closes at that session's close.
  `r_p = dir × ( Σ_i w_i × (exit_i − X) ) / (ATR × Σ_i w_i)`, with `Σ w_i = 100`.
  **No stop, ever** (rule 5, DP-02): the plan holds through every adverse excursion. The trailing
  rules in the platform's note ("tighten trail after L4", "small L6 tail only") are **not
  deterministic enough to simulate and are ignored**; the plan is labelled *truncated* wherever it is
  reported.

### 4.2 Per night, then per arm

For contributing night t, with `P_t` = its eligible 80–90 picks:

- `E_t = mean_{p ∈ P_t} [ e_p ]`  (control-adjusted touch rate, percentage points)
- `R_t = mean_{p ∈ P_t} [ r_p ]`  (committed-plan realized ATR per published pick)

**Primary endpoints (two, pre-specified, BH-corrected within the question and across F2 — §7):**

- **E1 = mean_{t ∈ STRONG} E_t − mean_{t ∈ NOTSTRONG} E_t**, in **percentage points**.
- **E2 = mean_{t ∈ STRONG} R_t − mean_{t ∈ NOTSTRONG} R_t**, in **ATR per published pick**.

`E_t` is the quantity Q006 owns computed per night; the only thing Q023 adds to it is the arm
contrast (§7 — a non-zero E1 is **not** a second confirmation of a selection edge, and E1 can be large
while Q006's excess is zero, or the reverse).

**DP-12 and the two endpoints.** E1 is the **control-adjusted** contrast DP-12 requires as primary:
the conditioning variable is the tape, and B2's within-night control is matched inside it, so the
tape is stripped out by construction. **E2 is the total effect in DP-12's sense** — a raw arm
contrast on a night-type defined by the tape, with no control inside it. DP-12 says the total effect
is descriptive and licenses no rule; here that is implemented, not merely asserted, by two clauses:
§8 clause 9 makes a CONFIRMED E2 conditional on its **control-adjusted companion** (§4.3) not being
beyond 0.25 ATR in the opposite sign, and §9 cites DP-12 for why an E2-only result changes no engine
setting, no publication behaviour and no sizing.

### 4.3 Secondary and sensitivity output

Everything here is printed with raw p only and labelled *"descriptive, does not decide"* — **except
the four named blockers**, which are descriptive in the sense that no verdict rests *on* them, but
which **block** a CONFIRMED verdict when they run the other way (§8 clauses 6, 7, 9). Suppression
(below) restricts **affirmative reporting only**: it never removes a blocker, and a suppressed cell
never by itself makes an endpoint INCONCLUSIVE.

**Computed, and blocking (§8):**

- the **control-adjusted E2** — the same committed plan run on each pick's matched controls at
  identical ATR distances, subtracted per pick before the night mean; the money twin of E1. **§8
  clause 9:** a CONFIRMED E2 additionally requires this companion not to be beyond 0.25 ATR in the
  opposite sign (DECISIONS item 7, DP-12);
- the **`effective_for_trading_date = t` label** version of both primaries (the strictly-prior row,
  DECISIONS item 1), with the night-level agreement rate between the two labels printed beside it.
  **§8 clause 7, which binds unconditionally** — there is no disagreement-rate threshold below which
  it stops binding. (R1 §5 measures the sealed-panel agreement at **89.06%**, disagreement **10.94%**,
  all seven disagreements sitting exactly on arm-transition boundaries — which is precisely why the
  drafted 15% threshold was struck rather than kept.)
- the **bull-only** version of both primaries, with the per-arm direction mix (§10 threat 5) — **§8
  clause 6's opposite-sign blocker**;
- **Half A / Half B** (§6) — **§8 clause 6's stability clause.** It blocks at whatever count it has;
  it is not a reported stratum and is not on the suppression list.

**Computed, mandatory in the report, and purely descriptive:**

- the **raw (unadjusted)** arm contrast of the L3 touch rate, `mean_{STRONG} mean_p[hit_p] −
  mean_{NOTSTRONG} …` — what the tape did, printed beside E1 so the control's work is visible;
- the **`C_t` entry basis** (DP-03(a)/DP-11) for both primaries, with the not-takeable counts;
- **B3**, the projection-bullish panel (§3), or `NOT COMPUTABLE` with its coverage figure;
- the **trailing-tape-matched sensitivity** (§10 threat 2): STRONG and NOTSTRONG nights matched 1:1 on
  SPY's trailing 20-session return (±0.5 pp caliper) and trailing 20-session realized-vol tercile,
  E1 and E2 recomputed on the matched night pairs — the direct read on "is the label anything more
  than the run that already happened". It is a **matched recomputation, not a stratum**: it prints its
  matched-pair count, stays mandatory and stays descriptive, and where it has fewer than 20 matched
  night-pairs it prints **counts only**;
- per-level **L1…L6 first-touch rates and sessions-to-touch** on each level's own lane window, per
  arm, against the same controls; **maximum favourable and maximum adverse excursion in ATR** from
  `X`; counter-direction touches (reported, never an exit — DP-02);
- the **40-session** companion of E1 (the platform's own swing window, DP-09);
- **close-to-close returns** at T+5 / T+20 / T+60 from `X` — **descriptive by rule 5 and DP-01; they
  never decide**, and no verdict sentence may lead with them. This matters more here than usual: the
  sealed panel that generated H-013 *was* a T+20 return.

**Sub-cells — the list is FIXED at lock and does not reopen at the decision pass** (DECISIONS item 9,
fixed at `record` from R1's measured splits). One arithmetical fact drives most of it: the NOTSTRONG
arm is projected at **22.8 contributing nights against its own 20-night floor** (§5.2), so **no
sub-cell that splits that arm can reach 20**, and every such sub-cell is SUPPRESSED at lock — counts
only, no point estimate, no sign, not even "directionally" — and **stays suppressed even if it clears
20 measured nights at the decision pass**:

- **SUPPRESSED at lock:** `90+` (structural — §2.1); `neutral`, `bearish`, `risk_off` as separate
  labels (R1 §3: **0 nights of each in 65 sessions**); `regime_phase = pullback_in_bull` (R1 §3: all
  8 such nights are STRONG, so the phase contrast has an empty cell in one arm; ≈ 14.0 nights even
  pooled); `regime_confidence` terciles (≈ 7.6 each); `raw_parent_regime` vs `market_regime`
  disagreement nights (not measured by R1 — an unmeasured cell is never projected to clear, DP-45);
  80–85 vs 85–90; `d_L3` tercile; `atr_pct` tercile; and **bear-only** as a *reported* sub-cell.
- **NOT suppressed:** the **`impulse_up`** cell of the contrast (the only `regime_phase` cell that
  clears in both arms — STRONG ≈ 72 / NOTSTRONG 22.8 projected nights), and the **`bullish`-only
  comparator**, which on R1's measured 100% composition *is* the NOTSTRONG arm and clears at 22.8.
- **Never on the list, because they block rather than report:** the control-adjusted E2 companion, the
  `effective_for_trading_date` version, the bull-only version, and Half A / Half B (above).

**Quotability:** 20- and 60-session bases, W20 research windows → **every number in this question is
`NON_QUOTABLE`** (rule 12).

### 4.4 Inference

Night-level throughout; control rows never add to n (rule 6).

- **CI (decides): episode-block bootstrap.** Resample **episodes** (§2.5, defined on the arm-label
  series and **carrying their contributing nights**) with replacement within arm, 2,000 resamples,
  recomputing the arm means from the resampled episodes' nights. Episodes are
  the honest block here because the arm label itself is generated by a hysteresis filter, so
  consecutive same-arm nights are one draw of the tape, not twenty. A **stationary block bootstrap**
  over the ordered contributing nights (expected block length **10 sessions**, the Q004 / Q007 / Q009
  / Q011 / Q015 value, fixed here at lock and not chosen after seeing anything) and a plain
  date-clustered CI are printed alongside, and are expected to be *narrower*; where they disagree with
  the episode bootstrap, **the episode bootstrap is the one that decides**.
- **p-value (decides): episode-label permutation.** Permute the arm labels **across episodes**,
  preserving each episode's length and the night ordering inside it, 10,000 permutations, seed
  20260913. A naive night-level label permutation is printed alongside and labelled
  **anti-conservative**; it never decides.
- **Every estimate prints:** contributing nights total and per arm; episodes per arm and their length
  distribution; contributing nights dated after the lock commit; eligible picks per arm; not-takeable
  counts; unfillable-fraction counts by level; control rows used and picks dropped for < 3 controls;
  post-match standardized mean differences on `beta60` / `atr_pct` / `runup20`; exclusions by reason;
  and the per-arm regime-label / phase composition.

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** and ≥ **20
  contributing nights per arm**, plus ≥ 20 per reported sub-cell. A sub-cell below 20 is
  **SUPPRESSED** — counts only, no point estimate, not even "small n, directionally" — and a
  SUPPRESSED sub-cell does not by itself make an endpoint INCONCLUSIVE (§8 clause 1); the
  **suppression list is fixed at lock** in §4.3 and does not reopen. The weaker "80 eligible with
  ≥ 20 contributing" reading is not used. **No floor is ever lowered to reach a date.** On top of the
  night floors, §8 clause 2 requires **≥ 5 episodes per arm** (§2.5's label-series definition,
  DECISIONS item 4) — and an episode shortfall is a **gate**, handled by §5.2's single extension and
  then DEFERRED, never an INCONCLUSIVE verdict.
- **Neither arm is demotable** (DECISIONS item 9, DP-43). E1 and E2 *are* the STRONG − NOTSTRONG
  contrast, so an arm below 20 contributing nights leaves no endpoint: it is a floor failure — the
  single DP-13 extension, then DEFERRED — never a demotion to descriptive. Both arms are projected
  clear at the registered window length (§5.2), so no demotion is recorded at lock.
- **Binding maturity: 60 sessions** (E2's plan budget, §2.3), uniform across every eligible pick.
- **DP-24:** ≥ 30 contributing nights dated after the lock commit. Here **every** contributing night
  is post-lock by construction (§6), so DP-24 binds at 30 of the 80 and is not the gate.
  **PROSPECTIVELY_CONFIRMED is reachable from this run by design; DP-31 does not apply and no
  successor replication question is needed.**

### 5.1 Measured exposure — the rates this window is sized on

**R1 is delivered:** `research/reports/STEWARD_Q023_exposure.md` (2026-09-13, counts only, no outcome
of any kind), measured on `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`,
over pick nights **2026-06-09..2026-09-10 — the whole point-in-time-legal span of
`market_regime_daily`, N = 65 elapsed sessions** (wider than the drafted 2026-06-09..2026-08-12: the
arm label is a 16:05 ET property with no outcome attached, so the longer span costs nothing and makes
the gate decision far less fragile). **Every number below is measured, not planned; no borrowed rate
and no invented haircut constant survives in this file.** The denominator of every rate is **elapsed
sessions**, with exclusions *not* pre-removed (the Q019 / Q022 convention, so rates are comparable
across questions).

| quantity | measured (R1, 2026-06-09..2026-09-10, 65 elapsed sessions) | used to size |
|---|---|---|
| contributing nights per elapsed session | **0.9538** (62/65), re-derived under *this* §2.4 funnel, not borrowed from Q015's 0.92 | floors A and C |
| rarer-arm (NOTSTRONG) nights per elapsed session | **0.2000** (13/65) | floor B (via episodes) |
| rarer-arm (NOTSTRONG) **episodes** per elapsed session | **0.0615** (4/65) | floor B, floor D |
| STRONG episodes per elapsed session | **0.0769** (5/65) | floor D |
| rarer-arm contributing nights **per gate-counting episode** | **3.25** (13/4); episode lengths in sessions [3, 4, 2, 5] | floor B's episode conversion |
| six-level ladder eligibility, 80–90 published | 433 of 482 rows survive the full §2.4 funnel; **every one of the 62 non-excluded nights keeps ≥ 1 eligible pick through every step** | not binding |

**The drafted planning rates are gone, and one of them ran the wrong way.** The draft cut the
contributing-night rate from a borrowed 0.92 to 0.85 (conservative, and the measured rate turns out
to be higher still, 0.9538) — but it cut the *rarer-arm* rate from a borrowed 0.30 to 0.25, and the
tape actually delivered **0.2000**, below both. A haircut on a borrowed number is not a haircut. §5.2
replaces it with a conversion that uses only R1's measured counts: **the rarer arm is sized in whole
episodes**, because whole episodes are the only unit in which its nights arrive.

**The fact that drives that choice, stated plainly because it is the live risk in this question:** the
NOTSTRONG arm produced **no contributing night in the trailing 30 sessions** of the sealed panel
(2026-07-30..2026-09-10 is one uninterrupted `strongly_bullish` episode; August 21 STRONG / 0
NOTSTRONG, September-to-the-10th 7 / 0). The whole-period rate of 0.2000 clears the gate; the recent
trend, 0.00/session, does not. R1 can measure the *sealed* arm mix, never the *future* one. A tape
that stops producing one of the two labels for eight months is exactly what DP-13's single extension
and the DEFERRED fallback exist for (§5.2, §10 threat 14), and neither gate is reduced if it happens.

### 5.2 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13; no outcome is looked at)

**Window: pick nights 2026-09-14 .. 2027-02-25 inclusive = 114 elapsed sessions**, after exclusions.
**Decision date: Monday 2027-06-07.** Single DP-13 extension to **2027-04-09** (144 sessions), decided
**Monday 2027-07-19**, which is also the **hard stop**: still short there, Q023 goes to DEFERRED.

**How 114 sessions is reached — the rarer arm is sized in whole episodes.** Floor B (20 contributing
nights in the NOTSTRONG arm) is the binding floor, and its nights do not arrive one at a time. R1
measures 4 gate-counting NOTSTRONG episodes carrying 13 contributing nights, i.e. **3.25 nights per
episode**, so 20 nights cost 20 / 3.25 = 6.15 → **7 whole episodes**, and at the measured episode rate
7 / 0.0615 = 113.75 → **114 elapsed sessions**. This is the rate haircut, and it uses only R1's
measured numbers (13 nights, 4 episodes, 65 sessions); no haircut constant is invented. **The option
not taken: the flat 0.2000 night rate, 100 sessions, window end 2027-02-04, decision 2027-05-10** —
which projects floor B at exactly **20.0 of 20** on an arm whose last 30 sessions produced nothing,
i.e. a window whose floors are met *only if* the extension fires. DP-13 is the fallback for a measured
shortfall, never the plan (DP-43, DP-45), and the option four weeks sooner is never the one taken.

**Floor projections at 114 sessions — every floor is met inside the primary window, with margin:**

| floor | measured rate | sessions needed | date first met | projected at 114 sessions |
|---|---|---|---|---|
| **A:** ≥ 80 contributing nights, per primary endpoint (DP-21) | 0.9538/session | 84 | 2027-01-12 | **108.7 nights** |
| **B:** ≥ 20 contributing nights in the rarer arm (NOTSTRONG) | 7 whole episodes at 0.0615/session | **114 — binds** | **2027-02-25** | **22.8 nights** |
| **C:** ≥ 30 contributing nights dated after the lock commit (DP-24) | 0.9538/session | 32 | 2026-10-27 | **108.7** (every night is post-lock by construction, §6) |
| **D:** ≥ 5 episodes per arm (§8 clause 2) | NOTSTRONG 0.0615, STRONG 0.0769 | 82 | 2027-01-08 | **7.0 NOTSTRONG / 8.8 STRONG** |

Floor A clears at 114 sessions even on the draft's own 0.85 haircut (96.9 nights), so the haircut
question bites on **B alone** and is settled there. DP-24 is satisfied by construction and is not the
gate. STRONG is projected at **85.9** contributing nights, NOTSTRONG at **22.8**.

**Arithmetic, session by session** (holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18,
2027-02-15, 2027-03-26, 2027-05-31, 2027-06-18, 2027-07-05):

- **Window.** 2026-09-14 is session 1. Sep 13 + Oct 22 + Nov 20 + Dec 22 + Jan 19 = 96 at 2027-01-29;
  Feb 1–4 = 100 at 2027-02-04; Feb 5, 8–12, 16–19, 22–25 = **114 at 2027-02-25** (Thursday).
- **Decision date.** 2027-02-25 **+ 60 sessions** maturity (Feb 26; Mar 1–25 minus Good Friday
  2027-03-26; Mar 29–31; Apr; May 1–21) = **2027-05-21** (Friday); **+ one calendar week** freeze
  margin = 2027-05-28; first Monday on or after = 2027-05-31, **which is Memorial Day**, so the date
  moves **out** one week to **Monday 2027-06-07**. Moving out is always permitted; moving in never is.
  That is **8.8 months from the 2026-09-13 lock**, inside DP-43's 12-month ceiling (latest admissible
  Monday 2027-09-13). `eval.py` is written once (rule 9) and run **once**, then. **No interim looks.**
- **Extension (DP-13; DP-43's +30 sessions).** If any gate — 80 contributing nights per primary
  endpoint, 20 per arm, **5 episodes per arm**, 30 post-lock nights — is short at 2027-06-07 on
  `eval.py`'s **own measured counts** (never on a projection or a run-rate), the window extends
  **once**, automatically and with no new question, to pick nights **2026-09-14 .. 2027-04-09**
  (session 144), decision date **Monday 2027-07-19** (2027-04-09 + 60 sessions = 2027-07-07; + one
  week = 2027-07-14; first Monday on or after). The extended run uses the **byte-identical, unmodified
  `eval.py`** and the same gates. 10.2 months, still inside the ceiling.
- **DEFERRED fallback (the hard stop).** If a gate is still short after that single extension, Q023
  goes to `research/questions/DEFERRED.md` with the measured counts, rather than running
  under-powered. There is **no second extension, no reduced gate**, and **a gate shortfall is never an
  INCONCLUSIVE verdict** (§8). §10 threat 14 is live: eight months of one-sided tape is a real and
  correct route to DEFERRED.
- **Fixed at lock, not reopened at the decision pass:** the §4.3 **sub-cell suppression list**; the
  **60%** composition guard (§8 clause 8); the **≥ 5 episodes per arm** gate; both MPEs (§8); `m = 2`
  (§7). No arm is demoted or promoted after lock in either direction (DECISIONS item 9).
- **If a `regime_version`, hysteresis-constant or regime-threshold change ships mid-window**
  (§5.3 R2, §10 threat 11), the label is **two features** and the **episodes are re-cut**: the window
  is cut at the ship date, the **post-ship** segment becomes the question's window with this whole
  schedule recomputed from it — **out, never in**, subject to the same single extension and the same
  12-month ceiling measured from the original lock — the pre-ship segment becomes a labelled
  descriptive panel entering no verdict, and if neither segment reaches the gates inside the ceiling
  the question is **DEFERRED** (DECISIONS item 12; DP-06, DP-50(a)).

### 5.3 Routed requests

- **R1 → data-steward — DELIVERED 2026-09-13, `research/reports/STEWARD_Q023_exposure.md`** (counts
  only, no outcome of any kind; on `manifest_v001` + `manifest_prices_v001` against
  `exclusions_v003.json`, plus read-only `git log` / `git show` in the platform repo — never a live
  query, DP-50(c)). It was **blocking for lock**, because no desk report had ever counted a regime-arm
  split or an *episode* and the DEFERRED gate below turned on those numbers. Measured over pick nights
  **2026-06-09..2026-09-10 (65 elapsed sessions)** — the whole point-in-time-legal span of
  `market_regime_daily`, not the drafted 2026-06-09..2026-08-12. What it returned, and where it lands
  in this file:
  (a) the §2 funnel re-derived under *this* funnel rather than Q015's → §5.1 (0.9538 contributing
  nights per elapsed session; 433 of 482 rows survive; **0** nights lost at any step);
  (b) the arm split and the **episodes** → §2.5, §5.1, §5.2 (NOTSTRONG 13 nights in 4 episodes,
  3.25 nights/episode; STRONG 49 nights in 5; NOTSTRONG composition **100% `bullish`**);
  (c) the legality audit on both limbs of the timestamp test → §2.2 (**1 failure in 65**, 2026-07-06,
  already excluded; 0 `unknown` / `insufficient` / missing-v1.2 nights);
  (d) the two-label agreement rate → §4.3 (**89.06%**, all 7 disagreements on arm-transition
  boundaries);
  (e) the control-pool distribution and the CTRA truncated-history scan → §3 B2;
  (f) B3 feasibility → §3 B3 (**98.17%** coverage already);
  (g) the **DP-50(a)/(b) commit sweep since manifest SHA `fa70688`: NONE** — the only intervening
  commit, `2d5776c` (PI-001), touches an unrelated table's backfill clamp; no hysteresis constant,
  secular-risk threshold, `BAND_EXITS` / scale-out fraction, weight, timeframe multiplier,
  `publication_floor` or `bear_publish_threshold` changed, and **no `regime_version` beyond v1.2
  exists anywhere in the frozen history**. DECISIONS item 12's window-split trigger does not fire and
  no `DATA_NOTES.md` entry is owed.
  **The lock-or-DEFER gate R1 decided, on three limbs** (the inequality is DP-43's 12-month ceiling
  solved at the actual lock date and rounded **up**: 188 admissible elapsed sessions → 80/188 = 0.43,
  20/188 = 0.11, 5/188 = 0.027): contributing nights **≥ 0.43** per elapsed session, rarer-arm nights
  **≥ 0.11**, rarer-arm **episodes ≥ 0.027**. Measured: **0.9538 / 0.2000 / 0.0615** — all three clear
  (2.2× / 1.8× / 2.3×), so **Q023 locks rather than going to DEFERRED**. The branch taken is the
  middle one of the three registered at `decide`: the measured rarer-arm rate is *below* the drafted
  0.25 planning rate, so the window end, the decision date and the extension date all **move out** to
  §5.2's recomputed dates. The window end is the **latest of the four floor projections** (80
  contributing nights, 20 rarer-arm nights, 30 post-lock nights, 5 episodes per arm). A rate faster
  than plan would have changed nothing: no date is ever pulled in (DP-43, DP-45).
- **R2 → data-steward (due at the decision date; not a blocker for lock; DP-23).** Successor freezes
  `manifest_v00N` (selections: same SQL, same exclusion criteria, **plus `market_regime_daily` and
  `projection_pick_bullish_daily`**) and `manifest_prices_v00N` (same Alpaca queries), covering pick
  nights **2026-09-14..2027-02-25** with **60 forward sessions** beyond the last included pick night
  (daily bars through **2027-05-21**), delivered before **Monday 2027-06-07**; a second pair **only
  if** the DP-13 extension fires, covering **.. 2027-04-09** with forward bars through 2027-07-07,
  delivered before **Monday 2027-07-19**, built then and not before. Four scope requirements, none
  optional: **(i)** the daily symbol list covers **every candidate symbol on every in-window night,
  published and unpublished** (B2 needs their pick-night closes, 60 prior bars for beta60 / atr_pct /
  runup20, and their own forward bars) **and every `projection_pick_bullish_daily` symbol on those
  nights** (B3, DECISIONS item 5) — never assumed from v001's symbol list; **(ii)** hourly bars scoped
  to at least the published-pick symbols, for the descriptive entry audit only (no primary depends on
  an hourly bar; a narrower scope costs a secondary and must be stated); **(iii)** an **add-only
  successor exclusions file** issued with the selection freeze, applying the **identical three
  criteria** to the post-lock nights — it may add nights and may never remove one from a v003 list;
  **(iv)** rows whose bars are missing are **excluded and counted, never back-filled or imputed**.
  **DP-50(a) guard, load-bearing here and not a formality:** where a successor freeze overlaps an
  earlier one on `market_regime_daily`, the rows are compared and `eval.py` **fails loudly** on any
  disagreement in `market_regime`, `regime_version` or `data_quality` — the arm assignment is this
  question's conditioning variable *and* its inference unit, so a repair that rewrote it would
  silently re-run the experiment. R1(g)'s commit sweep is **repeated for the period between the
  freezes** — including the hysteresis constants `promote_n` / `enter_bearish` / `exit_bearish`
  (`scorer.py:60`, `:386-420`) and the secular-risk thresholds (`:36-39`, `:78-110`), which re-cut the
  episodes as well as the labels — with a dated `DATA_NOTES.md` entry for any repair that rewrites
  historical rows, and an explicit answer **even when it is "none"** on whether any `regime_version`,
  hysteresis-constant, `BAND_EXITS`, publication-predicate or weights change shipped **inside** the
  window (§5.2's split rule). Every §5 date is re-confirmed **session by session from the trading
  calendar** when the freeze is built, against the holiday list above; a correction may move a date
  **out, never in**. Two holidays are load-bearing: **2027-02-15** (Presidents' Day) sits inside the
  window and shifts the 114th session, and **2027-05-31** (Memorial Day) is why the decision date is
  2027-06-07 and not 2027-05-31.
  `eval.py` takes the window start and end, the manifest paths, the exclusions-file paths and the
  output directory as inputs — **no hard-coded dates, manifest names or paths** — so the
  byte-identical script serves both runs, and it records every sha256.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights 2026-09-14 .. 2027-02-25**, opening on the first
  session after the lock and closing at the §5.2 window end (114 elapsed sessions; .. 2027-04-09 if
  the single DP-13 extension fires).
  *Justification, and it is not optional here.* The sealed period **has already been read for this
  hypothesis**: the weekly snapshots of 2026-09-10 and 2026-09-12 printed the 80–90 band's T+20 return
  by point-in-time regime label on both entry bases, the night and pick counts per label, and the
  projection-bullish comparator on the same nights (BACKLOG H-013). Those nights are contaminated and
  are **not used for any verdict** — the Q018 precedent. They are printed once, as a **labelled
  post-hoc panel** (`manifest_v001` + `manifest_prices_v001`, pick nights 2026-06-09..2026-08-12,
  every §4 endpoint), which **enters no verdict, no CI comparison, no half, no stratum test, no q and
  no §9 rule**, and exists only so the prospective result can be read against what was claimed. The
  panel is largely **right-censored by its own freeze** and is reported as such: R1 §2 measures that
  only **5 nights (2026-06-09..2026-06-15, 27 eligible picks)** carry a full t+1..t+60 forward window
  inside `manifest_prices_v001` — of which **0.0% fail gradeability** — so every panel endpoint prints
  its matured-night count beside it and immature nights are **counted, never graded as non-touches**
  (§2.4).
  The window also sits entirely after the 2026-06-01 catalyst fix (DP-06), after the 2026-07-06
  `_enforce_ladder_monotonic` commit and after the 2026-07-07 `publication_floor = 80.0` change
  (DATA_NOTES), so none of the three splits DP-06 / DP-50(a) would force falls inside it.
  *Additional contamination check (registrar; no results directory was read).* **Q005** is the only
  question that has produced regime-stratified output in this family, and its own PREREG §2 states
  *"No outcome column is read. `outcome_*`, `sas_excursion.*`, `level_hit_*` and
  `uoa_symbol_daily.fwd_return_*` are not joined in this question at all"* — it is a score
  decomposition, so its regime strata cannot contaminate an outcome question. The standing finding
  "regime A/B found no bonus-day edge" (CLAUDE.md) is about `allow_bull_earnings_bonus` **days**, a
  different variable and a different contrast.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date (re-derived from the final window at the decision pass); Half B = after.
  Both primaries must carry the same sign in both halves (§8 clause 6), and the halves are a
  **stability clause, not a reported stratum**: each is projected at ≈ 11.4 rarer-arm nights, it is
  **not** on the §4.3 suppression list, and it **blocks at whatever count it has**. `in_sample_end =
  2026-05-29` marks only what is excluded.
- **Regime stratification (rule 7).** Regime **is the arm here**, so **rule 7 is satisfied by the arm
  itself** — the arm *is* the regime. Two further strata are computed, and both are constrained by
  the §4.3 suppression list fixed at lock:
  - **`tape_t`**, the SPY proxy, trailing and legal at 16:05 ET: sign of SPY's trailing 20-session
    return × tercile of SPY's trailing 20-session realized volatility, from `prices_daily_split` bars
    dated ≤ t, with **expanding-window** tercile cut points (for night t, from every session
    2026-03-02..t), so no later night's data sets an earlier night's stratum. **All six cells are
    SUPPRESSED at lock** (≈ 3.8 rarer-arm nights each; ≈ 18.1 even pooled across arms) — counts only.
    Suppressing them costs no rule-7 obligation, because the arm already carries it. The *matched*
    read on the same variable — the trailing-tape-matched sensitivity of §4.3 — is a recomputation
    rather than a stratum, is **not** suppressed, and stays mandatory.
  - **`regime_phase`** from the same legal row — the direct read on H-013's own "late-trend
    exhaustion" mechanism, which predicts the effect sits in `impulse_up`. The **`impulse_up` cell is
    reportable** (projected STRONG ≈ 72 / NOTSTRONG 22.8 contributing nights); **`pullback_in_bull` is
    SUPPRESSED at lock** — R1 §3 measures all 8 such nights as STRONG, so the phase contrast has an
    empty cell in one arm and the pooled cell is under 20 as well. **Consequence, binding on §9: the
    "late-trend exhaustion" phase read is not reportable, and no mechanism claim may rest on it.**
- **Knowledge time (rule 14) — every input declared. Q023 needs no rule-14 exception and requests
  none** (DP-05 untouched, DP-41 respected). The regime label is the only input that has ever had a
  knowledge-time problem on this desk, and the window is chosen so it does not: `market_regime_daily`
  carries **no point-in-time label before 2026-06-09** (FREEZE_v001 §7,
  `exclusions_v003.json.regime_label_point_in_time_from`), and this window starts 2026-09-14 — long
  past that boundary, so the backfill hazard cannot reach it. Only `regime_version = 'v1.2'` rows are
  read, and **legality is a timestamp test, not a date test** (DECISIONS item 1, §2.2): the row must
  be written on its own `trading_date` **and at or before that night's own `sas_runs.finished_at`**,
  so a same-day row posted *after* the run that published the picks is treated as missing and its
  night is excluded in whole and counted. The label the platform's **own consumer** uses to gate a
  pick scored on the close of t is the row with `trading_date = t` (volatilx
  `services/market_regime/consumer.py:52-60`, `services/market_regime/repository.py:102-103`,
  `:154-162`); `freeze_config.availability.market_regime` **declares** that row at 16:05 ET, lag 0,
  and FREEZE_v001 §7 **verified** the declaration for exactly these rows (v1.2, `trading_date ≥
  2026-06-09`, `created_at` same day ~20:05 UTC, ahead of the night's own run at ~21:0x–21:1x UTC),
  with one late-write exception that R1 §4 re-confirms as the only one in 65 sessions. The strictly-
  prior `effective_for_trading_date = t` row is computed as a **binding, unconditional** sensitivity
  (§4.3, §8 clause 7) — there is no disagreement-rate threshold below which it stops binding.

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction` | `sas_candidates` | pick night, 16:05 ET | population, band, direction |
  | six-level ladder `L1…L6`, lane `entry` / `stop` | `sas_candidates.public_payload_json.lane_plans` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | levels, plan, exclusions |
  | `market_regime`, `regime_phase`, `data_quality`, `regime_version`, `created_at` | `market_regime_daily`, v1.2, `trading_date = t` | declared 16:05 ET / lag 0 (`freeze_config.availability`), verified FREEZE_v001 §7 for nights ≥ 2026-06-09, and enforced per night by §2.2's timestamp test against that night's own `finished_at` | **arm**, strata, episodes |
  | `score_details_json`, `outcome_target_invalid` | `sas_candidates` | publication | band-integrity check; exclusion audit |
  | control-candidate pool (non-published rows for night t) | `sas_candidates` | pick night, 16:05 ET | B2 |
  | projection-bullish list for night t | `projection_pick_bullish_daily` | pick night, 16:05 ET (FREEZE_v001 §7) | B3 panel |
  | `C_t`, ATR14, beta60, runup20, SPY tape | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | distances, matching, stratum |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion |
  | session t+1 open `X`; daily bars t+1..t+60; hourly bars (published symbols) | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **entry and outcome measurement only** |

  **What `eval.py` must enforce:** the eligible-pick set, the arm label, the plan parameters
  (`L1…L6`, `ATR`, direction), the control sets and every stratum label are computed and written to a
  frozen per-pick and per-night table **before any post-pick-night bar other than the t+1 open is
  loaded**, and the t+1 open is used **only** as the entry price `X` — never to filter, classify,
  match or stratify. The run fails if any t+1-or-later field is referenced in eligibility, arm
  assignment, matching or stratification. `sas_selection_excursion` / `outcome_*` / `level_hit_*`
  columns are never inputs (calendar windows, close basis, recomputed weeks later, v1/v2 duplication —
  volatilx `services/sas_excursion.py:8-18`, `:336-354`; DATA_NOTES).
  `uoa_symbol_daily.fwd_return_*` is **banned** (FREEZE_v001 §5); no UOA table is used.

## 7. Multiple testing

- **Within the question: BH across m = 2** — E1 and E2 — at q ≤ 0.10; the verdict uses q. **`m = 2`
  is fixed at lock**: both endpoints carry a verdict in every branch, an endpoint short of floor still
  has its p computed, and no primary is dropped afterwards (dropping one would lower the bar for the
  survivor). Every secondary in §4.3 prints raw p only, marked *"descriptive, does not decide"*.
- **Across the family: F2 Calibration.** F2 holds **5 hypotheses** — H-010, H-011, H-012, **H-013**,
  H-014. The **F2 correction set is computed at the decision pass over the F2 questions locked by
  then**, and it **never shrinks below the 2 primaries registered at this lock** (E1, E2); today that
  is **Q023 alone**. **Q005 is excluded from the set** and the exclusion is stated rather than
  assumed: it is a diagnostic decomposition with no MPE, no directional primary and no outcome column
  read at all (its PREREG §2, §4), so it contributes no testable primary. If H-010, H-011, H-012 or
  H-014 lock before the decision date **2027-06-07** — a later date can only enlarge the set, never
  shrink it — their primaries join the set and the q's are recomputed on the larger m. H-013 is
  counted **once**, in F2 (DP-29).
- **No companion correction is required.** E2 is a *plan-result* endpoint but there is no plan
  contrast anywhere in Q023 — one plan, two night-types — so its subject is calibration, not exits,
  and DP-29's re-filing grounds (Q009, Q012) do not apply.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q006 (F1)** owns the picks-versus-matched-control comparison of the path after selection,
    against the same control construction. Q023's `E_t` **is** Q006's quantity computed per night; the
    only thing Q023 adds is the arm contrast. A non-zero E1 is **not** a second confirmation of a
    selection edge and may never be reported as one — and E1 can be large while Q006's excess is zero,
    or the reverse.
  - **Q022 (F4)** uses the identical two-stage shape (within-night control-adjusted rate, then a
    between-night arm contrast) on overlapping nights with a different night-level arm (sector
    concentration). If concentrated slates cluster in strongly-bullish tapes, the two questions are
    reading overlapping structure; the Reporter cross-references and neither confirms the other.
  - **Q015 (F7)** grades the 85–90 sub-band's L3-touch-then-give-back shape on the same level and the
    same 20-session clock with **no regime arm**; Q023's population contains Q015's. The L3 touch rate
    by band is a shared ingredient, not a shared test.
  - **Q012 and Q018 (F6)** both contrast *exit plans* on this band. Q023 runs one plan and contrasts
    night-types; a Q023 E2 result says nothing about which plan is better and may not be quoted as
    though it did.
  - **Q016 (F7)** and **Q021 (F3)** condition on volatility and pin risk, not on the tape label.
  - **H-010 and H-011 (F2, unregistered)** carry the adjacent suspicions that the band structure is a
    calendar artefact and that the confidence label is mis-ordered. A Q023 confirmation does **not**
    confirm either, and §9 binds what may be said.
- Threshold: **q ≤ 0.10**, alongside raw p (rule 8).

## 8. Decision rule (numeric, written before unsealing)

`E1` is in **percentage points of control-adjusted L3-touch rate within 20 sessions, STRONG minus
NOTSTRONG**. `E2` is in **ATR per published pick of the committed SELECT scale-out over its 60-session
budget, STRONG minus NOTSTRONG**. Both over the contributing nights of §2.5.

**MPE — E1 ±10.0 pp.** E1 is a **difference of differences** (a control-adjusted rate, arm minus
arm), and the desk doubles the MPE of its components for such an endpoint — DP-20's larger-MPE clause,
with the Q012 P2, Q018 P4 and Q022 E1 precedents; at ~80 nights a 5 pp bar on a difference of
differences would return INCONCLUSIVE by construction rather than by evidence.
**MPE — E2 ±0.25 ATR** (DP-10, DP-44 — the standing number for every per-trade ATR-denominated
endpoint; E2 is a single difference of per-trade means, not a difference of differences, so no uplift
applies), measured **per published pick, never rescaled to a per-toucher or per-filled-fraction
basis**.

**Neither MPE is lowered at the decision pass in any branch** — including a branch where the MPE turns
a CI-excludes-zero result into INCONCLUSIVE. That is what an MPE is for (rule 6).

Both two-sided. H-013 predicts `E1 < 0` and `E2 < 0`.

Per endpoint, **HISTORICALLY_CONFIRMED** requires **all** of:

1. **contributing nights ≥ 80**, **≥ 20 per arm**, **≥ 30 dated after the lock commit** (DP-21,
   DP-24), and ≥ 20 for any sub-cell that is *reported* — a sub-cell below 20 is **SUPPRESSED**
   (counts only) and does **not** by itself make the endpoint INCONCLUSIVE. The suppression list is
   **fixed at lock** in §4.3 and restricts affirmative reporting only: it never removes clause 6's or
   clause 7's opposite-sign blockers, nor clause 9's companion, whatever their cell counts;
2. **≥ 5 episodes per arm** (§2.5's label-series definition, DECISIONS item 4). Fewer means the
   contrast is a comparison of two calendar stretches wearing a regime label. **This is a gate, not a
   verdict:** an arm below 5 gate-counting episodes at the decision date fires the **single automatic
   DP-13 extension** (§5.2); still short after it, Q023 goes to **DEFERRED**. No second extension, no
   reduced gate, and **never an INCONCLUSIVE verdict on this ground**;
3. `|E| > MPE` (10.0 pp for E1; 0.25 ATR for E2);
4. the **episode-block bootstrap** 95% CI excludes 0 (the night-level and stationary-block CIs are
   printed but do not decide), and the **episode-label permutation** p supports it;
5. BH `q ≤ 0.10` within the question (m = 2) **and** within F2 (§7);
6. the point estimate has the **same sign in both halves** (§6), and neither half is beyond MPE in the
   opposite sign; and the **bull-only** version (§4.3) is not beyond MPE in the opposite sign;
7. the **`effective_for_trading_date = t` label** version (§4.3, DECISIONS item 1) is not beyond MPE
   in the opposite sign. **This clause binds unconditionally** — there is no disagreement-rate
   threshold below which it stops binding; the night-level agreement rate is printed beside it;
8. **the NOTSTRONG arm is not a different question from the one registered:** if fewer than **60%** of
   NOTSTRONG contributing nights carry the `bullish` label, the pooled contrast is still reported but
   the verdict is taken on the **STRONG vs `bullish`-only** contrast, and if that cell is below 20
   contributing nights the endpoint is **INCONCLUSIVE**. (This is a composition guard, not a floor
   reduction: no floor moves in either direction. **The 60% is fixed at lock and may not be moved in
   either direction at the decision pass**; on the sealed panel it is met trivially at 100%, R1 §3.)
9. **for E2 only, because E2 has no control inside it:** the **control-adjusted E2 companion** (§4.3 —
   the same committed plan run on each pick's matched controls at identical ATR distances, subtracted
   per pick before the night mean) is **not beyond 0.25 ATR in the opposite sign**. E2 is the total
   effect in DP-12's sense; this is the clause-6 / clause-7 idiom applied to the one endpoint whose
   arm *is* the tape (DECISIONS item 7).

- **NULL:** floors and clauses 1–2 met, **and** the episode-bootstrap 95% CI includes 0, **and**
  `|E| < MPE`. *"The 80–90 band does no worse on strongly-bullish nights than on other nights"* is a
  real finding, it retires a standing suspicion, and it is ledgered with the same care as a positive.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, the bull-only or the alternative-label
  version beyond MPE in the opposite sign, a NOTSTRONG arm that fails clause 8, an E2 whose
  control-adjusted companion is beyond 0.25 ATR in the opposite sign (clause 9), `0 < |E| ≤ MPE` with
  the CI excluding 0 ("real but below MPE", rule 6), or a CI including 0 with `|E| ≥ MPE`.
  **A gate shortfall is never INCONCLUSIVE** — not the 80-night floor, not the 20-per-arm floor, not
  the 30-post-lock-night floor, and **not the 5-episodes-per-arm gate**: each fires the single DP-13
  extension, then DEFERRED (§5.2).
- **What licenses what** (§9 depends on this and on nothing else):
  - **E1 and E2 both CONFIRMED negative** → the full finding: the band is worse calibrated *and* pays
    less on those nights. Both a guide line and a flag-off engine change are licensed.
  - **E1 CONFIRMED negative, E2 NULL** → a calibration note only. The edge over look-alikes shrinks,
    but the band still pays what it pays; **no publication or sizing change ships**.
  - **E2 CONFIRMED negative, E1 NULL** → the tape, not the score. A descriptive expectation line is
    licensed; **no SAS config change, no publication change, no sizing change, and the sentence may
    not be written as a calibration claim** — **because DP-12 says a total effect is descriptive and
    licenses no rule**, not as a matter of house style. Clause 9's companion must also have held.
  - **Either CONFIRMED positive** → the finding is published with the opposite sign and the standing
    suspicion is retired explicitly.
- **What a confirmed E1 does and does not mean (binding on the report).** A CONFIRMED-negative E1
  means *"on nights labelled `strongly_bullish`, 80–90 picks beat their same-night distance-matched
  look-alikes to the printed swing target by N pp less than on other nights"*. It does **not** mean
  the picks fell, and it does **not** mean the band lost money — the raw arm contrast and E2 are the
  numbers that speak to that, and both must be quoted beside it.
- **SAS-specific language requires B3.** No sentence of the form "this is a SAS problem, not a market
  problem" may be written unless **B3 is computed** (§3) and its arm contrast is inside MPE while the
  SAS endpoint is beyond it. If B3 is `NOT COMPUTABLE`, the finding is reported as a property of
  *model-selected momentum names on those nights*, which is the weaker and honest reading.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — it requires ≥ 30 contributing
  nights dated after this file's lock commit (DP-24, DP-21), which every contributing night here is,
  frozen in the successor manifests and never inspected earlier, reproducing the sign of the
  confirming endpoint under the unmodified `eval.py`. The clause does not weaken. No subscriber-facing
  statement before that (rule 10); even then the basis is `NON_QUOTABLE` until restated on W60
  (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the regime label is already a **live input to scoring**: `allow_bull_earnings_bonus` fires only
when `market_regime ∈ {bullish, strongly_bullish}`, `regime_phase == 'impulse_up'` and confidence
≥ 0.70 (volatilx `services/market_regime/scorer.py:427-442`), and the earnings catalyst layer reads it
(`services/catalyst_scoring.py`). The engine therefore treats `strongly_bullish` as a reason to score
*higher*. Nothing on the platform tests whether that is the right sign, and no surface varies the
80–90 band's treatment by regime label.

Rules below fire **only** where §8 licenses them, and nothing subscriber-facing ships before
PROSPECTIVELY_CONFIRMED (rule 10):

- **E1 and E2 both CONFIRMED negative:** (a) a Manual Trading Guide line stating the measured
  difference, with the raw arm contrast, the control-adjusted contrast and the committed-plan ATR
  printed together and the episode counts shown; (b) an `INTERNAL_TOOL`, flag-off card field showing
  the night's regime label and the band's measured regime-conditional expectation; (c) a brief to
  **re-examine the sign of the bull bonus on `strongly_bullish` + `impulse_up` nights**
  (`services/market_regime/scorer.py:427-442`) — shipped flag-off with a byte-identical checksum on
  the old path and shadowed ≥ 20 trading days before any flip (rule 11). A publication *gate* on those
  nights is **not** licensed by this question; suppressing picks changes the product's shape and needs
  its own registered question.
  **DP-49 binds that brief when it is written:** every check it hands the **coding agent** must be
  satisfiable from the platform repo alone — the test suite, a pure-function import, `git show
  --stat`, a file diff. Anything that reads or writes a table belongs in the brief's verification
  section, addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where a write is required;
  a "prove you did not change file X" check is written as the diff that proves it, never as "run X
  twice and compare". Where a frozen manifest covers the affected table, the brief names that parquet
  as the before-snapshot rather than asking anyone to capture one (DP-50(c)).
- **E1 CONFIRMED negative, E2 NULL:** the guide line only, worded as calibration ("the score's edge
  over look-alikes is smaller on these nights"), no engine change, no sizing change.
- **E2 CONFIRMED negative, E1 NULL:** a descriptive expectation line on the performance surface, worded
  as a tape effect, with an explicit sentence that the selection edge is unchanged. **DP-12 is the
  reason no engine, publication or sizing change follows** — E2 is the total effect (§4.2) — and
  clause 9's control-adjusted companion must have held.
- **Either CONFIRMED positive:** the guide line runs the other way, and the weekly's regime × band
  panel is corrected in the ledger.
- **Both NULL:** the standing suspicion from the 2026-09-10 / 09-12 weeklies is **retired**, the
  weekly stops printing regime × band return cells as a signal, and F2 effort moves to H-010 and
  H-011. This is a result, not a non-result.
- **The suppressed cells license nothing.** No guide line, brief, flag or quoted number may cite the
  90+ sub-cell or any cell on §4.3's lock-time suppression list, whatever it shows. **In particular,
  `regime_phase = pullback_in_bull` is suppressed (§6), so H-013's own "late-trend exhaustion" phase
  read is not reportable and no mechanism sentence may rest on it.**
- **Q023 is in flight from this lock until its decision date, and DP-50(b) applies to the platform in
  the meantime.** There is one database, and a repair or a config change rewrites what this question
  reads. So any platform change to `services/market_regime/scorer.py` (the labels, the hysteresis
  constants, the secular-risk thresholds, the bull bonus), to `BAND_EXITS` / the SELECT scale-out
  fractions, or to the publication predicate is **flag-off until Q023's decision date, 2027-06-07**
  (2027-07-19 if the single DP-13 extension fires) — the PI-011 / Q010 pattern, checked before any fix
  brief is written. If such a change ships inside the window anyway, it takes a dated
  `DATA_NOTES.md` entry naming the column, the date range and the ship SHA, and §5.2's window split
  applies (DP-06, DP-50(a)).
- Owner: implementer. Shadow period before any flip: ≥ 20 trading days.

## 10. Known threats to validity (registrar's own list)

1. **The arm is calendar, and the label is built to make it so.** The regime label is smoothed by
   hysteresis (promote 3-of-5, enter-bearish 2, exit-bearish 3 — `scorer.py:60`, `:386-420`), so
   contributing nights arrive in long same-arm runs and the two arms are two sets of calendar
   stretches. R1 §3 measures exactly this on the sealed panel: one **30-session** STRONG episode
   covers the whole second half of it. This is the single largest threat and it is answered four ways,
   all pre-specified: the **episode-block bootstrap** and **episode-label permutation** (§4.4); the
   **≥ 5 gate-counting episodes per arm** gate, which is a gate and not a verdict (§8 clause 2); the
   **both-halves** clause (§8 clause 6); and the **episode definition on the label series** (§2.5), so
   an excluded night inside a stretch cannot manufacture an extra independent draw. None makes the
   threat vanish; together they stop a two-stretch contrast being read as 80 independent nights.
2. **The label may be nothing but the run that already happened.** `strongly_bullish` requires a low
   secular risk score, which is dominated by the weekly trend gap and the 200DMA distance
   (`scorer.py:36-39`, `:78-110`) — i.e. by trailing price. If the effect is entirely explained by
   SPY's trailing 20-session return, the finding is "after a big run this band does worse", not "the
   regime label marks it". The **trailing-tape-matched sensitivity** (§4.3) reads this directly and is
   mandatory in the report. It is deliberately **not** a gate: the label is the platform's own
   point-in-time variable and is what any rule would key on, so gating on it would be circular.
3. **The band changes composition with the arm.** On a strongly-bullish tape more names score 80–90
   because trend and flow agree, so the arm partly changes *which* stocks are in the band —
   H-013's own proposed mechanism. The within-night control is matched on `runup20`, `atr_pct` and
   `beta60`, which handles part of it; the per-arm distributions of those three and the post-match
   standardized mean differences are printed, and §8 clause 6's bull-only version is one read on it.
   The primary keeps the raw band, because matching away the features that produce the score would
   test something else.
4. **The 80–90 band is very nearly the whole traded book.** `publication_floor = 80.0` since
   2026-07-07 (`services/super_agent_select_models.py:86-91`) and 90+ is thin and shrinking, so this
   question is closer to "does the product do worse on these nights" than to "does this *band* do
   worse". The 90+ contrast that would separate them is SUPPRESSED at lock (§2.1, §4.3) and needs its
   own question when elite exposure recovers. Every §9 sentence must say *"the 80–90 band"*, never
   *"lower-scored picks"*.
5. **Direction mix.** Bearish publications are gated separately (`bear_publish_threshold`) and are
   plausibly rarer on strongly-bullish nights, so the arm partly contrasts a bull-only book against a
   mixed one. Because the in-sample read on bearish picks is *negative* (H-062), this confound pushes
   **against** H-013's predicted sign — the conservative direction — but it is still a confound: the
   direction mix is printed per arm and §8 clause 6 makes the bull-only version binding.
6. **E2 is a raw arm contrast on a night-type defined by the tape.** On a strong tape everything
   realizes more ATR, so E2's null is not zero in any deep sense — it is "whatever the tape gives".
   That is exactly why a *negative* E2 on the strongest-labelled nights would be the striking half of
   the finding, and why E2 alone licenses no calibration claim — **DP-12: the total effect is
   descriptive and licenses no rule** (§4.2, §8 clause 9, §9). The control-adjusted E2 companion is
   printed beside it and **blocks** a CONFIRMED E2 that runs the other way.
7. **The committed plan is truncated.** The trailing rules ("tighten trail after L4", "small L6 tail
   only") are not simulable, so Plan S is the scale-out without its trail, and unfillable fractions
   ride to the t+60 close rather than being reallocated. Both conventions are applied identically in
   both arms and cannot create the contrast; both are stated wherever E2 is reported.
8. **Band membership depends on a stored score that has been rewritten before.** The in-sample
   catalyst rescore and the E9a correction batch show `sas_candidates` rows are not immutable.
   `eval.py` re-derives each pick's band from `score_details_json` where the layer subscores are
   present and **fails loudly** on a disagreement with `overall_score` beyond 0.05.
9. **One database (DP-50).** A platform repair between successor freezes can rewrite the regime rows
   that assign the arms. The §5.3 R2 cross-freeze comparison fails loudly on any such disagreement,
   and a `regime_version` beyond v1.2 shipping mid-window makes the label two features (DP-06,
   DP-50(a)) and **re-cuts the episodes**, which are the inference unit — §5.2's split rule then moves
   the window **out, never in**. R1(g) swept the history to the lock and found **none**: no commit
   since manifest SHA `fa70688` touches the regime scorer, the conviction card, the guide generator or
   the SAS models, and no `regime_version` beyond v1.2 exists in the frozen history.
10. **Ladder and payload defects.** Null-ladder, non-monotone and split-scale payloads (DATA_NOTES)
    are excluded and counted; the question speaks only for published 80–90 picks carrying a complete,
    monotone, correctly-scaled six-level ladder.
11. **Config drift inside the window — and the surveillance list is wider than "the weights".** A
    change to the weights, the timeframe multipliers, the publication floor, `bear_publish_threshold`,
    `BAND_EXITS` / the SELECT scale-out fractions or the lane-plan writer changes what "an 80–90 pick"
    or "the committed plan" means. **A change to the hysteresis constants `promote_n` /
    `enter_bearish` / `exit_bearish` (`scorer.py:60`, `:386-420`) or to the secular-risk thresholds
    (`:36-39`, `:78-110`) is worse than that: it changes both the arm label and the episode structure
    — the conditioning variable and the inference unit at once — and is a DP-06 split exactly as a
    `regime_version` bump would be.** Every item on that list is named in R1(g) (swept to the lock:
    **none**) and repeated in R2 between freezes. `eval.py` additionally pins `regime_version =
    'v1.2'`, prints the per-night `regime_version` and `config_json` composition, and **fails
    loudly — it does not silently exclude** — if any in-window night's newest row carries a version
    beyond v1.2, or if the hysteresis constants or regime thresholds it records for the night differ
    from those in force at lock. A silent exclusion would let the arm die quietly; a loud failure
    cannot (DP-45).
12. **Overlapping 60-session windows** inflate precision badly at this horizon; the episode bootstrap
    is the mitigation and the block length is fixed at lock, not chosen after seeing results.
13. **B3 may be non-computable**, in which case the SAS-versus-tape separation rests on the within-night
    control alone and §8's language clause binds the report. R1 §7 projects it computable at 98.17%
    coverage, but the gate is evaluated on the successor freeze's own coverage, not on that figure.
14. **The prospective window may simply not contain the contrast — and this is the live risk, not a
    formality.** The NOTSTRONG arm has produced **no contributing night since 2026-07-29** (R1 §1, §3):
    the sealed panel ends in one uninterrupted 30-session `strongly_bullish` stretch. If the tape
    produces almost no `bullish`/other nights — or almost no `strongly_bullish` ones — for eight
    months, the 20-per-arm floor or the 5-episode gate fails, the DP-13 extension fires **once**, and
    then the question is **DEFERRED** rather than run under-powered (§5.2). §5.2's episode-sized window
    is the desk's answer to it — 114 sessions rather than 100, so the floors are projected met inside
    the primary window rather than via the extension — but no window length can manufacture a
    one-sided tape's missing arm. DEFERRED is a real and not-unlikely outcome here, and it is the
    correct one.

---

## Decisions before lock

Recorded in DECISIONS.md (2026-09-13), decide + record passes: **14 items — 10 DECIDED on standing
entries and locked precedent, 3 DEFAULTED under DP-43 / DP-45 (the prospective-only window start,
E2's 60-session clock, and the window end with its decision date — all three are where this question
spends waiting), and 1 ROUTED.** Eleven corrections to silent choices are applied above. No item is
pending and nothing blocks the lock.

**Routed item still open: R2 — the successor freezes** (`manifest_v00N` / `manifest_prices_v00N` with
`market_regime_daily`, `projection_pick_bullish_daily`, the full candidate symbol list, hourly bars
for published symbols, and the add-only successor exclusions file), **due before the decision pass on
Monday 2027-06-07 and not a blocker for lock** (DP-23, §5.3). A second pair is built only if the
single DP-13 extension fires, due before Monday 2027-07-19. R2's session-by-session calendar
re-confirmation may move any §5 date **out, never in**.

**R1 (counts only) is ANSWERED** — `research/reports/STEWARD_Q023_exposure.md`, 2026-09-13 — and it
was blocking: it decided that Q023 **locks rather than going to DEFERRED** (all three gate limbs clear
at 0.9538 / 0.2000 / 0.0615 against 0.43 / 0.11 / 0.027), and it fixed the schedule, the suppression
list, the composition guard's sealed-panel value and the DP-50(a) sweep. Every figure it returned is
folded into §§2–6 and §10 above.
