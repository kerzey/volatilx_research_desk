# Research desk — board

_Generated 2026-09-13 by `research/lib/board.py`. Do not edit; edit the source files and re-run. Ask the desk for anything on this page in plain words, or use the commands shown._

## 1. Waiting on you

- nothing. The desk has no item that only you can move.

**Ready when you ask** (you already decided these; the desk writes the prompt on request):

- **PI-001** — `uoa_symbol_daily.fwd_return_*` still ~95% degraded; 30d relapsed to 0% from 07-27  →  `/desk-run prompt PI-001`
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
| Q011 | is it better to rest a limit order below the pick-night close and buy the day-1 dip, or just buy at the next open? | DATASET_PINNED | 2026-12-14 |
| Q003 | are first-time picks weaker than picks SAS keeps re-selecting? | DATASET_PINNED | 2026-12-15 |
| Q008 | when a pick held from the pick-night close reaches its first target within two sessions, is it more likely to go on to i | DATASET_PINNED | 2026-12-28 |
| Q010 | does Q009's stop result repeat on nights nobody had seen when it was registered? | PREREG_LOCKED | 2027-02-22 |
| Q007 | for a pick already held from the pick-night close, does a next-morning gap of more than 2% predict the rest of the trade | DATASET_PINNED | 2027-04-26 (exposure check; hard stop 2027-06-30) |
| Q009 | does the stop printed on a SAS pick shake traders out of trades that would have reached the target anyway? | PREREG_LOCKED | — |

## 4. Platform issues

_Source: `research/PLATFORM_ISSUES.md`. Statuses: OPEN → HACI_DECIDED:fix/research/accept → BRIEF_WRITTEN → IMPLEMENTED:<sha> → VERIFIED._

| ID | status | issue |
|---|---|---|
| PI-001 | HACI_DECIDED:fix | `uoa_symbol_daily.fwd_return_*` still ~95% degraded; 30d relapsed to 0% from 07-27 |
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

## 5. Enhancements to build in the platform

_Source: `research/ENHANCEMENTS.md`. `plumbing` items can be built now; `behaviour` items wait for their question's verdict (rule 10/11) unless built as a flag-off internal tool._

| ID | status | build | enhancement |
|---|---|---|---|
| EN-001 | READY | — | Append-only run-history table for SAS runs. `super_agent_select_runs` is updated in place, so the 2026-06-26 unrecorded picks (PI-012) and t |
| EN-002 | PROPOSED | — | Speed-to-target on the report card: sessions to first touch of L1/L2/L3 from the next open, shown next to the distance-matched control. Sour |
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

## 8. Backlog and calendar

- Open hypotheses: **23** · registered: 12 · deferred (data missing): H-055
- Next to register (DP-47 order): H-053, H-066, H-064, H-062, H-040

| decides on | Q |
|---|---|
| 2026-10-05 | Q006 |
| 2026-10-12 | Q002 |
| 2026-10-26 | Q004 |
| 2026-12-14 | Q011 |
| 2026-12-15 | Q003 |
| 2026-12-28 | Q008 |
| 2027-02-22 | Q010 |
| 2027-04-26 | Q007 |

