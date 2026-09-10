#!/usr/bin/env python3
"""Deterministic pre-checks that run BEFORE the LLM Red Team looks at a result.

Usage: python research/lib/validators.py --question Q001
Exit 0 = all PASS; exit 1 = at least one FAIL (Red Team may not sign off).
Writes results/VALIDATORS.json. Checks are mechanical; no interpretation.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ET_DECISION = "16:05"  # SAS decision time; features must be available before this


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout.strip()


def v1_prereg_locked(qdir):
    f = qdir / "PREREG.md"
    committed = git("ls-files", "--error-unmatch", str(f))
    dirty = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", str(f)]).returncode != 0
    return bool(committed) and not dirty, "PREREG committed and unchanged"


def v2_manifest_verified(qdir):
    # manifest path is parsed from PREREG header line "**Manifest:** research/data/manifest_vNNN.json"
    for line in (qdir / "PREREG.md").read_text().splitlines():
        if line.startswith("**Manifest:**"):
            path = line.split("**Manifest:**")[1].split()[0]
            r = subprocess.run([sys.executable, "research/lib/freeze_dataset.py", "--verify", path])
            return r.returncode == 0, f"manifest {path} checksums"
    return False, "manifest line missing in PREREG"


def v3_no_revised_labels(qdir):
    """Regime label used must be the point-in-time column, never a revised one."""
    code = (qdir / "eval.py").read_text()
    bad = [k for k in ("regime_revised", "regime_final", "regime_latest") if k in code]
    return not bad, f"revised-label columns referenced: {bad}" if bad else "no revised labels referenced"


def v4_knowledge_time(qdir):
    """Every joined table must declare an availability lag in freeze_config; eval may not join undeclared tables."""
    cfg = json.loads(Path("research/lib/freeze_config.json").read_text())
    lags = cfg.get("availability", {})
    code = (qdir / "eval.py").read_text()
    used = [name for name in cfg["tables"] if f'"{name}"' in code or f"'{name}'" in code]
    undeclared = [u for u in used if u not in lags]
    return not undeclared, f"tables without availability declaration: {undeclared}" if undeclared else f"declared for {used}"


def v5_no_duplicate_observations(qdir):
    res = qdir / "results" / "nightly.csv"
    if not res.exists():
        return False, "results/nightly.csv missing (eval must emit one row per night)"
    df = pd.read_csv(res)
    dup = df.duplicated(subset=["trading_date"]).sum()
    return dup == 0, f"{dup} duplicate nights"


def v6_counts_reconcile(qdir):
    """n_nights in SUMMARY.md must equal rows in nightly.csv; no silent drops."""
    res = qdir / "results" / "nightly.csv"
    summ = qdir / "results" / "run_summary.json"
    if not (res.exists() and summ.exists()):
        return False, "nightly.csv or run_summary.json missing"
    n_csv = len(pd.read_csv(res))
    s = json.loads(summ.read_text())
    ok = s.get("n_nights") == n_csv and "n_nights_excluded" in s
    return ok, f"summary n_nights={s.get('n_nights')} csv={n_csv} excluded={s.get('n_nights_excluded')}"


def v7_mc_not_counted_as_n(qdir):
    s = json.loads((qdir / "results" / "run_summary.json").read_text()) if (qdir / "results" / "run_summary.json").exists() else {}
    n = s.get("n_nights", 0)
    return n <= 2000, f"n_nights={n} (a value in the thousands means MC draws were counted as observations)"


def v8_reproducible(qdir):
    """Re-run eval.py and compare the hash of run_summary.json."""
    summ = qdir / "results" / "run_summary.json"
    if not summ.exists():
        return False, "run_summary.json missing"
    before = sha(summ)
    r = subprocess.run([sys.executable, str(qdir / "eval.py")], capture_output=True, text=True)
    if r.returncode != 0:
        return False, f"eval.py failed on re-run: {r.stderr[-300:]}"
    return sha(summ) == before, "byte-identical on re-run" if sha(summ) == before else "output differs on re-run"


def v9_lineage_present(qdir):
    for line in (qdir / "PREREG.md").read_text().splitlines():
        if line.startswith("**Manifest:**"):
            m = json.loads(Path(line.split("**Manifest:**")[1].split()[0]).read_text())
            missing = [k for k in ("code_git_sha", "scoring_versions_present") if k not in m]
            return not missing, f"manifest lineage missing: {missing}" if missing else "lineage present"
    return False, "no manifest"


CHECKS = [v1_prereg_locked, v2_manifest_verified, v3_no_revised_labels, v4_knowledge_time,
          v5_no_duplicate_observations, v6_counts_reconcile, v7_mc_not_counted_as_n, v8_reproducible, v9_lineage_present]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--question", required=True)
    q = ap.parse_args().question
    qdir = next(Path("research/questions").glob(f"{q}_*"), None)
    if not qdir:
        sys.exit(f"no question dir for {q}")
    out, failed = [], 0
    for c in CHECKS:
        try:
            ok, msg = c(qdir)
        except Exception as e:  # a crashing validator is a FAIL, not a skip
            ok, msg = False, f"validator error: {e}"
        out.append({"check": c.__name__, "status": "PASS" if ok else "FAIL", "detail": msg})
        failed += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {c.__name__}: {msg}")
    (qdir / "results").mkdir(exist_ok=True)
    (qdir / "results" / "VALIDATORS.json").write_text(json.dumps(out, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
