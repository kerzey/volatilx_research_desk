# Q035 — decisions before lock
Run: 2026-09-14 by decision-maker (autonomous, DP-40..48) · Source: PREREG.md "Open decisions before
lock", 7 items (+ 20 decided, defaulted or routed here: the three routed requests named in §5.3 and
seventeen the draft settles silently or leaves to `record`)
`record`: 2026-09-14 by decision-maker (autonomous, DP-40..48) · Source: `research/reports/STEWARD_Q035_exposure.md` (R1, nine limbs) · **Outcome: DEFERRED**

State checked: `state.json` = `PREREG_DRAFT` (registrar, 2026-09-14) — in scope.

---

# RECORD — 2026-09-14: R1 landed. **Q035 is DEFERRED.**

**Q035 does not lock. Three of the seven gated limbs of R1 are short — (c) reorder room, (d) reorder
rate, (f) reconstruction correctness — and the branch that fires on them was fixed at `decide`, before
any count was seen (item 14, item 15, and the routed request's own closing sentence: "Any limb short →
Q035 goes to `research/questions/DEFERRED.md` with the measured counts and the re-check trigger, and it
is **not** re-registered on a weaker partition, a merged setup or a reduced floor").** The limbs that
fire are **testability** limbs, not sample-rate gates, so **DP-13's extension does not apply and the
question is not scheduled**: waiting adds nights shaped exactly like the ones measured. The root cause
is a platform data-completeness fact the desk had not logged — the **projection** layer (v1.6 weight 29,
the largest of the seven) carries `score: null, available: false, reasons: ["Projection context
unavailable"]` on **72.2%** of published bull-lane rows and **74.3%** of `capped_by_max_output` rows in
the window — and it is recommended to the Registrar as a platform issue below (DP-48), not fixed here.

**R1 is CLOSED.** Source: **`research/reports/STEWARD_Q035_exposure.md`** (data-steward, 2026-09-14),
measured on `research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json` against
`research/data/exclusions_v003.json`, pick nights **2026-06-01..2026-09-10**, **N = 71** elapsed
sessions, **68** non-excluded (2026-06-26, 2026-07-02, 2026-07-06 removed), counts only, no outcome
column of any kind read, no live query (DP-50(c)), with item 2's non-bearish-lane population correction
applied throughout. All nine limbs answered; limb (i) not computed and non-gating in every branch
(item 4), which changes nothing. **Item 26 (R3, successor freezes) and item 27 (R2, `fit.py` /
`eval.py` / the artefact) are WITHDRAWN** — a deferred question builds no freeze, writes no script,
runs no fit; the **2026-10-05 script deadline is void** and Q035's line in the R3 request is struck.
The successor selection and price freezes Q027, Q029, Q031, Q033 and Q034 need are unaffected: Q035 was
a subset of that build, never a driver of it.

## The gate, limb by limb, against the thresholds fixed at `decide`

| limb | floor (fixed at decide, never moved) | measured | result |
|---|---|---|---|
| (a) contributing nights / elapsed session | ≥ 0.36 (item 14) | **0.5775** (41/71); 0.8039 (41/51) | **PASS** |
| (b) rarest setup (C, catalyst) / elapsed session | ≥ 0.09 (item 14) | **0.0845** (6/71) full window; 0.1176 (6/51) sub-period | **SHORT** on the governing reading (below) |
| (c) reorder room | median `\|P_t\| ≥ 11` **and** `\|P_t\| ≥ 9` on ≥ 80% of nights | **median 5**, mean 5.83, **31.7%** (13/41) | **SHORT**, both sub-clauses |
| (d) reorder rate | ≥ 0.50 | **0.2683** (11/41); mean names swapped 0.34 over all nights | **SHORT** |
| (e) partition viability | margin share ≥ 0.60; ≥ 4 varying layers on ≥ 80% of nights | 0.615; 85.4% (35/41) | **PASS**, narrowly |
| (f) reconstruction correctness | agreement ≥ 0.90 on nights where §2.5 removed no row | **0** such nights exist (0/41); **0.00** on the only computable proxy | **SHORT** — undefined on its registered population |
| (g) DP-50(a)/(b) commit sweep since `fa70688` | no change, or dated | HEAD `d19c9a9` reconfirmed; **NONE** | **PASS** |

Informational: (h) 442/2,739 non-bearish-lane rows (16.1%) are `mixed`, and **0** of them reach
`qualification_reason IN ('selected','capped_by_max_output')` or the published slate — item 2's
correction is verified right against the code and **numerically inert on this window**, which is worth
recording exactly because it was the decide pass's headline finding. (i) not computed, non-gating.

## What is settled at this `record`

**1. The branch — (c), (d) and (f) fire, and they are not time-curable.** DP-13 grants one extension of
+30 sessions when a **count** is short; nothing it grants touches these three. Each is a property of the
**shape of a single night's `P_t`**, not of how many nights have accumulated: (c) is the median size of
that set, (d) is the share of nights on which two slates built from that set differ — mechanically
downstream of (c), since a set of median 5 cannot reorder a top-8 — and (f) is the per-night agreement
between the reconstructed and the published slate, whose registered population (nights on which §2.5
removes no row) is **empty, 0 of 41**. The driver is flat across the freeze: the null-projection share
sits at 71–79% in every timeframe bucket and at 72–74% across the whole window, so an additional 30, 90
or 225 sessions adds nights with the same median `|P_t|`, the same reorder rate and the same empty
(f) population. **Therefore: no extension, no schedule, no decision date.** The DEFERRED trigger is item
14's testability clause, not DP-43's 12-month ceiling — but **DP-43's ceiling defers this question
independently too**, on limb (b) under the reading settled next: floor B (20 nights in setup C) projects
at **≈ 237 elapsed sessions** against the **225** admissible under the ceiling. Two independent grounds,
same answer.

**2. Limb (b)'s reading — the full-window reading governs, so (b) is SHORT at 0.0845 (DP-45).** For the
record only: it changes no branch, because (c), (d) and (f) are short by margins no reading can close.
The Steward flagged and did not decide it, correctly. The rule is fixed here so a re-attempt inherits
it: **numerator and denominator are counted over the same period, and the period is the full window**
(item 13's own construction, and the Q019/Q022/Q023/Q027/Q031/Q032/Q033 elapsed-session convention).
The sub-period reading — 6 nights over the 51 sessions that happen to be t+20-gradeable inside this
freeze — divides by a denominator the freeze's right-censoring chose, which is a property of the
**freeze end date**, not of the platform's behaviour; it is also the reading that reaches the gate and
the shorter floor-B projection, and DP-45 forbids taking an option because it clears a floor more
easily. Not taken: the sub-period reading, 0.1176 — passes the gate, borrows the freeze's censoring.

**3. §2.5(3)'s completeness screen — `smart_money_confirmation_score` is excluded from it, and the
screen otherwise stands (PI-008 pattern).** The Steward's reading is adopted verbatim and registered so
a re-attempt inherits it rather than re-deriving it. Read fully literally, §2.5(3) ("a null/non-finite
value in **any** of the seven layer subscores removes the row") empties `P_t` **on every window,
forever**: that column is null on **100% of the entire 6,479-row frozen `sas_candidates` table**, which
is PI-008's weight-0 layer and is exactly the column §2.3 already accommodates with its zero-variance
argmax exclusion. A screen that empties its own population on all inputs is not a screen. **The excluded
column is the always-null one, and only it:** the **projection** nulls stay inside the screen and keep
removing rows — they are a genuine gap in a weight-29 layer, not a structural constant — which is why
the median `|P_t|` falls from 16 pre-screen to 3 after completeness and 5 after gradeability. Loosening
the screen to reach the gate is the move this record explicitly refuses (item 15, DP-21, DP-45).

**4. What is never done to make this question testable.** Fixed at `decide`, restated here because a
deferred question is exactly where the temptation lands: `P_t` is **never** re-specified — not widened
to the published eight, not narrowed, not rebuilt without the completeness screen, not rebuilt on a
bullish-only or an all-lane filter; the **setups are never merged** (C is not folded into B, O is never
made a setup); **no floor is reduced** — not the median `|P_t| ≥ 11`, not `≥ 9` on 80% of nights, not
the reorder rate 0.50, not the reconstruction 0.90, not 80/20 (DP-21); and the uniform 2.0-ATR level,
the entry, the clock, the MPE and the family stand as decided. **A different partition, a different
population or a different screen is a different question with its own id**, registered from the BACKLOG
with its own PREREG — never Q035 re-entering under its own number on a weaker construction.

## Re-entry condition — measured triggers, with the numbers

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

## What a re-attempt must re-measure

Nothing in this report is inherited as a measurement; only the **readings** (items 2 and 3 above) and
the refusals (item 4 above) carry forward. A re-attempt re-runs **all seven gated limbs from scratch**
on the successor freeze, over a trailing quarter, with: item 2's non-bearish-lane population correction
and item 1's `qualification_reason IN ('selected','capped_by_max_output')` reason set; the completeness
reading settled above; limb (f) measured on its **own registered population**, with the qualifying-night
count stated even when it is zero; the mixed-row share re-reported (inert today, not inert by
construction); and the DP-50(a)/(b) commit sweep repeated. **The sweep is load-bearing for the
re-attempt in a way it was not for the lock:** if a projection-coverage repair ships, `projection_score`
becomes **two different features** at the ship date (DP-06 / DP-50(a)) and so does every setup label
derived from it and the `overall_score` that ranks the universal arm — a re-attempt's window **splits at
the repair date and may use the post-repair segment only**, and its elapsed-session count starts there.

## Schedule

**DEFERRED — no schedule. The provisional block below (written at `decide`, before R1) is struck in
full and none of its dates stands.**

decision_date: **none — DEFERRED** · extension_date: **none** · hard_stop: **none** · rule: **none —
the blocker is a platform data-completeness gap, not elapsed time**

- **why no date:** limbs (c), (d) and (f) are testability limbs (item 14's own words). No window
  reaches them, so DP-43 names no window and DP-13 grants no extension. Independently, limb (b) on its
  governing full-window reading projects floor B at **≈ 237** elapsed sessions against the **225**
  admissible under DP-43's 12-month ceiling from a 2026-09-14 lock — the ceiling clause defers it too.
- **no `pin_at_decision`, no successor freeze, no script deadline:** items 26 and 27 withdrawn; the
  2026-10-05 `eval.py` / `fit.py` deadline is void; no `setup_model_v001.json` is produced and no
  `setup_model_v001.sha256` is committed.
- **no verdict, nothing quotable:** a deferred question produces no NULL, no INCONCLUSIVE and no
  finding. R1's counts are exposure measurements, `NON_QUOTABLE`, and are never reported as a result
  about setup architecture. The single reportable fact is the platform issue below, which is a fact
  about **data completeness**, not about the hypothesis.
- **re-entry:** the five triggers above, measured by the Steward on a successor freeze over a trailing
  quarter; the question then re-enters the queue with a fresh PREREG, never on a weaker construction.

## Platform issue recommended to the Registrar (DP-48 — filed with a recommendation, decision Haci's)

Recommended id **PI-015**, severity **high**, status **OPEN**. Row for the index table:

| PI-015 | high | OPEN | Projection layer (v1.6 weight 29, the largest) unscored — `available: false` — on 72.2% of published and 74.3% of capped main-lane rows; `overall_score` is a six-layer blend on ~3 of 4 picks |

**Measured numbers, and where the desk read them.** `research/reports/STEWARD_Q035_exposure.md`
(Headline and limbs (a), (c), (f)), on the pinned `manifest_v001`, pick nights 2026-06-01..2026-09-10:
**72.2% of 579** `selected` bull-lane rows and **74.3% of 692** `capped_by_max_output` rows carry
`score: null, available: false, reasons: ["Projection context unavailable"], weight: 0.0` in
`score_details_json.weighted_dimensions.projection`; **not** concentrated in one timeframe (short, swing
and long all 71–79%); read directly off the frozen rows before any Q035 screen touched them. **Second,
independent desk measurement of the same hole:** `research/questions/Q029_layer_value_ablation/PREREG.md`
records `projection_score` non-null on **62.74%** of its segment rows, clearing 70% in **no month
measured** (49.44% → 65.11% peak, plateauing below the floor from July) — which is why Q029 registered
`projection` as **UNEVALUABLE** on its E1 and E2 endpoints. Two questions, two populations, one gap.
*(Related but not new: `smart_money_confirmation_score` is null on 100% of all 6,479 frozen rows — that
is PI-008's weight-0 layer, recorded here only because it is what made Q035's completeness screen
reading-dependent.)*

**Why it is high, and the one thing the check must settle.** The published ranking is produced by a
seven-layer v1.6 blend in which projection carries 29 of 100 points. On roughly three of every four
published picks that layer is absent with `weight: 0.0`. **The desk cannot tell from the frozen payload
alone whether the remaining six weights are renormalized or the layer simply contributes zero**, and the
two have opposite consequences: renormalization means the published ranking is, most nights, a
**six-layer score** that is not the documented v1.6 blend; a plain zero means every affected row is
silently docked up to 29 points relative to the rows that do have projection, so a pick's rank depends
on whether its projection context happened to load. Either way the ranking every subscriber-facing
surface rests on is not the one the weights table describes, and no watchdog fires (PI-002's family).
A second consequence is the desk's: Q035 is deferred because the night's publishable choice set cannot
be reconstructed under a completeness screen when three-quarters of it fails that screen.

**The platform check — repo-only, no database step (DP-49).** Everything below is satisfiable from the
read-only platform repo by the coding agent: (i) trace the writer of `available: false` /
`"Projection context unavailable"` in `services/super_agent_select_scoring.py` (the projection subscore
path around `:925` and the no-projection-origin / no-projection-context branch at `:711-712`) back to
the projection context builder and the `ai_agents/projection_expert` path, and state in the brief which
of three it is — a missing upstream projection row, a config flag or coverage threshold, or an exception
swallowed into the unavailable branch; (ii) `git log --follow` on the projection scoring path, the
projection context builder and the projection agent from 2026-04-01, to date the step-up (the desk's own
two measurements suggest it predates 2026-06-01 and worsens through July); (iii) resolve the
renormalize-vs-zero question **from the code**, and state the answer explicitly; (iv) a pure-function
unit test that feeds a synthetic projection context to the scorer and asserts `available: true` with a
non-null score, plus `git show --stat` proving no other scorer file changed. **The coverage
before/after is the Data Steward's, on the pinned parquet (`manifest_v001`) and the successor freeze
(DP-50(c))** — the brief names that parquet as the before-snapshot and never asks anyone to capture one.

**DP-50(b) ship timing — named, decision left to Haci.** A repair rewrites `projection_score`
historically, and with it every setup label and `overall_score` derived from it. In-flight **locked**
questions that read the projection subscore: **Q029** layer value ablation — `projection_score` is a
Tier-1 layer with its own `E3_projection` endpoint and a **fixed and closed** EVALUABLE / DEAD /
UNEVALUABLE register that its schedule note says is "never revised", decision **2027-04-12**, hard stop
**2027-05-24**; **Q028** layer signal independence — `projection_score` is a Tier-1 column and part of
the object of the test, decision **2026-09-28**, hard stop **2026-10-12**; **Q026** point-in-time
integrity — `projection_score` read in its committed `eval.py`, decision **2026-09-21**, hard stop
**2026-10-05**. Every question that reads `overall_score` or the published slate is touched as well
(Q027 and Q031 share Q029's 2027-05-24 hard stop), because an unavailable layer changes the blend that
produces both. **The constraint the brief should carry: flag-off until 2027-05-24**, the latest in-flight
hard stop — or, if Haci wants it sooner, the repair ships and Q026, Q028, Q029, Q027 and Q031 each split
at the ship date under DP-06 / DP-50(a), which **Q029 cannot absorb** (its register is closed at
`record` and would have to be re-derived, i.e. Q029 defers). The two nearest dates are cheap: **Q026
2026-10-05 and Q028 2026-10-12** pass within a month, after which only the 2027-05-24 cohort binds. This
is the trade-off, stated; the decision is Haci's under DP-48, and the desk files nothing further until
`/desk-run prompt PI-015`.

---

## The headline *(decide pass, 2026-09-14, before R1 — unchanged below this line)*

**The Registrar's §11 item 1 citation is correct, and I checked it line by line at `fa70688`.**
`services/super_agent_select_scoring.py:1509-1548` says exactly what the draft says it says: rows are
sorted `(-overall_score, symbol)` (`:1509`), dropped below `max(timeframe_threshold,
publication_floor)` (`:1518`) and below `min_completeness` (`:1520`), and everything that survives
both and loses **only** to the cap is stamped `qualified = False, selected_rank = NULL,
qualification_reason = 'capped_by_max_output'` (`:1533-1537`). Under DP-28 read verbatim `P_t` is the
published eight and both arms are the same eight rows. **Item 1 is DECIDED the Registrar's way**, and
it is stronger than the draft argues: reading the *caller* (`:1642-1671`) shows the dark lane is
**bear-only** — `_qualify_lane(..., publishable=False)` is invoked on `bear_dark` alone — so DP-28's
stated purpose (dark rows out of every arm) is met by the **lane filter**, not by the reason string,
and no dark row can reach an arm however the reason string reads.

**Reading that same caller found a factual error in the draft that would have broken the universal
arm** (item 2, Correction 1). §2.4 states that `dominant_direction = 'mixed'` rows "cannot enter a
lane and are excluded and counted". The code says the opposite: the main lane is
`[c for c in scorecards if str(c.dominant_direction).strip().lower() != "bearish"]` (`:1643`), whose
docstring reads "every non-bearish candidate (**bullish + mixed**)" (`:1628`). Mixed rows compete for
the same eight slots and can be published. A `P_t` filtered to `'bullish'` is therefore **not the set
the platform chooses from** — which is the one thing §2.2 says the population must be — and the
reconstructed universal slate would differ from the platform's published slate by construction, on
exactly the nights a mixed row held a slot. `P_t` is redefined as the code's main lane, with the
bullish-only variant kept as a printed sensitivity and R1 measuring the mixed/null share before the
lock. This is the second time a desk file has said "bull lane" and meant "non-bearish lane" (the
BACKLOG H-083 entry carries it too).

**Q035 does not lock at `decide`: R1 is blocking, as §5.3 says — but the gate it states is the wrong
gate.** The draft back-solves its lock-or-DEFER thresholds (≥ 0.59 contributing nights, ≥ 0.15
rarest-setup nights per elapsed session) against **its own drafted 136-session window**, so a
measured rate that misses them would send to DEFERRED a question that a longer window reaches. DP-43
says the opposite: the window runs to the earliest date at which **every** floor is projected met, and
DEFERRED arrives only when that date passes the 12-month ceiling. Back-solved against the ceiling — a
2026-09-14 lock, 20 sessions of maturity, a one-week margin, latest admissible decision **Monday
2027-09-13**, last t+20 **2027-09-03** (2027-09-06 is Labor Day), last window end **2027-08-06** —
**225** elapsed sessions are admissible, and the gates become **≥ 0.36** and **≥ 0.09** (Correction 3).
The drafted window still stands if R1 measures at the drafted rates; it moves **out** if they are
slower, and DEFERRED is reached only past 2027-08-06.

**The draft's own date arithmetic is right, and that is worth saying after three questions in a row
where it was not.** Q035's binding maturity is **20** sessions, its endpoint's clock is 20 sessions,
and §5.4 schedules on 20: 2027-03-31 + 20 sessions = **2027-04-28**, + one week = 2027-05-05, first
Monday = **Monday 2027-05-10**, all of it verified session by session here, and the 136-session window
count is exact. Two smaller calendar items are corrected: the extension end is **2027-05-12**, not
2027-05-13 (the draft counted 31 sessions, DP-13 grants 30; the extension **decision date 2027-06-21
is unchanged**), and §6's calendar-half split at "the 63rd elapsed session (≈ 2026-12-14)" is neither
the midpoint nor the date of session 63 — Half A is sessions **1–68**, ending **2026-12-18**.

**Nothing in this question is blocked by the Alpaca / SPY credentials failure that deferred Q032 and
defers Q033's P2** (`STEWARD_Q033_exposure.md` §(f), `STEWARD_Q032_exposure.md` §(g), both today). The
Registrar deliberately took its rule-7 strata from `market_regime_daily` rather than a bar-derived
tape partition, and the successor freeze it needs is **daily-only**. That choice is endorsed and its
one cost is written into item 21: the partition is never re-specified to a bar-only one afterwards.

**Rule 14: no exception is requested and none is needed.** Every input is a 16:05 ET candidate column,
a bar dated ≤ t, or the session t+1 open used only as an entry price; the setup label, the slate and
the entry are all fixed at 16:05 on night `t`. **DP-05 is untouched and DP-41 is not engaged.**

| # | Decision | Bucket | Choice | Basis |
|---|---|---|---|---|
| 1 | `capped_by_max_output` rows in the arms, against DP-28's literal predicate (draft item 1) | DECIDED | **Option A — `P_t` = the rows separated from the published slate by the 8-slot cap alone, `qualification_reason IN ('selected','capped_by_max_output')`, dark and sub-threshold rows out.** Verified against the platform repo at `fa70688`, line by line, rather than accepted: `:1509` the `(-overall_score, symbol)` sort; `:1518` `max(timeframe_threshold, publication_floor)`; `:1520` `min_completeness`; `:1533-1537` the cap branch, which is reached **only** by rows that passed both floors; `:1541-1543` `selected` / `qualified = True`. The deviation is from DP-28's **text**, not its **purpose**, and the purpose is satisfied twice over: `_qualify_lane(..., publishable=False)` — the dark lane — is called on `bear_dark` **only** (`:1658-1671`), so every `selected_dark` row is bearish and item 2's lane filter removes them before the reason string is read. Under Option B both arms are the identical eight rows and H-083 cannot be stated. Kept as **§11 item 1 with the reason in view, and flagged to the Red Team at sign-off** per DP-28's own clause. | **DP-28** read to its stated purpose, with the code at the pinned SHA checked rather than cited; ground 3 (a predicate under which the hypothesis is a tautology is not an option); **DP-25** (the test stays the one H-083 proposed); **DP-50(c)** (read from the read-only repo at `fa70688`, never HEAD) |
| 2 | Which rows the lane actually contains — the draft says `dominant_direction = 'bullish'` and the platform's lane is **non-bearish** | DECIDED | **`P_t` is the code's main lane: `lower(trim(coalesce(dominant_direction,''))) <> 'bearish'`** — bullish, `mixed` and null-direction rows alike — intersected with item 1's reason set and §2.5's screens. §2.4's sentence "`dominant_direction = 'mixed'` rows cannot enter a lane and are excluded and counted" is **struck as false** (Correction 1): `:1643` builds the main lane as every non-bearish scorecard and `:1628` says so in words ("bullish + mixed"), so mixed rows hold published slots today. Three consequences, all applied: the **universal arm is again the platform's own slate**, which is what Gate 0.3 and R1(f) exist to verify and what a `'bullish'`-only filter would have silently broken; §4.3 gains a **printed per-slate `dominant_direction` composition** and a **bullish-only descriptive sensitivity of both primaries** that decides nothing; and **R1 gains a limb** measuring the mixed/null share of `P_t` and of the published slate before the lock, so the Red Team sees its size. The bear lane and the bear-dark lane are untouched and byte-identical in both arms. | ground 3 — the population of a question about *which eight of a set* must be the set the platform chooses from, and §2.2 says so itself; the code at `fa70688` (`:1628`, `:1642-1649`) against the draft's assertion; **DP-26** (a lock-time convention corrected before any outcome exists); **DP-28** (the dark lane stays out, by the stronger mechanism) |
| 3 | Whether the fitted arm P1 is registered at all (draft item 2) | DECIDED | **Option A — both primaries, `m = 2`: P1 the fitted ranker as H-083 filed it ("fitted once, frozen in the PREREG, tested only on prospective nights") and P2 the parameter-free `w ≡ 1` ranker.** Dropping P1 would re-write the hypothesis (DP-25), and `m = 2` makes the BH correction **stricter** for both, never looser. One containment clause is added, carrying Q034 DECISIONS #2's principle to the one place it reaches here: **`fit.py` writes the selected triple and the 125-cell grid objective and nothing else** — no per-night value, no per-arm touch rate, no `R_pool`, no per-symbol row, no panel — `results/fit_grid.json` is sealed with the rest of `results/` (rule 3), carries `NON_QUOTABLE`, is never ledgered as a finding and never quoted, and **no other question's registered endpoint is computed on the sealed nights**. §5.4's "no sealed-period panel for either primary" stands and is the reason this is a clause rather than a refusal: Q035's `Δ_t` is an endpoint no locked question owns. | **DP-25** (units and cuts from the hypothesis as filed; a re-unit is a new hypothesis); rule 9; rule 3; **Q034 DECISIONS #2** (nothing computed on sealed nights that belongs to a question still in flight — applied to its limit, not beyond it); **DP-45** (`m = 2` corrects harder than `m = 1`) |
| 4 | The uniform target level (draft item 3) | **DEFAULTED (R-2)** | **Option A — `H_i = C_t,i + 2.0 × ATR14_t,i` decides; the 1.0 ATR and 3.0 ATR versions are pre-declared descriptive sub-rows that decide nothing in any branch.** H-083's own level is the **printed L3**, which does not exist for a promoted row, so DP-42's first clause ("the level the hypothesis names") has nothing to name and its fallback names the same unavailable level; the choice of multiple is therefore not settled by policy and is defaulted. 2.0 ATR is taken because the three levels must be fixed before any of them is seen (rule 3) and because 1.0 ATR sits inside ordinary post-selection noise where H-053 expects no selection signal at all. **R1 gains a non-gating limb** reporting the distribution of the printed swing-L3 distance in ATR units, for the record and for §10 threat 3 — it **does not move the registered level in any branch**, whatever it shows. | **DP-42** (the hypothesis's own level, where it exists — here it does not, for half the population); **DP-40** (the Registrar's recommendation where no DECIDE ground reaches it); **DP-26**; rule 3; not taken: 1.0 ATR — nearer the printed L1/L2 band, inside ordinary noise |
| 5 | What the 2.0 ATR is measured **from**, which the draft states two different ways | DECIDED | **The level is anchored at the pick-night close: `H_i = C_t,i + 2.0 × ATR14_t,i`, entered at the session t+1 open, for every row in both slates and all four baselines.** §3's closing sentence — "every row … is asked to travel **2.0 of its own ATRs, on the same clock, from the same entry**" — is **struck as inaccurate** (Correction 2) and replaced with what the construction does: *reach a level 2.0 of its own ATRs above its own pick-night close, on the same 20-session clock, entered at the same session t+1 open.* The `C_t` anchor is kept because it is the only one fixed at 16:05 knowledge time, it cannot be moved by the overnight gap, and it matches how the platform writes its own ladders; the gap is then part of the measured path on **both** arms, drawn from the same pool, so it confounds nothing between them. `open_{t+1} ≥ H` stays **not a hit** with a printed `GAPPED_THROUGH` tally (DP-26), and §4.3 gains a **pre-declared descriptive companion** with the level anchored at the t+1 open instead, which decides nothing. | ground 3 — a stated construction and its formula must agree; **DP-26** (the anchor is a lock-time convention derived from no outcome, and it is not moved at the decision pass); **DP-11** correctly **not** fired (nothing here is a position already held) with **DP-03(b)** the entry; rule 5 (one basis on both sides) |
| 6 | Lane scope (draft item 4) | DECIDED | **Option A as corrected by item 2 — the re-ranking runs inside the platform's **main (non-bearish) lane** only; the bear lane and the bear-dark lane are untouched, byte-identical in both arms, and nothing in this question speaks to bear picks (§10 threat 11).** Option B (one setup model across both lanes) is refused on the code: the lanes carry separate thresholds (`bear_publish_threshold`) and separate caps (`bear_max_output_cap`) and are qualified by independent `_qualify_lane` calls with independent rank counters (`:1644-1671`), so a cross-lane re-rank would let a change in **direction mix** produce a verdict about **ranking** — H-062's live confound. | ground 3 (the lanes are independently capped and thresholded in the code at the pinned SHA); **DP-26**; H-062; §10 threat 11, which already states the cost |
| 7 | A ranker that seldom reorders (draft item 5) | DECIDED | **Option A — reorder rate < 0.25 ⇒ that primary is INCONCLUSIVE, labelled `NO_ROOM_TO_REORDER`; the reorder rate, the mean names swapped and the `\|P_t\|` distribution print in every branch.** The two options differ only in strictness — A converts a would-be NULL into a no-claim and can never make a CONFIRMED easier — so the stricter is taken without asking. The Registrar's reason is the right one and is kept: a NULL would be read as "setup ranking does not help" when the measurement says the ranker barely ran. **0.25 is fixed at this lock and is not lowered at the decision pass in any branch.** | **DP-45** / the standing rule that where two options differ only in strictness the stricter is taken; rule 6's own shape ("positive but below MPE is INCONCLUSIVE"); **DP-26** (threshold fixed before the run); **Q034 DECISIONS #5**, **Q005 / Q026 / Q028** (a threshold fixed at draft and never adjusted afterwards) |
| 8 | Nights on which the two slates come out identical (draft item 6) | DECIDED | **Option A — such a night contributes with `Δ_t = 0`; the restricted "reordered nights only" endpoint prints as a descriptive companion and decides nothing.** The product question is whether the architecture improves the **published slate**, and a night it leaves untouched is a night with no improvement; Option B would let a ranker that moves three nights in ten be reported as though it moved ten. A is also arithmetically the conservative side — the zeros dilute `mean_t(Δ_t)` toward zero, the direction that cannot manufacture a positive — and it keeps the denominator independent of the ranker's own behaviour. | ground 3 — an endpoint whose denominator is conditioned on the treatment having acted is not an estimate of the treatment's effect; **DP-45**; **Q033 DECISIONS #2** (the same denominator discipline, same day) |
| 9 | The fitted arm's training window (draft item 7) | DECIDED | **Option A — pick nights 2026-06-01 .. the last night whose session t+20 falls on or before the pinned price freeze's last bar date, derived by `fit.py` from the pinned calendar (today that is **2026-08-12**, exactly t+20 = 2026-09-10 with 2026-09-07 Labor Day skipped — verified here session by session); a night short of t+20 is dropped and counted.** Option B (the desk's pre-2026-06-01 in-sample split, as H-083's line words it) is refused on DP-06: setup C reads the catalyst layer, which is a **different feature** before the 2026-06-01 earnings fix `69ef05f`, so B would fit one of the three setups on a feature the test window does not contain. Stating the end as a **derived quantity** rather than a hard-coded date (Correction 10) is deliberate — the draft's 2026-08-12 is correct only because the freeze ends 2026-09-10, and a hard-coded date would silently include a right-censored night if that ever changed. | **DP-06** (Confirmed — the catalyst layer splits at 2026-06-01); **DP-25** (H-083's own wording yields to a Confirmed entry, and the substitution is recorded in §11 rather than made silently); ground 3 (a maturity boundary is computed from the calendar, not asserted) |
| 10 | What the `FIT_RETURNS_UNIVERSAL` branch produces — the draft calls it NULL | DECIDED | **INCONCLUSIVE, not NULL** (Correction 6), labelled `FIT_RETURNS_UNIVERSAL`, `HISTORICAL_ONLY` and `NON_QUOTABLE`; P1 leaves the F8 correction set and `m` drops to 1; **P2 is unaffected and the window runs in full**. A NULL is a substantive claim — "the fitted ranker picks the same eight, as well as any setup ranker does" — and in this branch **no test night has been read at all**: the shrinkage guard fired on ~50 **training** nights with no CI, no episode CI, no q, no floors and no prospective exposure. Ledgering that as NULL would put "a fitted setup ranker does not help" in the desk's memory on the strength of a grid search. §9's NULL consequences (retiring EN-018's ranking half, the "defended design decision" sentence) therefore fire only on a **measured test-window** NULL — in this branch, on P2's. DP-31's successor-question clause resolves to **P2 itself**, which carries the prospective track on the same nights, so no successor PREREG is owed. | rule 10 (four verdicts, and INCONCLUSIVE is the one that claims nothing); rule 6's shape ("below MPE is INCONCLUSIVE, not CONFIRMED" — read symmetrically, a training-window shortfall is not a NULL); rule 3; **DP-31** (the label travels wherever the verdict is restated; its successor clause is satisfied by P2); **DP-45** (the reading that supports no claim) |
| 11 | When `eval.py` and `fit.py` are committed, and where the artefact hash lives | DECIDED | **Both are written once (rule 9) and committed no later than **Monday 2026-10-05**, and `eval.py` is committed **before `fit.py` is run**; both sha256s are recorded and neither file is touched afterwards — the extension run uses the byte-identical files.** Two grounds, and the second is specific to this question: §4.5 requires `fit.py` to apply §2.2's filters, §2.3's labels, §2.5's screens and §4.1's level and clock **on the identical code path**, so writing `eval.py` afterwards means writing it with the fit's output in view — which is precisely what rule 9 forbids; and 2026-10-05 is the day **Q006** decides, the first sibling verdict on the published slate's path edge, with Q002 following 2026-10-12. The artefact's hash is recorded in a committed sidecar, **`research/questions/Q035_setup_architecture/setup_model_v001.sha256`**, written by the Researcher at the fit run — **not** in the locked PREREG and **not** by editing this file (rule 3, DP-22) — and `eval.py` fails loudly on any other hash. **If no artefact hash exists on 2026-10-05, P1 is demoted to descriptive** (§4.5's registered fallback) and the demotion is recorded by the Registrar in `schedule.json` that day, before any in-window night has matured to t+20 (the first, 2026-09-15, matures ≈ 2026-10-13), so the demotion is blind. | rule 9 (a deterministic script written once, no tuning while looking) read at its strongest; rule 3; **DP-22** (a locked file is not edited — hence the sidecar); **Q033 DECISIONS #14**, **Q034 #16** (the same deadline discipline, here earlier because this question's own fit runs first) |
| 12 | The trading calendar, and the length of DP-13's single extension | DECIDED | **The desk's standard holiday list, which §5.4 states nowhere: 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, 2027-06-18, 2027-07-05 and 2027-09-06** (the last three for the extension path and the ceiling back-solve) — Correction 9. On it, three arithmetic results, each verified session by session here: the window **2026-09-15 .. 2027-03-31 is exactly 136 elapsed sessions**; **t+20 of 2027-03-31 is 2027-04-28** and the decision date **Monday 2027-05-10** is right, which is worth stating after Q032, Q033 and Q034 each scheduled on the wrong maturity; and **DP-13's +30 sessions from 2027-03-31 is 2027-05-12, not the draft's 2027-05-13** (that is session 31), so the extension window ends **2027-05-12** with daily bars through **2027-06-10** (Correction 4). The extension **decision date, Monday 2027-06-21, does not move** — t+20 of 2027-05-12 is 2027-06-10, + one week = 2027-06-17, first Monday on or after = 2027-06-21. Every date is re-confirmed session by session by the Steward when the freeze is built, and a correction may move a date **out, never in**. | ground 3 — one calendar, and a date arithmetic that miscounts a session is simply wrong; **DP-13** (the extension is +30 sessions, a fixed quantity, not "about thirty"); **DP-45** (no correction shortens the schedule); **Q033 DECISIONS #7**, **Q034 #6** (the same list, the same day) |
| 13 | Which measured rate the schedule is built on | DECIDED | **The scheduling rate is `min(r_Q035 , 0.6620)`**, where `r_Q035` is R1(a)'s contributing-night rate **under §2.6's own rule** (a non-excluded, corroborated night with `\|P_t\| ≥ 1` after §2.2's filters and §2.5's screens, and ≥ 1 row gradeable at 2.0 ATR on the 20-session clock) with numerator and denominator counted over the same period, and **0.6620** is the desk's measured published-pick contributing rate (47/71, `STEWARD_Q031_exposure.md` §(a), reconfirmed bit-for-bit today in `STEWARD_Q033_exposure.md` §(a)(ii)). The cap is the binding half and it binds in an unusual direction here: Q035's night rule is **weaker** than the funnel 0.6620 was measured on (no `d_L3` bound, no ladder requirement, no ≥ 5-control clause), so `r_Q035` will almost certainly measure **faster** — and the faster number changes no date. **No date is ever computed from a rate faster than the desk's own measured published-pick number** (§5.2's own 0.6620 × 136 ≈ 90 projection is therefore kept, not improved), and a measured rate **slower** than 0.6620 governs and moves every date out. | **DP-43** (dates projected from the Steward's exposure count at the measured run-rate); **DP-45** (the `min`, never the faster rate); ground 3 (numerator and denominator over the same period); **Q033 DECISIONS #6**, **Q034 #8** — the identical construction, adopted rather than re-argued |
| 14 | The lock-or-DEFER thresholds, which the draft back-solves against its own window | DECIDED | **The rate limbs are back-solved against DP-43's ceiling, not against the drafted window: contributing nights ≥ 0.36 and rarest-setup nights ≥ 0.09 per elapsed session** (Correction 3), replacing §5.3's ≥ 0.59 and ≥ 0.15. The arithmetic, re-solved from the calendar: a 2026-09-14 lock gives a 12-month ceiling of 2027-09-14, so the latest admissible decision is **Monday 2027-09-13**, whose t+20 must fall on or before **2027-09-03** (2027-09-06 is Labor Day), back-solving to a last admissible window end of **2027-08-06** and **225** admissible elapsed sessions from 2026-09-15; 80 ÷ 225 and 20 ÷ 225, rounded **up**. The drafted thresholds would have sent to DEFERRED a question that a longer window reaches, which DP-43 forbids — it names the window that reaches **every** floor and reserves DEFERRED for the case where that date passes the ceiling. **The testability limbs are unchanged and stay as drafted** (median `\|P_t\| ≥ 11` with `\|P_t\| ≥ 9` on ≥ 80% of nights; reorder rate ≥ 0.50; margin share ≥ 0.60 with ≥ 4 varying layers on ≥ 80% of nights; reconstruction agreement ≥ 0.90): those are not sample-rate gates but conditions for the ranker to have been tested at all, and they are **not** relaxed by a longer window. Any limb short ⇒ DEFERRED with the measured number named; no floor is reduced and the partition is never re-specified. | **DP-43** (the window runs to the date every floor is projected met; the 12-month ceiling is the DEFERRED trigger, not a drafted window); **DP-21**; **DP-24**; **DP-26** (the testability thresholds are lock-time conventions and stand); **Q033 Correction 3**, **Q034 Correction 2** (the same back-solve, on this question's own maturity) |
| 15 | What a floor shortfall does — §8's last clause and Gate 0.2 give two different answers | DECIDED | **Resolved in the strict direction, in three parts** (Correction 7). (i) **Any** floor short at the initial decision date fires the **single automatic DP-13 extension** on the counts `eval.py` prints — more waiting, never a relaxed test, never a second extension. (ii) After it: **floor A short (< 80 contributing nights per primary) ⇒ DEFERRED**, as §8 says — the endpoint is under-powered and there is nothing to report. (iii) After it: **a setup short of 20 (floor B) or a calendar half short of 20 (floor C) does not defer the question and does not reduce the floor** — the short cell is SUPPRESSED and **named in every restatement**, the register runs, and **no primary may be PROSPECTIVELY_CONFIRMED**, ceiling INCONCLUSIVE, labelled **`PARTITION_INCOMPLETE`** (floor B) or **`HALF_INCOMPLETE`** (floor C). Two of three setups short stays `PARTITION_COLLAPSED` as drafted. NULL, INCONCLUSIVE and `SETUPS_WORSE` remain reachable in those branches — H-083's FAIL branch is a real finding and a confirmed negative retires a product change, neither of which can be bought with a shortfall — while the affirmative branch is not. §8 clause 1 already requires all four floors for CONFIRMED, so (iii) removes nothing and only says which floors defer and which merely block. | **DP-43** (demotion settled at lock and never at the decision pass); **DP-13** (one automatic extension on measured counts); **DP-21** (no floor moved in either direction); **DP-45** (of the available readings, the one that cannot let a missing cell produce a winner); **Q034 DECISIONS #14**, the identical contradiction resolved the identical way, same day; ground 3 (a draft that says both things must be made to say one) |
| 16 | The sub-cell suppression list | DECIDED | **Fixed at this lock as §4.3 and §4.5 list it, revised once at `record` from R1's measured counts, then closed — and the revision may only move cells ONTO the list, never off it.** Suppression restricts **affirmative reporting only**: it never removes a blocker. The three setups, the two calendar halves, the reorder rate, `R_pool`, the `GAPPED_THROUGH` tally, the B2 and B3 blocking companions and both primaries are **never** on the list and block at whatever count they have. A cell suppressed at lock stays suppressed even if it clears 20 measured nights at the decision pass; a cell not suppressed still needs ≥ 20 **measured** contributing nights to print. Q035's suppressions are **structural** — the Elite 90+ tier against PI-010's 2–3 elite picks a month (§4.3 row 5), the per-setup × tier cells, the `O` bucket's own rows — not density expectations R1 can overturn. | **DP-21** (20 per reported cell, never moved); **DP-45** (the stricter of two readings); **Q033 DECISIONS #10**, **Q034 #13**, **Q027 Correction 2** ("suppression never removes a blocker", in the same words) |
| 17 | The family, and F8's correction set | DECIDED | **F8 as filed (DP-29 — the primary's subject is the selection architecture), `m = 2` within the question, and §7's "F8 correction set at this lock: 4" is corrected to **3** — Q033's P1 plus Q035's P1 and P2 — **4 only if Q033's SPY-history limb clears at its lock**, which today's evidence says it will not** (Correction 5). Q030/H-074 and Q032 are DEFERRED and their primaries are out of the set while deferred (the H-062 / Q025 precedent); Q033's P2 is deferred on the same absent credentials under its own item 16; Q026, Q028 and Q034 are diagnostics with no primary, no MPE and no q. Because a **smaller** set is the looser direction for BH, two clauses bind: the set is **re-counted at the decision pass over every F8 primary that has produced a p**, and **Q035 never quotes a q computed on a set smaller than that count** — a primary that returns to the set (Q033's P2, Q030, Q032) enlarges it and is never omitted to reach a q. | rule 8; **DP-29**; **Q034 Correction 6** (the same count, corrected the same day, on the same evidence); **Q033 DECISIONS #4**, **Q032 #10**; **DP-45** (the correction set is never the smaller of two readings at the decision pass) |
| 18 | Exclusions, inside a window every night of which postdates every existing freeze | DECIDED | **As drafted, and verified: `eval.py` unions **`research/data/exclusions_v003.json`** — confirmed the newest file on disk (v001, v002, v003 present) — with the **add-only successor exclusions file** issued with the successor selection freeze, on the identical **four** criteria (`manual_runs` ∪ `non_session_runs` ∪ `uncorroborated_publication_runs` ∪ `payload_disabled_runs`), applied to nights after 2026-09-10.** The successor file may only **add** nights; no night is removed from a v003 list; the **criteria** are fixed at this lock even though the **dates** cannot be; `exclusions_v003.json` is not edited (`research/data/` is not writable from here); both paths are `eval.py` inputs with no hard-coded file name and no hard-coded date; DP-04 applies mechanically on top. The fourth criterion is load-bearing in the same way it is for the siblings: `STEWARD_Q033_exposure.md` §(a) shows every published row of 2026-06-02 carrying `analysis_status = "disabled"`, and such a night is excluded whole rather than entering as a zero. | **DP-22** read as "one list, one set of criteria" (its "cite the newest file" clause presumes a sealed window; Q035's is entirely post-freeze); **DP-04**; **Q033 DECISIONS #11**, **Q034 #11**, **Q032 #8**, **Q031 #12** — same construction |
| 19 | A mid-window change to the scoring engine, and the constraint running the other way | DECIDED | **§2.7's split list stands as drafted and gains the DP-50(b) half it is missing** (Correction 8): every quantity it names — `qualification_threshold`, `publication_floor`, `max_output_cap`, `min_completeness`, `bear_publish_threshold` / `bear_max_output_cap`, `scoring_weights`, `timeframe_weight_multipliers`, `timeframe_thresholds`, `conflict_penalties`, any layer's scoring function, any layer enable-flag, **including any promotion of v1.7** — is **flag-off until 2027-05-10** (**2027-06-21** if the extension fires; recomputed out if the window moves), checked before any fix brief is written. A change that does ship **cuts the window at the ship date**: the post-ship segment becomes the question's window with the §5 schedule recomputed from it (out, never in; same single extension; ceiling measured from the original lock), the pre-ship segment is a labelled descriptive panel entering no verdict, and if neither segment reaches the gates inside the ceiling Q035 is DEFERRED. `eval.py` prints the per-night `config_json` composition and **fails loudly** rather than silently excluding. **R1 limb (g) is cited, not re-run:** `STEWARD_Q033_exposure.md` §(e) (today) reports HEAD `d19c9a9`, `services/super_agent_select_scoring.py` last touched by `1765a6f` on 2026-07-07 — **before** the pin — none of the four commits since `fa70688` touching it or `super_agent_select_models.py`, the explicit answer **"NONE"**, and no v1.7 promotion scheduled anywhere because no start date exists. §2.7's "a change to the candidate universe builder does not split this window" is correct and stands. | **DP-06** / **DP-50(a)** (a repair or config change splits a column into two features at the ship date); **DP-50(b)** (ship timing checked against in-flight questions, the PI-011 / Q010 pattern); **DP-50(c)** (swept on the pinned freeze and the read-only repo); ground 2 — a limb measured today under the identical definition is cited rather than re-run (**Q034 DECISIONS #17**); **Q033 DECISIONS #12**, **Q034 #12** |
| 20 | The rule-7 stratification, and the guard it is missing | DECIDED | **As drafted — `market_regime_daily` regime on night `t` under the Q023 / Q032 §(d) legality test verbatim (a v1.2 row dated `t`, not `unknown`, not `insufficient`, `created_at` dated `t` and ≤ that night's `sas_runs.finished_at`), descriptive, with nights failing the test reported in a `REGIME_UNLABELLED` stratum and never dropped from a primary — plus one addition: `eval.py` **fails loudly** if an in-window night's `regime_version` is not v1.2.** A scorer repair makes the label two features (DP-06 / DP-50(a)) and the guard is the cheap way to see it. **No primary is defined per regime**, so a repair to that column can move a descriptive stability row and can never move a verdict; the binding stability check stays the calendar halves (§8 clause 6). The window begins 2026-09-15, well after the 2026-06-09 point-in-time boundary, so CLAUDE.md's backfill caveat does not reach it. | rule 7; **DP-06 / DP-50(a)** (the v1.2 guard); **DP-26** (the legality test is a lock-time convention); **Q034 DECISIONS #3(i)** (the same legality test and the same guard, same day); **Q033 DECISIONS #12** (a regime-scorer change splits a descriptive companion only) |
| 21 | The Alpaca / SPY provisioning blocker, and what it costs this question | DECIDED | **It costs this question nothing, and no probe limb is added: `STEWARD_Q033_exposure.md` §(f) and `STEWARD_Q032_exposure.md` §(g) (both 2026-09-14, `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` absent, no probe attempted, no pinned alternative) are cited for the record.** Q035 assigns no arm and defines no stratum from a bar-derived tape partition — §6 takes its strata from `market_regime_daily` — and its successor price freeze is **daily-only, candidate symbols only**, so nothing here depends on SPY history no manifest holds. The Registrar's choice to avoid the bar-only partition is endorsed, and its price is registered rather than left implicit: **the stratification is never re-specified to a bar-only tape partition after this lock**, in any branch, including one where the credentials arrive tomorrow — that would be an arm chosen after the data existed. | ground 2 — a provisioning limb answered for the desk today under the identical definition is cited, not re-routed (**Q034 DECISIONS #17**); **DP-43** (a question defers on a measured ground, and this ground does not reach these endpoints); **DP-26** (the partition is fixed at lock and does not move); **Q030 / H-074**, **Q032 headline**, **Q033 #16** |
| 22 | Where the calendar halves split | DECIDED | **Half A = elapsed sessions 1 .. ⌈N/2⌉ of the final window, Half B = the rest, `N` derived by `eval.py` from the pinned session calendar; on the drafted 136-session window Half A = **2026-09-15 .. 2026-12-18** and Half B = **2026-12-21 .. 2027-03-31**; extension nights join Half B; on the extended 166-session window the same rule re-cuts at session 83.** §6's "the 63rd elapsed session (≈ 2026-12-14)" is **struck**: 63 is not the midpoint of 136, and session 63 is 2026-12-11, not 2026-12-14 (which is session 64) — the figure is wrong twice over (Correction 15). The split is registered as a **rule on the session index**, not a date, because the window end is provisional until `record`. | ground 3 — a stated split must be reproducible from the calendar, and this one is neither the midpoint nor the date it names; **DP-26** (the session-index split is the desk's standing convention, fixed at lock); **Q033 DECISIONS Schedule**, **Q034 Schedule** (the identical session-index rule) |
| 23 | The MPE, the entry basis and the clock | DECIDED | **MPE ±5.0 pp on both primaries, two-sided, and not lowered at the decision pass in any branch; entry the **session t+1 official 09:30 ET open** for every row of both slates and all four baselines; clock **20 sessions from entry**.** The endpoint is a within-night control-adjusted touch-rate difference, which is DP-20's own case, and DP-44 routes it there explicitly; **no larger MPE is proposed** (DP-20 permits one only with a stated reason, and the Registrar gives none) and a smaller one is never accepted. The 12.5 pp granularity of an 8-name slate is a §10 threat, printed, and **not** a reason to move the bar. The entry is DP-03(b) and is **forced**, not chosen: a promoted name has no publication event and no after-hours print, and rule 5 requires one basis on both sides — **DP-11 is correctly not fired** (nothing here is a position already held). The clock is DP-09's 20 sessions on DP-42's swing default. **No MPE is invented in money or session units**; sessions-to-touch stays descriptive. | **DP-20** (+5.0 pp, the base value for a control-adjusted touch rate); **DP-44** (touch-rate endpoints use DP-20; no money-unit MPE; sessions-to-touch descriptive); **DP-03(b)**, **DP-11** (considered and not applicable), **DP-42**, **DP-09**; rule 5; rule 6 |
| 24 | Window end, decision date, extension, hard stop | **DEFAULTED (R-3)** — provisional; final at `record` on R1 | **Window: pick nights 2026-09-15 .. 2027-03-31 = 136 elapsed sessions** (verified exactly here; unchanged unless R1's measured rates push it **out**). **Decision date: Monday 2027-05-10** — 2027-03-31 + **20 sessions maturity** = 2027-04-28, + one calendar week = 2027-05-05, first Monday on or after. **Single DP-13 extension of +30 sessions** to pick nights .. **2027-05-12** (Correction 4, not the draft's 2027-05-13), decided **Monday 2027-06-21**, **which is also the hard stop** — still short there, Q035 goes to DEFERRED. **7.9 months** and **9.2 months** from the 2026-09-14 lock, both inside DP-43's ceiling with more room than any sibling on the board. The **method** is fixed here and is not re-argued with counts in view: window end = the **latest** of floor A (80 contributing nights per primary; at the capped rate, session 121 = 2027-03-09), floor B (20 contributing nights in the **rarest setup**, unmeasured today and the one that can bind), floor C (20 per calendar half) and floor D (30 post-lock nights, satisfied by construction) at item 13's rate; then + 20 sessions + one week, first Monday, moved out again for a holiday; capped at the last admissible end **2027-08-06** (item 14), beyond which the answer is DEFERRED. Every date moves **out** if R1 measures slower and **never in** if it measures faster. | **DP-43** (the window that reaches every floor at the measured rate, plus the endpoint's maturity and a one-week margin, first Monday on or after; +30-session extension; the 12-month ceiling); **DP-13**; **DP-21**; **DP-24**; **DP-45** (out only; never the shorter window, never the faster rate); not taken: the drafted dates read as final, with a gate that would have deferred at 0.59 |
| 25 | The exposure counts this question has never had | **CLOSED at `record` → DEFERRED** | **R1 answered in full, `STEWARD_Q035_exposure.md` 2026-09-14. (a) 0.5775 PASS · (b) 0.0845 SHORT on the governing full-window reading · (c) median 5 / 31.7% SHORT · (d) 0.2683 SHORT · (e) 0.615 / 85.4% PASS · (f) empty population, 0.00 proxy SHORT · (g) NONE PASS. The pre-fixed branch fires: any limb short ⇒ DEFERRED with the measured number named. (c), (d) and (f) are testability limbs — DP-13 does not apply and no window reaches them; (b) independently projects floor B at ≈ 237 sessions against DP-43's 225-session ceiling.** See the RECORD section. *Routed text as issued, kept for the record:* waits on **R1** (counts only) — **BLOCKING FOR LOCK**, as §5.3 says, and blocking on a limb no desk report has measured: how the reorder room splits three ways. It settles item 24's dates whole and the lock-or-DEFER gate itself — contributing nights **≥ 0.36** and rarest-setup nights **≥ 0.09** per elapsed session (item 14, re-solved at `record` from the calendar), plus the unchanged testability limbs. All limbs clear → Q035 locks with §5.2 recomputed **out**; any limb short → **DEFERRED** with the measured number named, never a re-specified partition and never a reduced floor. | — |
| 26 | Successor freezes | **WITHDRAWN at `record`** | **No freeze is built for Q035: it is DEFERRED and has no decision date to build toward.** Q027, Q029, Q031, Q033 and Q034's successor freezes are unaffected — Q035's scope was a subset of that build, never its driver. Re-issued only if the re-entry triggers are met and a fresh PREREG is registered. *Routed text as issued, kept for the record:* waits on **R3** — a successor **selection** freeze (`sas_candidates` **every row, published and unpublished**, `sas_runs`, `market_regime_daily` with `created_at` and `regime_version` preserved) and a **daily-only** price freeze for **every candidate symbol on every in-window night**, plus the add-only successor exclusions file. Due before the decision date; **not a blocker for lock** (DP-23). Scope and horizon fixed at `record` from item 24. **Q035's requirement stands on its own even if Q033 and Q034 defer** — it is a subset of their build today, not a dependency on it. | — |
| 27 | `fit.py`, `eval.py` and the frozen artefact | **WITHDRAWN at `record`** | **Neither script is written, no fit is run, no `setup_model_v001.json` is produced and no sha256 sidecar is committed; the Monday 2026-10-05 deadline is void.** A deferred question runs nothing (rule 3, rule 9). *Routed text as issued, kept for the record:* waits on **R2** (post-lock; **not** a lock blocker) — both scripts written once (rule 9), `eval.py` committed **before** `fit.py` runs, both by **Monday 2026-10-05**; `fit.py` run after the lock commit on item 9's training window; `setup_model_v001.json` produced and its sha256 committed to the sidecar (item 11); the `FIT_RETURNS_UNIVERSAL` branch reported as fired or not. §4.5's fallback covers failure and item 11 fixes what happens if the deadline passes. | — |

## Corrections to silent choices

**Fifteen.** The Registrar applies them at `apply` with the rest of this file. Every one strikes a
statement the code or the calendar contradicts, moves a date out, or tightens a clause; none weakens a
floor, an arm, an MPE or a gate.

1. **§2.4 and §2.2's SQL — "`dominant_direction = 'mixed'` rows cannot enter a lane" is false, and the
   arms are built on the wrong population.** `services/super_agent_select_scoring.py:1643` builds the
   main lane as every **non-bearish** scorecard and `:1628` says "bullish + mixed" in words; mixed and
   null-direction rows hold published slots. **Must read:** `P_t`'s direction filter is
   `lower(trim(coalesce(dominant_direction,''))) <> 'bearish'`; §2.4's mixed-row sentence is struck and
   replaced by the statement that the main lane is the non-bearish lane and the bear and bear-dark
   lanes are untouched; §4.3 gains the per-slate `dominant_direction` composition and a bullish-only
   descriptive sensitivity of both primaries; R1 measures the mixed/null share of `P_t` and of the
   published slate before the lock. (item 2.)
2. **§3's closing sentence misstates the construction.** It says every row is asked to travel "2.0 of
   its own ATRs … from the same entry"; the level is anchored at `C_t` and the entry is the t+1 open.
   **Must read:** *reach a level 2.0 of its own ATRs above its own pick-night close, on the same
   20-session clock, entered at the same session t+1 open* — with the `GAPPED_THROUGH` tally and a
   pre-declared open-anchored descriptive companion in §4.3. (item 5.)
3. **§5.3's lock-or-DEFER rates are back-solved against the drafted window, not DP-43's ceiling.**
   **Must read:** contributing nights **≥ 0.36** and rarest-setup nights **≥ 0.09** per elapsed
   session — 80 ÷ 225 and 20 ÷ 225, rounded up, on the **225** elapsed sessions still admissible at a
   2026-09-14 lock with 20 sessions of maturity and a one-week margin (latest decision Monday
   2027-09-13, last t+20 2027-09-03, last window end 2027-08-06) — **re-solved at `record` from the
   trading calendar**. The testability limbs (c)–(g) are unchanged. (item 14.)
4. **§5.4 and the header — DP-13's extension is 30 sessions and the draft counts 31.** **Must read:**
   extension window end **2027-05-12** (not 2027-05-13) with successor daily bars through
   **2027-06-10** (not 2027-06-11); the extension decision date **Monday 2027-06-21 is unchanged**.
   (item 12.)
5. **§7's "Family F8 correction set at this lock: 4" is no longer true on the day it is written.**
   **Must read:** **3** — Q033's P1 and Q035's P1 and P2 — **4 only if Q033's SPY-history limb clears
   at its lock**; Q030/H-074 and Q032 are DEFERRED and out while deferred, Q033's P2 is deferred on the
   same absent credentials, and Q026/Q028/Q034 are diagnostics; the set is **re-counted at the decision
   pass** over every F8 primary that produced a p and **no q is ever quoted on a smaller set**.
   (item 17; Q034 Correction 6, same day.)
6. **§4.5's `FIT_RETURNS_UNIVERSAL` branch closes P1 as NULL on training data.** **Must read:**
   **INCONCLUSIVE**, labelled `FIT_RETURNS_UNIVERSAL`, `HISTORICAL_ONLY` and `NON_QUOTABLE`; P1 leaves
   the correction set and `m` drops to 1; §9's NULL consequences fire only on a measured **test-window**
   NULL; DP-31's successor clause is satisfied by P2, which carries the prospective track. (item 10.)
7. **§8's "A floor shortfall is never INCONCLUSIVE … still short after the extension ⇒ DEFERRED"
   contradicts Gate 0.2's suppressed-stratum handling.** **Must read:** one automatic extension first,
   on measured counts; then floor **A** short ⇒ DEFERRED, while a short setup (**B**) or a short half
   (**C**) is SUPPRESSED and named, the question runs, and **no primary may be CONFIRMED**
   (`PARTITION_INCOMPLETE` / `HALF_INCOMPLETE`); two of three setups short stays `PARTITION_COLLAPSED`.
   No floor is reduced in any branch. (item 15.)
8. **§2.7 registers only half of DP-50 — the split rule, not the flag-off constraint.** **Must read:**
   every quantity §2.7 lists is **flag-off until 2027-05-10** (2027-06-21 on the extension path;
   recomputed out if the window moves), checked before any fix brief is written; and R1 limb (g) is
   **cited from `STEWARD_Q033_exposure.md` §(e)** — HEAD `d19c9a9`, scoring module last touched
   2026-07-07 before the pin, explicit answer "NONE", no v1.7 schedule — rather than re-run. (item 19.)
9. **§5.4 states no holiday list.** **Must read:** 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18,
   2027-02-15, 2027-03-26, 2027-05-31, 2027-06-18, 2027-07-05 and 2027-09-06 (the last three for the
   extension path and the ceiling back-solve), re-confirmed session by session by the Steward at the
   freeze build; a correction may move a date **out, never in**. (item 12.)
10. **§4.5 hard-codes the training window's end date.** **Must read:** 2026-06-01 .. **the last pick
    night whose session t+20 falls on or before the pinned price freeze's last bar date**, derived by
    `fit.py` from the pinned calendar — today **2026-08-12**, verified here as exactly t+20 = 2026-09-10
    — with any right-censored night dropped and counted. (item 9.)
11. **§4.5 records the artefact's sha256 "in `DECISIONS.md`", which is written before the fit exists
    and is not edited afterwards.** **Must read:** the hash is committed by the Researcher to
    **`research/questions/Q035_setup_architecture/setup_model_v001.sha256`** at the fit run, `eval.py`
    fails loudly on any other hash, and neither the locked PREREG nor this file is edited (rule 3,
    DP-22). (item 11.)
12. **§5.1 / §5.2's projection needs its rate named as a rule, not a number.** **Must read:** the
    scheduling rate is **`min(r_Q035 , 0.6620)`** (item 13), `r_Q035` measured by R1(a) on §2.6's own
    night rule with numerator and denominator over the same period; §5.2's table is rebuilt at `record`
    from R1's measured rates, **out only**. Q035's night rule is weaker than the funnel 0.6620 was
    measured on, so the cap is expected to bind — and binding is the point.
13. **§4.3's list closes at lock and three rows are added to it first** (each descriptive, none
    deciding anything, none carrying an MPE): (10) the three endpoints with the level anchored at the
    **t+1 open** instead of `C_t`; (11) the per-slate **`dominant_direction` composition** per night;
    (12) the **bullish-only** sensitivity of both primaries. After these the list is closed and nothing
    is added at the decision pass.
14. **§5.2's "Control-pool depth (unpublished same-night candidates)" row imports a quantity from
    `STEWARD_Q032_exposure.md` §(e) that this question does not use.** Q035 has no separate control
    cohort — the pool **is** `P_t` and the distance match is the construction (§3's last paragraph).
    **Must read:** the row is replaced by the `\|P_t\|` depth question, which is UNMEASURED and is R1
    limb (c); the Q032 figure is cited, if at all, only as context for how deep the same-night candidate
    set runs.
15. **§6's calendar-half split is wrong twice.** "The window's contributing nights split at its 63rd
    elapsed session (≈ 2026-12-14)": 63 is not the midpoint of 136, and session 63 is **2026-12-11**
    (2026-12-14 is session 64). **Must read:** Half A = sessions 1 .. ⌈N/2⌉, Half B = the rest, derived
    by `eval.py` from the pinned calendar — on the drafted window Half A = **2026-09-15..2026-12-18**,
    Half B = **2026-12-21..2027-03-31**; extension nights join Half B. (item 22.)

Checked and **not** corrections — each already matches the policy: the §11 item 1 code citation, read
line by line at `fa70688` and **correct in every particular** (`:1509`, `:1518`, `:1520`,
`:1533-1537`, `:1541-1543`), with the dark lane confirmed **bear-only** (`:1658-1671`) so DP-28's
purpose is met twice; **binding maturity 20 sessions**, with §2.5, §2.6, §4.1, §5.4's arithmetic and
the successor bar horizon all computed on 20 — the error Q032, Q033 and Q034 each carried is **not**
present here, and the decision date **Monday 2027-05-10** is verified session by session; the
**136-session** window count, verified exactly; the **training window's t+20 boundary**, verified
exactly (2026-08-12 → 2026-09-10, Labor Day skipped); entry the **session t+1 open** for every row of
both slates and all four baselines, with **DP-11 correctly not fired** (**DP-03(b)**, **DP-42**); the
20-session clock (**DP-09**); a gap through at the t+1 open scored **not a hit** with the row kept in
the denominator and the tally printed (**DP-26**, rule 5); **no stop assumed anywhere**, counter-
direction touches and adverse excursion reported and never used as exits, **DP-30** not engaged
(**DP-02**); floors read as **80 contributing nights per primary endpoint and 20 per cell**, the
stricter reading, never lowered (**DP-21**); **≥ 30 contributing nights after the lock commit**
satisfied by construction, so **DP-31** does not apply to the main branches and no successor
replication question is owed (**DP-24**); one automatic extension of +30 sessions then DEFERRED, fired
on `eval.py`'s **measured** counts (**DP-13**); the window entirely after the 2026-06-01 catalyst fix
and the training window starting at it, so setup C is one feature on both sides (**DP-06**); units and
the setup list taken from **H-083 as filed** and not re-united — `B` carries projection *and* technical
because splitting them would create a fourth setup H-083 does not name, and `O` is never a setup cell
(**DP-25**); the 2.0-ATR substitution for the printed L3 **recorded in §1.2 rather than applied
silently**, and it is the stricter construction (rule 5's distance match by construction); successor
freezes covering **every candidate symbol, published and unpublished** (**DP-23**); **two CIs per
primary**, CI-1 date-clustered and CI-2 episode-clustered, with CI-1-clears-CI-2-does-not
**INCONCLUSIVE, never CONFIRMED**, correctly identified as acute where a symbol sits in both slates on
consecutive nights (**DP-51**); **the larger of the two permutation p's** entering BH, strictly
stricter (rule 8); B2 and B3 **blocking in one direction only**, with `UNIVERSAL_BELOW_RANDOM` routed
to Q027 and `LAYER_BLEND_NOT_SETUP` sent to its own future PREREG rather than shipped off this verdict;
Registrar conventions fixed before any outcome exists — the within-night z-standardisation, the
zero-variance-layer exclusion, the v1.6 weight-order tie-break, the `symbol`-ascending tie-breaks, the
125-cell grid and its +5.0 pp shrinkage guard, seed `20260914`, the 2,000 draw counts, Gate 0's six
limbs and its two-pass bound (**DP-26**), none promotable at the decision pass; **no rule-14 exception
requested or needed** (**DP-05** untouched, **DP-41** respected); every exposure count taken from the
**pinned freeze** and the read-only repo, never a live query (**DP-50(c)**); no platform outcome column
read anywhere — `sas_selection_excursion`, `outcome_*`, `level_hit_*`, `directional_pct` and
`uoa_symbol_daily.fwd_return_*` all banned (FREEZE_v001 §5), with the desk's own ATR14 and `C_t` from
the bars (PI-003); nothing subscriber-facing before PROSPECTIVELY_CONFIRMED with EN-018's two halves
correctly separated and the ranking half gated on **P2** (rule 10, rule 11, rule 12); and **DP-49**
binding any brief that follows §9.

## Defaulted on Haci's behalf

> **At `record`, both defaults are moot: Q035 is DEFERRED, so neither the 2.0-ATR level nor the schedule
> ever runs.** They stay listed because a re-attempt inherits #4's reasoning (the level is not
> re-opened to make the question easier) and because the board already showed them. **#24 is void** —
> no window, no decision date, no extension, no hard stop. Nothing below became a DP entry (DP-40).

- #4 The uniform target level — chose **2.0 × the row's own ATR14 decides, 1.0 and 3.0 printed and
  deciding nothing**; not taken: 1.0 ATR — nearer L1/L2, inside ordinary noise — DP-42/DP-40. Overturn
  = successor question.
- #24 Window end, decision date and hard stop — chose **2026-09-15 .. 2027-03-31, decision Monday
  2027-05-10, single extension to 2027-05-12 decided Monday 2027-06-21**; not taken: the drafted gate
  that would have deferred at 0.59 — DP-43. Overturn = successor question.

**Two items, and between them they cost eight months of waiting and one measurement choice.** The
level is the one place H-083's own endpoint could not be honoured: it names the printed L3, and a name
the setup ranker promotes has no printed anything — no ladder, no target, no stop, no conviction card
(§10 threat 10). 2.0 ATR is the desk's substitute, identical on both sides so it cannot smuggle target
*placement* into a claim about *name selection*, and 1.0 and 3.0 print beside it so the level cannot be
chosen afterwards. Everything else met a DECIDE ground, and none of the rest is a question about how he
trades — the entry, the clock and the lane come from DP-03 / DP-09 / DP-42 as already locked in
Q002–Q034, and the MPE is DP-20's own number for DP-20's own case, so the usual R-4 never arises. What
is worth seeing on the board is not the date but **what the two decisions above discovered in the
code**: the platform's "bull lane" is the **non-bearish** lane and publishes `mixed` names, which three
desk files now say otherwise; and the rows this question needs — above the publication floor, above the
completeness floor, beaten only by the eighth slot — are a real and, today, **entirely unmeasured**
population. Whether they split three ways deeply enough to test an A/B/C architecture is the single
thing standing between Q035 and a lock, and it is R1's binding limb.

## Routed requests

> **Status at `record` (2026-09-14): R1 CLOSED — answered in `research/reports/STEWARD_Q035_exposure.md`.
> R3 and R2 WITHDRAWN — Q035 is DEFERRED. The three requests are kept verbatim below because a
> re-attempt re-issues R1 unchanged (only the freeze and the trailing quarter differ), and because the
> Red Team reads the request that produced the counts.**

### data-steward — R1 (counts only) — **BLOCKING FOR LOCK** — **CLOSED 2026-09-14**

Q035 (would a setup-specific ranker pick a better eight than the universal 0–100 score — PREREG §5.3
request R1, as amended by DECISIONS items 2, 4, 13, 14 and 19) needs a **counts-only** exposure
measurement on the **frozen** data — `research/data/manifest_v001.json` +
`research/data/manifest_prices_v001.json` against `research/data/exclusions_v003.json`, plus read-only
`git log` / `git show` in the platform repo — and **never a live query** (DP-50(c)). It is **blocking
for the lock**, and its binding limb is one no desk report has ever measured: this question's
population is **not** the published eight but the night's **publishable set** `P_t` — the rows the
platform's own `_qualify_lane` separated from the slate by the 8-slot cap alone — and how that reorder
room splits three ways is unknown. **One population correction before you start** (DECISIONS item 2,
Correction 1): the PREREG's SQL filters `dominant_direction = 'bullish'`, and the platform's main lane
is the **non-bearish** lane — `services/super_agent_select_scoring.py:1643` builds it as every
scorecard whose `dominant_direction` is not `'bearish'`, and `:1628` says "bullish + mixed" — so please
measure everything below on `lower(trim(coalesce(dominant_direction,''))) <> 'bearish'` **and**
`qualification_reason IN ('selected','capped_by_max_output')`, after the §2.5 screens (≥ 60 prior
split-adjusted sessions; a bar at t+1 and a forward series reaching t+20; `ATR14_t > 0` and non-null
finite `C_t`, `overall_score` and all seven layer subscores; no split-scale payload disagreement).
**No outcome of any kind:** no touch, no first-touch date, no return, no excursion, no `outcome_*`
column, no `sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`, and **no setup-versus-outcome
or slate-versus-outcome cross-tab of any shape**; forward bars may be read **only** to establish that a
bar exists (gradeability) and to compute ATR14 and `C_t` for the screens, never for a value. Period:
pick nights **2026-06-01..2026-09-10** (DP-06's segment; every quantity here is a 16:05 property with
no outcome attached, so the widest legal span is used); **denominator for every rate = elapsed
sessions** (calendar sessions minus holidays, exclusions *not* pre-removed — the Q019 / Q022 / Q023 /
Q027 / Q031 / Q032 / Q033 convention), with `exclusions_v003` nights and DP-04 late-`finished_at`
nights removed from the numerator. Please return, by month and for the period as a whole: **(a) the
§2.2 funnel and the §2.6 contributing-night rate** — a non-excluded night with a corroborated
`sas_runs` row, `|P_t| ≥ 1` after the filters and screens, and ≥ 1 row gradeable to t+20 — reported
both over the full window and over the maximal t+20-gradeable sub-period, stating that sub-period's
last pick night from the calendar; note that this rule is **weaker** than the published-pick funnel
your 0.6620 was measured under, so please report it on its own terms rather than reconciling it — the
schedule is built on `min(your rate, 0.6620)` (DECISIONS item 13), so a faster rate changes no date.
**(b) The per-setup rate, which is the limb that decides** — assign each row of `P_t` its dominant
layer by the argmax of the seven layer subscores **z-standardised within that night's `P_t`**
(`flow_strength_score`, `technical_structure_score`, `projection_score`, `catalyst_event_score`,
`gex_alignment_score`, `fundamental_quality_score`, `smart_money_confirmation_score`), excluding from
the argmax any layer with **zero within-night variance** that night and breaking exact ties by the v1.6
weight order projection > technical > flow > catalyst > fundamental > smart-money > GEX then layer name
— giving **A** = flow, **B** = projection *or* technical, **C** = catalyst, **O** = the other three —
then run the **pure** ranker (`w ≡ 1`: within each setup rank by that setup's own raw layer subscore,
`O` rows by `overall_score`, ties by `overall_score` then `symbol` ascending), take its top 8, and
report **the share of contributing nights on which that slate places ≥ 1 name of each of A, B and C,
all three reported and the rarest named**, as a rate per elapsed session. This needs no fit and no
outcome. **(c) Reorder room: the distribution of `|P_t|`** (min, median, max, and the share of
contributing nights with `|P_t| ≥ 9`), plus the count of rows per night by `qualification_reason`
within the lane. **(d) Reorder rate:** the share of contributing nights on which the pure-ranker slate
differs from the reconstructed universal slate, and the mean number of names swapped. **(e) Partition
viability:** the share of `P_t` rows whose top within-night layer z-score exceeds the runner-up by
≥ 0.25 sd, and the number of layers carrying non-zero within-night variance, per night. **(f)
Reconstruction correctness:** the agreement between the universal slate rebuilt from the platform's own
`sorted(key=(-overall_score, symbol))` rule over the screened `P_t` and the platform's **actual**
published main-lane slate, on nights where no row was dropped by §2.5 — and please list the
disagreeing nights with the reason. **(g) The mixed-row share** (DECISIONS item 2): how many rows of
`P_t` and how many **published** rows carry `dominant_direction` of `'mixed'`, null or anything other
than `'bullish'` or `'bearish'`, by month and as a share of nights — informational, **not a gate**, but
it is what tells the Red Team how far a `'bullish'`-only reading would have drifted from the platform's
slate. **(h) The DP-50(a)/(b) sweep:** please **cite `STEWARD_Q033_exposure.md` §(e) rather than
re-run it** if HEAD is still `d19c9a9` — that answer ("NONE" since `fa70688`, scoring module last
touched 2026-07-07, no v1.7 schedule) covers every §2.7 quantity — and add only whatever has landed
since. **(i) For the record only, and explicitly not a gate and not a level-setting input** (DECISIONS
item 4): the distribution of the printed swing-L3 distance in ATR units (`d_L3`) on published main-lane
picks — Q035's registered level is a uniform **2.0 × ATR14** and does not move whatever this shows;
it is asked so §10 threat 3 carries a number. **The call this request decides**, with every branch
fixed before your counts are seen: contributing nights **≥ 0.36** per elapsed session and rarest-setup
nights **≥ 0.09** per elapsed session — the floors 80 and 20 divided by the **225** elapsed sessions
still admissible under DP-43's 12-month ceiling at a 2026-09-14 lock with **20** sessions of maturity
and a one-week freeze margin (latest admissible decision Monday 2027-09-13, last t+20 2027-09-03 since
2027-09-06 is Labor Day, back-solving to a window end of 2027-08-06), rounded **up**, and please
**re-solve them from the trading calendar** rather than taking my arithmetic — the holiday list used
here is 2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31,
2027-06-18, 2027-07-05 and 2027-09-06 — together with the testability limbs, unchanged from the PREREG:
**median `|P_t| ≥ 11` with `|P_t| ≥ 9` on ≥ 80% of contributing nights** (c), **reorder rate ≥ 0.50**
(d), **margin share ≥ 0.60 with ≥ 4 varying layers on ≥ 80% of nights** (e), and **reconstruction
agreement ≥ 0.90** (f). All limbs clear → **Q035 locks**, with the window end set to the **latest** of
floor A (80 contributing nights per primary), floor B (20 contributing nights in the rarest setup),
floor C (20 per calendar half) and floor D (30 post-lock nights, satisfied by construction) at your
measured rates, capped at 2027-08-06 and moved **out** if those rates are slower than §5.2's
placeholders, **never in**. Any limb short → **Q035 goes to `research/questions/DEFERRED.md`** with the
measured counts and the re-check trigger *"the Steward measures ≥ 0.36 contributing nights and ≥ 0.09
rarest-setup nights per elapsed session, with median `|P_t| ≥ 11` and reorder rate ≥ 0.50, over a
trailing quarter"*, and it is **not** re-registered on a weaker partition, a merged setup or a reduced
floor — a different partition is a different question with its own id. Please also state **the
projected date each floor is first reached** at your measured rates, on **20** sessions of maturity
plus a one-week margin, and flag any §4.3 sub-cell projecting below 20 contributing nights at that date
(the suppression list may only gain cells at `record`, never lose them — DECISIONS item 16). Report to
`research/reports/STEWARD_Q035_exposure.md`.

### data-steward — R3 (successor freezes) — **WITHDRAWN 2026-09-14 (Q035 DEFERRED; do not build)**

Q035 (PREREG §5.3 request R3, DP-23) needs successor freezes before its decision pass; **the dates
below are provisional until R1 lands and may only ever move out** (DP-43, DP-45). Please build and pin
a successor **selection** freeze (the same SQL and the same exclusion criteria as v001, over
`sas_candidates` for **every candidate row, published and unpublished**, plus `sas_runs` and
`market_regime_daily` with **`created_at` and `regime_version` preserved**) and a successor **price**
freeze covering pick nights **2026-09-15 .. 2027-03-31** (the window end fixed at `record`, out only)
with **≥ 60 prior sessions before 2026-09-15**; and — only if the single DP-13 extension fires — a
second pair covering pick nights **.. 2027-05-12** (DECISIONS Correction 4: +30 sessions exactly, not
the PREREG's 2027-05-13), built then and not before. Six scope requirements, none optional: **(i)
daily split-adjusted and raw bars only — no hourly bars are needed**, because §4.1 reads one level per
row on a daily clock; this scope is a strict **subset** of the successor price freeze Q027, Q031, Q033
and Q034 already require, so please build the selection freeze **once** and serve them all from it
where the calendar permits — but note that **Q035's requirement stands on its own**: if Q033 and Q034
go to DEFERRED on their own counts, this pair is still built for Q035. **(ii)** The daily bar horizon
runs to **session t+20 of the last included pick night** — **2027-04-28** for a **2027-05-10** decision,
and **2027-06-10** on the extension path for a **2027-06-21** decision. **(iii)** The daily symbol list
covers **every candidate symbol on every in-window night, published and unpublished**, with ≥ 60 prior
sessions before 2026-09-15 — the promoted names are the whole point of this question and they are
unpublished by definition — never assumed from an earlier freeze's symbol list. **(iv) No SPY history
beyond the candidate set is required**, and no Alpaca-dependent extension of it: §6 takes its strata
from `market_regime_daily`, so the credentials blocker your `STEWARD_Q033_exposure.md` §(f) reports
unresolved today does **not** reach this question and must not delay this build. **(v)** An **add-only
successor exclusions file** applying the identical four criteria (`manual_runs`, `non_session_runs`,
`uncorroborated_publication_runs`, `payload_disabled_runs`) to post-2026-09-10 nights — it may add
nights and may never remove one from a v003 list, and its header should state whether the
`analysis_status = "disabled"` / no-`lane_plans` signature is still present and still a
first-published-night-of-the-month pattern, saying so explicitly rather than silently returning an
empty list. **(vi)** Rows whose bars are missing are **excluded and counted, never back-filled or
imputed**, and R1's commit sweep is repeated for the period between the freezes — any change to
`qualification_threshold`, `publication_floor`, `max_output_cap`, `min_completeness`,
`bear_publish_threshold` / `bear_max_output_cap`, the scoring weights, the timeframe multipliers or
thresholds, the conflict penalties, any layer scoring function or any layer enable-flag — with a dated
`DATA_NOTES.md` entry for any repair that rewrites historical rows and an explicit answer **even when
it is "none"**. **The DP-50(a) guard is load-bearing on the seven layer subscores specifically:** a
repair to any of them rewrites this question's **setup labels** retroactively and a repair to
`overall_score` rewrites its **universal slate**, so where this freeze overlaps an earlier one the
rows are compared and `eval.py` **fails loudly** on any disagreement. Please re-confirm every §5.4 date
**session by session from the trading calendar** when the freeze is built; the holiday list is
2026-11-26, 2026-12-25, 2027-01-01, 2027-01-18, 2027-02-15, 2027-03-26, 2027-05-31, 2027-06-18,
2027-07-05 and 2027-09-06. A correction to any date may move it **out, never in**.

### researcher — R2 (`fit.py`, `eval.py`, the frozen artefact) — **WITHDRAWN 2026-09-14 (Q035 DEFERRED; write nothing)**

Q035 (PREREG §5.3 request R2, §4.5, as amended by DECISIONS items 3, 9 and 11) needs both scripts
written **once** (rule 9) and committed by **Monday 2026-10-05**, with `eval.py` committed **before
`fit.py` is run** — §4.5 requires the fit to apply §2.2's filters, §2.3's labels, §2.5's screens and
§4.1's level and clock on the **identical code path**, so an `eval.py` written afterwards would be
written with the fit's output in view. Then run `fit.py` on the training window — pick nights
2026-06-01 through **the last night whose session t+20 falls on or before the pinned price freeze's
last bar date**, derived from the calendar (today 2026-08-12), right-censored nights dropped and
counted — over the exhaustive 125-cell grid `w_A, w_B, w_C ∈ {0, 0.25, 0.50, 0.75, 1.00}` with the
registered tie-break and the **+5.0 pp shrinkage guard**, and write `setup_model_v001.json` plus its
sha256 to the committed sidecar `setup_model_v001.sha256`. **Containment clause (DECISIONS item 3):**
`fit.py` writes the selected triple and the 125-cell grid objective **and nothing else** — no per-night
value, no per-arm touch rate, no `R_pool`, no per-symbol row, no panel — and `results/fit_grid.json` is
sealed with the rest of `results/`, carries `NON_QUOTABLE`, is never ledgered as a finding and is never
quoted. Report only whether the **`FIT_RETURNS_UNIVERSAL`** branch fired (a yes/no, not the numbers).
If the artefact cannot be produced by 2026-10-05, say so on that date: **P1 is demoted to descriptive**
under §4.5's registered fallback and P2 carries the question at `m = 1`; the demotion is recorded by
the Registrar in `schedule.json` that day, before any in-window night has matured to t+20.

## Schedule *(provisional, written at `decide`)* — **STRUCK IN FULL AT `record`**

> **Struck 2026-09-14 on R1.** Q035 is **DEFERRED**; **no date in this block stands** — not the
> 2027-05-10 decision date, not the 2027-06-21 extension or hard stop, not the 136-session window, not
> the halves, not the 2026-10-05 script deadline, not `pin_at_decision`. The governing block is
> `## Schedule` in the RECORD section at the top of this file, which reads DEFERRED. Kept here
> unedited only so the decide pass's reasoning remains readable (rule 3; nothing is rewritten after the
> fact).

**PROVISIONAL — final at `record`, on R1 (item 25).** No rate in this block is measured on Q035's own
funnel yet: the contributing-night rate is capped at the desk's measured published-pick number (item
13) and the rarest-setup share has never been measured anywhere. Every date may move **out** and never
in (DP-43, DP-45).

decision_date: **2027-05-10** (Monday, provisional) · extension_date: **2027-06-21** (Monday — DP-13's
single automatic extension of +30 sessions; then DEFERRED, there is no second pass) · hard_stop:
**2027-06-21** · rule: **exposure-driven**

- **window:** pick nights **2026-09-15 .. 2027-03-31** = **136 elapsed sessions** (verified session by
  session on the item 12 calendar); extended window .. **2027-05-12** = 166 sessions · **extended:
  false**
- **halves:** Half A = sessions 1–68 = **2026-09-15..2026-12-18**; Half B = sessions 69–136 =
  **2026-12-21..2027-03-31** — fixed by session index at this lock and re-derived from the calendar;
  re-cut by the same rule on the extended window (Half A = 1–83, Half B = 84–166). (item 22,
  Correction 15.)
- **binding floor:** **B** — ≥ 20 contributing nights in the **rarest setup**, **UNMEASURED** today and
  the reason R1 blocks. Floor A (≥ 80 contributing nights per primary, DP-21) binds at
  ceil(80 ÷ 0.6620) = session **121** = 2027-03-09, projecting **≈ 90** nights at session 136 — a
  15-session cushion. Floor C (20 per calendar half) binds at ≈ session 61 and floor D (DP-24, ≥ 30
  post-lock nights) at session **46**, both non-binding. Window end = the **latest** of the four,
  recomputed at `record` from R1's measured rates, **out only**, capped at **2027-08-06**.
- **decision date arithmetic:** window end **+ 20 sessions maturity** (§2.5 / §2.6 / §4.1 — this
  question's contributing-night definition and its endpoint's clock agree, which is why its calendar is
  the shortest on the board) **+ one calendar week** freeze margin, first Monday on or after, moved out
  again for a market holiday. 2027-03-31 + 20 sessions = **2027-04-28**, + one week = 2027-05-05, first
  Monday = **Monday 2027-05-10**. Extension: 2027-05-12 + 20 sessions = **2027-06-10**, + one week =
  2027-06-17, first Monday = **Monday 2027-06-21**.
- **maturity:** **20 sessions**, uniform across every row of both slates and all four baselines.
- **gates, all on `eval.py`'s measured counts and none reduced:** ≥ 80 contributing nights per primary;
  ≥ 20 contributing nights in each of setups A, B, C; ≥ 20 in each calendar half; ≥ 30 dated after the
  lock commit; Gate 0's six construction limbs at relative tolerance 1e-6, bounded at two
  fix-and-re-run passes inside the hard stop; reorder rate ≥ 0.25; both CIs excluding 0 (DP-51);
  BH q ≤ 0.10; sign agreement in both halves; both blocking companions (B2, B3) clearing on the
  verdict's side.
- **ceiling:** DP-43's 12 months from a 2026-09-14 lock = **2027-09-14**; the latest admissible
  decision is Monday **2027-09-13**, back-solving to a last window end of **2027-08-06** and **225**
  admissible elapsed sessions. 2027-05-10 is **7.9 months** and 2027-06-21 is **9.2 months** — both
  inside, with more room than any sibling. If R1's measured rates push the initial decision date past
  2027-09-13, the answer is **DEFERRED**.
- **lock-or-DEFER gate: OPEN, waiting on R1.** ≥ 0.36 contributing nights and ≥ 0.09 rarest-setup
  nights per elapsed session on **225** admissible sessions (item 14, Correction 3, re-solved at
  `record`), plus the four unchanged testability limbs (median `|P_t| ≥ 11`; reorder rate ≥ 0.50;
  margin share ≥ 0.60 with ≥ 4 varying layers; reconstruction agreement ≥ 0.90). **The SPY-history
  limb is not a gate here** (item 21).
- **`eval.py` and `fit.py` deadline: committed no later than Monday 2026-10-05, `eval.py` before
  `fit.py` is run, both sha256s recorded, neither touched afterwards** (item 11) — Q006 decides
  2026-10-05 and Q002 2026-10-12, and this question's own fit runs first.
- **artefact:** `setup_model_v001.json`, hash committed to `setup_model_v001.sha256` at the fit run
  (item 11); `eval.py` fails loudly on any other hash; no artefact by 2026-10-05 ⇒ **P1 descriptive,
  P2 carries the question at `m = 1`**, recorded in `schedule.json` that day.
- **pin_at_decision: true** — every night carrying a verdict postdates every existing manifest, so
  DATASET_PINNED runs at the decision date on R3's successor freezes (DP-23).

## Standing rules added

_none, and none is added at `record` either._ **No DP entry follows from a DEFAULTED item** (DP-40) and
none follows from a DEFERRED branch: the readings settled at `record` (limb (b)'s full-window
denominator, §2.5(3)'s always-null-column exclusion) are applications of DP-45, DP-21 and the existing
elapsed-session convention, not new policy, and they bind **this question's re-attempt** by being written
here — not the desk at large — until Haci confirms one of the proposals below. Nothing here is Haci's word: items 4 and 24 were **DEFAULTED** under DP-40 / DP-42 / DP-43 /
DP-45, and a DEFAULTED item adds **no** DP entry (DP-40). The rest are applications of DP-01, DP-02,
DP-03, DP-04, DP-06, DP-09, DP-13, DP-20, DP-21, DP-22, DP-23, DP-24, DP-25, DP-26, DP-28, DP-29,
DP-30, DP-31, DP-41, DP-42, DP-43, DP-44, DP-45, DP-49, DP-50 and DP-51, of the platform code read at
`fa70688`, and of locked precedent plus Q032's, Q033's and Q034's same-day decisions.

## Standing rules proposed

- **A population predicate is verified against the code at the pinned SHA before it is registered, not
  cited from another desk file.** Q035 item 2: three desk files now say "bull lane" where the platform
  means the **non-bearish** lane (`:1628`, `:1643`), which publishes `mixed` names. The error was
  invisible in every question that takes the published slate as given and fatal in the one question
  that has to rebuild it.
- **DP-28 should say what it protects, not only what it matches.** Its purpose is to keep **dark-lane**
  rows out of every arm, and the dark lane is bear-only (`:1658-1671`). A question about the night's
  **choice set** may use `qualification_reason IN ('selected','capped_by_max_output')` inside a
  non-dark lane without deviating from that purpose; a question about the **published** arm keeps
  `qualified IS TRUE AND selected_rank IS NOT NULL`. Worth one clarifying sentence so the next
  Registrar does not have to record a deviation for a case DP-28 never meant to forbid.
- **`eval.py` is committed before any script that shares its code path is run** — not merely before the
  decision pass. Q035 item 11: the fit and the test run the identical filters, labels, screens, level
  and clock, so a fit that runs first hands the eval's author part of its own construction.
- **A lock-or-DEFER rate gate is back-solved against DP-43's ceiling, never against the drafted
  window.** Q035 item 14: the drafted gates (0.59 / 0.15) would have deferred a question that a longer
  window reaches, which inverts DP-43 — the window moves out to reach the floors, and DEFERRED is what
  happens when the ceiling is passed.
- **A verdict computed from training data is INCONCLUSIVE, not NULL.** Q035 item 10: the
  `FIT_RETURNS_UNIVERSAL` branch would have ledgered "a fitted setup ranker does not help" on the
  strength of a grid search over fifty sealed nights, with no CI, no q and no prospective night read.
  Generalises to every early-stop branch decided before the test window opens.
*Added at `record`, 2026-09-14, on R1 — proposals only, no DP id taken:*

- **A testability limb is not a sample-size limb, and only the second one waits.** Q035 items 14/15 and
  this record: a floor short of **counts** fires DP-13's extension; a limb measuring the **shape of a
  single night's population** (median `\|P_t\|`, a per-night agreement rate, a per-night reorder rate)
  is not cured by any window and goes straight to DEFERRED. Worth one sentence in DP-13 or DP-43 so the
  next Registrar does not draft an extension path for a limb an extension cannot reach.
- **A rate is counted over the full window, not over the sub-period the freeze's censoring leaves
  gradeable.** Q035 limb (b): the sub-period denominator is a property of the freeze end date, and it is
  always the reading that clears the gate sooner. The desk has now hit this ambiguity twice in one day
  (Q033 limb (d), Q035 limb (b)); DP-45 answers it, but only after someone notices it is a DP-45
  question.
- **A completeness screen that names an always-null column empties its own population forever.** Q035
  §2.5(3) and PI-008's `smart_money_confirmation_score` (null on 100% of 6,479 frozen rows): a PREREG
  that screens on "all seven layer subscores" must name the columns it screens on, and a Registrar
  writing such a screen checks each named column's null rate on the pinned freeze before registering it.
- **A layer's coverage is checked before a question is built on rebuilding the night's choice set.**
  Q035 died on a 72–74% null rate in the weight-29 layer that Q029 had already measured at 62.74%
  non-null and registered as UNEVALUABLE. The number existed in a locked PREREG on the board; nobody
  carried it across. A desk-level coverage table per platform column, refreshed at each freeze, would
  have caught this at `explore` instead of at `record`.
- **The trading-calendar holiday list belongs in one place, and so does the provisioning register.**
  Third and fourth questions in a row (Q033, Q034, now Q035) to retype the list — Q035 omitted it
  entirely — and third to answer the same Alpaca question. A desk-level list and a dated desk-level
  provisioning register would remove both classes.
