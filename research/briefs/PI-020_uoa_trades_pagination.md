# PI-020 — UOA option trades stop at one page: follow `next_page_token`, batch calls and puts apart, record every cut

**Type:** fix brief (platform issue, not a research finding)
**Register row:** `research/PLATFORM_ISSUES.md` PI-020, severity high, `HACI_DECIDED:fix`
**Written:** 2026-09-15 by the Brief Writer, on Haci's `/desk-run prompt PI-020` (DP-48: asking is the decision)
**Rewritten:** 2026-09-15 under **DP-59** — fixes ship directly: no feature flag, no shadow mode, no inertness
proof, no flip step returned to Haci. The change below is **always on from the merge**. Haci: *"Every brief wants to
create a flag. I don't want it, it's hard to keep. Fix is fix. We will check here if it is working fine. I am the
only user in the platform."*
**Platform repo:** `C:\Users\sahin\Projects\volatilx`
**Platform SHA all `path:line` citations are taken at:** `380336725f3d8e69f977ee0e6bd11898f13bed23`
(`3803367`, merge of `main` into `feat/en-019-fixed-universe-report-batch`; working tree clean). Every line number
below was re-verified at this SHA and is unchanged from the first draft's `c311e81`.
**Research repo SHA:** `f1a82f5`

**No feature flag, and why that is correct here (DP-59).** Reading every page is what this code was meant to do, and
nobody chose to drop puts. DP-59 says a fix that changes published numbers still ships; the brief names which
numbers change (next section) and the desk logs the ship date and SHA in `research/data/DATA_NOTES.md` so locked
questions split there (DP-50 unchanged). There is no `UOA_TRADES_PAGINATION_ENABLED`, no shadow mode, no
`record_trades_shadow`, no byte-identical hash of the old path and no flag-off/flag-on test pair. Telemetry is kept
— `uoa_runs.stats_json.trades_fetch` — because it tells the desk whether the fix is working; it gates nothing.

## What changes for the desk

From the ship date `D0` (the first trading date whose nightly runs the merged SHA):

- `uoa_symbol_daily.call_premium_total / put_premium_total / total_premium / call_buy_premium / put_buy_premium /
  net_directional_premium / dir_ratio / prem_day / prem_swing / prem_long` **change for liquid names**, and through
  cross-sectional percentiles (`services/uoa_screener.py:1699-1705`) `unusual_* / quality_* / conc_* / score_* /
  bias_* / label_* / why_json` move a little for **every** symbol.
- Downstream: the UOA bulletin lists (`uoa_bulletins.lists_json / markdown`), the SAS flow layer (weight 24,
  `services/super_agent_select_scoring.py:769-790`), the flow **direction vote** (`:537-560`) and the SAS candidate
  universe (`services/candidate_universe_builder.py:38-48`). So it can change which picks are published, and the
  bullish tilt on capped names should fall. That is the point of the fix.
- **No historical row is rewritten by this fix.** It is forward-only: nights before `D0` stay capped. Re-scoring
  history is a separate decision and is out of scope (§7).
- **The desk logs the ship SHA and `D0`** in `research/data/DATA_NOTES.md` (text in §8, Step 3). Under DP-50(a) a
  question whose window spans `D0` treats flow before and after as two different features. Named now, so the
  Registrar has it in writing: **Q014** `uoa_persistence` (DATASET_PINNED, decision 2027-04-05; reads
  `uoa_symbol.score_* / label_*` in the successor freeze through 2027-02-25 — `Q014 PREREG.md:44-51`, `:424-436`),
  **Q029** `layer_value_ablation` (PREREG_LOCKED, 2027-04-12; `flow_strength` on the prospective window
  2026-09-15..2027-03-05 — `Q029 PREREG.md:20-32`, `:191`), **Q019** `conviction_monitor_exit` (DATASET_PINNED,
  2027-05-24; the polarity arm reads the `uoa_contract_daily` buy/sell decomposition,
  `services/symbol_context_builder.py:136-175`), **Q030** `universe_discovery_recall` (PREREG_LOCKED, 2027-03-01;
  rebuilds the universe from the bulletin lists, `Q030 PREREG.md:653-658`), and every locked question whose
  prospective window reads the published slate or `overall_score` (Q027; Q024, whose threat 8 at
  `Q024 PREREG.md:248` is exactly this defect). None of them is a reason to delay the fix; they are the reason the
  split date must be recorded on the day it ships.

You are the coding agent working in the platform repo. This brief is self-contained: do not ask questions, do not
redesign, do not widen the scope. Implement §3, run §4, add §5, report the SHA.

**Nothing in this brief runs against a database.** Under DP-49 you get no DB step at all: your credential on that
Postgres is the platform's read-write role on live production. Two specific prohibitions:

- **Do not run `pytest` in this repo** (research PI-021). `conftest.py:31-35` runs `create_tables()` (DDL), and the
  autouse fixture at `conftest.py:38-57` deletes every row of `UserActivityEvent` and `User` before and after
  **every test**, in whatever database `DATABASE_URL` names. Run the §5 test as
  `python tests/test_uoa_trades_pagination.py` with `DATABASE_URL` unset. It loads no conftest.
- **Do not run the UOA nightly, any `scripts/run_uoa_*.py`, `scripts/run_nightly_pipeline.py` or the app.** There is
  no DB-free dry run of the screener: `run_uoa_nightly` queries `uoa_bulletins` at
  `services/uoa_screener.py:1311-1316` before doing anything else.

Whose step is whose: the coding agent's work ends at §4 and §5, which are repo-only. Merging and deploying are
**Haci's**. The §8 queries are the **Data Steward's**, on the read-only role, after deploy.

**Indentation:** `services/uoa_screener.py` is **tab-indented**. The snippets for it below are shown with tabs; keep
them tabs. `ai_agents/options_client.py` and `tests/` are 4-space indented.

---

## 1. Symptom — what is wrong, and the evidence

The UOA screener reads at most **1,000 option trades per 50-contract request** and never asks for the next page. On
liquid names a busy request holds far more than 1,000 prints. Alpaca returns the page ordered by contract symbol,
and an OCC symbol sorts by expiry, then `C` before `P`, then strike. So the page fills with the nearest expiry's
calls, and every put comes back with zero trades. The screener then stores a zero-trade row for each such contract
and builds `dir_ratio` from the truncated totals.

**The traced night (research `reports/case_SNDK_2026-09-15/`, read-only DB plus Alpaca market data).** SNDK
2026-09-08: `uoa_contract_daily` holds 60 contracts and 2,000 trades, with trades on calls only and 0 puts. The
platform's request shape for the first 50 contracts returns 1,000 trades over 8 call contracts plus a
`next_page_token` (`verify_trades.py` step (a)). Paginated, the same 50 contracts hold **14,441 call trades
($200.7M) and 11,154 put trades ($82.5M)** (`verify_trades.py` step (b); `REPORT.md:67-69`). Stored `dir_ratio`: 1.00.

**The same night in the pinned freeze (DP-50(c); not a live query).**
`research/data/v001_uoa_symbol.parquet` (manifest_v001, as_of 2026-09-10, 83,747 rows, 2026-01-07..2026-09-10,
sha256 `1b959ef809fe925d4f1794e1ae347d385879823fa133cb1f051dd983fae34ac4`):

| trading_date | symbol | call_premium_total | put_premium_total | dir_ratio |
|---|---|---:|---:|---:|
| 2026-09-08 | SNDK | 54,213,915 | 0 | 1.000000 |
| 2026-09-08 | AMZN | 9,616,580 | 0 | 0.999999 |
| 2026-09-08 | GOOGL | 1,137,654 | 0 | 0.999991 |
| 2026-09-08 | MSFT | 1,814,598 | 100,543 | 0.827767 |

