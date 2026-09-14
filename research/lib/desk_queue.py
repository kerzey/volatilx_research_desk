#!/usr/bin/env python3
"""Deterministic work queue for the autonomous desk.

    python research/lib/desk_queue.py            # human-readable
    python research/lib/desk_queue.py --json     # machine-readable (the /desk-run skill reads this)
    python research/lib/desk_queue.py --max-register 3

Reads (never writes): every question's state.json and schedule.json (falling back to the
PREREG's own "Decision date" line), BACKLOG.md, questions/DEFERRED.md, INBOX.md,
PLATFORM_ISSUES.md, ENHANCEMENTS.md, TRADE_IDEAS.md, and each DECISIONS.md (for decisions the
desk defaulted on Haci's behalf). It answers one question: what is the next piece of work, and
whose is it — the desk's, or Haci's. /desk-run works through the output top to bottom; the
board (board.py) renders the same data for Haci.

schedule.json (written by the Registrar at `apply`, or by /desk-run at lock) — all optional:
  {"decision_date": "2026-10-12", "extension_date": "2026-11-23", "hard_stop": "2027-06-30",
   "rule": "fixed" | "exposure-driven" | "immediate", "extended": false, "note": "..."}
"""
import io
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QDIR = ROOT / "research/questions"

# Registration order (DP-47): Haci's INBOX items first, then this list (EXPLORE_001's ranking,
# Haci-style F7 first, testable-soonest first), then remaining BACKLOG order. A hypothesis marked
# "new data needed" is registered straight into DEFERRED.md with the data named.
# 2026-09-14: Haci's Master Hypothesis Program (H-069..H-084, BACKLOG F8 and the F1/F2/F6 entries
# that cite it) goes to the front as his own items. H-069 (point-in-time integrity) leads because
# its FAIL branch stops everything else; H-070 is DP-51 bookkeeping; then the cheap all-candidate
# diagnostics (H-073 IC, H-076 structure) that H-075 / H-082 / H-083 / H-084 build on; H-074 needs
# the Steward's universe price freeze first; H-077 is a synthesis after verdicts; H-078 defers.
PRIORITY = ["H-069", "H-070", "H-073", "H-076", "H-075", "H-074", "H-082", "H-079", "H-080",
            "H-081", "H-084", "H-083", "H-077", "H-078",
            "H-058", "H-053", "H-066", "H-064", "H-062", "H-040", "H-060", "H-059", "H-061",
            "H-051", "H-050", "H-033", "H-041", "H-034", "H-013", "H-011", "H-010", "H-012",
            "H-014", "H-002", "H-003", "H-020", "H-021", "H-022"]

RUN_STEPS = {           # state -> what the desk does next
    "IDEA": "registrar draft / decision-maker decide",
    "PREREG_DRAFT": "decision-maker decide → registrar apply → commit → lock (--by desk)",
    "PREREG_LOCKED": "data-steward: advance DATASET_PINNED",
    "DATASET_PINNED": "wait for decision date, then steward freeze-for → researcher run",
    "EVALUATED": "python research/lib/controller.py advance QNNN VALIDATED",
    "VALIDATED": "red-team review QNNN",
    "REDTEAM_SIGNED": "reporter write QNNN",
    "LEDGERED": "board; HISTORICALLY_CONFIRMED waits for Haci (HUMAN_APPROVED)",
    "HUMAN_APPROVED": "brief-writer QNNN",
    "BRIEF_WRITTEN": "Haci runs the brief in the platform repo",
    "IMPLEMENTED_FLAG_OFF": "steward shadow grading (≥ 30 nights)",
    "SHADOW_VALIDATED": "Haci: RELEASE_APPROVED",
}
TERMINAL = {"NULL", "INCONCLUSIVE", "REJECTED", "DEFERRED"}
STATUS_RE = re.compile(r"^(OPEN|PROPOSED|READY|IDEA|UNDER_TEST\S*|HISTORICAL\S*|PROSPECTIVE\S*|KILLED|HACI_DECIDED:\S+|"
                       r"BRIEF_WRITTEN|IMPLEMENTED:\S+|VERIFIED|FAILED\S*|ACCEPTED|DROPPED)$")
