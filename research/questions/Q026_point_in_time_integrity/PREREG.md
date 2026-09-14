# Q026 — point_in_time_integrity: did every input exist when SAS made the prediction?

**Status:** DRAFT (lock by committing this file; `--by desk`, DP-46)
**Family:** F8 System validity (Haci's Master Hypothesis Program, H0 → BACKLOG H-069)
**Type:** **DIAGNOSTIC / census. PASS / FAIL, no MPE, no BH, no confidence interval.** This question
tests no edge and estimates no effect. It produces a **leakage register**: an enumeration, row by row,
of where the frozen data's actual write times disagree with the availability the desk has declared.
**Every number it produces is `NON_QUOTABLE`** (rule 12) and none of them is ever a subscriber claim.
**Manifest (selections):** research/data/manifest_v001.json (as_of: 2026-09-10; frozen_at
2026-09-10T22:31:32Z; platform SHA fa70688bc252d14f8d67e371afafc194731c324e)
**Manifest (prices):** research/data/manifest_prices_v001.json (as_of: 2026-09-10; frozen_at
2026-09-11T02:04:59Z; base_manifest_sha256 b03f355a…bef374) — Channel D only (restatement check);
**no forward bar is read as an outcome and no outcome column of any table is read anywhere in this
question.**
**Exclusions:** research/data/exclusions_v003.json (newest, DP-22) — used as an **input to the
materiality test**, never as a filter on the census (§2.3).
**Script by:** Researcher (rule 9, written once from §4) · **Run by:** Data Steward, on the pinned
parquet (DP-50(c): **no live query of any kind produces any number here**).
**Attribution source:** the read-only platform repo at the frozen SHA
`fa70688bc252d14f8d67e371afafc194731c324e` (`git show fa70688:<path>`), never HEAD.
**DP-50 sweep at lock (2026-09-14, decision 8):** no repair that ships after the 2026-09-10 freeze can
reach a row here, the parquet being sha256-pinned — including `2d5776c` (PI-001, the
`uoa_symbol_daily.fwd_return_*` backfill, merged 2026-09-14). Any repair shipping before 2026-09-21
that rewrites historical rows still gets its dated `DATA_NOTES.md` entry and changes nothing in this
question.
**Registered by:** registrar · **Date:** 2026-09-14 · **Decisions:** DECISIONS.md

---

## 1. Hypothesis (plain English, one sentence)

**Every input the platform used to make a pick existed at 16:05 ET on the pick night — nothing the
desk treats as a feature was written, rewritten or restated after the decision it is supposed to have
informed.**

PASS = the register's material section is empty. FAIL = it has at least one row. There is no
directional claim, no effect size and nothing to confirm; the pre-registered object is **a fixed
enumeration procedure and a fixed materiality rule**, written before anyone looks at what it finds.

## 2. Population

### 2.1 Unit

Two units, both fixed here:

- **The census unit is the row** — this is a census, not a sample. Every row of every table in both
  pinned manifests is read. This is the whole point of the question: FREEZE_v001 §7 checked 15–20
  rows per table and `KT_AUDIT_manifest_v001_rerun_nights.md` §6 showed why that missed four re-run
  nights (231 of 6,479 candidate rows ≈ 3.6%; a 20-row sample has roughly a 50% chance of seeing none
  of them).
- **The reporting unit is the trading night** (rule 6). Every count in the register is reported per
  night as well as in total, and the register's rows are keyed `(table, column, night, question)`.

### 2.2 Exact filters on the frozen manifests

- **Nights:** `SELECT DISTINCT trading_date FROM v001_sas_runs.parquet` → **113 nights,
  2026-04-01 .. 2026-09-10**. Every one is in the census, including the 9 `manual_runs`, the 1
  `non_session_runs` and the 1 `uncorroborated_publication_runs` night.
- **Selection tables (manifest_v001), all 11, every row, no further WHERE clause beyond the frozen
  SQL** (`WHERE trading_date <= '2026-09-10'`): `sas_candidates` (6,479), `sas_runs` (113),
  `sas_excursion` (1,414), `conviction_monitor` (3,339), `market_regime` (385), `uoa_symbol`
  (83,747), `gex_symbol` (7,278), `whale_ledger` (0), `projection_bull` (2,420), `projection_bear_v2`
  (1,215), `outcome_corrections` (795) — **107,185 rows**. Note that `uoa_symbol`, `gex_symbol`,
  `projection_bull` and `market_regime` carry rows dated **before** 2026-04-01 (the frozen SQL has no
  lower bound); those rows are **in** the census (KT_AUDIT §3 found a 2026-01-07..2026-03-20 late-write
  block there) and are classified by the same materiality rule as every other row.
- **Price tables (manifest_prices_v001), Channel D only, every row:** `prices_daily_raw` (66,500),
  `prices_daily_split` (66,500), `prices_hourly_raw` (451,231); 436 symbols.
- **Columns:** every column listed in each manifest table block. No column is dropped; §4 Channel E
  classifies each one as feature-eligible, outcome, or metadata.
- **Questions:** the register is keyed against **21 registered questions**, and **this section is the
  authoritative list** (decision 1): the 20 in state `PREREG_LOCKED` or `DATASET_PINNED` as of the lock
  commit — Q002, Q003, Q004, Q006, Q007, Q008, Q009, Q010, Q011, Q012, Q013, Q014, Q015, Q016, Q018,
  Q019, Q021, Q022, Q023, Q024 — plus **Q005** (`LEDGERED`, closed — a material row against Q005
  produces a ledger note, not a re-run). Q001 (`REJECTED`), Q017, Q020 and Q025 (`DEFERRED`) are
  **out**, named here so the list is not silently re-derived later (state files verified 2026-09-14).
  Questions locked after this commit are not added mid-run. `eval.py` **transcribes** this list and
  **fails loudly** — aborts with the diff, produces no register — if its transcription does not match
  these 21 ids exactly (rule 9; the Q024 static-artifact pattern). The list is never re-derived from
  `state.json` at run time.
- **`ADVISORY` rows (decision 1).** Four listed questions have prospective windows extending past the
  freeze (**Q010, Q022, Q023, Q024**). A late-write pattern on a column one of them *will* read, found
  on a night **outside** 2026-04-01..2026-09-10 or outside that question's own in-window range, is
  itemised and labelled **`ADVISORY`**. An `ADVISORY` row is evidence for the Steward about a column a
  future run will read; it enters **neither M nor U nor either STOP-THE-DESK limb** (§8) and can
  therefore never create a FAIL or block a PASS.

### 2.3 Exclusions — used, but not as a filter

No night is removed from the census. `exclusions_v003.json` enters only the **materiality** test, and
it enters it **per question**: materiality is evaluated against **the exclusions file each locked
PREREG itself cites**, not against v003 (DP-22 — a locked PREREG is not edited, so it still reads the
nights *its own* file leaves in). This is the substantive half of the test, not bookkeeping:
`exclusions_v003.json`'s own header records that **Q006 cites v001** and **Q007 cites v002**, while
2026-06-26 is excluded only from **v003** — so if that night falls inside either window and either
question reads a feature column on it, that is a material row by construction.

### 2.4 What is not read

No outcome column of any table (`outcome_*`, `level_hit_*`, `sas_excursion.*` excursion fields,
`uoa_symbol.fwd_return_*`) is read **as an outcome** anywhere. `outcome_corrections` is read as
*evidence about restatement* (Channel D appendix), never as a result. No price bar is read as a
return, a touch or an excursion. There is therefore nothing in this question that could be unsealed
by running it, which is why it can run on the sealed freeze today (§5.3).

## 3. Baselines — what the register is measured against

There are two, and both are documents, not cohorts. A diagnostic's baseline is the claim it is
auditing.

- **B1 — the declared availability.** `manifest_v001.availability` (and the freeze config it came
  from): each table's `available_time_et` and `lag_sessions`, plus the two corrections already written
  into it (`market_regime`: point-in-time only for `regime_version='v1.2'`, `trading_date ≥ 2026-06-09`;
  `sas_excursion`: variable lag, never a feature) and the declarative amendment in
  `exclusions_v003.sas_candidates_availability_note_correction`. The register asks, per column and per
  night, whether the observed write time is consistent with **B1**. B1 is the null: PASS means the
  declaration is true everywhere a locked question relies on it.
- **B2 — the prior sampled verdicts, as a positive control.** FREEZE_v001 §7's 11-row table, the KT
  audit's 4 re-run nights (2026-04-02, 04-24, 05-15, 07-02), the 2026-07-06 late `market_regime` write,
  the pre-2026-06-09 `market_regime` backfill, the 2026-01-07..2026-03-20 `uoa_symbol` / `gex_symbol` /
  `projection_bull` late block, the `gex_symbol` 05-13..05-15 within-night append, and the 2026-06-26
  stats_json disagreement. The census must **independently re-find every one of these** before any
  other line of its output is read (Gate 0, §4.1). A census that cannot re-find what a 20-row sample
  and two hand audits already found is broken, and its silence elsewhere means nothing.

## 4. Objective metric — the leakage register (this replaces the template's path objective)

Rule 5's price-path objective **does not apply**: no price path, no touch, no return and no entry
basis exist in this question, because no outcome is measured. DP-01, DP-03, DP-09, DP-11 and DP-12
are inapplicable for the same reason and are cited here only to record that they were considered.
DP-10, DP-20 and DP-44 (MPEs) are inapplicable: there is no effect size, and the register's threshold
is **zero rows**, fixed here.

### 4.0 Definitions, fixed before the run

- **Decision time** `D(N) = 16:05 ET on trading night N` (rule 14), America/New_York, DST-aware, N a
  NYSE session.
- **Declared write time** `A(T, N)` for table `T` on night `N` = `available_time_et` ET on `N`, from
  B1.
- **Use time** `U(T, N) = D(N + lag_sessions(T))` — the earliest decision a row dated `N` may inform.
- **Observed row write times.** The frozen parquet gives `created_at` and `updated_at` per row; **no
  table carries a per-column timestamp**, and that limitation is the reason the INDETERMINATE class
  below exists. `W_row = created_at`; `L_row = updated_at` (the last write of *some* cell in the row).
  `updated_at` null or equal to `created_at` resolves to `created_at`.
- **In-window.** A (question, table, column, night) tuple is in-window when the night falls inside
  that question's registered population window, the question reads that column **as a feature** (per
  its own §2/§4), and the night is not excluded by the exclusions file **that question cites**.

