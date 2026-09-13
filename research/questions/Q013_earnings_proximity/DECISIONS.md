# Q013 — decisions before lock
Run: 2026-09-13 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 3 items
(+ items 4–17: the DP-compliance confirmations the Registrar needs when it applies, and the choices
the draft made silently that a `DP` entry or a locked precedent settles)
**Record pass: 2026-09-13 by decision-maker (autonomous)** · Source: `research/reports/STEWARD_Q013_exposure.md`
(R1(a) + R1(b), both returned). **R1 is CLOSED; no routed item blocks the lock.** `## Schedule` below
is final.

**Mode: autonomous (`--autonomous`).** DP-40..48 are in force: **no decision is put to Haci before
lock.** What would have been an ASK is `DEFAULTED` — R-1 → **DP-41**, R-2 → **DP-42**, R-3 →
**DP-43**, R-4 → **DP-44**, R-5 → **DP-45**; otherwise the Registrar's recommendation unless a DECIDE
ground gives another answer (DP-40). Every DEFAULTED item is listed under "Defaulted on Haci's
behalf" and on the board; the locked question stands (rule 3) and Haci overturns any of it by asking
for a successor question, never by editing the locked file.

**Summary: 16 DECIDED, 1 DEFAULTED (R-3 → DP-43, settled at `record` from the Steward's numbers),
1 ROUTED open (R2 successor freezes, due at the decision date, not blocking), 0 ASK.** Two of the
draft's three open items are settled by a `DP` entry or a locked precedent; the third is the decision
date, which is R-3, defaulted under DP-43 and **now computed** from R1(b).

**R1 has returned and Q013 locks (`record`, 2026-09-13).**
- **R1(a) PASS.** The sealed-window `days_to_earnings_corrected` / `earnings_phase` /
  `earnings_event_risk_corrected` values are live-path 16:05 ET writes at scoring time (platform SHA
  `fa70688b`, matching the manifest): the seasonal phase mix swings NO_WINDOW 83% → 19% → 71% → 87%
  across June–September (a flat backfill cannot produce that), non-null coverage holds at 98–100%
  where a re-run of the Phase-0b backfill would write null/`NO_UPCOMING`, and `created_at` clusters
  20:00–22:00 UTC on 98.5% of rows with the only two exceptions being the manual-run nights already
  carried in `exclusions_v003.json`. **No rule-14 exception is needed, so the DP-41 DEFERRED branch
  does not fire and the conditional registrar route below is VOID.** Two disclosures ride along, both
  accepted and neither changing the verdict: (i) `$RESEARCH_DB_URL` was not set, so the row timestamps
  were read from the frozen parquet's own `created_at`/`updated_at` rather than a live query — for
  historical, already-published, already-frozen rows these are the same DB-sourced values, and reading
  the freeze rather than the live table is the stricter course under rule 4, not a substitution;
  (ii) `earnings_phase_subtag` is 100% null in the sealed window because the live write block never
  calls `neutral_subtag()` — code-confirmed non-population, and the PREREG uses that column
  descriptively only, never for arm assignment. Item 11 already requires `eval.py` to reprint the
  monthly phase distribution and the non-null share, so the same check repeats on the successor freeze
  at the decision pass; a failure there is a `results/` finding, not a re-opened lock decision.
- **R1(b) returned:** 48 matured non-excluded nights (2026-06-01..2026-08-12), 383 published → 371
  eligible (arm A 44 / arm B 137 / arm C 190), **23 contributing nights**, B2 matching never binds
  (0 of 181 picks below the 3-control floor; every pick matched its full 10). Blended rate **0.4510
  contributing nights/session**. **80 contributing nights and 30 post-lock nights both project inside
  DP-43's 12-month ceiling (2027-09-13), so Q013 is locked, not DEFERRED** — see `## Schedule`.

Everything else in this file was already final at `decide`.

**State note:** `research/questions/Q013_earnings_proximity/state.json` reads `PREREG_DRAFT`
(registrar, 2026-09-13T20:59Z). R1 has returned; when `@registrar apply` runs, the controller advances
Q013 to `PREREG_LOCKED --by desk`, writing `schedule.json` from the `## Schedule` block in the same
step (DP-46). No `results/` directory exists and none was read; no parquet, no weekly and no daily
report was opened; `PREREG.md` was not edited.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Arm C (no scheduled report within 20 sessions) — third primary contrast or descriptive? (draft item 1) | DECIDED | **Option A — descriptive only (B4); the primaries stay the A-vs-B contrast H-064 writes.** The arms, the baseline and the endpoints come from the hypothesis as proposed; adding an A-vs-C primary would be a re-specification, not an application. Arm C keeps its full descriptive panel (counts, both estimands, its own per-`k` shape) and is reported beside B1 so a reader can see whether arm B is itself contaminated. BH within the question therefore runs across **m = 2**, and F4 carries 9 primaries (item 10). | DP-25 (the test stays the one that was proposed); DP-29; Q011 item 4 (endpoint count comes from the hypothesis, not from the Registrar); PREREG §3 B4 |
| 2 | Control pool for the primaries — unrestricted (B2) or earnings-arm-matched (B3)? (draft item 2) | DECIDED | **Option A — the unrestricted rule-5 distance-matched control B2 is inside P1 and P2; the arm-matched pool stays descriptive B3.** **DP-12 does not fire** (item 9): the conditioning variable here is a *scheduled report date known at 16:05 ET*, not a piece of the forward price path already completed when the signal is read, so nothing requires the control to be matched on it — and matching on it would strip out the very event being tested. B3's pool is additionally too thin to carry a floor (§10 threat 14). **§8's licensing paragraph is load-bearing and stands verbatim:** a CONFIRMED P1/P2 licenses a *skip rule* about picks; it never licenses "SAS is at fault" or a scoring change, which would need B3 registered as its own question. | rule 5 (unpublished same-night candidates at the same ATR distance); DP-12 (scope — does not fire); Q006 §3 construction; PREREG §8 licensing paragraph |
| 3 | Window end, decision date, extension and the DEFERRED fallback (draft item 3; **R-3**) | **DEFAULTED** | **DP-43's fixed recipe, arithmetic computed at `record` from R1(b) — not the draft's rolling exposure-driven Monday rule.** Window: pick nights **2026-06-01** (DP-06) through the session at which R1(b)'s measured contributing-night rate projects **≥ 80 contributing nights** (DP-21, on §2's ≥ 1 arm-A **and** ≥ 1 arm-B definition) **and ≥ 30 contributing nights dated after the lock commit** (DP-24). **Decision date** = window end + 20 sessions maturity + one-week freeze margin, first Monday on or after — and **never earlier than Monday 2027-03-01**, the drafted floor: a Steward projection pushes a date **out**, never pulls it **in** (Q011 item 8). **One automatic DP-13 extension**: window +30 sessions, maturity and margin recomputed, first Monday on or after. **Then DEFERRED** — no second extension, no reduced floor, no under-powered run, and a gate shortfall is **never** INCONCLUSIVE. Gates fire on **`eval.py`'s measured counts** at the decision pass, never on R1(b) or a run-rate. **12-month ceiling: if the projected initial decision date lands after 2027-09-13, Q013 is not locked — it goes to `research/questions/DEFERRED.md` with that date and the measured rate named** (the H-062 precedent). No interim looks; `eval.py` is written once (rule 9) and run once. **Settled at `record` from R1(b) (0.4510 contributing nights/session, blended): window end 2027-02-12, decision date Monday 2027-03-22, extension window end 2027-03-30 → extension date Monday 2027-05-10, hard stop none, DEFERRED thereafter. Inside the 2027-09-13 ceiling, so Q013 locks.** | DP-43; DP-13; DP-21; DP-24; DP-45; H-062 DEFERRED precedent; Q011 item 8; **not taken:** rolling Monday checks to a 2027-09-06 hard stop (Q007's form) |
| 4 | MPEs for both primaries | DECIDED | **P1 = 5.0 pp** (control-adjusted touch-rate endpoint, **DP-20** exactly — no uplift proposed, and none is warranted: P1 is a within-night A-minus-B contrast of control-adjusted rates, not an uncontrolled arm contrast). **P2 = 0.25 ATR** (**DP-10** via **DP-44** — the standing per-trade ATR number, not re-asked and not re-unitised). Both **two-sided**; the verdict carries its sign. No money-unit MPE is invented anywhere (DP-44). | DP-20; DP-10; DP-44; Q011 item 10; PREREG §8 as drafted (confirmed, not changed) |
| 5 | Which exclusions file | DECIDED | **`research/data/exclusions_v003.json`** — the newest file on disk (v001, v002, v003; no v004 exists at this run), read by `eval.py` as `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, with **no date hard-coded** in the PREREG or in `eval.py`. In-window that removes 2026-06-26, 2026-07-02 and 2026-07-06; the printed figure is the one `eval.py` derives. If the Steward issues `exclusions_v004.json` before Q013 locks, the draft cites that file instead — the cited version is always the newest at lock. `catalyst_layer_regime_change.fixed_from = 2026-06-01` and `regime_label_point_in_time_from = 2026-06-09` are read from the same file, not restated as literals. | DP-22; Q011 item 11; Q009 item 20 |
| 6 | Publication predicate | DECIDED | **`qualified IS TRUE AND selected_rank IS NOT NULL` (DP-28)**, as drafted. Dark-lane rows (`qualification_reason = 'selected_dark'`) are **not** treatment rows, are counted, and stay in the B2/B3 control pool. Q002/Q004/Q006's looser `selected_rank`-only predicate is **flagged to the Red Team for those questions' reviews, not fixed here** and not copied. | DP-28; PREREG §2, §10 threat 12 |
| 7 | Entry basis, and whether DP-11 forces the pick-night close | DECIDED | **Entry = the next session's official regular-session open `O_1` (DP-03(b))**, identically for picks and matched controls. **DP-11 does not fire:** nothing here is a position already held when the signal appears — the signal is a scheduled report date read at 16:05 ET and the decision it drives (skip / do not open the spread) is taken *before* entry. This is also the basis H-064 itself names ("drawdown from the open"), so DP-25 points the same way. No `C_t` entry variant is added as a primary; `C_t` is used only for ATR, beta60, runup20 and matching. | DP-03(b); DP-11 (scope — does not fire); DP-25; DP-42 (entry basis by DP-03/DP-11) |
| 8 | Primary level and clock | DECIDED | **L3 = `public_payload_json.lane_plans.swing_trading.targets[0]`, first touch within 20 sessions from entry** — the level H-064 names, on DP-09's clock; the platform's 40-session swing window is reported alongside, descriptively, wherever it has matured. L1, L2 and L4 stay descriptive. Sample floors, maturity and every date in §5 are computed on the **20**-session window. | DP-09; DP-42 (swing-lane question → L3 on the DP-09 clock); Q007 §5; Q011 §2 |
| 9 | Does DP-12 fire (matched control on a path-derived conditioning variable)? | DECIDED | **No.** DP-12 governs conditioning variables that are *themselves part of the price path* — an overnight gap (Q007), a fast start (Q008), any move already completed when the signal is read. Q013's arm label is a **scheduled calendar event known at 16:05 ET on the pick night**, fixed before any post-decision bar exists; no arm is formed from a session-t+1 or later price. The unrestricted B2 control therefore stands as the primary (item 2), and the arm-matched B3 is the descriptive panel by choice, not by DP-12 compulsion. | DP-12 (scope); PREREG §6.1; Q011 item 13 form |
| 10 | Family, within-question and within-family correction | DECIDED | **F4 Price behaviour after selection**, per the primary endpoint's subject — the price path after selection (DP-29), as BACKLOG files H-064. **BH across m = 2 within the question** (P1, P2) at **q ≤ 0.10**; every secondary prints raw p marked "descriptive, does not decide". **Across the family: 9 primary endpoints — Q007 (4), Q008 (3), Q013 (2)** — verified against those files; Q009/Q010 are F6, Q011 is F7 and **Q012 is F6** (re-filed from F7 under DP-29), so none of them enters F4's count. H-063 is *merged into Q007* and H-032 was re-filed to F6; neither is counted here. The Q007 / Q008 / Q011 / Q006 overlaps are non-independence hazards: cross-referenced, **never counted as two confirmations**, exactly as §7 drafts them. | DP-29; rule 8; Q007 §7, Q008 §7 (primary counts), Q012 §-header (F6) |
| 11 | Knowledge time — is a rule-14 exception needed? | DECIDED | **None is requested and none is granted; DP-05 is untouched.** The arm label is a scheduled report date available at 16:05 ET; every outcome is measured from `O_1` onward. DP-05(b)'s later classification clock is Q008's and **does not travel**. `eval.py` must freeze the eligible set, the arm labels, the matching inputs and every stratum label **before any session-t+1 or later bar is loaded**, and fail loudly if a t+1-or-later field is referenced in eligibility, matching or stratification. `uoa_symbol_daily.fwd_return_*` stays banned (PI-001); `sas_excursion` / `outcome_*` / `level_hit_*` are never inputs (counter-level **prices** only, never their dates). **R1(a) is blocking for exactly the DP-41 reason: if the sealed-window `days_to_earnings_corrected` / `earnings_phase` values are not point-in-time, the arm label would need a new rule-14 exception, the desk grants none, and Q013 goes to `DEFERRED.md` instead of locking.** `eval.py` reprints the monthly phase distribution and non-null share so the check repeats at the decision pass. | rule 14; DP-41; DP-05 (scope); DP-06; PREREG §6.1, §10 threat 1 |
| 12 | Successor freezes, and what blocks the lock | DECIDED | **Lock pinned to `manifest_v001` / `manifest_prices_v001`;** successor selection and price freezes are built and pinned **at the decision date** (routed R2), symbol scope = **every candidate on every new night, published and unpublished** (B2 needs the unpublished symbols' t+1 opens and forward bars) **plus hourly bars for published symbols** (the §4 descriptive tie-break), carrying **20** forward sessions beyond the last included pick night (40 where the descriptive companion is computed). A second pair only if the DP-13 extension fires. A night whose unpublished-candidate bars are missing loses its controls, is excluded from the primaries and is **counted, never back-filled**. `eval.py` takes window, manifests, exclusions path and output directory as inputs — no hard-coded dates or paths — so one byte-identical script serves both runs. **R2 does not block the lock; R1(a) and R1(b) do** (items 3 and 11). | DP-23; DP-46; Q006 §5; Q011 item 14 |
| 13 | Picks whose L3 is at or through `O_1` (`passed_at_entry`) | DECIDED | **Scored a non-hit (`Y_p = 0`), kept in the denominator, MAE still measured from `O_1`, counted and printed per arm** — a target you cannot buy is not a target, and the identical rule grades the controls. Both bounding sensitivities (removed from both arms; scored as favourable) are printed and **neither decides**. Removing them would filter the denominator on a session-t+1 price, which rule 14 forbids. | rule 5; DP-26; DP-41; Q002/Q003/Q006 convention; Q011 item 7 |
| 14 | `k = 0` picks (report dated on the pick night) | DECIDED | **Stay in arm A**, as H-064 writes the 0–3 band, with the per-`k` cells (0/1/2/3) printed. The desk holds no BMO/AMC flag, so some `k = 0` and `k = 1` prints are already absorbed at entry; that **dilutes arm A toward arm B**, i.e. it attenuates the hypothesis rather than helping it, which is the direction the desk takes when it must choose. A BMO/AMC version is a new question, not an edit. | DP-25; DP-45; PREREG §2, §10 threat 4 |
| 15 | Same-session ties in the counter-direction race | DECIDED | **Counter-level-first**, as drafted: any pick tie hourly bars cannot order, and **every** control tie (controls have no hourly bars), counts counter-level-first; the TIE count is printed separately and **TIE is never a third category in a printed share**. Hourly bars cover published symbols only (`freeze_prices.py:17`, `:117`), so the asymmetry is structural and is disclosed, not patched. | DP-27; PREREG §4; Q011 item 3 |
| 16 | Whether any arm or cell is demoted to descriptive at lock (DP-43's demotion clause) | DECIDED | **Nothing is demotable in this question, and the clause is discharged at lock.** A contributing night requires **≥ 1 eligible arm-A pick and ≥ 1 eligible arm-B pick** (§2), so arms A and B are not separate floors — they are jointly the unit, and a thin arm A shows up as *fewer contributing nights*, which the item-3 machinery handles (date moves → single extension → DEFERRED), not as a demotable arm. Arm C is already descriptive (item 1) and the per-`k` cells are already descriptive with a 20-contributing-night SUPPRESSION rule. **No demotion after lock, in either direction** (DP-43). **Discharged at `record` on R1(b)'s measured counts: nothing is demoted.** Both primaries share the one contributing-night floor (23 measured, 80 projected by the window end). The three arm-B bands already clear 20 nights inside the sealed window (23 / 20 / 27), and all four arm-A per-`k` cells (11 / 10 / 8 / 8 nights) project past 20 at their own measured per-cell rates by 2026-11-16 / 2026-11-30 / 2027-01-11 / 2027-01-11 — every one of them before the 2027-03-22 decision date — so no cell is demoted at lock either. Any cell that nevertheless comes up short on `eval.py`'s measured counts at the decision pass is **SUPPRESSED** (counts printed, no point estimate) under §5 and correction 3, which is not a demotion and does not by itself make an endpoint INCONCLUSIVE. Arm C stays descriptive (item 1). | DP-43 (demotion decided at lock, never afterwards); DP-21; PREREG §2 contributing-night definition; R1(b) §2, §6 |
| 17 | The two mandatory composition diagnostics (§10 threats 2 and 3) | DECIDED | **Both stand as drafted, are mandatory rather than discretionary, and neither replaces a primary.** (i) If arm A's bear share exceeds arm B's by **more than 20 pp** on measured counts, the bullish-only direction-restricted contrast is printed **beside** the primaries as a required diagnostic. (ii) If arm A's `passed_at_entry` share exceeds arm B's by **more than 10 pp**, the report **leads with the two bounds**, not with the point estimate. Both thresholds were fixed before any outcome was read and are not tunable at the decision pass; both are computed by the same `eval.py` run. | DP-26 (registrar-chosen thresholds stand, not derived from sealed outcomes); rule 9; PREREG §10 threats 2, 3 |

## Corrections to silent choices

Applied by the Registrar with the rest (`@registrar apply Q013`), after R1 returns.

- **§5 "Decision date" bullet — replace the rolling exposure-driven rule with DP-43's fixed form
  (item 3).** Delete "the evaluation runs on the **first Monday on or after 2027-03-01** on which the
  Steward's counts-only refresh shows …" and the **"Hard stop: 2027-09-06"** sentence. §5 states
  instead: a **window end**, a **decision date**, a **single automatic DP-13 extension date** and
  **DEFERRED thereafter**, all four computed at `record` from R1(b)'s measured contributing-night rate
  by DP-43's recipe (window end + 20 sessions maturity + one-week freeze margin, first Monday on or
  after; extension = window +30 sessions, recomputed), with **Monday 2027-03-01 as a floor the
  projection may push out but never pull in**. Keep the seasonality note as the reason the rate must
  be *measured* rather than assumed, and keep "gates fire on `eval.py`'s measured counts, never on a
  projection or a run-rate" and "no interim looks". Add DP-43's **12-month ceiling**: a projected
  initial decision date after **2027-09-13** means Q013 is **not locked** and goes to
  `research/questions/DEFERRED.md` with the date and the measured rate named. (DP-43; DP-13; item 3.)
  **The four dates are now fixed and are not conditional — write them into §5 verbatim from
  `## Schedule`:** window **pick nights 2026-06-01 .. 2027-02-12**; **decision date Monday
  2027-03-22**; **single automatic DP-13 extension** to pick nights **.. 2027-03-30**, decided
  **Monday 2027-05-10**; **DEFERRED thereafter; no hard stop.** The ceiling test is passed
  (2027-03-22 is inside 2027-09-13), so §5 records that Q013 locks rather than deferring.
