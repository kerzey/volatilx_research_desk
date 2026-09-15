"""Composition control: same contract-days, prints early (>3h to close) vs late (<30m)."""
import os, sys
import pandas as pd
sys.path[:0] = [r"C:\Users\sahin\OneDrive\Desktop\VolatilX_Research_Desk\research\lib"]
import desk_env; desk_env.load()
from sqlalchemy import create_engine, text
eng = create_engine(os.environ["RESEARCH_DB_URL"])
Q = """
with p as (
  select c.trading_date, c.contract_symbol, c.option_type, c.bid, c.ask,
         (t->>'p')::float price, (t->>'s')::float size,
         extract(epoch from ((c.trading_date + time '16:00') -
             ((t->>'t')::timestamptz at time zone 'America/New_York')))/60.0 ttc
  from uoa_contract_daily c, jsonb_array_elements(c.top_trades_json::jsonb) t
  where c.trading_date >= :d0 and c.trading_date <= :d1
    and c.trade_count > 0 and c.premium_total >= 100000 and c.ask > c.bid and c.bid > 0
), q as (
  select trading_date, contract_symbol, option_type,
         case when ttc < 30 then 'late' when ttc > 180 then 'early' else null end leg,
         price*size*100 prem,
         case when price >= ask - 0.10*(ask-bid) then 1 else 0 end is_buy,
         case when price <= bid + 0.10*(ask-bid) then 1 else 0 end is_sell
  from p where ttc between 0 and 390
), bb as (
  select trading_date, contract_symbol from q where leg is not null
  group by 1,2 having count(distinct leg) = 2
)
select q.trading_date, q.option_type, q.leg,
       sum(q.prem*q.is_buy) buy, sum(q.prem*q.is_sell) sell, count(*) n
from q join bb b on b.trading_date=q.trading_date and b.contract_symbol=q.contract_symbol
where q.leg is not null group by 1,2,3 order by 1,2,3
"""
with eng.connect() as c:
    df = pd.DataFrame(c.execute(text(Q), {"d0":"2026-06-01","d1":"2026-09-14"}).fetchall(),
                      columns=["trading_date","option_type","leg","buy","sell","n"])
for col in ("buy","sell"): df[col]=df[col].astype(float)
df["trading_date"]=pd.to_datetime(df["trading_date"])
spy = pd.read_csv(r"C:\Users\sahin\OneDrive\Desktop\VolatilX_Research_Desk\research\reports\uoa_side_2026-09-15\drift_test_daily.csv")
spy["d"]=pd.to_datetime(spy.iloc[:,0]); spy=spy.set_index("d")["spy_intraday"]
df["bs"]=df["buy"]/(df["buy"]+df["sell"])
print(f"same-contract sample: sessions {df.trading_date.nunique()}  prints {int(df.n.sum()):,}")
for leg in ("early","late"):
    out=[]
    for ot in ("call","put"):
        s=df[(df.leg==leg)&(df.option_type==ot)].set_index("trading_date")["bs"].dropna()
        j=pd.concat([s,spy],axis=1,join="inner").dropna()
        out.append(f"{ot} rho {j.iloc[:,0].corr(j.iloc[:,1],method='spearman'):+.3f} (days {len(j)}, mean bs {s.mean():.3f})")
    print(f"{leg:6s}: " + " | ".join(out))
