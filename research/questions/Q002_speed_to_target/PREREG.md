# Q002 — speed_to_target: do SAS picks reach the near targets sooner than matched candidates?

**Status:** DRAFT (lock by committing this file after Haci review)
**Family:** F7 Path, entry timing & volatility (hypothesis H-065; related H-056)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — plus the successor price freeze named in §5.
**Exclusions:** research/data/exclusions_v001.json (`manual_runs.trading_dates`, 5 nights)
**Registered by:** registrar · **Approved by:** haci · **Date:** 2026-09-10

---

## 1. Hypothesis (plain English)

**The platform's edge is speed, not distance: a published SAS pick gets to its first, second and
third targets in fewer days than near-identical stocks SAS did not publish — even when both
eventually get there.**

Formally: measured from the next session's open, the share of picks that touch L1 within 2 sessions,
L2 within 2 sessions, and L3 within 5 sessions each exceed the distance-matched control's share at
the same ATR distance. All three are **unconditional** — every pick is in the denominator, whether
or not it ever touches.

## 2. Population

- **Unit of inference: the trading night** (rule 6); pick rows are averaged within a night first.
- Source tables (manifest_v001): `sas_candidates` (published picks + full candidate universe:
  `public_payload_json` lane plans, `selected_rank`, `overall_score`, `dominant_direction`,
  `context_json`), `sas_runs` (`finished_at`, `config_json`).
- Source tables (manifest_prices_v001): `prices_daily_split` (paths, ATR14, beta60, run-up),
  `prices_daily_raw` (split-factor snapping), `prices_hourly_raw` (same-day tie-breaks only).
- **Treatment rows:** every published pick on a non-excluded night **in the test window of §6**
  that carries a lane-plan ladder.
- **Control pool, night t:** every unpublished `sas_candidates` row on night t with ≥ 60 prior
  split-adjusted bars, ≥ 21 bars of run-up history, and forward bars covering the endpoint window.
- Exclusions (counted, printed, never silent): the 5 manual-run nights from
  `exclusions_v001.json`; picks without a lane-plan ladder (for the level they lack); picks whose
  level is on the wrong side of the **actual** pick-night close at publication (invalid target);
  nights whose window has not matured in the pinned freeze (**excluded, not graded as a miss**);
  missing-bar symbols (night dropped if > 25% of its picks are missing).
- Reference price = the **actual** pick-night close from `prices_daily_split`, never the platform's
  `spot_close`. ATR = ATR14 from split-adjusted bars through the pick night, converted to the
  signal-date basis (platform `atr_pct` is corrupted around splits — DATA_NOTES).
- Levels/windows are the platform's: L1/L2 lane window 20 sessions, L3 lane window 40
  (volatilx `services/sas_conviction_card.py:182-195`). The speed cuts below are **shorter** than
  those windows by design; the lane window only bounds the descriptive "eventually" comparison.

## 3. Baseline — what this must beat

**B1 (primary):** the distance-matched control, identical construction to Q006 §3 and to
EXPLORE_001's conventions: the **10 nearest same-night unpublished candidates** on `beta60`,
`atr_pct` and `runup20` (night-wise median/MAD standardization, Euclidean distance, with
replacement, symbol-ascending tie-break), each carrying a synthetic target at the **same ATR
distance in the same direction** as the pick's level, graded by exactly the same rule and clock.
Control rows never add to inferential n (rule 6).

**B2 (secondary, descriptive):** all same-night unpublished candidates, unmatched.

**B3 (secondary, descriptive, answers "is this just distance?"):** the pick's own
touch-within-the-full-lane-window rate. If picks and controls converge by session 20/40 but differ
at 2/5 sessions, the edge is speed rather than reach — that contrast is the point of the question
and is reported next to the primaries.

## 4. Objective metric (amended rule 5 — price path)

**Entry basis: the next session's open**, identically for picks and controls. A level at or through
the entry price at the open is **not a hit** and is recorded as `passed_at_entry` (this matters
most at L1 and is exactly the hazard Q004 measures).

**Primary endpoints (three, pre-specified, BH-corrected within this question):**

| id | Endpoint | Estimand |
|---|---|---|
| S1 | first touch of **L1 within 2 trading sessions** of the entry | `mean_t( mean_p[hit] − mean_{p,c}[hit] )` |
| S2 | first touch of **L2 within 2 trading sessions** | same form |
| S3 | first touch of **L3 within 5 trading sessions** | same form |

All three are unconditional: the denominator is every eligible pick on the night, touchers and
non-touchers alike. **Days-to-touch among touchers is survivor-biased and is descriptive only.**

**Secondary, descriptive, never decides:** the same three levels at 1 / 3 / 10 sessions and at the
full lane window; median and p75 days-to-first-touch among touchers; touch rate by the level's ATR
distance tercile (the "speed is distance" alternative); L4/L5/L6 at their lane windows; order of
level hits; close-to-close return at T+2 / T+5 (secondary by rule 5).

**Quotability:** 2-, 5-, 20- and 40-session windows → **NON_QUOTABLE** throughout (rule 12).

