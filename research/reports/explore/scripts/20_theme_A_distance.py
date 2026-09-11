"""EXPLORE_001 Theme A: skill or distance?

For every published ladder level (L1..L6) at distance a ATR (from the actual pick-night close),
the control is the SAME NIGHT's unpublished candidates, graded on their own price paths for a
synthetic target at the same ATR distance, same direction as the pick, same lane window.
Per night: mean(pick hit) - mean(control hit). Nights are the unit (descriptive only, no p-values).

Also: does ATR normalisation equalise stocks? Distance curve P(touch a*ATR within w) for all
in-sample candidates, by ATR% tercile and beta tercile.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X

C = pd.read_parquet(X.WORK / "cands_ok.parquet")
P = pd.read_parquet(X.WORK / "picks_path.parquet")
Z = np.load(X.WORK / "curves.npz", allow_pickle=True)
UPc, DNc = Z["UPc"], Z["DNc"]
retro = set(pd.read_csv(X.WORK / "late_nights.csv").trading_date)
RETRO = {"2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14"}
C["row"] = np.arange(len(C))
P = P.merge(C[["trading_date", "symbol", "row"]], on=["trading_date", "symbol"])
P = P[P.has_lane_plans & ~P.trading_date.astype(str).str[:10].isin(RETRO)]
print("Theme A sample: picks", len(P), "nights", P.trading_date.nunique(), "elite", P.elite.sum(),
      "elite nights", P[P.elite].trading_date.nunique())

ctrl_rows = {d: g.row.to_numpy() for d, g in C[~C.published].groupby("trading_date")}
out = []
for r in P.itertuples():
    rows = ctrl_rows.get(r.trading_date, np.array([], int))
    for L in X.LADDER:
        a = getattr(r, f"{L}_datr", np.nan)
        if a is None or not np.isfinite(a) or a <= 0:
            continue
        w = X.LWIN[L]
        curve_ctrl = UPc[rows, w - 1] if r.bull else DNc[rows, w - 1]
        curve_own = UPc[r.row, w - 1] if r.bull else DNc[r.row, w - 1]
        out.append({"trading_date": r.trading_date, "symbol": r.symbol, "elite": r.elite, "L": L,
                    "a": a, "hit": float(curve_own >= a), "ctrl": float(np.mean(curve_ctrl >= a)),
                    "n_ctrl": len(rows), "bull": r.bull})
A = pd.DataFrame(out)
A["excess"] = A.hit - A.ctrl
A.to_parquet(X.WORK / "themeA_levels.parquet")


def nightly(df, col):
    return df.groupby("trading_date")[col].mean()


print("\n== Pick hit vs distance-matched same-night control (in-sample, exploratory — not a finding)")
print(f"{'lvl':4} {'n_pk':>5} {'nights':>6} {'medATR':>6} {'pick':>6} {'ctrl':>6} {'excess(night-avg)':>18} {'nights>0':>8}")
for L in X.LADDER + ["ALL"]:
    s = A if L == "ALL" else A[A.L == L]
    ex = nightly(s, "excess")
    print(f"{L:4} {len(s):5d} {s.trading_date.nunique():6d} {s.a.median():6.2f} {nightly(s,'hit').mean():6.2f} "
          f"{nightly(s,'ctrl').mean():6.2f} {ex.mean():+18.3f} {(ex > 0).mean():8.2f}")
print("\nElite 90+ only:")
for L in X.LADDER:
    s = A[(A.L == L) & A.elite]
    if len(s) == 0:
        continue
    print(f"{L:4} n={len(s):3d} nights={s.trading_date.nunique():3d} medATR={s.a.median():.2f} pick={s.hit.mean():.2f} "
          f"ctrl={s.ctrl.mean():.2f} excess={s.excess.mean():+.3f}")

# by distance bucket
A["abin"] = pd.cut(A.a, [0, 0.25, 0.5, 1, 2, 3, 5, 20])
print("\nBy ATR-distance bucket (all levels pooled):")
g = A.groupby("abin", observed=True).agg(n=("hit", "size"), nights=("trading_date", "nunique"),
                                         pick=("hit", "mean"), ctrl=("ctrl", "mean"), excess=("excess", "mean"))
print(g.round(3).to_string())

# direction split
print("\nBy direction:")
print(A.groupby("bull").agg(n=("hit", "size"), nights=("trading_date", "nunique"), pick=("hit", "mean"),
                            ctrl=("ctrl", "mean"), excess=("excess", "mean")).round(3))

# ---- ladder distance vs stock volatility: is the ladder placed in % terms (making vol names easy)?
print("\nLadder distance in ATR vs ATR% tercile of the pick:")
P["atr_terc"] = pd.qcut(P.atr14_px_pct, 3, labels=["lowATR", "midATR", "highATR"])
print(P.groupby("atr_terc", observed=True)[[f"{L}_datr" for L in X.LADDER]].median().round(2).to_string())
print(P.groupby("atr_terc", observed=True)[[f"{L}_dpct" for L in X.LADDER]].median().mul(100).round(2).to_string())
print("ATR% range by tercile:", P.groupby("atr_terc", observed=True).atr14_px_pct.agg(["min", "max"]).round(3).to_dict())

# ---- distance curve across all candidates: does P(touch a ATR in w) depend on vol / beta?
C["atr_terc"] = pd.qcut(C.atr14_px_pct, 3, labels=["lowATR", "midATR", "highATR"])
C["beta_terc"] = pd.qcut(C.beta60, 3, labels=["lowB", "midB", "highB"])
print("\nAll in-sample candidates (n=%d, nights=%d): P(touch +a ATR up | within w) — own-price path" %
      (len(C), C.trading_date.nunique()))
for w in (20, 60):
    for a in (0.5, 1, 2, 3, 5):
        up = UPc[:, w - 1] >= a
        dn = DNc[:, w - 1] >= a
        byv = pd.Series(up).groupby(C.atr_terc.values, observed=True).mean()
        byb = pd.Series(up).groupby(C.beta_terc.values, observed=True).mean()
        byvd = pd.Series(dn).groupby(C.atr_terc.values, observed=True).mean()
        print(f" w={w:2d} a={a}: up all={up.mean():.2f}  by ATR% {byv.round(2).to_dict()}  by beta {byb.round(2).to_dict()} | down by ATR% {byvd.round(2).to_dict()}")
# realized range / ATR by tercile
rng20 = (np.nanmax(Z["HI"][:, :20], axis=1) - np.nanmin(Z["LO"][:, :20], axis=1)) / (C.atr14_px_pct * C.raw_close_d)
print("\n20d realized range / ATR14 at selection, median by ATR% tercile:",
      pd.Series(rng20.values).groupby(C.atr_terc.values, observed=True).median().round(2).to_dict())
print("... by beta tercile:", pd.Series(rng20.values).groupby(C.beta_terc.values, observed=True).median().round(2).to_dict())
print("... published vs not:", pd.Series(rng20.values).groupby(C.published.values).median().round(2).to_dict())
