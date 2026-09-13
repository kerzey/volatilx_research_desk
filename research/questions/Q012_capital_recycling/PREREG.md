# Q012 — capital_recycling: for a pick below 90, is it better to take the first small target and put the money into the next pick, or to hold the committed scale-out?

**Status:** DRAFT (lock by committing this file) — nothing is open: every item is settled in DECISIONS.md (2026-09-13; autonomous run, items 5, 6 and 7 DEFAULTED under DP-40 / DP-42 / DP-43)
**Family:** **F6 Exits and execution** (hypothesis **H-066**, filed in F7 in `research/BACKLOG.md`; **re-filed to F6 under DP-29** — both primaries contrast two *exit plans* on the same picks, which is F6's subject, exactly as Q009 was re-filed from F4. F7 therefore holds 9 hypotheses and H-066 is **not** counted in both families. §7 nevertheless prints the F7 companion q and requires q ≤ 0.10 in **both** families.)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates.
**Decisions:** DECISIONS.md (recorded 2026-09-13, `record` pass folded in — 17 DECIDED, 3 DEFAULTED under DP-42 / DP-43, R1 CLOSED; R2 open, due at the decision date, not a blocker for lock)
**Measured exposure:** research/reports/STEWARD_Q012_exposure.md (R1, 2026-09-13; counts only, no outcome of any kind) — **517 eligible picks of 541 published rows** on the eligibility-criteria population, **495 LOW-or-HIGH picks**, **66 of 67 contributing start nights**, **42 of 67 both-band nights** (P2's own floor unit), ELITE 20 nights and declining, REF 1 night, hourly coverage 2,391 / 2,391 pick-sessions. Measured run-rates: **0.9429 contributing nights per session** and **0.6000 both-band nights per session**. **Every gate is decided on `eval.py`'s own measured counts** at the decision pass, never on R1 or on a projection.
**Registered by:** registrar · **Approved by:** desk (DP-46) · **Date:** 2026-09-13

---

## 1. Hypothesis (plain English)

**For a pick scoring below 90, the money works harder if you take the first day-target the pick
reaches and put it straight into the next pick, than if you hold that pick through the platform's
committed scale-out — and the advantage shrinks as the score rises, so the higher-scoring picks are
the ones worth holding.**

BACKLOG H-066 reads: *"Capital recycling by score band: a 'quick-exit' plan (enter at the actionable
price, exit at the first L1 or L2 touch, cap 5 sessions, redeploy) on sub-elite picks produces more
target-touches per unit of capital-time than holding the same picks for L3/L4, while elite (90+)
picks reward holding for L3–L6 — baseline: the same picks under the committed scale-out plan; the
matched control under the quick-exit plan."* It names no capital-time unit, no redeploy rule, no
treatment of the untraded `<80` band, and no decision. This PREREG fixes all of them (§2–§4). No
sign is presumed; every test is two-sided.

**Three things are tested as primaries** (§4), all on **published picks scoring 80–90** and all
measured over the **same 60-session capital budget for both plans**, so neither plan is given more
of the trader's money-time than the other:

- **(P1, the money)** does the recycle plan make more or less per capital slot than the committed
  scale-out, on the same picks and the same nights;
- **(P2, the band gradient)** is the recycle plan's advantage smaller in the 85–90 band than in the
  80–85 band — H-066's "band should decide hold length";
- **(P3, is it SAS)** does recycling *published picks* beat recycling distance-matched candidates
  the platform did not publish, under the identical plan.

**What this question does not test, stated up front.** The **elite (90+) half of H-066 carries no
verdict here.** DATA_NOTES records 12 / 8 / 3 / 2 elite picks per month since June and R1 measures
**exactly 20 ELITE contributing nights through 2026-09-09 on a declining monthly trend
(10 / 6 / 3 / 1)**, so the cohort sits on the 20-contributing-night sub-cell floor with no margin;
under **DP-43** it is **demoted to descriptive at lock** (a demotion at lock is never restored
afterwards), and whether it is **printed or SUPPRESSED** is decided at the decision pass on
`eval.py`'s own measured count against that floor (§5, §8). Either way it carries no verdict and
**BH stays at m = 3** (DECISIONS.md item 6). The `<80` band is likewise descriptive
(§2): the platform's committed schedule for it is literally *"not traded"*
(volatilx `scripts/generate_sas_trading_guide.py:94`), so there is no baseline plan to hold it under.
A verdict here speaks for **80 ≤ overall_score < 90 only**, and §9 binds the report to say so.

## 2. Population

- **Unit of inference: the trading night** (rule 6) — specifically the **slot-start night**. Slot
  rows are averaged within their start night first; the estimator is a within-night **paired**
  difference between two plans applied to the same picks, so the night's tape is held fixed.
- Source tables (manifest_v001 and its successors): `sas_candidates` (`qualified`, `selected_rank`,
  `overall_score`, `dominant_direction`, `best_timeframe`, `public_payload_json` →
  `lane_plans.{day_trading, swing_trading, longterm_trading}.targets`, `outcome_target_invalid` for
  the exclusion audit only), `sas_runs` (`finished_at`, for the DP-04 exclusion criterion and the
  descriptive `E_AH` sensitivity).
- Source tables (manifest_prices_v001 and its successors): `prices_daily_split` (pick-night close,
  session opens/highs/lows, forward bars, ATR14, beta60, run-up, SPY tape), `prices_daily_raw`
  (split-factor snapping only), `prices_hourly_raw` (same-session ordering of L1 vs L2 on published
  symbols, and the descriptive `E_AH` price).
- **Eligible pick (a pick that may fill a slot, in either plan):** `qualified IS TRUE AND
  selected_rank IS NOT NULL` (**DP-28**; dark-lane and qualified-false rows are never treatment
  rows), on a non-excluded night, carrying **all six committed ladder levels** —
  `L1, L2 = day_trading.targets[0..1]`, `L3, L4 = swing_trading.targets[0..1]`,
  `L5, L6 = longterm_trading.targets[0..1]` (volatilx `services/sas_conviction_card.py:182-195`) —
  each on the correct side of the pick-night close, with `overall_score` present and a
  bullish/bearish `dominant_direction`.
- **Cohorts (the platform's own bands, `scripts/generate_sas_trading_guide.py:78-95`):**
  **LOW** = 80 ≤ score < 85 · **HIGH** = 85 ≤ score < 90 · **ELITE** = score ≥ 90 (DP-42's
  definition of elite; descriptive only, §1) · **REF** = score < 80 (descriptive only). **LOW ∪ HIGH
  is the primary population.** **REF is measured at 1 of 579 published rows in the window** (TJX
  2026-06-11, score 79.58 — `STEWARD_Q012_exposure.md` §5): publication sits at an effective ~80
  gate, so the labelled 80-85 stand-in schedule (§3, §4) has essentially nothing to describe. REF is
  **SUPPRESSED** under the 20-night sub-cell floor and printed as a bare count (DECISIONS.md items 3
  and 6). The hold plan always uses the pick's **own** band row of `BAND_EXITS`
  (80-85, 85-88, 88-90, 90+); the LOW/HIGH grouping exists only for the slot queue and for P2.
- **Definitions (all prices in the signal-date split basis):**
  `C_t` = the pick's **actual** regular-session close on its pick night from `prices_daily_split`
  (never the platform's `spot_close`, stale on re-run nights — EXPLORE_001 §9);
  `ATR` = ATR14 from `prices_daily_split` bars dated ≤ the pick night (the platform's `atr_pct` is
  corrupted around splits — PI-003 / DATA_NOTES; not used);
  `dir` = +1 bullish, −1 bearish;
  `O_1` = the pick's session t+1 **official** regular-session open (`prices_daily_split.o`) — the
  **entry basis for every trade in this question**, picks and controls alike (**DP-03(b)**, the
  actionable price H-066 names; DP-11 does not apply because no position is already held. `C_t` and
  `E_AH` entries are descriptive sensitivities only, §4).
- **Exclusions — each counted per arm and printed in the results header, never silently dropped.
  Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or
  a measurement failure:**
  - nights in **`research/data/exclusions_v003.json`** — `manual_runs.trading_dates` ∪
    `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`. `eval.py`
    reads the JSON and unions the three lists; **no date is hard-coded** here or in `eval.py`
    (DP-22). Within the sealed part of this window those are 2026-06-26, 2026-07-02 and 2026-07-06.
  - any prospective night whose `finished_at` is later than the next session's open (DP-04, applied
    mechanically).
  - **null-ladder denominator:** picks missing any of the three lane plans or any of the six targets
    → not eligible, counted. **Measured** (`STEWARD_Q012_exposure.md` §2): 8 of 541 carry no lane
    plan at all, **all on the single night 2026-06-02**, and 8 more carry all three lanes but fail
    the six-target test (2 with a populated first and a null second day target — PM 2026-07-08,
    V 2026-07-28; 6 with an empty `day_trading.targets` list). The all-six-levels requirement
    removes **16 of 541 (3.0%)**, against Q011's 2.1% on the weaker one-target test (§10 threat 12).
  - picks with `outcome_target_invalid` non-null, or any committed level at or through `C_t` at
    publication (volatilx `services/super_agent_select_service.py:113-145`) → not eligible, counted.
    This test is made at the close, **before** any session t+1 price exists, so it is identical for
    both plans.
  - picks with no session t+1 bar, or missing forward bars inside the slot budget (halt, delisting)
    → ungradeable in both arms; excluded and counted. This is a **measurement failure, not a
    classifier**: it never moves a pick between arms. A start night is dropped if > 25% of its
    eligible picks are ungradeable.
  - symbols with fewer than 60 daily bars dated ≤ t (ATR / beta / run-up undefined) → excluded,
    counted.
  - start nights whose session **t+60** falls after the last trading date of the pinned price freeze
    (immature) → excluded and counted. Maturity comes **from the trading calendar**, never from
    whether a price exists; right-censoring is never graded as a non-touch.
- **Refill picks are inputs, not units.** A slot opened on night t may be refilled by eligible picks
  published on later nights inside its budget (§4). Those later picks are subject to the identical
  eligibility test, but they **add no contributing nights and no inferential n** — the unit is the
  slot's **start** night (rule 6).
- **Contributing night (the floor unit, DP-21):** a start night carrying **≥ 1 eligible LOW-or-HIGH
  pick whose slot is gradeable in both plans**. P1 and P3 share this definition. **P2's own
  contributing night is a start night carrying ≥ 1 gradeable slot in *each* of LOW and HIGH**
  ("both-band night") and is counted and gated separately (§5). A matured start night on which no
  slot survives the funnel is a **non-contributing night, not an exclusion**: it is never added to
  `exclusions_vNNN.json` and never counted toward any floor; it is printed in the funnel with its
  cause.

## 3. Baseline(s) — what this must beat

- **B1 (primary baseline, H-066's own): the committed scale-out on the same picks, same start
  nights, same 60-session capital budget, same entry** — Plan **H** in §4, i.e. the platform's own
  printed plan for that pick's band (`BAND_EXITS`,
  volatilx `scripts/generate_sas_trading_guide.py:89-95`). This is the "Y's rate when X did not
  happen" baseline in its cleanest form: the same picks, two plans, one tape. For the descriptive
  **REF** cohort there is no printed plan, so its hold arm uses the 80-85 row as an **explicitly
  labelled stand-in** — and R1 measures REF at **1 published row in the whole window** (§2), so the
  stand-in has essentially nothing to describe; REF is SUPPRESSED and printed as a bare count.
- **B2 (rule-5 distance-matched control; primary for P3):** for each pick in a chain, the **10
  nearest same-night non-published `sas_candidates` rows** — the complement of the DP-28 publication
  predicate — on `beta60` / `atr_pct` / `runup20` (from `prices_daily_split` bars dated ≤ that pick
  night; standardized by the night's cross-sectional median and MAD; Euclidean; with replacement
  across picks; ties by symbol ascending) — the **Q006 §3 / Q002 B1 construction verbatim** — each
  carrying **synthetic committed levels at the same ATR distances and the same direction** as the
  pick's L1…L6, anchored at the control's **own** pick-night close:
  `L_i,c = C_c × (1 + dir_p × d_i,p × atr_pct_c)` with `d_i,p = dir_p × (L_i,p − C_t,p)/ATR_p`,
  graded under exactly the §4 plans from the control's own session t+1 open and own forward bars.
  Control rows never add to inferential n (rule 6).
- **B3 (descriptive, cross-question reconciliation):** the same slots entered at `C_t` (the DP-03(a)
  after-hours proxy, DP-11 — the basis Q007 and Q009 use) and at `E_AH` (Q004's definition verbatim,
  picks only). Neither decides; both exist so Q012's numbers reconcile with the rest of the desk.
- **B4 (descriptive):** the same picks under a **no-redeploy** version of the quick-exit plan (the
  slot goes idle after the first exit and is never refilled). B4 isolates how much of any P1 effect
  is the *exit* and how much is the *recycling*; it is printed beside every P1 figure and decides
  nothing.

## 4. Objective metric (rule 5 — price path under a named execution plan)

**The capital slot.** Each eligible LOW/HIGH pick on a matured start night t opens one **slot**: one
unit of capital, committed on night t, with a budget of sessions **t+1 … t+60**. Sixty sessions is
the **long lane's own window** (`services/sas_conviction_card.py:194`), chosen so that the hold plan
— which puts 30–50% of a sub-elite position at L5/L6 — can **complete inside the budget**. A shorter
budget would truncate the baseline and flatter the hypothesis; the 20-session-budget version is
reported descriptively and labelled truncated. Both plans consume the identical budget, which is
what "per unit of capital-time" means here.

**Plan H (baseline, the committed scale-out).** Enter the night-t pick at `O_1`. Each fraction of
`BAND_EXITS[band(pick)]` exits at the **first touch** of its level within the budget, at the level
price — or at that session's open if the session opens through the level (a resting exit limit fills
at the better price). A fraction whose level is at or through `O_1` at entry is **unfillable** (rule
5: a target already passed at entry is not a hit): it is recorded, counted, and closed with the
remainder. The remainder closes at the session t+60 close. **No stop** (rule 5, DP-02). The written
trailing and max-hold text (`"loose trail on remainder after L5 · max hold 45d"`) is not
deterministic enough to simulate and is ignored (Q011 §4 precedent). The slot refills (below) only
if the position goes **fully flat** before the budget ends.

**Plan R (the tested rule, the quick-exit recycle).** Enter the night-t pick at `O_1`. Exit the whole
position at the **first touch of L1 or L2** (day-lane targets) within the trade's own 5-session cap,
at that level's price, or at the session's open if it opens through the level; if neither level is
touched by the close of the **5th session held**, exit at that close — H-066's own cap (DP-25). If
**both** L1 and L2 are at or through `O_1` at entry, the trade is **not takeable**: no position,
counted, and the slot refills at the next opportunity. When the slot goes flat on session s, it is
**refilled** on the first pick night t′ > s inside the budget by the **best-ranked (lowest
`selected_rank`, ties by symbol ascending) eligible pick of the same cohort**, entered at that pick's
own next-session open and traded under the same quick-exit rule; repeat until the budget ends. Any
position still open at session t+60 closes at that close (**truncated**, flagged and counted). If no
eligible same-cohort pick exists on any remaining pick night, the slot is **idle** for the remainder
(counted). **n(idle sessions) and n(idle slots) are printed separately for LOW and HIGH**, never
aggregated, beside the capital-occupancy counts of §10 threat 1: R1 §7 measures HIGH-band refill
supply missing on **25 of 67 sessions (37.3%)** against LOW's **1 of 67 (1.5%)**, so Plan R's idle
time is a HIGH-side phenomenon that an aggregate count would hide (DECISIONS.md items 1 and 18).
Slots are independent simulations and may hold the same later pick — this is a measure of
capital turnover per slot, **not** a portfolio backtest with position contention (§10 threat 7).

**Slot result (the money, in ATR).** `r_slot = Σ_trades Σ_fractions f × dir × (exit − entry) / ATR`,
each trade in its **own** pick's ATR, so the units are additive ATR per unit of capital committed on
night t. Idle time contributes 0.

**Ordering rules, stated once and applied by `eval.py` with no judgment:**
1. **L1 vs L2 in the same session (Plan R only).** Ordered with `prices_hourly_raw`; if one hourly
   bar holds both, or the symbol has no hourly bars in the freeze, the exit is taken at **L1** — the
   nearer level, i.e. the reading **less** favourable to the hypothesis (DP-27's convention applied
   to this pair; DP-45). Counts printed; the opposite reading printed as a named sensitivity.
   R1 §6 measures **100% hourly coverage** on the first five forward sessions of the published
   population (2,391 of 2,391 pick-sessions, 0 of 167 symbols missing), so this conservative reading
   is expected to apply almost only to **B2 control chains**, whose symbols sit outside the hourly
   freeze scope; the count is printed either way and hourly bars are never back-filled.
2. **Fractions of Plan H touching in the same session** need no ordering: each fraction exits at its
   own level price, so the order does not change the result.
3. **A level touched intraday on the entry session** counts (both plans), provided it was not at or
   through the entry open (rule 5, DP-26).
4. **Counter-direction levels and adverse excursion are measured and reported, never used as an
   exit** (rule 5, DP-02).

**Primary endpoints (three, pre-specified; BH within the question at m = 3 in every branch, §7).**
For slot i on start night t:

- **P1 — the money.** `Δ1_t = mean_i[ r_{R,i} − r_{H,i} ]` over all gradeable LOW ∪ HIGH slots on
  night t. Estimand **`m1 = mean_t Δ1_t`, in ATR per capital slot**. Positive = recycling pays.
- **P2 — the band gradient.** On **both-band nights** (§2),
  `Δ2_t = mean_{i ∈ HIGH}[ r_R − r_H ] − mean_{i ∈ LOW}[ r_R − r_H ]`. Estimand
  **`m2 = mean_t Δ2_t`, in ATR per capital slot**. H-066 predicts **negative** (the recycle advantage
  shrinks as the score rises); positive beyond MPE is a confirmed finding with the opposite sign.
  **P2's MPE is 0.50 ATR per capital slot — twice P1's and P3's** — because P2 is a difference of
  differences (HIGH's plan gap minus LOW's plan gap) measured on the thinner both-band nights, the
  shape Q007 §8 raised its MPE for citing Q003 §8; DP-10 permits a larger value with a stated reason
  and never a smaller one (§8; DECISIONS.md item 4).
- **P3 — is it SAS.** `Δ3_t = mean_i[ r_{R,i} ] − mean_c[ r_{R,c} ]`, published picks' recycle slots
  minus their **B2 matched-control** recycle slots on the same night (each pick's control slot = the
  mean of 10 parallel control chains, each started on one matched control and refilled by the nearest
  matched control of the cohort's next eligible pick, under identical rules and its own bars).
  Estimand **`m3 = mean_t Δ3_t`, in ATR per capital slot**.

**Secondary, descriptive, never decides:**
- **touches per slot** and the share of slots realizing ≥ 1 committed-level touch, both plans, both
  cohorts — H-066's literal "more target-touches per unit of capital-time": **descriptive, raw p
  only, does not decide; m stays 3** (DECISIONS.md item 2, DP-44 — a count endpoint gets no MPE and
  none is invented, and a touch that is not worth money licenses no rule);
- the **breakeven round-trip cost**: the per-trade cost, in ATR, that would erase a measured P1
  advantage, printed as a headline number beside P1, plus a grid of P1 net of 0.02 / 0.05 / 0.10 ATR
  per round trip. A measurement, not a threshold (§10 threat 2);
- **trades per slot**, sessions of capital occupancy per slot, idle sessions per slot, truncation and
  not-takeable counts, per plan and per cohort;
- **B4** (no-redeploy quick exit) beside every P1 figure; **B2 under Plan H**, and the
  control-adjusted difference-in-differences `(r_R − r_H)_picks − (r_R − r_H)_control`;
- **ELITE** and **REF** cohorts under both plans (REF's hold arm uses the 80-85 schedule as an
  explicitly labelled stand-in, since the guide does not trade `<80`) — **descriptive at lock and
  carrying no verdict**, and **SUPPRESSED below 20 contributing nights** on `eval.py`'s own measured
  count: **REF is already SUPPRESSED** (1 measured night, structural), **ELITE is decided at the
  decision pass** (20 measured through 2026-09-09, trend declining) — §5, §8;
- per-level first-touch rates L1…L6 within their own lane windows (20 / 40 / 60) and within the
  budget, picks and controls, from `O_1` — the rule-5 hit-rate table the plan result is reported next
  to; the decisive near-target speed claim belongs to **Q002 S1/S2** and is not re-decided here (§7);
- sessions-to-first-touch of L1 / L2 / L3; maximum adverse excursion per trade in ATR;
  counter-direction touches within the budget;
- **B3** (`C_t` and `E_AH` entries); the **20-session-budget** version of both plans (hold arm
  truncated, labelled); P1 in percent of price instead of ATR;
- close-to-close return at T+20 / T+60 — **fixed-horizon return is secondary and descriptive by rule
  5 and never decides**.

**Quotability:** 20/40/60-session bases → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** Night-level. **CI (decides):** stationary block bootstrap over the ordered
contributing start nights, expected block length **20 sessions** (slot budgets of 60 sessions overlap
heavily across adjacent start nights — a longer block than the desk's other path questions, chosen
for that reason and fixed here, not after seeing results); 2,000 resamples; the date-clustered
bootstrap CI is printed alongside. **p-value:** paired sign-flip permutation on the night contrasts
`Δ1_t`, `Δ2_t`, `Δ3_t`, 10,000 permutations, seed 20260913. Every estimate prints n(contributing
start nights), n(contributing start nights dated after the lock commit), n(slots), n(trades),
n(refills), n(truncated), n(idle slots), n(not takeable), n(unfillable fractions), n(hourly-unresolved
L1/L2 pairs), n(control chains) and n(excluded, by reason).

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing start nights per primary endpoint** and
  ≥ **20 contributing start nights per reported sub-cell**. A sub-cell below 20 nights is
  **SUPPRESSED** — no point estimate printed, not even "small n, directionally", counts only — and a
  SUPPRESSED sub-cell does **not by itself** make its endpoint INCONCLUSIVE (§8 clause 1). The weaker
  reading ("80 eligible nights with ≥ 20 contributing") is **not** used (DP-21). **No floor is ever
  lowered to hit a date.**
- **Binding maturity: 60 sessions** from each start night (the slot budget, §4).
- **Measured exposure — R1 is CLOSED** (`research/reports/STEWARD_Q012_exposure.md`, 2026-09-13;
  Data Steward, counts only, no outcome of any kind). On the eligibility-criteria population
  (published picks since 2026-06-01 with a session t+1 bar in the freeze, `exclusions_v003.json`
  applied, 67 non-excluded sessions through 2026-09-09): the §2 funnel leaves **517 eligible picks
  of 541**, the all-six-levels test removing only **16 of 541 (3.0%)** against Q011's 2.1% (§10
  threat 12 is answered and does not bite); **495 LOW-or-HIGH eligible picks** on **66 of 67
  contributing start nights**; **42 of 67 both-band nights** (P2's own floor unit), gated by HIGH-band
  publication since LOW is present on 98.5% of sessions; **ELITE 20 contributing nights** on a
  declining monthly trend (10 / 6 / 3 / 1); **REF 1 contributing night**; **hourly coverage 100%**
  (2,391 of 2,391 pick-sessions, 0 of 167 symbols missing); refill supply missing on **1 of 67**
  LOW sessions and **25 of 67** HIGH sessions. R1's measured counts **moved the window end and all
  three schedule dates out, never in** (DP-43, DP-45); they decide no endpoint.
- **Projection (mechanical, gates nothing) — on Q012's own measured rates.** R1 §4
  measures **0.9429 contributing (LOW-or-HIGH) nights per session** and **0.6000 both-band nights
  per session** over 2026-06-01..2026-09-09:
  - **80 contributing nights (P1, P3):** the 80th contributing start night projects to
    **2026-10-01**, matured (+60 sessions, +1 week, next Monday) **2027-01-04**. **Not binding.**
  - **80 both-band nights (P2):** the **binding** endpoint. The 80th both-band start night projects
    to **2026-12-10**, which is what sets the window end below; any earlier end would have printed P2
    INCONCLUSIVE (floor) with the sample a couple of weeks away. At that end the projection is
    **≈ 81 both-band nights** — it clears 80 by about one night, which is thin by construction, since
    DP-43 sets the window at the *earliest* date the floor is projected to be reached; DP-13's
    automatic +30 sessions (≈ 18 further both-band nights) is the stated remedy and needs no new
    decision.
  - **30 contributing start nights dated after the lock commit (DP-24):** the **63** post-lock
    sessions 2026-09-14..2026-12-10 project **≈ 59** contributing nights and **≈ 38** post-lock
    both-band nights. **Not binding, with margin.**
  - **Total at the window end:** ≈ **123** contributing start nights (P1 / P3) and ≈ **81** both-band
    nights (P2).
  - **ELITE** is **demoted to descriptive at lock under DP-43** and carries no verdict; whether it is
    **printed or SUPPRESSED** is decided at the decision pass on `eval.py`'s own count against the
    20-night sub-cell floor (R1 measures 20 through 2026-09-09, trend declining). **REF** is
    SUPPRESSED — 1 measured night, structural (§2). **BH stays at m = 3** either way (§1, §7, §8).
  Every gate below is decided on the **measured counts printed by `eval.py`** from the frozen data at
  the decision pass, never on this projection and never on R1.
- **Window, decision date, extension and DEFERRED fallback (DP-43; DP-13; no outcome is looked at at
  any point):**
  - **Primary window: slot-start nights 2026-06-01 .. 2026-12-10 inclusive**, after exclusions
    (start ≥ 2026-06-01 per DP-06 and §6). *Why this end date:* DP-43 sizes the window on **every**
    primary endpoint's floor, and R1 measures P2's both-band nights at **0.6000 per session**, putting
    the 80th both-band start night at **2026-12-10**. Refill picks are drawn from pick nights inside
    each slot's budget, i.e. through **2027-03-10** (the 60th session after 2026-12-10), and add no n.
  - **Decision date: Monday 2027-03-22.** The 60th session after 2026-12-10 is **2027-03-10**
    (2026-12-25, 2027-01-01, 2027-01-18 and 2027-02-15 closed); plus the one-week freeze margin =
    2027-03-17, and the first Monday on or after it is 2027-03-22. The Steward fixes the exact
    session-count date when building the successor freezes, and a correction may move it **out, never
    in**. `eval.py` is written once (rule 9) and run **once**, then. **No interim looks.** A shorter
    window or a truncated budget that reached a date sooner was not taken (DP-43, DP-45); the date
    sits 6.3 months after lock, inside DP-43's 12-month ceiling.
  - **Both gates, per primary endpoint, on measured counts.** An endpoint is evaluated only if it has
    **≥ 80 contributing start nights** (P1 and P3: a start night with ≥ 1 gradeable LOW-or-HIGH slot;
    **P2: a both-band night**) and **≥ 30 contributing start nights dated after this file's lock
    commit** (DP-24). A shortfall on one endpoint is never covered by another's count.
  - **One automatic extension (DP-13; DP-43's +30 sessions), triggered by *any* primary endpoint.**
    If **any of P1, P2, P3** is short of either gate at 2027-03-22 on `eval.py`'s measured counts, the
    window extends **once**, automatically and with no new question, to start nights
    **2026-06-01 .. 2027-01-26** (= 2026-12-10 + 30 sessions: 14 in December, 16 in January),
    decision date **Monday 2027-05-03** (2027-01-26 + 60 sessions = 2027-04-22 with 2027-03-26 Good
    Friday closed, plus the same one-week margin = 2027-04-29, next Monday; the Steward fixes the
    exact date). The trigger is not restricted to P1: this window is sized on **P2's** floor, so a
    P1-only trigger would print P2 INCONCLUSIVE on a one- or two-night miss with the sample a few
    weeks away. The extended run uses the **unmodified `eval.py`** and the same gates. Both dates are
    inside DP-43's ceiling (6.3 and 7.7 months from lock).
  - **DEFERRED fallback.** If **P1's** gates are still short after that single extension, Q012 goes
    to **DEFERRED** (`research/questions/DEFERRED.md`, with the measured counts) rather than running
    under-powered. There is no second extension and no gate is reduced. A gate shortfall is never
    INCONCLUSIVE for P1.
  - **After the extension, P2 and/or P3 still short while P1 is met:** that endpoint is reported
    **INCONCLUSIVE (floor)** with its counts and no point estimate; the question still runs on the
    endpoints that meet their gates, and **BH runs across m = 3 regardless**, so no surviving
    endpoint's bar is lowered (Q009 precedent).
  - **Nothing weakens.** No floor is lowered to hit a date, and a short count never licenses falling
    back to a descriptive endpoint as a verdict.
- **Freeze discipline (DP-23; routed request R2 — due at the decision date, not a blocker for lock).**
  Nights ≤ 2026-09-10 stay pinned to `manifest_v001` / `manifest_prices_v001`. Later nights enter
  only through successor freezes — `manifest_v002` (selections, same SQL, same exclusion criterion)
  and `manifest_prices_v002` (same Alpaca queries) — with three scope requirements this question
  cannot do without: (i) the **selection** freeze must cover pick nights through the refill horizon
  **2027-03-10** (**2027-04-22** if the DP-13 extension fires), because slots started at the window
  end are refilled from picks published after it; (ii) the **price** freeze must carry **every
  candidate symbol, published and unpublished** (B2 chains need the unpublished symbols' opens and
  forward bars), through **60 forward sessions** beyond the last start night, i.e. through
  **2027-03-10**; (iii) **hourly bars scoped to at least the published-pick symbols**, as
  `manifest_prices_v001` was (ordering rule 1 and the `E_AH` sensitivity) — R1 §6 measured 100%
  hourly coverage on that scope, and if the scope changes, ordering rule 1's conservative fallback
  stops being near-empty and the report must say so. The same pass re-reports the ELITE
  contributing-night count on the full window. `eval.py` takes the window start and end, the manifest
  paths, the exclusions-file path and the output directory as inputs — **no hard-coded dates,
  manifest names or paths** — so the byte-identical script serves both runs, and it records every
  sha256 and prints pre-lock and post-lock night counts separately. Control symbols missing hourly
  bars fall to ordering rule 1's stated reading and are counted, never back-filled.
- Sub-cells (LOW / HIGH / ELITE / REF; bull / bear; tape stratum; regime label; `atr_pct` tercile; L1
  ATR-distance tercile; month) are reported only where they clear **20 contributing start nights**.
  **REF is SUPPRESSED on R1's measured count** (1 night); ELITE, REF-bear and bear cells are expected
  to be SUPPRESSED, and ELITE's print-or-suppress status is decided at the decision pass on
  `eval.py`'s own count.

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — slot-start nights ≥ 2026-06-01** through the window end
  in §5.
  *Justification (one sentence):* EXPLORE_001 ran near-target speed, level-touch and band tables on
  April–May and reported them into the backlog — H-066's own line quotes in-sample counts (280 picks
  / 35 nights, elite 15 / 13) — so the in-sample nights are contaminated for this question and are
  not used, not even as a descriptive panel.
  *Contamination check on the sealed period (registrar; **no results directory was read**):* the
  desk's sealed-period descriptive outputs recorded in `research/BACKLOG.md` (the weekly-snapshot
  lines under H-010, H-011, H-051, H-062) report band-level and lane-level **fixed-horizon returns**
  and some L1/L2 touch shares on the sealed window; none reports a plan-versus-plan result, a
  capital-slot figure, a recycle chain or a touch count per unit of capital-time, and none supplied a
  threshold here — the 5-session cap and the L1-or-L2 exit are H-066's own (DP-25), the band edges are
  the platform's `BAND_DEFS`, the 60-session budget is the platform's long-lane window, and the
  committed fractions are the platform's `BAND_EXITS`. The residual exposure is disclosed rather than
  corrected for: H-051's snapshot ranks lanes on T+20 return over the sealed window, which is
  adjacent to "short holds did better", and Q002's registered near-target speed claim is measured on
  overlapping nights (§7).
- **Catalyst-layer regime change:** the window sits entirely after the 2026-06-01 fix
  (`exclusions_v003.json` `catalyst_layer_regime_change`; platform commit 69ef05f) — DP-06.
- **Split for "holds in both halves":** Half A = contributing start nights on or before the median
  contributing start-night date; Half B = after. `in_sample_end = 2026-05-29` marks only what is
  excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v003.json` `regime_label_point_in_time_from`). It is used only for start nights
    ≥ 2026-06-09, only `regime_version = 'v1.2'`, and only where the row is a same-evening write per
    its declared availability; a later-posted row is treated as missing. Start nights
    2026-06-01..06-08 carry no legal label and are stratified by the SPY proxy only, flagged.
  - Primary tape stratum for every start night, trailing and legal at 16:05 ET: `tape_t` = sign of
    SPY's trailing 20-session return × tercile of SPY's trailing 20-session realized volatility, from
    SPY bars dated ≤ t in `prices_daily_split`. **Tercile cut points are expanding-window** (for
    night t, computed from every session 2026-03-02..t), so no later night's data sets an earlier
    night's stratum. Cells < 20 contributing nights SUPPRESSED.
  - Because a slot spans 60 sessions, its start-night tape stratum labels the **entry**, not the
    whole holding period; the report says so and prints the SPY path across each stratum's slots.
  - The report describes the tape in words from SPY's path and never implies a regime label existed
    before 06-09.
- **Knowledge time (rule 14) — every input declared. Q012 needs no rule-14 exception and requests
  none (DP-05 untouched; DP-41 respected).** Both plans are fully specified at 16:05 ET on the start
  night; cohort, levels, ATR, direction and every stratum come from the start night or earlier; no
  later quantity classifies, filters, matches or stratifies any slot. **The refill rule is
  knowledge-time-legal by construction:** a slot refills only *after* it is flat, using the pick list
  published at 16:05 ET on that later night — a decision a trader could make at that moment, never a
  choice among later nights made with hindsight. Fills, touches, truncations and idle time are
  **execution and outcome measurement**, the same status Q007 §6.1 and Q011 §6 give them.

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | eligibility, cohort, refill order |
  | day / swing / long lane plans, L1…L6 | `sas_candidates.public_payload_json.lane_plans` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | committed levels, both plans |
  | committed exit fractions | `scripts/generate_sas_trading_guide.py:89-95` (`BAND_EXITS`) | platform constant at the pick date | Plan H |
  | `outcome_target_invalid` (audit only) | `sas_candidates` | set at publication for new rows | exclusion |
  | control-candidate pool (non-published rows for that night) | `sas_candidates` | pick night, 16:05 ET | B2 |
  | `C_t`, ATR14, beta60, runup20, level ATR distances | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | distances, matching, denominators |
  | SPY tape (trailing return, trailing vol, expanding terciles) | `prices_daily_split`, SPY bars ≤ t | pick-night close | stratum |
  | regime label (v1.2, nights ≥ 2026-06-09, same-evening rows only) | `market_regime_daily` | pick night, 16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion; `E_AH` clock (sensitivity) |
  | session t+1 open; sessions t+1..t+60 bars; hourly bars on trade sessions | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **execution and outcome only** |

  **What `eval.py` must enforce:** the eligible-pick set, both plans' parameters and every stratum
  label are computed and written to a frozen per-pick table **before any session t+1 or later bar is
  loaded**; the run fails if any t+1-or-later field is referenced in eligibility, cohort assignment,
  matching, refill ordering or stratification. `sas_selection_excursion` / `outcome_*` /
  `level_hit_*` columns are never inputs (calendar windows, close basis, recomputed weeks later —
  volatilx `services/sas_excursion.py:8-18`, `:336-354`). `uoa_symbol_daily.fwd_return_*` is
  **banned** (the May–June freeze is not fixed — FREEZE_v001 §5); no UOA table is used.

## 7. Multiple testing

- **Within the question:** **BH across m = 3** — P1, P2, P3 — at q ≤ 0.10; the verdict uses q.
  **m = 3 in every branch**: an endpoint short of its floor still has its p computed and included, so
  no surviving endpoint's bar is lowered (Q009 precedent). All secondaries — the touch counts, the
  breakeven cost, B4, the control DiD, the elite and REF cohorts — print raw p only, marked
  "descriptive, does not decide".
- **Across the family: F6 Exits and execution** (DP-29 — both primaries contrast two exit plans;
  H-066 is re-filed from F7, the Q009 precedent, and is **not** counted in both). F6 holds H-050,
  H-051, H-032 and H-066; registered F6 questions at registration: **Q009 (H-032, 2 primaries)** —
  **Q010 is the same hypothesis's prospective replication and is not a second F6 question** — and
  **Q012 (H-066, 3 primaries)**.
- **Strict two-family rule.** Because the re-filing moves this question into the smaller family, the
  Reporter also computes the **F7 companion q** (F7's registered primaries: Q002 3, Q004 2, Q011 4,
  plus these 3) and a CONFIRMED verdict requires **q ≤ 0.10 in both families**. The larger q is the
  one quoted.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q002 (F7):** owns the decisive near-target speed claim (L1/L2 within 2 sessions vs the identical
    B2 control). Plan R's exit *depends* on that same event at a 5-session cap, so Q012's L1/L2 touch
    tables are **descriptive here and never a second confirmation of speed**; the Reporter
    cross-references.
  - **Q006 (F1):** owns the per-level picks-vs-control touch profile from the next open; P3 uses the
    same matched-control construction on a plan result rather than a level, and the two are **not
    independent evidence**.
  - **Q011 (F7) / Q004 (F7):** own the entry-basis question. Q012 holds the entry fixed at the next
    open for both plans, so any entry effect differences out of P1 and P2.
  - **Q009 / Q010 (F6, same family):** stop-based exits on overlapping nights; Q012 uses no stop
    (DP-02). Different endpoints, same family, corrected together.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1`, `m2`, `m3` are night-averaged contrasts in **ATR per capital slot** over a 60-session budget.

**MPE: 0.25 ATR per capital slot on P1 and P3; 0.50 ATR per capital slot on P2.** P1 and P3 are
level contrasts and take the standing number for a per-trade ATR-denominated endpoint (**DP-10**,
**DP-44**), with the **slot as the trade unit**: one slot is one capital-allocation decision taken on
the start night, which is exactly the decision H-066 proposes to change, and both plans consume the
identical 60 sessions of that capital. **P2 carries twice that, 0.50 ATR per slot, because it is a
difference of differences** (HIGH's plan gap minus LOW's plan gap) measured on the thinner both-band
nights — the exact shape Q007 §8 raised its MPE for (10.0 pp = 2 × DP-20, "a difference of
differences with small cells", citing Q003 §8); DP-10 permits a larger value with a one-line reason
and never a smaller one (DECISIONS.md item 4). No MPE is invented in money units and none is asked
(DP-44). All three are two-sided: H-066 predicts `m1 > 0`, `m2 < 0`, `m3 > 0`, and a result beyond
MPE with the opposite sign is a confirmed finding with that sign.

Per endpoint (two-sided; the verdict carries its sign):

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **contributing start nights ≥ 80** for that endpoint (P2 counts both-band nights) **and ≥ 30
     dated after the lock commit**, on measured counts, **and ≥ 20 contributing nights for any
     sub-cell that is reported** (DP-21) — a sub-cell below floor is **SUPPRESSED** (counts only) and
     does **not by itself** make the endpoint INCONCLUSIVE; the stratification protection rule 7
     requires lives in clauses 5 and 6;
  2. `|m| >` that endpoint's MPE — **`|m1| > 0.25` and `|m3| > 0.25` ATR per slot; `|m2| > 0.50` ATR
     per slot** (the difference-of-differences uplift, above);
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 **within the question (m = 3) and within both families** (§7);
  5. the point estimate has the **same sign in both halves**, and neither half is beyond MPE in the
     opposite sign;
  6. no tape stratum with ≥ 20 contributing nights is beyond MPE in the opposite sign.
- **NULL:** floors met **and** 95% CI includes 0 **and** `|m| < MPE`. "Recycling sub-elite picks is
  worth no more than holding them" is a real finding, kills a plausible trading rule, and is ledgered
  with the same care as a positive.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, a tape stratum with ≥ 20 contributing
  nights beyond MPE in the opposite sign, `0 < |m| ≤ MPE` with the CI excluding 0 ("real but below
  MPE", rule 6), or CI including 0 with `|m| ≥ MPE`. **A floor shortfall on any of P1, P2, P3 first
  fires the single DP-13 extension** (§5). **After** the extension: a shortfall on **P2 or P3** is
  reported **INCONCLUSIVE (floor)** with counts only, while a shortfall on **P1** sends the question
  to **DEFERRED** and is **not** an INCONCLUSIVE verdict. No gate is reduced at either step.
- **What licenses a rule.** A guide line or platform change requires **P1 CONFIRMED**, and its
  wording is bounded by P2 and P3:
  - **P1 CONFIRMED, P2 NULL:** one hold-length rule for the whole 80–90 range; the report may **not**
    say the rule is band-dependent.
  - **P1 and P2 both CONFIRMED (with P2 negative):** a band-dependent hold-length rule inside 80–90,
    stated only for the two bands measured.
  - **P3 NULL or negative:** the effect is a **plan effect available on any comparable stock**, not a
    SAS edge. An internal execution rule may still follow (it is still Haci's money), but **no
    subscriber-facing or marketing claim of a selection edge may be made from it**, and the report
    must say so in its first sentence.
  - **P1 CONFIRMED negative** (holding beats recycling) is equally actionable and is written up with
    the same force.
  - **The breakeven round-trip cost is printed in the same sentence as any confirmed P1.** Plan R
    takes several times as many trades as Plan H, and the stock-path proxy charges nothing for them
    (§10 threat 2); a rule whose breakeven cost is below plausible slippage is reported as **not
    tradeable at this size** even when CONFIRMED.
- **Elite (90+) never carries a verdict in this question** (§1, DP-43 — demoted at lock, never
  restored afterwards). Any statement about holding elite picks is descriptive, printed only if
  `eval.py` measures ≥ 20 contributing ELITE nights at the decision pass and SUPPRESSED otherwise,
  and needs its own PREREG once elite counts allow. **REF (`<80`) is SUPPRESSED** on R1's measured
  count (§2). **BH stays at m = 3** in either case, so no surviving endpoint's bar moves.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5 — the 63 post-lock sessions
  2026-09-14..2026-12-10 project ≈ 59 contributing nights and ≈ 38 post-lock both-band nights against
  DP-24's 30) — it requires **≥ 30
  contributing start nights dated after this file's lock commit** (DP-24, DP-21), frozen in the
  successor manifests and never inspected earlier, reproducing the sign of the confirming endpoint
  under the unmodified `eval.py`. The clause does not weaken: if the window cannot supply 30, the
  DP-13 extension fires and then DEFERRED. No subscriber-facing statement before that (rule 10); even
  then the basis is NON_QUOTABLE until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform prints **one committed scale-out per band** and no statement about capital
turnover at all: `BAND_EXITS` (volatilx `scripts/generate_sas_trading_guide.py:89-95`) already
encodes a band gradient in *shape* — 80-85 takes 10% at L1 and front-loads, 85-88 and 88-90 take
nothing at L1 and weight L5/L6, 90+ puts 70% at L5/L6 — but that gradient is a **strategist ruling**
(`docs/SAS_EXIT_SCHEDULE_L4TRIM_RULING.md`, 2026-07-08), not a measured result, and nothing anywhere
measures what a slot of capital earns per unit of time under it. The conviction card reports
first-touch rates per level (`services/sas_conviction_card.py:178-195`) and never the money.

Rules below fire only where §8 licenses one, and only after PROSPECTIVELY_CONFIRMED for anything
subscriber-facing (rule 10):

- **P1 CONFIRMED positive (recycling pays):** a Manual Trading Guide line — "below 90, take the first
  day-target the pick reaches (5-session cap) and put the money into the next pick; the committed
  scale-out is for the top band" — printed with the measured ATR per slot, the trades per slot and
  the **breakeven round-trip cost** beside it. Brief: a **flag-off** `recycle_plan` block in the lane
  payload and on the pick card for the 80–90 bands, showing the quick-exit rule next to the committed
  schedule, with the committed schedule remaining the default until the flag flips.
- **P1 + P2 CONFIRMED:** the guide line becomes band-dependent inside 80–90, and a brief proposes a
  measured revision of the `BAND_EXITS` rows for 80-85 and 85-88/88-90 — the first time that table
  would be set by measurement rather than by ruling. Ship flag-off with a byte-identical checksum on
  the old path; shadow ≥ 20 trading days (rule 11).
- **P1 CONFIRMED negative (holding pays):** the opposite line — "do not flip sub-elite picks at L1/L2;
  the committed schedule earns more per unit of capital-time" — and the guide's front-loaded 80-85
  row goes to the Red Team as a candidate defect (PLATFORM_ISSUES, not a research question, DP-07).
- **P3 NULL with P1 CONFIRMED:** internal playbook only (`playbook/`), no subscriber-facing claim, and
  the report leads with "this is a plan effect, not a selection edge".
- **All three NULL:** no change; the guide records that, at this size, recycling sub-elite picks is
  worth no more than holding them, and F6 effort moves to H-050.
- **Not licensed by any outcome here:** anything about the 90+ band, anything about `<80`, and any
  option structure (the desk holds no option prices — `research/questions/DEFERRED.md`, EN-011).
- Owner: implementer. Shadow ≥ 20 trading days before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **Recycling manufactures exposure, and a rising tape pays for exposure.** Plan R holds a
   position for a larger share of a trending 60 sessions than Plan H does only if its exits are
   quickly refilled; in a one-way tape more trades is mechanically more money, and the whole window
   is a single tape. Mitigations, all pre-specified: **P3** runs the identical machinery on
   distance-matched non-published candidates, where the same mechanical advantage appears on both
   sides; tape strata are reported; sessions of capital occupancy per slot are printed for both
   plans so a reader can see whether the contrast is exposure or selection.
2. **The stock-path proxy charges nothing for turnover, and Plan R trades several times as often.**
   This is the single largest threat to a positive P1. The **breakeven round-trip cost** is printed
   with every P1 figure and §8 binds the report to it; a cost grid (0.02 / 0.05 / 0.10 ATR) is
   printed beside it. No cost number is invented as a threshold (DP-44).
3. **Slot budgets overlap heavily.** Sixty-session budgets on adjacent start nights share most of
   their trades, so precision is overstated by any independence assumption; the block length is fixed
   at 20 sessions here, before any result.
4. **Chains inside a cohort converge.** After the first exit, every slot of a cohort refills from the
   same best-ranked pick, so slots differ mainly in their first trade. The start night remains the
   inferential unit (rule 6) and the effective information per night is smaller than the slot count
   suggests; slot counts and trade counts are printed separately so nobody reads slots as n.
5. **Independent slots ignore contention.** A real portfolio cannot put every slot into the same
   refill pick at the same size. This is a per-slot turnover measure, not a portfolio backtest, and
   §9's guide line must say so.
6. **Truncation and idle time cut both ways.** A Plan H position open at session t+60 is closed at
   that close (not at a target), and a Plan R slot with no refill available sits idle at 0. Both are
   counted and printed; the 20-session-budget version is reported so the reader can see how much of
   the result is budget length.
7. **The `<80` exclusion removes the band where quick exits should look best.** The guide does not
   trade `<80`, so there is no committed baseline for it; **settled: `<80` is descriptive against a
   labelled 80-85 stand-in and never enters a primary** (DECISIONS.md item 3). R1 also shows the
   threat is close to empty in practice — 1 sub-80 published row in 579 (§2), publication sitting at
   an effective ~80 gate.
8. **Elite is thin and shrinking** (DATA_NOTES: 12 / 8 / 3 / 2 picks per month since June; R1
   measures 20 contributing ELITE nights through 2026-09-09 on a 10 / 6 / 3 / 1 monthly trend).
   H-066's
   elite half is the half Haci is most likely to anchor on and is exactly the half this question
   cannot decide; §1, §8 and §9 all say so, and the cohort is SUPPRESSED below 20 nights rather than
   reported small. Why elite is thinning is Q005.
9. **Ladder levels are not ATR-scaled** (volatilx `ai_agents/principal_agent.py:530-575`; fallback
   0.5%/1% steps at `:897-911`), so "first touch of L1 or L2" is partly a distance test and the
   quick-exit plan's speed varies with how close the LLM happened to place the day targets. The L1
   ATR-distance tercile cell is reported and B2 inherits the identical ATR distances.
10. **Both plans are equity paths; Haci trades spreads.** Theta, IV and strike width are not modelled,
    and a plan that closes in 3 sessions has a very different option P&L from one that runs 60. Any
    §9 line about options must say so (EN-011; DEFERRED).
11. **Hourly-bar coverage decides ordering rule 1.** `manifest_prices_v001` carries hourly bars for
    published-pick symbols only (227 symbols), so control chains are graded on daily bars with the
    stated conservative reading; coverage counts are printed in both runs and never back-filled.
    **Measured** (R1 §6): 100% on the published side (2,391 of 2,391 pick-sessions, 0 of 167 symbols
    missing), so the fallback should be near-empty for picks and is a control-chain issue only — the
    successor price freeze must keep the same hourly scope (§5 R2 item iii).
12. **Null-ladder denominator — measured and answered.** This question needs **all six** committed
    levels, a stricter requirement than any registered question had measured; R1 §2 finds the test
    removes **16 of 541 published rows (3.0%)**, against Q011's 2.1% on the weaker one-target test,
    and the genuine "first target present, second null" gap is **2 rows**. The eligible population is
    therefore not materially smaller than Q011's funnel suggested. The funnel is printed with the
    verdict.
13. **The refill freeze extends past the window.** Slots started near the window end are refilled from
    picks published after it; if the successor selection freeze stops at the window end, those slots
    silently go idle and Plan R is understated. §5's R2 makes the extension explicit and `eval.py`
    prints the count of refills that found no freeze row.
14. **Matching on 3 features may not span selection** (Q006 threat 1). Post-match standardized mean
    differences are printed for every control chain start.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: R2 (successor freezes
`manifest_v002` / `manifest_prices_v002`, selection scope through the refill horizon 2027-03-10),
due at the decision date and not a blocker for lock. R1 is CLOSED
(`research/reports/STEWARD_Q012_exposure.md`, folded into §2, §4, §5, §8 and §10).
