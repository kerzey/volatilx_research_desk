# Q020 — decisions before lock
Run: 2026-09-13 by decision-maker (autonomous) · Source: PREREG.md "Open decisions before lock", 4 items (+2 routed requests named in §5: R1 exposure, R2 successor freezes)

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14T00:13Z) — in scope.

**Q020 does not lock. Item 1 goes the DP-41 route: the question needs a rule-14 exception the desk
may not grant itself, so Q020 goes to `research/questions/DEFERRED.md` with the exception spelled
out (table, column, time), and re-enters the queue at the front if and when Haci adds the scope to
DP-05.** Items 2, 3 and 4 are decided anyway, on their own grounds, so that the question comes back
settled rather than re-argued: they are binding on re-entry. R1 is routed but **held** behind the
grant — it measures the very classifier that is in dispute, and running it now spends a full funnel
measurement on a question that cannot be tested.

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | Whether the mid-trade classifier needs a new rule-14 exception | **DEFAULTED (R-1)** | **Option B.** **DEFERRED — needs rule-14 exception:** `prices_daily_split` daily OHLC (and `prices_hourly_raw` hourly OHLC for the same-session ordering rule), **sessions t+1 … t+40**, for **published picks and the unpublished control pool alike**, used for one purpose — assigning the EVENT (`a` = first L4 touch, `b` = first qualifying L2 touch at or after it) and therefore **population membership, control-set membership and the decision basis `X_b = O_{b+1}`**; the decision time for that one input would be **09:30 ET on session `b+1`, `b ≤ 40`** (up to session t+41). Every other input stays at 16:05 ET on the pick night, and every outcome is measured strictly after `X_b`. §6's sentence "Q020 needs no rule-14 exception and requests none" is struck (Correction 1); §11 item 1's Recommendation A is **not** adopted. Q020 is **not** locked and **not** counted in the F4 or F6 correction sets while deferred | **DP-41** (the desk grants no new rule-14 exception; DEFERRED with the exception named), reinforced by **Q009 §6 locked** — "no session-t+1 quantity enters any primary endpoint **or any eligibility filter**" is the desk's line on this very shape, the adverse-side mirror — and by **DP-05**'s own text: the Q008 grant's scope is *"bars from sessions t+1 and t+2 … the decision time for that one input is 16:00 ET, session t+2"*, i.e. a later clock **for classification**, and Haci "explicitly did not take the standing-rule option" (Q008 §6.1, 2026-09-13). Q020 asks for the same licence over **40 sessions instead of 2**, on both arms; **DP-45** points the same way had it been read as R-5; not taken: A — no exception, the per-decision-clock reading |
| 2 | How the DP-12 control is built | DECIDED | **Option A** — **condition first, match second**: every same-night control-pool row carries synthetic L2/L4 at `p`'s **identical ATR distances and direction** from its **own** close, is classified for the EVENT from **its own** bars under the same 40-session cap and the same DP-27 same-session rule, and only the EVENT = 1 rows with 60 forward sessions enter the pool; from that pool the **10 nearest** on standardized (`beta60`, `atr_pct`, `runup20`), Euclidean, with replacement across picks, ties by symbol ascending; **fewer than 10 ⇒ take all; fewer than 3 ⇒ the pick is dropped from E1 and E2 and counted**, never back-filled and never replaced by an unmatched contrast. §2, §3 B2, §4 and §5 stand as drafted | **DP-12** (the control must be matched on the event; the total effect stays descriptive and licenses no rule, and its cost — smaller pools, dropped picks, a later floor date — is paid, not softened); **Q006 §3** (locked, `DATASET_PINNED`) for the 10-nearest construction verbatim; the two options differ only in strictness and A is the stricter (minimum 3 drops more picks than B's minimum 1), so the charter's stricter-of-two rule decides without troubling Haci. B is additionally not a live option: matching first on look-alikes and then filtering on a rare path empties most control sets and makes the question about who has controls |
| 3 | What "re-advance" is | DECIDED | **Option A** — first touch of **L4** again within **R = 20 sessions of `X_b`**. L3 re-touch and L5 first touch stay registered secondaries printing raw p only; `R` = 10 and `R` = 40 stay registered clock sensitivities (40 on matured nights only). §4, §8, §9 stand as drafted | **DP-42** first clause — the primary level is the level the hypothesis names, and H-033 names L4 on both legs; **DP-09** for the 20-session horizon counted from the stated basis. DP-42's "L4 within 40 sessions for deep targets" is satisfied by the EVENT's own 40-session cap (§2), and is **not** re-read as 40 further sessions from `X_b`: that would be the easier bar, an 80-session maturity and a longer wait at once. Both arms share the clock, so R = 20 shrinks the contrast in **either** sign — the harder test in both directions, which is what a two-sided question needs |
| 4 | What position the money endpoint re-commits at `X_b` | DECIDED | **Option A** — the **full unit** position at `X_b`, exit at the first L4 touch in `b+1 … b+R` (at the open where the session opens through L4), else at the close of session `b+R`, no stop; `r_p = dir × (exit_p − X_b) / ATR`, so flattening at `X_b` scores exactly 0. The `BAND_EXITS` residual version is printed beside it as the rule-5 execution report (§4), **descriptive**, and never decides. §4, §8, §10.11 stand as drafted | **CLAUDE.md rule 5** — one basis on both sides; the event-matched control has no scale-out, so a residual-sized pick against a full-sized control is not a comparison. **DP-10 / DP-44** — the 0.25 ATR MPE is per trade and **never rescaled**, and a residual basis is exactly that rescaling. **DP-02** — no stop anywhere in the plan |
| 5 | Window end, decision date, extension, lock-or-DEFER (§5 R1) | ROUTED → data-steward | **HELD** behind item 1's grant — waits on R1 items (1)–(7), which settle the matched-contributing rate `r`, the `r ≥ 0.31` ceiling test, the window end, the decision date and the sub-cell demotions. Not to be run while Q020 is deferred | — |
| 6 | Successor freezes (§5 R2, DP-23) | ROUTED → data-steward | **HELD** — no `manifest_v002` / `manifest_prices_v002` pair is built for Q020 while it is deferred; the request revives with the question, due before its decision pass, never a blocker for lock | — |
| 7 | Bookkeeping: the DEFERRED entry, BACKLOG, state, family counts | ROUTED → registrar | waits on nothing — write the `DEFERRED.md` entry in DP-41 form, re-mark H-033, leave `state.json` at `PREREG_DRAFT`, and keep Q020's 2 primaries out of the F4 and F6 correction sets until it re-enters | — |
| 8 | What happens to the schedule on re-entry | DECIDED | The §5 schedule is **recomputed from the new lock date, never carried forward**: window start stays **2026-06-01** (DP-06, the catalyst fix), the window end is re-derived at R1's measured `r`, and the `r ≥ 0.31` threshold is **re-solved** against the new 12-month ceiling (it is the solution of `1.4484 × 80/r + 87 + 7 ≤ (new lock date + 12 months) − 2026-06-01`, which tightens as the lock date moves later). Dates may move **out only** | **DP-43** (ceiling tested on the initial decision date, floors never lowered to meet one); **DP-45** (never the option that reaches a date sooner); **DP-06** for the window start |

