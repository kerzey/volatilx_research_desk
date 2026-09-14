# Q031 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous, DP-40..48) · Source: PREREG.md "Open decisions before
lock", 5 items (+ 9 decided or routed here: the two routed requests named in §5.3, and seven the
draft settles silently or leaves to `record`)
**`record` pass: 2026-09-14, on `research/reports/STEWARD_Q031_exposure.md` (R1, counts only).**
R1 is satisfied and closed; **R2 stays routed and open** (successor freezes, due before the decision
date, DP-23). Every date in this file is now **final**, not provisional.

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

## The headline — after `record`

**Nothing is demoted, `m = 2` stands, Q031 is not DEFERRED, and it now locks.** R1 measured series B's
contributing-night rate under §2.5's registered rule at **47/71 = 0.6620/elapsed session** — below the
0.6723 that Correction 1 derived for the unchanged window — so **branch (i) does not fire and branch
(ii) does**: the window end moves **out for both series**, from 149 to **153 elapsed sessions**
(pick nights **2026-09-15 .. 2027-04-23**), the blocks are re-cut at the registered 40/40/20
proportion, and the decision date moves out from Monday 2027-05-24 to **Monday 2027-06-07**.
**8.7 months from the lock** (266 days), inside DP-43's 12-month ceiling (2027-09-14) by 3.3 months —
**so the question is not DEFERRED.** Branch (iii) (demotion of P2 to descriptive, `m = 1`) does **not**
fire: an admissible window reaching 100+ contributing nights for series B exists well inside the
ceiling. **Every block of both series projects ≥ 20 contributing nights** (series B: 40.4 / 40.4 /
20.5; series A: 41.2 / 41.2 / 21.0), so **no arm is demoted to descriptive under DP-43** and
§8's cell floor is met per block per series.

**The three R1 findings that could have changed the design, and did not.** (e) Series A's rate is
**RECONFIRMED bit-for-bit at 0.6761 (48/71)** by an independent recomputation — two counts of the same
definition on the same freeze agree, so there is **no DP-50(a) disagreement** to split anything on.
(a) The cost of the stricter ≥ 5-matched-controls floor, measured, is **zero**: pool depth never falls
below 37 on any matured night, so the registered rule, Q006's ≥ 1-pick rule and the drop-the-thin-pick
variant all return the same 47/71, and the only binding night is **2026-06-02**, which has *zero*
valid picks (no `lane_plans` — the `payload_disabled_runs` signature item 12 already excludes).
The registered rule is **not** relaxed on that finding (DP-21, DP-45); it is simply not costly.
(f) The commit sweep since `fa70688` is **NONE** (`HEAD` unchanged at `d19c9a9`) and **no v1.7
promotion date exists** inside 2026-09-15..2027-07-19 — stated as an *absence of a schedule*, not a
guarantee, and item 13's window-cut rule plus §9's flag-off constraint stand unchanged and are now
re-dated to the later decision date.

**Arithmetic checked against DP-43's own recipe, not taken on trust** (the Steward's 2027-06-07 is
confirmed): window end **2027-04-23** (session 153, Friday) **+ 20 sessions maturity = 2027-05-21**
(Friday) **+ one calendar week = 2027-05-28**, first Monday on or after = **2027-05-31 — Memorial Day,
a listed market holiday** — so the next Monday, **2027-06-07**. The holiday skip moves the date **out**,
which is the only direction DP-43 and DP-45 allow. The minimal window was re-solved independently:
S = 149 gives 78.8 nights across `W1 ∪ W2` (short), S = 151/152 give a short `W3` (19.9), **S = 153 is
the smallest window meeting both per-block floors simultaneously** (80.8 and 20.5) once the 40/40/20
cuts are rounded — the Correction-1 class of error again, and the reason a sum of independent floor
dates (121 + 31 = 152) is **not** the answer.

