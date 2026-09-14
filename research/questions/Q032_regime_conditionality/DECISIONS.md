# Q032 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous, DP-40..48) · Source: PREREG.md "Open decisions before
lock", 3 items (+ 13 decided, defaulted or routed here: the two routed requests named in §5.3, and
eleven the draft settles silently or leaves to `record`)

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

> **OUTCOME, 2026-09-14 (`record`): Q032 is DEFERRED.** The lock gate closed short on **limb (g)** —
> `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` absent, the SPY-from-2025-01-02 probe not attemptable, no
> pinned alternative (items 12 and 15; the H-074 / Q030 blocker). **Q032 does not lock; no schedule
> exists; every provisional date below is struck.** Read **"## Record — 2026-09-14"** and
> **"## Schedule"** before anything else in this file.
>
> **RE-ENTRY, 2026-09-14 (`record` addendum): the deferral trigger was met and Q032 is back at
> PREREG_DRAFT.** The DEFERRED outcome above is closed. Read **"## Record — 2026-09-14 (re-entry)"**
> (items 17–22) and the rewritten **"## Schedule"**, which supersede the struck block.

## The headline

**Q032 does not lock at `decide`, and the draft is right that R1 is blocking — but R1 is blocking for
two reasons, not one.** The Registrar names the first: no desk report has ever counted a bar-only tape
partition, so the rarer arm's exposure (floor B, the binding floor) rests on a placeholder borrowed
from a *different* variable. The second is found here: **§5.2 computes the decision date on 20
sessions of maturity while §2.4, §2.5 and §2.6 bind maturity at 40** — a contributing night requires
bars to t+40 — so every date in the draft is ~5 weeks early and the shared price freeze is ~4 weeks
short of the bars the registered population needs (Correction 1). Both move the schedule **out**, which
is the only direction DP-43 and DP-45 permit.

**The draft's own three items all go the Registrar's way. Two are DECIDED** (#1 the bar-only partition
as the single primary; #4 the pooled HOSTILE arm with the 80% naming guard) and **#12 (the SMA50-only
lock gate) is DEFAULTED**, joined by **two more the draft settles silently** — the prospective-only
window start and the whole window-end / decision-date block (R-3, settled at `record` on R1). **Eleven
items are DECIDED** on DP entries and locked precedent. **Two are ROUTED** to the Data Steward: **R1**
(counts only, **blocking for lock**) and **R2** (successor freezes, due at the decision date, blocking
nothing — DP-23). **Five corrections** are listed for `apply`; every one of them tightens a clause or
moves a date out, and none weakens anything.

**One limb is added to the lock gate that the draft left to the decision pass, and it is the Q030
precedent, not an invention.** §2.2's arm cannot be assigned without SPY daily bars back to 2025-01-02,
which exist in **no** pinned manifest and were last unobtainable because `ALPACA_API_KEY` /
`ALPACA_SECRET_KEY` were absent from the desk session (H-074 / Q030, DEFERRED 2026-09-14). Discovering
that at the 2027 decision pass would cost the whole window for nothing. **R1(g) probes it now**, and a
failed probe with no pinned alternative is a **DEFERRED-at-lock** ground, not an eight-month wait
(DP-45).

