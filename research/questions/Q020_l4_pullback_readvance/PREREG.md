# Q020 — l4_pullback_readvance: when a pick runs to its fourth target and then pulls back to its second, does it get back to the fourth — and is holding through that pullback worth more than the same pullback in a look-alike stock?

**Status:** **DEFERRED (DP-41) — awaiting DP-05(c) grant.** This file does **not** lock. Its EVENT classifier reads `prices_daily_split` / `prices_hourly_raw` bars from sessions t+1…t+40 to assign population membership, control-set membership and the decision basis `X_b` (§6), which is outside the desk's current rule-14 licence; under DP-41 the desk does not grant itself the exception, so Q020 is filed in `research/questions/DEFERRED.md` with the exception named and re-enters the queue at the front if Haci adds the scope to DP-05 as **(c)**. On re-entry DECISIONS.md items 2, 3, 4 and 8 are binding, the §5 schedule is **recomputed from the new lock date and never carried forward** (DECISIONS item 8), and the lock stays **conditional on R1** (§5): if the Steward's measured matched-contributing rate is below the then-re-solved threshold (**0.31 nights per session** on the drafted dates), Q020 stays deferred on the DP-43 ground as well.
**Decisions:** DECISIONS.md
**Family:** **F4 Price behaviour after selection** (hypothesis **H-033**, filed in F4 in `research/BACKLOG.md`). DP-29 is ambiguous for E2 — its subject is a hold-versus-flatten *plan*, which is F6's subject — so the question stays where the BACKLOG files it **and** carries an F6 companion correction for E2 (q ≤ 0.10 required in both families, the larger q quoted; §7), the Q015 pattern. H-033 is counted once, in F4.
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates.
**Registered by:** registrar · **Approved by:** desk (DP-46) · **Date:** 2026-09-13

---

## 1. Hypothesis (plain English)

**When a pick you are holding runs all the way to its fourth ladder target and then trades back down
to its second, buying or holding it at the next morning's open gets you back to the fourth target more
often — and is worth more per trade — than the same round trip in a near-identical stock whose targets
sat at the same distances.**

BACKLOG H-033 reads, in full: *"L4 touched → retrace to L2 → re-advance (Haci's example 1)."* It names
no entry, no clock, no re-advance level, no baseline and no decision. This PREREG fixes all of them
(§2–§4). No sign is presumed; both primaries are two-sided, and a confirmed negative — a pullback from
L4 to L2 marks the end of the move, so the runner should be flattened at the next open — is a finding
of the same weight and is directly tradeable.

**The conditioning event is the price path itself, so DP-12 governs.** "Touched L4, then came back to
L2" is not a feature of the pick at 16:05 ET on the pick night; it is a completed excursion. A naive
contrast against picks that did not do it would say no more than "names that have already run far and
then fallen back behave differently from names that did neither" — a statement about excursions, not
about SAS. The **primary control is therefore matched on the event**: same-night unpublished
candidates that completed **the same round trip**, with synthetic L2 and L4 at the **same ATR
distances and direction** from their own pick-night close, matched on `beta60` / `atr_pct` / `runup20`
among those (§3 B2). The **total effect is descriptive and licenses no rule** (§3 B4). DP-12's cost
travels with the rule and is paid in full here: the matched pool is smaller, EVENT picks with fewer
than three event-completing controls are dropped and counted, and the sample floor arrives later.

**Two endpoints are primary** (§4), both measured from the **open of the session after the pullback
completes**, both against the same event-matched control:

- **(E1, the path)** the pick's **re-advance rate** — L4 touched again within 20 sessions of that open
  — minus its event-matched controls' rate at the identical ATR distances;
- **(E2, the money)** the realized **ATR per trade** of the named plan RE-ADD (hold or buy at that
  open, exit at the first re-touch of L4, otherwise at the 20th session's close, no stop) minus the
  same plan's result on those controls.

**Both must confirm in the same sign before any rule follows** (§8), and a "hold / re-add" line needs
E2's **absolute gate** — the plan's own expectation, `mean_t mean_p r_p`, with its CI clear of zero —
because "keep holding" is a statement about whether a trade Haci already has on pays, not a hit-rate
claim (the Q008 §8 carve-out, mirrored).

**Null:** the re-advance rate and the RE-ADD result of an EVENT pick do not differ from those of a
look-alike stock that completed the same round trip at the same ATR distances.

## 2. Population

- **Unit of inference: the trading night** (rule 6), and the night is the **pick night `t`** — the
  night the position was opened and the night on which selection correlations live. Pick rows are
  aggregated within a night first, so every estimator is a within-night difference and the night's
  tape is held fixed. A bootstrap clustered on the **decision session** is computed alongside and the
  **wider** of the two CIs decides (§4), because several picks from different nights can complete
  their pullbacks on one bad session.
- **Source tables (manifest_v001 and its successors):** `sas_candidates` (`qualified`,
  `selected_rank`, `qualification_reason`, `overall_score`, `dominant_direction`, `best_timeframe`,
  `public_payload_json` → `lane_plans`, `outcome_target_invalid` for the exclusion audit only),
  `sas_runs` (`finished_at`, DP-04).
- **Source tables (manifest_prices_v001 and its successors):** `prices_daily_split` (pick-night close,
  forward opens / highs / lows / closes, ATR14, beta60, run-up, SPY tape, trading calendar),
  `prices_daily_raw` (split-factor snapping only), `prices_hourly_raw` (same-session ordering of the
  L4 and L2 touches; published symbols only — `research/lib/freeze_prices.py:17`, `:117`).
- **Treatment rows (published picks), exact predicate:** `qualified IS TRUE AND selected_rank IS NOT
  NULL` (**DP-28**) — the platform's own exposure predicate (volatilx
  `services/sas_conviction_card.py:105`, `:308-309`). Dark-lane rows (`selected_rank` set,
  `qualified = FALSE`, `qualification_reason = 'selected_dark'`; volatilx
  `services/super_agent_select_scoring.py:1503-1546`) are **never** treatment rows; they are counted
  and they stay in the control pool.
- **Control pool, night `t`:** the complement of the publication predicate — every same-night
  `sas_candidates` row for which `NOT (qualified IS TRUE AND selected_rank IS NOT NULL)`, i.e.
  `qualified = FALSE` rows **and** dark-lane rows (DP-28; rule 5's "unpublished candidates from the
  same night"). A pool row also needs ≥ 60 prior split-adjusted bars (beta60), ≥ 21 bars (runup20) and
  **60 forward sessions** in the pinned freeze.
- **Levels, exact** — the platform's own mapping, `_LADDER_KEYS` × `_LADDER_SOURCES` (volatilx
  `services/sas_conviction_card.py:182-187`, `:246-258`):
  **L2 = `day_trading.targets[1]`**, **L4 = `swing_trading.targets[1]`**. L1, L3, L5 and L6 (for the
  descriptive order-of-hit and the shallow-retrace arm) are the remaining four of the same mapping.
