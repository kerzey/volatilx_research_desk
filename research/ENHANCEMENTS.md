# Platform enhancements — things VolatilX could do that it does not do today

Separate from `PLATFORM_ISSUES.md` (defects) and `BACKLOG.md` (hypotheses). An enhancement is a
change Haci might build in the platform. The desk proposes; Haci picks; the desk writes the prompt
and checks the result. Nothing here reaches subscribers on the strength of a hypothesis — that is
CLAUDE.md rules 10–12 and they do not bend.

## Two kinds

- **plumbing** — no subscriber-visible number changes (an audit table, a data feed, a stamp, a
  guard). Short route, like a fix: prompt → implement → verify. Buildable now.
- **behaviour** — changes what is scored, selected, shown or recommended. Its **gate** is a research
  question's verdict: HISTORICALLY_CONFIRMED + `HUMAN_APPROVED` → full `IMPLEMENTATION_BRIEF.md`
  with a shadow column (rule 11). Before the gate it may still be built as an **internal tool**:
  flag-off, visible only to Haci, no subscriber copy — the brief says so in its header
  (`INTERNAL_TOOL`).

## How an enhancement gets built

1. Desk proposes it here (`PROPOSED`, or `READY` for plumbing) with the source and the gate.
2. Haci asks: `/desk-run prompt EN-NNN`. Asking *is* the decision; the desk sets
   `HACI_DECIDED:build` and `@brief-writer brief EN-NNN` writes `research/briefs/EN-NNN_slug.md`.
3. Haci runs the prompt in the platform repo (Codex or Claude), then `/desk-run verify EN-NNN <sha>`.
4. The Data Steward runs the brief's before/after check and sets `VERIFIED` or `FAILED`.

Build statuses: `—` · `HACI_DECIDED:build` · `BRIEF_WRITTEN` · `IMPLEMENTED:<sha>` · `VERIFIED` · `FAILED` · `DROPPED`

