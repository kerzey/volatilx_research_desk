#!/usr/bin/env python3
"""Sixth maintenance pass — makes the desk autonomous.

    python docs/admin_pass/patch6.py --check    # show what would change, write nothing
    python docs/admin_pass/patch6.py --apply    # write (Haci; .claude/, CLAUDE.md, scripts/ and the
                                                 #        controller are enforcement/human files)

1. .claude/skills/desk-run/SKILL.md      <- docs/admin_pass/desk-run.SKILL.md   (the orchestrator)
2. .claude/agents/decision-maker.md      <- docs/admin_pass/decision-maker.md   (autonomous mode)
3. .claude/agents/registrar.md           += "Autonomous drafting" (merge / DEFERRED / schedule.json)
4. .claude/agents/data-steward.md        += "Successor freeze protocol" and "Verification protocol"
5. .claude/agents/brief-writer.md        += "Enhancement and trade-idea briefs" (EN-/TI-, INTERNAL_TOOL)
6. .claude/agents/reporter.md            += "After the verdict: the lists"
7. .claude/agents/explorer.md            += one line: enhancement ideas go to ENHANCEMENTS.md
8. CLAUDE.md                             += "Autonomous mode" section (who decides; rules unchanged)
9. scripts/research_routines.sh          <- docs/admin_pass/research_routines.sh (adds the `desk` mode;
                                            the old file is kept as scripts/research_routines.sh.bak)
10. research/lib/controller.py           prereg_manifests(): when a locked PREREG header names no
                                            manifest *file* (successor freezes built at the decision
                                            date — Q010), read <qdir>/manifests.json written by the
                                            Data Steward. Checksums are still verified. Nothing else
                                            in the controller changes; PREREG_LOCKED was never
                                            --by-haci-only in code, so no change is needed for DP-46.

Everything is idempotent: re-running reports "already patched".
"""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = lambda rel: ROOT / rel  # noqa: E731

SKILL_SRC, SKILL_DST = P("docs/admin_pass/desk-run.SKILL.md"), P(".claude/skills/desk-run/SKILL.md")
DM_SRC, DM_DST = P("docs/admin_pass/decision-maker.md"), P(".claude/agents/decision-maker.md")
RT_SRC, RT_DST = P("docs/admin_pass/research_routines.sh"), P("scripts/research_routines.sh")
CONTROLLER = P("research/lib/controller.py")
CLAUDE_MD = P("CLAUDE.md")

REGISTRAR_TAIL = '''
## Autonomous drafting (the default under /desk-run — DP-40..48)

When the caller says the run is autonomous: (1) if a locked PREREG already tests the hypothesis,
do not draft — mark it `merged into QNNN` in BACKLOG.md (DP-29) and reply MERGED; (2) if it needs
data the desk does not hold (options history, a column that is 12% populated), or a new rule-14
exception (DP-41), write the `research/questions/DEFERRED.md` entry with the blocker named, mark
BACKLOG `[x] H-NNN — DEFERRED`, and reply DEFERRED; (3) otherwise draft as usual. The Recommendation
line of every open decision is what the Decision-maker will apply (DP-40), so recommend the option
that keeps the test honest, never the one that reaches a date sooner. In `apply QNNN`, also write
`research/questions/QNNN_slug/schedule.json` from DECISIONS.md "## Schedule":
`{"decision_date": "YYYY-MM-DD", "extension_date": "YYYY-MM-DD" | null, "hard_stop": "YYYY-MM-DD" | null,
"rule": "fixed" | "exposure-driven", "extended": false, "note": "<one line: which §5 rule>"}`.
End with "ready to lock" — the coordinator commits and locks (DP-46); Haci reviews on the board.
'''

