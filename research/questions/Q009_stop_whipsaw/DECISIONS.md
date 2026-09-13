# Q009 — decisions before lock
Run: 2026-09-13 by decision-maker · Source: PREREG.md "Open decisions before lock", 8 items
(+ items 9–16, registrar-silent choices that a `DP` entry contradicts or that the applied decisions force)

State note: `research/questions/Q009_stop_whipsaw/state.json` does not exist and `PREREG.md` is
uncommitted — the question is pre-lock (PREREG_DRAFT) and these decisions are in scope. The state
file is initialised by the controller (registrar/coordinator), not here. No `results/` directory
exists and none was read.

**Summary (first pass):** 13 DECIDED, 3 ROUTED (all to the data-steward; R1 blocks the lock, R2 and
R3 do not), **0 ASK** — every open item is covered by a `DP` entry, a locked precedent or one
defensible technical answer. The one genuinely-Haci item this question carries (R-3: whether P3
stays a primary endpoint under the DP-21 floor, and where the decision date and hard stop land) is
**unanswerable without the Steward's counts** and goes to him with the numbers attached, exactly as
Q007's questions C and E did.

**Second pass, 2026-09-13 — R1 and R3 returned** (`research/reports/STEWARD_Q009_exposure.md`).
Items 1 and 7 are closed; items 4, 5, 10 and 14 are settled on the measured counts; six new items
(17–22) decide what the counts force. Headlines: the **null-stop denominator is zero** (0 of 874
published rows with a swing lane, all-time) — the PREREG's "binding unknown" does not exist; the
binding exclusion is instead the **wrong-side stop, 67 of 382 (17.5%)**; the bucket split is
**TIGHT 291 (93%) / MID 22 (7%) / WIDE 0** with a maximum `s_close` of 1.70 ATR, so the
three-bucket contrast the draft describes **does not exist in this window**; all three
contributing-night definitions collapse to **48 of 49** matured nights and project to 80 by
**2026-09-30**; the B1 control pool never binds (100% of eligible picks have ≥ 10 same-night
controls, 10th percentile 41); fallback-pattern stops are **0 in-window and 0 all-time**. R3
ruling 2 (E9a / guard / re-sort) is **negative**; R3 **ruling 1 (2026-06-26) is positive and blocks
the lock** — `exclusions_v003.json` is routed as R4. **One ASK** was opened: the initial window and
decision date (R-3, and DP-13 requires the extension and the DEFERRED fallback to be fixed with it).

