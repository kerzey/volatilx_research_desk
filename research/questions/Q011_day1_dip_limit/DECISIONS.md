# Q011 — decisions before lock
Run: 2026-09-13 by decision-maker · Source: PREREG.md "Open decisions before lock", 7 items
(+ items 8–16: two R-3 choices the draft made silently and now carries as `DEFAULTED`, and the
DP-compliance confirmations the Registrar needs when it applies)
**Recorded: 2026-09-13 by decision-maker** — routed request **R1 returned**
(`research/reports/STEWARD_Q011_exposure.md`, counts only, read in full). Items **8** and **9**, the
two items that waited on it, are settled below against the measured counts. **R2 (successor freezes)
stays routed, due at the decision date; it does not block the lock.** Nothing in `results/`, no
parquet, no weekly or daily report was opened; `PREREG.md` was not edited.

**Mode: autonomous (`--autonomous`).** DP-40..48 are in force: **no decision is put to Haci before
lock**. What would have been an ASK is `DEFAULTED` — R-3 → **DP-43**, R-5 → **DP-45**, otherwise the
Registrar's recommendation unless a DECIDE ground gives another answer. Every DEFAULTED item is
listed under "Defaulted on Haci's behalf" and on the board; the locked question stands (rule 3) and
Haci overturns any of it by asking for a successor question, never by editing the locked file.

**Summary:** **14 DECIDED, 2 DEFAULTED (both R-3 → DP-43, both now *confirmed* against R1's measured
counts), 1 ROUTED closed (R1, returned 2026-09-13), 1 ROUTED open (R2 successor freezes, due at the
decision date), 0 ASK.** All seven of the draft's open items are settled by a `DP` entry, a locked
precedent or one defensible technical answer — none of them was ever a Haci decision. The two
genuinely reserved choices in this file (the window/decision date, and whether the thin k = 0.5 arm
carries a verdict) are R-3 and are defaulted under DP-43. **Nothing is pending; the file is complete
for lock.**

