"""EXPLORE_001 Theme A (cont.): is the pick excess just beta / momentum / vol exposure?

Control 2 = the 10 nearest same-night unpublished candidates in standardized
(beta60, atr14_px_pct, ret20_pre), all known by 16:05 on the pick night. Same synthetic-target
grading as step 20. Also compares pick vs candidate characteristics.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
RETRO = {"2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14"}
C = pd.read_parquet(X.WORK / "cands_ok.parquet")
P = pd.read_parquet(X.WORK / "picks_path.parquet")
Z = np.load(X.WORK / "curves.npz", allow_pickle=True)
UPc, DNc = Z["UPc"], Z["DNc"]
C["row"] = np.arange(len(C))
P = P.merge(C[["trading_date", "symbol", "row"]], on=["trading_date", "symbol"])
P = P[P.has_lane_plans & ~P.trading_date.astype(str).str[:10].isin(RETRO)]

print("Characteristics, published vs unpublished (median):")
cols = ["beta60", "atr14_px_pct", "ret20_pre", "ret5_pre", "rv20", "dist_20d_high", "overall_score"]
print(C.groupby("published")[cols].median().round(3).to_string())

feats = ["beta60", "atr14_px_pct", "ret20_pre"]
Cz = C.copy()
for f in feats:
    Cz[f + "_z"] = (C[f] - C[f].mean()) / C[f].std()
zc = [f + "_z" for f in feats]
out = []
for r in P.itertuples():
    pool = Cz[(Cz.trading_date == r.trading_date) & ~Cz.published].dropna(subset=zc)
    me = Cz.loc[Cz.row == r.row, zc].to_numpy()[0]
    if np.isnan(me).any() or len(pool) < 10:
        continue
    dd = np.sqrt(((pool[zc].to_numpy() - me) ** 2).sum(axis=1))
    nn = pool.row.to_numpy()[np.argsort(dd)[:10]]
    for L in X.LADDER:
        a = getattr(r, f"{L}_datr", np.nan)
        if a is None or not np.isfinite(a) or a <= 0:
            continue
        w = X.LWIN[L]
        cc = UPc[nn, w - 1] if r.bull else DNc[nn, w - 1]
        own = UPc[r.row, w - 1] if r.bull else DNc[r.row, w - 1]
        out.append({"trading_date": r.trading_date, "symbol": r.symbol, "elite": r.elite, "bull": r.bull,
                    "L": L, "a": a, "hit": float(own >= a), "ctrl_nn": float(np.mean(cc >= a))})
B = pd.DataFrame(out)
B["excess_nn"] = B.hit - B.ctrl_nn
B.to_parquet(X.WORK / "themeA_matched.parquet")
print("\n== Pick vs beta/ATR%/momentum-matched same-night control (in-sample, exploratory — not a finding)")
print(f"picks {B.symbol.groupby(B.trading_date).nunique().sum()} nights {B.trading_date.nunique()}")
for L in X.LADDER + ["ALL"]:
    s = B if L == "ALL" else B[B.L == L]
    ex = s.groupby("trading_date").excess_nn.mean()
    print(f"{L:4} n={len(s):4d} nights={s.trading_date.nunique():3d} pick={s.groupby('trading_date').hit.mean().mean():.2f} "
          f"ctrl_nn={s.groupby('trading_date').ctrl_nn.mean().mean():.2f} excess={ex.mean():+.3f} nights>0={(ex>0).mean():.2f}")
print("\nBull only:")
for L in X.LADDER:
    s = B[(B.L == L) & B.bull]
    print(f"{L:4} n={len(s):4d} pick={s.hit.mean():.2f} ctrl_nn={s.ctrl_nn.mean():.2f} excess={s.excess_nn.mean():+.3f}")
print(chr(10) + "Elite (n picks=%d):" % len(B[B.elite].drop_duplicates(["trading_date", "symbol"])))
for L in X.LADDER:
    s = B[(B.L == L) & B.elite]
    print(f"{L:4} n={len(s):3d} nights={s.trading_date.nunique()} pick={s.hit.mean():.2f} ctrl_nn={s.ctrl_nn.mean():.2f} excess={s.excess_nn.mean():+.3f}")
# first half vs second half of in-sample
B["half"] = np.where(B.trading_date < pd.Timestamp("2026-05-01"), "Apr", "May")
print("\nBy month (ALL levels):", B.groupby("half").agg(n=("hit", "size"), nights=("trading_date", "nunique"),
      pick=("hit", "mean"), ctrl=("ctrl_nn", "mean"), excess=("excess_nn", "mean")).round(3).to_dict("index"))
