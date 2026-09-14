# Q030 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 7 items
(+ 6 items decided, defaulted or routed here: the lock-blocking R2 gate, the window and schedule the
draft leaves to `record`, and four choices the draft makes silently)

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

## The headline

**Q030 does not lock today. R2 is blocking and two of its three limbs have never been measured.**
The gate is *credentials present* **and** *≥ 90% bar coverage over the 2,405-symbol base universe*
**and** *an all-candidates contributing-night rate ≥ 0.36 per elapsed session*. **The rate limb is
now measured and passes:** `research/reports/STEWARD_Q027_exposure.md` returns **0.6761 contributing
nights per elapsed session** (48/71) on the all-candidates funnel, and Q030's night rule is strictly
broader than Q027's (Q030 needs a non-excluded matured run with `n_t ≥ 1` and `m_t ≥ 1` and imposes
**no per-row screen on candidates at all**), so 0.6761 is a **lower bound** on Q030's own rate and it
clears 0.36 by 88%. **The credential limb is the real blocker**, exactly as §5.3 predicted: the Q024
R1(d) precedent is that `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` were **not present in the Steward's
environment** (`STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md` §(d)), and
`manifest_prices_universe_v001` — daily split+raw bars for all 2,405 base symbols — has never been
built. **Coverage is unmeasured because the freeze does not exist.** One paste-ready request goes to
the Steward below; any limb failing → Q030 goes to `research/questions/DEFERRED.md` with the blocker
named, unregistered, and the Registrar writes that entry.

