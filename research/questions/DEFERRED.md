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


> **TRIGGER MET 2026-09-14 — this deferral is lifted; the entry is kept as the record of why it was made.**
> Both limbs were measured in a desk session, never inferred. **(1) Credentials present:** `ALPACA_API_KEY`
> and `ALPACA_SECRET_KEY` are both present, asserted by a direct presence test (`research/lib/desk_env.py`,
> which returns names and never values); they were always in `.env.research` and always loaded for headless
> runs by `scripts/research_routines.sh:13` — the interactive session that measured the deferral simply had
> not loaded them, so the blocker was **provisioning of one session**, not procurement.
> **(2) Coverage 97.55%** against the ≥ 90% gate: **2,346 of 2,405** blob symbols returned ≥ 60 daily bars
> over 2026-06-01..2026-09-11 (`feed=sip`, `adjustment=split`); 59 short or absent, named in the report.
> The blob re-verified at **2,405** entries and sha256 `c4d12610…0201` against the **committed** bytes of
> `4171b1a` — a Windows checkout rewrites LF to CRLF, so the working-tree copy hashes differently and must
> never be hashed in its place. Measurement: `research/reports/STEWARD_Q030_universe_coverage_probe.md`.
> **What happens next, in the order this entry already fixed:** R2(iii) builds and pins
> `manifest_prices_universe_vNNN`; R2(iv)'s counts-only dry run fixes the suppression list; Q030 re-enters
> the queue at the front and `@registrar apply Q030` folds DECISIONS.md items 1–13 and Corrections 1–7 into
> the PREREG before any lock. **§5.2's schedule is re-derived from the actual lock date, out only** (DP-43,
> DP-45): the 2027-04-12 decision date and every date beside it were the arithmetic at a 2026-09-14 lock and
> are not carried forward. The rate limb is not re-measured; 0.6761 is re-tested only as an inequality
> against the gate re-solved from the new lock date (Correction 3).
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


