# Successor scope — earlier-deciding successors to locked studies

**INTERNAL / NON_QUOTABLE. Counts and dates only.** 2026-09-14 · owner: registrar ·
bounded learning task `SCHEDULE-SUCCESSORS` (`research/learning/agenda.json`) ·
source: `research/reports/SCHEDULE_AUDIT.md`.

No outcome, hit rate, return, effect, p-value or statistic appears below. No `results/` directory
was opened, no parquet was read, no live query was made. Every count is transcribed from a locked
PREREG, a `schedule.json`, a `DECISIONS.md` or the schedule audit. **No locked question's PREREG.md,
schedule.json, DECISIONS.md or state.json was edited and no date was moved** (rule 3, DP-22).

This report scopes whether a *separately registered, earlier-deciding successor* is warranted for
each locked study the audit names. It is a filing recommendation, not a registration: nothing here
locks anything, and no recommendation reaches a parent's window, floors, endpoints or dates.

---

## 0. Q030 and Q032 — the audit clause is moot; they are not touched

The audit's disposition line reads: *"Q030/Q032: re-entry uses currently unlocked drafts. Apply
DP-53 before locking."* That clause no longer has a subject.

| Q | state | history (from `state.json`) |
|---|---|---|
| Q030 | **PREREG_LOCKED** | DEFERRED 2026-09-14T06:36Z (Alpaca credentials absent) → PREREG_DRAFT 2026-09-14T18:38Z (deferral lifted: coverage 97.55% vs 90%) → **PREREG_LOCKED 2026-09-14T19:07Z, `--by desk`, DP-46** |
| Q032 | **PREREG_LOCKED** | DEFERRED 2026-09-14T13:20Z (SPY history limb, same blocker) → PREREG_DRAFT 2026-09-14T18:38Z (SPY 424 bars vs 250) → **PREREG_LOCKED 2026-09-14T19:08Z, `--by desk`, DP-46** |

Both deferrals were lifted and both questions locked on 2026-09-14, after the audit was written.
They are **locked**, not unlocked drafts, so "apply DP-53 before locking" cannot be executed and is
recorded here as **moot**. Their PREREGs, schedules, decisions and state files are untouched by this
task, and neither is assessed for a successor below: a question locked today has no schedule-audit
scenario against it and no elapsed collection to re-forecast.

Two bookkeeping consequences the re-locks carry for the questions that *are* assessed, by those
files' own never-shrink clauses (the Reporter computes each set at its decision pass):

- Q032's `G` rejoins **F2** (17 at Q032's lock) and rejoins the **F1** companion set named in
  Q033 §7, taking it from 28 to **29**.
- Q030's primary rejoins **F8**, which Q033 §7 recorded as 1 while Q030 was deferred.

---

## 1. The structural finding, stated once

Every question below is **prospective-only**: its window starts at its lock (2026-09-14 or
2026-09-15) and runs forward. A successor that decides *earlier* than its parent must therefore
collect **fewer nights starting from the same date** — its window is a strict **prefix** of the
parent's window, on the same funnel, the same exclusions file and the same contributing-night rule.

That is the whole arithmetic, and it decides most of this report:

