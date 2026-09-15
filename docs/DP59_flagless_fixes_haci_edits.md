# DP-59 — fixes and builds ship without flags: the two human-owned files Haci should align

**2026-09-15.** Haci: "Every brief wants to create a flag… I don't want it, it's hard to keep. Fix is
fix. We will check here if it is working fine. I am the only user in the platform."

The desk recorded this as **DP-59** in `research/DECISION_POLICY.md` and updated the preambles of
`research/PLATFORM_ISSUES.md` and `research/ENHANCEMENTS.md`. The open briefs PI-020 and EN-019 were
rewritten flag-less. Two files the desk cannot write still describe the old flag ceremony; the edits
below make them agree. Both are optional — DP-59 already overrides the charter for PI/EN briefs — but
without them each new brief-writer run will argue with the policy before complying.

## 1. `.claude/agents/brief-writer.md`

Finding briefs (`QNNN`) section, items 2–5 and 8, currently:

```
2. **Change** — precisely what behaviour is added, and the config flag that gates it
   (follow the repo's existing flag conventions; default OFF). Name the runtime setting keys.
3. **Shadow column / sidecar** — what to persist so the Data Steward can grade the feature dark
4. **Inertness proof** — the exact dry-run command on a fixed trading date, before and after,
5. **Tests** — flag-off path unchanged (unit), flag-on behaviour against a fixture built from
8. **Rollback** — one command / one flag.
```

Replace with:

```
2. **Change** — precisely what behaviour is added. No feature flag (DP-59). Name any runtime
   setting keys that size the job; settings are not gates.
3. **After-deploy check** — the read-only query or listing the Data Steward runs on the first
   nightly after deploy, with the expected before/after values (DP-49: not a step for the coding agent).
4. **What changes for the desk** — which published numbers or stored rows change from the ship
   date, so the desk can log the SHA in DATA_NOTES.md and split locked questions there (DP-50).
5. **Tests** — unit tests on fixtures; no live calls.
8. **Rollback** — `git revert` of the PR.
```

Fix-brief item 3 ("No feature flag when the fix restores intended behaviour; say explicitly why no
flag is needed. If the fix changes any published number, STOP and return the issue to Haci as
`research`") becomes:

```
3. Change — the minimal fix. Never a feature flag (DP-59). If the fix changes a published number,
   say which and from when; it still ships. Return the issue as `research` only if the "fix" would
   change what is scored or selected on a hypothesis rather than restore intended behaviour.
```

Line 44 ("advances IMPLEMENTED_FLAG_OFF himself with the PR link and hashes") depends on §2 below.

## 2. CLAUDE.md rule 11 and the controller's finding states

Rule 11 today: "**Prove inert, ship dark, flip last.** New code ships flag-off with a byte-identical
checksum on the old path; validated in shadow; activated only after inertness is confirmed."

That rule and the controller states `IMPLEMENTED_FLAG_OFF → SHADOW_VALIDATED → RELEASE_APPROVED`
(`research/lib/controller.py:22-25`, human-edited) apply only to **research-finding** briefs — a
HISTORICALLY_CONFIRMED verdict changing scoring or selection. No such brief exists yet. If Haci wants
findings to ship the same way as fixes, the rule 11 text becomes:

```
11. **Ship, then verify here.** Platform changes ship directly (DP-59). The desk verifies every
    fix, build and finding after deploy with a read-only before/after check and records the ship
    SHA and date in DATA_NOTES.md; locked questions split at that date (DP-50).
```

and the controller's three post-LEDGERED states would collapse to `HUMAN_APPROVED → BRIEF_WRITTEN →
IMPLEMENTED → VERIFIED` — a patch the desk can draft under `docs/controller_patches/` on request,
applied by Haci as with patch8. Until then the desk leaves the finding path as it is; nothing is
waiting on it.

## 3. Already shipped with a flag

EN-002 (speed-to-target internal card) is VERIFIED behind `SAS_SPEED_TO_TARGET_INTERNAL`. Under DP-59
Haci can simply turn it on and delete the flag in a follow-up; the desk does not re-brief it.
