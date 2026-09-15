# VERIFY PI-017 -- forced UOA re-run delete scope

**Platform SHA verified:** `bccfa67b2baedb4e2a563a66f311874e69a7639d` (bccfa67); platform repo path
as given in the task (Projects\volatilx). Brief's citation base: `d19c9a9`. Confirmed `d19c9a9` is a
direct ancestor of `bccfa67` with exactly one commit between them (bccfa67 itself); the PR #28 merge
commit that carried it to `main` has an identical tree to `bccfa67` (empty diff), so nothing changed
in the merge.
**Desk repo SHA:** `4a87d15` (research repo HEAD at verification time). **Date:** 2026-09-14.

## FAIL: verification-blocked -- every repository-side item checks out clean, but the Data Steward's database checks (brief section 8, V1-V4) could not run: no desk database credential is present in this session. Same precedent as PI-001's second verify pass (research/reports/VERIFY_PI-001.md section 9). Not a code finding.

---

## 1. Checklist (brief section 8 item by item, all read at bccfa67)

| # | Item | What I looked at | Result |
|---|---|---|---|
| 1 | Delete scoped to the resolved universe on a partial forced run | services/uoa_screener.py:996-1040, delete_rows_for_forced_rerun -- the symbols=[...] branch filters UoaContractDaily.underlying_symbol.in_(syms) / UoaSymbolDaily.symbol.in_(syms); n_bulletins is forced to 0 on that branch | PASS |
| 2 | Universe resolved before any delete | :1329-1336 -- the universe is resolved and the delete scope computed immediately after the idempotency early-return (:1310-1327) and before the run-record lookup (:1348) and the if force: delete block (:1381-1396). The old duplicate universe-resolution call was removed -- only one call site remains in the whole file (:1331, confirmed by grep) | PASS |
| 3 | Full-universe / no-universe nightly path unchanged | a stat listing of the fix commit shows exactly 5 changed paths: a docs file, two scripts (the general nightly runner and the single-symbol range-repair script), services/uoa_screener.py, and the new test file. The scheduler, the nightly-pipeline entry point, the scoring service, the candidate-universe builder, and every router file are not in that list, so their diff against the base commit is empty by construction (the range is a single commit). services/uoa_scheduler.py:103 (the nightly caller) passes force=False and is untouched | PASS |
| 4 | Partial forced run preserves the bulletin | :1953-1960 -- when preserve_bulletin is true, the existing bulletin's fields are copied into the return payload, with no delete and no new row added; preserve_bulletin = bool(partial_force and existing_bulletin is not None) (:1338); the delete helper returns bulletins: 0 whenever a symbol list is given (:1034), so the UNIQUE(trading_date) constraint on the bulletin table is never at risk | PASS |
| 5 | Run record carries partial status + scope fields | run_config (:1339-1346) carries force, force_scope, universe_explicit, universe_size, universe_symbols; stats gains force_scope/force_partial/force_deleted (:1421-1423); stats also gains bulletin_action, "preserved" or "rebuilt_from_full_date" (:1960, :2002); run.status is "success_partial" when partial, else "success", both on the persisted row (:2004) and the returned dict (:2041) | PASS |
| 6 | The single-symbol range-repair script hardcodes universe scope | line 86 of that script passes the universe-only delete scope unconditionally on every call -- not read from a flag. Its --force help text was updated to the brief's exact wording (line 46) | PASS |
| 7 | Test exists and covers the delete contract | the new test file is a byte-for-byte match to the brief's test-file listing: 5 pure scope-rule assertions plus 3 in-memory-SQLite delete-contract assertions (single-symbol run leaves collateral symbols, the bulletin, and the neighbouring date untouched; full-universe run still wipes the whole date incl. the bulletin; an empty symbol list deletes nothing) | PASS (content match; execution blocked, see section 3) |
| 8 | Nothing in the brief's out-of-scope list touched | the OI-confirmation force path is a separate, untouched function; the 100-symbol sample script and the OI/GEX-for-day script are not in the changed-file list; no model/schema change (no new run-history table, the run table's existing uniqueness constraint is untouched); the subset-run cross-sectional-percentile issue the brief flags as a second, pre-existing defect is left alone -- only a warning log line was added, no scoring change | PASS |

## 2. Repo-only reproduction of brief section 4 (a), (b), (d)

(a) -- the pure scope-rule function, run live against the module at bccfa67's content (confirmed
identical between bccfa67 and the platform's current HEAD for every file this fix touches -- the only
files changed between them belong to an unrelated ladder-nightly change):

None
['INTC']
None
['AAPL', 'MSFT']

Matches the brief's expected output exactly, in order.

(b) -- a stat listing of the fix commit shows exactly the 5 named paths (section 1 item 3); since the
base-to-fix range is a single commit, any file not in that list has an empty diff against the base by
construction. Combined with (a)'s first line (no explicit universe leads to None, the whole-date branch),
the live nightly path is confirmed unchanged.