### 4.1 Gate 0 — positive control (run first, read first)

The script re-derives B2's items from the frozen parquet alone, with no hard-coded date list:
(a) runs whose `finished_at` is later than the next session's open (DP-04's own criterion) and, as
corroboration, runs with `started_at − created_at ≥ 12 h` (the benign late nights top out at 6.8 h —
KT_AUDIT §1); (b) per-night candidate `created_at` spread and its equality with the run's
`finished_at`; (c) `market_regime` rows whose `created_at` postdates their `trading_date` by more than
one session, and the multi-`regime_version` structure before 2026-06-09; (d) per-night median write
lateness by table across 2026-01..2026-03; (e) per-night disagreement between `sas_runs.stats_json`
counts and the frozen `sas_candidates` row set (Channel C). **If Gate 0 does not re-find every B2
item, the verdict is INCONCLUSIVE and no other section of the register is interpreted** (§8).

### 4.2 Channel A — write-time census (every row, every table, every night)

Per `(table, night)`: row count; rows with `W_row > A(T, N)` (declaration breach) and with
`W_row > D(N)`; rows with `L_row > U(T, N)` (post-use mutation); median and maximum lateness in hours;
the within-night spread of `W_row` (0 ⇒ single-batch write; > 0 ⇒ rows appended later, the
`gex_symbol` 05-13..05-15 signature). Printed in full for all 113 nights **and** for the pre-April
rows, per table, with no table omitted and no night summarised away.