**Third pass, 2026-09-13 — question A answered.** Haci took **option 2: window to 2026-10-02, decide
Monday 2026-11-09**, knowing that ≈ 16 contributing nights fall after the lock, that DP-24's 30-night
prospective gate therefore cannot be met, and that the best verdict from this run is
HISTORICALLY_CONFIRMED, licensing no subscriber-facing claim and no guide change. Recorded as the
decision, not re-litigated. Items 23–25 carry it: the dates, the **HISTORICAL_ONLY** labelling of §8
and §9, and a **successor prospective question (Q010, `stop_whipsaw_prospective`) drafted now and
locked at the same commit**. **No ASK remains open.** `DP-31` added (Default). R4 still blocks the
lock; R2 is due at the decision date by design.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Exposure-only stop count (swing-stop coverage, wrong-side stops, TIGHT/MID/WIDE night counts) | ROUTED → data-steward (**R1**) → **DONE 2026-09-13** (`research/reports/STEWARD_Q009_exposure.md`) | **Returned.** 394 published picks / 49 matured nights (20-session DP-09 clock) → **313 eligible picks / 48 nights**. Null-stop denominator **0** (0 of 874 published rows with a swing lane, all-time); wrong-side stop **67 of 382 = 17.5%** is the binding exclusion (→ item 18); buckets **TIGHT 291 / MID 22 / WIDE 0**, max `s_close` 1.70 ATR (→ item 17); P1(B1-valid), P2 and P3 contributing nights all **48 of 49**, projecting to 80 by **2026-09-30**; B1 pool never binds (100% ≥ 10 controls, 10th pct 41); fallback-pattern stops **0 in-window, 0 all-time** (→ item 21). The question is **not** deferred for want of stops, no endpoint is dropped for want of nights, and the date is set once (→ item 19, question A). Original request below, for the record. | DP-21; DP-12 downstream note (Q007 DECISIONS.md); Q007 items 2, 17; STEWARD_Q009 §R1(a)–(f) |
| 2 | Successor freezes (`manifest_v002`, `manifest_prices_v002`) | DECIDED (+ routed **R2**, not a blocker) | **Lock Q009 now, pinned to `manifest_v001` / `manifest_prices_v001`**; the successors are built and pinned **at the decision date**, with symbol scope = **every candidate on the new nights, published and unpublished** (B1 needs the unpublished symbols' closes and forward bars), plus hourly bars for published symbols (P2/P3 same-session tie-breaks). §5's clause stands: nights whose unpublished-candidate bars are missing are excluded from P1 and counted, never back-filled. Build order is in "Routed requests" R2 and does **not** block the lock. | DP-23; Q006 §5; Q007 item 1 |
| 3 | Stop line | DECIDED | **The printed swing-lane stop, paired with L3** — the printed stop of the lane whose target is the primary endpoint. The pick's own `best_timeframe` lane is **not** used (it would make the stop line vary pick by pick and would break the one-lane pairing with L3); the printed swing **invalidation** line stays a secondary run through the same P1/P2 constructions, descriptive; day lane (day stop ↔ L1) and long lane (long stop ↔ L5) stay secondaries. | DP-30; DP-09 (L3 is the primary level); Q007 item 8 |
| 4 | Stop-distance buckets | DECIDED → **scope narrowed by item 17** (WIDE is empty in this window; the contrast is TIGHT vs MID, descriptive) | **As drafted, on `s_close`: TIGHT `0 < s < 1.0`, MID `1.0 ≤ s < 2.0`, WIDE `s ≥ 2.0` ATR.** A registrar-chosen band stands provided it was not derived from sealed outcomes, and §6's disclosure establishes that the 1-ATR unit is the desk's existing Q004 adverse line, not an EXPLORE_001 figure. §2's sentence "the cut points are a registrar choice and an open decision for Haci" is deleted. Under item 12 the bucket variable and the entry-relative stop distance become the **same quantity**, which is what the bucket name is meant to mean. | DP-26; PREREG §6 disclosure |
| 5 | MPEs | DECIDED (P3's MPE is now a **reference line beside a descriptive figure** — item 17 — not a verdict threshold) | **P1: 5.0 pp** (control-adjusted touch-rate endpoint, the desk's standing number; P1 is a single control adjustment, not a difference of differences, so Q007's raised 10.0 pp does not carry over). **P2: 0.25 ATR per trade. P3: 0.25 ATR per trade.** The draft's 0.20 / 0.30 are placeholders written before Haci set the number; DP-10 fixes every per-trade ATR-denominated endpoint at 0.25 ATR and is **not re-asked**. P3 does not get a larger MPE than P2: DP-10 allows a larger one only with a Registrar reason, and "a wider stop raises risk per share" is an argument about position sizing, not about the per-trade ATR effect the endpoint measures. | DP-10 (Haci 2026-09-12, Q007 question B); DP-20; Q007 item 4b and its Q009 downstream note |
| 6 | Tie rule (unresolved same-session stop/target) | DECIDED | **P2/P3: stop fills first**, as drafted — hourly bars in time order first; if one hourly bar holds both levels, or the symbol has no hourly bars, the stop fills first; the count is printed. **P1 keeps SAME_SESSION = 0** (not a whipsaw) on daily bars for picks and controls alike: that is the same conservative principle in P1's direction (the outcome less favourable to the hypothesis) and it keeps picks and controls graded identically, which hourly-only-for-picks would not. The two rules are not harmonised into one; each is the conservative reading of its own endpoint. | DP-27; PREREG §4, §10.3 |
| 7 | Exclusions file | DECIDED (+ routed **R3** for 2026-06-26) | **Cite `research/data/exclusions_v002.json`** in the header, in §2 and in `eval.py` (`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`, read from the JSON, no hard-coded dates). The "exclusions_v001 plus the PREREG-cited re-run night 2026-07-02" fallback and the "if Haci issues v002 before lock" conditional are **deleted, not kept** — v002 exists and carries all four KT-audit re-run nights, of which 2026-07-02 is the one inside this window. The **2026-06-26 mixed-state night** (§10 threat 11) and the E9a historical-payload question (§10 threat 6) are a Steward ruling, not a Haci decision: routed as **R3**. **R3 returned 2026-09-13: ruling 2 (E9a / wrong-side guard / cross-lane re-sort) is NEGATIVE** — no payload rewrite anywhere in the 795-row correction ledger, §10 threat 6 is marked verified with the report cited; **ruling 1 (2026-06-26) is POSITIVE and blocks the lock** → item 20 and routed request **R4** (`exclusions_v003.json`). | DP-22; Q007 item 6; STEWARD_Q009 §R3 |
| 8 | Family: F4 vs F6 | DECIDED | **F6 — Exits and execution**, and `research/BACKLOG.md` H-032 is **re-filed from F4 to F6** by the Registrar when applying. DP-29 assigns a question by its **primary endpoint's subject**, and §8 is explicit that only **P2 or P3** can license a rule — both are the realized result of using the printed stop as an **exit** (the H-050 shape: exit rule vs no exit rule). §7 is rewritten: F6 holds H-050, H-051, H-052 and H-032; Q009 is the only registered F6 question, so the family correction is over Q009's own primaries today. **Anti-leniency clause (binding):** because P1 *is* a path-after-selection endpoint, the Reporter prints for P1 **two** q-values — BH within F6, and BH as if P1 were an F4 primary alongside the registered F4 primaries (Q007's four) — and **P1's verdict uses the larger (more conservative) q**. The family move must not make any endpoint easier to confirm than it was in the draft. | DP-29; rule 8; PREREG §8 ("a rule requires P2 or P3") |
| 9 | Primary clock: 40 sessions (drafted) vs 20 | DECIDED — **Correction** | **The primary clock is L3 within 20 sessions measured from the stated entry**, for P1, P2 and P3; the 40-session version of each is reported alongside, descriptively, wherever it has matured. DP-09 is Confirmed and was generalised in place on 2026-09-13 precisely so that it attaches to the level and the horizon, not to the entry basis: when L3 is the primary level the clock is 20 sessions, not the platform's 40-session swing-lane window, and **floors and decision dates are computed on the 20-session window**. It is also the conservative direction for this hypothesis — a shorter window gives the "recovered anyway" leg less room, so P1 and P2 both understate a whipsaw rather than overstate it. Nothing is lost: the 40-session numbers are still produced. | DP-09 (Haci 2026-09-12, Q007 question A); Q007 §4 |
| 10 | Sample floors: the floor reading | DECIDED — **Correction**; P3's floor question **resolved by R1**: TIGHT-contributing nights are **48 of 49** and project to 80 by 2026-09-30, so P3 is *not* short of sample — it is demoted for a different reason (item 17) | **≥ 80 contributing nights per primary endpoint, ≥ 20 contributing nights per reported sub-cell.** The draft's "≥ 20 eligible nights per reported cell, ≥ 80 eligible nights total" with "for P3 ≥ 20 TIGHT-cell nights" is exactly the weaker reading DP-21 rules out. **P3 is a primary endpoint, so P3's floor is 80 TIGHT-contributing nights**, not 20. Contributing night: for P1 — a night with ≥ 1 eligible pick **with a valid B1 control set**; for P2 — a night with ≥ 1 eligible pick; for P3 — a night with ≥ 1 eligible **TIGHT** pick. The floor is not loosened to keep P3; if the Steward's count (R1) cannot project 80 TIGHT-contributing nights by the hard stop, P3 drops to descriptive and the within-question BH runs across 2 — and **that drop is R-3, Haci's, with the numbers attached**. | DP-21; Q007 Corrections (same reading), Q008 §5 |
| 11 | Publication predicate | DECIDED — **Correction** | §2's "every published pick (`selected_rank IS NOT NULL`)" becomes **`qualified IS TRUE AND selected_rank IS NOT NULL`**; dark-lane rows are excluded from the treatment rows, and the B1 control pool is the **complement** of that predicate (same-night rows that are not published — qualified-false and dark-lane rows alike). | DP-28; Q007 item 18 / Corrections |
| 12 | Entry basis | DECIDED — **Correction** | **Entry is the pick-night regular-session close `C_t`** (`prices_daily_split`), the DP-03(a) after-hours proxy, **for picks and controls alike** — not the next-session open the draft uses. DP-11 is the standing rule for this batch and the Q007 pass recorded it explicitly ("Q008 and Q009 are drafts about picks that are already held, so their entry basis is `C_t` under DP-11"); a desk pass does not revert a recorded instruction of Haci's ("*measure the movement of the stock from closed price of previous day not opening prices*"). It is also the better geometry for this question in particular: the bucket variable `s_close` becomes the **actual entry-relative stop distance**, so TIGHT means what it says; the "stop at or through the entry" and "target at or through the entry" exclusions vanish (the wrong-side-of-`C_t` checks already cover them), so the picks whose stop was breached overnight — the most stop-relevant picks of all — are **graded instead of dropped**; and no forward bar is needed to decide eligibility, which is what lets R1 be a genuine no-forward-bar count. The **next-open basis is kept as a descriptive sensitivity** on picks and controls, and the real after-hours price `E_AH` (Q004's definition verbatim) as a **picks-only** descriptive sensitivity; neither decides. | DP-11; DP-03(a); Q007 item 12 and its Q009 downstream note; rule 5 (one basis on both sides) |
| 13 | Rule-5 stop-exit exception — its scope | DECIDED | The exception stands but is **written narrowly**: the printed stop is used as an exit **only inside the named execution plan E-STOP, and only in P2/P3**. In P1 and in **every** touch-rate, first-touch, excursion, counter-touch and scale-out figure in the file the stop is a measurement line and no position is ever exited on it; adverse excursion and counter-direction touches are reported, not used as exits. The results header and `REPORT.md` carry one sentence naming the exception and citing rule 5 and DP-02, so the desk's default ("stops are never assumed") is not read as having moved. | DP-02; rule 5 ("unless the PREREG says otherwise"; named execution plans) |
| 14 | Does DP-12 apply (matched control on a path-derived conditioning variable)? | DECIDED | **No.** Q009's conditioning variable is `s_close = dir × (C_t − S) / ATR` — the printed stop and the pick-night close, both **known at publication**; no part of it is a completed piece of the forward price path, so DP-12's matched-conditioning requirement does not fire. The Q007 downstream note ("check at decision time whether Q009's conditioning variable is path-derived") is hereby **closed: it is not**. The rule-5 distance-matched control **B1 stays as drafted** for P1 (it is required by rule 5 regardless of DP-12), and its availability is counted **before** lock in R1 — which is the part of DP-12's downstream note that does bind here, so the decision date is set once. **R1 confirms the pool never binds:** 100% of eligible picks have ≥ 10 same-night non-published controls (median pool 54, 10th percentile 41), so the P1 (B1-valid) contributing-night count is identical to P2's (48) and no pick is dropped for want of a control. | DP-12 (scope); rule 5; PREREG §2, §3; STEWARD_Q009 §R1(c) |
| 15 | Block bootstrap length | DECIDED — follows item 9 | **Expected block length 10 sessions** (20-session forward windows overlap across adjacent nights), 2,000 resamples, date-clustered CI printed alongside. The drafted 20 was Q006's length for a 40-session window; the 40-session descriptive companions are printed with the 20-session block and that is stated. | Q007 §4; Q006 §4; item 9 |
| 16 | PROSPECTIVELY_CONFIRMED clause | DECIDED — **Correction** | "≥ 30 eligible pick nights after this file's lock commit (and, for P3, ≥ 20 TIGHT-cell nights among them)" becomes **"≥ 30 *contributing* nights for the confirming endpoint dated after this file's lock commit"** — TIGHT-contributing for P3 — frozen separately, never inspected earlier, reproducing the sign under the unmodified `eval.py`. The clause does not weaken; if the window cannot supply 30, the decision date moves and that move is R-3. | DP-24; DP-21 |

## Second pass — what the Steward's counts and rulings decide, 2026-09-13

Source: `research/reports/STEWARD_Q009_exposure.md` (R1 counts, R3 rulings 1 and 2). No `results/`
directory exists and none was read; every figure below is an exposure count or a row-timestamp
ruling, not an outcome.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 17 | The bucket design and **P3's status**, now that WIDE is empty and 93% of picks are TIGHT | DECIDED | **P3 is removed from the primary endpoints and becomes descriptive; P1 and P2 are the primaries.** P3 as drafted is "P2 restricted to TIGHT", and TIGHT is **93% of the eligible picks** — the two endpoints would be computed on almost the same rows and would answer the same question, so registering both is a duplicate primary, not a stop-distance contrast. The contrast H-032 asks for cannot be formed in this window at all: **WIDE is empty (0 picks, max `s_close` = 1.70 ATR)** and MID is 22 picks, so there is no width variation to condition on. What replaces it: (a) the **TIGHT-vs-MID** difference of `D2_t`, descriptive, printed only if the MID cell clears 20 contributing nights and SUPPRESSED with its counts printed otherwise; (b) a **continuous** view — `Δ_p` against `s_close` (binned at 0.25 ATR and a rank correlation), descriptive; (c) the existing **model-free ATR stop grid** (synthetic stops at 0.5 / 1.0 / 1.5 / 2.0 / 3.0 ATR on the same picks), which is now the **only** view of stop width and still licenses no width (§9 unchanged). The bucket *definitions* stay in `eval.py` unchanged so a later window can populate WIDE. **Anti-leniency guard (binding): BH within the question keeps m = 3** — P3's p-value is still computed and still enters the correction; it simply cannot carry a verdict. Dropping a primary must not lower the bar for the two that remain, and with m = 3 every BH threshold is at or below its m = 2 value. **Why this is not an R-3:** P3's floor is comfortably met (48 TIGHT-contributing nights, projecting 80 by 2026-09-30), so nothing is being traded away for time; the demotion is forced by the measured composition of the population, and waiting cannot fix it (the stop writer produces tight stops — that is the finding). Disclosed to Haci in one line under "Questions for Haci" so he can overturn it at lock. | DP-29/rule 8 bookkeeping (a duplicate primary is not a second test); PREREG §5's own "P3 becomes descriptive, family shrinks" branch; STEWARD_Q009 §R1(b),(e) |
| 18 | The **17.5% wrong-side stop** — what it is and where it goes | DECIDED | **Two places, and neither is a research question.** (a) **In the PREREG:** it is a headline exclusion count, printed per bucket, per month and per score band in the results header; §10 threat 2 is quantified at **67 of 382 (17.5%)**; and §1, §10 threat 10 and `REPORT.md` must state plainly **which picks the question speaks for** — the 313 of 394 published picks (79%) whose printed swing stop is on the correct side of the pick-night close. The excluded 17.5% are exactly the picks whose printed stop is unusable, so no claim here extends to them. (b) **In `PLATFORM_ISSUES.md`:** a stop printed on the report card on the wrong side of the pick-night close is a **platform defect, not a hypothesis** — DP-07 sends it there for Haci to mark fix / research / accept. The desk does not "research" it and the Registrar does not fold it into Q009's §9. **Filing is the coordinator's/Steward's lane, not mine:** the entry text is supplied under "Routed requests → PLATFORM_ISSUES items" and I edit nothing. The same applies to the 2026-06-26 phantom rows (item 20). | DP-07; PREREG §10.2, §10.10; STEWARD_Q009 §R1(a) |
| 19 | Initial window, decision date, DP-13 extension and DEFERRED fallback | **ASK (question A)** — the numbers are attached and the choice is a date | Dates computed from the Steward's measured rate (48 contributing nights over 51 sessions = **0.941/session**, the same for all three definitions). The **binding gate is not the 80-night floor** — the 80th contributing pick night falls ≈ **2026-09-30**, maturing ≈ 2026-10-28 — but **DP-24's ≥ 30 contributing nights dated after the lock commit**, which needs ≈ 32 sessions after a ~2026-09-15 lock, i.e. pick nights to ≈ **2026-11-02**, maturing ≈ **2026-12-01**. Recommended: window **2026-06-01..2026-11-06**, decision date **first Monday on or after 2026-12-14**, one automatic DP-13 extension to window end **2026-12-31** / decision ≈ **2027-02-08**, DEFERRED if a gate is still short. R-3 names the decision date outright and DP-13 explicitly does **not** remove the R-3 for the *initial* window and date. | **R-3**; DP-13; DP-21; DP-24; STEWARD_Q009 §R1(c),(d); Q008 items 3/9 form |
| 20 | R3 ruling 1 — the 2026-06-26 night | DECIDED (scope) + ROUTED → data-steward (**R4**, blocks the lock) | **The whole night 2026-06-26 is excluded, not just the 3 uncorroborated rows.** The Steward offered both scopes and called whole-night the more conservative, KT-audit-consistent one: the 8 corroborated bullish rows came through the same write path and have not been shown clean of it, and the desk's existing precedent (`exclusions_v002.json`) excludes re-run **nights**, not rows. Where two answers differ only in strictness the stricter is taken. The exclusion is carried by **`exclusions_v003.json`**, issued by the Steward (R4) — **Q009 cannot lock until that file exists and the PREREG cites it** (DP-22: the newest file, read by `eval.py`, no hard-coded dates). Cost is one night: 48 → **47** contributing nights and ≈ 10 eligible picks, which changes no gate (the gates fire on `eval.py`'s measured counts, never on these projections). | DP-22; DP-04 (night-level exclusions); STEWARD_Q009 §R3 ruling 1 |
| 21 | Two secondaries that the counts have emptied | DECIDED | **(a) The fallback-pattern secondary is deleted as an endpoint** — "share of fallback-pattern stops … and P2 with them removed" is vacuous at **0 of 386 in-window and 0 of 874 all-time**; it survives as a one-line disclosed fact in §2 ("published picks never fall back to the deterministic 0.5% default stop; `ai_agents/principal_agent.py:897-911` is not the writer here"), which also removes §10's implicit worry that the population mixes LLM stops with fallback stops. **(b) The null-stop denominator bullet in §2/§5 stays as an exclusion in `eval.py`** (it must still be counted and printed, in case a successor freeze behaves differently) but **stops being described as "the binding unknown" and "a headline number"** — it is measured at **zero**, all-time, and §5's paragraph saying its size is unknown is deleted. | STEWARD_Q009 §R1(a),(f) |
| 22 | §10 threat 6 | DECIDED | **Marked verified negative**, citing `STEWARD_Q009_exposure.md` §R3 ruling 2: across the entire 795-row correction ledger no row touches `public_payload_json` or any `lane_plans` field; the wrong-side-target guard has no backfill path by construction; the W3 re-sort's late `updated_at` touches all cluster in freeze week (2026-09-05/08/09/10), none on the deployment dates. The draft's instruction that "the Steward should compare `created_at`/`updated_at` before lock" is replaced by the result. The `eval.py` clause that prints the platform commits touching `super_agent_select_service.py` / `principal_agent.py` inside the window, with P2 split at each such date, **stays** — it is a cheap descriptive robustness check, not a threat that is now closed. | STEWARD_Q009 §R3 ruling 2 |

**Decision-date rule the Registrar applies** (§5 and §8, verbatim in substance; **Haci 2026-09-13,
question A, option 2**):
- **Primary date.** Pick nights **2026-06-01..2026-10-02**; Q009 is evaluated at decision date
  **Monday 2026-11-09**, against the successor freezes built per R2 (the last pick night matures 20
  sessions later, ≈ 2026-10-30, leaving the Steward about a week to build and pin the freezes).
- **The gate, per retained primary endpoint, on measured counts.** Evaluation proceeds only if
  **each** of P1 and P2 (each on its own contributing-night definition, item 10) has **≥ 80
  contributing nights** printed by `eval.py` from the frozen data — **never** a projection, a
  run-rate or the Steward's 0.941/session figure, which is context for this decision only. A
  shortfall on one endpoint is never covered by the other's count. **This gate is marginal by
  construction:** the measured rate projects ≈ **81** contributing nights at 2026-10-02 against a
  floor of 80, so the extension below is the likely path and fires **automatically**.
- **The post-lock count is reported, not gating.** `eval.py` prints contributing nights dated after
  the lock commit per endpoint (projected ≈ **16**). It does **not** gate the historical verdict, and
  it cannot reach DP-24's 30 — see item 24 and the HISTORICAL_ONLY label.
- **One automatic extension (DP-13).** If either endpoint's 80-night gate is short at 2026-11-09, the
  window extends **once**, with no further question to Haci, to pick nights **2026-06-01..2026-11-13**
  (six further weeks of pick nights, ≈ 28 more contributing nights on the measured rate — a margin
  wide enough that a second extension is not foreseeable), decision **Monday 2026-12-21** (20 sessions
  after the last pick night, ≈ 2026-12-11, plus the same freeze margin the primary date uses; the
  Steward fixes the exact session-count date when building the successor freezes). The extended run
  uses the **unmodified `eval.py`** and the same gate.
- **DEFERRED fallback.** If a gate is still short after that single extension, Q009 goes to
  **DEFERRED** (`research/questions/DEFERRED.md`, with the measured counts) rather than running
  under-powered. There is no second extension.
- **Nothing weakens.** The 80-night gate is never reduced, no floor is lowered to hit a date (DP-21),
  the demotion of P3 never licenses reading P2 as a stop-distance result (item 17), BH stays at
  m = 3, and the shorter window is never used as an argument for relaxing anything else — the price
  of the shorter window is the prospective track, and that price is paid in full (item 24).

## Third pass — question A answered, 2026-09-13

**Recorded 2026-09-13:** Haci answered question A with **option 2** — window to **2026-10-02**,
decision **Monday 2026-11-09** — knowing and accepting that the prospective gate cannot be met from
this run. Items 23–25 record the consequences. **No ASK is open**; R2 and R4 remain outstanding by
design (R4 blocks the lock, R2 is due at the decision date).

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 23 | Window and decision date (question A) | ASK → **ANSWERED** | **Pick nights 2026-06-01..2026-10-02, decision Monday 2026-11-09**, one automatic DP-13 extension to **2026-11-13 / Monday 2026-12-21** on measured counts, **DEFERRED** if still short. Item 19's recommendation (2026-11-06 / 2026-12-14) is **superseded** and must not survive anywhere in the file. The 80-night gate is marginal at the primary date (≈ 81 projected), so the extension is the likely path and fires automatically with no further question. | R-3 → Haci 2026-09-13, question A, option 2; DP-13; DP-21 |
| 24 | What the shorter window costs, written into the file | DECIDED | **Q009 is registered HISTORICAL_ONLY.** §8 gains a paragraph, immediately after the verdict definitions: "**PROSPECTIVELY_CONFIRMED is unreachable from this run by design.** The registered window places ≈ **16** contributing nights per endpoint after the lock commit (measured rate 0.941 contributing nights/session, `STEWARD_Q009_exposure.md` §R1(d)), against DP-24's **30**. Haci chose this window on 2026-09-13 with that consequence stated (DECISIONS.md question A). The highest verdict available here is **HISTORICALLY_CONFIRMED**, and it is emitted with the label **`HISTORICAL_ONLY`** in the results header, in `REPORT.md` and in the LEDGER entry. The clause is not weakened to fit: DP-24's 30 stands, and the prospective track is reached by the successor question (item 25), never by re-reading this one." §9 gains, as its **first** line: "**Nothing in this section fires on a historical-only verdict.** Every guide line, card change, brief and subscriber-facing statement below requires PROSPECTIVELY_CONFIRMED (rule 10), which this run cannot produce; a HISTORICALLY_CONFIRMED result here licenses **no** product change, **no** Manual Trading Guide edit and **no** quotable number — it licenses only the successor question." The `DESIGN_CHOICE_NOT_BLIND`-style discipline applies: the label travels with the verdict wherever it is restated. | rule 10; DP-24; Haci 2026-09-13 (informed choice); Q007 §10.13 label precedent |
| 25 | A successor prospective question, pre-registered now | DECIDED | **Yes — the Registrar drafts it in this batch and it is locked at the same commit as Q009.** Working id **Q010**, slug `stop_whipsaw_prospective`. What it must be: a **replication, not a new question** — it inherits Q009 §2 (population, exclusions, entry basis `C_t`), §3 (B1), §4 (P1 and P2, 20-session clock, E-STOP/E-NOSTOP, tie rules), §7 (BH at m = 3) and §8 (MPEs 5.0 pp and 0.25 ATR, the six HISTORICALLY_CONFIRMED clauses) **by reference, verbatim, with no re-specification**, and it runs the **byte-identical, unmodified `eval.py`** Q009 registers. Its population is **pick nights strictly after Q009's decision date** (2026-11-09, or 2026-12-21 if the DP-13 extension fires — stated as a rule, so the successor needs no edit either way). Its gate is **DP-24's ≥ 30 contributing nights per endpoint** in that window, on measured counts, with its own single DP-13 extension and DEFERRED fallback. Its verdict rule: if Q009 returned HISTORICALLY_CONFIRMED on an endpoint and Q010 reproduces that endpoint's **sign** with `\|m\| >` MPE and its CI excluding 0, the pair is **PROSPECTIVELY_CONFIRMED** and only then does Q009 §9 fire. **Why this is decided and not asked:** locking it now is what keeps the prospective track blind — a successor drafted *after* Q009's numbers are seen would carry every design choice made with those numbers in hand, which is the hazard rule 3 exists for, and it is exactly the `DESIGN_CHOICE_NOT_BLIND` exposure Q007 had to label. It costs no new estimand, no new MPE and no new `eval.py`. **Q010's own initial decision date is its own R-3** and goes to Haci in Q010's decision pass, with the Steward's counts attached, the way this one did — it is not pre-empted here. Q010 is filed in **F6** with Q009 and is **not** counted as a second family member in BH (a replication of the same endpoints is not a second test; it is stated in both files). | rule 3; rule 10; DP-24; DP-13; DP-29; Q009 §8 PROSPECTIVELY_CONFIRMED clause |

## Corrections to silent choices

Applied by the Registrar with the rest; each is a `DP` entry the draft contradicts, or an edit the
decisions above force.

- **§8 MPE paragraph — the MPEs are not placeholders.** "**MPE (placeholders — Haci to confirm at
  lock…)**", "**P2: 0.20 ATR per trade**", "**P3: 0.30 ATR per trade**, higher because…" and the
  sentence "The P2/P3 MPEs have **no desk-derived basis** … Haci should set them from how much
  per-trade difference would make him stop honouring a printed stop" are stale: Haci set the number
  on 2026-09-12 (Q007 question B → DP-10). It must read: "**MPE: P1 5.0 pp (DP-20, the standing
  control-adjusted touch-rate number). P2 0.25 ATR per trade and P3 0.25 ATR per trade (Haci
  2026-09-12 → DP-10; the standing number for every per-trade ATR-denominated endpoint, not
  re-asked).**" (DP-10; DP-20; item 5.)