FLOW_RE = re.compile(r"^(HACI_DECIDED:\S+|BRIEF_WRITTEN|IMPLEMENTED:\S+|VERIFIED|FAILED\S*|ACCEPTED|DROPPED)$")
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _first_date(text: str):
    m = DATE_RE.search(text)
    return m.group(1) if m else None


def schedule_for(d: Path) -> dict:
    sj = d / "schedule.json"
    if sj.exists():
        s = json.loads(_read(sj))
        s.setdefault("source", "schedule.json")
        return s
    prereg = _read(d / "PREREG.md")
    s = {"decision_date": None, "extension_date": None, "hard_stop": None, "rule": "fixed",
         "extended": False, "source": "PREREG.md (parsed; write schedule.json to pin)"}
    for line in prereg.splitlines():
        low = line.lower()
        if "decision date" in low and s["decision_date"] is None:
            s["decision_date"] = _first_date(line.split("ecision date", 1)[1])
        if "hard stop" in low and s["hard_stop"] is None:
            s["hard_stop"] = _first_date(line.split("ard stop", 1)[1])
        if "exposure-driven" in low and "decision date" in low:
            s["rule"] = "exposure-driven"
    if s["decision_date"] is None and s["hard_stop"]:
        s["rule"] = "exposure-driven"
    return s


def question_rows() -> list:
    rows = []
    for d in sorted(QDIR.glob("Q*_*")):
        st = json.loads(_read(d / "state.json")) if (d / "state.json").exists() else {}
        first = _read(d / "PREREG.md").splitlines()[:1]
        title = first[0].lstrip("# ").strip() if first else d.name
        hyps = re.findall(r"\bH-\d{3}\b", " ".join(_read(d / "PREREG.md").splitlines()[:12]))
        decisions = _read(d / "DECISIONS.md")
        # prefer the plain-English list the decision-maker writes; fall back to the table rows
        sect = decisions.split("## Defaulted on Haci's behalf", 1)
        defaulted = [l.strip()[2:] for l in sect[1].split("\n## ", 1)[0].splitlines() if l.strip().startswith("- ")] if len(sect) > 1 else []
        if not defaulted:
            defaulted = [l.strip() for l in decisions.splitlines() if "DEFAULTED" in l and l.strip().startswith("|")]
        rows.append({
            "id": d.name.split("_", 1)[0], "dir": d.name, "title": title,
            "state": st.get("state", "(no state.json)"),
            "historical_verdict": st.get("historical_verdict", ""),
            "prospective_verdict": st.get("prospective_verdict", ""),
            "last_by": (st.get("history") or [{}])[-1].get("by", ""),
            "last_at": str((st.get("history") or [{}])[-1].get("at", ""))[:10],
            "hypotheses": sorted(set(hyps)),
            "schedule": schedule_for(d),
            "defaulted_decisions": defaulted,
            "prereg_committed": bool(st.get("prereg_commit")),
        })
    return rows


def backlog() -> dict:
    txt = _read(ROOT / "research/BACKLOG.md")
    open_, done = [], []
    for line in txt.splitlines():
        m = re.match(r"^- \[( |x)\] (H-\d{3})\b(.*)$", line)
        if not m:
            continue
        entry = {"id": m.group(2), "text": (m.group(2) + m.group(3)).strip()[:160],
                 "new_data": "new data needed" in line.lower()}
        (done if m.group(1) == "x" else open_).append(entry)
    deferred = sorted(set(re.findall(r"^## (H-\d{3})", _read(QDIR / "DEFERRED.md"), re.M)))
    return {"open": open_, "registered": done, "deferred": deferred}


def inbox() -> list:
    return [l[6:].strip() for l in _read(ROOT / "research/INBOX.md").splitlines() if l.startswith("- [ ] ")]


def list_rows(name: str) -> list:
    """Rows of the first markdown table in research/<name>.md whose first cell is an ID."""
    out = []
    for line in _read(ROOT / f"research/{name}").splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not re.match(r"^(PI|EN|TI)-\d{3}$", cells[0]):
            continue
        status = next((c for c in cells[1:] if STATUS_RE.match(c)), "")
        flow = next((c for c in cells[1:] if FLOW_RE.match(c)), "")
        out.append({"id": cells[0], "status": status, "flow": flow, "cells": cells, "text": cells[-1][:140]})
    return out