**Inference.** Night-level. CI: date-clustered bootstrap over nights (2,000 resamples); stationary
block bootstrap with expected block length 3 sessions for S1/S2 and 5 for S3 (overlapping forward
windows). p: paired sign-flip permutation on the night deltas, 10,000 permutations. Each estimate
prints n(nights), n(picks), n(control rows).

## 5. Sample floors and expected n

- Floors (rule 6): **≥ 20 nights per reported cell, ≥ 80 nights total.** Cells below 20 nights are
  **SUPPRESSED** — no point estimate is printed, not even "small n, directionally…".
- **Elite (90+) cell:** reported **only if** ≥ 20 eligible nights carry ≥ 1 elite pick; otherwise
  SUPPRESSED with the reason and the night count. DATA_NOTES records 12 / 8 / 3 / 2 elite picks in
  Jun / Jul / Aug / Sep-to-date, so the elite cell is expected to sit near or below the floor at the
  decision date; it is likely to be suppressed and that is the correct outcome, not a failure.
- Endpoint maturity is short: a night is eligible for S1/S2 once 2 sessions have passed, for S3 once
  5 have. Effectively every non-excluded night older than ~1 week qualifies.
- **Expected n today (2026-09-10), test window = sealed only (§6):** ≈ **66–70** nights
  (2026-06-01..2026-09-10 is 71 nights; 1 manual-run exclusion falls inside it, and the last ~5
  nights are immature for S3). **Below the 80-night floor today.**
- **Floor date:** ≈ 21 trading nights/month ⇒ the 80th eligible sealed night is a pick night around
  **2026-09-30 .. 2026-10-07** (the range reflects the 66-vs-70 discrepancy flagged in §10);
  its 5-session window matures ~5 sessions later.
- **Decision date: 2026-10-12.** Locked now, evaluated **once**, then. **No interim looks**;
  `eval.py` is written once and run once (rule 9).
