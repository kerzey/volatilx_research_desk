# PI-020 — UOA option trades stop at one page: follow `next_page_token`, batch calls and puts apart, record every cut

**Type:** fix brief (platform issue, not a research finding)
**Register row:** `research/PLATFORM_ISSUES.md` PI-020, severity high, `HACI_DECIDED:fix`
**Written:** 2026-09-15 by the Brief Writer, on Haci's `/desk-run prompt PI-020` (DP-48: asking is the decision)
**Platform repo:** `C:\Users\sahin\Projects\volatilx`
**Platform SHA all `path:line` citations are taken at:** `c311e819dbe492b18ef52d137000c1d8709919db`
(`c311e81`, "SAS ladder nightly: stamp trading-day steps, not only hit dates"). The platform working tree also
holds **uncommitted EN-019 work** at that SHA (`azure_storage.py` modified; `services/report_provenance.py`,
`services/fixed_universe_batch.py`, `scripts/run_fixed_universe_report_batch.py`,
`app_data/jobs/triggered/fixed_universe_report_batch/`, `docs/FIXED_UNIVERSE_REPORT_BATCH.md`,
`tests/test_report_provenance.py` untracked). None of them is touched here; do not stage them in this commit.
**Research repo SHA:** `ffda4d9`

**Feature flags (both default OFF, read from the environment at call time — the local convention of
`services/uoa_screener.py:1460-1465` and `core/feature_flags.py:11-23`):**
- `UOA_TRADES_PAGINATION_ENABLED` — score from the paginated fetch. **Flipping it changes published numbers.**
- `UOA_TRADES_PAGINATION_SHADOW_ENABLED` — keep scoring from the single page; for symbols whose page was cut
  short, also fetch every page and write the totals to `uoa_runs.stats_json` only. Ignored when the first flag is on.

Runtime settings (not gates): `UOA_TRADES_PAGE_LIMIT` (default 10000, clamped 1000..10000),
`UOA_TRADES_MAX_PAGES_PER_BATCH` (default 10, clamped 1..50).

**Why this fix ships behind a flag (read this first).** The Brief Writer's charter gives a fix that restores
intended behaviour no flag, and says a fix that *changes a published number* goes back to Haci. This one does
both. Reading every page is what the code was meant to do, and nobody chose to drop puts. It also changes, for
the most liquid names, `uoa_symbol_daily.call_premium_total / put_premium_total / dir_ratio`, and through
cross-sectional percentiles `score_* / bias_* / label_*` for **every** symbol. Those feed the UOA bulletin lists,
the SAS flow layer (weight 24; `services/super_agent_select_scoring.py:769-790`), the flow direction vote
(`:537-560`) and the SAS candidate universe (`services/candidate_universe_builder.py:38-48`). So it changes which
picks are published. This brief therefore ships the code **dark**, and the deploy moves no published number
(§4 proves it). The flag flip is **returned to Haci** as a DP-50(b) decision, with the constraints below.

**Ship-timing check (DP-50(b)), done before writing:**
- **Deploy (both flags unset):** no historical row is rewritten, and no scoring input, published number or subscriber field
  changes. The only data change is an additive `trades_fetch` key in `uoa_runs.stats_json`. **No
  `research/data/DATA_NOTES.md` repair-log row** (`DATA_NOTES.md:32-33`: forward-only changes take none).
- **Shadow on:** no published number changes. The nightly takes longer (extra Alpaca requests for about 70
  symbols a night), and UOA runs before SAS in the pipeline (`scripts/run_nightly_pipeline.py:272-275`), so
  `super_agent_select_runs.finished_at` can move later. DATA_NOTES treats `finished_at` as the earliest actionable moment
  (`DATA_NOTES.md:156-165`). The Data Steward measures the shift (§8 V6). No DATA_NOTES row.
- **Pagination on (the flip) — Haci's decision, not taken by this brief.** It changes columns locked questions read:
  - **Q014** `uoa_persistence` (DATASET_PINNED, decision **2027-04-05**) reads `uoa_symbol.score_* / label_*` from
    manifest_v001 **and its successor freeze** through window end 2027-02-25 (`Q014 PREREG.md:44-51`, `:424-436`).
  - **Q029** `layer_value_ablation` (PREREG_LOCKED, decision **2027-04-12**) tests `flow_strength` on the
    prospective window 2026-09-15..2027-03-05 (`Q029 PREREG.md:20-32`, `:191`).
  - **Q019** `conviction_monitor_exit` (DATASET_PINNED, decision **2027-05-24**). Its polarity arm reads the
    `uoa_contract_daily` buy/sell decomposition (`services/symbol_context_builder.py:136-175`), the PI-014 link.
  - **Q030** `universe_discovery_recall` (PREREG_LOCKED, decision **2027-03-01**) rebuilds the universe from
    the bulletin lists. The flip is not one of the composition changes Q030 enumerates (`Q030 PREREG.md:653-658`),
    but it changes which symbols those lists carry. The Registrar rules on it before the flip.
  - Every locked question whose prospective window reads the published slate or `overall_score` (for example
    Q027, decision 2027-04-12; Q024, decision 2027-05-17, whose threat 8 at `Q024 PREREG.md:248` is exactly this).
    For them the flip is a publication-path ship. The latest decision date on the board is **2027-08-30** (Q015).

  The choice is the PI-011 / Q010 pattern, and PI-014 put the same choice to Haci. **Either** keep pagination
  off until the affected decision dates. **Or** flip it with a dated DATA_NOTES entry (text in §8, Step 4) and let
  each question spanning the flip split there (DP-50(a)), after a Registrar sweep. The desk does not recommend
  holding a known bias in a live signal for a year. The cost of each option is written here so the choice is made
  with it in view. A historical backfill is a third, separate decision (§7).

You are the coding agent working in the platform repo. This brief is self-contained: do not ask questions,
do not redesign, do not widen the scope. Implement §3, run §4, add §5, report the SHA.

**Nothing in this brief runs against a database.** Under DP-49 you get no DB step at all: your credential on
that Postgres is the platform's read-write role on live production. Two specific prohibitions:

- **Do not run `pytest` in this repo** (research PI-021). `conftest.py:31-35` runs `create_tables()` (DDL).
  The autouse fixture at `conftest.py:38-57` deletes every row of `UserActivityEvent` and `User` before and after
  **every test**, in whatever database `DATABASE_URL` names. Run the §5 test as
  `python tests/test_uoa_trades_pagination.py` with `DATABASE_URL` unset. It loads no conftest.
- **Do not run the UOA nightly, any `scripts/run_uoa_*.py`, `scripts/run_nightly_pipeline.py` or the app**, with
  or without flags. There is no DB-free dry run of the screener: `run_uoa_nightly` queries `uoa_bulletins` at
  `services/uoa_screener.py:1311-1316` before doing anything else.

Whose step is whose: the coding agent's work ends at §4 and §5, which are repo-only. Deploying and setting flags are **Haci's**.
The §8 queries are the **Data Steward's**, on the read-only role.

**Indentation:** `services/uoa_screener.py` is **tab-indented**. The snippets for it below are shown with tabs;
keep them tabs. `ai_agents/options_client.py`, `tests/` are 4-space indented.

---

## 1. Symptom — what is wrong, and the evidence

The UOA screener reads at most **1,000 option trades per 50-contract request** and never asks for the next
page. On liquid names a busy request holds far more than 1,000 prints. Alpaca returns the page ordered by
contract symbol, and an OCC symbol sorts by expiry, then `C` before `P`, then strike. So the page fills with the
nearest expiry's calls, and every put comes back with zero trades. The screener then stores a zero-trade row for
each such contract and builds `dir_ratio` from the truncated totals.

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

**Scale (live read-only counts, 2026-09-15, `truncation_scale.py`).** Counting rule: a symbol-day is "capped"
when `sum(uoa_contract_daily.trade_count) >= 1000`. That is a floor, because the batch split is not stored.

