# Q009 — stop_whipsaw: does the stop printed on a SAS pick shake traders out of trades that would have reached the target anyway?

**Status:** DRAFT (lock by committing this file after Haci review; see "Decisions before lock" at the end)
**Family:** F6 Exits and execution (hypothesis H-032, re-filed from F4 under DP-29 — §7)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates. See §2.
**Registered by:** registrar · **Approved by:** haci (pending lock) · **Date:** 2026-09-12 (decisions applied 2026-09-13)
**Decisions:** DECISIONS.md
**Registered HISTORICAL_ONLY** (DP-31; DECISIONS.md items 23–24): the window Haci chose on 2026-09-13 places ≈ 16 contributing nights after the lock commit against DP-24's 30, so this run cannot reach PROSPECTIVELY_CONFIRMED; the tradeable verdict is reached by the successor question **Q010** (`research/questions/Q010_stop_whipsaw_prospective/PREREG.md`), locked at the same commit.

---

## 1. Hypothesis (plain English)

**The stop that SAS prints on a pick is often a trap: a real share of picks touch their printed swing
stop and then go on to reach the swing target L3 anyway, so a trader who treats the printed stop as
a hard exit loses money compared with one who does not.**

BACKLOG H-032 reads "Stop-hit then target within window (whipsaw rate) by stop distance". It names no
stop, no target, no window, no entry, no baseline and no decision. This PREREG fixes all of them
(§2–§4). Two things are tested as primaries, and no sign is presumed (two-sided):

- **(P1, mechanism)** picks go "stop first, then L3" more often than near-identical unpublished stocks
  with a stop and a target at the same ATR distances — i.e. the whipsaw is something about SAS picks,
  not just volatility geometry;
- **(P2, money)** treating the printed swing stop as a hard exit changes what a trade to L3 makes,
  on the same picks.

**H-032's "by stop distance" half cannot be tested in this window, and is registered as descriptive
only.** The Steward's measured exposure count (`research/reports/STEWARD_Q009_exposure.md` §R1(b) and
its v003 addendum) shows that of 303 eligible picks, **282 (93.1%) are TIGHT** (`0 < s_close < 1.0`
ATR), **21 (6.9%) are MID** and **0 are WIDE** — the widest printed stop in the window is **1.70 ATR**.
A "tight-stop" endpoint would therefore be P2 recomputed on 93% of the same rows, not a stop-distance
contrast. **P3 is demoted to a descriptive figure** (§4), the within-question BH correction still runs
across **m = 3** so that the demotion lowers no bar (§7), and the stop-distance view is carried by the
continuous `Δ_p`-against-`s_close` figure and the model-free ATR stop grid, neither of which licenses
a width (§9). DECISIONS.md item 17.

**Which picks this question speaks for.** Under `exclusions_v003.json`, the window's matured
population is **383 published picks on 48 matured nights**, of which **303 picks on 47 contributing
nights** are eligible — **79.1% of published picks**. The binding exclusion is the **wrong-side
printed stop: 66 of 371 (17.8%)** of published picks that carry a swing lane and an L3 print a stop
already on the wrong side of the pick-night close (for a bullish pick, a stop above the close). Those
picks' printed stops are unusable and **no claim in this file extends to them**; the defect itself is
filed to `PLATFORM_ISSUES.md` under DP-07 and is not a research question here (DECISIONS.md item 18).

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first.
- Source tables (manifest_v001 and its successor): `sas_candidates` (`qualified`, `selected_rank`,
  `overall_score`, `dominant_direction`, `best_timeframe`, `outcome_target_invalid` (exclusion
  audit only), `public_payload_json` → `lane_plans.<lane>.{entry, stop, targets, invalidation}`),
  `sas_runs` (`finished_at`, `stats_json` for the exclusion audit only).
- Source tables (manifest_prices_v001 and its successor): `prices_daily_split` (pick-night close,
  forward highs/lows/opens/closes, ATR14, beta60, run-up, SPY tape), `prices_daily_raw` (split-factor
  snapping only), `prices_hourly_raw` (same-session stop-vs-target ordering for P2 and P3's
  descriptive companion, on published picks only — §4).
- **Treatment rows:** every published pick — **`qualified IS TRUE AND selected_rank IS NOT NULL`**
  (DP-28; DECISIONS.md item 11); dark-lane and qualified-false rows are **not** treatment rows — on a
  non-excluded night in the §6 test window whose `public_payload_json.lane_plans.swing_trading`
  carries **both** a non-null `stop` **and** a first target (= L3, `targets[0]`).
- **What "the stop" is, exactly.** The **printed swing-lane `stop`** of the called-direction setup —
  the stop of the lane whose target is this question's primary level (DP-30; DECISIONS.md item 3) —
  as extracted at publication by volatilx `services/super_agent_select_service.py:94-95` and written
  at `:155-161` (`buy_setup` for bullish, `sell_setup` for bearish, `:77`). The pick's own
  `best_timeframe` lane is **not** used: it would make the stop line vary pick by pick and break the
  one-lane pairing with L3. It is an LLM-written price from the Principal Strategist prompt
  (`ai_agents/principal_agent.py:550`, `:568-581`), **not ATR-scaled and not validated**: the writer
  checks targets against spot and entry (`super_agent_select_service.py:113-152`) but passes `stop`
  through untouched (`:158`). The swing lane is chosen because L3 is the swing lane's first target
  (`services/sas_conviction_card.py:182-187`), the swing stop is the platform's own "realistic deep
  downside marker" (`services/sas_excursion.py:297`, `:315-317`), and it is the stop shown on the
  report card (`report_center_frontend/components/ReportCard.tsx:254-255`). Day-lane (day stop ↔ L1),
  long-lane (long stop ↔ L5) and the printed swing **invalidation** line are secondaries (§4).
