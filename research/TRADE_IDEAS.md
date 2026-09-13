# Trade ideas — how Haci could trade on what the platform produces

His list, not the subscribers'. Every idea here is either untested, under test, or proven on
history; nothing becomes subscriber-facing until it is PROSPECTIVELY_CONFIRMED (rule 10). The
point of the list: see at a glance what the desk is testing for his own trading, what it has
proved, and which ideas could become a tool in the platform.

Evidence statuses: `IDEA` (a hypothesis, may not be registered yet) · `UNDER_TEST:QNNN` (locked; the desk
looks once on the decision date) · `HISTORICAL` (HISTORICALLY_CONFIRMED; playbook entry; trade small) ·
`PROSPECTIVE` (held up on nights after the lock) · `KILLED` (NULL — don't trade it).

Tool-in-platform statuses (an idea can be built as an **internal, flag-off, Haci-only tool** at any
stage; a subscriber-facing version needs the gate in `ENHANCEMENTS.md`): `—` · `HACI_DECIDED:build` ·
`BRIEF_WRITTEN` · `IMPLEMENTED:<sha>` · `VERIFIED`. Ask with `/desk-run prompt TI-NNN`.

| ID | Evidence | Tool | Idea |
|---|---|---|---|
| TI-001 | UNDER_TEST:Q004 | — | Partial fill after hours on elite (90+) picks at publication, rest at the open. Q004 (decides 2026-10-26) tests whether after-hours, open or 10:00 entry changes the path. Tool: an after-hours fill alert keyed to the run's `finished_at` for 90+ picks. |
| TI-002 | IDEA | — | Vertical spread at the next open with the short strike at L3; close the short leg at the first L3 touch instead of holding to expiry. Blocked for a real answer until an options price history exists (H-055, EN-011); Q002 tests the speed half on the stock path. Tool: L3-touch alert. |
| TI-003 | UNDER_TEST:Q003 | — | Skip or size down first-time picks (not published in the prior 10 sessions); size up 3+ streaks. Q003 decides 2026-12-15. Tool: streak flag (EN-005). |
| TI-004 | IDEA | — | Don't buy the day-1 dip: no resting limit orders 0.25–0.5 ATR below the pick-night close; a filled dip limit is adverse selection. H-058, next to register. |
| TI-005 | UNDER_TEST:Q007 | — | For a pick already held from the close: a next-morning gap of ≥ 2% against the pick changes the rest of the trade (exit / don't add); a gap with it does not. Q007 decides on exposure, hard stop 2027-06-30. Tool: morning gap note (EN-006). |
| TI-006 | UNDER_TEST:Q008 | — | Fast start (L1 within two sessions) → hold for L4 rather than take the near target. Q008 decides 2026-12-28 (one extension to ≈ 2027-02-03). Tool: fast-start alert (EN-007). |
| TI-007 | UNDER_TEST:Q009 | — | Treat the printed stop as information, not an exit, if it whipsaws trades that go on to reach the target. Q009 decides 2026-11-09 (historical only, label `HISTORICAL_ONLY`); Q010 is the prospective replication (≈ 2027-02-22). Tool: EN-008. |
| TI-008 | IDEA | — | Capital recycling by band: quick exit at the first L1/L2 touch on sub-elite picks (cap 5 sessions) and redeploy; hold elite picks for L3–L6. H-066. Tool: EN-012. |
| TI-009 | IDEA | — | Skip bear picks in strongly bullish tapes (bear picks under-run their matched control in-sample). H-062. Tool: EN-013. |
| TI-010 | IDEA | — | Skip picks with an earnings report 0–3 sessions out; never hold a spread across the print. H-064. Tool: EN-014. |
| TI-011 | IDEA | — | Choose DTE from the target's ATR distance (in-sample: ≤ 1 ATR touched in 1–2 sessions, 2–3 ATR ≈ 8, 3–5 ATR ≈ 17). H-056 DTE half, deferred until EN-011. Tool: EN-009. |
| TI-012 | UNDER_TEST:Q002 | — | Prefer SAS picks for *speed*: they reach L3/L4 in fewer sessions than distance-matched names, so shorter-dated structures suit them. Q002 decides 2026-10-12. Tool: EN-002. |
| TI-013 | UNDER_TEST:Q006 | — | Trust the deep targets (L4–L6), not L1/L2, as evidence of selection edge; sell strikes against deep targets only. Q006 decides 2026-10-05. Tool: EN-004. |

## Detail

Add a `### TI-NNN` block when an idea needs more than a row: the exact rule, sizing, what the
verdict changed, and the playbook file once one exists (`playbook/PB-NNN_slug.md`).
