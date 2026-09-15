"""SNDK case study — verify the suspected trade-truncation defect. Read-only: stored contract rows from the DB,
option trades from Alpaca market data (data.alpaca.markets, v1beta1/options/trades). Nothing is written anywhere."""
import sys, os
sys.path[:0] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib")]
from desk_env import load; load()
import warnings; warnings.filterwarnings("ignore")
import requests, psycopg, pandas as pd

DAY = "2026-09-08"
conn = psycopg.connect(os.environ["RESEARCH_DB_URL"], options="-c default_transaction_read_only=on")
rows = pd.read_sql(f"""SELECT contract_symbol, option_type, strike_price, trade_count, premium_total FROM uoa_contract_daily
 WHERE underlying_symbol='SNDK' AND trading_date='{DAY}' ORDER BY contract_symbol""", conn)
print(f"stored contracts {len(rows)}; stored trade_count sum {int(rows.trade_count.sum())}; "
      f"calls with trades {int(((rows.option_type=='call') & (rows.trade_count>0)).sum())}, puts with trades {int(((rows.option_type=='put') & (rows.trade_count>0)).sum())}")
H = {"APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
URL = "https://data.alpaca.markets/v1beta1/options/trades"
start, end = f"{DAY}T13:30:00Z", f"{DAY}T20:15:00Z"

# (a) the platform's request shape: first 50 contracts in one call, limit 1000, no pagination
first50 = rows.contract_symbol.tolist()[:50]
r = requests.get(URL, headers=H, params={"symbols": ",".join(first50), "limit": 1000, "start": start, "end": end}, timeout=60)
r.raise_for_status(); j = r.json()
got = {s: len(v) for s, v in (j.get("trades") or {}).items()}
print(f"(a) one page, limit 1000: {sum(got.values())} trades over {len(got)} contracts; next_page_token present: {bool(j.get('next_page_token'))}")
print("    contracts returned (alphabetical):", sorted(got)[:3], "...", sorted(got)[-3:])
print("    puts returned:", sum(1 for s in got if 'P0' in s[-9:]))

# (b) the same 50 contracts, fully paginated, premium by type
tot = {"call": [0, 0.0], "put": [0, 0.0]}
token, pages = None, 0
while True:
    p = {"symbols": ",".join(first50), "limit": 10000, "start": start, "end": end}
    if token:
        p["page_token"] = token
    r = requests.get(URL, headers=H, params=p, timeout=60); r.raise_for_status(); j = r.json(); pages += 1
    for s, v in (j.get("trades") or {}).items():
        k = "put" if s[-9] == "P" else "call"
        for t in v:
            tot[k][0] += 1; tot[k][1] += float(t["p"]) * float(t["s"]) * 100
    token = j.get("next_page_token")
    if not token or pages > 200:
        break
print(f"(b) paginated ({pages} pages): calls {tot['call'][0]} trades ${tot['call'][1]/1e6:.1f}M; puts {tot['put'][0]} trades ${tot['put'][1]/1e6:.1f}M")
