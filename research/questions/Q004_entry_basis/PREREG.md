# Q004 — entry_basis: does it matter whether you buy the pick after hours, at the open, or at 10:00?

**Status:** DRAFT (lock by committing this file after Haci review)
**Family:** F7 Path, entry timing & volatility (hypotheses H-054 and H-057)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — plus the successor freezes named in §5.
**Exclusions:** research/data/exclusions_v001.json (`manual_runs.trading_dates`, 5 nights)
**Registered by:** registrar · **Approved by:** haci · **Date:** 2026-09-10

---

## 1. Hypothesis (plain English)

**Where you get in decides what the pick is worth: buying in the after-hours session when SAS
publishes beats waiting for the next open or for 10:00 ET — the later you buy, the more of the first
target is already gone, and the worse your odds of reaching the third target before the trade goes a
full ATR against you.**

Two parts, both pre-registered:
(a) **mechanical, descriptive** — the share of picks whose L1 (and L2, L3) is already passed at each
entry rises from the after-hours price to the open to 10:00 ET;
(b) **primary** — the rate at which the pick touches **L3 before it falls 1 ATR below the entry**
differs by entry basis, with the after-hours entry at least as good as the next open.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first;
  the estimator is a per-night **paired** difference between entry bases on the *same picks*.
- Source tables (manifest_v001): `sas_candidates` (published picks + full universe, lane plans,
  `selected_rank`, `overall_score`, `dominant_direction`, `context_json`), **`sas_runs.finished_at`
  — load-bearing here**: it defines the after-hours entry moment.
- Source tables (manifest_prices_v001): `prices_hourly_raw` (UTC stamps, includes pre/post-market —
  the after-hours and 10:00 ET entries), `prices_daily_split` (paths, ATR14, beta60, run-up, opens),
  `prices_daily_raw` (split-factor snapping; the hourly feed is **raw**, so hourly prices must be
  converted to the signal-date split basis before any comparison).
- **Treatment rows:** every published pick on a non-excluded night in the §6 test window with a
  lane-plan ladder.
