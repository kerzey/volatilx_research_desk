# Q026 — RUNBOOK (Data Steward, decision date Monday 2026-09-21)

**One pass. No interim look (rule 9). Gate 0 first and read first (PREREG §4.1).**

## Before you run

1. **A1 must be closed.** `AMENDMENTS.md` A1 is OPEN as of 2026-09-14: PREREG §4.0's
   `D(N) = 16:05 ET` is inconsistent with §4's own B1 declaration and B2 controls, and the
   choice decides the verdict. Until the registrar / decision-maker appends a dated amendment and
   sets, in `eval.py`,

   ```python
   DECISION_TIME_RULE = "R1_1605_LITERAL" | "R2_SAME_EVENING" | "R3_NEXT_OPEN"
   DECISION_TIME_RULE_AMENDMENT = "AMENDMENTS.md <date> A1 resolved: <one sentence>"
   ```

   the script **aborts in preflight, opens no parquet and writes no register**. That is intended.
   Do not set it yourself (rule 9), and do not run the script to "see what happens".
2. Nothing else is required. No live query, no new freeze, no exposure report (§5.2).

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

Abort, with no register and no number, on any of: the amendment gate above; Q026's own `PREREG.md`
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
2. Register §0 verdict block, then §4 (Channel B) — the section that decides.
3. Everything else.

## Outputs

- `research/reports/KT_REGISTER_manifest_v001.md` — the register (ledger it with Q026).
- `results/run_summary.json` and stdout — `verdict`, `M`, `MM_verified`, `MM_failed`, `U`,
  `advisory`, `stop_the_desk`, `n_nights`, plus `mean_oos`/`ci`/`p_perm`/`mpe` as `null`
  (§4.7: no estimate, no CI, no p-value, no MPE, no BH, no episode clustering).
- `results/nightly.csv` — one row per night (rule 6).
- `results/channel_a.csv`, `channel_b_class_counts.csv` (every column of every table),
  `channel_b_tuples.csv`, `channel_b_material.csv`, `channel_b_material_mitigated.csv`,
  `channel_b_contamination_unresolved.csv`, `channel_b_advisory.csv`, `channel_c.csv`,
  `channel_d_material.csv`, `channel_d_split_factor_changes.csv`,
  `channel_d_correction_appendix.csv`, `channel_e.csv`, `split_*.csv`,
  `proposed_availability_block.json`, `extraction_review.csv`, `preflight.json`,
  `reconstruction.json`, `SUMMARY.md`.

`extraction_review.csv` is the §10.5 backstop: every backticked token in a listed PREREG that
names a frozen column and is not in the script's transcription. It changes no classification —
read it, and if it names a column a question really reads as a feature, that is a Researcher
defect to file, not something to patch during the run.

## Afterwards

`python research/lib/controller.py advance Q026 EVALUATED` (the Reporter interprets; every number
is `NON_QUOTABLE` and the verdict carries the label `HISTORICAL_ONLY`, §9).
