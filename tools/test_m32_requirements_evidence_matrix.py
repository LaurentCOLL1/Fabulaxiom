"""Source-only matrix-to-checklist audit. Never invoke operator IO or runtime gates."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECK = (ROOT / "docs/continuity/M3_2_COMPLETION_MASTER_CHECKLIST_20261109.md").read_text(encoding="utf-8")
MATRIX = (ROOT / "docs/qualification/M3_2_REQUIREMENTS_EVIDENCE_MATRIX_CURRENT.md").read_text(encoding="utf-8")
TASK = re.compile(r"^- \[([ x])\] \*\*(M32-\d{3})\*\* ([^\n]+)", re.M)
ROW = re.compile(r"^\| (M32-\d{3}) \| ([x ]) \| (.*?) \| \x60([^\x60]+)\x60 \| \x60([^\x60]+)\x60 \| ([A-Z_]+) \|$", re.M)

class M32EvidenceMatrixContract(unittest.TestCase):
    def test_01_104_rows_match_current_canonical_checklist(self):
        tasks = [(m.group(2),m.group(1),m.group(3).strip()) for m in TASK.finditer(CHECK)]
        rows = [(m.group(1),m.group(2),m.group(3).replace(r"\|", "|").strip()) for m in ROW.finditer(MATRIX)]
        self.assertEqual(len(tasks),104)
        self.assertEqual(rows,tasks)

    def test_02_all_scope_labels_are_non_promoting_and_counts_match(self):
        rows = list(ROW.finditer(MATRIX))
        self.assertEqual(len(rows),104)
        closed = [m for m in rows if m.group(2)=="x"]
        self.assertEqual(len(closed),7)
        self.assertEqual(len(rows)-len(closed),97)
        self.assertEqual({m.group(1) for m in closed},
          {"M32-001","M32-002","M32-037","M32-049","M32-051","M32-095","M32-096"})
        for m in rows:
            if m.group(2)=="x":
                self.assertIn(m.group(6),{"CLOSED_GITHUB","CLOSED_DOCUMENTARY"})
            else:
                self.assertIn(m.group(6),{"OPEN_PARTIAL_ONLY","OPEN_UNPROVEN"})
        self.assertIn("- [ ] **M32-078**",CHECK)
        for marker in ("IN_PROGRESS_NOT_ACCEPTED", "NOT_PROVEN", "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
                       "PRODUCT_FIRST_PARALLEL_SAFETY", "NO_ACCEPTANCE_PROOF"):
            self.assertIn(marker,MATRIX)

    def test_03_referenced_sources_exist_or_missing_is_explicit(self):
        for m in ROW.finditer(MATRIX):
            for value in (m.group(4),m.group(5)):
                if value.startswith("NO_") or value.startswith("CHECKLIST_CLOSURE_"):
                    continue
                self.assertTrue((ROOT/value).is_file(),(m.group(1),value))

if __name__ == "__main__":
    unittest.main()
