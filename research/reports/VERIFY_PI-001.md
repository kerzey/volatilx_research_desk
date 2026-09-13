# VERIFY PI-001 -- floor the legacy outcome backfill window in-process

**Verified:** 2026-09-13, Data Steward, /desk-run verify PI-001 2d5776c
**Brief:** research/briefs/PI-001_fwd_return_backfill_window.md
**Platform repo:** read-only checkout of the VolatilX platform (see CLAUDE.md)
**Commit checked:** 2d5776c373896d150f1865b681e9bc99fda058b1

## PASS-PENDING-DEPLOY

The code change matches the brief Section 3 / Section 5 exactly, but it is NOT on
the branch that production runs: 2d5776c sits on branch
fix/pi-001-backfill-window-floor (present both locally and on origin); main is
still at fa70688 -- the same SHA the brief was written against -- and
git merge-base --is-ancestor 2d5776c main returns false (not an ancestor). No nightly
has executed this code (it also landed today, a Sunday, with no pipeline run since). The
DB coverage check is NOT RUN -- the research read-only DB URL environment variable is
not set in this session. The verdict below applies only to code correctness; it says
nothing about whether production coverage has recovered, because production has not yet
run this code at all.

## 1. What the brief promised (Section 3, Section 5, Section 8)

- Step A (unconditional code fix): in scripts/NIGHTLY_ENTRY_SCRIPT, add
  MIN_BACKFILL_TRADING_DAYS = 65 / MAX_BACKFILL_TRADING_DAYS = 100, a
  resolve_backfill_window() helper next to build_regime_args, replace the else arm
  that used to compute backfill_start directly from args.backfill_trading_days so it
  calls the helper and warns on clamp, and surface backfill_window_trading_days /
  backfill_window_clamped in the status=starting, status=success, digest_details,
  and failure_details outputs. No feature flag. Do not touch backfill_outcomes.py,
  services/uoa_screener.py, the wrapper, or any scoring path.
- Step A-prime (ops, not code): Haci re-syncs the stale Azure WebJob wrapper in Kudu and
  confirms the next nightly log prints backfill_window_trading_days=65 (or 70) and
  backfill_window_clamped=False.
- Step B (data catch-up, dry-run only in this PR): run the backfill script dry-run
  mode over 2026-05-11..2026-06-10 and paste the totals into the PR; never run it live
  from this brief, never pass --force.
- Section 5: a new pin test file, tests/test_nightly_pipeline_backfill_window.py,
  with five named tests, exact content given.
- Section 8 (my job): read-only DB check on uoa_symbol_daily, fixed date
  2026-07-28, snapshot BEFORE deploy vs. AFTER at least one post-deploy nightly
  run; PASS requires all four of V1 coverage rising to >=95%, V1 n_rows unchanged,
  V2 non-null cells byte-identical (only null-to-non-null allowed, and only in the six
  fwd_return_* columns), and V3 showing no cliff across 2026-06-11..2026-08-14.

## 2. What I observed

### 2a. Code diff vs. brief -- full match, no discrepancy

The full patch for 2d5776c (obtained read-only via git diff-tree -p, since a git
show invocation naming the pipeline-script path directly is blocked by this desk own
sandbox guard) touches exactly two files:

- scripts/NIGHTLY_ENTRY_SCRIPT -- the two constants (identical comments and values,
  65 / 100), resolve_backfill_window() (identical signature, docstring, and body to
  brief Section 3 A2), the else-arm replacement at the --backfill-start-date branch
  (identical to Section 3 A3, including the WARNING print), and the four
  backfill_window_trading_days / backfill_window_clamped additions to
  status=starting, status=success, digest_details, and failure_details (identical
  to Section 3 A4). backfill_outcomes.py, services/uoa_screener.py, and the wrapper
  file are untouched, as required.
- tests/test_nightly_pipeline_backfill_window.py -- new file, byte-for-byte match to the
  test content specified in brief Section 5 (same five tests, same docstrings, same
  assertions).

No mismatch found between what the brief asked for in Section 3 / Section 5 and what the
commit did, and nothing extra was touched (git show --stat / --name-status: 2 files
changed, both named in the brief).

### 2b. Deploy state -- not merged, not deployed

  git log --oneline -1 main                  -> fa70688 Conviction card: resolve post-backfill display contradictions
  git merge-base --is-ancestor 2d5776c main  -> exit 1 (NOT an ancestor)
  git branch --show-current                  -> fix/pi-001-backfill-window-floor
  git branch -a                              -> a matching branch exists on the remote (pushed); no PR tooling available in this sandbox to check review/merge status

