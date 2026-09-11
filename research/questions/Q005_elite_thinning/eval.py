#!/usr/bin/env python3
"""Q005 elite_thinning -- deterministic evaluation of the locked PREREG.

PREREG   research/questions/Q005_elite_thinning/PREREG.md (commit c52fa16, sha256 8347b498...cd7bc)
Data     research/data/manifest_v001.json          (sas_candidates, sas_runs, market_regime)
         research/data/manifest_prices_v001.json   (prices_daily_split: trailing bars only)
         research/data/exclusions_v001.json
Type     DIAGNOSTIC decomposition. Every number is NON_QUOTABLE. No outcome column is read.

Run:     python research/questions/Q005_elite_thinning/eval.py
Writes   results/nightly.csv, results/run_summary.json, results/SUMMARY.md and results/*.csv tables;
         prints the run_summary JSON block to stdout. Fixed seeds; byte-identical on re-run.
Reading choices for every ambiguity are logged in results/NOTES.md (Part A, fixed before the first run).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

QDIR = Path(__file__).resolve().parent
ROOT = QDIR.parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "research" / "lib"))
import eval_utils as eu  # noqa: E402

RES = QDIR / "results"
RES.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------- fixed spec (PREREG)
MANIFEST = "research/data/manifest_v001.json"
MANIFEST_PRICES = "research/data/manifest_prices_v001.json"
EXCLUSIONS = "research/data/exclusions_v001.json"
PREREG = QDIR / "PREREG.md"

WIN_START, WIN_END = pd.Timestamp("2026-04-01"), pd.Timestamp("2026-09-10")      # PREREG §2
P0_START, P0_END = pd.Timestamp("2026-04-01"), pd.Timestamp("2026-06-30")        # PREREG §3
P1_START, P1_END = pd.Timestamp("2026-07-01"), pd.Timestamp("2026-09-10")        # PREREG §3
ELITE = 90.0                                                                     # PREREG §2
EPS = 1e-9
ALPHA_GATE = 0.05                                                                # PREREG §4/§8
Q_BH = 0.10                                                                      # PREREG §7
EXPLAINS_SHARE, EXPLAINS_LO = 0.50, 0.25                                         # PREREG §8
CONTRIB_SHARE, CONTRIB_LO = 0.20, 0.00                                           # PREREG §8
HOLD_SHARE = 0.20                                                                # PREREG §8 month panel
N_BOOT = 2000                                                                    # PREREG §4
N_PERM = 10000
R_TIE = 25                                                                       # NOTES A6
SEED = eu.SEED                                                                   # 20260909
SEED_TIE_POINT = 20260911
SEED_TIE_BOOT = 20260912
FLOOR_CELL, FLOOR_TOTAL = eu.N_FLOOR_CELL, eu.N_FLOOR_TOTAL
QS = (0.50, 0.90, 0.95, 0.99)

DIMS = ["flow_strength", "technical_structure", "gex_alignment", "projection",
        "fundamental_quality", "catalyst_event", "smart_money_confirmation"]
CONFIRM_DIMS = ["flow_strength", "technical_structure", "smart_money_confirmation", "catalyst_event"]
CONFIRM_THRESHOLD = 65.0                  # services/super_agent_select_scoring.py:97-130
TF_CODES = {"short": 0, "swing": 1, "long": 2}
TF_NAMES = {v: k for k, v in TF_CODES.items()}
DIR_CODES = {"bullish": 0, "bearish": 1, "mixed": 2}
CFG_IGNORE = {"audit_output_dir", "market_regime"}   # NOTES A13

# The 14 Channel-3 components, in PREREG §4 order: (name, kind, key)
COMPONENTS = [
    ("projection_score", "layer", "projection"),
    ("technical_structure_score", "layer", "technical_structure"),
    ("flow_strength_score", "layer", "flow_strength"),
    ("catalyst_event_score", "layer", "catalyst_event"),
    ("fundamental_quality_score", "layer", "fundamental_quality"),
    ("gex_alignment_score", "layer", "gex_alignment"),
    ("smart_money_confirmation_score", "layer", "smart_money_confirmation"),
    ("cross_layer_bonus", "additive", "bonus"),
    ("conflict_penalty", "additive", "conflict"),
    ("missing_data_penalty", "additive", "missing"),
    ("gex_missing_offset", "binary", "offset"),
    ("completeness_score", "not_in_arithmetic", None),
    ("best_timeframe_mix", "categorical", "tf"),
    ("atr_elite_cap", "binary_block", "block"),
]
COMP_NAMES = [c[0] for c in COMPONENTS]
CAT_JUNE = "catalyst_event_score__P0_June_only"

USE_COLS = ["id", "run_id", "trading_date", "symbol", "overall_score", "dominant_direction",
            "best_timeframe", "confidence_level", "completeness_score", "threshold_pass", "qualified",
            "qualification_reason", "selected_rank",
            "flow_strength_score", "technical_structure_score", "gex_alignment_score", "projection_score",
            "fundamental_quality_score", "catalyst_event_score", "smart_money_confirmation_score",
            "cross_layer_bonus", "conflict_penalty", "missing_data_penalty", "source_membership_json",
            "score_details_json", "missing_data_json", "industry", "market_regime_snapshot"]


def sha256_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jround(o):
    """Recursively make an object JSON-safe with 6-decimal floats (deterministic output)."""
    if isinstance(o, dict):
        return {str(k): jround(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jround(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return None if not np.isfinite(o) else round(float(o), 6)
    if isinstance(o, pd.Timestamp):
        return o.strftime("%Y-%m-%d")
    return o


def ds(t) -> str:
    return pd.Timestamp(t).strftime("%Y-%m-%d")


# ============================================================================= 1. load frozen data
excl = json.loads(Path(EXCLUSIONS).read_text())
MANUAL = {pd.Timestamp(d) for d in excl["manual_runs"]["trading_dates"]}
NON_SESSION = {pd.Timestamp(d) for d in excl["non_session_runs"]["trading_dates"]}
CATALYST_FIX = pd.Timestamp(excl["catalyst_layer_regime_change"]["fixed_from"])
REGIME_PIT_FROM = pd.Timestamp(excl["regime_label_point_in_time_from"])
man = eu.load_manifest(MANIFEST)
man_p = eu.load_manifest(MANIFEST_PRICES)
IN_SAMPLE_END = pd.Timestamp(man["in_sample_end"])
assert man_p["in_sample_end"] == man["in_sample_end"], "in_sample_end differs between manifests"

runs = eu.load_table(MANIFEST, "sas_runs")[["id", "trading_date", "started_at", "finished_at", "config_json"]].copy()
runs["trading_date"] = pd.to_datetime(runs["trading_date"])
runs = runs[(runs.trading_date >= WIN_START) & (runs.trading_date <= WIN_END)].sort_values("trading_date")
assert runs.trading_date.is_unique, "more than one sas_run per trading_date"

px = eu.load_table(MANIFEST_PRICES, "prices_daily_split")[["symbol", "date", "c", "v"]].copy()
px["date"] = pd.to_datetime(px["date"])
SPY_SESSIONS = set(px.loc[px.symbol == "SPY", "date"].tolist())

run_dates = sorted(set(runs.trading_date.tolist()))
off_session = [d for d in run_dates if d not in SPY_SESSIONS]
unlisted = [ds(d) for d in off_session if d not in NON_SESSION]
if unlisted:
    raise SystemExit(f"FATAL: sas_run on a non-session day not listed in exclusions: {unlisted}")
EXCL_MANUAL = sorted(d for d in run_dates if d in MANUAL)
EXCL_NONSESSION = sorted(off_session)
NIGHTS = [d for d in run_dates if d in SPY_SESSIONS and d not in MANUAL]
SESSIONS_WITHOUT_RUN = sorted(d for d in SPY_SESSIONS if WIN_START <= d <= WIN_END and d not in set(run_dates))
NI = {d: i for i, d in enumerate(NIGHTS)}
N_NIGHTS = len(NIGHTS)

cand_raw = eu.load_table(MANIFEST, "sas_candidates")
cand_raw = cand_raw[USE_COLS].copy()   # no outcome_* / level_hit_* / excursion column is carried
assert not [c for c in cand_raw.columns if c.startswith(("outcome_", "level_hit"))]
cand_raw["trading_date"] = pd.to_datetime(cand_raw["trading_date"])
cand_raw = cand_raw[(cand_raw.trading_date >= WIN_START) & (cand_raw.trading_date <= WIN_END)].copy()
cand = cand_raw[cand_raw.trading_date.isin(NIGHTS)].sort_values(["trading_date", "id"]).reset_index(drop=True)
run_id_by_date = dict(zip(runs.trading_date, runs.id))
assert (cand.run_id.to_numpy() == cand.trading_date.map(run_id_by_date).to_numpy()).all(), "run_id/date mismatch"
N_ROWS = len(cand)

regime = eu.load_table(MANIFEST, "market_regime")[["trading_date", "regime_version", "market_regime"]].copy()
regime["trading_date"] = pd.to_datetime(regime["trading_date"])
regime = regime[(regime.regime_version == "v1.2") & (regime.trading_date >= REGIME_PIT_FROM)]
assert regime.trading_date.is_unique
REGIME_BY_NIGHT = dict(zip(regime.trading_date, regime.market_regime))

# ============================================================================= 2. per-row scoring arrays
CFG = {d: json.loads(c) for d, c in zip(runs.trading_date, runs.config_json)}
A_S = np.full((N_ROWS, 7), np.nan)
A_W = np.zeros((N_ROWS, 7))
A_BW = np.zeros((N_ROWS, 7))
A_bonus = np.zeros(N_ROWS); A_conflict = np.zeros(N_ROWS); A_missing = np.zeros(N_ROWS)
A_offset = np.zeros(N_ROWS); A_ib = np.zeros(N_ROWS)
A_atr_only = np.zeros(N_ROWS, bool); A_block_obs = np.zeros(N_ROWS, bool)
for i, s in enumerate(cand.score_details_json.tolist()):
    d = json.loads(s)
    sub, wd = d.get("subscores") or {}, d.get("weighted_dimensions") or {}
    for j, k in enumerate(DIMS):
        v = sub.get(k)
        A_S[i, j] = np.nan if v is None else float(v)
        A_W[i, j] = float((wd.get(k) or {}).get("weight") or 0.0)
        A_BW[i, j] = float((wd.get(k) or {}).get("base_weight") or 0.0)
    A_bonus[i] = float(d.get("cross_layer_bonus") or 0.0)
    A_conflict[i] = float(d.get("conflict_penalty") or 0.0)
    A_missing[i] = float(d.get("missing_data_penalty") or 0.0)
    A_offset[i] = float(d.get("gex_missing_offset_value") or 0.0)
    A_ib[i] = float(d.get("industry_rotation_bonus") or 0.0)
    A_atr_only[i] = bool((d.get("atr_projection_meta") or {}).get("is_atr_only", False))
    A_block_obs[i] = bool(d.get("atr_elite_block_applied", False))

A_obs = cand.overall_score.to_numpy(float)
A_dir = cand.dominant_direction.map(DIR_CODES).to_numpy()
assert not np.isnan(A_dir.astype(float)).any(), "unexpected dominant_direction value"
A_dir = A_dir.astype(int)
A_tf = cand.best_timeframe.str.lower().map(TF_CODES).to_numpy()
assert not pd.isna(A_tf).any(), "unexpected best_timeframe value"
A_tf = A_tf.astype(int)
A_night = cand.trading_date.map(NI).to_numpy().astype(int)
A_completeness = cand.completeness_score.to_numpy(float)

# per-night config -> per-row arrays
night_block_en = np.zeros(N_NIGHTS, bool); night_projcap_en = np.zeros(N_NIGHTS, bool)
night_projcap = np.full(N_NIGHTS, 35.0); night_cap_bull = np.full(N_NIGHTS, 84.9); night_cap_bear = np.full(N_NIGHTS, 79.9)
night_mult = np.ones((N_NIGHTS, 3, 7)); night_cfg_w = np.zeros((N_NIGHTS, 7))
for t, i in NI.items():
    c = CFG[t]
    night_block_en[i] = c.get("atr_elite_block_enabled") is True
    night_projcap_en[i] = c.get("atr_sas_cap_enabled") is True
    night_projcap[i] = float(c.get("atr_sas_component_cap", 35.0))
    night_cap_bull[i] = float(c.get("atr_elite_bull_max_score", 84.9))
    night_cap_bear[i] = float(c.get("atr_elite_bear_max_score", 79.9))
    tw = c.get("timeframe_weight_multipliers") or {}
    for tf, tc in TF_CODES.items():
        for j, k in enumerate(DIMS):
            night_mult[i, tc, j] = float((tw.get(tf) or {}).get(k, 1.0) or 0.0)
    for j, k in enumerate(DIMS):
        night_cfg_w[i, j] = float((c.get("scoring_weights") or {}).get(k, 0.0) or 0.0)
A_block_en = night_block_en[A_night]
A_projcap_en = A_atr_only & night_projcap_en[A_night]
A_projcap = night_projcap[A_night]
A_cap = np.where(A_dir == DIR_CODES["bearish"], night_cap_bear[A_night], night_cap_bull[A_night])
MULT = night_mult[A_night]                                # (n, 3, 7)
IDX_PROJ = DIMS.index("projection")
IDX_CONFIRM = [DIMS.index(k) for k in CONFIRM_DIMS]
A_resid = np.zeros(N_ROWS)


def score_arr(idx, S_, W_, b, c, m, o, blk_override=None, resid=True):
    """overall_score arithmetic, services/super_agent_select_scoring.py:1284-1423 (+ sector bonus 139f87d)."""
    S2 = S_.copy()
    proj = S2[:, IDX_PROJ]
    capflag = A_projcap_en[idx] & ~np.isnan(proj)
    S2[:, IDX_PROJ] = np.where(capflag, np.minimum(proj, A_projcap[idx]), proj)          # :1295-1308
    avail = ~np.isnan(S2) & (W_ > 0)
    num = np.where(avail, np.nan_to_num(S2) * W_, 0.0).sum(1)
    den = np.where(avail, W_, 0.0).sum(1)
    base = np.divide(num, den, out=np.zeros_like(num), where=den > 0)                      # :1348
    pre = np.clip(base + b - c - m + o, 0.0, 100.0)                                         # :1393-1399
    cap = A_cap[idx]
    if blk_override is None:
        strong = (np.nan_to_num(S2[:, IDX_CONFIRM], nan=-1.0) >= CONFIRM_THRESHOLD).sum(1)
        blk = A_atr_only[idx] & A_block_en[idx] & (strong < 2)                               # :1407-1410
    else:
        blk = blk_override
    post = np.where(blk & (pre > cap), cap, pre)                                            # :1417-1418
    fin = np.clip(post + A_ib[idx], 0.0, 100.0)                                             # sector bonus
    return fin + A_resid[idx] if resid else fin


ALL = np.arange(N_ROWS)
_rec = score_arr(ALL, A_S, A_W, A_bonus, A_conflict, A_missing, A_offset, resid=False)
A_resid = A_obs - _rec
recon_ok = np.abs(A_resid) < 0.01
A_resid = np.where(recon_ok, 0.0, A_resid)       # sub-0.01 float noise dropped; real residuals kept (NOTES A11)
ELITE_OBS = A_obs >= ELITE
_rec_full = score_arr(ALL, A_S, A_W, A_bonus, A_conflict, A_missing, A_offset)
_pre = np.clip(np.divide(np.where(~np.isnan(A_S) & (A_W > 0), np.nan_to_num(A_S) * A_W, 0).sum(1),
                         np.where(~np.isnan(A_S) & (A_W > 0), A_W, 0).sum(1),
                         out=np.zeros(N_ROWS), where=np.where(~np.isnan(A_S) & (A_W > 0), A_W, 0).sum(1) > 0)
               + A_bonus - A_conflict - A_missing + A_offset, 0, 100)
_strong = (np.nan_to_num(A_S[:, IDX_CONFIRM], nan=-1.0) >= CONFIRM_THRESHOLD).sum(1)
_blk_rule = A_atr_only & A_block_en & (_strong < 2) & (_pre > A_cap)
col_check = {}
for j, k in enumerate(DIMS):
    colv = pd.to_numeric(cand[f"{k}_score"], errors="coerce").to_numpy(float)
    same = (np.isnan(colv) & np.isnan(A_S[:, j])) | (np.abs(colv - A_S[:, j]) < 1e-6)
    col_check[k] = int((~same).sum())
for k, arr in (("cross_layer_bonus", A_bonus), ("conflict_penalty", A_conflict), ("missing_data_penalty", A_missing)):
    col_check[k] = int((np.abs(cand[k].to_numpy(float) - arr) > 1e-6).sum())
_bw_ok = (A_BW == night_cfg_w[A_night]) | (A_W == 0)
_w_expect = A_BW * MULT[ALL, A_tf, :]
RECON = {
    "rows": N_ROWS,
    "rows_reproduced_within_0.01": int(recon_ok.sum()),
    "rows_with_residual": int((~recon_ok).sum()),
    "residual_dates": sorted({ds(d) for d in cand.trading_date[~recon_ok]}),
    "residual_rows_elite": int(ELITE_OBS[~recon_ok].sum()),
    "elite_flag_mismatch_after_residual": int(((_rec_full >= ELITE - EPS) != ELITE_OBS).sum()),
    "json_vs_column_mismatches": col_check,
    "atr_block_rule_vs_recorded_mismatch": int((_blk_rule != A_block_obs).sum()),
    "base_weight_vs_night_config_mismatch_rows": int((~_bw_ok).any(1).sum()),
    "effective_weight_vs_base_x_multiplier_mismatch_rows": int(((A_W > 0) & (np.abs(A_W - _w_expect) > 1e-6)).any(1).sum()),
}

# ============================================================================= 3. night-level table
NIGHT_DATE = np.array(NIGHTS, dtype="datetime64[ns]")
ROWS = [np.flatnonzero(A_night == i) for i in range(N_NIGHTS)]
NIGHT_N = np.array([len(r) for r in ROWS], float)
assert (NIGHT_N > 0).all(), "a night with zero candidates"
NIGHT_ELITE = np.array([ELITE_OBS[r].sum() for r in ROWS], float)
PUB = cand.selected_rank.notna().to_numpy()
ELITE_PUB = ELITE_OBS & PUB
NIGHT_ELITE_PUB = np.array([ELITE_PUB[r].sum() for r in ROWS], float)
NIGHT_NPUB = np.array([PUB[r].sum() for r in ROWS], float)
nd = pd.Series(NIGHTS)
IS_P0 = ((nd >= P0_START) & (nd <= P0_END)).to_numpy()
IS_P1 = ((nd >= P1_START) & (nd <= P1_END)).to_numpy()
assert (IS_P0 ^ IS_P1).all()
P0N = np.flatnonzero(IS_P0); P1N = np.flatnonzero(IS_P1)
MONTHS = [("2026-04", "Apr"), ("2026-05", "May"), ("2026-06", "Jun"), ("2026-07", "Jul"), ("2026-08", "Aug"),
          ("2026-09", "Sep(1-10)")]
NIGHT_MONTH = np.array([d.strftime("%Y-%m") for d in NIGHTS])

# SPY trailing path (bars dated <= night)
spy = px[px.symbol == "SPY"].sort_values("date").set_index("date")["c"]
spy_ret20 = spy / spy.shift(20) - 1.0
spy_rv20 = np.log(spy).diff().rolling(20, min_periods=20).std() * np.sqrt(252)
NIGHT_SPY_RET20 = np.array([spy_ret20.get(d, np.nan) for d in NIGHTS])
NIGHT_SPY_RV20 = np.array([spy_rv20.get(d, np.nan) for d in NIGHTS])
NIGHT_SPY_STRATUM = np.where(np.isnan(NIGHT_SPY_RET20), None, np.where(NIGHT_SPY_RET20 >= 0, "up_tape", "down_tape"))
NIGHT_REGIME = np.array([REGIME_BY_NIGHT.get(d) if d >= REGIME_PIT_FROM else None for d in NIGHTS], dtype=object)


# config hash per night (flattened, NOTES A13)
def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def cfg_flat(t):
    return {k: v for k, v in flatten(CFG[t]).items() if k.split(".")[0] not in CFG_IGNORE}


def cfg_hash(t):
    return hashlib.sha256(json.dumps(cfg_flat(t), sort_keys=True, default=str).encode()).hexdigest()[:12]


NIGHT_CFG_HASH = np.array([cfg_hash(t) for t in NIGHTS])

# sources per row
A_sources = [json.loads(s) if isinstance(s, str) and s else [] for s in cand.source_membership_json.tolist()]
SOURCE_NAMES = sorted({s for lst in A_sources for s in lst})
A_src = np.array([[s in lst for s in SOURCE_NAMES] for lst in A_sources], bool).reshape(N_ROWS, len(SOURCE_NAMES))
NIGHT_SRC = np.array([A_src[r].sum(0) for r in ROWS], float)

nightly = pd.DataFrame({
    "trading_date": [ds(d) for d in NIGHTS],
    "period": np.where(IS_P0, "P0", "P1"),
    "month": NIGHT_MONTH,
    "calendar_split": np.where(nd <= IN_SAMPLE_END, "in_sample", "sealed"),
    "n_candidates": NIGHT_N.astype(int),
    "elite_candidate": NIGHT_ELITE.astype(int),
    "elite_candidate_share": NIGHT_ELITE / NIGHT_N,
    "n_published": NIGHT_NPUB.astype(int),
    "elite_published": NIGHT_ELITE_PUB.astype(int),
    "score_p50": [np.quantile(A_obs[r], 0.5) for r in ROWS],
    "score_p90": [np.quantile(A_obs[r], 0.9) for r in ROWS],
    "score_max": [A_obs[r].max() for r in ROWS],
    "spy_ret20": NIGHT_SPY_RET20,
    "spy_rv20": NIGHT_SPY_RV20,
    "spy_stratum": NIGHT_SPY_STRATUM,
    "regime_v12_pit": NIGHT_REGIME,
    "config_hash": NIGHT_CFG_HASH,
})
for j, s in enumerate(SOURCE_NAMES):
    nightly[f"n_src_{s}"] = NIGHT_SRC[:, j].astype(int)
nightly.round(6).to_csv(RES / "nightly.csv", index=False)
ser = lambda arr: pd.Series(arr, index=pd.Index([ds(d) for d in NIGHTS], name="night"))  # noqa: E731

# ============================================================================= 4. Gate 0
X_DAYS = np.array([(d - WIN_START).days for d in NIGHTS], float)


def poisson_slope_batch(Y, x):
    """Vectorised Poisson-GLM (log link) slope on x for each row of Y (Newton-Raphson)."""
    xc = x - x.mean()
    b0 = np.log(Y.mean(1)); b1 = np.zeros(Y.shape[0])
    for _ in range(100):
        mu = np.exp(b0[:, None] + b1[:, None] * xc[None, :])
        r = Y - mu
        g0, g1 = r.sum(1), (r * xc).sum(1)
        h00, h01, h11 = mu.sum(1), (mu * xc).sum(1), (mu * xc * xc).sum(1)
        det = h00 * h11 - h01 * h01
        d0 = (h11 * g0 - h01 * g1) / det
        d1 = (-h01 * g0 + h00 * g1) / det
        b0 += d0; b1 += d1
        if np.max(np.abs(d1)) < 1e-13:
            break
    return b1


def gate0(y, x, is_p1, perm_seed=SEED):
    import statsmodels.api as sm
    from scipy.stats import binomtest
    y = np.asarray(y, float); is_p1 = np.asarray(is_p1, bool)
    X = sm.add_constant(x / 30.0)
    fit = sm.GLM(y, X, family=sm.families.Poisson()).fit()
    fitq = sm.GLM(y, X, family=sm.families.Poisson()).fit(scale="X2")
    slope30 = float(fit.params[1])
    rng = np.random.default_rng(perm_seed)
    P = np.array([rng.permutation(y) for _ in range(N_PERM)])
    b_obs = poisson_slope_batch(y[None, :], x)[0]
    b_perm = poisson_slope_batch(P, x)
    p_trend = float((np.sum(np.abs(b_perm) >= abs(b_obs) - 1e-12) + 1) / (N_PERM + 1))
    n0, n1 = int((~is_p1).sum()), int(is_p1.sum())
    k0, k1 = int(y[~is_p1].sum()), int(y[is_p1].sum())
    diff_obs = y[is_p1].mean() - y[~is_p1].mean()
    diff_perm = P[:, is_p1].mean(1) - P[:, ~is_p1].mean(1)
    p_rate = float((np.sum(np.abs(diff_perm) >= abs(diff_obs) - 1e-12) + 1) / (N_PERM + 1))
    ex2 = binomtest(k1, k0 + k1, n1 / (n0 + n1), alternative="two-sided").pvalue if k0 + k1 > 0 else np.nan
    ex1 = binomtest(k1, k0 + k1, n1 / (n0 + n1), alternative="less").pvalue if k0 + k1 > 0 else np.nan
    trend_sig = (slope30 < 0) and (p_trend <= ALPHA_GATE)
    rate_sig = (diff_obs < 0) and (p_rate <= ALPHA_GATE)
    trend_sig_model = (slope30 < 0) and (float(fit.pvalues[1]) <= ALPHA_GATE)
    rate_sig_model = (diff_obs < 0) and (ex2 <= ALPHA_GATE)
    return {
        "n_nights": len(y), "n0": n0, "n1": n1, "k0": k0, "k1": k1,
        "rate0_per_night": k0 / n0, "rate1_per_night": k1 / n1,
        "rate_ratio_P1_over_P0": (k1 / n1) / (k0 / n0) if k0 > 0 else np.nan,
        "poisson_slope_log_per_30d": slope30, "poisson_slope_newton_check": float(b_obs * 30.0),
        "rate_ratio_per_30d": float(np.exp(slope30)),
        "p_trend_perm": p_trend, "p_trend_wald": float(fit.pvalues[1]), "p_trend_quasi": float(fitq.pvalues[1]),
        "pearson_dispersion": float(fitq.scale),
        "diff_mean_P1_minus_P0": float(diff_obs),
        "p_rate_perm": p_rate, "p_rate_exact_two_sided": float(ex2), "p_rate_exact_one_sided_less": float(ex1),
        "trend_decline_significant": bool(trend_sig), "rate_decline_significant": bool(rate_sig),
        "fall_is_real": bool(trend_sig or rate_sig),
        "fall_is_real_model_based": bool(trend_sig_model or rate_sig_model),
        "p_gate": float(min(p_trend, p_rate)),
    }


G0 = gate0(NIGHT_ELITE, X_DAYS, IS_P1)
G0["gate_outcome_differs_perm_vs_model"] = G0["fall_is_real"] != G0["fall_is_real_model_based"]
G0_PUB = gate0(NIGHT_ELITE_PUB, X_DAYS, IS_P1)
# informational sensitivity: keep the non-session night 2026-04-03 (NOTES A1)
_sens_dates = sorted(d for d in run_dates if d not in MANUAL)
_sens_y = np.array([(cand_raw.loc[cand_raw.trading_date == d, "overall_score"] >= ELITE).sum() for d in _sens_dates], float)
_sens_x = np.array([(d - WIN_START).days for d in _sens_dates], float)
_sens_p1 = np.array([d >= P1_START for d in _sens_dates])
G0_SENS = gate0(_sens_y, _sens_x, _sens_p1)
BH_Q_GATE = float(eu.benjamini_hochberg([G0["p_gate"]])[0])     # F2 family, m = 1 registered test
BH_WITHIN_GATE = [float(q) for q in eu.benjamini_hochberg([G0["p_trend_perm"], G0["p_rate_perm"]])]
GATE_NULL = not G0["fall_is_real"]

pd.DataFrame([{"target": "elite_candidate (primary)", **G0},
              {"target": "elite_published (secondary)", **G0_PUB},
              {"target": "elite_candidate incl. 2026-04-03 (sensitivity, informational)", **G0_SENS}]
             ).round(6).to_csv(RES / "gate0.csv", index=False)

# ============================================================================= 5. descriptive panels
def period_rate_row(label, mask):
    idx = np.flatnonzero(mask)
    n = len(idx)
    row = {"cell": label, "n_nights": n, "n_candidates": int(NIGHT_N[idx].sum()),
           "elite_candidate": int(NIGHT_ELITE[idx].sum()), "elite_published": int(NIGHT_ELITE_PUB[idx].sum()),
           "n_published": int(NIGHT_NPUB[idx].sum())}
    if n < FLOOR_CELL:
        row.update({"status": "SUPPRESSED", "elite_cand_per_night": None, "ci_lo": None, "ci_hi": None,
                    "N_per_night": None, "N_ci_lo": None, "N_ci_hi": None,
                    "elite_pub_per_night": None, "pub_ci_lo": None, "pub_ci_hi": None})
        return row
    m, lo, hi = eu.cluster_bootstrap_ci(ser(NIGHT_ELITE)[mask])
    mn, nlo, nhi = eu.cluster_bootstrap_ci(ser(NIGHT_N)[mask])
    mp, plo, phi = eu.cluster_bootstrap_ci(ser(NIGHT_ELITE_PUB)[mask])
    row.update({"status": "ok", "elite_cand_per_night": m, "ci_lo": lo, "ci_hi": hi,
                "N_per_night": mn, "N_ci_lo": nlo, "N_ci_hi": nhi,
                "elite_pub_per_night": mp, "pub_ci_lo": plo, "pub_ci_hi": phi})
    return row


raw_pub_elite = cand_raw[(cand_raw.selected_rank.notna()) & (cand_raw.overall_score >= ELITE)]
raw_pub_by_month = raw_pub_elite.groupby(raw_pub_elite.trading_date.dt.strftime("%Y-%m")).size()
raw_cand_elite_by_month = cand_raw[cand_raw.overall_score >= ELITE].groupby(
    cand_raw[cand_raw.overall_score >= ELITE].trading_date.dt.strftime("%Y-%m")).size()
panel_rows = []
for mkey, mlab in MONTHS:
    r = period_rate_row(mlab, NIGHT_MONTH == mkey)
    r["month"] = mkey
    r["DATA_NOTES_raw_published_elite_all_runs"] = int(raw_pub_by_month.get(mkey, 0))
    r["raw_elite_candidate_all_runs"] = int(raw_cand_elite_by_month.get(mkey, 0))
    panel_rows.append(r)
for lab, mask in (("P0 (Apr1-Jun30)", IS_P0), ("P1 (Jul1-Sep10)", IS_P1),
                  ("in_sample (<=05-29)", (nd <= IN_SAMPLE_END).to_numpy()),
                  ("sealed (>=06-01)", (nd > IN_SAMPLE_END).to_numpy()), ("ALL", np.ones(N_NIGHTS, bool))):
    panel_rows.append(period_rate_row(lab, mask))
PANEL = pd.DataFrame(panel_rows)
PANEL.round(6).to_csv(RES / "monthly_panel.csv", index=False)

# published-elite derivation (PREREG §5) and conversion (NOTES A23)
_raw_p0 = raw_pub_elite[(raw_pub_elite.trading_date >= P0_START) & (raw_pub_elite.trading_date <= P0_END)]
_raw_p1 = raw_pub_elite[(raw_pub_elite.trading_date >= P1_START) & (raw_pub_elite.trading_date <= P1_END)]
PUB_DERIV = {
    "P0_published_elite_all_runs": len(_raw_p0),
    "P0_removed_on_excluded_nights": int(_raw_p0.trading_date.isin(set(EXCL_MANUAL) | set(EXCL_NONSESSION)).sum()),
    "P0_published_elite_corrected": int(NIGHT_ELITE_PUB[P0N].sum()),
    "P1_published_elite_all_runs": len(_raw_p1),
    "P1_removed_on_excluded_nights": int(_raw_p1.trading_date.isin(set(EXCL_MANUAL) | set(EXCL_NONSESSION)).sum()),
    "P1_published_elite_corrected": int(NIGHT_ELITE_PUB[P1N].sum()),
}
conv_rows = []
for lab, nights_idx in (("P0", P0N), ("P1", P1N)):
    rows = np.concatenate([ROWS[t] for t in nights_idx])
    e = rows[ELITE_OBS[rows]]
    reasons = cand.qualification_reason.iloc[e[~PUB[e]]].value_counts().to_dict()
    conv_rows.append({"period": lab, "elite_candidates": len(e), "elite_published": int(PUB[e].sum()),
                      "conversion": PUB[e].mean() if len(e) else np.nan,
                      "unpublished_elite_reasons": json.dumps(reasons, sort_keys=True)})
CONV = pd.DataFrame(conv_rows)
CONV.round(6).to_csv(RES / "published_conversion.csv", index=False)

# sources per period (Channel 1 context)
src_rows = []
for j, s in enumerate(SOURCE_NAMES):
    for lab, mask in (("P0", IS_P0), ("P1", IS_P1)):
        m, lo, hi = eu.cluster_bootstrap_ci(ser(NIGHT_SRC[:, j])[mask])
        src_rows.append({"source": s, "period": lab, "n_nights": int(mask.sum()), "per_night": m, "ci_lo": lo, "ci_hi": hi})
pd.DataFrame(src_rows).round(6).to_csv(RES / "channel1_sources_by_period.csv", index=False)

# regime (PIT, >= 06-09) and SPY-tape strata
strata_rows = []
for target, arr in (("elite_candidate_per_night", NIGHT_ELITE), ("elite_share_of_candidates", NIGHT_ELITE / NIGHT_N),
                    ("n_candidates_per_night", NIGHT_N), ("elite_published_per_night", NIGHT_ELITE_PUB)):
    for stratifier, lab_arr in (("market_regime_daily_v1.2_PIT(>=06-09)", NIGHT_REGIME), ("spy_tape_20d", NIGHT_SPY_STRATUM)):
        for per_lab, pmask in (("ALL", np.ones(N_NIGHTS, bool)), ("P0", IS_P0), ("P1", IS_P1)):
            st = pd.Series(np.where(pmask, lab_arr, None), index=ser(arr).index)
            tab = eu.stratified_nightly(ser(arr), st)
            for rr in tab.to_dict("records"):
                strata_rows.append({"target": target, "stratifier": stratifier, "period": per_lab, **rr})
STRATA = pd.DataFrame(strata_rows)
STRATA.round(6).to_csv(RES / "strata_regime_and_tape.csv", index=False)
spy_month = pd.DataFrame({"month": NIGHT_MONTH, "spy_ret20": NIGHT_SPY_RET20, "spy_rv20": NIGHT_SPY_RV20}
                         ).groupby("month").agg(nights=("spy_ret20", "size"), spy_ret20_mean=("spy_ret20", "mean"),
                                                spy_rv20_mean=("spy_rv20", "mean")).reset_index()
spy_month.round(6).to_csv(RES / "spy_tape_by_month.csv", index=False)
regime_nights = pd.Series([r for r in NIGHT_REGIME if r is not None]).value_counts().to_dict()

# market_regime_snapshot (point-in-time candidate column; Channel 3a context)
snap_lab = cand.market_regime_snapshot.fillna("").str.split(":").str[2].fillna("none/absent")
SNAP = pd.crosstab(np.where(IS_P0[A_night], "P0", "P1"), snap_lab.to_numpy(), normalize="index")
SNAP.round(6).to_csv(RES / "channel3a_regime_snapshot_by_period.csv")

# ============================================================================= 6. Channel 3a -- config
cfg_rows = []
for d in run_dates:
    cfg_rows.append({"trading_date": ds(d), "config_hash": hashlib.sha256(json.dumps(
        {k: v for k, v in flatten(CFG[d]).items() if k.split(".")[0] not in CFG_IGNORE}, sort_keys=True,
        default=str).encode()).hexdigest()[:12],
        "excluded": "manual_run" if d in MANUAL else ("non_session" if d not in SPY_SESSIONS else ""),
        "market_regime_cfg_value": json.dumps(CFG[d].get("market_regime"), default=str)})
pd.DataFrame(cfg_rows).to_csv(RES / "channel3a_config_timeline.csv", index=False)
segments = []
for i, t in enumerate(NIGHTS):
    if i == 0 or NIGHT_CFG_HASH[i] != NIGHT_CFG_HASH[i - 1]:
        segments.append({"hash": NIGHT_CFG_HASH[i], "start": t, "end": t, "start_i": i, "n_nights": 1})
    else:
        segments[-1]["end"] = t; segments[-1]["n_nights"] += 1


def classify(key, old, new, status):
    top = key.split(".")[0]
    ref = new if status != "removed" else old
    if top == "scoring_weights":
        cat = "weight"
    elif top == "timeframe_weight_multipliers":
        cat = "multiplier"
    elif isinstance(ref, bool):
        cat = "flag"
    else:
        cat = "threshold/parameter"
    behavioural = not (status == "added" and new is False)
    return cat, behavioural


rng_cfg = np.random.default_rng(SEED)
P_CFG = np.array([rng_cfg.permutation(NIGHT_ELITE) for _ in range(N_PERM)])
change_rows, diff_rows = [], []
for a, b in zip(segments[:-1], segments[1:]):
    fa, fb = cfg_flat(a["end"]), cfg_flat(b["start"])
    diffs = []
    for k in sorted(set(fa) | set(fb)):
        if k in fa and k in fb and json.dumps(fa[k], sort_keys=True, default=str) == json.dumps(fb[k], sort_keys=True, default=str):
            continue
        status = "changed" if (k in fa and k in fb) else ("added" if k in fb else "removed")
        cat, beh = classify(k, fa.get(k), fb.get(k), status)
        diffs.append({"effective_date": ds(b["start"]), "key": k, "status": status, "category": cat,
                      "behavioural": beh, "old": json.dumps(fa.get(k), default=str), "new": json.dumps(fb.get(k), default=str)})
    diff_rows.extend(diffs)
    i = b["start_i"]
    before, after = np.arange(0, i), np.arange(i, N_NIGHTS)
    mb, ma = NIGHT_ELITE[before].mean(), NIGHT_ELITE[after].mean()
    stat = ma - mb
    perm = P_CFG[:, after].mean(1) - P_CFG[:, before].mean(1)
    p_perm = float((np.sum(np.abs(perm) >= abs(stat) - 1e-12) + 1) / (N_PERM + 1))
    from scipy.stats import binomtest
    kb, ka = int(NIGHT_ELITE[before].sum()), int(NIGHT_ELITE[after].sum())
    p_ex = binomtest(ka, ka + kb, len(after) / N_NIGHTS, alternative="less").pvalue if ka + kb > 0 else np.nan
    lb, la = np.arange(max(0, i - 20), i), np.arange(i, min(N_NIGHTS, i + 20))
    any_beh = any(dd["behavioural"] for dd in diffs)
    evaluable = len(before) >= FLOOR_CELL and len(after) >= FLOOR_CELL
    brackets = bool(any_beh and evaluable and stat < 0 and p_perm <= ALPHA_GATE)
    change_rows.append({
        "effective_date": ds(b["start"]), "from_hash": a["hash"], "to_hash": b["hash"],
        "n_keys_changed": len(diffs), "n_behavioural": int(sum(dd["behavioural"] for dd in diffs)),
        "categories": ",".join(sorted({dd["category"] for dd in diffs if dd["behavioural"]})),
        "nights_before": len(before), "nights_after": len(after), "evaluable_floor": evaluable,
        "elite_per_night_before": mb, "elite_per_night_after": ma, "diff_after_minus_before": stat,
        "p_perm_two_sided": p_perm, "p_exact_poisson_one_sided_less": float(p_ex),
        "local20_before": NIGHT_ELITE[lb].mean() if len(lb) else np.nan,
        "local20_after": NIGHT_ELITE[la].mean() if len(la) else np.nan,
        "local20_n_before": len(lb), "local20_n_after": len(la),
        "brackets_the_fall": brackets})
CFG_CHANGES = pd.DataFrame(change_rows)
CFG_DIFFS = pd.DataFrame(diff_rows)
CFG_CHANGES.round(6).to_csv(RES / "channel3a_config_changes.csv", index=False)
CFG_DIFFS.to_csv(RES / "channel3a_config_diffs.csv", index=False)
CONFIG_FIRES = bool(len(CFG_CHANGES) and CFG_CHANGES.brackets_the_fall.any())
SEGMENTS_OUT = [{"hash": s["hash"], "start": ds(s["start"]), "end": ds(s["end"]), "n_nights": s["n_nights"]} for s in segments]

# ============================================================================= 7. Channel 4 descriptors (trailing bars)
pxs = px.sort_values(["symbol", "date"]).reset_index(drop=True)
pxs["dv"] = pxs.c * pxs.v
pxs["c_lag20"] = pxs.groupby("symbol", sort=False)["c"].shift(20)
pxs["c_lag1"] = pxs.groupby("symbol", sort=False)["c"].shift(1)
pxs["dv20"] = pxs.groupby("symbol", sort=False)["dv"].transform(lambda s: s.rolling(20, min_periods=20).mean())
pxs["ret20"] = pxs.c / pxs.c_lag20 - 1.0
pxs["lr"] = np.log(pxs.c) - np.log(pxs.c_lag1)
pxs["rv20"] = pxs.groupby("symbol", sort=False)["lr"].transform(lambda s: s.rolling(20, min_periods=20).std()) * np.sqrt(252)
left = pd.DataFrame({"row": ALL, "symbol": cand.symbol.astype(str).to_numpy(),
                     "trading_date": cand.trading_date.astype("datetime64[ns]").to_numpy()}).sort_values("trading_date")
right = pxs[["symbol", "date", "c", "dv20", "ret20", "rv20"]].copy()
right["symbol"] = right.symbol.astype(str)
right["date"] = right.date.astype("datetime64[ns]")
right = right.sort_values("date")
mstat = pd.merge_asof(left, right, left_on="trading_date", right_on="date", by="symbol", direction="backward",
                      tolerance=pd.Timedelta(days=5)).sort_values("row")
assert (mstat["date"].dropna() <= mstat.loc[mstat["date"].notna(), "trading_date"]).all()   # knowledge time
A_px = mstat.c.to_numpy(float); A_dv20 = mstat.dv20.to_numpy(float)
A_ret20 = mstat.ret20.to_numpy(float); A_rv20 = mstat.rv20.to_numpy(float)
HAS_STATS = ~(np.isnan(A_px) | np.isnan(A_dv20))
px_cuts = np.quantile(A_px[HAS_STATS], [1 / 3, 2 / 3]); dv_cuts = np.quantile(A_dv20[HAS_STATS], [1 / 3, 2 / 3])
A_pt = np.searchsorted(px_cuts, A_px, side="right"); A_dvt = np.searchsorted(dv_cuts, A_dv20, side="right")
A_CELL = np.where(HAS_STATS, A_pt * 9 + A_dvt * 3 + A_dir, -1)
NC = 27

ever_p0 = set(cand.symbol[IS_P0[A_night]])
p1_rows = np.flatnonzero(IS_P1[A_night])
TURNOVER = float(np.mean([s not in ever_p0 for s in cand.symbol.iloc[p1_rows]]))
desc_rows = []
for lab, pm in (("P0", IS_P0[A_night]), ("P1", IS_P1[A_night])):
    r = {"period": lab, "candidate_rows": int(pm.sum()), "rows_with_price_stats": int((pm & HAS_STATS).sum())}
    for nm, arr in (("price_level", A_px), ("dollar_volume_20d", A_dv20), ("trailing_ret_20d", A_ret20), ("realized_vol_20d", A_rv20)):
        v = arr[pm & ~np.isnan(arr)]
        r[f"{nm}_median"] = float(np.median(v)); r[f"{nm}_mean"] = float(np.mean(v))
    for dn, dc in DIR_CODES.items():
        r[f"dir_{dn}"] = float(np.mean(A_dir[pm] == dc))
    for tn, tc in TF_CODES.items():
        r[f"tf_{tn}"] = float(np.mean(A_tf[pm] == tc))
    ind = cand.industry[pm]
    r["industry_populated_share"] = float(ind.notna().mean())
    r["industry_top5_populated_subset_only"] = json.dumps(ind.dropna().value_counts(normalize=True).head(5).round(4).to_dict())
    desc_rows.append(r)
DESC4 = pd.DataFrame(desc_rows)
DESC4.round(6).to_csv(RES / "channel4_descriptors.csv", index=False)

# ============================================================================= 8. decomposition machinery
def qmap(x1, ref_sorted, rng):
    """Randomised-tie quantile map of x1 onto the empirical (inverted-CDF) quantiles of ref_sorted (NOTES A6)."""
    n1, n0 = len(x1), len(ref_sorted)
    key = rng.random(n1)
    order = np.lexsort((key, x1))
    ranks = np.empty(n1, dtype=np.int64); ranks[order] = np.arange(n1)
    u = (ranks + 0.5) / n1
    k = np.clip(np.ceil(u * n0).astype(np.int64) - 1, 0, n0 - 1)
    return ref_sorted[k]


ADD_ARR = {"bonus": A_bonus, "conflict": A_conflict, "missing": A_missing, "offset": A_offset}


def make_override(kind, key, idx1, idx0ref, rng):
    """Return (override dict | None, status) replacing one component's P1 distribution with P0's."""
    if kind == "not_in_arithmetic":
        return None, "not_in_arithmetic"
    if len(idx0ref) == 0:
        return None, "no_reference_rows"
    if kind == "layer":
        j = DIMS.index(key)
        ref = A_S[idx0ref, j]; ref = np.sort(ref[~np.isnan(ref)])
        x = A_S[idx1, j]; m = ~np.isnan(x)
        if len(ref) == 0 or m.sum() == 0:
            return None, "no_data"
        col = x.copy(); col[m] = qmap(x[m], ref, rng)
        return {"S_cols": {j: col}}, "ok"
    if kind in ("additive", "binary"):
        arr = ADD_ARR[key]
        return {key: qmap(arr[idx1], np.sort(arr[idx0ref]), rng)}, "ok"
    if kind == "categorical":
        new = qmap(A_tf[idx1].astype(float), np.sort(A_tf[idx0ref].astype(float)), rng).astype(int)
        return {"tf_new": new}, "ok"
    if kind == "binary_block":
        new = qmap(A_block_obs[idx1].astype(float), np.sort(A_block_obs[idx0ref].astype(float)), rng) > 0.5
        return {"block": new}, "ok"
    raise ValueError(kind)


def score_with(idx1, overrides):
    S_ = A_S[idx1].copy(); W_ = A_W[idx1]
    vals = {k: v[idx1] for k, v in ADD_ARR.items()}
    blk = None
    for ov in overrides:
        if ov is None:
            continue
        for j, col in ov.get("S_cols", {}).items():
            S_[:, j] = col
        for k in ADD_ARR:
            if k in ov:
                vals[k] = ov[k]
        if "tf_new" in ov:
            old = A_tf[idx1]; new = ov["tf_new"]
            mo, mn = MULT[idx1, old, :], MULT[idx1, new, :]
            W_ = A_W[idx1] * np.divide(mn, mo, out=np.ones_like(mn), where=mo > 0)
        if "block" in ov:
            blk = ov["block"]
    fin = score_arr(idx1, S_, W_, vals["bonus"], vals["conflict"], vals["missing"], vals["offset"], blk_override=blk)
    return int((fin >= ELITE - EPS).sum())


def ch4_weights(idx1, idx0, method):
    c1, c0 = A_CELL[idx1], A_CELL[idx0]
    h1, h0 = c1 >= 0, c0 >= 0
    w = np.ones(len(idx1)); lost = 0.0
    if h1.sum() == 0 or h0.sum() == 0:
        return w, np.nan
    if method == "joint":
        p0 = np.bincount(c0[h0], minlength=NC) / h0.sum()
        p1 = np.bincount(c1[h1], minlength=NC) / h1.sum()
        wc = np.divide(p0, p1, out=np.zeros(NC), where=p1 > 0)
        lost = float(p0[p1 == 0].sum())
        ww = wc[c1[h1]]
    else:   # IPF raking on the three one-way margins
        dec1 = (c1[h1] // 9, (c1[h1] // 3) % 3, c1[h1] % 3)
        dec0 = (c0[h0] // 9, (c0[h0] // 3) % 3, c0[h0] % 3)
        tg = [np.bincount(a, minlength=3) / len(a) for a in dec0]
        ww = np.ones(h1.sum())
        for _ in range(100):
            for a, t in zip(dec1, tg):
                cur = np.bincount(a, weights=ww, minlength=3) / ww.sum()
                ww = ww * np.divide(t, cur, out=np.zeros(3), where=cur > 0)[a]
    ww = ww * (h1.sum() / ww.sum())
    w[h1] = ww
    return w, lost


ITEMS_TOP = ["channel1_candidate_count", "channel2_score_distribution", "channel4_universe_joint", "channel4_universe_ipf_margins"]
ITEMS_C3 = COMP_NAMES + [CAT_JUNE]


def decompose(p0n, p1n, rng, r_tie, order=None):
    p0n = np.asarray(p0n); p1n = np.asarray(p1n)
    idx0 = np.concatenate([ROWS[t] for t in p0n]); idx1 = np.concatenate([ROWS[t] for t in p1n])
    n0, n1 = len(p0n), len(p1n)
    k0, k1 = int(ELITE_OBS[idx0].sum()), int(ELITE_OBS[idx1].sum())
    S = k0 / n0 * n1 - k1
    out = {"n0": n0, "n1": n1, "k0": k0, "k1": k1, "S": S, "expected_P1_at_P0_rate": k0 / n0 * n1,
           "diff_rate": k1 / n1 - k0 / n0, "N0_per_night": len(idx0) / n0, "N1_per_night": len(idx1) / n1}
    cf = {}
    cf["channel1_candidate_count"] = (len(idx0) / n0) * float((NIGHT_ELITE[p1n] / NIGHT_N[p1n]).sum())
    wj, lost = ch4_weights(idx1, idx0, "joint"); wi, _ = ch4_weights(idx1, idx0, "ipf")
    cf["channel4_universe_joint"] = float((wj * ELITE_OBS[idx1]).sum())
    cf["channel4_universe_ipf_margins"] = float((wi * ELITE_OBS[idx1]).sum())
    out["channel4_joint_lost_mass"] = lost
    june_n = [t for t in p0n if CATALYST_FIX <= pd.Timestamp(NIGHT_DATE[t]) <= P0_END]
    idx0_june = np.concatenate([ROWS[t] for t in june_n]) if june_n else np.array([], int)
    acc = {k: 0.0 for k in ["channel2_score_distribution"] + ITEMS_C3}
    cum_acc = np.zeros(len(order)) if order is not None else None
    status = {}
    ref_obs = np.sort(A_obs[idx0])
    for _ in range(r_tie):
        acc["channel2_score_distribution"] += int((qmap(A_obs[idx1], ref_obs, rng) >= ELITE - EPS).sum())
        ovs = {}
        for name, kind, key in COMPONENTS:
            ovs[name], status[name] = make_override(kind, key, idx1, idx0, rng)
        ovs[CAT_JUNE], status[CAT_JUNE] = make_override("layer", "catalyst_event", idx1, idx0_june, rng)
        for name in ITEMS_C3:
            if ovs[name] is None:   # no change possible (0 by construction), or no reference rows (undefined)
                acc[name] += np.nan if status[name] == "no_reference_rows" else k1
            else:
                acc[name] += score_with(idx1, [ovs[name]])
        if order is not None:
            for i in range(len(order)):
                cum_acc[i] += score_with(idx1, [ovs[c] for c in order[: i + 1]])
    for k in acc:
        cf[k] = acc[k] / r_tie
    out["cf"] = cf
    out["share"] = {k: ((v - k1) / S if S > 0 else np.nan) for k, v in cf.items()}
    out["status"] = status
    if order is not None:
        cum = cum_acc / r_tie
        out["cum_cf"] = cum
        out["cum_share"] = (cum - k1) / S if S > 0 else np.full(len(order), np.nan)
    out["qshift"] = {f"p{int(q * 100)}": float(np.quantile(A_obs[idx1], q) - np.quantile(A_obs[idx0], q)) for q in QS}
    out["q0"] = {f"p{int(q * 100)}": float(np.quantile(A_obs[idx0], q)) for q in QS}
    out["q1"] = {f"p{int(q * 100)}": float(np.quantile(A_obs[idx1], q)) for q in QS}
    return out


LABEL_RANK = {"EXPLAINS": 3, "CONTRIBUTES": 2, "NOT_A_DRIVER": 1, "NOT_EVALUABLE": 0}


def attribution(share, lo, hi):
    if share is None or not np.isfinite(share) or lo is None or not np.isfinite(lo):
        return "NOT_EVALUABLE", False
    uninformative = bool(lo <= 0.0 and hi >= 1.0)
    if uninformative:
        return "NOT_A_DRIVER", True
    if share >= EXPLAINS_SHARE and lo >= EXPLAINS_LO:
        return "EXPLAINS", False
    if share >= CONTRIB_SHARE and lo >= CONTRIB_LO:
        return "CONTRIBUTES", False
    return "NOT_A_DRIVER", False


def pct_ci(vals):
    v = np.asarray(vals, float); v = v[np.isfinite(v)]
    if len(v) == 0:
        return np.nan, np.nan
    return float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))


# ============================================================================= 9. run the decomposition
DECOMP = None
if not GATE_NULL:
    rng_pt = np.random.default_rng(SEED_TIE_POINT)
    point = decompose(P0N, P1N, rng_pt, R_TIE)
    # greedy order: Channel-3 marginal shares, largest first; ties by PREREG list order (NOTES A19)
    ORDER = sorted(COMP_NAMES, key=lambda c: (-(point["share"][c] if np.isfinite(point["share"][c]) else -np.inf),
                                              COMP_NAMES.index(c)))
    point = decompose(P0N, P1N, np.random.default_rng(SEED_TIE_POINT), R_TIE, order=ORDER)

    # bootstrap: nights resampled within P0 and within P1 (NOTES A21)
    rng_b = np.random.default_rng(SEED); rng_t = np.random.default_rng(SEED_TIE_BOOT)
    boot = {k: [] for k in ITEMS_TOP[:1] + ["channel2_score_distribution"] + ITEMS_TOP[2:] + ITEMS_C3}
    boot_cum = []; boot_diff = []; boot_S = []; boot_q = {k: [] for k in point["qshift"]}
    n_S_nonpos = 0
    for b in range(N_BOOT):
        p0b = rng_b.choice(P0N, size=len(P0N), replace=True)
        p1b = rng_b.choice(P1N, size=len(P1N), replace=True)
        rb = decompose(p0b, p1b, rng_t, 1, order=ORDER)
        boot_diff.append(rb["diff_rate"]); boot_S.append(rb["S"])
        for k in boot_q:
            boot_q[k].append(rb["qshift"][k])
        if rb["S"] <= 0:
            n_S_nonpos += 1
            continue
        for k in boot:
            boot[k].append(rb["share"][k])
        boot_cum.append(rb["cum_share"])
    boot_cum = np.array(boot_cum)
    DIFF_CI = pct_ci(boot_diff)

    def item_row(name, family):
        sh = point["share"][name]
        lo, hi = pct_ci(boot[name])
        lab, unin = attribution(sh, lo, hi)
        st = point["status"].get(name, "ok")
        if st in ("not_in_arithmetic", "no_data"):
            lab, unin = "NOT_A_DRIVER", False
        return {"item": name, "family": family, "cf_elite_P1": point["cf"][name], "observed_elite_P1": point["k1"],
                "restored_share": sh, "ci_lo": lo, "ci_hi": hi, "label": lab, "uninformative": unin, "status": st}

    TOP_ROWS = [item_row("channel1_candidate_count", "channel1"), item_row("channel2_score_distribution", "channel2"),
                item_row("channel4_universe_joint", "channel4"), item_row("channel4_universe_ipf_margins", "channel4_secondary")]
    C3_ROWS = [item_row(c, "channel3") for c in COMP_NAMES] + [item_row(CAT_JUNE, "channel3_catalyst_postfix_P0")]

    # component distributions P0 vs P1 (context for the Channel-3 table)
    def comp_desc(name, kind, key):
        r = {"item": name}
        for lab, pm in (("P0", IS_P0[A_night]), ("P1", IS_P1[A_night])):
            if kind == "layer":
                v = A_S[pm, DIMS.index(key)]
                r[f"{lab}_null_share"] = float(np.isnan(v).mean()); v = v[~np.isnan(v)]
            elif kind in ("additive", "binary"):
                v = ADD_ARR[key][pm]
            elif kind == "not_in_arithmetic":
                v = A_completeness[pm]
            elif kind == "categorical":
                v = A_tf[pm].astype(float)
                for tn, tc in TF_CODES.items():
                    r[f"{lab}_tf_{tn}"] = float(np.mean(A_tf[pm] == tc))
            else:
                v = A_block_obs[pm].astype(float)
                r[f"{lab}_rows_at_84.9_or_79.9"] = float(np.mean(np.isin(np.round(A_obs[pm], 4), [84.9, 79.9])))
            r[f"{lab}_mean"] = float(np.mean(v)) if len(v) else np.nan
            r[f"{lab}_p50"] = float(np.quantile(v, 0.5)) if len(v) else np.nan
            r[f"{lab}_p90"] = float(np.quantile(v, 0.9)) if len(v) else np.nan
            if name == "gex_missing_offset":
                r[f"{lab}_firing_rate_recorded"] = float(np.mean(A_offset[pm] > 0))
                r[f"{lab}_firing_rate_prereg_def_null_gex"] = float(np.mean(np.isnan(A_S[pm, DIMS.index('gex_alignment')])))
        return r

    COMP_DESC = pd.DataFrame([comp_desc(*c) for c in COMPONENTS])
    COMP_DESC.round(6).to_csv(RES / "channel3_component_distributions.csv", index=False)

    # greedy cumulative table
    inc = np.diff(np.concatenate([[0.0], point["cum_share"]]))
    boot_inc = np.diff(np.concatenate([np.zeros((len(boot_cum), 1)), boot_cum], axis=1), axis=1) if len(boot_cum) else np.empty((0, len(ORDER)))
    GREEDY = []
    for i, c in enumerate(ORDER):
        clo, chi = pct_ci(boot_cum[:, i]) if len(boot_cum) else (np.nan, np.nan)
        ilo, ihi = pct_ci(boot_inc[:, i]) if len(boot_inc) else (np.nan, np.nan)
        GREEDY.append({"step": i + 1, "component": c, "cumulative_share": point["cum_share"][i], "cum_ci_lo": clo,
                       "cum_ci_hi": chi, "incremental_share": inc[i], "inc_ci_lo": ilo, "inc_ci_hi": ihi,
                       "marginal_share": point["share"][c]})
    GREEDY = pd.DataFrame(GREEDY)
    INTERACTION = float(point["cum_share"][-1] - sum(point["share"][c] for c in COMP_NAMES if np.isfinite(point["share"][c])))

    # month panel (P1 months) and in-sample/sealed cut -- point estimates (NOTES A16/A17)
    MONTH_SH = []
    for mkey, mlab in MONTHS:
        mn = np.flatnonzero((NIGHT_MONTH == mkey) & IS_P1)
        if len(mn) == 0:
            continue
        rm = decompose(P0N, mn, np.random.default_rng(SEED_TIE_POINT), R_TIE)
        for k, v in rm["share"].items():
            MONTH_SH.append({"month": mlab, "n_nights": len(mn), "suppressed": len(mn) < FLOOR_CELL,
                             "S_m": rm["S"], "k_m": rm["k1"], "expected_m": rm["expected_P1_at_P0_rate"],
                             "item": k, "restored_share": v})
    MONTH_SH = pd.DataFrame(MONTH_SH)
    cut0 = np.flatnonzero((nd <= IN_SAMPLE_END).to_numpy()); cut1 = np.flatnonzero((nd > IN_SAMPLE_END).to_numpy())
    rc = decompose(cut0, cut1, np.random.default_rng(SEED_TIE_POINT), R_TIE)
    CUT_SH = pd.DataFrame([{"item": k, "restored_share": v, "S_cut": rc["S"], "n0": rc["n0"], "n1": rc["n1"],
                            "k0": rc["k0"], "k1": rc["k1"], "status": rc["status"].get(k, "ok")} for k, v in rc["share"].items()])

    def stability(item):
        ms = MONTH_SH[(MONTH_SH["item"] == item)]
        holds = ms[(~ms.suppressed) & (ms.S_m > 0) & (ms.restored_share >= HOLD_SHARE)]
        cutv = CUT_SH.loc[CUT_SH["item"] == item, "restored_share"]
        cut_ok = bool(len(cutv) and np.isfinite(cutv.iloc[0]) and rc["S"] > 0 and cutv.iloc[0] >= HOLD_SHARE)
        return {"months_holding": int(len(holds)), "months_holding_list": holds.month.tolist(),
                "month_rule_met": len(holds) >= 2, "cut_share": float(cutv.iloc[0]) if len(cutv) else np.nan,
                "cut_rule_met": cut_ok}

    ALL_ITEMS = TOP_ROWS + C3_ROWS
    for r in ALL_ITEMS:
        r.update(stability(r["item"]))
    # catalyst label for the verdict = weaker of full-P0 and June-only versions (NOTES A18)
    c3 = {r["item"]: r for r in C3_ROWS}
    cat_full, cat_june = c3["catalyst_event_score"]["label"], c3[CAT_JUNE]["label"]
    cat_label_verdict = min((cat_full, cat_june), key=lambda l: LABEL_RANK[l])
    c3["catalyst_event_score"]["label_for_verdict"] = cat_label_verdict
    for r in ALL_ITEMS:
        r.setdefault("label_for_verdict", r["label"])
    pd.DataFrame(ALL_ITEMS).round(6).to_csv(RES / "channels_restored_shares.csv", index=False)
    GREEDY.round(6).to_csv(RES / "channel3_greedy_cumulative.csv", index=False)
    MONTH_SH.round(6).to_csv(RES / "month_panel_restored_shares.csv", index=False)
    CUT_SH.round(6).to_csv(RES / "cut_insample_vs_sealed_restored_shares.csv", index=False)
    pd.DataFrame([{"q": k, "P0": point["q0"][k], "P1": point["q1"][k], "shift_P1_minus_P0": point["qshift"][k],
                   "ci_lo": pct_ci(boot_q[k])[0], "ci_hi": pct_ci(boot_q[k])[1]} for k in point["qshift"]]
                 ).round(6).to_csv(RES / "channel2_score_quantile_shift.csv", index=False)

    # -------- distributional reading per §8 (NOTES A14/A15)
    rows_by = {r["item"]: r for r in ALL_ITEMS}
    nested = [rows_by[c] for c in COMP_NAMES] + [rows_by["channel4_universe_joint"]]
    nested_explains = [r["item"] for r in nested if r["label_for_verdict"] == "EXPLAINS"]
    explains = list(nested_explains)
    if rows_by["channel1_candidate_count"]["label"] == "EXPLAINS":
        explains.insert(0, "channel1_candidate_count")
    if rows_by["channel2_score_distribution"]["label"] == "EXPLAINS" and not nested_explains:
        explains.append("channel2_score_distribution")
    marg_top = max(COMP_NAMES, key=lambda c: (point["share"][c] if np.isfinite(point["share"][c]) else -np.inf))
    greedy_top = GREEDY.loc[GREEDY.incremental_share.idxmax(), "component"]
    recon = sum(rows_by[k]["restored_share"] for k in ("channel1_candidate_count", "channel2_score_distribution")
                if rows_by[k]["label"] in ("EXPLAINS", "CONTRIBUTES"))
    reasons = []
    if len(explains) >= 2:
        dist_verdict = "INCONCLUSIVE"; reasons.append(f"two or more items labelled EXPLAINS: {explains}")
    elif marg_top != greedy_top:
        dist_verdict = "INCONCLUSIVE"; reasons.append(f"marginal top ({marg_top}) != greedy top ({greedy_top})")
    elif recon < 0.5:
        dist_verdict = "INCONCLUSIVE"
        reasons.append(f"CONTRIBUTES/EXPLAINS shares of Ch1+Ch2 reconstruct {recon:.3f} < 0.50 of S: the fall is "
                       "unexplained by the registered channels")
    elif len(explains) == 1:
        st = rows_by[explains[0]]
        if st["month_rule_met"] and st["cut_rule_met"]:
            dist_verdict = "HISTORICALLY_CONFIRMED"; reasons.append(f"cause identified: {explains[0]}")
        else:
            dist_verdict = "INCONCLUSIVE"
            reasons.append(f"{explains[0]} EXPLAINS but is unstable (month rule {st['month_rule_met']}, "
                           f"cut rule {st['cut_rule_met']})")
    else:
        dist_verdict = "INCONCLUSIVE"; reasons.append("no item labelled EXPLAINS")
    DECOMP = {
        "shortfall": {"k0": point["k0"], "n0": point["n0"], "k1": point["k1"], "n1": point["n1"],
                      "expected_P1_at_P0_rate": point["expected_P1_at_P0_rate"], "S": point["S"],
                      "N0_per_night": point["N0_per_night"], "N1_per_night": point["N1_per_night"],
                      "bootstrap_replicates_with_S_le_0": n_S_nonpos},
        "top_level": [{k: r[k] for k in ("item", "restored_share", "ci_lo", "ci_hi", "label", "uninformative",
                                         "months_holding", "cut_share")} for r in TOP_ROWS],
        "channel3_marginal": [{k: r[k] for k in ("item", "restored_share", "ci_lo", "ci_hi", "label", "label_for_verdict",
                                                  "uninformative", "status", "months_holding", "cut_share")} for r in C3_ROWS],
        "channel3_greedy_order": ORDER,
        "channel3_greedy_cumulative_total": float(point["cum_share"][-1]),
        "channel3_interaction_cum_minus_sum_marginals": INTERACTION,
        "marginal_top": marg_top, "greedy_top": greedy_top,
        "explains_items_counted": explains, "reconstruction_ch1_ch2": recon,
        "channel2_quantile_shift": point["qshift"],
        "channel4": {"symbol_turnover_P1_new_vs_P0": TURNOVER, "joint_lost_mass": point["channel4_joint_lost_mass"]},
        "distributional_verdict": dist_verdict, "distributional_reasons": reasons,
    }

# ============================================================================= 10. verdict
if GATE_NULL:
    VERDICT, VREASON = "NULL", "Gate 0: no decline distinguishable from constant-rate noise at p <= 0.05 (trend and rate)"
elif CONFIG_FIRES:
    fired = CFG_CHANGES[CFG_CHANGES.brackets_the_fall].effective_date.tolist()
    VERDICT, VREASON = "HISTORICALLY_CONFIRMED", f"configuration (Channel 3a): config change(s) effective {fired} bracket the fall"
else:
    VERDICT, VREASON = DECOMP["distributional_verdict"], "; ".join(DECOMP["distributional_reasons"])

summary = {
    "question": "Q005", "type": "DIAGNOSTIC decomposition", "quotable": "NON_QUOTABLE",
    "prereg_sha256": sha256_file(PREREG),
    "manifests": {MANIFEST: sha256_file(MANIFEST), MANIFEST_PRICES: sha256_file(MANIFEST_PRICES)},
    "exclusions_sha256": sha256_file(EXCLUSIONS),
    "n_nights": N_NIGHTS,
    "n_nights_excluded": len(EXCL_MANUAL) + len(EXCL_NONSESSION),
    "excluded_nights": {"manual_runs": [ds(d) for d in EXCL_MANUAL], "non_session_runs": [ds(d) for d in EXCL_NONSESSION]},
    "spy_sessions_without_run": [ds(d) for d in SESSIONS_WITHOUT_RUN],
    "n_nights_P0": int(IS_P0.sum()), "n_nights_P1": int(IS_P1.sum()),
    "n_nights_in_sample": int((nd <= IN_SAMPLE_END).sum()), "n_nights_sealed": int((nd > IN_SAMPLE_END).sum()),
    "n_candidate_rows": N_ROWS,
    "floors": {"total_ok": N_NIGHTS >= FLOOR_TOTAL, "P0_ok": int(IS_P0.sum()) >= FLOOR_CELL, "P1_ok": int(IS_P1.sum()) >= FLOOR_CELL,
               "suppressed_cells": PANEL.loc[PANEL.status == "SUPPRESSED", "cell"].tolist()},
    "mean_oos": G0["diff_mean_P1_minus_P0"],
    "mean_oos_definition": "P1 minus P0 mean nightly elite-candidate count (NON_QUOTABLE)",
    "ci": list(DIFF_CI) if DECOMP is not None else None,
    "p_perm": G0["p_gate"],
    "mpe": None,
    "verdict": VERDICT,
    "verdict_reason": VREASON,
    "gate0_elite_candidate": G0,
    "gate0_elite_published_secondary": G0_PUB,
    "gate0_sensitivity_incl_2026-04-03": {k: G0_SENS[k] for k in ("n_nights", "p_trend_perm", "p_rate_perm", "fall_is_real")},
    "bh": {"family": "F2 Calibration", "m_registered_tests": 1, "p_gate": G0["p_gate"], "q_gate": BH_Q_GATE,
           "q_threshold": Q_BH, "within_gate_bh_trend_rate_informational": BH_WITHIN_GATE},
    "published_elite_derivation": PUB_DERIV,
    "channel3a_config": {"segments": SEGMENTS_OUT, "n_changes": len(CFG_CHANGES), "fires": CONFIG_FIRES,
                         "changes": CFG_CHANGES.to_dict("records") if len(CFG_CHANGES) else []},
    "decomposition": DECOMP,
    "regime_pit_nights_by_label": regime_nights,
    "reconstruction_check": RECON,
}
summary = jround(summary)
(RES / "run_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=False))

# ============================================================================= 11. SUMMARY.md (tables, no narrative)
def f(x, nd_=3, pct=False):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{100 * x:.1f}%" if pct else (f"{x:.{nd_}f}" if isinstance(x, (float, np.floating)) else str(x))


L = []
L.append("# Q005 elite_thinning — SUMMARY (generated by eval.py; NON_QUOTABLE)\n")
L.append(f"**Verdict (PREREG §8):** {VERDICT} — {VREASON}\n")
L.append(f"Nights: {N_NIGHTS} (P0 {int(IS_P0.sum())}, P1 {int(IS_P1.sum())}; in-sample {int((nd <= IN_SAMPLE_END).sum())}, "
         f"sealed {int((nd > IN_SAMPLE_END).sum())}); excluded {len(EXCL_MANUAL)} manual-run + {len(EXCL_NONSESSION)} "
         f"non-session; candidate rows {N_ROWS}. Floors: total ≥ {FLOOR_TOTAL} {'met' if N_NIGHTS >= FLOOR_TOTAL else 'NOT met'}; "
         f"cells ≥ {FLOOR_CELL} nights.\n")
L.append("## Gate 0 (elite-candidate, primary)\n")
L.append("| stat | value |\n|---|---|")
for k in ("k0", "n0", "k1", "n1", "rate0_per_night", "rate1_per_night", "rate_ratio_P1_over_P0", "poisson_slope_log_per_30d",
          "rate_ratio_per_30d", "p_trend_perm", "p_trend_wald", "p_trend_quasi", "pearson_dispersion", "diff_mean_P1_minus_P0",
          "p_rate_perm", "p_rate_exact_two_sided", "fall_is_real", "fall_is_real_model_based", "p_gate"):
    L.append(f"| {k} | {f(G0[k], 4) if isinstance(G0[k], float) else G0[k]} |")
L.append(f"| BH q (F2, m=1) | {BH_Q_GATE:.4f} |")
L.append(f"| P1−P0 mean nightly elite-candidate count, 95% CI | {f(G0['diff_mean_P1_minus_P0'])} "
         f"[{f(DIFF_CI[0]) if DECOMP else '—'}, {f(DIFF_CI[1]) if DECOMP else '—'}] |\n")
L.append("Secondary (elite-published): " + ", ".join(f"{k}={f(G0_PUB[k], 4) if isinstance(G0_PUB[k], float) else G0_PUB[k]}"
                                                   for k in ("k0", "k1", "rate0_per_night", "rate1_per_night", "p_trend_perm", "p_rate_perm", "fall_is_real")) + "\n")
L.append("## Month panel (non-excluded nights)\n")
L.append("| cell | nights | candidates | elite-cand | elite-cand/night [95% CI] | elite-pub | DATA_NOTES raw pub | status |\n|---|---|---|---|---|---|---|---|")
for r in PANEL.to_dict("records"):
    rate = "SUPPRESSED" if r["status"] == "SUPPRESSED" else f"{r['elite_cand_per_night']:.3f} [{r['ci_lo']:.3f}, {r['ci_hi']:.3f}]"
    raw = r.get("DATA_NOTES_raw_published_elite_all_runs")
    raw = "" if raw is None or (isinstance(raw, float) and np.isnan(raw)) else int(raw)
    L.append(f"| {r['cell']} | {r['n_nights']} | {r['n_candidates']} | {r['elite_candidate']} | {rate} | {r['elite_published']} | {raw} | {r['status']} |")
L.append("")
L.append("## Channel 3a — configuration\n")
L.append("| effective date | behavioural keys | categories | nights before/after | elite/night before → after | p_perm | local ±20 | brackets |\n|---|---|---|---|---|---|---|---|")
for r in CFG_CHANGES.to_dict("records"):
    L.append(f"| {r['effective_date']} | {r['n_behavioural']} | {r['categories']} | {r['nights_before']}/{r['nights_after']} | "
             f"{r['elite_per_night_before']:.3f} → {r['elite_per_night_after']:.3f} | {r['p_perm_two_sided']:.4f} | "
             f"{r['local20_before']:.3f} → {r['local20_after']:.3f} | {r['brackets_the_fall']} |")
L.append("\nKey-level diffs: results/channel3a_config_diffs.csv\n")
if DECOMP is not None:
    sf = DECOMP["shortfall"]
    L.append("## Shortfall\n")
    L.append(f"P0: {sf['k0']} elite candidates over {sf['n0']} nights; P1: {sf['k1']} over {sf['n1']} nights; expected at P0 rate "
             f"{sf['expected_P1_at_P0_rate']:.2f}; S = {sf['S']:.2f}. Bootstrap replicates with S ≤ 0: {sf['bootstrap_replicates_with_S_le_0']}/{N_BOOT}.\n")
    L.append("## Restored shares (bootstrap 95% CI over nights, 2,000 resamples)\n")
    L.append("| item | restored share | 95% CI | label | label for verdict | P1 months holding ≥20% (non-suppressed only) | in-sample/sealed cut share | status |\n|---|---|---|---|---|---|---|---|")
    for r in ALL_ITEMS:
        ci = "UNINFORMATIVE" if r["uninformative"] else f"[{f(r['ci_lo'], pct=True)}, {f(r['ci_hi'], pct=True)}]"
        L.append(f"| {r['item']} | {f(r['restored_share'], pct=True)} | {ci} | {r['label']} | {r['label_for_verdict']} | "
                 f"{r['months_holding']} {r['months_holding_list']} | {f(r['cut_share'], pct=True)} | {r['status']} |")
    L.append("")
    L.append(f"Greedy order (largest marginal first): {', '.join(DECOMP['channel3_greedy_order'])}. Cumulative total "
             f"{f(DECOMP['channel3_greedy_cumulative_total'], pct=True)}; interaction (cumulative − Σ marginal) "
             f"{f(DECOMP['channel3_interaction_cum_minus_sum_marginals'], pct=True)}. Marginal top: {DECOMP['marginal_top']}; "
             f"greedy top: {DECOMP['greedy_top']}. Full table: results/channel3_greedy_cumulative.csv\n")
    L.append("| score quantile | P0 | P1 | shift |\n|---|---|---|---|")
    for k in point["qshift"]:
        L.append(f"| {k} | {point['q0'][k]:.2f} | {point['q1'][k]:.2f} | {point['qshift'][k]:+.2f} |")
    L.append("")
    L.append(f"Distributional reading (secondary if 3a fires): {DECOMP['distributional_verdict']} — {'; '.join(DECOMP['distributional_reasons'])}\n")
    L.append(f"Channel 4: P1 candidate-nights on symbols never seen in P0: {f(TURNOVER, pct=True)}; industry populated share "
             f"P0 {f(DESC4.industry_populated_share[0], pct=True)} / P1 {f(DESC4.industry_populated_share[1], pct=True)} (populated subset only).\n")
L.append("## Regime (market_regime_daily v1.2, point-in-time nights ≥ 2026-06-09) and SPY tape strata — elite-candidate per night\n")
L.append("| stratifier | period | stratum | nights | mean | 95% CI | status |\n|---|---|---|---|---|---|---|")
for r in STRATA[STRATA.target == "elite_candidate_per_night"].to_dict("records"):
    ci = "" if r["status"] == "SUPPRESSED" else f"[{r['lo']:.3f}, {r['hi']:.3f}]"
    mean = "SUPPRESSED" if r["status"] == "SUPPRESSED" else f"{r['mean']:.3f}"
    L.append(f"| {r['stratifier']} | {r['period']} | {r['stratum']} | {r['n_nights']} | {mean} | {ci} | {r['status']} |")
L.append("")
L.append(f"Reconstruction check: {RECON['rows_reproduced_within_0.01']}/{RECON['rows']} rows reproduced; residual rows on "
         f"{RECON['residual_dates']} (elite among them: {RECON['residual_rows_elite']}); ATR-block rule mismatches "
         f"{RECON['atr_block_rule_vs_recorded_mismatch']}.\n")
L.append("All tables: results/*.csv. Reading choices: results/NOTES.md.\n")
(RES / "SUMMARY.md").write_text("\n".join(L), encoding="utf-8")

print(json.dumps(summary, indent=2))
