"""EXPLORE_001 Theme B: entry timing as Haci enters.

Entries (signal-date basis), published picks with lane plans, retro nights excluded:
  E_close : actual pick-night close (reference; not actionable — SAS publishes after the close)
  E_ah    : close of the after-hours hourly bar in which SAS finished (actionable nights only)
  E_open  : next-day regular open
  E_10    : next-day 10:00 ET price (close of the 13:00 UTC bar)
  E_11    : next-day 11:00 ET price (close of the 14:00 UTC bar)
Direction-adjusted: positive = in the pick's favour. All descriptive.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
pd.set_option("display.width", 220)
RETRO = {"2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14"}
P = pd.read_parquet(X.WORK / "picks_path.parquet")
E = pd.read_parquet(X.WORK / "entries.parquet")
C = pd.read_parquet(X.WORK / "cands_ok.parquet")
Z = np.load(X.WORK / "curves.npz", allow_pickle=True)
HI, LO, CL = Z["HI"], Z["LO"], Z["CL"]
C["row"] = np.arange(len(C))
P = P.merge(C[["trading_date", "symbol", "row"]], on=["trading_date", "symbol"]).merge(E, on=["trading_date", "symbol"], how="left")
P = P[P.has_lane_plans & ~P.trading_date.astype(str).str[:10].isin(RETRO)].copy()
sgn = np.where(P.bull, 1.0, -1.0)
P["sgn"] = sgn
P["E_close"] = P.ref
P["E_ah"] = P.E_ah_pub
atr = P.atr14_px_pct
for e in ("E_ah", "E_open", "E_10", "E_11"):
    P[f"{e}_move_atr"] = sgn * (P[e] / P.ref - 1) / atr     # how far price moved in favour before entry
P["ah_to_open_atr"] = sgn * (P.E_open / P.E_ah - 1) / atr
P["open_to_10_atr"] = sgn * (P.E_10 / P.E_open - 1) / atr
P["gap_pct"] = sgn * (P.E_open / P.ref - 1)
print("Theme B sample: picks", len(P), "nights", P.trading_date.nunique(), "| AH-actionable picks with AH price:",
      P.E_ah.notna().sum(), "nights", P[P.E_ah.notna()].trading_date.nunique())
print("elite:", P.elite.sum(), "elite with AH price:", (P.elite & P.E_ah.notna()).sum())

print("\n== Price at each entry vs pick-night close, in ATR, direction-adjusted (+ = already moved in favour)")
for e in ("E_ah", "E_open", "E_10", "E_11"):
    s = P[f"{e}_move_atr"].dropna()
    print(f"{e:7} n={len(s):3d} median={s.median():+.3f} mean={s.mean():+.3f} share>0={np.mean(s>0):.2f}")
s = P.ah_to_open_atr.dropna()
print(f"AH->open  n={len(s)} median={s.median():+.3f} mean={s.mean():+.3f} share>0 (open better for the pick than AH, i.e. AH was cheaper)={np.mean(s>0):.2f}")
s = P.open_to_10_atr.dropna()
print(f"open->10  n={len(s)} median={s.median():+.3f} mean={s.mean():+.3f} share>0={np.mean(s>0):.2f}")
print("gap (open vs close, %):", P.gap_pct.describe(percentiles=[.1, .25, .5, .75, .9]).round(4).to_dict())

# ---- levels already passed at each entry (target no longer available to that entry)
print("\n== Share of ladder levels already passed at entry")
rows = []
for e in ("E_close", "E_ah", "E_open", "E_10", "E_11"):
    rec = {"entry": e, "n": P[e].notna().sum()}
    for L in X.LADDER:
        lv = P[L]
        ok = P[e].notna() & lv.notna()
        passed = (P.sgn * (P[e] - lv) >= 0)
        if e == "E_10":   # also passed if touched between open and 10:00
            passed = passed | np.where(P.bull, P.b13_h >= lv, P.b13_l <= lv) | (P.sgn * (P.E_open - lv) >= 0)
        if e == "E_11":
            passed = passed | np.where(P.bull, P.b13_h >= lv, P.b13_l <= lv) | (P.sgn * (P.E_open - lv) >= 0)
        rec[L] = passed[ok].mean()
    rows.append(rec)
print(pd.DataFrame(rows).round(3).to_string(index=False))
for grp, sub in (("elite", P[P.elite]), ("non-elite", P[~P.elite])):
    print(f"  {grp}: L1 passed at open {np.mean(sub.sgn*(sub.E_open-sub.L1)>=0):.2f} (n={len(sub)}), "
          f"L2 {np.mean(sub.sgn*(sub.E_open-sub.L2)>=0):.2f}, L3 {np.mean(sub.sgn*(sub.E_open-sub.L3)>=0):.2f}")

# ---- Haci's AH partial fill: did it hurt? compare AH price to next-day low (bull) / high (bear)
Q = P[P.E_ah.notna()].copy()
Q["d1_adverse_vs_ah_atr"] = np.where(Q.bull, (Q.d1_l / Q.E_ah - 1), (1 - Q.d1_h / Q.E_ah)) / Q.atr14_px_pct
Q["d1_close_vs_ah_atr"] = Q.sgn * (Q.d1_c / Q.E_ah - 1) / Q.atr14_px_pct
Q["d1_close_vs_open_atr"] = Q.sgn * (Q.d1_c / Q.E_open - 1) / Q.atr14_px_pct
print("\n== After-hours entry vs day 1 (actionable nights, n=%d picks, %d nights)" % (len(Q), Q.trading_date.nunique()))
for grp, sub in (("all", Q), ("elite", Q[Q.elite]), ("non-elite", Q[~Q.elite])):
    print(f" {grp:9} n={len(sub):3d} nights={sub.trading_date.nunique():2d}  day-1 went below AH price by >=0.25 ATR: "
          f"{np.mean(sub.d1_adverse_vs_ah_atr <= -0.25):.2f}  day-1 close better than AH: {np.mean(sub.d1_close_vs_ah_atr > 0):.2f}  "
          f"median AH->d1close {sub.d1_close_vs_ah_atr.median():+.2f} ATR  median open->d1close {sub.d1_close_vs_open_atr.median():+.2f} ATR")

# ---- entry cost to deep targets: from each entry, fixed-horizon direction-adjusted return (secondary)
print("\n== Direction-adjusted close-to-close from entry (secondary; in-sample, exploratory — not a finding)")
for h in (1, 5, 10, 20):
    ck = np.array([CL[r, h - 1] for r in P.row])
    line = f" T+{h:2d}: "
    for e in ("E_close", "E_ah", "E_open", "E_10"):
        v = P.sgn * (ck / P[e] - 1)
        line += f"{e}={np.nanmedian(v)*100:+.2f}% (n={v.notna().sum()})  "
    print(line)

# ---- gap buckets vs path (seed H-030 context)
P["gap_atr"] = P.E_open_move_atr
P["gap_bin"] = pd.cut(P.gap_atr, [-10, -0.25, 0.25, 0.75, 10], labels=["gap_against", "flat", "gap_favour", "big_gap_favour"])
print("\n== Day-1 gap (ATR) vs path from the OPEN — L3/L5 reached after open, MAE from open (20d)")
res = []
for r in P.itertuples():
    o = r.E_open
    lo20 = np.nanmin(LO[r.row, :20]); hi20 = np.nanmax(HI[r.row, :20])
    mae_o = ((lo20 / o - 1) if r.bull else (1 - hi20 / o)) / r.atr14_px_pct
    hitL3 = (np.nanmax(HI[r.row, :40]) >= r.L3) if r.bull else (np.nanmin(LO[r.row, :40]) <= r.L3)
    passedL3 = r.sgn * (o - r.L3) >= 0
    res.append((mae_o, hitL3 and not passedL3))
P["mae20_from_open_atr"], P["L3_after_open"] = zip(*res)
print(P.groupby("gap_bin", observed=True).agg(n=("symbol", "size"), nights=("trading_date", "nunique"),
      L3_after_open=("L3_after_open", "mean"), mae20_open_med=("mae20_from_open_atr", "median"),
      elite=("elite", "sum")).round(3).to_string())

# ---- AH liquidity
print("\nAH bars/volume at the publication bar: median AH volume", Q.ah_vol.median(), " picks with no AH bar after publication:",
      int(((P.actionable == 'ah') & P.E_ah.isna()).sum()))
print("publication bar hour (UTC) distribution:", P.E_ah_pub_hr.value_counts().to_dict())
P.to_parquet(X.WORK / "themeB.parquet")
