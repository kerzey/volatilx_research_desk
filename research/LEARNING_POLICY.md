# Earlier internal answers, protected prospective tests

Effective 2026-09-14. Authorized by Haci: "Update the research desk per your recommendations."
DP-52..57 govern this procedure. The controller retains its existing verdict states and gates.

## Two outputs for each priority question

**Evidence now:** a source-linked card in `research/learning/agenda.json`, rendered on BOARD.md.
State what is established, its limitations, the internal decision it supports, and the next action.
Labels are MECHANICAL (coverage/arithmetic/lineage), EXPLORATORY (historical pattern), or
NOT_YET_ASSESSED. Every card is INTERNAL / NON_QUOTABLE. These are not controller verdicts.

**Registered verdict:** produced through the existing preregistration, manifests, sample gates,
inference, independent review and controller. Learning cards cannot authorize subscriber claims,
activate scoring changes or promote a trading rule into the confirmed playbook. An internal shadow
experiment may be proposed with scope, metrics, version and rollback stated.

## Cadence and priority

- Integrity defects and scoring/lineage diagnostics: triage within two working days. Existing
  outcome-free studies retain their registered dates; a maintenance fix is not an early run.
- Priority evidence cards: review weekly and after relevant new reports. Preserve the observation
  date; board regeneration does not advance `as_of`. If nothing changed, say so and set the next
  review date only after reviewing the sources.
- Historical companions: prepare protocols within a week; aim for a descriptive report within
  two weeks after admissible data and a fixed protocol are ready. Report inability to estimate
  rather than silently relaxing requirements to reach a deadline.
- Prospective evidence: retain the registered observations and maturity. Rare regimes and
  40/60-session endpoints keep their own clocks. Sample floors do not guarantee a decisive answer.
- During a cycle: due studies and urgent integrity blockers first; then one bounded learning task
  before discretionary registrations. Learning work must not starve a due study. Complete already
  approved desk-local work without repeated prompt requests. External deployment and communications
  retain their authorization requirements.

Priority: Q026, Q006, Q024, Q027, Q029, Q034; Q028 is a supporting cheap diagnostic. Other studies
continue accumulating observations. Priority never removes family-testing obligations or results.

## Historical companions

Use `research/learning/<id>/PROTOCOL.md`, `eval.py` and `REPORT.md`; never a locked question's
results directory. Before computing, specify the internal decision, exact input whitelist,
manifest hashes, admitted selection dates, prior exposure to that history, engine versions,
comparison, endpoint, uncertainty limits and output label. Record all variants examined.

Default admission is the existing **in-sample** split (`trading_date <= 2026-05-29` in v001),
loaded through the existing in-sample helper. Existing published reports may be summarized with
their original caveats. A report discussing sealed data does not authorize loading its raw rows.
Already-read sealed cohorts remain excluded from new companion computation unless a separately
documented admission establishes that no in-flight holdout is compromised. Frozen does not mean
untouched. Reanalyzing the same history adds no independent replication.

Do not load prospective selections or their outcomes. Forward bars for admitted historical picks
may extend beyond the selection cutoff only as the in-sample helper permits; later selections stay
excluded. Preserve feature knowledge time and engine-vintage splits. Learned weights, cutoffs or
ranking rules require a new version and future test, never a change to an in-flight study.

Reports lead with the permitted internal decision and limitations. Descriptive uncertainty must
name a fixed appropriate method and its dependence assumptions; no confirmatory p/q verdict or
independent-validation claim is permitted. Prefer NOT_ESTIMABLE for the current engine to a
misleading historical replay. Initial packages: `research/learning/HISTORICAL_COMPANIONS.md`.

## Counts-only readiness and scheduling

Separate elapsed calendar sessions, eligible nights, mature nights, contributing/gradeable nights,
and post-lock contributing nights **per primary endpoint**. Estimate future attrition on the
fully observable calendar cohort, keeping its exclusions in the denominator. Add the maturity
lag once. Do not penalize a forecast for its immature tail and then add that wait again.
Show planning scenarios and uncertainty separately; a later date is not inherently more valid.

The steward may write `questions/QNNN_slug/readiness.json` using
`research/templates/READINESS_TEMPLATE.json`. List every registered endpoint and its actual floor,
source manifests, observation date and count definition. No effect, hit rate, return, p-value,
statistic or outcome comparison belongs there. The board labels absent snapshots unmeasured and
snapshots older than seven calendar days stale. It never authorizes an early run from counts;
the registered evaluation independently checks all gates.

New/unlocked plans justify sample size against the MPE, precision/power assumptions, clustering,
multiplicity, strata and maturity. Sequential designs require specified stopping boundaries,
dependence assumptions and family correction before prospective outcomes are inspected.
Repeated ordinary confidence-interval checks are not a sequential design.

Locked studies keep their definitions, dates, hashes and exclusions. `schedule_audit.py` writes
planning scenarios only. An earlier deciding successor must be separately registered, declare
data overlap and multiplicity, and cannot claim to independently replicate its parent.

## Operational receipts

The agenda also holds bounded tasks, owners, due dates and sources. Mark DONE only with an artifact
or receipt. Keep maintenance, deployment, data readiness and statistical uncertainty distinct.
A cleared credential trigger means READY_TO_RESUME, not DATASET_PINNED. A code review passing does
not prove deployment or recovery. Correcting a verification specification preserves its failed report.

Rebuild with `python research/lib/board.py`; inspect work with
`python research/lib/desk_queue.py --json`. These commands read documents/counts only: they do not
run studies, fetch data, access credentials, send messages or change registered schedules.
