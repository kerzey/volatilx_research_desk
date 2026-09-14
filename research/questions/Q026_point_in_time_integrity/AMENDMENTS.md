# Q026 — amendments to §4 (PREREG §10.10)

**Rule for this file (PREREG §10.10, threat 10):** §4 is the only specification. A gap in it is
fixed by a **dated amendment before the run, never during it**. Nothing here changes a threshold,
a filter, an exit rule or the decision rule; A1 below is a *gap*, not a re-design, and it is
**not resolved here** — the Researcher does not choose it.

Every entry is dated, names who may settle it, and says exactly what `eval.py` does with it today.

---

## A1 — BLOCKING. §4.0's decision-time boundary is inconsistent with §4's own baseline B1

> **STATUS UPDATE 2026-09-14: RESOLVED — `R2_SAME_EVENING`.** See "Amendments applied" at the foot
> of this file. The filing below is left exactly as the Researcher wrote it, as the record of the
> gap; it is no longer a description of the script's state.

**Filed 2026-09-14 by the Researcher, before any frozen row was read. Status: OPEN. `eval.py`
aborts in preflight and produces no register until this is settled.**

### The gap

§4.0 fixes `D(N) = 16:05 ET on trading night N` and §4.3 makes a tuple **MATERIAL** when
`W_row > D(N)` for any row the question reads on that night. §4.2 separately counts
`W_row > A(T, N)`, where `A(T, N)` is the declared `available_time_et` — which is `16:05` for
`sas_candidates`, `sas_runs`, `market_regime`, `uoa_symbol`, `gex_symbol`, `projection_bull` and
`projection_bear_v2`, i.e. **A = D for seven of the eleven tables**.

The desk's own documents, all of them cited by §3 as the B1 declaration or as B2 positive
controls, record that the nightly batch writes those rows **after 16:05 ET on the same evening**
and treat that as compliant, not as a breach:

- `research/reports/KT_AUDIT_manifest_v001_rerun_nights.md` §1: on the ~103 normal nights
  "candidate-row creation is 0.4–1.3h **after the 16:05 ET cutoff** at the 25th–75th percentile,
  consistent with a same-evening scheduled batch", and classifies exactly those nights as benign.
- `research/reports/FREEZE_v001.md` §7: `sas_candidates` "Confirmed — created_at/updated_at
  cluster same trading_date evening"; `sas_runs` "started_at/finished_at ~21:0x–21:1x UTC same
  day" (≈ 17:0x ET); `market_regime` v1.2 "created_at same-day ~20:05 UTC".
- `research/data/exclusions_v003.json`, `uncorroborated_publication_runs`: the 2026-06-26 batch
  carries "one `created_at` (2026-06-26 21:17:31.403724 UTC)" — 17:17 ET — and that file calls it
  "a single-batch write, not a re-run", i.e. a normal write.
- CLAUDE.md rule 5: the desk's own entry basis is "pick-night after-hours (from ~21:10 UTC)".

So under the literal §4.0 reading, **every row of every same-evening table breaches `D(N)` on
every night**, and therefore every in-window (question, table, column, night) tuple is MATERIAL by
limb one of §4.3. That reading is self-consistent but it makes §8 inoperative: `M = 0` becomes
unreachable, PASS becomes unreachable, both STOP-THE-DESK limbs fire on all 21 questions by
construction, and §3's B1 null ("PASS means the declaration is true everywhere a locked question
relies on it") can never be true. A rule under which the null is unreachable before any data is
read is not a pre-registered test, and §9's PASS branch would be dead text.

The opposite reading — that `available_time_et: "16:05"` labels *the nightly batch of night N*
rather than a literal clock — is what B1's own notes, FREEZE §7's verdicts and the exclusions
files' re-run criterion all use. But §4 never says so, and the choice decides the verdict.

### The three readings, enumerated (not chosen)

`eval.py` implements all three behind one constant. Exactly one may be selected, by amendment:

