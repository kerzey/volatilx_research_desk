# Q008 — fast_start_l4: when a pick held from the pick-night close reaches its first target within two sessions, is it more likely to go on to its fourth?

**Status:** DRAFT (lock by committing this file after Haci review; see "Decisions before lock" at the end)
**Family:** F4 Price behaviour after selection (hypothesis H-031; H-063 is **merged into Q007** — §7, DP-29)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v002.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates. See §2.
**Registered by:** registrar · **Approved by:** haci (pending lock) · **Date:** 2026-09-12 (decisions applied 2026-09-13)
**Decisions:** DECISIONS.md
**Human decisions recorded:** 2026-09-13 — Haci: (1) **Rule 14 exception, Q008 only** — bars through 16:00 ET on session t+2 may be used to assign the fast-start F/S label and nothing else (question A → recorded inside **DP-05(b)**; §6.1); (2) **window and decision date** — pick nights 2026-06-01..2026-10-23, decision **2026-12-28**, with one pre-agreed automatic extension and a DEFERRED fallback (question B → **DP-13**; §5, §8). Carried from 2026-09-12: entry basis = **pick-night close `C_t`** (**DP-11**, §4) and MPE for per-trade ATR endpoints = **0.25 ATR** (**DP-10**, §8).

---

## 1. Hypothesis (plain English)

**If a SAS pick you are holding from the pick-night close touches its first target (L1) within the
next two sessions, it is more likely to go on to reach its fourth target (L4) than a pick from the
same night that did not start that fast. It is also more likely to get there than a similar
unpublished stock that started equally fast toward targets set at the same distance. And holding for
L4 after a fast start is worth more than holding after a slow start.**

BACKLOG H-031 reads "L1 within 2 days → L4 probability". It names no entry basis, no clock, no window
for L4, no baseline and no control. This PREREG fixes all of those (§2–§4). The expected sign is
positive. Tests are two-sided, because "a fast start is exhaustion, so take profit" is an equally
tradeable answer.

This is a question about a position that is **already held** when the signal appears: the fast start
is a completed part of that position's price path. The entry is therefore the **pick-night
regular-session close `C_t`** (DP-11), for picks and distance-matched controls alike, and the
conditioning variable is read at a second decision point — the **close of session 2** — under the
rule-14 exception Haci granted for this question only (§6.1).

**Null (per primary endpoint):** within night, the L4 outcome after the session-2 close does not
differ between fast-start and other picks (K1). It does not differ between fast-start picks and
fast-start matched controls (K2). The realized result of holding for L4 does not differ between
fast-start and other picks (K3).

