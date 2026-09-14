# Research desk — board

_Generated 2026-09-14 by `research/lib/board.py`. Do not edit; edit the source files and re-run. Ask the desk for anything on this page in plain words, or use the commands shown._

## 1. Waiting on you

- **EN-002** — run the brief in the platform repo, then tell the desk the SHA  
  `/desk-run verify EN-002 <sha>`

**Ready when you ask** (you already decided these; the desk writes the prompt on request):

- **PI-002** — No coverage watchdog fires on PI-001 (none found in the codebase by that name)  →  `/desk-run prompt PI-002`
- **PI-003** — `atr_pct` corrupted around splits (ATR computed on raw bars)  →  `/desk-run prompt PI-003`
- **PI-004** — Manual re-runs indistinguishable from nightly runs in `super_agent_select_runs`  →  `/desk-run prompt PI-004`
- **PI-006** — 16 published picks have no target ladder  →  `/desk-run prompt PI-006`
- **PI-007** — `industry` populated for only 12% of candidates  →  `/desk-run prompt PI-007`
- **PI-011** — Printed swing stop on the wrong side of the pick-night close for 67 of 382 published picks  →  `/desk-run prompt PI-011`

How you act on the lists below: **`/desk-run prompt <ID>`** writes the implementation prompt for an issue (PI), enhancement (EN) or trade idea (TI) — asking for it *is* your decision. Run the prompt in the platform repo with Codex or Claude, then **`/desk-run verify <ID> <sha>`** and the desk checks the result. Research findings (Q) still need `HUMAN_APPROVED --by haci` before a brief, because the controller enforces it. New idea: **`/desk-run idea "…"`** or a line in `research/INBOX.md`.

## 2. Results (verdicts on record)

| Q | question | verdict | the number | nights | date |
|---|---|---|---|---|---|
| Q005 | why does SAS publish fewer 90+ picks every month? | INCONCLUSIVE | elite-candidate rate P1−P0: −0.255/night [-0.442, -0.050], NON_QUOTABLE | 107 (P0 58 / P1 49) | 2026-09-11 |

## 3. Edges

**Proven (historical or prospective):**

_none yet — every question so far is NULL, INCONCLUSIVE, or still waiting for its decision date._

**Candidate edges under test (locked; the desk looks once, on the date):**

| Q | question | state | decides on |
|---|---|---|---|
| Q006 | does SAS selection beat a distance-matched control from its own universe, on the price path? | DATASET_PINNED | 2026-10-05 |
| Q002 | do SAS picks reach the near targets sooner than matched candidates? | DATASET_PINNED | 2026-10-12 |
| Q004 | does it matter whether you buy the pick after hours, at the open, or at 10:00? | DATASET_PINNED | 2026-10-26 |
| Q009 | does the stop printed on a SAS pick shake traders out of trades that would have reached the target anyway? | DATASET_PINNED | 2026-11-09 |
| Q011 | is it better to rest a limit order below the pick-night close and buy the day-1 dip, or just buy at the next open? | DATASET_PINNED | 2026-12-14 |
| Q003 | are first-time picks weaker than picks SAS keeps re-selecting? | DATASET_PINNED | 2026-12-15 |
| Q008 | when a pick held from the pick-night close reaches its first target within two sessions, is it more likely to go on to i | DATASET_PINNED | 2026-12-28 |
| Q010 | does Q009's stop result repeat on nights nobody had seen when it was registered? | PREREG_LOCKED | 2027-02-22 |
| Q016 | Q016 — two-sidedness by beta and ATR (does volatility at selection predict a round trip?) | DATASET_PINNED | 2027-02-22 |
| Q022 | Q022 — sector cluster nights (does a concentrated slate change what the picks do?) | PREREG_LOCKED | 2027-02-22 |
| Q012 | for a pick below 90, is it better to take the first small target and put the money into the next pick, or to hold the co | DATASET_PINNED | 2027-03-22 |
| Q013 | does a pick whose earnings report lands within three sessions run a worse path than a pick whose report is further out? | DATASET_PINNED | 2027-03-22 |
| Q014 | does a week of repeated unusual-options activity before the pick night make a SAS pick better, and does SAS add anything | DATASET_PINNED | 2027-04-05 |
| Q007 | for a pick already held from the pick-night close, does a next-morning gap of more than 2% predict the rest of the trade | DATASET_PINNED | 2027-04-26 (exposure check; hard stop 2027-06-30) |
| Q024 | Q024 — does SAS beat embarrassingly simple benchmarks, on the price path? | PREREG_LOCKED | 2027-05-17 (exposure check; hard stop 2027-06-28) |
| Q019 | when the Conviction Monitor flags a recent pick EXIT, is closing it at the next open worth more than holding to the tent | DATASET_PINNED | 2027-05-24 |
| Q023 | do the platform's 80–90 picks do worse on nights its own regime engine calls `strongly_bullish`? | PREREG_LOCKED | 2027-06-07 (exposure check; hard stop 2027-07-19) |
| Q018 | for the same pick, does the day, the swing or the long-term lane plan make the most money — and does the answer depend o | PREREG_LOCKED | 2027-07-12 |
| Q021 | Q021 — GEX pin risk and two-sided paths (does a pinned pick round-trip more often?) | DATASET_PINNED | 2027-08-09 (exposure check; hard stop 2027-09-20) |
| Q015 | do picks scoring 85–90 reach the swing target and then hand it back more often than picks scoring 80–85, and does exitin | DATASET_PINNED | 2027-08-30 |

