# Decision policy — standing answers for pre-registration decisions

Read by the Registrar before drafting and by the Decision-maker when it resolves a draft's
"Open decisions before lock". Purpose: a question that comes up in every PREREG is decided
**once**, the same way, and never put to Haci twice. Each entry has an id (`DP-nn`), the rule,
and where it came from. Nothing here overrides CLAUDE.md.

Two kinds of entry:
- **Confirmed** — Haci said so. Applied without asking.
- **Default** — a desk convention chosen for consistency. Applied without asking; Haci can
  overturn it at any time. When he does, edit the entry in place and note the date — don't add
  a second entry that contradicts it.

A third list, **Reserved for Haci**, names the decisions that are always asked.

How entries get added: when Haci answers a question the Decision-maker put to him, the
Decision-maker appends it here as Confirmed (naming the question it came from) if the answer
generalises beyond that one question. One-off answers stay in that question's `DECISIONS.md`.

## Confirmed (Haci)

| id | rule | source |
|---|---|---|
| DP-01 | The objective is the pick's price path: first touch of L1–L6 within the lane windows (day 20 / swing 40 / long 60 sessions), measured from a stated entry, against a distance-matched control. Fixed-horizon return is descriptive only. | CLAUDE.md rule 5 amendment, Haci 2026-09-10 |
| DP-02 | Stops are never assumed as exits. Adverse excursion and counter-direction touches are reported. A question *about* stops studies the platform's printed stop; it does not make the desk exit on it. | rule 5; Haci 2026-09-10: "I do not trade by considering stops" |
| DP-03 | Entry bases in scope: (a) pick-night after-hours, from the run's actual `finished_at` — Haci's partial after-hours buy on elite (90+) picks; (b) next-session open — his option-spread entry, legs closed as targets are touched. A target already passed at entry is not a hit. | Haci 2026-09-10; DATA_NOTES |
| DP-04 | A night is excluded when the run's `finished_at` is later than the next session's open (a manual re-run), or the run is dated on a non-session day. | Haci 2026-09-10; `exclusions_v001.json` |
| DP-05 | Rule-14 exception: the session t+1 official 09:30 ET open may be used as a conditioning variable for the **gap only** (Q007 §6.1). It does not extend to any other t+1 quantity. Every *new* rule-14 exception is asked (R-1). | Haci 2026-09-12 |
| DP-06 | The catalyst layer is a different feature before and after 2026-06-01 (earnings fix `69ef05f`). Earnings questions are sealed-period only, or split at that date. | Haci 2026-09-10; DATA_NOTES |
| DP-07 | Platform defects are not research questions. They go to `PLATFORM_ISSUES.md`; Haci marks fix / research / accept. | Haci 2026-09-10 |
| DP-08 | Speed is part of the claim: the desk measures *when* a target is first touched (sessions from entry), not only whether. L1/L2 are reachable by many stocks; the edge to test is speed. | Haci 2026-09-10; H-065 / H-066 |
| DP-09 | When the entry basis is the next-session open spread and L3 is the primary level, the primary clock is **L3 within 20 sessions** (the spread horizon, ≈ expiry), not the platform's 40-session swing-lane window; the 40-session result is reported alongside, descriptively, wherever it has matured. Sample floors and decision dates are computed on the 20-session window. | Haci 2026-09-12, Q007 |
| DP-10 | MPE for any **per-trade endpoint denominated in ATR**: **0.25 ATR per trade**. Set once, applies to every such endpoint; smaller values are not accepted and a larger one needs a one-line reason from the Registrar. | Haci 2026-09-12, Q007 |

## Defaults (desk convention; Haci can overturn)

| id | rule | why | first applied |
|---|---|---|---|
| DP-20 | MPE for a control-adjusted or within-night **touch-rate** endpoint: **+5.0 pp**. The Registrar may propose a larger MPE for an endpoint with no control (a raw arm contrast) with a one-line reason; a smaller one is not accepted. | consistency across F7; in force in Q006, locked by Haci | Q006, 2026-09-11 |
| DP-21 | Rule 6 floors read as **80 contributing nights per primary endpoint** and 20 per stratum cell. "80 eligible nights with ≥ 20 contributing" is the weaker reading and is not used. | the stricter of the two readings already in drafts (Q008 vs Q007) | 2026-09-12 |
| DP-22 | Exclusions: a draft cites the **newest** exclusions file. When the KT audit or the Steward finds new re-run nights, the Steward issues the next `exclusions_vNNN.json` *before* the batch is locked, and drafts cite it. Locked PREREGs are not edited; the file they cite stands. | one list, not per-question lists | 2026-09-12 |
| DP-23 | Successor freezes: a question whose floors need nights after `manifest_v001` is locked **now**, pinned to v001, with its successor manifests pinned at the decision date (the Q006 pattern). Successor price freezes always include **all candidate symbols, published and unpublished**, plus hourly bars for published symbols. | Q006 precedent; every path question needs the control cohort | 2026-09-12 |
| DP-24 | PROSPECTIVELY_CONFIRMED needs **≥ 30 contributing nights dated after the lock commit**. If the chosen window cannot supply 30, the decision date moves (that move is R-3); the clause does not weaken. | Q002 / Q004 precedent | 2026-09-12 |
| DP-25 | Units and cuts come from the BACKLOG hypothesis as written (H-030's "2%" is percent, not ATR). The Registrar does not re-unit a hypothesis; a re-unit is a new hypothesis. | the test stays the one that was proposed | 2026-09-12 |
| DP-26 | Registrar-chosen bands and clocks (a 1% "flat" band, TIGHT/MID/WIDE ATR buckets, a 2-session fast-start clock) stand as drafted, provided they were not derived from sealed outcomes. A gap-through at entry is never a hit. | conventions, not findings; rule 5 | 2026-09-12 |
| DP-27 | Ties: a same-session stop and target that hourly bars cannot order count **stop-first** — the outcome less favourable to the hypothesis. | conservative | 2026-09-12 |
| DP-28 | Publication predicate: `qualified IS TRUE AND selected_rank IS NOT NULL`; dark-lane rows are excluded from every arm. A locked PREREG with a looser predicate is flagged to the Red Team for that question's review, never edited. | Q008 draft finding | 2026-09-12 |
| DP-29 | Family is assigned by the primary endpoint's subject (exits → F6, path after selection → F4, calibration → F2). An overlapping BACKLOG hypothesis is marked *merged into QNNN* rather than counted twice. | rule 8 bookkeeping | 2026-09-12 |
| DP-30 | Stop line for a stop question: the printed stop of the lane whose target is the primary endpoint. | technical consistency | 2026-09-12 |

## Reserved for Haci (always asked)

- **R-1** Any new rule-14 (knowledge-time) exception.
- **R-2** Any choice that encodes how he trades: a horizon that differs from the platform's lane
  window (e.g. L3 within 20 sessions for a spread), which target level is primary, the lane, an
  option structure, what counts as "elite".
- **R-3** Trade-offs between waiting and sample size: the decision date, dropping an arm or a
  primary endpoint, sending a question to DEFERRED.
- **R-4** MPEs in money or ATR units — they encode his costs and slippage. Once he sets one for a
  metric type it becomes a DP entry and is not asked again.
- **R-5** Anything the Decision-maker cannot settle with strong alignment — if its own write-up of
  the choice would need an "on the other hand", it asks.
