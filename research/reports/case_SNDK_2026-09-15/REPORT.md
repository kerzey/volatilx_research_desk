# SNDK, week of 2026-09-08 — why three rank-1 SAS picks did not work

**2026-09-15. Operational case study, one symbol, one week. INTERNAL / NON_QUOTABLE. Not a research
verdict:** n = 1 proves nothing about SAS in general, and nothing here is a forecast. Live read-only
queries (rule 4 allows them for operational checks; no locked question's results were opened), Alpaca
market data, and two public news searches. Scripts in this folder; raw pulls stayed in the session
scratch directory.

## Decision paragraph

SNDK was published at **rank 1 on three nights** (93.3 on 09-08, 92.7 on 09-10, 87.1 on 09-11) and fell
from 1,737.99 to about 1,554 by the morning of 09-15. **The main cause was the market, not SNDK:** the
whole memory and storage group sold off on supply-glut and AI-demand worries (WDC and STX fell further
than SNDK; SMH fell half as much; SPY barely moved). **But the 93 score was inflated by a platform bug
the desk found while tracing it (PI-020):** the options-flow scanner keeps only the first 1,000 option
trades per request and never fetches the next page. Alpaca returns trades sorted by contract name, and
calls sort before puts, so on a heavily traded stock the puts are cut off. The platform stored **2,000
trades, all calls, dir_ratio 1.00** for SNDK on 09-08; the same contracts actually traded **~25,600
times: $201M in calls and $83M in puts.** The "huge bullish call flow" was real call buying on
**0–3-day weekly calls that expired 09-11**, most of them worthless, next to a put side the platform
never saw. The defect is not SNDK-specific: **about one symbol-day in six has hit the cap every month
since January, and 317 of 604 published picks since 2026-06-01 were scored on capped flow.** Two further
things went wrong that no bug explains: the platform's own **conviction monitor said EXIT on 09-10**,
the same night SAS published SNDK at rank 1 again, and the **bearish projection engine surfaced SNDK on
09-09** (score dropped to 76), then vanished on 09-10 (score back to 93). **Haci's action:** decide PI-020
(fix recommended); the other two are filed as research questions.

## 1. What SAS published

| night | score | rank | flow | tech | proj | layers agreeing | close |
|---|---:|---:|---:|---:|---:|---|---:|
| 09-04 | 78.5 | — | 35 | 88 | 95 | 2 | 1,740.00 (+11.9% that day) |
| **09-08** | **93.3** | **1** | 80 | 88 | 95 | 3 (bonus +6) | 1,737.99 |
| 09-09 | 76.1 | — | 78 | 88 | 93 | 2; conflict −13 (bearish projection also listed SNDK) | 1,764.17 |
| **09-10** | **92.7** | **1** | 80 | 88 | 93 | 3 (bonus +6) | 1,692.59 |
| **09-11** | **87.1** | **1** | 57 | 88 | 95 | 3 (bonus +6) | 1,633.35 |
| 09-14 | 40.5 | — | 70 | 58 | 35 | mixed; projection now bearish | 1,551.99 |

Every published night carried the same GPT risk text: positive gamma may dampen follow-through, nearby
call wall, very high volatility (ATR ≈ 7% of price a day, beta 5.2). Earnings are not near (next
2026-11-05). Regime: strongly_bullish / pullback_in_bull all week.

## 2. Why the score was 93

- **Projection 95:** a 10-bar pattern match projecting ~+14.8% in about two weeks (target ≈ 1,996).
- **Technical 88:** daily and weekly moving-average trend up, computed the evening after a +11.9% day.
- **Flow 80, and the three-layer agreement bonus:** two of the five bullish direction votes on 09-08 and
  09-10 came from options flow (`uoa_day`, `uoa_dir_ratio` = 1.00). That flow reading is the one PI-020
  truncated. What the corrected score would have been cannot be said without re-running the scorer on
  complete trades; the true 09-08 premium mix in the scanned contracts was still call-leaning (71% calls),
  so the flow vote may have survived, at a lower strength.

## 3. What the options flow really was

Top contracts by premium on each pick night (from the platform's own stored rows):

- **09-08:** calls expiring **09-11** (3 days), strikes 1,650–1,775; largest 1,650C $18.2M, 1,700C $10.4M.
- **09-09:** 09-11 calls, 1,700C $24.5M, 1,760C $9.1M.
- **09-10:** 09-11 calls (1 day), 1,650C $8.7M, 1,715C $5.7M.
- **09-11 (expiry day):** the largest line was a **put**, 1,750P $7.3M; SNDK closed 1,633.35.

All of it was same-week weekly options. SNDK closed 09-11 below every strike from 1,650 up, so most of
that call premium expired worthless. Short-dated call volume on a stock that just rose 12% in a day is
as consistent with chasing and hedging as with informed positioning; the scanner cannot tell those apart,
and with the puts cut off it could not see the other side either.

Verification (script `verify_trades.py`): the platform's request shape for 09-08 returns 1,000 trades
over 8 call contracts and a `next_page_token` that is never followed. Paginated, the same 50 contracts
hold 14,441 call trades ($200.7M) and 11,154 put trades ($82.5M).

## 4. What price did, against its group

Close on 09-08 to about 10:00 ET on 09-15:

| | SNDK | WDC | STX | MU | SMH | QQQ | SPY |
|---|---:|---:|---:|---:|---:|---:|---:|
| change | −10.6% | −12.1% | −13.6% | −6.9% | −5.0% | −1.3% | −0.8% |

The down days were group days: 09-10 (SNDK −4.1%, MU −4.9%, WDC −4.4%), 09-11 (SNDK −3.5%, WDC −3.0%,
STX −3.7% while SMH rose 1.5% — memory-specific), 09-14 (SNDK −5.0%, MU −5.3%, SMH −4.8%). Public
coverage attributes it to announced Samsung / SK Hynix supply additions and doubts about AI demand
growth (sources below, not independently verified by the desk).

## 5. How each pick would have traded

Levels are the platform's own (`sas_selection_excursion`, `public_payload_json`). Hourly bars include
extended hours.

- **09-08 pick (close 1,737.99).** Day targets L1 1,781.60 and L2 1,794.98 were **both touched on 09-09**
  (high 1,807.22). The swing target L3 1,952.59 was not. Both swing counter-levels (1,561.68 and 1,514.36)
  were touched on 09-14 (low 1,505.00). The execution plan (buy a breakout of 1,751–1,760 in the first 90
  minutes, stop 1,700, T1 1,995.72) triggered on 09-09 and **stopped out on 09-10**, about −3.4%.
- **09-10 pick (1,692.59).** L1 1,733.95 was reached only in pre-market on 09-11 (regular-session high
  1,720.70). The plan (breakout 1,700–1,715, stop 1,670) triggered at the 09-11 open and **stopped the
  same morning** as SNDK fell ~95 points in an hour — about −2.6% at the stop, more if it filled late.
- **09-11 pick (1,633.35).** The plan needed a breakout above 1,650–1,666.50; SNDK has not traded above
  1,582 since, so **the plan never entered.** An after-hours buyer at ~1,630 was about −4.6% by 09-15.

A trader who followed the day lane could have taken the 09-09 touch; one who followed the swing plan lost
twice and was kept out the third time.

## 6. The platform contradicted itself

- **Conviction monitor vs selection.** The monitor put the 09-08 pick on WATCH on 09-09 (OBV flipped
  bearish on 30m, 1h and 4h; 1h higher-low chain broken) and **EXIT on 09-10** (key support breached on
  30m and 1h, 4h Kalman regime flipped to opposing, MACD 4h bearish). SAS published SNDK at rank 1 that
  same night, and again on 09-11, when the monitor also rated the 09-10 pick EXIT. Selection does not
  read the monitor.
- **Bullish and bearish projection engines on consecutive nights.** On 09-09 the bearish projection
  engine listed SNDK, giving a 13-point conflict penalty; on 09-10 it did not, and the score returned to
  92.7 with no conflict. The score swung 17 points on which engine happened to list the symbol.
- **Gamma data looks suspect too (not verified).** Every SNDK wall is a call wall and the regime is
  POS_GAMMA every night; the GEX job used 39–50 of 2,000 contracts, with implied volatility missing. Since
  2026-08-01, 755 of 1,972 GEX rows carry no put wall at all. Filed as a note under PI-020 for the steward
  to check; the "positive gamma" risk warning should not be trusted until it is.

## 7. SNDK's own history, for context only

SNDK had four earlier rank-1 picks scoring 90+: three in April 2026, a strong tape, and one on 2026-05-29
(91.7), whose deepest drawdown in its window was −10.7%. Four picks on one symbol cannot say whether
high scores work on SNDK; the desk's known finding that repeatedly selected "champion" symbols grade
below the base rate is the relevant general result, and Q003 (repeat selection) is the registered test.

## 8. "Will it do better this week?"

The desk cannot answer that, and nothing on the platform has been shown to predict one stock's next week.
What the platform itself says today: SNDK scored 40.5 on 09-14 (direction mixed, projection now bearish),
is not published, and the conviction monitor rates all three picks EXIT. Facts a trader can watch, not
signals: SNDK is back below its 20-day average and above its 50-day; 1,600 was the 09-11 plan's stop and
1,505 is the 09-14 low; monthly options expire Friday 09-18; the memory group (MU, WDC, STX) has not yet
stopped falling (WDC and STX were down again on 09-15).

## 9. What was filed

- **PI-020** (high) — option-trade truncation in the UOA scanner; distorts flow scores and dir_ratio for
  the most liquid names every day since at least 2026-01. Affects frozen `uoa_symbol` in `manifest_v001`
  and therefore the flow inputs of registered questions (Q014, Q029's flow layer) and H-092. A fix will
  rewrite nothing historical by itself; any repair of past rows must be logged in `DATA_NOTES.md` and
  questions spanning it split at the ship date (DP-50).
- **H-095** (F1) — re-selection while the conviction monitor says EXIT.
- **H-096** (F2) — score swings caused by the bearish projection engine listing a symbol on alternate nights.

## Sources (news, section 4)

- [Motley Fool — Why Did Sandisk Stock Slump Today? (2026-09-10)](https://www.fool.com/investing/2026/09/10/why-did-sandisk-stock-slump-today/)
- [Invezz — Why are Micron, SanDisk, SK Hynix and other memory stocks falling? (2026-09-10)](https://invezz.com/news/2026/09/10/why-are-micron-sandisk-sk-hynix-and-other-memory-stocks-falling/)
- [Yahoo Finance — SanDisk shares fall 5.5% as AI demand concerns weigh on memory stocks](https://finance.yahoo.com/technology/ai/articles/sandisk-shares-fall-5-5-120141549.html)
- [FX Leaders — SNDK tests $1,500 after failing at resistance (2026-09-14)](https://www.fxleaders.com/news/2026/09/14/sandisk-sndk-stock-tests-1500-after-failing-at-resistance-as-demand-concerns-weigh-on-memory/)
