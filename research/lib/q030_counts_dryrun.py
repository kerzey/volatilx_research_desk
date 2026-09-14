#!/usr/bin/env python3
"""Q030 R2(iii) — counts-only dry run on the sealed period.

The PREREG is explicit about what this may and may not produce:

  "(iii) a counts-only dry run on the sealed period — `b_t`, `n_t`, `m_t` and nothing else
   (no `recall_t`, no lift, no intersection count) for pick nights 2026-06-01..2026-08-12,
   so the desk knows whether `m_t >= 1` is ever binding before it commits to a schedule."

So this script NEVER computes |M_t ∩ U_t^B|, recall_t, e_t, precision_t or the lift. It holds
the mover set and the universe set in separate variables and never intersects them. That is the
whole point: the question's outcome stays sealed while its denominators are measured.

Definitions taken verbatim from PREREG §2.1, §2.2, §2.3, §2.5:
  B    = the 2,405 `mapping` symbols of the pinned blob, fixed for the question
  B_t  = s in B with (a) >= 60 split-adjusted daily bars dated <= t and (b) a bar on t itself
  C,ATR= close and ATR14 from prices_daily_split bars <= t (never the platform's atr_pct)
  T    = C + 3 * ATR14                                (bulls; H-074's own distance)
  M_t  = s in B_t whose regular-session HIGH touches T on some session in t+1..t+20 (path, not
         fixed-horizon). Right-censored symbols (forward bars stop at t+k, k<20) are movers if
         they touched by t+k, else counted UNGRADEABLE — never graded as a non-move.
  U_t  = distinct sas_candidates symbols on t, no score/qualification/publication/direction filter
  n_t  = |U_t ∩ B_t|,  m_t = |M_t|,  b_t = |B_t|

  python research/lib/q030_counts_dryrun.py --start 2026-06-01 --end 2026-08-12
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CODEBASE = Path("C:/Users/sahin/Projects/volatilx")
DATA = ROOT / "research/data"
BLOB_COMMIT, BLOB_PATH = "4171b1a", "data/sp500_sectors.json"
BLOB_SHA = "c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201"
MIN_BARS, HORIZON, ATR_N, ATR_MULT = 60, 20, 14, 3.0


def blob_symbols() -> list:
    raw = subprocess.run(["git", "show", f"{BLOB_COMMIT}:{BLOB_PATH}"], cwd=CODEBASE,
                         capture_output=True, check=True).stdout
    got = hashlib.sha256(raw).hexdigest()
    if got != BLOB_SHA:
        sys.exit(f"blob sha mismatch: committed bytes hash {got}, pinned {BLOB_SHA}")
    return sorted(json.loads(raw)["mapping"])


def wide(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.pivot(index="date", columns="symbol", values=col).sort_index()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-06-01")
    ap.add_argument("--end", default="2026-08-12")
    ap.add_argument("--manifest", default=str(DATA / "manifest_prices_universe_v001.json"))
    ap.add_argument("--out", default=str(ROOT / "research/reports/STEWARD_Q030_counts_dryrun.md"))
    a = ap.parse_args()

    man = json.loads(Path(a.manifest).read_text())
    split_entry = next(t for t in man["tables"] if t["name"] == "daily_split")
    px = pd.read_parquet(ROOT / split_entry["file"], columns=["symbol", "date", "h", "l", "c"])

    base = blob_symbols()
    px = px[px.symbol.isin(base)]
    H, L, C = wide(px, "h"), wide(px, "l"), wide(px, "c")
    sessions = list(C.index)

    # ATR14 (Wilder) on split-adjusted bars. NOTE: PREREG 2.2 says "ATR14" without naming the
    # smoothing; recorded as an open item for the lock rather than silently chosen for eval.py.
    prev_c = C.shift(1)
    tr = pd.concat([(H - L).stack(), (H - prev_c).abs().stack(), (L - prev_c).abs().stack()],
                   axis=1).max(axis=1).unstack()
    atr = tr.ewm(alpha=1.0 / ATR_N, adjust=False, min_periods=ATR_N).mean()
    bars_to_date = C.notna().cumsum()

    cand = pd.read_parquet(DATA / "v001_sas_candidates.parquet", columns=["trading_date", "symbol"])
    cand["date"] = pd.to_datetime(cand.trading_date).dt.strftime("%Y-%m-%d")
    # exclusions_v003: manual_runs / non_session_runs / uncorroborated_publication_runs,
    # each a dict carrying a "reason" and a "trading_dates" list (PREREG 2.1's exclusion set).
    excl, excl_by_reason = set(), {}
    ef = DATA / "exclusions_v003.json"
    if ef.exists():
        ex = json.loads(ef.read_text())
        for key in ("manual_runs", "non_session_runs", "uncorroborated_publication_runs"):
            dates = {str(x)[:10] for x in (ex.get(key) or {}).get("trading_dates", [])}
            excl_by_reason[key] = sorted(dates)
            excl |= dates
    print("exclusions: " + ", ".join(f"{k}={len(v)}" for k, v in excl_by_reason.items())
          + f"  (union {len(excl)} nights)")

    nights = sorted(d for d in cand.date.unique() if a.start <= d <= a.end and d in C.index)
    rows = []
    for t in nights:
        i = sessions.index(t)
        on_t = C.loc[t].notna()
        enough = bars_to_date.loc[t] >= MIN_BARS
        has_atr = atr.loc[t].notna()
        Bt = C.columns[on_t & enough & has_atr]
        if len(Bt) == 0:
            continue
        target = C.loc[t, Bt] + ATR_MULT * atr.loc[t, Bt]

        fwd = H.iloc[i + 1:i + 1 + HORIZON][Bt]
        n_fwd = int(len(fwd))
        touched = (fwd >= target).any(axis=0) if n_fwd else pd.Series(False, index=Bt)
        bars_seen = fwd.notna().sum(axis=0)
        # right-censoring: short forward history and no touch -> ungradeable, never a non-move
        censored = (bars_seen < HORIZON) & (~touched)
        gradeable = Bt[~censored]
        movers = Bt[touched]

        Ut = set(cand.loc[cand.date == t, "symbol"].dropna().astype(str))
        # n_t and m_t are computed from DISJOINT code paths and are never intersected here.
        n_t = len(Ut & set(gradeable))
        m_t = int(len(movers))
        b_t = int(len(gradeable))
        rows.append({"night": t, "b_t": b_t, "n_t": n_t, "m_t": m_t,
                     "B_t_before_censor": int(len(Bt)),
                     "ungradeable": int(censored.sum()),
                     "ungradeable_pct": round(100.0 * censored.sum() / len(Bt), 2),
                     "fwd_sessions": n_fwd,
                     "U_t_all": len(Ut),
                     "excluded_run": t in excl})
    df = pd.DataFrame(rows)

    blob_n = len(base)
    df["B_t_cov_pct"] = (100.0 * df.B_t_before_censor / blob_n).round(2)
    df["contributing"] = ((df.m_t >= 1) & (df.n_t >= 1) & (df.B_t_cov_pct >= 90.0)
                          & (df.ungradeable_pct <= 10.0) & (~df.excluded_run))

    out = Path(a.out)
    L_ = []
    L_.append("# Steward — Q030 R2(iii): counts-only dry run on the sealed period\n")
    L_.append(f"_Generated {pd.Timestamp.utcnow():%Y-%m-%d} from `{Path(a.manifest).name}`. "
              "**Counts only.** `b_t`, `n_t`, `m_t` and the exclusion reasons — no `recall_t`, no `e_t`, "
              "no lift, and **no intersection `|M_t ∩ U_t^B|`**, which stays sealed until the "
              "registered decision date. INTERNAL / NON_QUOTABLE._\n")
    L_.append(f"Window **{a.start} .. {a.end}**, {len(df)} pick nights. Base universe `B` = **{blob_n}** "
              f"symbols from the pinned blob `{BLOB_COMMIT}:{BLOB_PATH}` (sha256 `{BLOB_SHA[:12]}…`, "
              "hashed from committed bytes).\n")
    L_.append("## What R2(iii) was asked: is `m_t >= 1` ever binding?\n")
    z = int((df.m_t == 0).sum())
    L_.append(f"- Nights with `m_t = 0`: **{z} of {len(df)}**"
              + ("  — the floor never binds on the sealed panel." if z == 0 else "  — it binds; see the table.") + "\n")
    L_.append(f"- `m_t` distribution: min **{df.m_t.min()}**, median **{int(df.m_t.median())}**, "
              f"max **{df.m_t.max()}**, mean {df.m_t.mean():.1f}\n")
    L_.append(f"- `n_t` distribution: min **{df.n_t.min()}**, median **{int(df.n_t.median())}**, "
              f"max **{df.n_t.max()}**\n")
    L_.append(f"- `b_t` distribution: min **{df.b_t.min()}**, median **{int(df.b_t.median())}**, "
              f"max **{df.b_t.max()}**\n")
    L_.append(f"- Nights meeting every §2.5 contributing test: **{int(df.contributing.sum())} of {len(df)}** "
              f"= **{df.contributing.mean():.4f}** per pick night\n")
    L_.append(f"- Base-universe coverage `|B_t|/2405`: min **{df.B_t_cov_pct.min():.2f}%**, "
              f"median **{df.B_t_cov_pct.median():.2f}%** against the §2.5 **90%** gate\n")
    L_.append(f"- Ungradeable share: max **{df.ungradeable_pct.max():.2f}%** against the **10%** gate\n")
    L_.append("\n## Per-night counts\n")
    cols = ["night", "b_t", "n_t", "m_t", "U_t_all", "B_t_cov_pct", "ungradeable", "ungradeable_pct",
            "fwd_sessions", "contributing"]
    L_.append("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
    for _, r in df.iterrows():
        L_.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    L_.append("\n## Excluded runs inside the window (exclusions_v003)\n")
    for k, v in excl_by_reason.items():
        inside = [d for d in v if a.start <= d <= a.end]
        L_.append(f"- `{k}`: {len(inside)} inside the window" + (f" — {', '.join(inside)}" if inside else ""))
    L_.append("\n## Open item for the lock\n")
    L_.append("PREREG §2.2 names **ATR14** without naming its smoothing. This dry run used Wilder "
              "(`alpha = 1/14`). Simple-mean ATR14 gives a different mover level and therefore a "
              "different `m_t`. **The registrar must fix the smoothing in §2.2 at `apply` time** so "
              "`eval.py` is not left to choose it. This is a counts artefact only; no outcome was read.\n")
    out.write_text("\n".join(L_) + "\n", encoding="utf-8")
    df.to_csv(out.with_suffix(".csv"), index=False)
    print(f"wrote {out.relative_to(ROOT)}  ({len(df)} nights, m_t=0 on {z})")


if __name__ == "__main__":
    main()
