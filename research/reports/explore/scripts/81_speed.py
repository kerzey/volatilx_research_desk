"""EXPLORE_001 step 81: speed — days to first touch for picks vs beta/ATR/momentum-matched same-night
control at the same ATR distance (from the pick-night close), conditional on touching within 40 sessions.
Retro nights excluded. Descriptive."""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
RETRO = {"2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14"}
C = pd.read_parquet(X.WORK / "cands_ok.parquet"); C["row"] = np.arange(len(C))
P = pd.read_parquet(X.WORK / "picks_path.parquet").merge(C[["trading_date", "symbol", "row"]], on=["trading_date", "symbol"])
P = P[P.has_lane_plans & ~P.trading_date.astype(str).str[:10].isin(RETRO)]
Z = np.load(X.WORK / "curves.npz", allow_pickle=True); UPc, DNc = Z["UPc"], Z["DNc"]
feats = ["beta60", "atr14_px_pct", "ret20_pre"]
Cz = C.dropna(subset=feats).copy()
for f in feats:
    Cz[f + "_z"] = (Cz[f] - Cz[f].mean()) / Cz[f].std()
zc = [f + "_z" for f in feats]
def kfirst(curve, a, w=40):
    ix = np.flatnonzero(curve[:w] >= a)
    return ix[0] + 1 if len(ix) else np.nan
rows = []
for r in P.itertuples():
    pool = Cz[(Cz.trading_date == r.trading_date) & ~Cz.published]
    me = Cz.loc[Cz.row == r.row, zc]
    if len(me) == 0: continue
    dd = np.sqrt(((pool[zc].to_numpy() - me.to_numpy()[0]) ** 2).sum(axis=1))
    nn = pool.row.to_numpy()[np.argsort(dd)[:10]]
    for L in ("L2", "L3", "L4"):
        a = getattr(r, f"{L}_datr")
        if not np.isfinite(a) or a <= 0: continue
        own = kfirst(UPc[r.row] if r.bull else DNc[r.row], a)
        ctr = [kfirst(UPc[j] if r.bull else DNc[j], a) for j in nn]
        rows.append({"trading_date": r.trading_date, "L": L, "a": a, "k_pick": own, "k_ctrl_med": np.nanmedian(ctr) if np.isfinite(ctr).any() else np.nan,
                     "hit_pick": np.isfinite(own), "hit_ctrl": np.mean(np.isfinite(ctr))})
S = pd.DataFrame(rows)
print("picks", P.shape[0], "nights", S.trading_date.nunique())
for L in ("L2", "L3", "L4"):
    s = S[S.L == L]
    print(f"{L}: median dist {s.a.median():.2f} ATR | touch<=40 pick {s.hit_pick.mean():.2f} ctrl {s.hit_ctrl.mean():.2f} | "
          f"median days-to-touch (if touched) pick {s.k_pick.median():.1f} vs ctrl {s.k_ctrl_med.median():.1f} | "
          f"share within 5 sessions: pick {np.mean(s.k_pick <= 5):.2f}")
