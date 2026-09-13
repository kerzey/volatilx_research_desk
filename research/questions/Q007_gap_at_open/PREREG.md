# Q007 — gap_at_open: for a pick already held from the pick-night close, does a next-morning gap of more than 2% predict the rest of the trade?

**Status:** DRAFT (lock by committing this file after Haci review; see "Decisions before lock" at the end)
**Family:** F4 Price behaviour after selection (hypothesis H-030; H-063 is **merged into this question** — §7, DP-29)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v002.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates. See §2.
**Registered by:** registrar · **Approved by:** haci (pending lock) · **Date:** 2026-09-12 (decisions applied 2026-09-13)
**Decisions:** DECISIONS.md
**Human decisions recorded:** 2026-09-12 — Haci: (1) Rule 14 exception scoped to gap-group classification only (§6.1); (2) entry basis = **pick-night close `C_t`**, gap groups kept (§4; DP-11); (3) primary clock = **L3 within 20 sessions** (question A → DP-09, §4); (4) MPE for per-trade ATR endpoints = **0.25 ATR** (question B → DP-10, §8). 2026-09-13 — Haci: (5) primary design variant = **B, the gap-matched same-night control** ("strip the gap out"; question D → DP-12, §4.1), A and C descriptive; (6) **hard stop 2027-06-30**, both arms stay primary under variant B (question E, §5; it supersedes both earlier stop dates).

---

## 1. Hypothesis (plain English)

**If you bought a SAS pick at the pick-night close, a next-morning open more than 2% against the
pick — or more than 2% in its favour — tells you something about how the rest of that trade will go
(how often it reaches the swing target L3, and what a trade held to L3 makes), compared with picks
from the same night that opened roughly flat.**

This is a **hold / exit / add** question about a position that is already open when the gap
appears, not a question about whether to enter. BACKLOG H-030 reads "Day-1 gap >2% at open vs flat
open → subsequent realized return". It names no gap direction, no definition of "flat", no exit rule
and no control; this PREREG fixes all four (§2–§4). The gap is **direction-adjusted** and the two
directions are registered as **separate arms**: "a held pick gapped against me — hold or cut?" and
"a held pick gapped in my favour — take it or let it run / add?" are different management decisions.
No sign is presumed; tests are two-sided.

**Measured from the close, the gap is itself part of the outcome** (a gap in favour has already
done part of the move to L3; a gap against has added distance). How the design separates what the
gap *predicts* from what the gap *already is* is **decided: variant B**, the gap-matched same-night
control (§4.1; DECISIONS.md items 13 and 18; Haci 2026-09-13, *"strip the gap out"* → DP-12).
Variants A (total effect) and C (split at the end of session t+1) are reported descriptively and
never decide.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first;
  the estimator is a **within-night difference** between gap-arm picks and flat picks from the same
  night (§4), so the night's tape is held fixed.
- Source tables (manifest_v001 and its successor): `sas_candidates` (`selected_rank`,
  `overall_score`, `dominant_direction`, `best_timeframe`, `public_payload_json` lane plans,
  `days_to_earnings_corrected` — conditional descriptive stratum only, §6), `sas_runs`
  (`finished_at`).
- Source tables (manifest_prices_v001 and its successor): `prices_daily_split` (pick-night close,
  next-session official open for classification, forward highs/lows/opens/closes, ATR14, beta60,
  run-up, SPY tape), `prices_daily_raw` (split-factor snapping only), `prices_hourly_raw` (the
  descriptive after-hours entry sensitivity in §4 and same-session tie-breaks for the secondary race
  only).
- **Treatment rows:** every **published** pick — `qualified IS TRUE AND selected_rank IS NOT NULL`
  (DP-28) — on a non-excluded night in the §6 test window that has a lane-plan ladder with an L3
  price in `public_payload_json`. Dark-lane rows (`selected_rank` set but `qualified` not true) are
  **not** treatment rows in any arm and are **not** in the FLAT baseline; they sit in the control
  pool with every other non-published candidate row (§3).
- **The gap (the conditioning variable), defined exactly:**
  `C_t` = the pick's **actual** regular-session close on pick night t from `prices_daily_split`
  (never the platform's `spot_close`, which is stale on re-run nights — EXPLORE_001 §9);
  `O_{t+1}` = the session t+1 **official regular-session open** (09:30 ET), read from
  `prices_daily_split.o` (same split basis; see §10 threat 5 on verifying that `o` is the official
  open). **`O_{t+1}` is used as an input only to assign the gap group (Rule 14 exception, §6.1).**
  `dir` = +1 for bullish `dominant_direction`, −1 for bearish;
  **`g = dir × (O_{t+1} − C_t) / C_t × 100`** (percent, direction-adjusted; positive = in the pick's
  favour).
- **Arms (fixed here):**
  - **AGAINST:** `g ≤ −2.0`
  - **FAVOUR:** `g ≥ +2.0`
  - **FLAT (the baseline):** `|g| < 1.0`
  - **MIDDLE:** `1.0 ≤ |g| < 2.0` — not in any primary contrast; reported descriptively.
  **Decided (DECISIONS.md item 3):** signed arms, not a single `|g| ≥ 2%` arm — "gapped against me"
  and "gapped in my favour" are opposite management decisions. The 2% cut is **in percent, not ATR**:
  it is H-030's own figure as written, and the desk does not re-unit a hypothesis (DP-25). The 1%
  FLAT band and the MIDDLE band are registrar conventions not derived from sealed outcomes and stand
  as drafted (DP-26). The ATR-unit version of the same cuts (`g_ATR`, ±0.25) is a **secondary,
  descriptive** result (§4), because those thresholds are EXPLORE_001 figures. A gap-through at the
  entry price is never a hit (DP-26).
- **Exclusions — each counted per arm and printed in the results header, never silently dropped.
  Every exclusion that removes a pick or a night before measurement uses only inputs available by
  16:05 ET on the pick night, the trading calendar, or (for group assignment only) the t+1 official
  open:**
  - nights in **`research/data/exclusions_v002.json`** — `manual_runs.trading_dates`
    (2026-04-02, 04-24, 2026-05-11..05-15, **2026-07-02**, 2026-07-06) ∪
    `non_session_runs.trading_dates` (2026-04-03). On these nights the frozen candidate rows are not
    the 16:05 ET output (a manual re-run, or a run dated on a non-session day), so the pick was not
    published before the gap was known and a pick-night entry is not definable. `eval.py` reads the
    JSON and takes that union; **no date is hard-coded in this PREREG or in `eval.py`** (DP-22).
    Inside Q007's ≥ 2026-06-01 window only **2026-07-02** differs from `exclusions_v001.json`, so
    moving to v002 changes the citation, not the population (DECISIONS.md item 6; the Steward's
    counts in §5 were computed on exactly this population).
  - any prospective night whose `finished_at` is later than the next session's open (same criterion
    as `manual_runs`, applied mechanically, not by judgment).
  - picks with no lane-plan ladder or no L3 (the null-ladder denominator: 17 of 915 published picks
    in manifest_v001 have no ladder row at all — FREEZE_v001 §3; inside this window and on matured
    nights the Steward measured **8 of 394** — research/reports/STEWARD_Q007_exposure.md §R2)
    → excluded and counted.
  - **picks whose L3 is at or through `C_t`** (already passed at the entry — rule 5: not a hit;
    also an invalid target at publication) → excluded and counted. This is decided at the close,
    **before** the gap exists, so it is the same rule for every arm. (Steward: **2 of 386**
    wrong-side L3 ladders in this window, leaving 384 side-ok picks — §R2.)
  - picks with no session t+1 official open in the pinned freeze → no gap group; excluded from all
    arm contrasts and counted.
  - nights whose session t+20 falls after the last trading date of the pinned price freeze
    (immature) → excluded and counted. Maturity is determined **from the trading calendar**, never
    from whether a price exists; right-censoring is never graded as a non-touch.
  - picks that have a t+1 open but are missing forward bars inside t+1..t+20 (halt, delisting) →
    cannot be graded; excluded from measurement and counted per arm as a headline number. This is a
    measurement failure, not a classifier — it never moves a pick between arms, never removes a
    night, and never alters the control pool of any other pick.
