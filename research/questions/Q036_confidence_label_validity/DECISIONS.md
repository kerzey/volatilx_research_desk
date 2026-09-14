# Q036 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous, DP-40..48) · Source: PREREG.md "Open decisions before
lock", 4 items (+ 15 decided, defaulted or routed here: the three routed requests named in §5.3 and
twelve the draft settles silently, leaves to `record`, or states in a form a DP entry contradicts)

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

> **RECORD PASS, 2026-09-14 — Q036 is DEFERRED and does not lock.** R1 closed on
> `research/reports/STEWARD_Q036_exposure.md`: **E2's `r_join` measures 0.0000 on every form (0/47,
> 0/71), and the zero is structural** — `completeness_score` never falls below **65.3686** in any of
> the 4,195 scored rows in the window, so a `medium`-labelled row with `overall_score ≥ 82` cannot
> exist under `_confidence_label`'s own arithmetic. Both of item 7's independent DEFERRED triggers
> fire. The decide-pass table below stands **as the record of the choices made before the counts were
> seen**; what they settle is read through `## Record — 2026-09-14` and the struck `## Schedule`.

## The headline

**All four of the draft's own items go the Registrar's way and all four are DECIDED**: the published
slate as the primary population (#1), adjacent-score-rank discordant pairs as E2's estimator (#2),
lock-now-behind-the-gate (#3) and the labelled sealed panel (#4). Each meets a DECIDE ground — a DP
entry, a locked-question precedent, or a technical matter with one defensible answer — and none of
them is a question about how Haci trades: the entry, the level, the clock and the lane come from
DP-03(b) / DP-09 / DP-42 exactly as Q027 and Q031 already locked them, and the MPE is DP-20's +5.0 pp
in both primaries, invented nowhere.

**Q036 does not lock at `decide`: R1 is blocking, as §5.1 says, and the gate it feeds is re-derived
here rather than accepted.** The draft's gate is a bet on one unmeasured quantity, `ρ_co` (the share
of nights carrying both a HIGH and a MED published row), against a threshold of 0.44 computed on
~182 non-excluded nights. Two things are wrong with that, and both push the same way — toward more
waiting, never less:

1. **`ρ_co` is not the rate the floor sits on.** A night contributes only if it is non-excluded,
   matured, carries a **defined `d*_t`** under Q027 §2.2 / §2.4's inherited screens **and** carries
   at least one HIGH and one MED row. The contributing series is the **joint** event, which is
   strictly rarer than either marginal: the desk's own measured published contributing-night rate at
   a 20-session maturity is **0.6620 per elapsed session** (`STEWARD_Q031_exposure.md` §(a), 47/71,
   reconfirmed by Q032 and Q034), so even at `ρ_co = 1` the joint rate cannot exceed 0.6620. A floor
   projected on `ρ_co` alone is optimistic by an unmeasured amount — the Q034 Correction 4 pattern,
   recurring in this question's own variable (item #6).
2. **The session count is wrong by three.** 2026-09-15..2027-06-11 is **187** elapsed sessions, not
   190, and the holiday list behind §5.2's maturity arithmetic omits **2027-06-18** (Juneteenth
   observed) — the third time today the same omission has been found on the same freeze
   (Q033 Correction 2, Q034 Correction 1). t+20 of the window end is **2027-07-13**, not 2027-07-12,
   and the decision date is therefore **Monday 2027-07-26**, not 2027-07-19 (item #5, Correction 1).

Re-solved on the corrected calendar the gate reads **≥ 0.43** contributing nights per elapsed session
for the registered window and **≥ 0.37** for the window plus its single DP-13 extension; below 0.37
the 80-night floor is unreachable inside DP-43's ceiling and Q036 goes to DEFERRED at lock rather
than running eleven months toward a predictable shortfall (item #7).

**One correction is a factual error the code settles, and it removes the only argument for the
draft's option B.** §4.3 and §11 item 1 both say the unpublished `threshold_pass` cohort is where
"all three labels have mass". It is not: `threshold_pass` is set at
`services/super_agent_select_scoring.py:1518-1521` as `overall_score ≥ max(lane_threshold,
publication_floor=80)` **and** `completeness_score ≥ min_completeness=35`, so the dark cohort carries
the **identical** floors as the published slate and its LOW arm is confined to the same
`completeness ∈ [35, 45)` sliver. Option B would have bought no label mass at all — only the rows the
8-cap and the bear cap dropped — while duplicating Q027's population exactly (item #1, Correction 5).

**The label citation verifies.** `_confidence_label(overall_score, completeness_score)` reads exactly
as §1.1 prints it at `services/super_agent_select_scoring.py:1166-1171`, is called at `:1425` **after**
the ATR-elite cap block (`:1407-1423`, so the stored `overall_score` is the post-cap value the label
was computed from — the §2.2 integrity screen is therefore well-posed), and is stamped at `:1451`;
`completeness_score = clamp(available_weight / total_weight × 100)` at `:1347` over the
timeframe-adjusted effective weights at `:1316-1322`; the subscriber sentence is at
`services/super_agent_select_public.py:212`; `publication_floor = 80.0` and `min_completeness = 35.0`
at `services/super_agent_select_models.py:91, :98`, and the enrichment flags at `:109-111` with
catalyst `True`, fundamental and smart-money `False`. All read **read-only** in the platform repo,
working tree at HEAD, which `STEWARD_Q034_exposure.md` §(f) reports unchanged from the pinned
`fa70688` across every scoring-config path today (no shell in this session, so `git show fa70688:…`
was not run; R1(f) re-confirms the pin, and the Steward's sweep is the standing evidence).

**Rule 14: no exception is requested and none is needed.** Every input is a 16:05 ET candidate field
(`overall_score`, `completeness_score`, `confidence_level`, direction, lane, the payload's printed
ladder), a split-adjusted bar dated ≤ t, or a point-in-time regime row legal from 2026-06-09; the
session t+1 open is used **only** as an entry price, never as a classifier. **DP-05 is untouched and
DP-41 is not engaged.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Primary population — published slate or every `threshold_pass` row (draft item 1) | DECIDED | **Option A — the published slate, `qualified IS TRUE AND selected_rank IS NOT NULL`, with the unpublished cohort used only for B3 and the §4.3 dark-set panel.** Three independent grounds and no hedging. (i) DP-28 is the desk's publication predicate and dark-lane rows are excluded from every arm; the question is about a word printed on a subscriber card (`super_agent_select_public.py:212`, verified), and B tests a field no subscriber ever sees. (ii) B's stated advantage is **false on the code**: `threshold_pass` already requires `overall_score ≥ 80` **and** `completeness_score ≥ 35` (`super_agent_select_scoring.py:1518-1521`), so the dark cohort carries the same two floors, its LOW arm sits in the same `[35, 45)` completeness sliver, and "all three labels have mass" describes neither population (Correction 5). (iii) B is Q027's population exactly, which is the one thing §1.2 and §8 clause 4 are built to keep this question away from. A is also the smaller population and therefore the lower-powered one, so the choice is not the one that reaches CONFIRMED more easily. | **DP-28**; **DP-29** (F2 bookkeeping: a population identical to Q027's is a second statement of Q027); ground 3 — the code settles the factual claim the options were weighed on; **DP-45**; **Q034 DECISIONS #11** / **Q033 #11** (dark-lane rows only ever in the control pool) |
| 2 | E2's estimator — adjacent-rank discordant pairs or Mantel–Haenszel strata (draft item 2) | DECIDED | **Option A, as drafted in §4.2, with §4.2's `\|Δoverall_score\| ≤ 2.0` recomputation and §8 clause 5's blocker kept exactly as registered.** A needs no caliper chosen by the registrar, contributes on every night where both arms have mass above 82, and matches each HIGH to the closest-scoring MED the night admits; B's `[82,88)` and `[88,100]` strata leave several points of residual score inside every comparison, which is the one confounder E2 exists to remove (§10 threat 1). The pair rule is deterministic (score ascending, ties by symbol ascending) and derived from no outcome, so it is a lock-time convention that stands as drafted. The caliper appears **only** as a blocker that can move the verdict toward INCONCLUSIVE and never toward CONFIRMED. | **DP-26** (registrar-chosen estimator fixed at draft, derived from no sealed outcome); ground 3 — one defensible answer: a score-matched endpoint is matched at the finest grain the night allows; **DP-45** (the variant retained is the one that can only block) |
| 3 | Lock now behind §5.1's gate, or hold the draft until R1 reports (draft item 3) | DECIDED | **Option A — the file is committed and locked once `apply` has run and R1 has closed the gate; R1 is counts-only and blocking for the lock, exactly as Q033 #19 and Q034 #19 are worded.** R1 reads no touch, no first-touch date, no return, no excursion and no `outcome_*` column, so nothing it returns can shape a hypothesis that is already fixed in writing (rule 3); the gate is numeric, pre-committed here, and its branches — lock as written / lock with the extension expected / DEFERRED — are fixed before the counts are seen. Option B (hold the draft uncommitted) buys nothing R1 can supply and costs the desk a queue slot. | ground 2 — **Q034 DECISIONS #19**, **Q033 #19**, the identical construction on the identical freeze today; **DP-46** (the desk locks once DECISIONS.md has no pending item and `apply` has run); rule 3 |
| 4 | The sealed post-hoc panel (draft item 4) | DECIDED | **Option A, strengthened in two parts.** The sealed stretch prints **once**, as a clearly labelled post-hoc panel computed on the registered construction, entering **no verdict, no half, no stratum, no CI comparison, no q and no §9 consequence** — because the weekly of 2026-09-12 already published an uncontrolled version of this exact number ("medium beat high on next-open L1 touch, 78% vs 65%") and replacing a loose line with the same statistic computed properly is better than leaving the loose line as the desk's only record. Added: (i) the panel is computed **by the committed, byte-identical `eval.py` at the decision pass and at no earlier moment**, so no one writes or tunes the script with the sealed answer in view (rule 9); (ii) every restatement of the panel carries the contamination note and the fixed label *"post-hoc, contaminated, carries no verdict"*. Q034 DECISIONS #2 (compute nothing at all on sealed nights) was weighed and does **not** transfer: its ground was that its rows are **other locked questions' primary endpoints**, and Q036's HIGH−MED label contrast is no question's registered endpoint — Q027 owns score ranking, not the label (§7). | ground 2 — **Q027 DECISIONS #7**, **Q031 #6**, **Q033 #17** (print once, labelled, no verdict, same freeze, same population); rule 9 (the timing clause); rule 3; **DP-45** (a panel that can carry no verdict cannot make CONFIRMED easier; the added timing clause removes the one channel by which it could) |
| 5 | The trading calendar the dates are solved on | DECIDED | **The desk's standard holiday list — 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, 2027-06-18, 2027-07-05 and 2027-09-06** (Correction 1). §5.2's arithmetic omits **2027-06-18** (Juneteenth observed; 2027-06-19 is a Saturday), the same omission Q033 Correction 2 and Q034 Correction 1 found on this freeze today. Consequences, every one moving a date **out**: **t+20 of 2027-06-11 = 2027-07-13** (not 07-12); **decision date Monday 2027-07-26** (2027-07-13 + one calendar week = 2027-07-20, a Tuesday; first Monday on or after = 07-26) — not 2027-07-19; the **extension window end = 2027-07-27** (+30 sessions, not 07-26); **extension maturity 2027-08-24** (not 08-23); and the **extension decision date Monday 2027-09-13**, because 2027-08-24 + one week = 2027-08-31 → first Monday 2027-09-06 → **Labor Day** → the next Monday. The successor price freezes' bar horizons move out with them. Every date is re-confirmed session by session from the calendar when the freeze is built; a correction may move a date **out, never in**. | ground 3 — one calendar, and a date arithmetic that omits a session is simply wrong; **Q034 DECISIONS #6 / Correction 1** and **Q033 #7 / Correction 2**, the identical omission at the identical lock date; **DP-45** (the omission shortened a freeze horizon and pulled a decision in; the correction lengthens and pushes out); **DP-23** |
| 6 | Which rate the 80-night floor is projected on — `ρ_co`, or the joint contributing rate | DECIDED | **The scheduling rate is `min(r_join , 0.6620)`, where `r_join` is the measured share of *elapsed sessions* that are non-excluded **and** carry a defined `d*_t` under Q027 §2.2 / §2.4's inherited screens **and** carry ≥ 1 HIGH and ≥ 1 MED eligible published row** — measured directly by R1 as one joint count, never as the product of two marginals and never as `ρ_co` alone (Correction 2). A night with both labels but no `d*_t` survivor (the `payload_disabled` / split-scale / `d_L3 ∈ [0.25,10]` / < 60-prior-bar losses) contributes nothing, so §5.1's `ρ_co ≥ 0.44` projects an 80-night floor on a strictly larger population than the floor is counted on. The 0.6620 cap is the desk's own measured published contributing-night rate at a 20-session maturity (`STEWARD_Q031_exposure.md` §(a), 47/71, reconfirmed by Q032 §(a)(ii) and Q034): **no date on this desk is ever computed from a rate faster than that number**, and a slower measured rate governs. R1 measures `r_join` with numerator and denominator over the **same** sub-period, with every real loss mechanism left in the denominator and **only** freeze-horizon censoring removed — it cannot occur inside the registered window, because R2 delivers bars to t+20 for every in-window night. **E2 carries its own `r_join` on the `overall_score ≥ 82` restriction and both must clear** (item #7). | ground 3 — a floor counted on the joint event cannot be projected from a marginal; **DP-43** (dates projected from the Steward's exposure count at the **measured** run-rate); **DP-21** (the stricter floor reading, never lowered); **DP-45** (never the rate that reaches the floor sooner); **Q034 DECISIONS #7 / #8 / Correction 4** and **Q033 #6**, the identical construction at t+60 and t+40 |
| 7 | The lock-gate thresholds, re-solved on the corrected calendar | DECIDED | **Gate, fixed at this lock and not negotiable afterwards, stated per elapsed session and applied to E1's `r_join` and E2's `r_join` separately** (Correction 3): **both ≥ 0.43** (80 ÷ 187 registered elapsed sessions, rounded up) → **lock as written**, window and dates stand; **either in [0.37, 0.43)** → **lock**, with the single DP-13 extension expected and already registered (80 ÷ 217 sessions on the extended window = 0.3687, rounded up); **either < 0.37** → **the question does not lock; it goes to `research/questions/DEFERRED.md`** with the measured rates named, because 80 contributing nights are then unreachable even with the single extension and the back-solved ceiling (last admissible window end 2027-08-06 = 225 elapsed sessions, 80 ÷ 225 = 0.36) leaves no window inside DP-43's 12 months. **E1's limb clearing while E2's fails is DEFERRED, not "lock E1 alone"** — as the draft says, and for the reason §1.2 gives: E1 without E2 cannot be distinguished from Q027's ranking result and would add a primary to the F2 correction set that can only restate another question. The thresholds are **re-solved from the trading calendar by the Steward** rather than taken from this arithmetic, and a re-solve may move a threshold **up, never down**. | **DP-43** (the 12-month ceiling on the *initial* decision date, the Q034 #4 reading); **DP-13** (one automatic extension, then DEFERRED); **DP-21**; **DP-24**; **DP-45** (the stricter of the extension bound 0.37 and the ceiling bound 0.36 governs; a question predictably short is deferred now, not in eleven months); ground 3 — the draft's 0.44 / 0.36 are computed on 190 elapsed sessions and a non-excluded denominator, and both numbers are arithmetically superseded |
| 8 | Window end, decision date, extension, hard stop | **DEFAULTED (R-3)** — provisional; final at `record` on R1 | **Window: pick nights 2026-09-15 .. 2027-06-11 = 187 elapsed sessions** (unchanged unless R1's measured rates push it **out**). **Decision date: Monday 2027-07-26** — 2027-06-11 + 20 sessions maturity = **2027-07-13** on the corrected calendar (item #5), + one calendar week = 2027-07-20, first Monday on or after. **Single DP-13 extension of +30 sessions** to pick nights .. **2027-07-27**, bars through **2027-08-24**, decided **Monday 2027-09-13** (2027-08-24 + one week = 08-31 → first Monday 09-06 is Labor Day → the next Monday), **which is also the hard stop**: still short there, Q036 goes to DEFERRED. **10.4 months** and **12.0 months** from the 2026-09-14 lock; the **initial** date is inside DP-43's ceiling, which is what the ceiling binds (Q034 #4). The **method** is fixed here and is not re-argued with counts in view: window end = the earliest date at which floor A (80 contributing nights on **each** primary's own `r_join`, item #6), floor B (20 contributing nights in every reported stratum cell) and floor C (30 post-lock nights, satisfied by construction — every night in the window is post-lock) are all projected reached at item #6's rate; then + 20 sessions + one week, first Monday, moved out again for a holiday. Every date moves **out** if R1 measures slower and **never in** if it measures faster. The halves are re-cut on the extended window by the same session-index rule fixed at this lock (H1 = sessions 1..⌈n/2⌉, H2 = the rest, re-derived from the calendar). | **DP-43** (the window that reaches every floor at the measured rate, plus the endpoint's maturity and a one-week margin, first Monday on or after; +30-session extension; the ceiling on the initial date); **DP-13**; **DP-21**; **DP-24**; **DP-09** (the 20-session clock is the maturity, and the 40-session companion is descriptive and never binds a date); **DP-45** (out only; never the shorter window, never the faster rate); not taken: a shorter window decided sooner on `ρ_co` alone |
| 9 | Exclusions | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** — verified the newest file on disk (v001, v002, v003 present) — with the **add-only successor exclusions file** issued with the successor selection freeze, on the identical **four** criteria (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10. The successor file may only **add** nights; no night leaves a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be; `exclusions_v003.json` is not edited (`research/data/` is not writable from here). Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. DP-04 applies mechanically on top. The fourth criterion is load-bearing exactly as §2.4 says: on a `payload_disabled` night no published row carries `lane_plans`, so there is no printed ladder, no `d_L3`, no `d*_t` and no eligible pick — the night is excluded whole rather than entering as a zero. | **DP-22** read as "one list, one set of criteria" (its "cite the newest file" clause presumes a sealed window; Q036's is entirely post-freeze); **DP-04**; **Q034 DECISIONS #11**, **Q033 #11**, **Q031 #12**, **Q027 #11** — same construction |
| 10 | The label-integrity screen, its tolerance, and when it is first measured | DECIDED | **The §2.2 screen stands as drafted — recompute `_confidence_label` from the stored `overall_score` and `completeness_score` using the literal constants at `super_agent_select_scoring.py:1167-1170`, exclude and count mismatches, and make both primaries INCONCLUSIVE above 2% across the window — with two additions.** (i) **A boundary tolerance:** a row whose `overall_score` or `completeness_score` sits within **0.01** of 82.0, 68.0, 65.0 or 45.0 and whose stored and recomputed labels differ is counted and printed **separately** as a rounding boundary case and is **not** charged to the 2% mismatch share; both counts print in the results header. The stored columns are rounded to 4 dp at `:1448`/`:1452`, and a rounding artefact is not evidence that a different writer owns the column, which is the only thing the screen is for. (ii) **The screen is measured before the lock, not only at the decision pass:** R1 gains limb (g), and **a sealed-window mismatch share above 2% (boundary cases excluded) stops the lock** — the question goes to DEFERRED with a `PLATFORM_ISSUES.md` entry filed (DP-07), because the arms would not be what this file registers and no amount of waiting fixes that. The recomputation is well-posed at the pin: the label is computed at `:1425` **after** the ATR-elite cap at `:1407-1423`, so the stored `overall_score` is the post-cap value the label was derived from (verified read-only). | ground 3 — a stored classifier column read as an arm is verified against the code that writes it, and a rounding boundary is not a mismatch; **DP-07** (a defect is filed, not researched); **DP-45** (the pre-lock measurement can only defer the question, never advance it); **Q034 #19** (a gate limb measured before the lock rather than discovered at the decision pass) |
| 11 | A mid-window change to the label's own inputs (§2.6), and the DP-50(b) constraint that follows | DECIDED | **The §2.6 tuple changing in-window **cuts the window at the ship date** — it does not pool on sign agreement (Correction 4).** A change to the scoring weights, the timeframe multipliers, `min_completeness`, `publication_floor`, `bear_publish_threshold`, `max_output_cap`, `qualification_threshold`, the ATR-elite caps, the GEX offset, **any of the three enrichment enable-flags** (`super_agent_select_models.py:109-111`) or the lane-plan writer — **including any promotion of v1.7** — moves the 65 and 45 lines without moving a price, so **the label is a different feature on either side** (DP-06 / DP-50(a)): the post-ship segment becomes the question's window with the whole §5 schedule recomputed from it (**out, never in**, same single extension, same ceiling measured from the original lock), the pre-ship segment becomes a labelled descriptive panel entering no verdict, and if neither segment reaches the floors inside the ceiling Q036 is **DEFERRED**. §8 clause 6's "pooled only when both sides agree in sign" is struck: agreeing signs do not make two features one. `eval.py` prints the per-night `config_json` composition and **fails loudly** rather than silently excluding. Running the other way (DP-50(b)): every listed change is **flag-off until 2027-07-26** (**2027-09-13** if the extension fires), checked before any fix brief is written — and this question's dependence is the strongest on the desk, because the enrichment flags *are* the completeness score. | **DP-06** / **DP-50(a)** (a config change splits a column into two features at the ship date); **DP-50(b)** (ship timing checked against in-flight questions, the PI-011 / Q010 pattern); **DP-50(c)** (the sweep runs on the pinned freeze and the read-only repo); **Q034 DECISIONS #12**, **Q033 #12**, **Q031 #13**; **DP-45** (of the two readings, the one that cannot let a feature change be averaged away) |
| 12 | The LOW arm | DECIDED | **Descriptive in every branch, at the lock and at the decision pass, whatever it measures.** LOW on a published slate means `completeness ∈ [35, 45)` — a sliver between two platform constants verified at `:98` and `:1169` — and registering it as a primary would put an endpoint in the F2 correction set that is expected to sit under the 20-night cell floor. R1(d) measures it before the lock; **if it clears 20 contributing nights per calendar half it is still reported descriptively**, with the reason printed, because an arm promoted after its counts are known is an endpoint chosen with the data in view. The same rule runs the other way: an arm projected below 20 contributing nights at the decision date is demoted to descriptive **at lock** and never dropped afterwards. | **DP-43** (demote-not-drop, settled at lock and never afterwards); **DP-21**; rule 8 (an endpoint is in the correction set from the lock or not at all); **DP-45** |
| 13 | `m`, and the F2 correction set | DECIDED | **`m = 2` within the question — E1 and E2, fixed in every branch.** Neither is dropped if it comes up short (dropping one lowers the bar for the survivor); an endpoint below floor still has its p and q computed and is reported INCONCLUSIVE. Every §4.3 panel, every stratum, the LOW arm and the dark-set panel print **raw p only**, marked *"descriptive, does not decide"*, and enter no correction set. **Across F2 the set never shrinks below the 18 primaries standing at this lock** — Q023 (2) + Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) + Q036 (2) — which is Q031 §7's **16** plus this question's two, verified against `Q031_edge_decay/PREREG.md` §7. Q005 is excluded for the stated reason. If H-013, H-014, H-073, H-079, H-080 lock before 2027-07-26 their primaries join and the q's are recomputed on the larger `m`. | rule 8; **DP-29**; ground 2 — **Q031 §7** verified, **Q033 #13**, **Q034 #15**; **DP-45** (`m` is never reduced to reach a q) |
| 14 | When `eval.py` must be committed | DECIDED | **Written once (rule 9) and committed no later than Monday 2027-04-05, sha256 recorded, not touched afterwards; the extension run uses the byte-identical, unmodified file, and the §6 sealed panel is computed by that same file at the decision pass and not before (item #4).** The draft registers no deadline and this question needs one as much as any on the desk: **Q027 and Q029 decide on Monday 2027-04-12**, on the same freeze, the same published slate, the same `d*_t`, the same t+1-open entry and the same 20-session clock — and Q036's E1 is, by §7's own admission, partly a restatement of Q027's ranking result. A script written after that pass is a script written with part of its own answer in view. 2027-04-05 is the Monday before the earliest sibling pass on this construction. | rule 9 (a deterministic script written once, no tuning while looking); rule 3; ground 2 — **Q033 DECISIONS #14**, **Q034 #16**, **Q032 #11** (same deadline, same reasoning, same window) |
| 15 | Two-sidedness and the MPE | DECIDED | **Both primaries registered two-sided at a symmetric ±5.0 pp, as drafted, and the negative direction carries the larger §9 consequence.** DP-20 sets +5.0 pp for a control-adjusted or within-night touch-rate endpoint and DP-44 routes touch-rate endpoints to it; both E1 and E2 are within-night touch-rate differences at an identical ATR distance, so no new MPE is invented in any unit and R-4 is not engaged. Two-sided is the stricter registration (a two-sided permutation p is never smaller than its one-sided counterpart), and it is also the honest one: the standing suspicion recorded in the 2026-09-12 weekly is that the label is **mis-ordered**, and a design that could only detect the flattering direction would be a design chosen after a read. Sessions-to-touch (`Δs`) carries **no MPE** and is descriptive; the unconditional touch-within-20 form decides. | **DP-20**; **DP-44** (touch-rate → +5.0 pp; sessions-to-touch descriptive; no money-unit MPE invented); **DP-45**; rule 5 / **DP-01** (the fixed-horizon return H-011 names is descriptive and decides nothing) |
| 16 | The dark-set panel's population, and what it may claim | DECIDED | **The panel stays on unpublished rows with `threshold_pass IS TRUE` (the B3 cohort), and the claim that it is a population "where all three labels have mass" is struck** (Correction 5). `threshold_pass` is set at `super_agent_select_scoring.py:1518-1521` to `overall_score ≥ 80 ∧ completeness_score ≥ 35`, so the dark cohort carries the same two floors as the published slate; it differs from it only by the `max_output_cap = 8` / bear-cap cut and the dark-lane flag, and its LOW arm is the same `[35, 45)` sliver. The panel therefore prints **with its own label-composition counts beside it** and is described as *"the same statistic on the rows the cap dropped"*, never as a higher-mass population. A panel on rows failing `threshold_pass` would be a different population and is **not** registered here (DP-25 — that is a new hypothesis, not a re-cut of this one). | ground 3 — the code settles what the cohort is; **DP-25** (no re-unit, no re-population of the registered question); **DP-28**; rule 5 (the B3 control cohort's role is unchanged: distance-matched, descriptive, printed beside every absolute rate) |
| 17 | The exposure counts this question has never had | ROUTED → data-steward | waits on **R1** (counts only) — **BLOCKING FOR LOCK**, as §5.1 and §5.3 say. It settles item #8's dates whole and the lock-or-DEFER call itself: **E1's `r_join` ≥ 0.43 and E2's `r_join` ≥ 0.43** per elapsed session → lock as written; **either in [0.37, 0.43)** → lock with the DP-13 extension expected; **either < 0.37**, or **E1 clearing while E2 fails**, or a **label-integrity mismatch above 2%** (item #10) → **DEFERRED**, with the measured rates and the re-check trigger named. Paste-ready text below. | — |
| 18 | Successor freezes | ROUTED → data-steward | waits on **R2** (DP-23) — the shared successor pair (selection: `sas_candidates` **every row, published and unpublished**, `sas_runs` with `config_json`, `market_regime_daily` with `created_at` and `regime_version` preserved; prices: daily bars for **every candidate symbol on every in-window night**), with Q036's scope requirement: **daily bars through t+20 of the last in-window pick night — 2027-07-13** on the corrected calendar (item #5), plus margin and ≥ 60 prior sessions before 2026-09-15; on the extension path through **2027-08-24**. **No hourly bar is needed and none is requested** — no primary and no blocker in this file reads one. Due before the decision date; **not a blocker for lock**. | — |
| 19 | `eval.py` | ROUTED → researcher | waits on **R3** — the deterministic script, written once against the §2 schema before any successor freeze exists, taking the window start, window end, both manifest paths, both exclusions paths and the output directory as **arguments** (no hard-coded date, manifest name or path), committed by **Monday 2027-04-05** with its sha256 recorded (item #14), byte-identical across the primary and extension runs. | — |

## Corrections to silent choices

**Five.** The Registrar applies them at `apply` with the rest of this file. Every one moves a date
out, strikes a statement the code or the calendar shows to be false, or tightens a clause; none
weakens a floor, a window, a threshold or a gate.

1. **§5.2's maturity arithmetic omits 2027-06-18 (Juneteenth observed), and the header and §5.3 R2
   carry the resulting dates.** **Must read:** the holiday list is 2026-11-26, 2026-12-25,
   2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05 and
   2027-09-06; **t+20 of 2027-06-11 = 2027-07-13** (the draft's 2027-07-12 is one session early);
   **decision date Monday 2027-07-26** (not 2027-07-19), **≈ 10.4 months** after lock (not 10.1);
   the single DP-13 extension runs to pick nights **2027-07-27** (not 07-26) with bars through
   **2027-08-24** (not 08-23) and an extension decision date of **Monday 2027-09-13** (not 08-30 —
   2027-09-06 is Labor Day), which is also the **hard stop**. The successor price freezes carry bars
   through 2027-07-13 plus margin, and 2027-08-24 on the extension path. (DP-43, DP-45, DP-23;
   Q033 Correction 2 and Q034 Correction 1, the same omission on the same day.)
2. **§5.1's session count and the quantity the floor is projected on.** **Must read:**
   2026-09-15..2027-06-11 is **187 elapsed sessions** (not ≈ 190), ≈ **179** non-excluded at the
   measured 4.2% exclusion rate; and the scheduling quantity is **`min(r_join , 0.6620)`** — the
   measured joint rate of item #6 (non-excluded **and** valid `d*_t` **and** both labels present),
   per **elapsed session** — not `ρ_co`, which is one marginal of it and cannot bound the floor.
   `ρ_co` is still reported by R1(b) as a diagnostic and is named as such.
3. **§5.1's gate table is arithmetically superseded.** **Must read (item #7):** both primaries'
   `r_join` **≥ 0.43** → lock as written; either in **[0.37, 0.43)** → lock, extension expected;
   either **< 0.37** → DEFERRED; E1 clearing while E2 fails → DEFERRED, not "lock E1 alone".
   Thresholds re-solved by the Steward from the trading calendar, and a re-solve may move a threshold
   **up, never down**.
4. **§2.6 and §8 clause 6 pool the two sides of a config ship when their signs agree.** **Must read
   (item #11):** a change to the §2.6 tuple **cuts the window at the ship date** — post-ship segment
   becomes the window with the schedule recomputed **out**, pre-ship segment becomes a labelled
   descriptive panel entering no verdict, DEFERRED if neither segment reaches the floors inside the
   ceiling — and the pooled result is **not** reported on sign agreement, because the label is a
   different feature on either side (DP-06 / DP-50(a)). §9 and the desk's fix-brief queue carry the
   matching DP-50(b) clause: every listed change is **flag-off until 2027-07-26** (2027-09-13 if the
   extension fires).
5. **§4.3's dark-set panel and §11 item 1's option B both assert the unpublished `threshold_pass`
   cohort is where "all three labels have mass"; the code says otherwise.** `threshold_pass` is
   `overall_score ≥ max(lane_threshold, publication_floor = 80)` **and** `completeness_score ≥
   min_completeness = 35` (`services/super_agent_select_scoring.py:1518-1521`, verified read-only).
   **Must read:** the dark cohort carries the identical two floors, its LOW arm occupies the same
   `completeness ∈ [35, 45)` sliver, and it differs from the published slate only by the
   `max_output_cap` / bear-cap cut and the dark-lane flag; the panel is described as *"the same
   statistic on the rows the cap dropped"*, prints its own label-composition counts, and claims no
   extra label mass anywhere.

**Checked and not corrections** — each already matches policy: **entry = the session t+1
regular-session open** for every row, with **DP-11 correctly not fired** (nothing here measures a
position already held) and the `C_t` basis a printed sensitivity that never decides (**DP-03(b)**,
**DP-42**); **L3 on the DP-09 20-session clock** with the platform's 40-session swing window printed
descriptively (**DP-09**, **DP-42**); a target at or through `X` at the t+1 open scored **not a hit**
with the row kept in the denominator and the not-takeable count printed per arm (**DP-26**, rule 5);
**no stop assumed anywhere**, MAE and counter-direction touches reported and never used as exits
(**DP-02**); published = **`qualified IS TRUE AND selected_rank IS NOT NULL`**, dark-lane rows only
ever in the control pool (**DP-28**); the distance-matched control printed beside every absolute rate
(rule 5, B3); floors read as **80 contributing nights per primary and 20 per reported cell**, the
stricter reading (**DP-21**); **≥ 30 post-lock contributing nights satisfied by construction**, so
**DP-31 correctly does not apply** and no successor replication question is owed (**DP-24**); the
**episode-clustered CI registered as a blocker** in §2.5 and §8 clause 7 (**DP-51**, in force for
every PREREG drafted from 2026-09-14); family **F2 by the primary endpoint's subject** with H-011 not
merged into Q027, on the verified ground that the label is a joint step function of `overall_score`
**and** `completeness_score` and not a band of either (**DP-29**, `:1166-1171`); the window entirely
after 2026-06-09, so the regime backfill hazard does not apply and **DP-06's catalyst split does not
bite** (the §2.6 split is the live one); `uoa_symbol_daily.fwd_return_*` **never read**
(FREEZE_v001 §5); and **no MPE invented in any unit** (**DP-10 / DP-20 / DP-44**).

## Defaulted on Haci's behalf

- #8 Window end, decision date and hard stop — chose **2026-09-15 .. 2027-06-11, decision Monday
  2027-07-26, single extension to 2027-07-27 decided Monday 2027-09-13**; not taken: a shorter window
  decided sooner on `ρ_co` alone — DP-43. Overturn = successor question.
  **MOOT at `record`, 2026-09-14:** the gate did not clear and the question is DEFERRED, so no window
  and no date was taken. **Nothing was defaulted on Haci's behalf in the end** — the one cost this
  file offered him (ten months of waiting) is not incurred, and the deferral itself is not a default
  but the branch item 7 fixed in writing before any count existed. What reaches the board is the
  subject, not a date: **the platform tells every subscriber a pick has "high conviction"
  (`super_agent_select_public.py:212`), and on the current configuration that word is a re-print of
  "the score is ≥ 82" — 401 high / 141 medium / 0 low on 542 published rows, with `completeness_score`
  never once below 65.37.** Recommended to him as `PI-016`, decision his (DP-48).

**One item, and it is one cost: waiting ten months, twelve if the extension fires.** Everything else
met a DECIDE ground. None of the four items the Registrar raised is a question about how he trades —
the entry, the clock, the level and the lane are DP-03(b) / DP-09 / DP-42 as already locked in
Q027 and Q031, and the MPE is DP-20's, so R-2 and R-4 are not engaged anywhere in this file. What is
worth seeing on the board is not the date but the subject: **the platform tells every subscriber that
a pick has "high conviction" (`super_agent_select_public.py:212`), the desk's own weekly of
2026-09-12 recorded medium beating high on sealed nights (78% vs 65%), and nothing has ever tested
the word.** Both primaries are registered two-sided for that reason, and a confirmed **negative** is
the branch with the larger consequence — it would suspend a subscriber-facing claim rather than add
one.

## Record — 2026-09-14 (record pass, autonomous, DP-40..48)

**Source: `research/reports/STEWARD_Q036_exposure.md`** (R1, counts only, on `manifest_v001` +
`manifest_prices_v001` against `exclusions_v003.json`, plus read-only `git show` / `git log` /
`git merge-base` against the platform repo; no live query, DP-50(c)). **No outcome of any kind was
read** — no touch, no first-touch date, no return, no excursion, no `outcome_*`, no
`sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`, and no label-versus-outcome cross-tab
of any shape. Forward bars were read only to establish that a bar exists (maturity accounting).

### The headline, in one line

**Q036 does not lock. The arm E2 compares against does not exist on this platform configuration:
`completeness_score` never falls below 65.3686 in 4,195 scored rows, so `medium ∧ overall_score ≥ 82`
is an empty cell by arithmetic, E2's `r_join` is exactly 0.0000, and item 7's gate sends the question
to `research/questions/DEFERRED.md`.**

### R1 — CLOSED

| limb (item 7's gate) | threshold | measured | call |
|---|---|---:|---|
| E1 `r_join`, Form (i) (schedule basis, item 6) | ≥ 0.43 | **0.5532** (26/47) | PASS |
| E1 `r_join`, Form (ii) / `ρ_co` (diagnostic) | — | 0.3662 (26/71) / 0.6269 (42/67) | descriptive |
| **E2 `r_join`, the limb that decides** | **≥ 0.43** | **0.0000** (0/47; 0/71; 0/67 — every form) | **SHORT by the whole 0.43** |
| (g) label-integrity mismatch | ≤ 2% | **0.000%** (0/542; 0 boundary cases) | PASS |
| (d) LOW arm | descriptive floor | **0 nights** | structurally absent, item 12 moot |

Population as measured: **71 elapsed sessions**, 68 non-excluded under `exclusions_v003`, **67** after
Q036's own `payload_disabled_runs` criterion (2026-06-02, the one night where every published row
carries `analysis_status = "disabled"` and no `lane_plans`), **47 matured to t+20** (last matured
night 2026-08-12). `d*_t` defined on all 67 nights; 0 zero-survivor nights, 0 fallback nights; `d*_t`
median 1.858 ATR, reproducing `STEWARD_Q027_exposure.md`'s 1.849 on an independently built ATR
series. Published label composition: **401 high / 141 medium / 0 low** on 542 rows; 25 of 67 nights
single-label, every one of them all-HIGH. **All 26 of E1's contributing nights fall out of E2 solely
because every MED row that night sits in `[80.05, 81.99]`** — §2.5's anticipated zero-mass gap,
measured at its maximum possible value.

### What the record settles

1. **The branch is the one fixed at `decide`, before any count existed — DEFERRED.** Both of item 7's
   independent triggers fire: **E2's `r_join` < 0.37** on its own, and **E1 clearing while E2 fails**,
   which item 7 and PREREG §5.1's gate table both answer with *"DEFERRED, not lock E1 alone"*. Neither
   trigger was written with the counts in view and neither is re-argued now (rule 3, DP-45).
2. **E1-alone is not locked, and is not a successor.** §1.2 and §8 clause 4 give the reason and it is
   unchanged by the measurement: the label contains `overall_score ≥ 82`, so an unconditional HIGH−MED
   contrast is partly Q027's ranking result on a coarser variable. Locking E1 alone would add a
   primary to the F2 correction set that can only restate another question (DP-29), and it would do so
   on the one endpoint whose measured `r_join` is comfortable — i.e. it would buy a runnable question
   by dropping the endpoint that made it a different question. **Refused.**
3. **DP-13 cannot cure a structural zero, and no window length can.** DP-13 extends a window **once**
   by +30 sessions when a floor is *marginal* at the decision date, and it fires on `eval.py`'s
   measured counts. It moves a slow rate to a later date; it cannot create a row in a cell whose
   membership condition is arithmetically unsatisfiable under the running configuration. At a rate of
   exactly zero the projected floor date is **undefined**, not merely distant (contrast Q034's finite
   "≈ session 880"). The extension is also registered **at lock**, and Q036 never locks. (The H-062 /
   Q025 reading of DP-13, verbatim: it rescues a floor short by a handful, not by 80 of 80.)
4. **Item 8's schedule, and routed items 18 and 19, fall with the question.** The provisional dates
   (window 2026-09-15..2027-06-11, decision 2027-07-26, extension to 2027-07-27 decided 2027-09-13)
   are **struck** — they were derived from a gate that did not clear, and a successor never inherits
   them (the Q025 precedent). **R2 is withdrawn**: no successor freeze is built for Q036, and the
   shared Q027 / Q029 / Q031 / Q033 / Q034 selection build is **not** extended or re-scoped for it;
   their own pins are untouched. **R3 is not issued**: no `eval.py` is written, and none exists.
5. **No verdict of any kind was produced.** Q036 returns **no NULL, no INCONCLUSIVE, no E1 number and
   no E2 number** — a gate shortfall is not a verdict (the Q025 item 14 precedent). E1's 0.5532 is an
   exposure rate, not a result about the label. **No `results/` directory exists and none may be
   created.** Under `DEFERRED.md`'s preamble nothing here may be reported, briefed or quoted.
6. **Item 10's PI branch does not fire.** (g) measures 0.000% with 0 boundary cases, so
   `sas_candidates.confidence_level` is exactly what `_confidence_label` at the pinned SHA would write
   from the stored columns. **This deferral is not a data-quality defect**; it is a population that
   does not exist on the current scoring configuration. (A *separate* PI is recommended in
   "Corrections and filings added at record" — it is about the field being degenerate, not about the
   column being mis-written.)
7. **Bookkeeping.** **F2's correction set returns to the 16 primaries standing before this draft** —
   Q023 (2) + Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) — which is exactly `Q031 §7`'s
   figure, so **no locked file needs editing and none was edited** (the H-062 / Q025 precedent).
   `research/BACKLOG.md` marks **H-011 — DEFERRED 2026-09-14**, not registered, not merged into Q027
   (DP-29: Q027 tests `overall_score` ranking and cannot return a verdict on the label). **The
   question number Q036 is consumed by this entry and is not reused.** `state.json` goes to `DEFERRED`
   via the controller: **no `PREREG_LOCKED`, no `schedule.json`, no pin** (the Q020 / Q025 / Q030
   precedent).
8. **Both files are preserved exactly as drafted** (the Q030 precedent). `@registrar apply Q036` is
   **not** run now: the five decide-pass corrections and Correction 6 below are recorded here rather
   than folded into a file that will never lock. **Where `PREREG.md` and this file disagree, this file
   governs**, and any re-attempt builds from this record, not from the draft's body. If the trigger
   below is ever met, the question resumes at `@registrar apply Q036`, with every correction folded in
   **then** and the whole §5 schedule recomputed from the new lock date — never carried forward.

### What would move it back into the backlog

**One measured trigger, and it is not a date.** The blocker is a per-row structural property of the
scoring configuration, not an arrival rate, so nights arriving at ~21 a month add contributing nights
at a rate of 0.000 and **no accrual date exists to name**.

- **The trigger, measured by the Steward on a then-current freeze over a trailing quarter, never
  assumed from a projection:** **E2's `r_join` ≥ 0.43 joint contributing nights per elapsed session on
  the `overall_score ≥ 82` series** (the §5.1 / item 7 gate, unchanged), **with E1's `r_join` ≥ 0.43 on
  the unrestricted series at the same time**. (i) is the count that overturns this entry; E1's rate
  alone never does.
- **The necessary precondition, never once observed:** at least one published row per night carrying
  **`completeness_score ∈ [45, 65)` together with `overall_score ≥ 82`**. Today the **minimum
  `completeness_score` anywhere in the window is 65.3686** across all 4,195 scored rows, published and
  unpublished alike, and **every cell of both §(e) grids sits in the `[65,100]` column** — zero rows in
  `[35,45)`, zero in `[45,65)`, on either cohort. Q014 §2 independently records the same floor (65.4)
  on its own control-pool screen.
- **What must become true on the platform for that precondition to hold** — stated as a condition to
  be observed, **not as a request, a recommendation or a brief**: the scoring stack must start leaving
  a *partial* layer gap on a high-scoring name, i.e. the completeness distribution must reach below 65
  on published rows above 82. Configurations under which that could happen: **`enable_fundamental_
  enrichment` (or `enable_catalyst_enrichment`) running False** rather than the True the deployment
  sets on every night measured (see Correction 6) — which would remove one or two layers from
  completeness's numerator on every row; a **weight or timeframe-multiplier change** (v1.6 → v1.7, or
  any edit at `super_agent_select_scoring.py:1316-1322`) that enlarges the effective-weight
  denominator; a change to **`_confidence_label`'s own constants** at `:1166-1171`; or a widening of
  the candidate universe that admits thin-coverage names above 82. **The desk takes no position on
  whether any of these should ship**, and this entry is never a reason to ship one (the Q025(b)
  precedent). Re-check **at the first freeze after any such change ships**, and not on a calendar.

### What a re-attempt must re-measure — nothing here is inherited

A configuration change is exactly the event that triggers re-entry, and under **DP-50(a)** it
invalidates every count above. A re-attempt re-runs the **whole** R1 limb set on the then-current
freeze — (a) label composition and single-label share, (b) and (c) both `r_join` series, (d) the LOW
arm, (e) the `overall_score × completeness_score` grid on both cohorts, (f) the `config_json` tuple
and the commit sweep, (g) label-integrity with item 10's 0.01 boundary tolerance, (h) the `d*_t`
funnel — and additionally re-verifies, read-only in the platform repo: that `_confidence_label` still
reads as at `fa70688` (`:1166-1171`), where it is called relative to the ATR-elite cap (`:1425` vs
`:1407-1423`, which is what makes the §2.2 screen well-posed), the subscriber sentence at
`super_agent_select_public.py:212`, and **whether the runtime `config_json` flags still differ from
the code defaults**. The exclusions file current at that date replaces `exclusions_v003`, and the
window is re-cut at any ship date that moves the §2.6 tuple (item 11). **E1's 0.5532 is not carried
forward as a planning rate**; it is re-measured.

### What is never re-specified, in any successor

- **E2's cut is not lowered, widened or re-based.** The 82 and the 65 are the platform's own constants
  at `:1167-1170`, not desk choices; moving either to manufacture a MED arm would test a label the
  platform does not print, and would be a re-unit of the registered hypothesis (**DP-25**, rule 3).
  There is no "completeness ≥ 55" version of this question.
- **No E1-alone successor.** A question whose only primary is the unconditional HIGH−MED contrast is
  Q027's ranking result restated on a coarser variable (§1.2, §8 clause 4, **DP-29**) and is refused
  however comfortable its exposure rate is.
- **No re-specification toward the arm that has mass.** Substituting `[80,82)`-vs-`[82,+)` for
  HIGH-vs-MED is Q027's band contrast; substituting the dark cohort for the published slate is Q027's
  population (item 1, Correction 5); substituting `completeness_score` as a continuous predictor is a
  **different hypothesis** needing its own PREREG — and on a column with no observed mass below 65.37
  it would be near-degenerate for the same reason. Each is a successor question with its own id, its
  own §1 and its own MPE, never an edit to this one (**DP-25**, the Q025(a) precedent).
- **The sealed post-hoc panel of §6 is not computed.** Item 4 tied it to the committed `eval.py` at
  the decision pass; there is no `eval.py` and no decision pass, so the weekly of 2026-09-12's
  uncontrolled "78% vs 65%" line stays uncorrected in the record — and stays unquotable, like every
  other line under `DEFERRED.md`'s preamble.

## Corrections and filings added at record

**Correction 6 (new, and the one load-bearing fact this pass adds).** **§2.6 mis-reads the platform:
it cites the *code default* as though it were the *runtime* value.** §2.6 says the enrichment flags
`enable_fundamental_enrichment` and `enable_smart_money_enrichment` are "the last two defaulting
**False**" (`services/super_agent_select_models.py:109-111`). The code default is correctly cited and
**confirmed read-only at `fa70688`** — but the **observed `sas_runs.config_json` on every one of the
67 non-excluded nights shows `enable_fundamental_enrichment = True`**, with `enable_catalyst_
enrichment = True` and only `enable_smart_money_enrichment` at its coded default. **Must read:** the
deployment's runtime configuration, not the ORM default, is the value of record for every flag in the
§2.6 tuple; on this window two of three enrichment layers populate completeness's numerator, and the
tuple is **constant across the window** (no in-window ship, so item 11's window cut does not fire
here).

**This is a PREREG mis-reading, not a platform defect, and it gets no PI of its own.** Three grounds.
(i) A runtime config that overrides an ORM default is the ordinary way a deployment is configured;
nothing is broken and nothing was rewritten. (ii) The desk already knew: **`Q029 §2` (PREREG_LOCKED)
records `enable_fundamental_enrichment` True on 67 of 68 segment nights** and registers
`fundamental_quality` as a **REMOVAL** layer on that measurement, explicitly calling the code-default
reading "contradicted by the measurement". Q036's §2.6 simply did not carry the sibling's finding
across. (iii) It rewrites no historical row, so **DP-50(a)'s repair log does not apply** — it belongs
in `DATA_NOTES.md` as a standing fact about the data that the tables do not say, which is that file's
stated purpose. Text drafted under "Routed requests → data-steward (N1)".

**Filing recommended — a PLATFORM_ISSUES row, recommendation only (DP-07, DP-48), for the
*consequence*, not the config.** What the counts show is that a **subscriber-facing field is
effectively constant**: on 542 published rows over 67 nights the printed conviction word is `high`
74.0% of the time and `medium` 26.0%, **`low` never**, and the `medium` rows are exactly the
`[80, 82)` score sliver — so *"scored X with {confidence_level} conviction"*
(`super_agent_select_public.py:212`) is a re-print of "is the score ≥ 82", and `_confidence_label`'s
completeness arm is inert under the running configuration. That is a defect claim about the field,
made entirely of population counts, and **DP-07 sends defects to `PLATFORM_ISSUES.md`, not to a
research question**. It is filed **with a recommendation and no action**: it is emphatically **not** a
finding that the label fails to predict the price path — that question is precisely the one this
entry defers, and no successor may cite the PI as evidence for it. Text drafted under "Routed requests
→ registrar".

**For the Red Team — one locked file the measurement contradicts, flagged not edited (rule 3).**
**`Q028_layer_signal_independence/PREREG.md` (PREREG_LOCKED) §9 at `:506` and §10 threat at `:580`**
state that `enable_smart_money_enrichment` / `enable_fundamental_enrichment` "default `False`" and
that `fundamental_quality` may therefore be "dead in the sample". The first is a true statement about
the code and a false one about the deployment; the second is a conditional whose antecedent is now
measured false for `fundamental_quality` (it stands for `smart_money`, which is at its coded default
and remains PI-008). **The locked file stands and is not edited**; the Red Team should read those two
lines against `STEWARD_Q036_exposure.md` §(f) and `Q029 §2` at sign-off, and check whether any Q028
dead-layer verdict sentence would name the wrong cause. **`Q035` (DEFERRED) carries the same
`enable_fundamental_enrichment = False` signature at `:146` / `:221` and is moot.**

**Other questions that read `completeness_score` or the label — named, with no correction owed.**
`Q029` (LOCKED) is the precedent and is correct. `Q027` (LOCKED, `:100`), `Q023` (LOCKED, `:65`) and
`Q024` (LOCKED, `:32`) carry `confidence_level` as a stratum or column and no verdict rests on its
spread. `Q014` (DATASET_PINNED, `:166`) independently records the 65.4 completeness floor and its
Pool A / Pool B reasoning is **corroborated**, not disturbed. `Q005` (LEDGERED) read
`completeness_score` as a channel component with no outcome column and is unaffected. **`Q032`
(`:368`), `Q033` (`:476`) and `Q034` (`:498`) register `confidence_level` *terciles* as descriptive
strata**: on this data that column takes two values on the published slate (74% / 26% / 0%), so those
terciles will collapse to at most two cells and most will sit under the 20-contributing-night floor.
Their own §4 floors already mark a thin cell descriptive, so **nothing is owed and nothing is edited**
— it is noted here so the collapse is expected at their decision passes rather than discovered.

## Routed requests

### data-steward — R1 (counts only) — **CLOSED 2026-09-14**

**Answered in full by `research/reports/STEWARD_Q036_exposure.md` (all eight limbs (a)–(h), counts
only, no outcome read). Its result is the DEFERRED call recorded above; nothing further is asked of
the Steward on this limb.** The request is preserved verbatim below as the record of what was asked
before the counts existed, and as the template a re-attempt re-runs unchanged.

Q036 (does the published "high / medium / low" conviction label actually mark a better price path —
PREREG §5.1 / §5.3 request R1, as amended by `DECISIONS.md` items 6, 7, 10 and 12) needs a
**counts-only** exposure measurement on the **frozen** data — `research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json` against `research/data/exclusions_v003.json`, plus read-only
`git log` / `git show` in the platform repo — and **never a live query** (DP-50(c)). It is **blocking
for the lock**, and its binding limb is one no desk report has measured: this question's contributing
night needs **both label arms present on the same published slate**, on top of every screen your
Q027 / Q031 / Q034 reports already apply. **No outcome of any kind:** no touch, no first-touch date,
no return, no excursion, no `outcome_*` column, no `sas_selection_excursion`, no
`uoa_symbol_daily.fwd_return_*`, and no label-versus-outcome cross-tab of any shape; forward bars may
be read **only** to establish that a bar exists (gradeability and maturity accounting), never for a
value. Period: pick nights **2026-06-01..2026-09-10** (DP-06's segment; every quantity here is a
16:05 ET property with no outcome attached, so the widest legal span is used); **denominator for
every rate = elapsed sessions** (calendar sessions minus holidays, exclusions *not* pre-removed — the
Q019 / Q022 / Q023 / Q027 / Q031 / Q032 / Q034 convention), with `exclusions_v003` nights and DP-04
late-`finished_at` nights removed from the numerator. Please return, by month and for the period as a
whole: **(a) the per-night count of published rows** (`qualified IS TRUE AND selected_rank IS NOT
NULL`) **by `confidence_level`**, with the count and share of nights whose published slate is
**single-label** (all HIGH, or all MED) — that share is the single biggest determinant of this
question's power. **(b) `r_join`, the limb that decides** — the share of **elapsed sessions** that are
non-excluded **and** carry a defined `d*_t` under Q027 §2.2 / §2.4's screens (published rows only for
the median: `lane_plans.swing_trading.targets[0]`, the split-scale payload screen, `d_L3 ∈ [0.25,
10]`, ≥ 60 prior split-adjusted bars, the 1–2-survivor trailing-20-night fallback, zero-survivor
nights excluded whole, `payload_disabled` nights excluded whole) **and** carry **≥ 1 HIGH and ≥ 1 MED
eligible published row** — reported three ways: (i) numerator and denominator both over the **maximal
sub-period whose nights grade to t+20** on `manifest_prices_v001` (please state that sub-period's last
pick night, derived from the calendar), (ii) the full-denominator rate for the record, and (iii) the
marginal `ρ_co` (nights with both labels ÷ non-excluded nights) **as a diagnostic only** — the
schedule is built on `min(r_join(i), 0.6620)` (DECISIONS item 6), so a rate faster than 0.6620 changes
no date. **(c) The same `r_join` restricted to rows with `overall_score ≥ 82`** — E2's contributing
series, a subset of (b) — and the count of nights that fall out of (b) into non-contributing solely
because every MED row sits in `[80, 82)`. **(d) The number of nights carrying any LOW published row,
and LOW rows per night**, so item 12's demotion is recorded on measured counts. **(e) The joint
distribution of `overall_score × completeness_score` on published rows**, as counts in the
`[80,82)/[82,85)/[85,88)/[88,90)/[90,100] × [35,45)/[45,65)/[65,100]` grid, plus the same grid on the
unpublished `threshold_pass` cohort (the B3 / dark-set panel's population — note that
`threshold_pass` already requires `overall_score ≥ 80 ∧ completeness_score ≥ 35`,
`services/super_agent_select_scoring.py:1518-1521`, so please report its label composition rather than
assuming it is broader). **(f) The per-night `sas_runs.config_json` tuple** — scoring weights,
timeframe multipliers, `min_completeness`, `publication_floor`, `bear_publish_threshold`,
`max_output_cap`, `qualification_threshold`, the ATR-elite caps and the three enrichment enable-flags
(`enable_catalyst_enrichment`, `enable_fundamental_enrichment`, `enable_smart_money_enrichment`) —
**stating whether that tuple has ever moved inside the sealed window**, together with the DP-50(a)/(b)
commit sweep since manifest SHA `fa70688` over the same settings and the lane-plan writer, **with an
explicit answer even when it is "none"**, and whether **v1.7** is scheduled to ship inside
2026-09-15..2027-09-13. This limb is load-bearing here in a way it is not elsewhere: the enrichment
flags *are* the completeness score, so a ship inside the window cuts it (DECISIONS item 11). **(g) The
label-integrity mismatch rate** — recompute `_confidence_label(overall_score, completeness_score)`
from the stored columns using the literal constants at `super_agent_select_scoring.py:1167-1170`
(`high` iff `overall ≥ 82 ∧ completeness ≥ 65`; `medium` iff `overall ≥ 68 ∧ completeness ≥ 45`; else
`low`) and compare with the stored `confidence_level`, reporting the mismatch count and share on
published rows **with rows within 0.01 of any of the four constants counted separately as rounding
boundary cases and excluded from the share** (DECISIONS item 10). **(h) The `d*_t` funnel counts**
behind (b): nights with zero surviving `d_L3` picks, nights on the 1–2-survivor fallback, rows dropped
by the split-scale screen, rows outside `d_L3 ∈ [0.25, 10]`, the `dominant_direction = 'mixed'` share
per label arm, and the `d*_t` distribution (median, IQR, min, max) — Q027 R1(c) measured this median
moving from ≈ 1.06 to ≈ 2.10 ATR across a single config ship, so please flag any similar movement
inside the sealed window. **The call this request decides**, with every branch fixed before your
counts are seen: **E1's `r_join` and E2's `r_join` each ≥ 0.43 per elapsed session** (80 ÷ 187
registered elapsed sessions) → **Q036 locks as written**; **either in [0.37, 0.43)** → **Q036 locks**
with the single DP-13 extension expected (80 ÷ 217 on the extended window); **either < 0.37**, or
**(c) failing while (b) clears**, or **(g) above 2%** → **Q036 goes to
`research/questions/DEFERRED.md`** with the measured rates named, the re-check trigger *"the Steward
measures ≥ 0.43 joint contributing nights per elapsed session, on both the unrestricted and the
`overall_score ≥ 82` series, over a trailing quarter"*, and — for a (g) failure — a
`PLATFORM_ISSUES.md` entry recommending investigation of what writes `sas_candidates.confidence_level`.
Please **re-solve both thresholds from the trading calendar** rather than taking my arithmetic — the
holiday list used here is 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26,
2027-05-31, **2027-06-18**, 2027-07-05 and 2027-09-06, giving 187 elapsed sessions in
2026-09-15..2027-06-11, 217 with the +30-session extension, and 225 admissible under DP-43's 12-month
ceiling (latest admissible initial decision Monday 2027-09-13, back-solving through a last t+20 of
2027-09-03 to a window end of 2027-08-06) — and a re-solve may move a threshold **up, never down**.
Please also state **the projected date each floor is first reached** at each measured rate, on **20**
sessions of maturity plus a one-week freeze margin, and flag any §4.3 stratum cell projecting below
20 contributing nights at that date (arm demotion is settled at lock and never afterwards — DP-43,
DECISIONS item 12). Report to `research/reports/STEWARD_Q036_exposure.md`.

### data-steward — R2 (successor freezes) — **WITHDRAWN 2026-09-14, not built**

**Q036 is DEFERRED, so no successor freeze is built for it and no date below stands.** The shared
selection build serving Q027 / Q029 / Q031 / Q033 / Q034 is **not** extended, re-scoped or
re-horizoned for this question; their own pins are unaffected and are not edited (the Q025 R2
precedent). Preserved verbatim as the record of the scope that would be needed on re-entry — every
date in it is struck and would be recomputed from a new lock date, out only.

_Original request (withdrawn):_

Q036 (PREREG §5.3 request R2, DP-23) needs successor freezes before its decision pass; **the dates
below are provisional until R1 lands and may only ever move out** (DP-43, DP-45). Please build and pin
a successor **selection** freeze (the same SQL and the same exclusion criteria as v001, over
`sas_candidates` for **every candidate row, published and unpublished**, plus `sas_runs` and
`market_regime_daily`) and a successor **price** freeze (`prices_daily_split`, `prices_daily_raw`),
covering pick nights **2026-09-15 .. 2027-06-11** with **≥ 60 prior sessions before 2026-09-15**; and
— only if the single DP-13 extension fires — a second pair covering pick nights **.. 2027-07-27**,
built then and not before. **This is the same selection build Q027, Q029, Q031, Q033 and Q034 are
served from**, so please build it once where the calendar permits; their own pins are unaffected and
are not edited. Six scope requirements, none optional: **(i)** the daily bar horizon runs to
**session t+20 of the last included pick night — 2027-07-13** on the corrected calendar
(DECISIONS Correction 1: the PREREG's 2027-07-12 is one session early), plus margin, delivered before
the **2027-07-26** decision date; on the extension path through **2027-08-24** for a **2027-09-13**
decision. **(ii)** The daily symbol list covers **every candidate symbol on every in-window night,
published and unpublished**, with ≥ 60 prior sessions before 2026-09-15 — the B3 distance-matched
control cohort needs the unpublished closes, ATR14, `beta60`, `atr_pct`, `runup20`, `adv20` and
forward bars to t+20 — never assumed from an earlier freeze's symbol list. **(iii)** `sas_candidates`
must preserve **`confidence_level`, `completeness_score`, `threshold_pass`, `qualification_reason`,
`selected_rank`, `qualified`**, the seven layer subscores, `cross_layer_bonus`, `conflict_penalty`,
`missing_data_penalty`, `score_details_json`, `context_json` and `public_payload_json` (the
`lane_plans` object is where `d*_t` comes from), and `sas_runs` must preserve **`config_json`** — under
DECISIONS item 11 the config tuple is a registered window-splitting condition, not a note.
**(iv)** `market_regime_daily` included with **`created_at` and `regime_version` preserved** (rule 7
stratum; the whole window is after 2026-06-09, so every label is point-in-time legal and that is a
property to be re-confirmed, not assumed). **(v)** An **add-only successor exclusions file** applying
the identical four criteria (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`,
`payload_disabled_runs`) to post-2026-09-10 nights — it may add nights and may never remove one, and
its header should state whether the `analysis_status = "disabled"` / no-`lane_plans` signature is
still present, saying so explicitly rather than silently returning an empty list. **(vi)** Rows whose
bars are missing are **excluded and counted, never back-filled or imputed**, and R1(f)'s commit sweep
is repeated for the period between the freezes — the enrichment flags and `min_completeness`
especially — with a dated `DATA_NOTES.md` entry for any repair that rewrites historical rows and an
explicit answer **even when it is "none"** (DP-50(a)). **No hourly bars are required for this
question** and none is requested: no primary and no blocker in Q036 reads one. Please re-confirm every
§5.2 date **session by session from the trading calendar** when the freeze is built; the holiday list
is 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**,
2027-07-05 and 2027-09-06. A correction to any date may move it **out, never in**.

### researcher — R3 (`eval.py`) — **NOT ISSUED; withdrawn 2026-09-14**

**No `eval.py` is written for Q036 and none exists.** The 2027-04-05 deadline is struck with the rest
of the schedule. The §6 sealed post-hoc panel was tied to that script by item 4 and is therefore **not
computed either** — nothing on the sealed nights is read. Preserved verbatim as the specification a
re-attempt would inherit.

_Original request (withdrawn):_

Q036's `eval.py` is written **once** (rule 9), against the §2 schema, **before any successor freeze
exists**, and takes the window start, the window end, both manifest paths, both exclusions-file paths
and the output directory as **arguments** — no hard-coded date, manifest name or path — so that the
byte-identical file serves the primary run, the single DP-13 extension run and the §6 sealed panel
alike. **Committed no later than Monday 2027-04-05 with its sha256 recorded, and not touched
afterwards** (DECISIONS item 14): Q027 and Q029 decide on **2027-04-12** on the same freeze, the same
published slate, the same `d*_t`, the same t+1-open entry and the same 20-session clock, and a script
written after that pass is a script written with part of its own answer in view. It must inherit
Q027 §2.2 / §2.3 **verbatim** (the `d*_t` median, the split-scale screen, the 1–2-survivor fallback,
the zero-survivor whole-night exclusion, the `[0.25, 10]` fail-loud bound, the synthetic target, the
t+1-open entry, the not-takeable rule), implement the §2.2 label-integrity screen with item 10's
0.01 boundary tolerance, print both the date-clustered and the episode-clustered CI for each primary
(DP-51), and **fail loudly** — never silently exclude — on a `regime_version` change, a `config_json`
tuple change (item 11 cuts the window at the ship date), or a `d*_t` outside the bound.

### registrar — the DEFERRED entry, the PI filing and the bookkeeping (new at record)

Q036 (`confidence_label_validity`, H-011) **does not lock**. R1 closed on
`research/reports/STEWARD_Q036_exposure.md` and both of `DECISIONS.md` item 7's independent DEFERRED
triggers fire: **E2's `r_join` = 0.0000 on every form** (0/47 matured, 0/71 elapsed, 0/67
non-excluded), and **E1 clears (0.5532, 26/47) while E2 fails**, which item 7 and PREREG §5.1 both
answer with *"DEFERRED, not lock E1 alone"*. Please do six things and no others. **(1) Write the
`research/questions/DEFERRED.md` entry** — heading `## Q036 / H-011 — "Does the published
high/medium/low conviction label mark a better price path?" — **the arm E2 compares against does not
exist on this scoring configuration**` — filed on that file's **second** admission ground (DP-43's
ceiling) **in its strongest form**, the Q025 shape: the rate is not slow, it is **exactly zero**, so
the floor date is **undefined** rather than distant. It must carry, in this order: what the question
is and why it is worth keeping (the platform prints *"scored X with {confidence_level} conviction"* at
`services/super_agent_select_public.py:212` to every subscriber and **nothing has ever tested the
word**; both primaries were registered two-sided and a confirmed *negative* was the branch with the
larger consequence); why it cannot be registered (§1.1's arithmetic — `high ⇔ score ≥ 82 ∧
completeness ≥ 65`, `medium ⇔ ¬high ∧ completeness ≥ 45` — against the measured fact that
**`completeness_score` never falls below 65.3686 in any of the 4,195 scored rows in 2026-06-01..
2026-09-10**, so `medium ∧ score ≥ 82` is an **empty cell by arithmetic**, and all 26 of E1's
contributing nights fall out of E2 because every MED row sits in `[80.05, 81.99]`); the measured
table above (E1 0.5532 / 0.3662, `ρ_co` 0.6269, E2 0.0000, (g) 0.000% of 542, (d) 0 LOW nights, 67
non-excluded of 71 elapsed, 47 matured); **why waiting does not fix it** (DP-13 extends a *marginal*
floor by +30 sessions on measured counts — it cannot create a row in an unsatisfiable cell, the
projection at a zero rate is undefined, and the extension is registered only at a lock that never
happens); what was considered and rejected (E1 alone — §1.2 / §8 clause 4 / DP-29; a lowered
completeness cut — DP-25; the dark cohort — item 1 and Correction 5, it carries the *identical*
floors and the identical 65+ completeness ceiling, 564 medium / 82 high / 0 low on 646 rows; DP-13);
and the re-entry condition **exactly as worded in "What would move it back into the backlog" and
"What a re-attempt must re-measure" above** — a measured trigger on a trailing quarter, a necessary
precondition never once observed, the platform conditions stated as **what must be true, not as a
request**, and **no calendar re-check date**, because the blocker is structural. Close it with the
"never re-specified" list verbatim and with this file's preamble sentence (nothing may be reported,
briefed or quoted). **(2) Bookkeeping in the entry:** no verdict of any kind, no `eval.py`, no
`results/`, no data unsealed; **F2's correction set returns to 16** (Q023 2 + Q027 2 + Q029 10 +
Q031 2 = `Q031 §7`'s own figure), so **no locked file is edited**; `research/BACKLOG.md` marks
**H-011 — DEFERRED 2026-09-14**, not registered and **not merged into Q027**; **the number Q036 is
consumed and not reused**. **(3) Controller:** `state.json` → `DEFERRED` (`--by desk`); **no
`PREREG_LOCKED`, no `schedule.json`, no pin** (Q020 / Q025 / Q030 precedent). **(4) Do not run
`apply`:** `PREREG.md` and `DECISIONS.md` are preserved **exactly as drafted**, Corrections 1–6 stand
in `DECISIONS.md`, **`DECISIONS.md` governs where the two disagree**, and a re-entry resumes at
`@registrar apply Q036` with everything folded in then (Q030 precedent). **(5) File one
`research/PLATFORM_ISSUES.md` row, recommendation only (DP-07, DP-48), next free id `PI-016`,
severity `med`, status `OPEN`:** *"Conviction label degenerate on the published slate:
`completeness_score` never falls below 65.37 (min 65.3686 of 4,195 scored rows, 2026-06-01..09-10),
so `_confidence_label`'s completeness arm is inert — 401 high / 141 medium / **0 low** on 542
published rows, and every `medium` row is the `[80,82)` score sliver. The subscriber sentence at
`services/super_agent_select_public.py:212` therefore re-prints 'is the score ≥ 82'. Counts only, no
outcome read; source `research/reports/STEWARD_Q036_exposure.md` §(a)/(c)/(e). Recommendation for
Haci: `fix` = re-derive the `:1167-1170` constants against the observed completeness distribution, or
rename the field to the coverage measure it is; `accept` = leave it and stop describing it as
conviction. **Not** a finding about whether the label predicts the price path — that question is
Q036 and it is DEFERRED; no brief may cite this row as evidence for it. Any brief that follows hands
the coding agent no database step (DP-49)."* **(6) Board:** `research/BOARD.md` shows Q036 as
DEFERRED with the one-line reason and the measured trigger, and the PI-016 row in the issues list.
**Do not write into `research/data/`** — the `DATA_NOTES.md` paragraph is routed to the Steward
below.

### data-steward — N1 (a `DATA_NOTES.md` note, new at record; no measurement requested)

One note for `research/data/DATA_NOTES.md`, from your own §(f). **Not a repair-log row** — nothing was
rewritten, so DP-50(a)'s table does not apply; this belongs in the body of that file as a standing
fact about the data the tables do not say. Suggested heading `## Enrichment flags: the runtime config
overrides the code default (Steward, Q036 R1, 2026-09-14)`, and text to the effect of: *"Several
PREREGs cite `services/super_agent_select_models.py:109-111` and state that
`enable_fundamental_enrichment` and `enable_smart_money_enrichment` default `False`. The **code
default is correctly cited**; it is **not** the value the deployment runs. Measured on
`sas_runs.config_json` over all 67 non-excluded nights of 2026-06-01..2026-09-10
(`STEWARD_Q036_exposure.md` §(f)), and independently on 68 nights by `Q029 §2` (67 of 68):
`enable_catalyst_enrichment = True`, **`enable_fundamental_enrichment = True`**,
`enable_smart_money_enrichment = False` (its coded default), constant across the window with no
in-window ship. **Rule for studies: the runtime `config_json` tuple, pinned per night in the freeze,
is the value of record for every enrichment flag, weight and multiplier — never the ORM default.** A
PREREG that reasons from the ORM default reasons about a configuration the platform does not run; the
consequence measured in Q036 is that two of three enrichment layers populate `completeness_score`'s
numerator on every row, and `completeness_score` never falls below 65.3686 in 4,195 scored rows,
which makes `_confidence_label`'s `medium` and `low` tiers unreachable on the published slate
(`PI-016`; Q036 DEFERRED for that reason). `Q028 §9/§10` (locked) carries the code-default reading
and is flagged to the Red Team rather than edited."* No query and no count is requested — every
number above is already in your own report.

## Schedule

**DEFERRED — no schedule. The provisional block set at `decide` is STRUCK in full.**

decision_date: **none — DEFERRED** · extension_date: **none** · hard_stop: **none** ·
rule: **n/a (deferred before lock; the gate that would have set these dates did not clear)**

- **why there is no date:** the binding limb (E2's `r_join`) measures **exactly 0.0000**, so the
  projected date at which floor A (80 contributing nights) is reached is **undefined**, not distant.
  E1 alone would clear 80 nights in ≈ 145 elapsed sessions, and that number decides nothing — E1 alone
  is not a question this desk registers (§1.2, §8 clause 4).
- **STRUCK — the provisional block, recorded so no successor inherits it** (the Q025 precedent):
  ~~decision_date 2027-07-26 · extension_date 2027-09-13 · hard_stop 2027-09-13 · rule
  exposure-driven~~; ~~window 2026-09-15 .. 2027-06-11 = 187 elapsed sessions, extended .. 2027-07-27
  = 217~~; ~~maturity t+20 = 2027-07-13, extension maturity 2027-08-24~~; ~~halves H1 2026-09-15 ..
  2027-01-29 / H2 2027-02-01 .. 2027-06-11~~; ~~`eval.py` deadline 2027-04-05~~. On any re-entry the
  **whole** schedule is recomputed from the new lock date at the then-measured rate, **out only** —
  never carried forward (DP-43, DP-45).
- **what survives the striking, because it is method rather than a date:** the gate thresholds are
  re-solved, never lowered (item 7); the scheduling rate stays `min(r_join, 0.6620)` on the **joint**
  contributing event, never a marginal (item 6); floors stay 80 per primary and 20 per reported cell
  (DP-21); the corrected holiday list stands (item 5, Correction 1) and a re-solve may move a date
  **out, never in**.
- **DP-50(b):** **no flag-off constraint is owed by Q036 and none is asserted.** The deferral removes
  the desk's only claim on the §2.6 settings, and a change to them is the very thing that could make
  this question testable again. Q028, Q029 and Q027 keep their own constraints; Q036 adds none.

## Standing rules added

_none. **No DP entry is added from a DEFAULTED item** (it is not Haci's word), and none is added at
`record` either: a deferral settled by a gate fixed before the counts is the application of DP-13,
DP-21, DP-43 and DP-45 as they already stand, not a new rule._

## Standing rules proposed

Four, for Haci to confirm or refuse when he next reviews the board. None is in force; all four were
applied inside Q036 as decisions of this pass only.

- **A floor is projected on the rate of the event it counts, not on a marginal of it.** Where a
  contributing night requires a conjunction (a valid distance **and** both arms present, a complete
  ladder **and** a usable stop), the schedule is built on the **measured joint rate**, never on the
  product of marginals and never on the looser of them. (From Q034 items 7 / 8 and Q036 item 6 — the
  same optimism found twice in two days, in two different questions' own variables.)
- **An arm read from a stored classifier column is verified against the code that writes it, before
  the lock.** The desk recomputes the column from the platform's own constants at the pinned SHA,
  counts mismatches with a rounding-boundary tolerance, blocks the question above a registered share,
  and measures that share on sealed nights as a lock gate rather than discovering it at the decision
  pass. (From Q036 item 10.)
- **A gate limb measuring exactly zero is a deferral, never an extension.** DP-13's single automatic
  extension rescues a floor that is *marginal* on measured counts; where a contributing-night rate is
  **0.000 because the arm's membership condition is unsatisfiable on the running configuration**, the
  projected floor date is undefined and no window length reaches it. Such a question goes to
  `DEFERRED.md` **at the gate**, with the structural reason named and a **measured** re-entry trigger
  rather than a calendar re-check. (From Q025 item 14 and Q036 record item 3 — the second time in two
  days that a zero rate was structural rather than thin.)
- **The runtime `config_json` is the value of record, never the ORM default.** A PREREG that reasons
  from a code default (`enable_*_enrichment`, a weight, a threshold) is reasoning about a
  configuration the deployment may not run; the per-night `config_json` tuple pinned in the freeze is
  what a question must read, and the desk checks it **before** the lock rather than at the decision
  pass. (From Q036 Correction 6, with `Q029 §2` as the prior instance and `Q028 §9/§10` as the locked
  file the measurement contradicts.)
