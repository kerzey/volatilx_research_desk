---
name: daily-check
description: Morning operational check of last night's VolatilX pipeline output against trailing baselines. Run by the data-steward after the 16:05 ET nightly completes.
---
The check is a deterministic script. Run it and print its output verbatim:

    python research/lib/daily_check.py

For a past night: `python research/lib/daily_check.py --date YYYY-MM-DD`.

Credentials come from the environment: `RESEARCH_DB_URL` for the database, and the
`ALPACA_*` keys for the trading calendar (SPY's latest daily bar, market-data host only).

Do not recompute, re-flag or reinterpret anything — the script is the check, and running it
twice gives the same answer. Its rules, documented in the script's docstring:

- tolerance = max(2 × MAD, floor), with floors of 1 for counts, 2 percentage points for
  rates, and 2 points for scores;
- a value already seen in the trailing 20 nights is OK;
- RED = breakage (stale tables, missing rows, null spikes, zero published, inconsistent
  published rows, W60 grading backlog) — posted to Discord by the routine;
- AMBER = drift (score distribution, direction / timeframe / source mix, pick counts) —
  report only.

If asked about a RED line, name the table and column and stop. Do not interpret; do not
suggest fixes.
