"""EXPLORE_001 Theme C: path shape, both directions.

Three scales, each pairing a called-direction ladder level with the counter level of the same lane
(counter levels = the report's opposite-direction setup targets, sas_excursion.counter_levels_json,
built at volatilx services/sas_excursion.py:269-287):
  day   : L1 vs day_c1   within 20 trading days
  swing : L3 vs swing_c1 within 40
  long  : L5 vs long_c1  within 60
plus a model-free symmetric version: +/-1.5 ATR within 20, +/-2 ATR within 60.
Same-day ties are ordered with next-day hourly regular-session bars when available.
Also: drawdown before L1, time L1->L3, recovery after a swing-scale counter touch.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
RETRO = {"2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14"}
P = pd.read_parquet(X.WORK / "themeB.parquet")
Z = np.load(X.WORK / "curves.npz", allow_pickle=True)
HI, LO = Z["HI"], Z["LO"]
prices = X.load_prices()
book = X.PathBook(prices)
fmap = prices.set_index(["symbol", "date"])["f"]
H = X.load_hourly()
H = H[H.symbol.isin(P.symbol.unique()) & H.hr.between(13, 19)]
Hg = {k: g.sort_values("t") for k, g in H.groupby(["symbol", "d"])}


def order_same_day(sym, d, k, fav_level, adv_level, bull):
    """Return 'fav', 'adv' or 'tie' for which level was touched first on trading day k."""
    dk = book.cal[book.pos[d] + k]
    g = Hg.get((sym, dk))
    if g is None:
        return "tie"
    adj = fmap.get((sym, d), np.nan) / fmap.get((sym, dk), np.nan)
    for b in g.itertuples():
        h, l = b.h * adj, b.l * adj
        f = (h >= fav_level) if bull else (l <= fav_level)
        a = (l <= adv_level) if bull else (h >= adv_level)
        if f and a:
            return "tie"
        if f:
            return "fav"
        if a:
            return "adv"
    return "tie"


def first_k(row_i, level, bull, favorable, w):
    if level is None or not np.isfinite(level):
        return np.nan
    up = (bull and favorable) or (not bull and not favorable)
    arr = HI[row_i, :w] >= level if up else LO[row_i, :w] <= level
    ix = np.flatnonzero(arr)
    return ix[0] + 1 if len(ix) else np.nan


SCALES = {"day": ("L1", "day_c1", 20), "swing": ("L3", "swing_c1", 40), "long": ("L5", "long_c1", 60)}
for sc, (fl, cl, w) in SCALES.items():
    shapes, kf_l, ka_l = [], [], []
    for r in P.itertuples():
        fav_lv, adv_lv = getattr(r, fl), getattr(r, cl)
        # counter level must be on the adverse side of the close to count
        if adv_lv is not None and np.isfinite(adv_lv) and r.sgn * (adv_lv - r.ref) >= 0:
            adv_lv = np.nan
        if fav_lv is not None and np.isfinite(fav_lv) and r.sgn * (fav_lv - r.ref) <= 0:
            fav_lv = np.nan
        kf = first_k(r.row, fav_lv, r.bull, True, w)
        ka = first_k(r.row, adv_lv, r.bull, False, w)
        if np.isnan(kf) and np.isnan(ka):
            s = "neither"
        elif np.isnan(ka):
            # did it come back down to the counter level AFTER the window of the fav touch? (still within w)
            s = "up_only"
        elif np.isnan(kf):
            s = "down_only"
        elif kf < ka:
            s = "up_then_down"
        elif ka < kf:
            s = "down_then_up"
        else:
            o = order_same_day(r.symbol, r.trading_date, int(kf), fav_lv, adv_lv, r.bull)
            s = {"fav": "up_then_down", "adv": "down_then_up", "tie": "same_bar"}[o]
        shapes.append(s); kf_l.append(kf); ka_l.append(ka)
    P[f"shape_{sc}"] = shapes; P[f"kf_{sc}"] = kf_l; P[f"ka_{sc}"] = ka_l

print("Theme C sample: picks", len(P), "nights", P.trading_date.nunique())
for sc in SCALES:
    print(f"\n{sc} scale ({SCALES[sc][0]} vs {SCALES[sc][1]}, {SCALES[sc][2]}d): median fav dist "
          f"{P[SCALES[sc][0] + '_datr'].median():.2f} ATR, counter dist {P[SCALES[sc][1] + '_datr'].median():.2f} ATR")
    print(P[f"shape_{sc}"].value_counts(normalize=True).round(3).to_dict())
for thr, w in ((1.5, 20), (2.0, 60)):
    print(f"\nsymmetric ±{thr} ATR / {w}d:", P[f"sym{thr}_{w}_shape"].value_counts(normalize=True).round(3).to_dict())

# ---- two-sided flags
P["two_sided_swing"] = P.shape_swing.isin(["up_then_down", "down_then_up", "same_bar"])
P["up_then_down_swing"] = P.shape_swing.eq("up_then_down")
P["two_sided_sym20"] = P["sym1.5_20_shape"].isin(["up_then_down", "down_then_up", "same_day"])
P["two_sided_sym60"] = P["sym2.0_60_shape"].isin(["up_then_down", "down_then_up", "same_day"])
P["utd_sym60"] = P["sym2.0_60_shape"].eq("up_then_down")

# ---- by pick-night features
P["atr_terc"] = pd.qcut(P.atr14_px_pct, 3, labels=["lowATR", "midATR", "highATR"])
P["beta_terc"] = pd.qcut(P.beta60, 3, labels=["lowB", "midB", "highB"])
P["score_band"] = pd.cut(P.overall_score, [0, 80, 85, 90, 100], labels=["<80", "80-85", "85-90", "90+"], right=False)
P["ext_terc"] = pd.qcut(P.ret20_pre, 3, labels=["lowRun", "midRun", "highRun"])
ne = pd.to_datetime(P.next_earnings_ctx, errors="coerce")
P["earn_td"] = [np.searchsorted(book.cal, e) - book.pos[d] if pd.notna(e) else np.nan for e, d in zip(ne, P.trading_date)]
P["earn_in_20"] = P.earn_td.between(1, 20)
P["earn_in_60"] = P.earn_td.between(1, 60)
P["gex_neg"] = P.gex_regime.astype(str).str.upper().str.startswith("NEG")
print("\nGEX regimes:", P.gex_regime.value_counts(dropna=False).to_dict(), " pin_risk:", P.gex_pin_risk.value_counts(dropna=False).to_dict())
print("earnings in 20td:", P.earn_in_20.sum(), " in 60td:", P.earn_in_60.sum(), " missing next_earnings:", ne.isna().sum())

cols = ["two_sided_swing", "up_then_down_swing", "two_sided_sym20", "two_sided_sym60", "utd_sym60"]
for f in ["atr_terc", "beta_terc", "score_band", "best_timeframe", "bull", "ext_terc", "earn_in_20", "earn_in_60", "gex_neg", "gex_pin_risk"]:
    g = P.groupby(f, observed=True)
    t = g[cols].mean().round(2)
    t.insert(0, "nights", g.trading_date.nunique()); t.insert(0, "n", g.size())
    print(f"\n-- by {f}\n{t.to_string()}")

# ---- drawdown before L1, time L1 -> L3, recovery after swing-scale counter touch
dd_before, t13, rec3, rec5 = [], [], [], []
for r in P.itertuples():
    kf = r.L1_k if np.isfinite(r.L1_k) else np.nan
    upto = int(kf) if np.isfinite(kf) else 20
    lo = np.nanmin(LO[r.row, :upto]) if r.bull else np.nanmax(HI[r.row, :upto])
    dd_before.append(r.sgn * (lo / r.ref - 1) / r.atr14_px_pct)
    t13.append((r.L3_k - r.L1_k) if np.isfinite(r.L1_k) and np.isfinite(r.L3_k) and r.L3_k <= 40 else np.nan)
    ka = r.ka_swing
    if np.isfinite(ka):
        after = slice(int(ka), 60)
        hi_after = np.nanmax(HI[r.row, after]) if r.bull else np.nanmin(LO[r.row, after])
        rec3.append(bool(r.sgn * (hi_after - r.L3) >= 0) if np.isfinite(r.L3) else np.nan)
        rec5.append(bool(r.sgn * (hi_after - r.L5) >= 0) if np.isfinite(r.L5) else np.nan)
    else:
        rec3.append(np.nan); rec5.append(np.nan)
P["dd_before_L1_atr"] = dd_before; P["days_L1_to_L3"] = t13; P["rec_L3_after_swingc1"] = rec3; P["rec_L5_after_swingc1"] = rec5
print("\nDrawdown before first L1 touch (ATR, direction-adjusted; 0 = none): median %.2f, share worse than -0.5 ATR %.2f, worse than -1 ATR %.2f"
      % (P.dd_before_L1_atr.median(), (P.dd_before_L1_atr <= -0.5).mean(), (P.dd_before_L1_atr <= -1).mean()))
print("Days L1 -> L3 (both hit, L3 within 40):", P.days_L1_to_L3.describe().round(1).to_dict())
s = P.rec_L3_after_swingc1.dropna(); s5 = P.rec_L5_after_swingc1.dropna()
print(f"After touching swing_c1 (n={len(s)}): later reached L3 {s.mean():.2f}, L5 {s5.mean():.2f}")
# time-to-L1 as predictor of L3/L5/L6
P["L1_k_bin"] = pd.cut(P.L1_k, [0, 1, 3, 10, 60], labels=["day1", "d2-3", "d4-10", ">10"])
g = P.groupby("L1_k_bin", observed=True)
print("\nTime to first L1 touch vs deeper levels (from close):")
print(pd.DataFrame({"n": g.size(), "nights": g.trading_date.nunique(), "L3_hit": g.L3_hit.mean(), "L4_hit": g.L4_hit.mean(),
                    "L5_hit": g.L5_hit.mean(), "L6_hit": g.L6_hit.mean(), "elite": g.elite.sum()}).round(2).to_string())
print("L1 never within 60:", P.L1_k.isna().sum())

# ---- excursion-table flags for comparison (calendar-window basis; NOT the same basis)
ex = X.load_excursion_v2()
ex = ex[ex.trading_date.isin(P.trading_date.unique())]
print("\nsas_excursion v2 (calendar windows, for reference): ran_then_dipped", ex.ran_then_dipped.mean().round(2),
      " dipped_before_l1", ex.dipped_before_l1.mean().round(2), " recovered_to_l3", ex.recovered_to_l3.mean().round(2),
      " recovered_to_l5", ex.recovered_to_l5.mean().round(2), " n", len(ex))
P.to_parquet(X.WORK / "themeC.parquet")