def build_queue(today: date = None, max_register: int = 2) -> dict:
    today = today or date.today()
    qs = question_rows()
    bl = backlog()
    reg_ids = {h for q in qs for h in q["hypotheses"] if q["state"] not in ("REJECTED",)}
    stale = [e for e in bl["open"] if e["id"] in reg_ids]          # open in BACKLOG, but a PREREG names it
    stale_ids = {e["id"] for e in stale}
    candidates = [e for e in bl["open"] if e["id"] not in stale_ids and e["id"] not in bl["deferred"]]
    order = {h: i for i, h in enumerate(PRIORITY)}
    candidates.sort(key=lambda e: (order.get(e["id"], 999), e["id"]))

    due, in_flight, runs, drafts, needs_pin, for_haci, desk_todo, ready_for_prompt = [], [], [], [], [], [], [], []
    for q in qs:
        s, sch = q["state"], q["schedule"]
        dd = sch.get("extension_date") if sch.get("extended") else sch.get("decision_date")
        # a PREREG_LOCKED question whose freeze can only exist at its decision date (Q010 pattern)
        # is in flight, not waiting for a pin
        if s == "DATASET_PINNED" or (s == "PREREG_LOCKED" and sch.get("pin_at_decision")):
            if sch.get("rule") == "immediate" or (dd and dd <= today.isoformat()):
                due.append({**q, "due_on": dd or "now"})
            elif sch.get("rule") == "exposure-driven" and sch.get("hard_stop"):
                in_flight.append({**q, "due_on": f"{sch.get('check_from') or '?'} (exposure check; hard stop {sch['hard_stop']})"})
            else:
                in_flight.append({**q, "due_on": dd or "unknown — write schedule.json"})
        elif s == "PREREG_LOCKED":
            needs_pin.append(q)
        elif s in ("IDEA", "PREREG_DRAFT"):
            drafts.append(q)
        elif s in ("EVALUATED", "VALIDATED", "REDTEAM_SIGNED"):
            runs.append({**q, "next": RUN_STEPS[s]})
        elif s == "LEDGERED" and q["historical_verdict"] == "HISTORICALLY_CONFIRMED":
            for_haci.append({"id": q["id"], "what": "approve for implementation (or leave it on the edges list)",
                             "type": f"python research/lib/controller.py advance {q['id']} HUMAN_APPROVED --by haci"})
        elif s == "HUMAN_APPROVED":
            desk_todo.append({"id": q["id"], "what": "brief-writer: IMPLEMENTATION_BRIEF.md"})
        elif s == "BRIEF_WRITTEN":
            for_haci.append({"id": q["id"], "what": f"run research/questions/{q['dir']}/IMPLEMENTATION_BRIEF.md in the platform repo, flag OFF",
                             "type": f"python research/lib/controller.py advance {q['id']} IMPLEMENTED_FLAG_OFF --by haci --note \"PR <link> sha <before> <after>\""})
        elif s == "IMPLEMENTED_FLAG_OFF":
            desk_todo.append({"id": q["id"], "what": "steward: shadow grading nightly; SHADOW.json after ≥ 30 nights"})
        elif s == "SHADOW_VALIDATED":
            for_haci.append({"id": q["id"], "what": "flip the flag on",
                             "type": f"python research/lib/controller.py advance {q['id']} RELEASE_APPROVED --by haci"})
    in_flight.sort(key=lambda q: q["due_on"])

    lists = {}
    for fname, key in (("PLATFORM_ISSUES.md", "issues"), ("ENHANCEMENTS.md", "enhancements"), ("TRADE_IDEAS.md", "trade_ideas")):
        rows = list_rows(fname)
        lists[key] = rows
        for r in rows:
            st = r["flow"] or r["status"]
            if st.startswith("HACI_DECIDED:fix") or st.startswith("HACI_DECIDED:build"):
                ready_for_prompt.append({"id": r["id"], "what": r["text"][:90], "type": f"/desk-run prompt {r['id']}"})
            elif st == "BRIEF_WRITTEN":
                for_haci.append({"id": r["id"], "what": "run the brief in the platform repo, then tell the desk the SHA",
                                 "type": f"/desk-run verify {r['id']} <sha>"})
            elif st.startswith("IMPLEMENTED:"):
                desk_todo.append({"id": r["id"], "what": f"steward verify {r['id']} {st.split(':',1)[1]}"})
            elif st.startswith("FAILED"):
                for_haci.append({"id": r["id"], "what": "verification failed — see research/reports/VERIFY_*.md", "type": "fix and re-run /desk-run verify"})

    defaulted = [{"id": q["id"], "line": l} for q in qs for l in q["defaulted_decisions"]]
    return {
        "today": today.isoformat(),
        "due": due, "runs_in_progress": runs, "needs_pin": needs_pin, "drafts": drafts,
        "in_flight": in_flight,
        "to_register": candidates[:max_register], "to_register_total": len(candidates),
        "stale_backlog": stale, "backlog": {"open": len(bl["open"]), "registered": len(bl["registered"]), "deferred": bl["deferred"]},
        "inbox": inbox(),
        "for_haci": for_haci, "desk_todo": desk_todo, "ready_for_prompt": ready_for_prompt,
        "defaulted_decisions": defaulted,
        "lists": {k: [{"id": r["id"], "status": r["status"], "flow": r["flow"], "text": r["text"]} for r in v] for k, v in lists.items()},
        "questions": [{k: q[k] for k in ("id", "dir", "title", "state", "historical_verdict", "prospective_verdict", "schedule")} for q in qs],
    }


