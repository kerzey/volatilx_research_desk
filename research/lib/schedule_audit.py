"""Reproduce scheduling arithmetic from published counts, without loading outcomes.

Usage: python research/lib/schedule_audit.py
Writes only research/reports/SCHEDULE_AUDIT.md. Never edits a registered schedule.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_HASHES = {
    "research/reports/STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md":
        "005f6d5ddb173ac3e41b287139d5f51625f234afcf15875e1fd36a909c458ada",
    "research/reports/STEWARD_Q027_exposure.md":
        "b2605d52e34174d3d5192ed06d42b55ead4f8bc94203299bad5dd59e832857e9",
}
CASES = [
    {"id": "Q024", "collection": 142, "total": 46, "immature_tail": 20,
     "contributing": 26, "source": "research/reports/STEWARD_Q024_sas_vs_simple_benchmarks_exposure.md"},
    {"id": "Q027", "collection": 119, "total": 71, "immature_tail": 20,
     "contributing": 48, "source": "research/reports/STEWARD_Q027_exposure.md"},
    {"id": "Q029", "collection": 119, "total": 71, "immature_tail": 20,
     "contributing": 48, "source": "research/reports/STEWARD_Q027_exposure.md"},
]


def collection_sessions(contributing, observable_sessions, floor=80, haircut=0.0):
    if not 0 < contributing <= observable_sessions or floor <= 0 or not 0 <= haircut < 1:
        raise ValueError("Require positive cohort counts, floor, and a haircut in [0, 1)")
    return math.ceil(floor / (contributing / observable_sessions * (1 - haircut)))


def render(root=ROOT):
    for source, expected in SOURCE_HASHES.items():
        actual = hashlib.sha256((root / source).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Scheduling source changed: {source}; re-audit counts before updating its pin")
    lines = ["# Schedule audit — counts only", "",
             "Prepared from the 2026-09-14 repository evidence. INTERNAL / NON_QUOTABLE.", "",
             "The published forecasts mix outcome maturation with permanent eligibility loss, then add "
             "maturation again. For forecasting, estimate contribution on the calendar cohort old enough "
             "to be fully observed, retaining exclusions in that cohort's denominator. Add the endpoint's "
             "maturity lag once. Counts below come from existing reports; no parquet or outcome was opened.", "",
             "These are planning scenarios, not replacement dates, power calculations, confidence bounds, "
             "or authorization to run a locked study early. All registered floors, endpoints, dates, "
             "extensions and holdouts remain binding. Q029 inherits Q027's funnel; layer-specific gates "
             "must still be checked separately.", "",
             "| Q | Registered date | Current collection sessions | Mature calendar cohort | Contributing nights | Collection at observed mature-cohort rate | With illustrative 10% rate haircut |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for c in CASES:
        d = next((root / "research/questions").glob(c["id"] + "_*"))
        sch = json.loads((d / "schedule.json").read_text(encoding="utf-8"))
        observed = c["total"] - c["immature_tail"]
        base = collection_sessions(c["contributing"], observed)
        cautious = collection_sessions(c["contributing"], observed, haircut=0.1)
        lines.append(f"| {c['id']} | {sch['decision_date']} | {c['collection']} | {observed} | {c['contributing']} | {base} | {cautious} |")
    lines += ["", "Each scenario still adds 20 trading sessions for maturation and the registered freeze margin. "
              "The 10% haircut is a sensitivity assumption, not a measured uncertainty bound. "
              "The earlier review's 82/84-session illustrations used all-period eligibility proxies; "
              "this audit instead uses the fully observable calendar cohort (26 and 51 sessions). "
              "A small historical cohort cannot guarantee the future contribution rate.", "",
              "## Disposition", "",
              "- Q024/Q027/Q029: maturity accounting confirmed as a scheduling concern from the published counts. "
              "Keep their locks intact; any earlier deciding experiment requires a separately registered successor, "
              "with shared-data and family-testing dependencies declared. It cannot be an independent replication of the original.",
              "- Q031: published 47/71 and 48/71 forecasts share this concern, but calendar-block floors also bind. "
              "Recompute every block constraint before proposing a successor schedule.",
              "- Q033/Q034: their files discuss horizon-adjusted rates but cap planning using Q031's 0.6620. "
              "Review inherited caps and 40/60-session endpoints separately; do not apply the 20-session scenarios above.",
              "- Q030/Q032: re-entry uses currently unlocked drafts. Apply DP-53 before locking; cleared credential "
              "triggers do not by themselves establish all sample, partition or maturity gates.",
              "- All other questions: review the actual endpoint funnel before changing a projection. Rare regimes, "
              "rare selections, overlapping episodes and long horizons remain real reasons to wait.", "",
              "## Reproduction and provenance", "",
              "Run `python research/lib/schedule_audit.py`. Inputs are transcribed explicitly in CASES; "
              "a source hash change fails closed until the counts are reviewed and their pin is updated.", ""]
    for src in sorted({c["source"] for c in CASES}):
        digest = hashlib.sha256((root / src).read_bytes()).hexdigest()
        lines.append(f"- [{Path(src).name}](../../{src}) — SHA-256 `{digest}`")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    output = ROOT / "research/reports/SCHEDULE_AUDIT.md"
    output.write_text(render(), encoding="utf-8")
    print("wrote research/reports/SCHEDULE_AUDIT.md (registered schedules unchanged)")