## Corrections to silent choices

Four. One is the disposition of item 1 written into the file; one is a calendar error in the
schedule; two apply policy entries added **today** that postdate the draft. Everything else in the
draft was checked against the policy and already matches (list at the end of this section).

1. **§6 (Knowledge time) and §11 item 1 — the "no exception needed" sentence and its authority both
   go.** §6 reads *"Q020 needs no rule-14 exception and requests none (DP-05 untouched; DP-41
   respected)"* and grounds that on *"the reading Q019 registered on 2026-09-13"*. Two problems.
   (a) **Q019 is `PREREG_DRAFT`, not locked** — a draft is not precedent; DECIDE ground 2 requires a
   locked PREREG, and the locked question on this exact shape says the opposite (Q009 §6: no
   post-pick-night quantity in *any eligibility filter*). (b) The reading itself is the general
   "later clock for classification" licence that **DP-05 records Haci declining on 2026-09-13**, the
   same day. §6 must instead state, in the knowledge-time table and in the prose: the EVENT
   classification from sessions 1 … `b` and the decision basis `X_b = O_{b+1}` are **outside** the
   desk's current rule-14 grant, the question is deferred under DP-41, and the exception it would
   need is the one written in row 1 above. `research/lib/validators.py:17` (`ET_DECISION = "16:05"`,
   *"features must be available before this"*) is the enforcement code's own reading and is not
   softened here (CLAUDE.md rule 15). The §6 table row for "daily bars 1 … `b`; hourly bars for
   ordering rule 1" must lose the phrase "complete before `X_b` exists" as a justification and carry
   the exception request instead.
