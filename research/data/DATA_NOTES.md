# Data notes — what the desk knows about the data that the tables don't say

Read this before writing a PREREG or an eval.py. Each note gives the fact, who established it,
and what a study must do about it. Machine-readable exclusions live in `exclusions_v003.json`
(successor to `exclusions_v002.json` and `exclusions_v001.json`, both superseded but never
deleted or overwritten — see §“Re-run nights folded into exclusions_v002” and
§“2026-06-26 uncorroborated publication rows folded into exclusions_v003” below).

## One database: `$RESEARCH_DB_URL` **is** production (Haci, 2026-09-13)

There is no separate research database. `$RESEARCH_DB_URL` points at the same Postgres instance
the platform writes to every night; the desk is separated from it by a **role**
(`sas_research_ro`, read-only — `UPDATE` and `CREATE` are refused at grant level, verified in
`docs/SETUP_STATUS.md`), not by a copy. Standing consequences are DP-50; the ones that bite an
`eval.py` or a PREREG:

- **A live query is not reproducible.** The rows behind it can be rewritten by a platform repair
  between one run and the next. Anything that has to be stable — a before-snapshot, an exposure
  count, a population funnel, any number a PREREG cites — comes from a pinned manifest, never from
  a live query. Rule 4 is the thing protecting locked questions from a repair, so it is
  load-bearing, not housekeeping.
- **A successor freeze can disagree with its predecessor about the past.** `manifest_v002` re-runs
  `manifest_v001`'s SQL against tables a repair may have changed in the meantime. That is not a
  bug in either freeze. A question whose window spans a repair date treats the repaired column as
  two different features and splits there, exactly as DP-06 splits the catalyst layer at
  2026-06-01.
- **The repair log below is the record of when that happened.** Check it before trusting any
  column across a date boundary.

### Repair log — platform changes that rewrote historical rows

Every fix that changes values already written gets a row here on the day it ships, with the ship
SHA. A repair that is only forward-looking (a new column, a guard on future writes) does not.

| shipped | SHA | table.column | date range rewritten | raised by |
|---|---|---|---|---|
| _pending_ | `2d5776c` (on branch `fix/pi-001-backfill-window-floor`, **not merged to main as of 2026-09-13**) | `uoa_symbol_daily.fwd_return_5/7/14/30d_pct` | nothing yet. The code fix only widens which NULLs the nightly revisits; it overwrites no value. If Haci runs the PI-001 catch-up sweep, that fills NULLs over 2026-04-15..2026-07-29 and gets its own row here. | PI-001 |

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

## 2026-06-26 uncorroborated publication rows folded into exclusions_v003 (steward, Q009 R3/R4, 2026-09-13)

Routed by the Q009 decision-maker as R3/R4 (`research/questions/Q009_stop_whipsaw/DECISIONS.md`,
items 20/22 and "Routed requests"). Ruling 1 of R3 found that the frozen `sas_candidates` table
for trading_date **2026-06-26** carries **11** qualified rows with a non-null `selected_rank`,
while that night's own contemporaneous run audit (`sas_runs.stats_json`) records
`qualified_count: 8`, all bullish. The 3 extra bearish rows (**DPZ, COIN, AAPL**) are not
corroborated by the run's own audit trail at all, yet each carries a fully-formed
`public_payload_json` with complete `lane_plans` across all three lanes, including the
swing-lane stop and L3 target. All 52 rows for the night share one `created_at`
(2026-06-26 21:17:31.403724 UTC) -- a single-batch write, not a re-run -- so this is a
**distinct failure mode** from the re-run signature `exclusions_v002.json` already excludes:
partial row mutation after a clean single-batch write, rather than a timestamp-reset re-run.
Checked against all 113 nights in the frozen history, **2026-06-26 is the only night** where the
frozen qualified-row count disagrees with the run's own `stats_json.qualified_count`. Ruling 2 of
R3 (the E9a correction batch, the wrong-side-target guard, and the cross-lane monotonic re-sort)
came back **negative** -- no payload rewrite anywhere in the 795-row correction ledger.

