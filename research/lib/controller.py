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
         "REDTEAM_SIGNED", "LEDGERED", "HUMAN_APPROVED", "BRIEF_WRITTEN", "IMPLEMENTED",
         "LIVE_VALIDATED", "RELEASE_APPROVED"]  # patch9 (2026-09-15, DP-59): no flag-off / shadow states
TERMINAL = {"NULL", "INCONCLUSIVE", "REJECTED", "DEFERRED"}
HUMAN_ONLY = {"HUMAN_APPROVED", "IMPLEMENTED", "RELEASE_APPROVED"}


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


def prereg_manifests(d):
    """Every manifest named in a PREREG header line "**Manifest…:** <path> …".
    Accepts "**Manifest:**" and qualified forms such as "**Manifest (selections):**"."""
    import re
    pat = re.compile(r"^\*\*Manifest[^*]*:\*\*\s*(\S+)")
    paths = [m.group(1) for line in (d / "PREREG.md").read_text(encoding="utf-8").splitlines()
             if (m := pat.match(line))]
    # Desk maintenance 2026-09-14: optional manifests may explicitly say "none".
    # Ignore decoration only when identifying placeholders; retain real tokens so
    # pre_DATASET_PINNED fails closed instead of silently losing a required input.
    paths = [p for p in paths if p.strip("*`").lower() not in {"none", "n/a", "tbd", "—", "–", "-"}]
    # patch6: a locked PREREG whose header names no manifest *file* (its freezes are built at the
    # decision date — Q010) lists them in <qdir>/manifests.json, written by the Data Steward.
    # Only when none of the header paths exists; a misspelled header path still fails loudly.
    if paths and not any(Path(p).exists() for p in paths):
        mj = d / "manifests.json"
        if mj.exists():
            return json.loads(mj.read_text(encoding="utf-8"))
    return paths


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
    if "After-deploy check" not in f.read_text() or "Rollback" not in f.read_text():
        return "brief lacks required sections"
    st["brief_sha256"] = sha(f)
    return None


def pre_IMPLEMENTED(d, st, args):
    if args.by != "haci":
        return "only Haci records that the brief was implemented in the platform repo"
    if not args.note or "PR" not in args.note or "sha" not in args.note.lower():
        return "--note must carry the PR link and the deployed sha"
    return None


def pre_LIVE_VALIDATED(d, st, args):
    f = d / "results" / "LIVE.json"
    if not f.exists():
        return "results/LIVE.json missing (steward writes it after ≥30 live nights)"
    s = json.loads(f.read_text())
    if s.get("n_nights", 0) < 30:
        return f"only {s.get('n_nights')} live nights; need ≥ 30"
    if s.get("mean_alpha", -1) <= 0:
        return "live mean_alpha not > 0 — prospective confirmation failed"
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


def resume_deferred_error(d, st, args):
    # patch8 (2026-09-14, Q030/Q032): the one way out of DEFERRED. A parked question may go back to
    # PREREG_DRAFT only if it was never locked and DEFERRED.md records its trigger as met.
    if args.by not in ("desk", "haci"):
        return "requires --by desk or --by haci"
    if any(h.get("state") == "PREREG_LOCKED" for h in st.get("history", [])):
        return "this question was locked once; a locked question never reopens (DP-22)"
    f = Path("research/questions/DEFERRED.md")
    text = f.read_text(encoding="utf-8") if f.exists() else ""
    section, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].split()[:1] == [args.q]
            continue
        if inside:
            section.append(line)
    if not any("TRIGGER MET" in line for line in section):
        return f"no 'TRIGGER MET' line under '## {args.q}' in DEFERRED.md"
    return None


def cmd_advance(args):
    d = qdir(args.q)
    st = load(d) or sys.exit("run init first")
    cur, nxt = st["state"], args.state
    if cur == "DEFERRED" and nxt == "PREREG_DRAFT":   # patch8 (2026-09-14, Q030/Q032)
        err = resume_deferred_error(d, st, args)
        if err:
            sys.exit(f"cannot resume {args.q} from DEFERRED: {err}")
        st["state"] = nxt
        st["history"].append({"state": nxt, "at": now(), "by": args.by, "note": args.note})
        save(d, st)
        print(f"{args.q}: {cur} -> {nxt} (deferral lifted)")
        return
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