| ID | Kind | Status | Gate | Build | Enhancement |
|---|---|---|---|---|---|
| EN-001 | plumbing | READY | — | — | Append-only run-history table for SAS runs. `super_agent_select_runs` is updated in place, so the 2026-06-26 unrecorded picks (PI-012) and the KT-audit re-run nights cannot be reconstructed, only detected. Source: STEWARD_Q009 §R3, KT_AUDIT. |
| EN-002 | behaviour | BRIEF_WRITTEN | Q002 (2026-10-12) | VERIFIED (2026-09-14, VERIFY_EN-002_2026-09-14.md; original FAIL receipt preserved) | Speed-to-target on the report card: sessions to first touch of L1/L2/L3 from the next open, shown next to the distance-matched control. Source: EXPLORE_001 §E, H-065. |
| EN-003 | behaviour | PROPOSED | Q004 (2026-10-26) | — | Actionable-basis hit rates (next-open and 10:00 ET) alongside the close-basis rate on performance surfaces; entry-timing note "L1 may be gone by the open". Source: EXPLORE_001 #4. |
| EN-004 | behaviour | PROPOSED | Q006 (2026-10-05) | — | Distance-matched control rate next to every published hit rate; ATR-scaled ladder placement (L1 ≥ ~0.75 ATR) if the deep-level pattern holds. Source: PI-009, EXPLORE_001 #2, H-053. |
| EN-005 | behaviour | PROPOSED | Q003 (2026-12-15) | — | Streak flag on the pick card (first-time / 2 / 3+ consecutive selections); lower default size note for first-time picks. Source: EXPLORE_001 #3. |
| EN-006 | behaviour | PROPOSED | Q007 (≤ 2027-06-30) | — | Next-morning gap note for held picks ("gap ≥ 2% against the pick: …"), on the gap-matched result. Source: Q007 §9. |
| EN-007 | behaviour | PROPOSED | Q008 (2026-12-28) | — | Fast-start alert: a pick that touches L1 within two sessions is flagged with its L4 odds from the matched result. Source: Q008 §9. |
| EN-008 | behaviour | PROPOSED | Q009 → Q010 (≈ 2027-02-22) | — | Printed-stop whipsaw disclosure or stop redesign, depending on the pair's verdict. The PI-011 stop-side guard must stay flag-off until Q010 decides. Source: Q009 §9, Q010 §10.6. |
| EN-009 | behaviour | PROPOSED | H-056 DTE half (needs EN-011) | — | Options context: DTE band chosen from the target's ATR distance instead of a flat 21–35 DTE. Source: EXPLORE_001 #5. |
| EN-010 | behaviour | PROPOSED | H-055 (needs EN-011) | — | Options context exit guidance "close the short leg at the first L3 touch" and a scale-out plan re-derived on that basis. Source: EXPLORE_001 #1. |
| EN-011 | plumbing | READY | — | — | Options EOD history feed the Data Steward can pin by sha256: per-contract daily marks with bid/ask, OI and IV for strikes spanning L1–L6 and 7–60 DTE, for every candidate symbol. Unblocks H-055 and H-056. Spec: `research/questions/DEFERRED.md`. |
| EN-012 | behaviour | PROPOSED | H-066 (to register) | — | Quick-exit / capital-recycling mode for sub-elite picks (exit at the first L1 or L2 touch, cap 5 sessions, redeploy); elite (90+) picks keep the deep-target plan. Source: PI-009 Haci's view, H-066. |
| EN-013 | behaviour | PROPOSED | H-062 (to register) | — | Bear-pick handling in strong tapes: skip, size down, or label bear picks when the point-in-time regime is `strongly_bullish`. Source: H-062, weekly 2026-09-12. |
| EN-014 | behaviour | PROPOSED | H-064 (to register) | — | Earnings-within-3-sessions flag on the pick card, with a "no spread across the print" note. Source: H-064. |
| EN-015 | plumbing | READY | — | — | Knowledge-time stamp on every displayed number (computed at 16:05 on the pick night vs next morning), so subscribers and the desk can tell what was knowable at publication. Source: rule 14, KT_AUDIT_manifest_v001. |
| EN-016 | plumbing | PROPOSED | — | — | A larger per-night candidate universe retained in `sas_candidates` — the full scanned universe rather than the scored shortlist, or a per-sector floor on candidates retained — so exposure-matched controls exist: ~50–60 candidates a night across eleven sectors leaves a median of 5–7 same-sector names, and only 7.6% of picks find ≥ 3 same-sector twins inside a five-feature caliper (0 of 46 nights carried 3). No subscriber-visible number changes; lowering the *admission* bar instead would be a behaviour change. Source: `research/questions/DEFERRED.md` Q025/H-068 re-try condition (b), `research/reports/STEWARD_Q025_exposure.md` §(d)/§(h). |
| EN-017 | plumbing | PROPOSED | — | — | Edge-decay monitor: a nightly job that appends, per pick night, the Spearman IC between `overall_score` and the path outcome across all 16:05 candidates (matured 20 sessions later, graded from bars) and the control-adjusted L3-touch excess of the published slate, into an append-only table with a rolling 20-night mean and a CUSUM flag. Internal only (`INTERNAL_TOOL`, flag-off); no subscriber-visible number. The desk's H-082 decides whether a fall is structural; the monitor is what makes the fall visible in production before the desk's next freeze. Source: H-082 / H-073 (Master Hypothesis Program H12 / H3). |
| EN-018 | behaviour | PROPOSED | H-083 (to register; prospective, ≈ 12 months) | — | Setup labels on the pick card (A flow-led / B projection-led continuation / C catalyst-driven, assigned deterministically from the 16:05 dominant layer) and, if H-083 confirms, per-setup ranking in place of the universal 0–100 cut. Ships label-only and flag-off first (rule 11); the ranking change is gated on H-083's verdict and on H-080 (if the 90 threshold is stable the universal score stays). Source: H-083 (Master Hypothesis Program H13). |
| EN-019 | plumbing | PROPOSED | — | — | **Make the multi-agent technical reports researchable going forward.** Run the internal batch analysis on a fixed, pre-declared universe every session at a fixed time (for example the night's SAS candidates plus a stable liquid list, the same symbols whether or not anyone asked), stamp every report with an explicit time zone and a `trigger` field (PI-019), and keep writing append-only history. Today 73.6% of the 697 historical reports come from a hand-picked watchlist of about seven names re-analysed every few days, which no F9 question can decide on; a fixed universe gives each night its own distance-matched controls. Gates nothing and changes nothing a subscriber sees. Source: F9 inventory 2026-09-14, H-086..H-090. |

## Detail

Add a `### EN-NNN` block here when an item needs more than the table row: the evidence, the
exact surface it touches (`path:line` in the platform repo), and what the verification check is.
The brief-writer copies from here.