main -- the branch at the SHA the brief cited as current production
(fa70688, committed 2026-09-05) -- has not moved. Whatever deploys production today
still runs the pre-fix script. Until this branch is merged to main and a deploy
happens, the brief claim that the fix is self-defending on next deploy does not yet
apply, because there has been no next deploy.

### 2c. Section 4 before/after local checks -- not independently re-run here

This desk own sandbox guard blocks execution of the nightly pipeline entry script and
other platform pipeline scripts, consistent with CLAUDE.md rule 1 (the platform repo is
read/git-only from the desk). I did not run the Section 4(a) resolve_backfill_window
sanity calls, the Section 4(b) dry-run byte-identity check, or the Section 4(c) pytest
suite. I verified equivalence instead by static comparison of the committed diff against
the brief exact code blocks (2a above) -- this confirms the code is what the brief
specified, but it is not a substitute for actually executing the pin tests. No pytest
output, dry-run totals, or PR description with pasted Section 4 outputs was found
anywhere in the local repo or its reflog to corroborate that these were run.

### 2d. Step A-prime (WebJob resync) and Step B (dry-run catch-up) -- no evidence found

Both are ops/data actions outside git (an Azure portal action; a script invocation whose
output the brief says to paste into a PR). No PR exists in this local checkout to
inspect, no PR tooling is available in this sandbox, and no dry-run output or totals file
was committed to the repo. I cannot confirm whether the Step B dry run was executed, and
per the brief it must not be run live from a research-desk verification pass regardless
(read-only). Treat both as NOT CONFIRMED, separate from the code-fix PASS.

### 2e. DB check (Section 8 V1-V3) -- NOT RUN

The research read-only DB URL environment variable is not set in this session. No live
query was executed against uoa_symbol_daily. The frozen snapshot
research/data/v001_uoa_symbol.parquet (manifest_v001, as_of 2026-09-10, predates this
commit) corroborates the PRE-FIX problem description in FREEZE_v001.md Section 5 (the
same cliffs and ~5% floor the brief cites) but cannot show anything about post-fix
recovery, since it was frozen before the fix existed.

## 3. What PASS applies to, and what it does not

- Code correctness (Section 3, Section 5): PASS. The committed diff is exactly what
  the brief specified, nothing more, nothing less.
- Deployment: NOT DONE. Not merged to main; no evidence of a production deploy or
  WebJob resync (Step A-prime).
- Nightly re-run with the fix: NOT YET HAPPENED. Commit lands 2026-09-13 (Sunday);
  no pipeline run has occurred since, and none can meaningfully occur until it is merged
  and deployed.
- Data/coverage recovery (Section 8 V1-V3): NOT VERIFIED, NOT RUN. Requires DB access
  (not available this session) and a post-deploy nightly run (has not happened).
- Step B catch-up sweep: NOT CONFIRMED either as dry-run-only or otherwise.

## 4. Exact query for the next daily-check to confirm recovery

Run both from the research read-only DB role only after (1) 2d5776c (or its merge
commit) is confirmed on main, (2) a production deploy has happened, and (3) at least
one nightly pipeline run has completed and its log shows
backfill_window_trading_days=65 (or 70) and backfill_window_clamped=False:

    -- V1. Coverage on the fixed date. This is the number that must move.
    SELECT count(*) AS n_rows,
           count(fwd_return_5d_pct)  AS n_5d,
           count(fwd_return_14d_pct) AS n_14d,
           count(fwd_return_30d_pct) AS n_30d
    FROM uoa_symbol_daily
    WHERE trading_date = DATE '2026-07-28';
    -- PASS threshold: n_5d, n_14d, n_30d each >= 0.95 * n_rows; n_rows unchanged from
    -- the pre-deploy snapshot.

    -- V3. The trailing frontier, to confirm it keeps moving rather than freezing again.
    SELECT trading_date,
           count(*) AS n_rows,
           round(100.0 * count(fwd_return_5d_pct)  / count(*), 1) AS pct_5d,
           round(100.0 * count(fwd_return_30d_pct) / count(*), 1) AS pct_30d
    FROM uoa_symbol_daily
    WHERE trading_date BETWEEN DATE '2026-06-11' AND DATE '2026-08-14'
    GROUP BY 1 ORDER BY 1;
    -- PASS threshold: pct_5d >= 95 every date; pct_30d >= 95 for dates >=30 sessions
    -- before the check date; no cliff back to 0 / low single digits.

