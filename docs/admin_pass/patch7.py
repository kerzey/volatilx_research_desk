#!/usr/bin/env python3
"""Seventh maintenance pass — one rule, learned from PI-001.

    python docs/admin_pass/patch7.py --check
    python docs/admin_pass/patch7.py --apply

The coding agent in the platform repo has exactly one database configured: **production**.
The desk's read-only role does not exist there. PI-001's fix brief asked that agent to run
`scripts/backfill_outcomes.py` twice and diff the output (§4(b)), and to run a historical sweep
(Step B). It correctly refused both, and the refusal was right: the brief had told it to point a
DDL-issuing, price-fetching script at production. Six more fix briefs are queued behind PI-001
with the same shape, so the constraint goes in the charter rather than in one brief.

Appends "## Checks the coding agent can actually run" to .claude/agents/brief-writer.md.
Idempotent: re-running reports "already patched". The rule is also recorded as DP-49 in
research/DECISION_POLICY.md (already written; no patch needed, research/ is desk-writable).
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRIEF_WRITER = ROOT / ".claude/agents/brief-writer.md"
MARKER = "## Checks the coding agent can actually run"

TAIL = '''
## Checks the coding agent can actually run (DP-49)

The coding agent working in the platform repo has **one** database configured: production. The
desk's read-only role does not exist there, and there is no sandbox. So every check you address to
*that agent* must be satisfiable from the repository alone:

- the test suite (`python -m pytest tests/... -q`);
- importing a pure function and asserting on its return;
- `git show --stat <sha>`, `git diff`, a file hash — to prove a file was **not** changed;
- a dry-run that touches no DB, only if you have confirmed it opens no connection.

Never write "run this script before and after and compare the output" as the coding agent's proof
that it left a file alone. The diff proves that directly, needs no DB, and cannot be fooled by a
flaky fetch. Check whether the script's entry point calls a schema or migration helper before you
consider a dry-run DB-free at all.

Anything that reads a table belongs in the brief's final section, addressed to the **Data Steward**
on `$RESEARCH_DB_URL`. Anything that *writes* — a backfill, a sweep, a repair — is **Haci's**, named
as his with the exact command, the row count it will touch, and what it will move on the product.
Say plainly in the brief which steps are whose, so the coding agent is never left deciding whether
it is allowed to touch production.

**Before-snapshots come from the freeze.** When the affected table is in a pinned manifest
(`research/data/manifest_v*.json`), name that parquet as the before state instead of asking anyone
to capture a CSV first: it is sha256-pinned, immutable, and it predates the change by construction.
Quote the relevant counts from it in the brief so the comparison is already half-done.

**Scope the repair from the frozen data, not from an estimate.** Count the exact rows a sweep has
to touch — which dates, which columns, how many cells — and put the list in the brief. PI-001's
Step B was written as "roughly 2026-05-11..2026-06-10" across four horizons; measured, it was one
column and fifteen dates, two of which fell outside the range the brief gave.
'''


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    if not BRIEF_WRITER.exists():
        sys.exit(f"missing {BRIEF_WRITER}")
    raw = BRIEF_WRITER.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    src = raw.replace("\r\n", "\n")

    if MARKER in src:
        print("brief-writer: already patched")
        new = None
    else:
        print(f"brief-writer: append section -> {BRIEF_WRITER.relative_to(ROOT)}")
        new = src.rstrip("\n") + "\n" + TAIL

    if not a.apply:
        print("\n--check only: nothing written")
        return
    if new is not None:
        BRIEF_WRITER.write_bytes((new.replace("\n", "\r\n") if crlf else new).encode("utf-8"))
        print("\nwritten: .claude/agents/brief-writer.md")
    else:
        print("\nnothing to do")


if __name__ == "__main__":
    main()