**Rule 14: no exception is requested and none is needed.** Every input is a 16:05 ET candidate field, a
SPY or symbol bar dated ≤ t, or the session t+1 open used **only** as an entry price; §6's table
declares each one and §6's `eval.py` clause freezes every eligibility, arm, match and stratum field
before any post-pick-night bar other than that open is loaded. **DP-05 is untouched and DP-41 is not
engaged.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Which of H-079's two regime definitions carries the primary (draft item 1) | DECIDED | **Option A — the bar-only §2.2 partition is the single primary, `m = 1`; the platform point-in-time label enters as C1, a mandatory blocking companion that can block a CONFIRMED and confirm nothing in any branch.** Not a preference: over the whole point-in-time-legal history of `market_regime_daily` the label takes exactly two values (49 `strongly_bullish` / 13 `bullish` of 65 sessions, `STEWARD_Q023_exposure.md` §3), so the only platform-label partition with exposure **is Q023's locked E1** on a ~95%-overlapping population. Option B would give the desk a second bite at a locked question's statistic and count it twice in F2. C1 is printed with its own night and tape-episode counts, its own legality-failure codes, the night-level agreement rate with the §2.2 arm, and the `effective_for_trading_date` variant beside it; it is corrected **jointly** with Q023's E1 and carries no q of its own. | **DP-29** (family bookkeeping — an overlapping hypothesis is merged or companioned, never counted twice); **Q023 §2.2 / E1 locked** (the identical arm definition, adopted here verbatim); rule 8 (forking paths); **DP-45** — A is the option under which the platform-label contrast can only ever *prevent* a positive |
| 2 | Binding maturity, and the clock the decision date is computed on | DECIDED | **40 sessions, as §2.4 / §2.5 / §2.6 register it — and §5.2's decision-date arithmetic is corrected to match (Correction 1).** A contributing night is a night matured to **t+40**; the primary's own clock stays L3 within **20** sessions from `X` (DP-09), and the 40-session companion is descriptive. Consequences, all applied: the decision date is **window end + 40 sessions + one calendar week, first Monday on or after** — at the registered 119-session window that is **Monday 2027-05-10**, not 2027-04-12; the successor price freeze carries daily bars through **t+40 of the last in-window pick night**, not t+20; §9's DP-50(b) flag-off dates move with it. The alternative — binding maturity at 20 and letting the 40-session companion be right-censored — was refused: it is the option that reaches a date sooner, it would make §2.6's own definition of a contributing night untrue, and §2.5 already forbids grading right-censoring as a non-touch. | ground 3 — one defensible answer: a floor counted on t+40-matured nights cannot be scheduled on t+20; **DP-43** (the decision date is the window end plus *the endpoint's* maturity window plus a one-week freeze margin); **DP-45** (never the earlier date); **DP-23** (a successor freeze is built to the horizon the registered population needs) |
| 3 | Which measured rate the schedule is built on, given a 40-session maturity and a freeze that ends 2026-09-10 | DECIDED | **The scheduling rate is `min(r₄₀, 0.6620)`**, where `r₄₀` = R1(a)'s contributing-night rate under §2.6's complete rule with **numerator and denominator counted over the same sub-period** — the maximal stretch of 2026-06-01..2026-09-10 whose nights can be graded to **t+40** on `manifest_prices_v001` (the Steward fixes its last date from the calendar) — and **0.6620** is the published-pick contributing rate Q031's R1 measured on the full 71-session denominator at t+20 maturity (47/71, `STEWARD_Q031_exposure.md` (a)). Every real loss mechanism stays in the denominator of `r₄₀` (exclusions, DP-04, null / non-monotone ladder, split-scale payload, < 3 valid controls, < 60 prior bars, > 25% ungradeable); **only** the freeze-horizon censoring is removed, and it is removed because it **cannot occur inside the registered window** — R2 delivers t+40 bars for every in-window night. Why this diverges from Q027 #8 / Q031 #7, stated rather than buried: their convention (numerator maturity-truncated, denominator the full span) deducted 28% for a 20-session endpoint; applied to a 40-session endpoint it deducts ~60% and would defer a testable question on an accounting artefact. The convention's *purpose* — never schedule on an extrapolation — is preserved by the cap: **no date is ever computed from a rate faster than the desk's own measured published-pick number**, and if R1 measures slower than 0.6620 the slower number is used. | **DP-43** (dates projected from the Steward's exposure count at the measured run-rate); **DP-45** (the min, never the faster rate; the cap is the binding half); ground 3 — a rate's numerator and denominator must cover the same period; `STEWARD_Q031_exposure.md` (a)/(b) (the ≥ 3-control clause never binds on this population: pool depth 37 / 54 / 60, so Q032's funnel differs from Q031's series B by the arm label alone) |
| 4 | How the pooled HOSTILE arm is protected from being one sub-state in disguise (draft item 3) | DECIDED | **Option A — the eight non-BENIGN cells are pooled, with the 80% composition guard of §8 clause 8 *renaming* the verdict.** If any single HOSTILE cell carries ≥ 80% of HOSTILE contributing nights the verdict is restated as being about that cell wherever it is reported, ledgered or quoted, and every §9 sentence names it. The 80% is fixed at lock and moves in neither direction; the nine-cell composition and the ordered UP ≥ MIXED ≥ DOWN read print in every branch. Option B (the HIGH-vol contrast and the not-UP contrast as two primaries) is refused because H-079 filed **one** primary and two thin arms would both fail DP-21's 20-night floor, reaching DEFERRED without either being testable — and because a second primary is a second chance at a positive, not a stricter test. | **DP-25** (the test stays the one that was proposed — one primary, H-079's own); **DP-21** (20 contributing nights per arm, not lowered to make B fit); **DP-26** (the partition is a Registrar convention fixed at lock, never derived from an outcome); **DP-45** (the guard can only restrict the claim; no alternative cut is fitted at the decision pass, and a different partition is a different question with its own id) |
| 5 | The MPE, and the two level lines | DECIDED | **MPE ±10.0 pp on `G`, H-079's own filed number, with DP-20's larger-MPE clause applied and the reason stated in §4.2** — `G` is a difference of differences (arm minus arm on an already control-adjusted rate) whose sign and size are **not** bounded by the level: `E_t` may be positive in one arm and negative in the other, so a conditionality effect can exceed the pooled level and a 5 pp bar would return INCONCLUSIVE by construction at ~80 nights. This is the Q023 E1 / Q012 P2 / Q018 P4 / Q022 E1 shape, and it is **not** the Q031 `D1ᴮ` shape (a decay bounded above by the level it decays from, where the doubling was correctly declined). **The level lines stay ±5.0 pp** (DP-20) in clauses 3 and 4 only. **No MPE and no level line is lowered at the decision pass in any branch**, including one where a CI excludes zero at 9 pp. | **DP-20** (+5.0 pp base, larger-MPE clause with a one-line reason); **DP-25** (±10.0 pp is the hypothesis's own number and is not re-united); **DP-44** (no invented unit; percentage points throughout, sessions-to-touch descriptive); **Q023 E1** locked precedent, same endpoint shape |
| 6 | Demotion — what happens if an arm is short | DECIDED | **Neither arm is demotable, as §5.1 registers.** `G` **is** the BENIGN − HOSTILE contrast, so an arm below 20 contributing nights leaves no endpoint at all: it is a floor failure — the single automatic DP-13 extension (+30 sessions), then **DEFERRED** — never a demotion to descriptive and **never an INCONCLUSIVE verdict**. DP-43's demotion clause is stated as having nothing to demote, and that is settled **at this lock**, not at the decision pass. The same handling covers the §8 clause 2 gate (≥ 5 gate-counting tape-episodes per arm). | **DP-43** (an arm's demotion is settled at lock and never afterwards; here it resolves to "not demotable"); **DP-13** (one extension, fired on `eval.py`'s measured counts, then DEFERRED); **DP-21**; **Q027 DECISIONS #10** (two primaries sharing one night set, same construction) |
| 7 | The sub-cell suppression list | DECIDED | **Fixed at this lock as §4.3 lists it, revised once at `record` from R1's measured counts on *this* question's own population, and then closed — and the revision may only move cells ONTO the list, never off it.** Suppression restricts **affirmative reporting only**: it never removes a blocker, and C1, the halves and the bull-only version are never on the list and block at whatever count they have. A cell suppressed at lock stays suppressed even if it clears 20 measured nights at the decision pass; a cell that is *not* suppressed still needs ≥ 20 **measured** contributing nights to print. The one-way rule is the deliberate divergence from Q027 #10 / Correction 8 (which moved cells both ways at `record`): Q032's suppressions are **structural** — PI-010's 2–3 elite picks a month against `publication_floor = 80.0`, H-062's bear grading, `regime_phase` and `best_timeframe` thinness — not density expectations R1 can overturn, and the desk does not add an affirmative cell to a prospective question after the drafting is done. | **DP-21** (20 per reported cell, no floor moved in either direction); **DP-45** (of two readings that differ only in strictness, the stricter); **Q023 DECISIONS #9** and **Q027 Correction 2** ("suppression never removes a blocker", in the same words) |
| 8 | Exclusions inside a window every night of which postdates every existing freeze | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** — verified the newest file on disk — with the **add-only successor exclusions file** issued with the successor selection freeze, on the identical **four** criteria (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10. The successor file may only **add** nights; no night is removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be; `exclusions_v003.json` is not edited (`research/data/` is not writable from here). Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. DP-04 applies mechanically on top. The fourth criterion is load-bearing here: on a `payload_disabled` night the published slate carries no `lane_plans`, so there is no `L3`, no `d_L3` and no eligible pick — the night is excluded whole rather than entering as a zero. | **DP-22** read as "one list, one set of criteria" (its "cite the newest file" clause presumes a sealed window; Q032's is entirely post-freeze); **Q027 DECISIONS #11 + `record` amendment**, **Q031 DECISIONS #12**, same construction; **DP-04** |
| 9 | A mid-window change to what "a published pick" or "its printed L3" is, and the DP-50(b) constraint that follows | DECIDED | A change to the SAS weights, the timeframe multipliers, `qualification_threshold`, the ATR-elite caps, the GEX offset, a scoring enable-flag, `publication_floor`, `bear_publish_threshold`, `max_output_cap`, `min_completeness` or the lane-plan writer — **including any promotion of v1.7** — **cuts the window at the ship date**: the post-ship segment becomes the question's window with the whole §5 schedule recomputed from it (**out, never in**, same single extension, same 12-month ceiling measured from the original lock), the pre-ship segment becomes a labelled descriptive panel entering no verdict, and if neither segment reaches the gates inside the ceiling Q032 is **DEFERRED**. `eval.py` prints the per-night `config_json` composition and **fails loudly** rather than silently excluding. Running the other way (DP-50(b)): every listed change is **flag-off until 2027-05-10** (2027-06-28 if the extension fires) — Correction 1's dates, ~4 weeks later than Q027's and Q029's identical clause — checked before any fix brief is written. A change to `services/market_regime/scorer.py` touches **C1 only** and is a DP-06 split for that companion, never for the primary; that is the practical payoff of a bar-only arm, and it is the one thing here a platform repair cannot move. | **DP-06** / **DP-50(a)** (a repair or config change splits a column into two features at the ship date); **DP-50(b)** (ship timing checked against in-flight questions, the PI-011 / Q010 pattern); **DP-50(c)** (the sweep runs on the pinned freeze and the read-only repo); **Q027 DECISIONS #12**, **Q031 #13** |
| 10 | The BH correction sets, and `m` | DECIDED | **`m = 1` within the question, fixed in every branch** — one primary, `G`; no second endpoint is added afterwards and the four blockers carry no q. Across **F2**, the set never falls below the **17** primaries standing at this lock: Q023 (2) + Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) + Q032 (1); Q005 stays excluded for the stated reason. Because `G` is built on Q006's `E_t`, it **additionally** carries the **F1** companion correction at **28**: Q006 (2) + Q024 (6) + Q025 (2) + Q029 (16) + Q031's `D1ᴮ` (1) + Q032's `G` (1) — cross-checked against Q031 #14's 27. **The larger of the two q's is the one quoted and the one §8 clause 9 reads.** C1 carries no q of its own and is reported as one non-independent pair with Q023's E1; neither may ever be read as confirming the other. | rule 8; **DP-29** (family by the primary endpoint's subject — calibration → F2 — with the F1 companion because the statistic is Q006's); **Q031 DECISIONS #14**, **Q027 #13**, **Q029 #20/#26** — stated symmetrically, never shrinking |
| 11 | When `eval.py` must be committed | DECIDED | **Written once (rule 9) and committed no later than Monday 2027-04-05, sha256 recorded, not touched afterwards** — one week before **Q027 and Q029 decide on 2027-04-12** on the same window, the same freeze, the same entry and the same 20-session clock, and Q031 decides after. Q027's decision pass prints control-adjusted touch statistics on Q032's own nights; a script written after that is a script written with the answer in view. The extension run uses the **byte-identical, unmodified** file. | rule 9 (deterministic script written once, no tuning while looking); rule 3 (pre-register before unsealing); **Q031 DECISIONS Schedule** (the same deadline logic, one question earlier) |
| 12 | How the lock gate handles SPY's missing 200-session history (draft item 2) | **DEFAULTED** | **Option A, with one limb added.** R1(b) measures the arm split under the **SMA50-only** trend variant and the gate is applied to it as the registered **one-sided bound** — the SMA50-only HOSTILE count is a **lower** bound on true HOSTILE exposure (adding `SMA50 > SMA200` can only move nights out of `UP`), the SMA50-only BENIGN count an **upper** bound — applied to the lower-bounded arm without adjustment and to the upper-bounded arm with that fact stated; **if the upper-bounded arm is the one that fails the gate, Q032 goes to DEFERRED rather than locking on a bound that runs the wrong way**. The registered window's own labels are unaffected: R2(i) delivers SPY from 2025-01-02, so every in-window night carries a true `SMA200` and a true 250-session tercile, and the partition is **never** re-specified to SMA50-only after the fact. **Added limb (the Q030 precedent):** R1(g) probes now whether that SPY history can be obtained at all — `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` present in the desk session and a bars-from-2025-01-02 coverage probe returning SPY — and **a failed probe with no pinned alternative is a DEFERRED-at-lock ground**, with the H-074 re-check trigger, rather than an eight-month wait for R2(i) to fail at the decision pass. | **DP-43** (a question locks when its floors are reachable inside the ceiling and defers when they are not; deferral is for a measured ground, never a preference); **DP-45** (the bound is used only in the direction that cannot flatter the arm the floors bind on; fail early rather than late); **Q030 / H-074** (the credentials limb of a lock gate, first admission ground 2026-09-14); not taken: defer Q032 now — costs the window for a probe not yet run |
| 13 | The window start: prospective-only, and the sealed stretch as a labelled panel | **DEFAULTED** | **Pick nights ≥ 2026-09-15 only** — the first session after the lock commit, so no night whose 16:05 ET run may precede the lock can enter. The sealed stretch (2026-06-01..2026-08-12) prints **once** as a labelled post-hoc panel, split at **2026-07-06** (`_enforce_ladder_monotonic`, the ship that changed the ladders `d_L3` is read from), computed from the successor freeze's extended SPY history so the arm is the registered one, entering **no verdict, no CI comparison, no half, no stratum test, no q and no §9 rule**, largely right-censored by its own freeze and printing its matured-night count beside every endpoint. The ground is not a convention here: **the weekly snapshots of 2026-09-10 and 2026-09-12 printed regime-stratified cells and are what put H-079 on the backlog**, so those nights can produce a description and not a test. | **DP-43**; rule 3; **Q027 DECISIONS #7** and **Q031 #6** verbatim (same population, same panel, same split date); not taken: read the sealed nights — decides now, but tests the data that proposed the hypothesis |
| 14 | Window end, decision date, extension, hard stop | **DEFAULTED (R-3)** — provisional; final at `record` on R1 | **Provisionally: window pick nights 2026-09-15 .. ≈ 2027-04-22 (≈ 151 elapsed sessions), decision ≈ Monday 2027-06-28, single DP-13 extension of +30 sessions to ≈ session 181 decided ≈ Monday 2027-08-09 = the hard stop, then DEFERRED.** The registered 119-session window does **not** survive Corrections 1–2: at item 3's capped rate of 0.6620 floor A (80 contributing nights) binds at session **121**, and floor B (20 contributing nights in the rarer arm) binds at ≈ **151** on §5.1's own placeholder arm share of 0.20 — so the window end moves **out**, as DP-43 requires when the planning rate is replaced by a measured one. The **method** is fixed here and is not re-argued with counts in view: window end = the **latest** of floors A (80 nights), B (20 rarer-arm nights), C (30 post-lock nights, satisfied by construction) and D (5 gate-counting tape-episodes per arm) at R1's measured rates; decision date = window end **+ 40 sessions maturity + one calendar week, first Monday on or after**, moved out again for a market holiday; DP-13's single extension = **+30 sessions** on the same arithmetic; > 12 months from the 2026-09-14 lock (2027-09-14) → **DEFERRED**. Every date may move **out** and never in. | **DP-43** (the window that reaches every floor at the measured rate, plus maturity and a one-week margin, first Monday on or after; +30-session extension; 12-month ceiling); **DP-13**; **DP-21**; **DP-24**; **DP-45** (out only; never the shorter window, never the faster rate); not taken: the registered 119-session window on the borrowed 0.9538 — decides 2027-05-10, below floor B |
| 15 | The exposure counts this question has never had | ROUTED → data-steward | waits on **R1** (counts only) — **BLOCKING FOR LOCK**, as §5.3 already says. It settles item 14's dates whole, and the lock-or-DEFER gate itself: **≥ 0.40** contributing nights per elapsed session, **≥ 0.10** rarer-arm contributing nights per elapsed session, **≥ 0.025** rarer-arm gate-counting tape-episodes per elapsed session (Correction 3's inequalities, re-solved at `record` from the calendar), **and** R1(g)'s SPY-history probe. All limbs clear → Q032 locks with §5.2 recomputed **out**; any limb short → **DEFERRED** with the measured counts and the re-check trigger named, not registered on a weaker partition. | — |
| 16 | Successor freezes | ROUTED → data-steward | waits on **R2** — the shared successor pair (selection: `sas_candidates` **every row, published and unpublished**, `sas_runs`, `market_regime_daily`; prices: daily bars for **every candidate symbol on every in-window night** plus hourly for published symbols), with Q032's **two** added scope requirements: **SPY split-adjusted daily bars from 2025-01-02**, and **daily bars through t+40 of the last in-window pick night** (Correction 1), plus the add-only successor exclusions file on the identical four criteria. Due before the decision date; **not a blocker for lock** (DP-23). Dates fixed at `record` from item 14. | — |

## Corrections to silent choices

**Five.** The Registrar applies them at `apply` with the rest of this file. Every one moves a date out
or tightens a clause; none weakens a floor, an arm, an MPE or a gate. Everything else was checked
against the policy and already matches (list at the end of this section).

1. **§5.2 (and §5.3 R2, §9) — the decision date is computed on 20 sessions of maturity, and the
   registered population needs 40.** §2.4 fixes binding maturity at 40 sessions, §2.5 excludes a night
   whose t+40 falls after the freeze's last date, and §2.6 defines a contributing night as one
   "matured to t+40" — but §5.2's arithmetic adds **20** sessions to the window end, and §5.3 R2 asks
   for daily bars through "session t+20 of the last included pick night". **Must read:** decision date
   = window end **+ 40 sessions + one calendar week, first Monday on or after** (at the registered
   119-session window: 2027-03-05 + 40 sessions = **2027-05-03**, + one week = **Monday 2027-05-10**,
   not 2027-04-12; on the extension path 2027-04-19 + 40 sessions = 2027-06-15, + one week = **Monday
   2027-06-28**, not 2027-05-24) — superseded in turn by item 14's recomputed window end; the
   successor **price** freeze carries daily bars through **t+40** of the last in-window pick night;
   and §9's DP-50(b) flag-off dates become **2027-05-10 / 2027-06-28**, or item 14's dates when they
   are fixed at `record`. (DP-43, DP-45, DP-23.)
2. **§5.1 / §5.2 — the borrowed 0.9538 and the "longer than this question's own floors require"
   sentence are both wrong on this funnel.** The borrow is defended as conservative because Q032's
   population is a superset of Q023's; that argument ignores maturity, the null- and non-monotone-ladder
   screens, the split-scale screen and the ≥ 3-control rule. The desk's own measured published-pick
   contributing rate is **0.6620** (47/71, `STEWARD_Q031_exposure.md` (a), at t+20 maturity), and item
   3 caps the scheduling rate there. **Must read:** floor A binds at **session 121**, not 84; floor B
   at ≈ **151 sessions** on §5.1's own 0.20 placeholder arm share, not 105; so the registered
   119-session window is **shorter than this question's floors require**, the sentence claiming the
   opposite is struck, and §5.2's table is rebuilt at `record` from R1's measured rates, **out only**.
   The freeze-sharing efficiency survives — Q031's own recomputed window already runs to 2027-04-23 —
   but it is a scheduling convenience and never a reason to end a window early (DP-43, DP-45).
3. **§5.3 R1 — the lock-or-DEFER inequalities are solved with 20 sessions of maturity.** The draft
   back-solves the 12-month ceiling (latest decision Monday 2027-09-13) through a one-week margin and
   **20** sessions to ≈ 225 admissible elapsed sessions, giving ≥ 0.36 / ≥ 0.09 / ≥ 0.023. At the
   registered 40-session maturity the same back-solve gives a window end of ≈ 2027-07-09, i.e.
   **≈ 205 admissible elapsed sessions**. **Must read:** contributing nights **≥ 0.40** per elapsed
   session; rarer-arm contributing nights **≥ 0.10**; rarer-arm gate-counting tape-episodes
   **≥ 0.025** — floors divided by the admissible span and rounded **up**, **re-solved at `record`
   from the trading calendar and again if the lock date moves** (the Q027 Correction 5 / Q031
   Correction 3 form, now in its third question).
4. **§4.3 — the per-level L1…L6 reads run on lane windows out to 60 sessions while maturity binds at
   40.** "each level's own lane window" includes the long lane's 60 sessions, which no in-window night
   will have. **Must read:** every descriptive read beyond t+40 (the long-lane L5 / L6 first-touch
   rates and their sessions-to-touch) prints its **matured-night count** beside it and its
   right-censored rows are **counted, never graded as non-touches** — §2.5's own rule, applied to the
   descriptive panel. No endpoint and no blocker depends on a bar after t+40.
5. **§5.3 R2 — "Q027's successor freeze pair, shared" understates the scope Q032 needs.** Q032's pair
   is a **superset** of the one Q027 and Q031 have requested: same population and same start, but SPY
   from **2025-01-02** and a bar horizon of **t+40** past a later window end. **Must read:** the
   Steward builds the selection freeze **once** and serves all three questions from it where the
   calendar permits, and Q032's price freeze is built to Q032's own horizon and delivered before
   Q032's own decision date; Q027's and Q031's earlier pins are unaffected and are **not** edited
   (DP-22, rule 3). The cross-freeze **SPY** comparison stays a loud failure (DP-50(a)) — SPY's
   history is this question's conditioning variable, and a vendor restatement would silently re-run
   the experiment.

Checked and **not** corrections — each already matches the policy: entry the **session t+1
regular-session open** for picks and matched controls alike, with **DP-11 correctly not fired**
(nothing here is a position already held) and the `C_t` basis a printed sensitivity that never decides
(**DP-03(b)**, **DP-42**); **L3 = `lane_plans.swing_trading.targets[0]` on the DP-09 20-session
clock**, with the platform's 40-session swing window descriptive (**DP-09**, **DP-42**); a level at or
through `X` at the t+1 open scored **not a hit** with the pick kept in the denominator and the
not-takeable count printed per arm (**DP-26**, rule 5); **no stop assumed anywhere**, counter-direction
touches and MAE / MFE reported and never used as exits, **DP-30** not engaged and **DP-27** not
reachable (no endpoint depends on an hourly bar) (**DP-02**); published = **`qualified IS TRUE AND
selected_rank IS NOT NULL`**, dark-lane rows never in the treatment arm and only in the control pool
(**DP-28**); the B2 control construction Q006 §3 verbatim, controls never adding to inferential n, a
pick with < 3 valid controls dropped and counted and never imputed (rule 6, rule 5); floors read as
**80 contributing nights per primary endpoint and 20 per arm and per reported cell**, the stricter
reading, never lowered (**DP-21**); **≥ 30 contributing nights after the lock commit**, satisfied by
construction, so **DP-31 correctly does not apply** and no successor replication question is owed
(**DP-24**); one automatic extension of +30 sessions then DEFERRED, fired on `eval.py`'s **measured**
counts, with a gate shortfall never an INCONCLUSIVE verdict (**DP-13**); window entirely after the
2026-06-01 catalyst fix, the 2026-07-06 ladder ship and the 2026-07-08 `publication_floor` ship, so no
**DP-06** / **DP-50(a)** split falls inside it, and the sealed panel split at 2026-07-06 (**DP-06**);
successor freezes covering **every candidate symbol, published and unpublished** (**DP-23**); **two
CIs per primary**, the tape-episode block bootstrap and the DP-51 symbol-episode bootstrap, with the
CI-2-includes-zero case **INCONCLUSIVE, never CONFIRMED**, and the three units given three names
(**DP-51**, §2.6, §8 clause 9); Registrar conventions fixed before any outcome exists — the SMA50 /
SMA200 / 20-session-vol cuts, the expanding-window terciles with the ≥ 250-session requirement, the
BENIGN definition, the 80% composition guard, the 10-session block length, seed 20260914, the
session-index half split, the 25%-ungradeable night rule (**DP-26**), none promotable at the decision
pass; no MPE anywhere in session or money units (**DP-44**); the exposure counts taken from the
**pinned freeze** and the read-only repo, never a live query (**DP-50(c)**); every number
**NON_QUOTABLE** on a 20- and 40-session basis (rule 12) and nothing subscriber-facing before
PROSPECTIVELY_CONFIRMED (rule 10); `uoa_symbol_daily.fwd_return_*` banned and no UOA table read
(FREEZE_v001 §5); `sas_selection_excursion` / `outcome_*` / `level_hit_*` never inputs; and **no
rule-14 exception requested or needed** (**DP-05** untouched, **DP-41** respected).

## Defaulted on Haci's behalf

- #12 SPY's missing 200-session history at the lock gate — chose **the SMA50-only one-sided bound,
  plus a credentials probe that defers now if the history is unobtainable**; not taken: defer Q032
  today — costs the window before probing — DP-43. Overturn = successor question.
- #13 Window start — chose **prospective-only, pick nights ≥ 2026-09-15, sealed stretch as a labelled
  panel**; not taken: use the sealed nights — decides now, not blind — DP-43. Overturn = successor
  question.
- #14 Window end and decision date — chose **the window that reaches every floor at R1's measured
  rates (provisionally ≈ 2027-04-22, decision ≈ Monday 2027-06-28)**; not taken: the registered
  119-session window on the borrowed rate — decides 2027-05-10, below floor B — DP-43. Overturn =
  successor question.

**Three items, and all three are the same cost: waiting, and one particular risk inside it.** Q032
asks Haci to wait roughly **nine and a half months** for a question whose most likely stopping point
is not its own result but a provisioning failure: §2.2's arm cannot be assigned without SPY daily bars
back to 2025-01-02, which sit in no pinned manifest, and the last attempt to fetch bars the desk did
not already hold ended in Q030's deferral for absent Alpaca credentials. That is why #12 pulls the
probe forward to the lock instead of leaving it at the decision pass — a DEFERRED today costs nothing,
a DEFERRED in June 2027 costs the window. The second cost is written down so he can see the tempting
shortcut: the draft's own dates (decide 2027-04-12, sharing Q027's freeze exactly) are **ten weeks
earlier** than what this file registers, and they are refused for two reasons that are arithmetic
rather than taste — a contributing night needs t+40 bars and the draft scheduled on t+20, and the
rarer arm's exposure was sized on a placeholder borrowed from a *different* variable. Nothing else was
defaulted: items 1–11 each met a DECIDE ground, and none of them is a question about how he trades —
the level, the lane, the clock, the entry basis and "elite = 90" all come from DP-09 / DP-42 as
already locked in Q002–Q031, and the one MPE that is not a DP number is **H-079's own**.