- **§8 clause 1 — the shortfall cascade must name the extension, not a hard stop.** "if either is
  short, the decision date moves under the §5 exposure-driven rule, and DEFERRED follows at the hard
  stop" reads: *if either is short at the decision date, the single automatic DP-13 extension fires on
  `eval.py`'s measured counts; if a gate is still short after that one extension, Q013 goes to
  DEFERRED.* The rest of the clause (gates do not weaken; a shortfall is not INCONCLUSIVE) is
  unchanged. (DP-13; DP-43; item 3.)
- **§8 INCONCLUSIVE bullet — a SUPPRESSED sub-cell must not make the question unfalsifiable.** As
  drafted the bullet ends "or a required sub-cell below 20 contributing nights", while §5 *expects*
  the bear and 90+ cells to be SUPPRESSED — read literally, no verdict could ever be reached. Align
  with the locked Q007 §8 wording (and the Q011 correction): a sub-cell below floor is **SUPPRESSED**
  (counts printed, no point estimate) and does **not by itself** make the endpoint INCONCLUSIVE. The
  stratification protection stays exactly where rule 7 puts it — clause 5 (same sign in both calendar
  halves) and clause 6 (no tape stratum, regime cell or reporting-season block **with ≥ 20
  contributing nights** beyond MPE in the opposite sign) — neither of which is weakened. (DP-21;
  Q007 §8 clause 1; Q011 correction 2.)