1. **A successor's nights are 100% inside its parent's nights.** Overlap is not partial; it is total
   containment. It cannot claim to independently replicate its parent (LEARNING_POLICY, "Counts-only
   readiness and scheduling"), and it is not a second observation of anything.
2. **An earlier read on a prefix of a locked study's own nights is an interim look.** The desk has
   exactly one legitimate form for that — DP-58's single preregistered interim at 60 contributing
   nights, O'Brien–Fleming, success-only, declared before the lock — and DP-58 is explicit that a
   locked PREREG never gains one (DP-22). A new Q-number does not convert a forbidden interim into
   an admissible question; it only removes the boundary that made the interim honest.
3. **The multiplicity runs the wrong way.** A successor's primaries join the parent's family
   correction set, which never shrinks (rule 8, DP-29). The successor therefore **raises the parent's
   own q-values on the parent's own decision date** — it buys weeks by making the parent's test
   harder. Section 2 prints the inflation factor per family.
4. **DP-53's benefit is available forward, not backward.** DP-53 explicitly does not amend locked
   dates ("Locked dates remain binding; discrepancies are audited separately"). The place its
   maturity-separated accounting pays is the *next* question that registers on these funnels, which
   may also register DP-58's interim. Re-buying it for a locked parent costs a family slot, a second
   successor freeze and the parent's own significance bar.

Against that, what a successor would have to declare before lock, in every case, is fixed:
**DP-57** sample-size justification against the MPE (precision, dependence, multiplicity, strata —
not merely "80 nights"); **DP-51** episode-clustered CIs beside the date-clustered CIs, with a
primary that clears the first and not the second scored INCONCLUSIVE; an optional **DP-58** single
interim at 60 contributing nights per primary, declared in §5 and §8 before the lock or not at all,
waiving no floor (DP-21's 20-per-cell and DP-24's 30 post-lock bind at the interim too); and a
**DP-53** forecast that separates eligibility, maturity, gradeability and post-lock counts and
justifies planning uncertainty rather than showing one date.

**A note on direction.** DP-53 says a later date is not inherently more valid. It does not say an
earlier one is. None of the recommendations below rests on preferring the later date; each rests on
the successor buying nothing the parent does not already produce from the same nights.

---

## 2. Per-question scope

### Q024 — `Q024_sas_vs_simple_benchmarks` (F1, H-067)

**(a) Locked date and the audit's scenario.** Decision date **2027-05-17** (extension /
hard stop 2027-06-28), rule exposure-driven, window pick nights 2026-09-14..2027-04-07 =
**142 elapsed sessions**, sized on the measured **0.5652** contributing nights per elapsed session
(26/46) for 80.3 projected against the 80 floor. The audit's mature-cohort scenario: current
collection 142 sessions, mature calendar cohort **26**, contributing nights **26** (a 26/26
conversion), collection at the observed mature-cohort rate **80 sessions**, with the illustrative
10% haircut **89**.
**Gap:** 142 − 80 = **62 sessions ≈ 12.4 weeks**; at the haircut, 142 − 89 = **53 sessions ≈ 10.6
weeks**. Illustrative implied Mondays, arithmetic only and not replacement dates: ≈ 2027-02-22 and
≈ 2027-03-08. This is the largest published gap in the set, and Q024's own §5 already names its
cause: 0.5652 is bound to `manifest_prices_v001`'s forward-bar horizon while 100% of testable nights
converted.

**(b) Warranted under DP-53? No.** Q024 §5 registered this exact branch before the lock — *"if the
artefact is what it looks like, the floors arrive well before 2027-04-07 and the window still runs
to its registered end — it is never cut short and there is no interim look"*. A successor deciding
≈ 12 weeks earlier would run on the first ~80 of the parent's own 142 nights. That is the refused
interim look with a different Q-number.

**(c) Shared with the parent.** Nights: successor window 2026-09-14..≈2027-01, **a strict prefix —
every successor night is a Q024 night**. Manifests: the parent's population arrives only through
`manifest_v002` / `manifest_prices_v002` (built after 2027-05-05); a successor needs its own earlier
freeze pair re-queried from the same one database, so the two freezes may disagree about the same
nights if a repair lands between them (DP-50(a)). Family **F1 Selection edge**, m = 6 primaries
(5 if the EW arm is not registered); F1's correction set was fixed at 10 at Q024's lock, stands at
**29** today, and never shrinks — a 6-primary successor takes it to **35**, inflating every F1
q-value by ≈ 1.21×, Q024's own included. It could not be reported as an independent replication of
Q024.

**(d) Pre-lock declarations if ever filed.** DP-57 against DP-20's +5.0 pp touch-rate MPE per arm;
DP-51 episode-clustered CI beside the date-clustered CI for all six arms; optional DP-58 interim at
60 contributing nights per arm; DP-53 forecast separating the 142-session eligibility cohort from
the 20-session maturity lag and the post-lock count.

**(e) Recommendation: DO NOT FILE.**

### Q027 — `Q027_score_ranking_validity` (F2, H-073)

**(a)** Decision date **2027-04-12** (extension / hard stop 2027-05-24), window 2026-09-15..
2027-03-05 = **119 elapsed sessions** at the measured **0.6761** (48/71); Floor A binds exactly at
session 119 with no cushion. Audit scenario: 119 current, mature cohort **51**, contributing **48**,
collection at the mature-cohort rate **85 sessions**, haircut **95**.
**Gap:** 119 − 85 = **34 sessions ≈ 6.8 weeks**; at the haircut, 119 − 95 = **24 sessions ≈ 4.8
weeks**. Illustrative implied Mondays ≈ 2027-03-01 and ≈ 2027-03-15.

