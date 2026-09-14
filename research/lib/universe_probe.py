#!/usr/bin/env python3
"""Q030 R2 trigger, limb 2: can Alpaca actually price the base universe?

    python research/lib/universe_probe.py --start 2026-06-01 --end 2026-09-11 --min-bars 60

Counts, for every symbol in the `mapping` key of the pinned sector blob, how many daily bars
Alpaca returns over a trailing window, and reports the share at or above `--min-bars`. The
`research/questions/DEFERRED.md` entry for Q030 gates re-entry on that share reaching 90%.

Reads only market data (rule 1). Writes nothing but the report path given by --out. It is a
measurement, not a freeze: no parquet, no manifest, no sha256 pin. R2(iii) builds the freeze
itself, and only after this probe clears.

The blob is hashed from the platform's **committed** bytes (`git show <sha>:<path>`), never
from the working tree — a Windows checkout rewrites LF to CRLF, so the working-tree file
hashes differently while being the same content.
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import desk_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA_HOST = "https://data.alpaca.markets/v2/stocks/bars"
BLOB_SHA = "c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201"
BLOB_COMMIT = "4171b1a"
BLOB_PATH = "data/sp500_sectors.json"
BATCH = 50


def blob_symbols(codebase: Path):
    """The committed blob's mapping keys, with its sha256 and entry count."""
    raw = subprocess.run(["git", "show", f"{BLOB_COMMIT}:{BLOB_PATH}"], cwd=codebase,
                         capture_output=True, check=True).stdout
    digest = sha256(raw).hexdigest()
    mapping = json.loads(raw).get("mapping") or {}
    return sorted(mapping), digest, len(mapping)


def fetch_counts(symbols, start, end, feed, verbose=True):
    """{symbol: n_daily_bars} over [start, end]. Follows next_page_token."""
    key, sec = os.environ.get("ALPACA_API_KEY"), os.environ.get("ALPACA_SECRET_KEY")
    if not key or not sec:
        sys.exit("not set: ALPACA_API_KEY / ALPACA_SECRET_KEY")
    hdr = {"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": sec}
    counts, errors = {}, []
    for i in range(0, len(symbols), BATCH):
        chunk = symbols[i:i + BATCH]
        token, tries = None, 0
        while True:
            params = {"symbols": ",".join(chunk), "timeframe": "1Day", "start": start,
                      "end": end, "adjustment": "split", "feed": feed, "limit": 10000}
            if token:
                params["page_token"] = token
            req = urllib.request.Request(DATA_HOST + "?" + urllib.parse.urlencode(params), headers=hdr)
            try:
                page = json.load(urllib.request.urlopen(req, timeout=90))
            except Exception as exc:                                  # noqa: BLE001
                tries += 1
                if tries >= 3:
                    errors.append(f"batch {i // BATCH}: {type(exc).__name__} {str(exc)[:80]}")
                    break
                time.sleep(2 * tries)
                continue
            for sym, bars in (page.get("bars") or {}).items():
                counts[sym] = counts.get(sym, 0) + len(bars)
            token = page.get("next_page_token")
            if not token:
                break
        if verbose:
            done = min(i + BATCH, len(symbols))
            print(f"  {done}/{len(symbols)} symbols probed", flush=True)
    return counts, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--min-bars", type=int, default=60)
    ap.add_argument("--gate", type=float, default=90.0, help="pass share, percent")
    ap.add_argument("--feed", default="sip")
    ap.add_argument("--codebase", default=os.environ.get("CODEBASE_DIR", r"C:/Users/sahin/Projects/volatilx"))
    ap.add_argument("--out", default="research/reports/STEWARD_Q030_universe_coverage_probe.md")
    a = ap.parse_args()

    desk_env.load()
    creds = desk_env.present("ALPACA_API_KEY", "ALPACA_SECRET_KEY")
    print("credential presence:", {k: ("present" if v else "MISSING") for k, v in creds.items()})

    symbols, digest, n = blob_symbols(Path(a.codebase))
    print(f"blob {BLOB_COMMIT}:{BLOB_PATH} sha256={digest[:8]}…{digest[-4:]} entries={n} "
          f"pin_match={digest == BLOB_SHA}")
    if digest != BLOB_SHA:
        sys.exit("blob sha256 does not match the pin — stopping (loud failure, per DEFERRED.md)")

    print(f"probing {len(symbols)} symbols, {a.start}..{a.end}, feed={a.feed}")
    counts, errors = fetch_counts(symbols, a.start, a.end, a.feed)

    ok = [s for s in symbols if counts.get(s, 0) >= a.min_bars]
    zero = [s for s in symbols if counts.get(s, 0) == 0]
    short = [s for s in symbols if 0 < counts.get(s, 0) < a.min_bars]
    share = 100.0 * len(ok) / len(symbols)
    maxbars = max(counts.values()) if counts else 0

    lines = [
        f"# STEWARD — Q030 universe coverage probe ({datetime.now(timezone.utc):%Y-%m-%d})",
        "",
        "Limb 2 of the Q030 / H-074 re-entry trigger in `research/questions/DEFERRED.md`: a",
        "trailing-session probe over every symbol in the pinned blob's `mapping` key. Counts only —",
        "no outcome, no freeze, no manifest, no live database query (DP-50(c)).",
        "",
        f"- Blob: `{BLOB_COMMIT}:{BLOB_PATH}`, sha256 `{digest}`, **pin match: {digest == BLOB_SHA}**, entries **{n}**",
        "  (hashed from the committed bytes via `git show`; the Windows working-tree copy is CRLF and hashes differently)",
        f"- Window `{a.start}..{a.end}`, daily bars, `adjustment=split`, `feed={a.feed}`; max bars returned for any symbol: **{maxbars}**",
        f"- Credentials: both present in the desk session (`research/lib/desk_env.py`)",
        "",
        "| measure | value |",
        "|---|---|",
        f"| symbols probed | {len(symbols)} |",
        f"| with ≥ {a.min_bars} daily bars | **{len(ok)}** |",
        f"| share | **{share:.2f}%** |",
        f"| gate | ≥ {a.gate:.0f}% |",
        f"| **limb 2 verdict** | **{'PASS' if share >= a.gate else 'FAIL'}** |",
        f"| zero bars | {len(zero)} |",
        f"| 1..{a.min_bars - 1} bars | {len(short)} |",
        f"| fetch errors | {len(errors)} |",
        "",
    ]
    if zero:
        lines += ["### Symbols returning zero bars", "", "```", ", ".join(zero), "```", ""]
    if short:
        lines += ["### Symbols returning fewer than the floor", "",
                  "```", ", ".join(f"{s}:{counts[s]}" for s in short), "```", ""]
    if errors:
        lines += ["### Fetch errors", "", *[f"- {e}" for e in errors], ""]
    lines += ["Excluded symbols are **counted and named, never back-filled or imputed** "
              "(Q030 DECISIONS.md). A symbol absent here is absent from the freeze R2(iii) builds.", ""]

    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n{len(ok)}/{len(symbols)} = {share:.2f}%  gate {a.gate:.0f}%  -> "
          f"{'PASS' if share >= a.gate else 'FAIL'}")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
