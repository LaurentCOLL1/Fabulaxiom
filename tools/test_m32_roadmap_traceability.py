"""Read-only CI check: align all V1 roadmap documents with accepted M3 gates.

Dated textual contract only. No GitHub requests, no runtime or SQLite opening,
no approval grant. A source change requires a reviewed new status checkpoint.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "docs" / "roadmap"
FILES = (
    "FABULAXIOM_ROADMAP_V1.md",
    "M1_PERSISTENCE_PROJECT_FOUNDATION.md",
    "M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md",
    "M3_TIME_KNOWLEDGE_RELATIONSHIPS.md",
    "V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md",
)
STATUS = "ROADMAP_STATUS_CURRENT.md"
INDEX = "README.md"

class V1RoadmapTraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = {file: (ROADMAP / file).read_text(encoding="utf-8") for file in FILES}
        cls.status = (ROADMAP / STATUS).read_text(encoding="utf-8")
        cls.index = (ROADMAP / INDEX).read_text(encoding="utf-8")
        cls.handoff = (ROOT / "docs/continuity/HANDOFF_CURRENT.json").read_text(encoding="utf-8")

    def test_01_all_five_original_roadmaps_are_preserved(self):
        self.assertEqual(len(self.documents), 5)
        for filename, body in self.documents.items():
            self.assertGreater(len(body), 500, filename)
            self.assertIn("ROADMAP_STATUS_CURRENT.md", body, filename)

    def test_02_master_m0_m1_m2_completion_does_not_promote_m3(self):
        master = self.documents["FABULAXIOM_ROADMAP_V1.md"]
        self.assertIn("M0 —", master)
        self.assertIn("M1 —", master)
        self.assertIn("M2 —", master)
        self.assertIn("M3.2", master)
        self.assertIn("NON ACCEPTÉE", master)

    def test_03_m3_1_independently_normalized_not_only_planned(self):
        plan = self.documents["M3_TIME_KNOWLEDGE_RELATIONSHIPS.md"]
        for phrase in ("PR #33", "PR #34", "COMPLETE + MERGED + NORMALIZED",
                       "IN_PROGRESS_NOT_ACCEPTED"):
            self.assertIn(phrase, plan)
        self.assertIn("M3.1", self.status)
        self.assertIn("M3.2", self.status)
        self.assertIn("PR #34", self.status)

    def test_04_m3_2_manual_product_acceptance_not_confused_with_toys(self):
        plan = self.documents["M3_TIME_KNOWLEDGE_RELATIONSHIPS.md"]
        for phrase in ("Manual event/time anchor CRUD", "world chronology",
                       "narration order", "relative", "acceptance"):
            self.assertIn(phrase.lower(), plan.lower())
        for phrase in ("IN_PROGRESS_NOT_ACCEPTED", "PR #35",
                       "CRUD", "normalisation"):
            self.assertIn(phrase, self.status)

    def test_05_out_of_scope_work_is_not_preemptively_complete(self):
        for milestone in ("M3.3", "M3.4", "M3.5", "M3.6", "M4", "M5",
                          "M6", "M7", "M8", "M9"):
            self.assertIn(milestone, self.status)
        self.assertIn("NOT_STARTED_NOT_AUTHORIZED", self.status)

    def test_06_visual_proposal_still_cannot_be_implemented(self):
        proposal = self.documents["V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md"]
        self.assertIn("PROPOSAL_ONLY_NOT_AUTHORIZED", proposal)
        self.assertIn("#19", proposal)
        self.assertIn("PROPOSAL_ONLY_NOT_AUTHORIZED", self.status)
        self.assertIn("M1.5", proposal)

    def test_07_gate_prohibitions_survive_roadmap_reconciliation(self):
        for phrase in ("PASS_METADATA_ONLY_OWNER_REPORTED", "NOT_PROVEN",
                       "STOP_UNAVAILABLE", "NOT_AUTHORIZED",
                       "PENDING_EXTERNAL_ATTESTATION(21/3/2)", "NOT_STARTED",
                       "migration 007"):
            self.assertIn(phrase, self.status)
        for phrase in ("G2-B", "G3", "G6", "v6"):
            self.assertIn(phrase, self.status)
        self.assertIn('"g3": "STOP_UNAVAILABLE_NOT_AUTHORIZED"', self.handoff)

    def test_08_index_covers_every_roadmap_source(self):
        for filename in (*FILES, STATUS):
            self.assertIn(filename, self.index)
        self.assertIn("continuity/README.md", self.index)

    def test_09_checkpoint_is_explicitly_dated_and_not_a_new_permission(self):
        self.assertIn("20 octobre 2026", self.status)
        self.assertIn("non autorisation", self.status)
        self.assertIn("re-fetch", self.status.lower())

if __name__ == "__main__":
    unittest.main()
