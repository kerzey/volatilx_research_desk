# VERIFY PI-020 — UOA option-trades pagination

**Verified:** 2026-09-15, `verify PI-020 3f1d3e6`. Repo half by the Data Steward; database half run
directly by the coordinator after the Steward's session lost the database credential (see §"Two passes").
**Brief:** `research/briefs/PI-020_uoa_trades_pagination.md`
**Ship SHA:** `3f1d3e6` ("PI-020: get_option_trades paginates in place, calls and puts apart (no flag)"),
authored 2026-09-15 11:57 -0500, merged into `main` as PR #32 (`e513d44`).
**D0 = 2026-09-15** — the first nightly whose `uoa_runs.stats_json` carries a `trades_fetch` block
(started 21:03:43 UTC, finished 21:13:21 UTC, `status = success`). Every prior nightly back to 2026-09-01
has no such block, so D0 is unambiguous.

**Note on what runs in production tonight.** `3f1d3e6` sits between `39fc8a5` (an earlier flag-based
attempt, PR #31, which `3f1d3e6` supersedes and de-flags) and later commits that also touch
`uoa_screener.py` / `options_client.py`: `d112d37` (Omega tables), `c5740cc` (EN-020 Phase A),
redeploy `2036454`, HEAD `9b8895c`. What the nightly actually ran tonight is HEAD, which contains
the PI-020 change. All repo checks below were run against the current checkout (HEAD = `9b8895c`,
which is `3f1d3e6`'s content unmodified for the files this brief touches).

## Status table

| Check | Result |
|---|---|
| repo (c) `git show --stat 3f1d3e6` lists exactly the 4 paths | PASS |
| repo (c) `git diff --quiet 3f1d3e6~1 3f1d3e6 -- <other paths>` | PASS — printed UNCHANGED |
| `git show 3f1d3e6 -- services/uoa_screener.py` shows only the PI-020 shape | PASS |
| repo (a) `python tests/test_uoa_trades_pagination.py` (no DB env var set anywhere in shell) | PASS — `PI-020: 9/9 checks passed` |
| repo (b) `trades_limit`, `_MAX_TRADE_PAGES` print | PASS — printed `10000 20` |
| D0 determination (`uoa_runs`, presence of `trades_fetch` block) | **PASS — D0 = 2026-09-15** |
| W5 (history unchanged: re-run section-1 R1/R2) | **PASS — identical to the brief, to the row** |
| W1 (15 always-capped names, first nightly on the fix) | **PASS** — all 15 have put premium; 2 names below the `trades > 2000` proxy for a benign reason (below) |
| W2 (`uoa_runs.stats_json.trades_fetch` telemetry) | **PASS** — `page_limit 10000`, 0 ceiling hits, 0 failed requests |
| W3 (dropped-side signature) | **PASS on the substitute; the literal query is void** — `snapshot_volume` is NULL on every row |
| W6 (zero-put share <= 2% over 10 sessions from D0) | **ON TRACK — 0/78 (0.0%) on D0**; decidable ~2026-09-29 |
| W4 (runtime / publication-time shift, reported not judged) | REPORTED — PI-020's own marginal cost ~ +40 s; no SAS publication delay |

## Two passes

The Steward's session could not reach the database: the credential was not in its shell and the
local env file is deny-listed for reading there. That half was re-run directly, in-session, through
the desk's documented loader (`research/data/DATA_NOTES.md:284`), read-only on `$RESEARCH_DB_URL`
under `sas_research_ro`. The repo half below is the Steward's, unchanged. Scripts:
`pi020_a.py` / `pi020_b.py` / `pi020_c.py` in the session scratchpad; every statement a read, no writes.

## Repo half — detail

**(c) `git show --stat 3f1d3e6`:**
```
ai_agents/options_client.py         |  84 ++++---------
docs/UOA_SCREENER_MVP.md            |  19 ++-
services/uoa_screener.py            | 216 ++++----------------------------
tests/test_uoa_trades_pagination.py | 239 +++++++++++++++++-------------------
```
Exactly the four paths named in the brief. `3f1d3e6~1` is `39fc8a5` (the flagged predecessor also
part of this fix's history), so the diff against its immediate parent is dominated by removing the
flag/shadow-mode machinery (`uoa_trades_fetch_settings`, `summarize_symbol_flow`,
`get_option_trades_paged`, `record_trades_shadow`) rather than the brief's literal "removals only
at line 806 and lines 1504-1509" (that description matches the diff against the pre-PI-020 baseline
commit `c311e81`, checked separately below). Substance is unaffected either way: at `3f1d3e6`, and
still at HEAD, `get_option_trades` is a single method, no flag, no second code path, calls and puts
batched apart, bounded by `_MAX_TRADE_PAGES` (env `ALPACA_OPTION_TRADE_PAGES`, default 20).

`git diff --quiet 3f1d3e6~1 3f1d3e6 -- services/super_agent_select_scoring.py
services/super_agent_select_service.py services/symbol_context_builder.py
services/candidate_universe_builder.py services/uoa_scheduler.py services/gex.py scripts/ routers/
models.py db.py conftest.py core/ fmp_mcp_server/ ai_agents/omega_agent.py
ai_agents/option_flow_monitor.py` exits 0 -> **UNCHANGED** (printed; exit code confirmed).

Cross-check against the pre-PI-020 baseline (`c311e81`, before either PI-020 commit) confirms the
brief's literal shape: the `services/uoa_screener.py` diff from `c311e81` to `3f1d3e6` is additions
plus one value change (`trades_limit: int = 1000` -> `10000`), and the call site gains a
`record_trades_fetch(...)` call after the unchanged `get_option_trades(...)` call — no other lines
removed. The `ai_agents/options_client.py` diff from `c311e81` to `3f1d3e6` replaces the whole
`get_option_trades` body per the brief's section 3.2, matching its snippet essentially verbatim
(side-split groups, page cap, truncated_sides, fetch dict shape).

**(a) Test, at HEAD (no DB credential env var set anywhere in that shell — confirmed by an
env-var scan returning nothing named for the database before running):**
```
python tests/test_uoa_trades_pagination.py
...
PI-020: 9/9 checks passed
```
(Two Alpaca-credentials-missing fallback-catalog warnings printed first; harmless and unrelated to
the test — the module import chain touches `indicator_fetcher`/`symbol_map`, as the brief
anticipates in its section 4 preamble.)

**(b) Page size, at HEAD:** printed `10000 20`. Matches exactly.

## W5 — history did not move. PASS, and this is the check that had to pass first.

**R1, SNDK 2026-09-08** — `contracts | trades | call_trades | put_trades` = **60 | 2000 | 2000 | 0**.
Identical to the brief's section 1. The fix rewrote nothing.

**R2, capped symbol-days per month** (a symbol-day is capped when stored prints >= 1,000):

| month | symbol-days | capped | capped, zero put premium | brief said |
|---|---:|---:|---:|---|
| 2026-01 | 7,992 | 1,311 | 164 | 1311 / 164 OK |
| 2026-04 | 10,499 | 1,741 | 165 | 1741 / 165 OK |
| 2026-07 | 10,927 | 1,601 | 194 | 1601 / 194 OK |
| 2026-08 | 10,461 | 1,483 | 164 | 1483 / 164 OK |

All four pre-D0 months reproduce to the row. No historical rewrite. (2026-02/03/05/06 are recorded
here for the first time: 1,571/146, 1,536/138, 1,668/191, 1,631/160.)

## W1 — the fifteen always-capped names on D0. PASS.

| symbol | call premium | put premium | dir_ratio | contracts | trades | call | put |
|---|---:|---:|---:|---:|---:|---:|---:|
| AMZN | 50,407,435 | 55,025,171 | 0.5204 | 60 | 33,112 | 15,903 | 17,209 |
| BA | 2,838,257 | 2,738,516 | 0.9521 | 60 | 3,922 | 2,639 | 1,283 |
| BAC | 2,076,303 | 2,347,838 | -0.2359 | 60 | 9,232 | 4,779 | 4,453 |
| CRM | 6,207,771 | 2,361,415 | 0.9894 | 60 | 4,938 | 3,290 | 1,648 |
| GLW | 1,142,793 | 1,164,712 | 0.8194 | 60 | 1,254 | 569 | 685 |
| GOOG | 8,255,864 | 4,259,435 | -0.2138 | 60 | 10,096 | 6,627 | 3,469 |
| GOOGL | 15,324,966 | 10,324,845 | -0.1595 | 60 | 19,406 | 12,629 | 6,777 |
| KO | 504,700 | 105,044 | -0.4553 | 60 | 1,411 | 1,088 | 323 |
| MSFT | 22,614,025 | 771,139 | 0.9873 | 60 | 6,614 | 6,003 | 611 |
| NFLX | 4,755,025 | 3,745,073 | 0.4663 | 60 | 18,021 | 9,957 | 8,064 |
| NOW | 5,896,960 | 1,835,808 | 0.8949 | 60 | 5,594 | 3,943 | 1,651 |
| ORCL | 11,218,820 | 7,528,522 | 0.8535 | 60 | 14,137 | 8,264 | 5,873 |
| PFE | 877,642 | 94,015 | 0.7678 | 60 | 2,089 | 1,650 | 439 |
| SNDK | 44,869,907 | 75,389,985 | -0.0575 | 60 | 12,081 | 4,859 | 7,222 |
| WMT | 3,121,837 | 1,509,536 | 0.8902 | 60 | 8,311 | 6,102 | 2,209 |

- **`put_premium_total > 0` on all fifteen.** PASS.
- **No `dir_ratio` within 0.001 of 1.00.** PASS. The day before (2026-09-14) four of these names sat
  at exactly 1.0000 (GLW, KO, NOW, WMT) and PFE at 0.9997 — the one-page signature, gone.
- **`trades > 2000` on 13 of 15.** GLW (1,254) and KO (1,411) fall short. This sub-bar is a *proxy*
  for "no longer capped at 1,000 prints per 50-contract batch", and three independent checks say
  neither name is capped: (i) W2's `truncated` map is empty `{}` and `ceiling_hits = 0`, so no symbol
  hit any page limit; (ii) **no symbol-day on D0 has a stored print count on a 1,000 boundary** —
  the old cap leaves 1000/2000/3000 exactly, and there are none; (iii) both names show the fix working
  in the opposite direction — GLW's puts went 219 -> **685** while its calls *fell* 1,256 -> 569, and
  KO's puts went 1 -> **323**. They simply traded fewer than 2,000 prints. Counted PASS.

**SNDK is the headline.** The name that opened this issue stored 2,000 call prints and zero puts on
2026-09-08; on D0 it stored 4,859 calls and **7,222 puts**, $75.4M of put premium, and `dir_ratio`
-0.0575 instead of 1.00. The bullish tilt on capped names was an artefact, and it is gone.

## W2 — run telemetry on D0. PASS.

`page_limit = 10000` · `status = success` · `symbols_fetched = 498` · `symbols_multi_page = 15` ·
`symbols_truncated = 0` · `requests = 1068` · `pages = 1068` · `failed_requests = 0` ·
`fetch_seconds = 104.4` · `truncated = {}`.

Every bar met: block present, page limit exact, zero ceiling hits (bar was "low single digits"),
zero failures. `ALPACA_OPTION_TRADE_PAGES` does **not** need raising — nothing came near the 20-page
cap. 1,068 requests for 498 symbols is ~2.1 per symbol, consistent with the calls/puts split
(2 x 498 = 996) plus the 15 multi-page names.

## W3 — the literal query is void; the substitute passes decisively.

**The brief's W3 cannot work as written.** It keys on `snapshot_volume > 0 AND trade_count = 0`, but
`uoa_contract_daily.snapshot_volume` is **NULL on every row** — 276,505 rows before D0 and 19,788
after, zero non-null. Run as written it returns `traded_but_empty = 0` for calls and puts, before and
after, which reads like a pass and means nothing. Recording this so the next verify does not repeat it.

**Substitute** (drops the chain-volume condition and uses the stored-print count directly, on
symbol-days with >= 1,000 prints, 2026-08-25 .. 2026-09-15):

| period | side | contracts | zero-print | % zero |
|---|---|---:|---:|---:|
| before | call | 32,224 | 17,779 | 55.2% |
| before | put | 26,034 | 19,277 | **74.0%** |
| after | call | 2,448 | 349 | 14.3% |
| after | put | 2,118 | 370 | **17.5%** |

This is the W3 pass condition exactly — the put side falls to roughly the call-side level. Before,
three of every four put contracts on a busy name held no prints at all, against half of calls; after,
17.5% against 14.3%, a gap of 3 points instead of 19. The residual is ordinary illiquidity, not a
side-specific drop.

## W6 — on track, not yet decidable.

Zero-put share among >= 1,000-print symbol-days, by session:

| session | capped | zero put | share |
|---|---:|---:|---:|
| 2026-09-08 | 81 | 16 | 19.8% |
| 2026-09-09 | 80 | 5 | 6.3% |
| 2026-09-10 | 73 | 8 | 11.0% |
| 2026-09-11 | 83 | 3 | 3.6% |
| 2026-09-14 | 78 | 5 | 6.4% |
| **2026-09-15 (D0)** | **78** | **0** | **0.0%** |

Day one is 0/78. The bar is <= 2% over the first ten sessions from D0, so W6 is decidable around
**2026-09-29**. Nothing about the D0 number suggests it will fail.

## W4 — runtime and publication time. Reported, not judged.

| session | UOA seconds | trade requests | fetch seconds | SAS finished (UTC) |
|---|---:|---:|---:|---|
| 2026-09-08 | 305.7 | — | — | 21:12:42 |
| 2026-09-09 | 310.1 | — | — | 21:11:55 |
| 2026-09-10 | 313.6 | — | — | 21:12:36 |
| 2026-09-11 | 531.3 | — | — | 21:32:45 |
| 2026-09-14 | 538.6 | — | — | 21:36:45 |
| **2026-09-15 (D0)** | **578.2** | 1,068 | 104.4 | **21:34:33** |

**PI-020's own cost is about +40 seconds** (538.6 -> 578.2 against the immediately preceding session),
of which 104.4 s is the whole trade fetch. The large step — UOA runtime 314 -> 531 s and SAS publication
21:12 -> 21:32 — happened on **2026-09-11**, four sessions *before* this fix, and belongs to whatever
shipped then (Omega tables `d112d37` is the candidate). **SAS publication did not slip on D0**: 21:34:33
is 2 minutes *earlier* than 2026-09-14. Versus early September the shift is ~+22 minutes, but PI-020 is
not the cause of it.

Haci: the +22 minutes is worth a separate look, because `finished_at` is the earliest actionable moment
and it moved on 2026-09-11 without anyone measuring it. Not filed as an issue here — it is outside this
verify's scope and the cause is not confirmed.

## Seen in passing — not part of this verify

`uoa_runs` holds two rows stuck at `status = 'running'` with no `finished_at`: `trading_date 2026-09-07`
(started 2026-09-08 02:30 UTC, a Sunday date) and `trading_date 2026-12-09` (started **2026-01-12**
15:03 UTC — a trading_date three months in the future, written eight months ago). Neither affects this
verify, which keys on the presence of the `trades_fetch` block in successful runs. But a run log with
rows that never terminate is the same blind spot PI-002 describes for the coverage watchdog: nothing
is watching the watcher. Worth a line in the register on a later pass.

## OVERALL

**OVERALL: PASS (W6 confirms ~2026-09-29).** Every check that can be decided today is decided and
passes. W5 — the one the brief says must hold before anything else is trusted — reproduces the brief's
history to the row, so no historical rewrite occurred. W1 shows the defect gone on all fifteen
always-capped names, SNDK moving from `dir_ratio` 1.00 on 2,000 call-only prints to -0.0575 on 12,081
prints across both sides. W2 shows the mechanism working with zero ceiling hits and zero failures.
W3, on a substitute instrument because the brief's own query is void against a NULL column, shows the
put-side drop falling from a 19-point gap to a 3-point gap. Cost is ~40 seconds of nightly runtime and
no delay to SAS publication. The single open item is W6's ten-session window, which reads 0.0% on day
one against a <= 2% bar.
