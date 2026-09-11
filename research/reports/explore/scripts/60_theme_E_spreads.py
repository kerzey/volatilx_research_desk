"""EXPLORE_001 Theme E: legging out verticals — stock-path proxy (no option prices yet).

Vertical opened at the next-day open (Haci opens spreads the day after the pick), long leg ~ entry,
short leg at L2 (day T2) or L3 (swing T1). The platform's options_context suggests 21-35 DTE
(calendar) ~= 15-25 trading days. For each short strike:
  * share already through the strike at the open (strike choice would have to move up);
  * P(touch within 5/10/15/20/25/40 trading days) and days-to-touch distribution;
  * P(settle at/through the strike at the close of day 15 / 20 / 25) (spread near max value at expiry);
  * race: short strike (L3) touched before the swing counter level / before -1 ATR from entry.
Retro nights excluded. Descriptive.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
pd.set_option("display.width", 250)
P = pd.read_parquet(X.WORK / "themeC.parquet")
Z = np.load(X.WORK / "curves.npz", allow_pickle=True)
HI, LO, CL = Z["HI"], Z["LO"], Z["CL"]
print("Theme E sample: picks", len(P), "nights", P.trading_date.nunique(), "elite", P.elite.sum())


def path_stats(r, level, entry):
    """touch day from entry (day1 includes the open), settle flags, race vs adverse levels."""
    if level is None or not np.isfinite(level) or not np.isfinite(entry):
        return None
    s = r.sgn
    passed = s * (entry - level) >= 0
    fav = HI[r.row] >= level if r.bull else LO[r.row] <= level
    k = np.flatnonzero(fav)
    kt = 0 if passed else (k[0] + 1 if len(k) else np.nan)
    settle = {h: bool(s * (CL[r.row, h - 1] - level) >= 0) for h in (15, 20, 25)}
    # adverse levels
    adv1 = entry * (1 - s * r.atr14_px_pct)                        # -1 ATR from entry
    advc = r.swing_c1 if np.isfinite(r.swing_c1) and s * (r.swing_c1 - entry) < 0 else np.nan
    def first_adv(lv):
        if not np.isfinite(lv):
            return np.nan
        a = LO[r.row] <= lv if r.bull else HI[r.row] >= lv
        ix = np.flatnonzero(a)
        return ix[0] + 1 if len(ix) else np.nan
    ka1, kac = first_adv(adv1), first_adv(advc)
    return {"passed": passed, "kt": kt, **{f"settle{h}": v for h, v in settle.items()}, "ka_1atr": ka1, "ka_ctr": kac}


rows = []
for r in P.itertuples():
    for strike in ("L2", "L3", "L4"):
        for ent in ("E_open", "E_10"):
            st = path_stats(r, getattr(r, strike), getattr(r, ent))
            if st is None:
                continue
            dist = r.sgn * (getattr(r, strike) / getattr(r, ent) - 1) / r.atr14_px_pct
            rows.append({"trading_date": r.trading_date, "symbol": r.symbol, "elite": r.elite, "strike": strike,
                         "entry": ent, "dist_atr": dist, "gap_bin": r.gap_bin, "atr_terc": r.atr_terc, **st})
S = pd.DataFrame(rows)
S.to_parquet(X.WORK / "themeE.parquet")


def summarize(df):
    out = {"n": len(df), "nights": df.trading_date.nunique(), "passed_at_entry": df.passed.mean(),
           "med_dist_atr": df.loc[~df.passed, "dist_atr"].median()}
    for w in (5, 10, 15, 20, 25, 40):
        out[f"touch<={w}"] = np.mean(df.kt <= w)
    live = df[~df.passed & df.kt.notna()]
    out["days_med"] = live.kt.median(); out["days_p75"] = live.kt.quantile(.75)
    for h in (15, 20, 25):
        out[f"settle@{h}"] = df[f"settle{h}"].mean()
    # race (strike not passed at entry)
    nl = df[~df.passed]
    kt = nl.kt.fillna(999); a1 = nl.ka_1atr.fillna(999); ac = nl.ka_ctr.fillna(999)
    out["strike_before_-1ATR"] = np.mean((kt < a1) & (kt < 999))
    out["-1ATR_first"] = np.mean(a1 <= kt) if len(nl) else np.nan
    out["strike_before_ctr"] = np.mean((kt < ac) & (kt < 999))
    return pd.Series(out)


for ent in ("E_open", "E_10"):
    print(f"\n== Entry {ent}")
    t = S[S.entry == ent].groupby("strike").apply(summarize, include_groups=False)
    print(t.round(2).to_string())
print("\n== Elite only (E_open); n picks =", S[(S.entry == 'E_open') & S.elite].symbol.size // 3)
print(S[(S.entry == "E_open") & S.elite].groupby("strike").apply(summarize, include_groups=False).round(2).to_string())
print("\n== L3 short strike by gap bucket (E_open)")
print(S[(S.entry == "E_open") & (S.strike == "L3")].groupby("gap_bin", observed=True).apply(summarize, include_groups=False).round(2).to_string())
print("\n== L3 short strike by ATR tercile (E_open)")
print(S[(S.entry == "E_open") & (S.strike == "L3")].groupby("atr_terc", observed=True).apply(summarize, include_groups=False).round(2).to_string())
# speed vs distance: days-to-touch by distance bucket
sub = S[(S.entry == "E_open") & ~S.passed]
sub = sub.assign(dbin=pd.cut(sub.dist_atr, [0, 0.5, 1, 2, 3, 5, 20]))
print("\n== Days to touch vs strike distance from open (all strikes pooled, E_open)")
print(sub.groupby("dbin", observed=True).agg(n=("kt", "size"), touch20=("kt", lambda x: np.mean(x <= 20)),
      med_days=("kt", "median"), p75_days=("kt", lambda x: x.quantile(.75))).round(2).to_string())
