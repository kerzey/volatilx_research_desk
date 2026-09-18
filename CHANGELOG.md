# v2 — changes after external review (2026-09-10)

Adopted
- Q001 rewritten: selection isolated from execution (next-open → T+10 close, no stops/targets);
  night is the unit of inference; one primary endpoint; MPE (placeholder 0.50% net/10 sessions)
  in the decision rule; C2 coin-flip-direction control separates direction skill from selection.
- eval_utils: night-level aggregation, MC control that never inflates n, date-clustered bootstrap,
  stationary block bootstrap for T+20/T+60, sign-flip permutation p, power hint, 4-state verdict.
- validators.py: nine mechanical checks (lock, checksums, revised labels, knowledge-time
  declarations, duplicate nights, count reconciliation, MC-as-n, byte-identical re-run, lineage)
  that must pass before the LLM Red Team can sign off.
- controller.py: deterministic 12-state machine with hash-checked preconditions; two states
  need --by haci; state.json is authoritative, Markdown is the human view.
- Four verdicts: NULL / INCONCLUSIVE / HISTORICALLY_CONFIRMED / PROSPECTIVELY_CONFIRMED;
  only the last supports a subscriber-facing claim; ≥30 forward shadow nights required.
- freeze_config: per-table availability (knowledge-time) declarations; manifest carries
  code_git_sha and version columns; OI-confirmation flagged as next-morning data.
- Guards: brief-writer must pass --dry-run; feature-branch push allowed, main/force blocked;
  brief-writer write set narrowed; enforcement code protected from all agents; hooks fail closed.
- setup_sandbox.sh: OS-level ACLs so scripts launched via Bash cannot write outside research/.

Narrowed / not adopted
- Point-in-time index membership: not applicable — universe is generated live nightly; recorded
  as a manifest note for any backfilled table only.
- Knowledge-time risk is in joins, not in SAS audit rows (point-in-time by construction).
- No additional agents; controller is a script, not an agent.

Consequence to keep in mind
- Night-level inference means Q001 has ~90–100 observations. Detectable edge ≈ 1% per 10 sessions.
  Modest real edges will read INCONCLUSIVE; the forward shadow cohort is where they get proven.

## 2026-09-15 — patch10: human gate and admin flag closed to sessions

guard_bash.py now blocks any command containing `--by haci` or the token `DESK_ADMIN` unless the
hook itself runs in an admin session (`scripts/start_desk.sh --admin`). Before this, controller.py
compared a string and any agent could approve a question; and an inline `DESK_ADMIN=1` prefix
reached the controller's child process unguarded. Cockpit Phase 0 entry gate.
