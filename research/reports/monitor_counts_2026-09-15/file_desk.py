"""One-off bookkeeping, 2026-09-15: H-097/H-098 to BACKLOG (F6), inbox tick, PI-014 addendum, DATA_NOTES FMP
section, DEFERRED H-022 note about FMP."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def insert_before(text, marker, block):
    i = text.index(marker)
    return text[:i].rstrip("\n") + "\n" + block + "\n" + text[i:]


# --- BACKLOG ---------------------------------------------------------------------------------------
p = ROOT / "research/BACKLOG.md"
t = p.read_text(encoding="utf-8")
h097 = """- [ ] H-097 (F6) — **Does the Conviction Monitor's tier order the forward path at all?** Three groups of published picks by their monitor history over sessions 1–5: (i) never worse than WATCH, (ii) EXIT that later softened to WATCH/HOLD within the five days, (iii) EXIT that persisted to day 5 — endpoint: from the open of session 6 to the close of session 15, the adverse-first rate (−1 ATR before +1 ATR) and the ATR move, each against a control matched on the damage already done by session 5 (DP-12, the Q019 construction); a confirmed result is a **monotone** ordering (iii) worse than (ii) worse than (i) in both primaries — baseline: same-night unpublished candidates at the same damage, and within-group adjacent comparisons — n: TBD (counts: 588 picks tracked 2026-06-01..09-14, 67% ever EXIT, 45% EXIT-then-softened, 5-day tracking only, `research/reports/monitor_counts_2026-09-15/REPORT.md`) — why real: the tiers are built from structure breaks on 30m/1h/4h/1d charts against the pick-night snapshot, a standard discretionary exit read; if they order paths after matching on damage, the display earns its place and its reversal behaviour tells a holder when a break was noise — why noise: since 2026-06-01 the polarity arm is dark and HOLD is unreachable (PI-014), so the tiers are a one-armed intraday support-break detector; EXIT-then-softened is partly the day-3 decay step rather than a repair; and the flow inputs behind the dead arm are themselves truncated (PI-020). **Distinct from Q019** (EXIT-then-sell vs hold to session 10, the money question, decision 2027-05-24): this asks whether the displayed tiers are *calibrated*, which Q019 does not test and which decides whether the surface stays or goes even if Q019 is positive. Register with the DP-58 interim look at 60 nights. Source: INBOX 2026-09-15 (Haci: "is the monitor working; if useless remove it").
"""
h098 = """- [ ] H-098 (F6, **Explorer first — not a PREREG**) — **Which monitor inputs carry information beyond the tier?** The 139 reason codes and the five per-timeframe tiers in `conviction_monitor_daily` (`reason_codes_json`, `technical_flip_*_tier`, `technical_signal_count_json`), on session-1 and session-2 rows, against the forward path from session 3 — each code demeaned within pick night and conditioned on the overall tier and on damage to date. The census shows the tier is carried by 1h/4h/1d support breaks while `obv_flipped_bearish_*`, `elliott_pattern_degraded_*` and `confidence_dropped_1step_*` sit on a quarter of rows regardless of tier; the question is whether any of the non-driving codes (OBV, Kalman regime, MACD, Elliott) predicts the path the tier misses, and whether any driving code is pure damage. Forking-paths surface (139 × 5), so the Explorer mines the in-sample split only and the survivors are pre-registered as separate F6 questions with BH correction. Why real: the raw inputs may hold signal the concurrence rollup throws away, as PI-018 showed for the report engine. Why noise: most single-code effects on a 10-session path are near zero and anything found in-sample must survive a prospective window. Source: INBOX 2026-09-15.
"""
t = insert_before(t, "## F7 — ", h097 + h098)
p.write_text(t, encoding="utf-8")

# --- INBOX -----------------------------------------------------------------------------------------
ib = ROOT / "research/INBOX.md"
it = ib.read_text(encoding="utf-8").rstrip("\n") + "\n"
it += ("- [x] Is the Conviction Monitor working? I ignore it in my trading. Is the overall evaluation correct, which data has "
       "significant impact, and if it is useless we can remove it from the platform (Haci, 2026-09-15) → census "
       "research/reports/monitor_counts_2026-09-15/REPORT.md; Q019 already registered (EXIT vs hold, 2027-05-24); "
       "H-097 (F6, calibration + reversal, register with DP-58 look), H-098 (F6, Explorer first); PI-014 addendum (HOLD unreachable)\n")
it += ("- [x] FMP API key granted to the desk (Haci, 2026-09-15) → `FMP_API_KEY` loads via desk_env; CLAUDE.md rule 1 line for Haci to add (guarded file); scope and knowledge-time "
       "rules in research/data/DATA_NOTES.md 'External source: FMP'; steward check on H-022's insider-history blocker noted in DEFERRED.md\n")
ib.write_text(it, encoding="utf-8")

# --- PLATFORM_ISSUES: PI-014 addendum ----------------------------------------------------------------
pi = ROOT / "research/PLATFORM_ISSUES.md"
pt = pi.read_text(encoding="utf-8")
addendum = """
**Addendum 2026-09-15 (census, `research/reports/monitor_counts_2026-09-15/REPORT.md`).** Two consequences
the original entry did not spell out:
- **HOLD is unreachable.** `overall_tier = _worst_tier([polarity_tier, technical_overall_tier])`
  (`services/conviction_monitor_service.py:792-805`); with `polarity_tier` fixed at WATCH the floor is WATCH,
  so the tier that means "conviction intact" cannot be printed. **0 HOLD `overall_tier` rows since 2026-06-01**
  (2,921 rows; the 1,221 HOLD values in `age_adjusted_severity` are decayed WATCHes). The subscriber sees a
  two-state monitor that rates 67% of picks EXIT within five sessions.
