# Q012 — decisions before lock
Run: 2026-09-13 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 3 items
(+ items 4–18: the R-class and technical choices the draft made silently, which the Registrar needs
settled when it applies; + item 19, the routed exposure count the draft names as R1)
**`record` pass: 2026-09-13, autonomous, against `research/reports/STEWARD_Q012_exposure.md` (R1,
delivered).** R1 is CLOSED. Its measured counts move **item 5's window end and all three schedule
dates OUT** (P2's both-band floor now binds), confirm **item 6's REF demotion** and leave **ELITE's
SUPPRESSED-or-not to `eval.py`'s own count at the decision pass**. Nothing moved in. No `results/`
directory exists or was read; no parquet, weekly or daily report was opened; `PREREG.md` was not
edited (the Registrar folds this in at `apply`).

**Mode: autonomous (`--autonomous`).** DP-40..48 are in force: **no decision is put to Haci before
lock**. What would have been an ASK is `DEFAULTED` — R-2 → **DP-42**, R-3 → **DP-43**, R-4 → **DP-44**,
R-5 → **DP-45** — otherwise the Registrar's recommendation unless a DECIDE ground gives another
answer (DP-40). Every DEFAULTED item is listed under "Defaulted on Haci's behalf" and goes on the
board; the locked question stands (rule 3) and Haci overturns any of it by asking for a successor
question, never by editing the locked file.

**Summary (after `record`):** **17 DECIDED, 3 DEFAULTED (R-3 window/date, R-3 elite arm, R-2 capital
budget), 0 ROUTED open for lock (R1 CLOSED at `record`; R2 successor freezes is folded into item 16
and is due at the decision date), 0 ASK.** The schedule is final and moved out: **window
2026-06-01..2026-12-10, decide Monday 2027-03-22, one extension to ..2027-01-26 / Monday 2027-05-03,
then DEFERRED.** All three of the draft's open items are settled by a `DP` entry
or one defensible technical answer — none of them was ever a Haci decision; the Registrar's
recommendation (A) is the right answer in all three on independent grounds. Two silent choices are
corrected: the DP-13 extension arithmetic is one session short, and **P2's MPE rises to 0.50 ATR per
slot** because P2 is a difference of differences (Q007 §8 / Q003 §8 precedent, DP-10's larger-value
clause). **Nothing is pending; the file is complete for lock.**

**State note:** `research/questions/Q012_capital_recycling/state.json` reads `PREREG_DRAFT` (advanced
by the Registrar 2026-09-13T21:00Z). The controller advances Q012 to `PREREG_LOCKED --by desk` after
`@registrar apply`, writing `schedule.json` from the `## Schedule` block below in the same step
(DP-46). No `results/` directory exists and none was read; no parquet, no weekly and no daily report
was opened; `PREREG.md` was not edited.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Does Plan R redeploy, or does the slot go idle after the first exit? (draft item 1) | DECIDED | **Option A — recycle.** The slot refills from the same cohort's next eligible pick until the 60-session budget ends, exactly as drafted; the **no-redeploy** version stays **B4, descriptive, printed beside every P1 figure**. H-066's claim *is* capital recycling ("redeploy" is in the hypothesis text); option B tests a different hypothesis and would be a new BACKLOG entry, not a re-unit of this one. The mechanical exposure advantage A hands Plan R is priced by **P3** (the identical machinery on matched controls) and by the printed capital-occupancy counts (§10 threat 1), not assumed away. | DP-25 (the test stays the one that was proposed); DP-29; §10 threats 1 and 6 |
| 2 | Does touches-per-slot carry a verdict? (draft item 2) | DECIDED | **Option A — descriptive only; the money endpoints decide.** Touch counts per slot and the share of slots with ≥ 1 committed-level touch are printed with raw p, marked "descriptive, does not decide"; **m stays 3**. DP-44 gives a count endpoint no MPE and forbids inventing one, and a touch that is not worth money licenses no rule — the whole point of §8's breakeven-cost clause. | DP-44 ("no money-unit MPE is invented"); DP-45 (the stricter of the two); rule 5 (the plan's realized result is what is reported) |
| 3 | Is the `<80` band in the primary population? (draft item 3) | DECIDED | **Option A — no. Primaries are 80 ≤ score < 90 only.** `<80` (**REF**) is reported descriptively against an **explicitly labelled 80-85 stand-in** hold schedule and never enters a primary; §1, §8 and §9 bind the report to say the verdict speaks for 80–90 only. The platform's committed plan for `<80` is literally *"not traded"* (volatilx `scripts/generate_sas_trading_guide.py:94`), so option B would contrast Plan R against a baseline the platform never printed — no baseline, no rule-5 comparison — and would credit the recycle arm with the band whose near targets are nearest. | rule 5 (a baseline that exists); DP-25; DP-45 (option B is the one that makes CONFIRMED easier); §10 threat 7 |
| 4 | The MPEs (silent, §8: "0.25 ATR on each of P1, P2 and P3") | DECIDED | **P1 = 0.25 ATR per capital slot. P3 = 0.25 ATR per capital slot. P2 = 0.50 ATR per capital slot** — see Corrections. P1 and P3 are level contrasts in per-trade ATR units and take the standing number unchanged (DP-10, DP-44), with the **slot as the trade unit** (one slot = one capital-allocation decision, both plans consuming the identical 60 sessions) — the draft's justification is correct and is not re-asked. **P2 is a difference of differences** (HIGH's plan gap minus LOW's plan gap) measured on the thinner both-band nights, which is exactly the shape Q007 §8 raised its MPE for (10.0 pp = 2 × DP-20, "difference of differences with small cells", Q003 §8 precedent); DP-10 permits a larger value with a one-line reason and never a smaller one. All three two-sided; a result beyond MPE with the opposite sign is a confirmed finding with that sign. **No MPE is asked and none is invented in money units.** | DP-10; DP-44; DP-20 (the uplift precedent's shape); Q007 §8; Q003 §8; DP-45 |
| 5 | Window, decision date, DP-13 extension and DEFERRED fallback (silent §5; **R-3**) | **DEFAULTED — settled at `record` on R1's measured run-rate; every date moved OUT** | **Window: slot-start nights 2026-06-01 .. 2026-12-10** (was ..2026-11-20; after `exclusions_v003.json`, start ≥ 2026-06-01 per DP-06). **Decision date: Monday 2027-03-22** (was 2027-03-01). **Extension: start nights ..2027-01-26, decide Monday 2027-05-03** (was ..2027-01-07 / 2027-04-19). Then **DEFERRED**; no second extension, no gate reduced, and a gate shortfall is never INCONCLUSIVE. **Why it moved:** DP-43 sizes the window on **every** primary endpoint's floor, and R1 measures **P2's both-band nights at 42 of 67 sessions, 0.6000/session** — the 80th both-band start night projects to **2026-12-10**, three weeks past the drafted window end, so the drafted 2027-03-01 date would have printed P2 INCONCLUSIVE (floor) with the sample sitting two weeks away. P1/P3 (0.9429/session → 80th night ≈ 2026-10-01, matured 2027-01-04) and the 30 post-lock nights (2027-02-01) are **not binding**. **Arithmetic (exact NYSE sessions, not the 365/252 approximation):** 2026-12-10 + 60 sessions = **2027-03-10** (2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15 closed) + one-week freeze margin = 2027-03-17 → first Monday on or after = **2027-03-22**; R1's 2027-03-15 used the calendar approximation (its 2027-03-07 is a Sunday) and the exact count is **later**, so the later date stands. 2026-12-10 + 30 sessions = **2027-01-26**; + 60 sessions = **2027-04-22** (2027-03-26 Good Friday closed) + one week = 2027-04-29 → **Monday 2027-05-03**. Both inside DP-43's 12-month ceiling (**6.3** and **7.7** months from lock). Gates unchanged, per primary endpoint on `eval.py`'s measured counts: **≥ 80 contributing start nights** (P2: both-band nights) **and ≥ 30 dated after the lock commit**. Projection at the new end: ≈ 81 both-band nights (clears 80 by about one night — thin, which is exactly what DP-13's automatic extension exists for; +30 sessions adds ≈ 18 more) and ≈ 123 LOW-or-HIGH nights, of which ≈ 59 post-lock (P2: ≈ 38 post-lock both-band). A date **moves out, never in** (DP-43, DP-45); the Steward may move it out again when building the successor freezes. | DP-43 ("through the earliest date at which **every** primary endpoint's contributing nights are projected ≥ 80"); DP-13; DP-21; DP-24; DP-45; R1 §4(b); **not taken:** keeping 2027-03-01 and printing P2 INCONCLUSIVE (floor) two weeks short |
| 6 | Does the ELITE (90+) arm carry a verdict? (silent §1/§5; **R-3**) | **DEFAULTED** | **No — ELITE is demoted to descriptive at lock and SUPPRESSED below 20 contributing nights.** DATA_NOTES measures 12 / 8 / 3 / 2 elite picks per month since June, so the cohort is projected far below the 20-night sub-cell floor at any date inside DP-43's 12-month ceiling; DP-43 demotes such an arm **at lock**, never after. **BH stays at m = 3** so no surviving endpoint's bar falls. H-066's elite half therefore carries **no verdict here** and needs its own PREREG once elite counts allow; §1, §8 and §9 already say so and the Registrar keeps that wording. **REF (`<80`)** is descriptive by item 3 and is SUPPRESSED under the same floor. R1 confirms the counts at `record`; because both cohorts are already descriptive, R1 **does not block the lock**. **Settled at `record` against R1 §5:** the demotion **stands unchanged for both cohorts** (DP-43 demotes at lock and never restores afterwards, so no measurement can promote them). **REF is confirmed** far below the floor and structurally so — **1 contributing night**, 1 of 579 published rows below 80 (TJX 2026-06-11, 79.58), publication sitting at an effective ~80 gate: REF is **SUPPRESSED**, printed as a bare count with the sentence that the labelled 80-85 stand-in has essentially nothing to describe (Correction below). **ELITE is not confirmed below 20** — R1 measures **exactly 20** contributing nights through 2026-09-09 on a declining monthly trend (10 / 6 / 3 / 1), so its **SUPPRESSED-or-printed status is genuinely undetermined and is decided at the decision pass on `eval.py`'s own measured count against the 20-night sub-cell floor** (≥ 20 → printed, descriptive, no verdict; < 20 → SUPPRESSED). Either way ELITE carries **no verdict** in Q012 and **BH stays at m = 3**, so nothing in the design turns on it. §5's "projected far below 20" sentence is replaced by R1's measured counts (Correction below). | DP-43 ("demoted to descriptive at lock, never dropped afterwards"); DP-21; R1 §5; Q009 / Q011 item 9 (m unchanged by a demotion); **not taken:** waiting for elite to reach 20 nights (outside the 12-month ceiling) |
| 7 | The capital budget and the unit of capital-time (silent §4; **R-2**) | **DEFAULTED** | **60 sessions, identical for both plans, one slot = one unit of capital committed on the start night; `r_slot` in additive ATR, each trade in its own pick's ATR; idle time contributes 0.** Sixty is the platform's own long-lane window (`services/sas_conviction_card.py:194`), the shortest budget in which Plan H — which puts 30–50% of a sub-elite position at L5/L6 — can **complete**. The **20-session-budget** version is printed descriptively and **labelled truncated**, never as a primary. Plan R's own 5-session per-trade cap is H-066's (DP-25) and is unchanged. | DP-42 (lane and horizon from the hypothesis / the platform's own window); DP-45 (the shorter budget truncates the baseline and flatters the hypothesis); DP-25; **not taken:** a 20-session budget that truncates the hold arm |
| 8 | Entry basis (silent §2) | DECIDED | **Session t+1 official regular-session open `O_1` (`prices_daily_split.o`) for every trade, picks and B2 controls alike** — DP-03(b), and H-066's own "enter at the actionable price". **DP-11 does not apply**: no position is already held when the signal appears (Q012 opens the slot on the signal). `C_t` (the DP-03(a) after-hours proxy) and `E_AH` (Q004's definition verbatim, picks only) stay **B3, descriptive**, printed so Q012 reconciles with Q007 and Q009 and never deciding. The entry is held fixed across both plans, so any entry effect differences out of P1 and P2. | DP-03(b); DP-11 (scope: already-held positions); DP-25; Q004 / Q011 own the entry-basis contrast (DP-29) |
| 9 | Exclusions file | DECIDED | **`research/data/exclusions_v003.json`** — the newest file (DP-22) — read by `eval.py` as `manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪ `uncorroborated_publication_runs.trading_dates`, **no date hard-coded** in the PREREG or in `eval.py`. In the sealed part of the window that is 2026-06-26, 2026-07-02, 2026-07-06. If the Steward issues `exclusions_v004.json` **before** Q012 locks, the draft cites that file instead; after lock the cited file stands and is never edited. A matured start night on which no slot survives the funnel is a **non-contributing night, not an exclusion** — it is never added to the exclusions file (the 2026-06-02 shape from Q011 R1). | DP-22; Q009 item 20; Q011 item 11 |
| 10 | Publication predicate | DECIDED | **`qualified IS TRUE AND selected_rank IS NOT NULL`** for every treatment row and every refill pick; dark-lane and `qualified = false` rows are never treatment rows and form the **B2 control pool complement** exactly as drafted. Unchanged from the draft, confirmed against DP-28 so the Registrar does not have to re-derive it. | DP-28; Q006 §3; Q008 draft finding |
| 11 | L1 vs L2 touched in the same session, or no hourly bars (§4 ordering rule 1) | DECIDED | **Exit at L1 — the nearer level, the reading less favourable to H-066** — applied identically wherever `prices_hourly_raw` cannot order the pair (one bar holding both, or no hourly bars for that symbol, which is the normal case for B2 control chains: `p001_hourly_raw` is scoped to the 227 published-pick symbols, Q011 R1 §4.4). The count of trades resolved by the rule is printed per arm and the opposite reading is printed as a **named sensitivity**. Missing hourly bars are never back-filled. Plan H needs no ordering (each fraction exits at its own level price). | DP-27 (the outcome less favourable to the hypothesis); DP-45; Q011 item 3 |
| 12 | Status of the rule-5 distance-matched control (B2) and of P3 | DECIDED | **P3 — published picks' recycle slots minus their B2 matched-control recycle slots — is a primary, and it is what satisfies rule 5 for this question.** P1 and P2 are within-night **paired** contrasts of two plans on the same picks and the same tape, so they carry no hit-rate-without-control hazard; their control-adjusted difference-in-differences is printed beside them, descriptively. Construction is **Q006 §3 / Q002 B1 verbatim** (10 nearest same-night non-published candidates on `beta60` / `atr_pct` / `runup20`, standardized by the night's median and MAD, Euclidean, with replacement, ties by symbol ascending), with synthetic levels at the pick's **ATR distances** anchored at the control's own close, graded from the control's own t+1 open and own bars. **Control rows never add to inferential n** (rule 6). Post-match standardized mean differences are printed at every chain start (§10 threat 14). | rule 5; rule 6; Q006 §3; Q002 B1; Q011 item 12 |
| 13 | Does DP-12 fire (a control matched on a path-derived conditioning variable)? | DECIDED | **No.** Q012 conditions on nothing that lives in the forward path: the cohort is the score band, the levels, ATR, direction and every stratum are fixed at 16:05 ET on the start night, and **every eligible pick enters both plans**. Exits, refills, truncation and idle time are **execution and outcome measurement** — the status Q007 §6.1 and Q011 §6 give a fill and a gap-through touch — not conditioning; the refill picks the list published at 16:05 ET on the night the slot happens to be flat, which is a decision a trader could take at that moment, never a choice among later nights made with hindsight. No arm is formed from a session-t+1-or-later event. | DP-12 (scope); rule 14; Q007 §6.1; Q011 items 13 and 16 |
| 14 | Knowledge time — is a rule-14 exception needed? | DECIDED | **No. Q012 requests no rule-14 exception and DP-05 is untouched** (DP-41 respected — the desk grants none in autonomous mode, and none is needed). `eval.py` must compute the eligible-pick set, both plans' parameters, cohort assignment, the B2 matches, the refill ordering key and every stratum label into a frozen per-pick table **before any session-t+1-or-later bar is loaded**, and **fail loudly** if a t+1-or-later field is referenced in any of them. `sas_selection_excursion` / `outcome_*` / `level_hit_*` are never inputs (recomputed weeks later on a different calendar and close basis); **`uoa_symbol_daily.fwd_return_*` is banned** and no UOA table is read (FREEZE_v001 §5 — the freeze is not fixed). Regime labels only for start nights ≥ 2026-06-09, `regime_version = 'v1.2'`, same-evening rows only; 2026-06-01..06-08 stratified by the SPY proxy and flagged. | rule 14; DP-41; DP-05; FREEZE_v001 §5 and §7; Q011 item 16 |
| 15 | Family, within-question correction, and the two-family requirement | DECIDED | **F6 Exits and execution**, per DP-29 (family follows the primary endpoint's subject — both money primaries contrast two *exit plans* on the same picks), with H-066 **re-filed from F7 and not counted in both**; the Q009 re-filing is the precedent. **BH across m = 3 within the question** (P1, P2, P3) at q ≤ 0.10, **m = 3 in every branch** — an endpoint short of its floor still has its p computed and included, so no surviving endpoint's bar is lowered (Q009 / Q011 precedent). The draft's **strict two-family rule stands**: the Reporter also computes the **F7 companion q** (Q002 3 + Q004 2 + Q011 4 + these 3) and a CONFIRMED verdict requires **q ≤ 0.10 in both** families, the larger q quoted — the stricter reading of rule 8 for a question that moved family. Overlaps with Q002 (speed), Q006 (per-level control profile) and Q009/Q010 (F6 stops) are cross-referenced and **never counted as a second confirmation**. | DP-29; DP-45; rule 8; Q009 §7; Q011 item 15 |
| 16 | Successor freezes, and what blocks the lock | DECIDED | **Lock now, pinned to `manifest_v001` / `manifest_prices_v001`.** `manifest_v002` (selections) and `manifest_prices_v002` (prices) are built and pinned **at the decision date** (routed **R2**, below), with the two scope requirements this question cannot do without: (i) the **selection** freeze covers pick nights through **2027-03-10** (2027-04-22 if the DP-13 extension fires) — updated at `record` with the window end; because slots started at the window end are refilled from picks published after it — a short selection freeze silently idles those slots and understates Plan R (§10 threat 13), and `eval.py` prints the count of refills that found no freeze row; (ii) the **price** freeze carries **every candidate symbol, published and unpublished** (B2 chains need the unpublished opens and forward bars) **plus hourly bars for published symbols**, through **60 forward sessions** beyond the last start night. A second pair only if the extension fires. `eval.py` takes window, manifest paths, exclusions path and output directory as **inputs** — no hard-coded dates, names or paths — so one byte-identical script serves both runs and records every sha256. **Neither successor freeze blocks the lock, and R1 does not block it either** (item 6: the two cohorts R1 could demote are already descriptive). | DP-23; DP-46; Q006 §5; Q009 item 2; Q011 item 14 |
| 17 | Is this question HISTORICAL_ONLY? | DECIDED | **No — DP-31 does not apply and no successor replication question is required.** PROSPECTIVELY_CONFIRMED is reachable from this run by design: the **63** post-lock sessions **2026-09-14..2026-12-10** project **≈ 59** contributing start nights (and **≈ 38 both-band nights for P2**) against DP-24's 30 at R1's measured rates, and the window is not a sealed-period window. _(Updated at `record` from the draft's "50 sessions … ≈ 42"; the new window end raises both figures — §5 and §8 take the new numbers.)_ The gate is decided on `eval.py`'s measured counts, never on that projection; a shortfall fires the single DP-13 extension and then DEFERRED — it is **not** an INCONCLUSIVE verdict and DP-24's 30 is never reduced to fit the window. | DP-24; DP-31 (scope); DP-13; Q011 item 8 |
| 18 | Inference specification | DECIDED | **Stands as drafted, fixed before any result:** stationary block bootstrap over the ordered contributing start nights, expected block length **20 sessions** (60-session budgets overlap heavily across adjacent start nights, §10 threat 3 — a longer block than the desk's other path questions and a **wider** CI, chosen for that reason), 2,000 resamples, the date-clustered CI printed alongside; **paired sign-flip permutation** on the night contrasts, 10,000 permutations, **seed 20260913**. Every estimate prints n(contributing start nights), n(post-lock), n(slots), n(trades), n(refills), n(truncated), n(idle), n(not takeable), n(unfillable fractions), n(hourly-unresolved L1/L2 pairs), n(control chains), n(excluded by reason). Slots and trades are printed **separately from n** so nobody reads a slot count as inferential n (§10 threat 4). | rule 6; DP-26 (registrar-chosen conventions stand as drafted, not derived from sealed outcomes); §10 threats 3 and 4 |
| 19 | Exposure count for this population (draft §5 R1) | **DECIDED — R1 CLOSED 2026-09-13** (`research/reports/STEWARD_Q012_exposure.md`) | **Delivered, counts only, no outcome.** What it settled: **(a)** the all-six-levels funnel is **not** materially narrower than Q011's — 16 of 541 rows removed (3.0%) vs Q011's 2.1%; **517 eligible picks, 495 LOW-or-HIGH, 66 of 67 contributing nights** (§10 threat 12 is priced and does not bite); **(b)** P2's both-band nights are **42 of 67 (62.7%)**, gated by HIGH-band publication (LOW is present on 98.5% of sessions), so the window and all three dates move out per item 5; **(c)** REF confirmed at 1 night, ELITE at exactly 20 and declining — item 6; **(d)** **hourly coverage 100%** (461/461 picks with a complete 5-session window, 2,391/2,391 pick-sessions, all 167 symbols inside the hourly universe), so item 11's ordering rule resolves from bars for the whole published population and its conservative fallback should be a near-empty count — **the successor price freeze must again scope hourly bars to at least the published symbols** (folded into R2 below); **(e)** refill supply: LOW idle-risk 1 of 67 sessions, **HIGH idle-risk 25 of 67 (37.3%)**, so idle-session accounting (§4) will bind on some HIGH chains and its counts must be printed per arm, not aggregated. Funnel A (11 fully-matured nights today) is a freeze-horizon fact, not a population defect, and is the reason R2 exists. **Nothing here decides an endpoint and nothing moved a date in.** | R1 §§1–8; DP-43; DP-21; item 5; item 6; item 11 |
| ~~19-prior~~ | _(the routed request as issued, kept for the record)_ | ROUTED → data-steward (fulfilled) | waited on the counts-only funnel: how many published picks carry **all six** committed levels, eligible picks and contributing start nights per month split LOW / HIGH / ELITE / REF, **both-band nights** (P2's floor unit), hourly-bar coverage on the first five sessions after each start night, and eligible same-cohort refill picks available per session. Decides nothing by itself: it confirms or **moves out** (never in) the item 5 dates, confirms item 6's demotions, and prices §10 threat 12. **Does not block the lock.** | — |

## Corrections to silent choices

Applied by the Registrar with the rest. **The first four are the `record` pass's corrections and
supersede the two extension-arithmetic bullets issued at `decide`** (those dates were computed off
the old window end and are void).

- **§5 — the primary window end and the decision date move out.** "slot-start nights 2026-06-01 ..
  **2026-11-20**" becomes "… **2026-12-10**", and "Decision date: **Monday 2027-03-01**" becomes
  "Decision date: **Monday 2027-03-22**". Reason in one sentence, to be written into §5: *DP-43 sizes
  the window on every primary endpoint's floor, and R1 measures P2's both-band nights at 0.6000 per
  session, putting the 80th both-band start night at 2026-12-10.* Arithmetic to write out: the 60th
  session after 2026-12-10 is **2027-03-10** (2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15 closed),
  + the one-week freeze margin = 2027-03-17 → first Monday on or after = **2027-03-22**. Every
  "2027-02-22" in §5 as the *refill horizon* becomes **2027-03-10**. Keep the sentence that the
  Steward fixes the exact session-count date when building the successor freezes, and keep "**out,
  never in**". (Item 5; DP-43; DP-45.)
- **§5 — the DP-13 extension dates follow the new end.** "start nights 2026-06-01 .. **2027-01-06**"
  becomes "… **2027-01-26**" (= 2026-12-10 + 30 sessions: 14 in December, 16 in January with 01-01
  and 01-18 closed), and decision date "**Monday 2027-04-12**" becomes "**Monday 2027-05-03**"
  (2027-01-26 + 60 sessions = **2027-04-22**, 2027-03-26 Good Friday closed; + one week = 2027-04-29
  → first Monday on or after). "5.6 and 7.0 months from lock" becomes "**6.3 and 7.7 months from
  lock**, inside DP-43's 12-month ceiling". (Item 5.)
- **§5 — the extension trigger is any primary endpoint, not P1 alone.** The draft fires the single
  DP-13 extension only "if **P1's** gates are short". DP-13's text is "**if any gate … per primary
  endpoint** is short at the decision date, the window extends once" — and Q012's window is now sized
  on **P2's** floor, so restricting the trigger to P1 would print P2 INCONCLUSIVE on a one- or
  two-night miss with the sample a few weeks away. §5 reads: *the single automatic extension fires if
  **any** of P1, P2, P3 is short of either gate on `eval.py`'s measured counts*. Unchanged after the
  extension: **P1 still short → DEFERRED**; **only P2 and/or P3 still short → those endpoints
  INCONCLUSIVE (floor)**, the question runs on the rest, BH across m = 3 regardless. No gate is
  reduced and there is no second extension. (DP-13; DP-21; DP-45; item 5.)
- **§5 — the projection paragraph is replaced by R1's measured counts; the 0.85 haircut goes.** The
  "haircut to ≈ 0.85 contributing start nights per session" and the Q011-derived 0.9216 rate are
  superseded by Q012's own measured rates: **0.9429 LOW-or-HIGH contributing nights per session
  (66 of 67 sessions eligible-population)** and **0.6000 both-band nights per session (42 of 67)**,
  with the funnel at **517 eligible picks of 541** and the all-six-levels test removing only 3.0%
  (§10 threat 12 answered, cite `research/reports/STEWARD_Q012_exposure.md` §§2–4). Projected at the
  new window end: **≈ 123 contributing nights (P1/P3)**, **≈ 81 both-band nights (P2 — clears 80 by
  about one night; the DP-13 extension is the stated remedy)**, **≈ 59 post-lock contributing nights
  and ≈ 38 post-lock both-band nights** against DP-24's 30. Keep the sentence that every gate is
  decided on `eval.py`'s measured counts, never on a projection or on R1. (Item 5; item 19.)
- **§5 / §1 / §8 — ELITE's status line is a measurement, not a projection.** "**ELITE** is projected
  at ≈ 2–3 picks per month (DATA_NOTES) → far below 20 contributing nights" is wrong as stated: R1
  measures **exactly 20 ELITE contributing nights** through 2026-09-09 on a declining monthly trend
  (10 / 6 / 3 / 1). The text becomes: *ELITE is **descriptive at lock** under DP-43 and carries no
  verdict; whether it is **printed or SUPPRESSED** is decided at the decision pass on `eval.py`'s own
  count against the 20-night sub-cell floor (R1 measures 20 through 2026-09-09, trend declining).*
  BH stays at m = 3 either way. (Item 6; R1 §5 and caveat 4.)
- **§2 / §3 — REF's stand-in gets its measured size.** Add: *REF (`< 80`) is **1 of 579 published rows
  in the window** (TJX 2026-06-11, score 79.58) — publication sits at an effective ~80 gate, so the
  labelled 80-85 stand-in schedule has essentially nothing to describe. REF is **SUPPRESSED** under
  the 20-night floor and printed as a bare count.* (Item 3; item 6; R1 §5 and caveat 3.)
- **§4 — print the idle-session counts per arm, not aggregated.** R1 §7 measures HIGH-band refill
  supply missing on **25 of 67 sessions (37.3%)** against LOW's 1 of 67, so Plan R's idle time is a
  HIGH-side phenomenon that an aggregate count would hide. §4's idle-slot sentence adds: *n(idle
  sessions) and n(idle slots) are printed **separately for LOW and HIGH**, beside the capital-occupancy
  counts of §10 threat 1.* (Item 1; item 18; R1 §7.)
- **§4 ordering rule 1 — record that the fallback is expected to be near-empty for picks.** R1 §6
  measures **100% hourly coverage** (2,391 of 2,391 pick-sessions, 0 of 167 symbols missing) on the
  first five forward sessions, so item 11's conservative L1 reading should apply almost only to B2
  control chains. Keep the rule and the printed count exactly as decided; add the measured coverage
  as the reason the count is expected to be small on the picks side. (Item 11; R1 §6.)
- **§8 (and §4's P2 line, and anywhere the MPE is restated) — P2's MPE is 0.50 ATR per capital
  slot, not 0.25.** The draft sets "0.25 ATR per capital slot on each of P1, P2 and P3". P1 and P3
  are level contrasts and keep DP-10's standing 0.25; **P2 is a difference of differences** (HIGH's
  plan gap minus LOW's plan gap) on the thinner both-band nights, which is the exact shape Q007 §8
  raised its MPE for (10.0 pp = 2 × DP-20, "a difference of differences with small cells", citing
  Q003 §8). DP-10 permits a larger value with a one-line reason; the reason is that sentence. Write
  it in **§8's MPE paragraph, §8's clause 2 (`|m2| > 0.50 ATR per slot`) and §4's P2 bullet**, and
  keep §8's two-sidedness and the opposite-sign clause unchanged. No new number is invented and no
  money-unit MPE appears anywhere (DP-44). (Item 4.)
- **Header — the status line.** "**Status:** DRAFT (lock by committing this file) — three items are
  open, listed at the end and settled by `@decision-maker decide Q012`" becomes the locked-file form,
  with **Decisions: DECISIONS.md** cited as in Q011's header. Nothing may read as open at lock.
- **§4 secondary bullet (touches per slot) — delete the pointer to an open decision.** "(see the open
  decision on whether this endpoint carries a verdict; as drafted it does not — DP-44 …)" becomes the
  settled ruling: *"descriptive, raw p only, does not decide; m stays 3 (DECISIONS.md item 2,
  DP-44)."* (Item 2.)
- **§10 threat 7 — same.** "(see the open decision)" becomes *"settled: `<80` is descriptive against a
  labelled 80-85 stand-in and never enters a primary (DECISIONS.md item 3)."* (Item 3.)
- **"Open decisions before lock" — delete the section entirely.** After applying, `grep` the file for
  `open decision`, `Recommendation:`, `2027-01-06`, `2027-04-12`, `2026-11-20`, `2027-03-01`,
  `2027-02-22`, `2027-04-05`, `haircut`, `0.85`, `far below 20` and `0.25 ATR per capital slot on
  each` — every hit must be gone or deliberate. (`2027-02-22` survives only if it is *not* used as
  the refill horizon or a decision-date input; the new refill horizon is **2027-03-10**.)
- **`research/BACKLOG.md` bookkeeping (Registrar).** H-066 is still `[ ]` under F7. Mark it
  **registered as Q012** with the PREREG path, and note that it is **re-filed to F6 under DP-29** and
  is **not counted in F7's family arithmetic** — while §7's F7 *companion* q still includes its 3
  primaries, which is a stricter reporting requirement, not a second family membership. (DP-29;
  item 15.)

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is
edited):** none new. Q004 §2's looser publication predicate (`selected_rank` only, vs DP-28) and
Q006/Q007's inclusion of pick night 2026-06-26 remain flagged in Q007's, Q009's and Q011's
DECISIONS.md; they are repeated here only so Q012's F7 companion arithmetic is read with them in
view. If Haci later confirms the DiD-MPE-uplift rule proposed below, **Q009's** and **Q011's** ATR
endpoints should be re-read for DiD shapes by the Red Team — the locked files stand either way.

## Defaulted on Haci's behalf

- #5 window and decision date — chose start nights 2026-06-01..**2026-12-10**, decide **Monday
  2027-03-22**, one automatic extension to ..2027-01-26 / **Monday 2027-05-03**, then DEFERRED; not
  taken: deciding 2027-03-01 with P2 short — DP-43. Overturn = successor question.
  _(Moved out three weeks at `record`: the Steward measures P2's both-band nights at 0.6/session, so
  the 80-night floor is not reached by the old window end. Three weeks of waiting buys P2 a verdict.)_
- #6 elite (90+) arm — chose demotion to **descriptive at lock**, printed-or-SUPPRESSED decided at the
  decision pass on the 20-night floor, BH still m = 3, so H-066's elite half carries no verdict here;
  not taken: waiting for elite to reach 20 nights — DP-43. Overturn = successor question.
- #7 capital budget — chose a **60-session budget for both plans**, slot = one unit of capital, ATR
  per slot; not taken: a 20-session budget truncating the hold arm — DP-42. Overturn = successor
  question.

## Schedule

**FINAL — filled at `record` (2026-09-13) from R1's measured counts
(`research/reports/STEWARD_Q012_exposure.md`). Every date moved OUT of the `decide` provisional;
none moved in (DP-43, DP-45).** Written verbatim to
`research/questions/Q012_capital_recycling/schedule.json` by the Registrar at `apply` / lock (DP-46).

- `decision_date`: **2027-03-22** (Monday) — window end **2026-12-10** + **60 sessions** (the slot
  budget, the binding maturity) = **2027-03-10**, with 2026-12-25, 2027-01-01, 2027-01-18 and
  2027-02-15 closed, + one-week freeze margin = 2027-03-17 (Wednesday) → first Monday on or after.
  Was 2027-03-01 at `decide`; **moved out three weeks** because P2's 80th both-band night projects to
  2026-12-10 at R1's measured 0.6000 both-band nights per session (R1 §4(b)). R1's own 2027-03-15 used
  the 365/252 calendar approximation (its 2027-03-07 is a Sunday); the exact NYSE session count is a
  week later and the later date stands.
- `extension_date`: **2027-05-03** (Monday) — window extends **once** to start nights ..**2027-01-26**
  (= 2026-12-10 + 30 sessions, DP-43: 14 sessions in December, 16 in January); 2027-01-26 + 60
  sessions = **2027-04-22** (2027-03-26 Good Friday closed), + one week = 2027-04-29 → first Monday on
  or after. Fires **automatically**, on `eval.py`'s measured counts only (DP-13), with the
  **unmodified** `eval.py`, if **any** of P1, P2, P3 is short of either gate.
- `hard_stop`: **null** — none. DP-13's single automatic extension, then DEFERRED, replaces it.
- `rule`: **exposure-driven** — the window end and both dates are set by R1's measured run-rate
  against the DP-21 floors (P2's both-band nights binding), not by a calendar choice; the Steward's
  successor-freeze calendar check may move them **out** again, never in.
- `extended`: **false**
- `window`: slot-start nights **2026-06-01..2026-12-10** (after `exclusions_v003.json`; in-window that
  removes 2026-06-26, 2026-07-02, 2026-07-06). Refill picks are drawn from pick nights inside each
  slot's 60-session budget, i.e. through **2027-03-10** (2027-04-22 if the extension fires), and add
  **no** contributing nights and **no** inferential n.
- `gates`: per primary endpoint, on `eval.py`'s measured counts — **≥ 80 contributing start nights**
  (P1 and P3: a start night with ≥ 1 gradeable LOW-or-HIGH slot; **P2: a both-band night**) **and
  ≥ 30 contributing start nights dated after the lock commit** (DP-24). A shortfall on one endpoint is
  never covered by another's count. **Any of P1/P2/P3 short → the single automatic extension**
  (DP-13). After the extension: **P1 still short → DEFERRED** (not INCONCLUSIVE); **only P2 and/or P3
  still short → that endpoint is INCONCLUSIVE (floor)**, counts only, and **BH still runs across
  m = 3**.
- `projection_at_lock` (mechanical, gates nothing; from R1 §4): ≈ **123** contributing start nights
  (P1/P3) and ≈ **81** both-band nights (P2) at the window end; ≈ **59** post-lock contributing nights
  and ≈ **38** post-lock both-band nights against DP-24's 30. P2 clears its floor by about one night —
  thin by construction, since DP-43 sets the window at the *earliest* date the floor is projected to
  be reached; DP-13's automatic +30 sessions (≈ 18 further both-band nights) is the stated remedy and
  needs no new decision.
- `sub_cell_status_at_lock`: **REF SUPPRESSED** (1 contributing night measured, structural — R1 §5);
  **ELITE undetermined**, descriptive at lock either way, printed only if `eval.py` measures ≥ 20
  contributing ELITE nights at the decision pass (20 measured through 2026-09-09, trend 10/6/3/1).
  Neither carries a verdict; **m = 3** regardless.
- `note`: _PREREG §5 / DP-43 / DP-13 / DP-21 / DP-24. Gates are evaluated on `eval.py`'s measured
  counts from the frozen data at the decision pass, never on the projection above or on R1.
  `eval.py` runs **once**; no interim looks. **Not HISTORICAL_ONLY — PROSPECTIVELY_CONFIRMED is
  reachable from this run by design** (item 17; DP-31 does not apply, no successor replication
  question needed). Both dates sit inside DP-43's 12-month ceiling (**6.3** and **7.7** months from
  lock), so Q012 is **not** DEFERRED. Routed **R2** (successor freezes `manifest_v002` /
  `manifest_prices_v002`, selection scope through the refill horizon **2027-03-10**) is due at
  `decision_date`; a second pair only if the extension fires. Routed **R1** is **closed** —
  `research/reports/STEWARD_Q012_exposure.md`, 2026-09-13._

## Routed requests

### data-steward

**R1 — CLOSED 2026-09-13, delivered as `research/reports/STEWARD_Q012_exposure.md`.** Its counts are
folded into items 5, 6, 11, 19 and the Corrections above; the Registrar applies them at `apply`. The
request as issued is kept below for the record — **no further Steward work is outstanding before the
lock.**

**R1 (as issued) — exposure-only count for Q012 (due before the successor freezes are built; earlier
if the cycle allows, in which case `@registrar apply` folds the counts into §2/§5 before the lock.
It does **not** block the lock).**

On the frozen data only (`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`),
for the exact Q012 §2 population — published picks under the DP-28 predicate (`qualified IS TRUE AND
selected_rank IS NOT NULL`), non-excluded nights per `research/data/exclusions_v003.json`
(`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪
`uncorroborated_publication_runs.trading_dates`), pick nights ≥ 2026-06-01, with `overall_score`
present and a bullish/bearish `dominant_direction` — please report **counts only**: **(1)** the §2
funnel to *eligible* picks, step by step — published/matured rows → rows missing any of the three
`public_payload_json.lane_plans` (`day_trading`, `swing_trading`, `longterm_trading`) → rows missing
any of the **six** committed levels `L1,L2 = day_trading.targets[0..1]`, `L3,L4 =
swing_trading.targets[0..1]`, `L5,L6 = longterm_trading.targets[0..1]` (please break out **how many
published picks carry all six**, and separately how many carry a lane but not its *second* target,
which no registered question has measured yet) → rows with any of the six at or through the
pick-night close `C_t` on the wrong side (`dir × (L_i − C_t) ≤ 0`) → rows with `outcome_target_invalid`
non-null → symbols with fewer than 60 daily bars dated ≤ t → rows with no session t+1 bar →
**eligible picks**; **(2)** eligible picks and **contributing start nights** (a start night with ≥ 1
eligible pick) **per month and in total, split LOW (80 ≤ score < 85) / HIGH (85 ≤ score < 90) /
ELITE (score ≥ 90) / REF (score < 80)**, with the matured-night count and the last matured pick
night, and the resulting contributing-nights-per-session run-rate; **(3)** the number of
**both-band nights** — start nights carrying ≥ 1 eligible pick in **each** of LOW and HIGH — per
month and in total, which is P2's own floor unit and the binding uncertainty in §5; **(4)**
**hourly-bar coverage** in `prices_hourly_raw` on the **first five sessions after each start night**
for eligible published symbols (how many trades §4 ordering rule 1 can resolve from hourly bars),
plus confirmation of the successor freeze's hourly symbol scope; **(5)** the count of eligible
**same-cohort** picks published per session (LOW and HIGH separately), i.e. how many sessions inside
a 60-session budget offer at least one refill candidate — this sets how often a Plan R slot goes
idle. Definitions: `C_t` = the actual pick-night regular-session close from `prices_daily_split`
(never `spot_close`); `ATR` = ATR14 from `prices_daily_split` bars dated ≤ t (never the platform's
`atr_pct`, corrupted around splits); `dir` = +1 bullish / −1 bearish from `dominant_direction`.
**Protocol (binding): counts only.** Everything above is computable from the payload, `C_t`, `ATR`,
the trading calendar and bar *presence*. **No bar value dated after the pick night may be used to
compute a touch, a return, a P&L, a plan result, an excursion or any picks-minus-control difference,
and no outcome of any kind may be reported** — the same counts-only discipline as
`STEWARD_Q011_exposure.md` and `STEWARD_Q009_exposure.md` §R1. Bar *coverage* counts under (4) and
maturity counts under (2) are coverage facts, not outcomes, and are the only forward-looking items.

