# Research desk process update — 2026-09-14

The desk now reports existing internal evidence before its final prospective verdicts, prioritizes
the product's core questions, and distinguishes operational delays from missing observations.
The update was explicitly authorized by Haci: "Update the research desk per your recommendations."

## Installed changes

- BOARD.md is generated with seven evidence cards, their sources/limitations, observation and review
  dates, registered dates, actionable learning work, and explicit readiness categories.
- The autonomous queue includes weekly card reviews, historical companion work, schedule successor
  scoping and counts-only readiness refreshes for the core outcome questions. Missing counts remain
  unmeasured; they are never inferred from a calendar projection.
- LEARNING_POLICY.md and DP-52..57 define admitted historical exploration, report cadence, priority,
  corrected forecasting, and the boundary between internal evidence and scientific confirmation.
  The coordinator, registrar and decision-maker instructions and user guides are updated.
- The preregistration template now agrees with current path objectives, sample floors, 30-night
  shadow requirements, episode dependence, prior-exposure disclosure and uncertainty reporting.
- SCHEDULE_AUDIT.md reproduces the Q024/Q027/Q029 maturity-accounting concern from pinned source
  reports. A changed source stops the audit until its counts are reviewed. Planning scenarios
  are not approved new dates or statistical power guarantees.
- The Q028 manifest parser repair removes only explicit placeholders and preserves other tokens.
  Q028 advanced through the controller to DATASET_PINNED after checksum verification.
- EN-002's brief distinguishes 579 published rows from 578 tier-eligible output picks. The failed
  original verification remains intact; a new verification receipt is queued against the corrected
  specification. No deployment or flag change occurred.
- The dated HTML calendar now directs readers to the regenerated board for current evidence.

## Validation

- `python -m unittest discover -s research/tests -p test_learning_workflow.py -v`: 15 tests pass.
  Covers missing/stale/future readiness, per-endpoint and post-lock floors, prohibited outcome fields,
  no early runs from met counts, extension dates, cleared deferrals, fail-closed manifest parsing,
  schedule arithmetic/source drift, recurring cards and queue read-only behavior.
- `python docs/controller_patches/test_manifest_header.py`: all 36 questions pass; real manifest
  tokens are preserved and Q028 resolves to its selections manifest alone.
- `python research/lib/controller.py advance Q028 DATASET_PINNED ...`: successful; existing
  manifest verification checked the frozen file checksums without producing study outcomes.
- All 28 stored locked PREREG hashes match their files. No PREREG, registered schedule, raw dataset,
  scientific result, verdict or market-data input changed. Q028's controller pin is the only question
  state change.
- Schedule audit and board generation succeed; `git diff --check` reports no whitespace errors.

The first isolated fixture test run hit Windows sandbox permissions in the temporary directory;
the same suite passed after the permitted elevated rerun. There were no test-logic failures in that run.

## What follows in normal desk cycles

The queue owns individual historical protocols, readiness refreshes, EN-002 re-verification and
proposals for earlier separately registered successor experiments. Existing studies continue on
their original schedules. Admitted history may yield an exploratory estimate or a documented
NOT_ESTIMABLE answer; neither becomes independent prospective confirmation. Public claims and
production activation retain their current gates.

This maintenance update is in the working tree; it has not been committed or pushed.