| id | boundary(N) | what it treats as "after the decision" | source of the reading |
|---|---|---|---|
| `R1_1605_LITERAL` | 16:05 ET on N | any write after 16:05 ET, including the same-evening batch | PREREG §4.0 as written |
| `R2_SAME_EVENING` | 23:59:59.999999 ET on N | a write dated on a later ET calendar date than N | FREEZE_v001 §7's "same trading_date evening" verdicts; manifest `availability` notes |
| `R3_NEXT_OPEN` | 09:30 ET on the next NYSE session after N | a write that lands after the next decision could have acted on it | DP-04; the `manual_runs` criterion in exclusions_v001/2/3; Gate 0(a) of §4.1 itself |

They are strictly ordered in permissiveness (R1 ⊂ R2 ⊂ R3) and they differ on real nights: e.g.
2026-05-01's run was created 2026-05-01 23:01 UTC and started 2026-05-02 05:51 UTC (KT_AUDIT §1),
which R2 flags and R3 does not; the same table's every ordinary night is flagged by R1 alone.

### What the script does today

`DECISION_TIME_RULE = None` and `DECISION_TIME_RULE_AMENDMENT = None` in `eval.py`. Preflight
aborts with the text of this amendment before Gate 0, before any parquet is opened, and writes no
register. Setting the constant requires **both** the rule id and a dated amendment citation, so a
rule can never be in force without a registered reason. The Steward does not set it at run time
(rule 9); the Researcher does not set it (this file); it is for the registrar / decision-maker, by
a dated amendment appended below, before Monday 2026-09-21.

`U(T, N)` and Channel A's `n_L_gt_U` use the same boundary function at `N + lag_sessions`, so the
post-use-mutation limb moves with the choice and cannot be left inconsistent with it.

### Why this is an amendment and not a Researcher's reading

Deciding it changes the verdict from a foregone FAIL + STOP-THE-DESK (R1) to a register that can
discriminate (R2/R3). PREREG decision 2's own precedent — "a 'verified reconstruction' needs its
tolerance and its failure branch written before the run, otherwise 'verified' is decided while
looking" — applies with more force to the boundary the whole classification turns on.

---

## Resolved in the script (recorded so the resolution is auditable, not to reopen §4)

Each of these is a place where §4 is silent on a mechanical detail that has **one** deterministic
reading consistent with §4's own text. Each is implemented, printed in the register, and named
here. None changes a threshold, a filter or the decision rule. If the registrar disagrees with any
of them, it is settled the same way A1 is — by a dated amendment before the run.

**A2 — `A(T, N)` where the declaration is not a clock.** Three tables declare
`available_time_et: "post-hoc"` (`sas_excursion`, `whale_ledger`, `outcome_corrections`). §4.2's
declaration-breach count is undefined for them. The script prints `n/a` for `n_W_gt_A` on those
tables and computes every other Channel A column normally. No listed question reads any of the
three as a feature, so the class is IMMATERIAL either way.

**A3 — `sas_excursion` carries no `created_at`/`updated_at`.** §4.0 assumes both exist on every
table. `sas_excursion` has only `computed_at`. The script uses `W_row = L_row = computed_at` and
says so in the register. It is an outcome table, never a feature (B1, FREEZE §7), so it cannot
produce a material row.

**A4 — the session calendar.** §4.0's `U(T, N) = D(N + lag_sessions)`, §4.1(a)'s "next session's
open" and Q014's five-session lookback all need a NYSE session list, which §4 does not name a
source for. The script derives it from the pinned files only: SPY's dates in
`p001_daily_split.parquet`, unioned with every `trading_date` in the eleven frozen selection
tables (the price freeze starts 2026-01-31 while the frozen selection SQL carries rows from
2026-01-02). Dates only — no bar value is read (§2.4). The derivation and the session count are
printed in the register.

**A5 — Gate 0(d) and the `gex_symbol` append have no stated threshold.** §4.1(a) fixes 12h for
the re-run corroboration; (d) and the 05-13..05-15 append item state no number. The script reuses
**12h** for both (median write lateness for (d), within-night `W_row` spread for the append), and
requires, for each of `uoa_symbol` / `gex_symbol` / `projection_bull`, **at least 20 nights**
inside 2026-01-07..2026-03-20 above that threshold — KT_AUDIT §3 measured 42–45 nights per table
at 15–70h, so 20 re-finds the block without hinging on either endpoint date. Targets are fixed
here, before the run, and §8 forbids relaxing any of them afterwards.