**`exclusions_v003.json`** (successor to `exclusions_v002.json`, declared by the Data Steward
2026-09-13) carries everything from v002 unchanged (`manual_runs`, `non_session_runs`,
`catalyst_layer_regime_change`, `regime_label_point_in_time_from`,
`sas_candidates_availability_note_correction`) and adds one new block,
`uncorroborated_publication_runs`, excluding trading_date **2026-06-26** in whole -- all 11
qualified rows, not only the 3 uncorroborated ones. Whole-night scope is the conservative,
KT-audit-consistent choice (the decision-maker's, per DECISIONS.md item 20): the 8 corroborated
bullish rows came through the same write path and have not themselves been shown clean of it,
and the desk's exclusion lists are night-level by precedent. The mutation cannot be dated more
precisely than "after the 2026-06-26 16:05 ET run, before the 2026-09-10 freeze" --
`super_agent_select_runs` is updated in place with no append-only run-history table, so the
night's true 16:05 published set is not recoverable, only excluded.

**Re-derived night counts (v003): 102 total, 34 in-sample (to 05-29), 68 sealed (from 06-01)** --
down from v002's 103 / 34 / 69. The one newly-excluded night (2026-06-26) is sealed; no in-sample
night count changes.

**Q009 population under v003** (the question this exclusion exists for, and the reason it cannot
lock without this file): re-deriving the full R1 funnel with 2026-06-26 also excluded gives
**303 eligible picks on 47 contributing nights** (down from 313 picks / 48 nights under v002),
buckets TIGHT 282 / MID 21 / WIDE 0. See
`research/reports/STEWARD_Q009_exposure.md` addendum for the full re-derived funnel.

**Rule for studies:** cite `exclusions_v003.json` going forward; `eval.py` reads
`manual_runs.trading_dates` ∪ `non_session_runs.trading_dates` ∪
`uncorroborated_publication_runs.trading_dates`, never hard-coded dates. Locked PREREGs that cite
`exclusions_v001.json` or `exclusions_v002.json` are not edited retroactively -- the exclusions
file a locked question cites stands as its population definition (DP-22). As of 2026-09-13 this
affects `Q009` (PREREG_DRAFT -- cites this file; cannot lock without it); `Q008` (PREREG_DRAFT,
cites v002 -- switches to this file at its decision pass under DP-22); `Q007` (PREREG_LOCKED
2026-09-13, commit `b211292`, cites v002 -- 2026-06-26 falls inside its ≥ 2026-06-01 window; NOT
edited, flagged to the Red Team for Q007's review); `Q006` (locked, cites v001 -- same treatment,
already flagged for the v002 re-run nights and now also for 2026-06-26); `Q005`
(LEDGERED/INCONCLUSIVE -- one night, no action).

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

## _enforce_ladder_monotonic did not exist for the first five weeks of the sealed-but-live window (steward, Q018 R1, 2026-09-13)

Platform commit `5fa3db4` ("W3: publication-time cross-lane ladder monotonicity (H4 family)",
2026-07-06) is what ships `_enforce_ladder_monotonic` (`services/super_agent_select_service.py:195-215`).
Before that commit there was no cross-lane re-sort at all -- a payload was published exactly as
the lane-plan writer produced it, monotonic or not. Measured directly from `manifest_v001` on the
495 six-level-eligible 80-90 published picks 2026-06-01..2026-09-09 (`STEWARD_Q018_exposure.md`
Section 2): flattened-ladder non-monotonicity is **25.71% (36 of 140) before 2026-07-06** and
**0.00% (0 of 355) on/after 2026-07-06**. The desk's standing "historically ~28%" figure for this
share is consistent with the pre-fix regime only; a blended figure across the whole window
(7.27%) understates the pre-fix rate and overstates the post-fix rate. The same commit range also
introduces `SuperAgentSelectConfig.publication_floor = 80.0` (`services/super_agent_select_models.py:86-91`,
commit `1765a6f`, 2026-07-07) and a multi-day bear/dark-lane build-out
(`services/super_agent_select_service.py` / `super_agent_select_scoring.py`, 2026-06-28..2026-07-06)
touching the same wrong-side-target and ladder-integrity machinery the six-level eligibility test
leans on.

**Rule for studies:** any study whose population spans 2026-07-06 and that reads ladder
monotonicity, "unresolvable ladder" status, or a wrong-side-of-close exclusion as a single-regime
fact must split at 2026-07-06 (DP-06 pattern) or state explicitly that it is reporting a blend of
two mechanisms. See `research/reports/STEWARD_Q018_exposure.md` Section 2 / Section 5 for the full
commit list and the empirical split.

## `public_payload_json.lane_plans` price levels are on the wrong split scale for some symbols (steward, Q018 R1, 2026-09-13)

Distinct from the already-documented `atr_pct` corruption (PI-003, above): for a subset of
symbols, the lane plan's own printed price levels (`entry`, `stop`, `targets`, `invalidation`
inside `public_payload_json.lane_plans`) are on a different price scale than `C_t` computed from
`prices_daily_split` for the identical symbol/date -- consistent with the lane-plan writer's price
reference having been built from a raw (non-split-adjusted) price while `prices_daily_split`
correctly retro-adjusts the whole history. Measured on the 495-pick population
`STEWARD_Q018_exposure.md` Section 2 uses: **APH, 14 of 14 eligible picks in-window (100%),
2026-06-05..2026-08-12, ratio ~2.00-2.05x** (systematic, not episodic -- every APH pick this
window carries the mismatch); **KLAC, 1 night (2026-06-05), ~10.18x**; **CRWD, 1 night
(2026-06-29), ~4.07x**; **MNST, 1 night (2026-07-13), ~2.02x**. The six-level eligibility test's
wrong-side-of-`C_t` check does not catch this: a raw-scale bullish target is still nominally
"above" a much smaller split-adjusted close, so the row passes eligibility while the printed
distance is not real.

