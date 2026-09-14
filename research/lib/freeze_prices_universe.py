#!/usr/bin/env python3
"""Freeze Alpaca daily bars for an EXPLICIT symbol list (parquet + SHA-256 manifest).

Q030 R2 authorizes this: "The existing tool takes its symbol list from a base manifest
(research/lib/freeze_prices.py); extending it to take an explicit symbol list is a change
under research/ and is not an enforcement file under rule 15." Q030's population is the
market OUTSIDE the candidate pool, so a base-manifest symbol list cannot express it.

Differences from freeze_prices.py: symbols come from the pinned sp500_sectors blob's mapping
(read from COMMITTED bytes via `git show` — a Windows checkout rewrites LF to CRLF and the
working-tree file hashes differently), plus candidates and benchmarks; the date range is
explicit; NO hourly bars ("No hourly bars are required", Q030 R2).

Symbols returning no bars are excluded and counted, never back-filled or imputed.
Market-DATA host only. Never overwrites an existing manifest. Read-only on the platform repo.

  python research/lib/freeze_prices_universe.py --version 001 \
      --start 2025-01-02 --end 2026-09-10 --feed sip
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import desk_env
from freeze_prices import BENCHMARKS, fetch_all, sha256_file  # reuse the sanctioned fetch path

ROOT = Path(__file__).resolve().parents[2]
CODEBASE = Path("C:/Users/sahin/Projects/volatilx")
DATA = ROOT / "research/data"
BLOB_COMMIT, BLOB_PATH = "4171b1a", "data/sp500_sectors.json"
BLOB_SHA = "c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201"


def blob_symbols() -> list:
    """The pinned base universe, hashed from committed bytes (never the working tree)."""
    raw = subprocess.run(["git", "show", f"{BLOB_COMMIT}:{BLOB_PATH}"], cwd=CODEBASE,
                         capture_output=True, check=True).stdout
    got = hashlib.sha256(raw).hexdigest()
    if got != BLOB_SHA:
        sys.exit(f"blob sha mismatch: committed bytes hash {got}, pinned {BLOB_SHA}")
    mapping = json.loads(raw)["mapping"]
    print(f"blob {BLOB_COMMIT}:{BLOB_PATH} verified, mapping = {len(mapping)} entries")
    return sorted(mapping)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--feed", required=True,
                    help="pass 'sip' explicitly; ALPACA_DATA_FEED is malformed (DATA_NOTES 2026-09-14)")
    a = ap.parse_args()

    desk_env.load()
    mp = DATA / f"manifest_prices_universe_v{a.version}.json"
    if mp.exists():
        sys.exit(f"{mp} exists - never overwrite a manifest; bump the version")

    base = blob_symbols()
    cand = pd.read_parquet(DATA / "v001_sas_candidates.parquet", columns=["symbol"])
    cands = sorted(set(cand.symbol.dropna().astype(str)))
    syms = sorted(set(base) | set(cands) | set(BENCHMARKS))
    print(f"{len(base)} base + {len(cands)} candidate + {len(BENCHMARKS)} benchmark "
          f"= {len(syms)} distinct symbols, {a.start}..{a.end}, feed={a.feed}")

    start, end = f"{a.start}T00:00:00Z", f"{a.end}T23:59:59Z"
    frames = {}
    for name, adj in (("daily_raw", "raw"), ("daily_split", "split")):
        df = fetch_all(syms, "1Day", start, end, adj, a.feed, name)
        df["date"] = df["t"].str[:10]
        frames[name] = (df.drop(columns="t")[["symbol", "date", "o", "h", "l", "c", "v", "n", "vw"]]
                        .sort_values(["symbol", "date"]).reset_index(drop=True))

    entries = []
    for name, df in frames.items():
        out = DATA / f"pu{a.version}_{name}.parquet"
        df.to_parquet(out, index=False)
        entries.append({"name": name, "file": str(out.relative_to(ROOT)).replace("\\", "/"),
                        "rows": int(len(df)), "symbols": int(df.symbol.nunique()),
                        "timeframe": "1Day", "adjustment": "split" if name.endswith("split") else "raw",
                        "sha256": sha256_file(out)})
        print(f"  wrote {out.name}: {len(df):,} rows, {df.symbol.nunique():,} symbols")

    got = set(frames["daily_split"].symbol)
    missing = sorted(set(base) - got)
    mp.write_text(json.dumps({
        "version": a.version, "kind": "prices_universe", "as_of": a.end,
        "window": {"start": a.start, "end": a.end}, "feed": a.feed,
        "source": "https://data.alpaca.markets/v2/stocks/bars",
        "base_universe": {"blob": f"{BLOB_COMMIT}:{BLOB_PATH}", "sha256": BLOB_SHA,
                          "mapping_entries": len(base), "returned_bars": len(base) - len(missing),
                          "absent": missing},
        "symbol_counts": {"base": len(base), "candidates": len(cands),
                          "benchmarks": len(BENCHMARKS), "distinct_requested": len(syms)},
        "tables": entries,
    }, indent=2), encoding="utf-8")
    print(f"wrote {mp.relative_to(ROOT)}  ({len(base) - len(missing)}/{len(base)} base symbols returned bars)")


if __name__ == "__main__":
    main()
