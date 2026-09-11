# Data notes — what the desk knows about the data that the tables don't say

Read this before writing a PREREG or an eval.py. Each note gives the fact, who established it,
and what a study must do about it. Machine-readable exclusions live in `exclusions_v001.json`.

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
