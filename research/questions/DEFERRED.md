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
