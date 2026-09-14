# Deferred questions — registered as un-answerable with the data the desk holds

A question lands here when its **objective cannot be measured** from the frozen manifests, not when
it merely lacks sample size. Sample-size problems get a PREREG with a floor date (see Q002/Q003/Q004);
data problems get this file. Each entry names the exact data that would move it back into the
backlog. Nothing here may be reported, briefed or quoted in any form until that data exists.

**Second admission ground, added 2026-09-13 (DP-43).** A sample-size problem *does* land here when
the earliest honest decision date is **more than 12 months after lock** — DP-43 sends such a question
to this file "with that date named instead of being locked", because a PREREG whose floor date sits
years out fills the family correction with a question the platform will have outgrown. Such an entry
names the measured exposure rate, the projected floor date, and the re-check trigger, in place of the
missing table a data entry would name. It is still bound by the same rule as every other entry:
nothing here may be reported, briefed or quoted.

**Opened 2026-09-10 by the registrar, registration round R1.**

## H-055 — "Leg out at the first touch of the short strike (L3) instead of holding to expiry" — and H-056's DTE recommendation

Both of these are **option-structure** questions wearing stock-path clothing, and the desk holds
**no option price history at all**. `manifest_prices_v001` contains Alpaca daily raw and
split-adjusted equity bars plus hourly equity bars including pre/post-market; there is no options
chain, no per-contract OHLC, no bid/ask, no implied volatility, no open interest history. The
platform tables do not fill the gap either: `whale_watch_ledger` is empty (0 rows, verified in
manifest_v001), `uoa_symbol_daily` carries aggregate premium and score columns but no contract-level
marks, and its `fwd_return_*` columns are degraded and banned as outcomes (DATA_NOTES; FREEZE_v001
§5). H-055's claim is that closing a vertical at the first L3 touch beats holding it to the
session-20 close; the stock path can say how often price touched L3 and how often it was back below
L3 at session 20, but it **cannot** say what the spread was worth at either moment — that depends on
time to expiry, the IV path, the strike width and the skew, and the whole point of the claim is a
comparison of two option P&Ls. H-056's second half has the same defect: mapping a target's ATR
distance to a DTE band is a recommendation about **which contract to buy**, and it cannot be
validated on a metric that contains no theta. Running either on the stock proxy alone would produce
a number that looks like a finding and is not one, which is exactly the failure mode this desk
exists to prevent. **Q002 therefore tests only the equity-path half of H-056 (unconditional speed to
target), and Q006 reports touch-then-settle at L3 as a descriptive statistic — neither may be
presented as evidence about spreads or expiry choice.** To move these back into the backlog the desk
needs, for every published pick's symbol and for the matched-control symbols, a frozen options
history covering the pick night through 60 sessions forward: per-contract daily OHLC or end-of-day
marks with bid/ask, open interest and implied volatility, for at least the strikes spanning L1–L6
and the 7–60 DTE range, from a source the Data Steward can pin with a sha256 (a paid EOD options
feed, or Alpaca's options endpoints if the subscription is extended to historical chains). With that
in hand, H-055 becomes a clean paired comparison — same spread, two exit rules — and H-056's DTE
recommendation becomes testable as realized option P&L per DTE band. Until then both stay here.
**Revisit when an options price freeze exists; no decision date can be set, because the blocker is
procurement, not time.**

---

## H-062 — "Bear-direction picks touch their ladder levels less often than same-night candidates' downside at the same ATR distance"

**Deferred 2026-09-13 by the registrar, autonomous run, under DP-43's 12-month ceiling. Blocker:
the platform does not publish bear picks often enough for the night floor. Would have been Q014.**

### What the question is, and why it is worth keeping

A skip rule. If published bear-direction picks reach their own targets *less* often than
distance-matched same-night candidates' downside — i.e. the selection layer subtracts value when it
points down — the platform should stop publishing bear picks, or publish them only in a weak tape.
The mechanism is plausible: bear setups fight the prevailing tape, and the bear projection library
(`projection_bear_v2`) is new and starts 2026-05-15. The counter-mechanism is equally plausible: the
in-sample read is entirely an up-tape, so "bear picks under-run" may be nothing but "everything that
pointed down under-ran in April". That is exactly the question a sealed weak-tape sample would
settle, and it is the reason the hypothesis was not simply killed.

### Why it cannot be registered — the exposure arithmetic

The endpoint is night-level (rule 6): a **bear-contributing night** is a non-excluded pick night
carrying at least one published bear-direction pick with a usable ladder. No framing of this
hypothesis escapes that unit — the treatment arm *is* a published bear pick, and pooling bear picks
across nights does not create nights.

Measured exposure, from the frozen freeze only (`manifest_v001` + `manifest_prices_v001`,
`exclusions_v003.json`; counts are of *nights carrying a bear pick*, never of outcomes — no results
directory was read, and none of the sealed return figures below the line in BACKLOG.md was used to
compute a floor):

| quantity | measured | source |
|---|---:|---|
| Published bear picks, 2026-04-01..2026-09-10 | 45 (25 of them in April) | weekly 2026-09-10 §6 |
| Bear-contributing nights, W20-matured, 2026-04-01..2026-08-12 | 22 (36 picks) | weekly 2026-09-12 §6 |
| — of those, inside the DP-06/DP-43 window (≥ 2026-06-01) | **8** | weekly 2026-09-12 §6 |
| All-pick contributing nights in the same span (2026-06-01..08-12, 51 sessions) | 47 | `STEWARD_Q011_exposure.md` §3 |
| **Bear-contributing nights per session, in-window** | **8 / 51 = 0.157** | derived |

Against that rate, and using the same two-step construction every Steward exposure report uses (raw
pick-night date at 365/252, then + 20 sessions maturity + 7 days freeze margin, next Monday):

- **DP-21, 80 contributing nights per primary endpoint** — 72 more nights needed beyond the 8
  measured, at 0.157/session = **459 further sessions**. Raw 80th bear pick night ≈ **2028-06-07**;
  maturity- and margin-adjusted decision date ≈ **2028-07-17**. That is **~22 months past DP-43's
  ceiling** of 2027-09-13.
- **DP-24, 30 contributing nights after lock** — ≈ 191 sessions, decision date ≈ 2027-07-26. Inside
  the ceiling, but it is not the binding gate; the 80-night floor is.
- **20 per stratum cell** — the hypothesis's second clause ("or only in weak tapes") needs ≥ 20
  bear-contributing nights *inside a weak-tape stratum*. Measured today in the weak tape: **8**. The
  strong-tape half of the hypothesis is the half the data has, and it is the half that cannot
  distinguish the mechanism from the tape.

The conclusion does not depend on the rate assumption. Even at the whole-sample Apr–Sep rate of
22 bear nights / 87 matured nights = 0.253/session — a rate that leans on the April tape and that
DP-06/DP-43 would not let the window use — 80 bear-contributing nights is ≈ 316 sessions ≈ 15 months
of new nights, still outside the ceiling. There is no honest window that reaches the floor inside
12 months, and DP-43 forbids shortening the window or DP-21 forbids lowering the floor to get there.

### What was considered and rejected before deferring

- **Merging into Q006** (DP-29): rejected. Q006 carries bull/bear as a *stratification cell* (§5),
  not as a primary endpoint; its two primaries pool direction, and its own §5 anticipates thin cells
  being SUPPRESSED. Q006 will therefore give at most a descriptive bear read, and only if the cell
  clears 20 nights — it cannot return a verdict on "bear selection subtracts value".
- **Registering with a demoted-to-descriptive bear arm** (DP-43's demotion clause): rejected. That
  clause demotes a secondary arm inside a question whose *primary* endpoint clears the floor. Here
  the bear arm **is** the primary endpoint; demoting it registers a question that cannot reach any
  verdict, and spends a slot in the F1 correction to do it.
- **A pick-level test on the 36–45 bear picks**: rejected outright — rule 6. The nights are the n.
- **Waiting under DP-13's single automatic extension**: rejected. DP-13 rescues a floor that is
  *marginal* at the decision date; this one is short by roughly 70 nights, not by a handful.

### What would move it back into the backlog

Two triggers, either of which is enough. Both are **measured by the Steward on a then-current
freeze**, never assumed from a projection:

1. **Accrual alone.** At today's rate the remaining wait falls inside DP-43's 12-month ceiling once
   roughly 48 bear-contributing nights have accrued from 2026-06-01, which happens around
   **2027-09-01**. Re-check at the first freeze on or after that date.
2. **A materially higher bear-publication rate, sooner.** The floor lands inside the ceiling from a
   lock today if the measured rate reaches ≈ **0.37 bear-contributing nights per session** (about 8
   of every 21 pick nights carrying a bear pick, against ~3 of 21 today). A sustained down-tape, or
   a platform config change to `bear_publish_threshold` / `bear_max_output_cap`, could produce that.
   Any freeze in which the Steward measures ≥ 0.37/session over a trailing quarter puts H-062 back
   at the front of the queue.

A third, non-time path exists and is the honest one to prefer if Haci wants the answer sooner: treat
"should the platform publish bear picks at all" as a **product decision informed by a descriptive
read**, not as a CONFIRMED research finding. Q006's bear cell and the weekly direction table are
that read. Under rule 10 neither supports a subscriber-facing claim, and under this file's preamble
neither may be quoted; the decision to publish fewer bear picks would be Haci's call on descriptive
evidence, filed as an ENHANCEMENT with that limitation stated, not a verdict this desk issued.

**Caveat carried forward, so no successor repeats it:** the direction figures in the weekly snapshots
(the −8.21% W20 bear return, the 54% vs 73% L2 touch gap) read sealed Jun–Aug data. Any future PREREG
on this hypothesis is **post-hoc with respect to manifest_v001** and must either say so in its §6 or
be built on a freeze whose nights postdate those snapshots. The exposure counts used above are not
subject to that caveat — they count nights that carry a bear pick, which is knowledge available at
16:05 ET on the pick night and contains no outcome.

---

## Q017 — "GEX pin risk and two-sided paths" (H-061) — **superseded by Q021 before lock; a bookkeeping entry, not a research deferral**

**Filed 2026-09-13 by the registrar, autonomous run.** Q017 is **not** here on either admission ground:
its objective is measurable from the frozen manifests, and its decision date (Monday 2027-08-09) sits
**inside** DP-43's 12-month ceiling on the Steward's measured exposure (0.868–0.909 contributing nights
per session, `research/reports/STEWARD_Q017_exposure.md` item 3). It is here for registration mechanics
only: **Q017's draft `PREREG.md` was committed before `@registrar apply` could fold in the amendments
recorded in its `DECISIONS.md`**, and the write guard treats a committed draft as locked (rule 3). The
desk does not untrack the file or rewrite history, so the question was **re-registered as Q021**
(`research/questions/Q021_pin_risk_two_sided/PREREG.md`) with every amendment folded in and with the
hypothesis, population, arms, endpoint, MPE, window, decision date, extension and decision rule
**unchanged**. The controller marks Q017 DEFERRED with the note *"superseded by Q021 — draft committed
before apply; re-registered with DECISIONS folded in"*.

**No data was unsealed.** Q017 was never run: no `eval.py` was written, no `results/` directory exists,
and no outcome of any kind — touch, `TWO_SIDED`, return or arm difference — was read for Q017 or for
Q021. The only measured numbers in either file come from the Steward's exposure count, which is counts
only and reads a forward bar solely to establish that it exists. H-061 is therefore **not** double-counted
in the F3 correction: Q021 is the one registered question, and `research/BACKLOG.md` records H-061 as
registered as Q021.

**Nothing moves this entry back into the backlog** — there is nothing to revive. The live question is
Q021; Q017's directory stays as the historical record of the draft and its decisions, and the Steward's
exposure report keeps its `STEWARD_Q017_exposure.md` filename because it was produced under that id.

---

## Q020 — "L4 touched → retrace to L2 → re-advance" (H-033) — **needs a rule-14 grant the desk may not give itself (DP-41)**

**Deferred 2026-09-13 by the registrar, autonomous run, on this file's first admission ground: the
objective cannot be measured with the licence the desk holds.** This is a **rule-14 blocker, not a
sample-size one** and not a DP-43 ceiling one — the blocker is a **grant**, not procurement and not
time. Drafted at `research/questions/Q020_l4_pullback_readvance/PREREG.md` (state stays
`PREREG_DRAFT`; no `PREREG_LOCKED`, no `schedule.json`); decisions at
`research/questions/Q020_l4_pullback_readvance/DECISIONS.md`, item 1.

### What the question is, and why it is worth keeping

Haci's example 1. A pick you are holding runs to its fourth ladder target, then trades back down to
its second. Is that a hold — re-commit at the next morning's open and work it back to L4 — or the end
of the move, flatten the runner? Both signs are tradeable and the PREREG registers both, with two
primaries required in the same sign: **E1**, the event-matched re-advance rate (L4 touched again
within 20 sessions of the decision basis, MPE +5.0 pp, DP-20), and **E2**, the event-matched realized
ATR of the re-add plan (MPE 0.25 ATR, DP-10), plus an absolute gate that E2's own expectation clear
zero. The design is complete and stands: population, arms, DP-12 event-matched control, decision rule,
threats. Nothing about it is unanswerable in principle — only unlicensed.

### The exception it needs, exactly

The hypothesis conditions on a **completed excursion**, so the classifier that assigns the event is
made of forward bars:

- **Tables and columns** — `prices_daily_split` daily OHLC, and `prices_hourly_raw` hourly OHLC for
  the same-session ordering rule (resolving the case where the L2 touch falls on the same session as
  the L4 touch).
- **Rows** — published picks **and** the unpublished same-night control pool. Both arms, because the
  DP-12 control is condition-first: a control enters only if it completed the same round trip at the
  same ATR distances from its own close.
- **Time** — bars from **sessions t+1 … t+40**, i.e. a decision time for that one input of **09:30 ET
  on session `b+1`, `b ≤ 40`** (at most session t+41). Every other input stays at 16:05 ET on the pick
  night.
- **Purpose** — assigning the EVENT (`a` = the first L4 touch, `b` = the first qualifying L2 touch at
  or after it) and therefore **population membership, control-set membership and the decision basis
  `X_b = O_{b+1}`**.
- **What it is not** — **no outcome** enters through it: every outcome is measured strictly after
  `X_b`. No selection-side input moves. It licenses nothing beyond this question.

### Why the desk cannot grant it

Under **DP-41** the desk grants itself no new rule-14 exception; it names the one it needs and defers.
The precedent chain, in one place: **Q008 §6.1 / DP-05(b)** is a **2-session** question-scoped grant
for exactly this kind of input, with the decision time for that one input moved to 16:00 ET on session
t+2, and DP-05 records that Haci **explicitly declined the standing-rule version** — the general
"a later clock is fine when the bar only classifies" licence — on **2026-09-13**; **Q009 §6 (locked)**,
the adverse-side mirror of this very shape, rests on the fact that *"no session-t+1 quantity enters
any primary endpoint **or any eligibility filter**"*, and Q020's EVENT **is** an eligibility filter on
both arms. Q020 asks for the Q008 licence over **40 sessions instead of 2**, on picks and controls
alike. The draft's contrary reading cited a **sibling draft** (Q019, unlocked the same day), which is
not precedent; that citation and the sentence "Q020 needs no rule-14 exception and requests none" are
struck from §6 (DECISIONS Correction 1), and `research/lib/validators.py:17`
(`ET_DECISION = "16:05"`) is left as the enforcement code wrote it (rule 15).

### What moves it back into the backlog

**One sentence from Haci: add the scope above to `research/DECISION_POLICY.md` DP-05 as (c).** There is
no data to buy, no table to build and no nights to wait for — the frozen manifests already contain the
bars. On that grant Q020 **re-enters the queue at the front** (DP-41), with:

- **DECISIONS.md items 2, 3, 4 and 8 binding** — the condition-first DP-12 control (minimum 3
  event-completing matched controls, picks below that dropped and counted); re-advance = first touch of
  **L4** again within **R = 20** sessions of `X_b`; the **full unit** position at `X_b` with the
  `BAND_EXITS` residual printed beside it as the descriptive execution report; and the schedule rule.
- **Corrections 1–4 already applied** to the PREREG (the exception request in §6, the Saturday
  extension date fixed to **Monday 2027-06-14**, DP-49 in the §9 brief bullet, DP-50(b) named in the
  §9 filing bullet).
- **The §5 schedule recomputed from the new lock date, never carried forward** (item 8): window start
  stays **2026-06-01** (DP-06), the window end is re-derived at the Steward's measured
  matched-contributing rate `r`, and the `r ≥ 0.31` ceiling threshold is **re-solved** against the new
  12-month ceiling — it tightens as the lock date moves later. Dates may move **out only** (DP-43,
  DP-45).
- **The two Steward requests revive with it and are HELD until then:** R1 (the counts-only exposure
  funnel, blocking for lock — it measures the very classifier in dispute, so it is not run while the
  question cannot be tested) and R2 (the `manifest_v002` / `manifest_prices_v002` successor pair, due
  before the decision pass, never a blocker for lock).

If, on re-entry, R1 measures `r` below the re-solved threshold, Q020 lands back here on the **second**
admission ground (DP-43's 12-month ceiling) with that measured rate named — a separate test that the
grant does not settle.

**Bookkeeping while deferred.** `research/BACKLOG.md` marks **H-033 deferred 2026-09-13 pending a
DP-05(c) grant**, not registered; Q020's two primaries are **not** in the F4 correction set (F4 is 9:
Q007 4 + Q008 3 + Q013 2) and **E2 is not** in F6 (F6 is 15, Q019 §7's figure). **No data was
unsealed:** no `eval.py` exists, no `results/` directory exists, no exposure count was run, and no
outcome of any kind — touch, re-advance, plan result or arm difference — was read for Q020. Under this
file's preamble nothing here may be reported, briefed or quoted until the grant exists.

---

## H-041 — "Repeat selection in the 10 days before earnings → the post-earnings path" (Haci's example 3)

**Deferred 2026-09-13 by the registrar, autonomous run, on this file's second admission ground
(DP-43's 12-month ceiling). Blocker: the treatment arm's unit is the (symbol, print) event, not the
pick row, and on that unit the earnings-proximate book is too thin to reach 80 contributing nights
inside 12 months. Would have been Q022; no question number is consumed and Q022 stays free.**
A second, independent blocker sits on the endpoint itself and is named below (locating the print to
the session). Not registered, not locked, no `eval.py`, no `results/` directory, no exposure count
run and **no outcome of any kind read**.

### What the question is, and why it is worth keeping

Haci's example 3. SAS publishes a name, and then keeps publishing it, in the ten days running into
its earnings report. Does that persistence say anything about how the stock trades *after* the
print — is the repeatedly-selected name the one to hold across the report, while the one-off pick is
the one to flatten before it? It is a real trading decision and it is adjacent to two things the desk
already believes: the standing finding that re-qualification after a favourable move is continuation,
and Q013's registered claim that an imminent print changes the path. Neither answers it. A confirmed
answer in either sign is tradeable (hold through / flatten before), which is why the hypothesis is
kept rather than killed.

**The backlog's own first step is done.** H-041 reads "expected n very small; broaden to all picks
with earnings in window first". That broadening is **Q013** (`research/questions/Q013_earnings_proximity/PREREG.md`,
locked 2026-09-13): all published picks with a scheduled report inside 20 sessions, arms 0–3 vs 4–20
sessions, L3 within 20 sessions of the next open against a distance-matched control. H-041 is the
residue the broadening was supposed to make tractable — and it is Q013's own measured funnel, below,
that shows the residue is not tractable.

### Why it cannot be registered — the unit, then the exposure arithmetic

**Step 1 — the unit is the print, not the night.** The outcome H-041 names is the *post-earnings*
path: one realization per (symbol, scheduled print). A symbol selected on four nights in the run-up
window has **one** post-print path, not four. Counting each selection night as an observation enters
the same forward bars into the estimator two to four times, and does so **hardest in the treatment
arm** — repeat selection is the treatment — so the inflation runs in the hypothesis's direction. That
is precisely what rule 6's "stock rows are aggregated per night first" exists to stop, one level up.
The honest population is therefore **one row per (symbol, print): the last selection before the
report**, classified repeat (≥ 2 published selections inside the 10-day run-up) vs single (exactly 1),
with the night of that last selection as the clustering unit and the same-night single-selection
events as the baseline (rule 5's "Y's rate when X did not happen, in the same regime").

**Step 2 — how thin the earnings-proximate book is** (counts only, frozen `manifest_v001` +
`manifest_prices_v001` against `exclusions_v003.json`; every figure below is a count of picks or
nights, never an outcome):

| quantity | measured | source |
|---|---:|---|
| Eligible published picks, pick nights 2026-06-01..2026-08-12 (48 matured non-excluded nights, 51 sessions) | 371 | `STEWARD_Q013_exposure.md` §1 |
| — report ≤ 3 sessions out (k = 0/1/2/3) | 44 picks, on 11 / 10 / 8 / 8 distinct nights | §2 |
| — report 4–7 sessions out | 42 picks, on 23 distinct nights | §2 |
| **— earnings-proximate, k ≤ 7 sessions** (the measured proxy for H-041's "within 10 days") | **86 picks = 23.2% of the book, 1.79 per window night** | §2, derived |
| Seasonal shape of that sub-book (arm-A picks per month) | **June 3 in 20 nights · July 30 in 20 · August 11 in 8** | §4 |
| Q013's both-arms contributing nights (the closest measured anchor for "a night carrying two earnings-proximate picks") | **23 of 48 = 0.4510/session**, monthly 10.0% → 70.0% → 87.5% | §3, §4 |
| Selection-history split, the only measured streak coverage the desk holds (April–May, picks with a full 10-session history) | 208 picks / 25 nights: **new (0 prior) 85 = 41%**, 1–2: 71 = 34%, **3+: 52 = 25%** | EXPLORE_001 §G (coverage counts) |

Two things follow. First, the earnings-proximate sub-book is **1–3 picks on a night that carries any
at all**, and it is nearly empty outside the six-week reporting bursts (3 arm-A picks in the whole of
June). Second, the 86 pick rows are **not** 86 events: with re-selections at roughly 59% of the book
and an in-sample multiplicity of 2–4 for the repeated names (EXPLORE_001 §B: SNDK ×4, WDC ×2, MU ×2,
QCOM ×2), they correspond to roughly **50–56 distinct (symbol, print) events** over 48 nights, i.e.
**≈ 1.1 events per window night**.

**Step 3 — the contributing-night rate.** A contributing night carries ≥ 1 repeat event **and** ≥ 1
single event, both earnings-proximate, each with ≥ 3 distance-matched controls (the B2 gate never
binds in this window — 0 of 181 picks fell below it, §3 — so matching is not the constraint; arrival
is). Taking the measured monthly arrival shape and the measured selection-history split, three
readings:

| reading | contributing nights / session | projected decision date | vs DP-43's ceiling (2027-09-13) |
|---|---:|---|---|
| **Event unit (the honest one)** — one row per (symbol, print), repeat vs single | **≈ 0.185** | ≈ **2028-04-03** | **~6.7 months past** |
| Q003's cells on pick rows — new (0 prior) vs 3+ streak, middle cell dropped | ≈ 0.20 | ≈ 2028-02-21 | ~5.3 months past |
| Most generous — repeat = ≥ 1 prior appearance, **pick rows, duplicates kept** | ≈ 0.32 | ≈ 2027-07-19 | inside, by counting one print up to four times |

Required rate, for reference: a window starting 2026-06-01 (DP-06) whose decision date lands on the
ceiling has ≈ 290 sessions of pick nights after the 27-session maturity (up to 7 sessions to the
print plus 20 graded sessions) and the 7-day freeze margin — so **≈ 0.28 contributing nights per
session** is the bar. **Only the reading that inflates n with duplicate outcomes clears it.** Dates
use the same two-step construction every Steward exposure report uses (sessions → calendar at
365/252, then + maturity + a 7-day margin, rounded to the next Monday).

**Step 4 — even the floor understates the problem.** Eighty contributing nights spread over ~14
months would carry perhaps six reporting seasons and, in the treatment arm, a handful of distinct
prints belonging to the small set of names SAS keeps re-picking (memory/semis, all reporting in the
same week of each season). Q003 §10 threat 2's leave-one-symbol-out sensitivity would very likely
decide such a verdict, and Q013 §8 clause 6's 20-night reporting-season cells would be unreachable.
The April–May streak share (25% at 3+) is also an **upper** bound for the post-June book: elite
repeats were a large part of that cell and elite publication has thinned to 12 / 8 / 3 / 2 picks per
month since June (DATA_NOTES; Q003 §10 threat 6), which pushes every rate above further down.

### The second blocker — the desk cannot locate the print to the session

The endpoint is *post*-earnings, so the entry basis is defined by the print. The desk holds the
scheduled report **date** and nothing else: no before-open / after-close flag (Q013 §10 threat 4) and
no as-reported source after 2026-05-30 to check the scheduled date against (Q013 §10 threat 8). For
Q013 that ambiguity merely dilutes — the print sits somewhere inside a 20-session window. For H-041 it
sits on the entry: a BMO print on session k has already gapped at the open of k, an AMC print on k
gaps at the open of k+1, and the only entry safe under both conventions is the open of session
**k+2**, which throws away the first post-print session — the session that carries the move the
hypothesis is about. Rows whose report moved after 16:05 ET on the pick night would be entered
*before* the print they are supposed to follow, and the desk cannot quantify how often that happens.
This blocker is not the reason for the deferral, but it does not disappear when the sample does, and
a future PREREG must answer it in §4 rather than inherit it as a threat.

### What was considered and rejected before deferring

- **Merging into Q013** (DP-29): rejected. Q013's arms are `k ≤ 3` vs `k = 4–20` with **no selection-history
  dimension anywhere** — neither its per-`k` cells nor its §5 sub-cells split by prior publications —
  and its §7 already declares H-041 "a different decision (selection persistence), overlapping
  population". Q013 cannot return a verdict on persistence into a print.
- **Merging into Q003** (repeat selection): rejected. Q003 contrasts first-time vs 3+ streak across
  **all** published picks, grades L3 within 40 sessions from the next open, and never measures a
  post-print stretch or conditions on a report date. An earnings-proximate cut of Q003 would be a
  sub-cell of a sub-cell, below the 20-contributing-night SUPPRESSION floor by construction.
- **Registering with the repeat arm demoted to descriptive** (DP-43's demotion clause): rejected. That
  clause demotes a secondary arm inside a question whose primary clears the floor; here the repeat arm
  **is** the primary (the H-062 precedent, verbatim).
- **Registering on pick rows rather than events** — the one reading that reaches the ceiling: rejected
  under DP-45 and the registrar's own charter. It buys the date by counting the same post-print path
  once per selection night, most often in the treatment arm.
- **Dropping the within-night pairing** (treatment events vs distance-matched controls only, with the
  single-selection comparison made across nights): rejected under DP-45. It lands at ≈ 0.30/session —
  marginally inside — but it gives up H-041's own baseline as a primary and confounds the contrast
  with the reporting season in a population that is *defined* by the reporting season. Every locked
  arm contrast on this desk pairs within night; this one would be the exception that bought a date.
- **Waiting under DP-13's single automatic extension**: rejected. DP-13 rescues a floor that is
  *marginal* at the decision date; this one is short by roughly 40–50 contributing nights.

### What would move it back into the backlog

All three are **measured by the Steward on a then-current freeze**, never assumed from the projection
above. The first two are alternatives; the third removes the second blocker and is needed either way
before a PREREG can state its §4.

1. **Accrual.** At the event-unit rate estimated here (≈ 0.20/session), a lock at date `D` has
   `A(D) + 0.20 × 220` contributing nights available inside a 12-month ceiling (220 = 252 sessions
   less maturity and margin), so the floor comes inside the ceiling once ≈ 36 contributing nights have
   accrued from 2026-06-01 — around **2027-03-01**. Re-check at the first freeze on or after that date.
2. **A higher measured rate, sooner.** Any freeze in which the Steward measures **≥ 0.28 event-unit
   contributing nights per session over a trailing quarter** — a quarter spanning both a reporting
   burst and a trough, so the seasonality is not averaged away — puts H-041 back at the front of the
   queue. The measurement to request, counts only: per pick night, the number of distinct
   (symbol, scheduled print) events whose print is within 10 calendar days, split by whether the symbol
   had ≥ 2 or exactly 1 published selections inside that run-up window, plus the count of nights
   carrying ≥ 1 of each with ≥ 3 valid matched controls. **That count is what overturns this entry**;
   the rates above are the registrar's arithmetic on Q013's funnel, not a Steward measurement, and they
   are offered to be falsified.
3. **A print-timing source.** A BMO/AMC field on the platform's earnings context, plus an as-reported
   earnings-date table covering the window (the existing post-hoc file ends 2026-05-30). With it the
   post-print entry is the open of the first session after the actual print and the scheduled-vs-actual
   drift is measurable; without it the entry must be the blunter `k+2` open, and that choice belongs in
   the PREREG's §4, stated, not discovered later.

**Bookkeeping while deferred.** `research/BACKLOG.md` marks **H-041 — DEFERRED 2026-09-13**, not
registered. **No F5 slot is consumed:** F5 holds H-040 (→ **Q014**, 2 primaries) and H-041, and the
family correction set stays **Q014 only, 2 primary endpoints**, exactly as Q014 §7 records it. H-041
is **not merged** into Q013, Q003 or Q014 (DP-29) — the overlaps each question declares stand as
written and none of them tests this hypothesis. **No data was unsealed:** the counts above come from
`STEWARD_Q013_exposure.md` (counts only, no outcome) and from EXPLORE_001 §G's *coverage* row
(picks / nights per streak bin). **Caveat carried forward, so no successor repeats it:** EXPLORE_001 §G
also prints an in-sample matched-control excess per streak bin, and BACKLOG H-052 summarises its
direction; those outcome figures play no part in this deferral, but any future PREREG on H-041 that
relies on the streak-bin structure is **post-hoc with respect to `manifest_v001`** and must say so in
its §6 or be built on a freeze whose nights postdate those reads. Under this file's preamble nothing
here may be reported, briefed or quoted.

---

## H-067 (arm only) — "analyst revisions" as a benchmark arm of Q024 — **the desk holds no point-in-time analyst data of any kind**

**Deferred 2026-09-13 by the registrar, autonomous run, on this file's first admission ground (the
objective cannot be measured from the frozen manifests). This is an *arm-level* deferral, not a
question-level one: `research/questions/Q024_sas_vs_simple_benchmarks/PREREG.md` is drafted with the
six arms that can be built legally and names this one as missing (Q024 §1, §7). No question number is
consumed and no F1 slot is spent.**

### What the arm would have been

Haci's INBOX line of 2026-09-13 lists seven "embarrassingly simple alternatives" the SAS slate should
have to beat, one of which is **analyst revisions**: rank the same night's candidate pool by recent
upward revisions to consensus estimates or price targets, take the top `k_t`, and grade that portfolio
on the identical price-path objective — first touch of a target at the pick's own ATR distance, within
20 sessions of the session t+1 open. It is a good benchmark precisely because it is the one simple
alternative that is *not* a price transform: B4–B6 (momentum-20, momentum-60, a technical rank) are all
functions of the same bars, so they can be correlated with one another and with the picks, while a
revisions rank is an independent information source and is the sternest of the seven.

### Why it cannot be built

**There is no analyst, estimate-revision, rating-change or price-target field anywhere the desk can
reach, in any freeze or any platform table.** Checked at platform SHA `fa70688…`, read-only:

- `models.py` — no column matching `analyst|price_target|estimate` anywhere in the ORM.
- `services/symbol_context_builder.py` — the FMP enrichment path writes profile fields (including the
  `industry` column that is 12% populated, PI-007); it requests no estimates, no ratings and no targets.
- `services/super_agent_select_scoring.py` — the fundamental layer (weight 5) scores balance-sheet and
  growth quantities; no layer of the seven reads a revision of any kind.
- `manifest_v001`'s `sas_candidates` column list carries no such field, and no other frozen table
  (`uoa_symbol`, `gex_symbol`, `projection_bull`, `projection_bear_v2`, `conviction_monitor`,
  `market_regime`, `whale_ledger` — empty) holds one either.
- The only occurrence of the string "analyst" in `volatilx/services` is a prompt instruction —
  `services/market_intelligence_summary.py:38`, "Write like a professional market analyst…" — which is
  an LLM style directive, not data.

Substituting something else for it was rejected. A rank built on the fundamental layer would be a SAS
subscore, which makes the "simple alternative" a piece of SAS (Q024 §11.2 rejects the same move for the
technical arm); a rank built from a *current* vendor snapshot would be the future read backwards, a
rule-14 violation the desk cannot grant itself in autonomous mode (DP-41); and running a
revisions-flavoured proxy off price data would produce a number that looks like a benchmark and is not
one, which is the failure mode this file exists to prevent.

### What would move it back into the backlog

A **point-in-time** analyst feed the Data Steward can pin with a sha256, covering every SAS candidate
symbol (not only the published picks) over the question's window, with:

1. an **as-of timestamp per row** so rule 14 can be enforced — the revision must be shown to have been
   public at or before 16:05 ET on the pick night, and a vendor file that restates history without
   timestamps is not usable at any price;
2. **consensus EPS / revenue estimates and their revision history**, or rating changes and price-target
   changes with their publication datetimes, at daily granularity;
3. coverage broad enough that a night's pool yields at least `k_t` ranked names — the candidate universe
   runs ≈ 50–60 symbols a night, and a feed covering only large caps would silently change the arm into
   a size screen.
Candidate sources: an FMP estimates/upgrades-downgrades historical endpoint on the platform's existing
subscription tier, or a paid IBES / Zacks revisions history. Procurement is Haci's call; the desk asks
for nothing here and files nothing against the platform.

**Bookkeeping while deferred.** `research/BACKLOG.md` marks H-067 as **registered as Q024** with this
arm deferred. Q024 registers **six** primary endpoints, not seven, and F1's correction set is
**Q006 (2) + Q024 (6) = 8** primaries (Q024 §7). If the feed later exists, the revisions arm is a
**successor question** with its own PREREG — it is never added to Q024, whose lock fixes `m` (rule 3).
Under this file's preamble nothing here may be reported, briefed or quoted.

---

## Q025 / H-068 — "Is the SAS path edge a residual, or inherited sector / size / momentum / volatility exposure?" — **the exposure-matched control does not exist on any night**

**Deferred 2026-09-13 by the registrar, autonomous run, on this file's second admission ground
(DP-43's 12-month ceiling) — in its strongest form: the earliest honest decision date is not merely
beyond the ceiling, it is _undefined_.** Drafted at
`research/questions/Q025_exposure_attribution/PREREG.md` (never locked: no `PREREG_LOCKED`, **no
`schedule.json`** — the Q020 precedent; the controller carries `state.json` to `DEFERRED`); decisions
and the full record at
`research/questions/Q025_exposure_attribution/DECISIONS.md` ("## Record — 2026-09-13", item 16);
the measurement at `research/reports/STEWARD_Q025_exposure.md`. The question number **Q025 is
consumed by this entry and is not reused**. This is **not** the first admission ground: the
objective *is* measurable from the frozen manifests. What is unreachable is the night floor under
this question's own control construction.

### What the question is, and why it is worth keeping

Haci's attribution null. When SAS publishes a pick, does the stock reach the pick's own target more
often than same-night candidates the engine looked at and did not publish that are its **twins on
everything already known about them** — same sector, similar market beta, similar size, similar
20- and 60-session momentum, similar volatility — or does the apparent edge disappear once the twins
are chosen properly? Two primaries, both two-sided: **E1**, the residual after the full exposure
match (MPE ±5.0 pp, DP-20); **E2**, the attribution gap between the full match and Q006's
three-feature match (CONFIRMED `|E2| > 10.0 pp`, NULL CI-includes-0 **and** `|E2| < 5.0 pp`,
between the two INCONCLUSIVE). Both signs are tradeable and both were registered. The design is
complete and stands as the historical record; nothing about it is unanswerable in principle — only
unpopulated.

### Why it cannot be registered — the measured rate, and the mechanism

**Reason in one line: the measured binding (E2) contributing-night rate is 0.000 per elapsed
session, below the PREREG §5 gate of 0.35, so DP-21's 80-contributing-night floor is unreachable
inside DP-43's 12-month ceiling and no floor date is defined.**

Counts only, on `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, no live
query (DP-50(c)); no outcome of any kind was read and no post-match balance was measured
(`STEWARD_Q025_exposure.md`):

| quantity | measured | source |
|---|---:|---|
| **E2 (binding) contributing nights / matured elapsed sessions**, 2026-07-08..2026-08-11 | **0 / 25 = 0.000 per session** | §(h) |
| E1 contributing nights, same window | 0 / 25 = 0.000 | §(h) |
| Full-window cross-check on the pre-maturity quasi-eligible proxy | **0 of 46 nights** | §(h) |
| By month (matured) | July **0 / 18** · August **0 / 7** · September not yet measurable | §(h) |
| **Maximum simultaneously B1-valid picks on any single night, all 46 nights** | **2 — never 3** | §(h) |
| Picks carrying a valid B1 set (≥ 3 same-sector controls inside the 1.5-MAD five-feature caliper) | **15 of 197 matured = 7.6%**, scattered over 13 nights | §(d), §(f) |
| B1 drop share (< 3 controls) | **92.4%** overall; 85.7% (XLF, XLI) to **100%** (XLB, XLC, XLRE, XLU, XLY); **XLK 94.4%** on n = 71 | §(d) |
| **B4 (Q006's three-feature construction, verbatim) validity on the identical population** | **100% (199 of 199)** | §(e) |
| Projected floor date at the one-sided 90% lower bound of the measured rate | **undefined** (a 0.000 point estimate has a 0.000 lower bound) | §(h) |
| Even at the 90% Clopper–Pearson **upper** bound, ≈ 0.088/session | ≈ **909 elapsed sessions ≈ 3.6 years** to 80 nights, **for one endpoint alone** | §(h) |

**The mechanism, stated so no successor rediscovers it: the caliper inside the sector block is the
entire constraint.** The hard sector block (DECISIONS item 3) shrinks the same-night unpublished
pool to a median of **~5–7 names**; the five-feature 1.5-MAD caliper on `beta60`, `atr_pct`,
`mom20`, `mom60`, `log10(adv20)` then passes **7.6%** of picks, scattered so thinly that **no night
in 46 ever carried 3 B1-valid picks** (the observed maximum is 2). It is **not** sector thinness on
its own and **not** maturity: the matured and full-window proxy measurements agree (0/25 and 0/46),
and **XLK — the deepest sector in the book, 71 matured picks — drops 94.4%**, so the loss tracks the
caliper, not the size of the sector. It is **not** feature coverage (100% of published and 99.4% of
unpublished candidate rows carry ≥ 60 prior bars and all five features, §(c)). It is **not** the
sector artifact (sha256 `c4d12610…0201` re-verified against the git blob at `fa70688`, byte-identical
at HEAD `d19c9a9`). It is **not** a mid-window platform ship (the DP-50(a)/(b) sweep is clean:
`2d5776c` and `22a2e1b` touch neither the selection/publication path, the lane-plan writer, which
picks are published, nor any historical row). **B4 passes 100% on exactly the same picks** — the
crude match has controls everywhere the strict one has none.

**Waiting does not fix this.** Unlike H-062, this is not an arrival-rate problem that accrues away.
The constraint is a **per-night structural property of the match** — how many same-sector twins
inside 1.5 MAD on five features exist in a ~5–7-name pool — so nights arriving at ~21 a month add
nights at a rate of 0.000. **There is therefore no date-based re-check trigger in this entry and
none is invented.**

### What was considered and rejected before deferring

Each would have bought a floor by weakening the question, which DP-45 forbids.

- **The Steward's §(d) sensitivity** — reading "standardised units" as the conventional
  1.4826-scaled robust z, i.e. a ≈ 2.22 raw-MAD caliper (pick-level validity 4.0% → 16.8%; nights
  with ≥ 3 valid picks 0 → **12 of 46**). **Rejected.** It still measures ≈ 0.26/session, short of
  the 0.35 gate — but it is rejected **on principle, not on arithmetic**: the primary reading
  (literal, unscaled median/MAD) was fixed at `decide` with no scaling constant named in §2.3, §3 or
  the Q006 language it borrows, and adopting the looser reading *after* seeing that it is the one
  which produces nights is exactly the tuning rule 9 and DP-45 exist to stop. It is a **printed
  sensitivity here, never a promotion**.
- **Relaxing the hard sector block to a soft distance penalty** (the option DECISIONS item 3
  rejected). **Rejected, and it may never be done inside this question.** A residual measured
  against partly-same-sector twins is a weaker claim wearing the stronger claim's name; item 3 chose
  the block knowing its cost, and a gate shortfall is not licence to revisit a decision made before
  the counts existed.
- **DP-13's single automatic extension as a rescue.** **Rejected.** DP-13 rescues a floor that is
  *marginal* at the decision date; this one is short by **80 nights out of 80**, and no extension of
  any length reaches a floor at a rate of 0.000.

### What would move it back into the backlog — three conditions, none of them taken by the desk

**(a) A wider caliper, or a soft sector penalty in place of the hard block — a *different, weaker*
question, and therefore a successor PREREG, never a relaxation of Q025.** This is the only option
that makes the arithmetic work quickly (the §(d) sensitivity moves 0 nights to 12 of 46), and it is
precisely the one the desk **may not choose for itself**: DP-45 forbids loosening a match to reach a
floor, and the loosened question does not answer H-068 — it answers a nearby question about a
*partly*-matched residual, which must state in its own §1 that it is **not** "SAS's residual after
sector and exposure are held fixed" and must carry its own §10 disclosure that the control is
partial. If Haci wants it, it is registered **from scratch, with its own id, its own MPEs and its
own §10** — **Q025's file is not edited into it**. The desk's own view, stated once: the weaker
control is already on the desk and it is called **Q006**, which is the thing this question was built
to test.

**(b) A larger candidate universe per night from the platform — an ENHANCEMENT, not a desk action.**
The binding scarcity is pool size: ~50–60 candidates a night spread across eleven sectors leaves a
median of 5–7 same-sector names, and **no matching method recovers twins that do not exist**. A
platform change that widens the nightly candidate universe — a larger pre-screen, a lower
candidate-admission bar, or retention of the full scanned universe in `sas_candidates` rather than
the scored shortlist, or a per-sector floor on candidates retained — would raise the B1 pass rate
mechanically. Filed as **`research/ENHANCEMENTS.md` EN-016** with this measurement as its evidence;
Haci's call under DP-48. It is **never** a reason to change the study.

**(c) The re-check trigger, stated as a measured B1 pass rate — not a date.** Two counts, measured by
the Steward **on a then-current freeze over a trailing quarter**, never assumed from a projection:
**(i)** the share of matured published picks carrying a valid B1 set — ≥ 3 same-sector controls
inside **1.5 standardised (unscaled median/MAD) units** on `beta60`, `atr_pct`, `mom20`, `mom60`,
`log10(adv20)` — **today 7.6%**; and **(ii)** the count of nights carrying **≥ 3 such picks, per
elapsed session** — **today 0.000**. **The trigger is (ii) reaching ≥ 0.35 per elapsed session,
measured directly. (ii) is the count that overturns this entry, not (i).** For orientation only, and
offered to be falsified: at the window's ~8.1 published picks per night, a pick-level B1 pass rate of
roughly **26%** — about **3.4× today's 7.6%** — is what (ii) ≥ 0.35 implies under a binomial reading;
that arithmetic is the **decision-maker's, not the Steward's**. A necessary precondition, never once
observed in 46 nights, is that the **maximum simultaneously B1-valid picks on a single night reach
3** (today: 2). Re-check **at the first freeze after any platform change of type (b) ships, and not
on a calendar** — the blocker is structural, so no accrual date exists to name.

### Bookkeeping while deferred

**No verdict of any kind was produced.** Q025 returns **no NULL, no INCONCLUSIVE, no E1 number and
no E2 number**; a gate shortfall is not a verdict (DECISIONS item 14). **No `eval.py` was written and
no `results/` directory exists**, and no outcome — touch, first-touch date, return, excess or arm
difference — was read for this question at any point. All **54** direction × band × lane × sector
sub-cells are **SUPPRESSED with certainty**, not by projection (§(i)): no cell can reach 20
contributing nights while the endpoint rate is 0. **F1's correction set is unchanged at
Q006 (2) + Q024 (6) = 8 primaries** — Q025's two primaries **leave** F1 while deferred (the H-062
precedent), which is already what `research/questions/Q024_sas_vs_simple_benchmarks/PREREG.md` §7 and
the "H-067 (arm only)" entry above record, so **no cross-question edit is required and none was
made**. `research/BACKLOG.md` marks **H-068 — DEFERRED 2026-09-13**, not registered. The Steward's
successor-freeze rider (R2) is **withdrawn**: Q022's `manifest_v002` / `manifest_prices_v002` pair is
built to **Q022's own window end (2027-01-13)** and is not extended for this question. The
provisional dates the draft carried over from Q022 (window 2027-01-13, decision 2027-02-22, extension
2027-02-26 / 2027-04-05) and the 0.696 planning stand-in are **struck** — they were derived from a
looser eligibility rule, they are never inherited by a successor, and DP-43's 2027-09-14 ceiling is
recorded only as the line the undefined floor date fails to meet.

**One correction the desk could not make, recorded here instead.** `DECISIONS.md` asked the registrar
to fold six bookkeeping corrections into the draft (the `Q024` → `Q025` self-references, E2's
`10.0 / 5.0 pp` MPE band, the binding-endpoint rate, R1's three additions and its
no-post-match-balance prohibition, §8 clause 7's B1-only scope, and §10.9's Q006-dependence sentence),
and to strike the provisional dates and the 0.696 stand-in. **The draft was committed
(`4725303`) before `apply` could run, so the write guard treats it as locked and the desk does not
untrack the file or rewrite history** — the Q017 precedent, here without a re-registration, because
the question is deferred rather than live. **The PREREG therefore still reads under the old id in its
body (§5–§7, §10) and still carries the struck dates, the 0.696 stand-in and the pre-correction §7 and
§8 text; where it and this entry or `DECISIONS.md` disagree, `DECISIONS.md` "## Record — 2026-09-13"
governs, and any successor question builds from that record, not from the draft's body.** Under this
file's preamble **nothing here may be reported, briefed or quoted.**

---

## Q030 / H-074 — "Does the candidate universe contain the market's big movers before they move?" — **the base-universe price freeze cannot be built: no Alpaca credentials in the desk's session**

**Deferred 2026-09-14 by the registrar, autonomous run (DP-40..48), on this file's first admission
ground: the objective cannot be measured with the artefacts the desk holds.** The blocker is
**provisioning, not procurement, not accrual and not a grant** — the data exists at a vendor the
desk is already licensed to read (rule 1 names `ALPACA_API_KEY` / `ALPACA_SECRET_KEY`), and the two
variables are simply **not present in the desk's session environment**, so the freeze the question's
population is defined on has never been built. Drafted at
`research/questions/Q030_universe_discovery_recall/PREREG.md` (state `PREREG_DRAFT` → `DEFERRED`;
**never locked: no `PREREG_LOCKED`, no `schedule.json`** — the Q020 / Q025 precedent); decisions at
`research/questions/Q030_universe_discovery_recall/DECISIONS.md` (decision-maker, 2026-09-14, 13
items + 7 corrections); the measurement at `research/reports/STEWARD_Q030_universe_freeze.md`.
**Both files are preserved exactly as drafted** — nothing in either was edited or deleted for this
deferral — and the question **resumes at `@registrar apply Q030`** when the trigger below is met.
**The question number Q030 is consumed by this entry and is not reused.**

### What the question is, and why it is worth keeping

Haci's H4, *Discovery*. The ~57 stocks VolatilX puts in front of its scoring engine each night —
does that pool contain the names that are about to make a big move far more often than the same
number of names drawn at random from the investable market, **at least twice as often**? One
primary, night-level, two-sided: **E1, the discovery lift** = mean nightly `recall_t`
(`|M_t ∩ U_t^B| / |M_t|`, movers being base-universe symbols whose session high first touches
`C_t + 3 × ATR14` somewhere in t+1..t+20) divided by mean nightly `e_t` (`|U_t^B| / |B_t|`, the
same-size uniform draw's expectation), **MPE lift ≥ 2.00** (Haci's own number), mirror ≤ 0.50, with
the **materiality floor `D = mean(recall_t − e_t) ≥ +1.0 pp`** as an inseparable second condition.

**It is the step before every other selection question, and nothing else on the desk can stand in
for it.** Q006 draws its controls from the night's own candidate pool; Q024's sector-random arm
draws from the same pool; Q027 ranks inside it. **None of them can see what the pool never
contained.** Q030 is the only registered question whose population is the market *outside* the pool,
and both signs are consequential: a confirmed lift below 1 — the universe systematically avoiding
the names that move — would be the most important thing this desk could say about candidate
generation. The design is complete and stands: population, the `n_t = |U_t ∩ B_t|` denominator with
the as-filed `|U_t|` version blocking, four baselines, the DP-51 two-CI gate, the corroboration gate,
the mid-window split rule. Nothing about it is unanswerable in principle — only unbuilt.

### Why it cannot be registered — the failing limb, named exactly

The lock-or-DEFER gate (DECISIONS item 10, PREREG §5.3 R2) has three limbs: **credentials present**
**and** **≥ 90% of the 2,405 pinned base symbols returning ≥ 60 daily bars** **and** an
all-candidates contributing-night rate **≥ 0.36 per elapsed session**.

**The failing limb is credentials: `no ALPACA_API_KEY / ALPACA_SECRET_KEY in the Steward's
environment, so `manifest_prices_universe_v001` cannot be built`.** Checked with a direct presence
test in the Steward's shell — stated, never inferred, per the Q024 R1(d) precedent — and the same
absence was confirmed independently in the coordinator's own session. It is the same failure mode as
`STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md` §(d).

**Coverage is UNMEASURED, not failed.** Because limb (i) failed, the request's own instruction —
*"if it cannot be built, say which limb fails and stop"* — stopped the run: no Alpaca probe was
attempted, no symbol list was narrowed, no coverage share was estimated. The ≥ 90% limb is therefore
**untested and may still fail on measurement**; this entry does not claim it would pass.

**The rate limb PASSED and is not the blocker.**

| quantity | measured | source |
|---|---:|---|
| **(i) Credentials** — `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` present in the desk session | **ABSENT (both)** | `STEWARD_Q030_universe_freeze.md` §(i) |
| **(ii) Coverage** — share of the 2,405 pinned symbols returning ≥ 60 daily bars (gate ≥ 90%) | **NOT MEASURED** — probe blocked by (i) | §(ii) |
| **(iii) Build** — `manifest_prices_universe_v001` | **NOT BUILT**; no manifest path, no sha256, no rows; nothing written to `research/data/` | §(iii) |
| **(iii-rate) All-candidates contributing nights per elapsed session** (gate ≥ 0.36) | **0.6761 (48/71) — PASSES, clears the gate by 88%** | `STEWARD_Q027_exposure.md`, borrowed as a conservative lower bound (Q030's night rule is strictly broader) |
| Pinned sector blob re-verified (credential-free) — entry count | **2,405**, matches the PREREG exactly | §(ii), `volatilx` `data/sp500_sectors.json` at `4171b1a` |
| Pinned blob sha256, LF-normalized | **`c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201`**, matches exactly; no disagreement to flag | §(ii) |
| **(iv) Nights with `n_t ≥ 1`**, pick nights 2026-06-01..2026-08-12, after `exclusions_v003.json` | **48 of 48 (100%)**; raw 51 of 51 | §(iv) |
| `n_t` min / median / max, post-exclusion | **45 / 60.5 / 68** (raw 45 / 61.0 / 68) | §(iv) |
| Nights removed by `exclusions_v003.json` in that span | **3** — 2026-06-26 (`uncorroborated_publication_runs`), 2026-07-02 and 2026-07-06 (`manual_runs`) | §(iv) |
| **Nights with `m_t ≥ 1`** | **UNAVAILABLE** — needs universe-wide bars | §(iv) |
| **`b_t` (gradeable base universe, ≥ 60 bars ≤ t plus a bar on night t)** | **UNAVAILABLE for the same reason** — the Steward's correction to the coordinator's framing | §(iv) |
| Only pinned price freeze the desk holds | `manifest_prices_v001`, **436 symbols** (candidates + benchmarks) — not `B` | §(iv) |
| As-filed residue (candidate symbols outside `B`, descriptive) | 7 of 51 nights, **one distinct symbol, `BRK.B`** — a ticker-format mismatch against the blob's key, not a true non-`B` name | §(iv) |

**The mechanism, stated so no successor rediscovers it.** Every quantity in this question's
denominator is defined over `B` — `b_t`, `m_t` and `e_t` all require daily bars for all 2,405 base
symbols — and **the desk's only price freeze covers 436 symbols, which are the candidates and the
benchmarks: precisely the names the universe already found.** There is no partial route. `n_t` is
computable from `manifest_v001.sas_candidates` and the pinned blob alone, and it is never zero (48/48
nights), which says the *numerator side* of the night rule would never bind — but a recall with no
measurable mover set is not a statistic. **Waiting does not fix this**: nights accrue at ~21 a month
and not one of them brings a bar for a symbol outside the 436, so there is **no date-based re-check
trigger in this entry and none is invented**.

### What was considered and rejected before deferring

Each would have bought a lock by weakening the question, which DP-45 forbids.

- **A narrower symbol list — build the freeze over whatever subset the desk can reach.** Rejected.
  `B` *is* the population; a denominator built from a subset of `B` is a different population, and
  the whole point of H-074 is the market **outside** the pool. Shrinking `B` shrinks `m_t` and `e_t`
  together in a direction nobody can sign in advance, and the lift it produces answers a question
  nobody filed.
- **Using `manifest_prices_v001`'s 436 symbols as `B`.** Rejected outright, and named here because it
  is the tempting one: those 436 are the candidate symbols plus benchmarks, so `U_t^B` would be
  nearly all of `B_t`, `e_t` would approach 1 and the lift would approach 1 **by construction** — a
  number that looks like a finding and is the arithmetic of its own denominator.
- **A random sample of `B` (say 400 of the 2,405).** Rejected. It is the subset defect plus a second
  one: `m_t` on a sample is a handful of symbols a night, so `recall_t` becomes a ratio of very small
  counts and the night statistic is noise the 80-night floor cannot absorb.
- **Estimating coverage from anything other than the probe** — from the 436-symbol freeze's fill
  rate, from the blob's composition, from a vendor's published coverage claim. Rejected; R2 disallows
  it explicitly, and a lock gate settled on an estimate is not a gate.
- **A platform table in place of the freeze.** Rejected — no platform table holds daily bars for the
  base universe; `uoa_symbol_daily` covers a screened subset and its `fwd_return_*` columns are
  degraded and banned as outcomes (DATA_NOTES; FREEZE_v001 §5).
- **Locking now and building the freeze before the decision pass.** Rejected. DECISIONS item 10 makes
  R2 **blocking for the lock** precisely because a PREREG whose population cannot be constructed is
  not falsifiable at lock (rule 3), and a lock that assumes a freeze which may never exist would put
  a question into F8's correction set that cannot be run.
- **DP-13's single automatic extension, or any wait.** Rejected — DP-13 rescues a floor that is
  *marginal* at the decision date. No floor is short here; the rate limb passes at 0.6761. Nothing
  accrues toward a credential.

### What would move it back into the backlog — the trigger is a measurement, not a date

**Both conditions, measured in the Steward's own session on a then-current freeze, never inferred and
never projected:**

1. **Credentials present.** A desk session in which **both `ALPACA_API_KEY` and `ALPACA_SECRET_KEY`
   are present**, stated explicitly by the Steward with a direct presence test (the Q024 R1(d)
   precedent: presence is asserted, never assumed).
2. **Coverage measured at ≥ 90%.** The Steward's **trailing-60-session probe over all 2,405 symbols**
   in the `mapping` key of the pinned blob returns **≥ 90% of them with ≥ 60 daily bars**, with the
   count and list of zero-bar symbols reported, and with the blob re-verified at 2,405 entries and
   sha256 `c4d12610…0201` (any disagreement is a loud failure). **If the probe runs and returns
   below 90%, Q030 lands back in this file on the coverage limb with the measured share named** —
   that is a different finding from today's, and this entry does not pre-empt it.

**On both conditions holding, in this order:** R2(iii) builds and pins
`manifest_prices_universe_vNNN` (daily bars, `adjustment=split` **and** `raw`, `feed=sip`, all 2,405
base symbols plus every in-window candidate symbol and the existing benchmarks, ≥ 60 sessions before
the window start through t+20 of the last in-window pick night, symbols lacking bars excluded and
counted, never back-filled or imputed); R2(iv)'s counts-only `b_t` / `n_t` / `m_t` dry run fixes the
sub-cell suppression list; **Q030 re-enters the queue at the front** (the Q020 precedent) with
**`DECISIONS.md` binding in full** — items 1–13, Corrections 1–7 — folded into the PREREG at
`@registrar apply Q030` before any lock. **§5.2's schedule is then re-derived session by session
from the actual lock date, out only** (DP-43, DP-45): the window opens on the first trading session
after the lock commit, the 119-session window end, the 2027-04-12 decision date, the 2027-04-19
extended window end and the 2027-05-24 extension decision **are not carried forward as dates** —
they are the arithmetic at a 2026-09-14 lock and nothing else. The **rate limb is not re-measured**;
0.6761 is re-tested only as an inequality against the gate **re-solved from the new lock date
against DP-43's 12-month ceiling**, which **tightens as the lock slips** (Correction 3). If the
re-solved gate ever exceeds 0.6761, Q030 lands back here on this file's second admission ground with
that arithmetic printed.

**Whose call it is.** Provisioning two environment variables the desk is already licensed to use is
**Haci's**, and it is neither a purchase nor a platform change: no `IMPLEMENTATION_BRIEF.md` follows
from this entry, no enhancement is filed against the platform, and **DP-49 is not engaged** (nothing
here hands a coding agent a database step). Rule 1 is untouched — the desk asks for no credential it
is not already named to hold, and asks for no other.

### Bookkeeping while deferred

**No verdict of any kind was produced.** Q030 returns **no CONFIRMED, no NULL, no INCONCLUSIVE, no
E1 and no lift**; a gate shortfall is not a verdict. **No `eval.py` was written and no `results/`
directory exists.** **No outcome of any kind was read** for this question at any point — no touch,
no first-touch date, no return, no excursion, no `outcome_*` column, no `sas_selection_excursion`, no
`uoa_symbol_daily.fwd_return_*`, no recall, no lift and no intersection count; the Steward's report
is counts of candidate symbols, an exclusions tally and a blob hash, on the pinned freeze, with **no
live query** (DP-50(c)).

`research/BACKLOG.md` marks **H-074 — DEFERRED (Q030 drafted; universe price freeze needs Alpaca
credentials in the desk session)**, not registered. **F8's BH correction set does not contain Q030
while deferred** (the H-062 / Q025 precedent), so F8 carries **no registered primary today** —
H-081 and H-083 join it when they lock, and Q026 / Q028 are diagnostics that enter no correction set
in any case. **No cross-question edit was required and none was made:** Q027 (F2) is untouched and
its own R2 / R3 freeze requests stand on their own scope — the one-freeze-serves-both efficiency
(PREREG §5.2) simply does not materialize while Q030 is deferred. Q030's Steward requests are
**HELD and revive with the question**: R1(b)–(d) (corroboration gate, the non-`B` residue, the
universe-side commit sweep), R3 (the successor selection freeze on Q030's account) and R4 (the sealed
B-wide bars for the labelled post-hoc panel, droppable by construction); **R2 does not revive — it
*is* the trigger above.**

**The draft is preserved, and DECISIONS.md governs where the two disagree.** `apply` never ran, so
the PREREG body still carries the pre-correction text: the borrowed 0.9538 planning rate and its
8-session cushion, the 92-session window ending 2027-01-26, the decision date 2027-03-08 and the
extension 2027-04-19, §5.3 listing all three gate limbs as pending, §9's flag-off dates, and §4.3's
reference to R1 rather than R2(iii). **Where the draft and `DECISIONS.md` disagree, `DECISIONS.md`
governs** (the Q025 precedent), and at `@registrar apply Q030` Corrections 1–7 plus the recomputed
schedule are folded in **before** any lock — which is the whole reason the draft is kept rather than
rewritten now. Under this file's preamble **nothing here may be reported, briefed or quoted.**

---

## H-080 — "Is 90 a real boundary or a historical artifact?" (Haci's H10, *Threshold stability*) — **the median pick night carries no candidate at all above 90**

**Deferred 2026-09-14 by the registrar, autonomous run (DP-40..48), on this file's second admission
ground (DP-43's 12-month ceiling), with a second, structural limb that does not accrue away.
Not drafted: no PREREG, no directory, no `eval.py`, no `results/`, no Steward request issued, no
outcome of any kind read. No question number is consumed — Q033 stays free** (the H-041 precedent,
not the Q020 / Q025 / Q030 one, which consume a number because a draft exists).

### What the question is, and why it is worth keeping

The 90 line is the most consequential hand-set number in the product. It decides what is called
elite, it is Haci's own after-hours entry trigger (DP-03(a)), and DP-42 fixes `overall_score ≥ 90` as
the desk's standing definition of "elite" in every question that needs one. H-080 asks whether that
line is *earned* — whether a walk-forward search for the cut `c` that maximises the within-night
control-adjusted L3-touch excess (Q006's `E_t`) of candidates `≥ c` over candidates `< c` keeps
landing near 90 in window after window, or whether the optimum wanders and 90 is an artifact of the
tape it was chosen in. Both signs are consequential and neither is available anywhere else on the
desk: a PASS defends every elite rule the platform prints, and a FAIL is the trigger for H-083's
categorical setups and would retire the hard threshold. The hypothesis is kept, not killed.

### Why it cannot be registered — limb 1, the exposure arithmetic

Both of H-080's primaries live **above 90**, and every night that carries no candidate above 90 is
silent on both. Counts only, from the two pinned Steward reports, no live query (DP-50(c)), no
outcome column read:

| quantity | measured | source |
|---|---:|---|
| All-candidates contributing nights, 2026-06-01..2026-09-10 (71 elapsed sessions) | **48 / 71 = 0.6761 per session** | `STEWARD_Q027_exposure.md` (a) |
| Eligible candidate rows on those 48 nights | 2,459 | (a) |
| — rows with `overall_score ≥ 90`, and the nights carrying ≥ 1 of them | **18 rows on 17 of 48 nights (35%)** | (d) |
| — rows in `[85, 90)`, and the nights carrying ≥ 1 | 57 rows on 33 of 48 nights | (d) |
| — rows in `[80, 85)` / `[70, 80)` / `< 70` | 627 / 575 / 1,182, each on 48 of 48 nights | (d) |
| **Rows ≥ 90 per elite-present night** | **18 / 17 = 1.06** | derived |
| **Rows ≥ 90 on the median contributing night** | **0** (17 of 48 nights carry any) | derived |
| ATR-elite cap firing (the backlog entry's suspected cause of the thin band) | **2 of 4,020 rows (0.05%), both at 79.9, none at 84.9** | (d) — measured, and **not** the cause |
| Published-pick basis, for comparison: band `[90, ∞)` picks / nights, 48 matured nights | **15 picks on 14 nights** | `STEWARD_Q015_exposure.md` (2), (4) |
| — by month, published elite picks | **June 11 · July 4 · August (matured to 08-12) 0** | `STEWARD_Q015_exposure.md` (9) |

**Derived rates — the registrar's arithmetic on the Steward's counts, offered to be falsified:**

- **Elite-present contributing nights per elapsed session = 17 / 71 = 0.2394.**
- **Both-arms nights** (≥ 1 row ≥ 90 **and** ≥ 1 row in `[85, 90)`, which primary 2 requires) have
  **not** been measured. Their count cannot exceed 17, so **≤ 0.2394/session**; under independence it
  is ≈ 17 × 33/48 ≈ 11.7 nights ≈ **0.165/session**. Every figure below uses the **upper** bound, so
  the conclusion does not rest on the estimate.
- The pooled 0.2394 is itself an **upper bound on the current rate**: the published-elite series runs
  11 → 4 → 0 picks by month and PI-010's whole-history series is 8 / 13 / 12 / 8 / 3 / 2, with Q005
  INCONCLUSIVE on the cause. Nothing in the measurement suggests the rate is recovering.

**Floors (rule 6 as read by DP-21).** Primary 1 is the dispersion of `c*` across **≥ 4
non-overlapping windows** with PASS at every `c*` inside `[87, 93]`; each window is a cell, so 20
contributing nights per window and ≥ 80 for the endpoint. A night can discriminate cuts inside the
PASS band only if its `≥ 90` arm is non-empty, so its contributing nights **are** elite-present
nights. Primary 2 is the `≥ 90` vs `85–89` contrast on a **held-out** window — 80 contributing nights
for the endpoint, each carrying both arms, on nights disjoint from the training windows, because that
is what held-out means.

| reading | elite-present nights needed | at 0.2394/session | last pick night | decision date | vs DP-43's ceiling (2027-09-14) |
|---|---:|---:|---|---|---|
| **As written** — 80 for primary 1 over ≥ 4 windows, plus 80 for primary 2 on a disjoint held-out window | **160** | 668 sessions | ≈ 2029-05-10 | ≈ **2029-06-18** | **~21 months past** |
| **Most generous** — primary 2's 80 nights taken as the union of the training windows, "held-out" satisfied by the ≥ 2-window sign clause alone | **80** | 334 sessions | ≈ 2028-01-12 | ≈ **2028-02-21** | **~5.4 months past** |
| Required rate for a lock today (≈ 220 elapsed sessions admissible inside the ceiling after maturity and margin) | — | **0.727/session** as written, **0.364/session** at the most generous reading | — | — | measured today: **≤ 0.2394** |

Dates use the two-step construction every Steward exposure report uses (sessions → calendar at
365/252, then + 20 sessions maturity + a 7-day freeze margin, rounded to the next Monday), from a
window opening 2026-09-15. **Neither reading reaches the ceiling, and the conclusion does not depend
on the rate assumption**: even the most generous reading, on the *upper* bound of an unmeasured joint
rate, on a pooled rate that the monthly series says is stale, misses by five and a half months.

### Limb 2 — the structural blocker: one elite row a night cannot locate a cut to ±3 points

This limb is the reason the entry does not simply name an accrual date, and it is the one a
successor must answer first. The band the PASS condition is stated in is `[87, 93]`, and the
population supplies **1.06 rows above 90 per elite-present night and none at all on the median
contributing night**. On a night carrying exactly one row above 90, every cut `c` between that row's
score and the next score below it induces the **identical** partition of the night, so the objective
function is flat across a wide interval and `c*` is decided by the tie-break rule, not by data.

That is a **density** problem, not a night-count problem, and it survives any amount of waiting: a
night rate of 0.73/session with one elite row per night still cannot distinguish `c = 87` from
`c = 93`. The permutation baseline H-080 names (scores shuffled within night) is the right null and
does not repair it — it would return a very wide null band for the wander of `c*`, against which
almost any observed dispersion is "consistent with noise", so the question would return
**INCONCLUSIVE by construction**. DP-45 forbids registering a design whose only reachable verdict is
the one that says nothing.

Two further hazards a successor must size before drafting, both unmeasured today and neither used to
reach this deferral: the elite rows are plausibly concentrated in a handful of recurring names
(memory / semis — Q003 §10 threat 6), so **DP-51's episode-clustered CI would be computed on very few
symbol-episodes** and is the clause most likely to decide the verdict; and `c*` is an **argmax**, so
its sampling distribution is not the bootstrap of a mean and the successor must state how the
dispersion statistic's CI is formed before it sees one.

### What was considered and rejected before deferring

- **Merging into Q027** (DP-29). Rejected. Q027's band secondary fixes five bands **at lock**, tests
  monotonicity and adjacent-band contrasts, and its blocking clause is an **inversion**, not an
  optimum: it never searches over `c`, never estimates an argmax, never reports that argmax's
  dispersion and never holds a window out. `research/BACKLOG.md`'s own H-010 line already settles
  this — an inversion at the 90 line "routes to H-080 as evidence rather than answering it". Q027
  cannot return a verdict on threshold stability, and its `≥ 90` band clearing 20 nights for
  *reporting* (28.5 projected) is a different and much weaker requirement than four windows of 20
  elite-present nights each.
- **Merging into Q015** (85–90 vs 90+). Rejected, and Q015 says so itself: its `90+` arm was
  **demoted to descriptive at lock and is SUPPRESSED at 14 contributing nights**, and its §1 names a
  properly powered 85–90 vs 90+ contrast as "a separate future question", registrable on the trigger
  reproduced below. H-080 is partly that successor; it inherits the trigger and cannot be answered
  inside Q015.
- **Merging into Q005.** Rejected: Q005 decomposes the elite **count** and reads no outcome column at
  all. It explains why the band is thinning; it cannot say whether the cut is in the right place.
- **Merging into Q031 (H-082) or Q032 (H-079).** Rejected: decay is the level of an edge over time
  and conditionality is the level by tape. Neither locates a boundary, and neither carries a cut
  search or a band contrast as an endpoint.
- **Registering primary 1 alone, dropping the ≥ 90 vs 85–89 contrast.** Rejected: primary 1 is the
  *worse* arithmetic (four cells of 20 elite-present nights) and carries limb 2 in full.
- **Registering on published picks instead of all candidates ≥ 70.** Rejected: strictly worse —
  15 picks on 14 of 48 nights, trending 11 → 4 → 0 by month.
- **Truncating the cut grid to the dense region (searching 70–85, where every band appears on 48 of
  48 nights).** Rejected under DP-25 and DP-45: a search that cannot evaluate `c = 90` cannot say
  whether 90 is optimal, which is the entire hypothesis.
- **Widening the PASS band from ±3 to ±8 points so it spans the populated region.** Rejected under
  DP-25 — the ±3 is the hypothesis's own number, fixed in the backlog entry as "Haci's 'nearby
  range', fixed at lock"; re-uniting it is a new hypothesis, not a registration of this one.
- **Pooling candidate rows across nights instead of aggregating per night.** Rejected outright,
  rule 6. The nights are the n.
- **Using the sealed 2026-06-01..2026-08-12 stretch for the training windows.** Rejected on two
  independent grounds. (a) The band-level outcomes at exactly this boundary have been read: CLAUDE.md
  carries "the 88–90 band underperforms 90+" as a standing finding, and the weekly snapshots of
  2026-09-10 / 09-12 printed the 90+ return series by twelve-week window (BACKLOG H-010). A `c*`
  fitted on those nights is fitted on data whose outcomes are known, which is the exact thing rule 3
  exists to prevent. (b) The 2026-07-08 publication-gate ship moves the common ATR distance from
  ≈ 1.06 to ≈ 2.10 ATR mid-stretch (`STEWARD_Q027_exposure.md` (c)), so a window spanning it measures
  the ship. Every recent F2 question (Q027, Q031, Q032) is prospective-only for the first reason; this
  one has both.
- **DP-13's single automatic extension as a rescue.** Rejected: DP-13 rescues a floor that is
  *marginal* at the decision date. This one is short by 60 to 140 elite-present nights, and no
  extension of the registered length closes it.
- **Registering with the `≥ 90` arm demoted to descriptive** (DP-43's demotion clause). Rejected: that
  clause demotes a secondary arm inside a question whose *primary* clears the floor. Here the `≥ 90`
  arm **is** both primaries — the H-062 and H-041 precedent, verbatim.

### What would move it back into the backlog

Both counts are **measured by the Steward on a then-current freeze over a trailing quarter** — a
quarter, so a single elite-heavy month cannot carry it — and never assumed from a projection. Both
are required; the first alone is not enough, which is the point of limb 2.

1. **Night rate.** Nights carrying ≥ 1 candidate with `overall_score ≥ 90` **and** ≥ 1 candidate in
   `[85, 90)`, per elapsed session, over all 16:05 candidate rows (published or not) on the Q027 §2.5
   contributing-night definition: **≥ 0.73**. Today: **≤ 0.2394** (upper bound; the joint has never
   been measured, and measuring it is the first thing a successor asks for). At **≥ 0.36** only the
   loosest reading of the floors clears, so that level triggers a **re-reading of this entry**, not an
   automatic lock. This is a stricter form of Q015 §1's own trigger (≥ 0.5 elite-contributing nights
   per session over a trailing quarter), and where the two differ this one governs for H-080, because
   H-080 needs four windows and a held-out window where Q015 needed one comparator arm.
2. **Density.** Median **rows per contributing night with `overall_score` in `[87, 93]`**: **≥ 3**.
   Below that a one-point move of the cut inside the PASS band re-partitions no rows on the median
   night and `c*` is a tie-break. Today: 18 rows ≥ 90 across 48 contributing nights, **median night
   0**.

Neither trigger is a date, because neither is an arrival-rate problem the calendar fixes on its own:
the elite band is thinning, not filling. The realistic paths to both counts are a platform change
that widens the candidate universe (**EN-016**, already filed on Q025's evidence — nothing new is
filed here) or a scoring change that restores the upper tail; either would also **split the window**
under DP-06 / DP-50(a), so a successor re-derives its schedule from the ship date, out only.

### Bookkeeping while deferred

**No verdict of any kind was produced.** H-080 returns no PASS, no FAIL, no NULL and no
INCONCLUSIVE; a floor shortfall is not a verdict. **No PREREG was drafted, no directory created, no
question number consumed — Q033 remains free.** No `eval.py` exists, no `results/` directory exists,
and **no outcome of any kind was read**: every count above is a count of candidate rows and nights
from `STEWARD_Q027_exposure.md` (a), (c), (d) and `STEWARD_Q015_exposure.md` (2), (4), (9), both
measured on the pinned freeze with no live query (DP-50(c)).

`research/BACKLOG.md` marks **H-080 — DEFERRED 2026-09-14**, not registered. **F2's correction set is
unchanged at 17** — Q023 (2) + Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) + Q032 (1) — and
H-080's two primaries do not join it while deferred (the H-062 / Q025 precedent). **No cross-question
edit was required and none was made:** Q015, Q027, Q031 and Q032 are untouched, and no Steward request
was routed, so none is held. **No rule-14 exception is involved** (DP-41): every input H-080 would use
is a 16:05 ET candidate field or a pinned bar dated ≤ t.

**One consequence to record, so a later question does not wait on a verdict that will not arrive.**
BACKLOG H-083 (Haci's H13, the A/B/C setup architecture) sequences itself "after H-076 … and H-080
(whether the threshold holds)" and routes H-080's FAIL branch into itself. H-076 is answered by Q028;
**H-080 is not, and H-083 must not be drafted as though a threshold verdict is coming.** It either
states in its own §1 that the threshold question is deferred and unanswered — so its setup-model
contrast stands on its own, against the published v1.6 slate as its baseline says — or it waits for
this entry's triggers. It may not cite a descriptive band read as a substitute.

**Caveat carried forward, so no successor repeats it.** CLAUDE.md's standing finding "the 88–90 band
underperforms 90+" and the weekly snapshots' 90+ return series are **sealed reads at exactly this
boundary**. Any future PREREG on H-080 is **post-hoc with respect to `manifest_v001`** and must be
built on a window whose pick nights postdate those snapshots — prospective-only, the Q027 / Q031 /
Q032 pattern — and must say so in its §6. The exposure counts used above are not subject to that
caveat: they count candidate rows by score band, which is knowledge available at 16:05 ET on the pick
night and contains no outcome. Under this file's preamble **nothing here may be reported, briefed or
quoted.**

---

## Q032 / H-079 — "Does the SAS selection edge exist only in identifiable tape states?" — **§2.2's arm cannot be assigned: the SPY history the partition needs exists in no pinned freeze and cannot be fetched without Alpaca credentials**

**Deferred 2026-09-14 by the registrar, autonomous run (DP-40..48), on this file's first admission
ground: the objective cannot be measured with the artefacts the desk holds.** The blocker is
**provisioning — not procurement, not accrual, not a grant and not the DP-43 ceiling**. It is the
**same blocker, the same pair of environment variables and the same desk session as Q030 / H-074**
(deferred earlier the same day), and this entry **cites that trigger by id rather than restating it**
(see "What would move it back", below). Drafted at
`research/questions/Q032_regime_conditionality/PREREG.md` (state `PREREG_DRAFT` → `DEFERRED`;
**never locked: no `PREREG_LOCKED`, no `schedule.json`** — the Q020 / Q025 / Q030 precedent);
decisions and the governing record at
`research/questions/Q032_regime_conditionality/DECISIONS.md` (decision-maker, 2026-09-14, 16 items +
5 corrections, "## Record — 2026-09-14" and "## Schedule"); the measurement at
`research/reports/STEWARD_Q032_exposure.md` (R1, counts only). **Both files are preserved exactly as
drafted and decided** — nothing in either was edited or deleted for this deferral — and the question
**resumes at `@registrar apply Q032`** when the trigger below is met. **The question number Q032 is
consumed by this entry and is not reused.**

### What the question is, and why it is worth keeping

Haci's H9, *Regime conditionality*. Does SAS's selection edge exist only in identifiable tape
states — does the within-night, control-adjusted L3-touch excess that Q006 measures show up in calm
uptrends and vanish (or invert) everywhere else? One primary, night-level, two-sided: **`G`** =
Q006's `E_t` (each published pick's own printed swing L3, 20 sessions from the session t+1 open,
against the ten nearest same-night unpublished candidates matched on `beta60` / `atr_pct` / `runup20`
with a synthetic target at the identical ATR distance — Q006 §3 verbatim) averaged over **BENIGN**
nights minus the same over **HOSTILE** nights, **MPE ±10.0 pp** (H-079's own number; DP-20's
larger-MPE clause for a difference of differences), `m = 1`.

**Its NULL branch is as consequential as its positive one**, which is why the hypothesis is kept
rather than killed: a NULL retires "it was a difficult tape" as an explanation for weak stretches,
re-labels the weekly's regime panels as composition rather than signal, and replaces the phrase with
a measured HOSTILE-arm band. The design is complete and stands: the bar-only partition, the
`NO_EDGE_TO_CONDITION` / `WORKS_IN_BENIGN` / `HOSTILE_ONLY` clauses, the 80% composition guard, the
three separately-named units (contributing night, tape-episode, symbol-episode), the DP-51 two-CI
gate, C1 as a blocking companion that can confirm nothing. **Nothing about it is unanswerable in
principle — only unassignable.**

### Why it cannot be registered — the failing limb, named exactly

The lock-or-DEFER gate (PREREG §5.3 R1, DECISIONS items 12 and 15) has four limbs: contributing
nights **≥ 0.40** per elapsed session, rarer-arm contributing nights **≥ 0.10**, rarer-arm
gate-counting tape-episodes **≥ 0.025**, **and limb (g) — the SPY-history feasibility probe**.

**The failing limb is (g), and it failed before it could be run: `ALPACA_API_KEY` and
`ALPACA_SECRET_KEY` are both unset in the desk session**, confirmed by a direct presence test in the
Steward's shell and stated rather than inferred (`STEWARD_Q032_exposure.md` §(g); the Q024 R1(d) /
Q030 §(i) precedent). **No SPY retrieval was attempted** — there is nothing to attempt without
credentials, and rule 1 forbids looking for or requesting any other. Under PREREG §5.3 R1(g) / R2(i)
and DECISIONS items 12 and 15, **a failed probe with no pinned alternative is a DEFERRED-at-lock
ground on its own**, independent of every counted limb.

**What the arm needs, exactly.** §2.2's partition is bar-only and therefore immune to a platform
relabelling — that is its whole point — but it is built from SPY's own history: `trend_t` needs
`SMA50_t` **and `SMA200_t`** (UP iff `close > SMA50 > SMA200`, DOWN iff `close < SMA50 < SMA200`,
else MIXED), and `vol_t` is an **expanding-window tercile of SPY's 20-session realised volatility
over every SPY session ≤ t, requiring ≥ 250 such sessions** — below 250 the night is excluded
(§2.2, §2.5). A window opening 2026-09-15 therefore needs **SPY split-adjusted daily bars from
2025-01-02**, which is exactly what R2(i) was sized to deliver and what limb (g) exists to probe.

**The blocker is confirmed a second time, from the opposite direction, by the counts themselves.**
Under the **literal §2.2 rule** the contributing-night rate in this freeze is **0/71 in all three
forms**: `manifest_prices_v001` holds **153** SPY daily bars (2026-02-02..2026-09-10) and the
expanding count of computable rvol20 observations reaches only **133** at the freeze's last date, so
the first session with ≥ 250 prior SPY sessions is **never** — not in this freeze and not in any
freeze the desk holds (`STEWARD_Q032_exposure.md` §(a), §(c); the freeze would have to reach roughly
117 sessions further back, to about mid-2025). **That is not evidence against H-079 and not a
screening failure**; it is the same missing SPY history, measured from inside the data instead of at
the credential. `SMA200` likewise exists nowhere in the freeze, which is why the Steward's
composition table is a **six-cell** proxy where §2.2 registers nine (§(c)), and why it cannot revise
the §4.3 suppression list in either direction.

### The counted limbs, recorded for the re-check and for nothing else

Limbs (a)–(f) were measured because R1 asks for them unconditionally. **Every count below is on the
SMA50-only one-sided bound, which is explicitly *not* §2.2-legal** (DECISIONS item 12), so none of it
is exposure evidence for the registered question. The Steward re-solved the thresholds from the
trading calendar as Correction 3 requires and got **0.39 / 0.097 / 0.0243** against the file's
rounded-up **0.40 / 0.10 / 0.025**; the file's numbers are the stricter and are the ones read here,
and every limb clears or fails identically on both.

| limb | floor (re-solved / as filed) | measured, SMA50-only proxy | strict §2.2 | read |
|---|---:|---:|---:|---|
| (a) contributing nights / elapsed session | 0.39 / **0.40** | **0.6620** (item 3's cap binds: min(0.8710, 0.6620)) | **0.0000** | proxy clears; strict short |
| (b) rarer-arm (HOSTILE) contributing nights / session | 0.097 / **0.10** | **0.3099** (22 of 68 nights HOSTILE) | **0.0000** | proxy clears; strict short |
| (b) rarer-arm gate-counting tape-episodes / session | 0.0243 / **0.025** | **0.0563** unmatured · **0.0141** t+40-matured | **0.0000** | proxy clears unmatured; **short on the t+40-matured basis** |
| (g) SPY-history feasibility probe | must succeed | — | — | **FAIL — credentials absent, probe not attempted** |

Three readings are recorded so a re-attempt does not rediscover them, and **none of them changes the
branch**: (1) the episode limb is **short on the t+40-matured basis** that DECISIONS item 2 requires,
but that is freeze-horizon censoring — no night after 2026-07-15 can reach t+40 inside
`manifest_prices_v001` — and it is a measurement the re-check must make again on a freeze carrying
t+40 bars, not exposure evidence; (2) the rarer arm is **much richer than §5.1's 0.20 placeholder**
(0.3099 measured against ≈ 0.132 assumed), so **floor A, not floor B, would bind** — recorded, and
**no schedule is built on it**, because item 14's method is re-run from scratch on a re-attempt and
never inherited; (3) **C1 carries more independent information than §10 threat 2 assumed** —
night-level agreement between the proxy arm and the legal platform label is **49/63 = 77.8%** with
the HOSTILE nights split exactly 11 STRONG / 11 NOTSTRONG, and §2.3 legality fails on 5 of 68 nights,
all on the `created_at` timestamp test (§(d)) — and item 1's disposition of C1 (blocking companion,
corrected jointly with Q023's E1, confirming nothing) is **not** promoted on the strength of it.

**Nothing else measured moves anything.** §(e) **confirms** the control-pool depth (min 37 / median
53 / max 60; **0** nights below 3) and the CTRA truncated-history signature (last bar 2026-05-06, 19
in-window appearances, the 5 pre-2026-08-12 ones matching Q027 exactly) — a confirmation, not a
correction, so **no DP-50(a) finding**. §(f) returns **NONE**: HEAD unchanged at `d19c9a9`, no commit
since `fa70688` touches the scoring path, the lane-plan writer or `services/market_regime/scorer.py`,
and **no v1.7 promotion is scheduled** — an absence of a schedule, to be re-checked at every future
freeze, never a permanent clearance. The `publication_floor` (2026-07-08) and
`bear_publish_threshold` (2026-06-29) config dates are already in `DATA_NOTES.md` and gate
publication, not scoring (item 9) — **no new `DATA_NOTES.md` entry is owed**.

### What was considered and rejected before deferring

- **Re-specifying the partition to SMA50-only** — the one move that would let Q032 lock today, on a
  split the desk has already measured. **Rejected, and it may never be made inside this question**
  (PREREG §5.3 R2(i), DECISIONS item 12): that is a different arm, chosen *after* the data existed
  and after its counts were seen, which is the exact thing rule 3 and DP-45 exist to stop. A
  SMA50-only partition is **a different question with its own id, its own MPE and its own §10**;
  Q032's file is not edited into it.
- **Locking now and probing at the decision pass.** Rejected in advance — that is what item 12's
  added limb exists to prevent. Discovering the missing history in June 2027 would have cost the
  whole window; discovering it today cost one afternoon.
- **Waiting under DP-13's single automatic extension.** Rejected. DP-13 rescues a floor that is
  *marginal at a decision date*; this question has no decision date, and waiting 30 sessions produces
  no SPY bars.
- **Deferring on DP-43's 12-month ceiling instead.** Rejected as a mis-filing: the proxy rates sit
  comfortably inside the ceiling, and the deferral would stand even if they were faster still. The
  ground is the first, not the second.
- **Merging into Q023** (DP-29). Rejected, and it is the tempting one, because Q023's locked E1 *is*
  the platform-label contrast this question carries as C1. Q023 runs it on the 80–90 band under the
  *other* regime definition; Q032's primary is the bar-only partition on the whole published slate,
  and item 1 registers C1 as a blocking companion corrected jointly with Q023's E1 precisely so the
  desk does not get a second bite at a locked question's statistic.
- **Merging into Q031** (H-082, decay). Rejected: decay is the level of an edge over time,
  conditionality is the level by tape. Q031 §8 clause 7 routes its `TAPE_COMPOSITION` case **to this
  question**, which it cannot do if this question is the same one.

### What would move it back into the backlog — the trigger is a measurement, not a date

**The H-074 trigger, cited by id and shared verbatim with Q030** (`DEFERRED.md`, "Q030 / H-074",
2026-09-14): **`ALPACA_API_KEY` and `ALPACA_SECRET_KEY` present in a desk session, stated by the
Steward with a direct presence test, AND a market-data coverage probe that returns the bars** — for
Q032 that probe is **SPY split-adjusted daily bars from 2025-01-02**, coverage and first/last bar
date only, feed `sip`, no values beyond that, market-data endpoints only. **Both limbs, measured,
never assumed:** credentials present but SPY history unretrievable is the same deferral. Q032's probe
is a strict sub-case of the freeze Q030 cannot build, so **satisfying that one trigger re-opens both
questions, in registration order** — Q030 first. **No calendar re-check date is named**, because no
amount of waiting produces the bars. Provisioning two environment variables the desk is already
licensed to use is **Haci's call**; it is neither a purchase nor a platform change, no
`IMPLEMENTATION_BRIEF.md` follows, and **DP-49 is not engaged**.

**What a re-attempt must re-measure before it may lock — six things, none of them inherited from the
record above:**

1. **Limb (a)** — the §2.5 / §2.6 contributing-night rate on a freeze carrying **t+40** bars, with
   numerator and denominator counted over the **same** period and item 3's cap applied.
2. **Limb (b)** — the §2.2 arm split on the **true** `close > SMA50 > SMA200` trend and the **true
   ≥ 250-session** volatility tercile. The SMA50-only proxy recorded above is a one-sided bound
   (HOSTILE lower, BENIGN upper) and is **never** the registered partition.
3. **The rarer-arm gate-counting tape-episode rate on the t+40-matured basis** — the limb that read
   **0.0141 < 0.0243** here, and the one this freeze could not measure honestly.
4. **The nine-cell `trend_t` × `vol_t` composition** (only six cells were observable here, because
   `SMA200` exists nowhere in the freeze) and, with it, item 7's **single permitted suppression
   revision — cells added only, never removed**.
5. **Limb (f)'s DP-50(a)/(b) commit sweep and the v1.7 schedule check**, re-run on the new freeze:
   today's "NONE" is an absence of a schedule, not a permanent clearance.
6. **Correction 3's three inequalities, re-solved from the trading calendar** against DP-43's
   12-month ceiling **measured from the new lock date** — they tighten as that date moves later.

**What does not change on re-entry.** **The partition is never re-specified to SMA50-only** (PREREG
§5.3 R2(i), DECISIONS item 12) — stated twice in this entry because it is the one shortcut the
measured proxy makes attractive. DECISIONS items 1–11 bind as written; items 13 and 14's **method**
binds and their **dates do not** — item 13's prospective-only window start applies to the new lock
commit, item 14's "window end = the latest of floors A, B, C, D at the measured rates; decision date
= window end + 40 sessions + one calendar week, first Monday on or after" is re-run from scratch, and
**every date may move out only** (DP-43, DP-45; the Q020 / Q025 / Q030 precedent). Q032's R2 rider is
**withdrawn and HELD**: the SPY-from-2025-01-02 history (i) and the t+40 bar horizon (ii) are not
built while the question is deferred, and **Q027's and Q031's own successor-freeze requests and pins
are unaffected and are not edited** (rule 3, DP-22).

### Bookkeeping while deferred

**No verdict of any kind was produced.** Q032 returns **no CONFIRMED, no NULL, no INCONCLUSIVE, no
`G` and no C1 number**; a gate shortfall is not a verdict (DECISIONS item 6, item 14 of the Q025
precedent). **No `eval.py` was written and no `results/` directory exists**, and **no outcome of any
kind was read** for this question at any point — no touch, no first-touch date, no return, no
excursion, no `outcome_*` column, no `sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`
and no arm-versus-outcome cross-tab of any shape; the Steward's report is counts of nights, picks,
controls and bars on the pinned freeze with **no live query** (DP-50(c)), reading a forward bar only
to establish that a bar exists. **Item 7's suppression list is not revised** (the one permitted
revision runs on a locked question) and **item 6 is not exercised** (there is no lock at which to
demote an arm).

`research/BACKLOG.md` marks **H-079 — DEFERRED (Q032 drafted; SPY-from-2025-01-02 history needs
Alpaca credentials in the desk session)**, not registered. **Q032's one primary (`G`) leaves the
`F2` correction set while deferred** (the H-062 / Q025 precedent): **F2 falls from 17 to 16** —
Q023 (2) + Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) — and **`G` leaves the `F1`
companion set, which falls from 28 to 27** (Q006 2 + Q024 6 + Q025 2 + Q029 16 + Q031's `D1ᴮ` 1),
exactly Q031 DECISIONS #14's figure. **No locked PREREG records Q032 in its correction set, so no
locked file is edited and none was**; the two unlocked drafts that counted `G` — Q033's §7 (F1 29 →
28, F2 18 → 17) — are corrected, and Q034 registers no primary and no BH set, so nothing there
changes. **C1 is withdrawn as a blocking companion to Q023's E1; Q023 is unaffected and is not
edited.** The `research/BOARD.md` line moves with this entry.

**Caveat carried forward, so no successor repeats it.** The sealed 2026-06-01..2026-08-12 stretch has
been read for this hypothesis — the weekly snapshots of 2026-09-10 and 2026-09-12 printed
regime-stratified cells, and they are what put H-079 on the backlog — so any future PREREG on this
hypothesis is **post-hoc with respect to `manifest_v001`** and must run **prospective-only**, with
the sealed stretch as a labelled panel split at 2026-07-06, exactly as the draft registers it. The
exposure counts used above are not subject to that caveat: they count nights, picks and bars, which
is knowledge available at 16:05 ET on the pick night and contains no outcome. **That binds the proxy
counts in this entry as firmly as anything else — they are planning numbers on a partition that was
never legally assignable.** Under this file's preamble **nothing here may be reported, briefed or
quoted** until the trigger is met.

---

## H-078 — "Founder vs Robot vs Dumb: can the edge actually be harvested?" (Haci's H8) — **two data blockers: the desk holds no record of Haci's fills, and no cost model in money units**

**Deferred 2026-09-14 by the registrar, autonomous run (DP-40..48), under DP-47** ("new data needed"
hypotheses go straight to this file with the data named) **and this file's first admission ground:
the objective cannot be measured with the artefacts the desk holds.** The blocker is **procurement
and elicitation, not accrual, not a rule-14 grant and not the DP-43 ceiling** — no amount of waiting
produces either missing artefact. **Nothing was drafted:** no PREREG, no directory, no `eval.py`, no
`results/`, **no question number consumed** (Q036 stays free). The hypothesis resumes as a new
registration, in queue order, when the trigger below is met.

### What the question is, and why it is worth keeping

Haci's H8. Every other question on this desk measures whether the *prediction* is good. This one
measures whether the prediction becomes **money in a real account after costs** — the gap the desk
has never closed. Three arms on the same pick nights:

- **ROBOT** — mechanical execution of the platform's committed plan: session t+1 open entry, SELECT
  scale-out `[0, 15, 30, 15, 25, 15]` on the flattened L1–L6 ladder
  (`volatilx services/sas_conviction_card.py:203-218`), no stop (DP-02), result in ATR per trade
  (DP-10), **after costs**.
- **DUMB** — the identical plan run on Q024's benchmark arms and on Q006's distance-matched control,
  also after costs.
- **FOUNDER** — Haci's realised trades on the same names, from his own fills.

PASS = the robot beats the dumb arms after costs and risk, and the founder comparison becomes a
diagnostic (does discretion add or subtract?). FAIL = the robot does not clear the dumb arms once
costs are paid, which would mean prediction quality is not becoming realisable returns — the single
most consequential NULL available to this desk, and the reason the hypothesis is kept rather than
killed. The mechanism for FAIL is concrete and already half-measured elsewhere: a target-touch edge
can be eaten by entry slippage on a gapping open (Q004's L1-already-passed rate) and by six legs of
scale-out commission on a move of roughly one ATR.

### What is already covered, and is therefore not what this entry defers (DP-29)

**The before-costs half of ROBOT vs DUMB is already locked and must not be registered twice.**
Q024's **clause-7 money gate** is exactly that contrast — the platform's committed SELECT scale-out,
truncated to a 20-session budget, in ATR per trade, SAS minus each benchmark arm
(`research/questions/Q024_sas_vs_simple_benchmarks/PREREG.md` §4, clause 7; decides 2027-05-17,
hard stop 2027-06-28) — and Q006's `E1`/`E2` are the same comparison expressed as a control-adjusted
touch rate (decides 2026-10-05). **Neither carries a cost line.** What H-078 adds, and all it adds,
is (i) the **cost line** and (ii) the **FOUNDER arm**. Both are blocked below.

### Blocker 1 — the FOUNDER arm: the desk holds no record of any fill Haci has ever made

`playbook/` contains a single `README.md` and no trade data of any kind. No platform table records
the founder's executions: `whale_watch_ledger` is empty (0 rows, `manifest_v001`), and no other
frozen table carries an account, an order or a fill. **The Alpaca trading API is out of scope under
rule 1** — the desk's credentials are market-data credentials, and the desk may not look for,
request or use any other, so "pull his fills from the broker" is not available to the desk at any
price. The arm has no proxy: reconstructing what Haci "probably" did from the printed lane plan is
precisely the ROBOT arm, so a proxy FOUNDER arm would be a tautology dressed as a comparison.

**Exactly what the desk needs, in the form it needs it.** One immutable export, **one row per
fill**, covering every fill in the study window — not only the ones on published picks (a file
filtered to picks conditions the arm on hindsight, and the desk cannot un-condition it afterwards):

| field | form | why it is required |
|---|---|---|
| `fill_timestamp` | ISO-8601 with timezone offset, to the second | entry basis (DP-03/DP-11) and knowledge time (rule 14) both need the clock, not the date |
| `symbol` | underlying ticker | the join to the pick night |
| `asset_class` | `equity` or `option` | the two cannot share a P&L column |
| `occ_symbol` | OCC 21-char contract symbol, blank for equity | option legs are uninterpretable without expiry/strike/right |
| `side` | `buy` / `sell` | — |
| `position_effect` | `open` / `close`, blank for equity | a close at a target touch is the whole execution claim |
| `quantity` | signed integer, shares or contracts | — |
| `fill_price` | decimal, per share or per contract | — |
| `commission`, `fees` | decimal per fill, actual not modelled | this is half of blocker 2, measured instead of assumed |
| `order_id`, `fill_id` | broker ids | de-duplication across partial fills |

Format: **CSV, UTF-8, header row, one file per export**, dropped at
`playbook/trades/fills_<from>_<to>.csv` or its location named in `research/INBOX.md`. Source: **Haci
only** — his broker's own trade-confirmation or activities export, downloaded by him, **not retyped
by hand** (a retyped file cannot be pinned honestly). The Data Steward pins it with a sha256 in a
manifest before any read, the DP-50(c) rule applying to it exactly as to a parquet.

**A second, unmeasurable gate rides on the same file.** Rule 6's floors are 20 contributing nights
per cell and 80 per primary (DP-21). One discretionary trader's fills may well not reach them, and
**the desk cannot know whether they do until the file exists** — so the re-entry check below is two
measurements, not one, and a FOUNDER arm that arrives below the floor is registered **descriptive at
lock** (DP-43), never promoted to make the number look complete.

### Blocker 2 — the cost line: a money-unit MPE the desk may not invent (DP-44, R-4)

The ROBOT-after-costs and DUMB-after-costs arms do not need the founder's file. They need a **cost
model in money units** — per-share or per-contract commission, the half-spread paid at a market
open, and a slippage assumption for a scale-out leg filled on a target touch — and under **DP-44**
those are Haci's costs: *"No money-unit MPE is invented — a hypothesis that needs one is DEFERRED
with the question stated."* The BACKLOG line as written contemplated a conservative default under
DP-40; **DP-44 is the more specific rule and DP-45 takes the stricter of two readings**, so the desk
does not default here, and this entry records the correction rather than acting on it.

**The question stated, so it can be answered in one line each:**

1. **Commission** — per equity share and per option contract, per leg, at his broker, including any
   per-order or assignment fee. (A number, or "zero, my broker is commission-free on equities".)
2. **Spread paid at entry** — what he assumes he gives up entering at the t+1 open: half the quoted
   spread, a fixed cents-per-share figure, or a basis-point figure.
3. **Slippage on a scale-out leg** — a target-touch sell is a resting limit for him or a market
   order? If limit, the arm may assume a fill at the level; if market, the desk needs the give-up.
4. **The gate.** Once (1)–(3) exist, the after-costs verdict still needs an MPE. The desk's standing
   answer is DP-10's **0.25 ATR per trade** applied to the *after-costs* contrast — that is a
   translation of an existing DP, not a new money MPE, and is what the successor will use unless he
   says otherwise. Haci's own "+0.10R" from the Master Hypothesis Program is **not** carried: with no
   stop assumed (DP-02) R has no denominator.

Answers to (1)–(3) become a DP entry (R-4: "once he sets one for a metric type it becomes a DP entry
and is not asked again") and unblock **every** future after-costs question, not only this one.

### What was considered and rejected before deferring

- **Registering ROBOT-after-costs now with a desk-chosen cost default**, as the BACKLOG line
  envisaged. Rejected under DP-44 and DP-45: a cost assumption is the *only* thing standing between
  a PASS and a FAIL on a contrast whose before-costs half is already locked in Q024, so inventing it
  would let the desk choose the verdict. One line from Haci removes the problem permanently.
- **Registering the FOUNDER arm on a reconstructed proxy** (assume he bought the elite picks after
  hours per TI-001 and sold at each printed level). Rejected: that *is* the ROBOT arm with a
  different label, and the comparison would measure nothing.
- **Merging the whole hypothesis into Q024** (DP-29). Rejected as a partial-merge only: Q024's
  clause-7 gate is the before-costs half and is recorded above as covered, but Q024 is locked
  (rule 3) and cannot acquire a cost line or a founder arm; a locked file is never edited to absorb
  a new arm.
- **Merging into Q006.** Rejected: Q006's endpoints are control-adjusted touch rates with no plan
  P&L at all.
- **Deferring under DP-43's 12-month ceiling.** Rejected as a mis-filing: the blocker is not
  exposure. The ROBOT/DUMB arms sit on nights Q024 is already accruing; they would clear a floor
  long before they clear a cost model.
- **Waiting under DP-13's single automatic extension.** Rejected: DP-13 rescues a floor marginal at
  a decision date. There is no decision date here, and thirty more sessions produce neither a fills
  export nor a commission schedule.

### What would move it back into the backlog — two triggers, both measurements, neither a date

**Trigger A (unblocks ROBOT-after-costs and DUMB-after-costs, the two arms that need no founder
data):** Haci answers cost questions (1)–(3) above, in `research/INBOX.md` or on the board. The
Decision-maker records them as a **new DP entry** (R-4), and the hypothesis re-enters the queue as
an **F6 successor registered after Q006 decides (2026-10-05)**, so that the control contrast it
builds on has a ledgered verdict. Its window is **prospective-only from its own lock commit**
(Q024's own §1 precedent — the sealed period's absolute SAS returns have already been printed in the
weeklies, so a benchmark arm is not blind on those nights), and it inherits Q024's clause-7 plan
definition **verbatim**, cost line added, so the two are comparable.

**Trigger B (unblocks the FOUNDER arm):** the fills CSV above **present** under `playbook/trades/`
or named in `INBOX.md`, **and** the Steward's sha256 pin of it, **and** a measured count of
contributing nights — nights on which at least one fill joins to a published pick — against the
rule-6 floors. **All three limbs, measured, never assumed:** a file that exists but supplies 11
contributing nights re-enters as a descriptive panel of a Trigger-A question, not as a primary.

**Order.** Trigger A alone is enough to register the after-costs question; Trigger B alone is not
enough to register anything, because the founder arm is only interpretable beside a costed robot.
If both are met, one question carries three arms as H-078 proposed.

**No `IMPLEMENTATION_BRIEF.md` follows from this entry, and DP-49 is not engaged**: nothing here
asks for a platform change or a database step. Trigger A is one message from Haci; Trigger B is a
file he exports from his own broker.

### Bookkeeping while deferred

**No verdict of any kind was produced, and no outcome was read** — no touch, no first-touch date, no
return, no excursion, no `outcome_*` column, no `sas_selection_excursion`, no P&L of any shape, for
any arm; **no live query was made** (DP-50(c)) and no freeze was requested. **H-078 was never
registered, so no correction set changes**: F6 is unchanged, no locked PREREG names an H-078
endpoint, and no locked file is edited (rule 3, DP-22). `research/BACKLOG.md` marks
**`[x] H-078 — DEFERRED`** with this entry cited. The `research/BOARD.md` line moves with this
entry. **Q024's and Q006's own schedules, pins and correction sets are unaffected and are not
edited.**

**Caveat carried forward, so no successor repeats it.** A founder-fills file is, by construction,
**a record of decisions made with knowledge of outcomes the desk is blind to** — he saw the tape as
he traded it. It may therefore be used only as the **FOUNDER arm's own realised result**, never as a
feature, a filter or a label on any other question (rule 14: it does not exist at 16:05 ET on the
pick night). Under this file's preamble **nothing here may be reported, briefed or quoted** until
the triggers are met.
