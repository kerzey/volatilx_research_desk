"""How many flags a day would each Tier-2 rule raise? Calibration from stored nightly UOA rows (S&P 500 universe,
2026-06-01..2026-09-14), read-only. Counts only. Rules:
  C1 contract premium today >= X            (X = 1M, 2M, 5M, 10M)
  C2 contract volume >= 10x same contract's previous-session volume, and >= 500 contracts
  C3 largest single print on a contract >= X (premium_max; X = 1M, 2M, 5M)  ~ the between-sweep jump rule
  S1 symbol premium today >= X               (X = 5M, 10M, 20M, 50M)
  S2 symbol premium today >= 20x previous session's and >= 5M  (also 10x)
"""
import os
import sys
from pathlib import Path

import pandas as pd

sys.path[:0] = [str(Path(__file__).resolve().parents[3] / "research" / "lib")]
import desk_env  # noqa: E402

desk_env.load()
from sqlalchemy import create_engine, text  # noqa: E402

engine = create_engine(os.environ["RESEARCH_DB_URL"])
D0, D1 = "2026-05-29", "2026-09-14"
with engine.connect() as c:
    con = pd.DataFrame(c.execute(text("""
        select trading_date, underlying_symbol sym, contract_symbol con, volume_traded vol, premium_total prem, premium_max pmax
        from uoa_contract_daily where trading_date between :d0 and :d1 and trade_count > 0"""), {"d0": D0, "d1": D1}).fetchall(),
        columns=["trading_date", "sym", "con", "vol", "prem", "pmax"])
    symd = pd.DataFrame(c.execute(text("""
        select trading_date, symbol sym, total_premium prem from uoa_symbol_daily
        where trading_date between :d0 and :d1"""), {"d0": D0, "d1": D1}).fetchall(), columns=["trading_date", "sym", "prem"])
for df in (con, symd):
    for col in df.columns:
        if col not in ("trading_date", "sym", "con"):
            df[col] = df[col].astype(float)
sessions = sorted(con["trading_date"].unique())
first = sessions[0]
n_sess = len(sessions) - 1  # first session is only a baseline
print(f"sessions counted: {n_sess} ({sessions[1]} .. {sessions[-1]}), symbols/session ~ {symd.groupby('trading_date').size().median():.0f}")


def per_session(mask_df, label):
    s = mask_df.groupby("trading_date").size().reindex(sessions[1:], fill_value=0)
    print(f"  {label:58s} median {s.median():6.0f}/day   p90 {s.quantile(0.9):6.0f}   max {s.max():6.0f}")


print("\nC1 — contract premium today >= X")
for x in (1e6, 2e6, 5e6, 10e6):
    per_session(con[(con.prem >= x) & (con.trading_date != first)], f"contract premium >= ${x/1e6:.0f}M")

print("\nC2 — contract volume >= k x previous session, and >= 500 contracts")
con = con.sort_values(["con", "trading_date"])
con["prev_vol"] = con.groupby("con")["vol"].shift(1)
con["prev_date"] = con.groupby("con")["trading_date"].shift(1)
# previous row must be the immediately preceding session in our list
prev_map = {sessions[i]: sessions[i - 1] for i in range(1, len(sessions))}
con["prev_ok"] = con["prev_date"] == con["trading_date"].map(prev_map)
for k in (5, 10, 20):
    m = con[con.prev_ok & (con.vol >= 500) & (con.vol >= k * con.prev_vol.clip(lower=1))]
    per_session(m, f"volume >= {k}x yesterday and >= 500")
m = con[con.prev_ok & (con.vol >= 500) & (con.vol >= 10 * con.prev_vol.clip(lower=1)) & (con.prem >= 1e6)]
per_session(m, "volume >= 10x yesterday, >= 500, and premium >= $1M")
noprev = con[(~con.prev_ok) & (con.trading_date != first) & (con.vol >= 500) & (con.prem >= 1e6)]
per_session(noprev, "no row yesterday (fresh line), >= 500 and premium >= $1M")

print("\nC3 — largest single print on a contract >= X (~ between-sweep jump)")
for x in (0.5e6, 1e6, 2e6, 5e6):
    per_session(con[(con.pmax >= x) & (con.trading_date != first)], f"largest print >= ${x/1e6:.1f}M")

print("\nS1 — symbol premium today >= X")
for x in (5e6, 10e6, 20e6, 50e6, 100e6):
    per_session(symd[(symd.prem >= x) & (symd.trading_date != first)], f"symbol premium >= ${x/1e6:.0f}M")

print("\nS2 — symbol premium >= k x previous session and >= $5M")
symd = symd.sort_values(["sym", "trading_date"])
symd["prev"] = symd.groupby("sym")["prem"].shift(1)
symd["prev_date"] = symd.groupby("sym")["trading_date"].shift(1)
symd["prev_ok"] = symd["prev_date"] == symd["trading_date"].map(prev_map)
for k in (3, 5, 10, 20):
    m = symd[symd.prev_ok & (symd.prem >= 5e6) & (symd.prem >= k * symd.prev.clip(lower=1))]
    per_session(m, f"symbol premium >= {k}x yesterday and >= $5M")
# how concentrated is the book? share of a session's premium in its top 20 symbols
top20 = symd.groupby("trading_date").apply(lambda g: g.nlargest(20, "prem")["prem"].sum() / g["prem"].sum()).reindex(sessions[1:])
print(f"\nshare of a session's premium in its top 20 symbols: median {top20.median():.2f}")
print("symbol premium percentiles ($M): " + ", ".join(f"p{p}={symd.prem.quantile(p/100)/1e6:.1f}" for p in (50, 75, 90, 95, 99)))
print("contract premium percentiles ($M): " + ", ".join(f"p{p}={con.prem.quantile(p/100)/1e6:.2f}" for p in (50, 90, 99, 99.9)))
