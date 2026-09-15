"""How many contracts does a per-underlying chain snapshot return within EN-020's band (±12% of spot, ≤180 DTE),
and how many 1,000-row pages is that? Red-team REQUIRED item 4. Alpaca market data only; read-only."""
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
FEED = (os.getenv("ALPACA_OPTION_FEED") or "indicative").strip().lower()
BASE = "https://data.alpaca.markets/v1beta1/options"
SYMS = ["SPY", "QQQ", "NVDA", "TSLA", "AAPL", "SNDK", "KO", "PFE"]
today = date.today()


def spot(sym):
    r = requests.get(f"https://data.alpaca.markets/v2/stocks/{sym}/trades/latest", headers=HDR, params={"feed": "sip"}, timeout=30)
    if r.status_code != 200:
        r = requests.get(f"https://data.alpaca.markets/v2/stocks/{sym}/trades/latest", headers=HDR, params={"feed": "iex"}, timeout=30)
    r.raise_for_status()
    return float(r.json()["trade"]["p"])


print(f"feed={FEED}  date={today}")
print("symbol   spot   contracts  pages  seconds  first_page_calls  first_page_puts  nearest_expiry_share")
total_pages = 0
for sym in SYMS:
    s = spot(sym)
    params = {
        "feed": FEED,
        "limit": 1000,
        "strike_price_gte": round(s * 0.88, 2),
        "strike_price_lte": round(s * 1.12, 2),
        "expiration_date_gte": today.isoformat(),
        "expiration_date_lte": (today + timedelta(days=180)).isoformat(),
    }
    n = 0
    pages = 0
    token = None
    t0 = time.time()
    first_calls = first_puts = 0
    expiries = {}
    while True:
        if token:
            params["page_token"] = token
        r = requests.get(f"{BASE}/snapshots/{sym}", headers=HDR, params=params, timeout=60)
        if r.status_code == 429:
            time.sleep(2)
            continue
        r.raise_for_status()
        js = r.json()
        snaps = js.get("snapshots") or {}
        pages += 1
        n += len(snaps)
        for k in snaps:
            exp = k[len(sym):len(sym) + 6]
            expiries[exp] = expiries.get(exp, 0) + 1
            if pages == 1:
                if k[len(sym) + 6] == "C":
                    first_calls += 1
                else:
                    first_puts += 1
        token = js.get("next_page_token")
        if not token or pages >= 40:
            break
    total_pages += pages
    nearest = max(expiries.values()) / n if n else 0
    print(f"{sym:6s} {s:8.2f} {n:10d} {pages:6d} {time.time()-t0:8.1f} {first_calls:17d} {first_puts:16d} {nearest:20.2f}")
print("pages for these", len(SYMS), "symbols:", total_pages)