- **Disclosed, measured fact — the studied stop is always the strategist's.** The deterministic
  fallback that sets the stop 0.5% from the lane entry (`ai_agents/principal_agent.py:897-911`) is
  **never** the writer in this population: **0 of 386 in-window and 0 of 874 all-time** published rows
  carry the fallback pattern (`STEWARD_Q009_exposure.md` §R1(f)). The population does not mix
  LLM-written and fallback stops, and no endpoint conditions on it (DECISIONS.md item 21).
- **Definitions (all prices in the signal-date split basis):**
  `C_t` = actual regular-session close on pick night t (`prices_daily_split`; never `spot_close`,
  which is stale on re-run nights — EXPLORE_001 §9) — **this is the entry** (§4);
  `ATR` = ATR14 from `prices_daily_split` through night t (platform `atr_pct` is corrupted around
  splits — DATA_NOTES; not used); `dir` = +1 bullish, −1 bearish;
  `S` = printed swing stop; `T` = L3;
  `s_close = dir × (C_t − S) / ATR` — the entry-relative stop distance, **known at publication**, and
  both the bucket variable and the grading geometry;
  `d_close = dir × (T − C_t) / ATR` — the entry-relative target distance, also known at publication.
- **Stop-distance buckets (fixed here, on `s_close`; DP-26, DECISIONS.md item 4):** **TIGHT**
  `0 < s_close < 1.0`; **MID** `1.0 ≤ s_close < 2.0`; **WIDE** `s_close ≥ 2.0`. The 1-ATR unit is the
  desk's standard adverse line (Q004's race); the cut points are fixed here and are not an open
  decision. **Measured composition (`STEWARD_Q009_exposure.md` §R1(b) + v003 addendum):** of 303
  eligible picks on 47 contributing nights, **TIGHT 282 (93.1%) / MID 21 (6.9%) / WIDE 0 (0.0%)**,
  maximum `s_close` **1.70 ATR**. The three buckets do **not** partition a spread of stop widths in
  this window; the WIDE definition is retained in `eval.py` for later windows and printed as n = 0.
- **Exclusions — each counted and printed in the results header, never silently dropped:**
  - nights in `research/data/exclusions_v003.json`: `manual_runs.trading_dates`,
    `non_session_runs.trading_dates` and `uncorroborated_publication_runs.trading_dates`. In this
    window those are **2026-07-02** and **2026-07-06** (re-run nights: the frozen `sas_candidates`
    rows, including every printed stop, are a re-run's output and not the 16:05 ET decision's) and
    **2026-06-26** (excluded **whole-night**: the night's own `sas_runs.stats_json` records 8
    qualified, all bullish, while the frozen table carries 11 qualified ranked rows, the 3 extra
    bearish ones carrying fully-formed payloads including swing stops — the only such night in 113;
    `STEWARD_Q009_exposure.md` §R3 ruling 1, DECISIONS.md item 20). `eval.py` reads the JSON and
    unions the three `trading_dates` lists; **no hard-coded dates** (DP-22).
  - any prospective night whose `finished_at` is later than the next session's open (DP-04, applied
    mechanically, the same criterion as `manual_runs`).
  - **null-ladder denominator:** picks with no lane-plan ladder at all → excluded and counted
    (measured: 8 of 383 in this window).
  - **null-stop denominator:** picks with a swing lane and L3 but `stop` null → excluded and counted.
    This exclusion stays in `eval.py` so a successor freeze cannot behave differently unnoticed, but
    it is **measured at zero** — 0 in-window, and 0 of the 874 all-time published rows that carry a
    swing lane (`STEWARD_Q009_exposure.md` §R1(a),(e)). It is not an unknown and not a headline
    (DECISIONS.md item 21).
  - picks whose `outcome_target_invalid` is non-null (4 in-window) or whose **L3 is on the wrong side
    of `C_t`** (`d_close ≤ 0`; invalid target at publication,
    `super_agent_select_service.py:810-839`; 2 in-window) → excluded and counted. Rule 5's "a target
    already passed at entry is not a hit" is carried by this exclusion.
  - picks whose **stop is on the wrong side of `C_t`** (`s_close ≤ 0`; possible because the stop is
    set off the lane `entry`, which may stray > 5% from spot — `super_agent_select_service.py:101-111`,
    `services/sas_excursion.py:188-203`) → excluded and counted. **This is the binding exclusion:
    66 of 371 (17.8%) measured.** It is printed **per bucket, per month and per score band** in the
    results header (§10 threat 10 cannot be read otherwise).
  - picks with fewer than **20** forward sessions in the pinned freeze (immature on the primary clock)
    → excluded and counted; right-censoring is never graded as a non-touch. The 40-session descriptive
    companions are computed only where 40 forward sessions exist, and say so.
  - delisted / missing-bar symbols → dropped and counted; a night is dropped if > 25% of its picks
    are missing bars. Symbols with fewer than 60 daily bars dated ≤ t are excluded (0 in-window).
- **Contributing nights (the floor unit, DP-21; DECISIONS.md item 10):** **P1** — a night with ≥ 1
  eligible pick carrying a valid B1 control set; **P2** — a night with ≥ 1 eligible pick; **P3
  (descriptive)** — a night with ≥ 1 eligible TIGHT pick. Measured today, all three definitions
  collapse to the same **47 of 48** matured nights.
- Levels and windows: L3 is the swing lane's first target and the platform's swing-lane window is 40
  trading sessions (volatilx `services/sas_conviction_card.py:188-195`, `_LADDER_LEVEL_WINDOW` at
  `:194`), but the **primary clock here is 20 sessions from the stated entry (DP-09; DECISIONS.md
  item 9)**, with the platform's 40-session lane window reported alongside, descriptively.