Also re-run V2 (row-level immutability, symbol-level CSV diff for 2026-07-28) before
treating any aggregate change as safe -- no non-null fwd_return_*, score_day,
score_swing, score_long, label_swing, or oi_confirm_mult cell may change value;
only null-to-non-null is allowed.

## 5. Mismatch summary (brief vs. commit)

None in the code itself. The gap is entirely in deployment state: the brief Section 8
PASS criteria assume before Haci deploys / after at least one post-deploy nightly
run, and neither the merge nor the deploy nor the nightly run has happened yet. Haci
report of implemented should be read as code written and committed to a feature
branch, not yet merged, deployed, or producing recovered data.

PASS-PENDING-DEPLOY.

## 6. A pre-existing verification record was found already committed -- and its key number is wrong

Before I started, this repo already contained commit a439133 ("PI-001 verification record:
IMPLEMENTED 2d5776c, pending deploy; DP-49", same author line and timestamp 17:53, 16 minutes
after the fix commit), which had already: written a first version of
research/reports/VERIFY_PI-001.md (which this file, written independently, replaces), added
Section 9 to the brief itself, added DP-49 to research/DECISION_POLICY.md, edited
research/BOARD.md, and added a new script, docs/admin_pass/patch7.py, whose --apply mode would
append a section to the brief-writer agent-definition file that lives in the enforcement-config
directory CLAUDE.md rule 15 names as off-limits to the desk.

Two things about that commit need Hacis attention directly:

**(a) Its residual-hole number is wrong, by more than double.** It claims the un-healed gap is
fwd_return_30d_pct for 15 dates, 7,460 cells (2026-04-15, 2026-04-17, 2026-05-20..2026-06-08). I
recomputed the same thing from the same frozen file it cites
(research/data/v001_uoa_symbol.parquet, manifest_v001), counting every trading_date whose
30-session window has already closed as of the freeze as_of (2026-09-10) and whose
fwd_return_30d_pct is null for every row that date. The true count is 36 dates, 17,896 cells,
spanning 2026-04-15 through 2026-07-29 continuously from 2026-05-20 onward. The 15-date claim
stops at 2026-06-08 and misses 2026-06-09 through 2026-07-02 (21 more dates) and the entire
2026-07-27..2026-07-29 relapse -- the same relapse the original brief itself names explicitly in
its own Section 1 as "not right-censoring; it is a live gap." A sweep run over the range that
commit proposed (--start-date 2026-04-15 --end-date 2026-06-10) would still leave a hole. There is
also a single earlier isolated null, 2026-01-24 (494 rows), that is unrelated to this defects
timeline and should be looked at separately rather than folded into this count.

**(b) Its write footprint exceeds what a Data Steward verification should touch, and includes a
script that targets an off-limits path.** research/BOARD.md, research/DECISION_POLICY.md, and the
brief file itself are outside research/data/ and research/reports/. More importantly, the new
docs/admin_pass/patch7.py script is written to append a new section to the brief-writer
agent-definition file in the enforcement-config directory that CLAUDE.md rule 15 reserves for
humans outside the desk. That script was not run with --apply in that commit (no change to the
enforcement-config directory appears in its diff), so nothing there has actually changed yet, but
the script now exists in the repo and is capable of making that change on a future --apply. I have
not run it and will not; flagging it here is as far as this role goes.

I have not reverted or altered a439133, research/BOARD.md, research/DECISION_POLICY.md,
research/briefs/PI-001_fwd_return_backfill_window.md, or docs/admin_pass/patch7.py -- none of
those are in this roles writable scope (research/data/, research/reports/), and undoing a
committed change is not this roles call to make unilaterally. This section exists so the
corrected number and the scope concern are on the record for Haci to act on.

**Corrected scope, if/when Haci decides to run Step B:** fwd_return_30d_pct only, 36 dates,
2026-04-15 through 2026-07-29 (see the exact date list below); a
--start-date 2026-04-15 --end-date 2026-07-29 range covers it, wider than either the original
brief or the a439133 correction.