**(b) Warranted? No — and plainly not.** Under the haircut this successor decides **under five
weeks** before its parent, on nights the parent is already collecting. A five-week head start on the
parent's own prefix is not worth a family slot. Q027 §5.1 also already priced the faster reading
(the 0.9577 eligible-night proxy, ≈ 2027-02-22) and declined it under DP-45; the audit's 85-session
scenario sits between the two and changes nothing about the parent's validity.

**(c) Shared.** Nights: strict prefix, total containment. Manifests: the parent pins successor
freezes at the decision date (`manifest_v00N` / `manifest_prices_v00N`, bars through 2027-04-05); a
successor needs an earlier pair over the same nights. Family **F2 Calibration**, m = 2; F2 stands at
**17** and never shrinks — a 2-primary successor takes it to **19** (≈ 1.12× on every F2 q,
including Q027's own two). No independent-replication claim.

**(d)** DP-57 against the registered MPE; DP-51 episode-clustered CI for E1 and E2; optional DP-58
interim at 60 contributing nights; DP-53 maturity-separated forecast on the 119-session cohort.

**(e) Recommendation: DO NOT FILE.**

### Q029 — `Q029_layer_value_ablation` (F1, H-075; F2 companion)

**(a)** Decision date **2027-04-12** (extension / hard stop 2027-05-24), window 2026-09-15..
2027-03-05 = **119 elapsed sessions**, adopted whole from Q027 and sized on Q027's borrowed 0.6761;
Floors A and B both bind at session 119. The audit gives Q029 the same row as Q027 (119 / 51 / 48 /
**85** / **95**) and states that Q029 inherits Q027's funnel while layer-specific gates must still
be checked separately.
**Gap:** identical to Q027 — **34 sessions ≈ 6.8 weeks**, or **24 ≈ 4.8 weeks** at the haircut.

**(b) Warranted? No, and this is the worst trade in the set.** Q029 carries **m = 16** EVALUABLE
layer-endpoint pairs, fixed and closed at record and never revised. A successor reproducing them
buys the same ≈ 5–7 weeks on the same nights while adding 16 primaries to F1 and 10 companion IC
endpoints to F2. The audit's own caveat cuts the other way as well: the inherited funnel rate is not
the layer-specific gate, so a successor sized on the mature-cohort scenario would be sized on a
number that was never measured for Q029's own E3 limbs.

**(c) Shared.** Nights: strict prefix; Q029 and Q027 already share one window, one funnel and one
successor freeze build, so a Q029 successor also overlaps Q027 and Q031/Q033/Q034's shared build.
Family **F1**, m = 16 — F1 **29 → 45**, ≈ 1.55× on every F1 q; plus the required F2 companion
correction on E1ⱼ/E2ⱼ, **17 → 27**, ≈ 1.59× on every F2 q. Q029 §7 fixed m and the EVALUABLE
register at record precisely so that one question, not three, would carry these endpoints; a
successor re-opens exactly that. No independent-replication claim.

**(d)** DP-57 against DP-20 / DP-10 per endpoint type, with the 16-way within-question BH and the
two-family companion correction stated in the power argument; DP-51 episode-clustered CIs on all 16;
optional DP-58 interim at 60 contributing nights **per evaluable pair** (any cell under 20 is a
continue); DP-53 forecast separating the funnel rate from each layer-specific gate.

**(e) Recommendation: DO NOT FILE.**

### Q031 — `Q031_edge_decay` (F2, H-082; F1 companion for `D1ᴮ`)

**(a)** Decision date **2027-06-07** (extension / hard stop 2027-07-19), window 2026-09-15..
2027-04-23 = **153 elapsed sessions**. **The audit publishes no mature-cohort scenario for Q031** —
it is not in the table. Its disposition reads: the 47/71 and 48/71 forecasts share the maturity
concern, *"but calendar-block floors also bind. Recompute every block constraint before proposing a
successor schedule."* The binding constraint is not the 80-night primary (series B reaches it at
session 121) but the **`W3` block cell floor of 20 contributing nights** solved jointly against the
registered 40/40/20 cuts, which is what makes 153 the smallest admissible window.

**(b) Warranted? No — and not even computable today.** The audit forbids proposing a successor
schedule before every block constraint is recomputed, and no such recomputation exists. Worse, the
endpoint is *decay*: `D1` contrasts calendar blocks and `D2` is a persistence holdout, so shortening
the window shortens the calendar span the hypothesis is about. A successor deciding earlier would
not be an earlier answer to Q031's question; it would be a different question with narrower blocks,
which DP-25 makes a new hypothesis rather than a successor.

