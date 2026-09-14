# Q019 — decisions before lock
Run: 2026-09-13 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 3 items (+2 routed requests named in §5: R1 counts-only/lock-or-DEFER, R2 successor freezes)
**Record pass: 2026-09-13 (autonomous)** · Source: `research/reports/STEWARD_Q019_exposure.md` (R1, counts only, on the pinned freeze; DP-50(c)). **Q019 LOCKS** on the unmodified drafted schedule. `A` = **42** matched-contributing nights accrued to 2026-08-26 under the corrected NOFLAG-at-`s` definition, `r` = **0.6885** per elapsed session; the last tier-logic ship is **2026-05-16**, before the window start. Every ROUTED item R1 settles is settled below and **no item is pending**; four further items (9–12) are decided here on the measured counts. R2 (successor freezes) stays open **by design** — due before the decision pass, never a blocker for lock (DP-23) — and is extended at record with two clauses.

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-13) — in scope. All **three** of the
Registrar's open items met a DECIDE ground and none of them needed Haci's word: item 1 on the
product-surface predicate plus DP-45, item 2 on rule 5 / DP-12 plus DP-45, item 3 on DP-06 / DP-50(a)
plus DP-21 / DP-43. Three further items are decided here because the rule they need already exists
(exclusions past the file, demotion at lock, and the control pool's own window), **one** item is
**DEFAULTED** under DP-43 — the planning rate, the window end and the DEFERRED trigger, which is the
R-3 in this question — and two are routed.

**Q019 did not lock at `decide`.** Unlike Q017 and Q018, this question had **no exposure measurement of
any kind** behind it: nothing in the desk's reports had ever counted a `conviction_monitor` tier
(EXPLORE_001 printed the table's shape and two head rows, nothing else), and no other question's
funnel was close enough to borrow — Q012's and Q015's funnels count *published picks*, not *flagged*
published picks with a damage-matched control on the same session, which is a strictly smaller and
unmeasured unit. R1 was therefore **blocking for lock**, and its item (3) was the number that decided
whether this question locked at all or went to `DEFERRED.md` (DP-43's 12-month ceiling).

**Resolved at `record`, the same day.** R1 measured `A` = **42** and `r` = **0.6885** matched-contributing
nights per elapsed session — nearly **twice** the 0.35 planning rate and far above the `r ≥ 0.26`
ceiling threshold — and dated the last tier-logic ship at **2026-05-16**, fifteen calendar days before
the window start. Both branches that could have moved the schedule are therefore closed: the window
start does **not** move (item 3 does not fire) and the DEFERRED branch does **not** fire. Because a
faster rate licenses nothing and **never pulls a date in** (item 4's third branch, DP-43, DP-45), the
drafted window end, decision date and extension date stand **exactly as written**. The measured rate
also means the registered window projects ≈ **160** contributing nights against an 80-night floor: the
question is over-powered by roughly 2× and the desk waits about six months longer than the floor
requires. That cost is real, it is named on the board under the DEFAULTED item, and it is paid where
it belongs — in the drafting order, not by moving a locked date (Standing rules proposed).

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Which tier field is "the Conviction Monitor exit" | DECIDED | **Option A** — the primary trigger is **`age_adjusted_severity = 'EXIT'`**, first such row in sessions `t+1 … t+5`, signal session `s` = that row's own `trading_date`. The undecayed **`overall_tier = 'EXIT'`** stays a registered secondary arm on the same two endpoints and the same matching, printing raw p only, and **never decides** — including in the §9 branch where it looks stronger, which is explicitly labelled as resting on a secondary and needing its own question. §2, §4, §5 and §9 stand as drafted. | Ground 3 (one defensible answer): the product *is* `age_adjusted_severity` — the panel sorts, counts and colours on it (`routers/conviction_monitor.py:157-168`, `:181-184`), so it is the only field on which "an EXIT tier is an exit" can be a claim about what a subscriber sees; H-050 names the Conviction Monitor's exit, not an internal rollup. **DP-45** points the same way: A is the smaller, slower-accruing arm (the age decay softens a day-3-to-5 EXIT to WATCH before it is shown, `:50-56`, `:807-811`), so B would reach the 80-night floor sooner on a signal nobody is shown — never a reason to choose it. Read as R-2 instead, **DP-42**'s first clause gives the same answer: the trigger the hypothesis names. Nothing is lost either way — B is registered |
| 2 | What the unflagged control pool is | DECIDED | **Option A** — **B2 is every NOFLAG published pick**, WATCH and UNKNOWN rows included, subject to the §3 calipers. **B3 (HOLD-only) stays a sensitivity that never decides.** §3 stands as drafted, with the knowledge-time repair in Correction 1 below. | CLAUDE.md rule 5 + **DP-12**: the baseline the desk owes is "Y when X did not happen", and the literal complement of "the monitor printed EXIT" includes every row it did not print EXIT on. **DP-45**: B is the weaker-of-two only in the hypothesis's favour — matching a flagged pick against a hand-picked healthy one inflates the contrast — and A is the noisier, smaller-effect pool, so A is the option less likely to reach CONFIRMED. Precedent: Q017 §3's B2/B3 pair (primary = the complement pool, the clean cohort as a sensitivity) |
| 3 | If R1 dates a tier-logic change after the window start | DECIDED | **Option A** — **move the window start to the first pick night after the last such change** and recompute the whole §5 schedule at that start (`window_start = max(2026-06-01, first pick night after the last tier-logic ship)`). No split, no second pair of primaries, **BH stays m = 2 in every branch**. The recomputation is mechanical and can only push dates **out**; if the recomputed initial decision date falls after **2027-09-13**, Q019 goes to `DEFERRED.md` at `record` rather than the ceiling being stretched or the start being left where it is (item 4's inequality, re-solved at the new start). Pre-change nights are **not** printed as a descriptive panel — they are a different feature, not a weaker reading of the same one. | **DP-06 / DP-50(a)**: a column that changed meaning mid-window is two features, and the monitor rows carry no engine-version column (§10.4), so the desk cannot split cleanly even if it wanted to. **DP-21 + DP-43**: a split registers two primaries neither of which can reach 80 contributing nights inside the ceiling — Q017 DECISIONS #2's rule applies, *INCONCLUSIVE-by-infeasibility is not strictness*, so B is not the conservative option, it is the one that spends two slots in the F6 correction on two under-powered tests. A moves the date out; DP-45 is satisfied by construction |
| 4 | Planning rate, window end and the DEFERRED trigger | **DEFAULTED** | **Plan on 0.35 matched-contributing nights per elapsed session**, window **pick nights 2026-06-01..2027-05-03**, drafted decision **Monday 2027-05-24**, one automatic DP-13 extension to window end **2027-06-15** decided **Monday 2027-07-12**, then DEFERRED. **The trigger is the inequality, not the number:** with `A` = measured contributing nights accrued to 2026-08-26 and `r` = the measured rate per elapsed session, the window end is `2026-08-26 + 1.4484 × (80 − A)/r` days and the decision date 21 days after it; **if that date is after 2027-09-13, Q019 is not locked and goes to `DEFERRED.md`** with the measured rate, the projected floor date and a re-check trigger (the H-062 form). `r ≥ 0.26` is that inequality's solution at `A = 58r` and a 2026-06-01 start only, and it is **re-solved at whatever start item 3 fixes**. Three branches: below the inequality → DEFERRED; inside it but slower than 0.35 → both dates move **out** to the recomputed date and the question locks on those; faster than 0.35 → **nothing changes** (a fast rate licenses nothing, never pulls a date in). | **DP-43**; not taken: descriptive read on the ≈20 nights already frozen, answered in weeks |
| 5 | Exclusions inside a window that outruns every exclusions file | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** (the newest file, DP-22) with the **add-only successor exclusions file issued with the successor selection freeze** — the identical three lists (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`) built by the identical criteria, covering the post-2026-09-10 nights. The successor file may only **add** nights; no night is ever removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be. DP-04 applies mechanically on top. Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. | DP-22 read as "one list, built by one set of criteria" — its "cite the newest file" clause presumes a sealed window, and Q019's window runs to 2027-05-03, eight months past v003. Leaving the post-lock nights to DP-04 alone would silently drop the `uncorroborated_publication_runs` and `non_session_runs` protections the sealed nights get. Q018 DECISIONS #4, same cycle, same construction; add-only, so the exclusion set can never be loosened after lock |
| 6 | Sub-cell demotion at lock (DP-43) | DECIDED | **The two arms are not demotable** — a night missing an eligible FLAG pick *or* its matched control is **non-contributing** (§2), never a thin arm, so DP-43's demotion clause reaches only the §4 sub-cells. **Rule fixed now, applied to R1's measured splits at `record`:** any sub-cell projected below 20 contributing nights at the decision date is **SUPPRESSED at lock** (counts only, no point estimate, no "directionally"), and the **bearish cell is expected to be a structural suppression** — the comparable published-pick population measures 14 bearish rows in 550 (`STEWARD_Q017_exposure.md`), and a *flagged bearish* pick with a damage-matched bearish-eligible control on the same session is rarer still; R1 item (8) settles it. **Suppression restricts affirmative reporting only.** It never removes a cell from **§8 clause 6** (no tape stratum with ≥ 20 contributing nights beyond MPE in the opposite sign, and the sign held in every such stratum) or from clause 7, and it is never a route to an easier CONFIRMED. | DP-43 (demotion decided at lock, never afterwards); DP-21 (20 per cell); DP-42 (elite = `overall_score ≥ 90`, a sub-cell here and never an arm); Q017 DECISIONS #7 (a)–(d) verbatim, the same four clauses |
| 7 | Window end, decision date, extension date, **lock-or-DEFER** | **DECIDED at `record`** (was ROUTED → data-steward; R1 landed) | **LOCK, on the unmodified drafted schedule.** Window start stays **2026-06-01** — R1 item (7) dates the only three commits ever to touch `services/conviction_monitor_service.py` at **2026-05-16** (13234cc / baf17b8 / 2cb7a7e, same day), fifteen calendar days *before* the start, so item 3 does not fire and the "Fix 1–6" work is bundled pre-window. Window end **2027-05-03**; decision **Monday 2027-05-24**; one automatic DP-13 extension to window end **2027-06-15**, decided **Monday 2027-07-12**; then DEFERRED. `A` = **42**, `r` = **0.6885**/elapsed session, above the `r ≥ 0.26` ceiling threshold → the DEFERRED branch is closed; above the 0.35 planning rate → **nothing moves**. The measured rate would have put the 80th contributing night near **2026-11-14** and an equivalent decision near **2026-12-05**; both are informational and **a date is never pulled in** (item 4, third branch). The registered window therefore runs ≈ 233 elapsed sessions and projects ≈ **160** contributing nights, ≈ 2.0× the floor. | **DP-43** + **DP-45** (a faster rate licenses nothing; no date moves in, no floor is lowered to meet one), item 4's third branch as drafted; **DP-06 / DP-50(a)** satisfied — no tier-logic ship inside the window, and the DP-50(a) sweep since manifest SHA `fa70688` is clean (only 2d5776c, PI-001, unrelated); **DP-13** (one extension, then DEFERRED) |
| 8 | Successor freezes | ROUTED → data-steward — **extended at `record`** | waits on **R2** — `manifest_v002` / `manifest_prices_v002` (including the `conviction_monitor` table key) due **before the decision pass**, not a blocker for lock (DP-23); a second pair **only if** the DP-13 extension fires. **Two clauses added at record:** (vi) the monthly polarity composition of the successor nights, and (vii) the dated SHA of any change that restores polarity coverage or otherwise alters which picks receive `EXIT` (items 10 and 12) | — |
| 9 | Which sub-cells are SUPPRESSED at lock (item 6's rule, applied to R1 item (8)) | **DECIDED at `record`** | **Five cells, SUPPRESSED at lock — counts only: no point estimate, no "directionally", no q-value, no sign.** *Accrual-based:* **direction = bearish** (3 of 42 nights → ≈ **11** at the registered end), **score band 90+** (2 of 42 → ≈ **8**, and PI-010's falling elite count — 12–13/month in May–June down to 2–3 in Aug–Sep — makes even that optimistic), **score band < 80** (1 of 42 → ≈ **4**; a single published row, TJX 2026-06-11, `overall_score` 79.58, just under the nominal qualification cut — §4's band list must gain a `< 80` residual cell so the band decomposition is exhaustive, Correction 9). *Structural, not an accrual gap and never cured by waiting:* **firing arm = polarity-only and = both** (0 of 284 flagged picks; `polarity_unavailable_coverage_low` on 100% of in-scope rows since 2026-06-01, 0 exceptions) and **primary-trigger age 3–5** (0 by the age decay's design; the cell is printed only under the registered **undecayed secondary**, where it is floor-tested at the decision pass like any other descriptive sub-cell — 14 / 11 / 7 picks at days 3 / 4 / 5 in the sealed portion). Projections are taken to the **registered window end** (≈ 160 nights), **not** to the 80-night floor the Steward extrapolated to; no cell crosses 20 under either reading, and the three that clear comfortably (80–85 ≈ 148, 85–90 ≈ 46, all three `dam` terciles ≈ 72 / 84 / 91) are unaffected. **Suppression restricts affirmative reporting only.** A suppressed cell keeps its printed counts, is **never** removed from **§8 clause 6** (a tape stratum with ≥ 20 contributing nights beyond MPE in the opposite sign still blocks CONFIRMED, and the sign must hold in every such stratum — measured counts, not this list, decide which strata qualify) or from **clause 7**, and never by itself makes an endpoint INCONCLUSIVE (§8 clause 1). **Decided now and never revisited:** a cell suppressed at lock stays suppressed even if it clears 20 measured nights at the decision pass — the stricter state, and the one that cannot be re-argued once counts are visible. | **DP-43** (demotion decided at lock, never afterwards), **DP-21** (20 per cell), item 6's four clauses verbatim, Q017 DECISIONS #7 (a)–(d); the two structural zeros are a measurement fact about the input, not a floor |
| 10 | What the 100%-polarity-unavailable finding does to the claim | **DECIDED at `record`** | **A population restriction, not a redefinition.** The trigger field is unchanged (`age_adjusted_severity = 'EXIT'`, item 1); arms, matching, endpoints, MPEs and §8 are untouched. What changes is the sentence the verdict is allowed to carry: over this window the Conviction Monitor's EXIT tier **is the technical arm alone** — 284 of 284 primary flags fired via `technical_overall_tier`, `polarity_tier` is `WATCH` on **every** row dated ≥ 2026-06-01 (0 HOLD, 0 EXIT), and the only polarity HOLD/EXIT rows in the whole freeze are in May 2026. **Three restrictions travel with every restatement of the verdict** — REPORT, LEDGER, the §9 guide line, any brief and any board line: **(i)** the tier as measured is **technical-arm-only**; **(ii)** it is a **day-1 or day-2** event (223 + 61 flags, zero at days 3–5, by the age decay's design); **(iii)** the matched estimate speaks for **ordinary-damage** flags only — 195 of 284 flagged picks (68.7%) are dropped for want of a caliper-matched control and the dropped tail is systematically the more damaged one (mean `dam` −0.94 vs −0.17 ATR), so **no claim is made about the worst drawdowns**. The arm decomposition registered in §4 is reported as **not measurable in this window, with the reason**, never as "the technical arm carries all the information" — that would be a claim about the tier logic where the fact is about data availability. `eval.py` prints the firing-arm composition, the age distribution and the drop rate **by month and by half**, so §8 clause 5's both-halves test is read with the composition in view (the drop share is already moving: 75.9% → 74.0% → 55.9%). | CLAUDE.md rules 5 and 10 (a claim is only as wide as the population it was measured on); **DP-12** — the cost is paid and stated, never softened: the 0.25 ATR caliper is **not** widened to retain the damaged tail, which would be re-tuning a registered definition against measured data; §10 threats 3 and 7, now measured rather than anticipated |
| 11 | Does the dead polarity arm need a PI filing (DP-07)? | **DECIDED at `record`** — yes; the filing itself **ROUTED → registrar** | **Yes — `PI-014`, severity high, status `OPEN`, recommendation fix.** It is a platform defect, not a research question (DP-07): one of the monitor's two arms has been structurally silent since 2026-06-01 while the surface is sold as a two-arm conviction read, and no watchdog caught it — the third silent degradation in the same UOA-side family after PI-001 and PI-002, and the first to reach a paid surface's logic. It is **not** a Q019 finding, enters no PREREG section as one, and changes no arm. The paste-ready entry is in *Routed requests* below: evidence from the pinned freeze only (DP-50(c)), the reproducing check addressed to the **Data Steward** on `$RESEARCH_DB_URL` rather than to the coding agent (DP-49), the cause narrowed to the **input** rather than the tier logic, and the **DP-50(b) timing constraint named in the entry itself**. Both branches of that constraint are written out, because the choice between them is Haci's (DP-07, DP-48), and item 12 says what the desk does in each. | **DP-07** (defects go to `PLATFORM_ISSUES.md` with a recommendation), **DP-48** (the desk files, he decides), **DP-50(b)** (ship timing checked against every in-flight question before a fix brief), **DP-49** (a DB step is never handed to the coding agent) |
| 12 | If polarity coverage returns inside Q019's window | **DECIDED at `record`** | Two limbs, decided now so neither is argued with counts in view. **(a) A dated ship** — a PI-014 fix, or any change carrying a SHA and a `DATA_NOTES.md` entry, that restores an input which had been structurally unavailable and thereby changes **which picks receive `EXIT`** — fires **item 3's window-start move**: the start goes to the first pick night after the ship, the whole §5 schedule is recomputed at the measured rate, and if the recomputed decision date lands after **2027-09-13** Q019 goes to `DEFERRED.md` rather than the ceiling being stretched. Item 3's rule therefore reads "**any dated change to what the tier means — a tier-logic ship *or* the restoration of a structurally-unavailable input**", not "a tier-logic ship" (Correction 11). At `r` = 0.6885 a restart costs ≈ 8 months, so a ship before ≈ **2027-03-08** is survivable and one after it is not. **(b) An undated drift** — coverage recovering on the vendor side with no ship and no SHA — fires **nothing**: there is no date to split on and the desk will not invent one. `eval.py` prints the firing-arm composition **by month**, the report states the measured composition as the claim's population restriction (item 10), and the window, the arms and the gates are untouched. R2 clause (vi) makes the Steward print the monthly polarity share with the successor freeze, so either limb is seen coming rather than discovered at the decision pass. | **DP-06 / DP-50(a)** (a feature that changes meaning mid-window is two features, split at the **dated** ship — the rows carry no engine-version column, so an undated split is not constructible); **DP-43** (the recomputation pushes the date out only, and past the ceiling is DEFERRED); **DP-45** (limb (a) accepts a real risk of DEFERRED rather than quietly blending two populations into one easier sample); limb (b) invents no threshold |

## Corrections to silent choices

**Twelve — six at `decide`, six more at `record` (7–12, from the Steward's measured counts).** The
Registrar applies all twelve at `apply`, with the rest of this file.

Six at `decide`. Two are substantive (a look-ahead in the control definition, and the control pool's own window),
one fixes a denominator the schedule rests on, two apply policy entries added **today** that postdate
the draft, and one is a cross-question flag. Everything else was checked against the policy and
already matches.

1. **§2 (NOFLAG) and §3 B2 — the unflagged label is read from rows dated *after* the exit decision,
   and must not be.** The draft defines NOFLAG as "the pick has ≥ 1 in-scope monitor row and **none of
   them** is EXIT", where in-scope means sessions `t+1 … t+5`. For a control matched at signal session
   `s`, that set includes rows dated `s+1 … t_c+5`, written at 16:02 ET on days **after** the
   `Open_{s+1}` exit — so a control is selected partly on the fact that it was *never subsequently
   flagged*. That is a look-ahead in arm assignment (rule 14 on the draft's own per-decision reading,
   §6), and it biases the contrast **in the hypothesis's favour** by handing the control arm a
   survivorship filter the flagged arm cannot have. **It must read:** a pick is NOFLAG **at session
   `s`** if it has ≥ 1 in-scope monitor row **dated ≤ `s`** and **none of its rows dated ≤ `s`** is
   EXIT under the trigger field. A control that is flagged on a later session stays in the pool for
   `i`'s window, graded with no early exit — that is exactly the choice a holder faces at the open of
   `s+1` (sell the flagged one, or hold a comparable one that has fallen as far and has not been
   flagged **yet**), and it is the only version of the contrast that is legal at the moment it is
   taken. §2's own governing sentence — "arm assignment, decided at the exit moment and never
   revisited" — already says this; the definition below it does not. Applies identically to the B3
   pool (HOLD **as of `s`**) and to the ITT secondary (each pick exits at its own first flag, which is
   prospective and needs no change). **Stated plainly: this repair makes the control pool larger and
   the expected contrast smaller, and it can only raise the measured matched-contributing rate.** That
   is a consequence, not the reason — rule 14 is, and R1 must measure the rate under the corrected
   definition, because the loose definition would report a rate this question is not entitled to.
2. **§3 B2 — the control's own pick night must sit inside the same window.** The draft draws controls
   "from any non-excluded pick night", which admits a control whose pick night precedes the window
   start. Where item 3 moves that start past a tier-logic change, such a control carries a NOFLAG
   label computed by the **old** tier logic (DP-06 / DP-50(a): two features), and at a 2026-06-01
   start it would additionally be a pick made under the pre-fix catalyst layer (DP-06) — in both cases
   the arms would then differ in more than "whether the flag fired", which §3 promises they do not.
   **Must read:** the control's own pick night satisfies the **same window bound and the same
   exclusion tests** as the flagged pick's. The bite is small by construction (a control must carry a
   monitor row on session `s`, so its pick night is within five weekdays of `i`'s) and it is
   one-directional — the pool can only shrink.
3. **§5 — "per session" must be "per elapsed session", and the accrued count must be a count.** The
   bullet mixes two denominators: it computes accrued nights as `58 × r` (58 = non-excluded matured
   nights) and then projects forward over **elapsed** sessions. Measure and project on **elapsed
   sessions** — calendar minus holidays, exclusions **not** pre-removed — which is the lower rate and
   therefore the longer window (the Q018 §5 correction, same shape), and state the accrued figure as
   R1's **measured count `A`**, not as a product of the planning rate. The ceiling inequality in item 4
   is written in `A` and `r` for exactly this reason. Recomputing on non-excluded sessions would give a
   faster rate, pull the window end in and shorten the wait — the move DP-43 and DP-45 forbid.
4. **§9, the implementer bullet and the `INTERNAL_TOOL` brief — DP-49 (added 2026-09-13, postdates the
   draft).** Every check a brief following from this question hands the **coding agent** must be
   satisfiable from the platform repo alone — the test suite, a pure-function import, `git show
   --stat`, a file diff. Anything that reads or writes a table belongs in the brief's verification
   section addressed to the Data Steward on `$RESEARCH_DB_URL`, or to Haci where a write is required;
   a "prove you didn't change the tier logic" check is written as the diff that proves it, never as
   "re-run the monitor and compare". Add that sentence to the bullet.
5. **§9, the `PLATFORM_ISSUES.md` filings — DP-50(b) (added 2026-09-13).** The draft's §10.5 carries
   the desk side of DP-50 ("any repair that touches this table must be checked against this question's
   decision date"), but the two §9 filings — the CONFIRMED-negative branch that sends the surface to
   `PLATFORM_ISSUES.md`, and the NULL-with-large-B4 branch that registers its own question — must name
   the constraint **in the PI entry itself**: a repair to the tier logic (`conviction_monitor_service.py`
   `:328-620`, `:736-785`, `:792-804`, or the age decay at `:50-56` / `:807-811`) is **flag-off until
   Q019's decision date** (the PI-011 / Q010 pattern), and if it ships inside the window anyway it
   takes a dated `DATA_NOTES.md` entry naming the column, the date range and the ship SHA, and the
   tier column becomes **two features split at the ship date** (DP-06 pattern, DP-50(a)) — which fires
   item 3's window-start move, mid-flight, with the DEFERRED branch live.
6. **Cross-question flag, not a Q019 edit — the F6 count.** Q019 §7 puts the F6 correction set at
   **15** (Q003 2 + Q009 2 + Q012 3 + Q015's 2 companion + Q018 4 + Q019 2) and that arithmetic is
   **correct**: Q003 is filed **F6** with 2 primaries (`Q003_repeat_selection/PREREG.md` header and
   §7). **Q018 §7 and its DECISIONS entry put F6 at 11 and omit Q003's 2** — they should read 13 at
   Q018's registration. Q018 is still `PREREG_DRAFT`, so the Registrar corrects it there; **Q019 §7
   stands as drafted** and needs no change. Both files already say the set is computed at the decision
   pass over the F6 primaries **locked by then**, so this is a stated-expectation error rather than a
   live mis-correction, but it should not survive into a locked file.

**Added at `record` (2026-09-13), on `STEWARD_Q019_exposure.md`:**

7. **Header status line and §5's planning-rate bullet — the conditionality is spent and must not
   survive into a locked file.** The header reads "**conditional on R1** … if the measured rate is
   below 0.26 nights per session, Q019 goes to `DEFERRED.md`", and §5 states 0.35 as a planning
   assumption. **They must read:** R1 measured **`A` = 42** matched-contributing nights over **61**
   elapsed sessions (June 12 / July 12 / August 18), **`r` = 0.6885**, under the Correction 1
   NOFLAG-at-`s` definition and the Correction 2 window bound; the `r ≥ 0.26` test is **passed**, the
   window start is confirmed at **2026-06-01** (last tier-logic ship 2026-05-16), and the drafted
   window end, decision date and extension date **stand unmodified** because a faster rate never pulls
   a date in (DP-43, DP-45). Keep the 0.35 figure visible as the *planning* rate that set the dates, so
   a reader can see that the registered window is ≈ 2× the floor by construction and not by accident.
   §5's R1 request block is kept and marked **answered**, with the report path cited.
8. **§4's sub-cell list — add the `< 80` residual band cell.** §4 names the bands as
   80–85 / 85–90 / 90+, but the population is every published pick (DP-28's predicate is
   `qualified IS TRUE AND selected_rank IS NOT NULL`, not a score floor) and the freeze holds one
   published row at **79.58** (TJX, 2026-06-11). **Must read:** a fourth, residual `< 80` cell, so the
   band decomposition is exhaustive and no pick is silently absent from it; the cell is **SUPPRESSED at
   lock** (item 9), counts only. The row stays in the population and in both primaries — it is a
   published pick — and is never dropped to tidy the band list.
9. **§4's arm decomposition and age sub-cell — record their structural emptiness, keep the bullets.**
   The "which arm fired" secondary promises the read that says "whether one of the two arms carries all
   of the information", and the age 1–2 vs 3–5 sub-cell promises a split the primary trigger cannot
   supply. **Must read:** both bullets stay registered, with the measured fact stated at lock — polarity
   contributed **0 of 284** primary flags over 2026-06-01..2026-08-26 and `polarity_tier` is `WATCH` on
   every row dated ≥ 2026-06-01, so the decomposition is **not measurable in this window**, and the
   primary trigger's age cell is **empty by the age decay's design** and is printed only under the
   undecayed secondary. A registered secondary is reported as unmeasurable **with its reason**, never
   quietly dropped and never restated as a finding about the tier logic.
10. **§1, §8 and §9 — the three population restrictions must appear where the verdict is stated, not
    only in §10's threat list.** Item 10's (i) technical-arm-only, (ii) day-1-or-2, (iii)
    ordinary-damage-only. In §9 the guide line and the `INTERNAL_TOOL` brief carry them verbatim beside
    the measured number, because a subscriber-facing sentence inherits the population it was measured
    on (rule 10). In §8 they are stated as scope, not as gates — they change no threshold.
11. **§5, §10 threat 4 and §11 item 3 — the window-start rule covers a dated *restoration*, not only a
    tier-logic ship.** Threat 4 anticipates six named code changes; the measured hazard is the mirror
    image — an input that has been dead since before the window and could come back inside it.
    **Must read:** the window start moves on **any dated change to what the tier means, a tier-logic
    ship or the restoration of a structurally-unavailable input**, with the date taken from the ship
    SHA and its `DATA_NOTES.md` entry; an undated recovery moves nothing and is printed by month
    (item 12). §10.5's DP-50(b) filing sentence (Correction 5) extends to the polarity input for the
    same reason.
12. **§2 and §10 threat 8 — record the measured in-window zero for the published/monitored gap.** The
    draft leans on the full-history 915-published-vs-907-qualified gap. Measured in this window: **0 of
    465** published picks have zero in-scope monitor rows, 0 lack `C_t`, 0 lack 60 prior daily bars, 0
    of 284 flagged picks lack forward bars, 0 nights exceed the 25%-ungradeable rule, and **0** monitor
    rows fail the §2 point-in-time guard (all 160 failures in the freeze are May 2026, pre-window).
    **Must read:** the monthly print stays — it is a diagnostic, not a claim — with the sealed in-window
    figure recorded as zero so the successor nights are compared against something.

Checked and **not** corrections — each already matches the policy: **MPE 0.25 ATR** on P1, the
standing number for a per-trade ATR-denominated endpoint, per flagged trade and never rescaled
(DP-10, DP-44) and **+5.0 pp** on P2, the standing number for a control-adjusted touch-rate endpoint
(DP-20, DP-44), with no uplift proposed and no money-unit MPE invented; sessions-to-touch and the
excursion panel descriptive with no MPE (DP-44); floors read as **≥ 80 contributing nights per primary
endpoint**, P1 and P2 sharing the §2 definition, and 20 per cell — the stricter reading (DP-21);
**≥ 30 contributing nights dated after the lock commit**, never reduced, and DP-31 correctly **not**
invoked because PROSPECTIVELY_CONFIRMED is reachable from this run by design (DP-24, DP-31); the
**damage-matched** contrast primary with the total effect descriptive and §8 clause 7 making the
matched form the verdict (DP-12, and DP-12's cost paid in §2's drop-and-count rather than softened);
entry **`X = C_t`** for picks and controls alike on an already-held position, with the after-hours
price a picks-only sensitivity (DP-11, DP-03), and the estimands entry-free by construction; the
publication predicate `qualified IS TRUE AND selected_rank IS NOT NULL` with dark-lane rows in no arm
(DP-28); the newest exclusions file read from JSON with no hard-coded dates (DP-22, extended by item
5); **ten sessions** taken from H-050 as written and not re-united, with `t+5`/`t+20` as sensitivities
(DP-25); registrar conventions fixed before any outcome is seen — the ±1 ATR levels, the 0.25 ATR
caliper, the 5-nearest match, the 5-session block length, the expanding-window tape terciles (DP-26);
**same-session ties adverse-first** (DP-27) — the draft's *symmetric* application to both arms is
DP-27 applied literally and is kept: an arm-dependent tie rule is manipulable, the effect on a
difference of rates is second-order, the opposite reading is printed as a sensitivity, and the tie
path is rare and symmetric here because **both arms are published picks** with measured 100% hourly
coverage (`STEWARD_Q015_exposure.md` §7); stops never used as exits, counter-direction touches
reported (DP-02), and DP-30 not engaged because the adverse level is the desk-standard −1 ATR line,
not the printed stop; family **F6** by the primary endpoint's subject with H-050 counted once and Q010
excluded as a replication (DP-29); one automatic extension then DEFERRED, firing on `eval.py`'s
measured counts and never on a projection (DP-13); successor freezes covering **every** candidate
symbol, published and unpublished, plus hourly bars for published symbols (DP-23); every basis
labelled **NON_QUOTABLE** (rule 12); regime used only for nights ≥ 2026-06-09, v1.2, same-evening rows
(rule 7, FREEZE_v001 §7); **no rule-14 exception requested or needed** — the monitor row is a 16:02 ET
`lag_sessions: 1` feature used for a `t+1`-open decision, so DP-05 is untouched and DP-41 respected;
and the exposure count specified on the pinned freeze rather than a live query (DP-50(c)).

## Defaulted on Haci's behalf

- #4 Planning rate, window end and the DEFERRED trigger — chose **0.35 matched-contributing nights per
  elapsed session, window 2026-06-01..2027-05-03, decision Monday 2027-05-24, one extension to
  ..2027-06-15 decided Monday 2027-07-12, DEFERRED if the measured rate cannot reach 80 nights by
  2027-09-13**; not taken: descriptive read on the ≈20 nights already frozen, answered in weeks —
  DP-43. Overturn = successor question.

**At `record` (2026-09-13): nothing new was defaulted.** Item 4's default is now *resolved on
measurement* — `r` = 0.6885 put Q019 in its third branch, so the defaulted dates stand exactly as
written, and items 7 and 9–12 were settled on measured counts against existing entries (DP-43, DP-45,
DP-06/DP-50(a)(b), DP-07, DP-48, DP-49, DP-12, DP-21), not on Haci's behalf. One consequence of the
default belongs on the board with it: **the desk will wait until 2027-05-24 for a question whose
80-night floor the measured rate reaches around 2026-11-14** — roughly six extra months, and a
registered window ≈ 2× the floor. That is the price of a schedule drafted before its exposure was
measured; DP-43 and DP-45 forbid paying it back by moving a locked date, so the fix is in the drafting
order (Standing rules proposed), and his overturn — if he wants the answer sooner — is a successor
question, never an edit to this one.

Nothing else was defaulted. Items 1–3 — the Registrar's whole open list — each met a DECIDE ground
and none is a question about how Haci trades: item 1 is the product's own field (and DP-42 gives the
same answer if it is read as R-2), item 2 is rule 5's baseline, item 3 is DP-06's two-features rule
plus arithmetic. Item 4 is the one place the desk spends his waiting: this is a **live product
surface** the platform sells and that no desk number has ever touched, and the desk has chosen to say
nothing about it for **at least 8.4 months** — and possibly to defer it outright — rather than publish
a read on the ≈20 contributing nights the freeze may already hold. DP-43 forbids the shorter window
and DP-45 forbids taking it because the date comes sooner; the honest alternative, if he wants
something before then, is a **descriptive** internal read filed as an enhancement with rule 10's
limitation stated, not a verdict. No floor, arm, gate or clause was weakened anywhere in this file,
and Correction 1 removes a look-ahead that would have flattered the hypothesis.

## Routed requests

### data-steward — R1 (counts only) — **ANSWERED 2026-09-13**, `research/reports/STEWARD_Q019_exposure.md`

**Closed.** All ten items returned; the request is kept below verbatim as the record of what was asked
before any number was seen. Headline: `A` = **42**, `r` = **0.6885**/elapsed session, last tier-logic
ship **2026-05-16**, window start stays **2026-06-01**, call = **LOCK** on the unmodified drafted
schedule (item 7). Items (4), (5), (6) and (8) are the measured facts that narrow the claim and set the
suppression list (items 9 and 10); item (9) confirms 100% hourly coverage in **both** arms, so the
DP-27 tie path is rare and symmetric as §3 B2 predicted; item (10)'s DP-50(a) sweep is clean.

### data-steward — R1, as issued at `decide` — **BLOCKING FOR LOCK**; settles the schedule and the lock-or-DEFER call

Q019 (Conviction Monitor EXIT vs holding to the tenth session, PREREG §5 request R1) needs a
**counts-only** exposure measurement on the **frozen** data — `research/data/manifest_v001.json`
(table key `conviction_monitor`) + `research/data/manifest_prices_v001.json`, never a live query
(DP-50(c)) — and it is **blocking for lock**: no desk report has ever counted a monitor tier, so this
question cannot be scheduled without it. **No outcome of any kind:** no touch, no ±1 ATR race, no
return, no plan result, no avoided move, and no tier-versus-outcome cross-tab. The read boundary is
explicit and is the only place this differs from previous requests — bars **up to and including the
close of session `s`** may be read, because `dam = dir × (Close_s − C_t)/ATR` is the *conditioning*
variable and is legal at the exit decision; **no bar dated after session `s`** may be read except to
establish that a bar *exists* (maturity and gradeability). Population: published picks (`qualified IS
TRUE AND selected_rank IS NOT NULL`, DP-28; dark-lane rows in no arm) on pick nights **2026-06-01**
through the last night whose session `t+10` has matured on `manifest_prices_v001` (**2026-08-26**),
with the nights in `research/data/exclusions_v003.json` (`manual_runs` ∪ `non_session_runs` ∪
`uncorroborated_publication_runs`) and DP-04 re-run nights removed; report pick-night-only quantities
through **2026-09-10** as well. **One definition differs from the draft PREREG and must be used as
written here** (DECISIONS Correction 1, a knowledge-time repair): a pick is **NOFLAG at session `s`**
if it has ≥ 1 monitor row dated `≤ s` in sessions `t+1 … t+5` and **none of its rows dated `≤ s`** is
EXIT under the trigger field — rows dated after `s` are written at 16:02 ET on later days and may not
be read to select a control; a pick flagged on a later session is still a valid control at `s`.
Controls must additionally come from a pick night **inside the same window and passing the same
exclusion tests** (Correction 2). Please return: **(1)** the §2 funnel night by night — matured pick
nights, eligible published picks after each exclusion, published picks with **zero** in-scope monitor
rows (the `qualified`-vs-published gap, FREEZE_v001 §1), picks with no `C_t`, symbols with fewer than
60 daily bars dated ≤ `t`, picks with missing forward bars or no `Open_{s+1}`, nights where more than
25% of eligible picks are ungradeable, and immature nights; **(2) FLAG picks and FLAG nights** under
the primary trigger **`age_adjusted_severity = 'EXIT'`** (earliest row in sessions `t+1 … t+5`) and,
separately, under the undecayed **`overall_tier = 'EXIT'`**, with the age (`days_since_qualified` and
the session distance from `t`) distribution of the first flag under each; **(3)** **matched-contributing
nights and their rate per *elapsed* session, by month** — a night with ≥ 1 eligible FLAG pick that
clears the §3 B2 caliper (`|dam_c − dam_i| ≤ 0.25 ATR`, `|age_c − age_i| ≤ 1` weekday, same session
`s`, different symbol) with ≥ 1 valid control, denominator **elapsed sessions** (calendar minus
holidays, exclusions **not** pre-removed — DECISIONS Correction 3), together with the **absolute count
`A`** of such nights accrued to 2026-08-26; **this is the number that decides whether Q019 locks at
all** — the window end is `2026-08-26 + 1.4484 × (80 − A)/r` days and the decision date 21 days after
it, and **if that date is after 2027-09-13 the question goes to `DEFERRED.md` instead of being
locked** (DP-43's 12-month ceiling; `r ≥ 0.26` is that inequality's solution at `A = 58r` only), while
a rate **faster** than the 0.35 planning rate changes nothing (DP-43, DP-45 — a date never moves in
and no floor is lowered to meet one); **(4)** flagged picks **dropped for no valid control**, as a
share and with the `dam` distribution of the dropped and of the retained (DP-12's stated cost, §10.7);
**(5)** monitor rows failing the §2 point-in-time guard — `created_at` not on the row's own
`trading_date` before the next session's open, or `updated_at` more than one minute after `created_at`
— by month, and how many picks lose their only flag row to it; **(6)** `technical_overall_tier =
'UNKNOWN'` and polarity-unavailable shares by month, and the share of WATCH rows whose only reason
code is an availability code; **(7)** **the platform git history of the tier logic** — from the
read-only platform repo, `git log --follow services/conviction_monitor_service.py` — dating every
change to the tier rules with SHA and date, specifically the "Fix 1–6" work (the ATR breach buffer
`:86`, the info/weak recategorisation `:388-446`, the dedupe `:627-638`, the concurrence rollup
`:736-785`, the aged-TF cap `:98-104`, the orientation gate) and the age decay (`:50-56`, `:807-811`);
if the **last** such change is dated after 2026-06-01, **the window start moves to the first pick
night after it** and item (3) is recomputed from that start (DECISIONS #3; DP-06, DP-50(a)) — the
rows carry no engine-version column, so this git history is the only way to see it; **(8)** the FLAG
picks' splits for the DP-43 demotion call — **direction (bull/bear), score band (80–85 / 85–90 /
90+), `dam` tercile, age 1–2 vs 3–5, and which arm fired (`polarity_tier = 'EXIT'` vs
`technical_overall_tier = 'EXIT'` vs both)** — each as *matched-contributing nights*, not picks, so
sub-cells projected below 20 nights can be SUPPRESSED at lock rather than at the decision pass;
**(9)** hourly-bar coverage over sessions `s+1 … t+10` for the symbols in **both** arms, confirming
that `p001_hourly_raw`'s published-symbol scope covers the control arm too (both arms are published
picks, so the DP-27 tie path should be rare and symmetric — say so if it is not); and **(10)** under
**DP-50(a)**, any commit since the manifest SHA `fa70688` touching the monitor's write path or tier
logic, since a repair there rewrites the same rows this freeze pinned. Items (3) and (7) settle the
window end, the decision date, the extension date and the lock-or-DEFER call at `record`; item (8)
settles which sub-cells are demoted at lock; items (4) and (5) are the two measured facts that could
make the question speak for a narrower population than it claims, and they go in the report whatever
they say. **R1 may push every date out; it can never pull one in.**

### data-steward — R2 (successor freezes) — due before the decision pass, **not** a blocker for lock — **extended at `record` (2026-09-13)**

**Two clauses added at record, to be read as part of the request below.** **(vi) Monthly polarity
composition, counts only.** With each successor selection freeze, please report by month, for the
in-window `conviction_monitor` rows: the share carrying `polarity_unavailable_coverage_low`, the
`polarity_tier` distribution (HOLD / WATCH / EXIT / UNKNOWN), the `technical_overall_tier = 'UNKNOWN'`
share, and the firing-arm split of primary `age_adjusted_severity = 'EXIT'` flags (technical-only /
polarity-only / both). Q019's claim scope is a **measured** population restriction (DECISIONS #10), not
an assumption, so it has to be re-measured on the successor nights; a recovery with no ship date
changes no window, no arm and no gate (DECISIONS #12(b)) but it must be **printed**, and a recovery
that makes polarity-fired EXITs non-trivial is stated in the decision paragraph as a composition
change. **(vii) The dated SHA of any restoration.** Under DP-50(a)/(b), if a change that restores
polarity coverage — or otherwise alters which picks receive `EXIT`, including any edit to
`services/symbol_context_builder.py:136-175`, `ConvictionMonitorConfig.polarity_coverage_threshold`, or
the `uoa_contract_daily` write path — ships between the freezes, report its SHA and date and open a
dated `DATA_NOTES.md` entry naming the column and the date range. That date fires **DECISIONS #12(a)**'s
window-start move mid-flight, with the DEFERRED branch live; an undated drift fires nothing.

Q019 (PREREG §5, request R2, DP-23) needs successor freezes before its decision pass — **Monday
2027-05-24** as drafted, or the later date R1 fixes at `record`. Please build and pin `manifest_v002`
(selections; the same SQL and the same exclusion criteria as v001, **including the `conviction_monitor`
table key** — this question's arm assignment lives in that table and a successor freeze without it is
useless here) and `manifest_prices_v002` (the same Alpaca queries) covering pick nights after
**2026-09-10** through Q019's registered window end (**2027-05-03** as drafted); a second pair is
built **only if** the single DP-13 extension fires, then covering through **2027-06-15**, and not
before. Five scope requirements, none optional: **(i)** the daily symbol list covers **every candidate
symbol on every in-window night, published and unpublished** (DP-23), never assumed from v001's symbol
list, with **60 prior daily bars** dated ≤ `t` (ATR14, beta60, runup20 — the platform's `atr_pct` is
split-corrupted, PI-003, and must not be used) and forward bars running **at least 20 sessions beyond
the last included pick night** (10 for the primaries, 20 for the registered `t+20` shape sensitivity);
**(ii) hourly bars for all published symbols** over `t+1 … t+20`, for the §4 same-session ordering —
where they are missing the pair falls to DP-27 (adverse-first) and is counted, per arm; **(iii)** the
`conviction_monitor` rows for every in-window night **with `created_at` and `updated_at` carried**, so
the §2 point-in-time guard can be applied row by row on the successor nights exactly as on the pinned
ones; **(iv)** a **successor exclusions file** (`exclusions_v00N`, DECISIONS #5) issued with the
selection freeze, applying the identical three criteria to the post-lock nights, **add-only** — it may
add nights and may never remove one from a v003 list; and **(v)** under **DP-50(a)**, any platform
commit between the freezes that rewrites historical rows in `conviction_monitor_daily` or changes the
tier logic, the age decay, `days_since_qualified`, the monitor's load predicate
(`:1043-1051`) or the publication predicate, with a dated `DATA_NOTES.md` entry naming the column, the
date range and the ship SHA — the successor freeze re-runs the same SQL against the same tables
(DP-50), so such a repair silently changes what this question's arms mean and splits the tier column
into two features at the ship date, which fires DECISIONS #3's window-start move mid-flight. Rows
whose bars are missing are **excluded and counted, never back-filled or imputed**. Please also
re-confirm every §5 date **session by session from the trading calendar** when the freeze is built —
the holiday list used here is 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26,
2027-05-31, 2027-06-18, 2027-07-05 — and a correction to any date may move it **out, never in**.

### registrar — file `PI-014` in `research/PLATFORM_ISSUES.md` (opened at `record`, DECISIONS #11; DP-07, DP-48)

Please add the row and the detail block below. It is a **platform defect found while doing Q019's own
work**, not a Q019 finding, and it enters no PREREG section. Next free id is **PI-014**. Paste-ready:

```
| PI-014 | high | OPEN | Conviction Monitor's polarity arm silent since 2026-06-01: `polarity_unavailable_coverage_low` on 100% of in-scope rows, 0 polarity HOLD/EXIT rows — the EXIT tier is the technical arm alone |
```

> ### PI-014 — the Conviction Monitor's polarity arm has been dark since 2026-06-01
> **Evidence:** `research/reports/STEWARD_Q019_exposure.md` §6 and §8, counts only, on the pinned
> freeze (`manifest_v001`, table key `conviction_monitor`, 3,339 rows; no live query, DP-50(c)).
> `polarity_unavailable_coverage_low` appears in `reason_codes_json` on **100% of in-scope monitor rows
> in every month 2026-06 through 2026-09**, with **0 exceptions**; `polarity_tier` is `WATCH` on
> **every** row dated ≥ 2026-06-01 (0 HOLD, 0 EXIT); the only 35 polarity-EXIT and 53 polarity-HOLD rows
> in the whole freeze are in **May 2026**, when the arm still worked (80.3% unavailable then, so it was
> already degrading). Consequence: **284 of 284** primary EXIT flags on pick nights
> 2026-06-01..2026-08-26 fired via the technical arm alone, on a tier that prints EXIT for **61%** of
> published picks within five sessions.
> **This is not the 2026-05-16 polarity rollback.** `docs/POLARITY_ROLLBACK_2026_05_16.md` disabled
> v1.6 polarity **in SAS scoring** by flipping `SuperAgentSelectConfig.flow_polarity_enabled` to
> `False`. The monitor does not read that flag — it recomputes polarity locally
> (`services/conviction_monitor_service.py:906-937`, `:1177-1186`) — and it kept writing polarity
> HOLD/EXIT rows for two weeks *after* the rollback shipped, dying at the 2026-05-31 / 06-01 boundary.
> A "working as intended" reading of the silence is wrong.
> **Cause (read-only, and not in the monitor):** the monitor's tier code has not changed since
> **2026-05-16** — `git log --follow services/conviction_monitor_service.py` returns exactly three
> commits, all that day (13234cc / baf17b8 / 2cb7a7e), and nothing since; `scripts/run_conviction_monitor.py`
> and `routers/conviction_monitor.py` show no commits since the manifest SHA `fa70688`. So this is an
> **input** failure, not a logic change. The gate is `services/conviction_monitor_service.py:184-185` —
> `coverage is None or coverage < config.polarity_coverage_threshold → ("WATCH", ["polarity_unavailable_coverage_low"])`
> — where `coverage_ratio = decomp_premium_total / contract_premium_total` (`:928-937`) is built by
> `services/symbol_context_builder.py:136-175` from **`uoa_contract_daily.buy_premium` /
> `sell_premium` / `premium_total`**. A 100% failure means the **aggressor decomposition** is empty or
> near-empty for the monitored symbols on every date since 2026-06-01, or `premium_total` has been
> inflated relative to it. Same table family as **PI-001** (`uoa_symbol_daily` write degradation from
> 2026-05-20, still ~5% of baseline) and still uncovered by any watchdog (**PI-002**) — the third silent
> UOA-side degradation, and the first to reach a paid surface's logic.
> **Reproducing check — for the Data Steward on `$RESEARCH_DB_URL`, read-only.** `uoa_contract_daily` is
> **not** in `manifest_v001`, so this is an operational diagnosis, not a study input and not a brief's
> before-snapshot; it is addressed to the Steward and never to the coding agent (DP-49). By month from
> 2026-04-01, over the SAS published-pick symbols: the share of `uoa_contract_daily` rows with
> `buy_premium + sell_premium > 0`, the median `(buy_premium + sell_premium) / premium_total`, the row
> count per date, and the date the median first falls below `polarity_coverage_threshold`. Plus, from
> the read-only platform repo, `git log --follow services/symbol_context_builder.py` and any change to
> `ConvictionMonitorConfig`'s polarity thresholds between 2026-05-20 and 2026-06-10 — R1 item (7) dated
> the monitor service only, so the builder and the config are the two unexamined code paths. If a fix is
> briefed, pin that coverage aggregate in the successor freeze so the before/after is reproducible
> (DP-50(c)).
> **Desk impact:** Q019 (locked 2026-09-13, decision 2027-05-24) tests "the Conviction Monitor's EXIT
> tier" and therefore tests **the technical arm alone** for the life of its window; the restriction is
> written into its §1/§8/§9 and travels with the verdict (Q019 DECISIONS #10). No other locked question
> reads this table.
> **Recommend: fix — and fix the input, not the gate.** The coverage threshold is doing its job;
> lowering it would publish a polarity tier computed from a fraction of the premium. **DP-50(b) timing
> constraint, named here as the policy requires:** restoring polarity changes which picks receive
> `EXIT` — a column a locked PREREG reads — so the PI-011 / Q010 pattern applies and the choice is
> Haci's. **Either** the restoration is held **flag-off until Q019's decision date, 2027-05-24**; **or**
> it ships with a dated `DATA_NOTES.md` entry (column, date range, ship SHA), Q019's window start moves
> to the first pick night after the ship and its schedule is recomputed at the measured 0.6885
> nights/session — ≈ 8 months to refill the floor — and if that pushes the decision date past
> **2027-09-13**, Q019 goes to DEFERRED (Q019 DECISIONS #12(a), DP-43's ceiling). On the arithmetic, a
> ship before ≈ **2027-03-08** is survivable and one after it is not. **The desk does not ask for the
> fix to be held**: a live surface with one of its two arms silent is worse than a research question
> that may have to restart. The cost is written here so the choice is made with it in view.

## Schedule

**FINAL — filled at `record` (2026-09-13) on `research/reports/STEWARD_Q019_exposure.md`. Every value
below is final for the lock; none is provisional and no item is pending.** The Registrar writes them
verbatim to `research/questions/Q019_conviction_monitor_exit/schedule.json` at `apply` / lock (DP-46),
with `check_from` = the decision date so the queue surfaces it (the Q021 convention). R2's
session-by-session calendar re-confirmation when the successor freezes are built may move these dates
**out, never in**.

decision_date: **2027-05-24** (Monday) · extension_date: **2027-07-12** (Monday) · hard_stop: **none**
(DP-13's single automatic extension, then DEFERRED, replaces it — the 2027-07-12 pass is the last one) ·
rule: **fixed** (see the note below — the dates were *derived* exposure-driven at draft and are
**not** re-derived at the measured rate) · window: pick nights **2026-06-01 .. 2027-05-03** (extended:
.. **2027-06-15**) · extended: **false** · maturity: **10 sessions** · gates: **≥ 80 contributing
nights per primary endpoint** (P1 and P2 share §2's definition — a night with ≥ 1 eligible FLAG pick
that is gradeable and has ≥ 1 valid matched control, DP-21) **and ≥ 30 contributing nights dated after
the lock commit** (DP-24), on `eval.py`'s measured counts at the single decision pass · ceiling:
**cleared** — 2027-05-24 is **8.4 months** after the 2026-09-13 lock and the extended date 2027-07-12 is
**9.97 months**, both inside DP-43's 12 months.

- **Why `rule: fixed` and not `exposure-driven`.** The window end was *derived* from accrual at the
  0.35 planning rate, but at the measured 0.6885 it no longer tracks accrual: the floor is reached
  around **2026-11-14** and the registered end sits ≈ six months past it, projecting ≈ **160**
  contributing nights against a floor of 80. The end is therefore a **fixed calendar date** from lock
  onward, not an accrual target — stating it as exposure-driven would imply it still moves with the
  rate, and it only ever could have moved **out**. The one accrual-sensitive mechanism left is DP-13's
  single extension, which fires on `eval.py`'s **measured counts** at the decision pass and never on a
  rate or a projection. **And the longer window is not only the rule's answer, it is the better one:**
  a recomputed 2026-12-05 pass would sit ≈ 2.5 months after lock with ≈ 30 post-lock nights — exactly
  at DP-24's floor, no margin, one slow patch from firing the extension — and would read an exit rule
  over a single autumn tape, which rule 7 and §8 clause 6 exist to prevent. The registered window
  spans a full year of tape strata and leaves ≈ 111 post-lock nights. The cost of the wait is real and
  is named on the board; the benefit is not nothing.
- **Lock-or-DEFER, settled (item 7).** `r` = 0.6885 ≥ 0.26 → the ceiling test passes and the DEFERRED
  branch does not fire. Last tier-logic ship 2026-05-16 → item 3 does not fire and the window start
  stays 2026-06-01. `r` ≥ 0.35 → item 4's third branch → **nothing moves**. **LOCK.**
- **Arithmetic, re-derived independently at `record` and in agreement with the Steward.** Elapsed
  sessions 2026-06-01..2026-08-26 = **61** (June 21, July 22, August 3–26 = 18; Juneteenth Friday
  2026-06-19 and the observed Independence Day Friday 2026-07-03 removed) — the Steward's count exactly,
  and the exclusions are **not** pre-removed (Correction 3). `A` = **42** (June 12, July 12, August 18),
  `r` = 42/61 = **0.6885**. Window end **2027-05-03** + 10 sessions = **2027-05-17** + one week =
  **Monday 2027-05-24**. Extension: 2027-05-03 + 30 sessions = **2027-06-15** (Memorial Day 2027-05-31
  removed) → + 10 sessions = **2027-06-30** (observed Juneteenth Friday 2027-06-18 removed) → + one
  week = 2027-07-07 → first Monday on or after = **Monday 2027-07-12** (2027-07-05 is the observed
  Independence Day holiday). The full registered window is ≈ 61 + 172 = **233** elapsed sessions →
  ≈ **160** contributing nights at the measured rate.
- **Both gates, projected on measured counts — neither is binding.** The 80th contributing night lands
  near **2026-11-14** and DP-24's 30th post-lock night near **2026-11-15** (≈ 111 post-lock contributing
  nights are projected by the window end), both about six months before the decision pass. So
  **PROSPECTIVELY_CONFIRMED is reachable from this run by design, DP-31 does not apply, and no successor
  replication question is needed** — as §5 anticipated at the much slower planning rate. The gates still
  fire on `eval.py`'s counts at the pass, never on this projection (DP-13).
- **Suppression at lock (item 9), fixed now and never revisited.** Five cells, counts only: **bearish**,
  **90+**, **< 80** (accrual), and **polarity-only / both firing arms** and **primary-trigger age 3–5**
  (structural). Suppression restricts affirmative reporting only — every §8 gate, including clause 6's
  tape-stratum test and clause 7, reads measured counts and is untouched by this list.
- **DEFERRED fallback.** If either primary's gates are still short after the single extension at
  **2027-07-12**, Q019 goes to `research/questions/DEFERRED.md` with the measured counts. No second
  extension, no reduced gate, and a gate shortfall is **not** INCONCLUSIVE (§8). On the measured rate
  this is remote; it is kept because the gate fires on counts, not on a rate.
- **The one live route back to DEFERRED (item 12(a)).** A **dated** change that restores polarity
  coverage — or otherwise alters which picks receive `EXIT` — inside the window moves the window start
  to the first pick night after the ship and recomputes the schedule; past **2027-09-13** the answer is
  DEFERRED. A ship before ≈ 2027-03-08 is survivable, after it is not. An undated drift moves nothing.
- **Not DEFERRED now.** The initial decision date is 8.4 months out, inside DP-43's 12-month ceiling, so
  the ceiling clause does not fire.

**The decide-time derivation, kept as the record of the planning-rate schedule** (superseded in nothing
— every date below survived the measurement unchanged; only `A` and `r` were assumptions and both came
in faster). Arithmetic checked independently at that run and it agrees with the draft, on the calendar's
own counts rather than the draft's. Elapsed sessions 2026-06-01..2026-08-26: June **21** (Juneteenth,
Friday 2026-06-19, removed) + July **22** (Independence Day observed Friday 2026-07-03, removed) +
August 3–26 **18** = **61**; minus the three in-window exclusion nights (2026-06-26, 2026-07-02,
2026-07-06) = **58** non-excluded matured nights, the draft's figure. At the 0.35 planning rate,
`A ≈ 20`, 60 more nights = 172 sessions = 249 calendar days at 365/252 → **2027-05-02** (Sunday), so
the draft's **2027-05-03** window end is one day **later** — out, never in. Window end + 10 sessions =
**2027-05-17**, + one week = **2027-05-24**, already a Monday → decision **2027-05-24**. Extension:
2027-05-03 + 30 sessions = **2027-06-15** (Memorial Day 2027-05-31 removed) → + 10 sessions =
**2027-06-30** (Juneteenth observed Friday 2027-06-18 removed) → + one week = 2027-07-07 → first
Monday on or after = **2027-07-12** (2027-07-05 is the observed Independence Day holiday and is not a
Monday the desk would use in any case). Ceiling test: 2026-08-26 → 2027-09-13 is **383** days, and
`1.4484 × (80 − 58r)/r + 21 ≤ 383` solves to **`r ≥ 0.26`** — at `r = 0.26` the decision date lands
2027-09-12, one day inside. Both the draft's dates and its threshold reproduce exactly. The Steward
re-confirms session by session at `record` and again when the successor freezes are built.

## Standing rules added

_none._ Nothing here is Haci's word: items 1–3, 5 and 6 were DECIDED on existing entries and
precedent, and item 4 was DEFAULTED under DP-43, which adds no DP entry (DP-40). **At `record`: still
none** — a DEFAULTED item never becomes a DP entry whatever the measurement says about it, and items 7
and 9–12 are applications of DP-43, DP-45, DP-21, DP-12, DP-06/DP-50(a)(b), DP-07, DP-48 and DP-49,
not new policy. The generalisable ones are listed below as **proposals**, for him to confirm or drop.

## Standing rules proposed

- **An arm label read from a per-day product table is evaluated with rows dated ≤ the decision
  session, for treated and control alike.** "X did not happen" means "X has not happened **yet**", not
  "X never happened": defining the control arm over the subject's whole future window is a
  survivorship filter that always flatters the signal under test. Q019 is the first question whose
  arms come from a daily-written table, and it will not be the last (the monitor, future alert or
  regime-flag tables); stating it once stops it being re-derived.
- **A question whose arms come from a table the desk has never counted treats its exposure request as
  blocking for lock, not as a `record`-time confirmation.** Q017 and Q018 could borrow a measured
  funnel; Q019 cannot, and the difference is the difference between a schedule and a guess. Worth a DP
  entry so the Registrar knows at drafting time which of the two shapes it is writing.
- **A live product surface that no desk number has ever touched, and whose research answer is more
  than six months out, is worth an explicit descriptive internal read in the meantime** — filed as an
  enhancement under rule 10's limitation, never as a verdict. Q019 leaves the Conviction Monitor
  unexamined until at least 2027-05-24; that is correct for the *claim* and uncomfortable for the
  *product*, and the desk should have a standing answer to the gap rather than re-arguing it per
  question.

_Added at `record` (2026-09-13) — proposals, not policy; a DEFAULTED or record-only item adds no DP
entry (DP-40):_

- **The blocking exposure count comes before the schedule is drafted, not after.** Q019's planning rate
  was 0.35 and the truth was 0.6885, so the registered window is ≈ 2× its floor and the desk waits ≈ six
  months longer than it needs to — and no rule permits fixing that, because a locked date may only move
  out (DP-43, DP-45), correctly. The asymmetry is real and one-sided: a planning rate that is too slow
  costs months of waiting that can never be recovered, while one that is too fast is caught by the
  ceiling test. Where the Steward has never counted the table, the counts-only request should run
  **before** the Registrar fixes §5's dates, so the dates are derived from a measured rate in the first
  place. This is the ordering fix for the "blocking for lock" shape already proposed above.
- **"Measured zero" and "not measurable" are different results and a locked file must distinguish
  them.** A sub-cell whose defining input was unavailable for 100% of rows is reported as *not
  measurable in this window, with the reason and the dates*, never as "no difference between the arms"
  and never silently dropped. Q019's arm decomposition is the first case; any two-arm signal the desk
  tests will have it again.
- **A question about a composite product signal states the arm composition of its population at lock.**
  "The Conviction Monitor's EXIT tier" turned out to mean "the technical arm alone, on days 1–2"; that
  is knowable from counts before any outcome is seen, and it belongs beside the verdict rather than in a
  threat list. Generalises to any tier, score or flag that rolls up more than one input.
- **A feature's meaning changes when a dead input comes back, not only when code ships.** DP-06 and
  DP-50(a) are written in terms of repairs and ships; the mirror case — an input that has been
  structurally unavailable since before the window and is restored inside it — has the identical effect
  on what the column means and should be named in the entry, with the same rule that only a **dated**
  change splits a window (an undated recovery is printed, never retro-fitted).
- **A population restriction created by a matching caliper travels with the verdict wherever it is
  restated.** Q019 drops 68.7% of flagged picks for want of a control and the dropped tail is the more
  damaged one, so the answer is about ordinary-damage flags. DP-12 already says the cost is paid and
  printed; it does not yet say the restriction is carried into the LEDGER line, the guide line and the
  brief, which is where it actually matters.