- **Header line and §5 exposure bullet — print R1's measured counts once they exist.** "**Measured
  exposure:** none yet" and the §5 "No measured exposure count exists" paragraph are replaced at
  `record` by `research/reports/STEWARD_Q013_exposure.md`'s funnel, eligible arm-A / arm-B / arm-C
  counts, contributing nights, per-`k` cells, B2 control-set distribution and monthly rate. The
  EXPLORE_001 §G April–May figures stay in the file **only** with their existing label — in-sample,
  pre-fix, outside the window, **not a projection**. (DP-43; R1(b).) **The numbers to paste:** 48
  matured non-excluded nights 2026-06-01..2026-08-12; funnel 383 published → 375 (−8 no swing lane)
  → 371 (−4 `outcome_target_invalid`) → **371 eligible** (0 removed for mixed direction, missing
  `C_t`/`O_1`, < 14 ATR bars or immaturity); **arm A 44 / arm B 137 / arm C 190**, `dtn` non-null on
  all 371 (no arm-C row entered for the null/unresolvable reason); **23 contributing nights of 48**;
  per-`k` nights A 11/10/8/8 (k = 0/1/2/3) and B 23/20/27 (4–7 / 8–13 / 14–20); **B2 never binds** —
  every one of the 181 arm-A/B picks matched its full 10 controls, 0.0% below the 3-control floor,
  per-night eligible control pool min 37 / median 54 / max 60; **B3 is thin**, 13.3% of picks below
  3 controls (A 27.3%, B 8.8%), which is why it cannot carry a primary (item 2); monthly contributing
  rate **10.0% (June) → 70.0% (July) → 87.5% (August, partial)**, blended **0.4510/session**; one
  matured night (2026-06-02) has zero eligible picks, the same no-swing-lane cause Q011 records.
  Also paste the two composition diagnostics as counts (§10 threats 2–3, item 17): **bear share
  A 4.5% vs B 2.9% (gap 1.6 pp, 20 pp trigger not tripped)** and **`passed_at_entry` A 4.5% vs
  B 0.7% (gap 3.8 pp, 10 pp trigger not tripped)** — measured on the sealed window only, printed as
  counts, deciding nothing, and **re-evaluated by `eval.py` on the full window at the decision pass**,
  which is the pass that fires the diagnostics.