- **Freeze discipline:** selections for nights ≤ 2026-09-10 stay pinned to `manifest_v001`.
  Prospective nights (2026-09-11 .. decision date) enter through a successor selection freeze
  `manifest_v002` produced by the Data Steward with the *same SQL* and the *same exclusion
  criterion* (`finished_at` later than the next session's open ⇒ excluded), plus the successor price
  freeze. `eval.py` records both manifests' sha256s and prints the sealed vs post-lock night counts
  separately.
- Cells: bull / bear; score band (< 80 / 80–85 / 85–90 / 90+); tape stratum (§6); level ATR-distance
  tercile (descriptive).

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-06-01**, plus every night after
  this file's lock commit, through the decision date. April–May is **not** used, not even as a
  descriptive panel in the primary table.
  *Justification (one sentence):* the speed *idea* is Haci's and predates the exploration, but the
  specific cuts — 2 sessions at L1/L2 and 5 sessions at L3 — echo EXPLORE_001 §E's in-sample speed
  tables, so under the contamination rule the thresholds may only be tested on data the Explorer
  never saw.
- **Split for the "holds in both halves" test:** since the whole window is post-05-29, the calendar
  split is **within** the test window: Half A = eligible nights on or before the median eligible
  night date; Half B = after it. The in-sample/out-of-sample boundary `in_sample_end = 2026-05-29`
  (both manifests) is recorded here only to mark what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` is knowledge-time-legal **only from 2026-06-09** and only
    `regime_version = 'v1.2'` (manifest_v001 `availability.market_regime`; pre-06-09 rows were
    backfilled 06-02/06-08). The test window starts 06-01, so the first ~6 nights have no legal
    label: they are stratified by the SPY proxy only and are flagged.
  - Primary tape stratum for all nights, trailing and therefore legal at 16:05 ET:
    `tape_t` = sign of SPY's trailing 20-session return × tercile of SPY's trailing 20-session
    realized volatility, from `prices_daily_split`. Cells < 20 nights SUPPRESSED.
  - The report describes the tape in words from SPY's path; it never implies a regime label existed
    before 06-09.
- **Catalyst-layer regime change:** the catalyst layer is a different feature before and after
  2026-06-01 (`exclusions_v001.json.catalyst_layer_regime_change`, platform commit 69ef05f). The
  test window sits entirely after the fix, which is a second reason the window choice is clean.
- **Knowledge time (rule 14):** matching and stratification features come only from bars dated ≤ the
  pick night or from 16:05-ET `sas_candidates` fields. `uoa_symbol_daily.fwd_return_*` is banned
  (degraded, DATA_NOTES). `sas_excursion` is an outcome table with a variable recomputation lag
  (manifest_v001 `availability.sas_excursion`) and is never a feature.

## 7. Multiple testing

- **Within the question:** 3 primary endpoints (S1, S2, S3). Benjamini–Hochberg across the 3; the
  verdict uses q. Secondaries print raw p and are marked "descriptive, does not decide".
- **Across the family:** F7 holds H-053…H-060, H-065, H-066 (10 hypotheses); registered questions in
  F7 at registration: **Q002 (H-065)** and **Q004 (H-054 + H-057)**. The Reporter applies BH across
  all primary endpoints of registered-and-run F7 questions and prints both the within-question and
  within-family q.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`s1, s2, s3` = the three night-averaged deltas, in percentage points of touch rate.
**MPE = +5.0 percentage points** on each endpoint (**placeholder — Haci to confirm at lock**).
Rationale for a per-endpoint MPE rather than a pooled one: each endpoint maps to a different
trading decision (L1/L2 = quick-exit and near-strike choice; L3 = DTE choice).

- **HISTORICALLY_CONFIRMED** (per endpoint) requires **all** of:
  1. eligible nights ≥ 80, with ≥ 30 of them post-lock (prospective) nights;
  2. `s > +5.0 pp`;
  3. bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question;
  5. point estimate > 0 in **both halves** (§6) and neither half below −5.0 pp;
  6. no tape stratum with ≥ 20 nights below −5.0 pp.
- **NULL** (per endpoint): eligible nights ≥ 80 **and** 95% CI includes 0 **and** |s| < 5.0 pp.
  A NULL here kills the "speed is the differentiator" claim; it is ledgered with the same care as a
  positive and the platform stops implying it.
- **INCONCLUSIVE** (per endpoint): n below floor, halves disagreeing in sign, or `0 < s ≤ 5.0 pp`.
- **Question-level:** CONFIRMED if **≥ 2 of the 3** endpoints are CONFIRMED and none is
  NULL-with-negative-sign; if exactly one confirms, the question is CONFIRMED **for that level only**
  and the report must say so in the first sentence.
- **Speed-vs-reach adjudication (pre-specified, so nobody argues after the fact):** if an endpoint
  confirms at the short cut while B3 (the same level at its full lane window) shows a delta below
  MPE, the finding is labelled **"speed, not reach"**. If both clear MPE, it is labelled
  **"reach, partly front-loaded"** and Q006 E1 owns the reach claim.
- **PROSPECTIVELY_CONFIRMED:** only after ≥ 30 post-lock nights reproduce the sign with `s > 0`
  under the unmodified `eval.py`. Because clause 1 already requires 30 post-lock nights, a
  CONFIRMED verdict here may be promoted directly — but only if those nights are frozen in a
  successor manifest and were never inspected before the decision date.

## 9. If CONFIRMED, what changes on the platform

- **Options context:** replace the flat 21–35 DTE suggestion with a DTE band derived from the
  target's ATR distance and the measured time-to-touch, per level. Brief against the options-context
  service; ship flag-off with a byte-identical checksum, shadow ≥ 20 trading days (rule 11).
- **Conviction card:** add a "typical sessions to first touch" figure beside each level's hit rate,
  with the matched-control figure next to it.
- **Manual Trading Guide / playbook:** a line stating that near targets resolve in days, so
  near-dated structures and quick exits are the intended use of L1/L2 (this is the H-066 lane; it is
  not registered here).
- **If NULL:** the platform must stop implying a speed advantage, and the DTE guidance stays flat
  until a different mechanism is found.

## 10. Known threats to validity (registrar's own list)

1. **Short windows are the most tape-sensitive metric on the desk.** A trending stretch front-loads
   every stock's move. Mitigation: the matched control is same-night, so the tape is differenced
   out at the night level; tape strata are reported.
2. **`passed_at_entry` interacts with the endpoint.** A pick that gaps through L1 at the open counts
   as a non-hit under §4, which *lowers* measured speed at L1 exactly when the pick worked best.
   This is deliberate (a target you cannot buy is not a target), but it means S1 understates value
   on gap nights; Q004 measures that share directly and the two reports must be read together.
3. **Matching on 3 features may not span selection.** Post-match standardized mean differences are
   printed; B2 is reported alongside.
4. **Overlapping short windows** across adjacent nights — block bootstrap, block length fixed here.
5. **Elite is thin and shrinking** (DATA_NOTES; 90+ per month 12 / 8 / 3 / 2 since June). The elite
   cell is SUPPRESSED below 20 nights by §5 rather than reported small, precisely because Haci will
   otherwise anchor on it. Why elite is thinning is Q005.
6. **Level placement is not ATR-scaled** (volatilx `ai_agents/principal_agent.py:530-575`), so a
   "fast L1" may simply be a close L1. Mitigation: the ATR-distance tercile cell, and the control
   inheriting the identical ATR distance.
7. **Prospective nights depend on the Steward re-freezing with the identical exclusion criterion.**
   If any post-lock night is a manual re-run, it must be excluded by the same rule, not by judgment.
8. **The sealed night count is itself disputed** (71 raw − 1 exclusion = 70, but the round-1 brief
   and EXPLORE_001 both quote 66). `eval.py` must print the derivation of its own night count from
   `sas_runs` and `exclusions_v001.json` so the floor test is auditable.
9. **Deferred adjacent:** the DTE recommendation that a CONFIRMED S3 would imply cannot be *priced*
   without option data (H-056's second half). See `research/questions/DEFERRED.md`.