## 4. Platform issues

_Source: `research/PLATFORM_ISSUES.md`. Statuses: OPEN → HACI_DECIDED:fix/research/accept → BRIEF_WRITTEN → IMPLEMENTED:<sha> → VERIFIED._

| ID | status | issue |
|---|---|---|
| PI-001 | IMPLEMENTED:2d5776c | `uoa_symbol_daily.fwd_return_*` still ~95% degraded; 30d relapsed to 0% from 07-27 — brief: `research/briefs/PI-001_fwd_return_backfill_wind |
| PI-002 | HACI_DECIDED:fix | No coverage watchdog fires on PI-001 (none found in the codebase by that name) |
| PI-003 | HACI_DECIDED:fix | `atr_pct` corrupted around splits (ATR computed on raw bars) |
| PI-004 | HACI_DECIDED:fix | Manual re-runs indistinguishable from nightly runs in `super_agent_select_runs` |
| PI-005 | HACI_DECIDED:accept | `market_regime_daily` not point-in-time before 06-09 (backfilled) |
| PI-006 | HACI_DECIDED:fix | 16 published picks have no target ladder |
| PI-007 | HACI_DECIDED:fix | `industry` populated for only 12% of candidates |
| PI-008 | HACI_DECIDED:accept | Smart-money layer weight forced to 0; CLAUDE.md weights text says 5 |
| PI-009 | HACI_DECIDED:research | L1/L2 targets sit inside one day's range (median 0.31 / 0.55 ATR) — targets are not ATR-scaled |
| PI-010 | HACI_DECIDED:research | Elite (90+) count falling: Apr 8 · May 13 · Jun 12 · Jul 8 · Aug 3 · Sep 2 |
| PI-011 | HACI_DECIDED:fix | Printed swing stop on the wrong side of the pick-night close for 67 of 382 published picks (17.5%) |
| PI-012 | HACI_DECIDED:research | 2026-06-26: three qualified, ranked picks the night's own run audit does not record; no run-history table |
| PI-013 | OPEN | `uoa_symbol_daily.score_swing` / `score_long` overwritten in place by the next-morning OI-confirmation pass; no point-in-time copy |
| PI-014 | OPEN | Conviction Monitor's polarity arm silent since 2026-06-01: `polarity_unavailable_coverage_low` on 100% of in-scope rows, 0 polarity HOLD/EXI |

## 5. Enhancements to build in the platform

_Source: `research/ENHANCEMENTS.md`. `plumbing` items can be built now; `behaviour` items wait for their question's verdict (rule 10/11) unless built as a flag-off internal tool._

| ID | status | build | enhancement |
|---|---|---|---|
| EN-001 | READY | — | Append-only run-history table for SAS runs. `super_agent_select_runs` is updated in place, so the 2026-06-26 unrecorded picks (PI-012) and t |
| EN-002 | BRIEF_WRITTEN | BRIEF_WRITTEN | Speed-to-target on the report card: sessions to first touch of L1/L2/L3 from the next open, shown next to the distance-matched control. Sour |
| EN-003 | PROPOSED | — | Actionable-basis hit rates (next-open and 10:00 ET) alongside the close-basis rate on performance surfaces; entry-timing note "L1 may be gon |
| EN-004 | PROPOSED | — | Distance-matched control rate next to every published hit rate; ATR-scaled ladder placement (L1 ≥ ~0.75 ATR) if the deep-level pattern holds |
| EN-005 | PROPOSED | — | Streak flag on the pick card (first-time / 2 / 3+ consecutive selections); lower default size note for first-time picks. Source: EXPLORE_001 |
| EN-006 | PROPOSED | — | Next-morning gap note for held picks ("gap ≥ 2% against the pick: …"), on the gap-matched result. Source: Q007 §9. |
| EN-007 | PROPOSED | — | Fast-start alert: a pick that touches L1 within two sessions is flagged with its L4 odds from the matched result. Source: Q008 §9. |
| EN-008 | PROPOSED | — | Printed-stop whipsaw disclosure or stop redesign, depending on the pair's verdict. The PI-011 stop-side guard must stay flag-off until Q010  |
| EN-009 | PROPOSED | — | Options context: DTE band chosen from the target's ATR distance instead of a flat 21–35 DTE. Source: EXPLORE_001 #5. |
| EN-010 | PROPOSED | — | Options context exit guidance "close the short leg at the first L3 touch" and a scale-out plan re-derived on that basis. Source: EXPLORE_001 |
| EN-011 | READY | — | Options EOD history feed the Data Steward can pin by sha256: per-contract daily marks with bid/ask, OI and IV for strikes spanning L1–L6 and |
| EN-012 | PROPOSED | — | Quick-exit / capital-recycling mode for sub-elite picks (exit at the first L1 or L2 touch, cap 5 sessions, redeploy); elite (90+) picks keep |
| EN-013 | PROPOSED | — | Bear-pick handling in strong tapes: skip, size down, or label bear picks when the point-in-time regime is `strongly_bullish`. Source: H-062, |
| EN-014 | PROPOSED | — | Earnings-within-3-sessions flag on the pick card, with a "no spread across the print" note. Source: H-064. |
| EN-015 | READY | — | Knowledge-time stamp on every displayed number (computed at 16:05 on the pick night vs next morning), so subscribers and the desk can tell w |
| EN-016 | PROPOSED | — | A larger per-night candidate universe retained in `sas_candidates` — the full scanned universe rather than the scored shortlist, or a per-se |
| EN-017 | PROPOSED | — | Edge-decay monitor: a nightly job that appends, per pick night, the Spearman IC between `overall_score` and the path outcome across all 16:0 |
| EN-018 | PROPOSED | — | Setup labels on the pick card (A flow-led / B projection-led continuation / C catalyst-driven, assigned deterministically from the 16:05 dom |

## 6. Trade ideas (yours; never subscriber-facing until prospective)

_Source: `research/TRADE_IDEAS.md`._

| ID | evidence | tool in platform | idea |
|---|---|---|---|
| TI-001 | UNDER_TEST:Q004 | — | Partial fill after hours on elite (90+) picks at publication, rest at the open. Q004 (decides 2026-10-26) tests whether after-hours, open or |
| TI-002 | IDEA | — | Vertical spread at the next open with the short strike at L3; close the short leg at the first L3 touch instead of holding to expiry. Blocke |
| TI-003 | UNDER_TEST:Q003 | — | Skip or size down first-time picks (not published in the prior 10 sessions); size up 3+ streaks. Q003 decides 2026-12-15. Tool: streak flag  |
| TI-004 | IDEA | — | Don't buy the day-1 dip: no resting limit orders 0.25–0.5 ATR below the pick-night close; a filled dip limit is adverse selection. H-058, ne |
| TI-005 | UNDER_TEST:Q007 | — | For a pick already held from the close: a next-morning gap of ≥ 2% against the pick changes the rest of the trade (exit / don't add); a gap  |
| TI-006 | UNDER_TEST:Q008 | — | Fast start (L1 within two sessions) → hold for L4 rather than take the near target. Q008 decides 2026-12-28 (one extension to ≈ 2027-02-03). |
| TI-007 | UNDER_TEST:Q009 | — | Treat the printed stop as information, not an exit, if it whipsaws trades that go on to reach the target. Q009 decides 2026-11-09 (historica |
| TI-008 | IDEA | — | Capital recycling by band: quick exit at the first L1/L2 touch on sub-elite picks (cap 5 sessions) and redeploy; hold elite picks for L3–L6. |
| TI-009 | IDEA | — | Skip bear picks in strongly bullish tapes (bear picks under-run their matched control in-sample). H-062. Tool: EN-013. |
| TI-010 | IDEA | — | Skip picks with an earnings report 0–3 sessions out; never hold a spread across the print. H-064. Tool: EN-014. |
| TI-011 | IDEA | — | Choose DTE from the target's ATR distance (in-sample: ≤ 1 ATR touched in 1–2 sessions, 2–3 ATR ≈ 8, 3–5 ATR ≈ 17). H-056 DTE half, deferred  |
| TI-012 | UNDER_TEST:Q002 | — | Prefer SAS picks for *speed*: they reach L3/L4 in fewer sessions than distance-matched names, so shorter-dated structures suit them. Q002 de |
| TI-013 | UNDER_TEST:Q006 | — | Trust the deep targets (L4–L6), not L1/L2, as evidence of selection edge; sell strikes against deep targets only. Q006 decides 2026-10-05. T |

## 7. Decisions the desk made for you (autonomous mode)

_Each was a question the desk would once have asked you. It took the recommended or the stricter option (DP-40..45). The locked question stands; to overturn one, say so and the desk registers a successor question._

- **Q011** #8 window and decision date — chose window 2026-06-01..2026-11-06, decide Monday 2026-12-14, one
- **Q011** #9 verdict status of the thin k = 0.5 arm — chose demotion to descriptive decided **at lock** from
- **Q012** #5 window and decision date — chose start nights 2026-06-01..**2026-12-10**, decide **Monday
- **Q012** #6 elite (90+) arm — chose demotion to **descriptive at lock**, printed-or-SUPPRESSED decided at the
- **Q012** #7 capital budget — chose a **60-session budget for both plans**, slot = one unit of capital, ATR
- **Q013** #3 window, decision date and extension — chose DP-43's fixed recipe computed at `record` from the
- **Q014** #4 E2's status — chose both E1 and E2 primary, BH across m = 2, each with its own 80-night gate;
- **Q014** #5 window and decision date — chose DP-43's recipe from 2026-06-01; **settled at `record` on the
- **Q014** #5b rate used — chose the pooled measured 0.4314 E1 nights/session; not taken: the fastest month
- **Q015** #1 H-060's missing baselines — chose the adjacent traded band **80–85** as the primary comparator,
- **Q015** #4 window, decision date and extension — chose, on the Steward's measured numbers, the **slowest**
- **Q017** #5 Planning rate and DEFERRED trigger — chose the haircut rate 0.35 contributing nights/session, window to 2027-04-30, decision Monday 2027-08-09, DEFER below 0.32/session; not taken: unhaircut 0.457 rate, window ends 2027-01-29, decides 2027-05-03 — DP-43. Overturn = successor question.
- **Q018** #1 Primary window start — chose **post-lock only, pick nights ≥ 2026-09-14, decision Monday 2027-07-12**; not taken: window open from 2026-06-01, sealed part descriptive, decides ~4 months sooner — DP-43. Overturn = successor question.
- **Q019** #4 Planning rate, window end and the DEFERRED trigger — chose **0.35 matched-contributing nights per
- **Q020** #1 Rule-14 exception for the mid-trade classifier — chose **DEFERRED: Q020 is not locked and needs
- **Q021** #5 Planning rate and DEFERRED trigger — chose the haircut rate 0.35 contributing nights/session, window to 2027-04-30, decision Monday 2027-08-09, DEFER below 0.32/session; not taken: unhaircut 0.457 rate, window ends 2027-01-29, decides 2027-05-03 — DP-43. Overturn = successor question.
- **Q022** #1 Window start — chose **pick nights from 2026-07-08** (measured at `record`: the first run beginning after both population-defining ships), window to **2027-01-13**, decision **Monday 2027-02-22**; not taken: 2026-06-09 start, ~18 more sealed sessions, decides sooner — DP-43. Overturn = successor question.
- **Q023** #6 Window start — chose **prospective-only, pick nights ≥ 2026-09-14**; not taken: read the sealed nights, decides now, not blind — DP-43. Overturn = successor question.
- **Q023** #3 E2's clock — chose **the committed plan's own lane windows on a 60-session budget**; not taken: truncate at 20 sessions, decides ~2 months sooner — DP-43. Overturn = successor question.
- **Q023** #13 Window end and decision date — chose **114 sessions, ending 2027-02-25, decision Monday 2027-06-07**; not taken: 100 sessions, decides 4 weeks sooner on a coin-flip floor — DP-43/DP-45. Overturn = successor question.
- **Q024** #1 Window start — chose prospective-only from 2026-09-14; not taken: sealed start 2026-07-08, ~2 months sooner — DP-45 (the weeklies have already printed SAS's absolute sealed-period returns, so the SPY arm is not blind on those nights; Q018/Q023 precedent). Overturn = successor question.
- **Q024** #7 Arm below the 80-night floor — chose removed from the deciding set but still printed descriptively at ≥ 20 nights, with the CONFIRMED sentence naming it; not taken: drop the arm silently and let `m` fall — DP-43. Overturn = successor question.
- **Q024** #3 (at `record`) EW / RSP arm — chose **conditional registration**, settled by the Steward's freeze-time pinnability check before `eval.py` exists (`m = 6` if RSP pins, 5 if not); not taken: **defer EW now and lock at `m = 5`** — DP-45: six arms is the harder gate, and dropping an arm before anyone knows whether it can
- **Q024** #9 (at `record`) Window end, decision date, extension — chose **2026-09-14..2027-04-07 (142 sessions), Monday 2027-05-17**, extension Monday 2027-06-28, sized on the measured 0.5652; not taken: **the drafted 2027-03-29, ten weeks sooner**, or the 0.9783 pre-maturity rate that would have been sooner still — DP-43/DP-45.
- **Q025** #6 Window end and decision date — the DP-43 rule fired and **chose DEFERRED**: measured binding rate **0.000 contributing nights per elapsed session** against a 0.35 gate, so there is no honest date; not taken: a wider caliper or a soft sector block, which would have produced nights by weakening the control — DP-43, DP
- **Q025** #6 Window end and decision date — chose **the DP-43 window computed at `record` from the Steward's measured rate, sized at its one-sided 90% lower bound (provisionally window to 2027-01-13, decision Monday 2027-02-22, one extension to 2027-02-26 decided Monday 2027-04-05), and DEFERRED if the binding rate is below 0.35

## 8. Backlog and calendar

- Open hypotheses: **23** · registered: 30 · deferred (data missing): H-041, H-055, H-062, H-067
- Next to register (DP-47 order): H-069, H-070, H-073, H-076, H-075

| decides on | Q |
|---|---|
| 2026-10-05 | Q006 |
| 2026-10-12 | Q002 |
| 2026-10-26 | Q004 |
| 2026-11-09 | Q009 |
| 2026-12-14 | Q011 |
| 2026-12-15 | Q003 |
| 2026-12-28 | Q008 |
| 2027-02-22 | Q010 |
| 2027-02-22 | Q016 |
| 2027-02-22 | Q022 |
| 2027-03-22 | Q012 |
| 2027-03-22 | Q013 |
| 2027-04-05 | Q014 |
| 2027-04-26 | Q007 |
| 2027-05-17 | Q024 |
| 2027-05-24 | Q019 |
| 2027-06-07 | Q023 |
| 2027-07-12 | Q018 |
| 2027-08-09 | Q021 |
| 2027-08-30 | Q015 |

