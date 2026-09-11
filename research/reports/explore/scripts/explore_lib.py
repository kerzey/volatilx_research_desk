"""EXPLORE_001 shared helpers. In-sample only.

Loads the in-sample split via eval_utils.load_split(manifest, "in_sample") and the frozen
Alpaca price tables via eval_utils.load_table. Never touches the out-of-sample split:
every candidate/pick frame is filtered to trading_date <= in_sample_end, and price bars
after that date are used only as the forward path (<= 60 trading days) of those rows.

Conventions
-----------
* Price basis = signal-date raw basis (what the targets are quoted in).
  basis(x) = split_bar(x) * raw_close(d) / split_close(d), with the factor snapped.
* Trading-day index k: k=1 is the first session after the pick night d.
* Touch = regular-session daily high (bull) / low (bear) crossing the level.
* Ladder windows (volatilx services/sas_conviction_card.py:190): L1/L2 20, L3/L4 40, L5/L6 60.
* Timestamps: April-Aug 2026 are all EDT (UTC-4). Regular session 13:30-20:00 UTC.
  SAS publishes ~21:0x UTC, so the first actionable after-hours bar is stamped 21:00 UTC.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research" / "lib"))
import eval_utils as eu  # noqa: E402

M = str(ROOT / "research" / "data" / "manifest_v001.json")
P = str(ROOT / "research" / "data" / "manifest_prices_v001.json")
WORK = ROOT / "research" / "reports" / "explore" / "work"
WORK.mkdir(parents=True, exist_ok=True)
IN_SAMPLE_END = pd.Timestamp(eu.load_manifest(M)["in_sample_end"])
HORIZON = 60
LADDER = ["L1", "L2", "L3", "L4", "L5", "L6"]
LWIN = {"L1": 20, "L2": 20, "L3": 40, "L4": 40, "L5": 60, "L6": 60}
LANE_SRC = [("day_trading", 0), ("day_trading", 1), ("swing_trading", 0),
            ("swing_trading", 1), ("longterm_trading", 0), ("longterm_trading", 1)]
COUNTER_KEYS = ["day_c1", "day_c2", "swing_c1", "swing_c2", "long_c1", "long_c2"]


def J(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    if isinstance(x, (dict, list)):
        return x
    try:
        return json.loads(x)
    except Exception:
        return None


def fnum(v):
    try:
        f = float(v)
        return f if np.isfinite(f) else None
    except (TypeError, ValueError):
        return None


# ----------------------------------------------------------------------------- data
def load_candidates() -> pd.DataFrame:
    df = eu.load_split(M, "in_sample", name="sas_candidates")
    assert df.trading_date.max() <= IN_SAMPLE_END
    return df


def load_excursion_v2() -> pd.DataFrame:
    ex = eu.load_split(M, "in_sample", name="sas_excursion")
    assert ex.trading_date.max() <= IN_SAMPLE_END
    v2 = ex[ex.computation_version == "v2"].copy()
    dup = v2.duplicated(["trading_date", "symbol"]).sum()
    assert dup == 0, f"v2 not unique per (date,symbol): {dup}"
    return v2


def load_prices():
    dr = eu.load_table(P, "prices_daily_raw")
    ds = eu.load_table(P, "prices_daily_split")
    for d in (dr, ds):
        d["date"] = pd.to_datetime(d["date"])
    m = dr.merge(ds[["symbol", "date", "o", "h", "l", "c"]], on=["symbol", "date"],
                 suffixes=("", "_s"))
    m["f"] = snap_factor(m["c"] / m["c_s"])
    return m.sort_values(["symbol", "date"]).reset_index(drop=True)


def snap_factor(f: pd.Series) -> pd.Series:
    f = f.astype(float)
    hi = np.round(f, 2)
    lo = 1.0 / np.round(1.0 / f, 2)
    return pd.Series(np.where(f >= 1, hi, lo), index=f.index)


def load_hourly() -> pd.DataFrame:
    h = eu.load_table(P, "prices_hourly_raw")
    h["t"] = pd.to_datetime(h["t"], utc=True)
    h["d"] = h["t"].dt.tz_convert("America/New_York").dt.normalize().dt.tz_localize(None)
    h["hr"] = h["t"].dt.hour
    return h


def calendar(prices: pd.DataFrame) -> pd.DatetimeIndex:
    return pd.DatetimeIndex(sorted(prices.loc[prices.symbol == "SPY", "date"].unique()))


# ----------------------------------------------------------------------------- candidate parsing
def parse_candidate(row) -> dict:
    ctx = J(row.context_json) or {}
    tech = ctx.get("technical_snapshot") or {}
    trend = tech.get("trend") or {}
    gex = ctx.get("gex_context") or {}
    flow = (ctx.get("options_flow_context") or {}).get("symbol_daily") or {}
    cat = ctx.get("catalyst_context") or {}
    pp = J(row.public_payload_json) or {}
    lp = pp.get("lane_plans") or {}
    out = {
        "spot": fnum(tech.get("spot_close")),
        "atr_pct": fnum(trend.get("atr_pct")),
        "above_20ma": fnum(trend.get("above_20ma")),
        "above_50ma": fnum(trend.get("above_50ma")),
        "gex_regime": gex.get("regime"),
        "gex_pin_risk": gex.get("pin_risk"),
        "gex_flip": fnum(gex.get("gamma_flip")),
        "net_gex": fnum(gex.get("net_gex")),
        "flow_total_premium": fnum(flow.get("total_premium")),
        "flow_dir_ratio": fnum(flow.get("dir_ratio")),
        "next_earnings_ctx": cat.get("next_earnings_date"),
        "days_to_earn_ctx": fnum(cat.get("days_to_earnings")),
        "src_membership": ",".join(sorted((J(row.source_payloads_json) or {}).keys())),
        "has_lane_plans": bool(lp),
    }
    for (lane, idx), lab in zip(LANE_SRC, LADDER):
        tg = ((lp.get(lane) or {}).get("targets") or [])
        out[lab] = fnum(tg[idx]) if idx < len(tg) else None
    for lane, short in (("day_trading", "day"), ("swing_trading", "swing"), ("longterm_trading", "long")):
        ld = lp.get(lane) or {}
        out[f"{short}_entry"] = fnum(ld.get("entry"))
        out[f"{short}_stop"] = fnum(ld.get("stop"))
        out[f"{short}_inval"] = fnum(ld.get("invalidation"))
    ex = pp.get("execution_private") or {}
    out["entry_window"] = ex.get("entry_window")
    out["entry_trigger"] = ex.get("entry_trigger")
    oc = pp.get("options_context") or {}
    out["opt_structure"] = oc.get("suggested_structure")
    out["opt_earnings_conflict"] = oc.get("earnings_conflict")
    return out


# ----------------------------------------------------------------------------- paths
class PathBook:
    """Forward daily bars (signal-date basis) for (symbol, d), k = 1..HORIZON."""

    def __init__(self, prices: pd.DataFrame):
        self.cal = calendar(prices)
        self.pos = {d: i for i, d in enumerate(self.cal)}
        self.by_sym = {s: g.set_index("date") for s, g in prices.groupby("symbol")}

    def forward(self, sym: str, d: pd.Timestamp, horizon: int = HORIZON):
        g = self.by_sym.get(sym)
        if g is None or d not in g.index or d not in self.pos:
            return None
        i = self.pos[d]
        dates = self.cal[i + 1: i + 1 + horizon]
        base = g.loc[d]
        scale = base["f"]  # snapped raw_close(d)/split_close(d)
        fwd = g.reindex(dates)
        out = pd.DataFrame({"k": np.arange(1, len(dates) + 1)}, index=dates)
        # split-adjusted bars rescaled to the signal-date basis
        for col in ("o", "h", "l", "c"):
            out[col] = fwd[f"{col}_s"].to_numpy() * scale
        out["raw_close_d"] = base["c"]
        return out

    def history(self, sym: str, d: pd.Timestamp, n: int):
        g = self.by_sym.get(sym)
        if g is None or d not in self.pos:
            return None
        i = self.pos[d]
        dates = self.cal[max(0, i - n + 1): i + 1]
        return g.reindex(dates)


def first_touch_k(fwd: pd.DataFrame, level, bull: bool, kmax: int, favorable: bool = True):
    """First k (1-based) where the regular-session bar crosses level. favorable=True means
    in the called direction (bull: high>=level); favorable=False = adverse (bull: low<=level)."""
    if level is None or fwd is None or len(fwd) == 0:
        return None
    f = fwd[fwd.k <= kmax]
    up = (bull and favorable) or ((not bull) and (not favorable))
    hit = f["h"].to_numpy() >= level if up else f["l"].to_numpy() <= level
    idx = np.flatnonzero(hit)
    return int(f["k"].iloc[idx[0]]) if len(idx) else None
