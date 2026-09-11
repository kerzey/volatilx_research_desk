"""EXPLORE_001 step 10: path metrics for every in-sample candidate and the published ladder.

Reference price = actual raw close on the pick night (raw_close_d). The platform's entry_ref is
context spot_close, which is stale on 2026-05-13/14 (see 05b); the actual close is what a
subscriber could trade against. Distances are in ATR14 computed from split-adjusted bars up to
and including the pick night (atr14_px_pct) — the platform's atr_pct is corrupted around splits.

Outputs (work/):
  curves.npz     per-candidate cumulative MFE/MAE in ATR units, up and down, k=1..60
  picks_path.parquet  per published pick: ladder distances, first-touch days, counter touches,
                      path shape, realized range.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X

C = pd.read_parquet(X.WORK / "cands.parquet")
FWD = pd.read_parquet(X.WORK / "fwd.parquet")
C = C[C.price_ok.fillna(False) & C.atr14_px_pct.notna()].reset_index(drop=True)
C["ref"] = C.raw_close_d
C["atr_px"] = C.atr14_px_pct * C.ref

# ---- cumulative excursion curves (ATR units) for every candidate
FWD = FWD.sort_values(["trading_date", "symbol", "k"])
key = FWD.set_index(["trading_date", "symbol"])
n = len(C)
UP = np.full((n, 60), np.nan); DN = np.full((n, 60), np.nan); CL = np.full((n, 60), np.nan)
HI = np.full((n, 60), np.nan); LO = np.full((n, 60), np.nan)
grp = {k: g for k, g in FWD.groupby(["trading_date", "symbol"])}
for i, r in enumerate(C.itertuples()):
    g = grp.get((r.trading_date, r.symbol))
    if g is None:
        continue
    kk = g.k.to_numpy() - 1
    HI[i, kk] = g.h.to_numpy(); LO[i, kk] = g.l.to_numpy(); CL[i, kk] = g.c.to_numpy()
    UP[i, kk] = (g.h.to_numpy() / r.ref - 1) / r.atr14_px_pct
    DN[i, kk] = (1 - g.l.to_numpy() / r.ref) / r.atr14_px_pct
UPc = np.fmax.accumulate(np.nan_to_num(UP, nan=-np.inf), axis=1)
DNc = np.fmax.accumulate(np.nan_to_num(DN, nan=-np.inf), axis=1)
np.savez_compressed(X.WORK / "curves.npz", UP=UP, DN=DN, UPc=UPc, DNc=DNc, CL=CL, HI=HI, LO=LO,
                    trading_date=C.trading_date.astype(str).to_numpy(), symbol=C.symbol.to_numpy())
C.to_parquet(X.WORK / "cands_ok.parquet")
print("candidates with curves:", n, " published:", C.published.sum())

# ---- per-pick ladder metrics
P = C[C.published].copy()
idx = P.index.to_numpy()
rows = []
for i, r in zip(idx, P.itertuples()):
    bull = bool(r.bull)
    fav = UPc[i] if bull else DNc[i]   # favorable excursion (ATR) running max
    adv = DNc[i] if bull else UPc[i]
    rec = {"trading_date": r.trading_date, "symbol": r.symbol}
    for L in X.LADDER:
        lv = getattr(r, L)
        if lv is None or not np.isfinite(lv if lv is not None else np.nan):
            continue
        dist_pct = (lv / r.ref - 1) * (1 if bull else -1)
        a = dist_pct / r.atr14_px_pct
        rec[f"{L}_dpct"] = dist_pct
        rec[f"{L}_datr"] = a
        w = X.LWIN[L]
        hitk = np.flatnonzero(fav >= a)
        k1 = int(hitk[0]) + 1 if len(hitk) else None
        rec[f"{L}_k"] = k1                                   # first touch within 60
        rec[f"{L}_hit"] = (k1 is not None and k1 <= w) if a > 0 else np.nan   # within lane window
        rec[f"{L}_passed_at_close"] = a <= 0
    for ck in X.COUNTER_KEYS:
        lv = getattr(r, ck)
        if lv is None or not np.isfinite(lv):
            continue
        dist_pct = (1 - lv / r.ref) * (1 if bull else -1)    # adverse distance (positive = on adverse side)
        a = dist_pct / r.atr14_px_pct
        rec[f"{ck}_datr"] = a
        if a <= 0:
            rec[f"{ck}_k"] = np.nan
            continue
        hk = np.flatnonzero(adv >= a)
        rec[f"{ck}_k"] = int(hk[0]) + 1 if len(hk) else np.nan
    for st in ("day_stop", "swing_stop", "long_stop"):
        lv = getattr(r, st)
        if lv is None or not np.isfinite(lv):
            continue
        a = (1 - lv / r.ref) * (1 if bull else -1) / r.atr14_px_pct
        rec[f"{st}_datr"] = a
        hk = np.flatnonzero(adv >= a) if a > 0 else []
        rec[f"{st}_k"] = int(hk[0]) + 1 if len(hk) else np.nan
    # generic excursions
    for w in (5, 20, 40, 60):
        rec[f"mfe{w}_atr"] = fav[w - 1]
        rec[f"mae{w}_atr"] = adv[w - 1]
        rec[f"range{w}_atr"] = (np.nanmax(HI[i, :w]) - np.nanmin(LO[i, :w])) / r.atr_px
        rec[f"ret{w}"] = (CL[i, w - 1] / r.ref - 1) * (1 if bull else -1)
    rec["ret_open_to_20"] = np.nan
    rows.append(rec)
PP = pd.DataFrame(rows)
P = P.merge(PP, on=["trading_date", "symbol"], how="left")

# ---- path shape (called direction = "up"). First favorable = first ladder touch (any L, within 60);
#      first adverse = first counter-level touch (any of the 6 counter levels, within 60).
kL = P[[f"{L}_k" for L in X.LADDER]].min(axis=1)
kC = P[[f"{c}_k" for c in X.COUNTER_KEYS if f"{c}_k" in P]].min(axis=1)
P["first_fav_k"] = kL
P["first_ctr_k"] = kC


def shape(a, b):
    if np.isnan(a) and np.isnan(b):
        return "neither"
    if np.isnan(b):
        return "up_only"
    if np.isnan(a):
        return "down_only"
    if a < b:
        return "up_then_down"
    if b < a:
        return "down_then_up"
    return "same_day"


P["shape_ladder"] = [shape(a, b) for a, b in zip(kL, kC)]
# model-free symmetric version: +/-1.5 ATR and +/-2 ATR within 20 and 60 days
for thr in (1.0, 1.5, 2.0, 3.0):
    for w in (20, 60):
        ku, kd = [], []
        for i, r in zip(idx, P.itertuples()):
            fav = UPc[i] if r.bull else DNc[i]
            adv = DNc[i] if r.bull else UPc[i]
            a = np.flatnonzero(fav[:w] >= thr); b = np.flatnonzero(adv[:w] >= thr)
            ku.append(a[0] + 1 if len(a) else np.nan); kd.append(b[0] + 1 if len(b) else np.nan)
        P[f"sym{thr}_{w}_shape"] = [shape(a, b) for a, b in zip(ku, kd)]
        P[f"sym{thr}_{w}_kfav"] = ku
        P[f"sym{thr}_{w}_kadv"] = kd
P.to_parquet(X.WORK / "picks_path.parquet")

lad = P[P.has_lane_plans]
print("\nladder picks:", len(lad), "nights:", lad.trading_date.nunique())
print("\nLadder distance (ATR multiples, from actual close) — median [p25,p75]:")
for L in X.LADDER:
    s = lad[f"{L}_datr"]
    print(f"  {L}: median {s.median():.2f} [{s.quantile(.25):.2f}, {s.quantile(.75):.2f}]  "
          f"%dist median {100*lad[f'{L}_dpct'].median():.2f}%  passed-at-close {int((s <= 0).sum())}  "
          f"hit-in-window {lad[f'{L}_hit'].mean():.2f}")
print("\ncounter distance (ATR):", {c: round(lad[f'{c}_datr'].median(), 2) for c in X.COUNTER_KEYS})
print("counter hit within 60 (share):", {c: round(lad[f'{c}_k'].notna().mean(), 2) for c in X.COUNTER_KEYS})
print("\nshape (ladder vs counter levels):\n", lad.shape_ladder.value_counts())
for thr in (1.5, 2.0):
    print(f"\nsymmetric ±{thr} ATR 20d:\n", P[f"sym{thr}_20_shape"].value_counts())
