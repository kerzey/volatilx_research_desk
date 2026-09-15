#!/usr/bin/env python
"""patch9 — DP-59: platform changes ship directly. No feature flags, no shadow mode, no inertness proof.

Why (Haci, 2026-09-15): "Every brief wants to create a flag... I don't want it, it's hard to keep.
Fix is fix. We will check here if it is working fine. I am the only user in the platform."

The desk already recorded DP-59 and rewrote the open briefs (PI-020, EN-019). But the files below
still tell every agent to add flags, and some of them only a human may edit. This script changes
all of them in one run so nothing disagrees afterwards.

What changes:

  CLAUDE.md                        rule 11 becomes "Ship, then verify here"; the list of your
                                   controller steps says IMPLEMENTED instead of IMPLEMENTED_FLAG_OFF
  README.md                        Step 9 and the Saturday note describe the no-flag path
  .claude/agents/brief-writer.md   no flag / shadow / inertness sections; after-deploy check;
                                   rollback = git revert; internal tools ship live, Haci-only
  .claude/agents/data-steward.md   "Shadow protocol" becomes "Live grading protocol" (results/LIVE.json)
  .claude/skills/desk-run/SKILL.md the verify sub-command names IMPLEMENTED
  research/lib/controller.py       finding path is now
                                     HUMAN_APPROVED -> BRIEF_WRITTEN -> IMPLEMENTED -> LIVE_VALIDATED -> RELEASE_APPROVED
                                   IMPLEMENTED:    --by haci, note carries the PR and the deployed sha
                                   LIVE_VALIDATED: results/LIVE.json, >= 30 live nights, mean_alpha > 0
                                                   (this is still what makes a finding PROSPECTIVELY_CONFIRMED)
                                   RELEASE_APPROVED: --by haci — approves quoting it to subscribers
                                   BRIEF_WRITTEN now requires an "After-deploy check" section, not "Inertness proof"
  research/lib/desk_queue.py       queue/board wording for the renamed states
  research/lib/board.py            one sentence on the enhancements section
  docs/AUTONOMOUS_DESK.md, docs/HOW_THE_DESK_WORKS.md, docs/chatgpt/RESEARCH_DESK_CONTEXT.md,
  research/templates/PREREG_TEMPLATE.md    same wording

What does NOT change: rule 10 (only PROSPECTIVELY_CONFIRMED supports a subscriber claim), the three
human-only controller steps, every research state before HUMAN_APPROVED, DP-49 (no database step for
the coding agent), DP-50 (locked questions split at a ship date). Locked PREREGs that mention the old
state names in their prose are historical text and are not touched. No question is on the finding
path today, so no state.json needs changing; the script refuses to run if one is.

Usage (from the repo root, in a plain PowerShell or Git Bash window -- NOT inside Claude):

    python docs/controller_patches/patch_no_flags.py --check    # show what would change, change nothing
    python docs/controller_patches/patch_no_flags.py            # apply
    python docs/controller_patches/test_no_flags.py             # prove it (runs on temp copies)

Idempotent: a second run reports "already applied". Writes <file>.bak next to each file before
changing it; roll back by copying the .bak files back. If any file has drifted from what this
script expects, it changes NOTHING and says which text it could not find.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

MARKER = "patch9 (2026-09-15, DP-59)"

PATCHES = {
    # ---------------------------------------------------------------------------------------------
    "CLAUDE.md": [
        ("11. **Prove inert, ship dark, flip last.** New code ships flag-off with a byte-identical\n"
         "    checksum on the old path; validated in shadow; activated only after inertness is confirmed.\n",
         "11. **Ship, then verify here (DP-59).** Platform changes ship directly: no feature flag, no shadow\n"
         "    mode, no inertness proof. The desk verifies every fix, build and finding after deploy with a\n"
         "    read-only before/after check and logs the ship SHA and date in `research/data/DATA_NOTES.md`;\n"
         "    locked questions split at that date (DP-50). A finding still needs >= 30 live nights graded by\n"
         "    the Data Steward before it is PROSPECTIVELY_CONFIRMED and quotable to subscribers (rule 10).\n"),
        ("(HUMAN_APPROVED, IMPLEMENTED_FLAG_OFF, RELEASE_APPROVED)",
         "(HUMAN_APPROVED, IMPLEMENTED, RELEASE_APPROVED)"),
    ],
    # ---------------------------------------------------------------------------------------------
    "README.md": [
        ("  `IMPLEMENTATION_BRIEF.md` (flag-off, shadow column, inertness hashes, tests, rollback) → you run\n"
         "  it in the platform repo with your coding agent → `advance QNNN IMPLEMENTED_FLAG_OFF --by haci\n"
         "  --note \"PR #… sha before=… after=…\"` → Steward grades the shadow column ≥30 nights →\n"
         "  `SHADOW_VALIDATED` → you `RELEASE_APPROVED` → flip the flag.\n",
         "  `IMPLEMENTATION_BRIEF.md` (change, live grading column, after-deploy check, tests, rollback; no\n"
         "  flag — DP-59) → you run it in the platform repo with your coding agent and deploy → `advance QNNN\n"
         "  IMPLEMENTED --by haci --note \"PR #… sha …\"` → Steward grades it live ≥30 nights →\n"
         "  `LIVE_VALIDATED` → you `RELEASE_APPROVED` → it may be quoted to subscribers.\n"),
        ("Only you can advance HUMAN_APPROVED,\nIMPLEMENTED_FLAG_OFF and RELEASE_APPROVED.",
         "Only you can advance HUMAN_APPROVED,\nIMPLEMENTED and RELEASE_APPROVED."),
    ],
    # ---------------------------------------------------------------------------------------------
    ".claude/agents/brief-writer.md": [
        ("2. **Change** — precisely what behaviour is added, and the config flag that gates it\n"
         "   (follow the repo's existing flag conventions; default OFF). Name the runtime setting keys.\n"
         "3. **Shadow column / sidecar** — what to persist so the Data Steward can grade the feature dark\n"
         "   for ≥30 nights (column name, table, write point, `path:line` of the write).\n"
         "4. **Inertness proof** — the exact dry-run command on a fixed trading date, before and after,\n"
         "   with SHA-256 of both outputs required to match; where to paste the hashes.\n"
         "5. **Tests** — flag-off path unchanged (unit), flag-on behaviour against a fixture built from\n"
         "   the study's frozen data (include the fixture rows), any DB-contract test.\n",
         "2. **Change** — precisely what behaviour is added. **No feature flag, no shadow mode, no inertness\n"
         "   proof (DP-59)** — it ships live. Name any runtime setting keys that size the job; settings are\n"
         "   not gates.\n"
         "3. **Live grading column** — what the platform persists so the Data Steward can grade the feature\n"
         "   live for ≥30 nights (column name, table, write point, `path:line` of the write). Usually the\n"
         "   feature's own output; add nothing extra if it already exists.\n"
         "4. **After-deploy check** — the read-only query or listing the Data Steward runs on the first\n"
         "   nightly after deploy, with expected values; and **what changes for the desk** — which published\n"
         "   numbers or stored rows change from the ship date, so the SHA is logged in DATA_NOTES.md and\n"
         "   locked questions split there (DP-50).\n"
         "5. **Tests** — unit tests against a fixture built from the study's frozen data (include the fixture\n"
         "   rows), any DB-contract test. No live calls.\n"),
        ("8. **Rollback** — one command / one flag.",
         "8. **Rollback** — `git revert` of the PR."),
        ("platform repo and advances IMPLEMENTED_FLAG_OFF himself with the PR link and hashes.",
         "platform repo, deploys it, and advances IMPLEMENTED himself with the PR link and the deployed SHA."),
        ("3. Change — the minimal fix. No feature flag when the fix restores intended behaviour;\n"
         "   say explicitly why no flag is needed. If the fix changes any published number, STOP and\n"
         "   return the issue to Haci as `research`.\n",
         "3. Change — the minimal fix. **Never a feature flag, shadow mode or inertness proof (DP-59).**\n"
         "   If the fix changes a published number, say which and from when; it still ships. Return the\n"
         "   issue as `research` only if the \"fix\" would change what is scored or selected on a\n"
         "   hypothesis rather than restore intended behaviour.\n"),
        ("4. Before/after check — one command on a fixed trading date; what differs, what must not.",
         "4. Before/after check — the coding agent's repository-only check (tests, diff), plus the read-only\n"
         "   check the Data Steward runs after deploy; what changes, what must not."),
        ("6. Rollback — one command.",
         "6. Rollback — `git revert` of the PR."),
        ("  `INTERNAL_TOOL — flag-off, visible to Haci only, no subscriber-facing copy or number; gate: QNNN\n"
         "  (<decision date>)`, then the same sections, plus an acceptance criterion that the subscriber\n"
         "  payload is byte-identical before and after (the inertness proof, rule 11). A trade idea (TI) is\n"
         "  always built this way until its evidence reads PROSPECTIVE.\n",
         "  `INTERNAL_TOOL — visible to Haci only (admin route or admin-only page), no subscriber-facing copy\n"
         "  or number; gate: QNNN (<decision date>)`, then the same sections. It ships live with no flag\n"
         "  (DP-59); being Haci-only is what keeps it off subscriber surfaces. A trade idea (TI) is always\n"
         "  built this way until its evidence reads PROSPECTIVE.\n"),
        ("names the constraint in its own header — flag-off until that question's decision date, the\n"
         "PI-011 / Q010 pattern — and the repair log row",
         "names the constraint in its own header — the ship date it creates and the locked questions that\n"
         "split at it (DP-50; under DP-59 it still ships) — and the repair log row"),
    ],
    # ---------------------------------------------------------------------------------------------
    ".claude/agents/data-steward.md": [
        ("## Shadow protocol\n"
         "When a question reaches IMPLEMENTED_FLAG_OFF, grade its shadow column nightly with the same\n"
         "T+10 rule. After ≥30 nights write `results/SHADOW.json` {n_nights, mean_alpha, ci} so the\n"
         "controller can evaluate SHADOW_VALIDATED. You do not decide; the controller does.\n",
         "## Live grading protocol (DP-59: findings ship live, no shadow)\n"
         "When a question reaches IMPLEMENTED, grade its live output nightly with the same T+10 rule,\n"
         "counting from the deployed SHA's ship date. After ≥30 nights write `results/LIVE.json`\n"
         "{n_nights, mean_alpha, ci, ship_sha, ship_date} so the controller can evaluate LIVE_VALIDATED.\n"
         "You do not decide; the controller does.\n"),
    ],
    # ---------------------------------------------------------------------------------------------
    ".claude/skills/desk-run/SKILL.md": [
        ("(`IMPLEMENTED_FLAG_OFF --by haci --note \"PR …\n"
         "  sha …\"`); reply with that command, then the steward's shadow protocol takes over on later runs.",
         "(`IMPLEMENTED --by haci --note \"PR …\n"
         "  sha …\"`); reply with that command, then the steward's live grading protocol takes over on later runs."),
    ],
    # ---------------------------------------------------------------------------------------------
    "research/lib/controller.py": [
        ("\"REDTEAM_SIGNED\", \"LEDGERED\", \"HUMAN_APPROVED\", \"BRIEF_WRITTEN\", \"IMPLEMENTED_FLAG_OFF\",\n"
         "         \"SHADOW_VALIDATED\", \"RELEASE_APPROVED\"]\n",
         "\"REDTEAM_SIGNED\", \"LEDGERED\", \"HUMAN_APPROVED\", \"BRIEF_WRITTEN\", \"IMPLEMENTED\",\n"
         "         \"LIVE_VALIDATED\", \"RELEASE_APPROVED\"]  # " + MARKER + ": no flag-off / shadow states\n"),
        ("HUMAN_ONLY = {\"HUMAN_APPROVED\", \"IMPLEMENTED_FLAG_OFF\", \"RELEASE_APPROVED\"}",
         "HUMAN_ONLY = {\"HUMAN_APPROVED\", \"IMPLEMENTED\", \"RELEASE_APPROVED\"}"),
        ("    if \"Inertness proof\" not in f.read_text() or \"Rollback\" not in f.read_text():",
         "    if \"After-deploy check\" not in f.read_text() or \"Rollback\" not in f.read_text():"),
        ("def pre_IMPLEMENTED_FLAG_OFF(d, st, args):",
         "def pre_IMPLEMENTED(d, st, args):"),
        ("        return \"--note must carry the PR link and the before/after dry-run hashes\"",
         "        return \"--note must carry the PR link and the deployed sha\""),
        ("def pre_SHADOW_VALIDATED(d, st, args):\n"
         "    f = d / \"results\" / \"SHADOW.json\"\n",
         "def pre_LIVE_VALIDATED(d, st, args):\n"
         "    f = d / \"results\" / \"LIVE.json\"\n"),
        ("\"results/SHADOW.json missing (steward writes it after ≥30 shadow nights)\"",
         "\"results/LIVE.json missing (steward writes it after ≥30 live nights)\""),
        (" shadow nights; need ≥ 30\"",
         " live nights; need ≥ 30\""),
        ("\"shadow mean_alpha not > 0",
         "\"live mean_alpha not > 0"),
    ],
    # ---------------------------------------------------------------------------------------------
    "research/lib/desk_queue.py": [
        ("    \"IMPLEMENTED_FLAG_OFF\": \"steward shadow grading (≥ 30 nights)\",\n"
         "    \"SHADOW_VALIDATED\": \"Haci: RELEASE_APPROVED\",\n",
         "    \"IMPLEMENTED\": \"steward live grading (≥ 30 nights)\",\n"
         "    \"LIVE_VALIDATED\": \"Haci: RELEASE_APPROVED\",\n"),
        ("IMPLEMENTATION_BRIEF.md in the platform repo, flag OFF\",",
         "IMPLEMENTATION_BRIEF.md in the platform repo and deploy (no flag, DP-59)\","),
        ("advance {q['id']} IMPLEMENTED_FLAG_OFF --by haci --note \\\"PR <link> sha <before> <after>\\\"\"",
         "advance {q['id']} IMPLEMENTED --by haci --note \\\"PR <link> sha <deployed>\\\"\""),
        ("        elif s == \"IMPLEMENTED_FLAG_OFF\":\n",
         "        elif s == \"IMPLEMENTED\":\n"),
        ("\"steward: shadow grading nightly; SHADOW.json after ≥ 30 nights\"",
         "\"steward: live grading nightly; LIVE.json after ≥ 30 nights\""),
        ("        elif s == \"SHADOW_VALIDATED\":\n",
         "        elif s == \"LIVE_VALIDATED\":\n"),
        ("\"what\": \"flip the flag on\",",
         "\"what\": \"approve quoting it to subscribers (PROSPECTIVELY_CONFIRMED)\","),
    ],
    # ---------------------------------------------------------------------------------------------
    "research/lib/board.py": [
        ("(rule 10/11) unless built as a flag-off internal tool._\\n\")",
         "(rule 10) unless built as a Haci-only internal tool (DP-59: no flags)._\\n\")"),
    ],
    # ---------------------------------------------------------------------------------------------
    "docs/AUTONOMOUS_DESK.md": [
        ("| HUMAN_APPROVED, IMPLEMENTED_FLAG_OFF, RELEASE_APPROVED |",
         "| HUMAN_APPROVED, IMPLEMENTED, RELEASE_APPROVED |"),
        ("or ships as a flag-off internal tool. |",
         "or ships as a Haci-only internal tool (no flag, DP-59). |"),
    ],
    # ---------------------------------------------------------------------------------------------
    "docs/HOW_THE_DESK_WORKS.md": [
        ("  → YOU run the brief in the platform repo, flag OFF, record SHA  ← moment 2\n"
         "  → steward grades the dark column ≥ 30 nights → SHADOW_VALIDATED → YOU flip the flag ← moment 3\n",
         "  → YOU run the brief in the platform repo and deploy it, record SHA (IMPLEMENTED)  ← moment 2\n"
         "  → steward grades it live ≥ 30 nights → LIVE_VALIDATED → YOU approve quoting it (RELEASE_APPROVED) ← moment 3\n"),
        ("a flag-off internal tool for you only.",
         "an internal tool for you only (no flag, DP-59)."),
        ("python research/lib/controller.py advance Q00N IMPLEMENTED_FLAG_OFF --by haci --note \"PR … sha …\"\n"
         "python research/lib/controller.py advance Q00N RELEASE_APPROVED --by haci   # yours: flip the flag\n",
         "python research/lib/controller.py advance Q00N IMPLEMENTED --by haci --note \"PR … sha …\"\n"
         "python research/lib/controller.py advance Q00N RELEASE_APPROVED --by haci   # yours: quotable to subscribers\n"),
    ],
    # ---------------------------------------------------------------------------------------------
    "docs/chatgpt/RESEARCH_DESK_CONTEXT.md": [
        ("     -> IMPLEMENTED_FLAG_OFF* -> SHADOW_VALIDATED -> RELEASE_APPROVED*",
         "     -> IMPLEMENTED* -> LIVE_VALIDATED -> RELEASE_APPROVED*"),
        ("9. **Ship, if it earns it** — prove inert, ship flag-off, validate in shadow, flip the flag last.",
         "9. **Ship, if it earns it** — ship directly with no flag (DP-59), verify after deploy, grade it live ≥ 30 nights before quoting it."),
    ],
    # ---------------------------------------------------------------------------------------------
    "research/templates/PREREG_TEMPLATE.md": [
        ("Owner: implementer. Flag off, prove inert, shadow validation ≥ 30 nights. HUMAN_APPROVED,\n"
         "IMPLEMENTED_FLAG_OFF and RELEASE_APPROVED retain their human-only gates.",
         "Owner: implementer. Ships live, no flag (DP-59); live grading ≥ 30 nights. HUMAN_APPROVED,\n"
         "IMPLEMENTED and RELEASE_APPROVED retain their human-only gates."),
    ],
}

OLD_STATES = ("IMPLEMENTED_FLAG_OFF", "SHADOW_VALIDATED")


def _variants(old: str, new: str, text: str):
    """Match either LF or CRLF endings, and write back in the file's own style."""
    if "\n" in old and old not in text and new not in text:
        o, n = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
        if o in text or n in text:
            return o, n
    return old, new


