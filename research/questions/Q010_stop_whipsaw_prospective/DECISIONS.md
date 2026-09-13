# Q010 — decisions before lock
Run: 2026-09-13 by decision-maker · Source: PREREG.md "Open decisions before lock", **1 item**
(+ items 2–15: silent choices a `DP` entry touches, gaps the inheritance leaves open, and the one
routed request)

State note: `research/questions/Q010_stop_whipsaw_prospective/state.json` does not exist and
`PREREG.md` is uncommitted — the question is pre-lock (PREREG_DRAFT) and these decisions are in
scope. The same is true of Q009, which is correct: the two files lock at **one commit** (DP-31;
Q009 DECISIONS.md item 25). No `results/` directory exists for either question and none was read;
every count quoted below is an exposure count from `research/reports/STEWARD_Q009_exposure.md`
(R1 and its v003 addendum).

**Summary: 14 DECIDED, 1 ROUTED (data-steward, due at the decision date, not a blocker for lock),
0 ASK.** The single open decision — the window length N and therefore the initial decision date —
is **DECIDED as option A (N = 46)**; item 1 states plainly why it is not R-3 despite naming a date.
Nine further items close gaps the inheritance-by-reference leaves open; four of those are the
answer to "can the two files drift?" (items 3, 4, 9, 10).

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Window length N and the initial decision date | **DECIDED** | **Option A: N = 46 trading sessions.** Q010's window is the 46 trading sessions beginning with the first session strictly after Q009's decision date D; on Q009's primary branch (D = 2026-11-09) that is **2026-11-10..≈ 2027-01-15, decision Monday 2027-02-22**, ≈ **42** contributing nights projected against DP-24's **30**. The dates stay stated as a rule so Q009's DP-13 branch moves them without an edit (item 10). B and C are rejected: B leaves a 10% margin over the gate on a rate measured over 51 sessions, so the DP-13 extension is the likely path and B is ~7 weeks *later* than A when it fires; C buys margin that DP-13's automatic extension already supplies at no cost in the good case. **Why this is not R-3** — see the note under the table. | DP-13 (the extension absorbs the sample risk, so no gate is traded for time); DP-24 (the gate, unreduced); Haci 2026-09-13 Q009 question A (the waiting-vs-verdict trade for H-032 was put to him and answered); STEWARD_Q009 §R1(c),(d) + v003 addendum (0.92 contributing nights/session) |
| 2 | `eval.py` must be *runnable* twice without an edit | **DECIDED** | Q010 §4's byte-identical requirement is only achievable if Q009's `eval.py` takes **window start, window end, manifest paths, the exclusions-file path and the output directory as inputs** (config/CLI), with **no hard-coded dates, manifest names or exclusion dates** anywhere in the script. The Registrar writes this into Q010 §4 and into Q009's §5 freeze bullet as a registered requirement. If the Researcher's Q009 script hard-codes any of them, that is a **defect to be fixed in the Q009 script before it is used for either run** — never a post-hoc edit taken as "the script changed". | rule 9; Q009 DECISIONS.md item 7 ("`eval.py` reads the JSON, no hard-coded dates") extended to every window input; Q010 §4 |
| 3 | Anti-drift pin between the two files | **DECIDED** | Q010's header records, at the lock commit, the **sha256 of `research/questions/Q009_stop_whipsaw/PREREG.md`** as well as of `eval.py`, and **both** are printed in Q010's results header and compared before the run; a mismatch on either **halts the run** and goes to the Red Team. The draft applies this to `eval.py` only. A question that inherits five sections by reference must checksum the file it inherits from, or "verbatim by reference" is unenforceable. | Q010 §4 (the `eval.py` pattern, extended); rule 3 |
| 4 | What "inherited verbatim from Q009 §2" actually covers | **DECIDED — Correction** | The inherited material is Q009 §2's **definitions, filters and exclusion list**, not its **window-specific measured counts** (48 matured nights, 383 published, 303 eligible, 47 contributing, TIGHT 282 / MID 21 / WIDE 0, wrong-side stop 66 of 371 = 17.8%). Those are Q009 data and enter Q010 only as the §10.5 population-drift comparison baseline, where they are already correctly cited. §2 says so in one sentence. | DP-26 (definitions are conventions and travel; measured counts are findings and do not); Q010 §10.5 |
| 5 | Which exclusions file the prospective run passes | **DECIDED** | As drafted (newest file at the decision date, a **superset of v003**), tightened on two points: (a) the **criteria set is closed at lock** to v003's blocks plus DP-04's mechanical re-run/non-session test — a night in Q010's window may not be excluded under a criterion invented after lock without a Steward ruling made on **row timestamps and exposure counts only**, routed and printed before the run; (b) the **delta between v003 and the file used** is printed in the results header with the number of Q010 nights each block removes. | DP-22 (newest file; the cited file stands — here the cited file cannot pre-date the nights, so the *criteria* are what is pinned); DP-04; Q009 DECISIONS.md item 20 / R4 precedent (a night-level integrity ruling is the Steward's, on timestamps, never on outcomes) |
| 6 | Which endpoints Q010 may deliver a pair verdict on | **DECIDED** | The unmodified script computes **everything** (P1, P2, P3, every secondary, both clocks) — it is byte-identical and nothing is switched off. Only an endpoint on which **Q009 returned HISTORICALLY_CONFIRMED** can take a pair verdict (§8 clause 1); every other endpoint's Q010 figure is printed descriptive-only. **BH stays at m = 3** whatever the number of endpoints in play — a narrower verdict scope must not lower the threshold for the endpoint that is in play — and P1 keeps its dual-q (larger of F6 and F4-equivalent). A P1-only pair licenses nothing: Q009 §8 requires **P2** for a guide line, and §9 is unchanged. | Q010 §8 clause 1; Q009 §8 ("a rule requires P2 CONFIRMED"), §7 anti-leniency clause (item 17/item 8 of Q009); rule 9 |
| 7 | The branch the draft does not cover: Q009 **DEFERRED** | **DECIDED — gap filled** | §5's "whether Q010 runs at all" gains one clause: **if Q009 goes to DEFERRED** (a gate still short after its single DP-13 extension), Q010 is **closed unrun** for the same reason as the NULL/INCONCLUSIVE branch, the reason is ledgered, and any later prospective test of H-032 is a **new** pre-registration. As drafted the clause covers only NULL and INCONCLUSIVE, and Q009's own §5 makes DEFERRED a live branch. | DP-13 (DEFERRED is a registered outcome of Q009, so Q010 must name it); rule 3; Q010 §5 |
| 8 | Q009 §8's both-halves and tape-stratum clauses | **DECIDED** | **Not imported as gates**, as drafted — they are 80-night clauses and a ~42-night window cannot carry them. They are **printed descriptively** wherever a half or a stratum clears the 20-contributing-night sub-cell floor (at N = 46 the two halves are ≈ 21 nights each, so they usually will), and a **sign disagreement between halves is stated next to the pair verdict** in `REPORT.md`. Not importing them is not a loosening: DP-24's prospective clause is sign + MPE + CI, and nothing else in §8 is relaxed to compensate. | DP-24 (the prospective clause as the desk has always written it); DP-21 (the 20-night sub-cell floor, which does apply); Q010 §5, §8 |
| 9 | §8 clause 2's blindness wording | **DECIDED — Correction** | "all of them dated after Q009's lock commit" → "**all of them dated after Q009's decision date D — hence, a fortiori, after both files' lock commit**". The construction is stronger than the clause claims, and the weaker wording is what a later reader would test against. Same edit in §5's first bullet. | DP-24; Q010 §2 (the window is defined off D, not off the lock commit) |
| 10 | The illustrative dates, and the discrepancy between two of them | **DECIDED — Correction** | §5 gives **2027-04-12** for {Q009 primary branch + Q010 extension} and **2027-04-05** for {Q009 extension branch + Q010 primary}, although both describe a window ending ≈ 2027-03-01 — one of the two is arithmetic, not a rule. The Registrar replaces the prose with a **four-row table** (Q009 primary/extension × Q010 primary/extension) carrying window start, window end, decision date, every cell marked **"illustrative — the Steward fixes the exact session-count date against the trading calendar when building the freezes"**, and states once that **the rule, not the illustration, is what is registered**. The rule is deterministic given the calendar, so fixing a date later is arithmetic, not a choice made with numbers in view. | DP-13 (the extension date must be *named* in the PREREG — as a rule plus a dated table, both branches); Q009 §5 (same rule/illustration split) |
| 11 | Why the window starts after Q009's **decision date** and not after its last pick night | **DECIDED — stands as drafted, with the reason written in** | The drafted rule leaves ≈ 26 sessions (2026-10-03..2026-11-09) in neither question on the primary branch. It stands, because it is the only rule under which **no night is ever assigned to a question after that night has occurred**: starting after Q009's last pick night would put 2026-10-05..2026-11-13 in Q010 if Q009 does not extend and in Q009 if it does, with the branch chosen on 2026-11-09 — after those nights happened. Under the drafted rule the start only ever moves **later**, no night is ever moved *into* Q009, and the two populations are disjoint on both branches. §2 states the rule's reason and §10 discloses the unused sessions as a cost, so the gap is visible rather than accidental. | rule 3; DP-31 (the successor exists to keep the prospective half blind); DP-26 (a registrar convention stands where it was not derived from outcomes) |
| 12 | Successor freezes for Q010's window (the third build) | **ROUTED → data-steward** | waits on the freeze build; **due at Q010's decision date, not a blocker for lock** (DP-23 pins successors at the decision date). Scope is fixed by DP-23 and needs no confirmation. Request is paste-ready below. | DP-23; Q006 §5; Q009 DECISIONS.md R2 |
| 13 | That Q010's 30-night gate never becomes a precedent | **DECIDED** | §5's and §8's "the 80-night floor is not the gate here" stand — rule 6 / DP-21 is satisfied **by the pair** (Q009 ≥ 80 contributing nights, Q010 ≥ 30 post-lock, exactly DP-24's standing construction), not by Q010 alone — and are made unusable as precedent by the reporting discipline already in §8: **Q010 never carries a standalone verdict, is never presented as independent evidence, and its LEDGER entry is written against Q009**. The Registrar adds one clause to §8: "*a future question may not cite this file as precedent for a 30-night primary endpoint; the 30 is DP-24's prospective clause, not a floor*". No CLAUDE.md rule is softened and no DP entry is added here. | rule 6; DP-21; DP-24; Q010 §1, §8 (reporting discipline) |
| 14 | The wrong-side-stop platform fix vs this replication | **DECIDED** | §10.6 already says a platform change to how the stop is written voids the replication. One line is added to the **`PLATFORM_ISSUES.md` entry** the Q009 pass filed (wrong-side stops, 17.8%): *"A side/distance guard on the written stop must not ship, flag-on, before Q010's decision date — it changes the population Q010 replicates and voids the pair (Q010 §10.6). Rule 11's flag-off-then-shadow discipline makes the fix and the question compatible; a live flip does not."* Filing is the coordinator's/Steward's lane; I edit nothing there. | DP-07; rule 11; Q010 §10.6; Q009 DECISIONS.md item 18 |
| 15 | Lock mechanics | **DECIDED** | Both `state.json` files are initialised by the controller and both questions enter **PREREG_LOCKED at the same commit**; Q010's header records that commit sha and Q009's header records Q010's path (it already does). Neither file may be committed without the other. If the controller will not advance one of them, **neither locks** — a Q009 locked without its successor is a DP-31 violation, not a sequencing detail. | DP-31; rule 3; controller (`research/lib/controller.py`) is not argued with |

