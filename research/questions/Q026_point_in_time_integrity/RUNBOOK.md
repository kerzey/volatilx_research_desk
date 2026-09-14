# Q026 — RUNBOOK (Data Steward, decision date Monday 2026-09-21)

**One pass. No interim look (rule 9). Gate 0 first and read first (PREREG §4.1).**

## Before you run

1. **A1 is CLOSED (2026-09-14).** The decision-maker settled the §4.0 decision-time boundary by
   dated amendment (`AMENDMENTS.md` "Amendments applied"; `DECISIONS.md` "## Amendments after
   lock"; autonomous, DP-40). The Researcher transcribed it into `eval.py` the same day:

   ```python
   DECISION_TIME_RULE = "R2_SAME_EVENING"
   DECISION_TIME_RULE_AMENDMENT = ("AMENDMENTS.md 2026-09-14 A1 RESOLVED: R2_SAME_EVENING "
       "(decision-maker, autonomous, DP-40; boundary(N) = 23:59:59.999999 ET on N)")
   ```

   `boundary(N) = 23:59:59.999999 ET on N`: a write is "after the decision" when it is dated on a
   **later ET calendar date** than the night it is attributed to. `D(N) = 16:05 ET` still stands
   as the decision moment and as `A(T, N)`'s clock in §4.2's separate `n_W_gt_A` column, and
   Gate 0(a) still uses DP-04's next-session-open criterion at **run** level.

   **Do not change either constant** (rule 9). The preflight gate is still live and still aborts
   before Gate 0 on an unset rule, an unknown rule id, or a rule id without its amendment
   citation. A different boundary after the register exists is a look, and is a successor
   question — not a re-run of this one.
2. **The register is written under R2 only.** §9 of the register prints a `Boundary sensitivity`
   block under R1 / R2 / R3. It is headed `DESCRIPTIVE — DOES NOT DECIDE` and it may never be
   used to pick a rule after looking. Read it as an audit of the choice, not as an option.
3. Nothing else is required. No live query, no new freeze, no exposure report (§5.2).
4. **Expect a longer run than a single pass.** A1r item 2 makes the script evaluate Channel B
   three times — once under each boundary — on the same frozen rows. Gate 0, Channel C,
   Channel D, the question windows and the reconstruction check are boundary-independent and are
   computed once. Nothing about this is a choice made at run time.

## The command

```
cd C:/Users/sahin/OneDrive/Desktop/VolatilX_Research_Desk
python research/questions/Q026_point_in_time_integrity/eval.py
```

Defaults, all overridable and all pinned by the PREREG for this run:

| flag | default |
|---|---|
| `--manifest` | `research/data/manifest_v001.json` |
| `--manifest-prices` | `research/data/manifest_prices_v001.json` |
| `--codebase` | `$CODEBASE_DIR`, else `C:/Users/sahin/Projects/volatilx` (read-only; the script runs `git show fa70688:<path>` only) |
| `--register` | `research/reports/KT_REGISTER_manifest_v001.md` |
| `--results` | `research/questions/Q026_point_in_time_integrity/results` |

Save stdout: `... eval.py > research/questions/Q026_point_in_time_integrity/results/run_<UTC timestamp>.json`
(the stdout block is the same JSON as `results/run_summary.json`).

For the standing per-freeze re-run (§9, decision 3) the **byte-identical** script takes the
successor paths, e.g.
`--manifest research/data/manifest_v002.json --manifest-prices research/data/manifest_prices_v002.json`,
and writes `research/reports/KT_REGISTER_manifest_v002.md`. Nothing about v001 is hard-coded in
the logic; the freeze protocol's 20-row knowledge-time hand sample is **retained alongside**, not
retired (decision 3).

## What it checks before it computes anything

Abort, with no register and no number, on any of: the amendment gate above (rule id set, known,
and carrying its dated amendment citation); Q026's own `PREREG.md`
sha256 ≠ the pinned lock hash; the §2.2 question list not matching the script's transcription (it
prints the diff); any listed question's `PREREG.md` sha256 ≠ the hash the column extraction was
made from; a manifest or parquet sha256 ≠ its pin; a declared row count ≠ the file's; the platform
repo not resolving `fa70688` to the full SHA; an exclusions file or block a question cites being
absent. The script opens no database connection anywhere (rule 4, DP-50(c), decision 4).

## Order of reading

1. `results/gate0.json` and register §1 — **Gate 0**. If it failed, stop: the verdict is
   INCONCLUSIVE, nothing else was computed, the register is filed incomplete, the defect goes to
   the Researcher, and at most **two** fix-and-re-run passes are allowed, all inside the hard stop
   **Monday 2026-10-05** (decision 7). No Gate 0 target is ever relaxed.
2. Register §0 verdict block, then §4 (Channel B) — the section that decides. The verdict
   sentence names the boundary it was computed under.
3. Everything else, in order. §9 `Boundary sensitivity` is descriptive and decides nothing;
   §10.1 states, per table, the band `R2_SAME_EVENING` does not see (16:05–23:59:59 ET on the
   night itself) and which of the other three defences covers it for that table.

## Outputs

- `research/reports/KT_REGISTER_manifest_v001.md` — the register (ledger it with Q026).
- `results/run_summary.json` and stdout — `verdict`, `M`, `MM_verified`, `MM_failed`, `U`,
  `advisory`, `stop_the_desk`, `n_nights`, `decision_time_rule`,
  `decision_time_rule_amendment`, `decision_time_boundary`, `a12_r3_fallback_nights`,
  `oi_mult_set_verified_at_sha`, `boundary_sensitivity`, plus
  `mean_oos`/`ci`/`p_perm`/`mpe` as `null`
  (§4.7: no estimate, no CI, no p-value, no MPE, no BH, no episode clustering).
- `results/nightly.csv` — one row per night (rule 6), including the three-rule band columns.
- `results/channel_a.csv`, `channel_b_class_counts.csv` (every column of every table),
  `channel_b_tuples.csv`, `channel_b_material.csv`, `channel_b_material_mitigated.csv`,
  `channel_b_contamination_unresolved.csv`, `channel_b_advisory.csv`, `channel_c.csv`,
  `channel_d_material.csv`, `channel_d_split_factor_changes.csv`,
  `channel_d_correction_appendix.csv`, `channel_e.csv`, `split_*.csv`,
  `proposed_availability_block.json`, `extraction_review.csv`, `preflight.json`,
  `reconstruction.json`, `SUMMARY.md`.
- **A1r additions (2026-09-14):** `boundary_bands_by_table.csv`, `boundary_bands_by_month.csv`,
  `boundary_bands_overall.csv` (`n_W_gt_R1/R2/R3`, `n_W_band_R1_R2`, `n_W_band_R2_R3`,
  `n_L_gt_U_R1/R2/R3`), `boundary_sensitivity.csv` (M, MM, U, questions_touched and both
  STOP-THE-DESK limbs under each rule), `a12_r3_fallback.json` (the A12 fallback nights, which
  affect the R3 sensitivity column only), and `as_feature_false_scoped.csv` (the A7 rider: every
  `as_feature=False` column with the PREREG sentence that scopes it).

`extraction_review.csv` is the §10.5 backstop: every backticked token in a listed PREREG that
names a frozen column and is not in the script's transcription. It changes no classification —
read it, and if it names a column a question really reads as a feature, that is a Researcher
defect to file, not something to patch during the run.

## Afterwards

`python research/lib/controller.py advance Q026 EVALUATED` (the Reporter interprets; every number
is `NON_QUOTABLE` and the verdict carries the label `HISTORICAL_ONLY`, §9).
