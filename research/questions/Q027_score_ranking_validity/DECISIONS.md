# Q027 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 6 items (+ 7 items decided or routed here: the two routed requests named in §5.3, and five the draft settles silently or leaves to `record`)
**`record` pass: 2026-09-14 by decision-maker (autonomous)**, on `research/reports/STEWARD_Q027_exposure.md` (R1, counts only). Every ROUTED item that R1 settles is settled below; nothing in this file is `_pending_`.

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

## The `record` headline (2026-09-14, after R1)

**Q027 LOCKS.** The measured contributing-night rate under §2.5's complete definition is
**48 / 71 elapsed sessions = 0.6761/session**, against the lock-or-DEFER inequality of **≥ 0.36**
(Correction 5, re-solved at the actual lock date 2026-09-14 and unchanged) — clear by 88%. The
eligible-night proxy is 0.9577/session with **100% (48/48) of matured nights converting**, but the
schedule is built on the **directly measured 0.6761**, never the extrapolation: dates move **out
only** (DP-43, DP-45). Floor A (80 contributing nights per primary endpoint) binds at session **119**;
Floor B (DP-24's 30 post-lock nights) at session 45 and is non-binding, satisfied by construction.
**Window 2026-09-15..2027-03-05 · decision Monday 2027-04-12 · single DP-13 extension to window end
2027-04-19, decided Monday 2027-05-24 · then DEFERRED.** 6.9 and 8.3 months from lock, both inside
DP-43's 12-month ceiling (2027-09-14) — **no DEFERRED**. Item 8 is settled and joins the DEFAULTED
list (the date moved out, as DP-43 requires it to when the measured rate is slower than the borrowed
one). Item 9's dates are fixed. Item 10's suppression list is fixed **from measurement and now
closed**: five `tape_t` cells and the three absent `market_regime` labels are suppressed; the **≥ 90
band and bear-only are NOT suppressed** — they clear, contrary to the draft's expectation, and §4.3's
registered rule is a **measured count**, not an expectation. Item 11 gains a **fourth exclusion
criterion** (the 2026-06-02 `analysis_status="disabled"` signature). Corrections 7–9 added.
**No primary is demoted; nothing that carries a verdict was weakened.**

## The headline (at `decide`, 2026-09-14 — kept as written, superseded above where R1 answers it)

**Q027 does not lock at `decide`. R1 is blocking and R1 has never been measured on this funnel.**
Every prior Steward exposure report counts *published* picks; Q027's population is **every scored
candidate row**, and its contributing-night rule (§2.5: ≥ 30 eligible rows **and** a defined `d*_t`
**and** matured to t+20) has no measurement anywhere on the desk. §5.1 says so plainly and borrows
Q023's **0.9538**/elapsed-session published-pick rate as a planning proxy. A borrowed rate cannot
decide a lock: the **inequality** decides it — **≥ 0.36 contributing nights per elapsed session**,
DP-43's 12-month ceiling solved at this lock date and rounded up — and R1 measures which side of it
the funnel sits on. Above the line Q027 locks and §5.2's dates are **recomputed on the measured rate,
moving out only** (DP-43, DP-45); below it Q027 goes to `research/questions/DEFERRED.md` with the
measured rate and the implied date, unregistered.

**One item is DEFAULTED** (#7, the prospective-only window start — where this question spends Haci's
waiting, the Q018 / Q023 shape). **Ten are DECIDED** on existing entries and locked precedent,
including all six of the draft's own §11 items, every one of which goes the Registrar's way. **Two
remain ROUTED** to the Data Steward: R1 (counts only, **blocking for lock**) and R2 (successor
freezes, due at the decision date, blocking nothing — DP-23). **Six corrections** are listed for
`apply`; five of them tighten a clause and none weakens one.

**Rule 14: no exception is requested and none is needed** — the entry is the t+1 open used only as a
price, every eligibility, ranking, tercile, band, episode and stratum field is frozen before any
post-pick-night bar is loaded, and §6's table declares each input. DP-05 is untouched and **DP-41 is
not engaged.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | The target distance for the IC and the tercile contrast | DECIDED | **Option A — one common ATR distance per night `d*_t`**, the median of that night's screened published `d_L3`, applied to every candidate in its own ATR and its own direction. B is refused for a reason stronger than the draft's: under B the distance is itself an engine output correlated with the score, so a rank correlation between score and touch would be part ranking information and part "how far the engine aimed", **in an unknown direction and with no way to separate them after the fact**. A is also the only construction under which rule 5's distance-matched control exists at all (§2.2 = Q006 §3 taken to its limit, the match exact on distance and direction by construction). | rule 5 (a hit rate without a distance-matched control is descriptive); **DP-42** (the level the hypothesis names — L3 — on the DP-09 20-session clock); **DP-26** (a Registrar convention fixed at lock, not derived from a sealed outcome); **DP-45** — of the two, A is the one that cannot borrow strength from an uncontrolled covariate |
| 2 | The outcome variable the IC is computed against | DECIDED | **Option A — the path rank `u_i`** (sessions to first touch, every non-toucher tied below every toucher), with the **binary-touch IC as a blocking companion** (§8 clause 6). Speed is half the objective and dropping it would test a different hypothesis than the one rule 5 defines. A is not the looser option *because* of the companion: a positive `u_i` IC whose binary version runs beyond MPE the other way cannot reach CONFIRMED. | rule 5 ("whether and when"), **DP-08** (the desk measures when a target is first touched, not only whether), **DP-01**; **DP-45** for keeping B's strictness as clause 6 rather than choosing between the two |
| 3 | The IC MPE, and the standing rule behind it | DECIDED | **`\|ρ̄\| ≥ 0.05` applied here as registered, from Haci's own H3 PASS line** (`research/reports/INBOX_2026-09-14_master_hypothesis_program.md` §1, H3: *"Mean daily Spearman IC ≥0.05"*), stated in §4.2 and §8 with that source and **not lowered at the decision pass in any branch**, including one where the CI excludes zero at 0.04. **No DP entry is written by this run** — an autonomous run adds no standing rule (DP-40) — so the *general* form ("the MPE for any per-night rank-correlation endpoint is 0.05 in Spearman-ρ units") is filed below under **Standing rules proposed**, for Haci to confirm before H-075's per-layer ICs and H-082's decay series need it. | **DP-25** (units and cuts come from the hypothesis as written; the Registrar does not re-unit it, and this number is the hypothesis's own); **DP-44** — it carries no rank-correlation unit, and the rule against *inventing* a number is satisfied precisely by taking his; **DP-40** (no DP entry from an autonomous run) |
| 4 | The band-inversion clause | DECIDED | **Option A — blocking on the question-level verdict**: no adjacent-band contrast at −5.0 pp or worse with its own 95% night-clustered CI excluding 0 may coexist with a question-level CONFIRMED. *"Materially non-monotonic → FAIL"* is half of H-073's own decision rule, so a purely descriptive band panel would delete half the hypothesis and let a confirmed IC be reported as a smooth ranking while an adjacent pair runs backwards. **Tightened, see Correction 2:** the blocker is computed on **measured** counts for every adjacent pair with ≥ 20 contributing nights, whether or not that band is on the lock-fixed affirmative-suppression list. | **DP-25** (the hypothesis's own FAIL condition is not demoted to a secondary); **DP-45** (of two readings that differ only in strictness, the stricter; the blocker reduces no floor and can only ever prevent a CONFIRMED); Q023 DECISIONS #9's "suppression never removes a blocker" |
| 5 | The contributing-night row floor | DECIDED | **Option A — ≥ 30 eligible rows per night** (terciles ≥ 10 wide), with a night that survives the night-level filters but carries fewer being **non-contributing and counted, not an exclusion**. Below 30 a per-night Spearman ρ is mostly tie structure and a tercile contrast is a contrast of singletons. The measured pool (min 56 / median 63 / max 68 rows with ≥ 60 prior bars, `STEWARD_Q024_…` (b)) makes the stricter floor free in expectation — and R1(a) measures it rather than assuming it. | **DP-21** (the stricter reading of a floor, never the weaker); **DP-26** (an inference convention fixed at lock before any outcome is seen); **DP-45** |
| 6 | Unresolved-direction (`mixed`) rows | DECIDED | **Option A — excluded and counted**, with the per-decile mixed share printed and the **"mixed graded long" version of both primaries as a blocking companion** (§8 clause 7), plus the whole-night exclusion above 25% mixed. A synthetic target needs a direction; B invents one for exactly the rows where the scorer said it could not resolve one (`super_agent_select_scoring.py:1180`), and an invented direction on the bottom of the distribution would feed the IC a fabricated outcome. The blocking companion is what stops A quietly deleting the tail the IC is about (§10 threat 3). | ground 3 — one defensible answer: the outcome variable is undefined without a direction; **DP-26**; **DP-45** for keeping B as a binding sensitivity rather than choosing between them |
| 7 | The window start (prospective-only) | **DEFAULTED** | **Pick nights ≥ 2026-09-15 only** — the first session after the lock commit. The sealed stretch (2026-06-01..2026-08-12) is printed **once** as an explicitly labelled post-hoc panel, split at 2026-07-06 (`_enforce_ladder_monotonic`, the ship that changed the ladders `d*_t` is computed from), entering **no** verdict, no CI comparison, no half, no stratum test, no q and no §9 rule. The cost is that Q027 decides on **2027-04-12 instead of now** (written as 2027-03-08 at `decide`; item 8's measured rate moved it out). **Confirmed at `record`:** the 2026-07-06 split stands and now brackets both the ladder ship and the `publication_floor` ship (2026-07-08), with R1(c)'s measured `d*_t` level shift — median 1.06 → 2.10 ATR — printed inside the panel; it remains a description and enters no verdict. | **DP-43**; not taken: read the sealed nights, decides now, but not blind |
| 8 | Window end, decision date, extension date, **lock-or-DEFER** | **DEFAULTED (R-3)** — settled at `record`, R1 received | **LOCK, not DEFERRED.** Measured contributing-night rate **0.6761/elapsed session** (48/71) ≥ the 0.36 gate. **Window: pick nights 2026-09-15..2027-03-05 = 119 elapsed sessions** (Floor A binds: ceil(80/0.6761) = 119; Floor B, DP-24's 30 post-lock nights, lands at session 45 = 2026-11-16 and is non-binding). **Decision date: Monday 2027-04-12** — window end + 20 sessions maturity (2027-04-05) + one calendar week, first Monday on or after, moved out for holidays. **Single DP-13 extension:** window end session 149 = **2027-04-19**, decided **Monday 2027-05-24**; still short there → `research/questions/DEFERRED.md`, no second pass. Every date moved **out** from the provisional schedule (2027-03-08 → 2027-04-12; 2027-04-19 → 2027-05-24), because the measured 0.6761 is **slower** than the borrowed 0.9538. The 0.9577 eligible-night proxy and the 100% maturity conversion are **not** used for any date: the schedule takes the stricter directly-measured number, and a faster rate could never have moved a date in. 6.9 / 8.3 months from lock, inside DP-43's 12-month ceiling (2027-09-14). | **DP-43** (the window that reaches every floor, computed at `record` from the Steward's numbers; +30-session extension; > 12 months → DEFERRED, not engaged here), **DP-45** (out only, never the shorter window, never the extrapolated rate), **DP-13**, **DP-21**, **DP-24**; Correction 5's inequality re-solved at the actual lock date; `STEWARD_Q027_exposure.md` Headline + "Projected schedule". Not taken: the 0.9577 eligible-night proxy — decides ~2027-02-22 |
| 8a | *(superseded at `record`)* the routed form of item 8 | ROUTED → data-steward — **CLOSED, R1 delivered 2026-09-14** | waits on **R1**. Settled at `record` on the measured contributing-night rate: **≥ 0.36/elapsed session → Q027 locks** and §5.2's dates are recomputed, **out only**; **< 0.36 → DEFERRED**, unregistered, with the measured rate and the implied date named (the H-062 form). Three things are fixed now so none is argued with counts in view: the **threshold is the inequality**, DP-43's 12-month ceiling solved at the actual lock date and rounded up, re-solved at `record` if the lock date moves (Correction 5); the window end is the **later** of the two floor projections (80 contributing nights, 30 post-lock nights) at the **measured** rate, so that every floor is projected met **inside the primary window** — DP-13 is the fallback for a measured shortfall, never the plan, and a rate faster than the borrowed 0.9538 changes nothing; and a decision date landing on a market holiday moves **out** to the next Monday, never in. | — |
| 9 | Successor freezes | ROUTED → data-steward | waits on **R2** — `manifest_v00N` (selections: same SQL, same exclusion criteria, **every candidate row published and unpublished**) and `manifest_prices_v00N` (daily bars for **every candidate symbol on every in-window night**, 20 forward sessions beyond the last pick night, ≥ 60 prior sessions before the first), plus the **add-only successor exclusions file**. Due before the decision date; **not a blocker for lock** (DP-23). **Dates fixed at `record` from item 8, and they moved out:** pick nights **2026-09-15..2027-03-05**, daily bars through **2027-04-05** (t+20 of the last pick night) and ≥ 60 prior sessions before 2026-09-15, delivered before **Monday 2027-04-12**; the extension pair only if DP-13 fires — pick nights through **2027-04-19**, bars through **2027-05-17**, due before **Monday 2027-05-24**. The add-only successor exclusions file now carries **four** criteria (item 11, amended at `record`). Re-issued in full under "Routed requests". | — |
| 10 | Demotion, and the sub-cell suppression list at lock | DECIDED | **Neither primary is demotable.** E1 and E2 share the same contributing nights and each *is* a primary, so a night shortfall leaves no endpoint: it is a floor failure — the single DP-13 extension, then DEFERRED — never a demotion to descriptive and never an INCONCLUSIVE verdict. **Sub-cells: the list is FIXED at lock**, revised **once** at `record` from R1(d)'s measured candidate-level band composition and R1(e)'s episode structure, and then **closed** — a cell suppressed at lock stays suppressed even if it clears 20 measured nights at the decision pass (Correction 3). **The revision ran at `record` on 2026-09-14 and the list is now closed. SUPPRESSED (8 cells):** `tape_t` `up_low` (projects 16.8 at session 119), `down_high` (13.4), `up_high` (8.4), `down_mid` (6.7), `down_low` (5.0) — five of the six `tape_t` cells — and the three `market_regime` labels **absent from the measurement**, `bearish` / `neutral` / `risk_off` (0 of 48 nights, structurally absent rather than thin). **NOT suppressed (on the affirmative-reporting list): `tape_t` `up_mid`** (30.2), **all five score bands including `≥ 90`** (28.5; also `85–90` at 55.3), `market_regime` `strongly_bullish` (48.6) and `bullish` (23.5), all three `best_timeframe` cells, **bull-only and bear-only** (80.4 each), published / unpublished, penalized / unpenalized. **The `≥ 90` band and bear-only stay on the list although §4.3's own text expected both to be suppressed: the registered rule is a measured count, not an expectation** — R1(d) measures the candidate-level band composition Q027 actually uses (elite candidates present on 17 of 48 nights, 35%) and R1(e)/(a) measures candidate-level bearish rows on every one of the 48 nights; the published-elite monthly counts (PI-010) and the 0.157/session bear rate (H-062/Q023) the draft cited are rates on a **narrower published population** and do not transfer. Clearing the projection is **permission to print, not a guarantee**: every listed cell still needs ≥ 20 **measured** contributing nights at the decision pass (Correction 3), and Correction 2's inversion blocker runs on measured counts for suppressed and unsuppressed cells alike. `market_regime` `unlabelled` is **not a cell** — the pre-2026-06-09 backfill cannot occur inside a window starting 2026-09-15 (rule 14; `exclusions_v003.regime_label_point_in_time_from`). **Suppression restricts affirmative reporting only**: it never removes clauses 5–10's blockers, never by itself makes an endpoint INCONCLUSIVE, and the halves, the bull-only version, the "mixed graded long" version, the binary-outcome IC, the 5-session companion and the monthly blocks are **not** on the list and block at whatever count they have. | **DP-43** (demotion decided at lock, never afterwards), **DP-21** (20 per cell, no floor moved in either direction); Q023 DECISIONS #9, Q022 #6, Q019 #6/#9 — same construction, same direction of travel |
| 11 | Exclusions inside a window every night of which postdates the freeze | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** (the newest file) with the **add-only successor exclusions file** issued with the successor selection freeze — the identical three lists (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`), built by the identical criteria, covering nights after 2026-09-10, **plus a fourth list added at `record` (see below, and Correction 7)**. The successor file may only **add** nights; no night is ever removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be. DP-04 applies mechanically on top. Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. **Amended at `record` (criteria fixed at lock, and the lock has not happened yet): a FOURTH list, `payload_disabled_runs`** — a night on which **every** published row (DP-28) carries `public_payload_json.analysis_status = "disabled"` or no `lane_plans` object at all, i.e. **zero screened `d_L3` survivors on the night**, is excluded **whole**. R1 found the signature on **2026-06-02** (8/8 published rows, two enrichment enable-flags off in that night's own `sas_runs.config_json`), recurring on 2026-04-01, 2026-05-01 and 2026-07-02 — all four the first published night of a calendar month, and the last already excluded via `manual_runs`. The criterion is a **payload signature, outcome-blind, measurable at freeze time**, and it is what §2.5's `d*_t` construction requires: on such a night the *source cohort for the night's common distance does not exist*, so the trailing-20-night median would import a distance from a different cohort — and R1(c) measures that distance moving by **~2x** across one config ship, so an imported `d*_t` is not a small error. The trailing-median fallback therefore fires **only** on nights with 1–2 screened survivors, **never** on a zero-survivor night. **Add-only and dateless:** the criterion is fixed here, the nights are whatever the Steward's scan finds after 2026-09-10; **no night is removed from any v003 list**, and `exclusions_v003.json` itself is **not edited** (research/data/ is not writable from here — the fourth list lives in the successor file). | **DP-22** read as "one list, one set of criteria" — its "cite the newest file" clause presumes a sealed window and Q027's is entirely post-freeze; **Q023 DECISIONS #8**, **Q018 #4**, **Q022 #7**, same construction |
| 12 | A mid-window change to what `overall_score` *is* | DECIDED | A change to the weights, the timeframe multipliers, `qualification_threshold`, the ATR-elite caps, the GEX-missingness offset or a scoring enable-flag makes `overall_score` **two different features**: the window is **cut at the ship date**, the **post-ship** segment becomes the question's window with the whole §5 schedule recomputed from it — **out, never in**, subject to the same single extension and the same 12-month ceiling measured from the original lock — the pre-ship segment becomes a labelled descriptive panel entering no verdict, and if neither segment reaches the floors inside the ceiling Q027 is **DEFERRED**. `eval.py` **fails loudly** on any cross-freeze disagreement in `overall_score`, `conflict_penalty` or `dominant_direction`, and on any row whose `score_details_json` re-derivation differs from `overall_score` by more than 0.05. **DP-50(b) runs the other way too:** any such platform change is **flag-off until 2027-03-08** (2027-04-19 if the extension fires), checked before any fix brief is written. A `publication_floor` / `bear_publish_threshold` change is **not** a split — it changes which rows are published, not which are scored — but it changes `d*_t`'s source cohort, so it is recorded and the `d*_t` series is printed across the ship date. **Confirmed at `record` on R1(g), and the answer is "no split":** the code sweep since `fa70688` over the three named SAS files returns **NONE** (4 commits, none touching them), and every scoring field — weights, timeframe multipliers, `qualification_threshold`, both ATR-elite caps, the GEX offset, the enable-flags — is **constant across all 71 in-window runs** in `sas_runs.config_json`. The two `config_json` changes R1 found are **publication gates, not scoring**: `bear_publish_threshold` null→80.0 effective 2026-06-29 and `publication_floor` null→80.0 effective 2026-07-08 (ship `1765a6f` 2026-07-07, already dated in `DATA_NOTES.md`). Both were live **more than two months before the window starts**, so neither falls inside the prospective window and neither splits it. The measured **~2x level shift in `d*_t`** across the `publication_floor` ship (median 1.06 → 2.10 ATR, R1(c)) is **context, not a split**: it sits entirely in the sealed stretch, whose post-hoc panel is already split at 2026-07-06 (item 7) — a boundary that now brackets **both** the ladder ship and the publication-floor ship, with only 2026-07-07 between them (2026-07-06 itself is excluded via `manual_runs`), and R1(c)'s three-segment table is reproduced in that panel. Its forward consequence is that item 12's recording clause is **load-bearing, not ceremonial**: if either gate moves inside the prospective window, the per-night gate values are read from `sas_runs.config_json`, the `d*_t` series is printed pre/post, and both primaries are printed split at the ship date as a **labelled descriptive panel** — no verdict split, no new blocker, no reopened list. | **DP-06** / **DP-50(a)** (a repair or a config change splits a column into two features at the ship date), **DP-50(b)** (ship timing checked against in-flight questions, the PI-011 / Q010 pattern), **DP-50(c)** (the sweep runs on the pinned freeze and the read-only repo, never a live query); Q023 DECISIONS #12, Q018 #9, Q022 #3 |
| 13 | The F2 correction set, and `m = 2` | DECIDED | BH within the question runs over **E1 and E2, m = 2, fixed in every branch** — both endpoints carry a verdict, an endpoint short of floor still has its p computed, and no primary is dropped afterwards (dropping one would lower the bar for the survivor). Across the family, BH runs over the primaries of the **F2 questions locked by the decision pass** and the set **never shrinks below the 4 registered at this lock and Q023's** — Q023 (2) + Q027 (2). **H-010 and H-012 are counted once, here** (merged into Q027, marked as such in the BACKLOG). **Q005 stays excluded**, for the stated reason and not by assumption: a diagnostic decomposition with no MPE, no directional primary and no outcome column read at all contributes no testable primary. If H-011, H-014, H-079, H-080 or H-082 lock before the decision date their primaries join the set and the q's are recomputed on the larger m. | rule 8; **DP-29** (family by the primary endpoint's subject — calibration → F2 — with an overlapping hypothesis merged, not double-counted); **Q023 DECISIONS #10**, **Q018 #11**, **Q022 #8** — a family correction set is stated symmetrically and never shrinks |

## Corrections to silent choices

**Nine** — six at `decide`, **three added at `record`** (7–9, from R1). The Registrar applies them all
at `apply` with the rest of this file. Everything else was checked against the policy and already
matches (list at the end of this section).

1. **§8 clause 6 — E2's blocking companion is stated in a unit that has no MPE.** The draft requires
   "the **sessions-to-touch** version, which must likewise not run beyond MPE the other way", but
   **DP-44 gives sessions-to-touch differences no MPE** — they are descriptive, and the
   touch-within-k form is what decides. As drafted the clause either invents a session-unit MPE or is
   unenforceable. **Must read:** E2's clause-6 blocker is the **touch-within-5-sessions** tercile
   contrast (§4.3's 5-session companion, DP-20 units), which must not run **beyond 5.0 pp in the
   opposite sign**; the sessions-to-first-touch distributions by tercile and band stay descriptive,
   with **no MPE anywhere in session units** (DP-44). E1's clause-6 blocker (the binary-outcome IC) is
   unchanged.
2. **§4.3 and §8 clause 9 — strike "a suppressed band cannot block (it has no estimate)".** A cell
   that is off the affirmative-reporting list still has measured nights and a computable contrast, and
   letting suppression delete the inversion blocker would mean the one boundary most likely to be
   suppressed — the 90 line, which is where H-010's whole claim lives — could run backwards with no
   consequence. **Must read:** suppression restricts **affirmative reporting only**; the clause-9
   inversion test is computed for **every** adjacent-band pair with ≥ 20 **measured** contributing
   nights, whether or not that band is on the lock-fixed suppression list, and a qualifying inversion
   blocks a question-level CONFIRMED (DP-45; Q023 DECISIONS #9's "suppression never removes a
   blocker", stated there in the same words).
3. **§4.3 — the `≥ 90` band's print-or-suppress status is fixed at lock, not "decided at the decision
   pass on `eval.py`'s own count".** That sentence contradicts §4.3's own "the list is FIXED at lock"
   and §5.2's list of what does not reopen. **Must read:** every sub-cell's status is fixed at lock,
   revised **once** at `record` from R1(d)'s measured candidate-level band composition and then
   closed; a cell suppressed at lock **stays suppressed even if it clears 20 measured nights** at the
   decision pass, and a cell cleared at lock still needs ≥ 20 measured contributing nights to print.
   Only Correction 2's blocker runs on measured counts (DP-43, DP-21, Q023 #9).
4. **§2.2, §2.4 and §4.3 — "published" must be named as DP-28's predicate.** The draft says "that
   night's **published** picks" for the `d*_t` median and "published versus unpublished rows" as a
   sub-cell without defining the term, and Q027's whole point is that publication is not an arm.
   **Must read:** published = **`qualified IS TRUE AND selected_rank IS NOT NULL`** (DP-28); dark-lane
   rows (`qualified` true, `selected_rank` null) are excluded from the `d*_t` median and from the
   published sub-cell, and — because this population is every scored row — they **remain in the
   population** carrying a score and a synthetic target like any other candidate. The `< 3 screened
   published picks` fallback is evaluated on that predicate.
5. **§5.3 R1 — the 0.36 is the ceiling's solution, not a constant, and the rate must be measured under
   §2.5's complete definition.** **Must read (a):** the lock-or-DEFER test is the **inequality** —
   80 contributing nights divided by the admissible elapsed sessions left under DP-43's 12-month
   ceiling, solved at the **actual** lock date and rounded **up**; at a 2026-09-14 lock that is
   ≈ 225 sessions and **≥ 0.36**, and it is **re-solved at `record`** if the lock date moves.
   **Must read (b):** the rate R1 returns is the **contributing-night** rate under §2.5 in full —
   ≥ 30 eligible rows **and** a defined `d*_t` (or its trailing-median fallback) **and** maturity —
   not an eligible-night rate and not Q023's published-pick rate. A gate that exists in §8 is measured
   in the exposure request under the same definition, or the question locks on an arithmetic that
   cannot reach its own verdict.
6. **§5.1 and §5.2 — the borrowed rate and the 8-session cushion are replaced at `record`, not
   defended.** **Must read:** §5.1's planning row is superseded by R1's measured rate and §5.2's
   session-by-session arithmetic is recomputed from it, **moving out only** (DP-43, DP-45); the
   8-session cushion is a drafting margin on a borrowed number and is **not evidence** — if the
   measured rate puts floor A below 80 inside the primary window, the **window end moves out before
   lock**, because DP-13's single extension is the fallback for a measured shortfall and never the
   plan.

**Added at `record` (2026-09-14), from R1:**

7. **§2.5 / §4.1 and the exclusions clause — a night whose published slate has no lane plans must be
   excluded, not fallback-filled.** The draft's only escape from a missing `d*_t` is the
   "< 3 screened published picks → trailing-20-night median" fallback, which was written for a *thin*
   slate. R1(c) found a different failure: **2026-06-02, where all 8 published rows carry
   `analysis_status = "disabled"` and no `lane_plans` at all** — zero screened survivors, the same
   signature as 2026-04-01, 2026-05-01 and 2026-07-02. **Must read:** a night with **zero** screened
   `d_L3` survivors is **excluded whole** under the successor exclusions file's new fourth list,
   `payload_disabled_runs` (item 11, criterion stated there); the trailing-median fallback applies
   **only** to nights with 1 or 2 screened survivors. Reason it is not left to the fallback: on a
   zero-survivor night the common distance would be imported wholesale from a different cohort, and
   R1(c) measures that cohort's median moving from ≈ 1.06 to ≈ 2.10 ATR across a single config ship —
   an imported `d*_t` is not a rounding error, it is a different experiment on that night.
8. **§4.3 — the two "expected to be SUPPRESSED" sentences are wrong on the measurement and must be
   struck.** The draft states "**`≥ 90` is expected to be suppressed**" (on published-elite monthly
   counts) and "**Bear-only is expected to be SUPPRESSED**" (on H-062's 0.157/session *published*-bear
   rate). R1(d)/(a) measure the population Q027 actually uses: elite **candidates** present on 17 of 48
   nights (projecting 28.5 at session 119) and candidate-level bearish rows on **48 of 48** nights
   (projecting 80.4). **Must read:** both cells are **on the affirmative-reporting list**; the
   suppression rule is and always was a **measured count**, and the expectations are replaced by
   item 10's closed list — five `tape_t` cells and the three absent `market_regime` labels suppressed,
   everything else printed at ≥ 20 measured nights. Also strike §4.3's "its print-or-suppress status is
   decided at the decision pass on `eval.py`'s own count" for the `≥ 90` band (Correction 3 already
   requires this; R1 has now supplied the number that closes it).
9. **§5.1 / §5.2 and the R1 request text — the borrowed 0.9538 and the provisional dates are
   replaced, and the *measured* rate is the maturity-truncated one.** **Must read:** §5.1's planning
   row becomes "measured 0.6761 contributing nights per elapsed session (48/71),
   `STEWARD_Q027_exposure.md`", §5.2's arithmetic is the item-8 schedule, and the file states in one
   line **why 0.6761 and not 0.9577**: the 0.6761 is bound by the price freeze's own forward-bar
   horizon (only 48 of 68 non-excluded nights could mature to t+20 by 2026-09-10), the 0.9577
   eligible-night figure is an upper bound, and DP-45 takes the directly measured number because the
   extrapolation is the one that would pull the decision date **in**.

Also for the **Red Team**, not a correction to this file and changing no locked document: the
`analysis_status = "disabled"` / no-`lane_plans` signature on **2026-06-02** (and 2026-04-01,
2026-05-01) is **not** in `exclusions_v003.json`, and those nights fall inside the population of
locked and pinned questions that read that night's `lane_plans` for a level, a stop or a distance.
Locked PREREGs are **not** edited (DP-22, rule 3): the flag is recorded here for the Red Team to
carry into each affected question's sign-off, and for whoever issues `exclusions_v004`.

Checked and **not** corrections — each already matches the policy: entry the **session t+1
regular-session open** for every row alike, with **DP-11 correctly not fired** (nothing here is a
position already held) and the `C_t` basis a printed sensitivity that never decides (**DP-03(b)**,
**DP-42**); the **L3 distance on the 20-session clock** with the platform's 40-session swing window
descriptive (**DP-09**, **DP-42**); a target already through the entry scored **not a hit** with the
row kept in the denominator and the count printed (**DP-26**, rule 5); **no stop assumed**, adverse
excursion and counter-direction touches reported and never used as exits, **DP-30** not engaged and
**DP-27** not reachable (no intra-session ordering is needed — no hourly bar is used anywhere)
(**DP-02**); E2's MPE at **±5.0 pp** as a single within-night difference of two touch rates at an
identical ATR distance — the Q006 E1 shape, not a difference of differences, so DP-20's doubling
clause correctly does not apply and no larger number is proposed (**DP-20**, **DP-44**); floors read
as **≥ 80 contributing nights per primary endpoint** and 20 per reported cell, the stricter reading
(**DP-21**); **≥ 30 contributing nights after the lock commit**, satisfied by construction, never
reduced, with **DP-31 correctly not invoked** because PROSPECTIVELY_CONFIRMED is reachable from this
run by design and no successor replication is owed (**DP-24**); one automatic extension then
DEFERRED, fired on `eval.py`'s **measured** counts and never on a projection, with a floor shortfall
never an INCONCLUSIVE verdict (**DP-13**); window entirely after the 2026-06-01 catalyst fix, so no
**DP-06** split falls inside it, and the sealed panel split at 2026-07-06 for the ladder ship;
successor freezes covering **every candidate symbol, published and unpublished** (**DP-23**); the
**two CIs per primary** with the episode defined as one symbol's run of appearances at gaps ≤ 10
sessions, and the CI-2-includes-zero case INCONCLUSIVE rather than CONFIRMED (**DP-51**, §8 clause 5);
registrar conventions fixed before any outcome is seen — the band cuts at the platform's own 70 / 80 /
85 / 90 boundaries, the 10-session stationary block length, seed 20260914, the expanding-window tape
terciles, the 25% mixed and 10% ungradeable night thresholds (**DP-26**), none promotable at the
decision pass; the exposure count taken from the **pinned freeze** and never a live query
(**DP-50(c)**); every number **NON_QUOTABLE** (rule 12) and nothing subscriber-facing before
PROSPECTIVELY_CONFIRMED (rule 10); no layer-level IC computed, so H-075's primaries stay its own
(rule 8, forking paths); and **no rule-14 exception requested or needed** (**DP-05** untouched,
**DP-41** respected).

## Defaulted on Haci's behalf

- #7 Window start — chose **prospective-only, pick nights ≥ 2026-09-15**; not taken: read the sealed
  nights, decides now, not blind — DP-43. Overturn = successor question.
- #8 Window end and decision date — chose **window end 2027-03-05, decision Monday 2027-04-12**
  (extension 2027-04-19, decided 2027-05-24, then DEFERRED); not taken: the 0.9577 eligible-night
  proxy — decides ~2027-02-22 — DP-43. Overturn = successor question.

**Two items, and both are the same cost: waiting.** Item 8 was routed at `decide` and came back at
`record` moving the date **out** by five weeks (2027-03-08 → 2027-04-12), which is the only direction
DP-43 and DP-45 permit. The tempting alternative was real and is written down so he can see it: 100%
of the nights old enough to test converted to contributing, so the eligible-night rate of 0.9577 is
not a fantasy and would have decided Q027 around 2027-02-22. It was refused because it is an
**extrapolation past the freeze's own forward-bar horizon**, and the desk does not buy seven weeks
with a number it has not measured.

On item 7, the expensive one: **Q027 asks Haci to wait until 2027-04-12 (2027-03-08 as this was first
written; the measured rate moved it out) for a question whose band-level version the weekly printed
four days ago.** That is the price of the hypothesis
having been read against the sealed period — the 2026-09-10 and 2026-09-12 weeklies published
band-level returns, and CLAUDE.md's standing list already carries "the 88–90 band underperforms 90+",
which is E2's top tercile and the band secondary both. Those nights can produce a description and not
a test. Nothing else was defaulted: items 1–6 and 10–13 each met a DECIDE ground, and none of them is
a question about how Haci trades — the level, the lane, the clock, the entry basis and "elite = 90"
all come from DP-42 and DP-09 as already locked in Q002–Q024, and the one MPE that is not a DP number
is **his own**, from H3. **Item 8 joined this list at `record`**, as foreseen: the measured rate moved
the window end and the decision date out, and a faster rate would have changed nothing (DP-43,
DP-45). No floor, arm, MPE, gate or clause was weakened anywhere in this file, at `decide` or at
`record`; Corrections 1–5 and 7–9 each tighten one, and the one place `record` **loosened** an
expectation — the `≥ 90` band and bear-only coming **off** the suppression list (Correction 8) — is
not a loosening of a gate at all: it adds two cells to the affirmative-reporting list that the
registered rule (a measured count) always required, and every blocker was already running on measured
counts for suppressed and unsuppressed cells alike (Correction 2).

## Routed requests

### data-steward — R1 (counts only) — **DELIVERED 2026-09-14, CLOSED**

Answered in full by `research/reports/STEWARD_Q027_exposure.md`: (a) funnel 4,020 scored → 3,588
directed → 2,459 eligible on 48 matured nights, **contributing-night rate 0.6761/elapsed session**,
eligible-row min/median/max 39/51/64, CTRA reproduced (5 rows, gradeability only); (b) mixed 10.75%
overall, 58.7% in decile 0 and **0.0% from decile 4 up**, **0 of 68** nights over the 25% threshold,
**0 of 48** over the 10% ungradeable threshold; (c) `d*_t` defined on all 68 nights (67 direct, 1
fallback), median 1.849 ATR, **0 nights outside the [0.25, 10] fail-loud bound**, level shift 1.06 →
2.10 across the `publication_floor` ship; (d) score IQR median 25.04 with **no night at IQR 0**, the
ATR-elite caps at **2 of 4,020 rows** and null GEX at **0.99%** — §10 threat 2 measured and not
observed — and the candidate-level band composition item 10 is now fixed from; (e) 400 symbols, 811
episodes, **70% of symbols recurring across more than one episode**, longest episode 44 appearances
over 71 sessions — §10 threat 5 confirmed and DP-51's second CI earning its place; (f) penalized
share 32.3%, B5 matched pool feasible on **48 of 48** nights; (g) code sweep **NONE**, two
publication-gate `config_json` changes both predating the window, `outcome_corrections` **0 of 125**
touching `overall_score` / `conflict_penalty` / `dominant_direction` across the entire frozen history.
Items 8, 9, 10, 11 and 12 are settled above on those numbers; nothing further is asked of R1.

### data-steward — R1 (counts only) — the request as issued at `decide`, for the record

Q027 (does a higher SAS score mean a better price path — PREREG §5.3 request R1) needs a
**counts-only** exposure measurement on the **frozen** data — `research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json` against `research/data/exclusions_v003.json`, plus read-only
`git log` / `git show` in the platform repo — and **never a live query** (DP-50(c)); it is **blocking
for lock**, because no desk exposure report has ever counted an **all-candidates** funnel (every prior
one counts published picks), §5.1 borrows Q023's published-pick rate of 0.9538 as a planning proxy,
and the §5.3 lock-or-DEFER gate turns on the measured number. **No outcome of any kind:** no touch, no
first-touch date, no return, no excursion, no `outcome_*` column, no `sas_selection_excursion`, no
`uoa_symbol_daily.fwd_return_*`, and no score-versus-outcome cross-tab of any shape; forward bars may
be read **only** to establish that a bar exists (gradeability accounting), never for a value.
Population: **every row in `sas_candidates`, published or not, regardless of `qualified` /
`threshold_pass`**, on pick nights **2026-06-01..2026-09-10**, with the nights in `exclusions_v003`
(`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs`) and DP-04 late-`finished_at`
nights removed; **denominator for every rate = elapsed sessions** (calendar sessions minus holidays,
exclusions *not* pre-removed — the Q019 / Q022 / Q023 convention, so the rates stay comparable across
questions). Please return, by month and for the period as a whole: **(a) the §2.1 / §2.4 funnel
step by step** — scored rows per night, then after the `dominant_direction IN ('bullish','bearish')`
screen, the ≥ 60-prior-split-adjusted-daily-bar screen (which is also the **CTRA truncated-history**
scan: a symbol whose daily bars stop mid-freeze while it keeps appearing as a candidate) and the
gradeability screen (bars covering t+1..t+20 without a gap), with **eligible rows per night (min /
median / max)** and — the number this question lives on — **contributing nights per elapsed session
under §2.5's complete definition**: a matured, non-excluded night carrying **≥ 30 eligible rows
*and* a defined `d*_t`**, which is stricter than any rate the desk has measured and may not be
approximated by an eligible-night rate; **(b) the `mixed` share** of scored rows, overall and **per
score decile**, plus the count of nights above the 25% mixed threshold and the count above the 10%
ungradeable threshold; **(c) the `d*_t` series** — nights with ≥ 3 published picks
(`qualified IS TRUE AND selected_rank IS NOT NULL`, DP-28) surviving the split-scale payload screen
(`lane_plans.day_trading.entry / C_t` outside [0.85, 1.15], or any flattened level implying
> 20 ATR), the median `d_L3 = dir × (L3 − C_t)/ATR` distribution whole and by direction using
desk-computed ATR14 and `C_t` from `prices_daily_split` (never `atr_pct` or `spot_close`, PI-003),
and the count of nights that would fall back to the trailing 20-night median or be excluded
outright; **(d) the score-resolution panel** — per night, score IQR, the share of rows at exactly
84.9 / 79.9 (the ATR-elite cap), the share with a null `gex_alignment_score`, and the **band
composition at candidate level** (`< 70` / `70–80` / `80–85` / `85–90` / `≥ 90`), so §4.3's
suppression list is fixed from measurement rather than from the published-elite trend; **(e) the
episode structure** (DP-51) — distinct symbols per night, symbol-episodes at the ≤ 10-session gap
rule, and the episode-length distribution in both appearances and sessions; **(f) the
`conflict_penalty > 0` share** and the B5 matched-pool feasibility (nights with ≥ 1 penalized row
having ≥ 1 unpenalized row within ±2.0 pre-penalty base-score points); and **(g) the DP-50(a)/(b)
commit sweep** since manifest SHA `fa70688` over `services/super_agent_select_scoring.py`,
`services/super_agent_select_models.py` and `services/sas_conviction_card.py` — the weights, the
timeframe multipliers, `qualification_threshold`, the ATR-elite caps, the GEX-missingness offset, the
scoring enable-flags, `publication_floor` / `bear_publish_threshold` and the lane-plan writer — each
with SHA and date in ET, with an explicit answer **even when it is "none"**, plus a dated
`DATA_NOTES.md` entry for any repair that rewrote historical `sas_candidates` or price rows.
**The call this request decides:** Q027 locks only if the measured contributing-night rate is
**≥ 0.36 per elapsed session** — 80 nights over the ≈ 225 elapsed sessions still admissible under
DP-43's 12-month ceiling at a 2026-09-14 lock, rounded up, and re-solved at `record` if the lock date
moves; below that line the 80-night floor cannot be reached inside the ceiling and **Q027 goes to
`research/questions/DEFERRED.md`** with the measured rate and the projected floor date named (the
H-062 form) instead of being locked. Above the line, please also state **the projected date each
floor is first reached at the measured rate** — 80 contributing nights per primary endpoint (DP-21),
30 contributing nights dated after the lock commit (DP-24, satisfied by construction here), and
20 contributing nights for each reported sub-cell (the §4.3 list: the five score bands, the
`market_regime` labels, the six `tape_t` cells, `best_timeframe`, bull-only and bear-only, published
versus unpublished, penalized versus unpenalized) — with the window end taken as the **later** of the
two primary floor projections and every date **moving out only, never in** (DP-43, DP-45; a rate
faster than the borrowed 0.9538 changes nothing). Please flag every sub-cell projecting below 20
contributing nights at that date, for the DECISIONS item-10 suppression list, which is fixed at
`record` and then closed. Report to `research/reports/STEWARD_Q027_exposure.md`.

### data-steward — R2 (successor freezes) — **RE-ISSUED at `record` with final dates**; due at the decision date, **not** a blocker for lock

Q027 (PREREG §5.3 request R2, DP-23) needs successor freezes before its decision pass. **Dates are now
final, computed from your R1 measured rate of 0.6761 contributing nights per elapsed session; they
moved out from the provisional set and may only ever move out again (DP-43, DP-45).** Please build and
pin `manifest_v00N` (selections: the same SQL and the same exclusion criteria as v001, over
**`sas_candidates` for every candidate row, published and unpublished**, plus `sas_runs` and
`market_regime_daily`) and `manifest_prices_v00N` (the same Alpaca queries over `prices_daily_split`
and `prices_daily_raw`), covering pick nights **2026-09-15 .. 2027-03-05** with daily bars through
**2027-04-05** (session t+20 of the last included pick night) and **≥ 60 prior sessions before
2026-09-15**, delivered before **Monday 2027-04-12** (the decision date). Only if the single DP-13
extension fires: a second pair covering pick nights through **2027-04-19** with daily bars through
**2027-05-17**, due before **Monday 2027-05-24**, built then and not before. The four scope
requirements below are unchanged, **with one addition: the add-only successor exclusions file now
carries a FOURTH list, `payload_disabled_runs`** — every night on which *all* published rows (DP-28:
`qualified IS TRUE AND selected_rank IS NOT NULL`) carry `public_payload_json.analysis_status =
"disabled"` or no `lane_plans` object at all, i.e. **zero rows surviving the split-scale `d_L3`
screen**. This is the 2026-06-02 signature you found (8/8 rows, two enrichment enable-flags off in
that night's own `config_json`), recurring on 2026-04-01, 2026-05-01 and 2026-07-02. It is **add-only
like the other three**: it may add post-2026-09-10 nights and may never remove a night from any v003
list, and `exclusions_v003.json` is not edited. Please also state, in the successor file's header
note, whether the signature is still present after 2026-09-10 and whether it is still a
first-published-night-of-the-month pattern — if it has stopped, say so explicitly rather than
silently returning an empty list. *(The request as issued at `decide` follows, unchanged except for
those dates and that fourth list.)*

Please build and pin `manifest_v00N` (selections: the
same SQL and the same exclusion criteria as v001, over **`sas_candidates` for every candidate row,
published and unpublished**, plus `sas_runs` and `market_regime_daily`) and `manifest_prices_v00N`
(the same Alpaca queries over `prices_daily_split` and `prices_daily_raw`), covering pick nights
~~**2026-09-15 .. 2027-01-26** with **20 forward sessions beyond the last included pick night** (daily
bars through **2027-02-24**) and **≥ 60 prior sessions before 2026-09-15**, delivered before
**Monday 2027-03-08**; and — only if the single DP-13 extension fires — a second pair covering
**.. 2027-03-10** with forward bars through **2027-04-08**, due before **Monday 2027-04-19**, built
then and not before.~~ **[SUPERSEDED at `record` by the dates in the re-issued request above:
2026-09-15..2027-03-05, bars through 2027-04-05, due before 2027-04-12; extension through 2027-04-19,
bars through 2027-05-17, due before 2027-05-24.]** Four scope requirements, none optional: **(i)** the daily symbol list covers
**every candidate symbol on every in-window night, published and unpublished** — this is the whole
population, not a control cohort, and it is never assumed from v001's symbol list; **(ii)** **no
hourly bars are required** (no primary or secondary uses one), so please say so explicitly rather
than building them; **(iii)** an **add-only successor exclusions file** applying the identical three
criteria (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`) to the post-lock
nights — it may add nights and may never remove one from a v003 list; **(iv)** rows whose bars are
missing are **excluded and counted, never back-filled or imputed**. **The DP-50(a) guard is
load-bearing here:** where a successor freeze overlaps an earlier one on `sas_candidates`, the rows
are compared and any disagreement in `overall_score`, `conflict_penalty` or `dominant_direction` is a
**loud failure** — the score is this question's ranking variable, so a repair that rewrote it would
silently re-run the experiment. Please repeat R1(g)'s commit sweep for the period between the
freezes, with a dated `DATA_NOTES.md` entry for any repair that rewrites historical rows, and report
explicitly — **even when the answer is "none"** — whether any weights, timeframe-multiplier,
`qualification_threshold`, ATR-elite-cap, GEX-offset or scoring enable-flag change shipped **inside**
the window (DECISIONS item 12 cuts the window at such a ship date, out and never in). Please
re-confirm every §5.2 date **session by session from the trading calendar** when the freeze is built;
the holiday list used here is 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15,
2027-03-26 **and, for the extension path, 2027-05-31**. A correction to any date may move it **out,
never in**.

## Schedule

**FINAL — filled at `record` 2026-09-14 from `research/reports/STEWARD_Q027_exposure.md` (R1).**
Measured rate **0.6761 contributing nights per elapsed session (48/71)**, not the borrowed 0.9538 and
not the 0.9577 eligible-night proxy. Every date below moved **out** from the provisional schedule and
may only ever move out again (DP-43, DP-45).

decision_date: **2027-04-12** (Monday) · extension_date: **2027-05-24** (Monday — DP-13's single
automatic extension, window end 2027-04-19 = session 149; then DEFERRED, there is no second pass) ·
hard_stop: **2027-05-24** (still short there → `research/questions/DEFERRED.md`) · rule:
**exposure-driven**

- **window:** pick nights **2026-09-15 .. 2027-03-05** = **119 elapsed sessions**; extended window
  .. **2027-04-19** = 149 sessions · **extended: false**
- **binding floor:** A — ≥ 80 contributing nights per primary endpoint (DP-21) at ceil(80/0.6761) =
  **session 119**. Floor B (DP-24, ≥ 30 contributing nights after the lock commit) lands at session 45
  = **2026-11-16** and is **non-binding**, satisfied by construction since every night in the window
  is post-lock. Window end = later of A and B = **A**.
- **decision date arithmetic:** window end 2027-03-05 + **20 sessions maturity** = 2027-04-05, + one
  calendar week freeze margin = 2027-04-12, first Monday on or after = **Monday 2027-04-12**, not a
  market holiday. Extension: session 149 = 2027-04-19, + 20 sessions = 2027-05-17, + one week, first
  Monday on or after = **Monday 2027-05-24** (2027-05-31 Memorial Day is after it, so no further
  move). Holidays used: 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26,
  2027-05-31; the Steward cross-checked the session count against the PREREG's own §5.2 arithmetic
  (session 92 = 2027-01-26, session 84 = 2027-01-13, both matching).
- **maturity:** 20 sessions, uniform across every eligible row.
- **gates, all on `eval.py`'s measured counts and none reduced:** ≥ 80 contributing nights per primary
  endpoint; ≥ 30 contributing nights dated after the lock commit; ≥ 30 eligible rows with both
  terciles non-empty on every contributing night; ≥ 20 measured contributing nights for any sub-cell
  on item 10's closed reporting list.
- **ceiling:** DP-43's 12 months from a 2026-09-14 lock = **2027-09-14**. 2027-04-12 is **6.9 months**,
  2027-05-24 is **8.3 months** — both inside. **Not DEFERRED.**
- **lock-or-DEFER gate: CLEARED.** ≥ 0.36 contributing nights per elapsed session, measured on the
  all-candidates funnel under §2.5's complete definition: **0.6761**, clear by 88%. The inequality was
  re-solved at the actual lock date (2026-09-14) per Correction 5 and is unchanged at 0.36.

## Standing rules added

_none._ Nothing here is Haci's word: items 7 **and 8** were **DEFAULTED** under DP-43, and a DEFAULTED
item adds **no** DP entry (DP-40) — the `record` pass changed nothing about that. Items 1–6 and 10–13 are applications of DP-01, DP-02, DP-06, DP-08, DP-09, DP-13, DP-20,
DP-21, DP-22, DP-23, DP-24, DP-25, DP-26, DP-28, DP-29, DP-42, DP-43, DP-44, DP-45, DP-50, DP-51 and
locked precedent. The generalisable ones are listed below as **proposals**, for him to confirm or drop.

## Standing rules proposed

- **The MPE for any per-night rank-correlation (IC) endpoint is 0.05 in Spearman-ρ units.** It is
  Haci's own number from H3, and **H-075** (per-layer ICs, partial ICs) and **H-082** (edge decay over
  time) both need one within months; deciding it three times invites three different numbers. The
  entry should carry the tie caveat in the same sentence: an IC against a mostly-tied path-outcome
  rank is bounded well below 1, so the per-night touch base rate, the tied-block size and the
  **maximum attainable |ρ|** are printed beside any quoted ρ, and `IC_t` is **never rescaled** by them
  — rescaling would silently move the MPE.
- **A blocking companion must be stated in a unit that has an MPE.** Where the companion is a timing
  statistic (sessions-to-touch, which DP-44 makes descriptive), the blocker is the corresponding
  **touch-within-k** form, not "beyond MPE" in session units. Q027 §8 clause 6 is the first place a
  drafted blocker had no unit to bind in; it will not be the last.
- **A suppression list fixed at lock restricts affirmative reporting only, and blockers run on
  measured counts.** The corollary is the part that keeps being lost: a cell can be off the reporting
  list *and* still block a CONFIRMED. Stating it once, beside DP-43, would stop it being re-derived
  per question (Q023 #9, Q027 Correction 2).
**Added at `record` (2026-09-14) — four more, each one a thing R1 taught that will recur:**

- **A contributing-night rate measured on a freeze is bounded by that freeze's own forward-bar
  horizon, and the schedule is built on the truncated measurement, never on the eligible-night
  extrapolation.** Q027's two numbers were 0.6761 (measured, maturity-truncated) and 0.9577 (eligible,
  with 100% of matured nights converting); they differ by seven weeks of Haci's waiting. Every future
  exposure report on a maturity-gated endpoint will produce the same pair, and the rule should be
  written once: **report both, schedule on the smaller, and say in one line why** (DP-45's direction
  applied to a rate rather than to an option).
- **A sub-cell suppression list is fixed from a measurement on the question's own population, and a
  rate measured on a narrower population never substitutes for it.** Q027's draft expected the `≥ 90`
  band and bear-only to be suppressed on published-elite counts and a published-bear rate; on the
  all-candidates population the same cells project 28.5 and 80.4 nights. The general form: **where a
  PREREG states an expectation about a cell's density, the expectation names the population it was
  measured on, and `record` replaces it with a measurement on the question's own** — in either
  direction, including the direction that adds cells back to the reporting list.
- **A night whose published payload is structurally absent is excluded whole, not fallback-filled.**
  The `analysis_status = "disabled"` / no-`lane_plans` signature (2026-04-01, 2026-05-01, 2026-06-02,
  2026-07-02 — first published night of a month, every time) is a night on which the engine did not
  produce the artefact a payload-dependent construction needs. A thin-slate fallback is for a thin
  slate; importing a level or a distance from a different cohort is a different experiment on that
  night. This belongs in `exclusions_vNNN` as its own criterion, beside `manual_runs` and
  `uncorroborated_publication_runs`, and it affects more than Q027 — locked questions read those
  nights' lane plans today.
- **A publication-gate change (`publication_floor`, `bear_publish_threshold`) is not a scoring split,
  but it is a cohort split for anything derived from the published slate.** R1(c) measured the night's
  common ATR distance **doubling** (1.06 → 2.10) across the `publication_floor` ship with no scoring
  field moving at all. Any question whose construction reads a statistic *of the published cohort*
  records these gates per night from `sas_runs.config_json` and prints that statistic across the ship
  date — the code sweep alone will not see it, because nothing in the code changed.

- **A borrowed planning rate never decides a lock; the inequality does.** Where no exposure report
  exists for a question's own funnel, the PREREG registers the **lock-or-DEFER inequality** solved at
  the ceiling, locks only above it, and recomputes the whole schedule at `record` from the measured
  rate, out only. A cushion added to a borrowed number is not a haircut — the Q023 §5.1 finding, now
  in its second question.