| month | symbol-days | capped | capped with zero put premium |
|---|---:|---:|---:|
| 2026-01 | 7,992 | 1,311 | 164 |
| 2026-04 | 10,499 | 1,741 | 165 |
| 2026-07 | 10,927 | 1,601 | 194 |
| 2026-08 | 10,461 | 1,483 | 164 |

Since 2026-06-01, **317 of 604** published SAS picks had a capped UOA row on their pick night (64 with zero put
premium). GOOG, GOOGL, MSFT, AMZN, NFLX, ORCL, CRM, NOW, KO, WMT, BAC, BA, PFE, GLW and SNDK are capped every
session. These rows predate the fix and the fix rewrites none of them, so the same query on those months must
return the same numbers at verification (§8 V1).

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
-- Expected today: 60 | 2000 | >0 | 0

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

**`services/uoa_screener.py`, the only nightly caller:**
- `:1453` `contract_symbols` come from `selected`, which `_pick_contracts` ranks by bucket, snapshot volume, OI,
  spread and ATM distance (`:1177-1189`). Calls and puts are interleaved, so each 50-contract batch mixes both.
- `:1504-1509` calls `get_option_trades(contract_symbols, start=start_iso, end=end_iso, limit=cfg.trades_limit)`,
  with `trades_limit = 1000` (`:806`). `:1510` reads `trades_map`.
- `:1520-1537` stores a zero-trade row for every contract the page did not reach (`trade_count 0`, `buy_premium 0.0`).
- `:1602-1605` builds `dir_ratio` from the truncated call and put totals. `:1609-1622` builds `prem_day/swing/long`
  from them too.

