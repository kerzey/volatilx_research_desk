# Q003 — repeat_selection: are first-time picks weaker than picks SAS keeps re-selecting?

**Status:** DRAFT (lock by committing this file after Haci review)
**Family:** F6 Exits and execution (hypothesis H-052, sharpened by EXPLORE_001 §G)
*Registrar's note on family:* H-052 is filed under F6 in `research/BACKLOG.md`, but this is a
selection question tested with F7's path objective. It stays in F6 so the BH family matches the
backlog; if Haci re-files H-052 into F1 or F7, the family assignment moves with it and the
Reporter recomputes q against the new family.
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — plus the successor freezes named in §5.
**Exclusions:** research/data/exclusions_v001.json (`manual_runs.trading_dates`, 5 nights)
**Registered by:** registrar · **Approved by:** haci · **Date:** 2026-09-10

---

## 1. Hypothesis (plain English)

**A stock SAS has published repeatedly in the last two weeks is a better pick than a name it is
publishing for the first time: the repeat name reaches its third target more often, and beats its
own matched control by more, than the first-timer does.**

Formally: among published picks with a full 10-session publication history, picks on a **3+
appearance streak** show a higher L3-within-40-sessions first-touch rate, and a higher excess over
their distance-matched control, than **first-time picks** (not published in the prior 10 sessions).

## 2. Population

- **Unit of inference: the trading night** (rule 6). Within a night, each streak cell is averaged
  first; the estimator is a per-night paired difference between cells.
- Source tables (manifest_v001): `sas_candidates` (published picks + full universe, lane plans,
  `selected_rank`, `overall_score`, `dominant_direction`), `sas_runs` (`finished_at`, `config_json`).
- Source tables (manifest_prices_v001): `prices_daily_split` (paths, ATR14, beta60, run-up),
  `prices_daily_raw` (split-factor snapping), `prices_hourly_raw` (same-day tie-breaks only).
- **Streak definition (computed only from published-pick history, all of which is known at 16:05 ET
  on the pick night):** for pick (symbol s, night t), `appearances_10 = ` number of the prior 10
  trading sessions on which s was published by SAS (`selected_rank` not null). Excluded manual-run
  nights **do not count** as appearances and **do not consume** a lookback slot; the lookback walks
  back over non-excluded sessions only.
  - **Cell A — first-time:** `appearances_10 = 0`.
  - **Cell B — streak:** `appearances_10 ≥ 3`.
  - Picks with `appearances_10 ∈ {1, 2}` are **reported descriptively** (the middle cell) and are
    **not** part of the primary contrast.
- A pick enters the population only if its symbol has a **full 10-session** publication history
  available in the frozen SAS tables (i.e. the pick night is at least 10 non-excluded sessions after
  2026-04-01). This censors the first two weeks of the manifest and is stated in the results header.
- Exclusions (counted, printed, never silent): the 5 manual-run nights; picks without a lane-plan
  ladder; picks whose L3 is on the wrong side of the actual pick-night close at publication;
  nights whose 40-session window has not matured in the pinned freeze (**excluded, not graded as a
  miss**); missing-bar symbols (night dropped if > 25% of picks are missing).