- **Header, §2 exclusions bullet — exclusions file.** Cite `research/data/exclusions_v002.json`;
  delete "exclusions_v001.json … plus the confirmed re-run night 2026-07-02" and the conditional
  "If Haci issues `exclusions_v002.json` before lock, `eval.py` reads it instead and this bullet
  becomes a pointer" — v002 exists, so the bullet **is** the pointer. `eval.py` reads
  `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` from the JSON; no hard-coded dates.
  (DP-22; item 7.)
- **§2 treatment rows — publication predicate.** "every published pick (`selected_rank IS NOT NULL`)"
  → **`qualified IS TRUE AND selected_rank IS NOT NULL`**; §3 B1's "same-night unpublished
  `sas_candidates` rows" → "same-night rows that are **not published** under that predicate
  (qualified-false and dark-lane rows alike)". (DP-28; item 11.)
- **§4, §2, §5, §7, §8, §10 — the primary clock is 20 sessions, not 40.** Every primary-endpoint
  definition (P1's `k_S`/`k_T`, P2's E-STOP/E-NOSTOP terminal exit, P3) runs on **k = 1..20** with
  the terminal exit at the **session-20 close**; the 40-session version of each is produced and
  labelled "descriptive, does not decide". §2's closing line ("Levels and windows are the platform's
  own: L3 lane window 40 trading sessions") keeps the platform citation but reads that the **primary
  clock is 20 sessions from the stated entry (DP-09), with the platform's 40-session lane window
  reported alongside**. §5's maturity arithmetic ("Binding maturity: 40 sessions", the "≈ 28 nights"
  and "80th eligible night ≈ 2026-09-25 → matures ≈ 2026-11-20" lines) is **recomputed on a
  20-session maturity** from the Steward's R1 counts, not re-estimated by hand. §10 threat 8 reads
  "overlapping **20-session** windows … block length fixed here (10 sessions)". Day-lane (L1/20) and
  long-lane (L5/60) secondaries are unchanged. (DP-09; item 9.)
