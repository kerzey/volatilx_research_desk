# STEWARD_Q030_universe_freeze — R2 feasibility check (Q030 lock gate)

**Run:** 2026-09-14, data-steward, desk run (autonomous) · **Request:** Q030 PREREG `research/questions/Q030_universe_discovery_recall/PREREG.md` §5.3 R2, routed by DECISIONS.md item 10 · **Scope:** feasibility and counts only — no outcome, no touch, no return, no excursion, no recall, no lift, no intersection count.

## Headline

**Limb (i) FAILS: `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` are ABSENT from this session's environment.** Checked directly (`[ -n "$ALPACA_API_KEY" ]` / `[ -n "$ALPACA_SECRET_KEY" ]`), stated explicitly rather than inferred, per the Q024 R1(d) precedent this request names. Because (i) fails, per the request's own instruction — *"if it cannot be built, say which limb fails and stop"* — **(ii) coverage and (iii) the freeze build were not attempted**: no Alpaca probe was run, no symbol list was narrowed, no coverage was estimated. `manifest_prices_universe_v001` does not exist and was not created.

**Per Q030 DECISIONS.md item 10 / the routed-request text: any limb failing → Q030 goes to `research/questions/DEFERRED.md`, unregistered, no `schedule.json`, with the failing limb named and the measured numbers printed.** Writing that entry is the Registrar's action (DECISIONS.md "registrar — conditional, fires only if R2's gate fails"), not this report's — it is deferred to the Registrar to apply against this finding. The rate limb (R1a, 0.6761/session, `STEWARD_Q027_exposure.md`) remains passed and is not the blocker; it is restated below only for completeness.

## (i) Credentials — ABSENT

```
ALPACA_API_KEY present: no
ALPACA_SECRET_KEY present: no
```
Checked with a direct presence test in the Steward's shell (no proxy, no inference from a prior report). Same failure mode as `STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md` §(d): the credentials this freeze needs are not provisioned in this environment.

## (ii) Coverage — NOT RUN (blocked by (i))

No trailing-60-session probe was attempted over the 2,405 symbols. No coverage share, no count/list of symbols returning zero bars, is reported, because none can be measured without a credentialed Alpaca call — estimating it from anything else is explicitly disallowed by the request.

**Pinned-blob re-verification (done — does not depend on credentials):** `volatilx` `data/sp500_sectors.json` at commit `4171b1a` (the Q022/Q024 pin), `mapping` key:
- entry count: **2,405** — matches the PREREG's pinned count exactly.
- sha256, LF-normalized: **`c4d12610ac95a8a83a0fc2365d02b4963d6a4169a9352acf2578164111390201`** — matches the PREREG's pinned hash exactly.
- No disagreement to flag.

## (iii) Build — NOT BUILT (blocked by (i))

`manifest_prices_universe_v001` was not built. Per the request: no partial build, no narrower symbol list, no back-fill/imputation substitute. Nothing was written to `research/data/`.

## (iv) Counts-only dry run, sealed pick nights 2026-06-01..2026-08-12

Per the coordinator's note: `m_t` needs universe bars (from the freeze that does not exist) and is **UNAVAILABLE**. On inspection, **`b_t` is likewise unavailable from pinned data alone**: §2.2 defines `b_t = |B_t|`, the gradeable base universe, requiring (a) ≥60 split-adjusted daily bars dated ≤t and (b) a bar on the pick night itself, for symbols of the full 2,405-symbol `B` — and no pinned freeze covers `B`. `manifest_prices_v001` (the only price freeze the desk holds) covers only 436 symbols (candidates + benchmarks), not `B`. So **both `b_t` and `m_t` are unavailable**; only `n_t` (candidate-universe ∩ `B`, no bar requirement) can be computed from `manifest_v001.sas_candidates` and the pinned blob alone. This is flagged as a correction to the coordinator's framing, not silently followed.

Computed from `research/data/v001_sas_candidates.parquet` (`trading_date`, `symbol`) intersected with the pinned blob's `mapping` keys, over pick nights 2026-06-01..2026-08-12 (51 nights carrying `sas_candidates` rows in that span):

| | nights | n_t min / median / max |
|---|---|---|
| raw (no exclusions applied) | 51 | 45 / 61.0 / 68 |
| after `exclusions_v003.json` (manual_runs ∪ non_session_runs ∪ uncorroborated_publication_runs) | 48 | 45 / 60.5 / 68 |

- **Nights with `n_t ≥ 1`: 48 of 48** (100%, post-exclusion) / 51 of 51 (raw). `n_t` is never zero in this window — the candidate universe always carries symbols, and virtually all are in `B`.
- **Nights with `m_t ≥ 1`: UNAVAILABLE** (no universe bars).
- **Nights excluded from the window by `exclusions_v003.json`: 3** — `2026-06-26` (uncorroborated_publication_runs), `2026-07-02`, `2026-07-06` (manual_runs).
- **As-filed residue** (candidate symbols outside `B`, §2.4/§4.3 companion, descriptive, counted not dropped): 7 of 51 nights carry a candidate symbol outside `B`; the entire residue across the window is **one distinct symbol, `BRK.B`** (a punctuation/ticker-format mismatch against the blob's `BRK-B`-or-equivalent key rather than a true non-`B` name — not investigated further here since it decides nothing and is outside this request's scope).

**So the desk cannot yet know whether `m_t ≥ 1` is ever binding** — that requires universe-wide bars, which requires the same credentials that block (i)–(iii).

## What was NOT done, by design

No touch, no first-touch date, no return, no excursion, no `outcome_*` column, no `sas_selection_excursion` read, no `uoa_symbol_daily.fwd_return_*` read, no recall, no lift, no intersection count. No live query against `$RESEARCH_DB_URL` was made (Alpaca is a market-data vendor read, the Steward's freeze exception; it was not reached because credentials are absent). Nothing was written outside `research/`. `research/lib/freeze_prices.py` was read but not edited — extending it to take an explicit symbol list is moot while limb (i) fails, and is not attempted here.

## Reply block

- **(i) Credentials:** **ABSENT** — `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` are both not present in the Steward's session environment.
- **(ii) Coverage:** **NOT MEASURED** — blocked by (i); no probe run, no share, no count/list.
- **(iii) Build:** **NOT BUILT** — blocked by (i); `manifest_prices_universe_v001` does not exist; no manifest path, no sha256, no rows.
- **(iv) Headline:** nights with `n_t ≥ 1`: **48 of 48** (post-exclusion; 51 of 51 raw), 2026-06-01..2026-08-12. Nights with `m_t ≥ 1`: **unavailable** (needs universe bars; `b_t` is unavailable for the same reason, contra the assumption that it could be read from `manifest_v001` + the blob alone).

**Failing limb, for the Registrar's DEFERRED entry:** **credentials** — `no ALPACA_API_KEY / ALPACA_SECRET_KEY in the Steward's environment, so manifest_prices_universe_v001 cannot be built`. The rate limb (R1a) passed at 0.6761/session and is not the blocker. Coverage is unmeasured, not failed, because the probe that would measure it never ran.