### 4.3 Channel B — column-level materiality (the section that decides)

For every in-window `(question, table, column, night)` tuple, using H-069's definition verbatim —
*whether any cell on that night was written after that night's decision time, and that, and only
that, is "material"* — each tuple is classified into exactly one class:

- **MATERIAL** — `W_row > D(N)` for any row the question reads on that night (the write itself
  postdates the decision); **or** the column's late-write path is attributable from the platform repo
  (read-only, cited `path:line`) or from a manifest/exclusions correction, e.g. `market_regime` rows
  with `trading_date ≤ 2026-06-08` (wholesale backfill, PI-005), `uoa_symbol.oi_confirm_*` (declared
  lag 1), `uoa_symbol.score_swing` / `score_long` (mutated in place by the next-morning OI pass,
  PI-013, volatilx `services/uoa_screener.py:2236-2239`), or a candidate row whose `W_row` equals a
  DP-04-flagged run's `finished_at`.
- **MATERIAL_MITIGATED** — the question reads a MATERIAL column **through a reconstruction its own
  locked PREREG states**, which recovers the 16:05 value from data stored in the same frozen row (the
  only instance known at drafting: Q014 §2.1 dividing `score_swing` by `oi_confirm_mult`). The
  verification is fixed here so it cannot be argued at run time (decision 2): a tuple stays mitigated
  **only if** the script reproduces the 16:05 value **row by row on every in-window row — never a
  sample** — from cells stored in that same frozen row, to a **relative tolerance of 1e-6**. Any row
  where the reconstruction cannot be evaluated — a null or zero divisor (`oi_confirm_mult`), a missing
  multiplier column, or a mismatch outside tolerance — makes the **whole tuple MATERIAL**, not just
  that row. Mitigated tuples are itemised in full, named in the verdict sentence, and counted
  separately from M.
- **INDETERMINATE** — `W_row ≤ D(N)` but `L_row > D(N)`: the row was rewritten after the decision and
  the frozen data cannot say which cell. **Resolution step, registered:** the Steward reads the
  platform write path for that table (read-only repo, `path:line` cited) and, where the code names a
  closed set of columns the later pass writes, the tuple resolves to MATERIAL (column in the set) or
  IMMATERIAL (column not in the set). **Attribution uses the frozen parquet and the read-only platform
  repo at SHA `fa70688` only. No live query of any kind is run for this question** (rule 4, DP-50(c));
  where the code cannot close the column set, the tuple stays INDETERMINATE and is listed as
  `CONTAMINATION_UNRESOLVED`, with the register naming exactly what would resolve it (EN-015, EN-001,
  PI-013). A tuple's MATERIAL classification *is* this study's result, and a classification taken from
  a live row is not reproducible against the pinned parquet (decision 4). `U > 0` is INCONCLUSIVE by
  §8, so leaving a tuple unresolved cannot manufacture a PASS either.
