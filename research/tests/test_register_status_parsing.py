r"""Register tables must parse structurally, or fail loudly. Two defects are pinned here.

1. **Status cells that carry an annotation** (2026-09-15). STATUS_RE / FLOW_RE were anchored
   `^...$` over `\S` classes, so a cell containing a space matched nothing. Every cell a verify
   writes contains a space, so list_rows returned status="" / flow="" and build_queue's branch
   chain skipped the row: PI-001's FAILED state was invisible and PI-017 was never queued for the
   Steward. The three row strings below are the real cells from PLATFORM_ISSUES.md at the time.

2. **Positional column access** (2026-09-15). list_rows returned only a positional `cells` list,
   so every consumer had to know column order. Zipping a header against it truncates silently when
   the lengths differ — and one unescaped `|` in a cell makes them differ, shifting every later
   column with no error. Rows now carry a `columns` dict keyed by header name, and a cell-count
   mismatch raises RegisterError instead of parsing into a shifted row.
"""
import sys
import tempfile
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

HEADER = "| ID | Severity | Status | Issue |"
SEP = "|---|---|---|---|"


def write_register(*body, header=HEADER, name="PLATFORM_ISSUES.md"):
    """Parse a throwaway register through the real list_rows, with ROOT pointed at a temp dir."""
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    (root / "research").mkdir()
    (root / "research" / name).write_text(
        "# fixture\n\nsome prose\n\n" + "\n".join([header, SEP, *body]) + "\n\nmore prose\n",
        encoding="utf-8")
    original, desk_queue.ROOT = desk_queue.ROOT, root
    try:
        return desk_queue.list_rows(name)
    finally:
        desk_queue.ROOT = original
        tmp.cleanup()


class StatusTokenTests(unittest.TestCase):
    """Defect 1 — the leading token must survive an annotation after it."""

    def parse(self, status_cell):
        rows = write_register(f"| PI-999 | high | {status_cell} | prose |")
        self.assertEqual(len(rows), 1)
        return rows[0]

    def test_annotated_cells_normalise_to_the_leading_token(self):
        for cell, expected in ((PI_001, "FAILED:merged"),
                               (PI_017, "IMPLEMENTED:bccfa67"),
                               (PI_020, "VERIFIED:3f1d3e6"),
                               ("HACI_DECIDED:fix", "HACI_DECIDED:fix"),
                               ("OPEN", "OPEN")):
            with self.subTest(cell=cell[:40]):
                row = self.parse(cell)
                self.assertEqual(row["status"], expected)
                self.assertEqual(row["status_raw"], cell, "the raw cell must come back untouched")

    def test_the_sha_extracted_downstream_is_the_sha_alone(self):
        # build_queue does st.split(":", 1)[1] to name the SHA for the Steward.
        self.assertEqual(self.parse(PI_017)["status"].split(":", 1)[1], "bccfa67")

    def test_the_branch_chain_routes_each_row(self):
        self.assertTrue(self.parse(PI_017)["status"].startswith("IMPLEMENTED:"))   # -> desk_todo
        self.assertTrue(self.parse(PI_001)["status"].startswith("FAILED"))         # -> for_haci
        verified = self.parse(PI_020)["status"]                                    # terminal
        self.assertEqual(verified, "VERIFIED:3f1d3e6")
        for prefix in ("HACI_DECIDED:fix", "HACI_DECIDED:build", "IMPLEMENTED:", "FAILED"):
            self.assertFalse(verified.startswith(prefix))

    def test_prose_is_never_read_as_a_status(self):
        # the description column is not a status column, whatever it opens with
        row = self.parse("OPEN")
        self.assertEqual(row["status"], "OPEN")
        self.assertEqual(self.parse("see PI-020, now VERIFIED")["status"], "")

    def test_compound_tokens_survive(self):
        self.assertEqual(self.parse("HISTORICALLY_CONFIRMED")["status"], "HISTORICALLY_CONFIRMED")
        self.assertEqual(self.parse("UNDER_TEST:Q004")["status"], "UNDER_TEST:Q004")


class StructuralTests(unittest.TestCase):
    """Defect 2 — columns by name, and a malformed table raises instead of shifting."""

    def test_well_formed_row_gives_columns_by_name(self):
        rows = write_register(f"| PI-042 | high | {PI_017} | the issue text |")
        row = rows[0]
        self.assertEqual(row["columns"], {"ID": "PI-042", "Severity": "high",
                                          "Status": PI_017, "Issue": "the issue text"})
        self.assertEqual(row["cells"], ["PI-042", "high", PI_017, "the issue text"])
        self.assertEqual(row["roles"], desk_queue.REGISTER_ROLES["PLATFORM_ISSUES.md"])
        self.assertEqual(row["text"], "the issue text")
        self.assertEqual(row["status"], "IMPLEMENTED:bccfa67")

    def test_one_extra_cell_raises_and_names_both_counts(self):
        with self.assertRaises(desk_queue.RegisterError) as e:
            write_register("| PI-042 | high | OPEN | the issue | an extra cell |")
        msg = str(e.exception)
        self.assertIn("PI-042", msg)
        self.assertIn("5 cells", msg)
        self.assertIn("header has 4", msg)

    def test_missing_trailing_cell_raises(self):
        with self.assertRaises(desk_queue.RegisterError) as e:
            write_register("| PI-042 | high | OPEN |")
        msg = str(e.exception)
        self.assertIn("PI-042", msg)
        self.assertIn("3 cells", msg)
        self.assertIn("header has 4", msg)

    def test_renamed_header_column_raises_rather_than_shifting(self):
        with self.assertRaises(desk_queue.RegisterError) as e:
            write_register("| PI-042 | high | OPEN | the issue |",
                           header="| ID | Severity | State | Issue |")
        self.assertIn("'Status'", str(e.exception))

    def test_an_escaped_pipe_is_one_cell_and_comes_back_literal(self):
        rows = write_register(r"| PI-042 | high | OPEN | a \| b, still one cell |")
        self.assertEqual(rows[0]["columns"]["Issue"], "a | b, still one cell")
        self.assertEqual(len(rows[0]["cells"]), 4)

    def test_an_unescaped_pipe_is_caught_by_the_cell_count_check(self):
        # this is the silent-shift bug: without the check, "Issue" would read "a " and the
        # row would lose " b" off the end with no error at all
        with self.assertRaises(desk_queue.RegisterError):
            write_register("| PI-042 | high | OPEN | a | b |")

    def test_only_the_first_table_is_read(self):
        rows = write_register("| PI-042 | high | OPEN | the issue |")
        self.assertEqual([r["id"] for r in rows], ["PI-042"])

    def test_the_live_registers_parse_and_leave_no_row_unparsed(self):
        # the regression itself, against the real files
        for name in desk_queue.REGISTER_ROLES:
            for row in desk_queue.list_rows(name):
                with self.subTest(register=name, row=row["id"]):
                    self.assertTrue(row["status"], f"{row['id']} parsed to an empty status")
                    self.assertEqual(len(row["cells"]), len(row["columns"]))


if __name__ == "__main__":
    unittest.main()