## 3. Baseline(s) — what this must beat

- **B1 (P1 — rule 5 distance-matched control).** For each eligible pick, the **10 nearest same-night
  non-published** `sas_candidates` rows — the complement of the DP-28 publication predicate
  (qualified-false and dark-lane rows alike) — matched on `beta60` / `atr_pct` / `runup20` (from
  `prices_daily_split` at the pick-night close; standardized by the night's cross-sectional median and
  MAD; Euclidean; with replacement across picks; ties by symbol ascending) — the Q006 §3 construction,
  with levels anchored to the **control's own pick-night close** (the Q007 B3 anchoring pattern, moved
  from the open to the close, DP-11):
  `S_c = C_c × (1 − dir_p × s_close,p × atr_pct_c)`,
  `T_c = C_c × (1 + dir_p × d_close,p × atr_pct_c)`,
  graded from the control's own close, same direction, same **20-session** window, **same daily-bar
  rule** (§4). Controls without a synthetic stop on the adverse side or with a non-positive target
  distance are impossible by construction. Control rows never add to inferential n (rule 6).
  *Measured availability (`STEWARD_Q009_exposure.md` §R1(c) + v003 addendum):* **100%** of eligible
  picks have ≥ 10 same-night non-published controls with ≥ 60 daily bars dated ≤ t (median pool 54,
  10th percentile 41) — the nearest-10 pool never binds in this window, and no pick is dropped for
  want of a control. Picks without a valid control set are excluded from P1 and counted.
  *What B1 answers:* if picks whipsaw no more than controls, the whipsaw is volatility geometry and
  the fix is ATR-scaled stop placement for everything; if picks whipsaw more, a stop touch on a pick
  is weaker evidence against the thesis than on a generic stock.
- **B2 (P2 — the same picks without the stop).** The paired baseline is the identical trade with
  no stop (plan E-NOSTOP, §4). No external cohort is needed: the question is what the stop does to
  *this* trade. This is the "Y's rate when X did not happen" baseline in its cleanest form — the
  same pick, stop vs no stop.
- **B3 (descriptive): P2's stop-minus-no-stop difference computed on the B1 matched controls** with
  their synthetic stops and targets. Separates "the printed stop costs money on SAS picks" from
  "a stop at that ATR distance costs money on any stock". Never decides.

## 4. Objective metric (rule 5 — price path, measured the way it is traded)

**Entry basis: the pick-night regular-session close `C_t`** (`prices_daily_split`), the DP-03(a)
after-hours proxy, **for picks and controls alike** (DP-11; DECISIONS.md item 12). Session index
k = 1..20, with **k = 1 = session t+1** and the position entered at `C_t`. Touches use the
regular-session daily low/high. Levels already on the wrong side of `C_t` are excluded (§2), which is
how rule 5's "a target already passed at that entry is not a hit" is enforced here.

**Stops are assumed in this question, and only here — rule 5's exception, stated explicitly (DP-02;
DECISIONS.md item 13).** The printed swing stop is used **as an exit only inside plan E-STOP**, in P2
and in P3's descriptive companion. **The exception is confined to plan E-STOP in P2 and P3. Every
other figure in this file — P1, every touch rate, first-touch session, adverse excursion,
counter-direction touch and the committed L1–L6 scale-out — is graded with no stop, and the same
sentence is printed in the results header and in `REPORT.md` (rule 5; DP-02).**

**Primary endpoints (two, pre-specified; BH-corrected within this question across m = 3 — §7):**

- **P1 — whipsaw rate beyond distance (touch-order claim; rule-5 control applied).**
  Bullish (bearish mirrored): `k_S` = first k ≤ 20 with `low_k ≤ S`; `k_T` = first k ≤ 20 with
  `high_k ≥ T`. **WHIPSAW = 1** iff `k_S` exists, `k_T` exists and `k_T > k_S`.
  Same-session first touches (`k_T = k_S`) are recorded as **SAME_SESSION** and scored 0 — daily bars
  only, for picks and controls alike, so the grading is symmetric (DP-27 in P1's direction: it is the
  reading less favourable to the hypothesis, and hourly-only-for-picks would grade the two sides
  differently; DECISIONS.md item 6).
  **Unconditional:** every eligible pick is in the denominator, stopped or not. The conditional rate
  "reached L3 given the stop was touched" is survivor-conditioned and is descriptive only.
  Pick: `x_p = WHIPSAW_p − mean_c WHIPSAW_c`. Night: `D1_t = mean_p x_p`. Estimand `m1 = mean_t D1_t`,
  percentage points.
- **P2 — realized result of the stop (named execution plans, paired on the same picks).**
  - **Plan E-NOSTOP:** enter at `C_t`; exit at the first touch of L3 within k ≤ 20 at the L3 price —
    at the session open instead if that session (k ≥ 1) **opens through** L3; otherwise exit at the
    session-20 close.
  - **Plan E-STOP:** enter at `C_t`; exit at the first of: L3 (as above) or the printed swing stop at
    the stop price — at the session open instead if that session (k ≥ 1) **opens through** the stop
    (gap-through fills at the worse price); otherwise the session-20 close.
    **Same-session ordering** (both levels first touched in the same session k, neither via the
    open): resolved with `prices_hourly_raw` bars for that session in time order (converted to the
    signal-date split basis; `eval.py` asserts basis agreement per symbol-date and fails loudly);
    if the same hourly bar holds both, or the symbol has no hourly bars, **the stop fills first**
    (DP-27, conservative for the no-stop side of the argument; the count is printed).
  - Per pick: `r = dir × (exit − C_t) / ATR`; `Δ_p = r_{E-STOP} − r_{E-NOSTOP}` (zero unless the stop
    exits first). Night: `D2_t = mean_p Δ_p` over **all** eligible picks. Estimand
    `m2 = mean_t D2_t`, ATR units. Negative = the printed stop costs money.