- **§4 Inference — block length.** "expected block length **20 sessions** (40-session forward windows
  overlap …; Q006's length for a 40-session window)" → "**expected block length 10 sessions**
  (20-session forward windows overlap across adjacent nights; Q007 §4)". (item 15.)
- **§4, §2, §3 — entry basis.** "**Entry basis: next-day open** (`X = O_{t+1}`…)" → "**Entry basis:
  pick-night regular-session close `C_t`** (`prices_daily_split`), the DP-03(a) after-hours proxy,
  for picks and controls alike (DP-11; DECISIONS.md item 12)". Consequential edits, all mechanical:
  - §2 definitions: delete `X = O_{t+1}`, `s_open`, `d_open`; keep `s_close = dir × (C_t − S)/ATR`
    as **both** the bucket variable and the grading stop distance, and add
    `d_close = dir × (T − C_t)/ATR` as the target distance.
  - §2 exclusions: delete the "stop at or through the entry (`s_open ≤ 0`)" and "L3 at or through the
    entry (`d_open ≤ 0`)" bullet — the wrong-side-of-`C_t` bullets for the stop (`s_close ≤ 0`) and
    for L3 already cover it on this basis, and nothing is dropped for a level breached overnight.
    Keep every other exclusion, each counted and printed, per bucket.
  - §3 B1: place the control's levels off the **control's own close**,
    `S_c = C_c × (1 − dir_p × s_close,p × atr_pct_c)`, `T_c = C_c × (1 + dir_p × d_close,p × atr_pct_c)`,
    graded from the control's own close, same direction, same 20-session window, same daily-bar rule
    (the Q007 B3 anchoring pattern, moved from the open to the close).
  - §4 plans: session index k = 1..20 with **k = 1 = session t+1, entered at `C_t`**; the
    "opens through … (k ≥ 2)" gap-through clauses become **k ≥ 1**, so a session-t+1 open through the
    stop fills at that open and an open through L3 fills there too. Rule 5's "a target already passed
    at entry is not a hit" is carried by the wrong-side-of-`C_t` exclusion.
  - §4 secondaries: add the **next-open entry basis** (picks and controls) and keep `E_AH` as a
    **picks-only** sensitivity — both "descriptive, does not decide".
  - §6 knowledge-time table: the `X = O_{t+1}` row moves to the secondaries (sensitivity only), so no
    session-t+1 quantity enters any primary or any eligibility filter; note explicitly that Q009
    needs **no** rule-14 exception (DP-05 is untouched, no R-1 arises).
  - §10 threat 2 ("the stop is anchored to the lane entry, not the close or the open") keeps its
    wrong-side headline counts, now per bucket on the close basis. Add one clause to §10 threat 4:
    the close is not a tradable price (SAS publishes after the close), so `C_t` is a proxy for an
    after-hours fill, and the `E_AH` sensitivity shows the picks-only difference (DP-11).
  (DP-11; DP-03(a); item 12.)
