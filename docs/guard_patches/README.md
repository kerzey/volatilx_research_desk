# Guard patches — apply by hand (2026-09-10)

Replacements for `.claude/hooks/guard_bash.py` and `.claude/hooks/guard_write.py`, plus a
test suite. I could not install them myself: edits to security-hook scripts are blocked here,
first by Claude Code's auto-mode classifier and then by the repo's own
`Edit(.claude/**)` deny rule. Apply them yourself.

## Apply

From the repo root, in Git Bash:

```bash
cp .claude/hooks/guard_bash.py  .claude/hooks/guard_bash.py.bak
cp .claude/hooks/guard_write.py .claude/hooks/guard_write.py.bak
cp docs/guard_patches/guard_bash.py  .claude/hooks/guard_bash.py
cp docs/guard_patches/guard_write.py .claude/hooks/guard_write.py
python docs/guard_patches/test_guards.py --installed
```

The last line must print `all 33 cases pass`. Hooks are re-executed per tool call, so the
change takes effect immediately — no restart needed. To roll back, copy the `.bak` files back.

## What these fix

**1. The identity-gated rules never ran.** Claude Code 2.1.267 does not populate `agent_type`
in the PreToolUse payload, nor `CLAUDE_AGENT_TYPE` in the hook environment, for subagent tool
calls — 16 subagent-originated commands in `hook_audit.log`, all with an empty agent field,
none duplicated (so the `.claude/agents/*.md` frontmatter hooks are not firing either).
Both guards gated their strongest rules behind `agent in DESK_AGENTS`, so those rules were
dead code. Against the installed guards the suite fails 12 of 33 cases, including the exact
check README Step 4 says must be blocked:

```
FAIL  bash   SQL DML via db.py, identity unknown           blocked=False
FAIL  bash   foreign credential DATABASE_URL               blocked=False
FAIL  bash   foreign credential BACKFILL_DB_URL            blocked=False
FAIL  bash   history rewrite                               blocked=False
FAIL  bash   blob upload outside research                  blocked=False
FAIL  bash   run platform pipeline                         blocked=False
FAIL  bash   edit guard via redirect                       blocked=False
FAIL  bash   edit controller via sed -i                    blocked=False
FAIL  write  enforcement code                              blocked=False
FAIL  write  controller                                    blocked=False
FAIL  write  outside allowed prefixes                      blocked=False
FAIL  write  research/data as data-steward                 blocked=True   <- see (2)
```

The fix inverts the default: every rule applies to every session. `resolve_agent()` still
records identity when it is available (payload, env, or `--agent <name>` on the hook command
line) so this improves automatically if a future version starts populating those fields.

**2. A latent Windows path bug in `guard_write.py` that would have deadlocked the desk.**
`os.path.relpath` returns backslash-separated paths on Windows, so `rel.startswith("research/")`
is always False. Today it is masked, because the identity check exits before any prefix test
runs. The moment identity starts working — by this patch or by a Claude Code update — every
desk agent write is rejected as "outside research/, docs/, playbook/". Demonstrated:

```
$ echo '{"tool_name":"Write","agent_type":"researcher",
         "tool_input":{"file_path":"research/questions/Q002_x/eval.py"}}' | python .claude/hooks/guard_write.py
BLOCKED by guard_write: research\questions\Q002_x\eval.py is outside research/, docs/, playbook/
```

The researcher could not write `eval.py`; the reporter could not write `REPORT.md`.
Fixing identity *without* fixing this would have broken the desk. Both are fixed together.

**3. `BACKFILL_DB_URL` added to `FORBIDDEN_CREDS`.** That credential is in `.env.research`,
outside CLAUDE.md rule 1's allowlist, and the old pattern did not match it. This is a
belt-and-braces measure — still remove it from `.env.research`.

**4. `eval_utils.py` added to the protected set.** CLAUDE.md rule 15 lists it as enforcement
code; the old `guard_bash` pattern omitted it.

## DESK_ADMIN

Making every rule universal would otherwise lock you out of your own enforcement code from
inside Claude Code. The escape hatch is a launch-time environment variable:

```bash
./scripts/start_desk.sh --admin      # Git Bash
.\scripts\start_desk.ps1 -Admin      # PowerShell
```

It lifts only the enforcement-code and allowed-prefix rules. It never lifts the credential
rule or the locked-PREREG rule. It is safe against self-escalation because the hook reads its
own process environment: an agent prefixing `DESK_ADMIN=1` to a Bash command changes that
command's environment, not the hook's.

## Deliberately not changed

- **Pushes to main/master.** `guard_bash`'s block message claims they are blocked, but
  `GIT_DANGER` only matches force pushes and rewrites — and `settings.json` explicitly allows
  `Bash(git push origin main*)`. The two contradict each other. I left the behaviour as-is
  rather than silently change policy; decide which you want and say so.
- **The `CODEBASE_DIR` false positive.** Any command that mentions `CODEBASE_DIR` and also
  contains a redirect or `python -c` is blocked, even when read-only. It is annoying but
  errs safe, and tightening it risks opening a real hole.