(d) -- searching the service module for the bulletin whole-date delete pattern returns exactly one hit,
at services/uoa_screener.py:1013, inside delete_rows_for_forced_rerun. The equivalent whole-date delete
pattern for the two other tables returns three hits total, all at :1011-1013 -- the symbols is None
branch of that same function. No stray whole-date delete survives anywhere else in the file.

## 3. Test suite -- could not execute; content-verified instead

Running the new test file under pytest (with bytecode writing and the cache plugin disabled, to avoid
writing into the repo) fails at collection, not at any PI-017 assertion. The failure is an
ImportError/ValueError chain: the test file imports the platform's user module (to register the User ORM
mapper, exactly as its own docstring says -- the same pattern as an existing regime-repository test),
which imports the platform's db module, which reads the platform's required database-connection
environment variable unconditionally at import time and raises if it is unset. That variable is a
distinct name from the desk's own read-only credential and is a credential the desk is never permitted to
hold or set (CLAUDE.md rule 1; DP-49). Retried with conftest collection disabled to rule out a root
database fixture -- same failure, same import chain, so this is intrinsic to the test module's own
imports, not to any conftest. It is a pre-existing property of the platform's test environment, not
something this fix introduced, and it would block every test file that imports user/db, not only this
one.

Fallback ("if it cannot run cleanly... fall back to reading it"). A full read of the new test file at
bccfa67 shows it is a byte-for-byte match to the brief's test-file listing: same fixture (the 2026-01-09
date under repair, a neighbouring 2026-01-12 date that must never move, 3 symbols x 2 tables x 2 dates
plus 1 bulletin per date), same 5 pure-function assertions, same 3 SQLite delete-contract assertions with
the same expected row counts. Cross-checked by hand against the shipped delete function (section 1 item
1): for a single-symbol delete on the repair date, the seeded fixture has 1 contract row and 1 symbol row
for that symbol, 2 each for the other two symbols combined -- the .in_() filters would delete exactly
contract_rows 1, symbol_rows 1, bulletins 0, matching the test's asserted value; for the whole-date delete
branch, all 3+3+1 rows are removed, matching; for an empty symbol list, the early return of all zeros
matches. The assertions and the implementation agree by inspection -- a code-reading confirmation, not an
executed pass, flagged as such and not claimed as a test run.

## 4. Database side -- could not run (credential absent)

A full environment listing in this session (108 variables) shows no desk database credential, no
production SAS token, and no market-data credential present at all. The desk's own read-only query
helper exits immediately with a "not set" message under this condition -- confirmed directly by invoking
its help path. Per rule 1 and DP-49 the desk does not request, source, or substitute any other credential
to work around this. None of the brief's four database checks, nor the task's own step-4 items, were run:

- V1 (the single short-symbol-count date, unchanged) -- not run
- V2 (per-date row counts against the frozen parquet) -- not run
- V3 (post-deploy run-audit fields on new nightly rows) -- not run
- V4 (one bulletin per date since 2026-09-01) -- not run
- No partial-status run row exists yet -- not confirmed
- No forced re-run on any trading date on/after 2026-06-01 since the brief was written (Haci's header
  constraint) -- not confirmed

This is identical in kind to PI-001's second verify pass (research/reports/VERIFY_PI-001.md section 9):
the repository-side proof is complete, but the database confirmation the protocol requires for a PASS
could not be attempted at all.

## 5. Deviations from the brief

None found in the implementation. Status value, helper names, the module export list additions, the doc
text, the new CLI flag's name and choices, and the line-level ordering of the change all match the
brief's prescribed text exactly. Line numbers are shifted slightly from the brief's base-commit citations
because earlier insertions in the same function push later code down (e.g. the idempotency block now
ends at :1327, not :1248), but the code at each shifted location is identical to what the brief specified.
The one deviation from the brief is environmental, not in the diff: the new test file cannot be collected
without the platform's database-connection variable, which the brief did not anticipate needing even for
the pure in-memory-SQLite half of the suite (transitively, via the mapper-registration import).

## 6. Deployment note (does not affect the code verdict -- counts only)

Confirming the code is correct at bccfa67 is not confirmation that the deployed nightly process is
running bccfa67 (the PI-001 precedent: a merge to main was not sufficient evidence there). What would
prove deployment here, counts only, once a database credential is available: (i) V3 above -- any
post-deploy nightly run-audit row carries the new config/stats keys at all (their mere presence,
regardless of value, is evidence the deployed code writes them -- the pre-fix code never wrote these
keys); (ii) a forced re-run executed after deploy (Haci's, per brief section 8 step 3) produces a
partial-status run row with the universe-only scope recorded and populated delete counts, while the
untouched-date and neighbouring-date row counts stay intact -- the exact V1/V2 comparison. Until one of
those is observed, deployment is unknown, same as PI-001.