- **§5 floors, §8 clause 1 — the floor reading.** "≥ **20 eligible nights per reported cell**, ≥ **80
  eligible nights total** … For P3 the cell is nights with ≥ 1 eligible TIGHT pick" must read
  **"≥ 80 contributing nights per primary endpoint — P1: nights with ≥ 1 eligible pick carrying a
  valid B1 control set; P2: nights with ≥ 1 eligible pick; P3: nights with ≥ 1 eligible TIGHT pick —
  and ≥ 20 contributing nights per reported sub-cell (bucket, tape stratum, half, band, bull/bear,
  regime)"**. §8 clause 1 becomes "contributing nights ≥ 80 for that endpoint". §5's pre-lock P3
  clause changes accordingly: "**If TIGHT-contributing nights project below 80 by the hard stop, P3
  is removed from the primaries before lock**" — the number 20 in that clause is wrong. (DP-21;
  item 10.)
- **§8 PROSPECTIVELY_CONFIRMED.** "≥ 30 eligible pick nights occurring after this file's lock commit
  (and, for P3, ≥ 20 TIGHT-cell nights among them)" → "**≥ 30 contributing nights for the confirming
  endpoint dated after this file's lock commit**" (TIGHT-contributing for P3). (DP-24; DP-21;
  item 16.)
- **§5 exposure-count paragraph — what the Steward may read.** "**no bar after night t is read** (not
  even `O_{t+1}`)" is **kept and now consistent**, because item 12 removes the open from every
  eligibility filter. Add that the count is also run on the **B1-valid** definition (same-night
  non-published candidates with ≥ 60 daily bars dated ≤ t) so the decision date is set once, and that
  it reports the null-stop share **by month and by score band** (§10 threat 10 cannot be read
  otherwise). (item 1; DP-12 downstream note.)
- **§5 decision date and hard stop — recomputed, not re-estimated.** The drafted "first Monday on or
  after **2026-11-23** … hard stop **2027-01-25**" was derived from a 40-session maturity and a
  20-night P3 floor, both now wrong in opposite directions. The **rule** stays in form — the first
  Monday on which every retained endpoint shows ≥ 80 contributing nights (DP-21), evaluation runs
  regardless on the hard stop, any endpoint below floor is INCONCLUSIVE (SUPPRESSED) — and the two
  **dates** are set from R1's counts and projections, in one pass. If the projection puts an endpoint
  past the hard stop, that is R-3 and goes to Haci with the numbers; it is never met by lowering a
  floor. (DP-21; DP-24; Q007 items 10 and 20 — the Registrar should note that Q007 moved its stop
  twice for exactly this reason and set Q009's once.)
- **§2 / §1 — the bucket sentence.** "the cut points are a registrar choice and an open decision for
  Haci" → "the cut points are fixed here (DP-26; DECISIONS.md item 4)". (DP-26; item 4.)
- **§4 — the rule-5 stop exception, narrowed.** "**Stops are assumed in this question, and only here**
  … In P1 it is a measurement line. Everywhere else stops are not assumed." is kept and extended by
  one sentence: "**The exception is confined to plan E-STOP in P2 and P3. Every other figure in this
  file — P1, every touch rate, first-touch session, adverse excursion, counter-direction touch and
  the committed L1–L6 scale-out — is graded with no stop, and the same sentence is printed in the
  results header and in `REPORT.md` (rule 5; DP-02).**" (DP-02; item 13.)
- **§7 — family.** "**Family:** F4 Price behaviour after selection (hypothesis H-032)" in the header
  and §7's "Across the family: F4 …" become **F6 Exits and execution** (H-050, H-051, H-052, H-032);
  Q009 is the only registered F6 question, BH runs across its own 3 primaries (2 if P3 is dropped),
  and the F4 paragraph naming Q007's primaries is replaced by the **dual-q clause for P1**: the
  Reporter prints P1's q both within F6 and as if P1 were an F4 primary alongside the registered F4
  primaries, and **P1's verdict uses the larger q**. `research/BACKLOG.md` H-032 is re-filed from F4
  to F6 with the note "registered as Q009"; the F4 list drops to 6 hypotheses and §7's overlap
  paragraph (H-033, H-058, H-060, Q004, Q007) is kept unchanged — none is merged. (DP-29; rule 8;
  item 8.)
- **§10 threats 6 and 11 — routed, not left as "the Steward should".** Both now read that the ruling
  is requested before lock as DECISIONS.md R3, and that if `public_payload_json` was mutated after
  publication on 2026-06-26 (or on the E9a-affected historical rows) the Steward issues
  `exclusions_v003.json` and the PREREG cites it under DP-22. (DP-22; item 7.)
- **"Open decisions before lock" section — delete it entirely** once the above are applied. All eight
  items are decided here or routed; nothing may be left in the file that reads as open at lock. After
  applying, `grep` the file for `0.20 ATR`, `0.30 ATR`, `placeholder`, `O_{t+1}`, `40 trading
  sessions`, `2027-01-25`, `2026-11-23`, `exclusions_v001`, `open decision` — every hit must be gone
  or deliberate (the 40-session descriptive companions and the day/long-lane secondaries are the only
  legitimate survivors of the window greps).

### Added on the second pass (2026-09-13) — what the Steward's counts force

- **Header, §2, §5 — exclusions file.** Cite **`research/data/exclusions_v003.json`** (R4), not v002,
  once it is issued; `eval.py` reads `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`
  ∪ the new 2026-06-26 block from that file. **Q009 does not lock before the file exists.** (DP-22;
  item 20.)
- **§1, §4, §5, §7, §8, §9, §10 — P3 is no longer a primary.** §1's P3 bullet is re-worded as the
  descriptive stop-distance view; §4's "Primary endpoints (three…)" becomes **two** (P1, P2) with P3
  moved into the secondaries as "**P3 (descriptive, does not decide)** — `D3_t` on TIGHT picks, the
  TIGHT-vs-MID difference (printed only if the MID cell clears 20 contributing nights, SUPPRESSED
  with counts otherwise), and `Δ_p` against `s_close` binned at 0.25 ATR with a rank correlation";
  §7 keeps **BH across m = 3** with the sentence "P3's p-value enters the correction and cannot carry
  a verdict — the demotion must not lower the bar for P1 and P2"; §8's clauses lose "and for P3 ≥ 20
  TIGHT-cell nights" and gain nothing in its place; §9's "**P3 CONFIRMED negative**" bullet is
  **deleted and its guide line moves to the P2 bullet**, re-worded: "the eligible population is 93%
  tight-stopped (`s_close < 1 ATR`, max 1.70), so a CONFIRMED-negative P2 **is** a statement about
  tight printed stops — the guide line 'a printed swing stop this close to the pick-night close is
  inside normal noise; do not use it as a hard exit' follows from P2, and the ATR floor's *width*
  still needs its own PREREG". The §4 ATR stop grid keeps its "cannot license a width" clause. (item
  17.)
- **§2, §5 — the empty WIDE bucket and the 93/7 split, stated as measured facts.** Add to §2, cited
  to `STEWARD_Q009_exposure.md` §R1(b),(e): eligible picks **313** on **48** nights, **TIGHT 291
  (93.0%) / MID 22 (7.0%) / WIDE 0 (0.0%)**, maximum `s_close` **1.70 ATR**; the WIDE definition is
  retained in `eval.py` for later windows and printed as n = 0. Delete §2's implication that the
  three buckets partition a spread of stop widths. (item 17.)
- **§2, §5, §10 threats 2 and 10 — the wrong-side stop is the binding exclusion, at 17.5%.** Replace
  the draft's "its size is unknown today and is a headline number" (written of the null-stop
  denominator) with the measured funnel: 394 published → 8 no ladder → 0 no L3 → **0 null stop** → 4
  `outcome_target_invalid` → **67 wrong-side stop (17.5% of 382)** → 2 wrong-side L3 → 0 short
  history → **313 eligible**. §1 and §10 threat 10 must say which picks the question speaks for:
  **313 of 394 published picks (79%)**, i.e. those whose printed swing stop is on the correct side of
  the pick-night close; the 17.5% excluded are exactly the picks whose printed stop is unusable and
  no claim extends to them. The wrong-side count is printed per bucket, per month and per score band
  in the results header. (item 18; DP-07 for the platform side.)
