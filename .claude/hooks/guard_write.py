#!/usr/bin/env python3
"""PreToolUse guard for Edit/Write/MultiEdit. Exit 2 blocks with reason on stderr.

Rules:
  - Nobody edits .env*, secrets, or a committed (locked) PREREG.
  - Nobody edits enforcement code (.claude/, controller, validators, freeze, eval_utils).
  - Writes are confined to research/, docs/, playbook/.
  - DESK_ADMIN=1 (a launch-time env var, see scripts/start_desk.sh --admin) lifts the
    enforcement-code and allowed-prefix rules for deliberate maintenance. It does NOT lift
    the credential rule or the locked-PREREG rule.

FAIL-SAFE SCOPE (changed 2026-09-10). Claude Code 2.1.267 does not populate `agent_type` in
the PreToolUse payload for subagent tool calls, so the previous `if agent not in {...}:
sys.exit(0)` line made every rule below it unreachable for desk agents AND for the main
session — including the locked-PREREG lock, which is a research-integrity rule, not a
convenience. Rules now apply to every session by default.

The one rule that genuinely needs identity — "only the data-steward writes under
research/data/" — cannot be enforced while identity is unavailable. It is applied when
identity IS known (a future version, or a per-agent hook command passing --agent <name>)
and otherwise skipped. Do not rely on it today; the manifest SHA-256 chain in
freeze_dataset.py is what actually protects frozen data.
"""
import json
import os
import re
import subprocess
import sys

ALLOWED_PREFIXES = ("research/", "docs/", "playbook/")
FORBIDDEN_SUBSTRINGS = (".env", "/secrets/", "settings.local.json")
PROTECTED_PREFIXES = (".claude/", "research/lib/validators.py", "research/lib/controller.py",
                      "research/lib/freeze_dataset.py", "research/lib/eval_utils.py")
DESK_AGENTS = {"data-steward", "registrar", "explorer", "researcher", "red-team", "brief-writer", "reporter"}

ADMIN = os.environ.get("DESK_ADMIN", "").strip().lower() in {"1", "true", "yes"}

# Alpaca keys can place orders; guard_bash blocks trading calls on the command line, and this
# closes the other route — writing a trading call into a script and then running the script.
# Scanned only in executable files, so prose that merely mentions an endpoint stays writable.
# DESK_ADMIN lifts it, because the guard's own source necessarily contains these patterns.
ALPACA_TRADING = re.compile(r"((paper-)?api\.alpaca\.markets|TradingClient|submit_order|replace_order|cancel_order|close_position|/v2/(orders|positions|account))", re.I)
CODE_SUFFIXES = (".py", ".sh", ".ps1", ".ipynb", ".js", ".ts", ".bat", ".cmd")


def written_text(tool_input) -> str:
    parts = [tool_input.get("content") or "", tool_input.get("new_string") or ""]
    for e in tool_input.get("edits") or []:
        if isinstance(e, dict):
            parts.append(e.get("new_string") or "")
    return "\n".join(parts)


def block(reason: str) -> None:
    sys.stderr.write(f"BLOCKED by guard_write: {reason}\n")
    sys.exit(2)


def resolve_agent(payload) -> str:
    """Best-effort caller identity; '' means unknown."""
    for key in ("agent_type", "agent_id", "subagent_type"):
        v = payload.get(key)
        if v:
            return str(v)
    v = os.environ.get("CLAUDE_AGENT_TYPE", "")
    if v:
        return v
    argv = sys.argv[1:]
    if "--agent" in argv:
        i = argv.index("--agent")
        if i + 1 < len(argv):
            return argv[i + 1]
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
    rel = os.path.relpath(os.path.abspath(path), root).replace("\\", "/")
    agent = resolve_agent(payload)

    # Absolute rules — no DESK_ADMIN escape.
    if any(s in rel for s in FORBIDDEN_SUBSTRINGS):
        block(f"{rel} is a credential/settings file")
    if is_locked_prereg(root, rel):
        block(f"{rel} is committed and therefore locked; register a new question instead")
    if not ADMIN and rel.lower().endswith(CODE_SUFFIXES) and ALPACA_TRADING.search(written_text(tool_input)):
        block(f"{rel} contains an Alpaca trading call; the desk uses market data only (data.alpaca.markets)")

    # Identity-dependent rule: enforced only when identity is actually available.
    if rel.startswith("research/data/") and agent and agent != "data-steward":
        block("only the data-steward writes under research/data/")

    if ADMIN:
        sys.exit(0)

    if any(rel.startswith(p) for p in PROTECTED_PREFIXES):
        block(f"{rel} is enforcement code; relaunch with DESK_ADMIN=1 to do maintenance")
    if not rel.startswith(ALLOWED_PREFIXES):
        block(f"{rel} is outside research/, docs/, playbook/ — the platform codebase is read-only; write an implementation brief instead")
    sys.exit(0)


if __name__ == "__main__":
    main()
