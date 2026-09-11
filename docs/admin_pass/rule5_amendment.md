# Rule 5 amendment — measure the price path, the way Haci trades

**Why.** Current rule 5 makes fixed-horizon return (next open → T+h close) the objective and
calls target touches "descriptive, never the objective." That is not how the product is judged
or traded. SAS publishes six ladder targets, and Haci trades their touches: a partial
after-hours entry on elite nights, next-day option spreads legged out as targets are hit, no
stops, and deliberate interest in picks that swing through targets in both directions.

**What stays.** A hit rate on its own can mislead. A target 1.4% away is touched by most stocks
within 20 days whether or not the pick was good. So every hit-rate claim must beat a
distance-matched control, and targets the price had already passed at a realistic entry do not
count.

## Replacement text for CLAUDE.md rule 5

Paste over the current rule 5:

```
5. **Objective = the pick's price path after selection, measured the way it is traded.**
   - Path metrics are primary: for each ladder target L1–L6 (day T1/T2 within 20 trading
     days, swing T1/T2 within 40, long T1/T2 within 60 — volatilx
     services/sas_conviction_card.py:182-195), whether and when it was first touched; the
     counter-direction levels likewise (sas_selection_excursion.counter_touch_dates_json);
     and the order in which levels were hit.
   - Every PREREG states its entry basis: pick-night after-hours (from ~21:10 UTC), next-day
     open, or a next-day intraday trigger. A target already passed at that entry is not a hit.
   - Every hit-rate claim is compared against a distance-matched control: unpublished
     candidates from the same night, with targets placed at the same ATR distance. A hit
     rate without that control is descriptive.
   - Where a PREREG names an execution plan (the committed L1–L6 scale-out, or an option
     structure legged out at target touches), the plan's realized result is reported next
     to the hit rates.
   - Stops are not assumed. Adverse excursion and counter-direction touches are reported,
     not used as exits, unless the PREREG says otherwise.
   - Fixed-horizon close-to-close return is secondary and descriptive.
```

## Knock-on changes (after the rule is in)

- **Q001 PREREG §4** — replace the close-to-close metric with L1–L6 hit-before-window versus the
  distance-matched control. Still DRAFT, so it can change freely.
- **weekly-performance skill** — lead with L1–L6 hit rates by band (with the control), add
  counter-direction touch rates, and keep returns as a secondary table.
- **Explorer brief** — already written on this basis; see research/reports/explore/.
