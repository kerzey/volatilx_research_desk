# Q033 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous, DP-40..48) · Source: PREREG.md "Open decisions before
lock", 4 items (+ 17 decided, defaulted or routed here: the two routed requests named in §5.3, and
fifteen the draft settles silently or leaves to `record`)

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

**`record` run 2026-09-14** on `research/reports/STEWARD_Q033_exposure.md`: every routed item is
settled, the schedule is final, and the branch is **P2 deferred / P1 locks alone**. See
"## Record — 2026-09-14" below; where this file's `decide` text and the record disagree, **the
record governs**.

## The headline

**Q033 does not lock at `decide`, and the draft is right that R1 is blocking — but, exactly as in
Q032, R1 is blocking for two reasons and the draft's dates are wrong in the same way.** §2.3 registers
**binding maturity at 40 sessions**, §2.4 excludes any night whose t+40 falls after the freeze's last
date and §2.5 defines a contributing night as one *matured to t+40* — while §5.2 computes the decision
date by adding **20** sessions to the window end, and §5.3 R2 asks for daily bars through "session
t+20 of the last included pick night". Every date in the draft is therefore ~8 weeks early and the
shared price freeze is ~5 weeks short of the bars the registered population needs (Correction 1). A
second calendar error runs the same way: **§5.2's holiday list omits 2027-06-18** (Juneteenth), which
every other question on the desk lists (Correction 2). Both move the schedule **out**, the only
direction DP-43 and DP-45 permit: **decision date Monday 2027-07-12**, not 2027-06-07; extension
decision and hard stop **Monday 2027-08-23**, not 2027-07-26.