**All five of the draft's own open items go the Registrar's way. Four are DECIDED** on DP entries
and locked precedent; **item 5 (lock now vs wait for Q006/Q027) is DEFAULTED** under DP-43 and rule 3,
and joins **two more DEFAULTED** items the draft settled silently: the prospective-only window start
(the Q027 #7 shape) and the window end / decision date (R-3, settled at `record` on R1, out only).
**Two remain ROUTED** to the Data Steward: **R1** (counts only, **blocking for lock**) and **R2**
(successor freezes, due at the decision date, blocking nothing — DP-23). **Four corrections** are
listed for `apply`; three tighten a clause, one fixes arithmetic in the strict direction, and none
weakens anything.

**Rule 14: no exception is requested and none is needed** — every input is a 16:05 ET candidate
field, a pinned bar dated ≤ t, or the session t+1 open used **only** as an entry price; §6's table
declares each one and §6's `eval.py` clause freezes every eligibility, distance, match, block,
episode and stratum field before any post-pick-night bar other than that open is loaded. **DP-05 is
untouched and DP-41 is not engaged.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | The decay MPEs, and DP-20's doubling clause | DECIDED | **Option A — `\|D1ᴬ\| ≥ 0.05` in Spearman-ρ units and `\|D1ᴮ\| ≥ 5.0 pp`, exactly as H-082 names them, with §8 clause 6's level gate registered in place of the doubling.** B (10.0 pp / ρ 0.10) is refused for a validity reason, not a taste: `S^B_t` is *already* control-adjusted, so at a 10.0 pp bar a **complete collapse** of a mid-sized edge (8 pp → 0) is unconfirmable by construction, and on the IC — where the *level* MPE is itself 0.05 — a 0.10 decay bar would require the IC to have exceeded 0.10 and then gone negative. An MPE that cannot be reached by the event the hypothesis is about is not conservatism. What replaces the doubling is **strictly harder than either bare MPE**: clause 6 requires the later blocks' own level to have fallen **below** the edge MPE, so a fall from excellent to good returns `SHRUNK_NOT_GONE` (INCONCLUSIVE) and licenses a monitor only. **Neither MPE is lowered at the decision pass in any branch** (§4.2, §8). | **DP-20** (+5.0 pp for a control-adjusted touch-rate endpoint; its larger-MPE clause is permissive, not mandatory, and is declined here with the reason stated in §4.2); **DP-25** (units and cuts come from the hypothesis as written — 5.0 pp and ρ 0.05 are H-082's own numbers, and the Registrar does not re-unit a hypothesis); **DP-44** (no rank-correlation unit exists and none is invented — the ρ 0.05 is Haci's own H3 PASS line); **Q029 §4.2 / DECISIONS #1** and **Q027 DECISIONS #3**, the identical reasoning on the identical two units; **DP-45** for keeping the strict half as a blocking level gate rather than choosing between the two |
| 2 | The primary estimator: fixed blocks vs the CUSUM's own magnitude | DECIDED | **Option A — `D1 = m̄(W2) − m̄(W1)` on the three blocks fixed at this lock by session index and proportion (40/40/20), with the CUSUM kept as §8 clause 9, a blocking clause that locates the break and prints `τ̂` in every branch.** B has one defensible answer against it and it is decisive: a magnitude read at a **data-chosen** change point is biased away from zero **by its own search**, and its two segments have no sample size knowable at lock — so **no floor could be written for it**, and rule 6 requires one. A fixed-block contrast has both, and it retains power against a *gradual* decline (early block vs late block), which is the shape PI-010's falling elite count and Q005's drifting score distribution would actually produce. H-082's named test is not deleted: it is kept in the role it can honestly fill (*is there a break, and where*), and the τ̂-based magnitude prints as a description with its selection caveat attached. | ground 3 — one defensible answer: rule 6's floors cannot be written for a data-chosen segment; **rule 9** (the script is deterministic and written once); **DP-45** — B is the option whose estimator is biased **toward** a positive finding; **DP-25** (the hypothesis's named test survives as clause 9 rather than being dropped) |
| 3 | The floor on the persistence holdout `W3` | DECIDED | **Option A — DP-21's cell floor of 20 contributing nights; `W3` blocks at whatever count it has.** `W3` is not a primary endpoint: `D2` can only ever **prevent** a DECAY verdict (§8 clause 5) and never produce one, so the 80-night per-primary floor does not attach to it — it attaches to `D1`, and `W1 ∪ W2` carries it. Option B would demand ~140 contributing nights per series, put the initial decision date past DP-43's 12-month ceiling and **defer the question whole**, which is a worse outcome than testing it: DP-43 defers for a ceiling breach, it does not manufacture one. §10 threat 11's reading of the noise is accepted as written — a noisy `W3` can fail a real decay (INCONCLUSIVE, re-registrable later), and it cannot pass a spurious one on its own because every other clause still binds. | **DP-21** (80 per primary endpoint, 20 per reported cell — read at its two stated levels, neither moved); **DP-43** (the 12-month ceiling; a window that cannot reach its floors inside it defers); **Q027 DECISIONS #10** (a blocker runs at the cell floor and blocks at whatever count it has) |
| 4 | Series B (`E_t`) as a second primary | DECIDED | **Option A — `D1ᴮ` is registered as a primary now, with the demotion rule settled at this lock and fired only on R1's measured rate (item 8).** H-082 names both series with their own MPEs, and the expectancy series is the one Haci actually trades. A is also the **harder** path in every direction that matters: BH runs at `m = 2` rather than `m = 1`, and a question-level DECAY requires **both** primaries to move with the same sign (§8), so registering P2 can only raise the bar for a positive verdict. B would leave the slate-level series — the one with a §9 consequence — as an unfalsifiable description. | **DP-25** (both series and both MPEs are the hypothesis as proposed); **DP-43** (an arm below floor is demoted to descriptive **at lock**, never dropped afterwards — which is exactly what §5.1 registers); **DP-45** (A carries the larger correction set and the both-must-move rule); rule 8 |
| 5 | Locking now vs waiting for Q006 (2026-10-05) / Q027 (2027-04-12) to establish there is an edge to decay | **DEFAULTED** | **Lock now, prospectively, carrying §8 clause 1's `NO_EDGE_TO_DECAY` precondition and the risk it names.** Waiting is refused for the reason pre-registration exists: Q006's and Q027's results would otherwise shape this question's blocks, MPEs and clauses — the exact contamination rule 3 prevents — and the night series **cannot be accrued retroactively**, so B costs a year of nights and buys nothing clause 1 does not already handle honestly. The cost is stated rather than hidden: if either level question returns NULL, this year of waiting yields `NO_EDGE_TO_DECAY` on that series, which licenses nothing (§9) and is not a null result about decay (§10 threat 2). | **DP-43** (the decision date is 8.3 months, inside the 12-month ceiling — the question locks; DEFERRED is for a ceiling breach, not for a preference); **rule 3** (pre-register before unsealing); **DP-47** (registration order — a hypothesis whose data does not yet exist is registered now and waits); not taken: defer registration until Q006 and Q027 report — costs a year of nights and lets their results shape this design |
| 6 | The window start: prospective-only, and the sealed stretch as a labelled panel | **DEFAULTED** | **Pick nights ≥ 2026-09-15 only** — the first session after the lock commit, so no night whose 16:05 ET run may precede the lock can enter. The sealed stretch (2026-06-01..2026-08-12) prints **once** as a labelled post-hoc panel split at 2026-07-06, entering **no verdict, no block, no CI comparison, no q and no §9 rule**, and it is **never the reference block** — for two independent reasons, each sufficient: it has already been read *for this hypothesis* (the weekly §7 rolling four-week 90+ trend, H-010's April→August fade, Q005's elite-rate halving are what generated H-082), and it sits on the far side of the 2026-07-08 publication-gate ship that doubled `d*_t` from ≈ 1.06 to ≈ 2.10 ATR, so a contrast across it would measure the ship. | **DP-43**; **Q027 DECISIONS #7** verbatim (same population, same panel, same split date); rule 3; not taken: use the sealed stretch as `W1` — decides now, but tests the data that proposed the hypothesis |
| 7 | Window end, decision date, extension, hard stop | **DEFAULTED (R-3)** — **final at `record`, 2026-09-14, on R1** | **Final: window pick nights 2026-09-15..2027-04-23 (153 elapsed sessions), decision Monday 2027-06-07, single DP-13 extension to ..2027-06-07 (183 sessions) decided Monday 2027-07-19 = the hard stop, then DEFERRED.** Moved **out** from the provisional dates below when R1 measured series B at 0.6620 (branch (ii)); it could never have moved in. *(The provisional text, kept so the move is auditable:* **window pick nights 2026-09-15..2027-04-19 (149 elapsed sessions), decision Monday 2027-05-24, single DP-13 extension to ..2027-06-01 (179 sessions) decided Monday 2027-07-12 = the hard stop, then DEFERRED.** Built on the **measured, maturity-truncated 0.6761**, never the 0.9577 eligible-night proxy (an extrapolation past the price freeze's own forward-bar horizon, and the one that pulls the date **in**) and never Q023's 0.9538 published-pick rate. Floor A (≥ 80 across `W1 ∪ W2`) binds at session 119 = 2027-03-05; floor B (≥ 20 in `W3`) binds at session 149 = 2027-04-19 and is the window end; DP-24's 30 post-lock nights land at session 45 and are non-binding, satisfied by construction. **These dates are final for series A and provisional for the question**: R1 may move them **out** (item 8), and may never move them in.)* Under the final window the binding floor is again **B** — ≥ 20 contributing nights in `W3` at the window end, session 153 — for the **slower** series (B), and floor A binds at session 122 for series B (121 for series A). | **DP-43** (the window that reaches every floor, at the measured rate, plus maturity and a one-week freeze margin, first Monday on or after — with a holiday Monday skipped to the next Monday, the Q027 §5.2 form); **DP-13** (+30 sessions, one extension, fired on `eval.py`'s measured counts and never on a projection); **DP-21**, **DP-24**; **DP-45** (out only; the slower measured rate of the two series, never the faster extrapolated one); not taken: the 0.9577 eligible-night proxy — decides ≈ 2027-03-29 |
| 8 | Series B's contributing-night rate, the window end it implies, and the P2 demotion | **SETTLED at `record`** (was ROUTED → data-steward; R1 delivered 2026-09-14) | **Measured 47/71 = 0.6620 contributing nights per elapsed session** (`STEWARD_Q031_exposure.md` (a)) → **branch (ii) fires**: window **2026-09-15..2027-04-23 = 153 elapsed sessions**, blocks re-cut at 40/40/20 — `W1` 1–61 (2026-09-15..2026-12-09), `W2` 62–122 (2026-12-10..2027-03-10), `W3` 123–153 (2027-03-11..2027-04-23) — decision **Monday 2027-06-07**, `m = 2`, **no demotion**. Branch (i) misses by 0.0103/session (0.6620 < 0.6723); branch (iii) does not fire. The registered ≥ 3-picks / ≥ 5-controls rule is **unchanged** on this count, as fixed in advance — and measured, it costs nothing (pool depth min 37). Original routing text follows: waits on **R1** (counts only) — **blocking for lock** (Correction 2), because **DP-43 settles a demotion at lock and never afterwards**. Three branches, all fixed now so none is argued with counts in view: **(i)** measured series-B rate **≥ 0.6723/elapsed session** (Correction 1) → nothing changes, `m = 2`, item 7's dates stand; **(ii)** slower, but a window end at the later of the two series' floor dates still yields a decision date inside DP-43's ceiling (2027-09-14) → **the window end moves out for both series** (one window, one freeze, one set of blocks, the 40/40/20 proportions re-applied and the session indices recomputed), `m = 2`, every date recomputed **out only**; **(iii)** slower still, so that no admissible window reaches 100 contributing nights for series B inside the ceiling → **P2 is demoted to descriptive at this lock**, `m = 1`, the question runs on series A alone on item 7's dates and series B prints without a verdict. **No fourth branch, no reduced floor in any branch, and the registered contributing-night rule itself does not change on R1** — only the dates and the demotion do. | — |
| 9 | Successor freezes | **ROUTED → data-steward — open** (dates fixed at `record`; due before 2027-06-07) | waits on **R2** — a selection freeze (`sas_candidates` **every row, published and unpublished**, `sas_runs`, `market_regime_daily`) and a price freeze (daily bars for **every candidate symbol on every in-window night**), pick nights 2026-09-15..the final window end with **20 forward sessions** beyond the last included pick night and **≥ 60 prior sessions** before 2026-09-15, plus the **add-only successor exclusions file** on the identical four criteria; the extension pair only if DP-13 fires, built then and not before. Due before the decision date; **not a blocker for lock** (DP-23). A **superset of Q027's R2** (same population, window extended), built once and serving both. **Dates now fixed (item 8, branch (ii)): pick nights 2026-09-15..2027-04-23, daily bars through 2027-05-21, delivered before Monday 2027-06-07; extension pair only if DP-13 fires — pick nights ..2027-06-07, bars through 2027-07-07, delivered before Monday 2027-07-19.** | — |
| 10 | The time null: H-082's "shuffle nights within episodes" vs B1's circular block permutation | DECIDED | **B1 as drafted — circular block permutation of the ordered night series, expected block length 10 sessions, 10,000 draws, seed 20260914, two-sided** — with the episode kept as a *cross-sectional* resampling unit in CI 2, where DP-51 puts it. A plain within-episode shuffle destroys the series' autocorrelation, so a slowly-drifting but stationary series would be declared a break far too often: the re-specification is the option that makes a positive **harder**, not easier, and the draft records it in §3 rather than applying it silently. 10 sessions is the desk's standing value (Q004 / Q007 / Q009 / Q011 / Q015 / Q023 / Q027). | ground 2 — the 10-session block length and the circular-block form are locked precedent in seven questions; **DP-26** (a Registrar convention fixed at lock, not derived from a sealed outcome); **DP-51** (the episode belongs in the CIs); **DP-45** |
| 11 | The series-B contributing-night rule (≥ 3 valid picks, each with ≥ 5 matched controls) vs Q006's ≥ 1 pick | DECIDED | **The stricter rule as drafted, fixed at lock**: a night is non-contributing for `S^B` if fewer than 3 valid picks remain, or if any retained pick carries fewer than 5 matched controls; a pick with an **invalid target** (§2.2 step 1) is excluded and counted, never silently dropped. A night-mean of `Delta_p` over one or two picks is a two-observation mean of a control-adjusted difference, and the whole point of `S^B_t` is that it is a *night* statistic. R1(a) measures the rate under **both** forms so the cost of the stricter one is visible in counts — and the count is used only for the dates and the demotion (item 8), **never to relax the rule**. | **DP-21** (the stricter of two readings, never the weaker); **DP-26** (an inference convention fixed before any outcome exists); **DP-45**; **Q027 DECISIONS #5** (the ≥ 30-eligible-rows analogue, same construction, same direction) |
| 12 | Exclusions inside a window every night of which postdates every existing freeze | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** — the newest file on disk, verified — with the **add-only successor exclusions file** issued with the successor selection freeze, on the identical **four** criteria Q027 fixes at its lock (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10. The successor file may only **add** nights; no night is ever removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be; `exclusions_v003.json` is not edited (research/data/ is not writable from here). Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. DP-04 applies mechanically on top. The fourth criterion matters more here than in Q027: a night whose published slate carries `analysis_status = "disabled"` / no `lane_plans` has **zero** valid picks, so it is a zero-`d*_t` night for series A *and* a no-`S^B` night for series B, and excluding it whole is the only reading under which neither series imports a distance from a different cohort. | **DP-22** read as "one list, one set of criteria" — its "cite the newest file" clause presumes a sealed window and Q031's is entirely post-freeze; **Q027 DECISIONS #11** and its `record` amendment, same construction; **DP-04** |
| 13 | A mid-window change to what `overall_score` *is*, and the DP-50(b) constraint that follows | DECIDED | A change to the SAS weights, the timeframe multipliers, `qualification_threshold`, the ATR-elite caps, the GEX-missingness offset or a scoring enable-flag — **including any promotion of the v1.7 score** — makes `overall_score` **two different features**: the window is **cut at the ship date**, the post-ship segment becomes the question's window with the whole §5 schedule recomputed from it (**out, never in**, same single extension, same ceiling measured from the original lock), the pre-ship segment becomes a labelled descriptive panel, and if neither segment reaches the floors inside the ceiling Q031 is **DEFERRED**. Running the other way, DP-50(b): any such platform change is **flag-off until 2027-05-24** (2027-07-12 if the extension fires), checked before any fix brief is written — this extends Q027's and Q029's identical constraint by about six weeks and is **the tightest such constraint on the board**, because for a decay question a scoring ship does not merely split the data, it *becomes* the explanation for what the question measures. A **publication-gate** change (`publication_floor`, `bear_publish_threshold`) is **not** a scoring split and does not cut the window, but it moves `d*_t`'s source cohort, so its per-night value is read from `config_json`, the distance series is printed across the ship date, and both series print split at it as a labelled descriptive panel. `eval.py` **fails loudly** on any cross-freeze disagreement in `overall_score`, `conflict_penalty` or `dominant_direction`. **No such split exists at the lock, checked rather than assumed** (Q027 R1(g): sweep NONE, every scoring field constant across all 71 in-window runs, `outcome_corrections` 0 of 125); R1(e) re-runs the sweep and asks whether v1.7 is scheduled inside 2026-09-15..2027-07-12. | **DP-06** / **DP-50(a)** (a repair or config change splits a column into two features at the ship date); **DP-50(b)** (ship timing checked against in-flight questions, the PI-011 / Q010 pattern); **DP-50(c)** (the sweep runs on the pinned freeze and the read-only repo, never a live query); **Q027 DECISIONS #12** |
| 14 | The BH sets, and `m` | DECIDED | BH within the question runs over **`D1ᴬ` and `D1ᴮ`, `m = 2`, fixed in every branch** — both endpoints carry a verdict, an endpoint short of floor still has its p computed, and no primary is dropped afterwards (dropping one would lower the bar for the survivor). `m` falls to **1 only** under item 8 branch (iii), settled at this lock. Across the family, **F2 never falls below the 16 primaries standing at this lock** — Q023 (2) + Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) = 16, arithmetic cross-checked against Q029 §7 (its F2 companion set of 14 at L = 5). **`D1ᴮ` additionally carries the F1 companion correction** — Q006 (2) + Q024 (6) + Q025 (2, which never shrinks) + Q029 (16) + `D1ᴮ` = **27**, cross-checked against Q029 §7's F1 = 26 — **with the larger q quoted and deciding** (the Q015 / Q020 / Q029 pattern: a decay test on Q006's own statistic is not independent of Q006's). `D2`, the CUSUM clause, B4's reweighting, the attribution limb and every §4.3 panel are blockers or descriptions and enter no correction set. Q005 stays excluded, for the stated reason. | rule 8; **DP-29** (family by the primary endpoint's subject — calibration → F2 — with an overlapping hypothesis merged, not double-counted; Q029 owns the layer endpoints, so the attribution limb licenses nothing); **Q027 DECISIONS #13**, **Q029 DECISIONS #20/#26**, same construction, symmetrical and never shrinking |
| 15 | Stratum reporting and the sub-cell suppression rule | DECIDED | **Regime is reported as block *composition*, not as arms** (a regime cell crossed with a block is far below any floor at ~40 nights a block), with the **coarse `tape_sign_t` reweighting (B4) blocking** §8 clause 7. A cell with fewer than **20 measured** contributing nights is SUPPRESSED (counts only). **Suppression restricts affirmative reporting only: it never removes a blocker** — B4's reweighted contrast, clause 5's persistence, clause 8's `C_t` and bull-only sensitivities and clause 9's CUSUM run at whatever count they have, and a suppressed cell can still block a CONFIRMED. No suppression list is fixed from an *expectation*: §6's note that `bearish` / `neutral` / `risk_off` appeared on zero of 48 measured nights is context, and the rule is a measured count at the decision pass. | **DP-21** (20 per reported cell); rule 7; **Q027 DECISIONS #10 + Correction 2** and **Q023 DECISIONS #9**, stated there in the same words; **DP-45** |

## Corrections to silent choices

**Fourteen.** Corrections 1–4 came from `decide`; **5–14 are the `record` pass**, and they are what
branch (ii) requires the file to say. The Registrar applies all fourteen at `apply` with the rest of
this file. Everything else was checked against the policy and already matches (list at the end of this
section). **No correction anywhere weakens a floor, an MPE, a gate or a clause; every date moves out.**

1. **§5.1 — the series-B "nothing changes" threshold is 0.671 and must be 0.6723.** The draft derives
   it from the *total* (100 contributing nights over the registered 149 sessions = 0.671), but the
   floors are **per block, not per window**: `W1 ∪ W2` is sessions 1..119 and must carry **80**, which
   needs **80 / 119 = 0.6723**/elapsed session, while `W3`'s 20 over 30 sessions needs only 0.6667. A
   rate of 0.6715 clears the draft's test and delivers **79.9** nights across `W1 ∪ W2` — a floor
   failure dressed as a pass. **Must read:** branch (i) of item 8 fires at **≥ 0.6723 contributing
   nights per elapsed session**, and the window end is recomputed at `record` as the **later** of the
   two series' floor dates at their **own measured rates**, moving **out only** (DP-21, DP-43, DP-45).
2. **§5.3 R1 — "not blocking for the lock" is wrong and must read "blocking for the lock".** The
   lock-or-DEFER *gate* is indeed cleared by series A's measured rate, and the draft is right about
   that. But **DP-43 settles an arm's demotion at lock and never afterwards**, and §5.1's own demotion
   rule, §7's `m`, §2.3's block dates and §5.2's whole schedule all turn on a number that has never
   been measured on this desk — every prior published-pick exposure count (Q019 / Q022 / Q023) uses a
   weaker contributing-night rule than §2.5's. **Must read:** R1 is **blocking for lock**; Q031 does
   not lock until R1 is in and §5.1 / §5.2 / §7 are recomputed from it, out only; it is **not** a
   lock-or-DEFER gate for the question as a whole, whose three branches are fixed in item 8 above.
3. **§5.1 — the 0.45 inequality is the ceiling's solution at the actual lock date, not a constant.**
   **Must read:** the lock-or-DEFER test is 100 contributing nights divided by the elapsed sessions
   still admissible under DP-43's 12-month ceiling **solved at the actual lock date and rounded up**
   — at a 2026-09-14 lock, ≈ 224 sessions and **≥ 0.45** — and it is **re-solved at `record` and again
   if the lock date moves** (the Q027 Correction 5 form, now in its second question).
4. **§2.3 — the projected-contributing-nights column is series A's only, and must be labelled as
   such.** The table applies 0.6761 to all three blocks for both series; that rate is measured on
   Q027's all-candidates funnel and is series A's. **Must read:** the column is headed "series A
   (measured 0.6761)", a second column for series B is written at `record` from R1's measured rate,
   and each block's floor is checked against **both** series separately — §2.5 already says the two
   series have their own contributing-night sets and their own floors, and the projection table must
   not quietly pool them. **At `record` this is discharged by Correction 5's two-column table.**

*Corrections 1–4 above were written at `decide` and stand as written; 1, 3 and 4 are consumed by the
`record` corrections below, which carry their arithmetic through. Correction 2 is discharged: R1 was
treated as blocking, and Q031 did not lock until it landed.*

5. **§2.3 — the block table is re-cut on the 153-session window, with one projection column per
   series.** **Must read:** `W1` = sessions **1–61**, 2026-09-15..2026-12-09, reference; `W2` =
   **62–122**, 2026-12-10..2027-03-10, test; `W3` = **123–153**, 2027-03-11..2027-04-23, persistence
   holdout — the registered 40/40/20 proportions re-applied to the longer window and the session
   indices recomputed, exactly as §2.3 registers for this case, with the cuts rounded
   (0.4 × 153 = 61.2 → 61; 0.8 × 153 = 122.4 → 122). Projected contributing nights, **two columns, never
   pooled**: series A at the measured 0.6761 → **41.2 / 41.2 / 21.0** (`W1 ∪ W2` = 82.5); series B at
   the measured 0.6620 → **40.4 / 40.4 / 20.5** (`W1 ∪ W2` = 80.8). Every cell clears DP-21's 20, and
   `W1 ∪ W2` clears 80 for both series, so **no arm is demoted (DP-43) and `m = 2` stands** (§7).
6. **§5.1 — the series-B row is measured, and the demotion rule is spent.** **Must read:** contributing
   nights per elapsed session, series B under §2.5's registered rule = **0.6620 (47/71)**, source
   `research/reports/STEWARD_Q031_exposure.md` (a), measured on `manifest_v001` + `manifest_prices_v001`
   against `exclusions_v003.json`, counts only. The paragraph that reads as a live conditional
   ("If R1 measures … at or above 0.671/session, nothing changes…") is rewritten in the **past tense**
   as the branch that fired: 0.6620 < 0.6723, so the **window end moved out for both series** to
   session 153, `m = 2`, **P2 is not demoted**, and no floor was reduced. The stricter
   ≥ 3-picks / ≥ 5-controls rule is recorded as **measured to cost nothing** on the 48 matured nights
   (pool depth min 37 / median 54 / max 60; the single non-contributing night, 2026-06-02, has zero
   valid picks under every form of the rule) — a measured fact, **not** a reason the rule could have
   been relaxed.
7. **§5.2 — the window, the decision date, the extension and the hard stop.** **Must read:** window
   **pick nights 2026-09-15 .. 2027-04-23 inclusive = 153 elapsed sessions**; **decision date Monday
   2027-06-07**; single DP-13 extension to pick nights **.. 2027-06-07** (session **183**), decided
   **Monday 2027-07-19**, which is also the **hard stop**, then DEFERRED. The extension's own block
   re-cut, printed now so it is fixed blind: `W1` 1–73 (2026-09-15..2026-12-28), `W2` 74–146
   (2026-12-29..2027-04-14), `W3` 147–183 (2027-04-15..2027-06-07).
8. **§5.2 — the decision-date arithmetic paragraph, rewritten with the holiday skip shown.**
   **Must read:** 2027-04-23 **+ 20 sessions maturity = 2027-05-21**; **+ one calendar week freeze
   margin = 2027-05-28**; first Monday on or after = **2027-05-31, which is Memorial Day and a listed
   market holiday**, so the decision date is the next Monday, **2027-06-07** — **8.7 months (266 days)
   from the lock**, inside DP-43's 12-month ceiling (2027-09-14) by 3.3 months. Extension: session 183
   = 2027-06-07, + 20 sessions = **2027-07-07** (2027-07-05 is the observed Independence Day holiday;
   at a 07-06 reading the Monday is unchanged), + one week = 2027-07-14, first Monday on or after =
   **Monday 2027-07-19** — 10.1 months from the lock, inside the ceiling.
9. **§5.2 — the floor table is per series, and the binding floor is the slower series'.**
   **Must read:** floor A (≥ 80 across `W1 ∪ W2`, DP-21, per primary) binds at session **121**
   (2027-03-09) for series B and **119** (2027-03-05) for series A; floor B (≥ 20 in `W3`, DP-21's cell
   floor) is **the binding floor and sets the window end at session 153** once the two are solved
   **jointly against one set of 40/40/20 cuts** — which is why 153 and not 152 (at 152 the cuts give
   `W3` = 30 sessions → 19.9 series-B nights, short) and not the 121 + 31 = 152 sum of independent
   floor dates; floor C (DP-24, ≥ 30 post-lock nights) lands at session **46** (2026-11-17) for series
   B and **45** for series A and is **non-binding**, satisfied by construction.
10. **§5.2 — the holiday list is extended, since the record pass used two dates it did not carry.**
    **Must read:** …, 2027-05-31 (Memorial Day — the reason the initial decision Monday is 06-07 and
    not 05-31), 2027-06-18 (Juneteenth observed), **2027-07-05 (Independence Day observed)** and
    **2027-09-06 (Labor Day — used only in solving the DP-43 ceiling)**. The Steward re-confirms every
    date session by session when the freeze is built, and **a correction may move a date out, never in**.
11. **§5.1 — the lock-or-DEFER gate, re-solved at the actual lock date (Correction 3's rule, applied).**
    **Must read:** solved at the **2026-09-14** lock against the 2027-09-14 ceiling, the last admissible
    decision Monday is **2027-09-13**, which admits a last window end of **2027-08-06 = session 225**
    (2027-08-06 + 20 sessions = 2027-09-03; + one week = 2027-09-10; first Monday = 2027-09-13). At
    S = 225 the 40/40/20 cuts give `W1 ∪ W2` = 180 and `W3` = 45, so the gate is
    max(80/180, 20/45) = 0.4445 → **≥ 0.45 contributing nights per elapsed session, rounded up** — the
    same 0.45 the draft named, now derived **per block** rather than as 100/224. **CLEARED for both
    series: series A 0.6761 (clear by 52%), series B 0.6620 (clear by 49%).** Below that line Q031
    would have gone to `research/questions/DEFERRED.md` unregistered.
12. **§5.3 R1 — closed, with its source named.** **Must read:** R1 is **satisfied** by
    `research/reports/STEWARD_Q031_exposure.md` (2026-09-14, counts only, frozen data, no live query —
    DP-50(c)), and the exposure basis table in §5.1 cites it for series B exactly as it cites
    `STEWARD_Q027_exposure.md` for series A. **R2 remains open** and is due before 2027-06-07.
13. **§5.3 R2 and the manifest prose in the header — every successor-freeze date moves out.**
    **Must read:** the successor selection and price freezes cover pick nights
    **2026-09-15 .. 2027-04-23** with daily bars through **2027-05-21** (session t+20 of the last
    included pick night) and ≥ 60 prior sessions before 2026-09-15, delivered before **Monday
    2027-06-07**; the second pair, **only if** the single DP-13 extension fires, covers pick nights
    **.. 2027-06-07** with bars through **2027-07-07**, delivered before **Monday 2027-07-19**, built
    then and not before. The "superset of Q027's R2" sentence now reads **window extended from
    2027-03-05 to 2027-04-23**. The six scope requirements are unchanged.
14. **§9, §5.2 and §10 — the dates that depend on the decision date, each moved out by the same amount.**
    **Must read:** (a) **§9's DP-50(b) flag-off constraint runs until 2027-06-07** (2027-07-19 if the
    extension fires), which extends Q027's and Q029's 2027-04-12 / 2027-05-24 constraint by about
    **eight** weeks, not six — and it is still the tightest such constraint on the board, for the reason
    §9 already gives. (b) **`eval.py`'s commit deadline stays 2027-03-08**, deliberately **not** moved
    out to the new `W2`/`W3` boundary of 2027-03-11: the deadline exists so the script is written before
    Q027 and Q029 print this question's own `S^A` series on 2027-04-12, and the **earlier** date is the
    stricter one (DP-45). It is now a fixed calendar date, no longer described as a block boundary.
    (c) Every "149 sessions" in §1, §5.2, §8's STABLE sentence and §10 threats 1 and 6 becomes
    **153 sessions**; §10 threat 6's "six weeks before Q031 decides" becomes **about eight weeks**, and
    its claim that Q027/Q029 print `W1 ∪ W2` is corrected to **all but the final three sessions of
    `W1 ∪ W2`** (Q027's window ends 2027-03-05; `W2` now ends 2027-03-10) — which makes the threat
    slightly *smaller* than drafted, and is recorded rather than quietly enjoyed.

**Sub-cell check at the final window (DP-43's last clause), answered rather than skipped.** No
**arm** and no **primary** projects below 20 contributing nights (Correction 5), so nothing is demoted.
The §4.3 **fine** strata are a different matter and were already handled at `decide` (item 15): over
the 48 measured nights `bearish` / `neutral` / `risk_off` appeared **zero** times and five of six
`tape_t` cells projected below 20 over a longer stretch than one block, so most fine cells will be
**SUPPRESSED** at the decision pass — on **measured** counts, never on this projection. Suppression
restricts affirmative reporting only: **B4's coarse two-cell `tape_sign_t` reweighting stays blocking**
(§8 clause 7) and runs at whatever count it has, as do clauses 5, 8 and 9. No blocker is removed and
no verdict becomes easier.

Checked and **not** corrections — each already matches the policy: entry the **session t+1
regular-session open** for both series and every control alike, with **DP-11 correctly not fired**
(nothing here is a position already held) and the `C_t` version a blocking sensitivity that never
decides (**DP-03(b)**, **DP-42**); **L3 on the DP-09 20-session clock** with Q006's 40-session
version printed descriptively (**DP-09**); "elite" = `overall_score ≥ 90` in the §4.3 panel
(**DP-42**); a target already through the entry scored **not a hit** with the row kept in the
denominator (**DP-26**, rule 5); **no stop assumed anywhere**, counter-direction touches reported and
never used as exits, **DP-27** not reachable (no hourly bar is used) and **DP-30** not engaged
(**DP-02**); published = **`qualified IS TRUE AND selected_rank IS NOT NULL`**, dark-lane rows out of
the published slate and into the control pool only (**DP-28**); floors read as **80 contributing
nights per primary endpoint and 20 per reported cell**, the stricter reading, never lowered
(**DP-21**); **≥ 30 contributing nights after the lock commit**, satisfied by construction, so
**DP-31 correctly does not apply** and no successor replication question is owed (**DP-24**); one
automatic extension of +30 sessions then DEFERRED, fired on `eval.py`'s **measured** counts, with a
floor shortfall never an INCONCLUSIVE verdict (**DP-13**); window entirely after the 2026-06-01
catalyst fix, so no **DP-06** split falls inside it, and the sealed panel split at 2026-07-06
(**DP-06**); successor freezes covering **every candidate symbol, published and unpublished**
(**DP-23**); **two CIs per primary** with the episode at gaps ≤ 10 sessions and the
CI-2-includes-zero case INCONCLUSIVE rather than CONFIRMED (**DP-51**, §8 clause 4); registrar
conventions fixed before any outcome exists — the 40/40/20 block proportions, the 10-session block
length, seed 20260914, the `[0.25, 10]` ATR validity bound, the ≥ 3-picks / ≥ 5-controls rule, the
coarse `tape_sign_t` cut (**DP-26**), none promotable at the decision pass; no MPE anywhere in
session units, the τ̂ magnitude and sessions-to-touch descriptive (**DP-44**, the Q027 Correction 1
trap avoided); the exposure count taken from the **pinned freeze** and never a live query
(**DP-50(c)**); every number **NON_QUOTABLE** (rule 12) and nothing subscriber-facing before
PROSPECTIVELY_CONFIRMED (rule 10); the attribution limb carrying no MPE, no q and no verdict so
Q029's layer endpoints stay its own (**DP-29**, rule 8); and **no rule-14 exception requested or
needed** (**DP-05** untouched, **DP-41** respected).

## Defaulted on Haci's behalf

- #5 Lock now vs wait for Q006/Q027 — chose **lock now, prospectively, carrying the
  `NO_EDGE_TO_DECAY` precondition**; not taken: wait for the level verdicts — costs a year, shapes
  this design — DP-43. Overturn = successor question.
- #6 Window start — chose **prospective-only, pick nights ≥ 2026-09-15, sealed stretch as a labelled
  panel**; not taken: the sealed stretch as `W1` — decides now, not blind — DP-43. Overturn =
  successor question.
- #7 Window end and decision date — chose **window end 2027-04-23 (153 sessions), decision Monday
  2027-06-07** (extension .. 2027-06-07 decided 2027-07-19, then DEFERRED); not taken: the 0.9577
  eligible-night proxy — decides ≈ 2027-03-29 — DP-43. Overturn = successor question.
  *(Final at `record` on R1's measured 0.6620: two weeks later than the provisional 2027-05-24, and
  out is the only direction it could move.)*

**Three items, and all three are the same cost: waiting, and a particular kind of risk inside it.**
Q031 asks Haci to wait **8.7 months** for a question that can come back `NO_EDGE_TO_DECAY` — if Q006
(2026-10-05) or Q027 (2027-04-12) finds no edge, the corresponding series has nothing to lose and
clause 1 fires. That risk is real, it is written into §10 threat 2, and it was accepted rather than
avoided, because the alternative is worse in kind and not merely in degree: the nights cannot be
accrued retroactively, so waiting for the level verdicts would cost the year *and* let those verdicts
choose these blocks and MPEs. The tempting shortcut is written down so he can see it: 100% of the
nights old enough to test converted to contributing in Q027's measurement, so the 0.9577 eligible-night
rate is not a fantasy and would decide this question around 2027-03-29 — eight weeks sooner. It was
refused because it extrapolates past the price freeze's own forward-bar horizon, and the desk does not
buy eight weeks with a number it has not measured (DP-45). Item 7's dates may still move **out** at
`record` when R1 lands; they can never move in. Nothing else was defaulted: items 1–4 and 10–15 each
met a DECIDE ground, and none of them is a question about how he trades — the level, the lane, the
clock, the entry basis and "elite = 90" all come from DP-42 / DP-09 as already locked in Q002–Q029,
and the one MPE that is not a DP number is **his own**, from H3. No floor, arm, MPE, gate or clause
was weakened anywhere in this file; Corrections 1–4 each tighten one.

## Routed requests

### data-steward — R1 (counts only) — **SATISFIED 2026-09-14, CLOSED**

**Answer received:** `research/reports/STEWARD_Q031_exposure.md` — N = 71 elapsed sessions, 68
non-excluded, 48 matured; (a) series B **47/71 = 0.6620**/session under the registered rule and
identically under both weaker forms (pool depth min 37, so the control floors never bind; the only
binding night is 2026-06-02 with zero valid picks); (b) pool depth min 37 / median 54 / max 60, no
night below 10 or 5; (c) **35 invalid targets of 383 published rows** (8 no `lane_plans`, 2 wrong-side,
19 split-scale, 6 outside [0.25, 10] ATR), reconciling to 348 valid; (d) valid picks per night min 0
(min 4 excluding 2026-06-02), median 8, max 10; (e) series A **RECONFIRMED bit-for-bit at 48/71 =
0.6761**, **47 nights contributing to both series**, no DP-50(a) disagreement; (f) commit sweep since
`fa70688` **NONE** (`HEAD` `d19c9a9`), **no v1.7 promotion date** inside 2026-09-15..2027-07-19,
stated as an absence of a schedule and to be re-swept at every future freeze (R2(vi), item 13).
**Branch (ii) fired; the settlement is item 8 and Corrections 5–14.** Original request, for the record:

Q031 (is the SAS edge decaying, or is a weak stretch normal variation — PREREG §5.3 request R1) needs
a **counts-only** exposure measurement on the **frozen** data — `research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json` against `research/data/exclusions_v003.json`, plus read-only
`git log` / `git show` in the platform repo — and **never a live query** (DP-50(c)). It is **blocking
for the lock**: Q031 registers **two** primaries, one per night series, and DP-43 requires an arm's
demotion to descriptive to be settled **at lock and never afterwards**, so the window end, the
decision date and whether `m = 2` or `m = 1` all turn on the number you return. **No outcome of any
kind:** no touch, no first-touch date, no return, no excursion, no `outcome_*` column, no
`sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`, and no score-versus-outcome cross-tab
of any shape; forward bars may be read **only** to establish that a bar exists (gradeability
accounting), never for a value. Period: pick nights **2026-06-01..2026-09-10**; **denominator for
every rate = elapsed sessions** (calendar sessions minus holidays, exclusions *not* pre-removed — the
Q019 / Q022 / Q023 / Q027 convention, so the rates stay comparable across questions); nights in
`exclusions_v003` (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs`) and DP-04
late-`finished_at` nights removed from the numerator, plus the **`payload_disabled_runs`** signature
you identified for Q027 (every published row carrying `public_payload_json.analysis_status =
"disabled"` or no `lane_plans` object — 2026-04-01, 2026-05-01, 2026-06-02, 2026-07-02). Please return,
by month and for the period as a whole: **(a) series B's contributing-night rate under Q031 §2.5's
registered rule** — a non-excluded, matured night carrying **≥ 3 valid published picks** (DP-28's
predicate `qualified IS TRUE AND selected_rank IS NOT NULL`, after the invalid-target and split-scale
payload screens) **each of which carries ≥ 5 matched controls** from the §2.2 construction (the ten
nearest same-night **unpublished** candidates by Euclidean distance on `beta60` / `atr_pct` /
`runup20`, each feature standardized by the night's own cross-sectional median and MAD, with
replacement across picks within a night, ties by symbol ascending) — **and, printed beside it, the
same rate under two weaker forms: Q006's own rule (≥ 1 valid pick, ten nearest controls) and a
"drop-the-thin-pick" variant (a pick with < 5 controls excluded and counted, the night contributing if
≥ 3 valid picks survive)**, so the cost of the registered floor is visible in counts; **the registered
rule does not change on your answer — only the dates and the demotion do**; **(b) the matched-control
pool depth** — per night and per pick, how many unpublished candidates survive the ≥ 60-prior-bar and
gradeability screens, and how often fewer than 10, and fewer than 5, exist; **(c) the invalid-target
count** — published picks whose printed swing L3 (`lane_plans.swing_trading.targets[0]`) sits on the
wrong side of the pick-night close `C_p`, fails the split-scale payload screen, or implies
`d_p = dir × (L3 − C_p)/ATR` outside `[0.25, 10]` ATR — per night and overall, using desk-computed
ATR14 and `C_p` from `prices_daily_split` (never `atr_pct`, never `spot_close` — PI-003); **(d) the
valid-pick-per-night distribution** (min / median / max), so the ≥ 3 floor can be seen against it;
**(e) a re-confirmation of series A's contributing-night rate under Q031 §2.5** — which is Q027 §2.5
verbatim, so the expected answer is your own **0.6761/elapsed session (48/71)** from
`STEWARD_Q027_exposure.md`; please state it explicitly as confirmed-or-corrected rather than
assumed, since a disagreement between two counts of the same definition on the same freeze would
itself be a DP-50(a) finding, and please also give **the count of nights contributing to *both*
series**, which §2.5 needs and no report holds; **(f) a repeat of the DP-50(a)/(b) commit sweep**
since manifest SHA `fa70688` over `services/super_agent_select_scoring.py`,
`services/super_agent_select_models.py` and `services/sas_conviction_card.py` — the weights, the
timeframe multipliers, `qualification_threshold`, both ATR-elite caps, the GEX-missingness offset, the
scoring enable-flags, `publication_floor` / `bear_publish_threshold` and the lane-plan writer — each
with SHA and date in ET, **with an explicit answer even when it is "none"**, plus whether any scoring
workstream (the **v1.7** score named in `docs/SAS_SCORING_RESEARCH_PLAN.md`) is scheduled to ship
inside **2026-09-15..2027-07-12**, and a dated `DATA_NOTES.md` entry for any repair that rewrote
historical `sas_candidates` or price rows. **The call this request decides**, with all three branches
fixed before your counts are seen: series-B rate **≥ 0.6723 contributing nights per elapsed session**
(80 across the first 119 sessions — the per-block floor, not 100 over 149) → nothing changes, `m = 2`,
window 2026-09-15..2027-04-19, decision Monday 2027-05-24; **slower, but a window end at the later of
the two series' floor dates still decides inside DP-43's 12-month ceiling (2027-09-14)** → the window
end moves **out for both series** (one window, one freeze, the 40/40/20 block proportions re-applied
and the session indices recomputed) and every date is recomputed, **out only, never in**; **slower
still, so that no admissible window reaches 100 contributing nights for series B inside the ceiling**
→ **P2 is demoted to descriptive at the lock**, `m = 1`, the question runs on series A alone. No floor
is reduced in any branch. Please also state **the projected date each floor is first reached at each
measured rate** — 80 contributing nights across `W1 ∪ W2` per series (DP-21), 20 in `W3` per series
(DP-21's cell floor), 30 dated after the lock commit (DP-24, satisfied by construction) — taking the
window end as the **later** of the two series' projections, and flag any §4.3 sub-cell projecting
below 20 contributing nights at that date. Report to `research/reports/STEWARD_Q031_exposure.md`.

### data-steward — R2 (successor freezes) — **OPEN**, due before the decision date, **not** a blocker for lock

*Re-issued at `record` with final dates (branch (ii)): window end **2027-04-23**, bars through
**2027-05-21**, delivered before **Monday 2027-06-07**; extension pair, only if DP-13 fires, pick
nights through **2027-06-07** with bars through **2027-07-07**, delivered before **Monday 2027-07-19**.
Everything else below is unchanged; the dates in the body are superseded by these and by Correction 13.*

Q031 (PREREG §5.3 request R2, DP-23) needs successor freezes before its decision pass; **the dates
are now final and may only ever move out** (DP-43, DP-45). Please build and pin
a successor selection freeze (the same SQL and the same exclusion criteria as v001, over
**`sas_candidates` for every candidate row, published and unpublished**, plus `sas_runs` and
`market_regime_daily`) and a successor price freeze (the same Alpaca queries over `prices_daily_split`
and `prices_daily_raw`), covering pick nights **2026-09-15 .. 2027-04-23** with daily bars through
**2027-05-21** (session t+20 of the last included pick night) and **≥ 60 prior sessions before
2026-09-15**, delivered before **Monday 2027-06-07**; and — only if the single DP-13 extension fires —
a second pair covering pick nights through **2027-06-07** with daily bars through **2027-07-07**, due
before **Monday 2027-07-19**, built then and not before. **This freeze is a superset of Q027's R2**
(identical population, window extended from 2027-03-05 to 2027-04-23), so please build it **once** and
serve both questions from it. Six scope requirements, none optional: **(i)** the daily symbol list
covers **every candidate symbol on every in-window night, published and unpublished** — series A's
whole population and series B's control pool — never assumed from an earlier freeze's symbol list;
**(ii)** `public_payload_json` lane plans are required for published rows (series A's common distance
`d*_t` and series B's own printed L3 both read them); **(iii)** **no hourly bars are required** by any
endpoint — please say so explicitly rather than building them; **(iv)** an **add-only successor
exclusions file** on the identical **four** criteria (`manual_runs`, `non_session_runs`,
`uncorroborated_publication_runs`, `payload_disabled_runs`), which may add post-2026-09-10 nights and
may never remove a night from a v003 list, with its header stating whether the
`analysis_status = "disabled"` / no-`lane_plans` signature is still present after 2026-09-10 and
whether it is still a first-published-night-of-the-month pattern — if it has stopped, please say so
explicitly rather than silently returning an empty list; **(v)** rows whose bars are missing are
**excluded and counted, never back-filled or imputed**; **(vi)** where a successor freeze overlaps an
earlier one on `sas_candidates`, the rows are compared and any disagreement in `overall_score`,
`conflict_penalty` or `dominant_direction` is a **loud failure** — for a decay question a repair that
rewrote a score is indistinguishable from decay itself (DP-50(a)), so please repeat R1(f)'s commit
sweep for the period between freezes with a dated `DATA_NOTES.md` entry for any repair that rewrites
historical rows, and report explicitly **even when the answer is "none"** whether any weights,
timeframe-multiplier, `qualification_threshold`, ATR-elite-cap, GEX-offset or scoring enable-flag
change — including any **v1.7** promotion — shipped **inside** the window (DECISIONS item 13 cuts the
window at such a ship date, out and never in). Please re-confirm every §5.2 and §2.3 date **session by
session from the trading calendar** when the freeze is built, including the **final** block boundaries
(session **61 = 2026-12-09**, **122 = 2027-03-10**, **153 = 2027-04-23**, and on the extension path
**73 = 2026-12-28**, **146 = 2027-04-14**, **183 = 2027-06-07**); the holiday list used here is
2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, 2027-06-18,
**2027-07-05** and **2027-09-06** — please confirm the last two, since 2027-07-05 sets the extension
path's t+20 date and 2027-09-06 was used to solve DP-43's ceiling. A correction to
any date may move it **out, never in**.

## Schedule

**FINAL — settled at `record`, 2026-09-14, on `STEWARD_Q031_exposure.md` (R1).** Both rates are now
measured on the same freeze against the same exclusions: series A **0.6761/elapsed session (48/71,
reconfirmed bit-for-bit)**, series B **0.6620/elapsed session (47/71)**. The window end is the
**later** of the two series' floor dates, solved **jointly against one set of 40/40/20 cuts** rather
than as a sum of independent floor dates. Branch (ii) of item 8 fired, so every date below moved
**out** from the provisional schedule; none moved in, and no floor was reduced to shorten any of it.

decision_date: **2027-06-07** (Monday) · extension_date: **2027-07-19** (Monday — DP-13's single
automatic extension, window end 2027-06-07 = session 183; then DEFERRED, there is no second pass) ·
hard_stop: **2027-07-19** · rule: **exposure-driven**

- **window:** pick nights **2026-09-15 .. 2027-04-23** = **153 elapsed sessions**; extended window
  .. **2027-06-07** = 183 sessions · **extended: false**
- **blocks (fixed at lock by proportion, 40/40/20, session indices from the 153-session window):**
  `W1` sessions **1–61** (2026-09-15..2026-12-09, reference) · `W2` **62–122**
  (2026-12-10..2027-03-10, test) · `W3` **123–153** (2027-03-11..2027-04-23, persistence holdout).
  On the extension path the same proportions give `W1` **1–73** (..2026-12-28), `W2` **74–146**
  (..2027-04-14), `W3` **147–183** (..2027-06-07) — printed now so the extension's cuts are fixed
  blind. The blocks are never re-cut after any outcome is read.
- **projected contributing nights, per block, per series (never pooled):** series A at 0.6761 →
  `W1` 41.2 · `W2` 41.2 · `W3` 21.0 (`W1 ∪ W2` **82.5**, total 103.5); series B at 0.6620 →
  `W1` 40.4 · `W2` 40.4 · `W3` 20.5 (`W1 ∪ W2` **80.8**, total 101.3). **Every cell clears DP-21's
  20 and both series clear 80 across `W1 ∪ W2`**, so **no arm is demoted to descriptive (DP-43) and
  `m = 2` stands**.
- **binding floor:** B — ≥ 20 contributing nights in `W3` (DP-21's cell floor) for the **slower**
  series (B) at the window end, session 153. Floor A (≥ 80 across `W1 ∪ W2`, DP-21, per primary) binds
  at session **121** (2027-03-09) for series B and **119** (2027-03-05) for series A. Floor C (DP-24,
  ≥ 30 nights after the lock commit) lands at session **46** = 2026-11-17 (series B; 45 for series A)
  and is **non-binding**, satisfied by construction. Why 153 and not 152: at S = 152 the rounded cuts
  give `W3` = 30 sessions → 19.9 series-B nights, short of 20.
- **decision date arithmetic:** window end 2027-04-23 + **20 sessions maturity** = **2027-05-21**,
  + one calendar week freeze margin = **2027-05-28**, first Monday on or after = **2027-05-31**, which
  is **Memorial Day, a listed market holiday**, so the next Monday: **Monday 2027-06-07**. Extension:
  session 183 = 2027-06-07, + 20 sessions = **2027-07-07** (2027-07-05 is the observed Independence Day
  holiday; a 07-06 reading leaves the Monday unchanged), + one week = 2027-07-14, first Monday on or
  after = **Monday 2027-07-19**.
- **maturity:** 20 sessions, uniform across every row of both series.
- **gates, all on `eval.py`'s measured counts and none reduced:** ≥ 80 contributing nights across
  `W1 ∪ W2` **per series**; ≥ 20 in each of `W1`, `W2`, `W3` **per series**; ≥ 30 contributing nights
  dated after the lock commit; ≥ 30 eligible rows on every `S^A`-contributing night; ≥ 3 valid picks
  each with ≥ 5 matched controls on every `S^B`-contributing night; ≥ 20 measured contributing nights
  for any reported sub-cell.
- **ceiling:** DP-43's 12 months from a 2026-09-14 lock = **2027-09-14**. 2027-06-07 is **8.7 months**
  (266 days), 2027-07-19 is **10.1 months** (308 days) — both inside. **Not DEFERRED.**
- **lock-or-DEFER gate: CLEARED for BOTH series, re-solved at the actual lock date (Correction 3,
  discharged by Correction 11).** At a 2026-09-14 lock the last admissible decision Monday is
  2027-09-13, which admits a last window end of **session 225** (2027-08-06); its 40/40/20 cuts give
  `W1 ∪ W2` = 180 and `W3` = 45, so the gate is max(80/180, 20/45) = 0.4445 → **≥ 0.45 contributing
  nights per elapsed session, rounded up**. Measured: series A **0.6761** (clear by 52%), series B
  **0.6620** (clear by 49%). Re-solved again if the lock date moves.
- **`eval.py` deadline: committed no later than 2027-03-08, sha256 recorded, not touched afterwards** —
  deliberately **not** moved out to the new `W2`/`W3` boundary of 2027-03-11 (the earlier date is the
  stricter one, DP-45). This is a validity requirement, not housekeeping: Q027 and Q029 decide on
  2027-04-12 and will print this question's own `S^A` series for all but the final three sessions of
  `W1 ∪ W2`, about eight weeks before Q031 decides.
- **pin_at_decision: true** — every night carrying a verdict postdates every existing manifest, so
  DATASET_PINNED runs at the decision date on R2's successor freezes (DP-23).
- **open at lock:** R2 only (successor freezes, due before 2027-06-07; the extension pair only if
  DP-13 fires, due before 2027-07-19). R1 is closed.

## Standing rules added

_none._ Nothing here is Haci's word: items 5, 6 and 7 were **DEFAULTED** under DP-43, and a DEFAULTED
item adds **no** DP entry (DP-40) — the `record` pass settles the dates inside item 7 and adds none
either, for the same reason. Items 1–4 and 10–15 are applications of DP-02, DP-03, DP-04, DP-06,
DP-09, DP-13, DP-20, DP-21, DP-22, DP-23, DP-24, DP-25, DP-26, DP-28, DP-29, DP-42, DP-43, DP-44,
DP-45, DP-50, DP-51 and locked precedent (Q006, Q023, Q027, Q029).

## Standing rules proposed

- **The MPE for any per-night rank-correlation (IC) endpoint is 0.05 in Spearman-ρ units.** This is
  now its **second** question (Q027 DECISIONS #3 proposed it; Q031 applies it to a *difference* of
  ICs) and H-075's per-layer ICs will need it next. Deciding it three times invites three numbers.
  The entry should carry the tie caveat in the same sentence: an IC against a mostly-tied
  path-outcome rank is bounded well below 1, so the per-night touch base rate, the tied-block size
  and the **maximum attainable |ρ|** print beside any quoted ρ, and `IC_t` is **never rescaled**.
- **DP-20's larger-MPE clause is not applied to a difference of two already-control-adjusted means
  when doing so would make the hypothesis's own event unconfirmable.** Three questions have now
  reached this crossroads (Q029 E3, Q031 `D1ᴮ`, and Q023 in the opposite direction where 10.0 pp was
  correct). The general form: **double the MPE where the second difference adds variance without
  bounding the effect (a raw arm contrast of contrasts); keep 5.0 pp and register a stricter
  *blocking* clause where the endpoint is already control-adjusted and its structural maximum is the
  level itself.** An MPE that the hypothesis's own event cannot reach is a validity failure, not
  conservatism.
- **A contrast over time is registered on blocks fixed at lock; a change-point statistic is a
  blocking clause, never the primary.** A magnitude read at a data-chosen change point is biased away
  from zero by its own search and has no sample size knowable at lock, so rule 6's floors cannot be
  written for it. The change-point test keeps the role it can honestly fill — *is there a break, and
  where* — and `τ̂` prints in every branch. This will recur for every decay, drift or
  threshold-stability question (H-079, H-080, EN-017).
- **A decay question carries a `NO_EDGE_TO_DECAY` precondition, and it is not a null result.** Where
  a question tests whether a measured edge *moves*, the reference block's own level must clear the
  edge MPE before any stability or decay language is used; below it the endpoint is INCONCLUSIVE with
  that label, licenses nothing, and is routed to the question that owns the level. A flat line at
  zero is not the stability of an edge — and without this clause a `STABLE` verdict on a
  never-existent edge would read as reassurance.
- **Where one window serves two series with different contributing-night rules, the window end is the
  later of the two floor dates at their own measured rates, and a per-block floor is checked per
  block, never as a total over the window.** Q031's draft derived its series-B threshold from
  100 nights over 149 sessions and would have accepted a rate delivering 79.9 nights against an
  80-night floor (Correction 1). The arithmetic slip is small and the class is not: every multi-series
  or multi-arm question with proportional blocks can make it. **Strengthened at `record`, where the
  same class bit again one level down:** the window end is found by **solving the smallest window whose
  *rounded* proportional cuts satisfy every per-block floor for the slowest series simultaneously** —
  not by summing the series' independent floor dates, which gave 152 sessions here against a correct
  153, and not by dividing a total by a rate. The rounding of the block cuts is part of the constraint,
  not a presentation detail.
- **A decision date that lands on a market-holiday Monday moves to the next Monday, never to the
  Friday before.** DP-43's recipe says "the first Monday on or after"; Q027 §5.2 checked the holiday
  and Q031's initial date needed the skip (2027-05-31 Memorial Day → 2027-06-07). The general form
  belongs in DP-43 in one clause: the freeze margin is a minimum, so the only legal direction is out,
  and the holiday list used to solve both the decision date and the 12-month ceiling is named in the
  PREREG and re-confirmed by the Steward when the freeze is built.
- **A `record` pass states the ceiling's own solution at the actual lock date, in sessions, before it
  reports the gate.** Q031's gate (≥ 0.45/session) is the ceiling solved backwards — last admissible
  decision Monday → last admissible window end → rounded block cuts → the rate each block floor
  implies. Writing it as a bare constant invites the next question to copy 0.45 to a different lock
  date, a different maturity or a different block split, where it is wrong. This is now its second
  question (Q027 Correction 5, Q031 Corrections 3 and 11).