- **Possible input cause shared with PI-020.** `coverage_ratio = decomp_premium_total / contract_premium_total`
  is built from `uoa_contract_daily.buy_premium / sell_premium / premium_total`
  (`services/symbol_context_builder.py:136-175`). PI-020 stores zero-trade rows (`buy_premium` 0) for every
  contract the truncated trades page did not reach, which empties the decomposition on the most liquid names.
  PI-020 predates June, so it is not the whole cause; the fix brief for PI-014 should check the two together.
"""
pt = insert_before(pt, "### PI-015", addendum)
pi.write_text(pt, encoding="utf-8")

# --- DATA_NOTES: FMP -----------------------------------------------------------------------------------
dn = ROOT / "research/data/DATA_NOTES.md"
dt = dn.read_text(encoding="utf-8").rstrip("\n") + "\n"
dt += """
## External source: Financial Modeling Prep (Haci, 2026-09-15)

Haci granted the desk his FMP subscription key on 2026-09-15 (`FMP_API_KEY` in `.env.research`, loaded only
through `research/lib/desk_env.py`, never printed). **Rule 1 names the desk's credentials and CLAUDE.md is a
guarded file the desk cannot edit; until Haci adds `FMP_API_KEY` to rule 1's list, agents treat it as
granted-but-unlisted and use it for Steward feasibility checks only, not for a freeze a PREREG cites.** Docs: https://site.financialmodelingprep.com/developer/docs.
It is **read-only reference and fundamental data**, and it is also what the platform's own enrichment path
already calls (`ai_agents/fmp_client.py`), so it changes nothing about rule 1's read-only stance.

What it is for, and the rules that travel with it:

- **Rule 4 still binds.** Any FMP field a PREREG cites is frozen first into `research/data/` with a manifest
  (`manifest_fmp_vNNN.json`: endpoint, parameters, fetch time, row hashes). No study number comes from a live
  call.
- **Rule 14 is the hard part.** FMP rows are *records*, not point-in-time observations: an estimate revision,
  a news item or an insider filing must carry a publish / acceptance timestamp that the freeze keeps, and a
  feature is usable only when that timestamp ≤ 16:05 ET on the pick night. Endpoints without a reliable
  publish time (most "profile" and "ratios" snapshots) are **descriptive only**. The Steward records the
  availability per endpoint in `freeze_config.availability` before any question uses it.
- **Candidate uses, in order:** (1) H-022's blocker — Form 4 insider-transaction *history* with acceptance
  timestamps (`insider-trading` search endpoints); the Steward checks coverage and as-of fields before the
  registrar may lift the deferral. (2) Analyst estimate and price-target revision history, for the smart-money
  and catalyst layers. (3) Stock news with publish times, for a news-catalyst arm. (4) Earnings-call transcript
  metadata for the earnings engine. Anything else is out of scope until a hypothesis names it.
- **Not for:** live checks during a study, price data (Alpaca remains the price source), or anything a
  subscriber-facing claim would cite before it is frozen and prospective.
"""
dn.write_text(dt, encoding="utf-8")

# --- DEFERRED: H-022 note ---------------------------------------------------------------------------------
df = ROOT / "research/questions/DEFERRED.md"
dtxt = df.read_text(encoding="utf-8")
marker = "## H-022 —"
i = dtxt.index(marker)
j = dtxt.find("\n## ", i + 10)
note = ("\n> **2026-09-15 — blocker may be lifting, not lifted.** Haci granted the desk his Financial Modeling Prep key "
        "(`FMP_API_KEY`; rule 1 listing pending Haci's edit; `research/data/DATA_NOTES.md` \"External source: FMP\"). FMP's insider-trading search "
        "endpoints are named above as a candidate source. Before any TRIGGER MET line: the Steward verifies, read-only, "
        "that the history endpoint returns Form 4 rows with an acceptance / filing timestamp for the study window and the "
        "candidate universe, freezes them with a manifest, and records the availability rule; only then does the registrar "
        "reassess. Not resumed by this note.\n")
dtxt = (dtxt[:j].rstrip("\n") + "\n" + note + dtxt[j:]) if j > 0 else dtxt.rstrip("\n") + "\n" + note
df.write_text(dtxt, encoding="utf-8")
print("ok")
