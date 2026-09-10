"""Deterministic helpers for research evaluations. Pure functions, fixed seeds, no DB.

Inference rules baked in:
  * The unit of inference is the trading night. Stock rows are aggregated per night first.
  * Monte Carlo control draws estimate a counterfactual; they never add to n.
  * CIs come from date-clustered (or block) bootstrap; p-values from permutation tests.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

SEED = 20260909
N_FLOOR_CELL = 20          # nights per stratum
N_FLOOR_TOTAL = 80         # nights overall


# ----------------------------------------------------------------------------- loading
def load_manifest(manifest: str | Path) -> dict:
    return json.loads(Path(manifest).read_text())


def load_table(manifest: str | Path, name: str) -> pd.DataFrame:
    t = next(t for t in load_manifest(manifest)["tables"] if t["name"] == name)
    return pd.read_parquet(t["file"])


def load_split(manifest: str | Path, split: str, name: str = "sas_candidates",
               date_col: str = "trading_date") -> pd.DataFrame:
    """split in {'in_sample','out_of_sample','all'}. The Explorer may only pass 'in_sample'."""
    m = load_manifest(manifest)
    df = load_table(manifest, name)
    df[date_col] = pd.to_datetime(df[date_col])
    if split == "all":
        return df
    end = m.get("in_sample_end")
    if end is None:
        dates = np.sort(df[date_col].unique())
        end = pd.Timestamp(dates[len(dates) // 2])
    end = pd.Timestamp(end)
    return df[df[date_col] <= end] if split == "in_sample" else df[df[date_col] > end]


# ----------------------------------------------------------------------------- returns
def simple_horizon_return(open_next: pd.Series, close_h: pd.Series, direction: pd.Series) -> pd.Series:
    """Dir × (Close_{t+h} − Open_{t+1}) / Open_{t+1}. Bear direction flips sign."""
    raw = (close_h - open_next) / open_next
    sign = np.where(direction.astype(str).str.lower().str.startswith("bear"), -1.0, 1.0)
    return raw * sign


def net_of_costs(r: pd.Series, bps_per_side: float = 10.0) -> pd.Series:
    return r - 2 * bps_per_side / 1e4


def nightly_basket(df: pd.DataFrame, value_col: str, date_col: str = "trading_date") -> pd.Series:
    """Equal-weight basket return per night. Index = night."""
    return df.groupby(date_col)[value_col].mean()


def mc_control_per_night(universe: pd.DataFrame, k_by_night: pd.Series, value_col: str,
                         date_col: str = "trading_date", n_draws: int = 2000,
                         seed: int = SEED) -> pd.Series:
    """Expected equal-weight return of K_t random picks from the night's universe.
    Returns one number per night — the MC draws are averaged, not stacked."""
    rng = np.random.default_rng(seed)
    out = {}
    for night, g in universe.groupby(date_col):
        vals = g[value_col].dropna().to_numpy()
        k = int(k_by_night.get(night, 0))
        if k == 0 or len(vals) < 2 * k:
            continue
        draws = np.array([rng.choice(vals, size=k, replace=False).mean() for _ in range(n_draws)])
        out[night] = draws.mean()
    return pd.Series(out, name="control")


# ----------------------------------------------------------------------------- inference
def cluster_bootstrap_ci(x: pd.Series, n_boot: int = 2000, alpha: float = 0.05,
                         seed: int = SEED) -> tuple[float, float, float]:
    """Bootstrap over nights (each night = one cluster). x indexed by night."""
    v = x.dropna().to_numpy(float)
    if len(v) == 0:
        return (np.nan, np.nan, np.nan)
    rng = np.random.default_rng(seed)
    boots = np.array([rng.choice(v, size=len(v), replace=True).mean() for _ in range(n_boot)])
    return float(v.mean()), float(np.quantile(boots, alpha / 2)), float(np.quantile(boots, 1 - alpha / 2))


def stationary_block_bootstrap_ci(x: pd.Series, block_len: int, n_boot: int = 2000,
                                  alpha: float = 0.05, seed: int = SEED) -> tuple[float, float, float]:
    """Politis–Romano stationary bootstrap for overlapping-horizon nightly series (T+20/T+60)."""
    v = x.dropna().to_numpy(float)
    n = len(v)
    if n == 0:
        return (np.nan, np.nan, np.nan)
    rng = np.random.default_rng(seed)
    p = 1.0 / max(block_len, 1)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        idx = np.empty(n, dtype=int)
        i = rng.integers(n)
        for j in range(n):
            if j > 0 and rng.random() < p:
                i = rng.integers(n)
            idx[j] = i
            i = (i + 1) % n
        boots[b] = v[idx].mean()
    return float(v.mean()), float(np.quantile(boots, alpha / 2)), float(np.quantile(boots, 1 - alpha / 2))


def signflip_permutation_p(alpha_t: pd.Series, n_perm: int = 10000, seed: int = SEED) -> float:
    """Two-sided sign-flip permutation test of H0: E[alpha_t] = 0, treating nights as exchangeable."""
    v = alpha_t.dropna().to_numpy(float)
    if len(v) == 0:
        return np.nan
    rng = np.random.default_rng(seed)
    obs = abs(v.mean())
    flips = rng.choice([-1.0, 1.0], size=(n_perm, len(v)))
    null = np.abs((flips * v).mean(axis=1))
    return float((np.sum(null >= obs) + 1) / (n_perm + 1))


def benjamini_hochberg(pvals: Iterable[float]) -> np.ndarray:
    p = np.asarray(list(pvals), float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order] * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.clip(q, 0, 1)
    return out


def stratified_nightly(alpha_t: pd.Series, strata: pd.Series) -> pd.DataFrame:
    """Mean/CI of nightly alpha per stratum; suppress strata with < N_FLOOR_CELL nights."""
    rows = []
    df = pd.DataFrame({"a": alpha_t, "s": strata}).dropna()
    for s, g in df.groupby("s"):
        n = len(g)
        if n < N_FLOOR_CELL:
            rows.append({"stratum": s, "n_nights": n, "mean": None, "lo": None, "hi": None, "status": "SUPPRESSED"})
            continue
        m, lo, hi = cluster_bootstrap_ci(g["a"])
        rows.append({"stratum": s, "n_nights": n, "mean": m, "lo": lo, "hi": hi, "status": "ok"})
    return pd.DataFrame(rows)


def power_hint(sigma_alpha: float, n_nights: int, alpha: float = 0.05, power: float = 0.80) -> float:
    """Minimum detectable effect (two-sided) for a one-sample mean; sanity check for PREREG §5."""
    from scipy.stats import norm
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    return float(z * sigma_alpha / np.sqrt(n_nights))


def verdict(mean_oos: float, lo: float, hi: float, p_perm: float, n_nights: int,
            same_sign_both_halves: bool, mpe: float, worst_regime_mean: float | None = None) -> str:
    """Historical verdict per PREREG §8. Prospective confirmation is assigned by the controller."""
    if n_nights < N_FLOOR_TOTAL:
        return "INCONCLUSIVE"
    regime_ok = worst_regime_mean is None or worst_regime_mean >= -mpe
    if mean_oos > mpe and lo > 0 and p_perm <= 0.05 and same_sign_both_halves and regime_ok:
        return "HISTORICALLY_CONFIRMED"
    if lo <= 0 <= hi and abs(mean_oos) < mpe:
        return "NULL"
    return "INCONCLUSIVE"
