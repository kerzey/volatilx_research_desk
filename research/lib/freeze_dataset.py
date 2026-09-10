#!/usr/bin/env python3
"""Freeze a pinned research dataset from the read-only DB into parquet + SHA-256 manifest.

Usage:
  python research/lib/freeze_dataset.py --as-of 2026-09-05 --version 001 [--config research/lib/freeze_config.json]
  python research/lib/freeze_dataset.py --verify research/data/manifest_v001.json

The config lists {name: sql} pairs. The Data Steward edits the SQL after inspecting
schemas; column names in the default config are best guesses and MUST be checked.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

DATA_DIR = Path("research/data")
DEFAULT_CONFIG = Path("research/lib/freeze_config.json")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def freeze(as_of: str, version: str, config_path: Path) -> None:
    import psycopg  # imported here so --verify works without a DB

    url = os.environ.get("RESEARCH_DB_URL")
    if not url:
        sys.exit("RESEARCH_DB_URL not set (read-only role only)")
    manifest_path = DATA_DIR / f"manifest_v{version}.json"
    if manifest_path.exists():
        sys.exit(f"{manifest_path} exists — never overwrite a manifest; bump the version")
    cfg = json.loads(config_path.read_text())
    entries = []
    with psycopg.connect(url, options="-c default_transaction_read_only=on") as conn:
        for name, sql in cfg["tables"].items():
            q = sql.replace(":as_of", f"'{as_of}'")
            df = pd.read_sql(q, conn)
            out = DATA_DIR / f"v{version}_{name}.parquet"
            df.to_parquet(out, index=False)
            entries.append({
                "name": name, "file": str(out), "rows": int(len(df)),
                "columns": list(df.columns), "sha256": sha256_file(out), "sql": q,
            })
            print(f"{name}: {len(df)} rows -> {out}")
    import subprocess
    code_sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    cb = os.environ.get("CODEBASE_DIR", "")
    platform_sha = subprocess.run(["git", "-C", cb, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip() if cb else ""
    versions = {}
    for e in entries:
        for col in e["columns"]:
            if "version" in col.lower() or col.lower().endswith("_v"):
                versions.setdefault(e["name"], []).append(col)
    manifest = {
        "version": version, "as_of": as_of,
        "code_git_sha": code_sha,
        "platform_git_sha": platform_sha,   # SHA of the VolatilX codebase the data was produced by
        "scoring_versions_present": versions,          # steward: verify these columns exist & summarise distinct values in the freeze report
        "engine_versions_present": cfg.get("engine_versions", {}),
        "availability": cfg.get("availability", {}),
        "universe_membership_note": cfg.get("universe_membership_note", ""),
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "db_role": "research_ro", "tables": entries,
        "in_sample_end": cfg.get("in_sample_end"),  # calendar split, set by registrar policy
        "notes": cfg.get("notes", ""),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"manifest -> {manifest_path}")


def verify(manifest_path: Path) -> None:
    m = json.loads(manifest_path.read_text())
    bad = 0
    for t in m["tables"]:
        p = Path(t["file"])
        ok = p.exists() and sha256_file(p) == t["sha256"]
        print(f"{'OK ' if ok else 'BAD'} {t['name']} {t['rows']} rows")
        bad += 0 if ok else 1
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of")
    ap.add_argument("--version")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--verify")
    a = ap.parse_args()
    if a.verify:
        verify(Path(a.verify))
    else:
        if not (a.as_of and a.version):
            sys.exit("--as-of and --version required")
        freeze(a.as_of, a.version, Path(a.config))