**Five items are DEFAULTED** (#8 the prospective-only window start, #9 the window end and decision
date, and three folded into them) — all R-3, all the same cost: waiting. **Seven are DECIDED**,
including all seven of the draft's own §11 items, every one of which goes the Registrar's way.
**One stays ROUTED and blocking** (R2), two are routed and non-blocking (R1's remainder, R3/R4).
**Seven corrections** are listed for `apply`; six tighten a clause and none weakens one.

**The schedule moves OUT, and that is the whole of what the measured rate changes.** On 0.6761 the
80-night floor binds at session **119**, not the draft's 92: window **2026-09-15 .. 2027-03-05**,
decision **Monday 2027-04-12**, single DP-13 extension to window end **2027-04-19** decided **Monday
2027-05-24**, then DEFERRED. Identical to Q027's `record` schedule, which is the point — one
successor selection freeze and one price fetch serve both (§5.2). 6.9 and 8.3 months from a
2026-09-14 lock, both inside DP-43's 12-month ceiling (2027-09-14). **Every date is conditional on
the actual lock commit date**, because §6's window opens on the first session after it; if R2 delays
the lock, §5.2's arithmetic is recomputed from the real start and the 0.36 gate is re-solved against
the ceiling measured from the real lock — **out only, and the gate tightens** (Correction 3).

**Rule 14: no exception is requested and none is needed.** Every eligibility field, every mover level
`T_{s,t}`, every episode id and every stratum label is frozen before a post-pick-night bar is loaded
(§6's enforcement clause); `market_regime` is a stratifier, never a filter or an arm, and the window
starts long after the 2026-06-09 point-in-time boundary. **DP-05 is untouched and DP-41 is not
engaged.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | The random-draw denominator | DECIDED | **Option A — `n_t = \|U_t ∩ B_t\|`**, with the as-filed `n_t = \|U_t\|` version computed and **blocking** (§8 clause 7). A candidate outside `B` can never appear in `M_t`, so counting it in the draw size would compare the engine against a random list it never drew, and §2.4's simultaneity rule (a symbol excluded from `B_t` leaves `M_t`, `U_t^B` **and** `b_t` together) has no coherent reading under B. The pair is **strictly the stricter test**: a larger `n_t` raises `e_t` and lowers the lift, so requiring the as-filed version to clear 2.00 as well can only ever prevent a CONFIRMED. | ground 3 — one arithmetically coherent answer; **DP-25** honoured, not overridden: the as-filed construction is kept and made *blocking* rather than discarded; **DP-45** (the option that cannot borrow strength from a denominator the engine never drew from) |
| 2 | The lift MPE, and the standing rule behind it | DECIDED | **`E1 ≥ 2.00` applied here as registered, from Haci's own H4 PASS line** (`research/reports/INBOX_2026-09-14_master_hypothesis_program.md` §1, H4: *"Candidate-universe recall materially exceeds random/base-universe expectation, ideally ≥2× lift"*), mirror `≤ 0.50`, **with the `D ≥ +1.0 pp` materiality floor** (item 3) as an inseparable second condition. *"Ideally"* is read as the threshold, not the aspiration. **Not lowered at the decision pass in any branch**, including one where the CI excludes 1.00 at 1.9. **DP-20 is considered and correctly not applied** — it governs a touch-rate endpoint on a 40–70% base, and +5.0 pp on `e_t ≈ 2.4%` silently demands a lift above 3, a different and unfiled hypothesis. **No DP entry is written by this run** (DP-40); the *general* rule is filed below under **Standing rules proposed**. | **DP-25** (units and cuts come from the hypothesis as written; this number is the hypothesis's own); **DP-44** — it carries no ratio unit, and its bar against *inventing* a number is satisfied precisely by taking his; **DP-45** (the stricter reading of "ideally"); **DP-40**; **Q027 DECISIONS #3**, the identical shape with H3's 0.05 |
| 3 | The materiality floor on `D` | DECIDED | **Option A — `D = mean_t(recall_t − e_t) ≥ +1.0 pp` required alongside the lift** (§8 clause 3b), mirror `≤ −1.0 pp`, with its own two CIs. A ratio can be large over nothing: a lift of 2 on a 0.4% base means the universe holds under 1% of the market's movers, and no reading of "finds major opportunities" survives that. | **DP-45** — A and B differ **only** in strictness and the floor can never do anything but block a CONFIRMED; ground 3 (a dimensionless ratio with no absolute anchor is not a finding) |
| 4 | The mover's reference price and gap-throughs | DECIDED | **Option A — the level `T_{s,t} = C_{s,t} + 3 × ATR_{s,t}` is set at the pick-night regular-session close, and any regular-session high touch in t+1..t+20 counts, including a gap through at the t+1 open** — for **every** symbol in `B_t` alike, found and missed. The construction is symmetric by design: it is not picks against an outside cohort, it is the universe against the rest of the market at an identical, self-scaled distance on both sides, which is where rule 5's distance match lives in this question. Rule 5's *"a target already passed at entry is not a hit"* governs a **pick's tradeable target** from a stated entry; it is honoured in the **mandatory tradeable companion** (the same endpoint from the t+1 open with gap-throughs excluded), which is printed always, decides nothing, and which §8's language clause and §9 require beside any quoted lift. | **DP-11 / DP-03(a)** (the pick-night close is the desk's standard reference, used identically on both sides); **DP-25** (H-074 asks whether the platform found the name *before it moved*, and an overnight gap is the archetype); rule 5 satisfied by the companion, not waived; **DP-26** (a construction fixed at lock, derived from no sealed outcome) |
| 5 | The base universe for the primary | DECIDED | **Option A — all of `B` as filed** (the 2,405 pinned symbols), with the **tradeable-B** restriction (`C_{s,t} ≥ $5`, `adv20 ≥ $5M`, which moves `b_t`, `m_t`, `n_t` and `e_t` together) computed and **blocking at lift ≥ 1.00** (§8 clause 8). The tradeable restriction changes the population in a direction the desk cannot sign in advance, so registering it as the primary would be re-filing the hypothesis; the blocking clause is what stops A being the looser choice, and §9 requires the tradeable number beside any quoted lift. **§10 threat 4 stands as disclosure**: the Russell microcap tail enlarges `m_t` and depresses `recall_t`, making the primary conservative. | **DP-25** (registered as filed); **DP-45** (the blocker keeps B's strictness without choosing between the two); **DP-26** ($5 / $5M fixed at lock) |
| 6 | The bear direction | DECIDED | **Option A — bull recall is the single primary, `m = 1`**; the identical statistic at −3 ATR over bear movers is a **fully computed secondary that decides nothing**, with both CIs and raw p, plus the `dominant_direction = 'bearish'` / bear-source-tag variant. **No secondary is promoted to a primary at the decision pass.** A striking bear result licenses a successor PREREG with its own primary and nothing else. | **DP-25** (H-074 names one primary and files bears separately); rule 8 (§10 threat 8: seven feeds × two directions × three thresholds is a ninety-number forking surface, and `m = 1` is the whole protection); **DP-45** — one shot at CONFIRMED, not two; **Q027 / H-012 convention** |
| 7 | The sealed post-hoc panel | DECIDED | **Option A — R4 is requested as a droppable routed item** and the panel is printed **once, at the decision pass, by the byte-identical `eval.py`**, labelled, split at 2026-07-02 (the bear-v1 rejoin, `5b716a2`) into A = 2026-06-01..2026-07-01 and B = 2026-07-03..2026-08-12, never blended, each sub-panel SUPPRESSED below 20 contributing nights. It enters **no verdict, no CI comparison, no half, no stratum test, no q and no §9 rule**. **R4 is explicitly subordinate to R2**: if the B-wide fetch is expensive or rate-limited, R4 is the first thing dropped and the panel is simply not printed. | ground 3 — a panel computed after the primary run is fixed cannot inform a choice made before it; **DP-06 / DP-50(a)** (the sealed stretch is two features and is split, never blended); **Q023 / Q024 / Q027** sealed-panel convention |
| 8 | The window start (prospective-only) | **DEFAULTED (R-3)** | **Pick nights ≥ the first session after the lock commit** (2026-09-15 if the lock is dated 2026-09-14). The sealed stretch is read only as item 7's labelled panel. Two independent reasons, either sufficient: the weeklies have printed sealed forward returns and 20-session touch rates for published picks, so the numerator's ingredients are not blind on those nights (DP-45); and the universe's **composition changed inside the sealed period** (bear projection v1 rejoined 2026-07-02), so `U_t` is not one feature across it. The cost is that Q030 decides in 2027 rather than on the sealed data now. | **DP-43**, **DP-45**; **Q027 DECISIONS #7**, same shape, same reason. Not taken: read the sealed nights — decides now, not blind |
| 9 | Window end, decision date, extension, DEFERRED fallback | **DEFAULTED (R-3)** — settled here on the Steward's delivered Q027 numbers | **Window: pick nights 2026-09-15 .. 2027-03-05 = 119 elapsed sessions** (Floor A binds: `ceil(80 / 0.6761) = 119`; Floor B, DP-24's 30 post-lock nights, lands at session 45 = 2026-11-16 and is non-binding — every contributing night is post-lock by construction). **Decision date: Monday 2027-04-12** (window end + 20 sessions maturity = 2027-04-05, + one calendar week = 2027-04-12, first Monday on or after). **Single DP-13 extension:** window end session 149 = **2027-04-19**, decided **Monday 2027-05-24**; still short there → `research/questions/DEFERRED.md`, no second pass, no reduced floor, and a floor shortfall is **never** an INCONCLUSIVE verdict. Every date moved **out** from the draft's provisional set (2027-01-26 → 2027-03-05; 2027-03-08 → 2027-04-12; 2027-04-19 → 2027-05-24) because the measured 0.6761 is slower than the borrowed 0.9538. **The 0.9577 eligible-night proxy is not used for any date** — it is an extrapolation past the freeze's own forward-bar horizon, and it is the number that would pull the decision date **in**. The draft's **8-session cushion is struck**: a cushion on a borrowed number is not a haircut (Q023 §5.1), the window end is simply the floor projection at the measured rate. Dates are recomputed session by session from the trading calendar at the actual lock, **out only**. | **DP-43** (the window that reaches every floor, computed from the Steward's numbers; +30-session extension; > 12 months → DEFERRED, not engaged — 6.9 and 8.3 months), **DP-45** (never the shorter window, never the extrapolated rate), **DP-13**, **DP-21**, **DP-24**; `STEWARD_Q027_exposure.md` Headline + "Projected schedule"; **Q027 DECISIONS #8**, identical dates by design. Not taken: the 0.9577 proxy — decides ≈ 2027-02-22 |
| 10 | **The lock-or-DEFER gate — the universe price freeze** | **ROUTED → data-steward (BLOCKING FOR LOCK)** | waits on **R2**: credentials present **AND** ≥ 90% of the 2,405 pinned symbols returning ≥ 60 bars **AND** the all-candidates night rate ≥ 0.36/elapsed session. **The third limb is already satisfied** (0.6761, Q027's report, a conservative lower bound for Q030's broader night rule) and is not re-measured. **All three limbs pass → Q030 locks** and §5.2's dates are recomputed from the actual lock date, moving **out only**. **Any limb failing → Q030 goes to `research/questions/DEFERRED.md`**, unregistered, no `schedule.json`, with the failing limb named (credential / coverage), the measured numbers printed, and the re-check trigger stated as a **measurement, not a date** (the Q025 form): the credential present in the Steward's session and a ≥ 90% coverage probe. The question number Q030 is consumed either way. | — |
| 11 | Demotion, and the sub-cell suppression list | DECIDED | **The primary is not demotable.** E1 is the only endpoint that carries a verdict, so a night shortfall leaves nothing to demote: it is a floor failure — the single DP-13 extension, then DEFERRED — never a demotion to descriptive and never INCONCLUSIVE. **Sub-cells: the list is FIXED at lock**, revised **once** at `record` from **R2(iii)**'s counts-only dry run (`b_t`, `n_t`, `m_t` on 2026-06-01..2026-08-12) and R1(b)/(c), then **closed** — a cell suppressed at lock stays suppressed even if it clears 20 measured nights at the decision pass, and a cell cleared at lock still needs ≥ 20 **measured** contributing nights to print. **Suppression restricts affirmative reporting only**: it never removes clauses 6–11's blockers, and the halves, the monthly blocks and every blocking companion are **not** on the list and block at whatever count they have. On the nearest measurement the desk holds (`STEWARD_Q027_exposure.md`, the same `tape_t` construction at 119 sessions) **five of the six `tape_t` cells project below 20 and only `up_mid` clears**; that is the expectation the `record` pass tests against a measurement, **not** a number registered now. | **DP-43** (demotion decided at lock, never afterwards), **DP-21** (20 per cell, no floor moved in either direction); **Q027 DECISIONS #10 and Correction 3**, **Q023 #9** — same construction |
| 12 | Exclusions in a window every night of which postdates the freeze | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** (the newest file, DP-22) with the **add-only successor exclusions file** issued with the successor selection freeze — the identical three lists (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`), identical criteria, covering nights after 2026-09-10; the successor file may only **add**, no night is ever removed from a v003 list, `exclusions_v003.json` is not edited, and both paths are `eval.py` inputs with no hard-coded file name or date. DP-04 applies mechanically on top. **On the successor file's fourth list, `payload_disabled_runs`** (added by Q027 DECISIONS #11 from the 2026-06-02 signature): Q030 **retains** such a night unless it independently fails §2.6's corroboration gate, because the criterion screens a **published payload Q030 never reads** — this question reads candidate symbol sets and prices, its universe is built upstream of publication, and §2.6 is the direct test of whether the universe was intact that night. The night is **flagged and counted**, and the whole endpoint recomputed **excluding** those nights is added to §4.3's mandatory descriptive list **before that list closes at lock** (Correction 6). | **DP-22** read as "one list, one set of criteria" — its "cite the newest file" clause presumes a sealed window and Q030's is entirely post-freeze; **DP-28** not engaged (Q030 has no published arm); **Q027 DECISIONS #11**, **Q023 #8**, same construction |
| 13 | A mid-window change to what `U_t` *is*, and DP-50(b) | DECIDED | §5.2's split rule stands **as drafted and is load-bearing**: any commit touching `services/candidate_universe_builder.py`, any change to `uoa_screener.max_symbols`, to the UOA bulletin list sizes, to the insider-watch parameters, or to which projection tables feed the universe — and any `sas_runs.config_json` change to those keys — makes `U_t` **two features**; the window is cut at the ship date, the **post-ship** segment becomes the question's window with the whole schedule recomputed from it (**out, never in**, same single extension, same ceiling measured from the original lock), the pre-ship segment becomes a labelled descriptive panel entering no verdict, and if neither segment reaches the floor inside the ceiling Q030 is **DEFERRED**. **A scoring-side change is not such a split** — the universe is built upstream of scoring. **DP-50(b) runs the other way too:** any such platform change is **flag-off until 2027-04-12** (2027-05-24 if the extension fires), checked before any fix brief is written (Correction 4 fixes the dates the draft carried). `eval.py` **fails loudly** on any cross-freeze disagreement in a night's candidate symbol set. | **DP-06 / DP-50(a)** (a repair or a config ship splits a column into two features at the ship date), **DP-50(b)** (the PI-011 / Q010 pattern), **DP-50(c)** (the sweep runs on the pinned freeze and the read-only repo, never a live query); **Q027 DECISIONS #12** |

## Corrections to silent choices

**Seven.** The Registrar applies them at `apply` with the rest of this file. Everything else was
checked against the policy and already matches (list at the end of this section).

1. **§5.1 and §5.2 — the borrowed 0.9538 planning rate and the 92-session schedule are superseded by
   a measurement that has since landed.** `research/reports/STEWARD_Q027_exposure.md` was *"in
   preparation at this lock"* when the draft was written and is now delivered. **Must read:** §5.1's
   planning row becomes **"measured 0.6761 all-candidates contributing nights per elapsed session
   (48/71), `STEWARD_Q027_exposure.md`, borrowed as a conservative lower bound — Q030's night rule
   (`n_t ≥ 1`, `m_t ≥ 1`, no per-row candidate screen) is strictly broader than Q027's (≥ 30 eligible
   rows and a defined `d*_t`)"**, and §5.2's session-by-session arithmetic is item 9's schedule:
   **window 2026-09-15..2027-03-05 = 119 sessions, decision Monday 2027-04-12, extension window end
   2027-04-19 decided Monday 2027-05-24**. The **8-session cushion is struck** — a cushion on a
   borrowed number is not a haircut (Q023 §5.1, in its third question now), and the window end is the
   floor projection at the measured rate, nothing added. One line states **why 0.6761 and not
   0.9577**: the 0.6761 is bound by the price freeze's own forward-bar horizon, the 0.9577
   eligible-night figure is an upper bound, and DP-45 takes the directly measured number because the
   extrapolation is the one that pulls the date **in**.
2. **§5.3 R2, R3 and R4 — every delivery date moves out with the schedule.** **Must read:** R2's
   primary cut covers ≥ 60 sessions before the window start through **2027-04-05** (t+20 of the last
   in-window pick night), delivered before **Monday 2027-04-12**; the extension cut, **only if** DP-13
   fires, through **2027-05-17**, delivered before **Monday 2027-05-24**, built then and not before.
   R3's successor selection freeze covers pick nights **2026-09-15..2027-03-05** (and ..2027-04-19 on
   the extension) with the same due dates. R4 is unchanged in scope and stays droppable. These are the
   **identical dates Q027's re-issued R2 carries**, which is what lets one selection freeze and one
   price fetch serve both questions (§5.2's alignment clause).
3. **§5.3 — "≥ 0.36 per elapsed session" is the ceiling's solution at the actual lock date, not a
   constant, and the limb is already satisfied.** **Must read (a):** the lock-or-DEFER test is the
   **inequality** — 80 contributing nights divided by the elapsed sessions still admissible under
   DP-43's 12-month ceiling **measured from the actual lock commit**, rounded **up**; at a 2026-09-14
   lock that is ≈ 225 sessions and **≥ 0.36**, and it is **re-solved if the lock date moves**, which
   it will if R2 takes time — the gate **tightens** as the lock slips, it never loosens. **Must read
   (b):** the rate limb is **measured and passed at 0.6761** via `STEWARD_Q027_exposure.md` and is
   **not re-measured**; the two limbs still open are **credentials** and **≥ 90% coverage**, and §5.3
   should say so rather than listing all three as unmeasured.
4. **§9 — the DP-50(b) flag-off dates are the draft's provisional ones.** The bullet reads *"flag-off
   until Q030's decision date, 2027-03-08 (2027-04-19 if the single DP-13 extension fires)"*.
   **Must read: 2027-04-12 (2027-05-24 if the extension fires)**, per item 9. A stale date here is
   the one correction in this file that could let a universe-construction change ship inside the
   question's own window.
5. **§6 and §5.2 — the window start is the first session after the *actual* lock commit, not the
   literal 2026-09-15.** The draft fixes 2026-09-15 and derives 92 sessions from it; R2 blocks the
   lock, so the lock date is not yet known. **Must read:** the window opens on the **first trading
   session after the lock commit** (2026-09-15 only if that commit is dated 2026-09-14), §5.2's whole
   arithmetic is re-derived session by session from that start when the freeze is built, and a
   correction to any date may move it **out, never in**. §2.1's SQL already takes the window start as
   an argument with no hard-coded date, which is what makes this mechanical.
6. **§2.4 and §4.3 — the successor exclusions file now carries a fourth list the draft does not
   mention, and Q030's handling of it must be registered before §4.3 closes.** **Must read:** §2.4
   names the three registered lists **plus DP-04**, and adds that a night on the successor file's
   **`payload_disabled_runs`** list (Q027 DECISIONS #11) is **retained, flagged and counted** in Q030
   — the criterion screens a published payload this question never reads, and §2.6's corroboration
   gate is the direct test of universe integrity on such a night — **with the primary recomputed
   excluding those nights added to §4.3's mandatory descriptive list**, which closes at lock and
   cannot take the sensitivity later.
7. **§4.3 — "revised once at `record` from R1's measured counts" names the wrong input.** Q030's
   R1(a) is *taken from* the Q027 report, which measures **nothing at all about `B`** (§5.1 says so
   itself). **Must read:** the sub-cell suppression list is fixed at lock and revised **once** at
   `record` from **R2(iii)**'s counts-only `b_t` / `n_t` / `m_t` dry run and R1(b)/(c), then closed;
   a cell suppressed at lock stays suppressed even if it clears 20 measured nights at the decision
   pass, and a cell cleared at lock still needs ≥ 20 measured nights to print (Q027 Correction 3).

Checked and **not** corrections — each already matches the policy: the **floors** read as ≥ 80
contributing nights for the primary and 20 per reported sub-cell, the stricter reading (**DP-21**);
**≥ 30 contributing nights after the lock commit**, satisfied by construction, never reduced, with
**DP-31 correctly not invoked** because PROSPECTIVELY_CONFIRMED is reachable from this run by design
and no successor replication is owed (**DP-24**); one automatic extension then DEFERRED, fired on
`eval.py`'s **measured** counts and never on a projection (**DP-13**); the **two CIs per primary**
with the episode defined as one symbol's run of appearances at gaps ≤ 10 sessions, and the
CI-2-includes-1.00 case **INCONCLUSIVE rather than CONFIRMED** as a decision clause, not a footnote
(**DP-51**, §8 clause 5 — and §10 threat 2 is the sharpest instance of it on the desk: one 3-ATR run
makes a symbol a mover on up to twenty consecutive nights); successor freezes covering **every
candidate row and symbol, published and unpublished** (**DP-23**); the exposure count taken from the
**pinned freeze** and a delivered report, never a live query (**DP-50(c)**); the family assigned by
the primary endpoint's subject — candidate generation, not path-after-selection and not calibration —
with H-074 counted **once** (**DP-29**), and the F8 set stated symmetrically so it never shrinks
below 1 (rule 8); **no stop assumed** and **DP-27 not reachable** (no hourly bar is used anywhere)
(**DP-02**); registrar conventions fixed before any outcome is seen — the 3-ATR level with the 2/4-ATR
band, the 20-session clock, the 90% `B_t` coverage and 10% ungradeable rules, the 2% corroboration
tolerance, the 10-session block length, seed 20260914, the expanding-window tape terciles
(**DP-26**), none promotable at the decision pass; **DP-49** named in §9's brief bullet; every number
**NON_QUOTABLE** (rule 12) and nothing subscriber-facing before PROSPECTIVELY_CONFIRMED (rule 10);
and **no rule-14 exception requested or needed** (**DP-05** untouched, **DP-41** respected).

## Defaulted on Haci's behalf

- #8 Window start — chose **prospective-only, pick nights after the lock commit**; not taken: read the
  sealed June–August nights — decides now, not blind — DP-43. Overturn = successor question.
- #9 Window end and decision date — chose **window end 2027-03-05, decision Monday 2027-04-12**
  (extension 2027-04-19, decided 2027-05-24, then DEFERRED); not taken: the 0.9577 eligible-night
  proxy — decides ≈ 2027-02-22 — DP-43. Overturn = successor question.

**Two items, and both are the same cost: waiting.** The tempting alternative is written down so he can
see it: 100% of the nights old enough to test converted to contributing in the Q027 measurement, so
the 0.9577 eligible-night rate is not a fantasy and would have decided Q030 around 2027-02-22. It was
refused because it is an **extrapolation past the freeze's own forward-bar horizon**, and the desk
does not buy seven weeks with a number it has not measured (DP-43, DP-45). Nothing else was defaulted:
items 1–7 and 11–13 each met a DECIDE ground, and **none of them is a question about how he trades** —
the mover distance (3 ATR), the clock (20 sessions), the base universe and the "≥ 2× lift" bar are all
**H-074's and H4's own numbers**, taken as filed under DP-25, not desk inventions. No floor, arm, MPE,
gate or clause was weakened anywhere in this file; Corrections 1–7 tighten six and the seventh fixes a
stale date.

## Routed requests

### data-steward — R2 (the universe price freeze) — **BLOCKING FOR THE LOCK**

Q030 (does the candidate universe contain the market's big movers before they move — PREREG
`research/questions/Q030_universe_discovery_recall/PREREG.md` §5.3 request R2) cannot be locked until
we know whether a price freeze over the **whole pinned base universe** can be built at all, and this
request is a **feasibility check first, counts only, with no outcome of any kind** — no touch, no
first-touch date, no return, no excursion, no `outcome_*` column, no `sas_selection_excursion`, no
`uoa_symbol_daily.fwd_return_*`, no recall, no lift and no intersection count; forward bars may be
read only to establish that a bar exists. Please answer three things, in this order. **(i)
Credentials:** are `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` present in your session environment? The
known hazard is the Q024 R1(d) result — that check *could not be run* for one benchmark symbol
because no credentials were present (`STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md` §(d)) — so
please state presence or absence explicitly and never infer it. **(ii) Coverage:** with credentials
present, run a trailing 60-session probe over **all 2,405 symbols in the `mapping` key of the pinned
blob** (volatilx `data/sp500_sectors.json`, sha256 LF-normalized
`c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201`, entry count 2,405 — please
re-verify both against the git blob at the pinned SHA and report any disagreement as a loud failure)
and report the **share returning ≥ 60 daily bars**, which must be **≥ 90%**, plus the count and list
of symbols returning none. **(iii) Build it if it can be built:** if (i) and (ii) pass, build and pin
the freeze **now** as the next free `manifest_prices_universe_vNNN` (DP-23) — daily bars,
`adjustment=split` **and** `adjustment=raw`, `feed=sip`, for all 2,405 base symbols plus every
in-window candidate symbol and the existing benchmarks, covering **≥ 60 sessions before the window
start** through **2027-04-05** (t+20 of the last in-window pick night; a second cut through
**2027-05-17** only if the DP-13 extension fires, built then and not before), **no hourly bars**, with
symbols lacking bars **excluded and counted, never back-filled or imputed** — and report the achieved
coverage, the sha256 and the row counts. `research/lib/freeze_prices.py` takes its symbol list from a
base manifest (`BATCH = 50`, `:46`); extending it to accept an explicit symbol list is a change under
`research/` and is **not** an enforcement file under rule 15. Please also return **(iv)** a
counts-only dry run on the sealed period — `b_t`, `n_t` and `m_t` per night for pick nights
**2026-06-01..2026-08-12** and nothing else, so the desk knows whether `m_t ≥ 1` is ever binding and
can fix the sub-cell suppression list from measurement. **If it cannot be built, say which limb fails
and stop** — do not partially build, do not substitute a narrower symbol list, and do not estimate
coverage from anything but the probe. **The call this request decides:** the third limb of Q030's
lock gate is **already satisfied** — the all-candidates contributing-night rate is measured at
**0.6761 per elapsed session** in `STEWARD_Q027_exposure.md` and Q030's night rule is strictly
broader, so it is a conservative lower bound and clears the **≥ 0.36** threshold (80 nights over the
≈ 225 elapsed sessions admissible under DP-43's 12-month ceiling at a 2026-09-14 lock, rounded up,
re-solved if the lock date moves) — and **no second exposure count is requested**. So credentials and
coverage decide it: **both pass → Q030 locks** on the schedule in DECISIONS item 9 (window
2026-09-15..2027-03-05, decision Monday 2027-04-12), re-derived from the actual lock date and moving
**out only**; **either fails → Q030 goes to `research/questions/DEFERRED.md`** with the failing limb
named and the measured numbers printed, unregistered and with no `schedule.json`. Report to
`research/reports/STEWARD_Q030_universe_freeze.md`.

### data-steward — R1 (counts only) — **(a) CLOSED; (b)–(d) open, blocking the schedule detail, not the lock**

Q030 §5.3 request R1. **(a) is answered and closed:** the all-candidates contributing-night rate is
**0.6761/elapsed session (48/71)** from `research/reports/STEWARD_Q027_exposure.md`, taken as
delivered and borrowed as a conservative lower bound; **no second count of the same nights is
requested** (§5.1). Still needed, all counts-only on the pinned freezes and the read-only platform
repo, no live query (DP-50(c)), no outcome of any kind: **(b)** the distinct-symbol count of
`sas_candidates` per night against `sas_runs.stats_json.universe_count`, the count of nights exceeding
the **2%** tolerance of §2.6, and the per-night `source_counts` — this is the corroboration gate, and
it is the only defence against a universe entry that was built, never persisted, and would be scored
as "the platform never found it"; **(c)** the share of each night's candidate symbols present in the
pinned blob's `mapping`, and the distinct list of candidate symbols **absent** from it over the sealed
window (the ETF / non-`B` residue of §2.4, which §4.3's as-filed companion is computed on); and
**(d)** the DP-50(a)/(b) commit sweep since manifest SHA `fa70688` over
`services/candidate_universe_builder.py`, `services/uoa_screener.py` and the projection-pick writers,
**with an explicit answer even when it is "none"**, plus a dated `DATA_NOTES.md` entry for any repair
that rewrote historical rows. For (d), `STEWARD_Q027_exposure.md` (g) already establishes that only
four commits (`2d5776c`, `4775e49`, `22a2e1b`, `d19c9a9`, all 2026-09-13) separate `fa70688` from
HEAD and that none touched the three SAS scoring files — please state directly whether any of them
touches the **universe-side** files above, rather than letting the desk infer it.

### data-steward — R3 (successor selection freeze) and R4 (sealed universe bars) — due before the decision date, **not** blockers for lock

R3 (DP-23): the successor **selection** freeze `manifest_v00N` — same SQL, same exclusion criteria,
**`sas_candidates` for every candidate row published and unpublished**, plus `sas_runs` and
`market_regime_daily` — covering pick nights **2026-09-15..2027-03-05** (and ..**2027-04-19** only if
the DP-13 extension fires), delivered before **Monday 2027-04-12** (extension pair before **Monday
2027-05-24**), with the **add-only successor exclusions file** — the identical file Q027's R2
requires, **built once and shared**. Where a successor freeze overlaps an earlier one on
`sas_candidates`, compare the rows and treat **any disagreement in a night's symbol set as a loud
failure**: a repair that changed which symbols were candidates would silently re-run this experiment
(DP-50(a)). Repeat R1(d)'s commit sweep for the period between the freezes. Please re-confirm every
§5.2 date session by session from the trading calendar when the freeze is built; a correction may move
a date **out, never in**. R4 (optional, droppable, decides nothing): the same B-wide daily bars for
pick nights **2026-06-01..2026-08-12** with forward bars to 2026-09-10, so the byte-identical
`eval.py` can print the labelled post-hoc panel at the decision pass. **If R2's fetch proves expensive
or rate-limited, R4 is the first thing dropped** and the panel is simply not printed — no verdict, no
clause and no date depends on it.

### registrar — conditional, fires only if R2's gate fails

If R2 reports credentials absent or coverage below 90%, write the `research/questions/DEFERRED.md`
entry for Q030 on this file's **first** admission ground (the objective cannot be measured with the
artefacts the desk holds), in the Q025 form: the hypothesis and why it is worth keeping; the failing
limb named exactly (**"no `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` in the Steward's environment, so
`manifest_prices_universe_v001` cannot be built"**, or the measured coverage share); the fact that
the **rate limb passed at 0.6761/session** and is therefore not the blocker; what was considered and
rejected (a narrower symbol list, a sample of `B`, estimating coverage — each rejected under DP-45,
because a denominator built from a subset of `B` is a different population and the whole point of the
question is the market outside the pool); and the re-check trigger stated as a **measurement, not a
date** — the credential present in a Steward session and a ≥ 90% coverage probe, at which point Q030
re-enters the queue at the front with this DECISIONS file binding and §5.2's schedule recomputed from
the new lock date. `state.json` stays at `PREREG_DRAFT` → `DEFERRED`; **no `PREREG_LOCKED`, no
`schedule.json`**, the question number Q030 consumed and not reused, `research/BACKLOG.md` marking
H-074 deferred rather than registered, and the F8 correction set recorded as **not** containing
Q030 while deferred (the H-062 / Q025 precedent).

## Schedule

**Conditional on R2 and on the actual lock date.** Every date below is derived from the **measured**
0.6761 contributing nights per elapsed session (`STEWARD_Q027_exposure.md`, borrowed as a lower bound)
with the window opening on the first session after the lock commit; if the lock slips, the whole
arithmetic is re-derived session by session and may move **out only** (DP-43, DP-45).

decision_date: **2027-04-12** (Monday) · extension_date: **2027-05-24** (Monday; DP-13's single
automatic extension, then DEFERRED — there is no second pass) · hard_stop: **2027-05-24** (still short
there → `research/questions/DEFERRED.md`) · rule: **exposure-driven** (window end set by accrual to
the later of the two primary floors at the measured rate; the decision date then follows from the
20-session maturity plus a one-week freeze margin, first Monday on or after, moved out if that Monday
is a market holiday) · window: pick nights **2026-09-15 .. 2027-03-05** = **119 elapsed sessions**
(extended: .. **2027-04-19**, 149 sessions) · extended: **false** · maturity: **20 sessions**, uniform
across every symbol in `B_t` · gates: **≥ 80 contributing nights for the primary endpoint**, **≥ 30
contributing nights dated after the lock commit** (satisfied by construction), **`B_t` ≥ 90% of 2,405,
ungradeable ≤ 10%, §2.6 corroboration passing on every contributing night**, on `eval.py`'s measured
counts · ceiling: 6.9 months from a 2026-09-14 lock, extended 8.3 months, against DP-43's 12 months
(2027-09-14) · **lock-or-DEFER gate: credentials present AND ≥ 90% coverage AND rate ≥ 0.36/session —
the rate limb measured and passed at 0.6761; the other two open, R2 blocking.**

## Standing rules added

_none._ Nothing here is Haci's word: items 8 and 9 were **DEFAULTED** under DP-43, which adds no DP
entry (DP-40), and items 1–7 and 11–13 are applications of DP-02, DP-03, DP-06, DP-11, DP-13, DP-21,
DP-22, DP-23, DP-24, DP-25, DP-26, DP-28, DP-29, DP-40, DP-43, DP-44, DP-45, DP-49, DP-50, DP-51 and
locked precedent. The generalisable ones are listed below as **proposals**, for him to confirm or drop.

## Standing rules proposed

- **The MPE for a ratio / lift endpoint is a lift of 2.00 together with a stated absolute floor on the
  underlying difference.** DP-44 carries touch-rate (+5.0 pp) and per-trade ATR (0.25) units and no
  ratio unit at all, and "lift ≥ 2" is Haci's own H4 number. The entry should carry the floor in the
  same sentence, because that is the half a bare ratio loses: a lift is dimensionless and can be large
  over nothing, so any lift MPE is paired with a minimum absolute difference (here `D ≥ +1.0 pp`)
  sized to the endpoint's own null base rate, and **DP-20 is explicitly not converted into a lift** —
  +5.0 pp on a 2.4% base demands a lift above 3 and silently re-files the hypothesis. H-081 and H-083
  (the other two F8 members carrying primaries) will need this within months.
- **A borrowed exposure rate may be borrowed *across questions* only when the borrowing question's
  contributing-night rule is strictly broader than the lender's, and the direction must be stated.**
  Q030 borrows Q027's 0.6761 rather than routing a second count of the same nights, and it is
  legitimate precisely because Q030's night rule (`n_t ≥ 1`, `m_t ≥ 1`, no per-row screen) contains
  Q027's (≥ 30 eligible rows and a defined `d*_t`) — so the borrowed number is a **lower bound** and
  every date it sets moves out, never in. Where the containment does not hold, the count is routed.
  Stating this once beside DP-43 would save a Steward request per question in an aligned batch.
- **A lock gate with more than one limb names which limbs are measured and which are open, every time
  it is restated.** Q030's gate has three; one was satisfied by a report that landed between drafting
  and `decide`, and the draft still listed all three as pending. A gate that is not re-read against
  the desk's current measurements sends the Steward to re-measure what it already holds, or blocks a
  lock on a limb that has already passed.
