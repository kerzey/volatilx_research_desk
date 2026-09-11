# Addendum for `.claude/agents/brief-writer.md` — the short route for platform bugs

The Brief Writer's charter only accepts a HUMAN_APPROVED research question. Plain bugs from
`research/PLATFORM_ISSUES.md` need a shorter form. Paste this block at the end of
`.claude/agents/brief-writer.md` (human edit; the desk cannot change agent charters):

```
## Fix briefs (platform issues, not findings)

Invocation: `fix-brief PI-NNN`. Precondition: the row for PI-NNN in
research/PLATFORM_ISSUES.md reads `HACI_DECIDED:fix`. If it reads anything else, stop and say
so — a `research` decision means the issue goes to the Registrar, not to you.

Output: research/briefs/PI-NNN_slug.md, a prompt the coding agent in the platform repo can run
without asking questions. Cite every touch point as path:line at the current platform SHA and
record the SHA in the header. Sections, in order:
1. Symptom — the evidence from the register, with a reproducing read-only SQL query.
2. Cause — the code path, path:line.
3. Change — the minimal fix. No feature flag when the fix restores intended behaviour;
   say explicitly why no flag is needed. If the fix changes any published number, STOP and
   return the issue to Haci as `research`.
4. Before/after check — one command on a fixed trading date; what differs, what must not.
5. Test — the unit or contract test that would have caught it.
6. Rollback — one command.
7. Out of scope.

Then set the register row to BRIEF_WRITTEN with the brief's path. Haci runs it, records the PR
and SHA in the register, and the Data Steward confirms the data changed on the next freeze.
```
