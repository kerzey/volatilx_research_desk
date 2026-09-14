# VERIFY EN-002 -- speed-to-target internal card

Commit verified: 22a2e1b (platform repo), merged to main at d19c9a9 (Merge pull request
27 from kerzey/feat/en-002-speed-to-target-internal); parent 2d5776c matches the brief BASE value.
Brief: research/briefs/EN-002_speed_to_target_internal_card.md.
Verified 2026-09-13 by the Data Steward under DP-49/DP-50.

## FAIL: picks=578 vs the frozen-predicate expectation of 579 named in Section 8a; everything else PASSES

One qualified, ranked, DP-28 published row (TJX, 2026-06-11, overall_score=79.5802) is silently
excluded by the router _tier_of() score>=80 gate, so the shipped payload picks count (578)
does not equal the 579-row count named in Section 1/8 as the frozen before-state. Nights (71)
match. Root cause is not a defect introduced by this diff -- _tier_of is copied verbatim from the
existing, byte-identical services/sas_conviction_card.py:314-321 (comment: sub-80 is not
published), and Section 3.1 point 5 of the brief specifies exactly this cut for tier. The
mismatch is between the Section 1 claim (579 published rows) and the Section 3.1 tier design in
the same document, not a coding-agent error -- see Mismatches below. Per the brief own wording
(If picks or nights differ, that is a FAIL, not a rounding note), this is recorded as FAIL rather
than softened.

All inertness, purity, security and test checks (Sections 4, 5, 7 AC-1..9, AC-11) pass without
qualification.

---

## 1. Brief Section 3 vs commit, file by file

- Flag: SAS_SPEED_TO_TARGET_INTERNAL, default OFF, read at call time via tool_enabled() in
  services/sas_speed_to_target.py:80-85 -- mirrors services/sas_conviction_card.py:68-69 exactly,
  as directed. Confirmed default-OFF empirically (Section 3 below).
- Control reference file data/sas_speed_control_reference.json ships byte-for-byte the Section 3.2
  JSON: status = AWAITING_Q002, decision_date = 2026-10-12, levels = empty object.
- Import purity: services/sas_speed_to_target.py imports only json, os, statistics,
  datetime.date, pathlib.Path, typing, core.trading_days -- no sqlalchemy, db, or models.
  db/sqlalchemy imports live only in routers/admin_sas_speed.py, and models and
  services.sas_reference are imported inside the handler function, not at module scope,
  matching the app-bootstrap-safe pattern at services/sas_conviction_card.py:301-302.
- Haci-only router gating: routers/admin_sas_speed.py -- _require_admin(x_admin_token) is the
  first statement in get_sas_speed_to_target, raising 401 before the flag check, before any db
  use; same env-var plus header model as routers/admin_outcome_coverage.py. Not mounted on
  routers/performance.py.
- Entry-basis and passed_at_entry_known labelling: router passes passed_at_entry=None for every
  row (no next-open price exists in the platform); payload entry_basis field reads
  signal_close_step_proxy (NOT Q002 next-open entry; passed_at_entry not applied) -- confirmed
  verbatim in the replayed payload (Section 4 below).
- app.py: one import line beside admin_outcome_coverage, one include_router line beside it --
  matches Section 3.7 exactly (diff shown in Section 2c).
- docs/README.md: one row added after line 47; docs/SAS_SPEED_TO_TARGET_INTERNAL.md new, carries
  the required sentence that no number on this card may reach a subscriber surface until Q002
  reaches PROSPECTIVELY_CONFIRMED.

No deviation found between Section 3 and the commit.

## 2. Section 4 inertness proof (from the repo, DP-49)

(a) Touched-file list -- git diff --name-only 2d5776c 22a2e1b:
app.py
data/sas_speed_control_reference.json
docs/README.md
docs/SAS_SPEED_TO_TARGET_INTERNAL.md
routers/admin_sas_speed.py
services/sas_speed_to_target.py
tests/test_sas_speed_to_target.py

Exactly the seven paths named in Section 4(a). PASS.

(b) Subscriber path diff -- git diff --stat 2d5776c 22a2e1b over the twelve named files gives
empty output. PASS.

