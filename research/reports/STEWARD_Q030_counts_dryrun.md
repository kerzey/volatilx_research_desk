# Steward — Q030 R2(iii): counts-only dry run on the sealed period

_Generated 2026-09-14 from `manifest_prices_universe_v001.json`. **Counts only.** `b_t`, `n_t`, `m_t` and the exclusion reasons — no `recall_t`, no `e_t`, no lift, and **no intersection `|M_t ∩ U_t^B|`**, which stays sealed until the registered decision date. INTERNAL / NON_QUOTABLE._

Window **2026-06-01 .. 2026-08-12**, 51 pick nights. Base universe `B` = **2405** symbols from the pinned blob `4171b1a:data/sp500_sectors.json` (sha256 `c4d12610ac95…`, hashed from committed bytes).

## What R2(iii) was asked: is `m_t >= 1` ever binding?

- Nights with `m_t = 0`: **0 of 51**  — the floor never binds on the sealed panel.

- `m_t` distribution: min **332**, median **886**, max **1328**, mean 883.5

- `n_t` distribution: min **45**, median **61**, max **68**

- `b_t` distribution: min **2342**, median **2355**, max **2375**

- Nights meeting every §2.5 contributing test: **48 of 51** = **0.9412** per pick night

- Base-universe coverage `|B_t|/2405`: min **97.80%**, median **98.54%** against the §2.5 **90%** gate

- Ungradeable share: max **0.76%** against the **10%** gate


## Per-night counts

