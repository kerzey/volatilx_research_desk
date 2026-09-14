#!/usr/bin/env python3
"""Render research/BOARD.md — the one page Haci reads. Usage: python research/lib/board.py

Deterministic: everything on the board is derived from files the agents already maintain
(state.json, schedule.json, LEDGER.md, playbook/, PLATFORM_ISSUES.md, ENHANCEMENTS.md,
TRADE_IDEAS.md, BACKLOG.md, DECISIONS.md). Nothing is written by hand into the board itself;
edit the source file and re-run. /desk-run regenerates it at the end of every cycle, and the
nightly `desk` routine regenerates it even when nothing else ran.
"""
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from desk_queue import ROOT, QDIR, build_queue, _read  # noqa: E402

OUT = ROOT / "research/BOARD.md"


def ledger_rows() -> list:
    rows = []
    for line in _read(ROOT / "research/LEDGER.md").splitlines():
        if line.startswith("| Q"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 12 and re.match(r"^Q\d{3}$", c[0]):
                rows.append({"id": c[0], "slug": c[1], "verdict": c[4], "prospective": c[5], "n": c[6],
                             "metric": c[7], "p": c[8], "date": c[11]})
    return rows


def playbook_rules() -> list:
    out = []
    for p in sorted((ROOT / "playbook").glob("PB-*.md")):
        lines = [l for l in _read(p).splitlines() if l.strip()]
        title = lines[0].lstrip("# ").strip() if lines else p.stem
        status = next((l for l in lines if l.startswith("Status:")), "")
        out.append({"file": p.name, "title": title, "status": status})
    return out


def table(rows, cols):
    if not rows:
        return "_none yet_\n"
    head = "| " + " | ".join(c for c, _ in cols) + " |\n|" + "---|" * len(cols) + "\n"
    body = "".join("| " + " | ".join(str(f(r)) for _, f in cols) + " |\n" for r in rows)
    return head + body


def main() -> None:
    q = build_queue(max_register=5)
    titles = {x["id"]: x["title"] for x in q["questions"]}
    by_id = {x["id"]: x for x in q["questions"]}
    L = []
    L.append("# Research desk — board\n")
    L.append(f"_Generated {q['today']} by `research/lib/board.py`. Do not edit; edit the source files and re-run. "
             "Ask the desk for anything on this page in plain words, or use the commands shown._\n")

    # 1. Waiting on you
    L.append("## 1. Waiting on you\n")
    if q["for_haci"]:
        for x in q["for_haci"]:
            L.append(f"- **{x['id']}** — {x['what']}" + (f"  \n  `{x['type']}`" if x.get("type") else ""))
    else:
        L.append("- nothing. The desk has no item that only you can move.")
    L.append("")
    if q["ready_for_prompt"]:
        L.append("**Ready when you ask** (you already decided these; the desk writes the prompt on request):\n")
        for x in q["ready_for_prompt"]:
            L.append(f"- **{x['id']}** — {x['what']}  →  `{x['type']}`")
        L.append("")
    L.append("How you act on the lists below: **`/desk-run prompt <ID>`** writes the implementation prompt for an "
             "issue (PI), enhancement (EN) or trade idea (TI) — asking for it *is* your decision. Run the prompt "
             "in the platform repo with Codex or Claude, then **`/desk-run verify <ID> <sha>`** and the desk checks "
             "the result. Research findings (Q) still need `HUMAN_APPROVED --by haci` before a brief, because "
             "the controller enforces it. New idea: **`/desk-run idea \"…\"`** or a line in `research/INBOX.md`.\n")

    # 2. Results
    L.append("## 2. Results (verdicts on record)\n")
    led = ledger_rows()
    L.append(table(led, [("Q", lambda r: r["id"]), ("question", lambda r: titles.get(r["id"], r["slug"]).split(": ", 1)[-1][:110]),
                         ("verdict", lambda r: r["verdict"]), ("the number", lambda r: r["metric"][:90]),
                         ("nights", lambda r: r["n"]), ("date", lambda r: r["date"])]))

    # 3. Edges
    L.append("## 3. Edges\n")
    L.append("**Proven (historical or prospective):**\n")
    conf = [r for r in led if "CONFIRMED" in r["verdict"] or "CONFIRMED" in r["prospective"]]
    pb = playbook_rules()
    if not conf and not pb:
        L.append("_none yet — every question so far is NULL, INCONCLUSIVE, or still waiting for its decision date._\n")
    else:
        for r in conf:
            L.append(f"- **{r['id']}** {titles.get(r['id'], r['slug'])[:110]} — {r['verdict']}" + (f" / {r['prospective']}" if r['prospective'] not in ('', '—', 'N/A') else ""))
        for p in pb:
            L.append(f"- playbook `{p['file']}` — {p['title'][:100]} — {p['status']}")
        L.append("")
    L.append("**Candidate edges under test (locked; the desk looks once, on the date):**\n")
    inflight = q["in_flight"] + q["needs_pin"] + q["drafts"]
    L.append(table(sorted(inflight, key=lambda x: str(x.get("due_on", "z"))),
                   [("Q", lambda r: r["id"]), ("question", lambda r: r["title"].split(": ", 1)[-1][:120]),
                    ("state", lambda r: r["state"]), ("decides on", lambda r: r.get("due_on", "—"))]))

    # 4. Platform issues
    L.append("## 4. Platform issues\n")
    L.append("_Source: `research/PLATFORM_ISSUES.md`. Statuses: OPEN → HACI_DECIDED:fix/research/accept → BRIEF_WRITTEN → IMPLEMENTED:<sha> → VERIFIED._\n")
    L.append(table(q["lists"]["issues"], [("ID", lambda r: r["id"]), ("status", lambda r: r["status"] or "OPEN"), ("issue", lambda r: r["text"])]))

    # 5. Enhancements
    L.append("## 5. Enhancements to build in the platform\n")
    L.append("_Source: `research/ENHANCEMENTS.md`. `plumbing` items can be built now; `behaviour` items wait for their question's verdict "
             "(rule 10/11) unless built as a flag-off internal tool._\n")
    L.append(table(q["lists"]["enhancements"], [("ID", lambda r: r["id"]), ("status", lambda r: r["status"] or "PROPOSED"), ("build", lambda r: r["flow"] or "—"), ("enhancement", lambda r: r["text"])]))

    # 6. Trade ideas
    L.append("## 6. Trade ideas (yours; never subscriber-facing until prospective)\n")
    L.append("_Source: `research/TRADE_IDEAS.md`._\n")
    L.append(table(q["lists"]["trade_ideas"], [("ID", lambda r: r["id"]), ("evidence", lambda r: r["status"] or "IDEA"), ("tool in platform", lambda r: r["flow"] or "—"), ("idea", lambda r: r["text"])]))

    # 7. Decisions the desk made
    L.append("## 7. Decisions the desk made for you (autonomous mode)\n")
    if q["defaulted_decisions"]:
        L.append("_Each was a question the desk would once have asked you. It took the recommended or the stricter option (DP-40..45). "
                 "The locked question stands; to overturn one, say so and the desk registers a successor question._\n")
        for x in q["defaulted_decisions"]:
            L.append(f"- **{x['id']}** {x['line'][:320]}")
        L.append("")
    else:
        L.append("_none yet_\n")

    # 8. Backlog & calendar
    L.append("## 8. Backlog and calendar\n")
    b = q["backlog"]
    L.append(f"- Open hypotheses: **{b['open']}** · registered: {b['registered']} · deferred (data missing): {', '.join(b['deferred']) or '—'}")
    if q["inbox"]:
        L.append(f"- Inbox items waiting: {len(q['inbox'])}")
    nxt = ", ".join(e["id"] for e in q["to_register"]) or "—"
    L.append(f"- Next to register (DP-47 order): {nxt}")
    if q.get("resumable"):
        L.append(f"- **Deferrals lifted, resuming at the front of the queue:** "
                 f"{', '.join(x['id'] for x in q['resumable'])} — the blocker was measured away, "
                 f"so each resumes at `@registrar apply` with its DECISIONS.md binding in full and "
                 f"its schedule re-derived from the actual lock date, out only (DP-43, DP-45)")
    L.append("")
    cal = [(str(x.get("due_on"))[:10], x["id"]) for x in q["in_flight"] if x.get("due_on") and re.match(r"\d{4}", str(x["due_on"]))]
    if cal:
        L.append("| decides on | Q |\n|---|---|")
        for d, i in sorted(cal):
            L.append(f"| {d} | {i} |")
        L.append("")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