Six sha256 checks (before = 2d5776c, after = 22a2e1b):
services/sas_conviction_card.py       before=e6ce8fe0ab89b6462bb01756f6bd6125153af8e3ae82b79aadac9bfdeeb6d86b after=e6ce8fe0ab89b6462bb01756f6bd6125153af8e3ae82b79aadac9bfdeeb6d86b MATCH
routers/performance.py                before=46dd1bf9dc936ec2763b05f0dca3257eb00bbc7647b2c430fb39c49ee291794a after=46dd1bf9dc936ec2763b05f0dca3257eb00bbc7647b2c430fb39c49ee291794a MATCH
templates/performance.html            before=48497c5bf3f7fbd1506d13824c0576c8c4c21d37f550594d03e9993017f0e487 after=48497c5bf3f7fbd1506d13824c0576c8c4c21d37f550594d03e9993017f0e487 MATCH
models.py                             before=ff0605e9219874cc9999e03016f84675cb3aba8a0a489add1475708be8b502bf after=ff0605e9219874cc9999e03016f84675cb3aba8a0a489add1475708be8b502bf MATCH
scripts/run_sas_ladder_nightly.py     before=3883f1f52cf7f808aedd78097fe472e8474b7afbf26e8a0c69282096c1b2763b after=3883f1f52cf7f808aedd78097fe472e8474b7afbf26e8a0c69282096c1b2763b MATCH
core/feature_flags.py                 before=3d37fdf70f1e6eaf4d440150036c231096e85f95337ce3a29347fcb5e4fcbfdb after=3d37fdf70f1e6eaf4d440150036c231096e85f95337ce3a29347fcb5e4fcbfdb MATCH

All six MATCH. PASS.

(c) app.py numstat -- git diff --numstat 2d5776c 22a2e1b -- app.py gives 2 0 app.py. PASS.

AC-8 -- a text search of the full diff for write and DDL shaped SQL markers (the ones the brief
names) returns nothing. PASS.

(d) Flag-default and import-purity -- reproduced the exact assertions from the brief (the desk
holds no write-capable database credential to unset in the first place, per rule 1 and DP-49/50)
against services.sas_speed_to_target loaded from the platform repo at 22a2e1b:
EN-002 flag default OFF: OK; import-pure: OK
tool_enabled() is False with the flag unset; sys.modules shows neither db nor models
imported as a side effect of importing the module. PASS.

## 3. Section 5 test

Ran python tests/test_sas_speed_to_target.py from the platform repo (no pytest, no conftest, no
DB connection attempted):
EN-002: 9/9 checks passed

PASS -- matches the expected last line named in the brief exactly. Confirms T1-T9 (step-to-session
bridge, classify precedence including passed_at_entry beating a step-1 hit, fixture denominators,
the 20-row floor release at exactly 20 with hit_within value 0.8333 for the 2 cut, the control
stub, the shipped reference file AWAITING_Q002 status, the entry-basis caveat string,
holiday-aware session counting via core/trading_days.py, and the flag-default matrix).

## 4. Section 8a replay over the pinned freeze (manifest_v001, no live query)

research/data/v001_sas_candidates.parquet sha256 confirmed
af40ad8a48915f979cf36b0cc4d6526a7e9ecfbd523351ac4d8155b7a0aaa2f2 -- matches the manifest exactly.

Filtered to the tool window (published predicate per DP-28, trading_date >= 2026-06-01): 579
rows over 71 nights -- matches Section 1 of the brief (579 published rows over 71 nights) precisely.

Imported the shipped summarize_speed, load_control_reference and sessions_elapsed from
services.sas_speed_to_target (platform repo, unmodified), reconstructed the router row-builder
(_level_prices, _entry_ref, _tier_of, ladder_level_is_void -- read verbatim from
routers/admin_sas_speed.py and services/sas_reference.py, not reimplemented from memory) over the
parquet rows, as_of = 2026-09-10, passed_at_entry = None for every row (no next-open price in the
platform, as specified), and called summarize_speed:

picks: 578   nights: 71
payload sha256: 944e59b3ffc66745b610224306bdb4b42d6f300fe4330bc454afffe59e573b5d

