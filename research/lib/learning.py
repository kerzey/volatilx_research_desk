"""Read the internal-learning agenda. Never reads raw data or changes study state."""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LABELS = {"MECHANICAL", "EXPLORATORY", "NOT_YET_ASSESSED"}
PRIORITY = ["Q026", "Q006", "Q024", "Q027", "Q029", "Q034", "Q028"]


def snapshot(questions, today=None, root=ROOT):
    today = today or date.today()
    path = root / "research/learning/agenda.json"
    if not path.exists():
        return {"cards": [], "work": []}
    agenda = json.loads(path.read_text(encoding="utf-8"))
    by_id = {q["id"]: q for q in questions}
    cards, work = [], []
    for entry in agenda["cards"]:
        qid = entry["question"]
        if qid not in by_id or entry["label"] not in LABELS:
            raise ValueError(f"Invalid evidence card: {qid}")
        as_of, review = date.fromisoformat(entry["as_of"]), date.fromisoformat(entry["review_on"])
        if as_of > today or review < as_of:
            raise ValueError(f"Invalid evidence dates: {qid}")
        for source in entry["sources"]:
            resolved = (root / source).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                raise ValueError(f"Missing or external evidence source: {source}")
        sch = by_id[qid]["schedule"]
        decision = sch.get("extension_date") if sch.get("extended") else sch.get("decision_date")
        cards.append({**entry, "state": by_id[qid]["state"], "decision_date": decision,
                      "review_due": review <= today, "quotability": "NON_QUOTABLE"})
        if review <= today:
            work.append({"id": f"LEARN-{qid}", "owner": "reporter",
                         "what": f"Refresh {qid} evidence card from allowed reports; {entry['next_action']}",
                         "source": "research/LEARNING_POLICY.md"})
    for task in agenda["tasks"]:
        if task["status"] != "OPEN" or date.fromisoformat(task["due_on"]) > today:
            continue
        # A successful controller pin resolves this maintenance task automatically.
        if task["id"] == "OPS-Q028" and by_id.get("Q028", {}).get("state") in {
            "DATASET_PINNED", "EVALUATED", "VALIDATED", "REDTEAM_SIGNED", "LEDGERED"
        }:
            continue
        work.append(task)
    order = {qid: i for i, qid in enumerate(PRIORITY)}
    cards.sort(key=lambda c: order.get(c["question"], len(order)))
    return {"cards": cards, "work": work}


def readiness(question, today, resumable=False, root=ROOT):
    """Classify the reason for waiting; dates never authorize an early outcome look."""
    state, sch = question["state"], question["schedule"]
    decision = sch.get("extension_date") if sch.get("extended") else sch.get("decision_date")
    if resumable:
        return "READY_TO_RESUME", "Measured deferral trigger cleared; finish registration"
    if state == "DEFERRED":
        return "DEFERRED", "See the question's measured re-entry trigger"
    if state in {"EVALUATED", "VALIDATED", "REDTEAM_SIGNED"}:
        return "READY_FOR_REVIEW", "Finish validation, independent review and reporting"
    if state in {"IDEA", "PREREG_DRAFT"}:
        return "REGISTRATION", "Resolve the draft under current decision policy"
    if state == "PREREG_LOCKED" and not sch.get("pin_at_decision"):
        return "NEEDS_PIN", "Verify the declared manifests and pin through the controller"
    if state not in {"PREREG_LOCKED", "DATASET_PINNED"}:
        return "RECORDED_STATE", state
    if sch.get("rule") == "immediate" or (decision and decision <= today.isoformat()):
        return "DUE_FOR_GATE_CHECK", "Check registered sample gates before opening outcomes"
    p = root / "research/questions" / question["dir"] / "readiness.json"
    if p.exists():
        counts = json.loads(p.read_text(encoding="utf-8"))
        allowed = {"as_of", "sources", "count_definition", "endpoints"}
        if set(counts) != allowed or not counts["sources"] or not counts["count_definition"]:
            raise ValueError(f"Readiness must contain only the documented counts schema: {question['id']}")
        for source in counts["sources"]:
            source_path = (root / source).resolve()
            if not source_path.is_relative_to(root.resolve()) or not source_path.is_file():
                raise ValueError(f"Missing or external readiness source: {source}")
        observed = date.fromisoformat(counts["as_of"])
        if observed > today:
            raise ValueError(f"Future readiness observation: {question['id']}")
        if (today - observed).days > 7:
            return "READINESS_STALE", f"Counts last checked {observed}; refresh counts only"
        endpoints = counts["endpoints"]
        if not endpoints:
            return "READINESS_UNMEASURED", "No endpoint counts supplied"
        for e in endpoints:
            required = ("eligible_nights", "contributing_nights", "required_nights",
                        "post_lock_contributing_nights", "required_post_lock_nights")
            if set(e) != set(required) | {"endpoint"} or not e["endpoint"]:
                raise ValueError(f"Readiness endpoint contains undocumented fields: {question['id']}")
            if any(not isinstance(e[k], int) or isinstance(e[k], bool) or e[k] < 0 for k in required):
                raise ValueError(f"Invalid readiness counts: {question['id']}")
            if e["contributing_nights"] > e["eligible_nights"] or e["post_lock_contributing_nights"] > e["contributing_nights"]:
                raise ValueError(f"Inconsistent readiness counts: {question['id']}")
        if len({e["endpoint"] for e in endpoints}) != len(endpoints):
            raise ValueError(f"Duplicate readiness endpoints: {question['id']}")
        if any(e["eligible_nights"] < e["required_nights"] for e in endpoints):
            return "WAITING_FOR_SAMPLE", f"Endpoint eligibility floor short as of {observed}"
        if any(e["contributing_nights"] < e["required_nights"] for e in endpoints):
            return "WAITING_FOR_MATURATION_OR_COVERAGE", f"Eligible nights exist; maturity/gradeability short as of {observed}"
        if any(e["post_lock_contributing_nights"] < e["required_post_lock_nights"] for e in endpoints):
            return "WAITING_FOR_POST_LOCK_SAMPLE", f"Post-lock contributing-night floor short as of {observed}"
        return "COUNTS_READY_DATE_PENDING", "Counts met; keep the registered date and all other gates"
    if question["id"] == "Q028":
        return "SCHEDULED_DIAGNOSTIC", "Outcome-free audit; run on its registered date"
    return "READINESS_UNMEASURED", "Registered date known; no fresh counts-only readiness snapshot"
