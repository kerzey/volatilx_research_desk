#!/usr/bin/env python3
"""Seventh maintenance pass — one database, and what a fix brief may ask of a coding agent.

    python docs/admin_pass/patch7.py --check
    python docs/admin_pass/patch7.py --apply

Two facts drive this pass, both established 2026-09-13.

1. **`$RESEARCH_DB_URL` and the platform's production database are the same instance** (Haci).
   The desk is separated by a *role* (`sas_research_ro`, read-only), not by a copy. The desk's
   documents were written as though a research database sat beside production. It does not.
   Recorded as DP-50 in research/DECISION_POLICY.md, with the operational consequences in
   research/data/DATA_NOTES.md ("One database" + the repair log).

2. **The coding agent in the platform repo holds a read-write credential on that same database.**
   PI-001's fix brief asked it to run `scripts/backfill_outcomes.py` twice and diff the output,
   and to run a historical sweep. It refused, correctly. Six more fix briefs are queued with the
   same shape, so the constraint goes in the charter, not in one brief. Recorded as DP-49.

Writes (both are human/enforcement files the desk cannot edit itself, hence a patch):
  - .claude/agents/brief-writer.md  += "## Checks the coding agent can actually run (DP-49, DP-50)"
  - CLAUDE.md                       += "## One database (2026-09-13)"

Idempotent: re-running reports "already patched". Nothing else is touched.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRIEF_WRITER = ROOT / ".claude/agents/brief-writer.md"
CLAUDE_MD = ROOT / "CLAUDE.md"

# An earlier revision of this patch was applied on 2026-09-13 before Haci established that the
# research URL and production are one database. That revision's section says "the desk's read-only
# role does not exist there", which is false. The section is the last one in the charter, so when
# the superseded header is found the patch truncates from it and appends the corrected text.
BW_MARKER = "## Checks the coding agent can actually run (DP-49, DP-50)"
BW_SUPERSEDED = "## Checks the coding agent can actually run (DP-49)"
BW_TAIL = '''
## Checks the coding agent can actually run (DP-49, DP-50)

**There is one database.** `$RESEARCH_DB_URL` and the platform's production database are the same
Postgres instance; the desk is separated by a read-only role, not by a copy. The coding agent in
the platform repo holds the platform's **read-write** credential on it. So any DB command you put
in a brief for that agent is a write-capable command pointed at live production data, whatever the
command's own intent. Do not write one.

Every check you address to the coding agent must be satisfiable from the repository alone:

- the test suite (`python -m pytest tests/... -q`);
- importing a pure function and asserting on its return;
- `git show --stat <sha>`, `git diff`, a file hash — to prove a file was **not** changed;
- a dry-run, and only after you have confirmed its entry point opens no connection. Check for a
  schema or migration helper first; `scripts/backfill_outcomes.py` calls `create_tables()` before
  it parses its own dry-run flag.

Never write "run this script before and after and compare the output" as the coding agent's proof
that it left a file alone. The diff proves that directly, needs no DB, and cannot be fooled by a
flaky fetch.

Anything that **reads** a table belongs in the brief's final section, addressed to the **Data
Steward** on the read-only role. Anything that **writes** is **Haci's**, named as his, with the
exact command, the number of rows it will touch, and what it will move on the product. Say in the
brief which steps are whose, so the coding agent is never left deciding whether it may touch
production.

**Before-snapshots come from the freeze.** When the affected table is in a pinned manifest, name
that parquet as the before state instead of asking anyone to capture a CSV first: it is
sha256-pinned, immutable, and it predates the change by construction. A live "before" is not
reproducible, because the rows behind it can be rewritten by the very repair you are briefing.
Quote the relevant counts from the freeze in the brief so the comparison is already half-done.

**Scope the repair from the frozen data, not from an estimate.** Count the exact rows a sweep has
to touch — which dates, which columns, how many cells — and put the date list in the brief. State
the counting rule you used, because "null today", "null and past its maturation window" and "null
and beyond any self-healing window" are three different numbers and a brief that quotes one
without saying which invites a contradictory recount. PI-001 produced two figures that both looked
like "the hole" and differed by a factor of two for exactly that reason.

**Check ship timing against every in-flight question (DP-50).** Before you write a repair brief,
read `research/lib/desk_queue.py` output or `research/BOARD.md` for the locked questions. If the
repair changes a column a locked PREREG reads, or changes which picks get published, the brief
names the constraint in its own header — flag-off until that question's decision date, the
PI-011 / Q010 pattern — and the repair log row in `research/data/DATA_NOTES.md` that will be
written when it ships. A repair is never briefed without that check.
'''

CL_MARKER = "## One database (2026-09-13)"
CL_TAIL = '''
## One database (2026-09-13)

`$RESEARCH_DB_URL` **is** the production database. There is no research copy: the desk is
separated by a read-only role (`sas_research_ro` — `UPDATE` and `CREATE` are refused at grant
level), not by a different instance. Rule 1 is unchanged and still binds; this says what it is
protecting against.

What follows from it, in full as DP-50 and `research/data/DATA_NOTES.md`:

- **Rule 4 is load-bearing.** The pinned manifest is the only thing standing between a locked
  question and a platform repair that rewrites history. Never take a number a PREREG will cite
  from a live query.
- **A successor freeze may disagree with its predecessor about the past**, because a repair can
  land between them. That is not a bug in either. A question whose window spans a repair date
  splits there, the way DP-06 splits the catalyst layer at 2026-06-01.
- **Every repair that rewrites historical rows is logged** in `research/data/DATA_NOTES.md` with
  its date, column, range and ship SHA, on the day it ships.
- **A fix brief never hands the coding agent a database step** (DP-49): its credential on that
  database is read-write.
'''


def _read(p):
    raw = p.read_bytes().decode("utf-8")
    return raw.replace("\r\n", "\n"), "\r\n" in raw


def _write(p, text, crlf):
    p.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def plan(path, marker, tail, label, superseded=None):
    if not path.exists():
        sys.exit(f"missing {path}")
    src, crlf = _read(path)
    if marker in src:
        print(f"{label}: already patched")
        return None, crlf
    if superseded and superseded in src:
        head = src[:src.index(superseded)]
        print(f"{label}: REPLACE superseded section -> {path.relative_to(ROOT)}")
        return head.rstrip("\n") + "\n" + tail, crlf
    print(f"{label}: append section -> {path.relative_to(ROOT)}")
    return src.rstrip("\n") + "\n" + tail, crlf


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    jobs = [
        (BRIEF_WRITER, *plan(BRIEF_WRITER, BW_MARKER, BW_TAIL, "brief-writer", BW_SUPERSEDED)),
        (CLAUDE_MD, *plan(CLAUDE_MD, CL_MARKER, CL_TAIL, "CLAUDE.md")),
    ]

    if not a.apply:
        print("\n--check only: nothing written")
        return
    written = []
    for path, new, crlf in jobs:
        if new is not None:
            _write(path, new, crlf)
            written.append(str(path.relative_to(ROOT)))
    print("\nwritten: " + (", ".join(written) if written else "nothing to do"))


if __name__ == "__main__":
    main()
