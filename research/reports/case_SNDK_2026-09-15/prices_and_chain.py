"""SNDK case study — (1) stored UOA contract mix by type and expiry, read-only; (2) daily and hourly bars from
Alpaca market data (data.alpaca.markets only) for SNDK, its memory peers and the tape. Operational, NON_QUOTABLE."""
import sys, os, json
sys.path[:0] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib")]
from desk_env import load; load()
import warnings; warnings.filterwarnings("ignore")
import requests, psycopg, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)

conn = psycopg.connect(os.environ["RESEARCH_DB_URL"], options="-c default_transaction_read_only=on")
q = lambda s: pd.read_sql(s, conn)
print("=== uoa_contract_daily mix, 2026-09-08..09-14")
try:
    print(q("""SELECT underlying_symbol sym, trading_date, option_type, count(*) n, min(expiration_date) min_exp, max(expiration_date) max_exp,
     round(min(strike_price)::numeric,0) kmin, round(max(strike_price)::numeric,0) kmax, round(sum(premium_total)::numeric,0) prem
     FROM uoa_contract_daily WHERE underlying_symbol IN ('SNDK','STX','WDC','MU') AND trading_date BETWEEN '2026-09-08' AND '2026-09-14'
     GROUP BY 1,2,3 ORDER BY 1,2,3""").to_string(index=False))
except Exception as e:
    print("ERR", e); conn.rollback()
print("\n=== gex quality, SNDK")
print(q("""SELECT trading_date, quality_json FROM gex_symbol_daily WHERE underlying='SNDK' AND trading_date >= '2026-09-04' ORDER BY trading_date""").to_string(index=False))
print("\n=== share of GEX rows whose walls are all call walls, since 2026-08-01")
print(q("""SELECT count(*) n, sum(case when top_walls_json::text NOT LIKE '%put_wall%' then 1 else 0 end) no_put_wall,
 sum(case when regime='POS_GAMMA' then 1 else 0 end) pos_gamma FROM gex_symbol_daily WHERE trading_date >= '2026-08-01'""").to_string(index=False))

H = {"APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
SYMS = ["SNDK", "MU", "WDC", "STX", "SMH", "QQQ", "SPY"]


def bars(tf, start, end):
    out, token = [], None
    while True:
        p = {"symbols": ",".join(SYMS), "timeframe": tf, "start": start, "end": end, "adjustment": "split", "feed": "sip", "limit": 10000}
        if token:
            p["page_token"] = token
        r = requests.get("https://data.alpaca.markets/v2/stocks/bars", headers=H, params=p, timeout=60)
        r.raise_for_status()
        j = r.json()
        for s, rows in (j.get("bars") or {}).items():
            for b in rows:
                out.append({"sym": s, "t": b["t"], "o": b["o"], "h": b["h"], "l": b["l"], "c": b["c"], "v": b["v"]})
        token = j.get("next_page_token")
        if not token:
            break
    return pd.DataFrame(out)


d = bars("1Day", "2026-08-20", "2026-09-15T23:59:00Z")
d["date"] = d.t.str[:10]
close = d.pivot(index="date", columns="sym", values="c")[SYMS]
print("\n=== daily closes")
print(close.round(2).to_string())
print("\n=== daily % change")
print((close.pct_change() * 100).round(2).to_string())
s = d[d.sym == "SNDK"][["date", "o", "h", "l", "c", "v"]]
print("\n=== SNDK daily OHLCV")
print(s.to_string(index=False))
h = bars("1Hour", "2026-09-08T13:00:00Z", "2026-09-15T23:59:00Z")
hs = h[h.sym == "SNDK"].copy()
hs["et"] = pd.to_datetime(hs.t).dt.tz_convert("America/New_York").dt.strftime("%m-%d %H:%M")
print("\n=== SNDK hourly (ET)")
print(hs[["et", "o", "h", "l", "c", "v"]].to_string(index=False))