STEWARD_TAIL = '''
## Successor freeze protocol (`freeze-for QNNN`)

At a question's decision date (desk_queue.py lists it as DUE). Read its PREREG §5 for the freezes
it names: a selections manifest with the same SQL and a new `as_of`, and a price freeze with the same
Alpaca queries, the symbol list extended to **every candidate on the new nights, published and
unpublished**, hourly bars for published symbols, `end` = the decision date (DP-23). Build them as
the next free version numbers — never overwrite — verify, write `research/reports/FREEZE_vNNN.md`,
and then print the **contributing-night counts per arm and per primary endpoint exactly as §5
defines them**: counts only, no outcomes, no touch rates. If a count is below the PREREG's floor,
say which §5 rule fires (the DP-13 extension, or DEFERRED); the coordinator applies it. If the
PREREG header names no manifest *file* (the freezes could only exist now), write
`research/questions/QNNN_slug/manifests.json` — a JSON list of the manifest paths you built — so
the controller can pin them. You do not advance the controller in this protocol.

## Verification protocol (`verify <PI|EN|TI>-NNN <sha>`)

Haci says an implementation landed. Read the brief (`research/briefs/<id>_*.md`, or the question's
IMPLEMENTATION_BRIEF.md) and run its "before/after check" exactly as written — read-only: the live
tables through `$RESEARCH_DB_URL`, or the platform repo at `<sha>` through `git -C $CODEBASE_DIR
show / log / diff`. Write `research/reports/VERIFY_<id>.md`: what the brief promised, what you
observed, then one line `PASS` or `FAIL: <reason>`. Set the register row (`PLATFORM_ISSUES.md`
Status, or the Build / Tool column of `ENHANCEMENTS.md` / `TRADE_IDEAS.md`) to `VERIFIED` or
`FAILED:<reason>`. Never say a fix landed because the code changed; say it because the data or the
dry-run output changed the way the brief said it would.
'''

BRIEF_TAIL = '''
## Enhancement and trade-idea briefs (`brief EN-NNN` / `brief TI-NNN`)

Precondition: the Build column of the row in `research/ENHANCEMENTS.md` (or the Tool column in
`research/TRADE_IDEAS.md`) reads `HACI_DECIDED:build`. Read the row and its detail block.
- **plumbing** → `research/briefs/EN-NNN_slug.md` in the fix-brief format (sections 1–7), with
  "Symptom" replaced by "What is missing, and the evidence".
- **behaviour, gate met** (the gating question is HUMAN_APPROVED) → write that question's finding
  brief instead and say so.
- **behaviour, gate not met** → an **INTERNAL_TOOL** brief: first line
  `INTERNAL_TOOL — flag-off, visible to Haci only, no subscriber-facing copy or number; gate: QNNN
  (<decision date>)`, then the same sections, plus an acceptance criterion that the subscriber
  payload is byte-identical before and after (the inertness proof, rule 11). A trade idea (TI) is
  always built this way until its evidence reads PROSPECTIVE.
Every brief ends with the exact before/after check the Data Steward will run at
`/desk-run verify <id> <sha>`. Then set the row to `BRIEF_WRITTEN` with the brief's path.
'''

REPORTER_TAIL = '''
## After the verdict: the lists

Update every row in `research/TRADE_IDEAS.md` and `research/ENHANCEMENTS.md` that names QNNN:
evidence `HISTORICAL` (HISTORICALLY_CONFIRMED — name the playbook file in the row), `KILLED` (NULL),
or leave `UNDER_TEST:QNNN` and append "INCONCLUSIVE <date>: <the one-line reason>" to the row text.
An enhancement whose gate was QNNN reads `PROPOSED (gate met)` or `PROPOSED (gate failed: NULL)`.
Then run `python research/lib/board.py`.
'''

EXPLORER_TAIL = '''
Enhancement ideas — things the platform could do that it does not — go to `research/ENHANCEMENTS.md`
as a table row (`| EN-NNN | plumbing|behaviour | PROPOSED | <gate H-/Q- or —> | — | <text> |`), not to
the BACKLOG. A defect goes to `research/PLATFORM_ISSUES.md`.
'''

CLAUDE_TAIL = '''
## Autonomous mode (2026-09-13)

`/desk-run` works the queue in `research/lib/desk_queue.py` without asking Haci: it registers and
locks questions (`--by desk`, DP-46), settles the decisions once reserved for him by
`research/DECISION_POLICY.md` DP-40..48 and lists them on `research/BOARD.md`, runs each question
once on its decision date, and writes briefs on request. His moments are: read the board;
`/desk-run prompt <id>` (asking is the decision); implement in the platform repo;
`/desk-run verify <id> <sha>`; and the three controller steps that stay `--by haci`
(HUMAN_APPROVED, IMPLEMENTED_FLAG_OFF, RELEASE_APPROVED). Ideas go in `research/INBOX.md`.
Nothing above changes: rules 1–15 bind the autonomous desk exactly as before.
'''

