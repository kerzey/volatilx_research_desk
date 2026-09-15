"""One-off bookkeeping for the SNDK case (2026-09-15): add H-095, H-096, flag H-092 with PI-020, tick the inbox."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
p = ROOT / "research/BACKLOG.md"
t = p.read_text(encoding="utf-8")

h095 = """- [ ] H-095 (F1) — **Re-selection while the platform's own monitor says EXIT.** Published picks of a symbol whose earlier pick (within the last 10 sessions) is rated `overall_tier = EXIT` in `conviction_monitor_daily` on the new pick night, vs published picks of symbols with a recent earlier pick not rated EXIT — endpoint: distance-matched excess L1 (20 sessions) and L3 (40 sessions) first-touch rate from the stated entry, each arm against its own same-night unpublished control — baseline: re-selections without an EXIT on the prior pick — n: TBD (steward: re-selection nights with a monitor row; probably thin) — why real: SNDK 2026-09-10 and 09-11 were published at rank 1 on the nights the monitor rated the 09-08 and 09-10 picks EXIT (key support breached on 30m/1h, 4h Kalman regime opposing); selection does not read the monitor, so a real warning would be free to use — why noise: the monitor's polarity arm has been silent since 2026-06-01 (PI-014), so EXIT is the technical arm alone, and EXIT on a prior pick is correlated with a pullback that can make the new entry better, not worse. **Overlaps** Q019 (does monitor EXIT predict the *flagged* pick's path) and Q003 (repeat selection) in inputs only; registrar checks DP-29. Source: INBOX 2026-09-15 (SNDK case, `research/reports/case_SNDK_2026-09-15/REPORT.md` §6).
"""

h096 = """- [ ] H-096 (F2) — **Scores that swing on whether the bearish projection engine lists the symbol.** Candidates whose `conflict_penalty` switches on and off across consecutive nights because `projection_bearish_v2` lists them one night and not the next (SNDK: 93.3 on 09-08, 76.1 on 09-09 with a 13-point conflict penalty, 92.7 on 09-10 with none), vs published picks with no such flip in the prior 3 sessions — endpoint: distance-matched excess L1 / L3 first-touch rate — baseline: same-band picks without a flip, same nights — n: TBD — why real: a symbol both projection engines surface within days is by construction contested, and the score treats the bearish listing as noise the moment it disappears — why noise: bearish-engine listings may be driven by the same volatility that makes targets easy to touch, and flips may be too rare to reach a floor. Diagnostic companion, no outcome needed: how often a published pick had a bearish listing in the prior 3 sessions. Source: INBOX 2026-09-15 (SNDK case, §6).
"""

old92 = "- [ ] H-092 (F5) — **Flow label vs the premium actually traded.**"
new92 = ("- [ ] H-092 (F5) — **Flow label vs the premium actually traded.** **⚠ PI-020 (2026-09-15): the stored premium mix is "
         "truncated toward calls on the most liquid names, so the arms are mis-assigned exactly where they matter; do not register "
         "until PI-020 is fixed and a clean window exists, or register it explicitly on complete trades from a new source.**")
assert old92 in t
t = t.replace(old92, new92, 1)


def insert_before(text, marker, block):
    i = text.index(marker)
    return text[:i].rstrip("\n") + "\n" + block + "\n" + text[i:]


t = insert_before(t, "## F2 — ", h095)
t = insert_before(t, "## F3 — ", h096)
p.write_text(t, encoding="utf-8")

ib = ROOT / "research/INBOX.md"
it = ib.read_text(encoding="utf-8").rstrip("\n") + "\n"
it += ("- [x] SNDK was picked 2–3 times last week at 92–93 with big bullish call flow expiring Friday and still fell; why, and will it do "
       "better this week (Haci, 2026-09-15) → answered in research/reports/case_SNDK_2026-09-15/REPORT.md; PI-020 filed (UOA trade "
       "truncation); H-095 (F1), H-096 (F2)\n")
ib.write_text(it, encoding="utf-8")
print("ok")
