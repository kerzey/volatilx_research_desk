# Q015 — band_85_90_updown: do picks scoring 85–90 reach the swing target and then hand it back more often than picks scoring 80–85, and does exiting at the touch pay in that band?

**Status:** REGISTERED — decisions applied, locked by committing this file (`PREREG_LOCKED --by desk`, DP-46). Nothing in this file is open.
**Family:** **F7 Path, entry timing & volatility** (hypothesis **H-060**, filed in F7 in `research/BACKLOG.md`). DP-29 is ambiguous here — P1's subject is the path after selection, P2/P3's subject is an exit plan (F6's subject, the ground on which Q009 and Q012 were re-filed) — so the question stays where the BACKLOG files it **and** carries the F6 companion correction: **q ≤ 0.10 is required in both families** for the two exit-plan primaries (§7). H-060 is counted in F7 only, once.
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices/outcomes):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; base_manifest_sha256 b03f355a…bef374) — **plus** the successor selection and price freezes named in §5 (DP-23), without which this question cannot reach its floors.
**Exclusions:** research/data/exclusions_v003.json (`manual_runs.trading_dates`, `non_session_runs.trading_dates`, `uncorroborated_publication_runs.trading_dates`) — the newest exclusions file (DP-22); `eval.py` reads the JSON, no hard-coded dates.
**Measured exposure (`research/reports/STEWARD_Q015_exposure.md`, 2026-09-13, counts only):** on pick nights 2026-06-01..2026-08-12, **48 matured nights / 383 published picks → 303 eligible** after the §2 funnel; **band A (85–90) 38 picks / 21 nights, band B (80–85) 249 / 47, band E (90+) 15 / 14, band U (<80) 1 / 1**; **P1/P2 paired contributing nights = 21** and **P3 band-A contributing nights = 21** (the identical set — `nights_A ⊂ nights_B` in this window); measured rate **21/51 = 0.4118 paired nights per session, declining month over month** (June 0.476, July 0.409, partial August 0.250). The §5 schedule is computed from the **slowest** of those rates. **Every gate is decided on `eval.py`'s own measured counts at the decision pass**, never on this report or on a projection.
**Registered by:** registrar · **Approved by:** desk (DP-46) · **Date:** 2026-09-13
**Decisions:** DECISIONS.md

---

## 1. Hypothesis (plain English)

**Picks scoring 85–90 are the ones that run to the swing target and then give it back: more often than
picks scoring 80–85, they touch L3 and then trade back down to the swing lane's counter level inside
the same 20 sessions — so in that band, taking the money at the L3 touch beats holding the position
through.**

BACKLOG H-060 reads: *"Up-then-down in the 85–90 band: 85–90 picks touch L3 and then revisit the
swing counter level more often than <80 picks, so holding through hurts this band and exiting at the
touch helps — baseline: <80 band and 90+ band."* It names no window, no counter-level definition, no
entry, no exit plan and no decision. This PREREG fixes all of them (§2–§4). No sign is presumed;
every test is two-sided.

**One thing about H-060 changes here, and it is not cosmetic: its two named baselines do not exist in
any window this desk can register.** The `<80` band is not a thin cell, it is **closed by
configuration** — `SuperAgentSelectConfig.publication_floor = 80.0` (2026-07-07, volatilx
`services/super_agent_select_models.py:86-91`, `docs/SAS_CONVICTION_TIER_DECISION.md` §5.1) drops
every sub-80 bull to the dark set with `selected_rank` NULL, and DP-28 excludes dark rows from every
arm; the band had already stopped appearing after May. No amount of waiting recovers it: the Steward
measures **1 eligible `<80` pick on 1 night** in the whole 2026-06-01..2026-08-12 matured window, and
that single row is dated 2026-06-02 (`STEWARD_Q015_exposure.md` §2, §4). The `90+` band is measured at
**15 eligible picks on 14 of 48 matured nights** and is **shrinking** — 10 contributing nights in June,
4 in July, **0** in the matured part of August (same report §2, §9; DATA_NOTES) — so as a *primary*
comparator it needs 80 contributing nights on a cell carrying about one pick a night, which lands the
decision date past DP-43's 12-month ceiling, and a ceiling sends a question to DEFERRED rather than
being stretched to fit. **The primary comparator is therefore the adjacent traded band, 80–85** (§3 B1)
— the desk's standard adjacent-band baseline (H-002, H-010) and the *stricter* of the available
contrasts, since 80–85 is closer to 85–90 than `<80` ever was. `90+` and `<80` are carried as
**descriptive arms, demoted at lock** under DP-43 and, at 14 and 1 contributing nights, **SUPPRESSED**
(counts only, no point estimate); they can return no verdict here (§3, §5, §8). H-060 is not deferred,
because the contrast it is really about — 85–90 against the band below it — is testable now at full
floors; a properly powered 85–90 vs 90+ contrast is a separate future question (§3 B1′).
(DECISIONS.md item 1, DEFAULTED under DP-43.)

**Three things are tested as primaries** (§4), all on published picks scoring 80–90, all on the
**20-session clock from the pick-night close** (DP-09), all two-sided:

- **(P1, the shape)** does the 85–90 band reach L3 and then revisit the swing counter level, inside
  20 sessions, on a larger share of picks than the 80–85 band, on the same nights;
- **(P2, the money, band contrast)** is "exit at the L3 touch minus hold through" worth more in the
  85–90 band than in the 80–85 band;
- **(P3, the money, in the band)** is "exit at the L3 touch minus hold through" worth more than
  nothing in the 85–90 band itself — the endpoint that would license an exit rule (§9).

**What P1 is and is not.** P1 is an **unconditional joint event** over every eligible pick: touched
L3, *then* revisited the counter level. The conditional form H-060's words suggest — *given* it
touched L3, how often did it hand it back — conditions the denominator on a post-entry path event; it
is computed, printed and decomposed out of P1 (§4), and it is **descriptive: it never decides**. A
band can score a high P1 simply by touching L3 more often, so the L3-touch rate itself is printed
beside every P1 figure and the decomposition `P1 = P(touch) × P(revisit | touch)` is mandatory in the
report.

## 2. Population

- **Unit of inference: the trading night** (rule 6). Pick rows are averaged within a night per band
  first; P1 and P2 are **within-night paired** band differences, so the night's tape is held fixed.
- Source tables (manifest_v001 and its successors): `sas_candidates` (`qualified`, `selected_rank`,
  `overall_score`, `dominant_direction`, `best_timeframe`,
  `public_payload_json` → `lane_plans.swing_trading.{entry, stop, targets}`, `outcome_target_invalid`
  for the exclusion audit only, `score_details_json` for the band-integrity check in §10 threat 12),
  `sas_runs` (`finished_at`, DP-04).
- Source tables (manifest_prices_v001 and its successors): `prices_daily_split` (pick-night close,
  forward bars, ATR14, beta60, run-up, SPY tape), `prices_daily_raw` (split-factor snapping only),
  `prices_hourly_raw` (same-session ordering of the L3 touch against the counter touch, published
  symbols).