## Record — 2026-09-14 — branch fired: **DEFERRED**

Run: `record Q032`, 2026-09-14, decision-maker, autonomous (DP-40..48). Source:
`research/reports/STEWARD_Q032_exposure.md` (R1, counts only, read in full). No `results/` directory
exists, no `eval.py` was written, and **no outcome of any kind** — touch, first-touch date, return,
excursion, plan result or arm-versus-outcome relation — was read for Q032 at any point. The Steward's
report is counts only and reads a forward bar solely to establish that a bar exists.

**The branch that fired is item 12's / item 15's failing limb, and it is limb (g): the SPY-history
feasibility probe could not be attempted, because `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` are unset in
the desk session** (Steward (g); Rule 1 forbids looking for or requesting any other credential). Under
**PREREG §5.3 R1(g) / R2(i)** and **DECISIONS items 12 and 15**, a failed probe with **no pinned
alternative** is a **DEFERRED-at-lock** ground on its own, independent of every counted limb. It is the
same blocker, the same pair of variables and the same session as **Q030 / H-074** (DEFERRED 2026-09-14).
**Q032 does not lock.** The partition is **not** re-specified to SMA50-only (PREREG §5.3 R2(i), item 12):
that is a different arm chosen after the data existed, and it is a different question with its own id.

