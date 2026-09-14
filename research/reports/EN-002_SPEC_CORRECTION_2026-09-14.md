# EN-002 verification specification correction

2026-09-14 — desk maintenance authorized by Haci's workflow-update request.

The original verification compared a tier-filtered output against the broader published-row
predicate. Existing `VERIFY_EN-002.md` identifies 579 published rows, one TJX row below the
specified tier floor, and 578 output picks over 71 nights. Section 3.1 already required the
score >=80 tier gate; the implementation followed it.

The brief now distinguishes published input, tier-eligible output and the named one-row
exclusion. No platform code, data, flag or scientific endpoint changed. The original FAIL report
remains untouched. A future verification writes a new dated receipt against the corrected
specification and the implemented SHA, including the existing inertness and control-stub checks.

Disposition: SPECIFICATION_CORRECTED / REVERIFICATION_PENDING. This document is not a new PASS
or evidence of deployment. The board should route re-verification to the steward rather than
ask Haci to implement an already reviewed code change again.
