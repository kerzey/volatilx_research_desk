# STEWARD_Q034_exposure.md — R1 (counts only), Q034 economic_objective

**Request:** `research/questions/Q034_economic_objective/PREREG.md` §5.3 R1, as amended by
`DECISIONS.md` items 7, 9, 17, and the "Routed requests — data-steward — R1" text. Counts only,
no outcome of any kind: no touch, no first-touch date, no return, no excursion, no `outcome_*`
column, no `sas_selection_excursion`, no `uoa_symbol_daily.fwd_return_*`. Forward bars read only
to establish that a bar exists (maturity accounting), never for a value. Frozen data only —
`research/data/manifest_v001.json` + `research/data/manifest_prices_v001.json` against
`research/data/exclusions_v003.json`, plus read-only git log/show/merge-base against the
pinned, read-only platform repository — never a live query (DP-50(c)).
`RESEARCH_DB_URL`, `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` are all unset in this session; none is
needed for (a)-(g), which use frozen parquet and the read-only repo only (their absence is limb
(g) itself, cited from `STEWARD_Q032_exposure.md` §(g) as DECISIONS item 17 directs).

**Population:** pick nights **2026-06-01..2026-09-10**. Denominator for every per-session rate =
**elapsed sessions** (exclusions not pre-removed, the Q019/Q022/Q023/Q027/Q031/Q032 convention).

**Elapsed sessions in window: N = 71**, reconfirmed against `v001_sas_runs.parquet` (71 rows) and
the SPY daily-bar calendar in `manifest_prices_v001` (153 bars, 2026-02-02..2026-09-10) — both
agree exactly, matching `STEWARD_Q027/Q031/Q032_exposure.md`.

