"""Register status cells must parse even when they carry an annotation.

The bug (found 2026-09-15): STATUS_RE / FLOW_RE were anchored `^...$` over `\\S` classes, so a
cell containing a space matched nothing. Every cell a verify writes contains a space, so
list_rows returned status="" / flow="", and build_queue's branch chain skipped the row entirely:
PI-001's FAILED state was invisible to the queue, and PI-017 was never queued for the Steward.

The three row strings below are the real cells from research/PLATFORM_ISSUES.md at the time.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/lib"))
import desk_queue  # noqa: E402

PI_001 = ("FAILED:merged to main but no date recovered (still ~5%, 21-25/498 through 2026-09-02) "
          "- deployed nightly likely not running d19c9a9")
PI_017 = ("IMPLEMENTED:bccfa67 (code verified 2026-09-14; deploy unconfirmed -- V3 re-check after "
          "the next nightly that runs bccfa67; see reports/VERIFY_PI-017.md)")
PI_020 = ("VERIFIED:3f1d3e6 (PR #32 merged e513d44, 2026-09-15; **D0 = 2026-09-15**; repo PASS, "
          "W5 history unchanged to the row) - BRIEF_WRITTEN")


def parse(cell, rx=None):
    """What list_rows would read out of a four-column row whose status cell is `cell`."""
    return desk_queue._status_cell(rx or desk_queue.STATUS_RE, ["PI-999", "high", cell, "prose"])


class StatusCellTests(unittest.TestCase):
    def test_annotated_cells_normalise_to_the_leading_token(self):
        for cell, expected in ((PI_001, "FAILED:merged"),
                               (PI_017, "IMPLEMENTED:bccfa67"),
                               (PI_020, "VERIFIED:3f1d3e6"),
                               ("HACI_DECIDED:fix", "HACI_DECIDED:fix"),
                               ("OPEN", "OPEN")):
            with self.subTest(cell=cell[:40]):
                token, raw = parse(cell)
                self.assertEqual(token, expected)
                self.assertEqual(raw, cell, "the raw cell must come back untouched")

    def test_the_sha_extracted_downstream_is_the_sha_alone(self):
        # build_queue does st.split(":", 1)[1] to name the SHA for the Steward.
        self.assertEqual(parse(PI_017)[0].split(":", 1)[1], "bccfa67")

    def test_the_branch_chain_routes_each_row(self):
        self.assertTrue(parse(PI_017)[0].startswith("IMPLEMENTED:"))   # -> desk_todo
        self.assertTrue(parse(PI_001)[0].startswith("FAILED"))         # -> for_haci
        self.assertTrue(parse("HACI_DECIDED:fix")[0].startswith("HACI_DECIDED:fix"))
        # VERIFIED is terminal: it must parse, and must match no branch.
        verified = parse(PI_020)[0]
        self.assertEqual(verified, "VERIFIED:3f1d3e6")
        for prefix in ("HACI_DECIDED:fix", "HACI_DECIDED:build", "IMPLEMENTED:", "FAILED"):
            self.assertFalse(verified.startswith(prefix))
        self.assertNotEqual(verified, "BRIEF_WRITTEN")

    def test_flow_re_sees_the_same_cells(self):
        for cell, expected in ((PI_017, "IMPLEMENTED:bccfa67"), (PI_020, "VERIFIED:3f1d3e6"),
                               ("BRIEF_WRITTEN", "BRIEF_WRITTEN")):
            self.assertEqual(parse(cell, desk_queue.FLOW_RE)[0], expected)
        # evidence-only tokens are not flow states
        self.assertEqual(parse("UNDER_TEST:Q004", desk_queue.FLOW_RE)[0], "")

    def test_prose_is_never_read_as_a_status(self):
        # the last cell is free text and is not scanned, even when it opens with a keyword
        self.assertEqual(
            desk_queue._status_cell(desk_queue.STATUS_RE,
                                    ["PI-999", "high", "OPEN", "OPEN question: is the ladder null?"]),
            ("OPEN", "OPEN"))
        # and a cell that merely mentions a token mid-sentence matches nothing
        self.assertEqual(parse("see PI-020, now VERIFIED")[0], "")

    def test_compound_tokens_survive(self):
        self.assertEqual(parse("HISTORICALLY_CONFIRMED")[0], "HISTORICALLY_CONFIRMED")
        self.assertEqual(parse("UNDER_TEST:Q004")[0], "UNDER_TEST:Q004")

    def test_the_live_registers_leave_no_row_unparsed(self):
        # the regression itself: every row of every register must yield a status
        for name in ("PLATFORM_ISSUES.md", "ENHANCEMENTS.md", "TRADE_IDEAS.md"):
            for row in desk_queue.list_rows(name):
                with self.subTest(register=name, row=row["id"]):
                    self.assertTrue(row["status"], f"{row['id']} parsed to an empty status")


if __name__ == "__main__":
    unittest.main()
