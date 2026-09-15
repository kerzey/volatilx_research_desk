# VERIFY PI-017 -- forced UOA re-run delete scope

**Platform SHA verified:** `bccfa67b2baedb4e2a563a66f311874e69a7639d` (bccfa67); platform repo path
as given in the task (Projects\volatilx). Brief's citation base: `d19c9a9`. Confirmed `d19c9a9` is a
direct ancestor of `bccfa67` with exactly one commit between them (bccfa67 itself); the PR #28 merge
commit that carried it to `main` has an identical tree to `bccfa67` (empty diff), so nothing changed
in the merge. Fix commit time: 2026-09-14 20:04:04 UTC (15:04:04 -0500).
**Desk repo SHA:** `4a87d15` (research repo HEAD at verification time). **Date:** 2026-09-14.

## IMPLEMENTED:bccfa67 -- code verified, deploy unconfirmed, not FAILED. Every repository-side item passes clean. Database checks V1, V2, V4, the success_partial count, and the no-unauthorized-forced-rerun check all confirm no regression and no historical rewrite. V3 shows the most recent nightly run (started 2026-09-14 21:04 UTC, after the fix commit) still carries no force_scope / bulletin_action -- the deployed process is not yet running this code. The row moves to VERIFIED when a nightly run-audit row dated after the deploy carries those fields (V3 re-check).

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

## 4. Database side (brief section 8, V1-V4) -- run this pass, read-only

A desk database credential was in fact present this session via the `.env.research` loader
(`research/lib/desk_env.py`) -- my first report wrongly said none was available; that was a missed
loading path, not a real absence, and is corrected here. Queries were run read-only
(`default_transaction_read_only=on`) from a scratchpad script, counts only, no row bodies beyond the
columns the brief names.

**V1 -- dates with fewer than 200 distinct symbols in uoa_symbol_daily.**

    trading_date  n_symbols
      2026-01-09         23

Exactly one row, unchanged from the frozen parquet's record of the same date. **PASS.**

**V2 -- per-date row/symbol counts, 2026-01-07..2026-09-10, against the frozen parquet.**

Completed by the coordinator in the same run after the Steward's first attempt crashed on a
date-dtype bug in its own comparison script. The check script is committed next to this report as
`research/reports/VERIFY_PI-017_v2_check.py` (read-only session, counts only, reads only the
trading_date and symbol columns of `research/data/v001_uoa_symbol.parquet`). Output:

    freeze dates: 169  live dates: 169  freeze rows: 83747  live rows: 83747
    dates differing or missing on one side: 0
    V2: PASS -- live matches freeze row-for-row on every date

**PASS.** No historical row in `uoa_symbol_daily` over the freeze window moved between the v001
freeze (2026-09-10) and this verification (2026-09-14).

**V3 -- the 10 most recent nightly runs (config/stats fields + timestamps).**

    trading_date  status forced force_scope universe_size bulletin_action           started_at
      2026-12-09 running   true        None          None            None  2026-01-12 15:03:23 UTC
      2026-09-14 success    NaN        None          None            None  2026-09-14 21:04:28 UTC
      2026-09-11 success    NaN        None          None            None  2026-09-11 21:02:17 UTC
      2026-09-10 success    NaN        None          None            None  2026-09-10 20:44:09 UTC
      2026-09-09 success    NaN        None          None            None  2026-09-09 20:44:03 UTC
      2026-09-08 success    NaN        None          None            None  2026-09-08 20:43:32 UTC
      2026-09-07 running    NaN        None          None            None  2026-09-08 02:30:00 UTC
      2026-09-04 success    NaN        None          None            None  2026-09-04 20:43:23 UTC
      2026-09-03 success    NaN        None          None            None  2026-09-03 20:43:28 UTC
      2026-09-02 success    NaN        None          None            None  2026-09-02 20:43:28 UTC

(timestamps and status columns only; config/stats fields shown, no other row content). The
2026-09-14 row started at 21:04:28 UTC -- about an hour **after** the fix commit (20:04:04 UTC) -- so a
nightly did run chronologically post-commit. It still shows `force_scope` and `bulletin_action` as
`None`: the pre-fix code never wrote those keys at all, so their absence on the very next nightly after
the commit means the deployed process is not yet running bccfa67. **Deploy not confirmed** -- same
conclusion as PI-001's precedent, reached the same way (a post-commit run exists, but it is not written
by the new code).

One unrelated oddity surfaced in this same top-10, noted but not chased: a `run_type='nightly'` row with
`trading_date = 2026-12-09`, `status = running` (never finished), `started_at = 2026-01-12`, `forced =
true`. This predates the fix commit by many months and is not evidence about deploy either way; flagged
only in case it is useful to Haci separately.

**V4 -- dates since 2026-09-01 without exactly one bulletin row.**

    (no rows -- exactly one per date)

**PASS.**

**Supplementary checks (from the coordinator's message, not brief section 8 itself):**

- Count of `uoa_runs` rows with `status = 'success_partial'`: **0**. Matches the expectation that no
  partial forced run has happened yet.
- Forced nightly runs on `trading_date >= 2026-06-01` with `started_at` after 2026-09-14 00:00 UTC
  (Haci's header constraint -- no forced re-run on those dates until this fix deploys): **none found.**
  The constraint has not been violated.

## 5. Deviations from the brief

None found in the implementation. Status value, helper names, the module export list additions, the doc
text, the new CLI flag's name and choices, and the line-level ordering of the change all match the
brief's prescribed text exactly. Line numbers are shifted slightly from the brief's base-commit citations
because earlier insertions in the same function push later code down (e.g. the idempotency block now
ends at :1327, not :1248), but the code at each shifted location is identical to what the brief specified.
The one deviation from the brief is environmental, not in the diff: the new test file cannot be collected
without the platform's database-connection variable, which the brief did not anticipate needing even for
the pure in-memory-SQLite half of the suite (transitively, via the mapper-registration import).

## 6. Deployment note

Section 4's V3 result already answers this directly for this pass: the code at bccfa67 is correct
(sections 1-3), but the nightly that ran roughly an hour after the fix commit does not carry the fix's
new fields, so the deployed process is not yet on this code -- the PI-001 pattern, confirmed rather than
assumed this time. What would confirm deployment going forward: a nightly run-audit row, dated after
today, with `force_scope` and `bulletin_action` populated at all (their mere presence is the signal --
the pre-fix code never wrote these keys). V2 has since completed and passed (section 4), so the only
thing standing between this row and `VERIFIED` is that V3 re-check on a post-deploy nightly.