**Secondary, descriptive, never decides:**
- **P3 (descriptive, does not decide) — the stop-distance view.** `D3_t = mean_{p ∈ TIGHT,t} Δ_p`,
  estimand `m3 = mean_t D3_t` in ATR units, on the same E-STOP/E-NOSTOP construction; the
  **TIGHT-vs-MID difference** of `D2_t`, printed **only if the MID cell clears 20 contributing
  nights** and SUPPRESSED with its counts printed otherwise; and a **continuous** view — `Δ_p`
  against `s_close`, binned at 0.25 ATR, with a rank correlation. `m3`'s p-value is still computed
  and still enters the BH correction (§7); it cannot carry a verdict (DECISIONS.md item 17);
- the **40-session companion** of P1, P2 and P3 — identical constructions with k = 1..40 and the
  terminal exit at the session-40 close — computed wherever 40 forward sessions have matured, on the
  same 10-session bootstrap block, labelled "descriptive, does not decide" (DP-09);
- a **model-free ATR stop grid** — synthetic stops at 0.5 / 1.0 / 1.5 / 2.0 / 3.0 ATR from `C_t` on
  the same picks, with L3: unconditional whipsaw rate (picks vs B1 controls) and E-STOP − E-NOSTOP
  per grid point. With WIDE empty and 93% of the population TIGHT, this is now the **only** view of
  stop width in the file. It is the causal-leaning view and it **cannot license a specific width**
  (§9);
- conditional rates: L3 reached after the stop was touched, among stopped picks (and controls);
  sessions from stop touch to L3 among whipsaws;
- stop touch rate within 20 sessions (and 40); maximum adverse excursion from `C_t` in ATR; the share
  of stops hit by a gap through at the open;
- the **printed swing invalidation** (`lane_plans.swing_trading.invalidation`) run through the same
  P1/P2 constructions, since the platform's guide treats it as the thesis-dead line
  (volatilx `scripts/generate_sas_trading_guide.py:538-542`, `services/sas_excursion.py:474-493`);
- day lane: day stop ↔ L1 within 20 sessions; long lane: long stop ↔ L5 within 60 sessions (matured
  nights only), each with B1;
- the committed L1–L6 scale-out (`BAND_EXITS`, volatilx `scripts/generate_sas_trading_guide.py:89-95`)
  run with and without the printed swing stop on the open remainder, truncated at 20 sessions (40 as
  a descriptive companion) and labelled so (fractions whose level was already passed at `C_t` are
  unfillable and excluded; `<80` not traded; trailing rules ignored as non-deterministic);
- **entry-basis sensitivities, neither of which decides:** the whole P1/P2 construction re-run on a
  **next-open** entry (`O_{t+1}`, picks and controls alike), and on the real after-hours price `E_AH`
  (Q004's definition verbatim) as a **picks-only** sensitivity;
- B3 (stop cost on matched controls); E-STOP − E-NOSTOP in percent instead of ATR;
- the platform commits touching `services/super_agent_select_service.py` and
  `ai_agents/principal_agent.py` inside the window, printed, with P2 split at each such date
  (a cheap robustness check — §10 threat 6);
- close-to-close return from `C_t` at T+20 / T+40 (secondary by rule 5).

**Quotability:** 20/40/60-session bases → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** Night-level. **CI (decides):** stationary block bootstrap over the ordered contributing
nights, **expected block length 10 sessions** (20-session forward windows overlap across adjacent
nights; Q007 §4; DECISIONS.md item 15), 2,000 resamples; the date-clustered bootstrap CI is printed
alongside. The 40-session descriptive companions are printed with the same 10-session block, and that
is stated. **p-value:** paired sign-flip permutation on the night statistics (`D1_t` pick minus
control; `D2_t`, `D3_t` stop minus no-stop), 10,000 permutations. Every estimate prints n(contributing
nights), n(picks), n(control rows), n(SAME_SESSION), n(hourly-unresolved ties), n(excluded, by
reason), and the count of contributing nights dated after the lock commit.

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21; DECISIONS.md item 10):** **≥ 80 contributing nights per primary
  endpoint** — P1 on its B1-valid definition, P2 on its own — and **≥ 20 contributing nights per
  reported sub-cell** (bucket, tape stratum, half, score band, bull/bear, regime). Cells below 20
  nights are **SUPPRESSED** — no point estimate printed. No floor is lowered to hit a date.
- **Binding maturity: 20 sessions** (DP-09). The 40-session companions are descriptive and are
  computed only where they have matured.
- **Measured exposure today (`research/reports/STEWARD_Q009_exposure.md` §R1 and its 2026-09-13 v003
  addendum; counts only, no bar dated after night t was read, not even `O_{t+1}`):** on pick nights
  2026-06-01..2026-08-12 with a matured 20-session window, under `exclusions_v003.json` —
  **48 matured nights**, **383 published picks**, **303 eligible picks**, **47 contributing nights on
  all three definitions** (P1 B1-valid, P2, P3 TIGHT), buckets **TIGHT 282 / MID 21 / WIDE 0**,
  B1 control pool median 54 / 10th percentile 41 with 100% of eligible picks at ≥ 10 controls. The
  Registrar states no hand-counted night total; `eval.py` prints every count it gates on.