**State note:** `research/questions/Q011_day1_dip_limit/state.json` reads `PREREG_DRAFT` (the
Registrar advanced it at 2026-09-13T20:01Z; the earlier `IDEA` note in this file is superseded). The
controller advances Q011 to `PREREG_LOCKED --by desk` after `@registrar apply`, writing
`schedule.json` in the same step (DP-46). No `results/` directory exists and none was read; no
parquet, no weekly or daily report was opened.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | How non-fills are scored in the primaries (draft item 1) | DECIDED | **Option A — intention-to-treat.** Every eligible pick stays in the denominator of both arms; a pick the limit never filled is scored as no position (race non-WIN, `r = 0`), never dropped. The fill-conditional contrast (`ADV`) is computed, printed and decomposed out of the ITT number, and **never decides**. | DP-41 (option B needs a new rule-14 exception; the desk grants none, DP-05 untouched); rule 14; Q007 §4.1 variant C precedent; DP-45 |
| 2 | Fill price when session t+1 opens through the limit (draft item 2) | DECIDED | **Option A — `FILL_k = min(O_1, LIM_k)` bullish, `max(O_1, LIM_k)` bearish.** That is how a resting limit actually trades, and it is the reading less favourable to H-058 (it hands the limit arm the better price). | DP-45 (stricter of two readings that differ only in strictness); order mechanics; DP-26 |
| 3 | A session-t+1 L3 touch in the fill's own hourly bar, or with no hourly bars (draft item 3) | DECIDED | **Option A — counted post-fill (a WIN for the limit arm)**, applied identically wherever hourly bars cannot order the pair; the count of picks resolved by the rule is printed and the opposite reading is printed as a named sensitivity. The separate L3-versus-adverse collision stays **adverse-first** in both arms (DP-27), unchanged. | DP-45; DP-27 (same conservative principle, own endpoint); draft §4 ordering rules 2 and 3 |
| 4 | How many limit distances are primaries (draft item 4) | DECIDED | **Option A — both k = 0.25 and k = 0.5 are primaries, BH across m = 4.** H-058 names the 0.25–0.5 band as written and the Registrar does not re-unit or narrow a hypothesis; m = 4 raises no bar for either arm relative to m = 2. | DP-25; DP-44 (units from the hypothesis, converted not invented); rule 8 |
| 5 | Order duration (draft item 5) | DECIDED | **Option A — a day order resting for session t+1's regular session only.** H-058's claim is the *day-1* dip; a GTC order through t+5 is a different hypothesis and needs its own PREREG. The exploratory view stays the k-grid, not a duration grid. | DP-25; DP-26 |
| 6 | Whether a pick-night-close entry is a third primary arm (draft item 6) | DECIDED | **Option A — descriptive only (B3).** The primaries stay limit-vs-open, the two entries H-058 names; `C_t` (DP-03(a) proxy) and `E_AH` (Q004's definition verbatim, picks only) are reconciliation sensitivities that never decide. DP-11 does not force `C_t` here because Q011's subject **is** the entry basis — DP-11 exempts exactly that case. | DP-25; DP-11 (entry-basis exemption); DP-29 (Q004 owns the basis contrast); DP-03 |
| 7 | Picks whose L3 is at or through an arm's own entry (draft item 7) | DECIDED | **Option A — "not takeable": no position, race non-WIN, `r = 0`, counted per arm.** Excluding them would filter the denominator on a session-t+1 price (rule 14) and would remove exactly the picks that gapped to target. Reported as a descriptive both-arms sensitivity, never as the primary. | rule 5 ("a target already passed at that entry is not a hit"); DP-26; DP-41; DP-45 |
| 8 | Window, decision date, DP-13 extension and DEFERRED fallback (silent in draft §5; **R-3**) | **DEFAULTED** | **Window: pick nights 2026-06-01..2026-11-06** (after exclusions). **Decision date: Monday 2026-12-14** (last pick night + 20 sessions = 2026-12-07 with 2026-11-26 closed, plus the one-week freeze margin, first Monday on or after). **One automatic DP-13 extension** to pick nights ..2026-12-21 / decision **Monday 2027-02-01** (exactly +30 sessions, +20 to maturity, +1 week, first Monday). **DEFERRED** if a gate is still short after that single extension; no second extension, and a gate shortfall is never INCONCLUSIVE. Gates per primary endpoint on `eval.py`'s measured counts: ≥ 80 contributing nights **and** ≥ 30 contributing nights dated after the lock commit. Arithmetic verified against DP-43's recipe and inside the 12-month ceiling (lock 2026-09-13 → 3.0 months to the primary date, 4.6 to the extension). **CONFIRMED at record (2026-09-13) against R1's measured rate 0.9216 contributing nights/session (47 nights / 51 sessions, 2026-06-01..08-12): every element stands unchanged, nothing moved out and nothing was pulled in.** See "R1 resolutions" below for the arithmetic, line by line. | DP-43; DP-13; DP-21; DP-24; **R1** `STEWARD_Q011_exposure.md` §3; **not taken:** a shorter window that reports sooner but is HISTORICAL_ONLY (DP-31) |
| 9 | Whether the thin k = 0.5 arm carries a verdict (draft §5 demotion rule; **R-3**) | **DEFAULTED** | **The demotion rule stands and is decided at lock, symmetrically for both k.** If R1's measured counts project fewer than **20 contributing nights carrying ≥ 1 fill** at that k by the decision date, that k's P1 and P2 are **demoted to descriptive at lock** (reported with CIs, no verdict) and **BH still runs across m = 4**, so no bar falls for the surviving arm. If **both** k are short, no primary survives and Q011 goes to **DEFERRED** rather than locking without a testable primary. If R1 has not returned when `@registrar apply` runs, **nothing is demoted**: all four endpoints stay primary and a sub-floor fill cell yields SUPPRESSED sub-cell figures and an INCONCLUSIVE verdict for that endpoint — there is **no post-lock demotion**. **RESOLVED at record (2026-09-13): R1 measured 46 of 47 contributing nights carrying ≥ 1 fill at k = 0.25 and 44 of 47 at k = 0.5 — both far above 20, so NEITHER ARM IS DEMOTED. All four endpoints (P1-A, P2-A, P1-B, P2-B) carry verdicts and BH runs across m = 4. The demotion rule is discharged at lock and cannot fire later.** | DP-43 ("demoted to descriptive at lock, never dropped afterwards"); DP-21; Q009 item 17 (m unchanged by a demotion); **R1** `STEWARD_Q011_exposure.md` §2(b); **not taken:** deciding the demotion at the decision pass from `eval.py`'s counts |
| 10 | MPEs | DECIDED | **P1 (race, percentage points): 5.0 pp. P2 (money, ATR): 0.25 ATR, per *published pick*** — the ITT denominator, **not** rescaled to a per-filled-trade basis (rescaling would lower the bar, since fills are a subset and the ITT mean is diluted). No uplift is proposed for P1: Q007's 10.0 pp was for a difference-of-differences across gap arms, while P1 is a paired within-night contrast of two plans on the same picks, which removes the tape confound the uplift guards against. Both two-sided. | DP-20; DP-10; DP-44; Q009 item 5; Q007 §8 (uplift scope) |
| 11 | Exclusions file | DECIDED | **`research/data/exclusions_v003.json`**, the newest file, read by `eval.py` as `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, **no date hard-coded** in the PREREG or in `eval.py`. In-window that is 2026-06-26, 2026-07-02, 2026-07-06. If the Steward issues `exclusions_v004.json` before Q011 locks, the draft cites that file instead — the cited version is always the newest at lock. | DP-22; Q009 item 20 |
| 12 | Status of the rule-5 distance-matched control (B2) | DECIDED | **B2 is descriptive and never decides; the primaries stay the within-night paired limit-minus-open contrasts.** Rule 5's control requirement is satisfied: the primary is not a hit-rate claim about picks versus the market but a contrast of two entry rules on the same picks and the same tape, and the control-adjusted versions of P1 and P2 are printed beside every primary. Construction is Q006 §3's verbatim (10 nearest same-night non-published candidates on beta60 / atr_pct / runup20, anchored at each control's own close), and control rows never add to inferential n. | rule 5; Q004 §3 (same entry-basis question, control descriptive, paired basis contrast primary); Q006 §3; rule 6 |
| 13 | Does DP-12 fire (matched control on a path-derived conditioning variable)? | DECIDED | **No.** Q011 conditions on nothing: both plans are fully specified at 16:05 ET and every eligible pick is in both arms' denominators. The one construction that *is* conditioned on a completed piece of the forward path — the fill-conditional `ADV` — is already descriptive for the rule-14 reason in item 1, which is DP-12's outcome by a stricter route. No arm is formed from a session-t+1 event. | DP-12 (scope); DP-41; Q009 item 14 form |
| 14 | Successor freezes and what blocks the lock | DECIDED | **Lock now, pinned to `manifest_v001` / `manifest_prices_v001`;** `manifest_v002` / `manifest_prices_v002` are built and pinned **at the decision date** (routed R2), symbol scope = **every candidate on the new nights, published and unpublished**, plus **hourly bars for published symbols**, carrying 20 forward sessions beyond the last included pick night (40 where a descriptive companion is computed). A second pair is built **only if** the DP-13 extension fires. `eval.py` takes window, manifests, exclusions path and output directory as inputs — no hard-coded dates or paths — so one byte-identical script serves both runs. **Neither successor freeze blocks the lock; R1 does not block it either** (item 9 states the no-R1 fallback). | DP-23; DP-46; Q006 §5; Q009 item 2 |
| 15 | Family, within-question and within-family correction | DECIDED | **F7 — Path, entry timing & volatility**, per the primary endpoint's subject (the entry basis, Q004's subject) and BACKLOG's own filing of H-058. **BH across m = 4 within the question** at q ≤ 0.10; across the family, BH over the 9 primaries of registered F7 questions — Q002 (3), Q004 (2), Q011 (4) — verified against those files. The Q004 and Q007 overlaps are non-independence hazards: cross-referenced, **never counted as two confirmations**, exactly as drafted. H-066 is not registered and is not tested here. | DP-29; rule 8; Q002 §4, Q004 §4 (primary counts) |
| 16 | Knowledge time — no exception requested | DECIDED | **Q011 needs and requests no rule-14 exception; DP-05 is untouched.** The fill, the not-takeable test and every touch are execution and outcome *measurement* — the status Q007 §6.1 already gives an exit fill and a gap-through touch — not feature use. `eval.py` must freeze the eligible set, both plans' parameters and every stratum label **before any session-t+1 or later bar is loaded**, and fail loudly if a t+1-or-later field is referenced in eligibility, matching or stratification. `uoa_symbol_daily.fwd_return_*` stays banned; `sas_selection_excursion` / `outcome_*` / `level_hit_*` are never inputs. | rule 14; DP-41; DP-05; Q007 §6.1 |

## R1 resolutions (recorded 2026-09-13)

Source: `research/reports/STEWARD_Q011_exposure.md` — counts only, no outcome of any kind. Headline:
**369 eligible picks on 47 contributing nights** (matured through **2026-08-12**; 48 matured nights,
one of which — **2026-06-02** — has zero eligible picks because all 8 published rows carry no
`swing_trading` lane). **Measured run-rate 0.9216 contributing nights/session** (47 / 51 sessions,
2026-06-01..08-12).

### Item 9 — neither k arm is demoted (R-3 default discharged)

| k | contributing nights with ≥ 1 fill | of 47 | fills / eligible | floor (DP-21/DP-43) | ruling |
|---|---|---|---|---|---|
| 0.25 | **46** | 97.9% | 232 / 369 (62.9%) | 20 | **not demoted** |
| 0.5 | **44** | 93.6% | 157 / 369 (42.5%) | 20 | **not demoted** |

- **Ruling: both arms carry verdicts.** All four primaries — P1-A, P2-A (k = 0.25) and P1-B, P2-B
  (k = 0.5) — stay primary; **BH runs across m = 4** (unchanged in every branch); no endpoint is
  descriptive by demotion. The §5 demotion rule is **discharged at lock** and cannot fire again
  (DP-43: never demoted afterwards).
- The ruling does not hedge on the window not yet measured: *nights carrying ≥ 1 fill* is monotone
  non-decreasing as nights accrue, so 46 and 44 are lower bounds for the registered window. The
  both-short cascade to DEFERRED is therefore dead in this question.
- Supporting counts the Registrar prints in §2/§5 (measured, not gates): Plan M **not takeable
  9 / 369 (2.4%)** — item 7's rule bites on 9 picks in the open arm; Plan L(k) **not takeable 0** for
  both k, confirming §2's construction argument. Of the fills, **at the open** 89/232 (38.4%) at
  k = 0.25 and 43/157 (27.4%) at k = 0.5 — item 2's fill-price rule (`min(O_1, LIM_k)`) governs those
  and no others. **Hourly-bar coverage on session t+1: 369 / 369 (100%)** — item 3's no-hourly-bars
  fallback is **not exercised anywhere in the sealed window**; it survives only for the descriptive
  B2 control pool, whose symbols are not all in `p001_hourly_raw` (report §4.4), and those are
  counted under R2's stated fallback, never back-filled.
- Funnel for §2, verbatim from R1: 383 published/matured → −8 no lane plan (all on 2026-06-02) → −0
  lane-without-L3 → −4 `outcome_target_invalid` → −0 direction/close/ATR → −2 wrong-side L3 → −0
  missing t+1 bar → **369 eligible**. A matured night with zero eligible picks is simply
  **non-contributing**; it is not added to the exclusions file and not counted toward any floor.

### Item 8 — window, decision date and extension CONFIRMED (nothing moved)

Each line is DP-43's recipe re-run on the measured 0.9216, against the drafted value.

- **80-contributing-night floor (DP-21).** 2026-06-01..2026-11-06 is **112 sessions**;
  112 × 0.9216 = **103.2 projected contributing nights ≥ 80**. The 80th falls 33 nights beyond the 47
  measured = 35.8 sessions after 2026-08-12 → raw pick night **≈ 2026-10-02**, inside the window.
  **Not binding; window end stands.**
- **30-post-lock-night floor (DP-24, binding).** 2026-09-14..2026-11-06 is **40 sessions**;
  40 × 0.9216 = **36.9 ≥ 30**, with 30 reached after 30 / 0.9216 = 32.6 sessions → raw pick night
  **≈ 2026-10-28/30** (R1 §3 floor 3), inside the window with ≈ 7 nights of margin. **Window end
  stands at 2026-11-06.**
- **Stratum floors (20 per cell).** **Already met as measured** — 42 of 47 regime-legal nights
  (label legal from 2026-06-09, FREEZE_v001 §7), calendar halves 24 / 23. No projection needed and
  no cell is at risk; the halves' split point is re-derived from the final window at the decision
  pass.
- **Decision date Monday 2026-12-14.** 2026-11-06 + 20 sessions = **2026-12-07** (2026-11-26
  Thanksgiving closed), + one-week freeze margin = 2026-12-14, which **is** the first Monday on or
  after. R1's independent binding-gate date is **2026-12-07 ≤ 2026-12-14**, so the recipe does not
  push the date **out**; and a date is never pulled **in** to report sooner (DP-43, DP-45).
  **Confirmed unchanged.**
- **DP-13 extension, window ..2026-12-21 / decision Monday 2027-02-01.** 2026-11-06 + 30 sessions =
  **2026-12-21** (DP-43's +30); 2026-12-21 + 20 sessions = **2027-01-21** (2026-12-25, 2027-01-01,
  2027-01-18 closed), + one week = 2027-01-28 → first Monday on or after = **2027-02-01**.
  **Confirmed unchanged.**
- **DEFERRED fallback.** Unchanged (DP-13): one automatic extension on `eval.py`'s measured counts,
  then DEFERRED. No second extension, no gate reduced, and a gate shortfall is never INCONCLUSIVE.
- **12-month ceiling (DP-43).** Lock 2026-09-13 → decision **3.0 months**, extension **4.6 months**.
  Inside the ceiling; Q011 is not DEFERRED on that ground.
- **Not HISTORICAL_ONLY.** DP-24 is met by design from this run, so DP-31 does not apply and no
  successor replication question is required.

## Corrections to silent choices

Applied by the Registrar with the rest.

- **§5 demotion rule — now settled, not conditional (DP-43; R1 returned).** The whole conditional
  passage goes. §5 states the **ruling**: measured at lock from `STEWARD_Q011_exposure.md` §2(b),
  **46 of 47 contributing nights carry ≥ 1 fill at k = 0.25 and 44 of 47 at k = 0.5, both above the
  20-night floor, so neither arm is demoted; all four primaries carry verdicts and BH runs across
  m = 4**. Add one sentence that the demotion test was decided **at lock** and that **no arm is ever
  demoted after lock** (DP-43), so the rule is discharged. Delete "The k = 0.25 arm is never demoted
  by this rule", the "failing R1 …" fallback and the both-short → DEFERRED cascade — all three are
  spent. (DP-43; item 9.)
- **§8 clause 1 and the INCONCLUSIVE list — a SUPPRESSED sub-cell must not make the question
  unfalsifiable.** As drafted, clause 1 requires "≥ 20 contributing nights for **every reported
  sub-cell**" while §5 says the bear and 90+ cells are *expected* to be SUPPRESSED — read literally,
  no verdict could ever be reached. Align with the locked Q007 §8 wording: the requirement attaches
  to **any sub-cell that is reported**; a sub-cell below floor is **SUPPRESSED** (no point estimate,
  counts printed) and does **not by itself** make the endpoint INCONCLUSIVE. The stratification
  protection rule 7 requires stays where it belongs — clause 5 (both halves) and clause 6 (no tape
  stratum with ≥ 20 contributing nights beyond MPE in the opposite sign), neither of which is
  weakened. The INCONCLUSIVE bullet's "a reported sub-cell below floor (SUPPRESSED)" reads "a
  **reported** sub-cell below floor", consistent with §5. (DP-21; Q007 §8 clause 1.)
- **§5 floor-date projection — replace the borrowed rate with the measured one; the dates do not
  move.** The draft's 0.92 contributing nights/session was borrowed from `STEWARD_Q009_exposure.md`
  §R1(d). R1 now measures Q011's **own** rate at **0.9216** (47 contributing nights / 51 sessions,
  2026-06-01..08-12, 369 eligible picks). §5 cites `research/reports/STEWARD_Q011_exposure.md` and
  prints the measured figures: **112 in-window sessions → ≈ 103 projected contributing nights** (80th
  ≈ 2026-10-02) and **40 post-lock sessions → ≈ 37 projected post-lock nights** (30th ≈ 2026-10-30),
  with the stratum floors **already met** (42/47 regime-legal; halves 24/23). Replace "≈ 101
  contributing and ≈ 35 post-lock nights" accordingly. **Window end 2026-11-06, decision date
  2026-12-14, extension ..2026-12-21 / 2027-02-01 all stand unchanged** — the recipe pushed nothing
  out, and a date is never pulled in to report sooner (DP-43, DP-45). §5 keeps the sentence that
  every gate is decided on `eval.py`'s measured counts, never on this projection or on R1. (DP-43;
  item 8.)
- **§2 funnel and §5 exposure — print R1's measured counts (bookkeeping).** The funnel (383 → −8
  no-lane-plan → −4 `outcome_target_invalid` → −2 wrong-side L3 → **369 eligible on 47 contributing
  nights**), the fill counts (232 / 137 at k = 0.25; 157 / 212 at k = 0.5), the not-takeable counts
  (**Plan M 9 (2.4%); Plan L(k) 0 for both k**, which *verifies* §2's construction argument rather
  than assuming it), the at-open fill shares (89/232 and 43/157) and **hourly coverage 369/369** go
  into §2/§5 as measured facts with the report cited. Add the data note that **all 8 no-lane-plan
  rows fall on the single night 2026-06-02**, which is therefore the one matured night with zero
  eligible picks: it is **non-contributing, not excluded** — no exclusions file changes — and it is
  flagged to the Red Team as an unexplained payload gap, not to this question's design.
  (R1 §1, §2, §4.3.)
- **State file.** `state.json` now reads `PREREG_DRAFT` (advanced by the Registrar 2026-09-13);
  after `@registrar apply` the controller advances it to `PREREG_LOCKED --by desk`, writing
  `schedule.json` from the `## Schedule` block below in the same step (DP-46). Bookkeeping, not a
  design change — the Decision-maker edits neither file.
- **"Open decisions before lock" (§11) — delete the section entirely** once the above are applied;
  nothing may read as open at lock. After applying, `grep` the file for `open decision`,
  `Recommendation:`, `k = 0.5 arm is never demoted`, `failing R1` and `every reported sub-cell` —
  every hit must be gone or deliberate.

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is
edited):** none new. Q004 §2's looser publication predicate (`selected_rank` only, vs DP-28) and
Q006/Q007's inclusion of pick night 2026-06-26 are already flagged in Q007's and Q009's DECISIONS.md
and are repeated here only so Q011's F7 family arithmetic is read with them in view.

