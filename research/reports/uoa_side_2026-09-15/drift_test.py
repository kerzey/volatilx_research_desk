"""Does the stored buy/sell split follow the day's price direction? (PI-023 signature test)

If every print is judged against the CLOSING quote, then on an up day calls close quoted above where
they traded (so call prints look like SELLs) and puts close quoted below (put prints look like BUYs).
Prediction if the artefact is real: call buy-share falls with the day's SPY return, put buy-share rises.
Descriptive, read-only, not a study result. SPY bars from Alpaca market data (allowed source)."""
import os
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path[:0] = [str(Path(__file__).resolve().parents[3] / "research" / "lib")]
import desk_env  # noqa: E402

desk_env.load()
from sqlalchemy import create_engine, text  # noqa: E402

engine = create_engine(os.environ["RESEARCH_DB_URL"])
q = """
    select trading_date, option_type,
           sum(buy_premium) buy, sum(sell_premium) sell, sum(unknown_premium) unk, sum(premium_total) total
    from uoa_contract_daily
    where trading_date >= '2026-01-01' and trade_count > 0
    group by 1, 2 order by 1, 2"""
with engine.connect() as c:
    df = pd.DataFrame(c.execute(text(q)).fetchall(), columns=["trading_date", "option_type", "buy", "sell", "unk", "total"])
for col in ("buy", "sell", "unk", "total"):
    df[col] = df[col].astype(float)
df["buy_share_classified"] = df["buy"] / (df["buy"] + df["sell"])
piv = df.pivot(index="trading_date", columns="option_type", values="buy_share_classified")
piv.index = pd.to_datetime(piv.index)

hdr = {"APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
r = requests.get(
    "https://data.alpaca.markets/v2/stocks/SPY/bars",
    params={"timeframe": "1Day", "start": "2025-12-15", "end": "2026-09-15", "limit": 1000, "adjustment": "all", "feed": "sip"},
    headers=hdr,
    timeout=60,
)
r.raise_for_status()
bars = pd.DataFrame(r.json()["bars"])
bars["d"] = pd.to_datetime(bars["t"]).dt.tz_convert("America/New_York").dt.normalize().dt.tz_localize(None)
bars = bars.set_index("d")
bars["spy_ret"] = bars["c"].pct_change()
bars["spy_intraday"] = bars["c"] / bars["o"] - 1.0  # open-to-close: the move the closing quote encodes

m = piv.join(bars[["spy_ret", "spy_intraday"]], how="inner").dropna()
print(f"nights: {len(m)}  ({m.index.min().date()} .. {m.index.max().date()})")
for side in ("call", "put"):
    for ret in ("spy_intraday", "spy_ret"):
        rho = m[side].corr(m[ret], method="spearman")
        print(f"{side:4s} buy-share vs SPY {ret:12s}: spearman {rho:+.3f}")
# tercile table on open-to-close
m["tercile"] = pd.qcut(m["spy_intraday"], 3, labels=["down day", "flat", "up day"])
print()
print(m.groupby("tercile", observed=True)[["call", "put"]].mean().round(3).rename(columns={"call": "call buy-share", "put": "put buy-share"}))
print()
print("call minus put buy-share, by tercile:")
g = m.groupby("tercile", observed=True)
print((g["call"].mean() - g["put"].mean()).round(3))
out = Path(__file__).with_name("drift_test_daily.csv")
m.to_csv(out)
print("wrote", out.name)