- **Projection, for context only — it gates nothing.** The Steward's measured run-rate is 0.941
  contributing nights per session on the v002 population (48 over the 51 sessions 2026-06-01..
  2026-08-12, §R1(d)); under v003 the same 51 sessions carry 47. At that rate 80 contributing nights
  arrive ≈ **2026-09-30** and the registered window end (2026-10-02) projects ≈ **80** contributing
  nights against a floor of 80 — **marginal by construction**, which is why the DP-13 extension below
  fires automatically. Every gate is decided on `eval.py`'s measured counts from the frozen data,
  **never** on this projection.
- **Stop coverage is complete, and this question is not a DEFERRED candidate for want of stops.**
  The null-stop denominator is measured at **0** in-window and **0 of 874** published rows with a
  swing lane all-time (§R1(a),(e)); fallback-pattern stops are **0 in-window and 0 all-time**
  (§R1(f)). The exclusions remain in `eval.py` and are printed, in case a successor freeze behaves
  differently. The binding exclusion is instead the **wrong-side stop (66 of 371, 17.8%)**, reported
  per bucket, per month and per score band.
- **Window, decision date, extension and DEFERRED fallback (Haci 2026-09-13, question A, option 2;
  DECISIONS.md item 23; DP-13; no outcome looks at any point):**
  - **Primary window:** pick nights **2026-06-01..2026-10-02** inclusive, after exclusions.
    **Decision date: Monday 2026-11-09** — the last pick night matures 20 sessions later, ≈ 2026-10-30,
    leaving the Steward about a week to build and pin the successor freezes (R2). `eval.py` is written
    once (rule 9) and run on successor freezes whose as_of covers the matured window. **No interim
    looks.**
  - **The gate, per retained primary endpoint, on measured counts.** Evaluation proceeds only if
    **each** of P1 and P2, on its own contributing-night definition, has **≥ 80 contributing nights**
    printed by `eval.py` from the frozen data — never a projection, a run-rate or the Steward's
    0.941/session figure. A shortfall on one endpoint is never covered by the other's count.
  - **The post-lock count is reported, not gating.** `eval.py` prints contributing nights dated after
    the lock commit, per endpoint (projected ≈ **16**). It does **not** gate the historical verdict,
    and it cannot reach DP-24's 30 — see §8's HISTORICAL_ONLY paragraph.
  - **One automatic extension (DP-13).** If either endpoint's 80-night gate is short at 2026-11-09,
    the window extends **once**, with no further question to Haci, to pick nights
    **2026-06-01..2026-11-13**, decision date **Monday 2026-12-21** (20 sessions after the last pick
    night, ≈ 2026-12-11, plus the same freeze margin the primary date uses; the Steward fixes the
    exact session-count date when building the successor freezes, R2). The extended run uses the
    **unmodified `eval.py`** and the same gate.
  - **DEFERRED fallback.** If a gate is still short after that single extension, Q009 goes to
    **DEFERRED** (`research/questions/DEFERRED.md`, with the measured counts) rather than running
    under-powered. There is no second extension.
  - **Nothing weakens.** The 80-night gate is never reduced, no floor is lowered to hit a date
    (DP-21), the demotion of P3 never licenses reading P2 as a stop-distance result, BH stays at
    m = 3, and the shorter window is never used as an argument for relaxing anything else — the price
    of the shorter window is the prospective track, and that price is paid in full (§8, §9, and the
    successor question Q010).
- **Freeze discipline (DP-23; routed request R2, due at the decision date and not a blocker for
  lock).** Nights ≤ 2026-09-10 are pinned to `manifest_v001` / `manifest_prices_v001`. Nights after
  2026-09-10 enter only through successor freezes — `manifest_v002` (selections, same SQL) and
  `manifest_prices_v002` (same Alpaca queries; symbol list extended to **every candidate on the new
  nights, published and unpublished**, because B1 needs the unpublished symbols' pick-night closes and
  forward bars; plus **hourly bars for published symbols** for the P2 tie-breaks), carrying **20**
  forward sessions beyond the last included pick night (40 where the descriptive companion is to be
  computed). A second pair is built **only if** the DP-13 extension fires. `eval.py` records every
  sha256 and prints pre-lock and post-lock night counts separately. **`eval.py` takes the window start
  and end, the manifest paths, the exclusions-file path and the output directory as inputs — no
  hard-coded dates, manifest names or paths — so the same byte-identical script serves the primary
  run, the DP-13 extension run and Q010** (Q010 §4). **Neither successor freeze exists
  today.** Nights whose unpublished-candidate bars are missing are excluded from P1 and counted,
  never back-filled.
- Sub-cells (bull / bear; score band < 80 / 80–85 / 85–90 / 90+; tape stratum; regime label) are
  reported only where they clear 20 contributing nights. Bear, 90+ and **MID** cells are expected to
  be SUPPRESSED (DATA_NOTES; and MID is 21 picks in total).

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-06-01** through the decision date
  (2026-10-02, or 2026-11-13 if the DP-13 extension fires — §5).
  *Justification (one sentence):* EXPLORE_001 computed the printed lane stops' ATR distances and
  first-touch sessions for every April–May pick (`research/reports/explore/scripts/10_paths.py:82-89`)
  and published a counter-level-touch-then-L3 recovery rate (EXPLORE_001 §C), which is the same
  stop-then-target object, so the in-sample nights are contaminated for this question.
  *Registrar's disclosure:* to scope that contamination the registrar read EXPLORE_001 §C
  (lines 222-237), which contain in-sample figures; no threshold here was taken from them — the stop
  line, L3 and the lane windows are platform definitions, the 20-session clock is DP-09, and the
  1-ATR bucket unit is the desk's existing Q004 line.
  *Contamination check on the sealed period (count-only search, then the matching lines only):* the
  weekly snapshots of 2026-09-10 and 2026-09-12 contain no stop, invalidation or whipsaw figure (the
  three hits are unrelated uses of "stopped"). **One residual exposure:** the platform's own trading
  guide prints a swing-invalidation breach-reclaim rate across sealed bullish picks
  (volatilx `scripts/generate_sas_trading_guide.py:538-542`), so Haci may have seen a close-basis,
  calendar-window reclaim statistic that overlaps part of the test window. It is a different line
  (invalidation, not stop) on a different basis; it is disclosed, not corrected for. No results
  directory was read.
