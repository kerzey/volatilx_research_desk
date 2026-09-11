"""EXPLORE_001 step 80: follow-ups for the ranked ideas (in-sample picks only).

(a) Day-1 limit entry at close -0.25 / -0.5 ATR (against the pick): fill rate on day 1 and the
    L3-before-(-1 ATR from fill) race after filling, vs market entry at the next open and after hours.
(b) Give-back after touching the short strike: P(day-20 close through L3 | L3 touched by day 20).
(c) Sealed-period calendar: how many pick nights after in_sample_end have matured 20/40/60-session
    windows as of the freeze date. Uses the SPY trading calendar ONLY — no sealed pick is loaded.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import explore_lib as X
P = pd.read_parquet(X.WORK / "seeds.parquet")
Z = np.load(X.WORK / "curves.npz", allow_pickle=True)
HI, LO, CL = Z["HI"], Z["LO"], Z["CL"]


def race(r, entry, k0, level):
    """From day k0 (1-based; the entry day, bars from k0 onward) — level touched before -1 ATR from entry?"""
    s = r.sgn
    if s * (entry - level) >= 0:
        return "passed"
    adv = entry * (1 - s * r.atr14_px_pct)
    for k in range(k0 - 1, 40):
        f = HI[r.row, k] >= level if r.bull else LO[r.row, k] <= level
        a = LO[r.row, k] <= adv if r.bull else HI[r.row, k] >= adv
        if f and a:
            return "same_day"
        if f:
            return "target"
        if a:
            return "adverse"
    return "neither"


rows = []
for r in P.itertuples():
    rec = {"elite": r.elite, "trading_date": r.trading_date}
    for off in (0.25, 0.5):
        lim = r.ref * (1 - r.sgn * off * r.atr14_px_pct)
        # day-1 fill: open through the limit fills at open; else intraday low/high touches it
        o, h, l = r.E_open, HI[r.row, 0], LO[r.row, 0]
        filled = (l <= lim) if r.bull else (h >= lim)
        fill_px = (min(o, lim) if r.bull else max(o, lim)) if filled else np.nan
        rec[f"fill_{off}"] = filled
        rec[f"race_{off}"] = race(r, fill_px, 1, r.L3) if filled else "nofill"
    rec["race_open"] = race(r, r.E_open, 1, r.L3)
    rec["race_ah"] = race(r, r.E_ah, 1, r.L3) if np.isfinite(r.E_ah) else "noah"
    # (b) give-back
    t = np.flatnonzero((HI[r.row, :20] >= r.L3) if r.bull else (LO[r.row, :20] <= r.L3))
    rec["L3_touch20"] = len(t) > 0
    rec["L3_settle20"] = bool(r.sgn * (CL[r.row, 19] - r.L3) >= 0)
    rows.append(rec)
R = pd.DataFrame(rows)
print("picks", len(R), "nights", R.trading_date.nunique())
for grp, sub in (("all", R), ("non-elite", R[~R.elite]), ("elite", R[R.elite])):
    print(f"\n== {grp} (n={len(sub)}, nights={sub.trading_date.nunique()})")
    for off in (0.25, 0.5):
        print(f"  limit close-{off} ATR: day-1 fill {sub[f'fill_{off}'].mean():.2f}; race after fill:",
              sub.loc[sub[f'fill_{off}'], f"race_{off}"].value_counts(normalize=True).round(2).to_dict())
    print("  next-open market entry race:", sub.race_open.value_counts(normalize=True).round(2).to_dict())
    print("  after-hours entry race:", sub.loc[sub.race_ah != "noah", "race_ah"].value_counts(normalize=True).round(2).to_dict(),
          "(n=%d)" % (sub.race_ah != "noah").sum())
    tt = sub[sub.L3_touch20]
    print(f"  L3 touched by day 20: {sub.L3_touch20.mean():.2f}; of those, day-20 close still through L3: {tt.L3_settle20.mean():.2f}")

# (c) sealed-period calendar maturity (calendar only)
book = X.PathBook(X.load_prices())
cal = book.cal
asof = pd.Timestamp(X.eu.load_manifest(X.M)["as_of"])
sealed_nights = cal[(cal > X.IN_SAMPLE_END) & (cal <= asof)]
last = np.searchsorted(cal, asof, side="right") - 1
print(f"\nSealed calendar: {len(sealed_nights)} sessions {sealed_nights[0].date()}..{sealed_nights[-1].date()}")
for w in (5, 10, 20, 40, 60):
    cutoff = cal[last - w] if last - w >= 0 else None
    n_mat = int(((sealed_nights <= cutoff)).sum()) if cutoff is not None else 0
    print(f"  window {w:2d} sessions matured for pick nights <= {cutoff.date()}: {n_mat} sealed nights")

# (d) same-subset comparison: picks with an actionable after-hours price
S = R[R.race_ah != "noah"]
print(f"\nSame subset (actionable AH price, n={len(S)}, nights={S.trading_date.nunique()}):")
print("  AH entry race:  ", S.race_ah.value_counts(normalize=True).round(2).to_dict())
print("  open entry race:", S.race_open.value_counts(normalize=True).round(2).to_dict())
print("  limit-0.25 fill:", round(S["fill_0.25"].mean(), 2), "race after fill:", S.loc[S["fill_0.25"], "race_0.25"].value_counts(normalize=True).round(2).to_dict())