### Why item 1 is not R-3, in full

R-3 reserves **trade-offs between waiting and sample size**. Item 1 names a date but contains no such
trade-off, for four reasons that hold together:

1. **No gate is on the table.** A, B and C all keep DP-24's 30 and DP-21's 20-night sub-cell floor
   untouched; no arm, no endpoint and no population is dropped in any option. The only thing that
   varies is how much margin is bought above a gate that is never reduced.
2. **DP-13 already absorbed the sample risk, and that was Haci's own answer.** The question a margin
   choice is insurance against — "it came up short, now what" — has a standing answer: one automatic
   extension, then DEFERRED, fired on measured counts. C is paying in calendar time for insurance the
   desk already holds for free; B is declining insurance it will probably have to claim (≈ 33 against
   30, on a rate measured over 51 sessions, across a holiday-season window), and a claimed extension
   puts B's decision ~7 weeks *later* than A's. After DP-13 and the "take the stricter" rule, A is
   what is left, not what is preferred.
3. **The substantive waiting question for H-032 was asked and answered on 2026-09-13.** Haci chose
   Q009's short window knowing it cost him the tradeable verdict, and DP-31 answered that by requiring
   this successor. Setting N to the shortest drafted window that clears DP-24's 30 with real margin
   **implements** that answer; re-asking it would be the fourth date question in a row and the second
   on the same hypothesis.
