# FMP insider-trading feasibility check for H-022 (Steward, read-only, 2026-09-15)

Scope: feasibility only. No manifest written, no freeze, no `freeze_config.availability`
entry, no outcome read, nothing this file says may be quoted in a PREREG under Rule 4 --
this is a live probe of the FMP API for the Steward's own use, per
`research/data/DATA_NOTES.md` "External source: Financial Modeling Prep". `FMP_API_KEY`
loaded via `research/lib/desk_env.py`; presence confirmed, value never printed. Docs
fetched read-only from `https://site.financialmodelingprep.com/developer/docs/stable`
(GET only); API probed read-only against `https://financialmodelingprep.com/stable/...`
(GET only, key redacted from every URL below). No FMP payload was written under
`research/`; the raw JSON pulled into session scratch space during this check has been
deleted.

## Decision paragraph

**Partly.** FMP's stable-tier insider-trading endpoints (`insider-trading/search`,
`insider-trading/latest`, `insider-trading/statistics`) supply full per-symbol Form 3/4/5
history back to 2013-2020 depending on symbol, with reporting-owner CIK, transaction
code (the full SEC letter-code set, including `P-Purchase`), transaction date, shares
and price -- most of DEFERRED.md H-022 condition 1's field list. But every row carries
only a `transactionDate` and a `filingDate`, both calendar dates with no time-of-day
component. There is no SEC acceptance date-time anywhere in the payload. That is
the specific blocker DEFERRED.md names ("no Form 4 insider-transaction history with
filing/acceptance timestamps"), and FMP does not close it. Two consequences: (1) the
Steward cannot declare a `freeze_config.availability` acceptance-datetime lag for this
source, because the field does not exist to declare a lag on; (2) a same-day-conservative
treatment is the only knowledge-time rule available, and it is a weaker substitute, not a
fix -- SEC acceptance can run up to two business days after `filingDate` per EDGAR's own
model, and FMP's `filingDate` is not documented as acceptance-equivalent. If the desk
wants to proceed anyway, the only defensible knowledge-time rule is: a filing is usable
on pick night t only if `filingDate` is more than 2 trading sessions before t (a 2-session
conservative buffer standing in for the undocumented acceptance lag), dated by
`filingDate` never `transactionDate`, and the rule itself would need re-verification
against true SEC EDGAR acceptance timestamps before any PREREG cites it -- which points
at EDGAR's own filing index (the `url` field in every row already links there) as the
real fix, with FMP usable at most as a discovery/backfill index over it. FMP alone does
not lift the H-022 blocker as DEFERRED.md's condition 1 defines it.

## Endpoints found (docs: `/developer/docs/stable`, section "Insider Trades")

- Search by symbol: `GET https://financialmodelingprep.com/stable/insider-trading/search?symbol=<SYM>&page=<n>&limit=<n>`
- Latest (cross-symbol feed): `GET https://financialmodelingprep.com/stable/insider-trading/latest?page=<n>&limit=<n>`
- Statistics: `GET https://financialmodelingprep.com/stable/insider-trading/statistics?symbol=<SYM>`
- (found, not requested -- out of this task's scope) Search by reporting name:
  `GET https://financialmodelingprep.com/stable/insider-trading/reporting-name?name=<name>`
- (found, not requested) Acquisition ownership: `GET https://financialmodelingprep.com/stable/acquisition-of-beneficial-ownership?symbol=<SYM>`
- Transaction-type code list: `GET https://financialmodelingprep.com/stable/insider-trading-transaction-type`

Legacy note: the v3 endpoint (`/api/v3/...`) is dead for this account -- it returned
HTTP 403 with body: "Legacy Endpoint: ... only available for legacy users who have valid
subscriptions prior August 31, 2025." The desk's key is on the post-migration "stable"
tier; all probing below used `/stable/`.

## Field table (identical schema on `search` and `latest`; verified as the union of keys
across all rows pulled for the 5 symbols)

| field | present | notes |
|---|---|---|
| `symbol` | yes | |
| `filingDate` | yes | date only (`YYYY-MM-DD`), no time-of-day |
| `transactionDate` | yes | date only, no time-of-day |
| acceptance date/time | no | not present under any key name; not `acceptedDate`, not in `url`'s visible text (the linked SEC EDGAR index page would carry it, but FMP does not surface it) |
| `reportingCik` | yes | stable per-insider id -- satisfies that part of condition 1 |
| `companyCik` | yes | |
| `reportingName` | yes | |
| `typeOfOwner` | yes | free text, e.g. director, officer: CEO |
| `transactionType` | yes | letter-dash code, e.g. `P-Purchase`, `S-Sale` (full code list below) |
| `acquisitionOrDisposition` | yes | A/D, blank on Form 3 rows with no transaction |
| `directOrIndirect` | yes | |
| `formType` | yes | `3`, `3/A`, `4`, `4/A`, `5` all observed -- not Form-4-only; a consumer must filter `formType` to `4`/`4/A` to match DEFERRED.md's Form-4 scope |
| `securitiesTransacted` | yes | 0 on non-transaction Form 3 rows |
| `securitiesOwned` | yes | |
| `price` | yes | 0 on grants/RSUs |
| `securityName` | yes | |
| `url` | yes | links to the SEC EDGAR filing index page (itself carries the true acceptance datetime, unfetched here -- out of scope, live SEC pull) |

Full transaction-type code list from `insider-trading-transaction-type` (18 codes):
A-Award, C-Conversion, D-Return, E-ExpireShort, F-InKind, G-Gift, H-ExpireLong,
I-Discretionary, J-Other, L-Small, M-Exempt, O-OutOfTheMoney, P-Purchase, S-Sale,
U-Tender, W-Will, X-InTheMoney, Z-Trust.

Statistics endpoint (`insider-trading/statistics?symbol=AAPL`) is a per-quarter rollup --
`year`, `quarter`, `acquiredTransactions`, `disposedTransactions`,
`acquiredDisposedRatio`, `totalAcquired`, `totalDisposed`, `averageAcquired`,
`averageDisposed`, `totalPurchases`, `totalSales` -- no per-transaction detail, no dates
finer than quarter. Not usable for the per-transaction classifier condition 1 requires;
useful only as a cross-check aggregate.

## Pagination / row cap

- `limit` is honored up to 1000 rows per page; a request for `limit=100000` silently
  returned exactly 1000 rows (AAPL: `page=0&limit=1000` gave 1000 rows, oldest
  2018-08-08; `page=1&limit=1000` gave the next 1000 rows, oldest 2014-03-03 --
  confirms pagination continues correctly beyond the 1000-row cap rather than truncating
  history).
- `from` / `to` / `date` query parameters are accepted but silently ignored on
  `insider-trading/search` -- a request with `from=2026-01-01&to=2026-01-10` returned the
  same 100 most-recent rows as no date params at all, spanning 2025-10-15 to
  2026-09-08. There is no server-side date-range filter on this endpoint. A
  full-window pull is pagination-plus-client-side-filter only, not a single scoped call.
- No `X-RateLimit-*` response headers observed on any call. A burst of 15 sequential
  calls completed in 3.7s with all 200s -- no 429 encountered at that rate. No pricing
  page consulted; this is an empirical note only, not a documented limit.

## Per-symbol counts (study window 2026-04-01..2026-09-14; `search?symbol=<SYM>&page=0&limit=1000`, one page sufficed for all five -- the oldest row on page 0 already predated the window)

| symbol | rows in window | window date range (actual) | transaction types present in window | oldest row pulled (page 0) |
|---|---|---|---|---|
| SNDK | 79 | 2026-04-20 .. 2026-09-08 | F-InKind, G-Gift, M-Exempt, S-Sale | 2013-02-15 |
| COIN | 154 | 2026-04-16 .. 2026-09-08 | (blank, Form 3 rows), A-Award, F-InKind, M-Exempt, S-Sale | 2024-02-20 |
| META | 329 | 2026-04-13 .. 2026-09-09 | A-Award, C-Conversion, F-InKind, G-Gift, M-Exempt, S-Sale | 2025-06-24 |
| AAPL | 55 | 2026-04-01 .. 2026-09-08 | (blank, Form 3 rows), A-Award, F-InKind, G-Gift, M-Exempt, S-Sale | 2018-08-08 |
| SWKS | 27 | 2026-05-13 .. 2026-09-08 | A-Award, F-InKind, M-Exempt | 2020-05-06 |

Zero P-Purchase rows in the study window for any of the five symbols. This is a
first, non-registered data point consistent with, but not a substitute for, DEFERRED.md
condition 2's required counts-only exposure probe ("Exposure ... is unmeasured and is
likely the next blocker") -- that probe must run across the full published plus
unpublished candidate pool on a pinned freeze, not five hand-picked symbols. The blank
transaction-type rows are Form 3 (initial ownership statement, no transaction) rows,
correctly blank per SEC convention, not a data defect -- but they confirm `formType`
filtering is required before any P/S classification.

## What would still be needed to lift the H-022 blocker

FMP supplies reporting-owner CIK, transaction code (including P), transaction date,
shares/price, and full symbol history -- most of condition 1's field list. It does not
supply the acceptance datetime condition 1 requires, and does not support server-side
date-range scoping (full-window pulls must paginate and filter client-side). The routine/
opportunistic classifier itself (36+ months of per-insider history) is buildable from
what FMP returns; the point-in-time gate on top of it is not, without either (a) a
documented, defensible proxy-lag policy substituting for the missing acceptance time, or
(b) pulling the acceptance datetime from the SEC EDGAR filing index each `url` already
points to. Recommendation to the registrar: this is a partly -- worth a DATA_NOTES.md
addendum naming FMP as a viable source of record fields with EDGAR as the required source
of the acceptance clock, not a standalone fix. The Steward does not decide whether to
pursue this; that is the registrar's and Haci's call per DEFERRED.md's bookkeeping
section.

## Rate-limit / plan-tier notes

- v3 API: dead for this key (403, legacy-endpoint message) -- confirms the account is
  provisioned as a post-2025-08-31 stable-tier subscriber, not a legacy plan.
- stable API: no rate-limit headers surfaced; no 429 in a 15-call/3.7s burst.
- `limit` parameter capped at 1000 rows per page server-side regardless of requested value.
- `from`/`to`/`date` parameters silently no-op on `insider-trading/search` -- worth
  flagging to Haci if procurement ever cites FMP's docs claiming range filtering; the
  docs page fetched did not document this parameter's non-effect, it was found
  empirically.
