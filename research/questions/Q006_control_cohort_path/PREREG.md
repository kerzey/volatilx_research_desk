# Q006 — control_cohort_path: does SAS selection beat a distance-matched control from its own universe, on the price path?

**Status:** DRAFT (lock by committing this file after Haci review)
**Family:** F1 Selection edge
**Supersedes:** Q001_control_cohort (same charter question, old rule-5 objective).
**Registrar's note on why this is Q006 and not a rewrite of Q001:** the round-1 instruction was to
overwrite `research/questions/Q001_control_cohort/PREREG.md` "because it is not committed". It **is**
committed (commit `bbed9aa`, "research desk v3"), and `guard_write` blocked the overwrite:
*"is committed and therefore locked; register a new question instead."* Enforcement code is policy
(rule 15), so the rewrite is registered here as a new question. Haci should retire Q001 through
`research/lib/controller.py` (a superseded/closed transition), not by editing the locked file.
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor price freeze named in §5 for nights that mature after 2026-09-10.
**Exclusions:** research/data/exclusions_v001.json (`manual_runs.trading_dates`, 5 nights)
**Registered by:** registrar · **Approved by:** haci · **Date:** 2026-09-10

---

## 1. Hypothesis (plain English)

**When SAS publishes a pick, the stock actually reaches the pick's own target more often — and
sooner — than near-identical stocks that SAS looked at the same night and did not publish.**

Formally: for a published pick and for same-night unpublished candidates matched on beta,
volatility and recent run-up, with a synthetic target placed at the **same ATR distance in the same
direction**, the pick's first-touch rate of L3 within 40 trading sessions, and within 5 trading
sessions, exceed the matched control's.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first.
- Source tables (manifest_v001): `sas_candidates` (published picks and the full candidate universe:
  `public_payload_json` lane plans, `selected_rank`, `overall_score`, `dominant_direction`,
  `best_timeframe`, `context_json`), `sas_runs` (`finished_at`, `config_json`).
- Source tables (manifest_prices_v001): `prices_daily_split` (all path metrics, ATR, beta60,
  run-up), `prices_daily_raw` (split-factor snapping only: raw/split on a date = cumulative split
  factor), `prices_hourly_raw` (same-day touch tie-breaks only).
- **Treatment rows:** every published pick (`selected_rank` not null) on a non-excluded night,
  2026-04-01 .. 2026-09-10, that has a lane-plan ladder in `public_payload_json`.
- **Control pool, night t:** every `sas_candidates` row on night t that is **not** published, has
  ≥ 60 prior split-adjusted daily bars (beta60) and ≥ 21 bars (run-up), and has forward bars
  covering the endpoint's window.