**The asymmetry across the freeze.** Counting rule: one row per `(trading_date, symbol)`; "call-only" is
`call_premium_total > 0 AND put_premium_total = 0`; "put-only" is the mirror. This is descriptive only. It includes
names that truly had no put prints, and the parquet carries no trade counts (`uoa_contract_daily` is not in
manifest_v001). The imbalance is the signature, not a count of truncated rows.

| month | rows | call-only | put-only |
|---|---:|---:|---:|
| 2026-01 | 7,992 | 806 | 180 |
| 2026-02 | 9,497 | 838 | 155 |
| 2026-03 | 10,459 | 725 | 419 |
| 2026-04 | 10,499 | 787 | 263 |
| 2026-05 | 9,977 | 854 | 214 |
| 2026-06 | 10,446 | 1,084 | 224 |
| 2026-07 | 10,927 | 1,261 | 250 |
| 2026-08 | 10,461 | 1,213 | 263 |
| 2026-09 (to 09-10) | 3,489 | 350 | 142 |

**Scale (live read-only counts, 2026-09-15, `truncation_scale.py`).** Counting rule: a symbol-day is "capped" when
`sum(uoa_contract_daily.trade_count) >= 1000`. That is a floor, because the batch split is not stored.

| month | symbol-days | capped | capped with zero put premium |
|---|---:|---:|---:|
| 2026-01 | 7,992 | 1,311 | 164 |
| 2026-04 | 10,499 | 1,741 | 165 |
| 2026-07 | 10,927 | 1,601 | 194 |
| 2026-08 | 10,461 | 1,483 | 164 |

Since 2026-06-01, **317 of 604** published SAS picks had a capped UOA row on their pick night (64 with zero put
premium). **GOOG, GOOGL, MSFT, AMZN, NFLX, ORCL, CRM, NOW, KO, WMT, BAC, BA, PFE, GLW and SNDK are capped every
session** — those fifteen names are the after-deploy check in §8. Their rows predate the fix and the fix rewrites
none of them, so the same query on past months must return the same numbers after deploy (§8 W5).

### Reproducing queries — **Data Steward only**, read-only role on `$RESEARCH_DB_URL`

Not for the coding agent (DP-49). Counts only.

```sql
-- R1. The traced night: 60 contracts, 2,000 trades, calls only.
SELECT count(*)                                                            AS contracts,
       sum(trade_count)                                                    AS trades,
       sum(CASE WHEN option_type = 'call' AND trade_count > 0 THEN 1 ELSE 0 END) AS calls_with_trades,
       sum(CASE WHEN option_type = 'put'  AND trade_count > 0 THEN 1 ELSE 0 END) AS puts_with_trades
FROM uoa_contract_daily
WHERE underlying_symbol = 'SNDK' AND trading_date = DATE '2026-09-08';
-- Expected today and after the fix (a historical row, never rewritten): 60 | 2000 | >0 | 0

-- R2. Capped symbol-days per month (truncation_scale.py's definition).
WITH c AS (
  SELECT trading_date, underlying_symbol AS sym, sum(trade_count) AS trades,
         sum(CASE WHEN option_type = 'put' THEN premium_total ELSE 0 END) AS put_prem
  FROM uoa_contract_daily GROUP BY 1, 2)
SELECT to_char(trading_date, 'YYYY-MM') AS m, count(*) AS symbol_days,
       sum(CASE WHEN trades >= 1000 THEN 1 ELSE 0 END) AS capped,
       sum(CASE WHEN trades >= 1000 AND put_prem = 0 THEN 1 ELSE 0 END) AS capped_zero_put
FROM c GROUP BY 1 ORDER BY 1;
```

---

## 2. Cause

**`ai_agents/options_client.py:985-1018`, `get_option_trades`:**

```python
        aggregated: Dict[str, Any] = {}
        for batch in self._chunk(valid, _SNAPSHOT_BATCH):          # :1007, 50 per batch (_SNAPSHOT_BATCH, :17)
            params: Dict[str, Any] = {
                "symbols": ",".join(batch),
                "limit": limit,
            }
            if start:
                params["start"] = start
            if end:
                params["end"] = end
            payload = self._request("/trades", params)              # :1016
            aggregated.update(payload.get("trades", {}))            # :1017, next_page_token never read
        return {"trades": aggregated}
```

Pagination is not missing from the file, only from this method. The contract list follows `next_page_token` at
`:563-588` (`_list_contracts`, token read at `:584`), and the underlying snapshot fetch at `:903-917`
(`_fetch_underlying_snapshots`, token at `:914`, bounded by `_MAX_SNAPSHOT_PAGES` at `:33`). The fix reuses that
pattern: send `page_token`, read `next_page_token`, stop at a bounded page count.

**`services/uoa_screener.py`, the nightly caller:**
- `:1453` `contract_symbols` come from `selected`, which `_pick_contracts` ranks by bucket, snapshot volume, OI,
  spread and ATM distance (`:1177-1189`). Calls and puts are interleaved, so each 50-contract batch mixes both.
- `:1504-1509` calls `get_option_trades(contract_symbols, start=start_iso, end=end_iso, limit=cfg.trades_limit)`,
  with `trades_limit = 1000` (`:806`). `:1510` reads `trades_map`.
- `:1520-1537` stores a zero-trade row for every contract the page did not reach (`trade_count 0`, `buy_premium 0.0`).
- `:1602-1605` builds `dir_ratio` from the truncated call and put totals. `:1609-1622` builds `prem_day/swing/long`
  from them too.

The other two callers are `ai_agents/omega_agent.py:1655-1673` (an LLM tool; it clamps `limit` to 10,000 at `:1669`,
which also shows the endpoint's page maximum) and `ai_agents/option_flow_monitor.py:92-97` (a live 10-minute
window). Both have the same defect, and both are fixed by this change because the fix is in the method they call.

---

## 3. Change

### Design choices, justified from the code

1. **`get_option_trades` itself paginates. One method, no second path.** The old body is replaced, not kept beside a
   new one. Every caller — the nightly screener, the omega tool, the flow monitor — gets complete prints. There is
   nothing to switch on and nothing to keep in step.
2. **Calls and puts go in separate batches, always.** A page ceiling on a mixed batch still returns calls first, so
   any ceiling would keep crowding out puts. Batched apart, each side gets its own page budget, and a ceiling hit on
   the call side cannot cost the put side a single print (§5 T4). A residual bias remains *inside* a side when a
   ceiling is hit: later expiries and higher strikes are read last. That is recorded (`truncated_sides`), not hidden.
   Per-contract requests were rejected: 60 requests per symbol is about 30,000 a night. Per-(type, expiry) batches
   were also rejected: more requests, and a recorded ceiling already covers the case.
3. **A generous, recorded ceiling.** `_MAX_TRADE_PAGES = 20` pages per side-batch, in the `_MAX_SNAPSHOT_PAGES` shape
   already at `options_client.py:33`, so a runaway night can be bounded without a deploy. It is a safety bound, not a
   gate: pagination happens at every value. With page size 10,000 (the endpoint's maximum — `omega_agent.py:1669`;
   `verify_trades.py:31` paged with it) that is 200,000 prints per side, about **fourteen times** SNDK's call side on
   2026-09-08. Worst-case memory is 2 side-batches × 20 pages × 10,000 prints for one symbol, released before the
   next. Every ceiling hit lands in `uoa_runs.stats_json` with the symbol and the side, so the Steward sees it
   (§8 W2) instead of guessing.
