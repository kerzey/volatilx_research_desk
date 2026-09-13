# Platform issues register

Defects and hazards in the VolatilX platform that the desk has found while doing its own work.
This is the follow-up list Haci asked for. It is separate from the LEDGER (verdicts on research
questions) and the BACKLOG (hypotheses). Anything here that becomes a *behaviour change* to
scoring or selection still goes through a research question and a full IMPLEMENTATION_BRIEF
(CLAUDE.md rule 11). Plain bug fixes take the short route below.

## How an issue gets fixed

1. Desk finds it, records it here with evidence (`path:line`, dates, a reproducing query).
2. Haci decides: **fix** (bug — short route), **research first** (it might be a feature, not a
   bug), or **accept** (document and move on).
3. Short route: `@brief-writer fix-brief PI-NNN` produces `research/briefs/PI-NNN_slug.md` — a
   self-contained prompt for the coding agent in the platform repo, with the reproducing query,
   the expected behaviour, a test, and a rollback. No feature flag is needed for a fix that
   restores intended behaviour, but the brief still names a before/after check.
4. Haci runs the brief in the platform repo, records the PR / SHA here, and the steward
   confirms on the next freeze that the data changed as expected. Then status → `VERIFIED`.

Statuses: `OPEN` · `HACI_DECIDED:<fix|research|accept>` · `BRIEF_WRITTEN` · `IMPLEMENTED:<sha>` · `VERIFIED` · `ACCEPTED`

| ID | Severity | Status | Issue |
|---|---|---|---|
| PI-001 | high | BRIEF_WRITTEN | `uoa_symbol_daily.fwd_return_*` still ~95% degraded; 30d relapsed to 0% from 07-27 — brief: `research/briefs/PI-001_fwd_return_backfill_window.md` |
| PI-002 | high | HACI_DECIDED:fix | No coverage watchdog fires on PI-001 (none found in the codebase by that name) |
| PI-003 | med | HACI_DECIDED:fix | `atr_pct` corrupted around splits (ATR computed on raw bars) |
| PI-004 | med | HACI_DECIDED:fix | Manual re-runs indistinguishable from nightly runs in `super_agent_select_runs` |
| PI-005 | med | HACI_DECIDED:accept | `market_regime_daily` not point-in-time before 06-09 (backfilled) |
| PI-006 | low | HACI_DECIDED:fix | 16 published picks have no target ladder |
| PI-007 | low | HACI_DECIDED:fix | `industry` populated for only 12% of candidates |
| PI-008 | low | HACI_DECIDED:accept | Smart-money layer weight forced to 0; CLAUDE.md weights text says 5 |
| PI-009 | research | HACI_DECIDED:research | L1/L2 targets sit inside one day's range (median 0.31 / 0.55 ATR) — targets are not ATR-scaled |
| PI-010 | research | HACI_DECIDED:research | Elite (90+) count falling: Apr 8 · May 13 · Jun 12 · Jul 8 · Aug 3 · Sep 2 |
| PI-011 | high | HACI_DECIDED:fix | Printed swing stop on the wrong side of the pick-night close for 67 of 382 published picks (17.5%) |
| PI-012 | med | HACI_DECIDED:research | 2026-06-26: three qualified, ranked picks the night's own run audit does not record; no run-history table |
| PI-013 | med | OPEN | `uoa_symbol_daily.score_swing` / `score_long` overwritten in place by the next-morning OI-confirmation pass; no point-in-time copy |

## Detail

### PI-001 — fwd_return freeze not fixed
**Evidence:** FREEZE_v001 §5. `fwd_return_30d_pct` coverage 99% → 0% from 2026-05-20;
14d from 06-12; 5d from 06-26; writes resume 07-06 at ~5% of baseline; 30d back to 0% for
`trading_date ≥ 07-27`, well past maturation. CLAUDE.md said "fixed" — corrected 09-10.
**Desk impact:** none now — the desk computes forward returns from its own price freeze.
**Platform impact:** anything on the product that reads these columns (UOA performance surfaces)
is showing mostly nulls. **Recommend: fix.**

