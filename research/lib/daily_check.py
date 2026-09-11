#!/usr/bin/env python3
"""Deterministic daily operational check of the VolatilX nightly pipeline.

Usage:
  python research/lib/daily_check.py                  # most recent trading date
  python research/lib/daily_check.py --date 2026-09-10

Prints a markdown report to stdout. RED lines come first (breakage — these are what the
routine posts to Discord), then AMBER lines (drift — report only), then either the RED
list or a single `ALL CLEAR (n AMBER)` line, then the full metric table.

Flag rules (Haci, 2026-09-10):
  1. Minimum normal movement. tolerance = max(2 x MAD, floor), where the floor is
     1 for counts, 2 percentage points for rates and 2 points for scores. A metric that
     sat perfectly still for 20 nights (MAD = 0) can no longer trip on a one-unit change.
  2. Seen before = not unusual. A value inside the trailing 20-night [min, max] is OK.
  3. Two severities. RED = breakage (stale tables, missing rows, null spikes, zero
     published, published rows inconsistent, W60 grading backlog). AMBER = drift (score
     distribution, direction / timeframe / source mix, pick counts).
Absolute checks (freshness, zero published, consistency, maturation) have no baseline and
ignore rules 1-2.

Live read-only queries are permitted here: CLAUDE.md rule 4 allows live tables for daily
operational checks. The session is opened read-only regardless of the role's grants.
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from statistics import median

import psycopg

BASELINE_NIGHTS = 20
FLOOR = {"count": 1.0, "rate": 2.0, "score": 2.0}   # rates are in percentage points

ROW_TABLES = [
    "super_agent_select_runs",
    "super_agent_select_candidates_daily",
    "projection_pick_bullish_daily",
    "uoa_symbol_daily",
    "gex_symbol_daily",
    "market_regime_daily",
]
FRESHNESS_TABLES = ROW_TABLES
LAYERS = {
    "projection": "projection_score",
    "technical": "technical_structure_score",
    "flow": "flow_strength_score",
    "catalyst": "catalyst_event_score",
    "fundamental": "fundamental_quality_score",
    "smart_money": "smart_money_confirmation_score",
    "gex": "gex_alignment_score",
}


# --- helpers ------------------------------------------------------------------------------
def connect():
    url = os.environ.get("RESEARCH_DB_URL") or sys.exit("RESEARCH_DB_URL not set")
    return psycopg.connect(url, options="-c default_transaction_read_only=on")


def rows(conn, sql, params=()):
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def et_now():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/New_York"))
    except Exception:
        return datetime.now(timezone(timedelta(hours=-4)))


def expected_trading_date():
    """Last completed US trading session. SPY's latest daily bar from the Alpaca market-DATA
    host is holiday-aware; if that fails, fall back to the last weekday (holiday-blind)."""
    k, s = os.environ.get("ALPACA_API_KEY"), os.environ.get("ALPACA_SECRET_KEY")
    if k and s:
        try:
            start = (et_now().date() - timedelta(days=10)).isoformat()
            url = ("https://data.alpaca.markets/v2/stocks/bars?symbols=SPY&timeframe=1Day"
                   f"&start={start}&feed={os.environ.get('ALPACA_DATA_FEED', 'sip')}&adjustment=raw")
            req = urllib.request.Request(url, headers={"APCA-API-KEY-ID": k, "APCA-API-SECRET-KEY": s})
            with urllib.request.urlopen(req, timeout=15) as r:
                bars = json.load(r).get("bars", {}).get("SPY", [])
            if bars:
                return date.fromisoformat(bars[-1]["t"][:10]), "SPY daily bars (Alpaca)"
        except Exception:
            pass
    n = et_now()
    d = n.date() if n.hour * 60 + n.minute >= 16 * 60 + 30 else n.date() - timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d, "last weekday (holiday-blind fallback)"


def judge(today, base, kind, breakage_side=None):
    """Return (level, median, tolerance, lo, hi). breakage_side: 'up' / 'down' / None.
    A move in the breakage direction is RED, the other direction AMBER; None = always AMBER."""
    base = [b for b in base if b is not None]
    if today is None or len(base) < 5:
        return "N/A", None, None, None, None
    med = median(base)
    mad = median([abs(b - med) for b in base])
    tol = max(2 * mad, FLOOR[kind])
    lo, hi = min(base), max(base)
    if abs(today - med) <= tol or lo <= today <= hi:
        return "OK", med, tol, lo, hi
    if breakage_side is None:
        return "AMBER", med, tol, lo, hi
    moved_up = today > med
    if (breakage_side == "up") == moved_up:
        return "RED", med, tol, lo, hi
    return "AMBER", med, tol, lo, hi


def engines(src_json):
    try:
        src = json.loads(src_json) if isinstance(src_json, str) else (src_json or [])
    except Exception:
        return set()
    out = set()
    for s in src:
        s = str(s)
        if s.startswith("projection"):
            out.add("projection")
        elif s.startswith("uoa"):
            out.add("uoa")
        elif s.startswith("whale"):
            out.add("whale")
    return out


def fmt(v, kind):
    if v is None:
        return "-"
    if kind == "rate":
        return f"{v:.1f}%"
    if kind == "score":
        return f"{v:.2f}"
    return f"{v:g}"


# --- main ---------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="trading date to check (default: latest in super_agent_select_runs)")
    a = ap.parse_args()
    # Reports are redirected to .md files; force UTF-8 so Windows doesn't write cp1252.
    sys.stdout.reconfigure(encoding="utf-8")

    conn = connect()
    dates = [r[0] for r in rows(conn, "SELECT DISTINCT trading_date FROM super_agent_select_runs "
                                      "WHERE trading_date <= COALESCE(%s::date, CURRENT_DATE) "
                                      "ORDER BY trading_date DESC LIMIT 70", (a.date,))]
    if not dates:
        sys.exit("no rows in super_agent_select_runs")
    today = dates[0]
    base_dates = dates[1:1 + BASELINE_NIGHTS]
    window = [today] + base_dates

    red, amber, table = [], [], []

    def record(level, name, today_v, kind, med, tol, lo, hi, note=""):
        line = (f"{name}: today {fmt(today_v, kind)} vs 20d median {fmt(med, kind)} "
                f"(tolerance ±{fmt(tol, kind)}; 20d range {fmt(lo, kind)}–{fmt(hi, kind)})")
        if note:
            line += f" — {note}"
        if level == "RED":
            red.append(line)
        elif level == "AMBER":
            amber.append(line)
        table.append((level, name, fmt(today_v, kind), fmt(med, kind), fmt(tol, kind)))

    def absolute(level, name, detail):
        (red if level == "RED" else amber).append(f"{name}: {detail}")
        table.append((level, name, detail, "-", "-"))

    # 1. Freshness (absolute) --------------------------------------------------------------
    # A --date run is a backtest: judge it as of that date, not against today's calendar.
    expected, exp_src = (today, "--date given; calendar check skipped") if a.date else expected_trading_date()
    if today < expected:
        absolute("RED", "super_agent_select_runs freshness",
                 f"latest run {today} but last trading session was {expected} ({exp_src})")
    for t in FRESHNESS_TABLES:
        mx = rows(conn, f"SELECT max(trading_date) FROM {t}")[0][0]
        if mx is None or mx < today:
            absolute("RED", f"{t} freshness", f"max(trading_date) = {mx}, expected {today}")
        else:
            table.append(("OK", f"{t} freshness", str(mx), "-", "-"))

    # 2. Row counts: a drop is breakage (RED), a rise is drift (AMBER) --------------------
    for t in ROW_TABLES:
        counts = dict(rows(conn, f"SELECT trading_date, count(*) FROM {t} "
                                 f"WHERE trading_date = ANY(%s) GROUP BY 1", (window,)))
        tv = counts.get(today, 0)
        bv = [counts.get(d, 0) for d in base_dates]
        lvl, med, tol, lo, hi = judge(tv, bv, "count", breakage_side="down")
        record(lvl, f"{t} row count", tv, "count", med, tol, lo, hi)

    # 3-7. Candidate-level metrics -----------------------------------------------------------
    layer_cols = ", ".join(LAYERS.values())
    cand = rows(conn, f"""
        SELECT trading_date, overall_score, completeness_score, qualified, qualification_reason,
               selected_rank, dominant_direction, best_timeframe, source_membership_json,
               public_payload_json IS NOT NULL, {layer_cols}
        FROM super_agent_select_candidates_daily WHERE trading_date = ANY(%s)""", (window,))
    by_date = {d: [] for d in window}
    for r in cand:
        by_date[r[0]].append(r)

    def per_date(fn):
        return {d: (fn(by_date[d]) if by_date[d] else None) for d in window}

    def pct(n, d):
        return 100.0 * n / d if d else None

    pub = lambda rs: [r for r in rs if r[4] == "selected"]

    metrics = [
        # (name, fn, kind, breakage_side)  breakage_side None -> AMBER only
        ("SAS qualified count", lambda rs: sum(1 for r in rs if r[3]), "count", None),
        ("SAS published count", lambda rs: len(pub(rs)), "count", None),
        ("published bearish count", lambda rs: sum(1 for r in pub(rs) if r[6] == "bearish"), "count", None),
        ("published short-timeframe count", lambda rs: sum(1 for r in pub(rs) if r[7] == "short"), "count", None),
        ("published swing-timeframe count", lambda rs: sum(1 for r in pub(rs) if r[7] == "swing"), "count", None),
        ("published long-timeframe count", lambda rs: sum(1 for r in pub(rs) if r[7] == "long"), "count", None),
        ("published projection-only count", lambda rs: sum(1 for r in pub(rs) if engines(r[8]) == {"projection"}), "count", None),
        ("published uoa-only count", lambda rs: sum(1 for r in pub(rs) if engines(r[8]) == {"uoa"}), "count", None),
        ("published whale-only count", lambda rs: sum(1 for r in pub(rs) if engines(r[8]) == {"whale"}), "count", None),
        ("published multi-engine count", lambda rs: sum(1 for r in pub(rs) if len(engines(r[8])) >= 2), "count", None),
        ("published score>=90 count", lambda rs: sum(1 for r in pub(rs) if (r[1] or 0) >= 90), "count", None),
        ("candidate median overall_score", lambda rs: median([r[1] for r in rs if r[1] is not None]) if any(r[1] is not None for r in rs) else None, "score", None),
        ("candidate share score>=90", lambda rs: pct(sum(1 for r in rs if (r[1] or 0) >= 90), len(rs)), "rate", None),
        ("candidate share completeness<60", lambda rs: pct(sum(1 for r in rs if (r[2] or 0) < 60), len(rs)), "rate", None),
    ]
    for i, (label, col) in enumerate(LAYERS.items()):
        idx = 10 + i
        metrics.append((f"{col} null rate", (lambda j: lambda rs: pct(sum(1 for r in rs if r[j] is None), len(rs)))(idx), "rate", "up"))

    for name, fn, kind, side in metrics:
        vals = per_date(fn)
        tv = vals[today]
        bv = [vals[d] for d in base_dates]
        lvl, med, tol, lo, hi = judge(tv, bv, kind, breakage_side=side)
        # A null rate that FELL is good news, not drift.
        if side == "up" and lvl == "AMBER":
            lvl = "OK"
        note = ""
        if name.startswith("gex_alignment_score") and lvl == "RED":
            note = "GEX-null spike; triggers the +5 completeness offset in scoring"
        record(lvl, name, tv, kind, med, tol, lo, hi, note)

    # Absolute: zero published is breakage
    n_pub = len(pub(by_date[today]))
    if n_pub == 0:
        absolute("RED", "SAS published count", "0 picks published today")

    # 8. Published consistency (absolute) --------------------------------------------------
    bad = [r for r in pub(by_date[today])
           if r[5] is None or not r[9] or r[6] not in ("bullish", "bearish") or not r[3]]
    if bad:
        absolute("RED", "published-vs-audit consistency",
                 f"{len(bad)} published row(s) missing selected_rank / public_payload_json / "
                 f"called direction, or not flagged qualified")
    else:
        table.append(("OK", "published-vs-audit consistency", f"{n_pub} rows consistent", "-", "-"))

    # 9. W60 maturation backlog (absolute) -------------------------------------------------
    if len(dates) > 61:
        cutoff = dates[61]   # window of a pick on dates[61] closed on dates[1] = yesterday
        backlog = rows(conn, """SELECT count(*) FROM super_agent_select_candidates_daily
                                WHERE qualification_reason = 'selected' AND trading_date <= %s
                                AND outcome_sealed_w60 IS NOT TRUE""", (cutoff,))[0][0]
        if backlog:
            absolute("RED", "W60 maturation backlog",
                     f"{backlog} published pick(s) dated <= {cutoff} still unsealed")
        else:
            table.append(("OK", "W60 maturation backlog", f"0 unsealed <= {cutoff}", "-", "-"))

    # 10. Correction ledger (informational) ------------------------------------------------
    corr = rows(conn, """SELECT count(*) FROM outcome_correction_ledger
                         WHERE correction_date::date = %s OR created_at::date = %s""", (today, today))[0][0]
    if corr:
        absolute("AMBER", "outcome_correction_ledger", f"{corr} correction row(s) written today")
    else:
        table.append(("OK", "outcome_correction_ledger", "0 rows today", "-", "-"))

    conn.close()

    # --- report ------------------------------------------------------------------------------
    out = []
    out += [f"RED — {x}" for x in red]
    out += [f"AMBER — {x}" for x in amber]
    if not red:
        out.append(f"ALL CLEAR ({len(amber)} AMBER)")
    out.append("")
    out.append(f"# Daily Check — {today}")
    out.append("")
    out.append(f"Baseline: {len(base_dates)} trading nights, {base_dates[-1]} .. {base_dates[0]}. "
               f"Last trading session: {expected} ({exp_src}).")
    out.append("Rules: tolerance = max(2×MAD, floor) with floors 1 (counts), 2pp (rates), 2 pts (scores); "
               "a value inside the 20-night range is OK; RED = breakage, AMBER = drift.")
    out.append("")
    out.append("| status | metric | today | 20d median | tolerance |")
    out.append("|---|---|---|---|---|")
    order = {"RED": 0, "AMBER": 1, "N/A": 2, "OK": 3}
    for lvl, name, tv, med, tol in sorted(table, key=lambda x: order.get(x[0], 9)):
        out.append(f"| {lvl} | {name} | {tv} | {med} | {tol} |")
    print("\n".join(out))


if __name__ == "__main__":
    main()