2. **§5 — the DP-13 extension window end `2027-06-12` is a Saturday.** 30 sessions after Friday
   **2027-04-30**, with Memorial Day **Monday 2027-05-31** removed, is **Monday 2027-06-14**. The
   extension decision date is unchanged at **Monday 2027-09-20** (60 sessions from 2027-06-14 =
   Thursday 2027-09-09 with Juneteenth observed Friday 2027-06-18, Independence Day observed Monday
   2027-07-05 and Labor Day Monday 2027-09-06 removed; + one week = 2027-09-16; first Monday on or
   after = 2027-09-20). The correction moves the window end **out, never in** (DP-43, DP-45). The
   same Saturday date is repeated in `research/BACKLOG.md`'s H-033 entry and in this question's
   header line there; both take the same fix when the entry is rewritten. The drafted primary window
   end **2027-04-30 is a Friday and is correct**; the drafted decision date **Monday 2027-08-02** is a
   Monday and is correct; R1's classification window **2026-06-01..2026-07-15** is correct (40
   sessions from 2026-07-15 is exactly 2026-09-10, `manifest_prices_v001`'s `as_of`). All of these
   are re-derived at re-entry under row 8 in any case.
3. **§9, the `INTERNAL_TOOL` brief and the implementer bullet — DP-49 (added 2026-09-13, postdates
   the draft).** Every check a brief following from this question hands the **coding agent** must be
   satisfiable from the platform repo alone — the test suite, a pure-function import,
   `git show --stat`, a file diff. The "byte-identical checksum on the old path" check is written as
   **the diff that proves it**, never as "run the excursion job twice and compare"; anything that
   reads or writes `sas_selection_excursion`, `conviction_monitor` or any other table belongs in the
   brief's verification section addressed to the **Data Steward on `$RESEARCH_DB_URL`**, or to Haci
   where a write is required. Add that sentence to the §9 implementer bullet.
4. **§9 — DP-50(b) must be named in the filing, not only in §10.14.** The draft carries the desk side
   of DP-50 in threat 14, but the §9 branch that sends the L4-trim ruling's premise back to the
   strategist (and any `PLATFORM_ISSUES.md` entry that follows) must name the constraint **in the
   entry itself**: a repair touching `_extract_lane_plans`
   (`services/super_agent_select_service.py:94-161`) or the cross-lane re-sort (`:195-257`) is
   **flag-off until Q020's decision date** (the PI-011 / Q010 pattern), and if it ships inside the
   window anyway it takes a dated `DATA_NOTES.md` entry naming the column, the date range and the
   ship SHA, and the lane-plan payload becomes **two features split at the ship date** (DP-06
   pattern, DP-50(a)) — which moves the window start, mid-flight.

**Cross-question flag, not a Q020 edit — Q019 §6.** Q019's *"no rule-14 exception requested or
needed"* rests on the same per-decision clock this file declines. The two are **not obviously the
same case**: Q019's classifier is a product row in `conviction_monitor` with a **declared**
`lag_sessions: 1` availability in `freeze_config.availability` — rule 14's own mechanism — read one
session after the pick night, whereas Q020 reads raw price bars over **40** sessions and uses them to
select the population and both arms. But the distinction is thin enough to be worth a second pair of
eyes: **Q019 is still `PREREG_DRAFT`, so the Registrar and the Red Team should re-check its §6
against DP-05's "no general later-clock licence" sentence before it locks.** Nothing in Q019's own
`DECISIONS.md` is edited here.

