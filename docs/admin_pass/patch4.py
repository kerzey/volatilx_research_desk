#!/usr/bin/env python3
"""Fourth maintenance pass — patch definitions, testable in memory before anything is written.

    python docs/admin_pass/patch4.py --check    # apply in memory, run the checks, write nothing
    python docs/admin_pass/patch4.py --apply    # write the patched files (Haci; enforcement code)

1. controller.py / validators.py read ONE manifest line, spelled exactly "**Manifest:**".
   The R1 PREREGs (Q002–Q006) name two manifests, "**Manifest (selections):**" and
   "**Manifest (prices/outcomes):**", so DATASET_PINNED fails with "no manifest line in
   PREREG" and validators V2/V9 fail the same way. The patch reads every "**Manifest…:**"
   header line, verifies each checksum, and pins all of them. "**Manifest:**" still works
   (Q001-style PREREGs are unaffected). V9's lineage check learns that a price manifest
   carries base_manifest_sha256 rather than scoring_versions_present.

2. .claude/agents/brief-writer.md — the pasted fix-brief section:
   - sat inside an unclosed ``` fence, so the agent would read it as a quoted example rather
     than as instructions;
   - was cut off mid-sentence ("records the PR / and");
   - came after an unconditional "reads HUMAN_APPROVED. If not, stop." — which would make the
     agent refuse every fix brief, since platform issues have no question id.
"""
import argparse
import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTROLLER = ROOT / "research/lib/controller.py"
VALIDATORS = ROOT / "research/lib/validators.py"
BRIEF = ROOT / ".claude/agents/brief-writer.md"

MANIFEST_HELPER = '''def prereg_manifests(d):
    """Every manifest named in a PREREG header line "**Manifest…:** <path> …".
    Accepts "**Manifest:**" and qualified forms such as "**Manifest (selections):**"."""
    import re
    pat = re.compile(r"^\\*\\*Manifest[^*]*:\\*\\*\\s*(\\S+)")
    return [m.group(1) for line in (d / "PREREG.md").read_text(encoding="utf-8").splitlines()
            if (m := pat.match(line))]
'''

OLD_PINNED = '''def pre_DATASET_PINNED(d, st, args):
    for line in (d / "PREREG.md").read_text().splitlines():
        if line.startswith("**Manifest:**"):
            m = Path(line.split("**Manifest:**")[1].split()[0])
            if not m.exists():
                return f"manifest {m} not found"
            r = subprocess.run([sys.executable, "research/lib/freeze_dataset.py", "--verify", str(m)], capture_output=True)
            if r.returncode != 0:
                return "manifest checksum verify failed"
            st["manifest"] = str(m)
            st["manifest_sha256"] = sha(m)
            return None
    return "no manifest line in PREREG"
'''

NEW_PINNED = MANIFEST_HELPER + '''

def pre_DATASET_PINNED(d, st, args):
    paths = prereg_manifests(d)
    if not paths:
        return "no manifest line in PREREG"
    pinned = {}
    for p in paths:
        m = Path(p)
        if not m.exists():
            return f"manifest {m} not found"
        r = subprocess.run([sys.executable, "research/lib/freeze_dataset.py", "--verify", str(m)], capture_output=True)
        if r.returncode != 0:
            return f"manifest checksum verify failed: {m}"
        pinned[p] = sha(m)
    st["manifest"] = paths[0]                 # kept for older tooling
    st["manifest_sha256"] = pinned[paths[0]]
    st["manifests"] = pinned                  # every manifest the PREREG names
    return None
'''

OLD_V2 = '''def v2_manifest_verified(qdir):
    # manifest path is parsed from PREREG header line "**Manifest:** research/data/manifest_vNNN.json"
    for line in (qdir / "PREREG.md").read_text().splitlines():
        if line.startswith("**Manifest:**"):
            path = line.split("**Manifest:**")[1].split()[0]
            r = subprocess.run([sys.executable, "research/lib/freeze_dataset.py", "--verify", path])
            return r.returncode == 0, f"manifest {path} checksums"
    return False, "manifest line missing in PREREG"
'''

NEW_V2 = MANIFEST_HELPER + '''

def v2_manifest_verified(qdir):
    # every manifest named in a PREREG header line "**Manifest…:** research/data/<file>.json"
    paths = prereg_manifests(qdir)
    if not paths:
        return False, "manifest line missing in PREREG"
    bad = [p for p in paths
           if subprocess.run([sys.executable, "research/lib/freeze_dataset.py", "--verify", p]).returncode != 0]
    return not bad, (f"checksum verify failed: {bad}" if bad else f"checksums OK: {paths}")
'''

OLD_V9 = '''def v9_lineage_present(qdir):
    for line in (qdir / "PREREG.md").read_text().splitlines():
        if line.startswith("**Manifest:**"):
            m = json.loads(Path(line.split("**Manifest:**")[1].split()[0]).read_text())
            missing = [k for k in ("code_git_sha", "scoring_versions_present") if k not in m]
            return not missing, f"manifest lineage missing: {missing}" if missing else "lineage present"
    return False, "no manifest"
'''

NEW_V9 = '''def v9_lineage_present(qdir):
    paths = prereg_manifests(qdir)
    if not paths:
        return False, "no manifest"
    missing = {}
    for p in paths:
        m = json.loads(Path(p).read_text())
        # a price manifest (freeze_prices.py) is keyed to a base SAS manifest instead of scoring versions
        need = ("code_git_sha", "base_manifest_sha256") if "base_manifest" in m else ("code_git_sha", "scoring_versions_present")
        gap = [k for k in need if k not in m]
        if gap:
            missing[p] = gap
    return not missing, (f"manifest lineage missing: {missing}" if missing else f"lineage present in {len(paths)} manifest(s)")
'''

