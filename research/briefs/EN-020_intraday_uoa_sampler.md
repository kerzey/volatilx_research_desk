# EN-020 — intraday UOA sampler: option buy/sell side from the quote at trade time

**Type:** enhancement brief, **plumbing** kind — and it is the whole of the PI-023 fix.
**Ships directly under DP-59** (`research/DECISION_POLICY.md:37`): no feature flag, no kill switch, no shadow
mode, no inertness proof, no flip step returned to Haci. The build is **always-on once deployed**; it is checked
*here*, in the registers, by the Data Steward after deploy (§4.2, §8).
**Register row:** `research/ENHANCEMENTS.md` EN-020, Build = `HACI_DECIDED:build (2026-09-15)`; asked for at
`/desk-run prompt EN-020` on 2026-09-15 (DP-48: asking is the decision).
**Closes:** `research/PLATFORM_ISSUES.md` PI-023 (buy/sell label judged against the closing quote). **There is no
separate PI-023 fix brief and there will not be one** — Alpaca keeps no historical option quotes, so the only way
to label a print correctly is to have captured the quote while the day ran. PI-023 closes when **Phase A** passes
the Data Steward's W1–W3 (§8).
**Depends on:** PI-020 (paginated `/trades`), already deployed at `3f1d3e6`; the sampler's trade fetch calls the
paginated `get_option_trades`.
**Blocks:** PI-014 (Conviction Monitor polarity arm) — **PI-014 must ship after Phase A**, see §0.2.
**Platform repo:** `C:\Users\sahin\Projects\volatilx`. Two PRs, in this order:
  * **PR 1 — Phase A**, branch `feat/en-020a-intraday-uoa-sampler`
  * **PR 2 — Phase B**, branch `feat/en-020b-uoa-widenet-live-tab` (cut from `main` after PR 1 is merged)
**Platform SHA all `path:line` citations are taken at:** `d112d37c61b971d3c530b0ddb0566913a8324e8f` (`d112d37`,
"Omega get_option_trades returns tables, not raw prints"). Every line cited here was re-read at that SHA while
this brief was written; where the design report `research/reports/uoa_side_2026-09-15/REPORT.md` cites a line
that has moved or a fact that does not hold in the code, this brief carries the corrected version and says so
(§0.3).
**Research repo SHA:** `dd54241`.
**Haci, 2026-09-15, after the first draft of this brief — two decisions that override the design report §5.13:**
(1) **no admin gate.** Haci is the platform's only user, so the "UOA live" tab is rendered on the AI Picks page
for every signed-in user, with the same sign-in check the other AI Picks routes use and nothing more: no
`ADMIN_TOKEN`, no `X-Admin-Token`, no `ADMIN_EMAIL`, no `is_admin` context flag. (2) **The feed is OPRA in
production. Take it as given; do not verify it.** Cadence 5 minutes, trade-fetch lag one tick, are the fixed
defaults. The feed value is still written on every tick row, as a record, not a check.
**Runtime settings — sizing and thresholds only, never gates** (read from the environment at call time, clamped;
every one of them leaves a runnable job): §3.11 lists them with defaults and clamps. There is **no**
`UOA_INTRADAY_ENABLED`, no `UOA_WIDENET_ENABLED`, and no `..._ENABLED` name anywhere in this build; §4.1(d)
greps for the pattern and must find nothing in the new files.