- **Treatment and comparator rows:** every **published** pick — `qualified IS TRUE AND selected_rank
  IS NOT NULL` (DP-28); dark-lane and qualified-false rows are never in any arm — on a non-excluded
  night in the §6 window, carrying a `swing_trading` lane plan with a first target and a stop.
- **Band assignment**, from the published `overall_score`, half-open intervals, no rounding:
  **A = [85, 90)** (the treatment band, H-060's own cut — not re-united, DP-25),
  **B = [80, 85)** (the primary comparator), **E = [90, ∞)** and **U = (−∞, 80)** (descriptive only).
  The platform's own sub-bands **85–88** and **88–90** (volatilx
  `scripts/generate_sas_trading_guide.py:78-84`) are printed as sub-cells where they clear 20
  contributing nights, because the known finding this hypothesis is the path face of ("88–90
  underperforms 90+") lives in the upper half of band A. They are **sub-cells, not arms**: measured
  today at **85–88 = 26 picks / 18 nights** and **88–90 = 12 / 9** (`STEWARD_Q015_exposure.md` §5),
  both below 20 as of the freeze and both projecting comfortably above 20 over the registered window
  at its slowest measured rate; whichever way `eval.py`'s counts fall at the decision pass, they are
  governed by the sub-cell rule (< 20 contributing nights ⇒ SUPPRESSED, §5, §8 clause 1) and never by
  demotion or promotion of an arm.
  `eval.py` **re-derives** each pick's band from `score_details_json` where the layer subscores are
  present and **fails loudly** on a disagreement with `overall_score` beyond 0.05 (§10 threat 12).
- **Lane, level and clock (DP-42, DP-09).** The hypothesis names the swing target and the swing
  counter level, so the level is **L3** = `lane_plans.swing_trading.targets[0]` (volatilx
  `services/sas_conviction_card.py:182-187`) and the primary clock is **20 sessions from entry**
  (DP-09); the platform's own 40-session swing window is reported alongside, descriptively, wherever
  it has matured.
- **Definitions (all prices in the signal-date split basis):**
  `C_t` = the pick's **actual** regular-session close on pick night t from `prices_daily_split` (never
  the platform's `spot_close`, stale on re-run nights — EXPLORE_001 §9);
  `ATR` = ATR14 from `prices_daily_split` bars dated ≤ t (the platform's `atr_pct` is corrupted around
  splits — DATA_NOTES / PI-003; not used);
  `dir` = +1 bullish / −1 bearish from `dominant_direction`;
  `X` = the **entry**, = `C_t` — the DP-03(a) after-hours proxy in DP-11's construction, one basis for
  picks and for the distance-matched controls (§4; DECISIONS.md item 3);
  `L3` = the printed swing first target, `d_L3 = dir × (L3 − X) / ATR`, required > 0;
  **`S` = the counter level = the printed swing-lane stop** `lane_plans.swing_trading.stop` — the same
  line Q009, Q010 and Q008 §4 read, and the platform's own documented fallback where the analysis-report
  blob is unavailable, as it is in every freeze this desk holds (DECISIONS.md item 2; §10 threat 3),
  `d_S = dir × (X − S) / ATR`, required > 0. `S` is used **only as a measured line, never
  as an exit** (rule 5, DP-02): no plan in this file stops out.
- **Exclusions — each counted per band and printed in the results header, never silently dropped.
  Every exclusion uses only inputs available by 16:05 ET on the pick night, the trading calendar, or a
  measurement failure:**
  - nights in **`research/data/exclusions_v003.json`** (`manual_runs.trading_dates` ∪
    `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`); in-window
    those are **2026-06-26**, **2026-07-02**, **2026-07-06**. `eval.py` reads the JSON; **no date is
    hard-coded** here or in `eval.py` (DP-22).
  - any prospective night whose `finished_at` is later than the next session's open (DP-04),
    mechanically, not by judgment.
  - **null-ladder denominator:** no lane plan, no swing lane, no `targets[0]`, or no `stop` →
    excluded and counted. (Measured on this population, `STEWARD_Q015_exposure.md` §1/§6: **8 of 383**
    matured published rows carry no lane plan at all — 4 A / 3 B / 1 E, **all on the single night
    2026-06-02**; **0** rows have a swing lane without an L3 and **0** have an L3 without a stop.)
  - picks whose **L3 is at or through `X`** (`d_L3 ≤ 0`) or whose **stop is at or through `X`**
    (`d_S ≤ 0`) — an invalid plan at publication — or whose `outcome_target_invalid` is non-null →
    excluded and counted. Decided at the close, before any forward bar exists, identically in both
    bands. (Measured: 4 `outcome_target_invalid`, 2 wrong-side L3, and **66 wrong-side stop** — 9 A /
    55 B / 2 E — the binding exclusion in every band, `STEWARD_Q015_exposure.md` §1/§6.)
  - picks with missing forward bars inside t+1..t+20 (halt, delisting) → ungradeable; excluded and
    counted. This is a **measurement failure, not a classifier**: it never moves a pick between bands.
    A night is dropped if > 25% of its eligible picks are ungradeable.
  - symbols with fewer than 60 daily bars dated ≤ t (ATR / beta / run-up undefined) → excluded,
    counted.
  - nights whose session t+20 falls after the last trading date of the pinned price freeze (immature)
    → excluded and counted. Maturity comes **from the trading calendar**, never from whether a price
    exists; right-censoring is never graded as a non-touch.
- **Contributing night, per primary endpoint (the floor unit, DP-21):**
  - **P1, P2:** a night carrying **≥ 1 eligible pick in band A *and* ≥ 1 in band B** (the paired
    contrast is undefined otherwise). Nights carrying only one of the two are **non-contributing for
    P1/P2**, printed in the funnel with their band, never added to any exclusions file.
  - **P3:** a night carrying **≥ 1 eligible pick in band A**.
  A matured night on which no row survives the funnel is a **non-contributing night, not an
  exclusion** — measured, that is **2026-06-02** and only it (all 8 no-lane-plan rows fall there;
  `STEWARD_Q015_exposure.md` §1, §3). Of the 48 matured nights, 21 are paired-contributing, 26 carry
  band B only, 1 carries nothing, and 0 carry band A without band B.
- **The already-measured nights are in the window, not outside it.** Pick nights
  2026-06-01..2026-08-12 sit inside the §6 window and inside `manifest_v001`; the Steward measured them
  to fix a rate, not to seed a result (counts only, no outcome of any kind), and they enter `eval.py`
  on exactly the same footing as every later night. The window is **not re-based** on them.
  `eval.py` prints **pre-lock and post-lock contributing-night counts separately** so DP-24's clause is
  checked rather than asserted (§5).

## 3. Baseline(s) — what this must beat

- **B1 (primary): band B = 80–85, same nights, same plans, same grading** — the adjacent traded band,
  paired within night. This is "Y's rate when X did not happen, in the same regime" in its cleanest
  available form: same tape, same night, same publication process, one score step away. It replaces
  H-060's `<80` (closed by `publication_floor`, §1) and `90+` (unreachable as a primary, §5) and is
  the **stricter** contrast of the three, because the adjacent band is the most similar cohort.
- **B1′ (descriptive, demoted at lock under DP-43, and SUPPRESSED on measured counts): band E = 90+
  and band U = <80.** Measured at **14** and **1** contributing nights respectively
  (`STEWARD_Q015_exposure.md` §2, §4) — both below the 20-contributing-night floor, so both are
  **SUPPRESSED: counts only, no point estimate, not even "small n, directionally"**. The demotion is
  settled here, at lock, on measured counts and before any outcome is seen; **no arm is demoted or
  promoted after lock in either direction**, whatever the decision-pass counts turn out to be. Neither
  can produce a verdict, and no §9 rule may cite them. A properly powered 85–90 vs 90+ contrast is a
  **separate future question**, registrable when the Steward measures ≥ 0.5 elite-contributing nights
  per session over a trailing quarter (the rate at which 80 paired nights fits inside DP-43's ceiling);
  H-062's re-check-trigger pattern.
  Bands **A and B are jointly the P1/P2 contributing-night unit** and neither is separately demotable:
  a thin band A shows up as *fewer contributing nights* and is handled by §5's date machinery — which
  is precisely what pushed this question's decision date from the drafted floor to 2027-08-30.
- **B2 (rule-5 distance-matched control; descriptive, and one §8 clause):** for each eligible pick,
  the 10 nearest same-night **non-published** `sas_candidates` rows (the complement of the DP-28
  predicate) on `beta60` / `atr_pct` / `runup20` from `prices_daily_split` bars dated ≤ t, standardized
  by the night's cross-sectional median and MAD, Euclidean, with replacement across picks, ties by
  symbol ascending — the Q006 §3 construction. Each control carries a **synthetic L3 at the same ATR
  distance and direction** and a **synthetic counter level at the same ATR distance** as the pick it
  matches: `L3_c = C_c × (1 + dir_p × d_L3,p × atr_pct_c)`, `S_c = C_c × (1 − dir_p × d_S,p ×
  atr_pct_c)`, graded with exactly the §4 rules from the control's own close, same direction, same
  20-session window. Control rows **never add to inferential n** (rule 6). B2 answers "is the
  up-then-down shape a property of this band's picks, or of stocks with these levels at these
  distances", and the **control-adjusted band contrast** carries one §8 clause, **binding on P1 and P2
  only**: if it is beyond MPE in the *opposite* sign to the primary, that endpoint is INCONCLUSIVE.
  This is how the distance confound (§10 threat 1) is prevented from manufacturing a band effect. P3 is
  a within-pick two-plan difference inside band A with no band contrast to confound, so the
  opposite-sign clause does not transfer with a sensible meaning; P3's control version is printed as a
  descriptive panel and **never decides** (DECISIONS.md item 17).
  **The pool is measured and never thin:** median 54 valid same-night non-published rows, p10 42,
  minimum 37 on any contributing night, and **0.0%** of eligible picks in any band with < 3 or < 10
  valid controls (`STEWARD_Q015_exposure.md` §8). Separately, **206 of 428 unpublished candidate
  symbols (48.1%) carry no hourly bars anywhere in the freeze** (§7 of the same report), so controls
  drawn from them fall to DP-27's counter-first ordering **by construction, not by a thin sample** —
  disclosed, applied identically, never patched (§4 ordering rule 1; §10 threat 14).
- **B3 (the money baseline, inside P2/P3 by construction):** the **same picks held through** — Plan H
  in §4. Two plans, same picks, one tape, paired.

## 4. Objective metric (rule 5 — price path, measured the way it is traded)

**Entry (DECIDED, DECISIONS.md item 3; DP-11, DP-03(a), DP-42).** `X = C_t`, the pick-night
regular-session close from `prices_daily_split` (never `spot_close`), the DP-03(a) after-hours
proxy in DP-11's construction and the basis Q007 and Q009 use — rule 5 requires **one basis on both
sides** and only the close exists on the distance-matched control side, which is what settles it.
`C_t` is also the ATR, `d_L3`, `d_S`, beta60 and runup20 reference. The **next-session-open
basis (DP-03(b)) is computed and printed for every endpoint as a named sensitivity**, and a pick whose
L3 was already through at that basis is not-takeable there (rule 5), never a hit.

**Grading window:** sessions t+1..t+20 (the 40-session companion is descriptive, matured nights only,
DP-09). Regular-session bars only.

**The two events, per pick:**
- **UP** — the first session `s_up ∈ [t+1, t+20]` on which the regular-session high (bullish) / low
  (bearish) touches `L3`.
- **DOWN-after** — a session `s_dn ∈ [s_up, t+20]` on which the regular-session low (bullish) / high
  (bearish) touches `S`, **at or after `s_up`**, with same-session pairs ordered by
  `prices_hourly_raw`.
- **UPDOWN = 1** iff both exist. Otherwise 0.

**Ordering rules, stated once, applied by `eval.py` with no judgment:**
1. **Same-session L3 and S.** Ordered from `prices_hourly_raw` on the published symbol, converted to
   the signal-date split basis (`eval.py` asserts basis agreement per symbol-date and fails loudly).
   If one hourly bar holds both, or the symbol has no hourly bars, the pair counts **counter-first**
   — **DP-27**, which here is also the reading **less** favourable to the hypothesis (a counter touch
   that cannot be shown to follow the L3 touch does not make an UPDOWN). Applied identically in both
   bands and in B2, so the convention cannot create the contrast. The count of picks resolved by this
   rule is printed **per band**, and the opposite reading is printed as a named sensitivity that
   **never decides**. Measured: hourly-bar coverage on sessions t+1..t+20 is **100.0%** for all 303
   eligible picks, in every band and every month (`STEWARD_Q015_exposure.md` §7), so no DP-27 fallback
   is forced on the picks side by a missing bar; on the control side **48.1% of unpublished candidate
   symbols have no hourly bars at all**, so B2 falls to counter-first by construction (§3 B2, §10
   threat 14).
2. **A counter touch strictly before `s_up`** does not score UPDOWN by itself; the pick scores UPDOWN
   only if `S` is touched again at or after `s_up`. The "counter first, then L3" ordering — Q009's
   whipsaw shape — is printed separately (§7 non-independence).
3. **A gap through a level is a touch** at that level for measurement, and a gap through `L3` at the
   session open is an exit at the open price for Plan T (below) — the better fill a resting exit limit
   would have got.

**The two plans (both enter at `X`; neither uses a stop — rule 5, DP-02):**
- **Plan T (exit at the touch, the tested rule):** exit the whole position at the first touch of `L3`
  within t+1..t+20, at the `L3` price or at the session's open where the session opens through it;
  if `L3` is never touched, exit at the session t+20 close.
- **Plan H (hold through, the baseline):** exit at the session t+20 close, whatever happened in
  between.
- `r_plan = dir × (exit − X) / ATR`. `Δr_p = r_{T,p} − r_{H,p}`, which is **0 for every pick that
  never touched L3** — that is the honest per-published-pick denominator and it is never rescaled to
  a per-toucher basis (that would divide a diluted mean by a smaller number and lower the bar).

**Primary endpoints (three, pre-specified, BH-corrected within the question and across the family —
§7).** For night t, `mean_A[·]` = the mean over band-A eligible picks on that night, `mean_B[·]`
likewise:

- **P1 — the shape (band contrast, touch-rate units).**
  `Δ1_t = mean_A[UPDOWN] − mean_B[UPDOWN]`; estimand `m1 = mean_t Δ1_t`, in percentage points, over
  P1/P2 contributing nights.
- **P2 — the money (band contrast, ATR units).**
  `Δ2_t = mean_A[Δr] − mean_B[Δr]`; estimand `m2 = mean_t Δ2_t`, in ATR per published pick.
- **P3 — the money in band A (ATR units).**
  `Δ3_t = mean_A[Δr]`; estimand `m3 = mean_t Δ3_t`, in ATR per published pick, over P3 contributing
  nights. **P3 is the endpoint that licenses an exit rule** (§9); P1 is the mechanism and P2 is what
  makes the rule band-specific.

**Pre-specified decomposition, printed with every P1 figure (descriptive):**
`UPDOWN rate = P(touch L3 within 20) × P(revisit S at or after the touch | touched)`, per band, with
each factor's own CI, plus the fraction of the band's picks that touched L3 and were **back beyond
`S`** versus merely **back below `L3`** at session t+20 (the settle-back shape Q006 reports).
The conditional factor is labelled *"conditions on a post-entry path event; descriptive, does not
decide"*.

**Secondary, descriptive, never decides:**
- the same three endpoints on the **next-open entry basis**, with the not-takeable count printed;
- the same three endpoints with the counter level taken as the **desk-standard −1.0 ATR line**
  `X − dir × 1.0 × ATR` (Q004/Q011's registered adverse line), which is distance-matched across bands
  by construction — the direct read on §10 threat 1;
- the **40-session** companion of every endpoint (the platform's own swing window, DP-09), matured
  nights only;
- **B2** (matched controls under the identical rules) and the **control-adjusted** versions of P1 and
  P2 (which carry the §8 clause);
- the **committed scale-out** for each pick's own band (`BAND_EXITS`, volatilx
  `scripts/generate_sas_trading_guide.py:89-95`: 85–88 `[0,15,30,15,25,15]`, 88–90
  `[0,10,25,15,30,20]`, 80–85 `[10,15,30,15,20,10]`) run from `X` — each fraction exits at its level's
  first touch, fractions whose level was at or through `X` are recorded unfillable and excluded from
  that fraction, the remainder closes at the t+20 close (truncated and labelled; the trailing rules
  are not deterministic enough to simulate and are ignored) — reported beside Plan T and Plan H, since
  rule 5 requires the named execution plan's realized result;
- sessions from entry to `s_up` and from `s_up` to `s_dn`; maximum favourable and maximum adverse
  excursion in ATR from `X`; counter-direction touches beyond `S` (reported, never an exit — DP-02);
- sub-cells: **85–88 / 88–90**, bull / bear, `atr_pct` tercile, `d_L3` tercile, `d_S` tercile, tape
  stratum, regime label — reported only at ≥ 20 contributing nights;
- a **band-matched sensitivity**: band-A picks matched 1:1 to band-B picks on `beta60` / `atr_pct` /
  `runup20` within night, P1 and P2 recomputed — the read on §10 threat 6;
- close-to-close return from `X` at T+5 and T+20 — **fixed-horizon return is secondary and descriptive
  by rule 5 and never decides**.

**Quotability:** 20-session (and 40-session) bases → **every number here is NON_QUOTABLE** (rule 12).

**Inference.** Night-level. **CI (decides):** stationary block bootstrap over the ordered contributing
nights, expected block length **10 sessions** (20-session forward windows overlap across adjacent
nights; Q004/Q007/Q009/Q011 use the same), 2,000 resamples; the date-clustered bootstrap CI is printed
alongside. **p-value:** permutation on the night contrasts — paired sign-flip for `Δ1_t`, `Δ2_t`,
`Δ3_t` (the arms are two plans and two bands on the same nights), 10,000 permutations, seed 20260913;
for P1/P2 a **within-night band-label shuffle** across the night's eligible picks is printed as a
second p-value. Every estimate prints n(contributing nights, per endpoint), n(contributing nights
dated after the lock commit), n(eligible picks per band), n(touched L3), n(UPDOWN), n(resolved by
ordering rule 1), n(control rows), n(excluded, by reason).

## 5. Sample floors and expected n

- **Floors (rule 6 as read by DP-21):** ≥ **80 contributing nights per primary endpoint** (P1/P2 on
  the paired definition, P3 on the band-A definition — §2) and ≥ **20 contributing nights per reported
  sub-cell**. A sub-cell below 20 is **SUPPRESSED** — no point estimate, not even "small n,
  directionally", counts only — and a SUPPRESSED sub-cell does **not by itself** make its endpoint
  INCONCLUSIVE (§8 clause 1). The weaker reading of rule 6 is not used. **No floor is ever lowered to
  hit a date.**
- **Binding maturity: 20 sessions** (DP-09).
- **Measured exposure (`research/reports/STEWARD_Q015_exposure.md`, 2026-09-13; counts only, no
  outcome of any kind — no touch, no UPDOWN, no revisit, no return, no plan result, no band
  difference).** On pick nights 2026-06-01..2026-08-12 (the last matured night on the pinned freeze):
  **48 matured nights, 383 published picks → 303 eligible** after the §2 funnel (8 no swing lane, all
  on 2026-06-02; 0 null-L3; 0 null-stop; 4 `outcome_target_invalid`; 2 wrong-side L3; **66 wrong-side
  stop**; 0 missing `C_t`; 0 ungradeable). **Band A 38 picks / 21 nights; band B 249 / 47; band E 15 /
  14; band U 1 / 1.** **P1/P2 paired contributing nights = 21** and **P3 band-A contributing nights =
  21** — the identical set, because `nights_A ⊂ nights_B` in this window (26 of the 48 matured nights
  carry band B only; 2026-06-02 carries nothing and is non-contributing, not an exclusion). Sub-bands
  **85–88 = 26 picks / 18 nights**, **88–90 = 12 / 9**. Hourly-bar coverage t+1..t+20 is **100.0%** for
  the picks; the B2 pool is **never thin** (median 54, p10 42, minimum 37; 0.0% of picks with < 3 or
  < 10 valid controls). Measured rate: **21 / 51 = 0.4118 paired-contributing nights per session,
  declining month over month** — June 0.476, July 0.409, partial August 0.250.
  Two other figures stay in the record with their existing labels and **gate nothing**: the 2026-09-12
  weekly's band counts and `STEWARD_Q011_exposure.md`'s rate are a mechanical projection for a
  different funnel, and EXPLORE_001's April–May figures are in-sample, outside the window, and not a
  projection.
- **Which rate the schedule uses, and why the slowest.** The three measured rates project the binding
  Floor-1 decision date at **2027-04-19** (flat 0.4118), **2027-05-10** (Jul+Aug 0.3667) and
  **2027-08-30** (partial August 0.2500). The desk takes the **slowest**, because the rate is *measured
  to be declining month over month, not flat*, and because DP-43/DP-45 forbid choosing the rate that
  reaches a date sooner: the cost of the slow rate is waiting, and the cost of the fast one is a short
  window, a fired extension and a DEFERRED question. **The window is never shortened to reach a date.**
- **Window, decision date, extension and DEFERRED fallback (DP-43; DP-13; no outcome looks at any
  point):**
  - **Primary window: pick nights 2026-06-01..2027-07-20 inclusive**, after exclusions (in-window
    those remove 2026-06-26, 2026-07-02, 2026-07-06). The end is where the **slowest measured rate**
    projects the 80th contributing night, not where a date would be convenient. A shorter window that
    reached a date sooner was rejected (DP-43, DP-45).
  - **Decision date: Monday 2027-08-30.** The arithmetic, printed so it can be checked: 59 contributing
    nights are needed beyond the 21 measured; at **0.2500/session** that is **236 sessions**, putting
    the 80th contributing night at **2027-07-20** (the window end); **+ 20 sessions maturity** (DP-09)
    = 2027-08-17 on the trading calendar (2027-08-18 on the Steward's mechanical 365/252 conversion —
    the two agree to one session and to the same Monday); **+ one week freeze margin** = 2027-08-24;
    first Monday on or after = **2027-08-30**. This is **11.5 months from the 2026-09-13 lock** — 7½
    months **out** from the drafted floor of Monday 2027-01-18, and R1 could only push it out, never in
    (DP-43, DP-45; Q011 item 8). The Steward fixes the exact session-count date when building the
    successor freezes. `eval.py` is written once (rule 9) and run **once**, then. **No interim looks.**
  - **DP-43's 12-month ceiling is cleared, so Q015 locks.** 2027-08-30 falls **14 days inside**
    2027-09-13, under the most pessimistic of the three measured rates (it clears by ~5 and ~4 months
    under the other two), so the conditional DEFERRED branch does not fire and no `DEFERRED.md` entry
    is written for H-060. Had the projection landed past the ceiling, the question would have gone to
    DEFERRED rather than the ceiling being stretched (H-062 precedent).
  - **Both gates, per primary endpoint, on measured counts.** Evaluation proceeds only if **every**
    primary endpoint has **≥ 80 contributing nights** on its own definition (P1/P2 paired, P3 band-A)
    and **≥ 30 contributing nights dated after this file's lock commit** (DP-24), printed by `eval.py`
    from the frozen data. A shortfall on one endpoint is never covered by another's count. **Gates fire
    on `eval.py`'s measured counts at the decision pass, never on R1, on this projection or on a
    run-rate.**
  - **Floor 3 is not the binding gate and arrives with margin.** At the same 0.2500/session rate, 30
    contributing nights dated after the lock commit are reached by **2027-04-12** — about 4½ months
    before the decision date — and Floor 1 (80 total) is later than Floor 3 under all three measured
    rates. The 21 contributing nights measured so far are all **pre-lock** (2026-06-01..2026-08-12,
    lock 2026-09-13), which is why `eval.py` prints pre-lock and post-lock counts separately (§2).
    **DP-24 is not reduced and DP-31 is not invoked:** PROSPECTIVELY_CONFIRMED is reachable from this
    run by design, the verdict is not `HISTORICAL_ONLY`, and no successor replication question is
    needed.
  - **One automatic extension (DP-13; DP-43's +30 sessions).** If any gate is short at 2027-08-30 on
    `eval.py`'s measured counts, the window extends **once**, automatically and with no new question,
    to pick nights **2026-06-01..2027-08-31**, decision date **Monday 2027-10-11** (2027-08-31 + 20
    sessions = 2027-09-29 with 2027-09-06 Labor Day closed; + one week = 2027-10-06; first Monday on or
    after). The extended run uses the **byte-identical, unmodified `eval.py`** and the same gates. That
    extension date falls **after** the 12-month ceiling date: DP-43's ceiling tests the **initial**
    decision date, and DP-13's single extension is agreed here at lock, so it stands.
  - **DEFERRED fallback.** If a gate is still short after that single extension, Q015 goes to
    **DEFERRED** (`research/questions/DEFERRED.md`, with the measured counts) rather than running
    under-powered. There is no second extension, no reduced floor, and a gate shortfall is **not** an
    INCONCLUSIVE verdict (§8).
  - **Arms demoted at lock (DP-43), not after:** band **E (90+)** at 14 contributing nights and band
    **U (<80)** at 1 are descriptive from lock and **SUPPRESSED** — measured (§1, §3), not guessed, and
    settled before any outcome is seen. **No arm is demoted or promoted after lock in either
    direction**, and a thin cell at the decision pass is handled where it belongs: as a SUPPRESSED
    sub-cell (§8 clause 1), never by moving a primary to descriptive. Bands A and B are jointly the
    P1/P2 unit and are not separately demotable; 85–88 and 88–90 are sub-cells, not arms.
- **Freeze discipline (DP-23; routed request R2 — due at the decision date Monday 2027-08-30, covering
  pick nights after 2026-09-10 through the registered window end 2027-07-20; not a blocker for lock).**
  Nights ≤ 2026-09-10 stay pinned to `manifest_v001` / `manifest_prices_v001`. Later nights enter only
  through successor freezes — `manifest_v002` (selections, same SQL, same exclusion criterion) and
  `manifest_prices_v002` (same Alpaca queries), with the daily symbol list extended to **every
  candidate on the new nights, published and unpublished** (B2 needs the unpublished symbols'
  pick-night closes, prior bars for beta60 / atr_pct / runup20, and forward bars),
  **plus hourly bars for published symbols** (ordering rule 1), carrying **20**
  forward sessions beyond the last included pick night (40 where the descriptive companion is
  computed). A second pair is built **only if** the DP-13 extension fires. `eval.py` takes the window
  start and end, the manifest paths, the exclusions-file path and the output directory as inputs —
  **no hard-coded dates, manifest names or paths** — so the byte-identical script serves both runs. It
  records every sha256 and prints pre-lock and post-lock night counts separately.

## 6. Test window, split and stratification

- **Test window: sealed + prospective only — pick nights ≥ 2026-06-01** through the §5 window end.
  *Justification:* H-060 comes from EXPLORE_001, which ran on April–May in-sample nights and quotes
  their counts (44 picks / 28 nights in 85–90), so those nights are contaminated for this question and
  are not used, not even as a descriptive panel. The window also sits entirely after the 2026-06-01
  catalyst fix (DP-06; `exclusions_v003.json` `catalyst_layer_regime_change`; platform commit
  `69ef05f`).
  *Contamination check on the sealed period (registrar; no results directory was read):* the desk's
  sealed-period descriptive outputs recorded in `research/BACKLOG.md` and the weekly reports show
  **band-level T+20 returns and L1/L2 touch rates for the pooled 80–90 band** (weekly 2026-09-12 §2,
  §3; Jun–Aug 80–90 −1.23%), the 90+ trend, and regime × band cells. Two things matter here and both
  cut the right way: (i) **the 85–90 band has never been shown on its own** — the weekly's own rule is
  that "the 88–90 range is folded into 80–90 and never shown on its own" (weekly 2026-09-12 §2), so
  no A-versus-B figure has been seen by anyone on the desk; (ii) **no counter-level revisit, give-back
  or exit-at-touch statistic exists anywhere in the sealed outputs** — the nearest neighbours are
  Q009's stop-then-target *exposure counts* (stop-distance buckets, no outcome) and Q006's registered
  touch-then-settle secondary, which has not been run. The band edges are H-060's own (DP-25), the
  level is the platform's, the counter level is the platform's printed stop, and the 20-session clock
  is DP-09; none was chosen after seeing a number.
- **Split for "holds in both halves":** Half A = contributing nights on or before the median
  contributing-night date (re-derived per endpoint from the final window at the decision pass);
  Half B = after. `in_sample_end = 2026-05-29` marks only what is excluded.
- **Regime / tape stratification (rule 7):**
  - `market_regime_daily` has **no point-in-time label before 2026-06-09** (FREEZE_v001 §7;
    `exclusions_v003.json` `regime_label_point_in_time_from`). It is used only for nights ≥ 2026-06-09,
    only `regime_version = 'v1.2'`, and only where the row is a same-evening write per its declared
    availability; a later-posted row is treated as missing. Nights 2026-06-01..06-08 carry no legal
    label and are stratified by the SPY proxy only, flagged.
  - Primary tape stratum for every night, trailing and legal at 16:05 ET: `tape_t` = sign of SPY's
    trailing 20-session return × tercile of SPY's trailing 20-session realized volatility, from SPY
    bars dated ≤ t in `prices_daily_split`. **Tercile cut points are expanding-window** (for night t,
    from every session 2026-03-02..t), so no later night's data sets an earlier night's stratum. Cells
    < 20 contributing nights SUPPRESSED.
  - The report describes the tape in words from SPY's path and never implies a regime label existed
    before 06-09.
- **Knowledge time (rule 14) — every input declared. Q015 needs no rule-14 exception and requests
  none** (DP-05 untouched; DP-41 respected): the band, the direction, the level, the counter level, the
  ATR and both plans are fully specified at 16:05 ET on the pick night, every eligible pick is in the
  denominator of its band from the close, and **no post-entry quantity classifies, filters, matches or
  stratifies any pick**. The one construction that would — the revisit rate *conditional* on having
  touched L3 — is descriptive and never decides (§1, §4).

  | input | source | available | use |
  |---|---|---|---|
  | `qualified`, `selected_rank`, `overall_score`, `dominant_direction`, `best_timeframe` | `sas_candidates` | pick night, 16:05 ET (FREEZE_v001 §7) | population, **band**, direction |
  | swing lane plan: **L3** (`targets[0]`) and **stop** | `sas_candidates.public_payload_json.lane_plans` | written during the nightly run before `finished_at` (volatilx `services/super_agent_select_service.py:155-161`) | target level, counter level |
  | `outcome_target_invalid`, `score_details_json` | `sas_candidates` | publication | exclusion audit; band-integrity check (§10.12) |
  | control-candidate pool (non-published rows for night t) | `sas_candidates` | pick night, 16:05 ET | B2 pool (descriptive) |
  | `C_t` (entry and ATR denominator), ATR14, beta60, runup20, `d_L3`, `d_S` | `prices_daily_split`, bars ≤ t | pick-night close, 16:00 ET | entry, distances, matching |
  | SPY tape (trailing return, trailing vol, expanding terciles) | `prices_daily_split`, SPY bars ≤ t | pick-night close | stratum |
  | regime label (v1.2, nights ≥ 2026-06-09, same-evening rows only) | `market_regime_daily` | pick night, 16:05 ET | stratum |
  | `finished_at` | `sas_runs` | publication time | DP-04 exclusion |
  | sessions t+1..t+20 (t+40 companion) daily bars; hourly bars for same-session ordering | `prices_daily_split`, `prices_hourly_raw` | after the pick night | **outcome measurement only** |

  **What `eval.py` must enforce:** the eligible-pick set, both plans' parameters (`L3`, `S`, `ATR`,
  direction, `X`), the band label and every stratum label are computed and written to a frozen per-pick
  table **before any post-pick-night bar is loaded**; the run fails if any t+1-or-later field is
  referenced in eligibility, band assignment, matching or stratification.
  `sas_selection_excursion` / `outcome_*` / `level_hit_*` columns are never inputs (calendar windows,
  close basis, recomputed weeks later, v1/v2 duplication — volatilx `services/sas_excursion.py:8-18`,
  `:336-354`; DATA_NOTES). `uoa_symbol_daily.fwd_return_*` is **banned** (FREEZE_v001 §5); no UOA table
  is used.

## 7. Multiple testing

- **Within the question:** **BH across m = 3** — P1, P2, P3 — at q ≤ 0.10; the verdict uses q. **`m = 3`
  is fixed at lock.** All three carry verdicts in every branch (the demoted arms are descriptive from
  lock, so there is no path on which m falls and no bar is lowered for any endpoint); an endpoint short
  of floor still has its p computed, so m never falls that way either. Every secondary, including the
  conditional revisit rate, the −1 ATR counter-level version, the next-open basis and the committed
  scale-out, prints raw p only, marked "descriptive, does not decide".
- **Across the family: F7 Path, entry timing & volatility.** F7 holds **9 hypotheses** —
  H-053…H-060 and H-065; **H-066 was re-filed to F6** under DP-29 with Q012 and is not counted in both.
  Of the nine, **H-053 is merged into Q006** and **H-055 is DEFERRED**, so neither contributes a
  primary to F7's correction. **The F7 correction set is computed at the decision pass on the questions
  locked by then:** Q002 (H-065, 3) + Q004 (H-054 + H-057, 2) + Q011 (H-058, 4) + **Q015 (H-060, 3)**
  **+ Q012's 3 F7-companion primaries where Q012 has locked** = **15**. H-060 is counted **once**, in
  F7.
- **F6 companion correction (strictness, not a re-filing).** P2 and P3 contrast two exit plans on the
  same picks, which is F6's subject and the ground on which Q009 and Q012 were re-filed under DP-29.
  Rather than argue the filing, the Reporter computes BH for P2 and P3 **also** across F6's registered
  primaries, and **q ≤ 0.10 is required in both families** for either to count as CONFIRMED; **the
  larger q is the one quoted**. **The F6 companion set, computed at the decision pass:** Q009 (2) +
  Q012 (3) + **these 2** = **7**; **Q010 is excluded** as the same hypothesis's prospective replication,
  not a second F6 question. Companion-corrected primaries count in **both** directions — the same
  arithmetic Q012 commits to, and the stricter one. P1 is corrected in F7 only.
- **Overlaps, stated so nothing is double-counted as independent evidence:**
  - **Q012 (H-066, drafted in the same autonomous cycle):** its P2 is a band gradient (85–90 vs 80–85)
    on a *recycle* plan (exit at the first L1/L2 touch, 5-session cap, 60-session capital budget)
    against the committed scale-out. Q015's P2/P3 use a different level (L3), a different clock (20
    sessions) and a different alternative (hold to t+20). The two are **adjacent readings of one idea —
    that lower-conviction picks should be exited earlier — and must never be presented or counted as
    two confirmations**; the Reporter cross-references. **No endpoint is identical**, so **`m = 3` is
    fixed at lock and no primary is dropped afterwards**: dropping a primary after lock would lower the
    BH bar for the survivors, which no rule permits.
  - **Q009 / Q010 (F6):** the same two lines (L3 and the printed swing stop) in the **opposite order**
    (stop first, then target). The "counter first, then L3" count is printed here so the two shapes can
    be read together; the questions are not merged and are not independent.
  - **Q006 (F1):** owns the L3 touch rate against the matched control and reports touch-then-settle
    descriptively; Q015's L3-touch rate by band is a decomposition factor, not a second test of Q006's
    endpoint.
  - **Q002 (F7):** owns speed to target. Sessions-to-touch is descriptive here (DP-44).
- Threshold: **q ≤ 0.10**.

## 8. Decision rule (numeric, written before unsealing)

`m1` in percentage points of UPDOWN rate (band A minus band B, paired within night); `m2` in ATR per
published pick (band A minus band B, of exit-at-touch minus hold); `m3` in ATR per published pick
(band A, exit-at-touch minus hold).

**MPE: P1 +5.0 pp** (DP-20, DP-44 — the standing number for a touch-rate endpoint; it is a within-night
paired contrast on one tape, the Q011 structure, so no uplift is proposed). **P2 and P3 0.25 ATR**
(DP-10, DP-44 — the standing number for every per-trade ATR-denominated endpoint), measured **per
published pick in the band, never rescaled to a per-toucher basis**. All three are two-sided: H-060
predicts `m1 > 0`, `m2 > 0`, `m3 > 0`, and a result beyond MPE with the opposite sign is a confirmed
finding with the opposite sign.

Per endpoint (two-sided; the verdict carries its sign):

- **HISTORICALLY_CONFIRMED** requires **all** of:
  1. **contributing nights ≥ 80** on that endpoint's own definition **and ≥ 30 contributing nights
     dated after the lock commit**, **and ≥ 20 contributing nights for any sub-cell that is reported**
     (DP-21) — a sub-cell below floor is **SUPPRESSED** (counts only) and does **not by itself** make
     the endpoint INCONCLUSIVE; the stratification protection rule 7 requires lives in clauses 5–7;
  2. `|m| > MPE` (5.0 pp for P1; 0.25 ATR for P2 and P3);
  3. block-bootstrap 95% CI excludes 0;
  4. BH q ≤ 0.10 within the question (m = 3) **and** within F7 — and, for P2 and P3, also within F6
     (§7);
  5. the point estimate has the **same sign in both halves**, and neither half is beyond MPE in the
     opposite sign;
  6. no tape stratum with ≥ 20 contributing nights is beyond MPE in the opposite sign;
  7. **for P1 and P2 only:** the **control-adjusted** version (B2) is not beyond MPE in the opposite
     sign — the distance-confound clause (§3 B2, §10 threat 1).
- **NULL:** floors met **and** 95% CI includes 0 **and** `|m| < MPE`. "The 85–90 band gives its L3
  touch back no more often than the band below it" is a real finding and is ledgered with the same
  care.
- **INCONCLUSIVE:** anything else — halves disagreeing in sign, a tape stratum or the control-adjusted
  version beyond MPE in the opposite sign, `0 < |m| ≤ MPE` with the CI excluding 0 ("real but below
  MPE", rule 6), or CI including 0 with `|m| ≥ MPE`. **A SUPPRESSED sub-cell is not by itself
  INCONCLUSIVE**; what bites is a *reported* sub-cell below floor, which must not happen. **A gate
  shortfall is not INCONCLUSIVE either**: it fires the single DP-13 extension, then DEFERRED (§5).
- **What licenses a rule.** A band-specific exit rule requires **P3 CONFIRMED positive** (exiting at
  the touch is worth more than 0.25 ATR per published pick in band A) **and P2 CONFIRMED positive**
  (it is worth materially more there than in band B). **P1 alone never licenses a rule**: it says the
  shape happens more often, not that acting on it pays. **P3 CONFIRMED with P2 NULL** licenses no
  *band* rule — it says "exit at the L3 touch pays across 80–90", which is a bigger claim than H-060
  and must be registered as its own question before anything ships (§9).
- **What a confirmed P1 does and does not mean (binding on the report).** A CONFIRMED-positive P1
  means **"a larger share of band-A picks touched L3 and then traded back to the printed swing stop
  inside 20 sessions than band-B picks did"**. It does **not** establish that band-A picks are more
  prone to give back *what they get*: that is the conditional factor in the §4 decomposition, which
  carries no verdict. Any sentence of the "this band hands it back" kind must quote the conditional
  factor and label it descriptive.
- **PROSPECTIVELY_CONFIRMED:** reachable from this run by design (§5) — it requires **≥ 30
  contributing nights dated after this file's lock commit** (DP-24, DP-21), frozen in the successor
  manifests and never inspected earlier, reproducing the sign of the confirming endpoint under the
  unmodified `eval.py`. The clause does not weaken: if the window cannot supply 30, the DP-13 extension
  fires and then DEFERRED — the 30 is never reduced. No subscriber-facing statement before that
  (rule 10); even then the basis is NON_QUOTABLE until restated on W60 (rule 12).

## 9. If CONFIRMED, what changes on the platform

Today the platform's committed scale-out already assumes most of a sub-90 position rides **past** L3:
`BAND_EXITS` (volatilx `scripts/generate_sas_trading_guide.py:89-95`) leaves 55% of an 85–88 position
and 65% of an 88–90 position on after the L3 fraction, with the trail tightened only after L4, and the
2026-07-08 L4-trim ruling moved weight *to* L3 without ever measuring what happens to the rest
(`docs/SAS_EXIT_SCHEDULE_L4TRIM_RULING.md`; the conviction card notes the premise was measured on the
old calendar windows — `services/sas_conviction_card.py:203-218`). Nothing on the platform measures
give-back after a target touch, and nothing varies the exit by the 85–90 band.

Rules below fire only where §8 licenses one, and only after PROSPECTIVELY_CONFIRMED for anything
subscriber-facing (rule 10):

- **P3 and P2 CONFIRMED positive:** a Manual Trading Guide line and a **flag-off** `BAND_EXITS` change
  for the 85–88 and 88–90 rows — weight the scale-out to a full or near-full exit at L3 — printed with
  the measured ATR gain per published pick, the measured UPDOWN rate and the L3-touch rate beside it,
  and with the 80–85 figure shown so the band-specificity is visible. Brief: an `INTERNAL_TOOL`
  flag-off card field showing the band's measured give-back rate on the pick card.
- **P3 and P2 CONFIRMED negative:** the opposite line — the 85–90 band is the one to *hold* through
  L3 — with the same numbers published together.
- **P1 CONFIRMED with P2/P3 NULL:** a descriptive card line ("N% of 85–90 picks that reach L3 trade
  back to the swing stop inside 20 sessions, against M% for 80–85"), and **no exit change**: the shape
  is real, acting on it is not worth 0.25 ATR.
- **P3 CONFIRMED with P2 NULL:** no band rule ships. The finding — "exit at the L3 touch pays across
  80–90" — is ledgered and registered as its own question, because a rule for the whole traded
  population is a bigger change than H-060 asked for and would collide with Q012's capital-recycling
  endpoints (§7).
- **The demoted arms license nothing.** No guide line, brief, flag or quoted number may cite the 90+ or
  <80 cells from this question (§3 B1′), whatever they show.
- **All three NULL:** no exit change; the committed schedule stands as a strategist ruling, the guide
  records that the 85–90 band's give-back is not distinguishable from the band below it, and F7 effort
  moves to H-059 and to the 85–90 vs 90+ contrast when elite exposure recovers (§3 B1′).
- Owner: implementer. Ship flag-off with a byte-identical checksum on the old path; shadow ≥ 20 trading
  days before any flip (rule 11).

## 10. Known threats to validity (registrar's own list)

1. **A band contrast is partly a distance contrast.** Ladder prices are LLM-written from projection
   levels with no ATR scaling (volatilx `ai_agents/principal_agent.py:530-575`), and printed stops
   likewise, so `d_L3` and `d_S` may differ systematically between bands — a band with nearer targets
   and nearer stops will score more UPDOWN for arithmetic reasons. Mitigations, all pre-specified: the
   `d_L3` and `d_S` tercile cells; the **−1 ATR counter-level** version (distance-matched by
   construction); the **B2 control-adjusted** contrast, which strips both distances and carries §8
   clause 7; and the per-band distance distributions printed in the results header.
2. **UPDOWN is a conjunction.** A band that simply touches L3 more often scores more UPDOWN without
   being more prone to give back. The §4 decomposition is mandatory and §8 binds what a confirmed P1
   may be said to mean.
3. **The counter level is the printed stop, which the platform itself treats as a *fallback* for the
   report's counter targets** (volatilx `services/sas_excursion.py:303-328`: `report_targets` when the
   analysis-report blob carries `sell_setup.targets`, `synthetic_stops` otherwise). The desk's freeze
   holds `lane_plans` but not the report blobs (`analysis_report_path` is a path, not content), so the
   true `swing_c1` is unavailable here — it is not in any freeze, which is what settled DECISIONS.md
   item 2. The −1 ATR version is printed beside every primary for exactly this reason, and any §9 line
   must say the level is the printed stop.
4. **Exit-at-touch caps upside by construction.** In a trending tape Plan T loses to Plan H whenever
   L3 is not the end of the move, so P2/P3 partly measure the tape. The whole window is Jun 2026 –
   Jul 2027 (Aug 2027 if the DP-13 extension fires); §8 clauses 5 and 6 (halves, tape strata) are the
   only protection, and nothing here speaks to the strong April–May tape.
5. **Band edges are arbitrary and the interesting half may be narrower.** H-060's 85–90 is kept as
   written (DP-25); the 85–88 and 88–90 sub-cells are printed where they clear 20 nights, and a
   sub-cell result never upgrades a NULL primary.
6. **Bands are not randomly assigned.** Score correlates with sector, ATR%, momentum and how extended
   the name already is — H-060's own proposed mechanism. The band-matched sensitivity (§4) and the
   post-match standardized mean differences are printed; the primary keeps the raw band contrast,
   because matching away the very features that produce the score would test something else.
7. **The `<80` baseline H-060 names is gone by configuration and the `90+` baseline is unreachable**
   (§1, §3). The registered contrast is therefore weaker than the one proposed: 80–85 is one step from
   85–90, so a true monotone effect will look smaller here than against `<80`. This raises the risk of
   a **false NULL**, which is the acceptable direction of error; it is stated so no reader treats a
   NULL here as evidence against the wider band claim.
8. **Overlapping 20-session windows** inflate precision; the block length is fixed here (10 sessions)
   and not chosen after seeing results.
9. **Same-session ordering depends on hourly bars, and the asymmetry is now measured.**
   `manifest_prices_v001` carries hourly bars for published-pick symbols only (227 symbols).
   `STEWARD_Q015_exposure.md` §7 measures **100.0% coverage of t+1..t+20 symbol-sessions for all 303
   eligible picks**, in every band and month — so no ordering failure is forced on the picks side —
   while **206 of 428 unpublished candidate symbols (48.1%) have no hourly bars anywhere in the
   freeze**, so B2 controls fall to DP-27's counter-first reading **by construction**. Where bars
   cannot order the pair, that reading applies identically in both bands, and the counts and the
   opposite reading are printed as a sensitivity that never decides.
10. **Null-ladder, null-stop and wrong-side denominators.** All excluded and counted; the question
    speaks only for published picks carrying a swing L3 and a swing stop on the correct sides of the
    pick-night close. The 8 no-lane-plan rows measured in the sealed window all fall on one night
    (2026-06-02), which is therefore non-contributing, not excluded.
11. **No stops are assumed.** The counter level is a measured line, never an exit (rule 5, DP-02);
    both plans hold through it. A reader who does stop out would see different money, and §9 must say
    so.
12. **Band membership depends on a stored score that has been rewritten before.** The in-sample
    catalyst rescore (`scripts/rescore_sas_earnings_corrected.py`) and the E9a correction batch show
    that `sas_candidates` rows are not immutable. The window is entirely post-fix, and the KT audit's
    re-run nights plus 2026-06-26 are excluded, but `eval.py` additionally re-derives each pick's band
    from `score_details_json` where the layer subscores are present and **fails loudly** on a
    disagreement with `overall_score` beyond 0.05, rather than silently trusting the column.
13. **Elite is thin and shrinking and `<80` is effectively empty — now measured, not asserted.** Band E
    carries 15 eligible picks on 14 of 48 matured nights (10 June / 4 July / 0 in matured August) and
    band U carries 1 pick on 1 night (`STEWARD_Q015_exposure.md` §2, §4, §9). Both are **SUPPRESSED**:
    they print counts only. Any report sentence that reaches for them is out of bounds (§9).
14. **Matching on 3 features may not span selection** (Q006 threat 1). B2 is descriptive here except
    for §8 clause 7 (P1 and P2 only), and post-match standardized mean differences are printed. The
    pool itself never binds — median 54 rows, minimum 37, 0.0% of picks under 3 or 10 valid controls
    (`STEWARD_Q015_exposure.md` §8) — but its hourly-bar gap (threat 9) means the control side's
    same-session ordering is systematically counter-first while the picks' is not; that asymmetry is
    disclosed and reported, never patched.

---

## Decisions before lock
Recorded in DECISIONS.md (2026-09-13). Routed items still open: **R2 only** — the successor selection
and price freezes (DP-23), due at the decision date Monday 2027-08-30, a second pair only if the DP-13
extension fires. R2 does not block the lock. **R1 has returned** (`research/reports/STEWARD_Q015_exposure.md`,
2026-09-13, counts only) and is closed; the schedule in §5 and the band-E / band-U suppressions in §3
are computed from it. Two items were **DEFAULTED on Haci's behalf** under DP-43 and are listed on the
board: the replacement of H-060's named baselines with the adjacent band 80–85 (item 1), and the
window / decision date / single extension on the slowest of the three measured rates (item 4).