- Exclusions — each counted and printed in the results header, never silently dropped:
  - the 5 manual-run nights in `exclusions_v001.json` (`2026-05-11..05-14`, `2026-07-06`) →
    **excluded**: `finished_at` later than the next session's open, mixed-date `spot_close`, never
    actionable (DATA_NOTES "Manual / late SAS runs"). `eval.py` reads the JSON, no hard-coded dates.
  - picks with no lane-plan ladder (the null-ladder denominator, 16 known) → excluded from the
    levels they lack; the night survives if ≥ 1 pick remains.
  - picks whose L3 is already on the wrong side of the **actual** pick-night close ("hit at
    publication") → excluded as invalid targets, counted separately.
  - nights whose endpoint window has not matured in the pinned price freeze → **excluded and
    counted**; right-censoring is never graded as a non-touch.
  - delisted / missing-bar symbols → dropped and counted; a night is dropped if > 25% of its picks
    are missing bars.
- **Reference price is the actual pick-night close from `prices_daily_split`**, never the platform's
  `spot_close`. ATR = ATR14 computed from `prices_daily_split` up to and including the pick night,
  converted to the signal-date basis (the platform's `atr_pct` is corrupted around splits —
  DATA_NOTES, EXPLORE_001 §9).
- Levels and windows are the platform's own: L1..L6 from the lane plans; windows L1/L2 = 20,
  L3/L4 = 40, L5/L6 = 60 trading sessions; **first touch**
  (volatilx `services/sas_conviction_card.py:182-195`, `_LADDER_LEVEL_WINDOW` at `:194`).

## 3. Baseline — what this must beat

**B1 (primary, distance-matched control).** Fixed here; identical to the object EXPLORE_001 used
(its conventions block), and specified by Haci **before** the exploration ran:

1. For each pick p on night t compute, at the pick-night close, from `prices_daily_split`:
   `beta60` = OLS slope of daily returns on SPY daily returns over the trailing 60 sessions;
   `atr_pct` = ATR14 / close; `runup20` = 20-session total return.
2. Standardize each feature by the **night's** cross-sectional median and MAD; take the **10
   nearest** control-pool candidates by Euclidean distance. Matching is with replacement across
   picks within a night. Ties broken by symbol ascending (deterministic).
3. Synthetic target for control c matched to pick p at level L:
   `target_c = close_c × (1 + dir_p × d_{p,L} × atr_pct_c)` with
   `d_{p,L} = |level_price_{p,L} − close_p| / ATR_p`, `dir_p` = the pick's `dominant_direction`.
   Same ATR distance, same direction.
4. The control is graded with **exactly** the pick's rule: same entry basis, same window, same
   "already passed at entry is not a hit" rule, regular-session daily high (bullish) / low
   (bearish), split factors snapped.
5. Control rows are a baseline, **not sample size**: they never add to inferential n (rule 6).

**B2 (secondary, descriptive).** All same-night unpublished candidates, unmatched, same synthetic
target rule — shows how much of any raw gap is beta/run-up composition rather than selection.

## 4. Objective metric (amended rule 5 — price path)

**Entry basis: the next session's open** (session t+1 open, `prices_daily_split`), for picks and
controls alike. A level at or through the entry price at the open is **not a hit**; it is recorded
as `passed_at_entry`. The platform's close basis (`entry_ref`, volatilx
`services/sas_excursion.py:336-354`) is reported only as a descriptive comparator.

**Primary endpoints (two, pre-specified, BH-corrected within this question):**

- **E1 — reach:** first touch of L3 within **40** trading sessions.
  `Delta1_t = mean_p[touch_{p,L3,40}] − mean_{p,c}[touch_{c,L3,40}]`; estimand `mean_t(Delta1_t)`.
- **E2 — unconditional speed:** first touch of L3 within **5** trading sessions, same construction;
  estimand `mean_t(Delta2_t)`. *Unconditional* = all picks in the denominator. This is deliberately
  **not** days-to-touch among touchers, which is survivor-biased.

**Secondary, descriptive, never decides:** L1, L2, L4, L5, L6 on their own windows; counter-direction
level touches (counter levels mirrored onto the control at the same ATR distance); days-to-first-
touch distributions (median, p75) among touchers; touch-then-settle (still through L3 at session
20/40); order of level hits; the platform close-basis rates; close-to-close return at T+10/T+20
(secondary by rule 5).

**Quotability:** 5- and 40-session windows → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** Night-level. CI: date-clustered bootstrap over nights, 2,000 resamples; for E1 a
stationary block bootstrap with expected block length 20 sessions (E2: 3), because forward windows
overlap across adjacent nights. p-value: paired sign-flip permutation on `Delta_t`, 10,000
permutations. Every estimate prints n(nights), n(picks), n(control rows).

## 5. Sample floors and expected n

