# Q025 — exposure attribution: is the SAS path edge a residual, or is it inherited market / sector / size / momentum / volatility exposure?

**Status:** PREREG_DRAFT (lock by committing this file; DP-46)
**Family:** **F1 Selection edge** (hypothesis **H-068**, filed in F1 in `research/BACKLOG.md`). DP-29 places it there: the primary endpoint's subject is whether *selection* carries information against a control cohort from the same night — Q006's subject, with a wider control. It is not "the path conditioned on a property known at 16:05" (F4), and it grades no exit plan (F6) and no score-to-outcome calibration (F2).
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10) — **plus** the successor freezes named in §5 (DP-23): `manifest_v002` / `manifest_prices_v002` covering pick nights **2026-07-08..2027-01-13** (a second pair **only if** the DP-13 extension fires, to 2027-02-26). Most of this question's population enters through those successors; only pick nights ≤ 2026-09-10 are covered by v001. The window and the forward-bar requirement are **identical to Q022's** request, so one freeze pair serves both questions.
**Manifest (static artifact):** `volatilx:data/sp500_sectors.json`, **sha256 `c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201`** — the content of platform commit **`4171b1a` (2026-05-17)**, that file's only commit ever, byte-identical at manifest SHA `fa70688…`. Pinned by sha256, recorded as a static artifact in `manifest_v002`, **never re-synced for the life of this question**; `eval.py` fails loudly on a mismatch. The pin, its provenance and its measured coverage of the candidate universe (99.5% of distinct symbols; the only two unmapped symbols in the entire frozen history are BRK.B and BF.B) are Q022 §2.1 and `research/reports/STEWARD_Q022_exposure.md`, reused here verbatim and unchanged.
**Exclusions:** research/data/exclusions_v003.json (DP-22) **unioned with the add-only successor exclusions file issued with `manifest_v002`** (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs`, identical three lists built by identical criteria for nights after 2026-09-10; the successor file may only **add** nights). Both paths are `eval.py` inputs; no file name and no date is hard-coded.
**Registered by:** registrar (autonomous run, DP-40..48) · **Date:** 2026-09-13

---

## 1. Hypothesis (plain English, one sentence)

**When SAS publishes a pick, does the stock reach the pick's own target more often than same-night stocks the engine looked at and did not publish that are its twins on everything we already know about them — same sector, similar market sensitivity, similar size, similar recent momentum, similar volatility — or does the apparent edge disappear once those twins are chosen properly?**

Why it matters, plainly: if the edge survives the full twin match, the ranking is adding information and the platform can say so. If it disappears — if the picks only did well because they were high-momentum semis in a month when high-momentum semis did well — then SAS is a very good *exposure* screen and a poor *ranking* engine, and the honest product claim is a different one. The desk does not know which is true, and Q006's control matches on three features only (beta60 / ATR% / 20-session run-up), leaving sector, size and longer-horizon momentum unmatched by construction (Q006 §10 threat 1 names this gap and does not test it).

**Registered two-sided.** H-068 predicts collapse toward zero; a residual materially *above* zero and a residual materially *below* zero (picks doing worse than their exposure twins) are both real findings and both are reportable with their sign.

## 2. Population

### 2.1 Sources

- **`manifest_v001` and its successors — `sas_candidates`:** `trading_date`, `symbol`, `qualified`, `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe`, `outcome_target_invalid`, `public_payload_json.lane_plans`. `sas_runs`: `finished_at` (DP-04). `market_regime_daily`: stratum only.
- **`manifest_prices_v001` and its successors — `prices_daily_split`** (`o/h/l/c/v` — the pick-night close `C_t`, ATR14, `beta60`, `mom20`, `mom60`, `adv20`, the SPY tape, the session t+1 open and all forward bars), **`prices_daily_raw`** (split-basis assertions only), **`prices_hourly_raw`** (descriptive ordering, published symbols only).
- **Static sector artifact:** the pinned `sp500_sectors.json` blob named in the header — `mapping` block only, upper-cased symbol → one of the eleven SPDR sector ETFs (volatilx `services/sector_breadth.py:38-50`), 2,405 entries. **The platform's `industry` column is never used, anywhere** (12% populated, PI-007; descriptive, feeds no scoring). The desk never hand-maps, supplements or overrides the pinned mapping.
- **Not used:** `sector_breadth_daily` (forward-only, never frozen, availability never declared). `uoa_symbol_daily.*` including `dollar_volume_20d` is **banned** — the table is degraded (FREEZE_v001 §5: coverage ~5% of baseline, `fwd_return_30d_pct` at 0% for trading_date ≥ 2026-07-27, i.e. across almost this whole window). Dollar volume is computed from bars instead (§2.3).

### 2.2 Treatment rows (the picks that are graded)

- `qualified IS TRUE AND selected_rank IS NOT NULL` (**DP-28**). Dark-lane rows (qualified, unranked) are never graded, are counted in the funnel, and stay available to the control pools.
- `dominant_direction ∈ {bullish, bearish}`. Direction does not define an arm; it selects the side of the target and is a reported sub-cell.
- **Pick nights 2026-07-08 through 2027-01-13 inclusive** (§5 window; §6 for the start rule), extended once to 2027-02-26 only if the DP-13 gate fires. No restriction on slate size `k_t`: every published pick on an eligible night is a candidate treatment row.

### 2.3 Exposure vector — computed at 16:05 ET, before any forward bar is read

For every candidate row (published and unpublished) on night `t`, from `prices_daily_split` bars dated **≤ t** only:

| feature | definition |
|---|---|
| `beta60` | OLS slope of daily returns on SPY daily returns, trailing 60 sessions |
| `atr_pct` | ATR14 / `C_t`, ATR14 computed by the desk from bars (the platform's `atr_pct` is corrupted around splits — DATA_NOTES) |
| `mom20` | 20-session total return (the Q006 `runup20`, identical definition) |
| `mom60` | 60-session total return |
| `size` | `log10` of the **median** daily dollar volume `c × v` over the trailing 20 sessions (`adv20`) |
| `sector` | the pinned `sp500_sectors.json` SPDR ETF for the symbol |

**On `size`.** No frozen table carries market capitalisation, shares outstanding or float — there is no such column anywhere in `manifest_v001`, and the FMP-sourced fundamentals that would carry one are the 12%-populated block (PI-007). `adv20` is the size/liquidity proxy the freeze can support, it is computed for every symbol with 20 prior bars (no coverage gap), and it is split-invariant because `c × v` is. It is a **proxy and is named as one** in §10; the claim this question can make is "residual after *these* exposures", never "residual after size".

**On `mom60`.** Plain 60-session total return. The 12-2-style skip variant (`t-60..t-20`) is computed and printed as a registered descriptive robustness; it never decides and cannot be promoted at the decision pass.

Continuous features are standardised **within the night** by the night's cross-sectional median and MAD across the full candidate universe of that night (the Q006 §3 convention), so no later night sets an earlier night's scale.

### 2.4 Night eligibility and pick-level exclusions (measurement failures only; each counted)

Night `t` is dropped entirely if it appears in the exclusions union named in the header or if `finished_at` is later than the next session's open (**DP-04**).

A published pick is dropped from the primary, and counted by reason, when:

- no swing-lane target in `public_payload_json.lane_plans` (the null-ladder denominator, PI-006);
- `outcome_target_invalid` non-null, or the swing t1 on the wrong side of `C_t` for the pick's direction;
- **price-scale screen** (DATA_NOTES 2026-09-13): `target / C_t` outside `[0.5, 2.0]`, or an implied ATR distance above 12 ATR. The screen is symbol-agnostic — it is a rule, not the APH / CRWD / KLAC / MNST list that produced it (measured 19 of 542 sealed-period picks, R1(g) of `STEWARD_Q022_exposure.md`);
- fewer than **60** daily bars dated ≤ t (`beta60`, `mom60` undefined), or no `C_t`, or no session t+1 open;
- **no sector mapping** for the symbol (measured: BRK.B and BF.B, the two dual-class tickers in the entire frozen history) — dropped, counted, listed by name, **never hand-mapped**: a desk-side supplement breaks the sha256 pin, and inventing a rule after seeing which symbols failed is judgment in the inner loop (rule 9);
- fewer than **3** valid controls in the full-exposure set B1 (§3) — dropped, counted, and the loss reported by sector, because it is the known cost of the sector block (§10.2);
- **ungradeable**: a pick is gradeable if every session t+1..t+20 has a daily bar, or the touch is already determined by the bars that exist. Halt, delisting or acquisition mid-window with no touch → dropped, counted;
- **immature**: session t+20 after the last trading date of the pinned price freeze → **excluded and counted, never graded as a non-touch**. Maturity comes from the trading calendar, not from whether a bar happens to exist.

**Contributing night (the floor unit, DP-21):** an eligible, matured night carrying **≥ 3 gradeable picks with a valid B1 control set**. Three, not five: the sector block drops picks in thin sectors, so a higher pick floor would silently select nights whose slates sat in XLK and bias the night set by sector composition. E1 restricted to nights with ≥ 5 such picks is printed as a named sensitivity. A night that survives to here and yields fewer than 3 is a **non-contributing night, not an exclusion** — printed in the funnel, never added to an exclusions file.

## 3. Baselines — what this must beat

H-068 names three baselines. All three are here; two of them are inside the primary endpoints and the third is descriptive.

- **B1 — the full-exposure distance-matched control (primary; H-068 baseline (a)).** For pick `p` on night `t`: the pool is the same-night `sas_candidates` rows that are **not** published (the complement of DP-28's predicate, dark-lane rows included) with ≥ 60 prior bars, a sector mapping and forward bars covering the window. Restrict the pool to the **same sector ETF** as `p` (hard block), then keep only rows within a **caliper of 1.5 standardised units on every one of `beta60`, `atr_pct`, `mom20`, `mom60`, `size`**, then take the **10 nearest** by Euclidean distance in that 5-dimensional standardised space, **minimum 3** or the pick is dropped (§2.4). Matching is with replacement across picks within a night; ties by symbol ascending (deterministic). Each control carries a **synthetic target at the identical ATR distance and the same direction**: `d_p = dir_p × (L3_p − C_{t,p}) / ATR_p`, applied to the control's own close and its own ATR14, graded on the control's own session t+1 open over the same 20 sessions, under exactly the pick's rules. **Controls never add to inferential n** (rule 6). The caliper and the 1.5 / 10 / 3 constants are registrar-chosen conventions fixed here (DP-26); none was derived from a sealed outcome.
- **B2 — within-exposure-block permutation of the published label (H-068 baseline (b)); this is the null distribution that decides E1's p-value.** Each pick and its B1 control set form a **block** — same night, same sector, same exposure profile inside the caliper, and exactly one member published. Under the null "the ranking carries no information once exposure is fixed", which member of the block was published is exchangeable. `eval.py` re-draws the published member uniformly within every block, jointly, recomputes the whole night-level statistic, and repeats **10,000 times, seed 20260913**. This is literally "exposure held fixed, ranking destroyed", and it is a stricter null than a night-level sign flip because it never lets the tape do the work. The night-level sign-flip permutation p is printed alongside; **the block-permutation p decides.**
- **B3 — sector-and-beta-matched random draws (H-068 baseline (c); descriptive).** For each pick, 10 draws taken **at random** (not nearest-neighbour) from the same-night unpublished pool restricted to the same sector ETF and the same `beta60` tercile of that night, 1,000 resamples, same synthetic-target rule. B3 says how much of B1's work is done by nearest-neighbour matching rather than by coarse sector-and-beta conditioning. Descriptive; never decides.
- **B4 — the partial (Q006) match, inside E2.** The Q006 §3 construction **verbatim**: 10 nearest same-night unpublished candidates on `beta60` / `atr_pct` / `runup20` standardised by the night's median and MAD, Euclidean, with replacement, ties by symbol ascending, **no sector block, no caliper, no size, no `mom60`**. It exists here only to be differenced against B1 (§4, E2), and it is computed on Q024's own window and Q024's own `eval.py` — **no Q006 result is read, now or at the pass** (rule 3).
- **B5 — unadjusted rates (descriptive).** Pooled published touch rate and pooled control touch rates, so the size of every adjustment is visible and a ~60% touch rate never reads as a finding on its own.

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Entry basis: the official 09:30 ET open of session t+1** (DP-03(b), DP-42), for published picks and for every control, one basis on both sides. The pick-night close basis (DP-11's construction) is computed and printed as a named sensitivity and decides nothing.

**Primary level: L3** — `public_payload_json.lane_plans.swing_trading.targets[0]`, the first swing target, direction-aware (DP-42: the hypothesis names the whole ladder, so the swing-lane default applies). **Primary clock: first touch within sessions t+1..t+20 from the entry** (DP-09); the platform's own 40-session swing window (`services/sas_conviction_card.py:194`) is printed alongside, descriptively, wherever it has matured.

**Touch rules, applied by `eval.py` with no judgment:**
1. `HIT_p = 1` iff some session `s ∈ [t+1, t+20]` has `high_s ≥ L3_p` (bullish) or `low_s ≤ L3_p` (bearish).
2. **A target already at or through the session t+1 open is not a hit** (DP-03, DP-26): graded `HIT = 0`, flagged `passed_at_entry`, and the primaries recomputed with those picks removed from both sides as a named sensitivity. The identical rule applies to every control's synthetic target.
3. A gap through the level during t+1..t+20 is a touch.
4. No stop is assumed anywhere and no touch is an exit (rule 5, DP-02). Adverse excursion and counter-direction touches are reported, never used as exits.

**Per-pick excesses and the night unit (rule 6):**

- `e_p^full = HIT_p − mean(HIT over p's B1 control set)`, in percentage points.
- `e_p^part = HIT_p − mean(HIT over p's B4 control set)`, in percentage points.
- `E_t^full = mean_p e_p^full` over the night's gradeable picks — **one number per night, the unit of inference**.
- `A_t = mean_p (e_p^part − e_p^full)` over the picks that carry **both** control sets — the same picks on both sides, so composition cannot leak into the difference.

**Primary endpoints (two, pre-specified, BH-corrected within this question):**

> **E1 — the residual.** `E1 = mean over contributing nights of E_t^full`, in percentage points of L3-touch rate. Two-sided. This is the number H-068 predicts collapses toward zero.

> **E2 — the attribution gap.** `E2 = mean over contributing nights of A_t`, in percentage points. Two-sided. `E2 > 0` means the crude three-feature twins understate what an exposure twin would have done, i.e. **part of the apparent edge is inherited exposure**; `E2 ≈ 0` means the extra exposure dimensions change nothing and a three-feature control was adequate.

**A property of E2 worth stating, because it is what makes it clean.** `e_p^part − e_p^full = mean(HIT over B1) − mean(HIT over B4)`: the pick's own outcome cancels. E2 is a statement about the two control constructions on the pick's own target distance and direction, and it cannot be moved by how the picks happened to do. The picks still define the population, the target and the side.

**Registered secondaries — printed always, deciding never:**

- **Feature-by-feature attribution:** E1 recomputed under five intermediate matches (sector block alone; + `size`; + `mom60`; the full vector without the sector block; the full vector without `size`). Read as a decomposition of E2; the whole ladder is descriptive and no rung may be promoted at the pass.
- **B3 (random sector-and-beta draws)** and **B5 (unadjusted rates)**, with control-set sizes and pool sizes throughout.
- **Rank information, exposure-adjusted:** `e_p^full` by `selected_rank` (top half vs bottom half of the night's slate, and the per-night Spearman of `e_p^full` on rank and on `overall_score`), p-values from permuting rank labels within the night, and — where a night has ≥ 2 picks in one sector ETF — within sector-direction cells. **Descriptive.** It is registered here so that it exists in the file before the numbers do, and so that it can never be read as a third primary; the ordering question belongs to F2 and to H-067, not to this endpoint set.
- **The rest of the ladder and the counter side:** first touch of L1, L2, L4 on their own lane windows, the counter-direction levels and the printed swing stop (recomputed by the desk from bars, never read from the outcome table), the order in which levels were hit, MFE and MAE in ATR from entry, sessions-to-first-touch (descriptive by DP-44).
- **The 40-session L3 result** wherever matured (DP-09); **the ±1.5 ATR synthetic-level version of E1** (target at a fixed ATR distance from `C_t` instead of the printed L3), which is the read on §10.7.
- **Close-to-close return** at T+20 by side. **Fixed-horizon return is descriptive by rule 5 and DP-01 and never decides, in any branch.**
- Sub-cells: bull/bear, score band (< 80 / 80–85 / 85–90 / 90+), `best_timeframe` lane, sector ETF, tape stratum, regime label — **reported only at ≥ 20 measured contributing nights, SUPPRESSED below, counts printed either way.** SUPPRESSED means counts only: no point estimate, no sign, no "small n, directionally", no q. A cell suppressed at lock stays suppressed even if it clears 20 at the pass. Suppression restricts affirmative reporting only — it never removes a cell from §8's opposite-sign clause.

**Quotability.** A 20-session window is **NON_QUOTABLE** under rule 12 in every branch; nothing is quotable at all before PROSPECTIVELY_CONFIRMED (rule 10).

**Inference (rule 6).**
- **p-values (decide significance):** E1 — the B2 within-block published-label permutation, 10,000 draws, seed 20260913. E2 — paired sign-flip permutation on `A_t` across nights, 10,000 draws, same seed (paired, because both matches are computed on the same picks on the same night). Night-level sign-flip p for E1 printed alongside; the block-permutation p decides.
- **CIs (decide the excludes-zero clause):** stationary block bootstrap over the ordered contributing nights, **expected block length 10 sessions** (half the forward window — the Q011 / Q015 / Q022 convention, fixed here, not chosen after seeing results), 2,000 resamples. The date-clustered bootstrap CI is printed alongside and is expected to be narrower; **the block-bootstrap interval decides.**
- **Match adequacy, pre-registered as a gate (§8 clause 7):** post-match standardised mean differences per feature, over all matched pairs, for B1 and for B4. |SMD| ≤ 0.25 on every B1 feature is required for E1 to be read as an attribution result at all.
- **Symbol overlap:** distinct symbols, repeat-selection counts, leave-one-symbol-out jackknife on both endpoints, and both endpoints recomputed with each symbol's contribution capped at its median night count. Descriptive.
- Every estimate prints: n(contributing nights), n(contributing nights dated after the lock commit), n(gradeable picks), n(HIT), n(`passed_at_entry`), n(control rows and control-set sizes for B1, B3, B4), n(picks dropped for < 3 B1 controls, by sector), n(unmapped), n(ungradeable), n(immature), n(excluded by reason), and the post-match SMDs.

## 5. Sample floors, expected n, dates

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** and ≥ **20 contributing nights per reported cell**. A cell below 20 is SUPPRESSED and does not by itself make an endpoint INCONCLUSIVE. **No floor is ever lowered to hit a date.** E2's floor is counted on nights carrying ≥ 3 picks with **both** control sets, which is a subset of E1's contributing nights and is printed separately.
- **Binding maturity: 20 sessions** from the session t+1 entry.
- **Exposure basis, and what is measured versus assumed (DP-50(c): no live query stands behind any number here).**
  - **Measured, on the pinned freeze** (`research/reports/STEWARD_Q022_exposure.md`, counts only): over **2026-07-08..2026-09-10, 46 elapsed sessions, every one of the 46 sessions published at least one pick** (§(c) of that report) — the eligible-night rate before the pick-level screens is ≈ **1.0 per elapsed session**. Same-sector control availability, which is the closest measured analogue of B1's binding constraint, retains **80.9%** of picks with ≥ 3 same-sector controls (median pool 7) and **31 of 32** nights retain ≥ 50% of their picks (§(e)). The §2.4 screens cost a measured 1.45% (no swing target), 3.5% (price scale), 0.7% (`outcome_target_invalid`) and 0% (insufficient prior bars) of sealed-period picks (§(g)).
  - **Not measured, and this is the one number that sizes the question:** the contributing-night rate under B1's *stricter* match — same sector **and** a 1.5-MAD caliper on five features, minimum 3 controls, on nights needing ≥ 3 such picks. It must be below the same-sector figure and is not derivable from it.
  - **The assumption the schedule below uses, chosen as a lower bound:** contributing-night rate = **0.696 per elapsed session** — Q022's *measured, fully matured* contributing rate for its own narrower night set, used here as a conservative stand-in rather than the ≈ 1.0 eligible-night rate this question's wider night set would suggest (DP-45: never the assumption that reaches a date sooner).
  - **R1 (routed, counts only, due before lock):** the Steward measures, on `manifest_v001` + `manifest_prices_v001` and nothing live, over 2026-07-08..2026-09-10 and its matured sub-window: (i) contributing nights under §2.4's full definition and their rate per elapsed session; (ii) the distribution of B1 control-set sizes and the share of picks dropped for < 3 controls, **by sector ETF**; (iii) the same for B4; (iv) picks carrying both sets; (v) the funnel counts of §2.4 on this window. **No outcome of any kind** — no touch, no first-touch date, no return, no excess, and no cross-tab of any exposure against any outcome. Forward bars are read only to establish that a bar exists.
- **DEFERRED gate, stated as the inequality R1 must clear.** Lock proceeds only if the measured contributing-night rate is **≥ 0.35 per elapsed session**. Below that line, 80 contributing nights need more than ~229 sessions from 2026-07-08 and the decision date passes DP-43's 12-month ceiling (2027-09-14), so Q024 goes to `research/questions/DEFERRED.md` with the measured rate and the projected date named, instead of being locked (the H-062 precedent). **If R1 measures a rate between 0.35 and the assumed 0.696, the window end and every date below are recomputed before lock at the one-sided 90% lower bound of the measured rate — moving out, never in.** No floor, gate or MPE moves with them.
- **Window, decision date, extension, fallback (DP-43; DP-13) — as drafted, subject only to the R1 recomputation above:**
  - **Primary window: pick nights 2026-07-08..2027-01-13 inclusive = 132 elapsed sessions** from the start. Sized at the conservative end of the assumed rate, not at its point estimate: `r` = 0.6957, one-sided 90% lower bound `r₉₀` = 0.6088, `80 / 0.6088` = 131.4 → 132 sessions. At `r` that projects ≈ 92 contributing nights; at `r₉₀`, ≈ 80. The margin is a sizing convention, not a gate: every gate fires on the counts `eval.py` prints at the pass.
  - **Decision date: Monday 2027-02-22.** Session t+20 after the last pick night 2027-01-13 is 2027-02-11 (MLK 2027-01-18 removed); plus a one-week freeze margin; first Monday on or after. The Steward re-confirms the exact session-count date from the trading calendar when building the successor freezes, and that re-confirmation may move the date **out, never in**. `eval.py` is written once (rule 9) and run **once**, then. **No interim looks at either endpoint.**
  - **Gates at the pass, on measured counts:** ≥ 80 contributing nights **per primary endpoint**, and ≥ **30 contributing nights dated after this file's lock commit** (DP-24, projected to arrive ≈ 2026-11-10 at the assumed rate, with ≈ 52–59 post-lock contributing nights by the window end). Whether the lock-night pick counts as post-lock is immaterial and is decided mechanically by comparing `finished_at` to the lock commit.
  - **One automatic extension (DP-13; DP-43's +30 sessions), fired on measured counts, with no new question:** window extends once to pick nights **2026-07-08..2027-02-26**, decision **Monday 2027-04-05**, using the **unmodified `eval.py`** and the same gates. Extension nights join Half B.
  - **DEFERRED fallback:** if a gate is still short after that single extension, Q024 goes to DEFERRED with the measured counts rather than running under-powered. There is no second extension, no reduced gate, and a gate shortfall is **not** an INCONCLUSIVE verdict.
  - Both dates sit inside DP-43's 12-month ceiling (5.4 and 6.7 months from a 2026-09-14 lock). **PROSPECTIVELY_CONFIRMED is reachable from this run by design**; DP-31's HISTORICAL_ONLY handling does not apply and no successor replication is needed.
  - **The one live route back to DEFERRED.** A **dated** platform ship inside the window that changes **which picks are published** (the publication predicate, the publication floor, the slate size) changes the treatment itself and re-fires §6's start rule; the whole schedule is then recomputed at the measured rate. A restart costs ≈ 227 calendar days, so the latest survivable ship is ≈ 2027-01-30 — every in-window ship is survivable, barely. A ship that changes the **ladder** (target placement) is the same class and is treated identically.
- **Freeze discipline (DP-23).** Nights ≤ 2026-09-10 stay pinned to v001. Later nights enter only through `manifest_v002` (selections, same SQL, same exclusion criteria, plus the pinned sector blob as a static artifact and the add-only successor exclusions file) and `manifest_prices_v002` (same Alpaca queries), covering pick nights **2026-07-08..2027-01-13** with forward bars **20 sessions beyond** (through 2027-02-11), the daily symbol list extended to **every candidate on every in-window night, published and unpublished**, each with **≥ 60 sessions of prior bars before its first appearance** (B1 needs `beta60`, `mom60` and `adv20` for the control pool, not only for the picks), plus hourly bars for published symbols, plus the CTRA-signature scan repeated. A second pair only if the extension fires. `eval.py` takes the window bounds, manifest paths, exclusions paths, sector-artifact path and output directory as inputs — **no hard-coded dates, names or paths** — records every sha256, and prints pre-lock and post-lock night counts separately.
- **DP-50 discipline.** If a platform repair before `manifest_v002` rewrites `sas_candidates` rows or price rows this question reads, it gets a dated `research/data/DATA_NOTES.md` entry naming the column, the range and the ship SHA, and the window splits at that date as two features (DP-50(a), the DP-06 pattern). If it changes which picks are published, it changes the treatment and §6's start rule re-fires. As of 2026-09-13 the platform's `main` HEAD **is** the manifest SHA `fa70688` — zero commits merged since the freeze (R1(a) of `STEWARD_Q022_exposure.md`); the clause stays live for the period between the two freezes.

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-07-08.** After the 2026-06-01 catalyst fix (DP-06, `69ef05f`), after the point-in-time regime label begins on 2026-06-09 (FREEZE_v001 §7), and after both population-defining ships DATA_NOTES records: `_enforce_ladder_monotonic` (`5fa3db4`, which took cross-lane ladder non-monotonicity from 25.71% to 0.00%) and the `publication_floor = 80.0` codification (`1765a6f`). Both are population-defining here: the ladder sets the ATR distance that every control inherits, and the publication predicate defines the treatment. The window is placed so the question reads **one mechanism, not a blend**.
- **The start is a rule, and the rule was run against the measured ship clock.** `window_start` = the first non-excluded pick night whose nightly run *begins* after the last population-defining ship, ship timestamps in ET against `sas_runs.finished_at`. Measured (R1(a), `STEWARD_Q022_exposure.md`): `5fa3db4` ships 2026-07-06 15:13:42 ET; `1765a6f` ships 2026-07-07 21:43:53 ET, four hours *after* that night's run finished; 2026-07-06 is excluded anyway as a late-finishing manual re-run. First run to begin after both ships: **2026-07-08** (started 17:19:37 ET). The rule stays here rather than a bare date because it re-fires on any later dated ship of the same class, and it can only move the start **out, never in**.
- **Cost of that start, stated plainly:** ≈ 22 sealed sessions (2026-06-09..2026-07-07) are discarded and they were usable. The alternative was a blended population: two ladder mechanisms and two publication predicates inside one treatment definition.
- **Contamination check (registrar; no results directory was read, rule 3).** Nothing on the desk reports any outcome by sector, by size or by exposure cell: EXPLORE_001 §8/§D say only that `industry` is 12% populated (a coverage fact with no outcome attached), and `research/reports/weekly/` and `daily/` carry no sector, size, dollar-volume or exposure-conditioned figure. Q006's numbers are unread and unknown to this draft. Every load-bearing choice here — the level, the clock, the entry, the MPE, the feature list, the caliper — comes from DP entries, from H-068 as Haci wrote it, or from constructions already locked in Q006 and Q022.
- **Split for "holds in both halves" (rule 7), fixed by date here rather than derived later:**
  - **Half A = pick nights 2026-07-08..2026-09-11** (47 elapsed sessions; ≈ 33 contributing nights projected; sealed-but-unread at lock).
  - **Half B = pick nights 2026-09-14..2027-01-13** (85 elapsed sessions; ≈ 59 projected; entirely after the lock commit). Extension nights join Half B.
  - The halves are **not** sub-cells and are not on the suppression list; `eval.py` prints each half's night count beside its estimate. `in_sample_end = 2026-05-29` marks only what is excluded from this question entirely.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` for nights ≥ 2026-06-09 only (every night here qualifies), `regime_version = 'v1.2'` only, same-evening writes only; a later-posted row is treated as missing.
  - Primary tape stratum, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's trailing 20-session return × tercile of SPY's trailing 20-session realised volatility, from SPY bars ≤ t, with **expanding-window** tercile cut points (for night t, from 2026-03-02..t). Cells below 20 contributing nights are SUPPRESSED.
- **Knowledge time (rule 14) — every input declared. Q024 needs no rule-14 exception and requests none** (DP-05 untouched; DP-41 respected).

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe` | `sas_candidates` | pick night, 16:05 ET | population, sub-cells |
  | swing lane plan (`targets[0]`) | `sas_candidates.public_payload_json.lane_plans` | written during the nightly run before `finished_at` (`services/super_agent_select_service.py:155-161`) | primary level |
  | symbol → sector ETF | pinned `sp500_sectors.json`, sha256 `c4d12610…0201` | 2026-05-17, seven weeks before the first in-window night; never re-synced | sector block, B3 pool |
  | `beta60`, `atr_pct`, `mom20`, `mom60`, `adv20`, `C_t` | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | exposure vector, ATR distance, sensitivity basis |
  | control pool (non-published rows for night t) | `sas_candidates` | pick night, 16:05 ET | B1, B3, B4 pools |
  | SPY tape (trailing return, trailing vol, expanding terciles) | `prices_daily_split`, SPY bars ≤ t | pick-night close | stratum |
  | regime label (v1.2, same-evening rows only) | `market_regime_daily` | pick night, 16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion |
  | session t+1 open; daily bars t+1..t+20; hourly bars (published symbols) | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **entry and outcome measurement only** |

  **What `eval.py` must enforce:** the eligible set, the exposure vector, the sector label, every matched set, the level, the ATR distance and every stratum label are computed and written to a frozen per-night and per-pick table **before any post-pick-night bar is loaded**; the run fails loudly if any t+1-or-later field is referenced in eligibility, matching or stratification, fails loudly on a sha256 mismatch on the sector artifact, and fails loudly on a split-basis disagreement between `prices_daily_split` and `prices_daily_raw` for any symbol-date it uses. `sas_selection_excursion`, every `outcome_*` column and `level_hit_dates_json` are **never** inputs (different basis, recomputed weeks later, manual overrides possible — `services/sas_excursion.py:336-354`, `routers/performance.py:935-970`). `uoa_symbol_daily.*` is banned outright (FREEZE_v001 §5; PI-001).

## 7. Multiple testing

- **Within the question: m = 2 primary endpoints (E1, E2).** Benjamini–Hochberg across those two; the verdict uses q. No secondary may be promoted at the pass — the feature-by-feature ladder, the rank-information panel, B3, B5, the rest of the ladder, the ATR-level variant and the fixed-horizon return all print raw p only, marked "descriptive, does not decide".
- **Across the family: F1 Selection edge** (DP-29). Registered F1 questions at this registration: **Q006 (2 primaries)** and **Q024 (2)** = **4 primary endpoints**. Q001 is superseded and not counted; **H-062 is DEFERRED and is not in the correction set while deferred**; H-002, H-003 and **H-067** are unregistered. Stated symmetrically and never shrinking below the 4 registered at this lock: BH runs over the primary endpoints of F1 questions **locked by the decision pass**, so if **H-067** registers and locks before 2027-02-22 its primaries join the denominator; a question leaving F1 after this lock does not lower Q024's denominator. Threshold **q ≤ 0.10**.
- **Overlaps (not duplicates; never presented as independent evidence):**
  - **Q006 (F1)** is the parent. Q024's E1 is Q006's E1 with a wider control and a different window (2026-07-08 onward versus 2026-04-01..2026-09-10) and a 20-session rather than a 40-session clock. **A confirmed E1 here is not a second confirmation of Q006 and may never be reported as one**, and the two can disagree: that disagreement *is* E2. The Reporter states the dependence explicitly wherever both appear.
  - **Q022 (F4)** shares the pinned sector artifact, the window, the entry, the level, the clock and the B4 control construction, and its own control-adjusted per-night quantity is Q024's `E_t^part`. Q022 asks whether concentrated slates behave differently; Q024 asks whether sector membership explains the edge at all. Cross-referenced, never counted twice, and the two must be read together if both confirm.
  - **H-067 (F1, unregistered)** is the same null from the benchmark side (SPY, equal-weight, momentum rank). It is **not** merged here: H-067 compares SAS to *external* benchmarks, Q024 compares SAS to its *own* same-night universe holding exposure fixed. If H-067 registers, the Reporter reads them as two halves of one attribution argument.
  - **Q015 / Q023 (F2, score bands)** touch the ordering question that Q024 carries only as a descriptive panel; nothing in §4's rank panel may be offered as evidence for or against them.

## 8. Decision rule (numeric, written before unsealing)

Both endpoints are in **percentage points of L3-touch rate within 20 sessions from the session t+1 open**, night-level. **MPE = +5.0 pp on each** (DP-20, the standing touch-rate MPE; DP-44 forbids inventing an alpha-unit or money-unit MPE for a residual, and none is invented here).

**E1 — the residual. HISTORICALLY_CONFIRMED requires all of:**
1. ≥ 80 contributing nights, with ≥ 30 dated after the lock commit (DP-24);
2. `|E1| > 5.0 pp`;
3. the block-bootstrap 95% CI excludes 0;
4. the **B2 within-block permutation** p gives BH q ≤ 0.10 within the question;
5. the point estimate has the **same sign in both halves**, and neither half is beyond 5.0 pp in the opposite sign;
6. no tape or regime stratum with ≥ 20 contributing nights is beyond 5.0 pp in the opposite sign;
7. **match adequacy:** post-match |SMD| ≤ 0.25 on **every** B1 feature (`beta60`, `atr_pct`, `mom20`, `mom60`, `size`) and 100% same-sector matching by construction.
A confirmed **positive** E1 reads "the ranking survives the exposures we can measure". A confirmed **negative** E1 reads "published picks reach their own target *less* often than their exposure twins" and is reported with that sign, in those words.

**E1 — NULL:** ≥ 80 contributing nights, clause 7 satisfied, the 95% CI includes 0 **and** `|E1| < 5.0 pp`. This is H-068's predicted outcome and is ledgered with the same care as a positive: "after conditioning on sector, market beta, size, 20- and 60-session momentum and volatility, publication adds no measurable touch-rate edge."

**E1 — INCONCLUSIVE:** anything else — nights below floor, halves disagreeing in sign, `0 < |E1| ≤ 5.0 pp` ("positive but below MPE" is INCONCLUSIVE, rule 6), or **clause 7 failing** (a feature left unmatched means the attribution claim is not supported by the design; this is a matching failure, not a null).

**E2 — the attribution gap. HISTORICALLY_CONFIRMED requires all of:** clauses 1, 3, 5, 6 above computed on `A_t` and its own contributing-night count; `|E2| > 5.0 pp`; the paired sign-flip permutation p giving BH q ≤ 0.10; and clause 7 for B1. A confirmed **positive** E2 means the three-feature control materially overstates the edge — **the exposure attribution is real**. A confirmed negative E2 means the wider match makes the picks look *better*, which is also a finding and is reported as one. **NULL** (CI includes 0 and `|E2| < 5.0 pp`) means the extra exposure dimensions change nothing measurable and Q006's control was adequate. **INCONCLUSIVE** on the same grounds as E1.

**Question level.** The stronger endpoint does not carry the question. The four readings are reported as such: E1 confirmed + E2 null → a residual that exposure does not explain; E1 null + E2 confirmed → the edge was exposure; both null → no edge and nothing to attribute (and the Q006 control is adequate); both confirmed → part of the edge was exposure and part survives, with both magnitudes printed. **Any combination that includes an INCONCLUSIVE endpoint is reported endpoint by endpoint and the question is marked INCONCLUSIVE overall.**

**PROSPECTIVELY_CONFIRMED:** only after ≥ 30 contributing nights dated **after this file's lock commit** reproduce the sign under the unmodified `eval.py` (DP-24; projected to be satisfied inside the primary window). No subscriber-facing claim before that (rule 10); even then the basis is NON_QUOTABLE (rule 12).

## 9. If CONFIRMED, what changes on the platform

- **E1 confirmed positive →** the conviction card's ladder hit rates gain a "matched-control rate at the same ATR distance" row computed against the **full exposure vector**, not a three-feature match, and a bare L-level hit rate is never shown again. Brief against `services/sas_conviction_card.py`. A Manual Trading Guide line may then say the edge is not merely sector and momentum exposure — in exactly those terms, no stronger.
- **E2 confirmed positive →** binding on the desk before it is binding on the product: every matched-control number the platform or the desk prints must use the full exposure match, and the Reporter restates each three-feature-matched figure with the measured attribution gap beside it. Product side: a conviction-card flag when a pick sits in the top decile of the night on `mom20` / `mom60` or in the night's dominant sector, saying the ladder rate reflects that profile.
- **E1 null (with clause 7 satisfied) →** the F1 selection-edge line closes for this construction: no subscriber-facing selection claim, effort moves to F3 (new information) and F6 (execution), and the honest repositioning — SAS as an exposure screen that finds the right sector and the right momentum profile, not a ranking engine — goes to Haci as a product-claim question, not as a marketing line.
- **E1 confirmed negative →** an immediate guide line and a red-team review of the ranking layer weights, since publishing would then be worse than its own twin cohort.
- Nothing follows from the descriptive rank panel, from B3, or from any fixed-horizon number, in any branch.
- Owner: implementer. Shadow ≥ 20 trading days; flag-off with a byte-identical checksum on the old path before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **The exposure vector is not "all known exposures", and the claim must not be phrased as if it were.** No true market cap, float, short interest, analyst-revision or earnings-cycle exposure is in the freeze. `size` is `log10(adv20)`, a liquidity proxy for size (§2.3). A surviving residual is "residual after sector, beta60, adv20, mom20, mom60 and ATR%" and is written that way everywhere.
2. **The sector block drops picks, and not at random.** Measured analogue: 19.1% of picks have < 3 same-sector controls (`STEWARD_Q022_exposure.md` §(e)); the caliper will drop more. Losses concentrate in thin sectors, so the graded set tilts toward XLK. Mitigations: the drop is counted **by sector** and printed in the funnel; E2 is computed on the intersection set so composition cannot leak into the attribution gap; E1 under the partial match is printed on the identical retained set as a like-for-like companion.
3. **Tighter matching means smaller control sets and noisier `e_p`.** Minimum 3, maximum 10, sizes printed; the block bootstrap carries the extra variance into the CI rather than hiding it. A shrinking control set does not bias E1, but it widens it, and the MPE is not lowered to compensate.
4. **Conditioning on exposures does not make publication as-if-random.** B2's null assumes exchangeability of the published label *within* a block; the engine may select on catalyst or flow information correlated with the future path that the vector does not contain. That is precisely what a surviving residual would mean — and also what an unmeasured confound would look like. The design cannot separate them, and §9's language is bounded accordingly.
5. **Momentum horizon.** 20 and 60 sessions may not be the momentum the projection layer trades; a residual could be momentum at a horizon not matched. The skip-20 variant is printed; a full horizon sweep is a successor question, not a promotion at the pass.
6. **Overlapping forward windows** inflate precision across adjacent nights; block bootstrap with a length fixed here, not chosen after seeing results.
7. **Ladder placement is not ATR-scaled** (`ai_agents/principal_agent.py:530-575`, fallback 0.5%/1% steps at `:897-911`), so L3's ATR distance varies by pick; the control inherits the distance by design, but if distance correlates with pick quality the endpoint mixes selection with target placement. The ±1.5 ATR synthetic-level variant is the registered read on this.
8. **Sector mapping gaps** (BRK.B, BF.B) and the mapping's 2026-05-17 vintage: a reclassification after that date is not reflected, which is the price of a pin that cannot look ahead. Never hand-mapped, always counted.
9. **Q006 dependence.** Q024 shares picks, construction and family with Q006 across part of its window; the two are never presented as independent confirmations, and BH within F1 is applied over both.
10. **Half A is sealed-but-unread at lock,** so the "both halves" clause is a genuine out-of-sample check only for Half B; Half B is the post-lock half and carries the DP-24 clause.
11. **The desk holds no option price history.** The residual is measured on the stock path; what Haci trades is a spread. The path is a proxy, and §9 licenses nothing about DTE or structure (ENHANCEMENTS EN-011; `research/questions/DEFERRED.md`, H-055).
12. **A platform ship inside the window** that changes publication or ladder placement changes the treatment; §5 and §6 name the trigger, the recomputation and the cost.

## 11. Open decisions before lock

1. **Size proxy** — Options: A `log10(adv20)` from bars only / B `log10(adv20)` **plus** a static large/small tier from the platform's `data/sp500_symbols.txt` and `data/r2k_symbols.txt`, pinned by sha256 like the sector file. Recommendation: **A**, because those two symbol files carry no `_meta` date and the desk could not establish their commit dates from here, so pinning them would import an artifact of unknown vintage into a rule-14 table for a marginal gain over a continuous proxy. Changes: §2.3, §3 B1, §8 clause 7, §10.1.
2. **Sector conditioning** — Options: A hard block (control must share the pick's sector ETF; pick dropped and counted when fewer than 3 qualify) / B sector as a penalty term in the distance so no pick is ever dropped. Recommendation: **A**, because a soft penalty leaves partly unmatched exactly the exposure H-068 is about, and the ≈ 19%+ pick loss is a disclosed, counted cost rather than a hidden one. Changes: §2.4, §3 B1, §5 (rate), §10.2.
3. **R1 before lock** — Options: A commission the Steward's counts-only exposure report (§5 R1) and re-size the window at the measured rate before locking / B lock now on Q022's measured 0.696 stand-in. Recommendation: **A**, because the contributing-night rate under the stricter B1 match is the one number that decides whether the floors are reachable at all, it is a count on frozen data (DP-50(c)), and a wrong rate here buys a DP-13 extension that was meant to be a fallback rather than the plan. Changes: §5 (rate, window end, all dates), §8 clause 1.
