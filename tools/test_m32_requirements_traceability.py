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

SCOPED_CLOSED_IDS = frozenset({
    "M32-001", "M32-002", "M32-004", "M32-005", "M32-006", "M32-037", "M32-049", "M32-051",
    "M32-094", "M32-095", "M32-096", "M32-104",
})

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
        for n in list(range(9,37))+list(range(38,49))+[52,63,64,88,89,90,93,97,98,99,100,101,102,103]:
            self.assertEqual(index[f"M32-{n:03d}"]["status"],"OPEN_NOT_ACCEPTED")
        self.assertIn("PENDING_EXTERNAL_ATTESTATION(21/3/2)",CHECK)
        self.assertIn("OPEN_NOT_REMEDIATED",CHECK)
        self.assertEqual(index["M32-094"]["status"], "CLOSED_SCOPED")
        self.assertEqual(index["M32-093"]["status"], "OPEN_NOT_ACCEPTED")

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
        self.assertEqual((MATRIX["total"],MATRIX["closed"],MATRIX["open"]),(104,len(SCOPED_CLOSED_IDS),104-len(SCOPED_CLOSED_IDS)))

    def test_104_provenance_records_never_invent_acceptance(self):
        """Workflow PASS is not a per-test PASS or operator admission."""
        expected = {
            "M32-001": (42699790716, "bef699511ff18e987a4858c797fde7aa88dfc59b", "2026-11-09", "push"),
            "M32-002": (42751838279, "fb523abbc05b636d98fd93240872882f4ee57f61", "2026-11-10", "pull_request"),
            "M32-004": (44604279698, "d9a8187aa889d08b6f943a38c539fca5d435f746", "2026-11-19", "pull_request"),
            "M32-005": (44778790112, "e0f318ece1fdae29e567e453db455b695e813e9a", "2026-11-20", "pull_request"),
            "M32-006": (44800413136, "27edacd94728f87b0e0ed6ff70bccc9e99331a08", "2026-11-20", "pull_request"),
            **{
                i: (42997104616, "1f5e201d3e7d0ab088a65621411cc911de0472a1", "2026-11-11", "pull_request")
                for i in ("M32-037", "M32-049", "M32-051", "M32-095", "M32-096")
            },
            "M32-094": (43594666828, "5206bba7f3196c454a22bf85d0d0dca879ee20e3", "2026-11-14", "pull_request"),
            "M32-104": (43117900804, "c4a04c59934064832dd7c700dcf39e25e729f88a", "2026-11-11", "pull_request"),
        }
        self.assertEqual(MATRIX["provenance_review_date"], "2026-11-12")
        self.assertEqual(set(expected), {x["id"] for x in MATRIX["rows"] if x["status"]=="CLOSED_SCOPED"})
        for row in MATRIX["rows"]:
            proof = row["proof_audit"]
            with self.subTest(row=row["id"]):
                self.assertEqual(proof["record_review_date"],
                                 "2026-11-20" if row["id"] in ("M32-005", "M32-006") else
                                  "2026-11-19" if row["id"] == "M32-004" else
                                 ("2026-11-14" if row["id"] == "M32-094" else "2026-11-12"))
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
        self.assertEqual((MATRIX["total"],MATRIX["closed"],MATRIX["open"]),(104,len(SCOPED_CLOSED_IDS),104-len(SCOPED_CLOSED_IDS)))
        self.assertIn("- [ ] **M32-078**", CHECK)

    def test_scoped_ci_job_steps_are_not_individual_test_or_operator_proofs(self):
        expected = {
            "M32-001": (129441151373, 28, "M3.2 living handoff source-only contract checks"),
            "M32-002": (129617016279, 28, "M3.2 living handoff source-only contract checks"),
            "M32-004": (135843672704, 31, "M3.2 master completion checklist 104-item closure evidence contracts"),
            "M32-005": (136435646377, 31, "M3.2 master completion checklist 104-item closure evidence contracts"),
            "M32-006": (136510779675, 31, "M3.2 master completion checklist 104-item closure evidence contracts"),
            **{key: (130443816096, 30, "M3.2 five autonomous documentary and SQLite memory audit checks")
               for key in ("M32-037", "M32-049", "M32-051")},
            **{key: (130443816096, 27, "M3.2 V1 roadmap source-only consistency 9 tests")
               for key in ("M32-095", "M32-096")},
            "M32-094": (132446512015, 58,
                "M3.2 Linux Rust selected GLib/GTK advisory exposure audit (no Linux build)"),
            "M32-104": (130850528111, 32,
                "M3.2 requirements test evidence 104-task matrix and deferred phase scope"),
        }
        self.assertEqual(MATRIX["workflow_step_review_date"], "2026-11-12")
        for row in MATRIX["rows"]:
            stage = row["workflow_step_audit"]
            with self.subTest(row=row["id"]):
                self.assertEqual(stage["step_review_date"],
                                 "2026-11-20" if row["id"] in ("M32-005", "M32-006") else
                                  "2026-11-19" if row["id"] == "M32-004" else
                                 ("2026-11-14" if row["id"] == "M32-094" else "2026-11-12"))
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
        self.assertEqual((MATRIX["total"],MATRIX["closed"],MATRIX["open"]),(104,len(SCOPED_CLOSED_IDS),104-len(SCOPED_CLOSED_IDS)))
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
                         (104,len(SCOPED_CLOSED_IDS),104-len(SCOPED_CLOSED_IDS)))


    def test_v6_named_cases_in_ci_do_not_close_open_requirements(self):
        """CI attests 11 synthetic case titles, not SQLite/writer/operator admission."""
        self.assertEqual(MATRIX["named_case_observation_review_date"], "2026-11-13")
        source = MATRIX["named_case_observation_source"]
        self.assertEqual((source["pull_request"], source["workflow_run_id"],
                          source["job_id"], source["step_number"], source["named_synthetic_cases"]),
                         (355, 43473302734, 132050546622, 36, 11))
        self.assertIs(source["requirement_acceptance"], False)
        self.assertIs(source["writer_acceptance"], False)
        groups = {"M32-075": ("src/m32WorldOrderBoundaries.test.tsx", 5),
                  "M32-080": ("src/m32WorldOrderBoundaries.test.tsx", 5),
                  "M32-079": ("src/m32WorldOrderIsolation.test.tsx", 6),
                  "M32-082": ("src/m32WorldOrderIsolation.test.tsx", 6),
                  "M32-083": ("src/m32WorldOrderIsolation.test.tsx", 6)}
        self.assertEqual({r["id"] for r in MATRIX["rows"]
                          if "synthetic_named_case_observation" in r}, set(groups))
        for row in MATRIX["rows"]:
            if row["id"] not in groups:
                self.assertNotIn("synthetic_named_case_observation", row)
                continue
            suite, count = groups[row["id"]]
            obs = row["synthetic_named_case_observation"]
            self.assertEqual((obs["workflow_run_id"], obs["job_id"], obs["workflow_step_number"]),
                             (43473302734, 132050546622, 36))
            self.assertEqual(obs["suite_file"], suite)
            self.assertEqual(obs["named_case_count"], count)
            self.assertEqual(len(obs["named_case_titles"]), count)
            self.assertEqual(len(set(obs["named_case_titles"])), count)
            for title in obs["named_case_titles"]:
                self.assertIn(title, (ROOT / suite).read_text(encoding="utf-8"))
            self.assertEqual(obs["negative_guard_cases"], 13)
            self.assertEqual(obs["workflow_step_conclusion"], "success")
            self.assertEqual(obs["scope"], "SYNTHETIC_READ_ONLY_UNMOUNTED")
            for flag in ("requirement_acceptance", "sqlite_writer_acceptance", "windows_operator_acceptance"):
                self.assertIs(obs[flag], False)
            self.assertEqual(row["status"], "OPEN_NOT_ACCEPTED")
            self.assertEqual(row["evidence"], "NONE_ACCEPTED")
            self.assertIsNone(row["proof_audit"]["individual_test_step_result"])
            self.assertIsNone(row["workflow_step_audit"]["job_id"])
        self.assertEqual((MATRIX["total"], MATRIX["closed"], MATRIX["open"]), (104,len(SCOPED_CLOSED_IDS),104-len(SCOPED_CLOSED_IDS)))
        self.assertIn("- [ ] **M32-078**", CHECK)

    def test_094_scoped_graph_proof_preserves_linux_risk_and_writer_stop(self):
        row = next(r for r in MATRIX["rows"] if r["id"] == "M32-094")
        proof = row["target_separation_scope"]
        self.assertEqual(row["status"], "CLOSED_SCOPED")
        self.assertEqual(proof["scope"], "CARGO_SELECTED_TARGET_GRAPH_ONLY")
        self.assertEqual(proof["source"], {
            "head_sha": "5206bba7f3196c454a22bf85d0d0dca879ee20e3",
            "run": 43594666828, "job": 132446512015})
        self.assertEqual(proof["windows"], {
            "target": "x86_64-pc-windows-msvc", "step": 57,
            "packages": 247, "glib_gtk_selected": False})
        self.assertEqual(proof["linux"], {
            "target": "x86_64-unknown-linux-gnu", "step": 58,
            "packages": 277, "glib": "0.18.5", "gtk": "0.18.2",
            "webkit2gtk": "2.0.2", "advisory": "GHSA-wrw7-89jp-8q8g",
            "risk": "OPEN_NOT_REMEDIATED"})
        self.assertEqual(proof["postmain"], {
            "head_sha": "8cba5e0bd758a39a501a5ee04c3957deec1ad36c",
            "run": 43610824403, "conclusion": "success"})
        for key in ("runtime_reachability_proven", "linux_build_performed",
                    "linux_distribution_authorized", "operator_data_access",
                    "writer_admission"):
            self.assertIs(proof[key], False)
        self.assertIn("- [x] **M32-094**", CHECK)
        self.assertIn("- [ ] **M32-093**", CHECK)
        self.assertIn("- [ ] **M32-092**", CHECK)
        self.assertEqual(
            set(SCOPED_CLOSED_IDS),
            {r["id"] for r in MATRIX["rows"] if r["status"]=="CLOSED_SCOPED"})


    def test_20261119_four_open_requirements_have_exact_scoped_named_chromium_evidence(self):
        """Real GitHub job logs verified outside CI; source contract must not turn them into admission."""
        expected = {
            "M32-070": (392, 44412057826, "c8dce8c150b50d528c04a32779a6e8ded1fbe2c4",
                        135182534955, 44416272668, "38a9dc204f6f1a9d768c6d9e45519b472e420e8c",
                        "109-fictional-event-revisions-match-explicit-active-anchor",
                        "19 offers only the exact current anchor revision, without implicit selection",
                        "FORM_EXPLICIT_ANCHOR_COMPATIBLE_REVISION_ONLY"),
            "M32-071": (393, 44453364420, "bd42eaedfc60bb300cce647013540ab62b3b1013",
                        135322434231, 44455249407, "411d5a677feba151248e3e69c6225dc3a6876aab",
                        "110-fictional-event-history-readable-after-withdrawal",
                        "20 exposes an explicit read-only history picker without implicit inspection",
                        "READONLY_FICTIONAL_EVENT_HISTORY_ONLY"),
            "M32-075": (393, 44453364420, "bd42eaedfc60bb300cce647013540ab62b3b1013",
                        135322434231, 44455249407, "411d5a677feba151248e3e69c6225dc3a6876aab",
                        "111-fictional-event-history-escaped-and-universe-isolated",
                        None, "REACT_ESCAPE_AND_UNIVERSE_REMOUNT_ONLY"),
            "M32-081": (393, 44453364420, "bd42eaedfc60bb300cce647013540ab62b3b1013",
                        135322434231, 44455249407, "411d5a677feba151248e3e69c6225dc3a6876aab",
                        "110-fictional-event-history-readable-after-withdrawal",
                        "21 keeps a withdrawn event selectable as history without restoring it",
                        "WITHDRAWN_EVENT_HISTORY_RETAINED_IN_RAM_ONLY"),
        }
        self.assertEqual(MATRIX["latest_named_chromium_observation_review_date"], "2026-11-19")
        self.assertEqual(MATRIX["latest_named_chromium_observation_status"],
                         "FOUR_OPEN_REQUIREMENTS_HAVE_PARTIAL_FICTIONAL_CASE_LOGS_NO_ADMISSION")
        self.assertEqual({row["id"] for row in MATRIX["rows"]
                          if "latest_named_chromium_observation" in row}, set(expected))
        chromium = (ROOT / "tools/m32_browser_interaction.cjs").read_text(encoding="utf-8")
        vitest = (ROOT / "src/m32FictionalEventManualWorkshop.test.tsx").read_text(encoding="utf-8")
        self.assertIn("M32_BROWSER_REAL_CHROMIUM_PASS 111/111", chromium)
        for row in MATRIX["rows"]:
            if row["id"] not in expected:
                self.assertNotIn("latest_named_chromium_observation", row)
                continue
            (pr, run, sha, job, post, postsha, case, vitest_name, scope) = expected[row["id"]]
            obs = row["latest_named_chromium_observation"]
            with self.subTest(requirement=row["id"]):
                self.assertEqual(row["status"], "OPEN_NOT_ACCEPTED")
                self.assertEqual(row["evidence"], "NONE_ACCEPTED")
                self.assertEqual(obs["date"], "2026-11-19")
                self.assertEqual(obs["evidence_kind"], "EXACT_HEAD_NAMED_CHROMIUM_CASE_LOG_SYNTHETIC_ONLY")
                self.assertEqual((obs["pull_request_number"], obs["source_workflow_run_id"],
                                  obs["source_workflow_head_sha"], obs["source_workflow_job_id"]),
                                 (pr, run, sha, job))
                self.assertRegex(sha, r"^[0-9a-f]{40}$")
                self.assertEqual(obs["source_log_locator"],
                                 f"https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/{run}/job/{job}")
                self.assertEqual(obs["source_workflow_conclusion"], "completed_success")
                self.assertEqual((obs["independent_postmain_run_id"],
                                  obs["independent_postmain_head_sha"],
                                  obs["independent_postmain_conclusion"]),
                                 (post, postsha, "completed_success"))
                self.assertEqual(obs["named_chromium_case"], case)
                self.assertIn(case, chromium)
                self.assertEqual(obs["chromium_source_file"], "tools/m32_browser_interaction.cjs")
                self.assertEqual(obs["scoped_vitest_suite"],
                                 "src/m32FictionalEventManualWorkshop.test.tsx")
                self.assertEqual(obs["scoped_vitest_case_title"], vitest_name)
                if vitest_name:
                    self.assertIn(vitest_name, vitest)
                self.assertEqual(obs["observation_scope"], scope)
                for flag in ("requirement_acceptance", "writer_admission",
                             "operator_acceptance", "p4_runtime_authorized"):
                    self.assertIs(obs[flag], False)
                self.assertIs(obs["individual_case_is_not_entire_requirement"], True)
                self.assertIsNone(row["proof_audit"]["individual_test_step_result"])
                self.assertIsNone(row["workflow_step_audit"]["job_id"])
        self.assertIn("- [ ] **M32-078**", CHECK)
        self.assertEqual((MATRIX["total"], MATRIX["closed"], MATRIX["open"]),
                         (104, len(SCOPED_CLOSED_IDS), 104-len(SCOPED_CLOSED_IDS)))

    def test_20261119_traceability_observation_cannot_promote_open_requirements(self):
        """Adversarial tampering to a source SHA or operator flag must fail the scoped contract."""
        observed = {
            row["id"]: row["latest_named_chromium_observation"]
            for row in MATRIX["rows"] if "latest_named_chromium_observation" in row
        }
        for requirement in ("M32-070", "M32-071", "M32-075", "M32-081"):
            value = observed[requirement]
            with self.subTest(requirement=requirement):
                self.assertNotEqual(value["source_workflow_head_sha"], "0" * 40)
                self.assertIs(value["operator_acceptance"], False)
                self.assertIs(value["writer_admission"], False)
                self.assertEqual(next(row for row in MATRIX["rows"]
                                      if row["id"] == requirement)["status"], "OPEN_NOT_ACCEPTED")
        self.assertEqual(MATRIX["gate"], "IN_PROGRESS_NOT_ACCEPTED")


    def test_m32_004_scoped_handoff_closure_retains_negative_scope(self):
        row = next(x for x in MATRIX["rows"] if x["id"] == "M32-004")
        self.assertEqual(row["status"], "CLOSED_SCOPED")
        self.assertIn("- [x] **M32-004**", CHECK)
        self.assertIn("POSTMAIN_RUN=#44611547386", row["evidence"])
        self.assertIn("POSTMAIN_SHA=9ec8aef81198f3ce8f376ce78435c43aa320351d",
                      row["evidence"])
        self.assertIn("NO_OPERATOR_ADMISSION", row["evidence"])
        self.assertFalse(row["proof_audit"]["operator_runtime_acceptance"])
        self.assertFalse(row["workflow_step_audit"]["Windows_operator_workflow_admission"])
        self.assertEqual(MATRIX["gate"], "IN_PROGRESS_NOT_ACCEPTED")
        for number in ("009","020","031","039","042","071","078"):
            self.assertIn(f"- [ ] **M32-{number}**", CHECK)


    def test_m32_005_scoped_dated_status_truth_without_operator_admission(self):
        row = next(x for x in MATRIX["rows"] if x["id"] == "M32-005")
        self.assertEqual(row["status"], "CLOSED_SCOPED")
        self.assertIn("- [x] **M32-005**", CHECK)
        self.assertIn("RUN=#44778790112", row["evidence"])
        self.assertIn("POSTMAIN_RUN=#44789068367", row["evidence"])
        self.assertIn("POSTMAIN_SHA=087996c2f62e4c7a90b7afc1d57031917d7b3701",
                      row["evidence"])
        self.assertIn("NO_OPERATOR_ADMISSION", row["evidence"])
        self.assertFalse(row["proof_audit"]["operator_runtime_acceptance"])
        self.assertFalse(row["workflow_step_audit"]["Windows_operator_workflow_admission"])
        self.assertEqual(MATRIX["gate"], "IN_PROGRESS_NOT_ACCEPTED")
        for id in ("M32-007","M32-071","M32-075","M32-078","M32-081"):
            self.assertEqual(next(x for x in MATRIX["rows"] if x["id"] == id)["status"],
                             "OPEN_NOT_ACCEPTED")

    def test_m32_006_scoped_audit_is_not_writer_or_deletion_proof(self):
        row = next(x for x in MATRIX["rows"] if x["id"] == "M32-006")
        self.assertEqual(row["status"], "CLOSED_SCOPED")
        self.assertIn("- [x] **M32-006**", CHECK)
        self.assertIn("POSTMAIN_RUN=#44818205234",row["evidence"])
        self.assertIn("NO_DELETION_HISTORY_PROOF",row["evidence"])
        self.assertFalse(row["proof_audit"]["operator_runtime_acceptance"])
        self.assertFalse(row["workflow_step_audit"]["Windows_operator_workflow_admission"])
        self.assertIn("- [ ] **M32-007**",CHECK)

    def test_20261121_pr215_23_path_and_p3bh_observations_do_not_close_gates(self):
        index={x["id"]:x for x in MATRIX["rows"]}
        for i in ("M32-007","M32-075"):
            self.assertEqual(index[i]["status"],"OPEN_NOT_ACCEPTED")
            self.assertEqual(index[i]["evidence"],"NONE_ACCEPTED")
            self.assertIn(f"- [ ] **{i}**",CHECK)
        view=index["M32-007"]["latest_pr215_scoped_observation"]
        self.assertEqual((view["paths"],view["identical"],view["different"],view["absent"]),
                         (23,6,17,0))
        self.assertEqual(view["source_main"],
                         "c4122c575f1e19b903acf5ca268cc6ab9d09f4fd")
        self.assertTrue((ROOT/view["report"]).is_file())
        self.assertFalse(view["old_tree_truncated"])
        self.assertFalse(view["main_tree_truncated"])
        self.assertFalse(view["requirement_acceptance"])
        self.assertFalse(view["writer_admission"])
        self.assertFalse(view["operator_acceptance"])
        x=index["M32-075"]["latest_p3bh_candidate"]
        self.assertIn("38 shows an explicit reset button",x["test_case"])
        self.assertIn("NOT_RUN",x["source_ci_status"])
        self.assertFalse(x["browser_click_attested"])
        self.assertFalse(x["operator_acceptance"])
        self.assertFalse(x["requirement_acceptance"])
        self.assertEqual((MATRIX["total"],MATRIX["closed"],MATRIX["open"]),(104,12,92))

    def test_metadata_does_not_grant_writer_admission(self):
        self.assertEqual(MATRIX["gate"],"IN_PROGRESS_NOT_ACCEPTED")
        for term in ("R1–R9 NOT_PROVEN","G3 STOP_UNAVAILABLE","P4 STOP","Greenfield"):
            self.assertIn(term,SCOPE)

if __name__=="__main__":
    unittest.main()
