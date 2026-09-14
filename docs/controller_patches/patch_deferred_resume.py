#!/usr/bin/env python
"""patch8 — let a parked (DEFERRED, never-locked) question come back once its trigger is met.

Why (Q030 and Q032, 2026-09-14): both questions were parked because price data was missing.
The data arrived and every check passed, but they could not be restarted:

  1. research/lib/controller.py treats DEFERRED as a dead end -- no way back to PREREG_DRAFT.
  2. .claude/hooks/guard_write.py treats ANY PREREG.md saved in git as locked, even a draft
     that was saved only as the record of why it was parked and never started.

What this changes -- and what it does not:

  controller.py   adds exactly one new move, DEFERRED -> PREREG_DRAFT, allowed only when ALL of:
                    - --by desk or --by haci
                    - the question has NEVER been PREREG_LOCKED
                    - research/questions/DEFERRED.md has a "TRIGGER MET" line under its heading
  guard_write.py  a saved PREREG.md stays locked unless its question is currently PREREG_DRAFT
                  AND has never been PREREG_LOCKED. Every study that was ever locked stays
                  locked forever. An unreadable state.json counts as locked (fail closed).

Nothing about the 28 locked studies changes. The locked-PREREG rule still has no DESK_ADMIN
escape.

Usage (from the repo root, in a plain PowerShell or Git Bash window -- NOT inside Claude):

    python docs/controller_patches/patch_deferred_resume.py            # apply
    python docs/controller_patches/patch_deferred_resume.py --check    # report only
    python docs/controller_patches/test_deferred_resume.py             # prove it

Idempotent. Writes <file>.bak next to each file before changing it. Roll back by copying the
.bak files back. Refuses to run if a target has drifted from what it expects.
"""
import argparse
import shutil
import sys
from pathlib import Path

MARKER = "# patch8 (2026-09-14, Q030/Q032)"

# --- controller.py -------------------------------------------------------------------------
CTRL_OLD_FN = "def cmd_advance(args):\n"
CTRL_NEW_FN = (
    "def resume_deferred_error(d, st, args):\n"
    "    " + MARKER + ": the one way out of DEFERRED. A parked question may go back to\n"
    "    # PREREG_DRAFT only if it was never locked and DEFERRED.md records its trigger as met.\n"
    "    if args.by not in (\"desk\", \"haci\"):\n"
    "        return \"requires --by desk or --by haci\"\n"
    "    if any(h.get(\"state\") == \"PREREG_LOCKED\" for h in st.get(\"history\", [])):\n"
    "        return \"this question was locked once; a locked question never reopens (DP-22)\"\n"
    "    f = Path(\"research/questions/DEFERRED.md\")\n"
    "    text = f.read_text(encoding=\"utf-8\") if f.exists() else \"\"\n"
    "    section, inside = [], False\n"
    "    for line in text.splitlines():\n"
    "        if line.startswith(\"## \"):\n"
    "            inside = line[3:].split()[:1] == [args.q]\n"
    "            continue\n"
    "        if inside:\n"
    "            section.append(line)\n"
    "    if not any(\"TRIGGER MET\" in line for line in section):\n"
    "        return f\"no 'TRIGGER MET' line under '## {args.q}' in DEFERRED.md\"\n"
    "    return None\n"
    "\n"
    "\n"
    "def cmd_advance(args):\n"
)
CTRL_OLD_BODY = (
    "    cur, nxt = st[\"state\"], args.state\n"
    "    if nxt in TERMINAL:\n"
)
CTRL_NEW_BODY = (
    "    cur, nxt = st[\"state\"], args.state\n"
    "    if cur == \"DEFERRED\" and nxt == \"PREREG_DRAFT\":   " + MARKER + "\n"
    "        err = resume_deferred_error(d, st, args)\n"
    "        if err:\n"
    "            sys.exit(f\"cannot resume {args.q} from DEFERRED: {err}\")\n"
    "        st[\"state\"] = nxt\n"
    "        st[\"history\"].append({\"state\": nxt, \"at\": now(), \"by\": args.by, \"note\": args.note})\n"
    "        save(d, st)\n"
    "        print(f\"{args.q}: {cur} -> {nxt} (deferral lifted)\")\n"
    "        return\n"
    "    if nxt in TERMINAL:\n"
)