## Defaulted on Haci's behalf

- #8 window and decision date — chose window 2026-06-01..2026-11-06, decide Monday 2026-12-14, one
  automatic extension to ..2026-12-21 / Monday 2027-02-01, then DEFERRED; not taken: a shorter
  window reporting sooner but HISTORICAL_ONLY (DP-31) — DP-43. **Confirmed at record against R1's
  measured 0.9216 nights/session: every date stands, nothing moved out, nothing pulled in.**
  Overturn = successor question.
- #9 verdict status of the thin k = 0.5 arm — chose demotion to descriptive decided **at lock** from
  R1's counts, symmetric across both k, BH m = 4 unchanged, DEFERRED if both arms are short; not
  taken: demoting the arm at the decision pass — DP-43. **Resolved at record: 46/47 and 44/47 nights
  carry ≥ 1 fill, so neither arm is demoted and all four primaries carry verdicts.** Overturn =
  successor question.

## Schedule

**Final — confirmed 2026-09-13 against R1's measured run-rate (0.9216 contributing nights/session).**
Written verbatim to `research/questions/Q011_day1_dip_limit/schedule.json` by the Registrar at
`apply` / lock (DP-46).

- `decision_date`: **2026-12-14** (Monday) — window end 2026-11-06 + 20 sessions = 2026-12-07
  (2026-11-26 closed) + one-week freeze margin, first Monday on or after. R1's independent binding
  gate (30 post-lock nights, matured + margin) lands 2026-12-07 ≤ this date, so it does not move out;
  it is never pulled in (DP-43, DP-45).