4. **`UoaConfig.trades_limit` 1000 → 10000 (`:806`).** With pagination the parameter is the *page size*, not a cap on
   what is read. 10,000 is the endpoint's maximum and it keeps the request count down: SNDK's call side becomes 2
   pages instead of 16. It is used in exactly one place (`git grep trades_limit` at this SHA returns `:806`, `:1508`
   and one line of `reports/pipeline_repair.md`).
5. **Telemetry in `uoa_runs.stats_json`, no schema change.** `stats_json` is a Text JSON column (`models.py:399`,
   `set_stats` `:413-414`), written at `services/uoa_screener.py:2006`. It is read only by the diagnostic passthrough
   `routers/uoa_screener.py:869-880` (behind login) and `scripts/diagnose_uoa_oi.py:92`. `uoa_symbol_daily.why_json`
   was rejected as the home for it: it is served to users (`routers/uoa_screener.py:1119`), fed to SAS context
   (`services/symbol_context_builder.py:323`, `:392`) and to the MCP server (`fmp_mcp_server/server.py:1556`,
   `:1643`). Nothing in `models.py` changes. No migration exists, and **none is to be written or run**.
6. **Cost.** About 1,500 capped symbol-days a month over about 21 sessions is about 70 symbols a night, out of about
   500. Today each symbol already costs about 25–30 Alpaca requests: a contract-list page, 12 snapshot batches for
   600 contracts (`options_client.py:705-708`, `:854-858`), up to 14 contract lookups (`uoa_screener.py:1466-1467`,
   `:1627`) and 2 trade requests. After the fix a typical symbol still sends 2 trade requests (one per side, both a
   single page at limit 10,000); a SNDK-like name sends 4. Expect roughly +150–300 requests a night, with the ceiling
   bounding the worst case. 429s are already retried with `Retry-After` (`options_client.py:77-93`, `:102-105`). Page
   latency is the unknown, so the run block records elapsed seconds and §8 W4 reads the publication-time shift.

### 3.1 `ai_agents/options_client.py` — module constant

After `_MAX_SNAPSHOT_PAGES = int(os.getenv("ALPACA_OPTION_SNAPSHOT_PAGES", "5"))` at `:33`, add:

```python
_MAX_TRADE_PAGES = int(os.getenv("ALPACA_OPTION_TRADE_PAGES", "20"))  # safety bound, research PI-020
```

### 3.2 `ai_agents/options_client.py` — `get_option_trades` paginates (4 spaces)

Replace the whole method, `:985-1018` (from `def get_option_trades(` through `return {"trades": aggregated}`), with:

```python
    def get_option_trades(
        self,
        contract_symbols: List[str],
        start: Optional[str] = None,
        end: Optional[str] = None,
        limit: int = 1000,
        *,
        max_pages: int = _MAX_TRADE_PAGES,
    ) -> Dict[str, Any]:
        """Return trade prints for the requested option contracts (research PI-020).

        Alpaca orders a multi-contract /trades response by contract symbol, and an OCC symbol sorts
        by expiry, then C before P, then strike. One page of a busy batch therefore holds only the
        nearest expiry's calls. This method follows next_page_token until the batch is exhausted
        (or max_pages is reached, which is recorded), and requests calls and puts in separate
        batches so a ceiling on one side can never spend the other side's budget.

        `limit` is the page size (Alpaca's maximum is 10000), not a cap on what is returned.
        Returns {"trades": {contract: [row, ...]}, "fetch": {...}}; "fetch" is telemetry only.
        """
        fetch: Dict[str, Any] = {
            "page_limit": int(limit),
            "max_pages_per_batch": max(int(max_pages), 1),
            "batches": 0,
            "pages": 0,
            "requests": 0,
            "failed_requests": 0,
            "failed_batches": 0,
            "truncated": False,
            "truncated_batches": 0,
            "truncated_sides": [],
            "trades_returned": {"call": 0, "put": 0},
        }
        if not contract_symbols:
            return {"trades": {}, "fetch": fetch}

        valid, invalid = self._sanitize_contract_symbols(contract_symbols)
        if invalid:
            logger.warning(
                "Dropping invalid option symbols for trades",
                extra={"invalid_symbols": invalid, "symbol_count": len(contract_symbols)},
            )
        if not valid:
            return {"trades": {}, "fetch": fetch}

        # _sanitize_contract_symbols guarantees ROOT + YYMMDD + C|P + 8-digit strike (_CONTRACT_SYMBOL_RE, :31).
        groups = [
            ("call", [s for s in valid if s[-9] == "C"]),
            ("put", [s for s in valid if s[-9] == "P"]),
        ]
        page_cap = fetch["max_pages_per_batch"]
        aggregated: Dict[str, Any] = {}
        truncated_sides = set()
        for side, symbols in groups:
            for batch in self._chunk(symbols, _SNAPSHOT_BATCH):
                fetch["batches"] += 1
                batch_trades: Dict[str, Any] = {}
                next_token: Optional[str] = None
                pages_ok = 0
                cut_short = False
                while True:
                    params: Dict[str, Any] = {
                        "symbols": ",".join(batch),
                        "limit": limit,
                    }
                    if start:
                        params["start"] = start
                    if end:
                        params["end"] = end
                    if next_token:
                        params["page_token"] = next_token
                    payload = self._request("/trades", params)
                    fetch["requests"] += 1
                    if not isinstance(payload, dict) or not payload:
                        # _request returns {} once its retries are exhausted.
                        fetch["failed_requests"] += 1
                        if pages_ok == 0:
                            fetch["failed_batches"] += 1
                        else:
                            cut_short = True
                        break
                    pages_ok += 1
                    fetch["pages"] += 1
                    for sym, rows in (payload.get("trades") or {}).items():
                        if isinstance(rows, list):
                            batch_trades.setdefault(sym, []).extend(rows)
                            fetch["trades_returned"]["call" if str(sym)[-9:-8] == "C" else "put"] += len(rows)
                        else:
                            batch_trades[sym] = rows
                    next_token = payload.get("next_page_token") or payload.get("nextPageToken")
                    if not next_token:
                        break
                    if pages_ok >= page_cap:
                        cut_short = True
                        break
                aggregated.update(batch_trades)
                if cut_short:
                    fetch["truncated_batches"] += 1
                    truncated_sides.add(side)
        fetch["truncated_sides"] = sorted(truncated_sides)
        fetch["truncated"] = bool(truncated_sides)
        return {"trades": aggregated, "fetch": fetch}
```

The two non-screener callers need no edit: `ai_agents/option_flow_monitor.py:92-98` and
`ai_agents/omega_agent.py:1655-1681` both read `payload.get("trades", {})`, so the added `"fetch"` key is additive
for them and they now see complete prints. The omega tool's result stays bounded by its own `max_limit` clamp
(`:1669`) times `_MAX_TRADE_PAGES`.

### 3.3 `services/uoa_screener.py` — page size (tabs)

`:806`, in `UoaConfig`:

```python
	trades_limit: int = 10000  # PI-020: /trades page size (Alpaca max); pagination reads every page
```

### 3.4 `services/uoa_screener.py` — two pure helpers (tabs)

Insert immediately **after** `_aggregate_trades_for_contract` ends (its `return {...}` closes at `:1271`) and
**before** `def _label_for_bucket(` at `:1274`:

```python
# --- Option-trade fetch telemetry (research PI-020) ----------------------------
# get_option_trades used to read one page (limit=1000) per 50-contract batch and drop next_page_token.
# Alpaca orders a multi-contract response by OCC symbol (expiry, then C before P, then strike), so on
# busy names the page held only near-dated calls and the puts came back empty. It now pages to the end,
# calls and puts apart. These helpers record what each night's fetch cost and where a ceiling was hit.
# They gate nothing: scoring always reads the paginated trades map.


def new_trades_fetch_stats(config: UoaConfig) -> Dict[str, Any]:
	"""The uoa_runs.stats_json["trades_fetch"] block for one run. Pure: no DB, no I/O."""
	return {
		"page_limit": int(config.trades_limit),
		"split_by_type": True,
		"symbols_fetched": 0,
		"symbols_multi_page": 0,
		"symbols_truncated": 0,
		"requests": 0,
		"pages": 0,
		"failed_requests": 0,
		"fetch_seconds": 0.0,
		"truncated": {},
	}


def record_trades_fetch(acc: Dict[str, Any], symbol: str, fetch_meta: Any, seconds: float) -> None:
	"""Fold one symbol's fetch into the run block. A symbol is named only when it was cut short. Pure."""
	meta = fetch_meta if isinstance(fetch_meta, Mapping) else {}
	requests = int(meta.get("requests") or 0)
	batches = int(meta.get("batches") or 0)
	truncated_batches = int(meta.get("truncated_batches") or 0)
	acc["symbols_fetched"] += 1
	acc["requests"] += requests
	acc["pages"] += int(meta.get("pages") or 0)
	acc["failed_requests"] += int(meta.get("failed_requests") or 0)
	acc["fetch_seconds"] = round(float(acc["fetch_seconds"]) + float(seconds or 0.0), 3)
	if requests > batches:
		acc["symbols_multi_page"] += 1
	if truncated_batches > 0:
		acc["symbols_truncated"] += 1
		acc["truncated"][str(symbol).upper()] = {
			"batches": batches,
			"truncated_batches": truncated_batches,
			"sides": list(meta.get("truncated_sides") or []),
			"requests": requests,
			"pages": int(meta.get("pages") or 0),
			"trades_returned": dict(meta.get("trades_returned") or {}),
		}
```

Add both public names to `__all__` at `services/uoa_screener.py:2457-2465`, after `"backfill_uoa_outcomes_range",`:
`"new_trades_fetch_stats"`, `"record_trades_fetch"`.

### 3.5 `services/uoa_screener.py` — initialise the run block

Insert immediately **after** `stats["force_deleted"] = deleted` at `:1423` and before `for symbol in universe_syms:`
at `:1425`:

```python
	# PI-020: what tonight's option-trade fetch cost, and every place a ceiling was hit.
	trades_fetch_stats = new_trades_fetch_stats(cfg)
	stats["trades_fetch"] = trades_fetch_stats
```

`stats` is serialised at `:2006` (`run.set_stats(stats)`) and again at `:2014` and `:2034`; the block rides along.

### 3.6 `services/uoa_screener.py` — the fetch at `:1504-1510`

Replace exactly the six lines `trades_payload = options_client.get_option_trades(` … `)` at `:1504-1509`, keep
`:1510` (`trades_map = ...`) as it is, and add the recording call after it:

```python
		# PI-020: read every page of prints, calls and puts in separate batches.
		trades_fetch_t0 = datetime.now(timezone.utc)
		trades_payload = options_client.get_option_trades(
			contract_symbols,
			start=start_iso,
			end=end_iso,
			limit=cfg.trades_limit,
		)
		trades_map = trades_payload.get("trades", {}) if isinstance(trades_payload, dict) else {}
		record_trades_fetch(
			trades_fetch_stats,
			symbol,
			trades_payload.get("fetch", {}) if isinstance(trades_payload, dict) else {},
			(datetime.now(timezone.utc) - trades_fetch_t0).total_seconds(),
		)
```

`datetime` and `timezone` are already imported at `:9` and used this way at `:1302`. Note that `time` at `:9` is
`datetime.time`, not the `time` module; do not add `import time`. Nothing from `:1511` onward changes: the
per-contract loop, `dir_ratio`, `prem_*`, percentiles, scores, labels and the bulletin builder are untouched — they
simply receive a complete `trades_map`.

### 3.7 Docs — `docs/UOA_SCREENER_MVP.md`

Replace `§2.3` at `docs/UOA_SCREENER_MVP.md:107-115` (from `### 2.3 Trades (intraday prints)` through
`MVP design assumes you compute UOA primarily from these trade rows.`) with:

```markdown
### 2.3 Trades (intraday prints)
Method: `AlpacaOptionsClient.get_option_trades(contract_symbols, start=..., end=..., limit=...)`
- Under the hood: `/v1beta1/options/trades`, up to 50 contracts per request
- For each contract: list of trade rows; the code expects:
  - `p` or `price`
  - `s` or `size`
  - `t` or `timestamp`

**Pagination (PI-020, shipped 2026-09-15).** Alpaca orders a multi-contract response by OCC symbol (expiry, then C
before P, then strike), so one page of 1,000 prints on a busy name held only near-dated calls and the puts came back
empty. The method now follows `next_page_token` to the end of each batch, and requests calls and puts in separate
batches so a page ceiling on one side cannot starve the other. `limit` is the page size (`UoaConfig.trades_limit` =
10,000, Alpaca's maximum); `ALPACA_OPTION_TRADE_PAGES` (20) is the per-batch safety bound. Every nightly writes
`uoa_runs.stats_json.trades_fetch`: page size, symbols fetched, pages, requests, elapsed seconds, and every symbol
whose fetch hit the ceiling, with the side (`truncated`). From the ship date, flow premiums, `dir_ratio` and the
cross-sectional scores are built from every print; earlier nights are capped.

MVP design assumes you compute UOA primarily from these trade rows.
```

That is the whole change: `ai_agents/options_client.py`, `services/uoa_screener.py`, `docs/UOA_SCREENER_MVP.md`, and
a new `tests/test_uoa_trades_pagination.py`. Nothing else.

---

## 4. Before / after check — repository only, no database, no network

This is the coding agent's own check. `DATABASE_URL` must be unset in the shell for every command
(PowerShell: `Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue`; Git Bash: `unset DATABASE_URL`). None of
these commands opens a connection. `ai_agents/options_client.py` imports only the standard library, `requests` and
`core.datetime_utils` (`:1-10`), and `ai_agents/__init__.py` imports nothing. `services/uoa_screener.py` imports
`models` (`:22-30`), and `models.py:1-7` imports only SQLAlchemy symbols. No module in that chain imports `db.py`;
`user.py:7` is the one that does, and nothing here imports `user`. Importing the screener pulls `indicator_fetcher`
→ `symbol_map`, which may try the Alpaca asset catalogue and fall back offline. That is slow, not a DB call.

The fixed trading date for every check is **2026-09-08** (SNDK, the traced night), built as the §5 fixture.

**(a) The test — before and after.**

```
python tests/test_uoa_trades_pagination.py
```

Before the change: the file does not exist. With the test file added but the code not yet changed, T3 and T7 fail
(`put_trades == 0`, the defect). After the change: exactly `PI-020: 9/9 checks passed`.

**(b) The page size the nightly will send.**

```
python -c "import os; [os.environ.pop(k, None) for k in ('DATABASE_URL','ALPACA_OPTION_TRADE_PAGES')]; from services.uoa_screener import UoaConfig; from ai_agents.options_client import _MAX_TRADE_PAGES; print(UoaConfig().trades_limit, _MAX_TRADE_PAGES)"
```

Before: `1000`, and `ImportError: cannot import name '_MAX_TRADE_PAGES'`. After, exactly: `10000 20`.