4. **The date is derived, not chosen.** It is D (his answer) + N + the 20-session maturity + a fixed
   freeze margin. The only free parameter is N, and (2) fixes it.

Had any option changed the reachable verdict class, dropped an endpoint, or met a floor by moving it —
the shape of Q009's question A — it would be his, and it would be asked. None does. It remains his to
overturn at lock like every other decision here; the one-line disclosure below is how he sees it.

## Corrections to silent choices

- **§8 clause 2** — "all of them dated after Q009's lock commit" → "**after Q009's decision date D,
  hence a fortiori after both files' lock commit**"; same in §5's first bullet. (item 9; DP-24.)
- **§5 extension/branch dates** — the two illustrations that disagree (2027-04-12 and 2027-04-05 for
  windows both ending ≈ 2027-03-01) are replaced by one four-row branch table, every date marked
  illustrative, with the rule stated as the registered text. (item 10; DP-13.)
- **§2 inheritance sentence** — "inherited verbatim from Q009 §2" is qualified: **definitions, filters
  and exclusions** are inherited; Q009's window-specific **measured counts** are not, and appear only
  as §10.5's drift baseline. (item 4; DP-26.)
- **§5 "whether Q010 runs at all"** — add the **DEFERRED** branch alongside NULL and INCONCLUSIVE.
  (item 7; DP-13.)
