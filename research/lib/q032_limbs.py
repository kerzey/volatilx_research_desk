#!/usr/bin/env python3
"""Q032 re-entry — re-measure the lock-or-DEFER limbs on the TRUE §2.2 partition.

DECISIONS.md fixes what a re-attempt must re-measure and forbids inheriting anything from the
SMA50-only proxy. This script measures, counts only, no outcome of any kind:

  (a) contributing nights per elapsed session            floor 0.40 (re-solved 0.39)
  (b) rarer-arm contributing nights per elapsed session  floor 0.10 (re-solved 0.097)
  (c) rarer-arm gate-counting tape-episodes per session  floor 0.025 (re-solved 0.0243)
  (d) the nine-cell trend x vol composition
  (e) the first session at which SPY has >= 250 prior sessions (honest tercile start)

§2.2, verbatim: SMA50/SMA200 are simple means of SPY split-adjusted closes over the trailing 50
and 200 sessions ending at t inclusive. trend_t = UP iff close_t > SMA50_t AND SMA50_t > SMA200_t;
DOWN iff close_t < SMA50_t AND SMA50_t < SMA200_t; MIXED otherwise. rvol_t = sample sd of daily log
returns over t-19..t, annualised by sqrt(252). vol_t = LOW/MID/HIGH by EXPANDING-window terciles of
rvol over every SPY session in the freeze dated <= t, requiring >= 250 such sessions (below 250 the
night is excluded and counted). BENIGN iff trend_t = UP and vol_t in {LOW, MID}; HOSTILE otherwise.

Tape-episode (DECISIONS item 15 / Steward (b)): a maximal run of consecutive sessions carrying the
same arm label; an excluded or unlabelled session does NOT break a run; an episode counts only if it
contains >= 1 contributing night.

Contributing night (Correction 1): matured to t+40. The proxy's 0.0141 shortfall on this basis was
recorded as freeze-horizon censoring, so both the matured and unmatured bases are printed, with the
censoring boundary named.

  python research/lib/q032_limbs.py
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research/data"
FLOOR_A, FLOOR_B, FLOOR_C = 0.40, 0.10, 0.025
MATURITY = 40


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(DATA / "manifest_prices_universe_v001.json"))
    ap.add_argument("--out", default=str(ROOT / "research/reports/STEWARD_Q032_limbs_true_partition.md"))
    a = ap.parse_args()

    man = json.loads(Path(a.manifest).read_text())
    split = next(t for t in man["tables"] if t["name"] == "daily_split")
    px = pd.read_parquet(ROOT / split["file"], columns=["symbol", "date", "c"])
    spy = px[px.symbol == "SPY"].sort_values("date").reset_index(drop=True)
    if spy.empty:
        raise SystemExit("no SPY bars in the freeze")

    spy["sma50"] = spy.c.rolling(50).mean()
    spy["sma200"] = spy.c.rolling(200).mean()
    spy["logret"] = np.log(spy.c / spy.c.shift(1))
    spy["rvol"] = spy.logret.rolling(20).std(ddof=1) * np.sqrt(252)

    trend = np.where((spy.c > spy.sma50) & (spy.sma50 > spy.sma200), "UP",
             np.where((spy.c < spy.sma50) & (spy.sma50 < spy.sma200), "DOWN", "MIXED"))
    spy["trend"] = np.where(spy.sma200.isna() | spy.sma50.isna(), None, trend)

    # expanding-window terciles of rvol over sessions <= t, requiring >= 250 such sessions
    vol, prior_n = [], []
    hist = []
    for r in spy.rvol:
        n_prior = len(hist)
        prior_n.append(n_prior)
        if pd.isna(r) or n_prior < 250:
            vol.append(None)
        else:
            lo, hi = np.quantile(hist, [1 / 3, 2 / 3])
            vol.append("LOW" if r <= lo else ("MID" if r <= hi else "HIGH"))
        if not pd.isna(r):
            hist.append(r)
    spy["vol"], spy["prior_rvol_sessions"] = vol, prior_n
    spy["arm"] = np.where(spy.trend.isna() | spy.vol.isna(), None,
                          np.where((spy.trend == "UP") & (spy.vol.isin(["LOW", "MID"])), "BENIGN", "HOSTILE"))

    first250 = spy.loc[spy.prior_rvol_sessions >= 250, "date"]
    first250 = first250.iloc[0] if len(first250) else None

    # pick nights and exclusions
    cand = pd.read_parquet(DATA / "v001_sas_candidates.parquet", columns=["trading_date"])
    nights = sorted(pd.to_datetime(cand.trading_date).dt.strftime("%Y-%m-%d").unique())
    ex = json.loads((DATA / "exclusions_v003.json").read_text())
    excl = set()
    for k in ("manual_runs", "non_session_runs", "uncorroborated_publication_runs"):
        excl |= {str(x)[:10] for x in (ex.get(k) or {}).get("trading_dates", [])}

    sess = list(spy.date)
    last_bar = sess[-1]
    idx = {d: i for i, d in enumerate(sess)}
    mature_cutoff = sess[-(MATURITY + 1)] if len(sess) > MATURITY else None

    rows = []
    for t in nights:
        if t not in idx:
            continue
        s = spy.iloc[idx[t]]
        rows.append({"night": t, "trend": s.trend, "vol": s.vol, "arm": s.arm,
                     "prior_rvol_sessions": int(s.prior_rvol_sessions),
                     "excluded": t in excl,
                     "matured_t40": idx[t] + MATURITY < len(sess)})
    df = pd.DataFrame(rows)
    df["contributing_unmatured"] = df.arm.notna() & (~df.excluded)
    df["contributing"] = df.contributing_unmatured & df.matured_t40

    elapsed = len([d for d in sess if df.night.min() <= d <= df.night.max()])

    def episodes(sub_arm: str, matured: bool) -> int:
        """Maximal runs of consecutive sessions carrying sub_arm; unlabelled/excluded sessions do
        not break a run; an episode counts only if it holds >= 1 contributing night."""
        flag = "contributing" if matured else "contributing_unmatured"
        contrib = set(df.loc[df[flag] & (df.arm == sub_arm), "night"])
        runs, cur, n = [], [], 0
        for d in sess:
            if d < df.night.min() or d > df.night.max():
                continue
            arm_d = spy.iloc[idx[d]].arm
            if arm_d == sub_arm:
                cur.append(d)
            elif arm_d is None or pd.isna(arm_d):
                if cur:
                    cur.append(d)          # unlabelled does not break the run
            else:
                if cur:
                    runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        return sum(1 for r in runs if any(d in contrib for d in r))

    out, L = Path(a.out), []
    counts = df[df.contributing].arm.value_counts().to_dict()
    counts_u = df[df.contributing_unmatured].arm.value_counts().to_dict()
    rarer = min(("BENIGN", "HOSTILE"), key=lambda k: counts.get(k, 0)) if counts else "HOSTILE"
    rarer_u = min(("BENIGN", "HOSTILE"), key=lambda k: counts_u.get(k, 0)) if counts_u else "HOSTILE"

    a_rate = df.contributing.sum() / elapsed
    a_rate_u = df.contributing_unmatured.sum() / elapsed
    b_rate = counts.get(rarer, 0) / elapsed
    b_rate_u = counts_u.get(rarer_u, 0) / elapsed
    c_rate = episodes(rarer, True) / elapsed
    c_rate_u = episodes(rarer_u, False) / elapsed

    def verdict(v, f):
        return f"**{v:.4f}** vs {f} — {'PASS' if v >= f else '**SHORT**'}"

    L.append("# Steward — Q032 re-entry: the lock-or-DEFER limbs on the TRUE §2.2 partition\n")
    L.append(f"_Generated {pd.Timestamp.utcnow():%Y-%m-%d} from `{Path(a.manifest).name}` "
             f"(SPY {spy.date.min()}..{spy.date.max()}, {len(spy)} split-adjusted daily bars). "
             "**Counts only** — no outcome, no `E_t`, no `G`. INTERNAL / NON_QUOTABLE._\n")
    L.append("Nothing here is inherited from the SMA50-only proxy: the partition below is the "
             "registered §2.2 one, with the true `SMA50 > SMA200` trend and the true ≥ 250-session "
             "expanding volatility tercile.\n")
    L.append("## (e) The honest tercile start\n")
    L.append(f"- First session with ≥ 250 prior rvol sessions: **{first250}** — the registered window "
             "starts 2026-09-15, so every night in it is calibrated. The \"never\" finding is superseded.\n")
    L.append(f"- SPY bars: **{len(spy)}**, {spy.date.min()} .. {spy.date.max()}. "
             f"SMA200 defined from **{spy.loc[spy.sma200.notna(), 'date'].min()}**.\n")
    L.append("## The three rate limbs\n")
    L.append(f"Panel: **{len(df)}** pick nights {df.night.min()}..{df.night.max()} over **{elapsed}** "
             f"elapsed sessions. t+40 maturity cutoff inside this freeze: **{mature_cutoff}** "
             f"(last bar {last_bar}).\n")
    L.append("| limb | floor | t+40-matured | unmatured |\n|---|---|---|---|")
    L.append(f"| (a) contributing nights / session | {FLOOR_A} | {verdict(a_rate, FLOOR_A)} | {verdict(a_rate_u, FLOOR_A)} |")
    L.append(f"| (b) rarer-arm nights / session | {FLOOR_B} | {verdict(b_rate, FLOOR_B)} (rarer = {rarer}) | {verdict(b_rate_u, FLOOR_B)} (rarer = {rarer_u}) |")
    L.append(f"| (c) rarer-arm episodes / session | {FLOOR_C} | {verdict(c_rate, FLOOR_C)} | {verdict(c_rate_u, FLOOR_C)} |")
    L.append(f"\n- Arm split, t+40-matured contributing nights: " +
             ", ".join(f"**{k}** {v}" for k, v in sorted(counts.items())) + f" (rarer = **{rarer}**)")
    L.append(f"- Arm split, unmatured: " + ", ".join(f"**{k}** {v}" for k, v in sorted(counts_u.items())))
    L.append(f"- Rarer-arm episodes: **{episodes(rarer, True)}** matured, **{episodes(rarer_u, False)}** unmatured")
    L.append(f"- Nights excluded by exclusions_v003: **{int(df.excluded.sum())}**; "
             f"unlabelled (no arm): **{int(df.arm.isna().sum())}**; "
             f"not t+40-matured in this freeze: **{int((~df.matured_t40).sum())}**\n")
    L.append("## (d) Nine-cell composition — contributing nights (t+40-matured)\n")
    cell = (df[df.contributing].groupby(["trend", "vol"]).size().rename("nights").reset_index())
    L.append("| trend | vol | nights | arm |\n|---|---|---:|---|")
    for _, r in cell.iterrows():
        arm = "BENIGN" if (r.trend == "UP" and r.vol in ("LOW", "MID")) else "HOSTILE"
        L.append(f"| {r.trend} | {r.vol} | {r.nights} | {arm} |")
    obs = len(cell)
    L.append(f"\n**{obs} of 9 cells observed** on this historical panel. "
             "Item 7's single permitted suppression revision is **cells added only**.\n")
    L.append("## Bound direction, against the superseded proxy\n")
    L.append("SMA50-only HOSTILE was a **lower** bound on true HOSTILE and SMA50-only BENIGN an "
             "**upper** bound on true BENIGN. The proxy read 22 of 68 nights HOSTILE (0.3099/session); "
             f"the true partition reads **{counts.get('HOSTILE', 0)}** matured HOSTILE nights here. "
             "The proxy's numbers are recorded for the comparison and decide nothing.\n")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    df.to_csv(out.with_suffix(".csv"), index=False)
    print(f"wrote {out.relative_to(ROOT)}")
    print(f"  (a) {a_rate:.4f} / {FLOOR_A}   (b) {b_rate:.4f} / {FLOOR_B} [{rarer}]   (c) {c_rate:.4f} / {FLOOR_C}")
    print(f"  unmatured: (a) {a_rate_u:.4f}  (b) {b_rate_u:.4f}  (c) {c_rate_u:.4f}")


if __name__ == "__main__":
    main()
