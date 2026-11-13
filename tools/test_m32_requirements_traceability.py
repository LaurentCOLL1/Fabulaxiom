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
        for n in list(range(9,37))+list(range(38,49))+[52,63,64,88,89,90,93,94,97,98,99,100,101,102,103]:
            self.assertEqual(index[f"M32-{n:03d}"]["status"],"OPEN_NOT_ACCEPTED")
        self.assertIn("PENDING_EXTERNAL_ATTESTATION(21/3/2)",CHECK)
        self.assertIn("OPEN_NOT_REMEDIATED",CHECK)

    def test_m33_m9_and_comfyui_remain_outside_m32(self):
        for term in ("M3.3","M3.4","M3.5","M3.6","M4","M5","M6","M7","M8","M9","Ollama","ComfyUI"):
            self.assertIn(term,SCOPE)
        for term in ("M3.3","M3.6","M4","M5","M6","M7","M8","M9"):
            self.assertIn(term,ROADMAP)
        for n in ("078",):
            self.assertIn(f"- [ ] **M32-{n}**",CHECK)
        self.assertIn("- [x] **M32-104**",CHECK)
        self.assertIn("PRODUCT_FIRST_PARALLEL_SAFETY",SCOPE)

    def test_104_documentary_boundary_closure_never_grants_deferred_features(self):
        row = next(x for x in MATRIX["rows"] if x["id"] == "M32-104")
        self.assertEqual(row["status"], "CLOSED_SCOPED")
        self.assertIn("SHA=c4a04c59934064832dd7c700dcf39e25e729f88a",row["evidence"])
        self.assertIn("RUN=#43117900804",row["evidence"])
        self.assertIn("POSTMAIN_RUN=#43154409245",row["evidence"])
        self.assertIn("JOURNAL=#6825809694",row["evidence"])
        for marker in ("M32-104 [x]","M32-078 [ ]","IN_PROGRESS_NOT_ACCEPTED",
                       "PRODUCT_FIRST_PARALLEL_SAFETY","aucune admission"):
            self.assertIn(marker,SCOPE)
        for phrase in ("M3.3", "M3.4", "M3.5", "M3.6", "M4", "M5",
                       "M6", "M7", "M8", "M9", "Ollama", "ComfyUI"):
            self.assertIn(phrase,SCOPE)
        self.assertEqual(MATRIX["gate"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual((MATRIX["total"],MATRIX["closed"],MATRIX["open"]),(104,8,96))

    def test_104_provenance_records_never_invent_acceptance(self):
        """Workflow PASS is not a per-test PASS or operator admission."""
        expected = {
            "M32-001": (42699790716, "bef699511ff18e987a4858c797fde7aa88dfc59b", "2026-11-09", "push"),
            "M32-002": (42751838279, "fb523abbc05b636d98fd93240872882f4ee57f61", "2026-11-10", "pull_request"),
            **{
                i: (42997104616, "1f5e201d3e7d0ab088a65621411cc911de0472a1", "2026-11-11", "pull_request")
                for i in ("M32-037", "M32-049", "M32-051", "M32-095", "M32-096")
            },
            "M32-104": (43117900804, "c4a04c59934064832dd7c700dcf39e25e729f88a", "2026-11-11", "pull_request"),
        }
        self.assertEqual(MATRIX["provenance_review_date"], "2026-11-12")
        self.assertEqual(set(expected), {x["id"] for x in MATRIX["rows"] if x["status"]=="CLOSED_SCOPED"})
        for row in MATRIX["rows"]:
            proof = row["proof_audit"]
            with self.subTest(row=row["id"]):
                self.assertEqual(proof["record_review_date"], "2026-11-12")
                self.assertEqual(proof["test_target_name"], Path(row["verification_target"]).name)
                self.assertEqual(proof["target_role"],
                    "CANDIDATE_VERIFICATION_TARGET_NOT_AN_INDIVIDUAL_TEST_ATTESTATION")
                self.assertTrue(proof["acceptance_expectation"].strip())
                self.assertIsNone(proof["individual_test_step_result"])
                self.assertIs(proof["operator_runtime_acceptance"], False)
                if row["id"] in expected:
                    run, sha, date, event = expected[row["id"]]
                    self.assertEqual(proof["workflow_run_id"], run)
                    self.assertEqual(proof["workflow_head_sha"], sha)
                    self.assertEqual(proof["workflow_run_date"], date)
                    self.assertEqual(proof["workflow_event"], event)
                    self.assertEqual(proof["workflow_attempt"], 1)
                    self.assertEqual(proof["workflow_result"], "COMPLETED_SUCCESS_WORKFLOW_ONLY")
                    self.assertEqual(proof["workflow_log_reference"],
                        f"https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/{run}")
                    self.assertIn(sha,row["evidence"])
                    self.assertIn(f"#{run}",row["evidence"])
                else:
                    for key in ("workflow_run_id","workflow_head_sha","workflow_run_date",
                                "workflow_event","workflow_attempt","workflow_log_reference"):
                        self.assertIsNone(proof[key])
                    self.assertEqual(proof["workflow_result"], "NO_ACCEPTED_WORKFLOW")
                    self.assertEqual(row["evidence"], "NONE_ACCEPTED")
        self.assertEqual((MATRIX["total"],MATRIX["closed"],MATRIX["open"]),(104,8,96))
        self.assertIn("- [ ] **M32-078**", CHECK)

    def test_scoped_ci_job_steps_are_not_individual_test_or_operator_proofs(self):
        expected = {
            "M32-001": (129441151373, 28, "M3.2 living handoff source-only contract checks"),
            "M32-002": (129617016279, 28, "M3.2 living handoff source-only contract checks"),
            **{key: (130443816096, 30, "M3.2 five autonomous documentary and SQLite memory audit checks")
               for key in ("M32-037", "M32-049", "M32-051")},
            **{key: (130443816096, 27, "M3.2 V1 roadmap source-only consistency 9 tests")
               for key in ("M32-095", "M32-096")},
            "M32-104": (130850528111, 32,
                "M3.2 requirements test evidence 104-task matrix and deferred phase scope"),
        }
        self.assertEqual(MATRIX["workflow_step_review_date"], "2026-11-12")
        for row in MATRIX["rows"]:
            stage = row["workflow_step_audit"]
            with self.subTest(row=row["id"]):
                self.assertEqual(stage["step_review_date"], "2026-11-12")
                self.assertIs(stage["CI_step_does_not_equal_individual_test_assertion"], True)
                self.assertIs(stage["Windows_operator_workflow_admission"], False)
                self.assertIsNone(row["proof_audit"]["individual_test_step_result"])
                if row["id"] in expected:
                    job, number, name = expected[row["id"]]
                    self.assertEqual((stage["job_id"],stage["step_number"],stage["step_name"]),
                                     (job,number,name))
                    self.assertEqual(stage["step_conclusion"],
                                     "SUCCESS_OBSERVED_IN_TERMINAL_JOB")
                    self.assertEqual(stage["source_kind"],"GITHUB_ACTIONS_WINDOWS_STEP_ONLY")
                    self.assertIn(str(row["proof_audit"]["workflow_run_id"]),
                                  stage["step_log_locator"])
                    self.assertIn(str(job),stage["step_log_locator"])
                else:
                    self.assertEqual(stage["source_kind"],
                                     "NOT_ATTESTED_FOR_OPEN_REQUIREMENT")
                    self.assertEqual(stage["step_conclusion"],"NO_ACCEPTED_STEP")
                    for key in ("job_id","step_number","step_name","step_log_locator"):
                        self.assertIsNone(stage[key])
                    self.assertEqual(row["evidence"],"NONE_ACCEPTED")
        self.assertEqual((MATRIX["total"],MATRIX["closed"],MATRIX["open"]),(104,8,96))
        self.assertIn("- [ ] **M32-078**",CHECK)


    def test_five_open_requirements_gain_scoped_vitest_suite_logs_not_acceptance(self):
        """Observed CI log suite summary is NOT per-case, DB, writer or operator proof."""
        groups = {
            "M32-079": (352, 43318898667, "a3462fa7097d398021a1f4104fe2a19a64c95654",
                        131534076295, "src/m32WorldOrderIsolation.test.tsx", 6),
            "M32-082": (352, 43318898667, "a3462fa7097d398021a1f4104fe2a19a64c95654",
                        131534076295, "src/m32WorldOrderIsolation.test.tsx", 6),
            "M32-083": (352, 43318898667, "a3462fa7097d398021a1f4104fe2a19a64c95654",
                        131534076295, "src/m32WorldOrderIsolation.test.tsx", 6),
            "M32-075": (353, 43371849171, "47ee4ac962dd9fbe5a80e59edcf4662cb6429d3f",
                        131709174580, "src/m32WorldOrderBoundaries.test.tsx", 5),
            "M32-080": (353, 43371849171, "47ee4ac962dd9fbe5a80e59edcf4662cb6429d3f",
                        131709174580, "src/m32WorldOrderBoundaries.test.tsx", 5),
        }
        self.assertEqual(MATRIX["suite_observation_review_date"], "2026-11-13")
        self.assertEqual(MATRIX["status"],
                         "CANDIDATE_TEST_SUITE_LOG_EVIDENCE_ONLY_M32_078_OPEN")
        actual = {
            row["id"] for row in MATRIX["rows"]
            if "synthetic_suite_observation" in row
        }
        self.assertEqual(actual, set(groups))
        for row in MATRIX["rows"]:
            with self.subTest(requirement=row["id"]):
                if row["id"] not in groups:
                    self.assertNotIn("synthetic_suite_observation", row)
                    continue
                pr, run, sha, job, suite, count = groups[row["id"]]
                obs = row["synthetic_suite_observation"]
                self.assertEqual(row["status"], "OPEN_NOT_ACCEPTED")
                self.assertEqual(row["evidence"], "NONE_ACCEPTED")
                self.assertIsNone(row["proof_audit"]["individual_test_step_result"])
                self.assertIsNone(row["workflow_step_audit"]["job_id"])
                self.assertEqual(obs["observation_date"], "2026-11-13")
                self.assertEqual(obs["kind"], "WINDOWS_GITHUB_ACTIONS_VITEST_SUITE_LOG_ONLY")
                self.assertEqual(obs["pull_request_number"], pr)
                self.assertEqual(obs["source_head_sha"], sha)
                self.assertRegex(sha, r"^[0-9a-f]{40}$")
                self.assertEqual(obs["workflow_run_id"], run)
                self.assertEqual(obs["workflow_event"], "pull_request")
                self.assertEqual(obs["workflow_attempt"], 1)
                self.assertEqual(obs["workflow_status"], "COMPLETED_SUCCESS_EXACT_HEAD")
                self.assertEqual(obs["job_id"], job)
                self.assertEqual(obs["job_conclusion"], "success")
                self.assertEqual(obs["workflow_step_number"], 35)
                self.assertEqual(obs["workflow_step_name"], "Frontend tests")
                self.assertEqual(obs["workflow_step_conclusion"], "success")
                self.assertEqual(obs["suite_file"], suite)
                self.assertTrue((ROOT / suite).is_file())
                self.assertEqual(obs["suite_reported_tests"], count)
                self.assertEqual(obs["suite_log_marker"], f"{suite} ({count} tests)")
                self.assertEqual(obs["suite_log_locator"],
                    f"https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/{run}/job/{job}#step:35:1")
                self.assertEqual(obs["observation_result"],
                                 "SUITE_PASS_OBSERVED_NOT_NAMED_PER_CASE_ATTESTATION")
                self.assertEqual(obs["scope"], "SYNTHETIC_READ_ONLY_UNMOUNTED")
                for flag in ("requirement_acceptance", "sqlite_writer_acceptance",
                             "windows_operator_acceptance"):
                    self.assertIs(obs[flag], False)
        self.assertIn("- [ ] **M32-078**", CHECK)
        self.assertEqual((MATRIX["total"], MATRIX["closed"], MATRIX["open"]),
                         (104, 8, 96))

    def test_metadata_does_not_grant_writer_admission(self):
        self.assertEqual(MATRIX["gate"],"IN_PROGRESS_NOT_ACCEPTED")
        for term in ("R1–R9 NOT_PROVEN","G3 STOP_UNAVAILABLE","P4 STOP","Greenfield"):
            self.assertIn(term,SCOPE)

if __name__=="__main__":
    unittest.main()
