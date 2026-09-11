"""EXPLORE_001 one-shot: append hypotheses H-053..H-064 to research/BACKLOG.md (idempotent guard).

Backlog lines carry n and direction only (Explorer charter): no in-sample returns or p-values.
"""
from pathlib import Path

p = Path(__file__).resolve().parents[3] / "BACKLOG.md"
s = p.read_text(encoding="utf-8")
if "H-053" in s or "## F7" in s:
    raise SystemExit("already appended")

f1 = ("- [ ] H-062 (F1) — Bear-direction picks touch their ladder levels less often than same-night candidates' "
      "downside at the same ATR distance (skip bear picks, or only in weak tapes) — baseline: same-night unpublished "
      "candidates, synthetic downside target at the same ATR distance, matched on beta60 / ATR% / 20-session run-up — "
      "in-sample n: 25 bear picks / 14 nights (144 level rows); direction: bear picks below control — why it might be "
      "real: bear setups fight the prevailing tape and the bear projection library is new (projection_bear_v2) — why it "
      "might be noise: tiny n, entirely an up-tape; the sealed Jun–Aug tape is the fair test of tape dependence. "
      "Source: EXPLORE_001 §A.")
f3 = ("- [ ] H-061 (F3) — GEX pin risk at selection (gex_context.pin_risk = true) goes with two-sided paths: pinned "
      "picks touch both +2 ATR and −2 ATR within 60 sessions more often — baseline: pin_risk = false picks; all "
      "candidates with pin_risk = false — in-sample n: 26 picks / 16 nights with pin risk (all candidates: 248 / 37 "
      "nights); direction: more two-sided among pinned picks, small difference across all candidates — why it might be "
      "real: dealer hedging near large gamma strikes pulls price back toward the strike from both sides — why it might "
      "be noise: GEX context missing for about half of picks; pin effects are short-horizon while the window is 60 "
      "sessions; tiny n. Source: EXPLORE_001 §C/§D.")
