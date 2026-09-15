"""Can a wide net catch a big option order OUTSIDE the monitored list? Probes, read-only:
1. Alpaca stock screener: most-actives (by volume / trades) and movers — stock-level only?
2. FMP most-actives and company screener — how many US names above a size floor (the Tier-2 universe size)?
3. A chain snapshot for a non-S&P-500 name: does it carry prevDailyBar (yesterday's volume) and openInterest?
Keys come from desk_env; nothing is printed but counts and field names."""
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests

sys.path[:0] = [str(Path(__file__).resolve().parents[3] / "research" / "lib")]
import desk_env  # noqa: E402

desk_env.load()
HDR = {"APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
FMP = os.environ.get("FMP_API_KEY")


def show(title, r):
    print(f"== {title}: HTTP {r.status_code}")
    if r.status_code != 200:
        print("   ", r.text[:200].replace(FMP or "\x00", "***"))
        return None
    return r.json()


js = show("alpaca most-actives by volume", requests.get("https://data.alpaca.markets/v1beta1/screener/stocks/most-actives", headers=HDR, params={"by": "volume", "top": 10}, timeout=30))
if js:
    print("    keys:", list(js.keys()), "| first:", (js.get("most_actives") or [{}])[0])
js = show("alpaca most-actives by trades", requests.get("https://data.alpaca.markets/v1beta1/screener/stocks/most-actives", headers=HDR, params={"by": "trades", "top": 100}, timeout=30))
if js:
    print("    n:", len(js.get("most_actives") or []))
js = show("alpaca movers", requests.get("https://data.alpaca.markets/v1beta1/screener/stocks/movers", headers=HDR, params={"top": 10}, timeout=30))
if js:
    print("    keys:", list(js.keys()), "| first gainer:", (js.get("gainers") or [{}])[0])
r = requests.get("https://data.alpaca.markets/v1beta1/screener/options/most-actives", headers=HDR, params={"by": "volume", "top": 10}, timeout=30)
show("alpaca OPTIONS most-actives (does it exist?)", r)

if FMP:
    js = show("fmp most-actives", requests.get("https://financialmodelingprep.com/stable/most-actives", params={"apikey": FMP}, timeout=30))
    if isinstance(js, list):
        print("    n:", len(js), "| first:", js[0] if js else None)
    js = show("fmp company screener (US, mcap > $2B, actively trading)", requests.get(
        "https://financialmodelingprep.com/stable/company-screener",
        params={"apikey": FMP, "marketCapMoreThan": 2_000_000_000, "country": "US", "isActivelyTrading": "true", "isEtf": "false", "limit": 10000}, timeout=60))
    if isinstance(js, list):
        exch = {}
        for row in js:
            exch[row.get("exchangeShortName")] = exch.get(row.get("exchangeShortName"), 0) + 1
        print("    n:", len(js), "| by exchange:", dict(sorted(exch.items(), key=lambda kv: -kv[1])[:8]))
    js = show("fmp company screener (US, mcap > $10B)", requests.get(
        "https://financialmodelingprep.com/stable/company-screener",
        params={"apikey": FMP, "marketCapMoreThan": 10_000_000_000, "country": "US", "isActivelyTrading": "true", "isEtf": "false", "limit": 10000}, timeout=60))
    if isinstance(js, list):
        print("    n:", len(js))

# 3. chain snapshot for a non-S&P name (Tier-2 style, one page, no strike filter): fields present?
for sym in ("SOFI", "RKLB"):
    t0 = time.time()
    r = requests.get(f"https://data.alpaca.markets/v1beta1/options/snapshots/{sym}", headers=HDR, params={
        "feed": "indicative", "limit": 1000,
        "expiration_date_gte": date.today().isoformat(), "expiration_date_lte": (date.today() + timedelta(days=180)).isoformat()}, timeout=60)
    js = show(f"chain snapshot {sym}", r)
    if js:
        snaps = js.get("snapshots") or {}
        k = next(iter(snaps))
        s = snaps[k]
        print(f"    {len(snaps)} contracts on page 1, next_page_token={'yes' if js.get('next_page_token') else 'no'}, {time.time()-t0:.1f}s")
        print("    fields:", sorted(s.keys()))
        print("    dailyBar:", s.get("dailyBar"), "| prevDailyBar:", s.get("prevDailyBar"), "| openInterest:", s.get("openInterest"))