**All four of the draft's own items go the Registrar's way and all four are DECIDED** — the ±0.5 ATR
band (#1), scoring an unresolved race 0 (#2), the equivalence reading of NULL (#3) and F8-with-two-
companion-corrections (#4). Each is either a Registrar convention fixed before any outcome exists
(DP-26), a technical matter with one defensible answer, or a pair of options differing only in
strictness, where the stricter is taken without asking. **Thirteen further items are DECIDED** on DP
entries and locked precedent. **Three are DEFAULTED** under R-3 — the prospective-only window start,
the window end / decision date block, and a new lock-gate limb. **Two are ROUTED** to the Data
Steward: **R1** (counts only, **blocking for lock**) and **R2** (successor freezes, due at the
decision date, blocking nothing — DP-23).

**One limb is added to the lock gate, and it is the Q030 precedent, not an invention** (item 16).
§2.2's arm cannot be assigned without SPY daily bars back to 2025-01-02, which sit in **no** pinned
manifest and were last unobtainable because `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` were absent from the
desk session (H-074 / Q030, DEFERRED 2026-09-14). The draft leaves that discovery to the **2027
decision pass**, where its cost is the whole window. It is probed **now**, and a failed probe with no
pinned alternative defers **P2 at the lock** while **P1 locks alone** — P1 does not depend on the arm.

**One arithmetic claim in the draft is false and is struck** (Correction 5). §2.4 asserts that the
`d_L3 ∈ [0.25, 10]` validity bound "keeps the direction band strictly inside the magnitude level: a
pick whose printed L3 sits below 0.5 ATR cannot enter". It does not — the bound admits `d_L3` between
0.25 and 0.5, and §10 threat 6 says so correctly two pages later. The bound is **not** raised to 0.5:
the conflation biases `V` **toward zero**, which is the direction that cannot manufacture a positive
(DP-45), and [0.25, 10] is Q027's and Q031's screen verbatim.

**Rule 14: no exception is requested and none is needed.** Every input is a 16:05 ET candidate field,
a SPY or symbol bar dated ≤ t, or the session t+1 open used **only** as an entry price; §6's table
declares each one and §6's `eval.py` clause freezes every eligibility, arm, match and stratum field
before any post-pick-night bar other than that open is loaded. **DP-05 is untouched and DP-41 is not
engaged.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | The width of the symmetric direction band (draft item 1) | DECIDED | **Option A — `U = X + dir × 0.5 × ATR`, `D = X − dir × 0.5 × ATR`, both from the t+1 open; the ±1.0 ATR variant is a fixed sensitivity printed in every branch that decides nothing.** The band is a **Registrar convention fixed at this lock and derived from no outcome**, so DP-26 carries it as drafted; H-081 names no level for its direction claim (it names a 20-session sign), so DP-42's "the level the hypothesis names" does not bind and nothing here encodes how Haci trades — the band is a measurement device, not an entry, a target or an exit (DP-02: nothing in this question is an exit). Option B is refused on the question's own logic: at ±1.0 ATR the band sits at or through the printed `L3` for a material share of picks, `a_p` and `m_p` become close to the same indicator, and `V` collapses toward zero by construction (§10 threat 6) — a direction endpoint that is quietly a second magnitude endpoint answers neither half of H-081. The 0.5 is fixed at lock, moves in neither direction at the decision pass, and R1(d) measures the residual conflation **before** the lock. | **DP-26** (registrar-chosen bands and clocks stand as drafted where no sealed outcome informed them); **DP-42** (no level is named by the hypothesis; nothing here is a horizon, a lane or a structure); **DP-02**; §10 threat 6; **DP-45** (the choice that keeps the two series distinguishable, not the one that makes them agree) |
| 2 | How a race that never resolves inside 20 sessions is scored (draft item 2) | DECIDED | **Option A — an unresolved race scores `a_p = 0` and the pick stays in the denominator, for picks and matched controls alike; a race resolving counter-first scores 0; a same-session pair hourly bars cannot order scores 0 (DP-27). The unresolved share and the same-session-tie count print per arm, for picks and controls separately, in every branch.** Option B (restrict both rates to decided races) makes the denominator a function of the outcome — the one thing a pre-registered rate may never be — and drops exactly the "went nowhere" picks a direction-versus-magnitude comparison exists to describe. A is also the arithmetically conservative side: unresolved races dilute both rates toward each other and so toward `A = 0`. | ground 3 — one defensible answer: a denominator that depends on the outcome is not an estimate of anything; **DP-27** (an unorderable same-session pair takes the outcome less favourable to the hypothesis); **DP-26** (the coding is a convention fixed at lock); **DP-45** |
| 3 | What NULL requires beyond a CI that includes 0 (draft item 3) | DECIDED | **Option A — the equivalence reading. NULL requires floors and clauses 1–3 met, both CIs including 0, the point estimate inside its MPE, **and both CIs lying entirely inside ±MPE**; anything else is INCONCLUSIVE.** This is a deliberate, one-way divergence from the house pattern (Q002, Q006, Q024 all read NULL as "CI includes 0 and |estimate| < MPE"), and the direction of the divergence is what makes it a DECIDE rather than an ASK: A makes a **NULL harder to declare** and can never make a CONFIRMED easier to reach. It is the stricter of two readings that differ only in strictness, so it is taken without asking. The ground is specific to this question: `V` is a **triple** difference whose CI may be several times ±10 pp wide, and under B *"the two halves of the pick's claim are equally sensitive to the tape"* — a sentence §9 would print — could be declared from an interval that excludes nothing. The clause binds both primaries, not only P2, and the reported NULL sentence carries the CI beside it. | **DP-45** / the standing rule that where two options differ only in strictness the stricter is taken and not put to Haci; rule 6 ("positive but below MPE" is INCONCLUSIVE — the same logic applied to "indistinguishable from zero"); ground 3; listed under *Standing rules proposed* because it generalises beyond Q033 |
| 4 | Which family carries the question (draft item 4) | DECIDED | **Option A — F8 as filed in BACKLOG.md, `m = 2` within the question, with P1 additionally BH-corrected across F1 and P2 additionally across F2, and the larger of the two applicable q's quoted and read by §8 clause 10.** A is **strictly stricter** than either single-family reading: F8 alone would correct `A` across 2 instead of 29 and `V` across 2 instead of 18. Option B (re-file the whole question to F2 and correct once) is refused because the two primaries have genuinely different subjects — `A` is a picks-versus-matched-control path contrast (F1's subject), `V` is a conditionality statistic (F2's) — and because re-filing a hypothesis out of the family it was filed in is a bookkeeping change that would also drop `A`'s F1 correction. Counts, cross-checked against Q032 DECISIONS #10: **F1 = 29** (Q006 2 + Q024 6 + Q025 2 + Q029 16 + Q031's `D1ᴮ` 1 + Q032's `G` 1 + Q033's `A` 1); **F2 = 18** (Q023 2 + Q027 2 + Q029's 10 companion IC endpoints + Q031 2 + Q032's `G` 1 + Q033's `V` 1); **F8 = 2** at this lock and never below it. `G_μ` carries **no q of its own** and is corrected jointly with Q032's `G` as one non-independent pair; neither may ever be read as confirming the other. | rule 8; **DP-29** (family by the primary endpoint's subject, with a companion correction where the statistic belongs to another family; an overlapping hypothesis is never counted twice); **DP-45** (of two readings differing only in strictness, the stricter); **Q031 DECISIONS #14**, **Q032 #10**, **Q029 #20/#26** — the same pattern, stated symmetrically and never shrinking |
| 5 | Binding maturity, and the clock the decision date is computed on | DECIDED | **40 sessions, as §2.3 / §2.4 / §2.5 register it — and §5.2's arithmetic, §5.3 R2's bar horizon and §9's flag-off dates are corrected to match (Correction 1).** A contributing night is a night matured to **t+40**; both primaries' own clock stays **20 sessions from `X`** (DP-09 — `L3` is the primary magnitude level, and the direction band runs on the same clock so the two series are contrasted over identical exposure); the 40-session companion of `μ` and of `V` stays descriptive. Consequences, all applied: decision date = window end **+ 40 sessions + one calendar week, first Monday on or after**, moved out again for a market holiday → **Monday 2027-07-12**, not 2027-06-07; the successor price freeze carries daily bars through **t+40** of the last in-window pick night (**2027-06-29**, not 2027-05-28), and through **2027-08-11** on the extension path (not 2027-07-13); §9's DP-50(b) flag-off runs to **2027-07-12 / 2027-08-23**. The alternative — bind maturity at 20 and let the 40-session companion be right-censored — was refused: it is the option that reaches a date sooner, it would make §2.5's own definition of a contributing night untrue, and §2.4 already forbids grading right-censoring as a non-touch. | ground 3 — a floor counted on t+40-matured nights cannot be scheduled on t+20; **DP-43** (window end plus *the endpoint's* maturity window plus a one-week freeze margin); **DP-45** (never the earlier date); **DP-23** (a successor freeze is built to the horizon the registered population needs); **Q032 DECISIONS #2 / Correction 1**, the identical error on the identical freeze at the identical lock date |
| 6 | Which measured rate the schedule is built on, given a 40-session maturity and a freeze ending 2026-09-10 | DECIDED | **The scheduling rate is `min(r₄₀, 0.6620)`**, where `r₄₀` = R1(a)'s contributing-night rate under **§2.5's complete rule** (≥ 3 valid published picks, each with ≥ 5 valid matched controls) with **numerator and denominator counted over the same sub-period** — the maximal stretch of 2026-06-01..2026-09-10 whose nights can be graded to **t+40** on `manifest_prices_v001`, whose last pick night the Steward fixes from the calendar — and **0.6620** is the desk's measured published-pick contributing rate (47/71 at t+20 maturity, `STEWARD_Q031_exposure.md` §(a)). Every real loss mechanism stays in `r₄₀`'s denominator (exclusions, DP-04, null / non-monotone ladder, split-scale payload, < 5 valid controls, < 60 prior bars, > 25% ungradeable); **only** freeze-horizon censoring is removed, and only because it **cannot occur inside the registered window** — R2 delivers t+40 bars for every in-window night. The cap is the binding half: **no date is ever computed from a rate faster than the desk's own measured published-pick number**, and if R1 measures slower than 0.6620 the slower number governs. | **DP-43** (dates projected from the Steward's exposure count at the measured run-rate); **DP-45** (the `min`, never the faster rate); ground 3 (a rate's numerator and denominator must cover the same period); **Q032 DECISIONS #3**, the identical construction, adopted here rather than re-argued |
| 7 | The trading calendar the dates are solved on | DECIDED | **The desk's standard holiday list, which §5.2's list is missing one entry of: 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05 and 2027-09-06** (Correction 2). 2027-06-18 (Juneteenth observed) is listed by Q018, Q020, Q021, Q023, Q024, Q031, Q032 and both Steward exposure reports; its omission does not touch the 158-session window count (it falls after 2027-04-30) but it moves **every** +40-session arithmetic that crosses June 2027, including the decision date, the extension decision date, the price-freeze horizons and the 12-month-ceiling back-solve. 2027-09-06 (Labor Day) is added for the ceiling back-solve only. Every date is **re-confirmed session by session from the trading calendar** by the Steward when the freeze is built, and a correction may move a date **out, never in**. | ground 3 — one calendar, and a date arithmetic that omits a session is simply wrong; **DP-45** (the omission shortened the schedule; the correction lengthens it); **Q031 DECISIONS Correction 8** (the holiday-skip arithmetic written out rather than asserted) |
| 8 | The MPEs, and the two level lines | DECIDED | **P1: ±5.0 pp** — DP-20's base value and H-081's own filed number for each excess. **P2: ±10.0 pp** — DP-20's larger-MPE clause applied with the Registrar's one-line reason kept in §4.2: `V = G_μ − G_α` is a **difference of two control-adjusted arm contrasts**, one further difference than the difference-of-differences shape DP-20's clause was written for, and at ~100 nights a 5 pp bar on a triple difference returns INCONCLUSIVE by construction rather than by evidence. This is the Q012 P2 / Q018 P4 / Q022 E1 / Q023 E1 / Q032 P1 shape at one further remove, and it is **not** the Q031 `D1ᴮ` shape (a decay bounded above by the level it decays from, where the doubling was correctly declined). **The level lines in clauses 3 and 5 stay ±5.0 pp and ±10.0 pp exactly as drafted. No MPE and no level line is lowered at the decision pass in any branch**, including one where a CI excludes zero at 9 pp. | **DP-20** (+5.0 pp base; larger MPE only with a stated reason, smaller never); **DP-25** (±5.0 pp is H-081's own number and is not re-united); **DP-44** (percentage points throughout; no money unit invented; sessions-to-touch descriptive); **Q032 DECISIONS #5**, **Q023 E1** locked precedent |
| 9 | Demotion — what happens if an arm is short | DECIDED | **Neither arm is demotable, settled at this lock and not at the decision pass, as §5 registers.** `V` **is** the BENIGN − HOSTILE contrast of two series, so an arm below 20 contributing nights leaves no P2 at all: it is a floor failure — the single automatic DP-13 extension (+30 sessions), then **DEFERRED** — never a demotion to descriptive and **never an INCONCLUSIVE verdict**. DP-43's demotion clause is recorded as having nothing to demote. The same handling covers the §8 clause 2 gate (≥ 5 gate-counting tape-episodes per arm). **P1 survives an arm shortfall** — it is a pooled level, not an arm contrast — and is reported alone in that branch **only after** the extension has fired and P2 has gone to DEFERRED, with the report saying so in one sentence. | **DP-43** (an arm's demotion is settled at lock and never afterwards; here it resolves to "not demotable"); **DP-13** (one extension, fired on `eval.py`'s measured counts, then DEFERRED); **DP-21**; **Q032 DECISIONS #6**, same construction on the same arms |
| 10 | The sub-cell suppression list | DECIDED | **Fixed at this lock as §4.3 lists it, revised once at `record` from R1's measured counts on this question's own population, and then closed — and the revision may only move cells ONTO the list, never off it.** Suppression restricts **affirmative reporting only**: it never removes a blocker, and the halves, the four stability cells, the bull-only companion and `G_μ` are never on the list and block at whatever count they have. A cell suppressed at lock stays suppressed even if it clears 20 measured nights at the decision pass; a cell not suppressed still needs ≥ 20 **measured** contributing nights to print. The one-way rule is deliberate and follows Q032 rather than Q027: Q033's suppressions are **structural** — PI-010's 2–3 elite picks a month against `publication_floor = 80.0`, H-062's bear grading, `confidence_level` / `best_timeframe` / `d_L3` / `atr_pct` thinness — not density expectations R1 can overturn, and the desk does not add an affirmative cell to a prospective question after the drafting is done. | **DP-21** (20 per reported cell, no floor moved in either direction); **DP-45** (the stricter of two readings); **Q032 DECISIONS #7**, **Q023 #9**, **Q027 Correction 2** ("suppression never removes a blocker", in the same words) |
| 11 | Exclusions inside a window every night of which postdates every existing freeze | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** — verified the newest file on disk (v001, v002, v003 present) — with the **add-only successor exclusions file** issued with the successor selection freeze, on the identical **four** criteria (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10. The successor file may only **add** nights; no night is removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be; `exclusions_v003.json` is not edited (`research/data/` is not writable from here). Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. DP-04 applies mechanically on top. The fourth criterion is load-bearing: on a `payload_disabled` night the published slate carries no `lane_plans`, so there is no `L3`, no `d_L3` and no eligible pick — the night is excluded whole rather than entering as a zero. | **DP-22** read as "one list, one set of criteria" (its "cite the newest file" clause presumes a sealed window; Q033's is entirely post-freeze); **DP-04**; **Q032 DECISIONS #8**, **Q031 #12**, **Q027 #11 + `record` amendment** — same construction |
| 12 | A mid-window change to what "a published pick" or "its printed L3" is, and the DP-50(b) constraint that follows | DECIDED | A change to the SAS weights, the timeframe multipliers, `qualification_threshold`, the ATR-elite caps, the GEX offset, a scoring enable-flag, `publication_floor`, `bear_publish_threshold`, `max_output_cap`, `min_completeness` or the lane-plan writer — **including any promotion of v1.7** — **cuts the window at the ship date**: the post-ship segment becomes the question's window with the whole §5 schedule recomputed from it (**out, never in**, same single extension, same 12-month ceiling measured from the original lock), the pre-ship segment becomes a labelled descriptive panel entering no verdict, and if neither segment reaches the gates inside the ceiling Q033 is **DEFERRED**. `eval.py` prints the per-night `config_json` composition and **fails loudly** rather than silently excluding. Running the other way (DP-50(b)): every listed change is **flag-off until 2027-07-12** (**2027-08-23** if the extension fires) — Correction 1's dates, five weeks later than the draft's — checked before any fix brief is written. A change to `services/market_regime/scorer.py` touches only the §4.3 descriptive cross-check and is a DP-06 split for that companion, never for either primary: the arm is a function of SPY bars alone, which is the practical payoff of a bar-only partition. | **DP-06** / **DP-50(a)** (a repair or config change splits a column into two features at the ship date); **DP-50(b)** (ship timing checked against in-flight questions, the PI-011 / Q010 pattern); **DP-50(c)** (the sweep runs on the pinned freeze and the read-only repo); **Q032 DECISIONS #9**, **Q027 #12**, **Q031 #13** |
| 13 | `m`, and what may never be added to it | DECIDED | **`m = 2` within the question, fixed in every branch** — P1 and P2 and nothing else. No third endpoint is added at the decision pass; the four named blockers (the halves, the stability cells, bull-only, `G_μ`) **block without carrying a q**; every §4.3 secondary prints raw p only, marked *"descriptive, does not decide"*. In the item-16 branch where P2 is deferred at lock, `m = 1` honestly — and that loosens nothing, because §7's larger-q rule already corrects `A` across the **29**-endpoint F1 companion set, which dominates the within-question correction in every branch. | rule 8; **DP-29**; **Q032 DECISIONS #10**; **DP-45** (the within-question `m` is never reduced to reach a q, and the branch that reduces it is shown not to change `A`'s correction) |
| 14 | When `eval.py` must be committed | DECIDED | **Written once (rule 9) and committed no later than Monday 2027-04-05, sha256 recorded, not touched afterwards; the extension run uses the byte-identical, unmodified file.** The draft registers no deadline, and this question needs one more than most: **Q027 and Q029 decide on 2027-04-12** on the same window, the same freeze, the same entry and the same 20-session clock, and **Q032 decides ≈ 2027-06-28 printing `G` — the same statistic as this question's `G_μ`, on the same nights, from the same picks and the same controls**. A script written after any of those passes is a script written with part of its own answer in view. | rule 9 (deterministic script written once, no tuning while looking); rule 3; **Q032 DECISIONS #11** (the same deadline, the same reasoning); **Q031 DECISIONS Schedule** |
| 15 | The descriptive reads that run past the binding maturity | DECIDED | **Every descriptive read beyond t+40 prints its matured-night count beside it, and its right-censored rows are counted, never graded as non-touches** (Correction 6). §4.3's per-level L1…L6 first-touch rates and sessions-to-touch run on "each level's own lane window", which includes the long lane's **60** sessions — a horizon no in-window night will have under a 40-session freeze. **No endpoint and no blocker depends on a bar after t+40**, and the 40-session companions of `μ` and `V` are inside the maturity and unaffected. | §2.4's own rule (right-censoring is never graded as a non-touch); **DP-01** (the descriptive companion is descriptive, and an incomplete one is labelled); **Q032 DECISIONS Correction 4**, identical clause |
| 16 | The SPY history the arm needs exists in no pinned manifest — when that is discovered, and what it costs | **DEFAULTED (R-3)** | **Probe at the lock, not at the decision pass: R1 gains limb (f)** — whether `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` are present in the desk session and whether SPY split-adjusted daily bars **from 2025-01-02** can be retrieved (coverage and first / last bar date only). **A failed probe with no pinned alternative defers P2 at this lock**: `V` is entered in `research/questions/DEFERRED.md` with the H-074 credentials re-check trigger, **P1 locks alone** (`m = 1`, F8 = 1, `A` still corrected across F1's 29), and §9's P2 consequences are struck for that branch. The partition is **never** re-specified to SMA50-only after the fact — that is a different arm chosen after the data existed — and §5.3 R2(i)'s decision-pass version of the same failure stays in force as the second net. The draft's handling (discover it in July 2027) was refused: it costs the whole window for a probe that costs an hour, and the last attempt to fetch bars the desk did not already hold ended in Q030's deferral for exactly this reason. | **DP-43** (a question locks when its floors are reachable and defers on a measured ground, never a preference; dropping a primary endpoint is R-3 and is defaulted here); **DP-45** (fail early rather than late; the deferral is of the endpoint that cannot be measured, not of the one that can); **Q030 / H-074** (the credentials limb, first admitted 2026-09-14); **Q032 DECISIONS #12**, the same limb added to the same freeze on the same day; not taken: leave it to R2 at the decision pass — costs the window |
| 17 | The window start: prospective-only, and the sealed stretch as a labelled panel | **DEFAULTED (R-3)** | **Pick nights ≥ 2026-09-15 only** — the first session after the lock commit, so no night whose 16:05 ET run may precede the lock can enter. The sealed stretch (2026-06-01..2026-08-12) prints **once** as a labelled post-hoc panel, split at **2026-07-06** (`_enforce_ladder_monotonic`, the ship that changed the ladders `d_L3` is read from), computed from the successor freeze's extended SPY history so the arm is the registered one, entering **no verdict, no CI comparison, no half, no stratum test, no q and no §9 rule**, with its matured-night count printed beside every endpoint. The ground is not a convention here: the standing `directional_pct ≈ base rate` finding and EXPLORE_001's in-sample per-level and speed reads are **what put H-081 on the backlog**, and H-081's own line records that the desk expects the opposite of Haci's PASS — those nights can produce a description and not a test. | **DP-43**; rule 3; **Q032 DECISIONS #13**, **Q027 #7**, **Q031 #6** verbatim (same population, same panel, same split date); not taken: read the sealed nights — decides now, but tests the data that proposed the hypothesis |
| 18 | Window end, decision date, extension, hard stop | **DEFAULTED (R-3)** — provisional; final at `record` on R1 | **Window: pick nights 2026-09-15 .. 2027-04-30 = 158 elapsed sessions** (unchanged unless R1's measured rates push it **out**). **Decision date: Monday 2027-07-12**, not the draft's 2027-06-07 — 2027-04-30 **+ 40 sessions maturity** (Correction 1) **= 2027-06-29** on the corrected calendar (Correction 2), **+ one calendar week = 2027-07-06**, first Monday on or after = **Monday 2027-07-12**. **Single DP-13 extension of +30 sessions** to pick nights .. **2027-06-14** (session 188), decided **Monday 2027-08-23** (2027-06-14 + 40 sessions = 2027-08-11; + one week = 2027-08-18; first Monday on or after = 2027-08-23), **which is also the hard stop**: still short there, Q033 goes to DEFERRED. **9.9 months** and **11.3 months** from the 2026-09-14 lock, both inside DP-43's 12-month ceiling (2027-09-14). The **method** is fixed here and is not re-argued with counts in view: window end = the **latest** of floor A (80 contributing nights per primary), floor B (20 contributing nights in the rarer arm), floor C (30 post-lock nights, satisfied by construction) and floor D (5 gate-counting tape-episodes per arm) at item 6's rate; then + 40 sessions + one week, first Monday, moved out again for a holiday. Floor B binds and projects **marginal** (20.9 against 20) on a **placeholder** arm share, which is exactly what DP-13's single extension and the DEFERRED fallback are for; every date moves **out** if R1 measures slower and **never in** if it measures faster. The halves and the four stability cells are re-cut on the extended window by the same session-index rule fixed at this lock. | **DP-43** (the window that reaches every floor at the measured rate, plus the endpoint's maturity and a one-week margin, first Monday on or after; +30-session extension; 12-month ceiling); **DP-13**; **DP-21**; **DP-24**; **DP-45** (out only; never the shorter window, never the faster rate, never the 20-session clock that would have decided five weeks sooner); not taken: the draft's 2027-06-07 / 2027-07-26 on 20 sessions of maturity and a calendar missing Juneteenth |
| 19 | The exposure counts this question has never had | ROUTED → data-steward — **CLOSED at `record` 2026-09-14** (`STEWARD_Q033_exposure.md`; limb (a) PASS 0.6620, limb (f) FAIL → items 22–24) | waited on **R1** (counts only) — **BLOCKING FOR LOCK**, as §5.3 already says. It settles item 18's dates whole, and the lock-or-DEFER gate itself: **≥ 0.40** contributing nights per elapsed session, **≥ 0.10** rarer-arm contributing nights per elapsed session, **≥ 0.025** rarer-arm gate-counting tape-episodes per elapsed session (Correction 3, re-solved at `record` from the calendar), **plus limb (f)'s SPY-history probe** (item 16). All limbs clear → Q033 locks with §5.2 recomputed **out**; a floor limb short → **DEFERRED** with the measured counts and the re-check trigger named, not registered on a weaker partition; limb (f) short → **P2 deferred, P1 locks alone**. | — |
| 20 | Successor freezes | ROUTED → data-steward — **OPEN, rescoped and dated at `record`** (item 30: SPY-from-2025-01-02 withdrawn and held with P2; `market_regime_daily` upgraded to the rule-7 read; horizon t+40 → 2027-06-29 / 2027-08-11; due before 2027-07-12) | waits on **R2** — the shared successor pair (selection: `sas_candidates` **every row, published and unpublished**, `sas_runs`, `market_regime_daily`; prices: daily bars for **every candidate symbol on every in-window night**, hourly for published symbols), with Q033's two added scope requirements: **SPY split-adjusted daily bars from 2025-01-02**, and **daily bars through t+40 of the last in-window pick night** (Correction 1) — through **2027-06-29**, and **2027-08-11** on the extension path. Due before the decision date; **not a blocker for lock** (DP-23). Dates fixed at `record` from item 18. | — |
| 21 | What a pick whose printed `L3` sits inside the direction band does to `V` | DECIDED | **The validity bound stays `d_L3 ∈ [0.25, 10]` ATR, verbatim Q027 / Q031 §2.4, and §2.4's claim that it "keeps the direction band strictly inside the magnitude level" is struck as false** (Correction 5). It does not: the bound admits `d_L3` between 0.25 and 0.5, for which `U` sits at or beyond `L3`, `a_p` and `m_p` are nearly the same indicator and `V` collapses toward zero. Raising the bound to 0.5 was considered and refused: the conflation biases `V` **toward** zero — the direction that cannot manufacture a positive — and raising it would change the population after Q027 and Q031 fixed the same screen. Instead: **R1(d) measures the `d_L3 < 0.5` share before the lock**; the joint distribution of `(a_p, m_p)` and their within-night correlation print at the decision pass; the `d_L3`-tercile panel is computed as counts (suppressed from affirmative reporting). If R1(d) shows a material share below 0.5 ATR, that is a reported fact about the ladder (PI-009 / H-053) and **never a licence to move the band after the fact**. | **DP-45** (the residual conflation runs against the hypothesis, so the loose bound is the conservative one); **DP-26** (the band and the screen are lock-time conventions and neither moves at the decision pass); **Q027 / Q031 §2.4** (the identical screen, not re-cut for one question); §10 threat 6, which the draft already states correctly |

## Record — 2026-09-14

**Run:** `record Q033` by decision-maker (autonomous, DP-40..48) · **Source:**
`research/reports/STEWARD_Q033_exposure.md` (R1, counts only, limbs (a)–(f), independently recomputed
from `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, no live query —
DP-50(c)) · **State at record:** `state.json` = `PREREG_DRAFT` — in scope.

**The branch is item 16's, and it fired on a measured limb, not a preference. Limb (f) FAILED** —
`ALPACA_API_KEY` and `ALPACA_SECRET_KEY` are both unset in the desk session, so the
SPY-from-2025-01-02 probe could not be attempted (the H-074 blocker, its third firing in one day
after Q030 and Q032). **P2 (`V = G_μ − G_α`) is DEFERRED at this lock; P1 (`A`, the direction
excess) locks alone**, `m = 1`. **Q033 itself is not deferred**: the only floor limb that gates P1
clears with 65% headroom — **0.6620 contributing nights per elapsed session against a floor of
0.40**, on Q033's own §2.5 funnel with item 6's cap binding (`min(r₄₀ = 0.8710, 0.6620) = 0.6620`) —
and the decision date lands **Monday 2027-07-12**, 9.9 months from the lock, inside DP-43's ceiling
of 2027-09-14.

**Nothing in the schedule moves in.** The Steward's informational note (measured HOSTILE richness
0.42/0.31/0.18 against §5.1's 0.20 placeholder) would move the binding floor from B to A and pull the
window end to ~121 sessions and the decision to ~2027-05-17. That reading is **not taken**: it rests
on an SMA50-only bound on a partition this question is **not computing at all** now that P2 is
deferred, and a shorter window is never chosen to reach a date sooner (DP-43, DP-45). The window
stays **158 sessions** — already longer than every floor the locked question carries, which is the
permitted direction.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 22 | The branch, on the measured limbs | **DEFAULTED (R-3)** | **P2 deferred at this lock, P1 locks alone** — items 16, 9 and 13 applied exactly as written. `V` goes to `research/questions/DEFERRED.md` on the **H-074 provisioning trigger cited by id** (item 33); P1 locks with `m = 1`, F8 = 1, `A` still corrected across F1's **28** (item 27). The §2.2 arm is **not computed anywhere** — not for a stratum, not for a panel, not for a sensitivity — and the **SMA50-only proxy is never substituted** for it (item 16, and the Q032 entry states the same prohibition twice for the same reason). The two options refused: **defer Q033 whole** (item 23 shows the limb that would force it gates P2 only, and P1's own limb clears) and **re-specify the partition to SMA50-only** (a different arm chosen after its counts were seen — rule 3, DP-45, PREREG §5.3 R2(i)). | **DP-43** (deferring a primary endpoint is R-3, defaulted here); **DP-45** (the endpoint deferred is the one that cannot be measured, not the one that can); PREREG §5.3 R2(i), §10 threat 11; **Q032 / H-079** and **Q030 / H-074**, same blocker, same day; not taken: defer Q033 whole — P1 is measurable |
| 23 | Whether the rarer-arm episode limb bears on P1, and which reading governs it | DECIDED | **It does not bear on P1, and its governing reading is the strict one.** Two parts, settled separately. **(i) Scope:** the rarer-arm limbs — ≥ 0.10 rarer-arm contributing nights and ≥ 0.025 rarer-arm gate-counting episodes — were sized for floors **B** and **D**, and §8 clauses 1 and 2 mark both **"(P2 only)"**. With P2 deferred at the lock they have no endpoint to gate; they travel to `DEFERRED.md` with `V`. P1's gate is limb (a) alone: **0.6620 ≥ 0.40, PASS**. **(ii) Reading:** for the record, and for what P2 must re-measure, the **strict full-window t+40-matured reading governs — 1/71 = 0.0141, SHORT** against 0.025. The Steward's reading 1 (sub-period-restricted, 0.0323) and reading 2 (eligible-pick basis, 0.0563) are both recorded and neither is adopted: where two readings of one count differ only in how easily a floor is reached, the desk takes the one that does not reach it (DP-45), and item 6's censoring-removal licence was written for limb (a)'s **rate**, whose denominator R2 can guarantee, not for an **episode count** whose supply no successor freeze can guarantee. The consequence is recorded honestly: **P2 now carries two independent deferral grounds** — the absent SPY history and a rarer-arm episode supply that this freeze cannot show reaching 5 — and **both must be re-measured** before any successor may lock (item 33). | ground 3 (a gate limb gates the endpoint it was sized for; §8 clauses 1–2 say "(P2 only)" in their own text); **DP-45** (the stricter reading of the same counts, and never the one that reaches a floor more easily); **Q032 / H-079** "what a re-attempt must re-measure", item 3 — the identical limb recorded the identical way one day earlier |
| 24 | Window, decision date, extension, hard stop — final | **DEFAULTED (R-3)** | **Window: pick nights 2026-09-15 .. 2027-04-30 = 158 elapsed sessions** (unchanged; item 18's method re-run on measured rates, which are not slower). **Decision date: Monday 2027-07-12.** Arithmetic, session by session on the Correction 2 calendar: 2027-04-30 (Friday, session 158) **+ 40 sessions maturity** — May 3…May 28 is 20 sessions (2027-05-31 Memorial Day removed), Jun 1…Jun 29 is 20 more (2027-06-18 Juneteenth removed) — **= 2027-06-29**; **+ one calendar week = 2027-07-06** (Tuesday); **first Monday on or after = 2027-07-12**, which is not a holiday. **Extension (DP-13, +30 sessions): pick nights .. 2027-06-14** (session 188), decided **Monday 2027-08-23** (2027-06-14 + 40 sessions = 2027-08-11, +one week = 2027-08-18, first Monday = 2027-08-23), **which is also the hard stop** — still short there, Q033 goes to DEFERRED. **9.9 and 11.3 months** from the 2026-09-14 lock, both inside DP-43's 2027-09-14 ceiling. **Binding floor is A** — ≥ 80 contributing nights — which at the measured 0.6620/session binds at session **121**, projecting **104.6 nights at 158**; floor C (DP-24's 30 post-lock) binds at session 46 and is satisfied by construction; **floors B and D leave the locked question with P2**. The window end is **not** pulled back to 121 (DP-43, DP-45). | **DP-43** (window = the one that reaches every floor at the Steward's measured rate, plus the endpoint's maturity and a one-week margin, first Monday on or after; +30-session extension; 12-month ceiling); **DP-13**; **DP-21**; **DP-24**; **DP-45** (out only; never the shorter window, never the faster rate); items 5, 6, 7, 18; not taken: pull the window end in to session 121 — sooner, shorter |
| 25 | What a contributing night is once the arm is not computed | DECIDED | **For P1 the §2.5 contributing-night rule reads: a non-excluded in-window night with ≥ 3 valid published picks, each carrying ≥ 5 valid matched controls, matured to t+40 — the clause "carrying a legal §2.2 arm label" is struck, and §2.4's "fewer than 250 prior SPY sessions → excluded" screen is not applied** (Correction 12). Both clauses exist only to serve the arm; left in place with no SPY history they would exclude **every** night and empty a population that is otherwise fully measurable. **Every other screen stands verbatim** — DP-04, the four exclusion criteria, null/wrong-side/non-monotone ladder, `d_L3 ∈ [0.25, 10]`, the split-scale payload screen, ≥ 60 prior bars, ungradeable ≤ 25% per night. This is exactly the funnel the Steward measured 0.6620 under (its (a)(ii) is arm-free by construction), so the rate and the rule do not drift apart. | ground 3 — a screen whose only purpose is a deferred endpoint cannot silently empty the surviving endpoint's population; **DP-21** (no floor moved); `STEWARD_Q033_exposure.md` §(a); **Q031 §2.5** series-B rule, which carries no arm clause and is the rule 0.6620 was counted under |
| 26 | Rule 7 in the P1-alone branch | DECIDED | **The platform's point-in-time `market_regime_daily` label carries the rule-7 stratification for P1, descriptively, and the two §6 halves carry the calendar split and block under §8 clause 6.** The bar-only partition was rule 7's answer for both primaries (§6); with it gone, CLAUDE.md rule 7's own words — "stratified by `market_regime_daily` regime, and by the calendar split in the PREREG" — are satisfied directly by the platform label, which is **knowledge-time-legal for every night in this window** (FREEZE_v001 §7: legal from 2026-06-09; the window opens 2026-09-15). It **defines no arm, blocks nothing and carries no q**, and it is reported as part of the same non-independent set as Q023's locked E1 (Correction 10, now without Q032's C1). `market_regime_daily` therefore stays a **required** table in the successor selection freeze with `created_at` preserved (item 30). | **rule 7** read literally; **DP-29** / rule 8 (the label's statistic belongs to Q023 and confirms nothing here); Correction 10; §4.3 as drafted, which already registers this read and only needed its status raised from cross-check to the rule-7 stratification |
| 27 | `m` and the correction sets, with P2 deferred | DECIDED | **`m = 1` within the question** (P1 alone; BH within the question is trivial and `q = p` there). **F8 = 1** at this lock and never below it. **`A`'s companion correction in F1 = 28** — Q006 2 + Q024 6 + Q025 2 + Q029 16 + Q031's `D1ᴮ` 1 + Q033's `A` 1, the registrar's edited figure, consistent with Q031 DECISIONS #14's 27 plus `A` — and **the larger applicable q is quoted**, which is F1's 28 in every branch, so `m = 1` loosens nothing (item 13 forecast exactly this). **F2 carries no Q033 endpoint while P2 is deferred: 17 → 16** (Q023 2 + Q027 2 + Q029's 10 + Q031 2), the H-062 / Q025 / Q032 precedent that a deferred primary leaves its family set. **`G_μ` is not computed at all** — it is P2's machinery — so §8 clause 8's `G_μ` half and §7's `G_μ` pairing lapse with P2. No locked PREREG records Q033's `V` in its correction set, so **no locked file is edited**. | rule 8; **DP-29**; **Q032 / H-079** bookkeeping (a deferred primary leaves F1 and F2, stated the same day); item 13 |
| 28 | Item 10's one permitted suppression revision, exercised at `record` | DECIDED | **No cell is added, and none is removed. The revision is exercised and closed here.** R1 offers nothing that would add one: the halves project ≈ 52 contributing nights each, the 80–90 band is nearly the whole population, and R1(d)'s `d_L3` finding lands on a tercile panel already suppressed at lock. The **nine `trend_t` × `vol_t` cells and the four stability cells are not "unsuppressed" — they become uncomputable** and leave the reportable set entirely with P2, which is stricter than suppression, not looser. The Steward's six-cell proxy composition (UP/MID 30 of 68, the only cell clearing 20) is **informational and is not written into the file**: it is a bounded proxy for a partition the locked question does not compute. | **DP-21**; **DP-45** (a one-way list; uncomputable is stricter than suppressed); item 10; `STEWARD_Q033_exposure.md` §(c) |
| 29 | Demotion (DP-43's clause), settled at the lock | DECIDED | **Nothing to demote.** The locked question has **no arm**: P1 is a pooled level. Item 9's "neither arm is demotable" resolves as registered — an arm shortfall was never a demotion here but a floor failure for `V`, and `V` is deferred on a prior ground. **No arm is projected below 20 contributing nights at the decision date because no arm is projected at all**, and DP-43's demotion clause is recorded as exercised-and-empty. For P1's reported cells the ≥ 20 **measured** contributing-night floor stands unchanged and is applied at the decision pass, never at the lock. | **DP-43** (demotion settled at lock and never afterwards); **DP-21**; item 9 |
| 30 | R2, rescoped for P1 alone — and which maturity binds now | DECIDED | **Binding maturity stays 40 sessions, so R2's bar horizon is t+40 of the last in-window pick night: daily bars through 2027-06-29, delivered before 2027-07-12 (extension pair: through 2027-08-11 for 2027-08-23).** The t+20 reading was considered and refused: §2.3 registers the 40-session maturity so that **μ's 40-session companion is never right-censored**, and that companion is a §4.3 descriptive read which survives P2's deferral (DP-09, the platform's own swing window); dropping to t+20 would also be the choice that reaches a date ~20 sessions sooner (DP-45). **P1's own clock stays 20 sessions from `X`.** Scope changes: **R2(i) — SPY split-adjusted daily bars from 2025-01-02 — is WITHDRAWN and HELD with P2** and is not built while `V` is deferred (the Q032 rider precedent); if the H-074 trigger is met before 2027-07-12 the history is built for the **successor question**, never folded into a locked Q033. **R2(v)** (`market_regime_daily`, `created_at` preserved) is **upgraded from descriptive cross-check to the rule-7 stratification read** (item 26) and is not optional. **R2(ii), (iii), (iv), (vi), (vii) bind unchanged** — hourly bars stay load-bearing, because §2.3's same-session `U`/`D` tie-break is **P1** machinery (DP-27). The **DP-50(a) cross-freeze guard** stays, now on the candidate and control daily bars generally; its SPY-specific limb lapses with R2(i). The selection freeze is still **one build serving Q027, Q029, Q031 and Q033** (Q032 having left the list). | **DP-23**; **DP-09**; **DP-45** (never the shorter maturity, never the earlier date); **DP-27**; item 5, Correction 1; **Q032 / H-079** (R2 rider withdrawn and held on deferral) |
| 31 | R1(d)'s measured conflation share | DECIDED | **Measured and recorded; nothing moves.** 7 published picks of 550 were excluded by the `d_L3 ∈ [0.25, 10]` bound, and **20 of the 514 valid picks (3.89%, about 1 in 26) carry `d_L3 < 0.5`** — the printed swing target sitting inside the registered ±0.5 ATR direction band. The band stays **0.5 ATR**, the bound stays **[0.25, 10]**, both unmoved in either direction (items 1, 21; §10 threat 6). Two notes for the report: the conflation biases **`V`** toward zero and `V` is deferred, so its bite on the **locked** question is smaller still — P1 measures `a_p` against controls carrying the identical band, and a coincident `L3` does not distort that contrast; and the 3.89% is a **fact about the ladder** (PI-009 / H-053) that the successor P2 question must carry in its own §10 with this measured value. | item 21; **DP-26** (a lock-time convention that does not move at the decision pass); **DP-45**; `STEWARD_Q033_exposure.md` §(d) |
| 32 | R1(e) — the commit sweep and the v1.7 check | DECIDED | **Answer: NONE, and it is recorded as an absence of a schedule rather than a clearance.** HEAD is unchanged at `d19c9a9`; `fa70688` is an ancestor; no commit since it touches the scoring path, the publication gates, the ATR-elite caps, the GEX offset, the scoring enable-flags or the lane-plan writer; and **no v1.7 promotion is scheduled anywhere inside 2026-09-15..2027-08-23**, because the workstream has no calendar anchor and no start. Consequences: **no DP-06 / DP-50(a) split is owed, no `DATA_NOTES.md` entry is owed**, and §12's **DP-50(b) flag-off window runs to 2027-07-12 (2027-08-23 if the extension fires)** — checked before any fix brief is written, and **re-run at R2(vii)** between the freezes. | **DP-50(a)/(b)/(c)**; item 12; Correction 1's dates; `STEWARD_Q033_exposure.md` §(e) |
| 33 | What `DEFERRED.md` must say for P2, and how `V` comes back | DECIDED + ROUTED → registrar | **An endpoint-level entry, on the first admission ground (the objective cannot be measured with the artefacts the desk holds), written by the Registrar at `apply`** — Q033 itself is **not** listed as deferred and no question number is consumed. It must carry: the failing limb named exactly (limb (f), both Alpaca variables unset, probe not attempted); the **second, independent ground** — the rarer-arm gate-counting episode limb at its governing strict reading, **0.0141 < 0.025** (item 23); the **re-entry trigger cited by id, not restated**: the **H-074 trigger shared verbatim with Q030 and Q032** (`DEFERRED.md`, "Q030 / H-074", 2026-09-14 — both keys present in a desk session by direct presence test, **and** a coverage probe returning SPY split-adjusted daily bars from 2025-01-02, feed `sip`, coverage and first/last bar date only; both limbs measured, never assumed), with **no calendar re-check date**, because no amount of waiting produces the bars; **seven things a successor must re-measure** (the §2.2 split on the **true** `close > SMA50 > SMA200` and the **true** ≥ 250-session tercile; the arm-bearing contributing-night rate under §2.5's **complete** rule; the rarer-arm contributing-night rate; the rarer-arm episode rate on a **t+40-matured** basis; the **nine-cell** composition — six only were observable here; the DP-50(a)/(b) sweep and the v1.7 check on the new freeze; and the lock-or-DEFER inequalities re-solved from the calendar against DP-43's ceiling **measured from the successor's own lock date**); and the rule that **`V` returns as a successor question with its own id**, inheriting Q033's definitions verbatim (the partition, the ±0.5 ATR band, the ±10.0 pp MPE, the equivalence NULL clause, the two-CI gate) — **Q033's locked file is never edited to add it back**, because its lock fixes `m`. **Caveat carried forward:** Q033's own 2027-07-12 run prints `α_t`, the raw rates and the §4.3 per-level reads on these nights, so a successor P2 is **post-hoc with respect to them** and runs **prospective-only from its own lock**, with Q033's window as a labelled panel. | ground 3 — bookkeeping with one defensible answer; **H-067 / Q024** ("the arm is a successor question with its own PREREG — never added to Q024, whose lock fixes `m`"), the exact precedent for an endpoint-level deferral; **Q030 / H-074**, **Q032 / H-079** (the trigger, cited by id); rule 3; **DP-45** |

### Corrections found at `record` — eleven through twenty-two

The Registrar applies these at `apply` together with Corrections 1–10. Every one of them follows from
P2's deferral or from R1's measured counts; none weakens a floor, an MPE, a gate or a date.

11. **§7 — the correction sets, with `V` deferred.** **Must read:** `m = 1` within the question;
    **F8 = 1** at this lock and never below it; **`A`'s F1 companion set = 28**; **F2 carries no Q033
    endpoint (17 → 16)** and `V` rejoins only if a successor registers it; the larger applicable q is
    quoted and is F1's in every branch; the `G_μ` / `G` pairing lapses because neither is computed.
12. **§2.5 and §2.4 — the arm clauses that would empty the population.** **Must read:** for P1 a
    contributing night is a non-excluded in-window night with ≥ 3 valid published picks, each with
    ≥ 5 valid matched controls, **matured to t+40**; the "carrying a legal §2.2 arm label" clause and
    the "fewer than 250 prior SPY sessions" exclusion are **struck for this branch** (item 25). Every
    other screen stands verbatim.
13. **§2.2, §4.3, §8, §9 — everything the arm carries goes with P2.** **Must read:** the nine-cell
    composition, the four stability cells, the 80% HOSTILE composition guard, B3, B4's tape-episode
    label permutation, the tape-episode block bootstrap, `G_μ`, §8 clauses 2, 3, 5, 7, 9 and the
    `G_μ` half of clause 8, and every §9 P2 bullet are **not computed and not printed**. Descriptive
    reads registered "per arm" print **pooled and per half**. **The SMA50-only proxy is substituted
    for the arm nowhere** — not in a stratum, not in a panel, not in a sensitivity.
14. **§6 — rule 7 for the surviving primary.** **Must read:** the platform's point-in-time
    `market_regime_daily` label carries the rule-7 stratification for P1 (descriptive, no q, blocks
    nothing, reported with Q023's E1 as one non-independent set), alongside the two halves, which
    block under §8 clause 6 (item 26).
15. **§4.4 — P1's inference is untouched and must be stated as complete on its own.** **Must read:**
    CI-1 = stationary block bootstrap over the ordered contributing nights, expected block length 10,
    with the date-clustered CI alongside; CI-2 = the DP-51 symbol-episode bootstrap; **both must
    clear**, CI-1-clears-CI-2-does-not is INCONCLUSIVE; p by paired sign-flip permutation on `α_t`,
    10,000 permutations, seed 20260914.
16. **§5 and §5.2 — the floors the locked question carries.** **Must read:** floor **A** (≥ 80
    contributing nights) and floor **C** (≥ 30 post-lock, satisfied by construction); **floors B and
    D travel to `DEFERRED.md` with `V`**; window 158 sessions unchanged; floor A binds at session 121
    at the measured 0.6620 and projects **104.6 nights at 158**; the window end is **not** pulled in.
17. **§5.1 — the placeholders are struck, not replaced.** **Must read:** the HOSTILE-share 0.20 row
    and the 3.0-nights-per-episode row are **struck**; the Steward's proxy arm numbers are **not**
    written in as measured exposure for a partition the question no longer computes. The measured
    rows stand as: contributing nights **0.6620** (47/71, t+20-comparable) with **r₄₀ = 0.8710**
    (27/31 sub-period) and **`min` = 0.6620 governing**; full-denominator t+40 0.3803 recorded;
    control-pool depth **min 37** with the ≥ 5 floor costing **zero** nights at both horizons; and
    **`d_L3 < 0.5` in 20 of 514 valid picks (3.89%)**.
18. **§5.3 — R1 is answered and closed; R2 is rescoped.** **Must read:** R1 is satisfied by
    `research/reports/STEWARD_Q033_exposure.md` (all six limbs, cited by section); **R2(i) is
    withdrawn and HELD with P2**; **R2(v) is upgraded to the rule-7 stratification read**; R2(ii)'s
    horizon is **t+40 → daily bars through 2027-06-29** (extension: 2027-08-11); R2(iii), (iv), (vi),
    (vii) bind unchanged; the DP-50(a) guard stays on the candidate and control bars and its
    SPY-specific limb lapses.
19. **§9 and §12 — the flag-off window and the sweep.** **Must read:** DP-50(b) flag-off runs to
    **2027-07-12** (**2027-08-23** if the extension fires); R1(e) returned **NONE** at HEAD `d19c9a9`
    with **no v1.7 promotion scheduled through 2027-08-23**, recorded as an absence of a schedule and
    **re-checked at R2(vii)**; no `DATA_NOTES.md` entry is owed.
20. **§10 — threats 3 and 11.** **Must read:** threat 3 (the rarer arm binds and projects marginal)
    **travels to `DEFERRED.md` with P2** and is struck from the locked question, which has no arm;
    **threat 11 is no longer a threat but a realized event** — the SPY history exists in no pinned
    manifest, it could not be fetched at the lock, and it deferred P2 on the day the question was
    registered. Threat 6 keeps its place and now carries R1(d)'s measured 3.89%.
21. **Header — the successor-freeze sentence.** **Must read:** the pair is a strict superset of the
    freezes **Q027, Q029 and Q031** require (Q032 having been deferred), one build serving all four;
    the **"and SPY split-adjusted daily bars from 2025-01-02" clause is struck** with R2(i); the daily
    horizon reads **t+40 of the last included pick night (2027-06-29; 2027-08-11 on the extension
    path)**, never t+20.
22. **§1, §4.2, §8, §9 — the question now has one primary, and H-081 is answered in half.** **Must
    read:** §1 states in one sentence that P2 is deferred at this lock on the H-074 provisioning
    blocker and that P1 locks alone; §8's question-level rule reads on the **single** primary; and
    **§9's "H-081's PASS" conjunction is struck** — with `V` unmeasured, **no branch of this run may
    be described as H-081 passing or failing**, and the report says so plainly. What P1 can still
    settle on its own is stated as it stands: whether published picks go their own way more often
    than their same-night look-alikes, with the matched-control rate beside it.

**One line for the Red Team, changing nothing here.** F1's companion count carries a live
inconsistency the desk inherited, not one this record creates: `DEFERRED.md` "Q025 / H-068" records
F1 as Q006 2 + Q024 6 = **8** with Q025's two primaries having left the set, while **Q031 §7
(locked)** and the Q032 entry both count Q025's 2 inside F1 (27 before `A` joins). Q033 uses **28**,
the figure consistent with the locked file and the **stricter** of the two (a larger BH set raises
every q). The locked file stands; the discrepancy is flagged for Q031's review, not corrected here.

## Corrections to silent choices

**Ten at `decide`**, plus **twelve found at `record`** (see "Corrections found at `record`" above).
The Registrar applies them at `apply` with the rest of this file. Every one moves a date out,
strikes a false statement or tightens a clause; none weakens a floor, an arm, an MPE or a gate.

1. **§5.2, §5.3 R2, the header and §9 — the decision date is computed on 20 sessions of maturity, and
   the registered population needs 40.** §2.3 fixes binding maturity at 40 sessions, §2.4 excludes a
   night whose t+40 falls after the freeze's last date, and §2.5 defines a contributing night as one
   "matured to t+40" — but §5.2's arithmetic adds **20** sessions to the window end, and §5.3 R2 and
   the header ask for daily bars through "session t+20 of the last included pick night". **Must
   read:** decision date = window end **+ 40 sessions + one calendar week, first Monday on or after**,
   moved out again for a market holiday → 2027-04-30 + 40 sessions = **2027-06-29**, + one week =
   2027-07-06, **Monday 2027-07-12** (not 2027-06-07); extension path 2027-06-14 + 40 sessions =
   **2027-08-11**, + one week = 2027-08-18, **Monday 2027-08-23** (not 2027-07-26), which is the hard
   stop; the successor **price** freeze carries daily bars through **2027-06-29** (extension pair:
   **2027-08-11**); §9's DP-50(b) flag-off becomes **2027-07-12 / 2027-08-23**; and §5.2's "8.8 months
   from the 2026-09-14 lock" becomes **9.9 months**, with the extension at **11.3 months** — both
   inside DP-43's 12-month ceiling of 2027-09-14, with less room than any question on the board except
   Q032. (DP-43, DP-45, DP-23.)
2. **§5.2's holiday list omits 2027-06-18 (Juneteenth observed).** Q018, Q020, Q021, Q023, Q024, Q031,
   Q032 and both Steward exposure reports all list it. **Must read:** the list is 2026-11-26,
   2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05
   and **2027-09-06** (the last for the ceiling back-solve only). The 158-session window count is
   **unaffected** — Juneteenth falls after 2027-04-30 — but every +40-session arithmetic crossing June
   2027 is, and Correction 1's dates are computed with it. The Steward re-confirms every date session
   by session when the freeze is built; a correction may move a date **out, never in**.
3. **§5.3 R1 — the lock-or-DEFER inequalities are back-solved through 20 sessions of maturity.** The
   draft solves the 12-month ceiling (latest decision Monday 2027-09-13) through a one-week margin and
   **20** sessions to 225 admissible elapsed sessions, giving ≥ 0.36 / ≥ 0.09 / ≥ 0.023. At the
   registered **40**-session maturity the same back-solve gives a last admissible window end of
   **2027-07-09** — 2027-07-09 + 40 sessions = 2027-09-03, + one week = 2027-09-10, first Monday =
   2027-09-13 — i.e. **205 admissible elapsed sessions** from 2026-09-15. **Must read:** contributing
   nights **≥ 0.40** per elapsed session; rarer-arm contributing nights **≥ 0.10**; rarer-arm
   gate-counting tape-episodes **≥ 0.025** — the floors 80 / 20 / 5 divided by 205 and rounded **up**,
   **re-solved at `record` from the trading calendar and again if the lock date moves**. Identical to
   Q032 Correction 3: same lock date, same window start, same maturity.
4. **§5.1 — the scheduling rate 0.6620 was measured at t+20 maturity and this question's contributing
   night is defined at t+40.** **Must read:** the scheduling rate is **`min(r₄₀, 0.6620)`** (item 6),
   `r₄₀` measured by R1(a) with numerator and denominator over the same t+40-gradeable sub-period
   under §2.5's complete rule; §5.2's projection table is rebuilt at `record` from R1's measured rates,
   **out only**. §5.1's own note that 0.6620 is preferred to Q032's borrowed 0.9538 stands and is
   correct (DP-45); this correction is about maturity, not about which report was borrowed from.
5. **§2.4 — a false statement, contradicted by §10 threat 6.** The draft says the `d_L3 ∈ [0.25, 10]`
   screen "is also what keeps the direction band strictly inside the magnitude level: a pick whose
   printed L3 sits below 0.5 ATR cannot enter, so `U` is never at or beyond `L3`". The bound admits
   `d_L3` between 0.25 and 0.5. **Must read:** the sentence is struck; the screen is stated as Q027 /
   Q031 state it (a validity bound and nothing more); §10 threat 6's accurate statement governs; and
   the handling is item 21's — R1(d)'s pre-lock count, the printed `(a_p, m_p)` joint distribution and
   within-night correlation, and the `d_L3`-tercile panel as counts. The bound is **not** raised to
   0.5 (DP-45: the conflation runs against the hypothesis).
6. **§4.3 — the per-level L1…L6 reads run on lane windows out to 60 sessions while maturity binds at
   40.** "each level's own lane window" includes the long lane's 60 sessions, which no in-window night
   will have. **Must read:** every descriptive read beyond t+40 (the long-lane L5 / L6 first-touch
   rates and their sessions-to-touch) prints its **matured-night count** beside it and its
   right-censored rows are **counted, never graded as non-touches** — §2.4's own rule, applied to the
   descriptive panel. No endpoint and no blocker depends on a bar after t+40.
7. **§5.3 R1 has no SPY-history feasibility limb.** **Must read:** add **R1(f)** — `ALPACA_API_KEY` /
   `ALPACA_SECRET_KEY` presence in the desk session and a coverage probe for SPY split-adjusted daily
   bars from **2025-01-02** (coverage and first / last bar date only) — as a **limb of the lock gate**,
   with item 16's branch: a failed probe with no pinned alternative **defers P2 at this lock** (entered
   in `DEFERRED.md` with the H-074 re-check trigger) and **P1 locks alone**. R2(i)'s decision-pass
   version of the same failure stays in force as the second net. (Q030 / H-074; Q032 #12.)
8. **The draft registers no `eval.py` commit deadline.** **Must read:** written once (rule 9) and
   **committed no later than Monday 2027-04-05**, sha256 recorded, not touched afterwards; the
   extension run uses the byte-identical file. Q027 and Q029 decide **2027-04-12** on this window, this
   freeze, this entry and this clock, and Q032 decides ≈ 2027-06-28 printing the same statistic as
   `G_μ` on the same nights.
9. **The header's "strict superset of the successor freezes Q027, Q031 and Q032 require" is true only
   as of this lock, and only after Correction 1.** Q032's own window end is provisional and may move
   **out** at its `record`. **Must read:** the Steward builds the selection freeze **once** and serves
   all four questions from it where the calendar permits; each question's **price** freeze is built to
   its own horizon and delivered before its own decision date; Q027's, Q029's and Q031's earlier pins
   are unaffected and are **not** edited (DP-22, rule 3). (Q032 Correction 5, same words.)
10. **§4.3's `market_regime_daily` cross-check names Q023's E1 and Q032's C1 — and Q032's C1 is itself
    corrected jointly with Q023's E1.** **Must read:** the platform-label read in §4.3 defines no arm,
    blocks nothing, carries **no q of its own**, and is reported as part of the **same
    non-independent pair** as Q023's E1 and Q032's C1 — three prints of one statistic on
    heavily-overlapping populations, none of which may ever be read as confirming another. (DP-29,
    rule 8; Q032 DECISIONS #1.)

Checked and **not** corrections — each already matches the policy: entry the **session t+1
regular-session open** for picks and matched controls alike, with **DP-11 correctly not fired**
(nothing here is a position already held) and the `C_t` basis a printed sensitivity that never decides
(**DP-03(b)**, **DP-42**); **L3 = `lane_plans.swing_trading.targets[0]` on the DP-09 20-session
clock** for both series, the platform's 40-session swing window descriptive (**DP-09**, **DP-42**); a
level at or through `X` at the t+1 open scored **not a hit** with the pick kept in the denominator and
the not-takeable count printed per arm (**DP-26**, rule 5); **no stop assumed anywhere**,
counter-direction touches and MAE / MFE reported and never used as exits, **DP-30** not engaged
(**DP-02**); an unorderable same-session race scored **counter-first** (**DP-27**); published =
**`qualified IS TRUE AND selected_rank IS NOT NULL`**, dark-lane rows never in the treatment arm and
only in the control pool (**DP-28**); the B1 control construction **Q006 §3 verbatim**, controls never
adding to inferential n, a pick with < 5 valid controls dropped and counted and never imputed (rule 6,
rule 5); floors read as **80 contributing nights per primary endpoint and 20 per arm and per reported
cell**, the stricter reading, never lowered (**DP-21**); **≥ 30 contributing nights after the lock
commit**, satisfied by construction, so **DP-31 correctly does not apply** and no successor
replication question is owed (**DP-24**); one automatic extension of +30 sessions then DEFERRED, fired
on `eval.py`'s **measured** counts, with a gate shortfall never an INCONCLUSIVE verdict (**DP-13**);
window entirely after the 2026-06-01 catalyst fix, the 2026-07-06 ladder ship and the 2026-07-08
`publication_floor` ship, so no **DP-06** / **DP-50(a)** split falls inside it, and the sealed panel
split at 2026-07-06 (**DP-06**); the **units** taken from H-081 as filed — percentage points on each
excess, ±5.0 pp — and not re-united (**DP-25**), with the path form of the direction endpoint
registered because rule 5 / **DP-01** forbid a fixed-horizon sign deciding a verdict and the filed
20-session sign printed beside it as a named descriptive companion; successor freezes covering **every
candidate symbol, published and unpublished** (**DP-23**); **two CIs per primary**, CI-1 (stationary
block / tape-episode block) and the **DP-51** symbol-episode bootstrap, with CI-1-clears-CI-2-does-not
**INCONCLUSIVE, never CONFIRMED**, and the three units given three names (**DP-51**, §2.5, §8 clause
10); Registrar conventions fixed before any outcome exists — the SMA50 / SMA200 / 20-session-vol cuts,
the expanding-window terciles with the ≥ 250-session requirement, the BENIGN definition, the 80%
HOSTILE composition guard, the 10-session block length, seed 20260914, the session-index half split,
the 25%-ungradeable night rule (**DP-26**), none promotable at the decision pass; no MPE anywhere in
session or money units (**DP-44**); the exposure counts taken from the **pinned freeze** and the
read-only repo, never a live query (**DP-50(c)**); every number **NON_QUOTABLE** on a 20- and
40-session basis (rule 12) and nothing subscriber-facing before PROSPECTIVELY_CONFIRMED (rule 10);
`uoa_symbol_daily.fwd_return_*` banned and no UOA table read (FREEZE_v001 §5);
`sas_selection_excursion` / `outcome_*` / `level_hit_*` never inputs; and **no rule-14 exception
requested or needed** (**DP-05** untouched, **DP-41** respected).

## Defaulted on Haci's behalf

- #16 The SPY history the arm needs, and when its absence is discovered — chose **probe it at the lock
  and defer P2 today if it cannot be fetched, with P1 locking alone**; not taken: discover it at the
  2027 decision pass — costs the window — DP-43. Overturn = successor question.
- #17 Window start — chose **prospective-only, pick nights ≥ 2026-09-15, sealed stretch as a labelled
  panel**; not taken: read the sealed nights — decides now, not blind — DP-43. Overturn = successor
  question.
- #18 Window end, decision date and hard stop — chose **2026-09-15 .. 2027-04-30, decision Monday
  2027-07-12, extension to 2027-06-14 decided Monday 2027-08-23**; not taken: the draft's 2027-06-07 on
  20-session maturity — five weeks sooner, wrong clock — DP-43. Overturn = successor question.
- #22 The branch, on R1's measured limbs — chose **defer P2 (`V`) at the lock on the absent SPY
  history and lock P1 (`A`) alone, `m = 1`**; not taken: defer Q033 whole — P1 is measurable —
  DP-43. Overturn = successor question.
- #24 The final window and dates — chose **158 sessions to 2027-04-30, decision Monday 2027-07-12,
  extension to 2027-06-14 decided Monday 2027-08-23**; not taken: pull the window end in to session
  121 — sooner, shorter — DP-43. Overturn = successor question.

**What #22 and #24 cost him, in one paragraph.** #22 gives up the half of H-081 that Haci's own line
is about — whether *target* attainment is the tape-conditional half while *direction* is not — and
keeps the half that needs no tape label at all. It is not a judgement about the hypothesis: two
environment variables are missing from the desk's session, the same two that deferred Q030 and Q032
today, and the desk may not look for or request any other credential (rule 1). Provisioning them is
his call and it re-opens all three questions in registration order. #24 asks him to wait to
**2027-07-12**, five weeks longer than the draft advertised and five to six weeks longer than the
Steward's informational note would allow — the extra weeks are the registered t+40 maturity and a
refusal to re-cut the window on a proxy measurement of a partition this question no longer computes.

**Three items, and all three are one cost: waiting, plus one particular risk inside it.** Q033 asks
Haci to wait **just under ten months**, five weeks longer than the draft advertised, and the extra five
weeks are not caution — they are arithmetic: a contributing night here needs t+40 bars and the draft
scheduled on t+20, and its holiday list was missing a session. The risk worth seeing is the same one
Q032 carries: the most likely stopping point for **P2** is not its own result but a **provisioning
failure**, because §2.2's arm cannot be assigned without SPY daily bars back to 2025-01-02, which sit
in no pinned manifest and which the desk last failed to fetch when Q030 was deferred for absent Alpaca
credentials. That is why #16 pulls the probe forward — a P2 deferred today costs nothing, a P2 deferred
in July 2027 costs the window — and why the P1 half is deliberately built to survive it: **"do
published picks go their own way more often than their look-alikes?" needs no regime label at all.**
Nothing else was defaulted: items 1–15 and 21 each met a DECIDE ground, and none of them is a question
about how he trades — the entry, the clock, the level and the lane come from DP-03 / DP-09 / DP-42 as
already locked in Q002–Q032, the direction band is a measurement device rather than a trade
(**DP-26**), and the one MPE that is not a DP number is a stated application of DP-20's larger-MPE
clause in the shape five locked questions already use.

## Routed requests

### data-steward — R1 (counts only) — **ANSWERED AND CLOSED 2026-09-14**

**Delivered:** `research/reports/STEWARD_Q033_exposure.md`, all six limbs, counts only, frozen data,
no live query. **Read at `record`:** limb (a) **PASS** (0.6620 per elapsed session against 0.40, cap
binding on r₄₀ = 0.8710); limbs (b) and (d)'s rarer-arm forms **gate P2 only** and travel with it
(item 23), with the strict t+40-matured episode reading **0.0141 — SHORT** recorded as `V`'s second
deferral ground; limb (c) six-cell proxy composition informational, no suppression change (item 28);
limb (d)'s ladder counts recorded (7 excluded by the bound; 20 of 514 valid picks at `d_L3 < 0.5`,
3.89% — item 31); limb (e) **NONE**, HEAD `d19c9a9`, no v1.7 through 2027-08-23 (item 32); limb (f)
**FAIL — credentials absent, probe not attempted**, which fired item 16's branch (item 22). **No
re-run is requested and nothing further is owed on R1.** The original request is preserved below as
the record of what was asked before the counts existed.

Q033 (does VolatilX get the direction right more reliably than the distance — PREREG §5.3 request R1)
needs a **counts-only** exposure measurement on the **frozen** data —
`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json` against
`research/data/exclusions_v003.json`, plus read-only `git log` / `git show` in the platform repo — and
**never a live query** (DP-50(c)). It is **blocking for the lock**: Q033's binding floor is the
**rarer arm's** 20 contributing nights on a bar-only tape partition no desk report has ever counted,
and §5.1's rarer-arm rate is a placeholder borrowed from the platform's *label*, a different variable.
**No outcome of any kind:** no touch, no first-touch date, no return, no excursion, no `outcome_*`
column, no `sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`, and no arm-versus-outcome
cross-tab of any shape; forward bars may be read **only** to establish that a bar exists (gradeability
and maturity accounting), never for a value. Period: pick nights **2026-06-01..2026-09-10** (DP-06's
segment; the arm is a 16:05 property with no outcome attached, so the widest legal span is used);
**denominator for every rate = elapsed sessions** (calendar sessions minus holidays, exclusions *not*
pre-removed — the Q019 / Q022 / Q023 / Q027 / Q031 / Q032 convention), with nights in
`exclusions_v003` and DP-04 late-`finished_at` nights removed from the numerator, plus the
`payload_disabled_runs` signature you identified for Q027 (2026-04-01, 2026-05-01, 2026-06-02,
2026-07-02). Please return, by month and for the period as a whole: **(a) the §2.4 funnel and the
contributing-night rate under §2.5's complete rule** — a non-excluded night carrying a legal §2.2 arm
label and **≥ 3 valid published picks** (DP-28's predicate, after the null-ladder, wrong-side /
non-monotone, split-scale, `d_L3 ∈ [0.25, 10]` and ≥ 60-prior-bar screens), **each with ≥ 5 valid
matched controls** — i.e. the series-B rule your `STEWARD_Q031_exposure.md` §(a) counted 47/71 =
0.6620 under, confirmed as that rule or corrected as a correction; reported **three ways**: (i) the
rate with numerator and denominator both counted over the **maximal sub-period whose nights can be
graded to t+40** on `manifest_prices_v001` (please state that sub-period's last pick night, derived
from the calendar), (ii) the same rule at **t+20** maturity for comparability with your 0.6620, and
(iii) the full-denominator t+40 rate for the record; **the schedule is built on `min` of (i) and
0.6620** (DECISIONS item 6), so a rate faster than 0.6620 changes no date. **(b) The §2.2 arm split
under the SMA50-only trend variant** (`UP` iff `close_t > SMA50_t`; `vol_t` by expanding-window
terciles of 20-session annualised realised SPY vol over every SPY session in the freeze dated ≤ t):
nights per arm over all elapsed sessions, **stating explicitly which arm is the rarer one**, and
**gate-counting tape-episodes per arm** (a maximal run of consecutive sessions carrying the same arm
label; an excluded or unlabelled session does **not** break a run; an episode counts only if it
contains ≥ 1 contributing night) with their length distributions and contributing nights per episode —
carrying with each count the bound direction that applies to it (SMA50-only HOSTILE is a **lower**
bound on true HOSTILE, SMA50-only BENIGN an **upper** bound on true BENIGN, because adding
`SMA50 > SMA200` can only move nights out of `UP`). **(c) The nine-cell `trend_t` × `vol_t`
composition** under the same variant, and **the first session at which SPY has ≥ 250 prior sessions in
the freeze**. **(d) Two counts on the published slate: the number of picks excluded by the
`d_L3 ∈ [0.25, 10]` validity bound, and — separately, as a share of otherwise-eligible picks — the
number with `d_L3 < 0.5`**, i.e. how often the printed swing target sits inside Q033's registered ±0.5
ATR direction band; this is the direct read on whether the direction endpoint and the magnitude
endpoint are the same test (§10 threat 6), and it is reported at the lock rather than discovered at the
decision pass. **(e) The DP-50(a)/(b) commit sweep** since manifest SHA `fa70688` — any change to the
SAS weights, timeframe multipliers, `qualification_threshold`, `publication_floor`,
`bear_publish_threshold`, `max_output_cap`, `min_completeness`, the ATR-elite caps, the GEX offset, the
scoring enable-flags or the lane-plan writer — **with an explicit answer even when it is "none"**, plus
whether the **v1.7** scoring workstream is scheduled to ship inside 2026-09-15..2027-08-23. **(f) A
SPY-history feasibility probe, which is a limb of the lock gate** (DECISIONS item 16, the Q030 / H-074
blocker): whether `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` are present in the desk session and whether
SPY split-adjusted daily bars **from 2025-01-02** can be retrieved — coverage and first / last bar date
only, no values needed beyond that. **If `STEWARD_Q032_exposure.md` already answers (b), (c) and (f)
under the identical definitions at lock time, please cite it rather than re-run them**; (a), (d) and
(e) are this question's own — note that (a)'s funnel is **stricter than Q032's** (≥ 3 picks and ≥ 5
controls, against Q032's ≥ 1 and ≥ 3), so its rate must be measured on Q033's rule and not borrowed.
**The call this request decides**, with every branch fixed before your counts are seen: contributing
nights **≥ 0.40** per elapsed session, rarer-arm contributing nights **≥ 0.10**, rarer-arm
gate-counting tape-episodes **≥ 0.025** — the floors (80 / 20 / 5) divided by the **≈ 205** elapsed
sessions still admissible under DP-43's 12-month ceiling at a 2026-09-14 lock with **40** sessions of
maturity and a one-week freeze margin (latest admissible decision Monday 2027-09-13, back-solving to a
window end of ≈ 2027-07-09), rounded up, and please **re-solve them from the trading calendar** rather
than taking my arithmetic — the holiday list used here is 2026-11-26, 2026-12-25, 2027-01-01,
2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05 and 2027-09-06. All three
floor limbs clear → **Q033 locks**, with the window end set to the **latest** of floor A (80
contributing nights per primary), floor B (20 rarer-arm contributing nights), floor C (30 post-lock
nights, satisfied by construction) and floor D (5 gate-counting tape-episodes per arm) at your measured
rates, and every date moved **out** if those rates are slower than §5.1's placeholders, never in. Any
floor limb short → **Q033 goes to `research/questions/DEFERRED.md`** with the measured counts and the
re-check trigger "the Steward measures ≥ 0.10 rarer-arm contributing nights per elapsed session over a
trailing quarter", and it is **not** re-registered on a weaker partition — a different partition is a
different question with its own id. **Limb (f) short → P2 only is deferred** (with the H-074
credentials trigger) and **P1 locks alone**; the partition is never re-specified to SMA50-only after
the fact. Please also state **the projected date each floor is first reached** at each measured rate,
on **40** sessions of maturity plus a one-week freeze margin, and flag any §4.3 sub-cell projecting
below 20 contributing nights at that date (the suppression list may only gain cells at `record`, never
lose them — DECISIONS item 10). Report to `research/reports/STEWARD_Q033_exposure.md`.

### data-steward — R2 (successor freezes) — **OPEN, rescoped at `record`; dates now fixed; due before 2027-07-12, not a blocker for lock**

**Amendment, 2026-09-14 — paste this in front of the request below; where the two disagree, this
governs.** Q033 locks with **P1 (`A`) alone**; **P2 (`V`) is deferred at the lock** on the H-074
provisioning blocker. Four changes and nothing else. **(1) Scope item (i) — SPY split-adjusted daily
bars from 2025-01-02 — is WITHDRAWN and HELD.** Do not build it for Q033: §2.2's arm is not computed
by this question in any form, and the SMA50-only proxy is never substituted for it. If the H-074
trigger is met (`DEFERRED.md`, "Q030 / H-074") the SPY history is built for the **successor question
that carries `V`**, never folded into Q033, whose lock fixes `m = 1`. The **DP-50(a) cross-freeze
guard stays**, now on the candidate and control daily bars generally; its SPY-specific limb lapses
with (i). **(2) Scope item (v) is upgraded, not optional:** `market_regime_daily` with `created_at`
preserved now carries **rule 7's stratification** for P1 (descriptive, no q, blocks nothing) rather
than a cross-check. **(3) The dates are no longer provisional and are fixed out:** pick nights
**2026-09-15 .. 2027-04-30** (158 sessions), **daily bars through session t+40 of the last included
pick night = 2027-06-29**, delivered before the **2027-07-12** decision date; on the extension path
only, a second pair to pick nights **2027-06-14** with daily bars through **2027-08-11**, for
**2027-08-23**, built then and not before. A correction may move a date **out, never in**. **(4) The
shared build now serves Q027, Q029, Q031 and Q033** — Q032 was deferred 2026-09-14 and its rider is
withdrawn; Q033's pair remains the superset on horizon (t+40 against their t+20) and its own price
freeze is built to that horizon. Everything else — (ii) the every-candidate-symbol daily list with
≥ 60 prior sessions, (iii) hourly bars (**still load-bearing: §2.3's same-session `U`/`D` tie-break
is P1 machinery, DP-27 — state their coverage explicitly**), (vi) the add-only successor exclusions
file on the identical four criteria, (vii) the repeated commit sweep with an explicit answer even
when it is "none" — binds exactly as written below.

Q033 (PREREG §5.3 request R2, DP-23) needs successor freezes before its decision pass; **the dates
below are superseded by the amendment above and may only ever move out** (DP-43, DP-45). Please build and pin
a successor **selection** freeze (the same SQL and the same exclusion criteria as v001, over
`sas_candidates` for **every candidate row, published and unpublished**, plus `sas_runs` and
`market_regime_daily`) and a successor **price** freeze (`prices_daily_split`, `prices_daily_raw`,
`prices_hourly_raw`), covering pick nights **2026-09-15 .. 2027-04-30** (the window end fixed at
`record`, out only) with **≥ 60 prior sessions before 2026-09-15**; and — only if the single DP-13
extension fires — a second pair covering pick nights **.. 2027-06-14**, built then and not before.
**This pair is a superset of the ones requested for Q027, Q029, Q031 and Q032** (identical population
and start, longer horizon), so please build the selection freeze **once** and serve all of them from it
where the calendar permits; their own pins are unaffected and are not edited. Seven scope
requirements, none optional: **(i) SPY split-adjusted daily bars from 2025-01-02** through the freeze
end — without them §2.2's `SMA200` and its 250-session volatility tercile do not exist and **no arm can
be assigned**; if the extended SPY history cannot be obtained (the Q030 / H-074 provisioning blocker),
**P2 is DEFERRED on that ground and P1 is reported alone**, and the partition is **never**
re-specified to SMA50-only after the fact, because that is a different arm chosen after the data
existed. **(ii)** The daily bar horizon runs to **session t+40 of the last included pick night** — not
t+20 (DECISIONS Correction 1: Q033's contributing night is defined at t+40) — i.e. daily bars through
**2027-06-29**, delivered before the **2027-07-12** decision date; on the extension path, through
**2027-08-11** for a **2027-08-23** decision. **(iii)** The daily symbol list covers **every candidate
symbol on every in-window night, published and unpublished**, with ≥ 60 prior sessions before
2026-09-15 (the matched controls need their closes, `beta60`, `atr_pct`, `runup20` and forward bars),
never assumed from an earlier freeze's symbol list. **(iv)** Hourly bars scoped to at least the
published-pick symbols — here they are **not** purely descriptive: §2.3's same-session `U` / `D`
ordering tie-break reads them, and a pair they cannot order is scored counter-first (DP-27), so please
state their coverage explicitly. **(v)** `market_regime_daily` included with `created_at` preserved,
for the §4.3 descriptive cross-check only. **(vi)** An **add-only successor exclusions file** applying
the identical four criteria (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`,
`payload_disabled_runs`) to post-2026-09-10 nights — it may add nights and may never remove one from a
v003 list, and its header should state whether the `analysis_status = "disabled"` / no-`lane_plans`
signature is still present and still a first-published-night-of-the-month pattern, saying so explicitly
rather than silently returning an empty list. **(vii)** Rows whose bars are missing are **excluded and
counted, never back-filled or imputed**, and R1(e)'s commit sweep is repeated for the period between
the freezes with a dated `DATA_NOTES.md` entry for any repair that rewrites historical rows and an
explicit answer **even when it is "none"**. **The DP-50(a) guard is load-bearing on SPY specifically:**
where the successor freeze overlaps an earlier one on SPY's daily bars, the rows are compared and
`eval.py` **fails loudly** on any disagreement — SPY's history is P2's conditioning variable, so a
vendor restatement would silently re-run the experiment. Please re-confirm every §5.2 date **session by
session from the trading calendar** when the freeze is built; the holiday list is 2026-11-26,
2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05 and
2027-09-06. A correction to any date may move it **out, never in**.

### registrar — write P2's `DEFERRED.md` entry at `apply` (item 33)

Q033 locks with **P1 alone**; **P2 (`V = G_μ − G_α`) is deferred at the lock** and needs an
**endpoint-level** entry in `research/questions/DEFERRED.md`, on that file's **first** admission
ground (the objective cannot be measured with the artefacts the desk holds), written the way the
"H-067 (arm only)" entry is written for Q024 — **Q033 itself is not listed as deferred, no question
number is consumed, and `state.json` goes to `PREREG_LOCKED`, not `DEFERRED`**. The entry must carry,
in this order: **what the endpoint is and why it is worth keeping** (H-081's own half — whether
target attainment is the tape-conditional part of the claim while direction is not — with the
`MAGNITUDE_IS_THE_CONDITIONAL_ONE` / `BOTH_CONDITIONAL` / `BOTH_MOVE_TOGETHER` labels, the ±10.0 pp
MPE and the two-CI gate recorded as designed and standing); **the failing limb named exactly** —
PREREG §5.3 R1 limb (f) / DECISIONS item 16, `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` both unset in
the desk session by direct presence test, **no retrieval attempted** (rule 1 forbids looking for any
other credential), `STEWARD_Q033_exposure.md` §(f), the same blocker, the same two variables and the
same session as Q030 / H-074 and Q032 / H-079 on the same day; **the second, independent ground** —
the rarer-arm gate-counting tape-episode limb at its governing strict full-window t+40-matured
reading, **1/71 = 0.0141 against a floor of 0.025** (DECISIONS item 23), with the other two readings
(0.0323 sub-period-restricted, 0.0563 eligible-pick basis) recorded and explicitly **not** adopted;
**the counted limbs, for the re-check and nothing else**, every one of them on the SMA50-only
one-sided bound that is **not** §2.2-legal (HOSTILE 22 of 68 nights, 8 episodes, six-cell
composition, first session with ≥ 250 prior SPY sessions = **never** in this freeze — 153 bars,
133 computable rvol20 observations); **what was considered and rejected** (re-specifying the
partition to SMA50-only — never, inside this question or any successor edit of it; locking P2 and
probing at the decision pass — the cost is the whole window; DP-13's extension — it produces no SPY
bars); **the re-entry trigger cited by id, not restated** — the **H-074 trigger shared verbatim with
Q030 and Q032** (`DEFERRED.md`, "Q030 / H-074", 2026-09-14: both keys present in a desk session,
stated by the Steward with a direct presence test, **and** a coverage probe that returns SPY
split-adjusted daily bars from **2025-01-02**, feed `sip`, coverage and first/last bar date only,
market-data endpoints only; both limbs measured, never assumed), with **no calendar re-check date**,
because no amount of waiting produces the bars, and with the note that satisfying that one trigger
re-opens Q030, Q032's successor and this endpoint **in registration order**; **the seven things a
successor must re-measure before it may lock** (the §2.2 split on the **true** `close > SMA50 >
SMA200` trend and the **true** ≥ 250-session volatility tercile; the arm-bearing contributing-night
rate under §2.5's complete rule; the rarer-arm contributing-night rate; the rarer-arm episode rate on
a **t+40-matured** basis; the **nine-cell** composition, of which only six were observable here; the
DP-50(a)/(b) sweep and the v1.7 check on the new freeze; and the lock-or-DEFER inequalities re-solved
from the trading calendar against DP-43's 12-month ceiling **measured from the successor's own lock
date**, which tighten as that date moves later); and **how `V` comes back** — as a **successor
question with its own id**, inheriting Q033's definitions verbatim (the partition, the ±0.5 ATR band,
the ±10.0 pp MPE, the equivalence NULL clause, the DP-51 two-CI gate, the 80% composition guard),
**never by editing Q033**, whose lock fixes `m = 1` (the H-067 / Q024 precedent, rule 3). Close with
the **bookkeeping**: no verdict of any kind was produced for P2 and **no outcome was read** — the
Steward's report is counts of nights, picks, controls and bars on the pinned freeze, reading a
forward bar only to establish that a bar exists; **F2 falls 17 → 16** and **F8 = 1**, while **F1
stays 28** with `A`; no locked PREREG records `V`, so **no locked file is edited**; `research/
BACKLOG.md` marks **H-081 — registered as Q033 (P1 only); the interaction half deferred, SPY
history needs Alpaca credentials in the desk session**; and the **caveat carried forward** — Q033's
own 2027-07-12 run prints `α_t`, the raw rates and the §4.3 per-level reads on these nights, so a
successor carrying `V` is **post-hoc with respect to them** and runs **prospective-only from its own
lock**, with Q033's window as a labelled panel. Under that file's preamble nothing in the entry may
be reported, briefed or quoted until the trigger is met.

## Schedule

**FINAL — settled at `record` on `STEWARD_Q033_exposure.md` (R1).** Every rate below is measured on
Q033's own funnel; no placeholder survives. The scheduling rate is item 6's cap,
`min(r₄₀ = 0.8710, 0.6620) = 0.6620`. Dates may move **out** and never in (DP-43, DP-45).

decision_date: **2027-07-12** (Monday) · extension_date: **2027-08-23** (Monday — DP-13's single
automatic extension of +30 sessions; then DEFERRED, there is no second pass) · hard_stop:
**2027-08-23** · rule: **exposure-driven**

- **scope:** **P1 (`A`) only.** P2 (`V`) is **deferred at this lock** (item 22) and carries no date;
  its re-entry is a measurement, not a calendar event (item 33).
- **window:** pick nights **2026-09-15 .. 2027-04-30** = **158 elapsed sessions**; extended window
  .. **2027-06-14** = 188 sessions · **extended: false**
- **halves:** Half A = sessions 1–79 = 2026-09-15..2027-01-06; Half B = sessions 80–158 =
  2027-01-07..2027-04-30 — fixed by session index at this lock and re-derived from the calendar;
  re-cut by the same rule on the extended window (Half A = 1–94, Half B = 95–188).
- **binding floor:** **A** — ≥ 80 contributing nights for the single primary (DP-21), at the
  **measured** 0.6620/elapsed session → `ceil(80 / 0.6620)` = session **121**, projecting **104.6**
  nights at session 158 (31% headroom). Floor **C** (DP-24, ≥ 30 post-lock nights) binds at session
  **46** and is satisfied by construction. **Floors B and D no longer belong to this question** —
  both are arm floors for `V` and travel to `DEFERRED.md` with it (items 22, 23). **The window end is
  not pulled back to 121**: a shorter window is never chosen to reach a date sooner, and the
  informational HOSTILE-richness reading that would allow it is a bounded proxy for a partition this
  question does not compute (DP-43, DP-45).
- **decision date arithmetic:** window end **+ 40 sessions maturity** (§2.3 / §2.5, Correction 1)
  **+ one calendar week** freeze margin, first Monday on or after, moved out again for a market
  holiday. 2027-04-30 + 40 sessions = **2027-06-29** (on the corrected calendar, Correction 2), + one
  week = 2027-07-06, first Monday on or after = **Monday 2027-07-12**. Extension: 2027-06-14 + 40
  sessions = **2027-08-11**, + one week = 2027-08-18, first Monday = **Monday 2027-08-23**.
- **maturity:** **40 sessions**, uniform across every eligible pick and every matched control —
  unchanged by P2's deferral, because μ's 40-session companion is a surviving §4.3 descriptive read
  and because t+20 is the option that would reach a date sooner (item 30, DP-45). P1's own clock is
  **20 sessions from `X`** (DP-09). **R2's daily bar horizon binds at t+40: 2027-06-29** (extension
  path: **2027-08-11**).
- **gates, all on `eval.py`'s measured counts and none reduced:** ≥ 80 contributing nights for P1;
  ≥ 30 dated after the lock commit; ≥ 20 measured contributing nights for any reported sub-cell;
  ≥ 5 valid matched controls per pick; ≥ 3 valid published picks per contributing night; ≤ 25%
  ungradeable picks per night. **The ≥ 20-per-arm and ≥ 5-episodes-per-arm gates are P2's and are
  not carried here** (§8 clauses 1 and 2 mark both "(P2 only)").
- **ceiling:** DP-43's 12 months from a 2026-09-14 lock = **2027-09-14**. 2027-07-12 is **9.9 months**,
  2027-08-23 is **11.3 months** — both inside, on the measured rates, so **the DEFERRED-on-ceiling
  route is not taken**. Less room than any question on the board now that Q032 has left it.
- **lock-or-DEFER gate: CLOSED, on R1.** Re-solved by the Steward from the trading calendar against
  205 admissible elapsed sessions (Correction 3) and read at the file's stricter rounded-up numbers.
  **Limb (a): 0.6620 ≥ 0.40 — PASS**, and it is the only limb that gates P1. **Limb (f): FAIL** —
  both Alpaca variables unset, probe not attempted → **P2 deferred, P1 locks alone** (item 16's
  registered branch). The rarer-arm limbs (≥ 0.10 nights, ≥ 0.025 episodes) gate P2's floors B and D
  and travel with it; their governing strict reading, **0.0141 < 0.025**, is recorded as `V`'s second
  deferral ground (item 23). **Q033 locks.**
- **`eval.py` deadline: committed no later than Monday 2027-04-05, sha256 recorded, not touched
  afterwards** (item 14) — **unchanged, and it does not move out**: Q027 and Q029 still decide
  **2027-04-12** on this window, this freeze, this entry and this clock, and a script written after
  that pass is written with part of its own answer in view. (Item 14's second reason — Q032 printing
  `G_μ`'s twin ≈ 2027-06-28 — lapses with Q032's deferral; the deadline stands on the first.) The
  extension run uses the byte-identical, unmodified file.
- **pin_at_decision: true** — every night carrying a verdict postdates every existing manifest, so
  DATASET_PINNED runs at the decision date on R2's successor freezes (DP-23).

## Standing rules added

_none, at `decide` and at `record` alike._ Nothing here is Haci's word: items 16, 17, 18 and — at
`record` — **22 and 24** were **DEFAULTED** under DP-43 / DP-45, and a DEFAULTED item adds **no** DP
entry (DP-40). `research/DECISION_POLICY.md` is not edited by this run. The rest are applications of DP-01, DP-02, DP-03, DP-04,
DP-06, DP-09, DP-13, DP-20, DP-21, DP-22, DP-23, DP-24, DP-25, DP-26, DP-27, DP-28, DP-29, DP-42,
DP-43, DP-44, DP-45, DP-50, DP-51 and locked precedent (Q006, Q023, Q027, Q029, Q031), plus Q032's
same-day decisions on the shared partition and the shared freeze.

## Standing rules proposed

- **NULL needs a precise interval, not merely one that contains zero.** Q033 item 3 registers the
  equivalence reading: NULL requires the point estimate inside ±MPE **and both CIs entirely inside
  ±MPE**; otherwise INCONCLUSIVE. The house pattern (Q002, Q006, Q024) lets "no difference" be declared
  from an interval that excludes nothing, which on a triple difference is a real hazard. The rule is
  one-way — it can only make a NULL harder, never a CONFIRMED easier — and would generalise to every
  endpoint whose CI can be wider than its MPE.
- **A question's decision date is computed on the maturity its *contributing-night* definition
  requires, not on its primary's clock.** Second question in a row (Q032, then Q033) registering a
  20-session endpoint with a 40-session binding maturity and then scheduling on 20. Where the two
  differ, the later governs the decision date, the freeze's bar horizon and the DP-50(b) flag-off
  window — DP-43's phrase "the endpoint's maturity window" should be read that way.
- **The trading-calendar holiday list belongs in one place.** Q033's §5.2 omitted 2027-06-18 while
  eight other questions list it, and the omission shortened a schedule by a session. A single
  desk-level holiday list, cited by every PREREG rather than retyped in each, removes the whole class.
- **A provisioning limb belongs in the lock gate whenever a question's arm, population or level
  depends on data no pinned manifest holds** — and where only *one* endpoint depends on it, the limb
  defers **that endpoint**, not the question. Q030 was deferred for absent Alpaca credentials after its
  freeze was attempted; Q032 and Q033 both need SPY history nobody has fetched, and Q033's P1 does not.
- **A conflation that biases an interaction toward zero is left in place and measured, not screened
  out.** Q033 item 21: where `d_L3 < 0.5` the direction and magnitude indicators coincide and `V`
  shrinks. Tightening the screen would have been the option that makes a positive easier; measuring the
  share before the lock and printing the joint distribution after is the one that does not. **Measured
  at `record`: 3.89% (20 of 514 valid picks).**

Added at `record`, from the branch this question actually took:

- **A gate limb gates the endpoint it was sized for.** Where a lock gate carries limbs specific to one
  primary's arms and that primary is deferred at the lock, the limb **travels with the deferred
  endpoint** rather than deferring the surviving one (Q033 item 23). The converse — deferring a pooled
  endpoint with 31% headroom on its own limb because an arm-contrast endpoint's episode supply is thin
  — deletes answerable questions. The safeguard is that the limb is never simply dropped: it is
  recorded at its **strictest** reading and listed among what a successor must re-measure.
- **An exposure limb the freeze's own horizon cannot supply is read at its strictest, and re-measured,
  never argued away.** Second question in two days (Q032, then Q033) where a rarer-arm episode count
  is short only because maturity consumes the first 40 of 71 sessions. The censoring-removal licence
  belongs to a **rate**, whose denominator a successor freeze can guarantee, not to an **episode
  count**, whose supply it cannot. DP-45 read literally gives this answer; writing it down stops it
  being re-argued each time.
- **When a primary is deferred at lock, rule 7's stratification falls back to the platform's
  point-in-time label** (`market_regime_daily`, where knowledge-time-legal), descriptive, carrying no
  q and blocking nothing — because rule 7 binds the question, not the endpoint that happened to
  satisfy it by design (Q033 item 26).
- **A deferred endpoint returns as a successor question with its own id, never by editing the locked
  file.** The H-067 / Q024 precedent, now used a second time (Q033's `V`). A lock fixes `m`; adding an
  endpoint back would be a second bite with the first question's registration date. The successor
  inherits every definition verbatim **and** the caveat that the first question's own run has since
  read those nights.
- **A provisioning blocker that fires three times in one day is a standing item, not three incidents.**
  Q030, Q032 and Q033's P2 all stopped on the same two absent environment variables. The desk cannot
  request credentials (rule 1) and cannot wait its way out; the board should carry one line naming the
  cost in questions, not one line per question.

---

## Addendum — 2026-09-14 (pre-lock)

**Run:** `decide Q033` addendum by decision-maker (autonomous, DP-40..48) · **Source:** Q034's
`record` pass the same day — `research/questions/Q034_economic_objective/DECISIONS.md` item 21 flagged
Q033 as carrying the identical §2.4 clause · **State:** `state.json` = `PREREG_DRAFT` (`apply` done,
**not yet locked**) — in scope, and the correction lands before the lock, not after it.

One item, one correction. **No DP entry is added** (a `record`-time correction on another question's
grounds is not Haci's word); the generalising form is listed under *Standing rules proposed* below.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 34 | **§2.4's monotonicity screen — "strictly monotone" is a mis-transcription of the platform invariant** | DECIDED | **The word "strictly" is struck and the clause is corrected to the platform's own non-strict predicate, with Q034 item 21's three guards riding with it unchanged.** §2.4 must read: *"**Wrong-side or non-monotone ladder at the close:** `d_L3 ≤ 0`, the six flattened levels **not monotone non-decreasing in the pick's direction (ties across lanes allowed — the platform's own predicate `_ladder_is_monotonic`, `services/super_agent_select_service.py:180-192` at the pinned SHA `fa70688`: bullish `all(b >= a for a, b in zip(values, values[1:]))`, bearish `all(b <= a ...)`)**, or `outcome_target_invalid` non-null → excluded and counted."* **Verified read-only at the pin, not taken from Q034:** `:180-192` is the non-strict predicate as quoted, and `_enforce_ladder_monotonic` `:195-257` states the intent in its own docstring — *"equal prices across lanes are allowed (non-strict monotonicity), as duplicates already exist in the book and grading handles them"* — so ties are allowed **by design**, and a payload that still fails the predicate after the writer ran is the documented *unresolvable-fallback* case, i.e. a defect. The strict reading is not a stricter version of this screen; it is a **different screen**, one that fails 429 of 550 published rows on this very population of which **388 are ties and only 41 are true reversals** (`STEWARD_Q034_exposure.md` §(b), same window, same freeze, same `exclusions_v003`) — a screen that discards 78% of the register's picks for satisfying the platform's invariant is not a conservative choice but a wrong one, so **DP-45 does not fire**: the two readings do not differ only in strictness. **Three guards, verbatim from Q034 item 21 and none of them loosening anything:** (i) `eval.py` prints the screen's **own firing rate per window** — pooled, per half, and for picks and controls separately — and **fails loudly** if it exceeds the pre-fix **25.71%** in `DATA_NOTES.md` (steward, Q018 R1: 36/140 before 2026-07-06; **0.00%, 0 of 355, on/after**); Q033's registered window opens **2026-09-15**, two months after the `5fa3db4` ship, so the expected rate is ~0% and any material rate is a platform-defect flag, not a population; (ii) the **strict variant is printed as a counted companion** (rows passing non-strict and failing strict), per window and per half, so the register shows on its face what the reading cost; (iii) a tied pair `L_k = L_{k+1}` is graded on **both** levels, for published picks and for their distance-matched controls alike through the identical `d_Lk` construction of §3 — picks and controls treated identically, which is the only thing P1's contrast requires. **Scope is the word "strictly" and nothing else:** the `d_L3 ≤ 0` wrong-side limb stays as registered (Q027 / Q031 §2.4 verbatim, **not** widened to "any flattened level" as Q034's own clause reads), the `d_L3 ∈ [0.25, 10]` bound stays, and the 2026-07-06 panel split of item 17 stays — it splits at this exact ship and is further evidence of the intended reading. | **Q034 §item 21** (the identical clause, settled today on the identical grounds); **ground 3** — a screen that transcribes an external invariant has one defensible reading, and it is the invariant's; platform predicate **verified read-only at the pin** (`:180-192`, `:195-257`, commit `5fa3db4` 2026-07-06, an ancestor of `fa70688` — `STEWARD_Q033_exposure.md` §(e) reconfirms the ancestry); **`DATA_NOTES.md`** (steward, Q018 R1) 25.71% pre-ship → 0.00% post-ship under the non-strict definition; **DP-26** (a lock-time convention derived from no outcome, corrected **before** the lock); **DP-50(c)** (code read read-only at the pinned SHA, never HEAD, never a live query); §10 threat 12, which already files non-monotonicity as a **defect** |

### Do the registered exposure numbers stand? — yes, and here is why, stated exactly

**`STEWARD_Q033_exposure.md` did not apply the strict screen. It applied no monotonicity screen at
all.** Its §(a) funnel resolves 550 published rows into exactly five buckets — valid **514**,
split-scale **19**, no-`lane_plans` **8**, `d_L3` bound **7**, wrong-side `d_L3 ≤ 0` **2** — with **no
"non-monotone" row and no `outcome_target_invalid` row**. Two consequences, both recorded rather than
assumed:

1. **Nothing in §5.1 needs restating downward on account of striking "strictly".** No registered
   number was ever computed under the strict reading, so the correction moves the registered *clause*
   **toward** the funnel that was actually measured, not away from it. Had the strict reading stood,
   §5.1's rows would have been wrong by the width of Q034's finding (429/550) and Q033 could not have
   locked on them; the correction is what makes the registered numbers usable, not what disturbs them.
2. **The measured funnel is, however, marginally *looser* than the corrected clause** — it omits the
   ~41 true reversals and the 4 `outcome_target_invalid` rows that the non-strict screen does remove
   (counts from `STEWARD_Q034_exposure.md` §(b), same 550 rows). So **0.6620 is an upper bound on the
   true non-strict rate**, and the honest question is whether the bound can move a date. It cannot,
   and the worst case is bounded without a recount: at most **45 of 550** rows are at issue, they are
   concentrated **before 2026-07-06** (`DATA_NOTES.md`: 25.71% pre-ship, 0.00% post-ship), and Q033's
   night rule needs **≥ 3** valid picks on a night where the measured distribution is min **4** and
   median **8** with only **five** nights below 7 valid picks (4×3, 5×1, 6×1 — §(a)). Even if every
   one of those five nights fell below 3, the rate becomes **42/71 = 0.5915**, floor A (≥ 80) binds at
   session **135 < 158**, and limb (a) clears **0.40** with 48% headroom. **The window stays 158
   sessions, the decision date stays Monday 2027-07-12, the extension and hard stop stay Monday
   2027-08-23, and the lock-or-DEFER call is unchanged.** Nothing moves in; nothing needs to move out.
   Guard (i) measures the real firing rate on the registered window at the decision pass, where it is
   expected to be ~0%.

**No re-count is routed to the Steward.** A recount could only lower 0.6620, which moves dates **out**
— and the bound above already shows that even the worst admissible value changes no date, no floor
call and no branch. Spending the Steward's pass to confirm a number that decides nothing would delay a
lock for arithmetic already done here. (If the Registrar prefers the number restated rather than
bounded, that is a §5.1 footnote, not a schedule change.)

### Corrections to silent choices — twenty-three

23. **§2.4, §10 threat 12, and §5.1's funnel note — the monotonicity screen is non-strict.** The
    Registrar applies exactly three edits, and no others.
    **(a) §2.4, the "Wrong-side or non-monotone ladder at the close" bullet (PREREG.md lines
    262–263).** **Currently reads:** *"`d_L3 ≤ 0`, the flattened six levels not **strictly** monotone
    in the direction, or `outcome_target_invalid` non-null → excluded and counted."* **Must read:**
    *"`d_L3 ≤ 0`, the six flattened levels **not monotone non-decreasing in the pick's direction —
    ties across lanes allowed, the platform's own predicate `_ladder_is_monotonic`
    (`services/super_agent_select_service.py:180-192` at the pinned `fa70688`: bullish
    `all(b >= a)`, bearish `all(b <= a)`), whose writer `_enforce_ladder_monotonic` (`:195-257`,
    commit `5fa3db4`, 2026-07-06) states that equal prices across lanes are allowed by design** —, or
    `outcome_target_invalid` non-null → excluded and counted."* Then, in the same bullet, the three
    guards of item 34 in one sentence each: the **firing rate printed per window** (pooled, per half,
    picks and controls separately) with `eval.py` **failing loudly above 25.71%** (`DATA_NOTES.md`,
    steward Q018 R1; post-ship measured 0.00% of 355, and this window is entirely post-ship); the
    **strict variant printed as a counted companion**; and **tied pairs graded on both levels for
    picks and matched controls alike**. The word **"strictly" is struck wherever this screen is
    referenced** — it occurs only here in the screen's own statement. **Nothing else in the bullet
    moves:** the `d_L3 ≤ 0` limb is **not** widened to "any flattened level" (Q027 / Q031 verbatim,
    DP-26), and line 104's and line 344's uses of "strictly" belong to the band construction and the
    `U`-before-`D` race and are untouched.
    **(b) §10 threat 12 (PREREG.md lines 964–966).** **Currently reads:** *"Null-ladder, non-monotone
    and split-scale payloads (DATA_NOTES) are excluded and counted; the question speaks only for
    published picks carrying a complete, monotone, correctly-scaled swing target."* **Must read** the
    same sentence with **"non-monotone"** and **"monotone"** qualified as **"non-monotone *in the
    platform's non-strict sense (ties allowed)*"** and **"*non-strictly* monotone"**, plus one added
    sentence: *"The screen is the platform's own invariant, not a stricter desk variant; its measured
    pre-ship rate is 25.71% and its post-ship rate 0.00% (`DATA_NOTES.md`, steward Q018 R1), this
    window is entirely post-ship, and a material firing rate inside it is a platform-defect flag that
    stops the run, not a population this question describes."*
    **(c) §5.1 — one footnote under the exposure table, and no number changed.** **Must read:** *"The
    R1 funnel in `STEWARD_Q033_exposure.md` §(a) (550 → 514 valid) applied **no** monotonicity or
    `outcome_target_invalid` screen, so every rate above is an **upper bound** on the corrected
    non-strict funnel by at most the ~41 true reversals and 4 `outcome_target_invalid` rows measured
    on the same 550 (`STEWARD_Q034_exposure.md` §(b)), concentrated before the 2026-07-06 ship.
    Worst case — all five nights carrying fewer than 7 valid picks lost — the rate is 0.5915, floor A
    binds at session 135 of 158, and no date, floor call or branch changes (DECISIONS item 34)."*
    The rows at lines **539, 541, 542, 543, 544, 545** and the §5.2 projection at **573–574** are
    **left exactly as they are**; §(d)'s 7-of-550 and 20-of-514 figures are unaffected because the
    `d_L3` bound is not the screen being corrected.

### Standing rules proposed (not added — no DP entry from an addendum)

- **A desk screen that transcribes a platform invariant is read as the invariant reads, at the pinned
  SHA, and the transcription is corrected before lock when they diverge** — with the firing rate
  printed and `eval.py` failing loudly above the defect's measured historical rate, and the discarded
  variant printed as a counted companion. Twice in one day (Q034 item 21, Q033 item 34) on the same
  clause. Haci confirms or declines it as a `DP`; until then it is precedent, not policy.
- **When a screen is corrected before lock, say in the same breath whether the exposure count that
  sized the schedule applied the old screen, the new one, or neither** — and if neither, bound the
  difference rather than re-routing a Steward pass that cannot change a date.