- nights == 71 -- MATCH.
- picks == 578, not 579 -- MISMATCH, see below.
- Every cell: control_status == AWAITING_Q002, control is None -- confirmed across all tier by
  level cells. PASS.
- Top level: quotability == NON_QUOTABLE, internal_only is True,
  gate is question Q002, decision_date 2026-10-12, required_state PROSPECTIVELY_CONFIRMED,
  entry_basis reads signal_close_step_proxy (NOT Q002 next-open entry; passed_at_entry not
  applied). All PASS.

Month-by-month coverage of level_hit_steps_json over the tool window, from the frozen parquet:

month               published rows   with level_hit_steps_json   nights
2026-06             171              163                         21
2026-07             177              168                         22
2026-08             170              170                         21
2026-09 (to 09-10)  61               43                          7
total               579              544                         71

Matches the Section 1 table in the brief exactly (June, July, August, September rows and totals).
No coverage gap introduced.

One read-only query named in Section 8a: NOT RUN. The RESEARCH_DB_URL credential is not set in
this session. Per CLAUDE.md rule 1 and DP-49/DP-50, no other credential may be substituted. The
Steward should re-run this check (against the SAS candidates table, June, July, August rows must
still read 171/163/21, 177/168/22, 170/170/21) the next time that credential is available
in-session, to confirm nothing rewrote the sealed June-August counts.

Zero rows written to the database: confirmed structurally, not just by inspection -- the commit
adds no migration, no new model column, and the AC-8 marker search (Section 2 above) finds no
write or DDL text anywhere in the diff. The router one database touch is a single read-only ORM
fetch-and-filter.

## Mismatches between brief and commit (both directions)

1. Section 1 of the brief states 579 published rows over 71 nights as the tool before-state; the
   shipped payload reports picks: 578. The gap is the router _tier_of() gate (score >= 90 maps to
   apex, score >= 80 maps to select, otherwise excluded), which Section 3.1 point 5 of the brief
   specifies directly (tier uses the same cut as services/sas_conviction_card.py:314-321). One row
   in the window -- TJX, 2026-06-11, overall_score = 79.5802, qualified = True, selected_rank = 8.0
   -- is DP-28 published but scores below the tier floor, so it is silently excluded from every
   tier picks and nights counters.
   This is not a defect in the diff:
   services/sas_conviction_card.py:314-321 (byte-identical per Section 2(b) above) has carried the
   identical _tier_of cut, on the identical qualification and rank query, since before this
   commit -- so the live conviction card already excludes this same row today. The Section 1
   count of 579 is the DP-28 predicate count; the Section 3.1 design produces 578. That is a gap
   in the brief own arithmetic, not something the coding agent introduced or could have avoided
   while following Section 3.1 as written. Recorded per the Section 8a rule in the brief (If
   picks or nights differ, that is a FAIL, not a rounding note) rather than waived.
   Recommend:
   either the brief writer amends the Section 1 before-state language to 578 tier-eligible picks
   (579 DP-28 published, 1 sub-80 tier gap), or Haci decides whether the tier gate should itself
   be a documented exclusion category in the summarize_speed excluded dict (currently it is
   invisible -- the row is dropped before summarize_speed ever sees it, at the router level). This
   is a documentation and definition gap worth a one-line PI, not a reason to hold the flag off
   any longer than the gate already requires.
2. No other mismatch found. Every other file, function signature, constant, docstring sentence,
   and test assertion named in Sections 3-5 matches the commit byte for byte or behaviourally as
   specified.

## Flag-flip instruction (Haci alone, Section 8b)

Turning SAS_SPEED_TO_TARGET_INTERNAL=true (and ADMIN_TOKEN if unset) in Azure app settings is the
only production-side action this brief authorizes, and it is not the Data Steward or the coding
agent to take. It writes zero rows and changes nothing subscriber-facing; the control arm stays
stubbed (AWAITING_Q002) regardless of when the flag is flipped, so flipping it before 2026-10-12
cannot leak a Q002 primary. That decision belongs to Haci.

## Verdict

FAIL: picks=578 vs the 579 count stated in Section 8a of the brief, traced to a gap between the
brief own Section 1 and Section 3.1, not a coding defect -- every other Section 3-7 check passes.
