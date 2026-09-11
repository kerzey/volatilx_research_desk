#!/usr/bin/env python3
"""Freeze Alpaca price bars for every symbol in a frozen SAS dataset (parquet + SHA-256 manifest).

Usage:
  python research/lib/freeze_prices.py --base research/data/manifest_v001.json --version 001
  python research/lib/freeze_dataset.py --verify research/data/manifest_prices_v001.json

The database holds no OHLC table: the platform pulls daily bars live from Alpaca at grading
time and de-splits them in memory (volatilx scripts/backfill_w60_outcomes.py:154, :185-193).
This freezes the same source so path studies — target touches in both directions, the order
levels are hit in, after-hours and next-day entries, distance-matched controls — run on
pinned prices.

Writes, next to the base manifest:
  p{V}_daily_raw.parquet    every candidate symbol + benchmarks, unadjusted daily OHLCV
  p{V}_daily_split.parquet  same bars, split-adjusted (divide raw by split to get the factor)
  p{V}_hourly_raw.parquet   published-pick symbols, hourly bars INCLUDING pre/post-market
  manifest_prices_v{V}.json same schema as freeze_dataset.py, so its --verify works on it

Split handling: SAS targets are in the signal-date price basis. For a signal on date d, a bar
on date x in that basis is  split_bar(x) * (raw(d) / split(d)). Never compare a raw bar across
a split to a published target.

Knowledge time: a bar dated <= the pick night is feature data for that night; anything later
is outcome data. Hourly bars stamped after ~21:10 UTC on the pick night (SAS finishes around
21:0x UTC per super_agent_select_runs) are the first after-hours prices a subscriber could act on.

Market-DATA host only (data.alpaca.markets). Never overwrites an existing manifest.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

DATA_HOST = "https://data.alpaca.markets/v2/stocks/bars"
BENCHMARKS = ["SPY", "QQQ", "IWM", "SMH", "DIA"]
BATCH = 50
LOOKBACK_DAYS = 60          # calendar days before the first pick: room for ATR / prior-trend features


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(symbols, timeframe, start, end, adjustment, feed):
    k, s = os.environ.get("ALPACA_API_KEY"), os.environ.get("ALPACA_SECRET_KEY")
    if not (k and s):
        sys.exit("ALPACA_API_KEY / ALPACA_SECRET_KEY not set")
    rows, token = [], None
    while True:
        q = {"symbols": ",".join(symbols), "timeframe": timeframe, "start": start, "end": end,
             "adjustment": adjustment, "feed": feed, "limit": 10000}
        if token:
            q["page_token"] = token
        req = urllib.request.Request(f"{DATA_HOST}?{urllib.parse.urlencode(q)}",
                                     headers={"APCA-API-KEY-ID": k, "APCA-API-SECRET-KEY": s})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    d = json.load(r)
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 4:
                    time.sleep(2 ** attempt * 3)
                    continue
                raise
        for sym, bars in (d.get("bars") or {}).items():
            for b in bars:
                rows.append({"symbol": sym, "t": b["t"], "o": b["o"], "h": b["h"], "l": b["l"],
                             "c": b["c"], "v": b["v"], "n": b.get("n"), "vw": b.get("vw")})
        token = d.get("next_page_token")
        if not token:
            return rows
        time.sleep(0.35)   # stay well under the 200 req/min limit


def fetch_all(symbols, timeframe, start, end, adjustment, feed, label):
    out = []
    for i in range(0, len(symbols), BATCH):
        chunk = symbols[i:i + BATCH]
        out += fetch(chunk, timeframe, start, end, adjustment, feed)
        print(f"  {label}: {min(i + BATCH, len(symbols))}/{len(symbols)} symbols, {len(out):,} bars", flush=True)
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="SAS manifest whose candidate symbols to price")
    ap.add_argument("--version", required=True)
    ap.add_argument("--feed", default=os.environ.get("ALPACA_DATA_FEED", "sip"))
    a = ap.parse_args()

    base_path = Path(a.base)
    base = json.loads(base_path.read_text())
    data_dir = base_path.parent
    manifest_path = data_dir / f"manifest_prices_v{a.version}.json"
    if manifest_path.exists():
        sys.exit(f"{manifest_path} exists — never overwrite a manifest; bump the version")

    cand_entry = next(t for t in base["tables"] if t["name"] == "sas_candidates")
    cand = pd.read_parquet(cand_entry["file"], columns=["trading_date", "symbol", "qualification_reason"])
    all_syms = sorted(set(cand.symbol.dropna().astype(str)) | set(BENCHMARKS))
    pub_syms = sorted(set(cand.loc[cand.qualification_reason.isin(["selected", "selected_dark"]), "symbol"].astype(str)) | {"SPY", "QQQ"})
    first = pd.to_datetime(cand.trading_date).min().date()
    start = (first - timedelta(days=LOOKBACK_DAYS)).isoformat() + "T00:00:00Z"
    end = f"{base['as_of']}T23:59:59Z"
    print(f"base {base_path.name} as_of {base['as_of']}: {len(all_syms)} symbols, {len(pub_syms)} published; {start[:10]} .. {base['as_of']}")

    frames = {
        "daily_raw": fetch_all(all_syms, "1Day", start, end, "raw", a.feed, "daily raw"),
        "daily_split": fetch_all(all_syms, "1Day", start, end, "split", a.feed, "daily split"),
        "hourly_raw": fetch_all(pub_syms, "1Hour", start, end, "raw", a.feed, "hourly raw"),
    }
    for name in ("daily_raw", "daily_split"):
        df = frames[name]
        df["date"] = df["t"].str[:10]
        frames[name] = df.drop(columns="t")[["symbol", "date", "o", "h", "l", "c", "v", "n", "vw"]] \
            .sort_values(["symbol", "date"]).reset_index(drop=True)
    frames["hourly_raw"] = frames["hourly_raw"].sort_values(["symbol", "t"]).reset_index(drop=True)

    entries = []
    for name, df in frames.items():
        out = data_dir / f"p{a.version}_{name}.parquet"
        df.to_parquet(out, index=False)
        tf = "1Hour" if name.startswith("hourly") else "1Day"
        adj = "split" if name.endswith("split") else "raw"
        syms = pub_syms if name.startswith("hourly") else all_syms
        entries.append({"name": f"prices_{name}", "file": str(out).replace("\\", "/"), "rows": int(len(df)),
                        "columns": list(df.columns), "sha256": sha256_file(out),
                        "sql": f"alpaca {DATA_HOST} timeframe={tf} adjustment={adj} feed={a.feed} "
                               f"start={start} end={end} symbols={len(syms)}"})
        print(f"{name}: {len(df):,} rows, {df.symbol.nunique()} symbols -> {out}")

    missing = sorted(set(all_syms) - set(frames["daily_raw"].symbol))
    code_sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    manifest = {
        "version": f"prices_{a.version}", "as_of": base["as_of"],
        "base_manifest": str(base_path).replace("\\", "/"), "base_manifest_sha256": sha256_file(base_path),
        "code_git_sha": code_sha, "platform_git_sha": base.get("platform_git_sha", ""),
        "source": f"Alpaca market data API, feed={a.feed}", "frozen_at": datetime.now(timezone.utc).isoformat(),
        "tables": entries, "symbols_requested": len(all_syms), "symbols_without_bars": missing,
        "in_sample_end": base.get("in_sample_end"),
        "availability": {
            "prices_daily_raw": {"note": "bar dated <= pick night = feature; later bars = outcome"},
            "prices_daily_split": {"note": "split-adjusted twin of daily_raw; raw/split on a date = cumulative split factor"},
            "prices_hourly_raw": {"note": "UTC stamps, includes pre/post-market; SAS publishes ~21:0x UTC on the pick night"},
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"manifest -> {manifest_path}  ({len(missing)} symbols returned no bars: {missing[:15]})")


if __name__ == "__main__":
    main()