**Checked and not corrections** — each already matches policy: MPE **+5.0 pp** on E1, the standing
number for a control-adjusted touch-rate endpoint with no uplift proposed (DP-20, DP-44), and **0.25
ATR** on E2, per EVENT trade and never rescaled (DP-10, DP-44); sessions-to-touch and the excursion
panels descriptive with no MPE, and **no money-unit MPE invented** (DP-44); floors read as **≥ 80
contributing nights per primary endpoint** with E1 and E2 sharing one §2 definition, and 20 per
sub-cell — the stricter reading (DP-21); **≥ 30 contributing nights dated after the lock commit**,
never reduced, with DP-31 correctly **not** invoked because PROSPECTIVELY_CONFIRMED is reachable by
design (DP-24, DP-31); the event-matched contrast primary with B4 descriptive and §8 clause 8 making
the matched form the verdict (DP-12); entry **`C_t`** for picks and controls alike on an already-held
position with `E_AH` a picks-only sensitivity, and the estimands entry-free by construction (DP-11,
DP-03); the publication predicate `qualified IS TRUE AND selected_rank IS NOT NULL` with dark-lane
rows in no arm (DP-28); **`exclusions_v003.json`**, the newest file, read from JSON with no hard-coded
dates (DP-22) — and on re-entry the Q018 / Q019 add-only successor-exclusions construction applies,
since the window outruns v003; H-033's levels and shape taken as written and not re-united (DP-25);
registrar conventions fixed before any outcome is seen — the ±1 ATR adverse line, the 30-session
block, the expanding-window tape terciles, the gap-through-is-a-touch rule (DP-26); **same-session
ties resolved against the hypothesis** — an unresolvable `b = a` is not an EVENT (DP-27); stops never
used as exits and counter-direction touches reported (DP-02), with DP-30 not engaged because no
printed stop is used; family **F4** by the primary endpoint's subject with the F6 companion
correction on E2 and H-033 counted once (DP-29); one automatic DP-13 extension firing on `eval.py`'s
measured counts, then DEFERRED, with no second extension and no reduced floor; successor freezes
covering **every** candidate symbol, published and unpublished, plus hourly bars for published
symbols (DP-23); every basis labelled **NON_QUOTABLE** (rule 12); regime used only for nights
≥ 2026-06-09, v1.2, same-evening rows (rule 7, FREEZE_v001 §7); the exposure count specified on the
pinned freeze rather than a live query (DP-50(c)); and the platform-repo git check in R1 item 7 read
**read-only**, with no database step handed to any coding agent (DP-49, DP-50).

## Defaulted on Haci's behalf

- #1 Rule-14 exception for the mid-trade classifier — chose **DEFERRED: Q020 is not locked and needs
  a DP-05(c) grant to read `prices_daily_split` / `prices_hourly_raw` bars for sessions t+1…t+40 as
  the EVENT classifier, on picks and controls alike, with the decision time for that one input at
  09:30 ET on session b+1**; not taken: **A — no exception, the per-decision-clock reading** —
  DP-41. Overturn = add the scope to DP-05 and the question re-enters at the front of the queue.

Nothing else was defaulted. Items 2, 3 and 4 each met a DECIDE ground and none is a question about
how Haci trades: item 2 is DP-12 plus Q006's locked matching construction plus the stricter of two,
item 3 is DP-42's first clause (the level the hypothesis names) on DP-09's clock, item 4 is rule 5's
one-basis requirement plus DP-10's never-rescaled MPE. No floor, arm, gate, clock or clause was
weakened anywhere in this file, and the one thing that moved — the DP-13 extension window end — moved
out by two days, not in.

**Why item 1 was not simply taken as recommended (DP-40).** DP-40 applies the Registrar's
recommendation *unless a DECIDE ground gives a different answer*, and here one does. The nearest
**locked** question, Q009 — the adverse-side mirror of this very shape — says in its §6 that it needs
no exception precisely because *"no session-t+1 quantity enters any primary endpoint **or any
eligibility filter**"*. Q020's EVENT is an eligibility filter: a pick is in E1 and E2 only if bars
from sessions 1 … 40 say it round-tripped, and its control set is chosen the same way. The draft's
authority for the other reading is a **draft** (Q019, registered hours earlier, still unlocked), and
the reading itself is the general later-clock-for-classification licence that DP-05 records Haci
declining **today**. Q008 paid a scoped grant for 2 sessions of exactly this; Q020 asks for 40, on
both arms. Even read at its most charitable this is R-5 — the write-up could not avoid an "on the
other hand" — and DP-45 then takes the option less likely to reach CONFIRMED, which is the same one.
The cost of being wrong is one sentence from Haci and a question that re-enters at the front with
items 2–4 already settled; the cost of being wrong the other way is a locked question that reads 40
sessions of forward bars to choose its own population.

