# Freeze report - manifest_v001

**as_of:** 2026-09-10 - **version:** 001 - **manifest:** research/data/manifest_v001.json
**code_git_sha (research repo):** bbed9aa4d852f8b49d0d8d8d6df91894892126b4
**platform_git_sha:** fa70688bc252d14f8d67e371afafc194731c324e (matches expected; not empty)
**db_role:** research_ro - **verify:** ran the freeze script's --verify mode against the
manifest -> OK, all 11 files, 0 bad

## as_of rationale
super_agent_select_runs shows the nightly pipeline has run every trading session with
status='success' (113/113 runs, no failed/partial rows) through 2026-09-10, with both
audit_path and public_output_path populated for that date. Every other core feeder table
(super_agent_select_candidates_daily, market_regime_daily, uoa_symbol_daily,
gex_symbol_daily, conviction_monitor_daily, projection_pick_bullish_daily,
projection_pick_bearish_daily_v2) also carries data through 2026-09-10. The one exception,
sas_selection_excursion (the ladder/outcome table), is one session behind (max trading_date
2026-09-09) - expected, since it is declared lag_sessions: 1 / post-hoc. as_of = 2026-09-10.

## in_sample_end
Set to 2026-05-29 (last trading date of May 2026). CLAUDE.md records April-May 2026 as a
strong tape and June-August as materially weaker. Splitting at the May/June boundary keeps the
entire strong-tape period in-sample and puts the larger, weaker June 1-Sep 10 stretch
out-of-sample - the conservative direction for Q001's OOS test. This is a data-steward default
only; Q001's PREREG is not locked and Haci sets the final value.

## Schema check
All 11 tables in the freeze config use trading_date as their date column - the guessed WHERE
clauses were correct as written; no column-name SQL fixes were needed. One SQL gap was found
and fixed: outcome_corrections had no WHERE trading_date <= :as_of filter at all (pulled
the whole table unscoped). Added the filter; verified 0 of 795 rows have a null trading_date,
so the fix is safe and lossless for this freeze.

---

## 1. Row counts per table (as_of 2026-09-10)

| table (config key) | source table | rows | file |
|---|---|---:|---|
| sas_candidates | super_agent_select_candidates_daily | 6,479 | v001_sas_candidates.parquet |
| sas_runs | super_agent_select_runs | 113 | v001_sas_runs.parquet |
| sas_excursion (ladder) | sas_selection_excursion | 1,414 | v001_sas_excursion.parquet |
| conviction_monitor | conviction_monitor_daily | 3,339 | v001_conviction_monitor.parquet |
| market_regime | market_regime_daily | 385 | v001_market_regime.parquet |
| uoa_symbol | uoa_symbol_daily | 83,747 | v001_uoa_symbol.parquet |
| gex_symbol | gex_symbol_daily | 7,278 | v001_gex_symbol.parquet |
| whale_ledger | whale_watch_ledger | 0 | v001_whale_ledger.parquet |
| projection_bull | projection_pick_bullish_daily | 2,420 | v001_projection_bull.parquet |
| projection_bear_v2 | projection_pick_bearish_daily_v2 | 1,215 | v001_projection_bear_v2.parquet |
| outcome_corrections | outcome_correction_ledger | 795 | v001_outcome_corrections.parquet |

Of the 6,479 sas_candidates rows: 907 qualified (boolean flag), 915 published
(selected_rank IS NOT NULL); 6,479 - 907 = 5,572 non-qualified.
sas_excursion row count (1,414) is inflated about 2x for most of the history by a dual
computation_version lane (see section 6) - it is NOT 1 row per published pick.

## 2. Maturation cutoffs
- W60 maturation cutoff (candidates): 2026-06-15. Empirically confirmed via
  outcome_sealed_w60: every published pick on or before 2026-06-15 is sealed; zero picks on
  or after 2026-06-16 are sealed (clean boundary, no partial-sealed dates).
- T+10 maturation cutoff (candidates): 2026-08-26. outcome_return_10d_w60 is fully
  populated for published picks through 2026-08-26 and null for every published pick from
  2026-08-27 onward (exactly 10 trading sessions before as_of) - also a clean boundary.

