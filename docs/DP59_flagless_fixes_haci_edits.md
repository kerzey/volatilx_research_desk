# DP-59 — no flags: what is left for Haci

**One thing: run the patch script.** It updates every file that still tells agents to add flags,
including the ones only a human may edit (CLAUDE.md rule 11, README.md, the brief-writer and
data-steward charters, the desk-run skill, the controller).

In a plain PowerShell or Git Bash window at the repo root (not inside Claude):

```
python docs/controller_patches/patch_no_flags.py --check
python docs/controller_patches/patch_no_flags.py
python docs/controller_patches/test_no_flags.py
```

The first line only shows what will change. The second applies it and keeps a `.bak` of every file.
The third proves it worked; it should end with `all checks pass`. Then commit.

What it does, in short, is listed at the top of `docs/controller_patches/patch_no_flags.py`.
The controller's finding path becomes
`HUMAN_APPROVED → BRIEF_WRITTEN → IMPLEMENTED → LIVE_VALIDATED → RELEASE_APPROVED`: the feature ships
live, the Data Steward grades it for 30 nights, and you approve quoting it to subscribers.

EN-002 (speed-to-target card) already shipped behind `SAS_SPEED_TO_TARGET_INTERNAL`. Turn it on and
delete the flag whenever you like; the desk will not re-brief it.