- **IMMATERIAL** — a late write on a column no listed question reads as a feature (every outcome
  table, every post-hoc table, every unread column), or on a night outside every question's window, or
  on a night that question's own exclusions file removes. Counted and summarised, never itemised.
- **ADVISORY** (§2.2, decision 1) — a late-write pattern on a column that one of the four
  prospective-window questions (Q010, Q022, Q023, Q024) will read, found on a night outside that
  question's in-window range. Itemised and labelled, and **excluded from M, from U and from both
  STOP-THE-DESK limbs**. It is a note to the Steward, not a finding about this freeze.

The register prints **class counts for every column of every table**, always, and the MATERIAL,
MATERIAL_MITIGATED, CONTAMINATION_UNRESOLVED and ADVISORY sections **itemised in full** — table,
column, nights, row counts, and which QNNN reads it. No column may be omitted from the class-count
table; the decision rule in §8 is applied to whatever appears, never to a subset chosen afterwards.

### 4.4 Channel C — internal corroboration (the only channel that sees a traceless mutation)

2026-06-26 proved that a post-write mutation can leave a uniform `created_at` and no timestamp trace
at all; timestamps alone cannot find it. Per night: `sas_runs.stats_json`'s count fields
(`qualified_count`, `direction_counts`, and every other count field present) against the frozen
`sas_candidates` row set; the published count (`qualified IS TRUE AND selected_rank IS NOT NULL`,
DP-28) against the run's own audit; duplicate or gap-ranked `selected_rank`; and rows whose
`public_payload_json` is fully formed on a night whose run audit does not corroborate them. A
disagreement is **MATERIAL** for every in-window question on that night, on the publication predicate
columns, regardless of what the timestamps say.

### 4.5 Channel D — restatement anachronism in the pinned price freeze

A cell can also fail to have existed at 16:05 without ever being "written late", by being **restated**.
Two checks:

- **Split adjustment.** `factor(s, d) = p001_daily_raw.c / p001_daily_split.c`. A change in
  `factor(s, ·)` at date `d` is a corporate action whose adjustment was applied to *every earlier bar*
  at freeze time. Ratio features (returns, ATR%, beta60, runup20) computed inside a lookback window
  that contains no such `d` are invariant and **IMMATERIAL**. **MATERIAL** is the level case: a listed
  question that compares a **stored price level** — `entry_ref`, `signal_date_close`, `spot_close`, a
  ladder target, a stop, an invalidation price — against `prices_daily_split` bars for a symbol with a
  split date in `(N, 2026-09-10]`, because the stored level is in pre-split dollars and the bar is not.
  Every affected `(symbol, question, night)` is itemised. **A Channel D restatement row is MATERIAL
  like any other and counts in M** (decision 6): a split-restated stored level is a value that did not
  exist at 16:05, which is the hypothesis's own test rather than a second test, so DP-25 is not
  offended. Its escalation scope is fixed here — it counts toward STOP-THE-DESK limb **(b)** and
  enters limb **(a)** only if the restated column is one of the five named core selection columns,
  which a stored price level is not.
- **Value correction appendix.** `outcome_correction_ledger` (795 rows) is summarised by
  `table_name × field × was_sealed × correction_date` as evidence of how often frozen values are later
  restated (DP-50(a)). It touches outcome fields only, so it produces **no** material rows; it is
  printed because it is the desk's only direct measurement of restatement frequency.

`prices_hourly_raw` and `prices_daily_raw` carry no write timestamps and are not subject to Channel A;
that is stated in the register rather than passed over.

### 4.6 Channel E — declaration coverage (the validator gap, in data form)

Every column of every frozen table is classified **feature-eligible / outcome / metadata**, and each
feature-eligible column is checked for whether B1 declares availability at a granularity that covers
it. The known counterexample is `uoa_symbol`, declared "16:05, lag 0" as a table while its `oi_*`
columns are lag 1 and `score_swing` / `score_long` are mutated by the same next-morning pass (PI-013).
Every feature-eligible column whose true availability is not expressible in its table's declaration is
listed as a **declaration gap**, and the register's deliverable includes a **proposed column-level
availability block** for the next freeze config. Declaration gaps are reported; they do not by
themselves create material rows (a gap is a documentation defect until a question reads through it, at
which point Channel B has already caught it).

### 4.7 Inference

**None.** No estimate, no standard error, no bootstrap, no permutation, no p-value. Every number in
the register is a count of rows in a frozen file and is reproducible to the row by re-running the
script against the same sha256-pinned parquet. **DP-51 (episode-clustered CI) does not apply and no
episode clustering is computed**, for the stated reason that DP-51 attaches to a *primary endpoint's
confidence interval*, and this question has no primary endpoint and no CI — there is no sampling
distribution to cluster, because nothing is sampled.

