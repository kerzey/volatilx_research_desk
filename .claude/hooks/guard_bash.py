#!/usr/bin/env python3
"""PreToolUse guard for Bash. Reads hook JSON on stdin; exit 2 blocks with reason on stderr.

Blocks:
  - any SQL DML/DDL keyword in a command that also references a DB URL / psql
  - any credential name other than the research read-only ones
  - writes/deletes to Azure blob containers other than `research`
  - git push to main/master, force pushes, history rewrites
  - rm -rf, sudo, curl|sh style installs
Logs every decision to research/reports/hook_audit.log (stderr only on block).
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

DML = re.compile(r"\b(insert|update|delete|drop|truncate|alter|grant|revoke|create|vacuum|copy\s+.*\s+from)\b", re.I)
DB_CONTEXT = re.compile(r"(psql|research/lib/db\.py|DATABASE_URL|DB_URL|postgres(ql)?://|pg_dump|pg_restore)", re.I)
FORBIDDEN_CREDS = re.compile(r"(DATABASE_URL_ADMIN|DATABASE_URL\b(?!_RESEARCH)|APP_DB_URL|PROD_DB_URL|AZURE_STORAGE_KEY|AZURE_STORAGE_CONNECTION_STRING|ACCOUNT_KEY)", re.I)
BLOB_WRITE = re.compile(r"az\s+storage\s+(blob|container)\s+(upload|delete|set|copy|sync)", re.I)
BLOB_RESEARCH = re.compile(r"(--container-name|-c)\s+research\b", re.I)
GIT_DANGER = re.compile(r"git\s+push.*(--force|-f\b|\+)|git\s+(reset\s+--hard|filter-branch)", re.I)
GIT_PUSH = re.compile(r"git\s+push\b", re.I)
GIT_PUSH_FEATURE = re.compile(r"git\s+push\s+(--set-upstream\s+|-u\s+)?origin\s+feature/Q\d{3}-[\w.-]+\s*$", re.I)
DESTRUCTIVE = re.compile(r"(\brm\s+-[a-z]*r[a-z]*f|\bsudo\b|curl[^|]*\|\s*(ba)?sh|wget[^|]*\|\s*(ba)?sh|\bmkfs\b|\bdd\s+if=)", re.I)


def log(decision: str, cmd: str, reason: str = "") -> None:
    try:
        root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
        os.makedirs(os.path.join(root, "research", "reports"), exist_ok=True)
        with open(os.path.join(root, "research", "reports", "hook_audit.log"), "a") as f:
            f.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "decision": decision,
                "agent": os.environ.get("CLAUDE_AGENT_TYPE", ""),
                "reason": reason,
                "cmd": cmd[:500],
            }) + "\n")
    except Exception:
        pass


def block(cmd: str, reason: str) -> None:
    log("BLOCK", cmd, reason)
    sys.stderr.write(f"BLOCKED by guard_bash: {reason}\n")
    sys.exit(2)


CODEBASE = os.environ.get("CODEBASE_DIR", "").replace("\\", "/").rstrip("/")
CODE_WRITE = re.compile(r"(>|>>|\bsed\s+-i|\btee\b|\bmv\b|\bcp\b|\brm\b|\bchmod\b|\btouch\b|\bpython3?\s+-c)")
CODE_GIT_RO = re.compile(r"git\s+(-C\s+\S+\s+)?(log|show|diff|rev-parse|status|ls-files|blame|describe|branch\s+--show-current)\b")
DESK_AGENTS = {"data-steward", "registrar", "explorer", "researcher", "red-team", "brief-writer", "reporter"}


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.stderr.write("BLOCKED by guard_bash: unparseable hook input (fail closed)\n"); sys.exit(2)
    if payload.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (payload.get("tool_input") or {}).get("command", "") or ""
    agent = payload.get("agent_type") or os.environ.get("CLAUDE_AGENT_TYPE", "")

    # Hard-safety rules apply to every session, including Haci's own dev sessions in this repo.
    if DESTRUCTIVE.search(cmd):
        block(cmd, "destructive shell command")
    if re.search(r"git\s+push.*(--force|-f\b|\+)", cmd, re.I):
        block(cmd, "force pushes are blocked")
    if BLOB_WRITE.search(cmd) and re.search(r"(delete|container\s+delete)", cmd, re.I) and not BLOB_RESEARCH.search(cmd):
        block(cmd, "blob deletes outside the `research` container are blocked")
    # The platform codebase is READ-ONLY for everyone in this repo, main session included.
    if CODEBASE and (CODEBASE in cmd.replace("\\", "/") or "../volatilx" in cmd or "CODEBASE_DIR" in cmd):
        if CODE_WRITE.search(cmd) or (re.search(r"\bgit\b", cmd) and not CODE_GIT_RO.search(cmd)):
            block(cmd, "the platform codebase is read-only from the research desk; changes go through an implementation brief")
    if agent not in DESK_AGENTS:
        log("ALLOW", cmd, "main session: hard-safety rules only")
        sys.exit(0)

    # Everything below applies only to the seven research-desk agents.
    if FORBIDDEN_CREDS.search(cmd):
        block(cmd, "references a non-research credential; only RESEARCH_DB_URL / PROD_BLOB_SAS / RESEARCH_BLOB_SAS are allowed")
    if DB_CONTEXT.search(cmd) and DML.search(cmd):
        block(cmd, "SQL write/DDL against a database is never allowed from the research desk")
    if BLOB_WRITE.search(cmd) and not BLOB_RESEARCH.search(cmd):
        block(cmd, "blob writes/deletes are allowed only in the `research` container")
    if GIT_DANGER.search(cmd):
        block(cmd, "pushes to main/master, force pushes and history rewrites are blocked; open a PR from a feature branch")
    # Only the brief-writer may run the nightly/scoring scripts, and only in dry-run.
    if re.search(r"run_(nightly_pipeline|super_agent_select|uoa|projection)", cmd):
        block(cmd, "platform pipeline scripts are never run from the research desk")
    if re.search(r"(\.claude/|research/lib/validators\.py|research/lib/controller\.py|research/lib/freeze_dataset\.py)", cmd) and re.search(r"(>|>>|\bsed\s+-i|\btee\b|\bmv\b|\bcp\b|\bchmod\b|\bpython3?\s+-c)", cmd):
        block(cmd, "guardrail, controller, validator and freeze code cannot be modified from the desk")

    log("ALLOW", cmd)
    sys.exit(0)


if __name__ == "__main__":
    main()
