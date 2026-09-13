# Data notes — what the desk knows about the data that the tables don't say

Read this before writing a PREREG or an eval.py. Each note gives the fact, who established it,
and what a study must do about it. Machine-readable exclusions live in `exclusions_v002.json`
(successor to `exclusions_v001.json`, which is superseded but never deleted or overwritten —
see §“Re-run nights folded into exclusions_v002” below).

## Manual / late SAS runs (Haci, 2026-09-10)

The runs for **2026-05-11, 05-12, 05-13, 05-14** and **2026-07-06** finished one or more
calendar days after their trading date (`super_agent_select_runs.finished_at`). Haci confirms
these were **manual re-runs during development and bug-fixing**, not the nightly job. Their
candidate `spot_close` values are mixed-date (worst: TER on 07-06, −9.6% versus the actual
close) and nobody could have traded them at publication.

13 runs in total finished on a later calendar day. Eight of them are harmless — they finished
late at night, or over a weekend, *before the next session opened*, so their prices are still
the correct close and a subscriber could still act at the next open (04-01, 04-02, 04-03,
04-06, 04-24, 05-01, 05-15, 07-02). The five above finished **after the next session had
opened**, which is the criterion that matters.

**Rule for studies:** a night is excluded when `finished_at` is later than the next trading
session's open. The resulting list is in `exclusions_v001.json` under `manual_runs`; `eval.py`
reads it rather than hard-coding dates, and reports the excluded count.

## A run on a market holiday (registrar, R1)

`super_agent_select_runs` has a row for **2026-04-03 (Good Friday, NYSE closed)** — no SPY
bar exists for that date, 0 picks were published, and the run finished on 04-04. Excluded under
`non_session_runs`. **Rule for studies:** derive trading nights from the price freeze's SPY
bars, never from `sas_runs` alone, and fail loudly on a run dated on a non-session day.

Night counts after all exclusions: **107 total, 37 in-sample (to 05-29), 70 sealed (from
06-01)**. Earlier desk text said 66 sealed — that subtracted all five manual-run nights, but
only 07-06 falls in the sealed period. 70 is right.

## Re-run nights folded into exclusions_v002 (steward, KT audit, 2026-09-12)

The knowledge-time audit (`research/reports/KT_AUDIT_manifest_v001_rerun_nights.md`) found that
4 of the 8 dates `exclusions_v001.json` had filed under `manual_runs.late_but_clean` —
**2026-04-02, 04-24, 05-15, 07-02** — are not clean: `sas_candidates` on those nights carries a
re-run's creation timestamp and config hash, 19–51 hours after the 16:05 ET decision (run
start/finish reset, run-row creation timestamp unchanged). Because `super_agent_select_runs` is
updated in place — there is no append-only run-history table — the original 16:05 candidate set
for those 4 nights is not recoverable from anything the desk can query. `exclusions_v002.json`
moves these 4 dates into `manual_runs.trading_dates` (now 9 dates total) and reduces
`late_but_clean` to the 4 remaining genuinely benign nights (04-01, 04-03, 04-06, 05-01 — single
continuous scheduled runs, no timestamp reset, no config swap). `non_session_runs`,
`catalyst_layer_regime_change` and `regime_label_point_in_time_from` carry over unchanged.

**Corrected night counts (v002): 103 total, 34 in-sample (to 05-29), 69 sealed (from 06-01)** —
down from v001's 107 / 37 / 70. Three of the four newly-excluded nights are in-sample
(04-02, 04-24, 05-15); one is sealed (07-02).

