"""EXPLORE_001 step 3: build the core tables (in-sample only).

Outputs (research/reports/explore/work/):
  cands.parquet  one row per in-sample candidate (published + unpublished), features known
                 by 16:05 ET on the pick night + ladder levels for published picks.
  fwd.parquet    long table of forward regular-session bars, signal-date basis, k=1..60.
  entries.parquet  published picks: pick-night after-hours / next-open / next-day 10:00 and
                 11:00 ET entry prices (signal-date basis) + day-1 intraday highs/lows after entry.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X

cand = X.load_candidates()
print("in-sample candidates", len(cand), cand.trading_date.min().date(), cand.trading_date.max().date())
parsed = pd.DataFrame([X.parse_candidate(r) for r in cand.itertuples()], index=cand.index)
keep = ["id", "trading_date", "symbol", "overall_score", "dominant_direction", "best_timeframe",
        "confidence_level", "completeness_score", "qualified", "selected_rank", "qualification_reason",
        "flow_strength_score", "technical_structure_score", "gex_alignment_score", "projection_score",
        "fundamental_quality_score", "catalyst_event_score", "smart_money_confirmation_score",
        "cross_layer_bonus", "conflict_penalty", "industry", "industry_rotation_active",
        "days_to_earnings_corrected", "earnings_phase", "earnings_event_risk_corrected"]
C = pd.concat([cand[keep], parsed], axis=1)
C["published"] = C.qualification_reason.eq("selected")
C["bull"] = C.dominant_direction.str.lower().str.startswith("bull")
C["elite"] = C.published & (C.overall_score >= 90)

# ---- excursion counter levels (v2 only; dedupe confirmed in loader)
ex = X.load_excursion_v2()
print("excursion v2 rows", len(ex), "published in-sample", C.published.sum())
exk = ex[["trading_date", "symbol", "counter_levels_json", "downside_source", "entry_ref",
          "signal_date_close", "earnings_within_window"]].copy()
cl = pd.DataFrame([X.J(v) or {} for v in exk.counter_levels_json], index=exk.index)
for k in X.COUNTER_KEYS:
    exk[k] = pd.to_numeric(cl.get(k), errors="coerce")
exk = exk.drop(columns="counter_levels_json").rename(columns={"entry_ref": "ex_entry_ref",
                                                             "earnings_within_window": "ex_earn_in_window"})
C = C.merge(exk, on=["trading_date", "symbol"], how="left")
print("published with excursion row:", C.loc[C.published, "downside_source"].notna().sum())
print(C.loc[C.published, "downside_source"].value_counts(dropna=False))

# ---- prices
prices = X.load_prices()
book = X.PathBook(prices)
spy = book.by_sym["SPY"]
spy_ret = spy["c_s"].pct_change()

rows, fwd_rows = [], []
for r in C.itertuples():
    d, s = r.trading_date, r.symbol
    g = book.by_sym.get(s)
    rec = {"trading_date": d, "symbol": s}
    if g is None or d not in g.index:
        rec["price_ok"] = False
        rows.append(rec)
        continue
    rec["price_ok"] = True
    rec["raw_close_d"] = g.loc[d, "c"]
    hist = book.history(s, d, 61)
    hc = hist["c_s"]
    rets = hc.pct_change().dropna()
    sr = spy_ret.reindex(rets.index)
    ok = rets.notna() & sr.notna()
    if ok.sum() >= 40:
        cov = np.cov(rets[ok], sr[ok])
        rec["beta60"] = cov[0, 1] / cov[1, 1]
        rec["corr60"] = np.corrcoef(rets[ok], sr[ok])[0, 1]
    rec["rv20"] = rets.tail(20).std() * np.sqrt(252)
    h14 = hist.tail(15)
    tr = np.maximum(h14["h_s"] - h14["l_s"], np.maximum((h14["h_s"] - h14["c_s"].shift()).abs(),
                                                         (h14["l_s"] - h14["c_s"].shift()).abs()))
    rec["atr14_px_pct"] = tr.tail(14).mean() / hc.iloc[-1]
    rec["ret5_pre"] = hc.iloc[-1] / hc.iloc[-6] - 1 if len(hc) >= 6 else np.nan
    rec["ret20_pre"] = hc.iloc[-1] / hc.iloc[-21] - 1 if len(hc) >= 21 else np.nan
    rec["dist_20d_high"] = hc.iloc[-1] / hist["h_s"].tail(20).max() - 1
    rows.append(rec)
    f = book.forward(s, d)
    if f is not None and len(f):
        f = f.reset_index(names="date")
        f["trading_date"] = d
        f["symbol"] = s
        fwd_rows.append(f[["trading_date", "symbol", "date", "k", "o", "h", "l", "c"]])

PX = pd.DataFrame(rows)
C = C.merge(PX, on=["trading_date", "symbol"], how="left")
FWD = pd.concat(fwd_rows, ignore_index=True)

# SPY context on the pick night (known at 16:05)
sc = spy["c_s"]
spyctx = pd.DataFrame({"spy_ret5_pre": sc / sc.shift(5) - 1, "spy_ret20_pre": sc / sc.shift(20) - 1,
                       "spy_dist_20d_high": sc / spy["h_s"].rolling(20).max() - 1})
C = C.merge(spyctx, left_on="trading_date", right_index=True, how="left")

# ---- sanity
C["spot_vs_close"] = C.spot / C.raw_close_d - 1
print("spot vs raw close |diff|>0.5%:", (C.spot_vs_close.abs() > 0.005).sum(), "of", C.spot.notna().sum())
print("atr_pct coverage all:", C.atr_pct.notna().mean().round(3), " published:",
      C.loc[C.published, "atr_pct"].notna().mean().round(3))
print("ctx atr_pct vs own ATR14 corr:", C[["atr_pct", "atr14_px_pct"]].corr().iloc[0, 1].round(3),
      " median ratio:", (C.atr_pct / C.atr14_px_pct).median().round(3))
print("forward bars per row (published):",
      FWD.merge(C.loc[C.published, ["trading_date", "symbol"]]).groupby(["trading_date", "symbol"]).size().describe())

# ---- run finish time per night -> actionability
runs = X.eu.load_split(X.M, "in_sample", name="sas_runs")
runs["finished_at"] = pd.to_datetime(runs.finished_at, utc=True)
runs = runs[["trading_date", "finished_at"]].drop_duplicates("trading_date")
C = C.merge(runs, on="trading_date", how="left")
d_utc = C.trading_date.dt.tz_localize("UTC")
d1 = pd.Series([book.cal[book.pos[d] + 1] for d in C.trading_date], index=C.index)
open1_utc = d1.dt.tz_localize("UTC") + pd.Timedelta(hours=13, minutes=30)
C["actionable"] = np.where(C.finished_at < d_utc + pd.Timedelta(hours=24), "ah",
                  np.where(C.finished_at < open1_utc, "next_open", "retro"))
C["finish_hour_utc"] = np.where(C.actionable == "ah", C.finished_at.dt.hour, np.nan)
print("actionability by night:", C.drop_duplicates("trading_date").actionable.value_counts().to_dict())

# ---- entries (published only) from hourly bars
H = X.load_hourly()
pubs = C[C.published]
H = H[H.symbol.isin(pubs.symbol.unique())]
fmap = prices.set_index(["symbol", "date"])["f"]
Hg = {k: g for k, g in H.groupby(["symbol", "d"])}
erows = []
for r in pubs.itertuples():
    d, s = r.trading_date, r.symbol
    i = book.pos[d]
    d1 = book.cal[i + 1]
    fd = fmap.get((s, d), np.nan)
    f1 = fmap.get((s, d1), np.nan)
    adj1 = fd / f1  # hourly raw on day1 -> signal-date basis
    e = {"trading_date": d, "symbol": s, "d1": d1}
    h0 = Hg.get((s, d))
    if h0 is not None:
        ah = h0[(h0.hr >= 21) & (h0.hr <= 23)].sort_values("t")
        # actionable AH entry: close of the bar during which SAS finished (or the next AH bar)
        if r.actionable == "ah":
            fh = int(r.finish_hour_utc)
            post = h0[(h0.hr >= fh) & (h0.hr <= 23)].sort_values("t")
            e["E_ah_pub"] = post.c.iloc[0] if len(post) else np.nan
            e["E_ah_pub_hr"] = post.hr.iloc[0] if len(post) else np.nan
            after = h0[(h0.hr > fh) & (h0.hr <= 23)]
            e["ah_hi_after_pub"] = after.h.max() if len(after) else np.nan
            e["ah_lo_after_pub"] = after.l.min() if len(after) else np.nan
        e["ah_nbars"] = len(ah)
        e["ah_vol"] = ah.v.sum()
        if len(ah):
            e["E_ah"] = ah.o.iloc[0]
            e["E_ah_vwap"] = (ah.vw * ah.v).sum() / ah.v.sum() if ah.v.sum() > 0 else np.nan
            e["ah_last"] = ah.c.iloc[-1]
            e["ah_hi"] = ah.h.max()
            e["ah_lo"] = ah.l.min()
        pc = h0[h0.hr == 20]
        e["post_close_20h_c"] = pc.c.iloc[0] if len(pc) else np.nan
    h1 = Hg.get((s, d1))
    if h1 is not None:
        h1 = h1.sort_values("t")
        pre = h1[(h1.hr >= 8) & (h1.hr <= 12)]
        e["pre_last"] = pre.c.iloc[-1] * adj1 if len(pre) else np.nan
        b13 = h1[h1.hr == 13]
        b14 = h1[h1.hr == 14]
        e["E_10"] = b13.c.iloc[0] * adj1 if len(b13) else np.nan
        e["E_11"] = b14.c.iloc[0] * adj1 if len(b14) else np.nan
        e["b13_h"] = b13.h.iloc[0] * adj1 if len(b13) else np.nan
        e["b13_l"] = b13.l.iloc[0] * adj1 if len(b13) else np.nan
        e["pre_hi"] = pre.h.max() * adj1 if len(pre) else np.nan
        e["pre_lo"] = pre.l.min() * adj1 if len(pre) else np.nan
        rest10 = h1[(h1.hr >= 14) & (h1.hr <= 19)]
        rest11 = h1[(h1.hr >= 15) & (h1.hr <= 19)]
        e["d1_hi_after10"] = rest10.h.max() * adj1 if len(rest10) else np.nan
        e["d1_lo_after10"] = rest10.l.min() * adj1 if len(rest10) else np.nan
        e["d1_hi_after11"] = rest11.h.max() * adj1 if len(rest11) else np.nan
        e["d1_lo_after11"] = rest11.l.min() * adj1 if len(rest11) else np.nan
    f = FWD[(FWD.trading_date == d) & (FWD.symbol == s) & (FWD.k == 1)]
    if len(f):
        e["E_open"] = f.o.iloc[0]
        e["d1_h"], e["d1_l"], e["d1_c"] = f.h.iloc[0], f.l.iloc[0], f.c.iloc[0]
    erows.append(e)
E = pd.DataFrame(erows)
print("E_ah_pub coverage (actionable-ah picks):", E.E_ah_pub.notna().sum(), "of", (pubs.actionable == "ah").sum())
print("entries: AH coverage", E.E_ah.notna().mean().round(3), " E_10 coverage", E.E_10.notna().mean().round(3))
print("AH bars per pick", E.ah_nbars.describe())
print("E_10 vs daily range check (outside [l,h] by >0.2%):",
      ((E.E_10 > E.d1_h * 1.002) | (E.E_10 < E.d1_l * 0.998)).sum())

C.to_parquet(X.WORK / "cands.parquet")
FWD.to_parquet(X.WORK / "fwd.parquet")
E.to_parquet(X.WORK / "entries.parquet")
print("saved", len(C), len(FWD), len(E))