**(c) Shared.** Nights: strict prefix, and the window is shared with Q027/Q033/Q034's single
successor freeze build. Family **F2**, m = 2 (**17 → 19**), plus `D1ᴮ`'s F1 companion
(**29 → 30**). Q031 §7 already records that it shares `W1 ∪ W2` and the entire `S^A` construction
with Q027 and may not be quoted as corroborating it; a successor inherits that clause twice over and
cannot claim independent replication.

**(d)** DP-57 against the MPE **per block**, not per question — the block cell floor is the binding
one and the power argument has to be made there; DP-51 episode-clustered CIs (block-nested
resampling declared); DP-58 is a poor fit and would have to be declared per block or not at all;
DP-53 forecast with each block constraint recomputed and printed separately.

**(e) Recommendation: DO NOT FILE.**

### Q033 — `Q033_direction_vs_magnitude` (F8, H-081; F1 companion for `A`)

**(a)** Decision date **2027-07-12** (extension / hard stop 2027-08-23), window 2026-09-15..
2027-04-30 = **158 elapsed sessions**, P1 alone (P2 deferred at lock, carrying no date).
**The audit publishes no scenario for Q033** and says so explicitly: *"their files discuss
horizon-adjusted rates but cap planning using Q031's 0.6620. Review inherited caps and 40/60-session
endpoints separately; do not apply the 20-session scenarios above."* The relevant internal counts:
binding maturity **40 sessions**, scheduling rate `min(r₄₀ = 0.8710, 0.6620) = 0.6620`, Floor A
binding at **session 121** with the window end deliberately not pulled back to it — 158 − 121 =
**37 sessions ≈ 7.4 weeks** of registered window beyond the binding floor, held because a shorter
window is never chosen to reach a date sooner (DP-43, DP-45) and because the window is shared with
its siblings for one freeze build.

**(b) Warranted? No.** The audit's instruction is to *review the inherited cap*, which is a
scheduling-methodology observation, not a defect in the parent's test: the cap can only have made
Q033 wait longer, never made it wrong. A successor would decide on a prefix of the same nights under
the same 40-session maturity, and the honest upper bound on what it buys (≈ 7–13 weeks) is bought by
taking the horizon-matched rate the parent declined under DP-45 — the desk does not buy weeks with a
rate it capped on purpose. Re-uniting the maturity to 20 sessions to decide sooner is forbidden by
DP-25 and would be a new hypothesis, not a successor.