def plan(root: Path):
    """Return (changes, problems). changes: {path: new_text}. Nothing is written here."""
    changes, problems, applied = {}, [], []
    for rel, pairs in PATCHES.items():
        p = root / rel
        if not p.exists():
            problems.append(f"{rel}: file not found")
            continue
        text = p.read_bytes().decode("utf-8")
        new_text, touched = text, False
        for old, new in pairs:
            o, n = _variants(old, new, new_text)
            count_old, count_new = new_text.count(o), new_text.count(n)
            if count_old == 1:
                new_text, touched = new_text.replace(o, n), True
            elif count_old == 0 and count_new >= 1:
                continue  # already applied
            else:
                first = old.strip().splitlines()[0][:90]
                problems.append(f"{rel}: expected exactly one of: {first!r} (found {count_old})")
        if touched:
            changes[rel] = new_text
        elif not any(pr.startswith(rel + ":") for pr in problems):
            applied.append(rel)
    # refuse if any question is sitting on a state this patch removes
    for sf in sorted((root / "research/questions").glob("Q*/state.json")):
        try:
            st = json.loads(sf.read_text(encoding="utf-8"))
        except Exception:
            continue
        if st.get("state") in OLD_STATES:
            problems.append(f"{sf.parent.name}: state is {st['state']} — move it by hand before patching")
    return changes, problems, applied


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="report only; change nothing")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[2]), help=argparse.SUPPRESS)
    args = ap.parse_args()
    root = Path(args.root)

    changes, problems, applied = plan(root)
    for rel in applied:
        print(f"  already applied  {rel}")
    for rel in changes:
        print(f"  will change      {rel}")
    if problems:
        print("\nNOT APPLIED — nothing was changed. These texts were not found as expected:")
        for pr in problems:
            print("  - " + pr)
        sys.exit(1)
    if not changes:
        print("\nNothing to do: patch9 is already fully applied.")
        return
    if args.check:
        print(f"\n--check: {len(changes)} file(s) would change. Run without --check to apply.")
        return
    for rel, text in changes.items():
        p = root / rel
        shutil.copyfile(p, p.with_name(p.name + ".bak"))
        p.write_bytes(text.encode("utf-8"))
    print(f"\npatch9 applied to {len(changes)} file(s); a .bak copy sits next to each.")
    print("Next: python docs/controller_patches/test_no_flags.py")


if __name__ == "__main__":
    main()