- **Three entry bases, defined exactly:**
  - **E_AH — after-hours at publication:** the **close of the first hourly bar in
    `prices_hourly_raw` whose bar end is at or after that night's `sas_runs.finished_at`**, for that
    symbol, on the pick night or the following pre-market, and strictly before the next regular
    open. Publication time is a deliberate trading decision and varies (DATA_NOTES "Publication time
    is deliberately early"): **no fixed 21:05 UTC assumption is permitted anywhere in `eval.py`.**
    If no such bar exists (thin after-hours), the pick has **no E_AH price** and is excluded from
    E_AH cells only (counted).
  - **E_OPEN — next-session open:** the session t+1 open.
  - **E_10 — next session 10:00 ET:** the close of the 14:00 UTC hourly bar on session t+1 (i.e. the
    bar covering 09:00–10:00 ET), matching EXPLORE_001's convention.
- Exclusions (counted, printed, never silent): the 5 manual-run nights from `exclusions_v001.json`
  — these are the nights where `finished_at` post-dates the next open, so an "after-hours entry" is
  not even definable; picks without a lane-plan ladder; picks whose L3 is on the wrong side of the
  **actual** pick-night close; nights whose 20-session window has not matured in the pinned freeze
  (**excluded, not graded as a loss**); missing-bar symbols.
  - **Night-level E_AH coverage rule (pre-specified):** a night enters the E_AH cells only if
    **≥ 50% of its eligible picks have an E_AH price**; otherwise the night is excluded from E_AH
    comparisons and counted. E_OPEN and E_10 cells keep all eligible nights. Every E_AH-vs-E_OPEN
    contrast is computed on the **common subset of picks that have all three entry prices**, so the
    comparison is paired and not a composition artefact.
- ATR = ATR14 from `prices_daily_split` through the pick night, converted to the signal-date basis.
  Reference price for level distances = the **actual** pick-night close, never `spot_close`.
- Levels/windows: the platform's own (volatilx `services/sas_conviction_card.py:182-195`).

## 3. Baseline(s) — what this must beat

- **B1 (primary baseline): the next-session-open entry, on the same picks, same nights.** E_OPEN is
  the reference basis because it is what a subscriber without after-hours access can do.
- **B2 (the platform's published basis, descriptive):** the close basis the platform actually grades
  on — `entry_ref` resolves to `technical_snapshot.spot_close` first (volatilx
  `services/sas_excursion.py:336-354`). Part (a) exists to quantify the gap between that basis and
  anything a subscriber can trade; it is mechanical and does not need a control.
- **B3 (distance-matched control, descriptive, for absolute framing):** the Q006 §3 construction —
  10 nearest same-night unpublished candidates on `beta60` / `atr_pct` / `runup20`, synthetic target
  at the same ATR distance and direction, graded on the **same entry basis** and the same −1 ATR
  race rule. Control rows never add to inferential n (rule 6).
- **B4 (elite vs non-elite, the H-057 leg):** non-elite picks are the baseline for the elite claim,
  under the suppression rule in §5.

## 4. Objective metric (amended rule 5 — price path)

For every (pick, entry basis) pair, all prices in the signal-date split basis:

- **Race outcome (the primary object).** Starting from the entry price `X`, over the next **20
  trading sessions**, which happens first:
  - **WIN:** the regular-session high (bullish) / low (bearish) touches **L3**; or
  - **LOSS:** the regular-session low (bullish) / high (bearish) touches `X − dir × 1.0 × ATR`.
  If neither occurs within 20 sessions → **NEITHER** (counted, and scored as a non-WIN in the rate).
  Same-session ties are broken with `prices_hourly_raw`; if the hourly bars cannot separate them the
  pair is recorded as **TIE** and scored as a non-WIN (conservative, pre-specified).
  **A level already at or through `X` at the entry is not a hit** — such a pick is scored
  `passed_at_entry` and, for L3 specifically, is **excluded from the race denominator** and counted.
  Stops are not assumed anywhere else in this question (rule 5): the −1 ATR line is a *measurement
  of which came first*, not an exit.

**Primary endpoints (two contrasts, pre-specified, BH-corrected within this question):**

- **T1 — after-hours vs open:** per night t, `A_t = raceWIN%_{E_AH} − raceWIN%_{E_OPEN}` on the
  common pick subset; estimand `mean_t(A_t)`.
- **T2 — 10:00 vs open:** per night t, `B_t = raceWIN%_{E_10} − raceWIN%_{E_OPEN}`; estimand
  `mean_t(B_t)`.

**Descriptive endpoint (part (a)) — mechanical, reported with CIs but never decides a verdict:**
the share of picks with L1 / L2 / L3 already passed at E_AH, E_OPEN, E_10, and at the platform's
close basis (B2), night-averaged; plus the median entry price drift from the pick-night close to each
entry in ATR units, direction-adjusted.

**Secondary, descriptive, never decides:** race outcome split into WIN / LOSS / NEITHER / TIE;
unconditional L3-within-5-sessions by entry basis; L1 and L2 touch rates by entry basis on their
20-session window; the matched control's race rate per basis (B3); the same table for elite vs
non-elite (B4, subject to §5 suppression); drawdown from entry before the first L1 touch;
`finished_at` distribution by month (how early Haci is pulling the job forward); close-to-close
T+5 / T+20 return from each entry (secondary by rule 5).

**Quotability:** 20-session basis → **NON_QUOTABLE** (rule 12).

**Inference.** Night-level, paired across entry bases. CI: date-clustered bootstrap over nights
(2,000 resamples) plus a stationary block bootstrap with expected block length 10 sessions
(overlapping 20-session windows). p: paired sign-flip permutation on the night contrasts, 10,000
permutations. Every estimate prints n(nights), n(picks), n(picks with all three entry prices),
n(nights dropped by the E_AH coverage rule).

## 5. Sample floors and expected n

- Floors (rule 6): **≥ 20 nights per reported cell, ≥ 80 nights total.** Cells below 20 nights are
  **SUPPRESSED** — no point estimate printed.
- **Elite (90+) cell (the H-057 leg):** reported **only if** ≥ 20 eligible nights carry ≥ 1 elite
  pick **with an E_AH price**; otherwise SUPPRESSED with the reason and the night count, and the
  H-057 elite claim is recorded as INCONCLUSIVE by construction. DATA_NOTES gives 12 / 8 / 3 / 2
  elite picks per month since June, so suppression is the expected outcome.
- The binding maturity is the race window: a night is eligible once **20 sessions** have passed.
- **Expected n today (2026-09-10), test window = sealed only (§6):** sealed nights with a matured
  20-session window are those ≤ **2026-08-12** → ≈ **51** nights, before the E_AH coverage rule
  (which will cost a further handful of nights for the E_AH contrast; EXPLORE_001 §9 notes thin
  after-hours prints on late-publishing nights). **Below the 80-night floor today.**
- **Floor date.** ≈ 21 trading nights/month ⇒ the 80th eligible sealed night is a pick night around
  **2026-09-24**; its 20-session window matures around **2026-10-22**.
- **Decision date: 2026-10-26.** Locked now, evaluated **once**, then. **No interim looks** (rule 9).
  Note: the descriptive part (a) would clear its floor today, but it is **not** evaluated early —
  looking at the same picks' entry prices before the primary is exactly the contamination this
  process prevents. Both parts run in the same single pass.
- **Freeze discipline:** nights ≤ 2026-09-10 pinned to `manifest_v001`; prospective nights enter via
  successor selection and price freezes (same SQL, same symbol list, same exclusion criterion,
  hourly bars included for published symbols). `eval.py` records all sha256s and prints sealed vs
  post-lock counts separately. **If the successor price freeze omits pre/post-market hourly bars for
  any prospective symbol, those nights are excluded from E_AH and counted — never back-filled from
  a daily bar.**
- Sub-cells (bull/bear, score band, tape stratum) reported only where they clear 20 nights.

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-06-01**, plus every night after this
  file's lock commit, through the decision date.
  *Justification (one sentence):* the entry-time comparison, its three bases and the
  L3-before-(−1 ATR) race are the exact constructions EXPLORE_001 §B/§E ran and reported on
  April–May, so under the contamination rule the test must use data the Explorer never saw.
- **Split for the "holds in both halves" test:** within the window — Half A = eligible nights on or
  before the median eligible-night date; Half B = after. `in_sample_end = 2026-05-29` (both
  manifests) marks only what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` is legal only from **2026-06-09**, `regime_version = 'v1.2'`
    (manifest_v001 `availability.market_regime`); nights 06-01..06-08 carry no legal label and use
    the SPY proxy only, flagged.
  - Primary tape stratum, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's trailing
    20-session return × tercile of SPY's trailing 20-session realized volatility, from
    `prices_daily_split`. Cells < 20 nights SUPPRESSED.
  - **Gap stratum (pre-specified, because it is the mechanism):** nights are also reported split by
    the night's median direction-adjusted open gap (≤ −0.25 ATR / flat / ≥ +0.25 ATR). This is
    descriptive; it does not gate the verdict (the gap threshold is itself an EXPLORE_001 figure).
- **Catalyst-layer regime change:** the window sits entirely after the 2026-06-01 fix
  (`exclusions_v001.json.catalyst_layer_regime_change`, commit 69ef05f).
- **Knowledge time (rule 14):** `finished_at` is a 16:05-ET-or-later *publication* timestamp used as
  the entry clock, not as a feature; nothing here uses a post-entry column.
  `uoa_symbol_daily.fwd_return_*` is banned (degraded). `sas_excursion` is outcome-only with a
  variable recomputation lag and appears only as the descriptive B2 basis citation.

## 7. Multiple testing

- **Within the question:** 2 primary contrasts (T1, T2); BH across the 2; the verdict uses q. The
  descriptive part (a) and all secondaries print raw p only, marked "descriptive, does not decide".
- **Across the family:** F7 holds H-053…H-060, H-065, H-066 (10 hypotheses); registered F7 questions
  at registration: **Q002 (H-065)** and **Q004 (H-054 + H-057)**. The Reporter applies BH across all
  primary endpoints of registered-and-run F7 questions — note that Q002 and Q004 together contribute
  5 primaries to that family correction.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`a = mean_t(A_t)` (after-hours minus open), `b = mean_t(B_t)` (10:00 minus open), in percentage
points of race-win rate. **MPE = +5.0 percentage points** (**placeholder — Haci to confirm at lock**).

- **T1 — after-hours entry.**
  - **HISTORICALLY_CONFIRMED ("after-hours is better"):** eligible nights ≥ 80 with ≥ 30 post-lock;
    `a > +5.0 pp`; bootstrap 95% CI excludes 0; BH q ≤ 0.10; `a > 0` in both halves with neither
    half below −5.0 pp; no tape stratum (≥ 20 nights) below −5.0 pp.
  - **CONFIRMED-EQUIVALENT ("after-hours is not worse", the weaker H-057 claim):** the two-sided
    95% CI on `a` lies **entirely above −5.0 pp**. This is a pre-registered equivalence test, not a
    consolation prize: it is the claim that licenses Haci's existing practice without asserting an
    edge, and it is reported as its own labelled verdict.
  - **NULL:** n ≥ 80 and CI includes 0 and `|a| < 5.0 pp` — entry timing between after-hours and the
    open does not change the race.
  - **INCONCLUSIVE:** n below floor (including via the E_AH coverage rule), halves disagreeing in
    sign, or `0 < a ≤ 5.0 pp`.
- **T2 — 10:00 entry.** Same structure. The pre-registered expectation to be tested is that `b` is
  **negative** (later entry is worse); a CONFIRMED negative requires `b < −5.0 pp` with CI excluding
  0, q ≤ 0.10, and sign agreement in both halves.
- **Part (a), descriptive:** no verdict. It is reported as a table with CIs and the single sentence
  it licenses ("the platform's published L1 hit rate is measured on a price you cannot trade; on an
  actionable basis it is X points lower"), where X is whatever the run produces.
- **Question-level:** the question is CONFIRMED if **either** T1 or T2 reaches a CONFIRMED verdict;
  each contrast keeps its own label in the LEDGER.
- **PROSPECTIVELY_CONFIRMED:** only after ≥ 30 post-lock nights reproduce the sign under the
  unmodified `eval.py`, on data frozen after the lock and never inspected earlier. Any
  subscriber-facing statement about entry timing requires this **and** a W60 restatement (rule 12).

## 9. If CONFIRMED, what changes on the platform

- **Part (a), whatever it shows, changes the performance surface:** hit rates get published on an
  **actionable** basis (next open) alongside the close basis, with the "already passed at entry"
  share shown. That is a correctness fix, not an edge claim, and it is the highest-value output of
  this question. Brief against `services/sas_excursion.py` (`entry_ref`, `:336-354`) and the
  conviction-card surface.
- **T1 CONFIRMED or CONFIRMED-EQUIVALENT:** the pick card carries an entry-timing note keyed to that
  night's actual `finished_at` ("published at HH:MM ET; after-hours entry available"), and the
  Manual Trading Guide records the after-hours fill as the default for elite nights **only if** the
  elite cell cleared its floor.
- **T2 CONFIRMED negative:** a guide line — "if you did not get filled by the open, the first hour is
  not a free option; the near targets are frequently gone" — plus a flag on the card when L1 sits
  inside the typical overnight-gap-plus-first-hour range.
- Owner: implementer. Ship flag-off with a byte-identical checksum on the old path; shadow ≥ 20
  trading days (rule 11).
- **If NULL:** entry-timing guidance is dropped from the roadmap and the effort moves to exits (F6).

## 10. Known threats to validity (registrar's own list)

1. **After-hours prices are not fills.** An hourly after-hours bar close can be untradeable size at a
   wide spread. The stock path is a proxy; the report must say that every E_AH number assumes a fill
   at a printed price. This is the single largest threat and it cannot be removed with the data the
   desk holds.
2. **E_AH availability is not random.** Picks with no after-hours print are plausibly the quieter
   names; the coverage rule and the common-subset pairing limit, but do not eliminate, that
   selection. n(picks without an E_AH price) is a headline number.
3. **Publication time drifts by design** (DATA_NOTES): Haci pulls the job forward deliberately, so
   `finished_at` is itself a decision that may correlate with the night's quality. The report prints
   the `finished_at` distribution by month and by tape stratum; a large drift makes T1 partly a
   comparison of nights rather than of entries.
4. **Hourly bars are raw, daily paths are split-adjusted.** Mixing the two without snapping the split
   factor would silently corrupt every E_AH and E_10 comparison. `eval.py` must assert basis
   agreement per symbol-date and fail loudly.
5. **The −1 ATR line is a measurement, not a stop** (rule 5). The race rate must never be presented
   as the return of a stopped strategy.
6. **TIE and NEITHER are scored as non-WIN**, which biases every basis in the same direction but not
   necessarily by the same amount (a faster entry has more time to resolve). Counts are printed
   separately so the asymmetry is visible.
7. **Elite is thin and shrinking** (DATA_NOTES); the H-057 elite leg is expected to be SUPPRESSED and
   must not be reported as a small-n direction.
8. **Manual-run nights are exactly the nights where this question is undefined** — they are excluded
   by the shared exclusions file, and any prospective night with the same pathology must be excluded
   by the same rule, not by judgment.
9. **Deferred adjacent:** the option-structure consequences of an entry-timing result (which DTE,
   which strike, H-055/H-056) need option prices the desk does not have. See
   `research/questions/DEFERRED.md`.