> **TRIGGER MET 2026-09-14 — this deferral is lifted; the entry is kept as the record of why it was made.**
> Limb **(g)**, the only failing limb, was attempted for the first time and **passes**: SPY returns **424**
> split-adjusted daily bars for 2025-01-02..2026-09-11, against the **≥ 250** prior SPY sessions `vol_t`'s
> expanding-window tercile needs and the 200 `trend_t`'s mean needs — so the arm is assignable from the
> first session of the window, and the "first session with ≥ 250 prior SPY sessions is never" finding is
> superseded (it described `manifest_prices_v001`'s 153 bars, not what the vendor supplies). Credentials
> were present all along in `.env.research` and loaded for every headless run by
> `scripts/research_routines.sh:13`; the measuring session had not loaded them. Limbs (a)–(f) cleared on
> 2026-09-14 and are not re-measured. Measurement: `research/reports/STEWARD_Q032_spy_history_probe.md`.
> **Next:** R2(i) pins the SPY history into a freeze, then Q032 re-enters the queue and resumes at
> `@registrar apply Q032` with its DECISIONS.md binding in full. The drafted schedule is re-derived from the
> actual lock date, **out only** (DP-43, DP-45).
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

---

## Q033 / H-081 — `V = G_μ − G_α`, the interaction endpoint (P2 only) — **the tape arm cannot be assigned: the SPY history the partition needs exists in no pinned freeze and cannot be fetched without Alpaca credentials**


> **TRIGGER MET 2026-09-14 — this deferral is lifted; the entry is kept as the record of why it was made.**
> P2's tape arm shares Q032's limb (g) verbatim, and that limb now **passes**: SPY returns **424**
> split-adjusted daily bars for 2025-01-02..2026-09-11 against the ≥ 250 required
> (`research/reports/STEWARD_Q032_spy_history_probe.md`). **Q033's P1 is locked and pinned and is not
> touched by this** — P2 rejoins as a second primary only at a successor PREREG or by the route its own
> entry names, never by editing the locked Q033 PREREG (DP-22).
**Deferred 2026-09-14 by the registrar, autonomous run (DP-40..48), on this file's first admission
ground: the objective cannot be measured with the artefacts the desk holds.** This is an
**endpoint-level deferral, not a question-level one** — the H-067 / Q024 precedent.
`research/questions/Q033_direction_vs_magnitude/PREREG.md` **locks with P1 (`A`, the direction
excess) alone**, `state.json` goes to `PREREG_LOCKED` (not `DEFERRED`), `schedule.json` is written,
and **no question number is consumed**. Decisions and the governing record:
`research/questions/Q033_direction_vs_magnitude/DECISIONS.md` (decision-maker, 2026-09-14, 33 items +
22 corrections, "## Record — 2026-09-14", items 16, 22, 23, 30, 33); the measurement:
`research/reports/STEWARD_Q033_exposure.md` (R1, counts only). The blocker is **provisioning — not
procurement, not accrual, not a grant and not the DP-43 ceiling** — and it is the **same blocker, the
same two environment variables and the same desk session as Q030 / H-074 and Q032 / H-079**, its
third firing in one day.

### What the endpoint is, and why it is worth keeping

**It is the half of H-081 that Haci's own line is about.** `V = G_μ − G_α`, where
`G_x = mean_{BENIGN} x_t − mean_{HOSTILE} x_t`: the tape-arm contrast of the control-adjusted
**magnitude** excess (first touch of the pick's own printed swing L3 within 20 sessions of the t+1
open — Q006 `Delta_t` on the DP-09 clock) minus the same contrast of the **direction** excess (the
±0.5 ATR own-side-first race). H-081's PASS predicts `V > 0`: *target attainment is the
tape-conditional part of the claim and direction is not*. Two-sided, night-level, **MPE ±10.0 pp**
(DP-20's larger-MPE clause: `V` is one difference further than a difference of differences, and at
~100 nights a 5 pp bar on a triple difference returns INCONCLUSIVE by construction rather than by
evidence).

**Everything designed for it stands and is recorded as designed**, so a successor inherits rather
than re-argues: the bar-only partition (§2.2, identical to Q032's), the ±0.5 ATR band, the ±10.0 pp
MPE, the **equivalence NULL clause** (NULL requires the point estimate inside ±MPE **and both CIs
entirely inside ±MPE**), the DP-51 two-CI gate, the 80% HOSTILE composition guard, the level clauses
`NO_EXCESS_TO_COMPARE` / `MAGNITUDE_IS_THE_CONDITIONAL_ONE` / `BOTH_CONDITIONAL` /
`BOTH_MOVE_TOGETHER`, the four arm × half stability cells, the tape-episode block bootstrap and the
tape-episode label permutation. **P1 does not depend on any of it** — "do published picks go their
own way more often than their look-alikes?" needs no regime label at all — which is why the question
locks rather than defers.

### Why it cannot be measured — the failing limb, named exactly

PREREG §5.3 R1 gained **limb (f)** at `decide` (DECISIONS item 16) precisely so this would be
discovered at the lock and not at the 2027 decision pass: a presence test for
`ALPACA_API_KEY` / `ALPACA_SECRET_KEY` in the desk session and a coverage probe for SPY
split-adjusted daily bars from **2025-01-02**.

**Limb (f) FAILED: both variables are unset in the desk session, stated by a direct presence test and
never inferred, and no retrieval was attempted** — there is nothing to attempt without credentials,
and rule 1 forbids looking for or requesting any other (`STEWARD_Q033_exposure.md` §(f); the Q024
R1(d) / Q030 §(i) / Q032 §(g) precedent). Under DECISIONS item 16's registered branch, a failed probe
with no pinned alternative **defers P2 at the lock and lets P1 lock alone**.

**What the arm needs, exactly.** `trend_t` needs `SMA50_t` **and `SMA200_t`** (UP iff
`close > SMA50 > SMA200`), and `vol_t` is an **expanding-window tercile of SPY's 20-session realised
volatility over every SPY session ≤ t, requiring ≥ 250 such sessions**. A window opening 2026-09-15
therefore needs SPY split-adjusted daily bars from **2025-01-02**. `manifest_prices_v001` holds
**153** SPY bars (2026-02-02..2026-09-10) and reaches only **133** computable rvol20 observations, so
the first session with ≥ 250 prior SPY sessions is **never** — not in this freeze and not in any
freeze the desk holds. The same absence, measured from inside the data instead of at the credential.

### The second, independent ground — the rarer-arm episode supply

**PREREG §8 clause 2's gate (≥ 5 gate-counting tape-episodes per arm) is not shown to be reachable,
at the reading that governs.** DECISIONS item 23 settles which reading that is: the **strict
full-window t+40-matured** one, **1 episode / 71 elapsed sessions = 0.0141 against a floor of
0.025 — SHORT**. The Steward's two looser readings are recorded and **neither is adopted**:
**0.0323** (sub-period-restricted) and **0.0563** (eligible-pick basis). Where two readings of one
count differ only in how easily a floor is reached, the desk takes the one that does not reach it
(DP-45) — and DECISIONS item 6's censoring-removal licence was written for limb (a)'s **rate**, whose
denominator a successor freeze can guarantee, not for an **episode count**, whose supply no freeze
can. **`V` therefore carries two independent deferral grounds, and both must be re-measured before
any successor may lock.**

### The counted limbs, recorded for the re-check and for nothing else

Every count below is on the **SMA50-only one-sided bound**, which is explicitly **not** §2.2-legal
(HOSTILE is a lower bound, BENIGN an upper bound, because adding `SMA50 > SMA200` can only move
nights out of `UP`). None of it is exposure evidence for the registered partition, and **none of it
sizes anything in the locked Q033**:

| limb | floor (as filed) | measured, SMA50-only proxy | strict §2.2 | read |
|---|---:|---:|---:|---|
| (a) contributing nights / elapsed session (**P1's limb**) | 0.40 | **0.6620** (item 6's cap binds: `min(0.8710, 0.6620)`) | — | **PASS — gates P1, which locks** |
| (b) rarer-arm (HOSTILE) contributing nights / session | 0.10 | **0.3099** (22 of 68 nights) | 0.0000 | proxy only; travels with `V` |
| (b) rarer-arm gate-counting tape-episodes / session | 0.025 | 0.0563 unmatured · **0.0141 t+40-matured** | 0.0000 | **SHORT at the governing reading** |
| (c) composition | — | **six-cell** proxy where §2.2 registers **nine**; first session with ≥ 250 prior SPY sessions = **never** (153 bars, 133 rvol20) | — | cannot revise the suppression list in either direction |
| (f) SPY-history feasibility probe | must succeed | — | — | **FAIL — credentials absent, probe not attempted** |

The Steward's informational note that the proxy HOSTILE arm is much richer than the draft's 0.20
placeholder (0.42 / 0.31 / 0.18 by month) would have moved the binding floor from B to A and pulled a
decision date ~5 weeks in. **It is not taken and no schedule was built on it** (DP-43, DP-45): it is a
bounded proxy for a partition nobody can assign.

### What was considered and rejected before deferring

- **Re-specifying the partition to SMA50-only** — the one move that would let `V` be measured today,
  on a split the desk has already counted. **Rejected, and it may never be made inside Q033 or any
  successor edit of it** (PREREG §5.3 R2(i), DECISIONS items 16, 22): that is a different arm, chosen
  *after* the data existed and after its counts were seen, which is the exact thing rule 3 and DP-45
  exist to stop. A SMA50-only partition is **a different question with its own id, its own MPE and its
  own §10**. Stated twice here for the same reason Q032's entry states it twice: the measured proxy
  makes it tempting.
- **Deferring Q033 whole.** Rejected: P1's own gate limb clears with 65% headroom (0.6620 against
  0.40) and P1 is a pooled level that needs no arm. Deferring an answerable question because an
  unanswerable endpoint sits beside it deletes answerable questions.
- **Locking P2 and probing at the decision pass.** Rejected in advance — that is what limb (f) exists
  to prevent. Discovering this in July 2027 would have cost the whole window; discovering it at the
  lock cost an afternoon.
- **DP-13's single automatic extension.** Rejected: it rescues a floor that is *marginal at a decision
  date*, and thirty more sessions produce neither SPY bars nor a credential.
- **Deferring on DP-43's ceiling instead.** Rejected as a mis-filing: the proxy rates sit comfortably
  inside the ceiling. The ground is the first, not the second.
- **Merging into Q023 or Q031.** Rejected on the same grounds Q032's entry gives: Q023 runs the
  platform-label contrast on the 80–90 band, and decay in time is not conditionality on the tape.

### What would move it back into the backlog — the trigger is a measurement, not a date

**The H-074 trigger, cited by id and shared verbatim with Q030 and Q032** (`DEFERRED.md`,
"Q030 / H-074", 2026-09-14): **both `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` present in a desk
session, stated by the Steward with a direct presence test, AND a market-data coverage probe that
returns the bars** — here **SPY split-adjusted daily bars from 2025-01-02**, feed `sip`, coverage and
first / last bar date only, market-data endpoints only. **Both limbs, measured, never assumed:**
credentials present but SPY history unretrievable is the same deferral. **No calendar re-check date is
named, because no amount of waiting produces the bars.** Satisfying that one trigger re-opens Q030,
Q032's successor and this endpoint **in registration order**. Provisioning two environment variables
the desk is already licensed to use is **Haci's call**; it is neither a purchase nor a platform
change, no `IMPLEMENTATION_BRIEF.md` follows, and **DP-49 is not engaged**.

**What a successor must re-measure before it may lock — seven things, none inherited from the record
above:**

1. **The §2.2 split on the true `close > SMA50 > SMA200` trend and the true ≥ 250-session volatility
   tercile.** The SMA50-only proxy is a one-sided bound and is never the registered partition.
2. **The arm-bearing contributing-night rate** under §2.5's **complete** rule (≥ 3 valid published
   picks, each with ≥ 5 valid matched controls, matured to t+40, carrying a legal arm label).