**The blocker is confirmed a second time, from the opposite direction, by the counts themselves.** Under
the **literal §2.2 rule** the contributing-night rate in this freeze is **0/71 in all three forms**:
`manifest_prices_v001` holds 153 SPY bars (2026-02-02..2026-09-10) and the expanding count of computable
rvol20 observations reaches **133** at the freeze's last date, so **no night in this or any freeze the
desk holds reaches the ≥ 250 prior SPY sessions** the volatility tercile requires — the first such
session is **never** (Steward (a), (c)). The registered arm cannot be legally assigned on any pinned
artefact. That is not evidence against H-079 and not a screening failure; it is the same missing SPY
history that limb (g) exists to probe, and it is what R2(i) was sized to fix.

**Item 15's remaining three limbs, measured on the SMA50-only registered bound only, and therefore
recorded for the re-check and for nothing else** (the bound is explicitly **not** §2.2-legal — item 12).
The Steward re-solved the thresholds from the trading calendar as Correction 3 requires and got
**0.39 / 0.097 / 0.0243** against the file's rounded-up **0.40 / 0.10 / 0.025**; the file's numbers are
the stricter and are the ones read here, and every limb below clears or fails identically on both.

| limb | floor (re-solved / as filed) | measured, SMA50-only proxy | strict §2.2 | read |
|---|---:|---:|---:|---|
| (a) contributing nights / elapsed session | 0.39 / **0.40** | **0.6620** (the item-3 cap binds: min(0.8710, 0.6620)) | 0.0000 | proxy clears; strict short |
| (b) rarer-arm (HOSTILE) contributing nights / session | 0.097 / **0.10** | **0.3099** (22 of 68 nights HOSTILE) | 0.0000 | proxy clears; strict short |
| (b) rarer-arm gate-counting episodes / session | 0.0243 / **0.025** | **0.0563** unmatured · **0.0141** t+40-matured | 0.0000 | proxy clears on the unmatured basis; **short on the t+40-matured basis** |
| (g) SPY-history feasibility probe | must succeed | — | — | **FAIL — credentials absent, probe not attempted** |

Three readings of that table are recorded so the re-check does not have to rediscover them, and none of
them changes today's branch:

1. **The episode limb is short on the basis this file's own item 2 requires.** A contributing night is a
   night matured to **t+40** (Correction 1), so the t+40-matured column is the consistent one, and on it
   the rarer-arm episode rate is **0.0141 < 0.0243** — below the floor. This is **not a second
   independent ground**: it is freeze-horizon censoring, because no night after **2026-07-15** can reach
   t+40 inside `manifest_prices_v001` (Steward (a) form (i)), and censoring that cannot occur inside the
   registered window is exactly what item 3's construction removes. It is recorded as a **measurement the
   re-check must make again on a freeze carrying t+40 bars**, not as exposure evidence.
2. **The rarer arm is much richer than §5.1's placeholder, so the binding floor would change.** Measured
   HOSTILE exposure is **0.3099/session** against the placeholder's 0.20 × 0.6620 ≈ **0.132**; at the
   measured rate floor **B** binds at ≈ 65 sessions and floor **D** at ≈ 89, both inside floor **A**'s
   ≈ 121 sessions at the capped 0.6620. **Floor A, not floor B, would bind** (Steward Re-check note).
   **No schedule is built on this and none is carried forward** — it is a proxy reading on a
   lower/upper-bounded arm, and item 14's method (window end = the latest of A, B, C, D at the measured
   rates; decision date = window end + 40 sessions + one week, first Monday on or after; out only) is
   re-run from scratch on a re-attempt, never inherited.
3. **C1 carries more independent information than §10 threat 2 assumed.** Night-level agreement between
   the proxy arm and the legal platform label is **49/63 = 77.8%**, with the HOSTILE nights split exactly
   **11 STRONG / 11 NOTSTRONG**; §2.3 legality fails on **5 of 68** nights, all on the `created_at`
   timestamp test, none on `unknown` / `insufficient` (Steward (d)). Item 1's disposition of C1 — blocking
   companion, corrected jointly with Q023's E1, confirming nothing — is unchanged by this and is **not**
   promoted to a second primary on the strength of it.

**Nothing else measured moves anything.** (e) **confirms** the control-pool depth (min 37 / median 53 /
max 60; 0 nights below 3) and the CTRA truncated-history signature (last bar 2026-05-06, 19 in-window
appearances, the 5 pre-2026-08-12 ones matching Q027 exactly) — a confirmation, not a correction, so
**no DP-50(a) finding**. (f) returns **NONE**: HEAD is unchanged at `d19c9a9`, no commit since `fa70688`
touches the scoring path, the lane-plan writer or `services/market_regime/scorer.py`, and **no v1.7
promotion is scheduled** — an absence of a schedule, to be re-checked at every future freeze, never
assumed clear permanently. The `publication_floor` / `bear_publish_threshold` config dates are already in
`DATA_NOTES.md` and gate publication, not scoring (item 9) — **no new `DATA_NOTES.md` entry is owed**.

**Item 7's suppression list is not revised.** The one permitted revision runs "at `record` from R1's
measured counts" *on a locked question*; Q032 does not lock, so the list stays exactly as §4.3 drafted
it. The Steward's (c) composition is a **six-cell** proxy (SMA200 exists nowhere in the freeze, so only
UP / NOTUP is observable) and cannot revise a nine-cell list in either direction; it is informational.
**Item 6 is likewise not exercised** — no arm is demoted, because there is no lock at which to demote it,
and a gate shortfall is **not** an INCONCLUSIVE verdict (item 6, DP-13). **No verdict of any kind is
produced: no NULL, no INCONCLUSIVE, no `G`, no C1 number.**

**DP-13 is not fired.** Its single automatic extension rescues a floor that is *marginal at a decision
date*; this question has no decision date and its blocker is provisioning, not accrual — waiting 30
sessions produces no SPY bars. **DP-43's 12-month ceiling is not the admission ground either** (the
proxy rates are comfortably inside it); this entry lands on `DEFERRED.md`'s **first** admission ground —
the objective cannot be measured with the artefacts the desk holds — exactly as Q030 did.

**The three DEFAULTED items stand as drafted and are not re-opened.** Item 12 is the reason this
deferral costs one afternoon instead of the nine and a half months the provisional schedule carried;
items 13 and 14 never take effect, because there is no window. Should the trigger below be met, Q032
resumes at **`@registrar apply Q032`** with this file binding, and **every date is recomputed from the
new lock date and never carried forward** (the Q020 / Q025 precedent) — items 13's window start and 14's
method apply to the new lock, Correction 3's inequalities are **re-solved** against the ceiling measured
from it, and dates may move **out only** (DP-43, DP-45).

## Routed requests

### data-steward — R1 (counts only) — **CLOSED 2026-09-14 — answered; limb (g) short**

**Answered in full by `research/reports/STEWARD_Q032_exposure.md` (2026-09-14).** Limbs (a)–(f) counted
and recorded above; **limb (g) FAILED — credentials absent, probe not attempted — and that is the
branch that fired.** No further Steward work is requested for Q032 while it is deferred. The request is
preserved below as issued.