- **§10 threat 1 — record the R1(a) result.** The threat stays in the file (it is why `eval.py`
  reprints the check), but its "unverified" framing is replaced by the R1(a) **PASS** and its evidence
  (live-path write at platform SHA `fa70688b`; seasonal phase mix 83% → 19% → 71% → 87%; non-null
  coverage 98–100%; `created_at` 20:00–22:00 UTC on 98.5% of rows, the two exceptions already
  excluded), plus the two disclosures in the header block: timestamps read from the frozen parquet's
  own `created_at`/`updated_at` because `$RESEARCH_DB_URL` was unset, and `earnings_phase_subtag`
  100% null by code path, used descriptively only. **No rule-14 exception is requested or granted;
  DP-05 is untouched.** (rule 14; DP-41; item 11.)
- **§5 DP-31 sentence — restate against measured numbers.** "The window below supplies far more than
  30 by construction, so DP-31 does not apply" is an assertion without an exposure count. At `record`
  it reads with R1(b)'s projected post-lock contributing nights printed; if that projection does not
  clear **30**, the window end moves out under item 3 until it does — **DP-24 is never reduced and
  DP-31 is never invoked to rescue a short window** here, because the hypothesis is not about the
  sealed period. (DP-24; DP-31 scope; DP-43.) **Settled at `record`:** at 0.4510/session the 30
  post-lock contributing nights project to **2027-01-25**, comfortably before the 2027-03-22 decision
  date, so the post-lock clause is **not** the binding gate (the 80-night floor is) and the window end
  did not have to move for it. **DP-31 does not apply and Q013 is not `HISTORICAL_ONLY`** —
  PROSPECTIVELY_CONFIRMED is reachable from this run by design, and no successor replication question
  is needed. §5 prints the 2027-01-25 projection with the standing caveat that the gate itself fires
  on `eval.py`'s measured post-lock count, never on this projection.