3. **The rarer-arm contributing-night rate** (floor B).
4. **The rarer-arm gate-counting tape-episode rate on a t+40-matured basis** (floor D) — the limb that
   read 0.0141 < 0.025 here, and the one this freeze could not measure honestly.
5. **The nine-cell `trend_t` × `vol_t` composition** — only six cells were observable here — and with
   it the single permitted suppression revision, **cells added only, never removed**.
6. **The DP-50(a)/(b) commit sweep and the v1.7 schedule check on the new freeze.** Today's "NONE"
   (HEAD `d19c9a9`) is an absence of a schedule, not a permanent clearance.
7. **The lock-or-DEFER inequalities re-solved from the trading calendar** against DP-43's 12-month
   ceiling **measured from the successor's own lock date** — they tighten as that date moves later.

**How `V` comes back.** As a **successor question with its own id**, inheriting Q033's definitions
verbatim — the partition, the ±0.5 ATR band, the ±10.0 pp MPE, the equivalence NULL clause, the DP-51
two-CI gate, the 80% composition guard — and **never by editing Q033**, whose lock fixes `m = 1` (the
H-067 / Q024 precedent, rule 3). Its window is **prospective-only from its own lock commit**, with
Q033's window carried as a labelled panel. It must also carry, in its own §10, the measured
`d_L3 < 0.5` share of **3.89% (20 of 514 valid picks)** — the conflation that biases `V` toward zero,
left in place deliberately and never screened out (DECISIONS items 21, 31).

### Bookkeeping

**No verdict of any kind was produced for P2 and no outcome was read.** `V` returns no CONFIRMED, no
NULL, no INCONCLUSIVE, no `G_μ`, no `G_α` and no arm difference; a gate shortfall is not a verdict.
No `eval.py` exists and no `results/` directory exists for Q033 at this date. The Steward's report is
counts of nights, picks, controls and bars on the pinned freezes, reading a forward bar only to
establish that a bar exists, with **no live query** (DP-50(c)).