- Reference price = the **actual** pick-night close from `prices_daily_split`; ATR = ATR14 from
  split-adjusted bars through the pick night, converted to the signal-date basis (DATA_NOTES: the
  platform's `atr_pct` is corrupted around splits).
- Level and window are the platform's own: L3, lane window **40 trading sessions**, first touch
  (volatilx `services/sas_conviction_card.py:182-195`).

## 3. Baseline(s) — what this must beat

- **B1 (the primary baseline): first-time picks in the same regime, same nights.** The hypothesis is
  a contrast between cells, so the first-time cell *is* the baseline; both cells are measured on the
  same nights so the tape is differenced out.
- **B2 (the distance-matched control, per cell):** identical construction to Q006 §3 — the **10
  nearest same-night unpublished candidates** on `beta60`, `atr_pct`, `runup20` (night-wise
  median/MAD standardization, Euclidean distance, with replacement, symbol-ascending tie-break),
  each graded against a synthetic target at the **same ATR distance and direction**, under exactly
  the pick's rule and clock. Control rows never add to inferential n (rule 6).
  B2 exists because a streak pick is, by construction, a name that has already run: the matched
  control absorbs "it is a high-beta name that just went up" so that the streak effect is not just
  momentum. **This is why the primary endpoint is the *excess*, not the raw rate.**
- **B3 (descriptive):** the 1–2 appearance middle cell, to show whether the relationship is
  monotone in streak length or a first-time penalty only.

## 4. Objective metric (amended rule 5 — price path)

**Entry basis: the next session's open**, identically for picks and controls. A level at or through
the entry price at the open is **not a hit** (`passed_at_entry`).

**Primary endpoints (two, pre-specified, BH-corrected within this question):**

- **R1 — raw touch-rate gap.** For each night t with ≥ 1 pick in **both** cells:
  `D1_t = mean_{p ∈ B}[touch_{L3,40}] − mean_{p ∈ A}[touch_{L3,40}]`; estimand `mean_t(D1_t)`.
- **R2 — matched-control excess gap (the decisive one).** With
  `excess_{p} = touch_p − mean_{c ∈ match(p)}[touch_c]`,
  `D2_t = mean_{p ∈ B}[excess_p] − mean_{p ∈ A}[excess_p]`; estimand `mean_t(D2_t)`.
  R2 is the endpoint that maps to the trading decision, because it asks whether the *selection* is
  better, not whether the *stock* is hotter.

**Secondary, descriptive, never decides:** per-cell raw and excess rates with their own CIs;
the 1–2 middle cell; L1/L2 (20 sessions), L4 (40), L5/L6 (60); unconditional speed cuts (L3 within
5 sessions) per cell; days-to-touch among touchers; counter-direction touches; streak length as a
continuous variable (0..10) with a monotonicity check; the same analysis with elite (90+) picks
removed (EXPLORE_001 reports the pattern is not an elite artefact in-sample — verify out of sample);
close-to-close T+10/T+20 return per cell (secondary by rule 5).

**Quotability:** 40-session basis → **NON_QUOTABLE** (rule 12).

**Inference.** Night-level, paired within night. CI: date-clustered bootstrap over nights (2,000
resamples) and a stationary block bootstrap with expected block length 20 sessions (overlapping
40-session windows). p: paired sign-flip permutation on `D_t`, 10,000 permutations. A second,
stricter permutation is reported as a robustness check: **within each night, permute the streak
labels across that night's picks** (10,000 draws), which holds the night's composition fixed.
Every estimate prints n(nights), n(picks per cell), n(control rows).

## 5. Sample floors and expected n

- Floors (rule 6): **≥ 20 nights per cell, ≥ 80 nights total.** Cells below 20 nights are
  **SUPPRESSED**.
- The primary estimator needs **both** cells present on a night, so the binding count is
  `n_paired` = eligible nights with ≥ 1 first-time pick **and** ≥ 1 streak pick.
- **Cell-size problem, stated plainly.** Streak picks are a minority of the book. From EXPLORE_001's
  in-sample coverage (sample sizes only, no outcomes): of the nights with a full 10-session history,
  the first-time cell was populated on nearly every night and the 3+ cell on a similar share, with
  roughly 2–4 picks per night in each. Expect **n_paired ≈ 0.85 × eligible nights**, i.e. about
  15% of nights lose one cell entirely and drop out of the primary.
- **Expected n today (2026-09-10), test window = sealed only (§6):** eligible sealed nights with a
  matured 40-session window are those ≤ **2026-07-14** → ≈ **31** nights, ⇒ `n_paired ≈ 26`.
  **Far below the 80-night floor.** This question cannot be answered today and is registered
  precisely so that the nights that answer it are clean.
- **Floor date.** To reach `n_paired ≥ 80` we need ≈ 94 eligible sealed nights, i.e. pick nights from
  2026-06-01 through roughly **2026-10-14** (≈ 21 nights/month, one manual-run exclusion already
  inside the window); the last of those matures 40 sessions later, around **2026-12-10**.
- **Decision date: 2026-12-15.** Locked now, evaluated **once**, then. **No interim looks** (rule 9).
  If Haci wants an earlier read he must register a *separate*, differently-numbered question with a
  20-session-capped endpoint — that variant would reach its floor around late October 2026 — and it
  will carry its own BH burden. Peeking at this one early voids it.
- **Freeze discipline:** nights ≤ 2026-09-10 stay pinned to `manifest_v001`; prospective nights
  enter through successor selection and price freezes produced with the same SQL and the same
  exclusion criterion (`finished_at` later than the next session's open ⇒ excluded). `eval.py`
  records all manifest sha256s and prints sealed vs post-lock night counts separately.
- Sub-cells (bull/bear, score band, tape stratum) are reported only where they clear 20 nights.
  The 90+ cell is expected to be SUPPRESSED (DATA_NOTES: 12 / 8 / 3 / 2 elite picks per month since
  June).

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-06-01**, plus every night after this
  file's lock commit, through the decision date.
  *Justification (one sentence):* both the cell boundaries (0 appearances vs ≥ 3) and the 10-session
  lookback come from EXPLORE_001 §G's in-sample table, so under the contamination rule they may only
  be tested on data the Explorer never saw. April–May is not used at all, not even descriptively, in
  the primary table.
- **Split for the "holds in both halves" test:** within the test window — Half A = paired nights on
  or before the median paired-night date, Half B = after. `in_sample_end = 2026-05-29` (both
  manifests) is recorded only to mark what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` is legal only from **2026-06-09**, `regime_version = 'v1.2'` (manifest_v001
    `availability.market_regime`). Nights 06-01..06-08 carry no legal label and are stratified by the
    SPY proxy only, flagged as such.
  - Primary tape stratum, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's trailing
    20-session return × tercile of SPY's trailing 20-session realized volatility, from
    `prices_daily_split`. Cells < 20 nights SUPPRESSED.
- **Catalyst-layer regime change:** the window sits entirely after the 2026-06-01 earnings-resolver
  fix (`exclusions_v001.json.catalyst_layer_regime_change`, commit 69ef05f), so the scoring engine
  that produced these streaks is one feature, not two.
- **Knowledge time (rule 14):** the streak is built only from prior published picks, known at 16:05
  ET. Matching features come from bars dated ≤ the pick night. `uoa_symbol_daily.fwd_return_*` is
  banned (degraded). `sas_excursion.reselected_within_5d` / `reselection_*` are **outcome-table
  columns with a variable recomputation lag** (manifest_v001 `availability.sas_excursion`) and must
  **not** be used to build the streak — the streak is recomputed from `sas_candidates.selected_rank`.

## 7. Multiple testing

- **Within the question:** 2 primary endpoints (R1, R2); BH across the 2; the verdict uses q.
  Secondaries print raw p, marked "descriptive, does not decide".
- **Across the family:** F6 holds H-050, H-051, H-052 (3 hypotheses); registered F6 questions at
  registration: **Q003 only**. The Reporter applies BH across all primary endpoints of
  registered-and-run F6 questions.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`r1 = mean_t(D1_t)`, `r2 = mean_t(D2_t)`, in percentage points of touch rate.
**MPE = +8.0 percentage points** on both endpoints (**placeholder — Haci to confirm at lock**).
Rationale for a larger MPE than Q006/Q002: this is a difference between two cells' differences, so
it must clear a bar that justifies an actual position-sizing rule (skip or half-size first-timers);
anything smaller is not worth a product change.

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. `n_paired ≥ 80`, with ≥ 20 nights in each cell and ≥ 30 post-lock nights;
  2. `r2 > +8.0 pp` (**R2 is the gating endpoint**; a confirmation on R1 alone is not a
     confirmation of the hypothesis, because R1 can be pure momentum composition);
  3. bootstrap 95% CI on `r2` excludes 0;
  4. BH q ≤ 0.10 within the question;
  5. `r2 > 0` in **both halves** (§6), neither half below −8.0 pp;
  6. no tape stratum with ≥ 20 nights showing `r2 < −8.0 pp`.
- **NULL:** `n_paired ≥ 80` **and** the 95% CI on `r2` includes 0 **and** `|r2| < 8.0 pp`.
  A NULL means first-time picks are not worse once you control for the kind of stock they are — a
  useful, publishable result that stops a sizing rule from shipping.
- **INCONCLUSIVE:** anything else — n below floor, halves disagreeing in sign, `0 < r2 ≤ 8.0 pp`,
  or **R1 confirms while R2 does not** (that specific pattern is reported as "streak names are
  hotter stocks, not better selections" and is explicitly INCONCLUSIVE for the hypothesis).
- **PROSPECTIVELY_CONFIRMED:** only after ≥ 30 post-lock nights reproduce the sign with `r2 > 0`
  under the unmodified `eval.py`, on data frozen after the lock and never inspected before the
  decision date.

## 9. If CONFIRMED, what changes on the platform

- **A streak flag on the conviction card:** "3rd appearance in 10 sessions" shown next to the score,
  with the measured excess beside it.
- **A lane / sizing rule in the Manual Trading Guide and `playbook/`:** first-time picks are
  half-size or skipped; re-qualified names carry full size. This is a guide line, not a subscriber
  claim, until PROSPECTIVELY_CONFIRMED (rule 10).
- **A scoring-side follow-up brief, not an immediate weight change:** if the streak carries
  information the engine does not already price, that belongs in a registered layer question (F1
  H-003 ablation), not in a hand-tuned bonus.
- Owner: implementer. Ship flag-off with a byte-identical checksum on the old path; shadow ≥ 20
  trading days before any flip (rule 11).
- **If NULL:** the existing "re-qualification after a favourable move is continuation" finding is
  narrowed in the LEDGER to the return basis only, and no sizing rule ships.

## 10. Known threats to validity (registrar's own list)

1. **Streak is mechanically correlated with the stock having just run.** That is the entire reason
   R2, not R1, gates the verdict, and why the matched control includes `runup20`.
2. **Symbol concentration.** A streak cell can be two or three names repeated (DATA_NOTES: in-sample
   elites were 9 distinct symbols, mostly memory/semis). The report must print distinct-symbol counts
   per cell and a leave-one-symbol-out sensitivity on `r2`; if dropping a single symbol moves `r2` by
   more than the MPE, the verdict is downgraded to INCONCLUSIVE regardless of the CI.
3. **Overlapping 40-session windows**, and streak picks by construction overlap *each other* (the
   same symbol on consecutive nights), which is the worst case for independence. Mitigation: block
   bootstrap; plus a pre-specified robustness estimator that keeps only the **first** night of each
   symbol's streak episode, reported next to the primary.
4. **Censored lookback** at the start of the window: the first 10 non-excluded sessions of the
   manifest cannot host a streak measurement. The test window starts 2026-06-01 and the lookback may
   reach back into May (including excluded nights, which are skipped) — that is legal (it uses only
   published-pick history) but is stated in the header.
5. **The 20-night-per-cell floor can be met while the *pick* count is tiny.** The report prints both
   night and pick counts; a cell with ≥ 20 nights but < 40 picks is flagged as fragile.
6. **Elite thinning** (DATA_NOTES) shrinks the streak cell over time, because elite repeats were a
   large part of it; the decision date is far enough out that this could bite. If the 3+ cell falls
   below 20 nights at evaluation, the verdict is INCONCLUSIVE, not "no effect".
7. **`sas_excursion.reselected_within_5d` must not be used** — outcome table, variable lag.
8. **Deferred adjacent:** whether the streak rule should change *option structure* (H-055, H-056)
   cannot be settled without option prices. See `research/questions/DEFERRED.md`.