- **§5 — the null-stop paragraph.** "**Stop coverage … no coverage figure exists, and this is the
  binding unknown**" and the DEFERRED branch that depends on it are **deleted and replaced** by the
  measured result: coverage is complete (0 null stops in 874 published rows with a swing lane,
  all-time), so Q009 is **not** a candidate for DEFERRED on stop coverage; the exclusion stays in
  `eval.py` and is printed. (item 21.)
- **§4 secondaries — delete the fallback-pattern endpoint**, replaced by one disclosed line in §2:
  0 of 386 in-window and 0 of 874 all-time carry the deterministic 0.5% fallback pattern
  (`ai_agents/principal_agent.py:897-911`), so the studied stop is always the strategist's. (item
  21.)
- **§5, §8 — the decision-date rule.** Replace the drafted "first Monday on or after **2026-11-23** …
  hard stop **2027-01-25**" with the five-bullet rule under "Second pass" above (primary date, both
  gates on measured counts, one automatic DP-13 extension, DEFERRED fallback, nothing weakens),
  filled in with Haci's answer to question A. The word "hard stop" is replaced throughout by
  "extension date" and "DEFERRED fallback" — DP-13's machinery, not Q007's. (DP-13; DP-21; DP-24;
  item 19.)
- **§10 threat 6 — marked verified negative**, and **§10 threat 11 — rewritten as resolved**: the
  2026-06-26 night is excluded by `exclusions_v003.json`, with one sentence on what was found (the
  night's own run audit records 8 qualified, all bullish; the frozen table carries 11, the 3 extra
  bearish rows with fully-formed payloads including swing stops; 1 of 113 nights). Both cite
  `STEWARD_Q009_exposure.md` §R3. (items 20, 22.)
### Added on the third pass (2026-09-13) — Haci's answer to question A

- **§5, §8 — the decision-date rule, filled in.** Apply the five-bullet block under "Second pass"
  **as amended by item 23**: window **2026-06-01..2026-10-02**, decision **Monday 2026-11-09**, the
  80-contributing-night gate per primary endpoint on measured counts, the post-lock count printed but
  **not gating**, one automatic DP-13 extension to **2026-11-13 / Monday 2026-12-21**, DEFERRED after
  that. After applying, `grep` the file for `2026-11-06`, `2026-12-14`, `2027-02-08`, `2026-11-23`,
  `2027-01-25` and `hard stop` — every hit must be gone. (item 23.)
- **§8 — the HISTORICAL_ONLY paragraph**, verbatim as item 24 writes it, placed immediately after the
  verdict definitions, and **the existing PROSPECTIVELY_CONFIRMED clause is kept unchanged** (it is
  not deleted and not weakened — it is simply unreachable here, and the successor question is what
  satisfies it). Add to the HISTORICALLY_CONFIRMED clause list: "**7. the verdict is emitted with the
  label `HISTORICAL_ONLY` and is never restated, ledgered or quoted without it.**" (item 24; DP-24;
  rule 10.)
- **§9 — the opening line**, verbatim as item 24 writes it: nothing in §9 fires on a historical-only
  verdict; the section's contents are otherwise unchanged and describe what would follow **after**
  the successor question confirms. The §9 bullets keep their "flag-off, byte-identical checksum,
  shadow ≥ 20 trading days" discipline (rule 11). (item 24; rule 10.)
- **§1 and the header — one line of framing**, so the ceiling is visible before §8: "**Registered
  HISTORICAL_ONLY** (DECISIONS.md items 23–24): the window Haci chose on 2026-09-13 places ≈ 16
  contributing nights after the lock commit against DP-24's 30, so this run cannot reach
  PROSPECTIVELY_CONFIRMED; the tradeable verdict is reached by the successor question **Q010**,
  locked at the same commit." (items 23, 24, 25.)
- **§7 — one sentence on Q010**: "Q010 (`stop_whipsaw_prospective`) is a **replication** of P1 and P2
  on nights after this question's decision date, locked at the same commit; it is **not** counted as a
  second F6 question in the BH correction, and its result is never presented as independent evidence —
  it is the prospective half of this result." (item 25; DP-29; rule 8.)
- **§5 expected-n arithmetic.** Replace every hand-computed figure ("≈ 28 nights", "69 sealed nights",
  "the 80th eligible night ≈ 2026-09-25", "matures ≈ 2026-11-20") with the Steward's measured ones,
  cited: 49 matured nights, 313 eligible picks, 48 contributing nights on all three definitions,
  0.941 contributing nights per session, 80 projected by 2026-09-30, B1 pool median 54 / 10th
  percentile 41. The Registrar states no hand-counted night total; `eval.py` prints them.

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is edited):**
- `Q006 §4 E1` — primary endpoint is **L3 within 40 sessions**, with floors and the floor date
  computed on that window. DP-09 (Confirmed 2026-09-12, generalised in place 2026-09-13) makes the
  primary clock for an L3 endpoint **20 sessions from the stated entry**, with 40 descriptive. Q006
  locked before DP-09 existed and is not edited; flagged for Q006's Red Team review so the two
  questions' L3 numbers are never read side by side as if they were on one clock.
- `Q004 §2`, `Q006 §2` — publication predicate is `selected_rank not null` only, looser than DP-28.
  (Already flagged in Q007's DECISIONS.md; repeated here only so the flag is not lost.)
- **New, from R3 ruling 1 — `Q007` (PREREG_LOCKED 2026-09-13, commit `b211292`, cites
  `exclusions_v002.json`) and `Q006` (locked, cites `exclusions_v001.json`) both carry pick night
  **2026-06-26** inside their populations, and that night's published set cannot be trusted: 3 of its
  11 "published" rows (AAPL, DPZ, COIN) are not corroborated by the night's own 16:05 ET run audit,
  and they carry complete payloads. Neither locked file is edited and neither exclusions file is
  overwritten — flagged to the Red Team for those questions' reviews, with
  `research/reports/STEWARD_Q009_exposure.md` §R3 ruling 1 as the evidence. `Q008` (PREREG_DRAFT)
  cites v002 and is **not** locked: its decision pass should switch it to `exclusions_v003.json`
  under DP-22 before it locks. `Q005` is LEDGERED/INCONCLUSIVE — one night, no action.

## Questions for Haci

### A. Q009 asks whether the stop printed on a pick shakes you out of trades that reach the target anyway. The Steward has counted the nights: the sample is there, and the clock is now set by the prospective half (30 nights *after* we lock), not by the 80-night floor. How long do we leave it open?
Why yours: R-3 — the decision date and how long a question stays open is always your call, and DP-13
requires the one automatic extension and the DEFERRED fallback to be fixed **now**, at lock, so that
"it came up short" never comes back to you as a second question. The desk never lowers a floor to
hit a date.
*One thing you should know before you answer, decided by the desk and yours to overturn at lock:*
**93% of picks carry a stop tighter than 1 ATR, 7% are MID and there are no WIDE stops at all** (the
widest printed stop in the window is 1.70 ATR), so H-032's "by stop distance" half cannot be tested —
the third endpoint (P3, tight stops only) would have been the second endpoint computed twice. **P3
is demoted to a descriptive figure; P1 (is the whipsaw more than volatility geometry?) and P2 (what
does honouring the printed stop cost?) stay primary**, and the multiple-testing correction still
counts three tests so nothing gets easier. Separately: **1 in 6 published picks (17.5%) prints a
stop on the wrong side of the pick-night close** — unusable, excluded and counted here, and filed to
`PLATFORM_ISSUES.md` for you to triage as a platform defect (DP-07).
- (Recommended) **Window to 2026-11-06, decide Monday 2026-12-14.** Both gates (80 nights, and 30
  nights after the lock) are met on the measured run-rate with about two weeks of margin. If either
  is short on the day, the window extends **once**, automatically, to 2026-12-31 / decide ≈ 2027-02-08;
  still short → DEFERRED. Cost: about three months before Q009 reports.
- **Window to 2026-10-02, decide Monday 2026-11-09.** Five weeks sooner and the 80-night floor is met —
  but only about 16 nights would fall after the lock, so the prospective track cannot be evaluated in
  the single run the rules allow, and the best verdict available becomes HISTORICALLY_CONFIRMED, which
  licenses no subscriber-facing claim and no guide change.
- **Window to 2026-12-04, decide Monday 2027-01-18.** Five weeks more margin in case the run-rate
  drops (it is currently near saturation — almost every session contributes), extension to 2027-01-29 /
  decide ≈ 2027-03-08. Cost: another five weeks of waiting for a risk the numbers say is small.
Answer: **"Window to 2026-10-02, decide Monday 2026-11-09"** (Haci, 2026-09-13) — **option 2**, chosen
over the recommendation with the consequence stated in front of him and accepted: only about **16
contributing nights fall after the lock commit**, so DP-24's **30-night prospective gate is not met**
and **PROSPECTIVELY_CONFIRMED is unreachable from this run by design**. The best verdict available is
**HISTORICALLY_CONFIRMED**, which licenses **no subscriber-facing claim and no guide change**
(rule 10). He traded the tradeable verdict for five weeks of speed; that is his call, it is recorded
as the decision, and it is **not re-asked**. What the desk does with it is items 23–25: the ceiling is
written into §8 and §9 so no reader mistakes a historical verdict for a tradeable one, and a
successor prospective question is pre-registered at the same commit so the tradeable verdict is still
reachable later without an interim look at Q009.

---

**Nothing else is open.** Every other item is settled by a `DP` entry (DP-07, DP-09, DP-10, DP-11,
DP-13, DP-20, DP-21, DP-22, DP-23, DP-24, DP-26, DP-27, DP-28, DP-29, DP-30), by a locked precedent,
or by one defensible technical answer:

- **R-4 (MPEs)** — already set: DP-10's 0.25 ATR governs P2 (and P3's descriptive figures); DP-20's
  5.0 pp governs P1. Asking again would be the second time for the same number.
