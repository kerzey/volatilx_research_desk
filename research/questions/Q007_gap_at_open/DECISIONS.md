# Q007 — decisions before lock
Run: 2026-09-12 by decision-maker · Source: PREREG.md "Open decisions before lock", 7 items (item 4
split into 4a/4b; items 8–9 registrar-silent; items 10–11 raised by the Steward's returned routes)
Recorded: 2026-09-12 — Haci answered A and B; both generalised (DP-09, DP-10).
Recorded: 2026-09-12 (second pass) — routed requests R1/R2/R3 returned; the R-3 item they raised (the
hard stop vs the per-arm 80-contributing-night floor) was put to Haci and answered as question C.
No ASK items remain open; R4 remains outstanding by design (it is built at the decision date).
Recorded: 2026-09-13 (**third pass, on the redrafted PREREG**) — Haci changed the entry basis from the
next-session open to the **pick-night close** in another session; the Registrar redrafted Q007 around
it (new §4.1, new §10 threat 13, two new open items) and applied part of this file before stopping.
Items 12–17 below decide the redraft; item 9 is **superseded**. One ASK is open (question D).
Recorded: 2026-09-13 (**fourth pass**) — Haci answered **D** ("strip the gap out" → **variant B is
primary** for P1 and P2; A and C descriptive; §6.1 is **not** widened). The R5 route then returned
(`research/reports/STEWARD_Q007_exposure.md` §R5) and put both arms past the 2027-03-31 stop under
variant B; that R-3 went to Haci as **question E**, answered **"hard stop Jun 30, 2027"**. Items
18–20 record the consequences; item 10's date is **superseded** by item 20. **No ASK items remain
open**; R4 is still outstanding by design (built at the decision date). Q007 is ready for
`@registrar apply Q007` and lock.

State note: `research/questions/Q007_gap_at_open/state.json` does not exist yet and `PREREG.md` is
uncommitted — the question is pre-lock (PREREG_DRAFT) and these decisions are in scope. The state
file is initialised by the controller (registrar/coordinator), not here.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Successor freezes (`manifest_v002`, `manifest_prices_v002`) | DECIDED | Lock Q007 **now**, pinned to `manifest_v001` / `manifest_prices_v001`; the successors are built and pinned at the decision date, with symbol scope = **every candidate on the new nights, published and unpublished**, plus hourly bars for published symbols (needed for the secondary race's tie-breaks). §5's existing clause stands: if a successor price freeze omits unpublished-candidate symbols, those nights are excluded from P1 and counted, never back-filled. Build order is in "Routed requests" but does **not** block the lock. | DP-23; Q006 §5; Q004 §5 |
| 2 | Exposure-only arm count | ROUTED → data-steward → **DONE** (`research/reports/STEWARD_Q007_exposure.md`, R2) | Counts returned on 49 matured nights: AGAINST 22 contributing nights, FAVOUR 20, union 35; projections to 80 contributing nights are AGAINST **2027-02-22**, FAVOUR **2027-03-21**, union 2026-11-14. Both arms projected past the draft's 2027-01-25 hard stop, which is the R-3 trade-off put to Haci as question C. **Answer: hard stop extended to 2027-03-31; both arms stay primary as drafted** — no arm is dropped, Q007 is not deferred. | R-3 → question C (Haci 2026-09-12) |
| 3 | Arm definitions | DECIDED | **Signed arms** (AGAINST `g ≤ −2.0`, FAVOUR `g ≥ +2.0`) as drafted, not a single `|g| ≥ 2%` arm; the **2% cut in percent**, not ATR (H-030's own figure, as written); **FLAT = `|g| < 1.0`**; MIDDLE (1–2%) descriptive only; the ATR-unit version (`g_ATR`, ±0.25) stays a secondary, descriptive, because those thresholds are EXPLORE_001 figures. A gap-through at entry is never a hit. | DP-25; DP-26; PREREG §2 |
| 4a | MPE for P1 (touch-rate, control-adjusted) | DECIDED | **10.0 pp stands as drafted.** DP-20's 5.0 pp is a floor that is never reduced; P1 is a *difference of differences* ((arm − its controls) − (FLAT − its controls)), and the locked precedent for a difference-of-differences is a larger MPE (Q003 §8 used 8.0 pp for the same estimand shape). Where two answers differ only in strictness, the stricter is taken. | DP-20; Q003 §8 |
| 4b | MPE for P2 (ATR units per trade) | ASK → ANSWERED | **0.25 ATR per trade** (Haci 2026-09-12, question B). Applies to P2-A and P2-F and to every per-trade ATR-denominated endpoint hereafter. | R-4 → DP-10 |
| 5 | Primary horizon: L3 within 20 sessions vs the platform's 40-session L3 window | ASK → ANSWERED | **L3 within 20 sessions** is the primary clock (Haci 2026-09-12, question A); the platform's 40-session L3 window is reported alongside, descriptively, wherever it has matured. All four primaries (P1-A/P1-F/P2-A/P2-F), their sample floors and the §5 maturity/decision-date arithmetic use the 20-session window. | R-2 → DP-09 |
| 6 | 2026-07-02 / `exclusions_v002.json` | ROUTED → data-steward → **DONE** (`research/data/exclusions_v002.json` issued; `research/data/DATA_NOTES.md` updated) | The file exists and carries all four KT-audit re-run nights. **DECIDED: the PREREG cites `exclusions_v002.json`** — header, §2 exclusions bullet and `eval.py` read that file; the v001 + "PREREG-cited 2026-07-02" fallback is dropped. Only 2026-07-02 differs inside Q007's ≥ 2026-06-01 window, so the population is unchanged (Steward confirms the R2 counts were computed on exactly this population). | DP-22; KT audit §7 |
| 10 | Hard stop vs the DP-21 per-arm floor (raised by R2) | ASK → ANSWERED → **date superseded by item 20** | **Hard stop moves from 2027-01-25 to ~~2027-03-31~~ → 2027-06-30 (item 20, Haci 2026-09-13, question E); both arms (AGAINST and FAVOUR) stay primary as drafted** (Haci 2026-09-12, question C, reaffirmed 2026-09-13). The exposure-driven decision-date *rule* in §5 is kept unchanged in form — the first Monday on or after 2026-10-26 on which every retained arm shows ≥ 80 contributing nights (DP-21 reading) — only the hard stop date moves. No arm is dropped to descriptive; Q007 is not deferred. | R-3 → Haci 2026-09-12 |
| 11 | §10 threats 4 and 5 (price basis, earnings point-in-time) | ROUTED → data-steward → **DONE** (`research/reports/STEWARD_Q007_exposure.md`, R3) | **DECIDED: both are marked verified in §10.** Threat 5 (official open / extended-hours) **PASS 40/40** on hourly cross-check, with the stated hourly-granularity caveat and the DST hazard (`eval.py` must compute the 09:30/16:00 ET boundary per date with `zoneinfo`, not a fixed UTC offset — a fixed offset mis-flagged 2 of 40 pre-DST dates). Threat 4 (`days_to_earnings_corrected`) **PASS on code-path evidence for trading_date ≥ 2026-06-01**, i.e. Q007's whole window, so the earnings stratum **is** computed (§6's "otherwise not computed" branch does not fire); the report states the evidence is code-path, not a per-column timestamp. | R3 report; §10.4, §10.5 |
| 7 | H-063 overlap | DECIDED | **Mark H-063 "merged into Q007" in `research/BACKLOG.md`** (registrar edits BACKLOG when applying); H-063's ATR-scaled gap buckets and its L3-before-(−1 ATR) race remain Q007 secondaries, descriptive. F4 keeps 7 hypotheses but H-063 is not counted as a second registered question in the family correction. | DP-29; PREREG §7 |
| 8 | Primary level = L3 (not listed as open; confirmed) | DECIDED | L3 stays the primary level — it is the strike Haci sells and it is the primary level in the locked Q006 and Q004. Only the *horizon* (item 5) is his. | Q006 §4; Q004 §4 |
| 9 | Entry basis | ~~DECIDED~~ **SUPERSEDED 2026-09-13 → see item 12** | ~~Next-session official open only (no after-hours arm here): the gap is defined at the open and the open is the entry price.~~ Decided against the earlier open-basis draft; overtaken by Haci's own later instruction to measure from the pick-night close (2026-09-12, recorded in the PREREG header and §6.1). The rest of the row still holds: the Rule-14 exception (§6.1) is the existing one, narrowed, and is not extended, so no new R-1 arises from the basis itself. | superseded by Haci 2026-09-12; see item 12 |

## Third pass — the redrafted (close-basis) PREREG, 2026-09-13

Source: PREREG.md as redrafted 2026-09-12 — "Open decisions before lock" items **8** and **9** (new),
plus the §4 "Stale decision, not applied" flag the Registrar sent back, plus §10 threat 13. The
Registrar's partial `apply` has already folded in the header, `exclusions_v002`, the 2027-03-31 hard
stop, the MPEs, the 20-session clock and §10 threats 4/5; it stopped before removing the
"Open decisions before lock" section.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 12 | Entry basis (re-decide; PREREG §4 "Stale decision, not applied") | DECIDED — **Haci-confirmed**, supersedes item 9 | **Pick-night close `C_t` from `prices_daily_split`, for picks and controls alike**, as the proxy for the DP-03(a) pick-night after-hours entry; the real after-hours price `E_AH` (Q004's definition verbatim) stays a **picks-only descriptive sensitivity** that never decides. Haci's own instruction of 2026-09-12 ("I want to measure the movement of the stock from closed price of previous day not opening prices"; "Keep gap groups, measure from close") governs: a desk pass cannot revert a recorded instruction from him. It is also the only basis the question can have — H-030's "subsequent realized return" on a **held** pick presumes the position existed before the gap appeared, and rule 5 requires the distance-matched control to be graded on the same basis, which only the close offers (after-hours prints cover 227 published symbols and no unpublished candidate). The §6.1 Rule-14 exception stays **narrowed to gap-group assignment**; the t+1 open is not an entry price, so no new R-1 arises. §4's "Stale decision, not applied" paragraph is deleted and replaced by one line citing this item. | Haci 2026-09-12; DP-03(a); rule 5; **DP-11** (new); DP-09 (wording generalised) |
| 13 | §4.1 primary variant A / B / C (draft open item 8) | ASK (question D) → **ANSWERED** | **Variant B — the gap-matched same-night B3 control — is the primary definition of P1 and P2** (Haci 2026-09-13: *"Strip the gap out"*). Variants **A and C are reported descriptively** and never decide. **§6.1's rule-14 exception is not widened** (C was not chosen), so no new R-1 arises and DP-05 stands unchanged. See items 18–20 for what the Registrar applies. | Haci 2026-09-13, question D → **DP-12**; R-1 closed (exception not widened) |
| 14 | Q004 overlap — separate BH families vs joint correction (draft open item 9) | DECIDED | **Separate.** Q004 stays in F7 and Q007 in F4, BH is applied within each family, exactly as drafted. Rule 8 defines the families in `research/BACKLOG.md` and DP-29 assigns a question to a family by its primary endpoint's subject — Q004's subject is the entry basis (F7), Q007's is the path after selection (F4). A joint correction would have to be applied to every F4×F7 pair on overlapping nights, i.e. to almost every registered question, and it is not the right instrument for shared nights anyway: the hazard is **non-independence**, not multiplicity. It is handled where it already is — §10 threat 11's standing sentence that the two results are never presented or counted as two confirmations, and the Reporter's cross-reference duty. §7's "unless Haci decides otherwise (open decision 9)" is deleted. | rule 8; DP-29; Q004 §7; PREREG §10.11 |
| 15 | §10 threat 13 — disclosing that the basis switch was not blind to sealed data | DECIDED | The switch is **defensible independent of** weekly 2026-09-12 line 29: that line is an unconditional L1 touch-rate comparison, carries no gap conditioning and no L3 figure, and the close basis is forced by the hold/exit/add framing and by rule 5's same-basis control requirement (item 12) — it is DP-03(a), a basis registered before the figure existed. It is nonetheless a design choice made with sealed-period knowledge, so it is **disclosed, and it weakens the historical track only**: nights already inside the pinned freeze at the switch (pick nights 2026-06-01..2026-09-10) were observable when the basis was chosen; nights after the lock commit were not, so **PROSPECTIVELY_CONFIRMED is unaffected**. Exact wording in "Corrections", including the `DESIGN_CHOICE_NOT_BLIND` label that must travel with any HISTORICALLY_CONFIRMED verdict. | rule 3; rule 10; DP-03(a); PREREG §6, §10.13 |
| 16 | MPE consequence if variant A is chosen | DECIDED → **scope narrowed by item 19** (item 13 = B, so the offset never touches a primary) | **The MPEs do not move: P1 10.0 pp (item 4a, DP-20) and P2 0.25 ATR (DP-10, not re-asked).** But under A the arm−FLAT difference contains the gap's own displacement, which for a 2% gap is a sizeable fraction of an ATR and can exceed 0.25 ATR by construction — an MPE below a known mechanical offset would make CONFIRMED reachable without any information in the signal. So **under variant A only**, P2's decision threshold in §8 becomes `\|m2(arm)\| > 0.25 ATR + \|Δgap_ATR(arm)\|`, where `Δgap_ATR(arm) = mean_t [ mean_{p∈arm,t}(dir×(O_{t+1,p}−C_{t,p})/ATR_p) − mean_{p∈FLAT,t}(same) ]` is computed from the pick-night close and the t+1 open only (inputs already permitted by §6.1, never an outcome) and is printed as a headline number per arm. DP-10's 0.25 ATR is unchanged as the *incremental* MPE; this is the "larger MPE with a one-line reason" DP-10 provides for. P1's mechanical part has no arithmetic offset in pp, so P1 keeps 10.0 pp and §8's arm-level reading (a CONFIRMED A licenses no management rule) carries it. Under B the displacement cancels and under C it is isolated in C1, so no offset applies there. | DP-10; DP-20; PREREG §4.1, §8, §10.2 |
| 17 | Is variant B reachable? (B3 control availability) | ROUTED → data-steward (R5) → **DONE** (`research/reports/STEWARD_Q007_exposure.md` §R5, 2026-09-13) | **Reachable, but later than the old stop.** Of the eligible picks, **85.1% of AGAINST (40/47) and 85.7% of FAVOUR (30/35)** have ≥ 3 same-group non-published controls (median 7 and 10; FLAT 201/201, min 11, so the FLAT side never binds). **Variant-B contributing nights on the 49 matured nights: AGAINST 18, FAVOUR 15, union 29** (vs 22 / 20 / 35 under the exposure-only count), projecting to 80 on **2027-04-23 (AGAINST)**, **2027-06-28 (FAVOUR)**, union 2026-12-19 — both arms past the then-current 2027-03-31 hard stop. That is the R-3 trade-off the route anticipated; it went to Haci as **question E** and was answered **"hard stop Jun 30, 2027"** → item 20. No arm is dropped, the floor is not loosened, Q007 is not deferred. | R5 report §R5(a)–(d); DP-21; R-3 → Haci 2026-09-13 |

**What R5 decided.** Exactly the branch it anticipated: Haci picked B (question D), the Steward's count
showed variant-B contributing nights projecting past the 2027-03-31 hard stop for both arms, so the
waiting-vs-sample trade-off went **R-3, back to Haci** with the numbers attached (question E). It was
not resolved by the desk and the floor was not loosened.

## Fourth pass — question D answered, R5 returned, question E answered, 2026-09-13

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 18 | Primary variant — what the Registrar applies (from item 13) | DECIDED — **Haci-answered** | **Variant B is the primary definition of P1 and P2 for all four primary endpoints (P1-A, P1-F, P2-A, P2-F).** Controls are **B3** as drafted in §3: same-night non-published candidates whose own gap, direction-adjusted with the pick's direction, falls in the pick's own group, nearest ≤ 10 on `beta60`/`atr_pct`/`runup20` from bars dated ≤ t, targets placed and graded exactly as B2 with the same E-L3 plan from their own close. `x_p` and `r_p` are pick minus its B3 control mean; the night contrast is arm minus FLAT of those differences. **The ≥ 3-control rule stands exactly as drafted in §3/§4.1: if fewer than 3 controls exist in the restricted pool, that pick's B3 value is missing, the pick is dropped from the night's arm (or FLAT) mean and the drop is counted and printed per arm.** A night is a contributing night only if it carries ≥ 1 eligible arm pick **with a valid B3 set** and ≥ 1 eligible FLAT pick **with a valid B3 set** (the R5 definition). **Variants A and C are reported as descriptive figures that never decide**; §4.1 keeps their full specification. §6.1 is unchanged — the t+1 open still enters for gap-group assignment only, now also for B3 control grouping as §3 already says, and no session-t+1 outcome is ever a classifier (C stays descriptive precisely because it would need that). | Haci 2026-09-13, question D → DP-12; PREREG §3 (B3), §4.1 variant B; DP-05 (unwidened); rule 5 |
| 19 | Scope of item 16's variant-A displacement offset | DECIDED | **The offset survives, but only on the descriptive side.** Since variant B is primary, `Δgap_ATR(arm)` is no longer part of any verdict rule: §8's decision thresholds for P2-A/P2-F are `\|m2(arm)\| > 0.25 ATR` flat (DP-10), and P1 keeps 10.0 pp. **Wherever the descriptive variant-A P2 figures are printed, they are printed next to `\|Δgap_ATR(arm)\|` and a variant-A number is never described as "beyond MPE" unless it exceeds `0.25 ATR + \|Δgap_ATR(arm)\|`** — the offset is what stops a mechanical number reading as an effect in the report. `Δgap_ATR(arm)` stays a printed headline number per arm, computed from `C_t` and the t+1 open only (§6.1 inputs, never an outcome). Under B (primary) and C (descriptive) no offset applies: B cancels the displacement, C isolates it in C1. | item 16; item 18; DP-10; DP-20; PREREG §4.1, §8 |
| 20 | Hard stop under variant B (R-3 raised by R5) | ASK (question E) → **ANSWERED** | **The hard stop moves from 2027-03-31 to 2027-06-30** (Haci 2026-09-13: *"Hard stop Jun 30, 2027"*), **everywhere the date appears**. **Both arms stay primary** — nothing is dropped, nothing is SUPPRESSED at lock, Q007 is not deferred, and variant B is not traded away for variant A. The exposure-driven decision-date **rule is unchanged in form**: the first Monday on or after 2026-10-26 on which **every retained arm shows ≥ 80 variant-B contributing nights** (DP-21 reading, now counted on the B3-valid definition in item 18); evaluation runs regardless on the hard stop, and any arm still below the floor on 2027-06-30 is INCONCLUSIVE (SUPPRESSED). On the Steward's run-rate the earliest evaluable Monday is not before **2027-06-28** (FAVOUR is the binding arm). This supersedes item 10's date; the floor itself did not move. | R-3 → Haci 2026-09-13, question E; DP-21; DP-24; R5 §(d) |

## Corrections to silent choices

- **§5 floors, §8 clause 1 — the floor reading.** The draft reads the rule-6 floors as "≥ 80 *eligible*
  nights total and ≥ 20 cell nights per arm contrast", with "total eligible nights" defined so that a
  night counts even when it carries no arm pick and no FLAT pick. That is exactly the weaker reading
  DP-21 rules out. It must read: **≥ 80 *contributing* nights per primary endpoint** — for P1-A/P2-A a
  night with ≥ 1 eligible AGAINST pick **and** ≥ 1 eligible FLAT pick; for P1-F/P2-F the same with
  FAVOUR — and **≥ 20 contributing nights per reported sub-cell** (tape stratum, half, band, bull/bear,
  earnings stratum). §5's expected-n arithmetic, the "80th eligible night ≈ 2026-09-25" projection and
  the decision-date rule in §5 are recomputed on contributing nights; §8 clause 1 becomes
  "contributing nights ≥ 80 for that arm". (DP-21; Q008 §5 uses the same reading.) **Fourth-pass
  refinement (item 18):** now that variant B is primary, "contributing night" means a night carrying
  ≥ 1 eligible arm pick **with a valid B3 set (≥ 3 controls)** and ≥ 1 eligible FLAT pick with a valid
  B3 set. Every floor, projection and decision-date test in §5 and §8 uses that definition; the
  exposure-only count is reported alongside it, labelled, and decides nothing.
- **§2 treatment rows — publication predicate.** "every published pick (`selected_rank IS NOT NULL`)"
  must read **`qualified IS TRUE AND selected_rank IS NOT NULL`**; dark-lane rows are excluded from
  every arm and from the FLAT baseline, and the B2/B3 control pool is the complement of that predicate
  (i.e. rows that are not published), unchanged otherwise. (DP-28.)
- **Header + §2 exclusions bullet — exclusions file.** `research/data/exclusions_v002.json` now exists,
  so cite it — replacing "exclusions_v001.json plus the confirmed re-run night 2026-07-02"; `eval.py`
  reads the JSON (`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates`), no hard-coded dates.
  The fallback wording is deleted, not kept. (DP-22; item 6.)
- **§5 decision date and hard stop.** "hard stop **2027-01-25**" becomes **2027-06-30** everywhere it
  appears (§5 decision-date bullet, the pre-lock arm-drop clause, §8, the R4 routed request, and
  anywhere §11/§12 repeat the date). **Superseded date note:** the intermediate 2027-03-31 (Haci
  2026-09-12, question C) must not survive anywhere in the file — question E replaced it on
  2026-09-13. The exposure-driven rule itself is unchanged in form: first Monday on or after
  2026-10-26 on which every retained arm shows **≥ 80 variant-B contributing nights** (DP-21, counted
  on the item-18 B3-valid definition), evaluation runs regardless on the hard stop, and any arm still
  below the floor on that date is INCONCLUSIVE (SUPPRESSED). (Haci 2026-09-13, question E; DP-21.)
- **§5 pre-lock arm-drop clause.** "If that count projects either arm below 20 cell nights by
  2027-01-25, that arm is removed from the primaries before lock" is now **resolved and rewritten as
  fact**: the Steward's count (`research/reports/STEWARD_Q007_exposure.md`) gives AGAINST 22 and
  FAVOUR 20 contributing nights on 49 matured nights (exposure-only), and §R5 gives the figures that
  now govern, since variant B is primary: **AGAINST 18 and FAVOUR 15 variant-B contributing nights,
  projecting to 80 on 2027-04-23 and 2027-06-28**, both inside the extended hard stop of 2027-06-30 —
  **so both arms are retained as primaries and nothing is dropped at lock**. The at-decision-date
  version of the rule (an arm below 80 on **2027-06-30** is INCONCLUSIVE/SUPPRESSED) stays.
- **§5 expected-n arithmetic.** Replace the registrar's "if 25% of eligible nights carry an AGAINST
  pick…" arithmetic and the "80th eligible night ≈ 2026-09-25" projection with the Steward's measured
  figures, cited to `research/reports/STEWARD_Q007_exposure.md` (49 matured nights; AGAINST 22 /
  FAVOUR 20 / union 35 contributing; monthly run-rates as tabled; 384 side-ok picks after 8 no-ladder
  and 2 wrong-side removals; passed-at-entry 0 AGAINST / 7 FAVOUR). **Add the §R5 variant-B figures
  as the ones the floors are actually read against** (item 18): 85.1% of AGAINST and 85.7% of FAVOUR
  eligible picks have ≥ 3 B3 controls (median 7 / 10; FLAT 201/201, min 11); variant-B contributing
  nights AGAINST **18**, FAVOUR **15**, union **29** of 49 matured nights; projections to 80 are
  **2027-04-23 / 2027-06-28 / 2026-12-19**, all inside the 2027-06-30 hard stop. The exposure-only
  counts stay in the file as the pre-variant figure, labelled as such.
- **§10 threats 4 and 5 — mark verified.** Both now carry the R3 result rather than "unverified" /
  "the Steward should verify": threat 5 PASS 40/40 with the hourly-granularity caveat and the DST
  requirement on `eval.py`; threat 4 PASS on code-path evidence for trading_date ≥ 2026-06-01, so the
  earnings stratum in §6 **is** computed and the "otherwise unmeasured" branch is deleted. Cite
  `research/reports/STEWARD_Q007_exposure.md` §R3 in both.
- **§8 PROSPECTIVELY_CONFIRMED clause.** "≥ 30 eligible pick nights after the lock commit … with ≥ 20
  cell nights among them" must read **≥ 30 *contributing* nights for that arm dated after the lock
  commit**, reproducing the sign of `m2` under the unmodified `eval.py`. The clause does not weaken;
  if the window cannot supply 30, the decision date moves and that move is R-3. (DP-24; DP-21.)

### Added on the third pass (2026-09-13) — the redraft

- **§4 entry basis — delete the "Stale decision, not applied" paragraph.** It is replaced by one line:
  "Entry basis decided: pick-night close `C_t`, the DP-03(a) after-hours proxy, for picks and controls
  alike (Haci 2026-09-12; DECISIONS.md item 12; DP-11). `E_AH` is a picks-only descriptive
  sensitivity." The following paragraph's opener, "*Which price and why (registrar's choice, stated for
  Haci's review)*", becomes "*Which price and why (decided, DECISIONS.md item 12)*" — its content is
  correct and stands.
- **§8 MPE paragraph — the MPEs are not placeholders.** "**MPE (placeholders — Haci to confirm at
  lock…)**" and the sentence "The P2 MPE has no desk-derived basis: the desk holds no fill or slippage
  data, so Haci should set it…" are stale: Haci set it on 2026-09-12 (question B → **DP-10**). It must
  read: "**MPE: P1 10.0 pp (DECISIONS.md item 4a; DP-20 is the 5.0 pp floor, raised here because P1 is
  a difference of differences with small cells — Q003 §8 precedent). P2 0.25 ATR per trade (Haci
  2026-09-12 → DP-10; the standing number for every per-trade ATR endpoint, not re-asked).**" The
  variant-A sentence that follows ("Haci should state at lock whether the MPEs stand") is replaced by
  item 16's rule below.
- **§8 — variant-A displacement offset (item 16, scope narrowed by item 19).** ~~Add, immediately
  after the MPE paragraph: "**If variant A is the selected primary**~~ — **variant B is the selected
  primary (item 18), so the conditional no longer fires.** The paragraph is still added after the MPE
  paragraph, in this form: "**P2's decision threshold is `|m2(arm)| > 0.25 ATR` (DP-10) and P1's is
  10.0 pp, under variant B, the selected primary. The descriptive variant-A P2 figures are printed
  next to `|Δgap_ATR(arm)|` and a variant-A figure is never called 'beyond MPE' unless it exceeds
  `0.25 ATR + |Δgap_ATR(arm)|` — the gap's own displacement is inside variant A's number and can
  exceed 0.25 ATR by construction.**" The definition below is kept verbatim as the definition of
  `Δgap_ATR(arm)`, which remains a printed headline number per arm. Original wording, for the record:
  "**If variant A is the selected primary**, P2's threshold is `|m2(arm)| > 0.25 ATR + |Δgap_ATR(arm)|`,
  where `Δgap_ATR(arm) = mean_t [ mean_{p∈arm,t}(dir×(O_{t+1,p}−C_{t,p})/ATR_p) −
  mean_{p∈FLAT,t}(dir×(O_{t+1,p}−C_{t,p})/ATR_p) ]`, computed from `C_t` and the t+1 open only (§6.1
  inputs, never an outcome) and printed as a headline number per arm. DP-10's 0.25 ATR is unchanged as
  the incremental MPE; the offset exists because the gap's own displacement is inside variant A's
  number and can exceed 0.25 ATR by construction. P1 keeps 10.0 pp under every variant. Under B and C
  no offset applies." (DP-10; DECISIONS.md items 16 and 19.)
- **§8 clause 1 — the floor reading, still unapplied.** It reads "eligible nights ≥ 80 total and ≥ 20
  cell nights for that arm"; the first pass required **"contributing nights ≥ 80 for that arm and ≥ 20
  contributing nights for any reported sub-cell"** (DP-21). §5 was corrected; §8 clause 1 was missed by
  the partial apply. (DP-21.)
- **§8 PROSPECTIVELY_CONFIRMED — still unapplied.** "≥ 30 eligible pick nights occurring after this
  file's lock commit … with ≥ 20 cell nights among them" must read **"≥ 30 *contributing* nights for
  that arm dated after this file's lock commit"** (DP-24; DP-21). Also missed by the partial apply.
- **§8 HISTORICALLY_CONFIRMED — add clause 7:** "the verdict is emitted with the label
  **`DESIGN_CHOICE_NOT_BLIND`** (§10 threat 13) and is never restated, ledgered or quoted without it."
- **§10 threat 13 — replace the second half with this wording (item 15), verbatim:**
  > **The close is not a tradable price, and the basis choice was not made blind.** SAS publishes after
  > the close (`finished_at` ~21:0x UTC), so `C_t` is a proxy for an after-hours fill (DP-11); the
  > `E_AH` sensitivity shows the picks-only difference, and after-hours prints are thin and are not
  > fills (Q004 §10 threat 1). Separately, and disclosed in full: Q007's entry basis was changed from
  > the next-session open to the pick-night close on 2026-09-12, **after**
  > `research/reports/weekly/2026-09-12.md` line 29 published sealed-period L1 touch rates measured
  > from the next open versus from the close. That figure is unconditional — no gap grouping, no L3
  > number — and the close basis is DP-03(a), a basis registered before the figure existed and forced
  > here by the question's own framing: a position that is already held when the gap appears must have
  > been entered before the gap, and rule 5 requires its distance-matched control on the same basis,
  > which only the close provides for unpublished candidates. The within-night arm − FLAT contrast also
  > uses one basis on both sides, so a basis-wide level shift largely cancels. None of that makes the
  > choice blind, so its exposure is recorded explicitly: **it weakens the historical track only.**
  > Pick nights 2026-06-01..2026-09-10 sat inside the pinned freeze and were observable when the basis
  > was chosen, so any HISTORICALLY_CONFIRMED verdict on Q007 carries the label
  > **`DESIGN_CHOICE_NOT_BLIND`** in the results header, in `REPORT.md` and in the LEDGER entry.
  > Pick nights after the lock commit were not observable at the switch, so the PROSPECTIVELY_CONFIRMED
  > track (§8) is unaffected, and it remains the only track that can license a rule or a
  > subscriber-facing statement (rule 10). `eval.py` already prints pre-lock and post-lock night counts
  > separately (§5), which is what makes the label checkable.
- **§6 contamination check — append to the third bullet** ("the switch of Q007's entry basis … is
  disclosed as such"): "— the exposure it creates is bounded in §10 threat 13: the historical track
  carries the label `DESIGN_CHOICE_NOT_BLIND`, the prospective track is unaffected."
- **§7 H-063 — the redraft reopened a decided item.** "Whether H-063 is merged, kept separate, or
  re-scoped is open decision 7" must read: "**H-063 is merged into Q007** (DECISIONS.md item 7;
  DP-29); its ATR-scaled gap buckets and its L3-before-(−1 ATR) race are carried here as secondaries,
  descriptive. F4 keeps 7 hypotheses and H-063 is not counted as a second registered question." The
  header already says merged; §7 must agree. **`research/BACKLOG.md` H-063 must be marked "merged into
  Q007"** — that edit is part of the Registrar's apply and has not happened yet.
- **§7 Q004 overlap — decided.** "the two families are corrected separately unless Haci decides
  otherwise (open decision 9)" must read: "**the two families are corrected separately** — Q004 is F7,
  Q007 is F4, and BH runs within a family (rule 8; DP-29). The overlap is a non-independence hazard,
  not a multiplicity one: the two results are never presented or counted as two confirmations (§10
  threat 11), and the Reporter cross-references rather than duplicates." Same deletion of "(open
  decision 9)" in §10 threat 11's last bullet.
- **§3 B3, §4 "Primary endpoints", §4.1, §5 and §10 threat 2 — "still-open item 8" wording
  (resolved 2026-09-13).** Every reference to "still-open item 8" / "OPEN DECISION 8, not chosen
  here" becomes "**variant B, fixed at lock (§4.1; DECISIONS.md items 13 and 18; Haci 2026-09-13)**".
  Specifically:
  - **§1 line 31** ("not yet decided — §4.1 and still-open item 8") → "decided: variant B (§4.1;
    DECISIONS.md item 18)".
  - **§3 B3 last sentence** ("B3 is the primary control **only if** still-open item 8 selects variant
    B; otherwise it is descriptive") → "**B3 is the primary control** (variant B; DECISIONS.md item
    18)." The ≥ 3-control sentence before it is unchanged, it is the rule as drafted.
  - **§4 "Primary endpoints"** ("under the variant fixed at lock by still-open item 8") → "under
    **variant B** (§4.1)"; P1's "controls per the §4.1 variant" → "controls = **B3**"; P2's "with the
    control adjustment of the §4.1 variant where that variant has one" → "**with the B3 control
    adjustment** (pick minus its B3 control mean, night contrast arm minus FLAT of those
    differences)".
  - **§4.1 heading** loses "(OPEN DECISION 8, not chosen here)" and becomes "**— design variants
    (variant B selected, Haci 2026-09-13)**"; the closing sentence "The registrar has not chosen" is
    replaced by "**Variant B is primary; A and C are reported as descriptive figures and never
    decide** (DECISIONS.md items 13, 18, 19)." Variant A's and C's full specifications stay, each
    labelled "**descriptive, does not decide**"; C's own cost note keeps the sentence that as a
    primary it would need §6.1 widened — **that widening was not granted** (Haci 2026-09-13).
  - **§5** (the "if still-open item 8 selects variant B" conditional in the Steward-count paragraph)
    → unconditional, citing the delivered §R5 counts.
  - **§10 threat 2 last sentence** ("Handling is open decision 8 (§4.1)") → "**Handled by variant B
    (§4.1): the displacement sits on both sides of the B3 contrast and cancels. The per-arm 'touched
    at the open' count remains a printed headline number, and the descriptive variant-A figures carry
    `|Δgap_ATR(arm)|` beside them (DECISIONS.md item 19).**"
  - **§10 threat 8** ("Variant B makes this worse (picks without ≥ 3 same-group controls drop out)")
    stays and is **quantified** from §R5: 7 of 47 AGAINST and 5 of 35 FAVOUR eligible picks lose
    their B3 value, and arm contributing nights fall from 22/20 to **18/15**, which is why the hard
    stop moved to 2027-06-30 (item 20).
  - **§8 arm-level reading and §9's opener** ("P2 CONFIRMED under variant B, or C if Haci widens
    §6.1") → "**P2 CONFIRMED under variant B**" alone; the "or variant C if made primary" branch is
    deleted, since §6.1 was not widened. §8's variant-A sentence ("Under variant A a CONFIRMED P2 is
    reported as …, and no management rule follows") and §9's "Variant A selected and CONFIRMED"
    bullet are kept but re-worded as **descriptive-only** statements about the A figures, not about a
    selected primary.
- **"Open decisions before lock" section — delete it entirely.** All nine items are now either decided
  here (1, 3, 4, 5, 6, 7, 9-new), returned by the Steward (2), or **answered by Haci (item 8 →
  question D, variant B, 2026-09-13)**. The partial apply stopped before this; nothing may be left in
  the file that reads as open at lock. Item 8's trailing "If A is chosen, also confirm whether the
  MPEs in item 4 stand" goes with it — A was not chosen and the MPEs stand (items 4a, 4b, 19).
- **§4 "Stale decision, not applied" paragraph** (still present at §4 lines 166–173) — delete per the
  third-pass bullet above; it is the last thing in the file that reads as unresolved.
- **Fourth-pass date sweep.** After applying, `grep` the file for `2027-01-25`, `2027-03-31`,
  `open decision 8`, `still-open item 8`, `not chosen here` and `registrar's choice` — every hit must
  be gone. The only stop date in the file is **2027-06-30**.

**Conflicts with already-locked questions (for the Red Team; the locked files stand, nothing is edited):**
- `Q003 §5` — floors written as "≥ 20 nights per cell, ≥ 80 nights total" while the primary estimator
  needs both cells on a night (`n_paired`); under DP-21 the 80 would attach to `n_paired`.
- `Q004 §5` — "≥ 80 nights total" with the E_AH coverage rule removing nights from T1; under DP-21 the
  80 would attach to T1's contributing nights.
- `Q004 §2`, `Q006 §2` — publication predicate is `selected_rank not null` only, looser than DP-28.

## Questions for Haci

### A. Q007 asks whether a pick that opens more than 2% away from its pick-night close trades differently. The target it measures is L3 — the strike you sell. How long do we give it to get there?
Why yours: a horizon that differs from the platform's own lane window is a statement about how you trade the spread, not a statistic (R-2).
- (Recommended) **20 sessions** — the spread horizon (≈ expiry), same clock as Q004's race; 40 sessions reported alongside wherever it has matured. Answers the question you would actually act on, and can reach its sample floor first.
- **40 sessions** (the platform's own L3 lane window) — matches what the conviction card promises, but the sample floor moves out by roughly another quarter, so the likely outcome on the hard stop is INCONCLUSIVE.
- **Both as co-primaries** — you get both numbers, but the question carries 8 primary endpoints instead of 4, every one needs its own sample floor, and the multiple-testing correction roughly doubles. Not recommended.
Answer: **"20 sessions"** (Haci, 2026-09-12) — the spread horizon. L3 within 20 sessions is the primary
clock; the platform's 40-session L3 window is reported alongside wherever it has matured, descriptively.
Generalised as **DP-09**.

### B. How much better (or worse) per trade, measured in ATR, would a 2%-gap pick have to be before you would actually skip it or take it? (This is the number the desk calls the MPE for P2; anything smaller is reported as "real but too small to trade".)
Why yours: it encodes your execution costs and slippage, which the desk holds no data on (R-4). Once set, it becomes the standing number for every per-trade ATR endpoint — Q008's K3 and Q009's P2/P3 currently carry placeholders of 0.25 and 0.20 ATR waiting on this.
- (Recommended) **0.25 ATR per trade** — roughly a round-trip cost at the size these names trade; what Q007 and Q008 drafted.
- **0.20 ATR per trade** — slightly more sensitive; what Q009 drafted. Picks up smaller effects, more likely to call something tradeable that costs eat.
- **0.50 ATR per trade** — only a large effect counts; near-certain INCONCLUSIVE on cells this size, but nothing marginal ever reaches the guide.
- **Your own number, in ATR, percent or dollars per trade** — say it in whatever unit is natural and the desk converts it once and records it.
Answer: **"0.25 ATR per trade"** (Haci, 2026-09-12) — the recommended option. Q007 P2's MPE is
**0.25 ATR per trade**, and this is now the standing number for every per-trade ATR-denominated
endpoint. Generalised as **DP-10**.

### C. The Steward has counted the nights. At the current rate the "gap against" arm reaches a full sample on 2027-02-22 and the "gap in favour" arm on 2027-03-21 — both a little past the 2027-01-25 stop date in the draft. Wait the extra weeks, or run early with less?
Why yours: it is a trade-off between waiting and sample size — how long you are willing to leave a
question open before it pays you an answer (R-3). The desk cannot pick the horizon you trade on.
- (Recommended) **Extend the hard stop to 2027-03-31, both arms stay primary** — both arms reach the
  full 80-night floor, so both can return a real verdict; the cost is roughly two extra months before
  Q007 reports anything.
- **Keep 2027-01-25 and drop the two arms to descriptive** — you get a number in January, but neither
  arm can be CONFIRMED or NULL, only described; the question effectively answers nothing.
- **Keep 2027-01-25 and report the combined arm only** — the union reaches the floor by 2026-11-14, so
  one clean answer in January, but it merges "gap against" and "gap in favour", which are the two
  opposite cases the question exists to tell apart.
- **Defer Q007 and revisit when the tape has produced more nights** — no work spent now; the question
  goes to `DEFERRED.md` and loses its place.
Answer: **"Extend the hard stop to 2027-03-31; both arms stay primary as drafted"** (Haci, 2026-09-12)
— the recommended option. Hard stop 2027-03-31; the exposure-driven decision-date rule is unchanged;
AGAINST and FAVOUR both remain primary arms with all four primary endpoints (P1-A/P1-F/P2-A/P2-F).

### D. Now that we measure from the previous close, a pick that gapped 2% your way has already done part of the move to L3 before the signal even exists. Do we measure the whole move, or strip the gap out of it?
Why yours: it fixes what Q007 actually tests and cannot be changed after lock, and one of the three
options needs you to widen the knowledge-time exception you granted on 2026-09-12 (R-1). Whichever you
pick, the other two are still reported alongside as descriptive numbers.
- (Recommended) **Strip the gap out** — compare each gapped pick against same-night stocks that gapped
  the same way (variant B). This is the only version that can license a hold/exit/add rule, because the
  gap's own move sits on both sides and cancels; it answers "does a 2% gap mean something different for
  a SAS pick than for any similar stock that gapped the same way". Cost: the comparison set is smaller,
  picks without at least 3 matching stocks drop out, so the arms may reach the 80-night floor later than
  2027-03-21 or not at all — the Steward is counting that now, and if it turns out unreachable the
  waiting-vs-sample choice comes back to you with the number.
- **Measure the whole move** (variant A) — simplest, and literally what your held position earned.
  Cost: the answer is largely arithmetic (a pick that gapped in your favour looks good because it
  gapped), so under the desk's own rule it licenses **no** management rule — only a description. To stop
  that being a free pass, a favourable-gap result would have to beat 0.25 ATR **on top of** the gap's own
  size before it counts.
- **Split the trade at the end of day 1** (variant C) — closest to your "rest of the trade" wording:
  day 1 reported on its own, then what happened from day 1's close onward. Cost: you would have to widen
  the 2026-09-12 knowledge-time exception so that a day-1 outcome can define the group, and the
  day-2-onward part quietly drops the picks that already hit their target — which are not the same
  picks in each arm, so the two arms stop being comparable.
Answer: **"Strip the gap out"** (Haci, 2026-09-13) — the recommended option. **Variant B (the
gap-matched same-night B3 control) is the primary definition of P1 and P2** for all four primary
endpoints; variants **A and C are reported descriptively** and never decide. The §6.1 rule-14
exception is **not** widened (C was not chosen), so DP-05 stands as written and no new R-1 arises.
The ≥ 3-control rule of §3 applies as drafted: a pick with fewer than 3 same-group controls loses its
B3 value, drops out of that night's mean, and the drop is counted and printed. Generalised as
**DP-12**. The Steward's R5 count then triggered the anticipated R-3 → question E below.

### E. To strip the gap out we compare each gapped pick against same-night stocks that gapped the same way — and the Steward has now counted how often that comparison actually exists. It does, for about 85% of picks, but it costs nights: the "gap against" arm now reaches a full sample around 2027-04-23 and "gap in favour" around 2027-06-28, both past the 2027-03-31 stop you set last time. Move the stop again, or give something up?
Why yours: the same waiting-vs-sample trade-off as question C — how long you are willing to leave a
question open before it pays you an answer (R-3). The desk does not set your horizon and never lowers
the sample floor to hit a date.
- (Recommended) **Move the hard stop to 2027-06-30, keep variant B and both arms** — both arms reach
  the 80-night floor with the gap stripped out, so both can return a real verdict that could license a
  hold/exit/add rule; the cost is about three more months before Q007 reports.
- **Keep 2027-03-31 and fall back to variant A** — a number in March, but it measures the whole move
  including the gap itself, so by the desk's own rule it licenses no management rule, only a
  description.
- **Keep 2027-03-31 with variant B and accept that FAVOUR is SUPPRESSED** — a "gap against" answer in
  March (marginal: AGAINST projects 2027-04-23) and no answer at all on favourable gaps, which is half
  the question.
- **Report the combined arm only** — the union reaches the floor by 2026-12-19, so one clean answer
  this year, but it merges "gap against" and "gap in favour", the two opposite cases the question
  exists to tell apart.
Answer: **"Hard stop Jun 30, 2027"** (Haci, 2026-09-13) — the recommended option. Both arms stay
primary under variant B; the exposure-driven decision-date rule is unchanged in form (first Monday on
or after 2026-10-26 on which every retained arm shows ≥ 80 variant-B contributing nights); only the
hard stop moves, from 2027-03-31 to **2027-06-30**. Supersedes the date in item 10. No new `DP` id —
see "Standing rules added".

## Routed requests

### data-steward

**R1 — exclusions_v002.json — DONE 2026-09-12.** Delivered: `research/data/exclusions_v002.json`
(103 nights total / 34 in-sample / 69 sealed), plus a paragraph in `research/data/DATA_NOTES.md`.
The PREREG now cites v002 (item 6). Original request below, for the record.
Please issue `research/data/exclusions_v002.json` as the successor to `exclusions_v001.json`, implementing your own proposal in `research/reports/KT_AUDIT_manifest_v001_rerun_nights.md` §7 verbatim: `manual_runs.trading_dates` becomes the existing five nights (2026-05-11, 05-12, 05-13, 05-14, 2026-07-06) **plus** the four confirmed re-run nights 2026-04-02, 2026-04-24, 2026-05-15 and 2026-07-02; `manual_runs.late_but_clean` is reduced to 2026-04-01, 2026-04-03, 2026-04-06, 2026-05-01; `non_session_runs`, `catalyst_layer_regime_change` and `regime_label_point_in_time_from` carry over unchanged; keep the availability-note correction you drafted for `sas_candidates`. This is desk policy under DP-22 (the newest exclusions file is cited by every draft not yet locked; locked PREREGs are never edited and the file they cite stands), so it does not need a further decision from Haci. Note in the file's header which registered questions it affects: Q007 (this draft, only 2026-07-02 falls inside its ≥ 2026-06-01 window, so its population is unchanged), Q008 and Q009 (drafts), and Q006 (DATASET_PINNED, locked citing v001 — flagged to the Red Team, not edited).

**R2 — exposure-only contributing-night count — DONE 2026-09-12.** Delivered:
`research/reports/STEWARD_Q007_exposure.md` §R2. Result: 49 matured nights, 384 side-ok picks;
contributing nights AGAINST 22, FAVOUR 20, union 35; projections to 80 contributing nights AGAINST
2027-02-22, FAVOUR 2027-03-21, union 2026-11-14. Both arms past the draft's hard stop → R-3 → Haci's
answer C: hard stop 2027-03-31, both arms stay primary. Original request below, for the record.
For every non-excluded, matured pick night in Q007's window (pick nights ≥ 2026-06-01 whose 20-session forward window has matured in `manifest_prices_v001`), please report **counts only**: the number of nights with ≥ 1 eligible AGAINST pick (`g ≤ −2.0`), ≥ 1 eligible FAVOUR pick (`g ≥ +2.0`), ≥ 1 eligible FLAT pick (`|g| < 1.0`), and — the number that decides this — the number of **contributing** nights per arm, i.e. nights carrying both ≥ 1 eligible pick in that arm and ≥ 1 eligible FLAT pick, where `g = dir × (O_{t+1} − C_t) / C_t × 100` with `C_t` the actual pick-night close and `O_{t+1}` the session t+1 official open from `prices_daily_split`, `dir` from `dominant_direction`, and "eligible" applying the PREREG §2 filters that need no forward bar (published under `qualified IS TRUE AND selected_rank IS NOT NULL`, has a lane-plan ladder with an L3, L3 on the correct side of `C_t`, L3 not at or through `O_{t+1}`, t+1 open present). Please also report the per-arm passed-at-entry count and the monthly run-rate of contributing nights per arm, and project the date on which each arm reaches **80** contributing nights and the date total contributing nights reach 80. No price level, no forward bar beyond the t+1 open, no touch, no return, no outcome of any kind — counts and dates only; the Decision-maker and the Registrar will read only the counts. What it decides: with the floor now read as ≥ 80 contributing nights per primary endpoint (DP-21), if an arm cannot project 80 contributing nights by the hard stop 2027-01-25 that arm drops out of the primaries and its two endpoints become descriptive, and if neither arm can, Q007 goes to DEFERRED instead of being locked — both of those are R-3 trade-offs between waiting and sample size, so they go to Haci with your numbers attached, not decided here.

**R3 — two pre-lock verifications — DONE 2026-09-12.** Delivered:
`research/reports/STEWARD_Q007_exposure.md` §R3. Part 1 (official open / extended hours): **PASS
40/40**, hourly-granularity caveat stated, DST hazard disclosed (`eval.py` must derive the
09:30/16:00 ET boundary per date with `zoneinfo`). Part 2 (`days_to_earnings_corrected`): **PASS on
code-path evidence for trading_date ≥ 2026-06-01**, Q007's whole window, so the earnings stratum is
computed. Both fold into §10 as verified (item 11). Original request below, for the record.
First and load-bearing: on a sample of symbol-dates in `prices_daily_split`, confirm that the daily `o` is the **official 09:30 ET regular-session opening print** and that `o`/`h`/`l` exclude extended-hours prints (cross-check against the 09:30–10:00 ET hourly bar in `prices_hourly_raw`, split-basis snapped). If `o` is a first-trade print that is not the official open, or the daily bar includes pre-market prints, Q007's gap variable and its entry price are both contaminated and the question must be re-specified before lock — so please report this as a pass/fail with the sample size, not as a number to interpret. Second and optional: state whether the report date behind `sas_candidates.days_to_earnings_corrected` (or any alternative column) was available by 16:05 ET on the pick night; if you cannot establish that, say so plainly and the earnings stratum is simply not computed, per §6, which needs no further decision.

**R4 — successor freezes — OPEN, at the decision date (by design, not a blocker for lock).**
Now due at the decision date under the extended hard stop of **2027-06-30** (item 20; earliest
evaluable Monday on or after 2026-10-26 at which every retained arm shows ≥ 80 **variant-B**
contributing nights; on the Steward's §R5 run-rate that is not before **2027-06-28**, FAVOUR being
the binding arm). Scope is unchanged and fixed by DP-23, and variant B does not change it — B3 needs
the same unpublished-candidate symbols the B2 pool already required, and their **t+1 opens** are now
load-bearing for group assignment as well. Original request below.
When Q007 reaches its decision date, build `manifest_v002` (selections, same SQL as v001) and `manifest_prices_v002` (same Alpaca queries) covering pick nights after 2026-09-10, with the symbol list extended to **every candidate on those nights, published and unpublished** — the unpublished symbols' opens and forward bars are what the B2 distance-matched control is made of — plus hourly bars for published symbols for the secondary race's same-session tie-breaks. Scope is fixed by DP-23 and needs no further confirmation; `eval.py` will record each sha256 and print pre-lock and post-lock night counts separately.

**R5 — variant-B feasibility, counts only — DONE 2026-09-13.** Delivered:
`research/reports/STEWARD_Q007_exposure.md` §R5, on the R2 population re-derived from the frozen
parquet (394 published rows / 49 matured nights; eligible AGAINST 47, FAVOUR 35, FLAT 201).
Result: (a) picks with ≥ 3 same-group non-published controls — **AGAINST 40/47 = 85.1%, FAVOUR
30/35 = 85.7%, FLAT 201/201 = 100%**; (b) median control count 7 (AGAINST) / 10 (FAVOUR) / 28
(FLAT), 10th percentile 1.6 / 1.4 / 19.0, FLAT's minimum 11 so the FLAT side never binds; (c)
**variant-B contributing nights AGAINST 18, FAVOUR 15, union 29** of 49 matured nights (vs 22 / 20 /
35 exposure-only — the reduction is entirely arm-side); (d) projections to 80 variant-B contributing
nights **AGAINST 2027-04-23, FAVOUR 2027-06-28, union 2026-12-19**. Both arms past the then-current
2027-03-31 hard stop → R-3 → Haci's answer E: **hard stop 2027-06-30, both arms stay primary under
variant B** (items 17, 20). Original request below, for the record.
On the same population as R2 (published picks under `qualified IS TRUE AND selected_rank IS NOT NULL`, non-excluded nights per `exclusions_v002.json`, pick nights ≥ 2026-06-01 whose 20-session window has matured in `manifest_prices_v001`, PREREG §2 filters that need no forward bar), please report **counts only** for the PREREG §3 **B3** gap-matched control: for every eligible pick p in AGAINST, FAVOUR and FLAT, how many same-night **non-published** `sas_candidates` rows (the complement of the publication predicate, symbol with ≥ 60 daily bars dated ≤ t) fall in p's own gap group when their gap is direction-adjusted with **p's** direction, i.e. `dir_p × (O_{t+1,c} − C_{t,c}) / C_{t,c} × 100` classified with the same cuts (AGAINST ≤ −2.0, FLAT |g| < 1.0, FAVOUR ≥ +2.0). From that give: (a) the number and share of picks per arm with **≥ 3** such controls; (b) the median and 10th-percentile control count per arm; (c) the number of **variant-B contributing nights** per arm — nights carrying ≥ 1 arm pick with a valid B3 set **and** ≥ 1 FLAT pick with a valid B3 set; (d) the monthly run-rate of (c) and the projected date each arm reaches **80** variant-B contributing nights. Inputs are the pick-night close and the session t+1 official open only — no price level, no forward bar beyond the t+1 open, no touch, no return, no outcome of any kind, and please do not compute or report anything about targets. What it decides: whether variant B (PREREG §4.1) can reach the DP-21 floor before the 2027-03-31 hard stop. If it cannot, that is a waiting-vs-sample trade-off (R-3) and goes to Haci with your numbers attached — drop to variant A with the item-16 displacement offset, move the stop again, or accept a SUPPRESSED arm; it is not resolved by the desk and never by loosening the floor.

## Standing rules added

- **DP-09** (Confirmed; Haci 2026-09-12, Q007) — when the entry basis is the next-session open spread
  and L3 is the primary level, the primary clock is L3 within 20 sessions; the platform's 40-session
  L3 window is reported alongside, descriptively, wherever it has matured. Floors and decision dates
  are computed on the 20-session window.
- **DP-10** (Confirmed; Haci 2026-09-12, Q007) — MPE for any per-trade endpoint denominated in ATR is
  **0.25 ATR per trade**.
- **DP-09 — edited in place 2026-09-13** (not a new id). Its scope clause "when the entry basis is the
  next-session open spread" no longer fits, because Haci moved Q007's entry to the pick-night close
  while the clock he chose stayed the same. It now reads "L3 within 20 sessions **measured from the
  stated entry**", with the edit, its date and its reason recorded in the source column. The rule is
  about the level and the horizon, not the entry basis; nothing else changes and no second row was
  added.
- **DP-11** (Confirmed; Haci 2026-09-12, recorded 2026-09-13, Q007) — when a question measures what
  happens to a position that is **already held** when the signal appears, the entry is the pick-night
  regular-session close `C_t`, the proxy for the DP-03(a) after-hours fill, for picks and controls
  alike; the real after-hours price (`E_AH`) is a picks-only descriptive sensitivity. Haci's words:
  *"I want to measure the movement of the stock from closed price of previous day not opening prices."*
  Generalised because the same choice arises in every held-position question (Q008, Q009 drafts) and
  must not be re-asked. Questions whose subject *is* the entry basis (Q004) are explicitly unaffected.
- **DP-12** (Confirmed; Haci 2026-09-13, Q007, question D) — when the conditioning variable is itself
  part of the price path (an overnight gap, a fast start, any move that has already happened when the
  signal is read), the **primary** contrast uses a control matched on that variable; the total effect
  is **descriptive**. Haci's words: *"Strip the gap out."* Generalised because the same shape recurs
  in Q008 (fast start to L4) and in every future "the move is inside the signal" question, and because
  it is the only form that can license a management rule under rule 5. Its cost is accepted with it:
  matched pools are smaller, picks below the control floor drop out and are counted, and the sample
  floor arrives later — that later date is an R-3 for Haci, never a reason to loosen the floor or to
  fall back to the total effect.
- **From question E (2026-09-13): none.** Like question C before it, the answer is a single date for a
  single question — Q007's hard stop moves from 2027-03-31 to 2027-06-30 — and generalises to nothing:
  it is the arithmetic of Q007's own variant-B arm run-rates against DP-21's floor. No new `DP` id was
  taken; DP-21 and DP-24 are unchanged (the floor did not move, the stop date did, which is exactly
  the R-3 move DP-24 anticipates). Note for the desk: this is the **second** stop extension on Q007,
  both caused by per-arm floors on a signed-arm design — the Registrar should carry that forward when
  drafting future signed-arm questions, as an expected-n warning at draft time, not as a new rule.
- **From question C (2026-09-12): none.** The answer is a single date for a single question — Q007's
  hard stop moves from 2027-01-25 to 2027-03-31 — and generalises to nothing: it is the arithmetic of
  Q007's own arm run-rates against DP-21's floor, which is already the standing rule. No new `DP` id
  was taken, and DP-21/DP-24 are unchanged (the floor did not move; the stop date did, which is
  exactly the R-3 move DP-24 anticipates).

**Downstream effect of DP-10 on other drafts** (noted here, applied when those questions are decided;
nothing outside Q007 is edited by this file):
- **Q008 K3** — carries 0.25 ATR already; consistent with DP-10, no change.
- **Q009 P2 (0.20 ATR) and P3 (0.30 ATR)** — placeholders that must be corrected to **0.25 ATR** when
  Q009's open decisions are decided. Both are drafts, so this is a correction, not a locked-file conflict.
- No locked PREREG carries an ATR-denominated per-trade MPE, so DP-10 creates no new Red Team flag.

**Downstream effect of DP-12** (noted here, applied when those questions are decided; nothing outside
Q007 is edited by this file):
- **Q008 (fast start to L4)** — the conditioning variable is a completed part of the path, exactly
  DP-12's shape. Its primary contrast needs a control matched on the fast start itself; the total
  effect is descriptive. Its expected-n must be counted on that matched definition **before** lock,
  as Q007's R5 was, so the stop date is set once rather than twice.
- **Q009 (stop whipsaw)** — check at decision time whether its conditioning variable is path-derived;
  if it is, DP-12 applies and the same pre-lock count is routed to the Steward.
- No locked PREREG conditions on a path-derived variable, so DP-12 creates no new Red Team flag.

**Downstream effect of DP-11** (noted, not applied here): Q008 and Q009 are drafts about picks that are
already held, so their entry basis is `C_t` under DP-11 and is settled when their own open decisions are
decided. Q004 is the registered entry-basis test and is out of DP-11's scope by construction. No locked
PREREG is contradicted: Q006 measures from the next-session open for a question about entering, which
DP-11 is scoped to
questions where the signal appears *after* the position already exists, so Q006 is outside it (and is
locked, so it is not edited in any case).
