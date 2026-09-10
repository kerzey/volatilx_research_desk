#!/usr/bin/env python3
"""Test the proposed guards. Run from the repo root:

    python docs/guard_patches/test_guards.py            # test the proposed files
    python docs/guard_patches/test_guards.py --installed  # test the live .claude/hooks copies

Each case is (label, payload, expect_blocked). Exit 0 = all pass.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INSTALLED = "--installed" in sys.argv
HOOK_DIR = os.path.join(ROOT, ".claude", "hooks") if INSTALLED else os.path.dirname(os.path.abspath(__file__))
PLATFORM = "C:/Users/sahin/Projects/volatilx"


def run(script, payload, admin=False):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=ROOT, CODEBASE_DIR=PLATFORM)
    env.pop("DESK_ADMIN", None)
    if admin:
        env["DESK_ADMIN"] = "1"
    p = subprocess.run([sys.executable, os.path.join(HOOK_DIR, script)],
                       input=json.dumps(payload), text=True, capture_output=True, env=env)
    return p.returncode == 2, p.stderr.strip()


def bash(cmd, agent=None):
    d = {"tool_name": "Bash", "tool_input": {"command": cmd}}
    if agent:
        d["agent_type"] = agent
    return d


def write(path, agent=None):
    d = {"tool_name": "Write", "tool_input": {"file_path": path}}
    if agent:
        d["agent_type"] = agent
    return d


BASH_CASES = [
    # (label, payload, expect_blocked, admin)
    ("SQL DML via db.py, identity unknown", bash('python research/lib/db.py "UPDATE users SET id=id"'), True, False),
    ("SQL DML, identity known", bash('psql $RESEARCH_DB_URL -c "DELETE FROM x"', "researcher"), True, False),
    ("foreign credential DATABASE_URL", bash('psql $DATABASE_URL -c "select 1"'), True, False),
    ("foreign credential BACKFILL_DB_URL", bash('python -c "import os; os.environ[\'BACKFILL_DB_URL\']"'), True, False),
    ("plain SELECT", bash('python research/lib/db.py "SELECT count(*) FROM super_agent_select_runs"'), False, False),
    ("platform redirect", bash(f"echo x > {PLATFORM}/README.md"), True, False),
    ("platform sed -i", bash(f"sed -i s/a/b/ {PLATFORM}/app.py"), True, False),
    ("platform git commit", bash(f"git -C {PLATFORM} commit -am x"), True, False),
    ("platform git log (read-only)", bash(f"git -C {PLATFORM} log --oneline -5"), False, False),
    ("platform grep (read-only)", bash(f"grep -n foo {PLATFORM}/services/super_agent_select_scoring.py"), False, False),
    ("force push", bash("git push --force origin master"), True, False),
    ("history rewrite", bash("git reset --hard origin/master"), True, False),
    ("rm -rf", bash("rm -rf research/data"), True, False),
    ("blob upload outside research", bash("az storage blob upload --container-name prod -f x"), True, False),
    ("blob upload to research", bash("az storage blob upload --container-name research -f x"), False, False),
    ("run platform pipeline", bash("python run_nightly_pipeline.py"), True, False),
    ("edit guard via redirect", bash("echo x > .claude/hooks/guard_bash.py"), True, False),
    ("edit guard via redirect, DESK_ADMIN", bash("echo x > .claude/hooks/guard_bash.py"), False, True),
    ("edit controller via sed -i", bash("sed -i s/a/b/ research/lib/controller.py"), True, False),
    ("normal freeze command", bash("python research/lib/freeze_dataset.py --verify research/data/manifest_v001.json"), False, False),
    ("normal controller advance", bash("python research/lib/controller.py advance Q001 DATASET_PINNED"), False, False),
]

WRITE_CASES = [
    ("credential file", write(".env.research"), True, False),
    ("credential file, even as admin", write(".env.research"), True, True),
    ("enforcement code", write(".claude/settings.json"), True, False),
    ("enforcement code, DESK_ADMIN", write(".claude/settings.json"), False, True),
    ("controller", write("research/lib/controller.py"), True, False),
    ("outside allowed prefixes", write("scripts/research_routines.sh"), True, False),
    ("outside allowed prefixes, DESK_ADMIN", write("scripts/research_routines.sh"), False, True),
    ("research/ write", write("research/questions/Q002_x/PREREG.md"), False, False),
    ("docs/ write", write("docs/SETUP_STATUS.md"), False, False),
    ("playbook/ write", write("playbook/PB-001_x.md"), False, False),
    ("research/data as data-steward", write("research/data/manifest_v002.json", "data-steward"), False, False),
    ("research/data as researcher", write("research/data/manifest_v002.json", "researcher"), True, False),
]


def main():
    fails = []
    print(f"testing {'INSTALLED' if INSTALLED else 'PROPOSED'} guards in {HOOK_DIR}\n")
    for label, payload, expect, admin in BASH_CASES:
        got, err = run("guard_bash.py", payload, admin)
        ok = got == expect
        print(f"{'pass' if ok else 'FAIL'}  bash   {label:45} blocked={got}")
        if not ok:
            fails.append((label, expect, got, err))
    print()
    for label, payload, expect, admin in WRITE_CASES:
        got, err = run("guard_write.py", payload, admin)
        ok = got == expect
        print(f"{'pass' if ok else 'FAIL'}  write  {label:45} blocked={got}")
        if not ok:
            fails.append((label, expect, got, err))
    print()
    if fails:
        print(f"{len(fails)} FAILURES:")
        for label, expect, got, err in fails:
            print(f"  {label}: expected blocked={expect}, got {got}. stderr={err}")
        sys.exit(1)
    print(f"all {len(BASH_CASES) + len(WRITE_CASES)} cases pass")


if __name__ == "__main__":
    main()
