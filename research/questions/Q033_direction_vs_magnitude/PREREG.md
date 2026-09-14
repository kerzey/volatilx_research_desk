# Q033 — direction_vs_magnitude: does VolatilX get the direction right more reliably than it gets the distance right?

**Status:** PREREG_DRAFT (lock by committing this file)
**Scope at this lock: P1 alone.** **P2 (`V = G_μ − G_α`) is DEFERRED at this lock** (DECISIONS items
16, 22, 33): §2.2's tape arm cannot be assigned without SPY split-adjusted daily bars from
2025-01-02, those bars sit in **no** pinned manifest, and the pre-lock probe could not be attempted
because `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` are both unset in the desk session
(`research/reports/STEWARD_Q033_exposure.md` §(f) — the H-074 blocker, shared with Q030 and Q032).
The endpoint's record, its second independent deferral ground and its re-entry trigger are in
`research/questions/DEFERRED.md`; **Q033 itself is not deferred, no question number is consumed, and
`state.json` goes to `PREREG_LOCKED`**. `V` returns only as a **successor question with its own id**,
never by editing this file, whose lock fixes `m = 1`.
**Family:** **F8 System validity** (hypothesis **H-081**, Haci's Master Hypothesis Program **H11**,
*Direction vs expansion*), as filed in BACKLOG.md (DECISIONS item 4). **F8 = 1** at this lock and
never below it. P1's subject is a picks-versus-matched-control path contrast, which is F1's subject,
so under DP-29 it **additionally** carries a companion correction across **F1 (28 endpoints)**, and
the **larger** of the two applicable q's decides — which is F1's in every branch (§7). With `V`
deferred, **Q033 carries no F2 endpoint** (F2 falls 17 → 16) and F2's slot returns only with a
successor.
**Manifest (sealed post-hoc panel and the borrowed exposure counts only):**
research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA
fa70688bc252d14f8d67e371afafc194731c324e).
**Manifest (prices, sealed post-hoc panel only):** research/data/manifest_prices_v001.json
(as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374).
**Successor freezes — the question itself (built and pinned at the decision date, DP-23; §5.3 R2):**
a selection freeze (`sas_candidates` **every row, published and unpublished**, `sas_runs`,
`market_regime_daily` with `created_at` preserved — the rule-7 stratification read, not optional) and
a price freeze (daily bars for **every candidate symbol on every in-window night**, hourly bars for
published symbols), covering pick nights **2026-09-15 .. 2027-04-30** with daily bars through
**2027-06-29** (session **t+40** of the last included pick night — the binding maturity of §2.3 /
§2.5, never t+20) and ≥ 60 prior sessions before 2026-09-15; a second pair **only if** the single
DP-13 extension fires, covering pick nights **.. 2027-06-14** with daily bars through **2027-08-11**.
**The SPY-from-2025-01-02 requirement is withdrawn and HELD with P2** (DECISIONS item 30): the arm is
not computed by this question in any form, and the SMA50-only proxy is substituted for it nowhere.
This scope is a **strict superset** of the successor freezes Q027, Q029 and Q031 require (Q032 having
been deferred 2026-09-14), so one build serves all four. **Every night that carries a verdict here is after this lock
and exists in no manifest pinned today**, so the population enters only through those successor
freezes (`pin_at_decision`, DP-23 — the Q024 / Q027 / Q031 / Q032 pattern). They are named in prose
and deliberately not written as `**Manifest …:**` header lines, because no such file exists yet and
the pin step reads every `**Manifest` line as a path.
**Exclusions:** research/data/exclusions_v003.json (DP-22, the newest file) unioned with the
**add-only successor exclusions file** issued with the successor selection freeze — the identical
**four** criteria Q027 fixes at its lock (`manual_runs` ∪ `non_session_runs` ∪
`uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10.
The successor file may only **add** nights; no night is removed from a v003 list; the **criteria**
are fixed at this lock even though the **dates** cannot be. Both paths are `eval.py` inputs; no
hard-coded file name, no hard-coded date. DP-04 applies mechanically on top.
**Registered by:** registrar (autonomous run, DP-40..48) · **Approved by:** desk (DP-46) ·
**Date:** 2026-09-14
**Decisions:** DECISIONS.md (decision-maker, `decide` and `record`, 2026-09-14 — 33 items,
Corrections 1–22; where this file and that record ever disagree, the record governs)

---

## 1. Hypothesis (plain English)

**When VolatilX publishes a pick, the stock goes the way the pick said more often than its same-night
look-alikes do — and that direction advantage holds up across good and bad tape, while the advantage
in actually reaching the printed target does not.**

BACKLOG **H-081** (Haci's H11) reads: *"does VolatilX predict direction better than magnitude — PASS
direction stays stable while target / magnitude attainment varies systematically with the
environment; FAIL both degrade together → selection itself is deteriorating."* It names the
population (published picks vs Q006's distance-matched control, from the t+1 open), the two
quantities (direction; the printed L3 distance, i.e. Q006 E1), the primary (the interaction across
the rule-7 calendar / regime cells, two-sided), the MPE (±5.0 pp on each excess, DP-20), the baseline
(the matched control's own rates) and the stability definition ("the excess keeps its sign in every
window"). This PREREG fixes the cells, the entry, the levels, the clocks, the window, the estimator
and the decision rule.

**H-081 is registered in half, and this file says so before anything else.** The interaction endpoint
that carries Haci's own sentence — whether *target* attainment is the tape-conditional part of the
claim while *direction* is not — **is deferred at this lock** on the H-074 provisioning blocker, so
**no branch of this question's run may be described as H-081 passing or failing**. What P1 can settle
on its own is stated as it stands: **whether published picks go their own way more often than their
same-night look-alikes do**, with the matched-control rate printed beside it.

**One registered primary, night-level, two-sided:**

- **P1 — the direction excess (REGISTERED, `m = 1`).** `A` = the mean per-night control-adjusted rate
  at which a published pick's **own side** of a symmetric **±0.5 ATR** band around the t+1 open is
  touched **first**, within 20 sessions, against the same distance-matched same-night unpublished
  controls carrying the identical symmetric band in the pick's direction. Units: percentage points.
  **MPE ±5.0 pp** (DP-20, and H-081's own number).

**One endpoint deferred at this lock, recorded here as designed and standing:**

- **P2 — the interaction (DEFERRED, DECISIONS items 16 / 22 / 33).** `V = G_μ − G_α`, where
  `G_x = mean_{BENIGN} x_t − mean_{HOSTILE} x_t` is the tape-arm contrast of a night series, `μ_t` is
  the control-adjusted **magnitude** excess (first touch of the pick's **own printed L3 distance**
  within 20 sessions — Q006 §4's `Delta_t` on the DP-09 clock) and `α_t` is P1's per-night direction
  excess. Units: percentage points. **MPE ±10.0 pp** (§4.2). H-081's PASS predicts **`V > 0`**.
  It is **not computed here in any form**: the §2.2 arm is not assigned, `G_μ` is not computed, and
  the SMA50-only proxy is **never** substituted for the registered partition — that would be a
  different arm chosen after the data existed. Its entry, its two independent deferral grounds, the
  seven things a successor must re-measure and the H-074 re-entry trigger are in
  `research/questions/DEFERRED.md`.

**Why direction is measured on the path and not as the sign of a 20-session return.** H-081 as filed
defines direction as *"the sign of the 20-session move agrees with the pick's direction"*. That is a
fixed-horizon close-to-close quantity, and rule 5 / DP-01 are explicit that a fixed-horizon return is
descriptive and **never decides a verdict**. The registered direction endpoint is therefore the
**path** form of the same idea — which side of a symmetric ATR band is reached first — and it is
strictly better matched to the hypothesis in two ways: it is symmetric by construction, so it cannot
smuggle target *placement* into a *direction* claim (the printed ladder is not ATR-scaled — volatilx
`ai_agents/principal_agent.py:530-575` — which is exactly why the magnitude endpoint needs its own
distance-matched control), and it is measured from the price the pick is actually entered at. **The
filed 20-session sign version is computed and printed in §4.3 as a named descriptive companion, and
decides nothing in any branch.** The band width (**±0.5 ATR**, with ±1.0 ATR a fixed non-deciding
sensitivity) and the coding of a race that never resolves (**score 0, the pick stays in the
denominator**) are settled at this lock and move in neither direction at the decision pass
(DECISIONS items 1 and 2; DP-26).

**What this question is *not*.** It is **not** a second test of whether the selection edge exists
(Q006, F1, decides 2026-10-05), **not** a second test of whether that edge decays in time (Q031, F2)
and **not** a second test of whether it is conditional on the tape (H-079 / Q032, F2 — deferred
2026-09-14 on the same blocker). Q033 as locked owns exactly one thing no other registered question
owns: the **direction** series `α_t` and its pooled level. The contrast between the two series' tape
sensitivity is the deferred endpoint and belongs to no question today. §7 states every overlap.

**Why the window starts after the lock.** The sealed period has already been read for this
hypothesis: the platform's own `directional_pct` grade sitting at base rate is a standing desk
finding (CLAUDE.md), and EXPLORE_001 read the in-sample path excess by level and by speed. Those
reads are what put H-081 on the backlog, and H-081's own line records that the desk expects the
**opposite** of Haci's PASS. Those nights are contaminated for this question, carry **no verdict**,
and print once as a labelled post-hoc panel (§6).

**Direction of the claim.** P1 is registered **two-sided**, and its NULL is the branch the desk
expects (H-081's own line): *"published picks are no likelier than their same-night look-alikes to go
the way the pick said"* is a real finding, ledgered with the same care as a positive, and §9 says
what each branch licenses.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are reduced to one number per night
  per series first; nights are the observations. Control rows never add to inferential n.
- **Source tables (the successor selection freeze, §5.3 R2):**
  `sas_candidates` — `trading_date`, `symbol`, `qualified`, `selected_rank`, `overall_score`,
  `dominant_direction`, `best_timeframe`, `confidence_level`, `public_payload_json` →
  `lane_plans.{day_trading, swing_trading, longterm_trading}.{entry, stop, targets}` and
  `analysis_status`, `outcome_target_invalid` (exclusion audit only), `score_details_json`
  (band-integrity check, §10 threat 7), `context_json`;
  `sas_runs` — `finished_at` (DP-04), `config_json` (the weights / publication-gate audit, §10 threat
  8); `market_regime_daily` — the platform's point-in-time label, which carries **rule 7's
  stratification** for P1, **descriptively: it defines nothing, blocks nothing and carries no q**
  (§4.3, §6; DECISIONS item 26).
- **Source tables (the successor price freeze, §5.3 R2):** `prices_daily_split` (pick-night close,
  ATR14, beta60, runup20, the t+1 open, forward bars to t+40), `prices_daily_raw` (split-factor
  snapping only), `prices_hourly_raw` (published symbols; the same-session ordering tie-break of §2.3
  — **P1 machinery under DP-27, not a descriptive read** — and the descriptive entry audit). **No SPY
  history is read by this question**: it was the deferred arm's only input (DECISIONS item 30).

### 2.1 Treatment rows — exact filter

**The two dates below are illustrative of values `eval.py` receives as inputs.** §5.3 R2 requires the
script to take the window start, the window end, the manifest paths, the exclusions-file paths and
the output directory as arguments, with **no hard-coded date, manifest name or path**, so that the
byte-identical script serves the primary run and the DP-13 extension run alike.

```sql
SELECT c.*
FROM   sas_candidates c
JOIN   sas_runs run ON run.trading_date = c.trading_date
WHERE  c.qualified IS TRUE
  AND  c.selected_rank IS NOT NULL                   -- publication predicate, DP-28
  AND  c.trading_date  >= DATE '2026-09-15'          -- §6 window start   (input, illustrative)
  AND  c.trading_date  <= DATE '2027-04-30'          -- §5.2 window end   (input, illustrative)
  AND  c.trading_date NOT IN (<exclusions_v003 ∪ the add-only successor exclusions file:
                               manual_runs ∪ non_session_runs
                               ∪ uncorroborated_publication_runs ∪ payload_disabled_runs>)
```

**No score-band filter** (DP-25: H-081 is about the published slate); the band is a stratum (§6) and
the 90+ cell is SUPPRESSED at lock (§4.3). **No direction filter:** bull and bear published picks
both enter, direction-adjusted throughout, with a **bull-only blocking companion** (§4.3, §8 clause
8) because bear exposure is thin and graded below base rate (H-062). Dark-lane rows (`qualified`
false or `selected_rank` NULL) are **never** in the treatment arm (DP-28); they are the control pool
(§3 B2).

### 2.2 The cells — a bar-only tape partition — **NOT COMPUTED: deferred with P2**

**This subsection defines the deferred endpoint's arm and nothing in the locked question depends on
it.** No night carries an arm label, no cell is computed, no stratum, panel or sensitivity uses one,
and **the SMA50-only proxy is substituted for it nowhere** (DECISIONS items 16, 22, Correction 13).
The definition is kept verbatim for one reason: a successor question carrying `V` inherits it
**unchanged**, and nothing about it may be re-specified now that its counts have been seen.

Specified in full here, not by reference, so the definition stands whatever happens to any other
draft. It is the **identical definition Q032 §2.2 registers**. Every input is a split-adjusted SPY
daily bar dated **on or before the pick night**, from a pinned price freeze — nothing reads a
platform column, so a regime-engine repair cannot move a night between cells (DP-50(a)). All cuts are
registrar-chosen conventions fixed at lock and never derived from an outcome (DP-26).

- **`SMA50_t`, `SMA200_t`** = the simple means of SPY's split-adjusted closes over the trailing 50 and
  200 sessions ending at t (inclusive).
- **`trend_t`** = **`UP`** iff `close_t > SMA50_t` **and** `SMA50_t > SMA200_t`; **`DOWN`** iff
  `close_t < SMA50_t` **and** `SMA50_t < SMA200_t`; **`MIXED`** otherwise.
- **`rvol_t`** = the sample standard deviation of SPY's daily log returns over sessions t−19..t,
  annualised by √252. **`vol_t`** = `LOW` / `MID` / `HIGH` by the **expanding-window** terciles of
  `rvol` over every SPY session in the pinned freeze dated ≤ t, requiring **≥ 250 such sessions**;
  below 250 the night is **excluded and counted** (inside the registered window this count must be
  **0**, or R2(i) did not deliver). Expanding, never full-sample: no later night's volatility may set
  an earlier night's cell.
- **The two arms:** **BENIGN** iff `trend_t = UP` **and** `vol_t ∈ {LOW, MID}`; **HOSTILE**
  otherwise.
- **The nine-cell composition** (`trend_t` × `vol_t`) and the **HOSTILE composition guard** of §8
  clause 9 (any single one of the eight HOSTILE cells carrying ≥ 80% of HOSTILE contributing nights
  restates the verdict as being about that cell; a naming clause, not a floor change, fixed at lock
  and moving in neither direction) — **both lapse with P2 and are not computed**.
- **The four stability cells** (H-081's "windows") = the two arms × the two calendar halves of §6 —
  **uncomputable without an arm, and therefore not reported at all**, which is stricter than
  suppression (DECISIONS item 28). H-081's "keeps its sign in every window" is carried for P1 by the
  **two calendar halves alone**, which block under §8 clause 6.

### 2.3 Levels, entry, clocks

- **Direction** `dir` = +1 bullish / −1 bearish from `dominant_direction`. Every distance and every
  touch is direction-adjusted.
- **`C_t`** = the pick's actual regular-session close on pick night t from `prices_daily_split` (never
  the platform's `spot_close` — EXPLORE_001 §9). **`ATR`** = ATR14 from `prices_daily_split` bars
  dated ≤ t (never the platform's `atr_pct` — DATA_NOTES / PI-003).
- **Entry `X` = the session t+1 regular-session open** (DP-03(b), DP-42), for picks and controls
  alike. The **`C_t` basis (DP-03(a) / DP-11) is computed and printed as a named sensitivity** and
  never decides.
- **Direction band (P1):** `U = X + dir × 0.5 × ATR` (the pick's own side) and
  `D = X − dir × 0.5 × ATR` (the counter side), both **from the entry**, symmetric by construction.
  **The 0.5 is fixed at this lock and moves in neither direction at the decision pass** (DECISIONS
  item 1, DP-26): it is a measurement device, not an entry, a target or an exit (DP-02). The **±1.0
  ATR** variant is printed as a fixed sensitivity that never decides.
- **Magnitude level (μ, descriptive — §4.3):** `L3` = `lane_plans.swing_trading.targets[0]`, the
  printed swing first target (volatilx `services/sas_conviction_card.py:182-187`), at its own distance
  `d_L3 = dir × (L3 − C_t) / ATR`. **A level at or through `X` at the t+1 open is not a hit** (rule
  5): `hit = 0`, the pick stays in the denominator, and the not-takeable count is printed **pooled
  and per half** (there is no arm to print it by).
- **Clock: 20 sessions from `X`** for both series (DP-09 — L3 is the primary level, so the primary
  clock is the 20-session spread horizon; the direction band runs on the same clock so that the two
  series are measured over the identical exposure). The platform's own 40-session swing window is
  printed alongside for μ, descriptively. **Binding maturity: 40 sessions**, uniform across every
  eligible pick and every matched control, so that descriptive companion is never right-censored
  either. The maturity is **unchanged by P2's deferral** and is the clock every §5 date is computed
  on (DECISIONS items 5, 30; Correction 1).
- **Same-session ordering.** Where `U` and `D` are both touched on the same session and
  `prices_hourly_raw` cannot order them, the race counts **counter-first** — the outcome less
  favourable to the hypothesis (DP-27). **This is P1 machinery, so hourly coverage is load-bearing**
  (§5.3 R2). The count of such sessions is printed, pooled and per half, for picks and controls
  separately.

### 2.4 Exclusions — each counted, printed in the results header, never silently dropped

Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or a
measurement failure. Counts print **pooled and per half**.

- **Nights** in the union of `exclusions_v003.json` and the add-only successor file, and any night
  whose `finished_at` is later than the next session's open (DP-04), mechanically.
- **The "fewer than 250 prior SPY sessions" screen is STRUCK** (DECISIONS item 25, Correction 12). It
  existed only to serve the §2.2 arm; left in place with no SPY history it would exclude **every**
  night and empty a population that is otherwise fully measurable. Every other screen below stands
  verbatim.
- **Null-ladder denominator:** no lane plan, no swing lane, or no `targets[0]` → pick excluded and
  counted (the measured in-sample signature is `analysis_status="disabled"` nights —
  `STEWARD_Q031_exposure.md` §(c): 8 of 383 rows, all on one night).
- **Wrong-side or non-monotone ladder at the close:** `d_L3 ≤ 0`, the six flattened levels **not
  monotone non-decreasing in the pick's direction — ties across lanes allowed, the platform's own
  predicate `_ladder_is_monotonic` (`services/super_agent_select_service.py:180-192` at the pinned
  `fa70688`: bullish `all(b >= a)`, bearish `all(b <= a)`), whose writer `_enforce_ladder_monotonic`
  (`:195-257`, commit `5fa3db4`, 2026-07-06) states that equal prices across lanes are allowed by
  design** —, or `outcome_target_invalid` non-null → excluded and counted (DECISIONS item 34,
  Correction 23). Three guards ride with the screen. **(i)** `eval.py` prints the screen's own firing
  rate per window — pooled, per half, and for picks and controls separately — and **fails loudly**
  if it exceeds the pre-fix **25.71%** recorded in `DATA_NOTES.md` (steward, Q018 R1: 36/140 before
  2026-07-06; **0.00%, 0 of 355, on/after**), and this question's window is entirely post-ship.
  **(ii)** The **strict** variant is printed as a **counted companion** — rows passing non-strict and
  failing strict — per window and per half, so the register shows on its face what the discarded
  reading would have cost. **(iii)** A tied pair `L_k = L_{k+1}` is graded on **both** levels, for
  published picks and for their distance-matched controls alike, through the identical `d_Lk`
  construction of §3. **Nothing else in this bullet moves:** the `d_L3 ≤ 0` limb is **not** widened
  to "any flattened level" (Q027 / Q031 verbatim, DP-26), and the `d_L3 ∈ [0.25, 10]` bound below
  stands as registered.
- **Validity bound** `d_L3 ∉ [0.25, 10]` ATR → excluded and counted (Q027 / Q031 §2.4 verbatim). It
  is a validity bound and nothing more. **The draft's claim that it "keeps the direction band strictly
  inside the magnitude level" is struck as false** (Correction 5): the bound admits `d_L3` between
  0.25 and 0.5, and §10 threat 6 states the position correctly. The bound is **not** raised to 0.5 —
  the residual conflation biases the *deferred* `V` toward zero, the direction that cannot manufacture
  a positive, and the screen is Q027's and Q031's verbatim (DECISIONS item 21, DP-45, DP-26).
  **Measured before the lock: 7 published picks of 550 excluded by the bound, and 20 of the 514 valid
  picks (3.89%) carry `d_L3 < 0.5`** (`STEWARD_Q033_exposure.md` §(d); DECISIONS item 31) — a fact
  about the ladder (PI-009 / H-053), never a licence to move the band after the fact.
- **Split-scale payload screen** (DATA_NOTES, the APH / KLAC / CRWD / MNST finding): excluded and
  counted if `lane_plans.day_trading.entry / C_t` is outside `[0.85, 1.15]` **and** a flattened lane
  level sits > 20 ATR from `C_t` (Q027 §2.4's joint screen, reused verbatim).
- **Missing forward bars** inside t+1..t+40 (halt, delisting) → ungradeable, excluded and counted; a
  measurement failure, never a classifier. A night is dropped if > 25% of its eligible picks are
  ungradeable.
- **Fewer than 60 daily bars dated ≤ t** for the pick or a control (ATR / beta60 / runup20 undefined)
  → excluded, counted. This is the screen that catches the CTRA truncated-history signature
  (`STEWARD_Q023_exposure.md` §6).
- **Immature nights** — session t+40 after the last trading date of the pinned price freeze →
  excluded and counted. Maturity comes from the trading calendar, never from whether a price exists;
  right-censoring is never graded as a non-touch.

### 2.5 Contributing night, tape-episode, symbol-episode

- **Contributing night (the floor unit, DP-21):** a non-excluded in-window night carrying **≥ 3 valid
  published picks, each with ≥ 5 valid matched controls**, matured to **t+40**. **The "carrying a
  legal §2.2 arm label" clause is struck** (DECISIONS item 25, Correction 12) — it served the deferred
  endpoint only. This is Q031 §2.5's series-B rule verbatim, and it is the rule the measured exposure
  rate in §5.1 was counted under (`STEWARD_Q031_exposure.md` §(a), re-confirmed for this population in
  `STEWARD_Q033_exposure.md` §(a)) — the rate and the rule are not allowed to drift apart. A night
  surviving the night-level filters but carrying no eligible pick is a **non-contributing night, not
  an exclusion**, and is printed in the funnel. **The direction series and the descriptive magnitude
  series contribute on exactly the same nights, from exactly the same picks and the same control
  sets**; there is no branch in which one has a night the other does not.
- **Tape-episode:** defined on the §2.2 arm label, so it **lapses with P2** — it is not computed, it
  gates nothing here (§8 clause 2 is P2's), and it appears in no bootstrap or permutation of the
  locked question. Its definition travels to `DEFERRED.md` with `V`: a maximal run of consecutive
  *sessions* carrying the same arm label, an excluded or unlabelled session not breaking a run, an
  episode counting toward the gate only if it contains ≥ 1 contributing night.
- **Symbol-episode (DP-51 only):** one symbol's run of *published-pick appearances* with gaps of ≤ 10
  sessions between successive appearances. It appears **only** in the §4.4 second CI; it never blocks,
  never gates and never defines a night.

## 3. Baseline(s) — what this must beat

- **B1 (rule-5 distance-matched control — inside both series by construction): the Q006 §3 B1
  construction verbatim.** For each eligible pick, the **10 nearest same-night non-published
  `sas_candidates` rows** on `beta60` / `atr_pct` / `runup20` computed from `prices_daily_split` bars
  dated ≤ t, standardized by the night's cross-sectional median and MAD, Euclidean distance, with
  replacement across picks, ties broken by symbol ascending. Each control carries **both** synthetic
  levels at the identical ATR distances and the pick's direction: the symmetric band
  `X_c ± 0.5 × ATR_c` for the direction series, and `L3_c = close_c × (1 + dir_p × d_L3,p ×
  atr_pct_c)` for the magnitude series — graded from the control's own t+1 open with exactly the §2.3
  rules, same direction, same 20-session clock. Controls **never add to inferential n** (rule 6). A
  pick with fewer than **5** valid controls is dropped and counted, **never imputed**; the measured
  cost of that floor on this population is **zero** (`STEWARD_Q031_exposure.md` §(b): pool depth min
  37, median 54, no night below 10).
- **B2 (P1's baseline, stated in H-081's own terms): the matched control's own direction rate.** "Y's
  rate when X did not happen" for a direction claim is: how often does a near-identical stock that SAS
  looked at and did not publish reach the same symmetric ATR band on the same side first? That rate is
  the second term of every `α_t` and is printed pooled and per half, with its own CI.
- **B3 (the deferred endpoint's arm baseline): the same slate on HOSTILE nights.** **Lapses with P2**
  and is not computed; there is no version of P2 without it, which is one reason `V` is deferred whole
  rather than demoted (DECISIONS items 9, 29).
- **B4 (the null the p-value is taken against): a paired sign-flip permutation on `α_t`**, 10,000
  permutations, seed 20260914. **The tape-episode label permutation lapses with P2** (Correction 13):
  with no arm there are no labels to permute.
- **B5 (descriptive, never a baseline for a verdict): the unadjusted rates.** The raw direction-race
  rate and the raw L3-touch rate of the published slate, pooled and per half, printed beside the
  control-adjusted numbers so the control's work is visible.

## 4. Objective metric (rule 5 — the price path, measured the way it is traded)

**Nothing in this question is decided by a fixed-horizon return.** Close-to-close returns at T+5,
T+20 and T+40 from `X`, and the sign of the 20-session move (H-081's filed direction proxy), are
printed and are **descriptive by rule 5 and DP-01**.

### 4.1 Per pick, per night

- **`a_p`** = 1 if `U` (the pick's own side of the symmetric band) is touched on some session in
  t+1..t+20 **strictly before** `D`, else 0. **A race that resolves the other way, and a race that
  never resolves inside 20 sessions, both score 0** and stay in the denominator (DECISIONS item 2 —
  a denominator that depends on the outcome is not an estimate of anything, and unresolved races
  dilute both rates toward each other and so toward `A = 0`). A same-session pair that hourly bars
  cannot order scores 0 (DP-27). **The unresolved share and the same-session-tie count print pooled
  and per half, for picks and controls separately, in every branch.**
- **`m_p`** = 1 if the regular-session high (bullish) / low (bearish) touches `L3` on some session in
  t+1..t+20, else 0. A gap through `L3` at a session open is a touch; a level at or through `X` at the
  t+1 open is not (§2.3).
- **`ctrl_a_p`, `ctrl_m_p`** = the means of the same two indicators over that pick's ≥ 5 matched
  controls, graded identically from each control's own t+1 open at the identical ATR distances.
- **`α_t = mean_{p ∈ P_t} [ a_p − ctrl_a_p ]`** — the night's **direction** excess, in rate units.
- **`μ_t = mean_{p ∈ P_t} [ m_p − ctrl_m_p ]`** — the night's **magnitude** excess, **descriptive in
  the locked question** (§4.3): it carries no q, blocks nothing and decides nothing, because the
  endpoint that contrasted it with `α_t` is deferred. This is Q006 §4's `Delta_t` on the DP-09
  20-session clock; it is the same series Q031 calls `S^B_t`, computed here from the pinned freezes by
  this question's own `eval.py` and never read from another question's `results/`. **`G_μ` — its
  arm contrast — is not computed at all** (DECISIONS item 27).

### 4.2 The primary endpoints

- **P1 (registered): `A = mean_t(α_t)`**, in percentage points, over the contributing nights of §2.5.
  Two-sided. **MPE ±5.0 pp** (DP-20; H-081's own number for each excess).
- **P2 (deferred at this lock, recorded as designed): `V = G_μ − G_α`**, where
  `G_x = mean_{t ∈ BENIGN}(x_t) − mean_{t ∈ HOSTILE}(x_t)`, in percentage points. Two-sided.
  **MPE ±10.0 pp.** `V` is a difference of two control-adjusted arm contrasts — one further difference
  than the difference-of-differences DP-20's larger-MPE clause was written for — and the desk's
  standing value for that shape is 10.0 pp (Q012 P2, Q018 P4, Q022 E1, Q023 E1). Registrar's one-line
  reason, as DP-20 requires: at ~100 nights a 5 pp bar on a triple difference returns INCONCLUSIVE by
  construction rather than by evidence. The MPE, the level lines and the equivalence NULL clause stand
  as designed and are **inherited verbatim by any successor** carrying `V` (DECISIONS items 8, 33).
  **No MPE and no level line is lowered at the decision pass in any branch**, including a branch where
  the MPE turns a CI-excludes-zero result into INCONCLUSIVE. That is what an MPE is for (rule 6).

**`m = 1`, fixed at lock** — P1 and nothing else (DECISIONS items 13, 27). BH within the question is
trivial at `m = 1` (`q = p`), and that loosens nothing: §7's larger-q rule corrects `A` across F1's
**28**-endpoint companion set, which dominates the within-question correction in every branch. **No
third endpoint is added at the decision pass**, and `V` is never added back — a lock fixes `m`.
P1 is registered as a primary and not merely as a precondition because "the platform predicts
direction" is a claim the platform makes on its own surfaces (`directional_pct`) and it must carry a
verdict of its own, including a NULL one.

**The level and label clauses `NO_EXCESS_TO_COMPARE`, `MAGNITUDE_IS_THE_CONDITIONAL_ONE`,
`BOTH_CONDITIONAL` and `BOTH_MOVE_TOGETHER` belong to P2 and lapse with it** (Correction 13). They are
recorded as designed in `DEFERRED.md` and are inherited verbatim by a successor. **No branch of this
locked question may use any of those labels**, and no result here may be described as H-081's PASS or
FAIL: `V` is unmeasured, and "both degrade together" is a statement about a contrast that was not
computed.

### 4.3 Secondary and sensitivity output

Everything here prints raw p only and is labelled *"descriptive, does not decide"* — **except the
two surviving named blockers**, which block a CONFIRMED verdict when they run the other way (§8
clauses 6 and 8). Suppression restricts **affirmative reporting only**: it never removes a blocker,
and a suppressed cell never by itself makes an endpoint INCONCLUSIVE. **Every read registered "per
arm" prints pooled and per half instead** (Correction 13).

**Computed, and blocking:**

- **Halves** — H-081's "the excess keeps its sign in every window", which with no arm is carried by
  the calendar halves alone. **Half A = window sessions 1–79, Half B = sessions 80–158**, fixed by
  session index at this lock and re-derived from the trading calendar (re-cut by the same rule if the
  extension fires, §5.2). **§8 clause 6**: the primary must carry the same sign in both halves, with
  neither half beyond MPE in the opposite sign. It **blocks at whatever count it has** and is not on
  the suppression list.
- **Bull-only** version of P1, with the direction mix per half — **§8 clause 8's opposite-sign
  blocker** (H-062: bear picks graded below base rate).
- **Lapsed with P2, computed nowhere:** the four stability cells and their `DIRECTION_STABLE` /
  `MAGNITUDE_STABLE` / `NEITHER_STABLE` labels (§8 clause 7), the nine-cell composition, the 80%
  HOSTILE composition guard (§8 clause 9) and **`G_μ`** (§8 clauses 3, 5 and the `G_μ` half of
  clause 8). None of them is suppressed — they are **uncomputable**, which is stricter (DECISIONS
  item 28).

**Computed, mandatory in the report, purely descriptive:**

- the **magnitude series `μ_t` itself** — its pooled level `M = mean_t(μ_t)` and its per-half levels,
  with CIs and night counts, printed beside `A` so the two halves of the pick's claim can be read side
  by side. **It carries no q, blocks nothing and decides nothing**, and it is **not** a second reading
  of Q006's endpoint: Q006 owns that level and decides it on its own date (§7);
- the **raw (unadjusted)** direction-race and L3-touch rates of picks and of controls, pooled and per
  half (B5), and the counter-side-first and unresolved-race shares for both;
- the **±1.0 ATR** direction band, and the **`C_t` entry basis** (DP-03(a) / DP-11), for both series,
  with not-takeable counts;
- **H-081's filed direction proxy** — the share of picks whose t+1-open-to-t+20-close move carries the
  pick's sign, minus the control's, pooled and per half — printed beside `A` so the two definitions
  can be compared, and **decisive in no branch** (rule 5, DP-01);
- **realised |move| in ATR against the printed target distance** (H-081's magnitude sentence): the
  distribution of `MFE_20 / d_L3` for picks and controls, pooled and per half, where `MFE_20` is the
  maximum favourable excursion in ATR from `X` within 20 sessions;
- the **40-session** companion of `μ` (the platform's own swing window, DP-09), which sits inside the
  binding maturity and is never right-censored;
- per-level **L1…L6 first-touch rates and sessions-to-touch** on each level's own lane window;
  **maximum adverse excursion** in ATR from `X`; counter-direction level touches (reported, never an
  exit — DP-02). **Every read whose lane window runs past t+40 — the long lane's L5 / L6 at 60
  sessions — prints its matured-night count beside it, and its right-censored rows are counted, never
  graded as non-touches** (Correction 6; §2.4's own rule). **No endpoint and no blocker depends on a
  bar after t+40**;
- the **joint distribution of `(a_p, m_p)` and their within-night correlation**, and the
  `d_L3`-tercile panel **as counts only** (suppressed from affirmative reporting) — the decision-pass
  half of §10 threat 6, whose pre-lock half measured `d_L3 < 0.5` in 3.89% of valid picks;
- the **platform's point-in-time regime label** (`market_regime_daily`, v1.2, `trading_date = t`),
  which **carries rule 7's stratification for this question** (DECISIONS item 26, Correction 14): `A`
  and `μ` are printed by label, **descriptively — the label defines nothing, blocks nothing and
  carries no q**, because that statistic on this population is Q023's locked E1 and is reported as
  part of the same non-independent set (§7). It is knowledge-time-legal for every night in this
  window (FREEZE_v001 §7: legal from 2026-06-09; the window opens 2026-09-15);
- **close-to-close returns** at T+5 / T+20 / T+40 from `X` — descriptive by rule 5, and no verdict
  sentence may lead with them.

**Sub-cells — the list is FIXED at lock and does not reopen at the decision pass.** The one permitted
revision from R1's measured counts was **exercised and closed at `record`: no cell was added and none
was removed** (DECISIONS item 28). A cell suppressed at lock stays suppressed even if it clears 20
measured nights at the decision pass; a cell not suppressed still needs ≥ 20 **measured** contributing
nights to print.

- **SUPPRESSED at lock:** the `90+` band (structural — `publication_floor = 80.0` since 2026-07-07 and
  2–3 elite picks a month, PI-010); **bear-only** as a *reported* cell (it blocks as the bull-only
  companion's complement but is not reported affirmatively); `confidence_level` terciles;
  `best_timeframe` cells; `d_L3` terciles; `atr_pct` terciles.
- **NOT suppressed:** the two halves; the 80–90 band (which is nearly the whole population — §10
  threat 4); bull-only; the `market_regime_daily` label cells (rule 7), each where it clears 20
  measured contributing nights.
- **Never on the list, because they block rather than report:** the halves and bull-only.
- **Left the reportable set entirely with P2, being uncomputable rather than suppressed:** the two
  arms, the nine `trend_t` × `vol_t` cells, the four stability cells and `G_μ`.

**Quotability:** 20- and 40-session bases → **every number in this question is `NON_QUOTABLE`**
(rule 12).

### 4.4 Inference

Night-level throughout; control rows never add to n (rule 6). **P1's inference is complete on its own
and is untouched by P2's deferral** (Correction 15). **Two CIs are reported and both must clear**
(DP-51):

- **CI-1 (registered, decides):** a **stationary block bootstrap** over the ordered contributing
  nights, expected block length **10 sessions** (the desk's standing value, fixed at lock and not
  chosen after seeing anything), 2,000 resamples, with a plain **date-clustered CI printed
  alongside**. The tape-episode block bootstrap lapses with P2 — it resampled arm labels that are not
  computed.
- **CI-2 (DP-51, decides jointly): symbol-episode-clustered bootstrap**, resampling symbol-episodes
  (§2.5) and nights jointly, 2,000 resamples. **Clearing MPE on CI-1 and not on CI-2 is INCONCLUSIVE,
  never CONFIRMED.** The threat is live: the same handful of symbols recur across consecutive nights
  with almost fully overlapping 20-session windows, and a 0.5 ATR race is decided early enough that
  one symbol's run can move the pooled mean on its own.
- **`α_t` and the descriptive `μ_t` are resampled together, night by night**, so the two series'
  printed intervals come from the same resamples (the same picks, the same controls, the same bars)
  and can be read side by side. `μ`'s interval decides nothing.
- **p-value (decides).** Paired **sign-flip permutation** on `α_t`, **10,000 permutations, seed
  20260914**. The tape-episode label permutation (§3 B4) lapses with P2.
- **Every estimate prints:** contributing nights total, per half and per rule-7 label cell;
  symbol-episodes and their length distribution; contributing nights dated after the lock commit;
  eligible picks per half; not-takeable counts; unresolved-race and same-session-tie counts; control
  rows used and picks dropped for < 5 controls; post-match standardized mean differences on `beta60` /
  `atr_pct` / `runup20`; exclusions by reason; matured-night counts beside every read running past
  t+40; seeds, resample counts and library versions.

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights** for the single primary endpoint,
  plus ≥ 20 per *reported* sub-cell. A sub-cell below 20 is **SUPPRESSED** — counts only, no point
  estimate, not even "small n, directionally" — and a suppressed sub-cell does not by itself make the
  endpoint INCONCLUSIVE. The weaker "80 eligible with ≥ 20 contributing" reading is not used (DP-21).
  **No floor is ever lowered to reach a date.** **Floor B (≥ 20 contributing nights in the rarer arm)
  and floor D (≥ 5 gate-counting tape-episodes per arm) are arm floors for `V` and travel to
  `DEFERRED.md` with it** (DECISIONS items 22, 23, Correction 16); §8 clauses 1 and 2 mark both
  "(P2 only)". The locked question carries **floor A** and **floor C** (DP-24's ≥ 30 post-lock nights,
  satisfied by construction).
- **Demotion (DP-43's clause): nothing to demote, settled at this lock and never afterwards.** The
  locked question has **no arm** — P1 is a pooled level — so no arm is projected below 20 contributing
  nights because no arm is projected at all, and the clause is recorded as exercised-and-empty
  (DECISIONS item 29). For P1's reported cells the ≥ 20 **measured** contributing-night floor stands
  unchanged and is applied at the decision pass, never at the lock. The arm-shortfall handling that
  was registered for `V` — a floor failure, the single DP-13 extension, then DEFERRED, **never** a
  demotion to descriptive and **never** an INCONCLUSIVE verdict — travels to `DEFERRED.md` with it.
- **Binding maturity: 40 sessions**, uniform across every eligible pick and every matched control —
  unchanged by P2's deferral, because μ's 40-session companion is a surviving §4.3 descriptive read
  and because t+20 is the option that would reach a date sooner (DECISIONS item 30, DP-45). It is the
  clock §5.2's dates and R2's bar horizon are computed on.
- **DP-24:** ≥ 30 contributing nights dated after the lock commit. Here **every** contributing night
  is post-lock by construction (§6), so DP-24 binds at 30 of the 80 and is not the gate.
  **PROSPECTIVELY_CONFIRMED is reachable from this run by design; DP-31 does not apply and no
  successor replication question is needed.**

### 5.1 Exposure — measured on this question's own funnel; no placeholder survives

Every row below is a **measurement on the pinned freezes**, read at `record` from
`research/reports/STEWARD_Q033_exposure.md` (R1, counts only, no live query — DP-50(c)). **The two
planning placeholders the draft carried — a 0.20 HOSTILE share of sessions and 3.0 rarer-arm
contributing nights per tape-episode — are STRUCK, not replaced** (Correction 17): they sized arm
floors that are no longer this question's, and the Steward's proxy arm numbers are **not** written in
as measured exposure for a partition the locked question does not compute.

| quantity | value used to size | status |
|---|---:|---|
| **contributing nights per elapsed session** (published slate, §2.5's rule verbatim) — **the scheduling rate** | **0.6620** | **measured**, `STEWARD_Q031_exposure.md` §(a) and re-confirmed on Q033's own funnel in `STEWARD_Q033_exposure.md` §(a) (47/71 at t+20-comparable maturity), pick nights 2026-06-01..2026-09-10 against `exclusions_v003`. Not the 0.9538 borrowed from Q023's narrower band funnel; the slower, measured rate is the one used (DP-45). |
| the same rule at **t+40** maturity over the sub-period that can be graded to t+40 | `r₄₀` = **0.8710** (27/31) | **measured**, §(a)(i) — faster than the cap, so it changes no date |
| **the rate the schedule is built on** | **`min(r₄₀, 0.6620) = 0.6620`** | DECISIONS item 6: no date is ever computed from a rate faster than the desk's own measured published-pick number (DP-43, DP-45) |
| full-denominator t+40 rate, for the record | 0.3803 | **measured**, §(a)(iii) — freeze-horizon censoring only, which cannot occur inside the registered window (R2 delivers t+40 bars for every in-window night) |
| control-pool depth (≥ 5 valid controls per pick) | min **37**, median 54, max 60 | **measured**, §(b) / `STEWARD_Q031_exposure.md` §(b) — the ≥ 5 floor's measured cost on this population is **zero nights at both horizons** |
| valid published picks per night (≥ 3 floor) | min 4 on contributing nights, median 8 | **measured**, `STEWARD_Q031_exposure.md` §(d) |
| picks excluded by the `d_L3 ∈ [0.25, 10]` bound / carrying `d_L3 < 0.5` | 7 of 550 / **20 of 514 valid (3.89%)** | **measured**, §(d) — §10 threat 6's pre-lock read (DECISIONS item 31) |

**Footnote on the funnel and §2.4's monotonicity screen.** The R1 funnel in
`STEWARD_Q033_exposure.md` §(a) (550 → 514 valid) applied **no** monotonicity or
`outcome_target_invalid` screen, so every rate above is an **upper bound** on the corrected
non-strict funnel by at most the ~41 true reversals and 4 `outcome_target_invalid` rows measured on
the same 550 (`STEWARD_Q034_exposure.md` §(b)), concentrated before the 2026-07-06 ship. Worst case
— all five nights carrying fewer than 7 valid picks lost — the rate is 0.5915, floor A binds at
session 135 of 158, and no date, floor call or branch changes (DECISIONS item 34).

**The SPY-history limb, and what it cost.** `manifest_prices_v001` carries SPY daily bars from
2026-01-31 only — 153 bars, 133 computable 20-session vol observations — so `SMA200` and the
250-session tercile exist **nowhere** in any pinned freeze, and the first session with ≥ 250 prior SPY
sessions is *never*. R1 limb (f) therefore probed whether the history could be fetched, and
**FAILED: `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` are both unset in the desk session and no retrieval
was attempted** (§(f); rule 1 forbids looking for any other credential). That fired DECISIONS item
16's registered branch — **P2 deferred, P1 locks alone**. The Steward's SMA50-only arm counts are a
**one-sided bound on a partition this question does not compute** and are recorded in `DEFERRED.md`
for the successor's re-measurement only; **they size nothing here, and the partition is never
re-specified to SMA50-only** (rule 3, DP-45).

### 5.2 Window, decision date, extension, DEFERRED fallback (DP-43, DP-13; no outcome is looked at)

**Window: pick nights 2026-09-15 .. 2027-04-30 inclusive = 158 elapsed sessions**, after exclusions.
**Decision date: Monday 2027-07-12.** Single DP-13 extension to **2027-06-14** (188 sessions,
DP-43's +30), decided **Monday 2027-08-23**, which is also the **hard stop**: still short there, Q033
goes to DEFERRED. **9.9 and 11.3 months from the 2026-09-14 lock**, both inside DP-43's 12-month
ceiling of 2027-09-14. These dates are **five weeks later than the draft's** for two arithmetic
reasons, both moving out and neither optional: the decision date is computed on the **40-session
binding maturity §2.3 and §2.5 register**, not on the primary's 20-session clock (Correction 1), and
the holiday list was missing **2027-06-18** (Correction 2).

**Floor projections at 158 sessions, on §5.1's measured rate:**

| floor | rate used | sessions needed | projected at 158 sessions |
|---|---|---:|---:|
| **A (binds):** ≥ 80 contributing nights for the primary (DP-21) | 0.6620/session (measured) | **121** | **104.6 nights** (31% headroom) |
| **C:** ≥ 30 contributing nights dated after the lock commit (DP-24) | 0.6620/session | 46 | **104.6** (all post-lock by construction) |
| **B:** ≥ 20 contributing nights in the rarer arm | — | — | **travels to `DEFERRED.md` with `V`** |
| **D:** ≥ 5 gate-counting tape-episodes per arm | — | — | **travels to `DEFERRED.md` with `V`** |

**Floor A binds and clears with 31% headroom on a measured rate. The window end is NOT pulled back to
session 121**: a shorter window is never chosen to reach a date sooner (DP-43, DP-45), and the
Steward's informational HOSTILE-richness reading that would have allowed it is a bounded proxy for a
partition this question does not compute. DP-13 still carries **one** pre-agreed automatic extension
and a DEFERRED fallback, both named below, firing on `eval.py`'s own measured counts and never on a
projection.

**Arithmetic, session by session** (holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18,
2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05 and 2027-09-06 — the last for the
12-month-ceiling back-solve only; the Steward re-confirms every date session by session from the
trading calendar when the freeze is built, and a correction may move a date **out, never in**):

- **Window.** 2026-09-15 is session 1. Sep 12 → 12 at 2026-09-30; Oct 22 → 34; Nov 20 → 54; Dec 22 →
  76 at 2026-12-31; Jan 19 → 95 at 2027-01-29; Feb 19 → 114 at 2027-02-26; Mar 22 (Good Friday
  2027-03-26 removed) → 136 at 2027-03-31; Apr 22 → **158 at 2027-04-30** (Friday).
- **Halves.** Half A = sessions 1–79 = 2026-09-15..2027-01-06; Half B = sessions 80–158 =
  2027-01-07..2027-04-30.
- **Decision date.** 2027-04-30 (Friday, session 158) **+ 40 sessions** binding maturity — May 3…May
  28 is 20 sessions (2027-05-31 Memorial Day removed), Jun 1…Jun 29 is 20 more (2027-06-18 Juneteenth
  removed) — = **2027-06-29**; **+ one calendar week** freeze margin = 2027-07-06 (Tuesday); first
  Monday on or after = **Monday 2027-07-12**, which is not a holiday. That is **9.9 months from the
  2026-09-14 lock**, inside DP-43's 12-month ceiling. `eval.py` is written once (rule 9) and run
  **once**, then. **No interim looks.**
- **`eval.py` is committed no later than Monday 2027-04-05**, sha256 recorded, and is not touched
  afterwards (DECISIONS item 14). The deadline is not a formality: **Q027 and Q029 decide 2027-04-12**
  on this window, this freeze, this entry and this 20-session clock, and a script written after that
  pass is a script written with part of its own answer in view (rule 9, rule 3). The extension run
  uses the **byte-identical, unmodified** file.
- **Extension (DP-13; DP-43's +30 sessions).** If a gate — 80 contributing nights, or 30 post-lock
  nights — is short at 2027-07-12 on `eval.py`'s **own measured counts**, the window extends **once**,
  automatically and with no new question, to pick nights **2026-09-15 .. 2027-06-14** (session 188),
  decision date **Monday 2027-08-23** (2027-06-14 + 40 sessions = 2027-08-11; + one week = 2027-08-18;
  first Monday on or after = 2027-08-23). 11.3 months from lock, still inside the ceiling. **The
  halves are re-cut on the extended window** by the same session-index rule (Half A = sessions 1–94 =
  ..2027-01-28, Half B = 95–188), fixed by that rule at this lock.
- **DEFERRED fallback (the hard stop).** If a gate is still short after that single extension, Q033
  goes to `research/questions/DEFERRED.md` with the measured counts rather than running under-powered.
  **No second extension, no reduced gate**, and **a gate shortfall is never an INCONCLUSIVE verdict**
  (§8).
- **Fixed at lock, not reopened at the decision pass:** the 0.5 ATR direction band and its coding; the
  `d_L3 ∈ [0.25, 10]` validity bound; the §4.3 suppression list (its one permitted revision was
  exercised and closed at `record`); the ±5.0 pp MPE and the ±5.0 pp level line; the block length; the
  seeds; the half-split rule; `m = 1`; and the fact that **P2 is deferred and its arm is computed
  nowhere**.
- **If a scoring or publication change ships mid-window** (§5.3 R2, §10 threat 8), the window is cut
  at the ship date, the **post-ship** segment becomes the question's window with this whole schedule
  recomputed from it — **out, never in**, subject to the same single extension and the same 12-month
  ceiling measured from the original lock — the pre-ship segment becomes a labelled descriptive panel
  entering no verdict, and if neither segment reaches the gates inside the ceiling the question is
  **DEFERRED** (DP-06, DP-50(a)). **Measured at the lock: R1(e) returned NONE** — HEAD unchanged at
  `d19c9a9`, no commit since manifest SHA `fa70688` touches the scoring path, the publication gates,
  the ATR-elite caps, the GEX offset, the scoring enable-flags or the lane-plan writer, and **no v1.7
  promotion is scheduled anywhere inside 2026-09-15..2027-08-23** (`STEWARD_Q033_exposure.md` §(e)).
  That is recorded as **an absence of a schedule, not a clearance**: no DP-06 / DP-50(a) split and no
  `DATA_NOTES.md` entry is owed today, and the sweep is **re-run at R2(vii)** between the freezes.

### 5.3 Routed requests

- **R1 → data-steward — counts only, no outcome of any kind, was BLOCKING FOR LOCK — ANSWERED AND
  CLOSED 2026-09-14.** Delivered as `research/reports/STEWARD_Q033_exposure.md`, all six limbs,
  measured on `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json` plus read-only
  `git log` / `git show` in the platform repo, **no live query** (DP-50(c)), over pick nights
  2026-06-01..2026-09-10. **No re-run is requested and nothing further is owed on R1.** What it
  returned, limb by limb, and what each settled:
  **(a)** §2.5's contributing-night rule confirmed as the rule `STEWARD_Q031_exposure.md` §(a) counted
  0.6620 under; `r₄₀ = 0.8710` on the t+40-gradeable sub-period, full-denominator t+40 0.3803, and
  **`min(r₄₀, 0.6620) = 0.6620` governs the schedule** (§5.1);
  **(b), (c)** the arm split, the tape-episode counts and the composition under the **SMA50-only**
  one-sided bound — **not §2.2-legal**, they gate `V` and **not** P1, and they travel to `DEFERRED.md`
  with it (DECISIONS item 23). Recorded there at their governing strict reading, including the
  rarer-arm episode rate **1/71 = 0.0141 against 0.025 — SHORT**, which is `V`'s **second, independent
  deferral ground**;
  **(d)** 7 of 550 published picks excluded by the `d_L3 ∈ [0.25, 10]` bound and **20 of 514 valid
  picks (3.89%) carrying `d_L3 < 0.5`** — §10 threat 6's pre-lock read; **the band stays 0.5 ATR and
  the bound stays [0.25, 10]**, unmoved in either direction;
  **(e)** the DP-50(a)/(b) commit sweep: **NONE**, HEAD `d19c9a9`, no v1.7 promotion scheduled through
  2027-08-23 (§5.2);
  **(f)** the **SPY-history feasibility probe** added as a limb of the lock gate (DECISIONS item 16):
  **FAIL — `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` both unset in the desk session, probe not
  attempted.**
  **The gate, as read:** the lock-or-DEFER inequalities were re-solved from the trading calendar at
  the registered **40**-session maturity (Correction 3 — latest admissible decision Monday 2027-09-13,
  back-solving through a one-week margin and 40 sessions to a last admissible window end of 2027-07-09
  and **205 admissible elapsed sessions**; the floors 80 / 20 / 5 divided by 205 and rounded up):
  contributing nights **≥ 0.40** per elapsed session, rarer-arm contributing nights **≥ 0.10**,
  rarer-arm gate-counting tape-episodes **≥ 0.025**. **Limb (a) — the only limb that gates P1 —
  PASSES at 0.6620 against 0.40, with 65% headroom, so Q033 locks.** The two rarer-arm limbs gate
  floors B and D, which are `V`'s, and travel with it. **Limb (f) short → P2 deferred at this lock,
  P1 locks alone**, exactly as item 16 registered the branch before the counts existed.
- **R2 → data-steward (due before the decision date; not a blocker for lock; DP-23) — OPEN, RESCOPED
  AT `record`.** The successor freeze pair named in the header, a **strict superset** of Q027's,
  Q029's and Q031's — one build serves all four:
  **(i) WITHDRAWN AND HELD WITH P2.** The SPY-split-adjusted-daily-bars-from-2025-01-02 requirement is
  **not built for Q033**: §2.2's arm is not computed by this question in any form, and the SMA50-only
  proxy is never substituted for it. If the H-074 trigger is met before the decision date the history
  is built for the **successor question that carries `V`**, never folded into this locked file.
  **(ii)** the daily bar horizon runs to **session t+40 of the last included pick night** — **daily
  bars through 2027-06-29**, delivered before **2027-07-12**; on the extension path only, through
  **2027-08-11** for **2027-08-23** (Correction 1: the contributing night is defined at t+40, never
  t+20);
  **(iii)** the daily symbol list covers **every candidate symbol on every in-window night, published
  and unpublished**, with ≥ 60 prior sessions before 2026-09-15 — never assumed from v001's list;
  **(iv)** hourly bars scoped to at least the published-pick symbols, **coverage stated explicitly**:
  they are **not** descriptive here — §2.3's same-session `U` / `D` ordering tie-break is **P1
  machinery** and an unorderable pair is scored counter-first (DP-27);
  **(v)** `market_regime_daily` with `created_at` preserved, **upgraded from a descriptive cross-check
  to the rule-7 stratification read and not optional** (DECISIONS item 26);
  **(vi)** an **add-only successor exclusions file** applying the identical four criteria to post-lock
  nights; it may add nights and may never remove one;
  **(vii)** rows whose bars are missing are **excluded and counted, never back-filled or imputed**,
  and R1(e)'s commit sweep is **repeated for the period between the freezes**, with a dated
  `DATA_NOTES.md` entry for any repair that rewrites historical rows and an explicit answer even when
  it is "none". **The DP-50(a) cross-freeze guard stays**, now on the candidate and control daily bars
  generally — where the successor freeze overlaps an earlier one, the rows are compared and `eval.py`
  **fails loudly** on any disagreement; **its SPY-specific limb lapses with (i)**.
  Every §5.2 date is re-confirmed **session by session from the trading calendar** when the freeze is
  built; a correction may move a date **out, never in**.

## 6. Test window, split and stratification

- **Test window: prospective only — pick nights 2026-09-15 .. 2027-04-30** (158 elapsed sessions;
  .. 2027-06-14 if the single DP-13 extension fires).
  *Justification.* The sealed period has already been read for this hypothesis — the standing
  `directional_pct ≈ base rate` finding, EXPLORE_001's in-sample per-level and speed reads, and
  H-081's own BACKLOG line stating what the desk expects — so those nights cannot referee it. They
  print once, as a **labelled post-hoc panel** (pick nights 2026-06-01..2026-08-12, every endpoint the
  locked question computes — `α_t`, the descriptive `μ_t`, the raw rates and the §4.3 per-level
  reads, **pooled and per half, with no arm, since none is computed**), **split at 2026-07-06** (the
  `_enforce_ladder_monotonic` ship, which changes the ladders `d_L3` is read from), entering **no
  verdict, no CI comparison, no half-stability test, no stratum test, no q and no §9 rule**, with its
  matured-night count printed beside every endpoint. Immature nights in the panel are counted, never
  graded as non-touches.
  The window sits entirely after the 2026-06-01 catalyst fix (DP-06), after the 2026-07-06 ladder
  commit and after the 2026-07-08 `publication_floor` change (DATA_NOTES), so none of the three splits
  DP-06 / DP-50(a) would force falls inside it.
- **Split for "the excess keeps its sign in every window" (H-081):** Half A = window sessions 1–79,
  Half B = sessions 80–158, **fixed by session index at this lock**, re-derived from the trading
  calendar and re-cut by the same rule if the extension fires (§5.2). The primary must carry the
  same sign in both halves (§8 clause 6). The halves are a **stability clause, not a reported
  stratum**: they block at whatever count they have. `in_sample_end = 2026-05-29` marks only what is
  excluded.
- **Regime stratification (rule 7).** The bar-only tape partition was rule 7's answer for both
  endpoints; with it deferred, **rule 7 is satisfied directly by its own words** — "stratified by
  `market_regime_daily` regime, and by the calendar split in the PREREG" (DECISIONS item 26,
  Correction 14). **`A` and the descriptive `μ` are printed by the platform's point-in-time
  `market_regime_daily` label**, which is knowledge-time-legal for every night in this window
  (FREEZE_v001 §7: legal from 2026-06-09; the window opens 2026-09-15) and which **defines nothing,
  blocks nothing and carries no q** — that statistic on this population is Q023's locked E1 and is
  reported as part of the same non-independent set (§7). **P1 is reported pooled, in both halves and
  in the label cells**, and §8 clause 6 binds the halves.
- **Knowledge time (rule 14) — every input declared. Q033 needs no rule-14 exception and requests
  none** (DP-05 untouched, DP-41 respected).

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction` | `sas_candidates` | pick night, 16:05 ET | population, strata, direction |
  | lane plans `L1…L6`, `analysis_status` | `sas_candidates.public_payload_json` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | `d_L3`, exclusions |
  | `C_t`, ATR14, beta60, atr_pct, runup20 | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | band width, distances, matching |
  | control-candidate pool (non-published rows for night t) | `sas_candidates` | pick night, 16:05 ET | B1 |
  | `market_regime`, `data_quality`, `regime_version`, `created_at` | `market_regime_daily`, v1.2 | declared 16:05 ET / lag 0, legal from 2026-06-09 (FREEZE_v001 §7) | **rule-7 stratification — descriptive, no q, blocks nothing** |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion |
  | session t+1 open `X`; daily bars t+1..t+40; hourly bars | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **entry and outcome measurement only** |

  **What `eval.py` must enforce:** the eligible-pick set, the control sets, the band and target levels
  and every stratum label are computed and written to a frozen per-pick and per-night table **before
  any post-pick-night bar other than the t+1 open is loaded**, and the t+1 open is used **only** to
  place `X`, `U`, `D` — never to filter, classify, match or stratify. The run fails if any
  t+1-or-later field is referenced in eligibility, matching or stratification. **It also fails loudly
  if any code path computes a §2.2 arm label, reads a SPY bar, or substitutes an SMA50-only proxy for
  either** — the arm is deferred, not approximated. `sas_selection_excursion` / `outcome_*` / `level_hit_*` columns are never inputs
  (calendar windows, close basis, recomputed weeks later — volatilx `services/sas_excursion.py:8-18`,
  `:336-354`; DATA_NOTES). `uoa_symbol_daily.fwd_return_*` is **banned** (FREEZE_v001 §5).

## 7. Multiple testing

- **Within the question: `m = 1`** (P1 alone), fixed at lock; BH within the question is trivial and
  `q = p` there. Every secondary in §4.3 prints raw p only, marked *"descriptive, does not decide"*;
  the two surviving blockers block without carrying a q. **No third endpoint is added at the decision
  pass, and `V` is never added back** — a lock fixes `m` (DECISIONS items 13, 27, 33).
- **Across the family: F8 System validity — `F8 = 1` at this lock and never below it.** The F8
  correction set is computed at the decision pass over the F8 questions locked by then: H-074 / Q030
  is DEFERRED and its primary leaves the set while deferred (the H-062 / Q025 precedent), and
  Q026 / Q028 are diagnostics with no primary.
- **Companion correction in F1 for `A`.** `A` is a picks-versus-matched-control path contrast built on
  Q006 §3 B1's construction, so — the Q015 / Q020 / Q029 / Q031 pattern — it is **additionally**
  BH-corrected across F1: Q006 (2) + Q024 (6) + Q025 (2) + Q029 (16) + Q031's `D1ᴮ` (1) + **Q033's
  `A` (1) = 28**. **Q032's `G` is not in the set:** Q032 was DEFERRED 2026-09-14 on the same
  Alpaca-provisioning blocker (`research/questions/DEFERRED.md`, "Q032 / H-079") and its primary leaves
  the companion set while deferred, taking F1 from 28 to 27 before `A` joins it. If Q032 ever
  re-enters and locks, `G` rejoins and this count rises with it. (One inherited inconsistency, flagged
  for the Red Team and not corrected here: `DEFERRED.md` "Q025 / H-068" records F1 without Q025's two
  primaries, while Q031 §7 (locked) counts them. **Q033 uses 28, the figure consistent with the locked
  file and the stricter of the two** — a larger BH set raises every q.)
- **F2 carries no Q033 endpoint while `V` is deferred: 17 → 16** (Q023 2 + Q027 2 + Q029's 10
  companion IC endpoints + Q031 2) — the H-062 / Q025 / Q032 precedent that a deferred primary leaves
  its family set. `V` rejoins F2 only if a successor registers it. **No locked PREREG records Q033's
  `V` in its correction set, so no locked file is edited.**
- **The larger of the two applicable q's is the one quoted and the one §8 clause 10 reads** — which is
  **F1's 28** in every branch, so `m = 1` loosens nothing.
- **`G_μ` is not computed at all** — it was P2's machinery — so §8 clause 8's `G_μ` half and the
  `G_μ` / `G` pairing lapse with the endpoint. **No branch of this question reports any tape-arm
  contrast of any series**, and nothing here may be read as evidence about tape conditionality: that
  is H-079's question, and it is unanswered today.
- Threshold: **q ≤ 0.10**, alongside raw p (rule 8).
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q006 (F1)** owns the *level* of `μ` — does selection beat the matched control at all, on the
    printed target. Q033 owns the *direction* level. **The descriptive `μ` printed here confirms,
    strengthens and weakens nothing about Q006**, and Q006's 2026-10-05 decision lands inside this
    window and **changes nothing here** — no MPE, no clause, no date.
  - **Q031 (F2)** asks whether `μ` decays **in time**; **H-079 / Q032** asks whether it is conditional
    on the tape and is deferred. Q033 as locked asks neither, and prints no statistic that could
    answer either.
  - **Q027 (F2)** shares this window, this entry and this clock and asks whether `overall_score`
    orders outcomes at all; a ranking edge and a direction edge are independent claims.
  - **Q023 (F2)** owns the platform-label regime contrast on the 80–90 band. That label is now this
    question's **rule-7 stratification** (§4.3, §6) — descriptive, carrying no q and blocking nothing
    — and the two are reported as **one non-independent set**: neither may ever be read as confirming
    the other (Correction 10, now without Q032's C1).
  - **Q009 / Q010 (F6)** own the L3-before-printed-stop race. Q033's race is symmetric at ±0.5 ATR
    from the entry, not the printed stop, and is a direction measurement rather than an exit rule
    (DP-02: nothing here is an exit).
  - **H-084 (F8, drafted as Q034)** pre-lists the 20-session direction excess among nine objectives as
    a **diagnostic with no primary, no MPE and no q**; it inherits this question's direction
    definition and adds no confirmation in either direction.

## 8. Decision rule (numeric, written before unsealing)

`A` is in **percentage points of control-adjusted own-side-first rate within 20 sessions from the t+1
open**, two-sided. **MPE ±5.0 pp** (§4.2); the level line is **±5.0 pp**. **No MPE and no level line
is lowered at the decision pass in any branch.** **Clauses 2, 3, 5, 7, 9 and the `G_μ` half of clause
8 are marked "(P2 only)" in their own text and LAPSE with the deferred endpoint** — they are not
computed, not printed and not read (Correction 13). The numbering is kept so that every
cross-reference in this file and in `DEFERRED.md` still points at the clause it named.

**HISTORICALLY_CONFIRMED** (for P1, the single primary) requires **all** of:

1. **contributing nights ≥ 80** and **≥ 30 dated after the lock commit** (DP-21, DP-24); plus ≥ 20
   **measured** contributing nights for any sub-cell that is *reported*. A sub-cell below 20 is
   **SUPPRESSED** (counts only) and does **not** by itself make the endpoint INCONCLUSIVE. The
   suppression list is fixed at lock (§4.3) and restricts affirmative reporting only: it never removes
   clauses 6 and 8's blockers, whatever their cell counts. **The ≥ 20-per-arm limb is P2's and is not
   carried here;**
2. **(P2 only — LAPSED) ≥ 5 gate-counting tape-episodes per arm.** Registered as a gate, never an
   INCONCLUSIVE verdict; it travels to `DEFERRED.md` with `V`;
3. **(P2 only — LAPSED) something to compare** (`NO_EXCESS_TO_COMPARE`);
4. the point estimate is **beyond its MPE** (`|A| > 5.0 pp`);
5. **(P2 only — LAPSED) the confirmed verdict's `MAGNITUDE_IS_THE_CONDITIONAL_ONE` /
   `BOTH_CONDITIONAL` label**;
6. the point estimate has the **same sign in both halves** (§6) and neither half is beyond MPE in the
   opposite sign — H-081's "reproduced with the same sign in every window", carried by the calendar
   halves alone now that the arm × half stability cells are uncomputable;
7. **(P2 only — LAPSED) the `NEITHER_STABLE` relabelling** on the four stability cells;
8. the **bull-only** version is not beyond MPE in the opposite sign. (The clause's `G_μ` half lapses:
   `G_μ` is not computed, and no branch of this question may report any tape-arm contrast as evidence
   of anything.);
9. **(P2 only — LAPSED) the 80% HOSTILE composition guard**;
10. **both CIs exclude 0** — CI-1 **and** CI-2 (DP-51). **Clearing MPE on CI-1 and not on CI-2 is
    INCONCLUSIVE, never CONFIRMED.** The permutation p (§4.4) supports it, and BH **q ≤ 0.10** within
    the question (trivially, `m = 1`) **and** in the F1 companion family of **28**, with the **larger
    q** quoted — which is F1's (§7).

- **NULL:** floors and clause 1 met, **both CIs include 0**, the point estimate is inside its MPE,
  **and both CIs lie entirely inside ±MPE** — the equivalence reading (DECISIONS item 3; without that
  precision clause, "no difference" can be declared from an uninformative interval). It is a
  deliberate one-way divergence from the house pattern: it makes a NULL **harder** to declare and can
  never make a CONFIRMED easier to reach. The reported NULL sentence — *"published picks are no
  likelier than their same-night look-alikes to go the way the pick said"* — carries its CI beside it,
  and is a real finding, ledgered with the same care as a positive.
- **INCONCLUSIVE:** anything else — the halves disagreeing in sign, the bull-only version beyond MPE
  in the opposite sign, an estimate inside MPE with a CI wider than ±MPE, an estimate beyond MPE with
  a CI including 0, or CI-1 and CI-2 disagreeing. **A gate shortfall is never INCONCLUSIVE** — not the
  80-night floor and not the 30-post-lock-night floor: each fires the single DP-13 extension, then
  DEFERRED (§5.2).
- **Question-level:** with one registered primary, the question's verdict **is** P1's verdict, on the
  single primary and nothing else. **H-081 is answered in half, and no branch of this run may be
  described as H-081 passing or failing**: its PASS was the conjunction of a confirmed direction level
  with a confirmed `V` labelled `MAGNITUDE_IS_THE_CONDITIONAL_ONE`, and `V` is unmeasured. The report
  says that plainly, in one sentence, wherever the verdict is restated.
- **What a confirmed `A` does and does not mean (binding on the report).** It means *"published picks
  reach a point 0.5 ATR in their own direction before a point 0.5 ATR against it, more often than
  same-night unpublished candidates matched on beta, volatility and run-up do at the identical
  distance, measured from the next session's open"*. It does **not** mean the picks rose, it does
  **not** mean they reached the printed target, and it does **not** mean money was made — `μ`, the raw
  rates and the T+20 returns are the numbers that speak to those and must be quoted beside it.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — it requires ≥ 30 contributing
  nights dated after this file's lock commit (DP-24, DP-21), which every contributing night here is,
  frozen in the successor manifests and never inspected earlier, reproducing the sign under the
  unmodified `eval.py`. The clause does not weaken. No subscriber-facing statement before that
  (rule 10); even then the basis is `NON_QUOTABLE` until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform prints a `directional_pct` grade and a six-level ladder on the same card, with no
statement that the two claims have different reliability and no control rate beside either. Rules
below fire **only** where §8 licenses them, and nothing subscriber-facing ships before
PROSPECTIVELY_CONFIRMED (rule 10). **Every P2 consequence is struck from this file with the endpoint**
(Correction 13): no lane rule, no tape-conditional target selection and no `V`-labelled sentence
follows from any branch of this run, because `V` is not measured.

- **P1 CONFIRMED positive (a real direction edge):** (a) a **guide line** in the Manual Trading Guide
  stating the measured own-side-first rate and the matched-control rate side by side, with their night
  counts; (b) a brief against `services/sas_conviction_card.py` adding a **matched-control column** to
  the direction claim, so a bare direction rate is never shown alone — the same treatment Q006 E1
  earns for the ladder; (c) an `INTERNAL_TOOL`, flag-off card field showing the pick's ±0.5 ATR band
  and the historical own-side-first rate at that distance (DP-48).
- **P1 NULL (no direction edge):** the platform's `directional_pct` surface is relabelled as a
  description of the tape rather than a skill claim, and the desk's own reporting stops describing a
  pick as "directionally right" without the control rate. This is the branch the desk expects
  (H-081's own line) and it is a result, not a non-result.
- **P1 INCONCLUSIVE:** nothing changes anywhere, and the report says so in one sentence.
- **In every branch, the report states that H-081's interaction half was deferred at the lock on a
  provisioning blocker** — not on evidence — and names `research/questions/DEFERRED.md` as where it
  lives. **No sentence in any output may describe this run as settling whether target attainment is
  the tape-conditional half of the claim.**
- **The suppressed cells license nothing.** No guide line, brief, flag or quoted number may cite the
  90+ cell, a bear-only cell, or any cell on §4.3's lock-time suppression list, whatever it shows.
- **Q033 is in flight from this lock until its decision date, and DP-50(b) applies to the platform in
  the meantime.** Any change to the SAS weights, the timeframe multipliers, `qualification_threshold`,
  the ATR-elite caps, the GEX offset, the scoring enable-flags, `publication_floor`,
  `bear_publish_threshold`, `max_output_cap`, `min_completeness` or the lane-plan writer — **including
  any promotion of the v1.7 score** — is **flag-off until 2027-07-12** (**2027-08-23** if the extension
  fires; Correction 1's dates, five weeks later than the draft's), the same clause Q027, Q029 and Q031
  carry, checked before any fix brief is written. If
  any listed change ships anyway it takes a dated `DATA_NOTES.md` entry naming the column, the date
  range and the ship SHA, and §5.2's window split applies (DP-06, DP-50(a)).
  **DP-49 binds every brief this question produces:** each check handed to the **coding agent** must
  be satisfiable from the platform repo alone — the test suite, a pure-function import, `git show
  --stat`, a file diff. Anything that reads or writes a table belongs in the brief's verification
  section, addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where a write is required;
  where a frozen manifest covers the affected table, the brief names that parquet as the
  before-snapshot rather than asking anyone to capture one (DP-50(c)).
- Owner: implementer. Shadow period before any flip: ≥ 20 trading days.

## 10. Known threats to validity (registrar's own list)

1. **A 0.5 ATR race is mostly beta and tape.** Over 20 sessions almost every liquid stock touches
   ±0.5 ATR; what P1 measures is which side comes **first**, and that is dominated by the market's own
   drift. The distance-matched control is the answer — it carries the identical band, in the pick's
   direction, on the same nights — but it removes the tape only to the extent of the three-feature
   match. Post-match standardized mean differences are printed per feature, and the raw rates are
   printed beside the adjusted ones (B5) so a reader can see how much work the control did.
2. **`V` is a triple difference and will be imprecise** — a threat that travels with the deferred
   endpoint, answered there by the ±10.0 pp MPE, the equivalence NULL clause, the joint night-by-night
   resampling and the DEFERRED route, and never by lowering the MPE.
3. **The rarer arm binds and projects marginal** — **struck from the locked question, which has no
   arm** (Correction 20). It travels to `DEFERRED.md` with P2, where it is recorded at its strictest
   measured reading.
4. **The population is nearly the whole traded book.** `publication_floor = 80.0` since 2026-07-07 and
   90+ is thin, so "the published slate" is in practice the 80–90 band. Every §9 sentence must say
   *"the published slate"*, never *"high-scoring picks"*, and the 90+ cell is SUPPRESSED at lock.
5. **Direction mix.** Bear publications are gated separately and their share moves with the tape, so a
   half-to-half comparison partly contrasts a bull-heavy book against a mixed one. Because bear picks
   grade *below* base rate in-sample (H-062), this pushes against the predicted sign — the
   conservative direction — but it is still a confound: the mix is printed per half and §8 clause 8
   makes the bull-only version binding.
6. **The band and the target must not be the same test.** If a pick's printed L3 sits close to 0.5
   ATR, `a_p` and `m_p` are nearly the same indicator. **Measured before the lock: `d_L3 < 0.5` in 20
   of 514 valid picks — 3.89%, about 1 in 26** (`STEWARD_Q033_exposure.md` §(d)). The `d_L3 ≥ 0.25`
   validity bound does not by itself prevent it and is deliberately **not** raised (DECISIONS item 21):
   the conflation biases the deferred `V` toward zero, the direction that cannot manufacture a
   positive. Its bite on the **locked** question is smaller still — P1 measures `a_p` against controls
   carrying the identical band, and a coincident `L3` does not distort that contrast. The joint
   distribution of `(a_p, m_p)` and their within-night correlation print at the decision pass, and the
   `d_L3`-tercile panel is computed as counts (suppressed from affirmative reporting). The 3.89% is a
   fact about the ladder (PI-009 / H-053), reported, and **never a licence to move the band after the
   fact** — a successor carrying `V` must restate it in its own §10.
7. **Band membership depends on a stored score that has been rewritten before.** `eval.py` re-derives
   each pick's band from `score_details_json` where the layer subscores are present and **fails
   loudly** on a disagreement with `overall_score` beyond 0.05.
8. **Config drift inside the window.** A change to the weights, publication gates or the lane-plan
   writer changes what "a published pick" or "its printed L3" means. Every item is named in R1(e) and
   repeated in R2(vii); `eval.py` prints the per-night `config_json` composition and **fails loudly —
   it does not silently exclude** — if an in-window night's scoring fields differ from those in force
   at lock.
9. **One database (DP-50).** A platform repair between freezes can rewrite the rows this question
   reads. The R2 cross-freeze comparison fails loudly on disagreement, now on the candidate and
   control daily bars generally (its SPY-specific limb lapsed with R2(i)).
10. **Overlapping 20-session windows** inflate precision, across nights *and* across the same symbol
    re-selected on consecutive nights. CI-1 handles the first, CI-2 (DP-51) the second, and both must
    clear. It bites harder here than usual: a 0.5 ATR race resolves early, so one symbol's run of
    selections can decide a large share of the pooled `α`.
11. **Not a threat but a realized event.** The SPY history the arm needs exists in no pinned manifest,
    it could not be fetched at the lock (`ALPACA_API_KEY` / `ALPACA_SECRET_KEY` both unset), and it
    **deferred P2 on the day the question was registered** — the third firing of the H-074 blocker in
    one day, after Q030 and Q032. It is a provisioning problem, not a measurement one, and no amount
    of waiting resolves it.
12. **Ladder and payload defects.** Null-ladder, non-monotone *in the platform's non-strict sense
    (ties allowed)* and split-scale payloads (DATA_NOTES) are excluded and counted; the question
    speaks only for published picks carrying a complete, *non-strictly* monotone, correctly-scaled
    swing target. The screen is the platform's own invariant, not a stricter desk variant; its
    measured pre-ship rate is 25.71% and its post-ship rate 0.00% (`DATA_NOTES.md`, steward Q018 R1),
    this window is entirely post-ship, and a material firing rate inside it is a platform-defect flag
    that stops the run, not a population this question describes.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-14), including the **2026-09-14 pre-lock addendum — item 34**
(§2.4's monotonicity screen is the platform's **non-strict** predicate `_ladder_is_monotonic`, with
the three guards, applied here as Correction 23 in §2.4, §5.1 and §10 threat 12). Routed items still
open: **R2** (the successor freeze pair, rescoped at `record`, due before 2027-07-12, blocking
nothing — DP-23). R1 is answered and closed (`research/reports/STEWARD_Q033_exposure.md`).