## Routed requests

### registrar — write the DEFERRED entry and the bookkeeping (do this now; nothing waits on it)

Q020 (`research/questions/Q020_l4_pullback_readvance/`) is **not locked**: DECISIONS.md item 1 takes
the DP-41 route, so please write its `research/questions/DEFERRED.md` entry under the file's **first**
admission ground (the objective cannot be measured with the licence the desk holds — a rule-14
blocker, not a sample-size one), in the H-062 form. The entry must name the exception exactly:
**table and columns** — `prices_daily_split` daily OHLC and `prices_hourly_raw` hourly OHLC;
**rows** — published picks **and** the unpublished same-night control pool; **time** — sessions
t+1 … t+40, i.e. a decision time of **09:30 ET on session `b+1` (`b ≤ 40`)** for that one input;
**purpose** — assigning the EVENT (`a` = first L4 touch, `b` = first qualifying L2 touch at or after
it) and therefore population membership, control-set membership and the decision basis
`X_b = O_{b+1}`, with every other input staying at 16:05 ET on the pick night and every outcome
measured strictly after `X_b`; and **what it is not** — no outcome, no selection-side input, no
licence beyond this question. Say in the entry that the blocker is a **grant, not procurement or
time**: Haci moves it back into the backlog by adding the scope to DP-05 as **(c)**, after which
Q020 re-enters at the front of the queue (DP-41) with DECISIONS items 2, 3, 4 and 8 binding and
Corrections 1–4 applied, and the §5 schedule recomputed from the new lock date (never carried
forward). Note the precedent chain in one sentence so the entry is self-contained: Q008 §6.1 is a
2-session scoped grant for the same kind of input, Q009 §6 (locked) is the desk's line that no
post-pick-night quantity enters an eligibility filter, and DP-05 records that Haci declined the
standing-rule version on 2026-09-13. Then: mark **H-033 in `research/BACKLOG.md`** as *deferred
2026-09-13 pending a DP-05(c) rule-14 grant* rather than *registered as Q020* (keeping the drafted
design, which stands), fix the Saturday extension date there and in the PREREG (**2027-06-12 →
Monday 2027-06-14**, Correction 2), leave `state.json` at `PREREG_DRAFT` (no `PREREG_LOCKED`, no
`schedule.json`), and make sure **Q020's two primaries are not counted in the F4 correction set and
E2 is not counted in F6** while it is deferred — Q019 §7's F6 count of 15 and the F4 count of 9
(Q007 4 + Q008 3 + Q013 2) are the correct figures without Q020.

### data-steward — R1 (exposure, counts only) — **HELD**: do not run until the DP-05(c) grant exists

