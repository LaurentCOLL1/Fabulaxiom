"""Offline handoff policy checks; not a live GitHub or operator authorization."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs" / "continuity"

class HandoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((DIRECTORY / "HANDOFF_CURRENT.json").read_text(encoding="utf-8"))
        cls.doc = (DIRECTORY / "HANDOFF_CURRENT.md").read_text(encoding="utf-8")
        cls.policy = (DIRECTORY / "HANDOFF_PROTOCOL.md").read_text(encoding="utf-8")
        cls.index = (DIRECTORY / "README.md").read_text(encoding="utf-8")

    def test_01_dated_non_authorizing_checkpoint(self):
        self.assertEqual(self.data["status_kind"], "DATED_PUBLIC_SOURCE_HANDOFF_ONLY")
        self.assertTrue(self.data["live_refetch_required"])

    def test_02_repo_and_sha_format(self):
        self.assertEqual(self.data["repository"], "LaurentCOLL1/Fabulaxiom")
        for key in ("last_confirmed_main_before_handoff", "last_verified_pr_head"):
            self.assertRegex(self.data[key], r"^[0-9a-f]{40}$")

    def test_03_latest_verified_merge_not_promoted_to_runtime(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 91)
        self.assertEqual(self.data["g2a"]["corrected_execution"], "STOP_WEBVIEW2_PARENTAGE")

    def test_04_pr35_and_external_issues_still_open(self):
        self.assertEqual(self.data["pr35"], "OPEN_DRAFT")
        self.assertEqual(self.data["issues"], {"36": "OPEN", "38": "OPEN"})

    def test_05_no_implicit_windows_authorization(self):
        self.assertEqual(self.data["g2a"]["exact_corrected_script_owner_approval"],
                         "APPROVED_FOR_ONE_MANUAL_RUN_CONSUMED")
        self.assertEqual(self.data["g2a"]["future_script_approval"],
                         "NEW_EXPLICIT_APPROVAL_REQUIRED_FOR_ANY_FURTHER_MANUAL_RUN")
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")

    def test_06_prospective_and_historical_not_promoted(self):
        self.assertEqual(self.data["governance"]["prospective"], "NOT_STARTED")
        self.assertEqual(self.data["governance"]["historic"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(self.data["governance"]["tauri_runtime"], "NOT_TESTED")

    def test_07_required_stop_scope(self):
        required = {"G2B", "G2C", "G2D", "G3", "G4", "G5", "G6",
                    "MIGRATION_007", "WRITER_IPC", "PR35_MERGE", "RELEASE"}
        self.assertTrue(required.issubset(set(self.data["prohibited"])))

    def test_08_all_critical_documents_in_index(self):
        for filename in ("HANDOFF_CURRENT.md", "HANDOFF_CURRENT.json",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md",
                         "NEXT.md", "STATE.md", "RESUME_PROMPT.md"):
            self.assertIn(filename, self.index)
            self.assertTrue((DIRECTORY / filename).is_file(), filename)

    def test_09_handoff_points_to_current_source(self):
        self.assertIn("SearchHost.exe", self.doc)
        self.assertIn("PR #86", self.doc)
        self.assertIn(self.data["last_confirmed_main_before_handoff"], self.doc)
        self.assertIn("STOP_WEBVIEW2_PARENTAGE", self.doc)

    def test_10_operator_stop_cannot_promote_any_gate(self):
        g = self.data['g2a']
        self.assertEqual(g['pr86_historic_stop']['stage'], 'WEBVIEW2_PARENTAGE')
        self.assertEqual(g['pr86_historic_stop']['reason'], 'UNEXPECTED_OR_UNSAFE')
        self.assertEqual(g['pr86_historic_stop']['subcause'], 'NOT_IDENTIFIABLE_FROM_SANITIZED_OUTPUT')
        self.assertEqual(g['absence_of_sqlite_writer'], 'NOT_PROVEN')
        self.assertEqual(self.data['governance']['prospective'], 'NOT_STARTED')
        self.assertEqual(self.data['governance']['tauri_runtime'], 'NOT_TESTED')
        self.assertIn('STOP_STAGE: WEBVIEW2_PARENTAGE', self.doc)
        self.assertIn('STOP_PROCESS_NAMES', self.doc)

    def test_11_new_candidate_stays_unexecuted_and_separate(self):
        c = self.data["g2a"]["future_candidate"]
        self.assertEqual(c["operator_execution"], "PASS_METADATA_ONLY_OWNER_REPORTED_SINGLE_RUN")
        self.assertEqual(c["cause_of_operator_stop"], "UNKNOWN_HISTORIC_PR86")
        self.assertEqual(c["review"], "EXACT_SCRIPT_REVIEWED_AND_ONE_TIME_RUN_CONSUMED")
        self.assertEqual(c["development_status"], "SOURCE_MERGED_AND_OWNER_REPORTED_LOCAL_METADATA_PASS")
        self.assertEqual(c["ci_run"], 39339365546)
        self.assertEqual(c["source_review_completed"], True)
        self.assertTrue((ROOT / c["path"]).is_file())
        self.assertIn("M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md", self.index)
        self.assertIn("STOP_WEBVIEW2_PARENTAGE", self.doc)

    def test_12_local_metadata_pass_stays_tightly_bounded(self):
        g = self.data["g2a"]
        observation = g["latest_operator_observation"]
        self.assertEqual(observation["g2a_local_metadata"], "PASS")
        self.assertEqual(observation["webview2_searchhost_lineage"], 6)
        self.assertEqual(observation["lineage_evidence"], "OBSERVED_METADATA_ONLY")
        self.assertEqual(observation["webview2_ownership_authenticated"], "NO")
        self.assertEqual(observation["process_writer_absence"], "NOT_PROVEN")
        self.assertEqual(observation["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(observation["tauri_runtime"], "NOT_TESTED")
        self.assertEqual(observation["authorized_single_manual_execution"], "CONSUMED")
        self.assertEqual(g["absence_of_sqlite_writer"], "NOT_PROVEN")
        self.assertEqual(g["pr86_historic_stop"]["actual_runtime"], "STOP_WEBVIEW2_PARENTAGE")
        self.assertIn("G2A_LOCAL_METADATA: PASS", self.doc)
        self.assertIn("G2B_G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED", self.doc)

    def test_13_writer_gap_is_source_only_refusal(self):
        review = self.data["g2a"]["writer_absence_review"]
        self.assertEqual(review["writer_absence"], "NOT_PROVEN")
        self.assertEqual(review["operator_execution"], "NOT_PERFORMED_NOT_AUTHORIZED")
        self.assertEqual(review["trusted_nonmigrating_owner"], "NOT_ESTABLISHED")
        self.assertEqual(review["even_all_fictional_checks_true"], "REAL_G3_STILL_STOP_UNAVAILABLE")
        self.assertEqual(review["open_private_sqlite_or_sidecars"], "PROHIBITED")
        self.assertEqual(self.data["g2a"]["latest_operator_observation"]["g2a_local_metadata"], "PASS")
        self.assertIn("M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md", self.doc)
        self.assertIn("M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md", self.index)
        self.assertIn("PROCESS_WRITER_ABSENCE: NOT_PROVEN", self.doc)

    def test_14_runtime_entrypoint_source_audit_is_not_g3_permission(self):
        d = self.data["g2a"]["runtime_entrypoint_source_audit"]
        self.assertTrue(d["source_only"])
        self.assertEqual(d["original_sqlite_access"], "PROHIBITED")
        self.assertEqual(d["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(d["writer_absence"], "NOT_PROVEN")
        self.assertEqual(d["operator_execution"], "NOT_AUTHORIZED")
        self.assertIn("TEXTUAL", d["warning"])
        self.assertTrue((ROOT / d["document"]).is_file())
        self.assertTrue((ROOT / d["script"]).is_file())
        self.assertTrue((ROOT / d["tests"]).is_file())
        self.assertIn("M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md", self.doc)
        self.assertIn("M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md", self.index)

    def test_15_current_gate_decision_cannot_promote_a_downstream_gate(self):
        d = self.data["gate_decision_current"]
        self.assertEqual(d["status"], "DATED_PUBLIC_SOURCE_HANDOFF_ONLY")
        self.assertEqual(d["scope"], "DOCUMENTARY_DECISION_NOT_EXECUTABLE")
        self.assertEqual(d["g2a"], "PASS_METADATA_ONLY_OWNER_REPORTED")
        for gate in ("g2b", "g2c", "g2d", "g4", "g5", "g6"):
            self.assertEqual(d[gate], "NOT_AUTHORIZED")
        self.assertEqual(d["g3"], "STOP_UNAVAILABLE_NOT_AUTHORIZED")
        self.assertEqual(d["process_writer_absence"], "NOT_PROVEN")
        self.assertEqual(d["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(d["prospective"], "NOT_STARTED")
        self.assertEqual(d["last_operator_consent"], "SINGLE_G2A_PID_ZERO_RUN_CONSUMED")
        self.assertTrue((ROOT / d["document"]).is_file())
        self.assertIn("M3_2_GATE_DECISION_CURRENT.md", self.index)
        self.assertIn("M3_2_GATE_DECISION_CURRENT.md", self.doc)

    def test_16_wide_rust_sqlite_inventory_never_permits_real_g3(self):
        i = self.data["g2a"]["wide_rust_sqlite_inventory"]
        self.assertEqual(i["operator_execution"], "NOT_AUTHORIZED")
        self.assertEqual(i["actual_sqlite_access"], "NONE")
        self.assertEqual(i["absence_of_writer"], "NOT_PROVEN")
        self.assertEqual(i["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(i["gate_promotion"], "NEVER_AUTOMATIC")
        self.assertEqual(i["baseline_matched_files"], 21)
        self.assertEqual(i["test_count"], 18)
        self.assertTrue((ROOT / i["document"]).is_file())
        self.assertTrue((ROOT / i["scanner"]).is_file())
        self.assertTrue((ROOT / i["tests"]).is_file())
        self.assertIn("M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md", self.doc)
        self.assertIn("M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md", self.index)

    def test_17_preopened_ram_reader_only_toy_no_operator_access(self):
        t = self.data["g2a"]["preopened_ram_query_only_toy"]
        self.assertEqual(t["gates"], "CFG_TEST_AND_NONDEFAULT_FEATURE_ONLY")
        self.assertEqual(t["test_count"], 13)
        self.assertEqual(t["migration_invoked"], "NO")
        self.assertEqual(t["disk_source_opened"], "NONE")
        self.assertEqual(t["operator_execution"], "NOT_AUTHORIZED")
        self.assertEqual(t["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(t["absence_of_real_writer"], "NOT_PROVEN")
        self.assertEqual(t["permission_promotion"], "NEVER")
        self.assertTrue((ROOT / t["document"]).is_file())
        self.assertTrue((ROOT / t["rust_module"]).is_file())
        self.assertIn("M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md", self.doc)
        self.assertIn("M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md", self.index)

    def test_18_external_writer_in_memory_counterexample_not_production_proof(self):
        e = self.data["g2a"]["other_writer_ram_counterexample"]
        self.assertEqual(e["sample_count"], 12)
        self.assertEqual(e["disk_sqlite_access"], "NONE")
        self.assertEqual(e["windows_operator_execution"], "NOT_AUTHORIZED")
        self.assertEqual(e["query_only_global_exclusion"], "FALSE")
        self.assertEqual(e["reader_total_changes_detects_other_writer"], "FALSE")
        self.assertEqual(e["actual_other_writer_absence"], "NOT_PROVEN")
        self.assertEqual(e["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(e["permissions"], "NO_GATE_PROMOTION")
        self.assertTrue((ROOT / e["tests"]).is_file())
        self.assertTrue((ROOT / e["document"]).is_file())
        self.assertIn("M3_2_SHARED_RAM_EXTERNAL_WRITER_NEGATIVE_PROOF.md", self.doc)
        self.assertIn("M3_2_SHARED_RAM_EXTERNAL_WRITER_NEGATIVE_PROOF.md", self.index)

    def test_19_v1_roadmap_audit_is_dated_not_completion(self):
        r = self.data["roadmap_alignment"]
        self.assertEqual(r["m3_1"], "COMPLETE_MERGED_NORMALIZED_PR33_PR34")
        self.assertEqual(r["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(r["m3_2_product_acceptance"],
                         "MISSING_REAL_MANUAL_CHRONOLOGY_CRUD_UI_WINDOWS_EVIDENCE_NORMALIZATION")
        self.assertEqual(r["future_m3_3_to_m3_6"], "NOT_STARTED_NOT_AUTHORIZED")
        self.assertEqual(r["m4_to_m9"], "NOT_STARTED_NOT_AUTHORIZED")
        self.assertEqual(r["comfyui"], "PROPOSAL_ONLY_NOT_AUTHORIZED")
        self.assertTrue(r["no_local_operator_commands"])
        self.assertEqual(r["expected_tests"], 9)
        for p in (*r["source_files"], r["index"], r["current"], r["check"]):
            self.assertTrue((ROOT / p).is_file())
        self.assertIn("ROADMAP_STATUS_CURRENT.md", self.doc)
        self.assertIn("ROADMAP_STATUS_CURRENT.md", self.index)

    def test_20_manual_chronology_candidate_only_in_synthetic_lab(self):
        x = self.data["m3_2_product_progress"]
        self.assertEqual(x["delivery"], "SYNTHETIC_BROWSER_LAB_ONLY_SOURCE_ONLY")
        self.assertEqual(x["expected_tests"], 55)
        self.assertEqual(x["browser_new_cases"], 2)
        self.assertEqual(x["browser_total_expected"], 48)
        self.assertEqual(x["app_tauri_production_integration"], "NONE")
        self.assertEqual(x["sqlite_real_access"], "NONE")
        self.assertEqual(x["operator_windows_acceptance"], "NOT_STARTED")
        self.assertEqual(x["m3_2_milestone"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["owner_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        for p in (x["document"], x["reducer"], x["user_interface"],
                  x["isolated_mount"], x["tests"]):
            self.assertTrue((ROOT / p).is_file())
        self.assertIn("M3_2_SYNTHETIC_MANUAL_CHRONOLOGY_LAB.md", self.doc)

    def test_21_exact_scene_revision_binding_stays_fictional(self):
        x = self.data["m3_2_product_progress"]
        r = x["scene_revision_binding"]
        self.assertEqual(x["expected_tests"], 55)
        self.assertEqual(x["browser_total_expected"], 48)
        self.assertEqual(r["fixture_catalog_limit"], 128)
        self.assertEqual(r["source_head_resolution"], "NEVER")
        self.assertFalse(r["accepts_cross_universe"])
        self.assertEqual(r["persisted_sqlite_access"], "NONE")
        self.assertEqual(r["operator_windows_execution"], "NOT_AUTHORIZED")
        self.assertEqual(x["m3_2_milestone"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertTrue((ROOT / r["doc"]).is_file())
        self.assertIn("M3_2_FICTIONAL_SCENE_REVISION_EXACT_BINDING.md", self.doc)

    def test_22_conflict_preview_never_promotes_operator_gate(self):
        x = self.data["m3_2_product_progress"]
        c = x["conflict_preflight"]
        self.assertEqual(c["preview_function"], "previewFictionalPrecedence")
        self.assertEqual(c["correction_function"], "previewFictionalCorrection")
        self.assertEqual(c["expected_unit_tests"], 32)
        self.assertEqual(c["expected_browser_cases"], 36)
        self.assertEqual(c["state_mutations_by_previewer"], "NONE")
        self.assertEqual(c["source_revision_head_lookup"], "NEVER")
        self.assertEqual(c["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(c["gates"], "G2B_TO_G6_NOT_AUTHORIZED")
        self.assertEqual(c["status"], "MERGED_SOURCE_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertTrue((ROOT / c["document"]).is_file())
        self.assertIn("M3_2_FICTIONAL_CONFLICT_WITNESS_AND_CORRECTION_PREFLIGHT.md", self.doc)

    def test_23_pr100_merge_status_not_runtime_acceptance(self):
        p = self.data["post_pr100_normalization"]
        self.assertEqual(self.data["last_confirmed_merged_pr"], 110)
        self.assertEqual(p["main_merge_sha"], "bf59b28b437470a4759a5971968e8f00f9fa895c")
        self.assertEqual(p["pr_head_sha"], "95e2e0385979e2b226aa1d6289e12250c6e6e19d")
        self.assertEqual(p["pr_ci"]["run_id"], 39533766395)
        self.assertEqual(p["main_ci"]["run_id"], 39534698504)
        self.assertEqual(p["test_laboratory"]["vitest"], 32)
        self.assertEqual(p["test_laboratory"]["chromium"], 36)
        self.assertTrue(p["test_laboratory"]["fictional_only"])
        self.assertEqual(p["product_m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(p["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertIn("39534698504", self.doc)

    def test_25_multinovel_fixture_candidate_never_implies_real_g3(self):
        m = self.data["m3_2_product_progress"]["multinovel_browser"]
        self.assertEqual(m["status"], "MERGED_SOURCE_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertEqual(m["total_unit_tests_expected"], 36)
        self.assertEqual(m["total_chromium_cases_expected"], 38)
        self.assertEqual(m["new_unit_tests"], 4)
        self.assertEqual(m["new_chromium_cases"], 2)
        self.assertEqual(m["reader_reveal_status"], "not_authored")
        self.assertTrue(m["no_cross_novel_world_order_inference"])
        self.assertEqual(m["real_sqlite_access"], "NONE")
        self.assertEqual(m["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(m["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")

    def test_26_pr102_postmerge_snapshot_is_documentary_only(self):
        x = self.data["post_pr102_normalization"]
        self.assertEqual(x["merged_pr"], 102)
        self.assertEqual(x["merge_sha"], "1f0a8cd9a369106202b57102aa28915de65b7472")
        self.assertEqual(x["pr_head_sha"], "07baf294286d427185c0817310d82418eb8c3fd2")
        self.assertEqual(x["pr_ci"]["run_id"], 39543328344)
        self.assertEqual(x["main_ci"]["run_id"], 39544279201)
        self.assertEqual(x["synthetic_tests"], {"vitest": 36, "chromium": 38})
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["windows_operator_execution"], "NONE")
        self.assertIn("39544279201", self.doc)

    def test_27_three_orders_comparator_stays_fictional_and_read_only(self):
        x = self.data["m3_2_product_progress"]["three_orders_comparator"]
        self.assertEqual(x["status"], "MERGED_SOURCE_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertEqual(x["function"], "previewFictionalThreeOrders")
        self.assertEqual(x["world_order"], "INDETERMINATE")
        self.assertEqual(x["cross_novel_order"], "INDETERMINATE")
        self.assertEqual(x["reader_reveal"], "NOT_AUTHORED")
        self.assertTrue(x["no_inference_from_manuscript_to_world"])
        self.assertEqual(x["unit_total_expected"], 42)
        self.assertEqual(x["browser_total_expected"], 41)
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")
        self.assertIn("comparaison des trois ordres", self.doc)

    def test_28_pr104_postmerge_is_fictional_not_operator_permission(self):
        x = self.data["post_pr104_normalization"]
        self.assertEqual(x["pr"], 104)
        self.assertEqual(x["merge_sha"], "997b60901e1f18a426eae3efa34ddb29c07b5721")
        self.assertEqual(x["source_head"], "b320b711763659d9a3af670b685254eeb8b815e9")
        self.assertEqual(x["ci_pr"]["run_id"], 39553745685)
        self.assertEqual(x["ci_pr"]["conclusion"], "SUCCESS")
        self.assertEqual(x["ci_main"]["run_id"], 39554622761)
        self.assertEqual(self.data["post_pr104_normalization"]["ci_main"]["conclusion"], "SUCCESS")
        self.assertEqual(x["ci_main"]["conclusion"], "SUCCESS")
        self.assertTrue(x["synthetic_only"])
        self.assertEqual(x["vitest"], 42)
        self.assertEqual(x["chromium"], 41)
        self.assertEqual(x["product"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("39554622761", self.doc)

    def test_29_human_witness_panel_is_fiction_only_and_not_authority(self):
        x = self.data["m3_2_product_progress"]["human_witness_panel"]
        self.assertEqual(x["status"], "MERGED_SOURCE_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertEqual(x["existing_comparison_module"], "M32WorldOrderComparison")
        self.assertEqual(x["proof_source"], "EXPLICIT_ACTIVE_HUMAN_EDGES_ONLY")
        self.assertFalse(x["allows_revoked_witnesses"])
        self.assertEqual(x["world_order_from_narration"], "NEVER")
        self.assertEqual(x["reader_reveal"], "NOT_AUTHORED")
        self.assertEqual(x["unit_total_expected"], 48)
        self.assertEqual(x["browser_total_expected"], 44)
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["sqlite_access"], "NONE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("preuves humaines fictives", self.doc)

    def test_30_pr106_merge_does_not_accept_m32_or_authorize_sqlite(self):
        x = self.data["post_pr106_normalization"]
        self.assertEqual(x["merged_pr"], 106)
        self.assertEqual(x["merge_sha"], "fbfc785afa6e5bdf92c337004d1bd2f925c4957a")
        self.assertEqual(x["source_head"], "4abcc5217be07cb65d089e55fa042ff757b9043e")
        self.assertEqual(x["pr_ci"]["run_id"], 39566947725)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39567933461)
        self.assertEqual(self.data["post_pr106_normalization"]["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["vitest"], 48)
        self.assertEqual(x["chromium"], 44)
        self.assertTrue(x["fiction_only"])
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_runtime"], "NONE")
        self.assertIn("39567933461", self.doc)

    def test_31_historic_selection_is_ui_only_no_gate_promotion(self):
        x = self.data["m3_2_product_progress"]["historical_selection_guard"]
        self.assertEqual(x["status"], "MERGED_SOURCE_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertEqual(x["stale_proof"], "SUPPRESSED")
        self.assertEqual(x["historical_option"], "DISABLED_IN_CONTROL")
        self.assertTrue(x["retired_identity_not_used_for_current_proof"])
        self.assertEqual(x["other_universe_selection"], "CLEARED_ON_SCENARIO_SWITCH")
        self.assertEqual(x["vitest_total_expected"], 51)
        self.assertEqual(x["chromium_total_expected"], 46)
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_sqlite"], "NONE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertIn("PR #108 fusionnée : sélections historiques explicites", self.doc)

    def test_32_pr108_merge_does_not_accept_real_m32(self):
        x = self.data["post_pr108_normalization"]
        self.assertEqual(x["merged_pr"], 108)
        self.assertEqual(x["merge_sha"], "ba4b8a599910cef6d1c76fa1e4fb561a0b45e631")
        self.assertEqual(x["pr_head_sha"], "fd62c1afd4ad6eff9a6f9d2f18679ef0704f59c1")
        self.assertEqual(x["pr_ci"]["run_id"], 39572172593)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39573518324)
        self.assertEqual(self.data["main_ci_post_merge"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["vitest"], 51)
        self.assertEqual(x["chromium"], 46)
        self.assertTrue(x["fiction_only"])
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("39573518324", self.doc)

    def test_33_preview_of_fictional_revocation_does_not_authorize_real_writes(self):
        x = self.data["m3_2_product_progress"]["revocation_impact_preview"]
        self.assertEqual(x["status"], "MERGED_SOURCE_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertEqual(x["after_state"], "HYPOTHETICAL_WITHOUT_WRITES")
        self.assertEqual(x["before_state"], "EXPLICIT_ACTIVE_HUMAN_EDGE_ONLY")
        self.assertEqual(x["preserved_alternate_witness"], "ACTIVE_HUMAN_PATH_ONLY")
        self.assertEqual(x["unit_total_expected"], 55)
        self.assertEqual(x["browser_total_expected"], 48)
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertIn("conséquence d'une révocation humaine", self.doc)

    def test_34_pr110_merge_keeps_g2_to_g6_stopped(self):
        x = self.data["post_pr110_normalization"]
        self.assertEqual(self.data["last_confirmed_merged_pr"], 110)
        self.assertEqual(self.data["last_confirmed_main_before_handoff"], x["merge_sha"])
        self.assertEqual(self.data["last_verified_pr_head"], x["pr_head_sha"])
        self.assertEqual(x["pr_ci"]["run_id"], 39577527093)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39591429432)
        self.assertEqual(x["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(x["vitest"], 55)
        self.assertEqual(x["chromium_per_mode"], 48)
        self.assertTrue(x["fiction_only"])
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #110 fusionnée", self.doc)

    def test_24_policy_requires_refetch_and_same_pr_handoff(self):
        for clause in ("Re-fetch", "HANDOFF_CURRENT.md", "HANDOFF_CURRENT.json",
                       "expected_head_sha", "autorisation"):
            self.assertIn(clause, self.policy)

if __name__ == "__main__":
    unittest.main()