- **§11 "Open decisions before lock" — delete the section entirely** once the above are applied;
  nothing may read as open at lock. After applying, `grep` the file for `open decision`,
  `Recommendation:`, `hard stop`, `2027-09-06`, `exposure-driven` and `required sub-cell` — every hit
  must be gone or deliberate.
- **Status line and `state.json` — bookkeeping.** The Status line drops "DRAFT … open items in §11 are
  resolved by `@decision-maker decide Q013`" and records the lock; the controller advances Q013 to
  `PREREG_LOCKED --by desk` and writes `schedule.json` from `## Schedule` in the same step (DP-46).
  The Decision-maker edits neither file.

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is
edited):** none new. Two standing ones are repeated only so Q013's F4 arithmetic is read with them in
view — (a) Q006/Q007 include pick night **2026-06-26**, which `exclusions_v003.json` now excludes
(already flagged in Q009's and Q011's DECISIONS.md; Q013 uses v003); (b) Q004 §2's looser publication
predicate (`selected_rank` only) versus DP-28, which Q013 follows. **Not a conflict:** Q007 §5 keeps
its locked rolling exposure-driven decision rule while Q013 takes DP-43's fixed form — DP-43 is dated
after Q007's lock and governs new questions only; Q007 is not edited.

## Defaulted on Haci's behalf