**Hold this request.** Q020 is deferred pending a rule-14 grant (DECISIONS item 1); the EVENT it
would count *is* the classifier in dispute, and no schedule follows from it while the question cannot
be tested. Run it only when Haci adds scope (c) to DP-05, and then as written here. Q020 (L4 touched,
pullback to L2, re-advance; PREREG §5 request R1) needs a **counts-only** exposure measurement on the
**frozen** data — `research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json`,
never a live query (DP-50(c)) — and it is **blocking for lock**: no desk report has ever crossed an L4
touch with a later pullback, so this question cannot be scheduled without it. **No outcome of any
kind:** nothing after session `b` — no re-advance, no L4 touch after `b`, no plan result, no return,
no pick-minus-control difference of any sort. Population: published picks (`qualified IS TRUE AND
selected_rank IS NOT NULL`, DP-28; dark-lane rows in no arm) on pick nights **2026-06-01..2026-07-15**
— the 40-session classification maturity on `manifest_prices_v001`, deliberately not the 60-session
outcome maturity — with the nights in `research/data/exclusions_v003.json` (`manual_runs` ∪
`non_session_runs` ∪ `uncorroborated_publication_runs`) and DP-04 re-run nights removed, and with the
control pool defined as the complement of the publication predicate on the same night. Please return:
**(1)** the §2 funnel night by night — matured pick nights, eligible published picks, then each
exclusion separately: no `lane_plans`, no `day_trading.targets[1]` (L2), no `swing_trading.targets[1]`
(L4), void at `C_t` (`d2 ≤ 0` or `d4 ≤ 0`), **non-monotone `d4 ≤ d2`**, mixed direction,
`outcome_target_invalid` non-null, missing `C_t` or 14-bar ATR history, missing bars in sessions
1..40, and nights where > 25% of eligible picks are ungradeable; **(2) EVENT picks and EVENT nights**
— `a` = first session in 1..40 with an L4 touch (a gap through at the open counts), `b` = first
session in `a`..40 with an L2 touch **at or after** the L4 touch in time — with the distributions of
`a`, `b`, `b − a`, `d2`, `d4` and the retrace depth `dep`; **(3) matched-contributing nights and the
rate per elapsed session, by month** — a night with ≥ 1 EVENT pick that is not void at `O_{b+1}` and
carries **≥ 3** event-completing matched controls (condition first at `p`'s ATR distances from each
control's own close, then the 10 nearest on standardized `beta60`/`atr_pct`/`runup20`; DECISIONS item
2), denominator **elapsed** sessions (calendar minus holidays, exclusions **not** pre-removed), plus
the absolute count accrued over the R1 window; **this is the number that decides whether Q020 locks
at all** — below **0.31 matched-contributing nights per session** the initial decision date passes
DP-43's 12-month ceiling and Q020 goes to DEFERRED on that ground too, and the 0.31 threshold is
**re-solved from whatever the new lock date is** (DECISIONS item 8), while a rate faster than the 0.35
planning rate changes nothing (DP-43, DP-45 — a date never moves in); **(4)** EVENT picks **dropped
for fewer than 3 event-completing controls**, as a share and with the `d2`/`d4` distribution of the
dropped and of the retained, plus the control-EVENT pool-size distribution (median, p10, minimum) —
DP-12's stated cost, §10.2; **(5)** EVENT picks whose `O_{b+1}` is already at or through L4, the
void-at-decision-basis exclusion, by month; **(6)** same-session (`b = a`) cases on picks and how many
`prices_hourly_raw` resolves, hourly-bar coverage on published symbols over sessions 1..40, and the
share of **unpublished candidate symbols with no hourly bars anywhere in the freeze** (the Q015 §7
asymmetry, remeasured on this funnel — it shrinks the control pool and makes the test harder, §10.5);
**(7)** from the **read-only** platform repo (`git log --follow`, no database step — DP-49), every
commit inside the window touching `_extract_lane_plans`
(`services/super_agent_select_service.py:94-161`) or the cross-lane re-sort (`:195-257`), with SHA and
date: a column that changed meaning mid-window is two features (DP-06, DP-50(a)) and the window start
moves to the first pick night after the last such ship; Q009 §R3 ruling 2 already found no historical
payload rewrite across the 795-row correction ledger, so this re-checks only for new ship dates; and
**(8)** the EVENT picks' splits for the DP-43 demotion call — direction (bull/bear), score band
(80–85 / 85–90 / 90+), `d4` tercile, `rem` tercile, `b − a` tercile — each as **matched-contributing
nights**, not picks, so sub-cells projected below 20 nights are SUPPRESSED at lock rather than at the
decision pass. Items (3) and (7) settle the window end, the decision date, the extension date and the
lock-or-DEFER call at `record`; item (8) settles the demotions at lock; items (4), (5) and (6) are the
measured facts that could make the question speak for a narrower population than it claims, and they
go in the report whatever they say. **R1 may push every date out; it can never pull one in.**

### data-steward — R2 (successor freezes) — **HELD**; revives with the question

