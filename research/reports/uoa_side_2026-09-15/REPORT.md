# Option buy/sell side: the closing-quote proxy is wrong by construction, and what to build instead

**Date:** 2026-09-15 · **Platform SHA read:** `d112d37` · **Research SHA:** `e043b42` · **Source:** Haci's
question of 2026-09-15 (Omega's option-trades tool cannot say whether a print was bought or sold; the nightly
UOA job has the same problem; his idea: fetch UOA live every 10 minutes and aggregate to the day).
Read-only queries and Alpaca market data only. Descriptive; not a study result.

## Decision paragraph

**The platform's buy/sell label is mostly a record of where the option's price went after the trade, not of
who was aggressive.** Every print of the day is compared with the contract's quote *at the close*
(`services/uoa_screener.py:1114-1116` selects the quote from the closing snapshot; `:1246-1256` classifies every
print against it). Over 170 sessions since January the daily call buy-share moves *against* the market
(Spearman −0.57 with SPY's open-to-close move) and the put buy-share moves *with* it (+0.53): on up days the
data says 43% of call premium was bought and 60% of put premium was bought; on down days 62% and 41%. That is
the mirror image of what a real aggressor label would show, and it feeds `dir_ratio`, `call_buy_premium`,
`put_buy_premium`, the SAS flow vote, the Whale Watch qualification and the UOA conviction display. Filed as
**PI-023**. The fix is not a formula change: Alpaca keeps no historical option quotes, so the quote at trade
time has to be *captured while the day runs*. Haci's idea is the right shape. The enhancement below
(**EN-020**) is an intraday sampler that every 10 minutes records the quotes of contracts that just traded and
classifies each print against the quotes that bracket it, stores 10-minute buckets, and lets the nightly job
sum those buckets instead of re-judging the day against the close. It gives Omega and a live "UOA now" view the
same labelled numbers. It ships directly (DP-59), labels its source on every row, and never rewrites history.

## 1. What the platform does today (read from code at `d112d37`)

| Step | Where | What |
|---|---|---|
| Contract selection | `uoa_screener.py:1086-1190` | ±10% moneyness, ≤180 DTE, OI ≥ 50, snapshot volume ≥ 10, relative spread ≤ 25%; up to 60 contracts per symbol. The bid/ask kept for the row is the **closing snapshot's** `latestQuote` (`:1114-1116`). |
| Trade fetch | `:1558-1570`, `options_client.py:987-1085` | Every print of the 09:30–16:00 session (`_session_window_utc`, `:908-911`), all pages (PI-020, shipped `3f1d3e6`). |
| Side label | `:1246-1256` | `edge = 0.10 × (ask − bid)` from the *closing* quote; print ≥ ask − edge → `buy_premium`; ≤ bid + edge → `sell_premium`; else `unknown_premium`. |
| Symbol roll-up | `:1663-1668` | `dir_ratio = (call_buy − put_buy) / (call_buy + put_buy + 1)` → `bull_dir` / `bear_dir` → flow scores and labels. |
| SAS | `symbol_context_builder.py:136-205`, `super_agent_select_scoring.py:254-330, 529-565` | Polarity `(call_buy − call_sell − put_buy + put_sell) / total` when enabled (it is off, PI-014) else the legacy `dir_ratio` vote at weight 1.3. |
| Whale Watch | `whale_watch_tracking.py:10-20`, `routers/whale_watch.py:153-159` | Qualifies a contract when classified fraction ≥ 0.50 **and** ask-share ≥ 0.65. |
| UOA UI | `routers/uoa_screener.py:465-474` | "Conviction" = `buy_premium / premium_total`. |
| Omega | `ai_agents/option_trades_summary.py` (`d112d37`) | Tables of prints, **no side** — correct, and the note in that commit says why. |

The nightly starts at 16:43–17:04 ET (`uoa_runs.started_at`, September) and the stored `last_trade_ts` reaches
15:59:59 every day, so the full session is fetched; the problem is only the quote it is judged against.

## 2. Evidence that the label follows the day's drift (PI-023)

`drift_test.py`, 170 sessions 2026-01-07..2026-09-14, `uoa_contract_daily` summed per day and side, SPY daily
bars from Alpaca. Buy-share = `buy / (buy + sell)` over classified premium.

| SPY open-to-close tercile | call buy-share | put buy-share | call − put |
|---|---:|---:|---:|
| down day | 0.624 | 0.412 | +0.212 |
| flat | 0.542 | 0.498 | +0.045 |
| up day | 0.429 | 0.598 | −0.169 |

Spearman: call buy-share vs SPY open-to-close **−0.566**; put buy-share **+0.533** (vs close-to-close −0.49 /
+0.45). Mechanism: on an up day a call's closing quote sits above most of the day's prints, so those prints
fall at or below the closing bid and are labelled *sold*; the put's closing quote sits below its prints, which
are labelled *bought*. A genuine aggressor label would, if anything, lean the other way (buyers chase calls
on up days). The size of the swing (≈ 20 points of buy-share between terciles) is the artefact's floor, not
its total: it is what survives after averaging across ~20,000 contracts a night.

Additional facts (`counts.py`): 497–499 symbols, 19,400–20,700 contracts and 154k–179k prints a night in
September (pre-PI-020 counts; PI-020 will raise print counts substantially on liquid names — SNDK alone had
25,750 on 09-08); 23–35% of premium is already `unknown` under the closing-quote rule; of the classified part
47–59% is "buy" month by month.

**Who is hurt.** Everything in §1 below the "Side label" row. For SAS, the flow vote is a *direction* vote:
on a strong up day the legacy vote leans bearish for calls-heavy names (their buy-share is depressed) and
bullish for puts-heavy names — noise correlated with the tape, which rule 7 says is the dominant variable. For
Whale Watch the 0.65 ask-share gate admits contracts by the afternoon's drift. For the desk, `manifest_v001`'s
`uoa_symbol` and `uoa_contract` carry the artefact for their whole range; Q014, Q029 and Q030 measure the
platform *as it behaved*, which stays legitimate; H-092 (flow label vs premium mix) is now blocked by PI-023
as well as PI-020 and must not be registered until a clean forward window exists.

## 3. What Alpaca can and cannot give us (checked 2026-09-15)

- **No historical option quotes.** The options endpoints are bars, trades, latest trades, latest quotes,
  snapshots, option chain, condition and exchange codes (`docs.alpaca.markets/us/llms.txt`). Quotes exist only
  as "latest". Nothing can label yesterday's prints correctly after the fact.
- **Snapshots per underlying** (`/v1beta1/options/snapshots/{underlying}`, the client's
  `_fetch_underlying_snapshots`, `options_client.py:868-921`): filtered by type, strike band and expiry range,
  up to 1,000 contracts a page, paginated; each contract returns `latestQuote {t, bp, ap, bs, as}`,
  `latestTrade`, `dailyBar` (cumulative day volume `v`), `minuteBar`, greeks and IV.
- **Trades** with `start`/`end`, 50 contracts a request, paginated (PI-020 code).
- **Streaming quotes** exist (`market_data/live_options.py` wraps them) but there is no wildcard for option
  quotes and 20,000+ contracts on a web dyno is not a serious plan. Not for v1.
- **Plan limits.** Basic: 200 requests/min, indicative feed, and the most recent 15 minutes of historical data
  are withheld. Algo Trader Plus: 10,000/min, OPRA. The platform's default feed is `indicative` unless
  `ALPACA_OPTION_FEED` is set (`options_client.py:30`). The design below works under Basic; Plus lets it run at
  5 minutes.
- **FMP** (Haci's premium key) has no options prints or quotes; it does not help here.

## 4. Alternatives considered and rejected

| Alternative | Why not |
|---|---|
| Tick rule (compare with the previous print on the same contract) — free, works on history | For options the tick rule is close to a coin flip: option prices move with the underlying between sparse prints, so an "uptick" says nothing about the aggressor. The options trade-classification literature (Savickas & Wilson 2003) puts quote rules near 80% and the tick rule near 60%. Would replace one bias with another. |
| Delta-adjusted closing quote: shift the closing mid back to trade time by `Δ × (S_close − S_t)` using the underlying's minute bars | Corrects the dominant error and *can* run on history, but assumes constant IV and spread through the day and needs every print re-fetched. Worth doing **only after** the sampler exists, because the sampler gives ground truth to calibrate it against. Kept as Phase 2 (§5.8). |
| Websocket quotes for the universe | Subscription scale (no wildcard; tens of thousands of contracts), stateful process on the web dyno, and nothing in the platform runs that way today. |
| Only fix Omega (label recent prints against the current quote) | Leaves the nightly, SAS, Whale Watch and the UI with the wrong number. Omega should *read* the same buckets instead. |
| Poll trades for the whole universe every 10 minutes (Haci's first sketch, literally) | Right idea, wrong unit: `/trades` takes contracts, not underlyings; polling all ~400k in-band contracts is ~8,000 requests a tick. The snapshot's cumulative volume tells which contracts traded, so only those are polled (§5.2). |

## 5. EN-020 — intraday UOA sampler: buy/sell from the quote at trade time

**Kind:** plumbing (a new data path and an internal view; no subscriber number changes *by itself*, but the
nightly's `buy_premium` / `sell_premium` / `dir_ratio` change from the ship date, as a fix does — named in
§5.9). **Ships directly, DP-59.** No flag, no shadow, no inertness proof. Rollback = `git revert`.

### 5.1 Schedule
A triggered WebJob, weekdays, every 10 minutes from **09:40 to 16:20 ET** (first tick at 09:40 so the first
interval is a full one; last tick at 16:20 so the 15:50–16:00 prints are fetchable even on Basic's 15-minute
hold-back; the nightly starts at 16:43+). Holiday guard from the platform's trading calendar. Missed ticks are
allowed and recorded; the design degrades to coverage, never to a wrong label (§5.5).

### 5.2 One tick, for each underlying in the nightly's universe (`_resolve_universe`, `uoa_screener.py:1043`)
1. Spot = underlying's latest trade (stock snapshot). Chain snapshot for strikes within **±12%** of spot
   (2 points wider than the nightly's band, because the band is re-centred every tick and the nightly centres
   on the close) and expiries ≤ 180 days — the nightly's `_pick_contracts` filters.
2. For every contract returned: `(contract, tick_ts, quote_ts=latestQuote.t, bid, ask, bid_size, ask_size,
   day_volume=dailyBar.v)`. Upsert into **`uoa_quote_latest`** (one row per contract, overwritten each tick;
   ~300k rows, no history). This table is the "quote prevailing at the start of the next interval".
3. **Traded set** = contracts whose `day_volume` rose since the previous tick (or first appearance with
   volume > 0). For each: write two rows to **`uoa_quote_sample`** — the previous tick's quote for that
   contract (from `uoa_quote_latest` before the upsert) and this tick's quote. Rows carry `tick_ts`, `quote_ts`,
   bid/ask/sizes. Nothing is written for contracts that did not trade.
4. **Trade fetch, lagged.** Fetch prints for the traded set of the interval that ended **≥ 20 minutes ago**
   (two ticks; clears Basic's 15-minute hold-back with margin) with `start`/`end` = that interval, 50 contracts a
   request, calls and puts apart, all pages (`get_option_trades`, PI-020). On Plus the lag can be one tick;
   the lag is a setting, not a gate.
5. **Classify each print** (pure function, §5.4) against the two `uoa_quote_sample` rows that bracket its
   timestamp (the latest sample at or before `t`, the earliest after `t`, both within `max_quote_age` = 15
   minutes).
6. **Aggregate** into **`uoa_contract_intraday`**: one row per (trading_date, contract, `bucket_start`):
   `trade_count`, `volume`, `premium_total`, `buy_premium`, `sell_premium`, `unknown_premium`,
   `buy_count`, `sell_count`, `unknown_count`, `conflict_premium` (bracket quotes disagreed), `no_quote_premium`
   (no bracket within age), `quote_age_median_sec`, `top_prints_json` (≤ 5 largest prints with price, size,
   side, the bid/ask used and quote age). Idempotent: re-running a tick replaces its bucket rows.
7. **Telemetry** row in `uoa_runs` with `run_type = 'intraday_tick'`: tick time, underlyings sampled, snapshot
   requests and pages, contracts sampled, traded-set size, prints fetched, prints by side, conflict and
   no-quote shares, request count, 429s, seconds, and any underlyings skipped. 40 rows a session.

**Budget under Basic (200/min).** ~500 underlyings × 1–3 snapshot pages ≈ 600–1,000 requests, plus the traded
set (~1,000–3,000 contracts an interval after PI-020) / 50 ≈ 20–60 trade requests and their pages. About
700–1,100 requests per tick, 70–110 a minute if spread over the tick. Fits; `_request` already backs off on
429 (`options_client.py:78-94`). Under Plus the same tick takes seconds and a 5-minute cadence is free.

**Storage.** `uoa_quote_sample`: ~2 rows per traded contract-interval, roughly 100k–250k rows a session; keep
**45 sessions** then delete (the nightly's merge is what persists). `uoa_contract_intraday`: 50k–120k rows a
session, keep 400 sessions. `uoa_quote_latest`: bounded by the in-band universe.

### 5.3 Why bracket quotes, not one
A quote sampled up to 10 minutes before the print can be stale when the underlying moved in between; the quote
after can already reflect the print's own impact. Requiring both to agree, or one to be decisive while the
other is silent, is the conservative reading. The disagreement rate (`conflict_premium` share) is itself the
measure of whether 10 minutes is short enough; if it stays above ~15% on liquid names the cadence goes to 5
minutes (Plus) or the traded set is re-sampled mid-tick for the top names.

### 5.4 `classify_print(price, prev_quote, next_quote, edge=0.10, max_age_sec=900)` → `(side, reason)`
- For each available bracket quote with `ask ≥ bid > 0` and age ≤ `max_age_sec`: `edge_$ = edge × (ask − bid)`;
  `BUY` if `price ≥ ask − edge_$`; `SELL` if `price ≤ bid + edge_$`; else `MID`. A crossed or missing quote is
  `ABSENT`.
- Both `BUY` → `BUY (both)`; both `SELL` → `SELL (both)`; one `BUY`/`SELL` and the other `MID` or `ABSENT` →
  that side `(one)`; `BUY` vs `SELL` → `UNKNOWN (conflict)`; both `MID` → `UNKNOWN (mid)`; both `ABSENT` →
  `UNKNOWN (no_quote)`.
- Same `edge` as today (`aggressor_edge`, `uoa_screener.py:812`) so the only thing that changes is the quote.
  The function is pure and unit-tested on fixed vectors (§5.10).

### 5.5 Nightly merge (`run_uoa_nightly`, replacing the per-contract call at `uoa_screener.py:1600`)
The nightly keeps fetching the full day's prints (its `premium_total`, `trade_count`, top prints and every
other column are unchanged). For each selected contract it then reads the day's `uoa_contract_intraday`
buckets and computes `coverage = intraday.trade_count / nightly.trade_count`.
- `coverage ≥ 0.90` → `buy_premium = Σ bucket.buy`, `sell_premium = Σ bucket.sell`,
  `unknown_premium = premium_total − buy − sell` (so the three always reconcile to the nightly total; the
  uncovered remainder is unknown, never guessed). `aggressor_source = 'quote_at_trade'`.
- `coverage < 0.90` (sampler outage, symbol not in the intraday universe, contract outside the ±12% band) →
  today's closing-quote rule, `aggressor_source = 'closing_quote'`. Same numbers as today, honestly labelled.
- No prints → `'none'`.
New columns: `uoa_contract_daily.aggressor_source` (text), `.aggressor_coverage` (float);
`uoa_symbol_daily.aggressor_qat_share` (share of the symbol's classified premium that came from
`quote_at_trade`). `dir_ratio`, `call_buy_premium`, `put_buy_premium`, `net_directional_premium` and the flow
scores follow automatically from the new `buy_premium` (`:1663-1668`). `stats_json` gains an `aggressor`
block: contracts by source, premium by source, median coverage, sessions' tick count.

### 5.6 Consumers
- **Omega `get_option_trades`** (`option_trades_summary.py`): add `buy_premium_usd`, `sell_premium_usd`,
  `unknown_premium_usd` and `side_source` to the per-contract and per-expiry tables **read from
  `uoa_contract_intraday`** for the requested window (joined on contract and bucket), and a `side` column on the
  largest prints when the print is in a bucket's `top_prints_json`. Never inferred against the current quote.
  Window older than the retained buckets → columns null with `side_source = 'unavailable'`.
- **Live view (internal, Haci only).** `GET /api/admin/uoa/intraday?date=&window_min=30|60|day`: per
  underlying, call and put buy-side and sell-side premium over the window, net buy-side premium
  `(call_buy − call_sell) − (put_buy − put_sell)`, conflict and no-quote shares, tick freshness; expandable to
  contract buckets and top prints with sides. Admin route, no subscriber copy (DP-48 internal tool). A
  subscriber-facing live UOA page is a separate EN gated on a research question (does intraday buy-side flow
  predict the close or next session? — to BACKLOG as a hypothesis once 20 sessions of buckets exist).
- **UOA UI "conviction"** (`routers/uoa_screener.py:465`) and **Whale Watch** read `buy_premium` as before and
  therefore improve on the ship date without code change; the Whale Watch qualification query should add
  `aggressor_source = 'quote_at_trade'` to its filter so the 0.65 ask-share gate is only applied to labels
  that mean something (one-line change, `services/whale_watch_tracking.py:114-116`).

### 5.7 What it does *not* do
It does not rewrite any historical row (`manifest_v001` keeps the artefact; the ship date is logged in
`DATA_NOTES.md` and Q014 / Q019 / Q029 / Q030 split there under DP-50 — the same split PI-020 already caused,
so if both ship within days the desk records one split window, not two). It does not change SAS weights,
thresholds or the polarity flag (PI-014 owns that). It does not publish anything to subscribers.

### 5.8 Phase 2 (optional, decided by the desk after 20 sessions of Phase 1)
Delta-adjusted closing-quote classifier for history: `mid_t ≈ mid_close − Δ_close × (S_close − S_t)` with the
closing spread, `S_t` from the underlying's minute bars. Phase 1's `quote_at_trade` labels are the truth set to
measure its agreement rate; if ≥ 85% on the covered prints, a backfill of 2026 (prints re-fetched from Alpaca,
which holds them from February 2024) becomes a separate PI-023 repair brief with its own DATA_NOTES entry.
Not before.

### 5.9 Numbers that change on the ship date (named, as DP-59 asks)
`uoa_contract_daily.buy_premium / sell_premium / unknown_premium` for covered contracts;
`uoa_symbol_daily.call_buy_premium / put_buy_premium / net_directional_premium / dir_ratio`, `bull_dir` /
`bear_dir`, the three flow scores and labels; the SAS flow vote (`uoa_dir_ratio` source) and, if PI-014 turns
polarity on, the polarity; Whale Watch qualification; the UOA "conviction" column; Omega's tables gain side
columns. Expected direction: the tape correlation of §2 collapses toward zero; the classified share
(`1 − unknown`) may fall at first because conflicts become unknown instead of being forced.

### 5.10 Tests (standalone runner, no `pytest` — PI-021)
`classify_print` vectors (both/one/conflict/mid/no-quote/crossed/aged-out; edge exactly at the boundary); traded-set
selection from two snapshot maps (volume up, unchanged, new contract, disappeared contract); bucket aggregation
and idempotent replace; nightly merge reconciliation `buy + sell + unknown == premium_total` on every row and
the coverage fallback with its label; retention deletes only rows older than the cut; the Omega table gains
side columns only from stored buckets. Fixtures are literal dicts; no network, no database.

### 5.11 After-deploy check (Data Steward, read-only, `/desk-run verify EN-020 <sha>`)
W1. `uoa_runs` shows ≥ 36 `intraday_tick` rows per session for three consecutive sessions, each with
    `status = 'success'` and a 429 count that did not grow tick over tick.
W2. On those sessions ≥ 80% of `uoa_contract_daily` premium carries `aggressor_source = 'quote_at_trade'`,
    and `buy + sell + unknown = premium_total` on every row (tolerance 1 cent).
W3. `drift_test.py` restricted to post-ship sessions: after 20 sessions, |Spearman| of call buy-share vs SPY
    open-to-close < 0.20 (it is −0.57 today). Descriptive pass/fail; the steward reports the number either way.
W4. Conflict share of premium per session, and its top-20 liquid-name value; > 15% for five sessions →
    a cadence note back to Haci, not a failure.
W5. Omega: one `get_option_trades` call on a liquid name for a completed window returns side columns with
    `side_source = 'quote_at_trade'`.
W6. `DATA_NOTES.md` entry written with ship SHA and first covered session; Q014 / Q019 / Q029 / Q030 split noted.

### 5.12 Open items for Haci (answer in the brief request, not blockers)
1. Which Alpaca plan is live (Basic or Algo Trader Plus) and whether `ALPACA_OPTION_FEED` is set — decides the
   trade-fetch lag (2 ticks vs 1) and whether 5-minute cadence is on the table. The stored `last_trade_ts` shows
   the nightly is not hurt by the 15-minute hold-back today because it starts after 16:43.
2. Whether the live view should sit in the existing UOA tab (admin-only panel) or a new admin route.

## 6. Two things seen in passing
- `uoa_runs` has a `nightly` row dated **2026-12-09** in state `running` (started 10:03 ET) and one for the
  Labor Day holiday 2026-09-07 (22:30, never finished). Harmless to the data; the first looks like a manual run
  with a mistyped date. Noted for the PI-002 watchdog.
- PI-020 shipped in the platform as `3f1d3e6` (PR #31) with Omega's table tool `d112d37`; the desk's register
  still says BRIEF_WRITTEN. `/desk-run verify PI-020 3f1d3e6` is due after the first nightly that runs it.

## Files
`counts.py` (book size, unknown share, latest run stats) · `drift_test.py` + `drift_test_daily.csv` (§2) ·
`timing.py` (nightly start times, last print seen).