- #3 window, decision date and extension — chose DP-43's fixed recipe computed at `record` from the
  Steward's measured contributing-night rate: **window pick nights 2026-06-01..2027-02-12, decide
  Monday 2027-03-22, one automatic extension to ..2027-03-30 / Monday 2027-05-10, then DEFERRED**;
  not taken: rolling Monday checks to a 2027-09-06 hard stop — DP-43. **Computed at record against
  R1(b)'s blended 0.4510 nights/session: the drafted floor of Monday 2027-03-01 moved OUT by three
  weeks and nothing was pulled in.** Overturn = successor question.

## Routed requests

### data-steward

**R1 — CLOSED 2026-09-13.** Returned in full as `research/reports/STEWARD_Q013_exposure.md`:
**(a) PASS** (live-path writes, no rule-14 exception needed, DP-41 branch does not fire);
**(b) returned** (23 contributing nights of 48, 0.4510/session blended, floors inside the ceiling).
The request text is kept verbatim below as the record of what was asked; it is no longer outstanding
and **no longer blocks the lock**. The original text:

**R1 — knowledge-time verification and exposure count for Q013 (earnings proximity, H-064). Blocking:
Q013 cannot lock without it.** On the frozen data only (`research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json`), pick nights **2026-06-01** through the last night with a
matured 20-session forward window, non-excluded per `research/data/exclusions_v003.json`
(`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪
`uncorroborated_publication_runs.trading_dates`), published picks under the DP-28 predicate
(`qualified IS TRUE AND selected_rank IS NOT NULL`), with a
`public_payload_json.lane_plans.swing_trading.targets[0]` present (L3):
**(a) Knowledge-time check on the arm label.** Confirm that `days_to_earnings_corrected`,
`earnings_phase`, `earnings_phase_subtag` and `earnings_event_risk_corrected` on `sas_candidates` rows
with `trading_date ≥ 2026-06-01` are **live-path writes** at scoring time (volatilx
`services/super_agent_select_service.py:396-402`, `services/super_agent_select_scoring.py:1436-1444`)
and **not** the Phase-0b backfill (`scripts/rescore_sas_earnings_corrected.py`, whose source file
`data/sp500_earnings_2026-01-05_to_2026-05-30.json` ends 2026-05-30 and would write `NO_UPCOMING` /
null across the sealed window if it had been re-run over it). Evidence wanted: the `earnings_phase`
distribution **by month**, the share of non-null `days_to_earnings_corrected` **by month**, the
row-level `created_at` / `updated_at` pattern for those columns, and whether any sealed-window row
carries a timestamp or config hash consistent with a post-hoc rescore rather than the 16:05 ET write.
**(b) Exposure, counts only.** The §2 funnel (published rows → null-ladder → `outcome_target_invalid`
→ mixed-direction / missing `C_t` / < 14 ATR bars → missing `O_1` → immature < 20 forward sessions →
**eligible picks**); eligible **arm-A** (`0 ≤ k ≤ 3`), **arm-B** (`4 ≤ k ≤ 20`) and **arm-C**
(`k > 20`, or `dtn` null / `NO_WINDOW`) picks, where `k` = trading sessions from the pick night to the
first session on or after `trading_date + days_to_earnings_corrected` calendar days on the SPY
calendar; **contributing nights** on Q013's definition — a matured non-excluded night carrying **≥ 1
eligible arm-A pick and ≥ 1 eligible arm-B pick, each with ≥ 3 valid matched controls**; the per-`k`
cells (k = 0/1/2/3 and 4–7 / 8–13 / 14–20) with their night counts; the **B2 control-set size
distribution** (10 nearest same-night non-published rows on beta60 / atr_pct / runup20 from
`prices_daily_split` bars ≤ t) and the **share of picks with < 3 valid controls**; the same two
figures for the **B3 arm-matched** pool; the **`passed_at_entry` count per arm**
(`dir × (L3 − O_1) ≤ 0`); the **bear share per arm**; and **contributing nights per month**, plus the
monthly contributing-night rate per session, so the seasonal clustering is visible rather than
averaged away. **Protocol (binding): counts only.** Session t+1's official open/high/low may be read
for the `passed_at_entry` and control-set counts; for sessions ≥ 2 only the **existence** of bars
(maturity/coverage) may be checked, never their values. **No touch of any level, no return, no MAE, no
P&L, no picks-minus-control difference and no outcome of any kind may be computed or reported** — the
same discipline as `STEWARD_Q011_exposure.md` and `STEWARD_Q009_exposure.md` §R1. Definitions: `C_t` =
the actual pick-night regular-session close from `prices_daily_split` (never `spot_close`); ATR14 from
`prices_daily_split` bars ≤ t (never the platform's `atr_pct`, PI-003); `dir` = +1 bullish / −1 bearish
from `dominant_direction`.
**What it decides.** (a) **Whether Q013 exists at all:** if the sealed-window earnings columns are not
point-in-time, the arm label needs a new rule-14 exception; under **DP-41** the desk grants none and
Q013 goes to `research/questions/DEFERRED.md` (exception named: `sas_candidates`,
`days_to_earnings_corrected` / `earnings_phase`, 16:05 ET on the pick night) instead of locking.
(b) **The whole §5 schedule** (DECISIONS.md item 3, DP-43): the measured contributing-night rate fixes
the window end, the decision date (first Monday on or after window end + 20 sessions + one week, never
earlier than Monday 2027-03-01), and the single DP-13 extension (+30 sessions); **if 80 contributing
nights and 30 post-lock contributing nights cannot be projected by 2027-09-13, Q013 is DEFERRED with
that date and the measured rate named, on the H-062 precedent, rather than locked.**

**R2 — OPEN, not a blocker for lock. Due at the decision date now fixed: the successor freezes must
cover pick nights after 2026-09-10 through 2027-02-12 and be built in time for Monday 2027-03-22 (a
second pair covering ..2027-03-30, for Monday 2027-05-10, only if the DP-13 extension fires).**
Paste-ready:

**R2 — successor freezes for Q013 (DP-23).** Build and pin the successor selection freeze (same SQL,
same exclusion criterion as v001) and the successor price freeze (same Alpaca queries) covering pick
nights after **2026-09-10** through Q013's registered window end (**2027-02-12**), with the daily symbol list extended
to **every candidate on every new night, published and unpublished** — B2 needs the unpublished
symbols' pick-night closes, prior bars for beta60/atr_pct/runup20, session-t+1 opens and forward bars
— **plus hourly bars for published symbols** (the §4 counter-direction tie-break), carrying **20**
forward sessions beyond the last included pick night (**40** where the descriptive 40-session
companion is to be computed), and please fix the exact session-count decision date from the trading
calendar at the same time. Nights whose unpublished-candidate bars are missing are excluded from the
primaries and **counted, never back-filled**; control pairs that hourly bars cannot order fall to
DP-27 (counter-level-first) and are counted.

### registrar (conditional) — **VOID, did not fire**

**R1(a) returned PASS on 2026-09-13, so this route is void and no `DEFERRED.md` entry is written for
H-064.** Kept for the record only; the Registrar takes no action on it. The original text:

**If R1(a) shows the sealed-window `days_to_earnings_corrected` / `earnings_phase` values are not
point-in-time:** write the `research/questions/DEFERRED.md` entry for **H-064**, naming the exception
the question would need — table `sas_candidates`, columns `days_to_earnings_corrected` /
`earnings_phase` / `earnings_phase_subtag`, time 16:05 ET on the pick night — the evidence from R1(a),
and what would move it back into the backlog (a point-in-time earnings-date source, or a platform
change that stamps the scoring-time value in a column the backfill cannot overwrite). Q013 is **not**
locked in that branch (DP-41, DP-43).

## Schedule

**Final — computed 2026-09-13 at `record` by DP-43's recipe on R1(b)'s measured contributing-night
rate (0.4510 nights/session, blended over 2026-06-01..2026-08-12).** Written verbatim to
`research/questions/Q013_earnings_proximity/schedule.json` by the Registrar at `apply` / lock (DP-46).

One-line summary for `schedule.json`:
`decision_date: 2027-03-22 · extension_date: 2027-05-10 · hard_stop: none · rule: fixed`

- `window`: pick nights **2026-06-01 .. 2027-02-12** (after `exclusions_v003.json`, whose in-window
  dates are read from the file, not hard-coded; sealed-part exclusions are 2026-06-26, 2026-07-02,
  2026-07-06). Derivation: 23 contributing nights measured through 2026-08-12, 57 still needed for
  DP-21's 80, at 0.4510/session → 127 further sessions → **2027-02-12** (Friday).
- `decision_date`: **2027-03-22** (Monday) — window end 2027-02-12 + **20 sessions maturity** =
  2027-03-15 (2027-02-15 Presidents' Day closed) + **one-week freeze margin** = 2027-03-20 (Saturday)
  → first Monday on or after. This reproduces the Steward's independently computed 2027-03-22 exactly.
  The **80-contributing-night floor is the binding gate**; DP-24's 30 post-lock nights project to
  2027-01-25 and therefore do not move the date out further.
- **Why this rate and not another (DP-43, DP-45).** The blended 0.4510/session is the measured
  whole-window run-rate the Steward reports and is the only figure DP-43's recipe admits. The
  July–August-only rate (0.75/session) is **not used**: it would project the 80-night floor to about
  2026-12-14, i.e. *earlier* than the drafted floor, and DP-43 lets a projection push a date **out**,
  never pull it **in** (Q011 item 8). Reading the June trough (0.10/session) forward instead would put
  the floor outside the ceiling altogether, but that is a worst-case forecast of one month, not a
  measured run-rate, and DP-43 says "the measured run-rate" — the desk does not pre-DEFER a question
  on a forecast. The seasonal risk is handled where it belongs: if the rate really does fall back to
  the trough, the gate comes up short **on `eval.py`'s measured counts** at the decision pass, the
  single DP-13 extension fires, and DEFERRED follows. That path is conservative and needs no guess now.
- **The drafted floor moved out, not in.** PREREG §5's Monday **2027-03-01** was a floor the
  projection may only push later; 2027-03-22 is three weeks later, so it governs. Nothing in this
  schedule is earlier than any date the draft named.
- `extension_date`: **2027-05-10** (Monday) — the window extends **once**, automatically, to pick
  nights **.. 2027-03-30** (= 2027-02-12 + 30 sessions; 2027-02-15 Presidents' Day and 2027-03-26 Good
  Friday closed); 2027-03-30 + 20 sessions = 2027-04-27 + one week = 2027-05-04 (Tuesday) → first
  Monday on or after. Fires on `eval.py`'s **measured counts** only, with the byte-identical `eval.py`
  (DP-13). Where the 365/252 calendar convention and exact session counting disagree by a few days,
  the **later** date is taken (DP-45).
- `hard_stop`: **null** — none. DP-13's single automatic extension, then DEFERRED, replaces the
  draft's 2027-09-06 hard stop (correction 1).
- `rule`: **fixed** · `extended`: **false**
- `ceiling`: **2027-09-13** (12 months from the lock). The initial decision date 2027-03-22 is inside
  it by nearly six months, and even the extension date 2027-05-10 is inside it, so **DP-43's DEFERRED
  branch does not fire and Q013 locks.**
- `gates`: per primary endpoint — **≥ 80 contributing nights** (DP-21, on §2's ≥ 1 eligible arm-A
  **and** ≥ 1 eligible arm-B pick, each with ≥ 3 valid B2 controls) **and ≥ 30 contributing nights
  dated after the lock commit** (DP-24). A shortfall on one endpoint is never covered by the other's
  count; a gate shortfall is **not** INCONCLUSIVE — it fires the single extension, then DEFERRED. No
  floor is lowered and no arm or cell is demoted after lock (item 16).
- `demotions_at_lock`: **none** (item 16, discharged on R1(b)'s counts).
- `note`: _PREREG §5 / DP-43 / DP-13 / DP-21 / DP-24. Every gate is evaluated on `eval.py`'s measured
  counts from the frozen data at the decision pass — never on the projection above, the run-rate, or
  R1. No interim looks; `eval.py` is written once (rule 9) and run once. **Not HISTORICAL_ONLY:**
  PROSPECTIVELY_CONFIRMED is reachable from this run by design, so DP-31 does not apply and no
  successor replication question is drafted. Successor freezes (R2) are due for 2027-03-22 covering
  pick nights 2026-09-11..2027-02-12; a second pair only if the extension fires._

## Standing rules added

_none._ Every item here is settled by an existing `DP` entry, a locked precedent or one defensible
technical answer, and the single DEFAULTED item is an application of DP-43. **No `DP` entry is created
from a DEFAULTED item** — a default is the desk acting on Haci's behalf, not an answer from him
(DP-40); only an answer of his becomes a Confirmed row. **The `record` pass adds none either:**
`research/DECISION_POLICY.md` was read and not edited, and the schedule above is an application of
DP-43 to the Steward's numbers, not a new rule.

## Standing rules proposed

Written down because they would generalise, **not added** to `research/DECISION_POLICY.md`. Each needs
Haci's word (or a later `--ask` cycle) before it becomes a `DP` row.

- **P-3 (would clarify DP-12): DP-12 fires on conditioning variables that are part of the price path,
  not on scheduled calendar events.** A variable known in full at 16:05 ET (an earnings date, an index
  add, a lockup expiry) does **not** require the matched control to be matched on it — matching on it
  would strip out the event under test. The unrestricted distance-matched control stays primary and
  the event-matched pool is descriptive. Rationale: Q013 item 2/9; without it the next earnings-style
  question re-argues DP-12 from scratch.
- **P-4 (would extend DP-43): when a question's contributing-night definition requires two arms to be
  present on the same night, the arms are not separately demotable.** A thin arm shows up as fewer
  contributing nights and is handled by the date machinery (extension, then DEFERRED), never by
  demoting an arm that the estimator cannot do without. Rationale: Q013 item 16; DP-43's demotion
  clause otherwise reads as if it applied.
- **P-5 (would sharpen DP-43): when the Steward's contributing-night rate is strongly seasonal, the
  projection uses the *blended whole-window* rate — never the peak-season sub-rate, and never a
  trough-month forecast.** The peak rate is excluded because it pulls the date in, which DP-43 already
  forbids; the trough is excluded because a one-month worst case is not a measured run-rate, and the
  question would be pre-DEFERRED on a guess. Seasonal downside is carried by the existing machinery: a
  short gate on `eval.py`'s measured counts fires the single DP-13 extension, then DEFERRED. Rationale:
  Q013 `record` — the three candidate rates here spanned 2026-12-14 to "never", and the file should
  not have to re-argue which one to use next time.
- **P-6 (bookkeeping): where the 365/252 session-to-calendar conversion and exact trading-calendar
  counting give different dates, the later one is taken, and the closed sessions are named.** Rationale:
  Q013's extension date (2027-05-03 by conversion, 2027-05-10 by exact count over Presidents' Day and
  Good Friday); consistent with DP-45 and with Q011's record pass, which counted actual sessions.