**(c) Shared.** Nights: strict prefix of the 158-session window shared with Q027, Q031 and Q034.
Family **F8 System validity**, m = 1 — F8 rises by the successor's primary — plus the mandatory
**F1** companion correction on `A` (Q006's construction), **29 → 30**. Q033 §7 already states that
`A` is quoted at the larger of the two q's; a successor inherits that and cannot be read as
independent replication.

**(d)** DP-57 against DP-20's +5.0 pp on the 40-session clock, with the two-family correction in the
power argument; DP-51 episode-clustered CI beside the date-clustered CI for `A`; optional DP-58
interim at 60 contributing nights; DP-53 forecast separating the 158-session eligibility cohort, the
40-session maturity lag and the post-lock count, and stating whether the 0.6620 cap or the measured
horizon-matched rate is used — once, not twice.

**(e) Recommendation: DO NOT FILE.**

### Q034 — `Q034_economic_objective` (F8, H-084)

**(a)** Decision date **2027-08-09** (extension / hard stop 2027-09-20), window 2026-09-15..
2027-04-30 = **158 elapsed sessions**, binding maturity **60 sessions**, scheduling rate
`min(r_rank,60 = 0.9091, 0.6620) = 0.6620`. **No audit scenario is published**; the same
"review inherited caps and 40/60-session endpoints separately" disposition applies. Internal counts:
Floor A (80 ranking-set nights) binds at **session 121**, projecting 104.6 at 158 — **37 sessions
≈ 7.4 weeks** of window beyond the binding floor; at the uncapped measured 0.9091 the floor would
bind near session 88, i.e. ≈ 70 sessions ≈ 14 weeks before the registered end. This is the largest
*potential* gap in the set and the only one with no family-correction cost.

**(b) Warranted? No.** Q034 is the case that most tempts a successor and least supports one. It
carries **no primary endpoint, no MPE, no q-value and declines PROSPECTIVELY_CONFIRMED in every
branch**; its output is a register that routes new PREREGs. An earlier successor would print the
same nine-objective register on a strict prefix of the parent's nights, three months before the
parent prints it on the superset — two registers from nested data, where the later one would look
like corroboration of the earlier and is not. For a question whose only product is *which question
to ask next*, routing on a partially collected register and then being contradicted by the parent is
the specific failure worth avoiding. Shortening the 60-session maturity to reach a date sooner is
DP-25-barred: H-084 names the long lane.

**(c) Shared.** Nights: strict prefix of the 158-session window shared with Q027, Q031 and Q033 —
and a successor needs its own freeze pair with 60-session forward bars, a second Steward build over
nights the shared build already covers. Family **F8**; Q034 itself enters no correction set and
computes no q, so a successor adds **no BH obligation** — the one case where multiplicity is not the
objection. The objection is that its overlap is total and its verdict is not a verdict: Q034 §7
already says the register confirms nothing and that a named winner routes a new PREREG rather than
supporting one.

**(d)** DP-57 stated as a **precision** argument rather than a power argument (there is no MPE to
size against) — what width of separation interval the register needs to name a winner, given
DP-51's clustering and the 9 × 9 objective correlation; DP-51 episode-clustered CIs beside the
date-clustered CIs for every objective row; **DP-58 is inapplicable** (no touch-rate or per-trade
ATR primary to spend α on); DP-53 forecast separating the 158-session eligibility cohort, the
60-session maturity lag and the ranking-set gradeability, with the inherited 0.6620 cap either
justified or replaced, once.

**(e) Recommendation: DO NOT FILE.**

---

## 3. Summary

| Q | family | locked decision date | registered window | audit mature-cohort scenario | gap (sessions / weeks) | recommendation |
|---|---|---|---:|---:|---|---|
| Q024 | F1 | 2027-05-17 | 142 | 80 (89 at haircut) | 62 / ≈12.4 (53 / ≈10.6) | **DO NOT FILE** |
| Q027 | F2 | 2027-04-12 | 119 | 85 (95) | 34 / ≈6.8 (24 / ≈4.8) | **DO NOT FILE** |
| Q029 | F1 (+F2) | 2027-04-12 | 119 | 85 (95) — inherited from Q027 | 34 / ≈6.8 (24 / ≈4.8) | **DO NOT FILE** |
| Q031 | F2 (+F1) | 2027-06-07 | 153 | none published; block constraints must be recomputed first | not computable today | **DO NOT FILE** |
| Q033 | F8 (+F1) | 2027-07-12 | 158 | none published; 40-session endpoint, inherited cap | ≤ 37 / ≈7.4 internal slack | **DO NOT FILE** |
| Q034 | F8 | 2027-08-09 | 158 | none published; 60-session endpoint, inherited cap | ≤ 37 / ≈7.4 (≈70 / ≈14 uncapped) | **DO NOT FILE** |
| Q030 | — | locked 2026-09-14 | — | audit clause **moot** (now PREREG_LOCKED) | — | not assessed; untouched |
| Q032 | — | locked 2026-09-14 | — | audit clause **moot** (now PREREG_LOCKED) | — | not assessed; untouched |

**BACKLOG.md hypotheses appended: none.** Next free H-number remains **H-095** (H-091..H-094 are the
2026-09-14 filings). No family's correction set is enlarged by this report, and no locked file was
edited.

---

## 4. What would change these recommendations

Stated now, so a later reader can tell a real change from a re-argument:

1. **A successor whose nights are not a prefix.** A question that registers a window starting after a
   parent's window ends, or on a population the parent excludes, is a genuine second observation and
   is judged on its own merits — but it decides *later*, not earlier, and is not what this report
   scoped.
2. **A platform ship that splits a parent's window** (DP-50(a)/(b), the DP-06 pattern). If a repair
   rewrites a column a locked PREREG reads, the post-ship nights are a different feature and a
   successor on them is a new question, not an interim look. `research/data/DATA_NOTES.md` is where
   that becomes visible.
3. **A parent reaching its hard stop and going to DEFERRED.** Then the successor is the remedy for a
   dead question, not an early read on a live one, and the overlap objection lapses with it.
4. **Q031's block recomputation** (the audit's own precondition). Until every block constraint is
   recomputed, no Q031 successor schedule can be proposed at all.

DP-53's accounting is not lost by declining these six. It applies in full to the next question that
registers on these funnels, which — unlike a locked parent — may also register DP-58's single
interim at 60 contributing nights.
