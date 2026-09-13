# Q011 — day1_dip_limit: is it better to rest a limit order below the pick-night close and buy the day-1 dip, or just buy at the next open?

**Status:** DRAFT (lock by committing this file) — nothing is open: every item is settled in DECISIONS.md (2026-09-13; autonomous run, items 8 and 9 DEFAULTED under DP-40/DP-43)
**Family:** F7 Path, entry timing & volatility (hypothesis H-058)
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates. See §2.
**Decisions:** DECISIONS.md (recorded 2026-09-13 — 14 DECIDED, 2 DEFAULTED under DP-43, R1 returned and folded in below; R2 open, due at the decision date, not a blocker for lock)
**Measured exposure:** research/reports/STEWARD_Q011_exposure.md (R1, 2026-09-13; counts only, no outcome of any kind) — 369 eligible picks on 47 contributing nights, sealed window 2026-06-01..2026-08-12.
**Registered by:** registrar · **Approved by:** desk (DP-46) · **Date:** 2026-09-13

---

## 1. Hypothesis (plain English)

**Waiting for a dip costs you: if you rest a buy limit a quarter or a half ATR below the pick-night
close instead of simply buying at the next open, you end up with a worse set of trades — you miss the
picks that never dip, and the ones that do dip to your price reach the swing target L3 before falling
a full ATR against you less often than a plain open entry does.**

BACKLOG H-058 reads: *"Don't buy the day-1 dip: resting limit orders 0.25–0.5 ATR against the
pick-night close often fill on day 1, and the filled picks do worse on the L3-before-(−1 ATR) race
than a market entry at the open — adverse selection — baseline: next-open market entry on the same
picks."* It names no order duration, no fill convention, no treatment of picks that never fill, no
window and no decision. This PREREG fixes all of them (§2–§4). No sign is presumed; every test is
two-sided.

**Two things are tested as primaries, at both limit distances H-058 names (0.25 and 0.5 ATR):**

- **(P1, the race)** does the limit rule win the L3-before-(−1 ATR) race on more of the night's
  published picks than the open-entry rule;
- **(P2, the money)** does the limit rule make more or less per published pick, in ATR, under a named
  execution plan.

