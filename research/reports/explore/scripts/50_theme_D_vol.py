"""EXPLORE_001 Theme D: volatility harvest.

(1) Realized range over the window vs ATR at selection: picks vs same-night unpublished candidates.
(2) Two-sided moves, model-free: touches BOTH +k ATR and -k ATR (called direction for picks,
    candidate's own dominant direction for unpublished) — k=1.5 within 20d, k=2 within 60d.
(3) What, known by 16:05, goes with a two-sided move? ATR%, beta, prior vol expansion,
    run-up, earnings inside the window (corrected report dates — knowledge-time caveat),
    GEX regime / pin risk, UOA premium, published flag. All candidates (bigger n), then picks.
Retro nights excluded.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
RETRO = {"2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14"}
C = pd.read_parquet(X.WORK / "cands_ok.parquet")
Z = np.load(X.WORK / "curves.npz", allow_pickle=True)
UPc, DNc, HI, LO, CL = Z["UPc"], Z["DNc"], Z["HI"], Z["LO"], Z["CL"]
C["row"] = np.arange(len(C))
C = C[~C.trading_date.astype(str).str[:10].isin(RETRO)].copy()
book = X.PathBook(X.load_prices())
r = C.row.to_numpy()
bull = C.bull.to_numpy()
fav = np.where(bull[:, None], UPc[r], DNc[r]); adv = np.where(bull[:, None], DNc[r], UPc[r])


def first_k(M, thr, w):
    hit = M[:, :w] >= thr
    k = np.where(hit.any(axis=1), hit.argmax(axis=1) + 1, np.nan)
    return k


for thr, w, tag in ((1.5, 20, "s20"), (2.0, 60, "s60"), (1.0, 20, "s1_20")):
    kf, ka = first_k(fav, thr, w), first_k(adv, thr, w)
    C[f"two_{tag}"] = ~np.isnan(kf) & ~np.isnan(ka)
    C[f"utd_{tag}"] = C[f"two_{tag}"] & (np.nan_to_num(kf, nan=99) < np.nan_to_num(ka, nan=99))
    C[f"fav_{tag}"] = ~np.isnan(kf)
C["range20_atr"] = (np.nanmax(HI[r, :20], axis=1) - np.nanmin(LO[r, :20], axis=1)) / (C.atr14_px_pct * C.raw_close_d)
C["range60_atr"] = (np.nanmax(HI[r, :60], axis=1) - np.nanmin(LO[r, :60], axis=1)) / (C.atr14_px_pct * C.raw_close_d)
# realized daily vol over next 20d vs ATR (vol expansion ratio)
rets = np.diff(np.log(np.column_stack([C.raw_close_d.to_numpy(), CL[r, :20]])), axis=1)
C["fwd_rv20"] = np.nanstd(rets, axis=1) * np.sqrt(252)
C["vol_exp"] = C.fwd_rv20 / C.rv20

# features known at 16:05
C["rv_to_atr"] = C.rv20 / (C.atr14_px_pct * np.sqrt(252))
ed = C.trading_date + pd.to_timedelta(C.days_to_earnings_corrected, unit="D")
C["earn_td"] = [np.searchsorted(book.cal, e) - book.pos[d] if pd.notna(e) else np.nan for e, d in zip(ed, C.trading_date)]
C["earn_in_20"] = C.earn_td.between(0, 20)   # 0 = reports on the pick night itself (after close)
C["earn_known"] = C.days_to_earnings_corrected.notna()
C["gex_cat"] = C.gex_regime.fillna("none").astype(str)
C["pin"] = C.gex_pin_risk.map({True: "pin", False: "nopin"}).fillna("none")
C["log_prem"] = np.log10(C.flow_total_premium.clip(lower=1))
print("Theme D sample (all candidates, retro nights excluded): n", len(C), "nights", C.trading_date.nunique(),
      "| published", C.published.sum(), "nights", C[C.published].trading_date.nunique())

print("\n== Realized range / ATR at selection (median) and forward/backward vol ratio")
t = C.groupby("published").agg(n=("symbol", "size"), range20=("range20_atr", "median"), range60=("range60_atr", "median"),
                               vol_exp=("vol_exp", "median"), two_s20=("two_s20", "mean"), two_s60=("two_s60", "mean"),
                               utd_s60=("utd_s60", "mean"), fav_s20=("fav_s20", "mean"))
print(t.round(3).to_string())
# per-night paired difference published - unpublished
nd = C.groupby(["trading_date", "published"])[["range20_atr", "two_s20", "two_s60", "vol_exp"]].mean().unstack()
for col in ["range20_atr", "two_s20", "two_s60", "vol_exp"]:
    dif = (nd[(col, True)] - nd[(col, False)]).dropna()
    print(f"  per-night published minus unpublished {col}: mean {dif.mean():+.3f}, nights>0 {np.mean(dif>0):.2f} (nights {len(dif)})")

feats = {"atr_terc": pd.qcut(C.atr14_px_pct, 3, labels=["lo", "mid", "hi"]),
         "beta_terc": pd.qcut(C.beta60, 3, labels=["lo", "mid", "hi"]),
         "rv_to_atr_terc": pd.qcut(C.rv_to_atr, 3, labels=["lo", "mid", "hi"]),
         "run20_terc": pd.qcut(C.ret20_pre, 3, labels=["lo", "mid", "hi"]),
         "earn_in_20": C.earn_in_20.where(C.earn_known, other=np.nan).map({True: "earn<=20td", False: "no_earn<=20td"}).fillna("unknown"),
         "gex": C.gex_cat, "pin": C.pin,
         "prem_terc": pd.qcut(C.log_prem, 3, labels=["lo", "mid", "hi"]),
         "score_band": pd.cut(C.overall_score, [0, 60, 65, 70, 80, 90, 101], right=False)}
for name, f in feats.items():
    for pop, mask in (("ALL", np.ones(len(C), bool)), ("PUB", C.published.to_numpy())):
        sub = C[mask]
        g = sub.groupby(f[mask], observed=True)
        t = pd.DataFrame({"n": g.size(), "nights": g.trading_date.nunique(), "range20": g.range20_atr.median(),
                          "two_s20": g.two_s20.mean(), "two_s60": g.two_s60.mean(), "utd_s60": g.utd_s60.mean(),
                          "vol_exp": g.vol_exp.median()})
        print(f"\n-- {pop} by {name}\n{t.round(2).to_string()}")

# industry (published only, top)
g = C[C.published].groupby("industry")
t = pd.DataFrame({"n": g.size(), "nights": g.trading_date.nunique(), "two_s60": g.two_s60.mean(), "range20": g.range20_atr.median()})
print("\n-- PUB by industry (n>=12)\n", t[t.n >= 12].sort_values("two_s60").round(2).to_string())
C.drop(columns=[]).to_parquet(X.WORK / "themeD.parquet")