Other callers of `get_option_trades`, untouched by this brief: `ai_agents/omega_agent.py:1655-1673` (an LLM tool;
it clamps `limit` to 10,000 at `:1669`, which also shows the endpoint's page maximum) and
`ai_agents/option_flow_monitor.py:92-97` (a live 10-minute window).

---

## 3. Change

### Design choices, justified from the code

1. **A new client method, and the old one untouched.** `get_option_trades` keeps its exact body, so the omega tool
   and the flow monitor are unaffected. A diff proves it (§4(c)). The screener calls the new
   `get_option_trades_paged` on **both** flag states. With `max_pages_per_batch=1, split_by_type=False,
   page_limit=cfg.trades_limit` it sends the same requests, in the same order, with the same parameters, and
   returns the same `trades` mapping as `get_option_trades` (§5 T1, T2). The one addition is reading whether a batch came back with
   a `next_page_token`. That signal is free and tells the Data Steward how often truncation happens, with nothing
   switched on. The alternative, keeping the flag-off path on the untouched method, loses that telemetry and gives
   the shadow nothing to trigger on.
2. **Calls and puts in separate batches when paginating.** A page ceiling on a mixed batch still returns calls
   first, so any cap would keep crowding out puts. Batched apart, each side gets its own page budget, and a
   ceiling hit on the call side cannot cost the put side a single print (§5 T5). A residual bias remains inside a
   side when a ceiling is hit: later expiries and higher strikes are read last. That is recorded
   (`truncated_sides`), not hidden. Per-contract requests were rejected: 60 requests per symbol is about 30,000 a
   night. Per-(type, expiry) batches were also rejected: more requests, and a recorded ceiling already covers the case.
3. **Page size 10,000 and at most 10 pages per side-batch by default.** 10,000 is the endpoint's maximum
   (`omega_agent.py:1669`; `verify_trades.py:31` paged with it). Ten pages is 100,000 prints per side, about seven
   times SNDK's call side on 2026-09-08. Worst-case memory is 3 side-batches × 10 pages × 10,000 prints for one
   symbol, released before the next. A ceiling hit is written to `stats_json`. If the Steward sees it on names that
   matter, Haci raises `UOA_TRADES_MAX_PAGES_PER_BATCH` (up to 50) without a deploy.
4. **Stored in `uoa_runs.stats_json`, no schema change.** `stats_json` is a Text JSON column (`models.py:399`,
   `set_stats` `:413-414`), written at `services/uoa_screener.py:2006`. It is read only by the diagnostic passthrough
   `routers/uoa_screener.py:869-880` (behind login, compares nothing) and `scripts/diagnose_uoa_oi.py:92`.
   `uoa_symbol_daily.why_json` was rejected. It is served to users (`routers/uoa_screener.py:1119`), fed to SAS
   context (`services/symbol_context_builder.py:323`, `:392`) and to the MCP server
   (`fmp_mcp_server/server.py:1556`, `:1643`), so a new key there would change a served payload with the flag off.
   Nothing in `models.py` changes. No migration exists, and **none is to be written or run**.
5. **Cost.** About 1,500 capped symbol-days a month over about 21 sessions is about 70 symbols a night, out of about 500.
   Today each symbol already costs about 25–30 Alpaca requests: a contract-list page, 12 snapshot batches for 600
   contracts (`options_client.py:705-708`, `:854-858`), up to 14 contract lookups (`uoa_screener.py:1466-1467`,
   `:1627`) and 2 trade requests. On a SNDK-like name pagination adds about 2 requests (2 pages per side instead of 1
   mixed page), about +150–300 a night in total. The ceiling bounds the worst case at +2,100. 429s are already
   retried with `Retry-After` (`options_client.py:77-93`, `:102-105`). The account's per-minute limit is not
   visible from the repo, and page latency is the unknown, so both fetches record elapsed seconds.

### What changes, byte for byte

| state | contract & symbol premium columns | `unusual_*`, `score_*`, `bias_*`, `label_*`, bulletin, SAS | `uoa_runs.stats_json` |
|---|---|---|---|
| deployed, flags unset | identical | identical | + `trades_fetch` block |
| shadow on | identical | identical | + `shadow_full` entries |
| pagination on, symbol whose every legacy batch was one complete page | **identical** (same prints per contract, same order; §5 T3, T8) | **may change**: percentiles are cross-sectional over all symbols (`:1699-1705`) | + block |
| pagination on, capped symbol | **changes — the fix** | changes | + block |

"Identical" for under-cap symbols follows from the paging arithmetic. A legacy batch that returned no token held
≤ 1,000 prints, so each side-batch holds ≤ 1,000 ≤ `page_limit` prints and returns in one complete page. The claim
assumes Alpaca returns a contract's prints in the same (timestamp) order whatever the batch composition, which is
how its page tokens work. The §5 fake encodes that assumption.

### 3.1 `ai_agents/options_client.py` — new method (4 spaces)

Insert immediately **after** `get_option_trades` ends (`return {"trades": aggregated}` at `:1018`) and **before**
`def get_option_latest_quote(` at `:1020`. Do not edit `get_option_trades` or anything else in the file.

```python
    def get_option_trades_paged(
        self,
        contract_symbols: List[str],
        start: Optional[str] = None,
        end: Optional[str] = None,
        *,
        page_limit: int = 1000,
        max_pages_per_batch: int = 1,
        split_by_type: bool = False,
    ) -> Dict[str, Any]:
        """Trade prints for option contracts, following next_page_token (research PI-020).

        Alpaca orders a multi-contract /trades response by contract symbol, and an OCC symbol
        sorts by expiry, then C before P, then strike. One page for a busy batch therefore holds
        only the nearest expiry's calls; get_option_trades reads that one page and drops the token.

        max_pages_per_batch=1, split_by_type=False: exactly the requests get_option_trades sends,
        and the same "trades" mapping, plus a "fetch" block saying whether any batch was cut short.
        split_by_type=True batches calls and puts separately, so a page ceiling on one side can
        never spend the other side's budget.
        """
        fetch: Dict[str, Any] = {
            "split_by_type": bool(split_by_type),
            "page_limit": int(page_limit),
            "max_pages_per_batch": max(int(max_pages_per_batch), 1),
            "batches": 0,
            "requests": 0,
            "failed_requests": 0,
            "failed_batches": 0,
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

        if split_by_type:
            # _sanitize_contract_symbols guarantees ROOT + YYMMDD + C|P + 8-digit strike.
            groups = [
                ("call", [s for s in valid if s[-9] == "C"]),
                ("put", [s for s in valid if s[-9] == "P"]),
            ]
        else:
            groups = [("mixed", valid)]

        max_pages = fetch["max_pages_per_batch"]
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
                        "limit": page_limit,
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
                    for sym, rows in (payload.get("trades") or {}).items():
                        if isinstance(rows, list):
                            batch_trades.setdefault(sym, []).extend(rows)
                            fetch["trades_returned"]["call" if str(sym)[-9:-8] == "C" else "put"] += len(rows)
                        else:
                            batch_trades[sym] = rows
                    next_token = payload.get("next_page_token") or payload.get("nextPageToken")
                    if not next_token:
                        break
                    if pages_ok >= max_pages:
                        cut_short = True
                        break
                aggregated.update(batch_trades)
                if cut_short:
                    fetch["truncated_batches"] += 1
                    truncated_sides.add(side)
        fetch["truncated_sides"] = sorted(truncated_sides)
        return {"trades": aggregated, "fetch": fetch}
```

### 3.2 `services/uoa_screener.py` — settings, summary and run-record helpers (tabs)

Insert immediately **after** `_aggregate_trades_for_contract` ends (its `return {...}` closes at `:1271`) and
**before** `def _label_for_bucket(` at `:1274`:

```python
# --- Option-trade pagination (research PI-020) --------------------------------
# get_option_trades reads one page (limit=1000) per 50-contract batch and drops next_page_token.
# Alpaca orders a multi-contract response by OCC symbol (expiry, then C before P, then strike), so on
# busy names the page holds only near-dated calls and the puts come back empty.
_UOA_FLAG_TRUE = {"1", "true", "yes", "on"}
UOA_TRADES_PAGE_LIMIT_DEFAULT = 10000  # the endpoint's maximum page size
UOA_TRADES_MAX_PAGES_DEFAULT = 10


def _env_int_clamped(name: str, default: int, lo: int, hi: int) -> int:
	raw = os.getenv(name)
	try:
		value = int(str(raw).strip()) if raw is not None and str(raw).strip() else int(default)
	except Exception:
		value = int(default)
	return max(int(lo), min(int(hi), value))


def uoa_trades_fetch_settings() -> Dict[str, Any]:
	"""PI-020 runtime settings, read from the environment at call time. Pure: no DB, no I/O.

	UOA_TRADES_PAGINATION_ENABLED (default off): score from the paginated fetch.
	UOA_TRADES_PAGINATION_SHADOW_ENABLED (default off; ignored when pagination is on): score from
	the single page as before; for symbols whose page was cut short, also fetch every page and
	record the totals in uoa_runs.stats_json only.
	"""
	paginate = str(os.getenv("UOA_TRADES_PAGINATION_ENABLED", "")).strip().lower() in _UOA_FLAG_TRUE
	shadow = str(os.getenv("UOA_TRADES_PAGINATION_SHADOW_ENABLED", "")).strip().lower() in _UOA_FLAG_TRUE
	return {
		"mode": "paginated" if paginate else "single_page",
		"shadow_enabled": bool(shadow and not paginate),
		"page_limit": _env_int_clamped("UOA_TRADES_PAGE_LIMIT", UOA_TRADES_PAGE_LIMIT_DEFAULT, 1000, 10000),
		"max_pages_per_batch": _env_int_clamped("UOA_TRADES_MAX_PAGES_PER_BATCH", UOA_TRADES_MAX_PAGES_DEFAULT, 1, 50),
	}


def summarize_symbol_flow(
	selected: Sequence[Mapping[str, Any]],
	trades_map: Mapping[str, Any],
	config: UoaConfig,
) -> Dict[str, Any]:
	"""Symbol-level totals from a trades map, with run_uoa_nightly's own arithmetic.

	Same order and formulas as the per-contract loop, dir_ratio and prem_* blocks of
	run_uoa_nightly. Used only for the PI-020 shadow record; scoring never calls it.
	Pure: no DB, no I/O.
	"""
	call_trades = 0
	put_trades = 0
	call_premium = 0.0
	put_premium = 0.0
	call_buy = 0.0
	put_buy = 0.0
	prem_day = 0.0
	prem_swing = 0.0
	prem_long = 0.0
	for meta in selected:
		rows = trades_map.get(meta.get("symbol")) or []
		if not isinstance(rows, list) or not rows:
			continue
		agg = _aggregate_trades_for_contract(rows, bid=meta.get("bid"), ask=meta.get("ask"), config=config)
		prem = float(agg["premium_total"])
		if meta.get("type") == "call":
			call_trades += int(agg["trade_count"])
			call_premium += prem
			if config.aggressor_proxy_enabled:
				call_buy += float(agg.get("buy_premium") or 0.0)
		elif meta.get("type") == "put":
			put_trades += int(agg["trade_count"])
			put_premium += prem
			if config.aggressor_proxy_enabled:
				put_buy += float(agg.get("buy_premium") or 0.0)
		if prem > 0:
			buckets = meta.get("buckets") or []
			if "day" in buckets:
				prem_day += prem
			if "swing" in buckets:
				prem_swing += prem
			if "long" in buckets:
				prem_long += prem
	call_dir = call_buy if config.aggressor_proxy_enabled else call_premium
	put_dir = put_buy if config.aggressor_proxy_enabled else put_premium
	return {
		"call_trades": call_trades,
		"put_trades": put_trades,
		"call_premium": call_premium,
		"put_premium": put_premium,
		"call_buy_premium": call_buy if config.aggressor_proxy_enabled else None,
		"put_buy_premium": put_buy if config.aggressor_proxy_enabled else None,
		"dir_ratio": (call_dir - put_dir) / (call_dir + put_dir + 1.0),
		"prem_day": prem_day,
		"prem_swing": prem_swing,
		"prem_long": prem_long,
	}


def new_trades_fetch_stats(settings: Mapping[str, Any], config: UoaConfig) -> Dict[str, Any]:
	"""The uoa_runs.stats_json["trades_fetch"] block for one run. Pure."""
	paginated = settings.get("mode") == "paginated"
	shadow = bool(settings.get("shadow_enabled"))
	return {
		"mode": "paginated" if paginated else "single_page",
		"shadow_enabled": shadow,
		"page_limit": int(settings["page_limit"]) if paginated else int(config.trades_limit),
		"max_pages_per_batch": int(settings["max_pages_per_batch"]) if paginated else 1,
		"split_by_type": paginated,
		"symbols_fetched": 0,
		"symbols_multi_page": 0,
		"symbols_truncated": 0,
		"requests": 0,
		"failed_requests": 0,
		"fetch_seconds": 0.0,
		"truncated": {},
		"shadow_page_limit": int(settings["page_limit"]) if shadow else None,
		"shadow_max_pages_per_batch": int(settings["max_pages_per_batch"]) if shadow else None,
		"shadow_symbols": 0,
		"shadow_requests": 0,
		"shadow_truncated": 0,
		"shadow_errors": 0,
		"shadow_seconds": 0.0,
		"shadow_full": {},
	}


def record_trades_fetch(acc: Dict[str, Any], symbol: str, fetch_meta: Any, seconds: float) -> None:
	"""Fold one symbol's scoring fetch into the run block. A symbol is named only when cut short."""
	meta = fetch_meta if isinstance(fetch_meta, Mapping) else {}
	requests = int(meta.get("requests") or 0)
	batches = int(meta.get("batches") or 0)
	truncated_batches = int(meta.get("truncated_batches") or 0)
	acc["symbols_fetched"] += 1
	acc["requests"] += requests
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
			"trades_returned": dict(meta.get("trades_returned") or {}),
		}


def record_trades_shadow(
	acc: Dict[str, Any],
	symbol: str,
	shadow_payload: Any,
	selected: Sequence[Mapping[str, Any]],
	config: UoaConfig,
	seconds: float,
) -> None:
	"""Record what the fully paginated fetch would have given. Never read by scoring."""
	payload = shadow_payload if isinstance(shadow_payload, Mapping) else {}
	meta = payload.get("fetch") if isinstance(payload.get("fetch"), Mapping) else {}
	summary = summarize_symbol_flow(selected, payload.get("trades") or {}, config)
	acc["shadow_symbols"] += 1
	acc["shadow_requests"] += int(meta.get("requests") or 0)
	acc["shadow_seconds"] = round(float(acc["shadow_seconds"]) + float(seconds or 0.0), 3)
	if int(meta.get("truncated_batches") or 0) > 0:
		acc["shadow_truncated"] += 1
	summary.update(
		{
			"requests": int(meta.get("requests") or 0),
			"truncated_batches": int(meta.get("truncated_batches") or 0),
			"truncated_sides": list(meta.get("truncated_sides") or []),
			"failed_requests": int(meta.get("failed_requests") or 0),
		}
	)
	acc["shadow_full"][str(symbol).upper()] = summary
```

Add the five public names to `__all__` at `services/uoa_screener.py:2457-2465`, after
`"backfill_uoa_outcomes_range",`: `"uoa_trades_fetch_settings"`, `"summarize_symbol_flow"`,
`"new_trades_fetch_stats"`, `"record_trades_fetch"`, `"record_trades_shadow"`.

### 3.3 `services/uoa_screener.py` — initialise the run block

Insert immediately **after** `stats["force_deleted"] = deleted` at `:1423` and before `for symbol in universe_syms:` at `:1425`:

```python
	# PI-020: how option trades are fetched tonight, and every place a fetch was cut short.
	trades_fetch_settings = uoa_trades_fetch_settings()
	trades_fetch_stats = new_trades_fetch_stats(trades_fetch_settings, cfg)
	stats["trades_fetch"] = trades_fetch_stats
```

`stats` is serialised once at `:2006` (`run.set_stats(stats)`) and again at `:2014` and `:2034`; the block rides along.

### 3.4 `services/uoa_screener.py` — replace the fetch at `:1504-1509`

Replace exactly the six lines `trades_payload = options_client.get_option_trades(` … `)` at `:1504-1509`. Keep
`:1510` (`trades_map = trades_payload.get("trades", {}) if isinstance(trades_payload, dict) else {}`) **unchanged**,
and put the new lines after it as shown:

```python
		# PI-020: option trades. Flag off sends exactly the pre-PI-020 requests (one page per
		# 50-contract batch, limit=cfg.trades_limit) and only reads whether a page was cut short.
		# Flag on follows next_page_token, with calls and puts batched apart.
		trades_fetch_t0 = datetime.now(timezone.utc)
		if trades_fetch_settings["mode"] == "paginated":
			trades_payload = options_client.get_option_trades_paged(
				contract_symbols,
				start=start_iso,
				end=end_iso,
				page_limit=int(trades_fetch_settings["page_limit"]),
				max_pages_per_batch=int(trades_fetch_settings["max_pages_per_batch"]),
				split_by_type=True,
			)
		else:
			trades_payload = options_client.get_option_trades_paged(
				contract_symbols,
				start=start_iso,
				end=end_iso,
				page_limit=cfg.trades_limit,
				max_pages_per_batch=1,
				split_by_type=False,
			)
		trades_map = trades_payload.get("trades", {}) if isinstance(trades_payload, dict) else {}
		trades_fetch_meta = trades_payload.get("fetch", {}) if isinstance(trades_payload, dict) else {}
		record_trades_fetch(
			trades_fetch_stats,
			symbol,
			trades_fetch_meta,
			(datetime.now(timezone.utc) - trades_fetch_t0).total_seconds(),
		)
		if trades_fetch_settings["shadow_enabled"] and int(trades_fetch_meta.get("truncated_batches") or 0) > 0:
			# Shadow only: everything below reads trades_map, never shadow_payload.
			shadow_t0 = datetime.now(timezone.utc)
			try:
				shadow_payload = options_client.get_option_trades_paged(
					contract_symbols,
					start=start_iso,
					end=end_iso,
					page_limit=int(trades_fetch_settings["page_limit"]),
					max_pages_per_batch=int(trades_fetch_settings["max_pages_per_batch"]),
					split_by_type=True,
				)
				record_trades_shadow(
					trades_fetch_stats,
					symbol,
					shadow_payload,
					selected,
					cfg,
					(datetime.now(timezone.utc) - shadow_t0).total_seconds(),
				)
			except Exception:
				trades_fetch_stats["shadow_errors"] += 1
				logger.exception("PI-020 shadow trades fetch failed symbol=%s", symbol)
```

`datetime` and `timezone` are already imported at `:9` and used this way at `:1302`. Note that `time` at `:9` is
`datetime.time`, not the `time` module; do not add `import time`. Nothing from `:1511` onward changes. The
per-contract loop, `dir_ratio`, `prem_*`, percentiles, scores, labels and bulletin code are exactly as at `c311e81`.

### 3.5 Docs — `docs/UOA_SCREENER_MVP.md`

Replace `§2.3` at `docs/UOA_SCREENER_MVP.md:107-115` (from `### 2.3 Trades (intraday prints)` through
`MVP design assumes you compute UOA primarily from these trade rows.`) with:

```markdown
### 2.3 Trades (intraday prints)
Method: `AlpacaOptionsClient.get_option_trades_paged(contract_symbols, start=..., end=..., page_limit=..., max_pages_per_batch=..., split_by_type=...)`
(the nightly screener; `get_option_trades` is the older single-page method, still used by the omega tool and the flow monitor)
- Under the hood: `/v1beta1/options/trades`, up to 50 contracts per request
- For each contract: list of trade rows; the code expects:
  - `p` or `price`
  - `s` or `size`
  - `t` or `timestamp`

**Pagination (PI-020).** Alpaca orders a multi-contract response by OCC symbol (expiry, then C before P, then strike).
One page of 1,000 prints on a busy name therefore holds only near-dated calls, and puts come back empty. Two
flags, both default off: `UOA_TRADES_PAGINATION_ENABLED` makes the nightly follow `next_page_token`, with calls and
puts in separate batches, up to `UOA_TRADES_MAX_PAGES_PER_BATCH` (10) pages of `UOA_TRADES_PAGE_LIMIT` (10,000)
prints per batch. `UOA_TRADES_PAGINATION_SHADOW_ENABLED` keeps scoring from the single page and, for symbols whose
page was cut short, records the fully paginated totals. Every run writes `uoa_runs.stats_json.trades_fetch`: mode,
requests, elapsed seconds, and every symbol whose fetch was cut short, by side (`truncated`). Shadow runs also write
`shadow_full`. Turning pagination on changes flow premiums, `dir_ratio` and the cross-sectional scores; the flip date is logged.

MVP design assumes you compute UOA primarily from these trade rows.
```

That is the whole change: `ai_agents/options_client.py`, `services/uoa_screener.py`, `docs/UOA_SCREENER_MVP.md`,
and a new `tests/test_uoa_trades_pagination.py`. Nothing else.

---

## 4. Before / after check — repository only, no database, no network

`DATABASE_URL` must be unset in the shell for every command
(PowerShell: `Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue`; Git Bash: `unset DATABASE_URL`).
None of these commands opens a connection. `ai_agents/options_client.py` imports only the standard library,
`requests` and `core.datetime_utils` (`:1-10`), and `ai_agents/__init__.py` imports nothing. `services/uoa_screener.py`
imports `models` (`:22-30`), and `models.py:1-7` imports only SQLAlchemy symbols. No module in that chain imports
`db.py`; `user.py:7` is the one that does, and nothing here imports `user`. Importing the screener pulls
`indicator_fetcher` → `symbol_map`, which may try the Alpaca asset catalogue and fall back offline. That is slow,
not a DB call.

The fixed trading date for every check is **2026-09-08** (SNDK, the traced night), built as the §5 fixture.

**(a) The test file — this is what changes.**

```
python tests/test_uoa_trades_pagination.py
```

Before: the file does not exist. After: exactly `PI-020: 10/10 checks passed`.

**(b) Flags default off, settings as specified.**

```
python -c "import os; [os.environ.pop(k, None) for k in ('DATABASE_URL','UOA_TRADES_PAGINATION_ENABLED','UOA_TRADES_PAGINATION_SHADOW_ENABLED','UOA_TRADES_PAGE_LIMIT','UOA_TRADES_MAX_PAGES_PER_BATCH')]; from services.uoa_screener import uoa_trades_fetch_settings as s, UoaConfig; print(s()); print(UoaConfig().trades_limit)"
```

Before: `ImportError: cannot import name 'uoa_trades_fetch_settings'`. After, exactly:
`{'mode': 'single_page', 'shadow_enabled': False, 'page_limit': 10000, 'max_pages_per_batch': 10}` then `1000`.

**(c) The old method and every other file are untouched — proved by diff, not by running anything.**

Commit PI-020 as **one commit** containing only the four paths in §3. Then:

```
git show --stat HEAD
git show --numstat HEAD -- ai_agents/options_client.py
git show --numstat HEAD -- services/uoa_screener.py
git diff --quiet HEAD~1 HEAD -- services/super_agent_select_scoring.py services/super_agent_select_service.py services/symbol_context_builder.py services/candidate_universe_builder.py services/uoa_scheduler.py services/gex.py scripts/run_nightly_pipeline.py scripts/run_uoa_oi_gex_for_day.py scripts/run_uoa_nightly.py scripts/run_uoa_range.py ai_agents/omega_agent.py ai_agents/option_flow_monitor.py routers models.py db.py conftest.py core fmp_mcp_server && echo UNCHANGED
```

- `git show --stat HEAD` lists exactly `ai_agents/options_client.py`, `services/uoa_screener.py`,
  `docs/UOA_SCREENER_MVP.md`, `tests/test_uoa_trades_pagination.py`.
- `numstat` for `ai_agents/options_client.py` shows **0 deleted lines**. The file only gains the new method, so
  `get_option_trades` is byte-identical.
- `numstat` for `services/uoa_screener.py` shows **at most 6 deleted lines**, and `git show HEAD -- services/uoa_screener.py`
  shows every removed line coming from the old `options_client.get_option_trades(` call at `:1504-1509`.
- The `git diff --quiet` line prints `UNCHANGED`.

With (a) T1–T3 this is the complete inertness argument. With the flags unset, the screener sends Alpaca the same
requests as at `c311e81` and builds the same `trades_map`, and nothing that turns `trades_map` into rows,
percentiles, scores, labels or bulletins changed. Do not try to demonstrate it by running the screener.

**(d) What must not differ, stated for the PR.** With flags unset: every `uoa_contract_daily`, `uoa_symbol_daily`
and `uoa_bulletins` value, and every SAS input. What differs: `uoa_runs.stats_json` gains `trades_fetch`.

---

## 5. Test — `tests/test_uoa_trades_pagination.py`

A standalone runner, the EN-019 pattern. It uses no pytest fixtures, no conftest and no database. The network seam
is `AlpacaOptionsClient._request`, replaced on the instance by an in-memory fake that honours `symbols`, `limit`
and `page_token` with Alpaca's ordering. **Fixture provenance:** the SNDK fixture reproduces the desk's measured
totals for 2026-09-08 (`research/reports/case_SNDK_2026-09-15/verify_trades.py`): 14,441 call and 11,154 put
prints on the first 50 contracts, 60 contracts in all, stored as 2,000 prints, all calls. The split across
contracts and the prices are synthetic. Every print is $1.00 × 1 contract, a $100 premium. Alpaca prints are not
frozen, and the desk does not ship market data into the platform repo. Which line would have caught the bug: T4
(a paginated fetch returns both sides) and T8 (`put_trades == 0` on the single page).

```python
"""PI-020: UOA option trades must not stop at one page.

get_option_trades sends one /trades request per 50-contract batch with limit=1000 and never reads
next_page_token. Alpaca orders a multi-contract response by contract symbol, and an OCC symbol sorts
expiry -> C before P -> strike, so a busy batch returns only the nearest expiry's calls. SNDK
2026-09-08: stored 2,000 trades, all calls, dir_ratio 1.00; paginated, 14,441 call and 11,154 put
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
_DB_STUB = types.ModuleType("db")
sys.modules.setdefault("db", _DB_STUB)  # any `from db import ...` raises ImportError

_FLAG_KEYS = (
    "UOA_TRADES_PAGINATION_ENABLED",
    "UOA_TRADES_PAGINATION_SHADOW_ENABLED",
    "UOA_TRADES_PAGE_LIMIT",
    "UOA_TRADES_MAX_PAGES_PER_BATCH",
)
for _k in _FLAG_KEYS:
    os.environ.pop(_k, None)

from ai_agents.options_client import AlpacaOptionsClient  # noqa: E402

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
    """60 contracts in the screener's mixed order -> legacy batches of 50 + 10, both capped.

    First 50 (exp 2026-09-11, DTE 3): 14,441 call and 11,154 put prints (the desk's paginated totals).
    Last 10 (exp 2026-09-18, DTE 10): 1,250 call and 500 put prints, enough to cap batch two as well.
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


def _legacy(trades, selected, fail_on_request=None):
    fake = _FakeAlpacaTrades(trades, fail_on_request)
    return _client(fake).get_option_trades(_syms(selected), start=START, end=END, limit=1000), fake


def _paged(trades, selected, page_limit, max_pages, split, fail_on_request=None):
    fake = _FakeAlpacaTrades(trades, fail_on_request)
    out = _client(fake).get_option_trades_paged(
        _syms(selected), start=START, end=END,
        page_limit=page_limit, max_pages_per_batch=max_pages, split_by_type=split,
    )
    return out, fake


# --- client -------------------------------------------------------------------

def test_t1_flag_off_sends_the_legacy_requests_and_returns_the_legacy_map():
    trades, selected = _sndk_case()
    legacy, legacy_fake = _legacy(trades, selected)
    new, new_fake = _paged(trades, selected, 1000, 1, False)
    assert new_fake.calls == legacy_fake.calls
    assert len(legacy_fake.calls) == 2
    assert new["trades"] == legacy["trades"]
    f = new["fetch"]
    assert (f["batches"], f["requests"], f["truncated_batches"]) == (2, 2, 2), f
    assert f["truncated_sides"] == ["mixed"]
    assert f["trades_returned"] == {"call": 2000, "put": 0}  # the stored signature: 2,000 prints, no puts


def test_t2_flag_off_failed_request_matches_legacy():
    trades, selected = _small((100, 100, 100), (100, 100, 100))
    legacy, legacy_fake = _legacy(trades, selected, fail_on_request=1)
    new, new_fake = _paged(trades, selected, 1000, 1, False, fail_on_request=1)
    assert new_fake.calls == legacy_fake.calls
    assert new["trades"] == legacy["trades"] == {}
    f = new["fetch"]
    assert (f["failed_requests"], f["failed_batches"], f["truncated_batches"]) == (1, 1, 0), f


def test_t3_under_the_cap_pagination_returns_the_same_prints():
    trades, selected = _small((100, 120, 90), (80, 60, 110))
    legacy, _ = _legacy(trades, selected)
    paged, _ = _paged(trades, selected, 10000, 10, True)
    assert paged["trades"] == legacy["trades"]
    assert paged["fetch"]["truncated_batches"] == 0 and paged["fetch"]["requests"] == 2


def test_t4_sndk_paginated_sees_both_sides():
    trades, selected = _sndk_case()
    out, fake = _paged(trades, selected, 10000, 10, True)
    f = out["fetch"]
    assert (f["batches"], f["requests"], f["truncated_batches"], f["failed_requests"]) == (2, 4, 0, 0), f
    assert f["trades_returned"] == {"call": 15691, "put": 11654}
    assert out["trades"] == trades  # every print of every contract, in order, including a contract split across pages
    for _path, params in fake.calls:
        assert len({s[-9] for s in dict(params)["symbols"].split(",")}) == 1  # one side per request


def test_t5_page_ceiling_is_side_balanced_and_recorded():
    trades, selected = _small((600, 600, 600), (400, 400, 400))
    one_page, _ = _paged(trades, selected, 1000, 1, False)
    assert one_page["fetch"]["trades_returned"] == {"call": 1000, "put": 0}  # the defect
    capped, _ = _paged(trades, selected, 500, 2, True)
    f = capped["fetch"]
    assert f["trades_returned"] == {"call": 1000, "put": 1000}  # a ceiling cannot crowd out puts
    assert (f["truncated_batches"], f["requests"]) == (2, 4) and f["truncated_sides"] == ["call", "put"]


def test_t6_failure_mid_pagination_keeps_pages_and_marks_the_batch_cut_short():
    trades, selected = _small((600, 600, 600), (400, 400, 400))
    out, _ = _paged(trades, selected, 1000, 10, True, fail_on_request=2)
    f = out["fetch"]
    assert (f["failed_requests"], f["failed_batches"], f["truncated_batches"], f["requests"]) == (1, 0, 1, 4), f
    assert f["truncated_sides"] == ["call"]
    assert f["trades_returned"] == {"call": 1000, "put": 1200}


# --- screener helpers (heavy import; opens no connection) ----------------------

def _screener():
    import services.uoa_screener as s
    return s


def test_t7_flags_default_off_and_settings_clamped():
    s = _screener()
    saved = {k: os.environ.pop(k, None) for k in _FLAG_KEYS}
    try:
        assert s.uoa_trades_fetch_settings() == {
            "mode": "single_page", "shadow_enabled": False, "page_limit": 10000, "max_pages_per_batch": 10,
        }
        assert s.UoaConfig().trades_limit == 1000
        os.environ["UOA_TRADES_PAGINATION_SHADOW_ENABLED"] = "1"
        assert s.uoa_trades_fetch_settings()["shadow_enabled"] is True
        os.environ["UOA_TRADES_PAGINATION_ENABLED"] = "true"
        got = s.uoa_trades_fetch_settings()
        assert got["mode"] == "paginated" and got["shadow_enabled"] is False
        for raw, want in (("50", 1000), ("99999", 10000), ("abc", 10000), ("", 10000), ("2500", 2500)):
            os.environ["UOA_TRADES_PAGE_LIMIT"] = raw
            assert s.uoa_trades_fetch_settings()["page_limit"] == want, raw
        for raw, want in (("0", 1), ("500", 50), ("x", 10), ("3", 3)):
            os.environ["UOA_TRADES_MAX_PAGES_PER_BATCH"] = raw
            assert s.uoa_trades_fetch_settings()["max_pages_per_batch"] == want, raw
    finally:
        for k in _FLAG_KEYS:
            os.environ.pop(k, None)
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


def test_t8_symbol_flow_single_page_vs_paginated():
    s = _screener()
    cfg = s.UoaConfig()
    assert cfg.aggressor_proxy_enabled is True
    trades, selected = _sndk_case()
    legacy, _ = _legacy(trades, selected)
    paged, _ = _paged(trades, selected, 10000, 10, True)
    before = s.summarize_symbol_flow(selected, legacy["trades"], cfg)
    after = s.summarize_symbol_flow(selected, paged["trades"], cfg)
    assert (before["call_trades"], before["put_trades"], before["put_premium"]) == (2000, 0, 0.0)
    assert before["dir_ratio"] == (200000.0 - 0.0) / (200000.0 + 0.0 + 1.0)  # the stored 1.00
    assert (before["prem_day"], before["prem_swing"]) == (200000.0, 100000.0)
    assert (after["call_trades"], after["put_trades"]) == (15691, 11654)
    assert (after["call_buy_premium"], after["put_buy_premium"]) == (1569100.0, 1165400.0)
    assert after["dir_ratio"] == (1569100.0 - 1165400.0) / (1569100.0 + 1165400.0 + 1.0)
    assert (after["prem_day"], after["prem_swing"], after["prem_long"]) == (2734500.0, 175000.0, 0.0)
    t2, sel2 = _small((100, 120, 90), (80, 60, 110))
    legacy2, _ = _legacy(t2, sel2)
    paged2, _ = _paged(t2, sel2, 10000, 10, True)
    assert s.summarize_symbol_flow(sel2, legacy2["trades"], cfg) == s.summarize_symbol_flow(sel2, paged2["trades"], cfg)


def test_t9_run_record_is_additive_and_names_what_was_cut():
    s = _screener()
    cfg = s.UoaConfig()
    acc = s.new_trades_fetch_stats(
        {"mode": "single_page", "shadow_enabled": True, "page_limit": 10000, "max_pages_per_batch": 10}, cfg
    )
    assert (acc["mode"], acc["page_limit"], acc["max_pages_per_batch"], acc["split_by_type"]) == ("single_page", 1000, 1, False)
    assert (acc["shadow_page_limit"], acc["shadow_max_pages_per_batch"]) == (10000, 10)
    trades, selected = _sndk_case()
    one_page, _ = _paged(trades, selected, 1000, 1, False)
    s.record_trades_fetch(acc, "sndk", one_page["fetch"], 0.5)
    t2, sel2 = _small((100, 100, 100), (100, 100, 100))
    ko, _ = _paged(t2, sel2, 1000, 1, False)
    s.record_trades_fetch(acc, "KO", ko["fetch"], 0.25)
    assert (acc["symbols_fetched"], acc["symbols_truncated"], acc["requests"], acc["fetch_seconds"]) == (2, 1, 3, 0.75)
    assert list(acc["truncated"]) == ["SNDK"]
    assert acc["truncated"]["SNDK"]["sides"] == ["mixed"]
    assert acc["truncated"]["SNDK"]["trades_returned"] == {"call": 2000, "put": 0}
    full, _ = _paged(trades, selected, 10000, 10, True)
    s.record_trades_shadow(acc, "SNDK", full, selected, cfg, 1.0)
    rec = acc["shadow_full"]["SNDK"]
    assert (acc["shadow_symbols"], acc["shadow_requests"], acc["shadow_truncated"]) == (1, 4, 0)
    assert (rec["call_trades"], rec["put_trades"], rec["truncated_sides"]) == (15691, 11654, [])
    json.dumps(acc)  # written to uoa_runs.stats_json: must serialise


def test_t10_nothing_imported_a_database():
    assert sys.modules.get("db") is _DB_STUB
    assert "user" not in sys.modules


_CHECKS = [
    test_t1_flag_off_sends_the_legacy_requests_and_returns_the_legacy_map,
    test_t2_flag_off_failed_request_matches_legacy,
    test_t3_under_the_cap_pagination_returns_the_same_prints,
    test_t4_sndk_paginated_sees_both_sides,
    test_t5_page_ceiling_is_side_balanced_and_recorded,
    test_t6_failure_mid_pagination_keeps_pages_and_marks_the_batch_cut_short,
    test_t7_flags_default_off_and_settings_clamped,
    test_t8_symbol_flow_single_page_vs_paginated,
    test_t9_run_record_is_additive_and_names_what_was_cut,
    test_t10_nothing_imported_a_database,
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

Arithmetic the assertions rest on, so a failure points at code, not at the test. The legacy batch one, sorted,
opens with call contracts of 578 prints each (14,441 = 25 × 577 + 16), so one page of 1,000 covers two call
contracts and no put. Batch two opens with five calls of 250 prints each, so its page is four call contracts. That
makes 2,000 prints, all calls. Every print is at the ask ($1.00 ≥ ask − 0.1 × spread), so it all counts as buy
premium. Paginated calls: 15,691 = 14,441 + 1,250, on 2 pages. Puts: 11,654 = 11,154 + 500, on 2 pages. If a
check fails, fix the code, not the numbers.

### Acceptance (what the PR must report)

1. §4(a): `PI-020: 10/10 checks passed`, and a statement that `pytest` was not run.
2. §4(b): the two exact output lines.
3. §4(c): the four-path stat list, `0` deletions for `ai_agents/options_client.py`, ≤ 6 deletions for
   `services/uoa_screener.py` (all from the old call), and `UNCHANGED`.
4. No file under `models.py`, `db.py`, `conftest.py`, `routers/`, `scripts/` or any SAS service in the diff; no
   migration script added.
5. The platform SHA of the merge.

---

## 6. Rollback

**Behaviour:** unset `UOA_TRADES_PAGINATION_ENABLED` and `UOA_TRADES_PAGINATION_SHADOW_ENABLED` in the application
settings the nightly reads. They are read at call time. **Code:**

```
git revert --no-edit <sha> && git push
```

One commit, four files, no schema, no data step. Rows written on nights when pagination was on stay as written.
Nothing rewrites them back, and the DATA_NOTES entry (§8 Step 4) records the interval.

---

## 7. Out of scope — do not touch

- **Backfilling history.** Re-scoring past nights with full prints would be forced UOA re-runs (PI-017-scoped) plus
  historical Alpaca trades. That rewrites `uoa_contract_daily`, `uoa_symbol_daily` and bulletins that Q014, Q029,
  Q030 and every frozen question read. It is Haci's separate decision. It would need the exact date list and row
  counts in the register before it runs, and a repair-log row in `research/data/DATA_NOTES.md` with range and ship
  SHA (DP-50(a)). Neither the desk nor the coding agent runs it.
- **The other `get_option_trades` callers**, `ai_agents/omega_agent.py:1655-1673` and
  `ai_agents/option_flow_monitor.py:92-97`. They keep the single-page method. Whether they need pagination is not
  part of PI-020.
- **The GEX lead.** `services/gex.py` does not call `get_option_trades`. It reads the contract list with
  `get_option_chain(limit=2000)` (`services/gex.py:422-427`, `:700-702`) and snapshots (`:476`, `:750`). The
  register's "39–50 of 2,000 contracts used" matches that **contract-list** cap, a different path. It is unverified
  whether it drops puts. The Steward checks it before any GEX finding (Q021, Q029, H-091) is trusted. Not fixed here.
- **The UOA contract-list cap.** `get_option_chain(symbol, limit=cfg.request_limit)` with `request_limit = 600`
  (`services/uoa_screener.py:798`, `:1435-1440`) stops `_list_contracts` at 600 contracts (`options_client.py:522-591`).
  Whether that list is expiry- or side-ordered on names with more than 600 contracts inside 180 DTE is unverified.
  Record it as a lead; do not change it.
- **PI-014** (polarity coverage, Conviction Monitor) and **PI-013** (morning OI overwrite of `score_swing/long`).
  They share tables and are different defects. PI-014's brief should read this one first.
- `UoaConfig.trades_limit` (`:806`), `_pct_rank` (`:870-895`), the scoring formulas (`:1793-1846`), labels,
  `model_version` (`:822`), the bulletin builder, SAS scoring and selection, `models.py`, `db.py`, `conftest.py`,
  every router and every script. §4(c) requires their diff to be empty.
- Any subscriber-visible copy, field, ordering or number. With the flags unset there is none.

---

## 8. Verification at `/desk-run verify PI-020 <sha>`

**Whose step is whose.** The coding agent's work ends at §4/§5. **Haci:** merge, deploy, set flags, and later the
flip decision. **Data Steward:** the queries below, on `$RESEARCH_DB_URL` under `sas_research_ro`, counts and
timestamps only, no outcome column. **Registrar:** the in-flight sweep before any flip.

**Repo half (Steward, read-only on the platform repo):** at `<sha>`, run the three `git` commands of §4(c). They
must reproduce the four-path list, 0 deletions in `ai_agents/options_client.py`, and `UNCHANGED`. Record the output.

**Step 1 — Haci.** Merge and deploy with both flags **unset**. Note `D0`, the first trading date whose nightly ran `<sha>`.

**Before-state.** The symbol-level before-state is the pinned freeze
`research/data/v001_uoa_symbol.parquet` (sha256 `1b959ef8…ae34ac4`, §1 tables). `uoa_contract_daily` is not
frozen, but the fix rewrites no row, so §1 R1/R2 on pre-`D0` dates are stable and are the contract-level before-state.

```sql
-- V1. History did not move. Must match §1 exactly: R1 = 60 | 2000 | >0 | 0; R2 capped / capped_zero_put for
--     2026-01 = 1311/164, 2026-04 = 1741/165, 2026-07 = 1601/194, 2026-08 = 1483/164.
--     (re-run §1 R1 and R2 as written)

-- V2. The run block exists and the flags read as deployed (first 5 nightlies from D0).
SELECT trading_date, status,
       (stats_json::jsonb)->'trades_fetch'->>'mode'               AS mode,
       (stats_json::jsonb)->'trades_fetch'->>'shadow_enabled'     AS shadow,
       (stats_json::jsonb)->'trades_fetch'->>'page_limit'         AS page_limit,
       (stats_json::jsonb)->'trades_fetch'->>'symbols_fetched'    AS fetched,
       (stats_json::jsonb)->'trades_fetch'->>'symbols_truncated'  AS truncated,
       (stats_json::jsonb)->'trades_fetch'->>'requests'           AS requests,
       (stats_json::jsonb)->'trades_fetch'->>'fetch_seconds'      AS fetch_seconds,
       extract(epoch FROM finished_at - started_at)               AS run_seconds
FROM uoa_runs
WHERE run_type = 'nightly' AND trading_date >= DATE 'D0'
ORDER BY trading_date LIMIT 5;

-- V3. On single-page nights every symbol the run names as cut short really hit a 1,000-print page.
WITH r AS (
  SELECT trading_date, jsonb_object_keys((stats_json::jsonb)->'trades_fetch'->'truncated') AS sym
  FROM uoa_runs
  WHERE run_type = 'nightly' AND trading_date >= DATE 'D0'
    AND (stats_json::jsonb)->'trades_fetch'->>'mode' = 'single_page'),
c AS (
  SELECT trading_date, underlying_symbol AS sym, sum(trade_count) AS trades,
         sum(CASE WHEN option_type = 'put' THEN premium_total ELSE 0 END) AS put_prem
  FROM uoa_contract_daily WHERE trading_date >= DATE 'D0' GROUP BY 1, 2)
SELECT r.trading_date, count(*) AS named_truncated,
       sum(CASE WHEN c.trades >= 1000 THEN 1 ELSE 0 END) AS with_1000_plus_trades,
       sum(CASE WHEN c.put_prem = 0 THEN 1 ELSE 0 END)   AS with_zero_put_premium
FROM r LEFT JOIN c USING (trading_date, sym)
GROUP BY r.trading_date ORDER BY r.trading_date;
```

**PASS for Step 1 requires:** V1 identical to §1. V2 shows `mode = single_page`, `shadow = false`,
`page_limit = 1000`, `status = success`, and `truncated` in the tens (the §1 floor is about 70 a night). V3 shows
`named_truncated ≤` that night's R2 capped count, with `with_1000_plus_trades = named_truncated` (a shortfall of a
few is allowed only for prints with zero price or size, which `_aggregate_trades_for_contract:1225` drops; list
them). Contract and symbol rows for `D0` onward need no check. Their equality with the old code is proved by §4, not by data.

**Step 2 — Haci, recommended, moves no published number.** Set `UOA_TRADES_PAGINATION_SHADOW_ENABLED=1`. Note `S0`.

```sql
-- V4. Shadow nights: how far the single page is from the full prints, counts and medians of a platform input.
WITH s AS (
  SELECT r.trading_date, e.key AS sym,
         (e.value->>'put_trades')::int      AS shadow_put_trades,
         (e.value->>'put_premium')::float   AS shadow_put_premium,
         (e.value->>'dir_ratio')::float     AS shadow_dir_ratio,
         (e.value->>'truncated_batches')::int AS shadow_cut
  FROM uoa_runs r
  CROSS JOIN LATERAL jsonb_each((r.stats_json::jsonb)->'trades_fetch'->'shadow_full') e
  WHERE r.run_type = 'nightly' AND r.trading_date >= DATE 'S0')
SELECT count(*)                                                                   AS shadow_symbol_days,
       count(DISTINCT s.trading_date)                                             AS nights,
       sum(CASE WHEN u.put_premium_total = 0 AND s.shadow_put_premium > 0 THEN 1 ELSE 0 END) AS puts_hidden_by_page,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY abs(u.dir_ratio - s.shadow_dir_ratio)) AS median_abs_dir_gap,
       sum(CASE WHEN sign(u.dir_ratio) <> sign(s.shadow_dir_ratio) THEN 1 ELSE 0 END)     AS dir_sign_flips,
       sum(CASE WHEN s.shadow_cut > 0 THEN 1 ELSE 0 END)                          AS ceiling_hit_even_paginated