## 5. Sample floors, expected n, window and decision date

### 5.1 Floors (rule 6)

Rule 6's floors — 20 contributing nights per cell, 80 per primary endpoint (DP-21) — exist to bound
the sampling variance of an estimate. **This question has no primary endpoint and takes no sample**,
so the floors do not bind in their usual form, and no floor is being waived: the census reads
**113 / 113 nights and 107,185 / 107,185 rows**, which is the strictest possible reading of any floor.
The one place counting still matters is reporting: any per-night or per-month count based on fewer
than 20 nights is labelled as such in the register and no trend is read from it.

### 5.2 Expected n

From the Steward's freeze report (`research/reports/FREEZE_v001.md` §1, sha256-pinned, no live query):
113 nights; 107,185 selection rows across 11 tables; 6,479 candidate rows of which 907 qualified and
915 published; 584,231 price rows across 436 symbols for Channel D. Non-excluded nights under
`exclusions_v003` are 102 (34 in-sample to 2026-05-29, 68 sealed from 2026-06-01) — that figure is an
**input to materiality**, not a census size. **No Steward exposure report is required and R1 is not a
lock condition**: nothing accrues, so there is no rate to measure and no projection to make.

### 5.3 Window — the sealed freeze, now (DP-31 applies)

The test window **is** the frozen period, **2026-04-01 .. 2026-09-10** (plus the pre-April rows the
frozen SQL carries in `uoa_symbol`, `gex_symbol`, `projection_bull` and `market_regime`), and the
question **runs on the sealed `manifest_v001` / `manifest_prices_v001` immediately**. This is not a
shortcut to a date: **DP-31's condition is met on its own terms — the hypothesis is itself about the
sealed period's integrity.** The object under test is whether *these* frozen rows were point-in-time;
a later freeze is a different object and cannot answer it. Rule 3 is satisfied because nothing in §2.4
is readable as an outcome: no verdict about any edge can move as a result of running this file, and
the sealed period stays sealed for every question that measures a price path.

### 5.4 Schedule (final; `schedule.json`)

**decision_date: Monday 2026-09-21 · extension_date: none · hard_stop: Monday 2026-10-05 ·
rule: fixed.**

- **2026-09-14/15** — lock (`--by desk`, DP-46). Population pinned at `manifest_v001` +
  `manifest_prices_v001`; no freeze work is required for the lock.
- **by Friday 2026-09-18** — the **Researcher** commits `eval.py`, written once from §4, with §2.2's
  question list transcribed and a loud failure on mismatch (decisions 1, 5).
- **Monday 2026-09-21** — the **Data Steward** runs it on the pinned parquet, Gate 0 first and read
  first (§4.1). One pass, no interim look (rule 9). Output:
  `research/reports/KT_REGISTER_manifest_v001.md`.
- **hard stop Monday 2026-10-05** — the outer bound on §8's Gate 0 fix-and-re-run loop (at most two
  passes, decision 7). Gate 0 still failing there ⇒ **INCONCLUSIVE**, ledgered as such, register filed
  incomplete, script defect to the Researcher.

**No extension exists.** DP-13's automatic extension and DEFERRED fallback answer "the floors came up
short at the decision date", and no floor can come up short on a census of already-mature,
already-frozen data; nothing accrues, so DP-43's exposure-driven schedule has no input (rule: fixed)
and its 12-month ceiling is not engaged — the decision date is 7 days after the lock. **No successor
freeze is needed** (DP-23 inapplicable — this question's population is complete at v001); what a
successor freeze does need is §9's standing re-run.

## 6. Split and stratification

- **Calendar panel:** the register is reported per month (2026-01 .. 2026-09, the pre-April months
  included where rows exist) and per night, as well as in total.
- **The three registered boundaries** are reported as explicit cuts, because each is a known
  discontinuity in the data's own provenance: **2026-06-01** (catalyst-layer regime change, DP-06,
  commit 69ef05f), **2026-06-09** (`regime_label_point_in_time_from`, PI-005), **2026-07-06** (the
  `uoa_symbol.fwd_return_*` write resumption, FREEZE_v001 §5). A late-write pattern that exists only
  on one side of a boundary is reported as bounded by that boundary and not generalised across it.
- **Rule 7 stratification is deliberately *not* by regime label before 2026-06-09,** and the reason is
  the question itself: `market_regime_daily` is one of the objects under audit there, so stratifying by
  it would assume the answer. For nights ≥ 2026-06-09 the `v1.2` label is carried as a descriptive
  stratum only. The point-in-time `sas_candidates.market_regime_snapshot` column is a *different
  object* (written with the candidate at 16:05) and the two are never conflated — conflating them is
  itself one of the leakage modes the register is looking for.
