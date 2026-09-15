# Steward — F9 blob inventory: the multi-agent technical reports

**2026-09-14. Counts and metadata only — no price outcome, no touch rate, no return, no correlation.
INTERNAL / NON_QUOTABLE.** Measured by the Data Steward over the production blob store (read/list via
`PROD_SAS_TOKEN`, loaded through `research/lib/desk_env.py`); written to the desk by the coordinator
from the Steward's returned findings, which the agent did not save itself. Scan artefacts stayed in
the session scratch directory; nothing but aggregate counts entered the desk.

## Decision paragraph

The reports exist and can be read, but they are **not a sample the F9 questions can decide on
historically.** There are **697** analyses over **120** days (2026-01-22 .. 2026-09-14), yet
**73.6% come from one internal batch account** (`user_id = 1`, hard-coded in the batch endpoint)
re-running a hand-picked watchlist: **seven symbols are 60% of the corpus, TSLA alone 134 reports.**
The same symbol is re-analysed within 5 trading days on 56.5% of symbol-days, so the number of
independent episodes (DP-51) is in the low dozens, concentrated in under ten names. That cannot reach
rule 6's 80-night floor with a distance-matched control, and a control drawn from an operator-curated
watchlist does not represent what subscribers ask about. **Historical use is exploratory at most.
A decidable F9 test needs reports generated going forward on a fixed, pre-declared universe, with
the trigger recorded** (proposed as EN-019).

The inventory also confirms PI-018 at scale and found two data traps any F9 script must handle: a
timezone switch on 2026-04-06, and a legacy report shape that uses 5m instead of 15m.

## 1. Where the reports are

Source of truth: volatilx `azure_storage.py:132-163` (container naming), `:523-639` (`store_ai_report`),
and `app.py:463-515` (what is written).

| store | contents | used here |
|---|---|---|
| `ai-reports-YYYY-MM-DD` (one per UTC day of the **write**) | F9 history blob `{SYMBOL}_{user_id}_{strategy_scope}_{TIMESTAMPZ}_{job_id}.json`, **append-only** (`overwrite=False`, `:565-570`); a `…_latest.json` pointer, **overwritten** (`:583-588`); legacy reports omit `_{strategy_scope}` | yes — history blobs only |
| same containers | `SAS_*` blobs — a different engine (`store_super_agent_select_report`, `:642-702`) | no (1,945 blobs) |
| `ai-reports-jobs` | job-status blobs `{job_id}.json`; `result` has no `technical_snapshot` | no (495 blobs) |
| `ai-earnings-YYYY` | earnings engine | no |

Every calendar day 2025-11-19 .. 2026-09-14 was scanned (300 days; the container code landed
2025-11-20, commit `a743cb4`). 150 date-containers exist. The first F9 report is 2026-01-22.

**697 history reports** (one per analysis run — the unit), across **120 distinct days**; plus 628
`latest` pointers, which are current state and not additional events. The DB index
`UserReportIndex` (`models.py:364-384`) is latest-only and cannot count history.

## 2. Volume and symbols

Reports per ISO week (history blobs; W07, W08, W24 = 0):

| week | n | week | n | week | n | week | n |
|---|---:|---|---:|---|---:|---|---:|
| 2026-W04 | 32 | 2026-W15 | 27 | 2026-W23 | 30 | 2026-W31 | 36 |
| 2026-W05 | 14 | 2026-W16 | 19 | 2026-W25 | 24 | 2026-W32 | 47 |
| 2026-W06 | 2 | 2026-W17 | 8 | 2026-W26 | 28 | 2026-W33 | 4 |
| 2026-W09 | 1 | 2026-W18 | 34 | 2026-W27 | 9 | 2026-W34 | 6 |
| 2026-W10 | 15 | 2026-W19 | 25 | 2026-W28 | 30 | 2026-W35 | 19 |
| 2026-W11 | 7 | 2026-W20 | 14 | 2026-W29 | 25 | 2026-W36 | 22 |
| 2026-W12 | 21 | 2026-W21 | 30 | 2026-W30 | 31 | 2026-W37 | 16 |
| 2026-W13 | 67 | 2026-W22 | 12 | | | 2026-W38 | 6 |
| 2026-W14 | 36 | | | | | | |