FROM s JOIN uoa_symbol_daily u ON u.trading_date = s.trading_date AND u.symbol = s.sym;
```

Report V4 after ≥ 30 shadow nights, plus V6 for runtime. This gives Haci the size of the change before the flip:
how many symbol-days a night move, and how many flip flow direction. It is not a gate; the flip is his decision (header).

**Step 3 — Haci's decision: the flip.** Before it, the **Registrar** sweeps the locked questions named in the
header (Q014, Q019, Q029, Q030, and every prospective slate reader), rules on Q030's composition clause, and
records, for each, split at the flip date or hold. Then Haci sets `UOA_TRADES_PAGINATION_ENABLED=1`. Note `P0`.

**Step 4 — on `P0`, the Steward writes this DATA_NOTES entry** (a forward-only mechanism change, not a repair-log
row, because no historical row is rewritten):

> ## UOA option trades paginated from `P0` (PI-020, flag flipped `P0`, code `<sha>`)
> From trading date `P0`, `uoa_contract_daily.trade_count / volume_traded / premium_total / premium_max /
> first_trade_ts / last_trade_ts / buy_premium / sell_premium / unknown_premium / top_trades_json`,
> `uoa_symbol_daily.call_premium_total / put_premium_total / total_premium / call_buy_premium / put_buy_premium /
> net_directional_premium / dir_ratio / prem_* / unusual_* / quality_* / conc_* / score_* / bias_* / label_* /
> why_json`, `uoa_bulletins.lists_json / markdown`, and every SAS flow input and output downstream
> (`flow_strength_score`, flow polarity and vote, `overall_score`, `selected_rank`) are built from every print,
> not one 1,000-print page per 50 contracts. Nights before `P0` stay capped. A question spanning `P0` treats these
> as two different features (DP-50(a)). Nights with `stats_json.trades_fetch.mode` absent or `single_page` are
> capped.

```sql
-- V5. Flip nights, fixed names: prints above the old cap and puts present.
SELECT c.trading_date, c.underlying_symbol,
       sum(c.trade_count)                                                   AS trades,
       sum(CASE WHEN c.option_type = 'call' THEN c.trade_count ELSE 0 END)  AS call_trades,
       sum(CASE WHEN c.option_type = 'put'  THEN c.trade_count ELSE 0 END)  AS put_trades,
       jsonb_exists((r.stats_json::jsonb)->'trades_fetch'->'truncated', c.underlying_symbol) AS ceiling_hit