# --- guard_write.py ------------------------------------------------------------------------
GUARD_OLD = (
    "def is_locked_prereg(root: str, rel: str) -> bool:\n"
    "    \"\"\"A PREREG.md that is already committed is locked; only a new question dir may be written.\"\"\"\n"
    "    if not rel.endswith(\"PREREG.md\"):\n"
    "        return False\n"
    "    try:\n"
    "        out = subprocess.check_output([\"git\", \"-C\", root, \"ls-files\", \"--error-unmatch\", rel],\n"
    "                                      text=True, stderr=subprocess.DEVNULL)\n"
    "        return bool(out.strip())\n"
    "    except Exception:\n"
    "        return False\n"
)
GUARD_NEW = (
    "def is_locked_prereg(root: str, rel: str) -> bool:\n"
    "    \"\"\"A committed PREREG.md is locked unless its question is a never-locked draft.\n"
    "\n"
    "    " + MARKER + ": a draft saved in git only as the record of a deferral (state\n"
    "    back at PREREG_DRAFT via the controller, never PREREG_LOCKED) stays writable. Anything\n"
    "    that was ever PREREG_LOCKED stays locked forever. Unreadable state.json -> locked.\n"
    "    \"\"\"\n"
    "    if not rel.endswith(\"PREREG.md\"):\n"
    "        return False\n"
    "    try:\n"
    "        out = subprocess.check_output([\"git\", \"-C\", root, \"ls-files\", \"--error-unmatch\", rel],\n"
    "                                      text=True, stderr=subprocess.DEVNULL)\n"
    "        if not out.strip():\n"
    "            return False\n"
    "    except Exception:\n"
    "        return False\n"
    "    try:\n"
    "        with open(os.path.join(root, os.path.dirname(rel), \"state.json\"), encoding=\"utf-8\") as f:\n"
    "            st = json.load(f)\n"
    "        ever_locked = any(h.get(\"state\") == \"PREREG_LOCKED\" for h in st.get(\"history\", []))\n"
    "        return ever_locked or st.get(\"state\") != \"PREREG_DRAFT\"\n"
    "    except Exception:\n"
    "        return True\n"
)

TARGETS = [
    (Path("research/lib/controller.py"), [(CTRL_OLD_FN, CTRL_NEW_FN), (CTRL_OLD_BODY, CTRL_NEW_BODY)]),
    (Path(".claude/hooks/guard_write.py"), [(GUARD_OLD, GUARD_NEW)]),
    (Path("docs/guard_patches/guard_write.py"), [(GUARD_OLD, GUARD_NEW)]),   # the reference copy
]


def patch_text(src: str, pairs) -> str:
    for old, new in pairs:
        if src.count(old) != 1:
            raise ValueError(f"expected exactly one match, found {src.count(old)}:\n{old.splitlines()[0]}")
        src = src.replace(old, new, 1)
    return src


def patch_file(target: Path, pairs, check: bool) -> int:
    if not target.exists():
        print(f"ERROR: {target} not found (run from the repo root)", file=sys.stderr)
        return 2
    raw = target.read_bytes()
    eol = "\r\n" if b"\r\n" in raw else "\n"
    src = raw.decode("utf-8").replace("\r\n", "\n")
    if MARKER in src:
        print(f"already applied: {target}")
        return 0
    try:
        patched = patch_text(src, pairs)
    except ValueError as e:
        print(f"ERROR: {target} has changed; patch by hand. {e}", file=sys.stderr)
        return 3
    if check:
        print(f"not applied (would patch): {target}")
        return 1
    shutil.copyfile(target, target.with_suffix(target.suffix + ".bak"))
    target.write_bytes(patched.replace("\n", eol).encode("utf-8"))
    print(f"patched: {target}  (backup: {target.name}.bak)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="report status, change nothing")
    args = ap.parse_args()
    # Check every target first, so a drifted file never leaves the set half-patched.
    for target, pairs in TARGETS:
        if target.exists():
            src = target.read_bytes().decode("utf-8").replace("\r\n", "\n")
            if MARKER not in src:
                try:
                    patch_text(src, pairs)
                except ValueError as e:
                    print(f"ERROR: {target} has changed; nothing was patched. {e}", file=sys.stderr)
                    return 3
    worst = 0
    for target, pairs in TARGETS:
        worst = max(worst, patch_file(target, pairs, args.check))
    return worst


if __name__ == "__main__":
    sys.exit(main())