- 5.81 reports per active day; 120 of ~236 trading days in range carry at least one.
- **72 distinct symbols: 67 stocks, 5 crypto** (ADA/USD, BTC/USD, BTC/USDC, BTC/USDT, ETH/USD, classified
  by the payload's own symbol suffix). Crypto is 14 of 697 (2.0%).
- **Reports per symbol:** min 1, p25 3, median 3, p75 9, p90 ≈ 14, **max 134**. Top ten: TSLA 134,
  SNDK 102, WDC 58, MU 47, AMD 24, QCOM 24, INTC 20, RKLB 14, HOOD 13, STX 12. **The top seven are 419 of
  697 = 60%.**

## 3. Who triggers a report — the selection question

Two code paths write these reports, and **neither the blob name nor the payload records which one**:

- `POST /analyze` (`app.py:3286-3287`) — a subscriber's own request, their `user_id`.
- `POST /api/internal/batch-analyze` (`app.py:3696-3700`, internal basic auth, ≤ 25 symbols per call)
  — **hard-codes `user_id = 1`** (`app.py:3966`).

Measured: 37 distinct `user_id`s; **`user_id = 1` is 513 of 697 = 73.6%.** The remaining 184 reports
(36 users) are themselves top-heavy (one user 21, another 15). So three-quarters of the corpus is a
recurring internal run over a small operator-chosen list, not subscriber demand — a stronger
selection problem than the momentum-clustering the F9 preamble anticipated. Provenance is inferable
only through `user_id`.

## 4. Schema

- `strategy_scope` (`day_trading` / `swing_trading` / `longterm_trading`) on 669 of 697 (96%); absent on
  28 — the no-lane fallback (`app.py:505-515`), scattered Feb–Aug, a coexisting path, not a version break.
- `status = done` on 697 of 697 and `technical_snapshot` present on all. This is survivorship over what
  was written; it does not show the error path (`app.py:606-616`) never fires.
- **Timeframes:** the 669 lane reports carry 15m/30m/1h/4h/1d/1wk/1mo; **the 28 legacy reports carry
  `5m` instead of `15m`** (28 of 28; 0 of 669 lane reports have 5m).
- Coverage is uneven even on lane reports: 15m/30m on 673, 1h/4h on 694, but **1d/1wk/1mo on only
  597–654 of 697** — 6–14% of reports lack the long-horizon timeframes that H-086's swing and long
  buckets need.

## 5. Stops and targets, by timeframe and call

`stop_loss` is present on effectively 100% of BUY and SELL decisions at every timeframe. `take_profit`
and `risk_reward_ratio` are missing together. Share of decisions with a `take_profit`:

| tf | BUY | SELL | HOLD |
|---|---:|---:|---:|
| 15m | 87.5% | 73.1% | 0.0% (n = 3) |
| 30m | 82.4% | 74.1% | 100.0% (n = 3) |
| 1h | 84.5% | 84.3% | 87.5% |
| 4h | 84.0% | 92.1% | 100.0% |
| 1d | 79.0% | 89.8% | 100.0% |
| 1wk | 78.0% | 96.2% | 98.7% |
| 1mo | 80.5% | 100.0% | 92.0% |

**"SELL calls carry no target" is refuted as a general rule.** It held for the SNDK sample's 30m and 1h
calls only. From 1h upward, SELL target availability matches or exceeds BUY's. H-086 measures target
availability per timeframe rather than assuming it.

## 6. Knowledge time

- **`entry_price == current_price` on 100% of 4,610 decisions checked.** Entry is always spot.
- **Every timeframe's `price_timestamp` equals the report's top-level `timestamp`** (median and max
  difference 0 minutes). It is one analysis clock read, not seven per-bar times.
- **The timestamp's zone changed on 2026-04-06, with no zone marker in either period.** Against the
  UTC `stored_at`:
  - 2026-01-22 .. 2026-04-05, **201 reports: difference ≈ 0 minutes → `timestamp` is UTC.**
  - from 2026-04-07, **494 reports: a clean 240–241 minutes → `timestamp` is US Eastern (EDT).**
  - 2026-04-06 is a mixed day carrying both.
  No `day_trading_agent.py` commit in that window explains it. **Any F9 `eval.py` must normalise the zone
  by report date**, and 2026-04-06 needs a per-report rule. (This corrects the F9 preamble, which assumed
  Eastern throughout from one sample.)
- **Rewrites:** `last_modified − timestamp` ranges 0.0001–0.174 days (0 to ~4.2 h) for all 697. **None
  was rewritten more than a day after its analysis.** History blobs are write-once near analysis time.

## 7. Re-analysis of the same symbol (DP-51)

248 distinct symbol-days. Another report on the same symbol within **1 trading day: 31.5%; within 5:
56.5%; within 10: 63.7%.** With §2's concentration, independent episodes number in the low dozens.

## 8. PI-018 at scale

- **Call against its own timeframe's bias: 495 of 3,933 (12.6%)** directional decisions with a known
  `overall_bias` — 378 BUY on a bearish bias, 117 SELL on a bullish bias.
- **"Near Fibonacci" in the reasoning of 2,992 of 3,933 (76.1%)** BUY/SELL decisions — the proximity rule
  is the main route to a directional call, not a corner case.
- **Consensus tally ≠ number of timeframes: 349 of 697 reports (50.1%).**

## 9. Retention

Hybrid store, confirmed in code and data: history append-only (697 unique names, no collision
suffixes), `latest` pointers overwritten. Earliest report 2026-01-22; no gap pattern suggesting deletion.
An Azure lifecycle policy is a management-plane setting the desk's data-plane token cannot see, so
future expiry can be neither confirmed nor ruled out.

## Incidental findings

- **`research/lib/desk_env.py` kept inline comments in values** (`KEY=value  # note` loaded the note),
  unlike the bash loader in `scripts/research_routines.sh:13`. Fixed the same day; the prefixes that
  tripped the Steward now load cleanly.
- `PROD_SAS_TOKEN` is an account SAS scoped to container + object with read + list. Listing containers at
  service level is refused (`AuthorizationResourceTypeMismatch`), which is expected; listing and reading
  named containers works.