Q032 (does the SAS selection edge exist only in identifiable tape states — PREREG §5.3 request R1)
needs a **counts-only** exposure measurement on the **frozen** data — `research/data/manifest_v001.json`
+ `research/data/manifest_prices_v001.json` against `research/data/exclusions_v003.json`, plus
read-only `git log` / `git show` in the platform repo — and **never a live query** (DP-50(c)). It is
**blocking for the lock**: no desk report has ever counted a bar-only tape partition, Q032's binding
floor is the **rarer arm's** 20 contributing nights, and §5.1's rarer-arm rate is a placeholder
borrowed from the platform's *label* — a different variable. **No outcome of any kind:** no touch, no
first-touch date, no return, no excursion, no `outcome_*` column, no `sas_selection_excursion`, no
`uoa_symbol_daily.fwd_return_*`, and no arm-versus-outcome cross-tab of any shape; forward bars may be
read **only** to establish that a bar exists (gradeability and maturity accounting), never for a
value. Period: pick nights **2026-06-01..2026-09-10** (DP-06's segment; the arm is a 16:05 property
with no outcome attached, so the widest legal span is used); **denominator for every rate = elapsed
sessions** (calendar sessions minus holidays, exclusions *not* pre-removed — the Q019 / Q022 / Q023 /
Q027 / Q031 convention), with nights in `exclusions_v003` and DP-04 late-`finished_at` nights removed
from the numerator, plus the `payload_disabled_runs` signature you identified for Q027 (2026-04-01,
2026-05-01, 2026-06-02, 2026-07-02). Please return, by month and for the period as a whole: **(a) the
§2.5 funnel and the contributing-night rate under §2.6's complete rule** — a non-excluded night
carrying a legal §2.2 arm label and **≥ 1 eligible published pick** (DP-28's predicate, after the
null-ladder, wrong-side / non-monotone, split-scale and ≥ 60-prior-bar screens) **with ≥ 3 valid
matched controls** — reported **three ways**: (i) the rate with numerator and denominator both
counted over the **maximal sub-period whose nights can be graded to t+40** on `manifest_prices_v001`
(please state that sub-period's last pick night, derived from the calendar), (ii) the same rule with
maturity evaluated at **t+20** for comparability with your own 0.6620 (47/71) in
`STEWARD_Q031_exposure.md`, and (iii) the full-denominator t+40 rate for the record; **the schedule
will be built on `min` of (i) and 0.6620** (DECISIONS item 3), so a rate faster than 0.6620 changes no
date; **(b) the §2.2 arm split under the SMA50-only trend variant** (`UP` iff `close_t > SMA50_t`,
`vol_t` by expanding-window terciles of 20-session annualised realised vol over every SPY session in
the freeze dated ≤ t): nights per arm over all elapsed sessions, **stating explicitly which arm is the
rarer one**, and **gate-counting tape-episodes per arm** (a maximal run of consecutive sessions
carrying the same arm label; an excluded or unlabelled session does **not** break a run; an episode
counts only if it contains ≥ 1 contributing night) with their length distributions and contributing
nights per episode — carrying with each count the bound direction that applies to it (SMA50-only
HOSTILE is a **lower** bound on true HOSTILE, SMA50-only BENIGN an **upper** bound on true BENIGN);
**(c) the nine-cell `trend_t` × `vol_t` composition** under the same variant, and **the first session
at which SPY has ≥ 250 prior sessions in the freeze** (the honest start of the tercile calibration);
**(d) the night-level agreement rate** between the SMA50-only arm and the §2.3 platform label
(`STRONG` iff `market_regime = 'strongly_bullish'` on the `v1.2` row with `trading_date = t`, legal
only if `market_regime <> 'unknown'`, `COALESCE(data_quality,'') <> 'insufficient'`,
`created_at::date = trading_date` **and** `created_at <= that night's own sas_runs.finished_at`), with
the legality-failure count by reason code — the direct read on how much independent information the
second regime definition carries (§10 threat 2); **(e) the matched-control pool depth and the CTRA
truncated-history scan** re-run on this population (your Q031 figures — min 37 / median 54 / max 60,
never below 5 — are expected to carry, but please state them as confirmed-or-corrected rather than
assumed, since a disagreement between two counts of the same definition on the same freeze would
itself be a DP-50(a) finding); **(f) the DP-50(a)/(b) commit sweep** since manifest SHA `fa70688` —
any change to the SAS weights, timeframe multipliers, `qualification_threshold`, `publication_floor`,
`bear_publish_threshold`, `max_output_cap`, `min_completeness`, the ATR-elite caps, the GEX offset,
the scoring enable-flags, the lane-plan writer, or `services/market_regime/scorer.py` (C1 only) —
**with an explicit answer even when it is "none"**, plus whether the **v1.7** workstream is scheduled
to ship inside 2026-09-15..2027-08-09; and **(g) a SPY-history feasibility probe, which is a limb of
the lock gate** — whether `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` are present in the desk session and
whether SPY split-adjusted daily bars **from 2025-01-02** can be retrieved (coverage and first/last
bar date only, no values needed beyond that); this is the Q030 / H-074 blocker, and §2.2's arm cannot
be assigned without those bars. **The call this request decides**, with every branch fixed before your
counts are seen: contributing nights **≥ 0.40** per elapsed session, rarer-arm contributing nights
**≥ 0.10**, rarer-arm gate-counting tape-episodes **≥ 0.025** — the floors (80 / 20 / 5) divided by
the **≈ 205** elapsed sessions still admissible under DP-43's 12-month ceiling at a 2026-09-14 lock
with **40** sessions of maturity, rounded up, and please **re-solve them from the trading calendar**
rather than taking my arithmetic — **and** limb (g) returning SPY back to 2025-01-02. All four clear →
**Q032 locks**, with the window end set to the **latest** of floor A (80 contributing nights), floor B
(20 rarer-arm contributing nights), floor C (30 post-lock nights, satisfied by construction) and floor
D (5 gate-counting tape-episodes per arm) at your measured rates, and every date moved **out** if
those rates are slower than §5.1's placeholders, never in. Any limb short → **Q032 goes to
`research/questions/DEFERRED.md`** with the measured counts and the re-check trigger "the Steward
measures ≥ 0.10 rarer-arm contributing nights per elapsed session over a trailing quarter" (or, for
limb (g), the H-074 credentials trigger), and it is **not** re-registered on a weaker partition — a
different partition is a different question with its own id. Please also state **the projected date
each floor is first reached** at each measured rate, on **40** sessions of maturity plus a one-week
freeze margin, and flag any §4.3 sub-cell projecting below 20 contributing nights at that date (the
suppression list may only gain cells at `record`, never lose them — DECISIONS item 7). Report to
`research/reports/STEWARD_Q032_exposure.md`.

### data-steward — R2 (successor freezes) — **WITHDRAWN 2026-09-14 (Q032's rider only), HELD pending the re-check trigger**

**Q032's additions to the shared successor pair are withdrawn and are not to be built:** the
**SPY-from-2025-01-02 history (i)** — which cannot be fetched without the credentials limb (g) just
failed on — and the **t+40 bar horizon (ii)** past Q032's own window end. **Q027's and Q031's own
requests and pins are unaffected, are not edited, and the shared selection freeze is built to their
horizons, not to Q032's** (rule 3, DP-22). Nothing else is asked of the Steward for Q032. The request
revives **with** Q032 if the trigger is met, and its dates are recomputed from the new lock date, never
inherited. It is preserved below as issued.

