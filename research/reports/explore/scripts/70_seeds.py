"""EXPLORE_001 Theme F/G: elite accounting + charter seeds on the path lens.

  * elite 90+ roster and why each is in / out of the analysis sample
  * re-qualification streak (published in prior 10 sessions) vs matched-control excess (H-052 context)
  * UOA persistence: strong same-direction UOA days (score>=70) in the prior 5 sessions (H-040 context)
  * earnings inside the day/swing window (corrected report dates) vs path shape
  * GEX alignment score / pin risk vs day-lane excess and two-sidedness (H-020 context)
  * near-miss 65-70 vs 70-75 unpublished vs published: ATR-normalised favourable excursion (H-002 context)
  * range excess of picks vs beta/ATR/momentum-matched same-night control
Retro nights excluded unless stated.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
RETRO = {"2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14"}
Call = pd.read_parquet(X.WORK / "cands_ok.parquet")
Call["row"] = np.arange(len(Call))
P = pd.read_parquet(X.WORK / "themeC.parquet")
A = pd.read_parquet(X.WORK / "themeA_matched.parquet")
D = pd.read_parquet(X.WORK / "themeD.parquet")
Z = np.load(X.WORK / "curves.npz", allow_pickle=True)
UPc, DNc, HI, LO = Z["UPc"], Z["DNc"], Z["HI"], Z["LO"]
book = X.PathBook(X.load_prices())

# ---- elite roster
el = Call[Call.elite][["trading_date", "symbol", "overall_score", "dominant_direction", "best_timeframe", "has_lane_plans", "actionable"]].copy()
el["in_sample_analysis"] = el.has_lane_plans & ~el.trading_date.astype(str).str[:10].isin(RETRO)
print("Elite 90+ in-sample:", len(el), "nights", el.trading_date.nunique(), "| in analysis sample:", el.in_sample_analysis.sum(),
      "nights", el[el.in_sample_analysis].trading_date.nunique(), "| unique symbols", el.symbol.nunique())
print(el.sort_values("trading_date").to_string(index=False))

# ---- re-qualification streak: published count in prior 10 sessions (in-sample history only; April truncated)
pubset = Call[Call.published][["trading_date", "symbol"]]
pubd = {s: set(g.trading_date) for s, g in pubset.groupby("symbol")}
def prior_pub(sym, d, n=10):
    i = book.pos[d]
    win = set(book.cal[max(0, i - n): i])
    return len(pubd.get(sym, set()) & win)
P["prior_pub10"] = [prior_pub(s, d) for s, d in zip(P.symbol, P.trading_date)]
P["streak_bin"] = pd.cut(P.prior_pub10, [-1, 0, 2, 10], labels=["new", "1-2", "3+"])
# only picks with a full 10-session in-sample history (first in-sample night 2026-04-01)
full_hist = P.trading_date >= book.cal[book.pos[pd.Timestamp("2026-04-01")] + 10]
A["pk"] = A.trading_date.astype(str) + A.symbol
A2 = A.merge(P.loc[full_hist, ["trading_date", "symbol", "streak_bin", "elite"]].rename(columns={"elite": "el"}), on=["trading_date", "symbol"])
print("streak sample: picks", int(full_hist.sum()), "nights", P[full_hist].trading_date.nunique())
print("\n== Re-qualification (published in prior 10 sessions) — matched-control excess, all ladder levels pooled")
g = A2.groupby("streak_bin", observed=True)
print(pd.DataFrame({"picks": g.pk.nunique(), "level_rows": g.size(), "nights": g.trading_date.nunique(),
                    "pick_hit": g.hit.mean(), "ctrl": g.ctrl_nn.mean(), "excess": g.excess_nn.mean()}).round(3).to_string())
for L in ("L3", "L5", "L6"):
    s = A2[A2.L == L].groupby("streak_bin", observed=True).excess_nn.mean().round(3).to_dict()
    print(f"   {L} excess by streak: {s}")
g = A2[~A2.el].groupby("streak_bin", observed=True)
print("   non-elite only:", pd.DataFrame({"picks": g.pk.nunique(), "nights": g.trading_date.nunique(),
      "excess": g.excess_nn.mean()}).round(3).to_dict("index"))
Pf = P[full_hist]
g = Pf.groupby("streak_bin", observed=True)
print("   path by streak:", pd.DataFrame({"n": g.size(), "gap_med": g.gap_atr.median(),
      "L1_passed_open": g.apply(lambda x: np.mean(x.sgn * (x.E_open - x.L1) >= 0), include_groups=False),
      "two_sym60": g.two_sided_sym60.mean(), "utd_sym60": g.utd_sym60.mean(), "ret20_pre_med": g.ret20_pre.median()}).round(2).to_dict("index"))

# ---- UOA persistence (prior 5 sessions, excluding the pick night)
U = X.eu.load_split(X.M, "in_sample", name="uoa_symbol")
# 'strong' UOA day = any bucket score >= 70 with a directional label matching the pick direction
# (non-NOISE labels alone cover ~half the universe every day, so they are not informative)
for b in ("day", "swing", "long"):
    U[f"bull_{b}"] = (U[f"score_{b}"] >= 70) & (U[f"label_{b}"] == "BULLISH_FLOW_SETUP")
    U[f"bear_{b}"] = (U[f"score_{b}"] >= 70) & (U[f"label_{b}"] == "BEARISH_FLOW_SETUP")
U["strong_bull"] = U[["bull_day", "bull_swing", "bull_long"]].any(axis=1)
U["strong_bear"] = U[["bear_day", "bear_swing", "bear_long"]].any(axis=1)
ub = {s: set(g.loc[g.strong_bull, "trading_date"]) for s, g in U.groupby("symbol")}
ur = {s: set(g.loc[g.strong_bear, "trading_date"]) for s, g in U.groupby("symbol")}
print("strong same-direction UOA day share of universe rows:", round(float((U.strong_bull | U.strong_bear).mean()), 3))
def uoa_prior(sym, d, bull, n=5):
    i = book.pos[d]
    win = set(book.cal[max(0, i - n): i])
    return len((ub if bull else ur).get(sym, set()) & win)
P["uoa_prior5"] = [uoa_prior(s, d, b) for s, d, b in zip(P.symbol, P.trading_date, P.bull)]
P["uoa_bin"] = pd.cut(P.uoa_prior5, [-1, 0, 2, 5], labels=["0", "1-2", "3+"])
print("uoa_prior5 distribution:", P.uoa_prior5.value_counts().sort_index().to_dict())
A3 = A.merge(P[["trading_date", "symbol", "uoa_bin"]], on=["trading_date", "symbol"])
print("\n== strong same-direction UOA days (score>=70) in prior 5 sessions — matched-control excess (pooled levels) and path shape")
g = A3.groupby("uoa_bin", observed=True)
t = pd.DataFrame({"picks": g.pk.nunique(), "nights": g.trading_date.nunique(), "pick_hit": g.hit.mean(),
                  "ctrl": g.ctrl_nn.mean(), "excess": g.excess_nn.mean()})
t2 = P.groupby("uoa_bin", observed=True)[["two_sided_sym60", "utd_sym60", "L3_hit", "L5_hit"]].mean()
print(t.join(t2).round(3).to_string())

# ---- earnings inside the window (corrected report dates; knowledge-time caveat)
ed = P.trading_date + pd.to_timedelta(P.days_to_earnings_corrected, unit="D")
P["earn_td"] = [np.searchsorted(book.cal, e) - book.pos[d] if pd.notna(e) else np.nan for e, d in zip(ed, P.trading_date)]
P["earn_bin"] = pd.cut(P.earn_td, [-1, 3, 10, 20, 40, 200], labels=["0-3td", "4-10td", "11-20td", "21-40td", ">40td"])
P["earn_bin"] = P.earn_bin.cat.add_categories("unknown").fillna("unknown")
print("\n== Earnings timing (trading days from pick night to next report, corrected dates) vs path")
g = P.groupby("earn_bin", observed=True)
print(pd.DataFrame({"n": g.size(), "nights": g.trading_date.nunique(), "elite": g.elite.sum(),
                    "L1_hit": g.L1_hit.mean(), "L3_hit": g.L3_hit.mean(), "L5_hit": g.L5_hit.mean(),
                    "two_sided_swing": g.two_sided_swing.mean(), "two_sym20": g.two_sided_sym20.mean(),
                    "mae20_open_med": g.mae20_from_open_atr.median(), "gap_abs_med": g.gap_atr.apply(lambda x: x.abs().median())}).round(2).to_string())
print("catalyst_event_score by earn_bin (should penalise near earnings if the layer worked):",
      P.groupby("earn_bin", observed=True).catalyst_event_score.median().round(1).to_dict())

# ---- GEX alignment (weight 0) and pin risk
P["gexal_terc"] = pd.qcut(P.gex_alignment_score, 3, labels=["lo", "mid", "hi"], duplicates="drop")
A4 = A.merge(P[["trading_date", "symbol", "gexal_terc", "gex_pin_risk"]], on=["trading_date", "symbol"])
print("\n== GEX alignment score tercile — day-lane (L1/L2) and swing (L3/L4) matched excess")
for lv in (("L1", "L2"), ("L3", "L4")):
    s = A4[A4.L.isin(lv)].groupby("gexal_terc", observed=True).agg(n=("hit", "size"), nights=("trading_date", "nunique"),
                                                                   pick=("hit", "mean"), ctrl=("ctrl_nn", "mean"), excess=("excess_nn", "mean"))
    print(lv, "\n", s.round(3).to_string())
print("gex_alignment_score distribution among picks:", P.gex_alignment_score.describe().round(1).to_dict())

# ---- near-miss: ATR-normalised favourable excursion (own direction) at 20d, and +2 ATR touch, by band
Dn = D.copy()
Dn["band"] = pd.cut(Dn.overall_score, [0, 60, 65, 70, 75, 80, 90, 101], right=False)
Dn["fav20"] = [ (UPc[r, 19] if b else DNc[r, 19]) for r, b in zip(Dn.row, Dn.bull)]
Dn["adv20"] = [ (DNc[r, 19] if b else UPc[r, 19]) for r, b in zip(Dn.row, Dn.bull)]
Dn["net20"] = Dn.fav20 - Dn.adv20
Dn["t2"] = Dn.fav20 >= 2
print("\n== Near-miss view (all candidates, own dominant direction, 20d, ATR units; retro nights excluded)")
g = Dn.groupby(["band", "published"], observed=True)
print(pd.DataFrame({"n": g.size(), "nights": g.trading_date.nunique(), "fav20_med": g.fav20.median(), "adv20_med": g.adv20.median(),
                    "net20_med": g.net20.median(), "touch+2ATR": g.t2.mean(), "bull_share": g.bull.mean(),
                    "beta_med": g.beta60.median()}).round(2).to_string())

# ---- range excess vs beta/ATR/momentum-matched control
feats = ["beta60", "atr14_px_pct", "ret20_pre"]
Dz = D.dropna(subset=feats).copy()
for f in feats:
    Dz[f + "_z"] = (Dz[f] - Dz[f].mean()) / Dz[f].std()
zc = [f + "_z" for f in feats]
ex = []
for r in Dz[Dz.published].itertuples():
    pool = Dz[(Dz.trading_date == r.trading_date) & ~Dz.published]
    me = np.array([getattr(r, c) for c in zc])
    dd = np.sqrt(((pool[zc].to_numpy() - me) ** 2).sum(axis=1))
    nn = pool.iloc[np.argsort(dd)[:10]]
    ex.append({"trading_date": r.trading_date, "d_range20": r.range20_atr - nn.range20_atr.mean(),
               "d_two60": float(r.two_s60) - nn.two_s60.mean(), "d_two20": float(r.two_s20) - nn.two_s20.mean()})
E = pd.DataFrame(ex)
nE = E.groupby("trading_date").mean()
print("\n== Picks minus matched control (night-averaged): range20/ATR %+.2f (nights>0 %.2f), two-sided±1.5/20d %+.3f, two-sided±2/60d %+.3f; nights %d"
      % (nE.d_range20.mean(), (nE.d_range20 > 0).mean(), nE.d_two20.mean(), nE.d_two60.mean(), len(nE)))
P.to_parquet(X.WORK / "seeds.parquet")
