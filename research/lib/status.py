#!/usr/bin/env python3
"""One-screen view of the research desk. Usage: python research/lib/status.py [--full]"""
import json, re, sys
from datetime import date
from pathlib import Path

full = "--full" in sys.argv
Q = Path("research/questions")
print(f"=== VolatilX Research Desk — {date.today()} ===\n")

print("QUESTIONS")
for d in sorted(Q.glob("Q*_*")):
    st = json.loads((d / "state.json").read_text()) if (d / "state.json").exists() else {"state": "(no state.json)", "history": []}
    hv = st.get("historical_verdict", ""); pv = st.get("prospective_verdict", "")
    last = st["history"][-1] if st.get("history") else {}
    print(f"  {d.name:<32} {st['state']:<22} {hv:<24} {pv:<24} last: {str(last.get('at',''))[:10]} by {last.get('by','')}")
    if full:
        for f in ("results/SUMMARY.md", "results/REDTEAM.md", "REPORT.md"):
            p = d / f
            if p.exists():
                head = [l for l in p.read_text().splitlines() if l.strip()][:3]
                print(f"      {f}: " + " | ".join(h[:90] for h in head))

bl = Path("research/BACKLOG.md")
if bl.exists():
    txt = bl.read_text()
    open_ = len(re.findall(r"^- \[ \]", txt, re.M)); done = len(re.findall(r"^- \[x\]", txt, re.M))
    fams = re.findall(r"^## (F\d+ — .+)$", txt, re.M)
    print(f"\nBACKLOG  open={open_} registered={done} families={len(fams)}")
    if full:
        for line in txt.splitlines():
            if line.startswith("- [ ]"): print("   " + line[6:120])

rep = Path("research/reports/daily")
if rep.exists():
    files = sorted(rep.glob("*.md"))
    if files:
        latest = files[-1]; body = latest.read_text()
        reds = [l for l in body.splitlines() if l.startswith("RED")]
        print(f"\nDAILY CHECK  latest={latest.stem}  RED={len(reds)}")
        for r in reds[:10]: print("   " + r[:120])
        if not reds and "ALL CLEAR" in body: print("   ALL CLEAR")

led = Path("research/LEDGER.md")
if led.exists():
    rows = [l for l in led.read_text().splitlines() if l.startswith("| Q")]
    print(f"\nLEDGER  rows={len(rows)}")
    for r in rows[-5:]: print("   " + r[:140])

log = Path("research/reports/hook_audit.log")
if log.exists():
    lines = log.read_text().splitlines()
    blocks = [json.loads(l) for l in lines if '"BLOCK"' in l]
    print(f"\nGUARDS  commands={len(lines)} blocked={len(blocks)}")
    for b in blocks[-5:]: print(f"   BLOCK [{b.get('agent','')}] {b['reason'][:70]} :: {b['cmd'][:60]}")
