# Controller patches — apply by hand

Enforcement code (`research/lib/controller.py`, validators, freeze, `.claude/`) is edited by a
human outside the desk (CLAUDE.md rule 15). The desk can only prepare the change and a test.
Each patch here is a small idempotent Python script that edits the target in place, writes a
`.bak`, and refuses to run if the target has drifted from what it expects.

## patch7 — `prereg_manifests()` skips non-path header values (2026-09-14)

**Symptom.** `python research/lib/controller.py advance Q028 DATASET_PINNED --by desk` fails with
`precondition failed for DATASET_PINNED: manifest **none not found`. Q028 has been stuck at
`PREREG_LOCKED` since 2026-09-14 for this reason (see its `schedule.json` note).

**Cause.** Q028's PREREG header says `**Manifest (prices):** **none — not used.**` because the
question reads no price bar. The parser's regex takes the first token after the colon as a path
and gets `**none`. The PREREG is hash-locked, so the header cannot be reworded; the parser has to
learn that "none" is not a path.

**Fix.** After collecting header tokens, drop any that start with `*` or read `none`, `n/a`,
`tbd` or a dash. Everything else is unchanged: a misspelled real path still fails loudly, and a
header with no real path still routes to `pin_at_decision` (step D of `/desk-run`).

## Apply

From the repo root, in a plain Git Bash or PowerShell window (not inside a desk session — the
desk's own guard blocks writes to `research/lib/controller.py`; `./scripts/start_desk.sh --admin`
would also lift it, but a plain terminal is simpler):

```bash
python docs/controller_patches/patch_manifest_header.py
python docs/controller_patches/test_manifest_header.py
```

The second line must end with `all checks pass (... questions; Q028 -> research/data/manifest_v001.json)`.
It sweeps every question's PREREG header through the patched parser and, using the `.bak` the
patcher left behind, proves no question that resolved to real manifests before resolves
differently after.

Then finish the pin and commit, in a desk session or the same terminal:

```bash
python research/lib/controller.py advance Q028 DATASET_PINNED --by desk
git add research/lib/controller.py research/questions/Q028_layer_signal_independence/state.json docs/controller_patches
git commit -m "controller patch7: manifest header skips non-path values; Q028 pinned — 2026-09-14"
```

Roll back: `cp research/lib/controller.py.bak research/lib/controller.py`.