- `extension_date`: **2027-02-01** (Monday) — window extends once to pick nights ..**2026-12-21**
  (= 2026-11-06 + 30 sessions, DP-43); 2026-12-21 + 20 sessions = 2027-01-21 (2026-12-25, 2027-01-01,
  2027-01-18 closed) + one week → first Monday on or after. Fires automatically, on `eval.py`'s
  measured counts only (DP-13), with the unmodified `eval.py`.
- `hard_stop`: **null** — none. DP-13's single automatic extension, then DEFERRED, replaces it.
- `rule`: **fixed**
- `extended`: **false**
- `window`: pick nights **2026-06-01..2026-11-06** (after `exclusions_v003.json`; in-window that
  removes 2026-06-26, 2026-07-02, 2026-07-06).
- `gates`: per primary endpoint — **≥ 80 contributing nights** (DP-21) **and ≥ 30 contributing
  nights dated after the lock commit** (DP-24, the binding one). A shortfall on one endpoint is
  never covered by another's count; a gate shortfall is not INCONCLUSIVE — it fires the single
  extension, then DEFERRED.
- `note`: _PREREG §5 / DP-43 / DP-13. Gates are evaluated on `eval.py`'s measured counts from the
  frozen data at the decision pass, never on the projection above, the run-rate, or R1. No interim
  looks; `eval.py` runs once. **Not HISTORICAL_ONLY — PROSPECTIVELY_CONFIRMED is reachable from this
  run by design** (DP-31 does not apply, no successor replication question needed). Both dates sit
  inside DP-43's 12-month ceiling (3.0 and 4.6 months from lock). Routed **R2** (successor freezes
  `manifest_v002` / `manifest_prices_v002`) is due at `decision_date`; a second pair only if the
  extension fires._