BRIEF_OLD_PRECOND = "Preconditions: `python research/lib/controller.py show QNNN` reads HUMAN_APPROVED. If not, stop."
BRIEF_NEW_PRECOND = ("Preconditions for a research finding: `python research/lib/controller.py show QNNN` reads\n"
                     "HUMAN_APPROVED. If not, stop. Fix briefs for platform issues have their own precondition —\n"
                     "see \"Fix briefs\" at the end.")
BRIEF_OLD_DESC = "Never edits platform code."
BRIEF_NEW_DESC = ("Also writes short fix briefs for platform issues Haci marked fix in research/PLATFORM_ISSUES.md "
                  "(invoke as `fix-brief PI-NNN`). Never edits platform code.")
BRIEF_TAIL = "and SHA in the register, and the Data Steward confirms the data changed on the next freeze.\n"


def _swap(src, old, new, label):
    if new.strip() in src:
        return src, f"{label}: already patched"
    if old not in src:
        sys.exit(f"{label}: expected text not found — file changed since the patch was written; stopping")
    return src.replace(old, new, 1), f"{label}: patched"


def _read(p):
    raw = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    return raw.replace("\r\n", "\n"), crlf


def _write(p, text, crlf):
    p.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def patch_controller(src):
    return _swap(src, OLD_PINNED, NEW_PINNED, "controller.pre_DATASET_PINNED")


def patch_validators(src):
    src, m1 = _swap(src, OLD_V2, NEW_V2, "validators.v2_manifest_verified")
    src, m2 = _swap(src, OLD_V9, NEW_V9, "validators.v9_lineage_present")
    return src, f"{m1}; {m2}"


def patch_brief(src):
    notes = []
    if BRIEF_NEW_PRECOND.splitlines()[0] not in src:
        if BRIEF_OLD_PRECOND not in src:
            sys.exit("brief-writer: precondition line not found; stopping")
        src = src.replace(BRIEF_OLD_PRECOND, BRIEF_NEW_PRECOND, 1)
        notes.append("precondition scoped to research findings")
    if "(invoke as `fix-brief PI-NNN`)" not in src:
        src = src.replace(BRIEF_OLD_DESC, BRIEF_NEW_DESC, 1)
        notes.append("description mentions fix briefs")
    lines = src.split("\n")
    fence = [i for i, l in enumerate(lines) if l.strip() == "```"
             and i + 1 < len(lines) and lines[i + 1].startswith("## Fix briefs")]
    if fence:
        del lines[fence[0]]
        notes.append("removed the unclosed ``` fence")
    src = "\n".join(lines).rstrip()
    if src.endswith("records the PR\nand"):
        src = src[:-len("and")] + BRIEF_TAIL
        notes.append("completed the cut-off last sentence")
    elif not src.endswith("\n"):
        src += "\n"
    # a stray closing fence at the very end would re-open the problem
    if src.rstrip().endswith("```"):
        src = src.rstrip()[:-3].rstrip() + "\n"
        notes.append("removed trailing fence")
    return src, "brief-writer: " + (", ".join(notes) if notes else "already patched")


def _load(name, source, path):
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    exec(compile(source, str(path), "exec"), mod.__dict__)
    return mod


def check(ctrl_src, val_src, brief_src):
    """Exercise the patched code on the real question directories without writing anything."""
    import os
    os.chdir(ROOT)
    ctrl = _load("controller_patched", ctrl_src, CONTROLLER)
    val = _load("validators_patched", val_src, VALIDATORS)
    ok = True
    qs = sorted(Path("research/questions").glob("Q00*_*"))
    for q in qs:
        names = ctrl.prereg_manifests(q)
        st = {}
        err = ctrl.pre_DATASET_PINNED(q, st, None)
        v2 = val.v2_manifest_verified(q)
        v9 = val.v9_lineage_present(q)
        good = err is None and v2[0] and v9[0]
        ok &= good
        print(f"{'OK ' if good else 'BAD'} {q.name:28} manifests={len(names)} pin={'ok' if err is None else err} "
              f"V2={'pass' if v2[0] else 'FAIL'} V9={'pass' if v9[0] else 'FAIL: ' + v9[1]}")
    b_ok = ("```" not in brief_src.split("## Fix briefs")[0].splitlines()[-2:]
            and brief_src.rstrip().endswith("next freeze.")
            and "Fix briefs for platform issues have their own precondition" in brief_src)
    print(f"{'OK ' if b_ok else 'BAD'} brief-writer.md: fence removed, ending complete, precondition scoped")
    return ok and b_ok


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    (c_src, c_crlf), (v_src, v_crlf), (b_src, b_crlf) = _read(CONTROLLER), _read(VALIDATORS), _read(BRIEF)
    c_new, m1 = patch_controller(c_src)
    v_new, m2 = patch_validators(v_src)
    b_new, m3 = patch_brief(b_src)
    for m in (m1, m2, m3):
        print(m)
    print()
    if not check(c_new, v_new, b_new):
        sys.exit("\nchecks FAILED — nothing written")
    if a.apply:
        _write(CONTROLLER, c_new, c_crlf)
        _write(VALIDATORS, v_new, v_crlf)
        _write(BRIEF, b_new, b_crlf)
        print("\nwritten: research/lib/controller.py, research/lib/validators.py, .claude/agents/brief-writer.md")
    else:
        print("\n--check only: nothing written")


if __name__ == "__main__":
    main()