f4 = [
    ("- [ ] H-063 (F4) — Gap against → skip or delay the spread: when the next open is ≥ 0.25 ATR against the pick, "
     "L3 is touched less often from the open and the adverse −1 ATR move comes first more often than for flat opens "
     "(extends H-030 from return to the path objective and a skip decision) — baseline: flat-open picks (|gap| < 0.25 "
     "ATR) — in-sample n: 39 picks / 19 nights (flat: 152 / 34); direction: gap-against worse — why it might be real: "
     "overnight news or a failed breakout against the thesis — why it might be noise: small cell; the gap threshold is "
     "arbitrary; big favourable gaps (15 picks) also looked worse, so it may be a |gap| effect. Source: EXPLORE_001 §B/§E."),
    ("- [ ] H-064 (F4) — Earnings within 0–3 sessions after the pick: deeper drawdown from the open and a lower L3 "
     "touch rate than picks whose report is 4–20 sessions out → skip rule, and no spreads held across the print — "
     "baseline: picks with the next report 4–20 sessions out — in-sample n: 30 picks / 18 nights; direction: worse "
     "path — why it might be real: binary event risk plus IV crush; in-sample the catalyst layer scored a bogus "
     "market-wide earnings date (catalyst_event_score flat for every pick; volatilx "
     "scripts/rescore_sas_earnings_corrected.py:1-24, fixed 69ef05f 2026-06-01), so such picks were never penalised — "
     "why it might be noise: report dates come from the later *_corrected backfill (knowledge-time caveat: scheduled "
     "dates were probably public, but verify); after the fix the sealed period may hold too few such picks for the "
     "20-night cell floor. Related to H-041 but a different decision. Source: EXPLORE_001 §G."),
]
f7 = [
    "",
    "## F7 — Path, entry timing & volatility (Haci's trading style)",
    ("Source for all entries: research/reports/explore/EXPLORE_001.md (in-sample only; strong Apr–May tape; retro "
     "nights 2026-05-11..14 excluded). Path metrics per the rule-5 amendment. \"Matched control\" = the 10 nearest "
     "same-night unpublished candidates on beta60 / ATR% / 20-session run-up, synthetic target at the same ATR "
     "distance and direction."),
    ("- [ ] H-053 (F7) — Ladder touches are mostly distance: L1/L2 sit inside one normal day's range, so their touch "
     "rate should not beat a distance-matched control, and any SAS excess should sit in the deep levels (L4–L6) → "
     "ATR-scaled ladder; stop quoting L1/L2 hit rates without the control — baseline: matched control at the same ATR "
     "distance, same lane window — in-sample n: 280 picks / 35 nights (1,660 level rows); direction: small excess at "
     "L1–L3, larger at L4–L6 — why it might be real: ladder prices are LLM-written from projection levels with no ATR "
     "scaling (volatilx ai_agents/principal_agent.py:530-575; fallback 0.5%/1% steps at :897-911), and in ATR units "
     "high-ATR names get closer targets; near levels get hit by ordinary noise, deep levels need a trend — why it "
     "might be noise: one strong tape; high-beta picks in an up-tape reach far levels regardless; a 3-feature match "
     "may be incomplete; L5/L6 need 60-session windows (11 matured sealed nights today)."),
    ("- [ ] H-054 (F7) — Actionable-basis hit rates: many L1 (and some L2) touches happen before a next-day buyer "
     "can enter, so L1/L2 hit rates on a next-open or 10:00 ET entry basis are materially below the close-basis rate "
     "the platform publishes — baseline: close-basis rate on the same picks (entry_ref = spot_close, volatilx "
     "services/sas_excursion.py:336-354) — in-sample n: 280 picks / 35 nights; direction: large share of L1 already "
     "passed at the open, more by 10:00 ET, more for elite — why it might be real: L1 is closer than the usual "
     "overnight gap plus first-hour range — why it might be noise: mechanical, but the size depends on the tape's gap "
     "behaviour; elite n is tiny."),
    ("- [ ] H-055 (F7) — Leg out at the touch: for a vertical opened at the next open with the short strike at L3, "
     "closing at the first touch of L3 beats holding to the session-20 (≈ expiry) close; a sizeable share of picks "
     "that touch L3 close back below it by session 20 — baseline: hold-to-session-20 settlement of the same spread "
     "(stock-path proxy until option prices exist; then real option P&L) — in-sample n: 280 picks / 35 nights; "
     "direction: touch rate well above session-20 settle rate — why it might be real: targets sit at "
     "extension/resistance levels where supply appears; post-touch mean reversion (sas_excursion ran_then_dipped "
     "pattern) — why it might be noise: the stock proxy ignores IV, theta and strike width; in a strong tape many "
     "touches keep running; overlapping windows across nights."),
    ("- [ ] H-056 (F7) — Speed: SAS picks reach swing targets (L3/L4) in fewer sessions than matched controls at the "
     "same ATR distance, even where 40-session touch rates are similar → option DTE chosen from the target's ATR "
     "distance instead of a flat 21–35 DTE — baseline: days to first touch for the matched control — in-sample n: 280 "
     "picks / 35 nights; direction: picks faster at L3/L4, no difference at L2 — why it might be real: flow-led, "
     "breakout-style selection front-loads the move — why it might be noise: speed conditional on touching is "
     "survivor-biased (pre-register an unconditional version, e.g., touch within 5/10 sessions); strong tape."),
    ("- [ ] H-057 (F7) — After-hours entry at publication vs next-day open: an AH fill (keyed to "
     "sas_runs.finished_at, not a fixed 21:00 UTC) captures L1/L2 moves that happen overnight, and its adverse-first "
     "rate (−1 ATR before L3) is no worse than an open entry; the AH advantage is concentrated in elite picks — "
     "baseline: next-open entry on the same picks; for the elite leg, non-elite picks — in-sample n: 211 picks / 31 "
     "nights with an actionable AH price (elite 12 / 11 nights); direction: AH ≥ open on the L3 race; elite day-1 "
     "close above the AH price more often than non-elite — why it might be real: overnight drift after flow-driven "
     "selection; elite picks gap in their favour — why it might be noise: AH liquidity is thin and publication time "
     "varied (20:4x–23:1x UTC in-sample); the elite leg cannot reach the 20-night cell floor for months."),
    ("- [ ] H-058 (F7) — Don't buy the day-1 dip: resting limit orders 0.25–0.5 ATR against the pick-night close "
     "often fill on day 1, and the filled picks do worse on the L3-before-(−1 ATR) race than a "
     "market entry at the open — adverse selection — baseline: next-open market entry on the same picks — in-sample "
     "n: 280 picks / 35 nights (≈150 fills at 0.25 ATR, ≈100 at 0.5 ATR); direction: filled limits worse on the race "
     "— why it might be real: a day-1 dip is information against the thesis, and limits fill preferentially on "
     "losers — why it might be noise: the race ignores the better fill price on eventual winners; strong tape."),
    ("- [ ] H-059 (F7) — Haci's belief: high-beta / high-ATR picks are two-sided more often, touching both +2 ATR "
     "and −2 ATR within 60 sessions — baseline: low-beta tercile of picks, and beta-matched same-night unpublished "
     "candidates — in-sample n: 280 picks / 35 nights (all candidates 2,076 / 37 nights); direction in-sample: NOT "
     "supported in ATR units — high-beta picks realised wider range but it was one-directional; low-ATR picks were "
     "the most two-sided — why it might be real: high beta amplifies market swings in both directions, which a "
     "choppy tape would reveal — why it might be noise: April–May was a one-way tape, and the weaker Jun–Aug tape may "
     "flip the sign; register precisely because the tape changed."),
    ("- [ ] H-060 (F7) — Up-then-down in the 85–90 band: 85–90 picks touch L3 and then revisit the swing counter "
     "level more often than <80 picks, so holding through hurts this band and exiting at the touch helps — baseline: "
     "<80 band and 90+ band — in-sample n: 44 picks / 28 nights (85–90) vs 100 / 24 (<80), 15 / 13 (90+); "
     "direction: more up-then-down in 85–90 — why it might be real: may be the path face of the known 88–90 "
     "underperformance; higher-scored non-elite picks are more extended at selection — why it might be noise: small "
     "cell, arbitrary band edges, the 90+ comparison n is tiny; mechanism: weak."),
]

lines = s.rstrip("\n").split("\n")


def insert_after_family(lines, header_prefix, new_lines):
    i = next(k for k, l in enumerate(lines) if l.startswith(header_prefix))
    j = i + 1
    while j < len(lines) and not lines[j].startswith("## "):
        j += 1
    k = j
    while k > i + 1 and lines[k - 1].strip() == "":
        k -= 1
    return lines[:k] + new_lines + lines[k:]


lines = insert_after_family(lines, "## F1", [f1])
lines = insert_after_family(lines, "## F3", [f3])
lines = insert_after_family(lines, "## F4", f4)
lines = lines + f7
p.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("appended H-053..H-064")