**Rule for studies:** any ATR-distance, price-level or percent-move computation that mixes a
payload's own printed price level with `C_t`/ATR from `prices_daily_split` should screen for
`target / C_t` (or `entry / C_t`) outside a sane band (e.g. [0.5, 1.5] for a near target) before
trusting the ratio, and should not assume this is limited to APH/KLAC/CRWD/MNST -- these four were
found only because they fell inside one question's 495-pick sample; a full sweep across all
published symbols has not been done. Flagged to the Red Team as a candidate PI filing (distinct
from PI-003). See `research/reports/STEWARD_Q018_exposure.md` Section 2 for the measured counts.

## Enrichment flags: the runtime config overrides the code default (Steward, Q036 R1, 2026-09-14)

Several PREREGs cite `services/super_agent_select_models.py:109-111` and state that
`enable_fundamental_enrichment` and `enable_smart_money_enrichment` default `False`. The **code
default is correctly cited**; it is **not** the value the deployment runs. Measured on
`sas_runs.config_json` (`research/data/manifest_v001.json`) over all 67 non-excluded nights of
2026-06-01..2026-09-10 (`research/reports/STEWARD_Q036_exposure.md` §(f)), and independently on 68
nights by `Q029 §2` (67 of 68): `enable_catalyst_enrichment = True`, **`enable_fundamental_enrichment
= True`**, `enable_smart_money_enrichment = False` (its coded default), constant across the window
with no in-window ship. **Rule for studies: the runtime `config_json` tuple, pinned per night in the
freeze, is the value of record for every enrichment flag, weight and multiplier -- never the ORM
default.** A PREREG that reasons from the ORM default reasons about a configuration the platform does
not run; the consequence measured in Q036 is that two of three enrichment layers populate
`completeness_score`'s numerator on every row, and `completeness_score` never falls below 65.3686 in
4,195 scored rows, which makes `_confidence_label`'s `medium` and `low` tiers unreachable on the
published slate (`PI-016`; Q036 DEFERRED for that reason). `Q028 §9/§10` (locked) carries the
code-default reading and is flagged to the Red Team rather than edited.

