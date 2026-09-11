# Knowledge-time audit: manifest_v001 re-run nights

Data Steward audit, 2026-09-11. Triggered by Q005 red-team addendum (A1),
`research/questions/Q005_elite_thinning/results/REDTEAM.md` lines 165, 279-293, 332.
Freeze audited: `research/data/manifest_v001.json` (frozen_at 2026-09-10T22:31:32Z).
Method: full re-read of the frozen parquet (`v001_sas_runs.parquet`, `v001_sas_candidates.parquet`,
`v001_conviction_monitor.parquet`, `v001_projection_bull.parquet`, `v001_projection_bear_v2.parquet`,
`v001_market_regime.parquet`, `v001_uoa_symbol.parquet`, `v001_gex_symbol.parquet`) comparing
row-level created/started/finished timestamps against each trading night's 16:05 ET decision
cutoff (America/New_York, DST-aware). One read-only query against the research database
(read-only role) was used for provenance only (listing run/audit-related tables; no live table
was used as a study input).

## Decision

4 of manifest_v001's 113 SAS run/candidate nights are confirmed re-run nights whose frozen
sas_candidates rows are NOT the 16:05 ET output: 2026-04-02, 2026-04-24, 2026-05-15, 2026-07-02.
All 4 are exactly the nights the red team named -- no others exist in sas_candidates/sas_runs.
All 4 are currently UNEXCLUDED (they sit in exclusions_v001.json's manual_runs.late_but_clean
list, which was never wired into any PREREG's exclusion clause). Two registered questions pin
manifest_v001 and both include these 4 nights in their population: Q005 (already LEDGERED
INCONCLUSIVE; red team reran Gate 0 without the 4 nights by hand and the result did not change)
and Q006 (DATASET_PINNED, not yet evaluated -- this matters more here, since nothing has
re-checked its population against A1 yet). I propose adding these 4 nights to a new exclusions
version (exclusions_v002.json, which I have NOT made) alongside the existing 5 manual-run nights
and the 1 non-session night; that is a freeze decision for Haci, not something applied here.
Separately, I found an unrelated, larger-scope knowledge-time gap: uoa_symbol, gex_symbol and
projection_bull rows for roughly 2026-01-07 through 2026-03-20 were routinely written 15-70
hours after the 16:05 ET cutoff on the trading date they carry (confirmed against the platform's
own run-schedule metadata), contradicting their declared available_time_et 16:05, lag_sessions 0.
This predates SAS's own history (first sas_runs row is 2026-04-01) so it does not affect
Q005/Q006, but it would affect any future question that uses uoa_symbol/gex_symbol/projection_bull
for Jan-Mar 2026 nights.

---

## 1. Per-night table: sas_candidates / sas_runs

sas_runs has exactly one row per trading_date (113 rows, no duplicates) -- this table is
updated in place, not append-only. When a night is re-run, the run's start/finish timestamps are
reset to the re-run's clock time but the row's own creation timestamp stays at the original
pick-night write. Every sas_candidates row for that night carries a creation timestamp that
equals the run's (new) finish time, to the second -- i.e. the whole candidate set for that night
was replaced by the re-run, not appended to (spread of candidate-row creation timestamps within a
night is 0 in every one of the 112 nights that have candidates). Because the row is overwritten
in place and no separate run-history/audit table exists in the database (checked: no
super_agent_select_run_attempts/_history/_log table; only super_agent_select_runs itself,
uoa_runs, market_intelligence_runs, bull_bear_conflict_log, sas_v2_order_log,
insider_watch_serve_audit, bot_runtime_settings), the original 16:05 pre-rerun candidate rows
are not recoverable from anything the desk can query. What's frozen in manifest_v001 is the only
surviving version, and it is the re-run's, not the 16:05 decision's.

| trading_date | run id | run created (UTC, ~pick night) | run start/finish (UTC) | hours after 16:05 ET | classification | candidate rows | elite (score>=90) | exclusions_v001.json status today |
|---|---|---|---|---|---|---|---|---|
| 2026-04-01 | 1 | 2026-04-02 00:23:01 | 2026-04-02 03:01:17 / 03:02:25 | +4.3 (created), +6.9 (started) | scheduled nightly, late start same evening -- NOT a re-run (created within 2.6h of started) | 67 | n/a | late_but_clean (no exclusion) |
| 2026-04-02 (RE-RUN) | 2 | 2026-04-02 20:28:41 | 2026-04-04 22:13:12 / 22:19:40 | +0.4 (created), +50.1 (started) | RE-RUN -- candidates carry the re-run's timestamp; config hash matches 04-24's | 67 | 1 | late_but_clean -- NOT excluded |
| 2026-04-03 | 3 | 2026-04-04 17:50:15 | 2026-04-04 17:50:15 / 17:50:15 | +21.8 | non-session (NYSE closed, Good Friday); single run, 0 candidates published | 0 | 0 | non_session_runs -- excluded |
| 2026-04-06 | 4 | 2026-04-07 01:46:42 | 2026-04-07 01:46:42 / 01:52:49 | +5.7 | scheduled nightly, late start same overnight window -- NOT a re-run (gap ~0) | (checked, not anomalous) | n/a | late_but_clean (no exclusion) |
| 2026-04-24 (RE-RUN) | 18 | 2026-04-24 23:01:37 | 2026-04-26 16:53:26 / 16:59:07 | +2.9 (created), +44.8 (started) | RE-RUN -- candidates carry the re-run's timestamp; config hash matches 04-02's | 50 | 0 | late_but_clean -- NOT excluded |
| 2026-05-01 | 23 | 2026-05-01 23:01:14 | 2026-05-02 05:51:24 / 05:51:31 | +2.9 (created), +9.8 (started) | scheduled nightly, late start same overnight window -- NOT a re-run (gap 6.8h, no calendar-day skip) | 52 | n/a | late_but_clean (no exclusion) |
| 2026-05-11 | 29 | 2026-05-11 20:35:11 | 2026-05-16 14:50:29 / 14:58:13 | +0.5 (created), +114.8 (started) | RE-RUN, largest gap in the set | 51 | n/a | manual_runs -- excluded |
| 2026-05-12 | 30 | 2026-05-12 20:34:27 | 2026-05-16 15:09:47 / 15:16:16 | +0.5 (created), +91.1 (started) | RE-RUN | 51 | n/a | manual_runs -- excluded |
| 2026-05-13 | 31 | 2026-05-13 20:35:08 | 2026-05-14 20:03:57 / 20:11:57 | +0.5 (created), +24.0 (started) | RE-RUN | 51 | n/a | manual_runs -- excluded |
| 2026-05-14 | 32 | 2026-05-14 20:36:05 | 2026-05-16 14:03:29 / 14:10:27 | +0.5 (created), +42.0 (started) | RE-RUN | 53 | n/a | manual_runs -- excluded |
| 2026-05-15 (RE-RUN) | 33 | 2026-05-15 20:38:48 | 2026-05-17 23:25:14 / 23:31:30 | +0.6 (created), +51.3 (started) | RE-RUN -- part of the 05-11..05-15 outage window; config hash distinct from all others | 53 | 0 | late_but_clean -- NOT excluded |
| 2026-07-02 (RE-RUN) | 65 | 2026-07-02 22:23:51 | 2026-07-03 14:58:21 / 14:59:48 | +2.3 (created), +18.9 (started) | RE-RUN -- the 07-02 config hash exists only in this re-run (never live at any 16:05 decision); the excluded 07-06 run and 07-07 both use the 06-29 config, so this is not a genuine mid-period change | 61 | 1 | late_but_clean -- NOT excluded |
| 2026-07-06 | 66 | 2026-07-07 20:57:49 | 2026-07-07 20:57:49 / 21:07:22 | +24.9 | manual run, entire run (not just candidates) kicked off ~1 day late; started time within seconds of created time (single continuous run, just late) | (not counted, excluded) | n/a | manual_runs -- excluded |

Rows not shown (the other ~103 nights): candidate-row creation is 0.4-1.3h after the 16:05 ET
cutoff at the 25th-75th percentile, consistent with a same-evening scheduled batch; run start time
is within 2h of run creation time in every case. No other night shows the re-run signature (a
multi-day gap between a run's creation timestamp and its start/finish timestamps).

Confirm/refute the red team's four nights: confirmed exactly as stated -- 2026-04-02 (50h),
2026-04-24 (45h), 2026-05-15 (51h), 2026-07-02 (19h). No fifth night in sas_candidates/sas_runs
shows the pattern. Independent corroboration: I recomputed a hash of each night's run-config JSON
(sha256, not the red team's shorter hash function, so the absolute values differ) and it agrees on
every relationship the red team reported -- 04-02 and 04-24 hash identically to each other and
differently from every other date; 05-15 is unique; 07-02 is unique; 07-06 and 07-07 hash
identically to each other (the "revert" the red team describes is really two nights sharing one
config, not two different configs).


## 2. Cross-check against other decision-time tables, same nights

For the tables the task named specifically (conviction_monitor, projection tables) plus
market_regime, uoa_symbol, gex_symbol (all carry a 16:05, lag_sessions 0, or explicit next-session
claim in the freeze config / manifest availability block), I grouped by trading_date and compared
row creation time to the same cutoff:

- conviction_monitor: only has rows from 2026-05-12 onward among the watch dates (it monitors
  previously-qualified picks, so early nights with no prior picks have no rows). It is late on
  2026-05-12/13/14/15 (25-96h after cutoff) -- matching the same broader May outage as the sas_runs
  re-runs -- and normal on 2026-07-02 (0.001h). It was NOT independently re-run on 04-02/04-24/07-02.
- projection_bull / projection_bear_v2: normal (0-6h) on 04-01, 04-02, 04-06, 04-24, 05-01,
  05-11, 05-12, 07-02; late (20-73h) on 05-13, 05-14, 05-15, 07-06 -- again tracking the May outage
  and the 07-06 manual run, not the SAS-specific 04-02/04-24/07-02 re-runs.
- market_regime: 07-06 shows an 18.3h-late write (posted 2026-07-07 14:23 UTC) -- this is the
  exact exception the manifest's own availability.market_regime note already documents
  independently; I reproduced it, no new finding there. All pre-2026-06-09 dates show the known
  2026-06-02 mass-backfill (already documented in the manifest and CLAUDE.md); 07-02 itself is
  normal (0.002h).
- gex_symbol: unlike the others, on 05-13/05-14/05-15 the earliest row creation time per night
  is normal (about 0.4h after cutoff) but the spread within the night is 21-51 hours and row counts
  are roughly double the typical ~25 -- i.e. the May outage's re-run appended extra gex_symbol
  rows for those three nights rather than replacing the set the way sas_candidates does. Worth
  knowing for provenance; does not change the sas_candidates finding.

Net: the SAS-engine re-run on 04-02, 04-24 and 07-02 was specific to the SAS candidate pipeline --
it did not re-trigger conviction_monitor, projection, market_regime or gex_symbol writes on those
three nights. 05-15 sits inside the broader 05-11..05-15 outage that touched multiple pipelines
(SAS, conviction_monitor, projection, uoa, gex).

## 3. A separate, unrelated finding: uoa_symbol / gex_symbol / projection_bull, 2026-01 to 2026-03

Checking every night in these three tables (not just the SAS watch dates, since the task asked
for every night with a decision-time claim), a large block of history -- roughly 2026-01-07
through 2026-03-20 (42-45 nights per table, about a quarter of each table's date range) -- has row
creation times 15-70 hours after the 16:05 ET cutoff on the trading_date the rows carry. This is
NOT the same phenomenon as the SAS re-runs (no multi-day start-time-reset signature; instead
the entire nightly job ran late). I checked this against the platform's own uoa_runs schedule
metadata (read-only query, provenance only): e.g. the "nightly" job for trading_date 2026-01-07
started 2026-01-09 18:51 UTC -- the scheduled job itself ran nearly two full sessions late during
this period, it wasn't a manual re-run. This contradicts the declared available_time_et 16:05,
lag_sessions 0 for uoa_symbol/gex_symbol/projection_bull for this stretch of history.

This does not affect Q005 or Q006: sas_runs has no rows before 2026-04-01 (SAS's own history
starts then), so neither question's population reaches into the Jan-Mar period. It would affect
any future question that uses uoa_symbol, gex_symbol or projection_bull for nights before
approximately 2026-03-23 (the last late night in the sample) and treats row creation as
16:05-ET-available. Flagging for the record; no action taken, no manifest/exclusions change
proposed for it here since it's out of scope for the A1 trigger.

## 4. Cross-check against exclusions_v001.json

exclusions_v001.json's manual_runs block already distinguishes two sub-lists:
- trading_dates (excluded): 2026-05-11, 05-12, 05-13, 05-14, 2026-07-06 -- all 5 confirmed above
  as genuine re-runs/late-started runs; correctly excluded.
- late_but_clean (NOT excluded): 2026-04-01, 04-02, 04-03, 04-06, 04-24, 05-01, 05-15, 07-02 --
  this list already flagged these 8 dates as something, but treated all 8 as equally benign. My
  per-night check splits it: 04-01, 04-06, 05-01 are genuinely benign (late-starting but single,
  continuous scheduled runs, no timestamp reset, no config swap). 04-02, 04-24, 05-15 and 07-02
  are not "clean" by the same standard applied to the excluded 5 -- they show the identical
  creation-frozen/start-time-reset re-run signature, just with smaller gaps (19-51h vs 24-115h for
  the excluded set). 04-03 is separately covered by non_session_runs and correctly excluded there.

Additionally, exclusions_v001.json has no entry at all for catalyst_layer_regime_change
interacting with these dates, and no note about the 06-26 mixed-state night the red team flagged
separately (F7) -- that one is a different defect (partial row mutation, not a re-run) and is out
of scope for this audit, which was scoped to the re-run pattern.


## 5. Which locked/registered questions are affected

Checked every research/questions/*/state.json and PREREG. Only two name manifest_v001:

- Q005 (research/questions/Q005_elite_thinning): state LEDGERED, verdict INCONCLUSIVE.
  PREREG's population is "all sas_runs nights minus the 5 manual_runs exclusions" -- includes
  04-02, 04-24, 05-15, 07-02. The red team already tested sensitivity by hand: dropping the 4
  nights and recomputing Gate 0 gives P0 28/55=0.509 vs P1 11/48=0.229 (permutation p 0.010 vs the
  registered 0.018) -- the finding holds and is slightly stronger without them. No re-run of
  eval.py was performed by the red team or by me, per instruction not to run/evaluate any question.
- Q006 (research/questions/Q006_control_cohort_path): state DATASET_PINNED, not yet
  evaluated. PREREG's exclusions section also cites only the 5 manual_runs dates, nothing about
  late_but_clean. Its population as currently specified includes 04-02, 04-24, 05-15 and
  07-02 -- this has not been sensitivity-checked by anyone yet, since Q006 hasn't run. This is
  the more consequential exposure: Q006 is a path-objective question over the same
  candidate/ladder population, and its eval.py has not been written/run against a version of the
  population that excludes these 4 nights.
- Q001-Q004 do not pin manifest_v001 (Q001 REJECTED/superseded by Q006; Q002-Q004 are
  PREREG_DRAFT, unregistered, no manifest pin yet).

No question was run or evaluated as part of this audit.

## 6. Is this a validator gap?

Yes, precisely. The desk's v4 knowledge-time check (function v4_knowledge_time, in the
validators module under research/lib) only checks that every table name referenced in an eval.py
has some entry in the freeze config's availability block -- a lexical/static check of declaration
presence: it collects table names mentioned in eval.py's source text and flags any that lack an
availability entry. That is all it does.

It never opens the frozen parquet and never compares a declared available_time_et/lag_sessions
against the actual creation/start timestamps of the rows a study consumes. So a table can be
correctly declared (as sas_candidates is, in both the freeze config and manifest_v001) and
still be wrong for a subset of nights, and this validator has no way to see that -- the defect
lives in the data, not in eval.py's table references. The freeze protocol's own step ("Knowledge
time: ... confirm the declared lag against the actual write timestamps, sample 20 rows") is a
sampling check for the same reason the original sas_candidates note says "Verified: sampled
created/updated timestamps cluster same trading_date evening" -- a 20-row sample out of 6,479 rows
has roughly a 50% chance of missing all ~4 re-run nights' ~231 rows entirely, since 231/6479 is
about 3.6%. That is almost certainly how the original freeze verification missed this: the check
exists, but its sample size is too small relative to how rare (but real) the re-run nights are. I
am not proposing a change to the validator file itself (out of the desk's write scope) -- flagging
the gap for whoever owns that file.

## 7. PROPOSED exclusions addendum (not applied -- freeze decision for Haci)

Below is a proposed manual_runs extension for a future exclusions_v002.json. I have not
created or modified any exclusions or manifest file.

    {
      "manual_runs": {
        "trading_dates_add": ["2026-04-02", "2026-04-24", "2026-05-15", "2026-07-02"],
        "reason": "sas_candidates rows for these nights carry a creation timestamp and config from a re-run 19-51h after the 16:05 ET decision (run start/finish reset, run creation timestamp unchanged); the 16:05 candidate set is not recoverable (no run-history table). Confirmed 2026-09-11, corroborates Q005 red-team A1. Moved from manual_runs.late_but_clean, which should be reduced to [2026-04-01, 2026-04-03, 2026-04-06, 2026-05-01]."
      },
      "sas_candidates_availability_note_correction": "The freeze config's availability.sas_candidates note currently reads: written live at decision time; point-in-time by construction; verified by a sample of created/updated timestamps clustering same trading_date evening. This should be amended to note the 4 known re-run nights above and that the run-metadata row is updated in place (no append-only history), so re-run nights cannot be recovered to their 16:05 state, only excluded.",
      "affected_questions": {
        "Q005": "LEDGERED/INCONCLUSIVE already; red team hand-check shows dropping these 4 nights does not change the verdict (effect is slightly stronger without them). No re-run required by this finding alone, but the ledger/report should note the exclusion decision once made.",
        "Q006": "DATASET_PINNED, not yet evaluated. Recommend Haci decide on the exclusions update before Q006's eval.py is written/run, since its population as registered currently includes all 4 nights and has not been sensitivity-checked."
      }
    }

If Haci approves, the next freeze step is a new exclusions_v002.json (new version, per the
"never overwrite an existing manifest/exclusions" rule) and, if it changes either question's
population, a note on the relevant state.json/ledger row -- not a new manifest, since the
underlying data doesn't need re-pulling, only the exclusion policy changes.

