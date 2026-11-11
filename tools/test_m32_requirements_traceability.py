"""104 M3.2 requirement-to-evidence rows and phase-scope checks; repository reads only."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECK = (ROOT / "docs/continuity/M3_2_COMPLETION_MASTER_CHECKLIST_20261109.md").read_text(encoding="utf-8")
MATRIX = json.loads((ROOT / "docs/qualification/M3_2_REQUIREMENTS_TEST_EVIDENCE_MATRIX_20261111.json").read_text(encoding="utf-8"))
SCOPE = (ROOT / "docs/qualification/M3_2_SCOPE_BOUNDARY_20261111.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs/roadmap/FABULAXIOM_ROADMAP_V1.md").read_text(encoding="utf-8")
TASK = re.compile(r"^- \[([ x])\] \*\*(M32-\d{3})\*\* (.+?)\s*$", re.M)

class TraceabilityAndScope(unittest.TestCase):
    def test_exact_104_criteria_and_unique_order(self):
        declared = [(m.group(2),m.group(3).strip()) for m in TASK.finditer(CHECK)]
        stored = [(x["id"],x["criterion"]) for x in MATRIX["rows"]]
        self.assertEqual(stored,declared)
        self.assertEqual([x[0] for x in stored],[f"M32-{i:03d}" for i in range(1,105)])
        self.assertEqual(MATRIX["total"],104)

    def test_open_never_receives_a_false_proof(self):
        checked = {m.group(2):m.group(1) for m in TASK.finditer(CHECK)}
        for item in MATRIX["rows"]:
            expected = "CLOSED_SCOPED" if checked[item["id"]]=="x" else "OPEN_NOT_ACCEPTED"
            with self.subTest(item=item["id"]):
                self.assertEqual(item["status"],expected)
                if expected=="OPEN_NOT_ACCEPTED":
                    self.assertEqual(item["evidence"],"NONE_ACCEPTED")
                    self.assertTrue(item["next_proof"].strip())
                else:
                    self.assertRegex(item["evidence"],r"[0-9a-f]{40}")
                    self.assertRegex(item["evidence"],r"#[0-9]{7,}")
        closed = sum(x["status"]=="CLOSED_SCOPED" for x in MATRIX["rows"])
        self.assertEqual((closed,104-closed),(MATRIX["closed"],MATRIX["open"]))

    def test_old_pr331_sha_does_not_substitute_for_final_exact_ci(self):
        evidence = {x["id"]:x["evidence"] for x in MATRIX["rows"]}["M32-002"]
        self.assertIn("#42751838279",evidence)
        self.assertNotIn("#42674870251",evidence)

    def test_every_target_is_a_real_repo_file_and_every_gate_is_explicit(self):
        for row in MATRIX["rows"]:
            with self.subTest(row=row["id"]):
                self.assertTrue((ROOT/row["verification_target"]).is_file())
                self.assertTrue(row["track"] and row["gate"])

    def test_r1_r9_g2_and_later_release_not_falsely_closed(self):
        index={x["id"]:x for x in MATRIX["rows"]}
        for n in list(range(9,37))+list(range(38,49))+[52,63,64,88,89,90,93,94,97,98,99,100,101,102,103,104]:
            self.assertEqual(index[f"M32-{n:03d}"]["status"],"OPEN_NOT_ACCEPTED")
        self.assertIn("PENDING_EXTERNAL_ATTESTATION(21/3/2)",CHECK)
        self.assertIn("OPEN_NOT_REMEDIATED",CHECK)

    def test_m33_m9_and_comfyui_remain_outside_m32(self):
        for term in ("M3.3","M3.4","M3.5","M3.6","M4","M5","M6","M7","M8","M9","Ollama","ComfyUI"):
            self.assertIn(term,SCOPE)
        for term in ("M3.3","M3.6","M4","M5","M6","M7","M8","M9"):
            self.assertIn(term,ROADMAP)
        for n in ("078","104"):
            self.assertIn(f"- [ ] **M32-{n}**",CHECK)
        self.assertIn("PRODUCT_FIRST_PARALLEL_SAFETY",SCOPE)

    def test_metadata_does_not_grant_writer_admission(self):
        self.assertEqual(MATRIX["gate"],"IN_PROGRESS_NOT_ACCEPTED")
        for term in ("R1–R9 NOT_PROVEN","G3 STOP_UNAVAILABLE","P4 STOP","Greenfield"):
            self.assertIn(term,SCOPE)

if __name__=="__main__":
    unittest.main()
