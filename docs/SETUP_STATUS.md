# Research desk — setup status (2026-09-10)

Setup performed against README Steps 1–7. Repo lives at
`C:/Users/sahin/OneDrive/Desktop/VolatilX_Research_Desk` (the README still says
`C:/Users/sahin/Projects/volatilx-research` — the Step 10 `schtasks` paths are wrong for
this location).

## How to start the desk

```bash
./scripts/start_desk.sh              # Git Bash
./scripts/start_desk.sh --admin      # maintenance session (enforcement code writable)
```
```powershell
.\scripts\start_desk.ps1             # PowerShell
.\scripts\start_desk.ps1 -Admin
```

Both load `.env.research` first. The Git Bash launcher runs Claude Code under `winpty`:
the binary is a native Windows console `.exe`, and when Git Bash starts it its stdin is an
MSYS pipe rather than a console, so it detects no TTY, falls back to `--print` mode and dies
with *"Input must be provided either through stdin or as a prompt argument"*. That was the
startup failure. PowerShell gives it a real console, so it needs no wrapper.

## Verified working

| Check | Result |
|---|---|
| Read-only DB role | `sas_research_ro` → `prodvolatilx…/postgres`. `UPDATE` = permission denied for table; `CREATE TABLE` = permission denied for schema public. Grant-level, not session-flag. |
| Freeze config tables | All 11 exist in schema `public`. |
| Python deps | psycopg, pandas, pyarrow, scipy, azure-storage-blob, openai — all import (system Python 3.13.14, no venv). |
| OpenAI second opinion | Key valid; `gpt-6-astra` visible on the account. |
| Controller | `init` / `advance` / `show` work. Q001 at PREREG_DRAFT. |
| status.py | Works (`--full`). |
| Freeze | manifest_v001, 11 tables, 107,185 rows, `--verify` OK, platform SHA recorded. |
| Platform-repo guard | Live — verified blocking a redirect, `sed -i` and `git commit` into the platform repo, while allowing `git log` and `grep`. |

## Fixed

- **`.env.research`** (backup: `.env.research.bak`, gitignored):
  - `RESEARCH_DB_URL` / `BACKFILL_DB_URL` were SQLAlchemy-style `postgresql+psycopg2://`,
    which `psycopg.connect()` cannot parse — nothing would have connected. Now `postgresql://`.
  - `OPENAI_API_KEY = value` (spaces around `=`) broke `. ./.env.research`. Normalised.
  - `CODEBASE_DIR` was absent. Added.
- **`.claude/settings.json`**:
  - The four `Write(...)` deny rules produced startup warnings and matched nothing —
    only `Edit(path)` rules are consulted by file-permission checks, and each already had an
    `Edit(...)` twin. Removed. Comments removed so the file is valid JSON again.
  - Added an `env` block setting `CODEBASE_DIR`. Previously it was only set if you happened
    to launch from a shell that had sourced `.env.research`; when empty, `guard_bash` skipped
    its entire platform-codebase protection. Now it holds however Claude Code is started.
- **`scripts/research_routines.sh`** sourced `.env` (nonexistent, and the forbidden filename)
  instead of `.env.research` — the scheduled routines would have run with no credentials.
- **`research/lib/freeze_config.json`** — corrected by the data-steward during the freeze
  (see `research/reports/FREEZE_v001.md`).
- **`scripts/start_desk.sh` / `.ps1`** — new launchers (above).

## Open — you must apply these

1. **Install the guard patches: `docs/guard_patches/`.** Two real defects, both proven with a
   33-case suite. (a) The identity-gated rules in both guards never execute, because Claude
   Code 2.1.267 does not populate `agent_type` for subagent calls — 12 of 33 cases fail
   against the installed guards, including the SQL-write check README Step 4 says must block.
   (b) A latent Windows path-separator bug in `guard_write.py` that, the moment identity
   starts working, would reject *every* desk-agent write as "outside research/". Apply
   instructions and the full rationale are in `docs/guard_patches/README.md`. I could not
   install them myself — edits to security-hook scripts are blocked here by the auto-mode
   classifier and by the repo's own `Edit(.claude/**)` deny rule.

2. **Remove `BACKFILL_DB_URL` from `.env.research`.** A second DB credential, outside the
   CLAUDE.md rule-1 allowlist; sourcing the env file puts it in every agent's shell. The
   patched guard adds it to `FORBIDDEN_CREDS`, but the credential should not be there at all.
   Not touched or tested during setup.

3. **Decide the push-to-main policy.** `guard_bash`'s message claims pushes to main/master are
   blocked; the regex only catches force pushes, and `settings.json` *allows*
   `Bash(git push origin main*)`. Pick one.

4. **Azure blob was never set up** (README Step 3.2). `az` CLI is not installed. The env file
   uses different names (`PROD_SAS_TOKEN`, `RESEARCH_SAS_TOKEN`, `PROD_BLOB_ENDPOINT`,
   `RESEARCH_CONTAINER`) than CLAUDE.md's `PROD_BLOB_SAS` / `RESEARCH_BLOB_SAS`.
   Non-blocking: no desk code reads any blob variable today.

5. **Step 10 routines not scheduled**; the README's `schtasks` commands point at the old path.

6. **CLAUDE.md's "known data issues" line is out of date** — it records the May–June 2026
   fwd_return freeze as *fixed*. It is not (below).

## Findings from the first freeze that affect Q001

- **`market_regime_daily` has no point-in-time label before 2026-06-09.** Every row for
  2026-01-02 … 2026-06-08 was backfilled on 2026-06-02/06-08. CLAUDE.md rule 7 requires
  every result be stratified by point-in-time regime; only ~65 nights (2026-06-09 → 09-10)
  can satisfy that. The steward's provisional `in_sample_end` of 2026-05-29 puts the entire
  in-sample half inside the non-compliant period. Resolve before locking Q001.
- **The uoa fwd_return freeze is live, not fixed** — ~95% below baseline, with a
  `fwd_return_30d_pct` relapse to 0% from 2026-07-27 that right-censoring does not explain.
  The coverage watchdog is not catching it. Platform-side; candidate for an implementation brief.
- **Q001's control universe is ungraded.** Unpublished candidates at score ≥ 70 have 0 sealed
  W60 outcomes and 1.3% any-return coverage, so `eval.py` must join prices independently
  rather than shortcut through `outcome_return_*`.