## 3. Null-ladder share
Of 915 published picks, 898 have at least one matching ladder (excursion) row by
(trading_date, symbol); 17 published picks (1.9%) have no ladder row at all. This confirms
and quantifies CLAUDE.md's known "null-ladder denominator" issue.

## 4. Non-qualified candidates: outcome grading coverage
Outcome grading is overwhelmingly a published-only phenomenon in this table, not a
qualified/non-qualified split:

| population | n | outcome_sealed_w60=true | outcome_max_move_pct populated | outcome_return_10d_w60 populated |
|---|---:|---:|---:|---:|
| non-qualified (qualified=false) | 5,572 | 0 | 0 | 136 (2.4%) |
| qualified (qualified=true) | 907 | 416 (46%, consistent with W60 cutoff) | 898 (99%) | 822 (91%) |
| PREREG U_t proxy: overall_score>=70 and completeness>=35 and unpublished | 1,950 | 0 | - | 25 (1.3%) |

Flag for the researcher/registrar: Q001's control universe U_t (score >= 70, unpublished)
is essentially ungraded in this table (0 sealed, 1.3% with any return). This is not fatal -
the PREREG's own metric (section 4, R from Close_t+10 minus Open_t+1) is computed directly
from price data, not from these precomputed outcome columns - but eval.py must not shortcut
control-basket returns from outcome_return_* columns; it needs an independent price join.

## 5. Null spikes

RED - uoa_symbol_daily.fwd_return_* : not fixed, still ~95% degraded.
This is the "May-June 2026 silent fwd_return freeze" named in CLAUDE.md, and the freeze
watchdog's "fixed" label is not supported by the data:
- fwd_return_30d_pct coverage falls from ~99% to 0% starting trading_date 2026-05-20,
  cliff-clean (2026-05-19: 494/498 non-null; 2026-05-20: 0/498).
- fwd_return_14d_pct falls from ~99% to 0% starting 2026-06-12.
- fwd_return_5d_pct falls from ~99% to 0% starting 2026-06-26.
  (Each horizon breaks exactly `horizon` trading days before a common underlying calendar
  cutoff around 2026-07-02 to 2026-07-05 - consistent with the upstream price series itself
  going stale on that date, not a per-horizon bug.)
- Writes resume 2026-07-06, but coverage recovers only to ~5% of the pre-freeze baseline
  (~23-25 of ~495-500 symbols/night for f5/f14) and stays at that degraded level through
  the latest sampled date, 2026-08-14 - six-plus weeks after the nominal "fix."
- fwd_return_30d_pct relapses to 0% again for trading_date >= 2026-07-27; those dates are
  more than 30 trading sessions in the past as of as_of 2026-09-10, so this is not explainable
  by normal right-censoring - it is a live, ongoing gap.
- Contrast: sas_candidates.outcome_return_*_w60 for published picks shows clean, expected
  right-censoring by maturation window with no comparable cliff or relapse - the freeze
  appears isolated to uoa_symbol_daily.fwd_return_*, not the SAS W60 pipeline.
- Recommend the coverage watchdog's threshold be revisited; it is apparently not catching a
  ~95%-of-baseline shortfall.

No other null spikes found: gex_symbol_daily.net_gex (7,277/7,278 populated, 1 null, not a
spike), whale_watch_ledger is 0 rows across the board (confirms known "whale ledger empty"),
sas_candidates.analysis_schema_version is null for ~85-88% of rows every month at a stable
rate (only populated when a full write-up report exists - not a spike, just conditional
population, stable across months, no lineage flag).

## 6. Lineage
scoring_versions_present (auto-detected, confirmed to exist as real columns):
sas_candidates.analysis_schema_version, sas_excursion.computation_version,
market_regime.regime_version, projection_bear_v2.library_version.