- **Picks that gap through L3 at the open are touches**, graded like any other session-t+1 touch
  (there is no "already passed at the open" exclusion). Their count per arm is printed as
  "touched at the open" (§10 threat 2).
- **Contributing night (the unit that counts toward the floors, DP-21):** a night carrying **≥ 1
  eligible pick in that arm with a valid B3 control set (≥ 3 same-group controls, §3) and ≥ 1
  eligible FLAT pick with a valid B3 control set** — the variant-B definition, since variant B is
  the primary (§4.1; DECISIONS.md item 18). A night with only one of the two contributes nothing to
  that contrast; it is counted and reported, and it is **not** a contributing night for that
  endpoint. P1-A and P2-A count AGAINST+FLAT nights; P1-F and P2-F count FAVOUR+FLAT nights (§5,
  §8). The **exposure-only** count (the same test without the B3 requirement) is reported alongside,
  labelled as such, and decides nothing.
- ATR = ATR14 from `prices_daily_split` bars dated ≤ pick night t, in the signal-date basis (the
  platform's `atr_pct` is corrupted around splits — EXPLORE_001 §9; not used).
- Levels and windows are the platform's own (volatilx `services/sas_conviction_card.py:182-195`,
  `_LADDER_LEVEL_WINDOW` at `:194`): L1/L2 = 20, L3/L4 = 40, L5/L6 = 60 trading sessions. Ladder
  prices are read only from the pick-night `public_payload_json` lane plans (§10 threat 12). The
  primary horizon here is **L3 within 20 sessions** — the spread horizon, shorter than L3's own
  40-session lane window (Haci 2026-09-12, question A; **DP-09**). The platform's 40-session L3
  window is reported alongside, descriptively, wherever it has matured (§4). All floors, maturity
  tests and decision dates in §5 are computed on the **20-session** window.

## 3. Baseline(s) — what this must beat

