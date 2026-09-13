#!/usr/bin/env python3
"""Fifth maintenance pass — installs the Decision-maker agent and teaches the Registrar about it.

    python docs/admin_pass/patch5.py --check    # show what would change, write nothing
    python docs/admin_pass/patch5.py --apply    # write (Haci; .claude/ and CLAUDE.md are enforcement/human files)

1. .claude/agents/decision-maker.md  <- copied from docs/admin_pass/decision-maker.md
2. .claude/agents/registrar.md
   - reads research/DECISION_POLICY.md before drafting and cites DP ids instead of asking;
   - writes "Open decisions before lock" in a fixed format the Decision-maker can work from;
   - new mode `apply QNNN`: folds DECISIONS.md back into an uncommitted draft;
   - gets Edit (for BACKLOG merge marks and the apply mode);
   - two stale lines brought in line with CLAUDE.md rules 5 and 6 (objective = price path;
     floors = 20 nights per cell / 80 nights total, not "n >= 100").
3. CLAUDE.md — decision-maker added to the agent list.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENT_SRC = ROOT / "docs/admin_pass/decision-maker.md"
AGENT_DST = ROOT / ".claude/agents/decision-maker.md"
REGISTRAR = ROOT / ".claude/agents/registrar.md"
CLAUDE_MD = ROOT / "CLAUDE.md"

REG_OLD_DESC = ("description: Drafts pre-registration documents (PREREG.md) for research questions before any "
                "sealed data is examined. Use when turning a backlog idea or a new hypothesis into a runnable, "
                "locked question. Does not run analyses.")
REG_NEW_DESC = ("description: Drafts pre-registration documents (PREREG.md) for research questions before any "
                "sealed data is examined. Use when turning a backlog idea or a new hypothesis into a runnable, "
                "locked question (`draft H-NNN`), and to fold the Decision-maker's DECISIONS.md back into a "
                "draft (`apply QNNN`). Does not run analyses.")
REG_OLD_TOOLS = "tools: Read, Grep, Glob, Write\n"
REG_NEW_TOOLS = "tools: Read, Grep, Glob, Write, Edit\n"

REG_OLD_OBJECTIVE = ("- Objective metric: direction-adjusted realized return under a named exit rule.\n"
                     "  Touch-hit and MFE may be reported but never decide the verdict.\n")
REG_NEW_OBJECTIVE = ("- Objective metric (rule 5): the price path from a stated entry basis — first touch of\n"
                     "  the named ladder target(s) within the lane window, against a distance-matched control.\n"
                     "  Fixed-horizon return may be reported but never decides the verdict.\n")
REG_OLD_FLOOR = ("- Sample floor per cell (n ≥ 20) and total floor (n ≥ 100); expected n from the\n"
                 "  Steward's coverage report. If expected n is below the floor, say so and mark the\n"
                 "  question DEFERRED rather than registering it.\n")
REG_NEW_FLOOR = ("- Sample floors in trading nights (rule 6): 20 contributing nights per cell, 80 per\n"
                 "  primary endpoint; expected n from the Steward's coverage report. If expected n is\n"
                 "  below the floor, say so and mark the question DEFERRED rather than registering it.\n")
REG_OLD_PUSHBACK = ("Push back on Haci when a question is unanswerable with the available n, when the\n"
                    "baseline is missing, or when the metric is excursion rather than realized return.\n")
REG_NEW_PUSHBACK = ("Push back on Haci when a question is unanswerable with the available n, when the\n"
                    "baseline is missing, or when the metric is a fixed-horizon return instead of the path.\n")

REG_TAIL = '''
## Standing decisions come first

Before drafting, read `research/DECISION_POLICY.md`. Every choice a `DP` entry settles — MPE for a
touch-rate endpoint, the exclusions file, successor-freeze scope, the floor reading, tie rules,
units, family — is applied in the draft with the id cited inline ("MPE +5.0 pp (DP-20)"). It is
not listed as an open decision. Only what the policy does not cover goes to the last section,
in this fixed format, at most one line per option:

```
## Open decisions before lock

1. **<decision in one line>** — Options: A <…> / B <…>. Recommendation: A, because <one line>.
   Changes: §<n>, §<m>.
```

Write them so that someone can answer without reading the draft. Do not address Haci in the
draft body ("Haci to confirm"); the Decision-maker (`@decision-maker decide QNNN`) resolves the
list and asks him only what is his.

## `apply QNNN`

Read `research/questions/QNNN_slug/DECISIONS.md`. The question must still be in `PREREG_DRAFT`
and its PREREG.md uncommitted — a committed draft is locked and you stop. For every DECIDED item
and every answered question, rewrite the affected sections so the document is internally
consistent (an MPE lives in §8 *and* in the decision rules; an arm definition in §2 *and* §4).
Replace the "Open decisions before lock" section with:

```
## Decisions before lock
Recorded in DECISIONS.md (<date>). Routed items still open: <list or none>.
```

and add `**Decisions:** DECISIONS.md` to the header. Apply BACKLOG merge marks the decisions call
for. Then say what changed, section by section, and that the draft is ready for Haci to commit.
'''

CLAUDE_OLD = "data-steward · registrar · explorer · researcher · red-team · brief-writer · reporter.\n"
CLAUDE_NEW = "data-steward · registrar · decision-maker · explorer · researcher · red-team · brief-writer · reporter.\n"


def _read(p):
    raw = p.read_bytes().decode("utf-8")
    return raw.replace("\r\n", "\n"), "\r\n" in raw


def _write(p, text, crlf):
    p.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def _swap(src, old, new, label):
    if new in src:
        return src, f"{label}: already patched"
    if old not in src:
        sys.exit(f"{label}: expected text not found — file changed since the patch was written; stopping")
    return src.replace(old, new, 1), f"{label}: patched"


def patch_registrar(src):
    notes = []
    for old, new, label in ((REG_OLD_DESC, REG_NEW_DESC, "description"),
                            (REG_OLD_TOOLS, REG_NEW_TOOLS, "tools"),
                            (REG_OLD_OBJECTIVE, REG_NEW_OBJECTIVE, "objective (rule 5)"),
                            (REG_OLD_FLOOR, REG_NEW_FLOOR, "floors (rule 6)"),
                            (REG_OLD_PUSHBACK, REG_NEW_PUSHBACK, "push-back line")):
        src, m = _swap(src, old, new, f"registrar {label}")
        notes.append(m)
    if "## Standing decisions come first" in src:
        notes.append("registrar tail: already patched")
    else:
        src = src.rstrip("\n") + "\n" + REG_TAIL
        notes.append("registrar tail: appended (standing decisions, open-decisions format, apply mode)")
    return src, notes


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    if not AGENT_SRC.exists():
        sys.exit(f"missing {AGENT_SRC}")
    agent_text, _ = _read(AGENT_SRC)
    if not agent_text.startswith("---\nname: decision-maker\n"):
        sys.exit("decision-maker.md: frontmatter not as expected; stopping")
    if AGENT_DST.exists() and _read(AGENT_DST)[0] == agent_text:
        print("decision-maker agent: already installed")
    else:
        print(f"decision-maker agent: {'update' if AGENT_DST.exists() else 'install'} -> {AGENT_DST.relative_to(ROOT)}")

    reg_src, reg_crlf = _read(REGISTRAR)
    reg_new, notes = patch_registrar(reg_src)
    for n in notes:
        print(n)

    cl_src, cl_crlf = _read(CLAUDE_MD)
    cl_new, m = _swap(cl_src, CLAUDE_OLD, CLAUDE_NEW, "CLAUDE.md agent list")
    print(m)

    if a.apply:
        _write(AGENT_DST, agent_text, reg_crlf)
        _write(REGISTRAR, reg_new, reg_crlf)
        _write(CLAUDE_MD, cl_new, cl_crlf)
        print("\nwritten: .claude/agents/decision-maker.md, .claude/agents/registrar.md, CLAUDE.md")
    else:
        print("\n--check only: nothing written")


if __name__ == "__main__":
    main()