**Both primaries are intention-to-treat (ITT), decided at lock (DECISIONS.md item 1): every eligible
pick is in the denominator of both arms, and a pick the limit never filled is scored as what it is —
no position (race non-WIN, result 0 ATR) — not dropped.** This is not a stylistic choice.
Restricting the contrast to *filled* picks
conditions the denominator on a session-t+1 path event (the day's low reaching the limit), which is
exactly the classifier Q007 §4.1 variant C was refused as a primary for, and which would need a new
rule-14 exception; in autonomous mode the desk grants none (DP-41, DP-05 untouched). The
fill-conditional contrast — H-058's adverse-selection *mechanism* — is therefore computed, printed
and decomposed out of the ITT number (§4), and is **descriptive: it never decides a verdict**
(DECISIONS.md items 1 and 13).

**What that costs the hypothesis, stated up front.** An ITT contrast blends two effects: the trades
the limit missed, and the price advantage on the trades it got. A confirmed-negative P1 or P2
licenses only "resting a limit at this distance costs this much per published pick" — it does **not**
license "a day-1 dip is information against the thesis" (§8, §9, §10 threat 1). The decomposition in
§4 is pre-specified so the report cannot blur the two.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night first; the
  estimator is a within-night **paired** difference between two entry rules applied to the same
  picks, so the night's tape is held fixed.
- Source tables (manifest_v001 and its successor): `sas_candidates` (`qualified`, `selected_rank`,
  `overall_score`, `dominant_direction`, `best_timeframe`,
  `public_payload_json` → `lane_plans.swing_trading.{entry, stop, targets}`,
  `outcome_target_invalid` for the exclusion audit only), `sas_runs` (`finished_at` for the DP-04
  exclusion criterion and for the descriptive `E_AH` sensitivity).
- Source tables (manifest_prices_v001 and its successor): `prices_daily_split` (pick-night close,
  session t+1 open/high/low, forward bars, ATR14, beta60, run-up, SPY tape), `prices_daily_raw`
  (split-factor snapping only), `prices_hourly_raw` (the fill clock and same-session ordering on
  published symbols — §4; and the descriptive `E_AH` price).
- **Treatment rows:** every **published** pick — `qualified IS TRUE AND selected_rank IS NOT NULL`
  (DP-28); dark-lane and qualified-false rows are never treatment rows — on a non-excluded night in
  the §6 test window whose `public_payload_json.lane_plans.swing_trading` carries a first target
  (= **L3**, `targets[0]`).
- **Lane and level (DP-42).** The hypothesis names the L3 race, so the level is **L3**, the swing
  lane's first target (volatilx `services/sas_conviction_card.py:182-187`), and the clock is
  **20 sessions from the stated entry** (**DP-09**), not the platform's 40-session swing window. The
  40-session version is reported alongside, descriptively, wherever it has matured (§4).
- **Definitions (all prices in the signal-date split basis):**
  `C_t` = the pick's **actual** regular-session close on pick night t from `prices_daily_split`
  (never the platform's `spot_close`, which is stale on re-run nights — EXPLORE_001 §9);
  `ATR` = ATR14 from `prices_daily_split` bars dated ≤ t (the platform's `atr_pct` is corrupted
  around splits — DATA_NOTES; not used);
  `dir` = +1 for bullish `dominant_direction`, −1 for bearish;
  `L3` = the printed swing first target; `d_close = dir × (L3 − C_t) / ATR`, required > 0 (§ exclusions);
  `O_1` = the session t+1 **official** regular-session open (`prices_daily_split.o`);
  **the limit price** `LIM_k = C_t − dir × k × ATR` for **k ∈ {0.25, 0.5}** — H-058's own distances,
  in ATR as written, not re-united (DP-25).
  **`C_t` is the reference price for the limit distance and the ATR denominator; it is not an entry
  in this question** (§4).
- **Fill (mechanical, from the frozen bars; decided at lock).** The order is a **day order resting
  for session t+1's regular session only** — H-058's claim is about the *day-1* dip, and a
  longer-lived order is a different hypothesis (DECISIONS.md item 5; DP-25).
  Bullish: `FILLED_k = 1` iff `low_1 ≤ LIM_k`, and the fill price is `FILL_k = min(O_1, LIM_k)` — a
  resting buy limit fills at the open when the session opens below it, which is both how the order
  actually trades and the reading **less** favourable to the hypothesis (DECISIONS.md item 2; DP-45).
  Bearish mirrored: `FILLED_k = 1` iff `high_1 ≥ LIM_k`, `FILL_k = max(O_1, LIM_k)`.
  `low_1` / `high_1` are the regular-session daily low/high. In the sealed window that rule governs
  the **89 of 232** fills taken at the open at k = 0.25 and the **43 of 157** at k = 0.5, and no
  others (R1 §2(a)).
- **Exclusions — each counted per arm and printed in the results header, never silently dropped.
  Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or
  a measurement failure (below):**
  - nights in **`research/data/exclusions_v003.json`** — `manual_runs.trading_dates` ∪
    `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`. Inside this
    window those are **2026-07-02**, **2026-07-06** (re-run nights: the frozen candidate rows,
    including every printed L3, are a re-run's output and not the 16:05 ET decision's) and
    **2026-06-26** (whole night: the run's own `stats_json` records 8 qualified, the frozen table
    carries 11 — the only such night in 113; DATA_NOTES). `eval.py` reads the JSON and unions the
    three lists; the dates above are printed for the reader only — the file is the source of truth
    and **no date is hard-coded in this PREREG or in `eval.py`** (DP-22, DECISIONS.md item 11).
    `exclusions_v003.json` is the newest exclusions file at lock (v001, v002 superseded).
  - any prospective night whose `finished_at` is later than the next session's open (DP-04, applied
    mechanically, not by judgment).
  - **null-ladder denominator:** picks with no lane-plan ladder, no swing lane, or no `targets[0]`
    → excluded and counted (R1 measures 8 of 383 on the sealed part of this window, all on one
    night, and 0 cases of a lane present without an L3).
  - picks whose **L3 is at or through `C_t`** (`d_close ≤ 0`; an invalid target at publication —
    volatilx `services/super_agent_select_service.py:113-145`) or whose `outcome_target_invalid` is
    non-null → excluded and counted. This exclusion is decided at the close, **before** any session
    t+1 price exists, so it is identical for both arms.
  - picks with no session t+1 bar, or missing forward bars inside t+1..t+20 (halt, delisting) →
    cannot be graded in either arm; excluded from measurement and counted. This is a **measurement
    failure, not a classifier**: it never moves a pick between arms and never removes a night. A
    night is dropped if > 25% of its picks are ungradeable.
  - symbols with fewer than 60 daily bars dated ≤ t (ATR/beta/run-up undefined) → excluded, counted.
  - nights whose session t+20 falls after the last trading date of the pinned price freeze
    (immature) → excluded and counted. Maturity comes **from the trading calendar**, never from
    whether a price exists; right-censoring is never graded as a non-touch.
- **Not excluded — "not takeable", a property of the plan (§4; decided at lock).** A pick whose L3
  is at or through **that arm's own entry price** is not entered by that arm: no position, race
  non-WIN, result 0 ATR, counted per arm. For the open arm this catches picks that gapped through L3
  (rule 5: a target already passed at that entry is not a hit); for the limit arm it is impossible by
  construction, since `L3` is beyond `C_t` and `FILL_k` is on the other side of `C_t`. Dropping such
  picks instead would filter the denominator on a session-t+1 price (rule 14) and would remove
  exactly the picks that gapped to target (DECISIONS.md item 7). R1 measures the rule in the sealed
  window: **Plan M not takeable 9 of 369 (2.4%)**; **Plan L(k) not takeable 0 at both k**, which
  *verifies* the construction argument rather than assuming it (R1 §2(a)).
- **Contributing night (the floor unit, DP-21):** a night carrying **≥ 1 eligible pick**. Both arms
  are defined for every eligible pick, so **all four primary endpoints share one contributing-night
  definition** and one count gates all four. Per-arm composition counts (filled at 0.25, filled at
  0.5, not filled, not takeable) are reported but are **not** floor units, except where an arm is
  itself a reported sub-cell, which then needs its own 20 contributing nights. A matured night on
  which **no** row survives this funnel is a **non-contributing night, not an exclusion**: it is
  never added to `exclusions_vNNN.json` (which would silently change every other question's
  population) and never counted toward any floor; it is printed in the funnel with its cause.
- **Measured funnel on the sealed part of the window** (R1, `research/reports/STEWARD_Q011_exposure.md`
  §1; counts only, verbatim; pick nights 2026-06-01..2026-08-12, the last matured night in
  `manifest_prices_v001`): **383** published / in-window / non-excluded / matured rows → **−8** no
  lane plan → **−0** lane present without L3 → **−4** `outcome_target_invalid` → **−0**
  direction / `C_t` / ATR-history → **−2** wrong-side L3 (`d_close ≤ 0`) → **−0** missing session-t+1
  or forward bar → **369 eligible picks on 47 contributing nights** (48 matured nights). Fill
  composition: **232 filled / 137 not filled** at k = 0.25 and **157 / 212** at k = 0.5; hourly-bar
  coverage on session t+1 **369 / 369 (100%)**. These are exposure counts, not results: no touch, no
  race outcome, no return and no picks-minus-control difference was computed, and they gate nothing
  (§5).
  **Data note:** all **8** no-lane-plan rows fall on the single night **2026-06-02** (R1 §4.3), which
  is therefore the one matured night with zero eligible picks. It is **non-contributing, not
  excluded** — the exclusions file does not change — and the concentration is flagged to the Red Team
  as an unexplained payload gap, not as a design question for Q011.

## 3. Baseline(s) — what this must beat

- **B1 (primary baseline, H-058's own): the next-open market entry on the same picks, same nights,
  same grading** — Plan M in §4 (DP-03(b): the next-session open, Haci's option-spread entry). The
  primary contrasts are limit-minus-open, paired within night. This is the "Y's rate when X did not
  happen" baseline in its cleanest form: the same picks, two entry rules, one tape.
- **B2 (rule-5 distance-matched control; descriptive, never decides):** for each eligible pick, the
  10 nearest same-night **non-published** `sas_candidates` rows — the complement of the DP-28
  publication predicate — on `beta60` / `atr_pct` / `runup20` (from `prices_daily_split` bars dated
  ≤ t; standardized by the night's cross-sectional median and MAD; Euclidean; with replacement across
  picks; ties by symbol ascending) — the Q006 §3 construction, anchored at each control's **own**
  pick-night close:
  `L3_c = C_c × (1 + dir_p × d_close,p × atr_pct_c)`, `LIM_{k,c} = C_c × (1 − dir_p × k × atr_pct_c)`,
  graded with exactly the §4 plans from the control's own close and own session-t+1 bars, same
  direction, same 20-session window. Control rows never add to inferential n (rule 6). B2 answers
  "is the limit rule's result on SAS picks different from the same rule on comparable stocks" — the
  missed-trade effect appears on both sides and largely cancels there. It is **descriptive** here,
  following Q004, the desk's other entry-basis question, where the matched control is the
  absolute-framing baseline and the paired basis contrast is the primary.
- **B3 (descriptive, cross-question reconciliation):** the same picks entered at `C_t` (the DP-03(a)
  after-hours proxy, DP-11 — the basis Q007 and Q009 use) and at `E_AH` (Q004's definition verbatim,
  picks only). Neither decides; both exist so Q011's numbers reconcile with the rest of the desk.

## 4. Objective metric (rule 5 — price path, measured the way it is traded)

**Entry bases (both in scope under DP-03; this question's subject *is* the entry, so DP-11's
held-position rule does not apply — DP-11 exempts questions whose subject is the entry basis):**

- **Plan M (baseline, DP-03(b) next-session open).** If `dir × (L3 − O_1) ≤ 0` → **not takeable**
  (no position; race non-WIN; `r_M = 0`; counted). Otherwise enter at `O_1`; exit at the first touch
  of L3 within sessions t+1..t+20 at the L3 price — or at that session's open if a session opens
  through L3 (a resting exit limit fills at the better price) — and otherwise at the session t+20
  close. **No stop** (rule 5, DP-02).
- **Plan L(k) (the tested rule; a next-day intraday trigger, rule 5's third entry basis).** Rest the
  day limit `LIM_k` for session t+1. If `FILLED_k = 0` → **no position**; race non-WIN; `r_{L(k)} = 0`;
  counted. If `FILLED_k = 1` → enter at `FILL_k`; exit at the first touch of L3 **at or after the
  fill** within sessions t+1..t+20, on the same exit rule as Plan M; otherwise at the session t+20
  close. **No stop.**

Both plans run over the identical calendar window (sessions t+1..t+20), so the two arms are on the
same clock (DP-09) and the contrast is not a horizon comparison.

**Race outcome, per arm (the primary object; Q004 §4's construction, anchored at each arm's own
entry `X`):** over sessions t+1..t+20 from that arm's entry, which comes first —
- **WIN:** the regular-session high (bullish) / low (bearish) touches **L3**; or
- **LOSS:** the regular-session low (bullish) / high (bearish) touches `X − dir × 1.0 × ATR`.
Neither within the window → **NEITHER**. **The −1 ATR line is a measurement of which came first, not
an exit** (rule 5, DP-02); no plan in this file exits on it. WIN = 1; LOSS, NEITHER, TIE, not filled
and not takeable all score 0.

**Ordering rules, stated once and applied by `eval.py` with no judgment:**
1. **Adverse line versus the fill — no ambiguity exists.** `X − dir × 1.0 × ATR` lies strictly beyond
   `FILL_k` in the adverse direction, so by price continuity a session-t+1 touch of it necessarily
   occurs at or after the first touch of `LIM_k`. No hourly bar is needed.
2. **L3 versus the fill, session t+1 only.** L3 lies on the other side of `C_t`, so a session-t+1 L3
   touch may precede the fill. The fill hour `h*` is the first regular-session hourly bar on t+1
   whose low ≤ `LIM_k` (bullish; mirrored for bearish), from `prices_hourly_raw` converted to the
   signal-date split basis (`eval.py` asserts basis agreement per symbol-date and fails loudly). An
   L3 touch in a bar strictly before `h*` is **pre-fill and not a WIN**. An L3 touch inside `h*`
   itself, or on any session-t+1 bar when the symbol has no hourly bars in the freeze, counts as
   **post-fill (a WIN)** — the reading **less** favourable to the hypothesis, applied identically
   wherever hourly bars cannot order the pair (DP-45; DECISIONS.md item 3). The count of picks
   resolved by this rule is printed, and the opposite reading is printed as a named descriptive
   sensitivity. **The no-hourly-bars fallback is not exercised anywhere in the sealed window**:
   hourly coverage on session t+1 is 369 / 369 (R1 §2(c)); it survives for the post-lock nights and
   for the descriptive B2 control pool, whose symbols are not all carried in `p001_hourly_raw`
   (R1 §4.4), and those cases are counted, never back-filled.
3. **L3 versus the adverse line in the same session** (either arm): ordered with `prices_hourly_raw`;
   if the same hourly bar holds both, or the symbol has no hourly bars, the pair counts
   **adverse-first (LOSS)** — **DP-27**, applied identically in both arms so the convention cannot
   create the contrast. TIE and NEITHER are scored non-WIN, and their counts are printed separately.

**Primary endpoints (four, pre-specified, BH-corrected within this question — §7).** Both limit
distances H-058 names are primaries, and **all four endpoints carry verdicts**: the §5 demotion test
was decided at lock on R1's measured counts and neither arm is demoted (DECISIONS.md items 4 and 9).
For pick p on night t, with `F_{p,k}` the fill indicator:

- **P1 — the race (touch-race form, DP-01/DP-08/DP-42).**
  `Δ1_t(k) = mean_p[WIN_{L(k),p}] − mean_p[WIN_{M,p}]` over **all** eligible picks on night t.
  Estimand `m1(k) = mean_t Δ1_t(k)`, in percentage points.
  - **P1-A:** k = 0.25. **P1-B:** k = 0.5.
- **P2 — the money (the named execution plan's realized result, rule 5).**
  `r_p = dir × (exit_p − entry_p) / ATR_p` in ATR units, and `r_p = 0` where the arm holds no
  position. `Δ2_t(k) = mean_p[r_{L(k),p} − r_{M,p}]`.
  Estimand `m2(k) = mean_t Δ2_t(k)`, in ATR units per published pick. Negative = the limit rule costs
  money.
  - **P2-A:** k = 0.25. **P2-B:** k = 0.5.
  P1 is the mechanism; P2 is the money, and P2 is what licenses a rule (§8).

**Pre-specified decomposition (descriptive, printed with every P2 figure).** Exactly:
`Δ2_t(k) = MISS_t(k) + ADV_t(k)`, where
`MISS_t(k) = mean_p[(1 − F_{p,k}) × (0 − r_{M,p})]` — the cost of the trades the limit never got — and
`ADV_t(k) = mean_p[F_{p,k} × (r_{L(k),p} − r_{M,p})]` — the price advantage on the trades it did get.
The same split is printed for P1. `ADV` **is** the fill-conditional contrast, i.e. H-058's
adverse-selection mechanism, and it is **descriptive only** for the rule-14 reason in §1 and §6.

**Secondary, descriptive, never decides:**
- the **fill-conditional** race and ATR contrasts (`mean over filled picks of WIN_L − WIN_M`, and
  `ADV`), with their own CIs, labelled *"conditions on a session-t+1 path event; descriptive, does
  not decide (Q007 §4.1 variant C precedent; DP-41)"*;
- **fill rates** by k, by month, by score band, by `atr_pct` tercile, bull/bear; the share of fills
  taken **at the open** (a gap through the limit) versus intraday; sessions-to-fill;
- a **model-free limit-distance grid** — k ∈ {0.10, 0.25, 0.50, 0.75, 1.00} ATR — fill rate, P1 and
  P2 at each grid point. It is the only view of limit *distance* in the file and it **cannot license
  a specific distance** (§9);
- **B2** (matched controls under the same two plans), and the B2-adjusted versions of P1 and P2;
- **B3**: the same two endpoints with the entry at `C_t` (DP-03(a) proxy) and at `E_AH` (picks only,
  Q004's definition verbatim: the close of the first `prices_hourly_raw` bar whose bar end is at or
  after that night's `sas_runs.finished_at`, strictly before the next regular open, converted to the
  signal-date basis; picks without such a bar excluded from the sensitivity and counted);
- the **strict-fill sensitivity**: `FILLED_k` requiring `low_1 ≤ LIM_k − 0.01 × ATR` (queue-position
  realism, §10 threat 3), and the **opposite same-bar reading** of ordering rule 2;
- L1 and L2 first touch within 20 sessions, and **L3 within 40 sessions** (the platform's own swing
  lane window, matured nights only, reported alongside the primary per **DP-09**), under both arms;
- sessions-to-first-touch of L3 from each entry, and the touch-within-2 / 5 / 10-session forms
  (speed is descriptive here: DP-44 gives sessions-to-touch differences no MPE, and Q002 owns the
  speed claim);
- maximum adverse excursion from each entry in ATR; counter-direction swing-level touches within
  20 sessions (reported, never used as an exit — DP-02);
- the **committed L1–L6 scale-out** (`BAND_EXITS`, volatilx `scripts/generate_sas_trading_guide.py:89-95`)
  run under both arms: each fraction exits at its level's first touch from that arm's entry (at the
  level price, or the better open), fractions whose level was at or through the entry are recorded as
  unfillable and excluded from that fraction, the remainder closes at the session t+20 close,
  truncated and labelled so; `<80` is not traded per the guide; the trailing rules are not
  deterministic enough to simulate and are ignored;
- P1 and P2 in percent of price instead of ATR; close-to-close return from each entry at T+5 and
  T+20 — **fixed-horizon return is secondary and descriptive by rule 5 and never decides**.

**Quotability:** 20-session (and 40-session) bases → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** Night-level. **CI (decides):** stationary block bootstrap over the ordered
contributing nights, expected block length **10 sessions** (20-session forward windows overlap across
adjacent nights; Q004/Q007/Q009 use the same), 2,000 resamples; the date-clustered bootstrap CI is
printed alongside. **p-value:** paired sign-flip permutation on the night contrasts `Δ1_t(k)`,
`Δ2_t(k)` (the two arms are two plans on the same picks), 10,000 permutations, seed 20260913. Every
estimate prints n(contributing nights), n(contributing nights dated after the lock commit),
n(eligible picks), n(filled) per k, n(not filled) per k, n(not takeable) per arm, n(resolved by
ordering rule 2), n(hourly-unresolved ties, DP-27), n(control rows) and n(excluded, by reason).

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** and ≥ **20
  contributing nights per reported sub-cell**. All four primaries share the §2 contributing-night
  definition, so one measured count gates all four; a sub-cell below 20 nights is **SUPPRESSED** —
  no point estimate printed, not even "small n, directionally", counts only — and a SUPPRESSED
  sub-cell does **not by itself** make its endpoint INCONCLUSIVE (§8 clause 1). The weaker reading
  ("80 eligible nights with ≥ 20 contributing") is **not** used (DP-21). **No floor is ever lowered
  to hit a date.**
- **Binding maturity: 20 sessions** (DP-09). The 40-session companions are descriptive and computed
  only where they have matured.
- **Measured exposure (R1, returned 2026-09-13 — `research/reports/STEWARD_Q011_exposure.md`;
  counts only, no outcome of any kind, no bar after session t+1).** Population: exactly §2 (published
  picks under the DP-28 predicate, non-excluded nights per `exclusions_v003.json`, pick nights
  ≥ 2026-06-01, swing L3 present, `d_close > 0`, 20-session window matured in
  `manifest_prices_v001`; last matured pick night **2026-08-12**). Measured:
  1. **funnel** 383 → −8 no lane plan → −0 lane-without-L3 → −4 `outcome_target_invalid` → −0
     direction / close / ATR → −2 wrong-side L3 → −0 missing t+1 bar → **369 eligible picks**, on
     **47 contributing nights** of 48 matured (§2; the non-contributing night is 2026-06-02);
  2. **fills** 232 filled / 137 not filled at k = 0.25; 157 / 212 at k = 0.5; **not takeable** Plan M
     9 (2.4%), Plan L(k) 0 at both k;
  3. **contributing nights carrying ≥ 1 fill: 46 of 47 at k = 0.25, 44 of 47 at k = 0.5** — the input
     to the demotion rule below, which is discharged by it;
  4. **fills at the open** 89 / 232 (38.4%) at k = 0.25 and 43 / 157 (27.4%) at k = 0.5;
  5. **hourly-bar coverage on session t+1: 369 / 369 (100%)**; the successor freeze carries hourly
     bars for published symbols (R2), and B2 control symbols without published history do not have
     them — those pairs fall to §4 ordering rule 2's stated reading and are counted;
  6. **contributing nights per month** 19 (Jun) / 20 (Jul) / 8 (Aug, matured through 08-12), i.e. a
     **measured run-rate of 0.9216 contributing nights per session** (47 / 51 sessions,
     2026-06-01..2026-08-12).
  **R1 decides nothing about P1 or P2.** It settled two design questions before lock — the window and
  decision date (unchanged) and the demotion rule (discharged) — and every gate below is evaluated on
  `eval.py`'s own measured counts at the decision pass, never on R1 or on the projection.
- **Floor-date projection (mechanical extrapolation of R1's measured rate, not a forecast; it gates
  nothing).** At this question's own **measured 0.9216 contributing nights per session** (R1 §3 — a
  measured rate, not a rate borrowed from another question's funnel), with the three in-window
  excluded nights (2026-06-26, 07-02, 07-06) already removed from the measurement —
  - the primary window holds **112 sessions**, projecting **≈ 103 contributing nights**; the **80th**
    falls ≈ 35.8 sessions after 2026-08-12, i.e. a raw pick night of **≈ 2026-10-02**, inside the
    window — **not binding**;
  - **30 contributing nights dated after the lock commit** (DP-24): the 40 post-lock sessions
    2026-09-14..2026-11-06 project **≈ 37**, with the 30th reached after ≈ 32.6 sessions, a raw pick
    night of **≈ 2026-10-30** — inside the window with ≈ 7 nights of margin. **This is the binding
    gate**, not the 80-night floor;
  - **stratum floors are already met as measured**: 42 of 47 contributing nights carry a legal regime
    label (legal from 2026-06-09, FREEZE_v001 §7) and the calendar halves stand at 24 / 23. The
    halves' split point is re-derived from the final window at the decision pass.
  Every gate below is decided on the **measured counts printed by `eval.py`** from the frozen data,
  never on this projection, a run-rate, or R1's counts.
- **Window, decision date, extension and DEFERRED fallback (DP-43; DP-13; no outcome looks at any
  point):**
  - **Primary window: pick nights 2026-06-01..2026-11-06 inclusive**, after exclusions. On R1's
    measured rate it projects **≈ 103 contributing nights** and **≈ 37 post-lock contributing
    nights** — margin over both gates, chosen so that **PROSPECTIVELY_CONFIRMED stays reachable from
    this run** (DP-24 met; DP-31's HISTORICAL_ONLY handling does not apply and no successor
    replication question is needed). A shorter window that reached a date sooner was not taken
    (DP-43, DP-45).
  - **Decision date: Monday 2026-12-14.** The 20th session after 2026-11-06 is **2026-12-07**
    (Thanksgiving 2026-11-26 closed); the decision date adds the one-week freeze margin and lands on
    the first Monday on or after it. R1's independent binding-gate date (the 30th post-lock night,
    matured and margin-adjusted) is 2026-12-07, **earlier** than this date, so the measured rate does
    not push the decision date out — and a date is never pulled **in** to report sooner (DP-43,
    DP-45). **Window end, decision date and extension all stand unchanged from the draft; R1 moved
    nothing.** The Steward fixes the exact session-count date when building the successor freezes
    (R2). `eval.py` is written once (rule 9) and run **once**, then. **No interim looks.**
  - **Both gates, per primary endpoint, on measured counts.** Evaluation proceeds only if **every**
    primary endpoint has **≥ 80 contributing nights** and **≥ 30 contributing nights dated after this
    file's lock commit**, printed by `eval.py` from the frozen data. A shortfall on one endpoint is
    never covered by another's count.
  - **One automatic extension (DP-13; DP-43's +30 sessions).** If either gate is short at
    2026-12-14 on `eval.py`'s measured counts, the window extends **once**, automatically and with no
    new question to Haci, to pick nights **2026-06-01..2026-12-21** (= 2026-11-06 + 30 sessions),
    decision date **Monday 2027-02-01** (2026-12-21 + 20 sessions = 2027-01-21 with 2026-12-25,
    2027-01-01 and 2027-01-18 closed, plus the same one-week freeze margin, first Monday on or after;
    the Steward fixes the exact date when building the second freeze pair). The extended run uses the
    **unmodified `eval.py`** and the same gates. Both dates sit inside DP-43's 12-month ceiling
    (3.0 and 4.6 months from the 2026-09-13 lock).
  - **DEFERRED fallback.** If a gate is still short after that single extension, Q011 goes to
    **DEFERRED** (`research/questions/DEFERRED.md`, with the measured counts) rather than running
    under-powered. There is no second extension, and a gate shortfall is **not** an INCONCLUSIVE
    verdict (§8).
  - **Nothing weakens.** No gate is reduced, no floor is lowered to hit a date (DP-21), and a short
    count never licenses falling back to the fill-conditional contrast, which is descriptive for
    knowledge-time reasons and not for want of sample.
- **Demotion test — decided at lock, and discharged (DP-43; DECISIONS.md item 9).** The test was
  whether a k arm carried fewer than **20 contributing nights with ≥ 1 fill**; it is settled here,
  symmetrically for both k, on R1's measured counts rather than after the numbers.
  **Measured (`STEWARD_Q011_exposure.md` §2(b)): 46 of 47 contributing nights carry ≥ 1 fill at
  k = 0.25 and 44 of 47 at k = 0.5 — both far above the 20-night floor, so NEITHER ARM IS DEMOTED.
  All four primaries (P1-A, P2-A, P1-B, P2-B) carry verdicts and BH runs across m = 4.** *Nights
  carrying ≥ 1 fill* is monotone non-decreasing as nights accrue, so 46 and 44 are lower bounds for
  the registered window. **No arm is ever demoted after lock** (DP-43): this rule is spent and cannot
  fire again, and a thin fill cell at the decision pass is handled where it belongs — as a SUPPRESSED
  sub-cell (§8), never by moving a primary to descriptive.
- **Freeze discipline (DP-23; routed request R2 — open, due at the decision date 2026-12-14, or
  2027-02-01 if the DP-13 extension fires; not a blocker for lock).** Nights ≤ 2026-09-10 stay
  pinned to `manifest_v001` / `manifest_prices_v001`. Nights after
  2026-09-10 enter only through successor freezes — `manifest_v002` (selections, same SQL, same
  exclusion criterion) and `manifest_prices_v002` (same Alpaca queries), with the daily symbol list
  extended to **every candidate on the new nights, published and unpublished** (B2 needs the
  unpublished symbols' closes, session-t+1 bars and forward bars), **plus hourly bars for published
  symbols** (ordering rule 2, the DP-27 tie-breaks and the `E_AH` sensitivity), carrying **20**
  forward sessions beyond the last included pick night (40 where the descriptive companion is to be
  computed). A second pair is built **only if** the DP-13 extension fires. `eval.py` takes the window
  start and end, the manifest paths, the exclusions-file path and the output directory as inputs —
  **no hard-coded dates, manifest names or paths** — so the byte-identical script serves both runs.
  It records every sha256 and prints pre-lock and post-lock night counts separately. **Neither
  successor freeze exists today, and neither blocks the lock.** Nights whose hourly bars are missing
  fall back to ordering rule 2's stated reading and are counted; nights whose unpublished-candidate
  bars are missing are excluded from B2 and counted, never back-filled.
- Sub-cells (bull / bear; score band < 80 / 80–85 / 85–90 / 90+; tape stratum; regime label;
  `atr_pct` tercile; L3 ATR-distance tercile) are reported only where they clear **20 contributing
  nights**. Bear and 90+ cells are expected to be SUPPRESSED (DATA_NOTES: elite is thin and
  shrinking).

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-06-01** through the decision date
  (2026-11-06, or 2026-12-21 if the DP-13 extension fires — §5).
  *Justification (one sentence):* EXPLORE_001 ran the L3-before-(−1 ATR) race and the day-1
  dip/gap constructions on April–May and reported them into the backlog — H-058's own line quotes
  in-sample fill counts (≈ 150 fills at 0.25 ATR and ≈ 100 at 0.5 ATR from 280 picks / 35 nights) —
  so the in-sample nights are contaminated for this question and are not used, not even as a
  descriptive panel.
  *Contamination check on the sealed period (registrar; no results directory was read):* the desk's
  sealed-period descriptive outputs recorded in `research/BACKLOG.md` (the weekly-snapshot lines
  under H-010, H-011, H-013, H-051, H-062) and the one weekly line disclosed in Q007 §6 report
  entry-basis, band, lane and gap figures; **none is conditioned on a limit fill and none reports a
  fill rate or a dip-entry result.** Two residual exposures are disclosed rather than corrected for:
  (i) the platform's own Manual Trading Guide publishes sealed-window **dip expectations** by band —
  "77–83% of picks pull back ≥ 2% (medians 7–8%) … Do not plan on being offered a dip entry in the
  top bands" (volatilx `scripts/generate_sas_trading_guide.py:531-537`) — which is a signed-MAE
  statistic in percent over the whole window, not a day-1 fill at an ATR distance, but is adjacent
  enough that Haci may have seen a related number; (ii) `STEWARD_Q007_exposure.md`'s arm counts, as
  quoted in Q007 §5, show how many sealed picks opened ≥ 2% against the pick — an exposure count with
  no outcome attached, and a near-neighbour of the fill event. Neither supplied a threshold here: the
  0.25 and 0.5 ATR distances are H-058's own (DP-25), the −1 ATR adverse line is Q004's registered
  line, L3 is the platform's level and the 20-session clock is DP-09.
  *(iii) The one pre-lock read of this question's own data is `STEWARD_Q011_exposure.md` (R1),
  disclosed in §2 and §5: a counts-only exposure report — funnel, fill counts, coverage, run-rate —
  built under a binding protocol that read no bar after session t+1 and computed no touch, no race
  outcome, no return and no picks-minus-control difference. It fixed no threshold, no window end and
  no decision rule that was not already drafted, and it decides no endpoint.)*
- **Catalyst-layer regime change:** the window sits entirely after the 2026-06-01 fix
  (`exclusions_v003.json` `catalyst_layer_regime_change`; platform commit 69ef05f).
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date; Half B = after. `in_sample_end = 2026-05-29` marks only what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v003.json` `regime_label_point_in_time_from`). It is used only for nights
    ≥ 2026-06-09, only `regime_version = 'v1.2'`, and only where the row is a same-evening write per
    its declared availability; a later-posted row is treated as missing. Nights 2026-06-01..06-08
    carry no legal label and are stratified by the SPY proxy only, flagged.
  - Primary tape stratum for every night, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's
    trailing 20-session return × tercile of SPY's trailing 20-session realized volatility, from SPY
    bars dated ≤ t in `prices_daily_split`. **Tercile cut points are expanding-window** (for night t,
    computed from every session 2026-03-02..t), so no later night's data sets an earlier night's
    stratum. Cells < 20 contributing nights SUPPRESSED.
  - The report describes the tape in words from SPY's path and never implies a regime label existed
    before 06-09.
- **Knowledge time (rule 14) — every input declared. Q011 needs no rule-14 exception and requests
  none: both plans are fully specified at 16:05 ET on the pick night, every eligible pick is in the
  denominator of both arms, and no session-t+1 quantity classifies, filters, matches or stratifies
  any pick (DP-05 untouched; DP-41 respected).** The fill, the not-takeable test and every touch are
  **execution and outcome measurement**, the same status Q007 §6.1 gives an exit fill and a
  gap-through touch — not feature use. The one construction that *would* condition on a session-t+1
  path event, the fill-conditional contrast, is **descriptive and never decides** (§1, §4).

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `dominant_direction`, `overall_score`, `best_timeframe` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | population, direction, band |
  | swing lane plan, **L3** (`targets[0]`) | `sas_candidates.public_payload_json.lane_plans` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | level |
  | `outcome_target_invalid` (exclusion audit only) | `sas_candidates` | set at publication for new rows | exclusion |
  | control-candidate pool (non-published rows for night t) | `sas_candidates` | pick night, 16:05 ET | B2 pool (descriptive) |
  | **`C_t` (limit reference and ATR denominator), ATR14, beta60, runup20, `d_close`, `LIM_k`** | `prices_daily_split`, bars dated ≤ t | pick-night close, 16:00 ET | limit price, distances, matching |
  | SPY tape (trailing return, trailing vol, expanding terciles) | `prices_daily_split`, SPY bars ≤ t | pick-night close | stratum |
  | regime label (v1.2, nights ≥ 2026-06-09, same-evening rows only) | `market_regime_daily` | pick night, 16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time, before the t+1 open on every included night | DP-04 exclusion; `E_AH` clock (sensitivity) |
  | session t+1 open / high / low / close; hourly bars on session t+1 | `prices_daily_split`, `prices_hourly_raw` | session t+1 | **execution measurement only** — whether the resting order filled, at what price, in which hour, and whether the open arm was takeable |
  | sessions t+2..t+20 (t+40 for the companions), hourly bars for tie-breaks | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **outcome only** |
  | `E_AH` after-hours price (sensitivity only) | `prices_hourly_raw` | publication, pick night | descriptive entry price only |

  **What `eval.py` must enforce:** the eligible-pick set, both plans' parameters (`LIM_k`, `L3`,
  `ATR`, direction) and every stratum label are computed and written to a frozen per-pick table
  **before any session-t+1 or later bar is loaded**; the run fails if any t+1-or-later field is
  referenced in eligibility, matching or stratification. `sas_selection_excursion` /
  `outcome_*` / `level_hit_*` columns are never inputs (calendar windows, close basis, recomputed
  weeks later — volatilx `services/sas_excursion.py:8-18`, `:336-354`).
  `uoa_symbol_daily.fwd_return_*` is **banned** (the May–June freeze is not fixed — FREEZE_v001 §5);
  no UOA table is used.

## 7. Multiple testing

- **Within the question:** **BH across m = 4** — P1-A, P1-B, P2-A, P2-B — at q ≤ 0.10; the verdict
  uses q. Both limit distances are primaries (DECISIONS.md item 4) and **neither arm is demoted**
  (§5, discharged at lock on 46/47 and 44/47 nights with ≥ 1 fill), so all four endpoints carry
  verdicts and **m = 4 in every branch** — there is no path on which m falls and no bar is lowered
  for any endpoint (Q009 precedent). All secondaries, including the fill-conditional contrasts and
  the decomposition, print raw p only, marked "descriptive, does not decide".
- **Across the family: F7 Path, entry timing & volatility** (DP-29 — the primary endpoint's subject
  is the entry basis, the same subject as Q004, and `research/BACKLOG.md` files H-058 in F7). F7
  holds H-053…H-060, H-065, H-066 (10 hypotheses). Registered F7 questions at registration:
  **Q002 (H-065, 3 primaries)**, **Q004 (H-054 + H-057, 2 primaries)** and **Q011 (H-058, 4
  primaries)** — 9 primaries in the family correction. The Reporter applies BH across all primary
  endpoints of registered-and-run F7 questions and prints both the within-question and the
  within-family q.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q004 (F7, same family):** shares the L3-before-(−1 ATR) race object, the −1 ATR line and most
    nights and picks. Q004 contrasts after-hours / open / 10:00 **market** entries; Q011 contrasts a
    **resting limit** against the open. The races are anchored at different entries, but the two
    results are **not independent evidence and must never be presented or counted as two
    confirmations**; the Reporter cross-references rather than duplicates.
  - **Q007 (F4):** its AGAINST arm (a next open ≥ 2% against the pick) mechanically overlaps this
    question's fills — a pick that opens 2% against will normally fill a 0.25 ATR limit at the open.
    Q007 asks a **hold/exit/add** question about a position entered at `C_t`; Q011 asks whether to
    enter at all and at what price. Different families, corrected separately (rule 8; DP-29); the
    overlap is a non-independence hazard handled by the same "never two confirmations" sentence, and
    the share of Q011's fills taken at the open is printed so the reader can see the intersection.
  - **Q009 / Q010 (F6):** adjacent path shapes (stop-then-target) using the printed stop, not an ATR
    entry line; nothing is merged.
  - **H-066 (capital recycling)** would reuse this question's fill rates; it is not registered and is
    not tested here.
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1(k)` in percentage points of race-win rate (limit minus open, paired within night, ITT);
`m2(k)` in ATR units per published pick (limit minus open, ITT).

**MPE: P1 +5.0 pp** — the standing number for a touch/race-rate endpoint (**DP-20**, **DP-44**); it
is a within-night paired contrast of two plans on the same picks and the same tape (Q004 T1/T2's
structure), which removes the tape confound Q007's difference-of-differences uplift guards against,
so **no uplift is proposed** (DECISIONS.md item 10). **P2 0.25 ATR** (**DP-10**, **DP-44**; the
standing number for every per-trade ATR-denominated endpoint, not re-asked), measured **per published
pick — the ITT denominator of §4, never rescaled to a per-filled-trade basis**, since fills are a
subset and rescaling a diluted ITT mean would lower the bar. Both are two-sided: H-058 predicts
negative values, and a positive result beyond MPE is a confirmed finding with the opposite sign.

Per endpoint (two-sided; the verdict carries its sign):

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **contributing nights ≥ 80** and **≥ 30 contributing nights dated after the lock commit** (§5
     gates, on measured counts), **and ≥ 20 contributing nights for any sub-cell that is reported**
     (DP-21) — a sub-cell below floor is **SUPPRESSED** (no point estimate, counts printed) and does
     **not by itself** make the endpoint INCONCLUSIVE (Q007 §8 clause 1's wording); the
     stratification protection that rule 7 requires lives in clauses 5 and 6, neither of which is
     weakened by this reading;
  2. `|m| > MPE` (5.0 pp for P1, 0.25 ATR per published pick for P2);
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question (m = 4 — all four endpoints are primary, §7);
  5. the point estimate has the **same sign in both halves**, and neither half is beyond MPE in the
     opposite sign;
  6. no tape stratum with ≥ 20 contributing nights is beyond MPE in the opposite sign.
- **NULL:** floors met **and** 95% CI includes 0 **and** `|m| < MPE`. "Resting a limit a quarter ATR
  below the close neither helps nor hurts" is a real finding and is ledgered with the same care.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, a tape stratum with ≥ 20 contributing
  nights beyond MPE in the opposite sign, `0 < |m| ≤ MPE` with the CI excluding 0 ("real but below
  MPE", rule 6), or CI including 0 with `|m| ≥ MPE`. **A SUPPRESSED sub-cell is not by itself
  INCONCLUSIVE** (clause 1); what bites is a *reported* sub-cell below floor, which must not happen —
  below floor, nothing is reported but counts. **A gate shortfall is not INCONCLUSIVE either**: it
  fires the single DP-13 extension, then DEFERRED (§5).
- **What licenses a rule.** A guide line or platform change requires **P2 CONFIRMED** for that k
  (§9). **P1 alone never licenses a rule**: it says how often the rule won the race, not what the
  rule made. P1 CONFIRMED with P2 NULL is reported as "the limit rule changes how often you win the
  race but not what the trades are worth at this size".
- **What a confirmed sign does and does not mean (binding on the report).** A CONFIRMED-negative
  P1/P2 means **"resting a limit at k ATR below the pick-night close costs this much per published
  pick relative to buying at the open"**. It does **not** establish H-058's adverse-selection
  mechanism: the ITT number contains the missed trades, and the mechanism lives in the descriptive
  `ADV` component, which carries no verdict (§1, §4, §10 threat 1). Any sentence about "the dip is
  information against the thesis" must quote `ADV` and label it descriptive. The report prints
  `MISS` and `ADV` beside every confirmed `m2`.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — it requires **≥ 30
  contributing nights dated after this file's lock commit** (DP-24, DP-21), frozen in the successor
  manifests and never inspected earlier, reproducing the sign of the confirming endpoint under the
  unmodified `eval.py`. The clause does not weaken: if the window cannot supply 30, the DP-13
  extension fires and then DEFERRED — the 30 is never reduced. No subscriber-facing statement before
  that (rule 10); even then the basis is NON_QUOTABLE until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform **already invites a limit entry** and says almost nothing about whether to wait
for one: each lane plan carries a written `entry` price that may sit far from spot — the stray beyond
±5% is a dark flag that logs and never rejects (volatilx
`services/super_agent_select_service.py:94`, `:101-111`, written at `:155-161`) — and the Manual
Trading Guide's pullback section gives band-level dip expectations with the line *"Do not plan on
being offered a dip entry in the top bands"* (`scripts/generate_sas_trading_guide.py:531-537`),
while the add-on-dip protocol is explicitly withheld for want of data (`:543-545`). Nothing measures
what a resting limit actually returns.

Rules below fire only where §8 licenses one (**P2 CONFIRMED** for that k), and only after
PROSPECTIVELY_CONFIRMED for anything subscriber-facing (rule 10):

- **P2 CONFIRMED negative (the limit rule costs money):** a Manual Trading Guide line — "do not rest
  a limit below the pick-night close waiting for a day-1 dip; the picks that dip to you are not worth
  the picks you miss — buy at the open" — printed with the measured cost per published pick in ATR
  and the measured fill rate beside it, and with the `MISS` / `ADV` split shown so the reason is
  visible. Brief: a **flag-off** field on the pick card and in the lane plan showing the 0.25 and
  0.5 ATR distances from the pick-night close with the historical fill rate, so the printed lane
  `entry` is read as a reference, not as an order to rest; the guide's pullback section gains the
  fill-rate table.
- **P2 CONFIRMED positive (the limit rule makes money):** the opposite guide line — "resting a limit
  at k ATR below the close pays for the trades it misses" — with the fill rate, the cost of the
  missed trades and the net figure all published together, never the net alone.
- **P1 CONFIRMED with P2 NULL:** a descriptive card line about how often each entry rule reaches L3
  first, and no entry rule in the guide.
- **The limit-distance grid (§4) never licenses a specific distance.** A confirmed verdict speaks for
  the k it was registered at; choosing a different k is a new PREREG.
- **All four NULL:** no entry rule. The guide records that resting a day-1 limit is neither better
  nor worse than buying at the open at this size, the add-on-dip protocol stays withheld, and F7
  effort moves to H-059 / H-060.
- Owner: implementer. Ship flag-off with a byte-identical checksum on the old path; shadow ≥ 20
  trading days before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **The ITT contrast mixes two effects, and one of them is nearly mechanical.** A rule that takes
   only the picks that dip will differ from one that takes all of them whenever picks have a non-zero
   expected result from the open; the `MISS` component carries that, and it pushes both primaries
   negative before any adverse selection exists. This is the honest score of the strategy a trader
   would follow, but it is **not** H-058's mechanism. Mitigations, all pre-specified: the `MISS`/`ADV`
   decomposition is printed with every estimate; §8 binds what a confirmed sign may be said to mean;
   the fill-conditional contrast and the B2 control version (where the missed-trade effect appears on
   both sides and largely cancels) are reported as descriptives. The alternative — conditioning the
   primary on the fill — is a rule-14 classifier the desk cannot adopt (§1, §6; DP-41).
2. **Knowledge-time leakage around the fill.** The defence of this design is that the fill is
   execution, not classification. The residual risk is drift: a session-t+1 quantity slipping into
   eligibility, matching or stratification (a coverage filter, a "valid fill" screen, an
   `atr_pct` recomputed on t+1 bars). §6 requires `eval.py` to freeze the eligible set and both
   plans' parameters before any t+1 bar is loaded and to fail on any other reference; the Red Team
   should check this specifically.
3. **A printed low is not a fill.** A limit resting exactly at the session's low may never trade —
   queue position is invisible in daily and hourly bars. Counting a touch as a fill is optimistic for
   the limit arm, which is conservative with respect to H-058 (DP-45), and the strict-fill
   sensitivity (`low_1 ≤ LIM_k − 0.01 × ATR`) is printed beside every primary. Neither version models
   partial fills or slippage.
4. **The fill arm is partly a gap arm.** Picks that open against the pick fill at the open by
   definition, so this question's filled subset overlaps Q007's AGAINST arm and inherits its
   confound (large gaps are earnings and news). The share of fills taken at the open is a headline
   number — measured at **38.4%** (89/232) at k = 0.25 and **27.4%** (43/157) at k = 0.5 on the
   sealed window (R1 §2(a)), i.e. a substantial minority of the limit arm is a gap arm — and the two
   questions' results are never counted as two confirmations (§7).
5. **Ladder levels are not ATR-scaled.** L3's distance in ATR varies widely (volatilx
   `ai_agents/principal_agent.py:530-575`), so the race is partly a distance test while the limit
   distance is in ATR by construction. The L3 ATR-distance tercile cell and the `atr_pct` tercile
   cell are reported; the B2 control inherits the identical ATR distance.
6. **Not-takeable penalises the open arm exactly when the pick worked best.** A pick that gaps
   through L3 gives the open arm no position (rule 5: a target already passed at entry is not a hit),
   which flatters the limit arm and works against H-058. On the sealed window the rule bites on
   **9 of 369 picks (2.4%)** in the open arm and **0** in either limit arm (R1 §2(a)), so the
   asymmetry is real but small. The count is printed per arm, and a sensitivity excluding those picks
   from **both** arms is reported descriptively — never as the primary, because that exclusion would
   filter the denominator on a session-t+1 price (DECISIONS.md item 7).
7. **One tape.** The whole window is Jun–Dec 2026. A sign that appears in only one half fails §8
   clause 5; nothing here speaks to the strong April–May tape, where dips recovered more.
8. **Overlapping 20-session windows** inflate precision; the block length is fixed here (10 sessions)
   and not chosen after seeing results.
9. **Hourly-bar coverage decides ordering rule 2.** `manifest_prices_v001` carries hourly bars for
   published-pick symbols only (227 symbols; Q007 §4), so B2 controls are graded on daily bars with
   the stated conventions, and any published symbol missing hourly bars falls to the conservative
   reading. Measured on the sealed window: **369 / 369 eligible picks (100%)** have session-t+1
   hourly bars, so the fallback is **not exercised there at all** (R1 §2(c)); the residual exposure
   is the post-lock nights, where R2 holds the successor freeze to the same published-symbol hourly
   scope, and the B2 control pool, whose symbols are not all in `p001_hourly_raw` (R1 §4.4). Coverage
   counts are printed by `eval.py` in both runs.
10. **The stock path is a proxy for the spread.** Both plans are equity trades; a vertical opened on
    a limit fill behaves differently (theta, IV, strike width), and the desk holds no option prices
    (`research/questions/DEFERRED.md`; ENHANCEMENTS.md EN-011). Any §9 guide line about spreads must
    say so.
11. **Null-ladder and wrong-side-L3 denominators.** Both are excluded and counted; the question
    speaks only for published picks carrying a swing L3 on the correct side of the pick-night close,
    and the report prints that share by month and by score band. Measured on the sealed window they
    are small but lumpy: 8 null-ladder rows, **all on the single night 2026-06-02**, which is
    therefore non-contributing (not excluded, §2), plus 4 `outcome_target_invalid` and 2 wrong-side
    L3 (R1 §1).
12. **`C_t` is not a price anyone fills at.** It is used here only as the **reference** for the limit
    distance and the ATR denominator — which is exactly how a trader placing the order after
    publication would use it — but a pick that moved far after hours may see its 0.25 ATR limit
    already through at the open. That is a fill at the open and is counted as such.
13. **Matching on 3 features may not span selection** (Q006 threat 1). B2 is descriptive here, and
    post-match standardized mean differences are printed.
14. **Elite is thin and shrinking** (DATA_NOTES: 12 / 8 / 3 / 2 picks per month since June). The 90+
    cell is SUPPRESSED below 20 contributing nights rather than reported small.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: R2 — successor freezes
(`manifest_v002` / `manifest_prices_v002`), due at the decision date, not a blocker for lock.
