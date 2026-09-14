#!/usr/bin/env python
"""patch7 — controller.prereg_manifests(): ignore header values that are not paths.

Bug (Q028, 2026-09-14): the PREREG header line

    **Manifest (prices):** **none — not used.**

is read by the "**Manifest…:** <path>" regex as a manifest path "**none", and the
DATASET_PINNED precondition fails with "manifest **none not found". The PREREG is hash-locked
(DP-22), so the header cannot be reworded; the parser has to skip non-path values.

The patch keeps only tokens that look like a file path. A misspelled *real* path still fails
loudly in pre_DATASET_PINNED, exactly as before. A header whose only value is "none" yields no
manifest, which the desk already handles via schedule.json "pin_at_decision" (step D).

Usage (from the repo root, in a plain terminal — not from inside a desk session):

    python docs/controller_patches/patch_manifest_header.py            # apply
    python docs/controller_patches/patch_manifest_header.py --check    # report only
    python docs/controller_patches/patch_manifest_header.py --target <copy-of-controller.py>

Idempotent: re-running on a patched file reports "already applied" and changes nothing.
Writes <target>.bak before modifying. Roll back by copying the .bak file back.
"""
import argparse
import shutil
import sys
from pathlib import Path

DEFAULT_TARGET = Path("research/lib/controller.py")

OLD = (
    '    paths = [m.group(1) for line in (d / "PREREG.md").read_text(encoding="utf-8").splitlines()\n'
    '             if (m := pat.match(line))]\n'
)

NEW = OLD + (
    '    # patch7 (2026-09-14, Q028): a header value that is not a path -- "**none -- not used.**",\n'
    '    # "none", "n/a", "tbd", a dash -- names no manifest and must not fail the pin. Keep only\n'
    '    # tokens that look like a file path; a misspelled real path still fails loudly below.\n'
    '    _not_a_path = {"none", "n/a", "na", "tbd", "-", "\\u2014", "\\u2013"}\n'
    '    paths = [p for p in paths\n'
    '             if not p.startswith("*") and p.strip("*_`.,;:").lower() not in _not_a_path]\n'
)

MARKER = "# patch7 (2026-09-14, Q028)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--target", type=Path, default=DEFAULT_TARGET,
                    help=f"file to patch (default {DEFAULT_TARGET})")
    ap.add_argument("--check", action="store_true", help="report status, change nothing")
    args = ap.parse_args()

    target: Path = args.target
    if not target.exists():
        print(f"ERROR: {target} not found (run from the repo root)", file=sys.stderr)
        return 2
    raw = target.read_bytes()
    eol = "\r\n" if b"\r\n" in raw else "\n"          # preserve the file's line endings
    src = raw.decode("utf-8").replace("\r\n", "\n")

    if MARKER in src:
        print(f"already applied: {target}")
        return 0
    if src.count(OLD) != 1:
        print(f"ERROR: expected exactly one match of the original block in {target}, "
              f"found {src.count(OLD)} -- controller.py has changed; patch by hand", file=sys.stderr)
        return 3
    if args.check:
        print(f"not applied (would patch): {target}")
        return 1

    bak = target.with_suffix(target.suffix + ".bak")
    shutil.copyfile(target, bak)
    patched = src.replace(OLD, NEW, 1).replace("\n", eol)
    target.write_bytes(patched.encode("utf-8"))
    print(f"patched: {target}  (backup: {bak})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