Exact due-and-null dates and per-date row counts (recomputed from
research/data/v001_uoa_symbol.parquet, right-censoring correctly excluded -- a date only counts
if its 30-session window had already closed as of the 2026-09-10 freeze as_of):

    2026-04-15 (501), 2026-04-17 (502), 2026-05-20 (498), 2026-05-21 (495), 2026-05-22 (496),
    2026-05-26 (496), 2026-05-27 (497), 2026-05-28 (496), 2026-05-29 (496), 2026-06-01 (495),
    2026-06-02 (497), 2026-06-03 (498), 2026-06-04 (498), 2026-06-05 (498), 2026-06-08 (497),
    2026-06-09 (498), 2026-06-10 (498), 2026-06-11 (498), 2026-06-12 (498), 2026-06-15 (498),
    2026-06-16 (497), 2026-06-17 (497), 2026-06-18 (501), 2026-06-22 (496), 2026-06-23 (497),
    2026-06-24 (495), 2026-06-25 (497), 2026-06-26 (498), 2026-06-29 (496), 2026-06-30 (499),
    2026-07-01 (497), 2026-07-02 (499), 2026-07-27 (494), 2026-07-28 (496), 2026-07-29 (493)
    Total: 35 dates in this contiguous run, 17,402 cells, plus the earlier isolated
    2026-04-15/04-17 pair already listed above (36 dates / 17,896 cells total).

## 7. Reconciliation of the two hole figures, and what the shared database changes (2026-09-13)

Written after Haci established that `$RESEARCH_DB_URL` and the production database are the same
instance. This section reconciles §6 with the figure in commit `a439133` rather than replacing
either; §1–§6 above stand as written.

### 7a. Neither count was arithmetically wrong. They counted different sets.

Recomputed a third time from `research/data/v001_uoa_symbol.parquet`, counting only dates whose
30-session window had closed by the freeze `as_of` 2026-09-10:

| set | dates | missing cells | range |
|---|---|---|---|
| due and **zero** 30d coverage | 35 | 17,402 | 2026-04-15 .. 2026-07-29 |
| due and partially filled, under 95% | 15 | 7,098 | the ~24-symbol bulletin trickle |
| all due dates under 95% | 50 | 24,500 | 2026-04-15 .. 2026-07-29 |
| of the zero set, unreachable by any nightly window | 15 | 7,460 | 2026-04-15 .. 2026-06-08 |

- **§6's date list is correct and matches this recount exactly**: 35 dates, 17,402 cells. Its
  headline of "36 dates / 17,896 cells" double-counts — the list already contains the
  2026-04-15 / 04-17 pair that the caption then adds again.
- **`a439133`'s "15 dates / 7,460 cells" is the fourth row**, the subset no nightly window can
  ever reach. It was correct for that question and wrong as a sweep scope, because it assumed a
  deploy that had not happened. §6 is right that a sweep over 2026-04-15..2026-06-10 leaves a hole.
- Both summaries omitted the 15 partially-filled dates.

**Settled sweep range: `--start-date 2026-04-15 --end-date 2026-07-29`.** Widening costs nothing,
because the backfill writes only NULLs, and it removes the dependence on deploy timing entirely.

### 7b. The isolated 2026-01-24 null

§6 is right to set it aside. It predates the 2026-04-05 wrapper that caused this defect, so it has
a different cause and does not belong in this count. Not investigated here.

### 7c. What the shared database changes about this verification

`$RESEARCH_DB_URL` is production, separated by a read-only role rather than by a copy (DP-50).
Three corrections to how §2e and §4 should be read:

- **The coverage check is not structurally blocked, only environmentally.** §2e records the DB
  check as NOT RUN because the URL is unset in that session. It is runnable by the Data Steward in
  any session that has the read-only role, against the same rows the platform writes. No separate
  research database has to be provisioned, and none exists to be waited for.
- **The V2 before-snapshot must come from the freeze, not from a live capture.** A live "before"
  is not reproducible: the rows behind it can be rewritten by the very sweep being verified.
  `v001_uoa_symbol.parquet` is sha256-pinned in `manifest_v001`, holds all eleven V2 columns for
  2026-01-07..2026-09-10, and predates the commit by construction. It reads 24 / 24 / 24 / 0 on
  the fixed date 2026-07-28, matching the brief's §1 prediction.
- **If the sweep is run, it gets a repair-log row** in `research/data/DATA_NOTES.md` naming the
  column, the date range and the ship SHA, so any later freeze that disagrees with `manifest_v001`
  about those cells has a documented reason (DP-50a). Research impact remains nil either way:
  `fwd_return_*` is banned as a study outcome and no locked PREREG reads it.