**Nights excluded from the population (3):** `2026-06-26` (`uncorroborated_publication_runs`),
`2026-07-02` (`manual_runs`), `2026-07-06` (`manual_runs`). DP-04 late-`finished_at` re-check
(every in-window `finished_at` vs the next session's ~09:30 ET open): **1** night fails,
`2026-07-06` — already excluded via `manual_runs`, so DP-04 adds **0** incremental nights.
**Non-excluded nights: 68.** Identical to the Q027/Q031/Q032 population, reconfirmed
independently here.

**Published rows on the 68 non-excluded nights (`qualified IS TRUE AND selected_rank IS NOT
NULL`): 550** — bit-for-bit the same figure `STEWARD_Q032_exposure.md` reports, independently
recomputed from `v001_sas_candidates.parquet` and `p001_daily_split.parquet` (own ATR14, `C_t`,
never `atr_pct` / `spot_close` — PI-003).

---

## Headline

**Q034 does not lock. Limb (b) — the ranking-set rate, the limb R1's own text calls "the limb
that decides" — is short by roughly a factor of five, and it is short for a reason worth stating
in one sentence up front: the section 2.4 "six levels not strictly monotone" screen, read
literally, fails 429 of 550 published rows (78%), and 388 of those 429 failures are ties, not
reversals — the platform's own 2026-07-06 fix (services/super_agent_select_service.py:195-257,
commit 5fa3db4, confirmed an ancestor of the pinned fa70688) explicitly allows equal prices
across lanes by design ("equal prices across lanes are allowed (non-strict monotonicity), as
duplicates already exist in the book") and its own docstring documents that its entry-price
guard leaves many ladders unresolved (non-monotonic) rather than force a resort. Applied
strictly, as section 2.4 is literally worded, this collapses the ranking-set rate to about
0.09 per elapsed session against a required floor of 0.44. Applied non-strictly (ties allowed,
matching the platform's stated design), the same population's ranking-set rate is about 0.91 per
elapsed session — comfortably above the floor. Both counts are reported below; the literal
wording governs the gate call made here, and the fork is flagged for the registrar rather than
resolved by this report.**

**Gate limb table (184 admissible elapsed sessions, Correction 2; thresholds re-solved below):**

| limb | measure | floor | measured (literal section 2.4, strict monotone) | measured (non-strict sensitivity) | pass/short |
|---|---|---:|---:|---:|---|
| (b) ranking-set contributing nights/session | scheduling rate min(r_rank60, 0.6620) | >= 0.44 (80/184) | 0.0909 (1/11, t+60 sub-period) | 0.9091 (10/11) | literal: SHORT -- non-strict: PASS |
| (c) rarer-window contributing nights/session, platform-label | | >= 0.11 (20/184) | 0.1972 (14/71) | -- | PASS |
| (c) rarer-window contributing nights/session, bar-only (cited) | | >= 0.11 | 0.3099 (Q032 5(b), SMA50-only proxy) | -- | PASS |
| (g) credential re-check | presence | n/a | absent (all three) | -- | not a gate (DECISIONS item 17) |

**Branch fired: DEFERRED, on limb (b), under the literal reading of section 2.4 that this report
applies by default.** Per PREREG section 5.3 / DECISIONS item 19: "Either limb short -> Q034 goes
to research/questions/DEFERRED.md." Limb (c) clears on both partitions; limb (b) does not, and
it is not close -- at the measured literal rate, the 80-night ranking-set floor projects to
session about 880 from lock, nowhere near the 184-session ceiling. If the registrar rules the
non-strict reading governs section 2.4 instead, limb (b) clears (0.9091 >= 0.44) and only limb
(c) needs to hold, which it already does -- Q034 would lock on this report's other counts
unchanged. That ruling is outside this report's mandate; it is a definitional question, not a
data one.

---

## (a) Section 2.4 funnel and the section 2.5 contributing-night rate at 60-session maturity, three ways

**Section 2.5 imports "Q031 section 2.5's series-B rule verbatim"** (maturity extended from t+20
to t+60 only), so the general/registered "valid published pick" screen here is Q031's own --
`no lane_plans`, wrong-side on **L3 only** (`d_p <= 0`), the split-scale payload screen, the
`d_L3 in [0.25,10]` bound, `>= 60` prior bars -- **not** the stricter all-six-levels screen that
governs (b). This funnel is independently recomputed, not copied, and reconciles bit-for-bit with
`STEWARD_Q032_exposure.md` section (a):

| category | rows | reason |
|---|---:|---|
| valid | **514** | passes all screens below |
| no `lane_plans` at all | 8 | all 8 on `2026-06-02` (`analysis_status="disabled"`) |
| wrong side (`d_p <= 0` on L3) | 2 | |
| split-scale payload screen | 19 | Q027 section 2.4's joint screen, reused verbatim |
| `d_L3` bound `[0.25, 10]` | 7 | |
| `< 60` prior daily bars | 0 | |
| **total** | **550** | reconciles exactly |

**Calendar-derived maturity cutoffs** (from `manifest_prices_v001`'s own last date, 2026-09-10 =
calendar index 152): a pick night matures to t+60 only if its index + 60 <= 152, i.e. index <= 92
= **2026-06-15**; to t+20 only if index <= 132 = **2026-08-12** (bit-for-bit the same cutoff
`STEWARD_Q031/Q032_exposure.md` report for t+20).

| form | definition | numerator | denominator | rate |
|---|---|---:|---:|---:|
| (i) t+60-evaluable sub-period | nights 2026-06-01..2026-06-15 (11 elapsed sessions, all non-excluded), >=3 valid picks | 10 | 11 | 0.9091 |
| (ii) t+20-comparable | nights maturing to t+20 (<=2026-08-12), >=3 valid picks, full 71-session denominator | 47 | 71 | 0.6620 |
| (iii) full-denominator t+60 | numerator = (i)'s 10, denominator = full window | 10 | 71 | 0.1408 |

Form (ii)'s 0.6620 is bit-for-bit the same as `STEWARD_Q031_exposure.md` section (a) and
`STEWARD_Q032_exposure.md` section (a)(ii); DECISIONS item 1's claim that the contributing-night
rate is unchanged by the t+60 maturity extension is **reconfirmed, not corrected**.

Only `2026-06-02` fails the >=3-valid-pick test inside the t+60 sub-period (0 valid picks, the
`analysis_status="disabled"` signature every prior Steward report flags on that night).

## (b) The ranking-set rate -- the limb that decides

A night enters the ranking set iff (per DECISIONS item 7) it is a section 2.5 contributing night
**and each of the nine objectives independently carries >=3 valid picks, each with >=5 valid
controls**, after that objective's own screen. The control-pool floor is not re-measured here in
full: it is the same 68-night population `STEWARD_Q031_exposure.md` section (b) and
`STEWARD_Q032_exposure.md` section (e) already measured at min 37, median 53-54, max 60, never
below 10 -- its cost on this population is zero, so the binding constraint below is the
valid-pick count alone, exactly as those reports found.

**The "shared screens" every objective inherits (section 2.4) add two clauses beyond (a)'s
Q031-style funnel: any of the six flattened levels wrong-side of `C_t` (not L3 alone), and the
six levels "not strictly monotone in the direction."** Applied literally:

| category (literal, strict monotone) | rows |
|---|---:|
| any flattened level wrong-side (any of L1-L6 present) | 7 |
| six levels not strictly monotone (of 534 rows with a complete ladder) | 429 |
| of which true reversals (fails even the non-strict/ties-allowed test) | 41 |
| of which ties only (passes non-strict, fails strict) | 388 |
| `outcome_target_invalid` non-null | 4 |
| valid_shared (literal, strict) total | 104 / 550 |
| valid_shared (non-strict sensitivity, ties allowed) total | 476 / 550 |

**Per-objective night counts (>=3 valid picks that night), full 68 non-excluded nights, no
maturity restriction -- literal/strict reading:**

| objective | screen beyond shared | nights >=3 valid |
|---|---|---:|
| O1, O2, O3, O6, O7, O9 | shared screens only | 12 each |
| O4 | plus wrong-side printed swing stop | 8 -- the binding objective |
| O5, O8 | plus complete six-level ladder (all 3 lanes) | 9 each |

**Ranking set (all nine simultaneously >=3, literal/strict): 6 / 68 nights** (no maturity
restriction); restricted to the t+60-evaluable sub-period (11 nights, section (a)): **1 / 11**
nights (`2026-06-08`); t+20-comparable (denom 71): **3 / 71**; full-denominator t+60: **1 / 71**.

| form | numerator | denominator | rate (literal) | rate (non-strict sensitivity) |
|---|---:|---:|---:|---:|
| (i) t+60-evaluable sub-period | 1 | 11 | 0.0909 | 0.9091 (10/11) |
| (ii) t+20-comparable | 3 | 71 | 0.0423 | -- |
| (iii) full-denominator t+60 | 1 | 71 | 0.0141 | -- |

**Scheduling rate per DECISIONS item 8, min(r_rank60, 0.6620), measured over the same t+60-
gradeable sub-period: min(0.0909, 0.6620) = 0.0909** (literal reading). Under the non-strict
sensitivity, min(0.9091, 0.6620) = 0.6620 -- the desk's own published-pick cap would then bind
instead, exactly as DECISIONS item 8 anticipates for a well-behaved ranking set.

**O4 is the binding objective in both bases** (8 of 68 nights, 1 of 11 in the t+60 sub-period) --
the wrong-side-swing-stop screen alone removes a comparable share to the monotonicity screen; see
(d). No sub-cell projection below 20 is flagged beyond what (b) itself already shows: at the
literal rate, every row and every window is far below both the 20-night and 80-night floors.

## (c) The rarer-window limb, on both candidate partitions

Applied to Q034's own general (section 2.5, Q031-style) contributing nights -- **67 of 68** clear
>=3 valid picks (only `2026-06-02` fails; consistent with (a)'s 47-of-48 pattern restricted to
matured nights).

**Platform-label partition** (`STRONG` iff `market_regime = strongly_bullish` on a
legality-tested v1.2 row -- row dated t, `market_regime` not unknown, `data_quality` not
insufficient, `created_at` dated t and <= that night's `finished_at` -- Q032 section (d)'s test,
run here independently on Q034's own 67 contributing nights):

| | count |
|---|---:|
| legal (of 67 contributing nights) | 63 |
| illegal (`created_at` timestamp test fails) | 4 |
| STRONG | 49 |
| NOTSTRONG (rarer arm) | 14 |

**NOTSTRONG rate: 14 / 71 = 0.1972 / elapsed session -- clears >=0.11.**

**Bar-only tape partition (cited, not re-run, per R1(c)):** `STEWARD_Q032_exposure.md` section
(b) measures HOSTILE (the rarer arm) at **0.3099/session** under the SMA50-only registered lower
bound -- also clears >=0.11. Q034's stricter funnel (>=3 picks/>=5 controls vs Q032's >=1/>=3)
cannot change the bar-only arm labels (a function of SPY bars alone, per section 2.2, unaffected
by pick validity) but would thin which nights within each arm actually contribute; that
re-measurement is not requested to be re-run per R1(c)'s own citation clause and is not performed
here.

**Lower of the two partitions: 0.1972 (platform-label). Limb (c) clears >=0.11 on both bases.**

## (d) Wrong-side swing stops and d_L3 exclusions

**Wrong-side printed swing stop** (Q009 section 1's 17.8% signature, re-measured on
2026-06-01..2026-09-10): of 550 published rows, 542 carry a `swing_trading.stop` value (8 have
none, all on `2026-06-02`). **103 of 542 (19.0%), or 103 of all 550 (18.7%), have a stop on the
wrong side of `C_t`** for the called direction (bullish: stop >= `C_t`; bearish: stop <= `C_t`).
This is somewhat higher than Q009's in-sample 66/371 (17.8%) but the same order of magnitude; it
is O4's own denominator loss, separate from and additive to O4's share of (b)'s
monotonicity/shared-screen loss.

**d_L3 in [0.25, 10] bound:** **7 of 550 (1.3%)** excluded, counted after `no_lane_plans`,
wrong-side-L3 and the split-scale screen are already removed (precedence order, matching the
Q027/Q031/Q032 convention) -- bit-for-bit the same count `STEWARD_Q032_exposure.md` section (a)
reports.

## (e) Complete six-level ladder -- O8's and O5's denominator

**534 of 550 published rows (97.1%) carry a complete six-level ladder** (both targets present in
each of `day_trading`, `swing_trading`, `longterm_trading`). **Share of nights with fewer than 3
picks carrying a complete ladder: 1 of 68 (1.5%)** -- only `2026-06-02` (0 lane_plans at all).
**The raw ladder-completeness rate is not what binds O5/O8's ranking-set count in (b)** -- the
shared-screens monotonicity/wrong-side loss dominates it by roughly an order of magnitude (534
complete vs 104 valid_shared under the literal reading).

## (f) DP-50(a)/(b) commit sweep since fa70688, plus BAND_EXITS

`fa70688bc252d14f8d67e371afafc194731c324e` reconfirmed an ancestor of `HEAD`
(`d19c9a945418b09773baffac37f8d723c8a90a9a`, git merge-base --is-ancestor, read-only). **`HEAD`
is unchanged at `d19c9a9`** -- the same commit `STEWARD_Q027/Q031/Q032_exposure.md` measured on
this same date (2026-09-14). **No new commits exist since those sweeps.** The 4 commits between
`fa70688` and `HEAD` touch none of `services/super_agent_select_scoring.py`,
`services/super_agent_select_models.py`, `services/sas_conviction_card.py` or
`services/market_regime/scorer.py` (reconfirmed here independently, same result as the two prior
reports).

**BAND_EXITS (`scripts/generate_sas_trading_guide.py:89-95`, O5's Plan H -- no sibling sweep
named this limb):** last touched by commit `b24954c` ("Guide sidecar: emit ruled exit
schedules"), 2026-07-09, confirmed via git merge-base --is-ancestor b24954c fa70688 to be **an
ancestor of the pinned `fa70688`** (2026-09-05) -- i.e. before the pin, not after. **Zero commits
touch this file between `fa70688` and `HEAD`.** BAND_EXITS is unchanged since the freeze.

**Answer: NONE** -- no weight, timeframe multiplier, `qualification_threshold`,
`publication_floor`, `bear_publish_threshold`, `max_output_cap`, `min_completeness`, ATR-elite
cap, GEX offset, scoring enable-flag, BAND_EXITS or the lane-plan writer has changed since
`fa70688`.

**v1.7 schedule check:** `docs/SAS_SCORING_RESEARCH_PLAN.md` unchanged since 2026-09-03 (before
`fa70688`), still headed "Status: PROPOSAL -- not a decision record... Owner sign-off required
before any workstream starts," phases in relative weeks with no calendar anchor, no commit
anywhere shows the workstream has started. **No v1.7 promotion is scheduled inside
2026-09-15..2027-09-20 (Q034's own admissible span) or anywhere else**, because no start date
exists to count weeks from -- the same finding `STEWARD_Q031/Q032_exposure.md` report, to be
rechecked at every future sweep, not assumed clear permanently.

## (g) Credential re-check (record only -- not a gate for Q034, DECISIONS item 17)

`RESEARCH_DB_URL`, `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` are all **absent** from this desk
session -- confirmed directly. Consistent with `STEWARD_Q032_exposure.md` section (g)'s same-day
finding (the H-074/Q030 blocker). This limb defers nothing in Q034 (no endpoint here is an arm
contrast, per DECISIONS item 17); it is reported for the record only.

---

## The lock-or-DEFER gate

**184 admissible elapsed sessions** (Correction 2, re-solved from the trading calendar: latest
admissible initial decision Monday 2027-09-13 -> last t+60 on or before 2027-09-03 (2027-09-06 is
Labor Day) -> window end **2027-06-08 = session 184**). Floors, rounded up: ranking-set nights
**>= 0.44** (80/184); rarer-window contributing nights **>= 0.11** (20/184), applied to the lower
of the two partitions.

- **Limb (b), literal section 2.4 (strict monotone), the reading this report applies: 0.0909 <
  0.44 -- SHORT**, by a wide margin. Projected date the 80-night floor is first reached at this
  rate: **about session 880 from lock** -- far beyond the 184-session ceiling; no extension
  reaches it.
- **Limb (b), non-strict sensitivity (ties allowed): 0.6620 (capped) >= 0.44 -- PASSES.**
  Projected date at this rate: **about session 121** (80 / 0.6620), comfortably inside the
  ceiling -- the same projection section 5.1's original table already carried before this
  measurement.
- **Limb (c), both partitions: 0.1972 (platform-label) and 0.3099 (bar-only, cited) -- both
  >= 0.11 -- PASSES.** Projected date the rarer-window 20-night floor is reached, at the lower
  (platform-label) rate: **about session 102** (20 / 0.1972) -- comfortably inside the ceiling.

**Gate call, on the literal reading: Q034 goes to research/questions/DEFERRED.md.** Limb (b) is
short; per PREREG section 5.3 / DECISIONS item 19, "Either limb short -> Q034 goes to DEFERRED,"
with the re-check trigger **"the Steward measures >= 0.44 ranking-set nights and >= 0.11
rarer-window contributing nights per elapsed session over a trailing quarter."** DP-13's
single-extension mechanism belongs to section 5.2's post-lock schedule, not to this binary
lock-or-DEFER gate, and does not apply here.

**What would change the call, stated plainly because the gap between the two readings is the
whole story of this report:** if the registrar rules that section 2.4's "not strictly monotone"
screen is meant non-strictly -- ties allowed, matching the platform's own
_enforce_ladder_monotonic design (services/super_agent_select_service.py:195-257, commit
5fa3db4, 2026-07-06, an ancestor of the pinned fa70688) -- then limb (b) measures **0.6620** (the
desk's own published-pick cap binds), clears 0.44, and Q034 locks on every other count in this
report unchanged. This report does not make that ruling; it states the literal count, flags the
sensitivity, and applies the wording as registered.

---

## What this does and does not decide

This is a counts-only exposure measurement. No touch rate, return, excursion, plan result, or
score-vs-outcome relationship appears anywhere above. The registered screens (section 2.4) and
the ranking-set rule (section 2.5, DECISIONS item 7) do not change on this measurement -- only
the counts, the gate call, and the flagged strict/non-strict sensitivity do. I report the branch
the literal wording implies; the Registrar/Decision-maker rules on the monotonicity-clause
reading and files the DEFERRED entry (or lock, if the non-strict reading is ruled to govern) and
updates the board. The Data Steward does not decide that step, and does not advance the
controller under this protocol.
