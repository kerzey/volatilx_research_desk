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