**What ships, in one paragraph.** Phase A adds an intraday sampler: a triggered WebJob that runs every five
minutes on NYSE sessions from a quote-only seed tick at 09:30 to ten minutes past the close, takes a chain
snapshot per underlying in the night's UOA universe (±12% of spot, ≤ 180 DTE, its own 12-page bound with any
truncation recorded), writes one atomic `uoa_quote_tick` row per sampled contract carrying *this* tick's quote
and the previous tick's quote, fetches the prints of the contracts whose day volume rose in the interval that
ended one tick ago, and labels each print with a pure `classify_print` against the two quotes that bracket it —
the previous quote alone may decide, the next quote alone may not, conflicts and fast markets are unknown. The
labelled prints are summed into `uoa_contract_intraday` buckets; the 16:43 nightly then sums the buckets for
each selected contract instead of comparing every print of the day with the closing quote, and premium the
sampler did not cover is **unknown**, never guessed: there is no closing-quote fallback. `dir_ratio` is NULL on
any symbol whose classified share is below 0.50, so SAS's legacy flow vote abstains rather than re-read the
artefact through a half-labelled symbol. Omega's `get_option_trades` gains side columns with a `side_source`,
populated only where the buckets cover ≥ 80% of the contract's own fetched premium. Phase B adds the Tier-2 wide
net — a 15-minute, snapshot-only sweep over every US name ≥ $2B that flags big and unusual orders from
`dailyBar v × vw` without fetching a single print, promotes a flagged name into Tier 1 and into that night's UOA
universe, and feeds a **"UOA live" tab** under AI Picks (no admin gate: Haci is the platform's only user). No
historical row is rewritten by either phase.

---

## 0. Before you start

### 0.1 DP-49 — nothing in this brief runs against a database

Your `DATABASE_URL` is the platform's **read-write** role on **live production**. The research desk's
`$RESEARCH_DB_URL` is a read-only role on the *same* Postgres instance; there is no copy. Therefore:

- **Do not run `pytest` in this repo, ever.** `conftest.py:31-35` calls `create_tables()` (DDL) and the autouse
  fixture at `conftest.py:38-55` runs `db.query(UserActivityEvent).delete()` and `db.query(User).delete()`
  before and after **every test**, against whatever `DATABASE_URL` names (PI-021). Run the §5 tests as
  `python tests/test_uoa_intraday_sampler.py` (and `python tests/test_uoa_widenet.py` in Phase B) with
  `DATABASE_URL` **unset**; those files load no conftest and import no database module.
- **Do not run `scripts/run_uoa_intraday_tick.py` in its normal mode**, do not run any other `scripts/run_uoa_*`
  script, do not run the nightly pipeline, and do not start the app. The only execution of the new script you
  may perform is the offline one of §3.10: `python scripts/run_uoa_intraday_tick.py --offline-fixture
  tests/_fixtures/en020_tick.json`, which parses its own flag **before** importing anything else, imports only
  the standard library and the pure `services.uoa_intraday_classify` module, opens no connection and writes
  nothing. §5 test T14 asserts that path leaves `db`, `models` and `sqlalchemy` out of `sys.modules`.
- **You create no table and run no migration.** New tables arrive through `Base.metadata.create_all` inside
  `create_tables()` (`db.py:47-52`), which the sampler script calls at its own start exactly as
  `services/uoa_scheduler.py:94` does; new *columns* on existing tables arrive through the lightweight
  `_ensure_columns` block (`db.py:54-127`), to which you add the five column entries named in §3.6(c). Both run inside the
  platform's own jobs in production. That is application code the platform executes, not a database step handed
  to you.
- **You do not touch the research repo.** `research/lib/freeze_config.json` lives in the desk repo
  (`C:\Users\sahin\OneDrive\Desktop\VolatilX_Research_Desk`); the Data Steward adds the `uoa_quote_tick` and
  `uoa_contract_intraday` availability entries at verify time (§8). Nothing under `research/` is yours.

§4.2 and §8 are the Data Steward's (read-only role) and Haci's (deploy). §4.1 and §5 are yours, and both are
satisfiable from this repository alone.

### 0.2 DP-50 — ship timing, checked before this brief was written

Checked against the locked questions on `research/BOARD.md` and `research/lib/desk_queue.py` on 2026-09-15.

- **Numbers change from the first covered session.** This build is forward-only — it rewrites **no historical
  row** — but from the first session on which the sampler runs and the merged nightly consumes its buckets,
  these stored values change meaning: `uoa_contract_daily.buy_premium / sell_premium / unknown_premium`;
  `uoa_symbol_daily.call_buy_premium / put_buy_premium / dir_ratio` (NULL below the classified-share threshold),
  `bull_dir` / `bear_dir` and therefore `score_day / score_swing / score_long`, `bias_*` and `label_*`; the SAS
  flow vote (`services/super_agent_select_scoring.py:555-560` abstains when `dir_ratio` is NULL); Whale Watch
  qualification (`services/whale_watch_tracking.py:122-123`, `routers/whale_watch.py:153-159`); the UOA
  "conviction" column (`routers/uoa_screener.py:465-474`); Omega's option-trade tables gain side columns.
- **Locked questions split at the ship date.** **Q014, Q019, Q029 and Q030** read `uoa_contract_daily` /
  `uoa_symbol_daily` or the SAS output built from them. Under DP-50(a) each treats the aggressor columns as two
  different features either side of the first covered session. The desk logs the ship SHA, the first covered
  session and the per-session classified share in `research/data/DATA_NOTES.md` (§8, exact text given there).
  Under DP-59 this does not delay the ship; it is a record, not a gate.
- **No repair-log row.** `research/data/DATA_NOTES.md:32-33`: a forward-only change takes no row in the repair
  log, because no value already written is overwritten. The ship-log entry of §8 is written instead.
- **PI-014 must ship after Phase A.** The Conviction Monitor's polarity arm computes polarity from
  `uoa_contract_daily.buy_premium / sell_premium` (`services/conviction_monitor_service.py:891-903`, feeding
  SAS's `_compute_flow_polarity`), the exact field PI-023 indicts, and PI-014's fix *wakes* that arm — it has
  printed `polarity_unavailable_coverage_low` on every row since 2026-05-19
  (`services/conviction_monitor_service.py:184`). Shipped before Phase A, the arm fires HOLD and EXIT off a
  label that tracks the day's drift, and Q019's re-measured rate and Q038's re-entry are set on contaminated
  nights. Shipped after, uncovered premium is `unknown`, so the arm's own 0.5 coverage gate abstains honestly.
  If you are handed the PI-014 brief and this one at the same time, do Phase A first.

### 0.3 Where this brief corrects the design report

The design is `research/reports/uoa_side_2026-09-15/REPORT.md` §5 (v2 after Red Team; §5.13 Haci's answers,
§5.14 the wide net, §5.15 the build order). You do not need to open it — this brief is self-contained. Five
points where the code at `d112d37` does not match the report, and this brief wins:

1. **Tick status rows cannot go in `uoa_runs`.** `models.py:390` declares
   `UniqueConstraint("run_type", "trading_date", name="uq_uoa_runs_type_date")`, so a session cannot hold ~40
   rows of `run_type='intraday_tick'`. Per-tick status goes in a new table **`uoa_intraday_run`** (§3.4); one
   summary row per session is still upserted into `uoa_runs` with `run_type='intraday_sampler'` (§3.4).
2. **The snapshot page bound is already an env var.** `_MAX_SNAPSHOT_PAGES = int(os.getenv(
   "ALPACA_OPTION_SNAPSHOT_PAGES", "5"))` (`ai_agents/options_client.py:33`). Do **not** raise that default —
   it would change the nightly too. Add an explicit `max_pages` keyword to `get_snapshots` and
   `_fetch_underlying_snapshots` defaulting to `_MAX_SNAPSHOT_PAGES`, and have the sampler pass 12 (§3.3).
3. **The client already surfaces truncation.** `_fetch_underlying_snapshots` returns
   `{"snapshots": …, "next_page_token": next_token}` (`ai_agents/options_client.py:921`) and so does
   `get_snapshots(underlying_symbol=…)` (`:828-839`); it is the *caller* that drops it. The sampler must record
   a non-null leftover token as coverage loss (§3.3), and must also record `pages`, which the client does not
   return today — add `"pages": pages` to that return dict.
4. **`net_directional_premium` carries no aggressor artefact.** It is written as
   `call_premium_total − put_premium_total` (`services/uoa_screener.py:1883-1884`), not from buy premium.
   Leave it exactly as it is; do **not** NULL it. Only `dir_ratio` is nulled (§3.6).
5. **`aggressor_edge` and the spread gate are config fields, not literals.** `UoaConfig.aggressor_edge = 0.10`
   (`services/uoa_screener.py:812`), `UoaConfig.max_relative_spread = 0.25` (`:801`). `classify_print` takes
   them as arguments with those defaults, so the only thing that changes is the quote.

### 0.4 Indentation

`models.py`, `services/uoa_screener.py`, `services/uoa_scheduler.py`, `services/conviction_monitor_service.py`
and `routers/uoa_screener.py` are **tab**-indented. `db.py`, `ai_agents/options_client.py`,
`ai_agents/option_trades_summary.py`, `ai_agents/omega_agent.py`, `services/whale_watch_tracking.py`,
`services/symbol_context_builder.py`, `services/super_agent_select_scoring.py`, the `routers/admin_*.py`
modules, `scripts/` and `tests/` are **4-space** indented. Match the file you are editing; new files under
`services/`, `scripts/`, `routers/` and `tests/` use 4 spaces, new `models.py` classes use tabs.

---

## 1. What is missing, and the evidence

The platform has no record of what an option's quote was when a print happened, so it labels every print of the
session against the **closing** quote. The label is therefore mostly a record of where the option's price went
after the trade.

- **The stored quote is the closing snapshot's.** `services/uoa_screener.py:1114-1116` keeps
  `latest_quote.bp / .ap` from the chain snapshot taken during the nightly (16:43–17:04 ET) and stores it as the
  contract's `bid` / `ask`.
- **Every print of 09:30–16:00 is compared with it.** `services/uoa_screener.py:1246-1255`:
  `edge = config.aggressor_edge * spread`; `price ≥ ask − edge → buy_premium`, `price ≤ bid + edge →
  sell_premium`, else `unknown_premium`, with `bid`/`ask` handed in from the closing snapshot at `:1599`.
- **Measured, 170 sessions 2026-01-07..2026-09-14:** the daily call buy-share runs *against* the tape (Spearman
  −0.566 with SPY's open-to-close move) and the put buy-share *with* it (+0.533). Up days: 42.9% of call premium
  "bought", 59.8% of put premium "bought". Down days: 62.4% / 41.2%.
- **The placebo settles that it is an artefact, not behaviour** (Red Team, 457,135 prints from `top_trades_json`,
  73 sessions 2026-06-01..2026-09-14, re-classified with the platform's own rule): for prints in the last 30
  minutes — where the closing quote *is* the quote at trade time — ρ is −0.03 / −0.02; for prints more than
  three hours before the close, in the **same contracts on the same days** (114,619 prints), ρ is −0.577 /
  +0.455. A gradient with a zero at the close is the artefact's signature and nothing else's.
- **Who consumes it:** `dir_ratio` (`services/uoa_screener.py:1663-1668`), the SAS flow vote at weight 1.3
  (`services/super_agent_select_scoring.py:555-560`), the polarity path's four buckets
  (`services/symbol_context_builder.py:136-174`), Whale Watch qualification (classified fraction ≥ 0.50 **and**
  ask-share ≥ 0.65, in two places: `services/whale_watch_tracking.py:113-123` and the inline query
  `routers/whale_watch.py:153-159`), and the UOA UI's "conviction" column (`routers/uoa_screener.py:465-474`).
- 23–35% of nightly premium is already `unknown` under the closing rule; of the classified part 47–59% is "buy".

**Reproducing query — Data Steward only, read-only role on `$RESEARCH_DB_URL`.** Not for the coding agent.

```sql
-- PI-023: the daily classified buy-share series. The SPY open-to-close join and the
-- Spearman are done in the desk script (research/reports/uoa_side_2026-09-15/drift_test.py).
SELECT c.trading_date,
       SUM(CASE WHEN c.option_type = 'call' THEN COALESCE(c.buy_premium, 0) ELSE 0 END)  AS call_buy,
       SUM(CASE WHEN c.option_type = 'call' THEN COALESCE(c.sell_premium, 0) ELSE 0 END) AS call_sell,
       SUM(CASE WHEN c.option_type = 'put'  THEN COALESCE(c.buy_premium, 0) ELSE 0 END)  AS put_buy,
       SUM(CASE WHEN c.option_type = 'put'  THEN COALESCE(c.sell_premium, 0) ELSE 0 END) AS put_sell,
       SUM(COALESCE(c.buy_premium,0) + COALESCE(c.sell_premium,0))
         / NULLIF(SUM(c.premium_total), 0)                                               AS classified_share
FROM uoa_contract_daily c
WHERE c.trading_date BETWEEN DATE '2026-01-07' AND DATE '2026-09-14'
GROUP BY c.trading_date
ORDER BY c.trading_date;
```

## 2. Cause — the code path

| # | Where | What it does |
|---|---|---|
| 1 | `services/uoa_screener.py:1086-1190` (`_pick_contracts`) | Selects ≤ 60 contracts per symbol (`:799`) within ±10% of spot (`:800`), ≤ 180 DTE, OI ≥ 50, snapshot volume ≥ 10, relative spread ≤ 25% (`:801`, `:1124`) — and at `:1114-1116` keeps the **closing** snapshot's `bid`/`ask` as the contract's quote. |
| 2 | `services/uoa_screener.py:1558-1571` | Fetches every print of the 09:30–16:00 session (`_session_window_utc`, `:908-911`; window resolved at `:1450`) through the paginated `get_option_trades` (`ai_agents/options_client.py:986-1087`, PI-020). Only `p`, `s`, `t` are read downstream; condition and exchange codes are discarded. |
| 3 | `services/uoa_screener.py:1599` → `_aggregate_trades_for_contract` (`:1192-1272`) | Passes `bid=meta["bid"], ask=meta["ask"]` — the closing quote — into the classifier at `:1246-1255`. **This is the defect.** |
| 4 | `services/uoa_screener.py:1663-1668` | `dir_ratio = (call_buy − put_buy) / (call_buy + put_buy + 1)` → `bull_dir` / `bear_dir`, which multiply every bucket score at `:1854-1862`. |
| 5 | `ai_agents/options_client.py:868-921` | The only way to get a contract's quote *now* is a chain snapshot; Alpaca exposes no historical option quotes at all, so nothing after the fact can repair step 3. |

The fix is therefore not a change to step 3's arithmetic. It is a second data path that captures the quote while
the session runs, and a step 3 that reads it.

---

# PR 1 — PHASE A: the sampler, the classifier and the nightly merge

This is the PI-023 fix. Nothing in it is subscriber-visible. Merge and deploy it before PR 2 and before PI-014.

## 3. Change — Phase A

### 3.1 New module layout

| File | Kind | Contents |
|---|---|---|
| `services/uoa_intraday_classify.py` | **new, pure** | `classify_print`, the reason constants, the bucket aggregator. Standard library only: no network, no database, no imports from `db`/`models`. |
| `services/uoa_intraday_sampler.py` | new | One tick: universe, snapshots, tick rows, traded set, lagged trade fetch, bucket upsert, status rows, retention. |
| `scripts/run_uoa_intraday_tick.py` | new | WebJob entry point; `create_tables()` then one tick. Also the offline `--offline-fixture` path (§3.10). |
| `app_data/jobs/triggered/uoa_intraday_sampler/run.py` | new | Copy of `app_data/jobs/triggered/fixed_universe_report_batch/run.py` with `script_name = "run_uoa_intraday_tick.py"` (that file's `_resolve_repo_root` / `_resolve_python_executable` bootstrap, lines 9-89, is the house pattern). |
| `app_data/jobs/triggered/uoa_intraday_sampler/settings.job` | new | `{"schedule": "0 */5 9-16 * * 1-5", "is_singleton": true, "stopping_wait_time": 60, "shutdownGraceTimeLimit": 280}` |
| `models.py` | edit | `UoaQuoteTick`, `UoaContractIntraday`, `UoaIntradayRun` (§3.2, §3.4). Tabs. |
| `db.py` | edit | Four `_ensure_columns` entries (§3.6). |
| `ai_agents/options_client.py` | edit | `max_pages` keyword and `pages` in the return dict (§3.3). |
| `services/uoa_screener.py` | edit | The nightly merge at `:1599` and the symbol roll-up at `:1663-1668` (§3.6). |
| `ai_agents/option_trades_summary.py`, `ai_agents/omega_agent.py` | edit | Side columns with `side_source` (§3.7). |
| `routers/uoa_screener.py` | edit | Coverage beside conviction (§3.8). |
| `tests/test_uoa_intraday_sampler.py`, `tests/_fixtures/en020_tick.json` | new | §5. |
| `docs/UOA_INTRADAY_SAMPLER.md`, `docs/AZURE_WEBJOBS_AUTOMATION.md` | new / edit | §6. |

### 3.2 Schemas — the two data tables (`models.py`, tab-indented)

```python
class UoaQuoteTick(TimestampMixin, Base):
	"""One row per sampled contract per tick: this tick's quote and the previous tick's,
	written together in one upsert so a bracket is never assembled across transactions."""

	__tablename__ = "uoa_quote_tick"
	__table_args__ = (
		UniqueConstraint("trading_date", "contract_symbol", "tick_seq", name="uq_uoa_quote_tick_pk"),
		Index("ix_uoa_quote_tick_date_contract", "trading_date", "contract_symbol"),
		Index("ix_uoa_quote_tick_date_seq", "trading_date", "tick_seq"),
	)

	id = Column(Integer, primary_key=True, index=True)
	trading_date = Column(Date, nullable=False, index=True)
	underlying_symbol = Column(String(24), nullable=False, index=True)
	contract_symbol = Column(String(64), nullable=False, index=True)

	tick_seq = Column(Integer, nullable=False)            # 0 = the 09:30 quote-only seed tick
	tick_ts = Column(DateTime(timezone=True), nullable=False)
	quote_ts = Column(DateTime(timezone=True), nullable=True)
	bid = Column(Float, nullable=True)
	ask = Column(Float, nullable=True)
	bid_size = Column(Float, nullable=True)
	ask_size = Column(Float, nullable=True)
	day_volume = Column(Float, nullable=True)             # dailyBar.v, cumulative
	day_vwap = Column(Float, nullable=True)               # dailyBar.vw
	feed = Column(String(16), nullable=True)              # "opra" | "indicative"

	prev_tick_seq = Column(Integer, nullable=True)
	prev_tick_ts = Column(DateTime(timezone=True), nullable=True)
	prev_quote_ts = Column(DateTime(timezone=True), nullable=True)
	prev_bid = Column(Float, nullable=True)
	prev_ask = Column(Float, nullable=True)
	prev_bid_size = Column(Float, nullable=True)
	prev_ask_size = Column(Float, nullable=True)
	prev_day_volume = Column(Float, nullable=True)

	sticky = Column(Boolean, nullable=False, default=False)   # sampled because it is in the sticky set
	raw_quote_json = Column(Text, nullable=True)              # the snapshot entry verbatim

class UoaContractIntraday(TimestampMixin, Base):
	"""One row per (trading_date, contract, bucket_start): the labelled prints of one interval."""

	__tablename__ = "uoa_contract_intraday"
	__table_args__ = (
		UniqueConstraint("trading_date", "contract_symbol", "bucket_start", name="uq_uoa_contract_intraday_pk"),
		Index("ix_uoa_contract_intraday_date_underlying", "trading_date", "underlying_symbol"),
	)

	id = Column(Integer, primary_key=True, index=True)
	trading_date = Column(Date, nullable=False, index=True)
	underlying_symbol = Column(String(24), nullable=False, index=True)
	contract_symbol = Column(String(64), nullable=False, index=True)
	option_type = Column(String(8), nullable=False)
	expiration_date = Column(Date, nullable=True)
	strike_price = Column(Float, nullable=True)

	bucket_start = Column(DateTime(timezone=True), nullable=False)
	bucket_end = Column(DateTime(timezone=True), nullable=False)

	trade_count = Column(Integer, nullable=False, default=0)
	volume = Column(Float, nullable=False, default=0.0)
	premium_total = Column(Float, nullable=False, default=0.0)
	buy_premium = Column(Float, nullable=False, default=0.0)
	sell_premium = Column(Float, nullable=False, default=0.0)
	unknown_premium = Column(Float, nullable=False, default=0.0)
	buy_count = Column(Integer, nullable=False, default=0)
	sell_count = Column(Integer, nullable=False, default=0)
	unknown_count = Column(Integer, nullable=False, default=0)

	reason_premium_json = Column(Text, nullable=True)     # {"both":…, "one_prev":…, "one_next":…, "conflict":…,
	                                                      #  "fast_market":…, "mid":…, "no_quote":…, "pre_open":…,
	                                                      #  "wide_spread":…, "widenet_bracket":…, "not_sampled":…}
	multileg_premium = Column(Float, nullable=False, default=0.0)
	oversize_premium = Column(Float, nullable=False, default=0.0)
	quote_age_median_sec = Column(Float, nullable=True)
	relative_spread_median = Column(Float, nullable=True)
	edge_ratio_hist_json = Column(Text, nullable=True)    # 10 bins of (price − mid) / (spread / 2)
	top_prints_json = Column(Text, nullable=True)         # <= 5 largest: price, size, premium, side, reason,
	                                                      # bid/ask used, quote age, conditions, exchange, ts
	side_source = Column(String(16), nullable=False, default="quote_at_trade")  # or "widenet_bracket" (Phase B)
	feed = Column(String(16), nullable=True)
```

`reason_premium_json` must always reconcile: the sum of its values equals `premium_total`, and
`buy_premium + sell_premium + unknown_premium == premium_total` to one cent. Only the reasons `both` and
`one_prev` contribute to `buy_premium` / `sell_premium`; **every other reason is unknown premium**, including
`one_next`.

### 3.3 One tick (`services/uoa_intraday_sampler.py::run_tick`)

Signature: `run_tick(db, *, now_utc=None, config=None) -> Dict[str, Any]`. Steps, in order:

1. **Calendar and window gate.** The session must be an NYSE trading day: use the XNYS calendar the way
   `services/whale_watch_tracking.py:58-65` does (`exchange_calendars.get_calendar("XNYS")`, falling back to
   `core.trading_days.is_trading_day`, `core/trading_days.py:69`). **Do not reuse the `_is_weekday` guard of
   `services/uoa_scheduler.py:100`** — it let a Labor Day run start. Resolve the session's close from the
   calendar, so an early close ends at 13:00 and the last tick is 13:10. Ticks run from 09:30:00 ET to
   `close + UOA_INTRADAY_CLOSE_BUFFER_MIN` (10). Outside that range the script exits `{"status":
   "outside_window"}` having written nothing; the cron fires more often than the window, and that is expected.
2. **Tick identity.** `tick_seq` = the number of whole cadence intervals since 09:30 (so 09:30 → 0, 09:35 → 1
   under the 5-minute default). `tick_seq == 0` is the **quote-only seed tick**: it takes snapshots and writes
   `uoa_quote_tick` rows, and fetches no prints, so the 09:30–09:35 interval already has a prior bracket.
3. **Universe** (Tier 1) = the nightly UOA universe (`_resolve_universe(db, cfg)`,
   `services/uoa_screener.py:1043-1066`, the S&P 500 list at `services/uoa_screener.py:786`) ∪ last night's SAS
   candidates (`super_agent_select_candidates_daily` for the most recent run date) ∪ the EN-019 20-name liquid
   list ∪ `UserFavoriteSymbol` symbols (`models.py:164`) ∪ `SPY`, `QQQ`, `IWM` ∪ today's Phase-B promotions
   (Phase B only) ∪ today's searched tickers (§3.9). Deduplicate, sort, cap at
   `UOA_INTRADAY_MAX_UNDERLYINGS` (800). The universe is resolved once per tick and recorded in the tick row.
4. **Spot** per underlying from the multi-symbol stock snapshot, `GET {ALPACA_STOCK_API_BASE}/v2/stocks/snapshots
   ?symbols=…` in batches of 100 with the `_auth_headers()` pattern of `services/whale_watch_tracking.py:91-97`
   and `feed=ALPACA_STOCK_FEED` (`:54`). A symbol with no spot is skipped for the tick and counted.
5. **Chain snapshot** per underlying: `options_client.get_snapshots(underlying_symbol=sym, limit=1000,
   expiration_date_lte=(today + 180 days).isoformat(), strike_price_gte=spot × (1 − band),
   strike_price_lte=spot × (1 + band), max_pages=UOA_INTRADAY_SNAPSHOT_PAGES)` with band = 0.12 (two points
   wider than the nightly's 0.10 at `services/uoa_screener.py:800`, because the sampler re-centres each tick).
   **`max_pages` is a new keyword** on `get_snapshots` (`ai_agents/options_client.py:812-839`) and
   `_fetch_underlying_snapshots` (`:868-921`), defaulting to `_MAX_SNAPSHOT_PAGES` so the nightly's behaviour is
   byte-for-byte unchanged; add `"pages": pages` to the `_fetch_underlying_snapshots` return at `:921`. If the
   returned `next_page_token` is not null, the underlying is **truncated**: record
   `{symbol: {"pages": n, "truncated": true}}` in the tick row. Truncation is coverage loss, never silence.
6. **Sampled set** = every in-band contract from the snapshot ∪ the **sticky set**: every contract already
   sampled today for that underlying (`SELECT DISTINCT contract_symbol FROM uoa_quote_tick WHERE trading_date =
   today AND underlying_symbol = sym`) plus last night's selected contracts (`uoa_contract_daily` for the
   previous trading date). Sticky contracts that fell out of the band are fetched with the multi-symbol
   `get_snapshots(contract_symbols=[…])` call (`ai_agents/options_client.py:844-866`, batches of 50) and stored
   with `sticky = True`. A name that gaps 10% keeps its morning coverage.
7. **Atomic tick rows.** For each sampled contract write one `uoa_quote_tick` row carrying this tick's quote
   **and** the previous tick's quote, copied forward from the contract's `tick_seq = current − 1` row (or from
   its most recent earlier row if a tick was missed, provided that row's `quote_ts` is within `max_age_sec`),
   in a **single upsert per contract, one transaction per underlying**. Never read a row in one transaction and
   write the bracket in another. A tick that dies half-way leaves contracts whose newest `tick_seq` is behind;
   step 9 marks the interval degraded and the classifier will read `no_quote` for it, which is the correct
   outcome.
8. **Traded set** = sampled contracts whose `day_volume` is strictly greater than `prev_day_volume`. Only these
   rows survive the next tick's prune (§3.5).
9. **Lagged trade fetch and classification.** With `UOA_INTRADAY_LAG_TICKS = 1` (OPRA in production: no
   15-minute hold-back), tick *k* fetches the prints of the interval `[tick_{k-2}.tick_ts, tick_{k-1}.tick_ts)`
   for the traded set *of that interval*, through `options_client.get_option_trades(contracts,
   start=interval_start_iso, end=interval_end_iso, limit=cfg.trades_limit)` — the paginated PI-020 call, 50
   contracts a request, calls and puts in separate batches, every page read. **Keep each print's condition
   codes (`c`), exchange (`x`) and size (`s`)**; today they are discarded at
   `services/uoa_screener.py:1216-1255`. Each print is labelled by `classify_print` (§3.4) against the bracket
   for its contract: the tick row whose `prev_quote_ts` is the last sample at or before the print and whose own
   `quote_ts` is the first at or after it. A print before the day's first quote sample — including the 09:30:00
   auction print — is `UNKNOWN (pre_open)`. An interval whose tick row is missing or degraded is
   `UNKNOWN (no_quote)`. Under a lag of 2 ticks (Basic feed) the same logic applies one interval further back;
   the setting exists so the lag can be raised without a code change.
10. **Bucket upsert** into `uoa_contract_intraday`, one row per (trading_date, contract, `bucket_start`),
    idempotent: a re-run of the same interval **replaces** the row. `bucket_start` / `bucket_end` are the
    interval's UTC bounds.
11. **Status rows, written last** (§3.4).
12. **Retention**, once per session on the last tick only (§3.5).

**Concurrency and rate.** The tick runs `UOA_INTRADAY_WORKERS` (4) threads over underlyings with a self-imposed
ceiling of `UOA_INTRADAY_MAX_REQUESTS_PER_MIN` (80) requests a minute across all workers, enforced by a shared
token bucket in the sampler. Under Algo Trader Plus (10,000/min) this is a courtesy to the 16:02 Conviction
Monitor and the 16:05 nightly pipeline on the same Alpaca account, not a binding constraint: a tick is
~700–1,000 requests (most names are one snapshot page; SPY 6, QQQ 5) and finishes in well under a minute at the
measured ~1 s a request. `_request` already backs off on 429 (`ai_agents/options_client.py:78-95`); count 429s
in the tick row. The WebJob is a singleton (`settings.job`), so a tick that overruns its cadence makes the next
one skip, which is visible coverage loss and never a wrong label.

### 3.4 `classify_print` — the pure classifier (`services/uoa_intraday_classify.py`)

```python
SIDE_BUY, SIDE_SELL, SIDE_UNKNOWN = "buy", "sell", "unknown"

class ClassifiedPrint(NamedTuple):
    side: str            # SIDE_BUY | SIDE_SELL | SIDE_UNKNOWN
    reason: str          # both | one_prev | one_next | conflict | fast_market | mid |
                         # no_quote | pre_open | wide_spread
    one_next_side: Optional[str]  # the side the next quote alone would have given, recorded, never counted
    edge_ratio: Optional[float]   # (price − mid) / (spread / 2) at the deciding quote
    quote_age_sec: Optional[float]
    bid_used: Optional[float]
    ask_used: Optional[float]
    oversize: bool
    multileg: bool

def classify_print(
    price: float,
    size: float,
    prev_quote: Optional[Mapping[str, Any]],
    next_quote: Optional[Mapping[str, Any]],
    *,
    trade_ts: datetime,
    conditions: Optional[Sequence[str]] = None,
    edge: float = 0.10,              # UoaConfig.aggressor_edge, services/uoa_screener.py:812
    max_age_sec: float = 900.0,
    max_rel_spread: float = 0.25,    # UoaConfig.max_relative_spread, services/uoa_screener.py:801
    pre_open: bool = False,
) -> ClassifiedPrint:
```

A quote mapping is `{"ts": datetime, "bid": float, "ask": float, "bid_size": float, "ask_size": float}`.
The design report writes the signature as `-> (side, reason)`; the NamedTuple is that plus the telemetry the
bucket columns need, and `.side` / `.reason` are its first two fields.

**Rules, applied in this order.**

| # | Condition | Result |
|---|---|---|
| 1 | `pre_open` is true, or there is no quote sample at or before `trade_ts` on the day | `UNKNOWN (pre_open)` |
| 2 | A bracket quote is **usable** iff `ask >= bid > 0`, `abs(trade_ts − quote.ts) <= max_age_sec`, and `(ask − bid) / mid <= max_rel_spread`. A quote failing only the spread test is `ABSENT` with reason token `wide_spread`; a missing/aged/crossed quote is `ABSENT` with token `no_quote`. | — |
| 3 | Both brackets usable **and** `abs(mid_next − mid_prev) > (ask_prev − bid_prev)` | `UNKNOWN (fast_market)` — regardless of agreement |
| 4 | Per usable bracket: `edge_$ = edge × (ask − bid)`; `BUY` if `price >= ask − edge_$`; `SELL` if `price <= bid + edge_$`; else `MID`. Boundaries are inclusive, exactly as `services/uoa_screener.py:1248-1251`. | — |
| 5 | prev `BUY` and next `BUY` | `BUY (both)` |
| 6 | prev `SELL` and next `SELL` | `SELL (both)` |
| 7 | prev `BUY` and next `SELL`, or prev `SELL` and next `BUY` | `UNKNOWN (conflict)` |
| 8 | prev decisive (`BUY`/`SELL`), next `MID` or `ABSENT` | that side, `(one_prev)` — **counted** |
| 9 | prev `MID` or `ABSENT`, next decisive | `UNKNOWN (one_next)`, with `one_next_side` recording the side. **Not counted** as buy or sell until W4 telemetry shows it unbiased. |
| 10 | both `MID` | `UNKNOWN (mid)` |
| 11 | both `ABSENT`, at least one for the spread reason | `UNKNOWN (wide_spread)` |
| 12 | both `ABSENT`, neither for the spread reason | `UNKNOWN (no_quote)` |

Flags, orthogonal to the side: `oversize = size > (ask_size if side is buy else bid_size)` at the deciding
quote — the side stands, the flag is recorded; `multileg = any condition code in the complex-order set` — the
side stands, the flag is recorded, and nothing is excluded on it in v1 (measured first).

**Why the rule is asymmetric.** A quote sampled minutes before a print can be stale if the underlying moved; the
quote *after* can already carry the print's own impact — an aggressive buy lifts the offer, so the post-trade
ask sits above the print and a next-only label would read it as a sale. The previous quote alone may therefore
decide; the next quote alone may not. Disagreement between the two (`conflict`) is the measure of whether the
cadence is short enough and is reported as telemetry (§8 W4).

**Aggregation** (`aggregate_bucket(labelled_prints, …) -> dict`, also pure): sums premium and counts by side and
by reason, median quote age, median relative spread, the 10-bin `edge_ratio` histogram, `multileg_premium`,
`oversize_premium` and the ≤ 5 largest prints with side, reason, the bid/ask used, the quote age and the
condition codes. Premium is `price × size × 100`, the platform's convention
(`ai_agents/option_trades_summary.py:130`).

**Status rows.** Per tick, one `uoa_intraday_run` row, written **last**:

```python
class UoaIntradayRun(TimestampMixin, Base):
	"""One row per sampler tick. uoa_runs cannot hold these: uq_uoa_runs_type_date (models.py:390)
	allows one row per (run_type, trading_date)."""

	__tablename__ = "uoa_intraday_run"
	__table_args__ = (UniqueConstraint("trading_date", "tick_seq", name="uq_uoa_intraday_run_pk"),)

	id = Column(Integer, primary_key=True, index=True)
	trading_date = Column(Date, nullable=False, index=True)
	tick_seq = Column(Integer, nullable=False)
	tick_ts = Column(DateTime(timezone=True), nullable=False)
	started_at = Column(DateTime(timezone=True), nullable=False)
	finished_at = Column(DateTime(timezone=True), nullable=True)
	status = Column(String(16), nullable=False, default="ok")     # ok | degraded | failed
	degraded = Column(Boolean, nullable=False, default=False)
	feed = Column(String(16), nullable=True)
	underlyings_sampled = Column(Integer, nullable=False, default=0)
	snapshot_requests = Column(Integer, nullable=False, default=0)
	snapshot_pages = Column(Integer, nullable=False, default=0)
	truncated_underlyings_json = Column(Text, nullable=True)
	contracts_sampled = Column(Integer, nullable=False, default=0)
	traded_set_size = Column(Integer, nullable=False, default=0)
	prints_fetched = Column(Integer, nullable=False, default=0)
	premium_by_reason_json = Column(Text, nullable=True)
	http_429_count = Column(Integer, nullable=False, default=0)
	seconds = Column(Float, nullable=True)
	stats_json = Column(Text, nullable=True)
```

and one **session summary** row upserted into the existing `uoa_runs` (`models.py:386-399`) with
`run_type = 'intraday_sampler'`, `trading_date = today`, `status` `running` until the last tick then `ok`, and
`stats_json` carrying the session rollup (tick count, premium by reason, classified share, truncated
underlyings, feed). One row per session satisfies `uq_uoa_runs_type_date`.

### 3.5 Retention (application code inside the job, DP-49-clean)

On the last tick of a session only, delete **by `trading_date < cutoff` and only from `uoa_quote_tick` and
`uoa_intraday_run`** (quote ticks: `UOA_INTRADAY_QUOTE_TICK_RETENTION_SESSIONS` = 45 trading sessions;
`uoa_contract_intraday` buckets are kept `UOA_INTRADAY_BUCKET_RETENTION_SESSIONS` = 400 sessions, so the labels
behind every bucket's `top_prints_json` stay auditable). Rules: cutoff computed from trading sessions, never
calendar days; **refuse to run** (log and return) if the cutoff falls inside the retention window or if the
estimated row count exceeds `UOA_INTRADAY_RETENTION_MAX_ROWS` (2,000,000); delete in batches of 50,000; record
what was deleted in the session `uoa_runs` row. Never a `DELETE` against any other table.

### 3.6 The nightly merge (`services/uoa_screener.py`)

**Replace the classification, keep everything else.** The nightly still fetches the full day's prints and still
computes `premium_total`, `trade_count`, `premium_max`, `first/last_trade_ts`, `volume_traded` and
`top_trades_json` exactly as it does now. Only the aggressor half changes.

(a) **Per contract, at `services/uoa_screener.py:1599`.** Instead of
`_aggregate_trades_for_contract(rows, bid=meta.get("bid"), ask=meta.get("ask"), config=cfg)` classifying against
the closing quote, call a new `merge_intraday_buckets(db, contract_symbol, trade_date, agg)` that reads the
day's `uoa_contract_intraday` rows for the contract and sets:

```
buy_premium      = Σ bucket.buy_premium
sell_premium     = Σ bucket.sell_premium
unknown_premium  = premium_total − buy_premium − sell_premium        # never negative; clamp at 0 and log
aggressor_coverage_premium = Σ bucket.premium_total / premium_total  # 0.0 when premium_total == 0
aggressor_coverage_count   = Σ bucket.trade_count   / trade_count
aggressor_reason_json      = merged reason→premium map, plus {"uncovered": premium_total − Σ bucket.premium}
aggressor_source           = "quote_at_trade" | "partial" | "unavailable"
```

`_aggregate_trades_for_contract` keeps computing the price/volume aggregates; **delete the closing-quote
classification block at `:1246-1255`** and have it return `buy_premium = sell_premium = None` with
`unknown_premium = premium_total`, which the merge then overwrites from the buckets. **There is no
closing-quote fallback**: a sampler outage makes the day *quiet*, not *wrong*. The three premiums must always
reconcile to `premium_total` within one cent. `UoaConfig.aggressor_proxy_enabled` (`:811`) is deleted along with
its branches — it is dead once the closing-quote path is gone, and leaving it would be a flag.

(b) **Per symbol, at `services/uoa_screener.py:1663-1668`.** Compute
`aggressor_qat_share = Σ contract classified premium / Σ contract premium_total` over the symbol's contracts,
where classified = `both` + `one_prev`. Then:

- `aggressor_qat_share >= UOA_AGGRESSOR_MIN_QAT_SHARE` (0.50, the same threshold SAS's polarity uses at
  `services/super_agent_select_scoring.py:309`): `dir_ratio`, `bull_dir`, `bear_dir` as today, from the new
  `call_buy_prem` / `put_buy_prem`.
- below it: **`dir_ratio = None`**, `bull_dir = bear_dir = 0.5`, and `label_day/swing/long = "FLOW_UNCLASSIFIED"`
  (a new early branch in `_label_for_bucket`, `services/uoa_screener.py:1323-1335`, after the `NOISE` test).
  `dir_ratio=dir_ratio` at `:1885` must stop coercing through `float(payload.get("dir_ratio") or 0.0)` and pass
  `None` through. This closes the re-entry door: the SAS legacy vote at
  `services/super_agent_select_scoring.py:555-560` reads `symbol_daily["dir_ratio"]`, and
  `_direction_from_ratio(None)` returns `None` (`:452-454`), so the vote abstains instead of reading a
  half-labelled symbol. Symbol-level gating is required because `prefetch_flow_polarity` sums across all of a
  symbol's contracts (`services/symbol_context_builder.py:159-174`).
- `net_directional_premium` is **unchanged** (`:1883-1884`; it is `call_premium_total − put_premium_total` and
  carries no aggressor artefact — see §0.3 item 4).
- Write `uoa_symbol_daily.aggressor_qat_share`.
- `stats_json` for the nightly `uoa_runs` row gains an `aggressor` block: premium by reason, median coverage,
  tick count seen, truncated underlyings, feed, and the count of symbols with `dir_ratio` NULL.

(c) **`db.py` `_ensure_columns`** (`db.py:99-127` is the existing pattern):

```python
_ensure_columns(
    "uoa_contract_daily",
    {
        "aggressor_coverage_premium": f"aggressor_coverage_premium {float_type}",
        "aggressor_coverage_count": f"aggressor_coverage_count {float_type}",
        "aggressor_reason_json": "aggressor_reason_json TEXT",
        "aggressor_source": "aggressor_source VARCHAR(16)",
    },
)
_ensure_columns(
    "uoa_symbol_daily",
    {"aggressor_qat_share": f"aggressor_qat_share {float_type}"},
)
```

with the matching `Column(...)` declarations added to `UoaContractDaily` (`models.py:862-876`) and
`UoaSymbolDaily` (`models.py:920-924`).

(d) **Whale Watch is not edited.** Both copies of the gate — `services/whale_watch_tracking.py:113-123` and the
inline query `routers/whale_watch.py:153-159` — keep `classified_fraction >= 0.50` and `ask_share >= 0.65`. With
uncovered premium now `unknown`, an outage day qualifies nothing, which is the correct behaviour for a signal
product. Cited here so you know it was considered and deliberately left alone.

### 3.7 Omega — `get_option_trades` gains sides

`ai_agents/option_trades_summary.py::summarize_option_trades` (`:84-…`) stays **pure**: add an optional
`sides_by_contract: Optional[Mapping[str, Mapping[str, Any]]] = None` argument, where each value is
`{"buy_premium_usd", "sell_premium_usd", "unknown_premium_usd", "side_premium_total", "side_window_start",
"side_window_end"}` summed from the buckets. Append to `CONTRACT_COLUMNS` (`:20-34`) and to the expiry table:
`buy_premium_usd`, `sell_premium_usd`, `unknown_premium_usd`, `side_window_start`, `side_window_end`,
`side_premium_total`, `side_source`. Rules:

- `side_source = "quote_at_trade"` when `side_premium_total / premium_usd >= UOA_OMEGA_SIDE_MIN_COVERAGE` (0.80)
  for that contract; `"partial"` when 0 < ratio < 0.80; `"unavailable"` when there are no buckets.
- **The side columns are null unless `side_source == "quote_at_trade"`**, so the model is never handed a bucket
  numerator over a live-fetch denominator.
- The **live tail** — the last `UOA_INTRADAY_CADENCE_MIN × (1 + lag)` minutes, which never has buckets yet — may
  be labelled against the *current* quote and tagged `side_source = "quote_now"` in the tool result only. It is
  **never persisted**; nothing writes it to any table.
- The largest prints carry `side` and `reason` when the print appears in a bucket's `top_prints_json`.

The database read that builds `sides_by_contract` lives in the tool, not in the pure module:
`ai_agents/omega_agent.py:1655-1690` (`_tool_get_option_trades`) opens a session, reads
`uoa_contract_intraday` for the contracts and the requested window, and passes the mapping into
`summarize_option_trades`. The docstring at `ai_agents/option_trades_summary.py:1-9` must stop saying prints
carry no side and say where the side comes from instead.

### 3.8 UOA UI — coverage beside conviction

`routers/uoa_screener.py:465-474` (`_buy_ratio`) keeps returning `buy_premium / premium_total`; add
`aggressor_coverage_premium` to the same row payload and render it next to the conviction number, because low
coverage would otherwise read as low conviction. No other UI change in Phase A.

### 3.9 Searched tickers join the day's set

Not applicable in Phase A (the live tab arrives in Phase B), except for the hook: `run_tick` reads the day's
"requested symbols" from the session `uoa_runs` row's `stats_json["requested_symbols"]` list and includes them
in the universe. Phase B's route appends to that list.

### 3.10 The WebJob entry point and its offline mode

`scripts/run_uoa_intraday_tick.py`:

- **Parses its own arguments first**, before importing `db`, `models` or `services.uoa_intraday_sampler`.
  `--offline-fixture PATH` prints the classified buckets for a fixture tick and exits; that path imports only
  the standard library and `services.uoa_intraday_classify`. This is the one execution of the script the coding
  agent may run (§0.1); make it true, and T14 enforces it.
- Normal mode: `create_tables()` (as `services/uoa_scheduler.py:94` does), open a `SessionLocal()`, call
  `run_tick(db)`, log the returned status dict, exit non-zero only on an unhandled exception.
- `--trading-date` and `--tick-seq` overrides exist for Haci's manual re-runs; a re-run replaces the same
  buckets (idempotent) and the same `uoa_intraday_run` row.

The WebJob wrapper is the house pattern copied verbatim from
`app_data/jobs/triggered/fixed_universe_report_batch/run.py:9-93` with `script_name =
"run_uoa_intraday_tick.py"`. Note the standing warning at `docs/AZURE_WEBJOBS_AUTOMATION.md:60-66`: after any
wrapper change, verify in Kudu that the dashboard executes the wwwroot copy.

### 3.11 Settings — sizing and thresholds, never gates

Read at call time, clamped, each leaving a runnable job. **Phase A:**

| Name | Default | Clamp | What it sizes |
|---|---|---|---|
| `UOA_INTRADAY_CADENCE_MIN` | 5 | 1..15 | Tick spacing. OPRA is live, so 5. |
| `UOA_INTRADAY_LAG_TICKS` | 1 | 1..3 | How far back the trade fetch reads. 1 under OPRA; 2 under Basic's 15-minute hold-back. |
| `UOA_INTRADAY_CLOSE_BUFFER_MIN` | 10 | 0..30 | Last tick = close + this. |
| `UOA_INTRADAY_MAX_UNDERLYINGS` | 800 | 1..1500 | Tier-1 cap. |
| `UOA_INTRADAY_WORKERS` | 4 | 1..8 | Concurrent underlyings. |
| `UOA_INTRADAY_MAX_REQUESTS_PER_MIN` | 80 | 10..600 | Self-imposed ceiling, so the 16:02 and 16:05 jobs are not starved. |
| `UOA_INTRADAY_SNAPSHOT_PAGES` | 12 | 1..40 | The sampler's own page bound. |
| `UOA_INTRADAY_MONEYNESS_BAND` | 0.12 | 0.02..0.50 | Strike band around spot. |
| `UOA_INTRADAY_MAX_DTE` | 180 | 1..400 | Expiry bound. |
| `UOA_INTRADAY_MAX_QUOTE_AGE_SEC` | 900 | 60..3600 | `classify_print`'s `max_age_sec`. |
| `UOA_AGGRESSOR_MIN_QAT_SHARE` | 0.50 | 0.0..1.0 | Symbol classified share below which `dir_ratio` is NULL. |
| `UOA_OMEGA_SIDE_MIN_COVERAGE` | 0.80 | 0.0..1.0 | Coverage below which Omega's side columns are null. |
| `UOA_INTRADAY_QUOTE_TICK_RETENTION_SESSIONS` | 45 | 5..120 | Quote-tick retention. |
| `UOA_INTRADAY_BUCKET_RETENTION_SESSIONS` | 400 | 60..1000 | Bucket retention. |
| `UOA_INTRADAY_RETENTION_MAX_ROWS` | 2000000 | 10000..50000000 | Retention sanity cap. |

`ALPACA_OPTION_FEED` already exists (`ai_agents/options_client.py:30`, default `indicative`); production runs
`opra` (Haci, 2026-09-15 — given, not to be verified by this build). Do not change the default in code; the
production setting stays where it is. The value in use is recorded on every `uoa_quote_tick` row and in the tick
status row so the ship log can quote it. There is no setting that turns any of this off.

---

# PR 2 — PHASE B: the Tier-2 wide net, promotion, and the "UOA live" tab

Cut from `main` after PR 1 is merged and deployed. Detection needs no labels, so B can ship any time after A;
shipping them as one PR would make a rollback all-or-nothing, which is why they are two.

## 3B. Change — Phase B

### 3B.1 Tier 2 — a snapshot-only wide net

A second triggered WebJob, `app_data/jobs/triggered/uoa_widenet_sweep/` with
`{"schedule": "0 */15 9-16 * * 1-5", "is_singleton": true, …}` and
`scripts/run_uoa_widenet_sweep.py` → `services/uoa_widenet.py::run_sweep(db, *, now_utc=None)`. Same calendar
and window gate as §3.3 step 1.

- **Universe:** every US-listed name with market cap ≥ `UOA_WIDENET_MIN_MARKET_CAP` ($2B) from FMP's company
  screener (~3,500 names; NASDAQ ~2,466 + NYSE ~1,022), refreshed **weekly** and cached in
  `uoa_widenet_universe` (symbol, market_cap, refreshed_on), plus Alpaca's stock most-actives top 100 and the
  movers of the moment. Use the existing FMP client style (`ai_agents/fmp_client.py:17-63`: base
  `https://financialmodelingprep.com/stable`, `FMP_API_KEY`); the screener endpoint is new to the platform.
  **Neither Alpaca nor FMP has an options most-actives feed** (both 404 / absent as of 2026-09-15) — the
  platform computes it from chain snapshots, which is what this sweep is.
- **What is fetched:** the chain snapshot only — `dailyBar {v, n, vw}`, `prevDailyBar` and `latestQuote` per
  contract. **No prints.** Premium so far today ≈ `v × vw × 100` per contract, with nothing fetched from
  `/trades`. A between-sweep jump in `v × vw` is a big single order. `openInterest` is absent from snapshots;
  the wide net does not attempt OI.
- **Cost:** ~3,500–4,000 requests a sweep, 1–2 minutes with `UOA_WIDENET_WORKERS` (8) under Plus's 10,000/min.
  The Tier-1 token bucket and the Tier-2 one are separate but both count against the same courtesy budget; the
  sweep yields to Tier 1 by using a lower ceiling (`UOA_WIDENET_MAX_REQUESTS_PER_MIN`, 400).
- **Storage:** one end-of-day row per symbol and per flagged contract in `uoa_widenet_daily` (~3,500 rows a
  session: trading_date, symbol, last_sweep_ts, premium_est_total, call_premium_est, put_premium_est,
  contracts_seen, top_contract_symbol, top_contract_premium_est, baseline_source) so the wide net builds its own
  trailing baseline; every flag in `uoa_widenet_flags` (trading_date, sweep_ts, symbol, contract_symbol, rule,
  value, baseline, baseline_source).

### 3B.2 The calibrated flag set — thresholds verbatim

Calibrated on 73 sessions (2026-06-01..2026-09-14) of stored nightly rows; the first-draft 20× symbol rule fired
on nobody and the $2M-per-contract rule fired 25 times a day, so neither is used. Target: 20–40 flag events a
day, fewer unique names. Every threshold is a setting (§3B.5).

| kind | rule | expected/day on the S&P 500 book |
|---|---|---:|
| whale (dollar) | contract premium today ≥ **$5M** | ~6 |
| whale (dollar) | single print ≥ **$2M** (between-sweep jump `Δ(v × vw) × 100`) | ~2 |
| whale (dollar) | symbol premium today ≥ **$20M** | ~2 |
| unusual (ratio) | contract volume ≥ **10× its trailing 20-session mean**, and ≥ 500 contracts, and ≥ $1M premium | ~8 |
| unusual (ratio) | fresh line: no volume in the trailing 20 sessions, ≥ 500 contracts and ≥ **$2M** | ~10–15 |
| unusual (ratio) | symbol premium ≥ **5× its trailing 20-session mean** and ≥ $5M | ~2 |

**Baselines** are a **trailing 20-session mean**, never yesterday alone (one quiet day makes every name look 10×
busier). Tier-1 names take the baseline from `uoa_contract_daily` / `uoa_symbol_daily`; Tier-2 names take it
from `uoa_widenet_daily`, and for the wide net's first 20 sessions fall back to `prevDailyBar` with the flag
written as `baseline_source = "yesterday"`. Dollar thresholds are not scaled by market cap in v1 — the ratio
rules are what make a $3B name visible — and the counts above are to be re-read after 20 live sessions with the
wide universe. **None of these thresholds is a research finding**; they are display and promotion rules.

### 3B.3 Promotion

A flagged symbol joins Tier 1 for the rest of the day at the next 5-minute tick (the sampler reads today's
distinct flagged symbols from `uoa_widenet_flags`), so its prints from that moment are labelled normally. Its
prints from **before** promotion are fetched once and labelled against Tier 2's own 15-minute brackets, written
with `side_source = "widenet_bracket"` and reason token `widenet_bracket`; that premium is reported separately
and is **counted as classified only when** W4-style telemetry shows the 15-minute bias is small (the placebo
puts a 10–30-minute-old quote at ρ ≈ 0.0–0.13). Until then `widenet_bracket` premium is unknown premium in the
nightly merge, exactly like `one_next`.

The promoted symbol is also appended to that night's UOA universe — `_resolve_universe` already accepts an
explicit list (`services/uoa_screener.py:1043-1046`), and the nightly step passes
`universe = default_universe + today's promotions` — so a SNDK-type name outside the S&P 500 gets a UOA row and
SAS sees it the same night. The nightly's own `force_scope` behaviour is untouched
(`services/uoa_screener.py:966-995`, PI-017).

### 3B.4 The "UOA live" tab — no admin gate (Haci, 2026-09-15)

- **Route:** `GET /ai-picks/uoa-live?date=&window_min=30|60|day&symbol=` in a new
  `routers/uoa_live.py`, authenticated exactly the way the other AI Picks routes are — `current_user:
  Optional[User] = Depends(get_optional_user)` and a 401 with the `signin_required` payload when it is `None`,
  copied from `routers/conviction_monitor.py:259-275` — and registered in `app.py` beside
  `conviction_monitor_router` (`app.py:7184`, `app.py:7200`). **No** `ADMIN_TOKEN`, **no** `X-Admin-Token`,
  **no** plan check: a signed-in user sees it. Haci is the platform's only user.
- **Payload per underlying:** symbol, **unusual ratio** = `today's classified premium so far ÷ (trailing
  20-session mean daily premium × fraction of the session elapsed)`, using `uoa_symbol_daily.total_premium` for
  the trailing mean; net buy-side premium `(call_buy − call_sell) − (put_buy − put_sell)`; call buy / sell; put
  buy / sell; classified share; largest print (contract, size, side, reason); multi-leg share; conflict share;
  last tick time and its degraded flag. Expandable to contract buckets and top prints with sides and reasons.
- **Tab:** a new panel in `templates/ai_picks.html` — a `<button class="vx-tab-btn" data-target="uoa-live">UOA
  live</button>` in the tab bar (`templates/ai_picks.html:1939-1954`) and a matching
  `<div class="vx-tab-panel" data-tab="uoa-live">`; the existing delegated tab switcher at `:4106-4118` needs no
  change. **Render the button and the panel unconditionally** — no `is_admin` flag, no new key in the context
  built at `app.py:2706-2718`, no template conditional. Haci is the platform's only user (2026-09-15); if
  subscribers are ever added, whether they see this tab is a research-gated decision (DP-48) taken then, not a
  gate written now.
- **Default view:** today's unusual names — the Tier-1 ratio rule above, plus the Tier-2 flags with their rule
  names, so a wide-net name appears within 15 minutes of the order whether or not anyone had it on a list.
  Ticker search opens that symbol's contract buckets and top prints with sides; a searched ticker outside the
  universe is **added to the day's sticky set from that moment** (append to
  `uoa_runs.stats_json["requested_symbols"]`, §3.9), its earlier prints stay `unknown (not_sampled)`, and the
  row says so.
- **Rows with classified share < 0.50 are greyed and sorted last**, so a quiet sampler reads as *no data*, not
  *no activity*. Numbers only; no sentiment words; no subscriber-facing copy anywhere in this tab.

### 3B.5 Phase B settings

`UOA_WIDENET_CADENCE_MIN` (15, 5..60), `UOA_WIDENET_MIN_MARKET_CAP` (2000000000, 1e8..1e12),
`UOA_WIDENET_MAX_SYMBOLS` (4000, 100..8000), `UOA_WIDENET_WORKERS` (8, 1..16),
`UOA_WIDENET_MAX_REQUESTS_PER_MIN` (400, 10..5000), `UOA_WIDENET_UNIVERSE_REFRESH_DAYS` (7, 1..30),
`UOA_FLAG_CONTRACT_PREMIUM_USD` (5000000), `UOA_FLAG_SINGLE_PRINT_USD` (2000000),
`UOA_FLAG_SYMBOL_PREMIUM_USD` (20000000), `UOA_FLAG_CONTRACT_VOL_RATIO` (10.0) with
`UOA_FLAG_CONTRACT_VOL_MIN` (500) and `UOA_FLAG_CONTRACT_RATIO_MIN_USD` (1000000),
`UOA_FLAG_FRESH_LINE_MIN_CONTRACTS` (500) with `UOA_FLAG_FRESH_LINE_MIN_USD` (2000000),
`UOA_FLAG_SYMBOL_PREMIUM_RATIO` (5.0) with `UOA_FLAG_SYMBOL_RATIO_MIN_USD` (5000000),
`UOA_WIDENET_BASELINE_SESSIONS` (20, 5..60), `UOA_LIVE_UNUSUAL_RATIO` (3.0, 1.0..50.0). No `..._ENABLED`.

---

## 4. Before / after check

### 4.1 Repository check — the coding agent runs this, from the repository alone

Run these and paste the output in the PR body. **None of them touches a database.**

(a) **Phase A tests** — `DATABASE_URL` unset: `python tests/test_uoa_intraday_sampler.py`
    → `EN-020 Phase A: 18/18 checks passed`, exit 0. Phase B: `python tests/test_uoa_widenet.py`
    → `EN-020 Phase B: 7/7 checks passed`. **Never `pytest`** (§0.1).

(b) **The offline tick** — `python scripts/run_uoa_intraday_tick.py --offline-fixture
    tests/_fixtures/en020_tick.json`. It prints the bucket JSON for the fixture's two contracts and exits 0.
    Confirm by reading the file that the argument parse precedes every non-stdlib import; T14 asserts it.

(c) **Prove the files you must not change are unchanged** — the diff proves it directly:
    `git diff --stat main -- services/super_agent_select_scoring.py services/symbol_context_builder.py
    services/whale_watch_tracking.py routers/whale_watch.py services/conviction_monitor_service.py
    scripts/backfill_outcomes.py scripts/run_nightly_pipeline.py conftest.py`
    → **empty**. (Phase A changes `dir_ratio`'s *value*, never the scoring code that reads it; the abstention
    comes for free from `_direction_from_ratio(None)`.)

(d) **No gate crept in** — `git grep -nE "UOA_(INTRADAY|WIDENET|AGGRESSOR|LIVE|FLAG)[A-Z_]*_ENABLED|aggressor_proxy_enabled|shadow|kill_switch"`
    → no hits in the new or edited files. `aggressor_proxy_enabled` must be gone from
    `services/uoa_screener.py` entirely.

(e) **The nightly's snapshot path is untouched** — `git diff main -- ai_agents/options_client.py` shows only the
    added `max_pages` keyword (defaulting to `_MAX_SNAPSHOT_PAGES`) and the added `"pages"` key; no change to
    `_MAX_SNAPSHOT_PAGES`, `_MAX_TRADE_PAGES`, `_DEFAULT_OPTION_FEED` or `get_option_trades`.

(f) **`git diff --stat`** of the whole PR lists only the files in §3.1 (Phase A) or §3B (Phase B).

### 4.2 After deploy — the Data Steward's check, read-only

Full protocol in §8. Summary: `uoa_intraday_run` has a tick row every cadence interval from 09:30 to close + 10
on three consecutive sessions; `buy + sell + unknown = premium_total` on every `uoa_contract_daily` row; the
early-vs-late placebo gap collapses on post-ship sessions. **Haci deploys; the Steward reads; the coding agent
does neither.**

## 5. Tests — standalone runners, no pytest (PI-021)

`tests/test_uoa_intraday_sampler.py`, in the shape of `tests/test_uoa_trades_pagination.py:tail` — a module-level
`_CHECKS` list of plain functions and:

```python
if __name__ == "__main__":
    passed = 0
    for check in _CHECKS:
        try:
            check()
        except Exception as exc:  # noqa: BLE001 - a runner, not a library
            print(f"FAIL {check.__name__}: {exc.__class__.__name__}: {exc}")
            raise SystemExit(1)
        passed += 1
    print(f"EN-020 Phase A: {passed}/{len(_CHECKS)} checks passed")
```

Fixtures are literal dicts and the JSON file `tests/_fixtures/en020_tick.json`. No network, no database, no
import of `db`, `models` or `sqlalchemy` anywhere in the file (T14 asserts this for the offline script path;
the merge and aggregation tests operate on plain dicts, not ORM rows).

| # | Test | Asserts |
|---|---|---|
| T1 | `classify_print` — `both` | prev ask 1.20 / bid 1.00, next ask 1.22 / bid 1.02, price 1.20 → `buy`, `both` |
| T2 | `one_prev` counts | prev decisive `sell`, next `MID` → `sell`, `one_prev` |
| T3 | `one_next` is recorded and **not** counted | prev `MID`, next decisive `buy` → side `unknown`, reason `one_next`, `one_next_side == "buy"`; the bucket puts its premium in `unknown_premium` |
| T4 | `conflict` | prev `buy`, next `sell` → `unknown`, `conflict` |
| T5 | `fast_market` | both usable, `abs(mid_next − mid_prev) > (ask_prev − bid_prev)`, both would say `buy` → `unknown`, `fast_market` |
| T6 | `mid` | price at the midpoint on both → `unknown`, `mid` |
| T7 | `no_quote` / aged-out / crossed | no brackets; a bracket older than `max_age_sec`; `bid > ask` → `unknown`, `no_quote` |
| T8 | `wide_spread` | `(ask − bid)/mid = 0.30 > 0.25` on both → `unknown`, `wide_spread`, distinct from `no_quote` |
| T9 | `pre_open` | a print before the day's first sample, including a 09:30:00.000 auction print → `unknown`, `pre_open` |
| T10 | edge exactly on the boundary | `price == ask − 0.10 × (ask − bid)` → `buy` (inclusive, as `services/uoa_screener.py:1248`); `price == bid + edge` → `sell` |
| T11 | `oversize` and `multileg` flags | `size > ask_size` at the deciding quote → side stands, `oversize` true; a complex-order condition code → side stands, `multileg` true |
| T12 | traded-set selection | from two tick rows: volume up → in the set; volume unchanged → out; a contract new this tick with no `prev_day_volume` → out (no bracket yet, `sticky` carried to the next tick); a contract that disappeared → out; a sticky carry-over that traded → in |
| T13 | atomic tick / degraded interval | a simulated half-written tick (some contracts at `tick_seq k`, others at `k−1`) marks the interval degraded and makes its prints `no_quote`, never a bracket assembled from two different ticks |
| T14 | the offline script imports no database | after `runpy` of `scripts/run_uoa_intraday_tick.py --offline-fixture …`, `"db"`, `"models"` and `"sqlalchemy"` are absent from `sys.modules` |
| T15 | bucket aggregation and idempotent replace | reasons sum to `premium_total`; `buy + sell + unknown == premium_total`; re-aggregating the same interval yields an identical row (replace, not add) |
| T16 | nightly merge arithmetic | on fixture buckets + a fixture contract total: `buy + sell + unknown == premium_total` to one cent; `aggressor_coverage_premium` and `_count` computed both ways; uncovered premium lands in `unknown`, **never** in `buy`/`sell`; a contract with no buckets gets coverage 0 and all premium unknown |
| T17 | `dir_ratio` gating | symbol at `aggressor_qat_share = 0.49` → `dir_ratio is None`, `bull_dir == bear_dir == 0.5`, `label_* == "FLOW_UNCLASSIFIED"`, `net_directional_premium` unchanged; at 0.51 → the normal values |
| T18 | retention refuses a bad cutoff | a cutoff inside the retention window, and an estimated row count over the cap, both return without deleting and log the refusal |

**Phase B, `tests/test_uoa_widenet.py`:** T19 each of the six flag rules fires exactly at its threshold and not
one cent below; T20 trailing-20 baselines are used when available and the `yesterday` fallback is labelled;
T21 the between-sweep single-print rule uses `Δ(v × vw) × 100` and never a level; T22 promotion adds the symbol
to the day's Tier-1 set and to the nightly universe list without disturbing `force_scope`; T23 pre-promotion
prints are written `side_source = "widenet_bracket"` and counted as **unknown** by the merge; T24 the live
route's serializer greys and sorts last any row with classified share < 0.50; T25 the unusual-ratio formula
matches the stated rule on a fixture with a half-elapsed session.

**Omega, in `tests/test_option_trades_summary.py`** (the file already exists and is a standalone runner): add
T26 side columns are null when coverage < 0.80 and `side_source == "partial"`; T27 `quote_now` never appears in
anything persisted — the summarizer is pure and the tool's persistence path is not reached.

## 6. Docs

- **New:** `docs/UOA_INTRADAY_SAMPLER.md` — the tick loop, the bracket rule table of §3.4, the reason
  vocabulary, the coverage columns, the `dir_ratio` NULL rule, retention, the settings table, and one line
  naming PI-023 and EN-020 as its origin. Phase B appends the wide-net section and the "UOA live" tab.
- **Edit:** `docs/AZURE_WEBJOBS_AUTOMATION.md` — one row in the WebJobs table (`:17-24`) for
  `uoa_intraday_sampler` (`0 */5 9-16 * * 1-5`, `scripts/run_uoa_intraday_tick.py`, "EN-020 intraday quote
  sampler: buy/sell side from the quote at trade time; window-gated 09:30 → close + 10 on XNYS sessions"), and
  in Phase B a second row for `uoa_widenet_sweep`. Also correct the closing note at `:113` — early closes **are**
  modelled by this job.
- **Edit:** `docs/AI_AGENTS.md` where `get_option_trades` is described: the tool now returns side columns with a
  `side_source`, and says why they are null when coverage is thin.

## 7. Acceptance criteria — numbered, verifiable; the PR body reports each

**Phase A (PR 1)**

1. `python tests/test_uoa_intraday_sampler.py` prints `EN-020 Phase A: 18/18 checks passed` and exits 0, with
   `DATABASE_URL` unset. `pytest` was not run.
2. `python scripts/run_uoa_intraday_tick.py --offline-fixture tests/_fixtures/en020_tick.json` prints buckets
   and exits 0; the file shows the flag parsed before any non-stdlib import.
3. `git grep` for `..._ENABLED` in the new/edited files returns nothing, and `aggressor_proxy_enabled` no longer
   appears in `services/uoa_screener.py`.
4. `git diff --stat main --` for the eight files of §4.1(c) is empty.
5. `git diff main -- ai_agents/options_client.py` shows only the `max_pages` keyword and the `"pages"` key.
6. `services/uoa_intraday_classify.py` imports nothing outside the standard library (shown by the import block).
7. The closing-quote classification block formerly at `services/uoa_screener.py:1246-1255` is deleted, and the
   merge at `:1599` reads `uoa_contract_intraday`.
8. `models.py` declares `UoaQuoteTick`, `UoaContractIntraday`, `UoaIntradayRun` with the unique constraints of
   §3.2 / §3.4, and `db.py` gains the five `_ensure_columns` entries of §3.6(c).
9. The WebJob directory and `settings.job` exist with `"is_singleton": true` and the 5-minute cron.
10. `docs/UOA_INTRADAY_SAMPLER.md` exists and the WebJobs table has the new row.
11. The PR body names the deployed SHA and states "PI-023 fix — Phase A" so the register can be updated.

**Phase B (PR 2)**

12. `python tests/test_uoa_widenet.py` prints `EN-020 Phase B: 7/7 checks passed`.
13. The six flag thresholds equal §3B.2 exactly, as settings with those defaults.
14. The live route uses the AI Picks sign-in check (`get_optional_user` → 401 `signin_required`) and nothing
    else: `grep -n "ADMIN_TOKEN\|X-Admin-Token\|ADMIN_EMAIL\|is_admin" routers/uoa_live.py templates/ai_picks.html
    app.py` finds nothing new (`git diff` shows it).
15. The "UOA live" tab markup is rendered unconditionally; the `git diff` of `templates/ai_picks.html` contains
    only the tab button, the panel and its script — no template conditional around them.
16. Promotion appends to the nightly universe through the existing `_resolve_universe(explicit=…)` path, with
    no change to `force_scope` behaviour.

## 8. Verification at `/desk-run verify EN-020 <sha>` — full protocol

**Haci:** merge and deploy PR 1; record the PR link and the deployed SHA on the EN-020 row; run
`/desk-run verify EN-020 <sha>` after the first full session with the sampler running. Repeat for PR 2. Ship
PI-014 only after PR 1 has passed W1–W3.

**Data Steward, read-only role on `$RESEARCH_DB_URL`.** Before-state comes from the freeze, never a live query:
`manifest_v001`'s `uoa_contract` and `uoa_symbol` parquet carry the closing-quote labels and predate the change
by construction (23–35% unknown premium; classified buy-share 47–59%; the early-vs-late placebo gap of §1).

- **W1 — the sampler ran.** `uoa_intraday_run` has one row per cadence interval from 09:30 to close + 10 on
  three consecutive sessions (**≥ 79 rows** on a full session at the 5-minute cadence, ≥ 43 on a 13:00 close),
  `status = 'ok'` on all of them, `http_429_count` not rising tick over tick, `truncated_underlyings_json`
  listing whatever was truncated (SPY and QQQ acceptable if recorded). The session `uoa_runs` row with
  `run_type = 'intraday_sampler'` exists and finished.
- **W2 — the merge reconciles.** On those sessions: `buy_premium + sell_premium + unknown_premium =
  premium_total` on every `uoa_contract_daily` row (to one cent); ≥ 80% of the book's premium sits in contracts
  with `aggressor_coverage_premium ≥ 0.90`; `dir_ratio` is NULL on every `uoa_symbol_daily` row with
  `aggressor_qat_share < 0.50` and non-NULL on every row above it; `net_directional_premium` is populated as
  before.
- **W3 — the placebo, post-ship. This is the PI-023 criterion.** Re-run
  `research/reports/uoa_side_2026-09-15/ttc_test2.py` against post-ship sessions using the **new** labels in
  `uoa_contract_intraday.top_prints_json`: the early leg (> 3 h before the close) and the late leg (< 30 min)
  must have |ρ| against SPY's open-to-close within **0.10** of each other after 10 sessions (before: −0.577 /
  +0.455 early versus −0.031 / −0.019 late). Thousands of prints a session and a built-in zero make this
  decisive in days. The daily Spearman of §1 is reported beside it but is **not** the criterion (its standard
  error at n = 20 is ≈ 0.23).
- **W4 — reason telemetry.** Premium share by reason per session. `conflict + fast_market > 15%` on the top-20
  liquid names for five sessions → a cadence note to Haci, not a failure. Report the `one_next` share and its
  own early-vs-late ρ, so the desk can later decide whether to start counting it. Same for
  `widenet_bracket` after Phase B.
- **W5 — Omega.** A read showing bucket rows exist for a liquid contract over a completed window, plus the
  repository-only tests T26/T27. **The live tool call is Haci's, not the desk's** (DP-49).
- **W6 — the record.** Write to `research/data/DATA_NOTES.md`, under a dated ship-log entry (**not** a
  repair-log row — nothing historical was rewritten, `DATA_NOTES.md:32-33`):

  > **EN-020 Phase A (PI-023) shipped `<sha>`, first covered session `<YYYY-MM-DD>`.** From that session
  > `uoa_contract_daily.buy_premium / sell_premium / unknown_premium` are summed from `uoa_contract_intraday`
  > buckets labelled against the quote bracketing each print; uncovered premium is `unknown`, with no
  > closing-quote fallback. `uoa_symbol_daily.dir_ratio` is NULL when `aggressor_qat_share < 0.50`, and
  > `bull_dir`/`bear_dir` fall to 0.50, which moves `score_day/swing/long` on those symbols; the SAS legacy flow
  > vote abstains there. Feed in use: `opra` (as recorded on the tick rows). Per-session `aggressor_qat_share`: `<table>`. **No
  > historical row was rewritten.** Under DP-50(a) the aggressor columns are two different features either side
  > of this date: **Q014, Q019, Q029 and Q030 split here.**

  Add `uoa_quote_tick` and `uoa_contract_intraday` to `research/lib/freeze_config.json` with availability
  `bucket_start + 20 minutes` and lag 0, and note in the same file that `uoa_symbol`'s declared 16:05
  availability is nominal — the rows are written 16:43–17:13 in the same pipeline, before SAS reads them for the
  same session, so there is no leak.
- **PI-023 closes** in `research/PLATFORM_ISSUES.md` when W1, W2 and W3 pass, with the ship SHA and date. The
  register row for EN-020 moves to `IMPLEMENTED` with both PR links.

## 9. Rollback

`git revert` of the PR (each phase independently; PR 2 first if both are live). Reverting Phase A restores the
closing-quote classification for sessions after the revert; the `uoa_quote_tick` / `uoa_contract_intraday` /
`uoa_intraday_run` tables and the added columns remain, holding nothing new, and no row written under either
regime is rewritten. The desk logs the revert SHA and date in `DATA_NOTES.md` the same way it logged the ship,
and the affected questions split again there.

## 10. Out of scope — do not touch

- **Phase 2, the delta-adjusted backfill of history** (`mid_t ≈ mid_close − Δ × (S_close − S_t)`, calibrated
  against Phase 1's `both`/`one_prev` labels) is **not in this brief**; the desk decides it after 20 sessions of
  live buckets, and it would be its own repair brief with its own DATA_NOTES entry.
- No historical row is rewritten by anything here. `manifest_v001` keeps the artefact, by design.
- No SAS weight, threshold, or the `flow_polarity` enable flag (PI-014 owns that);
  `services/super_agent_select_scoring.py` is not edited at all.
- No change to Whale Watch's two gate copies, to `premium_total` / `trade_count` / `top_trades_json` / the
  selection filters of `_pick_contracts`, to `_MAX_SNAPSHOT_PAGES`, `_MAX_TRADE_PAGES` or `get_option_trades`.
- Multi-leg prints are flagged and measured, not excluded — that would be a later, evidence-based change.
- No new subscriber-facing number in the nightly artefacts. The live tab is ungated because Haci is the
  platform's only user (2026-09-15); a live UOA page for subscribers, if they are ever added, is
  a separate enhancement gated on a research question (does intraday buy-side flow predict the close or the next
  session? — to `research/BACKLOG.md` once 20 sessions of buckets exist).
- No websocket/streaming option quotes (`market_data/live_options.py` is untouched); no OI in the wide net.
- `conftest.py`, `.github/`, the deploy workflows and any `scripts/backfill_*` are not edited.