**(c) Nothing outside the four files moved — proved by diff, not by running anything.**

Commit PI-020 as **one commit** containing only the four paths in §3. Then:

```
git show --stat HEAD
git diff --quiet HEAD~1 HEAD -- services/super_agent_select_scoring.py services/super_agent_select_service.py services/symbol_context_builder.py services/candidate_universe_builder.py services/uoa_scheduler.py services/gex.py scripts/ routers/ models.py db.py conftest.py core/ fmp_mcp_server/ ai_agents/omega_agent.py ai_agents/option_flow_monitor.py && echo UNCHANGED
```

- `git show --stat HEAD` lists exactly `ai_agents/options_client.py`, `services/uoa_screener.py`,
  `docs/UOA_SCREENER_MVP.md`, `tests/test_uoa_trades_pagination.py`.
- The `git diff --quiet` line prints `UNCHANGED`. No migration file, no schema change, no scripts.
- `git show HEAD -- services/uoa_screener.py` shows removals only at `:806` and `:1504-1509`.

**(d) What must change and what must not, stated for the PR.** Must change on the next nightly: `uoa_contract_daily`
and `uoa_symbol_daily` for capped names, and the percentile columns for all names (§8 W1, W3). Must not change: any
row dated before the deploy (§8 W5), any schema, any router response shape, any script.

---

## 5. Test — `tests/test_uoa_trades_pagination.py`