- **Catalyst-layer regime change:** the window sits entirely after the 2026-06-01 fix
  (`exclusions_v003.json` `catalyst_layer_regime_change`, platform commit 69ef05f).
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date; Half B = after. `in_sample_end = 2026-05-29` marks only what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v003.json` `regime_label_point_in_time_from`). It is used only for nights
    ≥ 2026-06-09 and only `regime_version = 'v1.2'`; nights 2026-06-01..06-08 carry no legal label
    and are stratified by the SPY proxy only, flagged.
  - Primary tape stratum for every night, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's
    trailing 20-session return × tercile of SPY's trailing 20-session realized volatility
    (`prices_daily_split`; terciles cut on the contributing-night set). Cells < 20 nights SUPPRESSED.
  - The report describes the tape in words from SPY's path and never implies a regime label existed
    before 06-09.
- **Knowledge time (rule 14) — every input declared. Q009 needs no rule-14 exception: no session-t+1
  quantity enters any primary endpoint or any eligibility filter (DP-05 untouched; no R-1 arises).**

  | input | source | available |
  |---|---|---|
  | `qualified`, `selected_rank`, `dominant_direction`, `overall_score`, `best_timeframe` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) |
  | **printed swing stop, L3, swing invalidation** | `sas_candidates.public_payload_json.lane_plans` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:792-809`); excluded nights are exactly those where `finished_at` post-dates the next open |
  | `C_t` (**the entry**), ATR14, beta60, runup20, `s_close`, `d_close`, SPY tape | `prices_daily_split`, bars dated ≤ t | pick night close |
  | regime label (v1.2, nights ≥ 2026-06-09) | `market_regime_daily` | pick night, ~16:05 ET |
  | `finished_at`, `stats_json` (exclusion criteria only) | `sas_runs` | publication time |
  | `outcome_target_invalid` (exclusion audit only) | `sas_candidates` | set at publication for new rows; §10 threat 6 verified negative |
  | forward bars k = 1..20 (40 for the companions), hourly bars for tie-breaks | `prices_daily_split`, `prices_hourly_raw` | outcome only |
  | `O_{t+1}`, `E_AH` — **secondary sensitivities only**, never a primary and never an eligibility filter | `prices_daily_split` bar t+1; after-hours quote | session t+1 / pick-night after-hours |

  Both the bucket variable `s_close` and the grading geometry are measured off `C_t`, so every
  conditioning input is known at publication. `sas_selection_excursion` already stores
  `pierced_swing_stop`, `reached_l3_after_reclaim` and related fields (volatilx
  `services/sas_excursion.py:469-537`), but they are close-basis (`entry_ref` = `spot_close`,
  `:336-354`), on calendar-day windows (`:8-18`, `:42-44`) and recomputed weeks later (manifest_v001
  `availability.sas_excursion`): **never used**, not even as a grading cross-check.
  `uoa_symbol_daily.fwd_return_*` is **banned** (the May–June freeze is not fixed — FREEZE_v001 §5);
  no UOA table is used.

## 7. Multiple testing

- **Within the question:** **BH across m = 3** — P1, P2 and P3 — at q ≤ 0.10; the verdict uses q.
  **P3's p-value enters the correction and cannot carry a verdict**: the demotion of P3 to descriptive
  (§1, §4) must not lower the bar for P1 and P2, and with m = 3 every BH threshold is at or below its
  m = 2 value (DECISIONS.md item 17). Secondaries other than P3 print raw p only, marked "descriptive,
  does not decide".