No `manifest_v002` / `manifest_prices_v002` pair is built for Q020 while it is deferred. On re-entry
the §5 R2 request stands as drafted (DP-23): selections and prices covering pick nights after
2026-09-10 through the recomputed window end, the daily symbol list covering **every candidate on
every in-window night, published and unpublished**, with 60 prior daily bars and forward bars running
60 sessions beyond the last included pick night (80 where the `R` = 40 companion is computed), **plus
hourly bars for published symbols** for the ordering rule, an **add-only successor exclusions file**
built by the identical three criteria, and a DP-50(a) check for any commit between the freezes that
rewrites historical `public_payload_json` rows. Due before the decision pass, never a blocker for
lock.

## Schedule

**Not filled — Q020 does not lock.** The drafted figures are carried below as provisional only, and
under DECISIONS item 8 they are recomputed from the new lock date on re-entry, moving out only:

decision_date: **none (deferred)** — provisional 2027-08-02 · extension_date: **none (deferred)** —
provisional window end **Monday 2027-06-14** (Correction 2; the drafted 2027-06-12 is a Saturday),
decided Monday 2027-09-20 · hard_stop: **none** (DP-13's single automatic extension, then DEFERRED,
replaces it) · rule: **exposure-driven**, and **blocked** — the blocker is a rule-14 grant, not time
or sample · window: provisional pick nights 2026-06-01..2027-04-30 · gates on re-entry: ≥ 80
contributing nights per primary endpoint (E1 and E2 share the §2 definition, DP-21) **and** ≥ 30
contributing nights dated after the lock commit (DP-24), on `eval.py`'s measured counts at a single
decision pass.

Arithmetic checked independently at this run. Primary window: 80/0.35 = 228.6 → 229 sessions ×
1.4484 = 332 days from 2026-06-01 → 2027-04-29; the draft's **2027-04-30** (a Friday) is one day
later — out, never in. Decision date: 2027-04-30 + 60 sessions ≈ +87 days = 2027-07-26, + one week =
2027-08-02, which **is** a Monday. Ceiling test: 2026-06-01 → 2027-09-13 is **469** days and
`1.4484 × 80/r + 87 + 7 ≤ 469` solves to **`r ≥ 0.309`**, so the draft's **0.31** is correct and
rounded the conservative way. Extension: 30 sessions after Friday 2027-04-30, Memorial Day
2027-05-31 removed, is **Monday 2027-06-14**, not 2027-06-12 (a Saturday); 60 sessions on from there,
with Juneteenth observed 2027-06-18, Independence Day observed 2027-07-05 and Labor Day 2027-09-06
removed, is Thursday **2027-09-09**, + one week = 2027-09-16, first Monday on or after =
**2027-09-20**, so the drafted extension decision date is unchanged. The Steward re-confirms every
date session by session from the trading calendar at `record`.

## Standing rules added

_none._ Nothing here is Haci's word: items 2, 3, 4 and 8 were DECIDED on existing entries and locked
precedent, and item 1 was DEFAULTED under DP-41, which adds no DP entry (DP-40).

## Standing rules proposed

- **A post-pick-night quantity may be an outcome; it may not select the population, assign an arm or
  choose a control without a scoped DP-05 grant.** This is the line Q009 §6 draws in passing and
  Q008 §6.1 paid for, and it is the whole of the difference between the two. Writing it once would
  stop every future path-conditioned hypothesis (H-033, and the several like it in F4 and F6) from
  re-arguing rule 14 from first principles in its §6 — and would tell the Registrar at drafting time
  that such a question needs a grant **before** it is drafted, not after.
- **A question may cite only a locked PREREG as precedent.** Q020's §6 rested on a reading
  "Q019 registered today" — a sibling draft written hours earlier in the same autonomous cycle,
  itself unlocked. Two drafts can otherwise bootstrap each other into a policy neither would have
  been granted alone, which is exactly what nearly happened here.
- **Where a hypothesis conditions on a completed excursion, the exception it needs is a property of
  the hypothesis, not of the draft.** The desk could see this from H-033's one-line BACKLOG entry
  ("L4 touched → retrace to L2 → re-advance") without writing a 700-line PREREG first. A DP entry
  telling the Registrar to run the rule-14 test at registration time — and to file straight to
  DEFERRED under DP-47's "new data needed" clause, extended to "new licence needed" — would have
  saved the drafting round.
