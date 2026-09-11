# VolatilX — Research Desk Rules (read by every agent, every session)

You are working on VolatilX, a subscription AI trading-intelligence platform. The
research desk exists to find and *prove* edges in Super Agent Select (SAS), AI Picks,
UOA/Whale Watch, and execution guidance — and to kill ideas that don't survive.
Most questions will return null. That is the design working.

## The platform codebase

The VolatilX code lives in a *separate* repo at `$CODEBASE_DIR` (also listed under
`additionalDirectories`). It is **read-only** from here — reads, `git log/show/blame`, and
`grep` are encouraged; edits, redirects, or `git` write commands into it are blocked. Read it to:
understand what a column actually means (`services/super_agent_select_scoring.py` is the source
of truth for every subscore), find knowledge-time hazards (what is written at 16:05 vs next
morning), cite `path:line` in hypotheses and briefs, and generate enhancement ideas from what
the code does *not* yet do. Every manifest records the platform SHA the data came from.
Changes to the platform happen only through an `IMPLEMENTATION_BRIEF.md` that Haci runs in the
platform repo.

## Non-negotiables

1. **Production is read-only.** Use `$RESEARCH_DB_URL` (read-only role) , `RESEARCH_SAS_TOKEN`,`ALPACA_SECRET_KEY`, `ALPACA_API_KEY` and
   `$PROD_SAS_TOKEN` (read/list only). Never look for, request, or use any other credential.
2. **Write only under `research/`, `docs/`, `playbook/`.** The platform codebase is never edited
   from here; the Brief Writer produces a prompt, Haci executes it in the platform repo.
3. **Pre-register before unsealing.** A question runs only if its `PREREG.md` is committed
   and unchanged since the dataset manifest date. If the PREREG is missing, stop and say so.
4. **Frozen data only.** Every study pins a `research/data/manifest_vNNN.json`. Never query
   live tables for a study result; live queries are for the Data Steward's freeze and for
   daily operational checks only.
5. **Objective = the pick's price path after selection, measured the way it is traded.**
   - Path metrics are primary: for each ladder target L1–L6 (day T1/T2 within 20 trading
     days, swing T1/T2 within 40, long T1/T2 within 60 — volatilx
     services/sas_conviction_card.py:182-195), whether and when it was first touched; the
     counter-direction levels likewise (sas_selection_excursion.counter_touch_dates_json);
     and the order in which levels were hit.
   - Every PREREG states its entry basis: pick-night after-hours (from ~21:10 UTC), next-day
     open, or a next-day intraday trigger. A target already passed at that entry is not a hit.
   - Every hit-rate claim is compared against a distance-matched control: unpublished
     candidates from the same night, with targets placed at the same ATR distance. A hit
     rate without that control is descriptive.
   - Where a PREREG names an execution plan (the committed L1–L6 scale-out, or an option
     structure legged out at target touches), the plan's realized result is reported next
     to the hit rates.
   - Stops are not assumed. Adverse excursion and counter-direction touches are reported,
     not used as exits, unless the PREREG says otherwise.
   - Fixed-horizon close-to-close return is secondary and descriptive.
6. **The unit of inference is the trading night.** Stock rows are aggregated per night first.
   Monte Carlo control draws never add to n. CIs come from date-clustered or block bootstrap;
   p-values from permutation tests. Floors: 20 nights per cell, 80 nights total.
   Every PREREG names a minimum practical effect (MPE); "positive but below MPE" is INCONCLUSIVE.
7. **Regime is the dominant variable.** Every result is reported stratified by
   `market_regime_daily` regime, and by the calendar split in the PREREG. April–May 2026
   was a strong tape; June–August was not. A result that only holds in one period is not a result.
8. **Multiple testing.** Questions are grouped into families in `research/BACKLOG.md`.
   Report Benjamini–Hochberg-adjusted q-values across the family (q ≤ 0.10) alongside raw p.
9. **No judgment in the inner loop.** The Researcher writes a deterministic `eval.py` once;
   the script produces the numbers. Agents interpret outputs; they do not tune while looking.
10. **Four verdicts:** NULL, INCONCLUSIVE, HISTORICALLY_CONFIRMED, PROSPECTIVELY_CONFIRMED.
    Only the last supports a subscriber-facing claim. Null results are ledgered with the same care.
    State transitions are enforced by `research/lib/controller.py`; agents don't argue with it.
14. **Knowledge time.** A feature may be used only if available_time ≤ decision time (16:05 ET
    on the pick night). Declared per table in `freeze_config.availability`; validators enforce.
15. **Enforcement code is off-limits.** `.claude/`, `research/lib/{validators,controller,
    freeze_dataset,eval_utils}.py` are edited by humans outside the desk. Hooks are policy;
    the OS sandbox (`scripts/setup_sandbox.sh`) is containment.
11. **Prove inert, ship dark, flip last.** New code ships flag-off with a byte-identical
    checksum on the old path; validated in shadow; activated only after inertness is confirmed.
12. **Quotable vs research basis.** Subscriber-facing numbers are W60 only (exposure policy).
    W10/W20 windows are allowed for research and must be labelled `NON_QUOTABLE`.
13. **Two-level reporting.** Anything for Haci: one decision paragraph first, detail after.
    Plain English over quant jargon.

## Key facts about the data (verify before relying on them)

- SAS audit table holds *every* candidate with all seven layer subscores, not just the
  published top 8. Non-qualified candidates are the counterfactual — but check whether
  they have outcome grading before using them.
- Weights (v1.6): projection 29 / technical 27 / flow 24 / catalyst 10 / fundamental 5 /
  smart-money 5 / GEX 0 (computed, unused). Timeframe multipliers change effective weights.
- Known findings: directional_pct ≈ base rate; champion symbols graded below base rate;
  whale ledger empty; regime A/B found no bonus-day edge; 88–90 band underperforms 90+;
  re-qualification after a large favorable move is continuation; short DTE underperforms.
- Known data issues: null-ladder denominator (a subset of picks lack ladder rows);
  May–June 2026 silent fwd_return freeze in `uoa_symbol_daily` — NOT fixed as of
  manifest_v001 (2026-09-10): coverage recovered to only ~5% of baseline and
  `fwd_return_30d_pct` relapsed to 0% for trading_date ≥ 2026-07-27. The coverage
  watchdog is not catching it. See research/reports/FREEZE_v001.md §5.
- `market_regime_daily` has no point-in-time label before 2026-06-09 — the whole
  2026-01-02..2026-06-08 range was backfilled on 2026-06-02/06-08. Rule 7 stratification
  is only knowledge-time-legal from 2026-06-09 onward. See FREEZE_v001.md §7.

## Where things live

- `research/LEDGER.md` — every question, every verdict. The desk's memory.
- `research/BACKLOG.md` — hypotheses awaiting registration, grouped by family.
- `research/questions/QNNN_slug/` — PREREG.md, eval.py, results/, REPORT.md.
- `research/data/` — frozen parquet + manifests (gitignored parquet, committed manifests).
- `research/reports/daily/` and `weekly/` — routine check outputs.
- `playbook/` — Haci's own trading rules that survived review (never subscriber-facing until prospective).

## Agents

data-steward · registrar · explorer · researcher · red-team · brief-writer · reporter.
Invoke with `@name`. Stay in your lane; if a task belongs to another agent, say so.
