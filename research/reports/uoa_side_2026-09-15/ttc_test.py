"""RED TEAM read-only placebo test for PI-023: does the closing-quote label's tape correlation
vanish for prints made just before the close?  Under the artefact it must (the closing quote IS
the quote at trade time for a 15:55 print).  Under a real behavioural story (profit-taking in
calls on up days) there is no reason for the relation to depend on minutes-to-close.
Sample: the 10 largest prints per contract (top_trades_json), premium-weighted."""
import os, sys
from pathlib import Path
import pandas as pd
sys.path[:0] = [r"C:\Users\sahin\OneDrive\Desktop\VolatilX_Research_Desk\research\lib"]
import desk_env; desk_env.load()
from sqlalchemy import create_engine, text

eng = create_engine(os.environ["RESEARCH_DB_URL"])
Q = """
with p as (
  select c.trading_date, c.option_type, c.bid, c.ask,
         (t->>'p')::float price, (t->>'s')::float size,
         ((t->>'t')::timestamptz at time zone 'America/New_York') ts
  from uoa_contract_daily c, jsonb_array_elements(c.top_trades_json::jsonb) t
  where c.trading_date >= :d0 and c.trading_date <= :d1
    and c.trade_count > 0 and c.premium_total >= 100000
    and c.ask > c.bid and c.bid > 0
), q as (
  select trading_date, option_type,
    case
      when extract(epoch from ((trading_date + time '16:00') - ts))/60.0 < 10 then '1_lt10m'
      when extract(epoch from ((trading_date + time '16:00') - ts))/60.0 < 30 then '2_10_30m'
      when extract(epoch from ((trading_date + time '16:00') - ts))/60.0 < 60 then '3_30_60m'
      when extract(epoch from ((trading_date + time '16:00') - ts))/60.0 < 180 then '4_1_3h'
      else '5_gt3h' end bucket,
    price*size*100 prem,
    case when price >= ask - 0.10*(ask-bid) then 1 else 0 end is_buy,
    case when price <= bid + 0.10*(ask-bid) then 1 else 0 end is_sell
  from p
  where ts >= trading_date + time '09:30' and ts <= trading_date + time '16:00'
)
select trading_date, option_type, bucket,
       sum(prem*is_buy) buy, sum(prem*is_sell) sell, sum(prem) tot, count(*) n
from q group by 1,2,3 order by 1,2,3
"""
d0, d1 = "2026-06-01", "2026-09-14"
with eng.connect() as c:
    df = pd.DataFrame(c.execute(text(Q), {"d0": d0, "d1": d1}).fetchall(),
                      columns=["trading_date","option_type","bucket","buy","sell","tot","n"])
for col in ("buy","sell","tot"):
    df[col] = df[col].astype(float)
df["trading_date"] = pd.to_datetime(df["trading_date"])
spy = pd.read_csv(r"C:\Users\sahin\OneDrive\Desktop\VolatilX_Research_Desk\research\reports\uoa_side_2026-09-15\drift_test_daily.csv")
spy["d"] = pd.to_datetime(spy.iloc[:,0]); spy = spy.set_index("d")["spy_intraday"]
df["bs"] = df["buy"]/(df["buy"]+df["sell"])
print(f"sessions {df.trading_date.nunique()}  prints {int(df.n.sum()):,}")
print("\nSpearman(buy-share, SPY open-to-close) by minutes-to-close bucket")
print(f"{'bucket':10s} {'call rho':>9s} {'put rho':>9s} {'n days':>7s} {'call bs':>8s} {'put bs':>8s} {'prints':>10s}")
for b in sorted(df.bucket.unique()):
    row = {}
    for ot in ("call","put"):
        s = df[(df.bucket==b)&(df.option_type==ot)].set_index("trading_date")["bs"].dropna()
        j = pd.concat([s, spy], axis=1, join="inner").dropna()
        row[ot] = (j.iloc[:,0].corr(j.iloc[:,1], method="spearman"), len(j), s.mean())
    npr = int(df[df.bucket==b].n.sum())
    print(f"{b:10s} {row['call'][0]:+9.3f} {row['put'][0]:+9.3f} {row['call'][1]:7d} {row['call'][2]:8.3f} {row['put'][2]:8.3f} {npr:10,d}")
