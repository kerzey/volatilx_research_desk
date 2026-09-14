# Schedule audit — counts only

Prepared from the 2026-09-14 repository evidence. INTERNAL / NON_QUOTABLE.

The published forecasts mix outcome maturation with permanent eligibility loss, then add maturation again. For forecasting, estimate contribution on the calendar cohort old enough to be fully observed, retaining exclusions in that cohort's denominator. Add the endpoint's maturity lag once. Counts below come from existing reports; no parquet or outcome was opened.

These are planning scenarios, not replacement dates, power calculations, confidence bounds, or authorization to run a locked study early. All registered floors, endpoints, dates, extensions and holdouts remain binding. Q029 inherits Q027's funnel; layer-specific gates must still be checked separately.

| Q | Registered date | Current collection sessions | Mature calendar cohort | Contributing nights | Collection at observed mature-cohort rate | With illustrative 10% rate haircut |
|---|---|---:|---:|---:|---:|---:|
| Q024 | 2027-05-17 | 142 | 26 | 26 | 80 | 89 |
| Q027 | 2027-04-12 | 119 | 51 | 48 | 85 | 95 |
| Q029 | 2027-04-12 | 119 | 51 | 48 | 85 | 95 |

Each scenario still adds 20 trading sessions for maturation and the registered freeze margin. The 10% haircut is a sensitivity assumption, not a measured uncertainty bound. The earlier review's 82/84-session illustrations used all-period eligibility proxies; this audit instead uses the fully observable calendar cohort (26 and 51 sessions). A small historical cohort cannot guarantee the future contribution rate.

## Disposition

- Q024/Q027/Q029: maturity accounting confirmed as a scheduling concern from the published counts. Keep their locks intact; any earlier deciding experiment requires a separately registered successor, with shared-data and family-testing dependencies declared. It cannot be an independent replication of the original.
- Q031: published 47/71 and 48/71 forecasts share this concern, but calendar-block floors also bind. Recompute every block constraint before proposing a successor schedule.
- Q033/Q034: their files discuss horizon-adjusted rates but cap planning using Q031's 0.6620. Review inherited caps and 40/60-session endpoints separately; do not apply the 20-session scenarios above.
- Q030/Q032: re-entry uses currently unlocked drafts. Apply DP-53 before locking; cleared credential triggers do not by themselves establish all sample, partition or maturity gates.
- All other questions: review the actual endpoint funnel before changing a projection. Rare regimes, rare selections, overlapping episodes and long horizons remain real reasons to wait.

## Reproduction and provenance

Run `python research/lib/schedule_audit.py`. Inputs are transcribed explicitly in CASES; a source hash change fails closed until the counts are reviewed and their pin is updated.

- [STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md](../../research/reports/STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md) — SHA-256 `005f6d5ddb173ac3e41b287139d5f51625f234afcf15875e1fd36a909c458ada`
- [STEWARD_Q027_exposure.md](../../research/reports/STEWARD_Q027_exposure.md) — SHA-256 `b2605d52e34174d3d5192ed06d42b55ead4f8bc94203299bad5dd59e832857e9`