**A6 — what "reproduces the 16:05 value to rtol 1e-6" can mean.** There is no independent 16:05
ground truth in the frozen row, so the check is: the divisor `oi_confirm_mult` must be non-null,
non-zero, and inside the closed set {0.90, 1.00, 1.05, 1.10} that the code names at
`fa70688:services/uoa_screener.py:2223-2232`, and the round trip `(score / m) * m` must return
`score` within 1e-6 relative. Decision 2 governs the failure branch verbatim: a null or zero
divisor, a missing multiplier column, or any out-of-tolerance row makes **the whole tuple
MATERIAL**, not just that row.

**A7 — the per-question feature-column list is not mechanised by §4.** §4.0's "reads that column
as a feature (per its own §2/§4)" is an extraction from 21 prose documents (§10.5). The script
carries the Researcher's transcription with a citation per question, pinned by each question's
`prereg_sha256` (a changed PREREG aborts the run), printed in full in register §2.1, and backed by
an automated backstop: every backticked token in a listed PREREG that names a frozen column and is
**not** in the transcription is listed in `results/extraction_review.csv` as `EXTRACTION_REVIEW`.
The backstop never changes a classification; it makes a miss visible instead of silent (§10.9).
Two transcription conventions are recorded: (i) a column a PREREG scopes to an "exclusion audit
only" use is marked `as_feature=False` and is IMMATERIAL by §4.3's own wording, while
`sas_runs.finished_at` is marked as a feature everywhere because it decides population membership
and, in Q004, sets the entry price; (ii) where a PREREG names a table but no columns (Q021's
`gex_symbol`, Q023's `projection_bull`, the `market_regime` strata) every column of that table is
taken — the wider surface, DP-45.

**A8 — Channel C's "every other count field present".** §4.4 names `qualified_count` and
`direction_counts` and then generalises. The script fixes the analogue map before the run
(`qualified_count` → n(qualified) or n(published); `direction_counts` → direction counts over
either set; `candidate_count` / `candidates_count` / `total_candidates` / `scored_count` /
`universe_count` → n(rows)). Any other numeric count field is printed under
`uncompared_count_fields` and can never create a disagreement, because inventing an analogue at
run time would be judgment in the inner loop.

**A9 — which tables can close an INDETERMINATE set.** §4.3's resolution step resolves a tuple only
"where the code names a closed set of columns the later pass writes". The script asserts closure
for **`uoa_symbol` only**, with its evidence verified at `fa70688` (the OI confirmation pass at
`services/uoa_screener.py:2231-2239` and the forward-outcome backfill writing
`_ALL_OUTCOME_COLUMNS` at `:151-160` through the `setattr` at `:420`). Every other table leaves
its INDETERMINATE tuples as `CONTAMINATION_UNRESOLVED`, which is `U > 0`, which is INCONCLUSIVE
and never PASS (§8, DP-45). If a cited literal is not at its cited line at `fa70688`, the closure
and the attribution entry are **withdrawn** at run time and the withdrawal is printed (§10.6).

**A10 — what makes an out-of-window night "a late-write pattern" for ADVISORY.** §4.3's ADVISORY
class needs a pattern test. The script uses: any row on that night written after the boundary, or
any row whose later write crosses the boundary, or an attributed late-write path on that column.
ADVISORY rows enter neither M nor U nor either STOP-THE-DESK limb (§2.2, §8), so the test can
never move the verdict.

**A11 — the row set "the question reads" on a night.** §4.3 says "any row the question reads on
that night". Most listed questions read both published picks and the same-night unpublished
control pool, so the script uses **every row of that table on that night** for the materiality
test (the wider reading, DP-45) and uses each question's own publication predicate only to itemise
Channel D rows by symbol.

**A12 — `R3_NEXT_OPEN` at the last session of a freeze.** There is no next open for the final
session. The script falls back to the same-evening boundary, which is earlier and therefore flags
more, never less (DP-45), and records the fallback.

---

## Amendments applied

### 2026-09-14 — A1 RESOLVED: the §4.0 decision-time boundary is `R2_SAME_EVENING`

**Settled by:** decision-maker, autonomous mode (DP-40), 2026-09-14. **Status of A1: CLOSED.**
**Authority:** PREREG §10.10 — "§4 is the only specification; a gap in it is fixed by a dated
amendment *before* the run, never during it" — and A1's own line naming the registrar /
decision-maker as the settler. **PREREG.md is not edited** (DP-22, rule 3; it is hash-locked at
`c857dad6…87933`, state `DATASET_PINNED`). This amendment is written before any frozen row has
been read: `eval.py` has never been run, `results/` does not exist, and no number from this
question exists anywhere. Nothing below changes a threshold, a filter, an exit rule or the
decision rule of §8; it closes the one definition §4.0 left ambiguous and adds reporting.

#### The rule now in force

**`DECISION_TIME_RULE = "R2_SAME_EVENING"`.** For every night `N`:

> `boundary(N) = 23:59:59.999999 ET on N` (America/New_York, DST-aware). A write is "after the
> decision" when it is dated on a **later ET calendar date** than the night it is attributed to.

This boundary replaces the literal `16:05` clock **everywhere §4 compares an observed write time
to a decision time** — §4.2's `W_row > D(N)` column, §4.3's MATERIAL limb one, §4.3's
INDETERMINATE test `W_row ≤ D(N) < L_row`, and `U(T, N) = boundary(N + lag_sessions(T))` with
Channel A's `n_L_gt_U`, so the post-use-mutation limb moves with it and cannot be left
inconsistent (A1's own requirement). `D(N) = 16:05 ET` stands unchanged as the **decision moment**
itself (rule 14) and as `A(T, N)`'s declared clock in §4.2's separate declaration-breach count
`n_W_gt_A`, which is reported as before. §4.1's Gate 0(a) keeps DP-04's next-session-open
criterion, which is where that criterion belongs: it is a test about **runs**, not about rows.

#### Why R2 and not R1 (the literal reading)

1. **Rule 14's intent.** A feature is usable when it was available at or before the decision. The
   nightly batch of night `N` **is** the decision being recorded — its write latency is the time
   the platform takes to persist a 16:05 state, not the arrival of information from after 16:05.
   A candidate row flushed at 16:45 ET carries no fact that did not exist at 16:05; a row written
   on `N+1` may. R2 draws the line exactly there.
2. **Every source §3 cites reads it this way.** `manifest_v001.availability` verifies compliance
   with the words "created_at/updated_at cluster same trading_date evening" (`sas_candidates`,
   and the same construction on `conviction_monitor`); FREEZE_v001 §7 records `sas_runs` at
   ~21:0x–21:1x UTC "same day" as **Confirmed**; KT_AUDIT §1 classifies the 0.4–1.3h same-evening
   nights as **benign** and reserves "late" for the 19–51h re-runs; `DATA_NOTES.md` calls the
   Jan–Mar 15–70h block a breach of "declared 16:05 ET / lag-0 availability" and the same-evening
   17:17 ET write of 2026-06-26 "a single-batch write, not a re-run". B1 is the null (§3), and a
   boundary under which B1's own declaration is false on every row of seven of eleven tables is
   not a reading of B1 — it is a different declaration.
3. **R1 is degenerate, not strict.** Under R1, every in-window tuple on a same-evening table is
   MATERIAL by limb one, so `M = 0` is unreachable, §8's PASS branch and §9's PASS branch are dead
   text, §3's B1 null can never be true, and both STOP-THE-DESK limbs fire on all 21 questions
   **before any data is read**. An outcome fixed by the specification rather than by the data is a
   script-correctness failure of the kind Gate 0 exists to catch — the instrument must be able to
   produce both readings before its output is interpreted (§4.1, §10.9) — not a finding about the
   freeze. DP-45 is **not** an argument for R1 here and is not used as one: in this question
   HISTORICALLY_CONFIRMED *is* the FAIL branch, so "the option less likely to reach CONFIRMED"
   points at the most permissive reading, which is the opposite of conservative. DP-45's *intent*
   — never take the option that makes the desk's own claim easier — is honoured instead by taking
   the reading that **flags more of the two non-degenerate ones**, which is R2 (R2 ⊂ R3).

#### Why R2 and not R3 (the next-open reading), i.e. why R3 is too loose

1. **R3 clears the contamination §4.3 names by name.** `uoa_symbol.oi_confirm_*` and the in-place
   mutation of `score_swing` / `score_long` are written by the **next-morning OI pass**, before
   09:30 ET (PI-013, `services/uoa_screener.py:2236-2239`). §4.3 lists them as MATERIAL. Under R3
   their timestamps sit *inside* the boundary and limb one goes quiet; the rows survive only
   because the attribution limb rescues them. A boundary that needs the attribution limb to
   recover this question's flagship contamination case is the wrong boundary, and it would leave
   any unattributed next-morning write path invisible.
2. **It is false on the desk's own trading model.** DP-03(a) and rule 5 put the desk's entry at
   pick-night after-hours from ~21:10 UTC (≈ 17:10 ET). A value written at 03:00 ET on `N+1` is
   after a position taken on night `N` has already been entered. Calling it "available at the
   decision" cannot be right for a desk that trades that night.
3. **It duplicates Gate 0 instead of complementing it.** The next-session-open test is DP-04's
   *exclusion* criterion — "was this whole run re-made?" — and §4.1(a) already runs it at run
   level as a positive control. Importing it into §4.3's per-row materiality collapses two
   different questions into one and loses the per-row resolution the register exists to provide.
   KT_AUDIT §1's 2026-05-01 night (run created 2026-05-01 23:01 UTC, started 2026-05-02 05:51
   UTC) is the worked example: R2 sees it, R3 does not.
4. **R2 keeps every B2 positive control re-findable**, which is the empirical test of whether it
   is too loose: the 4 re-run nights (19–51h), the 2026-07-06 late `market_regime` write, the
   pre-2026-06-09 backfill, the Jan–Mar 15–70h block, the `gex_symbol` 05-13..05-15 within-night
   append (found by the `W_row` spread, not the boundary) and the 2026-06-26 `stats_json`
   disagreement (Channel C, timestamp-blind) are all still re-found. Gate 0 is therefore
   satisfiable under R2, and §8's INCONCLUSIVE-first branch keeps its teeth.

#### R2's residual blind spot, stated rather than passed over

Under R2, a write between 16:05 and 23:59:59 ET on night `N` is **not** flagged by the timestamp
limb. That band is covered by the other three defences, and the register must say so per table:
§4.3's attribution limb (a documented late-write path), Channel C's internal corroboration (the
only channel that sees a traceless mutation, §10.2), and §4.2's within-night `W_row` spread. Where
a table has no independent count (`uoa_symbol`, `gex_symbol`, `projection_*` — §10.2), the
register states that this band rests on attribution alone for that table. This is a limitation of
the amended rule and is added to the register's own limitations section; it does not change §10 of
the PREREG, which is not edited.

#### What the register must print (auditability; the verdict rule is unchanged)

The three boundaries differ only by two bands of rows, and counting those bands is three integer
comparisons per row. The register makes the choice auditable by printing them, and a reader can
see what any other boundary would have produced **without the verdict depending on it**:

1. **Channel A, per `(table, night)` and totalled per table, per month and overall** — alongside
   the existing columns: `n_W_gt_R1`, `n_W_gt_R2`, `n_W_gt_R3`, and the two band columns
   `n_W_band_R1_R2` (= `n_W_gt_R1 − n_W_gt_R2`; the same-evening batch band) and
   `n_W_band_R2_R3` (= `n_W_gt_R2 − n_W_gt_R3`; the overnight-before-next-open band). The same
   triple for the post-use limb: `n_L_gt_U` under each of the three rules. The in-force rule is
   named in the column header of the columns that decide.
2. **A `Boundary sensitivity` section** giving `M`, `MM`, `U`, `questions_touched`, and both
   STOP-THE-DESK limbs evaluated under each of R1 / R2 / R3, headed verbatim:
   `DESCRIPTIVE — DOES NOT DECIDE. The verdict is computed under R2_SAME_EVENING only
   (AMENDMENTS.md 2026-09-14, A1).` The R1 row carries the note that its `M` is bounded below by
   the count of in-window tuples on same-evening tables **by construction**, so it is a property
   of the rule and not a measurement.
3. **Header and `summary.json`** — `decision_time_rule`, `decision_time_rule_amendment`, and the
   count of nights where A12's R3 fallback fired (which now affects the R3 sensitivity column
   only).