- **In-sample / out-of-sample** (`in_sample_end = 2026-05-29`) is reported as a third cut so the
  register can say whether contamination is concentrated in the half a question trains on.

## 7. Multiple testing

**No correction, because there is no test.** The register reports no p-value and no q-value: Gate 0 is
a reproduction check, not a hypothesis test, and every other output is a count of rows in a pinned
file. Q026 is filed in **F8** and, per the family's own header in `research/BACKLOG.md`, **enters no
BH correction set** (F8's correction runs across H-074, H-081 and H-083, the members that carry
primaries); Q026 neither joins that set nor changes any other family's denominator. The guard against
selective reporting is not a q-threshold but §4.3's rule that the class-count table is printed in full
for every column, always.

## 8. Decision rule (numeric, written before unsealing)

Let **M** = the count of MATERIAL tuples, **MM** = MATERIAL_MITIGATED tuples that failed the §4.3
row-by-row reconstruction check at relative tolerance 1e-6 (which are already counted in M by §4.3, at
tuple granularity), **U** = `CONTAMINATION_UNRESOLVED` tuples after the §4.3 resolution step.
**`ADVISORY` rows (§2.2, §4.3) enter neither M nor U nor either STOP-THE-DESK limb** and never move
the verdict. **Channel D MATERIAL rows count in M** and toward limb **(b)**, and enter limb **(a)**
only for the five named core selection columns (§4.5).

- **INCONCLUSIVE (Gate 0 first):** Gate 0 fails to re-find any B2 item ⇒ **INCONCLUSIVE** and the rest
  of the register is not interpreted. The script may then be fixed and re-run as a new pass — the fix
  is mechanical and is recorded with its diff and its date in the register; it is not tuning, because
  Gate 0's targets are fixed in §3 before the run. **The loop is bounded here: at most two Gate 0
  fix-and-re-run passes, all inside the hard stop Monday 2026-10-05** (decision 7; an unbounded
  fix-and-look loop is a look, rule 9, and DP-13 is inapplicable so no extension absorbs it). If Gate 0
  still fails at the hard stop, the verdict is **INCONCLUSIVE**, ledgered as such, the register is
  filed incomplete and the script defect goes to the Researcher. **No Gate 0 target is ever relaxed to
  make a pass succeed.**
- **PASS ⇒ controller verdict NULL (label `HISTORICAL_ONLY`):** Gate 0 passes, **M = 0 and U = 0**.
  Stated exactly: *no feature column any registered question reads was written after that question's
  decision time, on any night inside its window, on this freeze.* The register's IMMATERIAL and
  declaration-gap sections may be non-empty and the verdict still PASSes — that is what "material"
  means (H-069).
- **INCONCLUSIVE:** Gate 0 passes, **M = 0 but U > 0** — the timestamps cannot exclude contamination
  on `U` tuples and the platform code could not close the set. The register names the unresolved
  tuples and exactly what would resolve each one (a per-column write timestamp, EN-015; an append-only
  run history, EN-001; a point-in-time score column, PI-013). **U > 0 is INCONCLUSIVE, never PASS**
  (DP-45: the reading less likely to clear).
- **FAIL ⇒ controller verdict HISTORICALLY_CONFIRMED (the contamination is identified; label
  `HISTORICAL_ONLY`):** **M ≥ 1**. FAIL is **per-row and scoped**: the remedy in §9 attaches to the
  affected `(question, column, night)` tuples, not to the desk as a whole.
- **STOP-THE-DESK condition, fixed here numerically:** FAIL escalates to Haci's H0 consequence —
  *stop, repair the pipeline, re-run from zero* — when either (a) material rows cover **≥ 20% of any
  single question's in-window nights** on a core selection column (`overall_score`, `qualified`,
  `selected_rank`, `dominant_direction`, `best_timeframe`), or (b) material rows touch **≥ 5 of the 21
  listed questions**. Below both limits, the failure is scoped and the unaffected questions proceed.
  Neither limb counts an `ADVISORY` row; a Channel D material row counts in (b) always and in (a) only
  on one of the five core columns.
- **PROSPECTIVELY_CONFIRMED is unreachable from this run by design** (DP-31). The measured post-lock
  projection is **0 contributing nights**, exactly: the population is a freeze taken 2026-09-10, four
  days before this lock, and closed. There is no accrual and no waiting that would change it.
  **DP-31's successor-prospective-question clause resolves, here only, to §9's standing per-freeze
  register rather than to a successor PREREG**, and the reason is stated so it cannot be reused as a
  precedent: DP-31 exists to keep a *tradeable* verdict reachable without an interim look, and this
  question can never produce a tradeable verdict in either branch (§9 opening). The prospective track
  it protects does not exist for a diagnostic that reads no outcome.
- **No MPE applies.** The threshold is zero material rows, and it is fixed here.