- **Across the family:** **F6 Exits and execution** (DP-29 — family is assigned by the primary
  endpoint's subject, and both P1 and P2 are about using the printed stop as an **exit**). F6 holds
  H-050, H-051, H-052 and **H-032** (re-filed from F4 when these decisions were applied). Q009 is the
  only registered F6 question, so the family correction is over Q009's own primaries today.
- **Anti-leniency clause (binding).** Because P1 *is* also a path-after-selection endpoint, the
  Reporter prints for P1 **two** q-values — BH within F6, and BH as if P1 were an F4 primary alongside
  the registered F4 primaries (Q007's four) — and **P1's verdict uses the larger (more conservative)
  q**. Moving the question to F6 must not make any endpoint easier to confirm than it was in the
  draft.
- **Q010.** Q010 (`stop_whipsaw_prospective`) is a **replication** of P1 and P2 on nights after this
  question's decision date, locked at the same commit; it is **not** counted as a second F6 question
  in the BH correction, and its result is never presented as independent evidence — it is the
  prospective half of this result (DECISIONS.md item 25).
- **Overlaps, stated so they are not double-counted as independent evidence:** Q004's
  "L3 before −1 ATR" race (F7) and Q007's secondary race use a fixed ATR adverse line, not the
  printed stop, and neither asks what happens *after* the adverse touch; H-033 (L4 → L2 → re-advance)
  is the favourable-side mirror; H-058 (F7, day-1 limit fills) and H-060 (F7, up-then-down) touch
  adjacent path shapes. None is merged here.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1` in percentage points of whipsaw rate (control-adjusted); `m2` (and the descriptive `m3`) in ATR
units per trade.

**MPE: P1 5.0 pp** (DP-20, the standing control-adjusted touch-rate number; P1 is a single control
adjustment, not a difference of differences). **P2 0.25 ATR per trade and P3 0.25 ATR per trade**
(Haci 2026-09-12 → DP-10; the standing number for every per-trade ATR-denominated endpoint, not
re-asked). P2's figure is averaged over **all** eligible picks including the unstopped ones. P3's
0.25 ATR is a **reference line printed beside a descriptive figure**, not a verdict threshold.

Per endpoint (two-sided; the verdict carries its sign):

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **contributing nights ≥ 80 for that endpoint**, on its own contributing-night definition (§2, §5);
  2. `|m| > MPE`;
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question (m = 3); for P1, the **larger** of its F6 q and its F4-equivalent
     q (§7);
  5. same sign in **both halves**, and neither half beyond MPE in the opposite sign;
  6. no tape stratum with ≥ 20 contributing nights beyond MPE in the opposite sign;
  7. **the verdict is emitted with the label `HISTORICAL_ONLY` and is never restated, ledgered or
     quoted without it.**
- **NULL:** floors met **and** 95% CI includes 0 **and** `|m| < MPE`. "The printed stop neither costs
  nor saves money on a trade to L3" is a real finding and is ledgered with the same care.
- **INCONCLUSIVE:** anything else — a reported sub-cell below floor (SUPPRESSED), halves disagreeing
  in sign, `0 < |m| ≤ MPE` with the CI excluding 0 ("real but below MPE", rule 6), or CI including 0
  with `|m| ≥ MPE`. A **primary-endpoint gate shortfall is not INCONCLUSIVE**: it fires the single
  DP-13 extension, and then DEFERRED (§5).
- **What licenses a rule:** a guide line or platform change about stops requires **P2 CONFIRMED**
  (subject to §9's opening line). P1 alone never licenses a trading rule; it says only whether the
  whipsaw is more than volatility geometry. P1 CONFIRMED with P2 NULL is reported as "picks do recover
  from stop touches more than generic stocks, but not by enough to change what the trade makes". P3 is
  descriptive and licenses nothing on its own.

**PROSPECTIVELY_CONFIRMED is unreachable from this run by design.** The registered window places
≈ **16** contributing nights per endpoint after the lock commit (measured rate 0.941 contributing
nights/session, `STEWARD_Q009_exposure.md` §R1(d)), against DP-24's **30**. Haci chose this window on
2026-09-13 with that consequence stated (DECISIONS.md question A). The highest verdict available here
is **HISTORICALLY_CONFIRMED**, and it is emitted with the label **`HISTORICAL_ONLY`** in the results
header, in `REPORT.md` and in the LEDGER entry. The clause is not weakened to fit: DP-24's 30 stands,
and the prospective track is reached by the successor question **Q010**
(`research/questions/Q010_stop_whipsaw_prospective/PREREG.md`, locked at the same commit), never by
re-reading this one. (DP-31.)

- **PROSPECTIVELY_CONFIRMED:** only after **≥ 30 contributing nights for the confirming endpoint
  dated after this file's lock commit** (on that endpoint's own contributing-night definition),
  frozen separately and never inspected earlier, reproduce the sign of the confirming endpoint under
  the unmodified `eval.py`. No subscriber-facing statement before that (rule 10); even then the basis
  is NON_QUOTABLE until restated on W60 (rule 12). This clause is unchanged and unweakened; it is
  satisfied, if at all, through Q010.

## 9. If CONFIRMED, what changes on the platform

**Nothing in this section fires on a historical-only verdict.** Every guide line, card change, brief
and subscriber-facing statement below requires PROSPECTIVELY_CONFIRMED (rule 10), which this run
cannot produce; a HISTORICALLY_CONFIRMED result here licenses **no** product change, **no** Manual
Trading Guide edit and **no** quotable number — it licenses only the successor question Q010. What
follows describes what would change **after** Q010 confirms the pair (§8; DP-31).

Today the printed stop is shown to subscribers (volatilx
`report_center_frontend/components/ReportCard.tsx:254-255`), is written by the LLM with no ATR
scaling or validation (`services/super_agent_select_service.py:94-95`, `:158`), and the guide tells
traders not to ignore it ("size every position as if the breach could be real",
`scripts/generate_sas_trading_guide.py:538-542`).

- **P2 CONFIRMED negative (the printed swing stop costs money):** the guide's rule at
  `generate_sas_trading_guide.py:538-542` is rewritten so the printed swing stop is a **sizing
  reference, not an exit order**, and the card relabels "Stop" accordingly. Because the eligible
  population is **93% tight-stopped** (`s_close < 1 ATR`, maximum 1.70), a CONFIRMED-negative P2 **is**
  a statement about tight printed stops: the guide line "a printed swing stop this close to the
  pick-night close is inside normal noise; do not use it as a hard exit" follows from P2, together
  with a brief for a flag-off stop-distance field on the pick card (stop distance in ATR, computed at
  publication). A brief for an **ATR floor on written stops** in `_extract_lane_plans`
  (`services/super_agent_select_service.py:94-161`) is justified only for the *existence* of a floor;
  **the floor's width is not licensed by this question** (the §4 grid is descriptive) and needs its
  own PREREG. What replaces the stop as an exit is not tested here.
- **P2 CONFIRMED positive (the stop saves money):** the guide's existing language is strengthened to
  "honour the printed stop", with the measured saving shown next to it (NON_QUOTABLE until W60 and
  prospective).
- **P1 NULL with P2 CONFIRMED negative:** the cost is volatility geometry, not something about SAS
  picks — the fix is ATR-scaled placement of stops for every lane, linked to H-053's ATR-scaled
  ladder work, rather than a pick-specific "stop touches don't mean much" message.
- **All NULL:** no change; the guide's current stop language stands, and F6 effort moves on.
- Owner: implementer. Ship flag-off with a byte-identical checksum on the old path; shadow ≥ 20
  trading days before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **Stop placement is not random.** The LLM may set tight stops on names it sees as clean breakouts
   and wide ones on messy charts, so TIGHT vs MID differs in more than width. The descriptive P3
   figures are statements about *printed tight stops as they occur*, not about the causal effect of
   width; the §4 grid (same picks, synthetic widths) is the causal-leaning view and is descriptive.
   In this window the point is largely moot: there is almost no width variation to confound
   (TIGHT 282 / MID 21 / WIDE 0).
2. **The stop is anchored to the lane entry, not the close.** Lane entries can stray > 5% from spot
   (`super_agent_select_service.py:101-111`), so some stops sit in odd places. **Measured: 66 of 371
   (17.8%)** published picks with a swing lane and an L3 print a stop on the wrong side of `C_t` and
   are excluded; the count is a headline, printed per bucket, per month and per score band
   (`STEWARD_Q009_exposure.md` §R1(a) + v003 addendum). The wrong-side-L3 count (2) is printed beside
   it. Filed as a platform defect under DP-07, not researched here.
3. **Daily bars cannot order a same-session stop and target.** P1 scores SAME_SESSION as 0 for picks
   and controls alike; P2 (and P3's companion) use hourly bars for picks and fill the stop first when
   unresolved (DP-27). Both counts are printed; a large unresolved count makes P2 conservative
   against "the stop costs money".
4. **Gap-through fills, and the close is not a tradable price.** E-STOP fills at the open when price
   gaps through the stop, which is worse than the stop price; that is how a resting stop trades, and
   it is deliberate. Separately, SAS publishes after the close, so `C_t` is a **proxy** for an
   after-hours fill (DP-11); the picks-only `E_AH` sensitivity in §4 shows the size of that
   difference and never decides.
5. **The stock path is a proxy for the spread.** E-STOP/E-NOSTOP are equity trades; a vertical's stop
   behaves differently (theta, IV, width). Option prices are not held (research/questions/DEFERRED.md);
   any §9 guide line about spreads must say so.
6. **Ladder-writer changes inside the window — verified negative.** The wrong-side-target guard and
   E9a reclassification (`super_agent_select_service.py:810-839`, ruling E9-2026-07-05) and the
   cross-lane monotonic re-sort (`:195-257`) changed how L3 is written during the test window.
   **Ruled 2026-09-13 (`STEWARD_Q009_exposure.md` §R3 ruling 2): no historical payload rewrite.**
   Across the entire 795-row correction ledger no row touches `public_payload_json` or any
   `lane_plans` field; the wrong-side-target guard has no backfill path by construction; the W3
   re-sort's late `updated_at` touches all cluster in freeze week (2026-09-05/08/09/10), none on the
   deployment dates; the only 4 in-window E9a rows are exactly the 4 the `outcome_target_invalid`
   exclusion already removes. The descriptive commit-split robustness check in §4 stays.
7. **One tape.** The window is Jun–Oct 2026 (Nov if the extension fires); a sign in only one half
   fails §8 clause 5. Nothing here speaks to a strong up-tape, where dips recovered more (the guide
   itself calls its reclaim rate a bull-regime statistic).
8. **Overlapping 20-session windows** inflate precision; block length fixed here (10 sessions).
9. **Matching on 3 features may not span selection** (Q006 threat 1); post-match standardized mean
   differences are printed.
10. **Null-ladder and wrong-side denominators — which picks this speaks for.** The null-stop
    denominator is measured at zero, so the population is not thinned by missing stops; the
    wrong-side-stop exclusion thins it by 17.8%. The question therefore **speaks for 303 of 383
    published picks (79.1%)** — those whose printed swing stop is on the correct side of the
    pick-night close — and for no others. The null-stop share and the bucket split are printed by
    month and by score band so this can be read directly; if they differ sharply by month or band,
    the report must say so.
11. **Mixed-state night 2026-06-26 — resolved by exclusion.** The night's own run audit records 8
    qualified rows, all bullish; the frozen table carries 11 qualified ranked rows, the 3 extra
    (DPZ, COIN, AAPL) bearish with fully-formed payloads including swing stops. It is the only such
    night in 113. The **whole night is excluded** by
    `research/data/exclusions_v003.json` `uncorroborated_publication_runs`
    (`STEWARD_Q009_exposure.md` §R3 ruling 1; DECISIONS.md item 20). Cost: one contributing night
    (48 → 47) and 10 eligible picks (313 → 303), already reflected in every measured figure above.
    The platform half (an in-place run table with no append-only audit) is filed under DP-07.
12. **Elite is thin and shrinking** (DATA_NOTES); 90+ cells are SUPPRESSED, not reported small. So is
    MID (21 picks in total), and WIDE does not exist in this window.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: **R2 — the successor freezes
(`manifest_v002`, `manifest_prices_v002`, and a second pair if the DP-13 extension fires), built and
pinned at the decision date by design (§5, DP-23); not a blocker for lock.** R1 and R3 were returned
on 2026-09-13 (`research/reports/STEWARD_Q009_exposure.md`) and R4 was delivered as
`research/data/exclusions_v003.json`, which this file cites. Q009 is locked **together with its
successor** `research/questions/Q010_stop_whipsaw_prospective/PREREG.md` at the same commit (DP-31;
DECISIONS.md item 25) — the prospective half of this result, which must be registered before any of
Q009's numbers are seen.
