# Q034 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous, DP-40..48) · Source: PREREG.md "Open decisions before
lock", 5 items (+ 15 decided, defaulted or routed here: the two routed requests named in §5.3 and
thirteen the draft settles silently, leaves conditional on another question, or leaves to `record`)

**Record pass: 2026-09-14** (autonomous, DP-40..48) · Source: `research/reports/STEWARD_Q034_exposure.md`
(R1, counts only). **R1 is answered and item 19 closes.** One new item (**#21**, the §2.4 monotonicity
reading) and one new correction (**Correction 7**) are added here, because the Steward's binding limb
turned on a definitional fork he correctly refused to settle. Under #21's ruling **both gate limbs pass
and Q034 LOCKS**; item 18's dates are **final**; **item 20 (R2, the successor freezes) stays ROUTED and
open**, due before the decision date.

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

## The headline

**All five of the draft's own items go the Registrar's way and all five are DECIDED** — the
within-night standardized scale (#1), computing nothing on sealed nights (#2), stability over halves
**and** arms (#3), DP-43's ceiling binding the **initial** decision date (#4) and the two-limb
separation rule (#5). Each is a lock-time convention derived from no outcome (DP-26), a technical
matter with one defensible answer, or a pair of options differing only in strictness, where the
stricter is taken without asking.

**Q034 does not lock at `decide`: R1 is blocking, as §5.3 says.** But it is blocking for a *different*
reason than in Q032 and Q033, and this is the substantive finding of this pass. The SPY-history probe
those two questions put in their lock gates **has already been answered, today**:
`STEWARD_Q032_exposure.md` §(g) reports `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` absent from the desk
session, the probe not attempted, and no pinned alternative — which deferred Q032 outright and defers
Q033's P2. **It defers nothing in Q034**, because no endpoint here is an arm contrast: the tape arms
are stability *windows*, and §2.2 pre-registers a fallback. So Q034's lock turns on counts alone
(R1(a)/(b)/(c)), and its real exposure is that **the fallback branch is the one most likely to run**.

**That is why the draft's `STABILITY_ON_HALVES_ONLY` branch is not honest as written, and is
strengthened rather than accepted** (item 3, Correction 3). As drafted, a provisioning failure the desk
*already knows about* would silently remove **half the stability test** — two of four windows — and
"keeps its sign in every window" would become "keeps its sign across two calendar halves". Removing
windows can only make **STABLE easier to reach**, never harder, so the branch as drafted buys a
CONFIRMED-side verdict with a data failure (DP-45 forbids exactly this). Three things are added
together: the **platform's point-in-time `market_regime_daily` label becomes a registered stability
partition in every branch** — it is rule 7's own column, it is knowledge-time-legal for every night of
this window (legal from 2026-06-09, FREEZE_v001 §7), it is already in the successor freeze (R2(iv)),
and Q032 §(d) measured it carrying real information against the bar-only arm (agreement only 77.8%);
the qualifier is renamed **`STABILITY_WITHOUT_TAPE_ARMS`** so the label says what is missing; and
**every branch must run four windows that clear 20 nights before any objective may be named
strongest** (item 14). The bar-only partition stays exactly as registered and is **never**
re-specified to an SMA50-only variant after the fact — that failure mode is Q032's and Q033's, and it
is not repeated here.

**Two arithmetic corrections, both moving dates out, neither changing the decision date.** §5.2's
holiday list omits **2027-06-18** (Juneteenth observed) — the same omission Q033 Correction 2 found on
the same day — so t+60 of the window end is **2027-07-28**, not 2027-07-27, and on the extension path
**2027-09-09**, not 2027-09-08. The one-session shift is absorbed by the one-week margin and the
first-Monday rule, so **2027-08-09 and 2027-09-20 stand** — but the successor **price freeze's bar
horizon moves out by a session**, and the ceiling back-solve gives **184** admissible elapsed
sessions, not the draft's 186.

**One projection in the draft is measured on the wrong population** (item 7, Correction 4). The
80-night floor is on the **ranking set** — nights where *all nine* objectives are computable — but
§5.1 projects it at 0.6620, a rate measured under §2.5's contributing-night rule alone, which does not
require a usable printed stop (O4: Q009 measured 17.8% unusable) or a complete six-level ladder across
all three lanes (O5, O8). The ranking set is a subset of the contributing nights by construction, so
the projection is optimistic by an unmeasured amount. R1 gains a limb that measures the ranking-set
rate directly, and the schedule is built on it.

**Rule 14: no exception is requested and none is needed.** Every input is a 16:05 ET candidate field,
a SPY or symbol bar dated ≤ t, a legality-tested v1.2 regime row, or the session t+1 open used **only**
as an entry price; §6's clause freezes every eligibility, window, match and stratum field before any
post-pick-night bar other than that open is loaded. **DP-05 is untouched and DP-41 is not engaged.**

## The record pass (2026-09-14, on R1)

**The whole of R1 turned on one word, and the word is a transcription error.** §2.4 excludes a pick
whose "six levels [are] not **strictly** monotone in the direction". Read literally that screen fails
**429 of 550 published rows (78%)**, and **388 of the 429 are ties, not reversals**. The platform's own
publication-time invariant — `_ladder_is_monotonic` / `_enforce_ladder_monotonic`,
`services/super_agent_select_service.py:180-192` and `:195-257` at the pinned SHA `fa70688`, read
read-only here — is **non-strict** (`all(b >= a)` bullish, `all(b <= a)` bearish) and its docstring says
so in terms: *"equal prices across lanes are allowed (non-strict monotonicity), as duplicates already
exist in the book and grading handles them."* The clause is ruled a **mis-transcription of that
invariant** and corrected to non-decreasing (item **#21**, Correction **7**), on three grounds that are
all about intent and none about which reading locks:

1. **The draft says what it expects the screen to do.** §6 admits the window *because* it "sits … after
   the 2026-07-06 `_enforce_ladder_monotonic` ship"; §4.6(c) cites the screen as what *guarantees* the
   within-lane identity; §10 threat 13 files non-monotonicity beside null ladders, unusable stops and
   split-scale payloads as a **platform defect**. The registrar's twin clause in Q032 §2.4 — same
   registrar, same day, same screen — states the expectation outright: "The whole window sits after
   platform commit `5fa3db4` (2026-07-06, `_enforce_ladder_monotonic`), so **a non-zero rate is a loud
   flag**, not a silent drop." A screen written to fire at ~0% was not written to fire on 78% of rows,
   and 388 ladders the platform blesses by design are not defects.
2. **The measured invariant agrees.** `DATA_NOTES.md` (steward, Q018 R1) measures flattened-ladder
   non-monotonicity — under the platform's own non-strict definition — at **25.71% (36 of 140) before
   2026-07-06 and 0.00% (0 of 355) on/after**. Q034's registered window is entirely post-ship, so the
   corrected screen is expected to fire at **zero** inside it; the Steward's 41 true reversals sit in the
   pre-fix June segment of the *exposure* period, exactly where DATA_NOTES puts them.
3. **Nothing in the PREREG needs strictness.** No objective, estimator, Gate 0 check or floor requires
   six distinct levels. Gate 0(c)'s "T2 indicator ≤ T1 indicator" holds with equality when `L_k = L_{k+1}`;
   O8 counts levels, and the book already carries duplicates. The strict reading would not be a *stricter
   test* — it would be a **differently-selected population** (only picks whose six levels are all
   distinct), chosen by accident, with no stated purpose.

**This is not DP-45 territory and it is stated without hedging.** The ruling is made on the pinned code
and on the draft's own stated expectation; it would read the same way had the counts pointed the other
direction, and it is recorded before any outcome exists — the Steward's report is counts-only and reads
no touch, return or excursion anywhere. It is a definitional correction to a **draft**, made before lock,
and the Registrar applies it at `apply` like any other.

**With that ruling the gate closes PASS on both limbs and Q034 locks.** Limb (b), the ranking-set rate:
**10/11 = 0.9091** on the t+60-evaluable sub-period, scheduling rate `min(0.9091, 0.6620) =` **0.6620**
(item 8's cap binds, as item 8 anticipated) against the **≥ 0.44** floor. Limb (c), the rarer registered
window on the lower of the two partitions: platform-label NOTSTRONG **14/71 = 0.1972** (bar-only HOSTILE
0.3099, cited) against the **≥ 0.11** floor. **No date moves in** (item 18): every floor is reached well
before session 158, and the registered window end 2027-04-30 and decision date **Monday 2027-08-09**
stand exactly as drafted. **No window projects below 20**, so item 14's demotion clause is not engaged at
projection and stays in force on `eval.py`'s own counts at the decision pass. **The suppression list
gains no cell and is now CLOSED** (item 13).

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | The common scale the nine objectives are ranked on (draft item 1) | DECIDED | **Option A — the within-night pooled-sd standardized excess `D_o = mean_t(g_{o,t})`, with the native-unit `E_o` printed beside every row, in every window, always; a register line quoting `D` without `E` is malformed.** Option B (`mean_t(e_t) / sd_t(e_t)`) is refused on arithmetic, not taste: its denominator is the **between-night dispersion of a mean excess**, which shrinks as a night's eligible-pick count grows, so B would rank the nine objectives partly by **how many picks carry each one** — and the nine have deliberately different denominators here (O4 loses the wrong-side stops, O5 and O8 lose the incomplete ladders). A ranks on a quantity whose denominator is a within-night dispersion of the same picks. A's known distortion — a standardized effect inflates for a near-degenerate binary objective such as O9 at 5 sessions — is already §10 threat 2, is bounded by the printed `E` and the printed raw rates (B5), and is named in the register's own sentence where the `D` and `E` ranks disagree. Neither scale is derived from an outcome; both are lock-time conventions. | **DP-26** (a registrar-chosen scale fixed at draft from no sealed outcome stands as drafted); ground 3 — one defensible answer: a ranking statistic may not be a function of how many picks a night carries; **DP-45** (the distortion is printed and named, never used to promote a row) |
| 2 | Whether the sealed period prints as a post-hoc panel (draft item 2) | DECIDED | **Option B — nothing is computed on sealed nights at all: no panel, no companion, no funnel count, no `D`, no `E`, no raw rate.** This is a deliberate divergence from Q033 DECISIONS #17 (which prints a labelled sealed panel) and the distinguishing ground is specific and decisive: Q034's nine rows **are the registered primary endpoints of seven questions whose decision dates are still ahead** — O3 → Q033, O4 → Q009 / Q010, O5 → Q012, O8's L3 row → Q006 (decides 2026-10-05), O9 → Q002 (2026-10-12), plus Q004, Q011, Q015, Q018 — computed on *their* populations, on *their* sealed nights, from *their* freeze. A "labelled panel" of those numbers is an interim look at seven locked questions' data under another name, and no label on this file can undo it for them (rule 3, rule 9). The second ground stands on its own: EXPLORE_001 already read in-sample path, speed and level outcomes, and those reads are what put "the edge is in speed and deep levels" on the backlog — the exact ranking H-084 asks for. The Reporter cross-references those questions' **ledgered verdicts** when they land (the H-077 pattern); this register never pre-empts them. | rule 3; rule 9; ground 3 — a pre-registered question may not compute another locked question's endpoint on that question's sealed nights before its decision date; **DP-45** (B prints strictly less and can reach no verdict the sealed nights would support); §7's overlap statement, which already says each of those questions owns its endpoint |
| 3 | What "keeps its sign in every window" means, and what happens when the SPY history does not arrive (draft item 3) | DECIDED | **Option A, strengthened in three parts (Correction 3).** (i) The registered stability windows are the **two calendar halves**, the **two bar-only tape arms** of §2.2 **and — added here, in every branch — the two platform-label arms**: `STRONG` iff `market_regime_daily.market_regime = 'strongly_bullish'` on a **legality-tested** v1.2 row for night t (row dated t, `market_regime` not unknown, `data_quality` not insufficient, `created_at` dated t and ≤ that night's `sas_runs.finished_at` — Q032 §(d)'s test verbatim), `NOTSTRONG` otherwise; a night failing the legality test carries **no** platform-label window and is counted. This is rule 7's own column, it is knowledge-time-legal for **every** night of this window (legal from 2026-06-09, FREEZE_v001 §7), it is already delivered by R2(iv), and Q032 §(d) measured it as **non-redundant** against the bar-only arm (agreement 49/63 = 77.8%; the HOSTILE nights split 11/11). `eval.py` **fails loudly** if an in-window night's `regime_version` is not v1.2 (DP-06 / DP-50(a) — a scorer repair makes it two features, and the bar-only arm is unaffected, which is the point of having both). (ii) When R2(i) cannot deliver SPY from 2025-01-02, the tape arms print `UNAVAILABLE` and the stability test runs on the **halves and the platform-label arms** — four windows, not two — and every stability label carries the fixed qualifier **`STABILITY_WITHOUT_TAPE_ARMS`**, which replaces `STABILITY_ON_HALVES_ONLY` wherever the draft uses it, because the old name would misdescribe what ran. (iii) The partition is **never** re-specified to an SMA50-only variant after the data exists, in either branch. Option B (halves only) is refused outright: rule 7 makes regime the dominant variable and a "stable" label computed across calendar halves alone would survive an objective that works in one tape and not the other. **The draft's fallback as written is refused on the same ground** — it silently removes two of four windows on a provisioning failure the desk already knows about (`STEWARD_Q032_exposure.md` §(g)), and removing windows can only make STABLE easier. | rule 7 (`market_regime_daily` stratification is required of every result, not optional); **DP-45** (a data failure may never relax a stability test; the branch that keeps four windows is the one that cannot manufacture a STABLE label); **DP-26** (both partitions and the legality test are lock-time conventions derived from no outcome); **DP-06 / DP-50(a)** (the v1.2 guard); **Q032 §(d)** (measured non-redundancy, cited not assumed); **Q023 E1 / Q032 C1** (the same label, the same non-independent pair — §4.3 already says so) |
| 4 | DP-43's 12-month ceiling against the extension date (draft item 4) | DECIDED | **Option A — the ceiling binds the *initial* decision date (Monday 2027-08-09, 10.9 months from the 2026-09-14 lock), and DP-13's single automatic extension may carry the extended decision to Monday 2027-09-20 (12.2 months).** DP-43 is written as "**If the initial decision date** lands more than 12 months after lock, the question goes to DEFERRED" and, in the same entry, "**DP-13's single extension = +30 sessions**" — the entry contemplates the extension on top of a window it has just sized, and applies its ceiling to the initial date. DP-13 is a **Confirmed** entry in Haci's own words and its extension is automatic and unconditional on `eval.py`'s measured counts; reading DP-43's ceiling as removing it would let a Default overrule a Confirmed. Option B (a 186-session window decided Monday 2027-09-13 exactly at the ceiling, no extension possible) is refused for the reason the Registrar gives and one more: it spends the entire ceiling **up front, before any count is measured**, leaves the marginal rarer-window floor with no remedy but DEFERRED, and — on the corrected calendar — its own arithmetic is wrong, since the last admissible window end is **2027-06-08 (session 184)**, not 186 (Correction 2). DEFERRED remains the fallback in both readings, and the extension is never a second look: `eval.py` is byte-identical and the gates are unchanged. | **DP-43** read literally ("the initial decision date"), ground 1; **DP-13** (Confirmed, Haci 2026-09-13 — one pre-agreed automatic extension, fired on measured counts, no new question); ground 3 — a Default does not override a Confirmed entry; not the option that reaches a date sooner (**DP-45**: A's initial date is *earlier* than B's only because B forgoes the extension, and A's floors are the same) |
| 5 | The separation rule (draft item 5) | DECIDED | **Option A — a winner must clear both limbs: interval separation from the runner-up (its `D` lower bound above every other objective's `D` upper bound) on **both** CIs of §4.5, **and** an argmax share ≥ 0.50 in **both** the joint night bootstrap and the episode bootstrap.** Option B (interval separation alone) is a strict subset of A's conditions, so the two differ only in strictness and the stricter is taken without asking. The Registrar's reason is the right one and is kept verbatim in §8: with nine **correlated** series (§10 threat 3 — O4, O8's L3 row and O9 all contain "did L3 get touched") an interval gap can be produced by one long run of a single symbol across overlapping 60-session windows, and the argmax share is the cheap check that the winner wins in the resampled world too. The 0.50 floor, the 0.05 `SET_SENSITIVE` threshold and the 10-session block length are fixed at this lock and **none is lowered at the run in any branch**. | **DP-45** / the standing rule that where two options differ only in strictness the stricter is taken and not put to Haci; **DP-51** (a condition met on CI-1 and not on CI-2 is not met — already a gate in §8, and it binds both limbs); **DP-26** (the thresholds are lock-time conventions); **Q005 / Q026 / Q028** (thresholds fixed before the run and never adjusted afterwards) |
| 6 | The trading calendar the dates are solved on | DECIDED | **The desk's standard holiday list, which §5.2's list is missing one entry of: 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05 and 2027-09-06** (Correction 1). 2027-06-18 (Juneteenth observed; 2027-06-19 is a Saturday) is listed by Q018, Q020, Q021, Q023, Q024, Q031, Q032, Q033 and both Steward exposure reports. It does **not** touch the 158-session window count (it falls after 2027-04-30) but it moves every +60-session arithmetic that crosses June 2027: **t+60 of 2027-04-30 = 2027-07-28** (not 2027-07-27), **t+60 of 2027-06-14 = 2027-09-09** (not 2027-09-08), and the ceiling back-solve gives **184** admissible elapsed sessions (not 186). The **decision dates are unchanged** — 2027-07-28 + one week = 2027-08-04, first Monday = **2027-08-09**; 2027-09-09 + one week = 2027-09-16, first Monday = **2027-09-20** — because the one-session shift is absorbed by the margin and the first-Monday rule. The **successor price freeze's bar horizon moves out by one session** and the header, §5.2 and §5.3 R2 are corrected to say so. Every date is re-confirmed session by session from the calendar when the freeze is built; a correction may move a date **out, never in**. | ground 3 — one calendar, and a date arithmetic that omits a session is simply wrong; **DP-45** (the omission shortened a freeze horizon; the correction lengthens it); **Q033 DECISIONS #7 / Correction 2**, the identical omission on the identical freeze at the identical lock date; **DP-23** (a successor freeze is built to the horizon the registered population needs) |
| 7 | What "all nine objectives computable" means, and which rate the 80-night floor is projected on | DECIDED | **A night enters the ranking set iff it is a §2.5 contributing night **and each of the nine objectives independently carries ≥ 3 valid published picks on that night, each with ≥ 5 valid matched controls**, after that objective's own exclusions are applied** — O4 after the wrong-side-stop screen, O5 and O8 after the complete-six-level-ladder requirement, every objective after the shared §2.4 screens. **The schedule is built on the measured ranking-set rate**, `min(r_rank,60 , 0.6620)` (item 8's cap), **not** on §5.1's 0.6620 (Correction 4). The draft projects the 80-night floor at 0.6620, a rate measured under §2.5's contributing-night rule alone, which requires neither a usable printed stop — Q009 measured **17.8% (66/371)** of published picks without one — nor a complete ladder across all three lanes; the ranking set is a **subset** of the contributing nights by construction, so the projection is optimistic by an unmeasured amount and **R1(b) measures it before the lock**. The alternative reading (a night is in the ranking set if each objective is computable for *at least one* pick) was refused: it would let a single pick carry an objective's night value while the register's own floor asks for ≥ 3, and it is the reading that reaches the floor sooner. | ground 3 — a floor counted on a ranking set cannot be projected from a rate measured on a larger set; **DP-21** (the stricter reading of rule 6's floors, applied per reported row); **DP-43** (dates projected from the Steward's exposure count at the **measured** run-rate); **DP-45** (never the rate that reaches the floor sooner); **Q033 DECISIONS #6** (the same "numerator and denominator over the same population" construction) |
| 8 | Which measured rate the schedule is built on, given a 60-session maturity and a freeze ending 2026-09-10 | DECIDED | **The scheduling rate is `min(r_rank,60 , 0.6620)`**, where `r_rank,60` is R1(b)'s ranking-set rate (item 7's rule) measured with **numerator and denominator over the same sub-period** — the maximal stretch of 2026-06-01..2026-09-10 whose nights can be graded to **t+60** on `manifest_prices_v001`, whose last pick night the Steward fixes from the calendar — and **0.6620** is the desk's measured published-pick contributing rate (47/71 at t+20, `STEWARD_Q031_exposure.md` §(a), reconfirmed bit-for-bit by `STEWARD_Q032_exposure.md` §(a)(ii)). Every real loss mechanism stays in the denominator (exclusions, DP-04, null / non-monotone ladder, split-scale payload, wrong-side stop, `d_L3` bound, < 5 valid controls, < 60 prior bars, > 25% ungradeable); **only** freeze-horizon censoring is removed, and only because it cannot occur inside the registered window — R2 delivers t+60 bars for every in-window night. The cap is the binding half: **no date is ever computed from a rate faster than the desk's own measured published-pick number**, and a rate slower than 0.6620 governs. §5.1's note that 0.6620 is preferred to Q032's borrowed 0.9538 stands and is correct. | **DP-43**; **DP-45** (the `min`, never the faster rate); ground 3; **Q033 DECISIONS #6**, **Q032 DECISIONS #3** — the identical construction at t+40, adopted here at t+60 rather than re-argued |
| 9 | The rarer-window limb of the lock gate, when the branch that will run is not known at lock | DECIDED | **Both candidate partitions are measured at the lock and the limb is applied to the *lower* measured rate** — the rarer bar-only tape arm (cited from `STEWARD_Q032_exposure.md` §(b) under the registered SMA50-only lower bound rather than re-run) **and** the rarer platform-label arm (R1(c), measured on Q034's own funnel), each as contributing nights per elapsed session against the **≥ 0.11** threshold (20 ÷ 184, rounded up, re-solved at `record`). The branch is not fixed until R2(i) is attempted at the decision pass, so a gate applied to only one partition would be a gate on a coin-flip. Q032 §(b)'s proxy measured HOSTILE at **0.3099/session** — far above §5.1's 0.20 × 0.6620 = 0.132 placeholder — and Q032 §(d) implies a NOTSTRONG share of 14/68 nights; **neither faster number pulls a date in** (DP-45): the placeholder governs the schedule until R1 measures Q034's own funnel, and a measured rate below the placeholder moves every date **out**. | **DP-43** (the floors are projected from the Steward's measured counts, and the window that reaches **every** floor governs); **DP-45** (the lower of two measured rates; never the faster one); **DP-21** (20 per cell, never lowered); item 3 (both partitions are registered windows, so both carry the floor) |
| 10 | O3's definition, which the draft leaves conditional on Q033's lock | DECIDED | **O3 is fixed here and is no longer conditional: the symmetric **±0.5 ATR** band from `X`, an unresolved race scored **0** with the pick kept in the denominator, a same-session pair hourly bars cannot order scored **against the pick and for the control** (§4.0), for picks and matched controls alike; the ±1.0 ATR variant is a printed companion that decides nothing, and H-081's 20-session-sign proxy is a named companion outside the nine.** Q033 DECISIONS #1 and #2 settled exactly these three choices on 2026-09-14, before either question locks, and they are settled **whether or not Q033 itself locks** — if Q033 goes to DEFERRED on its own counts, O3 keeps this definition and `eval.py` cites Q033 DECISIONS #1/#2 rather than a PREREG section that may never exist. The draft's "this row moves with Q033's lock" clause is struck: a definition that can move after this lock is not pre-registered. | ground 2 — a decision already made for the same measurement (**Q033 DECISIONS #1, #2**, same day, same desk); **DP-26**; **DP-27** (the unorderable same-session pair takes the outcome less favourable to the hypothesis); rule 3 (nothing in a locked PREREG may be resolved later by another file) |
| 11 | Exclusions, inside a window every night of which postdates every existing freeze | DECIDED | `eval.py` unions **`research/data/exclusions_v003.json`** — verified the newest file on disk (v001, v002, v003 present) — with the **add-only successor exclusions file** issued with the successor selection freeze, on the identical **four** criteria (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10. The successor file may only **add** nights; no night is removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be; `exclusions_v003.json` is not edited (`research/data/` is not writable from here). Both paths are `eval.py` inputs — no hard-coded file name, no hard-coded date. DP-04 applies mechanically on top. The fourth criterion is load-bearing: on a `payload_disabled` night the published slate carries no `lane_plans`, so there is no ladder, no `d_L3` and no eligible pick for any of the nine — the night is excluded whole rather than entering as nine zeros. | **DP-22** read as "one list, one set of criteria" (its "cite the newest file" clause presumes a sealed window; Q034's is entirely post-freeze); **DP-04**; **Q033 DECISIONS #11**, **Q032 #8**, **Q031 #12**, **Q027 #11** — same construction |
| 12 | A mid-window change to what "a published pick", "its printed L3" or "the committed plan" is | DECIDED | A change to the SAS weights, the timeframe multipliers, `qualification_threshold`, the ATR-elite caps, the GEX offset, a scoring enable-flag, `publication_floor`, `bear_publish_threshold`, `max_output_cap`, `min_completeness`, **`BAND_EXITS`** or the lane-plan writer — **including any promotion of v1.7** — **cuts the window at the ship date**: the post-ship segment becomes the question's window with the whole §5 schedule recomputed from it (**out, never in**, same single extension, same ceiling measured from the original lock), the pre-ship segment becomes a labelled descriptive panel entering no register line, and if neither segment reaches the floors inside the ceiling Q034 is **DEFERRED**. `eval.py` prints the per-night `config_json` composition and **fails loudly** rather than silently excluding. Running the other way (DP-50(b)): every listed change is **flag-off until 2027-08-09** (**2027-09-20** if the extension fires), checked before any fix brief is written — the clause Q027, Q029, Q031, Q032 and Q033 carry. `BAND_EXITS` is named explicitly because **O5's Plan H is defined by it**, which no sibling question's flag-off list needed. A change to `services/market_regime/scorer.py` splits the **platform-label** stability partition at the ship date (item 3's v1.2 guard) and leaves the bar-only arms untouched. | **DP-06** / **DP-50(a)** (a repair or config change splits a column into two features at the ship date); **DP-50(b)** (ship timing checked against in-flight questions, the PI-011 / Q010 pattern); **DP-50(c)** (the sweep runs on the pinned freeze and the read-only repo); **Q033 DECISIONS #12**, **Q032 #9**, **Q031 #13** |
| 13 | The sub-cell suppression list | DECIDED | **Fixed at this lock as §4.3 lists it, revised once at `record` from R1's measured counts, and then closed — and the revision may only move cells ONTO the list, never off it.** Suppression restricts **affirmative reporting only**: it never removes a blocker. The two halves, the two tape arms, the **two platform-label arms** (item 3), the bull-only companion and the nine ranked rows are never on the list and block at whatever count they have. A cell suppressed at lock stays suppressed even if it clears 20 measured nights at the decision pass; a cell not suppressed still needs ≥ 20 **measured** contributing nights to print. Q034's suppressions are **structural** — PI-010's 2–3 elite picks a month against `publication_floor = 80.0`, H-062's bear grading, `confidence_level` / `best_timeframe` / `d_L3` / `atr_pct` thinness — not density expectations R1 can overturn. | **DP-21** (20 per reported cell, no floor moved in either direction); **DP-45** (the stricter of two readings); **Q033 DECISIONS #10**, **Q032 #7**, **Q023 #9**, **Q027 Correction 2** ("suppression never removes a blocker", in the same words) |
| 14 | What a window that misses 20 contributing nights does — §2.2 and §5.2 contradict each other | DECIDED | **Both halves of the contradiction are resolved in the strict direction (Correction 5).** (i) A window short at the initial decision date **fires the single DP-13 extension**, as §5.2 registers — more waiting, never a relaxed test. (ii) After that single extension, a still-short window is handled by §2.2 as drafted — it prints its count, leaves the stability test and is **named** in every stability label — and the register **runs**: a window shortfall is **not** a DEFERRED ground, which stays with the ranking-set 80-night floor and Gate 0. (iii) The price of (ii), which the draft does not charge: **no objective may be named strongest unless the branch's full set of four windows — the two halves and the two arms of whichever partition that branch registers — each clears 20 contributing nights.** Short of that the register's ceiling is **NO_SEPARATION (INCONCLUSIVE)**, with the missing window named in the sentence. Without (iii), a rarer window that never reaches 20 makes STABLE easier and SEPARATED more likely, which is a verdict bought with a shortfall; with it, the NULL branch (NO_STABLE_OBJECTIVE) stays reachable — as it must, since H14's FAIL is a real finding — while the CONFIRMED branch is not reachable on a partial window set. | **DP-43** (demote-not-drop, settled at lock and never afterwards; a floor is never lowered to reach a date); **DP-13** (one automatic extension on measured counts, then DEFERRED); **DP-45** (of the readings available, the one that cannot let a missing window produce a winner); ground 3 — a draft that says both "the extension fires" and "the window removes itself" must be made to say one thing; §2.2 and §8's own "keeps its sign in **every** window" |
| 15 | The family, the correction set, and what §7 asserts about F8's membership | DECIDED | **Q034 carries no primary, enters **no** correction set, and changes no family's denominator — as §7 says.** The one assertion corrected is the count: §7 states F8's correction "at this lock is **Q033's 2**", which is no longer true. `STEWARD_Q032_exposure.md` (2026-09-14) defers **Q032** outright, and Q033's own item 16 branch defers **P2** on the same absent credentials — so F8's primary-carrying membership at this lock is **Q033's 1, or 2 only if Q033's SPY limb clears**, with H-074 / Q030 and Q032 both DEFERRED and their primaries out of the set while deferred. **Must read that way** (Correction 6). Nothing in Q034's own numbers moves with it: a diagnostic that computes no q is unaffected by the size of a set it does not join. | rule 8; **DP-29** (family by the primary endpoint's subject; an overlapping hypothesis is never counted twice); **Q033 DECISIONS #4**, **Q032 #10** (the same bookkeeping, stated symmetrically); ground 3 — a stated count that is false on the day it is written is corrected, not carried |
| 16 | When `eval.py` must be committed | DECIDED | **Written once (rule 9) and committed no later than Monday 2027-04-05, sha256 recorded, not touched afterwards; the extension run uses the byte-identical, unmodified file.** The draft registers no deadline and this question needs one more than any other on the desk: its nine rows **are** the endpoints of questions that decide **before** it — Q006 (2026-10-05), Q002 (2026-10-12), Q027 and Q029 (2027-04-12) on this very window and freeze, Q012 (2027-03-22), Q033 (2027-07-12) and Q018 (2027-07-12) — and a script written after any of those passes is a script written with part of its own answer in view. 2027-04-05 is the Monday before the earliest sibling pass on this window. | rule 9 (a deterministic script written once, no tuning while looking); rule 3; **Q033 DECISIONS #14**, **Q032 #11** (the same deadline, the same reasoning) |
| 17 | The SPY-history probe: already answered, and what it costs Q034 | DECIDED | **The probe is not re-run as a lock gate; `STEWARD_Q032_exposure.md` §(g) is cited — `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` absent, probe not attempted, no pinned alternative (2026-09-14) — and R1 carries a one-line credential re-check only, for the record.** Its failure **defers nothing in Q034**: no endpoint here is an arm contrast, unlike Q032 (deferred outright on this ground) and Q033 (P2 deferred on it). The branch is determined when R2(i) is attempted at the decision pass, and **both branches are registered before the fact** (§2.2, item 3). What the known failure does change, and this is why it is a decision rather than a note: it makes `STABILITY_WITHOUT_TAPE_ARMS` the **expected** branch at lock, so the lock gate's rarer-window limb is applied to both partitions (item 9), the platform-label arms become registered windows in every branch (item 3), and §2.2's fallback sentence is rewritten to say plainly that on today's evidence it is the branch most likely to run. **The partition is never re-specified to an SMA50-only variant after the fact.** | ground 2 — the Steward measured it today under the identical definition and the draft's own R1(b) says a measured limb is cited rather than re-run; **DP-43** (a question defers on a measured ground, not a preference — and here the ground does not reach this question's endpoints); **DP-41** (nothing here asks for a rule-14 exception); **Q030 / H-074**, **Q032 headline**, **Q033 DECISIONS #16** |
| 18 | Window end, decision date, extension, hard stop | **DEFAULTED (R-3)** — **FINAL at `record` (2026-09-14), unchanged** | **Settled on R1's measured rates and nothing moved**: the scheduling rate is `min(0.9091, 0.6620) =` **0.6620** (item 8's cap binds), the rarer registered window measures **0.1972**/elapsed session, floor A (80 ranking-set nights) is reached at session **121**, floor B (20 rarer-window nights) at session **102**, floor C at session **46** — the latest is **121**, inside the registered **158**. Both measured rates are *faster* than §5.1's placeholders, and a faster rate **never pulls a date in** (DP-45, item 18's own rule), so the window end stays **2027-04-30**, the decision date stays **Monday 2027-08-09**, the single DP-13 extension stays **..2027-06-14 / Monday 2027-09-20**, and **2027-09-20 is the hard stop**. Full arithmetic in `## Schedule`. — *original entry:* **Window: pick nights 2026-09-15 .. 2027-04-30 = 158 elapsed sessions** (unchanged unless R1's measured rates push it **out**). **Decision date: Monday 2027-08-09** — 2027-04-30 **+ 60 sessions maturity = 2027-07-28** on the corrected calendar (Correction 1), **+ one calendar week = 2027-08-04**, first Monday on or after. **Single DP-13 extension of +30 sessions** to pick nights .. **2027-06-14** (session 188), decided **Monday 2027-09-20** (2027-06-14 + 60 sessions = **2027-09-09**; + one week = 2027-09-16; first Monday on or after), **which is also the hard stop** — still short there, Q034 goes to DEFERRED. **10.9 months** and **12.2 months** from the 2026-09-14 lock; the initial date is inside DP-43's ceiling and the extended one is permitted by item 4's reading. The **method** is fixed here and is not re-argued with counts in view: window end = the **latest** of floor A (80 nights on the **ranking set**, item 7), floor B (20 contributing nights in the rarer registered window, on the lower of the two partitions, item 9), floor C (30 post-lock nights, satisfied by construction) at item 8's rate; then + 60 sessions + one week, first Monday, moved out again for a holiday. Floor B projects **marginal** (20.9 against 20) on a **placeholder** arm share, which is what DP-13's single extension and the DEFERRED fallback are for; every date moves **out** if R1 measures slower and **never in** if it measures faster. The halves are re-cut on the extended window by the same session-index rule (Half A = sessions 1–94, Half B = 95–188) fixed at this lock. | **DP-43** (the window that reaches every floor at the measured rate, plus the endpoint's maturity and a one-week margin, first Monday on or after; +30-session extension; the ceiling on the initial date); **DP-13**; **DP-21**; **DP-24**; **DP-45** (out only; never the shorter window, never the faster rate, never a maturity shortened below H-084's own deepest objective); not taken: the draft's 186-session / no-extension variant and its 2027-07-27 maturity date |
| 19 | The exposure counts this question has never had | **ROUTED → data-steward — ANSWERED 2026-09-14, gate CLOSED: PASS** | `STEWARD_Q034_exposure.md` delivers every limb on the pinned freezes and the read-only repo, no live query. **Limb (b) ranking-set rate 0.9091 (10/11, t+60 sub-period) → scheduling rate 0.6620 ≥ 0.44 — PASS** under item 21's ruling (the Steward reported the literal-reading 0.0909 and flagged the fork for the desk rather than settling it, which is the right division of labour). **Limb (c) 0.1972 (platform-label NOTSTRONG, the lower partition; bar-only 0.3099 cited) ≥ 0.11 — PASS.** (d) wrong-side swing stop **103/550 = 18.7%** (Q009's 17.8% signature re-measured, same order) and `d_L3` bound **7/550**; (e) complete six-level ladder **534/550 = 97.1%**, nights with < 3 complete-ladder picks **1/68** (2026-06-02, the `analysis_status="disabled"` night); (f) DP-50 sweep **NONE** — HEAD unchanged at `d19c9a9`, `BAND_EXITS` last touched `b24954c` (2026-07-09), an **ancestor** of the pin, v1.7 unscheduled with no start date to count from, to be re-swept at R2(vii) and not assumed clear permanently; (g) credentials absent — **not a gate here** (item 17), and it makes `STABILITY_WITHOUT_TAPE_ARMS` the expected branch, re-attempted at R2(i). Item 7's ranking-set rule is **unchanged**: the Steward measured it as registered, and only the counts moved. — *original request:* waits on **R1** (counts only) — **BLOCKING FOR LOCK**, as §5.3 says. It settles item 18's dates whole and the lock-or-DEFER gate itself: **ranking-set nights ≥ 0.44** per elapsed session (80 ÷ 184) and **rarer registered-window contributing nights ≥ 0.11** per elapsed session (20 ÷ 184), the latter on the **lower** of the two partitions (item 9), both re-solved from the trading calendar at `record`. Both limbs clear → Q034 locks with §5.2 recomputed **out**; either limb short → **DEFERRED** with the measured counts and the re-check trigger named. | — |
| 20 | Successor freezes | ROUTED → data-steward | waits on **R2** — the shared successor pair (selection: `sas_candidates` **every row, published and unpublished**, `sas_runs`, `market_regime_daily` with `created_at` and `regime_version` preserved; prices: daily bars for **every candidate symbol on every in-window night**, hourly for published symbols, SPY split-adjusted from 2025-01-02), with Q034's own scope requirement: **daily bars through t+60 of the last in-window pick night — 2027-07-28** (Correction 1), and **2027-09-09** on the extension path. Due before the decision date; **not a blocker for lock** (DP-23). **Still ROUTED and OPEN at `record`.** Its dates are now **final, not provisional** (item 18, unchanged): daily bars through **2027-07-28**, delivered before **2027-08-09**; on the extension path through **2027-09-09** for **2027-09-20**. R2(vii) repeats R1(f)'s sweep, `BAND_EXITS` included, for the period between the freezes. | — |
| 21 | **The §2.4 monotonicity screen's reading — strict or ties-allowed** (raised at `record` by `STEWARD_Q034_exposure.md`; the limb the lock turned on) | DECIDED | **The clause is a mis-transcription of the platform's own invariant and is corrected to non-strict, with the reason recorded.** §2.4 must read: *"any flattened level with `dir × (L − C_t) ≤ 0`, the six flattened levels **not monotone non-decreasing in the pick's direction (ties across lanes allowed — the platform's own predicate `_ladder_is_monotonic`, `services/super_agent_select_service.py:180-192` at the pinned SHA `fa70688`: bullish `all(b >= a)`, bearish `all(b <= a)`)**, or `outcome_target_invalid` non-null → the pick is excluded from every objective and counted."* The word **"strictly" is struck** wherever this screen is referenced (§2.4, §4.6(c), §10 threat 13). **The Steward's ties-allowed counts are therefore the registered counts:** `valid_shared` **476/550** (not 104), ranking set **10/11 = 0.9091** on the t+60-evaluable sub-period, scheduling rate **0.6620**. **Three guards ride with the correction, none of them loosening anything:** (i) `eval.py` prints the screen's own firing rate per window and per objective and **fails loudly** if it exceeds the pre-fix **25.71%** measured in DATA_NOTES — the post-ship measured rate is **0.00% (0 of 355)** and Q034's window is entirely post-ship, so a material rate is a platform-defect flag, exactly as Q032 §2.4 words it; (ii) the **strict variant is printed as a counted companion** (rows passing non-strict and failing strict) per window and per objective, so the register shows on its face what the reading cost and no later reader has to take it on trust; (iii) a tied pair `L_k = L_{k+1}` is graded on **both** levels for picks and, through the identical `d_Lk` transfer of §3 B1, for controls — so picks and controls are treated identically and Gate 0(c)'s within-lane identity holds with equality. **Stated without hedging, so DP-45 does not fire** — and the ruling is made on the pinned code and on the draft's own stated expectation for the screen, not on which reading locks: it reads the same way had the counts pointed the other direction, and it is recorded before any outcome exists. **Cross-question exposure is flagged, not fixed** (Correction 7). | **ground 3** — a screen that transcribes an external invariant has one defensible reading, and it is the invariant's; the platform predicate **verified read-only** at the pinned SHA (`:180-192`, `:195-257`, commit `5fa3db4` 2026-07-06, an ancestor of `fa70688`) with its docstring's *"equal prices across lanes are allowed (non-strict monotonicity)"*; **intent evidenced inside the draft** — §6's "sits after the `_enforce_ladder_monotonic` ship", §4.6(c)'s "guaranteed by the monotone ladder screen", §10 threat 13's filing of non-monotonicity as a **defect**, and the registrar's twin clause in **Q032 §2.4** ("a non-zero rate is a **loud flag**"); **DATA_NOTES** (steward, Q018 R1) 25.71% pre-fix → **0.00% post-fix** under the same non-strict definition; **DP-26** (a lock-time convention derived from no outcome, corrected before lock); **DP-50(c)** (code read read-only at the pin, never HEAD, never a live query) |

## Corrections to silent choices

**Eight** (the seventh and eighth added at `record`). The Registrar applies them at `apply` with the rest of this file. Every one moves a date out,
strikes a statement that is false or no longer true, or tightens a clause; none weakens a floor, a
window, a threshold or a gate.

1. **§5.2's holiday list omits 2027-06-18 (Juneteenth observed), and the header, §5.2 and §5.3 R2
   carry the resulting maturity dates.** **Must read:** the list is 2026-11-26, 2026-12-25,
   2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05 and
   2027-09-06 (the last for the ceiling back-solve only); **t+60 of 2027-04-30 = 2027-07-28** (the
   draft's "60 on 2027-07-27" is one session early), so the successor price freeze carries daily bars
   through **2027-07-28**, and on the extension path **t+60 of 2027-06-14 = 2027-09-09** (not
   2027-09-08), bars through **2027-09-09**. The **decision dates do not move** — 2027-08-09 and
   2027-09-20 both stand — and the 158-session window count is unaffected. (DP-43, DP-45, DP-23;
   Q033 Correction 2, same omission, same day.)
2. **§5.3 R1's ceiling back-solve gives 186 admissible elapsed sessions and the corrected calendar
   gives 184.** Latest admissible initial decision Monday 2027-09-13 → last t+60 on or before
   2027-09-06 → **2027-09-03** (2027-09-06 is Labor Day) → window end **2027-06-08 = session 184**.
   **Must read:** 184 admissible elapsed sessions; ranking-set nights **≥ 0.44** and rarer-window
   contributing nights **≥ 0.11** per elapsed session (80 ÷ 184 and 20 ÷ 184, rounded **up** — the
   same rounded values the draft prints, from the correct denominator), **re-solved at `record` from
   the trading calendar and again if the lock date moves**.
3. **§2.2's `STABILITY_ON_HALVES_ONLY` branch removes half the stability test on a provisioning
   failure the desk already knows about.** **Must read (item 3):** the platform-label arms
   (`STRONG` = `market_regime = 'strongly_bullish'` on a legality-tested v1.2 row, else `NOTSTRONG`)
   are a **registered stability window in every branch**, at the same 20-night floor, with illegal
   nights carrying no platform-label window and counted, and with `eval.py` failing loudly on a
   `regime_version` other than v1.2; §4.3's and §4.4's "descriptive composition cross-check only" is
   amended to "a registered stability window **and** a composition cross-check, carrying no q and
   defining no arm contrast"; the qualifier is renamed **`STABILITY_WITHOUT_TAPE_ARMS`** wherever
   `STABILITY_ON_HALVES_ONLY` appears (§2.2, §8, §10 threat 12), and the branch sentence states
   plainly that on `STEWARD_Q032_exposure.md` §(g)'s evidence it is the branch most likely to run.
   The bar-only partition is unchanged and is never re-specified. (rule 7, DP-45, DP-26, DP-06.)
4. **§5.1 projects the ranking set's 80-night floor at a rate measured on a larger population.**
   0.6620 is §2.5's contributing-night rate; the 80-night floor is on the **ranking set**, which also
   needs a usable printed swing stop (O4) and a complete six-level ladder (O5, O8) for ≥ 3 picks per
   night. **Must read:** the scheduling rate is **`min(r_rank,60 , 0.6620)`** (items 7, 8), measured
   by R1(b) with numerator and denominator over the same t+60-gradeable sub-period; §5.2's projection
   table is rebuilt at `record` from R1's measured rates, **out only**; §5.1's "the rate per elapsed
   session is unchanged by the t+60 maturity" is true of the *contributing-night* rate and is not
   asserted of the ranking-set rate, which has never been measured.
5. **§2.2 and §5.2 give two different answers for a window below 20 contributing nights** — §2.2 says
   it prints its count and leaves the stability test, §5.2 lists "20 in each of the four windows" as an
   extension-then-DEFERRED gate. **Must read (item 14):** a short window fires the **single DP-13
   extension**; after it, a still-short window leaves the stability test and is **named**, the register
   runs, and **no objective may be named strongest unless the branch's full four-window set each
   clears 20 contributing nights** — the ceiling in that branch is NO_SEPARATION (INCONCLUSIVE).
   DEFERRED stays with the ranking-set 80-night floor and Gate 0.
6. **§7's "F8's correction … at this lock is Q033's 2" is no longer true on the day it is written.**
   `STEWARD_Q032_exposure.md` (2026-09-14) defers Q032 outright and Q033's item 16 branch defers its
   P2 on the same absent credentials. **Must read:** F8's primary-carrying membership at this lock is
   **Q033's 1 (2 only if Q033's SPY limb clears)**, with H-074 / Q030 and Q032 DEFERRED and their
   primaries out of the set while deferred; **Q034 carries no primary, enters no correction set and
   changes no family's denominator**, which is unaffected by the count. (rule 8, DP-29.)

7. **§2.4's ladder screen says "not strictly monotone" where the platform invariant it transcribes is
   non-strict** (added at `record`, item 21). **Must read:** *"the six flattened levels **not monotone
   non-decreasing in the pick's direction** — ties across lanes allowed, the platform's own
   `_ladder_is_monotonic` predicate (`services/super_agent_select_service.py:180-192` at the pinned
   `fa70688`: bullish `all(b >= a)`, bearish `all(b <= a)`), whose docstring records that **"equal prices
   across lanes are allowed (non-strict monotonicity), as duplicates already exist in the book and
   grading handles them"***; "strictly" is struck at §2.4, §4.6(c) and §10 threat 13; §4.6(c) must add
   that the within-lane identity **holds with equality** when two levels tie; §2.4 gains the loud-flag
   clause (firing rate printed per window and per objective, `eval.py` failing loudly above the pre-fix
   **25.71%**, against a measured post-ship **0.00%**) and the **counted strict-variant companion**.
   Under the literal wording the screen excluded **429 of 550 rows (78%)** of which **388 were ties**;
   under the correction it excludes the **41 true reversals**, all of which sit in the pre-2026-07-06
   segment of the exposure period and none of which can occur inside the registered window on
   DATA_NOTES' measurement. (Platform code verified read-only at the pin; DATA_NOTES, steward Q018 R1;
   Q032 §2.4's "loud flag" sentence; DP-26, DP-50(c).)

8. **§5.1's sizing table, §5.2's projections and §10 threat 7 are written on placeholders that R1 has
   now replaced** (added at `record`; this is Correction 4's promised rebuild, with the numbers).
   **Must read:** the HOSTILE-share row loses its **0.20 planning placeholder** and the rarer-window row
   is rebuilt on the **measured 0.1972** contributing nights per elapsed session (platform-label
   NOTSTRONG, the lower of the two partitions, `STEWARD_Q034_exposure.md` §(c); bar-only HOSTILE
   0.3099 cited); the ranking-set row carries the **measured 0.9091** with the scheduling rate
   **`min(0.9091, 0.6620) = 0.6620`** and a footnote that the sub-period measured is pre-2026-07-06 and
   therefore a **lower bound** for the registered window; the projection table reads floor A at session
   **121** (104.6 nights at 158), floor B at session **102** (31.2 at 158), floor C at session **46**;
   the wrong-side-swing-stop row is re-measured at **103/542 = 19.0%** (18.7% of all 550) against
   Q009's 17.8%, and the complete-six-level-ladder row is added at **534/550 = 97.1%** with **1 of 68**
   nights below 3 such picks. **§10 threat 7 must stop saying the rarer window "binds and projects
   marginal (20.9 against 20)"** — it is measured at **31.2** and the **ranking-set floor A binds
   instead**; the threat is **re-worded, not deleted**, to say that the arm was sized on a placeholder,
   that R1 measured it before the lock, and that a window failing to reach 20 still removes itself from
   the stability test, is named, and cannot silently weaken a label (item 14). **No date changes**:
   every measured rate is faster than its placeholder and a faster rate never pulls a date in.
   (DP-43, DP-45, item 18.)

**For the Red Team — cross-question exposure of Correction 7, flagged and not acted on here.** The
identical clause ("the flattened six levels not **strictly** monotone in the direction") appears in
**Q033 §2.4** (`PREREG_DRAFT`) and **Q032 §2.4** (`DEFERRED`). Q033 must take the same correction at its
own `apply` / `record` pass or it will exclude ~78% of its rows for the same transcription reason and its
own exposure counts will be measured against a screen its registrar did not intend; Q032 is DEFERRED and
is **not edited** here on any account. **No locked PREREG is affected** — Q027 and Q031 register no
cross-lane monotonicity screen at all, so the class is confined to the three drafts written on
2026-09-14. Q034 does not edit another question's file.

Checked and **not** corrections — each already matches the policy: **binding maturity 60 sessions**,
with §2.3, §2.4, §2.5, §5.2's arithmetic and §5.3 R2's bar horizon all computed on 60 (the error Q032
and Q033 both carried is **not** present here — DP-43's "the endpoint's maturity window"); entry the
**session t+1 regular-session open** for picks and matched controls alike, with **DP-11 correctly not
fired** and the `C_t` basis a printed sensitivity that never decides (**DP-03(b)**, **DP-42**); L3 on
the DP-09 20-session clock for O4 and O9 with the 40-session companion descriptive (**DP-09**); a level
at or through `X` at the t+1 open scored **not a hit** with the pick kept in the denominator and the
not-takeable count printed per objective (**DP-26**, rule 5); **no stop assumed anywhere** — O4 races
against the printed **swing** stop and O5's Plan H carries none, counter-direction touches and MAE at
40 and 60 sessions reported and never used as exits (**DP-02**, **DP-30**); an unorderable same-session
race scored against the pick and for the control (**DP-27**); published = **`qualified IS TRUE AND
selected_rank IS NOT NULL`**, dark-lane rows only ever in the control pool (**DP-28**); the B1 control
construction **Q006 §3 verbatim** with every synthetic construct at the identical ATR distances,
controls never adding to inferential n, a pick with < 5 valid controls dropped and counted and never
imputed (rule 5, rule 6); floors read as **80 contributing nights per reported row and 20 per window
and per reported cell**, the stricter reading, never lowered (**DP-21**); **≥ 30 contributing nights
after the lock commit** satisfied by construction, so **DP-31** correctly does not apply and no
successor replication question is owed (**DP-24**); PROSPECTIVELY_CONFIRMED **declined in every
branch** for the right reason — no primary, no MPE, no BH, nine simultaneous comparisons — with the
fixed labels `DIAGNOSTIC — no primary, no MPE, no BH` and `NON_QUOTABLE` carried wherever the verdict
is restated (rule 10, rule 12); **no MPE invented in any unit**, with DP-10 / DP-20 / DP-44 cited as
considered and inapplicable and the §8 thresholds serving their role, fixed before the run
(**DP-44**); units and the list of nine taken from **H-084 as filed** and not re-united to reach a date
(**DP-25**); successor freezes covering **every candidate symbol, published and unpublished**
(**DP-23**); **two CIs on every number**, with CI-1-clears-CI-2-does-not **not met** (**DP-51**, a
gate here and not a footnote, correctly identified as live at a 60-session horizon); Plan H inherited
from **Q012 §4** with the non-deterministic trailing text ignored (the Q011 / Q012 precedent);
Registrar conventions fixed before any outcome exists — the SMA50 / SMA200 / 20-session-vol cuts, the
expanding-window terciles with the ≥ 250-session requirement, the BENIGN definition, the 10-session
block length, seed 20260914, the session-index half split, the 25%-ungradeable night rule, the 0.05
`SET_SENSITIVE` threshold, the 0.50 argmax floor, |SMD| ≤ 0.25 (**DP-26**), none promotable at the
decision pass; the exposure counts taken from the **pinned freeze** and the read-only repo, never a
live query (**DP-50(c)**); `uoa_symbol_daily.fwd_return_*` banned (FREEZE_v001 §5) and
`sas_selection_excursion` / `outcome_*` / `level_hit_*` never inputs; no number read from another
question's `results/`; and **no rule-14 exception requested or needed** (**DP-05** untouched,
**DP-41** respected).

## Defaulted on Haci's behalf

- #18 Window end, decision date and hard stop — chose **2026-09-15 .. 2027-04-30, decision Monday
  2027-08-09, single extension to 2027-06-14 decided Monday 2027-09-20**; not taken: a 184-session
  window decided 2027-09-13 with no extension — DP-43. Overturn = successor question.

**Confirmed at `record` (2026-09-14) and still one item.** R1's measured rates changed no date: both are
faster than the placeholders they replace and a faster rate never pulls a date in. The new ruling of this
pass — **#21**, that §2.4's ladder screen reads non-strictly because it transcribes the platform's own
invariant — is **DECIDED, not defaulted**: it rests on the pinned code, on the draft's own stated
expectation for the screen and on DATA_NOTES' measurement, so no part of it is Haci's to settle and it
adds nothing to this list.

**One item, and it is one cost: waiting eleven months, twelve if the extension fires.** Everything
else met a DECIDE ground, and none of the five the Registrar raised is a question about how he trades
— the entry, the clock, the level and the lane come from DP-03 / DP-09 / DP-42 as already locked in
Q002–Q033, the common scale is a measurement device rather than a trade (DP-26), and this question
**invents no MPE at all**, which is the usual reason an R-4 reaches him. What is worth seeing on the
board is not the date but the branch: **the SPY history Q034's tape arms need is already known to be
unavailable** (`STEWARD_Q032_exposure.md` §(g), today), which deferred Q032 outright and defers
Q033's P2 — and Q034 survives it only because the draft pre-registered a fallback. That fallback was
too generous as written, so the platform's own regime label now carries the stability test in every
branch and no winner may be named on a partial window set. Q034 asks Haci to wait a year for a
register that **confirms nothing and quotes nothing**; its only output that travels is a routing
decision, and the most likely useful outcome is the sentence in §9.1 — that the objective the desk
already measures is the right one.

## Routed requests

### data-steward — R1 (counts only) — **BLOCKING FOR LOCK**

Q034 (of the nine ways the desk can measure a pick, which one does VolatilX predict best — PREREG
§5.3 request R1, as amended by DECISIONS items 7, 9 and 17) needs a **counts-only** exposure
measurement on the **frozen** data — `research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json` against `research/data/exclusions_v003.json`, plus read-only
`git log` / `git show` in the platform repo — and **never a live query** (DP-50(c)). It is **blocking
for the lock**, and its binding limb is one no desk report has measured: Q034's 80-night floor sits on
a **ranking set** — nights where *all nine* objectives are computable — which is strictly thinner than
the contributing-night series your Q031 and Q032 reports counted. **No outcome of any kind:** no touch,
no first-touch date, no return, no excursion, no `outcome_*` column, no `sas_selection_excursion`, no
`uoa_symbol_daily.fwd_return_*`, and no window-versus-outcome cross-tab of any shape; forward bars may
be read **only** to establish that a bar exists (gradeability and maturity accounting), never for a
value. Period: pick nights **2026-06-01..2026-09-10** (DP-06's segment; every window label here is a
16:05 property with no outcome attached, so the widest legal span is used); **denominator for every
rate = elapsed sessions** (calendar sessions minus holidays, exclusions *not* pre-removed — the Q019 /
Q022 / Q023 / Q027 / Q031 / Q032 convention), with `exclusions_v003` nights and DP-04 late-`finished_at`
nights removed from the numerator. Please return, by month and for the period as a whole: **(a) the
§2.4 funnel and the §2.5 contributing-night rate at a 60-session maturity** — a non-excluded night
carrying **≥ 3 valid published picks** (DP-28's predicate, after the null-ladder, wrong-side /
non-monotone, split-scale, `d_L3 ∈ [0.25, 10]` and ≥ 60-prior-bar screens), **each with ≥ 5 valid
matched controls** — reported three ways: (i) numerator and denominator both over the **maximal
sub-period whose nights grade to t+60** on `manifest_prices_v001` (please state that sub-period's last
pick night, derived from the calendar), (ii) the same rule at **t+20** for comparability with your
0.6620, and (iii) the full-denominator t+60 rate for the record. **(b) The ranking-set rate, which is
the limb that decides** — the same nights, further restricted to those on which **each of the nine
objectives independently carries ≥ 3 valid picks, each with ≥ 5 valid controls**, after that
objective's own screen: **O4** after the wrong-side-**swing**-stop screen, **O5** and **O8** after the
requirement of a complete six-level ladder across all three lanes (`day_trading`, `swing_trading`,
`longterm_trading` each carrying two targets), the rest after the shared screens; please report the
per-objective night counts side by side, name which objective is the binding one, and give the
ranking-set rate in the same three forms as (a). **The schedule is built on `min` of (b)(i) and
0.6620** (DECISIONS item 8), so a rate faster than 0.6620 changes no date. **(c) The rarer-window
limb, on both candidate partitions** (DECISIONS item 9), because the branch is not fixed until the
decision pass: for the **platform-label** partition — `STRONG` iff `market_regime_daily.market_regime
= 'strongly_bullish'` on a **legality-tested** v1.2 row (row dated t, regime not unknown,
`data_quality` not insufficient, `created_at` dated t and ≤ that night's `sas_runs.finished_at` — your
Q032 §(d) test) — the nights per arm **on Q034's own contributing nights**, which arm is the rarer one,
its contributing nights per elapsed session, and the count of nights failing the legality test; and for
the **bar-only tape** partition, **please cite `STEWARD_Q032_exposure.md` §(b)/(c) rather than re-run
it** (the SMA50-only bound, HOSTILE the rarer and lower-bounded arm at 0.3099/session, and the
never-reached ≥ 250-session requirement), noting only whether Q034's stricter funnel (≥ 3 picks, ≥ 5
controls, against Q032's ≥ 1 and ≥ 3) changes the arm counts materially. **(d) Two counts on the
published slate: the number and share of picks whose printed swing stop is on the wrong side of `C_t`**
(Q009 §1's 17.8% signature, re-measured on this period — it is O4's denominator) **and the number
excluded by the `d_L3 ∈ [0.25, 10]` validity bound**. **(e) The count and share of published picks
carrying a complete six-level ladder across all three lanes** — O8's and O5's denominator — **and the
share of nights on which fewer than 3 picks carry one**. **(f) The DP-50(a)/(b) commit sweep since
manifest SHA `fa70688`** — any change to the SAS weights, timeframe multipliers,
`qualification_threshold`, `publication_floor`, `bear_publish_threshold`, `max_output_cap`,
`min_completeness`, the ATR-elite caps, the GEX offset, the scoring enable-flags, **`BAND_EXITS`
(`scripts/generate_sas_trading_guide.py:89-95`, which defines O5's Plan H and no sibling question's
sweep named)** or the lane-plan writer — **with an explicit answer even when it is "none"**, plus
whether the **v1.7** workstream is scheduled to ship inside 2026-09-15..2027-09-20; cite your Q032 §(f)
sweep where HEAD is unchanged and add only the `BAND_EXITS` limb. **(g) A one-line credential re-check
for the record only** — whether `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` are present in this session.
**This limb is not a gate for Q034 and does not defer it** (DECISIONS item 17): the probe itself is
cited from your `STEWARD_Q032_exposure.md` §(g), Q034's tape arms are stability *windows* rather than
an arm contrast, and both branches are pre-registered — the answer only records which branch is
expected. **The call this request decides**, with every branch fixed before your counts are seen:
**ranking-set nights ≥ 0.44 per elapsed session** (limb (b)) and **rarer registered-window
contributing nights ≥ 0.11 per elapsed session** (limb (c), applied to the **lower** of the two
partitions) — the floors 80 and 20 divided by the **184** elapsed sessions still admissible under
DP-43's 12-month ceiling at a 2026-09-14 lock with **60** sessions of maturity and a one-week freeze
margin (latest admissible initial decision Monday 2027-09-13, back-solving through a last t+60 of
2027-09-03 to a window end of 2027-06-08), rounded **up**, and please **re-solve them from the trading
calendar** rather than taking my arithmetic — the holiday list used here is 2026-11-26, 2026-12-25,
2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05 and 2027-09-06.
Both limbs clear → **Q034 locks**, with the window end set to the **latest** of floor A (80 ranking-set
nights), floor B (20 contributing nights in the rarer registered window) and floor C (30 post-lock
nights, satisfied by construction) at your measured rates, and every date moved **out** if those rates
are slower than §5.1's placeholders, **never in**. Either limb short → **Q034 goes to
`research/questions/DEFERRED.md`** with the measured counts and the re-check trigger *"the Steward
measures ≥ 0.44 ranking-set nights and ≥ 0.11 rarer-window contributing nights per elapsed session over
a trailing quarter"*, and it is **not** re-registered on a thinner objective list — dropping an
objective is re-uniting H-084's own list (DP-25). Please also state **the projected date each floor is
first reached** at each measured rate, on **60** sessions of maturity plus a one-week freeze margin, and
flag any §4.3 sub-cell projecting below 20 contributing nights at that date (the suppression list may
only gain cells at `record`, never lose them — DECISIONS item 13). Report to
`research/reports/STEWARD_Q034_exposure.md`.

### data-steward — R2 (successor freezes) — due before the decision date, **not** a blocker for lock

Q034 (PREREG §5.3 request R2, DP-23) needs successor freezes before its decision pass; **the dates
below are provisional until R1 lands and may only ever move out** (DP-43, DP-45). Please build and pin
a successor **selection** freeze (the same SQL and the same exclusion criteria as v001, over
`sas_candidates` for **every candidate row, published and unpublished**, plus `sas_runs` and
`market_regime_daily`) and a successor **price** freeze (`prices_daily_split`, `prices_daily_raw`,
`prices_hourly_raw`), covering pick nights **2026-09-15 .. 2027-04-30** (the window end fixed at
`record`, out only) with **≥ 60 prior sessions before 2026-09-15**; and — only if the single DP-13
extension fires — a second pair covering pick nights **.. 2027-06-14**, built then and not before.
**This is Q033's R2 build with the daily tail extended from t+40 to t+60**, so please build the
selection freeze **once** and serve Q027, Q029, Q031, Q033 and Q034 from it where the calendar permits;
their own pins are unaffected and are not edited. Seven scope requirements, none optional: **(i) SPY
split-adjusted daily bars from 2025-01-02** through the freeze end — without them §2.2's `SMA200` and
its 250-session volatility tercile do not exist and **no tape window can be assigned**; if the extended
history cannot be obtained (the Q030 / H-074 blocker, which `STEWARD_Q032_exposure.md` §(g) reports
unresolved as of 2026-09-14), the **`STABILITY_WITHOUT_TAPE_ARMS` branch fires** — the tape arms print
`UNAVAILABLE`, the stability test runs on the two calendar halves and the **two platform-label arms**
(DECISIONS item 3), and the partition is **never** re-specified to an SMA50-only variant after the fact.
**(ii)** The daily bar horizon runs to **session t+60 of the last included pick night** — **2027-07-28**
on the corrected calendar (DECISIONS Correction 1: the PREREG's 2027-07-27 is one session early),
delivered before the **2027-08-09** decision date; on the extension path, through **2027-09-09** for a
**2027-09-20** decision. **(iii)** The daily symbol list covers **every candidate symbol on every
in-window night, published and unpublished**, with ≥ 60 prior sessions before 2026-09-15 (the matched
controls need their closes, `beta60`, `atr_pct`, `runup20` and forward bars to t+60), never assumed
from an earlier freeze's symbol list. **(iv)** Hourly bars scoped to at least the published-pick
symbols — **not** purely descriptive here: §4.0's same-session ordering of O3's band race and O4's
target-versus-stop race reads them, and a pair they cannot order is scored against the pick (DP-27), so
please state their coverage explicitly. **(v)** `market_regime_daily` included with **`created_at` and
`regime_version` preserved** — under DECISIONS item 3 the platform label is now a **registered
stability window**, not only a cross-check, and `eval.py` fails loudly on a `regime_version` other than
v1.2 for an in-window night. **(vi)** An **add-only successor exclusions file** applying the identical
four criteria (`manual_runs`, `non_session_runs`, `uncorroborated_publication_runs`,
`payload_disabled_runs`) to post-2026-09-10 nights — it may add nights and may never remove one, and its
header should state whether the `analysis_status = "disabled"` / no-`lane_plans` signature is still
present and still a first-published-night-of-the-month pattern, saying so explicitly rather than
silently returning an empty list. **(vii)** Rows whose bars are missing are **excluded and counted,
never back-filled or imputed**, and R1(f)'s commit sweep is repeated for the period between the freezes
— **including `BAND_EXITS`, which defines O5's Plan H** — with a dated `DATA_NOTES.md` entry for any
repair that rewrites historical rows and an explicit answer **even when it is "none"**. **The DP-50(a)
guard is load-bearing where this freeze overlaps Q033's**, which shares this window: the overlapping
rows are compared and `eval.py` **fails loudly** on any disagreement, SPY's own daily bars included.
Please re-confirm every §5.2 date **session by session from the trading calendar** when the freeze is
built; the holiday list is 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26,
2027-05-31, **2027-06-18**, 2027-07-05 and 2027-09-06. A correction to any date may move it **out,
never in**.

## Schedule

**FINAL — recorded 2026-09-14 on `STEWARD_Q034_exposure.md` (R1), under item 21's ruling on the §2.4
monotonicity reading.** Every rate below is measured on Q034's own funnel, on the pinned freezes, by the
Steward. Both measured rates are **faster** than §5.1's placeholders and **not one date moves in**
(DP-43, DP-45, item 18): the registered window, the decision date, the extension and the hard stop are
exactly as drafted, and the only thing that changed is that the margins are now known instead of
assumed.

decision_date: **2027-08-09** (Monday) · extension_date: **2027-09-20** (Monday — DP-13's single
automatic extension of +30 sessions; then DEFERRED, there is no second pass) · hard_stop: **2027-09-20**
· rule: **exposure-driven**

- **window:** pick nights **2026-09-15 .. 2027-04-30** = **158 elapsed sessions**; extended window
  .. **2027-06-14** = 188 sessions · **extended: false**
- **halves:** Half A = sessions 1–79 = 2026-09-15..2027-01-06; Half B = sessions 80–158 =
  2027-01-07..2027-04-30 — fixed by session index at this lock and re-derived from the calendar;
  re-cut by the same rule on the extended window (Half A = 1–94, Half B = 95–188).
- **measured rates (R1, per elapsed session):** scheduling rate **0.6620** = `min(r_rank,60 , 0.6620)`
  with `r_rank,60 = 10/11 = 0.9091` on the t+60-evaluable sub-period (item 8's cap binds, which is the
  conservative half by construction); rarer registered window **0.1972** (platform-label NOTSTRONG,
  14/71 — the **lower** of the two partitions, item 9; bar-only HOSTILE 0.3099 cited from
  `STEWARD_Q032_exposure.md` §(b)). The ranking-set and contributing-night sets **coincide** on the
  measured sub-period under the corrected screen (the same 10 nights of 11), and that sub-period
  (2026-06-01..06-15) sits **before** the 2026-07-06 ladder fix, where the non-strict screen still fires
  at 25.71% against **0.00%** inside the registered window — so the measured ranking-set rate is a
  **lower bound** for the window actually registered, and the cap governs regardless.
- **binding floor: A** — ≥ 80 contributing nights on the **ranking set** at 0.6620 → `ceil(80 ÷ 0.6620)`
  = session **121** (= 2027-03-09), projecting **104.6** nights at session 158. Floor **B** (≥ 20 in the
  rarer registered window) at 0.1972 → `ceil(20 ÷ 0.1972)` = session **102** (= 2027-02-09), projecting
  **31.2** nights at 158 — §5.1's "marginal at 20.9" was the placeholder's artefact and the measured
  arm is **not** marginal; §10 threat 7 is answered by measurement and must be re-worded to say so, not
  deleted. Floor **C** (DP-24, ≥ 30 post-lock nights) at session **46**, satisfied by construction.
  Latest of the three = **121**, inside the registered **158**, so the window end is **not pulled in**
  (DP-45; a floor reached sooner never shortens a registered window).
- **projected contributing nights at session 158, every registered window** — none below 20, so item
  14's demotion clause is **not engaged at projection** and stays in force on `eval.py`'s own measured
  counts at the decision pass: ranking set **104.6**; Half A **52.3**; Half B **52.3**; platform-label
  STRONG **109.0**, NOTSTRONG **31.2**; and, if R2(i) delivers, bar-only BENIGN **≈ 109**, HOSTILE
  **≈ 49**. Post-lock nights **104.6** (DP-24 satisfied, not invoked).
- **decision date arithmetic** (holidays 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15,
  2027-03-26, 2027-05-31, **2027-06-18**, 2027-07-05, 2027-09-06 — item 6 / Correction 1): window end
  **+ 60 sessions maturity** (§2.3's binding maturity, the long lane's own window) **+ one calendar
  week** freeze margin, **first Monday on or after**, moved out again for a market holiday.
  **2027-04-30** (Friday, session 158) + 60 sessions: **20** sessions to **2027-05-28** (May has 21
  weekdays less Memorial Day 2027-05-31), **41** to **2027-06-30** (June has 22 weekdays less Juneteenth
  observed **2027-06-18**), then July (22 weekdays less July 4 observed **2027-07-05**) carries sessions
  42–60 — **session 60 = 2027-07-28** (Wednesday). + one calendar week = **2027-08-04** (Wednesday);
  first Monday on or after = **Monday 2027-08-09**, not a holiday. **Extension:** session 188 =
  **2027-06-14**; + 60 sessions = 11 sessions to 2027-06-30, 32 to 2027-07-30, 54 to 2027-08-31, then
  2027-09-01/02/03 = 55/56/57, Labor Day **2027-09-06** skipped, 2027-09-07/08/09 = 58/59/**60** →
  **2027-09-09** (Thursday); + one week = 2027-09-16; first Monday on or after = **Monday 2027-09-20**.
  Both dates are one session's worth of slack later than the draft's arithmetic and **both land on the
  same Monday** — the shift is absorbed by the margin and the first-Monday rule, and only the successor
  **bar horizons** move out (Correction 1).
- **12-month ceiling check (item 4):** lock **2026-09-14** + 12 months = **2027-09-14**. The **initial**
  decision date **2027-08-09** is **10.9 months** — inside, with 36 days to spare. **Not DEFERRED.** The
  extended decision **2027-09-20** (12.2 months) is DP-13's single automatic extension and is permitted
  by item 4's reading; the ceiling binds the initial date only.
- **DEFERRED fallback (unchanged, the hard stop):** if any gate — 80 ranking-set nights, 20 in each
  registered window, or Gate 0 — is still short at **2027-09-20** on `eval.py`'s own measured counts
  after the single extension, **Q034 goes to `research/questions/DEFERRED.md`** with those counts, the
  re-check trigger *"the Steward measures ≥ 0.44 ranking-set nights and ≥ 0.11 rarer-window contributing
  nights per elapsed session over a trailing quarter"*, and it is **not** re-registered on a thinner
  objective list (DP-25). No second extension, no reduced floor, and a gate shortfall is never an
  INCONCLUSIVE register. The Gate 0 fix-and-re-run loop's hard stop is the same **2027-09-20**.
- **maturity:** **60 sessions**, uniform across every eligible pick and every matched control, so no
  objective is right-censored and all nine are measured on the same picks and nights; O4's and O9's own
  clock stays **20** and **5** sessions from `X` (DP-09, Q002's S3).
- **gates, all on `eval.py`'s measured counts and none reduced:** ≥ 80 contributing nights per reported
  row on the ranking set; ≥ 20 per registered window; ≥ 30 dated after the lock commit; ≥ 3 valid
  published picks per contributing night **per objective** (item 7); ≥ 5 valid matched controls per
  pick; ≤ 25% ungradeable picks per night; Gate 0's six construction checks, at most two fix-and-re-run
  passes inside the hard stop, no target relaxed.
- **lock-or-DEFER gate: CLOSED — PASS on both limbs** (R1, 2026-09-14; thresholds re-solved by the
  Steward from the trading calendar on **184** admissible elapsed sessions, Correction 2, and they agree
  with this file's arithmetic). Limb (b) **0.6620 ≥ 0.44**; limb (c) **0.1972 ≥ 0.11** on the lower
  partition (0.3099 on the other). The SPY-history limb is **not** a gate here (item 17) and the
  credentials remain absent. **Q034 locks.** Had item 21 gone the other way, limb (b) would have
  measured 0.0909, the 80-night floor would have projected to ≈ session 880 — beyond any extension — and
  the answer would have been **DEFERRED**; that is recorded so the ruling's consequence is visible next
  to the ruling.
- **suppression list (item 13): revised once here and now CLOSED.** No cell is added: R1 projects no
  not-suppressed cell below 20 — the two halves, the two platform-label arms, the two tape arms (if that
  branch runs) and the 80–90 band (nearly the whole population) all clear at 158 sessions, and the
  bull-only companion is governed mechanically by the ≥ 20 **measured** contributing-night rule at the
  decision pass rather than by the list. The list may not lose a cell, and it does not gain one.
- **branch expected at lock:** **`STABILITY_WITHOUT_TAPE_ARMS`** — `STEWARD_Q032_exposure.md` §(g)
  reports the Alpaca credentials absent and the SPY-from-2025-01-02 probe unattempted as of
  2026-09-14. R2(i) is re-attempted at the freeze build; both branches are registered.
- **`eval.py` deadline: committed no later than Monday 2027-04-05, sha256 recorded, not touched
  afterwards** (item 16) — Q027 and Q029 decide 2027-04-12 on this question's own window and freeze,
  and Q006, Q002, Q012, Q033 and Q018 decide on endpoints this register recomputes.
- **pin_at_decision: true** — every night carrying a register line postdates every existing manifest,
  so DATASET_PINNED runs at the decision date on R2's successor freezes (DP-23).

## Standing rules added

_none, at `decide` and at `record` alike._ Nothing here is Haci's word: item 18 was **DEFAULTED** under
DP-43 / DP-45, and a DEFAULTED item adds **no** DP entry (DP-40). Item 21 is DECIDED on the pinned
platform code and existing entries, which likewise adds none. The rest are applications of DP-01, DP-02, DP-03, DP-04, DP-06,
DP-09, DP-13, DP-21, DP-22, DP-23, DP-24, DP-25, DP-26, DP-27, DP-28, DP-29, DP-30, DP-41, DP-42,
DP-43, DP-44, DP-45, DP-50 and DP-51, and of locked precedent plus Q032's and Q033's same-day decisions
on the shared window and the shared freeze.

## Standing rules proposed

_Proposed only — none is added to `research/DECISION_POLICY.md` by this pass. Item 18 was DEFAULTED and
a DEFAULTED item adds no DP entry (DP-40); item 21 and the corrections are applications of existing
entries. These are listed so Haci can confirm them later._

- **A PREREG screen that transcribes a platform invariant cites the predicate by `path:line` and
  reproduces its strictness.** Q034 item 21: §2.4 wrote "strictly monotone" for a platform predicate
  that is non-strict by documented design, and the one word would have excluded 78% of the population
  and deferred the question. The rule has a cheap enforcement: any screen the draft expects to fire at
  ~0% prints its own firing rate, and a screen firing far from its stated expectation is a registration
  defect, ruled on the code **before** lock and never on which reading locks.
- **A counts-only exposure report measures each screen's own firing rate, not only the surviving n.**
  The Steward found this because he reported 429/550 with the tie/reversal split beside it. A funnel that
  printed only "valid_shared 104" would have deferred Q034 silently and correctly-looking.
- **A pre-registered fallback branch must be at least as strict as the branch it replaces.** Q034 item
  3: a provisioning failure would have removed two of four stability windows and made STABLE easier to
  reach. Where a PREREG registers a fallback for data that may not arrive, the fallback must preserve
  the number of blocking conditions — by substituting another pre-registered partition, or by blocking
  the affirmative branch outright — never by deleting a test.
- **A floor is projected on the population it is counted on.** Q034 item 7: the 80-night floor sits on
  the ranking set (all nine objectives computable) and the draft projected it at the
  contributing-night rate. Third question in a row (Q032, Q033, now Q034) whose schedule was built on
  a rate measured under a different rule than the floor.
- **The trading-calendar holiday list belongs in one place.** Q034's §5.2 omitted 2027-06-18, the same
  omission Q033 carried, and it shortened a freeze horizon by a session. A single desk-level list,
  cited by every PREREG rather than retyped, removes the whole class.
- **A provisioning limb answered for one question is answered for the desk.** `STEWARD_Q032_exposure.md`
  §(g) settled the Alpaca / SPY probe on 2026-09-14; Q033 and Q034 should cite it rather than each
  routing its own. A dated desk-level provisioning register (what data the desk can and cannot fetch
  today) would stop three questions asking the same question three times.
- **DP-43's 12-month ceiling binds the initial decision date, not DP-13's extension** (Q034 item 4).
  Worth confirming as a one-line clarification to DP-43 so the next question does not re-argue it.