## 9. If FAIL (and if PASS), what changes

**Opening, per DP-31 and rule 10: no guide line, no lane rule, no playbook entry, no product change,
no marketing claim and no quotable number follows from either verdict of this question.** Its verdict
carries the label **`HISTORICAL_ONLY`** wherever it is restated, ledgered or quoted, and every number
it produces is `NON_QUOTABLE` (rule 12). What it changes is the desk's own data handling and the
platform's plumbing.

**On FAIL, per material row, in this order:**
1. The affected question is **flagged to the Red Team for that question's review — never edited**
   (DP-22, rule 3). A locked PREREG stands as locked.
2. The Steward issues the next `exclusions_vNNN.json` with the contaminated nights excluded, or
   re-cuts that question's freeze with the contaminated **cells nulled**, whichever the row's channel
   calls for; drafts not yet locked cite the new file (DP-22).
3. **No verdict is ledgered on a contaminated pin.** A question already ledgered (Q005) gets a ledger
   note; a question not yet run does not run until its population is re-cut.
4. A `PLATFORM_ISSUES.md` entry is filed against the **writer**, not the reader (DP-07), with the
   `path:line` the resolution step attributed.
5. Channel D rows take a **desk-side** remedy rather than a platform one: level comparisons move to
   `prices_daily_raw`, or the price freeze is re-cut unadjusted for the affected symbols.
6. Channel E declaration gaps produce the **column-level availability block** for the next freeze
   config (a Steward artifact, not a platform change).

**On PASS:** the declared availability block is confirmed at census strength rather than sample
strength, and FREEZE_v001 §7's sampled row for each table is superseded by a counted one. PASS also
retires an excuse: after a census, "we sampled and it looked fine" is no longer the desk's standard of
evidence for knowledge time.

**In both branches — the standing per-freeze register (decision 3, registered here as a standing
Steward step):** the register is written to `research/reports/KT_REGISTER_manifest_v001.md` and
ledgered with this question, and **the byte-identical script runs at every subsequent freeze**, the
Steward publishing `KT_REGISTER_vNNN.md` with it. **The freeze protocol's 20-row knowledge-time sample
is retained alongside it, not retired:** it is the only check on the register's *own* script — a bug
gives a silent clean census, and Gate 0 catches a broken re-finder but not a mis-scoped column list —
and it costs 20 rows. `research/lib/freeze_config.json`'s `availability` notes are updated by the
Steward from the register's Channel E block at the next freeze; **Q026 edits nothing**. This standing
re-run is what DP-31's successor-question clause resolves to in §8, and what DP-50(a) requires,
because a successor freeze can disagree with its predecessor about the past. In both branches the
three platform controls the register depends on are recommended to Haci with their evidence attached — **EN-001** (append-only
SAS run history; without it a re-run night can be *detected* but never *recovered*), **EN-015**
(knowledge-time stamp on every displayed number), **PI-013** (a point-in-time copy of the UOA scores).
Per DP-48 the desk files them with a recommendation and the decision is Haci's; per DP-49 no brief
that follows hands the coding agent a database step.

## 10. Known threats to validity (registrar's own list)

1. **A timestamp is not a per-cell write time.** `updated_at` marks that *some* cell moved, not which.
   This is the single largest limitation and it is why INDETERMINATE exists as a class and why `U > 0`
   is INCONCLUSIVE rather than PASS. A PASS from this register means *no detectable* post-decision
   write on a read column — not a proof that none occurred.
2. **A traceless mutation is invisible to Channel A.** 2026-06-26 is the proof: 52 rows, one uniform
   `created_at`, a row set that its own run audit does not corroborate. Channel C is the answer to it,
   and Channel C only works where an independent count exists (`stats_json`). Tables with no internal
   corroboration — `uoa_symbol`, `gex_symbol`, `projection_*` — have **no** defence against this mode,
   and the register must say so per table rather than report a clean count.
3. **`sas_runs` is updated in place.** Re-run nights' original 16:05 output is unrecoverable from
   anything the desk can query (KT_AUDIT §1); the register can only exclude, never repair. EN-001 is
   the fix and it is not the desk's to make.
4. **The question list is frozen at this lock.** A question locked after 2026-09-14 is not in the
   register even if it reads a contaminated column. §9's standing per-freeze re-run is what closes that
   gap; until the next freeze, the coverage claim is bounded to the 21 named questions of §2.2.
5. **Materiality depends on each PREREG's own §2 being read correctly.** The feature-column list is
   extracted from 21 prose documents; a column a PREREG reads implicitly (inside a JSON blob, e.g.
   `context_json.gex_context` in Q021, or `public_payload_json` lane plans) is easy to miss. The
   register must list, per question, the columns it extracted, so the extraction is auditable and a
   miss is visible rather than silent.
