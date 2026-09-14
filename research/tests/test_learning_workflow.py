"""Boundary tests: learning metadata must not release a locked study early."""
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/lib"))
import desk_queue
import learning
import schedule_audit

spec = importlib.util.spec_from_file_location("desk_controller", ROOT / "research/lib/controller.py")
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.q = {"id": "Q999", "dir": "Q999_fixture", "state": "DATASET_PINNED",
                  "schedule": {"decision_date": "2027-04-12", "rule": "exposure-driven",
                               "extension_date": "2027-05-24", "extended": False}}
        self.today = date(2026, 9, 14)
        self.path = self.root / "research/questions/Q999_fixture/readiness.json"
        self.path.parent.mkdir(parents=True)
        src = self.root / "research/data/manifest_test.json"
        src.parent.mkdir(parents=True)
        src.write_text("{}", encoding="utf-8")
        self.counts = {"as_of": "2026-09-14", "sources": ["research/data/manifest_test.json"],
                       "count_definition": "Fixture endpoint eligibility and contribution",
                       "endpoints": [{"endpoint": "E1", "eligible_nights": 90,
                                      "contributing_nights": 80, "required_nights": 80,
                                      "post_lock_contributing_nights": 30,
                                      "required_post_lock_nights": 30}]}

    def check(self, write=True):
        if write:
            self.path.write_text(json.dumps(self.counts), encoding="utf-8")
        return learning.readiness(self.q, self.today, root=self.root)[0]

    def test_absent_counts_are_unmeasured(self):
        self.assertEqual(self.check(False), "READINESS_UNMEASURED")

    def test_met_counts_never_authorize_early_run(self):
        before = copy.deepcopy(self.q)
        self.assertEqual(self.check(), "COUNTS_READY_DATE_PENDING")
        self.assertEqual(self.q, before)

    def test_eligibility_and_maturation_are_distinguished(self):
        e = self.counts["endpoints"][0]
        e.update(eligible_nights=70, contributing_nights=50)
        self.assertEqual(self.check(), "WAITING_FOR_SAMPLE")
        e["eligible_nights"] = 90
        self.assertEqual(self.check(), "WAITING_FOR_MATURATION_OR_COVERAGE")

    def test_post_lock_floor_is_separate(self):
        self.counts["endpoints"][0]["post_lock_contributing_nights"] = 29
        self.assertEqual(self.check(), "WAITING_FOR_POST_LOCK_SAMPLE")

    def test_every_endpoint_must_clear(self):
        e2 = {**self.counts["endpoints"][0], "endpoint": "E2", "contributing_nights": 79}
        self.counts["endpoints"].append(e2)
        self.assertEqual(self.check(), "WAITING_FOR_MATURATION_OR_COVERAGE")

    def test_stale_and_future_counts(self):
        self.counts["as_of"] = "2026-09-06"
        self.assertEqual(self.check(), "READINESS_STALE")
        self.counts["as_of"] = "2026-09-15"
        with self.assertRaises(ValueError):
            self.check()

    def test_outcomes_and_inconsistent_counts_rejected(self):
        self.counts["endpoints"][0]["hit_rate"] = 0.8
        with self.assertRaises(ValueError):
            self.check()
        del self.counts["endpoints"][0]["hit_rate"]
        self.counts["endpoints"][0]["contributing_nights"] = 91
        with self.assertRaises(ValueError):
            self.check()

    def test_due_date_means_gate_check_not_confirmation(self):
        self.today = date(2027, 4, 12)
        self.assertEqual(self.check(False), "DUE_FOR_GATE_CHECK")
        self.q["schedule"]["extended"] = True
        self.assertEqual(self.check(False), "READINESS_UNMEASURED")

    def test_lifted_deferral_remains_registration_work(self):
        self.q["state"] = "DEFERRED"
        reason, _ = learning.readiness(self.q, self.today, resumable=True, root=self.root)
        self.assertEqual(reason, "READY_TO_RESUME")
        self.assertEqual(self.q["state"], "DEFERRED")


class ParserTests(unittest.TestCase):
    def test_placeholders_removed_real_tokens_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            qdir = Path(tmp)
            (qdir / "PREREG.md").write_text(
                "**Manifest:** research/data/manifest_missing.json\n"
                "**Manifest (prices):** **none — not used.**\n"
                "**Manifest (other):** `N/A`\n"
                "**Manifest (typo):** **research/data/typo.json**\n", encoding="utf-8")
            self.assertEqual(controller.prereg_manifests(qdir),
                             ["research/data/manifest_missing.json", "**research/data/typo.json**"])
            self.assertIn("not found", controller.pre_DATASET_PINNED(qdir, {}, None))

    def test_placeholder_only_cannot_pin_empty_dataset(self):
        with tempfile.TemporaryDirectory() as tmp:
            qdir = Path(tmp)
            (qdir / "PREREG.md").write_text("**Manifest:** **none**\n", encoding="utf-8")
            self.assertEqual(controller.pre_DATASET_PINNED(qdir, {}, None), "no manifest line in PREREG")


class QueueAndAuditTests(unittest.TestCase):
    def test_collection_forecast_uses_observable_cohort(self):
        self.assertEqual(schedule_audit.collection_sessions(26, 26), 80)
        self.assertEqual(schedule_audit.collection_sessions(48, 51), 85)
        self.assertEqual(schedule_audit.collection_sessions(26, 26, haircut=0.1), 89)
        self.assertEqual(schedule_audit.collection_sessions(48, 51, haircut=0.1), 95)
        with self.assertRaises(ValueError):
            schedule_audit.collection_sessions(27, 26)

    def test_audit_refuses_changed_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for src in schedule_audit.SOURCE_HASHES:
                p = root / src
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("changed counts", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source changed"):
                schedule_audit.render(root)

    def test_current_queue_dates_cards_and_no_writes(self):
        files = list((ROOT / "research/questions").glob("Q*/*json"))
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        queue = desk_queue.build_queue(today=date(2026, 9, 14))
        for qid in ("Q031", "Q033", "Q034"):
            row = next(q for q in queue["in_flight"] if q["id"] == qid)
            self.assertNotIn("?", row["due_on"])
            self.assertTrue(row["due_on"].startswith(row["schedule"]["decision_date"]))
        self.assertTrue(all(c["quotability"] == "NON_QUOTABLE" for c in queue["learning"]["cards"]))
        self.assertFalse(any(q["id"] == "Q024" for q in queue["due"]))
        self.assertFalse(any(q["id"] == "EN-002" for q in queue["for_haci"]))
        self.assertTrue(any(t["id"] == "READINESS-Q024" for t in queue["learning"]["work"]))
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in files})

    def test_cards_become_due_weekly(self):
        qs = desk_queue.question_rows()
        today = learning.snapshot(qs, date(2026, 9, 14))
        next_week = learning.snapshot(qs, date(2026, 9, 21))
        self.assertFalse(any(t["id"].startswith("LEARN-Q") for t in today["work"]))
        self.assertEqual(sum(t["id"].startswith("LEARN-Q") for t in next_week["work"]), 7)


if __name__ == "__main__":
    unittest.main()