- Floors (rule 6, which overrides the template's 100): **≥ 20 nights per reported cell, ≥ 80 nights
  total.** Cells below 20 nights are **SUPPRESSED** — no point estimate printed.
- Eligible night = non-excluded pick night whose endpoint window has matured in the pinned price
  freeze. Maturity at 2026-09-10: 20-session ≤ 2026-08-12; 40-session ≤ 2026-07-14;
  60-session ≤ 2026-06-15.
- Expected n today (2026-09-10):
  - **E2 (5 sessions):** ≈ **103** of 108 nights → floor already cleared.
  - **E1 (40 sessions):** ≈ **68** nights (2026-04-01..2026-07-14 less the manual-run nights) →
    **below the 80-night floor today.**
- **Floor date for E1:** at ≈ 21 trading nights/month the 80th non-excluded night is a pick night
  around **2026-07-30**, whose 40-session window matures around **2026-09-28**.
- **Decision date: 2026-10-05.** Locked now, evaluated **once**, then. **No interim looks** at
  either endpoint; `eval.py` is written once and run once (rule 9).
- **Freeze discipline at evaluation.** Selections stay pinned to `manifest_v001` — the SAS tables
  are not re-pulled and the night set stays 2026-04-01..2026-09-10. Only forward **price** bars are
  extended, via a successor freeze `manifest_prices_v002` (same Alpaca queries, same symbol list,
  `end` moved to the decision date); `eval.py` records its sha256s. Pick nights after 2026-09-10 do
  **not** enter Q006; they are the prospective stage in §8.
- Cells: bull / bear; score band (< 80 / 80–85 / 85–90 / 90+); tape stratum (§6). The 90+ cell is
  expected to fail the 20-night floor and to be SUPPRESSED (DATA_NOTES: 8/13/12/8/3/2 elite picks
  per month, on far fewer than 20 nights per stratum).

## 6. Test window, split and stratification

- **Test window: all 108 non-excluded nights (2026-04-01 .. 2026-09-10), in-sample included.**
  *Justification (one sentence):* both load-bearing choices predate EXPLORE_001 — the path objective
  and the distance-matched control come from the rule 5 amendment (Haci's trading practice), and
  "does SAS selection beat its own universe" is Q001's original charter question — while L3 is the
  strike Haci actually sells and 40 sessions is the platform's own lane ruling
  (`sas_conviction_card.py:194`), not an explored threshold.
  *Residual contamination, stated honestly:* the **"within 5 sessions" cut in E2 is the same figure
  that appears in EXPLORE_001 §E**, so E2's April–May half is exploratory-adjacent. §8 therefore
  requires E2 to hold in the sealed half on its own, and the report must print E2 restricted to
  sealed nights as a pre-specified robustness cell.
- **Calendar split:** in-sample ≤ **2026-05-29** (`in_sample_end`, both manifests); sealed ≥
  2026-06-01. Both halves reported for every endpoint.
- **Regime / tape stratification (rule 7, adapted):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (all v1/v1.1/v1.2 rows
    for 2026-01-02..2026-06-08 were backfilled 06-02/06-08; manifest_v001
    `availability.market_regime`). It is a stratifier **only for nights ≥ 2026-06-09**, and only
    `regime_version = 'v1.2'`.
  - Primary tape stratum for the whole sample, from SPY in `prices_daily_split`, trailing and
    therefore knowledge-time legal at 16:05 ET: `tape_t` = sign of SPY's trailing 20-session return
    × tercile of SPY's trailing 20-session realized volatility; terciles cut on the full pick-night
    sample. Cells < 20 nights SUPPRESSED.
  - The report describes the April–May tape **in words, from SPY's path**, and never implies a
    regime label existed then.
- **Knowledge time (rule 14):** matching and stratification features come only from bars dated ≤ the
  pick night or from `sas_candidates` fields written at 16:05 ET. No outcome column (`outcome_*`,
  `sas_excursion.*`) is ever an input; `uoa_symbol_daily.fwd_return_*` is banned outright
  (degraded — DATA_NOTES, FREEZE_v001 §5).

## 7. Multiple testing

- **Within the question:** 2 primary endpoints (E1, E2); Benjamini–Hochberg across those 2; the
  verdict uses q. Secondaries print raw p only, marked "descriptive, does not decide".
- **Across the family:** F1 Selection edge contains H-001 (Q001, superseded by this question),
  H-002, H-003, H-062 — 1 registered question at registration. The Reporter applies BH across all
  *primary* endpoints of registered-and-run F1 questions and prints both q's.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1 = mean_t(Delta1_t)`, `m2 = mean_t(Delta2_t)`, in percentage points of touch rate.
**MPE = +5.0 percentage points** for both endpoints (**placeholder — Haci to confirm at lock**;
any change must be committed before the decision date).

- **HISTORICALLY_CONFIRMED** (per endpoint) requires **all** of:
  1. eligible nights ≥ 80, with ≥ 40 in the sealed half;
  2. `m > +5.0 pp`;
  3. bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question;
  5. point estimate **> 0 in both calendar halves**, neither half below −5.0 pp;
  6. no tape stratum with ≥ 20 nights below −5.0 pp.
  E2 additionally: the **sealed-half-only** estimate > 0 (contamination guard, §6).
- **NULL** (per endpoint): eligible nights ≥ 80 **and** full-sample 95% CI includes 0 **and**
  |m| < 5.0 pp. "Picks touch L3 no more often / no faster than matched controls" is a real finding
  and is ledgered with the same care as a positive.
- **INCONCLUSIVE** (per endpoint): anything else — n below floor, halves disagreeing in sign, or
  `0 < m ≤ 5.0 pp` ("positive but below MPE" is INCONCLUSIVE, rule 6).
- **Question-level:** the stronger endpoint does not carry the question. CONFIRMED only if at least
  one endpoint is CONFIRMED **and** the other is not NULL-with-opposite-sign; otherwise report both
  verdicts and mark the question INCONCLUSIVE.
- **PROSPECTIVELY_CONFIRMED:** only after ≥ 30 pick nights occurring **after this file's lock
  commit**, frozen separately, reproduce the sign with `m > 0` under the unmodified `eval.py`. No
  subscriber-facing claim before that (rule 10); even then the basis is NON_QUOTABLE (rule 12).

## 9. If CONFIRMED, what changes on the platform

- **E1 confirms →** the conviction card's ladder hit rates gain a second row, "matched-control rate
  at the same ATR distance", so a bare L-level hit rate is never shown again. Brief against
  `services/sas_conviction_card.py`.
- **E2 confirms (speed) →** the options context stops recommending a flat 21–35 DTE and maps the
  target's ATR distance to a DTE band; a "typical days to target" line enters the Manual Trading
  Guide. Q002 is the dedicated test of that lane.
- **E1 NULL, E2 CONFIRMED →** the product line changes from "we pick winners" to "we pick names that
  get there sooner", which is a different and more defensible claim.
- **Both NULL →** F1 selection-edge work is de-prioritized, effort moves to F3 (new information) and
  F6 (execution), and the performance surface stops implying selection alpha.
- Owner: implementer. Shadow ≥ 20 trading days, flag-off with a byte-identical checksum on the old
  path before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **Three matching features may not span what selection sees.** Picks are structurally higher-beta
   and more extended than the pool; incomplete matching leaves composition, not skill. Mitigation:
   B2 is reported alongside, and post-match standardized mean differences per feature are printed.
2. **Overlapping forward windows** inflate precision; block bootstrap with a block length fixed
   here, not chosen after seeing results.
3. **One tape per half** (rule 7): a sign that appears in only one half fails §8 clause 5.
4. **No point-in-time regime before 2026-06-09** — handled by the SPY tape proxy (§6).
5. **Ladder placement is not ATR-scaled** (volatilx `ai_agents/principal_agent.py:530-575`, fallback
   0.5%/1% steps at `:897-911`), so L3's ATR distance varies by pick. The control inherits the same
   distance — that is the design — but if distance itself correlates with pick quality, E1 mixes
   selection with target placement. Mitigation: E1 within terciles of L3's ATR distance, descriptive.
6. **Null-ladder denominator** and wrong-side L1/L3 ladders: excluded and counted; the exclusion
   count is a headline number in the report, not a footnote.
7. **`sas_excursion` uses calendar windows, not session windows** (volatilx
   `services/sas_excursion.py:8-18`); its hit dates are never joined to this ladder as equivalent.
8. **Contamination residue in E2's 5-session threshold** (§6), guarded in §8.
9. **Elite (90+) is thin and shrinking** (DATA_NOTES); elite cells here are SUPPRESSED rather than
   reported small. Why it is thinning is Q005.
10. **Deferred adjacents.** H-055 (leg out at the L3 touch) and H-056's DTE recommendation cannot be
    settled here — the stock path is only a proxy for option P&L and the desk holds no option price
    history. See `research/questions/DEFERRED.md`.