| night | b_t | n_t | m_t | U_t_all | B_t_cov_pct | ungradeable | ungradeable_pct | fwd_sessions | contributing |
|---|---|---|---|---|---|---|---|---|---|
| 2026-06-01 | 2375 | 49 | 1149 | 49 | 99.21 | 11 | 0.46 | 20 | True |
| 2026-06-02 | 2375 | 45 | 1172 | 45 | 99.13 | 9 | 0.38 | 20 | True |
| 2026-06-03 | 2373 | 45 | 1328 | 45 | 99.13 | 11 | 0.46 | 20 | True |
| 2026-06-04 | 2373 | 48 | 1214 | 49 | 99.13 | 11 | 0.46 | 20 | True |
| 2026-06-05 | 2373 | 51 | 1314 | 52 | 99.13 | 11 | 0.46 | 20 | True |
| 2026-06-08 | 2373 | 52 | 1325 | 52 | 99.13 | 11 | 0.46 | 20 | True |
| 2026-06-09 | 2372 | 49 | 1167 | 50 | 99.13 | 12 | 0.5 | 20 | True |
| 2026-06-10 | 2371 | 49 | 1214 | 50 | 99.13 | 13 | 0.55 | 20 | True |
| 2026-06-11 | 2368 | 51 | 1071 | 52 | 99.09 | 15 | 0.63 | 20 | True |
| 2026-06-12 | 2369 | 52 | 970 | 52 | 99.04 | 13 | 0.55 | 20 | True |
| 2026-06-15 | 2365 | 50 | 1044 | 50 | 99.04 | 17 | 0.71 | 20 | True |
| 2026-06-16 | 2365 | 51 | 1111 | 51 | 98.96 | 15 | 0.63 | 20 | True |
| 2026-06-17 | 2365 | 51 | 1279 | 52 | 98.96 | 15 | 0.63 | 20 | True |
| 2026-06-18 | 2364 | 51 | 1135 | 51 | 98.96 | 16 | 0.67 | 20 | True |
| 2026-06-22 | 2362 | 53 | 1155 | 53 | 98.92 | 17 | 0.71 | 20 | True |
| 2026-06-23 | 2361 | 51 | 1032 | 51 | 98.88 | 17 | 0.71 | 20 | True |
| 2026-06-24 | 2361 | 50 | 894 | 51 | 98.84 | 16 | 0.67 | 20 | True |
| 2026-06-25 | 2359 | 54 | 840 | 55 | 98.79 | 17 | 0.72 | 20 | True |
| 2026-06-26 | 2357 | 52 | 634 | 52 | 98.75 | 18 | 0.76 | 20 | False |
| 2026-06-29 | 2358 | 52 | 710 | 52 | 98.71 | 16 | 0.67 | 20 | True |
| 2026-06-30 | 2359 | 47 | 787 | 47 | 98.75 | 16 | 0.67 | 20 | True |
| 2026-07-01 | 2357 | 52 | 666 | 52 | 98.63 | 15 | 0.63 | 20 | True |
| 2026-07-02 | 2358 | 61 | 609 | 61 | 98.59 | 13 | 0.55 | 20 | False |
| 2026-07-06 | 2356 | 62 | 639 | 62 | 98.59 | 15 | 0.63 | 20 | False |
| 2026-07-07 | 2355 | 63 | 695 | 63 | 98.54 | 15 | 0.63 | 20 | True |
| 2026-07-08 | 2355 | 68 | 877 | 68 | 98.54 | 15 | 0.63 | 20 | True |
| 2026-07-09 | 2355 | 60 | 853 | 60 | 98.5 | 14 | 0.59 | 20 | True |
| 2026-07-10 | 2355 | 59 | 891 | 59 | 98.5 | 14 | 0.59 | 20 | True |
| 2026-07-13 | 2355 | 65 | 871 | 65 | 98.46 | 13 | 0.55 | 20 | True |
| 2026-07-14 | 2355 | 64 | 931 | 64 | 98.34 | 10 | 0.42 | 20 | True |
| 2026-07-15 | 2355 | 66 | 912 | 66 | 98.25 | 8 | 0.34 | 20 | True |
| 2026-07-16 | 2353 | 67 | 786 | 67 | 98.21 | 9 | 0.38 | 20 | True |
| 2026-07-17 | 2352 | 64 | 857 | 64 | 98.21 | 10 | 0.42 | 20 | True |
| 2026-07-20 | 2349 | 62 | 969 | 62 | 98.21 | 13 | 0.55 | 20 | True |
| 2026-07-21 | 2348 | 65 | 920 | 65 | 98.13 | 12 | 0.51 | 20 | True |
| 2026-07-22 | 2348 | 63 | 1016 | 63 | 98.13 | 12 | 0.51 | 20 | True |
| 2026-07-23 | 2348 | 63 | 1074 | 63 | 98.09 | 11 | 0.47 | 20 | True |
| 2026-07-24 | 2348 | 63 | 1008 | 63 | 98.05 | 10 | 0.42 | 20 | True |
| 2026-07-27 | 2348 | 62 | 886 | 62 | 98.0 | 9 | 0.38 | 20 | True |
| 2026-07-28 | 2347 | 63 | 785 | 63 | 98.0 | 10 | 0.42 | 20 | True |
| 2026-07-29 | 2347 | 63 | 872 | 63 | 98.0 | 10 | 0.42 | 20 | True |
| 2026-07-30 | 2346 | 58 | 808 | 58 | 97.96 | 10 | 0.42 | 20 | True |
| 2026-07-31 | 2346 | 61 | 823 | 62 | 97.96 | 10 | 0.42 | 20 | True |
| 2026-08-03 | 2347 | 64 | 665 | 64 | 97.92 | 8 | 0.34 | 20 | True |
| 2026-08-04 | 2347 | 63 | 553 | 63 | 97.88 | 7 | 0.3 | 20 | True |
| 2026-08-05 | 2347 | 64 | 557 | 64 | 97.84 | 6 | 0.25 | 20 | True |
| 2026-08-06 | 2344 | 66 | 513 | 66 | 97.84 | 9 | 0.38 | 20 | True |
| 2026-08-07 | 2343 | 65 | 412 | 66 | 97.84 | 10 | 0.42 | 20 | True |
| 2026-08-10 | 2342 | 61 | 379 | 62 | 97.84 | 11 | 0.47 | 20 | True |
| 2026-08-11 | 2343 | 64 | 354 | 65 | 97.84 | 10 | 0.42 | 20 | True |
| 2026-08-12 | 2342 | 68 | 332 | 68 | 97.8 | 10 | 0.43 | 20 | True |

## Excluded runs inside the window (exclusions_v003)

- `manual_runs`: 2 inside the window — 2026-07-02, 2026-07-06
- `non_session_runs`: 0 inside the window
- `uncorroborated_publication_runs`: 1 inside the window — 2026-06-26

## Open item for the lock

PREREG §2.2 names **ATR14** without naming its smoothing. This dry run used Wilder (`alpha = 1/14`). Simple-mean ATR14 gives a different mover level and therefore a different `m_t`. **The registrar must fix the smoothing in §2.2 at `apply` time** so `eval.py` is not left to choose it. This is a counts artefact only; no outcome was read.