def print_text(q: dict) -> None:
    print(f"=== desk queue — {q['today']} ===\n")
    print("DESK WORK, in order")
    n = 0
    for s in q["inbox"]:
        n += 1; print(f"  {n}. INBOX → backlog entry: {s[:110]}")
    for e in q["stale_backlog"]:
        n += 1; print(f"  {n}. BACKLOG bookkeeping: mark {e['id']} registered (a PREREG names it)")
    for x in q["runs_in_progress"]:
        n += 1; print(f"  {n}. {x['id']} {x['state']} → {x['next']}")
    for x in q["due"]:
        n += 1; print(f"  {n}. DUE {x['id']} ({x['due_on']}): steward freeze-for → researcher run → validate → red-team → reporter")
    for x in q["needs_pin"]:
        n += 1; print(f"  {n}. {x['id']} PREREG_LOCKED → steward advance DATASET_PINNED")
    for x in q["drafts"]:
        n += 1; print(f"  {n}. {x['id']} {x['state']} → finish registration (decide → apply → commit → lock --by desk → pin)")
    for x in q["desk_todo"]:
        n += 1; print(f"  {n}. {x['id']}: {x['what']}")
    for e in q["to_register"]:
        n += 1; tag = " [new data needed → DEFERRED.md]" if e["new_data"] else ""
        print(f"  {n}. REGISTER {e['id']}{tag}: {e['text'][:100]}")
    if q["to_register_total"] > len(q["to_register"]):
        print(f"     … {q['to_register_total'] - len(q['to_register'])} more open hypotheses after these")
    if n == 0:
        print("  nothing — the desk is waiting on calendar dates")

    print("\nWAITING ON HACI")
    for x in q["for_haci"] or [{"id": "—", "what": "nothing", "type": ""}]:
        print(f"  {x['id']}: {x['what']}" + (f"\n      → {x['type']}" if x.get("type") else ""))

    if q["ready_for_prompt"]:
        print("\nREADY WHEN HACI ASKS (decided; no brief yet)")
        for x in q["ready_for_prompt"]:
            print(f"  {x['id']}: {x['what']}  ->  {x['type']}")

    print("\nIN FLIGHT (locked; no interim looks)")
    for x in q["in_flight"]:
        print(f"  {x['id']:<5} {x['state']:<15} due {x['due_on']}")

    if q["defaulted_decisions"]:
        print("\nDECISIONS THE DESK MADE FOR HACI (review on the board; overturn = successor question)")
        for x in q["defaulted_decisions"]:
            print(f"  {x['id']}: {x['line'][:130]}")
    print(f"\nBACKLOG open={q['backlog']['open']} registered={q['backlog']['registered']} deferred={','.join(q['backlog']['deferred']) or '—'}")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    mr = int(args[args.index("--max-register") + 1]) if "--max-register" in args else 2
    q = build_queue(max_register=mr)
    if "--json" in args:
        print(json.dumps(q, indent=2, ensure_ascii=False))
    else:
        print_text(q)