6. **Reading the platform repo to attribute a write path is an interpretation.** The resolution step
   cites `path:line` and the code at the **frozen platform SHA
   `fa70688bc252d14f8d67e371afafc194731c324e`** (`git show fa70688:<path>`), never today's HEAD; a
   write path that changed between them would mis-attribute. The register prints the SHA it read at.
   This is the only attribution source there is: decision 4 forbids a live query even for provenance,
   so where the code at `fa70688` cannot close the column set the tuple stays unresolved (§4.3) and
   `U > 0` makes the verdict INCONCLUSIVE.
7. **Channel D's split check assumes the raw/split divergence is a split.** A dividend adjustment or a
   vendor restatement would look the same. The register reports the factor change and its date and
   does not name the corporate action.
8. **This is a diagnostic of one freeze, not of the platform.** A PASS says `manifest_v001` is clean
   where it is read; it says nothing about `manifest_v002`, and under DP-50 a repair shipped between
   the two can rewrite the same historical rows — `2d5776c` (PI-001, the `uoa_symbol_daily.fwd_return_*`
   backfill, merged 2026-09-14) is the live example, and it cannot reach a single row here only because
   the parquet was frozen 2026-09-10 and is sha256-pinned. **The gap closes through §9's standing
   per-freeze register, which is registered here as a Steward step — not through a promise.**
9. **A buggy script produces a silent clean register.** Gate 0 defends against a broken re-finder, but
   not against a mis-scoped column list or a mis-extracted feature list (threat 5). The other two
   defences are the **retained 20-row hand sample** (§9) and §4.3's rule that **no column may be
   omitted** from the class-count table, so an absent column is visible rather than silent.
10. **The Researcher/Steward split means the script's author never sees the frozen rows before writing
   it** (decision 5). That is an advantage for rule 9 and a handoff risk for §4's completeness, which
   is why **§4 is the only specification**: a gap in it is fixed by a dated amendment *before* the run,
   never during it.

## 11. Decisions before lock

Recorded in DECISIONS.md (2026-09-14). Routed items still open: **none**. All eight items are DECIDED
— six drafted here plus two raised by the Decision-maker; no item was defaulted on Haci's behalf and
none reached the ASK class. Item 4 was decided **against** the Registrar's recommendation, on
CLAUDE.md rule 4. Sections below are as amended by these decisions.

| # | Decision | Choice | Where it lives |
|---|---|---|---|
| 1 | Questions the register is keyed to | **A** — all 21 as §2.2 names them; out-of-window nights of Q010 / Q022 / Q023 / Q024 are `ADVISORY`, in neither M nor U nor either limb; §2.2 is authoritative and `eval.py` transcribes it, failing loudly on a mismatch | §2.2, §4.3, §8 |
| 2 | Column read through a documented reconstruction | **A, strict** — mitigated only if reproduced row by row on every in-window row to relative tolerance **1e-6**; null/zero divisor, missing multiplier or out-of-tolerance ⇒ the **tuple** is MATERIAL | §4.3, §8 |
| 3 | Standing per-freeze register | **A, minus the retirement** — byte-identical script at every freeze, `KT_REGISTER_vNNN.md`; the freeze protocol's **20-row sample is retained**, not retired; Q026 edits nothing | §9, §10.8, §10.9 |
| 4 | Provenance-only live query on an INDETERMINATE row | **B — forbidden** (against the Registrar's recommendation; rule 4, DP-50(c)). Attribution from the pinned parquet and the read-only repo at `fa70688` only; an unclosable set stays `CONTAMINATION_UNRESOLVED` ⇒ U > 0 ⇒ INCONCLUSIVE | header, §4.3, §8, §10.6 |
| 5 | Who writes the script | **A** — the **Researcher** writes `eval.py` once from §4 (rule 9); the **Steward** runs it | header, §5.4, §10.10 |
| 6 | Channel D rows in the verdict | **A** — MATERIAL like any other, counted in **M**; limb **(b)** always, limb **(a)** only on a core selection column | §4.5, §8 |
| 7 | Gate 0 re-run bound *(raised at decide)* | **At most two** fix-and-re-run passes, each recorded with its diff and date, all inside the hard stop **2026-10-05**; still failing there ⇒ INCONCLUSIVE; no target is ever relaxed | §5.4, §8 |
| 8 | DP-50 sweep at lock and the attribution SHA *(raised at decide)* | Immaterial to the population by construction (sha256-pinned parquet frozen 2026-09-10; `2d5776c` shipped after it); **not** immaterial to attribution, which reads `fa70688bc252d14f8d67e371afafc194731c324e` and prints it | header, §4.3, §10.6, §10.8 |

**Standing rules proposed from this question** (DECISIONS.md; Haci's to confirm later, none added as a
DP here): a census, not a sample, is the desk's knowledge-time standard and the two run together;
a live query never classifies a study row, not even for provenance; a "verified reconstruction" needs
its tolerance and its failure branch written before the run; a re-run loop is bounded at registration.
