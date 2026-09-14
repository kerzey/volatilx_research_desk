#!/usr/bin/env python
"""Test patch8 on temporary copies. Never modifies the real controller, hook or any question.

    python docs/controller_patches/test_deferred_resume.py

Part 1 exercises the patched controller on fake questions in a temp folder.
Part 2 exercises the patched guard on fake questions in a temp git repo.
Part 3 reads the REAL questions and proves: every study ever locked stays locked, and the only
questions the controller would let resume are the ones DEFERRED.md marks TRIGGER MET.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import patch_deferred_resume as P  # noqa: E402

FAILS = []


def check(name, ok, detail=""):
    print(("  ok    " if ok else "  FAIL  ") + name + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def patched_source(rel: str) -> str:
    target, pairs = next((t, p) for t, p in P.TARGETS if str(t).replace("\\", "/") == rel)
    src = (ROOT / target).read_bytes().decode("utf-8").replace("\r\n", "\n")
    return src if P.MARKER in src else P.patch_text(src, pairs)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def state(cur, history):
    return {"id": "Q", "state": cur, "history": [{"state": s, "at": "t", "by": "desk"} for s in history]}


def part1_controller():
    print("\nPart 1 — controller: the one new move out of DEFERRED")
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "research/lib").mkdir(parents=True)
        (t / "research/lib/controller.py").write_text(patched_source("research/lib/controller.py"), encoding="utf-8")
        qs = t / "research/questions"
        cases = {
            "Q900_met": state("DEFERRED", ["IDEA", "PREREG_DRAFT", "DEFERRED"]),
            "Q901_nomet": state("DEFERRED", ["IDEA", "PREREG_DRAFT", "DEFERRED"]),
            "Q902_waslocked": state("DEFERRED", ["IDEA", "PREREG_DRAFT", "PREREG_LOCKED", "DEFERRED"]),
            "Q903_met_agent": state("DEFERRED", ["IDEA", "PREREG_DRAFT", "DEFERRED"]),
            "Q904_locked": state("PREREG_LOCKED", ["IDEA", "PREREG_DRAFT", "PREREG_LOCKED"]),
            "Q905_null": state("NULL", ["IDEA", "PREREG_DRAFT", "PREREG_LOCKED", "NULL"]),
        }
        for name, st in cases.items():
            (qs / name).mkdir(parents=True)
            (qs / name / "state.json").write_text(json.dumps(st), encoding="utf-8")
        (qs / "DEFERRED.md").write_text(
            "# Deferred\n\n## Q900 / H-1 — met\n\n> **TRIGGER MET 2026-09-14 — lifted.**\n\n"
            "## Q901 / H-2 — not met\n\nStill waiting.\n\n"
            "## Q902 / H-3 — met but was locked\n\n> **TRIGGER MET**\n\n"
            "## Q903 / H-4 — met\n\n> **TRIGGER MET**\n", encoding="utf-8")

        def run(q, target, by):
            r = subprocess.run([sys.executable, "research/lib/controller.py", "advance", q, target, "--by", by],
                               cwd=t, capture_output=True, text=True)
            return r.returncode, (r.stdout + r.stderr).strip()

        rc, out = run("Q900", "PREREG_DRAFT", "desk")
        check("trigger met, never locked, --by desk -> resumes", rc == 0, out)
        st = json.loads((qs / "Q900_met/state.json").read_text())
        check("state.json now PREREG_DRAFT with the move in history",
              st["state"] == "PREREG_DRAFT" and st["history"][-1]["state"] == "PREREG_DRAFT", str(st))
        rc, out = run("Q901", "PREREG_DRAFT", "desk")
        check("no TRIGGER MET line -> refused", rc != 0 and "TRIGGER MET" in out, out)
        rc, out = run("Q902", "PREREG_DRAFT", "haci")
        check("was ever PREREG_LOCKED -> refused, even --by haci", rc != 0 and "never reopens" in out, out)
        rc, out = run("Q903", "PREREG_DRAFT", "agent")
        check("--by agent -> refused", rc != 0 and "--by desk" in out, out)
        rc, out = run("Q904", "PREREG_DRAFT", "haci")
        check("PREREG_LOCKED -> PREREG_DRAFT still illegal", rc != 0, out)
        rc, out = run("Q905", "PREREG_DRAFT", "haci")
        check("NULL stays terminal", rc != 0 and "terminal" in out, out)
        rc, out = run("Q900", "PREREG_LOCKED", "desk")
        check("ordinary next step still enforces its precondition", rc != 0 and "committed" in out, out)


def part2_guard():
    print("\nPart 2 — guard: which saved PREREGs are writable")
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        guard_path = t / "guard_write_patched.py"
        guard_path.write_text(patched_source(".claude/hooks/guard_write.py"), encoding="utf-8")
        g = load_module("guard_write_patched", guard_path)

        def git(*a):
            subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *a], cwd=t,
                           check=True, capture_output=True)

        git("init", "-q")
        layout = {
            "Q910_resumed_draft": state("PREREG_DRAFT", ["IDEA", "PREREG_DRAFT", "DEFERRED", "PREREG_DRAFT"]),
            "Q911_deferred": state("DEFERRED", ["IDEA", "PREREG_DRAFT", "DEFERRED"]),
            "Q912_pinned": state("DATASET_PINNED", ["IDEA", "PREREG_DRAFT", "PREREG_LOCKED", "DATASET_PINNED"]),
            "Q913_draft_but_waslocked": state("PREREG_DRAFT", ["PREREG_DRAFT", "PREREG_LOCKED", "PREREG_DRAFT"]),
            "Q914_no_state": None,
            "Q915_bad_state": "{not json",
        }
        for name, st in layout.items():
            d = t / "research/questions" / name
            d.mkdir(parents=True)
            (d / "PREREG.md").write_text("# prereg\n", encoding="utf-8")
            if isinstance(st, dict):
                (d / "state.json").write_text(json.dumps(st), encoding="utf-8")
            elif isinstance(st, str):
                (d / "state.json").write_text(st, encoding="utf-8")
        untracked = t / "research/questions/Q916_new"
        untracked.mkdir(parents=True)
        (untracked / "PREREG.md").write_text("# new\n", encoding="utf-8")
        git("add", "research/questions/Q91[0-5]*")
        git("commit", "-q", "-m", "fixture")

        def locked(name):
            return g.is_locked_prereg(str(t), f"research/questions/{name}/PREREG.md")

        check("resumed never-locked draft -> writable", locked("Q910_resumed_draft") is False)
        check("still DEFERRED (not yet resumed) -> locked", locked("Q911_deferred") is True)
        check("running study -> locked", locked("Q912_pinned") is True)
        check("back at PREREG_DRAFT but was once locked -> locked forever", locked("Q913_draft_but_waslocked") is True)
        check("tracked, no state.json -> locked (fail closed)", locked("Q914_no_state") is True)
        check("tracked, unreadable state.json -> locked (fail closed)", locked("Q915_bad_state") is True)
        check("new untracked PREREG -> writable (unchanged)", locked("Q916_new") is False)
        check("non-PREREG file -> not this rule (unchanged)",
              g.is_locked_prereg(str(t), "research/questions/Q912_pinned/eval.py") is False)
        check("credential rule untouched", ".env" in g.FORBIDDEN_SUBSTRINGS)


def part3_real_questions():
    print("\nPart 3 — the real questions (read-only)")
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "g.py").write_text(patched_source(".claude/hooks/guard_write.py"), encoding="utf-8")
        (t / "c.py").write_text(patched_source("research/lib/controller.py"), encoding="utf-8")
        g = load_module("g_real", t / "g.py")
        c = load_module("c_real", t / "c.py")
    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        ever_locked, still_locked, resumable = 0, 0, []
        for d in sorted((ROOT / "research/questions").glob("Q*_*")):
            sf = d / "state.json"
            if not sf.exists() or not (d / "PREREG.md").exists():
                continue
            st = json.loads(sf.read_text())
            q = d.name.split("_")[0]
            rel = f"research/questions/{d.name}/PREREG.md"
            if any(h.get("state") == "PREREG_LOCKED" for h in st.get("history", [])):
                ever_locked += 1
                still_locked += g.is_locked_prereg(str(ROOT), rel)
            if st["state"] == "DEFERRED":
                err = c.resume_deferred_error(d, st, SimpleNamespace(q=q, by="desk"))
                if err is None:
                    resumable.append(q)
                    # even a resumable question's PREREG stays locked until the controller moves it
                    check(f"{q} PREREG still locked until the controller resumes it",
                          g.is_locked_prereg(str(ROOT), rel) is True)
        check(f"all {ever_locked} studies ever locked stay locked", ever_locked > 0 and still_locked == ever_locked,
              f"{still_locked}/{ever_locked}")
        check(f"only trigger-met deferrals can resume: {resumable}", resumable == ["Q030", "Q032"], str(resumable))
    finally:
        os.chdir(cwd)


if __name__ == "__main__":
    part1_controller()
    part2_guard()
    part3_real_questions()
    print()
    if FAILS:
        print(f"{len(FAILS)} check(s) FAILED")
        sys.exit(1)
    print("all checks pass")