A standalone runner, the EN-019 pattern: no pytest fixtures, no conftest, no database, no network. The network seam
is `AlpacaOptionsClient._request`, replaced on the instance by an in-memory fake that honours `symbols`, `limit` and
`page_token` with Alpaca's ordering. The pre-fix behaviour is reproduced *inside the test* by `_legacy_single_page`,
which is the old `:1007-1017` loop (chunks of 50 in the caller's order, one request each, token dropped) — so the
defect stays visible after the code that caused it is gone.

**Fixture provenance:** the SNDK fixture reproduces the desk's measured totals for 2026-09-08
(`research/reports/case_SNDK_2026-09-15/verify_trades.py`): 14,441 call and 11,154 put prints on the first 50
contracts, 60 contracts in all, stored as 2,000 prints, all calls. The split across contracts and the prices are
synthetic. Every print is $1.00 × 1 contract, a $100 premium. Alpaca prints are not frozen, and the desk does not
ship market data into the platform repo. **Which line would have caught the bug:** T3 (a fetch returns both sides)
and T7 (`put_trades == 0`, `dir_ratio` pinned at 1.00 on the single page).

```python
"""PI-020: UOA option trades must not stop at one page.

Before the fix, get_option_trades sent one /trades request per 50-contract batch with limit=1000 and
never read next_page_token. Alpaca orders a multi-contract response by contract symbol, and an OCC
symbol sorts expiry -> C before P -> strike, so a busy batch returned only the nearest expiry's calls.
SNDK 2026-09-08: stored 2,000 trades, all calls, dir_ratio 1.00; paginated, 14,441 call and 11,154 put
trades on the first 50 contracts (research PI-020, case_SNDK_2026-09-15/verify_trades.py).

Offline: no database, no network. Run as
    python tests/test_uoa_trades_pagination.py
with DATABASE_URL unset. Do NOT run under pytest in an environment whose DATABASE_URL points at a
real database: conftest.py:31-57 runs create_tables() and deletes every users row around each test.
"""

from __future__ import annotations

import json
import os
import sys
import types
from datetime import datetime, timedelta, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

os.environ.pop("DATABASE_URL", None)
os.environ.pop("ALPACA_OPTION_TRADE_PAGES", None)
_DB_STUB = types.ModuleType("db")
sys.modules.setdefault("db", _DB_STUB)  # any `from db import ...` raises ImportError

from ai_agents.options_client import _SNAPSHOT_BATCH, AlpacaOptionsClient  # noqa: E402

START = "2026-09-08T13:30:00Z"  # _session_window_utc(2026-09-08)
END = "2026-09-08T20:00:00Z"
_T0 = datetime(2026, 9, 8, 13, 30, tzinfo=timezone.utc)


# --- fixture ------------------------------------------------------------------

def _occ(root, yymmdd, side, strike):
    return f"{root}{yymmdd}{side}{int(round(strike * 1000)):08d}"


def _rows(n):
    return [
        {"t": (_T0 + timedelta(seconds=i)).isoformat().replace("+00:00", "Z"), "p": 1.0, "s": 1, "x": "C"}
        for i in range(n)
    ]


def _spread(total, parts):
    base, extra = divmod(total, parts)
    return [base + (1 if i < extra else 0) for i in range(parts)]


def _meta(sym, side, buckets):
    return {"symbol": sym, "type": side, "bid": 0.90, "ask": 1.00, "buckets": list(buckets)}


def _sndk_case():
    """60 contracts in the screener's mixed order -> pre-fix batches of 50 + 10, both capped.

    First 50 (exp 2026-09-11, DTE 3): 14,441 call and 11,154 put prints (the desk's paginated totals).
    Last 10 (exp 2026-09-18, DTE 10): 1,250 call and 500 put prints.
    """
    trades, selected = {}, []
    groups = (
        ("260911", 25, 14441, 11154, 1500.0, ("day",)),
        ("260918", 5, 1250, 500, 1600.0, ("day", "swing")),
    )
    for yymmdd, n, call_total, put_total, strike0, buckets in groups:
        calls = [_occ("SNDK", yymmdd, "C", strike0 + 12.5 * i) for i in range(n)]
        puts = [_occ("SNDK", yymmdd, "P", strike0 + 12.5 * i) for i in range(n)]
        for sym, k in zip(calls, _spread(call_total, n)):
            trades[sym] = _rows(k)
        for sym, k in zip(puts, _spread(put_total, n)):
            trades[sym] = _rows(k)
        for c, p in zip(calls, puts):
            selected.append(_meta(c, "call", buckets))
            selected.append(_meta(p, "put", buckets))
    return trades, selected


def _small(call_counts, put_counts):
    trades, selected = {}, []
    for i, (kc, kp) in enumerate(zip(call_counts, put_counts)):
        c = _occ("KO", "260911", "C", 60.0 + i)
        p = _occ("KO", "260911", "P", 60.0 + i)
        trades[c], trades[p] = _rows(kc), _rows(kp)
        selected += [_meta(c, "call", ("day",)), _meta(p, "put", ("day",))]
    return trades, selected


def _syms(selected):
    return [m["symbol"] for m in selected]


class _FakeAlpacaTrades:
    """In-memory /v1beta1/options/trades: ordered by contract symbol, then by time; offset page tokens."""

    def __init__(self, trades_by_contract, fail_on_request=None):
        self.trades_by_contract = trades_by_contract
        self.fail_on_request = fail_on_request
        self.calls = []

    def __call__(self, path, params=None, *, base_url=None):
        params = dict(params or {})
        self.calls.append((path, list(params.items())))
        if self.fail_on_request is not None and len(self.calls) == self.fail_on_request:
            return {}  # what _request returns once its retries are exhausted
        assert path == "/trades", path
        flat = [(s, r) for s in sorted(params["symbols"].split(",")) for r in self.trades_by_contract.get(s, [])]
        offset, limit = int(params.get("page_token") or 0), int(params["limit"])
        out = {}
        for s, r in flat[offset: offset + limit]:
            out.setdefault(s, []).append(r)
        more = offset + limit < len(flat)
        return {"trades": out, "next_page_token": str(offset + limit) if more else None}


def _client(fake):
    client = AlpacaOptionsClient(api_key="test", secret_key="test")
    client._request = fake  # the only network seam; nothing leaves the process
    return client


def _fetch(trades, selected, *, limit=10000, max_pages=20, fail_on_request=None):
    fake = _FakeAlpacaTrades(trades, fail_on_request)
    out = _client(fake).get_option_trades(
        _syms(selected), start=START, end=END, limit=limit, max_pages=max_pages,
    )
    return out, fake


def _legacy_single_page(trades, selected, limit=1000):
    """The pre-fix algorithm, options_client.py:1007-1017 at c311e81: chunks of 50 in caller order,
    one request each, next_page_token dropped. Kept here so the defect stays reproducible."""
    fake = _FakeAlpacaTrades(trades)
    syms = _syms(selected)
    aggregated = {}
    for i in range(0, len(syms), _SNAPSHOT_BATCH):
        batch = syms[i: i + _SNAPSHOT_BATCH]
        aggregated.update(fake("/trades", {"symbols": ",".join(batch), "limit": limit}).get("trades", {}))
    return aggregated, fake


# --- client -------------------------------------------------------------------

def test_t1_small_symbol_one_page_per_side_no_truncation():
    trades, selected = _small((100, 120, 90), (80, 60, 110))
    out, fake = _fetch(trades, selected)
    assert out["trades"] == trades  # every print of every contract
    f = out["fetch"]
    assert (f["batches"], f["requests"], f["pages"], f["truncated_batches"]) == (2, 2, 2, 0), f
    assert f["truncated"] is False and f["truncated_sides"] == []
    assert f["trades_returned"] == {"call": 310, "put": 250}
    for _path, params in fake.calls:
        assert len({s[-9] for s in dict(params)["symbols"].split(",")}) == 1  # one side per request


def test_t2_failed_first_page_is_recorded_and_the_other_side_still_reads():
    trades, selected = _small((100, 100, 100), (100, 100, 100))
    out, _ = _fetch(trades, selected, fail_on_request=1)  # the call batch fails outright
    f = out["fetch"]
    assert (f["requests"], f["failed_requests"], f["failed_batches"], f["truncated_batches"]) == (2, 1, 1, 0), f
    assert out["trades"] and all(s[-9] == "P" for s in out["trades"])  # puts survived the call side's failure
    assert f["trades_returned"] == {"call": 0, "put": 300}


def test_t3_sndk_paginated_sees_both_sides():
    trades, selected = _sndk_case()
    out, fake = _fetch(trades, selected)
    f = out["fetch"]
    assert (f["batches"], f["requests"], f["truncated_batches"], f["failed_requests"]) == (2, 4, 0, 0), f
    assert f["trades_returned"] == {"call": 15691, "put": 11654}
    assert out["trades"] == trades  # including contracts split across pages
    for _path, params in fake.calls:
        assert len({s[-9] for s in dict(params)["symbols"].split(",")}) == 1


def test_t4_page_ceiling_is_side_balanced_and_recorded():
    trades, selected = _small((600, 600, 600), (400, 400, 400))
    capped, _ = _fetch(trades, selected, limit=500, max_pages=2)
    f = capped["fetch"]
    assert f["trades_returned"] == {"call": 1000, "put": 1000}  # a ceiling cannot crowd out puts
    assert (f["truncated_batches"], f["requests"]) == (2, 4) and f["truncated_sides"] == ["call", "put"]
    assert f["truncated"] is True


def test_t5_failure_mid_pagination_keeps_pages_and_marks_the_batch_cut_short():
    trades, selected = _small((600, 600, 600), (400, 400, 400))
    out, _ = _fetch(trades, selected, limit=1000, max_pages=10, fail_on_request=2)
    f = out["fetch"]
    assert (f["failed_requests"], f["failed_batches"], f["truncated_batches"], f["requests"]) == (1, 0, 1, 4), f
    assert f["truncated_sides"] == ["call"]
    assert f["trades_returned"] == {"call": 1000, "put": 1200}


def test_t6_the_old_single_page_shape_reproduces_the_defect():
    trades, selected = _sndk_case()
    legacy, fake = _legacy_single_page(trades, selected)
    assert len(fake.calls) == 2  # 50 + 10 mixed contracts
    assert all(s[-9] == "C" for s in legacy)  # every put came back empty
    assert sum(len(v) for v in legacy.values()) == 2000  # the stored signature


# --- screener (heavy import; opens no connection) ------------------------------

def _screener():
    import services.uoa_screener as s
    return s


def _symbol_flow(s, selected, trades_map, cfg):
    """run_uoa_nightly's own arithmetic, uoa_screener.py:1538-1622, applied to a trades map."""
    tot = {"call_trades": 0, "put_trades": 0, "call_premium": 0.0, "put_premium": 0.0,
           "call_buy": 0.0, "put_buy": 0.0, "prem_day": 0.0, "prem_swing": 0.0, "prem_long": 0.0}
    for meta in selected:
        rows = trades_map.get(meta["symbol"]) or []
        if not rows:
            continue
        agg = s._aggregate_trades_for_contract(rows, bid=meta["bid"], ask=meta["ask"], config=cfg)
        prem = float(agg["premium_total"])
        side = "call" if meta["type"] == "call" else "put"
        tot[f"{side}_trades"] += int(agg["trade_count"])
        tot[f"{side}_premium"] += prem
        tot[f"{side}_buy"] += float(agg.get("buy_premium") or 0.0)
        if prem > 0:
            for b in meta["buckets"]:
                tot[f"prem_{b}"] += prem
    call_dir, put_dir = tot["call_buy"], tot["put_buy"]  # cfg.aggressor_proxy_enabled is True
    tot["dir_ratio"] = (call_dir - put_dir) / (call_dir + put_dir + 1.0)  # :1605
    return tot


def test_t7_symbol_flow_single_page_vs_paginated():
    s = _screener()
    cfg = s.UoaConfig()
    assert cfg.aggressor_proxy_enabled is True
    assert cfg.trades_limit == 10000  # PI-020 page size
    trades, selected = _sndk_case()
    legacy, _ = _legacy_single_page(trades, selected)
    paged, _ = _fetch(trades, selected)
    before = _symbol_flow(s, selected, legacy, cfg)
    after = _symbol_flow(s, selected, paged["trades"], cfg)
    # the defect, as stored on 2026-09-08
    assert (before["call_trades"], before["put_trades"], before["put_premium"]) == (2000, 0, 0.0)
    assert before["dir_ratio"] == (200000.0 - 0.0) / (200000.0 + 0.0 + 1.0)  # the stored 1.00
    assert (before["prem_day"], before["prem_swing"]) == (200000.0, 100000.0)
    # the fix
    assert (after["call_trades"], after["put_trades"]) == (15691, 11654)
    assert (after["call_buy"], after["put_buy"]) == (1569100.0, 1165400.0)
    assert after["dir_ratio"] == (1569100.0 - 1165400.0) / (1569100.0 + 1165400.0 + 1.0)
    assert 0.14 < after["dir_ratio"] < 0.15  # no longer pinned at 1.00
    assert (after["prem_day"], after["prem_swing"], after["prem_long"]) == (2734500.0, 175000.0, 0.0)


def test_t8_run_record_is_additive_and_names_what_was_cut():
    s = _screener()
    acc = s.new_trades_fetch_stats(s.UoaConfig())
    assert (acc["page_limit"], acc["split_by_type"], acc["truncated"]) == (10000, True, {})
    trades, selected = _sndk_case()
    sndk, _ = _fetch(trades, selected, limit=10000, max_pages=1)  # a ceiling hit on both sides
    s.record_trades_fetch(acc, "sndk", sndk["fetch"], 0.5)
    t2, sel2 = _small((100, 100, 100), (100, 100, 100))
    ko, _ = _fetch(t2, sel2)
    s.record_trades_fetch(acc, "KO", ko["fetch"], 0.25)
    assert (acc["symbols_fetched"], acc["symbols_truncated"], acc["fetch_seconds"]) == (2, 1, 0.75)
    assert (acc["requests"], acc["pages"]) == (4, 4)
    assert list(acc["truncated"]) == ["SNDK"]
    assert acc["truncated"]["SNDK"]["sides"] == ["call", "put"]
    assert acc["truncated"]["SNDK"]["trades_returned"] == {"call": 10000, "put": 10000}
    json.dumps(acc)  # written to uoa_runs.stats_json: must serialise


def test_t9_nothing_imported_a_database():
    assert sys.modules.get("db") is _DB_STUB
    assert "user" not in sys.modules


_CHECKS = [
    test_t1_small_symbol_one_page_per_side_no_truncation,
    test_t2_failed_first_page_is_recorded_and_the_other_side_still_reads,
    test_t3_sndk_paginated_sees_both_sides,
    test_t4_page_ceiling_is_side_balanced_and_recorded,
    test_t5_failure_mid_pagination_keeps_pages_and_marks_the_batch_cut_short,
    test_t6_the_old_single_page_shape_reproduces_the_defect,
    test_t7_symbol_flow_single_page_vs_paginated,
    test_t8_run_record_is_additive_and_names_what_was_cut,
    test_t9_nothing_imported_a_database,
]


if __name__ == "__main__":
    passed = 0
    for check in _CHECKS:
        try:
            check()
        except Exception as exc:  # noqa: BLE001 - a runner, not a library
            print(f"FAIL {check.__name__}: {exc.__class__.__name__}: {exc}")
            raise SystemExit(1)
        passed += 1
    print(f"PI-020: {passed}/{len(_CHECKS)} checks passed")
```

Arithmetic the assertions rest on, so a failure points at code, not at the test. The pre-fix batch one, sorted,
opens with call contracts of 578 prints each (14,441 = 25 × 577 + 16), so one page of 1,000 covers two call
contracts and no put; batch two opens with five calls of 250 prints each, so its page is four call contracts. That
makes 2,000 prints, all calls (T6). Every print is at the ask ($1.00 ≥ ask − 0.1 × spread), so it all counts as buy
premium. Paginated calls: 15,691 = 14,441 + 1,250, two pages of 10,000. Puts: 11,654 = 11,154 + 500, two pages.
T8's `max_pages=1` forces one 10,000-print page per side, hence the recorded ceiling on both. If a check fails, fix
the code, not the numbers.

### Acceptance criteria (what the PR must report)

1. `python tests/test_uoa_trades_pagination.py` prints `PI-020: 9/9 checks passed`, and the PR states that `pytest`
   was **not** run (PI-021).
2. §4(b) prints exactly `10000 20`.
3. §4(c): `git show --stat HEAD` lists exactly the four paths, and the `git diff --quiet` line prints `UNCHANGED`.
4. `git show HEAD -- services/uoa_screener.py` shows removals only at `:806` and `:1504-1509`; no migration file is
   added; `models.py`, `db.py`, `conftest.py`, `routers/` and `scripts/` are absent from the diff.
5. `get_option_trades` has no flag, no gate and no second code path: the only environment read added is
   `ALPACA_OPTION_TRADE_PAGES`, a page ceiling, and the method paginates at every value of it.
6. The PR body names the merge SHA and says, in one line, that from the first nightly on that SHA the UOA premium
   fields, `dir_ratio`, flow scores and SAS flow votes change for liquid names, and that no historical row is
   rewritten.

---

## 6. Rollback

One command, no data step, no flag to unset:

```
git revert --no-edit <sha> && git push
```

Rows written on nights that ran the fix stay as written; nothing rewrites them back. If a revert happens, the
Steward records the reverted interval in the DATA_NOTES entry of §8 Step 3, so the split range stays correct.

---

## 7. Out of scope — do not touch

- **Backfilling history.** Re-scoring past nights with full prints would be forced UOA re-runs (PI-017-scoped) plus
  historical Alpaca trades. That rewrites `uoa_contract_daily`, `uoa_symbol_daily` and bulletins that Q014, Q029,
  Q030 and every frozen question read. It is Haci's separate decision: it would need the exact date list and row
  counts in the register before it runs, and a repair-log row in `research/data/DATA_NOTES.md` with range and ship
  SHA (DP-50(a)). Neither the desk nor the coding agent runs it.
- **`ai_agents/omega_agent.py` and `ai_agents/option_flow_monitor.py`.** They call the fixed method and need no
  edit; do not change their call sites, their clamps or their payload handling.
- **The GEX lead.** `services/gex.py` does not call `get_option_trades`. It reads the contract list with
  `get_option_chain(limit=2000)` (`services/gex.py:422-427`, `:700-702`) and snapshots (`:476`, `:750`). The
  register's "39–50 of 2,000 contracts used" matches that **contract-list** cap, a different path. It is unverified
  whether it drops puts. The Steward checks it before any GEX finding (Q021, Q029, H-091) is trusted. Not fixed here.
- **The UOA contract-list cap.** `get_option_chain(symbol, limit=cfg.request_limit)` with `request_limit = 600`
  (`services/uoa_screener.py:798`, `:1435-1440`) stops `_list_contracts` at 600 contracts
  (`options_client.py:522-591`). Whether that list is expiry- or side-ordered on names with more than 600 contracts
  inside 180 DTE is unverified. Record it as a lead; do not change it.
- **PI-014** (polarity coverage, Conviction Monitor) and **PI-013** (morning OI overwrite of `score_swing/long`).
  They share tables and are different defects. PI-014's brief should read this one first.
- `_pct_rank` (`:870-895`), the scoring formulas (`:1793-1846`), labels, `model_version` (`:822`), the bulletin
  builder, SAS scoring and selection, `models.py`, `db.py`, `conftest.py`, every router and every script. §4(c)
  requires their diff to be empty.
- Any subscriber-visible copy, field name or ordering. The *numbers* change; the surfaces do not.

---

## 8. After deploy — the Data Steward's check at `/desk-run verify PI-020 <sha>`

**Whose step is whose.** The coding agent's work ends at §4/§5. **Haci:** merge and deploy. **Data Steward:** the
queries below, on `$RESEARCH_DB_URL` under `sas_research_ro`, counts and timestamps only, plus the DATA_NOTES entry.
No step here belongs to the coding agent (DP-49).

**Repo half (read-only on the platform repo):** at `<sha>`, run the two `git` commands of §4(c). They must reproduce
the four-path stat list and `UNCHANGED`.

**Step 1 — Haci.** Merge and deploy. Note `D0`, the first trading date whose UOA nightly ran `<sha>`.

**Before-state — from the freeze, not from a live capture.** The symbol-level before-state is the pinned parquet
`research/data/v001_uoa_symbol.parquet` (sha256 `1b959ef8…ae34ac4`), whose 2026-09-08 rows are quoted in §1: SNDK
`put_premium_total = 0`, `dir_ratio = 1.000000`; AMZN 0 / 0.999999; GOOGL 0 / 0.999991. `uoa_contract_daily` is not
frozen, but the fix rewrites no row, so §1 R1 (SNDK 2026-09-08: 60 | 2000 | >0 | 0) and R2 on pre-`D0` months are
the contract-level before-state and must be unchanged afterwards (W5).

**Step 2 — the Steward, on the first nightly after deploy (`D0`).**

```sql
-- W1. The fifteen always-capped names, first nightly on the new SHA. This is the fix, visible.
SELECT u.trading_date, u.symbol,
       u.call_premium_total, u.put_premium_total, round(u.dir_ratio::numeric, 4) AS dir_ratio,
       c.contracts, c.trades, c.call_trades, c.put_trades
FROM uoa_symbol_daily u
JOIN (
  SELECT trading_date, underlying_symbol AS symbol, count(*) AS contracts, sum(trade_count) AS trades,
         sum(CASE WHEN option_type = 'call' THEN trade_count ELSE 0 END) AS call_trades,
         sum(CASE WHEN option_type = 'put'  THEN trade_count ELSE 0 END) AS put_trades
  FROM uoa_contract_daily GROUP BY 1, 2) c USING (trading_date, symbol)
WHERE u.trading_date = DATE 'D0'
  AND u.symbol IN ('SNDK','GOOG','GOOGL','MSFT','AMZN','NFLX','ORCL','CRM','NOW','KO','WMT','BAC','BA','PFE','GLW')
ORDER BY u.symbol;

-- W2. The run telemetry block: pages, requests, ceilings, elapsed.
SELECT trading_date, status,
       (stats_json::jsonb)->'trades_fetch'->>'page_limit'         AS page_limit,
       (stats_json::jsonb)->'trades_fetch'->>'symbols_fetched'    AS fetched,
       (stats_json::jsonb)->'trades_fetch'->>'symbols_multi_page' AS multi_page,
       (stats_json::jsonb)->'trades_fetch'->>'symbols_truncated'  AS ceiling_hits,
       (stats_json::jsonb)->'trades_fetch'->>'requests'           AS requests,
       (stats_json::jsonb)->'trades_fetch'->>'pages'              AS pages,
       (stats_json::jsonb)->'trades_fetch'->>'failed_requests'    AS failed,
       (stats_json::jsonb)->'trades_fetch'->>'fetch_seconds'      AS fetch_seconds,
       (stats_json::jsonb)->'trades_fetch'->'truncated'           AS truncated_symbols,
       extract(epoch FROM finished_at - started_at)               AS run_seconds
FROM uoa_runs
WHERE run_type = 'nightly' AND trading_date >= DATE 'D0'
ORDER BY trading_date LIMIT 5;

-- W3. The dropped-side signature, by side, three weeks either side of D0: contracts the chain says
--     traded (snapshot_volume > 0) but that hold zero stored prints, on symbol-days with >= 1,000 prints.
WITH sd AS (
  SELECT trading_date, underlying_symbol FROM uoa_contract_daily
  WHERE trading_date BETWEEN DATE 'D0' - 21 AND DATE 'D0' + 21
  GROUP BY 1, 2 HAVING sum(trade_count) >= 1000)
SELECT CASE WHEN c.trading_date < DATE 'D0' THEN 'before' ELSE 'after' END AS period,
       c.option_type, count(*) AS contracts,
       sum(CASE WHEN c.snapshot_volume > 0 AND c.trade_count = 0 THEN 1 ELSE 0 END) AS traded_but_empty
FROM uoa_contract_daily c JOIN sd USING (trading_date, underlying_symbol)
GROUP BY 1, 2 ORDER BY 1, 2;

-- W4. Runtime and publication time, 10 nightlies either side of D0 (UOA runs before SAS:
--     scripts/run_nightly_pipeline.py:272-275; DATA_NOTES.md:156-165 treats finished_at as actionable).
SELECT u.trading_date,
       extract(epoch FROM u.finished_at - u.started_at)            AS uoa_seconds,
       (u.stats_json::jsonb)->'trades_fetch'->>'requests'          AS trade_requests,
       (u.stats_json::jsonb)->'trades_fetch'->>'fetch_seconds'     AS fetch_seconds,
       s.finished_at                                                AS sas_finished_at
FROM uoa_runs u
LEFT JOIN super_agent_select_runs s ON s.trading_date = u.trading_date
WHERE u.run_type = 'nightly' AND u.trading_date BETWEEN DATE 'D0' - 14 AND DATE 'D0' + 14
ORDER BY u.trading_date;

-- W5. History did not move. Re-run §1 R1 and R2 exactly as written.
--     R1 must still be 60 | 2000 | >0 | 0. R2 capped / capped_zero_put for months before D0 must still be
--     2026-01 = 1311/164, 2026-04 = 1741/165, 2026-07 = 1601/194, 2026-08 = 1483/164.

-- W6. The share of >= 1,000-print symbol-days with zero put premium, per month, through D0's month and after
--     (re-run §1 R2 and compare capped_zero_put / capped with 2026-07 = 12.1% and 2026-08 = 11.1%).
```

**PASS requires all of:**

1. **W1:** for each of the fifteen names on `D0` — `put_premium_total > 0` (it was 0 every session before),
   `dir_ratio` not within 0.001 of 1.00, and `trades > 2000` (the old ceiling was 1,000 prints per 50-contract
   batch, so 2,000 for a 60-contract name). A name that genuinely traded no puts is allowed only if W2's `truncated`
   map does not name it and its contract rows show no put with `snapshot_volume > 0`.
2. **W2:** the `trades_fetch` block is present, `page_limit = 10000`, `status = success`, `failed_requests` small,
   and `ceiling_hits` in the low single digits. If ceiling hits exceed 5 a night, or name any of the fifteen, tell
   Haci to raise `ALPACA_OPTION_TRADE_PAGES`: that is a knob, not a flag, and pagination is on either way.
3. **W3:** `after` `traded_but_empty` for puts falls to roughly the call-side level. Before, puts far exceed calls;
   report both numbers.
4. **W6:** the zero-put share among ≥ 1,000-print symbol-days drops to **≤ 2%** over the first ten sessions from `D0`.
5. **W4:** the median `sas_finished_at` shift is reported in minutes. Not a pass bar, but Haci reads it, because
   `finished_at` is the earliest actionable moment.
6. **W5 identical to §1.** Any change to a pre-`D0` month is a historical rewrite this fix does not make: FAIL —
   stop and find what wrote it.

**Step 3 — on `D0`, the Steward writes this DATA_NOTES entry** (a forward-only mechanism change, not a repair-log
row, because no historical row is rewritten):

> ## UOA option trades paginated from `D0` (PI-020, shipped `<sha>`, no flag — DP-59)
> From trading date `D0`, `uoa_contract_daily.trade_count / volume_traded / premium_total / premium_max /
> first_trade_ts / last_trade_ts / buy_premium / sell_premium / unknown_premium / top_trades_json`,
> `uoa_symbol_daily.call_premium_total / put_premium_total / total_premium / call_buy_premium / put_buy_premium /
> net_directional_premium / dir_ratio / prem_* / unusual_* / quality_* / conc_* / score_* / bias_* / label_* /
> why_json`, `uoa_bulletins.lists_json / markdown`, and every SAS flow input and output downstream
> (`flow_strength_score`, flow polarity and vote, `overall_score`, `selected_rank`) are built from every print, not
> from one 1,000-print page per 50 contracts. Nights before `D0` stay capped and were not rewritten. A question
> spanning `D0` treats these as two different features (DP-50(a)): Q014, Q019, Q029, Q030 and every prospective
> slate reader split there. Nights whose `stats_json` has no `trades_fetch` block are pre-fix.

**Step 4 — the Registrar** records the split date on Q014, Q019, Q029, Q030 and the prospective slate readers in the
board's decision log. No locked PREREG is edited (rule 3).