## Other

- 16 published picks have no target ladder at all (`public_payload_json` lacks lane targets).
- `industry` is populated for 12% of candidates; sector questions need an external mapping.
- `sas_selection_excursion` has two rows per pick (v1 and v2) through June; v1 retired in July.
  Use `computation_version = 'v2'`.
- Smart-money layer: weight forced to 0 by config
  (`services/super_agent_select_scoring.py:709-710`); the column has been null since April.

## Alpaca access from the desk session, and one config defect (2026-09-14)

**The credentials were never missing.** `.env.research` holds `ALPACA_API_KEY` and
`ALPACA_SECRET_KEY`, and `scripts/research_routines.sh:13` loads it for every headless `daily` /
`weekly` / `desk` run. What an interactive session lacked was the *load* — the agent cannot source
the file itself (`Read(.env.*)` is denied, and the deny rule covers sourcing it in a shell). Q030,
Q032 and Q033-P2 were each deferred on "no Alpaca credentials in the desk's session", which was
true of the session that measured it and false of the environment the Steward runs in.

`research/lib/desk_env.py` closes the gap: it loads the file into `os.environ` for desk tools,
never overwrites a variable already set, and **returns variable names, never values** — presence is
all any caller can learn. `present()` is the direct test the Q024 R1(d) precedent asks for.

**Defect: `ALPACA_DATA_FEED` is malformed.** The value is four alphabetic characters beginning
`sip` — a typo of `sip` — and Alpaca answers it with **HTTP 400** on every request. It matters
because `research/lib/freeze_prices.py:104` defaults `--feed` to that variable, so the next price
freeze run without an explicit `--feed` fails outright. `manifest_prices_v001` records `feed=sip`,
so the variable was correct when that freeze ran or the flag was passed by hand. Every probe on
2026-09-14 passed `--feed sip` explicitly. **The fix is Haci's**, a one-character edit in a file
the desk may not read; until it lands, every price fetch must pass `--feed sip` on the command line.

**Hash the committed bytes, not the working tree.** `data/sp500_sectors.json` pins at sha256
`c4d12610…0201`, the content of platform commit `4171b1a`. A Windows checkout with
`core.autocrlf=true` rewrites LF to CRLF, so the on-disk file hashes to something else
(`fc13551c…`) while being the same content. Verify the pin with
`git show 4171b1a:data/sp500_sectors.json | sha256sum`, never by hashing the working-tree file.
The mapping carries **2,405** entries, as the Q030 / Q024 / Q022 pins record.

**Measured coverage over that universe (2026-09-14, counts only, no freeze):** 2,346 of 2,405
symbols returned ≥ 60 daily bars over 2026-06-01..2026-09-11 on `feed=sip`, `adjustment=split` —
**97.55%**, against Q030's ≥ 90% gate. 59 symbols short or absent, named in
`research/reports/STEWARD_Q030_universe_coverage_probe.md`. Symbols without bars are counted and
named, never back-filled or imputed.

## `manifest_prices_universe_v001` — the base-universe price freeze (2026-09-14)

Built to unblock Q030 and Q032 after the Alpaca deferrals were lifted. **One fetch serves both**,
which is what Q030 §5.3's "one selection freeze and one price fetch can serve both" anticipated.

- **Scope.** Daily bars only (`1Day`), `adjustment=split` **and** `adjustment=raw`, `feed=sip`,
  2025-01-02 .. 2026-09-10. **No hourly bars** — Q030 R2 does not require them.