Q032 (PREREG §5.3 request R2, DP-23) needs successor freezes before its decision pass; **the dates
below are provisional until R1 lands and may only ever move out** (DP-43, DP-45). Please build and pin
a successor **selection** freeze (the same SQL and the same exclusion criteria as v001, over
`sas_candidates` for **every candidate row, published and unpublished**, plus `sas_runs` and
`market_regime_daily`) and a successor **price** freeze (`prices_daily_split`, `prices_daily_raw`,
`prices_hourly_raw`), covering pick nights **2026-09-15 .. the window end fixed at `record`**
(provisionally ≈ 2027-04-22) with **≥ 60 prior sessions before 2026-09-15**; and — only if the single
DP-13 extension fires — a second pair covering the +30-session extended window, built then and not
before. **This pair is a superset of the one already requested for Q027 and Q031** (identical
population and start, longer horizon), so please build the selection freeze **once** and serve all
three questions from it where the calendar permits; Q027's and Q031's own pins are unaffected and are
not edited. Seven scope requirements, none optional: **(i) SPY split-adjusted daily bars from
2025-01-02** through the freeze end — without them §2.2's `SMA200` and its 250-session volatility
tercile do not exist and **no arm can be assigned**; if the extended SPY history cannot be obtained
(the Q030 / H-074 provisioning blocker), **Q032 is DEFERRED on that ground** and the partition is
**never** re-specified to SMA50-only after the fact, because that is a different arm chosen after the
data existed; **(ii)** the daily bar horizon runs to **session t+40 of the last included pick night**
— not t+20 (DECISIONS Correction 1: Q032's contributing night is defined at t+40) — provisionally
daily bars through ≈ **2027-06-21**, delivered before the decision date; **(iii)** the daily symbol
list covers **every candidate symbol on every in-window night, published and unpublished**, with ≥ 60
prior sessions before 2026-09-15 (the matched controls need their closes, `beta60`, `atr_pct`,
`runup20` and forward bars), never assumed from an earlier freeze's symbol list; **(iv)** hourly bars
scoped to at least the published-pick symbols, for the descriptive entry audit only — **no endpoint
and no blocker depends on an hourly bar**; **(v)** `market_regime_daily` included, for C1 only, with
`created_at` preserved (§2.3's legality test is a timestamp test); **(vi)** an **add-only successor
exclusions file** applying the identical four criteria (`manual_runs`, `non_session_runs`,
`uncorroborated_publication_runs`, `payload_disabled_runs`) to post-2026-09-10 nights — it may add
nights and may never remove one from a v003 list, and its header should state whether the
`analysis_status = "disabled"` / no-`lane_plans` signature is still present and still a
first-published-night-of-the-month pattern, saying so explicitly rather than silently returning an
empty list; **(vii)** rows whose bars are missing are **excluded and counted, never back-filled or
imputed**, and R1(f)'s commit sweep is repeated for the period between the freezes with a dated
`DATA_NOTES.md` entry for any repair that rewrites historical rows and an explicit answer **even when
it is "none"**. **The DP-50(a) guard is load-bearing on SPY specifically:** where the successor freeze
overlaps an earlier one on SPY's daily bars, the rows are compared and `eval.py` **fails loudly** on
any disagreement — SPY's history is this question's conditioning variable, so a vendor restatement
would silently re-run the experiment. Please re-confirm every §5.2 date **session by session from the
trading calendar** when the freeze is built; the holiday list used here is 2026-11-26, 2026-12-25,
2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31 and 2027-06-18. A correction to any date
may move it **out, never in**.

## Record — 2026-09-14 (re-entry)

Run: `record Q032` addendum, 2026-09-14, decision-maker, autonomous (DP-40..48, DP-52..58). State
checked: `state.json` = `PREREG_DRAFT` (desk, 2026-09-14T18:38Z, "deferral lifted") — in scope.
Sources: `research/reports/STEWARD_Q032_limbs_true_partition.md` (counts only, true §2.2 partition,
`manifest_prices_universe_v001`); the Q032 section of
`research/reports/BLOCKED_Q030_Q032_registration_2026-09-14.md` (the registrar's rebuilt schedule);
items 1–16 and Corrections 1–5 above. **No `results/` directory, no `eval.py`, no outcome of any kind
was read.** Items 1–16 are not rewritten. Items 13–14's *method* binds and is re-run here. The
DEFERRED branch above is closed because its trigger was met.

**The headline: the registrar counted the calendar correctly but used the wrong rate.** The
arithmetic from 187 sessions to Monday 2027-08-23 is right, and both holidays it added are real.
**But the 187 is wrong.** The Steward's "t+40-matured" rates divide the nights that have matured
(pick nights up to 2026-07-15 only) by **all 112** elapsed sessions (running to 2026-09-10). Then 40
sessions of maturity are added again on top, so **maturity is counted twice**. Item 3 banned that
construction by name ("numerator and denominator counted over the same sub-period"). DP-53 bans it
for every unlocked draft ("add maturity once … do not penalize a forecast for its immature tail and
then add that wait again").

The correct basis is the **fully observable cohort**: the 72 sessions 2026-04-01..2026-07-15, with
exclusions kept in the denominator. On that basis:
- window = **121 sessions**
- decision = **Monday 2027-05-17**
- DP-13's ordinary **+30** extension fits, decided **Monday 2027-06-28**, which is the hard stop.

So the truncated-extension question does not come up on the main path. It is still answered (no) for
the branches where it would.

Floor D is not trimmed and Q032 is not deferred. Its risk is disclosed with numbers. **One count is
still missing before lock:** floor D is *per arm*, and the Steward reported the episode count only
for the arm that is rarer *by nights*.

### Derivation, from the Steward's own counts (arithmetic, not a new measurement)

- **Calendar (NYSE; 2026 holidays 04-03, 05-25, 06-19, 07-03, 09-07).** 2026-04-01..2026-09-10 =
  **112** sessions. This matches the Steward. 2026-04-01..2026-07-15 = **72** sessions, and t+40 of
  2026-07-15 = **2026-09-10**, the freeze's last bar. This matches the Steward's cutoff and its
  "40 not matured".
- **Where the 10 exclusions fall.** Unmatured contributing nights = 102 = 112 − 10, and unlabelled
  nights = 0. So every non-excluded night contributes. Matured contributing nights = 62 = 72 − 10. So
  **all 10 exclusions sit inside the 72-session cohort**, and the item-3 rate is
  **r₄₀ = 62/72 = 0.8611**, not 0.5536.
- **Scheduling rates (item 3's `min(r₄₀, 0.6620)`, kept as written).**
  - The cap is also the Q033 precedent: same population, same window start, floor A at session 121.
  - Contributing nights: **0.6620**. The cap binds.
  - DP-06 sub-period: on 2026-06-01..2026-07-15 (31 sessions) the same-basis rate cannot fall below
    (31 − 10)/31 = 0.677. So the cap binds there too, and the Steward's wider 2026-04-01 panel
    changes no date.
  - Rarer arm by nights (BENIGN, 29 of 62): **0.6620 × 29/62 = 0.3096**. The uncapped rate is
    29/72 = 0.4028 and is printed, not used.
  - HOSTILE (33 of 62): 0.3524 capped.
  - Gate-counting episodes: **3/72 = 0.04167** for BENIGN. This is a tape property, not a funnel
    property, so the cap does not apply. The HOSTILE count is **not reported** (item 21).

| floor | rate used | sessions | first reached |
|---|---|---:|---|
| **A** 80 contributing nights | 0.6620 (item 3 cap; r₄₀ 0.8611 → 93) | **121** | **2027-03-09 — BINDS** |
| **B** 20 nights, per arm (min = BENIGN) | 0.3096 (uncapped 0.4028 → 50) | 65 | 2026-12-15 |
| **C** 30 post-lock nights (DP-24) | 0.6620 | 46 | 2026-11-17 |
| **D** 5 gate-counting episodes, per arm | 3/72 = 0.04167 (BENIGN; HOSTILE pending, item 21) | 120 | 2027-03-08 |

**Ceiling re-solve (Correction 3), corrected.**
- Latest admissible decision is Monday 2027-09-13. That requires t+40 ≤ 2027-09-03 (−1 week lands
  on 2027-09-06, Labor Day, so the last session before it is 09-03).
- So the latest window end is **session 205 = 2027-07-09**, not 206 = 2027-07-12. Session 206 reaches
  t+40 on 2027-09-07, and first Monday on or after 09-14 is 2027-09-20, past the ceiling.
- Inequalities are floors ÷ 205, rounded up: **0.40 / 0.10 / 0.025**, identical to the file's
  as-filed values.
- Measured on the item-3 basis: **0.6620 (r₄₀ 0.8611) / 0.3096 / 0.0417**. All three limbs PASS. The
  episode limb has 67% headroom, against the registrar's 7% on the double-penalized rate.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 17 | Truncated DP-13 extension | **DEFAULTED (R-3)** | **No truncated extension in any branch. Q032's extension is DP-13's +30 sessions or nothing.** If the +30 extension would decide after 2027-09-14, no extension is registered, **hard stop = decision date**, and a gate still short there sends Q032 to DEFERRED. On item 18's schedule the +30 fits (pick nights to session 151 = 2027-04-21, decided Monday 2027-06-28, 9.5 months). So this rule binds only in item 21's `e_min = 2` branch, or after an item-9 window cut. **Why:** a truncated extension is a length no DP entry names. DP-43 fixes "DP-13's single extension = +30 sessions" and item 14 repeats it, so setting a new length would be writing policy, not applying it (DP-40). No extension is also the option less likely to reach CONFIRMED (DP-45), and DP-53 gives the later date no weight. The cost is recorded, not hidden: where this rule binds, a floor-D shortfall at the decision date ends the question with no second run. The truncation as proposed was also mis-dated: 206 → 2027-09-20, past the ceiling. The admissible version would have been **session 205 = 2027-07-09, decided Monday 2027-09-13**. | DP-43; DP-13; item 14; DP-45; not taken: extension truncated to session 205, deciding 2027-09-13 |
| 18 | Does the registrar's schedule stand | **DECIDED (correction)** | **The calendar stands; the rate basis does not, so the schedule is rebuilt.** Verified correct: session 187 = 2027-06-11; t+40 = 2027-08-10; first Monday after + one week = 2027-08-23; +30 → session 217 = 2027-07-27 → 2027-10-04; **2027-07-05 and 2027-09-06 are both NYSE holidays** (Independence Day observed; Labor Day), as is 2027-06-18. Wrong: the 0.5536 / 0.2589 / 0.0268 rates, for the reason above. The same error also makes the "item 3's cap does not bind — 0.5536 is slower" sentence false. **Rebuilt by item 14's method on item 3's basis:** window **2026-09-15..2027-03-09 = 121 sessions** (floor A binds); t+40 = 2027-05-05 (Good Friday 2027-03-26 excluded); + one week = 2027-05-12; **decision Monday 2027-05-17** (8.1 months). **Extension +30** to session 151 = **2027-04-21**; t+40 = 2027-06-17 (Memorial Day 05-31 excluded); + one week = 2027-06-24; **decided Monday 2027-06-28 = hard stop**. This moves the dates *in*. That is allowed and required: DP-53 governs this unlocked draft, and "out only" never licensed keeping an arithmetic error. | item 3; item 14; DP-53; `LEARNING_POLICY.md` "Counts-only readiness and scheduling"; Q033 `schedule.json`; not taken: 187-session window deciding 2027-08-23 — maturity counted twice |
| 19 | Floor D rests on 3 episodes: lock, DEFER, or a different plan | **DEFAULTED (R-3)** | **Lock, with floor D left at 5 per arm, the gate checked on `eval.py`'s measured counts, the single +30 extension, then DEFERRED.** There is no measured deferral ground: every limb passes, and D is reached inside the window at the point rate. DP-57 asks for a justification, not a deferral, and the justification is written into §5.1 and §10 as follows. **(a) Planning uncertainty, stated as numbers.** Three events in 72 sessions give an exact Poisson 95% interval of 0.62–8.77 episodes, so sessions-to-5-episodes ranges from ≈ 42 to ≈ 582. At the point rate, P(an arm is below 5 at session 121) ≈ 43%, so the extension is the likely path. P(still below 5 at session 151) ≈ 25%, so **about one chance in four of ending DEFERRED, before allowing for tape persistence, which makes these figures optimistic**. **(b) Dependence is already priced into inference.** CI-1 and the p-value resample tape-episodes (§4.4), and DP-51's CI-2 is required. Five episodes per arm is a floor that makes the contrast estimable; it does not guarantee a precise one. A near-minimum episode count yields a wide CI-1 and most likely INCONCLUSIVE, never a relaxed gate. **(c) Strata.** Only 4 of 9 cells were observed and UP×HIGH carries 90.9% of matured HOSTILE nights. The registrar's composition threat and the six-cell suppression addition stand. **(d) Readiness (DP-56).** The Steward's `readiness.json` prints per-arm label-run and gate-counting episode counts, counts only. It **never** triggers an early run, an early deferral or a date move. **Why not DEFER:** there is no measured ground (DP-43 defers on a date past the ceiling, and the date is 2027-05-17). A deferral would forfeit the blind prospective nights from 2026-09-15 for an uncertainty that only those nights can resolve. **Why not the registrar's 187:** stretching the window to lower the deferral risk (≈ 11% at 187 on the same Poisson) is not DP-43's method, and the 187 came from a double count, not from a precision argument. A quantile-based window would be a new rule, so it is proposed below, not applied. | DP-57; DP-53; DP-43; DP-13; DP-56; DP-45 (the shorter, extension-backed plan is the one less likely to CONFIRM); not taken: DEFER now on three episodes — no measured ground; forfeits the window |
| 20 | DP-58 interim look | **DECIDED** | **The registrar's declination is confirmed and re-derived on item 18's schedule.** 60 contributing nights arrive at session **91** on the scheduling rate (session 70 on r₄₀). By then the slower arm projects **3.8** gate-counting episodes (**2.9** at session 70), against §8 clause 2's 5. DP-58 waives no floor and no gate, and forbids futility stops, so the interim could only return "continue". A look that cannot stop is not a sequential design (`LEARNING_POLICY.md`: stopping boundaries must be specified; repeated CI checks are not one). Resampling ≈ 3 episodes per arm for DP-58's episode-clustered boundary is degenerate. The registrar's sentence is adopted for §5.2 and §8 with its number re-pointed: *"DP-58 is in scope and is deliberately not registered; at 60 contributing nights the slower arm projects fewer than 4 gate-counting tape-episodes against clause 2's 5, so the interim could return only 'continue'. No interim looks."* | DP-58; DP-57; ground 3; not taken: register the 60-night interim — can only return "continue" |
| 21 | Floor D per arm: the HOSTILE episode count | **ROUTED → data-steward — LOCK PRECONDITION** | Waits on the matured gate-counting episode count for **both** arms (request below). Floor D is "≥ 5 per arm", and tape runs alternate, so HOSTILE can carry 2, 3 or 4 episodes against BENIGN's 3. The arm rarer by nights is not necessarily rarer by episodes (on the unmatured basis the arm rarer by nights flips to HOSTILE). **Branches fixed now**, with `e_min` = the smaller count and D = ⌈5 × 72 / `e_min`⌉: **`e_min ≥ 3`** → D ≤ 120, floor A binds, **item 18's schedule stands unchanged**. **`e_min = 2`** → D = 180: window 2026-09-15..**2027-06-02**; t+40 = 2027-07-30 (06-18 and 07-05 excluded); **decision Monday 2027-08-09**; the +30 extension would decide 2027-09-20, so **none** (item 17); **hard stop 2027-08-09**; halves 1–90 / 91–180; DP-50(b) flag-off to 2027-08-09. **`e_min ≤ 1`** → D ≥ 360 sessions, past the ceiling, so **DEFERRED** under DP-43 with the counts named. No other count moves any date. | — |
| 22 | Limb (f): DP-50(a)/(b) commit sweep and v1.7 check since `fa70688` / HEAD `d19c9a9` | **ROUTED → data-steward — in progress — LOCK PRECONDITION** | Not waited on here. The lock commit waits on it. The DP-50(b) window it must cover is now **2026-09-15..2027-05-17** (to **2027-06-28** if the extension fires; to 2027-08-09 in item 21's `e_min = 2` branch). A listed change scheduled inside that window is item 9's window cut, applied at lock. | — |

### Corrections to the registrar's re-entry output (applied at `apply`)

1. **§5.1 / §5.2 rates:** 0.5536 / 0.2589 / 0.0268 → **0.6620 (item 3 cap; r₄₀ = 62/72 = 0.8611
   printed) / 0.3096 (BENIGN; uncapped 0.4028 printed) / 0.0417 (3/72, BENIGN; HOSTILE per item
   21)**. The sentence "item 3's 0.6620 cap does not bind — 0.5536 is slower" is struck (item 3,
   DP-53).
2. **§5.2 schedule:** window 187 → **121** (2027-03-09); decision 2027-08-23 → **2027-05-17**;
   extension "NONE ADMISSIBLE" → **+30 to session 151 = 2027-04-21, decided 2027-06-28**; hard stop
   2027-08-23 → **2027-06-28**; binding floor D → **A** (D at 120, pending item 21).
3. **§5.3 ceiling re-solve:** session 206 / 2027-07-12 → **session 205 / 2027-07-09**; inequalities
   floors ÷ 205 = **0.40 / 0.10 / 0.025** (the as-filed values, now exact).
4. **§8 clauses 1–2:** "no extension behind the gate" → **the single +30 DP-13 extension stands behind
   every gate**, then DEFERRED (item 17's no-extension rule applies only in item 21's `e_min = 2`
   branch).
5. **§6 halves:** 1–94 / 95–187 → **1–61 / 62–121**; extended **1–76 / 77–151**.
6. **§9 DP-50(b) flag-off:** 2027-08-23 → **2027-05-17 (2027-06-28 if the extension fires)**.
7. **§5.3 R2 dates:** selection freeze pick nights **2026-09-15..2027-03-09**; daily bars (every
   candidate symbol, SPY from 2025-01-02) through **2027-05-05**, delivered before 2027-05-17.
   Extension pair: pick nights ..**2027-04-21**, bars through **2027-06-17**, delivered before
   2027-06-28. The holiday list gains **2027-07-05 and 2027-09-06**, as the registrar found.
   SPY overlap with `manifest_prices_universe_v001` is compared and fails loudly (DP-50(a)).
8. **§5.1 wording:** "rarer-arm episodes" → **"gate-counting episodes in the arm with fewer
   episodes"**. Floor B and floor D each take the minimum over arms *in their own unit*, and the two
   minima need not fall on the same arm.
9. **§5.1 / §10:** item 19's uncertainty paragraph is added verbatim in substance (Poisson interval,
   ≈ 43% / ≈ 25% shortfall figures, labelled a planning approximation that tape persistence makes
   optimistic).
10. **Lock-date sensitivity:** every date assumes the lock commit lands on 2026-09-14 and the window
    starts 2026-09-15 (item 13). If the commit slips, item 13's start and every date are recomputed by
    this method, and none is carried.
11. **Unchanged and re-checked:** item 11's `eval.py` deadline **Monday 2027-04-05** still precedes
    Q027/Q029 (2027-04-12) and this decision date. §7 F2 → 17 and F1 → 28 as `G` rejoins; Q033's
    unlocked §7 count restoration is owed by the registrar, as flagged. The registrar's six-cell
    suppression addition (cells added only, closed) matches item 7.

### Defaulted on Haci's behalf (re-entry)

- #17 Truncated extension — chose **+30 sessions or no extension; hard stop = decision date when +30
  passes the ceiling**; not taken: extension truncated to session 205, deciding 2027-09-13 — DP-43.
  Overturn = successor question.
- #19 Floor D on three observed episodes — chose **lock with disclosed ≈ 25% deferral risk, standard
  extension, no trim**; not taken: defer now, forfeiting the prospective window — DP-43. Overturn =
  successor question.

### Routed requests (re-entry)

#### data-steward — R3 (counts only) — **LOCK PRECONDITION** (item 21)

Q032 is about to lock on floor D ("≥ 5 gate-counting tape-episodes **per arm**", PREREG §2.6 / §8
clause 2). `STEWARD_Q032_limbs_true_partition.md` reports matured episodes only for the arm rarer by
nights (BENIGN, 3). Please measure, on the same artefacts
(`manifest_prices_universe_v001.json`, `manifest_v001.json`, `manifest_prices_v001.json`,
`exclusions_v003.json`), never from a live query (DP-50(c)), and **counts only**. No touch, return,
excursion, `E_t` or arm-versus-outcome cross-tab of any shape; a forward bar may be read only to
establish that it exists.

- **(1)** Gate-counting tape-episodes (§2.6: maximal same-label run on the session series;
  excluded or unlabelled sessions do not break a run; counts only if it contains ≥ 1 t+40-matured
  contributing night) **for BENIGN and for HOSTILE separately**, over the fully observable cohort
  2026-04-01..2026-07-15, with each episode's first/last session and contributing-night count. Please
  **state which episodes are truncated** by the 2026-04-01 panel start or the 2026-07-15 cutoff.
- **(2)** Confirm the cohort is 72 elapsed sessions with all 10 `exclusions_v003` nights inside it, so
  r₄₀ = 62/72.
- **(3)** For disclosure only: per-arm label-run counts and run-length distributions over every SPY
  session carrying a legal §2.2 label (from 2026-02-02, the first ≥ 250-session tercile, to
  2026-09-10), with no contributing-night requirement.

**What it decides, fixed before your count (DECISIONS item 21):** `e_min` = the smaller of the two
counts in (1). `e_min ≥ 3` → the schedule in `## Schedule` stands. `e_min = 2` → window to
2027-06-02, decision Monday 2027-08-09, no extension, hard stop 2027-08-09. `e_min ≤ 1` → Q032 is
DEFERRED on DP-43's ceiling. Item (3) decides nothing. Please also write these per-arm counts into
`research/questions/Q032_regime_conditionality/readiness.json` (DP-56). Report to
`research/reports/STEWARD_Q032_episodes_per_arm.md`.

#### data-steward — limb (f) — in progress (item 22)

No new request. The sweep already under way closes the last lock limb. The only change is its
DP-50(b) horizon: **2026-09-15..2027-05-17**, or 2027-06-28 if the extension fires.

## Schedule

**Rewritten 2026-09-14 at re-entry; supersedes the struck DEFERRED block of 2026-09-14** (the reasons
for that deferral remain in "## Record — 2026-09-14"). Built by item 14's method on item 3's rate basis
(DP-53), on NYSE sessions with holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15,
2027-03-26, 2027-05-31, 2027-06-18, 2027-07-05, 2027-09-06. **Valid for `e_min ≥ 3` (item 21).**
Lock preconditions still open: **R3 per-arm episode count (item 21)** and **limb (f) commit sweep
(item 22)**.

decision_date: **2027-05-17** · extension_date: **2027-06-28** · hard_stop: **2027-06-28** · rule:
**exposure-driven**

```
Window:         pick nights 2026-09-15 .. 2027-03-09 = 121 elapsed sessions (lock commit 2026-09-14)
Binding floor:  A (80 contributing nights) at 0.6620/session (item 3 cap; r40 = 62/72 = 0.8611)
Other floors:   B 65 (2026-12-15) · C 46 (2026-11-17) · D 120 (2027-03-08; 3/72, e_min pending)
Maturity:       + 40 sessions        -> 2027-05-05 (Wed)
Freeze margin:  + one calendar week  -> 2027-05-12 (Wed)
Decision date:  first Monday on/after -> Monday 2027-05-17   (8.1 months from lock)
Extension:      DP-13 +30 sessions -> pick nights .. 2027-04-21 (session 151);
                t+40 2027-06-17; +1 week 2027-06-24 -> Monday 2027-06-28 (9.5 months)
Hard stop:      Monday 2027-06-28 -> any gate still short = DEFERRED
Ceiling:        latest admissible window end session 205 = 2027-07-09 (decision Monday 2027-09-13)
Halves:         1-61 / 62-121 (extended 1-76 / 77-151)
Interim:        none (DP-58 declined, item 20)
DP-50(b):       flag-off to 2027-05-17 (2027-06-28 if extended)
Branch e_min=2: window .. 2027-06-02, decision = hard stop Monday 2027-08-09, no extension (item 17)
Branch e_min<=1: DEFERRED (DP-43 ceiling)
```

### Superseded — the 2026-09-14 deferral block (kept as history; none of it binds after re-entry)

Its F1/F2 bookkeeping reverses as `G` rejoins (F2 17, F1 28). Its "re-measure before lock" list is
satisfied by `STEWARD_Q032_spy_history_probe.md`, `STEWARD_Q032_limbs_true_partition.md`, R3
(item 21) and limb (f) (item 22).

- **Admission ground:** `DEFERRED.md`'s **first** — the objective cannot be measured with the artefacts
  the desk holds. **Not** the second (DP-43's 12-month ceiling): the measured proxy rates sit
  comfortably inside it, and the deferral would stand even if they were faster still.
- **The blocker, exactly:** **`ALPACA_API_KEY` and `ALPACA_SECRET_KEY` are unset in the desk session**,
  so SPY split-adjusted daily bars from **2025-01-02** cannot be fetched; and **no pinned manifest holds
  them** — `manifest_prices_v001`'s SPY series starts 2026-02-02 and reaches **133** prior rvol20
  observations against the **≥ 250** §2.2 requires, at **no** session, ever. Without those bars §2.2's
  `SMA200` and its 250-session volatility tercile do not exist and **no arm can be assigned to any
  night**. It is provisioning, **not** procurement (the desk is already licensed to read this vendor —
  rule 1 names both variables), **not** a rule-14 grant, and **not** time.
- **Re-entry condition (the H-074 trigger, shared verbatim with Q030 — one trigger, two questions):**
  **`ALPACA_API_KEY` and `ALPACA_SECRET_KEY` present in a desk session, AND a market-data coverage probe
  returning SPY split-adjusted daily bars from 2025-01-02** (coverage and first/last bar date only, feed
  `sip`, no values beyond that — market-data endpoints only; the trading endpoints stay blocked by policy
  regardless of credential validity). **Both limbs, measured, never assumed:** credentials present but
  SPY history unretrievable is the same deferral. Nothing else revives it, and **no calendar re-check
  date is named**, because no amount of waiting produces the bars.
- **What a re-attempt must re-measure before it may lock — none of it inherited from this file:**
  **(1)** limb **(a)**, the §2.5/§2.6 contributing-night rate on a freeze carrying **t+40** bars, with
  numerator and denominator over the same period and the item-3 cap applied; **(2)** limb **(b)**, the
  §2.2 arm split on the **true** `SMA50 > SMA200` trend and the **true ≥ 250-session** volatility
  tercile — the SMA50-only proxy recorded above is a one-sided bound and is **never** the registered
  partition; **(3)** the rarer-arm **gate-counting tape-episode** rate on the **t+40-matured** basis,
  which is the limb that read **0.0141 < 0.0243** here and is the one this freeze could not measure
  honestly; **(4)** the nine-cell composition (six cells were observable here, because SMA200 does not
  exist in the freeze) and, with it, item 7's single permitted suppression revision, **cells added
  only**; **(5)** limb **(f)**'s DP-50(a)/(b) commit sweep and the **v1.7** schedule check, re-run at
  the new freeze — today's "NONE" is an absence of a schedule, not a permanent clearance; and **(6)**
  Correction 3's three inequalities, **re-solved from the trading calendar against the 12-month ceiling
  measured from the new lock date**, which tightens as that date moves later.
- **What does not change on re-entry:** the partition is **never** re-specified to SMA50-only (PREREG
  §5.3 R2(i), item 12) — that is a different arm chosen after the data existed, and it is a different
  question with its own id. Items 1–11 bind as written; items 13–14's method binds, its dates do not.
- **Bookkeeping.** `research/BACKLOG.md` marks **H-079 — DEFERRED 2026-09-14**, not registered; **the
  question number Q032 is consumed by this entry and is not reused.** Q032's **1** primary (`G`) leaves
  the **F2** correction set while deferred — F2 falls from 17 to **16** (Q023 2 + Q027 2 + Q029 10 +
  Q031 2) — and `G` leaves the **F1** companion set, which falls from 28 to **27**, exactly Q031
  DECISIONS #14's figure; **no cross-question edit is required and none is made**, since no locked
  PREREG records Q032 in its correction set (the H-062 / Q025 precedent). C1 is withdrawn as a blocking
  companion to Q023's E1; **Q023 is unaffected and is not edited.**
- **Nothing here may be reported, briefed or quoted**, in any form, until the trigger is met
  (`DEFERRED.md` preamble, rule 10). That binds the proxy counts in the Record above as firmly as
  anything else: they are planning numbers on a partition that was never legally assignable.

## Standing rules added

_none._ Nothing here is Haci's word: items 12, 13 and 14 were **DEFAULTED** under DP-43 / DP-45, and a
DEFAULTED item adds **no** DP entry (DP-40). Items 1–11 are applications of DP-02, DP-03, DP-04,
DP-06, DP-09, DP-13, DP-20, DP-21, DP-22, DP-23, DP-24, DP-25, DP-26, DP-28, DP-29, DP-42, DP-43,
DP-44, DP-45, DP-50, DP-51 and locked precedent (Q006, Q023, Q027, Q029, Q031).

## Standing rules proposed

- **A contributing-night rate is measured with its numerator and denominator over the same period,
  and is then capped at the desk's slowest comparable measured rate.** Q027 and Q031 scheduled on a
  maturity-truncated rate over a full-span denominator, which was a 28% haircut at a 20-session
  endpoint and would be a ~60% haircut at Q032's 40-session one — large enough to defer a testable
  question on an accounting artefact. The conservative intent is better served by measuring the rate
  on the sub-period where the endpoint's maturity is evaluable and **capping it at the slowest rate
  the desk has measured for a comparable funnel**, which is what item 3 does. Every maturity-gated
  endpoint longer than 20 sessions will meet this.
- **A question's decision date is computed on the maturity its *contributing-night* definition
  requires, not on its primary's clock.** Q032 registered a 20-session endpoint with a 40-session
  binding maturity and then scheduled on 20. Where the two differ, the later governs the decision
  date, the freeze's bar horizon and the DP-50(b) flag-off window — and DP-43's phrase "the endpoint's
  maturity window" should be read that way.
- **A provisioning limb belongs in the lock gate whenever a question's arm, population or level
  depends on data no pinned manifest holds.** Q030 was deferred for absent Alpaca credentials after
  the freeze was attempted; Q032 needs SPY history nobody has fetched, and without item 12's probe it
  would have discovered that in June 2027. The general form: **if a question cannot be graded without
  an artefact the desk does not hold, the feasibility probe runs before the lock, not at the decision
  pass.** — **This one is no longer a proposal looking for evidence: it fired on 2026-09-14 and saved
  the window.** Item 12 added the limb, R1(g) ran it the same day, it failed, and Q032 was deferred at
  a cost of one afternoon instead of at a 2027 decision pass. Recommended for confirmation first, with
  a second clause: **the probe's scope is coverage and first/last date only — never values** — so that
  running it can never unseal anything.
- **Two questions blocked by the same missing artefact share one re-check trigger, written identically
  in both entries.** Q030 and Q032 are both stopped by the absence of `ALPACA_API_KEY` /
  `ALPACA_SECRET_KEY` in the desk session, and Q032's SPY probe is a strict sub-case of the freeze Q030
  cannot build. Two separately-worded triggers on one condition is two chances to mis-record it and two
  places to forget. The general form: **when a deferral's blocker is already named in `DEFERRED.md`,
  the new entry cites that trigger by id rather than restating it, and satisfying it re-opens every
  question that cites it, in registration order.**
- **A rate measured on a proxy the question cannot legally use is recorded for the re-check and never
  carried into a schedule.** Q032's SMA50-only arm split is a one-sided bound on a partition that no
  pinned freeze can assign at all; it clears every gate and it establishes nothing. The provisional
  dates it would have produced are struck rather than parked, because a struck date cannot be inherited
  by a successor and a parked one can (the Q025 precedent, now in its second question). The general
  form: **a deferred question's schedule block is emptied, not frozen.**
- **A blocking companion that duplicates a locked question's statistic is corrected jointly with it
  and can never confirm.** Q032's C1 and Q023's E1 are the same contrast on a ~95%-overlapping
  population. Stating the pattern once — same statistic, non-independent pair, one q, blocking only —
  would stop the next overlap being registered as a second primary.
- **(re-entry, from item 17) A DP-13 extension is +30 sessions or none.** When the +30 extension's
  decision date would pass DP-43's 12-month ceiling, the hard stop equals the decision date. The
  extension is never truncated to fit.
- **(re-entry, from item 21) A per-arm floor is scheduled on the minimum over arms in that floor's own
  unit.** The arm rarer by nights is not necessarily rarer by episodes. A Steward report gives every
  arm's count, not only the rarer arm's.
- **(re-entry, from item 18) A Steward's scheduling rate states its matured cohort's own denominator.**
  A maturity-truncated numerator over a full-span denominator is printed only beside that figure, so
  a schedule cannot count maturity twice (DP-53).
- **(re-entry, from item 19) Whether a gate built on a handful of observed events should be scheduled
  at a stated probability of being met, not at the point rate.** Q032's floor D rests on 3 episodes:
  the point rate gives ≈ 25% eventual deferral, and 187 sessions would give ≈ 11%. DP-43 says "measured
  run-rate" and DP-57 does not name a quantile. Choosing one is Haci's call, not a default.