### PI-002 — no watchdog caught PI-001
**Evidence:** a ~95% shortfall persisted for 3+ months. `grep` for a fwd_return coverage
watchdog finds only `scripts/phase2_signals/feasibility.py:7`, a one-off feasibility note.
**Recommend: fix** — a nightly coverage check with a threshold (the desk's own
`research/lib/daily_check.py` shows the shape: trailing median, floor, RED on a drop).

### PI-003 — ATR corrupted around splits
**Evidence:** EXPLORE_001 §9. BKNG `atr_pct` up to 0.49 (true ≈ 0.04–0.06), CVNA up to 0.55.
Cause: ATR over raw bars spanning a split. The W60 grader already de-splits bars
(`scripts/backfill_w60_outcomes.py:185-193`); the ATR path does not.
**Platform impact:** any ATR-based target or sizing on a recently split name is wrong for ~14
sessions. **Recommend: fix**, reusing the grader's de-split.

### PI-004 — manual runs look like nightly runs
**Evidence:** runs for 05-11, 05-12, 05-13, 05-14, 07-06 finished after the next session had
opened (`finished_at`), with mixed-date `spot_close` (TER 07-06: −9.6%). Haci confirms these
were manual development re-runs. Nothing in `super_agent_select_runs` marks them as such.
**Desk impact:** handled by `research/data/exclusions_v001.json`.
**Recommend: fix (small)** — a `run_kind` column (`nightly` / `manual` / `backfill`) written by
the entry point, so the next manual run is self-declaring. Also lets the product hide manual
runs from subscriber-facing history.

### PI-005 — regime history backfilled
**Evidence:** FREEZE_v001 §7. Three `regime_version` rows per date for 01-02..06-08, all
written 06-02 / 06-08. Live same-night writes only from 06-09.
**Recommend: accept**, with the desk rule "regime-stratify from 06-09 only". Nothing to fix
going forward; the label is now written on the night.

### PI-006 — picks without a ladder
16 published picks lack lane targets in `public_payload_json`. A subscriber saw a pick with no
plan. **Recommend: fix** — publication should require all three lanes' targets, or mark the
pick as plan-pending.

### PI-007 — `industry` mostly empty
12% populated. Blocks sector-cluster questions (H-034) and any sector-aware product feature.
**Recommend: fix** — populate from the fundamentals source already used for `fundamental_quality`.

### PI-008 — smart-money weight is zero
`services/super_agent_select_scoring.py:709-710` forces the weight to 0 when
`enable_smart_money_enrichment` is off; the column has been null since April. Not a bug — a
disabled feature — but CLAUDE.md's "smart-money 5" and any marketing of a seven-layer score
overstate it. **Recommend: accept + docs**, or decide whether to enable.

### PI-009 — targets are distance, not forecast *(research first)*
EXPLORE_001: L1/L2 median 0.31 / 0.55 ATR from the close. The strategist prompt asks for two
targets per lane with no volatility scaling (`ai_agents/principal_agent.py:530-575`). If the
sealed period confirms H-053, the change is ATR-scaled target placement — a scoring/plan
behaviour change, so: PREREG → verdict → HUMAN_APPROVED → full brief with a shadow ladder.
**Haci's view (2026-09-10):** near targets being reachable by other stocks is expected; the
differentiator is *how fast* SAS picks reach them. Product direction if that holds: quick
L1/L2 exits and capital recycling on sub-elite picks, deeper holds on elite picks, and
strategies built on speed. Registered as H-065 / H-066; the research question tests speed
against a distance-matched control, unconditionally, before any target redesign.