FROM uoa_contract_daily c
JOIN uoa_runs r ON r.trading_date = c.trading_date AND r.run_type = 'nightly'
WHERE c.trading_date BETWEEN DATE 'P0' AND DATE 'P0' + 6
  AND c.underlying_symbol IN ('SNDK', 'GOOG', 'GOOGL', 'MSFT', 'AMZN')
GROUP BY c.trading_date, c.underlying_symbol, r.stats_json
ORDER BY 1, 2;

-- V5b. Dropped-side signature, by side, before and after the flip: contracts the chain says traded
--      (snapshot_volume > 0) but that hold zero stored prints, on symbol-days with >= 1,000 stored prints.
WITH sd AS (
  SELECT trading_date, underlying_symbol FROM uoa_contract_daily
  WHERE trading_date BETWEEN DATE 'P0' - 30 AND DATE 'P0' + 30
  GROUP BY 1, 2 HAVING sum(trade_count) >= 1000)
SELECT CASE WHEN c.trading_date < DATE 'P0' THEN 'before' ELSE 'after' END AS period,
       c.option_type, count(*) AS contracts,
       sum(CASE WHEN c.snapshot_volume > 0 AND c.trade_count = 0 THEN 1 ELSE 0 END) AS traded_but_empty
FROM uoa_contract_daily c JOIN sd USING (trading_date, underlying_symbol)
GROUP BY 1, 2 ORDER BY 1, 2;

