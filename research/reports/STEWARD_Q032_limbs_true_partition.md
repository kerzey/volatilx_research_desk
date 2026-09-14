# Steward — Q032 re-entry: the lock-or-DEFER limbs on the TRUE §2.2 partition

_Generated 2026-09-14 from `manifest_prices_universe_v001.json` (SPY 2025-01-02..2026-09-10, 423 split-adjusted daily bars). **Counts only** — no outcome, no `E_t`, no `G`. INTERNAL / NON_QUOTABLE._

Nothing here is inherited from the SMA50-only proxy: the partition below is the registered §2.2 one, with the true `SMA50 > SMA200` trend and the true ≥ 250-session expanding volatility tercile.

## (e) The honest tercile start

- First session with ≥ 250 prior rvol sessions: **2026-02-02** — the registered window starts 2026-09-15, so every night in it is calibrated. The "never" finding is superseded.

- SPY bars: **423**, 2025-01-02 .. 2026-09-10. SMA200 defined from **2025-10-20**.

## The three rate limbs

Panel: **112** pick nights 2026-04-01..2026-09-10 over **112** elapsed sessions. t+40 maturity cutoff inside this freeze: **2026-07-15** (last bar 2026-09-10).

| limb | floor | t+40-matured | unmatured |
|---|---|---|---|
| (a) contributing nights / session | 0.4 | **0.5536** vs 0.4 — PASS | **0.9107** vs 0.4 — PASS |
| (b) rarer-arm nights / session | 0.1 | **0.2589** vs 0.1 — PASS (rarer = BENIGN) | **0.4018** vs 0.1 — PASS (rarer = HOSTILE) |
| (c) rarer-arm episodes / session | 0.025 | **0.0268** vs 0.025 — PASS | **0.0714** vs 0.025 — PASS |

- Arm split, t+40-matured contributing nights: **BENIGN** 29, **HOSTILE** 33 (rarer = **BENIGN**)
- Arm split, unmatured: **BENIGN** 57, **HOSTILE** 45
- Rarer-arm episodes: **3** matured, **8** unmatured
- Nights excluded by exclusions_v003: **10**; unlabelled (no arm): **0**; not t+40-matured in this freeze: **40**

## (d) Nine-cell composition — contributing nights (t+40-matured)

| trend | vol | nights | arm |
|---|---|---:|---|
| MIXED | HIGH | 3 | HOSTILE |
| UP | HIGH | 30 | HOSTILE |
| UP | LOW | 16 | BENIGN |
| UP | MID | 13 | BENIGN |

**4 of 9 cells observed** on this historical panel. Item 7's single permitted suppression revision is **cells added only**.

## Bound direction, against the superseded proxy

SMA50-only HOSTILE was a **lower** bound on true HOSTILE and SMA50-only BENIGN an **upper** bound on true BENIGN. The proxy read 22 of 68 nights HOSTILE (0.3099/session); the true partition reads **33** matured HOSTILE nights here. The proxy's numbers are recorded for the comparison and decide nothing.