- **B1 (primary baseline, H-030's own): FLAT picks from the same night**, entered on the same basis,
  graded with the same rule. The primary contrasts are AGAINST − FLAT and FAVOUR − FLAT, within
  night.
- **B2 (rule 5 distance-matched control):** for each eligible pick, the 10 nearest same-night
  **non-published** `sas_candidates` rows — the complement of the §2 publication predicate, i.e.
  `NOT (qualified IS TRUE AND selected_rank IS NOT NULL)`, so dark-lane rows are controls, not
  treatment (DP-28) — on `beta60` / `atr_pct` / `runup20` (computed from
  `prices_daily_split` bars dated ≤ t; standardized by the night's cross-sectional median and MAD;
  Euclidean; with replacement across picks; ties by symbol ascending) — the Q006 §3 construction,
  anchored at the close:
  `d_p = |L3_p − C_{t,p}| / ATR_p`;
  `target_c = C_{t,c} × (1 + dir_p × d_p × atr_pct_c)`;
  graded from each control's **own** pick-night close, same direction, same 20-session window,
  same touch rule (a control that gaps through its target at the open is a touch).
  - **Control pool and matching are fixed at 16:05 ET on the pick night:** the pool is the night-t
    non-published `sas_candidates` rows (predicate complement above) whose symbol has ≥ 60 bars
    dated ≤ t; the 10 nearest are
    chosen from that pool using only bars dated ≤ t. No control is filtered, re-ranked or replaced
    using anything after 16:05 ET: a matched control later found to lack forward bars is **not**
    replaced by the next-nearest candidate; it is dropped from that pick's control mean and counted.
  - B2 controls are **not** conditioned on their own gap. Control rows never add to inferential n
    (rule 6).
  - **What B2 removes and what it does not.** B2 removes the part of a touch rate that is just
    L3's ATR distance from the close. It does **not** remove the mechanical contribution of the gap
    itself: a pick that gapped 2% toward L3 is closer to L3 than its unconditioned controls on
    average, and one that gapped 2% away is further. Under B2 alone, AGAINST − FLAT and
    FAVOUR − FLAT therefore contain the gap's own displacement. See §4.1.
- **B3 (gap-matched same-night control):** for pick p in gap group G, the pool is the B2 pool
  restricted to candidates whose own gap, **direction-adjusted with the pick's direction**,
  `dir_p × (O_{t+1,c} − C_{t,c}) / C_{t,c} × 100`, falls in the same group G (the control's t+1 open
  enters only for this group assignment — §6.1). Within that restricted pool the nearest ≤ 10 on the
  same three features are taken, targets placed and graded exactly as B2. If fewer than **3**
  controls exist in the restricted pool, the pick's B3 value is missing and counted — the pick drops
  out of that night's arm (or FLAT) mean and the drop is printed per arm. **B3 is the primary
  control** (variant B; §4.1; DECISIONS.md item 18).

## 4. Objective metric (rule 5 — price path, measured the way it is traded)

**Entry basis: Rule-5 pick-night after-hours entry, measured at the pick-night close `C_t`
(`prices_daily_split`), for picks and controls alike** (DP-03(a); Haci 2026-09-12: *"I want to
measure the movement of the stock from closed price of previous day not opening prices"*).

*Entry basis decided:* pick-night close `C_t`, the DP-03(a) after-hours proxy, for picks and
controls alike (Haci 2026-09-12; DECISIONS.md item 12; **DP-11**, which generalises it to every
held-position question). `E_AH` is a picks-only descriptive sensitivity that never decides.

*Which price and why (decided, DECISIONS.md item 12).* The frozen data hold two
candidates: (i) the pick-night regular-session close in `prices_daily_split` for all 436 symbols;
(ii) an after-hours print in `prices_hourly_raw` (UTC stamps, includes pre/post-market), which
covers **227 symbols** (manifest_prices_v001 `sql` for that table) — the published-pick symbols per
Q004 §5 — and not the unpublished candidates that form the control pool. The close is chosen as the
primary entry price because: (a) rule 5 requires the pick and its distance-matched control to be
graded on the same basis, and only the close exists for the controls; (b) it is exactly the price
Haci named ("closed price of previous day"); (c) an after-hours hourly bar is often missing or thin
and is not a fill (Q004 §10 threat 1; EXPLORE_001 §B had an actionable after-hours price for 211 of
280 in-sample picks). The close is a **proxy**: SAS publishes after the close (`finished_at`
~21:0x UTC), so nobody can buy at exactly `C_t` (§10 threat 13).
**Descriptive sensitivity (picks only, never decides):** the same P1/P2 arm contrasts computed from
the real after-hours price, using **Q004's `E_AH` definition verbatim** (close of the first
`prices_hourly_raw` bar whose bar end is at or after that night's `sas_runs.finished_at`, strictly
before the next regular open, converted to the signal-date split basis; picks without such a bar
excluded from the sensitivity and counted), so the two questions' after-hours numbers reconcile.
No control is available on that basis, so the sensitivity is a raw arm contrast only.

**Touch rule.** A level at or through the entry price is not a hit (§2 exclusion at `C_t`; in the
sensitivity, at `E_AH`). Touches are the regular-session daily high (bullish) / low (bearish) from
session t+1 onward, split factors snapped — so **a gap through L3 at the t+1 open is a touch on
session t+1**. Stops are not assumed.

**What post-close information is used, and how.** Classification, filtering, matching,
stratification and level placement use inputs available by 16:05 ET, plus the t+1 official open
**for gap-group assignment only** (§6.1). All bars from session t+1 onward — including session
t+1's open, high, low and close — enter only as the **outcome path** (touches and exit fills), never
as an input.

**Why L3, and why 20 sessions.** **L3 is the primary level** — it is the short strike Haci sells and
the primary level in the locked Q006 §4 and Q004 §4 (DECISIONS.md item 8); the desk did not put the
level to him, only the clock. **The clock is 20 sessions** (Haci 2026-09-12, question A → **DP-09**):
the spread horizon ≈ expiry, the same window the desk already uses for the stock-path proxy (Q004
race window, H-055's "session 20 ≈ expiry"). The platform's own 40-session L3 lane window is
reported **alongside, descriptively**, wherever it has matured; it is never a verdict input, carries
no sample floor of its own and takes no BH slot. Sample floors and the decision date (§5) are
computed on the 20-session window only.

**Primary endpoints (four, pre-specified, BH-corrected within this question).** Each is defined
under **variant B** (§4.1), the primary selected by Haci on 2026-09-13 (DECISIONS.md items 13, 18;
DP-12).

- **P1 — reach (hit-rate claim, rule-5 control applied).**
  For pick p: `x_p = touch_{p,L3,20} − mean_c(touch_{c,20})`, controls = **B3** (§3); a pick with
  fewer than 3 same-group controls has no `x_p`, drops out of that night's mean and is counted.
  Per night: `D1_t(arm) = mean_{p∈arm,t}(x_p) − mean_{p∈FLAT,t}(x_p)`.
  Estimand: `mean_t D1_t(arm)`, in percentage points.
  - **P1-A:** arm = AGAINST. **P1-F:** arm = FAVOUR.
- **P2 — realized result of a named plan (H-030's "subsequent realized return").**
  **Plan E-L3 (close basis):** enter at `C_t`; exit at the first touch of L3 within sessions
  t+1..t+20 at the L3 price, except that if a session **opens through L3** — including session t+1,
  i.e. a gap through L3 — the exit is that session's open (a resting limit fills at the better
  price); if L3 is not touched, exit at the session t+20 close. No stop.
  For pick p: `r_p = dir × (exit_p − C_{t,p}) / ATR_p` (ATR units; ATR from bars dated ≤ t).
  Per night: `D2_t(arm) = mean_{p∈arm,t}(r_p) − mean_{p∈FLAT,t}(r_p)`, **with the B3 control
  adjustment** — `r_p` is the pick minus the mean of its B3 controls graded on the same E-L3 plan
  from their own close, and the night contrast is arm minus FLAT of those differences (variant B,
  §4.1); a pick with fewer than 3 same-group controls drops out of the night's mean and is counted.
  Estimand: `mean_t D2_t(arm)`, in ATR units.
  - **P2-A:** arm = AGAINST. **P2-F:** arm = FAVOUR.
  *Exit logic kept unchanged from the open-basis draft.* It still makes sense on the close basis: a
  resting L3 limit placed at the pick-night entry fills at the better of L3 and any open that gaps
  through it, and the session-20 close remains the spread-horizon fallback. The only change is that
  the session-t+1 gap-through, which the open basis excluded, is now a fill at the t+1 open.
  P1 is the mechanism; P2 is the money.

### 4.1 The gap is partly the outcome — design variants (variant B selected, Haci 2026-09-13)

From the close, a FAVOUR pick has already moved ≥ 2% toward L3 at the moment the signal appears,
and an AGAINST pick has moved ≥ 2% away; with B2 controls that are not conditioned on their own
gap, both P1 and P2 would show the gap's own displacement even if the gap predicted nothing about
the rest of the path. Rule 5's distance-matched control removes the target-distance effect **at the
close**, not this. Three variants are fully specified below. **Variant B is primary; A and C are
reported as descriptive figures and never decide** (DECISIONS.md items 13, 18, 19; Haci 2026-09-13,
question D → DP-12).

- **Variant A — total effect from the close, disclosed. *Descriptive, does not decide.***
  Controls = B2. P1 and P2 as written.
  Answers "what did the held position experience after a gap". *Cost, and why it is not the
  primary:* the sign is largely mechanical (FAVOUR up, AGAINST down) and by itself licenses **no**
  hold/exit/add rule (§8, §9), because the gap is inside the number. Its P2 figures are printed next
  to `|Δgap_ATR(arm)|` and are never called "beyond MPE" unless they exceed
  `0.25 ATR + |Δgap_ATR(arm)|` (§8; DECISIONS.md items 16, 19).
- **Variant B — gap-matched control. *Primary (Haci 2026-09-13).*** Controls = B3 (same-night
  unpublished candidates that gapped into the same group, in the pick's direction). `x_p` and `r_p` are pick minus its B3 controls
  (control trades graded with the same E-L3 plan against their synthetic target from their own
  close); the night contrast is arm minus FLAT of those differences. The gap's displacement is
  shared by pick and control and cancels. Answers "does a gap mean something different for a SAS
  pick than for a comparable stock that gapped the same way". *Costs, accepted with the choice
  (DP-12):* it is a different question from "gap vs flat" (it tests the pick-vs-stock difference
  inside each gap group); restricted pools are smaller, so some picks lose their B3 value
  (≥ 3-control rule, §3) — measured by the Steward at 7 of 47 eligible AGAINST and 5 of 35 eligible
  FAVOUR picks, which moves arm contributing nights from 22/20 to **18/15** and is why the hard stop
  is 2027-06-30 (§5; STEWARD_Q007_exposure.md §R5); uses controls' t+1 opens for grouping (within
  §6.1, as §3 already provides).
- **Variant C — split the path at the end of session t+1. *Descriptive, does not decide.***
  Report separately (C1) touch of L3 on session t+1 (including a gap through at the open), and
  (C2) first touch of L3 in sessions t+2..t+20 among picks **not** touched on session t+1, each with
  B2; for money, split `r_p` into the session-t+1 part and the remainder. Answers "what happens to
  the rest of the path once day 1 is over". *Costs, and why it is not the primary:* C2 conditions on
  a session-t+1 outcome (the t+1 high/low), which §6.1 as narrowed does **not** allow as a
  classifier — as a primary it would need Haci to widen the exception, and **that widening was not
  granted** (Haci 2026-09-13, question D; DP-05 stands unchanged), so C stays descriptive; it is
  also survivor-conditioned (picks that already touched drop out, differently by arm); and a
  "remainder" return needs a price anchor inside session t+1 (its close), which is a post-open level
  anchor.
- *Why B, for the record:* B is the only variant that removes the mechanical part without widening
  §6.1, and under rule 5 it is the only one that can license a hold/exit/add rule; A measures exactly
  what a held position earned but has the gap inside the number; C is closest to Haci's "rest of the
  path" wording but conflicts with the narrowed exception. Haci chose B on 2026-09-13
  (*"strip the gap out"*).

**Secondary, descriptive, never decides:**
- **§4.1 variants A and C**, the two non-selected variants — variant A's P2 figures always printed
  beside `|Δgap_ATR(arm)|` (§8; DECISIONS.md item 19);
- the after-hours entry sensitivity (`E_AH`, picks only, above);
- the plan's realized result under the **committed L1–L6 scale-out** (`BAND_EXITS`, volatilx
  `scripts/generate_sas_trading_guide.py:89-95`), close basis: fractions exited at each level's first
  touch at the level price or the better open; fractions whose level was at or through `C_t`
  recorded as unfillable and excluded from that fraction; remainder closed at the session t+20
  close; `<80` band not traded per the guide — truncated at 20 sessions and labelled so; the
  trailing rules in `BAND_EXITS` are not deterministic enough to simulate and are ignored;
- E-L3 in percent instead of ATR units;
- per arm: "touched at the open" counts for L1/L2/L3; the gap distribution itself by month;
- L1 and L2 first touch within 20 sessions from the close, and **L3 within 40 sessions** — the
  platform's own L3 lane window, matured nights only, reported alongside the primary per **DP-09**
  and never a verdict input — each with B2;
- the race "L3 before `C_t − dir × 1.0 × ATR`" within 20 sessions from the close — **H-063's race,
  carried here as a secondary when H-063 was merged into this question** (§7, DP-29) — with hourly
  tie-breaks, and a same-session pair that hourly bars cannot order scored **stop-first** (DP-27);
  TIE/NEITHER scored non-WIN as in Q004;
- maximum adverse excursion from the close within 20 sessions, in ATR; counter-direction swing-level
  touches within 20 sessions;
- the same contrasts with the gap in **ATR units** (`g_ATR = dir × (O_{t+1} − C_t) / ATR`,
  AGAINST ≤ −0.25, FLAT < 0.25 in absolute value, FAVOUR ≥ +0.25 — **H-063's ATR-scaled buckets,
  carried here on merge** (§7); EXPLORE_001 thresholds, so **descriptive only** and never a primary,
  per DECISIONS.md item 3 and DP-25);
- MIDDLE band (1–2%) vs FLAT;
- close-to-close return from `C_t` at T+5 and T+20 (secondary by rule 5).

**Quotability:** 20-session basis → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** Night-level. **CI (decides):** stationary block bootstrap over the ordered eligible
nights, expected block length 10 sessions (20-session forward windows overlap across adjacent
nights), 2,000 resamples; the date-clustered bootstrap CI is printed alongside. **p-value:**
within-night label permutation — on each eligible night, the arm/FLAT labels are shuffled among that
night's eligible arm+FLAT picks (each pick carrying its own B3 controls), 10,000 permutations; the
statistic is recomputed exactly as the estimand. Under variant B the labels and each pick's
group-restricted controls move together. Every estimate prints n(contributing nights),
n(exposure-only nights, labelled), n(arm picks), n(FLAT picks), n(control rows), n(picks dropped for
fewer than 3 B3 controls, per arm), and n(excluded, by reason).

## 5. Sample floors and expected n

- **Floors (rule 6, read per DP-21):** ≥ **80 contributing nights per primary endpoint** and
  ≥ **20 contributing nights per reported sub-cell**. A *contributing* night for an endpoint is
  defined in §2 on the **variant-B** definition, since variant B is the primary: for P1-A / P2-A a
  night with ≥ 1 eligible AGAINST pick **with a valid B3 control set** and ≥ 1 eligible FLAT pick
  with a valid B3 control set; for P1-F / P2-F the same with FAVOUR. Every floor, projection and
  decision-date test below uses that definition; the exposure-only count is reported alongside,
  labelled, and decides nothing. The weaker reading — "≥ 80 *eligible* nights total with ≥ 20
  contributing per arm", under which a night counts even when it carries no arm pick and no FLAT
  pick — is **not** used (DP-21; Q008 §5 uses the same reading). Any endpoint or sub-cell below its floor is **SUPPRESSED**: no point
  estimate printed.
- **Measured exposure — exposure-only, the pre-variant figure (Data Steward,
  research/reports/STEWARD_Q007_exposure.md §R2, 2026-09-12 — counts and dates only; no touch, no
  return, no outcome was computed or reported).** Population:
  published picks (`qualified IS TRUE AND selected_rank IS NOT NULL`) on non-excluded nights
  (`exclusions_v002.json`) with pick night ≥ 2026-06-01 whose **20-session** window has matured in
  `manifest_prices_v001` — i.e. exactly this PREREG's population.
  - **49 matured nights** (last matured pick night 2026-08-12), 394 published picks; after 8
    no-ladder and 2 wrong-side removals, **384 side-ok picks**.
  - Picks by arm (of 384): AGAINST 47, FAVOUR 42, FLAT 201, MIDDLE 94. **Passed-at-entry: 0 AGAINST,
    7 FAVOUR** (2 MIDDLE).
  - Nights with ≥ 1 eligible pick: AGAINST 23, FAVOUR 21, FLAT 46.
  - **Exposure-only contributing nights (pre-variant figure, labelled, decides nothing):
    AGAINST 22, FAVOUR 20, union 35.**
  - Monthly run-rate of exposure-only contributing nights: 2026-06 → AGAINST 6 / FAVOUR 10 /
    union 15; 2026-07 → 13 / 6 / 14; 2026-08 (matured only through 08-12) → 3 / 4 / 6.
  - Projection to 80 **exposure-only** contributing nights at the June–August run-rate:
    AGAINST 2027-02-22, FAVOUR 2027-03-21, union 2026-11-14.
  - *One conservative difference, disclosed.* The Steward's eligibility filter dropped picks whose L3
    was at or through `O_{t+1}` (a gap-group-only filter), which this PREREG does **not** do — under
    the close basis such a pick is graded as a touch at the open (§4). The 7 excluded FAVOUR picks
    therefore make the FAVOUR counts a **lower bound** on this PREREG's own contributing nights.
- **Variant-B exposure — the counts the floors are actually read against (Data Steward,
  research/reports/STEWARD_Q007_exposure.md §R5, 2026-09-13 — counts and dates only, computed from
  `C_t` and `O_{t+1}` alone; no target, no touch, no return, no outcome).** Same population,
  re-derived from the frozen parquet (394 published rows / 49 matured nights; eligible AGAINST 47,
  FAVOUR 35, FLAT 201).
  - Picks with ≥ 3 same-group non-published B3 controls: **AGAINST 40/47 = 85.1%**,
    **FAVOUR 30/35 = 85.7%**, **FLAT 201/201 = 100%**. Median control count 7 (AGAINST) / 10
    (FAVOUR) / 28 (FLAT); 10th percentile 1.6 / 1.4 / 19.0; FLAT's minimum is 11, so **the FLAT side
    never binds** and the reduction is entirely arm-side (7 AGAINST and 5 FAVOUR eligible picks lose
    their B3 value).
  - **Variant-B contributing nights: AGAINST 18, FAVOUR 15, union 29** of 49 matured nights (vs
    22 / 20 / 35 exposure-only) — all three below the 80-night floor today, which is why this
    question is locked now and evaluated later (freeze discipline below).
  - Monthly run-rate of variant-B contributing nights: 2026-06 → AGAINST 6 / FAVOUR 9 / union 14;
    2026-07 → 11 / 3 / 11; 2026-08 (matured only through 08-12) → 1 / 3 / 4.
  - Projection to **80 variant-B contributing nights** at the June–August run-rate:
    **AGAINST 2027-04-23**, **FAVOUR 2027-06-28**, union 2026-12-19 — all inside the **2027-06-30**
    hard stop. These are mechanical extrapolations of a three-month run-rate, not forecasts; the
    decision-date rule below is evaluated on measured counts, never on the projection.
- **Both arms are retained as primaries; nothing is dropped at lock.** The draft's pre-lock clause
  ("if either arm projects below the floor by the hard stop, that arm leaves the primaries; if both
  do, the question goes to DEFERRED") is now **resolved as fact on the Steward's counts**: under
  variant B, the primary, AGAINST stands at 18 and FAVOUR at 15 contributing nights and they project
  to 80 on **2027-04-23** and **2027-06-28**, both inside the **2027-06-30** hard stop — so **all
  four primary endpoints (P1-A, P1-F, P2-A, P2-F) stand and the BH family within the question stays
  at 4** (§7). Haci was asked the waiting-vs-sample trade-off directly, twice (R-3, questions C and
  E), and chose to extend the stop rather than drop an arm, fall back to variant A, or merge the two
  arms into a single `|g| ≥ 2%` arm. The at-decision-date version of the rule stands: an arm still
  below 80 contributing nights on 2027-06-30 is INCONCLUSIVE (SUPPRESSED).
- **Decision date (exposure-driven, fixed rule, no outcome looks):** the first Monday on or after
  **2026-10-26** on which the Steward's counts-only refresh shows **≥ 80 variant-B contributing
  nights for every retained arm** (DP-21, counted on the B3-valid definition in §2); **hard stop
  2027-06-30** (Haci 2026-09-13, question E; it is the only stop date in this file and replaces both
  earlier ones), on which date the evaluation runs regardless and **any arm still below 80
  contributing nights is INCONCLUSIVE (SUPPRESSED)**. On the Steward's §R5 run-rate the earliest
  evaluable Monday is **not before 2027-06-28**, FAVOUR being the binding arm. `eval.py` is written
  once and run **once** (rule 9). Waiting on exposure counts is not optional stopping, because
  exposure counts carry no outcome. Each refresh uses the same counts-only protocol as §R2/§R5.
- **What the Steward must recount at each decision-date check:** variant-B contributing nights per
  arm (i.e. nights with ≥ 1 eligible arm pick and ≥ 1 eligible FLAT pick, each with ≥ 3 same-group
  non-published candidates), the same per sub-cell, and the exposure-only counts alongside for
  reference. **Counts only**, computed from `C_t` and `O_{t+1}`; no forward bar beyond the t+1 open,
  no price level, no outcome.
- **Freeze discipline (DP-23).** This question is **locked now, pinned to `manifest_v001` /
  `manifest_prices_v001`** for nights ≤ 2026-09-10. Nights after 2026-09-10 enter only through
  successor freezes **built and pinned at the decision date**: `manifest_v002` (selections, same SQL
  as v001) and `manifest_prices_v002` (same Alpaca queries), with the daily symbol list extended to
  **every candidate on the new nights, published and non-published** — B2 needs their closes and
  forward bars and B3 needs their t+1 opens — plus **hourly bars for published symbols** for the
  `E_AH` sensitivity and the secondary race's same-session tie-breaks. That scope is fixed by DP-23
  and needs no further confirmation. `eval.py` records every sha256 and prints pre-lock and post-lock
  night counts separately. **Neither successor freeze exists today**, and neither blocks the lock. If
  `manifest_prices_v002` omits non-published-candidate symbols, P1 cannot be computed for those
  nights; they are excluded from P1 and counted, never back-filled.
- Sub-cells (bull / bear; score band < 80 / 80–85 / 85–90 / 90+; tape stratum; regime label;
  earnings stratum — now computed, §6) are reported only where they clear **20 contributing nights**
  for that arm. Bear and 90+ arm cells are expected to be SUPPRESSED.

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-06-01** through the decision date.
  *Justification (one sentence):* EXPLORE_001 §B split the 20-session L3 path by the same
  direction-adjusted next-open gap on April–May (measured from the open) and published the result
  into BACKLOG H-063; the close-basis version shares the gap grouping and the L3 object, so the
  in-sample nights stay contaminated for this question.
  *Contamination check on the sealed period:*
  - the weekly snapshots of 2026-09-10 and 2026-09-12 contain no gap-conditioned figure (registrar,
    count-only search, no figures read);
  - at the coordinator's instruction the registrar read **line 29 of
    research/reports/weekly/2026-09-12.md**. It reports sealed-period L1 touch rates within 20
    sessions measured from the next open vs from the close, and the share of 90+ picks with L1
    already passed at the open. It is **not** conditioned on the gap and concerns L1, not L3;
  - the switch of Q007's entry basis from the open to the close was made **after** that sealed
    entry-basis figure was published. The within-night arm − FLAT contrast uses the same basis on
    both sides, so a basis-wide level shift largely cancels, but the choice is not blind to sealed
    data and is disclosed as such (§10 threat 13) — the exposure it creates is bounded there: the
    historical track carries the label `DESIGN_CHOICE_NOT_BLIND`, the prospective track is
    unaffected;
  - no results directory was read.
- **Catalyst-layer regime change:** the window sits entirely after the 2026-06-01 fix
  (`exclusions_v002.json` `catalyst_layer_regime_change`, carried over unchanged from v001; platform
  commit 69ef05f).
- **Split for "holds in both halves":** Half A = eligible nights on or before the median eligible
  night date (computed on the total eligible set, not per arm, from the calendar and maturity only);
  Half B = after. `in_sample_end = 2026-05-29` marks only what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v002.json` `regime_label_point_in_time_from`, carried over unchanged from v001). It
    is used only for nights
    ≥ 2026-06-09, only `regime_version = 'v1.2'`, and only where the row is a same-evening write per
    its declared availability (16:05 ET, lag 0); a row written later (FREEZE_v001 §7 names
    2026-07-06, posted 2026-07-07 14:23 UTC — already an excluded night) is treated as missing.
    Nights 2026-06-01..06-08 carry no legal label and are stratified by the SPY proxy only, flagged.
  - Primary tape stratum for every night, legal at 16:05 ET: `tape_t` = sign of SPY's trailing
    20-session return × tercile of SPY's trailing 20-session realized volatility, both from SPY bars
    dated ≤ t in `prices_daily_split`. **Tercile cut points are expanding-window:** for night t they
    are computed from SPY's trailing-20 volatility on every session from 2026-03-02 through t, so no
    later night's data sets the stratum of an earlier night. Cells < 20 nights SUPPRESSED.
  - **Earnings stratum (descriptive) — computed.** Picks with a scheduled report between the
    pick-night close and the t+1 open vs the rest, per arm, from
    `sas_candidates.days_to_earnings_corrected`. The Data Steward verified availability
    (research/reports/STEWARD_Q007_exposure.md §R3 part 2): **PASS on code-path evidence for
    trading_date ≥ 2026-06-01**, i.e. this question's whole window — the column is written on the
    live scoring path inside the same nightly pass that creates the row
    (volatilx `services/super_agent_select_service.py:396-403` ←
    `services/super_agent_select_scoring.py:1438,1482`), and the one backfill script that touches it
    (`scripts/rescore_sas_earnings_corrected.py`) is scoped by its own docstring to
    trading_date < 2026-06-01. The evidence is **code-path, not a per-column timestamp** (the frozen
    table has none), and the report is cited as such. The earlier "otherwise not computed" branch is
    therefore retired. The stratum is never a filter and never a verdict input.

### 6.1 Rule 14 exception — human decision record

- **Decided by:** Haci, **2026-09-12**, relayed by the coordinator. Haci's words: *"Item 1 i accept
  to see the gap next morning 9:30"* (his "item 1" is the knowledge-time question put to him on
  2026-09-12; DP-05).
- **Narrowed 2026-09-12** after Haci changed the entry basis to the pick-night close (his words:
  *"I want to measure the movement of the stock from closed price of previous day not opening
  prices"*; choice: *"Keep gap groups, measure from close"*).
- **Scope — gap-group assignment only.** The session t+1 **official open** may be used as an input
  for exactly one purpose: computing the direction-adjusted gap `g` against the pick-night close
  `C_t` and assigning AGAINST / FLAT / MIDDLE / FAVOUR — for picks, for the ATR-unit secondary
  grouping, and for B3 control grouping. The decision time for that input is **09:30 ET on session
  t+1**. The t+1 open is **not** an entry price, **not** a level or synthetic-target anchor, and
  **not** a matching, filtering or stratifying input.
- **Not covered by the exception:** every other input — pick membership (`selected_rank`),
  direction, score and band, ladder levels, the entry price `C_t`, ATR, beta60, runup20, the
  control-candidate pool and its matching, regime label, tape stratum, and any earnings stratum —
  must have **available_time ≤ 16:05 ET on the pick night**. Nothing from session t+1 other than the
  official open used for grouping (not the t+1 high, low, close, volume, VWAP, hourly bars, or any
  intraday price) may be used to classify, filter, match, stratify or place a level.
- **Outcome use is not input use.** Bars from session t+1 onward, including the t+1 open, high, low
  and close, are part of the measured path: a gap through L3 is a touch, and an open through L3 is
  an exit fill. That is measurement of the outcome, not use of a feature.
- **What eval.py must enforce:** the gap and arm labels (and B3 group labels) are computed and
  written to a frozen per-pick table **before** any forward bar is loaded, reading only `o` from
  bars dated t+1; the run fails if any other t+1-or-later field is referenced in the classification
  step, or if `o` from a t+1 bar is referenced anywhere in classification other than the gap.

- **Knowledge time (rule 14) — every input declared:**

  | input | source | available | use |
  |---|---|---|---|
  | `selected_rank` (pick membership), `dominant_direction`, `overall_score`, `best_timeframe` | `sas_candidates` | pick night, 16:05 ET (declared; FREEZE_v001 §7) | population, direction, band |
  | lane-plan ladder levels L1–L6 | `sas_candidates.public_payload_json` | pick night, 16:05 ET (declared) | levels |
  | control-candidate pool (unpublished rows for night t) | `sas_candidates` | pick night, 16:05 ET (declared) | B2/B3 pool |
  | `C_t` (entry price and gap base), ATR14, beta60, runup20 | `prices_daily_split`, bars dated ≤ t | pick-night close, 16:00 ET | entry, distances, matching |
  | SPY tape (trailing return, trailing vol, expanding terciles) | `prices_daily_split`, SPY bars dated ≤ t | pick-night close | stratum |
  | regime label (v1.2, nights ≥ 2026-06-09, same-evening rows only) | `market_regime_daily` | pick night, 16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time, before the t+1 open on every included night | exclusion criterion; `E_AH` clock (sensitivity) |
  | `E_AH` after-hours price (sensitivity only) | `prices_hourly_raw` | publication, pick night | descriptive entry price only |
  | **`O_{t+1}`, official open, `o` only** | `prices_daily_split`, bar dated t+1 | **09:30 ET session t+1 — Rule 14 exception, Haci 2026-09-12, narrowed (§6.1)** | **gap-group assignment only** |
  | report date for the earnings stratum | `sas_candidates.days_to_earnings_corrected` | pick night, 16:05 ET — **verified PASS on code-path evidence for trading_date ≥ 2026-06-01** (STEWARD_Q007_exposure.md §R3 part 2; §10 threat 4) | descriptive stratum only |
  | session t+1 open/high/low/close; sessions t+2..t+20; hourly bars after the open | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **outcome only** |

  `sas_excursion` / `outcome_*` / `level_hit_*` columns are never inputs (they are on calendar
  windows and a different grading pipeline — volatilx `services/sas_excursion.py:8-18`, `:336-354`).
  `uoa_symbol_daily.fwd_return_*` is **banned** (the May–June freeze is not fixed: FREEZE_v001 §5);
  no UOA table is used.

## 7. Multiple testing

- **Within the question:** 4 primary endpoints (P1-A, P1-F, P2-A, P2-F) under **variant B** (§4.1);
  Benjamini–Hochberg across the 4; the verdict uses q. Both arms are retained at lock (§5), so the
  family within the question is 4. Variants A and C and all secondaries print raw p only, marked
  "descriptive, does not decide".
- **Across the family:** F4 Price behaviour after selection holds H-030, H-031, H-032, H-033, H-034,
  H-063, H-064 (7 hypotheses); registered F4 questions at registration: **none besides this one**.
  The Reporter applies BH across all primary endpoints of registered-and-run F4 questions and prints
  both q's.
- **Overlap with H-063:** H-063 is a gap question measured **from the open** with a skip-or-delay
  decision. After the 2026-09-12 basis change, Q007 measures from the close and asks a hold/exit/add
  question, so it no longer tests H-063's skip-from-the-open decision. **H-063 is merged into Q007**
  (DECISIONS.md item 7; DP-29); its ATR-scaled gap buckets and its L3-before-(−1 ATR) race are
  carried here as secondaries, descriptive. F4 keeps 7 hypotheses and H-063 is not counted as a
  second registered question in the family correction; `research/BACKLOG.md` marks it
  "merged into Q007".
- **Overlap with Q004 (F7):** Q004 is registered in a different family on overlapping nights and
  picks (§10 threat 11); **the two families are corrected separately** — Q004 is F7, Q007 is F4, and
  BH runs within a family (rule 8; DP-29, which assigns a question by its primary endpoint's
  subject: Q004's is the entry basis, Q007's is the path after selection). The overlap is a
  **non-independence** hazard, not a multiplicity one: the two results are never presented or counted
  as two confirmations (§10 threat 11), and the Reporter cross-references rather than duplicates
  (DECISIONS.md item 14).
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1(arm) = mean_t D1_t(arm)` in percentage points of L3 touch rate (B3-control-adjusted, variant B);
`m2(arm) = mean_t D2_t(arm)` in ATR units.

**MPE: P1 10.0 pp** (DECISIONS.md item 4a; DP-20 is the 5.0 pp floor, raised here because P1 is a
difference of differences with small cells — Q003 §8 precedent). **P2 0.25 ATR per trade** (Haci
2026-09-12, question B → **DP-10**; the standing number for every per-trade ATR endpoint, not
re-asked).

**P2's decision threshold is `|m2(arm)| > 0.25 ATR` (DP-10) and P1's is 10.0 pp, under variant B,
the selected primary. The descriptive variant-A P2 figures are printed next to `|Δgap_ATR(arm)|`
and a variant-A figure is never called "beyond MPE" unless it exceeds `0.25 ATR + |Δgap_ATR(arm)|` —
the gap's own displacement is inside variant A's number and can exceed 0.25 ATR by construction.**
Where `Δgap_ATR(arm) = mean_t [ mean_{p∈arm,t}(dir×(O_{t+1,p}−C_{t,p})/ATR_p) −
mean_{p∈FLAT,t}(dir×(O_{t+1,p}−C_{t,p})/ATR_p) ]`, computed from `C_t` and the t+1 open only (§6.1
inputs, never an outcome) and printed as a **headline number per arm**. P1 keeps 10.0 pp under every
variant. Under B (primary) the displacement cancels and under C it is isolated in C1, so no offset
applies there (DECISIONS.md items 16 and 19).

Per endpoint (two-sided; the verdict carries its sign):

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **contributing nights ≥ 80 for that arm** (variant-B definition, §2/§5) **and ≥ 20 contributing
     nights for any reported sub-cell** (DP-21);
  2. `|m| > MPE`;
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question;
  5. the point estimate has the **same sign in both halves**, and neither half is beyond MPE in the
     opposite sign;
  6. no tape stratum with ≥ 20 contributing nights is beyond MPE in the opposite sign;
  7. the verdict is emitted with the label **`DESIGN_CHOICE_NOT_BLIND`** (§10 threat 13) and is
     never restated, ledgered or quoted without it.
- **NULL:** floors met **and** 95% CI includes 0 **and** `|m| < MPE`. "A ≥ 2% gap on a held pick
  says nothing about the rest of the trade" is a real finding and is ledgered with the same care.
- **INCONCLUSIVE:** anything else — cell below floor (SUPPRESSED), halves disagreeing in sign,
  `0 < |m| ≤ MPE` with the CI excluding 0 ("real but below MPE", rule 6), or CI including 0 with
  `|m| ≥ MPE`.
- **Arm-level reading (what licenses a rule):** a hold / exit / add guide line about an arm requires
  **P2 for that arm CONFIRMED under variant B**, the primary, which removes the gap's own
  displacement. The descriptive variant-A P2 figure — even a large one — reads only as "held
  positions that gapped this way ended up better/worse", and **no management rule follows** from it,
  because the gap is inside the number. P1 alone never licenses a rule; it only says whether
  the effect is more than distance. P1 CONFIRMED with P2 NULL for the same arm is reported as
  "information present but not worth acting on at this size".
- **PROSPECTIVELY_CONFIRMED:** only after **≥ 30 contributing nights for that arm dated after this
  file's lock commit** (variant-B definition; DP-24, DP-21), frozen separately and never inspected
  earlier, reproduce the sign of `m2` for that arm under the unmodified `eval.py`. The clause does
  not weaken: if the window cannot supply 30, the decision date moves and that move is R-3. No
  subscriber-facing
  statement before that (rule 10); even then the basis is NON_QUOTABLE until restated on W60
  (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform has **no per-pick gap logic** — the only overnight-gap field in `services/` is
SPY's, for the market brief (volatilx `services/market_intelligence_data.py:638`,
`services/market_intelligence_scoring.py:250`). The conviction monitor runs at 16:02 ET
(FREEZE_v001 §7), so nothing re-evaluates a held pick at the next open.

Rules below apply only where §8's arm-level reading licenses one (**P2 CONFIRMED under variant B**):

- **P2-A CONFIRMED negative (a gap against predicts a worse rest-of-trade):** Manual Trading Guide
  line — "if a pick you bought last night opens 2% or more against you, the rest of the trade has
  historically gone worse than flat opens; consider cutting or reducing at the open rather than
  holding to L3". Brief: a flag-off at-open job that writes the direction-adjusted gap per
  published pick and surfaces "GAPPED AGAINST" on the card for held picks.
- **P2-A CONFIRMED positive:** guide line — "a gap against on a held pick is not a failed thesis;
  holding (or adding at the open) has done better than flat opens".
- **P2-F CONFIRMED negative (a favourable gap predicts give-back):** guide line — "if a held pick
  opens 2% or more in your favour, take some off at the open"; the at-open flag shows
  "GAPPED IN FAVOUR — consider taking profit".
- **P2-F CONFIRMED positive:** guide line — "a favourable gap is continuation; let it run toward
  L3/L4 (or add)".
- **P1 NULL with P2 CONFIRMED:** the effect is price, not information about reaching L3; the guide
  line talks about the trade's result only, not about target odds.
- **A large descriptive variant-A figure (A is never a primary):** a descriptive line only ("held
  picks that gapped against ended worse, which includes the gap itself"), printed next to
  `|Δgap_ATR(arm)|`; no flag, no management rule, no verdict.
- **All four NULL:** no gap rule; the guide says a gap at the open on a held pick is not by itself a
  reason to act, and F4 effort moves to H-031/H-064.
- Owner: implementer. Ship flag-off with a byte-identical checksum on the old path; shadow ≥ 20
  trading days before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **Gap is confounded with volatility.** A 2% cut selects high-ATR names into both arms, so arm vs
   FLAT differs in `atr_pct`, beta and run-up. The controls and P2's ATR units reduce but do not
   remove this. The report prints standardized mean differences (arm vs FLAT) on the three matching
   features and P2 within `atr_pct` terciles, descriptive.
2. **The gap is partly the outcome (mechanical inclusion).** Measured from the close, FAVOUR picks
   start session t+1 closer to L3 and some are touched **at the open** by the gap alone; AGAINST
   picks start further away. Unconditioned controls (B2) do not cancel this. This replaces the
   earlier arm-dependent "already passed at the open" exclusion bias: the passed-at-entry rule is now
   applied at the close, before the gap, identically for every arm, but gap-through-at-the-open
   touches and fills now enter the metric and are expected to be concentrated in FAVOUR.
   **Handled by variant B (§4.1): the displacement sits on both sides of the B3 contrast and
   cancels. The per-arm "touched at the open" count remains a printed headline number, and the
   descriptive variant-A figures carry `|Δgap_ATR(arm)|` beside them (DECISIONS.md item 19).**
3. **The gap is a t+1 observation.** Haci accepted it on 2026-09-12 as a Rule 14 exception, now
   narrowed to gap-group assignment only (§6.1). The residual risk is leakage around the exception:
   the t+1 open drifting into an entry price, a level anchor or a filter, or any other t+1 field
   (the t+1 high/low/close, hourly bars, a post-open data-availability filter) slipping into
   classification, filtering, matching or stratification. §6.1 requires `eval.py` to freeze group
   labels before forward bars are loaded and to fail on any other t+1 reference; the Red Team should
   check this specifically. Any subscriber-facing use must say the signal appears at the open, after
   the position was entered.
4. **Earnings and news drive most large gaps.** A gap arm is partly an earnings arm, which overlaps
   H-064. **Verified (research/reports/STEWARD_Q007_exposure.md §R3 part 2): PASS on code-path
   evidence for trading_date ≥ 2026-06-01, i.e. this question's whole window**, so the earnings
   stratum **is** computed (§6) and the confound is measured rather than merely stated. The evidence
   is code-path, not a per-column timestamp — the frozen table has none — and the report is cited as
   such; the stratum is descriptive, never a filter and never a verdict input.
5. **Daily-bar open and high/low definition.** Group assignment uses the **official** open, and a
   gap through L3 is graded from the t+1 daily high/low and open. **Verified
   (research/reports/STEWARD_Q007_exposure.md §R3 part 1): PASS 40/40** — the daily `o` falls inside
   the hourly bar containing 09:30 ET and the daily `h`/`l` never exceed the regular-session
   (09:30–16:00 ET) hourly envelope, on a 40 symbol-date sample. Caveat, stated: the frozen data is
   hourly, not tick-level, so this places `o` inside the official-open bar rather than confirming the
   exact opening print. **DST hazard, disclosed and binding on `eval.py`:** the 09:30/16:00 ET
   boundary must be computed per date with `zoneinfo` (America/New_York), not a fixed UTC offset — a
   fixed offset mis-flagged 2 of 40 pre-DST dates in the Steward's first pass.
6. **Overlapping forward windows** inflate precision; block length fixed here (10 sessions), not
   chosen after seeing results.
7. **One tape.** The whole window is Jun–Oct 2026. A sign that appears in only one half fails §8
   clause 5; nothing here speaks to a strong tape.
8. **Small arms and permutation power.** Within-night label permutation draws its information only
   from nights with both an arm pick and FLAT picks; with ~20–30 such nights the test is weak, and
   INCONCLUSIVE is a likely outcome that should not be read as a lean. Variant B makes this worse
   (picks without ≥ 3 same-group controls drop out), and the cost is now **quantified** from the
   Steward's §R5 count: **7 of 47 eligible AGAINST and 5 of 35 eligible FAVOUR picks lose their B3
   value** (FLAT loses none, minimum 11 controls), and arm contributing nights fall from 22/20 to
   **18/15** — which is why the hard stop moved to **2027-06-30** (§5; DECISIONS.md item 20).
9. **Null-ladder denominator** and wrong-side L3 ladders: excluded and counted (§2).
10. **Stock path is a proxy for the spread.** E-L3 is an equity trade; the option P&L of a vertical
    opened on the pick night needs option prices the desk does not hold
    (research/questions/DEFERRED.md, H-055/H-056). Any guide line from §9 about spreads must say so.
11. **Overlap with Q004 (research/questions/Q004_entry_basis/PREREG.md).** Q004 is the registered
    entry-basis test (cited as such by research/reports/weekly/2026-09-12.md line 29). Points of
    overlap:
    - **Shared nights and picks:** Q004's window is also sealed + prospective pick nights
      ≥ 2026-06-01 with 20-session windows and a 2026-10-26 decision date; Q007's nights and picks
      are a near-superset of Q004's. The two results are not independent evidence and must never be
      presented or counted as two confirmations.
    - **Shared after-hours construct:** Q004's primary contrast T1 is `E_AH` vs next open. Q007's
      after-hours sensitivity reuses Q004's `E_AH` definition verbatim so the numbers reconcile;
      Q007 does **not** test entry basis and makes no claim about close vs open vs after-hours.
    - **Shared gap construct:** Q004 §6 reports its race split by the night's median open gap
      (≤ −0.25 ATR / flat / ≥ +0.25 ATR), descriptively and from the open; Q007's ATR-unit
      secondary is close to that split but measured from the close. Reports must cross-reference,
      not duplicate.
    - **Shared race object:** Q007's secondary race (L3 before −1 ATR) mirrors Q004's primary race
      but anchored at the close; it stays descriptive here so the same object is not a primary in
      two questions.
    - **Different families:** Q004 is F7, Q007 is F4, so BH corrections are applied separately
      (§7; rule 8; DP-29; DECISIONS.md item 14). The shared nights are a non-independence hazard,
      handled by the "never two confirmations" sentence above, not by a joint correction.
    - **Independence of code:** neither `eval.py` may read the other's outputs.
12. **Ladder levels live in a row that is updated later.** `sas_candidates` rows later receive outcome
    columns (`outcome_*`, `level_hit_*`), so the row's `updated_at` post-dates the pick night. The
    ladder is read only from `public_payload_json`; the KT audit found whole-row replacement only on
    re-run nights (2026-07-02 is excluded here). If any evidence appears that `public_payload_json`
    itself is rewritten after the night, the ladder fails its 16:05 ET availability and the question
    must stop.
13. **The close is not a tradable price, and the basis choice was not made blind.** SAS publishes
    after the close (`finished_at` ~21:0x UTC), so `C_t` is a proxy for an after-hours fill (DP-11);
    the `E_AH` sensitivity shows the picks-only difference, and after-hours prints are thin and are
    not fills (Q004 §10 threat 1). Separately, and disclosed in full: Q007's entry basis was changed
    from the next-session open to the pick-night close on 2026-09-12, **after**
    `research/reports/weekly/2026-09-12.md` line 29 published sealed-period L1 touch rates measured
    from the next open versus from the close. That figure is unconditional — no gap grouping, no L3
    number — and the close basis is DP-03(a), a basis registered before the figure existed and forced
    here by the question's own framing: a position that is already held when the gap appears must have
    been entered before the gap, and rule 5 requires its distance-matched control on the same basis,
    which only the close provides for unpublished candidates. The within-night arm − FLAT contrast
    also uses one basis on both sides, so a basis-wide level shift largely cancels. None of that makes
    the choice blind, so its exposure is recorded explicitly: **it weakens the historical track only.**
    Pick nights 2026-06-01..2026-09-10 sat inside the pinned freeze and were observable when the basis
    was chosen, so any HISTORICALLY_CONFIRMED verdict on Q007 carries the label
    **`DESIGN_CHOICE_NOT_BLIND`** in the results header, in `REPORT.md` and in the LEDGER entry.
    Pick nights after the lock commit were not observable at the switch, so the PROSPECTIVELY_CONFIRMED
    track (§8) is unaffected, and it remains the only track that can license a rule or a
    subscriber-facing statement (rule 10). `eval.py` already prints pre-lock and post-lock night counts
    separately (§5), which is what makes the label checkable.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: **R4 — the successor freezes
(`manifest_v002`, `manifest_prices_v002`), built and pinned at the decision date by design (§5,
DP-23); not a blocker for lock.**