- **§2 window-start rule** — add the one-sentence reason (no night is assigned to a question after it
  has occurred; the start moves only later) and disclose in §10 the ≈ 26 sessions that fall in neither
  question on Q009's primary branch. (item 11; rule 3.)
- **§4 header checks** — extend the byte-identity check from `eval.py` to **Q009's `PREREG.md`
  sha256**, both printed and both halting the run on mismatch. (item 3.)
- **§4 / Q009 §5** — register that `eval.py` takes window bounds, manifest paths, exclusions path and
  output directory as **inputs**, with no hard-coded dates or paths. (item 2; rule 9.)
- **§5 exclusions bullet** — the criteria set is closed at lock; the v003→run-file **delta is printed**
  with per-block night counts. (item 5; DP-22.)
- **§8** — add "*this file is not precedent for a 30-night primary endpoint*". (item 13; DP-21.)

Nothing in the draft contradicts a `DP` entry outright: the MPEs (DP-10, DP-20), the 20-session clock
(DP-09), the entry basis `C_t` (DP-03(a)/DP-11), the tie rule (DP-27), the publication predicate
(DP-28), the stop line (DP-30), the exclusions file (DP-22), the freeze scope (DP-23), the family and
the not-a-second-F6-question clause (DP-29), the extension/DEFERRED machinery (DP-13) and the
HISTORICAL_ONLY handling (DP-31) are all as the policy requires. `research/BACKLOG.md` H-032 already
carries the Q010 line and needs no edit.

