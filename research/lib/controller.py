#!/usr/bin/env python3
"""Deterministic Research Controller — the state machine that agents cannot argue with.

State lives in research/questions/QNNN_*/state.json. Markdown is for humans; this is authoritative.

Usage:
  python research/lib/controller.py init Q001
  python research/lib/controller.py advance Q001 <STATE> [--by haci|red-team|...] [--note "..."]
  python research/lib/controller.py show Q001

Each transition checks its precondition (hashes, files, sign-offs). Illegal transitions exit 1.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ORDER = ["IDEA", "PREREG_DRAFT", "PREREG_LOCKED", "DATASET_PINNED", "EVALUATED", "VALIDATED",
         "REDTEAM_SIGNED", "LEDGERED", "HUMAN_APPROVED", "BRIEF_WRITTEN", "IMPLEMENTED_FLAG_OFF",
         "SHADOW_VALIDATED", "RELEASE_APPROVED"]
TERMINAL = {"NULL", "INCONCLUSIVE", "REJECTED", "DEFERRED"}
HUMAN_ONLY = {"HUMAN_APPROVED", "IMPLEMENTED_FLAG_OFF", "RELEASE_APPROVED"}


def qdir(q):
    d = next(Path("research/questions").glob(f"{q}_*"), None)
    if not d:
        sys.exit(f"no question dir for {q}")
    return d


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout.strip()


def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(d):
    f = d / "state.json"
    return json.loads(f.read_text()) if f.exists() else None


def save(d, st):
    (d / "state.json").write_text(json.dumps(st, indent=2))


# --- preconditions -------------------------------------------------------------------
def pre_PREREG_LOCKED(d, st, args):
    f = d / "PREREG.md"
    h = git("log", "-1", "--format=%H", "--", str(f))
    dirty = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", str(f)]).returncode != 0
    if not h or dirty:
        return "PREREG.md must be committed and clean"
    st["prereg_commit"] = h
    st["prereg_sha256"] = sha(f)
    return None


def pre_DATASET_PINNED(d, st, args):
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


def pre_EVALUATED(d, st, args):
    if sha(d / "PREREG.md") != st.get("prereg_sha256"):
        return "PREREG.md changed after lock — illegal"
    for f in ("eval.py", "results/run_summary.json", "results/nightly.csv", "results/SUMMARY.md"):
        if not (d / f).exists():
            return f"missing {f}"
    st["eval_sha256"] = sha(d / "eval.py")
    st["summary_sha256"] = sha(d / "results" / "run_summary.json")
    return None


def pre_VALIDATED(d, st, args):
    r = subprocess.run([sys.executable, "research/lib/validators.py", "--question", st["id"]])
    return None if r.returncode == 0 else "validators FAIL — see results/VALIDATORS.json"


def pre_REDTEAM_SIGNED(d, st, args):
    f = d / "results" / "REDTEAM.md"
    if not f.exists():
        return "results/REDTEAM.md missing"
    last = [l for l in f.read_text().splitlines() if l.strip()][-1]
    if not last.startswith("SIGN-OFF:"):
        return f"REDTEAM.md must end with SIGN-OFF: … (got: {last[:60]})"
    if sha(d / "results" / "run_summary.json") != st.get("summary_sha256"):
        return "results changed after evaluation — re-run VALIDATED"
    st["historical_verdict"] = last.split("SIGN-OFF:")[1].strip()
    return None


def pre_LEDGERED(d, st, args):
    led = Path("research/LEDGER.md").read_text()
    return None if f"| {st['id']} |" in led else "LEDGER.md has no row for this question"


def pre_HUMAN_APPROVED(d, st, args):
    if args.by != "haci":
        return "only --by haci may approve"
    if st.get("historical_verdict") != "HISTORICALLY_CONFIRMED":
        return "only HISTORICALLY_CONFIRMED questions can be approved for implementation"
    return None


def pre_BRIEF_WRITTEN(d, st, args):
    f = d / "IMPLEMENTATION_BRIEF.md"
    if not f.exists():
        return "IMPLEMENTATION_BRIEF.md missing"
    if "Inertness proof" not in f.read_text() or "Rollback" not in f.read_text():
        return "brief lacks required sections"
    st["brief_sha256"] = sha(f)
    return None


def pre_IMPLEMENTED_FLAG_OFF(d, st, args):
    if args.by != "haci":
        return "only Haci records that the brief was implemented in the platform repo"
    if not args.note or "PR" not in args.note or "sha" not in args.note.lower():
        return "--note must carry the PR link and the before/after dry-run hashes"
    return None


def pre_SHADOW_VALIDATED(d, st, args):
    f = d / "results" / "SHADOW.json"
    if not f.exists():
        return "results/SHADOW.json missing (steward writes it after ≥30 shadow nights)"
    s = json.loads(f.read_text())
    if s.get("n_nights", 0) < 30:
        return f"only {s.get('n_nights')} shadow nights; need ≥ 30"
    if s.get("mean_alpha", -1) <= 0:
        return "shadow mean_alpha not > 0 — prospective confirmation failed"
    st["prospective_verdict"] = "PROSPECTIVELY_CONFIRMED"
    return None


def pre_RELEASE_APPROVED(d, st, args):
    return None if args.by == "haci" else "only --by haci may approve release"


PRE = {k[4:]: v for k, v in globals().items() if k.startswith("pre_")}


# --- commands --------------------------------------------------------------------------
def cmd_init(args):
    d = qdir(args.q)
    if load(d):
        sys.exit("state.json exists")
    save(d, {"id": args.q, "state": "IDEA", "history": [{"state": "IDEA", "at": now(), "by": args.by}]})
    print(f"{args.q}: IDEA")


def now():
    return datetime.now(timezone.utc).isoformat()


def cmd_advance(args):
    d = qdir(args.q)
    st = load(d) or sys.exit("run init first")
    cur, nxt = st["state"], args.state
    if nxt in TERMINAL:
        st["state"] = nxt
    else:
        if nxt not in ORDER:
            sys.exit(f"unknown state {nxt}")
        if cur in TERMINAL:
            sys.exit(f"{cur} is terminal")
        if ORDER.index(nxt) != ORDER.index(cur) + 1:
            sys.exit(f"illegal transition {cur} -> {nxt}; next allowed is {ORDER[ORDER.index(cur)+1]}")
        if nxt in HUMAN_ONLY and args.by != "haci":
            sys.exit(f"{nxt} requires --by haci")
        err = PRE.get(nxt, lambda *a: None)(d, st, args)
        if err:
            sys.exit(f"precondition failed for {nxt}: {err}")
        st["state"] = nxt
    st["history"].append({"state": nxt, "at": now(), "by": args.by, "note": args.note})
    save(d, st)
    print(f"{args.q}: {cur} -> {nxt}")


def cmd_show(args):
    print(json.dumps(load(qdir(args.q)), indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "advance", "show"):
        s = sub.add_parser(name); s.add_argument("q")
        if name == "advance":
            s.add_argument("state")
        s.add_argument("--by", default="agent"); s.add_argument("--note", default="")
    a = ap.parse_args()
    {"init": cmd_init, "advance": cmd_advance, "show": cmd_show}[a.cmd](a)
