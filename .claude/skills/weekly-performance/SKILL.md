---
name: weekly-performance
description: Weekly descriptive performance snapshot of SAS and AI Picks on the W60 basis with n floors, stratified by score band, regime, lane and source. Descriptive only — no verdicts.
---
Produce the weekly performance snapshot on the latest frozen manifest (not live tables).
Basis: W60 for quotable cells; W20 as NON_QUOTABLE for recency.

Tables (each cell: n, mean direction-adjusted return, 95% bootstrap CI, touch-hit L1/L2 as
descriptive columns; cells with n<20 print SUPPRESSED):
- By score band: 70–80 / 80–90 / 90+ (never expose 88–90 as its own band).
- By regime (point-in-time label) × score band.
- By best_timeframe lane.
- By source membership (single-source vs multi-source).
- By confidence label.
- Rolling 4-week trend of the 90+ band.

Append a "changes since last week" block: cells that moved more than their CI width.
Write to research/reports/weekly/<date>.md. If any pattern looks interesting, write it to
research/BACKLOG.md as a hypothesis — do not call it a finding.