## Routed requests

### data-steward

**R1 — RETURNED 2026-09-13 → `research/reports/STEWARD_Q011_exposure.md`.** Counts only, protocol
observed (no bar after session t+1, no touch, no return, no P&L, no picks-minus-control difference).
It settled items **8** (dates confirmed, nothing moved) and **9** (neither arm demoted) — see
"R1 resolutions" above; `@registrar apply` folds the counts into §2/§5 before the lock. The request
as issued, for the record:

**R1 — exposure-only count for Q011 (due before the decision pass; earlier if the cycle allows, in
which case `@registrar apply` folds the counts into §5 before the lock; it does not block the
lock).**

On the frozen data only (`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`),
for the exact Q011 §2 population — published picks under the DP-28 predicate (`qualified IS TRUE AND
selected_rank IS NOT NULL`), non-excluded nights per `research/data/exclusions_v003.json`
(`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪
`uncorroborated_publication_runs.trading_dates`), pick nights ≥ 2026-06-01, a
`public_payload_json.lane_plans.swing_trading` first target present (L3 = `targets[0]`),
`d_close = dir × (L3 − C_t) / ATR > 0`, and a 20-session forward window matured in
`manifest_prices_v001` — please report **counts only**: **(1)** the §2 funnel — published rows →
null-ladder removals → wrong-side-L3 / `outcome_target_invalid` removals → ungradeable-symbol
removals → **eligible picks**, and **contributing nights** (≥ 1 eligible pick), with the
matured-night count and the last matured pick night; **(2)** per contributing night and in total:
picks filled at k = 0.25, picks filled at k = 0.5, picks not filled (per k), and picks not takeable
at the open (`dir × (L3 − O_1) ≤ 0`), where `LIM_k = C_t − dir × k × ATR`, a fill is `low_1 ≤ LIM_k`
bullish / `high_1 ≥ LIM_k` bearish on session t+1's regular-session daily low/high; **(3)** the
number of **contributing nights carrying ≥ 1 fill, per k** — this is the input to the §5 demotion
rule and it is needed **before lock** if the arm is to be demoted at lock at all; **(4)** the share
of fills that occur **at the open** (`dir × (O_1 − LIM_k) ≤ 0`) versus intraday, per k; **(5)**
**hourly-bar coverage** on session t+1 for published symbols in the window (how many eligible picks
can be resolved by §4 ordering rule 2), and confirmation that the successor price freeze's symbol
list will carry hourly bars for published symbols; **(6)** contributing nights **per month**, so the
draft's borrowed 0.92 contributing-nights-per-session run-rate can be replaced by a measured one.
Definitions: `C_t` = the actual pick-night regular-session close from `prices_daily_split` (never
`spot_close`); `ATR` = ATR14 from `prices_daily_split` bars dated ≤ t (never the platform's
`atr_pct`); `dir` = +1 bullish / −1 bearish from `dominant_direction`. **Protocol (binding): counts
only.** Everything above is computable from `C_t`, `ATR`, the printed `L3`, and session t+1's
open/high/low plus hourly bars. **No bar dated after session t+1 may be read, no touch of any level
after session t+1, no return, no P&L, no picks-minus-control difference, and no outcome of any kind
may be computed or reported** — the same counts-only discipline as `STEWARD_Q007_exposure.md` §R5
and `STEWARD_Q009_exposure.md` §R1.

What it decides: **(a)** whether the k = 0.5 arm (and, symmetrically, k = 0.25) carries a verdict —
fewer than 20 contributing nights with ≥ 1 fill at that k demotes that k's P1 and P2 to descriptive
**at lock**, BH staying at m = 4; if both k are short, Q011 goes to DEFERRED (DECISIONS.md item 9,
DP-43); and **(b)** whether the measured contributing-night rate leaves the window 2026-06-01..
2026-11-06 and the decision date 2026-12-14 where DP-43's recipe puts them, or moves them **out**
(never in).

**R2 — OPEN, routed → data-steward. Due at the decision date 2026-12-14 (a second pair only if the
DP-13 extension fires, then due 2027-02-01). Not a blocker for lock.** One addition from R1 §4.4:
`p001_hourly_raw` is scoped to the 227 published-pick symbols, so B2 control symbols without their
own published history have no hourly bars — the successor hourly scope stays **published symbols**
and control pairs that cannot be ordered fall to §4 ordering rule 2's stated reading and are
**counted**, never back-filled. The request as issued:

**R2 — successor freezes (due at the decision date; not a blocker for lock).** Build and pin
`manifest_v002` (selections; same SQL, same exclusion criterion) and `manifest_prices_v002` (same
Alpaca queries) covering pick nights after 2026-09-10 through the registered window end, with the
daily symbol list extended to **every candidate on the new nights, published and unpublished** (B2
needs the unpublished symbols' closes, session-t+1 bars and forward bars) **plus hourly bars for
published symbols** (§4 ordering rule 2, the DP-27 tie-breaks and the `E_AH` sensitivity), carrying
**20** forward sessions beyond the last included pick night (40 where the descriptive 40-session
companion is to be computed), and please fix the exact session-count decision date from the trading
calendar at the same time. A second pair is built **only if** the DP-13 extension fires. Nights
whose hourly bars are missing fall back to §4 ordering rule 2's stated reading and are counted;
nights whose unpublished-candidate bars are missing are excluded from B2 and counted, never
back-filled. (DP-23.)

## Standing rules added

_none._ Every item here is settled by an existing `DP` entry, a locked precedent or one defensible
technical answer, and the two DEFAULTED items are applications of DP-43. **No `DP` entry is created
from a DEFAULTED item** — a default is the desk acting on Haci's behalf, not an answer from him
(DP-40); only an answer of his becomes a Confirmed row.

## Standing rules proposed

Written down because they would generalise, **not added** to `research/DECISION_POLICY.md`. Each
needs Haci's word (or a later `--ask` cycle) before it becomes a `DP` row; until then the desk keeps
applying DP-43 case by case, as here.

- **P-1 (would extend DP-43): a Steward projection can only push a drafted date out, never pull it
  in.** When the Steward's measured run-rate re-derives a floor date *earlier* than the drafted
  decision date, the drafted date stands; when it re-derives one *later*, the window end and decision
  date move out to it and the extension is recomputed as +30 sessions from the new end. Rationale:
  DP-43 already forbids choosing a shorter window to report sooner; this states the comparison
  asymmetry explicitly, which is the exact step Q011 item 8 took (2026-12-07 projected vs 2026-12-14
  drafted → drafted stands).
- **P-2 (bookkeeping, would extend DP-22/DP-28): a matured pick night on which no row survives a
  question's eligibility funnel is a non-contributing night, not an exclusion.** It is never added to
  `exclusions_vNNN.json`, never counted toward a floor, and is reported in the funnel with its cause.
  Rationale: 2026-06-02 here (all 8 rows lack a swing lane); the same shape will recur in any
  question with a payload-dependent eligibility filter, and mixing it into the exclusions file would
  silently change every *other* question's population.