-- V5c. Share of >=1,000-print symbol-days with zero put premium, per month (R2's ratio), through P0's month and after.
--      (re-run §1 R2; compare capped_zero_put / capped for months after P0 with 2026-07 = 12.1%, 2026-08 = 11.1%)

-- V6. Runtime and publication time, 10 nightlies before and after each flag change (D0, S0, P0).
SELECT u.trading_date,
       extract(epoch FROM u.finished_at - u.started_at)                AS uoa_seconds,
       (u.stats_json::jsonb)->'trades_fetch'->>'requests'              AS trade_requests,
       (u.stats_json::jsonb)->'trades_fetch'->>'fetch_seconds'         AS fetch_seconds,
       (u.stats_json::jsonb)->'trades_fetch'->>'shadow_seconds'        AS shadow_seconds,
       (u.stats_json::jsonb)->'trades_fetch'->>'symbols_truncated'     AS truncated,
       s.finished_at                                                    AS sas_finished_at
FROM uoa_runs u
LEFT JOIN super_agent_select_runs s ON s.trading_date = u.trading_date
WHERE u.run_type = 'nightly' AND u.trading_date BETWEEN DATE 'X' - 14 AND DATE 'X' + 14   -- X = D0, S0 or P0
ORDER BY u.trading_date;
```

**PASS for the flip requires all of:**
1. **V5:** on each of the first five flip nights, each of the five names has `trades > 1000` or `ceiling_hit = true`,
   and `put_trades > 0` unless `ceiling_hit` names the put side.
2. **V5b:** `after` `traded_but_empty` for puts falls to within the same range as calls. Before, puts should far
   exceed calls; report both.
3. **V5c:** the zero-put share among ≥ 1,000-print symbol-days is **≤ 2%** over the first ten flip nights. Each
   remaining case either has no put contract selected, or its symbol is in that night's `truncated` map with side `put`.
4. **V2 on flip nights:** `mode = paginated`, `page_limit = 10000`, `symbols_truncated` (ceiling hits) reported. If
   it is above 5 a night on the names in V5, the Steward tells Haci to raise `UOA_TRADES_MAX_PAGES_PER_BATCH`.
5. **V6:** the median `sas_finished_at` shift is reported in minutes for each flag change. It is not a pass bar, but
   Haci reads it because `finished_at` is the actionable time (`DATA_NOTES.md:156-165`).
6. **V1 still identical** to §1 for months before `D0`. Any change there is a historical rewrite this fix does not
   make, so it is a FAIL: stop and find what wrote it.