- market_regime.regime_version - FLAG, mid-period engine change. Three versions
  (v1, v1.1, v1.2) exist for every trading_date from 2026-01-02 through 2026-06-08 (all written
  by a same-day backfill on 2026-06-02 (v1) and 2026-06-08 (v1.1, v1.2) - see section 7). From
  2026-06-09 onward only v1.2 appears, written live. June 2026 is a mixed month (v1: 5
  dates, v1.1: 3 dates, v1.2: 21 dates within June) - the engine version changed mid-month.
- sas_excursion.computation_version - FLAG, mid-period lane retirement. v1 and v2 run in
  parallel (roughly 1:1, two rows per candidate) from April through June. July 2026 is a
  transition month: only 17 v1 rows vs 177 v2 rows. August and September have v2 only. v1 was
  retired mid-July.
- market_regime.regime_version and sas_excursion.computation_version both explain why raw row
  counts for those two tables are not 1-row-per-candidate-per-night (see section 1).
- projection_bear_v2.library_version - no flag. Constant single value
  (v20260517-221435) across every month in range; no engine change detected.
- sas_candidates.analysis_schema_version - no flag. Only value present is
  sas_report_v1; null the rest of the time (see section 5), stable share by month, no version
  churn.

## 7. Knowledge-time confirmation (sampled ~15-20 rows per table)
| table | declared | confirmed? |
|---|---|---|
| sas_candidates | 16:05 ET, lag 0 | Confirmed - created_at/updated_at cluster same trading_date evening. |
| sas_runs | 16:05 ET, lag 0 | Consistent with started_at/finished_at ~21:0x-21:1x UTC same day. |
| conviction_monitor | 16:02 ET, lag 1 (t+1 feature) | Confirmed - created_at is same trading_date ~20:02 UTC (16:02 ET) in every sampled row, no exceptions. |
| market_regime | 16:05 ET, lag 0 | Corrected. True only for regime_version='v1.2' rows with trading_date >= 2026-06-09 (created_at same-day ~20:05 UTC, one late-write exception: 2026-07-06 posted 2026-07-07 14:23 UTC). For trading_date <= 2026-06-08, no point-in-time row exists at all - the whole period was backfilled on 2026-06-02/2026-06-08, weeks to months after the fact. This is worse than a "revised column" (which validator V3 guards against) - it is a wholesale missing-then-backfilled history. Do not use market_regime_daily as a knowledge-time feature, and do not stratify Q001 by it, for any night before 2026-06-09. The freeze config's availability note has been corrected accordingly. |
| uoa_symbol (general fields) | 16:05 ET, lag 0 | Confirmed on sample. |
| uoa_symbol (oi_* / oi_confirm_* columns) | next-morning, lag 1 | Confirmed as next-morning data, stated explicitly here per protocol. In a 15-row sample, oi_confirm_* fields' updated_at always postdates created_at - ranging from next-day to several weeks later for older, backfilled rows. Never same-day in the sample, so no same-day leak; but "next-morning" is optimistic for older rows where the true finalization lag was much longer. |
| gex_symbol | 16:05 ET, lag 0 | Consistent with row completeness; not specifically timestamp-sampled (no separate live-vs-backfill signal found in schema). |
| sas_excursion (ladder) | post-hoc, lag 1 | Corrected. computed_at sampling shows recomputation weeks-to-months after trading_date (e.g. trading_date 2026-04-21 first computed 2026-07-05, later rows recomputed again on 2026-07-31/08-21/09-10) - not a fixed 1-session lag. Already correctly marked "never a feature"; the lag_sessions value is descriptive only and has been annotated as understated. |
| whale_ledger | post-hoc, lag 1 | Table is empty (0 rows) - nothing to confirm. |
| projection_bull / projection_bear_v2 | 16:05 ET, lag 0 | Consistent with row presence through as_of; not separately timestamp-sampled. |
| outcome_corrections | post-hoc, lag 1 | Never a feature; SQL now scoped to as_of (see schema check above). |

---

## Files
- Manifest: research/data/manifest_v001.json
- Parquet: research/data/v001_*.parquet (11 files, gitignored)
- Config (edited by data-steward): freeze_config.json in research/lib