4. **The verdict sentence names the boundary**, e.g. "…was written after the end of the ET
   calendar day on which the decision was made (`R2_SAME_EVENING`, AMENDMENTS.md 2026-09-14 A1)".

The rule is fixed here, before the run. **The sensitivity block may never be used to select a
rule after looking** (rule 9); a different boundary after the register exists is a look, and is a
successor question, never a re-run of this one.

#### Constants the Researcher sets in `eval.py` (no other edit)

```python
DECISION_TIME_RULE = "R2_SAME_EVENING"
DECISION_TIME_RULE_AMENDMENT = (
    "AMENDMENTS.md 2026-09-14 A1 RESOLVED: R2_SAME_EVENING "
    "(decision-maker, autonomous, DP-40; boundary(N) = 23:59:59.999999 ET on N)")
```

Plus the reporting in the four items above. Both constants and the reporting are committed by
**Friday 2026-09-18** (PREREG §5.4); the Steward runs the script **Monday 2026-09-21** and sets
nothing at run time (rule 9).

**Basis:** rule 14 (intent); §3's B1 sources (`manifest_v001.availability`, FREEZE_v001 §7,
KT_AUDIT §1, `exclusions_v003`, `DATA_NOTES.md`); §4.1 Gate 0 / §10.9 (an instrument whose output
is fixed before it reads is broken, not informative); DP-40 (settled by the desk, not put to
Haci); DP-45 by intent, not by its mechanical direction — the stricter of the two non-degenerate
readings. **Options not taken:** `R1_1605_LITERAL` (degenerate: PASS unreachable by construction);
`R3_NEXT_OPEN` (clears the next-morning OI pass §4.3 names as MATERIAL).

