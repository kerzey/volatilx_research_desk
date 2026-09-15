#!/usr/bin/env python
"""Test patch9 on temporary copies. Never modifies the real files.

    python docs/controller_patches/test_no_flags.py

Part 1: the patch applies cleanly to copies of the real files, and a second run is a no-op.
Part 2: no guarded file still names a flag-off or shadow state or asks for a flag.
Part 3: the patched controller walks a fake finding through the new path and refuses the wrong moves.
Part 4: the patched Python files still compile.
"""
import json
import py_compile
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(Path(__file__).resolve().parent)]
import patch_no_flags as P  # noqa: E402

FAILS = []


def check(name, ok, detail=""):
    print(("  ok    " if ok else "  FAIL  ") + name + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def copy_tree(tmp: Path):
    for rel in P.PATCHES:
        src, dst = ROOT / rel, tmp / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    (tmp / "research/questions").mkdir(parents=True, exist_ok=True)


def apply(tmp: Path, *extra):
    r = subprocess.run([sys.executable, str(ROOT / "docs/controller_patches/patch_no_flags.py"), "--root", str(tmp), *extra],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def part1(tmp):
    print("\nPart 1 — applies cleanly, then is a no-op")
    pending, problems, _ = P.plan(ROOT)
    if not pending and not problems:
        # The real repo is already patched, so the copies are too: there is nothing left to apply.
        rc, out = apply(tmp)
        check("real repo already patched; a run on the copies is a no-op",
              rc == 0 and "already fully applied" in out, out)
        return
    rc, out = apply(tmp, "--check")
    check("--check succeeds and changes nothing", rc == 0 and "would change" in out
          and (tmp / "CLAUDE.md").read_bytes() == (ROOT / "CLAUDE.md").read_bytes(), out)
    rc, out = apply(tmp)
    check("apply succeeds", rc == 0 and "applied" in out, out)
    check(".bak written for CLAUDE.md", (tmp / "CLAUDE.md.bak").exists())
    rc, out = apply(tmp)
    check("second run: nothing to do", rc == 0 and "already fully applied" in out, out)


def part2(tmp):
    print("\nPart 2 — no file still asks for flags or names the old states")
    for rel in P.PATCHES:
        text = (tmp / rel).read_bytes().decode("utf-8")
        for bad in ("IMPLEMENTED_FLAG_OFF", "SHADOW_VALIDATED", "SHADOW.json", "Inertness proof", "config flag that gates it",
                    "Prove inert, ship dark", "flip the flag", "one command / one flag", "flag-off internal tool"):
            if bad in text:
                check(f"{rel} no longer contains {bad!r}", False)
    check("scan complete", True)
    bw = (tmp / ".claude/agents/brief-writer.md").read_text(encoding="utf-8")
    check("brief-writer names DP-59 and After-deploy check", "DP-59" in bw and "After-deploy check" in bw)
    cl = (tmp / "CLAUDE.md").read_text(encoding="utf-8")
    check("CLAUDE.md rule 11 is 'Ship, then verify here'", "Ship, then verify here" in cl)
    check("CLAUDE.md rule 10 untouched", "Only the last supports a subscriber-facing claim" in cl)
    check("CLAUDE.md FMP line untouched", ("FMP_API_KEY" in cl) == ("FMP_API_KEY" in (ROOT / "CLAUDE.md").read_text(encoding="utf-8")))


def part3(tmp):
    print("\nPart 3 — the controller's new finding path")
    q = tmp / "research/questions/Q999_fake_finding"
    q.mkdir(parents=True)
    (q / "state.json").write_text(json.dumps({
        "id": "Q999", "state": "LEDGERED", "historical_verdict": "HISTORICALLY_CONFIRMED",
        "history": [{"state": "LEDGERED", "at": "t", "by": "reporter"}]}), encoding="utf-8")

    def adv(state, by, note=None):
        cmd = [sys.executable, "research/lib/controller.py", "advance", "Q999", state, "--by", by]
        if note:
            cmd += ["--note", note]
        r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr).strip()

    rc, out = adv("HUMAN_APPROVED", "haci")
    check("HUMAN_APPROVED --by haci", rc == 0, out)
    (q / "IMPLEMENTATION_BRIEF.md").write_text("# brief\n## Inertness proof\n## Rollback\n", encoding="utf-8")
    rc, out = adv("BRIEF_WRITTEN", "brief-writer")
    check("old-style brief (Inertness proof, no After-deploy check) refused", rc != 0, out)
    (q / "IMPLEMENTATION_BRIEF.md").write_text("# brief\n## After-deploy check\n## Rollback\n", encoding="utf-8")
    rc, out = adv("BRIEF_WRITTEN", "brief-writer")
    check("new-style brief accepted", rc == 0, out)
    rc, out = adv("IMPLEMENTED_FLAG_OFF", "haci", "PR #1 sha abc")
    check("old state IMPLEMENTED_FLAG_OFF is unknown", rc != 0 and "unknown state" in out, out)
    rc, out = adv("IMPLEMENTED", "desk", "PR #1 sha abc")
    check("IMPLEMENTED --by desk refused", rc != 0, out)
    rc, out = adv("IMPLEMENTED", "haci")
    check("IMPLEMENTED without PR/sha note refused", rc != 0 and "deployed sha" in out, out)
    rc, out = adv("IMPLEMENTED", "haci", "PR #1 sha abc123")
    check("IMPLEMENTED --by haci with PR and sha", rc == 0, out)
    rc, out = adv("LIVE_VALIDATED", "data-steward")
    check("LIVE_VALIDATED without results/LIVE.json refused", rc != 0 and "LIVE.json" in out, out)
    (q / "results").mkdir()
    (q / "results/LIVE.json").write_text(json.dumps({"n_nights": 12, "mean_alpha": 0.2}), encoding="utf-8")
    rc, out = adv("LIVE_VALIDATED", "data-steward")
    check("LIVE_VALIDATED with 12 live nights refused", rc != 0 and "live nights" in out, out)
    (q / "results/LIVE.json").write_text(json.dumps({"n_nights": 31, "mean_alpha": 0.2}), encoding="utf-8")
    rc, out = adv("LIVE_VALIDATED", "data-steward")
    st = json.loads((q / "state.json").read_text(encoding="utf-8"))
    check("LIVE_VALIDATED at 31 nights sets PROSPECTIVELY_CONFIRMED",
          rc == 0 and st.get("prospective_verdict") == "PROSPECTIVELY_CONFIRMED", out)
    rc, out = adv("RELEASE_APPROVED", "desk")
    check("RELEASE_APPROVED --by desk refused", rc != 0, out)
    rc, out = adv("RELEASE_APPROVED", "haci")
    check("RELEASE_APPROVED --by haci", rc == 0, out)


def part4(tmp):
    print("\nPart 4 — patched Python compiles")
    for rel in ("research/lib/controller.py", "research/lib/desk_queue.py", "research/lib/board.py"):
        try:
            py_compile.compile(str(tmp / rel), doraise=True)
            check(f"{rel} compiles", True)
        except py_compile.PyCompileError as e:
            check(f"{rel} compiles", False, str(e))


def part5():
    print("\nPart 5 — the real repo (read-only)")
    stuck = [sf.parent.name for sf in (ROOT / "research/questions").glob("Q*/state.json")
             if json.loads(sf.read_text(encoding="utf-8")).get("state") in P.OLD_STATES]
    check("no real question sits on a removed state", not stuck, str(stuck))
    changes, problems, _ = P.plan(ROOT)
    check("every expected text is present in the real files (or already patched)", not problems, "; ".join(problems))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        copy_tree(tmp)
        part1(tmp)
        part2(tmp)
        part3(tmp)
        part4(tmp)
    part5()
    print()
    if FAILS:
        print(f"{len(FAILS)} check(s) FAILED")
        sys.exit(1)
    print("all checks pass")
