#!/usr/bin/env python3
"""PreToolUse guard for Bash. Reads hook JSON on stdin; exit 2 blocks with reason on stderr.

Blocks:
  - any SQL DML/DDL keyword in a command that also references a DB URL / psql
  - any credential name other than the research read-only ones
  - writes/deletes to Azure blob containers other than `research`
  - force pushes, history rewrites
  - rm -rf, sudo, curl|sh style installs
  - Alpaca trading endpoints (market data only) — absolute, no DESK_ADMIN escape
  - modification of enforcement code (unless DESK_ADMIN=1)
  - any `--by haci` (human-only transitions) and any DESK_ADMIN token, unless launched as admin (patch10)
Logs every decision to research/reports/hook_audit.log (stderr only on block).

FAIL-SAFE SCOPE (changed 2026-09-10). Claude Code 2.1.267 does not populate `agent_type` in
the PreToolUse payload, nor CLAUDE_AGENT_TYPE in the hook environment, for subagent tool
calls — verified against 16 subagent-originated commands, all logged with an empty agent
field. The previous version gated its strongest rules behind `agent in DESK_AGENTS`, so with
identity unavailable those rules never executed at all: the SQL-DML block, the
foreign-credential block, the blob rule, the git rules, the pipeline-script rule and the
enforcement-code rule were dead code.

Every rule now applies to EVERY session. Deliberate maintenance is done by launching with
DESK_ADMIN=1 (see scripts/start_desk.sh --admin). That is a launch-time decision: this hook
reads its own process environment, which a command's inline `VAR=value` prefix cannot change.
`resolve_agent` still records identity when a future Claude Code version provides it, and
accepts `--agent <name>` on the hook command line for per-agent hook definitions.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

DML = re.compile(r"\b(insert|update|delete|drop|truncate|alter|grant|revoke|create|vacuum|copy\s+.*\s+from)\b", re.I)
DB_CONTEXT = re.compile(r"(psql|research/lib/db\.py|DATABASE_URL|DB_URL|postgres(ql)?://|pg_dump|pg_restore)", re.I)
FORBIDDEN_CREDS = re.compile(r"(DATABASE_URL_ADMIN|DATABASE_URL\b(?!_RESEARCH)|APP_DB_URL|PROD_DB_URL|BACKFILL_DB_URL|AZURE_STORAGE_KEY|AZURE_STORAGE_CONNECTION_STRING|ACCOUNT_KEY)", re.I)
BLOB_WRITE = re.compile(r"az\s+storage\s+(blob|container)\s+(upload|delete|set|copy|sync)", re.I)
BLOB_RESEARCH = re.compile(r"(--container-name|-c)\s+research\b", re.I)
GIT_DANGER = re.compile(r"git\s+push.*(--force|-f\b|\+)|git\s+(reset\s+--hard|filter-branch)", re.I)
GIT_PUSH = re.compile(r"git\s+push\b", re.I)
GIT_PUSH_FEATURE = re.compile(r"git\s+push\s+(--set-upstream\s+|-u\s+)?origin\s+feature/Q\d{3}-[\w.-]+\s*$", re.I)
DESTRUCTIVE = re.compile(r"(\brm\s+-[a-z]*r[a-z]*f|\bsudo\b|curl[^|]*\|\s*(ba)?sh|wget[^|]*\|\s*(ba)?sh|\bmkfs\b|\bdd\s+if=)", re.I)
# Alpaca API keys are NOT read-only: the pair that reads prices can also place orders on the
# account it belongs to. The desk may use market DATA only (data.alpaca.markets). The trading
# hosts, the trading SDK client and the order/position/account routes are blocked outright.
ALPACA_TRADING = re.compile(r"((paper-)?api\.alpaca\.markets|TradingClient|submit_order|replace_order|cancel_order|close_position|/v2/(orders|positions|account))", re.I)

ADMIN = os.environ.get("DESK_ADMIN", "").strip().lower() in {"1", "true", "yes"}
DESK_AGENTS = {"data-steward", "registrar", "explorer", "researcher", "red-team", "brief-writer", "reporter"}

CODEBASE = os.environ.get("CODEBASE_DIR", "").replace("\\", "/").rstrip("/")
CODE_WRITE = re.compile(r"(>|>>|\bsed\s+-i|\btee\b|\bmv\b|\bcp\b|\brm\b|\bchmod\b|\btouch\b|\bpython3?\s+-c)")
CODE_GIT_RO = re.compile(r"git\s+(-C\s+\S+\s+)?(log|show|diff|rev-parse|status|ls-files|blame|describe|branch\s+--show-current)\b")
ENFORCEMENT = re.compile(r"(\.claude/|research/lib/validators\.py|research/lib/controller\.py|research/lib/freeze_dataset\.py|research/lib/eval_utils\.py)")

# patch10 (cockpit, 2026-09-15): the human gate and the admin flag never come from inside a session.
BY_HACI = re.compile(r"--by(?:=|\s+)[\"']?haci\b", re.I)
ADMIN_TOKEN = re.compile(r"\bDESK_ADMIN\b")


def resolve_agent(payload) -> str:
    """Best-effort caller identity; '' means unknown. Unknown is treated as a desk agent."""
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


def log(decision: str, cmd: str, reason: str = "", agent: str = "") -> None:
    try:
        root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
        os.makedirs(os.path.join(root, "research", "reports"), exist_ok=True)
        with open(os.path.join(root, "research", "reports", "hook_audit.log"), "a") as f:
            f.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "decision": decision,
                "agent": agent or "unknown",
                "admin": ADMIN,
                "reason": reason,
                "cmd": cmd[:500],
            }) + "\n")
    except Exception:
        pass


def block(cmd: str, reason: str, agent: str = "") -> None:
    log("BLOCK", cmd, reason, agent)
    sys.stderr.write(f"BLOCKED by guard_bash: {reason}\n")
    sys.exit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.stderr.write("BLOCKED by guard_bash: unparseable hook input (fail closed)\n"); sys.exit(2)
    if payload.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (payload.get("tool_input") or {}).get("command", "") or ""
    agent = resolve_agent(payload)

    # patch10: the three HUMAN_ONLY transitions are Haci's alone (controller.py:25). They are typed
    # in a terminal, never issued by an agent or a cockpit job. DESK_ADMIN is a launch-time decision
    # (scripts/start_desk.sh --admin), never an inline prefix on one command.
    if not ADMIN and BY_HACI.search(cmd):
        block(cmd, "--by haci is a human-only transition; Haci runs it himself in a terminal", agent)
    if not ADMIN and ADMIN_TOKEN.search(cmd):
        block(cmd, "DESK_ADMIN cannot be set from inside a session; relaunch with scripts/start_desk.sh --admin", agent)
    if DESTRUCTIVE.search(cmd):
        block(cmd, "destructive shell command", agent)
    if re.search(r"git\s+push.*(--force|-f\b|\+)", cmd, re.I):
        block(cmd, "force pushes are blocked", agent)
    if BLOB_WRITE.search(cmd) and re.search(r"(delete|container\s+delete)", cmd, re.I) and not BLOB_RESEARCH.search(cmd):
        block(cmd, "blob deletes outside the `research` container are blocked", agent)
    # Absolute — DESK_ADMIN does not lift it. There is no maintenance reason to trade.
    if ALPACA_TRADING.search(cmd):
        block(cmd, "Alpaca trading endpoints are blocked; the desk uses market data only (data.alpaca.markets)", agent)

    # The platform codebase is READ-ONLY for everyone. CODEBASE_DIR now comes from
    # .claude/settings.json `env`, so this holds however Claude Code was launched.
    # A bare mention of the path is fine; only write-shaped commands are blocked.
    if CODEBASE and (CODEBASE in cmd.replace("\\", "/") or "../volatilx" in cmd or "CODEBASE_DIR" in cmd):
        if CODE_WRITE.search(cmd) or (re.search(r"\bgit\b", cmd) and not CODE_GIT_RO.search(cmd)):
            block(cmd, "the platform codebase is read-only from the research desk; changes go through an implementation brief", agent)

    # --- everything below was previously unreachable (agent identity never resolved) ---
    if FORBIDDEN_CREDS.search(cmd):
        block(cmd, "references a non-research credential; only RESEARCH_DB_URL / PROD_SAS_TOKEN / RESEARCH_SAS_TOKEN / ALPACA_* (market data) are allowed", agent)
    if DB_CONTEXT.search(cmd) and DML.search(cmd):
        block(cmd, "SQL write/DDL against a database is never allowed from the research desk", agent)
    if BLOB_WRITE.search(cmd) and not BLOB_RESEARCH.search(cmd):
        block(cmd, "blob writes/deletes are allowed only in the `research` container", agent)
    if GIT_DANGER.search(cmd):
        block(cmd, "force pushes and history rewrites are blocked; open a PR from a feature branch", agent)
    if re.search(r"run_(nightly_pipeline|super_agent_select|uoa|projection)", cmd):
        block(cmd, "platform pipeline scripts are never run from the research desk", agent)
    if ENFORCEMENT.search(cmd) and CODE_WRITE.search(cmd) and not ADMIN:
        block(cmd, "guardrail, controller, validator and freeze code cannot be modified from the desk; relaunch with DESK_ADMIN=1 for maintenance", agent)

    log("ALLOW", cmd, "admin session" if ADMIN else "", agent)
    sys.exit(0)


if __name__ == "__main__":
    main()