- **R-2 (horizon, level, lane)** — already set: DP-09 (L3 within 20 sessions) and DP-30 (the swing
  lane's printed stop, the lane whose target is the primary endpoint).
- **R-1 (knowledge time)** — none arises: after item 12 the question reads no session-t+1 quantity in
  any primary or eligibility filter, so DP-05 is untouched.
- **R-3 (waiting vs sample size)** — **asked once, as question A, and answered 2026-09-13** (option 2;
  window to 2026-10-02, decide Monday 2026-11-09), with the Steward's measured counts attached and the
  DP-13 extension and DEFERRED fallback fixed in the same answer. Not re-asked. The
  demotion of P3 (item 17) is *not* bundled into it as a choice: it is not a waiting-vs-sample
  trade-off — P3's floor is met — and a 93/7/0 bucket split cannot support the contrast either way,
  so it is decided and disclosed in the preamble rather than put to him as an option.
- **The 2026-06-26 night** is a Steward artefact ruling, not a Haci decision: whole-night exclusion
  under DP-22/DP-04, routed as R4 (item 20). Its *platform* half, and the 17.5% wrong-side stops, go
  to `PLATFORM_ISSUES.md` under DP-07 for him to triage there — that is a triage queue, not a
  pre-registration decision, and it does not gate the lock.

## Routed requests

### data-steward

**R1 — exposure-only stop count — DONE 2026-09-13.** Delivered:
`research/reports/STEWARD_Q009_exposure.md` §R1. Result: 394 published picks / 49 matured nights →
**313 eligible picks / 48 nights**; **null-stop denominator 0** (0 of 874 published rows with a
swing lane, all-time); wrong-side stop **67 of 382 (17.5%)** is the binding exclusion; buckets
**TIGHT 291 (93%) / MID 22 (7%) / WIDE 0**, max `s_close` 1.70 ATR; P1(B1-valid) = P2 = P3(TIGHT) =
**48** contributing nights, projecting to 80 by **2026-09-30** at 0.941/session; B1 pool never binds
(100% ≥ 10 controls, median 54, 10th pct 41); fallback-pattern stops **0 in-window, 0 all-time**.
Consequences: items 17 (P3 demoted), 18 (wrong-side stop), 19 (question A), 21 (two secondaries
emptied). Original request below, for the record.

On the frozen data only (`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`),
for published picks (`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28) on non-excluded nights
(`research/data/exclusions_v002.json`, `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`),
pick nights ≥ 2026-06-01, whose **20-session** forward window has matured against the trading calendar
implied by `prices_daily_split` (the DP-09 clock, not 40 sessions), please report **counts only**.
Inputs are the pick-night close `C_t` from `prices_daily_split`, ATR14 from `prices_daily_split` through
night t, and `public_payload_json.lane_plans.swing_trading` — **no bar dated after night t is read, not
even the session t+1 open**; no high, low or close after t, no touch, no return, no target outcome, no
`sas_selection_excursion` column, nothing from `results/`. Definitions: `dir` = +1 bullish / −1 bearish
from `dominant_direction`; `S` = `lane_plans.swing_trading.stop`; `T` = L3 = `lane_plans.swing_trading.targets[0]`
(confirmed as the swing lane's first target, `services/sas_conviction_card.py:183-186`);
`s_close = dir × (C_t − S) / ATR`; `d_close = dir × (T − C_t) / ATR`.
Please give: **(a)** the population funnel — published picks and nights in window and matured, then rows
removed at each step: no lane-plan ladder at all; swing lane present but **no L3**; swing lane and L3
present but **`stop` null** (the null-stop denominator — this is the headline unknown); non-bullish/bearish
direction; no `C_t` or no ATR; `outcome_target_invalid` non-null; **wrong-side stop** (`s_close ≤ 0`);
**wrong-side L3** (`d_close ≤ 0`); symbol with fewer than 60 daily bars dated ≤ t. **(b)** eligible picks
(all filters passed) split by bucket on `s_close`: **TIGHT** `0 < s_close < 1.0`, **MID** `1.0 ≤ s_close < 2.0`,
**WIDE** `s_close ≥ 2.0`. **(c)** contributing nights on three definitions: **P2** — nights with ≥ 1
eligible pick; **P3** — nights with ≥ 1 eligible **TIGHT** pick; **P1 (B1-valid)** — nights with ≥ 1
eligible pick that has a usable distance-matched control set, i.e. ≥ 10 same-night **non-published**
`sas_candidates` rows (the complement of the publication predicate, including qualified-false and
dark-lane rows) whose symbol has ≥ 60 daily bars dated ≤ t; please also report the share of eligible
picks with ≥ 10 and with ≥ 3 such rows and the median and 10th percentile of that count, so the Registrar
can see whether the nearest-10 pool ever binds. **(d)** the monthly run-rate of each of the three
contributing-night counts, and the projected date each reaches **80** contributing nights, by the method
you used in `research/reports/STEWARD_Q007_exposure.md` R2 (rate = contributing nights ÷ elapsed sessions
between the first and last matured night, projected forward at that constant rate, sessions converted at
365/252). **(e)** the null-stop share and the TIGHT/MID/WIDE split **by month and by score band**
(< 80 / 80–85 / 85–90 / 90+), counts only — §10 threat 10 cannot be read without it. **(f)** the count and
share of **fallback-pattern stops** (stop exactly 0.5% from the lane `entry` with targets at +0.5% / +1%,
`ai_agents/principal_agent.py:897-911`), by month.
**What it decides:** with the floor read as ≥ 80 contributing nights per primary endpoint (DP-21), (c) and
(d) decide whether **P3 stays a primary endpoint** (it needs 80 **TIGHT**-contributing nights, not 20 —
if it cannot project them by the hard stop it drops to descriptive and the within-question BH runs across
2), whether **P1's B1-valid count** rather than the raw pick count is the binding one, and whether Q009 can
be **locked at all** — if eligible contributing nights cannot project to 80, the blocker is that the printed
stop is not populated, which is a data problem and sends the question to `research/questions/DEFERRED.md`
rather than to a later date. Every one of those is a waiting-vs-sample trade-off (R-3): it goes to Haci with
your numbers attached, is not decided by the desk, and is never met by loosening a floor. Your counts also
set Q009's **decision date and hard stop in one pass** — Q007 moved its stop twice because the matched
design was counted after the first date was set; please treat (c)'s B1-valid and TIGHT definitions as the
ones the dates are computed on.

**R2 — successor freezes (at the decision date; not a blocker for lock).** Due at the decision date
Haci set (question A, 2026-09-13): window end **2026-10-02**, decision **Monday 2026-11-09** — so the
freezes are built in the week of **2026-11-02**, after the last pick night matures ≈ 2026-10-30 — and
**again, if and only if the DP-13 automatic extension fires on measured counts**, for window end
**2026-11-13** / decision **Monday 2026-12-21**. A third build will be needed for **Q010** on its own
window (nights after Q009's decision date); that request comes with Q010's own decision pass. Scope
is unchanged and fixed by DP-23.

When Q009 reaches its decision date, build `manifest_v002` (selections, same SQL as v001) and
`manifest_prices_v002` (same Alpaca queries) covering pick nights after 2026-09-10, with the symbol list
extended to **every candidate on those nights, published and unpublished** — the unpublished symbols'
pick-night closes and forward bars are what the B1 distance-matched control is made of — plus **hourly bars
for published symbols**, needed for P2/P3's same-session stop-vs-target ordering. Scope is fixed by DP-23
and needs no further confirmation; `eval.py` records each sha256 and prints pre-lock and post-lock night
counts separately. If a successor price freeze omits unpublished-candidate symbols for some nights, those
nights are excluded from P1 and counted, never back-filled. Note that under DECISIONS.md item 9 the maturity
window is **20 sessions**, so the freeze must carry 20 forward sessions (40 where the descriptive companion
is to be computed) beyond the last included pick night.

**R3 — two pre-lock payload-integrity rulings — DONE 2026-09-13.** Delivered:
`research/reports/STEWARD_Q009_exposure.md` §R3. **Ruling 2 NEGATIVE** — no E9a / wrong-side-guard /
re-sort payload rewrite anywhere in the 795-row correction ledger; §10 threat 6 marked verified
(item 22). **Ruling 1 POSITIVE** — 2026-06-26 is the only night in 113 where the frozen qualified-row
count (11) disagrees with the run's own `stats_json` (8, all bullish); the 3 extra bearish rows
(DPZ, COIN, AAPL) carry complete payloads including the swing stop this question studies, and 10 of
the 11 rows sit in the eligible population. **This blocks the lock** → item 20 and R4. Original
request below, for the record.

Two nights/rows in Q009's window could carry a `public_payload_json` that is not what was published at
16:05 ET, which would mean the **printed stop the question studies is not the printed stop traders saw**.
First: **2026-06-26**, the mixed-state night the red team flagged separately and the KT audit explicitly
placed out of its scope (`research/reports/KT_AUDIT_manifest_v001_rerun_nights.md`, closing paragraph) —
partial row mutation, not a re-run. Please rule on whether that mutation touched `public_payload_json` (or
the lane-plan fields inside it) on that night's `sas_candidates` rows. Second: **§10 threat 6** — the
wrong-side-target guard and the E9a reclassification (`services/super_agent_select_service.py:810-839`,
ruling E9-2026-07-05) and the cross-lane monotonic re-sort (`:195-257`, "historical rows untouched"):
please compare `created_at` / `updated_at` on the affected rows inside 2026-06-01..2026-09-10 and state
whether any historical row's payload was rewritten after publication, and if so on which trading dates.
Row timestamps, counts and a pass/fail only — no price, no touch, no outcome. **What it decides:** if either
comes back positive, the affected nights are not knowledge-time-legal for this question, and under DP-22 you
issue `research/data/exclusions_v003.json` before this batch is locked and the PREREG cites it (the locked
files that cite v001/v002 are not edited); if both come back negative, §10 threats 6 and 11 are marked
verified with your report cited and nothing else changes. This needs no decision from Haci either way.

**R4 — `exclusions_v003.json` (blocks the lock; new, 2026-09-13).**

Please issue `research/data/exclusions_v003.json` as the successor to `exclusions_v002.json`,
implementing your own R3 ruling 1 at the **whole-night** scope (DECISIONS.md item 20 chose the
conservative option you flagged: the 8 corroborated bullish rows came through the same write path
and have not been shown clean of it, and the desk's exclusion lists are night-level by precedent —
`manual_runs`, `non_session_runs`). Contents: everything in v002 carried over unchanged
(`manual_runs.trading_dates` and `late_but_clean`, `non_session_runs`, `catalyst_layer_regime_change`,
`regime_label_point_in_time_from`, the `sas_candidates_availability_note_correction`), **plus a new
block** — suggested key `uncorroborated_publication_runs` — containing **2026-06-26** alone, with the
reason stated from your own evidence: the night's `sas_runs.stats_json` records `qualified_count: 8`
and 0 bearish selections, while the frozen `sas_candidates` table carries 11 qualified rows with a
non-null `selected_rank`, the 3 extra (DPZ, COIN, AAPL) carrying fully-formed `public_payload_json`
including swing-lane stops; it is the only night in all 113 with that mismatch; the mutation cannot
be dated more precisely than "after the 2026-06-26 16:05 ET run, before the 2026-09-10 freeze", so
the publication predicate cannot be trusted for that night. Cite
`research/reports/STEWARD_Q009_exposure.md` §R3 ruling 1 and the red team's original 06-26 flag; note
that the criterion is **new and distinct from** the re-run criterion (partial row mutation, not a
timestamp reset), so it is a separate block rather than an addition to `manual_runs`. Please also
re-derive `night_counts_after_exclusions` and, as a small addendum to your R1 report, the Q009
population under v003 (eligible picks and contributing nights, expected ≈ 303 picks / **47** nights),
so the Registrar quotes measured figures rather than my arithmetic. In the header note which
questions are affected: **Q009** (PREREG_DRAFT — cites this file; it is the reason the file exists
and **cannot lock without it**); **Q008** (PREREG_DRAFT, cites v002 — should switch to v003 at its
decision pass under DP-22); **Q007** (**PREREG_LOCKED** 2026-09-13, cites v002, and 2026-06-26 is
inside its ≥ 2026-06-01 window — **not edited**, flagged to the Red Team for Q007's review); **Q006**
(locked, cites v001 — same treatment, already flagged); **Q005** (LEDGERED/INCONCLUSIVE — one night,
no action). This is desk policy under DP-22 and needs no decision from Haci.

### PLATFORM_ISSUES items (DP-07) — for the coordinator/Steward to file; the decision-maker edits nothing

Two platform defects surfaced by R1/R3. Under DP-07 they are **not** research questions: they belong
in `PLATFORM_ISSUES.md` for Haci to mark fix / research / accept. Neither gates Q009's lock, and
neither may be folded into Q009 §9 as a finding.

- **Wrong-side printed stops — 17.5% of published picks.** 67 of 382 published picks with a swing
  lane and an L3 (pick nights 2026-06-01..2026-08-12, matured) carry a printed swing `stop` on the
  **wrong side of the pick-night close** — for a bullish pick, a stop above the close. The stop is
  written by the Principal Strategist off the lane `entry`, which may stray more than 5% from spot
  (`services/super_agent_select_service.py:101-111`), and it is passed through to
  `public_payload_json` **unvalidated** (`:94-95`, `:158`) while targets *are* checked against spot
  and entry (`:113-152`). It is displayed to subscribers on the report card
  (`report_center_frontend/components/ReportCard.tsx:254-255`). Effect: roughly one published pick in
  six shows a stop that is already breached at publication. Evidence:
  `research/reports/STEWARD_Q009_exposure.md` §R1(a). Suggested triage: a side-and-distance guard on
  the written stop, mirroring the existing target guard.
- **2026-06-26: three qualified, ranked picks the night's own run audit does not record.** The frozen
  `sas_candidates` table holds 11 qualified rows with a `selected_rank` for that trading date; the
  run's contemporaneous `stats_json` records 8, all bullish. The 3 extra bearish rows (DPZ, COIN,
  AAPL) carry complete lane plans with the payload `rank` matching the outer `selected_rank`. It is
  the only night in 113 with this mismatch, and `super_agent_select_runs` is updated in place with no
  run-history table, so the write path cannot be reconstructed from the desk side. Evidence:
  `research/reports/STEWARD_Q009_exposure.md` §R3 ruling 1. Suggested triage: find the write path,
  and consider an append-only run-history/audit table — its absence is what makes both this and the
  KT-audit re-run nights unrecoverable rather than merely detectable.

## Standing rules added

- **From question A (2026-09-13): the date itself generalises to nothing.** Window 2026-06-01..
  2026-10-02, decision 2026-11-09, extension 2026-11-13 / 2026-12-21 — the arithmetic of Q009's own
  run-rate against DP-21's floor, like Q007's questions C and E. No `DP` id taken for the date, and
  DP-13, DP-21 and DP-24 are all unchanged (no gate moved; the window did).
- **`DP-31` added (Default, `Q009, 2026-09-13`)** — **HISTORICAL_ONLY**. What generalises is not his
  answer but **what the desk owes a question whose window cannot supply DP-24's 30 post-lock nights**:
  §8 says PROSPECTIVELY_CONFIRMED is unreachable by design with the measured projection; §9 opens by
  saying no guide line, product change, brief or quotable number follows; the verdict carries the
  `HISTORICAL_ONLY` label wherever it is restated; and the **successor replication is locked at the
  same commit** so the prospective half stays blind. Every future ASK offering such a window states
  the ceiling in that option's consequence line instead of re-explaining it. Filed as a **Default, not
  Confirmed**, deliberately: Haci chose a date, he did not lay down a rule, and a Default is his to
  overturn the moment he wants a different handling. If he ever repeats the choice, that is the point
  to ask whether it should become Confirmed.

Four notes for the desk, not rules: (i) DP-12's Q009 downstream check is **closed negative** (item 14) — Q009's
conditioning variable is known at publication; (ii) DP-09's re-worded form has now been applied to a
question that never had a next-open spread entry (item 9), which is what the 2026-09-13 in-place edit
was for; (iii) the PREREG's "binding unknown" (null-stop coverage) turned out to be **zero**, while
the exclusion nobody had sized (wrong-side stops) turned out to be **17.5%** — worth carrying into
future drafts as a reason to route the *whole* funnel for counting, not only the suspected unknown;
(iv) if a second question ever hits a degenerate conditioning variable the way item 17 did, the
handling used here (demote the endpoint, keep BH at the registered m, say plainly that the
hypothesis's conditioning half is untestable in the window) is a candidate for a `DP` id — one
instance is not enough to write one.
