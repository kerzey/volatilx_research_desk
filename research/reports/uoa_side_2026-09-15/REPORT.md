# Option buy/sell side: the closing-quote proxy is wrong by construction, and what to build instead

**Date:** 2026-09-15 · **Platform SHA read:** `d112d37` · **Research SHA:** `fe8c091` (draft), revised after
Red Team review the same day · **Source:** Haci's question of 2026-09-15 (Omega's option-trades tool cannot say
whether a print was bought or sold; the nightly UOA job has the same problem; his idea: fetch UOA live every
10 minutes and aggregate to the day). Read-only queries and Alpaca market data only. Descriptive; not a study
result.

## Decision paragraph

**The platform's buy/sell label is mostly a record of where the option's price went after the trade, not of
who was aggressive.** Every print of the day is compared with the contract's quote *at the close*
(`services/uoa_screener.py:1114-1116` keeps the closing snapshot's quote; `:1246-1256` classifies every print
against it). Over 170 sessions since January the daily call buy-share moves *against* the market (Spearman
−0.57 with SPY's open-to-close move) and the put buy-share *with* it (+0.53). The Red Team's placebo settles
that this is the artefact and not trader behaviour: for prints made in the last 30 minutes, where the closing
quote *is* the quote at trade time, the correlation is zero (−0.03 / −0.02); for prints made more than three
hours before the close, in the **same contracts on the same days**, it is −0.58 / +0.46. The label feeds
`dir_ratio`, the SAS flow vote, Whale Watch qualification and the UOA conviction column. Filed as **PI-023**.
Alpaca keeps no historical option quotes, so the fix is to *capture the quote while the day runs*: Haci's idea
is the right shape. **EN-020** is an intraday sampler that every 10 minutes takes a chain snapshot per
underlying, records the quotes of contracts that just traded, fetches those prints with a short lag and labels
each against the quotes that bracket it; the nightly sums the buckets and marks anything uncovered as
*unknown* — never the old closing-quote guess. The placebo also says what to expect: a quote no more than ten
minutes old carries a residual tape correlation of about +0.03 (calls) / +0.10 (puts) against −0.55 / +0.47
today. The design below is the version after the Red Team's thirteen required changes (§7). It ships directly
(DP-59), labels its source on every row, and never rewrites history.

## 1. What the platform does today (read from code at `d112d37`)

| Step | Where | What |
|---|---|---|
| Contract selection | `uoa_screener.py:1086-1190` | ±10% moneyness, ≤180 DTE, OI ≥ 50, snapshot volume ≥ 10, relative spread ≤ 25% (`:801`, `:1124`); up to 60 contracts per symbol (`:799`). The bid/ask kept for the row is the **closing snapshot's** `latestQuote` (`:1114-1116`). |
| Trade fetch | `:1558-1570`, `options_client.py:987-1085` | Every print of the 09:30–16:00 session (`_session_window_utc`, `:908-911`), all pages (PI-020, shipped `3f1d3e6`). Only `p`, `s`, `t` are read; condition and exchange codes are discarded (`:1216-1256`). |
| Side label | `:1246-1256` | `edge = 0.10 × (ask − bid)` from the *closing* quote; print ≥ ask − edge → `buy_premium`; ≤ bid + edge → `sell_premium`; else `unknown_premium`. |
| Symbol roll-up | `:1663-1668` | `dir_ratio = (call_buy − put_buy) / (call_buy + put_buy + 1)` → `bull_dir` / `bear_dir` → flow scores and labels. |
| SAS | `symbol_context_builder.py:136-205` (sums buy/sell across all of a symbol's contracts, `:160-174`), `super_agent_select_scoring.py:254-330, 529-565` | Polarity when enabled (it is off, PI-014); otherwise the legacy `dir_ratio` direction vote at weight 1.3 (`:555-560`). SAS reads the **same session's** UOA row (`symbol_context_builder.py:482-483`), written by pipeline step 3 before SAS runs. |
| Whale Watch | `whale_watch_tracking.py:118-123` and the inline query `routers/whale_watch.py:153-159` | Qualifies a contract when classified fraction ≥ 0.50 **and** ask-share ≥ 0.65 — the same gate in two places. |
| UOA UI | `routers/uoa_screener.py:465-474` | "Conviction" = `buy_premium / premium_total`. |
| Omega | `ai_agents/option_trades_summary.py` (`d112d37`) | Tables of prints for any `start`/`end` window (`omega_agent.py:1660-1679`), **no side** — correct, and the docstring says why. |

The nightly starts at 16:43–17:04 ET (`uoa_runs.started_at`, September) and the stored `last_trade_ts`
reaches 15:59:59 every day, so the full session is fetched; the problem is only the quote it is judged against.

## 2. Evidence that the label follows the day's drift (PI-023)

### 2.1 Daily buy-share against the tape
`drift_test.py`, 170 sessions 2026-01-07..2026-09-14, `uoa_contract_daily` summed per day and side, SPY daily
bars from Alpaca. Buy-share = `buy / (buy + sell)` over classified premium.

| SPY open-to-close tercile | call buy-share | put buy-share | call − put |
|---|---:|---:|---:|
| down day | 0.624 | 0.412 | +0.212 |
| flat | 0.542 | 0.498 | +0.045 |
| up day | 0.429 | 0.598 | −0.169 |

Spearman: call buy-share vs SPY open-to-close **−0.566**; put buy-share **+0.533**. On its own this is
suggestive, not decisive: traders *could* sell calls into strength and buy puts for protection on up days.

### 2.2 The placebo that separates artefact from behaviour (Red Team, `ttc_test.py`, `ttc_test2.py`)
If the label is a closing-quote artefact it must vanish for prints made just before the close, because for a
15:55 print the closing quote *is* the quote at trade time. Trader behaviour has no reason to switch off at
15:30. Sample: the 10 largest prints per contract (`top_trades_json`), contracts with premium ≥ $100k, 73
sessions 2026-06-01..2026-09-14, 457,135 prints, re-classified with the platform's own rule against the
stored closing bid/ask, premium-weighted, Spearman against SPY open-to-close:

| minutes to close | call ρ | put ρ | prints |
|---|---:|---:|---:|
| < 10 | **+0.026** | +0.103 | 17,764 |
| 10–30 | −0.006 | −0.128 | 23,885 |
| 30–60 | +0.017 | +0.169 | 29,437 |
| 1–3 h | −0.240 | +0.181 | 94,151 |
| > 3 h | **−0.545** | **+0.474** | 291,898 |

With composition held fixed — the **same contract-days**, prints in both legs (114,619 prints): early (> 3 h)
ρ = **−0.577 / +0.455**; late (< 30 min) ρ = **−0.031 / −0.019**. The gradient with a zero at the close is the
artefact's signature and nothing else's. Two bonuses: the < 10-minute row is an empirical estimate of the
residual bias EN-020 will carry at a 10-minute cadence, and the early-vs-late gap is a per-session measure that
replaces a weak post-ship correlation test (§5.11 W3). Caveat: a big-print sample; descriptive.

Additional facts (`counts.py`): 497–499 symbols, 19,400–20,700 contracts and 154k–179k prints a night in
September (pre-PI-020 counts; PI-020 raises print counts on liquid names — SNDK alone had 25,750 on 09-08);
23–35% of premium is already `unknown` under the closing rule; of the classified part 47–59% is "buy".

**Who is hurt.** Everything in §1 below the "Side label" row. For SAS the flow vote carries tape-correlated
noise on the variable rule 7 calls dominant. Whale Watch admits contracts by the afternoon's drift. The UI's
conviction number is not what it says. For the desk, `manifest_v001`'s `uoa_symbol` / `uoa_contract` carry the
artefact throughout; Q014, Q029 and Q030 measure the platform *as it behaved* (legitimate); **H-092 must not
be registered** until a forward window with quote-at-trade labels exists.

## 3. What Alpaca can and cannot give us (checked 2026-09-15)

- **No historical option quotes.** Endpoints: bars, trades, latest trades, latest quotes, snapshots, option
  chain, condition and exchange codes (`docs.alpaca.markets/us/llms.txt`). Nothing labels yesterday's prints.
- **Chain snapshot per underlying** (`/v1beta1/options/snapshots/{underlying}`; client
  `_fetch_underlying_snapshots`, `options_client.py:868-921`): filters by type, strike band, expiry range;
  1,000 contracts a page; each contract carries `latestQuote {t, bp, ap, bs, as}`, `latestTrade`, `dailyBar`
  (cumulative day volume `v`), `minuteBar`, greeks, IV. **The client stops after `_MAX_SNAPSHOT_PAGES = 5`
  pages (`:33`) and records nothing when it does.**
- **Measured today (`chain_size.py`, ±12% of spot, ≤180 DTE, indicative feed, ~1 s a request):**

  | symbol | contracts | pages |
  |---|---:|---:|
  | SPY | 5,248 | 6 |
  | QQQ | 4,478 | 5 |
  | SNDK | 1,188 | 2 |
  | NVDA / TSLA / AAPL / KO / PFE | 204–778 | 1 |

  So the 5-page cap already truncates SPY, and pages arrive ordered by expiry (nearest first), each page
  roughly half calls, half puts — a *far-expiry* bias, not PI-020's calls-first bias. Most names are one page.
- **Trades** with `start`/`end`, 50 contracts a request, paginated, calls and puts apart (PI-020). The trades
  call does **not** pass a `feed` parameter (`:1047-1050`); snapshots do (`:856`, `:888`).
- **Streaming quotes** exist (`market_data/live_options.py`) but there is no wildcard for option quotes and
  tens of thousands of contracts on a web dyno is not a plan. Not for v1.
- **Plan limits.** Basic: 200 requests/min, indicative feed, the most recent 15 minutes of historical data
  withheld. Algo Trader Plus: 10,000/min, OPRA. The platform defaults to `indicative` unless
  `ALPACA_OPTION_FEED` is set (`options_client.py:30`); the desk's own environment reports `indicative`.
- **FMP** (Haci's premium key) has no options prints or quotes.

## 4. Alternatives considered and rejected

| Alternative | Why not |
|---|---|
| Tick rule (previous print on the same contract) | Near a coin flip for options — prices move with the underlying between sparse prints (Savickas & Wilson 2003: quote rules ≈ 80%, tick rule ≈ 60%). |
| Delta-adjusted closing quote (`mid_t ≈ mid_close − Δ × (S_close − S_t)`) | Corrects the dominant error and can run on history, but assumes constant IV and spread and needs every print re-fetched. Phase 2 (§5.8), calibrated against the sampler's labels. |
| Websocket quotes for the universe | Scale and a stateful process the platform does not run today. |
| Only fix Omega (label recent prints against the current quote) | Leaves the nightly, SAS, Whale Watch and the UI wrong. Omega reads the buckets instead (§5.6). |
| Poll trades for the whole universe every 10 minutes | `/trades` takes contracts, not underlyings — ~8,000 requests a tick. The snapshot's cumulative volume tells which contracts traded; only those are polled. |
| Working set only (last night's ≤ 60 selected contracts per symbol + today's volume leaders, via the multi-symbol snapshot) — the Red Team's cheaper alternative | Deterministic and immune to the page cap, but blind to the strike that lights up from nowhere, which is what "unusual" means. Adopted as the **sticky set** inside the band sweep (§5.2 step 3) rather than instead of it; the band sweep's measured cost (§3) is affordable. |

## 5. EN-020 — intraday UOA sampler: buy/sell from the quote at trade time (v2, after Red Team)

**Kind:** plumbing (a new data path and an internal view; the nightly's `buy_premium` / `sell_premium` /
`dir_ratio` change from the first covered session, as a fix does — §5.9). **Ships directly, DP-59.** No flag,
no shadow, no inertness proof. Rollback = `git revert`.

### 5.1 Schedule and calendar
A triggered WebJob, every 10 minutes, **09:30 → session close + 20 minutes** on NYSE sessions (the
`core.trading_days.is_trading_day` helper plus the XNYS calendar already used at
`services/whale_watch_tracking.py:58-65`; early closes end at 13:00, so the last tick is 13:20). The first tick
at 09:30 is a **quote-only tick**: it seeds every in-band contract's quote so the 09:30–09:40 interval has a
prior bracket. The `_is_weekday` guard in `services/uoa_scheduler.py:100` (which let a Labor Day run start) is
not reused. Missed ticks are allowed and become visible coverage loss, never a wrong label.

### 5.2 One tick, for each underlying in the nightly's universe (`_resolve_universe`, `uoa_screener.py:1043`)
1. **Spot** from the multi-symbol stock snapshot (one request per 100 underlyings).
2. **Chain snapshot** for strikes within ±12% of spot, expiries ≤ 180 days — the nightly's `_pick_contracts`
   filters, 2 points wider because the band is re-centred each tick and the nightly centres on the close. The
   sampler uses its **own page bound (12)** and records `pages` and whether a `next_page_token` was left
   unread per underlying, per tick; a truncated underlying is *coverage loss*, never silent.
3. **Sampled set** = in-band contracts ∪ **sticky set** (every contract sampled earlier today, and last night's
   selected contracts for the symbol, fetched by the multi-symbol snapshot if they left the band). A name that
   gaps 10% keeps its morning coverage.
4. **Atomic per-contract row** in `uoa_quote_tick` carrying *this* tick's quote **and** the previous tick's
   quote for the same contract, copied forward in the same upsert: `(trading_date, contract, tick_seq,
   tick_ts, quote_ts, bid, ask, bid_size, ask_size, day_volume, feed, prev_tick_seq, prev_quote_ts, prev_bid,
   prev_ask, prev_bid_size, prev_ask_size, prev_day_volume, raw_quote_json)`. No read-then-write across
   transactions: a tick that dies half-way leaves rows whose `tick_seq` is behind, and the interval is marked
   degraded (step 7). Quotes are capture-once and irreproducible, so the raw payload (feed, exchange, any
   condition) is kept wide.
5. **Traded set** = contracts whose `day_volume` rose since `prev_day_volume`. Only their rows are retained
   beyond the next tick (others are pruned at the next upsert), which keeps the table to ~2 rows per traded
   contract-interval.
6. **Trade fetch, lagged.** Fetch prints for the traded set of the interval that ended **≥ 20 minutes ago**
   (two ticks; clears Basic's 15-minute hold-back) with `start`/`end` = that interval, 50 contracts a request,
   calls and puts apart, all pages (`get_option_trades`). On Plus the lag can be one tick. Every print's
   **condition codes, exchange and size** are kept (today they are discarded).
7. **Classify each print** (§5.4) against the bracketing quotes from step 4: the tick row whose `prev_*` quote
   is the last sample at or before `t` and whose own quote is the first after `t`. A print before the day's
   first quote sample (including the 09:30:00 auction print) is `unknown (pre_open)`. An interval whose tick
   row is missing or degraded is `unknown (no_quote)`.
8. **Aggregate** into `uoa_contract_intraday`, one row per (trading_date, contract, `bucket_start`):
   `trade_count`, `volume`, `premium_total`, `buy_premium`, `sell_premium`, `unknown_premium`, `buy_count`,
   `sell_count`, `unknown_count`, premium by reason (`both`, `one_prev`, `one_next`, `conflict`, `fast_market`,
   `mid`, `no_quote`, `pre_open`, `wide_spread`), `multileg_premium` (prints whose condition code marks a
   complex-order leg), `oversize_premium` (prints larger than the displayed size at the quote used),
   `quote_age_median_sec`, `relative_spread_median`, `edge_ratio_hist` (a 10-bin histogram of
   `(price − mid) / (spread / 2)` for re-tuning `aggressor_edge` later), `top_prints_json` (≤ 5 largest prints
   with price, size, side, reason, the bid/ask used, quote age, condition codes). Idempotent: a re-run replaces
   the bucket.
9. **Tick status row** in `uoa_runs`, `run_type = 'intraday_tick'`, written **last**: tick time, `tick_seq`,
   underlyings sampled, snapshot requests, pages, truncated underlyings, contracts sampled, traded-set size,
   prints fetched, premium by reason, 429s, seconds, degraded flag. Roughly 40 rows a session.

**Budget under Basic (200/min).** ~500 underlyings → ~600–700 snapshot pages (§3: most names one page, SPY 6,
QQQ 5) + 5 stock-snapshot requests + the traded set (~1,000–3,000 contracts an interval after PI-020) / 50 ≈
20–60 trade requests, mostly one page for a 10-minute window. **≈ 700–800 requests a tick.** At the measured
~1 s a request, serial execution takes 12 minutes — too slow — so the sampler runs **4 concurrent workers
with a self-imposed ceiling of 80 requests/min** (40% of Basic's limit, leaving the rest for the 16:02 monitor
and the 16:05 pipeline on the same account; `_request` already backs off on 429, `options_client.py:78-94`).
A tick then takes ~9 minutes under Basic — the cadence is what Basic allows, not a choice — and seconds under
Plus, where 5 minutes is free. 429s attributable to the sampler are counted in the tick row.

**Storage.** `uoa_quote_tick`: ~2 rows per traded contract-interval, ~100k–250k rows a session, retained
**45 sessions**; the quotes behind every bucket's `top_prints_json` live in the bucket row itself, so the
labels of the largest prints stay auditable for the full **400 sessions** `uoa_contract_intraday` is kept.
Retention is application code inside the job (DP-49 concerns briefs handing the coding agent a DB step, not
scheduled housekeeping the platform runs itself): delete only by `trading_date < cutoff`, only from the two
new tables, in bounded batches, refusing to run if the cutoff falls inside the retention window or the row
estimate exceeds a sanity cap, logged as a `uoa_runs` row.

### 5.3 Why bracket quotes, and why the rule is asymmetric
A quote sampled up to 10 minutes before a print can be stale if the underlying moved; the quote after can
already carry the print's own impact (an aggressive buy lifts the offer, so the post-trade ask sits above the
print and a *next-only* label would read it as a sale). Therefore: the **previous** quote alone may decide; the
**next** quote alone may not. Disagreement between the two is the measure of whether 10 minutes is short
enough; the conflict share is telemetry (§5.11 W4).

### 5.4 `classify_print(price, size, prev_quote, next_quote, edge=0.10, max_age_sec=900, max_rel_spread=0.25)` → `(side, reason)`
- A bracket quote is **usable** if `ask ≥ bid > 0`, its age ≤ `max_age_sec` and `(ask − bid) / mid ≤
  max_rel_spread` (the nightly's own spread gate, `uoa_screener.py:801`). Otherwise `ABSENT`
  (`wide_spread` recorded separately from `no_quote`).
- **Fast-market guard:** if both brackets are usable and `|mid_next − mid_prev| > (ask_prev − bid_prev)` →
  `UNKNOWN (fast_market)`, regardless of agreement.
- Per usable bracket: `edge_$ = edge × (ask − bid)`; `BUY` if `price ≥ ask − edge_$`; `SELL` if
  `price ≤ bid + edge_$`; else `MID`.
- Combine: both `BUY` → `BUY (both)`; both `SELL` → `SELL (both)`; `BUY` vs `SELL` → `UNKNOWN (conflict)`;
  decisive prev + `MID`/`ABSENT` next → that side `(one_prev)`; `ABSENT`/`MID` prev + decisive next → the side
  is *recorded* as `(one_next)` but **counted as unknown** in `buy_premium` / `sell_premium` until telemetry
  shows it unbiased (W4); both `MID` → `UNKNOWN (mid)`; both `ABSENT` → `UNKNOWN (no_quote)`.
- `size > displayed size` at the deciding quote → the side stands, `oversize` flagged. A condition code marking
  a complex-order leg → the side stands, `multileg` flagged (excluded from nothing in v1; measured first).
- Same `edge` as today (`aggressor_edge`, `:812`) so the only thing that changes is the quote. Pure function,
  unit-tested on fixed vectors (§5.10).

### 5.5 Nightly merge (`run_uoa_nightly`, replacing the per-contract call at `uoa_screener.py:1599`)
The nightly keeps fetching the full day's prints; `premium_total`, `trade_count`, top prints and every other
column are unchanged. For each selected contract it reads the day's buckets and computes coverage **in
premium and in count**:
- `buy_premium = Σ bucket.buy`, `sell_premium = Σ bucket.sell`, `unknown_premium = premium_total − buy − sell`.
  Uncovered premium is **unknown**. There is no closing-quote fallback: a sampler outage makes the day *quiet*,
  not *wrong*. The three always reconcile to `premium_total`.
- New columns: `uoa_contract_daily.aggressor_coverage_premium`, `.aggressor_coverage_count`,
  `.aggressor_reason_json` (premium by reason). `uoa_symbol_daily.aggressor_qat_share` = the symbol's
  classified premium ÷ its total premium (classified = `both` + `one_prev`).
- **Closing the re-entry door.** `dir_ratio` (`:1666`) and `net_directional_premium` are **NULL** when
  `aggressor_qat_share < 0.50` (the same threshold SAS's polarity uses, `super_agent_select_scoring.py:309`),
  so the legacy vote at `:555-560` abstains instead of reading a half-labelled symbol; `bull_dir` / `bear_dir`
  fall back to their neutral 0.5 and the flow labels say `FLOW_UNCLASSIFIED` on such nights. Symbol-level
  gating is required because `prefetch_flow_polarity` sums across all of a symbol's contracts
  (`symbol_context_builder.py:160-174`).
- `stats_json` gains an `aggressor` block: premium by reason, median coverage, tick count, truncated
  underlyings, feed.

### 5.6 Consumers
- **Omega `get_option_trades`** (`option_trades_summary.py`): per-contract and per-expiry tables gain
  `buy_premium_usd`, `sell_premium_usd`, `unknown_premium_usd`, **`side_window_start`, `side_window_end`,
  `side_premium_total`** (the buckets' own premium for the contract) and `side_source ∈ {quote_at_trade,
  partial, unavailable}`; side columns are **null unless `side_premium_total / premium_usd ≥ 0.80`** for that
  contract, so the model is never handed a bucket numerator over a live-fetch denominator. The live tail (the
  last ≤ 20 minutes, which never has buckets) may be labelled against the *current* quote, tagged `quote_now`,
  never stored — the placebo puts a ≤ 10-minute-old quote's bias at ρ ≈ +0.03. The largest prints carry `side`
  and `reason` when they sit in a bucket's `top_prints_json`.
- **Live view (internal, Haci only).** `GET /api/admin/uoa/intraday?date=&window_min=30|60|day`: per
  underlying, call and put buy-side and sell-side premium over the window, net buy-side premium
  `(call_buy − call_sell) − (put_buy − put_sell)`, classified share, conflict and multileg shares, tick
  freshness and degraded flags; expandable to contract buckets and top prints with sides and reasons. Admin
  route, no subscriber copy (DP-48 internal tool). A subscriber-facing live UOA page is a separate EN gated on
  a research question (does intraday buy-side flow predict the close or next session? — to BACKLOG once 20
  sessions of buckets exist).
- **Whale Watch:** both copies of the gate — `services/whale_watch_tracking.py:118-123` and the inline
  query `routers/whale_watch.py:153-159` — keep `classified_fraction ≥ 0.50`; with uncovered premium now
  unknown, an outage day qualifies nothing, which is the correct behaviour for a signal product.
- **UOA UI conviction** (`routers/uoa_screener.py:465-474`) shows coverage next to the ratio, since low
  coverage would otherwise read as low conviction.

### 5.7 What it does *not* do
No historical row is rewritten (`manifest_v001` keeps the artefact). No SAS weight, threshold or the polarity
flag changes (PI-014 owns that). Nothing is published to subscribers. Multi-leg prints are flagged and
measured, not excluded (a later, evidence-based change).

### 5.8 Phase 2 (optional, decided by the desk after 20 sessions of Phase 1)
Delta-adjusted closing-quote classifier for history, `mid_t ≈ mid_close − Δ_close × (S_close − S_t)` with
`S_t` from the underlying's minute bars. Phase 1's `both`/`one_prev` labels are the truth set; if agreement
≥ 85% on covered prints, a backfill of 2026 (prints re-fetched from Alpaca, held since February 2024) becomes a
separate PI-023 repair brief with its own DATA_NOTES entry. Not before.

### 5.9 Numbers that change, and when (DP-59)
From the **first session on which the sampler ran and the merged nightly consumed its buckets** (SAS reads the
same session's UOA row, `symbol_context_builder.py:482-483`, produced by pipeline step 3 before SAS runs):
`uoa_contract_daily.buy_premium / sell_premium / unknown_premium`; `uoa_symbol_daily.call_buy_premium /
put_buy_premium / net_directional_premium / dir_ratio` (NULL when unclassified), `bull_dir` / `bear_dir`, the
three flow scores and labels; the SAS flow vote (abstains on unclassified symbols); Whale Watch qualification;
the UOA conviction column; Omega's tables gain side columns. Expected: the early-vs-late gap of §2.2 collapses;
the classified share falls at first (conflicts, fast markets, `one_next` and pre-open prints become unknown
instead of being forced). The desk logs the ship SHA, the first covered session and the per-session
`aggressor_qat_share` in `DATA_NOTES.md`; Q014 / Q019 / Q029 / Q030 split there under DP-50 (one window with
PI-020 if both ship within days). `research/lib/freeze_config.json` gains `uoa_quote_tick` and
`uoa_contract_intraday` with availability = `bucket_start + 20 minutes` (the fetch lag), lag 0.

### 5.10 Tests (standalone runner, no `pytest` — PI-021)
`classify_print` vectors: both / one_prev / one_next (counted unknown) / conflict / fast_market / mid /
no_quote / pre_open / wide_spread / crossed / aged-out / edge exactly on the boundary / oversize / multileg
flag. Traded-set selection from two tick rows (volume up, unchanged, new contract, contract gone, sticky
carry-over). Atomic tick row: a simulated half-written tick leaves `tick_seq` behind and the interval reads
degraded. Bucket aggregation and idempotent replace. Nightly merge: `buy + sell + unknown == premium_total`
on every row, coverage in premium and count, `dir_ratio` NULL below 0.50 `aggressor_qat_share`. Retention
refuses a cutoff inside the window. Omega table: side columns null under 0.80 coverage, `quote_now` never
persisted. Fixtures are literal dicts; no network, no database.

### 5.11 After-deploy check (Data Steward, read-only, `/desk-run verify EN-020 <sha>`)
W1. `uoa_runs`: one `intraday_tick` row per 10 minutes from 09:30 to close + 20 (≥ 40 on a full session,
    ≥ 22 on a 13:00 close) for three consecutive sessions, none degraded, 429 count not rising tick over tick,
    truncated underlyings listed (SPY acceptable if recorded).
W2. On those sessions: `buy + sell + unknown = premium_total` on every `uoa_contract_daily` row (1 cent);
    ≥ 80% of the book's premium in contracts with `aggressor_coverage_premium ≥ 0.90`; `dir_ratio` NULL on
    every symbol with `aggressor_qat_share < 0.50` and non-NULL on every symbol above it.
W3. **The placebo, post-ship** (`ttc_test2.py` on post-ship sessions with the *new* labels from
    `top_prints_json`): early-leg (> 3 h) |ρ| vs SPY open-to-close within 0.10 of the late-leg |ρ| after 10
    sessions. Decisive in days: thousands of prints per session, built-in zero. The daily Spearman of §2.1 is
    reported alongside but is not the criterion (its standard error at n = 20 is ≈ 0.23).
W4. Premium share by reason per session: `conflict` + `fast_market` > 15% on the top-20 liquid names for five
    sessions → cadence note to Haci (5 minutes needs Plus), not a failure; `one_next` share and its own
    early-vs-late ρ reported, so the desk can later decide to count it.
W5. Omega: a DB read showing bucket rows exist for a liquid contract and a completed window, plus the
    repo-only unit test in §5.10 that the tool nulls side columns under 0.80 coverage. The live tool call is
    Haci's, not the desk's (DP-49).
W6. `DATA_NOTES.md` entry with ship SHA, first covered session, the feed in use and per-session
    `aggressor_qat_share`; `freeze_config.json` entries present; Q014 / Q019 / Q029 / Q030 split noted.

### 5.12 Two facts Haci must state in the brief request (they decide numbers, not whether to build)
1. **Which Alpaca plan and feed are live.** `ALPACA_OPTION_FEED` unset means `indicative`
   (`options_client.py:30`); the desk's environment reports `indicative`. Under `indicative` the captured
   quotes are derived, not consolidated NBBO, and the brief must say plainly that label quality is unproven
   until W3 passes; under OPRA/Plus the fetch lag drops to one tick and 5-minute cadence is available. The feed
   is recorded on every quote row either way.
2. Whether the live view sits in the existing UOA tab (admin-only panel) or a new admin route.

### 5.13 Haci's answers (2026-09-15) and the settings that follow — these override §5.1, §5.2, §5.6 and §5.12
1. **Feed: OPRA in production** (Algo Trader Plus: 10,000 requests/min, no 15-minute hold-back, consolidated
   NBBO). Therefore: **5-minute cadence**, quote-only seed tick at 09:30, last tick at close + 10 minutes;
   **one-tick lag** (each tick fetches the interval that ended at the previous tick); the 80/min ceiling and
   the 4-worker limit stay as a courtesy to the 16:02 and 16:05 jobs but are far from binding; `fast_market`,
   `conflict` and quote-age numbers should all fall against the 10-minute estimates in §2.2. `feed` is still
   recorded on every quote row.
2. **Live view: a tab under AI Picks, "UOA live".** Visible to the **admin role only** in v1 (Haci is the
   platform's only user; making it subscriber-visible later is a role change gated on a research question,
   DP-48). Default table = today's unusual names; ticker search opens the symbol's contract buckets and top
   prints with sides. **"Unusual" is a rule:** `today's classified premium so far ÷ (trailing 20-session mean
   daily premium × fraction of the session elapsed) ≥ 3`, using `uoa_symbol_daily.total_premium` for the
   trailing mean. Row columns: symbol, unusual ratio, net buy-side premium `(call_buy − call_sell) − (put_buy −
   put_sell)`, call buy / sell, put buy / sell, classified share, largest print (contract, size, side, reason),
   multi-leg share, last tick time. Rows with classified share < 0.50 are greyed and sorted last, so a quiet
   sampler reads as *no data*, not *no activity*. Numbers only; no sentiment words.
3. **Universe (desk recommendation, Haci to confirm in the brief request):** the nightly UOA universe
   (`_resolve_universe`, S&P 500 list today, ~500 names — the floor, since every scored symbol needs coverage
   or its `dir_ratio` is NULL) ∪ last night's SAS candidates ∪ the EN-019 20-name liquid list ∪ Haci's
   favourites (`UserFavoriteSymbol`) ∪ SPY, QQQ, IWM; cap 800; ~1,000 requests a tick under Plus. A ticker
   searched in the tab that is not in the universe is **added to the day's sticky set from that moment**; its
   earlier prints stay `unknown (not_sampled)` and the tab says so on the row.

## 6. Seen in passing
- `uoa_runs` has a `nightly` row dated **2026-12-09** in state `running` (started 10:03 ET) and one for the
  Labor Day holiday 2026-09-07 (22:30, never finished — the `_is_weekday` guard). Harmless to the data; noted
  for the PI-002 watchdog.
- PI-020 shipped in the platform as `3f1d3e6` (PR #31) with Omega's table tool `d112d37`; the desk's register
  still says BRIEF_WRITTEN. `/desk-run verify PI-020 3f1d3e6` is due after the first nightly that runs it.
- `freeze_config.json` declares `uoa_symbol` available at 16:05 with lag 0; the rows are written 16:43–17:13
  inside the same pipeline, before SAS reads them for the same session. 16:05 is the nominal decision time, so
  no leak — but the note there should say the rows post-date 16:05 by ~40 minutes.

## 7. Red Team review (2026-09-15) and what changed
Verdict: **ACCEPT WITH CHANGES**; PI-023 "real, and made stronger" by the placebo (§2.2). The thirteen required
changes and their disposition:

| # | Required | Done in v2 |
|---|---|---|
| 1 | Kill the closing-quote fallback; uncovered → unknown; coverage in premium and count | §5.5 |
| 2 | Close the re-entry path: `dir_ratio` NULL / vote abstains below symbol-level classified share | §5.5 |
| 3 | Snapshot page cap truncates silently | own bound 12, truncation recorded as coverage loss, §5.2 step 2; measured §3 |
| 4 | Re-measure the budget; cap the sampler's rate vs the 16:02 / 16:05 jobs | §3 table, §5.2 budget (80/min ceiling, 4 workers) |
| 5 | Fix the opening | quote-only tick at 09:30; `pre_open` reason, §5.1, §5.4 |
| 6 | Asymmetric "one" rule | `one_prev` counts, `one_next` recorded but unknown, §5.4 |
| 7 | Bracket-movement guard | `fast_market`, §5.4 |
| 8 | Atomic, self-describing tick | `uoa_quote_tick` carries both quotes; status row last, §5.2 steps 4, 9 |
| 9 | Omega join | `side_window_*`, `side_premium_total`, 0.80 threshold, `partial`, §5.6 |
| 10 | Whale Watch gate lives in two places; line citations | both cited, §1, §5.6 |
| 11 | Knowledge time: availability for new tables; timing of the SAS change | §5.9 (SAS reads the same session's row, so the change lands on the first covered session, not one later) |
| 12 | Resolve the feed | §5.12 item 1, recorded per row, named in W6 |
| 13 | Replace W3 (underpowered); W5 not a desk check | §5.11 |

Recommended items adopted: condition/exchange codes and multileg share; oversize flag; sticky set; intraday
spread gate; raw wide quote payload; edge-ratio histogram; auditable top-print quotes for 400 sessions;
`quote_now` live tail in Omega; coverage beside conviction; XNYS calendar. Not adopted: the working set *as
the primary design* (blind to new strikes; the band sweep is affordable at the measured page counts — §4).

## Files
`counts.py` (book size, unknown share, latest run stats) · `drift_test.py` + `drift_test_daily.csv` (§2.1) ·
`ttc_test.py`, `ttc_test2.py` (§2.2, Red Team) · `timing.py` (nightly start times, last print seen) ·
`chain_size.py` (§3 page counts).