CTRL_OLD = '''    pat = re.compile(r"^\\*\\*Manifest[^*]*:\\*\\*\\s*(\\S+)")
    return [m.group(1) for line in (d / "PREREG.md").read_text(encoding="utf-8").splitlines()
            if (m := pat.match(line))]
'''
CTRL_NEW = '''    pat = re.compile(r"^\\*\\*Manifest[^*]*:\\*\\*\\s*(\\S+)")
    paths = [m.group(1) for line in (d / "PREREG.md").read_text(encoding="utf-8").splitlines()
             if (m := pat.match(line))]
    # patch6: a locked PREREG whose header names no manifest *file* (its freezes are built at the
    # decision date — Q010) lists them in <qdir>/manifests.json, written by the Data Steward.
    # Only when none of the header paths exists; a misspelled header path still fails loudly.
    if paths and not any(Path(p).exists() for p in paths):
        mj = d / "manifests.json"
        if mj.exists():
            return json.loads(mj.read_text(encoding="utf-8"))
    return paths
'''


def _read(p):
    raw = p.read_bytes().decode("utf-8")
    return raw.replace("\r\n", "\n"), "\r\n" in raw


def _write(p, text, crlf):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def plan_copy(src, dst, label):
    if not src.exists():
        sys.exit(f"missing {src}")
    text, _ = _read(src)
    same = dst.exists() and _read(dst)[0] == text
    print(f"{label}: {'already installed' if same else ('update' if dst.exists() else 'install')} -> {dst.relative_to(ROOT)}")
    return None if same else text


def plan_append(path, marker, tail, label):
    src, crlf = _read(path)
    if marker in src:
        print(f"{label}: already patched")
        return None, crlf
    print(f"{label}: append section")
    return src.rstrip("\n") + "\n" + tail, crlf


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    skill = plan_copy(SKILL_SRC, SKILL_DST, "desk-run skill")
    dm = plan_copy(DM_SRC, DM_DST, "decision-maker agent")
    if dm is not None and not dm.startswith("---\nname: decision-maker\n"):
        sys.exit("decision-maker.md: frontmatter not as expected; stopping")
    rt = plan_copy(RT_SRC, RT_DST, "research_routines.sh (desk mode)")

    appends = []
    for rel, marker, tail, label in (
        (".claude/agents/registrar.md", "## Autonomous drafting", REGISTRAR_TAIL, "registrar"),
        (".claude/agents/data-steward.md", "## Successor freeze protocol", STEWARD_TAIL, "data-steward"),
        (".claude/agents/brief-writer.md", "## Enhancement and trade-idea briefs", BRIEF_TAIL, "brief-writer"),
        (".claude/agents/reporter.md", "## After the verdict: the lists", REPORTER_TAIL, "reporter"),
        (".claude/agents/explorer.md", "Enhancement ideas — things the platform could do", EXPLORER_TAIL, "explorer"),
        ("CLAUDE.md", "## Autonomous mode (2026-09-13)", CLAUDE_TAIL, "CLAUDE.md"),
    ):
        new, crlf = plan_append(P(rel), marker, tail, label)
        appends.append((P(rel), new, crlf))

    ctrl_src, ctrl_crlf = _read(CONTROLLER)
    if CTRL_NEW in ctrl_src:
        print("controller manifests.json fallback: already patched"); ctrl_new = None
    elif CTRL_OLD not in ctrl_src:
        sys.exit("controller.py: prereg_manifests() text not as expected — file changed since the patch was written; stopping")
    else:
        print("controller manifests.json fallback: patch prereg_manifests()"); ctrl_new = ctrl_src.replace(CTRL_OLD, CTRL_NEW, 1)

    if not a.apply:
        print("\n--check only: nothing written"); return

    if skill is not None: _write(SKILL_DST, skill, False)
    if dm is not None: _write(DM_DST, dm, _read(DM_DST)[1] if DM_DST.exists() else False)
    if rt is not None:
        if RT_DST.exists(): shutil.copyfile(RT_DST, RT_DST.with_suffix(".sh.bak"))
        _write(RT_DST, rt, False)
    for path, new, crlf in appends:
        if new is not None: _write(path, new, crlf)
    if ctrl_new is not None:
        shutil.copyfile(CONTROLLER, CONTROLLER.with_suffix(".py.bak"))
        _write(CONTROLLER, ctrl_new, ctrl_crlf)
    print("\nwritten. Next: register the scheduled task (docs/AUTONOMOUS_DESK.md §Schedule), then `/desk-run` once by hand.")


if __name__ == "__main__":
    main()
