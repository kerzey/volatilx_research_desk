#!/usr/bin/env python
"""Test for patch7: prereg_manifests() must skip non-path header values.

Runs prereg_manifests() from the given controller file over every research/questions/Q*/
directory, prints what each header resolves to, and asserts:

  1. Q028 resolves to exactly ["research/data/manifest_v001.json"] (the "**none" token is gone).
  2. No question that resolved to real paths before the patch resolves differently after it
     (checked against a snapshot the script takes from the *unpatched* .bak file when present).
  3. No resolved token starts with "*" or equals "none".

Usage (from the repo root):

    python docs/controller_patches/test_manifest_header.py                     # installed controller
    python docs/controller_patches/test_manifest_header.py --target <path.py>  # a copy
"""
import argparse
import importlib.machinery
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_TARGET = REPO / "research" / "lib" / "controller.py"
QDIRS = sorted(p for p in (REPO / "research" / "questions").iterdir() if p.is_dir() and p.name.startswith("Q"))


def load(path: Path, name: str):
    # explicit SourceFileLoader so a ".bak" suffix imports too (spec_from_file_location rejects it)
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)               # controller.py has an __main__ guard; import is inert
    return mod


def resolve(mod) -> dict:
    out = {}
    for q in QDIRS:
        if not (q / "PREREG.md").exists():
            continue
        try:
            out[q.name] = list(mod.prereg_manifests(q))
        except Exception as e:                # noqa: BLE001 -- report, don't crash the sweep
            out[q.name] = [f"<error: {e}>"]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    args = ap.parse_args()

    import os
    os.chdir(REPO)                            # prereg_manifests() tests Path(p).exists() relative to the repo root
    patched = load(args.target, "controller_patched")
    after = resolve(patched)

    before = None
    bak = args.target.with_suffix(args.target.suffix + ".bak")
    if bak.exists():
        before = resolve(load(bak, "controller_before"))

    failures = []
    for q, paths in after.items():
        tag = ""
        if before is not None and q in before and before[q] != paths:
            good_before = [p for p in before[q] if not p.startswith("*") and p.lower() != "none"]
            if good_before != paths:
                failures.append(f"{q}: real paths changed {before[q]} -> {paths}")
                tag = "  CHANGED"
            else:
                tag = "  (non-path token dropped)"
        for p in paths:
            if p.startswith("*") or p.lower() == "none":
                failures.append(f"{q}: non-path token survived: {p}")
        print(f"{q:45s} {paths}{tag}")

    want = ["research/data/manifest_v001.json"]
    if after.get("Q028_layer_signal_independence") != want:
        failures.append(f"Q028 resolved to {after.get('Q028_layer_signal_independence')}, want {want}")

    print()
    if failures:
        for f in failures:
            print("FAIL ", f)
        return 1
    print(f"all checks pass ({len(after)} questions; Q028 -> {want[0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