- **Symbols.** 2,405 base (the pinned blob's `mapping`) ∪ 431 candidate ∪ 5 benchmark
  = **2,412 distinct requested**; **2,404 of 2,405 base symbols returned bars**. The one absent
  symbol is **TSEOF**, named in the manifest's `base_universe.absent` and **never imputed**.
- **Rows.** 1,008,092 per adjustment, 2,411 symbols present.
- **The blob is hashed from committed bytes**, `git show 4171b1a:data/sp500_sectors.json`, verified
  at 2,405 mapping entries and sha256 `c4d12610…0201`. A Windows checkout rewrites LF to CRLF, so
  the working-tree copy hashes differently and **must never be hashed in its place**.
- **The start date is 2025-01-02 deliberately**: Q032 §2.2's expanding-window volatility tercile
  needs ≥ 250 prior SPY sessions, and 2025-01-02 puts the first calibrated session at **2026-02-02**,
  well before the registered window opens on 2026-09-15.
- **Tool.** `research/lib/freeze_prices_universe.py` — a sibling of `freeze_prices.py` that takes an
  explicit symbol list instead of a base manifest, which Q030 R2 authorizes by name. It reuses
  `freeze_prices.fetch_all`, so the sanctioned fetch path is unchanged.
- **`--feed sip` is passed explicitly**, because `ALPACA_DATA_FEED` still holds the malformed value
  recorded above and `freeze_prices.py:104` defaults to it.

**This freeze covers history only.** Q030 R2's forward study cut — the registered window through
2027-02-24, delivered before Monday 2027-03-08 — is still owed and is a separate, later artefact.

### An operational trap worth recording: two concurrent freeze runs

The first run was launched with its output piped to `tail`, which buffered everything and made it
look dead; a second run was started against the same version. Both would have written the same
parquet paths, and the second was killed only because the manifest appeared on disk while its log
still showed it mid-fetch. **`freeze_prices_universe.py` checks for an existing manifest at start-up
only**, so that check cannot catch a concurrent run — it is not a lock. Until it takes one, never
start a second freeze at the same `--version`, and pipe freeze output to a file rather than through
`tail`. The delivered files were verified by SHA-256 against the manifest after the kill.

## External source: Financial Modeling Prep (Haci, 2026-09-15)

Haci granted the desk his FMP subscription key on 2026-09-15 (`FMP_API_KEY` in `.env.research`, loaded only
through `research/lib/desk_env.py`, never printed). Haci added `FMP_API_KEY` to CLAUDE.md rule 1 the same
day (his edit; CLAUDE.md is a guarded file the desk does not write), so it is a named desk credential. Docs: https://site.financialmodelingprep.com/developer/docs.
It is **read-only reference and fundamental data**, and it is also what the platform's own enrichment path
already calls (`ai_agents/fmp_client.py`), so it changes nothing about rule 1's read-only stance.

What it is for, and the rules that travel with it:

- **Rule 4 still binds.** Any FMP field a PREREG cites is frozen first into `research/data/` with a manifest
  (`manifest_fmp_vNNN.json`: endpoint, parameters, fetch time, row hashes). No study number comes from a live
  call.
- **Rule 14 is the hard part.** FMP rows are *records*, not point-in-time observations: an estimate revision,
  a news item or an insider filing must carry a publish / acceptance timestamp that the freeze keeps, and a
  feature is usable only when that timestamp ≤ 16:05 ET on the pick night. Endpoints without a reliable
  publish time (most "profile" and "ratios" snapshots) are **descriptive only**. The Steward records the
  availability per endpoint in `freeze_config.availability` before any question uses it.
- **Candidate uses, in order:** (1) H-022's blocker — Form 4 insider-transaction *history* with acceptance
  timestamps (`insider-trading` search endpoints); the Steward checks coverage and as-of fields before the
  registrar may lift the deferral. (2) Analyst estimate and price-target revision history, for the smart-money
  and catalyst layers. (3) Stock news with publish times, for a news-catalyst arm. (4) Earnings-call transcript
  metadata for the earnings engine. Anything else is out of scope until a hypothesis names it.
- **Not for:** live checks during a study, price data (Alpaca remains the price source), or anything a
  subscriber-facing claim would cite before it is frozen and prospective.

## `conviction_monitor_daily` has no rows for 2026-07-06 (steward, Q038 R1, 2026-09-15)

Answering Q038 R1 (`research/questions/Q038_monitor_tier_calibration/DECISIONS.md`, "Routed
requests -- data-steward", and `research/reports/STEWARD_Q038_exposure.md` item (3)). Counts
only, no live query: the source is the frozen `conviction_monitor` parquet named by
`manifest_v001.json`.

**What was measured.** Row count of `conviction_monitor_daily` by `trading_date`, every
in-window session 2026-06-01..2026-08-19 (the matured cohort). Every session but one carries
**31 to 56 rows**. **2026-07-06 carries exactly 0.** This is a complete one-day outage of the
monitor job, system-wide -- not a partial degradation and not holiday shortening: a genuine
market holiday (2026-06-19 Juneteenth, 2026-07-03 Independence Day observed, 2026-09-07 Labor
Day) still receives roughly 40-44 off-calendar rows dated on the holiday from the monitor's
Monday-through-Friday cron running regardless of the market being open; 2026-07-06 was a normal
NYSE trading session and received zero rows of any kind.

**Downstream effect measured.** Pick nights 2026-06-29, 2026-06-30 and 2026-07-01 each have
session t+3 or t+4 landing on 2026-07-06, dropping their in-scope monitor row count to 3 --
one short of the 4-row eligibility floor Q038's (and Q019's) funnel requires. All 24 published
picks across these three nights fail the eligibility rule on this account alone. Filed as a new,
add-only block in `research/data/exclusions_v004.json` (`monitor_coverage_outage`,
`trading_dates`: 2026-06-29, 2026-06-30, 2026-07-01), successor to `exclusions_v003.json` per
DP-22 -- v003 carries over unchanged; nothing in it is edited.

**Q019 must treat the same three nights the same way.** `research/questions/Q019_conviction_monitor_exit`
reads the identical `conviction_monitor_daily` table over the same window. Its `eval.py` must
read `exclusions_v004.json`'s `monitor_coverage_outage` block (never hard-code the three dates)
and exclude the same 2026-06-29 / 2026-06-30 / 2026-07-01 pick nights from any monitor-row-dependent
funnel step, in addition to -- not instead of -- `exclusions_v003.json`'s existing
`manual_runs` treatment of 2026-07-06 itself as an excluded SAS pick night (an unrelated,
independent reason: that block excludes 2026-07-06 as a candidate-publication re-run night, not
because of the monitor outage on that date).

**Not caught by the platform's coverage watchdog.** A complete one-day, system-wide zero-row
outage on a normal trading session should be exactly the kind of gap a coverage watchdog exists
to catch, and it was not flagged. No existing entry in `research/PLATFORM_ISSUES.md` covers this
defect as of 2026-09-15 (the register's highest filed id is PI-021, already assigned to an
unrelated defect -- platform pytest fixtures deleting all users -- so this is **not** the same
issue and should not be cited under that id). The coordinator is filing this as a new
`PLATFORM_ISSUES.md` entry (expected next free id **PI-022**); reference the entry the
coordinator actually files, not PI-021, when this note is next revised.

## EN-020 Phase A (PI-023) ship log (steward, 2026-09-15)

**EN-020 Phase A (PI-023) shipped `c5740cc` (merged `eb2de2c`, redeployed `2036454`), first covered
session pending — expected 2026-09-16, to be filled at the next verify.** From that session
`uoa_contract_daily.buy_premium / sell_premium / unknown_premium` are summed from
`uoa_contract_intraday` buckets labelled against the quote bracketing each print; uncovered premium
is `unknown`, with no closing-quote fallback. `uoa_symbol_daily.dir_ratio` is NULL when
`aggressor_qat_share < 0.50`, and `bull_dir`/`bear_dir` fall to 0.50, which moves
`score_day/swing/long` on those symbols; the SAS legacy flow vote abstains there. Feed in use:
`opra` (as recorded on the tick rows). Per-session `aggressor_qat_share`: pending — no trading
session has run with the sampler deployed as of 2026-09-15 (ship date); to be filled once a session
completes. **No historical row was rewritten.** Under DP-50(a) the aggressor columns are two
different features either side of this date: **Q014, Q019, Q029 and Q030 split here** (split date
= first covered session, TBD, expected 2026-09-16).

Ship date: **2026-09-15**. Repository checks (§4.1 a-f of the brief) and the schema-landed check
passed the same day; W1-W3 (sampler ran, merge reconciles, early-vs-late placebo) are pending on
the schedule in `research/reports/VERIFY_EN-020.md`.

## UOA option trades paginated from D0 (PI-020, shipped 3f1d3e6, no flag — DP-59)

From trading date D0, `uoa_contract_daily.trade_count / volume_traded / premium_total / premium_max /
first_trade_ts / last_trade_ts / buy_premium / sell_premium / unknown_premium / top_trades_json`,
`uoa_symbol_daily.call_premium_total / put_premium_total / total_premium / call_buy_premium / put_buy_premium /
net_directional_premium / dir_ratio / prem_* / unusual_* / quality_* / conc_* / score_* / bias_* / label_* /
why_json`, `uoa_bulletins.lists_json / markdown`, and every SAS flow input and output downstream
(`flow_strength_score`, flow polarity and vote, `overall_score`, `selected_rank`) are built from every print, not
from one 1,000-print page per 50 contracts. Nights before D0 stay capped and were not rewritten. A question
spanning D0 treats these as two different features (DP-50(a)): Q014, Q019, Q029, Q030 and every prospective
slate reader split there. Nights whose `stats_json` has no `trades_fetch` block are pre-fix.

**D0 = 2026-09-15**, confirmed: the nightly of that date is the first whose `uoa_runs.stats_json` carries a
`trades_fetch` block (started 21:03:43 UTC, finished 21:13:21 UTC, `status = success`); every nightly back to
2026-09-01 has none. Ship SHA `3f1d3e6` ("PI-020: get_option_trades paginates in place, calls and puts apart
(no flag)"), merged into `main` as PR #32 (`e513d44`), 2026-09-15.

**Verified 2026-09-15 — OVERALL PASS, with W6 confirming ~2026-09-29** (`research/reports/VERIFY_PI-020.md`).
History is unchanged to the row (SNDK 2026-09-08 still 60 contracts / 2,000 prints / 0 puts; capped and
zero-put counts for 2026-01, -04, -07, -08 all reproduce the brief exactly), so **no historical row was
rewritten** and the DP-50(a) split at 2026-09-15 is clean. On D0 all fifteen always-capped names carry put
premium and none sits within 0.001 of `dir_ratio` 1.00; SNDK moved from `dir_ratio` 1.00 on 2,000 call-only
prints to -0.0575 on 12,081 prints with 7,222 puts and $75.4M of put premium. Run telemetry: `page_limit`
10000, 498 symbols, 1,068 requests, 0 ceiling hits, 0 failed requests, 104.4 s of trade fetch. The share of
>= 1,000-print symbol-days with zero put premium is 0/78 on D0, against 3.6-19.8% in the preceding six
sessions. Nightly runtime cost of this fix is about +40 s and SAS publication did not slip.

**A caveat for anyone re-running the brief's checks:** `uoa_contract_daily.snapshot_volume` is NULL on every
row, before and after D0. The brief's W3 query keys on `snapshot_volume > 0`, so it returns all zeros and
reads like a pass while measuring nothing. The substitute used instead — zero-print contracts by side on
symbol-days with >= 1,000 prints — is decisive: the put-side zero-print share falls 74.0% -> 17.5% while the
call side falls 55.2% -> 14.3%, i.e. a 19-point side gap closing to 3 points.