---

### 2026-09-14 — A2..A12 reviewed and CONFIRMED as implemented

All eleven stand. **None is overturned.** Three carry a rider, each of which only adds printing or
tightens an already-strict branch; no threshold, filter or decision rule moves.

- **A2, A3, A4, A5, A8, A9, A10, A11 — confirmed as written**, with no change. A5's 12h and
  ≥ 20-night targets are fixed by this confirmation and §8 forbids relaxing them afterwards. A11's
  "every row of that table on that night" is the wider reading and is confirmed as such.
- **A6 — confirmed, with A9's withdrawal convention extended to it.** If the closed divisor set
  `{0.90, 1.00, 1.05, 1.10}` is not at `fa70688:services/uoa_screener.py:2223-2232` at run time,
  the check cannot be evaluated; by decision 2's own failure branch the tuple is then **MATERIAL**
  (not mitigated, not skipped), and the withdrawal is printed as A9 requires. This is the stricter
  direction and closes the one gap A6 leaves.
- **A7 — confirmed, with one printing requirement.** Convention (i) narrows the surface (a column
  a PREREG scopes to "exclusion audit only" is `as_feature=False`), so it must be visible: register
  §2.1 itemises, per question, **every** column marked `as_feature=False` together with the PREREG
  sentence that scopes it, and those columns keep a row in the class-count table labelled
  `IMMATERIAL_BY_SCOPE` rather than being absent (§4.3: no column may be omitted). Convention (ii)
  (a table named without columns ⇒ every column) is the wider reading and is confirmed.
  `sas_runs.finished_at` stays a feature everywhere, as written.
- **A12 — confirmed, with its scope narrowed by A1's resolution.** With R2 in force, the last
  session's missing next open no longer affects the verdict; A12 now governs the **R3 sensitivity
  column only**, where the same-evening fallback applies and the fallback count is printed (item 3
  above).

---

**A1 is CLOSED. No amendment to this file remains open; `eval.py` may be completed and run on the
registered schedule.** Any further gap found in §4 before 2026-09-21 is filed here as A13+ and
settled the same way — dated, before the run, never during it.