What it decides: **(a)** whether the all-six-levels requirement — stricter than any registered
question has measured (§10 threat 12) — leaves the eligible population near Q011's funnel or well
below it; **(b)** whether **P2's both-band nights** can reach the 80-night floor by the decision
date, or whether P2 is heading for INCONCLUSIVE (floor) while P1 and P3 run (DECISIONS.md item 5,
DP-21); **(c)** confirmation of item 6's ruling that ELITE and REF sit below 20 contributing nights
and are therefore **descriptive at lock** (DP-43) — both are already descriptive, so this cannot
change the design, only the printed counts; and **(d)** whether the measured run-rate leaves the
window 2026-06-01..2026-11-20 and the decision date 2027-03-01 where DP-43's recipe puts them, or
moves them **out** (never in).

**R2 — successor freezes (REISSUED at `record` with the new window; due at the decision date
**2027-03-22**; a second pair only if the DP-13 extension fires, then due **2027-05-03**. Not a
blocker for lock).** Build and pin `manifest_v002` (selections; same SQL, same exclusion criterion)
and `manifest_prices_v002` (same Alpaca queries) covering pick nights after 2026-09-10, with three
scope requirements Q012 cannot do without: **(i)** the **selection** freeze must run through
**2027-03-10** — 60 sessions *past* the last start night **2026-12-10** (the window end moved out
from 2026-11-20 at `record`, on your own R1 both-band rate) — because slots opened at the window end
are refilled from picks published after it, and a freeze that stops at the window end silently idles
them and understates Plan R (§10 threat 13); **(ii)** the **price** freeze must carry **every
candidate symbol on those nights, published and unpublished** (the B2 control chains need the
unpublished symbols' closes, t+1 opens and forward bars), carrying **60 forward sessions** beyond the
last start night, i.e. through **2027-03-10**; **(iii)** **hourly bars scoped to at least the
published-pick symbols**, as `manifest_prices_v001` was — R1 §6 measured 100% hourly coverage
(2,391 of 2,391 pick-sessions) on the first five forward sessions and §4's ordering rule 1 depends on
it; if that scope changes, say so, because the conservative fallback count then stops being
near-empty. Please also fix the exact session-count dates from the trading calendar at the same time
(the desk's arithmetic gives 2026-12-10 + 60 sessions = 2027-03-10, + one week → **Monday
2027-03-22**, and 2026-12-10 + 30 = 2027-01-26, + 60 = 2027-04-22, + one week → **Monday
2027-05-03**, with 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15 and 2027-03-26 closed; a correction
may move a date **out**, never in). Control symbols with no hourly bars fall to §4 ordering rule 1's
stated reading and are **counted**, never back-filled; nights whose unpublished-candidate bars are
missing are excluded from B2 and counted. Please also re-report, at the same pass, the ELITE
contributing-night count on the full window — R1 §5 leaves it at exactly 20 and declining, and
whether it is printed or SUPPRESSED is decided there on `eval.py`'s count. (DP-23; DP-43; R1 §§4–6.)

## Standing rules added

_none._ **The `record` pass adds none either** — every date it moved came out of DP-43's own recipe
applied to R1's numbers, and item 5 is a DEFAULTED item, not Haci's word. Every item here is settled
by an existing `DP` entry, a locked precedent or one defensible technical answer, and the three
DEFAULTED items are applications of DP-42 and DP-43. **No `DP` entry is created from a DEFAULTED
item** — a default is the desk acting on Haci's behalf, not an answer
from him (DP-40); only an answer of his becomes a Confirmed row.

## Standing rules proposed

Written down because they would generalise, **not added** to `research/DECISION_POLICY.md`. Each
needs Haci's word (or a later `--ask` cycle). P-1 and P-2 were proposed in Q011's DECISIONS.md and
are not restated; Q012 applied both again (item 5's "out, never in"; item 9's non-contributing
night).

- **P-3 (would extend DP-10 / DP-20): a difference-of-differences endpoint carries twice the standing
  MPE for its metric type.** 10.0 pp where DP-20 gives 5.0 pp; 0.50 ATR where DP-10 gives 0.25 ATR.
  Rationale: Q007 §8 already did this for a touch-rate DiD citing Q003 §8, and Q012 item 4 has now
  done it for an ATR DiD; a DiD subtracts two noisy contrasts and is usually measured on the thinner
  intersection of both cells, so the same bar on a DiD is a materially weaker bar. Writing it once
  stops each Registrar re-arguing the uplift, and stops a DiD silently inheriting the level-contrast
  number.

Added at the `record` pass:

- **P-4 (would sharpen DP-43 and DP-13): the window is sized on the *binding* primary endpoint, and
  the single DP-13 extension is triggered by *any* primary endpoint.** When the Steward's measured
  run-rate puts one primary endpoint's floor **after** the drafted decision date, the window end moves
  out to that endpoint's floor date rather than the endpoint being written off as INCONCLUSIVE
  (floor); and the automatic extension fires on a shortfall in **any** primary endpoint, not only the
  headline one. Rationale: Q012 P2's both-band nights (0.6000/session, a *pair* of bands per night)
  reach 80 three weeks after the P1 unit does — a question with a paired-cell endpoint always has a
  slower-filling floor, and the drafted schedule would have thrown that endpoint away for three weeks
  of waiting. DP-43 already says "every primary endpoint" and DP-13 already says "any gate … per
  primary endpoint"; writing the consequence down stops the next draft narrowing both to P1 by
  habit. Cost, stated honestly: every question with a paired-cell endpoint decides later.
- **P-5 (bookkeeping): the exact NYSE session count governs a maturity date; the 365/252 calendar
  conversion is a projection aid only, and where they disagree the later date stands.** Q012's own
  R1 put the P2 floor's maturity at 2027-03-07 (a Sunday) by the 365/252 route; the exact count is
  2027-03-10, a week further on in Monday terms. Rationale: the conversion is fine for ranking
  candidate dates in an exposure report but is not a calendar, and "out, never in" (DP-43, DP-45)
  already tells the desk which of the two to keep — saying so once stops the two arithmetics being
  argued question by question.