**Rule for studies:** cite `exclusions_v002.json` going forward; `eval.py` reads the JSON, never
hard-codes dates. Locked PREREGs that cite `exclusions_v001.json` are not edited retroactively —
the exclusions file a locked question cites stands as its population definition (DP-22); any
locked question whose registered population includes these 4 nights is flagged to the Red Team,
not silently re-scoped. As of 2026-09-12 this affects `Q006` (`DATASET_PINNED`, cites v001,
not yet evaluated — flagged, not edited) and `Q005` (`LEDGERED`/`INCONCLUSIVE` — the red team's
own hand-check already showed dropping these 4 nights does not change the verdict, so no further
action). `Q007`/`Q008`/`Q009` (all `PREREG_DRAFT`) cite `exclusions_v002.json`.

Separately, and out of scope for this correction: the KT audit also found `uoa_symbol`,
`gex_symbol` and `projection_bull` rows for roughly 2026-01-07 through 2026-03-20 were written
15–70 hours after their declared 16:05 ET / lag-0 availability (the scheduled nightly job itself
ran late, not a manual re-run). This predates SAS's own history (first `sas_runs` row is
2026-04-01) so it does not affect any currently registered question, but any future study using
those three tables for Jan–Mar 2026 nights must not treat row creation as 16:05-ET-available for
that stretch.

## Publication time is deliberately early on many nights (Haci, 2026-09-10)

28 of 42 in-sample runs finished after 23:00 UTC, but many later runs finish well before.
Haci **pulls the nightly job forward on purpose** so that elite picks can be bought in the
after-hours session, after seeing that elite names moved after the close. Publication time is
therefore a *trading decision*, not noise.

**Rule for studies:** use each night's actual `finished_at` as the earliest actionable moment.
An after-hours entry basis means "the first hourly bar at or after `finished_at`". Do not assume
a fixed 21:05 UTC.

## Earnings dates wrong before 2026-06-01 (Haci fixed; platform commit 69ef05f)

Every in-sample candidate carried a wrong earnings date (always ≥ 38 days out), so the
catalyst layer scored a flat 80 and 26 picks were published within 0–3 days of a report
without the engine knowing. Platform commit `69ef05f` (2026-06-01, "Earnings catalyst: fix
resolver + direction-aware windowed scoring") fixed it.

**Rule for studies:** the catalyst layer is a *different feature* before and after 06-01. Any
catalyst or earnings question must be sealed-period only, or must treat the two regimes
separately. For in-sample earnings work, recompute the earnings distance from an independent
source rather than trusting `days_to_earnings_corrected`.

## `market_regime_daily` is not point-in-time before 2026-06-09 (steward, FREEZE_v001 §7)

Backfilled on 06-02 / 06-08. Regime stratification is knowledge-time-legal only from 06-09.
Describe the earlier tape with SPY's own path instead.

## `uoa_symbol_daily.fwd_return_*` is still degraded (steward, FREEZE_v001 §5)

~95% below baseline since 2026-05-20; `fwd_return_30d_pct` is 0% again for dates ≥ 07-27.
Never use these columns as an outcome; compute forward returns from the price freeze.

## Platform `atr_pct` is corrupted around splits (explorer, EXPLORE_001 §9)

BKNG, CVNA and others show ~10× their true ATR% near split dates because the platform computes
ATR on raw bars. Compute ATR from `p001_daily_split` and convert to the signal-date basis.

## Elite (90+) is thin and shrinking in the frozen data

Published elite picks by month: Apr 8 · May 13 · Jun 12 · Jul 8 · Aug 3 · Sep (to 10th) 2. The
in-sample elites are 9 distinct symbols, mostly memory/semis. Haci (2026-09-10) wants to
understand *why*. Any "elite" claim is a claim about ~45 picks and a handful of names until this
is understood — say so in every report.

## Other

- 16 published picks have no target ladder at all (`public_payload_json` lacks lane targets).
- `industry` is populated for 12% of candidates; sector questions need an external mapping.
- `sas_selection_excursion` has two rows per pick (v1 and v2) through June; v1 retired in July.
  Use `computation_version = 'v2'`.
- Smart-money layer: weight forced to 0 by config
  (`services/super_agent_select_scoring.py:709-710`); the column has been null since April.