### PI-010 — elite is thinning *(research first)*
Published 90+ picks per month fell from 12–13 (May–Jun) to 3 (Aug) and 2 (Sep to the 10th);
the candidate median score fell 67.3 → 62.7 on 09-10 (daily check). Haci wants to know why.
Candidates: score-distribution drift after the 06-01 catalyst fix, weaker tape, GEX nulls
(+5 completeness offset), or universe changes. This is a Registrar question (calibration
family F2), not a fix.

### PI-011 — printed stop on the wrong side of the entry
**Evidence:** STEWARD_Q009_exposure §R1(a). 67 of 382 published picks with a swing lane and an L3
(pick nights 2026-06-01..08-12, matured) carry a printed swing `stop` on the **wrong side of the
pick-night close** — for a bullish pick, a stop above the close, i.e. already breached at publication.
**Cause (read-only):** the stop is written by the Principal Strategist off the lane `entry`, which may
stray more than 5% from spot (`services/super_agent_select_service.py:101-111`), and is passed into
`public_payload_json` **unvalidated** (`:94-95`, `:158`), while targets *are* checked against spot and
entry (`:113-152`). It is shown to subscribers on the report card
(`report_center_frontend/components/ReportCard.tsx:254-255`).
**Desk impact:** these picks are excluded from Q009, which therefore speaks for 303 of 383 published
picks (79%).
**Recommend: fix** — a side-and-distance guard on the written stop, mirroring the existing target
guard. **Timing note:** rule 11 applies with unusual force here — a stop-side guard must not go
flag-on before Q010's decision date, or Q010 would be replicating Q009 on a different population
(Q010 §10.6).

### PI-012 — 2026-06-26: ranked picks the run audit does not record
**Evidence:** STEWARD_Q009_exposure §R3 ruling 1. The frozen `sas_candidates` table holds 11 qualified
rows with a `selected_rank` for that trading date; the run's contemporaneous `stats_json` records 8,
all bullish. The three extra bearish rows (DPZ, COIN, AAPL) carry complete lane plans, including swing
stops, with the payload `rank` matching the outer `selected_rank`. It is the only night in 113 with
this mismatch.
**Desk impact:** the whole night is excluded (`exclusions_v003.json`, `uncorroborated_publication_runs`);
usable nights 103 → 102. Q006 and Q007 are locked citing earlier exclusions files and include that
night — flagged to the Red Team for their reviews, never edited.
**Recommend: research first** — the write path cannot be reconstructed from the desk side, because
`super_agent_select_runs` is updated in place with no run-history table. Two questions for the platform:
what wrote those rows, and should there be an append-only run-history/audit table — its absence is what
makes this and the KT-audit re-run nights unrecoverable rather than merely detectable.

### PI-013 — UOA scores rewritten next morning with no audit trail
**Evidence:** Registrar draft of Q014 (H-040), 2026-09-13. volatilx `services/uoa_screener.py:2236-2239`
multiplies `score_swing` and `score_long` in place by `oi_mult` (0.90 / 1.00 / 1.05 / 1.10, stored in
`oi_confirm_mult`, `:2223-2232`) during the next-morning open-interest confirmation pass, and the
bulletin's lists are re-ranked from the mutated scores (`:2245-2303`). `label_*` is written once,
pre-multiplier (`:1728-1734`). The row therefore carries the *morning* score under a column that
every downstream reader treats as the 16:05 ET screener output. FREEZE_v001 §7 flagged the OI lag
for older rows only.
**Desk impact:** any study conditioning on `score_swing` / `score_long` must divide out
`oi_confirm_mult` to recover the pick-night value (Q014 PREREG §2.1 does exactly that; no rule-14
exception needed because the multiplier is stored). Rows where `oi_confirm_mult` is null cannot be
told apart from unconfirmed ones.
**Recommend: fix** — keep the 16:05 score in its own column (`score_swing_pt`, `score_long_pt`) or write
the confirmed score to a new column and leave the original untouched; either way the point-in-time
value must survive. Fix, not research: no behaviour changes, only where a value is stored.
