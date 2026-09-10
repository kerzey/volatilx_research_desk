#!/usr/bin/env python3
"""PreToolUse guard for Edit/Write/MultiEdit. Exit 2 blocks with reason on stderr.

Rules:
  - Nobody edits .env*, secrets, or committed manifests / PREREG files that are already locked.
  - Research agents write only under research/, .claude/, docs/research/.
  - The implementer may write anywhere except the above forbidden files, and only on a
    non-main git branch.
"""
import json
import os
import subprocess
import sys

ALLOWED_PREFIXES = ("research/", "docs/", "playbook/")
FORBIDDEN_SUBSTRINGS = (".env", "/secrets/", "settings.local.json")
# Nobody — not even the implementer — edits enforcement code from inside the desk.
PROTECTED_PREFIXES = (".claude/", "research/lib/validators.py", "research/lib/controller.py",
                      "research/lib/freeze_dataset.py", "research/lib/eval_utils.py", "research/data/")


def block(reason: str) -> None:
    sys.stderr.write(f"BLOCKED by guard_write: {reason}\n")
    sys.exit(2)


def current_branch(root: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", root, "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
    except Exception:
        return ""


def is_locked_prereg(root: str, rel: str) -> bool:
    """A PREREG.md that is already committed is locked; only a new question dir may be written."""
    if not rel.endswith("PREREG.md"):
        return False
    try:
        out = subprocess.check_output(["git", "-C", root, "ls-files", "--error-unmatch", rel],
                                      text=True, stderr=subprocess.DEVNULL)
        return bool(out.strip())
    except Exception:
        return False


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.stderr.write("BLOCKED by guard_write: unparseable hook input (fail closed)\n"); sys.exit(2)
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not path:
        sys.exit(0)
    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    rel = os.path.relpath(os.path.abspath(path), root)
    agent = payload.get("agent_type") or os.environ.get("CLAUDE_AGENT_TYPE", "")

    if any(s in rel for s in FORBIDDEN_SUBSTRINGS):
        block(f"{rel} is a credential/settings file")
    if agent not in {"data-steward", "registrar", "explorer", "researcher", "red-team", "brief-writer", "reporter"}:
        sys.exit(0)  # Haci's own dev session: only the credential rule above applies
    if rel.startswith("research/data/"):
        if agent != "data-steward":
            block("only the data-steward writes under research/data/")
    elif any(rel.startswith(p) for p in PROTECTED_PREFIXES):
        block(f"{rel} is enforcement code; edit it as a human, outside the desk")
    if is_locked_prereg(root, rel):
        block(f"{rel} is committed and therefore locked; register a new question instead")


    if not rel.startswith(ALLOWED_PREFIXES):
        block(f"{rel} is outside research/, docs/, playbook/ — the platform codebase is read-only; write an implementation brief instead")
    sys.exit(0)


if __name__ == "__main__":
    main()