**Correction sets.** **`m = 1`** inside Q033 (P1 alone) and **F8 = 1** at that lock, never below it.
**`A` stays in the F1 companion set, which is 28.** **F2 carries no Q033 endpoint while `V` is
deferred: 17 → 16** (Q023 2 + Q027 2 + Q029's 10 companion IC endpoints + Q031 2) — the
H-062 / Q025 / Q032 precedent. **No locked PREREG records Q033's `V` in its correction set, so no
locked file is edited and none was.** `G_μ` is not computed at all, so §8 clause 8's `G_μ` half and
the `G_μ` / `G` pairing lapse. `research/BACKLOG.md` marks **H-081 — registered as Q033 (P1 only);
the interaction half deferred, SPY history needs Alpaca credentials in the desk session**. Q033's R2
rider for SPY-from-2025-01-02 is **withdrawn and HELD** and is not built while this endpoint is
deferred; **Q027's, Q029's and Q031's own successor-freeze requests and pins are unaffected and are
not edited** (rule 3, DP-22). Floors **B** and **D**, §8 clauses **2, 3, 5, 7, 9** and the `G_μ` half
of clause 8, §10 threat 3, and the tape-episode block bootstrap and label permutation all travel here
with the endpoint.

**Caveat carried forward, so no successor repeats it.** Q033's own **2027-07-12** run prints `α_t`,
the raw direction and L3-touch rates, the descriptive `μ_t` and the §4.3 per-level reads **on the
nights 2026-09-15..2027-04-30**. A successor carrying `V` is therefore **post-hoc with respect to
those nights** and must run **prospective-only from its own lock**, with Q033's window as a labelled
panel — exactly the constraint Q033 itself applied to the sealed 2026-06-01..2026-08-12 stretch.
Under this file's preamble **nothing here may be reported, briefed or quoted** until the trigger is
met.

---

## Q035 / H-083 — "Would a setup-specific ranker (A flow · B projection-or-technical · C catalyst) pick a better eight than the universal 0–100 score?" — **the night's publishable choice set cannot be reconstructed: the projection layer is unscored on three of every four rows**

**Deferred 2026-09-14 by the registrar, autonomous run (DP-40..48), on this file's second admission
ground _as amended in the next paragraph_: the blocker is a **platform data-completeness gap, not
elapsed time**.** Drafted at `research/questions/Q035_setup_architecture/PREREG.md`; decided and
recorded at `research/questions/Q035_setup_architecture/DECISIONS.md` ("# RECORD — 2026-09-14",
items 1–4 and "Re-entry condition"); measured at `research/reports/STEWARD_Q035_exposure.md`
(data-steward, 2026-09-14, R1, nine limbs, counts only). **Never locked: no `PREREG_LOCKED`, no
`schedule.json`, no `pin_at_decision`** — the Q020 / Q025 / Q030 precedent; `state.json` reads
`PREREG_DRAFT` at this writing and the controller's transition to `DEFERRED` is the coordinator's
step, not the registrar's. **Both files are preserved exactly as drafted**; where the draft's body
and `DECISIONS.md` "# RECORD — 2026-09-14" disagree — the provisional schedule, the §7 correction-set
figure — **the RECORD governs, and a successor builds from the RECORD, not from the draft.**
**The question number Q035 is consumed by this entry and is not reused.**

**The amendment, stated once so a successor entry can cite it.** The second admission ground as
written (DP-43) is a *sample-size* ground: it admits a question whose earliest honest decision date
sits more than 12 months after lock, and it asks for the measured exposure rate, the projected floor
date and the re-check trigger. Q035 satisfies that ground on limb (b) alone — floor B projects at
**≈ 237 elapsed sessions** against the **225** admissible under the ceiling (below) — but that is the
*lesser* of two independent grounds and it is not what is wrong with this question. Three limbs fail
that **no window of any length reaches**, because each is a property of the shape of a single night's
choice set rather than of how many nights have accumulated, and their single common cause is a
**platform column that is incomplete**. The entry therefore names **the measured limb counts, the
completeness gap that drives them, and a measured re-check trigger in place of an accrual date**, and
records that **no DP-13 extension is available**: thirty, ninety or two hundred and twenty-five more
sessions add nights shaped exactly like the ones measured.

### What the question is, and why it is worth keeping

Haci's H13, *A/B/C architecture*. Each night the platform sorts its publishable candidates by one
universal 0–100 score and publishes the top eight. H-083 asks whether sorting each candidate by the
signal that is actually driving *it* — flow (setup **A**), projection-or-technical continuation
(**B**), catalyst (**C**), with a residual bucket **O** handed back to the universal rule — would
publish eight names that reach a target **2.0 ATR** away more often, within 20 sessions of the
session t+1 open, against the same night's distance-matched pool. Two primaries were registered, both
two-sided, both **MPE ±5.0 pp (DP-20, DP-44)**: **P1**, a ranker whose three weights are fitted once
after the lock commit and never refit, and **P2**, the pure ranker (`w ≡ 1`), which needs no fit, no
training data and no artefact and is the form of H13 that cannot be argued with. It is a question
about *ordering inside the publishable set* and says nothing about the 80 floor, the 90 line or the
8-slot cap, all of which are held as fixed configuration identical in both arms. The design is
complete and stands; nothing about it is unanswerable in principle — only unreconstructable on the
data the platform currently writes.

### Why it cannot be registered — the three limbs that fail, and the one thing that drives all three

The lock-or-DEFER gate (PREREG §5.3 R1 as amended by `DECISIONS.md` items 2, 4, 13, 14 and 19) has
seven gated limbs; the branch that fires on any short limb was fixed at `decide`, **before any count
was seen**. Measured on `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, pick
nights **2026-06-01..2026-09-10**, **N = 71** elapsed sessions, **68** non-excluded, counts only, no
outcome column of any kind read, **no live query** (DP-50(c)):

| limb | floor, fixed at `decide` and never moved | measured | result |
|---|---|---:|---|
| **(c) reorder room** | median `\|P_t\| ≥ 11` **and** `\|P_t\| ≥ 9` on **≥ 80%** of nights | **median 5** (mean 5.83, min 1 / max 14); **31.7%** (13/41) | **SHORT — both sub-clauses** |
| **(d) reorder rate** | **≥ 0.50** of contributing nights | **0.2683** (11/41); mean names swapped over all nights **0.34** | **SHORT** |
| **(f) reconstruction correctness** | agreement **≥ 0.90** on nights where §2.5 removed no row | registered population **empty — 0 of 41** qualifying nights; **0.00** on the only computable proxy | **SHORT — undefined on its own registered population** |

They are not three findings. **(d) is mechanically downstream of (c)** — a set whose median size is 5
cannot reorder a slate of 8 — and **(f) is (c) again at the other end**: once the completeness screen
removes roughly 70% of a night's rows, the top-8-by-`overall_score` of what survives is not the eight
names the platform actually published, because most of the published eight are themselves among the
rows the screen just removed.

**The driver, named exactly.** The **projection** layer — v1.6 weight **29**, the single largest of
the seven — carries `score: null, available: false, reasons: ["Projection context unavailable"],
weight: 0.0` in `score_details_json.weighted_dimensions.projection` on **72.2% of the 579 `selected`
(published) main-lane rows** and **74.3% of the 692 `capped_by_max_output` rows** in this window, read
directly off the frozen rows before any Q035 screen touched them, and **not** concentrated in one
timeframe (short, swing and long all sit at 71–79%). It takes the median `|P_t|` from **16**
pre-screen to **3** after completeness and **5** after gradeability. A **second, independent desk
measurement of the same hole** corroborates it on a different population:
`research/questions/Q029_layer_value_ablation/PREREG.md` records `projection_score` non-null on
**62.74%** of its segment rows, clearing 70% in **no month measured** (49.44% → 65.11% peak,
plateauing below the floor from July), which is why Q029 registered `projection` as **UNEVALUABLE**
on its E1 and E2 endpoints. Two questions, two populations, one gap. It is filed as
**`research/PLATFORM_ISSUES.md` PI-015** (high, OPEN) — a recommendation only; the decision is Haci's.

**Limb (b), on the reading that governs.** The rarest setup (**C**, catalyst) places at least one name
on **6** nights: **0.0845 per elapsed session on the full-window reading, against a floor of ≥ 0.09 —
SHORT**. The reading was settled at `record` and a re-attempt inherits it: **numerator and denominator
are counted over the same period, and the period is the full window** (the
Q019/Q022/Q023/Q027/Q031/Q032/Q033 elapsed-session convention). The sub-period reading — 6 nights over
the 51 sessions that happen to be t+20-gradeable inside this freeze, **0.1176**, which *passes* — is
**not taken**: it divides by a denominator the freeze's own right-censoring chose, and DP-45 forbids
taking an option because it clears a floor more easily. On the governing reading, **floor B (20 nights
in setup C) projects at ≈ 237 elapsed sessions against the 225 admissible under DP-43's 12-month
ceiling** from a 2026-09-14 lock (20 sessions of maturity, a one-week margin, latest admissible
decision Monday 2027-09-13, last window end 2027-08-06) — the second, independent ground. At the
sub-period reading it would be ≈ 170 sessions, inside the ceiling; that reading is recorded and not
used.

**What was *not* the problem — recorded so a re-attempt does not go looking in the wrong place.** Four
of the seven gated limbs clear, two of them comfortably:

- **(a) contributing-night rate: 0.5775** (41/71 full window; 0.8039 on the t+20-evaluable sub-period)
  against a floor of **≥ 0.36**. Nights are not scarce. Floors A, C and D would all be reached well
  inside the ceiling at this rate.
- **(e) partition viability: row-weighted margin share 0.615** against **≥ 0.60**, and **≥ 4 layers
  carrying non-zero within-night variance on 85.4%** of nights (35/41) against **≥ 80%**. **PASS,
  narrowly.** The A/B/C partition itself separates; it is not the defect.
- **(g) DP-50(a)/(b) commit sweep since `fa70688`: NONE.** HEAD reconfirmed at `d19c9a9`; no weight,
  threshold, cap, completeness floor, bear-lane setting, enable-flag or v1.7 promotion has landed
  since the pin. No mid-window ship explains any count above.
- **(h), informational: 442 of 2,739 non-bearish-lane rows (16.1%) are `mixed`, and 0 of them reach
  `qualification_reason IN ('selected','capped_by_max_output')` or the published slate.** The
  population correction the `decide` pass made — reading the platform's main lane as *non-bearish*
  (bullish + mixed, `services/super_agent_select_scoring.py:1643`, docstring `:1628`) rather than
  bullish-only — is **verified right against the code and numerically inert on this window**. It was
  the `decide` pass's headline finding, and it changed no number here. (Limb (i), the printed swing
  target distance in ATR units, was not computed and is non-gating in every branch.)

One further measurement is worth keeping, because it is the cleanest evidence that the population
correction is sound and that the defect is the screen's input rather than the question's construction:
on the **raw** `P_t` (direction + qualification-reason filter alone, 1,185 rows / 68 nights) the
reconstructed universal slate agrees with the platform's actual published slate on **68 / 68 nights =
100%**.

### What was considered and rejected before deferring

Each of these would have bought a testable question by weakening it, which `DECISIONS.md` item 4 and
DP-45 forbid. They are listed because a deferred question is exactly where the temptation lands.

- **Re-specifying `P_t`** — widening it to the published eight, narrowing it, rebuilding it without
  the completeness screen, or rebuilding it on a bullish-only or an all-lane filter. **Rejected.**
- **Loosening the §2.5(3) completeness screen beyond the one reading settled at `record`.**
  **Rejected.** The settled reading excludes **`smart_money_confirmation_score` and only it** — that
  column is null on **100% of the entire 6,479-row frozen `sas_candidates` table** (PI-008's weight-0
  layer, the one §2.3 already accommodates with its zero-variance argmax exclusion), so a literal
  screen would empty `P_t` **on every window, forever**, and a screen that empties its own population
  on all inputs is not a screen. The **projection** nulls stay inside the screen and keep removing
  rows: they are a genuine gap in a weight-29 layer, not a structural constant. Loosening the screen
  to reach the gate is the move this entry explicitly refuses.
- **Merging the setups** — folding C into B, or making O a setup — to cure limb (b). **Rejected.**
- **Reducing any floor** — the median `|P_t| ≥ 11`, the `≥ 9` on 80% of nights, the reorder rate 0.50,
  the reconstruction 0.90, or 80/20 (DP-21). **Rejected.**
- **Taking limb (b)'s sub-period reading**, which passes the gate and shortens the floor-B projection
  from ≈ 237 sessions to ≈ 170. **Rejected under DP-45**, on principle and not on arithmetic: it
  borrows the freeze's right-censoring as a denominator.
- **DP-13's single automatic extension.** **Rejected.** DP-13 rescues a *count* that is marginal at a
  decision date. Limbs (c), (d) and (f) are **testability limbs, not sample-rate gates**
  (`DECISIONS.md` item 14's own words), and the null-projection share is flat across the freeze at
  71–79% in every timeframe bucket, so more nights arrive with the same median `|P_t|`, the same
  reorder rate and the same empty (f) population.

**Stated plainly, because it is the whole point of this entry: Q035 is not re-registered on a weaker
partition, a merged setup, a widened `P_t` or a reduced floor. A different partition, a different
population or a different screen is a different question with its own id**, registered from the
BACKLOG with its own PREREG, its own MPEs and its own §10 — never Q035 re-entering under its own
number on a weaker construction.

### Re-entry condition — the five triggers, verbatim from `DECISIONS.md`

Q035 returns to the backlog when the Steward measures, on a successor freeze **over a trailing
quarter**, all of the following. They are the registered floors, unchanged; the fourth is the driver
that has to move first and is stated because the other three are mechanically downstream of it.

1. **Reorder room** — median `|P_t| ≥ 11` **and** `|P_t| ≥ 9` on **≥ 80%** of contributing nights.
   *Measured 2026-09-14: median **5**, **31.7%**.*
2. **Reorder rate** — pure-ranker slate differs from the reconstructed universal slate on **≥ 0.50** of
   contributing nights. *Measured: **0.2683**.*
3. **Reconstruction correctness** — agreement **≥ 0.90** on a **non-empty** population of nights where
   §2.5 removes no row. *Measured: population **empty** (0/41); **0.00** on the proxy.*
4. **Projection-layer coverage, the driver** — `projection_score` non-null (`available: true`) on
   **≥ 70%** of both `selected` and `capped_by_max_output` main-lane rows, i.e. a null share **≤ 30%**
   against today's **72.2%** and **74.3%**. The 30% is not a new floor: it is what trigger 1 requires
   arithmetically — the pre-screen median `|P_t|` is **16**, so a screen removing more than ~31% of a
   night's rows cannot leave a median of 11. It is **necessary, not sufficient**, and triggers 1–3 are
   re-measured on their own terms regardless of it.
5. **Rate gates, unchanged** — contributing nights **≥ 0.36** and rarest-setup nights **≥ 0.09** per
   elapsed session, **on the full-window reading** (settled above). *Measured: **0.5775** (clears) and
   **0.0845** (short).*

**No calendar re-check date is named and none is invented.** The trigger is a measurement, and the
measurement that has to move first is trigger 4 — which moves only if the platform's projection
coverage changes (PI-015), not if nights accrue.

### What a re-attempt must re-measure

Nothing in the Steward's report is inherited as a measurement; only the **readings** (limb (b)'s
full-window convention; the completeness screen's `smart_money_confirmation_score` exclusion) and the
**refusals** (the list above) carry forward. A re-attempt re-runs **all seven gated limbs from
scratch** on the successor freeze, over a trailing quarter, with: the non-bearish-lane population
correction and the `qualification_reason IN ('selected','capped_by_max_output')` reason set; limb (f)
measured on its **own registered population**, with the qualifying-night count stated even when it is
zero; the mixed-row share re-reported (inert today, not inert by construction); and the DP-50(a)/(b)
commit sweep repeated. **The sweep is load-bearing for a re-attempt in a way it was not for this
lock:** if a projection-coverage repair ships, `projection_score` becomes **two different features**
at the ship date (DP-06 / DP-50(a)), and so does every setup label derived from it and the
`overall_score` that ranks the universal arm — a re-attempt's window **splits at the repair date and
may use the post-repair segment only**, with its elapsed-session count starting there.

### Bookkeeping while deferred

**No verdict of any kind was produced.** Q035 returns no CONFIRMED, no NULL, no INCONCLUSIVE, no `Δ_t`,
no P1 number and no P2 number; a gate shortfall is not a verdict. **No `eval.py` and no `fit.py` were
written, no `results/` directory exists, no `setup_model_v001.json` was produced and no
`setup_model_v001.sha256` was committed**; the 2026-10-05 script deadline is **void**. No outcome —
touch, first-touch date, return, excursion or arm difference — was read for this question at any
point: R1 read forward bars only to establish that a bar exists, and its counts are `NON_QUOTABLE`
exposure measurements, never a result about setup architecture.

**Correction set.** Q035's two primaries **never join F8**, which stays at **1** — Q033's P1 alone
(the H-062 / Q025 / H-074 precedent: a deferred question leaves the correction set, and one that never
locked never enters it). The draft's own §7 figure (Q033 as 2, F8 as 4) is superseded on both counts
and no locked file is edited.

**Successor freezes and Steward requests.** R3 (the successor selection and price freeze pair) and R2
(`fit.py` / `eval.py` / the artefact) are **WITHDRAWN** — a deferred question builds no freeze, writes
no script and runs no fit — and Q035's line in the R3 request is struck. **The successor freezes
Q027, Q029, Q031, Q033 and Q034 need are unaffected and are not edited**: Q035 was a subset of that
build, never a driver of it. **No successor freeze is built or requested for this question.**

**`research/BACKLOG.md`** marks **H-083 — DEFERRED (Q035 drafted; …)**, not registered. The related
platform fact is filed as **PI-015** (`research/PLATFORM_ISSUES.md`, high, OPEN) with a repo-only
check (DP-49) and a DP-50(b) ship-timing paragraph; that filing is a **recommendation**, and nothing
further is filed until `/desk-run prompt PI-015`.

**Rule 14 note, carried forward:** Q035 requested no exception and needed none — every input is a
16:05 ET candidate column, a bar dated ≤ t, or the session t+1 open used only as an entry price.
**DP-05 is untouched and DP-41 is not engaged**, and a successor inherits that clean position.

Under this file's preamble **nothing here may be reported, briefed or quoted** until the triggers are
met.

---

## Q036 / H-011 — "Does the published high/medium/low conviction label mark a better price path?" — **the arm E2 compares against does not exist on this scoring configuration**

**Deferred 2026-09-14 by the registrar, autonomous run (DP-40..48), on this file's **second**
admission ground (DP-43's 12-month ceiling) — in its strongest form, the Q025 shape: the binding
rate is not slow, it is **exactly zero**, so the projected floor date is **undefined** rather than
distant.** Drafted at `research/questions/Q036_confidence_label_validity/PREREG.md`; decided and
recorded at `research/questions/Q036_confidence_label_validity/DECISIONS.md` (decision-maker,
`decide` + `record` passes 2026-09-14, 19 items, 6 corrections); measured at
`research/reports/STEWARD_Q036_exposure.md` (data-steward, 2026-09-14, R1, eight limbs (a)–(h),
counts only, no outcome of any kind read, no live query — DP-50(c)). **Never locked: no
`PREREG_LOCKED`, no `schedule.json`, no pin** — the Q020 / Q025 / Q030 / Q035 precedent;
`state.json` reads `PREREG_DRAFT` at this writing and the controller's transition to `DEFERRED` is
the coordinator's step, not the registrar's. **Both files are preserved exactly as drafted** —
`@registrar apply Q036` was **not** run, so Corrections 1–6 stand in `DECISIONS.md` rather than in
the draft's body, and **where the two disagree, `DECISIONS.md` "## Record — 2026-09-14" governs; any
re-attempt builds from that record, not from the draft.** **The question number Q036 is consumed by
this entry and is not reused.** This is **not** the first admission ground: the objective *is*
measurable from the frozen manifests. What does not exist is one of the two arms.

### What the question is, and why it is worth keeping

The platform prints *"scored X with {confidence_level} conviction"* on every published card
(`services/super_agent_select_public.py:212`, verified read-only at the pinned SHA), and **nothing
has ever tested the word.** Q036 asked whether the label marks a better price path: two primaries,
both night-level, both within-night touch-rate contrasts at the night's common ATR distance `d*_t`
with a session t+1 open entry on the DP-09 20-session clock (DP-03(b), DP-42), both **two-sided at
±5.0 pp (DP-20, DP-44)** — **E1**, the unconditional HIGH−MED touch-rate difference against H-011's
own label-shuffle baseline; **E2**, the same contrast on adjacent-score-rank discordant pairs with
`overall_score ≥ 82`, which is the part that is *not* a restatement of Q027's ranking result.

**A confirmed negative was the branch with the larger consequence**, and that is why both primaries
were registered two-sided: the desk's own weekly of 2026-09-12 recorded medium beating high on
sealed nights (78% vs 65% next-open L1 touch), so a confirmed mis-ordering would **suspend a
subscriber-facing claim** rather than add one. The design is complete and stands — population,
`d*_t`, the label-integrity screen, the episode-clustered CI blocker (DP-51), the §8 clause 4 rule
that "E1 confirms, E2 nulls" is a **NULL for Q036**. Nothing about it is unanswerable in principle —
only unpopulated.

### Why it cannot be registered — the label's own arithmetic against the measured completeness floor

`_confidence_label(overall_score, completeness_score)`
(`services/super_agent_select_scoring.py:1166-1171`, called at `:1425` **after** the ATR-elite cap
block at `:1407-1423`, stamped at `:1451`; verified byte-identical at the pin) is a **joint step
function**:

- `high` ⇔ `overall_score ≥ 82` **∧** `completeness_score ≥ 65`
- `medium` ⇔ ¬`high` **∧** `overall_score ≥ 68` **∧** `completeness_score ≥ 45`
- `low` otherwise

E2's population is therefore **`medium ∧ overall_score ≥ 82`**, which requires
`completeness_score ∈ [45, 65)`. **The measured minimum `completeness_score` anywhere in the window
is 65.3686, across all 4,195 scored `sas_candidates` rows — published and unpublished, any
qualification status, any date.** The instant a row clears 82 it is `high` by construction, so
**E2's arm is an empty cell by arithmetic, not a rare one**, and **all 26 of E1's contributing
nights fall out of E2 solely because every MED row that night sits in `[80.05, 81.99]`** — §2.5's
anticipated zero-mass gap, measured at its maximum possible value (100% of E1's nights, not a
subset).

Counts only, on `manifest_v001` + `manifest_prices_v001` against `exclusions_v003.json`, pick nights
**2026-06-01..2026-09-10** (DP-06's segment), denominator = **elapsed sessions**
(`STEWARD_Q036_exposure.md`):

| quantity | gate (fixed at `decide`, before any count existed) | measured | call |
|---|---|---:|---|
| **E2 `r_join`, the limb that decides** (`overall_score ≥ 82`) | **≥ 0.43** | **0.0000** — 0/47 matured, 0/71 elapsed, 0/67 non-excluded | **SHORT by the whole 0.43** |
| E1 `r_join`, Form (i), the schedule basis (item 6) | ≥ 0.43 | **0.5532** (26/47) | PASS |
| E1 `r_join`, Form (ii), full denominator | — | 0.3662 (26/71) | descriptive |
| `ρ_co` marginal (diagnostic only, item 6) | — | 0.6269 (42/67) / 0.5915 (42/71) | diagnostic |
| (g) label-integrity mismatch, recomputed vs stored | ≤ 2% | **0.000%** (0 of 542; 0 boundary cases) | PASS |
| (d) LOW arm | descriptive floor (item 12) | **0 nights** | structurally absent, not thin |
| Minimum `completeness_score`, all scored rows | — | **65.3686** of 4,195 rows | the blocker |
| Published label composition, 542 rows / 67 nights | — | **401 high / 141 medium / 0 low**; 25 of 67 nights single-label, every one all-HIGH | — |
| `overall_score × completeness_score` grid, both cohorts | — | **every cell in the `[65,100]` completeness column**; 0 rows in `[35,45)`, 0 in `[45,65)` | — |
| Population funnel | — | 71 elapsed · 68 non-excluded (`exclusions_v003`) · **67** after `payload_disabled_runs` (2026-06-02) · **47 matured to t+20** (last 2026-08-12) | — |
| `d*_t` | — | defined on all 67 nights; median **1.858 ATR** (reproduces `STEWARD_Q027_exposure.md`'s 1.849 on an independently built ATR series); 0 zero-survivor, 0 fallback nights | — |

**Both of `DECISIONS.md` item 7's independent DEFERRED triggers fire**, and neither was written with
the counts in view: **E2's `r_join` < 0.37** on its own, and **E1 clearing while E2 fails**, which
item 7 and PREREG §5.1's gate table both answer with *"DEFERRED, not lock E1 alone"*.

**This deferral is not a data-quality defect.** Limb (g) measures **0.000%** with **0** boundary
cases, so `sas_candidates.confidence_level` is exactly what `_confidence_label` at the pinned SHA
would write from the stored columns; item 10's PI branch does **not** fire. What is filed instead is
the *consequence* — a subscriber-facing field that is effectively constant — as **PI-016**
(`research/PLATFORM_ISSUES.md`, med, OPEN), a recommendation only, and **no successor may cite it as
evidence that the label does or does not predict the price path.** That question is this one, and it
is deferred.

### Why waiting does not fix it

**DP-13 cannot cure a structural zero, and no window length can.** DP-13 extends a window **once**,
by +30 sessions, when a floor is *marginal* at the decision date, and it fires on `eval.py`'s
measured counts. It moves a slow rate to a later date; it cannot create a row in a cell whose
membership condition is **arithmetically unsatisfiable under the running configuration**. At a rate
of exactly zero the projected floor date is **undefined**, not merely distant — contrast Q034's
finite "≈ session 880" and this question's own E1, which would clear 80 nights in ≈ 145 elapsed
sessions and decides nothing. The extension is also registered **at lock**, and Q036 never locks.
(The H-062 / Q025 reading of DP-13, verbatim: it rescues a floor short by a handful, not by 80 of
80.) Nights arrive at ~21 a month and add contributing nights to E2 at a rate of **0.000**, so
**no accrual date exists to name and none is invented.**

### What was considered and rejected before deferring

- **Locking E1 alone.** **Refused.** §1.2 and §8 clause 4 give the reason and the measurement does
  not change it: the label *contains* `overall_score ≥ 82`, so an unconditional HIGH−MED contrast is
  partly Q027's ranking result on a coarser variable. Locking E1 alone would add a primary to the F2
  correction set that can only restate another question (**DP-29**) — and it would do so by dropping
  the one endpoint that made this a different question, on the ground that its exposure rate is
  comfortable. That is buying a runnable question with the part that was worth running.
- **A lowered or widened completeness cut** — a "completeness ≥ 55" version, or re-basing the 82.
  **Rejected (DP-25, rule 3).** The 82 and the 65 are the platform's own constants at `:1167-1170`,
  not desk choices; moving either manufactures a MED arm and tests a label the platform does not
  print.
- **Substituting the unpublished `threshold_pass` (dark) cohort for the published slate.**
  **Rejected** — item 1 and Correction 5, on the code rather than on preference: `threshold_pass` is
  `overall_score ≥ max(lane_threshold, publication_floor = 80)` **and** `completeness_score ≥
  min_completeness = 35` (`services/super_agent_select_scoring.py:1518-1521`), so the dark cohort
  carries the **identical** two floors and the identical 65+ completeness ceiling — measured **564
  medium / 82 high / 0 low on 646 rows**, every cell of its grid in the `[65,100]` column. It buys no
  label mass at all, and it is Q027's population exactly.
- **DP-13's single automatic extension.** **Rejected**, for the reason set out above: short by 80 of
  80, at a rate of zero, on a question that never locks.

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

### Bookkeeping while deferred

**No verdict of any kind was produced.** Q036 returns **no CONFIRMED, no NULL, no INCONCLUSIVE, no E1
number and no E2 number** — a gate shortfall is not a verdict (the Q025 item 14 precedent). E1's
0.5532 is an **exposure rate**, not a result about the label. **No `eval.py` was written and none
exists, no `results/` directory exists and none may be created**, and no outcome — touch, first-touch
date, return, excursion, `outcome_*`, `sas_selection_excursion` or
`uoa_symbol_daily.fwd_return_*` — was read for this question at any point; R1 read forward bars only
to establish that a bar exists (maturity accounting), and its counts are `NON_QUOTABLE` exposure
measurements.

**Correction set.** **F2 returns to the 16 primaries standing before this draft** — Q023 (2) +
Q027 (2) + Q029's 10 companion IC endpoints + Q031 (2) — which is exactly `Q031 §7`'s own figure, so
**no locked file needs editing and none was edited** (the H-062 / Q025 / H-083 precedent: a question
that never locked never enters the correction set). Q036's two primaries never join it.

**Successor freezes and routed requests.** **R2 is withdrawn** — no successor freeze is built or
requested for Q036, and the shared selection build serving **Q027, Q029, Q031, Q033 and Q034 is not
extended or re-scoped** for it; their own pins are unaffected and are not edited. **R3 is not
issued**: no `eval.py` is written and the 2027-04-05 script deadline is void. The provisional
schedule the `decide` pass carried (window 2026-09-15..2027-06-11, decision 2027-07-26, extension to
2027-07-27 decided 2027-09-13) is **struck in full and is never inherited** — on any re-entry the
whole schedule is recomputed from the new lock date at the then-measured rate, **out only**. What
survives the striking is method, not dates: the gate thresholds are re-solved and never lowered
(item 7), the scheduling rate stays `min(r_join, 0.6620)` on the **joint** event (item 6), floors
stay 80 per primary and 20 per reported cell (DP-21), and the corrected holiday list stands
(item 5, Correction 1).

**`research/BACKLOG.md`** marks **H-011 — DEFERRED 2026-09-14**, not registered and **not merged into
Q027** (DP-29: Q027 tests `overall_score` ranking and cannot return a verdict on a joint step
function of the score *and* `completeness_score`).

**Filings.** **`PI-016`** (`research/PLATFORM_ISSUES.md`, med, OPEN) — the conviction label is
degenerate on the published slate; a **recommendation only** under DP-07 / DP-48, `HACI_DECIDED`
unset until `/desk-run prompt PI-016`, and explicitly **not** a finding about whether the label
predicts the price path. A `DATA_NOTES.md` note on Correction 6 — the runtime `config_json`
overrides the ORM default for `enable_fundamental_enrichment` on every one of the 67 nights measured
— is routed to the **Data Steward** (`DECISIONS.md` "Routed requests → data-steward (N1)"); the
registrar writes nothing into `research/data/`. **`Q028_layer_signal_independence/PREREG.md` (locked)
§9 `:506` and §10 `:580` carry the code-default reading that the measurement contradicts for
`fundamental_quality`; the locked file stands and is not edited, and the discrepancy is flagged to
the Red Team** to read against `STEWARD_Q036_exposure.md` §(f) and `Q029 §2` at sign-off.
`Q032 (:368)`, `Q033 (:476)` and `Q034 (:498)` register `confidence_level` terciles as descriptive
strata that will collapse to at most two cells on this data — their own §4 floors already mark a thin
cell descriptive, so **nothing is owed and nothing is edited**; it is noted so the collapse is
expected rather than discovered.

**DP-50(b):** **no flag-off constraint is owed by Q036 and none is asserted.** The deferral removes
the desk's only claim on the §2.6 settings, and a change to them is the very thing that could make
this question testable again. Q027, Q028 and Q029 keep their own constraints; Q036 adds none.

**Rule 14 note, carried forward:** Q036 requested no exception and needed none — every input is a
16:05 ET candidate field (`overall_score`, `completeness_score`, `confidence_level`, direction, lane,
the printed ladder), a split-adjusted bar dated ≤ t, or a point-in-time regime row legal from
2026-06-09, with the session t+1 open used **only** as an entry price. **DP-05 is untouched and
DP-41 is not engaged**, and a successor inherits that clean position.

Under this file's preamble **nothing here may be reported, briefed or quoted** until the trigger is
met.