**Conflicts with already-locked questions:** none new. Q009 is not locked and is not edited by this
pass — items 2 and 10 touch Q009's §5 only as part of the same pre-lock apply, at the same commit.

## Questions for Haci

_None._ The single open decision is settled under DP-13 and DP-24 — see "Why item 1 is not R-3".

**Disclosure at lock (not a question, one line for the coordinator to put in front of him when he
signs the commit):** *Q010, the prospective half of the stop question you dated on 2026-09-13, is set
to run for 46 pick nights after Q009 reports — decision Monday 22 Feb 2027, about 42 contributing
nights against the 30 needed. The desk set that length rather than ask you a fourth date question: no
floor moves, and if it still falls short it extends once automatically and then defers, which is the
rule you already agreed. Yours to change at lock if you want it sooner or later.*

## Routed requests

### data-steward

**R5 — successor freezes for Q010's window (third build; due at Q010's decision date, not a blocker
for lock).** When Q010 reaches its decision date — on Q009's primary branch, the week of 2027-02-15
for a Monday 2027-02-22 decision; on Q009's DP-13 extension branch, the equivalent week for the
branch table in Q010 §5, and again only if Q010's own single extension fires — please build the
successor selection freeze (same SQL as `manifest_v001`) and price freeze (same Alpaca queries)
covering Q010's registered pick nights: the 46 trading sessions beginning with the first session
strictly after Q009's decision date D. Scope is fixed by DP-23 and needs no confirmation: the symbol
list is **every candidate on those nights, published and unpublished** (B1 needs the unpublished
symbols' pick-night closes and forward bars), plus **hourly bars for published symbols** (the P2
same-session stop-vs-target tie-break), carrying **20** forward sessions beyond the last pick night
(40 where the 40-session descriptive companion is to be computed). Please also fix the exact
session-count dates for all four branch cells (Q009 primary/extension × Q010 primary/extension)
against the trading calendar implied by `prices_daily_split`, and issue the newest
`exclusions_vNNN.json` in force for those nights — a **superset of `exclusions_v003.json`**, with any
night excluded under a criterion not already in v003 ruled on from row timestamps and exposure counts
only (the R3 pattern), routed and printed before the run, never silently dropped. With the freeze,
please return an **exposure-only** count for Q010's window in the same form as
`STEWARD_Q009_exposure.md` §R1(a),(c): the population funnel and the contributing-night counts on
both definitions (P1 B1-valid, P2), plus the wrong-side-stop share and the TIGHT/MID/WIDE split by
month and score band, so Q010 §10.5's population-drift comparison against Q009's measured 17.8% /
0% / 93.1%–6.9%–0% can be made **before** any estimate is read. **No bar after night t, no touch, no
return, no outcome column, nothing from any `results/` directory.** What it decides: nothing about
the verdict — DP-24's 30-night gate fires on `eval.py`'s measured counts, and the exposure count
carries no outcome, so producing it is not an interim look. A large population drift is a Red Team
call on the face of the population (Q010 §10.5), not a gate.

## Standing rules added

_none — nothing here generalises beyond Q010; item 1's N is arithmetic on Q009's measured run-rate
against DP-24's gate, exactly as Q009's own date was (Q009 DECISIONS.md, "Standing rules added"), and
DP-13, DP-21, DP-23, DP-24 and DP-31 are all applied unchanged. Two candidates for a future `DP`, each
with one instance only and therefore not written: (i) **a replication inherits by checksum, not by
section number** (item 3) — if a second successor question is ever registered under DP-31, that is the
point to write it; (ii) **`eval.py` takes its window and its data paths as inputs** (item 2), which
DP-31's "byte-identical script" clause silently assumes and which will be assumed again._