- **Clocks, and why they are these.** The EVENT lives on **L4's own 40-session swing-lane window**
  (`_LADDER_LEVEL_WINDOW`, `:194`; DP-42's "L4 within 40 sessions for questions about deep targets"):
  both legs — the L4 touch and the pullback to L2 — must complete inside sessions 1..40 from the entry.
  The **re-advance clock is `R` = 20 sessions from the decision basis** (DP-09, the horizon a spread is
  held over, counted from the stated basis rather than from the pick night). L2's own 20-session day-lane
  window governs L2-**as-a-target** (Q002's use) and is not used here: L2 is read as a **retrace line**
  on the swing lane's clock, which is not a re-uniting of the hypothesis (DP-25) but the only clock on
  which "after L4" exists.
- **Notation (all prices in the signal-date split basis):**
  - `C_t` — the pick's **actual** regular-session close on pick night `t` from `prices_daily_split`;
    never the platform's `spot_close`, which is stale on re-run nights (DATA_NOTES, EXPLORE_001 §9).
  - `dir` = +1 (bullish `dominant_direction`) / −1 (bearish).
  - `ATR` — ATR14 from `prices_daily_split` bars dated ≤ `t`. The platform's `atr_pct` is corrupted
    around splits (DATA_NOTES / PI-003) and is not used; `atr_pct = ATR / C_t`.
  - Sessions `s = 1, 2, …` are the trading sessions after `t`, from the SPY calendar. `O_s`, `H_s`,
    `L_s`, `Cl_s` are that session's open, high, low and close.
  - `d2 = dir × (L2 − C_t) / ATR` and `d4 = dir × (L4 − C_t) / ATR`.
- **The EVENT, per pick (deterministic; `eval.py` applies it with no judgment):**
  - `a` = the first session in 1..40 on which L4 is touched (`H_a ≥ L4` bullish / `L_a ≤ L4` bearish).
    A gap through L4 at a session's open is a touch in that session.
  - `b` = the first session in `a`..40 on which L2 is touched (`L_b ≤ L2` bullish / `H_b ≥ L2`
    bearish) **at or after the L4 touch in time**. Because `0 < d2 < d4` is required (below), L2 is
    necessarily passed on the way up; only a touch that can be shown to follow the L4 touch counts.
  - **EVENT = 1** iff both `a` and `b` exist. `b = a` (a same-session round trip) is ordered from
    `prices_hourly_raw`; where one hourly bar holds both, or the symbol has no hourly bars, the pair
    counts **not an EVENT** — DP-27, which here is also the reading less favourable to the hypothesis.
  - **Decision session = `b`; decision basis `X_b = O_{b+1}`**, the open of the next session (§4).
- **Exclusions — each counted per arm and printed in the results header, never silently dropped.**
  Every exclusion uses inputs available by 16:05 ET on the pick night, the trading calendar, or a
  measurement failure:
  - nights in **`research/data/exclusions_v003.json`** (`manual_runs.trading_dates` ∪
    `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`); in-window
    those are **2026-06-26**, **2026-07-02** and **2026-07-06**. `eval.py` reads the JSON and takes the
    union; **no date is hard-coded** here or in `eval.py` (DP-22).
  - any prospective night whose `finished_at` is later than the next session's open (DP-04), applied
    mechanically, not by judgment.
  - **null-ladder denominator:** no `lane_plans`, no `day_trading.targets[1]`, or no
    `swing_trading.targets[1]` → excluded and counted (FREEZE_v001 §3 counts 17 of 915 selected rows
    with no ladder row at all).
  - **void levels at the entry price:** `d2 ≤ 0` or `d4 ≤ 0` — the platform's own void rule
    (`services/sas_reference.py:199-227`) applied to the actual close, and rule 5's "a target already
    passed at that entry is not a hit" evaluated at the entry basis `C_t` (DP-11, DP-26). Excluded and
    counted.
  - **non-monotone ladder:** `d4 ≤ d2`. L2 and L4 are written by an LLM on two different lanes, each
    relative to its own lane entry (`ai_agents/principal_agent.py:548-554`), and the platform states
    that levels "are not strictly price-ordered across lanes" (`services/sas_conviction_card.py:289`).
    "Ran to L4 then back to L2" only means something when L2 lies between the entry and L4. Excluded
    and counted; the share is a headline number, printed by month and by band.
  - **void at the decision basis:** an EVENT pick whose `X_b` is already at or through L4
    (`dir × (L4 − X_b) ≤ 0` — an overnight gap of more than `d4 − d2` ATR). Rule 5 and DP-26 are
    explicit that a gap-through at entry is never a hit, so the pick is excluded from E1 and E2 and
    **counted**, and the count is printed as a headline and as a descriptive "instant re-advance" cell.
  - mixed-direction picks (`dominant_direction` neither bullish nor bearish); `outcome_target_invalid`
    non-null → excluded and counted.
  - **immature:** fewer than **60** forward sessions in the pinned freeze. The maturity test is
    **uniform across every eligible pick and never a function of its own path** — `b + R ≤ 40 + 20 = 60`
    by construction, so no EVENT and no outcome is right-censored. Maturity comes from the trading
    calendar, never from whether a price exists; right-censoring is never graded as a non-touch.
  - missing-bar or delisted symbols (missing `C_t`, missing 14-bar ATR history, a missing bar inside
    1..60) → dropped and counted. A night is dropped if > 25% of its eligible picks are ungradeable.
    This is a measurement failure, never a classifier: it can never move a pick between arms.
- **Contributing night (the floor unit, DP-21) — one definition, shared by E1 and E2:** a night
  carrying **≥ 1 EVENT pick** that is not excluded at the decision basis and whose **control-EVENT set
  has ≥ 3 members** (§3 B2). A night with EVENT picks but no valid control set contributes nothing to
  either endpoint; it is counted, printed in the funnel and is **not** a contributing night. A matured
  night on which no row survives the funnel is a **non-contributing night, not an exclusion**, and is
  never added to any exclusions file.
- **The already-measured nights are in the window, not outside it.** The nights R1 counts (§5) sit
  inside the §6 window and inside `manifest_v001`; the Steward measures them to fix a rate, not to seed
  a result (counts only, and no re-advance of any kind), and they enter `eval.py` on exactly the same
  footing as every later night. The window is **not re-based** on them. `eval.py` prints pre-lock and
  post-lock contributing-night counts separately so DP-24's clause is checked rather than asserted.

## 3. Baseline(s) — what this must beat

- **B1 (H-033's implicit baseline, "Y's rate when X did not happen"), descriptive:** picks that touched
  L4 inside 40 sessions and **did not** pull back to L2. Their re-advance is undefined (they never came
  back), so this cohort cannot carry the primary; what it can do, and does, is bound the question "is
  the pullback itself bad news?" It is reported as the **shallow-retrace arm** below and never decides.
- **B2 (the DP-12 primary control — event-matched *and* distance-matched).** For each EVENT pick `p` on
  night `t`, built in this order and no other:
  1. **Condition first.** Take every control-pool row `c` on night `t` (§2) and give it synthetic
     levels at `p`'s ATR distances in `p`'s direction, anchored at the control's **own** pick-night
     close: `L2_c = C_c × (1 + dir_p × d2_p × atr_pct_c)` and
     `L4_c = C_c × (1 + dir_p × d4_p × atr_pct_c)`. Classify `c` for the EVENT from **its own** bars by
     the §2 rules (its own `a_c`, its own `b_c`, the same 40-session cap, the same DP-27 same-session
     rule). Keep the rows with EVENT = 1 and 60 forward sessions — the **control-EVENT pool**.
  2. **Match second.** From that pool take the **10 nearest** on standardized (`beta60`, `atr_pct`,
     `runup20`) measured at the pick-night close — night-cross-sectional median and MAD, Euclidean,
     with replacement across picks, ties by symbol ascending (the Q006 §3 construction). Fewer than 10
     available ⇒ take all of them; **fewer than 3 ⇒ the pick is dropped from E1 and E2 and counted**,
     never back-filled, never substituted with an unmatched contrast (DP-12). That drop count is a
     headline number (§10 threat 2).
  3. **Grade third.** Each control is graded from **its own** decision basis `O_{b_c+1}` over its own
     `R` sessions, using its own `dir` and its own `ATR`, by the identical §4 rules. A control whose
     `O_{b_c+1}` is already at or through `L4_c` is dropped from that pick's control set and counted,
     the same rule the pick faces.
  4. Control rows **never add to inferential n** (rule 6). Post-match standardized mean differences on
     `beta60`, `atr_pct`, `runup20`, `d2`, `d4`, `b − a`, the retrace depth and the remaining distance
     `rem` are printed for every night.
  **Condition-then-match is deliberate and is what DP-12 asks for**: the control must have completed
  the same round trip, and among those it must look like the pick. Matching first and filtering second
  would empty most control sets for want of ten look-alikes that happen to complete a rare path, and
  would make the question about who has controls rather than about re-advance.
- **B3 (descriptive): the unmatched control-EVENT pool** — every same-night control that completes the
  EVENT at `p`'s distances, with no covariate matching. Shows how much of any E1/E2 gap is composition.
- **B4 (the total effect; descriptive, licenses no rule — DP-12):** EVENT picks against (a) the
  **shallow-retrace arm** (B1: touched L4, pulled back to L3 but not to L2, graded from the open after
  the first L3 touch at or after `a`) and (b) all eligible picks' unconditional L4-touch rate on a
  clearly different denominator. Printed beside every primary and labelled *"total effect: includes the
  excursion that had already happened; descriptive, does not decide."*

## 4. Objective metric (rule 5 — the price path from a stated basis, measured the way it is traded)

**Entry basis (DP-11).** The position is **already held** when the signal appears, so the entry is the
**pick-night regular-session close `C_t`**, the DP-03(a) after-hours proxy, for picks and controls
alike — the one basis rule 5 requires on both sides, and the only basis the unpublished control
candidates have. `C_t` fixes eligibility (the void and monotonicity rules), the ATR denominator, `d2`,
`d4` and the matching covariates. **It does not enter either estimand:** E1 and E2 are measured from
`X_b`, so the well-known gap between `C_t` and a real after-hours fill (Q004 §10 threat 1) cannot move
the primaries. The picks-only `E_AH` sensitivity — Q004's definition verbatim, the close of the first
`prices_hourly_raw` bar at or after that night's `sas_runs.finished_at` and before the next regular
open — is printed for the eligibility filters only and never decides.

**The decision basis.** The pullback completes at the close of session `b`. A holder cannot trade a
close he is still watching form, so the decision basis is **`X_b = O_{b+1}`**, the first executable
moment after every classifying bar has closed, for picks and controls alike. The session-`b` close is
printed as a picks-only descriptive sensitivity, labelled *not executable*, and never decides.

**The plan (no stop — rule 5, DP-02; adverse excursion is reported, never traded):**
- **Plan RE-ADD (the tested rule):** hold, or buy, the full unit position at `X_b`; exit at the first
  touch of L4 in sessions `b+1 … b+R` at the L4 price — at that session's open instead if the session
  **opens through** L4, the better fill a resting limit would have got; otherwise exit at the close of
  session `b+R`. `R = 20`.
- `r_p = dir × (exit_p − X_b) / ATR`. Flattening at `X_b` scores exactly 0, so `r_p` **is** the
  hold-versus-flatten difference as the trader faces it, and its baseline is the same plan run on the
  event-matched controls (B2).

**Primary endpoints (two, pre-specified, BH-corrected within the question and across the family — §7).**
For pick night `t`, `mean_E[·]` is the mean over that night's eligible EVENT picks and, for each such
pick, `mean_M[·]` is the mean over its matched controls (a pick's control mean enters once, so a pick
with 10 controls does not outweigh a pick with 3):

- **E1 — the path (re-advance rate, event-matched, percentage points).**
  `Y_p = 1` if L4 is touched in sessions `b+1 … b+R`, else 0.
  `Δ1_t = mean_E[ Y_p − mean_M[ Y_c ] ]`; estimand `m1 = mean_t Δ1_t`, in percentage points, over
  contributing nights. Picks and controls carry their targets at the **identical ATR distance and
  direction** from their own closes, so the contrast is distance-matched by construction (rule 5).
- **E2 — the money (RE-ADD realized ATR per trade, event-matched).**
  `Δ2_t = mean_E[ r_p − mean_M[ r_c ] ]`; estimand `m2 = mean_t Δ2_t`, in **ATR per trade**.
  **Gate reported with E2 (pre-specified, used in §8):** the absolute expectation
  `g = mean_t mean_E[ r_p ]` with its 95% CI — what holding through the pullback makes, before any
  control is subtracted.

**Ordering rules, stated once, applied by `eval.py` with no judgment:**
1. **Same-session L4 and L2 touches (`b = a`)** are ordered from `prices_hourly_raw`, converted to the
   signal-date split basis (`eval.py` asserts basis agreement per symbol-date and fails loudly). Where
   one hourly bar holds both, or the symbol has no hourly bars, the pick or control is **not an EVENT**
   (DP-27, the reading less favourable to the hypothesis). The rule is identical on both sides; its
   effect is not, because roughly half of unpublished candidate symbols carry no hourly bars anywhere
   in the freeze (`STEWARD_Q015_exposure.md` §7 measured 206 of 428), which **shrinks the control-EVENT
   pool** and therefore makes the test harder, not easier. The counts are printed per arm and the
   opposite reading is a named sensitivity that never decides (§10 threat 5).
2. **A gap through a level at a session open is a touch** in that session, for L4, for L2 and for the
   adverse line — except at the decision basis itself, where a level already through `X_b` is void and
   the row is excluded (§2, rule 5, DP-26).
3. The **first** L4 touch sets `a`; the **first** qualifying L2 touch sets `b`. There is no second
   EVENT on the same pick, no re-arming and no use of any later round trip, whatever it does.

**Secondary, descriptive, never decides (each prints raw p only):**
- **B4** (the total effect) and **B3** (the unmatched control-EVENT pool), beside every primary;
- the **shallow-retrace arm** (touched L4, pulled back to L3 but not to L2) run through E1 and E2 with
  its own event-matched controls — the read on "how deep a pullback is too deep", which is a different
  hypothesis and is registered here as a secondary rather than as a third primary;
- **re-advance levels other than L4:** L3 re-touch and L5 first touch within `R` sessions of `X_b`,
  and the share of re-advancers that go on to L5 (does the re-advance stick?);
- **clock sensitivities:** `R` = 10 and `R` = 40 sessions (40 on matured nights only, labelled), and
  the EVENT cap at 20 sessions instead of 40;
- **the rule-5 execution report:** the **committed scale-out** `BAND_EXITS` (volatilx
  `scripts/generate_sas_trading_guide.py:89-95`; 80–85 `10/15/30/15/20/10`, 85–88 `0/15/30/15/25/15`,
  88–90 `0/10/25/15/30/20`, 90+ `0/0/10/20/30/40`) entered at `C_t`, each fraction exiting at its
  level's first touch (or the better open where a session opens through it), fractions whose level was
  at or through `C_t` recorded unfillable, the remainder closed at the session-60 close (truncated and
  labelled; the trailing rules are not deterministic enough to simulate and are ignored) — reported
  **with and without** a RE-ADD of the residual at `X_b`, so the plan's realized result sits next to
  the hit rates as rule 5 requires;
- **proximity:** the remaining distance `rem_p = dir × (L4 − X_b) / ATR` and the retrace depth
  `dep_p = dir × (L2 − min-price-through-b) / ATR`, for picks and controls, with E1 and E2 recomputed
  within night-pooled terciles of each — the read on whether the event carries information beyond
  where price is sitting at the decision basis;
- **the adverse race from `X_b`:** with levels `X_b + dir × 1.0 × ATR` and `X_b − dir × 1.0 × ATR`
  over `b+1 … b+R`, the adverse-first rate for picks and matched controls (levels set from the basis,
  so none can be passed at entry); maximum adverse and maximum favourable excursion in ATR from `X_b`;
  counter-direction touches — reported, never an exit (DP-02). This panel carries a §8 guard clause;
- **the tape-aligned control set** — B2 restricted to controls with `|b_c − b| ≤ 5` sessions — as the
  §8 clause 7 guard;
- sessions from `X_b` to the L4 re-touch; the `b − a` round-trip length; the order-of-hit sequence
  after `X_b`;
- sub-cells at ≥ 20 contributing nights: score band (80–85 / 85–90 / 90+), bull / bear,
  `best_timeframe`, `d4` tercile, `rem` tercile, `dep` tercile, `b − a` tercile, tape stratum, regime
  label;
- the **session-`b` close** decision basis (picks only, not executable), and the **`E_AH`** entry
  sensitivity on the eligibility filters (picks only);
- close-to-close return from `X_b` at `b+10` and `b+20` — **fixed-horizon return is descriptive by
  rule 5 and never decides**.

**Quotability:** 40- and 60-session bases → **every number in this question is NON_QUOTABLE**
(rule 12).

**Inference.** Night-level. **CI (decides):** the **wider** of (a) a stationary block bootstrap over
the ordered contributing pick nights, expected block length **30 sessions** (half the 60-session
forward window — the Q016 / Q017 convention, fixed here and not chosen after seeing results), and
(b) a bootstrap clustered on the **decision session `b`**; 2,000 resamples each, seed 20260913. Taking
the wider is deterministic, conservative, and chosen here rather than after seeing which is wider.
**p-value:** paired sign-flip permutation on the night contrasts `Δ1_t`, `Δ2_t`, 10,000 permutations,
seed 20260913; a within-night EVENT-label shuffle across the night's eligible picks is printed second
for B4. Every estimate prints n(contributing nights), n(contributing nights dated after the lock
commit), n(EVENT picks), n(control rows), n(picks dropped for < 3 controls), n(picks void at the
decision basis), n(resolved by ordering rule 1), n(excluded, by reason).

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** — E1 and E2
  share the §2 definition — and ≥ **20 contributing nights per reported sub-cell**. A sub-cell below 20
  is **SUPPRESSED** (counts only, no point estimate, not even "small n, directionally") and does not by
  itself make its endpoint INCONCLUSIVE (§8 clause 1). The weaker reading of rule 6 is not used.
  **No floor is ever lowered to hit a date.**
- **Binding maturity: 60 sessions** from the pick night (§2), uniform across every eligible pick.
- **No exposure has been measured for this question, and nothing in the desk's reports measures it.**
  The Steward's Q008 count deliberately stopped at what sessions 1–2 required and computed no L4 touch
  (`STEWARD_Q008_exposure.md` §(e)); Q009's and Q015's counts are stop-side and L3-side; no weekly,
  daily or freeze report crosses an L4 touch with a later pullback. The schedule below is therefore
  **provisional at a stated planning rate** and is re-derived from R1.
- **What has to be true for the planning rate to hold, written out so R1 can be read against it.** With
  `k ≈ 6.3` eligible picks per night (the Q008 and Q009 funnels give 522/67 and 303/48), a per-pick
  EVENT-with-valid-controls probability `qπ`, and nights independent,
  `r ≈ 1 − (1 − qπ)^k`. The planning rate `r = 0.35` needs `qπ ≈ 0.066`; the break-even rate
  `r = 0.31` needs `qπ ≈ 0.057`. **Disclosed, and it gates nothing:** the conviction card's own note
  claims an L4 first-touch rate of about 67% over the 40-session swing window (volatilx
  `services/sas_conviction_card.py:207-218`) — a platform-displayed figure, on the close basis, over
  the full history including the strong April–May tape, on its own denominator. If the first leg is
  anywhere near that common, `qπ ≈ 0.066` needs only about one EVENT pick in ten to complete the
  second leg with three usable controls, and the 0.35 planning rate is conservative. It is not an
  exposure measurement for this question, no threshold or definition here was taken from it, and
  **R1 measures the EVENT** (§10 threat 12).

**R1 is HELD while Q020 is DEFERRED (header; DECISIONS.md item 1).** It counts the very classifier the
DP-05(c) request is about, and no schedule follows from it while the question cannot be tested, so it
is run only once the grant exists — then exactly as written below, with every date re-derived from the
new lock date (DECISIONS item 8) and the `r` threshold re-solved against the new 12-month ceiling.

**R1 — routed to the Data Steward, due before lock (counts only; no outcome of any kind — no
re-advance, no L4 touch after `b`, no plan result, no return, no pick-minus-control difference of any
sort).** The EVENT is the *conditioning variable*, not the endpoint, and may be counted; nothing after
`b` may be. On pick nights **2026-06-01..2026-07-15** (the 40-session classification maturity on
`manifest_prices_v001` — deliberately not the 60-session outcome maturity, which would leave about ten
nights), after the §2 funnel and `exclusions_v003.json`:
  1. matured pick nights, published picks, and the §2 funnel step by step: no lane plan, no L2, no L4,
     void at `C_t`, non-monotone `d4 ≤ d2`, mixed direction, `outcome_target_invalid`, ungradeable;
  2. **EVENT picks and EVENT nights** — picks with `a` in 1..40 and a qualifying `b` in `a`..40 — with
     the distributions of `a`, `b`, `b − a`, `d2`, `d4` and the retrace depth `dep`;
  3. **matched-contributing nights** — nights with ≥ 1 EVENT pick carrying ≥ 3 event-completing
     matched controls — and the **rate per session, by month**;
  4. EVENT picks dropped for fewer than 3 event-completing controls, with their `d2` / `d4`
     distribution, and the control-EVENT pool-size distribution (median, p10, minimum);
  5. EVENT picks whose `O_{b+1}` is already at or through L4 (the void-at-decision-basis exclusion);
  6. same-session (`b = a`) cases on picks, and how many hourly bars resolve; hourly-bar coverage on
     published symbols for sessions 1..40, and the share of unpublished candidate symbols with no
     hourly bars anywhere in the freeze (the Q015 §7 asymmetry, remeasured on this funnel);
  7. any platform commit inside the window touching `_extract_lane_plans`
     (`services/super_agent_select_service.py:94-161`) or the cross-lane re-sort (`:195-257`), from the
     read-only platform repo — a column that changed meaning mid-window is two features (DP-06,
     DP-50(a)), and the window start moves after it. Q009 §R3 ruling 2 already found **no historical
     payload rewrite** across the 795-row correction ledger; R1 re-checks only for new ship dates.
- **Planning rate and schedule (DP-43; every figure below is an assumption to be replaced by R1's
  measurement, printed so it can be checked; the desk's mechanical conversion is 1.4484 calendar days
  per session):**
  - **Planning rate `r_plan` = 0.35 matched-contributing nights per session.** 80 contributing nights
    need 229 sessions ≈ 332 days from 2026-06-01 → **2027-04-30**.
  - **Primary window: pick nights 2026-06-01..2027-04-30 inclusive**, after exclusions. The end is
    where the planning rate projects the 80th contributing night, not where a date would be convenient.
    A shorter window that reached a date sooner was rejected (DP-43, DP-45).
  - **Decision date: Monday 2027-08-02.** 2027-04-30 + 60 sessions maturity ≈ 2027-07-26, + one week
    freeze margin = 2027-08-02, first Monday on or after = 2027-08-02 — **10.6 months from the
    2026-09-13 lock**, inside DP-43's 12-month ceiling. The Steward fixes the exact session-count date
    when building the successor freezes. `eval.py` is written once (rule 9) and run **once**, then.
    **No interim looks.**
  - **Conditional lock (the DP-43 ceiling test, on R1's measured rate `r`).** Solving
    `1.4484 × 80/r + 87 + 7 ≤ 469` days (2026-06-01 → 2027-09-13) gives **`r ≥ 0.31`**. If the Steward
    measures a matched-contributing rate **below 0.31 nights per session**, the initial decision date
    falls past the ceiling and **Q020 goes to `research/questions/DEFERRED.md` at `record` with that
    date named**, rather than the ceiling being stretched (H-062 precedent). If `r ≥ 0.31`, the window
    end and decision date are recomputed at the measured `r` and the question locks on those dates —
    later than the drafted ones if `r < 0.35`, **never earlier than a rate supports** (DP-43, DP-45).
  - **Both gates, per primary endpoint, on measured counts.** Evaluation proceeds only if **each**
    primary has **≥ 80 contributing nights** and **≥ 30 contributing nights dated after this file's
    lock commit** (DP-24), printed by `eval.py` from the frozen data. At 0.35/session the 30 post-lock
    nights arrive ≈ 2027-01-11 and about 55 accrue by the window end (49 at the break-even 0.31), so
    DP-24 is not the binding gate: **PROSPECTIVELY_CONFIRMED is reachable from this run by design,
    DP-31 does not apply, and no successor replication question is needed.** Gates fire on `eval.py`'s
    measured counts at the decision pass, never on R1, on this projection or on a run-rate.
  - **One automatic extension (DP-13; DP-43's +30 sessions).** If any gate is short at the decision
    date on `eval.py`'s measured counts, the window extends **once**, automatically and with no new
    question, by 30 sessions — on the drafted schedule to pick nights **2026-06-01..2027-06-14**
    (30 sessions after Friday 2027-04-30 with Memorial Day Monday 2027-05-31 removed is **Monday
    2027-06-14**; the drafted 2027-06-12 was a Saturday, corrected per DECISIONS Correction 2, moving
    the window end **out, never in** — DP-43, DP-45), decision **Monday 2027-09-20** (unchanged: 60
    sessions from 2027-06-14 is Thursday 2027-09-09 with Juneteenth observed 2027-06-18, Independence
    Day observed 2027-07-05 and Labor Day 2027-09-06 removed; + one week = 2027-09-16; first Monday on
    or after = 2027-09-20) — run with the **byte-identical, unmodified `eval.py`** and the same
    gates. That extension date falls after the 12-month ceiling: DP-43's ceiling tests the **initial**
    decision date, and DP-13's single extension is agreed here at lock, so it stands.
  - **DEFERRED fallback.** If a gate is still short after that single extension, Q020 goes to DEFERRED
    with the measured counts rather than running under-powered. There is no second extension, no
    reduced floor, and a gate shortfall is **not** an INCONCLUSIVE verdict (§8).
  - **Arms demoted at lock (DP-43), not after:** the shallow-retrace arm (§3 B1 / §4) is descriptive
    from lock, and the 90+ and `<80` band sub-cells are expected to be SUPPRESSED (DATA_NOTES: 12 / 8 /
    3 / 2 elite picks per month since June; `publication_floor = 80.0` since 2026-07-07, volatilx
    `services/super_agent_select_models.py:86-91`). **No arm is demoted or promoted after lock in
    either direction**; a thin cell at the decision pass is handled where it belongs, as a SUPPRESSED
    sub-cell (§8 clause 1).
- **Freeze discipline (DP-23; routed request R2 — due at the decision date, not a blocker for lock;
  HELD while Q020 is DEFERRED, since no successor pair is built for this question until the DP-05(c)
  grant exists, and the request revives with it).**
  Nights ≤ 2026-09-10 stay pinned to `manifest_v001` / `manifest_prices_v001`; later nights enter only
  through `manifest_v002` (selections, same SQL, same exclusion criterion) and `manifest_prices_v002`
  (same Alpaca queries), with the daily symbol list covering **every candidate on every night in the
  window, published and unpublished** — B2 needs the unpublished symbols' pick-night closes, their
  prior bars for `beta60` / `atr_pct` / `runup20` and their forward bars — **plus hourly bars for
  published symbols** (ordering rule 1), carrying **60** forward sessions beyond the last included pick
  night (80 where the `R` = 40 companion is computed). A second pair is built **only if** the DP-13
  extension fires. `eval.py` takes the window bounds, the manifest paths, the exclusions-file path and
  the output directory as inputs — **no hard-coded dates, manifest names or paths** — records every
  sha256, and prints pre-lock and post-lock night counts separately. If a successor price freeze omits
  unpublished-candidate symbols for a night, that night is excluded from both primaries and counted,
  never back-filled.

## 6. Test window, split and stratification

- **Test window: sealed + prospective — pick nights ≥ 2026-06-01** (or later per §5 R1 item 7) through
  the §5 window end.
  *Justification:* H-033 is one of the original F4 seeds ("Haci's example 1") and predates
  EXPLORE_001, but the Explorer's April–May scripts tabulated first-touch timing against deep-level hit
  rates (`research/reports/explore/scripts/40_theme_C_shape.py:147-152`, read by the Q008 registrar) and
  EXPLORE_001 §C published a counter-touch-then-L3 recovery rate, so the in-sample nights are treated
  as contaminated for any question about level sequences and are excluded entirely — not even as a
  descriptive panel. The window also sits entirely after the 2026-06-01 catalyst fix (DP-06;
  `exclusions_v003.json` `catalyst_layer_regime_change`; platform commit `69ef05f`).
  *Contamination check on the sealed period (registrar; count-only, and **no results directory was
  read**):* the desk's sealed-period descriptive outputs recorded in `research/BACKLOG.md`, in the
  weekly entries and in the other questions' own disclosures contain **no L4-then-pullback figure of
  any kind**. The nearest neighbours are Q009's stop-then-target exposure counts (the adverse-side
  mirror, counts only, no outcome), Q015's registered-but-unrun L3-then-counter-level endpoint, and
  Q006's registered touch-then-settle secondary — Q015's own check states that "no counter-level
  revisit, give-back or exit-at-touch statistic exists anywhere in the sealed outputs". Every parameter
  here comes from the platform (the L2 / L4 mapping, the 40-session swing window), from H-033's own
  wording (DP-25) or from standing policy (the 20-session re-advance clock, DP-09; the ±1 ATR adverse
  line and the 30-session block, DP-26); none was chosen after seeing a number.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date (re-derived from the final window at the decision pass); Half B = after.
  `in_sample_end = 2026-05-29` marks only what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v003.json` `regime_label_point_in_time_from`). It is used only for nights ≥ 2026-06-09,
    only `regime_version = 'v1.2'`, and only where the row is a same-evening write; a later-posted row
    is treated as missing. Nights 2026-06-01..06-08 carry no legal label and are stratified by the SPY
    proxy only, flagged.
  - Primary tape stratum for every night, trailing and legal at the pick night's close: `tape_t` =
    sign of SPY's trailing 20-session return × tercile of SPY's trailing 20-session realized
    volatility, from SPY bars dated ≤ `t` in `prices_daily_split`. **Tercile cut points are
    expanding-window**, so no later night's data sets an earlier night's stratum. Cells < 20
    contributing nights SUPPRESSED.
  - A **decision-window tape panel** — SPY's return over sessions `b+1 … b+R` — is printed
    descriptively, because a re-advance in a rising market is a different event. It never gates,
    filters, matches or stratifies anything: it is measured entirely after the decision basis and is an
    outcome-side description, not an input.
- **Knowledge time (rule 14) — every input declared. Q020 is outside the desk's current rule-14
  licence and therefore requests a scoped exception it may not grant itself; under DP-41 the question
  is DEFERRED until Haci adds the scope to DP-05 as (c)** (DECISIONS.md item 1, Correction 1). The
  **selection-side** inputs (population, band, direction, levels, ATR, matching covariates, strata) are
  all 16:05 ET on the pick night or earlier and need nothing. What is outside the licence is the
  **EVENT classification from sessions 1 … `b`** and the decision basis it produces: a pick is in E1
  and E2 **only if** bars from sessions t+1 … t+40 say it round-tripped, its control set is selected
  the same way, and `X_b = O_{b+1}` is itself located by those bars. That is an **eligibility filter
  and an arm assignment built from post-pick-night quantities**, not an outcome, and the locked
  question on this shape says so in the opposite direction: **Q009 §6** (locked) rests on the fact that
  *"no session-t+1 quantity enters any primary endpoint **or any eligibility filter**"* — Q020's does,
  on both arms. **DP-05(b)** is the nearest precedent in the other direction and shows the price: Q008
  paid a **question-scoped** grant for bars from sessions t+1 and t+2 with the decision time for that
  one input moved to 16:00 ET on session t+2, and DP-05 records that Haci **explicitly declined** the
  standing-rule version — the general "a later clock is fine when the bar only classifies" licence — on
  2026-09-13. Q020 would need that same licence over **40 sessions instead of 2**, on published picks
  and the unpublished control pool alike, so it is asked for **explicitly and narrowly** rather than
  assumed. `research/lib/validators.py:17` (`ET_DECISION = "16:05"`, *"features must be available
  before this"*) is the enforcement code's own reading and is not softened here (rule 15).

  **The exception requested, exactly** — and nothing beyond it:
  - **Tables and columns:** `prices_daily_split` daily OHLC, and `prices_hourly_raw` hourly OHLC for
    the same-session ordering rule (rule 1, resolving `b = a`).
  - **Rows:** published picks **and** the unpublished same-night control pool.
  - **Time:** sessions **t+1 … t+40**, i.e. a decision time for that one input of **09:30 ET on
    session `b+1`, `b ≤ 40`** (at most session t+41).
  - **Purpose:** assigning the EVENT (`a` = first L4 touch, `b` = first qualifying L2 touch at or after
    it) and therefore **population membership, control-set membership and the decision basis
    `X_b = O_{b+1}`** — nothing else.
  - **What it is not:** no outcome enters through it (every outcome is measured strictly after `X_b`),
    no selection-side input moves (everything else stays at 16:05 ET on the pick night), and it
    licenses nothing beyond this question.

  Until that scope exists, Q020 does not lock and is not counted in the F4 or F6 correction sets (§7).

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `qualification_reason`, `overall_score`, `dominant_direction`, `best_timeframe` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | population, band, direction |
  | **L2 (`day_trading.targets[1]`), L4 (`swing_trading.targets[1]`)**, L1/L3/L5/L6 | `sas_candidates.public_payload_json.lane_plans` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | event levels, secondaries |
  | `outcome_target_invalid` | `sas_candidates` | publication | exclusion audit only |
  | control-candidate pool (non-published rows for night `t`) | `sas_candidates` | pick night, 16:05 ET | B2 pool |
  | `C_t`, ATR14, `beta60`, `atr_pct`, `runup20`, `d2`, `d4` | `prices_daily_split`, bars ≤ `t` | pick-night close, 16:00 ET | entry, distances, matching |
  | SPY tape (trailing return, trailing vol, expanding terciles) | `prices_daily_split`, SPY bars ≤ `t` | pick-night close | stratum |
  | regime label (v1.2, nights ≥ 2026-06-09, same-evening rows only) | `market_regime_daily` | pick night, 16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion; `E_AH` clock (sensitivity only) |
  | daily bars 1 … `b`; hourly bars for ordering rule 1 | `prices_daily_split`, `prices_hourly_raw` | each session's 16:00 ET close, sessions t+1 … t+40 | **EVENT classification, `a`, `b`** — and therefore population membership, control-set membership and where `X_b` sits: **outside the current rule-14 licence; the DP-05(c) exception requested above, decision time 09:30 ET on session `b+1`** |
  | `O_{b+1}` | `prices_daily_split` | session `b+1`, 09:30 ET | **decision basis `X_b`**, race levels — located by the classifier above, so covered by the same requested exception |
  | daily bars `b+1 … b+R` (`b+40` companion) | `prices_daily_split`, `prices_hourly_raw` | after the decision | **outcome measurement only** |

  **What `eval.py` must enforce:** the eligible-pick set, `a`, `b`, the EVENT label, every matched
  control and every stratum label are computed and written to a frozen per-pick **and per-control**
  table **before any bar dated after session `b` is loaded**; the run **fails** if any `b+1`-or-later
  field is referenced in eligibility, EVENT classification, matching or stratification, or if a bar
  from sessions 1 … `b` is referenced anywhere outside classification and the excursion panels.
  `sas_selection_excursion` / `outcome_*` / `level_hit_*` columns are **never inputs** — including
  `ran_then_dipped`, `peak_upside_level_before_dip` and `mae_from_peak_pct`
  (`services/sas_excursion.py:603-638`), which encode the first two legs of this very shape but on the
  close basis, on calendar windows, recomputed weeks later and subject to manual overrides
  (`:8-18`, `:336-354`; `routers/performance.py:935-970`; DATA_NOTES). They are not used, not even as a
  grading cross-check. `uoa_symbol_daily.fwd_return_*` is **banned** (FREEZE_v001 §5); no UOA table is
  used.

## 7. Multiple testing

- **Within the question:** **BH across m = 2** — E1 and E2 — at q ≤ 0.10; the verdict uses q.
  **`m = 2` is fixed at lock**: both primaries carry verdicts in every branch, and an endpoint short of
  floor still has its p computed, so `m` never falls and no bar is lowered for the survivor. Every
  secondary — B3, B4, the shallow-retrace arm, the other re-advance levels, the `R` = 10 / 40 clocks,
  the scale-out report, the proximity terciles, the adverse race, the tape-aligned control set and
  every sub-cell — prints raw p only, marked "descriptive, does not decide".
- **Across the family: F4 Price behaviour after selection.** F4 holds **H-030, H-031, H-033, H-034 and
  H-064**; H-063 is **merged into Q007** (DP-29) and H-032 was **re-filed to F6** with Q009, so neither
  is counted here. The correction set is **computed at the decision pass over the F4 primaries locked
  by then**; as drafted it is Q007 (4) + Q008 (3) + Q013 (2) + **Q020's 2** = **11**. H-033 is counted
  once, in F4. **While Q020 is DEFERRED (DP-41, header) it is not locked, so its 2 primaries are not in
  the F4 set — the correct F4 count without Q020 is 9** (Q007 4 + Q008 3 + Q013 2); the 11 applies only
  from a re-entry lock.
- **F6 companion correction for E2 (strictness, not a re-filing).** E2 contrasts a hold-versus-flatten
  plan on positions already open, which is F6's subject and the ground on which Q009 and Q012 were
  re-filed. Rather than argue the filing, the Reporter computes BH for E2 **also** across F6's
  registered primaries, and **q ≤ 0.10 is required in both families** for E2 to count as CONFIRMED;
  **the larger q is quoted**. As drafted the F6 set is Q003 (2) + Q009 (2) + Q012 (3) + Q015's 2
  companions + Q018 (4) + Q019 (2) + **E2** = **16**; **Q010 is excluded** as Q009's prospective
  replication of the same hypothesis. E1 is corrected in F4 only. **While Q020 is DEFERRED, E2 is not
  in the F6 set either — the correct F6 count without it is 15** (Q019 §7's figure); the 16 applies
  only from a re-entry lock.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q008 (F4, H-031)** asks whether a fast start predicts the *first* L4 touch and **stops there** —
    its own §7 names H-033 as "the after-L4 path". Q020 begins where Q008 ends: Q008's outcome is the
    first leg of Q020's conditioning event, on overlapping picks and nights, with the same `C_t` entry.
    The two are **not independent** and are never presented as two confirmations; neither `eval.py`
    reads the other's outputs.
  - **Q009 / Q010 (F6, H-032)** are the **adverse-side mirror** — stop touched first, then the target —
    and Q009 §7 says so in those words. Q020's first leg is favourable and its retrace line is a ladder
    target, not the printed stop; no stop is assumed anywhere here (DP-02).
  - **Q015 (F7, H-060)** tests L3-then-counter-level *within a score band*, with **no third leg**: it
    asks how often the shape happens and whether exiting at the touch pays, not what happens after the
    give-back. Q020 uses a deeper level, a different retrace line and adds the re-advance. Adjacent
    readings of one idea — *what a target touch is worth once it is handed back* — and they must never
    be counted as two confirmations.
  - **Q006 (F1)** owns the unconditional L4 touch rate against the same control construction; Q020's
    L4-touch rate is a decomposition factor, not a second test of it.
  - **Q012 (F6, H-066)** recycles capital into new picks; Q020 re-commits to the same pick. Different
    plan, different budget, different denominator.
  - **Q019 (F6, H-050)** is the only other registered question whose decision moment is after the pick
    night; its trigger is a monitor row and its estimand is an avoided move, not a re-advance.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1` in **percentage points** of re-advance rate (EVENT pick minus its event-matched controls);
`m2` in **ATR per trade** (the same contrast on plan RE-ADD). Both two-sided; the verdict carries its
sign. H-033 predicts `m1 > 0` and `m2 > 0`.

**MPE: E1 +5.0 pp** (DP-20, DP-44 — the standing number for a control-adjusted touch-rate endpoint; it
is a single control adjustment on one tape, not a difference of differences, so no uplift is proposed).
**E2 0.25 ATR** (DP-10, DP-44 — the standing number for every per-trade ATR-denominated endpoint),
measured **per EVENT trade and never rescaled** to a per-re-advancer or per-portfolio basis.

Per endpoint:

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **contributing nights ≥ 80** on the §2 definition **and ≥ 30 dated after the lock commit**
     (DP-24), **and ≥ 20 contributing nights for any sub-cell that is reported** — a sub-cell below
     floor is **SUPPRESSED** (counts only) and does **not** by itself make the endpoint INCONCLUSIVE;
  2. `|m| > MPE` (5.0 pp for E1; 0.25 ATR for E2);
  3. the deciding CI — the **wider** of the two bootstraps (§4) — excludes 0;
  4. BH q ≤ 0.10 within the question (m = 2) **and** within F4 — and, for E2, also within F6 (§7);
  5. the point estimate has the **same sign in both halves**, and neither half is beyond MPE in the
     opposite sign;
  6. **no tape stratum with ≥ 20 contributing nights is beyond MPE in the opposite sign**, and the
     result is not carried by a single tape stratum: the estimate must keep its sign in **every** tape
     stratum that clears 20 nights. A re-advance rule that only pays in a rising tape is a tape bet,
     not a ladder finding;
  7. **the tape-aligned guard.** The B2 contrast recomputed on controls with `|b_c − b| ≤ 5` sessions
     (§4) is **not beyond MPE in the opposite sign**. Picks and controls complete their round trips on
     their own schedules, so an unaligned control set can be graded across a different stretch of
     market; this clause stops that from manufacturing either sign. The aligned version is a guard, not
     a gate: it never has to clear a floor of its own, and its counts are printed;
  8. **the event-matched form is the verdict.** If the matched estimate is inside MPE while the
     unmatched total effect (B4) is beyond it, the endpoint is **NULL for the pullback claim** and the
     report says so in those words: the excursion that had already happened accounted for it (DP-12).
- **Both primaries must be CONFIRMED in the same sign for any rule to follow** (§9). E1 CONFIRMED with
  E2 NULL says the pick gets back to L4 more often than its look-alikes but not by enough to be worth
  0.25 ATR; E2 CONFIRMED with E1 NULL is a money result with no path behind it. Either mixed case is
  reported as **split**, not as a partial win.
- **The absolute gate, and what it licenses.** A `playbook/` line telling Haci to **hold or re-add**
  after the pullback requires E1 and E2 CONFIRMED **positive** *and* E2's absolute gate
  `g = mean_t mean_E[r_p]` with its 95% CI entirely **above** 0. A `playbook/` line telling him to
  **flatten the runner** at `X_b` requires E1 and E2 CONFIRMED **negative** *and* the gate's CI
  entirely **below** 0. The matched difference alone licenses neither: "beats a look-alike" is not
  "pays", and a trade that loses less than a look-alike is still a losing trade.
- **NULL:** floors met **and** the deciding CI includes 0 **and** `|m| < MPE`. "A pullback from L4 to L2
  says nothing about what happens next, once you match on the pullback" is a real finding, it retires a
  piece of trading folklore, and it is ledgered with the same care.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, a tape stratum beyond MPE in the
  opposite sign or the sign not held across strata, the tape-aligned guard beyond MPE in the opposite
  sign, `0 < |m| ≤ MPE` with the CI excluding 0 ("real but below MPE", rule 6), or the CI including 0
  with `|m| ≥ MPE`. A SUPPRESSED sub-cell is not by itself INCONCLUSIVE. **A gate shortfall is not
  INCONCLUSIVE either**: it fires the single DP-13 extension, then DEFERRED (§5).
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — ≥ 30 contributing nights dated
  after this file's lock commit (DP-24, DP-21), frozen in the successor manifests, never inspected
  earlier, reproducing the sign of both confirming endpoints under the unmodified `eval.py`. The clause
  does not weaken: if the window cannot supply 30, the DP-13 extension fires and then DEFERRED. No
  subscriber-facing statement before that (rule 10); even then the basis is NON_QUOTABLE until restated
  on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform **stores this shape and never asks what happens next**. `sas_selection_excursion`
computes `peak_upside_level_before_dip`, `mae_from_peak_pct` and `ran_then_dipped` — "peak ≥ L3 and a
deep counter-touch after" (volatilx `services/sas_excursion.py:603-638`; `models.py:2357`;
`docs/SAS_EXCURSION_BACKFILL.md:119` describes it as distinguishing "ran to L4 then pulled back") — but
it is a post-hoc diagnostic on the close basis and calendar windows, it is not shown to anyone, and
nothing anywhere measures the re-advance. The committed scale-out `BAND_EXITS`
(`scripts/generate_sas_trading_guide.py:89-95`) is fixed per score band with no path conditioning, the
2026-07-08 L4-trim ruling moved weight to L3 on an unconditional L4 rate
(`docs/SAS_EXIT_SCHEDULE_L4TRIM_RULING.md`; the card itself notes the premise is basis-dependent,
`services/sas_conviction_card.py:197-218`), and the Conviction Monitor — which already runs at 16:02 ET
every session — writes structure-break tiers, not ladder states.

Rules below fire only where §8 licenses one, and only after PROSPECTIVELY_CONFIRMED for anything
subscriber-facing (rule 10):

- **E1 and E2 CONFIRMED positive, gate CI above 0:** a `playbook/` line — *"a pullback from L4 to L2 is
  a hold, not an exit: re-commit at the next open and work the position back to L4"* — carrying the
  measured ATR per EVENT trade, the event-matched excess beside it (rule 5), and the EVENT rate so a
  reader knows how often it applies. Brief: an `INTERNAL_TOOL`, flag-off Conviction Monitor state
  `LADDER_PULLBACK` written at 16:02 ET on the session the pullback completes, surfacing
  `ran_then_dipped`'s shape on the traded basis, with the measured re-advance rate and the
  matched-control rate printed next to it. **Every check that brief hands the coding agent must be
  satisfiable from the platform repo alone (DP-49)** — the test suite, a pure-function import,
  `git show --stat`, a file diff; the "byte-identical checksum on the old path" check is written as
  **the diff that proves it**, never as "run the excursion job twice and compare", and anything that
  reads or writes `sas_selection_excursion`, `conviction_monitor` or any other table goes in the
  brief's verification section addressed to the **Data Steward on `$RESEARCH_DB_URL`**, or to Haci
  where a write is required. A `BAND_EXITS` trailing-rule clause that re-commits the
  residual comes only after prospective confirmation and needs its own strategist ruling.
- **E1 and E2 CONFIRMED negative, gate CI below 0:** the opposite `playbook/` line — the pullback is the
  end of the move, flatten the runner at the next open — and the L4-trim ruling's premise goes back to
  the strategist with this question's numbers attached, since a ladder that is reached and handed back
  is an argument about where the committed weight belongs. **That filing — and any `PLATFORM_ISSUES.md`
  entry that follows from it — must name DP-50(b) in the entry itself:** a repair touching
  `_extract_lane_plans` (`services/super_agent_select_service.py:94-161`) or the cross-lane re-sort
  (`:195-257`) is **flag-off until Q020's decision date** (the PI-011 / Q010 pattern), and if it ships
  inside the window anyway it takes a dated `DATA_NOTES.md` entry naming the column, the date range and
  the ship SHA, and the lane-plan payload becomes **two features split at the ship date** (DP-06
  pattern, DP-50(a)) — which moves the window start, mid-flight.
- **Split (one primary CONFIRMED, the other NULL), or a confirmed difference with the gate straddling
  0:** no rule, no guide line, no brief. The Ledger records the split, and the Reporter states which
  half failed and that "beats a look-alike" was not "pays".
- **NULL on the event-matched form with B4 large (§8 clause 8):** no ladder rule ships. The finding —
  "what happens after a deep pullback is what happens after any deep pullback" — is ledgered, and the
  card never implies that a pullback to L2 is an opportunity.
- **Both NULL:** `ran_then_dipped` stays an internal diagnostic and is never surfaced as a signal; the
  committed schedule stands; F4 effort moves to H-034.
- Owner: implementer. Ship flag-off with a byte-identical checksum on the old path; shadow ≥ 20 trading
  days before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **The conditioning event is the price path, so the naive contrast is an excursion contrast.** This is
   the dominant threat and it is why DP-12's event-matched control is the primary, why B4 is descriptive
   and why §8 clause 8 exists. A positive unmatched result would mean only that names which have run far
   and fallen back behave differently from names that did neither.
2. **Conditioning the controls on their own path selects the pool.** The control-EVENT pool is chosen by
   what the controls did, so picks whose look-alikes rarely complete the round trip drop out, and the
   EVENT picks that survive into E1/E2 are not a random subset. Every such pick is **dropped and
   counted, never back-filled and never substituted with an unmatched contrast**; the drop count and the
   dropped picks' `d2` / `d4` distribution are printed (R1 item 4 bounds it before lock), and if the
   drop rate is high the question speaks only for the picks whose look-alikes also round-trip.
3. **The remaining distance at the decision basis is matched only approximately.** Pick and control both
   pulled back to a line at the same ATR distance, but their next opens differ, so `rem` is not
   identical. The `rem` and `dep` terciles, the post-match standardized mean differences and the
   printed distributions are the reads on what is left.
4. **The ladder is not ATR-scaled and L2 and L4 come from different lanes.** Ladder prices are
   LLM-written from projection levels with no ATR scaling (`ai_agents/principal_agent.py:530-575`;
   fallback 0.5%/1% steps at `:897-911`), each lane relative to its own entry, and the platform states
   levels are not price-ordered across lanes (`services/sas_conviction_card.py:289`). The `d4 ≤ d2`
   exclusion is necessary but not random: the population becomes "picks whose lanes happen to be
   ordered". The share is printed by month and band, and `d2` / `d4` terciles are reported.
5. **Same-session round trips need hourly bars, and the coverage is asymmetric.** Where ordering rule 1
   cannot resolve `b = a`, the row is not an EVENT. Published symbols have near-complete hourly coverage
   (`STEWARD_Q015_exposure.md` §7 measured 100% on the comparable population) while about half of
   unpublished candidate symbols have none, so the rule bites the **control** side harder — which
   shrinks the control-EVENT pool and makes the test harder, not easier. Disclosed, counted per arm,
   with the opposite reading printed as a sensitivity that never decides, and never patched.
6. **Picks and controls complete their round trips on different sessions,** so an unaligned control can
   be graded across a different stretch of market. §8 clause 7's `|b_c − b| ≤ 5` guard is the defence,
   and the distribution of `b_c − b` is printed.
7. **One tape.** The window is June 2026 – April 2027 (June 2027 if the extension fires). A sign present
   in one half fails §8 clause 5, and clause 6 requires the sign to hold in every tape stratum with
   20+ nights. Nothing here speaks to the strong April–May tape, which is outside the window by design.
8. **Overlapping 60-session windows across adjacent pick nights** inflate precision badly — adjacent
   nights' windows overlap almost completely. The 30-session block length and the decision-session
   clustering are fixed here, before any result, and the **wider** CI decides.
9. **The stock path is a proxy for the spread.** A pullback and a 20-session re-advance is exactly where
   theta and IV decide a vertical's fate, and the desk holds no option prices
   (`research/questions/DEFERRED.md`; ENHANCEMENTS.md EN-011). **No §9 line may mention spreads** on the
   strength of this question.
10. **No stops are assumed** (rule 5, DP-02). A reader who stops out would very likely have been taken
    out during the retrace itself and would never reach the decision basis; the adverse-excursion panel
    and the `dep` distribution are how that reader judges the rule, and §9 must say so.
11. **A full unit position at `X_b` is a modelling choice.** Under `BAND_EXITS` a real position is partly
    scaled out by the time L4 is tagged, so the money a re-commitment makes depends on what is left. The
    primary uses the full unit because the control has no scale-out and rule 5 requires one basis on
    both sides; the residual-position version is printed beside it (§4; DECISIONS.md item 4).
12. **Registrar's incidental exposure, disclosed.** While fixing the level mapping the registrar read the
    conviction card's Select-tier note, which asserts an L4 first-touch rate of about 67% over the
    40-session swing window (`services/sas_conviction_card.py:207-218`). It is a platform-displayed
    number on the close basis over the full history including April–May, it is quoted in §5 only to show
    that the 0.35 planning rate is conservative, and **no threshold, window, level or definition in this
    file was taken from it**. No results directory was read.
13. **Null-ladder and void denominators — which picks this speaks for.** The question speaks for
    published picks carrying both a day-lane L2 and a swing-lane L4 on the correct side of the pick-night
    close, in a monotone order, that completed the round trip and had three usable look-alikes that did
    the same. Every step of that funnel is counted and printed, by month and by band.
14. **One database (DP-50).** `$RESEARCH_DB_URL` reads the rows the platform writes, so a repair that
    rewrites `public_payload_json` would change L2 and L4 for historical rows and split this column into
    two features (DP-50(a), the DP-06 pattern). Nights ≤ 2026-09-10 are pinned to `manifest_v001` and are
    safe by rule 4 (DP-50(d)); Q009 §R3 ruling 2 measured **no** historical payload rewrite across the
    795-row correction ledger; R1 item 7 re-checks for new ship dates, and any future repair touching
    lane plans must be checked against this question's decision date before a fix brief is written
    (DP-50(b)).
15. **Right-censoring is designed out, not handled.** The 60-session maturity is uniform and never a
    function of a pick's own path, so no EVENT and no outcome can be censored by its own timing; a pick
    that is short of 60 forward sessions is excluded before any classification runs, and counted.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Item 1 was **DEFAULTED to DEFERRED under DP-41** — the
recommendation in the draft (no exception needed) was **not** adopted, and §6 now carries the scoped
exception request instead; the question does not lock until Haci adds the scope to DP-05 as (c).
Items 2 (condition-first DP-12 control, minimum 3), 3 (re-advance = first L4 touch within R = 20
sessions of `X_b`) and 4 (full unit position at `X_b`, `BAND_EXITS` residual printed beside it) were
DECIDED as drafted and are **binding on re-entry**, as is item 8: the §5 schedule is recomputed from
the new lock date, never carried forward, with the window start fixed at 2026-06-01 and the `r`
threshold re-solved against the new 12-month ceiling. Corrections 1–4 are applied above.
Routed items still open: **R1 (Steward, exposure counts)** and **R2 (Steward, successor freezes)** —
both **HELD** behind the DP-05(c) grant and not to be run while Q020 is deferred.