**Which endpoint can license a claim:** **K2 only** (DP-12; §4, §8). The conditioning variable is
itself part of the price path, so only the contrast matched on it — F picks against their control-F
sets at the same ATR distances — can support a SAS-facing claim, a card flag or a §9 platform change.
K1 and K3 are unmatched F-vs-S contrasts: they stay primary endpoints and stay in the BH set of
three, but on their own they license no rule, with one carve-out stated in §8 (a `playbook/` line
that says *stop holding* may rest on K3's absolute F-hold gate).

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first.
  Every estimator is a within-night difference, so the night's tape is held fixed.
- Source tables (manifest_v001 and its successor): `sas_candidates`: `qualified`, `selected_rank`,
  `qualification_reason`, `overall_score`, `dominant_direction`, `best_timeframe`,
  `public_payload_json` (lane plans). Also `sas_runs` (`finished_at`, used only for exclusions and as
  the `E_AH` clock in the §4 descriptive sensitivity).
- Source tables (manifest_prices_v001 and its successor): `prices_daily_split` (pick-night close,
  opens, forward highs/lows/closes, ATR14, beta60, run-up, SPY tape, trading calendar) and
  `prices_daily_raw` (split-factor snapping only). `prices_hourly_raw` is used for the descriptive
  counter-level tie-break and the descriptive `E_AH` entry sensitivity only (§4). It covers published
  symbols only (research/lib/freeze_prices.py:17, :117).
- **Treatment rows (published picks), exact predicate:**
  `qualified IS TRUE AND selected_rank IS NOT NULL` (**DP-28**). This is the platform's own exposure
  predicate (volatilx `services/sas_conviction_card.py:105`, `:308-309`).
  **This deliberately differs from Q002/Q004/Q006's `selected_rank IS NOT NULL`.** Since the
  2026-07-02 dark-lane decision, the platform ranks a "dark" top-cap with `selected_rank` set and
  `qualified = FALSE`, `qualification_reason = 'selected_dark'`. Those rows are scored and graded
  but never published (volatilx `services/super_agent_select_scoring.py:1503-1508`, `:1539-1546`).
  FREEZE_v001 §1 counts 915 rows with `selected_rank` against 907 qualified; the Steward counted
  **8 dark-lane rows** inside this question's sealed window (STEWARD_Q008_exposure.md §(e)).
  **Dark-lane rows are excluded from the treatment set** — they were selected by SAS, so they are not
  a published pick — **and their count is printed.** They are **not** excluded from the control pool
  (next bullet).
- **Control pool, night t: the complement of the publication predicate** — every same-night
  `sas_candidates` row for which `NOT (qualified IS TRUE AND selected_rank IS NOT NULL)`, i.e.
  `qualified = FALSE` rows **and dark-lane rows alike** (DP-28; rule 5's "unpublished candidates from
  the same night"; the Q007 §3 / §R5 construction). Dark rows are unpublished candidates, and a
  control pool that contains SAS's own strong-but-dark names raises the bar rather than lowering it.
  Each pool row also needs ≥ 60 prior split-adjusted bars (beta60), ≥ 21 bars (run-up) and ≥ 40
  forward sessions in the pinned freeze. Steward count in the sealed window: **3,408 control-pool
  rows, of which 3,391 usable for matching** (§(e)).
- **Levels, exact:** from `public_payload_json.lane_plans`, the platform's own mapping
  (volatilx `services/sas_conviction_card.py:182-187`, `:246-258`):
  **L1 = `day_trading.targets[0]`**, **L4 = `swing_trading.targets[1]`**. L2 and L3 (for descriptive
  order-of-hit) are `day_trading.targets[1]` and `swing_trading.targets[0]`.
  Windows are the platform's: L1/L2 = 20, L3/L4 = 40 trading sessions
  (`_LADDER_LEVEL_WINDOW`, `:194`). **L4 on its own 40-session swing window is the primary clock**
  (DECISIONS.md item 12): **DP-09 is not extended to L4** — DP-09 is scoped to L3 as the primary
  level, and Q008's clock does not differ from the platform's lane window, so no R-2 arises.
- **Notation (all prices in the signal-date split basis):**
  - `C_t` is the pick's **actual** regular-session close on pick night t, from `prices_daily_split`.
    It is never the platform's `spot_close`, which is stale on re-run nights (DATA_NOTES).
  - `dir` = +1 (bullish `dominant_direction`) / −1 (bearish).
  - `ATR_p` = mean of the last 14 true ranges ending at t, from `prices_daily_split`. `atr_pct_p` =
    `ATR_p / C_t`. The platform's `atr_pct` is corrupted around splits and is not used
    (DATA_NOTES).
  - Sessions `s = 1, 2, …` are the trading sessions after t, from SPY bars. `s = 1` is t+1.
    `O_s`, `H_s`, `L_s`, `Cl_s` are the open, high, low and close of session s.
  - `d1 = dir × (L1 − C_t) / ATR_p` and `d4 = dir × (L4 − C_t) / ATR_p` are the ATR distances from
    the entry price.
- **Exclusions (each counted and printed in the results header, never silently dropped).** The
  Steward's counts on the sealed window (STEWARD_Q008_exposure.md §(e)) are given for audit; `eval.py`
  recomputes all of them.
  - Nights in **`research/data/exclusions_v002.json`** — `manual_runs.trading_dates` ∪
    `non_session_runs.trading_dates` (DP-22). On those nights the frozen candidate rows are not the
    16:05 ET output (a manual re-run, or a run dated on a non-session day), so a pick-night entry is
    not definable. `eval.py` reads the JSON and takes that union; **no date is hard-coded in this
    PREREG or in `eval.py`.** Two of the ten excluded dates fall inside the sealed part of this
    window — **2026-07-02 and 2026-07-06** — leaving **67 non-excluded nights 2026-06-01..2026-09-08**
    on the Steward's count (STEWARD_Q008_exposure.md §0). No night total is hand-counted here; the
    printed figure is the one `eval.py` derives from the JSON.
  - Any prospective night whose `finished_at` is later than the next session's open. This is the
    same criterion as `manual_runs`, applied mechanically, not by judgment.
  - Dark-lane rows, from the treatment set only (see above). *Sealed count: 8.*
  - **Null-ladder picks:** no `lane_plans`, or no L1 or no L4 price. FREEZE_v001 §3 counts 17 of
    915 selected rows with no ladder row at all. Excluded and counted. *Sealed count: 14.*
  - **Void levels at the entry price:** `d1 ≤ 0` or `d4 ≤ 0`. This is the platform's void rule
    (volatilx `services/sas_reference.py:199-227`) applied to the actual close, and it is also rule
    5's "a target already passed at entry is not a hit", evaluated at the entry basis `C_t`
    (DP-11; DP-26). Excluded and counted. *Sealed count: 6.*
  - **Non-monotone ladder:** `d4 ≤ d1`. Lane targets are written per lane by an LLM relative to
    each lane's own entry (volatilx `ai_agents/principal_agent.py:548-554`). The platform states
    that "levels are not strictly price-ordered across lanes" (`services/sas_conviction_card.py:289`).
    "L1 then L4" only means something when L4 lies beyond L1. Excluded and counted, and the share is
    a headline number. *Sealed count: 1.*
  - Mixed-direction picks (`dominant_direction` neither bullish nor bearish). *Sealed count: 0.*
  - **Immature:** fewer than 40 forward sessions in the pinned freeze. Excluded and counted.
    Right-censoring is never graded as a non-touch.
  - Missing-bar or delisted symbols are dropped and counted (missing `C_t` or 14-bar ATR history;
    missing session-1/session-2 bars — *sealed counts: 0 and 0*). A night is dropped if > 25% of its
    eligible picks are missing bars.
- **Path classification at the entry price and at the decision clock (per pick; controls
  identically, §3):**
  - Entry basis: **pick-night regular-session close `C_t`** (§4; DP-11). A level at or through `C_t`
    is not a hit — that is the void rule above, applied before any session-1 bar is read.
  - **F (fast start):** L1 is touched in session 1 or session 2. Touched means `H_s ≥ L1` for bullish
    or `L_s ≤ L1` for bearish, for some s ∈ {1, 2}. **A gap through L1 at the t+1 open is a session-1
    touch**, because the position has been held since `C_t` and the overnight move is part of its
    path (DECISIONS.md item 6; DP-25, DP-26). There is no "gapped through" carve-out and no
    "passed at the open" exclusion; rule 5's passed-at-entry rule bites at `C_t` and nowhere else.
  - **S (no fast start):** L1 is not touched in sessions 1–2. F and S partition the eligible picks.
  - **E4 (L4 already touched by the decision clock):** L4 is touched in session 1 or 2 (necessarily
    an F pick). Excluded from the primaries, counted, and its share of F reported. Such a pick has
    nothing left to decide at the clock. *Sealed count: 24.*
  - **Decision clock `D` = the close of session 2** (16:00 ET, session t+2). Everything that defines
    F / S / E4 uses bars up to and including session 2 — the sole rule-14 exception, §6.1. Every
    outcome is measured strictly after it.
- **Population funnel, as measured by the Steward on the sealed window (frozen data, counts only;
  STEWARD_Q008_exposure.md §(e), 2026-09-13; `eval.py` reprints it for the full window):** 543
  published rows on 67 non-excluded nights → 529 after no-ladder (−14) → 529 after direction (−0) →
  529 after missing `C_t`/ATR (−0) → 523 after void at `C_t` (−6) → 522 after non-monotone (−1) →
  522 after missing session-1/2 bars (−0). Of those **522 eligible** picks: **291 eligible F**,
  **207 eligible S**, **24 E4** set aside and counted.
- **Contributing nights (the unit that counts toward the floors, DP-21; DECISIONS.md item 4):**
  - **K1 and K3:** a night with **≥ 1 eligible F pick and ≥ 1 eligible S pick**.
  - **K2:** a night with **≥ 1 eligible F pick whose control-F set is non-empty** (§3 B2 step 4) —
    the matched-control validity is part of "contributing" (the Q007 item-18 definition).
  A night that carries only one side contributes nothing to that endpoint; it is counted and
  reported and is **not** a contributing night for it.

## 3. Baseline(s) — what this must beat

- **B1 (the backlog baseline, "Y's rate when X did not happen"):** S picks from the **same night**,
  entered on the same basis and graded identically. Used in K1 and K3. An unmatched contrast
  (§8; DP-12).
- **B2 (rule 5 distance-matched control):** the Q006 §3 construction, anchored at the close,
  unchanged except for the conditioning step:
  1. For each eligible pick p on night t, compute `beta60`, `atr_pct` and `runup20` at the
     pick-night close from `prices_daily_split` bars dated ≤ t. Standardize by the night's
     cross-sectional median/MAD over the control pool plus that night's picks. Take the **10 nearest**
     control-pool rows (§2: the complement of the publication predicate) by Euclidean distance, with
     replacement across picks, ties broken by symbol ascending. Control pool and matching are fixed
     with inputs available at 16:05 ET on the pick night; a matched control later found to lack
     forward bars is **not** replaced by the next-nearest candidate — it is dropped from that pick's
     control set and counted.
  2. Synthetic levels for control c: `L1_c = C_{t,c} × (1 + dir_p × d1_p × atr_pct_c)` and
     `L4_c = C_{t,c} × (1 + dir_p × d4_p × atr_pct_c)`. These are the same ATR distances in the same
     direction, measured from the control's **own** pick-night close — the same entry basis as the
     pick (DP-11), which is what makes the contrast legal under rule 5.
  3. Each control is classified **F / S / E4** from **its own** bars in sessions 1–2 by the §2 rules,
     against levels anchored at its own close. A gap through `L1_c` at the control's t+1 open is a
     session-1 touch, exactly as for picks.
  4. **Control-F set of p** = p's matched controls that are F and not E4. A pick with an empty
     control-F set is **excluded from K2 and counted** — never back-filled, never substituted with
     the unmatched B1 contrast (DP-12). That count is a headline number (§10 threat 2); on the sealed
     window it is **2 of 291 F picks (0.7%)** (STEWARD_Q008_exposure.md §(c)).
  5. Control rows never add to inferential n (rule 6).
- **B3 (descriptive):** all same-night control-pool rows that are F, unmatched, with synthetic levels
  at each pick's distances. This shows how much of any K2 gap is composition.

## 4. Objective metric (rule 5 — price path, measured the way it is traded)

**Entry basis: the rule-5 pick-night after-hours entry, measured at the pick-night regular-session
close `C_t` (`prices_daily_split`), for picks and controls alike** (DP-03(a) via **DP-11**; Haci
2026-09-12: *"I want to measure the movement of the stock from closed price of previous day not
opening prices"*; DECISIONS.md item 10). The close is the proxy for the after-hours fill: only the
close exists for the unpublished control candidates, and rule 5 requires one basis on both sides.
A level at or through `C_t` is **not** a hit (§2 void rule). Touches use regular-session daily highs
(bullish) / lows (bearish), split factors snapped, from session 1 onward — so a gap through a level
at a session open is a touch on that session. **Stops are not assumed** anywhere in the primaries.
Adverse moves are measured and reported, never used as exits.

**Descriptive entry sensitivity (picks only, never decides; required by DP-11):** the same endpoints
recomputed from the real after-hours price `E_AH`, using **Q004's definition verbatim** — the close
of the first `prices_hourly_raw` bar whose bar end is at or after that night's `sas_runs.finished_at`
and strictly before the next regular open, converted to the signal-date split basis; picks without
such a bar are excluded from the sensitivity and counted. It bears mainly on the void /
passed-at-entry filter and on `d1`/`d4`. No control is available on that basis, so the sensitivity is
a raw arm contrast only, and it never decides.

**Outcome `Y`** = 1 if L4 is first touched in sessions **3 through 40** inclusive, else 0. This is
L4's own 40-session lane window counted from the entry, minus the two sessions that define the
condition.

**Primary endpoints (three, pre-specified, BH-corrected within this question):**

- **K1 — conditional lift (H-031 as written).** *Unmatched contrast; licenses no rule on its own
  (DP-12; §8).*
  Per contributing night t (≥ 1 eligible F and ≥ 1 eligible S pick):
  `Δ1_t = mean_{p∈F,t}(Y_p) − mean_{p∈S,t}(Y_p)`. Estimand: `mean_t Δ1_t`, in percentage points.
- **K2 — continuation beyond distance (the rule 5 control applied to the fast-start hit rate).**
  For each F pick p with a non-empty control-F set: `x_p = Y_p − mean_{c∈control-F(p)}(Y_c)`.
  Per contributing night t (≥ 1 such pick): `Δ2_t = mean_p(x_p)`. Estimand: `mean_t Δ2_t`, in
  percentage points.
  **K2 is the DP-12 primary: the conditioning variable is part of the price path, so only a contrast
  matched on it can license a rule; K1 and K3 are unmatched contrasts and are read under §8's table.**
  K2 as defined here (F pick minus its control-F mean) satisfies DP-12; it is **not** promoted to a
  double difference — the difference-in-differences stays a secondary below.
- **K3 — the money: realized result of holding for L4 from the decision clock.** *Unmatched
  contrast; licenses no rule on its own except through the absolute F-hold gate carve-out (§8).*
  **Plan E-HOLD4:** the position is held from `Cl_2` (the close of session 2). It exits at the first
  touch of L4 in sessions 3..40 at the L4 price. If a session **opens through L4**, the exit is that
  session's open, because a resting limit fills at the better price. If L4 is not touched, the exit
  is `Cl_40`. There is no stop.
  For pick p: `r_p = dir × (exit_p − Cl_2) / ATR_p` (ATR units).
  Per contributing night t (≥ 1 eligible F and ≥ 1 eligible S pick):
  `Δ3_t = mean_{p∈F,t}(r_p) − mean_{p∈S,t}(r_p)`. Estimand: `mean_t Δ3_t`.
  K3 is deliberately **not** control-adjusted. It is the hold-or-flatten decision as a trader faces it
  at the session-2 close. K2 is the mechanism. K3 is the trade. K3 is measured strictly **after** the
  clock, so the conditioning move is not inside it and no displacement offset is available or needed.
  **Gate reported with K3 (pre-specified, used in §8):** `mean_t mean_{p∈F,t}(r_p)`, the absolute
  expectation of holding after a fast start, with its 95% CI.

**Secondary, descriptive, never decides:**
- **Proximity check:** the remaining distance at the clock,
  `rem_p = dir × (L4 − Cl_2) / ATR_p`, for F vs S picks and for F picks vs control-F. Also K1 and
  K2 recomputed within night-pooled terciles of `rem`. This asks whether a fast start carries
  information beyond where price is sitting at the clock, which the raw K1 cannot separate.
- **Difference-in-differences:** K1 on picks minus the same F-vs-S lift computed on matched
  controls.
- **Gapped-through-L1 split of F:** the L4 rate and E-HOLD4 result for F picks whose session-1 touch
  of L1 was an opening gap, printed beside the rest of F (§10 threat 3). E4 share of F.
- Clock sensitivity: the fast-start definition at 1 session and at 3 sessions (outcome window moved
  to start the session after the clock).
- Outcome sensitivity: L4 within sessions 3..20 (NON_QUOTABLE) and, where matured, 3..60.
  L3, L5 and L6 as outcomes after a fast start (L5/L6 on their 60-session windows, matured nights
  only).
- **Order of hits after the clock:** the share of F picks whose sequence runs L2 → L3 → L4, and the
  share where the swing counter level is touched before L4. Counter levels use the swing lane `stop`
  from `lane_plans` (the platform's synthetic counter tier, volatilx
  `services/sas_excursion.py:301-332`). Also the report-blob counter targets from
  `sas_excursion.counter_levels_json` where present (`:269-287`, `computation_version = 'v2'`),
  **prices only, never its touch dates**, which are on calendar windows (`:8-18`). Touches are
  recomputed from the price freeze. A same-session tie between a counter level and L4 is broken with
  hourly bars for picks; **any tie that hourly bars cannot order — and every control tie, controls
  having no hourly bars — is counted counter-level-first (DP-27), the outcome less favourable to the
  hypothesis, with the TIE count printed separately.** TIE is never a third category in a printed
  share.
- Adverse excursion from `Cl_2` before L4 (or to session 40), in ATR units. Also the share touching
  `Cl_2 − dir × 1.0 × ATR_p` before L4.
- **Committed scale-out plan, reported next to the hit rates (rule 5):** the band schedule
  `BAND_EXITS` (volatilx `scripts/generate_sas_trading_guide.py:89-95`; 80–85 `10/15/30/15/20/10`,
  85–88 `0/15/30/15/25/15`, 88–90 `0/10/25/15/30/20`, 90+ `0/0/10/20/30/40`). It is entered at
  `C_t`, each fraction exits at its level's first touch from the entry (at the level price, or the
  better open if a session opens through it), and fractions whose level was at or through `C_t` are
  recorded as unfillable. The remainder is closed at `Cl_40` (truncated and labelled so). The
  trailing rules are not deterministic enough to simulate and are ignored. `<80` is not traded per
  the guide. Reported for F vs S, in ATR units and percent.
- The platform's close basis (`entry_ref`, volatilx `services/sas_excursion.py:336-354`) version of
  K1, for comparison with anything the platform displays.
- Close-to-close return from `C_t` at T+10 and T+40 (secondary by rule 5).

**Quotability:** 40-session basis → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** All at night level.
- **CI (decides):** stationary block bootstrap over the ordered contributing nights, expected block
  length **20 sessions** (40-session forward windows overlap across adjacent nights; same choice as
  Q006 E1), 2,000 resamples. The date-clustered bootstrap CI is printed alongside.
- **p-values:** for K1 and K3, within-night label permutation: on each contributing night, the F/S
  labels are shuffled among that night's eligible F+S picks and the estimand is recomputed exactly.
  For K2, a paired sign-flip permutation on `Δ2_t`. Both use 10,000 permutations and seed 20260912.
- Every estimate prints n(contributing nights, on that endpoint's own definition), n(F picks),
  n(S picks), n(E4), n(control rows), n(control-F rows), n(F picks dropped from K2 for an empty
  control-F set) and n(excluded, by reason).

## 5. Sample floors and expected n

- **Floors (rule 6 read per DP-21; DECISIONS.md item 4):**
  - ≥ **80 contributing nights for each primary endpoint**, each counted on **its own** definition
    (§2): K1/K3 = nights with ≥ 1 eligible F and ≥ 1 eligible S pick; **K2 = nights with ≥ 1 eligible
    F pick whose control-F set is non-empty**. A shortfall on one endpoint is never covered by
    another endpoint's count. The weaker reading — "80 eligible nights with ≥ 20 contributing" — is
    not used (DP-21).
  - ≥ **20 contributing nights** per reported sub-cell. Cells below 20 are **SUPPRESSED**: no point
    estimate is printed.
  - **No floor is ever lowered to hit a date** (DP-21), and a short K1/K3 count never licenses
    reading K1 off a K2-sized sample or falling back to the unmatched contrast (DP-12).
- **Measured exposure (Data Steward, research/reports/STEWARD_Q008_exposure.md, 2026-09-13 — frozen
  data, counts only; no L4 touch beyond what sessions 1–2 require, no return, no outcome, and no
  picks-minus-control difference on the L1 event).** Population: published picks under the §2
  predicate on non-excluded nights (`exclusions_v002.json`), pick nights 2026-06-01 through the
  **2-session classification maturity** of `manifest_prices_v001` (last such night 2026-09-08) —
  deliberately **not** the 40-session outcome maturity, which is a pure calendar shift and would
  leave ~28 nights. These are exposure counts for the classification; the 40-session outcome
  maturity is supplied by the successor price freeze at the decision date.
  - **67 non-excluded nights** 2026-06-01..2026-09-08 (§0); 543 published rows → **522 eligible**
    after the §2 funnel; **291 eligible F, 207 eligible S, 24 E4** set aside (§(e)).
  - **K1/K3 contributing nights: 59.** **K2 contributing nights: 64.** Floor 80 (§(a), §(b)).
  - Control-F set size per F pick: median 7, 10th percentile 4, minimum 0; **empty for 2 of 291
    F picks = 0.7%**, so the matched contrast exists for **99.3%** of F picks on frozen data (§(c)).
  - Monthly contributing rate (K1/K3): 76.2% (Jun) / 90.0% (Jul) / 100.0% (Aug) / 80.0% (Sep,
    5 nights only); overall **88.1% (K1/K3)** and **95.5% (K2)** (§(d)).
  - Projected to reach 80 contributing nights ≈ **2026-10-12 (K1/K3)** and ≈ **2026-10-01 (K2)**;
    projected cumulative by 2026-10-23 ≈ **83.7 (K1/K3)** and ≈ **90.7 (K2)**; projected **new**
    contributing nights 2026-09-16..2026-10-23 ≈ **24.7 / 26.7**, and 2026-09-16..2026-11-30
    ≈ **46.7 / 50.6** (§(d)). These are mechanical extrapolations of a run-rate, not forecasts; every
    gate below is evaluated on **measured counts printed by `eval.py`**, never on a projection.
  - *Distinction from Q002, stated so no reader conflates them:* this F/S classification is measured
    from `C_t` with the void rule at `C_t`; Q002's primary endpoint S1 is the unconditional
    L1-within-2-sessions rate measured from the **next-session open** with `passed_at_entry` picks
    excluded on that basis. Different event, different denominator; the Steward computed no
    picks-minus-control L1 difference anywhere (§7, §10 threat 14).
- **Calendar arithmetic (labelled as such; not an expected n):** the drafted window holds roughly
  100 non-excluded sessions — the 67 above plus the sessions 2026-09-09..2026-10-23, before any new
  prospective exclusion. It is the calendar size of the window, not a projection of contributing
  nights; the expected-n figures are the Steward's, above.
- **Window and decision date (Haci 2026-09-13, question B, option 1 → DP-13; no outcome looks at any
  point):**
  - **Primary window:** pick nights **2026-06-01..2026-10-23** inclusive, after exclusions.
    **Decision date: Monday 2026-12-28.** The 40th session after 2026-10-23 is 2026-12-21
    (Thanksgiving 2026-11-26 closed); the decision date adds the freeze margin. `eval.py` is written
    once (rule 9) and run on successor freezes whose as_of is ≥ 2026-12-21. **No interim looks.**
  - **Both gates, per primary endpoint, on measured counts.** Evaluation proceeds only if **every**
    primary endpoint — K1, K2, K3, each on its own contributing-night definition — has
    **≥ 80 contributing nights** and **≥ 25 contributing nights dated after this file's lock commit**
    (§8 clause 1). The gates are checked on the **actual counts printed by `eval.py`** from the frozen
    data, never on a projection, a run-rate or an expectation.
  - **One automatic extension.** If any gate is short at 2026-12-28, the window extends **once**, with
    no further question to Haci, to pick nights **2026-06-01..2026-11-30**, decision date
    ≈ **2027-02-03** (40 sessions after the last pick night plus the same freeze margin the primary
    date uses; the Steward fixes the exact session-count date when building the successor freezes,
    R2). The extended run uses the **unmodified `eval.py`** and the same gates.
  - **DEFERRED fallback.** If any gate is still short after that single extension, Q008 goes to
    **DEFERRED** (`research/questions/DEFERRED.md`, with the measured counts) rather than running
    under-powered. There is no second extension.
  - **Nothing weakens.** Neither gate is ever reduced, no floor is lowered to hit a date (DP-21), and
    a short K1/K3 count never licenses falling back to the unmatched contrast (DP-12). A gate
    shortfall is **not** an INCONCLUSIVE verdict — it triggers the extension, then DEFERRED (§8).
- **Freeze discipline (DP-23; routed request R2, due at the decision date and not a blocker for
  lock).**
  - Selections for nights ≤ 2026-09-10 stay pinned to `manifest_v001` / `manifest_prices_v001`.
  - Nights after 2026-09-10 enter only through `manifest_v002` (selections, same SQL as v001, same
    exclusion criterion, frozen after the window closes).
  - Forward prices for **all** nights come from `manifest_prices_v002`: the same Alpaca queries with
    `end` ≥ the 40th session after the last pick night (2026-12-21 for a 2026-10-23 window end), and
    a symbol list covering **every candidate on every night in the window, published and
    unpublished** — B2 needs the unpublished symbols' closes and forward bars — **plus hourly bars for
    published symbols** for the §4 counter-level tie-break and the `E_AH` sensitivity.
    freeze_prices.py already prices every candidate symbol for daily bars (`:115-116`).
  - **If and only if the DP-13 extension fires on measured counts**, a second pair of successor
    manifests is built on the same terms for the 2026-11-30 window end.
  - `eval.py` records every sha256 and prints sealed (≤ 2026-09-10) and new (≥ 2026-09-11) night
    counts separately, and pre-lock vs post-lock counts for §8 clause 1.
  - **Neither successor freeze exists today**, and neither blocks the lock. If a successor price
    freeze omits unpublished-candidate symbols for a night, **K2 is not computed for that night**:
    the night is excluded from K2 and counted, never back-filled.
- **Sub-cells** (reported only where they clear 20 contributing nights): bull / bear; score band
  (< 80 / 80–85 / 85–90 / 90+); `best_timeframe` (short / swing / long); tape stratum; regime label;
  `d1` ATR-distance tercile. Bear and 90+ cells are expected to be SUPPRESSED
  (DATA_NOTES: 12 / 8 / 3 / 2 elite picks per month since June).

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights 2026-06-01..2026-10-23** (extending once to
  2026-11-30 if and only if the DP-13 gate check fires, §5).
  *Justification:* H-031 predates EXPLORE_001 (it is in the original F4 seed list). However, the
  Explorer's script `research/reports/explore/scripts/40_theme_C_shape.py:147-152` tabulated
  "time to first L1 touch" bins (day 1 / days 2–3 / 4–10 / > 10) against L3–L6 hit rates on
  April–May picks. That is the same construction on a close basis. The in-sample nights are
  therefore contaminated for this question.
  *Registrar's contamination check, on code and counts only:* the script's source was read; its
  output (EXPLORE_001.md, `work/logs/40_theme_C_shape.log`) was not. A count-only search of the
  weekly and daily reports and of BACKLOG found no fast-start or L4-conditioned figure for the sealed
  period. No results directory was read.
- **Catalyst-layer regime change:** the window sits entirely after the 2026-06-01 fix
  (`exclusions_v002.json` `catalyst_layer_regime_change`, carried over unchanged from v001; platform
  commit 69ef05f).
- **Dark lane / publication floor:** the window straddles 2026-07-02 (dark lane) and 2026-07-07
  (publication floor 80, volatilx `services/super_agent_select_scoring.py:1514-1518`). The treatment
  predicate in §2 is correct on both sides. The score-band cells show the composition change.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date (computed per endpoint); Half B = after. The sealed (≤ 09-10) vs
  new (≥ 09-11) split is printed as a descriptive panel. `in_sample_end = 2026-05-29` only marks
  what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v002.json` `regime_label_point_in_time_from`). It is used only for nights
    ≥ 2026-06-09 and only with `regime_version = 'v1.2'`. Nights 2026-06-01..06-08 carry no legal
    label, are stratified by the SPY proxy only, and are flagged.
  - Primary tape stratum for every night, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's
    trailing 20-session return × tercile of SPY's trailing 20-session realized volatility, from
    `prices_daily_split` bars dated ≤ t, with terciles cut on the eligible-night set. Cells < 20
    nights SUPPRESSED.
  - A tape stratum **at the decision clock** (SPY's return over sessions 1–2, sign only) is printed
    descriptively, because a fast start on a strong market day is a different event. It does not
    gate the verdict. It is covered by the §6.1 exception only in the sense that it is descriptive;
    it never gates, filters or matches.

### 6.1 Rule 14 exception — human decision record

- **Decided by:** Haci, **2026-09-13**, relayed by the coordinator. His words: *"Yes, for Q008 only."*
  He explicitly did **not** take the standing-rule option, so the grant does not generalise; it is
  recorded as a scoped grant inside **DP-05(b)** (edited in place 2026-09-13), with no new `DP` id.
- **Scope — fast-start classification only.** Bars from sessions t+1 and t+2, up to **16:00 ET on
  session t+2**, may be used for exactly one purpose: assigning the **F / S** label (and setting
  aside **E4**) against levels anchored at `C_t` — for picks and for B2 distance-matched controls
  alike, each classified from its own bars. The decision time for that one input is **16:00 ET,
  session t+2**.
- **Not covered by the exception:** every other input — pick membership (`qualified`,
  `selected_rank`), direction, score and band, `best_timeframe`, the lane-plan ladder levels, the
  entry price `C_t`, ATR, `beta60`, `runup20`, the control pool and its matching, the regime label,
  the tape stratum, the calendar stratum — must have **available_time ≤ 16:05 ET on the pick night**.
  The session-1 and session-2 bars are **never** an entry price, **never** a level or
  synthetic-target anchor, and **never** a matching, filtering or stratifying input.
- **Outcome use is not input use.** Every outcome is measured **strictly after** the classification
  moment: L4 first touch in sessions **3..40**, `r_p` from `Cl_2` (the session-2 close), the
  counter-level race from session 3 on. Bars inside sessions 1–2 enter the primaries only through the
  F / S / E4 label and the anchor `Cl_2`.
- **What `eval.py` must enforce:** F / S / E4 and `rem` are computed and written to a frozen per-pick
  **and per-control** table **before any bar dated after session t+2 is loaded**. The run **fails**
  if the classification step references any field dated after session t+2's 16:00 ET close, or if a
  session-1/2 bar is referenced anywhere outside classification.

- **Knowledge time (rule 14) — every input declared:**

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `qualification_reason`, `dominant_direction`, `overall_score`, `best_timeframe`, L1–L6 and swing `stop` from `lane_plans` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | population, direction, band, levels |
  | control-candidate pool (non-published rows for night t) | `sas_candidates` | pick night, 16:05 ET | B2 pool |
  | `C_t` (entry price and distance base), ATR14, beta60, runup20, SPY trailing tape | `prices_daily_split`, bars dated ≤ t | pick-night close, 16:00 ET | entry, `d1`/`d4`, matching, stratum |
  | regime label (v1.2, nights ≥ 2026-06-09) | `market_regime_daily` | pick night, ~16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time | exclusion criterion; `E_AH` clock (sensitivity only) |
  | `E_AH` after-hours price (sensitivity only) | `prices_hourly_raw` | publication, pick night | descriptive entry price only |
  | **F / S / E4 classification, `Cl_2`, `rem`** | `prices_daily_split`, sessions 1–2 | **16:00 ET, session t+2 — Rule 14 exception, Haci 2026-09-13 (§6.1), classification only** | **F/S label, E4 set-aside, `Cl_2` anchor** |
  | counter-target prices (descriptive only) | `sas_excursion.counter_levels_json` | copied from the publication-time report, stored in a post-hoc table (never a feature; prices only) | descriptive race |
  | L4 touches and exits, sessions 3..40 | `prices_daily_split` (hourly for descriptive ties) | after the clock | **outcome only** |

  **The conditioning variable is not known at 16:05 ET on the pick night.** It is a second decision
  point — hold-or-flatten at the session-2 close, which is also when the platform's conviction monitor
  already runs (16:02 ET) — and every outcome is measured strictly after it. That is legal here only
  because of the scoped grant in §6.1, and **only for Q008** (DP-05 as amended 2026-09-13): no other
  question inherits it. `sas_excursion` hit/touch columns, `level_hit_dates_json`,
  `level_hit_steps_json` and all `outcome_*` columns are **never** inputs. They are outcomes on a
  different basis, and `level_hit_dates` can carry manual overrides (volatilx
  `routers/performance.py:935-970`, for 2026-04-01, outside this window). `uoa_symbol_daily` is not
  used at all. Its `fwd_return_*` columns are banned (FREEZE_v001 §5).

## 7. Multiple testing

- **Within the question:** 3 primary endpoints (K1, K2, K3), Benjamini–Hochberg across the 3. The
  verdict uses q. Secondaries print raw p only, marked "descriptive, does not decide". K2's DP-12
  status (§4, §8) governs what a q ≤ 0.10 licenses; it does not change the BH set.
- **Across the family:** F4 Price behaviour after selection holds H-030, H-031, H-032, H-033, H-034,
  H-063, H-064 (7 hypotheses), with **H-063 marked "merged into Q007"** in `research/BACKLOG.md`
  (Q007 DECISIONS.md item 7; DP-29), so it is not counted as a further registered F4 question.
  Registered or drafted F4 questions at this draft: **Q007 (H-030 + merged H-063, DRAFT, 4
  primaries)** and **Q008 (H-031, this file, 3 primaries)**. The Reporter applies BH across all
  primary endpoints of registered-and-run F4 questions and prints both q's.
- **Overlaps (not duplicates; the reports must not be presented as independent evidence):**
  - **Q002 (F7, H-065):** its primary endpoint S1 is the unconditional rate of an L1 touch within 2
    sessions **measured from the next-session open, with `passed_at_entry` picks excluded on that
    basis**, against a matched control. Q008's conditioning event is measured from the **pick-night
    close** with the void rule applied at `C_t`, so it is a **different event on a different
    denominator** — the two are not the same statistic. They remain non-independent (same picks,
    overlapping nights) and are never presented as two confirmations; neither `eval.py` reads the
    other's outputs.
  - **Q006 (F1):** reports L4 unconditionally as a secondary, on a different night set.
  - **Q007 (F4):** overlapping nights and picks on the same entry basis (`C_t`), different
    conditioning variable and different primary level. Cross-referenced, never counted twice.
  - **H-033 (F4, unregistered):** L4 touched, then retrace to L2, then re-advance. That is the
    after-L4 path. This question stops at the first L4 touch.
  - **H-066 (F7, unregistered):** quick exit at L1/L2 vs hold. A K3 result bears on it but does not
    test it (different plan, band split, capital-time metric).
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1 = mean_t Δ1_t` and `m2 = mean_t Δ2_t` are in percentage points of L4 touch rate. `m3 = mean_t Δ3_t`
is in ATR units.

**MPE: K1 +10.0 pp** (DECISIONS.md item 5; DP-20 is the 5.0 pp floor, raised here because K1 carries
a known mechanical proximity component — a fast starter is mechanically closer to L4 at the clock —
on the Q003 §8 / Q007 item 4a precedent for an endpoint carrying a known mechanical component). **K2
+5.0 pp** (DP-20 exactly: a control-adjusted touch rate). **K3 0.25 ATR per trade** (Haci 2026-09-12
→ **DP-10**; the standing number for every per-trade ATR-denominated endpoint, not re-asked).

Per endpoint (two-sided; the verdict carries its sign):

- **HISTORICALLY_CONFIRMED** requires **all** of the following:
  1. **contributing nights ≥ 80 for that endpoint**, on its own definition (§2, §5), **with ≥ 25
     contributing nights for that endpoint dated after this file's lock commit** — the lock commit is
     the blindness criterion, and those nights are outside `manifest_v001` and uninspected by anyone
     before the decision date. **This clause does not weaken if the count is short: the date moves
     instead**, exactly once, per the DP-13 rule in §5 (extension to 2026-11-30, decision ≈
     2027-02-03), and DEFERRED thereafter. ≥ 25 is never reduced to 24, and a short K1/K3 count never
     licenses reading K1 off a K2-sized sample;
  2. `|m| > MPE`;
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question;
  5. the point estimate has the **same sign in both halves**, and neither half is beyond MPE in the
     opposite sign;
  6. no tape stratum with ≥ 20 contributing nights is beyond MPE in the opposite sign.
- **NULL:** floors met **and** 95% CI includes 0 **and** `|m| < MPE`. "A fast start says nothing
  about L4" is a real finding and is ledgered with the same care.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, `0 < |m| ≤ MPE` with the CI excluding
  0 ("real but below MPE", rule 6), a CI including 0 with `|m| ≥ MPE`, or a sub-cell below 20 nights
  (SUPPRESSED). A **gate shortfall is not an INCONCLUSIVE verdict**: a primary endpoint below 80
  contributing nights, or below 25 post-lock contributing nights, triggers the single DP-13 extension
  and then DEFERRED (§5).

**Question-level reading (pre-specified, so nobody argues after the fact). K2 is the DP-12 primary:
it is the only endpoint that can license a SAS-facing claim, a card flag or a §9 platform change,
because it is the only contrast matched on the conditioning variable. K1 and K3 are unmatched
contrasts.**

| K1 | K2 | K3 | label | what it licenses |
|---|---|---|---|---|
| CONF + | CONF + | CONF +, and the F-hold gate CI > 0 | **"SAS continuation after a fast start"** | the §9 platform changes (after prospective confirmation for anything subscriber-facing) |
| CONF + | NULL or INCONCL. | CONF +, gate CI > 0 | **"generic fast-start momentum, not a SAS property"** | **descriptive; ledgered. No playbook line and no SAS claim** — an unmatched contrast licenses no rule (DP-12). A playbook line becomes available only under the row-4 absolute-gate carve-out, or if K2 is later CONFIRMED |
| CONF + | any | NULL or INCONCL. | **"information, not worth trading at this size"** | nothing ships; ledgered |
| any | any | CONF − | **"fast start = take profit"** | a `playbook/` line to exit the runner after a fast start — **licensed only when K3's absolute F-hold gate `mean_t mean_{p∈F,t}(r_p)` has its 95% CI entirely below 0**; the F−S difference alone does not license it. That carve-out exists because "stop holding" is a statement about whether a trade Haci already makes pays, not a hit-rate claim (rule 5) and not a claim of a SAS edge. A §9 guide change only after prospective confirmation |
| NULL | NULL | NULL | **"a fast start says nothing about L4"** | the unconditional schedule and the L4-trim ruling stand; ledgered with the same care |
| otherwise | | | **INCONCLUSIVE** | nothing ships |

A K2 CONFIRMED with K3 not confirmed is reported as "SAS picks continue more than look-alikes, but
the hold does not pay beyond a slow start". No rule follows.

- **PROSPECTIVELY_CONFIRMED:** only after **≥ 30 contributing nights for that endpoint** (its own
  definition), dated **on or after 2026-10-26** — which is after the lock commit — frozen separately
  (`manifest_v003` / `manifest_prices_v003`) and never inspected earlier, reproducing the sign of
  every confirmed endpoint under the **unmodified `eval.py`** (DP-24, DP-21). The clause does not
  weaken: if the window cannot supply 30, the decision date moves and that move is R-3. No
  subscriber-facing statement before that (rule 10). Even then the basis stays NON_QUOTABLE until it
  is restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform has **no conditional exit logic keyed to how fast L1 was reached**. The committed
schedules are fixed per score band (volatilx `scripts/generate_sas_trading_guide.py:89-95`). The
2026-07-08 L4-trim ruling cut the 85–88 band's L4 fraction from 30% to 15% using an unconditional L4
rate, and the card itself notes that premise is basis-dependent (`services/sas_conviction_card.py:197-218`).
The conviction monitor runs at 16:02 ET (FREEZE_v001 §7; `services/conviction_monitor_service.py`),
so it already runs at the right moment of day to evaluate a session-2 close.

- **"SAS continuation after a fast start" (K1+K2+K3 positive) — requires K2 CONFIRMED in the same
  sign; there is no `BAND_EXITS` variant and no card flag without it (DP-12):**
  - `BAND_EXITS` gains a **fast-start variant** per band: the L4 fraction is restored or raised when
    L1 was touched within two sessions of the pick-night close, and L1/L2 fractions are shifted toward
    L4. The exact fractions come from a strategist ruling on this question's K3 and scale-out tables,
    not from the registrar.
  - The conviction monitor writes a per-pick `fast_start` flag at the session-2 close. The pick card
    shows "FAST START — L4 in play" beside the ladder, with the matched-control rate next to it
    (rule 5).
  - Brief against the guide generator and the conviction monitor. Ship flag-off with a byte-identical
    checksum on the old path, shadow ≥ 20 trading days (rule 11). Subscriber-facing only after
    PROSPECTIVELY_CONFIRMED.
- **"Generic fast-start momentum" (K1/K3 positive, K2 not CONFIRMED):** **nothing ships** — the
  result is descriptive and ledgered. No `playbook/` line, no card flag, no marketing copy; an
  unmatched contrast licenses no rule (DP-12).
- **"Fast start = take profit" (K3 negative with the absolute F-hold gate CI entirely below 0):** a
  `playbook/` line to exit the runner at the session-2 close after a fast start. A fast-start variant
  of `BAND_EXITS` that front-loads L1–L3 requires K2 CONFIRMED in the same sign **and** prospective
  confirmation.
- **All NULL:** no conditional schedule. The L4-trim ruling stands. The card never implies that early
  speed predicts depth. F4 effort moves on (H-032/H-033/H-064).
- Owner: implementer.

## 10. Known threats to validity (registrar's own list)

1. **K1 is partly mechanical.** A fast starter is, by construction, closer to L4 at the clock. K1 can
   clear its MPE with no SAS-specific information at all. Mitigations: K2 (control-F at the same ATR
   distances) as the only licensing endpoint (DP-12), the remaining-distance terciles and the
   difference-in-differences (§4 secondaries), and the §8 table, which never lets K1 alone license
   anything.
2. **Conditioning controls on their own path.** Control-F is selected by what the controls did in
   sessions 1–2. Picks whose matched controls rarely start fast (far L1, low-ATR look-alikes) drop out
   of K2, so K2's picks are not a random subset of F. **Measured on the sealed window: the control-F
   set is empty for 2 of 291 F picks = 0.7%** (median set size 7, 10th percentile 4), so the matched
   contrast exists for 99.3% of F picks and K2 costs about 1% of the treatment arm rather than a large
   fraction (STEWARD_Q008_exposure.md §(c)). **The threat is not downgraded on that figure:** 0.7% is
   a sealed-period number that may worsen in the post-lock window; an F pick with an empty control-F
   set is **dropped from K2 and counted**, never back-filled and never substituted with the unmatched
   contrast (DP-12); the drop count stays a printed diagnostic. Balance on `rem`, `d1`, `atr_pct`,
   `beta60` and `runup20` is printed for F picks vs control-F.
3. **F includes picks that gapped through L1 — the converse of the old draft's threat, disclosed.**
   Under the `C_t` entry there is no "gapped through" removal: the overnight move is part of the path
   of a position already held, so an L1 touch at or through the t+1 open is a session-1 touch
   (DECISIONS.md item 6). The fast-start group therefore contains picks whose L1 touch was an opening
   gap, which is mechanically closer to L4 at the clock. That is the K1 confound of threat 1, handled
   by K2 (DP-12), the `rem` terciles and the difference-in-differences. The gapped-through-L1 cell is
   printed as a descriptive split of F (§4).
4. **Leakage around the rule-14 exception.** The F/S label is a t+2 observation, granted by Haci on
   2026-09-13 as a **Q008-scoped** exception (§6.1; DP-05 as amended 2026-09-13 — **no other question
   inherits it**). The residual risk is leakage around the exception: a session-1 or session-2
   quantity silently entering matching, filtering, stratification or level placement, or an outcome
   window that starts too early (a touch on session 1 or 2 counted as an outcome rather than as part
   of the classification). Mitigation: §6.1 requires `eval.py` to freeze F/S/E4 and `rem` for picks
   and controls **before any bar after session t+2 is loaded**, and to fail on any reference to a
   later-dated field in classification or to a session-1/2 bar outside classification. The Red Team
   should check this specifically.
5. **Dark-lane predicate elsewhere.** Q002, Q004 and Q006 define "published" as
   `selected_rank IS NOT NULL`, which, from 2026-07-02, also catches never-published dark-lane rows
   (volatilx `services/super_agent_select_scoring.py:1503-1546`). This question uses
   `qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28) and puts dark rows in the control pool,
   not the treatment set. The difference is small in manifest_v001 (915 vs 907; 8 dark rows in this
   window). It will grow with every night the dark lane runs, and it also mis-scopes those questions'
   control pools. Flagged to the Red Team for those questions; locked files are never edited, and it
   is not this question's to fix.
6. **Non-monotone ladders.** L1 and L4 come from different LLM-written lanes, each relative to its
   own lane entry. Excluding `d4 ≤ d1` rows is necessary but not random. On the sealed window it
   removes 1 of 523 picks, but if the share grows the population becomes "picks whose lanes happen to
   be ordered". The share is printed by month and band.
7. **Short-lane picks.** The platform's performance router counts only 2 ladder levels for
   `best_timeframe = 'short'` picks (volatilx `routers/performance.py:920`), while the guide schedules
   L4 fractions for every band. For short-lane picks, "hold for L4" may be outside the lane's intent.
   The `best_timeframe` cell is reported. The verdict is not restricted.
8. **Overlapping 40-session windows** inflate precision. The block length is fixed here at 20
   sessions, not chosen after seeing results.
9. **One tape.** The window is June–October 2026 only (November if the DP-13 extension fires). A sign
   present in one half fails §8 clause 5. Nothing here speaks to an April–May-style tape. Regime
   labels do not exist before 06-09.
10. **Successor freezes do not exist**, and the decision date is 15 weeks away (R2, §5). If
    `manifest_prices_v002` lacks unpublished symbols or forward bars to 2026-12-21, the affected
    nights are excluded from K2 and counted — never back-filled — and if that leaves an endpoint
    below its gate the DP-13 extension fires, once, and then DEFERRED. No night is ever re-run later
    on the same data.
11. **Daily-bar definition — verified.** The desk assumes the Alpaca SIP daily `o/h/l` are
    regular-session values (Q004/Q006/Q007 convention); if extended-hours prints entered the daily
    high/low, session-1/2 touches, and hence F, would be inflated. **Verified:
    research/reports/STEWARD_Q007_exposure.md §R3 Part 1 — PASS 40/40** on the hourly cross-check
    (daily `o` inside the hourly bar containing 09:30 ET; daily `h`/`l` never outside the
    09:30–16:00 ET hourly envelope), with the stated caveat that the frozen data is hourly, not
    tick-level, so this places `o` inside the official-open bar rather than confirming the exact
    opening print. **Binding on `eval.py`:** the 09:30/16:00 ET boundary must be derived **per date
    with `zoneinfo` (America/New_York)**, never a fixed UTC offset — a fixed offset mis-flagged 2 of
    40 pre-DST dates in the Steward's first pass.
12. **Null-ladder denominator:** excluded and counted (§2; 14 of 543 on the sealed window).
13. **Stock path is a proxy, and the close is not a tradable price.** E-HOLD4 is an equity hold. What
    a fast start implies for an option structure (roll the short strike to L4, extend DTE) needs
    option prices the desk does not hold (research/questions/DEFERRED.md); no §9 line may mention
    spreads on the strength of this question. Separately, SAS publishes after the close
    (`finished_at` ~21:0x UTC), so `C_t` is a **proxy** for an after-hours fill (DP-11); the
    picks-only `E_AH` sensitivity (§4) shows the difference on the void filter and the distances, and
    after-hours prints are thin and are not fills (Q004 §10 threat 1).
14. **Dependence on Q002.** Q008's F rate is close kin to Q002's S1 event, though measured from a
    different entry with a different denominator (§7). If picks rarely start fast, the
    contributing-night counts here are at risk — the Steward's pre-lock count (§5) bounds that risk on
    the sealed window without computing any picks-minus-control L1 difference. It is not a reason to
    look early.
15. **Registrar's incidental exposure, disclosed.** While checking the ladder code, the registrar saw
    the hard-coded 2026-04-01 "manual track overrides" in volatilx `routers/performance.py:935-946`.
    They list days-to-L1 and levels hit for 8 picks on that one night. That night is in-sample and
    outside this window, and no design choice here was taken from it.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: **R2 — the successor freezes
(`manifest_v002`, `manifest_prices_v002`, and a second pair if the DP-13 extension fires), built and
pinned at the decision date by design (§5, DP-23); not a blocker for lock.**
